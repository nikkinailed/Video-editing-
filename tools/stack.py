# Recreates the Edits app stacked text looks with the closest free fonts
import sys
from PIL import Image, ImageDraw, ImageFont
S=sys.argv[1] if len(sys.argv)>1 else "."
F=S+"/fonts/ttf/"
EMO=ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",109)
FONTS={  # Edits font name: closest free match
 "Literature":"literata-400-normal.ttf","Poster":"fraunces-900-normal.ttf","Advercase":"instrument-serif-400-normal.ttf",
 "Cobbler":"nunito-900-normal.ttf","Coldia":"allura-400-normal.ttf","Luckiest Guy":"luckiest-guy-400-normal.ttf",
 "Lobster Two":"lobster-two-700-normal.ttf","Playfair":"playfair-display-700-normal.ttf","Instrument Serif":"instrument-serif-400-normal.ttf"}
CX=515
def pin(size):
    im=Image.new("RGBA",(220,220),(0,0,0,0)); ImageDraw.Draw(im).text((20,20),"📍",font=EMO,embedded_color=True)
    im=im.crop(im.getbbox()); return im.resize((int(size*im.width/im.height),size),Image.LANCZOS)
def draw_line(img,y,text,fontname,size,color=(255,255,255),spacing=0,shadow=True):
    d=ImageDraw.Draw(img); f=ImageFont.truetype(F+FONTS[fontname],size)
    has_pin=text.startswith("📍 "); t=text[2:] if has_pin else text
    chars=list(t); widths=[d.textlength(c,font=f)+spacing for c in chars]; w=sum(widths)-spacing
    p=pin(int(size*0.8)) if has_pin else None
    if p: w+=p.width+int(size*0.2)
    x=CX-w/2; assert x>=70 and x+w<=960, ("too wide",text,w)
    if p: img.alpha_composite(p,(int(x),int(y+size*0.2))); x+=p.width+int(size*0.2)
    for c,cw in zip(chars,widths):
        if shadow: d.text((x+2,y+3),c,font=f,fill=(0,0,0,110))
        d.text((x,y),c,font=f,fill=color); x+=cw
    asc,desc=f.getmetrics(); return y+asc+desc
def stack(img,y,lines,gap=6):
    for l in lines:
        y=draw_line(img,y,**l)+gap
    return y
