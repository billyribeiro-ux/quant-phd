"""Round 13 (M7-d): re-checks the fraction tokens that cards_numbers_r13.py reported absent, after normalising TeX
fractions (\\frac, \\tfrac, with or without braces) in the card's own lesson to N/D form."""
import html, json, pathlib, re
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB13-M7-d")
MOD = ROOT / "course/modules/M/M7"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
frac = re.compile(r"\\t?frac\s*\{?\s*(\d+)\s*\}?\s*\{?\s*(\d+)\s*\}?")
missing = []
cache = {}
for c in cards:
    lesson = c["lesson"]
    if lesson not in cache:
        raw = (MOD / f"{lesson}.html").read_text(encoding="utf-8")
        raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
        txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        txt = frac.sub(lambda m: f"{m.group(1)}/{m.group(2)}", txt)
        cache[lesson] = re.sub(r"\s+", " ", txt)
    for tok in set(re.findall(r"(?<![A-Za-z_])-?\d+/\d+", c["back"])):
        t = tok.lstrip("-")
        if t not in cache[lesson]:
            missing.append((c["id"], lesson, tok))
print("fraction tokens absent after TeX normalisation:", len(missing))
for m in missing:
    print(*m)
