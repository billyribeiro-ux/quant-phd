import json, sys
R = []
def row(id_, check, loc, status, ev, fix=None):
    r = {"id": id_, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)
P = "PASS"; F = "FAIL"; U = "UNVERIFIABLE"
# ---- project page and rubric
row("d-p-no-file-claim", "2.9-prose: claim about the page vs its code", "course/modules/FC/FC2/project.html:285 vs course/assets/js/grader.js:46,75-80", F,
    "project.html:285 says 'Nothing on this page uploads or reads a file.' grader.js:46 creates <input type=file> and grader.js:75-78 reads it with file.text() into the editor; project.html:359 says 'Paste or load your scanner.py'.",
    "Reword project.html:285 to 'Nothing on this page uploads a file; the autograder can load a .py file from your device into the editor, which stays in this browser.'")
row("d-p-rubric-C3-P1-P4", "2.9 rubric consistency with conventions", "course/modules/FC/FC2/project.html:509 (rubric C3 level 3) vs project.html conventions P5 and P6", F,
    "Rubric C3 level 3 says 'names, for each finding, the labels P1 to P4'. The conventions make the convexity finding depend on P1, P2 and P5 (P5 is present values), and every finding on P6 (cost). reference.py:_explain_convexity cites P5. A note that names P5 meets the conventions but not level 3 as written.",
    "Change level 3 to 'the labels P1 to P6 that it depends on, as the conventions define them'.")
row("d-p-exemplarA-C2-score", "2.3 grade of exemplar A against the rubric cells", "course/modules/FC/FC2/project.html:585 and :605", F,
    "Exemplar A official C2 = 2, but its own text says 'gives no cost model'. The C2 level-1 cell is 'No cost model, or the costs are ignored'; the rule that level 1 is the absence its cell names gives level 1.",
    "Set exemplar A C2 to 1 (official scoring line at :585 and the annotation at :605).")
row("d-p-exemplarB-C3-level4", "2.3 grade of exemplar B against the rubric cells", "course/modules/FC/FC2/project.html:577 (C3 level 4 annotation)", F,
    "C3 level 4 requires, for EACH assumption a finding depends on, what would change it if it failed. Exemplar B covers P3 (dividend) and P4 (factor) only; it gives no failure consequence for P1, P2 or P5, which the convexity finding depends on. Official C3 = 4 is over-scored; level 3 fits.",
    "Score exemplar B C3 as 3, or add the failure consequence of P1, P2 and P5 to the note.")
row("d-p-unequal-spacing-claim", "2.5 grader claim vs suite", "course/modules/FC/FC2/project.html:320; grader/test_project.py:~ test_convexity_matches_exhaustive_oracle_seed (INST, INST2) and test_unequal_grid_violation_is_found", F,
    "project.html:320 says the convexity test is checked 'against an exhaustive check of every interior strike, including a chain with unequal spacing'. The two seeded oracle tests run only on instance.py chains, which are evenly spaced (STRIKE_OFFSETS in instance.py, checked over 2000 seeds). The unequal-spacing case is one hand-built three-strike chain with one interior strike.",
    "Either add an oracle test on an unequal-grid chain, or reword to 'a three-strike chain with unequal spacing, checked at its one interior strike'.")
row("d-p-reading-convexity-bound", "2.9 term used against lesson", "course/modules/FC/FC2/project.html:657", F,
    "'The parity relation and the convexity bound are proved in Lesson 5'. Lesson 5 names the convexity result 'convexity in strike' (L05 Definition 3.1, Theorem 3.2); 'bound' is used there for the model-free bounds of Theorem 2.2.",
    "Replace 'the convexity bound' with 'convexity in strike (Theorem 3.2)'.")
row("d-p-spec-message-df", "2.6 spec wording vs reference", "course/modules/FC/FC2/grader/reference.py:26 vs course/modules/FC/FC2/project.html:~309 (Constraints)", F,
    "project.html says 'the message says that df_ppm must lie in 1 to 1000000'. reference.py:26 raises 'df_ppm must lie in 1..1000000'. The grader checks type only (match='df_ppm'), so the suite passes, but the reference does not say what the page says.",
    "Change reference.py:26 to 'df_ppm must lie in 1 to 1000000'.")
row("d-g-instance-spot-docstring", "2.9 docstring claim vs code", "course/modules/FC/FC2/grader/instance.py:6 vs :56", F,
    "Docstring: 'a spot between 80.00 and 200.01'. Code: spot = rng.randrange(8_000, 20_001), maximum 20000 cents = 200.00. Over make_instance seeds 0..1999 the observed spots are 8003..19997 cents.",
    "Change the docstring to 'between 80.00 and 200.00'.")
row("d-g-overconstrained-message", "2.5 over-constraint (architect ruling a and b)", "course/modules/FC/FC2/grader/test_project.py:468,470,476", F,
    "Witness: alt1 (ledgers/FC2/scripts/FC2-d-r1/alt1_scanner.py) raises 'need one call per strike: 3 strikes, 2 calls' for calls of length 2. It is correct and names both lengths, but test_calls_shorter_than_strikes_is_rejected fails with 'Regex pattern did not match. Expected regex: one quote per strike'. The page (project.html:313) asks only that the message name the lengths. alt2 (same code with the phrase) passes all 50 seeds.",
    "Drop match='one quote per strike' at lines 468, 470, 476 and rely on the type plus the lengths test (test_length_message_names_both_lengths).")
# ---- cards
row("d-c-ungraded", "2.3 BLUEPRINT s3 every substantive claim carries a grade", "course/modules/FC/FC2/cards.json: 36 cards with no grade field, e.g. FC2-c014, FC2-c007, FC2-c129, FC2-c037, FC2-c049, FC2-c062, FC2-c090, FC2-c102", F,
    "36 of 131 cards have no grade key. Several cite a theorem or proposition as a substantive claim: FC2-c129 ('Theorem 2.3' on existence of an implied volatility), FC2-c007 (Proposition 3.2 runs one way), FC2-c014 (Proposition 3.2 gives the all-holdings result), FC2-c062 (Example 2.5 and Remark 2.6), FC2-c037 and FC2-c049 (Remark 1.4).",
    "Give each card that asserts a claim a grade (T for proved claims with a cited statement; a definitional card may omit it only if the card asserts no claim).")
row("d-c-simulated-graded-T", "2.3 architect rule (e): SIMULATED-lab results are grade C", "course/modules/FC/FC2/cards.json: FC2-c038 (L03), FC2-c072, FC2-c073, FC2-c074, FC2-c079 (L05)", F,
    "Each card is graded T with a basis naming a SIMULATED lab: FC2-c038 'Lab 3, Part A (SIMULATED)' (84 cents, 4 loss days, both read off lab-FC2-L03-1 output); FC2-c072 'Lab 1 (SIMULATED price set)'; FC2-c073, FC2-c074, FC2-c079 'Lab 1 (planted error; SIMULATED price set)'. The printed values come from the lab (tests/labs/FC2/lab-FC2-L05-1.py output), not from a proof on the page.",
    "Grade these cards C with a basis naming the lab (for example 'Lab 1 (SIMULATED price set)').")
row("d-c-notation-R-star", "2.4 notation conformity (notation/notation.json)", "course/modules/FC/FC2/cards.json FC2-c042, c043, c044, c046, c050; course/modules/FC/FC2/L03.html (R^\\ast = par rate, 17 uses)", F,
    "notation/notation.json defines R^\\ast as 'the return on the SDF in the payoff space (defined in AP1 Lesson 4)'. L03 and the cards write the par rate as R^\\ast or R* (e.g. FC2-c042 'R* = (1 − DF_n)/Σ DF_i'). The same symbol is used with a different meaning.",
    "Rename the par rate, for example R_{par} as the build plan §2 specifies, in L03 and in the cards.")
row("d-c-h-number", "2.2 card number appears in its lesson", "course/modules/FC/FC2/cards.json FC2-c046 vs course/modules/FC/FC2/L03.html", F,
    "Card FC2-c046 uses 'h = 0.01'. The string 0.01 does not occur in the L03 text (lesson writes 'one point higher' and 'one percent'). Value itself is correct: -0.01 * sum DF * 100000000 = -4415468 cents, sum DF = 4.415468.",
    "State 'h = 0.01 (one percentage point)' in L03 so the card's number appears in the lesson.")
row("d-c-full-text", "2.7 every card's prose claim vs its lesson text", "course/modules/FC/FC2/cards.json (131 cards)", U,
    "Read all 131 cards. Checked: every number token in each card occurs in its own lesson text (script card_numeric_and_refs.py); all cited Definition/Proposition/Theorem/Lemma/Corollary/Remark/Example/Problem/Section labels resolve to its lesson; numeric cards recomputed (listed under the PASS rows). Claim-by-claim hypothesis checks were done for about 25 cards (c038, c055, c067, c069, c070, c071, c076, c078, c085, c096, c110, c111, c117, c027, c056, c057, c072-c075, c079, c046, c050, c059, c060, c061). The remaining cards were not each compared line by line against the lesson paragraph, so this row is not PASS.",
    "Complete a line-by-line card-to-lesson comparison for the cards not listed; this was not done in round 1.")
# ---- PASS rows: grader, labs, mutants, numbers, structure
row("d-g-collect-75", "2.5 test count on page equals real collect-only count", "course/modules/FC/FC2/grader/test_project.py; project.html:320", P,
    "In a copy with scanner.py=reference.py: QF_SEED=s .venv/bin/python -I -m pytest --collect-only -q test_project.py for s=0..49: 75 tests collected each time (50 of 50).")
row("d-g-reference-suite", "2.5 reference passes every seed", "course/modules/FC/FC2/grader/reference.py; test_project.py", P,
    "QF_SEED=s pytest -q -p no:cacheprovider --assert=plain -W error test_project.py for s=0..49: 75 passed each seed. tools/run_graders.py --unit FC2: PASS (reference 50/50 seeds).")
row("d-g-starter-fails", "2.5 starter fails the suite (project.html Required outputs)", "course/modules/FC/FC2/grader/starter.py", P,
    "starter.py copied as scanner.py, QF_SEED=0: 66 failed, 9 passed (the passing tests were not enumerated).")
row("d-g-alt-correct-impls", "2.5 over-constraint: three alternative correct implementations", "ledgers/FC2/scripts/FC2-d-r1/alt1_scanner.py, alt2_scanner.py, alt3_scanner.py", P,
    "alt2 (integer micro-cent arithmetic, cross-multiplied chord test, page phrase in the length message) passes 75/75 on seeds 0..49. alt3 (Decimal at 60 digits, floor(x+1/2) tie rule, own validators) passes 75/75 on seeds 0..49. alt1 fails only the message-phrase over-constraint (row d-g-overconstrained-message). Each implementation passes all other tests, including the tie and boundary tests.")
row("d-g-mutants", "2.6 every mutant killed; >=3 new student-error mutants", "ledgers/FC2/mutants/ (m01-m14)", P,
    "tools/mutate_graders.py --unit FC2 --seeds 0-9: PASS (14/14 killed). Builder's m01-m10 killed (seed 0 or 2). New mutants written by this verifier: m11_convexity_on_discounted_quotes.py (convexity test and gross both use quotes times df; killed by test_scan_matches_exhaustive_oracle_seed, seed 2); m12_midpoint_chord_ignores_spacing.py (killed by test_unequal_grid_no_false_positive, seed 0); m13_gross_rounds_half_even.py (Python round(), killed by test_half_cent_gross_rounds_once_up, seed 0); m14_convexity_skips_last_interior.py (killed by test_scan_matches_exhaustive_oracle_seed, seed 2). Equivalence note: a first m11 that discounted only the sign test was equivalent (positive scaling keeps the sign, and scan's gross used undiscounted calls), so it was not counted; the counted m11 scales the gross as well.")
row("d-g-instance-other-claims", "2.9 instance docstring other ranges", "course/modules/FC/FC2/grader/instance.py:1-12", P,
    "Over make_instance seeds 0..1999: df_ppm in 930084..998972 (docstring 0.930000 to 0.999000); fee 0..40; half-spread 1..150; strikes evenly spaced in every draw; planted kinds convexity 683, none 673, parity 644; every 'none' draw has every exact parity gap rounding to 0.")
row("d-p-labs-run", "2.5 labs run: run_labs, -I -W error, page_smoke", "tests/labs/FC2/lab-FC2-project-1.py, -2.py, -3.py; course/modules/FC/FC2/project.html", P,
    "tools/run_labs.py --unit FC2: PASS (11/11). Each project twin under python -I -W error exits 0. tools/page_smoke.py --unit FC2: project.html PASS (labs and in-browser grader: 'All 75 tests pass').")
row("d-p-lab-numbers", "2.2 numbers printed by project labs and the page", "project.html Lab 1 (lines ~60-120), Lab 2, Lab 3 (~line 370-480); tests/labs/FC2/lab-FC2-project-*.py", P,
    "Recomputed in python: Lab 1 parity gaps 0,120,0,0,-20,0 (cents) at strikes 9000..11500; chord less call 50, 100, -75, 75 at strikes 9500, 10000, 10500, 11000 (only 10500 is a violation, the other three are not); cost 45; kept 2. Lab 3 parity gaps 0,-60,0,0,226,540, chord-less-call 35, 470/3, -188/3, 59, cost 60; kept 3, gross 226/540/63, net 166/480/3. The page's printed values equal these, and the 1/3 and 2/3 weights in the exemplar match.")
row("d-p-exemplar-B-numbers", "2.2 exemplar numbers", "course/modules/FC/FC2/project.html exemplar B passage", P,
    "Discounted strikes 6175 (6500 x 0.95) and 6650 (7000 x 0.95); parity 226 and 540; chord at 6000 = 802/3; net 3; cost 60 = 3 x (8+12). All recomputed in Fraction.")
row("d-p-costs-and-classes", "2.4 mathematics: parity sign and convexity direction", "course/modules/FC/FC2/project.html Conventions (P1-P6) and grader/reference.py _explain_*", P,
    "Cash flows checked: a positive gap C-P-(S-K df) gives an inflow of the gap at t=0 for sell call, buy put, buy stock, borrow K df, and the expiry payoff cancels by put-call parity; a call above the chord is sold against the wings with the chord weights. Consistent with the page's trade descriptions.")
row("d-p-concepts-dag", "2.8 DAG: concepts used on project page inside closure", "course/modules/FC/FC2/project.html data-concept links; tools/check_dag.py", P,
    "check_dag FC2: PASS. data-concept links on project.html: arbitrage-opportunity (FC2 L01), put-call-parity and option-arbitrage-bounds (FC2 L05); all owned by FC2 and reachable.")
row("d-p-notation-project", "2.4 notation conformity for the project page", "course/modules/FC/FC2/project.html; notation/notation.json", P,
    "Project symbols C, P, S, K, df_ppm, D are not in notation.json. The page's P1-P6 are assumption labels defined on the page and declared separate from the lessons' labels (page text: 'the project's own labels'). No registry symbol conflict.")
row("d-p-citations", "2.1 citations", "course/modules/FC/FC2/project.html data-cite (cox1979option, hull2021options, stoll1969relationship); references/references.json", P,
    "tools/verify_refs.py --unit FC2 (live): 3 of 560 entries, 0 problems. tools/verify_refs.py --offline: 560 entries, 0 problems. Registry entries read: cox1979option (DOI 10.1016/0304-405x(79)90015-1, verified crossref), stoll1969relationship (DOI 10.1111/j.1540-6261.1969.tb01694.x, verified crossref), hull2021options (ISBN 9780136940166, verified openlibrary). Page says no locator is quoted from them, and it quotes none.")
row("d-p-hours", "2.9 hours arithmetic (not pace)", "course/modules/FC/FC2/project.html time-budget table; index.html data-hours-*; L01-L08 data-hours", P,
    "Project time budget rows 2+3+5+9+3+5+3 = 30; hub data-hours-project=30; lesson data-hours 6,8,9,7,8,8,8,6 = 60 = hub data-hours-lessons; 60+30=90. Pace not judged (architect ruling).")
row("d-p-structure", "2.9 structure and banned phrases in project page", "course/modules/FC/FC2/project.html", P,
    "tools/check_projects.py --unit FC2: PASS (spec sections in order; grading names autograder and rubric). Text search on the page text: 'roughly' 0, 'historically' 0, 'always' 0, 'drives' 0, ellipsis 0; 'about' 6 (three are exemplar A amounts 'about 226 cents' etc., one is 'questions about each finding').")
row("d-p-scope-words", "2.7 scope words (only, every, all, same) need a computation or hypothesis", "course/modules/FC/FC2/project.html ('every' 17, 'only' 15, 'all' 62, 'same' 12 occurrences)", U,
    "Counts from a text search. Sampled and backed: 'every strike' (parity tests over range(6)), 'only if net > 0' (test_finding_with_net_exactly_zero_is_not_returned), 'the same chain' (Lab 3 chain). The remaining occurrences were not each audited, so this row is not PASS.",
    "Audit each scope word on project.html against a test or a printed computation, or rephrase it.")
row("d-c-numeric-recompute", "2.2 card numbers recomputed", "course/modules/FC/FC2/cards.json; ledgers/FC2/scripts/FC2-d-r1/card_numeric_and_refs.py", P,
    "Recomputed: BS call 10.450584 (c109), d1 0.35 d2 0.15 (c114), put 5.573526 -> 557 cents (c118), L 4.877058 (c126), 131: 120e^-0.05=114.15 so L=0 (c131), 4-step u,d,R,q=1.105171,0.904837,1.012578,0.537808 (c115), 1-step V1 12.1623 -> 1216 cents (c116), 400-step error -0.0049977 currency units = -0.4998 cents (c110,c117), sign pattern at 1,2,5,10,25,50,100,200,400 (c111), 100e^-0.1-50=40.48 (c076), 50e^0.025=51.2658 (c021), FC2-c027 237.11 uses the unrounded fair price (237.1077), c045 4902625 cents, c046 -4415468 with sum DF 4.415468, c056 6.70 and 18.10, c057 14.82, c098 56.25 and 36 and 45. All match.")
row("d-c-cross-refs", "2.7 card cross-references resolve in own lesson", "course/modules/FC/FC2/cards.json; L01-L08 text", P,
    "Every Definition/Proposition/Theorem/Lemma/Corollary/Remark/Example/Problem/Section citation in every card occurs as a label in its own lesson (Problem labels M1..R3 in each lesson's problem set; Section 5 is L05 'Where the canon breaks').")
row("d-c-hypotheses-sample", "2.7 card hypotheses vs theorem statements (sample)", "cards FC2-c055, c067, c069, c070, c071, c078, c085; L04 lines 158, L05 lines 192, 274-278, 49", P,
    "c055 (A2, A3, A5) matches L04 line 158; c067 matches L05 Remark 2.3 (line 49); c069 (A2, A3, A5, (N)) and c070 match L05 lines 274-277; c071 (A1-A5, (N), r>=0) matches L05 line 278; c085 matches L06 Theorem 1.4(c) text; c078's 'initial value S - C < 0' is the lesson's cost convention for a call priced above the stock (L05 line 213, 296), consistent with the card.")
row("d-c-grades-T-proofs", "2.3 grades of proof-backed cards", "cards FC2-c004-c006, c019, c084, c089, c093, c100-c104", P,
    "Sampled: c004, c005 (A3 only), c006 (positive state prices, no A3), c019 and c084 match the lesson Propositions/Theorems the cards cite. Grades T assigned to proof-backed statements. (Sample only; see d-c-full-text.)")
row("d-g-ruff", "gate: ruff on grader and labs", "course/modules/FC/FC2/grader; tests/labs/FC2", P,
    "ruff check: All checks passed. ruff format --check: 15 files already formatted.")
row("d-gate-dag-labs-refs", "gate: check_dag, check_pages, verify_refs for FC2", "tools", P,
    "check_dag FC2: PASS. check_pages FC2: PASS. run_graders FC2: PASS (50/50). verify_refs live FC2: 0 problems.")
mut = [
 {"id": "m01_parity_strike_not_discounted", "description": "Parity uses the strike K instead of the discounted strike K df (both entry points).", "killed_by": "test_parity_gap_matches_exact_rounding_seed[0] (seed 0)"},
 {"id": "m02_parity_sign_flipped", "description": "Parity gap sign flipped: parity_gap_cents returns the negated gap.", "killed_by": "test_parity_gap_matches_exact_rounding_second_chain[2] (seed 0)"},
 {"id": "m03_cost_charged_once", "description": "Cost charged once per finding (one leg) instead of per leg (three legs).", "killed_by": "test_scan_matches_exhaustive_oracle_second_chain (seed 0)"},
 {"id": "m04_costs_ignored", "description": "Costs ignored: gross violations are reported as findings with no cost netting.", "killed_by": "test_scan_matches_exhaustive_oracle_second_chain (seed 0)"},
 {"id": "m05_no_ordering_check_input_order", "description": "Ordering not checked: convexity is computed in the input order of strikes, so shuffled strikes are accepted.", "killed_by": "test_strikes_equal_neighbours_are_rejected_by_scan (seed 0)"},
 {"id": "m06_convexity_first_difference", "description": "Convexity tested with the first difference: a violation is a call that falls between neighbours, not a second difference.", "killed_by": "test_convexity_matches_exhaustive_oracle_seed (seed 0)"},
 {"id": "m07_rounding_truncates_toward_zero", "description": "Rounding by truncation toward zero instead of half up, so an exact half cent goes down in magnitude.", "killed_by": "test_parity_gap_matches_exact_rounding_second_chain[2] (seed 0)"},
 {"id": "m08_df_read_as_parts_per_thousand", "description": "df_ppm read as parts per thousand: the discount factor is df_ppm / 1000.", "killed_by": "test_parity_gap_matches_exact_rounding_seed[2] (seed 0)"},
 {"id": "m09_net_rule_at_least_zero", "description": "Net-of-cost rule uses >= 0: a finding whose net amount is exactly zero is kept.", "killed_by": "test_finding_with_net_exactly_zero_is_not_returned (seed 0)"},
 {"id": "m10_seed0_answer_hard_coded", "description": "Hard-coded answer: scan returns seed 0's findings for any chain.", "killed_by": "test_strikes_equal_neighbours_are_rejected_by_scan (seed 0)"},
 {"id": "m11_convexity_on_discounted_quotes", "description": "Convexity test run on call quotes discounted by df_ppm (P5 says quotes are present values, so no discounting): the gross of a convexity finding is scaled by df.", "killed_by": "test_scan_matches_exhaustive_oracle_seed (seed 2)"},
 {"id": "m12_midpoint_chord_ignores_spacing", "description": "Convexity chord uses equal weights of one half on the two neighbours, which is wrong on an uneven strike grid.", "killed_by": "test_unequal_grid_no_false_positive (seed 0)"},
 {"id": "m13_gross_rounds_half_even", "description": "Gross amount rounded with Python round(), which sends an exact half cent to the even cent, not up.", "killed_by": "test_half_cent_gross_rounds_once_up (seed 0)"},
 {"id": "m14_convexity_skips_last_interior", "description": "Convexity scan stops one strike early, so a violation at the last interior strike is never reported.", "killed_by": "test_scan_matches_exhaustive_oracle_seed (seed 2)"},
]
counts = {"PASS": sum(r["status"] == P for r in R), "FAIL": sum(r["status"] == F for r in R), "UNVERIFIABLE": sum(r["status"] == U for r in R)}
frag = {
 "unit": "FC2",
 "slice": "FC2-d (project.html rubric and exemplars, grader/ (instance, reference, starter, test_project), project labs lab-FC2-project-1..3, cards.json, project mutants)",
 "round": 1,
 "verifier": "Claude Haiku 5.5 (independent verifier, FC2 slice d, round 1; not the builder)",
 "pin": "55b5634 (detached checkout /tmp/verifyC1-FC2-d)",
 "base": "none",
 "previous_ledger": "none",
 "checkout": "/tmp/verifyC1-FC2-d",
 "scratch": "/tmp/fc2-v/d",
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": "FAIL",
 "rows": R,
 "mutants": mut,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": "Round 1, first independent verification of FC2 slice d. Scripts: ledgers/FC2/scripts/FC2-d-r1/ (alt1/alt2/alt3 scanners, card_numeric_and_refs.py). Mutants m11-m14 are this verifier's; m01-m10 are the builder's and were run unchanged. Not checked: the full claim-by-claim comparison of all 131 cards against lesson paragraphs (row d-c-full-text); the lesson pages L01-L08 are other slices and were read only for card and lab evidence; the browser run of the exemplars' self-assessment form was not exercised; no git operations were performed.",
 "summary": {"rows": len(R), **counts, "mutants": len(mut), "mutants_killed": len(mut)},
}
json.dump(frag, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(counts, len(R))
