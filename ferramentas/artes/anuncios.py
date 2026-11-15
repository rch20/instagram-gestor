"""Gera as artes dos anúncios (clique para o WhatsApp), 15/11/2026: 4 públicos x 2 formatos (feed 4:5 e story 9:16).
Saída: artes/anuncios_2026-11/<publico>-<formato>.html (depois render-html.js gera os .jpg)."""
import base64, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, '..', '..', 'artes', 'anuncios_2026-11')
F = {p: base64.b64encode(open(os.path.join(AQUI, 'fontes', f'bricolage-{p}.ttf'), 'rb').read()).decode() for p in (400, 700)}

CSS = """
@font-face{font-family:B;font-weight:400;src:url(data:font/ttf;base64,%(f400)s)}
@font-face{font-family:B;font-weight:700;src:url(data:font/ttf;base64,%(f700)s)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%(w)dpx;height:%(h)dpx}
body{font-family:B,sans-serif;-webkit-font-smoothing:antialiased;background:#FBF6F7;color:#21161F;
 padding:%(topo)dpx 88px %(base)dpx;display:flex;flex-direction:column}
.marca{display:flex;align-items:center;gap:16px;font-weight:700;font-size:32px;letter-spacing:-.01em}
.marca i{width:20px;height:20px;border-radius:50%%;background:#A3124A}
.tag{margin-top:%(gap1)dpx;color:#A3124A;font-weight:700;font-size:28px;letter-spacing:.14em}
h1{margin-top:22px;font-weight:700;font-size:%(h1)dpx;line-height:.98;letter-spacing:-.045em}
h1 em{font-style:normal;color:#A3124A;display:block}
.sub{margin-top:26px;font-size:%(sub)dpx;line-height:1.32;color:#5E525A;max-width:860px}
.palco{zoom:%(zoom)s;flex:1;display:flex;flex-direction:column;justify-content:center;gap:22px;padding:%(gap2)dpx 0}
.cartao{background:#fff;border:2px solid #EADDE3;border-radius:30px;padding:34px 38px;box-shadow:0 18px 40px -24px rgba(33,22,31,.28)}
.rot{font-size:24px;font-weight:700;letter-spacing:.1em;color:#5E525A}
.linha{display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding:18px 0;border-bottom:2px solid #F3E9ED;font-size:34px}
.linha:last-child{border-bottom:0;padding-bottom:4px}
.linha b{font-weight:700}
.linha span{color:#5E525A;white-space:nowrap}
.selo{display:inline-block;background:#F5D7E2;color:#7E0D38;font-weight:700;font-size:26px;padding:10px 20px;border-radius:999px}
.balao{align-self:flex-start;background:#fff;border:2px solid #EADDE3;border-radius:30px 30px 30px 8px;padding:24px 30px;font-size:34px;max-width:760px}
.balao small{display:block;margin-top:8px;font-size:24px;color:#8A7D85;text-align:right}
.nota{font-size:26px;color:#5E525A}
.rodape{border-top:2px solid #EADDE3;padding-top:30px;display:flex;justify-content:space-between;align-items:flex-end;gap:24px}
.rodape p{font-size:30px;line-height:1.25;color:#5E525A;max-width:640px}
.rodape strong{font-weight:700;font-size:34px;color:#A3124A;text-align:right;line-height:1.15}
.grade{display:grid;grid-template-columns:110px repeat(3,1fr);gap:10px;font-size:27px}
.grade .h{font-weight:700;padding-bottom:6px}
.grade .t{color:#8A7D85;padding-top:16px}
.grade .c{border-radius:16px;padding:14px 16px;font-weight:700;background:#F5D7E2;color:#7E0D38;min-height:66px}
.grade .c.l{background:#fff;border:2px dashed #EADDE3;color:#8A7D85;font-weight:400}
.grade .c.e{background:#21161F;color:#fff}
.campo{display:flex;justify-content:space-between;padding:14px 0;border-bottom:2px solid #F3E9ED;font-size:31px}
.campo span{color:#5E525A}
.ass{margin-top:18px;display:flex;align-items:flex-end;justify-content:space-between;gap:20px}
.ass svg{width:300px;height:90px}
"""

PUBLICOS = {
    'manicure': {
        'tag': 'MANICURE E NAIL DESIGNER',
        'h1': ('Cliente pedindo horário', 'às 23h?'),
        'sub': 'Com a sua página de agendamento, ela mesma escolhe o horário e já paga o sinal.',
        'palco': '''<div class="balao">Oi! Tem horário amanhã pra alongamento?<small>23:12</small></div>
<div class="cartao"><div class="rot">NOVO AGENDAMENTO</div>
<div class="linha"><b>Alongamento em gel</b><span>2h</span></div>
<div class="linha"><b>Quinta, 14:00</b><span class="selo">Sinal pago no Pix</span></div></div>
<p class="nota">Marcado pela cliente. Você não precisou responder.</p>''',
    },
    'salao': {
        'tag': 'SALÃO E CABELEIREIRA',
        'h1': ('A equipe toda', 'numa agenda só.'),
        'sub': 'Cada profissional com os seus horários. A cliente escolhe com quem quer e marca sozinha.',
        'palco': '''<div class="cartao"><div class="grade">
<div></div><div class="h">Bia</div><div class="h">Carla</div><div class="h">Duda</div>
<div class="t">09:00</div><div class="c">Escova</div><div class="c l">livre</div><div class="c e">Coloração</div>
<div class="t">10:00</div><div class="c l">livre</div><div class="c">Corte</div><div class="c e">Coloração</div>
<div class="t">11:00</div><div class="c">Hidratação</div><div class="c">Escova</div><div class="c l">livre</div>
</div></div>
<p class="nota">Os horários livres aparecem na página do salão para a cliente marcar.</p>''',
    },
    'estetica': {
        'tag': 'CLÍNICA DE ESTÉTICA',
        'h1': ('Anamnese assinada', 'antes de ela chegar.'),
        'sub': 'A cliente marca pelo link, preenche a ficha e assina no celular. Você imprime ou salva em PDF.',
        'palco': '''<div class="cartao"><div class="rot">FICHA DE ANAMNESE · LIMPEZA DE PELE</div>
<div class="campo"><span>Alergias</span><b>Não</b></div>
<div class="campo"><span>Usa ácidos na pele</span><b>Sim, retinol</b></div>
<div class="campo"><span>Gestante</span><b>Não</b></div>
<div class="ass"><svg viewBox="0 0 300 90" fill="none" stroke="#21161F" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M8 62c18-30 30-46 38-40 9 7-14 44-4 46 12 2 24-42 36-40 10 2-6 34 4 36 9 2 18-22 28-22 8 0 4 18 12 18 10 0 16-14 26-14 9 0 6 12 14 12 12 0 28-10 46-12 18-2 34 2 46 0"/></svg>
<span class="selo">Assinada pelo link</span></div></div>''',
    },
    'sobrancelha': {
        'tag': 'SOBRANCELHA E CÍLIOS',
        'h1': ('Manutenção marcada', 'sem você no celular.'),
        'sub': 'A cliente vê os horários livres e marca a manutenção sozinha. O lembrete chega por e&#8209;mail antes do horário.',
        'palco': '''<div class="cartao"><div class="rot">SÁBADO</div>
<div class="linha"><b>Manutenção de cílios</b><span>10:30</span></div>
<div class="linha"><b>Design com henna</b><span>11:30</span></div>
<div class="linha"><b>Lash lifting</b><span>13:00</span></div></div>
<p class="nota">Todos marcados pelas próprias clientes.</p>''',
    },
}

FORMATOS = {'feed': (1080, 1350, 80, 72, 34, 18, 96, 34, '1'), 'story': (1080, 1920, 250, 330, 56, 30, 112, 38, '1.1')}

for nome, p in PUBLICOS.items():
    for fmt, (w, h, topo, base, gap1, gap2, h1, sub, zoom) in FORMATOS.items():
        css = CSS % {'f400': F[400], 'f700': F[700], 'w': w, 'h': h, 'topo': topo, 'base': base, 'gap1': gap1, 'gap2': gap2, 'h1': h1, 'sub': sub, 'zoom': zoom}
        html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="tamanho" content="{w}x{h}"><style>{css}</style></head><body>
<div class="marca"><i></i>Dia e Beleza</div>
<div class="tag">{p['tag']}</div>
<h1>{p['h1'][0]}<em>{p['h1'][1]}</em></h1>
<p class="sub">{p['sub']}</p>
<div class="palco">{p['palco']}</div>
<div class="rodape"><p>Agenda online completa em poucos minutos.</p><strong>14 dias grátis,<br>sem cartão</strong></div>
</body></html>'''
        open(os.path.join(SAIDA, f'{nome}-{fmt}.html'), 'w').write(html)
print('ok')
