"""Round-4: internal anchors in L04-L06 resolve; L06 cross-reference to Lesson 3 cost structure; banned and process words on the three pages."""
import html
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "course/modules/E/E1"
ids = {}
for L in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"):
    ids[L] = set(re.findall(r'\sid="([^"]+)"', (BASE / f"{L}.html").read_text(encoding="utf-8")))
for L in ("L04", "L05", "L06"):
    raw = (BASE / f"{L}.html").read_text(encoding="utf-8")
    bad, n = [], 0
    for href in re.findall(r'href="([^"]+)"', raw):
        if href.startswith("http"):
            bad.append(("EXTERNAL", href))
            continue
        if "#" not in href:
            continue
        path, frag = href.split("#", 1)
        n += 1
        if path == "":
            target = L
        else:
            m = re.search(r"E1/(L\d\d)\.html$", os.path.normpath(os.path.join(BASE, path)).replace("\\", "/"))
            target = m.group(1) if m else None
        if target is None:
            if "concepts.html" in path:
                continue
            bad.append(("UNRESOLVED", href))
        elif frag not in ids.get(target, set()):
            bad.append(("MISSING_ANCHOR", href))
    print(f"{L}: internal anchors checked={n} problems={bad}")
    plain = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    hits = re.findall(r"\b(obviously|clearly|TODO|lorem|TBD|builder|verifier|round \d|agent)\b", plain, re.I)
    print(f"{L}: banned/process word hits={hits}")
t = html.unescape(re.sub(r"<[^>]+>", " ", (BASE / "L06.html").read_text(encoding="utf-8")))
i = t.find("competitive equilibrium of Lesson 3")
print("L06 claim:", re.sub(r"\s+", " ", t[i:i + 150]))
q = html.unescape(re.sub(r"<[^>]+>", " ", (BASE / "L03.html").read_text(encoding="utf-8")))
m = re.search(r"C\(q\)\s*=\s*F\s*\+\s*cq\s*\+\s*kq\^2", q)
print("L03 cost:", re.sub(r"\s+", " ", q[m.start():m.start() + 60]) if m else "NOT FOUND", "| k > 0 present:", bool(re.search(r"k\s*>\s*0", q)))
