"""For every card: each cited label (Definition/Proposition/Lemma/Theorem/Remark/Example/Corollary/Problem/Assumption/
Lab/Section/Misconception/Setting) must be printed in the card's own lesson, or in the lesson the card names after 'Lesson N,'."""
import json, re, sys, html
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
texts = {}
for i in range(1, 10):
    raw = (root / f"L0{i}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    texts[f"L0{i}"] = re.sub(r"\s+", " ", t)
LABEL = re.compile(r"(?:Lesson (\d)[, ]+(?:the )?)?\b(Definition|Proposition|Lemma|Theorem|Remark|Example|Corollary|Problem [A-Z]\d|Problem|Assumption|Assumptions|Section|Lab|Misconception|Setting)\b ?([\d.]+|[A-Z]\d)?")
missing = []
checked = 0
for c in cards:
    back = c["back"]
    for m in LABEL.finditer(back):
        lesson = f"L0{m.group(1)}" if m.group(1) else c["lesson"]
        label = (m.group(2) + (" " + m.group(3) if m.group(3) else "")).strip()
        if label in ("Setting",):
            hit = ("the Setting" in texts[lesson]) or ("Setting" in texts[lesson])
        elif label in ("Lab", "Section", "Assumption", "Assumptions", "Misconception", "Problem") and not m.group(3):
            hit = True
        else:
            hit = label in texts[lesson]
        checked += 1
        if not hit:
            missing.append((c["id"], c["lesson"], lesson, label))
print("label citations checked:", checked)
print("citations not printed in the named lesson:", len(missing))
for x in missing: print("  ", x)
