"""Verifier CS2-d round 4: writes ledgers/CS2/CS2-d.json from the round 4 verification rows.

Usage: python -I build_fragment_r4.py <checkout>
The mutants list is parsed from out/mutate_0-49_r2.txt (tools/mutate_graders.py --unit CS2 --seeds 0-49). The one
surviving mutant, d4_03_mean_is_running_sum_over_count.py, is an alternative correct implementation and is left out.
"""

import json
import re
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
out_dir = checkout / "ledgers/CS2/scripts/CS2-d-r4/out"
rows = json.loads((Path(__file__).parent / "rows_r4.json").read_text(encoding="utf-8"))

mutants = []
for line in (out_dir / "mutate_0-49_r2.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+?): (.*) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})

fragment = {
    "unit": "CS2",
    "slice": "CS2-d",
    "round": 4,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 4; did not build CS2; no shared context with builders)",
    "pin": "2657ab5 (detached checkout /tmp/verifyB4-CS2-d)",
    "base": "aa3c26c (round 3 pin). Delta since aa3c26c in the slice: project.html (hunks at 202, 208-211, 378-390), grader/reference.py (docstring), grader/test_project.py (two new window tests, docstring), cards.json (12 cards added, 65 changed), ledgers/CS2/mutants (5 new mutants of the builder's and round 3's, plus round 4 verifier mutants r4_01-r4_05), lesson labs L02, L04, L08, L09 (not in this slice; cards citing them re-read).",
    "checkout": str(checkout),
    "scratch": "/tmp/CS2-v/d4/",
    "verified_at": "2026-10-28",
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Ran in this round: tools/run_graders.py --unit CS2 --seeds 0-49 (PASS, 50/50); tools/mutate_graders.py --unit CS2 "
        "--seeds 0-49 (55 of 56 killed; the survivor is d4_03, an alternative correct implementation); run_candidates.py over "
        "alternatives A-G, I, K, L on seeds 0-49; tools/run_labs.py --unit CS2 --page project (3/3); page_smoke.py --unit CS2 "
        "--pages project (PASS, in-browser grader 141 passed); check_pages, check_dag, check_projects for CS2 (PASS); "
        "verify_refs --unit CS2 (live, 1 entry, 0 problems) and --offline (560 entries, 0 problems); ruff check and format and "
        "mypy --no-incremental on the grader files and test_project.py (clean); the page's own pytest command with QF_SEED=3 "
        "(reference 141 passed; starter 138 failed, 3 passed). Scripts and outputs: ledgers/CS2/scripts/CS2-d-r4/. Card checks "
        "were automated for all 167 cards (numbers, locators, duplicates, fields) and read by hand for the 77 added or changed "
        "cards and the 90 unchanged cards. NOT CHECKED: (1) every card proof was not re-derived line by line (about 25 T cards "
        "were re-derived or compared with the lesson statement); (2) the lesson texts of L02-L11 were not verified in full "
        "(other slices); (3) the rubric is scored from its descriptors only, with no second scorer; (4) no external source was "
        "read (the only citation is the textbook registry key, which has no locator); (5) the variance tests use exact zero "
        "(constant 5.0 and one value) where the page allows the 1e-9 tolerance: no alternative I wrote fails them, recorded as "
        "an observation, not a row; (6) the Pyodide run was one page_smoke pass, not a timing study."
    ),
    "rows": rows,
    "mutants": mutants,
}
fragment["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": sum(1 for r in rows if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    "mutants": len(mutants),
}
fragment["verdict"] = "PASS" if fragment["summary"]["fail"] == 0 and fragment["summary"]["unverifiable"] == 0 else "FAIL"
target = checkout / "ledgers/CS2/CS2-d.json"
target.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", target, fragment["summary"], fragment["verdict"])
