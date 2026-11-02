"""Assemble ledgers/E3/E3-e.json for E3-e round 1 from the mutation log and the row list (verifier-written)."""
import json
import re
import sys
from datetime import UTC, datetime

CHECKOUT = "/Users/billyribeiro/.fanout/wt/verifyD1-E3-e"
MUT_LOG = sys.argv[1]
ALT_LOG = sys.argv[2]

mutants = []
for line in open(MUT_LOG, encoding="utf-8"):
    m = re.match(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (.*)$", line.rstrip("\n"))
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else killed.split(" (seed")[0].strip()
    mutants.append({"id": fname[:-3], "description": desc.strip(), "killed_by": killed_by,
                    "status": status})

alt_lines = [l.strip() for l in open(ALT_LOG, encoding="utf-8") if re.match(r"^alt\d: (PASS|FAIL)", l.strip())]

ROWS = json.load(open(f"{CHECKOUT}/ledgers/E3/scripts/E3-e-r1/rows.json", encoding="utf-8"))
if alt_lines:
    for r in ROWS:
        if r["id"] == "E3e-32":
            ok = all("PASS" in l for l in alt_lines) and len(alt_lines) == 5
            r["status"] = "PASS" if ok else "FAIL"
            r["evidence"] = "ledgers/E3/scripts/run_alternatives.py --seeds 0-9 (output kept at ledgers/E3/scripts/E3-e-r1/alternatives.out): " + " | ".join(alt_lines)
            if not ok:
                r["fix"] = "An alternative correct implementation fails the suite; fix the over-constrained test named in the output."
            else:
                r.pop("fix", None)

fragment = {
    "unit": "E3",
    "slice": "e",
    "round": 1,
    "verifier": "Haiku independent verifier, E3-e round 1 (did not build E3)",
    "pin": "d0f39c0",
    "base": "none (round 1)",
    "checkout": CHECKOUT,
    "scratch": "/tmp/e3e_r1/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in ROWS) and all(m["killed_by"] for m in mutants) else "FAIL",
    "rows": [{k: v for k, v in r.items()} for r in ROWS],
    "mutants": [{"id": m["id"], "description": m["description"], "killed_by": m["killed_by"]} for m in mutants],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope of this round: project.html read line by line (767 lines), plus the project lab twins, the grader files the page links, and the lessons only where the project cites them (L02, L03, L06, L07, L08, index.html).",
        "Cards were not read (out of slice per the orchestrator's instruction).",
        "The E3-e fragment ledgers/E3/E3-e.json from earlier rounds (round 13, pin 762f636) is still in the checkout; this round-1 fragment replaces it in the checkout as requested.",
        "check_pages.py --unit E3 --page project reports lesson-only checks on the project page; this is a page-filter artifact, and the full-unit check_pages run passes.",
        "Mutation run: tools/mutate_graders.py --unit E3 --seeds 0-9 reported 62/63 killed; the survivor is r10n06_logit_log_term_naive_exp_overflow.py.",
    ],
    "summary": {},
}
fragment["summary"] = {
    "rows": len(ROWS),
    "pass": sum(r["status"] == "PASS" for r in ROWS),
    "fail": sum(r["status"] == "FAIL" for r in ROWS),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in ROWS),
    "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    "mutants": len(mutants),
}
out = f"{CHECKOUT}/ledgers/E3/E3-e.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, fragment["summary"], fragment["verdict"])
