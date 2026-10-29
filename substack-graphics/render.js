// Renders Substack quote graphics (1080 x 1350).
// Usage: node render.js <week folder>
// The week folder holds quotes.json: [{ "file", "html", "size", "style": "cream" | "photo", "photo" }]
// "photo" is a path relative to the week folder, used when style is "photo".
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const sparkle = (size, color) => `<svg width="${size}" height="${size}" viewBox="0 0 100 100"><path d="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z" fill="${color}"/></svg>`;

const sparkles = (color) => `
  <div class="sp" style="top:80px;left:80px">${sparkle(70, color)}</div>
  <div class="sp" style="top:165px;left:150px">${sparkle(40, color)}</div>
  <div class="sp" style="bottom:150px;right:120px">${sparkle(70, color)}</div>
  <div class="sp" style="bottom:90px;right:80px">${sparkle(40, color)}</div>`;

const creamLayers = `
  <svg class="layer" style="opacity:.35;mix-blend-mode:multiply" width="1080" height="1350"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 .3  0 0 0 .35 0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
  <svg class="layer" style="opacity:.45;mix-blend-mode:multiply;mask-image:linear-gradient(150deg,#000 0%,transparent 25%,transparent 75%,#000 100%)" width="1080" height="1350"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".012 .03" numOctaves="4" seed="7"/><feColorMatrix values="0 0 0 0 .8  0 0 0 0 .68  0 0 0 0 .45  0 0 0 -2.2 1.25"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg>`;

const page = (q, photoUrl) => {
  const photo = q.style === 'photo';
  return `<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
  html,body{margin:0}
  .card{width:1080px;height:1350px;position:relative;overflow:hidden;
    background:
      radial-gradient(ellipse 60% 35% at 92% 8%, rgba(214,186,140,.55), transparent 70%),
      radial-gradient(ellipse 45% 25% at 78% 22%, rgba(230,208,170,.45), transparent 70%),
      radial-gradient(ellipse 55% 30% at 5% 92%, rgba(214,186,140,.5), transparent 70%),
      radial-gradient(ellipse 40% 20% at 25% 80%, rgba(236,218,186,.5), transparent 70%),
      linear-gradient(160deg,#f6efe4 0%,#f3eadc 50%,#efe3d1 100%);}
  .layer{position:absolute;inset:0}
  .photo{position:absolute;inset:0;background:url('${photoUrl}') center/cover;filter:saturate(.75) sepia(.18)}
  .tint{position:absolute;inset:0;background:linear-gradient(180deg,rgba(60,45,32,.25) 0%,rgba(60,45,32,.45) 50%,rgba(60,45,32,.3) 100%)}
  .quote{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;
    font-family:'Cormorant Garamond',serif;color:${photo ? '#fbf6ee' : '#5b4636'};font-size:${q.size}px;line-height:1.08;letter-spacing:-.5px;padding:0 90px;
    ${photo ? 'text-shadow:0 2px 18px rgba(40,28,18,.45);' : ''}}
  em{font-style:italic}
  .sp{position:absolute}
</style></head><body>
<div class="card">
  ${photo ? '<div class="photo"></div><div class="tint"></div>' : creamLayers}
  ${sparkles(photo ? '#f3e6d3' : '#8a6f55')}
  <div class="quote"><div>${q.html}</div></div>
</div></body></html>`;
};

(async () => {
  const dir = path.resolve(process.argv[2] || '.');
  const quotes = JSON.parse(fs.readFileSync(path.join(dir, 'quotes.json'), 'utf8'));
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const q of quotes) {
    let photoUrl = '';
    if (q.style === 'photo') {
      const file = path.join(dir, q.photo);
      const ext = path.extname(file).slice(1).toLowerCase().replace('jpg', 'jpeg');
      photoUrl = `data:image/${ext};base64,${fs.readFileSync(file).toString('base64')}`;
    }
    await p.setContent(page(q, photoUrl), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(dir, q.file) });
  }
  await browser.close();
})();
