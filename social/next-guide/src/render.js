// Renders each built HTML page to a PNG at its exact Instagram size
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const dir = __dirname, out = path.join(dir, '..'); const jobs = JSON.parse(fs.readFileSync(path.join(dir, 'jobs.json')));
  const b = await chromium.launch();
  for (const [name, w, h] of jobs) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('file://' + path.join(dir, name + '.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(out, name + '.png') }); await p.close();
  }
  await b.close();
})();
