"""Writes ledgers/E5/E5-b.json (round 1) for unit E5 slice b (L04-L06, their lab twins and their cards)."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD1-E5-b")
S = "ledgers/E5/scripts/E5-b-r1/"
RD = S + "rederive.out"
PAGE_TWIN = S + "page_twin_cards_check.out"
EXP = S + "expected_vs_output.out"

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- commands (2.5 labs, 2.9 structure, tooling gates) ----
row("E5b-r1-cmd-run-labs", "run_labs.py --unit E5 (all 11 E5 labs, includes L04-L06)", "tests/labs/E5/lab-E5-L0{4,5,6}-1.py",
    "PASS", f"`.venv/bin/python tools/run_labs.py --unit E5` exit 0, output 'run_labs E5: PASS (11/11)' (saved {S}run_labs_E5.out).")
row("E5b-r1-cmd-twin-expected", "twins alone under python -I -W error; stdout equals page expected block",
    "course/modules/E/E5/L04.html, L05.html, L06.html expected blocks", "PASS",
    f"`python3 -I {S}expected_vs_output.py <checkout>`: L04 exit 0, stderr 0 bytes, 26 lines, 0 differing; L05 21 lines, 0 differing; L06 32 lines, 0 differing (output in {EXP}).")
row("E5b-r1-cmd-page-eq-twin", "page lab code equals its twin", "L04.html, L05.html, L06.html <pre><code data-run>",
    "PASS", f"{PAGE_TWIN}: page_code==twin modulo final newline True for L04, L05, L06 (the tool ignores the final newline too).")
row("E5b-r1-cmd-check-pages", "check_pages.py --unit E5 --page L04/L05/L06", "course/modules/E/E5/L04-L06.html", "PASS",
    f"Exit 0 each; 'check_pages E5 L04: PASS', 'L05: PASS', 'L06: PASS' (saved {S}check_pages_L0{{4,5,6}}.out).")
row("E5b-r1-cmd-check-dag", "check_dag.py --unit E5 and --all", "concept uses and definitions in L04-L06", "PASS",
    f"'check_dag E5: PASS' (exit 0, {S}check_dag_E5.out); --all exit 0 (every unit PASS, {S}check_dag_all.out).")
row("E5b-r1-cmd-page-smoke", "page_smoke.py --unit E5 --pages L04 L05 L06 (Chromium, Pyodide labs)",
    "L04.html, L05.html, L06.html", "PASS",
    f"exit 0; each page PASS (zero console errors, math rendered, no external requests, labs in Pyodide); 'page_smoke E5: PASS' ({S}page_smoke_L04_L06.out).")
row("E5b-r1-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on each twin", "tests/labs/E5/lab-E5-L04-1.py, L05-1, L06-1",
    "PASS", f"ruff check clean, 'already formatted', mypy 'Success: no issues found in 1 source file' for each (saved {S}ruff_check_L0*.out, {S}mypy_L0*.out).")
row("E5b-r1-cmd-pytest-labs", "pytest tests/test_labs.py -k E5", "tests/test_labs.py", "PASS",
    f"exit 0, 11 tests passed (saved {S}pytest_labs_E5.out).")
row("E5b-r1-cmd-verify-refs", "verify_refs.py --unit E5 (live) and --offline", "references/references.json (keys hicks1937mr, phelps1968money)",
    "PASS", f"live: 'live re-verification of E5: 4 of 560 entries, 0 problems' ({S}verify_refs_E5.out); offline: '560 entries, 0 problems' ({S}verify_refs_offline.out).")
row("E5b-r1-cmd-rederive", "independent Fraction re-derivation of every number in L04-L06 prose, quiz, lab and Part B path",
    S + "rederive.py", "PASS", f"`python3 -I {S}rederive.py` exit 0, 147 CHECK lines all OK, 'MISMATCHES: none' ({RD}).")

# ---- registry ----
row("E5b-r1-ref-hicks", "citation: data-cite hicks1937mr (L04 references)", "course/modules/E/E5/L04.html:567 and L05.html:487",
    "PASS", "Registry record: Hicks, 'Mr. Keynes and the \"Classics\"; A Suggested Interpretation', Econometrica 5(2), 147, 1937, doi 10.2307/1907242. "
    "Live Crossref `curl https://api.crossref.org/works/10.2307/1907242` (HTTP 200) returns title, container, volume 5, issue 2, page 147, year 1937, author Hicks J. R. — identical. "
    "The page attributes no result to Hicks (L04 says so explicitly; L05 says the key is not cited).")
row("E5b-r1-ref-phelps", "citation: data-cite phelps1968money (L06 references)", "course/modules/E/E5/L06.html:525",
    "PASS", "Registry record: Phelps, 'Money-Wage Dynamics and Labor-Market Equilibrium', JPE 76(4, Part 2), 678-711, 1968, doi 10.1086/259438. "
    "Crossref `curl https://api.crossref.org/works/10.1086/259438` (HTTP 200) matches title, container, volume, issue, pages and year. "
    "L06 says it has not read the paper and attributes no result to it; no claim in L06 is attributed to Phelps (checked every L06 sentence).")

# ---- L04 ----
row("E5b-r1-l04-why", "2.9 why-it-matters length and cross-references", "L04.html p.why-it-matters", "PASS",
    "Counted 120 words (limit 120). Every cross-reference in it resolves: Definition 1.1, Definition 2.1, Proposition 3.2, Remark 4.4, Definition 4.1 (all present as block titles).")
row("E5b-r1-l04-s1", "§1 definition and remark (business cycle, output gap, what 'cycle' does not claim)", "L04.html:58-66", "PASS",
    "Definitions only; no numerical claim. Output gap sign (positive above trend) matches the definition text. Remark 1.2 makes no fixed-interval claim.")
row("E5b-r1-l04-s2", "§2 Definition 2.1, Assumptions A1-A4, Derivation 2.2", "L04.html:72-100", "PASS",
    f"Derivation 2.2 re-derived: Y - cY = c0 - c Tax + b0 + G - b i, so (1-c)Y + b i = A (rederive.out, L04 A(G=1)=3). Assumption A2 gives 0<c<1, b>=0, d>=0, h>0 (text line 88); used in Prop 3.2 and 4.3.")
row("E5b-r1-l04-s3", "Definition 3.1 (D = h(1-c)+bd) and Proposition 3.2 (unique equilibrium) with its proof", "L04.html:109-127", "PASS",
    "Re-derived with Fractions: D=5/4 at the lab parameters (rederive 'L04 D'); Cramer's formulas (hA+b m)/D and (dA-(1-c)m)/D; the determinant is -D; both substitution checks reproduce A and m (both algebraically re-derived). A1-A4 are stated; D>0 follows from A2.")
row("E5b-r1-l04-s4-prop42", "Proposition 4.2 partial derivatives and proof", "L04.html:137-154", "PASS",
    "Partials h/D, b/D, -ch/D, d/D, -(1-c)/D re-derived from the closed forms (proof step: dA/dG=1, dA/dTax=-c). Checked numerically at the lab parameters: L04 multiplier 4/5 = h/D, monetary 8/5 = b/D, interest -1/5 = -(1-c)/D (rederive 'L04 b/D', '-(1-c)/D').")
row("E5b-r1-l04-s4-prop43", "Proposition 4.3 (h/D <= 1/(1-c), equality iff bd=0) and proof", "L04.html:156-168", "PASS",
    "Proof step checked: h/D <= 1/(1-c) iff h(1-c) <= D, iff 0 <= bd (multiply by D(1-c)>0). Grade T matches a page-proved result. Numerically h/D=4/5 < 4 at bd=1 (rederive 'L04 h/D').")
row("E5b-r1-l04-remarks", "Remark 4.4 (b=0 benchmark) and Remark 4.5 (di/dG = d/D >= 0; investment fall bd/D)", "L04.html:171-178", "PASS",
    "b=0 gives D=h(1-c), multiplier 1/(1-c), monetary 0 (rederive 'L04 Part D multiplier b=0' = 4). Remark 4.5 re-derived: I = b0 - b i gives dI/dG = -bd/D. Why-it-matters cites Remark 4.4 for 'strictly smaller'; Remark 4.4 states the Prop 4.3 consequence in its second sentence, so the citation holds.")
row("E5b-r1-l04-lab", "Lab 1 (lab-E5-L04-1): code equals twin, expected equals output, hypothesis numbers",
    "L04.html:180-333; tests/labs/E5/lab-E5-L04-1.py", "PASS",
    f"Twin output (26 lines) equals the page expected block byte for byte ({EXP}). Hypothesis predictions 28/5, 4/5, 2/5-step values, 8/5, -1/5, 4 all re-derived (rederive 'L04 Y*', 'L04 dY G->11/10', 'L04 dY G->2', 'L04 monetary multiplier'). Lab docstring matches code (seeded? no random draws: none in the code).")
row("E5b-r1-l04-interp", "Lab 1 interpretation paragraph (every number and every printed token)", "L04.html:332",
    "PASS", "Each printed value cited (5.6000000000, 0.8000000000, 2/25, 1/25, 2/5, 8/5, -1/10, -1/5, multiplier_below_cross True, equals_one_over_one_minus_c True) matches the twin's output in " + EXP + ". Says 'one parameter set'; no economy claim.")
row("E5b-r1-l04-canon", "§5 Where the canon breaks (5 bullets)", "L04.html:338-342", "PASS",
    "Cross-lesson claims checked: L05 adds a price level (L05 A1-A2); L07 'treats as a rule that sets the nominal policy rate from inflation and the output gap' matches L07 Definition 1.4 (Taylor rule). Other bullets are model statements.")
row("E5b-r1-l04-misc", "§6 Misconceptions (3)", "L04.html:350-360", "PASS",
    "Three misconceptions, each with its wrong belief, correction and evidence. Numbers 0.8000000000, 4, 4/5, 2/5 re-derived.")
row("E5b-r1-l04-prob-M", "Problem set Mechanics M1-M3", "L04.html:370-390", "PASS",
    "M1 (c=1/2,b=2,d=1,h=2,A=4,m=3): D=3, Y*=14/3, i*=5/6, IS and LM checks 4 and 3 (rederive 'L04 M1 D/Y*/i*'). M2: h/D=2/3, benchmark 2, ratio 1/3. M3: b/D=2/3, -(1-c)/D=-1/6.")
row("E5b-r1-l04-prob-P", "Problem set Proof P1-P3", "L04.html:395-416", "PASS",
    "P1 wording now says 'state which definition makes c the marginal propensity to consume' (Definition 2.1 defines c) and A2 gives 1-c>0; the round-13 defect is gone. P2: D>=h(1-c)>0 for b=0 or d=0; strict inequality needs bd>0 (b>0 and d>0). P3: IS slope -(1-c)/b, LM slope d/h (rederive 'L04 P3 IS slope (c=1/2, b=2)').")
row("E5b-r1-l04-prob-E", "Problem set Empirical E1-E3", "L04.html:421-440", "PASS",
    "E1: ratio di/dY = 1/25 / (2/25) = 1/2 = d/h, exact for any dG != 0 since the LM relation gives d dY = h di. E2: -1/10 over 1/2 gives -1/5 = -(1-c)/D. E3: 0.8/4 = 1/5 = h(1-c)/D. Values rederived.")
row("E5b-r1-l04-prob-R", "Problem set Research R1-R3", "L04.html:446-466", "PASS",
    "R1 (d=0): D=h(1-c), multiplier 1/(1-c), di/dG = 0, LM horizontal (i=-m/h). R2 (b=0): dY/dm = 0, IS (1-c)Y=A fixes Y. R3: di/dG = d/D >= 0, zero iff d=0. All re-derived.")
row("E5b-r1-l04-keyres", "§8 Key results table (4 rows)", "L04.html:474-478", "PASS",
    "Each row matches a proposition or derivation and its grade (T). Lab references point to Parts B and A (the Part B benchmark 4 and multiplier 0.8 agree).")
row("E5b-r1-l04-quiz", "§9 retrieval quiz (10 items, answer keys and explanations)", "L04.html:484-563", "PASS",
    "10 items within 8-15. Correct options: cycle = output about trend; exactly one equilibrium; spending multiplier strictly smaller when bd>0; sign of di/dm negative; IS slopes down; prices fixed = A3. Numeric answers 5.6, 0.8, 4, -0.2 each re-derived and tolerances set.")
row("E5b-r1-l04-refs", "§10 references paragraph", "L04.html:567-568", "PASS",
    "Names hicks1937mr, states the lesson has not read it and attributes no result. Registry record verified (E5b-r1-ref-hicks).")

# ---- L05 ----
row("E5b-r1-l05-why", "why-it-matters length and cross-references", "L05.html:52", "PASS",
    "119 words (limit 120). Cross-references: Assumption A1, Proposition 2.2, Definition 1.1, Proposition 2.1, Proposition 3.1 all exist. 'Lesson 6 ... turns it into a Phillips curve' is a signpost to L06, not a use; see DAG row.")
row("E5b-r1-l05-model", "§1 Assumptions A1-A3, Definition 1.1, Remark 1.2 (linearity from IS-LM)", "L05.html:58-81", "PASS",
    "A1 slope -eta < 0 (a, eta > 0); A2 nu > 0; A3 P^e = P. Remark 1.2: IS-LM output affine in m-bar = M/P with slope b/D, so affine in 1/P; zero slope iff b=0, which is Lesson 4 Remark 4.4 (b=0 gives dY/dm = 0, rederive 'L04 monetary multiplier' and 'L04 Part D').")
row("E5b-r1-l05-prop21", "Proposition 2.1 (short-run equilibrium) and proof", "L05.html:85-97", "PASS",
    "Re-derived: P*=(a-Ybar+nu Pe)/(eta+nu), Y*=a-eta P*; Y*-Ybar = nu(P*-Pe). Lab values P*=6/5 and Y*=1040 (rederive 'L05 P*', 'L05 Y*', 'L05 AS residual'). Exactly one solution since eta+nu>0.")
row("E5b-r1-l05-prop22", "Proposition 2.2 (demand shock) and proof; Remark 2.3", "L05.html:99-116", "PASS",
    "dP = da/(eta+nu), dY = nu da/(eta+nu) re-derived (rederive 'L05 dP shock 30', 'L05 dY shock 30' = 20). Bounds 0<share<1 from eta,nu>0 (P2 identity). Remark 2.3: share -> 1 as nu grows (1/(1+eta/nu)).")
row("E5b-r1-l05-lab", "Lab 1 (lab-E5-L05-1): code equals twin, expected equals output, hypothesis numbers",
    "L05.html:118-232; tests/labs/E5/lab-E5-L05-1.py", "PASS",
    "Twin output (21 lines) equals the expected block (" + EXP + "). Hypothesis numbers 1.2, 1040, 0.1, 20, 1.6, 1.9 and the Part D table (shares 1/3,1/2,2/3,4/5,8/9; price changes 1/5, 3/20, 1/10, 3/50, 1/30; output changes 10,15,20,24,80/3) all rederived. Code uses no random draws.")
row("E5b-r1-l05-interp", "Lab 1 interpretation paragraph", "L05.html:231", "PASS",
    "Every printed token cited is in the twin output: 1.200000, 1040.000000, 0.000000 residuals, exact_match True, 0.333333 to 0.888889, 0.200000 to 0.033333, long_run_is_short_run_fixed_point True.")
row("E5b-r1-l05-prop31", "Proposition 3.1 (long-run equilibrium), proof and Remark 3.2", "L05.html:236-253", "PASS",
    "P_LR=(a-Ybar)/eta, Y_LR=Ybar; fixed-point proof algebra checked: (a-Ybar)(1+nu/eta)/(eta+nu) = (a-Ybar)/eta. Remark 3.2 shock 30 raises long-run price by 0.3 (rederive 'L05 LR dP = da/eta').")
row("E5b-r1-l05-canon", "§4 Where the canon breaks (4 bullets)", "L05.html:258-261", "PASS",
    "Bullet 2 formulas re-derived: dP=(da+nu dPe)/(eta+nu), dY=nu(da-eta dPe)/(eta+nu). Bullet 3: a=1190, Pe=1 gives Y=1060, 60 above potential (rederive 'L05 R3 output gap').")
row("E5b-r1-l05-misc", "§5 Misconceptions (3)", "L05.html:269-279", "PASS",
    "Demand 1060 at P=1 and 1000 at P=1.6 (rederive 'L05 misc demand'); 20 of 30 = two thirds (nu=200); long-run output 1000 before and after.")
row("E5b-r1-l05-prob-M", "Problem set Mechanics L05-M1 to M3", "L05.html:291-308", "PASS",
    "M1 P*=21/20, Y*=995 (supply check 995). M2 share 3/4, dY=30, dP=1/5. M3 LR 1 and 7/5, output 1000. All rederived.")
row("E5b-r1-l05-prob-P", "Problem set Proof L05-P1 to P3", "L05.html:316-332", "PASS",
    "P1 uniqueness by subtracting the two demand and two supply equations gives (eta+nu)(P2-P1)=0. P2 identity 1-nu/(eta+nu)=eta/(eta+nu)>0 (eta>0). P3 numerator (a-Ybar)(eta+nu)/eta, so P*=(a-Ybar)/eta.")
row("E5b-r1-l05-prob-E", "Problem set Empirical L05-E1 to E3", "L05.html:341-358", "PASS",
    "E1 nu=400: share 4/5, dY 24, dP 3/50 = 0.06 (rederive 'L05 E1'). E2 increments 5,5,4,2.666667 and exact 8/3 = 30(8/9-4/5) (rederive 'L05 E2 increment'). E3 1.9-1.6=0.3 gives da=30; 8/5 and 19/10 are exact.")
row("E5b-r1-l05-prob-R", "Problem set Research L05-R1 to R3", "L05.html:366-384", "PASS",
    "R1: H(P)=F(P)-Ybar-nu(P-Pe) continuous, strictly decreasing, H->inf at 0+ and -inf at infinity (F(P)<=F(1) for P>=1); IVT plus monotonicity gives one zero. R2: P*=(190+260)/300=3/2, Y*=1040 (rederive 'L05 R2 P*', 'L05 R2 Y*'). R3: Y=1060 gives gap 60.")
row("E5b-r1-l05-keyres", "§7 Key results table (5 rows)", "L05.html:395-399", "PASS",
    "Each row matches a proposition (T) or a lab part marked exact; all values rederived.")
row("E5b-r1-l05-quiz", "§8 retrieval quiz (10 items)", "L05.html:409-481", "PASS",
    "10 items. Correct: P*=1.2; Y*=1040; slope -eta; dY=20; dP=0.1; share strictly between 0 and 1; larger nu flatter; dP_LR=0.3; LR output potential; LR price needs A3. Numeric answers and explanations re-derived.")
row("E5b-r1-l05-refs", "§9 references paragraph", "L05.html:487", "PASS",
    "Cites no outside source and states hicks1937mr is not cited. The key appears only as text, not as data-cite.")

# ---- L06 ----
row("E5b-r1-l06-why", "why-it-matters length and cross-references", "L06.html:52", "PASS",
    "117 words (limit 120). A3 and Definition 1.1 and 1.2 cross-references resolve. Adaptive-expectations claim matches Corollary 3.2.")
row("E5b-r1-l06-defs", "§1 variables, Assumptions A1-A3, Definitions 1.1 and 1.2", "L06.html:56-85", "PASS",
    "pi_t, P^e_t = P_{t-1}(1+pi^e_t), A1 P_{t-1}>0 and nu>0, A2 kappa>0, A3 pi^e_t = pi_{t-1}. Definition 1.1 slope kappa/(nu P_{t-1}); Definition 1.2 natural rate unique because the relation is strictly decreasing in u. 5 percent = 0.05 and 3 percent = 0.03 are consistent with the rule.")
row("E5b-r1-l06-prop21", "Proposition 2.1 (Phillips form) and proof", "L06.html:89-105", "PASS",
    "Derivation re-checked: P_t = P^e_t - (kappa/nu)(u_t-un); subtracting P_{t-1} and dividing gives pi_t = pi^e_t - beta(u_t-un) (the first term equals pi^e exactly). '100 percentage points' per unit of u (u is a decimal). rederive 'L06 beta at P=6/5' = 5/6.")
row("E5b-r1-l06-remark22", "Remark 2.2 (slope depends on P_{t-1}; kappa=nu=200 gives beta=1/P)", "L06.html:107-110", "PASS",
    "beta=1 at P=1 and 5/6 at P=6/5 (rederive 'L06 R1 ratio' = 6/5 equals 1.2/1).")
row("E5b-r1-l06-lab-A", "Lab 1 Part A: one-period levels vs Phillips form, u=0.06", "L06.html:112-263 (Part A); lab-E5-L06-1.py", "PASS",
    "pe=1.236, price 1.226, pi=13/600=0.021667 both ways, beta 0.833333, identity True (rederive 'L06 Part A pe/price/inflation levels/Phillips' all OK). Hypothesis '13/600 or 0.021667' matches.")
row("E5b-r1-l06-lab-B", "Lab 1 Part B: 12-period seeded SIMULATED path (identity, changes, signs, zero counts)",
    "L06.html:112-263 (Part B); lab-E5-L06-1.py", "PASS",
    "Independent recursion pi_t = pi_{t-1} - beta(u_t-un) with seed 20261028 reproduces every printed draw, inflation (6dp) and change (6dp) for t=1..12, with zero_gap_periods 0 and no_change_periods 0 (rederive 'L06 Part B t=1..12' all OK). Interpretation's claim that no_change_only_at_natural_rate holds only vacuously is correct.")
row("E5b-r1-l06-lab-C", "Lab 1 Part C: one-period change grid at P=6/5, zero at u=5%, sign on each side",
    "L06.html:212-261", "PASS", "Grid 3.0% to 7.0%: changes 0.016667, 0.012500, 0.008333, 0.004167, 0, -0.004167, ... -0.016667 (rederive 'L06 misc2 change at 3%', 'L06 E1', 'L06 quiz q4'). slope 0.833333.")
row("E5b-r1-l06-lab-code", "Lab 1 code equals twin; expected block equals output; docstring and hypothesis match the code",
    "tests/labs/E5/lab-E5-L06-1.py; L06.html:115-261", "PASS",
    "Page code equals twin (" + S + "page_twin_cards_check.out); expected block equals output 32 lines (" + EXP + "); twin runs with -I -W error exit 0 and stderr 0 bytes; the labels SIMULATED and seeded match the code (random.Random(SEED)).")
row("E5b-r1-l06-prop31", "Proposition 3.1 (pi_t=pi^e_t iff u=un iff Y=Ybar) and proof", "L06.html:267-275", "PASS",
    "Proof: pi_t - pi^e_t = -beta_t(u_t-un) with beta>0; A2 gives Y-Ybar=-kappa(u-un). Both equivalences hold.")
row("E5b-r1-l06-cor32", "Corollary 3.2 (adaptive expectations: pi_t - pi_{t-1} = -beta(u-un)) and proof", "L06.html:277-285", "PASS",
    "With pi^e_t=pi_{t-1} the identity follows; change zero iff u=un since beta>0. Used correctly in quiz q3 (sign negative above un).")
row("E5b-r1-l06-remark33", "Remark 3.3 (natural rate not measured here; not a floor, cross-ref §5)", "L06.html:287-290", "PASS",
    "Consistent with Definition 1.2 and Proposition 3.1; the §5 cross-reference points to the Misconceptions section, which says the natural rate is not a lower bound.")
row("E5b-r1-l06-canon", "§4 Where the canon breaks (4 bullets)", "L06.html:295-298", "PASS",
    "Supply-shock bullet: u = un + v/beta, re-derived (rederive 'L06 R2 u*' = 0.062). Bullet on slope depending on P_{t-1} matches Remark 2.2.")
row("E5b-r1-l06-misc", "§5 Misconceptions (3) with numbers", "L06.html:306-316", "PASS",
    "Gap -0.01 at beta=5/6: change +1/120 = 0.008333 (rederive 'L06 misc1'). Gap -0.03 (3%): +1/60 = 0.016667 (rederive 'L06 misc2'). Part B non-zero changes in all 12 periods (expected block). Third misconception correct under A3.")
row("E5b-r1-l06-prob-M", "Problem set Mechanics L06-M1 to M3", "L06.html:326-346", "PASS",
    "M1 beta=1/2, pi=0.03. M2 beta=4/5, pi=0.048 (above expected by 0.008). M3 pi=0.02 at u=un and 0.005 at un+0.03 (falls 0.015). All rederived.")
row("E5b-r1-l06-prob-P", "Problem set Proof L06-P1 to P3", "L06.html:353-371", "PASS",
    "P1 derivative -beta (linear in u). P2 same denominator, so pi=pi^e iff P=P^e iff Y=Ybar (nu>0). P3 kappa>0 gives u~=un.")
row("E5b-r1-l06-prob-E", "Problem set Empirical L06-E1 to E3", "L06.html:376-396", "PASS",
    "E1 1/120 = 0.008333 (rederive). E2 counts from the twelve printed lines: positive gaps in periods 1,2,3,4,5,7,8,11,12 (nine), negative 6,9,10 (three); all changes have the opposite sign (checked against the expected block). E3: beta_1=5/6; change -0.0048333 prints -0.004833; 5.5% row gives -0.004167 (rederive 'L06 E3 change period1', '5.5%').")
row("E5b-r1-l06-prob-R", "Problem set Research L06-R1 to R3", "L06.html:401-421", "PASS",
    "R1 ratio 6/5. R2 u* = 0.05 + 0.01/(5/6) = 0.062 (6.2 percent). R3 names data and modelling needs without giving a value; no numerical claim about beta.")
row("E5b-r1-l06-keyres", "§7 Key results table (6 rows; Part B row graded C)", "L06.html:431-436", "PASS",
    "Rows 1-3 T (propositions); row 4 T (Part A exact); row 5 C naming the SIMULATED Part B path, per BLUEPRINT grade rule for lab-read results; row 6 T (Part C exact).")
row("E5b-r1-l06-quiz", "§8 retrieval quiz (10 items)", "L06.html:446-520", "PASS",
    "10 items. Correct: natural rate = Y=Ybar; beta=1; sign negative above un; 0.008333; A3 expected inflation; 0.021667; no shock term; beta proportional to 1/P; 0.048; check trivially true. Numeric answers and explanations re-derived.")
row("E5b-r1-l06-refs", "§9 references paragraph", "L06.html:525-526", "PASS",
    "Names phelps1968money; states the lesson has not read the paper and attributes no result to it. Registry record verified (E5b-r1-ref-phelps).")

# ---- cards ----
row("E5b-r1-cards-L04", "cards L04 (c053-c070, c134; 19 cards): every card against lesson text", "course/modules/E/E5/cards.json", "PASS",
    "All 19 read against L04 text. Each card's cited key (Definition 1.1, 2.1, 3.1, 4.1, Prop 3.2, 4.2, 4.3, Remark 1.2, 4.4, 4.5, Derivation 2.2, A3) appears in the lesson; numbers 28/5, 4/5, 4, 2/5, 2/25 agree with the lab output (" + S + "page_twin_cards_check.out CARD refs missing from own lesson: []).")
row("E5b-r1-cards-L05", "cards L05 (c071-c087, c137, c139, c140; 20 cards): every card against lesson text", "course/modules/E/E5/cards.json", "PASS",
    "All 20 read against L05 text. Numbers 1.2, 1040, 0.1, 20, 0.333333..0.888889, 0.200000..0.033333, 1.6, 1.9, 1000, 1060, 0.3 agree with the lab output and the re-derivation. Cited keys all exist in L05.")
row("E5b-r1-cards-L06", "cards L06 (c088-c104, c136, c138; 19 cards): every card against lesson text", "course/modules/E/E5/cards.json", "PASS",
    "All 19 read against L06 text. c099 '+0.008333', c100 '0.016667 at 3 percent', c102 '0.021667 = 13/600', c104 '0.000000 at 5 percent, 0.008333 at 4 percent' agree with the expected block. c103 is graded C with basis 'Lab 1, Part B (SIMULATED, one seed)', matching the key-results table.")
row("E5b-r1-card-c060", "card E5-c060 'What is an equilibrium of IS-LM?' (scope word 'only')", "course/modules/E/E5/cards.json (E5-c060, back)", "FAIL",
    "Back reads: 'The word is used only in that sense (Definition 3.1).' The lesson, L04.html line 105 and 3, says only 'In this lesson the word has that sense.' Nothing in the lesson asserts exclusivity (no sentence says the word is used nowhere else). Scope word without basis (verifier rule 4). " + S + "page_twin_cards_check.out lists it under SCOPE-WORD CARD.",
    fix="In cards.json, E5-c060 back: replace 'The word is used only in that sense (Definition 3.1).' with 'In this lesson the word has that sense (Definition 3.1).' (matches L04.html line 105). Re-run the card check.")
row("E5b-r1-cards-dup", "full card scan for duplicates (139 cards, unit-wide)", "course/modules/E/E5/cards.json", "PASS",
    "No duplicate ids and no duplicate fronts (normalised). " + PAGE_TWIN + " 'duplicate_fronts=[] duplicate_ids=[]'. Id numbering: c135 is absent (c001-c140 otherwise present); numbering is upward, so noted only.")
row("E5b-r1-cards-coverage", "card coverage of definitions, theorems, key formulas and misconceptions of L04-L06", "cards.json, L04-L06", "PASS",
    "Each definition (1.1, 1.2, 2.1 items, 3.1, 4.1, A1-A3 of L05, A2/A3 of L06), each proposition/corollary (L04 3.2, 4.2, 4.3; L05 2.1, 2.2, 3.1; L06 2.1, 3.1, Cor 3.2) and each of the 9 misconceptions has at least one card.")

# ---- structure, prose, grades, notation, DAG ----
row("E5b-r1-struct", "2.9 structure: §4.2 order and minimum counts for L04-L06", "L04.html, L05.html, L06.html", "PASS",
    "Order: why-it-matters, numbered core sections, inline labs, canon-breaks, misconceptions (3 each), problem set (3 per tier: Mechanics, Proof, Empirical, Research), key-results table, quiz (10 items each, within 8-15), references. Debate brief not required (no debate key, E5 plan).")
row("E5b-r1-banned", "BUILDER_RULES §1.2-1.4 banned phrases and placeholders", "L04-L06 pages and lab twins", "PASS",
    "Scanned for TODO, TBD, lorem, ellipsis, 'for brevity', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', 'it can be shown', 'roughly', 'historically', 'about' (as ordinary word only). None found.")
row("E5b-r1-process", "2.9 / 12: no process words in learner text", "L04-L06 pages", "PASS",
    "Scanned for builder, verifier, agent (only the economic sense: 'no agents who take prices as given'), draft, placeholder. No process words.")
row("E5b-r1-scope", "rule 4: scope words (only, all, always, every, any, same, exactly, drives, never, no, each, unique)",
    "L04-L06 prose (sentences containing scope words: L04 53, L05 31, L06 57)", "PASS",
    "Each sentence with a scope word was read. Every one is backed by a computation, a stated hypothesis or a definition (for example 'exactly one' under A1-A4 in Prop 3.2; 'the only moving variables' in §5 with A1-A3; 'vacuously' flagged in L06). The only unsupported one is card E5-c060 (separate FAIL row).")
row("E5b-r1-notation", "rule 13: every symbol vs notation/notation.json", "L04-L06 pages", "PASS",
    "Registry symbols: T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q and macros \\E, \\Prob, \\R etc. None appears in L04-L06 (grep of KaTeX macros: \\nu, \\eta, \\bar, \\pi, \\partial, \\ast, \\Delta, \\beta, \\kappa, \\mathrm, \\frac, \\qquad, \\ge, \\le, \\to, \\infty, \\tilde, \\text, \\neq, \\cdot, \\times, \\bigl, \\bigr, \\quad - all standard TeX). Lesson-local letters (beta, kappa, eta, nu, pi, H, F, v, D, A, m-bar) are defined where first used (A1-A2, Definition 1.1, Definition 3.1, §2, R1).")
row("E5b-r1-dag", "rule 14: DAG (check_dag, closure, definition once, no use before definition)", "L04-L06 concept links and dfn", "PASS",
    "check_dag E5 PASS. comparative-statics and competitive-equilibrium are in E5's prerequisite closure (E1 is the prerequisite, curriculum/02-economics-finance-core.yaml:159). is-lm-model linked from L05 to L04#def-is-lm-model; ad-as-model linked from L06 to L05#def-ad-as-model; each concept defined once (business-cycle and is-lm-model in L04, ad-as-model in L05, phillips-curve and natural-rate-of-unemployment in L06). Note: L05 why-it-matters names 'a Phillips curve' as a signpost to L06, not a use.")
row("E5b-r1-hours", "hours arithmetic (hub split vs curriculum; each page hours)", "index.html:29, L04-L06 data-hours", "PASS",
    "Hub data-hours-lessons=80, data-hours-project=30 (sum 110). Curriculum hours 110 (curriculum/02-economics-finance-core.yaml:158). Eight lessons of 10 hours = 80. L04, L05, L06 each data-hours=10 and eyebrow '10 study hours'.")
row("E5b-r1-simulated", "SIMULATED labels and no data passed off as real", "L04-L06 labs and key results", "PASS",
    "L06 lab carries the SIMULATED label in hypothesis, docstring and key-results grade C. L04 and L05 inputs labelled 'illustrative parameters, not data' and deterministic.")
row("E5b-r1-figures", "2.8 figures (charts, SVG title/desc, interactive figures)", "L04-L06", "PASS",
    "No <svg> or figure in L04-L06 (grep count 0 each). Nothing to check.")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}

frag = {
    "unit": "E5",
    "slice": "b",
    "round": 1,
    "round_note": "Round 1 of this campaign: first independent verification of E5-b at pin d0f39c09 (detached checkout /Users/billyribeiro/.fanout/wt/verifyD1-E5-b). An earlier fragment for E5-b (round 13 at pin 762f636d, FAIL) is replaced by this round-1 fragment as instructed; its scripts directory E5-b-r1 names are not reused (this round's scripts are new files in ledgers/E5/scripts/E5-b-r1/). Every L04-L06 row was re-verified from scratch; no row carried.",
    "verifier": "Claude Haiku 5.5, independent verifier for E5-b round 1 (did not build E5; re-derived every L04-L06 number with exact Fractions and re-ran every command row on pin d0f39c09)",
    "pin": "d0f39c09598ffefaf0ec18d5d1077cfacd42998b",
    "base": "d0f39c09598ffefaf0ec18d5d1077cfacd42998b (no earlier round in this campaign; the round-13 base 460b6963 belongs to the previous campaign)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD1-E5-b (detached at d0f39c09, .venv symlinked)",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyD1-E5-b/ledgers/E5/scripts/E5-b-r1",
    "verified_at": "2026-11-02T16:30:00Z",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "hicks1937mr and phelps1968money: live Crossref re-resolution matched the registry record (E5b-r1-ref-hicks, E5b-r1-ref-phelps). No update needed.",
        "verify_refs --unit E5 live: '4 of 560 entries, 0 problems'; --offline: '560 entries, 0 problems'."
    ],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. Verifier rules require mutants for project graders only; lessons and lab twins are demonstrations (ruling in the campaign brief), so no mutant rows.",
        "Card id E5-c135 is absent; ids c001 to c140 are otherwise present. Numbering runs upward, so this is noted, not failed.",
        "L05 why-it-matters names 'a Phillips curve' as a forward signpost to Lesson 6 without linking or defining it. Not a use under BUILDER_RULES §1.10; noted only.",
        "L04 why-it-matters cites Remark 4.4 for the strict-inequality claim; Remark 4.4 states the Proposition 4.3 consequence, so the citation holds.",
        "L06 Part B cannot falsify the identity claim on this seed: no period has zero gap or unchanged inflation, so no_change_only_at_natural_rate holds vacuously. The lesson says so in its interpretation, and Part C carries the zero test.",
        "The scope sweep read 141 sentences containing scope words across L04-L06; only card E5-c060 is unsupported."
    ],
    "summary": {
        "counts": counts,
        "rows": len(rows),
        "fails": [r["id"] for r in rows if r["status"] != "PASS"],
        "what_was_checked": "All 58 cards of L04-L06 read; all L04-L06 prose read line by line (lesson HTML 47 + 44 + 44 KB); all three lab twins run under python -I -W error; expected blocks diffed; page code equals twin; numbers re-derived with exact Fractions (147 checks); checks run on pin d0f39c09.",
        "not_checked": [
            "Rendered appearance in light and dark mode at 360 px (page_smoke ran headless Chromium checks; no manual screenshot inspection was done).",
            "Hub, project and other lessons of E5 (outside slice b).",
            "The published content of Hicks (1937) and Phelps (1968) beyond their Crossref metadata; neither lesson makes a claim about their content, so no attribution was checked against the text.",
        ],
    },
}

out = ROOT / "ledgers/E5/E5-b.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, "verdict", verdict)
