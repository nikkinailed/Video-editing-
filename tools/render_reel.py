import sys, os, subprocess
from PIL import Image, ImageDraw, ImageFont
S, clip, mix, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
F=S+"/fonts/ttf/"
def font(n,s): return ImageFont.truetype(F+n,s)
CX=515  # safe column center, nudged left of Instagram's right side buttons
YEL=(246,226,122); WHT=(255,255,255); PINK=(224,187,223); PURP=(164,40,214)
IS=lambda s:font("instrument-serif-400-normal.ttf",s); ISI=lambda s:font("instrument-serif-400-italic.ttf",s)
PF=lambda s:font("playfair-display-700-normal.ttf",s); BD=lambda s:font("bodoni-moda-500-normal.ttf",s)
CLIPS={
 "pumpkin":dict(hook=(("A haunted house,","but it's Route 140"),"at","5pm."),hooky=300,capy=1250,
   words="Tag the friend stuck in it right now".split(),cta="Comment HOME"),
 "porch":dict(hook=(("This porch","and a Friday night"),"at","home."),hooky=330,capy=1330,
   words="This is what more space feels like".split(),cta="Comment MOVING"),
}
def line(d,y,parts,heavy=False):
    w=sum(d.textlength(t,font=f) for t,f,_ in parts); x=CX-w/2
    assert x>=80 and x+w<=950, ("too wide",parts[0][0],w)
    for t,f,c in parts:
        if heavy: d.text((x,y),t,font=f,fill=(0,0,0,170),stroke_width=4,stroke_fill=(0,0,0,170))
        d.text((x+3,y+4),t,font=f,fill=(0,0,0,150)); d.text((x,y),t,font=f,fill=c); x+=d.textlength(t,font=f)
def hook(d,y,h):
    (a,b),c,e=h
    if mix==1:
        line(d,y,[(a,IS(104),YEL)]); line(d,y+105,[(b,IS(104),YEL)]); line(d,y+215,[(c+" ",IS(104),YEL),(e,ISI(104),YEL)])
    if mix==2:
        line(d,y,[(a.upper(),BD(60),WHT)],heavy=True); line(d,y+80,[(b.upper(),BD(60),WHT)],heavy=True); line(d,y+160,[(c+" "+e,ISI(120),PINK)])
    if mix==3:
        line(d,y,[(a,PF(70),WHT)]); line(d,y+88,[(b,PF(70),WHT)]); line(d,y+185,[(c+" ",ISI(106),YEL),(e,ISI(106),YEL)])
def word(d,y,t,cta=False):
    k=0.75 if cta else 1
    if mix==1:
        f=PF(int(96*k)); w=d.textlength(t,font=f)
        d.rounded_rectangle((CX-w/2-32,y-6,CX+w/2+32,y+int(130*k)),radius=26,fill=PURP+(235,)); d.text((CX-w/2,y),t,font=f,fill=WHT)
    if mix==2: line(d,y,[(t,IS(int(140*k)),WHT)])
    if mix==3: line(d,y,[(t,font("dm-serif-display-400-normal.ttf",int(124*k)),PINK)])
c=CLIPS[clip]; tmp=f"{S}/layers/{clip}{mix}"; os.makedirs(tmp,exist_ok=True)
base=Image.new("RGBA",(1080,1920),(0,0,0,55)); hook(ImageDraw.Draw(base),c["hooky"],c["hook"]); base.save(f"{tmp}/hook.png")
dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{S}/base/{clip}.mp4"]))
start, step = 1.0, 0.42
items=[(w,start+i*step,start+(i+1)*step,False) for i,w in enumerate(c["words"])]
items.append((c["cta"],items[-1][2],dur+1,True))
args=["ffmpeg","-v","error","-y","-i",f"{S}/base/{clip}.mp4","-i",f"{tmp}/hook.png"]
fc="[0][1]overlay[v0]"
for i,(t,a,b,cta) in enumerate(items):
    im=Image.new("RGBA",(1080,1920),(0,0,0,0)); word(ImageDraw.Draw(im),c["capy"],t,cta); p=f"{tmp}/w{i}.png"; im.save(p)
    args+=["-i",p]; fc+=f";[v{i}][{i+2}]overlay=enable='between(t,{a:.2f},{b:.2f})'[v{i+1}]"
args+=["-filter_complex",fc,"-map",f"[v{len(items)}]","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",out]
subprocess.check_call(args)
