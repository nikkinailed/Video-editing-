# Builds the NEXT guide story frames (1080x1920) and carousel slides (1080x1350) as HTML, rendered to images by render.js
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
@font-face{font-family:Advercase;src:url(instrument-serif-400-normal.ttf)}
@font-face{font-family:Advercase;font-style:italic;src:url(instrument-serif-400-italic.ttf)}
@font-face{font-family:Literature;src:url(literata-400-normal.ttf)}
@font-face{font-family:Cobbler;src:url(nunito-900-normal.ttf)}
@font-face{font-family:Poster;src:url(fraunces-900-normal.ttf)}
:root{--purple:#a428d6;--blush:#fbf4fb;--pink:#e0bbdf;--ink:#2b1a33;--soft:#6b5873}
*{box-sizing:border-box;margin:0}
body{width:WIDTHpx;height:HEIGHTpx;overflow:hidden;font-family:Literature,'Noto Color Emoji',serif;color:var(--ink);background:var(--blush);position:relative}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,12,34,.55) 0%,rgba(28,12,34,.15) 45%,rgba(28,12,34,.65) 100%)}
.cob{font-family:Cobbler;letter-spacing:.22em;text-transform:uppercase}
.adv{font-family:Advercase;font-weight:400;line-height:.98}
.adv i{font-style:italic;color:var(--pink)}
.pos{font-family:Poster}
.white{color:#fff}
.pill{display:inline-block;background:var(--purple);color:#fff;font-family:Cobbler,'Noto Color Emoji';letter-spacing:.18em;border-radius:999px}
.card{background:#fff;border-radius:28px;box-shadow:0 18px 50px rgba(90,30,110,.18)}
.ba{display:grid;grid-template-columns:auto 1fr;gap:18px 26px;align-items:start}
.tag{font-family:Cobbler;letter-spacing:.18em;font-size:24px;color:var(--purple);padding-top:10px}
.foot{position:absolute;left:80px;right:80px;bottom:56px;display:flex;justify-content:space-between;font-family:Cobbler;letter-spacing:.16em;font-size:22px;color:var(--soft);text-transform:uppercase}
"""

def page(w, h, body):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS.replace('WIDTH',str(w)).replace('HEIGHT',str(h))}</style></head><body>{body}</body></html>"

# Stories keep text between y 260 and y 1560 so Instagram's top bar and reply box never cover it, centered left of the right edge
stories = {
"story1": f"""<div class='bg' style="background-image:url(porch.jpg);background-position:50% 70%"></div><div class='shade'></div>
<div style='position:absolute;left:90px;right:110px;top:300px;display:flex;flex-direction:column;gap:30px;align-items:center;text-align:center'>
 <span class='pill' style='font-size:30px;padding:14px 30px'>NEW FREE GUIDE</span>
 <div class='adv white' style='font-size:150px'>Your Next<br><i>Home</i> Guide</div>
 <div class='white' style='font-size:40px;line-height:1.35'>for Carroll County families who need<br>more land, less upkeep or more room</div>
</div>""",
"story2": f"""<div style='position:absolute;inset:0;background:linear-gradient(170deg,#fbf4fb,#ecd0ec)'></div>
<div style='position:absolute;left:90px;right:110px;top:300px;display:flex;flex-direction:column;gap:34px;align-items:center;text-align:center'>
 <div class='cob' style='font-size:28px;color:var(--purple)'>BE HONEST</div>
 <div class='adv' style='font-size:128px'>What does your house<br><i style="color:var(--purple)">need most?</i></div>
 <div style='font-size:36px;color:var(--soft)'>Tap your answer 👇</div>
 <div style='height:430px;width:100%;border:4px dashed var(--pink);border-radius:30px;display:flex;align-items:center;justify-content:center;color:var(--soft);font-size:30px;font-family:Cobbler;letter-spacing:.14em'>ADD POLL STICKER HERE<br>MORE SPACE · LESS UPKEEP · MORE LAND</div>
</div>""",
"story3": f"""<div style='position:absolute;inset:0;background:var(--blush)'></div>
<div style='position:absolute;left:90px;right:110px;top:290px;display:flex;flex-direction:column;gap:34px'>
 <div class='cob' style='font-size:28px;color:var(--purple);text-align:center'>A PEEK INSIDE</div>
 <div style='display:flex;gap:40px;align-items:center'>
  <div class='card' style='flex:0 0 340px;height:440px;padding:26px;background:linear-gradient(160deg,#fbf4fb,#e0bbdf);display:flex;flex-direction:column;justify-content:space-between'>
   <div class='adv' style='font-size:62px'>Your Next<br><i style='color:var(--purple)'>Home</i><br>Guide</div>
   <div style='height:170px;border-radius:16px;background:url(nikki.jpg) center 30%/cover;border:5px solid #fff'></div>
  </div>
  <div style='display:flex;flex-direction:column;gap:22px;font-size:36px;line-height:1.25'>
   <div>✔️ 10 signs it's time</div><div>✔️ Buy first or sell first</div><div>✔️ Your equity calculator</div><div>✔️ Carroll County land checklist</div><div>✔️ A 90 day plan</div>
  </div>
 </div>
 <div class='card' style='padding:34px 40px;font-size:38px;line-height:1.35;text-align:center'>Too much mowing for a travel sports family?<br>A hilly yard where the ball rolls away?<br><b class='pos' style='color:var(--purple)'>There's a page for that.</b></div>
</div>""",
"story4": f"""<div class='bg' style="background-image:url(barn.jpg);background-position:50% 45%"></div><div class='shade'></div>
<div style='position:absolute;left:90px;right:110px;top:250px;display:flex;flex-direction:column;gap:22px;align-items:center;text-align:center'>
 <div class='cob white' style='font-size:30px'>WANT IT?</div>
 <div class='adv white' style='font-size:140px'>DM me<br><i>NEXT</i></div>
 <div class='white' style='font-size:42px;line-height:1.35'>and I'll send your free<br>Next Home Guide link 💜</div>
 <span class='pill' style='font-size:28px;padding:14px 30px'>LET'S FIND YOUR NEXT HOME</span>
</div>""",
}

def ex_slide(n, title, before, after, why, img, pos="50% 50%"):
    return f"""<div style='position:absolute;left:0;right:0;top:0;height:560px;background:url({img}) {pos}/cover'></div>
<div style='position:absolute;left:0;right:0;top:0;height:560px;background:linear-gradient(180deg,rgba(28,12,34,.0) 50%,rgba(28,12,34,.35))'></div>
<span class='pill' style='position:absolute;left:80px;top:480px;font-size:24px;padding:12px 24px'>EXAMPLE {n} OF 4</span>
<div style='position:absolute;left:80px;right:80px;top:600px;display:flex;flex-direction:column;gap:30px'>
 <div class='adv' style='font-size:78px'>{title}</div>
 <div class='ba' style='font-size:34px;line-height:1.35'><span class='tag'>BEFORE</span><span>{before}</span><span class='tag'>AFTER</span><span>{after}</span></div>
 <div style='font-size:28px;color:var(--soft)'>What made it work: {why}</div>
</div><div class='foot'><span>Next Home Guide</span><span>Swipe 👉</span></div>"""

slides = {
"slide1": f"""<div class='bg' style="background-image:url(mountain.jpg);background-position:50% 80%"></div><div class='shade'></div>
<div style='position:absolute;left:80px;right:120px;top:120px;display:flex;flex-direction:column;gap:26px'>
 <div class='cob white' style='font-size:26px'>📍 CARROLL COUNTY</div>
 <div class='adv white' style='font-size:118px'>Bigger isn't<br>always better.</div>
 <div class='white' style='font-size:44px;line-height:1.3'>Here's what rightsizing<br>really looks like here 👉</div>
</div>""",
"slide2": ex_slide(1,"Done mowing, busy with <i style='color:var(--purple)'>travel sports</i>","Three hours of mowing every week, and you're on a field two hours away every Saturday anyway.","A smaller yard, or lawn care that's covered or easy to hire out.","trading grass you never sit on for weekends back.","hayfield.jpg","50% 15%"),
"slide3": ex_slide(2,"A flat yard for <i style='color:var(--purple)'>soccer practice</i>","A Westminster home on a hill. The ball ends up in the neighbor's yard every time.","A flat, usable lot with room for a goal, a garden and the dog.","shopping for usable land, not just more acres.","field.jpg","50% 37%"),
"slide4": ex_slide(3,"Too much house, <i style='color:var(--purple)'>not enough land</i>","Five bedrooms, two of them storage, on a small suburban lot.","A house sized for how you live, on a few acres with room to roam.","putting the budget into land instead of square footage.","mountain.jpg","30% 85%"),
"slide5": ex_slide(4,"The kids <i style='color:var(--purple)'>moved out</i>","A two story colonial with stairs and rooms that stay closed.","Main level living near Main Street dinners and the grandkids' games.","selling first, then buying with the equity in hand.","barn.jpg","50% 47%"),
"slide6": f"""<div style='position:absolute;left:80px;right:80px;top:110px;display:flex;flex-direction:column;gap:34px'>
 <div class='cob' style='font-size:26px;color:var(--purple)'>THE QUESTION EVERYONE ASKS</div>
 <div class='adv' style='font-size:104px'>Buy first or<br><i style='color:var(--purple)'>sell first?</i></div>
 <div style='display:grid;grid-template-columns:1fr 1fr;gap:24px'>
  <div class='card' style='padding:30px'><div class='pos' style='font-size:34px;color:var(--purple)'>Sell first</div><div style='font-size:28px;margin-top:10px;line-height:1.35'>Know your budget. Ask for extra time so you move once.</div></div>
  <div class='card' style='padding:30px'><div class='pos' style='font-size:34px;color:var(--purple)'>Buy first</div><div style='font-size:28px;margin-top:10px;line-height:1.35'>Move on your schedule using your equity.</div></div>
  <div class='card' style='padding:30px'><div class='pos' style='font-size:34px;color:var(--purple)'>Contingent offer</div><div style='font-size:28px;margin-top:10px;line-height:1.35'>Your purchase depends on your home selling.</div></div>
  <div class='card' style='padding:30px'><div class='pos' style='font-size:34px;color:var(--purple)'>Time both</div><div style='font-size:28px;margin-top:10px;line-height:1.35'>Two settlements, one moving day.</div></div>
 </div>
 <div style='font-size:30px;color:var(--soft)'>The right one depends on your numbers. The guide walks you through it.</div>
</div><div class='foot'><span>Next Home Guide</span><span>Swipe 👉</span></div>""",
"slide7": f"""<div style='position:absolute;inset:0;background:linear-gradient(165deg,#fbf4fb 0%,#ecd0ec 100%)'></div>
<div style='position:absolute;left:80px;right:80px;top:110px;display:flex;gap:50px;align-items:center'>
 <div class='card' style='flex:0 0 380px;height:500px;padding:30px;background:linear-gradient(160deg,#fbf4fb,#e0bbdf);display:flex;flex-direction:column;justify-content:space-between;transform:rotate(-3deg)'>
  <div class='adv' style='font-size:70px'>Your Next<br><i style='color:var(--purple)'>Home</i><br>Guide</div>
  <div style='height:190px;border-radius:16px;background:url(nikki.jpg) center 30%/cover;border:5px solid #fff'></div>
 </div>
 <div style='display:flex;flex-direction:column;gap:20px;font-size:32px;line-height:1.3'>
  <div class='cob' style='font-size:24px;color:var(--purple)'>FREE GUIDE</div>
  <div>✔️ 10 signs it's time</div><div>✔️ Buy first or sell first</div><div>✔️ Equity calculator</div><div>✔️ Land checklist</div><div>✔️ 90 day plan</div>
 </div>
</div>
<div style='position:absolute;left:80px;right:80px;top:700px;display:flex;flex-direction:column;gap:22px;align-items:center;text-align:center'>
 <div class='adv' style='font-size:116px'>Comment <i style='color:var(--purple)'>NEXT</i></div>
 <div style='font-size:38px;line-height:1.35'>and let's find your next home.<br>I'll send your free guide link 💜</div>
 <div style='font-size:26px;color:var(--soft);margin-top:16px'>Nikki Nail, REALTOR® · Shelley Home Group of Cummings &amp; Co Realtors</div>
</div>""",
}

jobs = []
for name, body in stories.items():
    open(os.path.join(HERE, name + ".html"), "w").write(page(1080, 1920, body)); jobs.append([name, 1080, 1920])
for name, body in slides.items():
    open(os.path.join(HERE, name + ".html"), "w").write(page(1080, 1350, body)); jobs.append([name, 1080, 1350])
json.dump(jobs, open(os.path.join(HERE, "jobs.json"), "w"))
print(len(jobs), "pages")
