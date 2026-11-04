"""Build the FC2-d round-8 fragment from the round-7 fragment (carry rule) and this round's fresh evidence.

Usage: python -I build_fragment_fc2d_r8.py <checkout>
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/FC2/scripts/FC2-d-r8"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/D-FC2-d.round7.json", encoding="utf-8"))
CARRY = "Carried from round 7 (course/modules/FC/FC2/project.html lines 1-673 except the exemplar hunk at 581-620, grader/starter.py docstring and cards.json except FC2-c104, c143, c156, c157 are byte-identical since the previous pin 9373ef3 for this row's subject): "

fresh = {}


def row(id_, check, location, status, evidence, fix=""):
    fresh[id_] = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix}


# ---- gates (run this round on 2d75559) ----
row("fc2d-r2-gate-mutate", "2.6", "tools/mutate_graders.py --unit FC2 --seeds 0-9", "FAIL",
    f"{S}/mutate_fc2_r8.out: 'mutate_graders FC2: FAIL (76/79 killed)', rc 1. The 76 prior mutants are KILLED. "
    "SURVIVED: x8_a_cost_checked_only_when_a_parity_finding_is_kept.py, x8_b_short_chain_skips_validation_in_convexity.py, "
    f"x8_c_one_strike_chain_skips_quote_length_check.py (written by this verifier, ledgers/FC2/mutants/). {S}/mutant_probe_r8.out "
    "shows the reference raises ValueError on each named-condition chain where the survivor returns a value (rows fc2d-r8-mut-x8-a/b/c).",
    "Add to grader/test_project.py one test per survivor (see fc2d-r8-mut-x8-a/b/c) and rerun tools/mutate_graders.py --unit FC2 until 79/79 are killed.")
row("fc2d-r2-gate-run-graders", "2.5/2.6", "tools/run_graders.py --unit FC2 --seeds 0-49", "PASS",
    f"{S}/run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.3 s)', rc 0.")
row("fc2d-r2-gate-check-projects", "2.6", "tools/check_projects.py --unit FC2 and --all", "PASS",
    f"{S}/check_projects_fc2.out: 'check_projects FC2: PASS' rc 0; {S}/check_projects_all.out: 'check_projects FC2: PASS' rc 0.")
row("fc2d-r2-gate-check-dag", "2.9", "tools/check_dag.py --all (FC2 line) and --unit FC2", "PASS",
    f"{S}/check_dag_all.out: 'check_dag FC2: PASS' rc 0; {S}/check_dag_fc2.out: 'check_dag FC2: PASS' rc 0.")
row("fc2d-r2-gate-check-pages", "2.9", "tools/check_pages.py --all (FC2 line) and --unit FC2", "PASS",
    f"{S}/check_pages_all.out: 'check_pages FC2: PASS' rc 0; {S}/check_pages_fc2.out: 'check_pages FC2: PASS' rc 0.")
row("fc2d-r2-gate-run-labs", "2.5", "tools/run_labs.py --unit FC2", "PASS",
    f"{S}/run_labs_fc2.out: 'run_labs FC2: PASS (11/11)', rc 0.")
row("fc2d-r2-lab-twins-isolated", "2.5", "project twins alone under python -I -W error", "PASS",
    "project twins run by this verifier from an empty temp dir "
    "with '.venv/bin/python -I -W error lab.py': lab 1 rc 0 stderr 0 B; lab 2 rc 0 stderr 0 B; lab 3 rc 0 stderr 0 B; "
    f"stdout saved to {S}/project_lab{{1,2,3}}_stdout.out.")
row("fc2d-r2-lab-page-equals-twin", "2.5", "page code equals twin; expected block equals output", "PASS",
    "Re-run this round with a regex over course/modules/FC/FC2/project.html: lab 1 and lab 3 page code equals the twin line for line "
    "(the page block lacks only the final newline); lab 2 page code differs from its twin only at lines 58, 60 and 73, the three "
    "blanks ('gap = ___', 'net = ___' twice). Each expected block equals the twin's stdout (True for labs 1, 2, 3).")
row("fc2d-r2-gate-page-smoke", "2.9", "tools/page_smoke.py --unit FC2 --pages project", "PASS",
    f"{S}/page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 90 tests pass on seed 1998231570', rc 0.")
row("fc2d-r2-gate-ruff-mypy", "2.6", "ruff check, ruff format --check, mypy --no-incremental", "PASS",
    f"{S}/ruff_check.out: 'All checks passed!' rc 0; {S}/ruff_format_repo.out: '553 files already formatted' rc 0 (repo-wide); "
    f"{S}/mypy.out: 'Success: no issues found in 385 source files' rc 0.")
row("fc2d-r2-gate-pytest-fc2", "2.5/2.6", "relevant pytest (FC2 filter)", "PASS",
    f"{S}/pytest_fc2.out: pytest tests/labs/FC2 tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py -k 'FC2 or fc2 or project or grader' -q: dots only, '[100%]', rc 0.")
row("fc2d-r2-gate-verify-refs", "2.1", "verify_refs --offline and --unit FC2", "PASS",
    f"{S}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' rc 0; {S}/verify_refs_unit_FC2.out: 'live re-verification of FC2: 3 of 560 entries, 0 problems' rc 0.")
row("fc2d-r2-collect-count", "2.6", "collected checks equal the page count, every seed 0..49", "PASS",
    f"{S}/collect_count.out (collect_count_r8.py, python -I, reference.py as scanner.py): 'collected 90 for 50 seeds', rc 0. project.html line 320 states 90.")
row("fc2d-r2-starter-suite-fails", "2.6", "the suite fails on starter.py", "PASS",
    "Re-run this round on the changed starter.py (docstring line 23-24): starter.py as scanner.py, QF_SEED=0, pytest -W error: '82 failed, 8 passed', rc 1.")
row("fc2d-r2-numbers-lab1", "2.2", "Lab 1 numbers (project.html 55-163)", "PASS",
    f"{S}/labout (Lab 1 twin run via project_lab1 stdout {S}/project_lab1_stdout.out) matches the expected block; re-derived by hand: "
    "gaps 0, 120, 0, 0, -20, 0 at 9000..11500 (C-P-(S-Kdf)); cost 3 x 15 = 45; nets -45, 75, -45, -45, -25, -45; chord-less-call 50, 100, -75, 75 at 9500, 10000, 10500, 11000; "
    "kept: 9500 parity (net 75) and 10500 convexity (net 30). Interpretation line 163 agrees.")
row("fc2d-r2-numbers-lab3", "2.2", "Lab 3 numbers (project.html 376-486)", "PASS",
    f"{S}/project_lab3_stdout.out (Lab 3 twin, rc 0) equals the expected block: gaps 0, -60, 0, 0, 226, 540 at 4000..7000; cost 60; chord-less-call 35, 470/3, -188/3 (gross 63, net 3), 59; "
    "kept 6500 (226/166), 7000 (540/480), 6000 convexity (63/3). Interpretation line 486 ('about minus 62.67' = 188/3) agrees.")
row("fc2d-r2-numbers-exemplars", "2.2", "exemplar numbers (project.html 520-634)", "PASS",
    "Re-derived with exact fractions: Exemplar B parity 6500 = 151 - 1100 - (5000 - 6175) = 226, net 166; parity 7000 = 90 - 1200 - (5000 - 6650) = 540, net 480; "
    "convexity 6000: chord (500 + 2*151)/3 = 802/3, less 330 = -188/3, gross 63, net 3. Exemplar A (project.html line 584-619) quotes 'about 226', 'about 540', 'about 63': "
    "rounded forms of the same values. The round-8 hunk changes annotation and score text only (line 584 data-scores, 586 verdict, 618-619 annotations); no number changed.")
row("fc2d-r2-hours", "2.6", "hours arithmetic and hub consistency", "PASS",
    CARRY + "project.html line 33 data-hours-project=\"30\" and the time-budget table (lines 345-352: 2+3+5+9+3+5+3 = 30). Carried from round 7; "
    "re-checked: 30 + 60 (lessons) = 90, as in round 7.")
row("fc2d-r2-banned-phrases", "2.9", "banned phrases and process words", "PASS",
    f"{S}/page_text_checks.out (page_text_checks_r8.py over project.html, 674 lines): 'about' hedges only at lines 486 and 590; "
    "no banned-phrase hit and no process/pronoun hit in the changed hunk.")
row("fc2d-r2-notation", "2.4", "notation against notation/notation.json", "PASS",
    f"{S}/page_text_checks.out: 'macro commands []'. notation/notation.json registers T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q; "
    "a grep of project.html finds none of them (count 0). The page's local symbols C, P, S, K, D and df are defined at lines 335-336; "
    "the label P (P1 to P6) is disclosed as a different use of P on the same line.")
row("fc2d-r2-dag", "2.9", "check_dag and concepts outside the closure", "PASS",
    f"{S}/check_dag_fc2.out: 'check_dag FC2: PASS'. The round-8 hunk (project.html 581-620) adds no concept link; "
    "the prerequisites are unchanged (curriculum/02-economics-finance-core.yaml unchanged since 9373ef3).")
row("fc2d-r2-instances", "2.6", "autograder item 2: instance validity and seed variation", "PASS",
    f"{S}/instances_and_links.out: 40 seeds (0..19, 1000..1019) all valid, '40 distinct (kind, index, amount, strikes, spot, df) tuples'; "
    "'starter.py suite rc 1', '82 failed, 8 passed'; internal #links 18, targets missing []; grader links resolve.")
row("fc2d-r2-grader-over-constraint-case", "2.6", "correct alternatives pass with case-insensitive rule names", "PASS",
    f"{S}/alts_r8.out (run_alts_r8.py, python -I, the suite on seeds 0..49): all 10 alternatives 50/50 (alt1..alt8 carried from round 7, alt9_integer_only_parity.py and alt10_cross_multiplied_convexity_no_fraction.py new this round); "
    "each agrees with reference.py on 3000/3000 random chains.")
row("fc2d-r2-rubric-calibration", "2.6", "blind calibration of exemplars A and B", "PASS",
    "Re-verified from the rubric cells (project.html lines 504-512) with the rubric text only. Exemplar A C3: the note names the discount factor for the parity findings (line 614) and no label P1 to P6, "
    "so level 2 ('Names assumptions for some findings') is met and level 3 is not: official C3 = 2 (data-scores '2,1,2,2,1', line 584), with the verdict (line 586) and annotations (lines 618-620) saying so. "
    "The round-7 defect (C3 scored 1 with an annotation that claimed level 2 was missed) is resolved. Other exemplar scores agree blind: B 4,4,3,3,3; A C1 2, C2 1, C4 2, C5 1.")
row("fc2d-r2-mut-r7-docstrings", "2.6", "mutant docstrings (first line describes the error)", "PASS",
    f"Re-run this round on all 79 mutants in ledgers/FC2/mutants: every first docstring line names the error (listed in {S}/mutate_fc2_r8.out).")
row("fc2d-r2-mut-new-killed", "2.6", "round-2 new mutants v07..v10 killed", "PASS",
    f"{S}/mutate_fc2_r8.out: v07_convexity_indices_returned_in_decreasing_order, v08_convexity_scan_skips_first_interior_strike, v09_parity_explanation_omits_P3_no_income, v10_convexity_gross_from_rounded_chord: KILLED.")
row("fc2d-r2-mut-r5d-resolved", "2.6", "round-1 survivor r5_d (historical)", "PASS",
    "The mutant file r5_d_explanation_direction_reversed.py is no longer in ledgers/FC2/mutants at 2d75559 (git history shows it was renamed; "
    "no current row depends on it). The mutant set at this pin is fully killed by the gate (76 of 79 killed, the 3 new survivors are the fail rows fc2d-r8-mut-x8-*). "
    "Recorded as historical, not as a current claim.")
row("fc2d-r2-mut-equivalents", "2.6", "no equivalent mutant in the set", "PASS",
    f"{S}/mutant_probe_r8.out shows the three new survivors differ from the reference on named-condition chains, so none is equivalent. The 76 prior mutants are killed (equivalence not re-argued beyond the kill).")
row("fc2d-r2-cards-full-scan", "2.6", "cards: unique ids, fronts, backs; near-duplicate review", "PASS",
    f"{S}/cards_refs_r8.out: 155 cards, no duplicate fronts, 0 flags; cards.json ids unique (python check). The round-7 duplicates (c139/c156, c140/c157) are gone: "
    "FC2-c156 and c157 are replaced by FC2-c158 and c159, whose fronts ask different questions (L04 Propositions 2.2 and 2.3 and A1; L04 A2 for options). "
    "c139/c140 are about L02's A1 and A2, which differ from L04's A1 and A2 in content (L02 A2 concerns the underlying's frictionless trading; L04 A2 permits short sales of options). Near-duplicate review: no duplicate.")
row("fc2d-r2-cards-refs-numbers", "2.1/2.6", "every numbered reference on each card appears in its lesson", "PASS",
    f"{S}/cards_refs_r8.py (numbered references: Definition, Proposition, Theorem, Lemma, Corollary, Remark, Example, Assumption, Section, A1..A8) and {S}/cards_refs_r8.out: 0 flags. "
    f"{S}/cards_numbers_r8.py: every decimal or integer of two or more digits in each card appears in its own lesson HTML or in the FC2 lab twins: 0 misses.")
row("fc2d-r2-cards-lab-numbers", "2.5", "cards c012, c013, c095, c147, c148 and the other lab-basis cards", "PASS",
    f"{S}/labout/lab-FC2-L01-1.out: c012 (1/2, 9/10), c013 ((-5, 9): cost 0, payoffs 22 and 4), c147 (30 arbitrage portfolios, holdings -10..10), c138 (-1/5 and 11/10); "
    f"{S}/labout/lab-FC2-L06-1.out: c095, c148 (3/4 share, bond -30, cost 45), c094 (45), c137 (75); "
    "lab-FC2-L02-1.out: c021 (5126.58), c023 (-2126.58, -626.58, 873.42, 2373.42), c024 (73.42), c027 (237.11); lab-FC2-L03-1.out: c038 (84), c045 (0.049026), c046 (-4415468), c133 (days 4, 6, 7, 10 with -35, -13, -36, -22), c134 (4902625); "
    f"lab-FC2-L05-1.out: c072, c073 (-300 at 10000), c074, c075 (0, 100, 800 recomputed), c079, c155; lab-FC2-L07-1.out: c109, c111, c114; lab-FC2-L08-1.out: c126 (L = 4.8771 printed), c129 (rejection message printed); c131 recomputed (120 e^-0.05 = 114.15 > 100, so L = 0); c127's 4.90 is in the lesson text (Problem M2), not printed by the lab.")
row("fc2d-r8-card-c110-c111-c117", "2.2/2.6", "cards c110, c111, c117 (Lab 1 of L07: binomial errors)", "PASS",
    f"Recomputed with python -I (binomial tree, S=K=100, r=0.05, sigma=0.2, tau=1): errors in cents -91.0082 at 2 steps (c110: -91 printed, -91.01 unrounded), "
    f"+171.17 at 1, +35.54 at 5, +7.04 at 25, -3.99 at 50, -2.00 at 100, -1.00 at 200, -0.4998 at 400 (c117: -0.4998 cents); sign pattern + at 1, 5, 25 and - at 2, 10, 50, 100, 200, 400 (c111). "
    f"lab-FC2-L07-1.out shows the same rounded values; the lesson text carries '91.01' (L07.html once), '0.0049977' (twice) and '0.4998' (three times), so the unrounded values are on the page.")
row("fc2d-r8-card-c104", "2.6", "course/modules/FC/FC2/cards.json FC2-c104 (grade T); L07.html Proposition 1.5 lines 110-111", "PASS",
    "The card's hypothesis 'Under the formula of Definition 1.3' is the hypothesis of Proposition 1.5 (L07.html line 111: 'Under Definition 1.3, C depends on S, K, r tau and sigma sqrt(tau) only'). "
    "The 'no drift term' sentence is in the proof (line 114). Agrees.")
row("fc2d-r8-card-c143", "2.6", "course/modules/FC/FC2/cards.json FC2-c143; L04.html line 63 (A4)", "PASS",
    "A4 (L04.html line 63): 'The riskless rate r is constant over the life of the contract and compounded continuously. The discount factor from date t to date tau is e^{-r(tau - t)}.' "
    "The card's answer and its 'A4 of Lesson 4' locator agree.")
row("fc2d-r8-card-c158", "2.6", "course/modules/FC/FC2/cards.json FC2-c158; L04.html lines 111, 249 and 247 (Section 3 heading)", "PASS",
    "L04.html line 249 (inside 'Section 3 · Where the canon breaks', heading at line 247): 'Proposition 2.2 uses A2 and A3, and Proposition 2.3 uses the same two together with A5. Neither uses A1, so both hold whether or not the underlying pays income.' "
    "The card's 'Both use A2 and A3, and Proposition 2.3 also uses A5' and '(Lesson 4, Section 3)' locator agree.")
row("fc2d-r8-card-c159", "2.6", "course/modules/FC/FC2/cards.json FC2-c159; L04.html line 61 (A2)", "PASS",
    "L04.html line 61 (A2): 'There are no transaction costs and no bid-ask spread. The underlying and the options can be sold short, and cash can be lent and borrowed at the riskless rate.' "
    "The card's 'Yes' and '(A2 of Lesson 4)' agree.")
row("fc2d-r8-alt-9-10", "2.6", "new alternatives: integer-only parity (alt9) and cross-multiplied convexity with net >= 1 cutoff (alt10)", "PASS",
    f"{S}/alts/alt9_integer_only_parity.py and alt10_cross_multiplied_convexity_no_fraction.py: 50/50 seeds each in {S}/alts_r8.out; 3000/3000 random-chain agreement with reference.py each.")
row("fc2d-r8-exemplar-level-labels", "2.6", "project.html line 351 and the exemplar data-level attributes (lines 520, 584)", "FAIL",
    "The hours row (line 351) says the learner should 'compare with exemplar level 4 and exemplar level 2'. The rubric defines levels per criterion (lines 504-512) and no level for a note. "
    "Exemplar B carries data-level=\"4\" (line 520) but its official scores are 4,4,3,3,3 (line 520 data-scores), so it is not a level-4 note on every criterion; Exemplar A carries data-level=\"2\" with scores 2,1,2,2,1. "
    "A learner reads 'level 4' as all criteria at 4.",
    "Replace 'exemplar level 4 and exemplar level 2' at line 351 with 'Exemplar B and Exemplar A', and either drop data-level from lines 520 and 584 or define it as the note's lowest criterion level (which gives 3 for B and 1 for A).")
row("fc2d-r8-mut-x8-a", "2.6", "grader/test_project.py: cost validation only when a parity finding is kept (mutant x8_a)", "FAIL",
    f"ledgers/FC2/mutants/x8_a_cost_checked_only_when_a_parity_finding_is_kept.py SURVIVED tools/mutate_graders.py (seeds 0-9; {S}/mutate_fc2_r8.out). "
    f"{S}/mutant_probe_r8.out: scan(chain with fee -1, half-spread 4, one strike with gap 0) returns [] in the mutant; the reference raises ValueError('cost terms must be non-negative'). "
    "project.html line 309 states: 'The named error conditions raise ValueError ... Each condition is checked in every function that receives the input it names, and the grader checks it in each of those functions', and lists 'fee_cents_per_contract or half_spread_cents is negative: in scan' (lines 309-316). "
    "No test in test_project.py calls scan with a negative cost on a chain that keeps no finding (the negative-cost tests at lines 550-561 use chains that keep a finding).",
    "Add a test in grader/test_project.py: scan on a one-strike chain with fee=-1, half_spread=4 and call=put=0 must raise ValueError matching 'non-negative'; add the matching half-spread case. Rerun mutate_graders until x8_a is KILLED.")
row("fc2d-r8-mut-x8-b", "2.6", "grader/test_project.py: convexity_violations short-circuit for fewer than three strikes (mutant x8_b)", "FAIL",
    f"ledgers/FC2/mutants/x8_b_short_chain_skips_validation_in_convexity.py SURVIVED ({S}/mutate_fc2_r8.out). {S}/mutant_probe_r8.out: convexity_violations([100,110],[5,5], df_ppm=0) returns [] in the mutant; the reference raises ValueError('df_ppm must lie in 1 to 1000000'). "
    "project.html line 309 states: 'df_ppm is not in 1 to 1000000: in each of the three functions, the message says that df_ppm must lie in 1 to 1000000'. No test covers a two-strike chain with a bad df_ppm (test_df_outside_range_is_rejected at lines 489-495 uses three strikes).",
    "Add to test_project.py: convexity_violations([100, 110], [5, 5], 0) and with df_ppm = PPM + 1 must raise ValueError matching 'df_ppm'; add a two-strike length-mismatch case. Rerun mutate_graders until x8_b is KILLED.")
row("fc2d-r8-mut-x8-c", "2.6", "grader/test_project.py: scan skips the quote-length check for one-strike chains (mutant x8_c)", "FAIL",
    f"ledgers/FC2/mutants/x8_c_one_strike_chain_skips_quote_length_check.py SURVIVED ({S}/mutate_fc2_r8.out). {S}/mutant_probe_r8.out: scan(one strike, call [5], put [0, 0]) returns one parity finding in the mutant; the reference raises ValueError('calls and puts need one quote per strike: 1 strikes, 1 calls, 2 puts'). "
    "project.html lines 313 states: 'calls_cents or put_cents does not have one quote per strike: ... in scan it applies to both lists; the message names the lengths' (the condition list in lines 309-316). The length tests (lines 507-541) all use three strikes.",
    "Add to test_project.py: scan(hand_chain([100], [5], [0, 0])) must raise ValueError naming the lengths (1 strike, 2 puts), and the calls-too-long one-strike case. Rerun mutate_graders until x8_c is KILLED.")
row("fc2d-r2-scope-curriculum-brief", "2.6", "Rung 3 matches the curriculum scope", "FAIL",
    "Re-verified from scratch on 2d75559: curriculum/02-economics-finance-core.yaml lines 427-429 still read 'Given an embedded option-chain snapshot, detect put-call parity and convexity violations net of a stated cost model'. "
    "project.html states the chain is SIMULATED and no market data is embedded (project.html line 285, 'No market data is embedded'). plans/FC2-build-plan.md line 635 (Architect decisions, binding) allows a SIMULATED chain with a DATA_REQUEST; plans/FC2-open-items.md D1 is still open. "
    "The curriculum brief is unchanged, so the scope mismatch is unchanged.",
    "Architect: amend the brief in curriculum/02-economics-finance-core.yaml lines 427-429 to the SIMULATED-chain scope in plans/FC2-build-plan.md line 635, or clear D1 with a sourced snapshot.")
row("fc2d-r7-card-c156", "2.6", "cards.json FC2-c156 (round-7 id)", "PASS",
    "Subject removed: FC2-c156 no longer exists in cards.json at 2d75559 (its content is replaced by FC2-c158, verified in fc2d-r8-card-c158). Recorded as superseded.")
row("fc2d-r7-card-c157", "2.6", "cards.json FC2-c157 (round-7 id)", "PASS",
    "Subject removed: FC2-c157 no longer exists in cards.json at 2d75559 (its content is replaced by FC2-c159, verified in fc2d-r8-card-c159). Recorded as superseded.")
row("fc2d-r7-grader-convexity-docstring", "2.6", "grader/starter.py and reference.py: convexity docstring says 'strictly above'", "PASS",
    "starter.py lines 23-24 and reference.py line 68 both say 'strictly above the chord'; the round-7 defect (starter drops 'strictly') is resolved at 2d75559.")
row("fc2d-r7-cards-delta-read", "2.6", "cards.json delta since 9373ef3 read in full", "PASS",
    "git diff 9373ef3 2d75559 -- course/modules/FC/FC2/cards.json: four cards changed: FC2-c104 (back, qualifier added), FC2-c143 (front and back), FC2-c156 renamed to FC2-c158 (content replaced), FC2-c157 renamed to FC2-c159 (content replaced). Each read and checked (fc2d-r8-card-c104, c143, c158, c159).")
row("fc2d-r7-mut-s7-new-killed", "2.6", "round-7 new mutants s7_a..s7_d killed", "PASS",
    f"{S}/mutate_fc2_r8.out: s7_a_parity_gap_discounts_the_spot, s7_b_convexity_loop_runs_past_last_strike, s7_c_convexity_net_omits_half_spread, s7_d_parity_gap_floors_the_signed_gap: all KILLED.")
row("fc2d-r3-exemplar-scores-match-text", "2.6", "exemplar scores agree with their annotations", "PASS",
    "project.html line 520 data-scores '4,4,3,3,3' matches the verdict 'C1 4 · C2 4 · C3 3 · C4 3 · C5 3'; line 584 data-scores '2,1,2,2,1' matches 'C1 2 · C2 1 · C3 2 · C4 2 · C5 1' (line 585-586); the C3 annotations (lines 618-620) say 'Meets C3 level 2' and 'Misses C3 level 3', consistent with 2.")
row("fc2d-r3-scope-changed-hunks", "2.6", "every hunk changed since the previous pin is read", "PASS",
    "git diff 9373ef3 2d75559 for the slice: project.html hunk 581-620 (exemplar A scores, verdict and annotations; read in full), grader/starter.py (docstring; read), cards.json (four cards; read). "
    "No other FC2 slice-d file changed (test_project.py, reference.py, instance.py, tests/labs/FC2/*, mutants and alternatives of round 7 are byte-identical; this round adds three mutants).")
row("fc2d-r3-mut-new-killed", "2.6", "round-3 student-error mutants q3_a..q3_d killed", "PASS",
    f"{S}/mutate_fc2_r8.out: q3_a_df_rounded_to_four_places, q3_b_gross_tie_toward_zero, q3_c_convexity_charges_two_legs, q3_d_convexity_explanation_omits_P5: KILLED.")
row("fc2d-r3-mut-prior-untracked", "2.6", "round-3 mutants r3_a..r3_d re-run", "PASS",
    f"{S}/mutate_fc2_r8.out: r3_a_half_spread_halved_again, r3_b_puts_longer_than_strikes_accepted, r3_c_net_field_reports_gross, r3_d_parity_explanation_names_P5_for_P4: KILLED.")
row("fc2d-r4-mut-u4-new-killed", "2.6", "round-4 new mutants u4_a..u4_c killed", "PASS",
    f"{S}/mutate_fc2_r8.out: u4_a_parity_explanation_omits_P6, u4_b_cost_ignores_half_spread, u4_c_discounted_strike_floor_division: KILLED.")
row("fc2d-r5-mut-w5-new-killed", "2.6", "round-5 new mutants w5_a..w5_c killed", "PASS",
    f"{S}/mutate_fc2_r8.out: w5_a_parity_gap_truncated_toward_zero, w5_b_length_check_rejects_only_short_lists, w5_c_gross_rounded_up_to_ceiling: KILLED.")
row("fc2d-r5-alt7-cross-multiplied", "2.6", "alt7_cross_multiplied_integers in the suite", "PASS",
    f"{S}/alts_r8.out: alt7_cross_multiplied_integers.py 50/50 seeds; 3000/3000 agreement with reference.py.")
row("fc2d-r6-mut-w6-new-killed", "2.6", "round-6 new mutants w6_a..w6_d killed", "PASS",
    f"{S}/mutate_fc2_r8.out: w6_a_convexity_counts_call_on_chord, w6_b_chord_weights_by_own_distance, w6_c_finding_kept_when_net_is_zero, w6_d_half_spread_charged_once_per_finding: KILLED.")
row("fc2d-r6-alt8-forward-price", "2.6", "alt8_forward_price_fraction in the suite", "PASS",
    f"{S}/alts_r8.out: alt8_forward_price_fraction.py 50/50 seeds; 3000/3000 agreement with reference.py.")


# ---- assemble: keep every round-7 row id in order; carry PASS rows whose subject is byte-identical ----
def carry_files(id_):
    if id_.startswith(("fc2d-r2-card", "fc2d-r4-card", "fc2d-r5-card", "fc2d-r6-card", "fc2d-r7-card")) or "card" in id_:
        return "course/modules/FC/FC2/cards.json (this card's entry is unchanged since 9373ef3; only FC2-c104, c143, c156, c157 changed)"
    if "mut" in id_:
        return "ledgers/FC2/mutants (the named mutant files are unchanged since 9373ef3)"
    if "alt" in id_:
        return "ledgers/FC2/scripts/FC2-d-r7/alts (unchanged)"
    if "page" in id_ or "exemplar" in id_ or "rubric" in id_ or "spec" in id_ or "hours" in id_ or "hub" in id_ or "reading" in id_ or "footer" in id_ or "autograder" in id_ or "banned" in id_ or "scope" in id_:
        return "course/modules/FC/FC2/project.html (the cited lines are outside the round-8 hunk 581-620)"
    return "course/modules/FC/FC2/grader/test_project.py, grader/reference.py and the cited lesson or reference files (unchanged since 9373ef3)"


rows = []
seen = set()
for old in prev["rows"]:
    id_ = old["id"]
    seen.add(id_)
    if id_ in fresh:
        rows.append(fresh[id_])
        continue
    if old["status"] != "PASS":
        raise SystemExit(f"non-PASS round-7 row not re-verified: {id_}")
    ev = old["evidence"]
    rows.append({"id": id_, "check": old["check"], "location": old["location"], "status": "PASS",
                 "evidence": f"Carried from round 7 ({carry_files(id_)} byte-identical since the previous pin 9373ef3): " + ev,
                 "fix": ""})
for id_, r in fresh.items():
    if id_ not in seen:
        rows.append(r)

# ---- mutants: parse the gate output ----
mut = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
for line in (root / S / "mutate_fc2_r8.out").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mut.append({"name": name, "description": desc.strip(),
                "killed_by": None if status == "SURVIVED" else killed.strip()})

killed = sum(1 for x in mut if x["killed_by"])
counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"), "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
assert len(mut) == 79, len(mut)
frag = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 8 (did not build FC2)",
    "pin": "2d755599d8d74df292e3e43025f0458c4053802e",
    "base": "9373ef3 (round-7 pin); the delta is listed in notes",
    "checkout": str(root),
    "scratch": f"{S}/ (alternatives in {S}/alts, probes and recomputations in the same folder)",
    "verified_at": "2026-11-04T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mut,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 8 on pin 2d75559 (round-7 pin 9373ef3). Delta inside FC2-d (git diff 9373ef3 2d75559): project.html hunk 581-620 "
        "(exemplar A data-scores 2,1,2,2,1, verdict, C3 annotations; exemplar B untouched); grader/starter.py docstring 'strictly above' restored; "
        "cards.json: FC2-c104 back qualified, FC2-c143 front/back rewritten, FC2-c156 and c157 removed and replaced by FC2-c158 and c159. "
        "No change to test_project.py, reference.py, instance.py, tests/labs/FC2, lessons, curriculum, plans, references or notation. "
        "This round adds three student-error mutants (x8_a..x8_c, all SURVIVED) and two correct alternatives (alt9, alt10). "
        "Observations (not rows): (a) Lab 2 page code equals its twin except the three blanks; labs 1 and 3 page code equals the twin except a trailing newline. "
        "(b) The historical row fc2d-r2-mut-r5d-resolved refers to a mutant file no longer present at 2d75559 (renamed in git history); recorded as historical. "
        "(c) Round-6 observation on float alternatives vs project.html line 308 is still open for the architect and not counted. "
        "Not run: the full repo gate (render_curriculum.py, build_site.py --check, fetch_data.py --check, run_graders for other units, pytest for all of tests/); those belong to other slices or to the unit gate."
    ),
    "summary": (
        f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL. "
        "FAIL: fc2d-r2-gate-mutate (mutate gate 76/79, exit 1), fc2d-r8-mut-x8-a, fc2d-r8-mut-x8-b, fc2d-r8-mut-x8-c (grader coverage of named conditions on clean or short chains), "
        "fc2d-r8-exemplar-level-labels (undefined 'exemplar level' wording), fc2d-r2-scope-curriculum-brief (curriculum brief not amended). "
        f"Mutants: {len(mut)}, {killed} killed, {len(mut) - killed} survived (x8_a, x8_b, x8_c)."
    ),
}
out = root / "ledgers" / "FC2" / "FC2-d.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mut), "killed", killed)
