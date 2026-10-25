"""Confere na Publora o andamento das publicações já enviadas (somente leitura na Publora).

Uso: python ferramentas/conferir.py
- Para cada item com postGroupId e estado "agendado", consulta GET /get-post/<postGroupId>.
- Atualiza o estado local para "publicado" (com postedId) ou "erro" (com o motivo).
- Escreve o resumo no log e no resumo do GitHub Actions.
"""
import datetime as dt
import json
import os
import sys

import requests

ARQ = "dados/publicacoes.json"
BASE = "https://api.publora.com/api/v1"


def main():
    chave = os.environ.get("PUBLORA_API_KEY")
    if not chave:
        print("::error::Secret PUBLORA_API_KEY não encontrado.")
        sys.exit(1)
    itens = json.load(open(ARQ, encoding="utf-8"))
    agora = dt.datetime.now(dt.timezone.utc).isoformat()
    linhas = []
    mudou = False
    for item in itens:
        pg = item.get("postGroupId")
        if not pg or item.get("estado") not in ("agendado",):
            continue
        r = requests.get(f"{BASE}/get-post/{pg}", headers={"x-publora-key": chave}, timeout=30)
        if r.status_code != 200:
            linhas.append(f"{item['id']}: Publora respondeu {r.status_code} {r.text[:150]}")
            continue
        g = r.json()
        posts = g.get("posts") or []
        st_plat = [p.get("status") for p in posts]
        midias = g.get("media") or []
        prontas = sum(1 for m in midias if m.get("status") == "ready")
        linhas.append(
            f"{item['id']}: grupo={g.get('status')} · plataformas={st_plat} · horário={g.get('scheduledTime')} · imagens prontas={prontas}/{len(midias)}"
        )
        publicado = next((p for p in posts if p.get("status") == "published"), None)
        falhou = next((p for p in posts if p.get("status") == "failed"), None)
        if publicado:
            item["estado"] = "publicado"
            item["postedId"] = publicado.get("postedId")
            item["link"] = publicado.get("permalink")
            item.setdefault("historico", []).append({"data": agora, "estado": "publicado", "nota": f"Publora confirmou publicação (postedId {publicado.get('postedId')})."})
            mudou = True
        elif falhou:
            erro = falhou.get("error") or {}
            item["estado"] = "erro"
            item.setdefault("historico", []).append({"data": agora, "estado": "erro", "nota": f"{erro.get('code')}: {erro.get('message')}"})
            with open("registro/erros.md", "a", encoding="utf-8") as f:
                f.write(f"\n- {agora[:10]}: publicação {item['id']} falhou na Publora: {erro.get('code')} {erro.get('message')}\n")
            mudou = True
    if mudou:
        json.dump(itens, open(ARQ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    texto = "\n".join(linhas) or "Nenhuma publicação agendada para conferir."
    print(texto)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as s:
            s.write(texto + "\n")


if __name__ == "__main__":
    main()
