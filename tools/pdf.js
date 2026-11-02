const { chromium } = require('playwright');
(async () => {
  const [src, out, png] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 816, height: 1056 } });
  await p.goto('file://' + src); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, format: 'Letter', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
  await p.screenshot({ path: png, fullPage: true }); await b.close();
})();
