import sys; sys.path.insert(0,sys.argv[2]); from quiet import *
from PIL import Image, ImageDraw, ImageFont
panels=[("porch","serif","this porch and the quiet after the kids finally fall asleep",360),
        ("hayframe","sans","some of you have never raced your kids down pumpkin mountain and it shows",330),
        ("pumpkin","yellow","this field and the last warm saturday of october",300)]
labels=["1  Quiet serif, white","2  Clean bold, white","3  Quiet serif, your yellow"]
sheet=Image.new("RGB",(3*452-20,840),(251,244,251)); lab=ImageFont.truetype(S+"/fonts/ttf/playfair-display-700-normal.ttf",20)
for i,(img,st,txt,y) in enumerate(panels):
    im=Image.open(f"{S}/{img}.jpg").convert("RGBA").resize((1080,1920)); block(im,txt,"Carroll County",y,st)
    sheet.paste(im.convert("RGB").resize((432,768)),(i*452,0)); ImageDraw.Draw(sheet).text((i*452+8,790),labels[i],font=lab,fill=(164,40,214))
sheet.save("/home/user/Video-editing-/previews/cc_style_options.jpg",quality=90)
