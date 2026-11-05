"""SC1-b round 7: duplicate scan of all cards, card id/lesson census, U+2026 scan (cards and pages), process-word scan (prose)."""
import html
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

ROOT = pathlib.Path(sys.argv[1]) / "course/modules/SC/SC1"
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("lesson census for L04-L06:", Counter(c["lesson"] for c in cards if c["lesson"] in ("L04", "L05", "L06")))
for lesson in ("L04", "L05", "L06"):
    sel = sorted(int(c["id"].split("c")[-1]) for c in cards if c["lesson"] == lesson)
    print(lesson, "ids:", sel[0], "to", sel[-1], "count", len(sel))
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
fronts = defaultdict(list)
backs = defaultdict(list)
for c in cards:
    fronts[norm(c["front"])].append(c["id"])
    backs[norm(c["back"])[:120]].append(c["id"])
print("duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("near-duplicate backs (120 chars):", [v for v in backs.values() if len(v) > 1])
print("cards containing U+2026:", [(c["id"], k) for c in cards for k in ("front", "back") if "…" in c[k]])
banned = re.compile(r"(\bTODO\b|\bTBD\b|\blorem\b|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|\bobviously\b|\bclearly\b|\.\.\.)", re.I)
proc = re.compile(r"(\bbuilder\b|\bbuild\b|\bround\b|verifier|ledger|\bagent\b|\baudit\b|\bfixer\b|REQUESTS|\bpending\b)", re.I)
for f in ("L04.html", "L05.html", "L06.html"):
    t = (ROOT / f).read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<pre.*?</pre>", "", t, flags=re.S)
    t = re.sub(r"\\\(.*?\\\)|\\\[.*?\\\]", "MATH", t, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    print(f, "banned hits:", [m.group(0) for m in banned.finditer(t)], "process-word hits:", [m.group(0) for m in proc.finditer(t)],
          "U+2026 outside math:", t.count("…"))
