"""Write the round-4 SC1-a ledger fragment (ledgers/SC1/SC1-a.json) from the rows judged in this round.

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r4/build_fragment.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
O = "ledgers/SC1/scripts/SC1-a-r4/out/"
S = "ledgers/SC1/scripts/SC1-a-r4/"
rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates (commands run at 9a02b1a; outputs under out/)
row("SC1a-gate-check-pages", "2.9-structure-tool", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "PASS",
    f"tools/check_pages.py --unit SC1 at 9a02b1a printed 'check_pages SC1: PASS', exit 0 ({O}check_pages.txt).")
row("SC1a-gate-check-dag", "2.9-dag-tool", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "PASS",
    f"tools/check_dag.py --unit SC1 printed 'check_dag SC1: PASS', exit 0 ({O}check_dag.txt).")
row("SC1a-gate-run-labs", "2.5-labs-run", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "PASS",
    f"tools/run_labs.py --unit SC1: 'run_labs SC1: PASS (11/11)', exit 0 ({O}run_labs_unit.txt); --page L01, L02, L03 each "
    f"'PASS (1/1)', exit 0 ({O}run_labs_L01.txt, run_labs_L02.txt, run_labs_L03.txt).")
row("SC1a-gate-page-smoke", "2.9-page-smoke", "index.html, L01.html, L02.html, L03.html", "PASS",
    f"tools/page_smoke.py --unit SC1 --pages index L01 L02 L03, run alone on the quiet checkout: 'page_smoke SC1: PASS', "
    f"exit 0; lab times 0.0 s, 0.2 s, 0.1 s; boot 1.1 s ({O}page_smoke.txt).")
row("SC1a-gate-lint-types-tests", "2.5-ruff-mypy-pytest",
    "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py; pytest -k SC1", "PASS",
    f"ruff check on the three twins: 'All checks passed!' exit 0 ({O}ruff_check.txt); ruff format --check: '3 files already "
    f"formatted' exit 0 ({O}ruff_format.txt); mypy --no-incremental on the three twins: 'Success: no issues found in 3 source "
    f"files' exit 0 ({O}mypy.txt); pytest -q -k SC1: 11 passed, exit 0 ({O}pytest_sc1.txt).")
row("SC1a-gate-verify-refs", "2.1-citations", "course/modules/SC/SC1/index.html:182 (data-cite shreve2004stochastic)", "PASS",
    f"tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 ({O}verify_refs_offline.txt); "
    f"tools/verify_refs.py --unit SC1: 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 "
    f"({O}verify_refs_unit.txt).")

# ---- labs
row("SC1a-lab-L01-twin", "2.5-lab-L01", "tests/labs/SC1/lab-SC1-L01-1.py; L01.html:137-206", "PASS",
    f"{S}embed_check.py ({O}embed_check.txt): page code equals the twin (True); the expected block at L01.html:202-207 equals "
    f"the twin's stdout, 6 lines (True); python -I -W error exit 0, stderr 0 bytes; no @@ markers left. CPython wall time 0.01 s.")
row("SC1a-lab-L02-twin", "2.5-lab-L02", "tests/labs/SC1/lab-SC1-L02-1.py; L02.html:168-262", "PASS",
    f"{S}embed_check.py ({O}embed_check.txt): page code equals the twin (True); the expected block at L02.html:263-274 equals "
    f"the 12 stdout lines (True); exit 0, stderr 0 bytes; wall 0.09 s.")
row("SC1a-lab-L03-twin", "2.5-lab-L03", "tests/labs/SC1/lab-SC1-L03-1.py; L03.html:131-252", "PASS",
    f"{S}embed_check.py ({O}embed_check.txt): page code equals the twin (True); the expected block at L03.html:218-252 equals "
    f"the 35 stdout lines (True); exit 0, stderr 0 bytes; wall 0.05 s.")
row("SC1a-lab-claims-L01", "2.5-lab-claims",
    "tests/labs/SC1/lab-SC1-L01-1.py:1-9 (module docstring, shown at L01.html:137-145); L01.html:136 (hypothesis), :208 (interpretation)",
    "PASS",
    "Docstring says the lab checks two identities on finite grids: dyadic variance sums (arithmetic on piece lengths fixed by "
    "D2) and the covariance identity 'checked on a grid' (Proposition 1.2). Printed lines (out/twin_L01.stdout, = L01.html:202-207): "
    "'15 of 15' (3 times x depths 0..4, loop at twin lines 42-45), 'Cov(B at 1/4, B at 5/8) = 1/4', '81 of 81' (9x9 grid pairs, "
    "twin lines 54-55). Hypothesis and interpretation match the code and output. The round-3 FAIL (docstring text) is resolved at 9a02b1a.")
row("SC1a-lab-claims-L03", "2.5-lab-claims", "course/modules/SC/SC1/L03.html:133 (hypothesis), :253 (interpretation), :343 (E1)",
    "PASS",
    f"Hypothesis: se H*sqrt(2/N)/20 follows from Var(Q)=2H^2/N (Theorem 2.3 with Assumption 3.2) and 400 paths: recomputed in "
    f"{O}recompute.txt. Printed z values (out/twin_L03.stdout) max |z| 2.39 at H=1,N=2; the next largest is 1.84 (interpretation at "
    f"L03.html:253 is correct). 'All 16 values lie within +-3' (E1, L03.html:343) is true of the printed output. Printed se at H=2,N=128 is 0.0125 = population value (recompute.txt).")
row("SC1a-lab-L02-docstring", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L02-1.py:1-8 (docstring, shown at L02.html:171-178)", "PASS",
    f"Docstring: dyadic count and grid-supremum line are identities for every seed; bound lines describe one seeded sample. "
    f"{S}seed_sweep_L02.py over seeds 0..199 ({O}seed_sweep_L02.txt): dyadic identity failures 0; grid-sup identity failures 0; "
    f"levels within bound range 6..8, so the bound lines are sample-dependent as stated.")
row("SC1a-r4-seed-sweep-L02", "2.5-lab-seed", "tests/labs/SC1/lab-SC1-L02-1.py; L02.html:170 (SIMULATED claim)", "PASS",
    f"{S}seed_sweep_L02.py ({O}seed_sweep_L02.txt): 200 seeds, 216 dyadic cases each, all equal; 'seeds with all 8 within: 172'. "
    f"The L02.html:170 sentence ('count of levels within the bound is one sample's count and is not a guaranteed value') holds.")

# ---- numbers
row("SC1a-numbers-L01", "2.2-numbers",
    "course/modules/SC/SC1/L01.html:132, :229, :298, :305, :348-352, :393, :398, :412, :426", "PASS",
    f"Exact Fractions in {S}recompute.py ({O}recompute.txt, section 'L01 exact numbers'): sd 1/2 at h=1/4, 1/10 at h=1/100, "
    f"ratio 10, 3/64 pieces with 16*3/64 = 3/4, Cov(B_{{1/2}},B_1)=1/2, Var(3B_1-B_2)=5, E[B_3^2]=3, Cov(B_{{1/3}},B_{{2/3}})=1/3, "
    f"Var increment 1/3, 2*1/8=1/4, 81 pairs, 15 counts. All match the page.")
row("SC1a-numbers-L02", "2.2-numbers",
    "course/modules/SC/SC1/L02.html:263, :274, :385, :392, :399, :405-406, :418, :444, :486, :493, :514-516", "PASS",
    f"{S}recompute.py ({O}recompute.txt): level-1 observed sup unrounded 0.11658934 -> 0.116589; |xi_1,1| = 0.23317869 -> "
    f"0.233179 and twice the unrounded sup 0.2331787 (L02.html:418 now correct; the round-3 FAIL at 0.233178 is fixed); "
    f"lambda_1 = 1.665109, bound_1 = 0.832555; grid sup |S_8-S_4| = 0.348139; sum of bounds 5..8 = 1.309399; 216 cases "
    f"(2,3,5,9,17 points x 9,8,7,6,5 levels). Variance identities Var(U_j)=2^-(n+1), Cov=0 checked exactly for n=0..5.")
row("SC1a-numbers-L03", "2.2-numbers",
    "course/modules/SC/SC1/L03.html:253, :270, :275, :343, :350, :357, :368, :375, :398, :434, :457, :475", "PASS",
    f"{O}recompute.txt: 16*255/1536 = 2.65625; 15/24 = 0.625; 0.166664 (H=2,N=128) = closed form; "
    f"0.0125 = 2*sqrt(2/128)/20; 0.625 at N=2; sqrt(2/pi) = 0.797885 = 2 phi(0); N sqrt(2/pi) sqrt(t/N) values 0.797885, "
    f"1.595769, 3.191538 at N=1,4,16 (t=1). Printed values in out/twin_L03.stdout agree.")
row("SC1a-numbers-L02-36-points", "2.2-numbers", "course/modules/SC/SC1/L02.html:263", "PASS",
    f"2^n+1 points at depths 0..4 are 2,3,5,9,17, summing to 36 pairs, each compared with levels n..8 (9-n values): 216 cases. "
    f"{O}recompute.txt ('L02 dyadic case count and formula').")
row("SC1a-numbers-L03-SE-follow", "2.2-numbers", "course/modules/SC/SC1/L03.html:398 (key-results row, grade C)", "PASS",
    f"{O}recompute.txt ('L03 gap table'): gap = printed se / (H sqrt(2/N)/20) - 1; the largest |gap| is 13.21% at H=2, N=1 "
    f"(0.1601 vs 0.141421); the page's 'within 14 percent' and '13.2 percent' agree.")

# ---- grades
row("SC1a-grade-L01", "2.3-grades", "course/modules/SC/SC1/L01.html:83, :101, :119, :349-352", "PASS",
    "Proposition 1.2 (T, Assuming A1(a)), Remark 1.3 (T, A1(a),(b)), Example 1.4 (T); key-results rows graded T with a proof "
    "in the section named. The proofs are complete (see the math rows); the only unlisted fact is Cauchy-Schwarz (row SC1a-r4-cauchy-schwarz-L01).")
row("SC1a-grade-L02", "2.3-grades", "course/modules/SC/SC1/L02.html:74, :93, :110, :134, :274, :287, :436-447", "PASS",
    "Lemma 2.2, 2.1, 2.3 (T), Proposition 2.4 (T), Theorem 2.5 (T, under A2), Remark 2.6 (T, proved on page). Each T has a complete "
    "proof on the page from the Assumptions it names; A2 is the only identification step left as a labelled sketch (L02.html:282).")
row("SC1a-grade-L03", "2.3-grades", "course/modules/SC/SC1/L03.html:77, :90, :99, :118, :394-398", "PASS",
    "Lemma 2.1, 2.2, Theorem 2.3, Proposition 2.4 graded T with proofs on the page; the Lab 1 row is graded C with basis 'Lab 1 (SIMULATED), one seed, 400 paths'.")
row("SC1a-hub-grade-definition", "2.3-grades", "course/modules/SC/SC1/index.html:79; BLUEPRINT.md:158", "PASS",
    "Hub text 'A theorem, proved on the page or with a precisely cited proof' matches BLUEPRINT.md:158 'Theorem: proved on the page, or with a precisely cited proof'.")

# ---- maths
row("SC1a-math-L01-prop1.2", "2.4-math", "course/modules/SC/SC1/L01.html:84-98 (Proposition 1.2 and proof)", "FAIL",
    "Re-derived: symmetry, the s=0 and s=t cases, independence of B_s and B_t-B_s from (D3) with t0=0,t1=s,t2=t, the covariance "
    "E[X(X+Y)]=E X^2+E[XY]=s, and the use of A1(a). The one unlisted step is L01.html:95, 'integrable by the Cauchy-Schwarz "
    "inequality', which is a standard fact not in Assumption A1 (see SC1a-r4-cauchy-schwarz-L01).",
    "At L01.html:95 replace 'The product XY is therefore integrable by the Cauchy-Schwarz inequality' with 'Since |XY| <= (X^2+Y^2)/2 "
    "and X^2, Y^2 are integrable (E X^2 = s, E Y^2 = t-s), XY is integrable' (elementary, no further assumption).")
row("SC1a-math-L01-remark1.3", "2.4-math", "course/modules/SC/SC1/L01.html:102-113", "PASS",
    "Re-derived: increments independent by (D3), normal by (D2); linear combinations normal by A1(b); covariance by Proposition 1.2 "
    "(needs A1(a), named as H2).")
row("SC1a-math-L01-canon-construction", "2.4-math", "course/modules/SC/SC1/L01.html:215-217", "PASS",
    "Re-derived: B~_t = B_t + 1{t=U} with U uniform on (0,1): B~_0 = 0, P(U in F)=0 for finite F so fidi laws agree, (D2),(D3) hold; "
    "B~ discontinuous at U on every outcome since B is continuous. Non-normal counterexample (B_1 = +-1) checked: mean 0, variance 1, P(B_1=1)=1/2 != 0.")
row("SC1a-math-L02-lemmas-2.1-2.2", "2.4-math", "course/modules/SC/SC1/L02.html:73-117", "PASS",
    "Re-derived Lemma 2.2 (a)-(e) (hat support, disjointness, dyadic zeros, dyadic agreement, linearity) and Lemma 2.1: E e^{theta eta}=e^{theta^2/2}; "
    "1{eta>lambda} <= e^{theta(eta-lambda)} by 2.1(a); theta=lambda gives e^{-lambda^2/2}; two-sided factor 2.")
row("SC1a-math-L02-lemma2.3-arithmetic", "2.4-math", "course/modules/SC/SC1/L02.html:121-141", "PASS",
    "Re-derived: c = 2^{-(n+2)/2}; Var(U_j) = 2^{-(n+2)} + 2^{-(n+2)} = 2^{-(n+1)}; Cov(U_j,V_j) = 2^{-(n+2)} - 2^{-(n+2)} = 0; "
    "checked exactly for n=0..5 (recompute.py 'Lemma 2.3 variance bookkeeping').")
row("SC1a-math-L02-prop2.4", "2.4-math", "course/modules/SC/SC1/L02.html:145-165", "PASS",
    "Re-derived: lambda_m^2 = 4m log 2 gives 2e^{-lambda_m^2/2} = 2*4^{-m}, union bound 2^{-m}; P(A_{m0}^c) <= 2^{1-m0}; continuity from below "
    "(2.1(c)); M_m = sqrt(2 log 2) sqrt(m) 2^{-m/2} <= sqrt(2 log 2) m r^m; sum m r^m = r/(1-r)^2 (recompute.txt: 8.2426406871 both); "
    "Cauchy and uniform convergence (2.1(b)); continuity by epsilon/3 argument.")
row("SC1a-math-L02-A2-sketch", "2.4-math", "course/modules/SC/SC1/L02.html:278-282", "PASS",
    "Labelled 'Sketch, not a proof'; names the skipped step (passage of characteristic functions to the limit and the joint version).")
row("SC1a-math-L02-thm2.5", "2.4-math", "course/modules/SC/SC1/L02.html:286-296", "PASS",
    "Re-derived: B_0 = 0 via S_M(0)=0 (Problem P2); (D2),(D3) from A2 on Omega*; B = S a.s. so fidi laws agree; off Omega* path is zero, so all paths continuous.")
row("SC1a-math-L03-thm2.3", "2.4-math", "course/modules/SC/SC1/L03.html:99-115", "PASS",
    "Re-derived: E[Q]=t by Lemma 2.2 and telescoping; Var(Q)=sum 2 Delta_k^2 by Assumption 3.2(a),(b); sum Delta_k^2 <= |P| t; mean-square error bound 2t|P|; "
    "L03.html:115 'no almost-sure limit' statement is consistent with the proof.")
row("SC1a-math-L03-prop2.4", "2.4-math", "course/modules/SC/SC1/L03.html:117-129", "PASS",
    "Re-derived: (b^2-a^2)^2 <= 4H^2(b-a)^2; sum bound 4H^3|P|; equal-step sum H^4(4N^2-1)/(3N^3) by induction (checked with exact Fractions for N<=128 in recompute.txt).")
row("SC1a-math-L03-misc-claims", "2.4-math", "course/modules/SC/SC1/L03.html:259-261, :270, :274-279, :366-382", "PASS",
    "Re-derived: E|Z| = sqrt(2/pi) by P3; the counterexample N X_N^2 has variance 2t^2 for every N; R2 least constant c=2 (equal partition gives 2t|P| exactly). "
    "The 'Theorem 2.3 fails' wording at L03.html:260 is handled in row SC1a-r4-thm23-counterexample-L03.")
row("SC1a-math-L03-density", "2.4-math", "course/modules/SC/SC1/L03.html:78 (Lemma 2.1 density), :332 (P3)", "PASS",
    "phi is the standard normal density in both places; P3 uses z phi(z) = -phi'(z) consistently with Lemma 2.1.")
row("SC1a-grade-L02-remark2.6", "2.4-math", "course/modules/SC/SC1/L02.html:300-313", "PASS",
    "Re-derived: W_t = sum_{j<k} B^(j)_1 + B^(k)_{t-k} is continuous at integers and W_0 = 0; refinement by integers puts each unit interval in one copy; "
    "(D2) via (H1) independence and A1(b),(a); (D3) via A1(e) with sub-partitions of [0,1] for each copy (A2 through Theorem 2.5). The statement "
    "itself is correct; its assumption list in the reference paragraph is row SC1a-reference-section-L02-L03.")
row("SC1a-math-L02-thm2.5-extension", "2.4-math", "course/modules/SC/SC1/L02.html:300-303", "PASS",
    "H2 lists Assumption 2.1 with A1(a),(b),(e) and A2; the proof uses Theorem 2.5, whose H2 also lists Assumption 2.1. Consistent with the proof.")
row("SC1a-exercises-L01-L03", "2.4-problems",
    "course/modules/SC/SC1/L01.html:246-427 (M1-M3, P1-P3, E1-E3, R1-R3); L02.html:351-520; L03.html:291-466", "PASS",
    "Every worked solution re-derived. The round-3 FAIL (last displayed digit at L02.html:406/418) is fixed: L02.html:418 now gives 0.2331787 -> 0.233179, "
    "and the L02.html:418 digits agree with recompute.txt. M1-M3, P1-P3, R1-R3, E1-E3 of L01 and L03 match the exact recomputation (recompute.txt, section L01 exact numbers).")
row("SC1a-misconceptions-canon", "2.4-canon", "course/modules/SC/SC1/L01.html:219-235, L02.html:307-330, L03.html:256-281", "PASS",
    "Each misconception has a wrong belief, a reason and evidence. L02 harmonic-series argument recomputed (partial sum to 2^k >= 1 + k/2); "
    "L03 E|Z| misconception recomputed; L01 misconception 2 recomputed (10 = 1/10 / (1/100)).")
row("SC1a-canon-breaks-ungraded", "2.3-grades", "course/modules/SC/SC1/L02.html:319-322; L01.html:215-217; L03.html:259-261", "PASS",
    "Round-3 FAIL resolved: each canon-break claim now has a proof or an explicit counterexample (L01:215 construction; L01:217 B_1=+-1; "
    "L02:322 X_t with X_{1/3}=0; L03:260 independence counterexample) or is hedged ('do not follow from this page's arguments', L02:320).")

# ---- notation
row("SC1a-notation-macros", "2.4-notation", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "PASS",
    f"{S}notation_scan.py ({O}notation_scan.txt). Registered macros used: \\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic. "
    "Not registered but standard KaTeX: \\mathbb Z at L02.html:78 (no registered Z macro; not a notation collision).")
row("SC1a-notation-no-registered-collision", "2.4-notation", "course/modules/SC/SC1/L01.html, L02.html, L03.html", "PASS",
    f"{O}notation_scan.txt: no Phi, gamma, R*, R^{{e*}}, R_f, or \\mathbb{{Q}} in the slice math. Q(P) in L03 is the quadratic variation, "
    "plain Q, not the registered \\mathbb{Q} (risk-neutral measure).")
row("SC1a-notation-T-subscript", "2.4-notation", "course/modules/SC/SC1/L02.html (all math; round-3 defect was T_m in the R3 solution)", "PASS",
    f"{O}notation_scan.txt, section '== L02.html': the single-letter tokens contain no T, and grep for 'T_m' or 'T_{{m}}' in L02.html returns 0 matches. The round-3 defect is absent.")
row("SC1a-notation-H-horizon", "2.4-notation", "course/modules/SC/SC1/L03.html:120, :122, :128, :133; tests/labs/SC1/lab-SC1-L03-1.py", "PASS",
    f"H is the horizon throughout L03 (scan: 'H': 56 math tokens). The reserved T appears once, as a mention at L03.html:120. Twin HORIZONS=(1.0, 2.0).")
row("SC1a-r4-notation-S-symbol-L02", "2.4-notation", "course/modules/SC/SC1/L02.html:67-68, 126, 132-134, 139, 151, 163-165, 282, 296", "FAIL",
    "L02 uses S_M (partial sums, Definition 2.1 at L02.html:67), S_n, S_{n+1} (Lemma 2.3) and S(t) (limit) for the Levy-type construction. "
    "plans/SC1-build-plan.md section 2.3 (binding) reserves S_n for the simple random walk (local symbol, 'never redefined'), and L07/L08 use S_n "
    "for that walk (L07.html:193-202, L08.html:153-239). The same symbol therefore carries two meanings across the unit. "
    "(M_m for the bounds at L02.html:160-164 is a second, weaker overlap with the running maximum M_t of the plan.)",
    "Rename the L02 partial sums and their limit to a symbol the plan does not assign, for example Sigma_M and Sigma(t) (or S^{(M)}), "
    "in L02.html lines 67-68, 126-165, 282 and 296; keep S_n for the simple random walk in L07 and L08. Optionally rename the bounds M_m.")

row("SC1a-r4-thm23-counterexample-L03", "2.4-math", "course/modules/SC/SC1/L03.html:260 ('Independence is not optional'); L03.html:382 (R3 solution)", "FAIL",
    "The example takes, for each N, all N increments of the equal partition equal to one X_N ~ N(0,t/N). Its computation is right: E Q = t and "
    "Var Q = N^2 * 2(t/N)^2 = 2t^2 for every N (L03.html:382). But these increments are not independent, so the family violates (D3) of Definition 1.1 and is not a "
    "standard Brownian motion. Hypothesis H1 of Theorem 2.3 (L03.html:101) therefore does not hold, and the page's 'so Theorem 2.3 fails' (L03.html:260) "
    "is loose. The accurate statement is that the conclusion fails for this non-independent family, which shows Assumption 3.2 cannot be dropped from the proof.",
    "In L03.html:260 replace 'so Theorem 2.3 fails' with 'so the mean-square conclusion of Theorem 2.3 fails for this family. The family is not a standard "
    "Brownian motion, so the theorem does not apply to it, and the example shows that the independence in Assumption 3.2 cannot be dropped.'")

# ---- structure, prose, hub
row("SC1a-process-words", "2.9-prose", "index.html, L01.html, L02.html, L03.html; lab twins L01-L03", "PASS",
    "grep (case-insensitive) for build, builder, verifier, round, REQUEST and 'unit report' in the four pages and the three twins: no matches in learner text.")
row("SC1a-banned-phrases", "2.9-prose", "index.html, L01.html, L02.html, L03.html; lab twins", "PASS",
    "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, "
    "studies show, experts agree, it is well known, obviously, clearly and the ellipsis character: no matches.")
row("SC1a-structure-L01-L03", "2.9-structure", "course/modules/SC/SC1/L01.html, L02.html, L03.html", "PASS",
    "why-it-matters words: L01 99, L02 99, L03 117 (limit 120). Each lesson: 3 misconceptions, 12 solution blocks (M1-M3, P1-P3, E1-E3, R1-R3), "
    "a key-results table, a 10-item quiz (8-15), data-hours=9, one why-it-matters paragraph.")
row("SC1a-scope-words-L02-L03", "2.4-scope", "course/modules/SC/SC1/L02.html:122, :139, :158, :263, :316, :385, :417; L03.html:85, :104, :115, :261, :278", "PASS",
    "Each 'every', 'all', 'always', 'any', 'exactly', 'converge' claim re-read: each is computed (dyadic identities, Lemma 2.2(d) for all "
    "dyadic points, Prop 2.4 for all outcomes in Omega*, a closed form or the lab's 216 cases); almost-sure and pathwise claims are "
    "disclaimed (L03.html:115, :261).")
row("SC1a-scope-L01-prop1.2-only", "2.4-scope", "course/modules/SC/SC1/L01.html:216 (canon-break 3)", "PASS",
    "The statement that Proposition 1.2 still holds with a non-normal law of the same mean and variance is correct: the proof uses only the "
    "first two moments and A1(a), and square-integrability is given by the variance (the integrability step needs no Cauchy-Schwarz after the fix).")
row("SC1a-ref-L01-every-result", "2.1-citations", "course/modules/SC/SC1/L01.html:433", "FAIL",
    "L01.html:433 says 'Every result is proved on this page from Definition 1.1 and, where it says so, from Assumption A1'. Proposition 1.2 "
    "uses Cauchy-Schwarz at L01.html:95, which is neither in Definition 1.1 nor in A1 (see SC1a-r4-cauchy-schwarz-L01).",
    "Either apply the elementary fix at L01.html:95 (then the sentence is true), or name Cauchy-Schwarz as a numbered Assumption in A1.")
row("SC1a-r4-cauchy-schwarz-L01", "2.4-assumptions", "course/modules/SC/SC1/L01.html:95; index.html:69 (promise)", "FAIL",
    "index.html:69 promises that a standard fact of a prerequisite that the page does not prove is stated as a numbered Assumption. "
    "L01.html:95 uses the Cauchy-Schwarz inequality without stating it. It is needed only for integrability of XY, and "
    "|XY| <= (X^2+Y^2)/2 with E X^2 = s, E Y^2 = t-s proves it without any extra assumption (I checked the inequality and the moments).",
    "At L01.html:95 replace the Cauchy-Schwarz sentence with: 'Since |XY| <= (X^2+Y^2)/2, and X^2 and Y^2 are integrable (E X^2 = s, E Y^2 = t-s), XY is integrable.'")
row("SC1a-hub-assumption-promise", "2.4-assumptions", "course/modules/SC/SC1/index.html:69 (promise), :184; L02.html:93-99 (Assumption 2.1), :105, :152", "PASS",
    "Round-3 FAIL resolved for the two named facts: monotonicity is Assumption 2.1(a), completeness is 2.1(b), and countable subadditivity / "
    "continuity from below is 2.1(c); Lemma 2.1 and Proposition 2.4 say 'Assuming Assumption 2.1' and the part. The one further unlisted "
    "fact (Cauchy-Schwarz, L01:95) is row SC1a-r4-cauchy-schwarz-L01.")
row("SC1a-attrib-L01-A1-parts", "2.4-assumptions", "course/modules/SC/SC1/L01.html:37, :72-80", "PASS",
    "A1 parts (a)-(e) are standard facts of M4 and M6 stated without proof, as L01.html:80 says; their uses are named by part.")
row("SC1a-assump-L01-P3", "2.4-assumptions", "course/modules/SC/SC1/L01.html:285-287", "PASS",
    "P3 says 'Assuming A1(a)' and uses it for symmetry plus Proposition 1.2, which uses A1(a).")
row("SC1a-assump-L02-grouping", "2.4-assumptions", "course/modules/SC/SC1/L02.html:113, :127-128", "PASS",
    "Lemma 2.3 H2 names A1(b), A1(c), A1(e); the proof uses A1(e) for grouping and A1(c) for uncorrelated jointly normal pairs; no other part is used.")
row("SC1a-attrib-L02-lemma2.1-union", "2.4-attribution", "course/modules/SC/SC1/L02.html:158, :263", "PASS",
    "Union bound over 2^{m-1} coefficients with Lemma 2.1 gives 2^{-m}; the lab text attributes the bound to Lemma 2.1 and the union bound, both on the page.")
row("SC1a-attrib-L02-eponym", "2.1-citations", "course/modules/SC/SC1/L02.html:7 (meta description); tests/labs/SC1/lab-SC1-L02-1.py:1", "PASS",
    "grep -i for Ciesielski, Levy and Schauder over the four pages and the three twins: no matches (no eponym attribution).")
row("SC1a-reference-section-L02-L03", "2.1-citations", "course/modules/SC/SC1/L02.html:544; L03.html:491; L01.html:433", "FAIL",
    "L02.html:544 says 'The extension to [0,infty) (Remark 2.6) is proved under Assumptions A1(a), A1(b), A1(e) and A2.' The statement of Remark 2.6 "
    "(L02.html:303) reads 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1', and Theorem 2.5 (its input) assumes Assumption 2.1 (L02.html:289). "
    "The paragraph omits Assumption 2.1. L03.html:491 (Shreve at book level, no locator) and L01.html:433 (no source) are correct.",
    "In L02.html:544 change 'Assumptions A1(a), A1(b), A1(e) and A2' to 'Assumptions A1(a), A1(b), A1(e), A2 and Assumption 2.1, as its statement lists'.")
row("SC1a-hub-hours", "2.9-hours", "course/modules/SC/SC1/index.html:29, :39-42, :150; project.html:33, :262-273", "PASS",
    "index.html:29 data-hours-lessons=72, data-hours-project=28; eight lesson pages each data-hours=9 (L01-L08 grep); 72+28=100; "
    "project share 28% (10-40% rule); hub 72 h text at index.html:42.")
row("SC1a-hub-placement", "2.9-structure", "course/modules/SC/SC1/index.html:72-145", "PASS",
    "Nine items (seven prerequisite items, two data-skill items at lines 131 and 140); data-mastery=0.8; 7/9=77.8% and 8/9=88.9% (recomputed in "
    f"{O}recompute.txt, section hub placement); the mastery bar needs 8 of 9.")
row("SC1a-r4-hub-quiz-keys", "2.9-structure", "course/modules/SC/SC1/index.html:72-145 (data-correct / data-answer)", "PASS",
    "Keys checked against the item text: P0.1 grade T (data-correct on the theorem option), proof by contradiction, 1 (integral of 2x), 2 (E[X]), "
    "E[XY]=E X E Y, completeness, X_n, 2P(B_t>=a) (skill check 1), 2 (skill check 2, numeric). All correct.")
row("SC1a-hub-prereq-chain", "2.9-structure", "course/modules/SC/SC1/index.html:35, :58-68; curriculum/curriculum.json (concepts/modules)", "PASS",
    "curriculum.json: SC1 prereqs [M6]; M6 [M4, M5]; M5 [M2]; M4 [M2]; M2 [M1]; M1 [P0.1]; P0.1 []. Closure {M1, M2, M4, M5, M6, P0.1} as the hub says.")
row("SC1a-hub-concept-list", "2.9-structure", "course/modules/SC/SC1/index.html:61-67", "PASS",
    "All 24 concepts named in the hub exist in curriculum.json with the owner the hub gives: M4 x8 (random-variable, normal-distribution, multivariate-normal, independence, expectation, variance, moment-generating-function, characteristic-function), "
    "M5 x3 (Cauchy sequence, completeness-of-reals, uniform-convergence), M6 x7, M1 x2, M2 x2, P0.1 x2.")
row("SC1a-hub-cards-L01-L03", "2.7-cards-copy", "course/modules/SC/SC1/index.html:152-154", "PASS",
    "Lesson-map descriptions for L01-L03 match each lesson's content (Definition 1.1, Proposition 1.2, Example 1.4, Assumption A2 in L02, the quadratic variation in L03).")
row("SC1a-hub-ladder-objectives", "2.9-structure", "course/modules/SC/SC1/index.html:45-56, :163-171", "PASS",
    "Six objectives with measurable verbs (Define, Construct, Prove, Verify, State, Prove) mapped to Lessons 1 to 8.")
row("SC1a-simulated-labels", "2.5-labels", "course/modules/SC/SC1/L02.html:170 and :173 (lab-SC1-L02-1.py:3); L03.html:132 and :136 (lab-SC1-L03-1.py:3); L03.html:398", "PASS",
    "The seeded labs carry the SIMULATED label in the lab heading or hypothesis and in the twin docstring: L02.html:170 ('SIMULATED.'), L02.html:173, twin line 3; "
    "L03.html:132 (heading '(SIMULATED)'), L03.html:136, twin line 3; the key-results row L03.html:398 says 'Lab 1 (SIMULATED)'. The L01 lab uses no generated paths and carries no label, as BUILDER_RULES 6 requires; its docstring says so (lab-SC1-L01-1.py:5).")
row("SC1a-hub-data-status", "2.8-data", "course/modules/SC/SC1/index.html:37, :174-177; L01-L03", "PASS",
    "grep -c data-files on index.html, L01, L02, L03: 0 on each; no MANIFEST entry used; SIMULATED labels on L02 (L02.html:170) and L03 (L03.html:132).")
row("SC1a-dag-hub-prose", "2.9-dag", "course/modules/SC/SC1/index.html:33, :53, :150", "PASS",
    "Scan of the four pages for D1-D9 names (Ito, SDE, Girsanov, Ornstein, geometric Brownian motion, Feynman-Kac, Poisson, Levy, Black-Scholes, barrier, Euler, Milstein, Donsker, bias, bridge): none in slice prose. Hub prose uses closure concepts and SC1 concepts only.")
row("SC1a-prose-L01-three-conditions", "2.9-prose", "course/modules/SC/SC1/index.html:49; L01.html:51", "PASS",
    "Both places say 'three conditions on the process and its increments' and Definition 1.1 has exactly three conditions (D1)-(D3).")
row("SC1a-define-dyadic", "2.9-define-before-use", "course/modules/SC/SC1/L01.html:132 (dfn def-dyadic-partition), L02.html:71, L03.html:55", "PASS",
    "The dyadic partition is defined with a plain <dfn> at L01.html:132 before any use; L02.html:71 and L03.html:55 use it afterwards.")
row("SC1a-scope-L03-converge", "2.4-scope", "course/modules/SC/SC1/L03.html:270 (misconception 1)", "PASS",
    "'For s to s^2 the sums vanish in the limit, and for Brownian motion their mean converges to the elapsed time, with mean-square error tending to zero' is correct (Prop 2.4(a); Theorem 2.3).")
row("SC1a-hub-quiz-cross", "2.9-hub-quiz", "course/modules/SC/SC1/index.html:143 (skill check 2 explanation)", "PASS",
    f"Round-3 FAIL resolved. The explanation says 'Rung 2 counts the same quantity for n=6 and a=2, and its check prints 29.' Running "
    f"tests/labs/SC1/lab-SC1-project-2.py run with python -I -W error, exit 0, stdout saved at {O}project2_twin.stdout: "
    f"'n = 6, a = 2: walks with maximum >= a: 29'. The hub's 2-step count of 2 (index.html:140, data-answer=2) uses the same identity.")
row("SC1a-prose-two-sources", "2.1-citations", "course/modules/SC/SC1/index.html:184; references/references.json (grep Karatzas: 0 matches)", "PASS",
    "The hub says the second curriculum source (Karatzas and Shreve) has no admitted registry record, which matches references/references.json (0 matches for 'karatzas') and the registry key shreve2004stochastic (references.json:20732, verified, book level).")
row("SC1a-lab-L02-hypothesis-expected", "2.5-lab-claims", "course/modules/SC/SC1/L02.html:170 (hypothesis), :275 (interpretation)", "PASS",
    "Hypothesis: 216 cases all agree (printed 216 of 216), grid-sup line True (printed True), bounds per level (printed observed <= bound lines). Interpretation's count explanation 36 pairs and 216 cases matches recompute.txt.")
row("SC1a-r4-twin-timing-and-purity", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "PASS",
    "Standard library only (fractions, math, random, itertools); RNGs seeded (SEED constants; random.Random); no network; CPython wall times 0.01 s, 0.09 s, 0.05 s, all under 10 s; no warnings with -W error.")

# ---- finish
for r in rows:
    if r["status"] == "PASS":
        r["fix"] = ""
ledger = {
    "unit": "SC1",
    "slice": "SC1-a",
    "round": 4,
    "verifier": "Haiku independent verifier, SC1-a round 4 (did not build SC1; no round-3 PASS row carried)",
    "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
    "base": "67a2d13e (round-3 pin of E-SC1-a.round3.json). Slice files changed since then (git diff 67a2d13e..9a02b1a): course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html and tests/labs/SC1/lab-SC1-L01-1.py. Unchanged: lab-SC1-L02-1.py, lab-SC1-L03-1.py.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-SC1-a (detached at 9a02b1a, .venv symlinked)",
    "scratch": "ledgers/SC1/scripts/SC1-a-r4/ (textview.py, notation_scan.py, embed_check.py, recompute.py, seed_sweep_L02.py, build_fragment.py; outputs under out/)",
    "verified_at": "2026-11-04",
    "verdict": "FAIL",
    "slice_files": [
        "course/modules/SC/SC1/index.html",
        "course/modules/SC/SC1/L01.html",
        "course/modules/SC/SC1/L02.html",
        "course/modules/SC/SC1/L03.html",
        "tests/labs/SC1/lab-SC1-L01-1.py",
        "tests/labs/SC1/lab-SC1-L02-1.py",
        "tests/labs/SC1/lab-SC1-L03-1.py",
    ],
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "shreve2004stochastic: verify_refs.py --unit SC1 live 1 of 560 entries, 0 problems; cited at book level only (index.html:182, L03.html:491).",
        "Karatzas and Shreve (second curriculum source, curriculum/03-markets.yaml:524): no registry record (references.json grep 0 matches); index.html:184 says so.",
    ],
    "freshness_flags": [],
    "notes": [
        "No grader in slice a: mutation testing not applicable (lab twins are demonstrations, architect ruling). run_graders and mutate_graders were not run.",
        "Round 4 re-verified every row from scratch; no round-3 PASS row is carried. All round-3 row ids are kept. Round-3 FAIL rows SC1a-lab-claims-L01, SC1a-numbers-L02, SC1a-exercises-L01-L03, SC1a-hub-quiz-cross, SC1a-hub-assumption-promise, SC1a-canon-breaks-ungraded are now PASS with the evidence cited.",
        "New round-4 FAIL rows: SC1a-r4-cauchy-schwarz-L01 (with dependents SC1a-math-L01-prop1.2 and SC1a-ref-L01-every-result), SC1a-reference-section-L02-L03 (assumption list omits Assumption 2.1), SC1a-r4-thm23-counterexample-L03 (wording 'Theorem 2.3 fails' for a non-Brownian family), SC1a-r4-notation-S-symbol-L02 (S_M/S used for a different object than the plan's S_n).",
        "Seed sensitivity: the L02 lab's identities hold for 200 seeds (seed_sweep_L02.txt); bound lines are sample-dependent, as the page says.",
        "Not judged in slice a (other slices): cards.json, project.html, grader/, L04 to L08 (read only where index or L01-L03 refer to them), lab-SC1-L04..L08, project labs (run only project-2 for the hub's '29' claim).",
        "Citation markup: BLUEPRINT section 3 asks for a citation key on every substantive claim; the architect restricts citations to shreve2004stochastic and the SC1 pages cite no key on derived results. Accepted as the architect decision (not a row).",
    ],
    "summary": "SC1-a round 4 at 9a02b1a: verdict FAIL. 76 rows: 70 PASS, 6 FAIL, 0 UNVERIFIABLE. Gates re-run and passing: check_pages, check_dag, check_projects, run_labs 11/11 and per page, ruff, ruff format, mypy, twins under python -I -W error with page-code and expected-block equality, page_smoke on index/L01-L03 alone, pytest -k SC1 (11 passed), verify_refs offline and unit SC1. Open FAILs: L01 Cauchy-Schwarz use (L01.html:95) with its dependents SC1a-math-L01-prop1.2 and SC1a-ref-L01-every-result; L02 Remark 2.6 assumption list (L02.html:544); L03 'Theorem 2.3 fails' wording (L03.html:260); L02 symbol S_M/S versus the plan's S_n (L02.html:67-68 and following).",
}
bad = [r["id"] for r in rows if r["status"] not in {"PASS", "FAIL", "UNVERIFIABLE"}]
assert not bad, bad
out = ROOT / "ledgers" / "SC1" / "SC1-a.json"
out.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", sum(r["status"] == "PASS" for r in rows), "fail", sum(r["status"] == "FAIL" for r in rows))
