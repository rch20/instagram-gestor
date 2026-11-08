// Reel animado (08/11/2026): grava artes/<pasta>/reel-animado.html quadro a quadro e monta reel.mp4.
// Mesma ideia do Remotion (cada quadro é calculado a partir do tempo), sem dependência nova:
// usa o Playwright e o ffmpeg que o gerar-artes.yml já instala.
// Contrato do HTML: define window.DURACAO (segundos) e window.seek(t) (desenha o quadro no instante t).
// Uso: node ferramentas/artes/reel-animado.js artes/<pasta> [--fps 30] [--quadro 2.5 (só salva um JPG desse instante)]
const fs = require('fs'); const path = require('path'); const { spawnSync } = require('child_process');
const { chromium } = require('playwright');

const pasta = process.argv[2];
const arg = (n, p) => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : p; };
const FPS = +arg('--fps', 30);
const soQuadro = arg('--quadro', null);

(async () => {
  const html = path.resolve(pasta, 'reel-animado.html');
  if (!fs.existsSync(html)) { console.error('Sem reel-animado.html em', pasta); process.exit(1); }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  const dur = await page.evaluate(() => window.DURACAO);
  if (!(dur > 0 && dur <= 90)) { console.error('window.DURACAO inválida:', dur); process.exit(1); }

  if (soQuadro !== null) {
    const ts = soQuadro.split(',').map(Number);
    for (const t of ts) {
      await page.evaluate((t) => window.seek(t), t);
      const out = path.join(pasta, `_quadro-${String(t).replace('.', '_')}.jpg`);
      await page.screenshot({ path: out, type: 'jpeg', quality: 90 });
      console.log('quadro', out);
    }
    await browser.close(); return;
  }

  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'reel-'));
  const total = Math.round(dur * FPS);
  for (let i = 0; i < total; i++) {
    await page.evaluate((t) => window.seek(t), i / FPS);
    await page.screenshot({ path: path.join(tmp, `q${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  await browser.close();
  const saida = path.join(pasta, 'reel.mp4');
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'q%05d.jpg'),
    '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
    '-vf', 'format=yuv420p', '-c:v', 'libx264', '-profile:v', 'high', '-crf', '19', '-r', String(FPS),
    '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', saida], { stdio: 'inherit' });
  fs.rmSync(tmp, { recursive: true, force: true });
  if (r.status !== 0) process.exit(r.status || 1);
  console.log(`gerado ${saida} (${total} quadros, ${dur}s)`);
})();
