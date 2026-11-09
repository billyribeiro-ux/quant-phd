"""Verifier J1 (E3 slice e, round 1): token and word checks over the 85b109f8..HEAD delta of the E3 slice paths."""
import re, subprocess, sys
root = sys.argv[1]
paths = ["course/modules/E/E3", "tests/labs/E3", "cards.json", "plans/E3-open-items.md", "plans/FINAL-ARCHITECT-RULINGS.md", "plans/E3-build-plan.md", "references", "tools", "notation"]
diff = subprocess.run(["git", "-C", root, "diff", "-U0", "85b109f8..HEAD", "--", *paths], capture_output=True, text=True, check=True).stdout
removed, added = [], []
for line in diff.splitlines():
    if line.startswith("---") or line.startswith("+++"):
        continue
    if line.startswith("-"):
        removed.append(line[1:])
    elif line.startswith("+"):
        added.append(line[1:])
print(f"removed lines {len(removed)} added lines {len(added)}")
num = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")
rn = sorted(t for l in removed for t in num.findall(l))
an = sorted(t for l in added for t in num.findall(l))
print("numeric tokens removed:", rn)
print("numeric tokens added:  ", an)
scope = re.compile(r"\b(only|all|every|always|exactly|any|same|drives|never|none)\b", re.I)
proc = re.compile(r"\b(verifier|fixer|ruling|round|pin|delta|ledger|builder|slice|audit|architect|rubric|checker|previous|todo|placeholder|batch|reviewer|agent)\b", re.I)
rhet = re.compile(r"\b(crucial|notably|importantly|clearly|obviously|simply|just|very|really|powerful|elegant)\b", re.I)
for l in added:
    for name, rx in (("scope", scope), ("process", proc), ("rhetoric", rhet)):
        for m in rx.finditer(l):
            print(f"HIT {name}: {m.group(0)!r} in: {l[:140]}")
print("added text:")
for l in added:
    print("  +", l)
