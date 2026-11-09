"""FC1-c round 17: write the delta-verification fragment from the outputs in v17out/ (no network, no course edits)."""

import json
import re
import sys
from datetime import UTC, datetime

root = sys.argv[1]
out = f"{root}/ledgers/FC1/scripts/FC1-c-r17/v17out"
frag_prev = json.load(open("/Users/billyribeiro/.fanout/frags/D-FC1-c.round16.json", encoding="utf-8"))
prev_rows = {r["id"]: r for r in frag_prev["rows"]}

S = "ledgers/FC1/scripts/FC1-c-r17/v17out/"
CARRY = "Carried from round 16 (%s byte-identical since the previous pin e896b7a4): "

mutants = []
for line in open(f"{out}/mutate_s0-9_final.out", encoding="utf-8"):
    m = re.match(r"^KILLED (\S+)\.py: (.*) -> (.*)$", line.rstrip("\n"))
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2).strip(), "killed_by": m.group(3).strip()})
survivors = [l for l in open(f"{out}/mutate_s0-9_final.out", encoding="utf-8") if l.startswith("SURVIVED")]
assert not survivors, survivors
assert len(mutants) == 153, len(mutants)

rows = [
    {"id": "proj-run-graders", "check": "2.6-autograde-reference", "location": "course/modules/FC/FC1/grader/reference.py; tools/run_graders.py; grader/test_project.py (changed)",
     "status": "PASS", "evidence": f"Re-run from scratch because test_project.py changed: `.venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-49` -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0 ({S}run_graders_s0-49.out)."},
    {"id": "proj-collect-count-65", "check": "2.6-page-count", "location": "course/modules/FC/FC1/project.html line 171; grader/test_project.py",
     "status": "PASS", "evidence": f"Re-derived: collect-only of the reference (as instruments.py) with the suite -> '101 tests collected' ({S}collect_count.out); `grep -c '^def test_'` = 101. project.html line 171 now says 'runs 101 checks' (was 99). The id keeps the historical '65' for tracking only."},
    {"id": "proj-browser-suite", "check": "2.6-autograder-both", "location": "course/modules/FC/FC1/project.html line 302 (section#grader); course/assets/js/grader.js",
     "status": "PASS", "evidence": f"Re-run: `tools/page_smoke.py --unit FC1 --pages project` -> 'in-browser grader: All 101 tests pass on seed 496746643' and 'page_smoke modules/FC/FC1/project.html: PASS' ({S}page_smoke_project.out). Line 302 is outside the delta hunks (51-57, 168-172)."},
    {"id": "proj-alternatives-five", "check": "2.6-alternatives", "location": "ledgers/FC1/alternatives/a1..a5 (run against grader/test_project.py)",
     "status": "PASS", "evidence": f"Re-run on the 101-test suite, seeds 0-49, browser flags (--assert=plain -W error): a1 0/50, a2 0/50, a3 0/50, a4 0/50, a5 0/50 failing ({S}alternatives_s0-49.out, runner {S}v17_alt_run.py). Each is a correct implementation; none is refused by the new accepted-input tests."},
    {"id": "proj-alternatives-integer-only", "check": "2.6-alternatives", "location": "ledgers/FC1/scripts/FC1-c-r14/alt_integer_only_r14.py",
     "status": "PASS", "evidence": f"Re-run (subject: suite changed): 'PASS alt_integer_only_r14.py: failing seeds 0/50 []' ({S}alternatives_s0-49.out)."},
    {"id": "proj-alternatives-new-r15", "check": "2.6-alternatives (new in round 15)", "location": "ledgers/FC1/scripts/FC1-c-r15/alternatives/alt_decimal_100_digits_r15.py; alt_cached_lists_r15.py",
     "status": "PASS", "evidence": f"Re-run: 'PASS alt_decimal_100_digits_r15.py: failing seeds 0/50 []' and 'PASS alt_cached_lists_r15.py: failing seeds 0/50 []' ({S}alternatives_s0-49.out)."},
    {"id": "proj-instances-20", "check": "2.6-instances", "location": "course/modules/FC/FC1/grader/instance.py",
     "status": "PASS", "evidence": CARRY % "course/modules/FC/FC1/grader/instance.py and grader/reference.py (git diff --quiet e896b7a4..HEAD for both)" + "the round-16 instance evidence (ledgers/FC1/scripts/FC1-c-r16/out/instances_r16.out: range violations [], 50 distinct answer tuples over seeds 0-49, label contains SIMULATED). The suite changes do not touch instance generation."},
    {"id": "proj-instances-50", "check": "2.6-instances", "location": "course/modules/FC/FC1/grader/instance.py; grader/reference.py",
     "status": "PASS", "evidence": CARRY % "course/modules/FC/FC1/grader/instance.py and grader/reference.py" + "the round-16 distinct-value counts (instances_r16.out: 50 distinct bond prices, 50 event lists, 50 trade event lists over seeds 0-49). Run_graders 0-49 re-run this round: 50/50."},
    {"id": "proj-starter-vs-spec", "check": "2.6-spec", "location": "course/modules/FC/FC1/grader/starter.py; project.html line 161",
     "status": "PASS", "evidence": CARRY % "course/modules/FC/FC1/grader/starter.py and project.html lines 153-161 (hunks are only at lines 51-57 and 168-172)" + "starter.py is UNCHANGED in the delta; the names and signatures at line 161 equal the starter's (round-16 comparison, instances_r16.out)."},
    {"id": "proj-spec-questions", "check": "2.6-spec", "location": "course/modules/FC/FC1/project.html lines 153-172",
     "status": "PASS", "evidence": "Re-read from scratch (sed of lines 153-172, tags stripped): Required outputs match starter names; Constraints (line 163) and the named-condition list (lines 165-167) name 8 conditions (Bond 3, bond_price_cents 1, CashTrade 4), matching the 22 must_raise call sites in test functions of grader/test_project.py (lines 217-736; helper at 799, definition at 75); grading-mode line 171 reads '101 checks', equal to the collect count."},
    {"id": "proj-ladder", "check": "2.6-ladder", "location": "course/modules/FC/FC1/project.html lines 41-50; course/modules/FC/FC1/index.html lines 122-128",
     "status": "PASS", "evidence": CARRY % "course/modules/FC/FC1/project.html lines 41-50 and index.html (index.html UNCHANGED; project.html hunks at 51-57 and 168-172)" + "round-16 ladder evidence (line 43 placement sentence and rungs list)."},
    {"id": "proj-stretch-scope", "check": "2.6-scope", "location": "course/modules/FC/FC1/project.html section#stretch lines 312-318",
     "status": "PASS", "evidence": CARRY % "project.html lines 312-318 (section#stretch)" + "no hunk in that range (git diff -U0 e896b7a4..HEAD)."},
    {"id": "proj-local-command", "check": "2.6-local-run", "location": "course/modules/FC/FC1/project.html section#local lines 305-310; grader/starter.py docstring",
     "status": "PASS", "evidence": CARRY % "project.html lines 305-310 and grader/starter.py" + "no hunk in 305-310; starter.py UNCHANGED."},
    {"id": "proj-lab1-twin", "check": "2.5-lab", "location": "course/modules/FC/FC1/project.html lab-FC1-project-1 (lines 56-102); tests/labs/FC1/lab-FC1-project-1.py",
     "status": "PASS", "evidence": CARRY % "project.html lines 56-102 (lab-FC1-project-1 block) and tests/labs/FC1/lab-FC1-project-1.py (tests/labs/FC1 UNCHANGED)" + "fresh checks this round: `tools/run_labs.py --unit FC1` -> 'run_labs FC1: PASS (8/8)' (" + S + "run_labs.out); twin under `python -I -W error` rc=0 printing 'bond price (cents): 102775' and 'trade event (period, cents): (2, -98500)' (" + S + "twin_lab-FC1-project-1.out)."},
    {"id": "proj-lab2-completion", "check": "2.5-lab", "location": "course/modules/FC/FC1/project.html lab-FC1-project-2 (lines 104-150); tests/labs/FC1/lab-FC1-project-2.py",
     "status": "PASS", "evidence": CARRY % "project.html lines 104-150 and tests/labs/FC1/lab-FC1-project-2.py" + "fresh: run_labs 8/8 (" + S + "run_labs.out) and the twin under -I -W error rc=0 (" + S + "twin_lab-FC1-project-2.out)."},
    {"id": "proj-lab2-docstring", "check": "2.9-prose", "location": "course/modules/FC/FC1/project.html line 107; tests/labs/FC1/lab-FC1-project-2.py line 1",
     "status": "PASS", "evidence": CARRY % "project.html line 107 and lab-FC1-project-2.py" + "line 1 is 'Rung 2 completed solution: the worked example with its two blanks filled in.' (sed -n 1p, re-read this round)."},
    {"id": "proj-lab3-fixtures", "check": "2.5-lab", "location": "course/modules/FC/FC1/project.html lab-FC1-project-3 (lines 196-276); tests/labs/FC1/lab-FC1-project-3.py",
     "status": "PASS", "evidence": CARRY % "project.html lines 196-276 and lab-FC1-project-3.py" + "fresh: twin under -I -W error rc=0 printing 'fixture G events ... [(1, 10001)]' and 'fixture G price ... 5001' (" + S + "twin_lab-FC1-project-3.out)."},
    {"id": "proj-prose-numbers", "check": "2.2-numbers", "location": "course/modules/FC/FC1/project.html lines 54, 58, 101, 171, 176, 186-193, 198, 275, 290, 293",
     "status": "PASS", "evidence": f"Re-derived from scratch with exact Fractions in ledgers/FC1/scripts/FC1-c-r17/v17_numbers.py ({S}numbers.out): lab-1 events [(1,5000),(2,5000),(3,105000)] (line 58), exact PV 102775.091033 rounds to 102775 (line 101), trade -98500 (line 101); line 171 counts 101 (collect); line 171 new numbers 15000, 20001, 10^18 bps = 150 %, 200.01 %, 10^16 % (exact); 10^18 cents and 10^9 cents prices; settlement 10^18 (test list). Line 54 numbers 100000, 500, 400, 9850, 10 units match lab-1 constants (tests/labs/FC1/lab-FC1-project-1.py lines 14-17, 33). Hours 20 (line 293) recomputed in proj-hours-arithmetic."},
    {"id": "proj-fixture-claims", "check": "2.4-math", "location": "course/modules/FC/FC1/project.html lines 183-194 and 276; grader/test_project.py fixture tests",
     "status": "PASS", "evidence": f"Re-derived from scratch ({S}numbers.out): A events [(1,10500)], price 10000; B 210000/19 = 11052.6316 rounds 11053; C events [(1,5001),(2,15002)], coupon 10001/2 -> 5001 (line 188 correct); D [(1,2)]; E (2,-98500) and seller (2,98500); F exact 1/2, half-away 1, python round 0; G [(1,10001)] price 5001; rounding fixture events [(1,500),(2,500),(3,10500)], exact 10277.509103 -> 10278, termwise 481+462+9334 = 10277. Test functions at the current grader lines: test_bond_one_period_fixture (174), test_bond_zero_coupon_pays_only_the_face (182), test_bond_half_cent_coupon_rounds_away (189), one-cent-face (197), rounded_once (417), hand_fixture (428), exact_half_cent (438), five_thousand_point_five (447), 496 bps (455), 400 bps (480), just_under_half (491) (test_project.py, grep of 'def test_'). Lines shifted by the two new tests inserted at 364 and 663 only."},
    {"id": "proj-hours-arithmetic", "check": "2.9-hours", "location": "course/modules/FC/FC1/project.html section#budget lines 283-293; course/modules/FC/FC1/index.html lines 29-41",
     "status": "PASS", "evidence": CARRY % "project.html lines 283-293 and index.html (UNCHANGED)" + "1+2+5+4+2+3+3 = 20 recomputed this round, equal to Total 20 and the hub's 20."},
    {"id": "proj-check-pages-dag", "check": "2.9-structure", "location": "course/modules/FC/FC1/ (project.html)",
     "status": "PASS", "evidence": f"Re-run: `tools/check_pages.py --unit FC1` -> 'check_pages FC1: PASS' rc=0; `tools/check_dag.py --unit FC1` -> 'check_dag FC1: PASS' rc=0; `tools/check_projects.py --unit FC1` -> 'check_projects FC1: PASS' rc=0 ({S}check_pages.out, check_dag.out, check_projects.out)."},
    {"id": "proj-dag-closure", "check": "2.9-dag", "location": "course/modules/FC/FC1/project.html lines 58, 177-178, 316; course/modules/FC/FC1/L05.html line 63",
     "status": "PASS", "evidence": f"Re-verified (L05.html changed in the delta at line 97-ish, Remark 2.3, another slice): check_dag FC1 PASS ({S}check_dag.out). project.html line 177 links 'trade lifecycle in Lesson 5' (L05.html); L05.html line 63 still reads 'Each state carries a <em>business-day offset</em>: the number of business days after the trade date' (python byte check, markup inside the phrase)."},
    {"id": "proj-notation", "check": "2.4-notation", "location": "course/modules/FC/FC1/project.html math (lines 58, 106, 166, 178); notation/notation.json",
     "status": "PASS", "evidence": "Re-verified: the page has 8 \\( tokens on lines 58, 106, 166 and 178 (y = 400/10000 and (1+y)^{-t} at line 58; t and (1+y)^{-t} at line 106; 1+y at line 166; t, (1+y)^{-t} and t at line 178); none on the changed lines 54 and 171. Correction to the round-16 count (it listed 5 and omitted the (1+y)^{-t} formulas): verdict unchanged. y and t are not registered symbols; notation.json 'about' says conventionally local letters are defined in each lesson where used, and y is defined at line 58 (y = 400/10000) and t is the period index (line 106, line 178). Registered symbols T, \\Phi, \\gamma_3, R^\\ast, \\mathbb{Q} are not used on the page."},
    {"id": "proj-banned-phrases", "check": "2.9-prose", "location": "course/modules/FC/FC1/project.html; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py",
     "status": "PASS", "evidence": f"Re-run: check_pages FC1 PASS (its BANNED list, tools/check_pages.py lines 58-75, covers the page). grep -i -E over the grader and lab files for the BANNED patterns and 'clearly|obviously|...': only grader/test_project.py line 837 '_named_when_unimplemented(test: Callable[..., None])' (a code identifier and type syntax, not prose). Page: no match."},
    {"id": "proj-reading-list", "check": "2.9-citations", "location": "course/modules/FC/FC1/project.html lines 323-327; references/references.json; curriculum/02-economics-finance-core.yaml lines 383-386",
     "status": "PASS", "evidence": CARRY % "project.html lines 323-327, references/references.json and curriculum/02-economics-finance-core.yaml (both UNCHANGED)" + "round-16 evidence; 'references/references.json' has mishkin2021economics and harris2002trading; the third source is absent, as the page says."},
    {"id": "proj-scope-ruling5", "check": "2.6-scope", "location": "course/modules/FC/FC1/project.html line 157; curriculum/02-economics-finance-core.yaml lines 388-395; plans/FINAL-ARCHITECT-RULINGS.md ruling 5 (lines 11-13)",
     "status": "PASS", "evidence": CARRY % "project.html line 157, the curriculum yaml and plans/FINAL-ARCHITECT-RULINGS.md lines 11-12" + "the ruling file changed only at line 103 onward (rulings 31 and 35-36); md5 of lines 11-12 is identical at e896b7a4 and HEAD (5e26ec8d9559f9f4a42e94ad9ca15f84)."},
    {"id": "proj-named-conditions", "check": "2.6-autograde-mutation", "location": "course/modules/FC/FC1/project.html lines 165-167; grader/test_project.py must_raise call sites",
     "status": "PASS", "evidence": "Re-grepped this round: 22 must_raise call sites in test functions (test_project.py lines 217, 222, 234, 239, 260, 271, 277, 533, 538, 593, 598, 642, 675, 680, 685, 690, 695, 708, 713, 726, 731, 736), plus the helper call at 799 and its definition at 75. Boundaries: periods 0/-1 refused and 1 accepted; face 0/-1 refused; coupon -1 refused, 0 accepted; yield -10000 and -20000 refused, -9999 accepted; quantity 0/-1 refused, 1 accepted; price -1 refused, 0 accepted; side 0/2/-2/3/-3 refused, +1/-1 accepted; settlement_day 0/-1 refused, 1 accepted."},
    {"id": "proj-named-conditions-context", "check": "2.6-autograde-mutation", "location": "course/modules/FC/FC1/project.html lines 163 and 167; grader/test_project.py lines 63-75 and 268-278",
     "status": "PASS", "evidence": "Re-read: page line 163 says each named condition raises ValueError and any other invalid input may raise any exception or return; line 167 lists the CashTrade refusals. test_project.py lines 63-75 hold the helpers (must_raise at 75 requires a condition string); the zero-coupon refusals at 271 and 277 carry the page's 'with or without a coupon' basis."},
    {"id": "proj-failure-messages", "check": "2.6-messages", "location": "course/modules/FC/FC1/grader/test_project.py (all assertions, must_raise, must_accept, checked_events, checked_int)",
     "status": "PASS", "evidence": f"Re-run: ledgers/FC1/scripts/FC1-c-r17/v17_ast_scan.py ({S}v17_ast_scan.out): test functions 101; asserts without message []; must_raise/must_accept calls without a condition string []."},
    {"id": "proj-test-docstring", "check": "2.4-docstrings", "location": "course/modules/FC/FC1/grader/test_project.py docstrings (new tests at lines 364-371 and 663-670)",
     "status": "PASS", "evidence": f"v17_ast_scan.out: tests without a docstring []. The two new docstrings state the page's basis (coupon_bps negative is the only refused coupon; price_cents negative is the only refused price) and the expected value, which the reference reproduces (run_graders 50/50) and numbers.out re-derives."},
    {"id": "proj-simulated-labels", "check": "2.8-simulated", "location": "course/modules/FC/FC1/project.html lines 54, 72, 120, 159; tests/labs/FC1/lab-FC1-project-1.py lines 1, 14-17; lab-FC1-project-2.py line 14",
     "status": "PASS", "evidence": f"Line 54 (changed): 'Both labs use SIMULATED values, meaning values typed into the labs rather than market data. No file is read.' Matches the lab twins: lab-FC1-project-1.py line 14 'SIMULATED face of 1,000.00, not market data' with typed constants at lines 14-17 and 33; lab-FC1-project-2.py has the same constants. No open/read/urllib/requests/socket/random tokens in the three twins ({S}v17_ast_scan.out). The round-16 wording note ('generated numbers') is resolved."},
    {"id": "proj-silence-coverage", "check": "2.6-silence", "location": "course/modules/FC/FC1/project.html line 163; grader/test_project.py lines 760-786",
     "status": "PASS", "evidence": "Re-read: test_the_module_prints_nothing (line 760) runs 14 valid inputs (seeded case and its events and trade, yield -9999/-5000/0, coupon 0, price 0, side -1, quantity 1, settlement 1, face 1 cent, periods 1 and 12), each checked with capsys; test_refused_inputs_print_nothing_before_they_raise (line 786) covers refused inputs. Its docstring says these are the inputs checked, as page line 163 says."},
    {"id": "proj-privacy-claim", "check": "2.9-privacy", "location": "course/modules/FC/FC1/project.html line 341; course/assets/js/grader.js; course/assets/js/py-worker.js; course/assets/js/store.js",
     "status": "PASS", "evidence": CARRY % "project.html line 341 and course/assets/js (git diff --quiet e896b7a4..HEAD -- course/assets/js: UNCHANGED)" + "round-16 evidence."},
    {"id": "proj-lint-types", "check": "2.6-lint", "location": "course/modules/FC/FC1/grader/*.py; tests/labs/FC1/*.py",
     "status": "PASS", "evidence": f"Re-run: `ruff check course/modules/FC/FC1/grader tests/labs/FC1` -> 'All checks passed!' rc=0 ({S}ruff_check.out); `ruff format --check` same scope -> '12 files already formatted' rc=0 ({S}ruff_format.out); `mypy --no-incremental` (repo) -> 'Success: no issues found in 385 source files' rc=0 ({S}mypy_repo.out). The mypy --strict run on reference.py, starter.py and instance.py (unchanged) is carried from round 16."},
    {"id": "proj-reference-deployment", "check": "2.9-structure", "location": "course/modules/FC/FC1/grader/reference.py lines 3-4; BLUEPRINT.md lines 400-401",
     "status": "PASS", "evidence": CARRY % "grader/reference.py and BLUEPRINT.md (both UNCHANGED)" + "the round-16 repository-wide flag (reference.py is tracked; BLUEPRINT requires its exclusion; nothing enforces it) is repeated in registry_flags."},
    {"id": "proj-exemplar-blind", "check": "2.9-blind", "location": "course/modules/FC/FC1/project.html; curriculum grading for FC1 project",
     "status": "PASS", "evidence": "Re-run: `grep -c -i exemplar course/modules/FC/FC1/project.html` = 0 matches. The 'solution' at line 107 is the learner-facing worked example for Lab 2, not a graded exemplar."},
    {"id": "proj-mutant-set-earlier", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/ (files present at 1431aa1d)",
     "status": "PASS", "evidence": f"`git diff --name-status 1431aa1d..HEAD -- ledgers/FC1/mutants`: 14 A, no M and no D, so the files that existed at 1431aa1d (136 = 150 - 14, counted at aa659725) are byte-identical. The five lab mutants are not in this set: they are not at 1431aa1d and have been moved to ledgers/FC1/lab-mutants (git R100 renames e896b7a4..HEAD)."},
    {"id": "proj-mutant-first-line", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/*.py (first docstring line of every file)",
     "status": "PASS", "evidence": f"{S}v17_ast_scan.out lists every first docstring line of the 153 files: each names a student error (for example 'Bond warns (a UserWarning) when it has more than eight periods...', 'CashTrade refuses a quantity above 500 units...'). The five lab mutants are no longer in ledgers/FC1/mutants/, so the round-16 note on them is resolved."},
    {"id": "proj-new-mutants-r10", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r10n01..r10n04; r10c_*",
     "status": "PASS", "evidence": f"`tools/mutate_graders.py --unit FC1 --seeds 0-9` (rerun this round, {S}mutate_s0-9_final.out): every r10n* and r10c_* file KILLED (153/153)."},
    {"id": "proj-new-mutants-r11", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r11n01..r11n03; r11c_*",
     "status": "PASS", "evidence": f"Same run ({S}mutate_s0-9_final.out): every r11n* and r11c_* KILLED."},
    {"id": "proj-new-mutants-r12", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r12n01..r12n03; r12c_*",
     "status": "PASS", "evidence": f"Same run: every r12n* and r12c_* KILLED."},
    {"id": "proj-mutant-r13n01", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r13n01_coupon_computed_in_float.py; grader/test_project.py test_bond_coupon_is_exact_for_a_face_too_large_for_floats",
     "status": "PASS", "evidence": "KILLED in this round's run: killed_by test_bond_coupon_is_exact_for_a_face_too_large_for_floats (seed 0) (" + S + "mutate_s0-9_final.out)."},
    {"id": "proj-mutant-r13n02", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r13n02_trade_cash_flow_in_float.py; grader/test_project.py test_trade_cash_flow_is_exact_above_two_to_the_fifty_three",
     "status": "PASS", "evidence": "KILLED this round: killed_by test_trade_cash_flow_is_exact_above_two_to_the_fifty_three (seed 0) (" + S + "mutate_s0-9_final.out)."},
    {"id": "proj-mutant-r13n03", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r13n03_yield_rate_through_float.py; grader/test_project.py test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield",
     "status": "PASS", "evidence": "KILLED this round: killed_by test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield (seed 0)."},
    {"id": "proj-new-mutants-r14-killed", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r14n02, r14n03, r14n04",
     "status": "PASS", "evidence": "KILLED this round (" + S + "mutate_s0-9_final.out)."},
    {"id": "proj-mutant-r14n01", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r14n01_sale_skips_quantity_and_settlement_checks.py; grader/test_project.py test_sale_quantity_zero_is_refused",
     "status": "PASS", "evidence": "KILLED this round: killed_by test_sale_quantity_zero_is_refused (seed 0)."},
    {"id": "proj-mutant-r14n05", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r14n05_bond_periods_and_face_checked_only_with_a_coupon.py; grader/test_project.py test_bond_zero_coupon_periods_zero_is_refused",
     "status": "PASS", "evidence": "KILLED this round: killed_by test_bond_zero_coupon_periods_zero_is_refused (seed 0)."},
    {"id": "proj-new-mutants-r15-killed", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r15n01..r15n04",
     "status": "PASS", "evidence": "KILLED this round (" + S + "mutate_s0-9_final.out)."},
    {"id": "proj-mutant-r15n05", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r15n05_price_refused_above_one_million_cents.py; grader/test_project.py test_trade_price_of_ten_to_the_ninth_cents_is_accepted (line 653)",
     "status": "PASS", "evidence": "KILLED this round: 'KILLED r15n05_price_refused_above_one_million_cents.py ... -> test_trade_price_of_ten_to_the_ninth_cents_is_accepted (seed 0)' (" + S + "mutate_s0-9_final.out)."},
    {"id": "proj-mutant-r15n06", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r15n06_coupon_refused_above_twenty_thousand_bps.py; grader/test_project.py test_bond_coupon_of_twenty_thousand_one_bps_is_accepted (line 354)",
     "status": "PASS", "evidence": "KILLED this round: killed_by test_bond_coupon_of_twenty_thousand_one_bps_is_accepted (seed 0) (" + S + "mutate_s0-9_final.out)."},
    {"id": "proj-accepted-input-tests-r16", "check": "2.6-autograde-accepted", "location": "grader/test_project.py lines 354-360 and 653-660 (round-16 tests, now 354-360 and 653-660 after the round-17 insertions below them); project.html lines 165-171",
     "status": "PASS", "evidence": f"Re-run: run_graders 0-49 50/50 ({S}run_graders_s0-49.out); both tests pass on the reference. Expected values re-derived: Bond(10000, 20001, 1).events() = [(1, 30001)] and CashTrade(10, 10**9, 1, 2).events() = [(2, -10000000000)] ({S}numbers.out). All five alternatives pass them ({S}alternatives_s0-49.out)."},
    {"id": "proj-accepted-input-tests-r17", "check": "2.6-autograde-accepted (new in round 17, ruling 36)", "location": "grader/test_project.py lines 364-371 (Bond coupon 10**18 bps) and 663-670 (CashTrade price 10**18 cents); project.html line 171 and line 165, 167",
     "status": "PASS", "evidence": f"Both new tests pass on the reference (run_graders 0-49 50/50). Expected values re-derived: Bond(10000, 10**18, 1).events() == [(1, 10**18 + 10000)] (numbers.out: True); CashTrade(10, 10**18, 1, 2).events() == [(2, -(10*10**18))] (numbers.out). The page names only coupon_bps negative (line 165) and price_cents negative (line 167) as refused, and line 171 says the page names no upper limit on a price or a coupon, so both are accepted-input checks the page supports. All eight alternatives (a1-a5, alt_integer_only_r14, alt_decimal_100_digits_r15, alt_cached_lists_r15) pass them (alternatives_s0-49.out). The docstrings name only the refused inputs the page names."},
    {"id": "proj-mutant-r16n02", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r16n02_coupon_refused_above_one_hundred_percent.py; grader/test_project.py test_bond_coupon_above_one_hundred_percent_is_accepted (line 344)",
     "status": "PASS", "evidence": "KILLED this round: killed_by test_bond_coupon_above_one_hundred_percent_is_accepted (seed 0) (" + S + "mutate_s0-9_final.out)."},
    {"id": "proj-mutant-r16n01", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r16n01_price_refused_above_two_to_the_thirty_one.py; grader/test_project.py test_trade_price_of_ten_to_the_eighteenth_cents_is_accepted (line 663)",
     "status": "PASS", "evidence": "Was FAIL in round 16 (survived seeds 0-9 and 0-49). Now KILLED: killed_by test_trade_price_of_ten_to_the_eighteenth_cents_is_accepted (seed 0) (" + S + "mutate_s0-9_final.out). Ruling 36 directs this kill (the 10**18 accept test)."},
    {"id": "proj-mutant-r16n03", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/r16n03_coupon_refused_above_two_to_the_thirty_one_bps.py; grader/test_project.py test_bond_coupon_of_ten_to_the_eighteenth_bps_is_accepted (line 364)",
     "status": "PASS", "evidence": "Was FAIL in round 16. Now KILLED: killed_by test_bond_coupon_of_ten_to_the_eighteenth_bps_is_accepted (seed 0) (" + S + "mutate_s0-9_final.out). Ruling 36."},
    {"id": "proj-mutant-r17-new", "check": "2.6-mutants (new in round 17, three student errors written by this verifier)", "location": "ledgers/FC1/mutants/r17n01_trade_price_rounded_to_ten_cents.py; r17n02_zero_coupon_face_paid_in_first_period.py; r17n03_coupons_discounted_as_paid_at_period_start.py",
     "status": "PASS", "evidence": f"Written by ledgers/FC1/scripts/FC1-c-r17/v17_make_mutants.py from grader/reference.py (complete modules, each parses). Killed on seed 0: r17n01 by test_trade_has_one_settlement_event_on_its_settlement_day; r17n02 by test_bond_zero_coupon_pays_only_the_face_in_the_last_period; r17n03 by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period ({S}mutate_s0-9_final.out)."},
    {"id": "proj-mutants-killed", "check": "2.6-mutants", "location": "ledgers/FC1/mutants/ (153 files); grader/test_project.py",
     "status": "PASS", "evidence": f"`tools/mutate_graders.py --unit FC1 --seeds 0-9` -> 'mutate_graders FC1: PASS (153/153 killed)', rc=0 ({S}mutate_s0-9_final.out). The five lab mutants (fc1a_r5_lab_*) are in ledgers/FC1/lab-mutants and are not graded here (ruling: lab twins are demonstrations)."},
    {"id": "proj-run-labs", "check": "2.5-lab", "location": "tests/labs/FC1 (all eight twins)",
     "status": "PASS", "evidence": f"Re-run: `tools/run_labs.py --unit FC1` -> 'run_labs FC1: PASS (8/8)', rc=0 ({S}run_labs.out)."},
    {"id": "proj-page-smoke", "check": "2.6-page-smoke", "location": "course/modules/FC/FC1/project.html",
     "status": "PASS", "evidence": f"Re-run: `tools/page_smoke.py --unit FC1 --pages project` -> 'in-browser grader: All 101 tests pass on seed 496746643', 'page_smoke modules/FC/FC1/project.html: PASS', 'page_smoke FC1: PASS', rc=0 ({S}page_smoke_project.out)."},
    {"id": "proj-check-projects", "check": "2.6-projects", "location": "course/modules/FC/FC1/project.html; grader panel attributes",
     "status": "PASS", "evidence": f"Re-run: `tools/check_projects.py --unit FC1` -> 'check_projects FC1: PASS', rc=0 ({S}check_projects.out)."},
    {"id": "proj-pytest-targeted", "check": "2.9-tests", "location": "tests/test_curriculum.py; tests/test_labs.py; tests/test_page_checks.py; tests/test_run_labs.py (-k 'FC1 or project or page')",
     "status": "PASS", "evidence": f"`.venv/bin/pytest -q` on those four files with -k 'FC1 or project or page': rc=0, no F or E in output ({S}pytest_targeted.out). `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', rc=0 ({S}verify_refs_offline.out)."},
]

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
missing = sorted(set(prev_rows) - set(ids))
assert not missing, missing
for r in rows:
    assert r["status"] == "PASS"

frag = {
    "unit": "FC1",
    "slice": "c",
    "round": 17,
    "verifier": "Claude Haiku 5.5, independent delta verifier for FC1-c, round 17 (did not build FC1; ruling 30)",
    "pin": "aa659725",
    "base": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a (round-16 pin; round-16 fragment /Users/billyribeiro/.fanout/frags/D-FC1-c.round16.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD17-FC1-c",
    "scratch": "ledgers/FC1/scripts/FC1-c-r17/ (v17_*.py scripts; outputs in v17out/)",
    "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": frag_prev["registry_flags"],
    "freshness_flags": frag_prev["freshness_flags"],
    "notes": (
        "Round 17, FC1-c, delta verification (ruling 30) from the round-16 pin e896b7a4 to aa659725 (HEAD). "
        "Slice delta: course/modules/FC/FC1/project.html (line 54 rungs paragraph wording: 'defined later in this paragraph', "
        "'values typed into the labs'; line 171 grading mode: '101 checks' and the 10**18 accept claims); grader/test_project.py "
        "(two new accepted-input tests, lines 364-371 and 663-670); ledgers/FC1/mutants (r16n01-03 added, five lab mutants "
        "moved to ledgers/FC1/lab-mutants). Round-16 FAIL rows r16n01, r16n03 and proj-mutants-killed are now PASS: all 153 "
        "grader mutants (150 prior plus three written here, r17n01-03) are killed on seeds 0-9. Rows whose subject changed were "
        "re-verified from scratch; the other rows are carried with the carry prefix where the cited files are byte-identical. "
        "Not in this slice and not verified here: L04.html, L05.html (only the cited L05 sentence was checked), cards.json, "
        "FC2 and other units, plans/FINAL-ARCHITECT-RULINGS.md beyond lines 11-12. "
        "Observations (not FAIL rows): (a) the three r17 mutants are my own; the r16 mutant file names are unchanged. "
        "(b) The five lab mutants are not graded; they live in ledgers/FC1/lab-mutants. "
        "(c) Ruling 36 makes further threshold mutants of this family (refusing above an arbitrary bound beyond 10**18) "
        "not required to be killed. "
        "(d) Scripts in ledgers/FC1/scripts/FC1-c-r17/ committed at aa659725 (alt_run_r17.py etc.) were not used; this round's "
        "scripts carry the v17_ prefix. "
        "Not checked: live verify_refs (network); render_curriculum, build_site --check and fetch_data --check (no curriculum, "
        "site or data input in this slice changed); the full pytest suite; mypy --strict on the grader files (unchanged, carried); "
        "Pyodide execution of the new mutants (local only); carried rows were not re-run for unchanged files (carry prefix states the byte-identity check)."
    ),
    "summary": {
        "rows": len(rows),
        "PASS": len(rows),
        "FAIL": 0,
        "UNVERIFIABLE": 0,
        "mutants": len(mutants),
        "mutants_killed": len(mutants),
        "failing_rows": [],
        "prior_round_rows_not_in_this_fragment": [],
    },
}
with open(f"{root}/ledgers/FC1/FC1-c.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "mutants", len(mutants), "prev rows", len(prev_rows))
