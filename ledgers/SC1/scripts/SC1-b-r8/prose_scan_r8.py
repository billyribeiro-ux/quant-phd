"""Round-8 scan of SC1 slice-b learner text: process words, banned strings, ellipses, scope words.

Usage: python3 -I ledgers/SC1/scripts/SC1-b-r8/prose_scan_r8.py  (run from the checkout root).
Strips <pre> blocks (code and expected output) and tags, then searches visible prose.
"""
import json
import re

PAGES = ["course/modules/SC/SC1/L04.html", "course/modules/SC/SC1/L05.html", "course/modules/SC/SC1/L06.html"]
PROCESS = re.compile(r"\b(build|builds|builder|builders|round|rounds|verifier|verifiers|ledger|agent|agents|audit|REQUESTS?|TODO|TBD|lorem|pending)\b", re.I)
BANNED = re.compile(r"(for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly)", re.I)
SCOPE = re.compile(r"\b(every|all|always|never|any|exactly|only|same|drives)\b", re.I)


def prose(html: str) -> str:
    html = re.sub(r"<pre.*?</pre>", " ", html, flags=re.S)
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", html)


for page in PAGES:
    text = prose(open(page, encoding="utf-8").read())
    print(f"== {page}")
    for label, rx in (("process", PROCESS), ("banned", BANNED)):
        hits = [m.group(0) for m in rx.finditer(text)]
        print(f"  {label} hits: {len(hits)} {sorted(set(h.lower() for h in hits))}")
    print(f"  ellipsis (U+2026 or three dots) in prose: {text.count(chr(0x2026)) + text.count('...')}")
    print(f"  scope-word count: {len(SCOPE.findall(text))}")

cards = json.load(open("course/modules/SC/SC1/cards.json", encoding="utf-8"))
sel = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
blob = " ".join(c["front"] + " " + c.get("back", "") for c in sel)
print("== cards L04-L06")
print(f"  cards: {len(sel)}")
print(f"  process hits: {sorted(set(m.group(0).lower() for m in PROCESS.finditer(blob)))}")
print(f"  banned hits: {sorted(set(m.group(0).lower() for m in BANNED.finditer(blob)))}")
print(f"  cards containing U+2026: {[c['id'] for c in sel if chr(0x2026) in c['front'] + c.get('back', '')]}")
ids = [c["id"] for c in cards]
fronts = {}
for c in cards:
    fronts.setdefault(c["front"].strip(), []).append(c["id"])
print(f"  total cards: {len(cards)}; duplicate ids: {len(ids) - len(set(ids))}; duplicate fronts: {[v for v in fronts.values() if len(v) > 1]}")
