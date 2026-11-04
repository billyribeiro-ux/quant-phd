"""Round-7 verifier (slice d): static checks on the project page, cards and lessons, with the output written to
out/static_checks_r7.out. Covers: card grades and bases; card id and text duplicates; the orthogonal-matrix overlap of
M3-c208 with M3-c101 and M3-c205; process words; \\mathbb uses; out-of-closure concept names; concept links on the
project page; and the Lab 2 page code against its twin (the only differences must be the two blanks)."""

import difflib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
MOD = ROOT / "course/modules/M/M3"
out = []


def say(s: str) -> None:
    out.append(s)
    print(s)


cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
say(f"cards: {len(cards)}; unique ids {len({c['id'] for c in cards})}")
ids = [c["id"] for c in cards]
front_count = {f: sum(1 for x in cards if x["front"] == f) for f in {x["front"] for x in cards}}
back_count = {b: sum(1 for x in cards if x["back"] == b) for b in {x["back"] for x in cards}}
say("duplicate fronts: " + str([f for f, n in front_count.items() if n > 1]))
say("duplicate backs: " + str([b for b, n in back_count.items() if n > 1]))
grades: dict[str, int] = {}
for c in cards:
    grades[str(c.get("grade"))] = grades.get(str(c.get("grade")), 0) + 1
say(f"grades: {grades}")
say("grade C without a Lab in basis: " + str([c["id"] for c in cards if c.get("grade") == "C" and "Lab" not in c.get("basis", "")]))
say("non-C cards with a basis: " + str([c["id"] for c in cards if c.get("grade") != "C" and "basis" in c]))
STOP = {"the", "a", "an", "of", "is", "to", "and", "in", "for", "that", "with", "it", "by", "as", "on", "or", "be", "this",
        "not", "are", "true", "false", "from", "does", "do", "what", "which", "when", "if", "its", "each", "at", "than"}


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP}


by = {c["id"]: c for c in cards}
c208 = words(by["M3-c208"]["front"] + " " + by["M3-c208"]["back"])
for k in ("M3-c101", "M3-c205", "M3-c067"):
    o = words(by[k]["front"] + " " + by[k]["back"])
    say(f"Jaccard M3-c208 vs {k}: {len(c208 & o) / len(c208 | o):.2f}")
say("M3-c208 back: " + by["M3-c208"]["back"])
say("M3-c101 back: " + by["M3-c101"]["back"])
say("M3-c205 back: " + by["M3-c205"]["back"])

proc = re.compile(r"\b(round|verif\w*|fixer|builder|architect|ruling|revised|corrected|updated|blind|placeholder|TODO|TBD)\b", re.I)
for f in [MOD / "project.html", MOD / "cards.json", *sorted((MOD / "grader").glob("*.py")),
          *sorted((ROOT / "tests/labs/M3").glob("lab-M3-project-*.py"))]:
    hits = [m.group(0) for m in proc.finditer(f.read_text(encoding="utf-8"))]
    say(f"process words in {f.relative_to(ROOT)}: {hits}")
for f in [MOD / "project.html", MOD / "cards.json", *sorted(MOD.glob("L0*.html"))]:
    say(f"mathbb in {f.relative_to(ROOT)}: {f.read_text(encoding='utf-8').count('mathbb')}")
conc = re.compile(r"cholesky|ieee|minimum.variance|mean.variance|quadratic programming|equal.weight", re.I)
for f in [MOD / "project.html", MOD / "cards.json", *sorted(MOD.glob("L0*.html"))]:
    say(f"out-of-closure concept names in {f.name}: {len(conc.findall(f.read_text(encoding='utf-8')))}")
say("concept links on project.html: " + str(re.findall(r'data-concept="([a-z0-9-]+)"', (MOD / "project.html").read_text(encoding="utf-8"))))

page = (MOD / "project.html").read_text(encoding="utf-8")
m = re.search(r'<section class="lab completion" id="lab-M3-project-2".*?<pre><code[^>]*data-run>(.*?)</code></pre>', page, re.S)
code = html.unescape(m.group(1)).rstrip("\n")
twin = (ROOT / "tests/labs/M3/lab-M3-project-2.py").read_text(encoding="utf-8").rstrip("\n")
diff = [l for l in difflib.unified_diff(code.splitlines(), twin.splitlines(), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("---", "+++")]
say("Lab 2 page code vs twin, differing lines:")
for l in diff:
    say("  " + l)

# notation: symbols used in TeX on the project page, against notation/notation.json
registry = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
reg_symbols = [s["symbol"] for s in registry["symbols"]]
say("registered symbols: " + str(reg_symbols))
maths = re.findall(r"\\\((.+?)\\\)", page, flags=re.S) + re.findall(r"\\\[(.+?)\\\]", page, flags=re.S)
letters: set[str] = set()
for mth in maths:
    stripped = re.sub(r"\\[A-Za-z]+", "", mth)
    letters |= set(re.findall(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])", stripped))
say(f"math spans on project.html: {len(maths)}; single Latin letters used: {''.join(sorted(letters))}")
say("registered symbols used on project.html (T, Phi, gamma3, gamma4, R*, R^e*, Rf, Q): " +
    str([s for s in ("T", "Q", "R_f", "\\Phi", "\\gamma_3") if any(re.search(r"(?<![A-Za-z\\])" + re.escape(s) + r"(?![A-Za-z])", mth) for mth in maths)]))
say("macros used on project.html: " + str(sorted({t for mth in maths for t in re.findall(r"\\[A-Za-z]+", mth)})))
