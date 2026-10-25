// Gera as artes de uma publicação a partir de artes/<pasta>/arte.json.
// Uso: node ferramentas/artes/render.js artes/2026-10-27_dicas-whatsapp
// Saída: lamina-01.jpg, lamina-02.jpg... na mesma pasta (JPEG, exigido pela API do Instagram).
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const pasta = process.argv[2];
if (!pasta) { console.error('Informe a pasta da arte.'); process.exit(1); }
const spec = JSON.parse(fs.readFileSync(path.join(pasta, 'arte.json'), 'utf8'));
const FORMATOS = { post: [1080, 1350], story: [1080, 1920] };
const [W, H] = FORMATOS[spec.formato || 'post'] || FORMATOS.post;

const esc = (s) => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// **trecho** vira destaque na cor da marca
const rico = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, '<em>$1</em>').replace(/\n/g, '<br>');

const css = `
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&display=block');
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:${W}px;height:${H}px}
body{font-family:'Bricolage Grotesque',sans-serif;background:#FBF6F7;color:#21161F;-webkit-font-smoothing:antialiased}
.arte{position:relative;width:${W}px;height:${H}px;padding:96px 88px;display:flex;flex-direction:column}
.marca{display:flex;align-items:center;gap:14px;font-size:30px;font-weight:600;letter-spacing:-.01em}
.marca i{width:18px;height:18px;border-radius:50%;background:#A3124A;display:inline-block}
.meio{flex:1;display:flex;flex-direction:column;justify-content:center}
.etiqueta{font-size:28px;font-weight:600;color:#A3124A;text-transform:uppercase;letter-spacing:.08em;margin-bottom:28px}
h1{font-size:96px;line-height:1.02;font-weight:800;letter-spacing:-.035em}
h2{font-size:68px;line-height:1.06;font-weight:800;letter-spacing:-.03em}
p{font-size:40px;line-height:1.38;color:#5E525A;margin-top:36px;max-width:880px}
em{font-style:normal;color:#A3124A}
.num{font-size:150px;font-weight:800;color:#F5D7E2;line-height:1;margin-bottom:8px;letter-spacing:-.04em}
.rodape{display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#5E525A;border-top:2px solid #EADDE3;padding-top:28px}
.cta{background:#A3124A;color:#fff}
.cta .marca i{background:#F5D7E2}
.cta p,.cta .rodape{color:#F5D7E2}
.cta em{color:#fff;text-decoration:underline;text-decoration-thickness:4px;text-underline-offset:10px}
.cta .rodape{border-top-color:rgba(255,255,255,.25)}
.botao{display:inline-block;margin-top:56px;background:#fff;color:#A3124A;font-size:38px;font-weight:700;padding:26px 44px;border-radius:999px}
`;

const lamina = (l, i, total) => {
  const tipo = l.tipo || (i === 0 ? 'capa' : 'texto');
  const conteudo = tipo === 'capa'
    ? `${l.etiqueta ? `<div class="etiqueta">${esc(l.etiqueta)}</div>` : ''}<h1>${rico(l.titulo)}</h1>${l.texto ? `<p>${rico(l.texto)}</p>` : ''}`
    : tipo === 'cta'
      ? `<h2>${rico(l.titulo)}</h2>${l.texto ? `<p>${rico(l.texto)}</p>` : ''}${l.botao ? `<div><span class="botao">${esc(l.botao)}</span></div>` : ''}`
      : `${l.numero ? `<div class="num">${esc(l.numero)}</div>` : ''}<h2>${rico(l.titulo)}</h2>${l.texto ? `<p>${rico(l.texto)}</p>` : ''}`;
  const pag = total > 1 ? `${i + 1}/${total}` : '';
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>
<div class="arte ${tipo === 'cta' ? 'cta' : ''}">
  <div class="marca"><i></i>Dia e Beleza</div>
  <div class="meio">${conteudo}</div>
  <div class="rodape"><span>diaebeleza.com.br</span><span>${pag}${total > 1 && i < total - 1 ? ' →' : ''}</span></div>
</div></body></html>`;
};

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const total = spec.laminas.length;
  for (let i = 0; i < total; i++) {
    await page.setContent(lamina(spec.laminas[i], i, total), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const ok = await page.evaluate(() => document.fonts.check('800 40px "Bricolage Grotesque"'));
    if (!ok) { console.error('Fonte da marca não carregou; arte não gerada.'); process.exit(2); }
    // Texto não pode vazar da arte
    const vaza = await page.evaluate(() => {
      const m = document.querySelector('.meio');
      return m.scrollHeight > m.clientHeight + 2;
    });
    if (vaza) { console.error(`Lâmina ${i + 1}: texto grande demais para a arte.`); process.exit(3); }
    const nome = path.join(pasta, `lamina-${String(i + 1).padStart(2, '0')}.jpg`);
    await page.screenshot({ path: nome, type: 'jpeg', quality: 92 });
    console.log('gerada', nome);
  }
  await browser.close();
})();
