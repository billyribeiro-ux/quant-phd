"""Round-9: every card's cross-references (Definition/Proposition/Theorem/Lemma/Corollary/Remark/Problem/Example/
Assumption/Section/Misconception/Lab) must name a label that occurs in the card's own lesson text, and every number
other than 0, 1, 2 on a grade-C card must occur in that lesson's twin output (ledgers/CS2/scripts/CS2-d-r9/twins)."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOD = ROOT / "course" / "modules" / "CS" / "CS2"
TWIN = ROOT / "ledgers" / "CS2" / "scripts" / "CS2-d-r9" / "twins"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))


def text_of(path: Path) -> str:
    src = path.read_text(encoding="utf-8")
    src = re.sub(r"<script.*?</script>", "", src, flags=re.S)
    src = re.sub(r"<[^>]+>", " ", src)
    return re.sub(r"\s+", " ", html.unescape(src))


lessons = {f"L{i:02d}": text_of(MOD / f"L{i:02d}.html") for i in range(1, 12)}
twin_lesson = {}
for lid in lessons:
    outs = sorted(TWIN.glob(f"lab-CS2-{lid}-1.out"))
    twin_lesson[lid] = outs[0].read_text(encoding="utf-8") if outs else ""
ref_re = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Problem|Example|Assumption|Misconception|Section)\s+(\d+(?:\.\d+)?)(\([a-z]\))?")
unresolved = []
num_missing = []
checked_refs = 0
for c in cards:
    t = lessons[c["lesson"]]
    s = c["front"] + " " + c["back"]
    for m in ref_re.finditer(s):
        kind, num = m.group(1), m.group(2)
        checked_refs += 1
        # the label as the lesson writes it: "Kind num" followed by a non-digit character
        pat = re.compile(rf"\b{kind}\s+{re.escape(num)}(?![\d.])")
        if not pat.search(t):
            unresolved.append((c["id"], f"{kind} {num}"))
    if c["grade"] == "C":
        out = twin_lesson[c["lesson"]]
        for field in ("front", "back"):
            for num in set(re.findall(r"(?<![A-Za-z_\d.])\d+(?:\.\d+)?", c[field])):
                if num in ("0", "1", "2"):
                    continue
                if num not in out:
                    num_missing.append((c["id"], field, num))
print("cross-references checked:", checked_refs)
print("cross-references not found as labels in own lesson text:", unresolved)
print("C-card numbers (other than 0,1,2) not in own twin output:", num_missing)
