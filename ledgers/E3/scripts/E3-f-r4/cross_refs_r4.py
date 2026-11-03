"""E3 slice f round 4: every labelled reference on a slice card resolves to a labelled block in the named lesson."""
import html
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD4-E3-f/course/modules/E/E3")
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
LESSONS = ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08")

def lesson_text(name):
    raw = (ROOT / f"{name}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))

texts = {n: lesson_text(n) for n in LESSONS}
raw_html = {n: (ROOT / f"{n}.html").read_text(encoding="utf-8") for n in LESSONS}
label = re.compile(r"\b(Proposition|Remark|Lemma|Theorem|Definition|Example|Problem|Assumption|Section|section)\s+([0-9A-Z][0-9.a-z]*)")
checks = []
for c in cards:
    if c["lesson"] not in ("L01", "L02", "L03", "L04"):
        continue
    s = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for m in label.finditer(s):
        kind, num = m.group(1), m.group(2).rstrip(".")
        pre = s[max(0, m.start() - 14):m.start()]
        lesson = c["lesson"]
        lm = re.search(r"(L0[1-8])\s*$", pre)
        if lm:
            lesson = lm.group(1)
        if kind in ("Section", "section"):
            ok = f'id="s{num}"' in raw_html[lesson]
            checks.append((c["id"], lesson, f"section {num}", ok))
        else:
            # block title "Kind num" or problem title "Num ·" inside the lesson
            ok = (f"{kind} {num}" in texts[lesson]) or (kind == "Problem" and f'id="{num}"' in raw_html[lesson])
            checks.append((c["id"], lesson, f"{kind} {num}", ok))
bad = [r for r in checks if not r[3]]
print("references checked:", len(checks), "unresolved:", len(bad))
for r in bad:
    print("UNRESOLVED", r)
