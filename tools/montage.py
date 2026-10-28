import sys, os, json, subprocess
from PIL import Image, ImageDraw, ImageFont
S, specfile, mix, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
spec=json.load(open(specfile)); F=S+"/fonts/ttf/"
def font(n,s): return ImageFont.truetype(F+n,s)
CX=515  # safe column center, nudged left of Instagram's right side buttons
YEL=(246,226,122); WHT=(255,255,255); PINK=(224,187,223); PURP=(164,40,214)
IS=lambda s:font("instrument-serif-400-normal.ttf",s); ISI=lambda s:font("instrument-serif-400-italic.ttf",s)
PF=lambda s:font("playfair-display-700-normal.ttf",s); BD=lambda s:font("bodoni-moda-500-normal.ttf",s)
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
    if mix==2: line(d,y,[(t,IS(int(140*k)),WHT)],heavy=True)
    if mix==3: line(d,y,[(t,font("dm-serif-display-400-normal.ttf",int(124*k)),PINK)])
tmp=f"{S}/layers/{os.path.basename(out)}"; os.makedirs(tmp,exist_ok=True)
# 1. normalize each segment to 1080x1920 30fps and join
parts=[]; t0=0; bounds=[]
for i,sg in enumerate(spec["segments"]):
    p=f"{tmp}/seg{i}.mp4"; d=sg["dur"]
    cover="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    if sg.get("photo"):
        fr=int(d*30)
        vf=f"scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,zoompan=z='1+0.08*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30"
        cmd=["ffmpeg","-v","error","-y","-i",sg["src"],"-vf",vf,"-frames:v",str(fr)]
    else:
        sp=sg.get("speed",1)
        cmd=["ffmpeg","-v","error","-y","-ss",str(sg.get("start",0)),"-t",str(d/sp),"-i",sg["src"],"-an","-vf",f"{cover},setpts={1/sp}*PTS,fps=30","-t",str(d)]
    subprocess.check_call(cmd+["-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p",p])
    parts.append(p); bounds.append((t0,t0+d,sg)); t0+=d
lst=f"{tmp}/list.txt"; open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
base=f"{tmp}/base.mp4"; subprocess.check_call(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c","copy",base])
dur=t0
# 2. text layers: hook shows only over segments flagged hook, words placed at each segment's safe height
hk=Image.new("RGBA",(1080,1920),(0,0,0,0)); hook(ImageDraw.Draw(hk),spec["hooky"],spec["hook"]); hk.save(f"{tmp}/hook.png")
dim=Image.new("RGBA",(1080,1920),(0,0,0,55)); dim.save(f"{tmp}/dim.png")
def seg_at(t): return next(sg for a,b,sg in bounds if a<=t<b) if t<dur else bounds[-1][2]
start,step=spec.get("words_start",1.0),spec.get("step",0.42)
items=[(w,start+i*step,start+(i+1)*step,False) for i,w in enumerate(spec["words"])]
items.append((spec["cta"],items[-1][2],dur+1,True))
args=["ffmpeg","-v","error","-y","-i",base,"-i",f"{tmp}/dim.png","-i",f"{tmp}/hook.png"]
hook_on="+".join(f"between(t,{a:.2f},{b:.2f})" for a,b,sg in bounds if sg.get("hook",True))
fc=f"[0][1]overlay[d];[d][2]overlay=enable='{hook_on}'[v0]"
for i,(t,a,b,cta) in enumerate(items):
    im=Image.new("RGBA",(1080,1920),(0,0,0,0)); word(ImageDraw.Draw(im),seg_at(a)["capy"],t,cta); p=f"{tmp}/w{i}.png"; im.save(p)
    args+=["-i",p]; fc+=f";[v{i}][{i+3}]overlay=enable='between(t,{a:.2f},{b:.2f})'[v{i+1}]"
args+=["-filter_complex",fc,"-map",f"[v{len(items)}]","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",out]
subprocess.check_call(args)
print(out, round(dur,2))
