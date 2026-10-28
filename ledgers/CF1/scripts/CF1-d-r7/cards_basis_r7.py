"""Check each CF1 card's basis resolves inside its own lesson. Usage: python -I cards_basis_r7.py <checkout>"""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1], "course/modules/CF/CF1")
cards = json.loads((root / "cards.json").read_text())
html = {p.stem: p.read_text() for p in root.glob("L0*.html")}
ITEM = re.compile(r"(Definition|Theorem|Proposition|Corollary|Example|Remark|Assumption) (\d+)\.(\d+|0)")
bad = 0
for c in cards:
    les = c["lesson"]
    text = html[les]
    basis = str(c.get("basis", "")) + " " + str(c.get("cite", ""))
    problems = []
    for kind, a, b in ITEM.findall(basis):
        label = f"{kind} {a}.{b}"
        m = re.search(r'block-title[^>]*>\s*' + re.escape(label) + r'\b', text)
        if not m:
            problems.append(f"label '{label}' not a block-title in {les}")
            continue
        if kind in ("Theorem", "Proposition", "Corollary"):
            tail = text[m.end():]
            nxt = re.search(r'block-title', tail)
            seg = tail[: nxt.start()] if nxt else tail
            if "Proof" not in seg and "proof" not in seg:
                problems.append(f"no proof block after {label} before next block-title")
    for sec in re.findall(r"proved in Section (\d+)", basis):
        if not re.search(r"(Proposition|Theorem|Corollary) " + sec + r"\.\d", basis):
            problems.append(f"'proved in Section {sec}' with no label of section {sec} in basis")
    for n in re.findall(r"Problem ([RP]\d)", basis):
        if not re.search(r"\b" + n + r"\b", text):
            problems.append(f"Problem {n} not in {les}")
    for sec, which in re.findall(r"Section (\d+), (first|second) misconception", basis):
        sec_text = re.search(r'<section class="misconceptions".*?</section>', text, re.S)
        items = len(re.findall(r'class="misconception"', sec_text.group(0))) if sec_text else 0
        need = 1 if which == "first" else 2
        if items < need:
            problems.append(f"{which} misconception missing in {les} (have {items})")
    for ab in re.findall(r"Lab (\d)", basis):
        if f"lab-CF1-{les}-{ab}" not in text and f"lab-CF1-{les}-" not in text:
            problems.append(f"Lab {ab} not in {les}")
    if problems:
        bad += 1
        print(c["id"], les, c["grade"], repr(basis), problems)
print("cards", len(cards), "cards with unresolved basis", bad)
