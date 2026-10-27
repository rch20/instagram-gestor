"""Cancela na Publora UMA publicação ainda agendada (nunca uma já publicada).

Uso (no GitHub Actions): python ferramentas/cancelar.py <id> "<motivo>"
O item volta para "aprovado" (sem postGroupId), com o motivo no histórico.
"""
import datetime as dt
import json
import os
import sys

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "instagram-skills"))
from lib.publora_client import PubloraClient  # noqa: E402

ARQ = "dados/publicacoes.json"


def main():
    alvo, motivo = sys.argv[1].strip(), (sys.argv[2] if len(sys.argv) > 2 else "").strip()
    itens = json.load(open(ARQ, encoding="utf-8"))
    item = next((i for i in itens if i.get("id") == alvo), None)
    if not item or item.get("estado") != "agendado" or not item.get("postGroupId"):
        print(f"::error::{alvo} não está agendado na Publora; nada feito.")
        sys.exit(1)
    r = requests.get(f"https://api.publora.com/api/v1/get-post/{item['postGroupId']}",
                     headers={"x-publora-key": os.environ["PUBLORA_API_KEY"]}, timeout=30)
    dados = r.json() if r.status_code == 200 else {}
    posts = dados.get("posts") or (dados.get("postGroup") or {}).get("posts") or []
    if any(p.get("status") == "published" for p in posts) or str(dados.get("status", "")).lower() == "published":
        print("::error::Já foi publicado; não cancelo.")
        sys.exit(1)
    cli = PubloraClient()
    cli.delete_post(item["postGroupId"])
    agora = dt.datetime.now(dt.timezone.utc).isoformat()
    item.setdefault("historico", []).append({"data": agora, "estado": "aprovado",
                                             "nota": f"Agendamento cancelado na Publora ({item['postGroupId']}). {motivo}"})
    item["estado"] = "aprovado"
    item.pop("postGroupId", None)
    json.dump(itens, open(ARQ, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Cancelado: {alvo}")


if __name__ == "__main__":
    main()
