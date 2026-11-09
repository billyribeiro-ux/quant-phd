"""Mechanical carry test for the round-13 rows: a row is carried only if no line it cites was changed since e919577.

Changed lines come from `git diff -U0 e919577 8e5751c` (project.html 407, 432, 696; plan 420-423 and 430-432;
L04.html 65, 72, 83; L06.html 154, 397, 411). A row that cites a file with no line number, or a changed file name
without a line number, is not carried. Output: the row ids that may be carried, and the ids that need fresh evidence.
"""
import json
import re
import sys

ROWS = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-c.round13.json"))["rows"]
CHANGED = {
    "project.html": set([407, 432, 696]),
    "PC3-build-plan.md": set(range(420, 424)) | set(range(430, 433)),
    "L04.html": set([65, 72, 83]),
    "L06.html": set([154, 397, 411]),
}
CHANGED_NONLINE = {"cards.json"}  # any citation of cards.json is not carried


def cited_numbers(text):
    nums = set()
    for a, b in re.findall(r"(\d+)\s*(?:-|–)\s*(\d+)", text):
        nums |= set(range(int(a), int(b) + 1))
    for n in re.findall(r"(?<![\w.])(\d+)(?![\w.])", text):
        nums.add(int(n))
    return nums


def decide(row):
    loc = row["location"]
    reasons = []
    for fname, lines in CHANGED.items():
        if fname in loc:
            if "whole page" in loc or "(whole" in loc:
                reasons.append(f"{fname} cited as whole")
            hits = cited_numbers(loc) & lines
            if hits:
                reasons.append(f"{fname} line(s) {sorted(hits)} changed")
            if fname in loc and not cited_numbers(loc):
                reasons.append(f"{fname} cited without lines")
    for fname in CHANGED_NONLINE:
        if fname in loc:
            reasons.append(f"{fname} changed")
    return reasons


carry, fresh = [], []
for row in ROWS:
    reasons = decide(row)
    (fresh if reasons else carry).append((row["id"], row["status"], reasons))
json.dump({"carry": [c[0] for c in carry], "fresh": [f[0] for f in fresh], "fresh_reasons": {f[0]: f[2] for f in fresh}},
          open(sys.argv[1], "w"), indent=1)
print("carry", len(carry), "fresh", len(fresh))
for f in fresh:
    print("  FRESH", f[0], f[1], f[2])
