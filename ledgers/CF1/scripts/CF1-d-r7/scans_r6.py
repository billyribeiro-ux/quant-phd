"""Round-6 scans of the CF1 project page and cards.json: banned strings, scope words, duplicates, cite keys, numbers.

Run: /path/to/checkout/.venv/bin/python -I scans_r6.py <checkout>
"""

import difflib
import glob
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
CF = ROOT / "course/modules/CF/CF1"
BANNED = [r"TODO", r"TBD", r"lorem", r"\.\.\.", r"…", r"for brevity", r"details omitted", r"beyond the scope",
          r"left as an exercise", r"you can add more", r"it is important to note", r"studies show", r"experts agree",
          r"it is well known", r"obviously", r"clearly", r"roughly half", r"about 6%", r"historically", r"It can be shown"]
SCOPE = r"\b(only|most|all|same|raises?|always|as much as|drives?|offsets?)\b"
page = re.sub(r"<[^>]+>", " ", html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>", "", (CF / "project.html").read_text(encoding="utf-8"), flags=re.S)))
cards = json.loads((CF / "cards.json").read_text(encoding="utf-8"))
print("banned hits in project.html:", {p: len(re.findall(p, page)) for p in BANNED if re.search(p, page)})
print("banned hits in cards.json:", {p: len(re.findall(p, json.dumps(cards, ensure_ascii=False))) for p in BANNED if re.search(p, json.dumps(cards, ensure_ascii=False))})
print("scope-word counts project.html:", len(re.findall(SCOPE, page)), "cards:", len(re.findall(SCOPE, json.dumps(cards, ensure_ascii=False))))
ids = [c["id"] for c in cards]
print("duplicate ids:", len(ids) - len(set(ids)), "duplicate fronts:", len(cards) - len({c["front"] for c in cards}), "duplicate backs:", len(cards) - len({c["back"] for c in cards}))
near = [(a["id"], b["id"]) for i, a in enumerate(cards) for b in cards[i + 1:] if difflib.SequenceMatcher(None, a["front"], b["front"]).ratio() > 0.8]
print("near-duplicate fronts (ratio > 0.8):", near)
reg = {e["key"] for e in json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))["entries"]}
print("cite keys missing from registry:", [(c["id"], k) for c in cards for k in (c.get("cite") or []) if k not in reg])
print("cards with neither cite nor basis:", len([c for c in cards if not c.get("cite") and not c.get("basis")]))
txt = {L: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape((CF / f"{L}.html").read_text(encoding="utf-8")))) for L in ["L01", "L02", "L03", "L04", "L05", "L06"]}
labs = "".join(open(f, encoding="utf-8").read() for f in glob.glob("/tmp/cf1-v/d/r6/labs/*/out.txt"))
alltext = " ".join(txt.values()) + " " + labs
missing = []
for c in cards:
    for n in set(re.findall(r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?", c["back"])):
        core = n.lstrip("-").replace(",", "")
        if core in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "20", "30", "100"}:
            continue
        if core not in alltext.replace(",", ""):
            missing.append((c["id"], n))
print("card numbers not found in lesson text or lab outputs:", missing)
