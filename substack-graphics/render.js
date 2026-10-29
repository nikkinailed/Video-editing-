const { chromium } = require('playwright');
const path = require('path');

const sparkle = (size) => `<svg width="${size}" height="${size}" viewBox="0 0 100 100"><path d="M50 0 C54 38 62 46 100 50 C62 54 54 62 50 100 C46 62 38 54 0 50 C38 46 46 38 50 0Z" fill="#8a6f55"/></svg>`;

const quotes = [
  {
    file: 'option1-sidelines.png',
    html: `Years from now<br>you won’t remember<br>the laundry.<br><em>You’ll remember<br>the Saturday mornings<br>on the sidelines.</em>`,
    size: 92,
  },
  {
    file: 'option2-went-for-it.png',
    html: `Fill your life with<br><em>“I’m so glad<br>we went for it”</em><br>and not<br><em>“I wish we had.”</em>`,
    size: 104,
  },
  {
    file: 'option3-someday.png',
    html: `<em>Someday</em><br>is not a plan.<br>The best chapters<br>start the day you<br><em>finally say yes.</em>`,
    size: 104,
  },
];

const page = (q) => `<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Montserrat:wght@400;500&display=swap" rel="stylesheet">
<style>
  html,body{margin:0}
  .card{width:1080px;height:1350px;position:relative;overflow:hidden;
    background:
      radial-gradient(ellipse 60% 35% at 92% 8%, rgba(214,186,140,.55), transparent 70%),
      radial-gradient(ellipse 45% 25% at 78% 22%, rgba(230,208,170,.45), transparent 70%),
      radial-gradient(ellipse 55% 30% at 5% 92%, rgba(214,186,140,.5), transparent 70%),
      radial-gradient(ellipse 40% 20% at 25% 80%, rgba(236,218,186,.5), transparent 70%),
      linear-gradient(160deg,#f6efe4 0%,#f3eadc 50%,#efe3d1 100%);}
  .grain{position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply}
  .vein{position:absolute;border-radius:50%;filter:blur(2px)}
  .quote{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;
    font-family:'Cormorant Garamond',serif;color:#5b4636;font-size:${q.size}px;line-height:1.08;letter-spacing:-.5px;padding:0 90px}
  em{font-style:italic}
  .sp{position:absolute}
  .sig{position:absolute;bottom:70px;left:0;right:0;text-align:center;font-family:'Montserrat',sans-serif;
    font-size:22px;letter-spacing:6px;color:#8a6f55;text-transform:uppercase}
</style></head><body>
<div class="card">
  <svg class="grain" width="1080" height="1350"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 .3  0 0 0 .35 0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>
  <svg class="grain" style="opacity:.45;mask-image:linear-gradient(150deg,#000 0%,transparent 25%,transparent 75%,#000 100%)" width="1080" height="1350"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".012 .03" numOctaves="4" seed="7"/><feColorMatrix values="0 0 0 0 .8  0 0 0 0 .68  0 0 0 0 .45  0 0 0 -2.2 1.25"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg>
  <div class="sp" style="top:80px;left:80px">${sparkle(70)}</div>
  <div class="sp" style="top:165px;left:150px">${sparkle(40)}</div>
  <div class="sp" style="bottom:170px;right:120px">${sparkle(70)}</div>
  <div class="sp" style="bottom:110px;right:80px">${sparkle(40)}</div>
  <div class="quote"><div>${q.html}</div></div>
  <div class="sig">Nikki Nail</div>
</div></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const q of quotes) {
    await p.setContent(page(q), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(__dirname, q.file) });
  }
  await browser.close();
})();
