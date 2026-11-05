# "3 reasons" list reel: hook, then one numbered reason per group of clips, then a CTA.
# Usage: python3 reasons.py <kit dir with fonts/ttf> <spec.json> <out.mp4>
# Text styles follow font Mix 2 (Bodoni caps + pink Instrument Serif italic). Output is silent.
import sys, os, json, subprocess
from PIL import Image, ImageDraw, ImageFont
S, specfile, out = sys.argv[1], sys.argv[2], sys.argv[3]
spec = json.load(open(specfile)); F = S + "/fonts/ttf/"
def font(n, s): return ImageFont.truetype(F + n, s)
CX = 515  # safe column center, nudged left of Instagram's right side buttons
WHT = (255, 255, 255); PINK = (224, 187, 223)
STYLES = {
    "caps": lambda: (font("bodoni-moda-500-normal.ttf", 62), WHT, True),
    "pink": lambda: (font("instrument-serif-400-italic.ttf", 128), PINK, False),
    "num": lambda: (font("instrument-serif-400-italic.ttf", 150), PINK, False),
    "body": lambda: (font("instrument-serif-400-normal.ttf", 100), WHT, True),
    "small": lambda: (font("instrument-serif-400-italic.ttf", 66), WHT, True),
}
def card(lines, y):
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for text, style in lines:
        f, c, heavy = STYLES[style]()
        if style == "caps": text = text.upper()
        w = d.textlength(text, font=f); x = CX - w / 2
        assert x >= 80 and x + w <= 950, ("too wide", text, w)
        if heavy: d.text((x, y), text, font=f, fill=(0, 0, 0, 170), stroke_width=4, stroke_fill=(0, 0, 0, 170))
        d.text((x + 3, y + 4), text, font=f, fill=(0, 0, 0, 150)); d.text((x, y), text, font=f, fill=c)
        b = f.getbbox("Hg"); y += int((b[3] - b[1]) * 1.25)
    return im
tmp = f"{S}/layers/{os.path.basename(out)}"; os.makedirs(tmp, exist_ok=True)
# 1. normalize each clip to 1080x1920 30fps, no audio, and join
parts = []; t0 = 0; starts = []
for i, sg in enumerate(spec["segments"]):
    p = f"{tmp}/seg{i}.mp4"; d = sg["dur"]
    z = sg.get("zoom", 1); W, H = int(1080 * z) // 2 * 2, int(1920 * z) // 2 * 2
    cx = {"left": "0", "right": "in_w-1080"}.get(sg.get("align"), "(in_w-1080)/2")  # zoom in and slide to keep a subject clear of the text
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop=1080:1920:{cx}:(in_h-1920)/2,fps=30"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-ss", str(sg.get("start", 0)), "-t", str(d), "-i", sg["src"], "-an",
                           "-vf", vf, "-t", str(d), "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", p])
    parts.append(p); starts.append(t0); t0 += d
dur = t0; starts.append(dur + 1)
lst = f"{tmp}/list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
base = f"{tmp}/base.mp4"; subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])
# 2. each card shows from its first segment until the next card's first segment
Image.new("RGBA", (1080, 1920), (0, 0, 0, 60)).save(f"{tmp}/dim.png")
cards = spec["cards"]
args = ["ffmpeg", "-v", "error", "-y", "-i", base, "-i", f"{tmp}/dim.png"]; fc = "[0][1]overlay[v0]"
for i, c in enumerate(cards):
    a = starts[c["seg"]]; b = starts[cards[i + 1]["seg"]] if i + 1 < len(cards) else dur + 1
    p = f"{tmp}/card{i}.png"; card(c["lines"], c["y"]).save(p)
    args += ["-i", p]; fc += f";[v{i}][{i + 2}]overlay=enable='between(t,{a:.2f},{b:.2f})'[v{i + 1}]"
args += ["-filter_complex", fc, "-map", f"[v{len(cards)}]", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
subprocess.check_call(args)
print(out, round(dur, 2))
