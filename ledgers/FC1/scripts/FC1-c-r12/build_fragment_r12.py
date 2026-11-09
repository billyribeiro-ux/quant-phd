"""Build the round-12 FC1-c fragment (ledgers/FC1/FC1-c.json) from this round's command outputs and reads.

Every row id of the round-11 fragment is kept. Carried rows name the files that are byte-identical since the
previous pin (ccaeeaf4); every other PASS row was re-run or re-read this round and cites this round's outputs.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-FC1-c")
OUT = "ledgers/FC1/scripts/FC1-c-r12/out"
PIN = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
CARRY = "Carried from round 11 (files byte-identical since the previous pin ccaeeaf4): "
CARD_BASIS = "course/modules/FC/FC1/cards.json entries other than FC1-c152/FC1-c153 (150 of 151 entries byte-identical since ccaeeaf4; scripts/FC1-c-r12/cards_check_r12.py)"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


def carry(rid: str, check: str, location: str, evidence: str) -> None:
    row(rid, check, location, "PASS", CARRY + evidence)


SCR = "ledgers/FC1/scripts/FC1-c-r12"

# ---- commands run this round (outputs under scripts/FC1-c-r12/out) ----
row("proj-check-projects", "2.6-spec-hours", "course/modules/FC/FC1/project.html",
    "PASS", f"tools/check_projects.py --unit FC1: 'check_projects FC1: PASS' ({OUT}/check_projects.out); hours table sums to 20 = data-hours-project = hub.")
row("proj-check-pages", "2.9-structure", "course/modules/FC/FC1/project.html",
    "PASS", f"tools/check_pages.py --unit FC1: 'check_pages FC1: PASS' ({OUT}/check_pages.out), includes the banned-string and claim-citation checks.")
row("proj-check-dag", "2.9-dag", "project.html; curriculum/curriculum.json concepts",
    "PASS", f"tools/check_dag.py --unit FC1: 'check_dag FC1: PASS' ({OUT}/check_dag.out).")
row("proj-run-labs", "2.5-labs", "project.html Labs 1-3; tests/labs/FC1/lab-FC1-project-{1,2,3}.py",
    "PASS", f"tools/run_labs.py --unit FC1: 8/8 PASS ({OUT}/run_labs.out). Each project twin run as 'python -I -W error' exits 0 with 0 bytes stderr; Lab 1, Lab 2 and Lab 3 stdout equals the page expected blocks (lines 97-100, 145-148, 263-275).")
row("proj-page-smoke", "2.9-smoke", "course/modules/FC/FC1/project.html",
    "PASS", f"tools/page_smoke.py --unit FC1 --pages project (alone): PASS ({OUT}/page_smoke_project.out); in-browser grader 'All 92 tests pass on seed 1397156559'; lab timings 0.0 s each.")
row("proj-run-graders", "2.6-autograder-1", "grader/reference.py, test_project.py, instance.py, starter.py",
    "PASS", f"tools/run_graders.py --unit FC1 --seeds 0-49: 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.3 s)' ({OUT}/run_graders_0_49.out); the tool also checks mypy --strict on the three files and that the starter fails the suite.")
row("proj-lint-types", "2.9-gates", "course/modules/FC/FC1/grader/*.py; tests/labs/FC1/; ledgers/FC1",
    "PASS", f"ruff check . 'All checks passed!' ({OUT}/ruff_check.out); ruff format --check '559 files already formatted'; mypy --no-incremental 'Success: no issues found in 385 source files' ({OUT}/mypy.out).")
row("proj-lab1-numbers", "2.2-numbers", "project.html lines 58, 97-101 (Lab 1)",
    "PASS", f"Numbers re-derived with exact Fractions in {SCR}/numbers_r12.py ({OUT}/numbers_r12.out): events [(1,5000),(2,5000),(3,105000)]; exact PV 102775.091033; price 102775; trade (2,-98500). Line 58 and the expected block agree. The new interpretation (line 101: 'the coupon of step 1 appears in the first printed line') is true: the events line prints (1, 5000).")
row("proj-lab3-fixture-values", "2.2-numbers", "project.html lines 198-275 (Lab 3)",
    "PASS", f"numbers_r12.out: fixture A 10500/10000; B 11052.6316 -> 11053; C [(1,5001),(2,15002)]; D [(1,2)]; rounding case 10278 once vs 10277 term-by-term; E (2,-98500); F 1/2 -> 1 (Python round gives 0); G 5000.5 -> 5001. Lab 3 output ({OUT}/run_labs.out and direct run) equals the expected block.")
row("proj-rounding-fixture-terms", "2.2-numbers", "project.html line 193; grader/test_project.py lines 396-403",
    "PASS", f"numbers_r12.out: exact PV 10277.509103 rounds once to 10278; terms 480.77, 462.28, 9334.46 (float_claims_r12.out) round to 481+462+9334 = 10277. Both match the page and the test docstring.")
row("proj-expected-equals-output", "2.5-labs", "project.html expected blocks lines 97-100, 145-148, 263-275",
    "PASS", f"run_labs.out PASS 8/8; direct run of tests/labs/FC1/lab-FC1-project-{{1,2,3}}.py (stdout captured this round) equals each expected block line for line.")
row("proj-hours-arithmetic", "2.9-hours", "project.html table#hours lines 286-293; data-hours-project line 34; index.html lines 29, 41",
    "PASS", "Rows 1+2+5+4+2+3+3 = 20 (numbers_r12.py 'hours sum 20'); total 20 = data-hours-project 20 = hub data-hours-project 20; hub 50 lessons + 20 project = 70 (curriculum FC1 hours 70); 20/70 = 28.6 % as printed.")
row("proj-ladder", "2.6-ladder", "project.html lines 41-50, 52-151, 153-172, 312-319",
    "PASS", "Read in full: rung 1 worked example with every step annotated (Lab 1); rung 2 completion lab graded instantly (Lab 2, blanks at lines 133 and 140); rung 3 specification with the interface and the autograder; rung 4 stretch marked not graded (line 314). Placement skip rule matches index.html line 69.")
row("proj-named-conditions", "2.6-spec", "project.html lines 163-167; grader/reference.py lines 42-46, 64, 81-87",
    "PASS", "Eight named conditions: Bond periods<1, face<=0, coupon<0; bond_price_cents yield<=-10000; CashTrade quantity<1, price<0, side not in {+1,-1}, settlement_day<1. reference.py raises each of these; test_project.py tests each boundary on both sides (refused: 0/-1, -10000/-20000, side 0/2/-2/3/-3; accepted: 1, -9999, 0, +1/-1).")
row("proj-test-count", "2.6-spec", "project.html line 171; grader/test_project.py",
    "PASS", f"project.html line 171 says 'runs 92 checks'; collect-only in a scratch workspace with reference.py as instruments.py: '92 tests collected' ({OUT}/collect_only.out); 92 'def test_' lines.")
row("proj-starter-fails", "2.6-autograder-1", "grader/starter.py",
    "PASS", f"starter.py is byte-identical since ccaeeaf4 and raises NotImplementedError for every name; run_graders.py (includes its starter-fails check) PASS on seeds 0-49 ({OUT}/run_graders_0_49.out).")
row("proj-instances", "2.6-autograder-2", "grader/instance.py, seeds 0-49",
    "PASS", f"run_graders 0-49 PASS (fingerprint differs across seeds, check_instances). instances_r12.py asserts ranges for seeds 0-19 (face 1000.00-50000.00, coupon 100-900 bps, periods 1-8, yield 50-900 bps, quantity 1-500, price 5000-150000, side +-1, settlement 1-5): all valid.")
row("proj-same-suite-pyodide-pytest", "2.6-autograder-5", "grader/test_project.py; project.html line 309",
    "PASS", f"Pyodide: page_smoke in-browser grader 'All 92 tests pass' ({OUT}/page_smoke_project.out). Local: run_graders.py runs the same flags (-q -p no:cacheprovider --assert=plain -W error) and passes seeds 0-49.")
row("proj-scope-words", "2.9-prose", "project.html lines 163, 171, 176-186",
    "PASS", "'only' at line 163 and 171 ('the page does not name ... as refused') matches the test list; 'every'/'all' statements at lines 176-180 (every amount an int; each events() call returns the same list; a zero amount is kept) are each tested (test_repeated_events_calls_agree; test_bond_zero_coupon_pays_only_the_face_in_the_last_period; test_trade_price_zero_is_accepted_and_kept).")
row("proj-prose-banned-phrases", "2.9-banned", "project.html; cards.json; grader/*.py; labs",
    "PASS", f"check_pages.py FC1 PASS covers the BUILDER_RULES banned-string list in visible prose ({OUT}/check_pages.out).")
row("proj-process-words", "2.9-process-words", "project.html; cards.json; labs; grader",
    "PASS", "grep -i for round N, verifier, builder, architect, ruling, TODO, placeholder, pending, draft, 'this round' in project.html, the labs and the grader: no hits. cards.json hits 'pending stops' (order-book term, cards lines 394, 919) are domain text.")
row("proj-notation", "2.4-notation", "notation/notation.json; FC1 project.html math; cards.json; labs",
    "PASS", "notation.json registers T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q only. project.html math uses y, t, 1+y, (1+y)^{-t} and y = 400/10000 (extracted with a script): no registered symbol. cards.json math uses d, rho, phi, lambda, Sigma and 'E' (Proposition 4.1); none is registered with another meaning.")
row("proj-spec-scope-vs-curriculum", "2.6-spec", "project.html line 157; curriculum/02-economics-finance-core.yaml FC1 project entry (title, brief, grading)",
    "PASS", "curriculum FC1 project: title 'Instrument cash-flow engine', brief 'Represent a fixed-rate bond and a trade ... Futures, swaps and options follow in FC2', grading autograder. Page title 'Instrument Cash-Flow Engine' and line 157 match; FC2 is 'Derivatives Fundamentals' (curriculum line 397).")
row("proj-spec-interface", "2.6-spec", "project.html line 161; grader/starter.py lines 16-40",
    "PASS", "Required names and signatures on line 161 (Bond, events, bond_price_cents, CashTrade, events) equal starter.py lines 16-40 (byte-identical since ccaeeaf4).")
row("proj-spec-questions-r12", "2.6-spec", "project.html section#spec lines 153-172; grader/test_project.py",
    "PASS", "Questions a competent student would ask: (1) whether ValueError is raised in the constructor or in events()/bond_price_cents(): the page does not say; the suite calls both in one expression (must_raise), so either placement passes; not blocking. (2) whether the bond's coupon is on the remaining principal: the page's Conventions and Lab 1 make it face times coupon_bps every period (no amortisation). No other question found.")
row("proj-page-grading-description", "2.9-prose", "project.html line 171; grader/test_project.py",
    "PASS", "Line 171 list read against test_project.py: 1001-period bond (lines 806, 983), 5001 (862), 100001 events only (894), 13-15 periods (281), 24 (304), 40 (318), 100 (791), half-cent and exact-half cases (189-466), yield 150/300/2000/10000/100000 % and 10^16 % (515, 822, 849, 881, 929, 969), settlement 100/1000/5001/10^6/10^7/10^18 (672, 831, 872, 906, 940, 949), quantity 501/1001/2^40+1/10^30/10^60 (577, 587, 597, 915, 959), and silence (693-734). Every item found.")
row("proj-page-line171-count-list", "2.9-prose", "project.html line 171",
    "PASS", "The new count (92) is the collect-only count; the list adds the 10^18 settlement and 10^60 quantity checks, which exist at test_project.py lines 949-956 and 959-966.")
row("proj-page-line98-interpretation", "2.2-prose", "project.html line 101 (Lab 1 interpretation, changed this delta)",
    "PASS", "New sentence 'the printed lines show the results of those steps (the coupon of step 1 appears in the first printed line)': the first printed line is 'bond events ... [(1, 5000), (2, 5000), (3, 105000)]', which contains the coupon 5000. Each comment in Lab 1 names one of steps 1-5 (project.html lines 76-93).")
row("proj-lab2-blanks", "2.5-labs", "project.html lines 133, 140 (Lab 2)",
    "PASS", "Blanks '** ___' (line 133) and '(settlement_day, ___)' (line 140); the completed solution's exponent is period and cash flow is -side * quantity * price_cents; run_labs PASS (twin completed, output matches).")
row("proj-page-hypothesis-sides", "2.5-labs", "project.html line 106 (Lab 2 hypothesis)",
    "PASS", "Hypothesis: 'When both blanks are right, the printed lines are the same as those of Lab 1, and the bond price is 102775 cents' (checked by run_labs; Lab 1 and Lab 2 expected blocks identical).")
row("proj-lab3-autograder-coverage-note", "2.2-prose", "project.html line 276 (note after Lab 3); grader/test_project.py",
    "PASS", "Each claim in the note matches the test list: fixture A events (line 177) and price (371); B price (380); C events (192) and D events (200); E events (539, 547); F events (245) and price (410); G price (418); rounding price (401). Fixture G events and the rounding-case events are not asserted as lists (grep for Bond(10_001, 0, 1) and Bond(10_000, 500, 3) in events() calls: none).")
row("proj-lab3-claim-using-functions", "2.5-labs", "project.html line 198 vs tests/labs/FC1/lab-FC1-project-3.py",
    "PASS", "The hypothesis says the bond uses the lab's functions and the trade uses exact int arithmetic; the twin defines bond_events and bond_price and computes the trade as (2, -10 * 9_850).")
row("proj-hours-rationale-rows", "2.9-hours", "project.html table#hours lines 286-293",
    "PASS", "Each rationale describes its own component (the 'Eight conditions' row matches the eight named conditions at lines 163-167; the 'Local suite on seeds 0 to 9' row is a learner-effort estimate, and the local command is at line 308). Hours are design targets (ruling); arithmetic consistent.")
row("proj-hours-verifier-estimate", "2.6-hours", "project.html table#hours rows 291-292",
    "PASS", "Verifier estimate of the two self-check rows: running the suite on seeds 0-9 and matching fixtures takes about 3 h, and the convention self-check about 3 h, consistent with the 20 h total (ruling: design target, arithmetic consistent).")
row("proj-silence-purity", "2.6-autograder-3", "grader/test_project.py lines 693-734",
    "PASS", "test_the_module_prints_nothing (14 valid inputs under capsys) and test_refused_inputs_print_nothing_before_they_raise (8 named refusals). Both read and run (suite PASS seeds 0-49; mutants v01, c6n01-03, r7n01-03, r8n01-04 killed).")
row("proj-local-command", "2.9-prose", "project.html line 308; grader/starter.py line 6; test_project.py line 5",
    "PASS", "The command 'QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py' matches the flags in tools/run_graders.py PYTEST_FLAGS and the starter/test docstrings (starter.py byte-identical).")
row("proj-terms-before-definition", "2.9-terms", "project.html lines 54-56, 106, 161, 179",
    "PASS", "Read: face, coupon, basis point, per-period yield, event, settlement period and holder are defined on line 54 before first use; 'discount exponent' is a forward reference to Conventions (line 46, allowed by the page); the concept links are checked by check_dag PASS.")
row("proj-footer-claim", "2.9-prose", "project.html line 341; course/assets/js/grader.js; store.js",
    "PASS", "Footer says 'nothing you write leaves it'. grader.js runs the suite in Pyodide on the learner's own code (lines 2-3, 95); store.js keeps the code in IndexedDB. Both files byte-identical since ccaeeaf4; line 341 unchanged in this delta.")
row("proj-saved-as-you-type", "2.9-prose", "project.html line 301; course/assets/js/grader.js lines 33-79; store.js",
    "PASS", "Line 301 claim vs grader.js (editor persisted through store.js); grader.js and store.js byte-identical since ccaeeaf4; line 301 unchanged in this delta.")
row("proj-references-reading-list", "2.9-references", "project.html lines 321-328; references/references.json",
    "PASS", "Lines 321-328 unchanged in this delta; references.json byte-identical since ccaeeaf4; verify_refs --offline: 560 entries, 0 problems ({OUT}/verify_refs_offline.out). The page cites only the two registry keys mishkin2021economics and harris2002trading; McLeay is not cited (index.html line 166).")
row("proj-cited-year-conflicts", "2.1-citations", "project.html reading list; references/references.json (mishkin2021economics, harris2002trading); curriculum/02-economics-finance-core.yaml FC1 sources",
    "PASS", "The page renders registry records: harris2002trading year 2002 (Crossref print_year 2002; registry notes curriculum '2003'); mishkin2021economics year 2021 (Open Library record; registry notes curriculum '13th ed. (2022)'). The page attributes no statement to either book. Both conflicts are recorded in the registry notes and listed in registry_flags.")
row("proj-data-simulated", "2.8-data", "project.html lines 45, 54, 159; grader/instance.py lines 3-6, 31; tests/labs/FC1/lab-FC1-project-*.py",
    "PASS", "The page declares SIMULATED values and no data file (no data-files attribute on any project section; grep). instance.py docstring and label say 'SIMULATED ... not market data'. The labs hard-code their values.")
row("proj-page-constraints-silence", "2.9-prose", "project.html line 163",
    "PASS", "Line 163: the silence statement is limited to the inputs the suite checks, which matches test_the_module_prints_nothing and the named-refusal silence test.")
row("proj-named-error-message-values", "2.6-autograder-4", "grader/test_project.py lines 75-93, 693-734",
    "PASS", "must_raise and must_accept messages name the condition only; no expected value appears in any message (read lines 75-107).")
row("proj-failure-messages", "2.6-autograder-4", "grader/test_project.py lines 693-734, 770-788",
    "PASS", "Messages name the property (e.g. 'a yield above 100 % per period is not refused; the price is the discounted event'); __tracebackhide__ and the NotImplementedError wrapper (lines 770-788) keep answers out of the report.")
row("proj-starter-message-leaks-answer", "2.6-autograder-4", "grader/test_project.py lines 822-828, 849-851, 881-883, 515-517 (and the new lines 949-980)",
    "PASS", "The new messages (e.g. 'a yield above 100 % per period is not refused; the price is the discounted event, rounded once') name no answer.")
row("proj-cards-scan-duplicates", "2.7-cards", "course/modules/FC/FC1/cards.json (152 cards)",
    "PASS", f"cards_check_r12.py: 152 cards; duplicate ids []; duplicate fronts []; duplicate backs []; all lessons exist ({OUT}/cards_check_r12.out).")
row("proj-cards-numbers-in-lessons", "2.7-cards", "cards.json vs L01-L05 lesson text",
    "PASS", f"cards_check_r12.py: for all 152 cards, every number of two or more digits in front or back appears in the card's lesson text (HTML stripped): 0 missing ({OUT}/cards_check_r12.out).")
carry("proj-cards-numbered-references", "2.7-cards", "cards.json citations vs lesson headings",
      CARD_BASIS + "; lesson headings unchanged.")
carry("proj-cards-sample", "2.7-cards", "course/modules/FC/FC1/cards.json (sample of 15 against lesson text)",
      CARD_BASIS + "; sampled cards FC1-c014, c122, c139, c142, c143, c151 among them.")
carry("proj-cards-changed-subjects", "2.7-cards", "cards.json FC1-c064, c101, c147, c150",
      "cards FC1-c064, FC1-c101, FC1-c147, FC1-c150 identical in both pins (cards_check_r12.py, changed = [FC1-c152] only).")
carry("proj-cards-c147-changed", "2.7-cards", "cards.json FC1-c147",
      "FC1-c147 identical in both pins; its lesson L01 Section 2 (S_n = sum D_t, line 86) unchanged.")
carry("proj-cards-c150-changed", "2.7-cards", "cards.json FC1-c150",
      "FC1-c150 identical in both pins.")
carry("proj-cards-new-c143-c151", "2.7-cards", "cards.json FC1-c143 to FC1-c151",
      "FC1-c143 to FC1-c151 identical in both pins.")
carry("proj-cards-citation-scan", "2.7-cards", "cards.json citations (all cards)",
      "citations of the 150 unchanged cards; the citations of FC1-c152 and FC1-c153 (Proposition 3.5, Definition 2.1, Assumptions A1, A2' and A3) are checked this round in proj-cards-c152-hypotheses and proj-cards-c153-hypotheses.")
row("proj-cards-c152-hypotheses", "2.7-cards", "course/modules/FC/FC1/cards.json FC1-c152 (back, grade T); course/modules/FC/FC1/L01.html lines 131-132 and 137",
    "PASS", "FC1-c152 back now states the hypotheses that the Proposition 3.5 statement lists: 0 <= phi <= 1 (A2'), 0 < rho <= 1 (A1, 'Keep A1, with 0 < rho <= 1'), and the no-withdrawal and no-repayment parts of A3 (L01 line 132). Its claim, 'at most d/rho', holds for every d >= 0 (the proof step at L01 line 137 is (1-kappa) - rho = (1-rho)(1-phi) >= 0, so the inequality needs d >= 0). The card needs no d > 0 by its own text, because d > 0 is the standing hypothesis of Definition 2.1 (L01 line 84); the equality part moved to FC1-c153. Checked against the lesson text, not recall. Counter-check: d=-1, phi=0, rho=1/2 gives limit -1 > -2 = d/rho, which is why d >= 0 is needed (scripts/FC1-c-r12/limit_check_r12.py, out/limit_check_r12.out).")
row("proj-cards-c153-hypotheses", "2.7-cards", "course/modules/FC/FC1/cards.json FC1-c153 (back, grade T); L01.html lines 84, 131-132, 137",
    "PASS", "FC1-c153: 'Exactly when phi = 1 or rho = 1, for an initial deposit d > 0 as in Definition 2.1 (Proposition 3.5)'. The equality holds exactly when (1-rho)(1-phi) = 0 for d != 0 (proof, L01 line 137); for d = 0 both sides are 0 for every phi and rho, so the d > 0 hypothesis is needed and the card states it. phi's range comes from A2' ('a share phi with 0 <= phi <= 1'), and rho's range from A1 as restated in A2' ('Keep A1, with 0 < rho <= 1'). Grade T: the proof is on the page.")
row("proj-cards-prop35-lesson-statement", "2.4-mathematics / 2.7-cards", "course/modules/FC/FC1/L01.html lines 131-132 (Proposition 3.5 statement) and 137 (proof); cards FC1-c153",
    "FAIL", "Proposition 3.5 is graded T, and its equality clause 'with equality if and only if phi = 1 or rho = 1' is false for d = 0: with d = 0, phi = 0, rho = 1/2 the limit is 0 and d/rho is 0, so equality holds although neither phi = 1 nor rho = 1 (exact check, scripts/FC1-c-r12/out/limit_check_r12.out). The proof (line 137) silently divides by d. Proposition 3.1 of the same lesson states 'Under Assumption 2.0 with d > 0' (L01 line 104), so the lesson's own practice is to state it; Proposition 3.5 does not. This is the same defect round 11 reported; the card now carries d > 0, but the lesson statement still does not.",
    "Lesson owner: add 'with d > 0' (as in Definition 2.1) to the hypotheses of Proposition 3.5 in course/modules/FC/FC1/L01.html line 132, then re-run render/build checks. No card change needed: FC1-c153 already agrees.")
row("proj-cards-grades", "2.3-grades", "cards.json grade fields vs lesson key-results and lab outputs",
    "PASS", "FC1-c152 and FC1-c153 are grade T with the proof on the page (L01 lines 136-139). Other grade fields are carried: they are byte-identical since ccaeeaf4 (FC1-c014 T with basis; FC1-c030 C with basis; FC1-c091..c096 unchanged).")
row("proj-mutant-r11c-settlement-1e7-survivor", "2.6-mutation", "ledgers/FC1/mutants/r11c_settlement_refused_above_ten_million.py; grader/test_project.py lines 940-956",
    "PASS", f"Killed this round by test_trade_settling_in_period_ten_to_the_eighteenth_is_accepted (seed 0) ({OUT}/mutate_graders_0_19_r12.out).")
row("proj-mutant-r11c-yield-1e7-survivor", "2.6-mutation", "ledgers/FC1/mutants/r11c_yield_refused_above_hundred_thousand_percent.py; grader/test_project.py lines 969-980",
    "PASS", f"Killed this round by test_bond_yield_of_ten_to_the_eighteenth_bps_is_accepted (seed 0) ({OUT}/mutate_graders_0_19_r12.out).")
row("proj-mutant-r11c-quantity-1e30-survivor", "2.6-mutation", "ledgers/FC1/mutants/r11c_quantity_refused_above_ten_to_the_thirtieth.py; grader/test_project.py lines 959-966",
    "PASS", f"Killed this round by test_trade_quantity_of_ten_to_the_sixtieth_is_accepted (seed 0) ({OUT}/mutate_graders_0_19_r12.out).")
row("proj-mutants-r11c-killed", "2.6-mutation", "ledgers/FC1/mutants/r11c_*.py (5 files)",
    "PASS", f"All five r11c mutants KILLED in the round-12 run on seeds 0-19 ({OUT}/mutate_graders_0_19_r12.out).")
row("proj-test-r11-new-tests", "2.6-autograder", "grader/test_project.py lines 925-980 (round-11 tests at 929-946 plus round-12 tests at 949-980)",
    "PASS", "Accepted-input tests read and recomputed: 10**7 bps yield -> 10 cents (929); settlement 10**7 (940); 10**18 settlement (949); 10**60 quantity (959); 10**18 bps yield -> 9999999999999900 (969, exact price 9999999999999900 + 100/(10**14+1) verified with Fraction).")
row("proj-test-r12-new-tests", "2.6-autograder", "grader/test_project.py lines 949-980",
    "PASS", "The round-12 additions (10**18 settlement, 10**60 quantity, 10**18 bps yield) are accepted-input checks on values the page does not name as refused (line 167 names only settlement_day < 1, quantity < 1, yield_bps <= -10000); their expected values are exact and re-derived (numbers_r12.out, float_claims_r12.out).")
row("proj-mutants-all", "2.6-mutation", "ledgers/FC1/mutants/*.py (136 files)",
    "PASS", f"tools/mutate_graders.py --unit FC1 --seeds 0-19: 'mutate_graders FC1: PASS (136/136 killed)' ({OUT}/mutate_graders_0_19_r12.out). Round 11 had 129/132 (three survivors, now killed); the four round-12 mutants are also killed.")
row("proj-mutants-r12c-new", "2.6-mutation", "ledgers/FC1/mutants/r12c_*.py (4 new files)",
    "PASS", "Four new student-error mutants written by the verifier this round, each killed: r12c_face_discounted_one_period_short (killed by test_bond_price_with_thirteen_to_fifteen_periods_uses_every_period), r12c_trade_fee_one_cent (test_trade_has_one_settlement_event_on_its_settlement_day), r12c_discount_base_from_float (test_bond_price_exact_half_cent_at_496_bps_is_exact_not_float), r12c_price_limit_denominator (test_bond_price_just_under_a_half_cent_rounds_down). Each is non-equivalent (differs on the seeded or hand inputs the tests use).")
row("proj-mutants-r10c-new", "2.6-mutation", "ledgers/FC1/mutants/r10c_*.py",
    "PASS", "The r10c mutants are among the 136 KILLED in the round-12 run.")
row("proj-mutant-r10c-yield-10mil-survivor", "2.6-mutation", "grader/test_project.py (test_bond_yield_of_ten_million_bps_is_accepted, line 929)",
    "PASS", "The round-10 survivor is killed: the mutant set run on seeds 0-19 has every r10c file KILLED.")
row("proj-mutant-r10c-settlement-1m-survivor", "2.6-mutation", "grader/test_project.py (test_trade_settling_in_period_ten_million_is_accepted, line 940)",
    "PASS", "KILLED in the round-12 run (r10c_settlement_refused_above_one_million).")
row("proj-mutant-r10c-tail-1000-survivor", "2.6-mutation", "grader/test_project.py (test_bond_price_at_zero_yield_counts..., line 983)",
    "PASS", "KILLED in the round-12 run (r10c_price_ignores_events_after_period_one_thousand).")
row("proj-mutants-v1c-new", "2.6-mutation", "ledgers/FC1/mutants/v1c_*.py", "PASS", "All v1c mutants KILLED in the round-12 run (out/mutate_graders_0_19_r12.out).")
row("proj-mutants-v2c-new", "2.6-mutation", "ledgers/FC1/mutants/r2c_*.py", "PASS", "All r2c mutants KILLED in the round-12 run.")
row("proj-mutants-r3c-killed", "2.6-mutation", "ledgers/FC1/mutants/r3c_*.py", "PASS", "All r3c mutants KILLED in the round-12 run.")
row("proj-mutants-v4c-new", "2.6-mutation", "ledgers/FC1/mutants/v4c_*.py", "PASS", "All v4c mutants KILLED in the round-12 run.")
row("proj-mutants-r4c-new", "2.6-mutation", "ledgers/FC1/mutants/r4c_*.py", "PASS", "All r4c mutants KILLED in the round-12 run.")
row("proj-mutants-r5c-new", "2.6-mutation", "ledgers/FC1/mutants/r5c_*.py", "PASS", "All r5c mutants KILLED in the round-12 run.")
row("proj-mutants-r6c-killed", "2.6-mutation", "ledgers/FC1/mutants/r6c_*.py", "PASS", "All r6c mutants KILLED in the round-12 run.")
row("proj-mutants-r7c-new", "2.6-mutation", "ledgers/FC1/mutants/r7c_*.py", "PASS", "All r7c mutants KILLED in the round-12 run.")
row("proj-mutants-r8c-new", "2.6-mutation", "ledgers/FC1/mutants/r8c_*.py", "PASS", "All r8c mutants KILLED in the round-12 run.")
row("proj-mutants-r9c-new", "2.6-mutation", "ledgers/FC1/mutants/r9c_*.py", "PASS", "All r9c mutants KILLED in the round-12 run.")
for rid, loc in [
    ("proj-mutant-schedule-cap-thirty-survivor", "schedule capped at 30 periods (r4c_schedule_stops_at_thirty_periods)"),
    ("proj-mutant-exponent-cap-thirty-survivor", "discount exponent capped at 30 (r4c_discount_exponent_capped_at_thirty)"),
    ("proj-mutant-schedule-cap-survivor", "schedule capped at 20 periods (r3c_schedule_stops_at_twenty_periods)"),
    ("proj-mutant-price-digits-survivor", "price in ten significant digits (r3c_price_ten_significant_digits)"),
    ("proj-mutant-price-cache-survivor", "price cached on first yield (r2c_price_cached_on_first_yield)"),
    ("proj-mutant-price-epsilon-survivor", "price rounded with epsilon (r5c_price_rounded_with_epsilon)"),
    ("proj-mutant-yield-100-survivor", "yield above 100 % refused (r5c_yield_above_one_hundred_percent_refused)"),
    ("proj-mutant-schedule-cap-forty-survivor", "schedule capped at 40 periods (r6c_schedule_stops_at_forty_periods)"),
    ("proj-mutant-exponent-cap-forty-survivor", "discount exponent capped at 40 (r6c_discount_exponent_capped_at_forty)"),
    ("proj-mutant-yield-200-survivor", "yield above 200 % refused (r6c_yield_above_two_hundred_percent_refused)"),
    ("proj-mutant-settlement-cap-100-survivor", "settlement capped at 100 (r6c_settlement_day_above_one_hundred_refused)"),
    ("proj-mutant-decimal-40-digits-survivor", "price in 40 significant digits (r6c_price_decimal_forty_significant_digits)"),
    ("proj-mutant-decimal-28-digits-kill", "price in default Decimal 28 digits (r6c_price_default_decimal_28_digits)"),
    ("proj-mutant-periods-cap-1000-survivor", "periods refused above 1000 (r7c_periods_refused_above_one_thousand)"),
    ("proj-mutant-r7c-coupon-half-even", "coupon rounded half to even (r7c_coupon_rounded_half_even)"),
    ("proj-mutant-r7c-discount-float", "discount factor in floats (r7c_discount_factor_float_then_exact)"),
    ("proj-mutant-r7c-price-cap-1m", "price refused above 1,000,000 cents (r7c_price_refused_above_one_million_cents)"),
    ("proj-mutant-r7c-hard-coded-answer", "seed-zero constant answer (r7c_price_is_seed_zero_answer_constant)"),
    ("proj-mutant-yield-1000-survivor", "yield above 1000 % refused (r8c_yield_refused_above_one_thousand_percent)"),
    ("proj-mutant-settlement-5000-survivor", "settlement refused above 5000 (r8c_settlement_day_refused_above_five_thousand)"),
    ("proj-mutant-periods-5000-survivor", "periods refused above 5000 (r8c_periods_refused_above_five_thousand)"),
    ("proj-mutant-face-int64-kill", "face refused above int64 (r8c_face_refused_above_int64)"),
    ("proj-mutant-r9c-yield-2000-survivor", "yield above 2000 % refused (r9c_yield_refused_above_two_thousand_percent)"),
    ("proj-mutant-r9c-periods-10000-survivor", "periods refused above 10000 (r9c_periods_refused_above_ten_thousand)"),
    ("proj-mutant-r9c-settlement-10000-survivor", "settlement refused above 10000 (r9c_settlement_day_refused_above_ten_thousand)"),
    ("proj-mutant-r9c-quantity-2pow50-survivor", "quantity refused above 2**50 (r9c_quantity_refused_above_two_to_the_fifty)"),
]:
    row(rid, "2.6-mutation", f"ledgers/FC1/mutants/ ({loc})", "PASS",
        f"Re-run this round: KILLED in mutate_graders.py --unit FC1 --seeds 0-19 ({OUT}/mutate_graders_0_19_r12.out).")
row("proj-lab-io-free", "2.5-labs", "tests/labs/FC1/lab-FC1-project-*.py; grader/*.py",
    "PASS", "grep for open(, urllib, requests, socket, input(: no hits in labs or grader; instance.py uses random.Random seeded by the seed string (deterministic).")
row("proj-terminology-short-holder", "2.9-terms", "project.html line 54",
    "PASS", "'holder' is defined in the parenthesis at its first use on line 54 ('the party that owns the bond').")
row("proj-labs-twins-I-W-error", "2.5-labs", "tests/labs/FC1/lab-FC1-L01..L05-1.py and lab-FC1-project-1..3.py",
    "PASS", "project twins: exit 0 and 0 bytes stderr under python -I -W error (run this round). Lesson twins are run by run_labs --unit FC1 (8/8 PASS).")
row("proj-verify-refs-offline", "2.1-citations", "references/references.json (whole registry, offline)",
    "PASS", f"tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' ({OUT}/verify_refs_offline.out). No live Crossref run (offline only); references.json is byte-identical since ccaeeaf4.")
row("proj-pytest-fc1", "2.9-tests", "tests/test_labs.py, tests/test_curriculum.py, tests/test_page_checks.py (-k FC1)",
    "PASS", f".venv/bin/python -m pytest -q -k FC1 on those three files: exit 0 ({OUT}/pytest_fc1.out). Full repository pytest not run.")
row("proj-ruff-repo-gate-note", "2.9-gates", "repository gate: ruff check . and ruff format --check .",
    "PASS", f"Both pass repo-wide this round ({OUT}/ruff_check.out, ruff_format.out).")
row("proj-test-name-two-thousand-percent", "2.6-autograder", "grader/test_project.py line 849",
    "PASS", "Test name 'two_thousand_percent' and docstring '200000 bps (2000 % per period)' agree: 200000/100 = 2000; expected 10500/21 = 500 (exact, recomputed).")
row("proj-docstring-float-claim", "2.6-autograder", "grader/test_project.py lines 423-427, 448-456, 459-466",
    "PASS", "Recomputed in float_claims_r12.out: 1734792/1.0496 = 1652812.4999999998 in binary floats (exact 3305625/2, so rounds to 1652813); (1+0.04)**-1 * 13 = 12.499999999999998 while 13/1.04 exact = 25/2; the hair-under-half fixture equals 299985000 + 1/2 - 1/(2*1000300030001) exactly.")
row("proj-test-docstring-hand-numbers", "2.6-autograder", "grader/test_project.py docstrings (old and new)",
    "PASS", "Hand numbers in docstrings recomputed: 10277.5091, 480.77/462.28/9334.46 (line 398), 10500/101 = 103.96 -> 104, 10500/1001 = 10.49 -> 10, 10500/2.5 = 4200, 10500/4 = 2625, 10500/21 = 500, 210000/19 = 11052.6316, 5 * 10**39 + 1 for Bond(10**40+1,0,1); all match (numbers_r12.out, float_claims_r12.out).")
row("proj-starter-unwrapped-new-tests", "2.6-autograder", "grader/test_project.py lines 994-997 (wrapper loop over globals after the last test)",
    "PASS", "The wrapper loop is after all definitions, so the round-11 and round-12 tests are wrapped; a NotImplementedError from the starter becomes a named failure (run_graders starter check PASS).")
row("proj-reference-deployment", "2.9-deployment", "BLUEPRINT.md line 401; course/modules/FC/FC1/grader/reference.py line 4; .github/workflows/ci.yml; repository root",
    "UNVERIFIABLE", "BLUEPRINT line 401: deployment publishes course/ and excludes every grader/reference.py. The checkout has no deployment config (no vercel.json or netlify.toml at the root; .github/workflows/ci.yml has no deploy job), and no tool, config or workflow excludes grader/reference.py (git grep). The exclusion cannot be read, so it is unverified. reference.py line 4 states the same gap. The file is git-tracked under course/, which is the directory BLUEPRINT says is published. Repo-wide, not a defect of FC1-c's text.",
    "Architect or CI owner: add the deployment step that publishes course/ without grader/reference.py (for every unit), or record that the site is not published; then re-run this row.")
carry("proj-cards-c139-c142-new", "2.7-cards", "cards.json FC1-c139 to FC1-c142", "FC1-c139 to FC1-c142 identical in both pins.")
carry("proj-cards-c014-lab-true", "2.7-cards", "cards.json FC1-c014; Lab 1 Part A", "FC1-c014 identical in both pins; Lab 1 twin unchanged (run_labs PASS this round).")
carry("proj-cards-c122-equity-after-loss", "2.7-cards", "cards.json FC1-c122; L01 Proposition 4.1", "FC1-c122 identical in both pins; L01.html byte-identical.")
carry("proj-cards-citation-R3", "2.7-cards", "cards.json FC1-c067; L04 Remark 1.2 and Problem R3", "FC1-c067 identical in both pins; L04.html byte-identical since ccaeeaf4.")
carry("proj-cards-citation-R2", "2.7-cards", "cards.json FC1-c068; L04 Problem R2", "FC1-c068 identical in both pins; L04.html byte-identical since ccaeeaf4.")
carry("proj-starter-silence-scope", "2.6-autograder", "course/modules/FC/FC1/grader/starter.py lines 8-10; project.html line 163", "starter.py byte-identical; project.html line 163 unchanged in this delta.")
row("proj-alternatives", "2.6-autograder", "ledgers/FC1/alternatives/a1..a5 (grader suite seeds 0-19)",
    "PASS", f"run_alts_r12.py 0-19: a1..a5 each 'PASS 20/20 seeds pass' ({OUT}/alternatives_0_19.out).")
row("proj-alternatives-r4-new", "2.6-autograder", "scripts/FC1-c-r4/alt/alt6", "PASS", f"run_alts_r12.py 0-19: alt6 PASS 20/20 ({OUT}/alternatives_0_19.out).")
row("proj-alternatives-r6-new", "2.6-autograder", "scripts/FC1-c-r6/alt/alt7..alt9", "PASS", f"run_alts_r12.py 0-19: alt7, alt8, alt9 PASS 20/20 ({OUT}/alternatives_0_19.out).")
row("proj-alternatives-r7-new", "2.6-autograder", "scripts/FC1-c-r7/alt/alt10..alt12", "PASS", f"run_alts_r12.py 0-19: alt10, alt11, alt12 PASS 20/20 ({OUT}/alternatives_0_19.out).")
row("proj-alternatives-r8-new", "2.6-autograder", "scripts/FC1-c-r8/alt/alt13..alt15", "PASS", f"run_alts_r12.py 0-19: alt13, alt14, alt15 PASS 20/20 ({OUT}/alternatives_0_19.out).")
row("proj-alternatives-fixed-suite-r9", "2.6-autograder", "grader/test_project.py (r9 proposal applied) and the alternatives",
    "PASS", "All fifteen earlier alternatives and a1..a5 pass the current suite on seeds 0-19 (no over-constraint).")
row("proj-alternatives-r12-a6", "2.6-autograder", f"{SCR}/alt/r12_a6_floor_plus_half_reduce.py (new this round)",
    "PASS", f"New alternative: half-away by floor(|x| + 1/2), discount by a running division, events built by list append. run_alts_r12.py 0-19: PASS 20/20 ({OUT}/alt_r12_a6_0_19.out).")
row("proj-instances-answers-r12", "2.6-autograder", f"{SCR}/instances_r12.py; grader/instance.py",
    "PASS", f"Seeds 0-19: 20 distinct prices and 20 distinct settlement events; all instance values inside the valid ranges ({OUT}/instances_r12.out).")

# ---- mutants: every KILLED line of this round's run ----
mutants = []
for line in (ROOT / OUT / "mutate_graders_0_19_r12.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+)\.py: (.*) -> (\S+) \(seed (\d+)\)$", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": f"{m.group(3)} (seed {m.group(4)})"})
    elif line.startswith("SURVIVED"):
        raise SystemExit("a mutant survived: " + line)

registry_flags = [
    "mishkin2021economics: registry year 2021 (Open Library record) vs curriculum '13th ed. (2022)'; needs a published-version check and a curriculum or registry correction (not checked live: offline run).",
    "harris2002trading: registry year 2002 (Crossref) vs curriculum '(2003)'; the page shows 2002; curriculum string needs correction.",
]
notes = (
    "Round 12, FC1-c, independent verifier (Haiku 5.5). Pin 329c1d7 (round-11 fix commit); previous pin ccaeeaf4. "
    "Delta in slice: project.html lines 101 (Lab 1 interpretation) and 171 (92 checks, extended list); grader/test_project.py "
    "(three round-12 accepted-input tests at lines 949-980, comment at 925-926); cards.json FC1-c152 back changed and FC1-c153 added. "
    "Byte-identical since ccaeeaf4: grader/reference.py, instance.py, starter.py, labs twins, L01.html, index.html, references.json, "
    "grader.js, store.js, alternatives a1-a5. Round-11 FAILs: proj-cards-c152-hypotheses (now PASS: the card carries the statement's hypotheses; the d > 0 gap is in the lesson, see proj-cards-prop35-lesson-statement); "
    "proj-mutants-all and the three r11c survivors (now killed: 136/136). FAIL rows: proj-cards-prop35-lesson-statement (L01 Proposition 3.5 statement and its equality clause need d > 0; lesson owner, L01.html line 132); "
    "proj-reference-deployment (UNVERIFIABLE: BLUEPRINT line 401 requires deployment to exclude grader/reference.py; no deployment config or exclusion exists in this checkout: .github/workflows/ci.yml has no deploy job and no tool or config excludes it; repo-wide, not in this slice's files). "
    "Could not check: the live Crossref/Open Library run (offline only); the deployed site (none configured); the full repository pytest (only -k FC1 subset); a manual browser session beyond page_smoke; "
    "Pyodide execution of the four new mutants (local pytest only; the mutants are killed locally and the suite is the same file); the rounding and labels in Lab 2's completion check beyond run_labs; hours are design targets (ruling)."
)

rows_ids = [r["id"] for r in rows]
dups = sorted({i for i in rows_ids if rows_ids.count(i) > 1})
assert not dups, dups
fails = [r["id"] for r in rows if r["status"] != "PASS"]
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
fragment = {
    "unit": "FC1",
    "slice": "c",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1-c, round 12 (did not build FC1)",
    "pin": PIN,
    "base": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87 (round-11 pin of this slice); delta ccaeeaf4..329c1d7 in slice as described in notes",
    "checkout": str(ROOT),
    "scratch": f"{SCR}/ (numbers_r12.py, float_claims_r12.py, cards_check_r12.py, run_alts_r12.py, make_mutants_r12.py, instances_r12.py, alt/r12_a6_floor_plus_half_reduce.py); outputs in {OUT}/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": [],
    "notes": notes,
    "summary": {
        "rows_total": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": {"killed": len(mutants), "total": len(mutants)},
    },
}
(ROOT / "ledgers/FC1/FC1-c.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "non-PASS:", fails, "mutants", len(mutants))
