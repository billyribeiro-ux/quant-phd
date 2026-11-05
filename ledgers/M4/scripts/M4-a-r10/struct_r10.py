# Round 10: structure, counts and process-word scan for the slice pages and their cards.
import html, json, re, sys
from pathlib import Path
from collections import Counter
root = Path(sys.argv[1])
pages = ["index", "L01", "L02", "L03", "L04"]
proc = re.compile(r"\b(builder|verifier|verification|round|TODO|ledger|fragment|checkout|pin|slice|Architect|ruling)\b", re.I)
for n in pages:
    raw = (root / f"course/modules/M/M4/{n}.html").read_text(encoding="utf-8")
    txt = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)))
    hits = sorted(set(m.group(0).lower() for m in proc.finditer(txt)))
    print(f"{n}: process-word hits in visible text: {hits}")
    if n != "index":
        m = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
        wc = len(html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).split()) if m else None
        print(f"  why-it-matters words: {wc}")
        print(f"  misconception items: {len(re.findall(r'<li class=\"misconception\">', raw))}")
        tiers = re.findall(r'<div class="problem" id="([^"]+)"', raw)
        print(f"  problems: {len(tiers)} ids={tiers}")
        print(f"  quiz items: {len(re.findall(r'<li class=\"item\"', raw))}")
        print(f"  h2 sections: {re.findall(r'<h2 id=\"([^\"]+)\"', raw)}")
        print(f"  data-hours: {re.findall(r'data-hours=\"(\d+)\"', raw)}  eyebrow: {re.findall(r'M4 · Lesson (\d+) of 10 · (\d+) study hours', raw)}")
        print(f"  grade attrs: {Counter(re.findall(r'data-grade=\"([A-DX])\"', raw))}")
        print(f"  dfn ids: {re.findall(r'<dfn id=\"([^\"]+)\"', raw)}")
        print(f"  Definition/Prop/Example/Remark/Problem labels: {re.findall(r'<span class=\"block-title[^\"]*\">(Definition|Proposition|Example|Remark|Assumption) (\d+\.\d+)', raw)}")
cards = json.loads((root / "course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
hits = Counter()
for c in cards:
    for f in ("front", "back"):
        for m in proc.finditer(c[f]):
            hits[(c["id"], m.group(0).lower())] += 1
print("cards process-word hits (all 230):", dict(hits) if hits else "none")
