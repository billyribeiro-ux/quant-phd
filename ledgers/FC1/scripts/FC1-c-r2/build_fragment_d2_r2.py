"""Build ledgers/FC1/FC1-c.json (round 2, slice c) from the evidence in this round's scripts. Verifier D2 round 2."""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
D = "ledgers/FC1/scripts/FC1-c-r2/out"
mut_lines = (ROOT / D / "mutate_graders_all_r2.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = "" if status == "SURVIVED" else killer.strip()
    mutants.append({"name": name, "description": desc.strip(), "killed_by": killed_by})
assert len(mutants) == 84, len(mutants)

P = "PASS"
F = "FAIL"

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        assert fix, rid
        r["fix"] = fix
    return r

carried_note = "Carried from round 1 (registry and curriculum facts unchanged since d0f39c09):"
rows = [
    row("proj-check-projects", "2.6-structure", "course/modules/FC/FC1/project.html", P,
        "Re-run on c737272: tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS' (out/check_projects.out)."),
    row("proj-check-pages", "2.9-structure", "course/modules/FC/FC1/project.html", P,
        "Re-run: tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS' (out/check_pages.out)."),
    row("proj-check-dag", "2.9-DAG", "course/modules/FC/FC1/project.html (concept links and the new L05.html link)", P,
        "Re-run: tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' (out/check_dag.out). The new link to L05.html "
        "(project.html line 177) is a plain lesson link, not a concept link; present-value and discount-factor remain the only concept links."),
    row("proj-run-labs", "2.5-labs", "project.html labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py", P,
        "Re-run: tools/run_labs.py --unit FC1 --page project -> 'run_labs FC1: PASS (3/3)' (out/run_labs_project.out). "
        "All FC1 pages: 'run_labs FC1: PASS (8/8)' (out/run_labs_all_pages_r2.out). Twin lab-FC1-project-3 also run alone under python -I -W error (exit 0)."),
    row("proj-page-smoke", "2.9-smoke", "course/modules/FC/FC1/project.html", P,
        "Re-run: tools/page_smoke.py --unit FC1 --pages project -> 'page_smoke FC1: PASS'; in-browser grader 'All 68 tests pass on seed 1354160130' (out/page_smoke_project.out)."),
    row("proj-run-graders", "2.6-autograder-1", "course/modules/FC/FC1/grader/reference.py, test_project.py, instance.py, starter.py", P,
        "Re-run: tools/run_graders.py --unit FC1 --seeds 0-19 -> 'run_graders FC1: PASS (reference 20/20 seeds, slowest 0.2 s)' (out/run_graders_0_19.out). "
        "grader/reference.py is still tracked in the repository; ruling 4 (FINAL-ARCHITECT-RULINGS) makes this a recorded note, not a failure."),
    row("proj-lint-types", "gate", "course/modules/FC/FC1/grader/*.py and tests/labs/FC1/", P,
        "ruff check (out/ruff_check.out: 'All checks passed!'), ruff format --check (out/ruff_format.out: '12 files already formatted'); "
        "mypy --no-incremental on reference.py, instance.py, starter.py and tests/labs/FC1/ (out/mypy_r2.out: 'Success: no issues found in 11 source files'). "
        "Repo-wide ruff check . and format --check . also pass (out/ruff_repo_r2.out, out/ruff_format_repo_r2.out)."),
    row("proj-lab1-numbers", "2.2-numbers / 2.5-labs", "project.html lines 58 and 97-100 (Lab 1)", P,
        "Recomputed in Fraction: coupon 5000; events (1,5000),(2,5000),(3,105000); exact PV 102775.09103322713 -> 102775; trade (2,-98500). "
        "Prose '102775.091033' and 'below one half' are correct. Lab 1 text unchanged since d0f39c09."),
    row("proj-lab2-blanks", "2.5-labs", "project.html lines 133 and 140 (Lab 2); tests/labs/FC1/lab-FC1-project-2.py", P,
        "Two blanks, twin is the completed solution; run_labs PASS. Tolerance 1e-6*(1+102775.09)=0.103 cent matches 'about 0.1 cent'. Lab 2 text unchanged."),
    row("proj-lab3-fixture-values", "2.2-numbers / 2.5-labs", "project.html lines 198-276 (Lab 3); tests/labs/FC1/lab-FC1-project-3.py", P,
        "Ran the twin under python -I -W error: every printed line equals the expected block (A [(1, 10500)] price 10000; B 11053 | exact 11052.6316; C [(1, 5001), (2, 15002)]; "
        "D [(1, 2)]; rounding events [(1, 500), (2, 500), (3, 10500)], 10278 once, 10277 term by term; E (2, -98500); F [(1, 1)] price 1; G [(1, 10001)] price 5001). "
        "Hand values recomputed: 210000/19 = 11052.6316; 10500/1.05 = 10000; 0.5 -> 1; 5000.5 -> 5001."),
    row("proj-rounding-fixture-terms", "2.2-numbers", "project.html line 193; grader/test_project.py lines 357-364 and 358-360 docstring", P,
        "Recomputed (python Fraction): exact PV 10277.509103322713 -> 10278; per-term 480.7692, 462.2781, 9334.4618 -> 481 + 462 + 9334 = 10277. Docstring figures 480.77, 462.28, 9334.46 and 10277.5091 are correct."),
    row("proj-lab3-claim-using-functions", "2.5-labs / prose vs code", "project.html line 198 (Lab 3 hypothesis) vs tests/labs/FC1/lab-FC1-project-3.py lines 37-61", P,
        "Round-1 FAIL resolved. The hypothesis now reads 'using the functions of this lab for the bond, and exact arithmetic (Fraction or int) for the trade and for the exact values'. "
        "Checked against the twin: bond fixtures A, B, C, D, F, G and the rounding case go through bond_events/bond_price/term_by_term_price; fixture E is int arithmetic (-10 * 9_850, line 54); "
        "the exact value of fixture B is Fraction (line 42). The sentence now matches the code."),
    row("proj-expected-equals-output", "2.5-labs", "project.html expected blocks (lines 97, 145, 263-275)", P,
        "run_labs compares each expected block with the output (tolerance 1e-6 scaled); PASS for all 8 FC1 labs (out/run_labs_all_pages_r2.out). Lab 3 expected block compared line by line by hand as well."),
    row("proj-hours-arithmetic", "2.6-hours / 2.9-structure", "project.html table#hours (lines 286-293); index.html data-hours-lessons, data-hours-project", P,
        "Components 1+2+5+4+2+3+3 = 20 (the table's Total row is 20). index.html: data-hours-lessons=\"50\" and data-hours-project=\"20\" (sum 70, the FC1 module hours). Table unchanged in this round."),
    row("proj-hours-rationale-rows", "2.6-hours", "project.html table#hours rows", P,
        "Each of the seven component rows has a one-line rationale; the Total row names the hub figure (20 of 70)."),
    row("proj-ladder", "2.6-spec ladder", "project.html lines 41-50 and 153-278", P,
        "Rung 1 worked example (Lab 1), Rung 2 completion (Lab 2, class completion, graded instantly), Rung 3 spec, Rung 4 stretch marked 'Not graded'. The index.html#placement anchor exists."),
    row("proj-spec-interface", "2.6-spec", "project.html line 161; grader/starter.py lines 16-40", P,
        "Required names and signatures: Bond(face_cents, coupon_bps, periods).events, bond_price_cents(bond, yield_bps), CashTrade(quantity, price_cents, side, settlement_day).events match starter.py exactly."),
    row("proj-named-conditions", "2.6-autograder-exception-table", "grader/test_project.py must_raise call sites (lines 215-260, 418-425, 469-476, 518-520, 531-553, 564-571, 630-644)", P,
        "must_raise is used for exactly the eight named conditions: periods 0 and -1; face 0 and -1; coupon -1; yield -10000 and -20000; quantity 0 and -1; price -1; side 0, 2, -2, 3, -3; settlement_day 0 and -1. "
        "Boundaries accepted: periods 1, face 1, coupon 0, yield -9999, quantity 1, price 0, side +1 and -1, settlement_day 1 (tests 225, 242, 263, 428, 479, 523, 556, 574)."),
    row("proj-test-count", "2.9-count", "project.html line 171 ('68 checks'); grader/test_project.py", P,
        "pytest --collect-only -q in a scratch copy (reference as instruments.py): '68 tests collected' (out/collect_only_r2.out). Page count equals the real count."),
    row("proj-starter-fails", "2.6-autograder-2", "grader/starter.py", P,
        "Starter under the browser flags: '66 failed, 2 passed' (out/starter_local_r2.out; the two that pass accept any exception by design, page lines 163-165). Browser messages name the property and the missing implementation (out/starter_browser_messages_r2.out)."),
    row("proj-instances", "2.6-instance", "grader/instance.py, seeds 0-19", P,
        "Ran ledgers/FC1/scripts/FC1-c-r2/instances_r2.py: all 20 seeds satisfy the page's valid-input rules (asserted) and give 20 distinct bond prices and 20 distinct trade flows (out/instances_0_19_r2.out)."),
    row("proj-silence-purity", "2.6-autograder-3", "grader/test_project.py lines 603-644 (silence), 647-652 (purity)", P,
        "Silence test covers the page's valid boundary list (negative yield, zero yield, zero coupon, zero price, sell side, quantity 1, settlement 1, one cent face, one period, twelve periods) and each named refusal (print only; a warning would be an error under -W error and would fail must_raise). PASS on reference and on all 8 alternatives for seeds 0-19."),
    row("proj-same-suite-pyodide-pytest", "2.6-dual-mode", "grader/test_project.py in Pyodide (page_smoke) and in local pytest", P,
        "Pyodide: 'All 68 tests pass' (out/page_smoke_project.out). Local pytest with the page flags: 68 passed (out/collect_only_r2.out run and scratch runs)."),
    row("proj-mutants-all", "2.6-mutation", "ledgers/FC1/mutants/*.py (84 files: 75 earlier, 5 round-1 v1c_*, 4 new r2c_*)", F,
        "Re-run: tools/mutate_graders.py --unit FC1 --seeds 0-9 -> 'mutate_graders FC1: FAIL (82/84 killed)' (out/mutate_graders_all_r2.out). The two survivors are the round-2 mutants r2c_bond_periods_capped_at_twelve.py and r2c_price_cached_on_first_yield.py; the other 82 are killed (see the mutants array).",
        fix="Add grader tests for the two survivors (rows proj-mutant-periods-13-15-survivor and proj-mutant-price-cache-survivor). Keep the mutant files; re-run mutate_graders.py --unit FC1 --seeds 0-9 until 84/84 are killed."),
    row("proj-mutants-v1c-new", "2.6-mutation", "ledgers/FC1/mutants/v1c_*.py (5 round-1 student-error mutants)", P,
        "Re-run in the mutate output: v1c_simple_discount_not_compound (killed by the 13-15 test, seed 0), v1c_trade_rounded_to_dollars, v1c_yield_guard_missing (killed by test_yield_at_minus_one_is_refused), v1c_price_discounted_at_coupon_rate, v1c_seller_side_refused: all KILLED."),
    row("proj-mutants-v2c-new", "2.6-mutation", "ledgers/FC1/mutants/r2c_*.py (4 round-2 student-error mutants written by this verifier)", P,
        "make_r2_mutants.py wrote four mutants from reference.py, each with a one-line docstring naming the student error: r2c_events_change_on_second_call (KILLED by test_repeated_events_calls_agree, seed 0, but only through a bare assert: see proj-failure-messages); "
        "r2c_trade_settles_one_period_early (KILLED by test_trade_has_one_settlement_event_on_its_settlement_day); r2c_bond_periods_capped_at_twelve (SURVIVED); r2c_price_cached_on_first_yield (SURVIVED). Two of four survive, so the suite is not yet complete; the survivors are the two FAIL rows that follow."),
    row("proj-alternatives", "2.6-autograder-alternatives", "ledgers/FC1/alternatives/a1..a5 and ledgers/FC1/scripts/FC1-c-r2/alt/alt_decimal.py, alt_recurrence.py, alt_integer.py", P,
        "Eight correct alternatives run under the browser flags on seeds 0-19: all pass 68 tests on every seed (out/alternatives_0_19_r2.out). Three are new this round: Decimal in a 60-digit context with ROUND_HALF_UP; exact Fraction discount factors by recurrence v_t = v_(t-1)/(1+y); integer-only price over (10000+yield)**N with one integer rounding. "
        "Sanity: the same runner fails m07_price_without_discounting on all 20 seeds (out/sanity_runner_on_mutants_r2.out)."),
    row("proj-failure-messages", "2.6-autograder-4", "grader/test_project.py lines 647-652 (test_repeated_events_calls_agree, two bare asserts); page line 309", F,
        "Round-1 FAIL partly resolved: the round-1 bare asserts now carry messages, and each function that has a literal expected value sets __tracebackhide__ (scan: ledgers/FC1/scripts/FC1-c-r2/out/scan_leak.out lists only the two bare asserts as visible frames; no literal in a visible frame). "
        "Still FAIL: lines 650 and 652 are bare asserts with no message. Browser message from the worker's Collector for the mutant r2c_events_change_on_second_call is 'AssertionError' only (out/browser_message_bare_assert_r2.out), so the learner sees no property. Plan section 5.5 requires failure messages that name the violated property; the docstring line 12 promises the same.",
        fix="Give both asserts a message naming the property, e.g. 'events() must return the same list on every call, for the bond and for the trade', with no expected value in it."),
    row("proj-cards-scan-duplicates", "2.7-cards", "course/modules/FC/FC1/cards.json (119 cards)", P,
        "ledgers/FC1/scripts/FC1-c-r2/cards_check.py over all 119 cards: ids unique; no duplicate front or back text (out/cards_check.out, problems list empty apart from the Assumption-label false positives below)."),
    row("proj-cards-numbers-in-lessons", "2.7-cards", "cards.json, every digit run of length >= 2 in back vs the lesson text", P,
        "cards_check.py: for all 119 cards every number in the back (commas removed) appears in its own lesson HTML text; zero misses (out/cards_check.out). Derived numbers were recomputed (next row)."),
    row("proj-cards-sample", "2.7-cards (sampled, then re-derived)", "cards.json: the 12 round-1 sample cards (c001, c011, c021, c031, c041, c051, c061, c071, c081, c091, c101, c111) and the numeric cards below", P,
        "Round-1 sample re-checked this round. Numbers recomputed with Fraction (ledgers/FC1/scripts/FC1-c-r2/numbers_r2.py, out/numbers_r2.out): c010 1000(1-0.9^11)/0.1 = 6861.894 -> 686189 cents; c011 1000/0.55 = 1818.18 -> 181818 cents, 18.18 % of 10000; c012 6.8619 x 1000 = 6861.90 vs 6861.89; c016 6.8619; "
        "c037 4985/5015, spread 30, 0.6 %; c043 spread 400, mid-move -1000, profit -600 (L03 Example 2.5 text, read); c052/c053 h V = 2 x 2000 = 4000; c061 159000 and 1060; c082 216 x 10060 = 2172960; c083 2026-10-28 is a Wednesday and 2026-10-30 a Friday; "
        "c084 14282414/68398886 = 0.20881 -> 0.209; c092 181790 (half redeposit) and 686189; c093 100-150 = -50; c097/c098 4000-545 = 3455; c068 and c067 Problem R2/R3 (L04 lines 474-481) read; c029/c030/c033/c034/c095/c096 counts from the Lab 2 register (tests/labs/FC1/lab-FC1-L02-1.py lines 23-40). "
        "Lab-printed numbers (181790, 14282414, -545, 3455, 2172960, 'Friday 2026-10-30', 0.209, 'crossed 0') are in the lesson expected blocks (run_labs all pages PASS). "
        "Not done: a line-by-line re-derivation of all 119 cards against their lesson prose; the other cards were read in full (out/cards_all.txt) and scanned mechanically, so this row covers the sample and the numeric cards only."),
    row("proj-cards-citation-R3", "2.7-cards / 2.9-DAG", "cards.json FC1-c054 (lesson L03)", P,
        "Round-1 FAIL resolved. The back now reads '(Lab 1, Part C)' with no 'Problem R3'. L03.html has 'Lab 1, Part C' output and the 121-pair grid (expected block; 11 asks x 11 asks = 121). Resolved by cards_check.py."),
    row("proj-cards-citation-R2", "2.7-cards", "cards.json FC1-c089 (lesson L05)", P,
        "Round-1 FAIL resolved. The back now cites 'the proof of Proposition 2.1(ii)'. L05.html lines 78-86: the proof of (ii) contains 'By A1 every c_i is non-negative, so Rec_j >= 0 and Pay_j >= 0'. The counterexample numbers recomputed: one trade of -100 gives NP = 100, G = -100."),
    row("proj-cards-citation-scan", "2.7-cards", "cards.json block references (back and basis)", P,
        "cards_check.py resolves every reference against its own lesson. Its only unresolved hits were 'Assumption A1/B1/...' in L03; L03 headings read 'Assumptions A1 to A3' and 'Assumptions B1 to B4' with items 'A1 (trades at the quote)' etc. (L03.html lines 78-80, 133-135), so those resolve."),
    row("proj-cards-grades", "2.7-cards / 2.3-grades", "cards.json grade T and C fields vs lesson data-grade attributes", P,
        "All 23 T-graded cards that cite a Proposition or Corollary cite a claim element carrying data-grade=\"T\" in their own lesson (scripted check this round). The other 16 T cards cite Examples, Remarks or Problems, which are arithmetic or worked results; read, not re-graded."),
    row("proj-spec-scope-vs-curriculum", "2.6-spec (rung 3 matches curriculum scope)", "project.html lines 157, 161; curriculum/02-economics-finance-core.yaml lines 388-395; curriculum/curriculum.json; course/assets/data/program.json", P,
        "Round-1 FAIL resolved. The curriculum brief for FC1 now reads 'Represent a fixed-rate bond and a trade that settles later as dated cash-flow objects ... Futures, swaps and options follow in FC2.' (yaml 390-393); curriculum.json and program.json carry the same text. "
        "FC2 is 'Derivatives Fundamentals' (yaml 396-397). The page (line 157) states the same scope and 'this project uses none of them'; the grader defines only Bond and CashTrade. Architect ruling 5 is satisfied. render_curriculum.py --check and build_site.py --check PASS (out/render_curriculum_check.out, out/build_site_check.out)."),
    row("proj-terminology-short-holder", "2.12-prose", "project.html line 179 (Sides and signs); grader/reference.py docstring line 10", P,
        "Round-1 FAIL resolved. 'long' and 'short' no longer appear in project.html or grader/*.py. The page and reference now say side +1 is the buyer, who pays cash, and -1 the seller, who receives cash."),
    row("proj-prose-banned-phrases", "1.3-1.4 banned phrases", "course/modules/FC/FC1/project.html and cards.json", P,
        "grep -E for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'left as an exercise', 'it is important to note', 'studies show', 'experts agree', 'well known', 'obviously', 'clearly', and process words (builder, verifier, round, ledger, checkout, mutant, plan, Architect): no hits in project.html; 'round' hits in grader/test_project.py are the mathematical word for rounding."),
    row("proj-scope-words", "2.2 / prose scope words", "project.html (changed sentences at lines 174-178, 195-198) and cards", P,
        "Changed scope words read in context: 'Every amount is an int number of cents' (definition), 'No discounted term is rounded' (rule), 'this project uses none of them' (checked against the grader: no Future, Swap or Option), 'the autograder checks some' (checked against the test names, see proj-lab3 note)."),
    row("proj-terms-before-definition", "2.9 terms", "project.html: event, period, settlement period, holder, buyer, seller, trade date", P,
        "event, holder, settlement period and face are defined before use (line 54). Buyer and seller are defined in the sides bullet (line 179) before the trade formula. Trade date is defined by the offset-0 link to L05 (line 177; L05 lines 117 and 'offset 0')."),
    row("proj-notation", "2.9 notation", "project.html symbols y and t (lines 58, 106, 178) vs notation/notation.json", P,
        "notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f and \\mathbb{Q}. The page uses y (per-period yield) and t (period index), neither registered and neither reusing a registered meaning. No registered macro is misused."),
    row("proj-footer-claim", "2.9 footer", "project.html footer line", P,
        "Footer: 'The autograder runs in your browser; nothing you write leaves it.' page_smoke enforces zero requests to any host other than the local server (out/page_smoke_project.out). Saved drafts use the browser store (grader.js lines 30-62)."),
    row("proj-saved-as-you-type", "2.9 claim", "project.html line 'Your code is saved in this browser as you type'; course/assets/js/grader.js", P,
        "grader.js: editor 'input' handler stores the draft with store.put(\"files\", draftKey, ...) after a 400 ms debounce, and restores it on load (lines 30-62)."),
    row("proj-references-reading-list", "2.9 references", "project.html Reading section (data-cite mishkin2021economics, harris2002trading)", P,
        "Both keys exist in references/references.json (verified_by crossref and openlibrary); the page attributes no statement to either. references/ is unchanged since d0f39c09."),
    row("proj-cited-year-conflicts", "2.9 registry", "references/references.json; plans/FC1-build-plan.md line 29", P,
        "Carried from round 1 (references/references.json byte-identical since the previous pin): the registry gives harris2002trading year 2002 and mishkin2021economics year 2021, while the plan's curriculum string gives 2003 and 2022. The page cites the key only, so no year is printed (architect Q3). Recorded in registry_flags, not failed."),
    row("proj-data-simulated", "1.4 honest data", "project.html Inputs, Lab 1 text; grader/instance.py", P,
        "Inputs and labs are SIMULATED and say so (page line 'The values are SIMULATED; none is market data'; instance.py docstring). No data file is read."),
    row("proj-reference-deployment", "repo-wide (not failed)", "course/modules/FC/FC1/grader/reference.py", P,
        "Repo-wide note, not a failure (FINAL-ARCHITECT-RULINGS ruling 4): reference.py is tracked; BLUEPRINT's exclusion is not enforced by any deploy step, which does not yet exist. Recorded for the owner."),
    row("proj-mutant-periods-13-15-survivor", "2.6-mutation / 2.2-numbers", "grader/test_project.py lines 281-292 vs project.html line 171 ('the discounted-sum price ... on bonds of 13 to 15 periods') and line 177 (coupon in each of periods 1 to periods)", F,
        "Mutant ledgers/FC1/mutants/r2c_bond_periods_capped_at_twelve.py (events() stops at period 12, face moved to period 12) SURVIVES all 68 tests on seeds 0-9 (out/mutate_graders_all_r2.out). Cause: the 13-15 test uses Bond(10000, 500, n) at 500 bps, which is exactly par for every n (exact sum 10000 for n = 12..15, recomputed), so a schedule that drops the later coupons still prices at 10000. "
        "The mutant is wrong on the page's own convention (line 177): at 400 bps it prices 10939 for n = 13, 14, 15 while the exact oracle gives 10999, 11056, 11112 (out/bond13_nonpar_r2.out). The page states this check in line 171.",
        fix="In test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period, price the 13-, 14- and 15-period bonds at a yield that is not the coupon rate (e.g. 400 bps) and compare to oracle_price, and/or assert the event list equals oracle_events for those n. Re-run mutate_graders --unit FC1 --seeds 0-9 and require the mutant to die."),
    row("proj-mutant-price-cache-survivor", "2.6-mutation / 2.2-numbers", "grader/test_project.py lines 404-408 (falls as the yield rises) and 411-415; project.html line 178 (price is the present value of the bond at that yield) and line 161 (bond_price_cents returns the present value of the bond's events)", F,
        "Mutant ledgers/FC1/mutants/r2c_price_cached_on_first_yield.py (price cached on the bond object at its first yield) SURVIVES: 68 passed on seeds 0-19 (out/sanity_runner_on_mutants_r2.out; out/mutate_graders_all_r2.out). "
        "Cause: test_bond_price_falls_as_the_yield_rises builds a new Bond for each call (bond_of(INST) twice), so a per-object cache is never reused, and the repeated-call test uses the same yield twice. The page states the price is the present value at the given yield (line 178).",
        fix="Add a test that prices one bond object at two different yields and requires each result to equal oracle_price for its own yield (and that the two differ for a non-zero coupon). Re-run mutate_graders --unit FC1 --seeds 0-9 and require the mutant to die."),
    row("proj-docstring-float-claim", "2.12-prose / 2.2 (docstring vs computation)", "grader/test_project.py lines 394-401 (test_bond_price_exact_half_cent_at_400_bps_uses_the_exact_yield), docstring line 397", F,
        "The docstring says 'the float yield misses this case'. Python: 13/(1+0.04) = 12.5 in float (rounds to 13, correct); only the inverse-multiply float form 13*(1+0.04)**-1 = 12.499999999999998 rounds to 12. "
        "So the case catches one float formula, not the float yield in general, and the reference's own division form does not fail. The test is correct; the sentence overstates it (out/numbers_r2.out, last three lines).",
        fix="Reword the docstring to name the failing form, e.g. 'a float discount factor (1 + 0.04) ** -1 times 13 gives 12.499999999999998 and rounds to 12', or delete the claim."),
    row("proj-named-error-message-values", "2.6-autograder-4 (values in messages)", "grader/test_project.py all assert messages and pytest.fail texts (47 asserts with messages, 7 pytest.fail calls)", P,
        "scan_asserts.py (out/scan_asserts.out) and scan_leak.py (out/scan_leak.out): no assert message or pytest.fail text contains an expected value; the messages hold rule names only. Literal expected values appear in source lines of asserts that set __tracebackhide__, so the local --assert=plain traceback is hidden for them (verified: 'All traceback entries are hidden'). Page line 309 ('no values') is therefore accurate for those tests; the two bare asserts are a separate row."),
]

registry_flags = [
    "harris2002trading: registry year 2002 (crossref), curriculum string 2003 (plans/FC1-build-plan.md line 29); page cites the key only (architect Q3). Carried from round 1.",
    "mishkin2021economics: registry year 2021 (record), curriculum string 2022; page cites the key only (architect Q3). Carried from round 1.",
]

fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 2 (did not build FC1)",
    "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "base": "d0f39c09598ffefaf0ec18d5d1077cfacd42998b (round 1 of this slice, verifyD1-FC1-c)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-FC1-c",
    "scratch": "/tmp/fc1c_r2_scratch, /tmp/fc1c_r2_alts, /tmp/fc1c_r2_starter, /tmp/fc1c_r2_collect (copies of grader files; the evidence is archived under ledgers/FC1/scripts/FC1-c-r2/out)",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": [],
    "notes": (
        "Round 2 of FC1-c on pin c737272. Delta from d0f39c09 read hunk by hunk: project.html (conventions periods and sides, Lab 3 hypothesis), "
        "cards.json (FC1-c054 and FC1-c089 backs), grader/reference.py (docstring only), grader/test_project.py (__tracebackhide__ lines, messages, no logic change), "
        "curriculum yaml/json and program.json (FC1 project brief), plans/FINAL-ARCHITECT-RULINGS.md. Every round-1 non-PASS row was re-verified from scratch: "
        "proj-lab3-claim-using-functions and proj-spec-scope-vs-curriculum and proj-terminology-short-holder and proj-cards-citation-R3/R2 now PASS; proj-failure-messages is still FAIL for two bare asserts; "
        "proj-mutants-all is FAIL because of two new survivors. Every command row was re-run on the pin. "
        "Not checked: the full pytest suite (only the relevant modules: tests/test_page_checks.py, test_run_labs.py, test_curriculum.py, test_labs.py, output in out/pytest_relevant_r2.out); "
        "the live verify_refs (network; only --offline run, 560 entries, 0 problems); the Pyodide run of the four new mutants (the browser suite ran the reference only); "
        "a line-by-line re-derivation of all 119 cards against lesson prose (all read, mechanically checked, sample and numeric cards re-derived). "
        "Repo-wide hygiene: ledgers/FC1/scripts/FC1-c-r2/ already contained tracked files from pin c737272 (alt1-alt5, build_fragment_r2.py, labs_and_cards_audit_r2.py, make_mutants_r2.py, nums_r2.py, run_alternatives.sh); they were not modified or run, and this round's scripts use distinct names. "
        "The hours arithmetic and the 68-check count are consistent; the Lab 3 note lists the checks but omits fixture F's events (test_bond_face_one_cent_is_accepted does check them); this is an incomplete list, not a false sentence, and is not failed."
    ),
    "summary": "",
}
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment["summary"] = (
    f"{len(rows)} rows: {counts.get('PASS', 0)} PASS, {counts.get('FAIL', 0)} FAIL, {counts.get('UNVERIFIABLE', 0)} UNVERIFIABLE. "
    f"Mutants: {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed on seeds 0-9 (2 survivors, r2c_bond_periods_capped_at_twelve and r2c_price_cached_on_first_yield). "
    "Alternatives: 8/8 pass seeds 0-19. Verdict FAIL."
)
out = ROOT / "ledgers/FC1/FC1-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
