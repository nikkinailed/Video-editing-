// Monthly market update graphic. Edit DATA, then: node social/market-update/render.js
const { chromium } = require('playwright');
const path = require('path');
const G = path.resolve(__dirname, '../../guides');

// Leave a value as null to print a blank line for writing in the number.
const CARROLL = {
  file: 'carroll-oct-2026', place: 'Carroll County', month: 'October 2026',
  stats: [
    { label: 'Median Sale Price', value: null, change: null },
    { label: 'Homes Sold', value: null, change: null },
    { label: 'Median Days on Market', value: null, change: null },
    { label: 'Active Listings', value: null, change: null },
  ],
  source: 'Source: Bright MLS via Maryland REALTORS®, October 2026',
};

const MARYLAND = {
  file: 'maryland-oct-2026', place: 'Maryland', month: 'October 2026',
  stats: [
    { label: 'Fewer Home Sales Than Last October', value: '16.5%', change: 'down from October 2025', dir: 'down' },
    { label: 'Active Listings', value: '19,236', change: 'up 22.8%', dir: 'up' },
    { label: 'Median Days on Market', value: '21', change: 'up from 17', dir: 'up' },
  ],
  source: 'Source: Bright MLS via Maryland REALTORS®, October 2026 statewide',
};

const fs = require('fs');
const font = (n, f) => `@font-face{font-family:${n};src:url(data:font/ttf;base64,${fs.readFileSync(path.join(G, f)).toString('base64')})}`;

const card = (d, theme) => {
  const dark = theme === 'bold';
  const bg = dark ? '#a428d6' : '#fbf4fb';
  const ink = dark ? '#fbf4fb' : '#3a1a47';
  const accent = dark ? '#fbf4fb' : '#a428d6';
  const tile = dark ? 'rgba(251,244,251,.12)' : '#ffffff';
  const tileBorder = dark ? 'rgba(251,244,251,.35)' : '#e0bbdf';
  const rows = d.stats.map(s => `
    <div class="tile">
      <div class="val">${s.value ?? '<span class="blank"></span>'}</div>
      <div class="lab">${s.label}</div>
      <div class="chg">${s.change ? (s.dir === 'down' ? '▼ ' : s.dir === 'up' ? '▲ ' : '') + s.change : (s.value ? '' : 'vs last year <span class="blank sm"></span>')}</div>
    </div>`).join('');
  return `<!doctype html><html><head><style>
  ${font('Fraunces', 'fraunces-900-normal.ttf')}
  ${font('Instrument', 'instrument-serif-400-normal.ttf')}
  ${font('InstrumentI', 'instrument-serif-400-italic.ttf')}
  ${font('Nunito', 'nunito-900-normal.ttf')}
  ${font('Literata', 'literata-400-normal.ttf')}
  html,body{margin:0}
  .card{width:1080px;height:1350px;box-sizing:border-box;padding:90px 80px 70px;background:${bg};color:${ink};
    display:flex;flex-direction:column;font-family:Literata;position:relative;overflow:hidden}
  .card:before{content:'';position:absolute;width:620px;height:620px;border-radius:50%;right:-220px;top:-240px;
    background:${dark ? 'rgba(251,244,251,.10)' : '#e0bbdf'};opacity:${dark ? 1 : .55}}
  .kicker{font-family:Nunito;letter-spacing:.22em;text-transform:uppercase;font-size:26px;color:${accent};position:relative}
  h1{font-family:Fraunces;font-size:118px;line-height:.95;margin:22px 0 6px;position:relative}
  .month{font-family:InstrumentI;font-size:72px;color:${accent};margin-bottom:46px;position:relative}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;position:relative}
  .grid.three .tile:first-child{grid-column:1 / span 2}
  .tile{background:${tile};border:2px solid ${tileBorder};border-radius:28px;padding:34px 36px;min-height:190px;box-sizing:border-box}
  .val{font-family:Fraunces;font-size:84px;line-height:1;color:${accent};min-height:84px}
  .lab{font-family:Nunito;font-size:28px;margin-top:14px;letter-spacing:.02em}
  .chg{font-size:26px;margin-top:10px;opacity:.85}
  .blank{display:inline-block;width:300px;border-bottom:4px solid ${tileBorder};height:70px}
  .blank.sm{width:120px;height:22px;border-bottom-width:3px}
  .take{font-family:Instrument;font-size:50px;line-height:1.1;margin:48px 0 0;position:relative}
  .cta{font-family:Nunito;font-size:30px;margin-top:22px;color:${accent}}
  .foot{margin-top:auto;padding-top:28px;display:flex;justify-content:space-between;align-items:flex-end;font-size:22px;line-height:1.45}
  .foot b{font-family:Nunito;font-size:26px}
  .src{font-size:18px;opacity:.7;margin-top:18px}
</style></head><body><div class="card">
  <div class="kicker">Housing Market Update</div>
  <h1>${d.place}</h1>
  <div class="month">${d.month}</div>
  <div class="grid ${d.stats.length === 3 ? 'three' : ''}">${rows}</div>
  <div class="take">Thinking about moving up or rightsizing?<br>Here is what October told us.</div>
  <div class="cta">Comment NEXT and let's find your next home 🏡</div>
  <div class="foot">
    <div><b>Nikki Nail | REALTOR®</b><br>Shelley Home Group of Cummings &amp; Co Realtors<br>410.746.6238 · nikki@theshelleyhomegroup.com</div>
  </div>
  <div class="src">${d.source}</div>
</div></body></html>`;
};

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  const jobs = [[CARROLL, 'light'], [CARROLL, 'bold'], [MARYLAND, 'bold']];
  for (const [d, t] of jobs) {
    await p.setContent(card(d, t), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const out = path.join(__dirname, `${d.file}-${t}.png`);
    await p.screenshot({ path: out });
    console.log(out);
  }
  await b.close();
})();
