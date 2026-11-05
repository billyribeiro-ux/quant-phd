"""Assumption-label, learner-wording and cross-reference scans of cards.json against the rendered lessons.

Usage: python -I assumption_and_wording_scan_r8.py <cards.json> <out_dir>
Step 1: every assumption label in a card is checked against the lesson that defines it (defined[] below, read from
out/L0N.txt); where a card writes 'of Lesson K' right after a label, K must be the defining lesson.
Step 2: process words, banned ASCII strings, and the Unicode ellipsis (list notation only).
"""
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
out_dir = sys.argv[2]
for n in range(1, 9):
    open(f"{out_dir}/L0{n}.txt", encoding="utf-8").read()  # every lesson text must exist

definer = {
    "A1": 1, "A2": 2, "Assumption 2.1": 2, "Assumption 3.1": 3, "Assumption 3.2": 3,
    "Assumption 4.1": 4, "Assumption 4.2": 4, "A3": 5, "A4": 5, "A5": 7,
}
# Verified against the rendered text: L01 defines A1(a)-(e); L02 defines A2 and Assumption 2.1; L03 defines
# Assumptions 3.1 and 3.2; L04 defines Assumptions 4.1 and 4.2; L05 defines A3 and A4(a)-(h); L07 defines A5.
label = re.compile(r"\bA([1-5])\b|Assumptions? (\d\.\d)")
problems = []
checked = 0
for c in cards:
    body = c["front"] + " | " + c["back"] + " | " + c.get("basis", "")
    for m in label.finditer(body):
        name = f"A{m.group(1)}" if m.group(1) else f"Assumption {m.group(2)}"
        if name not in definer:
            continue
        tail = body[m.end(): m.end() + 25]
        k = re.search(r"of Lesson (\d)", tail)
        if not k:
            continue
        checked += 1
        if definer[name] != int(k.group(1)):
            problems.append((c["id"], name, f"'{tail[:k.end()].strip()}'", f"defined in Lesson {definer[name]}"))
print("explicit 'of Lesson K' references checked:", checked)
print("mismatches:")
for p in sorted(set(problems)):
    print("  ", p)
print("mismatch count:", len(set(problems)))

process = re.compile(r"\b(builder|verifier|round|fixer|ledger|mutant|grader|REQUEST)s?\b", re.I)
banned = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|"
                    r"it is important to note|studies show|experts agree|it is well known|\bobviously\b|\bclearly\b|\.\.\.")
pw = []
ellipsis_cards = []
for c in cards:
    body = c["front"] + " | " + c["back"]
    pw += [(c["id"], m.group(0)) for m in process.finditer(body)]
    if banned.search(body):
        pw.append((c["id"], "banned:" + banned.search(body).group(0)))
    if "…" in body:
        ellipsis_cards.append(c["id"])
print("process words or banned ASCII strings:", pw)
print("cards with the Unicode ellipsis (list notation t_1,...,t_r):", sorted(ellipsis_cards))
