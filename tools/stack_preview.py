import sys; sys.path.insert(0,sys.argv[2]); from stack import *
S=sys.argv[1]
P=[("pumpkin",250,[dict(text="a haunted house",fontname="Literature",size=64),
                  dict(text="Route 140",fontname="Poster",size=150),
                  dict(text="at 5pm",fontname="Literature",size=64),
                  dict(text="📍 CARROLL COUNTY",fontname="Cobbler",size=38,spacing=8)]),
   ("porch",230,[dict(text="THIS PORCH AND",fontname="Cobbler",size=42,spacing=10),
                dict(text="the quiet after",fontname="Advercase",size=120),
                dict(text="the kids fall asleep",fontname="Advercase",size=120),
                dict(text="📍 Carroll County",fontname="Literature",size=48)]),
   ("barn",250,[dict(text="fine, the crowds",fontname="Advercase",size=96),
               dict(text="are worth it",fontname="Poster",size=128),
               dict(text="Carroll County",fontname="Coldia",size=130)])]
labels=["1  Literature + Poster + Cobbler","2  Cobbler + Advercase + Literature","3  Advercase + Poster + Coldia"]
sheet=Image.new("RGB",(3*452-20,840),(251,244,251)); lab=ImageFont.truetype(S+"/fonts/ttf/playfair-display-700-normal.ttf",20)
for i,(img,y,lines) in enumerate(P):
    im=Image.open(f"{S}/{img}.jpg").convert("RGBA").resize((1080,1920)); stack(im,y,lines)
    sheet.paste(im.convert("RGB").resize((432,768)),(i*452,0)); ImageDraw.Draw(sheet).text((i*452+8,790),labels[i],font=lab,fill=(164,40,214))
sheet.save("/home/user/Video-editing-/previews/edits_font_stacks.jpg",quality=90)
