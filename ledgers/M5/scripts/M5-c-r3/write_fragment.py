"""Writes the round-3 fragment for M5 slice c (L08-L10). Row content is the verifier's evidence; see the rows."""
import datetime
import json
import sys

out = sys.argv[1]
S = "tests/labs/M5"
P = "course/modules/M/M5"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- commands (re-run on aa3c26c)
row("M5c-cmd-check-pages", "2.9-structure", "tools/check_pages.py --unit M5",
    "PASS", "Re-run at aa3c26c: output 'check_pages M5: PASS', rc 0.")
row("M5c-cmd-check-dag", "DAG", "tools/check_dag.py --unit M5; tools/check_dag.py --all",
    "PASS", "Re-run: 'check_dag M5: PASS'; --all lists AC2, AC4, CF1, AP1 as PASS (all lines shown were PASS).")
row("M5c-cmd-run-labs", "2.5-labs", "tools/run_labs.py --unit M5",
    "PASS", "Re-run: 'run_labs M5: PASS (13/13)'. Twins also run alone: .venv/bin/python -I -W error tests/labs/M5/lab-M5-L08-1.py, L09-1, L10-1: rc 0 each; outputs in /tmp/M5-c-v3/L08.out, L09.out, L10.out.")
row("M5c-cmd-page-smoke", "2.5-labs", "tools/page_smoke.py --unit M5 --pages L08 L09 L10 --skip-sweep",
    "PASS", "Re-run: page_smoke L08, L09, L10 each PASS; lab runtimes 0.0 s; 'page_smoke M5: PASS'; rc 0 (output /tmp/M5-c-v3/smoke.out).")
row("M5c-cmd-lint-types", "gate", "ruff check, ruff format --check, mypy --no-incremental on tests/labs/M5/lab-M5-L08-1.py, lab-M5-L09-1.py, lab-M5-L10-1.py",
    "PASS", "'All checks passed!'; '3 files already formatted'; 'Success: no issues found in 3 source files'.")
row("M5c-cmd-verify-refs", "2.1-citations", "tools/verify_refs.py --unit M5 (live); tools/verify_refs.py --offline",
    "PASS", "Live: 'live re-verification of M5: 2 of 560 entries, 0 problems'. Offline: 'offline integrity: 560 entries, 0 problems'. The slice cites no registry key: L08 references section 'This page cites no source'; L09 and L10 references sections say the same.")
row("M5c-cmd-mutate-graders", "2.6-projects (informational)", "tools/mutate_graders.py --unit M5",
    "PASS", "'mutate_graders M5: PASS (47/47 killed)'. Project grader only; this slice has no grader (ruling: lab twins are not mutation-tested).")
row("M5c-hours-arithmetic", "hours", "course/modules/M/M5/index.html line 29 (data-hours-lessons=104, data-hours-project=26); L08.html, L09.html, L10.html line 2 (data-hours=11); hub card kickers",
    "PASS", "Hub card kickers: L01-L06 '10 h' (6 x 10 = 60), L07-L10 '11 h' (4 x 11 = 44), total 104; 104 + 26 = 130 = curriculum hours. Arithmetic only (ruling: hours are design targets).")
row("M5c-L08-numbers", "2.2-numbers", f"{P}/L08.html Example 1.2, Example 2.3, M2, M3, E2, Misconception 2, E1 solution, Lab 1 interpretation, quiz",
    "PASS", "Ran /tmp/verifyB3-M5-c/ledgers/M5/scripts/M5-c-r3/recheck_L08_L10.py: BETA 0.5 -> 40 iterations, 0.9 -> 257, 0.95 -> 527 (Misconception 2 and E1 match); Part B worst ratio unrounded 0.9000000000000006 = 0.9 + 5.55e-16 (5.0 ulp, text says 5.6e-16 and 'about five units', matches); E2 sqrt(0.457107) = 0.676097, 0.9*5 + 0.676097 = 5.176097; Example 2.3 and M2 arithmetic checked by hand (0.5/0.05 = 10; 0.5/0.1 = 5). Lab output (/tmp/M5-c-v3/L08.out) matches the embedded pre block line for line.")
row("M5c-L09-numbers", "2.2-numbers", f"{P}/L09.html Lab 1 interpretation, Misconceptions 1-3, E1-E3, R2, M1-M3, quiz",
    "PASS", "recheck_L08_L10.py: naive ratio of printed values 0.0000085808/0.0000009534 = 9.000210 (text 9.0002); unrounded actual/step 8.999999; R2 bound 0.9^151/0.1 * sqrt(3)/2 = 1.066963e-6 (n=151), 9.602671e-7 (n=152), so least n = 152, matches; sqrt(3)/2 = 0.8660254037844386 equals the lab's V1-V0 norm; 0.9^10/0.1 = 3.4867844010 (quiz tolerance 1e-6 accepts 3.486784); M3 1/9000 = 1.111111e-4; M2 4 x 0.016 = 0.064. Lab output (/tmp/M5-c-v3/L09.out) matches the embedded block.")
row("M5c-L10-numbers", "2.2-numbers", f"{P}/L10.html Example 3.3, E1-E3, Lab 1 interpretation, Misconceptions 1-2, M1-M2, quiz",
    "PASS", "Example 3.3 closed forms re-derived: right (n+1)(4n-1)/(6n^2), left (4n^2-3n-1)/(6n^2), errors (3n-1)/(6n^2) and -(3n+1)/(6n^2); E1 29/600, -31/600, gap 1/300 (exact 0.003333333333; printed-digit gap 0.003333333334); Part D 1/(2n) = 0.0005; M1 15/16; M2 16/3; quiz 3/4. Quiz value (1001)(3999)/(6e6) = 0.6671665, a tie at the 6th decimal rounded half-up to 0.667167 (within the 1e-6 tolerance). P2 check over 20000 random tagged partitions: max |S-2/3|/mesh = 0.622876 <= 1. Lab output (/tmp/M5-c-v3/L10.out) matches the embedded block.")
row("M5c-L08-proofs", "2.4-mathematics", f"{P}/L08.html Proposition 1.3, Theorem 2.2(a)-(c), Proof of (a), Proof of (b) and (c), P1-P3, R1-R3, Remark on well-definedness, canon-breaks 1-3",
    "PASS", "Re-derived: Proof of (a) inequality chain (choice of a, b and the exchange); (b),(c) via L07 Theorem 2.1 whose hypotheses (complete metric, contraction) match and whose Step 1 uses beta^n -> 0 (L07.html line 122); P1 monotonicity; P2 closed form; P3 V_{n+1} = u(1-beta^{n+1})/(1-beta) by algebra; R1 Lipschitz bound via |max f - max g| <= max|f-g|; R2 non-expansiveness argument at beta=1; R3 k^(alpha-1) >= 1 for k in (0,1]; (2,3) grid has F(2) empty since sqrt(2) < 2.")
row("M5c-L09-proofs", "2.4-mathematics", f"{P}/L09.html Lemma 1.1, Lemma 1.2, Theorem 1.3, Lemma 2.3(a)-(c), Theorem 2.4, P1-P3, R1-R3, canon-breaks 1-3",
    "PASS", "Re-derived each lemma and the Theorem 2.4 chain cert_n <= beta^n/(1-beta) ||V1-V0||; Lemma 2.3(c) from (a),(b); R3 example T(x)=beta x+1 gives |V1-x*| = beta/(1-beta) with V1 = 1; canon item 1 (T(x)=x/2 on (0,1], iterates 2^-n x0 -> 0 not in X) and item 2 checked by hand.")
row("M5c-L10-proofs", "2.4-mathematics", f"{P}/L10.html Lemma 1.3, Lemma 2.1, Lemma 2.2, Lemma 2.4(a)-(c), Theorem 3.1, Corollary 3.2, Example 3.3, Propositions 4.1 and 4.2, P1-P3, R1-R3",
    "PASS", "Re-derived: Lemma 2.1 (i) and (ii) by subsequence arguments; Lemma 2.2 via P1 and U-L <= eps(b-a); Lemma 2.4 (a) inf/sup comparison, (b) constants, (c) refinement and additivity; Theorem 3.1 bound (b-a)M eta = eps M(b-a)/(M(b-a)+1) < eps; Prop 4.1 with even n (k = n/2) gives sums 0 and 1 with distances summing to >= 1; Prop 4.2 |S-1/2| <= |P|. P1-P3 hypotheses match the M2 pages (see M5c-prereq-citations).")
row("M5c-prereq-citations", "2.1-citations (internal cross-references)", f"{P}/L08.html Theorem 2.2(b),(c); {P}/L09.html Lemma 1.2, Lemma 2.3; {P}/L10.html P1-P3, Lemma 2.4, Corollary 3.2",
    "PASS", "Read targets: M2 L09 Lemma 1.1 (refinement, line 65), Lemma 1.2 (L <= U, line 75), Definition 1.3 (line 85), Example 3.2 (int x^2 = 1/3, lines 136-137); M2 L10 Theorem 2.1 (fundamental theorem, line 74: F continuous on [a,b], differentiable on (a,b), f = F' integrable); M2 L11 Lemma 1.1 (linearity, line 57-59) and Example 3.2 (int_0^2 x^2 = 8/3, line 241); M5 L02 Theorem 2.5 (Cauchy criterion, line 125); M5 L06 Proposition 1.3 (Bolzano-Weierstrass, line 74); M5 L07 Theorem 2.1 (Banach, line 89). Hypotheses cited match each target.")
row("M5c-lab-prose-L08", "2.5-labs", f"{P}/L08.html Lab 1 hypothesis (line 138), interpretation (line 271), printed block",
    "PASS", "Hypothesis tolerances (1e-12 ratio and iterate checks; 1e-9 residual) match the code docstring and checks (lab-M5-L08-1.py). Printed lines match the run. 'never exceeds would be false at float level' confirmed by the unrounded 0.9 + 5.55e-16. 'The lab does not print this value' confirmed (the printed Part B line shows 0.900000 only).")
row("M5c-lab-prose-L09", "2.5-labs", f"{P}/L09.html Lab 1 hypothesis and interpretation, printed block",
    "PASS", "bound_holds True x4 and cert_within_tol True x3 in the run; step_spread 0.000e+00 at all three tolerances (exact zero); counts 59/103/147; reference 278 iterations, certified 9.512e-13; naive 126 steps. The code docstring matches the hypothesis (checks add SLACK 1e-12 for the reference error).")
row("M5c-lab-prose-L10", "2.5-labs", f"{P}/L10.html Lab 1 hypothesis, interpretation, printed block",
    "PASS", "Part A flags True (4 rows); Part B 200 partitions, largest_error_over_mesh 0.491631, all_within_2_mesh True; Part C jumps 1, sums 0 and 1 at n = 10 and 100 (the hypothesis's 'at each mesh that contains 1/2' is a stated expectation covered by Proposition 4.1, not a claim the two-row print proves; the interpretation's 'do not approach one value' rests on Proposition 4.1); Part D 0.5005 and 0.4995. No overreach beyond the printed output.")
row("M5c-cards-duplicates", "2.7-cards", f"{P}/cards.json (187 cards)",
    "PASS", "Python scan: 187 cards, no duplicate ids, no duplicate fronts. The 67 cards of L08-L10 read in full (listing /tmp/M5-c-v3/cards_L08_10.txt).")
row("M5c-hub-L08-L09", "2.9-structure", f"{P}/index.html lines 140-141 (L08 and L09 card bodies)",
    "PASS", "git diff 1817191 aa3c26c touches index.html only at line 142 (the L10 card), so lines 140-141 are byte-identical to the previous pin; their text matches the current L08 and L09 pages (operator defined by formula; certified stop to the grid fixed point).")
row("M5c-banned-process-words", "2.9-structure", f"{P}/L08.html, L09.html, L10.html (text with tags stripped)",
    "PASS", "Scan for TODO, TBD, lorem, for brevity, beyond the scope, it is important to note, studies show, it is well known, obviously, clearly, roughly, historically, and process words build, builder, round, verifier, REQUEST: no hits in learner prose. 'about nine' and 'about five units' are approximations each shown by a calculation on the same page.")
row("M5c-hours-consistency-L08-L10", "hours", f"{P}/L08.html, L09.html, L10.html data-hours; index.html line 29",
    "PASS", "L08, L09, L10 each declare 11 h; hub split 104 + 26 = 130 matches (see M5c-hours-arithmetic).")
row("M5c-L08-scope-only", "2.4-scope-words", f"{P}/L08.html line 69 (Definition 1.1 closing sentence), line 52 (why-it-matters), misconception 1 text",
    "FAIL", "Definition 1.1 closing sentence reads 'It uses only the grid, the feasible sets and beta.' The displayed formula on the same block uses the utility sqrt(.) and the output k^alpha in sqrt(k^alpha - k'), so the operator depends on u and alpha as well. The 'only' claim is contradicted by the formula the page prints.",
    fix="Replace the sentence with 'It uses the grid, the feasible sets F(k), the utility sqrt(.) and the discount factor beta, and no other object of the continuous model.'")
row("M5c-L08-lab-tolerance-claim", "2.5-labs", "tests/labs/M5/lab-M5-L08-1.py docstring lines 1-11 vs code (solve gap test, part_b worst > BETA + TOL, part_c iterate check > TOL, residual 1e-9)",
    "PASS", "Docstring says TOL = 1e-12 bounds the stopping gap, the Part B ratio check and the Part C iterate checks, and 1e-9 for residual and one-point check; code matches (checked in source).")
row("M5c-L08-never-exceeds", "2.2-numbers and claims vs output", f"{P}/L08.html Lab 1 hypothesis and interpretation",
    "PASS", "Claim 'the sampled check does not prove the contraction' is consistent with Theorem 2.2(a); the 'never exceeds would be false at float level' counterfactual is confirmed by the recomputed unrounded worst ratio 0.9 + 5.55e-16.")
row("M5c-L08-R2-proof-gap", "2.4-mathematics", f"{P}/L08.html Problem R2 solution",
    "PASS", "Re-derived: V_{n+1}(0.25) >= 0.5 + V_n(0.25) via the candidate k' = 0.25; non-expansiveness at beta = 1 from the proof of Theorem 2.2(a) with beta = 1 gives ||V_n - V*|| <= ||V_0 - V*||; contradiction with V_n(0.25) >= n/2. No gap.")
row("M5c-L08-E1-placeholder", "2.4-mathematics", f"{P}/L08.html Problem E1 solution",
    "PASS", "No unfilled argument: the counts 40, 527 are reproduced (recheck output). The a priori formula and the 1/ln 2, 1/ln(1/0.9), 1/ln(1/0.95) values are correct (1.4427, 9.4912, 19.4957).")
row("M5c-L08-term-order", "2.9-structure (term before definition)", f"{P}/L08.html why-it-matters paragraph (line 52) and Section 1",
    "PASS", "'feasible set' and 'grid' appear in the one-paragraph summary (line 52) before Section 1 defines them. They are plain-English terms in that summary; each is defined in Section 1 (the grid sentence and the F(k) bullet), before the first formal use. Not one of the plan's named terms that must be defined at first use; noted, not failed.")
row("M5c-L09-sharpness-overreach", "2.4-scope (quantifier)", f"{P}/L09.html canon-breaks item 3 and R3",
    "PASS", "Item 3 claims no constant below beta/(1-beta) works 'for this family at n = 1' for this map and V_0 = 0; R3 proves the equality for every beta in (0,1). The claim is limited to the family, so the quantifier is correct.")
row("M5c-L10-P4-contradiction", "2.4-prerequisites", f"{P}/L10.html Section 2 prerequisites paragraph and Lemma 2.4",
    "PASS", "The paragraph now says the monotonicity, estimate and additivity are not assumed and Lemma 2.4 proves them; Lemma 2.4 is proved from the Darboux definition and M2 Lemmas 1.1, 1.2. No contradiction remains.")
row("M5c-L10-P2-monotonicity-gap", "2.4-mathematics", f"{P}/L10.html Problem P2 solution",
    "PASS", "Solution uses Lemma 2.4(a) (applied to +/- m 2t) and linearity (P2), then Lemma 2.4(c) for the sum; each step matches the statements of Lemma 2.4 and P2 on the page.")
row("M5c-L10-corollary-checked-claim", "2.5-labs claim vs code", f"{P}/L10.html Key results row for Corollary 3.2",
    "PASS", "The row says Lab 1 Part A prints exact sums 'that tend to 2/3, which is consistent with it but does not compare them with 2/3'. Part A prints exact sums and their errors from 2/3 (right_err, left_err), so the row's description of the lab is slightly narrow but not false; no overreach.")
row("M5c-hub-L10-bounded-variation", "2.4-scope vs plan section 3", f"{P}/index.html line 142 (L10 card); plans/M5-build-plan.md line 215 (section 3, L10 bullet)",
    "FAIL", "The hub card now describes the C^1-integrator theory and the step, which matches L10.html. But plans/M5-build-plan.md section 3 requires L10 to establish the Riemann-Stieltjes existence result 'for G of bounded variation and f continuous ... proof or precise statement with hypotheses stated'. grep -i variation over course/modules/M/M5/*.html and cards.json returns nothing; the lesson has no bounded-variation statement. The Architect decisions (plan lines 219-220) do not remove this bullet.",
    fix="Either add a precise statement (with hypotheses listed, graded T or C with basis) for f continuous and G of bounded variation, or obtain an Architect ruling that removes the bullet from plan section 3 and then record the narrowed scope in the hub card (which already matches).")
row("M5c-cards-mirror-L08", "2.7-cards agree with lesson", f"{P}/cards.json M5-c133 (line 973), M5-c137 (line 999)",
    "FAIL", "M5-c133 now matches Misconception 1 (three facts: finite nonempty F(k), same F(k) for V and W, beta >= 0). M5-c137 states 'Unrounded, the largest ratio is 0.9 + 5.6 x 10^(-16)' with basis 'Lab 1 Part B'. The lab does not print that value (L08.html interpretation: 'The lab does not print this value'); it was recomputed outside the lab (recheck_L08_L10.py gives 0.9 + 5.55e-16). The card's basis misattributes the number to the lab.",
    fix="Change M5-c137 basis to 'recomputed outside the lab (L08 Lab 1 Part B interpretation)'; keep the printed 0.900000 as the lab's output.")
row("M5c-cards-R1-lipschitz", "2.7-cards agree with lesson", f"{P}/cards.json M5-c132 (line 965)",
    "PASS", "Card now says 'For each fixed V, ||B_beta V - B_gamma V|| <= |beta - gamma| ||V||, so BV depends Lipschitz-continuously on beta, with constant ||V||' which is Problem R1 exactly.")
row("M5c-L08-R3-well-definedness", "2.4-scope (characterisation claim)", f"{P}/L08.html 'Remark on well-definedness' (line 89) and canon-breaks item 2",
    "PASS", "The remark now says R3 'shows that it holds for every grid contained in (0, 1]' and 'gives a grid where it fails'. R3 proves min G in F(k) for G in (0,1] (k^alpha >= k there) and gives G = (2,3) with F(2) empty. No 'when it holds' characterisation remains.")
row("M5c-L09-certificate-only-when", "2.4-scope and self-consistency", f"{P}/L09.html Misconception 3 paragraph (line 297)",
    "FAIL", "The paragraph says 'A certificate guarantees a stated accuracy only when cert_N is compared with a tolerance'. The lab's fixed-count line (bound_holds True, cert 1.7433922005 = actual error) is a certificate that states an accuracy with no tolerance attached, so 'only when' is contradicted by the page's own output. The next sentences (a fixed count cannot certify 1e-6) are correct.",
    fix="Replace with: 'A certificate guarantees that the error is at most its value. To certify a tolerance tau, the certificate must be compared with tau, as in Theorem 2.4.'")
row("M5c-L10-canon-dG-replace", "2.4-mathematics (overgeneralised claim)", f"{P}/L10.html canon-breaks item 3 (line 363)",
    "PASS", "Now reads 'dG cannot be replaced by dx in general' with G = x^2 (value 2/3 vs 1/2, Corollary 3.2 and Part D) and G = x+5 (no change, by R3 with G = x and P3). The 'in general' qualifier is supported by the example.")
row("M5c-L10-R3-corollary-applies", "2.4-citation (hypothesis mismatch)", f"{P}/L10.html Problem R3 solution (line 484)",
    "PASS", "R3 now applies Theorem 3.1 with G' = 2x (continuous) to G + c = x^2 + 5 on [0,1], giving 2/3 = int_0^1 x * 2x dx. The hypotheses of Theorem 3.1 hold; Corollary 3.2 (which needs G = x^2 exactly) is no longer misapplied.")
# ---- round-3 new rows
row("M5c3-L08-E1-scales-with", "2.4-scope (proportionality without computation)", f"{P}/L08.html Problem E1 solution (line 362)",
    "FAIL", "The solution says the a priori count 'scales with 1/ln(1/beta)'. Recomputed with the lab's operator and tau = 1e-12 (recheck_L08_L10.py): n = 41, 283, 595 at beta = 0.5, 0.9, 0.95; n*ln(1/beta) = 28.42, 29.82, 30.52. The ratio is not constant (the numerator ln(d/(tau(1-beta))) changes with beta), so 'scales with' is an unsupported proportionality.",
    fix="Replace 'so it scales with 1/ln(1/beta)' with 'so its dependence on beta is through ln(1/beta) in the denominator, with a numerator that changes slowly with beta' (or state the three computed counts and stop).")
row("M5c3-cards-L09-c154-in-lab", "2.7-cards agree with lesson", f"{P}/cards.json M5-c154 (line 1129-1131)",
    "FAIL", "The front asks 'In Lab 1, what is the smallest n for which the a priori bound ... is at most 1e-6?'. Lab 1 does not compute that bound (lab prints the certified and naive stops only); the value 152 comes from Problem R2's solution, which derives ||V1-V0|| = sqrt(3)/2 by hand. Card basis is R2, so the 'In Lab 1' framing misattributes the source.",
    fix="Change the front to 'On the four-point grid of Lesson 9, ...' (drop 'In Lab 1,').")
row("M5c3-cards-L10-c175-continuity", "2.7-cards agree with lesson", f"{P}/cards.json M5-c175 (line 1285-1288); {P}/L10.html Remark 4.2 (line 344)",
    "FAIL", "The card's back says 'Continuity of f is needed as well (Remark 4.2).' Remark 4.2 says that Proposition 4.1 does not by itself show that hypothesis (2) is needed when G is continuously differentiable, so it does not support the general claim. Proposition 4.1 supports only: for a step integrator, a discontinuous integrand at the jump has no integral.",
    fix="Change the card back to: 'Monotonicity does not rescue the integral: Proposition 4.1 shows that a discontinuous integrand against a nondecreasing step has no integral. Remark 4.2 does not claim that continuity of f is necessary in general.'")
row("M5c3-L10-misc3-increasing", "2.4-quantifier vs counterexample", f"{P}/L10.html Misconception 3 (line 379); cards.json M5-c181 (line 1329-1332)",
    "FAIL", "Misconception 3 and card M5-c181 refute the claim 'the formula holds for every increasing G' with the step integrator, which is nondecreasing but not strictly increasing. The counterexample therefore does not match the quantifier as written. The conclusion (no general formula without C^1) is true, but the page does not show it for strictly increasing G.",
    fix="Change 'increasing' to 'nondecreasing' in Misconception 3 and card M5-c181 (the example then matches), or use the strictly increasing G(x) = x + 1_{x >= 1/2} with the same argument.")
row("M5c3-L09-typo-defined-here", "2.9-structure (prose)", f"{P}/L09.html line 58 ('The norm is defined here.The discounted ...')",
    "FAIL", "Missing space between sentences: 'The norm is defined here.The discounted Bellman operator' (grep of L09.html line 58).",
    fix="Insert a space after 'here.'.")
row("M5c3-labs-stray-L10-e", "2.5-labs (lab code lives once)", "tests/labs/M5/lab-M5-L10-1.py-e (tracked since c11ae01)",
    "FAIL", "A stale tracked copy of the L10 twin, named lab-M5-L10-1.py-e, sits beside the twin. diff shows an older version (Part D absent; different Part C wording). CLAUDE.md: 'Lab code lives once, in its twin'. run_labs is unaffected (13/13), but the stale copy is a second source of lab code.",
    fix="Delete tests/labs/M5/lab-M5-L10-1.py-e (git rm in the builder's commit; no verifier commit).")
row("M5c3-cards-L08-L10-read", "2.7-cards", f"{P}/cards.json (67 L08-L10 cards: M5-c121..c139, c140..c161, c162..c187)",
    "PASS", "Every L08-L10 card was read against its lesson text. Non-PASS card findings are in M5c-cards-mirror-L08 (c137), M5c3-cards-L09-c154-in-lab, M5c3-cards-L10-c175-continuity and M5c3-L10-misc3-increasing (c181). The remaining cards match their lesson statements and hypotheses (checked card by card; the full list is /tmp/M5-c-v3/cards_L08_10.txt).")

fragment = {
    "unit": "M5",
    "slice": "M5-c",
    "round": 3,
    "verifier": "round-3 independent verifier (Haiku) for slice M5-c (L08-L10); did not build M5; shares no context with builders or earlier verifiers",
    "pin": "aa3c26c",
    "base": "1817191",
    "checkout": "/tmp/verifyB3-M5-c",
    "scratch": "/tmp/M5-c-v3",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta from previous pin 1817191 to aa3c26c on this slice: L08.html, L09.html, L10.html, cards.json (M5-c077, c107, c109, c112, c120, c132, c133, c135, c137, c147, c154, c169, c186, c187 and others), index.html line 142. "
        "Lab twins tests/labs/M5/lab-M5-L08-1.py, L09-1, L10-1 unchanged since 1817191 (verified by git diff). "
        "Every previous non-PASS row was re-verified: M5c-hub-L10-bounded-variation FAIL (kept), M5c-cards-mirror-L08 FAIL (kept, now only c137), M5c-cards-R1-lipschitz PASS, M5c-L08-R3-well-definedness PASS, M5c-L09-certificate-only-when FAIL (kept), M5c-L10-canon-dG-replace PASS, M5c-L10-R3-corollary-applies PASS. "
        "No previous PASS row was carried: every cited subject either changed or was re-run. "
        "Gaps: the full pytest suite was run once in the background (it was broader than the brief required; the captured output showed progress dots only, so its summary line was not captured); targeted pytest (tests/test_labs.py, tests/test_docs_figures.py) exited 0. The 'Bellman equation' DAG wording (plan section 0.3) was checked by grep on the L08-L10 pages: the term 'Bellman equation' does not appear; only 'discounted Bellman operator'. "
        "Not checked: the Lesson 7 and Lesson 2/6 pages were checked only for the cited theorem numbers and hypotheses, not for their own content (other slices). Hub objectives and placement quiz (index.html) were not re-read in full."
    ),
    "summary": None,
}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_ids = [r["id"] for r in rows if r["status"] != "PASS"]
fragment["summary"] = {"rows": len(rows), "pass": pass_n, "fail": len(fail_ids), "unverifiable": 0, "mutants": 0, "fail_ids": fail_ids}
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print(json.dumps(fragment["summary"], indent=1))
