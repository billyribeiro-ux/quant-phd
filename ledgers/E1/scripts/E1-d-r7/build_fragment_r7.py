"""Assembles the round-7 fragment for E1 slice d from the checks run in this checkout."""
import json, sys
from pathlib import Path
SC = "ledgers/E1/scripts/E1-d-r7"
P = "PASS"; F = "FAIL"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix or ""
    rows.append(r)

# ---- project page, labs, rubric (2.5, 2.6)
row("E1d-proj-lab1-numbers", "2.5-lab", "course/modules/E/E1/project.html lab-E1-project-1 (lines 55-128)", P,
    f"{SC}/lab_page_vs_twin.txt: page code == twin (lab 1) and twin output (python -I -W error) == expected block. Printed numbers re-derived in {SC}/lab3_numbers_r7.py and by hand (monopoly 50/70/2500/1250/3750/1250; Cournot 200/3->67, 160/3->53, 20000/9->2222, 40000/9->4444, 5000/9->556; Bertrand 100/20/0/5000/5000/0).")
row("E1d-proj-lab2-numbers", "2.5-lab", "course/modules/E/E1/project.html lab-E1-project-2 (lines 130-187)", P,
    f"{SC}/lab_page_vs_twin.txt: completion page code differs from twin only at the two ___ blanks (diff shown); twin output == expected block (True). Blank contents match the interpretation text (line 186): (d - rival)/2 and (a*volume - volume*volume/2)/b - c*volume. 60-step error d/(3*2^60) recomputed.")
row("E1d-proj-lab3-tie-numbers", "2.5-lab", "course/modules/E/E1/project.html lab-E1-project-3 (lines 189-257)", P,
    f"{SC}/lab3_numbers_r7.py output reproduces all 12 rows of the expected block (a=120: 50,70,2500,1250,3750,1250 / 67,53,2222,2222,4444,556 / 100,20,0,5000,5000,0; a=121: 51,71,2550,1275,3825,1275 / 67,54,2267,2267,4534,567 / 101,20,0,5101,5101,0). Hypothesis numbers (10201/4 -> 2550, 141/2 -> 71, 101/2 -> 51) confirmed.")
row("E1d-proj-lab-twins", "2.5-lab", "tests/labs/E1/lab-E1-project-{1,2,3}.py; project.html data-run blocks", P,
    f"{SC}/lab_page_vs_twin.txt: lab 1 and lab 3 page code == twin (whitespace-stripped); lab 2 differs only at the ___ blanks. All three twins run under python -I -W error and match expected blocks. run_labs E1 PASS (12/12) in {SC}/gates.txt.")
row("E1d-proj-prop1", "2.4-math", "course/modules/E/E1/project.html prop-1 (id=prop-1, lines 284-287)", P,
    "Re-derived: pi(Q) = -Q^2/b + (d/b)Q; pi' = (d-2Q)/b; Q*=d/2; f(Q*) = (a+bc)/(2b); pi* = d^2/(4b). Hypotheses stated (a>bc>0, b>0, constant c). Proof complete.")
row("E1d-proj-prop2", "2.4-math", "course/modules/E/E1/project.html prop-2 (id=prop-2, lines 289-292)", P,
    "Re-derived: best response max(0,(d-q_j)/2) from second derivative -2/b; equilibrium excludes q_1=0 via q_2=d/2 -> q_1=d/4>0; symmetric q=d/3; fee (a+2bc)/(3b); per-exchange profit d^2/(9b), total 2d^2/(9b); iteration error d/(3*2^k) from e_{k+1}=-e_k/2. Proof complete; hypotheses stated.")
row("E1d-proj-prop3", "2.4-math", "course/modules/E/E1/project.html prop-3 (id=prop-3, lines 294-297)", P,
    "Case analysis over f1<=f2 covers f1<c; f1>c with f2>f1; f1=f2>c; f1=c<f2; each non-equilibrium has a profitable deviation (g=(c+f1)/2, g=(f+c)/2, g in (c,f2)). Profit (f-c)(a-bg)/2 comparison checked. Equilibrium (c,c) verified. Complete.")
row("E1d-proj-prop4", "2.4-math", "course/modules/E/E1/project.html prop-4 (id=prop-4, lines 299-302)", P,
    "Re-derived: CS = int (Q-t)/b dt = Q^2/(2b); G(x)=(ax-x^2/2)/b; W'(x)=(d-x)/b; W(d)-W(Q)=(d-Q)^2/(2b); f(Q)Q = G(Q)-Q^2/(2b) gives welfare = CS + profit. Complete.")
row("E1d-proj-prop5", "2.4-math", "course/modules/E/E1/project.html prop-5 (id=prop-5, lines 304-307)", P,
    "Differences re-derived: d/6, d/3, d/(6b), d/(3b), d^2/(8b)-d^2/(18b)=5d^2/(72b), d^2/(36b). Integer-order claim: half-up moves each value by <=1/2, so exact difference >1 keeps sign; each listed bound checked from d>6b (d^2>36b^2). Holds.")
row("E1d-proj-spec-constraints", "2.6-spec", "course/modules/E/E1/project.html section 'Rung 3 · Specification' (dl.spec lines 312-323)", P,
    "Interface, key set, int type, ValueError conditions and exact messages (a must exceed b*c / b must be positive / c must be positive / structure names) match grader/reference.py lines 26-35 and tests (must_raise phrases). Constraint 'any other invalid input may ...' leaves no test over-constraint. Grading-mode count 124 = collect-only count (see E1d-proj-r7-collect-count).")
row("E1d-proj-hours", "2.6-hours", "course/modules/E/E1/project.html section 'Time budget' (#hours lines 333-349); curriculum/hub index.html line 42", P,
    "Table sums to 30 (2+3+8+8+6+3); hub 90 h lessons + 30 h project = 120. Independent estimate: reading/annotating Lab 1 about 2 h; completion 2-3 h; five proofs 6-8 h; engine plus 124-test run 3-6 h; memo 5-7 h; self-assessment 2-3 h. Total 21-29 h, within 30% of 30.")
row("E1d-proj-rubric-structure", "2.6-rubric", "course/modules/E/E1/project.html table#rubric (lines 384-395)", F,
    "C6 level 2 descriptor 'Names one or two of the limits without what changes' does not cover a memo that names all three limits and states the change for only one (exemplar B). Level 2 wording is therefore not satisfiable by that memo as written, while level 3 needs an outcome for each limit. Other descriptors (C1-C5, C6 levels 1, 3, 4) are observable.",
    "Rewrite C6 level 2 as 'Names the limits, and states what changes for at most one of them' (or equivalent), so that exemplar B matches level 2 by its text and not only by containment.")
row("E1d-proj-exemplar-blind-scoring", "2.6-rubric", "course/modules/E/E1/project.html #exemplar-a, #exemplar-b (passages, lines 401-549)", P,
    "Blind scoring by the rubric alone: A = C1 1, C2 2, C3 2, C4 2, C5 1, C6 2; B = C1 4, C2 4, C3 4, C4 4, C5 3, C6 2. Official scores (data-scores; lines 401, 466) match on every criterion; no annotation is more than one level from my score.")
row("E1d-proj-exemplar-annotation-C6", "2.6-rubric", "course/modules/E/E1/project.html #exemplar-b, Limits passage annotation (line 543)", F,
    "The annotation says 'Meets C6 level 2: names all three limits'. The level-2 descriptor (line 393) reads 'Names one or two of the limits without what changes', so the cited descriptor does not describe the memo. The annotation argues from containment rather than quoting the descriptor. Scores are within one level, so the defect is the descriptor, not the score.",
    "Fix together with the C6 level 2 descriptor (see E1d-proj-rubric-structure): change the annotation to quote the revised level-2 text.")
row("E1d-proj-autograder-reference", "2.6-autograder", "course/modules/E/E1/grader/reference.py; tools/run_graders.py", P,
    f"{SC}/gates.txt: 'run_graders E1: PASS (reference 50/50 seeds)'. Direct pytest on a workspace (reference as market_structure.py) with QF_SEED=0 and 1824812280: 124 passed ({SC}/collect_and_reference.txt).")
row("E1d-proj-autograder-instances", "2.6-autograder", "course/modules/E/E1/grader/instance.py", P,
    f"{SC}/instance_orderings_r7.txt: seeds 0-199 all valid (a > bc > 0), 200 distinct output sets, b in {{1,2,3}}, c in 5..60, gap in 60..400 (matches the docstring). Strict rounded orderings the tests assert hold on all 200 seeds (volume, fee, welfare, DWL, profit).")
row("E1d-proj-mutant-float-rounding", "2.6-mutation", "course/modules/E/E1/grader/test_project.py test_large_exact_inputs_round_from_exact_values; ledgers/E1/mutants/r6d_m01_half_up_in_float_wrong_for_large_inputs.py", P,
    f"{SC}/mutate_E1_seeds0-9_r7_full.txt: 'KILLED r6d_m01 ... -> test_large_exact_inputs_round_from_exact_values[monopoly] (seed 0)'. The round-6 survivor is now killed.")
row("E1d-proj-mutant-new-m02", "2.6-mutation", "ledgers/E1/mutants/r6d_m02_profit_is_revenue_not_margin.py", P,
    f"{SC}/mutate_E1_seeds0-9_r7_full.txt: KILLED by test_reference_case_matches_closed_forms[profit_cents-cournot] (seed 0).")
row("E1d-proj-mutant-new-m03", "2.6-mutation", "ledgers/E1/mutants/r6d_m03_a_must_cover_cost_twice.py", P,
    f"{SC}/mutate_E1_seeds0-9_r7_full.txt: KILLED by test_smallest_valid_case_is_accepted[103-3-34-monopoly] (seed 0).")
row("E1d-proj-mutant-new-m04", "2.6-mutation", "ledgers/E1/mutants/r6d_m04_welfare_takes_half_consumer_surplus.py", P,
    f"{SC}/mutate_E1_seeds0-9_r7_full.txt: KILLED by test_closed_form_matches[welfare_cents-monopoly] (seed 0).")
row("E1d-proj-mutant-new-m05", "2.6-mutation", "ledgers/E1/mutants/r6d_m05_monopoly_fee_sign_error_on_cost.py", P,
    f"{SC}/mutate_E1_seeds0-9_r7_full.txt: KILLED by test_closed_form_matches[fee_cents-monopoly] (seed 0).")
row("E1d-proj-mutant-existing", "2.6-mutation", "ledgers/E1/mutants/*.py (102 prior mutants)", P,
    f"{SC}/mutate_E1_seeds0-9_r7_full.txt: 'mutate_graders E1: PASS (107/107 killed)' over all 107 mutants with --seeds 0-9; zero SURVIVED lines.")
row("E1d-proj-alt-integer-pairs", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt1_integer_pairs.py", P,
    f"{SC}/alternatives_seeds0-49.txt: alt1_integer_pairs passes seeds 0-49. The round-6 over-constraint came from the float-input test, which is removed (test_project.py line 322 now tests integer inputs only). Page Constraints say 'Any other invalid input may raise any exception or return a value', so 120.0 is not constrained.")
row("E1d-proj-alt-cramer", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt3_cramer.py", P,
    f"{SC}/alternatives_seeds0-49.txt: passes seeds 0-49 (Cramer's rule in Fractions).")
row("E1d-proj-alt-decimal", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt2_decimal_half_up.py", P,
    f"{SC}/alternatives_seeds0-49.txt: passes seeds 0-49 (Decimal, prec 60, ROUND_HALF_UP).")
row("E1d-proj-alt-trapezoid", "2.6-autograder", "ledgers/E1/scripts/E1-d-r6/alt4_trapezoid_consumer.py", P,
    f"{SC}/alternatives_seeds0-49.txt: passes seeds 0-49.")
row("E1d-proj-r7-alternatives", "2.6-autograder", "ledgers/E1/scripts/E1-d-r7/alts/*.py; ledgers/E1/scripts/alt1..alt5", P,
    f"{SC}/alternatives_seeds0-49.txt: 9 correct alternatives pass all 50 seeds (closed form, linear system, fraction vertex, integer-pair arithmetic, Decimal, Cramer, trapezoid, pure integer arithmetic, common-denominator Fraction). Rejected: alt2_best_response (float iteration, fails test_large_exact_inputs_round_from_exact_values[cournot]) and alt5_float_half_up (fails [monopoly]). Both violate the page's exact-fraction rule, so they are real faults, not over-constraint.")
row("E1d-proj-pyodide-local", "2.6-autograder", "tools/page_smoke.py --unit E1 --pages project", P,
    f"{SC}/gates.txt: 'in-browser grader: All 124 tests pass on seed 1824812280'; 'page_smoke modules/E/E1/project.html: PASS'; lab runtimes 0.0 s; boot 1.2 s.")
row("E1d-proj-ruff-mypy", "2.6-autograder", "tests/labs/E1; course/modules/E/E1/grader; repo", P,
    f"{SC}/gates.txt: 'ruff check tests/labs/E1 course/modules/E/E1/grader: All checks passed'; 'mypy --no-incremental: Success: no issues found in 255 source files'. gates2.txt: ruff check . and ruff format --check . pass (362 files).")
row("E1d-proj-check-gates", "2.9-structure", "tools/check_projects.py, check_pages.py, check_dag.py, run_labs.py, verify_refs.py, build_site.py", P,
    f"{SC}/gates.txt and gates2.txt: 'check_projects E1: PASS', 'check_pages E1: PASS', 'check_dag E1: PASS', 'run_labs E1: PASS (12/12)'; build_site --check 'site data current'. pytest -k E1 over test_labs, test_run_labs, test_page_checks: 13 passed.")
row("E1d-proj-reference-varian", "2.1-citations", "references/references.json key varian2014intermediate; course/modules/E/E1/project.html #reading and #references", P,
    f"Registry record: Open Library OL28519988M, 'Intermediate Microeconomics: A Modern Approach', Varian, 2014. Live: tools/verify_refs.py --unit E1 -> 'live re-verification of E1: 1 of 560 entries, 0 problems' ({SC}/verify_refs_E1_live.txt). Plain curl https://openlibrary.org/books/OL28519988M.json -> HTTP 200. Page cites no locator and attributes no statement (line 569).")
row("E1d-proj-notation", "2.9-notation", "notation/notation.json; course/modules/E/E1/project.html math (197 spans)", P,
    "Registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. The project uses a, b, c, d, Q, f, q, q_i, q_j, W, G, pi, CS-type names, none of which is registered or reused with a registered meaning. The plain Q is volume, not the registered \\mathbb{Q} measure.")
row("E1d-proj-banned", "2.9-structure", "course/modules/E/E1/project.html; course/modules/E/E1/cards.json", P,
    f"{SC}/gates.txt: check_pages E1 PASS includes the banned-phrase scan (tools/check_pages.py BANNED tuple). Process words (verif, builder, revis, round N, agent) grep-empty in project.html and cards.json.")
row("E1d-proj-delta-r5", "2.6-delta", "course/modules/E/E1/project.html (6 hunks: lines 53, 183, 319, 540, 569); grader/test_project.py (1 hunk, 322-330); tests/labs/E1/lab-E1-L01-1.py (docstring); cards.json (see E1d-cards-delta-r5)", P,
    "Delta 44f1eb6..7aa909e read hunk by hunk. Project prose changes: printed-output pointer to Definitions, exact-rounding wording for lab 2 interpretation, grading count 124, C6 annotation text (see E1d-proj-exemplar-annotation-C6), Reading wording. Grader change: float-input test replaced by large-exact-input test (verified killing r6d_m01 and passing alternatives). Each hunk re-verified above.")
row("E1d-proj-reading-section", "2.1-citations", "course/modules/E/E1/project.html section 'Reading' (lines 567-573)", P,
    "Text now says 'the reference this page cites' and attributes no statement; the only reference is varian2014intermediate (registry key present, live-verified).")

# ---- cards (2.7)
sample_ids = ["E1-c010","E1-c020","E1-c030","E1-c040","E1-c050","E1-c060","E1-c070","E1-c080","E1-c090","E1-c100","E1-c110","E1-c120","E1-c130"]
sample_notes = {
 "E1-c010": "MRS = p_x/p_y at optimum: y/x = (m/(2p_y))/(m/(2p_x)) = p_x/p_y; L01 Proposition 2.3 and 1.4 printed.",
 "E1-c020": "pi(q*)-pi(0) = (p-c)^2/(4k) recomputed; L02 Remark 1.6 printed; 'provided p > c' matches.",
 "E1-c030": "p* = (a+sc)/(b+s), s=n/(2k), Q*=s(p*-c), p*-c=(a-bc)/(b+s) recomputed; L03 Proposition 1.3 printed.",
 "E1-c040": "epsilon = -bp/(a-bp) recomputed; L04 Example 1.3 printed.",
 "E1-c050": "dQ*/da = S'dp*/da; Example 2.4 gives 10/11 at a=120 (1 - 2/22); L04 Proposition 2.3 printed ('Proposition 2.3.' is a regex artefact).",
 "E1-c060": "p_m = (c + a/b)/2 and p_m - c = (a-bc)/(2b) recomputed; L05 Problem R2 and Proposition 5.2 printed.",
 "E1-c070": "Monopoly d/2, fee (a+bc)/(2b), profit d^2/(4b) re-derived; L06 Proposition 1.4 printed.",
 "E1-c080": "Bertrand fee-lower-takes-all, tie rule, Definition 3.1 text read in L06 (any tie rule).",
 "E1-c090": "R(0)=d/2 and R(x)=max(0,(d-x)/2) zero for x>=d recomputed; L06 Lemma 2.4 read.",
 "E1-c100": "W_comp = d^2/(2b) = 5000; DWL_M = d^2/(8b) = 1250; DWL_C = d^2/(18b) = 5000/9 -> 556 (half up). L07 Example 2.2 printed.",
 "E1-c110": "Off-diagonal improvement statement matches L08 Proposition 2.2 text (strictly raises both utilities).",
 "E1-c120": "MSC = c+e; q_s=(a-c-e)/b; q_p=(a-c)/b; matches L09 Definition 1.2.",
 "E1-c130": "(1000-200-100)/10 = 70; (b/2)(70-68)^2 = 20 with b=10; matches L09 Lab 1 text and misconception 3.",
}
for sid in sample_ids:
    row(f"E1d-cards-sample-{sid[-3:]}", "2.7-cards", f"course/modules/E/E1/cards.json {sid}", P,
        f"Card text checked against its lesson and recomputed: {sample_notes[sid]} Full-scan label, number and duplicate scripts: {SC}/cards_labels_r7.txt, cards_numbers_r7.txt, cards_dup_scan.txt.")
row("E1d-cards-full-scan-duplicates", "2.7-cards", "course/modules/E/E1/cards.json (135 cards)", F,
    f"{SC}/cards_scan.txt: 135 cards, no duplicate ids, fronts or backs. Near-duplicate facts (cards_dup_scan.txt and reading): E1-c019 vs E1-c134 (both: Proposition 1.5, fixed cost leaves output unchanged); E1-c034 vs E1-c135 (both: Remark 2.2, market supply is n times one firm's supply, with the same Example 1.5 numbers 48/7 and 480/7); E1-c065 vs E1-c071 (both: reference monopoly outcome 50 units, 70 cents, 2500 cents, L05 and L06); E1-c088 repeats the monopoly outcome again; E1-c100 vs E1-c105 (both L07: reference-case CS 1250, PS 2500, W 3750, DWL 1250, and Cournot DWL 556).",
    "Remove the duplicate card or merge it into one card per fact: drop E1-c134 (or E1-c019) and E1-c135 (or E1-c034); keep one of E1-c065/E1-c071/E1-c088 and one of E1-c100/E1-c105. Renumber with a clean sequence afterward only through the generator.")
row("E1d-cards-lab-graded", "2.7-cards", "course/modules/E/E1/cards.json grade C cards (E1-c014, c025, c027, c036, c051, c066, c084, c085, c105, c115, c129, c131, c132, c133)", P,
    f"14 grade-C cards each carry a basis naming Lab 1 with its part (checked against lesson labs); check_pages E1 cards check passes ({SC}/gates.txt). Grade-less cards are definitions and formulas, which BUILDER_RULES §7 does not grade.")
row("E1d-cards-numbers-in-lesson", "2.7-cards", "course/modules/E/E1/cards.json; L01-L09.html", P,
    f"{SC}/cards_numbers_r7.py: 0 number tokens on any card back or front missing from the card's own lesson text (checked literally, and fractions via flexible match). Sample: 110/7, 48/7, 480/7 in L03; 1111.11 in L06; F = 100 in L02.")
row("E1d-cards-labels-resolve", "2.7-cards", "course/modules/E/E1/cards.json (all 'Misconception', 'Proposition', 'Remark', 'Example', 'Corollary', 'Problem', 'Definition', 'Lemma', 'Theorem', 'Section' citations)", P,
    f"{SC}/cards_labels_r7.py: 194 label citations checked against the named lesson text (or 'Lesson N' cross-reference): 0 unresolved after review (2 regex hits reviewed: 'Proposition 2.3.' in E1-c050 is present; 'Section 3' in E1-c102 is the lesson's 'Where the canon breaks' section, which contains the transfer argument). 0 'Misconception N' labels remain; the 18 former labels are now prose. The misconception statements on cards (c012, c024, c026, c035, c048, c049, c050, c062-c064, c091, c102, c104, c116-c118, c128-c130) match the L01-L09 'Misconceptions' sections.")
row("E1d-cards-profit-sign-c019", "2.7-cards", "course/modules/E/E1/cards.json E1-c019", P,
    "Back now reads 'The profit under F' equals the profit under F minus F' - F at every output (Proposition 1.5)'. This matches L02 Proposition 1.5 text (profit under F' equals profit under F minus F' - F) and its proof pi_F'(q) = pi_F(q) + (F - F'). Sign correct.")
row("E1d-cards-hypotheses", "2.7-cards", "course/modules/E/E1/cards.json E1-c023, E1-c041, E1-c075", P,
    "c023 now opens 'Under the Setting (k > 0)' (L02 Setting, k > 0); c041 opens 'Under a > 0 and b > 0, for 0 < p < a/b' (L04 Proposition 1.4 hypotheses); c075 opens 'Under the hypotheses of Definition 1.1 (b > 0, c > 0, a > bc)' (L06 Lemma 2.4 assumes the hypotheses of Definition 1.1). Each now carries its proposition's hypotheses.")
row("E1d-cards-delta-r5", "2.7-cards", "course/modules/E/E1/cards.json (changed cards: c012, c019, c023, c024, c026, c033, c035, c041, c048, c049, c050, c056, c057, c060, c062, c063, c064, c075, c102-c104 area, c134, c135 added)", P,
    "Every changed card read against the current lesson text: hypotheses added (c023, c041, c056, c057, c060, c075, c033), misconception labels replaced by statements (checked against the Misconceptions sections), c134 and c135 added (see duplicate row).")
row("E1d-cards-r7-new-c134-c135", "2.7-cards", "course/modules/E/E1/cards.json E1-c134, E1-c135", F,
    "Both cards are added this round and both test facts already carried by existing cards: E1-c134 repeats E1-c019 (Proposition 1.5, same output under two fixed costs); E1-c135 repeats E1-c034 (Remark 2.2 and Example 1.5 numbers). Their content is correct against L02 and L03 text, but they are duplicate cards.",
    "Delete E1-c134 and E1-c135 (their facts are on E1-c019 and E1-c034), or rewrite each to test a fact no other card tests. Then re-run cards_scan.py and cards_dup_scan.py.")
row("E1d-cards-lessons-tier", "2.9-structure", "course/modules/E/E1/cards.json; L01-L09.html", P,
    f"{SC}/gates.txt: check_pages E1 PASS (card-lesson names exist; every lesson has cards: L01 14, L02 14, L03 11, L04 17, L05 13, L06 25, L07 14, L08 13, L09 14).")
row("E1d-cards-read-complete", "2.7-cards", "course/modules/E/E1/cards.json (135 cards read)", P,
    "All 135 cards printed and read in full; scripts cards_scan.py, cards_labels_r7.py, cards_numbers_r7.py, cards_dup_scan.py cover all cards mechanically.")

# ---- new rows for this round
row("E1d-proj-r7-mutants-new", "2.6-mutation", "ledgers/E1/mutants/r7v_m01..m05 (written this round); scripts/E1-d-r7/make_r7_mutants.py", P,
    f"Five new student-error mutants, each killed at seed 0: r7v_m01 float true division (test_large_exact_inputs_round_from_exact_values[monopoly]); r7v_m02 linear deadweight (test_closed_form_matches[deadweight_loss_cents-monopoly]); r7v_m03 welfare minus profit (test_closed_form_matches[welfare_cents-monopoly]); r7v_m04 Bertrand profit forgets cost (test_closed_form_matches[profit_cents-bertrand]); r7v_m05 Cournot fee monopoly formula (test_closed_form_matches[fee_cents-cournot]). Output in {SC}/mutate_E1_seeds0-9_r7_full.txt.")
row("E1d-proj-r7-collect-count", "2.6-autograder", "course/modules/E/E1/grader/test_project.py; project.html Grading mode (line 322)", P,
    "pytest --collect-only in a workspace with reference.py as market_structure.py: 124 tests collected. Page says 124 checks.")
row("E1d-proj-r7-gates-lint", "2.9-structure", "repo", P,
    f"{SC}/gates2.txt: check_projects/check_pages/check_dag E1 PASS; build_site --check current; ruff check . and format check pass; {SC}/gates.txt mypy strict on the repo passes.")

verdict = "PASS" if all(r["status"] == P for r in rows) else "FAIL"
mutants = [
    {"id": "r7v_m01_float_division_everywhere", "description": "Student uses float true division for every exact quotient, then rounds the float once.", "killed_by": "test_large_exact_inputs_round_from_exact_values[monopoly] (seed 0)"},
    {"id": "r7v_m02_deadweight_not_squared", "description": "Student writes the deadweight loss as the linear gap (d - Q)/(2b), dropping the square of the triangle.", "killed_by": "test_closed_form_matches[deadweight_loss_cents-monopoly] (seed 0)"},
    {"id": "r7v_m03_welfare_minus_profit", "description": "Student subtracts exchange profit from consumer surplus for welfare, a sign error on the profit term.", "killed_by": "test_closed_form_matches[welfare_cents-monopoly] (seed 0)"},
    {"id": "r7v_m04_bertrand_profit_forgets_cost", "description": "Student takes Bertrand profit as fee times volume, forgetting the cost of one trade.", "killed_by": "test_closed_form_matches[profit_cents-bertrand] (seed 0)"},
    {"id": "r7v_m05_cournot_fee_monopoly_formula", "description": "Student copies the monopoly fee (a + bc)/(2b) into the Cournot branch instead of (a + 2bc)/(3b).", "killed_by": "test_closed_form_matches[fee_cents-cournot] (seed 0)"},
]
pin = "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4"
frag = {
  "unit": "E1", "slice": "d", "round": 7,
  "verifier": "independent verifier (Haiku 5.5), round 7",
  "pin": pin, "base": "44f1eb6",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-E1-d",
  "scratch": "/tmp/e1d-r7-ws, /tmp/e1d-r7-alt-* (removed after each run)",
  "verified_at": "2026-10-28T00:00:00+00:00",
  "verdict": verdict,
  "rows": rows,
  "mutants": mutants,
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Slice d: course/modules/E/E1/project.html, grader/ (reference, starter, instance, test_project), tests/labs/E1/lab-E1-project-{1,2,3}.py, cards.json (135 cards; the previous fragment recorded 133).",
    "Delta 44f1eb6..7aa909e read hunk by hunk for project.html, grader/test_project.py, tests/labs/E1/lab-E1-L01-1.py (docstring only, outside slice), cards.json.",
    "Mutation: tools/mutate_graders.py --unit E1 --seeds 0-9 over 107 files in ledgers/E1/mutants (102 prior + 5 new r7v): 107/107 killed. Output in ledgers/E1/scripts/E1-d-r7/mutate_E1_seeds0-9_r7_full.txt.",
    "Alternatives: 11 implementations run over seeds 0-49 (ledgers/E1/scripts/E1-d-r7/alternatives_seeds0-49.txt); 9 correct ones pass, 2 float-based ones fail on exact large inputs, which the page's exact-fraction rule forbids.",
    "Live verify_refs --unit E1: 1 of 560 entries, 0 problems. Offline integrity: 560 entries, 0 problems.",
    "Not checked: the full CI gate (the pytest suite outside E1 slice; test_labs.py fails for unit E3 in the previous round, not in this slice); figure sweeps (no figures in project page); lesson-level prose and labs of L01-L09 (other slices); the 13 card samples are read against lesson text, not a full line-by-line proof check of every card; live browser screenshot of the grader panel; hours estimate is independent but approximate."
  ],
  "summary": (f"E1 slice d verdict {verdict}. Previous round's float-rounding survivor is killed; the float-input over-constraint is gone; the 18 Misconception labels and the c019/c023/c041/c075 defects are fixed. "
              "Remaining FAILs: (1) C6 level 2 rubric descriptor does not describe exemplar B, and its annotation cites it; (2) duplicate cards: E1-c134 repeats E1-c019 and E1-c135 repeats E1-c034 (both added this round); plus reference-case duplicates E1-c065/c071/c088 and E1-c100/c105.")
}
out = Path(sys.argv[1])
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fails", sum(r["status"] != P for r in rows), "verdict", verdict)
