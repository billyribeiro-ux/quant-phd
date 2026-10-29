"""Round-10 verifier: every numbered label a card cites must occur in the lesson it cites (same lesson, or the lesson named after 'of Lesson N'/'Lesson LN')."""
import html, json, re, pathlib, sys, subprocess
ROOT = pathlib.Path(sys.argv[1]) / "course/modules/M/M2"
PY = sys.argv[2]
cards = json.load(open(ROOT / "cards.json"))
lab_re = re.compile(r"\b(Theorem|Lemma|Proposition|Example|Corollary|Problem|Remark|Definition|Assumption|Misconception|Section|Lab|Problem [A-Z]\d)\s+([A-Z]?\d+(?:\.\d+)?)")
texts = {}
def text(L):
    if L not in texts:
        texts[L] = subprocess.run([PY, "-I", "/tmp/m2e_r10/txt.py", str(ROOT / f"{L}.html")], capture_output=True, text=True).stdout
    return texts[L]
bad, n = [], 0
for c in cards:
    body = c["front"] + " " + c["back"]
    # cross-lesson references: "Lesson N" or "Lesson LN" or "Lesson L(N)" -> that lesson
    targets = {c["lesson"]}
    for m in re.finditer(r"Lesson\s+L?(\d{1,2})\b", body):
        targets.add(f"L{int(m.group(1)):02d}")
    for m in lab_re.finditer(body):
        label = f"{m.group(1)} {m.group(2)}"
        n += 1
        pat = re.compile(r"(?<![\w.])" + re.escape(label) + r"(?![\d.]\d)")
        if not any(pat.search(text(t)) for t in targets):
            bad.append((c["id"], c["lesson"], label, sorted(targets)))
print("labels checked:", n)
print("unmatched:", len(bad))
for b in bad:
    print("  ", b)
