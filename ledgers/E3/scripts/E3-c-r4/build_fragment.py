import json
from pathlib import Path

S = "ledgers/E3/scripts/E3-c-r4/"
P = "Carried from round 3 is not used: subject re-verified in round 4 (L07/L08 and twins changed between ccfdf4c and b276325). "
R = []
def row(i, check, loc, status, ev, fix=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

row("E3c-R01-check-pages", "2.9 structure: check_pages", "course/modules/E/E3/L07.html, L08.html", "PASS",
    "Re-run at pin b276325: .venv/bin/python tools/check_pages.py --unit E3 --page L07 -> 'check_pages E3 L07: PASS'; --page L08 -> 'check_pages E3 L08: PASS' (exit 0).")
row("E3c-R02-check-dag", "2.9 DAG: check_dag", "course/modules/E/E3/L07.html, L08.html", "PASS",
    "Re-run: tools/check_dag.py --unit E3 -> 'check_dag E3: PASS' (exit 0). Unlinked uses checked by hand (R36, R37).")
row("E3c-R03-run-labs", "2.5 labs: run_labs", "tests/labs/E3/lab-E3-L07-1.py, lab-E3-L08-1.py", "PASS",
    "Re-run: tools/run_labs.py --unit E3 --page L07 -> 'run_labs E3: PASS (1/1)'; --page L08 -> 'run_labs E3: PASS (1/1)'.")
row("E3c-R04-twin-isolated", "2.5 labs: twin alone under python -I -W error", "tests/labs/E3/lab-E3-L07-1.py, lab-E3-L08-1.py", "PASS",
    "ledgers/E3/scripts/E3-c-r4/twin_page_check.py (output twin_page_check.out.txt): 'L07 twin exit 0', 'L08 twin exit 0', stderr ''. Run as python -I -W error.")
row("E3c-R05-page-code-equals-twin", "2.5 labs: page code equals twin", "course/modules/E/E3/L07.html:140-316; L08.html:168-428", "PASS",
    "twin_page_check.out.txt: 'page code == twin.rstrip(newline): True' for L07 and L08 (embed convention, tools/embed_labs.py).")
row("E3c-R06-expected-equals-output", "2.5 labs: expected block equals output", "L07.html:296-314; L08.html:402-426", "PASS",
    "twin_page_check.out.txt: 'L07 expected == stdout: True', 'L08 expected == stdout: True' (twin stdout from the -I -W error run).")
row("E3c-R07-page-smoke", "2.9 page_smoke", "course/modules/E/E3/L07.html, L08.html", "PASS",
    "Re-run: tools/page_smoke.py --unit E3 --pages L07 -> 'page_smoke modules/E/E3/L07.html: PASS'; --pages L08 -> 'page_smoke modules/E/E3/L08.html: PASS'; lab runtime 0.0 s each.")
row("E3c-R08-ruff-mypy-labs", "gate: ruff and mypy on the twins", "tests/labs/E3/lab-E3-L07-1.py, lab-E3-L08-1.py", "PASS",
    ".venv/bin/ruff check on both -> 'All checks passed!'; ruff format --check -> '2 files already formatted'; mypy --no-incremental on both -> 'Success: no issues found in 2 source files'.")
row("E3c-R09-verify-refs", "2.1 citations: verify_refs", "references/references.json (kahneman1979prospect, gilboa1989maxmin, ellsberg1961risk)", "PASS",
    "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit E3 -> 'live re-verification of E3: 5 of 560 entries, 0 problems' (exit 0).")
row("E3c-R10-banned-phrases", "2.9 banned phrases (BUILDER_RULES 3-4) and ellipses in prose", "L07.html, L08.html prose", "PASS",
    "ledgers/E3/scripts/E3-c-r4 prose check (E3-c-r3/prose_grep.py run with -I): 'L07 banned: 0', 'L08 banned: 0'.")
row("E3c-R11-process-words", "2.9 no process words in learner text", "L07.html, L08.html prose", "PASS",
    "prose_grep.py: 'L07 process: 0', 'L08 process: 0'.")
row("E3c-R12-structure-L07", "2.9 structure and template order (BUILDER_RULES 4.2)", "course/modules/E/E3/L07.html", "PASS",
    "Read in full (570 lines). Order: header, grade legend, why-it-matters, s1 definitions 1.1-1.2, remark/proof, example 1.4, observation 1.5, remark 1.6, s2 (example 2.1, Prop 2.2, remark 2.3), Lab 1 section (140-316), s3 canon breaks, s4 misconceptions (3), s5 problem set (mechanics 3, proof 3, empirical 3, research 3, each with solution), s6 key results, s7 quiz (11 items), s8 references, lesson nav. data-hours=7.")
row("E3c-R13-structure-L08", "2.9 structure and template order (BUILDER_RULES 4.2)", "course/modules/E/E3/L08.html", "PASS",
    "Read in full (726 lines). Order: header, grade legend, why-it-matters, s1 prior sets, s2 ambiguity aversion, s3 Epstein-Zin, Lab 1 (168-428), s4 four models with table and Remark 4.2, s5 canon breaks, s6 misconceptions (3), s7 problems (mechanics 3, proof 3, empirical 3, research 3), s8 key results, s9 quiz (11 items), s10 references, nav. data-hours=7.")
row("E3c-R14-hours", "hours arithmetic: lesson hours vs hub split", "course/modules/E/E3/L07.html:2,35; L08.html:35; index.html:29,127,135-136", "PASS",
    "data-hours=7 and 'Lesson 7 of 8 · 7 study hours' (L07), 'Lesson 8 of 8 · 7 study hours' (L08). Hub data-hours-lessons=56 and text 'Eight lessons of seven study hours each, which is 56 hours'; 56 + data-hours-project=14 = 70 = unit hours (index.html:31 'Tier U · 70 hours'). Consistent.")
row("E3c-R15-lab-hypothesis-L07", "2.5 labs: stated hypothesis vs output", "L07.html:142", "PASS",
    "Hypothesis numbers: 42.87 vs 39.13 (alpha=1; output 42.8686, 39.1251), 4.88 vs 3.91 (alpha=1/2; output 4.8788, 3.9125), closed form gap 3.33e-16 (output), crossing near 0.278 (output last point 0.278). Every nondecreasing utility in the family ranks B at or above A: part D 10 of 10. Recompute: ledgers/E3/scripts/E3-c-r4/recompute_L07.out.txt.")
row("E3c-R16-lab-hypothesis-L08", "2.5 labs: stated hypothesis vs output", "L08.html:170", "PASS",
    "4180000/41 = 101951.2195 (exact recompute, recompute_L08.out.txt); prospect 99892.7670 (output); EZ equals EU for six (psi,beta) pairs (part B); maxmin 99523.8095 at P(red)=1/3 (output 'worst prior is P(red) = 1/3'); known urn preferred for both colours (part C 'True; True').")
row("E3c-R17-lab-interpretation-L08", "2.5 labs: interpretation sentence vs lab output", "course/modules/E/E3/L08.html:427 (interpretation after the expected block)", "FAIL",
    "The sentence says 'the largest gap between the closed form and bisection is printed in part A and is below 10^{-15} CU'. Part A (L08.html:326-327 in the twin, printed at expected line 406) computes ONE gap, for the single value prospect_cu: 'prospect inverse, closed form minus bisection = 4.44e-16 CU'. No maximum over a range of values is computed or printed. The value 4.44e-16 is below 1e-15, so only the 'largest' wording is false.",
    "Replace the sentence with: 'the gap between the closed form and bisection at the gamble's value is printed in part A (4.44e-16 CU), below 10^{-15} CU.' (Or compute a maximum over a grid of values in the lab and re-embed with tools/embed_labs.py.)")
row("E3c-R18-lab-hygiene", "2.5 labs: seeded, no network, stdlib only, runtime", "lab-E3-L07-1.py, lab-E3-L08-1.py", "PASS",
    "Imports only __future__, itertools, math, collections.abc, fractions (L07) and math, collections.abc, fractions (L08). No randomness (both docstrings say 'no randomness and no network access'); runtime 0.0 s (page_smoke).")
row("E3c-R19-L07-numbers-prose", "2.2 numbers in L07 prose (one row per number)", "L07.html:86,94,98,127,132,137,315,330,334,338,352-353,360,403,410,417", "PASS",
    "recompute_L07.out.txt: omega(3/10)=0.2857908849 (0.28579088), omega(3/5)=0.3912507700, omega(1/2)=0.3535533906, omega(1/4)=0.2679491924=2-sqrt3, 2*omega(3/10)=0.57158177, ratio 0.73045450 (closed form same), threshold 0.58578644, 0.66666667, V(A)=45, V(B)=60 (identity), Gamma(A)=42.86863274, Gamma(B)=39.12507700, diff 3.74355573 -> 3.7436, alpha=1/2 Gamma 4.87875558 -> 4.8788 and 3.91250770 -> 3.9125, omega(0.01)=0.08340301, omega(0.99)=0.82984948, ETA=1 scratch run (eta_one_run.out.txt): Gamma 45.0000/60.0000, closed-form gap 3.13e-01.")
row("E3c-R20-L07-misconception-numbers", "2.2 misconception arithmetic", "L07.html:330,334,338", "PASS",
    "Weighted value 8.340301+41.492474=49.832775 -> 49.8328; EV 50.5; net -0.667225 -> -0.67; over (0.08340301-0.01)*100=7.340301 -> 7.34; under (0.99-0.82984948)*50=8.007526 -> 8.01; 7.34-8.01=-0.67. Consistent (recompute_L07.out.txt).")
row("E3c-R21-L07-prop2.2", "2.4 mathematics: Proposition 2.2 and proof", "L07.html:119-133", "PASS",
    "Re-derived: V(A)=omega(3/10)(50^a+100^a), V(B)=omega(3/5)100^a; 50^a=2^-a 100^a; threshold 1/(1+2^-a) = 2/3 (a=1), 0.58578644 (a=1/2); ratio 0.73045450 > both. Quotient of printed 8-decimal values 0.28579088/0.39125077 = 0.73045449 (computed), as the page states.")
row("E3c-R22-L07-observation-and-E1", "2.4/2.2: Observation 1.5 and Problem E1", "L07.html:90-92, 401-404", "PASS",
    "Grid of 1001 points (recompute): interior sign changes = 1; last grid point with omega>p is 0.278 (omega(0.278)=0.27808523>0.278); omega(0.279)<0.279; bisection crossing 0.27813210 lies in (0.278, 0.279). Observation is labelled a finite check.")
row("E3c-R23-L07-example-2.1", "2.4 mathematics: Example 2.1 table", "L07.html:107-116", "PASS",
    "F_A(0)=2/5, F_A(50)=7/10, F_A(100)=1; F_B(0)=2/5, F_B(50)=2/5, F_B(100)=1 (exact Fractions, part B output). Dominance yes, strict at 50.")
row("E3c-R24-L07-proofs-and-solutions", "2.4 mathematics: M1-M3, P1-P3 solutions", "L07.html:349-395", "PASS",
    "M1: 1/(2+sqrt3)=2-sqrt3=0.26794919 (checked). M2: 100*0.35355339=35.355339, EV 50. M3: endpoints. P1: (sqrt p + sqrt(1-p))^2 = 1+2sqrt(p(1-p)). P2: term-by-term. P3: cancels 100^a>0 and omega(3/5)>0. All re-derived.")
row("E3c-R25-L07-research-R1-R3", "2.4 mathematics: R1-R3 solutions", "L07.html:424-445", "PASS",
    "R1: affine with endpoints is identity; omega_{1/2}(1/2)=0.35355339 != 1/2. R2: Tail_A(50)=3/5, Tail_B(50)=3/5, Tail_A(100)=3/10, Tail_B(100)=3/5 (exact); monotone step correct. R3: no number, design only, no data reported.")
row("E3c-R26-L07-key-results-grades", "2.3 grades: key-results table vs BLUEPRINT grade of each claim", "L07.html:452-462", "PASS",
    "Rows graded T are proved on the page (Example 1.4/P1, Remark 1.3/P2, Remark 1.6, Prop 2.2, Lesson 4 Thm 1.5 cited, verified in L04.html:89-95 with finite support S). The grid crossing row is C with basis stated. Kahneman row is C with registry title only (references.json: 'Prospect Theory: An Analysis of Decision under Risk').")
row("E3c-R27-L07-citation-kahneman", "2.1 attribution: kahneman1979prospect", "L07.html:80", "PASS",
    "references.json record kahneman1979prospect: title 'Prospect Theory: An Analysis of Decision under Risk', Econometrica 47(2), verified_by crossref. Claim (name appears in title; lesson does not reproduce the paper) matches the title read; graded C with locator 'title only'.")
row("E3c-R28-L08-numbers-prose", "2.2 numbers in L08 prose (one row per number)", "L08.html:85,132,142-143,165,170,427,436,441,446,451,468,471,476,496", "PASS",
    "recompute_L08.out.txt: 4180000/41=101951.2195; prospect V=-2.0710678 (printed -2.071068), inverse -1.0723305 (-1.072330), wealth 99892.7670; maxmin 1/(1/3/110000+2/3/95000)=99523.8095; premium 102500-101951.2195=548.7805 = 22500/41; maxmin - W0 = -476.1905; Ex 2.5 known red 103125, black 3300000/31=106451.6129; ambiguous 100000 (P_0 / P_90); Remark 4.2 45/90=1/2; Model 1 CE vs W0 = 1951.2195.")
row("E3c-R29-L08-model-table", "2.2 numbers: four-model table", "L08.html:454-464", "PASS",
    "Each row equals the recomputed value: EU 101951.2195/101951/1951.2195; prospect 99892.7670/99893/-107.2330; EZ 101951.2195/101951/1951.2195; maxmin 99523.8095/99524/-476.1905; alpha-MEU tau=1/2 101951.2195/101951/1951.2195 (exact equality with EU CE: True).")
row("E3c-R30-L08-prop-proofs", "2.4 mathematics: Proposition 1.3, Theorem 2.2, Proposition 2.4", "L08.html:70-134", "PASS",
    "Prop 1.3: weights sum to one, so V=E_P u(f). Thm 2.2: average of n numbers each >= m is >= m; u^{-1} strictly increasing (A2); CE_maxmin <= CE_Pbar. Prop 2.4: E_p u(f) = u(W_no)+p(u(W_red)-u(W_no)) with positive bracket (A2, A3), min at P_0 for red and P_90 for black. Remark 2.3: equality for one prior; strict when EUs differ.")
row("E3c-R31-L08-EZ-proof", "2.4 mathematics: Definition 3.1, Proposition 3.2 and proof", "L08.html:140-161", "PASS",
    "Re-derived: sure plan V0 = [(1-b)c0^a + b c^a]^{1/a}; gamble V0 = [(1-b)c0^a + bK]^{1/a}, K=(E c1^{1-g})^{a/(1-g)}; injectivity of x^{1/a} on positives (A4, A5 give positive bases; a != 0 from A1); beta>0 gives c^a=K; a-th root gives c=(E c1^{1-g})^{1/(1-g)}. Notation a=1-1/psi matches L05.html:65. No rho remains (grep).")
row("E3c-R32-L08-problem-solutions", "2.4 mathematics: M1-M3, P1-P3, E1-E3, R1-R3 solutions", "L08.html:507-607", "PASS",
    "M1: 8360000/85 = 1672000/17 = 98352.94; expected final wealth 98750. M2: min(98352.94, 105822.78)=98352.94 (1/(3/4/110000+1/4/95000)=105822.78 recomputed). M3: tau=0 gives 1/min E[1/W] = 105822.78. P2: weighted average with nonnegative weights (no 'convex' left, grep). P3: g affine, midpoint identity, u=-1/W explicit. E1: 3125 cents = 31.25 CU. E2: gap 0.00e+00 printed. E3: 22500/41 cents = 5.4878 CU. R1/R2/R3 re-derived (R2 black: worst black prob 1/3 gives 103125; known 106451.6129).")
row("E3c-R33-L08-citations", "2.1 attribution: gilboa1989maxmin, ellsberg1961risk", "L08.html:67,133,619-620", "PASS",
    "references.json: gilboa1989maxmin title 'Maxmin expected utility with non-unique prior' (contains the name); ellsberg1961risk title 'Risk, Ambiguity, and the Savage Axioms' (contains 'ambiguity'). Pages make title-only claims, graded C, locator 'title only; paper not read'.")
row("E3c-R34-quiz-keys-L07", "2.9 quiz keys and explanations L07", "L07.html:470-554", "PASS",
    "Q1 correct omega(0)=0,omega(1)=1 (Def 1.1). Q2 0.26795 +-1e-4 (2-sqrt3=0.2679492). Q3 B dominates. Q4 39.1251 +-5e-4 (39.125077). Q5 above 2/3 (threshold 2/3 at alpha=1). Q6 0.35355 +-1e-4. Q7 'not in general' (Remark 1.6). Q8 B with 60 (identity). Q9 ten utilities (part D 10 of 10). Q10 not linear (R1). Q11 0.278 +-1e-3.")
row("E3c-R35-quiz-keys-L08", "2.9 quiz keys and explanations L08", "L08.html:630-708", "PASS",
    "Q1 expected utility (Prop 1.3). Q2 101951.22 +-0.01 (4180000/41). Q3 P(red)=1/3 worst (CE increasing in p). Q4 99523.81 +-0.01. Q5 CE_maxmin <= CE_Pbar. Q6 103125 +-0.5. Q7 100000 (worst prior no red, W0). Q8 CRRA same gamma (Prop 3.2). Q9 548.78 +-0.01 (22500/41). Q10 symmetric prior set / affine inverse expectation (Remark 4.2). Q11 99892.77 +-0.01.")
row("E3c-R36-dag-L07", "2.9 DAG: linked and unlinked uses in L07", "L07.html:38, 56, 103, 320, 323-328", "PASS",
    "check_dag E3 PASS. Linked: expected-utility (L01), prospect-theory (L06), FOSD (L04), expectation (concepts). Named uses: Lesson 4 Thm 1.5 (L04.html:89), Lesson 6 v(x)=x^alpha (L06.html:62-63), Lesson 4 FOSD. No unlinked closure-external concept used by name (grep 'convex|concave|martingale|likelihood|...' in prose: only 'probability weighting', introduced here at L07.html:65).")
row("E3c-R37-dag-L08", "2.9 DAG: linked and unlinked uses in L08", "L08.html:38, 65, 138, 440, 543", "PASS",
    "check_dag E3 PASS. Linked: expected-utility, CE (L02), CRRA (L03), EZ and EIS (L05), prospect theory and loss aversion (L06). The former unlinked 'convex combination' (P2) is now 'weighted average with nonnegative weights' (L08.html:543; grep finds no 'convex' in L08 prose).")
row("E3c-R38-scope-L07", "2.9 scope words without computation or hypothesis", "L07.html prose", "PASS",
    "Scope hits (36) inspected: 'every finite lottery' (Remark 1.3, proved), 'every outcome' (Def 1.2), 'every nondecreasing utility' (Lesson 4 theorem, lab part D says finite family), 'every lottery with small chance' (misconception, refuted by the stated counterexample), 'No ... magnitude' (stated limit). None unsupported.")
row("E3c-R39-scope-L08", "2.4/2.9 scope claim: the known-urn preference holds for any strictly increasing u", "course/modules/E/E3/L08.html:132 (Example 2.5)", "FAIL",
    "The page says: 'the numbers depend on this choice, and the preference for the known urn does not (Theorem 2.2 and Proposition 2.4 use only that u is strictly increasing).' The claim is true (for any strictly increasing u, ambiguous CE = W0 = 100000 via P_0 / P_90, and the known urn's EU (1/3)u(110000)+(2/3)u(100000) > u(100000)), but neither cited result states it: Theorem 2.2 is about maxmin vs average prior, Proposition 2.4 is about which prior is worst. The known-urn comparison and the value W0 are not computed for general u anywhere on the page.",
    "Add the one-line argument at Example 2.5: for any strictly increasing u the worst prior gives final wealth W0 surely, so the maxmin CE is W0 = 100000 cents for both colours, while the known urn's expected utility (1/3)u(110000)+(2/3)u(100000) exceeds u(100000) for red (and (2/3)u(110000)+(1/3)u(100000) for black), so its CE exceeds W0. Then cite that argument instead of Theorem 2.2 and Proposition 2.4.")
row("E3c-R40-references-list", "2.1 reference keys used in the pages", "L07.html:80 data-cite; L08.html:67,133 data-cite; references", "PASS",
    "Keys used: kahneman1979prospect (L07), gilboa1989maxmin and ellsberg1961risk (L08). All three exist in references/references.json with status verified (crossref). Page reference lists are generated by data-references; no hand-typed bibliography in the pages.")
row("E3c-R41-quiz-expl-L07-L08-links", "2.9 quiz explanations cite existing items", "L07.html:519; L08.html:637,651,665,679,688,693,702", "PASS",
    "L07 Q7 cites 'Problem P2' (exists at L07.html:381, id P2; round-3 'Proposition P2' fixed). L08 Q9 cites 'Problem E3' (exists at L08.html:571). Proposition 2.4, Proposition 3.2, Remark 4.2, Model 1 and Model 4 cited in explanations exist.")

row("E3c-F01-notation-rho", "2.4/2.5 notation: rho vs a (round 3 F01)", "L08.html:142-160, 446, 586", "PASS",
    "Re-verified: no rho or U+03C1 in L08 (grep). Definition 3.1 now uses a = 1 - 1/psi, the same name as L05.html:65 (a := 1 - 1/psi). Prior non-PASS row fixed.")
row("E3c-F02-notation-alpha", "2.4 notation: alpha vs tau (round 3 F02)", "L08.html:64-66, 440, 617", "PASS",
    "Re-verified: the alpha-MEU mixing weight is now tau (L08.html:65-66, 450-462, twin lines 179-187). alpha is used only as the gains exponent (Model 2, alpha = delta = 1/2), which matches L06.html:62-64 and L08.html:65's explicit note. Prior non-PASS row fixed.")
row("E3c-F03-remark42-only-when", "2.4 mathematics: Remark 4.2 'only when' (round 3 F03)", "L08.html:468", "PASS",
    "Re-verified: the sentence is now 'It equals expected utility at the average prior P-bar when that midpoint equals P-bar(red)', a sufficient condition; the example midpoint 1/2 = P-bar(red) = 45/90 is checked. The counterexample at priors {1/5, 3/5} is no longer asserted. Prior non-PASS row fixed.")
row("E3c-F04-keyrow-alpha-meu-CRRA", "2.3 grades: key-results row 6 (round 3 F04)", "L08.html:617; P3 at 548-551", "PASS",
    "Row now scoped to 'CRRA utility with gamma = 2 (u(W) = -1/W) and a two-outcome gamble'. P3 states u(W)=-1/W and proves the midpoint identity (affinity of g). Remark 4.2 uses E[1/W], the same utility. Graded T with a proof that covers the scoped claim. Prior non-PASS row fixed.")
row("E3c-F05-example25-utility-unstated", "2.4 numbers: Example 2.5 utility (round 3 F05)", "L08.html:132; twin Part C lines 361-380", "PASS",
    "Example 2.5 now states 'Take u(W) = -1/W (CRRA with gamma = 2, as in Section 4)' and the twin Part C prints 'CRRA utility u(W) = -1/W' with 103125.0000 and 106451.6129. Recomputed: 1/((1/3)/110000+(2/3)/100000)=103125; 1/((2/3)/110000+(1/3)/100000)=106451.6129. Prior non-PASS row fixed for the numbers; the separate u-independence claim is R39.")
row("E3c-F06-L07-E2-printed-name", "2.9 lab output label (round 3 F06)", "L07.html:408-410", "PASS",
    "Problem E2 now says 'Gamma is the lab's name for V_omega' and uses Gamma(A)=42.8686, Gamma(B)=39.1251 (printed labels in the expected block, L07.html:312). Prior non-PASS row fixed.")
row("E3c-F07-L07-E3-eta1-prediction", "2.5 labs: ETA=1 prediction (round 3 F07)", "L07.html:417", "PASS",
    "Scratch run of the shipped twin with ETA=1 (ledgers/E3/scripts/E3-c-r4/eta_one_run.out.txt, run with python -I -W error, exit 0): Part A ends 'largest gap 3.13e-01', 'sign changes = 0; last point = none'; Part C 'Gamma(A) = 45.0000  Gamma(B) = 60.0000 ... B at or above A'. The prediction in the solution matches. The round-3 crash (max() over empty sequence) is gone from the twin (grep: no max over the empty list). Prior non-PASS row fixed.")
row("E3c-F08-L07-interpretation-table", "2.9 lab interpretation sentence (round 3 F08)", "L07.html:315", "PASS",
    "Now: 'the comparisons in Parts A to D are made on the unrounded values (floats and exact Fractions)'. Verified in the twin: part A omega>p on floats; part B exact Fractions; part C floats; part D floats. No table is referenced. Prior non-PASS row fixed.")
row("E3c-F09-L07-quiz-proposition-P2", "2.9 citation label (round 3 F09)", "L07.html:519", "PASS",
    "Explanation now reads 'Remark 1.3 and Problem P2'. Problem P2 exists (L07.html:381-387). Prior non-PASS row fixed.")
row("E3c-F10-dag-convex-combination", "2.9 DAG closure-external term (round 3 F10)", "L08.html:543", "PASS",
    "Now 'a weighted average of two numbers with nonnegative weights summing to one' (P2 solution). grep for 'convex' in L08 and L07 prose: no hits. Prior non-PASS row fixed.")

row("E3c-R42-notation-registry", "2.4 notation: every symbol vs notation/notation.json", "notation/notation.json (8 symbols, 'about' says Greek letters are local); L07.html, L08.html",
    "PASS",
    "Registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. None appears in L07 or L08 (grep). Greek letters alpha, beta, gamma, psi, tau, omega, eta, lambda, delta, kappa are local per the registry's about text. Macros used: \\E and \\Prob only (both registered); other commands are standard TeX. Local letters: L07 omega, eta, Gamma, Tail; L08 tau, a, psi, beta, gamma, lambda, delta, kappa, W (final wealth), P-bar. No registered symbol is reused.")
row("E3c-R43-cards-L07-L08", "2.7 retrieval cards tied to L07/L08 (all 41 read)", "course/modules/E/E3/cards.json ids E3-c118..E3-c158", "PASS",
    "All 41 cards with lesson L07 or L08 read. Numbers match the lesson text: 0.28579088/0.39125077/0.35355339 (c121), 0.278 (c122), 0.57158177 (c123, c130), 0.73045450, 0.58578644 (c125), 42.8686/39.1251/4.8788/3.9125 (c127), 3.7436 (c131), 49.8328 vs 50.5 (c132), 4180000/41 (c149), 99892.7670 and -1.072330 (c150), 99523.8095 (c151), 548.7805 and 5.4878 CU (c152), 2.91e-11 (c153, c156), 103125/106451.6129/100000 (c144). Citations: kahneman1979prospect (c134), ellsberg1961risk (c157), gilboa1989maxmin (c158) match registry titles. No contradiction found; no duplicate of another card in this set. Cards c118-c158 were not checked for duplicates against L01-L06 cards (other slices).")
row("E3c-R44-pytest-E3-and-lab-tests", "gate: pytest for E3 and lab-related tests", "tests/ (selection -k 'E3 or lab')", "PASS",
    ".venv/bin/pytest -k 'E3 or lab' -p no:cacheprovider -> '220 passed, 345 deselected in 45.35s'.")

ids = [r["id"] for r in R]
assert len(ids) == len(set(ids))
nonpass = [r for r in R if r["status"] != "PASS"]
counts = {"PASS": sum(1 for r in R if r["status"] == "PASS"), "FAIL": len(nonpass), "UNVERIFIABLE": 0}
frag = {
    "unit": "E3",
    "slice": "E3-c",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-c, round 4 (did not build E3; no shared context with builders)",
    "pin": "b276325",
    "base": "ccfdf4c (round-3 pin). Delta for the slice: course/modules/E/E3/L07.html, L08.html, tests/labs/E3/lab-E3-L07-1.py, lab-E3-L08-1.py changed; every L07/L08 row re-verified from scratch, no PASS row carried from round 3.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC4-E3-c (detached at b276325, .venv symlinked)",
    "scratch": "/tmp/c4_eta1 (ETA=1 copy of the L07 twin)",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Two rows FAIL: E3c-R17 (L08 interpretation claims 'the largest gap' is printed; the lab prints one gap) and E3c-R39 (L08 Example 2.5 claims the known-urn preference holds for any strictly increasing u with citations that do not state it). Both are wording/justification fixes; no number is wrong.",
        "All 10 round-3 non-PASS rows (F01-F10) were re-verified at b276325 and are fixed.",
        "Lab-slice mutants are not required (twins are demonstrations; mutation testing applies to project graders). mutants is empty.",
        "Not checked in this slice: L01-L06 pages, their twins and cards (other slices), project.html and grader, the hub index.html beyond hours, run_graders, mutate_graders, run_labs for other pages, and the full-unit cards duplicate scan.",
        "Commands run at b276325: check_pages (L07, L08), check_dag, run_labs (L07, L08), page_smoke (L07, L08), verify_refs --offline and --unit E3, ruff check and format --check on both twins, mypy --no-incremental on both twins, pytest -k 'E3 or lab' (220 passed). Twins run alone under python -I -W error (twin_page_check.out.txt).",
    ],
    "summary": {"rows": len(R), **counts},
}
out = Path("ledgers/E3/E3-c.json")
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), counts, [r["id"] for r in nonpass])
