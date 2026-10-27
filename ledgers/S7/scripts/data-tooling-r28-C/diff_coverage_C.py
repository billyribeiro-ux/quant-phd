"""Round-28 part C: coverage of the 5e5da87..c9beb92 non-ledger delta by the data-tooling part fragments A, B, C.
A changed file counts as covered when its repository path appears in the location or evidence of some row of
ledgers/S7/data-tooling-{A,B,C}.json (a directory-level path counts when a file beneath it is named).
Run: python -I diff_coverage_C.py <checkout>"""
import json
import subprocess
import sys

CK = sys.argv[1]
files = subprocess.run(["git", "-C", CK, "diff", "--name-only", "5e5da87", "c9beb92"], capture_output=True, text=True, check=True).stdout.split()
files = [f for f in files if not f.startswith("ledgers/")]
text = ""
for part in "ABC":
    d = json.load(open(f"{CK}/ledgers/S7/data-tooling-{part}.json", encoding="utf-8"))
    for r in d["rows"]:
        if r["id"] in ("R26-diff-coverage", "r25-diff-scope"):
            continue  # the coverage rows themselves name files; they are not evidence of coverage
        text += " " + r["location"] + " " + r["evidence"] + " " + r["id"]
uncovered = []
for f in files:
    if f in text:
        continue
    base = f.rsplit("/", 1)[-1]
    stem = base.rsplit(".", 1)[0]
    if base in text or (stem and f"{stem}." in text):
        continue
    uncovered.append(f)
print(f"(rows R26-diff-coverage and r25-diff-scope excluded: they name the files they report)")
print(f"non-ledger files changed 5e5da87..c9beb92: {len(files)}")
print(f"named by a row of parts A/B/C (path or basename): {len(files) - len(uncovered)}")
print("not named:", uncovered)
