"""Write the round-3 M7-d ledger fragment from the verification outputs. Run from the checkout root."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "ledgers/M7/scripts/M7-d-r3"
mutate = (D / "mutate_graders_M7_seeds0-49.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mutate:
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, description, killed_by = m.groups()
    mutants.append({
        "id": name,
        "description": description,
        "killed_by": killed_by if status == "KILLED" else "none: survived the suite on seeds 0-49",
    })
rows = json.loads((D / "rows_r3.json").read_text(encoding="utf-8"))
killed = sum(1 for m in mutants if m["killed_by"] != "none: survived the suite on seeds 0-49")
fails = [r for r in rows if r["status"] != "PASS"]
fragment = {
    "unit": "M7",
    "slice": "M7-d",
    "round": 3,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 3, slice M7-d: project.html, grader, project labs, cards.json; did not build M7)",
    "pin": "aa3c26c (detached checkout /tmp/verifyB3-M7-d; round-2 pin 1817191; delta 1817191..aa3c26c covers project.html, grader/test_project.py, cards.json, L01 and L04 lab twins, the M7 mutants folder)",
    "base": "1817191",
    "checkout": "/tmp/verifyB3-M7-d",
    "scratch": "/tmp/M7-v/d-r3/",
    "verified_at": "2026-10-28",
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round-3 delta re-verification. Commands on the pin: run_graders M7 seeds 0-49 (50/50); mutate_graders M7 --seeds 0-49 "
        f"({killed}/{len(mutants)} killed; survivor v06 is the only one, see m7d-mutate-tool-verdict); alternatives on seeds 0-49: "
        "core routes 1-5 (50/50 each), bland, exact_order, first_order (50/50 each), float_arithmetic (0/50: crashes with RuntimeError "
        "'the working set lost independence' on valid cases, a defect of that alternative, not counted as a witness); "
        "collect-only 145 on all 50 seeds; starter run 142 failed; run_labs M7 11/11; page_smoke project PASS; check_projects, "
        "check_pages, check_dag PASS; ruff check and format PASS; mypy --strict plan command PASS; pytest -k M7 exit 0. "
        "Independent recomputation: scripts lab1_check.py, cards_numbers.py, l04_gap.py, card_nums.py, card_expected_check.py. "
        "Card count is 143 (round 2 recorded 147). Not done: a line-by-line read of every card against the L01-L08 prose "
        "(m7d-cards-vs-lesson-text is UNVERIFIABLE). No external source was read this round (the reading list cites only registry keys)."
    ),
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants": len(mutants),
        "mutants_survived": len(mutants) - killed,
    },
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out)
