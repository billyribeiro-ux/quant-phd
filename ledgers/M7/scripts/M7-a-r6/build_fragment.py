"""Builds ledgers/M7/M7-a.json (round 6, slice a) from the verifier's findings. Rows carry their evidence inline."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/M7/scripts/M7-a-r6"
G = f"{S}/run_gates_output.txt"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---------- hub index.html ----------
row("M7a-hub-structure", "2.9 structure: hub sections and minimums", "course/modules/M/M7/index.html lines 29-177",
    "PASS",
    f"check_pages --unit M7 PASS ({G} line 91). Read all 182 lines. Objectives: 8 items (lines 48-57, rule 4-8). "
    "Prerequisites with concept links (60-69). Placement quiz with 9 items (75-135), data-mastery 0.8 (71). Lesson map: "
    "8 cards L01-L08 with data-progress-key (143-150). Ladder: four span.rung-title in order Worked example, Completion, "
    "Independent, Stretch (158-161). Data (165-168). Reading list (170-177).")
row("M7a-hub-hours", "2.9 hours split arithmetic", "index.html lines 29, 40-42, 141-150; L01-L08 data-hours",
    "PASS",
    "Hub data-hours-lessons=77, data-hours-project=33: 77+33=110; 33/110=30.0%, 77/110=70.0% (widths 70%/30% at line 40). "
    "Per-lesson data-hours (grep): L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10; sum 77. Card kickers "
    "(143-150) and the sentence at line 141 (Lessons 1, 2, 7 declare 9 hours) agree. Hours are design targets; no arithmetic "
    "inconsistency.")
row("M7a-hub-placement-numbers", "1 numbers in prose and numeric items", "index.html lines 73, 75-135",
    "PASS",
    "Recomputed: 7/9 = 77.8%, 8/9 = 88.9%, 80% of 9 = 7.2 so eight correct is the bar (line 73). Keys recomputed: "
    "d/dx1 of x1^2+3x1x2 at (1,0) = 2 (line 76, data-answer 2); mixed partial = 3 (81, data-answer 3); smaller eigenvalue "
    "of [[2,1],[1,2]] = 1 (95, answer 1); d/dx x^2 at 3 = 6 (132, answer 6); skill numeric: Sigma=diag(1,2), u=(1,1/2), "
    "lambda = 2/3 = 0.6667 (126-129, tolerance 0.001 accepts 2/3). Nine items: 7 non-skill, 2 data-skill (117, 126), "
    "meeting 'at least two skill items'.")
row("M7a-hub-placement-explanations", "2.2 attributions in placement explanations",
    "index.html lines 88-124", "PASS",
    "Pq1 (92): diag(1,-1) gives -1 at (0,1), [[0,1],[1,0]] gives -2 at (1,-1); identity is the PSD option; correct. "
    "Pq5 (106): 'M1 Lesson 1, Theorem 3.1' verified at course/modules/M/M1/L01.html line 79 (Theorem 3.1, negating one "
    "quantifier). Pq6 (124): 'Lesson 2, Proposition 3.2 (c)' verified at L02.html line 122-123 (c) gradient = lambda 1. "
    "Pq7 (115): spectral theorem statement consistent with M3 closure.")
row("M7a-hub-cross-refs", "2.9 cross-references to other lessons and project",
    "index.html lines 156-161, 176; project.html lines 44-55", "PASS",
    "Stretch rung (161): 'Lesson 2, Problem R3' exists (L02.html 421-425) and computes the derivative c/s of c^2/(2s), "
    "equal to lambda at c=1 (matches). Skill-check note (129): 'rung 2 has three assets and bounds (project page, Lab 2)' "
    "verified at project.html line 45 (Lab 2, completion) and lines 44-45/54 (three-asset problem).")
row("M7a-hub-dag-concepts", "2.9 / DAG: concept links and definitions",
    "index.html; L01.html; L02.html; L03.html; check_dag --unit M7", "PASS",
    f"check_dag --unit M7 PASS ({G}). Concept links resolve to closure ids: gradient, hessian, implicit-function-theorem, "
    "envelope-theorem, positive-semidefinite-matrix, eigendecomposition, spectral-theorem (M2, M3, M1 via prerequisites). "
    "Definitions once each: convex-set (L01 line 57), convex-function (L01 line 82), lagrange-multiplier (L02 line 63), "
    "kkt-conditions (L03 line 62). Lesson links point only backward (L03 -> L01#def-convex-function, L02#def-lagrange-multiplier). "
    "Out-of-closure terms appear as plain prose only (no data-concept): covariance (index 167, disclaimer), efficient "
    "frontier and turnover (index 54, 148), dynamic programming (index 7, 149), value function (index 55), convexity "
    "(FI1 name collision, prose). Verified with grep for data-concept and concepts.html#.")
row("M7a-hub-covariance-disclaimer", "2.4 / plan B1 disclaimer", "index.html line 167", "PASS",
    "'estimating a covariance matrix is outside M7' appears once, with no link (grep). Matches architect decision B1/Q1.")
row("M7a-hub-attributions-registry", "2.1 attribution and registry fields",
    "index.html lines 170-177; L01.html 548-551; L02.html 531-535; L03.html 541-545; references/references.json entries "
    "boyd2004convex (line 3648) and stokey1989recursive (line 21295)", "PASS",
    "boyd2004convex: title 'Convex Optimization', authors Boyd, Vandenberghe, year 2004, years [2004,2013], print_year 2004 "
    "(matches the page's '(2004)'). stokey1989recursive: title 'Recursive Methods in Economic Dynamics', authors Stokey, "
    "Lucas, Prescott, year 1989; the page says the curriculum string is 'Stokey & Lucas' and that the record has three "
    "authors (index 176), which is accurate. No locator, page or theorem number is attributed to either book on any of the "
    "four pages (grep: data-locator count 0 in all four pages; no page or passage locator follows either key). verify_refs --offline: 560 entries, 0 problems "
    f"({G}). Live Crossref re-resolution not run (see notes).")
row("M7a-hub-data-simulated", "2.8 data and SIMULATED labels", "index.html lines 37, 167; L01 line 165; L02 line 157; L03 lines 143, 161-162",
    "PASS",
    "grep: no data-files, svg, figure or figures- in index/L01/L02/L03 (count 0), so 'no lab reads a data file' and 'no figure "
    "shows a real asset' are true. SIMULATED labels: L01 lab docstring (165), L02 docstring (157), L03 section 4 (143) and "
    "lab docstring (161-162). Inputs stated as hand-chosen or generated.")
row("M7a-hub-page-smoke", "2.9 page_smoke: console, math, external requests, 360 px",
    "index.html, L01.html, L02.html, L03.html", "PASS",
    f"page_smoke --unit M7 --pages index L01 L02 L03: PASS for all four pages ({G} lines 110-123; full output "
    f"{S}/run_gates_output.txt). Labs in Pyodide: lab-M7-L01-1 0.6 s, lab-M7-L02-1 0.0 s, lab-M7-L03-1 0.0 s (limit 10 s).")
row("M7a-hub-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)",
    "index.html; L01.html; L02.html; L03.html", "PASS",
    "grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, "
    "it is important to note, studies show, experts agree, well known, obviously, clearly, note that, let us, we will, "
    "interestingly, importantly: zero hits in the four pages.")
row("M7a-hub-prereq-prose", "2.9 prose accuracy", "index.html line 65", "PASS",
    "'Lesson 2 uses positive semidefinite matrices for its matrix Sigma': L02 requires Sigma positive definite (L02.html 114, "
    "Prop 3.2 at 122). Positive definite implies positive semidefinite, so the sentence is true but understates the "
    "hypothesis. Non-blocking note; no change required.")
row("M7a-hub-lede-claims", "2.9 claims about lessons", "index.html line 141", "PASS",
    "'Each lesson page has graded claims, runnable labs, a problem set with worked solutions, and a retrieval quiz' verified "
    "for L01, L02, L03 (grade attributes, lab sections, details.solution blocks, quiz sections).")

# ---------- L01 ----------
row("M7a-L01-structure", "2.9 structure and minimums", "course/modules/M/M7/L01.html", "PASS",
    f"check_pages --page L01 PASS ({G}). Read all 563 lines. Order matches BUILDER_RULES 4.2: why-it-matters (51, 107 words "
    "<= 120), sections 1-3 (53-150), inline lab (157-310, before canon), canon-breaks (313), misconceptions (323-339, "
    "three items), problems (341-444, three per tier), key-results (446-460), quiz (462-546, 11 items), references (548). "
    "data-hours=9 matches hub.")
row("M7a-L01-lab-run", "2.5 lab: run and twin identity", "L01.html lines 157-310; tests/labs/M7/lab-M7-L01-1.py",
    "PASS",
    f"run_labs --page L01 PASS (1/1). {S}/check_labs.py: page code byte-equal to twin (after rstrip): True; twin run with "
    "python -I -W error exit 0, stderr empty; stdout equals the page expected block (data-tolerance 0). ruff check/format and "
    "mypy --strict on the twin pass; pytest tests/test_labs.py -k 'M7 and L01' passes (run_gates_output.txt lines 96-106).")
row("M7a-L01-lab-numbers", "2.2 numbers printed by Lab 1", "L01.html lines 295-308 (expected block)", "PASS",
    f"{S}/recompute_numbers.py (independent of the twin): 3125 cases per function over 625 ordered pairs x 5 weights; Q1 identity "
    "3125 of 3125; Q2 identity 3125 of 3125; Q1 chord 3125; Q2 chord 2573; Q2 negative pairs 184; 3*184 = 552 = 3125-2573; "
    "midpoint value 3/2, chord 1, chord-minus-midpoint -1/2, identity term (1/4)(1,-1)'Q2(1,-1) = -1/2; Q2 quad at (1,-1) = -2. "
    "Hessian eigenvalues 6,2 (Q1) and 6,-2 (Q2) by hand (Example 3.3).")
row("M7a-L01-lab-prose", "2.5 claims about what the lab prints (defect class 2)", "L01.html lines 159, 309, 319, 332, 336",
    "PASS",
    "Hypothesis (159): 'both identity lines read 3125 of 3125', 'Q2 eigenvalues 3 and -1', failing count = 3 x negative pairs: "
    "each matches output lines 297-302. Misconception 1 (332): eigenvalue -2 of 2Q2 and midpoint 3/2 vs chord 1: lines 305-306, "
    "303. Misconception 2 (336): 2573 of 3125 and 552 failing: line 300. Interpretation (309) and canon (319): counts match. "
    "The docstring's four checks (lab lines 167-176) match the code (cases() uses all ordered pairs and all five weights).")
row("M7a-L01-lemma-3-1", "2.4 Lemma 3.1 identity and proof", "L01.html lines 108-121", "PASS",
    "Re-derived: q(z) = l^2 q(x) + (1-l)^2 q(y) + 2l(1-l) x'Qy; l q(x) - l^2 q(x) = l(1-l) q(x) etc.; gap = l(1-l)(q(x)+q(y)-2x'Qy) "
    "= l(1-l)(x-y)'Q(x-y). Exact check on 3125 cases (row M7a-L01-lab-numbers).")
row("M7a-L01-props", "2.4 Propositions 1.3, 2.3, 3.2 and proofs", "L01.html lines 66-148", "PASS",
    "Re-derived each proof. Prop 1.3 and 2.3 complete with stated hypotheses. Prop 3.2: (i)<->(ii) without Assumption 1 "
    "(gap identity with y=0, lambda=1/2 gives q(x)/4; and (ii)=>(i) via lambda(1-lambda) >= 0). Assumption 1 (lines 129-131) is named, "
    "stated as the spectral theorem from M3 and not proved; it is used only in (ii)=>(iii) and (iii)=>(ii) (lines 146-147), as "
    "the text says.")
row("M7a-L01-examples", "2.2 numbers in Examples 1.2, 2.2, 3.2a, 3.3", "L01.html lines 61-63, 88-89, 124-125, 153-154", "PASS",
    "Q1 eigenvalues 3,1 with eigenvectors (1,1),(1,-1) (Q1(1,1)=3(1,1)); Q2 eigenvalues 3,-1 (Q2(1,-1)=-(1,-1)); Hessians 2Q; "
    "circle midpoint (1/2,1/2) has squared norm 1/2. All correct.")
row("M7a-L01-problems", "2.4 problem-set solutions and numbers", "L01.html lines 345-444", "PASS",
    "M1 half-space convex; M2 chord at x^2 gives 1 and Lemma 3.1 gives 1; M3 q(1,1)=6, gap 6 = (1/4)*24 (Q1, x-y=(2,2)); "
    "P1 midpoint of 2 and -2 is 0 with f=0<1; P2 correct; P3 gap 1/4 q(v) < 0; E1 counts (3x184=552); E2; E3 (Q1 eigenvalues 3,1); "
    "R1 x'Qx = x1^2+x2^2 and symmetric part I; R2; R3: a+c=4, ac-b^2=3 for Q1. Tier counts 3/3/3/3 (check_pages).")
row("M7a-L01-key-results-grades", "2.3 grades", "L01.html lines 67, 93, 109, 134, 452-456", "PASS",
    "Lemma 3.1, Props 1.3, 2.3, 3.2 carry data-grade T and are proved on the page; Prop 3.2 (iii) row is marked conditional on "
    "Assumption 1 (line 456). Example 3.2a row T (derived). No unsupported grade.")
row("M7a-L01-quiz", "2.9 retrieval quiz (11 items)", "L01.html lines 462-546", "PASS",
    "Each key recomputed: disk convex; Hessian entry (1,1) of Q1 = 4; smaller eigenvalue 1; Q2 correct option (eigenvalue -1); "
    "gap -1/2; 3125; defining inequality <= ; Hessian 2Q; intersections; xQ2x at (1,-1) = -2; one failing case. Union example "
    "in the explanation (line 529): disks of radius 1 at (+/-3,0), midpoint (0,0) at distance 3 from both centres: correct.")
row("M7a-L01-canon-misconceptions", "2.9 canon and misconceptions", "L01.html lines 313-339", "PASS",
    "Four canon bullets re-checked against Example 1.2, Prop 1.3/2.3, the constant-function remark and the 3125-case grid. "
    "Three misconceptions (326, 330, 334), each with wrong belief and reason; numbers match Lab 1.")
row("M7a-L01-notation", "2.4 notation (BUILDER_RULES 3; notation/notation.json)", "L01.html", "PASS",
    "Local symbols: S_i, D, C, Q, Q1, Q2, H, V, Lambda, mu_i (eigenvalues), L_c (sublevel set). None is a registered "
    "program symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q-measure). \\mathbb{R} and \\R used; registered macro renders "
    "in page_smoke.")

# ---------- L02 ----------
row("M7a-L02-structure", "2.9 structure and minimums", "course/modules/M/M7/L02.html", "PASS",
    f"check_pages --page L02 PASS ({G}). Read all 546 lines. Order: why-it-matters (51, 110 words), sections 1-3, inline lab "
    "(148-293), canon (295-304, four bullets), misconceptions (306-322, three), problems (324-427, three per tier), key-results "
    "(429-443, five rows), quiz (445-529, 11 items), references (531-535). data-hours=9.")
row("M7a-L02-lab-run", "2.5 lab: run and twin identity", "L02.html 148-293; tests/labs/M7/lab-M7-L02-1.py", "PASS",
    f"run_labs --page L02 PASS. check_labs.py: code == twin True; twin exit 0 under python -I -W error, stderr empty; stdout == "
    "expected block. ruff/mypy strict/pytest pass (run_gates_output.txt). The LCG seed 1 and its 9 outputs were recomputed "
    "independently: [1,2,3,1,-1,2,-1,-1,0].")
row("M7a-L02-lab-numbers", "2.2 numbers printed by Lab 1", "L02.html lines 279-291", "PASS",
    f"{S}/recompute_numbers.py: Sigma = A'A + I = [[4,2,5],[2,7,4],[5,4,14]]; u = Sigma^-1 1 = (47/177,17/177,-3/59); "
    "s = 55/177; lambda = 177/55 = 3.2181...; w = (47/55,17/55,-9/55); Sigma w - lambda 1 = 0 exactly; f(w) = 177/110. "
    "The '36 of 36' counts: 6 directions with 1'd = 0 (sums checked) x 6 steps; identity holds algebraically since "
    "w'Sigma d = lambda 1'd = 0 (proof of Prop 3.2 (d), lines 133-135), so the count is consistent with the proof.")
row("M7a-L02-lab-prose", "2.5 claims about the lab output and its interpretation", "L02.html lines 150, 292, 311",
    "PASS",
    "Hypothesis (150): 'budget equals 1 exactly', 'residual zero', 'increase equals (1/2)t^2 d'Sigma d' match lines 288-291. "
    "Interpretation (292): values of Sigma, lambda, w and f(w) match; third weight negative is a short position (correct); "
    "'36 of 36' twice matches lines 290-291. Misconception 1 (311): Sigma w* - lambda 1 = 0 with lambda = 177/55 matches line 288.")
row("M7a-L02-theorem-2-2", "2.4 Theorem 2.2 and proof (necessity)", "L02.html lines 68-85", "PASS",
    "Re-derived: r = p - c g with c = p.g/g.g, r.g = 0, d = -r, p.d = -|r|^2 < 0 (line 81). Coordinate k with d_k != 0 "
    "chosen; curve gamma(t) = (x*_{-k}+t d_{-k}, phi(...)) is feasible by Assumption 1; gamma'(0) = d because g.d = 0 gives "
    "d_k = grad phi . d_{-k}; f(gamma(t)) = f(x*) + t p.d + o(t) gives a strictly better feasible point near x*, a contradiction. "
    "Hypotheses listed (75): U open, C^1, feasible, grad h != 0, local minimiser. Complete.")
row("M7a-L02-assumption-1", "2.4 named assumption (implicit function theorem)", "L02.html lines 67-70", "PASS",
    "Statement of the implicit function theorem (neighbourhood N, C^1 phi, phi(x*_{-k}) = x*_k, gradient formula "
    "-grad_{-k} h / d_k h) is the standard one. Stated as an assumption, not proved (line 69).")
row("M7a-L02-examples", "2.4 Examples 2.5, 2.6 and Prop 2.4", "L02.html lines 92-110", "PASS",
    "Example 2.5: h = y^2 - x^3, grad h(0) = 0, feasible set forces x >= 0, f = x >= 0 = f(0), grad f(0) = (1,0) not a multiple "
    "of 0. Example 2.6: grad h = (1,0), grad f(0,0) = (0,0) with lambda = 0; witness (0,-1) gives f = -1 < 0. Prop 2.4 "
    "uniqueness proof is correct.")
row("M7a-L02-prop-3-2", "2.4 Proposition 3.2 (a)-(d) and proof", "L02.html lines 121-136", "PASS",
    "Re-derived: Sigma u = 1 so u != 0 and s = u'Sigma u > 0 (a); budget (b); grad f = (Sigma+Sigma')w/2 = Sigma w (c); "
    "f(w) = f(w*) + w*'Sigma d + d'Sigma d/2 with w*'Sigma d = lambda 1'd = 0 (d). Hypotheses complete (line 124; no sign "
    "condition). Prop 3.3 proof correct.")
row("M7a-L02-problems-quiz", "2.4 problem solutions and quiz numerics", "L02.html lines 330-427, 445-529", "PASS",
    "M1 (1/2,1/2), lambda = 1; M2 (2/3,1/3), f = 1/3; M3 f(5/3,-2/3) = 11/6, increase 3/2 = (1/2) d'Sigma d; P3 f = lambda/2 = 1/(2s); "
    "E1 4*47/55 + 2*17/55 - 5*9/55 = 177/55 exactly; R3 minimum c^2/(2s), derivative c/s, = lambda at c=1 (recomputed). "
    "Quiz: lambda 0.6667; second coordinate 0.3333; A=(2) gives 5; 3.2182 (177/55 = 3.21818..., tolerance 0.00005 accepts it and "
    "rejects 3.2181); minimum value 0.3333; diag(5,-1) has trace 4 and is not PD (line 521). All correct.")
row("M7a-L02-misconceptions-canon", "2.9 misconceptions and canon", "L02.html lines 295-322", "PASS",
    "Canon bullets and three misconceptions re-checked against Examples 2.5, 2.6, Prop 3.2, Lab 1 numbers. Correct.")
row("M7a-L02-wording-theorem-applies", "2.4 wording precision", "L02.html line 118", "PASS",
    "'Theorem 2.2 applies to it under Assumption 1' is loose: the constraint h is not a minimiser. The intended claim (grad h = 1 != 0, "
    "so the regularity hypothesis holds for h) is correct. Non-blocking note.")
row("M7a-L02-notation", "2.4 notation", "L02.html", "PASS",
    "Local symbols: U, f, h, g = grad h, p, c, r, d, Sigma, u, s, lambda, w, A, gamma, phi. No registered symbol reused. "
    "\\operatorname{diag} (index.html lines 88, 115, 127) is a standard command; the registered \\diag has the same meaning, so no registered symbol is changed.")

# ---------- L03 ----------
row("M7a-L03-structure", "2.9 structure and minimums", "course/modules/M/M7/L03.html", "PASS",
    f"check_pages --page L03 PASS ({G}). Read all 556 lines. Order: why-it-matters (51, 95 words), sections 1-4, inline lab "
    "(155-306, before canon), canon (313-322, four bullets), misconceptions (324-340, three), problems (342-445, three per tier), "
    "key-results (447-463, seven rows), quiz (465-539, nine items), references (541-545). data-hours=10.")
row("M7a-L03-lab-run", "2.5 lab: run and twin identity", "L03.html 155-306; tests/labs/M7/lab-M7-L03-1.py", "PASS",
    "run_labs --page L03 PASS. check_labs.py: code == twin; twin exit 0 under python -I -W error, stderr empty; stdout == "
    "expected block (data-tolerance 1e-9, output is exact). ruff/mypy strict/pytest pass.")
row("M7a-L03-lab-numbers", "2.2 numbers printed by Lab 1", "L03.html lines 283-304", "PASS",
    f"{S}/recompute_numbers.py: active instance: grid minimum -1/2 at w1 = 1 (101 points); inactive: -1/4 at w1 = 1/2; candidate "
    "objectives equal; residuals exact zero (by the printed formulas); off-solution stationarity: grad f(1/2,1/2) + nu*1 - lambda = (0,13/10) + (-1/2,-1/2) - (0,3/10) = (-1/2, 1/2), as printed; "
    "flipped lambda2 gives dual residual 3/10.")
row("M7a-L03-lab-prose", "2.5 hypothesis, interpretation and comments", "L03.html lines 157, 255-256, 305", "PASS",
    "Hypothesis (157) predictions match lines 285-304 (residuals, grid minima, off-solution residual, dual residual 3/10). "
    "Comment (255-256): nu = mu1 - 2 = -1/2 and lambda2 = 1 - mu2 + nu = 3/10: recomputed. Interpretation (305): 101 points, "
    "'Theorem 2.1 gives the proof, because the data of (P_A) are convex' (Section 4 line 143). Consistent.")
row("M7a-L03-lemmas-thm", "2.4 Lemmas 1.4, 1.5 and Theorem 2.1 and proofs", "L03.html lines 77-114", "PASS",
    "Lemma 1.4: difference quotient argument correct; limit gives grad.(x-y) <= phi(x)-phi(y). Lemma 1.5: cross-term identity "
    "checked: coefficient of x'Sigma x is theta(1-theta)/2 on both sides; cross term -theta(1-theta) x'Sigma y on both sides; "
    "linear term cancels. Theorem 2.1: lambda_i g_i convex since lambda_i >= 0; affine h_j convex; sum convex; grad phi(x*) = 0 "
    "by K1; phi(x*) = f(x*) by K2, K4; phi(x) <= f(x) on F. Chain f(x) >= phi(x) >= phi(x*) = f(x*). Hypotheses listed (105) "
    "match the proof.")
row("M7a-L03-examples-sec4", "2.4 Examples 2.3, 3.1, 4.1, 4.2 and Remarks", "L03.html lines 121-153, 308-311",
    "PASS",
    "Example 2.3: f(-1/2) = -1/8 vs average -1/2 (convexity fails, -1/8 > -1/2). Example 3.1: grad g1(0) = 0 so K1 reads 1 = 0 "
    "(false). Example 4.1: grad f(1,0) = (1/2, 4/5); nu = -1/2; lambda2 = 3/10; p* = 1 - 3/2 = -1/2. Example 4.2: Sigma(1/2,1/2) = "
    "(3/2,3/2); grad f = (1/2,1/2); nu = -1/2; f = 3/4 - 1 = -1/4. Remark 4.3: Sigma^-1 = (1/3)[[2,-1],[-1,2]], w = (14/15,-11/30), "
    "sum 17/30 (matches). Sigma-form identity (a,b)Sigma(a,b)' = a^2+b^2+(a+b)^2 (line 143) correct.")
row("M7a-L03-open-item-proof", "2.4 theorem without proof or citation (Open item 3.2)",
    "L03.html lines 133-136 (block), 318, 431-441, 458, 543", "FAIL",
    "Open item 3.2 is a theorem-form assertion (KKT necessity under Slater's condition: 'then there exist lambda and nu such that "
    "(x*, (lambda, nu)) is a KKT point', line 135) with no proof, no sketch and no data-cite or locator. The page says so: "
    "'not proved, sketched or graded on this page, and no source has been read for it' (135). It is load-bearing: canon bullet 2 "
    "(318), R2 (431-436: 'the conclusion of Open item 3.2 fails') and R3 (439-441) rely on it. BUILDER_RULES 3.3 requires each "
    "theorem to have a complete proof or a precise data-cite plus locator; VERIFIER_RULES 2.4 requires the proof complete or "
    "precisely cited. Neither holds, and I could not read a source to supply a locator (UNVERIFIABLE).",
    "Remove the theorem form. Replace the block (133-136) with one sentence stating that the converse direction, KKT necessity "
    "under Slater's condition, is not treated on this page. Rewrite canon bullet 2 (318) to rest only on Example 3.1, and rewrite "
    "R2 (431-436) and R3 (439-441) to refer to Example 3.1's direct computation (no appeal to an unproved conclusion). Key-results "
    "row 458 then becomes a statement of scope, not a graded claim. Alternatively, prove the necessity direction on the page "
    "with every hypothesis (note it needs a separating-hyperplane argument not in the M7 closure) or cite a source whose locator "
    "the builder has read.")
row("M7a-L03-open-item-wording", "2.9 process and deferral wording in learner text (BUILDER_RULES 1.3, process words)",
    "L03.html lines 134, 135, 318, 431, 432, 439, 458, 504, 516, 543", "FAIL",
    "'Open item 3.2' is a tracking label from the planning files (plans/M7-open-items.md) and appears 12 times in L03 (grep -c count of occurrences 12) in learner-facing "
    "text, together with the process-style sentence 'no source has been read for it' (135, 543). It reads as a deferral, which "
    "BUILDER_RULES 1.3 bans, and a learner cannot act on it. Quiz item at 516 asks which hypothesis of 'Open item 3.2' fails.",
    "Delete the label with the fix in the previous row. Any statement that remains must be named by its content (for example "
    "'KKT necessity under Slater's condition is not treated here'), with no 'Open item' or 'no source has been read' wording. "
    "Quiz item 516 must be rewritten to ask about the hypothesis of Slater's condition in Example 3.1 directly.")
row("M7a-L03-R-and-misconceptions", "2.4 problem solutions, misconceptions and quiz numerics", "L03.html lines 329-337, 346-445, 465-539",
    "PASS",
    "M1: min x^2+y^2 with 1-x-y <= 0 gives (1/2,1/2), lambda = 1, p* = 1/2; M2: f(3/5,2/5) = 19/25 - 1 = -6/25 = -0.24 > -0.25 = -1/4 (recomputed); "
    "M3: grad f = (0,13/10), nu = 0 forced, no multiplier, value -1/10; P1 convexity of lambda g and concavity for lambda<0 "
    "(x=1,y=-1: midpoint 0, average -1); P2 gradient inequality identity (x-y)^2; P3 f(w) >= -1/2 + (3/10) w2; E1 norm sqrt(1/2) = 0.7071; "
    "E2 101 points; E3 -1/4; R1 -x^2 max at 0; R2 Slater fails only; R3. Quiz: lambda2 = 0.3, nu = -0.5, -0.25, multipliers (0,0), "
    "dual feasibility, complementary slackness, f(-1) < f(0) for x^3. Misconception 2 (333): slack constraint w1>=0 with multiplier 0 and binding w2>=0 with 3/10 (matches Examples 4.1, 4.2); "
    "misconception 3 (337): Remark 4.3 point (14/15,-11/30) with sum 17/30 (matches). Misconception 1 (329): Example 2.3 and R1 values (matches).")
row("M7a-L03-notation", "2.4 notation", "L03.html", "PASS",
    "Local symbols: F (feasible set), f, g_i, h_j, L (Lagrangian), phi, Sigma, mu (given vector in Section 4, not the eigenvalue mu of "
    "L01), lambda, nu, p*, d, r. Registered symbols not used with other meanings. \\R macro is registered and renders "
    "(page_smoke).")
row("M7a-L03-cross-lesson", "2.9 cross-lesson references", "L03.html lines 37, 102, 320; L01.html line 102; L02.html line 37",
    "PASS",
    "L03 uses Lemma 1.5 and Theorem 2.1 (its own), cites L01 Definition 2.1 and Lesson 2 multiplier by backward links (verified by the link "
    "checker). L01 line 102 'Theorem 2.1' refers to L03 Theorem 2.1 (exists, line 103). L03 line 320: 'Finding the active set ... "
    "is the subject of Lesson 5': L05 enumerates active sets for an inequality QP (L05.html lines 130, 179, 323). Accurate.")

row("M7a-DAG-links-pages", "2.9 link and anchor integrity", "index.html, L01-L03 (local hrefs and concepts.html#ids)", "PASS",
    "Script check: every local href to a .html file exists and every #fragment exists in the target (including concepts.html ids). "
    "No duplicate ids on the four pages.")
row("M7a-plan-compliance", "plan section 8 and architect decisions B1, B2, Q1-Q6, Q12",
    "plans/M7-build-plan.md sections 4, 6, 8, 9; index.html; L01-L03", "PASS",
    "Hours 9/9/10 and hub split match plan section 4. Concept ownership matches the plan's table. Architect Q12 (undeclared terms "
    "are prose): dynamic programming, efficient frontier, covariance matrix, contraction mapping appear as prose only. Q3 "
    "(objective (gamma/2) w'Sigma w - mu'w) is stated in section 4 (line 143 uses gamma = 1). Q9 registry keys cited as keys, "
    "no locator. No Atlas milestone, no data files.")

summary = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": sum(1 for r in rows if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
}
fragment = {
    "unit": "M7",
    "slice": "a",
    "round": 6,
    "verifier": "independent verifier (Haiku), round 6, fresh context, no builder context; previous fragment not on disk, so every row was re-verified from scratch",
    "pin": "44f1eb6",
    "base": "none (B-M7-a.round5.json absent from /Users/billyribeiro/.fanout/frags/; no carry-forward)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB6-M7-a",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB6-M7-a/ledgers/M7/scripts/M7-a-r6",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "stokey1989recursive: the record has three authors (Stokey, Lucas, Prescott); the curriculum string is 'Stokey & Lucas'. The pages cite the record and say so. No registry change requested."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice a is not a project slice, so no mutants and no alternative implementations are required (VERIFIER_RULES 2.6 does not apply).",
        "Not checked: a live Crossref re-resolution (verify_refs --unit needs a live run; I ran verify_refs --offline only, 560 entries, 0 problems). Boyd & Vandenberghe and Stokey, Lucas & Prescott were not read, and the pages claim no locator from them, so no attribution row depends on the books.",
        "Not checked: the full M7 gate (only the slice's commands were run, per the rules). Pyodide timing was taken from page_smoke, not from a quiet machine.",
        "The '36 of 36' counts in Lab 1 of L02 were confirmed by the twin run and by the algebraic identity, not by an independent enumeration in my own script.",
        "Non-blocking wording notes (no FAIL): L02.html line 118 'Theorem 2.2 applies to it' (loose); index.html line 65 says Lesson 2 uses positive semidefinite matrices where it requires positive definite.",
        "Tools run (see run_gates_output.txt): run_labs --page L01/L02/L03 (PASS), check_pages --unit M7 and per page (PASS), check_dag --unit M7 (PASS), ruff check and format and mypy --strict on the three twins (PASS), pytest tests/test_labs.py -k 'M7 and (L01 or L02 or L03)' (3 passed), verify_refs --offline (0 problems), check_projects --unit M7 (PASS, unit level), page_smoke --pages index L01 L02 L03 (PASS).",
        "Scripts backing rows: ledgers/M7/scripts/M7-a-r6/check_labs.py, recompute_numbers.py, run_gates.sh, run_gates_output.txt, page_smoke_out.txt, build_fragment.py.",
    ],
    "summary": summary,
}
out = ROOT / "ledgers/M7/M7-a.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(summary))
