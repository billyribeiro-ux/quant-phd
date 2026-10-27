"""Round 28: classify the 582 round-27 rows of ledgers/S7/L07-L08.json for the round-28 fragment.

Output: JSON list of {id, cls, check, loc}. Classes:
  LAB   lab twin / page code / test rows (re-run this round: compare_labs.py, page_smoke, pytest, mutants)
  FIG   live figure rows (re-run this round: drive_figs.py and the screenshots)
  NUM   numeric or derivation rows (re-derived this round: derive_numbers.py, lab4_independent.py)
  CMD   command and gate rows (re-run this round)
  REG   citation / freshness rows (registry records verified for the cited keys; live re-read of DOIs)
  DATA  data rows (fetch_data --check re-run; snapshot and MANIFEST unchanged)
  BAN   banned-phrase rows (re-scanned this round)
  CARD  flashcard rows (cards read in full this round; numbers re-derived where present)
  CARRY structural, prose and proof rows whose subject is byte-identical and whose claim has no toolchain numerics
"""
import json
import sys
from collections import Counter

rows = json.load(open(sys.argv[1], encoding="utf-8"))["rows"]


def classify(r):
    rid, check, loc = r["id"], r["check"], r["location"]
    if rid.startswith(("r26-drive", "r26-fig-", "r26-mutants-fig")) or check.startswith("2.8-figure"):
        return "FIG"
    if check.startswith(("0-gates", "0-scope")) or rid.startswith(("r27-cmd", "r27-git", "r27-scope")):
        return "CMD"
    if rid.startswith(("r27-banned", "r23-banned", "r19-banned", "L07-banned", "L08-why-it-matters-question")) or check.startswith("2.9-banned"):
        return "BAN"
    if check.startswith("2.8-data") or rid.startswith(("fetch", "data-", "L08-data", "r19-data", "manifest")):
        return "DATA"
    if check.startswith(("2.1-citation", "2.1-freshness")) or rid.startswith(("r26-registry", "registry", "r24-counter", "r24-freshness", "counter-")):
        return "REG"
    if rid.startswith(("card", "cards-")) or check.startswith("2.7-cards"):
        return "CARD"
    if check.startswith("2.5-lab") or rid.startswith(("r24-test", "r25-hunk-test", "r23-mut", "r24-mut", "r26-mutants-lab", "r20-mutants", "mut-", "L08-test", "r21-labs", "L07-twin", "r19-lab4-twin", "L07-lab-", "L08-lab-", "L07-sol", "L08-sol", "L07-L08-mutants", "r27-E4-lab", "r24-diff-hunk", "r25-hunk-test")):
        return "LAB"
    if check.startswith(("2.2-number", "2.4-math", "2.6-derivation")) or rid.startswith(("r19-l521", "r20-l521", "r22-derive", "r23-theorem", "r24-num", "r25-hunk-L07", "r25-fig-quiz", "r27-num", "r27-E4", "r27-math", "r27-hunk", "r24-mut-M06", "r26-hunk", "r26-ex55", "L07-num", "L08-num", "L07-math", "L08-math", "L07-prob", "L08-prob", "L07-E", "L08-E", "L07-R", "L08-R", "L07-shape", "L08-sec7", "L08-lab4", "L07-lab4", "L07-misconception6", "L08-lab3", "L07-R2.9", "L07-kr", "L08-kr", "L07-quiz", "L08-quiz", "L08-lab-4", "L07-lab-4", "L07-sec")):
        return "NUM"
    return "CARRY"


out = [{"id": r["id"], "cls": classify(r), "check": r["check"][:90], "loc": r["location"][:70]} for r in rows]
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(Counter(o["cls"] for o in out))
