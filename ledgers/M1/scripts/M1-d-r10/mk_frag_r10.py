"""Builds the round-10 M1-d fragment (ledgers/M1/M1-d.json) from the round-9 rows and this round's command output (run with python -I)."""
import json
import re
import sys

CHECKOUT = "/tmp/verify10-M1-d"
prev = json.load(open("/tmp/fanout-frags/M1-d.round9.json", encoding="utf-8"))
mut_out = open(f"{CHECKOUT}/ledgers/M1/scripts/M1-d-r10/mutate_r10_all.out", encoding="utf-8").read().splitlines()

mutants = []
for line in mut_out:
    m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, stem, desc, killed = m.groups()
    mid = stem.split("_")[0] if not stem.startswith("r10_") else "_".join(stem.split("_")[:2])
    killed_by = None if killed.strip() == "None" or status == "SURVIVED" else killed.strip()
    mutants.append({
        "id": mid,
        "file": f"ledgers/M1/mutants/{stem}.py",
        "description": desc.strip(),
        "killed_by": killed_by,
        "run": "tools/mutate_graders.py --unit M1 --seeds 0-9 (round 10, checkout af08ad1 plus the five new mutants): " + status,
    })

ROUND10 = "Re-verified round 10 (checkout af08ad1): "
rows = {r["id"]: r for r in prev["rows"]}

def carry(rid, files):
    r = dict(rows[rid])
    r["evidence"] = f"Carried from round 9 ({files} byte-identical since the previous pin 96dd532): " + r["evidence"]
    rows[rid] = r

def upd(rid, status, evidence, location=None, fix=None):
    r = dict(rows[rid])
    r["status"] = status
    r["evidence"] = evidence
    if location:
        r["location"] = location
    if fix:
        r["fix"] = fix
    rows[rid] = r

G = "course/modules/M/M1/grader/test_project.py"
P = "course/modules/M/M1/project.html"

# Rows that changed status or subject this round
upd("proj-grader-mutation-suite", "FAIL",
    ROUND10 + "tools/mutate_graders.py --unit M1 --seeds 0-9 on 68 mutants (m01 to m58 and r10_01 to r10_10): 67 KILLED, 1 SURVIVED (m57_term_capped_at_480_months). Output in ledgers/M1/scripts/M1-d-r10/mutate_r10_all.out. Mutant m57 is listed in the new mutant row proj-mutant-m57-term-cap-480.",
    location="ledgers/M1/mutants/ (68 files m01 to m58 and r10_01 to r10_10); tools/mutate_graders.py",
    fix="Add a grader test that a loan of 481 or more months (for example 1200 months) is accepted and its schedule closes to zero; then re-run mutate_graders M1 and require every mutant killed.")
upd("proj-mutant-m51-tiny-rate-cutoff-1e-8", "PASS",
    ROUND10 + "mutate_graders M1 --seeds 0-9: m51 KILLED by test_level_payment_below_the_old_cutoffs_is_exact (seed 0). Test at " + G + " lines 352-362 is new in af08ad1; arithmetic recomputed in ledgers/M1/scripts/M1-d-r10/arith_r10.py: exact payment 36934.50000000427 -> 36935; loan over months 36934.4972 rounds to 36934.",
    location=G + " lines 352-362; ledgers/M1/mutants/m51_tiny_rate_cutoff_1e-8_treated_as_zero.py")
upd("proj-mutant-m53-term-cap-360", "PASS",
    ROUND10 + "mutate_graders M1 --seeds 0-9: m53 KILLED by test_level_payment_accepts_a_term_above_360_months (seed 0); the 480-month case is exact (482 cents, recomputed in arith_r10.py).",
    location=G + " lines 364-374; ledgers/M1/mutants/m53_term_capped_at_360_months.py")
upd("proj-grader-tie-comment-digits", "PASS",
    ROUND10 + "the comment now reads 499999999999.499999999999 cents; recomputed: 499999999999 x (1 + 1e-12) = 499999999999.499999999999 (arith_r10.py, Decimal, 40 digits). Comment at " + G + " lines 395-396.",
    location=G + " lines 395-396 (comment in the tie test parametrization)")
upd("proj-exemplar-intro-claim", "PASS",
    ROUND10 + "the intro sentence (" + P + " line 339) now says the monthly rate is written as 0.045/12 because the run does not print it. Checked against the run output of Lab 3 (run_labs M1 PASS, 11/11): the printed lines contain no monthly rate; the printed annuity factor 179.910321841 and due factor 180.584985548 are the values the exemplars quote at 0.045/12. Lab 3 hypothesis at project.html line 218 states the monthly rate; the printed output (run_labs) does not.",
    location=P + " line 339")
upd("proj-exemplar-B-setup-claim", "PASS",
    ROUND10 + "line 422 (Exemplar B, Setup and conventions): the monthly rate is written 0.045/12, not printed by run_report.py (Lab 3 output has no rate line); the four factor function names match project.html line 166-177 and the reference; the suite's per-row schedule check is grader test_schedule_matches_the_exact_schedule_row_for_row (seed 0 PASS).",
    location=P + " line 422")
upd("proj-exemplar-B-level4-claims", "FAIL",
    ROUND10 + "line 407 (Exemplar B official scoring) says 'the cent bound is derived from the printed run'. The bound 300(1+0.00375)^300 + 1 = 923.1228 is printed by Lab 3 (run_labs PASS), but it is derived in A4 (" + P + " lines 468-476) from the recursion and the inputs n and i, not from the run's output. The stated basis is wrong. The other claims of line 407 hold: every number in the report is a loan input, a symbol, or printed by the run with its unit.",
    location=P + " line 407 (exemplar-b data-reveal verdict)",
    fix="Replace 'and the cent bound is derived from the printed run' with 'and the cent bound is derived in A4 from the rule and the loan inputs, its value 923.1228 printed by the run'.")
upd("proj-grader-alternatives", "PASS",
    ROUND10 + "ran 13 engines against the current grader, seeds 0-49 (ledgers/M1/scripts/M1-d-r10/run_engine.sh). Correct and passing 50/50: reference, reference_r9, alt_fraction_sum_v6, alt_expm1_cutoff_v6, alt_balance_closed_form_v6, alt_r9_cutoff_1e15, alt_r10_fraction_sum, alt_r10_expm1_log1p, alt_r10_direct_sum_closed_payment, alt_r10_tie_explicit. Wrong and failing: witness_int_zero_rate (int 0 at zero rate; test_closed_forms_return_floats, spec 'The closed forms return floats' at project.html line 170); alt_fraction_binary_v6 (binary float rate, not the decimal as written; spec line 170); alt_decimal_v6 and alt_r9_decimal60 (Decimal at prec 28 and 60 gives 100.4999... for 100 cents at 6 %, one month, so the tie rounds down to 100; exact value 201/2 rounds to 101; spec line 170 requires exact rational arithmetic); alt_float_epsilon_v6 (binary float at tiny rates; spec line 170). No over-constraint witness found.",
    location="ledgers/M1/scripts/M1-d-r10/run_engine.sh; ledgers/M1/scripts/M1-d-r9/alts_r8/; ledgers/M1/scripts/M1-d-r10/alt_r10_*.py")

upd("proj-grader-minus-one-docstring-arithmetic", "FAIL", "", location=G + " lines 219-223 (test_annuity_accepts_a_rate_just_above_minus_one docstring)", fix="Change the docstring's closed form to (1 - 10^9) / (-0.999) (equal to 1001001000), or (10^9 - 1) / 0.999.") if False else None
rows["proj-grader-minus-one-docstring-arithmetic"] = {
    "id": "proj-grader-minus-one-docstring-arithmetic",
    "check": "2.5-grader",
    "location": G + " lines 219-223 (docstring of test_annuity_accepts_a_rate_just_above_minus_one)",
    "status": "FAIL",
    "evidence": ROUND10 + "the docstring says 'the closed form (1 - 10^-9) / (-0.999) gives the same value' as 1001001000. Computed in arith_r10.py: (1 - 1e-9)/(-0.999) = -1.001001, not 1001001000; the correct closed form is (1 - (1+r)^-3)/r = (1 - 10^9)/(-0.999) = 1001000999.9999974 (float). The test assertion itself passes on the reference, so only the learner-facing sentence is wrong.",
    "fix": "Replace the expression in the docstring by (1 - 10^9) / (-0.999), which is 1001001000 (or 10^9 - 1 over 0.999).",
}
rows["proj-mutant-m57-term-cap-480"] = {
    "id": "proj-mutant-m57-term-cap-480",
    "check": "2.6-mutation",
    "location": "ledgers/M1/mutants/m57_term_capped_at_480_months.py; " + P + " line 177 (the term has 'a whole number of months of one or more' as its only condition); " + G + " lines 364-374 (docstring: 'no upper limit')",
    "status": "FAIL",
    "evidence": ROUND10 + "a new student-error mutant that refuses a term above 480 months survives mutate_graders M1 --seeds 0-9 (the only survivor). No test calls level_payment_cents or amortization_schedule with more than 480 months, so the cap is not detected. The spec at project.html line 177 says the term is invalid only when it is not a whole number of months of one or more, and the grader docstring at line 365 says 'no upper limit'.",
    "fix": "Add a grader test that a 1200-month loan (or any term above 480) is accepted, that its payment is the exact value, and that its schedule has 1200 rows and closes to zero; then re-run mutate_graders M1 and require all mutants killed.",
}
rows["proj-mutants-m54-m58-new"] = {
    "id": "proj-mutants-m54-m58-new",
    "check": "2.6-mutation",
    "location": "ledgers/M1/mutants/m54_growing_perpetuity_refuses_negative_growth.py, m55_perpetuity_refuses_rates_below_a_small_floor.py, m56_schedule_interest_tie_rounds_down.py, m58_annuity_refuses_rates_below_minus_half.py",
    "status": "PASS",
    "evidence": ROUND10 + "five new verifier mutants written with ledgers/M1/scripts/M1-d-r10/mk_mut_r10d.py. KILLED: m54 (test_growing_perpetuity_factor_matches_one_over_rate_minus_growth), m55 (test_perpetuity_accepts_a_tiny_positive_rate), m56 (test_schedule_interest_tie_goes_up), m58 (test_annuity_factor_accepts_a_negative_rate_above_minus_one[-0.5-3]). m57 SURVIVED: see proj-mutant-m57-term-cap-480.",
}
rows["proj-alt-correct-implementations-r10"] = {
    "id": "proj-alt-correct-implementations-r10",
    "check": "2.5-grader",
    "location": "ledgers/M1/scripts/M1-d-r10/alt_r10_expm1_log1p.py; alt_r10_direct_sum_closed_payment.py; alt_r10_tie_explicit.py; ledgers/M1/scripts/M1-d-r10/alt_r10_fraction_sum.py (committed in af08ad1)",
    "status": "PASS",
    "evidence": ROUND10 + "four new correct implementations with different cutoffs and algorithms (log1p/expm1 with no cutoff; direct summation of discount factors with the closed payment P i (1+i)^n / ((1+i)^n - 1); an explicit integer tie test; exact Fraction sum) each pass seeds 0-49 under the browser pytest flags (run_engine.sh). Over-constraint: none found.",
}
rows["proj-grader-collect-count"] = {
    "id": "proj-grader-collect-count",
    "check": "2.5-grader",
    "location": G + "; " + P + " line 164 ('runs 138 checks')",
    "status": "PASS",
    "evidence": ROUND10 + "pytest --collect-only on the grader copy with -W error --assert=plain prints '138 tests collected'; the page says 138. QF_SEED=0 run: 138 passed.",
}
rows["proj-commands-gate-r10"] = {
    "id": "proj-commands-gate-r10",
    "check": "2.3-gates",
    "location": "tools/check_pages.py --unit M1; tools/check_projects.py --unit M1; tools/check_dag.py --unit M1; tools/run_labs.py --unit M1; tools/verify_refs.py --offline; tools/page_smoke.py --unit M1 --pages project.html --skip-sweep; ruff check and ruff format --check on the grader; mypy --no-incremental (project-wide)",
    "status": "PASS",
    "evidence": ROUND10 + "check_pages M1: PASS; check_projects M1: PASS; check_dag M1: PASS; run_labs M1: PASS (11/11); verify_refs --offline: 560 entries, 0 problems; page_smoke M1 project.html: PASS; ruff check: All checks passed; ruff format --check: 4 files already formatted; mypy --no-incremental: Success, no issues found in 153 source files. Not run: verify_refs live (no citation changed).",
}
rows["proj-grader-run-graders-r10"] = {
    "id": "proj-grader-run-graders-r10",
    "check": "2.5-grader",
    "location": "tools/run_graders.py --unit M1 --seeds 0-49 (output ledgers/M1/scripts/M1-d-r10/run_graders_r10.out)",
    "status": "PASS",
    "evidence": ROUND10 + "run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s); the starter fails the suite; mypy --strict clean for reference, starter and instance.",
}
rows["proj-spec-65-checks"] = dict(rows["proj-spec-65-checks"], evidence=ROUND10 + "page line 164 says 'runs 138 checks'; collect-only prints 138 (see proj-grader-collect-count). The change from 105 to 138 is the new tests; the claim list in that sentence (closed forms, finite identities, schedule row for row, invariants, zero-rate, invalid inputs, booleans, purity) names tests that exist in " + G + ".", location=P + " line 164")
rows["proj-spec-claims-mapped"] = dict(rows["proj-spec-claims-mapped"], evidence=ROUND10 + "line 164 claims are each mapped to a test in " + G + " (closed forms, invariants, zero rate, invalid inputs, booleans, purity); re-read this round.")
rows["proj-grader-perpetuity-rate-test"] = dict(rows["proj-grader-perpetuity-rate-test"], evidence=ROUND10 + "the new test test_perpetuity_accepts_a_tiny_positive_rate (" + G + ") passes on the reference (1e12 within 1e-9 relative) and the mutants m50, m08, r10_03 and m55 are KILLED. Recomputed: 1/1e-12 = 1e12.")
rows["proj-grader-tiny-rate-test-arithmetic"] = dict(rows["proj-grader-tiny-rate-test-arithmetic"], evidence=ROUND10 + "the tiny-rate test body is unchanged; arith_r10.py recomputes its inputs; the suite passes on the reference (138 passed) and mutants m48, m52 are KILLED.")
rows["proj-grader-messages-no-leak"] = dict(rows["proj-grader-messages-no-leak"], evidence=ROUND10 + "read every new assertion message in the af08ad1 diff of " + G + ": none prints or implies an expected numeric value; m36 (print on invalid term) KILLED by test_functions_do_not_print_or_warn.")
rows["proj-grader-lint-types"] = dict(rows["proj-grader-lint-types"], evidence=ROUND10 + "ruff check and ruff format --check clean on course/modules/M/M1/grader; run_graders M1 mypy --strict clean for reference, starter and instance; the direct mypy run on test_project.py reports only missing modules annuity_engine and instance (not in the target list; the tool passes mypy on those files with the solution path).")
rows["proj-numbers-recomputed"] = dict(rows["proj-numbers-recomputed"], evidence=ROUND10 + "recomputed in arith_r10.py: Lab 3 bound 923.1228; tail 3.0706e-4 printed as 3.071e-04; least N 345 and error at 344 1.0278e-6; effective annual (1+0.045/12)^12 = 1.04594 > 1.045; nominal payment 166749.74 and effective-rate payment 165217.05 (direction: nominal larger).")
rows["proj-exemplar-B-closed-forms-and-schedule"] = dict(rows["proj-exemplar-B-closed-forms-and-schedule"], evidence=ROUND10 + "lines 431-456 re-read; each number recomputed (arith_r10.py) or printed by Lab 3 (run_labs PASS). The tolerance sentence matches " + G + " close() (max(1,|b|) relative) and the exact == checks at zero rate (lines 186-187, 207).")
rows["proj-exemplar-length-and-summary"] = dict(rows["proj-exemplar-length-and-summary"], evidence=ROUND10 + "Exemplar B summary is 48 words (under 80), recounted from project.html line 411 with the same regex.")
rows["proj-banned-phrase-about"] = dict(rows["proj-banned-phrase-about"], evidence=ROUND10 + "the three 'about' occurrences in project.html (lines 332, 388, 457) are 'evidence about the borrower/loan' and not a banned quantity phrase; no 'roughly', 'about 6%', or 'historically' in the file.")
rows["proj-calibration-blind"] = dict(rows["proj-calibration-blind"], evidence=ROUND10 + "exemplar article data-level and data-scores attributes unchanged; the annotations and verdicts were re-read in full, lines 338-487.")
rows["proj-links-anchors"] = dict(rows["proj-links-anchors"], evidence=ROUND10 + "check_pages M1 PASS and page_smoke project.html PASS (no failed requests, no console errors) on af08ad1; anchors #rubric, #self-assessment, #exemplars, #brief unchanged.")
rows["cards-L01"] = dict(rows["cards-L01"], evidence=ROUND10 + "M1-c017 changed: front and back now ask only for the least n (40); 'n = 40' and the first-failure sentence are in L01.html line 306 and line 309 (Lab 1 prints 'least n in 1 to 50 ... not prime: 40'). The removed value 1681 is still in the lesson and was dropped from the card; the card is accurate. Other L01 cards carried.")
rows["cards-L08"] = dict(rows["cards-L08"], evidence=ROUND10 + "M1-c143 front no longer asks for the month; back '3.41 CU.' matches L08.html line 321 ('3.41, at month 359'). New M1-c169 asks for the month: 'Month 359.' matches the same line and the table at L08.html line 478. Both cards grade C with basis 'Lab 1, Part B (illustrative input, not data)', which the lesson uses. Other L08 cards carried.")
rows["cards-numbers-recomputed"] = dict(rows["cards-numbers-recomputed"], evidence=ROUND10 + "re-scanned all 169 cards: every back number appears in its lesson, digit-grouped or as LaTeX (1,648,721.27 in L04/L05; 783,526.17 in L05 as 783{,}526.17); the changed cards c017, c143 and c169 are checked against their lessons (see cards-L01 and cards-L08).")
rows["cards-duplicate-scan"] = dict(rows["cards-duplicate-scan"], evidence=ROUND10 + "169 ids, no duplicate id, no duplicate front (case-insensitive exact match) across M1 cards.json.")
rows["cards-process-and-banned"] = dict(rows["cards-process-and-banned"], evidence=ROUND10 + "grep of project.html and cards.json for build, builder, round, verifier, REQUESTS and unit report returns no match; no banned phrase in the changed cards.")

# Rows whose round-9 evidence said "re-run this round" are re-verified here, not carried
for rid in ["proj-mutant-m47-m49", "proj-mutant-m48-small-rate-cutoff", "proj-mutant-m50-perpetuity-rate-above-one", "proj-mutant-m52-float-small-rate"]:
    upd(rid, "PASS", ROUND10 + "mutate_graders M1 --seeds 0-9 (round 10, output ledgers/M1/scripts/M1-d-r10/mutate_r10_all.out): " + {
        "proj-mutant-m47-m49": "m47 and m49 KILLED.",
        "proj-mutant-m48-small-rate-cutoff": "m48 KILLED by test_level_payment_at_a_tiny_rate_is_exact (seed 0).",
        "proj-mutant-m50-perpetuity-rate-above-one": "m50 KILLED by test_perpetuity_factor_accepts_a_rate_of_one_or_more (seed 0).",
        "proj-mutant-m52-float-small-rate": "m52 KILLED by test_level_payment_below_the_old_cutoffs_is_exact (seed 0).",
    }[rid])
upd("proj-grader-reference-50-seeds", "PASS", ROUND10 + "tools/run_graders.py --unit M1 --seeds 0-49: 'run_graders M1: PASS (reference 50/50 seeds, slowest 0.2 s)' (ledgers/M1/scripts/M1-d-r10/run_graders_r10.out). Also QF_SEED=0 pytest on the reference copy: 138 passed.")
upd("proj-closed-forms-float-test", "PASS", ROUND10 + "witness_int_zero_rate (int 0 at zero rate) FAILS test_closed_forms_return_floats on seeds 0-49 (run_engine.sh); the reference passes 50/50. Lines 160-165 of " + G + " unchanged in the delta.")
for rid, what in [("proj-lab1-run", "lab-M1-project-1"), ("proj-lab2-completion", "lab-M1-project-2"), ("proj-lab3-reference", "lab-M1-project-3")]:
    upd(rid, "PASS", ROUND10 + "tools/run_labs.py --unit M1: PASS (11/11) including " + what + "; the page's lab code and expected blocks in lines 55-149 are byte-identical to 96dd532 (the delta hunks start at line 161), and the Lab 3 block (lines 218-307) changed only in the hypothesis sentence, which the run confirms.")
upd("cards-L01", "PASS", rows["cards-L01"]["evidence"])  # kept as updated above
# Carry the rest (subjects not in the af08ad1 delta) with the round-9 evidence and the prefix
carry_map = {
    "proj-spec-names-and-conventions": "course/modules/M/M1/project.html lines 160 and 170",
    "proj-grader-stdlib-and-purity": "course/modules/M/M1/grader/test_project.py purity tests",
    "proj-grader-instances": "course/modules/M/M1/grader/instance.py",
    "proj-grader-instance-docstring-growth": "course/modules/M/M1/grader/instance.py",
    "proj-grader-browser-and-local": "course/modules/M/M1/project.html 'Running the suite locally' section",
    "proj-lab-interpretations-no-overreach": "course/modules/M/M1/project.html Lab interpretations lines 306 and 309 (unchanged hunks)",
    "proj-l04-cited-numbers": "course/modules/M/M1/L04.html cited numbers",
    "proj-hours": "course/modules/M/M1/project.html 'Time budget' table lines 183-201",
    "proj-ladder-rungs": "course/modules/M/M1/project.html lines 1-30",
    "proj-atlas-studio-data": "course/modules/M/M1/project.html and grader instance",
    "proj-cite-velleman": "course/modules/M/M1/project.html 'Reading' section, references/references.json key velleman2019prove (tools/verify_refs.py --offline 560 entries, 0 problems)",
    "proj-section-references": "course/modules/M/M1/project.html brief section",
    "proj-factor-tolerance-claim": "course/modules/M/M1/grader/test_project.py close() (line 97-98)",
    "proj-invalid-input-claim": "course/modules/M/M1/project.html lines 175-178",
    "proj-invalid-input-any-other-value": "course/modules/M/M1/project.html lines 175-178",
    "proj-tie-rule-enforced": "course/modules/M/M1/grader/test_project.py tie tests (unchanged bodies)",
    "proj-tie-interest-docstring": "course/modules/M/M1/grader/test_project.py test_schedule_interest_tie_goes_up",
    "proj-rubric-shape": "course/modules/M/M1/project.html rubric table lines 300-335",
    "proj-rubric-descriptor-observable": "course/modules/M/M1/project.html rubric table lines 300-335",
    "proj-exemplar-intro-claim": None,
    "proj-grader-over-constraint-unnamed": "course/modules/M/M1/grader/test_project.py lines 166-172 (lines 1-215 unchanged in the delta)",
    "cards-L02": "course/modules/M/M1/cards.json entries M1-c021 to M1-c041 (unchanged; only M1-c017, M1-c143, M1-c169 changed)",
    "cards-L03": "course/modules/M/M1/cards.json entries M1-c042 to M1-c063 (unchanged)",
    "cards-L04": "course/modules/M/M1/cards.json entries M1-c064 to M1-c076 (unchanged)",
    "cards-L05": "course/modules/M/M1/cards.json entries M1-c077 to M1-c092 (unchanged)",
    "cards-L06": "course/modules/M/M1/cards.json entries M1-c093 to M1-c103 (unchanged)",
    "cards-L07": "course/modules/M/M1/cards.json entries M1-c104 and M1-c164 (unchanged)",
}
for rid, files in carry_map.items():
    if files and rid in rows and rows[rid]["status"] == "PASS" and not rows[rid]["evidence"].startswith(ROUND10):
        carry(rid, files)

rows_out = [rows[r["id"]] for r in prev["rows"]]
for rid in ["proj-grader-minus-one-docstring-arithmetic", "proj-mutant-m57-term-cap-480", "proj-mutants-m54-m58-new",
            "proj-alt-correct-implementations-r10", "proj-grader-collect-count", "proj-commands-gate-r10",
            "proj-grader-run-graders-r10"]:
    rows_out.append(rows[rid])

# Ensure every FAIL row has a fix
for r in rows_out:
    if r["status"] != "PASS" and not r.get("fix"):
        raise SystemExit("missing fix: " + r["id"])

counts = {"PASS": 0, "FAIL": 0}
for r in rows_out:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m["killed_by"])
fragment = {
    "unit": "M1",
    "slice": "M1-d",
    "round": 10,
    "round_note": "round 10 (independent re-verification of slice M1-d at af08ad1). Delta 96dd532..af08ad1 read in full for project.html (hunks at lines 164, 339, 407, 422, 430, 442, 454), grader/test_project.py (new tests at lines 219-262, 352-374, 414-429, 600-608, 654-694 and the comment at 395), cards.json (c017, c143 changed; c169 new). Previous non-PASS rows re-verified; rows whose subject changed re-verified; other rows carried with the round-9 prefix when byte-identical. Full project.html read line by line. Mutants: 63 from earlier rounds re-run plus five new (m54 to m58); new survivor m57.",
    "verifier": "Claude Haiku 5.5 (independent verifier, slice M1-d, round 10; did not build M1; no shared context with builders)",
    "pin": "af08ad1 (detached HEAD of /tmp/verify10-M1-d)",
    "base": "96dd532 (round-9 pin, used for the delta)",
    "previous_ledger": "/tmp/fanout-frags/M1-d.round9.json (context only)",
    "checkout": CHECKOUT,
    "scratch": "/tmp/m1-v10/d/",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows_out,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Commands run at af08ad1: run_graders M1 --seeds 0-49 (PASS 50/50); mutate_graders M1 --seeds 0-9 (67/68 killed, m57 survived); check_pages, check_projects, check_dag, run_labs (11/11), verify_refs --offline (560 entries, 0 problems) and page_smoke project.html for M1 all PASS; ruff check and format check and project-wide mypy PASS; pytest collect of the grader copy 138.",
        "Alternative engines: 13 run seeds 0-49 against the af08ad1 grader (ledgers/M1/scripts/M1-d-r10/run_engine.sh).",
        "Not checked: verify_refs live (no citation changed); Pyodide browser run of the grader (the local run uses the same file and pytest flags); page_smoke figure sweep (the project page has no live figures).",
        "Hours are not judged on pace (architect ruling); the arithmetic 2+3+8+7+6+4 = 30 equals data-hours-project 30.",
        "Previous mutant file names in ledgers/M1/mutants/ end in .py; the r9 fragment wrote '.py.py' in its file field, this fragment uses the real file names.",
        "The committed r10 scripts in ledgers/M1/scripts/M1-d-r10/ (alt_r10_fraction_sum.py, mk_mut_r10.py, mutate_r10.txt, run_seeds.sh) were committed by the builder in af08ad1 and were not authored by this verifier; this verifier added run_engine.sh, alt_r10_expm1_log1p.py, alt_r10_direct_sum_closed_payment.py, alt_r10_tie_explicit.py, mk_mut_r10d.py, arith_r10.py and the output files.",
    ],
    "summary": f"M1-d round 10 at af08ad1: {len(rows_out)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL. FAIL rows: proj-grader-mutation-suite, proj-mutant-m57-term-cap-480, proj-exemplar-B-level4-claims, proj-grader-minus-one-docstring-arithmetic. Mutants: {len(mutants)} ({killed} killed, 1 survived: m57).",
}
json.dump(fragment, open(f"{CHECKOUT}/ledgers/M1/M1-d.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows_out), counts, "mutants", len(mutants), killed)
