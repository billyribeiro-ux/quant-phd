import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course"

def txt(f: Path) -> str:
    s = f.read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"[ \t]+", " ", s))

concepts = (root / "concepts.html").read_text(encoding="utf-8")
for cid in ("present-value", "discount-factor", "geometric-series"):
    print(cid, "anchor count in concepts.html:", len(re.findall(r'id="%s"' % cid, concepts)))
    m = re.search(r'<[^>]*id="%s"[^>]*>' % cid, concepts)
    print("   ", m.group(0)[:200] if m else None)
for f in ("modules/M/M1/L05.html", "modules/M/M1/L06.html"):
    p = root / f
    h1 = re.search(r"<h1>(.*?)</h1>", p.read_text(encoding="utf-8"), re.S)
    print(f, "| h1:", h1.group(1) if h1 else None)
    t = txt(p)
    for kw in ("present value", "discount factor", "geometric series", "Geometric series"):
        i = t.find(kw)
        print("   ", kw, "->", t[max(0, i - 60): i + 120].replace("\n", " ") if i >= 0 else None)
