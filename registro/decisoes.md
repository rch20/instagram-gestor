# Decisões

- 2026-10-25: Instagram gerido é o @diaebeleza (conta profissional).
- 2026-10-25: Publicação pela Publora via API (chamada pelo GitHub Actions); métricas pela API oficial da Meta; concorrentes pela Apify. Motivo: este ambiente não acessa essas APIs diretamente e as chaves ficam só nos Secrets do GitHub.
- 2026-10-25: Artes geradas por modelos próprios (HTML → JPEG no GitHub Actions) com as cores e a fonte da marca, sem serviço pago de imagem.
- 2026-10-25: Plano Starter da Publora (grátis): 15 posts/mês e 3 canais. Frequência inicial de 3 posts por semana.
- 2026-10-25: Agendamento só por `ferramentas/agendar.py`: recusa item não aprovado, já enviado, sem data ou com data a menos de 15 min. Trava testada com o post de teste em revisão (recusado, nada enviado).
- 2026-10-25: Concorrentes acompanhados: @trinksoficial, @booksybrasil, @appbarber, @simplesagenda (aprovado pelo dono).
- 2026-10-25: Proposta de perfil (nome, bio, link /criar-salao, categoria Software) aprovada pelo dono.
- 2026-10-25: Plano Starter da Publora permite no máximo **3 posts agendados ao mesmo tempo** (erro SCHEDULED_POST_LIMIT_REACHED). Regra: manter a fila com até 3 e agendar o próximo aprovado assim que um for publicado.
- 2026-10-25: Nova foto de perfil (avatar 'Dia e / Beleza' em #A3124A com Bricolage Grotesque), autorizada pelo dono ("total liberdade, inclusive para criar um logo novo"). Fonte em artes/marca_avatar/avatar-a.html.
- 2026-10-25: Dono pediu para excluir os 2 posts antigos (arte roxa e logo antigo). Excluídos pelo Chrome; perfil ficou com 0 posts até o carrossel das 18h.
- 2026-10-25: Dono autorizou o modo automático ("poste sem minha autorização"). Implementado com travas: liga só após a 1ª publicação confirmada, limites de 3/semana e 15/mês, fila ≤ 3, checklist obrigatório, pausa em `dados/config.json`.
- 2026-10-25: Fluxo completo validado: carrossel de teste publicado às 18h pela Publora (postedId 17914479012283634). Modo automático liberado pela trava da primeira publicação.

- 2026-10-25: Dono aprovou turbinar posts (teste R$ 100, 7 dias, Brasil todo, objetivo visitas a /criar-salao, início previsto 28/10). Criada a Página do Facebook "Dia e Beleza" (site, WhatsApp de suporte autorizado, logo). Dono conectou o Instagram; a Meta criou o portfólio "@dia&beleza". Conta de anúncios e cartão: o dono cria/cadastra (ação de conta e pagamento fica com ele).
- 2026-10-25: Conta de anúncios "Dia e Beleza - Anúncios" (id 1780141879958687) criada pelo dono no portfólio @dia&beleza, em BRL, com saldo pré-pago por Pix (R$ 115 depositados). Campanha de teste será montada em 28/10 e só ativada após aprovação do dono.

- 2026-10-27: Dono autorizou usar o Instagram para seguir perfis ("pode usar o instagram e começa a seguir"). Diagnóstico com dado real: 0 seguidores e post de hoje com 0 visualizações após 2h. Plano: seguir 20–30 perfis/dia do público-alvo (donas de salão, nail designers, lash, sobrancelha, estética), começando pelos salões clientes; mais Reels; post em parceria (Collab) com a Unhas Capão; destaques e post fixado; anúncio de 28/10. Não fazer: comentários automáticos, DM em massa, compra de seguidores.
- 2026-10-27: Seguidos 25 perfis (5 salões clientes + 20 profissionais de beleza tirados de quem a @ollgaoliveiranails segue), com intervalo de 7–13 s entre cada um. Lista em dados/seguidos.md.
- 2026-10-28: Campanha de teste publicada com aprovação do dono ("faça conforme você vê que vai ser melhor"). Conta 1780141879958687. Campanha "Teste 1 - Tráfego criar-salao - out/2026" (id 120251842130510425): Tráfego → site, otimiza visualizações da página; orçamento total R$ 100 (sem compartilhamento), 28/10 a 04/11; Brasil, 20+; interesses Salões de beleza, Manicure, Cabeleireiro Profissional, Esteticista (sobrancelha e empreendedorismo ficaram de fora: o primeiro só existe como "parte do corpo", o segundo dispersa o público); anúncio = post Instagram Unhas Capão, botão "Cadastre-se". Destino trocado de /criar-salao para https://diaebeleza.com.br/experimentar?utm_source=meta&utm_medium=pago&utm_campaign=teste1 (simulação publicada hoje; público frio). Métricas orgânicas em dados/metricas/2026-10-28.md.
- 2026-10-29: Novo canal "manual" em publicacoes.json para posts que o dono publica pelo app sem ser Collab; a automação não aprova nem agenda esses itens (rotina.md, regra 10). Motivo: evitar publicação em dobro.

- 2026-10-29: Dono quer postar com mais frequência (roteiro de dicas e entretenimento). Caminho escolhido: publicação direta pela API oficial do Instagram (app da Meta), sem o limite de 15/mês da Publora. Código preparado (`ferramentas/publicar_ig.py`, `publicar-ig.yml`); a regra de 3 posts/semana só muda quando a chave estiver funcionando e o dono confirmar a frequência.
