"""Build the round-6 fragment for E1 slice d from the verifier's recorded results (verifier r6, pin 44f1eb6)."""
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
S = "ledgers/E1/scripts/E1-d-r6"
PIN = "44f1eb6"
PREV = "09b87514c240fd5cc904939ec6aba2ca0388ede4"
P = "course/modules/E/E1/project.html"
G = "course/modules/E/E1/grader/test_project.py"
C = "course/modules/E/E1/cards.json"
MUT = "ledgers/E1/mutants"


def row(i, check, loc, status, evidence, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r


rows = [
    # ---- project page: numbers, derivations, labs, spec
    row("E1d-proj-lab1-numbers", "2.2 numbers / 2.5 labs", f"{P} lab-E1-project-1 (lines ~40-70)", "PASS",
        f"{S}/lab-E1-project-1.out via tests/labs/E1/lab-E1-project-1.py; expected block equals output (page_vs_twin.py: "
        "expected==output True). Recomputed by hand: monopoly 50/70/2500/1250/3750/1250; Cournot 200/3, 160/3, 20000/9, "
        "20000/9, 40000/9, 5000/9 -> 67/53/2222/2222/4444/556; Bertrand 100/20/0/5000/5000/0."),
    row("E1d-proj-lab2-numbers", "2.2 numbers / 2.5 labs", f"{P} lab-E1-project-2", "PASS",
        f"Completion lab; twin run output equals expected block (GRADER-IDENTICAL). Iterate error (1/2)^60 * d/3 < 1e-12 "
        "checked; welfare 40000/9 -> 4444 recomputed."),
    row("E1d-proj-lab3-tie-numbers", "2.2 numbers / 2.5 labs", f"{P} lab-E1-project-3", "PASS",
        f"{S}/lab-E1-project-3 twin output equals expected block. Recomputed a=121: monopoly fee 141/2->71, volume 101/2->51, "
        "profit 10201/4->2550, CS 1275.125->1275, W 3825.375->3825, DWL 1275.125->1275; Cournot 67/54/2267/2267/4534/567; "
        "Bertrand 101/20/0/5101/5101/0 (all matched)."),
    row("E1d-proj-lab-twins", "2.5 labs", "tests/labs/E1/lab-E1-project-{1,2,3}.py; "
        f"{P} data-run blocks", "PASS",
        f"run_labs --unit E1: 12/12 PASS ({S}/run_labs_E1.txt). Twins run alone under python -I -W error, exit 0 "
        f"({S}/twin_project_*.out). {S}/page_vs_twin.py: project-1 and project-3 page code == twin; project-2 page code differs "
        "from its twin only in the two '___' blanks (completion problem, graded by labs.js 'completion' class); its expected "
        "block equals the twin output. Lab 1 and Lab 2 docstring wording changed since round 5 (checked on HEAD)."),
    row("E1d-proj-prop1", "2.4 mathematics", f"{P} prop-1 (id=prop-1)", "PASS",
        "Re-derived: pi(Q) = -Q^2/b + (d/b)Q, pi' = (d-2Q)/b, Q*=d/2, fee (a+bc)/(2b), profit d^2/(4b). Checked by hand."),
    row("E1d-proj-prop2", "2.4 mathematics", f"{P} prop-2 (id=prop-2)", "PASS",
        "Re-derived best response max(0,(d-q_j)/2); case analysis excluding q_1=0 (q_2=d/2, q_1=d/4>0); symmetric d/3; "
        "fee (a+2bc)/(3b); profit per exchange d^2/(9b); iteration error d/(3*2^k) with e_{k+1}=-e_k/2. All confirmed."),
    row("E1d-proj-prop3", "2.4 mathematics", f"{P} prop-3 (id=prop-3)", "PASS",
        "Case analysis re-read: f1<c, f1>c with f2>f1, f1=f2>c (deviation g=(f+c)/2 gain (f-c)/2*(a-bg)), f1=c<f2. "
        "Each deviation's gain sign checked; (c,c) equilibrium checked."),
    row("E1d-proj-prop4", "2.4 mathematics", f"{P} prop-4 (id=prop-4)", "PASS",
        "CS = int_0^Q (Q-t)/b dt = Q^2/(2b); W'(x)=(d-x)/b; W(d)-W(Q)=(d-Q)^2/(2b); CS+profit = G(Q)-cQ identity checked."),
    row("E1d-proj-prop5", "2.4 mathematics / 2.6 spec", f"{P} prop-5 (id=prop-5)", "PASS",
        f"{S}/instance_and_order_check.py: brute force over b in 1..3, c in 1..60, d in 6b+1..400 (69,840 triples) found 0 "
        "printed-ordering failures for volumes, fees, welfare, DWL and profit. Exact differences d/6, d/3, d/(6b), d/(3b), "
        "d^2/(18b), 5d^2/(72b), d^2/(36b) re-derived."),
    row("E1d-proj-spec-constraints", "2.6 spec", f"{P} section 'Rung 3 · Specification' (dl.spec)", "PASS",
        "Inputs, outputs, key set, int types, ValueError table and messages match reference.py check_inputs and test_project.py "
        "tests. Browser stop 120 s matches course/assets/js/python.js:4 (TIMEOUT_MS = 120000). Test count 125 matches "
        f"collect-only output (ledgers/E1/scripts/E1-d-r6/alts_collect_probe.txt) and the page text."),
    row("E1d-proj-hours", "2.6 hours", f"{P} section 'Time budget' (#hours)", "PASS",
        "Components 2+3+8+8+6+3 = 30 equals the table total and the hub split (course/modules/E/E1/index.html: 90 lessons + 30 "
        "project = 120). Own estimates: Rung 1 about 1-2 h, Rung 2 about 2-3 h, five proofs 7-9 h, engine plus suite about 4-8 h, "
        "memo with appendix 6-8 h, self-assessment 2-3 h: within 30 % of 30."),
    row("E1d-proj-rubric-structure", "2.6 rubric", f"{P} table#rubric", "PASS",
        "Six criteria x four levels; each descriptor is observable (counts, named elements, numbers). Coverage note only: C6 "
        "level 2 ('one or two limits') does not describe a memo naming all three limits with partial outcomes; no descriptor "
        "gap is marked FAIL."),
    row("E1d-proj-exemplar-blind-scoring", "2.6 rubric calibration", f"{P} #exemplar-a, #exemplar-b", "PASS",
        "Blind scores from the rubric alone: Exemplar A 1,2,2,2,1,2 (official 1,2,2,2,1,2); Exemplar B 4,4,4,4,3,2 (official "
        "4,4,4,4,3,2). Every criterion within one level."),
    row("E1d-proj-exemplar-annotation-C6", "2.6 rubric calibration", f"{P} #exemplar-b, annotation for C6 level 2", "FAIL",
        "Annotation reads 'Meets C6 level 2: names the three limits, with no outcome stated for linear demand or for two "
        "exchanges.' The level-2 descriptor is 'Names one or two of the limits without what changes', so naming three does "
        "not match that descriptor's wording. The score 2 is still right.",
        "Reword the level-2 annotation to match the descriptor, for example 'Meets C6 level 2: names all three limits, but gives "
        "an outcome only for constant cost; the level-2 descriptor is met by the limits named without the changes for linear demand and two exchanges'."),
    row("E1d-proj-autograder-reference", "2.6 autograder 1", "course/modules/E/E1/grader/reference.py; run_graders", "PASS",
        "run_graders --unit E1 --seeds 0-49: 'run_graders E1: PASS (reference 50/50 seeds)' "
        f"({S}/run_graders_E1_seeds0-49.txt). Local pytest with QF_SEED=0 -W error on the reference: 125 passed."),
    row("E1d-proj-autograder-instances", "2.6 autograder 2", "course/modules/E/E1/grader/instance.py", "PASS",
        "Seeds 0-19 sampled: all valid (a > bc > 0, d > 6b), 20 distinct inputs and 20 distinct output vectors. Ranges "
        "b 1-3, c 5-60, d 60-400 match the page. SIMULATED label present on the page."),
    row("E1d-proj-mutant-float-rounding", "2.6 mutation (surviving mutant)", f"{G}; ledgers/E1/mutants/r6d_m01_half_up_in_float_wrong_for_large_inputs.py",
        "FAIL",
        f"Mutant rounds with math.floor(float(x)+0.5). tools/mutate_graders.py --unit E1 --seeds 0-9 "
        f"({S}/mutate_E1_seeds0-9_r6.txt): SURVIVED, 'mutate_graders E1: FAIL (91/92 killed)'. It is wrong on a=15000000000000002, "
        "b=1, c=1 (Cournot volume 10^16+2/3 printed 10000000000000000, must be 10000000000000001; see "
        f"{S}/large_input_check.py). The page says each money output is an exact fraction (project.html Constraints dd) and "
        "volume_trades is the exact volume rounded once. No test uses inputs large enough to separate float from exact arithmetic.",
        "Add a test with a large exact input, e.g. a=15000000000000002, b=1, c=1, comparing every structure with the exact "
        f"oracle. {S}/probe_float_kill.sh shows it kills the float mutant (3 failures) and passes reference.py and "
        "alt3_cramer.py and alt2_decimal_half_up.py."),
    row("E1d-proj-mutant-new-m02", "2.6 mutation", f"{G}; r6d_m02", "PASS",
        "Profit as fee times volume (revenue). Killed by test_closed_form_matches[profit_cents-monopoly] on seed 0."),
    row("E1d-proj-mutant-new-m03", "2.6 mutation", f"{G}; r6d_m03", "PASS",
        "Over-constrained a<2bc raise. Killed by test_smallest_valid_case_is_accepted[103-3-34-monopoly] on seed 0."),
    row("E1d-proj-mutant-new-m04", "2.6 mutation", f"{G}; r6d_m04", "PASS",
        "Welfare = CS/2 + profit. Killed by test_closed_form_matches[welfare_cents-monopoly] on seed 0."),
    row("E1d-proj-mutant-new-m05", "2.6 mutation", f"{G}; r6d_m05", "PASS",
        "Monopoly fee sign error (a-bc)/(2b). Killed by test_closed_form_matches[fee_cents-monopoly] on seed 0."),
    row("E1d-proj-mutant-existing", "2.6 mutation (all existing)", f"{MUT}/*.py (87 prior mutants)", "PASS",
        f"Re-run in full on this pin: {S}/mutate_E1_seeds0-9_r6.txt shows every mutant except r6d_m01 KILLED, including all 87 "
        "prior mutants (r*, v*, vx*, f*, fx*, m*)."),
    row("E1d-proj-alt-integer-pairs", "2.6 autograder over-constraint (alternative correct implementation)", f"{G} test_non_integer_inputs_do_not_yield_float_money; {S}/alt1_integer_pairs.py",
        "FAIL",
        f"alt1 (exact integer pairs, half-up by integer arithmetic) is correct for every whole-number int input. "
        f"{S}/alts_collect_probe.txt: it fails test_non_integer_inputs_do_not_yield_float_money[args0] (120.0) and [args2] "
        "(20.0) on every seed, because it returns float money for float inputs. project.html Inputs says 'Three whole numbers' "
        "and Constraints says 'Any other invalid input may raise any exception or return a value', so the page never requires "
        "int output for float inputs. The test over-constrains.",
        "Either state in the Inputs that a, b and c are Python ints and make float inputs 'invalid', then delete the float "
        "cases (the page permits any value for them), or drop the float-output requirement from the test. Do not require int "
        "output for inputs the page calls invalid."),
    row("E1d-proj-alt-cramer", "2.6 alternative implementation", f"{S}/alt3_cramer.py", "PASS",
        "Passes all 125 tests on seeds 0-49 (alts_collect_probe.txt: 0 failing seeds)."),
    row("E1d-proj-alt-decimal", "2.6 alternative implementation", f"{S}/alt2_decimal_half_up.py", "PASS",
        "Decimal at 60 digits with ROUND_HALF_UP passes on seeds 0-49 (0 failing seeds)."),
    row("E1d-proj-alt-trapezoid", "2.6 alternative implementation", f"{S}/alt4_trapezoid_consumer.py", "PASS",
        "Two-panel trapezoid consumer surplus passes on seeds 0-49 (0 failing seeds)."),
    row("E1d-proj-pyodide-local", "2.6 autograder 5 / 2.9 smoke", "tools/page_smoke.py --unit E1 --pages project", "PASS",
        "page_smoke E1 PASS; 'in-browser grader: All 125 tests pass on seed 1977596653'. Local: QF_SEED=0 -W error pytest on "
        "reference gives 125 passed."),
    row("E1d-proj-ruff-mypy", "2.9 gates", "tests/labs/E1; course/modules/E/E1/grader", "PASS",
        f"{S}/ruff.txt: 'All checks passed!', 16 files formatted. {S}/mypy.txt: 'Success: no issues found in 14 source files' "
        "(mypy --no-incremental)."),
    row("E1d-proj-check-gates", "2.9 structure gates", "tools/check_projects.py, check_dag.py, check_pages.py, run_labs.py, verify_refs.py", "PASS",
        f"{S}/check_projects.txt 'check_projects E1: PASS'; {S}/check_dag.txt exit 0; {S}/check_pages.txt 'check_pages E1: PASS'; "
        f"{S}/verify_refs_offline_all.txt 'offline integrity: 560 entries, 0 problems'. Live verify_refs --unit was not run "
        "(the tool's --unit flag is live-only); the Varian record was checked by plain curl instead."),
    row("E1d-proj-reference-varian", "2.1 citation (project 'Reading')", "references/references.json key varian2014intermediate; project.html #reading", "PASS",
        "Open Library plain curl https://openlibrary.org/books/OL28519988M.json returned title 'Intermediate Microeconomics', "
        "publish_date 2014, ISBN 9780393919677, publisher 'Norton & Company, Incorporated, W. W.'; author key OL530867A "
        "resolves to 'Hal R. Varian'. Matches the registry entry. The page attributes no passage, so no locator is needed."),
    row("E1d-proj-notation", "2.4 notation", "notation/notation.json; project.html", "PASS",
        "Registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q-blackboard) are not used on the project page. Local letters (F, q, Q, d, a, b, c) are defined in the model section."),
    row("E1d-proj-banned", "2.9 banned phrases", f"{P}; {C}", "PASS",
        "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, "
        "important to note, obviously, clearly, well known, experts agree, studies show, can be shown, roughly, historically, "
        "verifier, builder: 0 hits. 'about' appears only in deliberately weak Exemplar A text."),
    row("E1d-proj-delta-r5", "delta since pin 09b8751", f"{P}; {G}; tests/labs/E1/lab-E1-project-{{1,2}}.py", "PASS",
        "git diff 09b8751..44f1eb6 read hunk by hunk: test count 118 -> 125 (new tests test_unit_cost, test_smallest_positive_b, "
        "test_import_prints_nothing), importlib import, wording changes in the labs and the page. Each new test was read; "
        "I checked all three against reference.py and they pass."),
    row("E1d-proj-reading-section", "2.9 structure", f"{P} section 'Reading'", "PASS",
        "Lists the only registry key; no statement attributed to it; no locator claimed. Consistent with the registry entry."),
    # ---- retrieval cards
    row("E1d-cards-sample-010", "2.7 cards (sample 1 of 13)", f"{C} E1-c010", "PASS",
        "MRS = p_x/p_y at the optimum (Proposition 2.3 from Proposition 1.4); lesson L01 Prop 2.3 text matches."),
    row("E1d-cards-sample-020", "2.7 cards (sample 2 of 13)", f"{C} E1-c020", "PASS",
        "pi(q*) - pi(0) = (p-c)^2/(4k) re-derived; matches L02 Remark 1.6."),
    row("E1d-cards-sample-030", "2.7 cards (sample 3 of 13)", f"{C} E1-c030", "PASS",
        "p* = (a+sc)/(b+s), s = n/(2k), Q* = s(p*-c), p*-c = (a-bc)/(b+s): re-derived; matches L03 Prop 1.3."),
    row("E1d-cards-sample-040", "2.7 cards (sample 4 of 13)", f"{C} E1-c040", "PASS",
        "epsilon = -bp/(a-bp) re-derived from Q'(p) p / Q; matches L04 Example 1.3."),
    row("E1d-cards-sample-050", "2.7 cards (sample 5 of 13)", f"{C} E1-c050", "PASS",
        "dQ*/da = S'(p*) dp*/da = 20/22 = 10/11 at a=120; matches L04 Example 2.4 and Lab 1 Part B."),
    row("E1d-cards-sample-060", "2.7 cards (sample 6 of 13)", f"{C} E1-c060", "PASS",
        "p_m - c = (a-bc)/(2b) = half the distance from c to a/b; re-derived; L05 Prop 5.2 proof."),
    row("E1d-cards-sample-070", "2.7 cards (sample 7 of 13)", f"{C} E1-c070", "PASS",
        "Monopoly d/2, fee (a+bc)/(2b), profit d^2/(4b) from Lemma 1.3; matches L06 Prop 1.4."),
    row("E1d-cards-sample-080", "2.7 cards (sample 8 of 13)", f"{C} E1-c080", "PASS",
        "Bertrand: lower fee takes whole volume max(0,a-bf); tie rule; L06 Definition 3.1 and Theorem 3.3 'any tie rule'."),
    row("E1d-cards-sample-090", "2.7 cards (sample 9 of 13)", f"{C} E1-c090", "PASS",
        "R(0)=d/2 and R(x)=(d-x)/2 falls by half a unit; L06 Lemma 2.4."),
    row("E1d-cards-sample-100", "2.7 cards (sample 10 of 13)", f"{C} E1-c100", "PASS",
        "Reference surplus values: CS 1250, PS 2500, W 3750, DWL 1250 (monopoly); DWL Cournot 5000/9 -> 556; competitive W 5000; matches Lab output L07."),
    row("E1d-cards-sample-110", "2.7 cards (sample 11 of 13)", f"{C} E1-c110", "PASS",
        "Off-diagonal interior allocation improvable (L08 Prop 2.2); hypotheses X>0, Y>0 carried on the card."),
    row("E1d-cards-sample-120", "2.7 cards (sample 12 of 13)", f"{C} E1-c120", "PASS",
        "MSC = c+e; q_s = (a-c-e)/b; q_p = (a-c)/b re-derived; L09 Def 1.2."),
    row("E1d-cards-sample-130", "2.7 cards (sample 13 of 13)", f"{C} E1-c130", "PASS",
        "Tax 100: q = (1000-200-100)/10 = 70; loss (b/2)(70-68)^2 = 20 with b = 10; matches L09 Misconception 3."),
    row("E1d-cards-full-scan-duplicates", "2.7 cards duplicates", f"{C} (133 cards)", "PASS",
        "Full scan of ids and normalised front+back text: no duplicate id and no duplicate card (card_check.py, duplicate checks = 0)."),
    row("E1d-cards-lab-graded", "2.7 cards / 2.5 labs", f"{C} grade C cards", "PASS",
        "The 14 C-graded cards (c014, c025, c027, c036, c051, c066, c084, c085, c105, c115, c129, c131, c132, c133) match the "
        "lesson lab outputs in ledgers/E1/scripts/E1-d-r6/lab-E1-L0*-1.out (e.g. 2650 vs 2700 cents; 15 grid-efficient; 80/68 units; "
        "9.391047e-7 and 3.880758e-11; step 25)."),
    row("E1d-cards-numbers-in-lesson", "2.7 cards / rule 10 numbers", f"{C}; lessons L01-L09", "PASS",
        f"{S}/card_check.py: every numeric token in every card occurs in its lesson text (0 number-not-in-lesson findings). "
        "This presence check is weaker than the manual recomputation of each card's formula, which I also did for all 133 cards."),
    row("E1d-cards-labels-resolve", "2.7 cards / rule 10 labels", f"{C} (18 cards citing 'Misconception N')", "FAIL",
        f"{S}/card_check.py reports 18 'label-missing' problems, all 'Misconception 1/2/3' (E1-c012, c024, c026, c035, c048, c049, "
        "c050, c062, c063, c064, c102, c104, c116, c117, c118, c128, c129, c130). Every lesson has exactly three misconception "
        "items (class 'misconception'), but none prints a number, so the reader cannot match the card's reference. The "
        "numbers are ordinal and the mapping is correct. ('Section 3' in c102 is printed as a section-number span and resolves.)",
        "Print the number in each misconception item of every lesson (for example a block-title 'Misconception 1.' before the "
        "wrong statement), or cite the card's Misconception by its quoted wrong statement."),
    row("E1d-cards-profit-sign-c019", "2.7 cards correctness", f"{C} E1-c019", "FAIL",
        "Card: 'Their profits differ by F' - F.' L02 Proposition 1.5 says the profit under F' equals the profit under F minus "
        "F' - F at every output. The card drops the sign.",
        "Replace with: 'The profit under F' is lower than under F by F' - F, at every output.'"),
    row("E1d-cards-hypotheses", "2.7 cards carry the hypotheses (rule 10)", f"{C} E1-c023, E1-c041, E1-c075", "FAIL",
        "Cards cite results whose lesson statements carry hypotheses that the card omits: E1-c041 ('For linear demand...', "
        "Proposition 1.4 assumes a > 0 and b > 0); E1-c075 (Lemma 2.4 is stated under the hypotheses of Definition 1.1, "
        "including b > 0, c > 0, a > bc); E1-c023 (Proposition 2.2 is under the Setting, k > 0). The round-5 edits did add hypotheses "
        "to other cards (E1-c004, c006, c008, c039, c067, c093, c095, c096), which I checked.",
        "Add the cited result's hypotheses to each named card, e.g. E1-c041 'With a > 0 and b > 0, |epsilon(p)| > 1 exactly when p > a/(2b)'."),
    row("E1d-cards-delta-r5", "delta since pin 09b8751", f"{C}", "PASS",
        "git diff 09b8751..44f1eb6 cards.json read hunk by hunk (24 changed lines): renames u* -> u_bar, hypothesis additions "
        "(E1-c004, c006, c008, c010, c039, c067, c093, c095, c096), E1-c012 and c013 wording. Each changed card checked against the "
        "current lesson text. No new card is unsupported."),
    row("E1d-cards-lessons-tier", "2.7 cards agree with current lesson text", f"{C}; course/modules/E/E1/L01-L09.html", "PASS",
        f"Every card's lesson, definition, proposition and lab reference was checked against the lesson text (block titles listed "
        f"by script). Only the defects in the two FAIL rows above were found."),
    row("E1d-cards-read-complete", "2.7 full read", f"{C}", "PASS",
        "All 133 cards read in full (ids E1-c001 to E1-c133) with the lesson HTML they cite; no card skipped."),
]

mutants = [
    {"id": "r6d_m01", "description": "Student rounds with float(x) + 0.5, exact on small cases, loses the half on large exact fractions.",
     "killed_by": None},
    {"id": "r6d_m02", "description": "Student takes exchange profit as fee times volume (revenue), forgetting the cost c per trade.",
     "killed_by": "test_closed_form_matches[profit_cents-monopoly] (seed 0)"},
    {"id": "r6d_m03", "description": "Student over-constrains the input: rejects a < 2*b*c, so valid cases with bc < a < 2bc raise ValueError.",
     "killed_by": "test_smallest_valid_case_is_accepted[103-3-34-monopoly] (seed 0)"},
    {"id": "r6d_m04", "description": "Student reads welfare as half the consumer surplus plus profit.",
     "killed_by": "test_closed_form_matches[welfare_cents-monopoly] (seed 0)"},
    {"id": "r6d_m05", "description": "Student has a sign error in the monopoly fee: (a - b*c)/(2b) instead of (a + b*c)/(2b).",
     "killed_by": "test_closed_form_matches[fee_cents-monopoly] (seed 0)"},
]

statuses = [r["status"] for r in rows]
fragment = {
    "unit": "E1",
    "slice": "d",
    "round": 6,
    "verifier": "independent verifier (Haiku 5.5), round 6",
    "pin": PIN,
    "base": PREV,
    "checkout": str(ROOT),
    "scratch": "/tmp/e1d-*-r6 (candidate and probe copies, removed after each run)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "PASS" if all(s == "PASS" for s in statuses) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/E/E1/project.html, grader/ (reference, starter, instance, test_project), tests/labs/E1/lab-E1-project-{1,2,3}.py, cards.json (133 cards, lessons L01-L09 cited).",
        "Delta since pin 09b8751 read hunk by hunk for project.html, test_project.py, lab-E1-project-1/2.py and cards.json.",
        "Mutation run: tools/mutate_graders.py --unit E1 --seeds 0-9 over all 92 files in ledgers/E1/mutants: 91 killed, r6d_m01 survived.",
        "Unrelated failures seen but outside slice d: tests/test_labs.py fails for unit E3 (missing twins tests/labs/E3/*, 11 cases). No E1 test failed in test_page_checks.py, test_labs.py or test_run_labs.py.",
        "Not checked: live verify_refs run (network registry re-resolution for the whole unit; only plain-curl Open Library check); tools/fetch_data.py (no data in E1); figure sweeps (no figures in project page); lesson-level rows (other slices); the full CI gate; live browser screenshot of the grader panel.",
        "Judgement calls recorded in rows: float inputs (E1d-proj-alt-integer-pairs) depend on whether 120.0 is a 'whole number' under the page's Inputs; the FAIL stands because the page does not say so.",
    ],
    "summary": "E1 slice d verdict FAIL: 3 project/grader FAIL rows (float-rounding mutant survives; alternative integer-pair implementation over-constrained by float-output test; exemplar B C6 annotation does not match its descriptor) and 3 card FAIL rows (18 Misconception references not printed in lessons; E1-c019 drops the sign; E1-c023/c041/c075 omit hypotheses). All other rows pass.",
}

problems = []
out = ROOT / "ledgers/E1/E1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fails", statuses.count("FAIL"), "verdict", fragment["verdict"])
