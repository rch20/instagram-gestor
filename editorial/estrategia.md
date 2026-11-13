# Estratégia — @diaebeleza

> Estado: versão 2, de 31/10/2026. O dono definiu o público (beleza e clínicas) e deixou a operação com Claude
> ("estou deixando em tuas mãos e confio"). Base: métricas reais da API em `dados/metricas/2026-10-31-api.md`.
> Rever toda segunda com `metricas.yml` (roda sozinho todo dia às 8h).

## Diagnóstico com dado real (31/10/2026)

- 15 seguidores, 4 posts no feed, nenhum Reel publicado ainda (o primeiro sai em 03/11).
- Alcance orgânico por post: 4 a 7 contas nos posts próprios; **36 no post em parceria (Collab) com a Unhas Capão**,
  que também trouxe as únicas visitas ao perfil vindas de post (4) e o único seguidor vindo de post (1).
- Conta em 7 dias: 6.206 contas alcançadas, 22 visitas ao perfil, 2 cliques no link da bio, 0 salvamentos.
  Estimativa (não confirmada pela API): quase todo esse alcance é do anúncio de teste (28/10 a 04/11), porque os
  posts somam menos de 60 contas.
- Conclusões: (1) post próprio em formato de foto/carrossel quase não é entregue a quem não segue; (2) caso real com
  parceria rende 5 vezes mais; (3) quem chega ao perfil não clica no link: o perfil ainda não convence.

## Público (definido pelo dono em 31/10/2026)

| Segmento | Quem | O que dói | O que o sistema resolve de verdade |
|---|---|---|---|
| Beleza | salões, nail designers, cílios e sobrancelha, cabeleireiras, barbearias | WhatsApp o dia todo, faltas, cobrar sinal | página de agendamento, sinal por Pix, lembretes, agenda por profissional |
| Clínicas de estética | estética facial e corporal, depilação, micropigmentação, massoterapia | faltas em procedimento longo, anamnese no papel, sinal | sinal por Pix, **ficha de atendimento digital com assinatura da cliente e impressão**, pacotes de sessões |
| Consultórios (secundário) | psicologia, fisioterapia, nutrição, terapias | agenda e confirmação | página de agendamento, lembretes, sinal. **Não** falar em ficha: os modelos de ficha são de beleza e estética |

Quem paga é o dono ou a dona do negócio. Toda peça fala com quem decide, não com a cliente final.

### Ampliação (dono, 31/10/2026: "abranger o máximo possível")

O sistema serve para qualquer negócio que atende com hora marcada (no cadastro, o tipo "Outros" monta a página
sem serviços prontos). Para crescer sem perder a cara do perfil, o conteúdo segue em camadas:

| Camada | Quem | Peso no feed | Como entra |
|---|---|---|---|
| Núcleo | beleza e clínica de estética | ~70% | todos os pilares |
| Bem-estar e saúde com hora marcada | massoterapia, podologia, terapias, pilates, psicologia, nutrição, fisioterapia | ~20% | dica de agenda, faltas e sinal; série "Também serve para você?" |
| Outros serviços com hora marcada | tatuagem, maquiagem, banho e tosa, personal, aulas | ~10% | série "Também serve para você?" e anúncios com vários interesses |

- Anúncio (só com autorização do dono): um conjunto com vários interesses somados (beleza, estética, manicure,
  cabeleireiro, barbearia, massagem, podologia, tatuagem, pilates, psicologia, nutrição, fisioterapia), e a Meta
  mostra os resultados por interesse; os que trouxerem cadastro ficam.
- Ponto de atenção: o site e o cadastro falam "salão" em quase toda tela. Para quem não é de beleza isso pode afastar;
  medir pelo Funil do site e, se cair muito nesses públicos, propor ao dono textos neutros ("seu espaço").

## Funil (do Instagram até a assinatura)

1. **Descoberta:** Reels curtos (até 30 s) com situação reconhecível nos primeiros 2 segundos + posts em parceria (Collab).
2. **Perfil que convence:** fixados (1 caso real, 1 demonstração do produto, 1 dica forte); destaques quando houver Stories.
3. **Teste sem atrito:** link da bio em /experimentar (simulação sem cadastro) → salão de demonstração → criar conta.
4. **Conversa:** quem pede contato pelo site entra na Prospecção do Super Admin (origem "Site"); quem chama no direct
   o dono cadastra com origem "Instagram". A automação não responde direct nem comentário.
5. **Assinatura:** acontece no sistema (14 dias grátis). O Instagram é medido por cadastros, não por curtidas.

## Frequência e formato

- **3 por semana** (terça 12h, quinta 12h, sábado 10h), **2 Reels e 1 carrossel**. Subir para 4 só se 4 semanas
  mostrarem alcance subindo sem cair salvamentos.
- Rodízio de segmento: a cada 3 posts, 2 de beleza e 1 de clínica de estética; consultórios 1 vez por mês.
- Reel: gancho escrito na tela no primeiro segundo, uma ideia por vídeo, legenda com o mesmo gancho.
- Carrossel: conteúdo de salvar (passo a passo, checklist), 6 a 8 lâminas.

## Pilares

| Pilar | Objetivo | Formato | Frequência |
|---|---|---|---|
| Rotina do negócio (humor e identificação) | alcance e seguidores | Reel | 1 por semana |
| Dica prática de gestão (faltas, sinal, preço, agenda) | salvamentos e compartilhamentos | Carrossel ou Reel | 1 por semana |
| Produto funcionando (tela real, dados fictícios) | visitas ao perfil e cliques no link | Reel | 1 a cada 2 semanas |
| Caso real em parceria (Collab) | confiança e alcance fora da bolha | Post ou Reel em Collab | 1 a cada 2 semanas, quando houver cliente autorizando |

## Programa de parceria (a alavanca mais forte hoje)

Só vale caso de quem usa de verdade. Em 01/11/2026 o dono informou que só a **Day (Dayane Xavier)** e a
**Unhas Capão** usam ativamente. Unhas Capão já foi (27/10); a próxima é a Day. Os outros clientes só entram quando
estiverem usando (post de caso real com agenda parada passa a imagem errada). A automação prepara a arte e a legenda; **o dono pede a
autorização do cliente, publica pelo app e convida o perfil do cliente como colaborador** (canal `collab_manual`).
Nunca citar nome de pessoa ou endereço sem autorização.

## Metas de 4 semanas (até 28/11/2026), medidas pela API

| Indicador | 31/10 | Meta | Onde ver |
|---|---|---|---|
| Alcance médio por post (sem anúncio) | ~14 | 150 | `dados/metricas/*-api.md` |
| Seguidores | 15 | 100 | idem |
| Visitas ao perfil (7 dias) | 22 | 60 sem anúncio | idem |
| Cliques no link da bio (7 dias) | 2 | 15 | idem |
| Salvamentos por carrossel | 0 | 5 | idem |
| Cadastros de salão no período | — | acompanhar | Super Admin → Comercial (Indicadores e Funil do site) |

As metas são objetivos de trabalho, não promessa. Se em 2 semanas o alcance médio não passar de 50, trocar o formato
dos Reels (gancho e duração) antes de aumentar a frequência.

## Calendário das próximas 3 semanas (temas; a rotina da tarde cria e aprova)

Já na fila (aprovados, canal api): 03/11 Reel (horário amanhã), 05/11 carrossel (mitos do sinal),
07/11 carrossel em parceria com a Day, 10/11 Reel (bloqueie antes), 14/11 post (cliente que não aparece: pergunta).

| Data | Segmento | Formato | Tema |
|---|---|---|---|
| 12/11 qui | Clínica de estética | Reel | "Anamnese no papel?" Ficha digital assinada pela cliente pelo link, pronta para imprimir (tela real) |
| 17/11 ter | Bem-estar e saúde | Reel | Série "Também serve para você?": massoterapia, podologia, psicologia (agenda por profissional, lembrete) |
| 19/11 qui | Beleza e estética | Reel | Novidade real (no ar desde 01/11): a cliente recebe o lembrete na véspera e toca em "Vou comparecer"; a dona vê quem confirmou na agenda. Responde à pergunta do post de 14/11 (tela real) |
| 21/11 sáb | Todos | Reel | Bela, a assistente virtual da página de agendamento (pedido do dono em 11/11; o pacote de sessões foi para a reserva) |
| 24/11 ter | Todos | Reel | **Campanha Black Friday (27/11)**: a página de agendamento com a decoração da data. A dona liga no painel, em Aparência: faixa com a mensagem dela (até 80 caracteres), desconto opcional de 5 a 30% em todos os serviços ou só nos escolhidos (preço de/por na página), ela escolhe os dias (entre 01/11 e 07/12) e a faixa some sozinha no fim. Liberado em todos os planos. Tela real só do salão de demonstração (prévia da decoração); sem tela real, Reel só de texto, nunca tela inventada |
| 26/11 qui | Beleza | Reel | Produto: do link na bio ao horário confirmado em 20 segundos (tela real) |
| 28/11 sáb | Beleza | Carrossel | Quanto custa um horário vazio: conta simples de quanto a falta tira do mês (valores fictícios, avisando que são exemplo) |

| 01/12 ter | Todos | Reel | **Campanha Fim de ano**: decoração de Natal/Fim de ano na página (a dona escolhe os dias entre 15/11 e 31/12; mensagem padrão "Boas festas! Garanta seu horário para as festas de fim de ano"), mesmo desconto opcional. Mesma regra de tela real |

Reserva (se faltar tema ou um item cair): Reel de humor "a cliente que pede encaixe sábado às 18h"; Reel "Também serve para você?": tatuagem, maquiagem, banho e tosa (saiu de 24/11 para a Black Friday); carrossel pacote de sessões (clínica de estética).
O carrossel de 29/10 (como a cliente marca, em erro desde a queda da Publora) não volta: o tema está coberto pelo Reel de 26/11.

## Regras

- Um chamado para ação por post, coerente com o objetivo.
- Gancho nos primeiros 125 caracteres da legenda.
- 3 a 5 hashtags do nicho, no fim da legenda (beleza ou estética, conforme o segmento do post).
- Telas do produto: só capturas reais do sistema, com dados fictícios ou autorizados.
- Link em post de feed **não é clicável** (nem na arte, nem na legenda). Nunca desenhar algo que pareça botão
  ("Teste agora →"); escrever "link na bio". Link clicável só na bio, na figurinha de link do Story (o dono põe pelo app)
  ou em anúncio pago (só com autorização do dono).
- Nada de promessa sem número medido ("acabe com as faltas", "dobre a agenda").
- Não publicar só para cumprir número: se não houver bom conteúdo, pular o dia e registrar o motivo.
- Anúncio: nenhum gasto novo sem autorização do dono. Próximo teste só depois de o perfil ter 2 Reels com alcance acima
  da média e os fixados prontos (hoje o anúncio leva gente a um perfil que ainda não converte).
