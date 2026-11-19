// Monthly market update graphic. Edit DATA, then: node social/market-update/render.js
const { chromium } = require('playwright');
const path = require('path');
const G = path.resolve(__dirname, '../../guides');

// Leave a value as null to print a blank line for writing in the number.
const CARROLL = {
  file: 'carroll-oct-2026', place: 'Carroll County', month: 'October 2026',
  stats: [
    { label: 'Median Sale Price', value: '$472,500', change: 'down about 4.5% vs last year', dir: 'down' },
    { label: 'Homes Sold', value: '168', change: 'up about 12.5% vs last year', dir: 'up' },
    { label: 'Days to Sell', value: '24', change: 'roughly, give or take' },
    { label: 'Active Listings', value: '408', change: '2.6 months of supply' },
    { label: 'New Listings', value: '201', change: '91 went under contract' },
  ],
  take: 'Prices eased a little. Sales picked up.<br>Sellers still have the edge.',
  source: 'Sources: Bright MLS October 2026 Carroll County residential report. Year over year trend from Redfin.',
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
  .grid.odd .tile:first-child{grid-column:1 / span 2}
  .tile{background:${tile};border:2px solid ${tileBorder};border-radius:28px;padding:34px 36px;min-height:190px;box-sizing:border-box}
  .val{font-family:Fraunces;font-size:84px;line-height:1;color:${accent};min-height:84px}
  .lab{font-family:Nunito;font-size:28px;margin-top:14px;letter-spacing:.02em}
  .chg{font-size:26px;margin-top:10px;opacity:.85}
  .blank{display:inline-block;width:300px;border-bottom:4px solid ${tileBorder};height:70px}
  .blank.sm{width:120px;height:22px;border-bottom-width:3px}
  .grid.odd.big .tile{min-height:0;padding:22px 32px}.grid.big .val{font-size:64px;min-height:0}.grid.big .lab{font-size:26px}.grid.big .chg{font-size:24px}.grid.big{gap:20px}.grid.big .lab{margin-top:8px}.grid.big .chg{margin-top:6px}
  .card.big h1{font-size:104px;margin-top:16px}.card.big .month{font-size:62px;margin-bottom:30px}.card.big .take{font-size:44px;margin-top:30px}.card.big{padding-top:76px}
  .take{font-family:Instrument;font-size:50px;line-height:1.1;margin:40px 0 0;position:relative}
  .cta{font-family:Nunito;font-size:30px;margin-top:22px;color:${accent}}
  .foot{margin-top:auto;padding-top:28px;display:flex;justify-content:space-between;align-items:flex-end;font-size:22px;line-height:1.45}
  .foot b{font-family:Nunito;font-size:26px}
  .src{font-size:18px;opacity:.7;margin-top:18px}
</style></head><body><div class="card ${d.stats.length > 4 ? 'big' : ''}">
  <div class="kicker">Housing Market Update</div>
  <h1>${d.place}</h1>
  <div class="month">${d.month}</div>
  <div class="grid ${d.stats.length % 2 ? 'odd' : ''} ${d.stats.length > 4 ? 'big' : ''}">${rows}</div>
  <div class="take">${d.take || 'Thinking about moving up or rightsizing?<br>Here is what October told us.'}</div>
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
