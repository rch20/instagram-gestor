"""Leitor de métricas reais do @diaebeleza pela API oficial (Graph API), só leitura.

Uso (no GitHub Actions, com o secret META_IG_TOKEN):
  python ferramentas/metricas.py

Salva dados/metricas/AAAA-MM-DD-api.json (dado bruto, com fonte e hora) e dados/metricas/AAAA-MM-DD-api.md (resumo).
Nada aqui publica, comenta ou segue: só GET.

Métricas (Graph API v21, 2025-2026):
- Conta: seguidores, posts; por dia nos últimos 28 dias: alcance, visualizações, visitas ao perfil, cliques no link
  da bio, contas que interagiram, interações; seguidores ganhos/perdidos.
- Cada post: alcance, visualizações, curtidas, comentários, salvamentos, compartilhamentos, interações,
  visitas ao perfil e seguidores vindos do post (quando a Meta entrega para aquele formato).
A Meta não entrega todas as métricas para todo formato; quando uma falha, fica registrada como indisponível
(nunca inventada).
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from publicar_ig import chamar, conta_ig  # noqa: E402

FUSO = dt.timezone(dt.timedelta(hours=-3))
METRICAS_CONTA = ["reach", "views", "profile_views", "website_clicks", "accounts_engaged", "total_interactions",
                  "likes", "comments", "saves", "shares", "follows_and_unfollows"]
METRICAS_POST = ["reach", "views", "likes", "comments", "saved", "shares", "total_interactions",
                 "profile_visits", "follows"]
NOMES = {
    "reach": "alcance", "views": "visualizações", "profile_views": "visitas ao perfil",
    "website_clicks": "cliques no link da bio", "accounts_engaged": "contas que interagiram",
    "total_interactions": "interações", "likes": "curtidas", "comments": "comentários", "saves": "salvamentos",
    "saved": "salvamentos", "shares": "compartilhamentos", "profile_visits": "visitas ao perfil",
    "follows": "seguidores vindos do post", "follows_and_unfollows": "seguir / deixar de seguir",
}


def metrica_conta(ig, nome, desde, ate):
    """Total do período (metric_type=total_value). Devolve número, dict (quebras) ou o erro."""
    try:
        r = chamar("GET", f"{ig}/insights", metric=nome, period="day", metric_type="total_value",
                   since=int(desde.timestamp()), until=int(ate.timestamp()))
        d = (r.get("data") or [{}])[0]
        tv = d.get("total_value") or {}
        if tv.get("breakdowns"):
            return {"total": tv.get("value"), "quebras": tv["breakdowns"]}
        return tv.get("value")
    except Exception as e:  # noqa: BLE001
        return {"indisponivel": str(e)[:200]}


def metricas_post(mid):
    saida = {}
    for m in METRICAS_POST:
        try:
            r = chamar("GET", f"{mid}/insights", metric=m)
            vals = (r.get("data") or [{}])[0].get("values") or [{}]
            saida[m] = vals[0].get("value")
        except Exception:  # noqa: BLE001
            saida[m] = None  # a Meta não entrega essa métrica para este formato
    return saida


def main():
    agora = dt.datetime.now(FUSO)
    ig = conta_ig()
    perfil = chamar("GET", ig, fields="username,name,biography,website,followers_count,follows_count,media_count")
    ate = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    periodos = {"7d": ate - dt.timedelta(days=7), "28d": ate - dt.timedelta(days=28)}
    conta = {p: {m: metrica_conta(ig, m, desde, ate) for m in METRICAS_CONTA} for p, desde in periodos.items()}

    posts = []
    lista = chamar("GET", f"{ig}/media", fields="id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count", limit=50)
    for p in lista.get("data", []):
        posts.append({
            "id": p["id"], "tipo": p.get("media_product_type") or p.get("media_type"), "quando": p.get("timestamp"),
            "link": p.get("permalink"), "legenda_inicio": (p.get("caption") or "")[:90],
            "metricas": metricas_post(p["id"]),
        })

    bruto = {
        "fonte": "Instagram Graph API v21 (META_IG_TOKEN, usuário do sistema Publicador), só leitura",
        "coletado_em": agora.isoformat(timespec="seconds"),
        "periodos": {k: {"desde": v.date().isoformat(), "ate": ate.date().isoformat()} for k, v in periodos.items()},
        "perfil": perfil, "conta": conta, "posts": posts,
    }
    os.makedirs("dados/metricas", exist_ok=True)
    base = f"dados/metricas/{agora.date().isoformat()}-api"
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump(bruto, f, ensure_ascii=False, indent=1)

    def fmt(v):
        if isinstance(v, dict):
            if "indisponivel" in v:
                return "indisponível"
            return str(v.get("total"))
        return "—" if v is None else str(v)

    linhas = [f"# Métricas reais do @diaebeleza — {agora.strftime('%d/%m/%Y %H:%M')}",
              "", f"Fonte: {bruto['fonte']}.", "",
              f"Seguidores: {perfil.get('followers_count')} · seguindo: {perfil.get('follows_count')} · posts: {perfil.get('media_count')}", "",
              "| Conta | 7 dias | 28 dias |", "|---|---|---|"]
    for m in METRICAS_CONTA:
        linhas.append(f"| {NOMES.get(m, m)} | {fmt(conta['7d'][m])} | {fmt(conta['28d'][m])} |")
    linhas += ["", "| Post | Tipo | Alcance | Visualizações | Salvos | Compart. | Visitas perfil | Seguidores |", "|---|---|---|---|---|---|---|---|"]
    for p in posts:
        mm = p["metricas"]
        quando = (p["quando"] or "")[:10]
        linhas.append(f"| [{quando}]({p['link']}) {p['legenda_inicio'][:40].replace('|', '/').replace(chr(10), ' ')} | {p['tipo']} | "
                      f"{fmt(mm.get('reach'))} | {fmt(mm.get('views'))} | {fmt(mm.get('saved'))} | {fmt(mm.get('shares'))} | "
                      f"{fmt(mm.get('profile_visits'))} | {fmt(mm.get('follows'))} |")
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print("\n".join(linhas[:20]))


if __name__ == "__main__":
    main()
