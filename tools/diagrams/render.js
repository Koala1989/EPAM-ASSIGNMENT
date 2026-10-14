// Renders every agents/diagrams/*.svg to a 2x PNG and fails if any text runs past the edge of its box.
// Usage (from the repo root): node tools/diagrams/render.js
const fs = require('fs');
const path = require('path');
const { chromium } = require(path.resolve(__dirname, '../../automation/node_modules/playwright'));

const dir = path.resolve(__dirname, '../../agents/diagrams');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  let problems = 0;
  for (const file of fs.readdirSync(dir).filter((f) => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, file), 'utf8');
    await page.setContent(`<!doctype html><html><body style="margin:0">${svg}</body></html>`);
    const overflow = await page.evaluate(() =>
      [...document.querySelectorAll('rect[data-box]')].flatMap((rect) => {
        const r = rect.getBBox();
        return [...document.querySelectorAll(`text[data-in="${rect.dataset.box}"]`)]
          .filter((t) => { const b = t.getBBox(); return b.x + b.width > r.x + r.width - 8 || b.y + b.height > r.y + r.height - 4; })
          .map((t) => t.textContent);
      }),
    );
    for (const text of overflow) console.log(`${file}: text does not fit its box: "${text}"`);
    problems += overflow.length;
    await page.locator('svg').screenshot({ path: path.join(dir, file.replace(/\.svg$/, '.png')) });
    console.log('rendered', file);
  }
  await browser.close();
  process.exitCode = problems ? 1 : 0;
})();
