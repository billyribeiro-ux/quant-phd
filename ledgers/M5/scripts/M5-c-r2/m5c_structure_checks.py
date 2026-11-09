"""Round-2 structure, prose, card and cross-reference checks for M5 slice c (L08-L10 and their cards)."""
import difflib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
M5 = ROOT / "course/modules/M/M5"
out = []


def say(s):
    out.append(s)
    print(s)


pages = {}
for lid in ("L08", "L09", "L10"):
    t = (M5 / f"{lid}.html").read_text(encoding="utf-8")
    pages[lid] = t
    body = re.sub(r"<pre.*?</pre>", "", t, flags=re.S)
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
              "you can add more", "it is important to note", "studies show", "experts agree", "well known",
              "obviously", "clearly", "roughly", "historically", "…", "&hellip;", "stock"]
    hits = [b for b in banned if b.lower() in text.lower()]
    say(f"{lid} banned-string hits in prose: {hits}")
    proc = [w for w in ["builder", "verifier", "round", "ledger", "fragment", "checkout", "agent", "placeholder"] if w in text.lower()]
    say(f"{lid} process-word hits: {proc}")
    tags = set(re.findall(r"<\s*([A-Za-z][A-Za-z0-9]*)", re.sub(r"<pre.*?</pre>", "", t, flags=re.S)))
    vocab = set("a abbr b body br button c code dd details dfn div dl dt em fieldset footer h1 h2 h3 head header hr html i input label legend li link main meta nav ol p pre s section small span strong style summary sup sub svg table tbody td tfoot th thead title tr ul script g path rect text circle line polyline polygon desc use defs".split())
    say(f"{lid} non-vocabulary start tags: {sorted(x for x in tags if x.lower() not in vocab)}")
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    say(f"{lid} why-it-matters words: {len(html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1))).split())} (limit 120)")
    items = re.findall(r'<li class="item" data-kind="(\w+)"(.*?)</li>', t, re.S)
    mc_bad = [i for i, (k, blk) in enumerate(items) if k == "mc" and blk.count("data-correct") != 1]
    say(f"{lid} quiz items {len(items)} (8-15), mc items without exactly one data-correct: {mc_bad}")
    say(f"{lid} footer present: {'Every claim carries an evidence grade and a registry citation' in t}; page says 'cites no source': {'cites no source' in t}")
    say(f"{lid} problem counts per tier: {[(n, len(re.findall(r'class=\"problem\"', b))) for n, b in re.findall(r'<div class=\"tier\" data-tier=\"(\\w+)\">(.*?)<h3>', t, re.S)] and ''}")
    say(f"{lid} problems total: {len(re.findall(r'class=\"problem\"', t))}")
    lesson_nav = re.search(r'<nav class="lesson-nav".*?</nav>', t, re.S).group(0)
    say(f"{lid} nav text: {html.unescape(re.sub(r'<[^>]+>', ' ', lesson_nav)).split()}")

h1 = {lid: html.unescape(re.search(r"<h1>(.*?)</h1>", pages[lid]).group(1)) for lid in pages}
say(f"h1: {h1}")

l07 = (M5 / "L07.html").read_text(encoding="utf-8")
i07 = l07.find("Theorem 2.1 <span")
say("L07 Theorem 2.1 hypotheses mention nonempty: " + str("nonempty" in l07[i07: i07 + 400]))

idx = (M5 / "index.html").read_text(encoding="utf-8")
say("hub data-hours-lessons/project: " + str(re.findall(r'data-hours-(?:lessons|project)="(\d+)"', idx)))
say("lesson data-hours L08/L09/L10: " + str([re.search(r'data-hours="(\d+)"', pages[l]).group(1) for l in pages]))

cards = json.loads((M5 / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
say(f"cards total {len(cards)}, ids unique {len(ids) == len(set(ids))}")
slice_cards = [c for c in cards if c["lesson"] in ("L08", "L09", "L10")]
say(f"slice cards: {len(slice_cards)} (L08 {sum(c['lesson']=='L08' for c in slice_cards)}, L09 {sum(c['lesson']=='L09' for c in slice_cards)}, L10 {sum(c['lesson']=='L10' for c in slice_cards)})")
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
near = []
for i, a in enumerate(slice_cards):
    for b in slice_cards[i + 1:]:
        r = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        if r > 0.8:
            near.append((round(r, 2), a["id"], b["id"]))
say(f"slice card fronts with similarity > 0.8: {near}")
allb = [norm(c["back"]) for c in cards]
say(f"identical backs across all cards: {len(allb) - len(set(allb))}")
missing = []
for c in slice_cards:
    for num in re.findall(r"\b\d+\.\d+(?:e[-+]?\d+)?\b|\b\d{2,}\b", c["front"] + " " + c["back"]):
        if num not in pages[c["lesson"]]:
            missing.append((c["id"], num))
say(f"card numbers not found verbatim in their lesson: {missing}")
(ROOT / "ledgers/M5/scripts/M5-c-r2/out").mkdir(parents=True, exist_ok=True)
(ROOT / "ledgers/M5/scripts/M5-c-r2/out/structure_checks.out").write_text("\n".join(out) + "\n", encoding="utf-8")
