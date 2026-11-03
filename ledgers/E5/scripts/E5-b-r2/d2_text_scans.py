"""Round 2 verifier scans (E5-b): banned strings, process words, scope words, why-it-matters length, hours, notation symbols.

Run: .venv/bin/python -I ledgers/E5/scripts/E5-b-r2/d2_text_scans.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ["L04", "L05", "L06"]
TWINS = {p: ROOT / f"tests/labs/E5/lab-E5-{p}-1.py" for p in PAGES}
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly"]
PROCESS = ["build", "builder", "round", "verifier", "REQUEST", "unit report", "verification", "ledger", "fragment",
           "campaign", "slice", "planner", "Architect", "plan ", "E5-open", "open item"]
SCOPE = re.compile(r"\b(only|all|always|every|any|same|drives|exactly|never|no|each|unique|none|whenever|entire|both)\b",
                   re.I)


def visible_text(raw: str) -> str:
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<(pre|code)[^>]*>.*?</\1>", " ", raw, flags=re.S) if False else raw
    txt = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(txt)


print("== banned strings and ellipses (page text, outside code)")
for p in PAGES:
    raw = (ROOT / f"course/modules/E/E5/{p}.html").read_text(encoding="utf-8")
    body = re.sub(r'<pre><code class="language-python" data-run>.*?</code></pre>', " ", raw, flags=re.S)
    txt = visible_text(body)
    for b in BANNED:
        for m in re.finditer(re.escape(b), txt, flags=re.I):
            print(f"{p}: banned '{b}' at ~{m.start()}: ...{txt[max(0,m.start()-60):m.end()+60]!r}")
    if "..." in txt or "…" in txt:
        print(f"{p}: ellipsis present outside code")
print("banned scan done")

print("== process words (learner text, page text incl. code comments excluded)")
for p in PAGES:
    raw = (ROOT / f"course/modules/E/E5/{p}.html").read_text(encoding="utf-8")
    txt = visible_text(raw)
    for w in PROCESS:
        for m in re.finditer(re.escape(w), txt, flags=re.I):
            print(f"{p}: process word '{w}': ...{txt[max(0,m.start()-50):m.end()+50]!r}")
print("process scan done")

print("== why-it-matters word counts")
for p in PAGES:
    raw = (ROOT / f"course/modules/E/E5/{p}.html").read_text(encoding="utf-8")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, flags=re.S)
    txt = visible_text(m.group(1))
    print(f"{p}: words={len(txt.split())}")

print("== hours")
for p in PAGES:
    raw = (ROOT / f"course/modules/E/E5/{p}.html").read_text(encoding="utf-8")
    print(f"{p}: ", re.search(r'<html[^>]*>', raw).group(0))
idx = (ROOT / "course/modules/E/E5/index.html").read_text(encoding="utf-8")
print("index hours attrs:", re.findall(r'data-hours[^=]*="[^"]*"', idx))

print("== cards: ids, duplicates, scope words (full unit)")
cards = json.loads((ROOT / "course/modules/E/E5/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)))
dups_front = {}
for c in cards:
    key = re.sub(r"\W+", " ", c["front"].lower()).strip()
    dups_front.setdefault(key, []).append(c["id"])
print("duplicate fronts:", {k: v for k, v in dups_front.items() if len(v) > 1})
dups_back = {}
for c in cards:
    key = re.sub(r"\W+", " ", c["back"].lower()).strip()
    dups_back.setdefault(key, []).append(c["id"])
print("duplicate backs:", {k[:40]: v for k, v in dups_back.items() if len(v) > 1})
for c in cards:
    if c["lesson"] in ("L04", "L05", "L06"):
        for m in SCOPE.finditer(c["back"] + " " + c["front"]):
            print(f"card {c['id']} scope word '{m.group(0)}'")
print("cards scope scan done")

print("== notation: symbols used in L04-L06 vs notation.json")
nj = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
print("notation keys:", list(nj.keys()))
syms = nj.get("symbols", [])
print("registered symbols count", len(syms))
for s in syms:
    sym = s.get("symbol") or s.get("tex") or str(s)[:60]
    print("  ", sym, "|", (s.get("meaning") or s.get("description") or "")[:90])
