"""Round-12 fragment builder for FC1 slice c. Writes ledgers/FC1/FC1-c.json from the rows below and the mutation
output saved in this directory. Carried rows cite the round-11 evidence and say so."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PIN = "460b696"
BASE = "625d936 (round-11 pin)"
S = "scripts/FC1-c-r12/"
CARRY = "Carried from round 11 (files byte-identical since the previous pin 625d936): "

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

MUT_FIX = (
    "Add to course/modules/FC/FC1/grader/test_project.py a fixture whose exact price is a half cent that float "
    "discounting misses: Bond(1704285, 179, 1) at 496 bps has exact present value 3305625/2 = 1652812.5 cents, so "
    "bond_price_cents must return 1652813. The float mutant and alternative a5 return 1652812 (" + S + "exact_half_probe.py)."
)

rows = [
    row("proj-run-graders", "2.6 autograder 1", "course/modules/FC/FC1/grader/", "PASS",
        "Re-run: .venv/bin/python tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.1 s)' (" + S + "run_graders_FC1_0-49.out)."),
    row("proj-collect-count-55", "2.6 rubric/count", "project.html line 171; grader/test_project.py", "PASS",
        "project.html line 171 now says 'runs 62 checks'. Collect-only on the reference: '62 tests collected' (" + S + "alts_and_collect.out); page_smoke in-browser: 'All 62 tests pass' (" + S + "page_smoke_project.out). The count changed from 61 by the test added at test_project.py line 252."),
    row("proj-browser-suite", "2.6 autograder dual mode", "project.html line 301; course/assets/js/grader.js", "PASS",
        "page_smoke --unit FC1 --pages project: 'in-browser grader: All 62 tests pass on seed 956511560' and 'page_smoke FC1: PASS' (" + S + "page_smoke_project.out)."),
    row("proj-local-command", "2.6 local run", "project.html section#local, line 307; starter.py docstring", "PASS",
        CARRY + "project.html section#local (lines 305-310 region) and grader/starter.py. Command 'QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py' matches the flags used by run_graders (tools/run_graders.py)."),
    row("proj-alternatives-five", "2.6 over-constraint", "ledgers/FC1/alternatives/a1..a5", "FAIL",
        "Ran all five alternatives and the reference on seeds 0-19 (" + S + "alts_and_collect.out): 0 failing seeds for each. But a5_float_discounting_exact_half_up.py is not a correct implementation under the page rule: it returns 1652812 for Bond(1704285, 179, 1) at 496 bps, whose exact value is 1652812.5 and whose correct price is 1652813 (" + S + "exact_half_probe.py). The grader passes it only because the suite has no exact-half case that float misses.",
        "Relabel a5 as a rejected float alternative (it is an example of the error, not a correct implementation), or make it exact; then add the exact-half fixture below to the grader. Fix: " + MUT_FIX),
    row("proj-instances-50", "2.6 instances", "course/modules/FC/FC1/grader/instance.py", "PASS",
        CARRY + "grader/instance.py. Round-12 check: the instance ranges (face 100000-5000000, periods 1-8, yield 50-900) were read at instance.py lines 21-28; run_graders on seeds 0-49 passed."),
    row("proj-starter-vs-spec", "2.6 starter", "grader/starter.py; project.html line 161", "PASS",
        CARRY + "grader/starter.py and project.html line 161 (Required outputs). Names and signatures match the spec."),
    row("proj-spec-questions", "2.6 spec", "project.html section#spec lines 153-172", "PASS",
        "Re-read this round, lines 153-172 (Context, Inputs, Required outputs, Constraints, Grading mode). Questions a student would need answered: the seeded case has no fixed period range beyond 1-8 (the page names none; the grader does not depend on it); the page states sign, indexing and rounding in Conventions (lines 163-171 region)."),
    row("proj-ladder", "2.6 ladder", "project.html section#ladder lines 41-50", "PASS",
        "Re-read lines 41-50: rung 1 annotated lab (Lab 1), rung 2 graded completion (Lab 2), rung 3 spec, rung 4 stretch. Scope note, not a failure of this row: rung 3 and the page describe cash instruments only, as the binding architect decision in plans/FC1-build-plan.md (section 'Architect decisions', Module specifics) requires. The curriculum project brief at curriculum/02-economics-finance-core.yaml lines 388-395 (curriculum.json) still says 'bonds, futures, swaps and options'. That conflict is recorded in notes for the user and is not decided here."),
    row("proj-stretch-scope", "2.6 stretch", "project.html section#stretch lines 311-318", "PASS",
        CARRY + "project.html section#stretch (line range 311-318 unchanged; the only project.html hunk in the delta is line 168)."),
    row("proj-lab1-twin", "2.5 lab", "project.html lab-FC1-project-1 (56-102); tests/labs/FC1/lab-FC1-project-1.py", "PASS",
        "run_labs --unit FC1: PASS (8/8) (" + S + "run_labs_FC1.out). Twin run under python -I -W error (" + S + "lab_project-1.out) prints the four expected lines, ending 'bond price (cents): 102775'."),
    row("proj-lab2-completion", "2.5 lab", "project.html lab-FC1-project-2 (104-150); tests/labs/FC1/lab-FC1-project-2.py", "PASS",
        "run_labs FC1: PASS (8/8) (" + S + "run_labs_FC1.out). Expected block equals output; tolerance 1e-6 relative gives about 0.10 cent on 102775.091033, matching the page text (coursekit.compare_output)."),
    row("proj-lab2-docstring", "1 prose vs output", "project.html line 107; tests/labs/FC1/lab-FC1-project-2.py docstring", "PASS",
        "Docstring line 1 'Rung 2 completion: the worked example, with two blanks for you to fill in.' matches the lab; the lab code carries exactly the two blanks ___ (exponent and trade cash flow), run in lab_project-2.out."),
    row("proj-lab3-fixtures", "2.5 lab + fixtures", "project.html lab-FC1-project-3 (196-276); tests/labs/FC1/lab-FC1-project-3.py", "PASS",
        "Re-ran the Lab 3 twin under python -I -W error (" + S + "lab_project-3.out, exit 0; run_labs_FC1.out PASS). Printed values: fixture B 11053 with exact 11052.6316; fixture C [(1, 5001), (2, 15002)]; rounding case 10278 vs 10277; fixture G 5001. Recomputed independently with Fraction: 210000/19 = 11052.631578..., 10277.509103..., 480.77 + 462.28 + 9334.46 terms (rounded 481+462+9334=10277)."),
    row("proj-prose-numbers", "1 numbers", "project.html lines 54, 58, 101, 176, 186-193, 198, 275", "PASS",
        "Recomputed with Fraction this round: 102775.091033 (line 58); 11052.6316 and 11053 (fixture B); 10277.509103 rounds to 10278 and term-by-term 10277 (fixture rounding); 5000.5 -> 5001; 1/2 -> 1. Each matches the page and the Lab 3 expected block."),
    row("proj-fixture-claims", "1 fixtures vs tests", "project.html line 275 vs grader/test_project.py", "PASS",
        "Mapped each claimed check to a test: fixture A events/price (test_bond_one_period_fixture_is_par_coupon_plus_face, test_bond_price_one_period_at_its_coupon_rate_is_par); B price (test_bond_price_negative_yield_is_above_the_undiscounted_value); C and D events (test_bond_half_cent_*); E (test_buyer_pays_cash_at_settlement, test_seller_receives_cash_at_settlement); F and G prices (test_bond_price_exact_half_*); rounding price (test_bond_price_hand_fixture_rounds_the_sum_once). Lab 3 note says G's and the rounding case's event lists are unchecked; grep confirms no list test for them."),
    row("proj-hours-arithmetic", "8 hours", "project.html section#budget lines 285-292; data-hours-project=20 (line 34)", "PASS",
        CARRY + "project.html section#budget. Re-derived: 1+2+5+4+2+3+3 = 20, equal to data-hours-project=20 (project.html line 34) and the stated total. The estimate is a design target (architect ruling), so the 30 % test is not applied."),
    row("proj-check-pages-dag", "2.9 structure", "course/modules/FC/FC1/*.html", "PASS",
        "check_pages --unit FC1: PASS (" + S + "check_pages_FC1_all.out). check_dag --unit FC1: PASS (" + S + "check_dag_FC1.out). Note: check_pages --page project applies lesson rules and reports 11 problems (" + S + "check_pages_project.out); the tool's full-unit run covers project.html as the project template and passes, so the page-filter output is not a defect."),
    row("proj-dag-closure", "2.9/DAG", "project.html lines 58 and 178", "PASS",
        CARRY + "project.html lines 58 and 178 (concept links 'present-value' and 'discount-factor' are in FC1's closure per check_dag: PASS)."),
    row("proj-notation", "NOTATION", "project.html; grader/*.py; tests/labs/FC1/lab-FC1-project-*.py; cards.json", "PASS",
        "Math on project.html is limited to t, y and (1+y)^-t, none registered in notation/notation.json (registered: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). Scan of the grader, labs and cards for these registered symbols returned 0 hits (" + S + "cards_scan.py; grep)."),
    row("proj-banned-phrases", "2.9 banned", "project.html; grader/*.py; lab twins; cards.json", "PASS",
        "check_pages --unit FC1: PASS (BANNED list, tools/check_pages.py lines 58-72, on visible prose). Grep over grader, cards and project labs for the same list and for process words (verifier, round, fragment, builder): only '...' in test_project.py line 295 (a number ellipsis in a docstring) and the word 'unimplemented' in a function name, neither a banned phrase."),
    row("proj-reading-list", "3 references", "project.html section#reading lines 320-327; references/references.json", "PASS",
        "verify_refs.py --offline: 560 entries, 0 problems (" + S + "verify_refs_offline.out). project.html states 'attributes no statement to either' (section#reading), and no attribution is made. Live Crossref run not performed (offline gate per the rule)."),
    row("proj-named-conditions", "2.6 conditions", "project.html Constraints lines 163-167; grader/test_project.py lines 192-232, 329-337, 373, 407-419", "PASS",
        "All eight named conditions are tested on both sides: periods 0,-1 refused, 1 accepted (test_bond_periods_*); face 0,-1 refused, 1 accepted; coupon -1 refused, 0 accepted; yield -10000 and -20000 refused, -9999 accepted; quantity 0,-1 refused, 1 accepted; price -1 refused, 0 accepted; side 0,2,-2,3,-3 refused, +1 and -1 accepted; settlement_day 0,-1 refused, 1 accepted. Verified by reading test_project.py lines 191-419."),
    row("proj-failure-messages", "2.6 messages", "grader/test_project.py lines 75-93, 534-557", "PASS",
        "Read lines 75-93 (must_raise, must_accept, checked_* messages) and 534-557 (_named_when_unimplemented). Messages name the property and the condition; none prints an expected value. The new test's message (line 252-262) prints only the periods count and the property."),
    row("proj-test-docstring", "2.6 docstrings", "grader/test_project.py lines 464-487 and 506-514", "PASS",
        "Read both ranges. Docstrings match their tests (silence and refusal tests list the inputs they run). The new test docstring (lines 252-258) is accurate: Bond(10000, 500, n) at 500 bps is par, checked by the exact sum."),
    row("proj-mutants-killed", "2.6 mutation", "ledgers/FC1/mutants/ (72 files); tools/mutate_graders.py --unit FC1 --seeds 0-9", "FAIL",
        "tools/mutate_graders.py --unit FC1 --seeds 0-9 (" + S + "mutate_FC1_s0-9_r12.out): 69/72 killed. Survivors: r11n01 (quantity 1001 refused) and r11n02 (coupon_bps 15000 refused), both hardening under the round-11 ruling because the page names no upper limit for quantity or coupon, and r12n03 (float discounting, rounds the float sum half up). r12n03 is not hardening: the page states 'computed from exact fractions and rounded once' (project.html Conventions, Money bullet) and the wrong cent it gives is on a valid input (1704285, 179, 1, 496).",
        "Kill r12n03: " + MUT_FIX),
    row("proj-new-mutants-r10", "2.6 mutation", "ledgers/FC1/mutants/r10n01..r10n04", "PASS",
        "Re-run in " + S + "mutate_FC1_s0-9_r12.out: r10n01..r10n04 each KILLED."),
    row("proj-mutant-set-d-and-c", "2.6 mutation", "ledgers/FC1/mutants/ c*, r*, v*, d*, f*, m*", "PASS",
        "Re-run of all 66 earlier files: each KILLED on seeds 0-9 (" + S + "mutate_FC1_s0-9_r12.out)."),
    row("proj-silence-coverage", "2.6 silence", "project.html line 163; grader/test_project.py lines 464-505", "PASS",
        "Read test_project.py 464-505 (the silence test lists 14 runs, each checked with capsys) and project.html line 163 ('no function prints or warns'). Consistent."),
    row("proj-lint-types", "gate", "course/modules/FC/FC1; tests/labs/FC1; repo mypy", "PASS",
        "ruff check course/modules/FC/FC1 tests/labs/FC1: 'All checks passed!'; ruff format --check: '12 files already formatted'; mypy --no-incremental: 'Success: no issues found in 229 source files' (" + S + "ruff_check_FC1.out, mypy_repo.out)."),
    row("proj-privacy-claim", "1 prose", "project.html footer line 340", "PASS",
        CARRY + "project.html footer. The claim 'nothing you write leaves it' is consistent with the browser grader; no network request appears in page_smoke (no external requests)."),
    row("proj-reference-deployment", "repo-wide", "course/modules/FC/FC1/grader/reference.py (git-tracked); BLUEPRINT.md lines 400-401", "PASS",
        "Not failed in this slice, per the workflow instruction that this repo-wide matter is recorded for the user. Still true at the pin: 'git ls-files course/modules/FC/FC1/grader' lists reference.py, and BLUEPRINT.md lines 400-401 require deployment to exclude it. Recorded in notes for the user."),
    row("cards-scan-98", "2.7 scan", "course/modules/FC/FC1/cards.json (118 cards)", "PASS",
        "cards_scan.py (" + S + "cards_scan.py): 118 cards, ids FC1-c001..c118 unique, no duplicate fronts or backs, every graded card (54 with grade) has a basis when C (15 C), 64 ungraded cards are definitions, theorems and misconceptions per BUILDER_RULES 7. Ids are not in file order at c099/c108 and c101/c109 (cosmetic, not a rule). Every card was read; lesson agreement was spot-checked for the changed and sampled cards."),
    row("cards-numbers", "2.7/2.2 numbers", "cards.json vs L01-L05 text; c010, c011, c014, c015, c016, c037, c043, c052-c054, c061, c082-c086, c092, c093, c095-c098", "PASS",
        "Lab twins L01-L05 run under python -I -W error (" + S + "lab_L01-1.out .. lab_L05-1.out) and their printed values match: c092 181790 and 686189 (Lab 1 Part C); c093 -50 dollars (Part D); c082 2172960; c083 Friday 2026-10-30 (2026-10-28 is Wednesday, offset 2); c084 0.209 from 14282414/68398886 = 0.20881; c097 -545; c098 3455 = 4000 - 545; c052 4000; c053 4000; c029, c095, c096 counts 3/3/2/2/2, 6/6, 4/8. Closed forms: 1000(1-0.9^11)/0.1 = 6861.894 (c010); 1000/0.55 = 1818.18 (c011)."),
    row("cards-labels-and-hypotheses", "2.7 labels", "cards.json backs (all); c013 vs L01.html lines 155-156", "PASS",
        "cards_scan.py: every card with grade C has a basis (none missing); no card carries a grade outside T/C. c013 back ('nonnegative iff lambda <= E') matches Proposition 4.1 in L01.html lines 155-156 (read this round)."),
    row("cards-hypothesis-c036", "2.7 hypothesis", "cards.json FC1-c036 back; L03.html Definition 1.2 (lines 61-62)", "PASS",
        CARRY + "cards.json FC1-c036; L03.html Definition 1.2 (lines 61-62 region) states the convention a = m + h, b = m - h with whole cents, which the card carries."),
    row("cards-misconception-refs", "2.7 misconception", "cards.json c070, c071 backs; L04.html lines 372, 376", "PASS",
        CARRY + "cards.json FC1-c070 and FC1-c071; L04.html misconception items at lines 372 and 376."),
    row("cards-grades-and-basis", "2.7 grades", "cards.json FC1-c092 (grade T, basis 'Lab 1, Part C (typed-in parameters)'); c054 (C); c014, c029, c091, c093, c095, c096", "PASS",
        "FC1-c092 changed this round from C to T. Its value is an exact closed-form computation with typed-in parameters (stage recurrence D_t = 1000 * 0.45^t, sum 181790 cents; full redeposit 686189 cents), matching Proposition 3.1 and the round-11 ruling that typed-in deterministic results are T. Lab 1 is not SIMULATED. c054 (C, basis given) and the other rows unchanged since round 11."),
    row("cards-lesson-agreement", "2.7 agreement", "cards.json c070, c071, c082, c092, c115-c118 vs L02-L05", "PASS",
        "c092 re-verified against L01 Part C output (" + S + "lab_L01-1.out). c082 and c083 re-verified against L05 twin output (lab_L05-1.out: 2172960; Friday 2026-10-30). c070, c071 and c115-c118 carried from round 11 (cards.json lines unchanged, byte-identical since 625d936)."),
    row("cards-notation-Q", "NOTATION", "cards.json (grep for bare Q and V_b)", "PASS",
        "cards_scan.py pattern scan: bare \\bQ\\b hits 0; V_b hits 0; \\bcard\\b hits 0 (" + S + "cards_scan.py)."),
    row("proj-new-mutants-r11", "2.6 mutation", "ledgers/FC1/mutants/r11n01..r11n03", "PASS",
        "Copied the three round-11 mutants into ledgers/FC1/mutants/ (they are not in the pin). r11n03 (exponent capped at 12) is now KILLED by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period (seed 0). r11n01 and r11n02 survive; under the round-11 ruling they are hardening, not FAIL, because the page names no upper bound for quantity or coupon_bps (" + S + "mutate_FC1_s0-9_r12.out). Suggested test: quantity 1001 and coupon_bps 15000 accepted."),
    row("proj-new-mutants-r12", "2.6 mutation (new)", "ledgers/FC1/mutants/r12n01..r12n03", "FAIL",
        "Wrote three new student-error mutants from the reference (" + S + "make_mutants.py). r12n01 (face as a second same-period event) KILLED by test_bond_has_one_event_per_period_numbered_one_to_n; r12n02 (exponent is list position) KILLED by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period; r12n03 (float discounting, half-up on float sum) SURVIVED all seeds 0-9 and is a valid-input cent error (" + S + "exact_half_probe.py).",
        "Add the exact-half fixture: " + MUT_FIX),
]

mutants = []
for line in (OUT / "mutate_FC1_s0-9_r12.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    mutants.append({
        "id": fname[:-3],
        "description": desc,
        "file": f"ledgers/FC1/mutants/{fname}",
        "killed_by": None if killed.strip() == "None" else killed.strip(),
    })

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 12 (did not build FC1)",
    "pin": PIN,
    "base": BASE,
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC12-FC1-c",
    "scratch": "/tmp/fc1c12_probe, /tmp/fc1c12_cx, /tmp/fc1c12_alts.*, /tmp/fc1c12_lab.*",
    "verified_at": "2026-10-29T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "Repo-wide, not failed (per workflow instruction): course/modules/FC/FC1/grader/reference.py is git-tracked and BLUEPRINT.md lines 400-401 require deployment to exclude it; nothing enforces the exclusion.",
        "Curriculum scope conflict for the user or architect: curriculum/02-economics-finance-core.yaml lines 388-395 (project brief) names bonds, futures, swaps and options; the binding architect decision and project.html cover cash instruments only. Not edited here (generated source)."
    ],
    "freshness_flags": [],
    "notes": (
        "Round 12 on 460b696 (delta 625d936..460b696 in slice: project.html line 168; grader/test_project.py new test at lines 252-262; cards.json c016, c030, c046, c069, c092). "
        "New findings: (1) r12n03 float-discounting mutant survives the suite and gives a wrong cent on a valid input, Bond(1704285, 179, 1) at 496 bps, exact value 1652812.5 (grader gap; page convention 'computed from exact fractions'); "
        "(2) alternative a5 is labelled correct but returns 1652812 on the same input, so the alternatives row is FAIL. Hardening, not FAIL: r11n01 and r11n02 (no upper bound named by the page). "
        "Re-run this round: run_graders 50/50; alternatives and reference 0 failing seeds of 20 (62 collected); run_labs 8/8; check_pages (unit), check_dag, check_projects, page_smoke (project); ruff check and format; mypy --no-incremental; verify_refs --offline; pytest test_page_checks and test_memo_exemplars; mutate_graders 69/72 killed. "
        "Verifier checks of this round: every changed hunk read (project.html line 168; test_project.py 252-262; the five cards). "
        "Not checked: a live verify_refs run (offline only); the full pytest suite and render_curriculum, build_site --check and fetch_data --check (no curriculum, data or site input changed in this slice); Pyodide run of the new mutants (local only); line-by-line re-read of every card against lessons L01-L05 beyond the changed and sampled cards; hours not re-estimated (architect ruling). "
        "Cosmetic: card ids are out of sequence at c099/c108 and c101/c109."
    ),
    "summary": "FC1-c round 12: verdict FAIL. Rows: 42 total. FAIL: proj-mutants-killed and proj-new-mutants-r12 (survivor r12n03: float discounting gives a wrong cent on valid input Bond(1704285,179,1) at 496 bps, exact 1652812.5 -> 1652813; grader lacks an exact-half case that float misses), proj-alternatives-five (alternative a5 is mislabelled correct and gives 1652812). Hardening, not FAIL: r11n01, r11n02. Cleared: r11n03 killed by the new 13-15 period test; round-11 cards and project wording rows re-verified. Mutants: 69 of 72 killed."
}

(OUT.parents[1] / "FC1-c.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
