"""Build the round-5 fragment for E1 slice E1-d from the verifier's recorded results (verifier r5)."""
import json
import re
from pathlib import Path

ROOT = Path("/tmp/verifyB5-E1-d")
S = "ledgers/E1/scripts/E1-d-r5"
PIN = "09b87514c240fd5cc904939ec6aba2ca0388ede4"
P = "course/modules/E/E1/project.html"
C = "course/modules/E/E1/cards.json"

def row(i, check, loc, status, evidence, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
    row("E1d-gate-projects", "2.9 check_projects --unit E1", "tools/check_projects.py",
        "PASS", f"{S}/check_projects.txt; unit run: 'check_projects E1: PASS' (pin {PIN[:7]})."),
    row("E1d-gate-pages-dag", "2.9 check_pages, check_dag --unit E1", "tools/check_pages.py; tools/check_dag.py",
        "PASS", f"{S}/check_pages.txt: 'check_pages E1: PASS'; {S}/check_dag.txt: 'check_dag E1: PASS'."),
    row("E1d-gate-graders", "2.5 run_graders --unit E1 --seeds 0-49", "course/modules/E/E1/grader/",
        "PASS", f"{S}/run_graders_E1_seeds0-49.txt: 'run_graders E1: PASS (reference 50/50 seeds, slowest 0.2 s)'."),
    row("E1d-gate-mutants", "2.6 mutate_graders --unit E1 --seeds 0-9 (all mutants)", "ledgers/E1/mutants/ (77 files)",
        "PASS", f"{S}/mutate_E1_seeds0-9_r5.txt: 'mutate_graders E1: PASS (77/77 killed)'. The earlier run before the new mutants: 73/73 ({S}/mutate_E1_seeds0-9.txt)."),
    row("E1d-mutants-existing", "2.6 every mutant the builder or an earlier verifier wrote", "ledgers/E1/mutants/f*, fx*, m*, r2_*, r3_*, r4_*, r5_*, v*, vx4_*",
        "PASS", "All 73 pre-existing mutants KILLED on seeds 0-9 (run before my additions); the ten r5_m01..r5_m10 mutants are in the same run and KILLED (listed in mutants)."),
    row("E1d-mutants-r3", "2.6 round-3 mutants r3_m01..r3_m04", "ledgers/E1/mutants/r3_m01..r3_m04.py",
        "PASS", f"{S}/mutate_E1_seeds0-9_r5.txt: all four KILLED on seed 0 (floor division of the monopoly volume; profit from the rounded volume; Bertrand volume without b; surplus on the rounded fee)."),
    row("E1d-mutants-vx4", "2.6 round-4 mutants vx4_m01..vx4_m04", "ledgers/E1/mutants/vx4_m01..vx4_m04.py",
        "PASS", f"{S}/mutate_E1_seeds0-9_r5.txt: all four KILLED on seed 0 (consumer surplus with the slope b dropped; welfare from rounded parts; deadweight loss by floor division; fee from the printed volume)."),
    row("E1d-mutants-v5", "2.6 >= 3 NEW student-error mutants of mine", "ledgers/E1/mutants/v5_m01..v5_m04.py",
        "PASS", "Four new: v5_m01 welfare with the 1/b factor dropped from the quadratic term; v5_m02 cost check c < 0 (c = 0 accepted); v5_m03 Cournot volume from ten best-response steps (not exact); v5_m04 deadweight loss measured from the monopoly volume for every structure. All four KILLED on seed 0 (run_alts_r5 seeds 0-9 FAIL; mutate run above)."),
    row("E1d-labs-run", "2.5 run_labs --unit E1; the three project twins under python -I -W error",
        "tests/labs/E1/lab-E1-project-{1,2,3}.py; course/modules/E/E1/project.html",
        "PASS", f"{S}/run_labs_E1.txt: 'run_labs E1: PASS (12/12)'. Twins run rc 0 under -I -W error (outputs {S}/lab-E1-project-{{1,2,3}}.out). {S}/embed_compare_project.py: project-1 and project-3 code identical to twin and expected == run output; project-2 differs from its twin only in its two blank lines (reaction and welfare_cents), and its expected output equals the run."),
    row("E1d-smoke", "2.5 page_smoke --unit E1 --pages project (Pyodide timing)", "course/modules/E/E1/project.html",
        "PASS", f"{S}/page_smoke_project.txt: 'in-browser grader: All 118 tests pass on seed 1518818653. (0.9 s)'; 'page_smoke E1: PASS'."),
    row("E1d-lint-types", "ruff check/format and mypy on the E1 labs and grader", "tests/labs/E1; course/modules/E/E1/grader",
        "PASS", f"{S}/ruff.txt: 'All checks passed!', '16 files already formatted'; {S}/mypy.txt: 'Success: no issues found in 255 source files', rc 0."),
    row("E1d-test-count", "2.9 test count on the page equals collect-only count", f"{P} (Grading mode); course/modules/E/E1/grader/test_project.py",
        "PASS", "Staged reference as market_structure.py in a scratch workspace: 'pytest --collect-only' -> '118 tests collected'; full run with QF_SEED=392601084: '118 passed'. Page: 'runs 118 checks'."),
    row("E1d-alternatives", "2.6 five alternative correct implementations plus extra valid algorithms, seeds 0-49",
        f"{S}/run_alts_r5.py; ledgers/E1/scripts/alt1..alt5, alt_a..alt_d",
        "PASS", "run_alts_r5.py (seeds 0-49): alt1_closed_form, alt2_best_response, alt3_linear_system, alt4_fraction_vertex, alt5_float_half_up, alt_a_linear_solve, alt_b_simpson, alt_c_decimal, alt_d_iterate_cutoff: all PASS."),
    row("E1d-instance", "2.4 instance.py generator, docstring claims", "course/modules/E/E1/grader/instance.py",
        "PASS", "Code unchanged (only the docstring unit wording changed this round). Re-derived: b in 1..3, c in 5..60, gap in 60..400 so gap > 6b (18 at most) on every seed; fee gaps d/(6b) >= 3.3 and d/(3b) >= 6.6 exceed 1; the suite passes on seeds 0-49."),
    row("E1d-exceptions", "2.4 exception table vs the page's Constraints", f"{P} (Constraints); grader/test_project.py (must_raise, UNKNOWN_STRUCTURES)",
        "PASS", "Constraints names ValueError for: a structure not one of the three names (padded, capitalised, non-string) with the message naming all three; a <= bc with 'a must exceed b*c'; b <= 0 with 'b must be positive'; c <= 0 with 'c must be positive'. Tests check exactly these; other invalid input is not constrained (test_non_integer_inputs accepts any exception)."),
    row("E1d-grader-coverage", "2.4 each named exception is tested with several structures and values", "grader/test_project.py",
        "PASS", "The three exception tests are parametrised over the structures and over (a, b, c) pairs (a: 3 pairs; b: 2; c: 2); r4 mutants fx01..fx11 and r5_m01..m10 are killed by these tests."),
    row("E1d-grader-spec-trace", "2.4 every grading-mode claim traced to a test", f"{P} (Grading mode); grader/test_project.py",
        "PASS", "The page lists: six outputs vs exact closed forms (test_closed_form_matches), ordering (test_volume_ordering, test_fee_ordering, test_welfare_ordering, test_deadweight_loss_ordering), exception table, integer types (test_every_output_is_an_int), tie and half rounding (test_tie_rounds_up_for_each_output, test_value_below/above_a_half), standard-library rule (test_module_imports_only_the_standard_library), purity (test_outcome_prints_nothing), second instance (test_second_instance_matches_closed_forms). Each is present."),
    row("E1d-spec-grader-agree", "2.4 starter, reference and tests agree on the signature and key set", "grader/starter.py; grader/reference.py; grader/test_project.py",
        "PASS", "outcome(structure: str, a: int, b: int, c: int) -> dict[str, int] in starter.py and reference.py; the six keys equal the page's Required outputs (test_outcome_has_exactly_the_six_keys)."),
    row("E1d-prop1", "2.4 Proposition 1 (monopoly) statement and proof", f"{P} #prop-1 (line 201 of the extracted text)",
        "PASS", "Re-derived: pi(Q) = -Q^2/b + (d/b)Q; pi' = (d - 2Q)/b; pi'' = -2/b < 0; Q* = d/2; fee (a + bc)/(2b); profit d^2/(4b). Hypotheses a > bc > 0, b > 0 stated. Proposition text re-read this round (unchanged)."),
    row("E1d-prop2", "2.4 Proposition 2 (Cournot) statement, existence and uniqueness, iteration error", f"{P} #prop-2",
        "PASS", "Re-derived: best response max(0,(d - q_j)/2) from pi_i' = (d - 2q_i - q_j)/b; a zero rival quantity gives q_1 = d/4 > 0 (contradiction); equal quantities d/3; existence by checking the reaction equations; iteration e_{k+1} = -e_k/2, |e_k| = d/(3*2^k); profit d^2/(9b) each; fee (a + 2bc)/(3b)."),
    row("E1d-prop3", "2.4 Proposition 3 (Bertrand) statement and proof", f"{P} #prop-3",
        "PASS", "Re-checked each case: f1 < c (negative margin; raising to c gains, including a tie); f1 = c < f2 (lower fee raises to g in (c, f2), gains); f1 > c, f2 > f1 (undercut to (c+f1)/2 gains); f1 = f2 = f > c (g = (f+c)/2 gains); the proof is complete and the statement's hypotheses (fees in [0, a/b], a > bc > 0) are used."),
    row("E1d-prop4", "2.4 Proposition 4 (surplus identities)", f"{P} #prop-4",
        "PASS", "CS = int_0^Q (Q - t)/b dt = Q^2/(2b); G(x) = (ax - x^2/2)/b; W' = (d - x)/b; W(d) - W(Q) = (d - Q)^2/(2b); G(Q) - cQ = Q^2/(2b) + (f(Q) - c)Q since f(Q)Q = G(Q) - Q^2/(2b)."),
    row("E1d-prop5", "2.4 Proposition 5 (ordering) and its integer claim", f"{P} #prop-5",
        "PASS", "Each exact difference re-derived: d/6, d/3; d/(6b), d/(3b); d^2/(8b) - d^2/(18b) = 5d^2/(72b); d^2/(18b); d^2/(36b). Printed-order claim: exact difference > 1 keeps the sign after half-up rounding (|round(x) - x| <= 1/2); with d > 6b every difference exceeds 1 (d/6 > b >= 1; d^2/(18b) > 2b >= 2; 5d^2/(72b) > 5b/2 >= 1; d^2/(36b) > b >= 1)."),
    row("E1d-lab1-prose", "2.2 Lab 1 prose numbers vs run", f"{P} lab-E1-project-1 (lines 23 and 81)",
        "PASS", "Stated: d = 100; monopoly 50 and 70; Cournot 200/3 -> 67 and 160/3 -> 53; Bertrand 100, 20, DWL 0. Run output (lab-E1-project-1.out): 'monopoly volume 50 trades -> 50; fee 70 cents -> 70'; 'cournot volume 200/3 trades -> 67; fee 160/3 cents -> 53'; 'bertrand ... deadweight loss 0 -> 0 cents'. Cournot profit 20000/9 -> 2222, welfare 40000/9 -> 4444, DWL 5000/9 -> 556: recomputed."),
    row("E1d-lab2-prose", "2.2 Lab 2 prose: blanks, 10^-12 claim, printed values", f"{P} lab-E1-project-2 (lines 83 and 122)",
        "PASS", "Run: 'gap from d/3 after 60 steps is below 10^-12: True'; volume 67; fee 53; welfare 4444. The error formula (-1/2)^k(-d/3) and size d/(3*2^60) = 2.9e-17 < 1e-12 re-derived. welfare exact 40000/9 re-derived."),
    row("E1d-lab2-blanks", "2.5 Lab 2 page code vs twin", f"{P} lab-E1-project-2; tests/labs/E1/lab-E1-project-2.py",
        "PASS", "Diff of page code against the twin (embed_compare_project.py and diff): only line 28 (return (d - rival)/2 vs ___) and line 33 (half_up((a*volume - volume*volume/2)/b - c*volume) vs half_up(___)) differ. Docstrings identical."),
    row("E1d-lab3-numbers", "2.2 Lab 3 reference numbers, including the tie case a = 121", f"{P} lab-E1-project-3 (lines 124, 177)",
        "PASS", "Recomputed a = 121 by hand: monopoly fee 141/2 -> 71, volume 101/2 -> 51, profit 10201/4 -> 2550, CS 1275.125 -> 1275, welfare 3825.375 -> 3825, DWL 1275.125 -> 1275; Cournot volume 202/3 -> 67, fee 161/3 -> 54, profit 20402/9 -> 2267, welfare 40804/9 -> 4534, DWL 10201/18 -> 567; Bertrand CS 5100.5 -> 5101. All match lab-E1-project-3.out."),
    row("E1d-lab3-location", "2.3 Lab 3 named as run_report.py in Required outputs and in the brief", f"{P} (Required outputs; Rung 3 · The memo)",
        "PASS", "Both places say run_report.py is Lab 3 with the closed-form call replaced by outcome; the lab's own docstring says the same."),
    row("E1d-numbers-prose", "2.2 numbers in prose (exemplars, comparison, welfare, recommendation, limits)", f"{P} Exemplar B (Summary, Welfare, Comparison, Recommendation); Limits",
        "PASS", "200/3 and 202/3 both in (66.5, 67.5): 67. 5000/9 = 555.56 -> 556; 20000/9 = 2222.22 -> 2222. Comparison: volume differences +17 and +33 (50->67, 67->100) and exact 50/3, 100/3; fee differences -17 and -33 and exact d/(6b) = 50/3; welfare +694 and +556; profit 2500 - 20000/9 = 277.8 = d^2/(36b) = 10000/36. Exemplar B derivations: q1 = 0 gives q2 = 50 and q1 = 25 > 0. Constant-cost derivatives c/2, 2/3, 1."),
    row("E1d-scope-words", "2.2 scope words (only, all, every, always, any, same, drives, never)", f"{P} (whole page; Limits; Exemplar B Limits)",
        "PASS", "Round-4 FAIL closed: the Limits sentence now reads 'the closed forms here are derived for the linear inverse demand of Proposition 1, and the memo draws no conclusion for a curved one' (no unproved property). Each remaining scope word has a computation: 'every money value is an exact fraction' (all Lab 1 code uses Fraction); 'the same time' is the simultaneous-choice definition; 'the symmetric point is the only one' (Proposition 2) is proved in the proof; 'the only zero' and 'unique' claims are proved in the propositions."),
    row("E1d-banned-process", "2.9 banned phrases and process words (learner text and cards)", f"{P} (text, pre removed); {C}",
        "PASS", "Scan of the extracted project text and cards.json for TODO, TBD, lorem, ellipsis, 'roughly', 'historically', 'clearly', 'obviously', 'builder', 'verifier', 'unit report', 'REQUESTS': no hits."),
    row("E1d-exemplar-a", "2.3 Exemplar A scores and annotations", f"{P} #exemplar-a",
        "PASS", "Official scores C1 1, C2 2, C3 2, C4 2, C5 1, C6 2; the annotations name the missing elements (no cost, no unit, one closed form derived, no signs, no recommendation, one limit). Consistent with the rubric text."),
    row("E1d-exemplar-b-C2", "2.3 Exemplar B derivations (C2 = 4)", f"{P} #exemplar-b Derivations",
        "PASS", "Monopoly FOC, reaction function, symmetric d/3, the q1 = 0 case analysis (q2 = 50, q1 = 25) and the difference argument are all shown; level 4 criteria met."),
    row("E1d-exemplar-b-C3-C4", "2.3 Exemplar B welfare and comparison (C3 = 4, C4 = 4)", f"{P} #exemplar-b Welfare; Comparison",
        "PASS", "C3: exact before rounding; the DWL on the exact volume; the tie named (71, 51). C4: printed differences with signs; exact profit difference d^2/(36b) = 277.8 cents, positive."),
    row("E1d-exemplar-b-C5", "2.3 Exemplar B recommendation (C5 = 3)", f"{P} #exemplar-b Recommendation",
        "PASS", "Names Bertrand, justifies from printed welfare 5000 and fee 20, names one condition (exchange profit alone: monopoly 2500 vs Bertrand 0). No direction for c or b is stated, so level 4 is missed as the official scoring says."),
    row("E1d-exemplar-b-C6", "2.3 Exemplar B limits (C6 = 2)", f"{P} #exemplar-b Limits",
        "PASS", "The changed Limits text names three limits; constant cost gives the direction (derivatives c/2, 2/3, 1 in c, recomputed); linear demand and two exchanges give no outcome that changes without them; the official score 2 is consistent with the level descriptors."),
    row("E1d-citations", "2.1 citations: verify_refs live and offline; the one key", "references/references.json (varian2014intermediate); tools/verify_refs.py",
        "PASS", f"{S}/refs_live.txt: 'live re-verification of E1: 1 of 560 entries, 0 problems'; {S}/refs_off.txt: 'offline integrity: 560 entries, 0 problems'. The page cites only varian2014intermediate."),
    row("E1d-citations-intext", "2.1 in-text attribution", f"{P} #reading",
        "PASS", "Reading paragraph attributes nothing to the source: 'The propositions above are proved on this page ... The source below is the only reference this page cites. No passage locator from it has been confirmed'. No locator is typed."),
    row("E1d-hours", "2.9 hours arithmetic (hub split vs lessons and project)", f"{P} Time budget; course/modules/E/E1/index.html",
        "PASS", "index.html: data-hours-lessons 90, data-hours-project 30 (sum 120). Nine lessons at 10 h each = 90. Project time budget rows 2 + 3 + 8 + 8 + 6 + 3 = 30. Pace not judged (architect ruling)."),
    row("E1d-dag", "DAG: concepts used by the project inside the unit's closure", f"{P}; cards.json; L01-L09",
        "PASS", "check_dag E1: PASS. The project page has no concept links. Its names (surplus, Cournot, Bertrand, reaction function) are defined on L06 and L07 or in the page itself; 'Nash' does not appear (architect Q2)."),
    row("E1d-forward-refs", "2.5 terms used before definition (labs before Definitions)", f"{P} lines 55-259 vs Definitions (line 264)",
        "PASS", "The labs (Rungs 1 and 2, Lab 3) use the structure names, 'rival' and 'consumer surplus' before the Definitions block, but the intro (line 13) names all three structures in words and each lab's docstring defines the quantity it computes."),
    row("E1d-time-limit", "2.9 the 120 s limit stated on the page matches the runtime", f"{P} Constraints; course/assets/js/python.js",
        "PASS", "python.js: 'const TIMEOUT_MS = 120000;' and the resolve message 'Stopped after 120 s'. The page says 'A run in your browser stops after 120 seconds.'"),
    row("E1d-definitions", "2.4 model definitions and formulas", f"{P} #model-definitions",
        "PASS", "f(Q) = (a - Q)/b; monopoly profit (f - c)Q; Cournot profit (f(Q) - c)q_i; Bertrand demand rule; CS = int (f(t) - f(Q)) dt = Q^2/(2b); welfare = gross value less cost; DWL = W(d) - W(Q). Units now consistent: b is in trades per (cent per trade), so b*c is in trades and f(Q) in cents per trade (dimension check)."),
    row("E1d-units", "2.9 units of b across the page, the labs, the grader and the rubric",
        f"{P} Model, Inputs, Conventions, rubric C1; tests/labs/E1/lab-E1-project-1.py and -2.py; grader/instance.py; grader/reference.py; grader/starter.py",
        "PASS", "Round-4 FAIL closed: every occurrence reads 'trades per (cent per trade)'; a grep of the E1 module, the twins and the grader finds no residual 'trades per cent' for b (the remaining 'per cent' are percentages in L08 and L09 prose)."),
    row("E1d-cards-structure", "2.7 card structure, ids, duplicates, grades", C,
        "PASS", "133 cards, ids E1-c001..E1-c133 sequential; grades T 94, C 14, ungraded 25 (definitions); every C card has a basis; no duplicate ids, fronts or backs."),
    row("E1d-cards-numbers-refs", "2.7 locators and numbers cited by cards exist in their lesson", f"{C} vs L01-L09",
        "PASS", "Every 'Proposition', 'Lemma', 'Theorem', 'Corollary', 'Remark', 'Example', 'Misconception', 'Problem', 'Lab 1 Part' locator in a card was matched to its lesson text (e.g. c121 'Proposition 1.3, and problem set item P1' with P1 at L09 line 197; c060 'Problem R2' at L05; c037 'Problem P2' at L03)."),
    row("E1d-cards-recompute", "2.7 card numbers recomputed", f"{C}; tests/labs/E1/lab-E1-L0x-1.py run this round",
        "PASS", "Recomputed: c046 (sqrt(121) - 1 = 10, dp/da = 1/22); c047/c053 (p'' = -1/5324, p''' = 3/1288408, forward error -h/10648, central h^2/2576816); c078 (10000/9 -> 1111); c088 (20000/9 = 2222.22); c100 (5000/9 -> 556); c101 (DWL_M/W_B = 1/4, DWL_C/W_B = 1/9); c118 (108/35 > 3, 76/5 > 15); c129/c132 (vertical sum 400 at g = 6; S(6) = 2700, S(7) = 2650); c130 ((b/2)(70 - 68)^2 = 20); c131 (e^2/(2b) = 720). All agree with the lab output."),
    row("E1d-cards-changed", "2.7 cards whose lesson text changed this round", f"{C} c007, c008, c010, c013, c097-c103, c109, c112, c124; L01, L07, L08, L09",
        "PASS", "Each changed card was checked against the current lesson statement: c007 (x_bar, Example 1.6 line 53); c008 (Remark 1.7 line 55, ln u with positive maximum); c010 (Proposition 2.3 with 'tangency' in its title); c013 (Remark 2.4 and Misconception 3); c097-c099 and c103 (cite 'Lesson 6, Definition 1.1' explicitly, matching L07 Corollary 2.1); c109 and c112 (L08 Lemma 2.1 and Theorem 2.4 with X, Y > 0); c124 (L09 Proposition 1.6 hypotheses a > 0, b > 0, e >= 0, c + e < a)."),
    row("E1d-cards-lab-grade", "2.7 lab-based cards are graded C and name their lab", C,
        "PASS", "The 14 C cards (c014, c025, c027, c036, c051, c066, c084, c085, c105, c115, c129, c131, c132, c133) each carry a basis naming its lab part. T cards state a theorem or formula proved on the page."),
    row("E1d-cards-basis", "2.7 T cards: basis is a locator in the lesson", C,
        "PASS", "Each T card's basis names a locator found in its lesson (e.g. c048 'Proposition 3.1 and Misconception 3', c056 'Proposition 5.2'). Hypothesis content of the bases is in the two hypothesis rows below."),
    row("E1d-cards-c048-basis", "2.7 round-3 defect: lab numbers on a T card", f"{C} E1-c048",
        "PASS", "c048 now states an order-of-error result (Proposition 3.1) with no lab number; the round-3 defect is removed."),
    row("E1d-cards-duplicates", "2.7 full duplicate scan", C,
        "PASS", "No duplicate ids, fronts or backs (python scan over 133 cards). c019 and c025 are different questions."),
    row("E1d-cards-locators", "2.7 locators changed in round 4", f"{C} E1-c121; course/modules/E/E1/L09.html problem set",
        "PASS", "c121 reads 'Proposition 1.3, and problem set item P1'; L09 contains 'P1 · The overproduction gap' (line 197 of the extracted text)."),
    row("E1d-cards-hyp-c039", "2.7 T card drops a hypothesis the current lesson states", f"{C} E1-c039 (L04 Remark 1.2)",
        "FAIL", "E1-c039 is graded T and states epsilon(p) = d(ln Q)/d(ln p) with no hypothesis. The current L04 Remark 1.2 reads 'Assuming Assumption 1, and under the hypotheses of Definition 1.1, epsilon(p) = d(ln Q)/d(ln p)', and the Assumption 1 derivative of ln is stated and not proved on the page.",
        "Prefix the back of E1-c039 with 'Under Assumption 1 (the derivative of ln x is 1/x), and under the hypotheses of Definition 1.1,'. Keep grade T and the rest of the back."),
    row("E1d-cards-hyp-c093-c096", "2.7 cards cite hypotheses under a reference that has none", f"{C} E1-c093, E1-c095, E1-c096 (L07 Theorem 1.2, Lemma 1.4, Theorem 1.5)",
        "FAIL", "The three cards write 'Under the hypotheses of Definition 1.1'. In L07, Definition 1.1 is the consumer and producer surplus definition and states no hypotheses; the hypotheses (b > 0, c > 0, a > bc) are those of Lesson 6, Definition 1.1, which L07 Theorem 1.2, Lemma 1.4 and Theorem 1.5 cite explicitly ('Assume the hypotheses of Lesson 6, Definition 1.1'). The fixed cards c097-c103 already use the full reference.",
        "Replace 'the hypotheses of Definition 1.1' with 'the hypotheses of Lesson 6, Definition 1.1 (b > 0, c > 0, a > bc)' in the backs of E1-c093, E1-c095 and E1-c096."),
    row("E1d-cards-market-c067", "2.7 definition card matches the current Definition 1.1 wording (L06)", f"{C} E1-c067 (L06 Definition 1.1)",
        "FAIL", "E1-c067 states 'Two exchanges, each charging a fee per unit, face trade demand Q(f) = max(0, a - bf)'. L06 Definition 1.1 is 'the market': real numbers a, b, c with b > 0, c > 0, a > bc, the trade demand Q(f) = max(0, a - bf) and the inverse demand f(Q) = (a - Q)/b. It does not mention two exchanges; L06 Section 1 says the lesson covers one monopoly and two exchanges in two forms, all facing this demand.",
        "Rewrite the back of E1-c067 to the definition's own wording: 'Trade demand Q(f) = max(0, a - bf) for real a, b, c with b > 0, c > 0, a > bc; d = a - bc > 0; inverse demand f(Q) = (a - Q)/b (Definition 1.1). One exchange (monopoly) or two (Cournot, Bertrand) face it.'"),
    row("E1d-cards-qualitative", "2.7 card-by-card comparison with the current lesson text (all 133 cards)", f"{C} vs L01-L09 (current)",
        "FAIL", "Completed this round for all 133 cards (round 4 left this UNVERIFIABLE). Every card was read against its lesson's current statement and every number was recomputed or matched to a lab output. Three defects, recorded as their own rows: E1d-cards-hyp-c039 (hypothesis dropped), E1d-cards-hyp-c093-c096 (hypotheses cited under the wrong definition), E1d-cards-market-c067 (definition card adds 'two exchanges').",
        "Apply the three fixes in the rows named above; re-run the card scan and the lesson-text comparison of the three cards."),
    row("E1d-lessons-changed-cards", "2.7 changed lesson statements vs cards citing them", "course/modules/E/E1/L01.html ... L09.html (changed statements)",
        "PASS", "The changed statements (L01 Remark 1.7, Proposition 1.4 x-bar, Proposition 2.3 wording; L02 Proposition 1.5 and Remark 1.6; L04 Remark 1.2 (assumption), Assumption 1 and Remark 3.3; L05 Misconception 3 and Lab 1 text; L06 Lemma 1.3, Remark 3.4 and Definition 3.1; L07 Corollary 2.1 and Proposition 2.3; L08 Lemma 2.1 and Example 2.5; L09 Proposition 1.4 and 1.6) were compared with the cards that cite them. The one card that disagrees is E1d-cards-hyp-c039, recorded above."),
    row("E1d-starter", "2.4 starter.py fails the suite (no implementation)", "grader/starter.py; grader/test_project.py",
        "PASS", f"{S}/starter_run.txt: '112 failed, 6 passed'. The page states no count for the starter, so nothing is claimed about it."),
    row("E1d-citations-note", "2.1 references section lists the one key only", f"{P} #reading, #references",
        "PASS", "The references section is generated from data-cite; no page or table locator is typed for varian2014intermediate."),
]

mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+)\.py: (.*?) -> (.*)$")
for line in (ROOT / S / "mutate_E1_seeds0-9_r5.txt").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if m:
        mutants.append({"id": m.group(2), "description": m.group(3), "result": m.group(1), "killed_by": m.group(4)})

frag = {
    "unit": "E1",
    "slice": "E1-d",
    "round": 5,
    "verifier": "independent verifier (Haiku 5.5), round 5 for slice E1-d (project.html, grader, project labs, cards.json, project mutants)",
    "pin": PIN,
    "base": "round-4 pin 2657ab5 (previous fragment /tmp/fanout-frags/B-E1-d.round4.json); the delta touched project.html (units of b, Limits), grader/instance.py, reference.py, starter.py (docstrings), cards.json (c007-c013, c097-c103, c109, c112, c124), the project lab twins and L01-L09 text",
    "checkout": "/tmp/verifyB5-E1-d",
    "scratch": "/tmp/e1d-v/r5",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": ("Round 5. Re-verified this round: the units fix (E1d-units) and the scope fix (E1d-scope-words) are closed. "
              "Completed the card-by-card comparison that round 4 left open. Three card defects found: a T card drops Assumption 1 (c039), "
              "three T cards cite the hypotheses of an unnumbered Definition 1.1 in L07 (c093, c095, c096), and a definition card (c067) adds 'two exchanges'. "
              "Four new student-error mutants written (v5_m01..v5_m04), all KILLED; 77/77 mutants killed on seeds 0-9. Ten alternative implementations PASS on seeds 0-49. "
              "Not run: the repository-wide gate (render_curriculum, build_site --check, fetch_data --check, full pytest, run_graders for other units) is the architect's and was not run by this verifier; "
              "Lessons L01-L09 text belongs to other slices and was read only for the cards that cite it."),
    "summary": None,
}
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
frag["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": n_fail,
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    "mutants": len(mutants),
    "mutants_killed": sum(1 for m in mutants if m["result"] == "KILLED"),
    "fail_ids": [r["id"] for r in rows if r["status"] == "FAIL"],
    "unverifiable_ids": [],
}
out = ROOT / "ledgers/E1/E1-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants), "fail", n_fail)
