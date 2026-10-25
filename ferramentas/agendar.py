"""Agenda na Publora UMA publicação aprovada pelo dono.

Uso (no GitHub Actions): python ferramentas/agendar.py <id>

Travas (qualquer uma falhando = nada é enviado):
- o item existe em dados/publicacoes.json e está com estado "aprovado";
- o item ainda não tem postGroupId (nunca agenda duas vezes);
- tem "agendado_para" em ISO 8601 com fuso, pelo menos 15 minutos no futuro
  (sem horário a biblioteca publicaria na hora; isso nunca é permitido aqui);
- a pasta de artes tem de 1 a 10 JPEGs;
- a legenda tem no máximo 2.200 caracteres.
"""
import datetime as dt
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "instagram-skills"))
from lib.publora_client import PubloraClient, PubloraError  # noqa: E402

ARQ = "dados/publicacoes.json"
CONEXAO = "dados/conexao-publora.json"


def falha(msg):
    print(f"::error::{msg}")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        falha("Informe o id da publicação.")
    alvo = sys.argv[1].strip()
    itens = json.load(open(ARQ, encoding="utf-8"))
    item = next((i for i in itens if i.get("id") == alvo), None)
    if not item:
        falha(f"Publicação {alvo} não existe em {ARQ}.")
    if item.get("estado") != "aprovado":
        falha(f"Publicação {alvo} está como '{item.get('estado')}'. Só itens 'aprovado' podem ser agendados.")
    if item.get("postGroupId"):
        falha(f"Publicação {alvo} já foi enviada (postGroupId {item['postGroupId']}). Nada feito.")

    quando = item.get("agendado_para")
    if not quando:
        falha("Falta 'agendado_para' (data e hora). Sem horário nada é enviado.")
    try:
        momento = dt.datetime.fromisoformat(quando)
    except ValueError:
        falha(f"'agendado_para' inválido: {quando}")
    if momento.tzinfo is None:
        falha("'agendado_para' precisa ter fuso (ex.: 2026-10-27T18:00:00-03:00).")
    agora = dt.datetime.now(dt.timezone.utc)
    if momento < agora + dt.timedelta(minutes=15):
        falha("'agendado_para' precisa estar pelo menos 15 minutos no futuro.")

    ajustes = None
    if item.get("formato") == "reel":
        fotos = [os.path.join(item.get("pasta_artes", ""), "reel.mp4")]
        if not os.path.isfile(fotos[0]):
            falha("Reel sem o arquivo reel.mp4 na pasta de artes.")
        ajustes = {"instagram": {"videoType": "REELS"}}
    else:
        fotos = sorted(glob.glob(os.path.join(item.get("pasta_artes", ""), "*.jpg")))
        if not 1 <= len(fotos) <= 10:
            falha(f"A pasta de artes tem {len(fotos)} JPEGs; o Instagram aceita de 1 a 10.")
    legenda = item.get("legenda") or ""
    if not legenda.strip() or len(legenda) > 2200:
        falha("Legenda vazia ou maior que 2.200 caracteres.")

    plataforma = json.load(open(CONEXAO, encoding="utf-8")).get("instagram_platform_id")
    if not plataforma:
        falha("Instagram não está conectado na Publora (rode o teste de conexão).")

    utc = momento.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    try:
        r = PubloraClient().publish_media_post(
            content=legenda, platforms=[plataforma], media=fotos, scheduled_time=utc, platform_settings=ajustes
        )
    except PubloraError as e:
        item.setdefault("historico", []).append({"data": agora.isoformat(), "estado": "erro", "nota": str(e)[:300]})
        item["estado"] = "erro"
        json.dump(itens, open(ARQ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        with open("registro/erros.md", "a", encoding="utf-8") as f:
            f.write(f"\n- {agora.date()}: falha ao agendar {alvo}: {str(e)[:300]}\n")
        print(f"::error::Publora recusou: {e}")
        sys.exit(2)

    item["estado"] = "agendado"
    item["postGroupId"] = r.get("postGroupId")
    item.setdefault("historico", []).append({
        "data": agora.isoformat(), "estado": "agendado",
        "nota": f"Enviado à Publora para {quando} ({len(fotos)} imagem(ns)).",
    })
    json.dump(itens, open(ARQ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Agendado: {alvo} para {quando} · postGroupId {item['postGroupId']}")


if __name__ == "__main__":
    main()
