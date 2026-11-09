"""Misc delta checks: derivative example values, duplicate card fronts, LaTeX command set, problem counts, hours lines."""
import json
import re
import subprocess
from fractions import Fraction

REPO = "/Users/billyribeiro/.fanout/wt/verifyS6-M5-b"
OLD = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"
NEW = "e896b7a4"


def show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True, cwd=REPO).stdout


# (b) L06 Problem solution f(x)=x^3-3x on [-2,2]
f = lambda x: x**3 - 3 * x
vals = {x: f(Fraction(x)) for x in (-2, -1, 1, 2)}
print("(b) f values:", {k: str(v) for k, v in vals.items()}, "max", str(max(vals.values())), "at", [k for k, v in vals.items() if v == max(vals.values())], "min", str(min(vals.values())), "at", [k for k, v in vals.items() if v == min(vals.values())])
print("    f'(x)=3x^2-3 zeros:", [x for x in (-1, 1) if 3 * x * x - 3 == 0])
# (c) duplicate fronts across the file
cards = json.loads(show(NEW, "course/modules/M/M5/cards.json"))
fronts = [c["front"] for c in cards]
dups = sorted({x for x in fronts if fronts.count(x) > 1})
print("(c) cards:", len(cards), "unique ids:", len({c['id'] for c in cards}), "duplicate fronts:", len(dups))
# (d) LaTeX command set per slice page, old vs new
for page in ("L05", "L06", "L07"):
    cmds = {}
    for rev in (OLD, NEW):
        t = show(rev, f"course/modules/M/M5/{page}.html").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        cmds[rev] = (set(re.findall(r"\\[A-Za-z]+", t)), len(re.findall(r"class=\"problem\"", t)), len(re.findall(r"<svg", t)), len(re.findall(r"data-hours", t)))
    o, n = cmds[OLD], cmds[NEW]
    print(f"(d) {page}: LaTeX commands equal={o[0] == n[0]} new-only={sorted(n[0] - o[0])} removed={sorted(o[0] - n[0])}; problems old/new={o[1]}/{n[1]}; svg old/new={o[2]}/{n[2]}; data-hours old/new={o[3]}/{n[3]}")
# (e) hours lines and files outside the slice unchanged
for path in ("course/index.html", "course/modules/M/M5/project.html", "curriculum/01-foundations.yaml"):
    print(f"(e) {path}: bytes identical across pins = {show(OLD, path) == show(NEW, path)}")
for page in ("L05", "L06", "L07", "L10"):
    print(f"(e) {page} data-hours line:", [l.strip()[:90] for l in show(NEW, f"course/modules/M/M5/{page}.html").split("\n") if "data-hours" in l][:1])
