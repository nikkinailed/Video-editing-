# Giveaway reel generator: fill in a place, the gift card amount and a few clips, get a ready reel.
# Usage: python3 -I tools/giveaway.py giveaways/<place>.json   (renders with tools/beats.py)
# Each place file: {"place": "...", "town": "...", "amount": 50, "end": "Sunday, Dec 7", "hook": 1,
#                   "clips": [{"src": "...", "start": 0, "dur": 1.2}, {"src": "photo.jpg", "photo": true, "dur": 1.5}],
#                   "loves": ["the brisket", "the line out the door", "the sweet tea"]}
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("REEL_SCRATCH", "/tmp/claude-0/-home-user-Video-editing-/2ff7ae43-88db-5b34-b1bf-56000836fa59/scratchpad")

L = lambda t, s=54: dict(text=t, fontname="Literature", size=s)
A = lambda t, s=108: dict(text=t, fontname="Advercase", size=s)
P = lambda t, s=116: dict(text=t, fontname="Poster", size=s)
C = lambda t, s=36: dict(text=t, fontname="Cobbler", size=s, spacing=8)

# Hooks adapted from the conference slide ("The first second decides the next thirty")
HOOKS = {
    1: lambda g: [L("okay, I got some bad news", 54), A("there's only a few", 108), A("weeks left to try this", 104)],
    2: lambda g: [L("why is there a line", 54), A("outside this little spot", 104), L(f"in {g['town']}?", 54)],
    3: lambda g: [C("STOP RIGHT HERE"), A("for a chance", 108), A("to win this", 108)],
}

def spec(g):
    clips = g["clips"]; total = sum(c["dur"] for c in clips)
    loves = g["loves"]; t1, t2 = 3.2, min(6.6, total - 3.5)
    cta_y = g.get("cta_y", 200)
    beats = [
        dict(start=0, end=t1, y=200, lines=HOOKS[g.get("hook", 1)](g), max_y=g.get("max_y", 700)),
        dict(start=t1, end=t2, y=200, lines=[L(loves[0], 52), L(loves[1], 52), A(loves[2], 100)], max_y=g.get("max_y", 700)),
        dict(start=t2, end=total + 1, y=cta_y, max_y=g.get("max_y", 760), lines=[
            C(f"WIN A ${g['amount']} GIFT CARD"), P(g["place"], g.get("place_size", 96)),
            A("comment WIN", 100), L("like + share for bonus entries", 44), L(f"enter by {g['end']}", 44)]),
    ]
    segs = [dict(c) for c in clips]
    return dict(segments=segs, beats=beats)

if __name__ == "__main__":
    src = sys.argv[1]; g = json.load(open(src))
    name = os.path.splitext(os.path.basename(src))[0]
    sp = os.path.join(SCRATCH, "specs", f"giveaway_{name}.json"); os.makedirs(os.path.dirname(sp), exist_ok=True)
    json.dump(spec(g), open(sp, "w"))
    out = g.get("out") or os.path.join(os.path.dirname(HERE), "reels", "giveaways", f"{name}.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.check_call([sys.executable, "-I", os.path.join(HERE, "beats.py"), SCRATCH, sp, out])
