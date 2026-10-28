import json, re, sys
CK = "/tmp/verify12-M1-d"
rows = json.load(open("/tmp/m1-v12/d/build/rows.json", encoding="utf-8"))
lines = open(CK + "/ledgers/M1/scripts/M1-d-r12/out/mutate_all_r12.out", encoding="utf-8").read().splitlines()
mutants = []
for line in lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.group(1), m.group(2), m.group(3), m.group(4)
    mid = re.match(r"(m\d\d|r1[01]_\d\d|r1[01]d_\d\d|r12d_\d\d|r12v_\d\d)", name).group(1)
    mutants.append({
        "id": mid,
        "file": f"ledgers/M1/mutants/{name}",
        "description": desc,
        "killed_by": killed if status == "KILLED" else "SURVIVED (no test failed at seeds 0-9)",
        "run": "tools/mutate_graders.py --unit M1 --seeds 0-9 (round 12, checkout aebdc15): " + status,
    })
assert len(mutants) == 96, len(mutants)
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = len(rows) - pass_n
fragment = {
    "unit": "M1",
    "slice": "M1-d",
    "round": 12,
    "round_note": "round 12 (independent re-verification of slice M1-d at aebdc15). Delta 91946cf..aebdc15 read: project.html line 164 only (192 checks); grader/test_project.py (must_refuse, the tiny-rate test, the integer-zero tests, the widened invalid-input lists); no M1 cards, lesson, labs, instance or reference change. Rows whose cited subject is byte-identical carry round 11 evidence with the prefix; every other row was re-run or recomputed this round. Mutants: all 96 committed files re-run (92 earlier, of which r12d_01 to r12d_10 were already in aebdc15, plus the four new r12v_01 to r12v_04).",
    "verifier": "Claude Haiku 5.5 (independent verifier, slice M1-d, round 12; did not build M1; no shared context with builders)",
    "pin": "aebdc15 (detached HEAD of /tmp/verify12-M1-d)",
    "base": "91946cf (round-11 pin, used for the delta)",
    "previous_ledger": "/tmp/fanout-frags/M1-d.round11.json (context only)",
    "checkout": "/tmp/verify12-M1-d",
    "scratch": "/tmp/m1-v12/d/",
    "verified_at": "2026-10-28T14:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 12 found two surviving student-error mutants (r12v_01 cutoff 1e-10 for annuity_factor; r12v_03 float schedule interest). Both are FAIL rows with the page sentence cited; the grader is not edited (verifier rule).",
        "Witnesses: the wrong-type TypeError witness (witness_r12v_d) passes 192/192, so the round-11 FAIL row proj-grader-wrong-type-rate-valueerror is closed; witness_r12v_e (TypeError for month counts) fails 10/10, so counts still need ValueError.",
        "Not checked: the Pyodide browser run of the grader and the per-lab 10 s Pyodide budget (page_smoke reported PASS; its timing was not read); the full repo pytest suite (only tests/test_curriculum.py was run); mypy's file list was not confirmed to include grader/.",
        "Live Crossref/registry: tools/verify_refs.py --unit M1 re-verified 1 of 560 entries (0 problems); offline integrity 560 entries, 0 problems. Other registry entries are outside this slice.",
        "Hours are not judged on pace (architect ruling); the arithmetic 2+3+8+7+6+4 = 30 equals data-hours-project 30.",
        "Four earlier-round alternatives (alt_decimal_v6, alt_float_epsilon_v6, alt_fraction_binary_v6, alt_r9_decimal60) fail the suite as they should (binary or float rounding of the rate); they are negative examples, not correct alternatives.",
        "Mutants killed at seed 0 by the first failing test named in out/mutate_all_r12.out; the mutate run used seeds 0-9.",
        "Card count 179 (cards.json); no page states a card count.",
        "Reference-match rules do not apply to this slice (no reference capture).",
    ],
    "summary": (f"M1-d round 12 at aebdc15: {len(rows)} rows, {pass_n} PASS, {fail_n} FAIL. FAIL rows: "
        "proj-grader-mutation-suite (94 of 96 mutants killed), proj-mutant-r12v01-annuity-cutoff-1e-10 (a rate of 5e-11 taken as zero in annuity_factor survives: the suite's only tiny rate is 5e-10), "
        "proj-mutant-r12v03-float-schedule-interest (schedule interest rounded in float survives on the exact tie of principal 462554000 cents at 0.027: exact 1040747, float 1040746, against the page's exact-arithmetic rule). "
        "Closed in this round: the round-11 FAILs proj-grader-wrong-type-rate-valueerror (witness_r12v_d passes 192/192) and proj-mutant-r11d03-annuity-tiny-cutoff (killed)."),
}
json.dump(fragment, open(CK + "/ledgers/M1/M1-d.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written", len(rows), pass_n, fail_n, "mutants", len(mutants))
