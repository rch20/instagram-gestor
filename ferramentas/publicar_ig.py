"""Publica no Instagram pela API oficial (Instagram API com login do Instagram), sem a Publora.

Uso (no GitHub Actions):
  python ferramentas/publicar_ig.py testar        -> só confere se a chave funciona (não publica nada)
  python ferramentas/publicar_ig.py <id>          -> publica AGORA o item <id>

Chave: secret META_IG_TOKEN (nunca em arquivo, commit ou conversa).
As imagens/vídeos precisam de link público: usamos o raw.githubusercontent.com deste repositório (público).

Travas (qualquer uma falhando = nada é publicado):
- item existe, está "aprovado", não é "collab_manual" nem "manual" (esses o dono publica pelo app);
- item não tem postGroupId (já está na Publora) nem ig_media_id/link (já publicado);
- "agendado_para" com fuso, no máximo 30 min no futuro e no máximo 24 h no passado;
- formatos: post/carrossel (1 a 10 JPEGs), reel (reel.mp4), story (1 JPEG 1080x1920);
- legenda até 2.200 caracteres (story não usa legenda).
"""
import datetime as dt
import glob
import json
import os
import sys
import time

import requests

API = "https://graph.instagram.com/v21.0"
RAW = "https://raw.githubusercontent.com/rch20/instagram-gestor/{ref}/{path}"
ARQ = "dados/publicacoes.json"


def falha(msg, codigo=1):
    print(f"::error::{msg}")
    sys.exit(codigo)


def token():
    t = os.environ.get("META_IG_TOKEN", "").strip()
    if not t:
        falha("Secret META_IG_TOKEN não configurado.")
    return t


def chamar(metodo, caminho, **params):
    params["access_token"] = token()
    r = requests.request(metodo, f"{API}/{caminho}", data=params if metodo == "POST" else None,
                         params=params if metodo == "GET" else None, timeout=60)
    try:
        corpo = r.json()
    except ValueError:
        corpo = {"texto": r.text[:300]}
    if r.status_code >= 400 or "error" in corpo:
        erro = corpo.get("error", corpo)
        raise RuntimeError(f"{r.status_code}: {json.dumps(erro, ensure_ascii=False)[:400]}")
    return corpo


def esperar(container_id, limite_s=300):
    inicio = time.time()
    while time.time() - inicio < limite_s:
        st = chamar("GET", container_id, fields="status_code,status").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Container {container_id} com status {st}.")
        time.sleep(8)
    raise RuntimeError(f"Container {container_id} não ficou pronto em {limite_s}s.")


def testar():
    eu = chamar("GET", "me", fields="user_id,username,account_type,media_count")
    print(f"Conectado: @{eu.get('username')} · tipo {eu.get('account_type')} · {eu.get('media_count')} posts")
    if eu.get("username", "").lower() != "diaebeleza":
        falha(f"A chave é da conta @{eu.get('username')}, não do @diaebeleza.")


def publicar(alvo):
    ref = os.environ.get("GITHUB_SHA", "main")
    itens = json.load(open(ARQ, encoding="utf-8"))
    item = next((i for i in itens if i.get("id") == alvo), None)
    if not item:
        falha(f"Publicação {alvo} não existe.")
    if item.get("estado") != "aprovado":
        falha(f"{alvo} está como '{item.get('estado')}'. Só 'aprovado' pode ser publicado.")
    if item.get("canal") in ("collab_manual", "manual"):
        falha(f"{alvo} é publicado pelo dono, pelo app (canal {item.get('canal')}). Nada feito.")
    if item.get("postGroupId") or item.get("ig_media_id") or item.get("link"):
        falha(f"{alvo} já foi enviado ou publicado. Nada feito.")

    quando = item.get("agendado_para")
    try:
        momento = dt.datetime.fromisoformat(quando or "")
    except ValueError:
        falha(f"'agendado_para' inválido: {quando}")
    if momento.tzinfo is None:
        falha("'agendado_para' precisa ter fuso.")
    agora = dt.datetime.now(dt.timezone.utc)
    if momento > agora + dt.timedelta(minutes=30):
        falha(f"Cedo demais: {alvo} é para {quando}.")
    if momento < agora - dt.timedelta(hours=24):
        falha(f"{alvo} passou da data ({quando}) há mais de 24 h; precisa de nova data.")

    pasta = item.get("pasta_artes", "")
    formato = item.get("formato", "post")
    legenda = item.get("legenda") or ""
    if formato != "story" and (not legenda.strip() or len(legenda) > 2200):
        falha("Legenda vazia ou maior que 2.200 caracteres.")
    url = lambda p: RAW.format(ref=ref, path=p)  # noqa: E731

    try:
        if formato == "reel":
            video = os.path.join(pasta, "reel.mp4")
            if not os.path.isfile(video):
                falha("Reel sem reel.mp4 na pasta de artes.")
            c = chamar("POST", "me/media", media_type="REELS", video_url=url(video), caption=legenda,
                       share_to_feed="true")["id"]
            esperar(c, 600)
        else:
            fotos = sorted(glob.glob(os.path.join(pasta, "*.jpg")))
            if formato == "story":
                if len(fotos) != 1:
                    falha(f"Story precisa de exatamente 1 JPEG (tem {len(fotos)}).")
                c = chamar("POST", "me/media", media_type="STORIES", image_url=url(fotos[0]))["id"]
                esperar(c)
            elif len(fotos) == 1:
                c = chamar("POST", "me/media", image_url=url(fotos[0]), caption=legenda)["id"]
                esperar(c)
            elif 2 <= len(fotos) <= 10:
                filhos = []
                for f in fotos:
                    fid = chamar("POST", "me/media", image_url=url(f), is_carousel_item="true")["id"]
                    esperar(fid)
                    filhos.append(fid)
                c = chamar("POST", "me/media", media_type="CAROUSEL", children=",".join(filhos),
                           caption=legenda)["id"]
                esperar(c)
            else:
                falha(f"A pasta tem {len(fotos)} JPEGs; o Instagram aceita de 1 a 10.")
        media_id = chamar("POST", "me/media_publish", creation_id=c)["id"]
        link = chamar("GET", media_id, fields="permalink").get("permalink")
    except RuntimeError as e:
        item["estado"] = "erro"
        item.setdefault("historico", []).append({"data": agora.isoformat(), "estado": "erro", "nota": str(e)[:300]})
        json.dump(itens, open(ARQ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        with open("registro/erros.md", "a", encoding="utf-8") as f:
            f.write(f"\n- {agora.date()}: falha ao publicar {alvo} pela API do Instagram: {str(e)[:300]}\n")
        falha(f"Instagram recusou: {e}", 2)

    item["estado"] = "publicado"
    item["ig_media_id"] = media_id
    item["link"] = link
    item.setdefault("historico", []).append({
        "data": agora.isoformat(), "estado": "publicado",
        "nota": f"Publicado direto pela API do Instagram ({formato}). {link}",
    })
    json.dump(itens, open(ARQ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Publicado: {alvo} · {link}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        falha("Informe 'testar' ou o id da publicação.")
    testar() if sys.argv[1] == "testar" else publicar(sys.argv[1].strip())
