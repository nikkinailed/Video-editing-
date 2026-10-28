# Puts an Edits style text stack on a clean (text free) reel, Coffee & Contracts style: one block, no word captions
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stack as st
from PIL import Image
S, specfile, src, out = sys.argv[1:5]
st.F = S + "/fonts/ttf/"
spec = json.load(open(specfile))
tmp = f"{S}/layers/{os.path.basename(out)}"; os.makedirs(tmp, exist_ok=True)
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src]))
args = ["ffmpeg","-v","error","-y","-i",src]; fc = ""; last = "0"; n = 1
dim = Image.new("RGBA",(1080,1920),(0,0,0,spec.get("dim",45))); dim.save(f"{tmp}/dim.png")
args += ["-i",f"{tmp}/dim.png"]; fc += f"[0][1]overlay[v1]"; last = "v1"; n = 2
for i, L in enumerate(spec["layers"]):
    im = Image.new("RGBA",(1080,1920),(0,0,0,0)); end_y = st.stack(im, L["y"], L["lines"])
    if "cta" in spec:
        c = Image.new("RGBA",(1080,1920),(0,0,0,0)); st.draw_line(c, end_y + 20, **spec["cta"]); c.save(f"{tmp}/cta{i}.png")
    im.save(f"{tmp}/layer{i}.png"); a = L.get("start",0); b = L.get("end",dur+1)
    args += ["-i",f"{tmp}/layer{i}.png"]; fc += f";[{last}][{n}]overlay=enable='between(t,{a},{b})'[v{n}]"; last=f"v{n}"; n+=1
    if "cta" in spec:
        ca = max(a, dur - spec.get("cta_secs",2.5))
        if ca < b:
            args += ["-i",f"{tmp}/cta{i}.png"]; fc += f";[{last}][{n}]overlay=enable='between(t,{ca},{b})'[v{n}]"; last=f"v{n}"; n+=1
args += ["-filter_complex",fc,"-map",f"[{last}]","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",out]
subprocess.check_call(args); print(out, round(dur,2))
