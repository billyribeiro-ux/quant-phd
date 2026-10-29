"""Write the round-3 CS2-c fragment (rows, verdict fields) to ledgers/CS2/CS2-c.json."""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/CS2/scripts/CS2-c-r3/"
rows = []

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("CS2-c-cmd-check-pages", "tools/check_pages.py --unit CS2", "course/modules/CS/CS2/L09-L11.html, cards.json", "PASS",
    "Run at pin aa3c26c: output 'check_pages CS2: PASS' (rc 0).")
row("CS2-c-cmd-check-dag", "tools/check_dag.py --unit CS2", "curriculum/curriculum.json CS2 entry", "PASS",
    "Run at pin: 'check_dag CS2: PASS'. CS2 prereqs are ['CS1', 'M1'] (architect decision applied).")
row("CS2-c-cmd-run-labs", "tools/run_labs.py --unit CS2", "tests/labs/CS2/lab-CS2-L09-1.py, L10-1.py, L11-1.py", "PASS",
    "Run at pin: 'run_labs CS2: PASS (14/14)'.")
row("CS2-c-cmd-page-smoke", "tools/page_smoke.py --unit CS2 --pages L09 L10 L11 --skip-sweep", "L09.html, L10.html, L11.html", "PASS",
    "Run at pin: 'page_smoke modules/CS/CS2/L09.html: PASS', L10 PASS, L11 PASS, 'page_smoke CS2: PASS' (lab 0.0-0.1 s). Light/dark sweep not run (--skip-sweep).")
row("CS2-c-cmd-verify-refs", "tools/verify_refs.py --offline; tools/verify_refs.py --unit CS2", "references/references.json", "PASS",
    "'offline integrity: 560 entries, 0 problems'; 'live re-verification of CS2: 1 of 560 entries, 0 problems'. The slice pages carry no data-cite.")
row("CS2-c-lab-twin-identity", "Each data-run block equals its twin; twin output equals the expected block",
    "L09.html, L10.html, L11.html (data-run and pre.expected); tests/labs/CS2/lab-CS2-L09-1.py, L10-1.py, L11-1.py", "PASS",
    S + "twin_identity.py: embedded==twin True for L09, L10, L11; expected==run output (python -I -W error) True for all three.")
row("CS2-c-L09-lab-numbers", "Lab 1 expected block recomputed from unrounded values", "L09.html Lab 1 expected block", "PASS",
    S + "l09_numbers.py: rel W 9.2581e-16, 2P 2.8195e-17, N 7.2859e-15 (offset 0); 8.8517e-11, 4.3574e-17, 1.4185e-2 (1e6); 7.4493e-8, 1.2694e-14, 1.0000 (1e9); exact 0.087281 at all offsets; naive estimate at 1e9 is 0.0.")
row("CS2-c-L09-sigdigits", "Printed precision matches the hypothesis wording", "L09.html line 121 hypothesis; twin format", "PASS",
    "The hypothesis now says 'printed in scientific notation with three digits after the decimal point'; the twin uses f'{...:.3e}' (tests/labs/CS2/lab-CS2-L09-1.py docstring and print) and the expected block shows 9.258e-16 etc. Consistent (round-2 FAIL resolved).")
row("CS2-c-L09-prose-numbers", "Prose numbers in L09 recomputed", "L09.html Lab 1 interpretation; Section 3; Misconceptions 1-2; Problem E1, E2",
    "PASS", S + "l09_numbers.py: sum x^2 = 2.000e21 at 1e9; ulp 2^18 = 262144 (frexp: 2e21 in [2^70, 2^71)); (n-1)s^2 = 174.4749 ('about 174.5'); E2 absolute error 0.0872811 x 9.2581e-16 = 8.08e-17 ('8.1e-17'); ratios 7.870, 1.6019e8, 1.3425e7 ('about 8', '1.6e8', '1.3e7'). " + S + "l09_rounding_scope.py: the rounding error of the computed sum of squares at 1e9 is 3.2e6, far above 174.5 (claim 'larger than the quantity' holds).")
row("CS2-c-L09-theorems", "Lemma 1.3, Theorems 2.1 and 2.2, Corollary 2.3 re-derived", "L09.html sections 1-2", "PASS",
    "Re-derived by hand: mean step nM_n = (n-1)M_{n-1} + x_n; sum-of-squares difference x_n^2 - nM_n^2 + (n-1)M_{n-1}^2 = d^2(n-1)/n; induction base n=1 and step; six operations counted. Hypotheses (1)-(4) of Theorem 2.1 and (1)-(3) of Theorem 2.2 match the proofs.")
row("CS2-c-L09-R1-deferred", "Research R1 weighted update solution", "L09.html R1 solution", "PASS",
    "Re-derived: T_n - T_{n-1} = w_n W_{n-1} d^2/W_n; example x=(1,2), w=(1,3): M_2 = 1.75, S_2 = 0.75 = 0.5625 + 0.1875.")
row("CS2-c-L09-far-more", "Misconception 2 factors", "L09.html Misconception 2; card CS2-c126", "PASS",
    "Unrounded factors: 7.870 (offset 0), 1.6019e8 (1e6), 1.3425e7 (1e9); stated as about 8, 1.6e8, 1.3e7 with the quotients shown.")
row("CS2-c-L09-quiz", "Quiz answer keys and numeric answers (L09q1-L09q9)", "L09.html section 7", "FAIL",
    "Answers verified: 4.5714 (32/7), 2 (S_3), 6 (Cor 2.3), 0.25 (S_4 = 1), option keys match Definition 1.2, Theorem 2.2 and Section 3. The L09q9 explanation is a non-sequitur (see CS2-c-L09-zero-estimate), so the item fails.",
    "Rewrite the L09q9 explanation as in CS2-c-L09-zero-estimate.")
row("CS2-c-L09-problems", "Problem set M1-M3, P1-P3, E1-E3, R1-R3", "L09.html section 5", "PASS",
    "M1: sum 40, S_8 = 32, 32/7 and 4. M2: M_3 = 2, S_3 = 2. M3: S_4 = 1, 1/4 = p(1-p). P1, P2, P3 algebra re-derived (P3: cross term 0; ab Delta^2/(a+b)). E2 absolute 8.08e-17. R3: 0.24 = 2.4/10.")
row("CS2-c-L09-hypothesis-scope", "Lab 1 hypothesis and interpretation claims", "L09.html Lab 1 hypothesis and interpretation", "PASS",
    "Two-pass is smallest at each offset: 2.8e-17 < 9.3e-16; 4.4e-17 < 8.9e-11; 1.27e-14 < 7.45e-8. Naive above Welford at each offset. 'at offset 0 each relative error below 1e-14': 9.3e-16, 2.8e-17, 7.3e-15 all below. Interpretation's 'one stream, one seed' is accurate (lab seeds once).")
row("CS2-c-L09-zero-estimate", "Claim that Lab 1 returns an estimate of exactly 0.0 at offset 1e9, and that its printed output shows this",
    "L09.html line 232 (Misconception 1), line 303-305 (E1), line 363 (key-results row), line 436 (quiz L09q9 explanation); cards CS2-c124, CS2-c125",
    "FAIL",
    "Lab 1 prints only relative errors (expected block: naive 1.000e+00 at offset 1e9). Its code never prints the estimate. Running " + S + "l09_numbers.py shows naive_variance(stream(1e9)) == 0.0 exactly, so the claim is true of the code. But |est - exact|/exact = 1 also holds when est = 2 x exact, so the printed 1.000e+00 does not show that the estimate is zero. The quiz explanation says the output 'shows ... which means the estimate is zero'; the key-results row and card CS2-c124 cite 'Lab 1 ... offset 1e9 lines' as the basis.",
    "Either make the twin print the naive estimate at offset 1e9 (then regenerate the expected block with tools/embed_labs.py --refresh L09) and keep the zero claim, or reword the five places to say the lab's code returns 0.0 and the printed relative error 1.000e+00 is consistent with it.")
row("CS2-c-L09-R2-claim", "R2 solution: the identity does not bound floating-point error", "L09.html R2 solution", "PASS",
    "Reasoned remark, no theorem claimed; it names the rounding model it would need. Theorem 2.2 is described as not supplying a bound, which matches its hypotheses.")
row("CS2-c-L10-lab-numbers", "Lab 1 expected block recomputed", "L10.html Lab 1 expected block and interpretation",
    "PASS", S + "l10_counts.py: lab series operations min/max: w1 399/399, w2 398/399, w5 398/398, w13 397/398, w30 396/397; step-(1) value comparisons <= 2n in 20000 random trials; expected block equals the twin run (twin_identity.py).")
row("CS2-c-L10-theorems", "Theorems 2.2, 2.3, 2.4, Corollary 2.5 re-derived", "L10.html sections 1-2", "PASS",
    "Theorem 2.2 both inclusions re-derived (S_i = D_i; W_{i-1} membership for j >= i-w+1); Theorem 2.3 front = latest minimum index (f = p); Theorem 2.4 counts: <= n appends, <= n removals, one stop per insertion for step-(1) value comparisons (random check: max step-(1) comparisons - 2n = 0). Corollary 2.5(c) witness 1..w then a smaller value removes w entries. The key-results row overstating Theorem 2.4 is a separate FAIL.")
row("CS2-c-L10-key-comparisons", "Key-results row: 'n insertions cost at most 2n operations and at most 2n comparisons' (T, Theorem 2.4)",
    "L10.html line 354 (key-results table)", "FAIL",
    "Theorem 2.4 bounds value comparisons in step (1) loops only. Step (3) also compares indices (items[0][0] <= i - w). " + S + "l10_counts.py: series [0,1,2,3] with w=1 gives 7 operations (<= 8) but 3 step-(1) and 7 step-(3) comparisons, 10 > 2n = 8. Over 20000 random series all comparisons minus 2n reached 25. The unqualified 'comparisons' in a T row is not established.",
    "Change the row to 'at most 2n value comparisons in the step (1) loops' to match Theorem 2.4 and card CS2-c132, or prove and state a bound on all comparisons.")
row("CS2-c-L10-problems", "Problem set M1-M3, P1-P3, E1-E3, R1-R3", "L10.html section 5", "PASS",
    "M1 rolling minimum 3,1,1,1,1; M2 fronts 3,1,1,1,1 with trace; M3 total 8 <= 10; E1 2n-1 = 399 for w=1 (checked by " + S + "l10_counts.py); E2 witness 1..5,0 with w=5 removes 5 at i=5; E3 total 2n-1; R1 looser rule keeps the minimum; R2 example 4,1,4 with w=2 re-traced; R3 bound n-w attained by an increasing series.")
row("CS2-c-L10-usually", "Misconception 3 and Section 3 claims", "L10.html Misconception 1-3; Section 3", "PASS",
    "Front is the new index exactly when x_i is at most every value still in the window (Theorem 2.3: front = latest index attaining the window minimum). Largest single-push removals 5 for window 5 (lab output).")
row("CS2-c-L10-quiz", "Quiz answer keys and numeric answers (L10q1-L10q10)", "L10.html section 7", "PASS",
    "Answers: 1 (rolling minimum at 4 for 3,1,4,1,5 with w=3); 19 (2n-1, n=10); 400 (2n, n=200); 7 (n-w, n=10, w=3). Keys match Theorem 2.3, Definition 2.1 step (1) rule, Corollary 2.5(c), Theorem 2.4 (operations, not time).")
row("CS2-c-L11-theorems", "Lemma 2.3, Theorems 2.2, 2.4, 2.5 and Corollary 2.6 re-derived", "L11.html sections 1-2", "PASS",
    "Theorem 2.2(b): P_{h+1} = C_h k_h 2^h <= P_h <= n. Theorem 2.4: change 2^h(2 floor(c/2) - c) in {0, -2^h}; E <= eps n from k_h >= (h+1)(h+2)/eps and Lemma 2.3 (telescoping 1 - 1/(H+2)). Theorem 2.5 lower count: R^-(v) <= R-hat^-(v) + E <= qn + eps n. Corollary 2.6 proof checked.")
row("CS2-c-L11-lab-numbers", "Lab 1 expected block recomputed from an independent sketch", "L11.html Lab 1 expected block and interpretation",
    "PASS", S + "l11_recheck_recursive.py (recursive push as in Definition 2.1(2)): eps 1/20: caps 40,120,240; weight 5000; stored 500; compactions 151; max excess/N 0.021200; max deficit 0. eps 1/10: stored 220; compactions 305; max excess/N 0.044200; deficit 0. Note: a LIFO push order gave 0.0454 at eps 1/10; the definition specifies push in order, which is what the twin and the page use.")
row("CS2-c-L11-odd-docstring", "Twin docstring: even-numbered items, buffer[1::2]", "tests/labs/CS2/lab-CS2-L11-1.py docstring; L11.html Definition 2.1", "PASS",
    "buffer[1::2] keeps 0-based indices 1, 3, 5 = 2nd, 4th, 6th items (twin line 'kept = buffer[1::2]').")
row("CS2-c-L11-growth", "Cubic growth and Corollary 2.6 numeric bounds", "L11.html section 1, Corollary 2.6 proof, why-it-matters, Section 3 bullet 2, Misconception 1",
    "PASS", S + "l11_recheck_recursive.py and direct computation: L=12 bound (L+1)(L+2)(L+3)/(3 eps)+(L+1) = 18200+13 = 18213 >= 18187 (exact sum 20 x 910 - 13); L=29 (n=1e9): formula 198430, exact sum 198370; floor(log2 1e9)=29, floor(log2 5000)=12. Stated as an upper bound and O((log2 n)^3/eps).")
row("CS2-c-L11-not-optimal", "No optimality claim", "L11.html Section 3 bullet 2; quiz L11q8", "PASS",
    "grep 'optimal' in the slice: only the non-claims 'not claimed to be optimal' and 'does not claim the design is space-optimal'.")
row("CS2-c-L11-eps0", "eps = 0 extension is labelled", "L11.html Definition 1.2 note; Section 3 bullets 1 and 3; Misconception 2; P3",
    "PASS", "Definition 1.2 requires eps > 0; the note names the eps = 0 extension and its uses. Example R^-(450)=449 <= 550, R(450)=450 >= 450 with eps=1/20 re-checked.")
row("CS2-c-L11-R2", "R2 odd positions solution", "L11.html R2 solution", "PASS",
    "Re-derived: change 2^h(2 ceil(c/2) - c) in {0, +2^h}; 0 <= R-hat - R <= E; upper count R(v) >= W_j* - E >= qn - eps n; lower count R^-(v) <= R-hat^-(v) <= qn.")
row("CS2-c-L11-R3", "R3 memory bound", "L11.html R3 solution; quiz L11q9", "PASS",
    "Sum_{h=0}^{12} (20(h+1)(h+2) - 1) = 20 x 910 - 13 = 18187 (" + S + "l11_recheck_recursive.py prints 18187).")
row("CS2-c-L11-E2-counter", "E2 level bounds and total 151", "L11.html E2 solution",
    "PASS", "k_h = 40, 120, 240, 400, 600; floor(5000/(k_h 2^h)) = 125, 20, 5, 1, 0; sum 151; the per-level counts of the recheck run are 125, 20, 5, 1 (sum 151).")
row("CS2-c-L11-canon-450", "Section 3 example values 500, 501, 450", "L11.html Section 3 bullet 1; quiz L11q10",
    "PASS", "1..1000, q = 1/2: R^-(500)=499 <= 500, R(500)=500 >= 500; R^-(501)=500 <= 500, R(501)=501 >= 500 (eps = 0); R^-(450)=449 <= 550, R(450)=450 >= 450 (eps=1/20); 450 and 500 differ by 50 and both are accepted.")
row("CS2-c-L11-E1-M3", "M1 capacities, M3 forty values, E1 thirty-nine values", "L11.html section 5", "PASS",
    "M1: k0, k1, k2 = 20, 60, 120 for eps = 1/10. M2 query answer 5 (totals 1, 3, 7 against qn = 3.5). M3: 20 stored, weight 40. E1: 29 stored, weight 39, E = 1 <= 3.9.")
row("CS2-c-L11-R2-E", "R1 solution: constant capacity fails, level-dependent capacity gives eps n", "L11.html R1 solution",
    "PASS", "E/n <= (floor(log2 n)+1)/k grows with n for fixed k; level-dependent contributions n/k_h sum to at most eps n by Lemma 2.3.")
row("CS2-c-L11-quiz", "Quiz answer keys and numeric answers (L11q1-L11q10)", "L11.html section 7", "PASS",
    "Numeric: 20 (k0 for 1/10), 29 (E1 stored), 1 (E for E1), 18187 (R3). Keys match Definition 1.2, Definition 2.1 (weight 2^h), Lemma 2.3, Section 3 (no optimality claim). The L11q7 key ('rank of each value changes by at most one item's weight') matches the Theorem 2.4 proof.")
row("CS2-c-L11-cover-prose", "Interpretation: 'does not check every q', 'one run'", "L11.html Lab 1 interpretation; Section 3 bullet 2",
    "PASS", "The twin checks nine probes on one seeded stream (QuantileSketch, PROBES) and no other stream; the prose says so.")
row("CS2-c-L11-much-smaller", "Why-it-matters claim about memory", "L11.html line 52 (why-it-matters)", "PASS",
    "Round-2 FAIL resolved: the text no longer says 'much smaller than n' without a condition; it states the bound at n = 10^9 (198430, far below n) and at n = 5000 (18187, above n).")
row("CS2-c-keyresults-grade", "Key-results rows for lab results are graded", "L09.html line 363; L10.html line 355; L11.html line 404", "PASS",
    "Each lab-read row now carries grade C with basis 'Lab 1 (SIMULATED ..., one seed)'. Round-2 FAIL resolved. (The L10 comparisons row is a separate FAIL.)")
row("CS2-c-cards", "All 39 slice cards (CS2-c116 to CS2-c154) read against their lesson text", "course/modules/CS/CS2/cards.json",
    "FAIL", S + "cards_check.py (round 2) and a fresh read: 39 cards checked against L09, L10, L11. Cards that agree with the current text: all except CS2-c147 (hypotheses dropped) and the nine cards without a grade field. Round-2 card FAILs c148, c151 and the ungraded lab cards are fixed.",
    "See CS2-c-cards-c147 and CS2-c-cards-grade-field.")
row("CS2-c-cards-ungraded-lab", "Cards that state lab results carry a grade and a basis", "cards.json CS2-c124, CS2-c136, CS2-c150, CS2-c154, CS2-c138", "PASS",
    "Each has grade C and a basis naming Lab 1 (SIMULATED, one seed). The inference in CS2-c124 and CS2-c125 is recorded under CS2-c-L09-zero-estimate.")
row("CS2-c-cards-c151", "Card CS2-c151 (bound and growth)", "cards.json CS2-c151", "PASS",
    "Back states the proof's bound (L+1)(L+2)(L+3)/(3 eps)+(L+1) with L = floor(log2 n), 'a cubic in log2 n', 198430 at 1e9 and 18187 at 5000. Matches Corollary 2.6 and the proof; no order claim about the sum.")
row("CS2-c-cards-c148", "Card CS2-c148 hypotheses", "cards.json CS2-c148; L11.html Theorem 2.5", "PASS",
    "Back now lists n >= 1, eps in (0,1), the capacities of Definition 2.1 and the hypotheses of Theorem 2.2, which are those of Theorem 2.4 and so of Theorem 2.5.")
row("CS2-c-cards-c147", "Card CS2-c147 hypotheses (Theorem 2.4)", "cards.json CS2-c147; L11.html Theorem 2.4 'Hypotheses'", "FAIL",
    "The card says 'Also E <= epsilon n (Theorem 2.4, with n >= 1)'. Theorem 2.4's hypotheses are 'Those of Theorem 2.2, with n >= 1, and the capacities of Definition 2.1' (values added in order, exact arithmetic, capacities k_h). The card drops the capacities and the order and exactness hypotheses; E <= eps n depends on k_h >= (h+1)(h+2)/eps.",
    "Change the card's last sentence to: 'Assume the values are added in order, arithmetic is exact, the capacities are as in Definition 2.1, and n >= 1 (Theorem 2.4).'")
row("CS2-c-cards-grade-field", "Every card has the grade field the plan requires", "cards.json CS2-c116, c117, c118, c128, c129, c140, c141, c142, c143", "FAIL",
    "CS2-c-plan section 9 lists the fields as id, lesson, front, back, grade, and either cite or basis. These nine cards have no grade key (check_pages does not require it, so the gate passes). Each is a definition or a procedure, not a claim.",
    "Add a grade field to each (T for a definition or procedure, as the lesson's definitions are not lab results), or record in the plan that definition cards carry no grade.")
row("CS2-c-dag", "DAG: concepts used are in the unit's prerequisite closure or earlier in CS2", "L09.html, L10.html, L11.html concept links; curriculum CS2 entry",
    "PASS", "Links used: mathematical-induction (M1, now a CS2 prereq), big-O-complexity (L01, CS2), welford-algorithm, monotonic-deque, quantile-sketch (defined in the slice), comparison-sorting and binary-search (L04, CS2). Each dfn appears once. Variance and quantile appear as plain formulas or words (architect decision Q2).")
row("CS2-c-process-words", "No process words in learner text", "L09.html, L10.html, L11.html, cards.json slice cards", "PASS",
    "Case-insensitive grep for builder, verifier, round N, REQUEST, unit report, roughly, historically, typically, usually, generally, in practice: 0 hits in the pages and the slice cards.")
row("CS2-c-hours", "Hours: arithmetic between hub split and lesson hours", "L09 data-hours=10; L10=8; L11=7; index.html data-hours-lessons=100; project 30",
    "PASS", "8+9+10+10+9+9+10+10+10+8+7 = 100 = data-hours-lessons; project 30 = data-hours-project = curriculum 130 - 100. Pace not judged (architect ruling).")
row("CS2-c-attribution-M1L06", "Attribution: 'Theorem 1.2 of M1 Lesson 6' (induction principle)", "L09.html Theorem 2.2 proof; L10.html Theorem 2.2 proof",
    "PASS", "course/modules/M/M1/L06.html line 64: 'Theorem 1.2 (the induction principle)'. M1/L06.html is byte-identical since the previous pin (git diff --quiet clean). No bibliographic source is cited in the slice.")
row("CS2-c-mutants-na", "Mutation testing", "ledgers/CS2/mutants/ (project graders only)", "PASS",
    "Not applicable to lesson pages: architect ruling that lab twins are demonstrations and mutation testing applies to project graders only. No mutants written for this slice.")

rows_ids = [r["id"] for r in rows]
assert len(rows_ids) == len(set(rows_ids))
fails = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "CS2",
    "slice": "CS2-c",
    "round": 3,
    "verifier": "independent verifier (Haiku 5.5), CS2 slice c round 3; did not build CS2 and shares no context with its builders",
    "pin": "aa3c26c",
    "base": "none",
    "previous_pin": "1817191",
    "checkout": "/tmp/verifyB3-CS2-c (detached at aa3c26c, .venv symlink)",
    "scratch": "/tmp/cs2-v/c-r3",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since 1817191 for this slice: L09.html (11 lines), L10.html (6), L11.html (12), cards.json (40 lines; slice cards c123-c126, c136, c148-c151 changed, c124 and c136 newly graded; c155 added for L02, outside this slice), tests/labs/CS2/lab-CS2-L09-1.py (docstring only). Lab twins L10 and L11 unchanged.",
        "No carry-forward was used: every round-2 row was re-verified against the pin (the subjects were re-read in full). The round-2 FAIL rows CS2-c-L09-sigdigits, CS2-c-L11-much-smaller, CS2-c-keyresults-grade, CS2-c-cards-ungraded-lab, CS2-c-cards-c151 and CS2-c-cards-c148 are now PASS.",
        "Independent scripts: ledgers/CS2/scripts/CS2-c-r3/ (twin_identity.py, l09_numbers.py, l09_rounding_scope.py, l10_counts.py, l11_recheck.py, l11_recheck_recursive.py). The LIFO variant l11_recheck.py is kept for transparency; it differs from the defined push order and is not used as evidence.",
        "Not run: tools/fetch_data.py --check (no data in slice c), the light/dark sweep of page_smoke, the full pytest suite and repo-wide ruff/mypy (only the three twins were linted and type-checked: ruff check and format --check clean, mypy strict no issues), tools/run_graders (no project grader in slice c), rendered KaTeX in a browser.",
        "Not checked: no bibliographic sources are cited in the slice, so no live citation rows; rendered layout at 360 px beyond page_smoke.",
        "Hours were not judged on pace (architect ruling); only the hub-versus-lesson arithmetic was compared.",
        "Lab results read off the SIMULATED twins are C with a basis naming the lab (rule e). The one place the printed output is used for a claim it does not show is CS2-c-L09-zero-estimate.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": len(fails),
        "unverifiable": 0,
        "fail_ids": fails,
    },
}
out = ROOT / "ledgers/CS2/CS2-c.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fails", fails)
