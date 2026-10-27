"""Builds ledgers/AC2/L05-L06.json (round 4) from the round-3 row list and the round-4 findings.

Every round-3 row id is kept. Statuses and evidence are the round-4 verifier's own (see the fragment notes).
Run: <checkout>/.venv/bin/python -I ledgers/AC2/scripts/L05-L06-r4/build_fragment_r4.py
"""

import json
import sys

ROUND3 = "/tmp/ac2-frags/L05-L06.round3.json"
OUT = "/tmp/verify-ac2r4-l56/ledgers/AC2/L05-L06.json"
SCRATCH = "/tmp/ac2-v/L05-L06-r4"
CHECKOUT = "/tmp/verify-ac2r4-l56"

r3 = json.load(open(ROUND3, encoding="utf-8"))
r3rows = {r["id"]: r for r in r3["rows"]}

P = "PASS"
F = "FAIL"

# id -> (status, location override or None, evidence)
new = {}

def put(rid, status, evidence, location=None):
    new[rid] = (status, location, evidence)

# --- commands (re-run this round on the 2607c60 checkout; outputs in SCRATCH)
put("L05-L06-cmd-pin", P, "git rev-parse --short HEAD = 2607c60; git status shows only untracked .venv (no tracked file modified). Pin is the round-4 pin, not 4a8690a.")
put("L05-L06-cmd-check-pages", P, "tools/check_pages.py --unit AC2 --page L05 -> 'check_pages AC2 L05: PASS' (rc 0); --page L06 -> 'check_pages AC2 L06: PASS' (rc 0). Output " + SCRATCH + "/check_pages.txt.")
put("L05-L06-cmd-check-dag", P, "tools/check_dag.py --unit AC2 -> 'check_dag AC2: PASS' (rc 0). " + SCRATCH + "/check_dag.txt.")
put("L05-L06-cmd-run-labs", P, "tools/run_labs.py --unit AC2 -> 'run_labs AC2: PASS (11/11)' (rc 0). " + SCRATCH + "/run_labs.txt.")
put("L05-L06-cmd-twins-isolated", P, "python -I -W error tests/labs/AC2/lab-AC2-L05-1.py and lab-AC2-L06-1.py: rc 0 both. Outputs " + SCRATCH + "/lab05.out, lab06.out. Each output equals the expected block quoted in its page (compared line by line this round).")
put("L05-L06-cmd-page-smoke", P, "tools/page_smoke.py --unit AC2 --pages L05 L06 -> 'page_smoke modules/AC/AC2/L05.html: PASS', 'page_smoke modules/AC/AC2/L06.html: PASS', 'page_smoke AC2: PASS' (rc 0). Lab timings L05 2.8 s, L06 0.1 s. " + SCRATCH + "/page_smoke.txt.")
put("L05-L06-cmd-verify-refs-unit", P, "tools/verify_refs.py --unit AC2 -> 'live re-verification of AC2: 7 of 560 entries, 0 problems' (rc 0). " + SCRATCH + "/verify_refs_live.txt.")
put("L05-L06-cmd-verify-refs-offline", P, "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (rc 0). " + SCRATCH + "/verify_refs_offline.txt.")
put("L05-L06-cmd-lint", P, "ruff check on both twins: 'All checks passed!'; ruff format --check: '2 files already formatted'; python -m mypy --no-incremental on both twins: 'Success: no issues found in 2 source files'. pytest tests/test_labs.py -k AC2: 11 passed. " + SCRATCH + "/lint.txt.")

# --- citations
put("L05-L06-cit-sloan-registry", P, "references/references.json key sloan1996stock present (offline integrity 560/0). Crossref api.crossref.org/works/10.2308/tar-9608042309 fetched with plain curl: HTTP 200 (" + SCRATCH + "/cr_sloan.json). Registry title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?', The Accounting Review.")
put("L05-L06-cit-sloan-claim-s1", P, "L05.html line 61 claim span (grade C, data-cite sloan1996stock): 'Sloan (1996) investigates whether stock prices reflect information about future earnings contained in the accrual and cash-flow components of current earnings.' Crossref abstract (HTTP 200): 'Investigates whether stock prices reflect information about future corporate earnings contained in accrual and cash flow components of currents earnings.' Matches; the claim names no finding.")
put("L05-L06-cit-sloan-claim-s3", P, "L05.html has three data-cite spans this round: line 61 (sloan1996stock), lines 232 and 233 (mclean2016academic, hou2018replicating). The §3 Sloan paragraph (L05.html section 3) has no claim span and states the question only; §5 and §7 attribute no finding to Sloan (grep 'Sloan' lines 111, 217, 222, 246: no finding named).")
put("L05-L06-cit-dechow-registry", P, "references/references.json key dechow1995detecting: DOI 10.2308/tar-9505096112, title 'Detecting Earnings Management.', container The Accounting Review. Crossref (HTTP 200, " + SCRATCH + "/cr_dechow.json): volume 70, issue 2, pages 193-225, published 1995-04. The page's 'The Accounting Review 70(2), 1995' matches.")
put("L05-L06-cit-dechow-scope", P, "L06.html line 61 claim span (grade C): 'The paper evaluates alternative accrual-based models for detecting earnings management and compares the specification and power of commonly used test statistics.' Crossref abstract: 'Evaluates alternative accrual-based models for detecting earnings management. Comparison of the specification and power of commonly used test statistics; ...'. Matches. §5 bullet 1 (L06.html line 358) and key-results row 6 (line 499) claim the same and quote no power figure.")
put("L05-L06-cit-dechow-motivation", P, "Round-2 claim spans 'Jones's regression uses...' and 'Dechow et al. (1995) motivate...' are absent: grep 'et al' and 'Dechow' in L05.html, L06.html, cards.json returns no hit. No attribution of the receivables term to Dechow in learner text.")
put("L05-L06-cit-dechow-grouping", P, "L06.html §5 bullet 4 ('Grouping changes the model') carries no data-cite and no attribution; it is stated as a methodological property of the model, with 'The A15 contract estimates one cross-section' as the only fact claimed.")
put("L05-L06-cit-dechow-authors", P, "Ruling (1): the registry bibliography may show two authors and is not failed. Authored prose: grep 'Dechow' in L05.html, L06.html and cards.json: no hit. The L06 citation names the key and the title 'Detecting Earnings Management' only. Crossref lists Dechow, Patricia M. and Sloan, Richard G. (" + SCRATCH + "/cr_dechow.json); the page does not resolve or state the author question.")
put("L05-L06-cit-mclean", P, "L05.html line 232 claim span (grade C, data-cite mclean2016academic): 'McLean and Pontiff, \"Does Academic Research Destroy Stock Return Predictability?\", are in the registry under mclean2016academic.' Registry title 'Does Academic Research Destroy Stock Return Predictability?' (The Journal of Finance). Matches; no finding stated.")
put("L05-L06-cit-hou", P, "L05.html line 233 claim span (grade C, data-cite hou2018replicating): 'Hou, Xue and Zhang, \"Replicating Anomalies\", are in the registry under hou2018replicating.' Registry title 'Replicating Anomalies' (The Review of Financial Studies), authors Hou, Xue, Zhang. Matches; no finding stated.")
put("L05-L06-reg-used-by", P, "Carried from round 3 (references/references.json byte-identical since 4a8690a: git diff --quiet 4a8690a HEAD -- references/references.json returns 0 this round): used_by entries for mclean2016academic and hou2018replicating unchanged; the L05 citations rely on them only as registry keys.")

# --- numbers
put("L05-L06-num-L05-lab", P, "Lab 1 of L05 re-run (python -I -W error, rc 0): every line of the page's expected block equals the run (16 of 16 lines, compared this round): mean_z_gap_simulated -2.7937, planted_monthly_spread 0.00223, spread_sd_theory 0.01131, expected_t_at_planted 2.164, recovered 0.00219, null_false_positive_rate 0.060, effect_rejection_rate_power 0.590, effect_median_t 2.155, seed0 0.00075 t 0.676, sweep -2.7437/-2.7728/-2.7912/-2.7991, seed0_distance_in_se -1.433. Interpretation figures (0.6 SE, about 0.015, 41%) recomputed: 0.0154, 0.649 SE, 1 - 0.590 = 0.41.")
put("L05-L06-num-L05-derived", F, "FAIL (see L05-L06-r4-arith-L05-E2 and L05-L06-r3-num-L05-E3). The page's main E3 figure is now the lab's -1.433 (correct), but E3 then states 'Rounded inputs, 0.00075 and 0.00223, give -1.44, which is an artefact of rounding'. Recomputed (" + SCRATCH + "/recompute_r4.out): (0.00075 - 0.00223)/0.0010328 = -1.4330, so rounded inputs with the page's own standard error give -1.43. -1.44 needs the rounded SE 0.00103 (-1.4369) or planted 0.002235 (-1.4378), not the rounded inputs. E2 displayed arithmetic is also off in the last digit (2.1647 as written). Fix: state the -1.44 source correctly or drop it; write the E2 result as 2.1647 from the rounded SD and 2.164 from the unrounded SD.")
put("L05-L06-num-L06-lab", P, "Lab 1 of L06 re-run (python -I -W error, rc 0): page expected block equals the run line for line (39 of 39 lines, compared this round). Interpretation figures recomputed: 0.3891 - 0.1806 = 0.2085 printed, 0.2084 unrounded (decomposition 0.1425 + 0.1965 - 0.1306 = 0.2084); 0.2084/0.2824 = 0.738; 0.1031 vs 0.10 and -0.0805 vs -0.08 quoted correctly; TPR 0.985 = 197/200; weak TPR 0.355 = 71/200, FPR 0.0717 (129/1800); flags_only 6 and 6, flags_differing 12 (strong 0).")
put("L05-L06-num-L06-derived", F, "FAIL (see L05-L06-r4-arith-L06-E3). Derived values all recompute (" + SCRATCH + "/recompute_r4.out): 0.2824/0.05 = 5.648 -> 5.6; 0.2781 sqrt(1800/57600) = 0.0492; 1800 (0.2781/0.05)^2 = 55,685 rows and /0.9 = 61,872 firm-years (page 55,700 and 61,900); M1 NDA -0.02295, DA -0.00705; M2 c 0.01645, Phi(3.355) = 0.9996; E1 129/200 = 0.645. The E3 displayed arithmetic 0.003076/0.001467 = 2.0968 is written as 2.096 (displays as 2.097); the lab's 2.096 comes from unrounded inputs.")
put("L05-L06-num-L06-roughly-4pct", P, "E3 tails: 2(1 - Phi(2.096)) = 0.0361 (lab two_sided_tail_a2 0.036) and 2(1 - Phi(2.067)) = 0.0387; both round to 'about 4%' (shown calculation present). Recomputed this round.")

# --- maths (read in full this round; no proof hunk in git diff 4a8690a HEAD touches these blocks)
put("L05-L06-math-L05-def-t", P, "L05.html Definition 1.2: t = S-bar/(s_S/sqrt(T)) with s_S^2 the 1/(T-1) sample variance; matches the lab's t_stat (mean over std(ddof=1)/sqrt(n)). Read in full.")
put("L05-L06-math-L05-prop21", P, "L05.html Proposition 2.1 and proof read in full: E[S_t | z] = beta (zbar_L - zbar_H); the constant cancels and the noise averages to zero given the sort. Lab 1 planted spread = beta x mean z-gap (-0.0008 x -2.7937 = 0.0022350) is an instance. Not in any 4a8690a..HEAD diff hunk.")
put("L05-L06-math-L05-prop23", P, "L05.html Proposition 2.3 and proof read in full: q = Phi^-1(0.2) = -0.841621; phi(q) = 0.279962; gap = -2 phi(q)/0.2 = -2.79962 (recomputed, " + SCRATCH + "/recompute_r4.out); Prop states approximately -2.800 (rounded). Low-quintile mean -1.3998 (page: -1.400). Not in any diff hunk.")
put("L05-L06-math-L05-remark22-P1-P3", P, "L05.html Remark 2.2, P1, P3 read in full. P1: monotone g preserves ranks and quintile sets; P3: E[S_t]=0 under beta=0 needs E[eps|z]=0, serial independence only for the normal approximation. Statements correct.")
put("L05-L06-math-L06-prop31", P, "L06.html Proposition 3.1 and proof read in full: X'e = 0 from the normal equations; 1'e = 0 for every y iff 1 in col(X). Remark 3.2 recomputed: b = 1.5/1.25 = 1.2, fitted (1.2, 0.6), residuals (-0.2, 0.4), sum 0.2.")
put("L05-L06-math-L06-prop33-formula", P, "L06.html Proposition 3.3 formula E[b_hat | X] = b* + (X'X)^-1 X'd read in full; substitution in the proof is correct. Not in any diff hunk.")
put("L05-L06-math-L06-prop33-statement", P, "L06.html Proposition 3.3 statement and proof, key-results row 2, card AC2-c079 and quiz L06q3 explanation read this round; the bias is zero iff X'd = 0 (correct for invertible X'X). Not in any diff hunk.")
put("L05-L06-math-L06-P3", P, "L06.html P3 solution read in full: the bias term passes the conditional expectation because d is a function of X; no step unsupported.")
put("L05-L06-math-L06-remark32-P1-P2", P, "L06.html Remark 3.2, P1 and P2 read in full. P2: 1/(kA) = (1/k)(1/A) so a1 scales by k; a2, a3 and residuals unchanged (matches contract Scale row, atlas/A15.contract.md line 190).")
put("L05-L06-math-notation", P, "Carried from round 3 (notation/notation.json byte-identical since 4a8690a: git diff --quiet returns 0 this round): the pages use only the macros and symbols already defined there (E, hat b, widehat, mathbf 1, and the 8 symbols).")

# --- labs
put("L05-L06-lab-L05-1-run", P, "Lab 1 of L05 re-run; the expected block, including the two sweep lines and seed0_distance_in_se, matches the printed run (lab05.out). Sweep is 20 seeds (seeds 0-19) at each firm count, as the page says.")
put("L05-L06-lab-L05-1-interp", P, "L05.html Lab 1 interpretation and Misconceptions 1-3 read against the printed values: SIMULATED stated; 'does not reproduce Sloan (1996)'; seed-0 misconception uses 1.43 with the lab's unrounded -1.433 cited. The E2 cause sentence is now hedged (L05-L06-r2-math-E2-zgap-cause).")
put("L05-L06-lab-L06-1-run", P, "Lab 1 of L06 re-run (rc 0, identical to expected block). Lab docstring states SIMULATED and that the flag scores are one draw at seed 606; the page says the same.")
put("L05-L06-lab-L06-1-overreach-sample", P, "L06.html §4 and Lab 1 interpretation read: 'The lab says nothing about real firms'; no real-data claim; the 0.2084 is decomposed, not called bias alone.")
put("L05-L06-lab-L06-1-single-seed", P, "Interpretation: 'every flag score below is one simulated draw at seed 606'; key-results rows 4-5 say 'In one simulated draw'; cards c082-c084 say 'one draw'. Matches lab docstring.")
put("L05-L06-lab-L06-1-threshold-claim", P, "Misconception 3 precision sentence: precision = TP/flagged = 71/200 = 0.355 and 197/200 = 0.985 (flagged = 200 = manipulators, so precision equals TPR here, which the page does not claim otherwise). Says 'Two shifts at one seed do not establish how the precision depends on the shift'; no threshold claimed.")
put("L05-L06-lab-L06-1-flag-count", P, "Interpretation and M3 solution: flags_only_all_firms 6 + flags_only_oracle 6 = 12 = flags_differing_all_vs_oracle 12 (weak); strong scenario 0 differing (lab06.out). Matches.")

# --- cards (all 13 L05 and 22 L06 cards read against their lesson text this round)
put("L05-L06-card-L05-defs", P, "Cards c063, c065, c066, c067, c068 read against L05 Def 1.1-1.2, Props 2.1 and 2.3, Remark 2.2: c068 '-2 phi(q)/0.2, approximately -2.800' matches Prop 2.3; c066 and c067 match Prop 2.1 and Remark 2.2.")
put("L05-L06-card-L05-lab", P, "Cards c069-c075 read against the L05 Lab 1 expected block and E1-E3, R1: 0.00219/0.00223, 0.060 (SE about 0.015), 0.590, seed-0 0.00075 and 0.676, 201 months (14.177^2 = 200.99). c075 drops 'roughly 17 years' and keeps 201 (page R1 says 201 and 'about 17 years'). Matches.")
put("L05-L06-card-L05-sloan", P, "Cards c064, c072, c074 read against L05 §1, §3 and §5: c064 states the question and that no finding is quoted (matches §1 and §3); c072 and c074 match misconceptions 1 and 3. c122 ('close to but not equal to -2.800') and c123 (2.164, 2.155) match the lab output.")
put("L05-L06-card-L06-defs", P, "Cards c076, c077, c087, c138 read against L06 Defs 1.1, 1.2, 2.1 and §2: c087 'over lagged assets, as the regressor' matches the revised §2 text and Def 2.1; c138 matches Def 1.2.")
put("L05-L06-card-L06-lab", P, "Cards c082, c085, c086, c124, c125 read against Lab 1 and the revised interpretation: 197/200 and 0.985, 71/200 and 0.355, FPR 0.0717, flags_only 6/6, se_scaling 0.2781 (1,800 rows) and 0.0489 (57,600 rows). c125 'roughly as the square root of the row count': 5.69 observed vs 5.66 sqrt ratio. Matches.")
put("L05-L06-card-L06-iff", P, "Card c078 ('X'e = 0 always; sum zero iff ones in col(X)') matches Prop 3.1 and Remark 3.2.")
put("L05-L06-card-L06-projection", P, "Card c079 ((X'X)^-1 X'd, projection, needs d a function of X and E[u|X]=0; zero only if X'd = 0) matches Prop 3.3.")
put("L05-L06-card-L06-only-when", P, "Card c080 (a1 carries CU; scales by k) and c081 (residuals, a2, a3 invariant) match Def 2.1, Remark-level text §3 and P2.")
put("L05-L06-card-L06-dechow", P, "Card c128 ('Graded C; no power figure is quoted') matches L06 §1 and §5 and key-results row 6; no author names in the card.")
put("L05-L06-card-L06-12of200", P, "Card c124 ('Twelve firm-years change flag status ... six enter ... six leave') matches Lab 1 flags_only_all_firms 6 and flags_only_oracle 6 and the M3 solution.")
put("L05-L06-cards-dup-scan", P, "Scan of all 140 cards this round: 140 unique ids (c001-c140), no duplicate front or back text. L05/L06 cards: c063-c088, c122-c125, c128, c138 (c138 is the L06 entry at the end of the file).")
put("L05-L06-cards-coverage", P, "Every L05 and L06 claim-bearing sentence I read has a card or none is needed: the definitions, props, Lab 1 results and misconceptions are covered; no card states a number absent from its lesson.")

# --- structure and prose
put("L05-L06-struct-hours", P, "data-hours: L05 8, L06 10 (index sums to 76 over eight lessons, as stated in the round-3 notes). Own estimates 7.5 h and 9.5 h: within 30%.")
put("L05-L06-struct-sections", P, "Both pages have the template sections: why-it-matters, definitions/propositions, lab, misconceptions, problem set (M, P, E, R tiers), key results, retrieval quiz, references, lesson nav.")
put("L05-L06-struct-banned", P, "Scan (this round) for TODO, TBD, lorem, ellipsis, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'roughly', 'historically', 'typically', 'generally', 'usually': no hit. 'about' occurrences each carry a shown calculation (e.g. about 1.4 = 0.2800/0.2; about 0.0010 = 0.0113/sqrt 120; about 129 = 0.0717 x 1800; about 41% = 1 - 0.590; about 0.001 = 1/1000).")
put("L05-L06-prose-unmarked-claims", P, "Every quantitative claim in the revised text carries a locator (lab output name) or a shown calculation; the Sloan and Dechow claim spans carry grade C and data-cite. No unmarked claim found in the rewritten sentences except the reserves example (L05-L06-r4-prose-L06-s5-reserves).")
put("L05-L06-prose-L04-xref", P, "L05 cross-references to L04 read this round: Definition 1.3 (L04 line ~71, the two contract measures) exists; Proposition 3.1 of L04 (free cash flow = earnings less growth in NOA; key-results row 'NI - CFO = dNOA - capex') matches L05 §3's description; L04 changes (lines 60-137, 341-394) do not alter these labels.")
put("L05-L06-prose-inversion", P, "Scan of the revised sentences for inverted direction: 'a negative residual is not evidence...' (M1), 'a positive spread' with beta < 0 (Prop 2.1), 'Precision 0.355 means most flags are not manipulators' (E1) all state the right direction.")
put("L05-L06-prose-jargon", P, "Learner text grep for 'builder', 'this build', 'REQUESTS', 'unit report': no hit in L05.html, L06.html or cards.json. Lowercase 'open source requests' appears once in L05 honest-pending text naming plans/AC2-open-items.md; architect question (a) from round 3 is unchanged (not a FAIL).")
put("L05-L06-prose-concept-links", P, "Concept links: 'modified-jones-model' and 'earnings-management' defined once (dfn) in L06 Defs 2.1 and 1.1 and linked once in the meta row; 'accruals-anomaly' defined in L05 Def 1.1; 'ols-estimator' linked in the meta row and Def 2.1 only (two links, both after the concept is introduced). No concept used before its definition in these pages.")
put("L05-L06-dag", P, "tools/check_dag.py --unit AC2 -> 'check_dag AC2: PASS' (rc 0). L05 uses AC1/S0/S2 concepts; L06 prerequisites L04 and L05 precede it in the unit.")
put("L05-L06-figures", P, "No live figure is embedded in L05 or L06 (no figures-L05.js or figures-L06.js); the check_pages gate PASS covers the pages' figure references.")
put("L05-L06-honest-data", P, "Both pages say SIMULATED throughout; no real filing or return data appears; honest-pending paragraph in L05 names the SEC company-facts reuse statement and the Kenneth French library as not cleared. No fabricated real-data number.")

# --- round-2 rows (re-verified this round unless noted)
put("L05-L06-r2-prop21-sigma0", P, "Carried from round 3 (course/modules/AC/AC2/L05.html Proposition 2.1 block byte-identical since 4a8690a: no diff hunk of 4a8690a..HEAD touches it): proposition and proof re-read this round (L05-L06-math-L05-prop21).")
put("L05-L06-r2-lab-flags-only-lines", P, "tests/labs/AC2/lab-AC2-L06-1.py prints flags_only_all_firms and flags_only_oracle (6 and 6, weak); the page quotes both (lab06.out).")
put("L05-L06-r2-attribution-sweep", P, "All data-cite spans this round: L05 lines 61 (sloan1996stock), 232 (mclean2016academic), 233 (hou2018replicating); L06 lines 61, 358 (dechow1995detecting) and 499 (key-results row, dechow1995detecting). Each checked against its registry entry or the Crossref abstract (see the citation rows).")
put("L05-L06-r2-num-L06-se-basis", P, "L06 §4 states 0.2824 as the classical SE of a1 on the 1,800 non-manipulator rows of the seed-606 sample (lab06.out: se_non_manipulators 0.2824; rows_non_manipulators 1800). R1 uses 1,800 rows and 57,600 rows consistently (lab output se_scaling 0.2781 and 0.0489).")
put("L05-L06-r2-lab-contamination-prop33", P, "Lab 1 interpretation and key-results row 2 now give the 0.2084 decomposition (0.1425 + 0.1965 - 0.1306, residual 0.000000) and state Prop 3.3 applies to E[d|X] = 0.005 (conditional-mean prediction 0.6223, lab output). No 'contamination Prop 3.3 describes' sentence remains (grep).")
put("L05-L06-r2-math-E2-zgap-cause", P, "Round-3 FAIL is resolved. E2 now says the printed sweep values are 'consistent with a finite-sort effect that shrinks as the number of firms grows' and that 'four counts with 20 seeds each do not establish the rate of that decay'. The distances 0.0559, 0.0268, 0.0084, 0.0005 recomputed (recompute_r4.out) and the trend is monotone. No causal claim is stated as established. Seed-to-seed explanation of the 0.0025 gap (20 seeds are a subset of 200) is correct.")
put("L05-L06-r2-math-L06-misc3-sentence", P, "Misconception 3 first sentence: 'Precision is the share of flagged firm-years that are manipulators: 71 of 200 (0.355) ... 197 of 200 (0.985)'. Recomputed 71/200 and 197/200. No 'because' clause.")
put("L05-L06-r2-prose-s4-lab-bears", P, "L06 §4 opening: 'The lab bears on the second and third. It fits no intercept, so it says nothing about the first.' Remark 3.2 supports the first-choice clause (sum of residuals 0.2); the second (0.2084 decomposition) and third (SE scaling 0.2824 and 0.0489) are printed by the lab.")
put("L05-L06-r2-prose-A15-reference", P, "L06 §3 units paragraph: 'This is the wording of the A15 contract's Scale row.' atlas/A15.contract.md line 190 (Scale row): a1 'is in currency units and scales by k'; a2, a3, residuals invariant. Matches.")

# --- round-3 rows (re-verified this round)
put("L05-L06-r3-num-L05-E2-printed", P, "E2 printed values re-read against lab05.out: -2.7937 (200 seeds), -2.7437, -2.7728, -2.7912, -2.7991 (20 seeds), spread_sd 0.01131, planted 0.00223, expected t 2.164, median 2.155. All printed values match. Displayed-arithmetic issue is in L05-L06-r4-arith-L05-E2.")
put("L05-L06-r3-num-L05-E3", F, "FAIL. E3 solution: 'Rounded inputs, 0.00075 and 0.00223, give -1.44, which is an artefact of rounding.' Recomputed: (0.00075 - 0.00223)/0.0010328 = -1.4330 (-1.43). -1.44 comes from rounding the SE to 0.00103 (-1.4369) or from 0.002235 (-1.4378), not from the rounded inputs as stated. Lab prints -1.433 unrounded (correct on the page's main sentence). Fix: attribute -1.44 to the rounded SE, or write -1.43 with the unrounded SE.")
put("L05-L06-r3-num-L06-decomp", P, "L06 §4, Lab interpretation and misconceptions: 0.2084 = 0.1425 + 0.1965 - 0.1306 (recomputed 0.2084); residual 0.000000 printed; a1_conditional_mean_prediction 0.6223 and 0.1245 printed.")
put("L05-L06-r3-num-L06-cond-mean", P, "Conditional-mean figures 0.6223 (strong) and 0.1245 (weak) printed by lab06.out and quoted with 'a different quantity from the realised 0.2084'. Matches.")
put("L05-L06-r3-num-L06-se-scaling", P, "se_scaling 0.2781 (1,800 rows, 2,000 firm-years) and 0.0489 (57,600 rows, 64,000 firm-years), mean over seeds 606-610 (SCALE_SEEDS = (606, 607, 608, 609, 610) in tests/labs/AC2/lab-AC2-L06-1.py line 169). Quoted correctly.")
put("L05-L06-r3-num-L06-a2z", F, "FAIL (minor, displayed arithmetic). The round-3 defect (2.07 from rounded SE) is fixed: the Lab 1 interpretation now says 2.10 with unrounded z 2.096 (lab output z_a2 2.096). But E3 still writes 'z = 0.003076/0.001467 = 2.096', and that arithmetic gives 2.0968, which displays as 2.097. See L05-L06-r4-arith-L06-E3.")
put("L05-L06-r3-hyp-L06-shift", P, "Hypothesis now reads: 'the coefficient on 1/A should shift by the projection of the planted term plus the difference in sampling noise between the all-firm and non-manipulator estimates, and the lab decomposes the shift into those components.' Consistent with the decomposition (0.1425 + 0.1965 - 0.1306). Round-3 defect fixed.")
put("L05-L06-r3-prose-L06-s2-purpose", P, "§2 now states the mechanical effect only: 'the regressor is the change in revenue less the change in receivables, divided by lagged assets'. The 'so that revenue booked as receivables...' purpose clause is gone. Round-3 defect fixed.")
put("L05-L06-r3-prose-L06-s5-bullet", F, "FAIL. The 'matters only if the manipulation runs through revenue' condition is removed (round-3 defect fixed), but the rewritten bullet 2 now says: 'A manipulation through reserves or capitalised costs changes total accruals without changing the revenue or receivables terms, so the adjustment does not represent it.' This is an unsourced accounting mechanism: an allowance (reserve) against receivables changes net receivables, and the page never defines receivables as gross or net. See L05-L06-r4-prose-L06-s5-reserves.")
put("L05-L06-r3-prose-L06-imprecise", P, "L06 §4 'too imprecise to recover the planted value': 0.2824 is 5.6 times 0.05 and the non-manipulator estimate 0.1806 is 0.46 SE above 0.05 (0.1306/0.2824 = 0.46). Accepted as a reading of the SE (round-3 note carried for the architect).")
put("L05-L06-r3-cards-c083-c087-c124-c125", P, "c083 '0.738 of the classical SE 0.2824' = 0.2084/0.2824 (recomputed); c087 matches the revised §2; c124 matches flags_only 6/6; c125 matches se_scaling 0.2781/0.0489. All four read against their lessons this round.")
put("L05-L06-r3-cit-dechow-crossref-abstract", P, "Crossref abstract for dechow1995detecting re-fetched this round with plain curl (HTTP 200, " + SCRATCH + "/cr_dechow.json). Key-results row 6 and the §5 claim span claim only that the paper compares specification and power; no power figure quoted. Matches.")
put("L05-L06-r3-math-L06-misc2-first-term", P, "Misconception 2: the 0.2084 split into the planted-term projection (0.1425, the realised contamination) and two noise terms (0.1965, -0.1306) matches the lab decomposition; calling the first term 'the effect of including manipulators' is a reading of that decomposition (accepted).")
put("L05-L06-r3-cmd-validate", P, "ledger.validate is run on this round's fragment (command in the final report; output recorded there).")

# --- new round-4 rows
put("L05-L06-r4-arith-L05-E2", F, "FAIL (minor, displayed arithmetic). E2 solution: 'The expected t is 0.0022350/(0.01131/sqrt(120)) = 2.164'. With the displayed inputs the quotient is 2.1647, which displays as 2.165. 2.164 is correct only from the unrounded SD (0.011314 gives 2.1640; lab prints expected_t_at_planted 2.164). Fix: write 2.1647 from the rounded SD and 2.164 from the unrounded SD.", location="course/modules/AC/AC2/L05.html E2 solution (expected t sentence)")
put("L05-L06-r4-arith-L06-E3", F, "FAIL (minor, displayed arithmetic). E3 solution: 'z = 0.003076/0.001467 = 2.096 standard errors'. The displayed quotient is 2.0968, which displays as 2.097; the lab's 2.096 comes from the unrounded inputs (b = 0.1030755..0.1030765, SE 0.0014665..0.0014675). Fix: write 2.097 from the displayed inputs, or quote the lab's 2.096 as the unrounded value.", location="course/modules/AC/AC2/L06.html E3 solution (z sentence)")
put("L05-L06-r4-prose-L06-s5-reserves", F, "FAIL. L06.html §5 bullet 2 ('The receivables adjustment is untested in Lab 1'): 'A manipulation through reserves or capitalised costs changes total accruals without changing the revenue or receivables terms, so the adjustment does not represent it.' No source or model definition supports it: a bad-debt allowance reduces net receivables, so a reserve-based change can move the receivables term, and the contract defines receivables as AccountsReceivableNetCurrent (atlas/A15.contract.md line 67), so an allowance-based change does move d_receivables in the contract's own model. The claim is the mechanism the §2 disclaimer says is not sourced. Fix: drop the reserves example and the 'does not represent it' conclusion, or label the mechanism as an untested model reading.", location="course/modules/AC/AC2/L06.html §5 bullet 2")

# --- assemble: every round-3 id is kept
rows = []
for r in r3["rows"]:
    rid = r["id"]
    if rid in new:
        status, loc, ev = new[rid]
    else:
        raise SystemExit(f"no round-4 decision for {rid}")
    rows.append({"id": rid, "check": r["check"], "location": loc or r["location"], "status": status, "evidence": ev})
for rid in ("L05-L06-r4-arith-L05-E2", "L05-L06-r4-arith-L06-E3", "L05-L06-r4-prose-L06-s5-reserves"):
    status, loc, ev = new[rid]
    chk = {"L05-L06-r4-arith-L05-E2": "2.1-numbers", "L05-L06-r4-arith-L06-E3": "2.2-numbers", "L05-L06-r4-prose-L06-s5-reserves": "2.1-attribution"}[rid]
    rows.append({"id": rid, "check": chk, "location": loc, "status": status, "evidence": ev})

extra = set(new) - {r["id"] for r in r3["rows"]} - {"L05-L06-r4-arith-L05-E2", "L05-L06-r4-arith-L06-E3", "L05-L06-r4-prose-L06-s5-reserves"}
if extra:
    raise SystemExit(f"decisions for unknown ids: {sorted(extra)}")


FIXES = {
    "L05-L06-num-L05-derived": "Resolve the E3 -1.44 sentence and the E2 displayed arithmetic (see the two arith/E3 rows).",
    "L05-L06-num-L06-derived": "Write the E3 z as 2.097 from the displayed inputs, or quote the lab's unrounded 2.096 as such.",
    "L05-L06-r3-num-L05-E3": "Attribute -1.44 to the rounded SE 0.00103 or drop it; the rounded inputs with the page's SE give -1.43.",
    "L05-L06-r3-num-L06-a2z": "Write the E3 z as 2.097 from the displayed inputs, or quote the lab's unrounded 2.096 as such.",
    "L05-L06-r3-prose-L06-s5-bullet": "Delete the reserves/capitalised-cost mechanism sentence in bullet 2 of L06 §5.",
    "L05-L06-r4-arith-L05-E2": "Write 2.1647 for the displayed quotient with the rounded SD, and 2.164 for the unrounded SD.",
    "L05-L06-r4-arith-L06-E3": "Write 2.097 for the displayed quotient, or state that 2.096 comes from the unrounded inputs.",
    "L05-L06-r4-prose-L06-s5-reserves": "Drop the reserves example and the 'does not represent it' conclusion, or label the mechanism as an untested model reading.",
}
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIXES[r["id"]]

fails = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "AC2",
    "slice": "L05-L06",
    "round": 4,
    "verifier": "AC2 independent verifier, round 4, slice L05-L06 (fresh verifier; did not build AC2; shares no context with the builders or the round 1-3 verifiers)",
    "pin": "2607c60",
    "base": "4a8690a",
    "checkout": CHECKOUT,
    "scratch": SCRATCH,
    "verified_at": "2026-10-27T00:00:00+00:00",
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": r3.get("registry_flags", []),
    "freshness_flags": [],
    "notes": [
        "Round 4 delta read in full: git diff 4a8690a HEAD for L05.html, L06.html, cards.json (L05/L06 cards), lab-AC2-L05-1.py and lab-AC2-L06-1.py (every hunk). Other slice files unchanged in the delta except L03/L04/L07/L08 (not in this slice).",
        "Round-3 FAIL rows: r3-num-L06-a2z, r2-math-E2-zgap-cause, r3-hyp-L06-shift, r3-prose-L06-s2-purpose, r3-prose-L06-s5-bullet (rewritten sentence now carries a new unsourced mechanism; FAIL), num-L05-derived and num-L06-derived (both still carry displayed-arithmetic errors; see the arith rows).",
        "Round-3 FAIL rows that are now PASS: r2-math-E2-zgap-cause (cause now hedged and the sweep is printed), r3-hyp-L06-shift, r3-prose-L06-s2-purpose.",
        "Scripts: ledgers/AC2/scripts/L05-L06-r4/recompute_r4.py (all derived figures; output " + SCRATCH + "/recompute_r4.out) and build_fragment_r4.py (this fragment). Lab, check and page outputs are in " + SCRATCH + ".",
        "Publisher pages (doi.org, AAA, Wiley, OUP, JFE, tandfonline, SSRN) were NOT fetched. Crossref api.crossref.org records were fetched with plain curl (HTTP 200) for dechow1995detecting and sloan1996stock.",
        "Mutation testing: none (lesson slice; project slice only).",
        "Architect questions (not FAILs): (a) learner text names 'BLUEPRINT §5.3' and 'the A15 contract' and 'open source requests ... plans/AC2-open-items.md' (not on the ruling's word list); (b) the 'too imprecise to recover' reading of the 0.2824 SE is accepted as a reading; (c) the authors of dechow1995detecting remain an open question (ruling 1), not resolved here.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": len(fails),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "fail_ids": fails,
    },
}

json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "pass", frag["summary"]["pass"], "fail", len(fails), "verdict", frag["verdict"])
print("fail ids", fails)
