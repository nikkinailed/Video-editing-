# Coffee & Contracts style: one small centered text block plus a location pin line, no word by word captions
import sys
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1]; F=S+"/fonts/ttf/"
EMO=ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",109)
CX=515
STYLES={
 "serif":dict(font=F+"instrument-serif-400-normal.ttf",size=62,color=(255,255,255),lh=66),
 "sans":dict(font="/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",size=50,color=(255,255,255),lh=62),
 "yellow":dict(font=F+"instrument-serif-400-normal.ttf",size=62,color=(246,226,122),lh=66),
}
def pin(size):
    im=Image.new("RGBA",(220,220),(0,0,0,0)); ImageDraw.Draw(im).text((20,20),"📍",font=EMO,embedded_color=True)
    im=im.crop(im.getbbox()); return im.resize((int(size*im.width/im.height),size),Image.LANCZOS)
def wrap(d,text,f,maxw=760):
    lines=[""]
    for w in text.split():
        t=(lines[-1]+" "+w).strip()
        if d.textlength(t,font=f)<=maxw: lines[-1]=t
        else: lines.append(w)
    return lines
def block(img,text,place,y,style):
    st=STYLES[style]; f=ImageFont.truetype(st["font"],st["size"]); d=ImageDraw.Draw(img)
    for i,l in enumerate(wrap(d,text,f)+[None]):
        yy=y+i*st["lh"]
        if l is None:
            p=pin(int(st["size"]*0.8)); w=p.width+12+d.textlength(place,font=f); x=CX-w/2
            img.alpha_composite(p,(int(x),int(yy+st["size"]*0.15))); x+=p.width+12; l=place
        else:
            x=CX-d.textlength(l,font=f)/2
        d.text((x+2,yy+3),l,font=f,fill=(0,0,0,120)); d.text((x,yy),l,font=f,fill=st["color"])
