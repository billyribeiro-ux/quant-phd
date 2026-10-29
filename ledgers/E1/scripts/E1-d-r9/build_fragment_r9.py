import json, datetime, pathlib
R8 = "Carried from round 8 (course/modules/E/E1/%s byte-identical since the previous pin ce7b382): "
rows = []
def row(id_, check, loc, status, ev, fix=None):
    r = {"id": id_, "check": check, "location": loc, "status": status, "evidence": ev}
    if fix: r["fix"] = fix
    rows.append(r)

# --- labs and math (carried where the subject is byte-identical)
row("E1d-proj-lab1-numbers", "2.5-lab", "course/modules/E/E1/project.html lab-E1-project-1 (lines 55-128)", "PASS",
    "Re-verified this round: the hypothesis (line 57) changed to add a pointer to the rounding rule; code, expected block and interpretation unchanged. run_labs.txt (ledgers/E1/scripts/E1-d-r9/run_labs.txt): 'run_labs E1: PASS (12/12)'. Expected values re-derived by hand: monopoly 50/70/2500/1250/3750/1250; Cournot 200/3->67, 160/3->53, 20000/9->2222, 40000/9->4444, 5000/9->556; Bertrand 100/20/0/5000/5000/0.")
row("E1d-proj-lab2-numbers", "2.5-lab", "course/modules/E/E1/project.html lab-E1-project-2 (lines 130-187)", "PASS",
    "run_labs E1 PASS (12/12). Blanks unchanged: (d - rival)/2 and (a*volume - volume*volume/2)/b - c*volume. Error after 60 steps d/(3*2^60) is about 2.9e-17 < 1e-12, matching the expected 'True' line.")
row("E1d-proj-lab3-tie-numbers", "2.5-lab", "course/modules/E/E1/project.html lab-E1-project-3 (lines 189-257)", "PASS",
    (R8 % "project.html lines 189-257") + " Re-derived this round by hand: a=121 monopoly fee 141/2->71, volume 101/2->51, profit 10201/4->2550, CS 1275.125->1275, welfare 3825.375->3825, DWL 1275.125->1275; Cournot 202/3->67, 161/3->54, profit 20402/9->2267, welfare ->4534, DWL 10201/18->567; Bertrand 101, 20, CS 5100.5->5101.")
row("E1d-proj-lab-twins", "2.5-lab", "tests/labs/E1/lab-E1-project-{1,2,3}.py; project.html data-run blocks", "PASS",
    "run_labs E1 PASS (12/12): page code equals twin, twin under python -I -W error matches expected. tests/labs/E1 unchanged since ce7b382.")
for n, desc in [(1, "monopoly/Cournot/Bertrand closed forms (50, 70, 2500, 1250, 3750, 1250 ...)"), (2, "Cournot reaction and iteration"), (3, "closed_form_outcome and the tie case")]:
    pass
PROPS = {
 1: "Re-derived this round: pi(Q) = -Q^2/b + (d/b)Q, Q*=d/2, f(Q*) = (a+bc)/(2b), pi* = d^2/(4b).",
 2: "Re-derived this round: best response max(0,(d-q_j)/2); equilibrium excludes q_1=0; q=d/3; fee (a+2bc)/(3b); profit per exchange d^2/(9b); e_{k+1}=-e_k/2 gives |e_k|=d/(3*2^k).",
 3: "Re-read this round: the case analysis (f1<c; f1>c with f2>f1; f1=f2>c; f1=c<f2) closes with a profitable deviation in each case; (c,c) equilibrium; holds for any tie rule with shares in [0,1].",
 4: "Re-derived this round: CS = Q^2/(2b); W(d)-W(Q) = (d-Q)^2/(2b); welfare = CS + profit.",
 5: "Re-derived this round: differences d/6, d/3, d/(6b), d/(3b), d^2/(8b)-d^2/(18b)=5d^2/(72b), d^2/(36b); each bound > 1 for d > 6b (d/6 > b, d/3 > 2b, d^2/(18b) > 2b, 5d^2/(72b) > 5b/2, d^2/(36b) > b).",
}
for k in range(1, 6):
    row(f"E1d-proj-prop{k}", "2.4-math", f"course/modules/E/E1/project.html prop-{k} (id=prop-{k})", "PASS",
        (R8 % f"project.html lines of prop-{k} (unchanged; the delta hunks are at lines 53, 57, 390, 392, 393, 540)") + PROPS[k])
row("E1d-proj-spec-constraints", "2.6-spec", "course/modules/E/E1/project.html dl.spec (lines 312-323)", "PASS",
    (R8 % "project.html lines 312-323 and grader/reference.py, grader/test_project.py") + "Interface, key set, int type, ValueError conditions and messages agree with grader/reference.py lines 26-35 and the must_raise phrases; 124 = collect-only count (E1d-proj-r7-collect-count).")
row("E1d-proj-hours", "2.6-hours", "course/modules/E/E1/project.html #hours (lines 333-349); course/modules/E/E1/index.html line 42", "PASS",
    (R8 % "project.html lines 333-349 and index.html line 42") + "Table sums to 30 (2+3+8+8+6+3); index.html data-hours-project=30 and data-hours-lessons=90 (120 total).")

# --- rubric (changed subjects re-verified this round)
row("E1d-proj-rubric-structure", "2.6-rubric", "course/modules/E/E1/project.html table#rubric, C6 level 2 (line 393)", "PASS",
    "Re-verified: level 2 now reads 'Names one or more of the limits, and states what changes for fewer than three of them.' A memo naming all three limits and stating the change for exactly two falls at level 2 (fewer than three), not level 3 (for each) and not level 1 (a limit is named). The round-8 gap is closed. (Other rubric gaps are separate rows.)")
row("E1d-proj-rubric-C3-C5-level2", "2.6-rubric", "course/modules/E/E1/project.html table#rubric C3 level 2 (line 390), C5 level 2 (line 392)", "PASS",
    "Re-verified: C3 level 2 now reads '...or reports all three without the rounding rule or without a tie example'; C5 level 2 now reads '...justifies it without naming a condition, or names a condition without a direction'. A memo with all three DWL, a rounding rule and no tie example falls at level 2; a justified recommendation with no condition falls at level 2. Round-8 gap closed.")
row("E1d-proj-rubric-C3-welfare-without-dwl", "2.6-rubric", "course/modules/E/E1/project.html table#rubric C3 level 1 (line 390) and level 2 (line 390)", "FAIL",
    "C3 level 1 is 'No welfare figure is reported.' C3 level 2 is 'Reports the deadweight loss of one or two structures, or ...'. A memo that reports the welfare of all three structures but no deadweight loss meets neither: it reports a welfare figure (so not level 1) and reports the deadweight loss of zero structures (so not level 2). The memo brief (line 373) requires the DWL, but the criterion must place every memo.",
    "Change level 1 to 'Reports no deadweight loss.' (so a memo with welfare but no DWL is level 1), keeping level 2 as written.")
row("E1d-proj-rubric-C4-all-three-unsigned", "2.6-rubric", "course/modules/E/E1/project.html table#rubric C4 level 2 (line 391)", "FAIL",
    "C4 level 2 is 'Orders one or two of the outcomes without the signs, or gives a difference without its number.' A memo that orders all three volumes (or fees, or welfare levels) without signs and gives no difference numbers, e.g. 'volume rises from monopoly to Cournot to Bertrand', meets neither level 2 (it orders three, not one or two; it gives no difference) nor level 1 (a comparison is made). Exemplar A (line 411-412) is scored 2 for ordering the outcomes without signs, so the text does not match the scoring it is calibrated to.",
    "Change level 2 to 'Orders the outcomes without the signs, or gives a difference without its number.'")
row("E1d-proj-rubric-C1-two-structures-timing", "2.6-rubric", "course/modules/E/E1/project.html table#rubric C1 level 2 (line 388)", "FAIL",
    "C1 level 2 covers 'omits the timing of one structure'. A memo that gives units for a, b and c and names the three structures but states the timing of only one of them (omitting it for two) matches no level literally: not level 3 (timing for each), not level 2 (one structure), not level 1 (symbols are defined).",
    "Change level 2 to 'omits the timing of a structure' (or 'of one or more structures').")
row("E1d-proj-exemplar-blind-scoring", "2.6-rubric", "course/modules/E/E1/project.html #exemplar-a (401-464), #exemplar-b (466-549)", "FAIL",
    "Blind scoring by the rubric alone: A = C1 1, C2 2, C3 2, C4 2, C5 1, C6 2 (matches data-scores line 401). B = C1 4, C2 2, C3 4, C4 4, C5 3, C6 2. Exemplar B's C2 is scored 4 at line 466, but level 3 of C2 requires that the memo 'reproduces each volume and fee from the conditions'. Exemplar B derives only the monopoly and Cournot volumes and fees (line 494); the Bertrand volume d and fee c (summary line 472, welfare line 505) are stated and never derived, and no Bertrand passage exists. The verdict (line 468) says 'each closed form is derived with its hypotheses', which is false for Bertrand. Level 3 is missed, so C2 is 2 by the descriptor 'misses an element of level 3'.",
    "Either add a Bertrand derivation to exemplar B's Derivations passage (the (c,c) equilibrium and the undercut step of Proposition 3), or set data-scores C2 to 2 at line 466 and correct the verdict text at line 468.")
row("E1d-proj-exemplar-annotation-C6", "2.6-rubric", "course/modules/E/E1/project.html #exemplar-b Limits annotation (line 543)", "PASS",
    "Re-verified: the quoted descriptor 'names one or more of the limits, and states what changes for fewer than three of them' matches line 393 word for word. The other annotations at 544-545 (level 3 and 4 misses) are consistent with the descriptors.")

# --- autograder and mutants
row("E1d-proj-autograder-reference", "2.6-autograder", "course/modules/E/E1/grader/reference.py; tools/run_graders.py", "PASS",
    "ledgers/E1/scripts/E1-d-r9/run_graders.txt: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.2 s)'. Direct run (scratch /tmp/e1d-r9-ws, reference as market_structure.py): QF_SEED=0 '124 passed'.")
row("E1d-proj-autograder-instances", "2.6-autograder", "course/modules/E/E1/grader/instance.py", "PASS",
    (R8 % "grader/instance.py") + "run_graders E1 PASS over seeds 0-49 (instances differ across seeds).")
row("E1d-proj-mutant-float-rounding", "2.6-mutation", "course/modules/E/E1/grader/test_project.py test_large_exact_inputs_round_from_exact_values; ledgers/E1/mutants/r6d_m01_*.py", "PASS",
    "ledgers/E1/scripts/E1-d-r9/mutate_E1_seeds0-9_r9_all.txt: all 119 mutants KILLED, including r6d_m01 (seed 0).")
row("E1d-proj-mutant-existing", "2.6-mutation", "ledgers/E1/mutants/*.py (115 prior mutants)", "PASS",
    "ledgers/E1/scripts/E1-d-r9/mutate_E1_seeds0-9_r9_all.txt: 'mutate_graders E1: PASS (119/119 killed)' (seeds 0-9); 0 SURVIVED lines. Re-run of all existing mutants this round.")
row("E1d-proj-mutant-r9-new", "2.6-mutation", "ledgers/E1/mutants/v9d_m01..m04 (four new student-error mutants)", "PASS",
    "Four new mutants, all KILLED (seeds 0-9): v9d_m01_profit_is_fee_times_volume.py -> test_reference_case_matches_closed_forms[profit_cents-cournot]; v9d_m02_cournot_profit_is_one_exchange.py -> test_closed_form_matches[profit_cents-cournot]; v9d_m03_deadweight_linear_not_squared.py -> test_closed_form_matches[deadweight_loss_cents-monopoly]; v9d_m04_bertrand_splits_demand.py -> test_closed_form_matches[volume_trades-bertrand].")
row("E1d-proj-alt-integer-pairs", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt1_integer_pairs.py", "PASS",
    (R8 % "grader tests (r6 alternative carried)") + "Carried from ledgers/E1/scripts/E1-d-r8/alternatives_seeds0-49_r8.txt (50/50).")
row("E1d-proj-r9-alternatives", "2.6-autograder", "/tmp/e1d-r9-alt/alt1_integer_half_up.py, alt2_decimal_half_up.py, alt3_bertrand_first_checks.py", "PASS",
    "ledgers/E1/scripts/E1-d-r9/alternatives_r9.txt: alt1 (integer half-up from numerator and denominator) 50/50; alt2 (60-digit Decimal, ROUND_HALF_UP) 50/50; alt3 (input checks in the order c, b, a) 50/50. No over-constraint found.")
row("E1d-proj-r7-alternatives", "2.6-autograder", "ledgers/E1/scripts/alt1..alt5; E1-d-r7/alts/*.py; E1-d-r8/alts/*.py", "PASS",
    (R8 % "grader (alternatives from earlier rounds)") + "Round-8 13-candidate scan (50/50 for the 11 correct ones; float-based fail as the exact-fraction rule requires).")
row("E1d-proj-pyodide-local", "2.6-browser", "tools/page_smoke.py --unit E1 --pages project", "PASS",
    "ledgers/E1/scripts/E1-d-r9/page_smoke_project.txt: 'page_smoke E1: PASS'; ledgers/E1/scripts/E1-d-r9/page_smoke.txt (all E1 pages) PASS. Live browser screenshot not taken.")
row("E1d-proj-ruff-mypy", "2.6-gates", "tests/labs/E1; course/modules/E/E1/grader", "PASS",
    "ledgers/E1/scripts/E1-d-r9/ruff.txt: ruff check and ruff format --check exit 0 on tests/labs/E1 and the grader; mypy.txt: 'Success: no issues found in 12 source files' (mypy on tests/labs/E1). Repo-wide mypy not re-run this round.")
row("E1d-proj-check-gates", "2.6-gates", "tools/check_pages.py, check_dag.py, check_projects.py, run_labs.py, verify_refs.py", "PASS",
    "ledgers/E1/scripts/E1-d-r9/: check_pages.txt, check_dag.txt, check_projects.txt all 'E1: PASS' (exit 0); run_labs.txt 'run_labs E1: PASS (12/12)'; verify_refs_offline.txt '560 entries, 0 problems'. build_site.py not re-run (see notes).")
row("E1d-proj-reference-varian", "2.6-reference", "references/references.json key varian2014intermediate; project.html #reading", "PASS",
    (R8 % "project.html Reading section and references") + "verify_refs offline 560 entries, 0 problems (r9).")
row("E1d-proj-notation", "2.6-notation", "notation/notation.json; project.html math spans", "PASS",
    "Re-verified: notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (blackboard). Search of project.html and cards.json for each registered symbol and macro finds no use (the only 'T' hits are grade labels). The project's symbols a, b, c, d, Q, q, f, W, G, pi, e_k, F are not registered, so no reuse conflict.")
row("E1d-proj-banned", "2.6-prose", "course/modules/E/E1/project.html; cards.json", "PASS",
    "check_pages E1 PASS (banned-string and page contract). New text added this round (lines 53, 57, 390-393, 540) contains no process words.")
row("E1d-proj-delta-r9", "2.4-delta", "course/modules/E/E1/project.html (hunks at lines 53, 57, 390, 392, 393, 540); L07.html; L09.html; cards.json", "PASS",
    "Delta ce7b382..b6865c7 in the slice read hunk by hunk: project.html 53 (pointer to the three structures and Propositions 1-4), 57 (rounding pointer in Lab 1 hypothesis), 390 (C3 level 2), 392 (C5 level 2), 393 (C6 level 2), 540 (exemplar B C6 annotation). Grader and lab twins: no diff. Cards: E1-c102 locator, E1-c136 added. Other-slice hunks (L07, L09) read because cards cite them.")
row("E1d-proj-delta-r5", "2.4-delta", "course/modules/E/E1/project.html (hunks at lines 53, 390, 540); course/modules/E/E1/cards.json", "PASS",
    "Superseded by E1d-proj-delta-r9 for the current delta; the round-8 hunks were read and re-checked.")
row("E1d-proj-reading-section", "2.6-prose", "course/modules/E/E1/project.html section 'Reading' (lines 567-573)", "PASS",
    (R8 % "project.html lines 567-573") + "Reading section unchanged.")
row("E1d-proj-model-propositions-link", "2.6-prose", "course/modules/E/E1/project.html line 53; #model-propositions (line 281)", "PASS",
    "Re-verified: line 53 links #model-definitions and #model-propositions; both ids exist (anchor check: no missing local anchors). Propositions 1-4 are the closed forms used by Labs 1-3.")
row("E1d-proj-l07-consistency", "2.6-cards-lesson", "course/modules/E/E1/L07.html Definitions 1.1 and 1.3, Lemma 1.4; cards E1-c092, E1-c094, E1-c102", "PASS",
    "Re-verified against L07.html lines 56-92: Definition 1.1 defines CS, PS and total surplus W = CS + PS; Definition 1.3 defines DWL = W(d) - W(Q); Lemma 1.4 gives the competitive volume. E1-c092 and E1-c094 agree with these. E1-c102 locator now Section 4 (see E1d-cards-c102-section-locator).")
row("E1d-proj-r7-mutants-new", "2.6-mutation", "ledgers/E1/mutants/r7v_m01..m05", "PASS",
    "ledgers/E1/scripts/E1-d-r9/mutate_E1_seeds0-9_r9_all.txt: all KILLED (119/119).")
row("E1d-proj-r7-collect-count", "2.6-count", "course/modules/E/E1/grader/test_project.py; course/modules/E/E1/project.html Grading mode (line 322)", "PASS",
    "Collect-only with QF_SEED=0 and the reference as market_structure.py: '124 tests collected'. Page line 322 says 124. Equal. Full run: '124 passed' with --assert=plain -W error.")
row("E1d-proj-r7-gates-lint", "2.6-gates", "repo (E1 slice)", "PASS",
    "ruff, ruff format, mypy (tests/labs/E1), run_labs E1, run_graders E1 (50 seeds), check_pages/dag/projects, verify_refs offline, page_smoke E1 all re-run this round: PASS.")

# --- cards
for n in ["010", "020", "030", "040", "050", "060", "070", "080", "090", "100", "110", "120", "130"]:
    row(f"E1d-cards-sample-{n}", "2.3-cards", f"course/modules/E/E1/cards.json E1-c{n}", "PASS",
        (R8 % f"cards.json object E1-c{n} (JSON-equal to the previous pin)") + "Card text unchanged; numbers re-derived in round 8 and consistent with this round's scripted cross-reference.")
row("E1d-cards-full-scan-duplicates", "2.3-cards", "course/modules/E/E1/cards.json (133 cards)", "PASS",
    "Scripted this round: 133 cards, no duplicate ids, fronts or backs (ledgers/E1/scripts/E1-d-r9/cards_refs_r9.txt plus an inline check). E1-c136 is a new card about the completed-square identity; it asks a different question from E1-c056 (the price, quantity and profit), so it is not a duplicate. c065/c088 overlap in content but ask different questions (round 8).")
row("E1d-cards-lab-graded", "2.3-cards", "course/modules/E/E1/cards.json grade C cards", "PASS",
    "Recounted: 14 grade-C cards (c014, c025, c027, c036, c051, c066, c084, c085, c105, c115, c129, c131, c132, c133), each with a basis; 94 grade T; 25 with no grade field (definitional 'What is ...?' cards). Each grade-C card's cited numbers were checked against the expected blocks of L01-L09 (see E1d-cards-lab-outputs-r9).")
row("E1d-cards-lab-outputs-r9", "2.3-cards", "course/modules/E/E1/cards.json grade-C cards vs L01..L09 expected blocks", "PASS",
    "Compared with /tmp/e1d-r9-exp2.py output (ledgers/E1/scripts/E1-d-r9/): c014 (four cases, grid point 30, MRS = price ratio); c025 (cases 1 and 4: 4 and 4, profit 4 and -84); c027 (j/12, j=0..72, four cases; L02 Part code); c036 (141 grid prices, 110/0/30 signs, F=0 and F=100 both 48/7); c051 (10 cents, 100 units, -0.2 and 2); c066 (70, 20, 27.5 cents; equal True); c084 (6/5/6 outputs, step 25 for the reference case, grid step 1/12 at L06 line 231); c085 (best grid profit 0; four rival fees each); c105 (1, 2, 10, 97 steps; Part A); c115 (45, 15, 13 interior, 10 off diagonal, (0,0), (8,4)); c129 (7 units, 2650 vs 2700); c131 (80, 68, [120], 720 cents); c132 (6 units, 2700); c133 (9.391047e-7, 3.880758e-11 at step 0.01). All match.")
row("E1d-cards-numbers-in-lesson", "2.3-cards", "course/modules/E/E1/cards.json; L01-L09.html", "PASS",
    "ledgers/E1/scripts/E1-d-r9/cards_refs_r9.txt: 1 problem, E1-c102 'Section 4 not in lesson' (a false positive: the heading is '4 Misconceptions', L07.html line 323, with section-number span 4). All other labelled references resolve in their own lesson.")
row("E1d-cards-labels-resolve", "2.3-cards", "course/modules/E/E1/cards.json (all labels)", "PASS",
    "All labelled references resolve in their own lesson. The only script hit (E1-c102 'Section 4') is a false positive of the literal-text check: L07.html line 323 is '<h2 id=\"s4\"><span class=\"section-number\">4</span>Misconceptions</h2>', so Section 4 is that heading. Round-8 'Section 3' error is fixed.")
row("E1d-cards-c102-section-locator", "2.3-cards", "course/modules/E/E1/cards.json E1-c102 back", "PASS",
    "Back now reads '(the misconception that the monopoly profit is the deadweight loss; Section 4).' L07.html line 323 is the Section 4 heading 'Misconceptions'; the first item at lines 325-327 is 'The deadweight loss is the profit that the monopoly keeps', which is the item described. Locator correct.")
row("E1d-cards-profit-sign-c019", "2.3-cards", "course/modules/E/E1/cards.json E1-c019", "PASS",
    (R8 % "cards.json object E1-c019") + "Re-derived: pi(F') = pi(F) - (F' - F) at every output, so the sign is right.")
row("E1d-cards-hypotheses", "2.3-cards", "course/modules/E/E1/cards.json E1-c023, E1-c041, E1-c075", "PASS",
    (R8 % "cards.json objects E1-c023, E1-c041, E1-c075") + "Hypotheses re-checked: E1-c041 uses a > 0, b > 0 (L04 Proposition 1.4); E1-c075 uses b > 0, c > 0, a > bc (L06 Lemma 2.4).")
row("E1d-cards-delta-r9", "2.3-cards", "course/modules/E/E1/cards.json (delta ce7b382..b6865c7)", "PASS",
    "Delta read: E1-c102 back ('Section 3' -> 'Section 4'); E1-c136 added (L05, grade T). No other object changed (JSON compare with the previous pin).")
row("E1d-cards-c136-new", "2.3-cards", "course/modules/E/E1/cards.json E1-c136; course/modules/E/E1/L05.html Assumption M, Proposition 5.2 (lines 62-85)", "PASS",
    "Re-derived: (a-bc)^2/(4b) - b(p-p_m)^2 with p_m=(a+bc)/(2b) equals (p-c)(a-bp) for every p (L05 proof lines 77-83; my expansion: -bp^2 + (a+bc)p - ac). p_m is the unique maximiser, maximum (a-bc)^2/(4b). Card matches Proposition 5.2 and its proof. Lesson 5 is the card's lesson tag, and the card's labels (Proposition 5.2) resolve there.")
row("E1d-cards-r7-new-c134-c135", "2.3-cards", "course/modules/E/E1/cards.json E1-c134, E1-c135", "PASS",
    (R8 % "cards.json (ids removed)") + "Both ids absent; no references remain.")
row("E1d-cards-lessons-tier", "2.3-cards", "course/modules/E/E1/cards.json; L01-L09.html", "PASS",
    "Every card lesson tag is one of L01..L09 (lessons per count: L01 14, L02 13, L03 10, L04 17, L05 14, L06 24, L07 14, L08 13, L09 14); E1-c136 is tagged L05 and resolves there.")
row("E1d-cards-c105-basis", "2.3-cards", "course/modules/E/E1/cards.json E1-c105 (basis)", "PASS",
    (R8 % "cards.json object E1-c105") + "Basis 'Lab 1, Parts A and B' is a superset of the back's 'Lab 1, Part A'.")
row("E1d-cards-numbers-recheck-r9", "2.3-cards", "course/modules/E/E1/cards.json (all 133 cards read this round)", "PASS",
    "Every card was read this round (chunks 1-470 and 470-922). Numbers re-derived by hand: c006-c007, c009, c013, c017-c020, c024-c026, c030, c032, c035-c036, c040-c042, c046-c047, c049-c051, c053, c057, c059-c064, c069-c070, c072, c075-c079, c081, c086-c088, c090-c101, c103-c104, c120-c124, c128, c130-c131, c136. All match the lesson text or its lab output. Not every card's hypothesis list was cross-checked against its lesson proof text, which is the remaining gap.")
row("E1d-cards-read-complete", "2.3-cards", "course/modules/E/E1/cards.json (133 cards)", "UNVERIFIABLE",
    "Every card was read this round and its numbers and label references were checked, but a line-by-line comparison of each card's hypotheses and claim wording against its full lesson proof was not done for all 133 cards. Counted as UNVERIFIABLE.",
    "Cross-check every card's hypotheses against the lesson proof text in a round whose scope is the whole cards file.")

frag = {
 "unit": "E1", "slice": "d", "round": 9,
 "verifier": "independent verifier (Haiku 5.5), round 9",
 "pin": "b6865c7d10020e31b9858a49edf751f4b814c031",
 "base": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB9-E1-d",
 "scratch": "/tmp/e1d-r9-alt (alternatives), /tmp/e1d-r9-ws (grader workspace), /tmp/e1d-r9-exp*.py (expected-block extraction); removed after use",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [
  {"id": "v9d_m01_profit_is_fee_times_volume.py", "description": "Exchange profit taken as fee times volume with the cost never subtracted", "killed_by": "test_reference_case_matches_closed_forms[profit_cents-cournot] (seed 0)"},
  {"id": "v9d_m02_cournot_profit_is_one_exchange.py", "description": "Cournot profit reported for one exchange only, not the two-exchange total", "killed_by": "test_closed_form_matches[profit_cents-cournot] (seed 0)"},
  {"id": "v9d_m03_deadweight_linear_not_squared.py", "description": "Deadweight loss taken as the linear gap (d - volume)/(2b)", "killed_by": "test_closed_form_matches[deadweight_loss_cents-monopoly] (seed 0)"},
  {"id": "v9d_m04_bertrand_splits_demand.py", "description": "Bertrand volume taken as d/2, as if the two exchanges split the demand", "killed_by": "test_closed_form_matches[volume_trades-bertrand] (seed 0)"},
  {"name": "existing 115 mutants (ledgers/E1/mutants, prior rounds)", "description": "Re-run with tools/mutate_graders.py --unit E1 --seeds 0-9", "killed_by": "119/119 killed including the four new ones (ledgers/E1/scripts/E1-d-r9/mutate_E1_seeds0-9_r9_all.txt)"}
 ],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": "Delta ce7b382..b6865c7 for this slice: project.html (lines 53, 57, 390, 392, 393, 540), cards.json (E1-c102, E1-c136 added), with L07.html and L09.html read because cards cite them. Round-8 FAILs E1d-proj-rubric-structure, E1d-proj-rubric-C3-C5-level2, E1d-cards-labels-resolve and E1d-cards-c102-section-locator are fixed and re-verified. Not checked: repo-wide mypy and full pytest (outside slice); tools/build_site.py not re-run; live browser screenshot; L01-L08 lesson prose except where cards cite it; full line-by-line cross-check of every card's hypotheses against its lesson proof (E1d-cards-read-complete). The E1-c102 'Section 4' literal-text check in cards_refs_r8.py is a false positive for a numbered heading (E1d-cards-labels-resolve).",
 "summary": "Slice d (project.html, grader, project labs, cards.json), round 9. Verdict FAIL. Round-8 defects fixed. New rubric defects: C3 welfare-without-DWL unplaceable, C4 all-three-unsigned unplaceable, C1 two-structure timing gap; exemplar B's C2 score 4 unsupported (no Bertrand derivation). One UNVERIFIABLE: full cross-check of card hypotheses against lesson proofs.",
}
p = pathlib.Path("ledgers/E1/E1-d.json")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "FAIL", sum(r["status"]=="FAIL" for r in rows), "UNVER", sum(r["status"]=="UNVERIFIABLE" for r in rows))
