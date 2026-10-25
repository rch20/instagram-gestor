// Renderiza cada .html de uma pasta em .jpg do mesmo nome.
// Tamanho em <meta name="tamanho" content="1080x1080"> (padrão 1080x1080).
const fs = require('fs'); const path = require('path'); const { chromium } = require('playwright');
const pasta = process.argv[2];
(async () => {
  const browser = await chromium.launch();
  for (const f of fs.readdirSync(pasta).filter((x) => x.endsWith('.html'))) {
    const html = fs.readFileSync(path.join(pasta, f), 'utf8');
    const m = html.match(/name="tamanho" content="(\d+)x(\d+)"/);
    const [W, H] = m ? [+m[1], +m[2]] : [1080, 1080];
    const page = await browser.newPage({ viewport: { width: W, height: H } });
    await page.setContent(html, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(pasta, f.replace(/\.html$/, '.jpg'));
    await page.screenshot({ path: out, type: 'jpeg', quality: 95 });
    console.log('gerada', out); await page.close();
  }
  await browser.close();
})();
