# Rotina automática — @diaebeleza

Executada por uma tarefa agendada 3 vezes ao dia (horário de São Paulo). Cada execução começa do zero:
ler `CLAUDE.md`, `dados/config.json`, `marca/identidade.md`, `editorial/estrategia.md`, `dados/publicacoes.json`
e `registro/pendencias.md` antes de agir.

## Travas (valem para toda execução)

1. Se `dados/config.json` tiver `"pausado": true`, **não criar nem agendar nada**: só conferir publicações e registrar.
2. Enquanto nenhuma publicação estiver com estado `publicado`, não aprovar conteúdo criado pela automação
   (o modo automático só liga depois da primeira publicação confirmada).
3. Limites: no máximo 3 posts de feed por semana (segunda a domingo).
4. Nunca agendar o mesmo `id` duas vezes (o `ferramentas/agendar.py` já recusa).
5. Não responder comentários nem mensagens, não excluir posts, não mudar o perfil, não gastar dinheiro.
6. Nunca inventar número, resultado, depoimento ou recurso. Só afirmar o que está em `marca/identidade.md`.
7. Sem fotos de pessoas. Telas do sistema só reais e sem dados pessoais.
8. Se a mesma etapa falhar 2 vezes seguidas, parar a parte automática, registrar em `registro/erros.md` e avisar o dono.
9. **Canal (desde 29/10/2026): publicação direta pela API** — todo item novo nasce com `"canal": "api"` e
   `agendado_para` com fuso. O `publicar-ig.yml` roda sozinho a cada 15 min e publica na hora; não usar `agendar.yml`
   (a Publora fica desligada; ela recusa itens "api"). Item com mais de 3 h de atraso não sai: dar nova data.
10. Itens com `"canal": "collab_manual"` ou `"canal": "manual"` nunca vão para a Publora nem são aprovados pela automação (são publicados pelo dono no app).

## Formato (desde 27/10/2026 — alcance)

- Perfil novo cresce por Reels: **pelo menos 1 de cada 2 posts novos deve ser Reel** (`"formato": "reel"`,
  lâminas verticais montadas em vídeo por `gerar-artes.yml`). Carrossel fica para conteúdo de salvar.
- Medir toda segunda (`coletar-perfis.yml`) e anotar em `dados/metricas/`.

## Manhã (~7h30)

1. Conferir em `dados/publicacoes.json` o que saiu (estado `publicado` com link) e o que deu `erro`.
2. Item `aprovado` com aviso de atraso: dar nova data numa vaga livre e registrar.
3. Registrar no `registro/diario.md`: o que saiu, o que está na fila, erros.

## Tarde (~13h30)

1. Garantir conteúdo pronto para os próximos 10 dias, respeitando os limites e os `horarios_padrao`.
2. Para cada vaga: escolher tema pelos pilares de `editorial/estrategia.md`, sem repetir assunto das últimas 4 semanas,
   ler a skill adequada em `ferramentas/instagram-skills/skills/`, escrever arte (`arte.json`) e legenda.
3. Checklist antes de aprovar (todos obrigatórios; registrar no histórico do item):
   - gancho nos primeiros 125 caracteres; um único chamado para ação; 3 a 5 hashtags; 0 a 3 emojis;
   - nada de vocabulário de IA (ver `CLAUDE.md`), nenhum número ou promessa sem fonte;
   - artes geradas por `gerar-artes.yml` e conferidas visualmente (texto legível, nada cortado).
4. Com o checklist completo: marcar `"estado": "aprovado"`, `"aprovado_por": "automacao"`, com data.
5. Conferir que tem `"canal": "api"` e `agendado_para` (a publicação sai sozinha).

## Noite (~21h30)

1. Conferir os estados (como na manhã).
2. Toda segunda-feira: `coletar-perfis.yml` com `diaebeleza` e os concorrentes de `dados/concorrentes.md`; registrar números com data e fonte.
3. Toda segunda-feira: conferir se https://github.com/sergebulaev/instagram-skills tem versão nova; se tiver, só registrar em pendências (não atualizar sem o dono).
4. Escrever o resumo do dia em `registro/diario.md` e avisar o dono só se algo foi publicado, agendado, falhou ou precisa dele.
