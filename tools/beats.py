# Story reels: hook, pain point, payoff, CTA as changing Edits style text stacks over fast cuts or one slow clip
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stack as st
from PIL import Image
S, specfile, out = sys.argv[1:4]
st.F = S + "/fonts/ttf/"
spec = json.load(open(specfile)); tmp = f"{S}/layers/{os.path.basename(out)}"; os.makedirs(tmp, exist_ok=True)
parts = []; total = 0
for i, sg in enumerate([] if "base" in spec else spec["segments"]):
    p = f"{tmp}/seg{i}.mp4"; d = sg["dur"]; fr = round(d*30)
    if sg.get("photo"):
        vf = f"scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,zoompan=z='1+0.06*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30"
        cmd = ["ffmpeg","-v","error","-y","-i",sg["src"],"-vf",vf,"-frames:v",str(fr)]
    else:
        sp = sg.get("speed",1); vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts={1/sp}*PTS"
        vf += ",minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1" if sp < 1 else ",fps=30"
        cmd = ["ffmpeg","-v","error","-y","-ss",str(sg.get("start",0)),"-t",str(d*sp+0.1),"-i",sg["src"],"-an","-vf",vf,"-frames:v",str(fr)]
    subprocess.check_call(cmd+["-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p",p]); parts.append(p); total += fr/30
if "base" in spec:  # reuse an already rendered clip, skips the slow motion step
    base = spec["base"]; total = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",base]))
else:
    open(f"{tmp}/list.txt","w").write("".join(f"file '{p}'\n" for p in parts))
    base = f"{tmp}/base.mp4"; subprocess.check_call(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{tmp}/list.txt","-c","copy",base])
Image.new("RGBA",(1080,1920),(0,0,0,spec.get("dim",50))).save(f"{tmp}/dim.png")
args = ["ffmpeg","-v","error","-y","-i",base,"-i",f"{tmp}/dim.png"]; fc = "[0][1]overlay[v1]"; last = "v1"; n = 2
for i, b in enumerate(spec["beats"]):
    im = Image.new("RGBA",(1080,1920),(0,0,0,0)); end_y = st.stack(im, b["y"], b["lines"])
    assert end_y <= b.get("max_y", 1560), ("beat runs too low", i, end_y)
    im.save(f"{tmp}/beat{i}.png"); e = b.get("end", total+1)
    args += ["-i",f"{tmp}/beat{i}.png"]; fc += f";[{last}][{n}]overlay=enable='between(t,{b['start']},{e})'[v{n}]"; last = f"v{n}"; n += 1
args += ["-filter_complex",fc,"-map",f"[{last}]","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-movflags","+faststart",out]
subprocess.check_call(args); print(out, round(total,2))
