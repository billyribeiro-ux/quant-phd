import json, sys
sys.path.insert(0, "tools")
import ledger  # noqa: E402

PIN = "ce7b382"
PREV = "7aa909e"
C = "Carried from round 7 (course/modules/M/M7/%s byte-identical since the previous pin 7aa909e):"
rows = []

def row(rid, check, location, status, evidence):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})

# ---- hub (index.html byte-identical since 7aa909e; twins L01-L03 byte-identical) ----
hub_carry = [
 ("M7a-hub-structure","2.9 structure: hub sections and minimums","course/modules/M/M7/index.html (whole file)"),
 ("M7a-hub-hours","2.9 hours split arithmetic","index.html data-hours-lessons, data-hours-project, card-kicker L01-L08; L01-L08 data-hours (L01 9, L02 9, L03 10 unchanged)"),
 ("M7a-hub-placement-numbers","1 numbers in prose and numeric items","index.html lines 73, 75-135"),
 ("M7a-hub-placement-explanations","2.2 attributions in placement explanations","index.html lines 88-124"),
 ("M7a-hub-cross-refs","2.9 cross-references to other lessons and project","index.html lines 156-161, 176; project.html lines 44-55"),
 ("M7a-hub-covariance-disclaimer","2.4 / plan B1 disclaimer","index.html line 167"),
 ("M7a-hub-attributions-registry","2.1 attribution and registry fields","index.html lines 170-177; L01.html 548-551; L02.html 531-535; L03.html 541-545 (no changed hunk in these lines)"),
 ("M7a-hub-data-simulated","2.8 data and SIMULATED labels","index.html lines 37, 167; L01.html 165; L02.html 157; L03.html 140, 159"),
 ("M7a-hub-prereq-prose","2.9 prose accuracy","index.html line 65"),
 ("M7a-hub-lede-kkt-scope","2.9 prose accuracy","index.html line 30 (lede), line 49"),
 ("M7a-hub-l04-claims","2.9 claims about lessons","index.html line 52 and line 146 (card L04)"),
 ("M7a-hub-lede-claims","2.9 claims about lessons","index.html line 141"),
]
for rid, chk, loc in hub_carry:
    row(rid, chk, loc, "PASS", "Carried from round 7 (course/modules/M/M7/index.html byte-identical since the previous pin 7aa909e; cited lines of L01-L04 unchanged except the hunks listed in notes): round-7 evidence stands. Re-checked this round: the index.html lesson-map and card text describing L01-L03 (lines 35, 65, 115, 143-145) names no changed passage (no Slater, triangle or Section-3 reference).")

row("M7a-hub-placement-explanations-x", "placeholder", "placeholder", "PASS", "placeholder")  # removed below
rows.pop()

row("M7a-hub-page-smoke","2.9 page_smoke: console, math, external requests, 360 px","index.html, L01.html, L02.html, L03.html",
    "PASS","FRESH this round at ce7b382: `page_smoke.py --unit M7 --pages modules/M/M7/index.html modules/M/M7/L01.html modules/M/M7/L02.html modules/M/M7/L03.html` exit 0, 'page_smoke M7: PASS' (ledgers/M7/scripts/M7-a-r8/page_smoke_hub_L01-03.txt).")
row("M7a-hub-banned-phrases","2.9 banned phrases (BUILDER_RULES 1.3-1.4)","index.html; L01.html; L02.html; L03.html",
    "PASS","FRESH: `check_pages.py --unit M7` exit 0, 'check_pages M7: PASS' (ledgers/M7/scripts/M7-a-r8/check_pages_unit_M7.txt) includes the banned-string scan of the changed prose. Grep for process/deferral words (Open item, deferred, TODO, not yet, next lesson) in L01-L03: no hit in learner text.")
row("M7a-DAG-links-pages","2.9 link and anchor integrity","index.html, L01-L03 (local hrefs and concepts.html#ids)",
    "PASS","FRESH: `check_dag.py --unit M7` exit 0, 'check_dag M7: PASS' (ledgers/M7/scripts/M7-a-r8/check_dag_M7.txt). Hrefs in the changed hunks are unchanged (L03 line 37 links L01.html#def-convex-function and L02.html#def-lagrange-multiplier; both anchors still exist: L01 line 82, L02 line 63).")
row("M7a-plan-compliance","plan section 8 and architect decisions B1, B2, Q1-Q6, Q12","plans/M7-build-plan.md section 4 and section 8 item 6 (Slater as hypothesis); index.html; L01-L03",
    "PASS","Re-read at this round: Slater's condition is stated only as the missing hypothesis of the converse direction (L03 line 133, line 315) and never as a hypothesis of Theorem 2.1 (L03 line 105; Remark 2.2 line 118 lists the four conditions, convexity and differentiability, affineness). The section renamed at L03 line 126 ('An optimum with no multipliers') does not conflict with the plan. Architect decisions B1/B2 concern the hub and DAG, unchanged.")

# ---- L01 ----
row("M7a-L01-why-it-matters","2.9 prose accuracy","L01.html line 51",
    "PASS","FRESH (changed hunk). New text: 'proves its results apart from the spectral theorem (Assumption 1 below), takes the triangle inequality as known'. Checked against the page: the triangle inequality is used without proof in Examples 1.2 (line 62) and 2.2 (line 89) and is disclosed; Assumption 1 (line 129-130) is the only named unproved fact of Proposition 3.2 (iii); Lemma 3.1 (line 111) and Propositions 1.3 (line 68), 2.3 (line 94), 3.2 (i)-(ii) (lines 136-147) are proved on the page. Residual note: R3 solution (line 440) states the trace and determinant of a 2 by 2 symmetric matrix as the sum and product of its eigenvalues (Vieta on the characteristic polynomial); this is elementary algebra, not an assumed result, and is not a FAIL.")
row("M7a-L01-structure","2.9 structure and minimums","course/modules/M/M7/L01.html (whole file)",
    "PASS","FRESH: check_pages --unit M7 PASS (L01 line 2 data-page L01, data-hours 9; header, grade legend, Definitions 1.1/2.1, Propositions 1.3/2.3/3.2, Lemma 3.1, Example, Assumption, Lab, canon-breaks, misconceptions (3), problem set (9 problems in 3 tiers), key-results table, quiz (11 items), references, complete button). page_smoke PASS.")
row("M7a-L01-lab-run","2.5 lab: run and twin identity","L01.html lab section lines 157-310; tests/labs/M7/lab-M7-L01-1.py",
    "PASS","FRESH: `run_labs.py --unit M7 --page L01` PASS (1/1) at ce7b382 (ledgers/M7/scripts/M7-a-r8/run_labs_L01-03.txt); twin byte-identical to pin (git diff --quiet); ruff check and ruff format --check PASS on the twin; mypy --no-incremental PASS; pytest tests/test_labs.py -k M7 PASS.")
row("M7a-L01-lab-numbers","2.2 numbers printed by Lab 1","L01.html lines 295-308 (expected block); tests/labs/M7/lab-M7-L01-1.py",
    "PASS","FRESH: independent script (ledgers/M7/scripts/M7-a-r8/rederive_r8.py, stdlib-free numerics, own code): Q1 chord 3125 of 3125; Q2 chord 2573 of 3125; Q2 negative ordered pairs 184; 3*184=552=3125-2573; gap at (1,0),(0,1), 1/2 for Q2 is -1/2; eigenvalues Q1 {3,1}, Q2 {3,-1}; Hessian eigenvalues 6,2 and 6,-2. All match the expected block.")
row("M7a-L01-lab-prose","2.5 hypothesis, interpretation and comments","L01.html lines 159, 309, 319, 332, 336",
    "PASS", C % "L01.html lines 159, 309, 319, 332, 336 (carried)" + " the lab text is unchanged; the statements re-read this round: 'Q2 fails 552 of them' (309) = 3125-2573 (336), 'prints the eigenvalue -2 of Hessian 2Q2' (332) matches the expected block line 306, 'a finite check' (319) is correct.")
row("M7a-L01-lemma-3-1","2.4 Lemma 3.1 identity and proof","L01.html lines 108-121",
    "PASS", C % "L01.html lines 108-121" + " re-derived this round: expansion gives lambda q(x)+(1-lambda)q(y)-q(z) = lambda(1-lambda)(q(x)+q(y)-2x'Qy) = lambda(1-lambda)(x-y)'Q(x-y) using symmetry; no restriction on lambda.")
row("M7a-L01-props","2.4 Propositions 1.3, 2.3, 3.2 and proofs","L01.html lines 66-148",
    "PASS", C % "L01.html lines 66-148 (the only changed line in L01 is 51)" + " re-checked: Prop 3.2 (i)=>(ii) uses y=0, lambda=1/2 giving q(x)/4; (ii)=>(i) uses Lemma 3.1; (ii)=>(iii) uses x=V e_i; all steps verified.")
row("M7a-L01-examples","2.2 numbers in Examples 1.2, 2.2, 3.2a, 3.3","L01.html lines 61-63, 88-89, 124-125, 153-154",
    "PASS", C % "L01.html lines 61-63, 88-89, 124-125, 153-154" + " re-derived: Q1 eigenvalues 3 and 1 via (1,1),(1,-1); Q2 eigenvalues 3 and -1; Hessian 2Q; midpoint (1/2,1/2) of circle points has squared norm 1/2.")
row("M7a-L01-problems","2.4 problem-set solutions and numbers","L01.html lines 345-444",
    "PASS", C % "L01.html lines 345-444" + " re-derived this round: M1, M2 (f(0)=0, chord 1, difference 1), M3 (q(1,1)=6, gap 6, (2,2)Q1(2,2)=24), P1 (x=2,-2, midpoint 0), P2, P3 (q(v)=mu|v|^2), E1 (184 pairs, 3*184=552), E2, E3 (6,2 halved to 3,1), R1 (x'Qx=x1^2+x2^2), R2, R3 ((a+c)=4, ac-b^2=3 for Q1). All hold.")
row("M7a-L01-key-results-grades","2.3 grades","L01.html lines 67, 93, 109, 134, 452-456",
    "PASS", C % "L01.html lines 67, 93, 109, 134, 452-456" + " grades T for Props 1.3, 2.3, 3.2 and Lemma 3.1 are proved on the page (the (iii) part is stated under Assumption 1 in the row, line 456).")
row("M7a-L01-quiz","2.9 retrieval quiz (11 items)","L01.html lines 462-546",
    "PASS", C % "L01.html lines 462-546" + " re-derived: L01q3 smaller eigenvalue 1; L01q5 gap -1/2; L01q6 3125; L01q9 -2 for x=(1,-1); each explanation consistent with the page.")
row("M7a-L01-canon-misconceptions","2.9 canon and misconceptions","L01.html lines 313-339",
    "PASS", C % "L01.html lines 313-339" + " re-read: the four canon points and three misconceptions agree with Example 1.2, Example 3.3 and Lab 1 counts (2573, 552).")
row("M7a-L01-notation","2.4 notation (BUILDER_RULES 3; notation/notation.json)","L01.html (whole file)",
    "PASS","FRESH for the changed hunk (line 51 introduces no symbol). notation/notation.json lists 8 symbols (T, gamma_3, gamma_4, ...); none of the M7 symbols Q, q, V, Lambda, mu_i, H, L_c is registered, so no registry conflict. Observation (not a FAIL under rule 13 as written): mu denotes an eigenvalue in L01 (line 130, 440), a Lagrange multiplier in L02 Prop 2.4 (line 104) and a return/linear-term vector in L03 (line 139); see notes.")

# ---- L02 ----
row("M7a-L02-structure","2.9 structure and minimums","course/modules/M/M7/L02.html (whole file)",
    "PASS","FRESH (changed hunks lines 63 and 89): check_pages PASS; page_smoke PASS; header, Definition 2.1, Assumption 1, Theorem 2.2, Remark 2.3, Examples 2.5 and 2.6, Prop 2.4, Section 3 (Prop 3.2, 3.3), lab, canon-breaks, misconceptions (3), problem set (9 problems), key-results (5 rows), quiz (9 items), references.")
row("M7a-L02-lab-run","2.5 lab: run and twin identity","L02.html lab section 148-293; tests/labs/M7/lab-M7-L02-1.py",
    "PASS","FRESH: run_labs --page L02 PASS (1/1); twin byte-identical to pin; ruff/mypy/pytest M7 PASS.")
row("M7a-L02-lab-numbers","2.2 numbers printed by Lab 1","L02.html lines 279-291",
    "PASS","FRESH: independent script: seed-1 LCG entries [1,2,3,1,-1,2,-1,-1,0]; Sigma = [[4,2,5],[2,7,4],[5,4,14]]; 1'Sigma^-1 1 = 55/177; lambda = 177/55; w = (47/55, 17/55, -9/55); Sigma w - lambda 1 = 0 exactly; f(w) = 177/110. All match the expected block; lambda rounds to 3.2182 (3.21818...).")
row("M7a-L02-lab-prose","2.5 claims about the lab output and its interpretation","L02.html lines 150, 292, 311",
    "PASS", C % "L02.html lines 150, 292, 311" + " re-read: the 36 of 36 counts (line 290-291) are exact over 6 directions and 6 steps; line 311 misconception residual claim matches the expected block line 288.")
row("M7a-L02-theorem-2-2","2.4 Theorem 2.2 and proof (necessity); Remark 2.3","L02.html lines 68-85 (Theorem 2.2 and proof, carried); Remark 2.3 at line 89 (changed)",
    "PASS","Theorem 2.2 and proof: carried from round 7 (lines 68-85 byte-identical). Changed Remark 2.3 (line 89) re-verified: 'For each prescribed tangent d ... the proof constructs a feasible curve through x* with that tangent'. The written proof fixes d = -r, but the construction uses only g.d = 0 (d_k = grad phi . d_{-k}, line 83), so the same construction works for every d in the tangent space; the remark's generalisation is correct. Minimality argument unchanged.")
row("M7a-L02-assumption-1","2.4 named assumption (implicit function theorem)","L02.html lines 67-70",
    "PASS", C % "L02.html lines 67-70" + " the Assumption text is the same statement used in the proof at line 83; not proved on the page and labelled as such (line 69).")
row("M7a-L02-examples","2.4 Examples 2.5, 2.6 and Prop 2.4","L02.html lines 92-110",
    "PASS", C % "L02.html lines 92-110" + " re-checked: Example 2.5 (f=x, h=y^2-x^3, minimizer at 0, no multiplier); Example 2.6 (f=y^3, h=x, lambda=0, (0,-1) gives -1 < 0); Prop 2.4 proof. The term 'stationary' used at line 98 is now defined at line 63, before use.")
row("M7a-L02-prop-3-2","2.4 Proposition 3.2 (a)-(d) and proof","L02.html lines 121-136",
    "PASS", C % "L02.html lines 121-136" + " re-derived: s = u'Sigma u > 0; w* budget 1; gradient Sigma w* = lambda 1; f(w)-f(w*) = (1/2) d'Sigma d with 1'd = 0 and w*'Sigma d = lambda 1'd = 0.")
row("M7a-L02-problems-quiz","2.4 problem solutions and quiz numerics","L02.html lines 330-427, 445-529",
    "PASS", C % "L02.html lines 330-427, 445-529" + " re-derived: M2 f=1/3 at (2/3,1/3); M3 increase 3/2; E1 first coordinate 177/55; quiz 0.6667, 0.3333, 3.2182 (|3.21818-3.2182| < 0.00005), 0.3333 minimum value.")
row("M7a-L02-misconceptions-canon","2.9 misconceptions and canon","L02.html lines 295-322",
    "PASS", C % "L02.html lines 295-322" + " re-read: the stationarity-not-sufficient point agrees with Example 2.6 and the 'stationary' definition at line 63.")
row("M7a-L02-wording-theorem-applies","2.9 prose accuracy","L02.html line 118",
    "PASS", C % "L02.html line 118" + " 'Under Assumption 1, Theorem 2.2 applies to every local minimizer of f on the budget set' is consistent with the regularity check grad h = 1 != 0.")
row("M7a-L02-notation","2.4 notation","L02.html (whole file)",
    "PASS","FRESH for the changed hunk: line 63 introduces the term 'stationary' (defined in the same sentence, with <em>), not a symbol. Symbols Sigma, mu-free, lambda, nabla, 1 are used consistently with Definition 2.1 and Prop 3.2. No registry symbol conflict (notation.json). Observation: L02 Prop 2.4 uses mu as a second multiplier (see notes).")

# ---- L03 ----
row("M7a-L03-why-and-limits","2.9 prose accuracy","L03.html line 7 (meta description, changed); line 51 (why-it-matters); lines 314-316 (limits bullets)",
    "PASS","FRESH for the changed meta description (line 7): 'Sufficiency under convexity is proved' (Theorem 2.1 with proof, lines 103-114); 'An example has an optimum with no KKT point, and Slater's condition fails there' (Example 3.1, lines 128-131: no feasible point with x^2<0); 'A two-asset problem is solved and checked exactly in Lab 1' (lines 136-153, 155-303). Why-it-matters (line 51) and limits bullets (314-316) carried: unchanged and consistent with Example 2.3 and Example 3.1.")
row("M7a-L03-structure","2.9 structure and minimums","L03.html (whole file)",
    "PASS","FRESH (changed hunks lines 7, 118, 126, 438, 501, 519): check_pages PASS; page_smoke PASS; header, Definitions 1.1/1.2, Remark 1.3, Lemmas 1.4/1.5, Theorem 2.1, Remark 2.2, Examples 2.3, 3.1, 4.1, 4.2, Remark 4.3, lab, canon-breaks, misconceptions (3), problems (9), key-results (7), quiz (9), references.")
row("M7a-L03-lab-run","2.5 lab: run and twin identity","L03.html lab section 155-306; tests/labs/M7/lab-M7-L03-1.py",
    "PASS","FRESH: run_labs --page L03 PASS (1/1); twin byte-identical to pin; ruff/mypy/pytest M7 PASS.")
row("M7a-L03-lab-numbers","2.2 numbers printed by Lab 1","L03.html lines 283-304 (expected block 280-301)",
    "PASS","FRESH: independent script: active instance grid min -1/2 at w1=1; inactive grid min -1/4 at w1=1/2 (101 points); f(1,0) = -1/2; f(1/2,1/2) = -1/4 inactive and -1/10 active (M3); Remark 4.3 unconstrained stationary point (14/15, -11/30), weights sum 17/30. Expected block matches.")
row("M7a-L03-lab-prose","2.5 hypothesis, interpretation and comments","L03.html lines 157, 255-256, 305",
    "PASS", C % "L03.html lines 157, 255-256, 305 (carried; the lab hypothesis is at line 154 and interpretation at 302)" + " re-read: predicted values match the expected block (-1/2, -1/4, residual (-1/2, 1/2), dual residual 3/10).")
row("M7a-L03-lemmas-thm","2.4 Lemmas 1.4, 1.5 and Theorem 2.1 and proofs","L03.html lines 77-114",
    "PASS", C % "L03.html lines 77-114" + " re-derived: Lemma 1.5 cross-term check (-theta(1-theta) x'Sigma y on both sides); Theorem 2.1 chain f(x) >= phi(x) >= phi(x*) = f(x*). Only line 118 (Remark 2.2) changed in this region, verified separately.")
row("M7a-L03-examples-sec4","2.4 Examples 2.3, 3.1, 4.1, 4.2 and Remarks","L03.html lines 121-153, 308-311; heading line 126 (changed)",
    "PASS","FRESH for the changed heading (line 126 'An optimum with no multipliers', consistent with the Example 3.1 title on line 129 and with Remark 2.2 'Example 3.1 (Section 3)'). Example 3.1 (lines 128-131): f=x, g1=x^2, F={0}, (K1) reads 1 + lambda_1 * 0 = 0; Slater fails (no x with x^2<0). Example 4.1: grad f = (1/2, 4/5), nu = -1/2, lambda_2 = 3/10, f* = -1/2. Example 4.2: grad f = (1/2,1/2), nu = -1/2, f* = -1/4. Example 2.3: f(-1) = -1 < 0 = f(0); midpoint -1/8 > chord -1/2. Remark 4.3 values re-derived. Carried for lines 121-125 and 140-153 (unchanged).")
row("M7a-L03-open-item-proof","2.4 theorem without proof or citation (Open item 3.2)","L03.html lines 126-133",
    "PASS","FRESH: the open item was removed in round 6->7 and remains removed. Example 3.1 is proved by direct computation (F = {0}, (K1) fails), and the converse direction is stated as not treated on this page (line 133), with no unproved claim presented as a result.")
row("M7a-L03-open-item-wording","2.9 process and deferral wording in learner text (BUILDER_RULES 1.3, 1.4)","L03.html lines 126-133, 318, 431-441, 458, 504-543",
    "PASS","FRESH on the changed lines (R3 solution line 438; quiz explanations lines 501 and 519): no process or deferral words; 'Slater's condition also fails there' and 'the optimum has no KKT point because (K1) reads 1 = 0' are statements about the example. Carried for lines 318, 458, 504-543: unchanged.")
row("M7a-L03-R-and-misconceptions","2.4 problem solutions, misconceptions and quiz numerics","L03.html line 438 (R3 solution); line 519 (quiz L03q7 explanation); lines 326-339 (misconceptions, carried)",
    "PASS","Round-7 FAIL re-verified and FIXED. Line 438 now says Example 3.1 has 'no multiplier ... because the gradient grad g_1(0) is zero, which makes (K1) false for every multiplier. Slater's condition also fails there', which attributes the failure of (K1) to grad g_1(0) = 0 (line 130) and does not claim Slater's failure as the cause. Line 519 now reads 'Slater's condition fails there, since no strictly feasible point exists; the optimum has no KKT point because (K1) reads 1 = 0 (Example 3.1)', which is consistent with line 130. R1 (line 424) and R2 (line 431) re-verified: correct. Misconceptions (326-339) re-checked: correct.")
row("M7a-L03-notation","2.4 notation","L03.html (whole file)",
    "PASS","FRESH for the changed hunks: Remark 2.2 (line 118) and quiz/R3 text use only existing symbols (f, g_i, h_j, Sigma, lambda_i, nu_j, nabla); no new symbol. Observation: mu is the return vector of (P_A) (line 139), and in L03 Example 4.1 mu = (3/2, 1/5); see notes on mu.")
row("M7a-L03-cross-lesson","2.9 cross-lesson references","L03.html lines 37, 102, 320; L01.html line 102; L02.html line 37",
    "PASS", C % "L03.html lines 37, 102, 320; L01.html line 102; L02.html line 37" + " (no changed hunk in these lines; the Section 3 rename at line 126 is referenced by Remark 2.2 as 'Section 3' and that reference is correct).")
row("M7a-L03-remark-2-2","2.4 Theorem 2.1 hypotheses versus the Remark that claims them complete","L03.html line 118 (Remark 2.2 text), lines 104-110 (Theorem 2.1 and proof)",
    "PASS","Round-7 FAIL re-verified and FIXED. Remark 2.2 now lists 'the convexity and differentiability of f and of the g_i, and the affineness of the h_j'. Theorem 2.1 (line 105) requires differentiability and the proof uses Lemma 1.4 (line 110), which needs differentiability; the listed hypotheses now cover everything the proof uses. The h_j are affine hence differentiable; the four conditions are the remaining inputs. 'It does not use any hypothesis beyond these' is now correct.")

row("M7a-hub-dag-concepts","2.9 / DAG: concept links and definitions","index.html; L01.html; L02.html; L03.html; check_dag --unit M7",
    "PASS","FRESH: check_dag.py --unit M7 PASS (ledgers/M7/scripts/M7-a-r8/check_dag_M7.txt). Changed hunks add no concept link; L02 line 63 adds <em>stationary</em> (not a concept). L03 meta-row links resolve to L01 line 82 and L02 line 63 anchors.")

notes_r8 = [
 "Slice a is not a project slice: no mutants and no alternative implementations required (VERIFIER_RULES 2.6 does not apply); mutants list is empty by design, as in rounds 6 and 7.",
 "Delta reviewed: git diff 7aa909e..ce7b382 for index.html (byte-identical), L01-L03 (hunks at L01 line 51; L02 lines 63, 89; L03 lines 7, 118, 126, 438, 501, 519) and tests/labs/M7 L01-L03 twins (byte-identical). Every changed hunk was read and re-verified. Rows whose cited lines have no hunk are carried with the round-7 prefix; rows whose subject changed were re-run or re-derived this round.",
 "Round-7 FAIL rows M7a-L03-R-and-misconceptions and M7a-L03-remark-2-2 are resolved and re-verified from scratch.",
 "Observation for the architect (not a row FAIL): the symbol mu is used with three meanings in M7 (eigenvalue in L01 lines 130, 440; Lagrange multiplier in L02 Prop 2.4 line 104; return / linear-term vector of (P_A) in L03 lines 139-140). notation/notation.json registers none of these, so rule 13 as written is not triggered; the unit could use a different letter for one of them.",
 "Observation: the L03 quiz item L03q7 asks which condition fails and marks Slater's condition. The cause (grad g_1(0) = 0 makes (K1) false) is now stated in R3 and in the key-results row, and the quiz wording is consistent with that.",
 "Observation: R3 solution in L01 (line 440) uses trace = mu1+mu2 and determinant = mu1*mu2 for a 2 by 2 symmetric matrix without naming them; these follow from the characteristic polynomial (elementary), so the 'proved apart from the spectral theorem' sentence stands.",
 "Registry flag carried: stokey1989recursive citation string versus three-author record (round 7 flag). Not changed in this slice.",
 "Not verified in this slice: course/modules/M/M7/cards.json (changed in the delta, outside slice a), L04-L08, project.html, grader and lab twins L04-L08, check_projects, pytest beyond the M7 lab tests.",
 "Note: `check_pages.py --unit M7 --page index` is not a valid hub check (it treats index.html as a lesson); the hub is checked by `--unit M7`, which PASSes.",
]

# ---- DAG / plan rows already included above ----
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
rows_out = rows

frag = {
  "unit": "M7", "slice": "a", "round": 8,
  "verifier": "independent verifier (Haiku), round 8, fresh context, no builder context",
  "pin": PIN, "base": PREV + " (round 7 pin; B-M7-a.round7.json used as context only)",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-M7-a",
  "scratch": "/Users/billyribeiro/.fanout/wt/verifyB8-M7-a/ledgers/M7/scripts/M7-a-r8",
  "verified_at": "2026-10-28",
  "verdict": None,
  "rows": rows_out,
  "mutants": [],
  "registry_flags": ["stokey1989recursive: the record has three authors (Stokey, Lucas, Prescott); the hub and curriculum cite 'Stokey & Lucas'. Carried from round 7; no registry change requested in this slice."],
  "freshness_flags": [],
  "notes": notes_r8,
  "summary": None,
}
n_pass = sum(r["status"] == "PASS" for r in rows_out)
n_fail = sum(r["status"] == "FAIL" for r in rows_out)
frag["verdict"] = "PASS" if n_fail == 0 else "FAIL"
frag["summary"] = {"rows": len(rows_out), "pass": n_pass, "fail": n_fail, "unverifiable": 0}
json.dump(frag, open("ledgers/M7/M7-a.json", "w"), ensure_ascii=False, indent=1)
print(frag["summary"], frag["verdict"])
