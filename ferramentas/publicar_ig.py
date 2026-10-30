"""Publica no Instagram pela API oficial (Graph API com login do Facebook), sem a Publora.

Chave (29/10/2026): token do usuário do sistema "Publicador" do portfólio @dia&beleza (não vence),
com acesso só à Página Dia e Beleza e ao @diaebeleza. A conta do Instagram é achada pela Página.

Uso (no GitHub Actions):
  python ferramentas/publicar_ig.py testar        -> só confere se a chave funciona (não publica nada)
  python ferramentas/publicar_ig.py <id>          -> publica AGORA o item <id>
  python ferramentas/publicar_ig.py devidos       -> (a cada 15 min) publica o item "canal": "api" cuja hora chegou

Canal (30/10/2026): itens com "canal": "api" saem por aqui na hora de "agendado_para"; a Publora não os aceita.
O modo "devidos" respeita a pausa (dados/config.json), publica no máximo 1 item por vez e não publica
nada com mais de 3 h de atraso (só avisa), para não soltar post fora de hora.

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
import subprocess
import sys
import time

import requests

API = "https://graph.facebook.com/v21.0"
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


_IG = None


def conta_ig():
    """Id da conta do Instagram @diaebeleza, achada pelas Páginas que a chave enxerga (ou META_IG_USER_ID)."""
    global _IG
    if _IG:
        return _IG
    fixo = os.environ.get("META_IG_USER_ID", "").strip()
    if fixo:
        _IG = fixo
        return _IG
    paginas = chamar("GET", "me/accounts", fields="name,instagram_business_account{id,username}").get("data", [])
    for p in paginas:
        ig = p.get("instagram_business_account") or {}
        if (ig.get("username") or "").lower() == "diaebeleza":
            _IG = ig["id"]
            return _IG
    falha("A chave não enxerga nenhuma Página com o @diaebeleza ligado.")


def testar():
    eu = chamar("GET", conta_ig(), fields="username,media_count,followers_count")
    print(f"Conectado: @{eu.get('username')} · {eu.get('media_count')} posts · {eu.get('followers_count')} seguidores")
    if (eu.get("username") or "").lower() != "diaebeleza":
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
            c = chamar("POST", f"{conta_ig()}/media", media_type="REELS", video_url=url(video), caption=legenda,
                       share_to_feed="true")["id"]
            esperar(c, 600)
        else:
            fotos = sorted(glob.glob(os.path.join(pasta, "*.jpg")))
            if formato == "story":
                if len(fotos) != 1:
                    falha(f"Story precisa de exatamente 1 JPEG (tem {len(fotos)}).")
                c = chamar("POST", f"{conta_ig()}/media", media_type="STORIES", image_url=url(fotos[0]))["id"]
                esperar(c)
            elif len(fotos) == 1:
                c = chamar("POST", f"{conta_ig()}/media", image_url=url(fotos[0]), caption=legenda)["id"]
                esperar(c)
            elif 2 <= len(fotos) <= 10:
                filhos = []
                for f in fotos:
                    fid = chamar("POST", f"{conta_ig()}/media", image_url=url(f), is_carousel_item="true")["id"]
                    esperar(fid)
                    filhos.append(fid)
                c = chamar("POST", f"{conta_ig()}/media", media_type="CAROUSEL", children=",".join(filhos),
                           caption=legenda)["id"]
                esperar(c)
            else:
                falha(f"A pasta tem {len(fotos)} JPEGs; o Instagram aceita de 1 a 10.")
        media_id = chamar("POST", f"{conta_ig()}/media_publish", creation_id=c)["id"]
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


ATRASO_MAX = dt.timedelta(hours=3)
ADIANTADO = dt.timedelta(hours=4)  # o agendamento do GitHub atrasa horas: a execução pega o item antes e espera a hora


def devidos(agora=None):
    """Escolhe o próximo item do canal "api" (hora já chegou ou chega em até 4 h). Retorna (id, hora) ou None."""
    agora = agora or dt.datetime.now(dt.timezone.utc)
    config = json.load(open("dados/config.json", encoding="utf-8"))
    if config.get("pausado"):
        print("Instagram pausado pelo dono: nada publicado.")
        return None
    prontos = []
    for i in json.load(open(ARQ, encoding="utf-8")):
        if i.get("canal") != "api" or i.get("estado") != "aprovado":
            continue
        if i.get("postGroupId") or i.get("ig_media_id") or i.get("link"):
            continue
        try:
            m = dt.datetime.fromisoformat(i.get("agendado_para") or "")
        except ValueError:
            print(f"::warning::{i['id']} sem 'agendado_para' válido.")
            continue
        if m.tzinfo is None:
            print(f"::warning::{i['id']}: 'agendado_para' sem fuso.")
        elif m < agora - ATRASO_MAX:
            print(f"::warning::{i['id']} passou da hora ({i['agendado_para']}) há mais de 3 h: precisa de nova data. Nada publicado.")
        elif m <= agora + ADIANTADO:
            prontos.append((m, i["id"]))
    if not prontos:
        print("Nada para publicar agora.")
        return None
    m, alvo = sorted(prontos)[0]
    return alvo, m


def esperar_e_publicar():
    """O agendamento do GitHub atrasa (às vezes horas): a execução pega o item até 4 h antes, espera a hora,
    atualiza o repositório (pausa ou mudança do dono durante a espera valem) e só então publica."""
    achado = devidos()
    if not achado:
        return
    alvo, m = achado
    falta = (m - dt.datetime.now(dt.timezone.utc)).total_seconds()
    if falta > 0:
        print(f"{alvo}: esperando até {m.isoformat()} ({int(falta // 60)} min).")
        sys.stdout.flush()
        time.sleep(falta)
    subprocess.run(["git", "pull", "-q", "--rebase"], check=False)
    if json.load(open("dados/config.json", encoding="utf-8")).get("pausado"):
        print("Instagram pausado pelo dono durante a espera: nada publicado.")
        return
    publicar(alvo)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        falha("Informe 'testar', 'devidos' ou o id da publicação.")
    alvo = sys.argv[1].strip()
    if alvo == "testar":
        testar()
    elif alvo == "devidos":
        esperar_e_publicar()
    else:
        publicar(alvo)
