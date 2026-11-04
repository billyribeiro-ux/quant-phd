"""Round-8 verifier (M3 slice d): consolidated static checks backing several fragment rows.

Covers: project.html relative links and anchors; process and banned words on project.html, cards.json and the grader and
labs; other-module concept names on the project, cards, lessons, grader and labs; notation macros (\\mathbb) and the
registry symbols; deleted identifiers (Definition 1.2a, M3-c208, M3-c204); grade-C / lab-citation consistency.
Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/misc_checks_r8.py
"""

import html
import json
import re
from pathlib import Path

ROOT = Path.cwd()
BASE = ROOT / "course/modules/M/M3"
out = []


def say(msg):
    out.append(msg)
    print(msg)


# 1. project.html links and anchors
page = (BASE / "project.html").read_text(encoding="utf-8")
hrefs = sorted(set(re.findall(r'href="([^"]+)"', page)))
ids_here = set(re.findall(r'id="([^"]+)"', page))
bad = []
for h in hrefs:
    if h.startswith("http"):
        bad.append(("external", h))
        continue
    path, _, frag = h.partition("#")
    target = (BASE / path).resolve() if path else (BASE / "project.html").resolve()
    if path and not target.exists():
        bad.append(("missing file", h))
        continue
    if frag:
        text = ids_here if not path else set(re.findall(r'id="([^"]+)"', target.read_text(encoding="utf-8")))
        if frag not in text:
            bad.append(("missing anchor", h))
say(f"links: {len(hrefs)} href values; problems: {bad or 'none'}")

# 2. banned and process words
BANNED = [r"\bTODO\b", r"\bTBD\b", r"lorem", r"for brevity", r"details omitted", r"beyond the scope",
          r"left as an exercise", r"you can add more", r"it is important to note", r"studies show", r"experts agree",
          r"it is well known", r"\bobviously\b", r"\bclearly\b", r"it can be shown", r"\bbuilder\b", r"\bverifier\b",
          r"\bfixer\b", r"\bround \d", r"\bArchitect\b", r"\bruling\b", r"\bplanner\b", r"\bcampaign\b",
          r"https?://"]
def plain(text):
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)
targets = {
    "project.html": plain(page),
    "cards.json": (BASE / "cards.json").read_text(encoding="utf-8"),
    "grader": "\n".join(p.read_text(encoding="utf-8") for p in (BASE / "grader").glob("*.py")),
    "labs": "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "tests/labs/M3").glob("lab-M3-project-*.py")),
}
hits = {}
for name, text in targets.items():
    for pat in BANNED:
        found = len(re.findall(pat, text, re.I))
        if found:
            hits.setdefault(name, []).append((pat, found))
say(f"banned/process-word hits: {hits or 'none'}")

# 3. other-module concept names (M4, M7, M8, AP2, PR1, S2) by name
OTHER = [r"cholesky", r"ieee", r"minimum.variance", r"mean.variance", r"quadratic programming", r"shrinkage",
         r"equal.weight", r"\bOLS\b", r"present value", r"discount factor", r"random variable", r"expectation"]
other = {}
sources = {"project.html": plain(page), "cards.json": targets["cards.json"], "grader": targets["grader"],
           "labs": targets["labs"]}
for n in range(1, 10):
    sources[f"L{n:02d}.html"] = plain((BASE / f"L{n:02d}.html").read_text(encoding="utf-8"))
for name, text in sources.items():
    for pat in OTHER:
        found = len(re.findall(pat, text, re.I))
        if found:
            other.setdefault(name, []).append((pat, found))
say(f"other-module concept names: {other or 'none'}")

# 4. notation: \mathbb absent from the listed files; registry symbols absent from project math
mathbb = {n: len(re.findall(r"\\mathbb", (BASE / n).read_text(encoding="utf-8")))
          for n in ["project.html", "cards.json", "L07.html", "L08.html", "L09.html"]}
say(f"\\mathbb counts: {mathbb}")
reg = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
reg_syms = [s["symbol"] for s in reg["symbols"]]
math_segments = " ".join(a or b for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", page, re.S))
clash = [s for s in ["T", "\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}"]
         if s in math_segments]
say(f"registry symbols used on project.html math: {clash or 'none'} (registry has {len(reg_syms)} entries)")

# 5. deleted identifiers
cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))
ids = {c["id"] for c in cards}
said = [f for f in list(BASE.glob("*.html")) + [BASE / "cards.json"] if "1.2a" in f.read_text(encoding="utf-8")]
say(f"'1.2a' in M3 pages/cards: {[p.name for p in said] or 'none'}; 'M3-c208' present: {'M3-c208' in ids}; "
    f"'M3-c204' present: {'M3-c204' in ids}; cards: {len(cards)}")
refs_c208 = [p.name for p in BASE.rglob("*") if p.is_file() and p.suffix in {".html", ".json", ".py"}
             and "M3-c208" in p.read_text(encoding="utf-8", errors="ignore")]
say(f"files mentioning M3-c208: {refs_c208 or 'none'}")

# 6. grade and lab-citation consistency
probs = []
for c in cards:
    t = c["front"] + " " + c["back"]
    if re.search(r"\bLab\b", t) and c.get("grade") != "C":
        probs.append(("lab cited, not grade C", c["id"]))
    if c.get("grade") == "C" and not re.search(r"Lab|SIMULATED|seed", t + " " + c.get("basis", "")):
        probs.append(("grade C without lab", c["id"]))
say(f"grade/lab consistency problems: {probs or 'none'}")
