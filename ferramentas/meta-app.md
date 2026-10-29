# App da Meta — publicação direta e métricas (etapa 4)

Objetivo: publicar no @diaebeleza pela API oficial do Instagram (sem o limite de 15/mês da Publora) e ler métricas reais.
Código pronto: `ferramentas/publicar_ig.py` + `.github/workflows/publicar-ig.yml` (rodar com id `testar` para conferir a chave).

## Passos (a tela da Meta muda às vezes; os nomes podem variar um pouco)

1. developers.facebook.com → entrar com a conta que administra o @diaebeleza → "Meus apps" → "Criar app".
2. Caso de uso: **Instagram** ("Gerenciar mensagens e conteúdo no Instagram"). Tipo: Empresa. Nome: "Gestor diaebeleza".
3. No app: produto **Instagram → Configuração da API com login do Instagram**.
4. "Gerar tokens de acesso" → adicionar a conta @diaebeleza (o dono faz o login do Instagram e aceita).
5. Permissões: `instagram_business_basic`, `instagram_business_content_publish`, `instagram_business_manage_insights`.
   Não pedir permissões de mensagens nem de comentários.
6. O app pode ficar em **modo de desenvolvimento** (só a nossa própria conta usa; não precisa de análise da Meta).
7. Copiar o token gerado e colar **direto** em GitHub → rch20/instagram-gestor → Settings → Secrets and variables → Actions →
   New repository secret → nome `META_IG_TOKEN`. Nunca colar no chat nem em arquivo.
8. Rodar o workflow "Publicar direto no Instagram" com id `testar`: deve aparecer "Conectado: @diaebeleza".

## Atenção

- O token dura cerca de 60 dias. Quando salvar (ou renovar), a data vai em `dados/config.json` → `meta_token.salvo_em`; a conferência (3x por dia) avisa 10 dias antes de vencer.
- Pela API não dá para: música da biblioteca do Instagram nos Reels, figurinhas de enquete/pergunta nos Stories, seguir perfis, Live.
