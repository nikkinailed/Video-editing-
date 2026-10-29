import json
U="/root/.claude/uploads/2ff7ae43-88db-5b34-b1bf-56000836fa59"; O="/tmp/claude-0/-home-user-Video-editing-/2ff7ae43-88db-5b34-b1bf-56000836fa59/scratchpad/specs/"
L=lambda t,s=54:dict(text=t,fontname="Literature",size=s)
A=lambda t,s=112:dict(text=t,fontname="Advercase",size=s)
P=lambda t,s=120:dict(text=t,fontname="Poster",size=s)
C=lambda t,s=36:dict(text=t,fontname="Cobbler",size=s,spacing=8)
K=lambda t,s=110:dict(text=t,fontname="Coldia",size=s)
def beat(a,b,y,lines,**kw): return dict(start=a,end=b,y=y,lines=lines,**kw)
v=lambda f,start,dur,**kw:dict(src=f"{U}/{f}",start=start,dur=dur,**kw)
ph=lambda f,dur:dict(src=f"{U}/{f}",photo=True,dur=dur)

# 1 Pumpkin: slow clip, many words, LOCAL
json.dump(dict(segments=[v("a6a500e4-IMG_7183.mov",0,9.0,speed=0.33),ph("20e865c1-image.jpg",4.0)],
 beats=[beat(0,3.2,180,[L("reason #921232123 why I",50),L("put up with",50),P("Route 140",128)],max_y=620),
        beat(3.2,6.4,180,[L("because ten minutes later",50),A("it's open fields",104),A("and pumpkin patches",104)],max_y=620),
        beat(6.4,9.0,180,[L("no city noise",50),L("no hour long drive",50),A("just Saturdays like this",96)],max_y=620),
        beat(9.0,14,260,[C("COMMENT LOCAL"),A("for my free",104),A("Carroll County guide",104),L("farms, parks + family spots inside",44)])]),
 open(O+"pumpkin.json","w"))

# 2 Hayride: fast best moments, FALL
json.dump(dict(segments=[v("7d0c9d94-IMG_7186.mov",1,1.2),v("8297aa13-IMG_7166.mov",7.0,1.3),ph("20e865c1-image.jpg",1.1),
   v("a5006ac5-dupe.mov",3.0,1.0),v("8297aa13-IMG_7166.mov",2.0,1.1),v("7d0c9d94-IMG_7186.mov",5,1.0),
   v("7372f3c0-IMG_5422.mov",0.5,1.0),ph("1064ad2f-image.jpg",1.2),v("034e8c13-IMG_8628.mov",5.0,4.0)],
 beats=[beat(0,3.6,210,[C("SOME OF YOU HAVE NEVER"),A("raced down",116),A("pumpkin mountain",116),L("and it shows",54)]),
        beat(3.6,6.0,230,[L("the kids grow up fast",56),A("fall goes faster",116)]),
        beat(6.0,8.9,230,[L("hayrides. pumpkin walls.",56),A("one more time",116),A("down the hill",116)]),
        beat(8.9,14,930,[C("COMMENT FALL"),A("for my free fall guide",100),L("the best farms + hayrides",46),L("before the season ends",46)])]),
 open(O+"hayride.json","w"))

# 3 Crowds: fast best moments, LOCAL
json.dump(dict(segments=[v("7372f3c0-IMG_5422.mov",0,1.3),v("a9d0f9b1-IMG_7187.mov",2.4,1.3),v("8297aa13-IMG_7166.mov",7.2,1.1),
   v("a5006ac5-dupe.mov",1.0,1.0),v("a9d0f9b1-IMG_7187.mov",0.2,1.1),v("7372f3c0-IMG_5422.mov",3.5,1.0),
   ph("20e865c1-image.jpg",1.0),ph("1064ad2f-image.jpg",4.2)],
 beats=[beat(0,3.4,180,[A("you couldn't pry me",96),A("out of",96),P("Carroll County",104),K("if you tried",100)]),
        beat(3.4,6.4,200,[L("packed pumpkin patches",54),L("small town parades",54),A("running into everyone",104),A("you know",104)]),
        beat(6.4,8.0,200,[L("some people move away",54),A("most of us come back",104)]),
        beat(8.0,13,180,[C("COMMENT LOCAL"),A("for my free",100),A("Carroll County guide",100),L("towns, schools + favorite spots",44)],max_y=780)]),
 open(O+"crowds.json","w"))

# 4 Porch: one slow clip, pain points, MOVING
json.dump(dict(segments=[v("2ac4d0fc-IMG_7325.mov",0,13.0,speed=0.38)],
 beats=[beat(0,3.2,170,[L("that feeling when you finally",48),A("move into",108),A("a bigger house",108)],max_y=640),
        beat(3.2,6.2,170,[L("no more",48),A("kids sharing rooms",104),A("shoes piled at the door",96)],max_y=640),
        beat(6.2,9.2,170,[L("no more",48),A("everyone on top of",104),A("each other at night",104)],max_y=640),
        beat(9.2,14,170,[C("COMMENT MOVING"),A("for my free",100),A("move up guide",100),L("what your home could sell for",42)],max_y=640)]),
 open(O+"porch.json","w"))

# Porch rightsizing versions, reuse the slow porch footage
PB="/tmp/claude-0/-home-user-Video-editing-/2ff7ae43-88db-5b34-b1bf-56000836fa59/scratchpad/layers/porch_v3.mp4/base.mp4"
json.dump(dict(base=PB,
 beats=[beat(0,3.2,170,[L("that feeling when you stop",48),A("taking care of a house",100),A("you're never home for",100)],max_y=640),
        beat(3.2,6.2,170,[L("too many rooms to clean",48),L("a yard you never use",48),A("gone every weekend",104),A("for travel sports",104)],max_y=640),
        beat(6.2,9.2,170,[L("less house",48),A("more life",116)],max_y=640),
        beat(9.2,14,170,[C("COMMENT MOVING"),A("for my free",100),A("rightsizing guide",100),L("what your home could sell for",42)],max_y=640)]),
 open(O+"porch_rightsize.json","w"))
json.dump(dict(base=PB,
 beats=[beat(0,3.2,170,[L("too much house",52),A("not enough land",116)],max_y=640),
        beat(3.2,6.2,170,[L("bedrooms nobody uses",48),L("a backyard you can see across",48),A("and no room to roam",104)],max_y=640),
        beat(6.2,9.2,170,[L("trade the square footage",48),A("for acreage",116)],max_y=640),
        beat(9.2,14,170,[C("COMMENT MOVING"),A("for my free",100),A("move guide",100),L("what your home could sell for",42)],max_y=640)]),
 open(O+"porch_land.json","w"))
