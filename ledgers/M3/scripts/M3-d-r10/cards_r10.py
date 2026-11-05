"""Round-10 verifier (M3 slice d): card structure, ids, grade/basis, numbers on each card vs its lesson text and
lab twin output, cited labels vs lesson HTML, and a full pairwise duplicate scan (token Jaccard). Run from the root."""

import html
import json
import re
import subprocess
import sys
from itertools import combinations

cards = json.load(open("course/modules/M/M3/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)) == len(ids))
keys = {tuple(sorted(c.keys())) for c in cards}
print("key sets:", keys)
bad_grade = [c["id"] for c in cards if "grade" in c and c["grade"] not in ("T", "C")]
no_basis_c = [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")]
t_with_lab = [
    c["id"]
    for c in cards
    if c.get("grade") == "T" and re.search(r"lab|SIMULATED|seed", c["back"] + c["front"], re.I)
]
print("grade values bad:", bad_grade, "| C without basis:", no_basis_c)
print("T cards mentioning lab/SIMULATED/seed:", t_with_lab)
print("grade counts:", {g: sum(1 for c in cards if c.get("grade") == g) for g in ("T", "C", None)})

# lesson text (visible text) and twin outputs
texts = {}
for L in sorted({c["lesson"] for c in cards}):
    raw = open(f"course/modules/M/M3/{L}.html", encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    texts[L] = html.unescape(re.sub(r"<[^>]+>", " ", body))
twin_out = {}
for n in range(1, 10):
    L = f"L0{n}"
    p = f"tests/labs/M3/lab-M3-{L}-1.py"
    res = subprocess.run([sys.executable, "-I", "-W", "error", p], capture_output=True, text=True)
    twin_out[L] = res.stdout
    if res.returncode:
        print("twin failed", p, res.stderr[:200])

num_re = re.compile(r"(?<![A-Za-z_])-?\d+(?:\.\d+)?(?:e-?\d+)?")
misses = []
for c in cards:
    text_all = c["front"] + " " + c["back"]
    for num in set(num_re.findall(text_all)):
        n = num.lstrip("-")
        if n in ("1", "0", "2", "3", "4"):
            continue
        L = c["lesson"]
        if n in texts[L] or n in twin_out[L] or any(n in texts[x] for x in texts):
            continue
        misses.append((c["id"], num))
print("numbers on cards not found in any read M3 lesson text or twin output:", misses)

# citations: 'Definition 1.1', 'Proposition 2.3', 'Remark 1.4', 'Example 3.6', 'Theorem 2.2', 'Lemma 1.3', 'Corollary 3.6', 'Fact 1.2'
cite_re = re.compile(r"\b(Definition|Proposition|Remark|Example|Theorem|Lemma|Corollary|Fact)s? (\d+\.\d+)")
missing_cites = []
for c in cards:
    L = c["lesson"]
    for kind, num in set(cite_re.findall(c["front"] + " " + c["back"])):
        label = f"{kind} {num}"
        if label not in texts[L]:
            missing_cites.append((c["id"], L, label))
print("citations not found in the card's own lesson text:", missing_cites)

# duplicate scan
def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))
pairs = []
T = {c["id"]: toks(c["front"] + " " + c["back"]) for c in cards}
for a, b in combinations(cards, 2):
    ta, tb = T[a["id"]], T[b["id"]]
    j = len(ta & tb) / max(1, len(ta | tb))
    pairs.append((j, a["id"], b["id"]))
pairs.sort(reverse=True)
print("pairs scanned:", len(pairs))
print("top 8 pairs by Jaccard:")
for j, x, y in pairs[:8]:
    print(f"  {j:.3f} {x} {y}")
exact = [(a["id"], b["id"]) for a, b in combinations(cards, 2) if a["front"] == b["front"] or a["back"] == b["back"]]
print("exact duplicate fronts or backs:", exact)
print("id gaps:", sorted(set(f"M3-c{n:03d}" for n in range(1, 208)) - set(ids)))
