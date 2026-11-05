"""Round-10 structure, notation, process-word, concept and card scans for E4 L04 to L06 (stdlib plus json only).

Run from the checkout root: python -I ledgers/E4/scripts/E4-b-r10/structure_scan_r10.py
"""

import collections
import html
import itertools
import json
import re

PAGES = ("L04", "L05", "L06")
BANNED = re.compile(
    r"\b(builder|verifier|verification|round|fragment|ledger|twin|architect|plan|mutant|REQUEST|registry|TODO|TBD|"
    r"lorem|obviously|clearly|studies show|experts agree|well known|for brevity|beyond the scope|left as an exercise|"
    r"it is important to note|details omitted|you can add more)\b",
    re.I,
)
TAG = re.compile(r"</?[a-zA-Z][a-zA-Z0-9]*(\s[^>]*)?/?>")
print("== why-it-matters words (<=120), solution word counts (>=15), section and quiz counts")
for t in PAGES:
    txt = open(f"course/modules/E/E4/{t}.html", encoding="utf-8").read()
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', txt, re.S).group(1)
    why_words = len(html.unescape(TAG.sub("", why)).split())
    sols = re.findall(r'<details class="solution">(.*?)</details>', txt, re.S)
    sol_words = [len(html.unescape(TAG.sub(" ", s)).split()) for s in sols]
    quiz = len(re.findall(r'<div class="question"|<fieldset', txt))
    misc = len(re.findall(r'class="misconception"|<h3[^>]*>[^<]*Misconception', txt))
    print(f"{t} why_words={why_words} solutions={len(sols)} min_solution_words={min(sol_words)} "
          f"quiz_like_blocks={quiz}")
print("== visible-text banned or process words (expected: none)")
for t in PAGES:
    txt = open(f"course/modules/E/E4/{t}.html", encoding="utf-8").read()
    body = re.sub(r"<script.*?</script>|<style.*?</style>", "", txt, flags=re.S)
    body = re.sub(r'<pre class="expected".*?</pre>|<code class="language-python" data-run>.*?</code>', "", body, flags=re.S)
    vis = html.unescape(TAG.sub(" ", body))
    print(t, "hits", [m.group(0) for m in BANNED.finditer(vis)], "ellipsis", len(re.findall(r"\.\.\.", vis)))
print("== math macros used in L04 to L06 pages, against notation.json and the plan forbidden list")
nota = json.load(open("notation/notation.json", encoding="utf-8"))
registered = set(nota["macros"].keys())
for t in PAGES:
    txt = open(f"course/modules/E/E4/{t}.html", encoding="utf-8").read()
    maths = [a or b for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", txt, re.S)]
    s = " ".join(maths)
    used = collections.Counter(re.findall(r"\\([a-zA-Z]+)", s))
    reg_used = sorted(m for m in used if "\\" + m in registered)
    print(t, "registered macros used:", reg_used, "| mathbb uses:", s.count("\\mathbb"),
          "| \\Phi, \\gamma, \\ast-after-R, R_f, \\mathbb{Q}:", len(re.findall(r"\\Phi|\\gamma|R\^\{?\\ast|R_f|\\mathbb\{Q\}", s)))
print("== card id uniqueness and near-duplicate fronts (slice cards)")
cards = json.load(open("course/modules/E/E4/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "duplicate ids", [i for i, n in collections.Counter(ids).items() if n > 1])
slice_cards = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
STOP = {"the", "a", "an", "of", "in", "is", "what", "under", "assume", "and", "to", "for", "with", "at", "does", "do",
        "how", "which", "are", "be", "it", "that", "this", "from", "on", "by", "or", "if", "when", "whether", "c",
        "assuming", "lab", "part", "l04", "l05", "l06", "1", "2", "3"}


def toks(x: str) -> set[str]:
    return set(re.findall(r"[a-zA-Zα-ωΑ-Ω]+", x.lower())) - STOP


for a, b in itertools.combinations(slice_cards, 2):
    ta, tb = toks(a["front"]), toks(b["front"])
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.55:
        print(f"front-overlap {j:.2f} {a['id']} {b['id']} | {a['front'][:80]} || {b['front'][:80]}")
print("== dump of the L04 to L06 cards (outputs/cards_L04_L06.txt)")
with open("ledgers/E4/scripts/E4-b-r10/outputs/cards_L04_L06.txt", "w", encoding="utf-8") as fh:
    for c in slice_cards:
        fh.write(f"{c['id']} {c['lesson']} |F: {c['front']} |B: {c['back']} |G: {c.get('grade')} "
                 f"|Bas: {c.get('basis')} |cite: {c.get('cite')}\n")
print("dumped", len(slice_cards), "cards")
