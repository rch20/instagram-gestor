# Erros de execução

(nenhum até agora)

- 2026-10-25: falha ao agendar 2026-10-31_caso-real-estudio-de-unhas: HTTP 403: {'error': 'Scheduled post limit reached', 'code': 'SCHEDULED_POST_LIMIT_REACHED', 'metric': 'posts.scheduled_active', 'message': 'Your Starter plan allows up to 3 active scheduled posts across the workspace.', 'limit': 3, 'used': 3, 'requested': 1, 'remaining': 0, 'periodStart': None, 'per
  - Tratado: item voltou para 'aprovado'; será agendado depois que o post de 25/10 18h sair.

- 2026-10-27: falha ao agendar 2026-11-05_mitos-do-sinal: HTTP 403: {'error': 'Schedule horizon reached', 'code': 'SCHEDULE_HORIZON_REACHED', 'metric': 'posts.schedule_horizon_days', 'message': 'Your Starter plan allows scheduling up to 7 days ahead.', 'limit': 7, 'used': None, 'requested': None, 'remaining': None, 'periodStart': None, 'periodEnd': None, '
  - Tratado: limite do plano Starter (agendar no máximo 7 dias à frente). Item voltou para 'aprovado'; regra adicionada em editorial/rotina.md.

- 2026-10-29: publicação 2026-10-29_como-a-cliente-marca falhou na Publora: PLATFORM_AUTH_EXPIRED Error validating access token: The session has been invalidated because the user changed their password or Facebook has changed the session for security reasons.
