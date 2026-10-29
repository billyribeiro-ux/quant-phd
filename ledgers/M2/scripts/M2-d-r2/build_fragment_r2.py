"""Verifier round 2 (slice M2-d): writes ledgers/M2/M2-d.json. Rows, statuses and evidence are the verifier's own findings.
Run: python -I ledgers/M2/scripts/M2-d-r2/build_fragment_r2.py <checkout>"""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/M2/scripts/M2-d-r2/"
R = []

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

# 2.9 / 2.5 commands (run in round 2 on pin 1817191)
row("M2-d-cmd-check-pages", "2.9-structure", "course/modules/M/M2/L19.html ... L24.html", "PASS",
    "tools/check_pages.py --unit M2 --page L19 ... L24: 'check_pages M2 Lnn: PASS' for all six.")
row("M2-d-cmd-check-dag", "2.9-dag", "course/modules/M/M2/ (slice links)", "PASS",
    "tools/check_dag.py --unit M2: 'check_dag M2: PASS'; check_dag.py --all: CF1 and AP1 PASS.")
row("M2-d-cmd-run-labs", "2.5-labs", "tests/labs/M2/lab-M2-L19-1.py ... lab-M2-L24-1.py", "PASS",
    "tools/run_labs.py --unit M2 --page Lnn: 'run_labs M2: PASS (1/1)' for L19 through L24.")
row("M2-d-cmd-twins-isolated", "2.5-labs", "tests/labs/M2/lab-M2-L19-1.py ... lab-M2-L24-1.py", "PASS",
    "python -I -W error on each twin: exit 0 for L19..L24; stdout in /tmp/M2-v/d-r2/L19.txt .. L24.txt.")
row("M2-d-cmd-expected-match", "2.5-labs", "course/modules/M/M2/L19.html ... L24.html (pre.expected)", "PASS",
    "ledgers/M2/scripts/M2-d-r1/extract_expected.py /tmp/verifyB2-M2-d L19 ... L24: 'MATCH' for all six.")
row("M2-d-cmd-embed-match", "2.5-labs", "course/modules/M/M2/L19.html ... L24.html (data-run block)", "PASS",
    "ledgers/M2/scripts/M2-d-r2/embed_match_r2.py: embedded code equals the twin up to the final newline for all six "
    "(True). The round-1 exact comparison script reports DIFFERENT only because of that final newline.")
row("M2-d-cmd-page-smoke", "2.9-structure", "tools/page_smoke.py --unit M2 --pages L19 ... L24 --skip-sweep", "PASS",
    "'page_smoke M2: PASS', exit 0; /tmp/M2-v/d-r2/smoke.txt. The figure sweep was skipped and has nothing to sweep: "
    "grep for <svg> or <figure> in the six pages returns 0 each.")
row("M2-d-cmd-ruff-mypy", "2.5-labs", "tests/labs/M2/", "PASS",
    "ruff check tests/labs/M2: 'All checks passed!'; ruff format --check: '27 files already formatted'; "
    "mypy --no-incremental on the six slice twins: 'Success: no issues found in 6 source files'.")
row("M2-d-cmd-verify-refs", "2.1-citations", "references/references.json (keys spivak2008calculus, hubbard2015vector)", "PASS",
    "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit M2 "
    "(live): 'live re-verification of M2: 2 of 560 entries, 0 problems'.")
row("M2-d-2.1-keys-used", "2.1-citations", "course/modules/M/M2/L19.html ... L24.html (section 9 References)", "PASS",
    "Slice pages cite only spivak2008calculus and hubbard2015vector, in the References sections, which say that no statement "
    "is attributed to them. Re-read in L19..L24 (grep of 'spivak|hubbard' in the text dumps). No locator or theorem number is attributed to either key.")

# 2.2 numbers (recomputed in ledgers/M2/scripts/M2-d-r2/recheck_r2.py; output in /tmp/M2-v/d-r2/recheck_r2.out)
row("M2-d-num-L19", "2.2-numbers", "course/modules/M/M2/L19.html Lab 1, Misconception 2, Remark 3.2", "PASS",
    "recheck_r2.py: first-order ratios 3.9509, 3.9750, 3.9874 and second-order ratios 7.8836, 7.9429, 7.9717 (match the printed lab output); "
    "cross term |f_xy*d1*d2*0.1^2| = 0.010314 against second-order error 1.568275e-04 at s=0.1.")
row("M2-d-num-L20", "2.2-numbers", "course/modules/M/M2/L20.html Lab 1, Proposition 2.4, E1 to E3, Misconception 3", "PASS",
    "recheck_r2.py: exact Fraction midpoint sums in both orders equal 5/3 - 1/(6n^2) for n in 1,2,3,4,8,16,32 (True); "
    "Example 3.1 inner integrals at x=y=0.5 by quadrature give 0.8 and -0.8, matching 1/(1+x^2) and -1/(1+y^2).")
row("M2-d-num-L21", "2.2-numbers", "course/modules/M/M2/L21.html Lab 1 and E1 to E3", "PASS",
    "recheck_r2.py: roots 0.9168754789, 0.8351223485, 0.6823278038, 0.4533976515; dy/dx formula values match the printed "
    "ones; F_y runs from 2.3967 (x=1.0) to 2.7720 (x=0.25), so 'about 2.4 to 2.8' is a correct rounding.")
row("M2-d-num-L22", "2.2-numbers", "course/modules/M/M2/L22.html Lab 1 interpretation (Part A and Part B), Misconception 3, E1", "PASS",
    "recheck_r2.py: central differences of V equal ln a to eight decimals at a=1.5,2,3,4; f_xx(x*,a) at a=1.5 = -0.666667, "
    "so 0.5*0.667*1e-16 = 3.3e-17 (the page says about 3e-17, computed on the page). Part B printed errors 1.9e-13, 1.0e-12, 5.4e-12.")
row("M2-d-num-L23", "2.2-numbers", "course/modules/M/M2/L23.html Lab 1 hypothesis, interpretation, Misconception 1, E1 to E3", "PASS",
    "recheck_r2.py: P(0.04)=108110.895779 (rounds to 108111); P'=-851466.739529; P''=8376648.511919; -P'/P=7.875864 and "
    "P''/P=77.482001 (printed as previews); exact minus second-order expansion = -15.06 at +0.01 and +16.01 at -0.01; "
    "ratios 3.9279/3.9634 and 7.8807/7.9396.")
row("M2-d-num-L24", "2.2-numbers", "course/modules/M/M2/L24.html Lab 1, Part B interpretation, Misconceptions 1, E2, E3", "PASS",
    "recheck_r2.py: forward and central error table reproduces every printed value checked (k=1,5,8,9,11,15); "
    "2*sqrt(delta/e)=1.8074e-8 and (3delta/e)^(1/3)=6.2574e-6 with delta=2.22e-16; 0.5*e*1e-5=1.3591e-5; "
    "Problem M3 (2.1^3-2^3)/0.1=12.61.")

# 2.3 grades
row("M2-d-grade-L19-L20-L22-L23-L24", "2.3-grades", "course/modules/M/M2/L19.html ... L24.html (grade spans, key-results tables)", "PASS",
    "Every T row in the key-results tables matches a proof on the page (L19 Theorems 2.1, 3.1, Prop 3.3; L20 Thm 1.2, Props 2.2, 2.4, Example 3.1; "
    "L22 Lemma 1.2, Thm 1.3, Prop 2.1, Example 2.3; L23 Props 2.1, 2.2, 3.2, 3.3, Thm 3.1; L24 Thms 2.1, Props 3.1, 3.2, 4.2, 4.3). "
    "Results that depend on prerequisites are cited (L08, L09, L10). Lab results are labelled as lab results.")
row("M2-d-grade-L21-assumed-result", "2.3-grades", "course/modules/M/M2/L21.html Theorem 1.2 (proved in Section 1) and its uses", "PASS",
    "Theorem 1.2 now has a complete proof on the page (L21 lines 62-70): existence and uniqueness of g in J, continuity, differentiability by the mean value "
    "theorem and continuity of F_x, F_y, and C^1. Re-derived step by step; each inequality holds under the stated hypotheses. The previous FAIL is resolved. "
    "The stale name that remains is a separate prose row.")

# 2.4 mathematics
row("M2-d-math-L19-thm2.1", "2.4-math", "course/modules/M/M2/L19.html Theorem 2.1 and proof; Example 2.2", "PASS",
    "Re-derived Steps 1-3 (double mean value argument, bound with delta/2, limit in k). Example 2.2 re-derived: f_x(0,y)=-y, f_y(x,0)=x, "
    "f_xy(0,0)=-1, f_yx(0,0)=1; the continuity failure follows by contraposition.")
row("M2-d-math-L19-thm3.1-prop3.3", "2.4-math", "course/modules/M/M2/L19.html Theorem 3.1, Remark 3.2, Proposition 3.3", "PASS",
    "Re-derived: phi'' bound 2|h|^2 omega(|h|), phi(1)=phi'(s1)=s1 phi''(s2); Remark 3.2 coefficient with f_xy=f_yx from Theorem 2.1 "
    "(symmetry at p holds under Theorem 3.1's hypotheses); Prop 3.3 E(s)/E(s/2)->8 via 1/6 vs 1/48.")
row("M2-d-math-L19-misconception2", "2.4-math", "course/modules/M/M2/L19.html Misconception 2", "PASS",
    "Cross term at s=0.1 is 0.0103 (recheck_r2.py), well above the printed second-order error 1.568e-04, so dropping it changes the printed values.")
row("M2-d-math-L20-thm1.2-prop2.2-2.4", "2.4-math", "course/modules/M/M2/L20.html Theorem 1.2, Proposition 2.2, Proposition 2.4, P1 to P3", "PASS",
    "Re-derived: product split of the double Riemann sum; Prop 2.2 both orders 5/3; Prop 2.4 midpoint sum of x^2 equals 1/3-1/(12n^2) via the odd-square identity "
    "(verified n<=50 by the lab); both orders give 5/3-1/(6n^2).")
row("M2-d-math-L21-thm2.1-ex3.2", "2.4-math", "course/modules/M/M2/L21.html Theorem 2.1 and its proof; Examples 2.2, 3.1, 3.2; Problems P1 to P3", "FAIL",
    "Theorem 2.1 states the slope formula 'for every x in I', with I the interval of Theorem 1.2. Theorem 1.2 itself only asserts that some I and J exist with "
    "I x J inside U, and it does not state F_y != 0 on I x J. The proof of Theorem 2.1 says 'shrinking I and J if necessary ... gives F_y != 0 on I x J'. "
    "So the proof establishes the formula on a shrunken interval, not on the I the statement names. Example of the gap: F = y^3 - x, (x0,y0)=(1,1), "
    "I=(-0.1,1.1), J=(-0.5,1.5): the zero of F(x,.) in J is unique (g = cube root), F_y(0,0)=0, so the slope formula is undefined at x=0 "
    "(the triple is not C^1 at 0, so it is not a triple that Theorem 1.2 asserts; the point is that the statement does not fix I). Problems P1 to P3 and Examples 2.2, 3.1, 3.2 are correct.",
    "State Theorem 2.1 for x in the interval I of Theorem 1.2 after shrinking so that F_y != 0 on I x J (as the proof does), or add 'F_y != 0 on I x J' to "
    "the conclusion of Theorem 1.2 with its proof. Make card M2-c310 say the same.")
row("M2-d-math-L22-lemma-thm1.3-ex1.5", "2.4-math", "course/modules/M/M2/L22.html Lemma 1.2, Theorem 1.3, Remark 1.4, Examples 1.5, 2.2, 2.3, Proposition 2.1, P1 to P3", "PASS",
    "Re-derived: Lemma 1.2 both signs; Theorem 1.3 chain rule with f_x=0; Example 1.5 x*=a-1, V=a ln a-(a-1), V'=ln a; Example 2.2 V=a^2/4; Example 2.3 V=max(a,0) with one-sided derivatives 1 and 0; "
    "Prop 2.1 formula; Problem M1 to M3 values. Remark 1.4 uses that the zero of f_x(.,a) in J is unique; the proof of Theorem 1.2 gives this pointwise uniqueness, and the statement's function-level uniqueness is what Remark 1.4 cites.")
row("M2-d-math-L23-prop2.1-3.1-3.2-3.3", "2.4-math", "course/modules/M/M2/L23.html Proposition 2.1, Theorem 3.1, Propositions 3.2 and 3.3, P1 to P3", "PASS",
    "Re-derived P', P'', P''' term by term; sign of R(Delta) equals sign of -Delta; Lagrange remainder; Prop 3.3 from the second derivative. recheck_r2.py: P'<0, P''>0, P'''<0 at 0.04.")
row("M2-d-math-L23-prop2.2", "2.4-math", "course/modules/M/M2/L23.html Proposition 2.2 and proof", "PASS",
    "New proof handles y=0 separately, and for y != 0 uses 1-v=yv and the geometric series. Re-derived: sum_{t=1}^N v^t=(1-v^N)/y, so yF times it gives F(1-v^N), and adding F v^N gives F. Par check at yield 0.05 prints 100000.000000.")
row("M2-d-math-L23-quiz-essential", "2.4-math", "course/modules/M/M2/L23.html section 8 retrieval quiz (item on 'essential' hypothesis); section 6 Research R3", "FAIL",
    "The quiz asks 'Which hypothesis of Proposition 2.1 is essential to the sign P'(y) < 0?' with answer 'Every cash flow is positive'. "
    "The hypothesis is sufficient, not essential: recheck_r2.py with c_1 = -1, c_2 = 1000 (N=2) gives P'(0.04) = -1777.07 < 0, so P'<0 holds without every cash flow being positive.",
    "Reword the item to ask which hypothesis guarantees the sign (sufficient), and say that the condition is not necessary; R3 already says the sign is not fixed by the terms, so state it there.")
row("M2-d-math-L24-prop3.1-3.2-thm2.1", "2.4-math", "course/modules/M/M2/L24.html Theorem 2.1, Propositions 3.1, 3.2, 4.2, 4.3 and their proofs; Problems M1 to M3, P1 to P3", "PASS",
    "Re-derived: |x| quotients; Prop 3.1 and 3.2 truncation bounds with the sign and factor of 1/12 and 1/6; Prop 4.2 minimizer h*=sqrt(B/A) with A=M2/2, B=2delta; "
    "Prop 4.3 h^3=3delta/M3 with C=M3/6; the hypotheses M2>0 and M3>0 are needed for the minimizers. Misconception 1 rise 6.603e-9 -> 2.154e-7 checked.")
row("M2-d-math-L24-derivative-def", "2.4-math", "course/modules/M/M2/L24.html Section 1 (definition of the derivative, quotients)", "PASS",
    "The derivative is the limit of the difference quotient over both signs of h. The forward quotient can have a one-sided limit where the derivative does not exist (|x| at 0). Whenever the derivative exists the central quotient converges to it: D0 = (D+ + D-)/2 and both one-sided quotients converge. Consistent with Theorem 2.1.")
row("M2-d-math-L24-prop4.2-4.3", "2.4-math", "course/modules/M/M2/L24.html Propositions 4.2 and 4.3, their proofs, Key results", "PASS",
    "The minimization requires M2>0 (resp. M3>0) and delta>0, now stated in each proposition and Key results row. Recomputed the bound at h* for M2=e and delta=2.22e-16: 2 sqrt(M2 delta)=4.9131e-08 equals g(h*).")
row("M2-d-math-L20-def-not-apply", "2.4-math", "course/modules/M/M2/L20.html Section 3, Example 3.1 (non-applicability of Definition 1.1)", "PASS",
    "The page now says it does not check Definition 1.1's hypothesis for the unbounded integrand and makes no claim that the double integral exists. Consistent with Definition 1.1 (closed rectangle, all tags).")
row("M2-d-math-L20-scope", "2.4-math", "course/modules/M/M2/L20.html 'Why it matters' and Section 3", "PASS",
    "The sentence 'in practice it is computed one variable at a time' is replaced by 'Lab 1 computes an example one variable at a time', which is what the lab does.")
row("M2-d-math-L21-R1-hypothesis", "2.4-math", "course/modules/M/M2/L21.html Research R1 and its solution", "PASS",
    "Now says the bond has every cash flow positive and cites L23 Proposition 2.1 with that hypothesis, so P'<0 holds. dy/dP0 = 1/P'(y) < 0 re-derived.")

# 2.5 labs
row("M2-d-lab-L19", "2.5-labs", "course/modules/M/M2/L19.html Lab 1 hypothesis, interpretation; tests/labs/M2/lab-M2-L19-1.py", "PASS",
    "The central difference is defined in the hypothesis paragraph before use (the lab uses u(x+h,y)-u(x-h,y))/(2h)). Predictions (f_xx=0.41218, f_xy=2.14872, f_yy=1, errors about 1e-11 printed as 2.26e-11) match the output. Interpretation: lab tests one function and one direction; the limit is Prop 3.3's content.")
row("M2-d-lab-L20-overreach", "2.5-labs", "course/modules/M/M2/L20.html Lab 1 interpretation and E2", "PASS",
    "Now says n = 1, 2, 4, 8, 16, 32 and 'each of the six printed values of n'; main() loops over (1, 2, 4, 8, 16, 32) and prints six match True lines. The identity for n<=50 is in the lab. Previous FAIL resolved.")
row("M2-d-lab-L21", "2.5-labs", "course/modules/M/M2/L21.html Lab 1 hypothesis and interpretation", "PASS",
    "Predictions (agreement to about 1e-11, residuals at rounding level) match the output (differences 6.2e-13 to 3.9e-12; residuals up to 2.2e-16). The interpretation says the lab does not test uniqueness, which matches main(). The stale name in the hypothesis paragraph is a separate prose row.")
row("M2-d-lab-L22-count", "2.5-labs", "course/modules/M/M2/L22.html Lab 1 interpretation, last sentence", "PASS",
    "Now: 'The lab checks two problems, Part A at four values of a and Part B at three values of a'. Matches the lab docstring ('two maximization problems') and output (4 + 3 lines).")
row("M2-d-lab-L23", "2.5-labs", "course/modules/M/M2/L23.html Lab 1 hypothesis, interpretation, E1 to E3", "PASS",
    "'Tens of cents' is replaced by the printed 15 and 16 cents at the two shifts. Predictions (par price 100000, P'<0, P''>0, alternating remainder, ratios 4 and 8) match the output. Previews printed and undefined, as stated.")
row("M2-d-lab-L24", "2.5-labs", "course/modules/M/M2/L24.html Lab 1 hypothesis, interpretation, E1 to E3", "PASS",
    "Part A prints +1/-1/0 for k=1..6; Part B values match recheck_r2.py; 'ties at three digits' with 5.859e-11 at 1e-5 and 1e-7 is correct; decade grid is range(1, 16). The 'predicted minimizer 6.3e-6 lies between decades' statement is correct (log10 6.26e-6 = -5.2).")
row("M2-d-lab-L22-naive-constant", "2.5-labs", "course/modules/M/M2/L22.html Lab 1 hypothesis ('prints the naive partial ... which is zero')", "PASS",
    "The printed 'naive partial 0.00000000' comes from the literal naive_partial = 0.0 in the lab code, so it is true by construction rather than computed. The page says the lab prints it, which is accurate; the demonstration rests on the computed central difference a/2 against the reduced problem. Recorded as a note, not a defect.")

# 2.9 prose
row("M2-d-prose-L19-schwarz", "2.9-prose", "course/modules/M/M2/L19.html Misconception 3 heading; tests cards M2-c294", "PASS",
    "Heading now reads 'shows that Theorem 2.1 fails'; card M2-c294 now reads 'Theorem 2.1 fails'. grep for 'Schwarz' in the six pages and in cards.json for M2-c280..c377 returns nothing.")
row("M2-d-prose-L19-central-difference", "2.9-prose", "course/modules/M/M2/L19.html Lab 1 hypothesis, Section 4, Misconception 3, E1", "PASS",
    "'central difference' is defined in the Lab 1 hypothesis paragraph at its first use; 'finite-difference' terms in Section 4 point to L13 (L13 introduces finite-difference derivative approximation).")
row("M2-d-prose-L19-hypothesis-count", "2.9-prose", "course/modules/M/M2/L19.html Section 4, bullet 1 ('The statement of Theorem 2.1 has three hypotheses, and each one is used in the proof')", "FAIL",
    "Theorem 2.1 states the conditions 'f_x, f_y and f_xy exist at every point of N' and 'f_xy is continuous at p'. That is two conditions (existence, continuity) or four listed items (three existence conditions and one continuity condition), not three.",
    "Replace 'three hypotheses' with 'four conditions' (or 'two hypotheses, existence of the three partials and continuity of f_xy at p').")
row("M2-d-prose-L20-thm1.2-cite", "2.9-prose", "course/modules/M/M2/L20.html Theorem 1.2 proof and Section 1 (citation of L09)", "PASS",
    "Cites 'Corollary 2.3 of Lesson L09 for monotone integrands'. L09 Corollary 2.3 (course/modules/M/M2/L09.html line 77): for monotone f and any Riemann sum R with mesh delta, |R - integral| <= delta |f(b)-f(a)|, which gives convergence for every choice of tags. The monotonicity of x, x^2 and y is correct.")
row("M2-d-prose-L21-process-word", "2.9-prose", "course/modules/M/M2/L21.html References and Section 2; card M2-c315", "PASS",
    "'in this build' no longer appears in L19..L24 or cards.json (grep count 0). The implicit-function result is now proved on the page.")
row("M2-d-prose-L21-assumed-name", "2.9-prose", "course/modules/M/M2/L21.html Lab 1 hypothesis (line 102) and Exercise E3 (line 290)", "FAIL",
    "'Assumed result 1.2' is no longer a labelled result in L21 (it is Theorem 1.2 and is proved), but the lab hypothesis says 'the hypothesis of Assumed result 1.2 holds at every point the lab uses' and E3 says 'the root that Assumed result 1.2 provides'. A reader cannot find that name.",
    "Replace 'Assumed result 1.2' with 'Theorem 1.2' in both places.")
row("M2-d-prose-L22-uniqueness", "2.9-prose", "course/modules/M/M2/L22.html Section 2 bullets and Misconception 2; card M2-c334", "PASS",
    "No uniqueness is claimed as a hypothesis; Theorem 1.3 uses (H2) and (H3) and an open J; Example 2.3 covers the closed domain and the non-unique maximizer at a=0. Consistent.")
row("M2-d-prose-L23-units", "2.9-prose", "course/modules/M/M2/L23.html Lab 1 interpretation", "PASS",
    "Units now stated: 1.6e-03 cents per unit yield and 1.9 cents per unit yield squared, against 851466.74 and 8376648.51 in the same units. Printed values match.")
row("M2-d-prose-L23-exponentials", "2.9-prose", "course/modules/M/M2/L23.html Section 4 bullet 1 and Lab 1 hypothesis", "PASS",
    "Now 'a sum of powers of (1+y)' and 'the tangent line never lies above the price' under positive cash flows (Prop 3.3); the earlier 'biased in one direction for every shift' is gone.")
row("M2-d-prose-L24-problem-ref", "2.9-prose", "course/modules/M/M2/L24.html Section 5 bullet 3", "PASS",
    "Now 'Problem P3 shows for sqrt(1+x)-1', and P3 in Section 7 is the rewrite x/(sqrt(1+x)+1). Correct.")
row("M2-d-scope-words-L21-L24", "2.9-prose", "course/modules/M/M2/L21.html ... L24.html introductions and body text", "PASS",
    "Grep for 'many', 'usually', 'rarely', 'in practice', 'as much as', 'drives', 'offsets', 'raises' in L19..L24: the earlier 'Many ...' and 'is usually answered' are rewritten; 'raises' occurs only in Python docstrings and the Misconception 'raises the price' (a false statement being corrected).")
row("M2-d-banned-phrases", "2.9-prose", "course/modules/M/M2/L19.html ... L24.html", "PASS",
    "grep for 'roughly', 'historically', 'about 6%', ellipses in learner text: no matches. Ellipses in code are range/tuple syntax only.")
row("M2-d-dag-prose-names", "2.9-prose", "course/modules/M/M2/L20.html Remark 2.3 ('often called Fubini's theorem')", "PASS",
    "Carried in substance: the remark is unchanged since the previous pin, names the statement it describes, grades it nothing and uses it nowhere. The name is not a registered source, so no locator or theorem number is attributed.")

# DAG and structure
row("M2-d-dag-links", "2.9-dag", "course/modules/M/M2/L19.html ... L24.html concept links and 'Uses' lines", "PASS",
    "check_dag M2 PASS. Prerequisite citations: L08 (Lagrange remainder, introduced there), L09 (Corollary 2.3), L10 (FTC), L13 (finite-difference approximation), L14 (automatic differentiation), L16/L17/L18 (partials, gradient, Jacobian), M1 (prereq of M2 per curriculum/01-foundations.yaml line 126). All cited lessons precede or are M1.")
row("M2-d-dag-closure", "2.9-dag", "course/modules/M/M2/L19.html ... L24.html (concepts used by name)", "PASS",
    "No slice lesson uses a concept outside M2's prerequisite closure by name: M1 is a direct prerequisite; AC1, S0, S2 are not named in the slice.")
row("M2-d-struct-hours", "2.9-structure", "course/modules/M/M2/L19.html ... L24.html data-hours and index.html data-hours-lessons", "PASS",
    "Declared lesson hours: 10 each for L19..L24; sum of data-hours over L01..L24 is 240, equal to index.html data-hours-lessons=240, and 240+60=300 (Tier F). Pace not judged (architect ruling).")
row("M2-d-cards-duplicate-scan", "2.7-cards", "course/modules/M/M2/cards.json (377 cards)", "PASS",
    "Full scan: 377 cards, no duplicate ids, no duplicate fronts (case-insensitive). New cards M2-c376 (L01, outside this slice, not checked here) and M2-c377 (L24, checked below). Card decimals appear in their lesson text (card_numbers_r2.py: no misses).")
row("M2-d-cards-L19-L20", "2.7-cards", "course/modules/M/M2/cards.json M2-c280..c307", "FAIL",
    "Card M2-c292 back reads 'Equality follows when f_xy is continuous at the point (Theorem 2.1, Misconception 1)'. Theorem 2.1 also needs f_x, f_y and f_xy to exist at every point of the disc N; the card drops that hypothesis. The other L19 and L20 cards (c281-c291, c293-c307, including the corrected c294) match their lesson text and the numbers in it.",
    "Restore the existence hypothesis on c292: 'Equality follows when f_x, f_y and f_xy exist near the point and f_xy is continuous at it'.")
row("M2-d-cards-L21", "2.7-cards", "course/modules/M/M2/cards.json M2-c308..c322", "PASS",
    "Card M2-c309 now names Theorem 1.2 and says it is proved in Section 1; card M2-c315 no longer says 'in this build'; M2-c319 adds the sufficiency remark; M2-c317, c318, c321, c322 match Examples 3.1, 3.2 and Misconception 2, 3. Card M2-c310 repeats Theorem 2.1's 'for every x in I after shrinking' (see M2-d-math-L21-thm2.1-ex3.2), which is consistent with the proof but not with the statement.")
row("M2-d-cards-L22", "2.7-cards", "course/modules/M/M2/cards.json M2-c323..c337", "PASS",
    "Card M2-c326 names Theorem 1.2 of Lesson 21 (proved there); M2-c334 says no uniqueness is assumed; M2-c336 matches the 1e-8 printed location error; c327..c333 values re-derived (V=a ln a-(a-1), a/2, V(a)=max(a,0), one-sided derivatives 1 and 0).")
row("M2-d-cards-L23", "2.7-cards", "course/modules/M/M2/cards.json M2-c338..c357", "PASS",
    "All twenty cards match the current lesson text and its printed numbers (-851466.739529, 8376648.511919, 1.6e-03, 1.9, 4.037716e+02, -1.506081e+01, 117060, 100015 minus -15 etc.).")
row("M2-d-cards-L24", "2.7-cards", "course/modules/M/M2/cards.json M2-c358..c377", "FAIL",
    "Cards M2-c363 ('Hypotheses: those of Proposition 3.1 and Definition 4.1. ... The bound is smallest at h* = 2 sqrt(delta/M_2)') and M2-c364 ('... smallest at h* = (3 delta/M_3)^(1/3)') drop the lesson's new hypotheses M_2 > 0 and M_3 > 0 that Propositions 4.2 and 4.3 now state. Other cards (c358, c359..c362, c365..c377, including new c377) match the lesson text and its numbers.",
    "Add 'with M_2 > 0' to card M2-c363 and 'with M_3 > 0' to card M2-c364.")

frag = {
    "unit": "M2",
    "slice": "M2-d",
    "round": 2,
    "verifier": "independent verifier (Haiku), round 2, slice M2-d (L19-L24 and their lab twins); did not build M2 and shares no context with the builders",
    "pin": "1817191",
    "base": "c11ae01",
    "previous_ledger": "/tmp/fanout-frags/B-M2-d.round1.json",
    "checkout": "/tmp/verifyB2-M2-d (detached at 1817191)",
    "scratch": "/tmp/M2-v/d-r2",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since round 1 (c11ae01..1817191): course pages L19..L24, cards.json (2 cards added: c376 L01, c377 L24), and the M2 hub. Lab twins tests/labs/M2 and tools/ are byte-identical to the pin; no lab was changed.",
        "Every previous non-PASS row was re-verified from scratch. Every row whose subject changed was re-verified. No row was carried forward on a byte-identity basis because all six slice pages changed.",
        "Mutants: none. This is a lesson slice; the architect ruling says lab twins are demonstrations and mutation applies to project graders only.",
        "Not checked: M2-c376 (lesson L01, belongs to another slice); grades and proofs of lessons outside L19..L24; live network access for the L21 Theorem 2.1 counterexample is not needed (algebraic).",
        "Hours: declared 10 h per lesson, not judged on pace (architect ruling). Only the arithmetic (240 lesson hours = hub split) was checked.",
        "The brief's 'two-dimensional' sweep: page_smoke ran with --skip-sweep; the six pages contain no svg or figure element, so the sweep has no target.",
    ],
    "summary": "Round 2, slice M2-d: 6 FAIL rows (M2-d-math-L21-thm2.1-ex3.2; M2-d-math-L23-quiz-essential; M2-d-prose-L19-hypothesis-count; M2-d-prose-L21-assumed-name; M2-d-cards-L19-L20 (card c292); M2-d-cards-L24 (cards c363, c364)). Round-1 FAIL rows fixed: L19 Schwarz, L19 central difference, L20 overreach, L20 citation, L21 assumed-result grade, L21 process word, L21 R1 hypothesis, L22 uniqueness, L22 count, L23 units, L23 exponentials, L23 Prop 2.2, L24 derivative definition, L24 Prop 4.2/4.3, L24 problem reference, scope words.",
}
out = root / "ledgers/M2/M2-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), "FAIL", sum(r["status"] == "FAIL" for r in R), "PASS", sum(r["status"] == "PASS" for r in R))
