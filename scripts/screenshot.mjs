// Screenshot the garage in headless Chromium and print window.__garage as JSON.
//
//   npm run shot -- [url] [out.png] [WIDTHxHEIGHT]
//   npm run shot -- "http://localhost:3000/?model=placeholder&hinges=open" open.png
//
// SHOT_SETTLE_MS (default 2500) is the wait after the model reports loaded.
// CHROME_PATH overrides the browser; without it the sandbox's preinstalled Chromium is
// used when present, otherwise Playwright's own download.
import { existsSync } from 'node:fs';
import { chromium } from 'playwright';

const url = process.argv[2] ?? 'http://localhost:3000/?model=placeholder';
const out = process.argv[3] ?? 'shot.png';
const [width, height] = (process.argv[4] ?? '1600x900').split('x').map(Number);
const settleMs = Number(process.env.SHOT_SETTLE_MS ?? 2500);
const chrome = process.env.CHROME_PATH ?? '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const browser = await chromium.launch({
  headless: true,
  executablePath: existsSync(chrome) ? chrome : undefined,
  // software WebGL through ANGLE + SwiftShader, so it works without a GPU
  args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--use-gl=angle'],
});

try {
  const page = await browser.newPage({ viewport: { width, height } });
  page.on('console', (msg) => {
    if (msg.type() === 'error' || msg.type() === 'warning') console.error(`[page ${msg.type()}] ${msg.text()}`);
  });
  page.on('pageerror', (err) => console.error(`[page error] ${err.message}`));

  await page.goto(url, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__garage?.loaded || window.__garage?.error, null, { timeout: 120_000 });
  const error = await page.evaluate(() => window.__garage.error);
  if (error) throw new Error(error);

  await page.waitForTimeout(settleMs);
  // software GL can take seconds per frame: let two more frames land so the capture shows the settled state
  await page.evaluate(() => new Promise((done) => requestAnimationFrame(() => requestAnimationFrame(done))));
  await page.screenshot({ path: out });
  console.log(JSON.stringify(await page.evaluate(() => window.__garage), null, 2));
  console.error(`saved ${out}`);
} finally {
  await browser.close();
}
