"""Quick checks run by the round-5 verifier (checkout root as cwd). Prints each result; exit 0 always."""
import html
import json
import os
import re
from pathlib import Path

M2 = Path("course/modules/M/M2")
page = (M2 / "project.html").read_text(encoding="utf-8")

print("== 1. project.html link targets")
ids = set(re.findall(r'id="([^"]+)"', page))
bad = []
links = re.findall(r'href="([^"]+)"', page)
for l in links:
    if l.startswith("#"):
        if l[1:] not in ids:
            bad.append(l)
        continue
    f, _, frag = l.partition("#")
    if f and not (M2 / f).exists():
        bad.append(l)
        continue
    if frag and f:
        if f'id="{frag}"' not in (M2 / f).read_text(encoding="utf-8"):
            bad.append(l)
print("links", len(links), "bad", bad)

print("== 2. banned phrases and process words in project.html text and cards")
text = re.sub(r"<script.*?</script>", "", page, flags=re.S)
text = html.unescape(re.sub(r"<[^>]+>", " ", text))
banned = ["roughly half", "about 6%", "historically", "studies show", "well known", "important to note",
          "beyond the scope", "left as an exercise", "typically", "in practice", "TODO", "TBD", "lorem",
          "for brevity", "roughly", "build", "builder", "verifier", "unit report"]
for w in banned:
    n = len(re.findall(re.escape(w), text, flags=re.I))
    if n:
        print("  hit", repr(w), n)
cards = json.loads((M2 / "cards.json").read_text(encoding="utf-8"))
ctext = " ".join(c["front"] + " " + c["back"] for c in cards)
for w in banned:
    n = len(re.findall(re.escape(w), ctext, flags=re.I))
    if n:
        print("  cards hit", repr(w), n)
print("  (no line above means no hit)")

print("== 3. scope words, sentence list for project.html")
sents = re.split(r"(?<=[.;])\s+", text)
for s in sents:
    if re.search(r"\b(only|all|always|every|any|same|drives)\b", s, flags=re.I):
        print("  *", s.strip()[:140])

print("== 4. hours")
print("  hub:", re.findall(r'data-hours-[a-z]+="\d+"', (M2 / "index.html").read_text(encoding="utf-8")))
lh = [int(re.search(r"(\d+) study hours", (M2 / f"L{i:02d}.html").read_text(encoding="utf-8")).group(1)) for i in range(1, 25)]
print("  lesson study hours sum", sum(lh), "count", len(lh))
rows = [4, 6, 22, 6, 14, 8]
print("  project table sum", sum(rows))

print("== 5. cards")
ids_all = [c["id"] for c in cards]
print("  cards", len(cards), "unique ids", len(set(ids_all)) == len(ids_all))
nums = [int(i.split("c")[-1]) for i in ids_all]
print("  missing numbers in 1..max:", sorted(set(range(1, max(nums) + 1)) - set(nums)))
print("  grade C without basis:", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("  basis on non-C:", [c["id"] for c in cards if c.get("basis") and c.get("grade") != "C"])
print("  cards per lesson:", {l: sum(1 for c in cards if c["lesson"] == l) for l in sorted({c["lesson"] for c in cards})})

print("== 6. decimal and exponent tokens on cards that are absent from their lesson text")
lesson_txt = {}
for c in cards:
    L = c["lesson"]
    if L not in lesson_txt:
        raw = (M2 / f"{L}.html").read_text(encoding="utf-8")
        raw = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
        lesson_txt[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
miss = []
for c in cards:
    for tok in set(re.findall(r"\b\d+\.\d+(?:e-?\d+)?\b|\b\d+e-\d+\b", c["front"] + " " + c["back"])):
        if tok not in lesson_txt[c["lesson"]]:
            miss.append((c["id"], tok))
print("  tokens not found in lesson html:", miss if miss else "none")

print("== 7. instance distinctness over seeds 0-49")
import sys
sys.path.insert(0, "course/modules/M/M2/grader")
from instance import make_instance  # noqa: E402
ins = [make_instance(s) for s in range(50)]
print("  distinct instances:", len({(i["face_cents"], i["coupon_bps"], i["maturity_years"], i["yield_bps"]) for i in ins}))
