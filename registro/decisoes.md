# Decisões

- 2026-10-25: Instagram gerido é o @diaebeleza (conta profissional).
- 2026-10-25: Publicação pela Publora via API (chamada pelo GitHub Actions); métricas pela API oficial da Meta; concorrentes pela Apify. Motivo: este ambiente não acessa essas APIs diretamente e as chaves ficam só nos Secrets do GitHub.
- 2026-10-25: Artes geradas por modelos próprios (HTML → JPEG no GitHub Actions) com as cores e a fonte da marca, sem serviço pago de imagem.
- 2026-10-25: Plano Starter da Publora (grátis): 15 posts/mês e 3 canais. Frequência inicial de 3 posts por semana.
- 2026-10-25: Agendamento só por `ferramentas/agendar.py`: recusa item não aprovado, já enviado, sem data ou com data a menos de 15 min. Trava testada com o post de teste em revisão (recusado, nada enviado).
