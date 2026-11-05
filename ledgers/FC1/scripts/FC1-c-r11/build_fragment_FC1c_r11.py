"""Build the round-11 fragment ledgers/FC1/FC1-c.json for FC1 slice c (verifier output, not hand-typed verdicts).

Carried rows take the round-10 evidence and the prefix 'Carried from round 10 ...' only where the cited subject is
byte-identical to the round-10 pin 47a36d8c. Every other row carries evidence from a command or check run this round.
Run from the checkout root: python -I ledgers/FC1/scripts/FC1-c-r11/build_fragment_FC1c_r11.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers" / "FC1" / "scripts" / "FC1-c-r11" / "out"
R10 = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-FC1-c.round10.json").read_text(encoding="utf-8"))
R10_ROWS = {r["id"]: r for r in R10["rows"]}
CARRY_PREFIX = "Carried from round 10 (cited files byte-identical since the round-10 pin 47a36d8c): "

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix or ""
    rows.append(item)


def carry(rid: str, note: str = "") -> None:
    prev = R10_ROWS[rid]
    assert prev["status"] == "PASS", rid
    ev = CARRY_PREFIX + note + " " + prev["evidence"] if note else CARRY_PREFIX + prev["evidence"]
    rows.append({"id": rid, "check": prev["check"], "location": prev["location"], "status": "PASS", "evidence": ev.strip()})


# ---- fresh evidence this round -------------------------------------------------------------------------------
row("proj-check-projects", "2.6-structure", "course/modules/FC/FC1/project.html", "PASS",
    "Re-run r11: tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS', exit 0 (out/check_projects.out).")
row("proj-check-pages", "2.9-structure", "course/modules/FC/FC1/project.html", "PASS",
    "Re-run r11: tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (out/check_pages.out).")
row("proj-check-dag", "2.9-dag", "project.html; curriculum/curriculum.json concepts", "PASS",
    "Re-run r11: tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0 (out/check_dag.out). Concept links "
    "present-value and discount-factor (project.html line 178) resolve.")
row("proj-run-labs", "2.5-labs", "project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py", "PASS",
    "Re-run r11: tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)' (out/run_labs_project.out); "
    "whole unit 'run_labs FC1: PASS (8/8)' (out/run_labs_all.out).")
row("proj-page-smoke", "2.9-smoke", "course/modules/FC/FC1/project.html", "PASS",
    "Re-run r11: tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke modules/FC/FC1/project.html: PASS', exit 0; "
    "in-browser grader 'All 89 tests pass on seed 706127255' (out/page_smoke_project.out). Chromium harness, not a manual session.")
row("proj-run-graders", "2.6-autograde-reference", "grader/reference.py, test_project.py, instance.py, starter.py", "PASS",
    "Re-run r11: tools/run_graders.py --unit FC1 --seeds 0-49 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.3 s)' "
    "(out/run_graders_0_49.out). ledgers/FC1/scripts/FC1-c-r11/suite_run.py: reference 89 passed on each of seeds 0-19 (out/reference_0_19.out).")
row("proj-lint-types", "2.6-lint", "course/modules/FC/FC1/grader/*.py; tests/labs/FC1/; ledgers/FC1", "PASS",
    "Re-run r11: ruff check . -> 'All checks passed!' (out/ruff_check.out); ruff format --check . -> '553 files already formatted' "
    "(out/ruff_format.out); mypy --no-incremental -> 'Success: no issues found in 385 source files' (out/mypy.out).")
row("proj-lab1-numbers", "2.2-numbers", "project.html lines 58, 97-100 (Lab 1)", "PASS",
    "Re-derived with Fraction (scripts/FC1-c-r11/numbers_r11.py, out/numbers_r11.out): events [(1,5000),(2,5000),(3,105000)]; "
    "exact PV 102775.091033 (float repr 102775.09103322713); price 102775; trade (2,-98500). Expected block equals run_labs output.")
row("proj-lab3-fixture-values", "2.2-numbers", "project.html lines 198-275 (Lab 3)", "PASS",
    "numbers_r11.out re-derives A [(1,10500)] price 10000; B exact 210000/19 = 11052.6316 (float 11052.631578947368) price 11053; "
    "C [(1,5001),(2,15002)]; D [(1,2)]; E (2,-98500); F [(1,1)] price 1 (exact 1/2; Python round gives 0); G [(1,10001)] price 5001 "
    "(exact 10001/2). Lab 3 expected block equals twin output (run_labs PASS).")
row("proj-rounding-fixture-terms", "2.2-numbers", "project.html line 193; grader/test_project.py lines 396-403", "PASS",
    "numbers_r11.out: Bond(10000,500,3) at 400 bps exact 10277.509103 (float repr 10277.509103322713) rounds once to 10278; "
    "terms round one by one to 481+462+9334 = 10277 (out/numbers_r11.out). Page line 193 and test docstring 398-399 agree.")
row("proj-expected-equals-output", "2.5-labs", "project.html expected blocks lines 97-100, 145-148, 263-275", "PASS",
    "Re-run r11: run_labs --page project PASS 3/3 (out/run_labs_project.out); the three project twins also exit 0 under "
    "python -I -W error when run alone.")
row("proj-hours-arithmetic", "2.9-hours", "project.html table#hours lines 286-293; data-hours-project line 34", "PASS",
    "Components 1+2+5+4+2+3+3 = 20 = data-hours-project (line 34) = the 20 of the module's 70 in course/assets/data/program.json "
    "(FC1 hours 70) and index.html data-hours-lessons 50 + data-hours-project 20 = 70 (index.html line 29). 5 lessons x 10 = 50.")
row("proj-ladder", "2.9-structure", "project.html lines 41-50, 52-151, 153-172, 312-319", "PASS",
    "Rung links resolve: #spec (line 153), #grader-section (line 299), #stretch (line 312), #conventions (line 174); "
    "placement link index.html#placement exists (index.html line 67). Rung titles match the sections.")
row("proj-named-conditions", "2.6-conditions", "project.html lines 163-167; grader/reference.py lines 42-46, 64, 81-87", "PASS",
    "reference.py checks: Bond count<1 (line 42), face<=0 (44), coupon<0 (46); bond_price_cents rate<=-10000 (64); CashTrade units<1 (81), "
    "price<0 (83), side not in (1,-1) (85), day<1 (87). Eight conditions, each in the page's list; tests check both sides (test_project.py lines 215-266, 499-513, 559-661).")
row("proj-test-count", "2.9-count", "project.html line 171; grader/test_project.py", "PASS",
    "pytest --collect-only on the pinned suite: '89 tests collected' (out/collect_only.out; 89 'def test_' lines). Page line 171 says 89 checks.")
row("proj-starter-fails", "2.6-starter", "grader/starter.py", "PASS",
    "starter.py as instruments.py, seed 0: '87 failed, 2 passed' (out/starter_full_seed0.out); the 2 passing tests are the two that "
    "accept any exception (float face, bool periods). 0 tracebacks; 87 'has no implementation' messages.")
row("proj-instances", "2.6-instances", "grader/instance.py, seeds 0-49", "PASS",
    "instance.py byte-identical; run_graders seeds 0-49 PASS (out/run_graders_0_49.out); alternatives and reference pass seeds 0-19.")
row("proj-same-suite-pyodide-pytest", "2.6-same-file", "grader/test_project.py; project.html line 309", "PASS",
    "suite_run.py uses the page's flags (-q -p no:cacheprovider --assert=plain -W error) and passes 89 on seeds 0-19 (out/reference_0_19.out); "
    "in-browser run 89 pass (out/page_smoke_project.out).")
row("proj-scope-words", "2.6-prose", "project.html lines 163, 171, 176-186", "PASS",
    "Scope words in the changed line 171 ('every named condition', 'a yield above 100 %', 'trades ... which the page does not bound') checked: "
    "all eight conditions have both boundaries tested; the five yields (150, 300, 2000, 10000, 100000 %) and the five settlement periods are tested "
    "(test_project.py lines 515, 822, 849, 881, 929; 672, 831, 872, 906, 940).")
row("proj-prose-banned-phrases", "2.6-prose", "project.html; cards.json; grader/*.py; labs", "PASS",
    "Re-grep r11 of the changed text (project.html line 171, cards c147/c150/c152, new tests lines 925-957): no verifier, round, "
    "builder or audit wording. The only process-like words in the project page are pre-existing 'reviewer reads it' (lines 161, 163).")
row("proj-process-words", "2.6-prose", "project.html; cards.json; labs", "PASS",
    "Same grep as proj-prose-banned-phrases (out/process_words_grep.out is the round-10 pattern; no new hit in the r11 delta).")
row("proj-notation", "2.6-notation", "notation/notation.json; FC1 pages, cards, labs", "PASS",
    "Changed symbols (S_n, D_t, d, phi, rho, kappa in cards c147/c152 and L01) are not among the 8 registered symbols of notation.json "
    "(T, Phi, gamma_3, ...); no registered symbol is reused with another meaning in the changed text.")
row("proj-cards-scan-duplicates", "2.6-cards", "course/modules/FC/FC1/cards.json (151 cards)", "PASS",
    "out/cards_check.out: 'cards: 151 unique ids: 151', 'duplicate fronts: 0', 'duplicate backs: 0'. Near-duplicate fronts (32, ratio > 0.8) "
    "are distinct assumptions (for example A1/A2/A3 of the dealer model) and not duplicates.")
row("proj-cards-numbers-in-lessons", "2.6-cards", "cards.json vs out/lessons/L01-L05.txt (regenerated this round)", "PASS",
    "out/cards_check.out: 'card numbers >= 13 absent from the card's lesson: []'.")
row("proj-cards-numbered-references", "2.6-cards", "cards.json citations vs lesson headings", "PASS",
    "out/cite_resolve_r11.out is identical to round 10 (diff exit 0): 162 labels, 25 unresolved by the regex (for example 'Section 2' "
    "where the heading reads '2Bank money creation'). Those 25 were resolved by hand in round 10. The changed cards resolve by hand: "
    "c147 'Section 2' = L01.txt line 50 heading; c152 'Proposition 3.5' = L01.txt line 114.")
row("proj-cards-sample", "2.6-cards", "course/modules/FC/FC1/cards.json (sample of 15 against lesson text)", "PASS",
    "The 14 sampled cards not changed this delta (c010, c020, c030, c040, c050, c060, c070, c080, c090, c100, c110, c120, c130, c140) are "
    "byte-identical since 47a36d8c and carried from round 10; the fifteenth sampled card, c150, was changed and is re-verified below.")
row("proj-cards-changed-subjects", "2.6-cards", "cards.json FC1-c064, c101, c147, c150 (c152: its own row)", "PASS",
    "c064 and c101 byte-identical since 47a36d8c (carried); c147 and c150 re-verified (rows proj-cards-c147-changed, proj-cards-c150-changed). "
    "c152 is judged in proj-cards-c152-hypotheses.")
row("proj-cards-c147-changed", "2.6-cards", "cards.json FC1-c147 (front and back changed this delta)", "PASS",
    "front 'Which sum of stage deposits is S_n?'; back 'The sum of the deposits received at stages 0 to n, S_n = sum_{t=0}^{n} D_t (Section 2).' "
    "L01.txt line 56 ('total deposits after stages 0 to n are S_n = sum D_t, defined in Section 2') and line 72 agree; Section 2 is "
    "the heading '2Bank money creation in a stylised model' (L01.txt line 50). Lesson L01 is byte-identical since the pin.")
row("proj-cards-c150-changed", "2.6-cards", "cards.json FC1-c150 (back changed this delta)", "PASS",
    "back 'A claim with terms.' matches L02.txt line 34: 'An instrument is a claim with terms, and this lesson sorts ...'. The removed "
    "'as the opening paragraph of the lesson states it' is no longer needed.")
row("proj-cards-new-c143-c151", "2.6-cards", "cards.json FC1-c143 to FC1-c151", "PASS",
    "c147 and c150 re-verified (rows above). c143-c146, c148, c149 and c151 are byte-identical since 47a36d8c (carried).")
row("proj-cards-citation-scan", "2.6-cards", "cards.json citations (all cards)", "PASS",
    "out/cite_resolve_r11.out identical to round 10; c147 and c152 citations checked by hand (rows above); no citation changed on the other 148 cards.")
row("proj-cards-c152-hypotheses", "2.6-cards",
    "course/modules/FC/FC1/cards.json FC1-c152 back (grade T); L01 Proposition 3.5 (course/modules/FC/FC1/L01.html, lesson text out/lessons/L01.txt line 114)",
    "FAIL",
    "The card's back now lists A2' with 0<=phi<=1, A1 with 0<rho<=1, the no-withdrawal and no-repayment parts of A3, and d > 0, then "
    "'with equality if and only if phi = 1 or rho = 1 (Proposition 3.5)'. The card is true under those hypotheses. But Proposition 3.5 "
    "as printed (L01.txt line 114) does not state d > 0 (Proposition 3.1 at line 88 does), and the 'equality iff' clause is false at d = 0: "
    "d = 0, phi = 1/2, rho = 1/2 gives 0/(1-1/4) = 0 = d/rho with phi != 1 and rho != 1 (checked by hand). The proof at L01.txt line 118 reaches its equality clause by dividing through by d, so the step "
    "'equality holds exactly when (1-rho)(1-phi) = 0' needs d != 0. The card cites a proposition whose statement lacks "
    "one of the card's hypotheses.",
    "Add 'with d > 0' to the statement of Proposition 3.5 in the L01 source (lesson owner), so the card's hypotheses equal the "
    "proposition's. Then re-run render_curriculum and the lesson build. Alternatively drop the '(Proposition 3.5)' attribution and "
    "cite the proof. Either way the card and the printed proposition must state the same hypotheses.")
row("proj-cards-grades", "2.6-cards", "cards.json grade fields vs lesson key-results and lab outputs", "PASS",
    "Grade fields byte-identical since 47a36d8c: the delta changed only the front and back of c147, c150 and c152 (git diff 47a36d8c..HEAD, cards.json, 6 lines). "
    "Carried from round 10: " + R10_ROWS["proj-cards-grades"]["evidence"])
row("proj-spec-scope-vs-curriculum", "2.6-spec", "project.html line 157; curriculum/02-economics-finance-core.yaml line 389 (FC1 project title and brief)", "PASS",
    "Carried from round 10: " + R10_ROWS["proj-spec-scope-vs-curriculum"]["evidence"] +
    " (yaml line 389 is byte-identical; the round-11 yaml change is at line 425, the FC2 arbitrage brief, not FC1.)")
row("proj-reference-deployment", "2.6-deployment", "BLUEPRINT.md line 401; grader/reference.py line 4; .github/workflows/ci.yml; repository root", "FAIL",
    "BLUEPRINT.md line 401 (unchanged): deployment 'excludes every grader/reference.py'. reference.py line 4 says no file in this repository "
    "enforces that. Re-checked r11: no deploy config at the root (no vercel, netlify, wrangler or render file); ci.yml has no publish step "
    "(artifact upload only, line 79); tools/ has no exclusion of reference.py (grep). UNVERIFIABLE in this repository.",
    "Add a build or publish step that removes grader/reference.py from the published tree, with a check that fails if it is present, "
    "or state in BLUEPRINT that deployment is external and not verified here.")
row("proj-mutant-r11c-settlement-1e7-survivor", "2.6-mutants",
    "grader/test_project.py lines 940-946 (largest settlement tested is 10**7); project.html line 171", "FAIL",
    "Student-error mutant ledgers/FC1/mutants/r11c_settlement_refused_above_ten_million.py (CashTrade refuses settlement_day > 10**7) "
    "survives seeds 0-19: all 89 pass (out/mutate_graders_0_19_final.out; out/new_r11c_settlement_refused_above_ten_million.out). "
    "project.html line 171 states 'trades settling in periods 100, 1000, 5001, 1,000,000 and 10,000,000, which the page does not bound', "
    "so a refusal above 10**7 contradicts the stated behaviour and no test exercises it.",
    "Add an accepted-input test at a far larger settlement period (for example 10**18), and reword line 171 so that the checked values are "
    "listed as checked, not as unbounded. Or record the limit (no check above the largest listed value) as an explicit honest gap.")
row("proj-mutant-r11c-yield-1e7-survivor", "2.6-mutants",
    "grader/test_project.py lines 929-937 (largest yield tested is 10**7 bps); project.html line 171", "FAIL",
    "Student-error mutant ledgers/FC1/mutants/r11c_yield_refused_above_hundred_thousand_percent.py (bond_price_cents refuses yield_bps > 10**7) "
    "survives seeds 0-19: 89 pass (out/mutate_graders_0_19_final.out). project.html line 171 states 'a yield above 100 % per period, which the "
    "page does not refuse (checked at 150 %, at 300 %, at 2000 %, at 10000 % and at 100000 %)'.",
    "Add an accepted-input test at a far larger yield (for example 10**18 bps, with the price computed exactly), and reword line 171 "
    "to list the checked yields. Or record the limit as an explicit honest gap.")
row("proj-mutant-r11c-quantity-1e30-survivor", "2.6-mutants",
    "grader/test_project.py lines 915-922 (largest quantity tested is 10**30); project.html line 171", "FAIL",
    "Student-error mutant ledgers/FC1/mutants/r11c_quantity_refused_above_ten_to_the_thirtieth.py (CashTrade refuses quantity > 10**30) "
    "survives seeds 0-19: 89 pass (out/mutate_graders_0_19_final.out). project.html line 171 states 'trades of 501, 1001, 2<sup>40</sup>+1 "
    "and 10<sup>30</sup> units, which the page does not bound'.",
    "Add an accepted-input test at a far larger quantity (for example 10**60), and reword line 171 to list the checked quantities. "
    "Or record the limit as an explicit honest gap.")
row("proj-mutants-r11c-killed", "2.6-mutants", "ledgers/FC1/mutants/r11c_coupon_rounded_half_even.py; r11c_zero_yield_price_drops_last_event.py", "PASS",
    "Both KILLED on seed 0 (out/mutate_graders_0_19_final.out): coupon half-even by test_bond_half_cent_coupon_rounds_away_from_zero; "
    "zero-yield tail drop by test_bond_price_at_zero_yield_counts_the_events_after_period_one_thousand (and the fixture tests).")
row("proj-test-r11-new-tests", "2.6-tests", "grader/test_project.py lines 925-957 (three new accepted-input tests)", "PASS",
    "test_bond_yield_of_ten_million_bps_is_accepted: 10500/1001 = 10.4895 rounds to 10 (numbers_r11.out). "
    "test_trade_settling_in_period_ten_million_is_accepted: event (10**7, -98500). "
    "test_bond_price_at_zero_yield_counts_the_events_after_period_one_thousand: Bond(10000,0,1001) at 0 bps prices 10000 (numbers_r11.out). "
    "Each docstring value matches the arithmetic; each test passes on the reference (89/89 seeds 0-19). Collect count 89 = page line 171.")
row("proj-mutants-all", "2.6-mutants", "ledgers/FC1/mutants/*.py (132 files)", "FAIL",
    "tools/mutate_graders.py --unit FC1 --seeds 0-19 -> 'mutate_graders FC1: FAIL (129/132 killed)', exit 1 (out/mutate_graders_0_19_final.out). "
    "The 127 earlier mutants are all KILLED (including the three round-10 r10c_* survivors, now killed by the new tests). The three "
    "survivors are the threshold mutants of this round (rows proj-mutant-r11c-*-survivor).",
    "Close the three threshold survivors (see their rows), then re-run mutate_graders.")
row("proj-mutants-r10c-new", "2.6-mutants", "ledgers/FC1/mutants/r10c_*.py (3 files)", "PASS",
    "r10c_price_ignores_events_after_period_one_thousand KILLED by test_bond_price_at_zero_yield_counts_the_events_after_period_one_thousand; "
    "r10c_settlement_refused_above_one_million KILLED by test_trade_settling_in_period_ten_million_is_accepted; "
    "r10c_yield_refused_above_ten_thousand_percent KILLED by test_bond_yield_of_ten_million_bps_is_accepted (out/mutate_graders_0_19_final.out).")
for mid, test in [
    ("proj-mutant-r10c-yield-10mil-survivor", "test_bond_yield_of_ten_million_bps_is_accepted"),
    ("proj-mutant-r10c-settlement-1m-survivor", "test_trade_settling_in_period_ten_million_is_accepted"),
    ("proj-mutant-r10c-tail-1000-survivor", "test_bond_price_at_zero_yield_counts_the_events_after_period_one_thousand"),
]:
    row(mid, "2.6-mutants", "grader/test_project.py (new tests, lines 929-957)", "PASS",
        f"Round-10 survivor now KILLED on seed 0 by {test} (out/mutate_graders_0_19_final.out).")

# Mutant family rows: re-run this round, all KILLED (names checked against out/mutate_graders_0_19_final.out)
killed_out = (OUT / "mutate_graders_0_19_final.out").read_text(encoding="utf-8").splitlines()
KILLED = {m.group(1): m.group(2) for m in (re.match(r"KILLED (\S+)\.py: .* -> (\S+) \(seed", l) for l in killed_out if l.startswith("KILLED")) if m}


def family(prefix: str) -> int:
    names = [k for k in KILLED if k.startswith(prefix)]
    return len(names)


for rid, prefix, label in [
    ("proj-mutants-v1c-new", "v1c_", "v1c_*"), ("proj-mutants-v2c-new", "r2c_", "r2c_*"),
    ("proj-mutants-r3c-killed", "r3c_", "r3c_*"), ("proj-mutants-v4c-new", "v4c_", "v4c_*"),
    ("proj-mutants-r4c-new", "r4c_", "r4c_*"), ("proj-mutants-r5c-new", "r5c_", "r5c_*"),
    ("proj-mutants-r6c-killed", "r6c_", "r6c_*"), ("proj-mutants-r7c-new", "r7c_", "r7c_*"),
    ("proj-mutants-r8c-new", "r8c_", "r8c_*"), ("proj-mutants-r9c-new", "r9c_", "r9c_*"),
]:
    n = family(prefix)
    assert n > 0, prefix
    row(rid, "2.6-mutants", f"ledgers/FC1/mutants/{label}", "PASS",
        f"Re-run r11 (tools/mutate_graders.py --unit FC1 --seeds 0-19): {n} '{label}' mutants KILLED (out/mutate_graders_0_19_final.out).")

SURVIVOR_ROWS = {
    "proj-mutant-schedule-cap-thirty-survivor": "r4c_schedule_stops_at_thirty_periods",
    "proj-mutant-exponent-cap-thirty-survivor": "r4c_discount_exponent_capped_at_thirty",
    "proj-mutant-schedule-cap-survivor": "r3c_schedule_stops_at_twenty_periods",
    "proj-mutant-price-digits-survivor": "r3c_price_ten_digits_integral_rounding",
    "proj-mutant-price-cache-survivor": "r2c_price_cached_on_first_yield",
    "proj-mutant-price-epsilon-survivor": "r5c_price_rounded_with_epsilon",
    "proj-mutant-yield-100-survivor": "r5c_yield_above_one_hundred_percent_refused",
    "proj-mutant-schedule-cap-forty-survivor": "r6c_schedule_stops_at_forty_periods",
    "proj-mutant-exponent-cap-forty-survivor": "r6c_discount_exponent_capped_at_forty",
    "proj-mutant-yield-200-survivor": "r6c_yield_above_two_hundred_percent_refused",
    "proj-mutant-settlement-cap-100-survivor": "r6c_settlement_day_above_one_hundred_refused",
    "proj-mutant-decimal-40-digits-survivor": "r6c_price_decimal_forty_significant_digits",
    "proj-mutant-decimal-28-digits-kill": "r6c_price_default_decimal_28_digits",
    "proj-mutant-periods-cap-1000-survivor": "r7c_periods_refused_above_one_thousand",
    "proj-mutant-r7c-coupon-half-even": "r7c_coupon_rounded_half_even",
    "proj-mutant-r7c-discount-float": "r3c_discount_factor_float_times_amount",
    "proj-mutant-r7c-price-cap-1m": "r7c_price_refused_above_one_million_cents",
    "proj-mutant-r7c-hard-coded-answer": "r7c_price_is_seed_zero_answer_constant",
    "proj-mutant-yield-1000-survivor": "r8c_yield_refused_above_one_thousand_percent",
    "proj-mutant-settlement-5000-survivor": "r8c_settlement_day_refused_above_five_thousand",
    "proj-mutant-periods-5000-survivor": "r8c_periods_refused_above_five_thousand",
    "proj-mutant-face-int64-kill": "r8c_face_refused_above_int64",
    "proj-mutant-r9c-yield-2000-survivor": "r9c_yield_refused_above_two_thousand_percent",
    "proj-mutant-r9c-periods-10000-survivor": "r9c_periods_refused_above_ten_thousand",
    "proj-mutant-r9c-settlement-10000-survivor": "r9c_settlement_day_refused_above_ten_thousand",
    "proj-mutant-r9c-quantity-2pow50-survivor": "r9c_quantity_refused_above_two_to_the_fifty",
}
for rid, mname in SURVIVOR_ROWS.items():
    assert mname in KILLED, (rid, mname)
    prev = R10_ROWS[rid]
    row(rid, "2.6-mutants", prev["location"], "PASS",
        f"Re-run r11: mutant {mname}.py KILLED on seed 0 by {KILLED[mname]} (out/mutate_graders_0_19_final.out). "
        "Round-10 evidence for this mutant's class is superseded by this run.")

row("proj-lab3-autograder-coverage-note", "2.5-labs", "project.html line 276 (note after Lab 3); grader/test_project.py", "PASS",
    "Note claims: fixture A events and price (test_bond_one_period_fixture_is_par_coupon_plus_face, test_bond_price_one_period_at_its_coupon_rate_is_par); "
    "fixture B price (test_bond_price_negative_yield_is_above_the_undiscounted_value); fixture C and D events (test_bond_half_cent_*); "
    "fixture E events (test_buyer_pays_cash_at_settlement, test_seller_receives_cash_at_settlement); fixture F events (test_bond_face_one_cent_is_accepted); "
    "fixture F and G prices (test_bond_price_exact_half_cent_rounds_away_from_zero, test_bond_price_exact_half_at_five_thousand_point_five_rounds_up); "
    "rounding price (test_bond_price_hand_fixture_rounds_the_sum_once). grep of the suite: Bond(10_001, 0, 1) is used only for its price (line 418); "
    "the rounding case's events are not listed (no Bond(10000,500,3) events assertion). The note is accurate.")
row("proj-page-grading-description", "2.6-claims", "project.html line 171; grader/test_project.py", "PASS",
    "Each listed item of line 171 checked against the suite: 13-15, 24, 40, 100, 1001 (with zero-yield test), 5001, 100001 (events only) periods; "
    "150, 300, 2000, 10000, 100000 % yields; settlement 100, 1000, 5001, 1,000,000, 10,000,000; quantities 501, 1001, 2**40+1, 10**30; "
    "half-cent cases incl. Bond(10**40+1,0,1) at 10000 bps; collect count 89 (out/collect_only.out).")

# Rows whose cited subjects are byte-identical since the round-10 pin: carried
for rid, note in [
    ("proj-lab2-blanks", "project.html lines 133 and 140 and lab-FC1-project-2.py byte-identical; run_labs re-run this round PASS 3/3 (out/run_labs_project.out)."),
    ("proj-lab3-claim-using-functions", "project.html line 198 and lab-FC1-project-3.py byte-identical."),
    ("proj-hours-rationale-rows", "project.html lines 286-293 byte-identical."),
    ("proj-hours-verifier-estimate", "project.html lines 291-292 byte-identical."),
    ("proj-spec-interface", "project.html line 161 and grader/starter.py byte-identical."),
    ("proj-silence-purity", "grader/test_project.py lines 693-734 byte-identical (the r11 additions are at lines 925-957); the reference passes the suite on seeds 0-19 this round."),
    ("proj-local-command", "project.html line 308 and starter.py line 6 byte-identical; the flags reproduced by suite_run.py this round."),
    ("proj-terms-before-definition", "project.html lines 54-56, 106, 161, 179 byte-identical."),
    ("proj-footer-claim", "project.html line 341, course/assets/js/grader.js, store.js and python.js byte-identical."),
    ("proj-saved-as-you-type", "project.html line 301, grader.js lines 33-79 and store.js byte-identical."),
    ("proj-references-reading-list", "project.html lines 321-328 and the two references/references.json entries mishkin2021economics and harris2002trading byte-identical (git diff 47a36d8c..HEAD hunks at references.json lines 2838 and 19676 only)."),
    ("proj-cited-year-conflicts", "project.html reading list, references.json entries and curriculum/02-economics-finance-core.yaml line 385 byte-identical."),
    ("proj-data-simulated", "project.html lines 45, 54, 159, grader/instance.py and tests/labs/FC1 byte-identical."),
    ("proj-page-hypothesis-sides", "project.html line 106 byte-identical."),
    ("proj-page-constraints-silence", "project.html line 163 byte-identical."),
    ("proj-named-error-message-values", "grader/test_project.py lines 75-93 and 693-734 byte-identical."),
    ("proj-failure-messages", "grader/test_project.py lines 693-734 and 770-788 byte-identical."),
    ("proj-starter-message-leaks-answer", "grader/test_project.py lines 515-517, 822-828, 849-851, 881-883 byte-identical."),
    ("proj-cards-c139-c142-new", "cards.json FC1-c139 to c142 byte-identical."),
    ("proj-cards-c014-lab-true", "cards.json FC1-c014 and L01 Lab 1 Part A byte-identical."),
    ("proj-cards-c122-equity-after-loss", "cards.json FC1-c122 and L01 Proposition 4.1 byte-identical."),
    ("proj-cards-citation-R3", "cards.json FC1-c067 and L04 byte-identical."),
    ("proj-cards-citation-R2", "cards.json FC1-c068 and L04 byte-identical."),
    ("proj-starter-silence-scope", "starter.py lines 8-10 and project.html line 163 byte-identical."),
    ("proj-lab-io-free", "tests/labs/FC1/lab-FC1-project-*.py byte-identical."),
    ("proj-terminology-short-holder", "project.html line 54 byte-identical."),
]:
    carry(rid, note)

# Rows re-verified by targeted checks this round (not carried)
row("proj-labs-twins-I-W-error", "2.5-labs", "tests/labs/FC1/lab-FC1-L01..L05-1.py and lab-FC1-project-1..3.py", "PASS",
    "Re-run r11, each twin alone: python -I -W error exits 0 for L01-1, L02-1, L03-1, L04-1, L05-1, project-1, project-2, project-3. "
    "tests/labs/FC1 byte-identical since the pin.")
row("proj-verify-refs-offline", "2.1-citations", "references/references.json (whole registry, offline)", "PASS",
    "Re-run r11: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.out).")
row("proj-pytest-fc1", "2.5-tests", "tests/test_labs.py, tests/test_curriculum.py, tests/test_page_checks.py (-k FC1)", "PASS",
    "Re-run r11: .venv/bin/pytest -q -k FC1 on the three files -> 9 passed, exit 0 (out/pytest_fc1.out).")
row("proj-ruff-repo-gate-note", "2.6-lint", "repository gate (ruff check .)", "PASS",
    "Re-run r11: ruff check . 'All checks passed!' exit 0; ruff format --check . '553 files already formatted' exit 0 (out/ruff_check.out, out/ruff_format.out).")
row("proj-test-name-two-thousand-percent", "2.6-tests", "course/modules/FC/FC1/grader/test_project.py line 849", "PASS",
    "Line 849 defines test_bond_yield_of_two_thousand_percent_per_period_is_accepted; its docstring's 200000 bps is 2000 % per period (line 850). Name matches.")
row("proj-docstring-float-claim", "2.2-numbers", "grader/test_project.py lines 423-427, 451-452, 459-462", "PASS",
    "checks2.py (out/checks2.out): exact coupon 61013403/2000 = 30506.7015 rounds to 30507, event 1734792, exact PV 3305625/2 (= half cent, rounds to "
    "1652813); binary float 1652812.4999999998; (1+0.04)**-1*13 = 12.499999999999998 rounds to 12; hair case 299985000 + 1/2 - 1/(2*1000300030001) "
    "equals the exact value and rounds to 299985000.")
row("proj-test-docstring-hand-numbers", "2.2-numbers", "grader/test_project.py docstrings (old and new)", "PASS",
    "numbers_r11.out and checks2.out re-derive the docstring numbers: fixture values, the 10277.5091 rounding case, 10**17+4999 coupon "
    "(rounds to 10**13), 10**9 face coupon 5*10**7, 10500/101 = 103.96 -> 104, 10500/1001 -> 10, 10500/21 = 500, 10500/2.5 = 4200, "
    "Bond(10**40+1,0,1) half = 5*10**39 + 1/2.")
row("proj-starter-unwrapped-new-tests", "2.6-messages", "grader/test_project.py lines 929-957 and the wrapper loop lines 959-962", "PASS",
    "Starter run seed 0: 0 tracebacks, 87 'has no implementation' messages (out/starter_full_seed0.out); the wrapper loop at lines 959-962 is "
    "after the three new tests, so they are wrapped.")
row("proj-alternatives", "2.6-autograder", "ledgers/FC1/alternatives/a1..a5 (grader suite seeds 0-19)", "PASS",
    "Re-run r11 with the current suite: a1..a5 each 20 of 20 seeds 0-19 pass, 89 passed per seed (out/alt_a1.out, out/alt_a2_*.out ... out/alt_a5_*.out).")
row("proj-alternatives-r4-new", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r4/alt/alt6", "PASS",
    "Re-run r11: alt6_r4_pow_fraction_floor 20/20 seeds (out/alt_alt6_r4_pow_fraction_floor.out).")
row("proj-alternatives-r6-new", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r6/alt/alt7..alt9", "PASS",
    "Re-run r11: alt7, alt8, alt9 each 20/20 seeds (out/alt_alt7_*.out, out/alt_alt8_*.out, out/alt_alt9_*.out).")
row("proj-alternatives-r7-new", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r7/alt/alt10..alt12", "PASS",
    "Re-run r11: alt10, alt11, alt12 each 20/20 seeds (out/alt_alt10_*.out, out/alt_alt11_*.out, out/alt_alt12_*.out).")
row("proj-alternatives-r8-new", "2.6-autograder", "ledgers/FC1/scripts/FC1-c-r8/alt/alt13..alt15", "PASS",
    "Re-run r11: alt13, alt14, alt15 each 20/20 seeds (out/alt_alt13_*.out, out/alt_alt14_*.out, out/alt_alt15_*.out).")
row("proj-alternatives-fixed-suite-r9", "2.6-autograder", "grader/test_project.py (r9 proposal applied) and the alternatives", "PASS",
    "The round-9 accepted-input tests are in the current suite; all five a-alternatives and alt6-alt15 pass 20/20 on it this round.")

# Round-10 PASS rows about the project page's whole file (re-run this round above) and the reading list are covered.
ids_r10 = list(R10_ROWS.keys())
new_ids = {r["id"] for r in rows}
missing = [i for i in ids_r10 if i not in new_ids]
if missing:
    raise SystemExit(f"round-10 rows not covered: {missing}")

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

mutants = []
for line in killed_out:
    m = re.match(r"(KILLED|SURVIVED) (\S+)\.py: (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = killed.replace(" (seed 0)", " (seed 0)") if status == "KILLED" else "SURVIVED seeds 0-19 (none)"
    mutants.append({"id": name, "description": desc, "killed_by": killed_by})

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 11 (did not build FC1)",
    "pin": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87",
    "base": "47a36d8c78633793ccc762ae19dcd5e19b780d19 (round-10 pin of this slice). Delta 47a36d8c..ccaeeaf4 in slice: project.html line 171 (89 checks, two new named values); grader/test_project.py +35 lines (three new accepted-input tests at lines 925-957, wrapper loop now at 959-962); cards.json FC1-c147 front, FC1-c150 back, FC1-c152 back; ledgers/FC1/mutants/r10c_*.py (three files). Lessons L01-L05, index.html, tests/labs/FC1, grader/reference.py, instance.py and starter.py are byte-identical since the round-10 pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD11-FC1-c",
    "scratch": "ledgers/FC1/scripts/FC1-c-r11/ (suite_run.py, make_mutants_r11.py, numbers_r11.py, checks2.py, lesson_text.py, cards_check_r10.py (r11 paths), cite_resolve_r11.py, build_fragment_FC1c_r11.py); outputs in out/",
    "verified_at": "2026-11-05T14:42:54+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": R10["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "Round 11, FC1-c. Verdict FAIL. Non-PASS rows: proj-cards-c152-hypotheses (Proposition 3.5 in L01 omits d > 0, which its "
        "equality clause needs; the card now carries it); proj-reference-deployment (repo-wide, UNVERIFIABLE here); "
        "proj-mutants-all (129/132) and three threshold survivors r11c_settlement_refused_above_ten_million, "
        "r11c_yield_refused_above_hundred_thousand_percent, r11c_quantity_refused_above_ten_to_the_thirtieth, each refusing above "
        "the largest value the suite accepts (the page lists that value as unbounded). Closed this round: the three round-10 r10c "
        "survivors (now KILLED by the three new tests), and the round-10 cards row for c152 is re-judged with the lesson text. "
        "Test count: 89 collected = page line 171. Alternatives a1-a5 and alt6-alt15: 20/20 seeds each. Reference: 89 passed on seeds 0-19 and 50/50 via run_graders. "
        "Labs: 8/8 via run_labs; the eight twins pass under python -I -W error. "
        "Could not check: the deployed site (no deploy config); live Crossref or publisher checks (offline only); the full repository pytest "
        "(only -k FC1 subset); a manual browser session; the L01 proposition wording beyond the card row (lesson owner). "
        "Note: the file ledgers/FC1/FC1-c.json present in this checkout at the start was a round-13 fragment (pin 762f636d) committed "
        "in d0f39c09; this round-11 fragment replaces it in the checkout only, uncommitted."
    ),
    "summary": {
        "rows_total": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": {
            "killed": sum(1 for m in mutants if m["killed_by"] != "SURVIVED seeds 0-19 (none)"),
            "total": len(mutants),
        },
    },
}

target = ROOT / "ledgers" / "FC1" / "FC1-c.json"
target.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", target, "rows", len(rows), "verdict", verdict, counts, "mutants", len(mutants))
