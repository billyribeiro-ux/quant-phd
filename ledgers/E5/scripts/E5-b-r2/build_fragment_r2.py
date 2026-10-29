"""Writes the round-2 fragment for E5-b. Statuses are set from the checks recorded in the evidence strings."""
import json
import sys
from pathlib import Path

root = Path("/tmp/verifyC2-E5-b")
prev = json.loads(Path("/tmp/fanout-frags/C-E5-b.round1.json").read_text())
CMD = "ledgers/E5/scripts/E5-b-r2/cmp_r2.py"
REC = "ledgers/E5/scripts/E5-b-r2/recompute_r2.py"

ev = {
 "E5-b-cmd-check-pages": ("PASS", "Round 2, pin e22feb3: .venv/bin/python tools/check_pages.py --unit E5 --page L04 / L05 / L06 -> 'check_pages E5 L04: PASS', 'check_pages E5 L05: PASS', 'check_pages E5 L06: PASS'."),
 "E5-b-cmd-check-dag": ("PASS", "tools/check_dag.py --unit E5 -> 'check_dag E5: PASS'. Note: the tool's closure and the plan's computed closure (plans/E5-build-plan.md section 4: {E1, M1, M2, P0.1}) are the reference; the brief's 'AC1, S0, S2' does not match the plan and is not used."),
 "E5-b-cmd-run-labs": ("PASS", "tools/run_labs.py --unit E5 -> 'run_labs E5: PASS (11/11)'; --page L04, L05, L06 each 'PASS (1/1)'."),
 "E5-b-lab-L04-embedded": ("PASS", f"{CMD} run with python -I -W error from the checkout: 'L04 code_equals_twin True exit 0 stderr_empty True', 'L04 expected_equals_run True lines 26'."),
 "E5-b-lab-L05-embedded": ("PASS", f"{CMD}: 'L05 code_equals_twin True exit 0 stderr_empty True', 'L05 expected_equals_run True lines 21'."),
 "E5-b-lab-L06-embedded": ("PASS", f"{CMD}: 'L06 code_equals_twin True exit 0 stderr_empty True', 'L06 expected_equals_run True lines 32'."),
 "E5-b-lab-hypothesis-L04": ("PASS", f"{REC} (own Fraction re-derivation by Cramer's rule, not the lab code): 49 PASS, 0 FAIL in /tmp/E5-v/E5-b/r2/recompute.out. Values checked: Y* 28/5, i* 4/5, dY 2/25 and di 1/25 for G 1 to 11/10, multiplier 4/5 for both steps, di 2/5, monetary multiplier 8/5 and -1/5, b=0 multiplier 4, benchmark 4."),
 "E5-b-lab-hypothesis-L05": ("PASS", f"{REC}: L05 P* 6/5, Y* 1040, dP 1/10, dY 20, long-run prices 8/5 and 19/10, Part D dY = 30 nu/(eta+nu) for nu 50..800 (all PASS). Hypothesis values in L05.html:120 match."),
 "E5-b-lab-hypothesis-L06-AC": ("PASS", f"{REC}: 'L06 A inflation 13/600' and 'L06 A form 13/600' PASS. Part C: the change is -(5/6)(u-0.05) on the grid u = 3%..7% (steps of 0.5 point), giving 0.016667, 0.0125, 0.008333, 0.004167, 0, -0.004167, -0.008333, -0.0125, -0.016667 by hand (linear in the step); these match the printed grid."),
 "E5-b-lab-L04-interpretation": ("PASS", "Each value cited at L04.html:328 and in misconceptions (L04.html:347-351) appears in the embedded output (cmp_r2 expected_equals_run True); 'multiplier_below_cross True' is the strict inequality of Proposition 4.3 at bd>0."),
 "E5-b-lab-L05-interpretation": ("PASS", "Values at L05.html:229 (1.200000, 1040.000000, 20.000000, 0.100000, 1.6/1.9, long_run_output 1000, Part D 0.333333 to 0.888889 and 0.200000 to 0.033333) match the embedded output and recompute; the 60-point gap at P=1 (L05.html:258 and 380) equals 1060-1000 (recompute 'L05 R2' and the Part B output)."),
 "E5-b-lab-L06-interpretation": ("PASS", f"L06.html:262 values (0.021667, identity True, identity_every_period True, zero_gap_periods 0, no_change_periods 0, slope 0.833333, change 0.000000 at 5 percent) match the output. {REC} reproduces the twelve gaps [58, 42, 76, 85, 49, -89, 48, 75, -46, -91, 27, 38] bp with no zero gap, so 'the check holds only vacuously here' is correct. The page discloses the vacuity (L06.html:262; quiz L06.html:503 q10)."),
 "E5-b-lab-simulated-label": ("PASS", "L06.html:114 'The lab is SIMULATED'; twin docstring lines 1 and 3 say SIMULATED; L06 output header 'seeded SIMULATED path'. L04 and L05 read no generated data and are not labelled. grep -c data-files on L04, L05, L06 HTML -> 0 each (no dataset read)."),
 "E5-b-lab-determinism": ("PASS", "tests/labs/E5/lab-E5-L04-1.py and lab-E5-L05-1.py import only fractions (exact, no randomness); lab-E5-L06-1.py imports random and seeds random.Random(SEED) with SEED = 20261028 (line 30). Re-run gave identical stdout to the embedded block (cmp_r2)."),
 "E5-b-lab-runtime": ("PASS", "tools/page_smoke.py --unit E5 --pages L04 L05 L06 --skip-sweep -> 'page_smoke modules/E/E5/L04.html: PASS', 'L05: PASS', 'L06: PASS', 'page_smoke E5: PASS'; lab timings 0.0 s after 1.1-1.2 s runtime boot. The figure sweep was skipped because these pages contain no figure."),
 "E5-b-lint-types": ("PASS", ".venv/bin/ruff check on the three twins -> 'All checks passed!'; ruff format --check -> '3 files already formatted'; .venv/bin/mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files'."),
 "E5-b-pytest": ("PASS", ".venv/bin/pytest -q -k 'E5 or lab' -> all dots, 100% passed (no failures)."),
 "E5-b-refs-registry": ("PASS", "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit E5 (live) -> 'live re-verification of E5: 4 of 560 entries, 0 problems'. Keys used by L04-L06: hicks1937mr (references/references.json:12484) and phelps1968money (19130), both used_by E5, verified_by crossref."),
 "E5-b-refs-hicks-attribution": ("PASS", "Previously UNVERIFIABLE because the Hicks paper was not read; the page does not need it: L04.html:566 says the lesson 'has not read that paper, so it summarises no argument of it and attributes no result to it'. The bibliographic record (Econometrica 5(2), 1937, DOI 10.2307/1907242) was re-checked live against Crossref by tools/verify_refs.py --unit E5 (0 problems). No content is attributed; nothing else in L04-L06 attributes an IS-LM result to Hicks."),
 "E5-b-refs-no-numbers-b": ("PASS", "L04-L06 prose: the only locators are registry keys (hicks1937mr, phelps1968money); no page numbers, coefficients or bibliographic numbers from memory were found by reading the three pages."),
 "E5-b-num-L04": ("PASS", "All prose numbers in L04 recomputed by " + REC + " and by hand: 28/5, 4/5, 2/25, 1/25, 2/5, 8/5, -1/5, 4, 4/5 vs 1/(1-c)=4 (ratio 1/5), M1 14/3, 5/6, 2/3, -1/6, 1/2 vs 1/3 ratio. No unrounded-versus-displayed mismatch."),
 "E5-b-num-L05": ("PASS", "All L05 prose numbers recomputed: P*=1.2, Y*=1040, dP=0.1, dY=20, long-run 1.6 and 1.9, share 2/3 at nu=200, Part D shares and price changes, M1 1.05 and 995, M2 3/4 and 30 and 0.2, E1 24 and 0.06, E2 increases 5, 5, 4, 2.666667 (8/3), R2 1.5 and 1040, R3 60."),
 "E5-b-num-L06": ("PASS", "All L06 prose numbers recomputed: 13/600 = 0.0216667 (0.021667), beta 5/6 = 0.833333, 1/120 = 0.0083333 (0.008333), 1/60 = 0.0166667 (0.016667), 0.048, 0.005, 0.062, 0.0041667 (0.004167), E3 -0.0048333 (printed -0.004833 from the 58 bp gap)."),
 "E5-b-num-L04-E1": ("PASS", "Previously FAIL (display of 2/25). L04.html:423 now reads 'Part B prints a change in the interest rate of 1/25, or 0.0400000000, and a change in output of 2/25 ... The lab prints the fraction only'. The lab prints (0.0400000000) for di and only the fraction 2/25 for dY; the ratio (1/25)/(2/25)=1/2 = d/h is correct."),
 "E5-b-num-L04-E3": ("PASS", "Previously FAIL. L04.html:437 now cites 0.8000000000 (Part B) and 4 (Part D) and gives 0.8/4 = 1/5 = h(1-c)/D = (1/4)/(5/4); the lab prints (0.8000000000) and 4; consistent."),
 "E5-b-grades-L04": ("PASS", "Prop 3.2, Prop 4.2, Prop 4.3 and Derivation 2.2 are T with proofs on the page (re-derived: determinant -D, direct substitution check, Cramer, h/D <= 1/(1-c) iff bd >= 0). Remarks 4.4 and 4.5 are derivations on the page. Key results table L04.html:471-474 matches."),
 "E5-b-grades-L05": ("PASS", "Prop 2.1, 2.2 and 3.1 are T with proofs re-derived; Part D and the lab numbers are exact (Lab 1 exact), so the key-results grade T is right; key results L05.html:392-396."),
 "E5-b-grades-L06": ("PASS", "Prop 2.1, Prop 3.1 and Corollary 3.2 are T with proofs re-derived; the seeded path result is graded C (key results row L06.html:435; cards E5-c103 C); Part C grid exact T."),
 "E5-b-math-L04": ("PASS", "Prop 3.2 determinant -D (D>0 under A2), direct check of both relations; Prop 4.2 derivatives from Y*=(hA+b m)/D, i*=(dA-(1-c)m)/D and dA/dG=1, dA/dTax=-c; Prop 4.3 algebra: h/D <= 1/(1-c) iff h(1-c) <= D iff 0 <= bd. All re-derived by hand and by recompute."),
 "E5-b-math-L05": ("PASS", "Prop 2.1 algebra (eta+nu)P = a - Ybar + nu Pe; Prop 2.2 Delta P and Delta Y and bounds (1 - nu/(eta+nu) = eta/(eta+nu) > 0); Remark 2.3 limit; Prop 3.1 fixed point (P^e = (a-Ybar)/eta gives P* = P^e). R1 existence argument: H strictly decreasing, limits at 0+ and infinity, intermediate value theorem: correct."),
 "E5-b-math-L06": ("PASS", "Prop 2.1 proof (P_t - P^e_t = (Y_t - Ybar)/nu, substitution, divide by P_{t-1}); Prop 3.1 iff chain; Corollary 3.2 under A3 (pi^e_t = pi_{t-1}); Remark 2.2 numbers (beta = 1 at P=1, 5/6 at 6/5). All re-derived."),
 "E5-b-problems-L04": ("PASS", "M1-M3 (14/3, 5/6, 2/3, 1/3, -1/6), P1-P3, E1-E3 and R1-R3 solutions re-derived; P2 'b>0 and d>0 together' follows from bd>0 iff both positive under A2."),
 "E5-b-problems-L05": ("PASS", "L05-M1 (21/20 wait: P*=1.05, Y*=995), M2 (3/4, 30, 0.2), M3 (1, 1.4), P1 uniqueness algebra, P2 (eta/(eta+nu)>0), P3 fixed point, E1 (24, 0.06), E2 (5, 5, 4, 8/3), E3 (Delta a = 30), R1 (existence/uniqueness argument), R2 (1.5 and 1040), R3 (60). All re-derived."),
 "E5-b-problems-L06": ("PASS", "L06-M1 (0.5, 0.03), M2 (0.8, 0.048), M3 (0.02, 0.005, -0.015), P1 (-beta), P2 (iff chain), P3 (uniqueness), E1 (1/120), E2 (9 positive-gap periods, 3 negative, all opposite-sign from printed draws), E3 (beta1 = 5/6, gap 0.0058, -0.0048333), R1 (6/5), R2 (0.062), R3 (no numeric value). All re-derived."),
 "E5-b-notation-registry": ("PASS", "notation/notation.json registers T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. grep of the three pages finds no \\Phi, \\gamma, R_f or \\mathbb{Q}; the only T is the grade label T; no registered symbol is used with another meaning."),
 "E5-b-notation-s": ("PASS", "Previously FAIL (S in L05 and L06). grep -n '\\bS\\b' over L04, L05, L06 HTML and the three twins: no matches. The symbol S is gone."),
 "E5-b-notation-b": ("PASS", "Previously FAIL (b vs A1 of L05). L05 now uses a, eta, nu, Ybar, P^e only (L05.html:60-75); b is the investment sensitivity only in L04 (Definition 2.1, L04.html:74), and L06 uses beta_t for the slope. The card E5-c072 uses eta, not b. No conflict remains."),
 "E5-b-L05-undefined-M": ("PASS", "Previously FAIL. M first appears at L05.html:80 where it is defined: 'where M is the nominal money stock (Lesson 4, Definition 2.1)'. grep shows no earlier use of M in L05."),
 "E5-b-dag-closure": ("PASS", "tools/check_dag.py --unit E5 -> PASS. grep -i of the three pages for rational, New Keynesian, determinacy, Lagrange, Gordon, filter, standard deviation, correlation, regression, exchange rate, open economy, Hodrick, Taylor, dynamic: only prose, no link or dfn to an outside concept. 'Expected inflation' is an outside-closure concept used as a plain dfn: see E5-b2-L06-expected-inflation-dfn."),
 "E5-b-dfn-once": ("PASS", "data-concept dfns: business-cycle (L04.html:60), is-lm-model (L04.html:74), ad-as-model (L05.html:75), phillips-curve (L06.html:79), natural-rate-of-unemployment (L06.html:84); each defined once in the page that introduces it; later uses are links."),
 "E5-b-cards-L04-sample": ("FAIL", "cards.json:428 (E5-c060) back: 'The word is used only in that sense (Definition 3.1).' The lesson (L04.html:105) says only 'In this lesson the word has that sense.' The scope word 'only' is not in the lesson and no computation supports it. Cards E5-c053 to E5-c070 otherwise match their lesson text (checked one by one). Fix: change the card back to 'In this lesson the word has that sense (Section 3).' Row E5-b2-cards-L04-c060 records the same defect."),
 "E5-b-cards-L04-c068": ("PASS", "Previously FAIL. cards.json:483 (E5-c068) now says 'Only when bd = 0 (Proposition 4.3)' with b=0 or d=0 (Problem R1) and gives 0.8 against benchmark 4 (L04 Parts B and D). Matches L04.html:167 (equality iff bd=0), L04 R1 and Parts B and D."),
 "E5-b-cards-L05-sample": ("FAIL", "cards.json:510 (E5-c071) back and cards.json:546 (E5-c077) back use 'Y = Y^d = Y^s'. The lesson (L05.html:75 Definition 1.1) uses Y = Y^d = Y^{\\nu}; 'Y^s' is not defined in L05 and appears nowhere else on the page. Fix: write Y^{\\nu} on both cards. Other cards E5-c072 to E5-c087 match (checked one by one). Row E5-b2-cards-L05-supply-symbol records the defect."),
 "E5-b-cards-L05-c074": ("PASS", "Previously FAIL. cards.json:525 (E5-c074) now says 'A3 is used in the long-run equilibrium of Definition 1.1 and in Proposition 3.1', which matches L05.html:70 text; no 'only' remains."),
 "E5-b-cards-L06-sample": ("PASS", "Cards E5-c088 to E5-c104 each checked against L06 text: c093 (Def 1.1), c094 (Def 1.2), c095 (Prop 2.1), c096 (Remark 2.2: 1 and 5/6), c097 (Prop 3.1), c098 (Cor 3.2), c099 (0.008333, 1/120, §5), c100 (0.016667 at 3 percent), c101 (§5), c102 (0.021667, 1.236, 1.226), c103 (SIMULATED, C), c104 (grid, T). All agree."),
 "E5-b-cards-dup-scan": ("PASS", "cards.json has 130 cards, unique ids (E5-c001 to E5-c130), and no duplicate fronts (case-insensitive scan)."),
 "E5-b-L04-nav-titles": ("PASS", "Previously FAIL. L04.html nav 'Previous: L03 · The Solow growth model' matches course/modules/E/E5/L03.html h1 'The Solow growth model'. L05 nav previous/next and L06 nav previous match the h1 of L04, L05; L06 next 'L07 · Central-Bank Policy and the Taylor Rule' matches L07.html:36."),
 "E5-b-refs-free-text-phelps": ("PASS", "Previously FAIL. L05.html:485 and L06.html:525 now say the key is 'not cited' on the page; both data-references lists are empty; tools/check_pages.py and verify_refs report no problem. Naming a verified registry key to disclaim it is not a citation. Note: the sentence is a disclaimer about access ('has not read that paper') and is accurate to the page."),
 "E5-b-L05-canon-linearity": ("PASS", "Previously FAIL. L05 canon-breaks first item (L05.html:256) now says Remark 1.2 shows the real-balance IS-LM is not linear in P unless investment does not respond to the interest rate; Remark 1.2 (L05.html:80) gives the slope in 1/P as b/D times M, zero when b=0. Consistent; no mismatch."),
 "E5-b-L05-only-A3": ("PASS", "Previously FAIL. L05.html:70 now says 'A3 is used in Definition 1.1 ... and in Proposition 3.1'. It does not claim exclusivity (A3 also appears in Remark 3.2, Canon 3, Quiz 10); no 'only' claim remains."),
 "E5-b-L06-nochange-check": ("PASS", "Previously FAIL. " + "lab-E5-L06-1.py check no_change_only_at_natural_rate (line ~94) is correct code but holds vacuously on this path (zero_gap_periods 0, no_change_periods 0). The page now says so: L06.html:262 (interpretation) and quiz L06.html:503 q10 ('trivially true'). Residual note: the hypothesis at L06.html:114 still predicts the 'only when the gap is zero' statement, which this path cannot test; the disclosure covers it, so PASS with this note."),
 "E5-b-L04-twin-docstring": ("PASS", "Previously FAIL. lab-E5-L04-1.py:37-42 docstring of denominator: 'D is positive under A2: 0 < c < 1, h > 0, b >= 0, d >= 0', with D = h(1-c)+bd; matches D >= h(1-c) > 0 (L04.html:85-100). Accurate."),
 "E5-b-L04-A3-fwd": ("PASS", "L04.html:85-90 A3 (fixed prices, zero expected inflation) and L04.html:336 'L05 relaxes this assumption' are consistent with L05's A1-A3 and the canon-breaks list."),
 "E5-b-structure": ("PASS", "check_pages PASS for L04, L05, L06 (see E5-b-cmd-check-pages). Section structure (hypothesis, lab, interpretation, canon-breaks, misconceptions, problem set with four tiers, key results, quiz, references) present in each page."),
 "E5-b-banned-phrases": ("PASS", "grep for roughly, about (except 'fluctuation ... about trend'), historically, typically, generally, usually, ellipsis: no banned phrase in learner text of L04-L06."),
 "E5-b-hours": ("PASS", "data-hours=10 on each of L04, L05, L06; course/modules/E/E5/index.html data-hours-lessons=80 (8 x 10) and data-hours-project=30 (sum 110). Arithmetic consistent; pace not checked (design targets)."),
 "E5-b-page-smoke": ("PASS", "tools/page_smoke.py --unit E5 --pages L04 L05 L06 --skip-sweep -> PASS for each page (see E5-b-lab-runtime)."),
 "E5-b-scope-every": ("PASS", "L05.html:56 'Every symbol introduced here is defined where it first appears and keeps that meaning' checked against the page: P, Ybar, P^e, a, eta, nu, Y^d, Y^nu, P^*, P_LR, Y_LR, m-bar, M (L05.html:80), F and H (research) all defined before or at first use. L04.html:85 'stated for every result on this page' checked: each result uses A1 to A4."),
 "E5-b-scope-hedges": ("PASS", "L05.html:80 and 257 hedge the model limits and match the Remark text; L04.html:65 'a fall in output ... is a comparison of two equilibria' matches Proposition 3.2."),
 "E5-b-causal": ("PASS", "Causal sentences are model-internal: L04.html:177 (rise in i lowers I by b dG i/dG = bd/D, computed), L04.html:351 (interest offsets part of the rise, computed: 0.8 against 4), L05.html:111-115 (A2 gives output above potential for P above P^e), L06.html:95, 109 (inflation falls with u for given expectations, from Prop 2.1 sign)."),
 "E5-b-ratio-bases": ("PASS", "Ratios checked with their bases: L04.html:434 share 0.8/4 against Part D value (computed); L05 output share is dY/da (definition, Prop 2.2); L06 slope ratio 1/(5/6) = 6/5 = 1.2/1 (R1). No mismatched base."),
 "E5-b-terms-before-use": ("PASS", "IS-LM and its relations defined in L04 Definition 2.1 before use; expected inflation defined at L06.html:60 before A3; natural rate used in A2 (L06.html:70) before Definition 1.2 (L06.html:84), disclosed by the 'defined in Definition 1.2' wording; adaptive expectations defined in A3 before Corollary 3.2."),
 "E5-b-prose-process-words": ("PASS", "grep of L04-L06 learner text (outside code and class names) for round, build, builder, verifier, REQUEST, unit report, ledger, planner, architect: no match."),
 "E5-b-grades-claims-none-empirical": ("PASS", "L04.html:563 and L05.html:485 and L06.html:523 state no empirical claim; the empirical items are graded C (L06 simulated path) or T (exact) with the lab named; L06-R3 gives no value."),
}

rows = []
for r in prev["rows"]:
    rid = r["id"]
    status, evidence = ev[rid]
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence})

new = [
 {"id": "E5-b2-cards-L04-c060", "check": "2.7-cards", "location": "course/modules/E/E5/cards.json:428 (E5-c060); course/modules/E/E5/L04.html:105",
  "status": "FAIL", "evidence": "Card back: 'The word is used only in that sense (Definition 3.1).' Lesson L04.html:105: 'In this lesson the word has that sense.' The scope word 'only' is absent from the lesson and unsupported. Fix: replace the card back with 'In this lesson the word has that sense (Section 3).'"},
 {"id": "E5-b2-cards-L05-supply-symbol", "check": "2.7-cards / notation", "location": "course/modules/E/E5/cards.json:510 (E5-c071), :546 (E5-c077); course/modules/E/E5/L05.html:75",
  "status": "FAIL", "evidence": "Both cards write 'Y = Y^d = Y^s'. The lesson's Definition 1.1 (L05.html:75) writes Y = Y^d = Y^{\\nu}; 'Y^s' is defined nowhere in L05. Fix: use Y^{\\nu} on both cards."},
 {"id": "E5-b2-L05-ad-from-is-lm", "check": "plan-content (plans/E5-build-plan.md section 3, L05)", "location": "course/modules/E/E5/L05.html:80 (Remark 1.2) vs plans/E5-build-plan.md section 3 L05",
  "status": "FAIL", "evidence": "The plan's mandatory L05 content is 'the aggregate-demand curve from IS-LM'. Remark 1.2 states: 'This lesson does not derive its demand curve from the IS-LM specification of Lesson 4. It takes the linear form A1 as the model.' The IS-LM output is affine in 1/P only (Y* = (hA + b M/P)/D), so the linear AD of A1 is an assumption, not a consequence. Fix: either derive the AD relation from L04 (stating the b=0 or linearisation case explicitly), or obtain an architect ruling that amends the plan's L05 content."},
 {"id": "E5-b2-L06-expected-inflation-dfn", "check": "architect default (no dfn outside closure)", "location": "course/modules/E/E5/L06.html:60 (<dfn>expected inflation</dfn>); plans/E5-build-plan.md section 4 D1; Architect decisions paragraph",
  "status": "FAIL", "evidence": "Architect default (binding): 'concepts outside the prerequisite closure are plain prose with no link and no dfn'. Expected inflation is the out-of-closure concept 'expectation' (M4, plan section 4 D1). The page wraps it in a plain <dfn>. The plan's D1 row says plain <dfn>; that conflicts with the binding default, so the architect must rule. Fix (per the default): remove the <dfn> tags at L06.html:60 and keep the sentence as plain prose."},
 {"id": "E5-b2-L06-expectation-macro", "check": "plan-content / notation (plans/E5-build-plan.md section 3, L06)", "location": "course/modules/E/E5/L06.html:60, 74, 92 (pi^e_t); plans/E5-build-plan.md section 3 L06",
  "status": "FAIL", "evidence": "Plan section 3 L06 says 'Expected inflation is written with the \\E macro and defined in prose'. The page writes expected inflation as the symbol pi^{e}_t throughout (for example L06.html:60) and uses no \\E macro. Fix: write expected inflation with the registered \\E macro as the plan requires, or ask the architect to amend the plan line."},
]
rows.extend(new)

summary_fail = [r["id"] for r in rows if r["status"] == "FAIL"]
summary_unv = [r["id"] for r in rows if r["status"] == "UNVERIFIABLE"]
frag = {
 "unit": "E5",
 "slice": "E5-b",
 "round": 2,
 "verifier": "Haiku independent verifier, unit E5 slice E5-b (L04-L06 and lab twins); round 2; did not build E5 and shares no context with the builders",
 "pin": "e22feb3",
 "base": "55b5634 (round-1 pin, the delta is computed from it)",
 "previous_ledger": "/tmp/fanout-frags/C-E5-b.round1.json (round-1 rows, context only; no previous PASS row carried)",
 "checkout": "/tmp/verifyC2-E5-b (detached at e22feb3; .venv symlinked)",
 "scratch": "/tmp/E5-v/E5-b/r2",
 "verified_at": "2026-10-28T23:00:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
   "Delta from 55b5634 to e22feb3 for the slice: course/modules/E/E5/L04.html, L05.html, L06.html, cards.json (all of which changed) and tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py (changed). L01-L03, L07, L08 and project files changed in the same commit range but are other slices and were not re-verified here. Because every subject of this slice changed, no PASS row was carried from round 1; every row was re-run or re-read.",
   "Scripts (repository paths): ledgers/E5/scripts/E5-b-r2/cmp_r2.py (embedded code vs twin, embedded output vs fresh run, python -I -W error), ledgers/E5/scripts/E5-b-r2/recompute_r2.py (independent Fraction re-derivation, 49 PASS, 0 FAIL; output in /tmp/E5-v/E5-b/r2/recompute.out), ledgers/E5/scripts/E5-b-r2/build_fragment_r2.py (writes this fragment).",
   "Mutants: not applicable to this slice. Plan Architect decisions and the ruling for this round: lab twins are demonstrations, mutation applies to project graders only. ledgers/E5/mutants/ is not created (plan section 13: rubric-only).",
   "Alternative correct implementations: not applicable (no autograder in these labs).",
   "Hours are not checked for pace (architect ruling). Hours arithmetic: 10 h each, hub 80 + 30 = 110, consistent.",
   "Plan-dependency note: plans/E5-build-plan.md section 4 states the closure as {E1, M1, M2, P0.1}; the brief says AC1, S0, S2. The check_dag tool passed; the plan's closure was used for the outside-closure judgement.",
   "Not checked: the Hicks (1937) and Phelps (1968) articles themselves were not read (JSTOR and Springer-hosted texts were not attempted; no bot check was bypassed). Only the registry records and the live Crossref metadata (verify_refs) were checked. The Blanchard record was re-verified live by verify_refs but no Blanchard content is cited on these pages.",
   "Not run: the full repository gate (targeted checks only, per the slice). The figure sweep of page_smoke was skipped with --skip-sweep because the three pages contain no figure. check_projects and the project slice are other slices.",
   "The hub index.html card titles (for example 'Business Cycles and IS-LM') differ in wording from the lesson h1; not a defect in this slice, and not judged here."
 ],
 "summary": {
   "rows": len(rows),
   "pass": sum(1 for r in rows if r["status"] == "PASS"),
   "fail": len(summary_fail),
   "unverifiable": len(summary_unv),
   "mutants": 0,
   "fail_ids": summary_fail,
   "unverifiable_ids": summary_unv,
 },
}
out = root / "ledgers/E5/E5-b.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("written", out, len(rows), frag["summary"])
