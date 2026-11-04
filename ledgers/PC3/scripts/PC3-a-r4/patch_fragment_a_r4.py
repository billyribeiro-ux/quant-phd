"""Round-4 verifier: final edits to the PC3 slice-a fragment, then validation with tools/ledger.py.

Run from the checkout root: python -I ledgers/PC3/scripts/PC3-a-r4/patch_fragment_a_r4.py
Sets the evidence pointers to the scripts kept under ledgers/PC3/scripts/PC3-a-r4/, fixes two locations,
recomputes the summary from the rows, and prints the ledger validation result (empty list = valid).
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
FRAG = ROOT / "ledgers/PC3/PC3-a.json"
LINKS = "ledgers/PC3/scripts/PC3-a-r4/outputs/link_and_grep_checks_a_r4.out"
COUNTS = "ledgers/PC3/scripts/PC3-a-r4/outputs/counts_and_scans_a_r4.out"

data = json.loads(FRAG.read_text(encoding="utf-8"))
rows = {r["id"]: r for r in data["rows"]}


def cite(row_id: str, extra: str) -> None:
    rows[row_id]["evidence"] = rows[row_id]["evidence"] + " " + extra


cite("PC3a-check-dag", f"Link and grep script output: {LINKS} (section 'concept links' and 'PC3 dfn tags').")
cite("PC3a-hub-data", f"Script output {LINKS}: 'no hits' for data reads in tests/labs/PC3 and grader; data-files count 0.")
cite("PC3a-hub-P0.1-claim", f"Script output {LINKS}: every concepts.html target maps to M1, M2, M4, CS2, FC2, CF1 or AC1; 'P0.1 targets: []' on all four pages.")
cite("PC3a-notation", f"Script output {LINKS}: registered-symbol grep 'no hits'.")
cite("PC3a-L03-thm-number-3-10", f"Script output {LINKS}: 'Theorem 3.10' and 'adapted' counts 0 on all four pages.")
cite("PC3a-L03-adapted-undefined", f"Script output {LINKS}: 'adapted' count 0 on all four pages.")
cite("PC3a-r4-cross-references", f"Script output {LINKS}: cross-reference counts listed; each reference resolves to an existing item.")
cite("PC3a-r4-restated-M4-concepts", f"Script output {LINKS} shows the M4 dfn tags (M4 L02.html:59, M4 L04.html:139) and the PC3 dfn tags (L02.html:57, 67; L03.html:62).")
cite("PC3a-L03-fair-game-before-definition", f"Counts/scan output {COUNTS}: 'stopping rule' and 'stopping polic' first offsets in L03.")
cite("PC3a-canon-misconceptions-problems-counts", f"Counts output {COUNTS}.")

rows["PC3a-L03-fair-game-before-definition"]["fix"] = (
    "Either move the Definition 3.7 block (L03.html:286-289) above the lab section (before L03.html:107), or, while "
    "Definition 3.7 stays where it is, reword L03.html:104, 108 and 109 so that they do not use 'stopping rule(s)' or "
    "'stopping polic(y/ies)' (for example 'rules that decide when to stop'). The lab code and its twin do not change. "
    "Then re-run check_pages PC3 and page_smoke PC3 --pages L03."
)

rows["PC3a-r4-observations-no-row"]["location"] = (
    "tests/labs/PC3/lab-PC3-L02-1.py:278-280 (typed prior and likelihood); L01.html:431-433 (R1 criterion c); "
    "all three pages (claim-span markup)"
)

summary = Counter(r["status"] for r in data["rows"])
data["summary"] = {
    "rows": len(data["rows"]),
    "pass": summary["PASS"],
    "fail": summary["FAIL"],
    "unverifiable": summary["UNVERIFIABLE"],
}
data["verdict"] = "PASS" if summary["PASS"] == len(data["rows"]) else "FAIL"

FRAG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

sys.path.insert(0, "tools")
import ledger  # noqa: E402

print("summary:", data["summary"], "verdict:", data["verdict"])
print("validate:", ledger.validate(json.loads(FRAG.read_text(encoding="utf-8")), "PC3-a"))
