"""Round 28, data-tooling part B (rows 160-299 of the 430-row fragment): build ledgers/S7/data-tooling-B.json and
ledgers/S7/scripts/data-tooling-r28-B/row_decisions.json from the round-26 fragment at c9beb92 and the decisions below.
Every CARRY row is checked here by git diff --quiet 47bac8d c9beb92 -- <files> (or passage-level for the files named)."""
import json, re, subprocess, sys, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
D = ROOT / "ledgers/S7/scripts/data-tooling-r28-B"
old = json.loads((ROOT / "ledgers/S7/data-tooling-B.json").read_text(encoding="utf-8"))
rows_old = old["rows"]
CARRY_BASE = "47bac8d"
GENERIC = "the claim is text, a registry fact or a test outcome, with no toolchain numeric"

def git_identical(files):
    r = subprocess.run(["git", "diff", "--quiet", CARRY_BASE, "c9beb92", "--", *files], cwd=ROOT)
    return r.returncode == 0

def files_of(row):
    # subject files are the ones the row's location names (evidence mentions other files as context only)
    text = row["location"]
    cands = re.findall(r"((?:tools|tests|course|references|curriculum|\.github|ledgers)/[\w./*\-]+|VERIFIER_RULES\.md|BUILDER_RULES\.md|CLAUDE\.md)", text)
    out = []
    for c in cands:
        c = c.rstrip(".,;:)")
        if c.startswith("ledgers/"):
            continue
        out.append(c)
    kept = []
    for c in sorted(set(out)):
        if c.endswith("*") or (ROOT / c).exists():
            kept.append(c)
        else:
            print("  note: location path not in checkout, dropped:", c, "in", row["id"])
    return kept

# passage-level carries: file changed between 5e5da87 and 47bac8d, with the change outside the cited passage
PASSAGE = {
    "tools/build_site.py": "its only change since 5e5da87 is line 382 (git diff -U0), outside the cited lines 105-110 and 138",
    "references/references.json": "since 5e5da87 only generated_at and four used_by 'AP1' lines changed (git diff -U0); no entry text changed",
    "course/modules/S/S7/L01.html": "since 5e5da87 only line 133 changed (git diff -U0), outside the cited lines",
    "course/modules/S/S7/project.html": "since 5e5da87 only line 195 changed (git diff -U0), outside the cited lines",
    "VERIFIER_RULES.md": "since 5e5da87 changed at lines 72, 152-161 and 215-220 (git diff -U0), outside the cited lines 41-44",
    "tools/data_sources.yaml": "since 5e5da87 changed at lines 31-37 and 65-71 (git diff -U0), outside the cited passages",
}

# ---- decisions: id -> (kind, status, text)
# kind: CARRY (carried on byte-identity since 47bac8d; text is the basis), OWN (re-derived today; text is the evidence),
#       CITE (covered by an accepted ledger row; text names it), UNV (not compared; text names what was not compared)
D_ = {}
def d(i, kind, status, text): D_[i] = (kind, status, text)

d("r16-invert-real-data", "OWN", "PASS", "Re-derived in round 28 by invert_check.py (logs/invert_check.out) from the raw Federal Reserve zips saved under /tmp/ap1-r5/data-tooling/raw27: all 24,132 inverted cells of the committed CSVs fx_daily.csv and fx_monthly.csv equal an exact Fraction reference (integer decade search, hand half-to-even rounding), and the reference equals tools/fetch_data.py::_invert on all 103,989 raw inverted observations in the two datasets' date ranges: 0 disagreements.")
d("r16-invert-random", "OWN", "PASS", "Re-derived in round 28 by invert_check.py section 2 (logs/invert_check.out): 200,000 seeded random plain decimals (seed 20261028; 1-40 digits, trailing-zero and sign variants, zeros skipped) through the exact reference and tools/fetch_data.py::_invert: 0 disagreements.")
d("r16-invert-targeted", "OWN", "PASS", "Re-derived in round 28 by invert_check.py section 3 (logs/invert_check.out): 40,000 inputs at the eighth-digit ties (seed 20261029; x = 1/T truncated at 40 significant digits and one unit above) and 40,000 inputs near powers of ten (T = 10^k(1-d), d up to 1e-9): 0 disagreements with the exact reference.")
d("r16-invert-tests-cases", "OWN", "PASS", "Re-derived in round 28 by invert_check.py section 1 (logs/invert_check.out): the 17 (value, expected) pairs of test_inversion_keeps_eight_significant_digits_in_plain_decimal read from tests/test_fetch_data.py by AST; the exact reference reproduces every expected string (0 mismatches). tests/test_fetch_data.py: 65 passed today (logs/pytest_three_summary.log).")
d("r16-invert-spec", "OWN", "PASS", "Re-derived in round 28 by invert_spec_check.py (200,000 seeded random plain decimals, seed 20261030): for every input floor(log10(1/|x|)) is L0-1 or L0 with L0 = len(str(q)) - len(str(p)) for |x| = p/q in lowest terms, and the code's lead after the one-step correction equals the decade: 0 failures (logs/invert_spec_check.out). tools/fetch_data.py is byte-identical since 47bac8d.")
d("r16-retired-round15-mutants", "OWN", "PASS", "Round-28 check: 'quantize' occurs 2 times in tools/fetch_data.py at 9334148^ and 0 times at 9334148 and at c9beb92 (git show | grep -c). The round-15 mutants 35-48 target that Decimal quantize code, which no longer exists, so they cannot be re-run; their behaviour is covered by the I01-I18 rows (carried). The round-15 mutant list itself is not re-run.")
d("numbers-L08-E1-solution-704", "OWN", "PASS", "Re-derived in round 28 by e1_numbers.py (logs/e1_numbers.out), scipy quad on the density 19 phi Phi^18: E[Q19] = 1.844482 (page 1.844); sd 0.529090 (page 0.529); sqrt(1 + 0.529^2) = 1.131301 (page 1.1313); delta = 1.844 + 1.2816 x 1.1313 = 3.2939 (page 3.294); mu = 3.294/sqrt(500) = 0.147312 (page 0.147); 0.147 sqrt(252) = 2.334 and unrounded 2.3385 (page 2.3). The exact law of Q19 gives P(Z + 3.294 > Q19) = 0.8993, the page's 0.9 approximation.")
d("numbers-L08-E1-sweep-claim", "OWN", "PASS", "Re-derived in round 28 by e1_numbers.py with Lab 2's own pbo() (copied from tests/labs/S7/lab-S7-L08-2.py; 1000 days, 20 configurations, 10 blocks; 400 replications per drift; seed 20261101): mean PBO 0.2245 (drift 0.00100), 0.1023 (0.00125), 0.0525 (0.00150), 0.0224 (0.00175), 0.0055 (0.00200). The mean crosses 0.05 between 0.00125 and 0.00150, near the derived 0.00147 (0.147 per day), as the page says.")
d("L04-hunks-other-slice", "CITE", "PASS", "Covered by ledgers/S7/L03-L04.json rows L04-math-remark3.5 (the changed Remark 3.5 cut-off sentence and limits 0.258, 0.150), R15-remark35-limit-algebra (the limit algebra of the same line) and L04-num-E4 (the E4 numbers paragraph at line 754 and its expected block 742-752) (PASS, re-derived on 49def2c): course/modules/S/S7/L04.html is byte-identical from 49def2c to c9beb92 (logs/pin_checks.out, rc 0), so the cited passages are the same text.")
d("chg-H01-L01-M1c", "OWN", "PASS", "Re-derived in round 28 by numbers_r28B.py (logs/numbers_r28B.out) on L01.html Problem M1 (lines 498-508): (a) sqrt(2 ln 20) = 2.447747 (2.4477), 1/sqrt(756) = 0.036370 (0.03637), sqrt(252) = 15.8745 (15.875), bound 1.41321 (1.413); (b) Phi^-1(0.95) = 1.644854 (1.6449), Phi^-1(1 - 1/(20e)) = 2.088110 (2.0881), bracket 1.9007, estimate 1.0974 (1.097); (c) exact E[max of 20] = 1.8675 by quad (1.8675), annualised 1.0782 (1.078), approximation (3) 1.10. The Lab 1 second table (exact means and sds for N = 10, 20, 100, 1000) equals quad (1.5388/0.5868, 1.8675/0.5251, 2.5076/0.4294, 3.2414/0.3514) and the twin's output (logs/twin_L01-1.out).")
d("chg-H02-L02-sidak-gain", "OWN", "PASS", "Re-derived in round 28 by numbers_r28B.py (logs/numbers_r28B.out): Sidak 1 - 0.95^(1/20) = 0.0025613788 (page 0.0025614); relative gain 0.0025614/0.0025 - 1 = 2.455% (page 2.46%); Bonferroni FWER under independence 1 - (1 - 0.0025)^20 = 0.04883 (page 0.0488); the misconception's 'about 2.5%' at m = 20 is the same 2.455% rounded.")
d("chg-H03-L02-R1-solution", "OWN", "PASS", "Re-derived in round 28 by running the twin tests/labs/S7/lab-S7-L02-3.py under python -I -W error (logs/twin_L02-3.out, exit 0): m = 50 false-null case, power and FWER: Bonferroni 0.5803 / 0.0250, Holm 0.6212 / 0.0355 (page 0.58 and 0.62). Closed form check: Bonferroni per-test power = Phi(3.5 - Phi^-1(0.9995)) = Phi(0.2095) = 0.583, consistent with the seeded 0.5803. 'About 40%' = 1 - 0.58 = 0.42.")
d("chg-H05-L06-disagreement-span", "OWN", "PASS", "Re-read in round 28 from the abstracts: Crossref 10.1093/rfs/hhy131 (Hou, Xue, Zhang, 'Replicating Anomalies', RFS 33(5) 2019-2133; HTTP 200): 'With microcaps mitigated via NYSE breakpoints and value-weighted returns ... single test hurdle of the absolute t-value of 1.96 ... higher multiple test hurdle of 2.78' (the span's construction sentence). Crossref 10.1111/jofi.13249 (Jensen, Kelly, Pedersen, J. Finance 78(5) 2465-2518; HTTP 200): 'a Bayesian model of factor replication', 'can be clustered into 13 themes', 'strengthened (not weakened)' by the large number of factors (first page 2465 = locator). OpenAlex W4211170237 (Harvey, Liu, Zhu 2015; HTTP 200): 'a new multiple testing framework', 'A new factor needs to clear a much higher hurdle, with a t-statistic greater than 3.0', 'most claimed research findings in financial economics are likely false'. The span's reading 'a frequentist hurdle charges for the number of predictors' is the page's paraphrase of the multiple-testing framework; the Theorem 4.2 cross-reference is the lesson's own (L06 line 257).")
d("chg-H06-L06-misconception-358", "CARRY", "PASS", "the misconception's span is the Section 5 claim whose abstracts were re-read today (chg-H05-L06-disagreement-span); the page passage is unchanged")
d("chg-H07-L07-remark210-ledoit", "OWN", "PASS", "Re-read in round 28 from the published article (curl https://www.econ.uzh.ch/dam/jcr:ffffffff-935a-b0d6-0000-00007214c2bc/jef_2008pdf.pdf, HTTP 200, 308,784 bytes; pdftotext): Remark 3.1 (text lines 277-285) states that Opdyke's formulae for the time-series case 'are incorrect, since they are equivalent to the formulae for the i.i.d. case'. The Remark 2.10 span (L07.html line 211) states the same, with locator 'Remark 3.1 (published version, Journal of Empirical Finance 15(5), 2008)'. Crossref 10.1016/j.jempfin.2008.03.002 (HTTP 200): 15(5), pages 850-859.")
d("chg-H08a-L07-sec5-JK-T", "OWN", "PASS", "Re-read in round 28 from the published PDF (see chg-H07): Section 2 (text lines 114-120): Memmel (2003) and Jobson and Korkie (1981) use a formula for Omega 'that crucially relies on i.i.d. return data from a bivariate normal distribution', which is the covariance the span describes (sigma_i^2 and sigma_12 for the means, 2 sigma^4 for the variances, zero cross terms). Remark 3.1 supplies the corrected formulae. The page's further claims (delta method gives (5); Corollary 5.2; kappa_22 = 1 + 2 rho^2 and P5(b)) are internal to the lesson and are covered by the accepted L07-L08 rows L07-math-sec5-jk-paragraph and L07-P5b-coefficient.")
d("chg-H08b-L07-sec5-B-ledoit", "OWN", "PASS", "Re-read in round 28 from the published PDF (see chg-H07): the abstract states 'A simulation study demonstrates the improved finite sample performance' and 'we suggest to construct a studentized time series bootstrap confidence interval for the difference of the Sharpe ratios'; Section 4 and the Section 5 footnotes give T = 120 (text lines 468, 541); Table 1 at 1% nominal: JKM 3.5% for t6-IID and 2.5% for Normal-VAR (liberal), the bootstrap columns 1.0-1.6% (near nominal); Section 5 states HAC inference is 'often liberal in finite samples'.")
d("chg-H10-L07-lab4-interpretation", "OWN", "PASS", "Re-derived in round 28 for interpretation (3) (scope of the hunk) by lab4_part3_r28B.py (logs/lab4_part3_r28B.out): b(0.09) = 1 + 2(0.09) + 2(0.09)^2 = 1.1962; first-order sd 1 - 0.09 x 2.36/(2 x 1.1962) = 0.9112 (0.91); mean sqrt(914) x 0.09/sqrt(1.1962) = 2.4878 (2.488); Phi((2.488 - 1.645)/0.911) = 0.8226 (0.82). The twin tests/labs/S7/lab-S7-L07-4.py (logs/twin_L07-4.out, exit 0) prints 'MinTRL 401 0.9473 0.4888' and '80%_power 915 0.9940 0.8297' (median PSR 0.947; 49% and 83% pass) and formula (4) 1.1167 vs simulated 1.1582.")
d("chg-H11-L07-E3-solution", "OWN", "PASS", "Re-derived in round 28 by numbers_r28B.py (logs/numbers_r28B.out): E[max of 50 normals] = 2.249074 (page 2.249) and variance 0.215712 (0.216), by quad; average pairwise correlation 2 C(50,2) 0.9 / C(100,2) = 0.44545, so 1 - rho = 0.5545 and sqrt(0.5545) x 2.5306 = 1.884 (hurdle); Y mean sqrt(0.1) x 2.249 = 0.711, sd sqrt(0.9 + 0.1 x 0.216) = 0.960, E max approx 0.711 + 0.960/sqrt(pi) = 1.2528 (1.25); overstatement 1.884/1.25 - 1 = 50.7% ('about 50%'). The twin sol-S7-L07-E3 (logs/twin_sol-L07-E3.out) prints mass 1.000000, mean_of_max 2.249, variance_of_max 0.216.")
d("chg-H12-card-c069", "OWN", "PASS", "Re-checked in round 28: card S7-c069 back = PSR(SR_0) with SR_0 = sqrt(Var[{SR_n}]) ((1 - gamma)Phi^-1(1 - 1/N) + gamma Phi^-1(1 - 1/(N e))), the same formula as L07 Definition 3.1 equation (3) (L07.html lines 220-221). The DSR author version (davidhbailey.com/dhbpapers/deflated-sharpe.pdf, 'This version: July 31, 2014', HTTP 200, 1,048,118 bytes; pdftotext) gives the approximate expected maximum of N independent trials in its Eq. (1) with the same bracket; the text layer drops the Greek and bracket symbols, so the bracket is read from its surviving structure ('approx. 0.5772' Euler constant, Phi, e). The Crossref record of 10.3905/jpm.2014.40.5.094 (HTTP 200) has the same title. Grade C.")
d("chg-H13-card-c128", "CARRY", "PASS", "the card's efron2004large claim is the Remark 7.5 span (chg-H04 family) and its registry record; the citing card text and registry entry are unchanged")
d("chg-H14-card-c204-grade", "CARRY", "PASS", "card S7-c204 text and its L06 Section 5 span (line 324) were re-read today through chg-H05-L06-disagreement-span; the grade B and the two cites match those spans")
d("chg-H15-card-c207-cite", "OWN", "PASS", "Re-read in round 28 from the DSR author version (dsr.txt): Eq. (2) uses the variance of the trials' SRs with N the number of independent trials, and Appendix A.3 ('Estimating the number of independent trials') introduces the 'implied independent trials' N-hat from the average correlation of M dependent trials. So the source pairs the implied count with the cross-sectional variance, as the card says. The 'double count' is the lesson's own inference (Definition 3.1, Section 4), which the card cites to Definition 3.1, not to the source. Grade C and basis 'Lab 3 (SIMULATED)' kept.")
d("chg-H16-card-c238-grade", "CARRY", "PASS", "card S7-c238 is a definition card with no grade; its text matches L01 Definition 3.1 (lines 123-124), both unchanged since 47bac8d")
d("chg-H17-card-c240", "OWN", "PASS", "Re-derived in round 28 by prop42_mc_r28B.py (logs/prop42_mc_r28B.out): the representation SR_n = C + sqrt((1-rho)/T) eps_n with C ~ N(0, rho/T) common to all n gives Var = 1/T and Cov = rho/T (checked: Var x T = 0.996-1.003, Cov x T = rho within 0.5%), and E[max_n SR_n] equals sqrt((1-rho)/T) E[max eps_n] in all nine cells (N in 5, 20, 50; rho in 0.2, 0.5, 0.9; 200,000 replications; every difference within 2 standard errors). The proof is linearity with E[C] = 0 (L07.html line 305-311), so the identity is exact.")
d("card-c188-L02-misconception", "OWN", "PASS", "Re-derived in round 28: card S7-c188 back and L02.html line 356 say Example 2.4 buys 'a relative gain of about 2.5% at m = 20'; the exact relative gain is 0.0025614/0.0025 - 1 = 2.455% (numbers_r28B.py, logs/numbers_r28B.out), so 'about 2.5%' is the same figure rounded.")
d("hours-sums-hub-curriculum", "OWN", "PASS", "Re-derived in round 28 by hours_r28B.py (logs/hours_r28B.out): the eight lesson data-hours are 10, 7, 8.5, 8.5, 11, 7, 10, 8 = 70 (= the hub's data-hours-lessons 70); the hub's data-hours-project 30; 70 + 30 = 100 = the S7 module hours in curriculum/curriculum.json. Project share 30% (checker range 10-40%). render_curriculum.py reproduces curriculum/curriculum.json and CURRICULUM.md with no diff (logs/curriculum_diff.log, rc 0), and check_pages.py --unit S7 PASS (logs/check_pages_S7.log).")
d("lab-embed-identity", "OWN", "PASS", "Re-derived in round 28 by lab_embed_r28B.py (logs/lab_embed_r28B.out): all 42 S7 twins (34 lab-S7-*.py and 8 sol-S7-*.py) compared with the code block of their page after HTML unescape: 41 identical. lab-S7-project-2 is a completion lab (class 'lab completion'): its page block shows two lines as '___' blanks by design; the diff is exactly those two lines, which tools/run_labs.py's completion rule accepts (every page line equals the twin line or contains a blank). run_labs S7: PASS (42/42) today (logs/run_labs_S7.log).")
d("chg-L01-lab1-table", "OWN", "PASS", "Re-derived in round 28 (logs/numbers_r28B.out): the second table of L01's Lab 1 (N = 10, 20, 100, 1000: exact mean and sd of the maximum) equals quad integration (1.5388/0.5868, 1.8675/0.5251, 2.5076/0.4294, 3.2414/0.3514); the twin lab-S7-L01-1 run today prints the same nine lines (logs/twin_L01-1.out); run_labs S7 42/42.")
d("chg-L01-twin-lab-S7-L01-1", "CARRY", "PASS", "tests/labs/S7/lab-S7-L01-1.py is byte-identical since 47bac8d (it is not in the 47bac8d..c9beb92 diff), its output was re-run today (logs/twin_L01-1.out, exit 0) and run_labs S7 42/42 (logs/run_labs_S7.log)")
d("chg-L01-M2-sentence", "OWN", "PASS", "Re-derived in round 28 (logs/numbers_r28B.out) for L01 Problem M2 (solution, lines 512-513): bound sqrt(2 ln 50) = 2.797150 x (1/sqrt(60)) x sqrt(12) = 1.2509 (page 1.251); bracket at N = 50 = 0.4228 x 2.0537 + 0.5772 x 2.4393 = 2.2763; estimate 2.2763 x 0.12910 x 3.4641 = 1.0180 (page 1.018). 'About what luck alone produces' is interpretation, not a number.")
d("chg-L01-E1-solution", "OWN", "PASS", "Re-derived in round 28 (logs/numbers_r28B.out) for L01 Problem E1 (line 588): sqrt(252/630) = 0.632455532 (page 0.632456); approximation (3) at N = 10, 100, 1000 = 1.5746, 2.5306, 3.2551, times the multiplier = 0.9959, 1.6005, 2.0587 (page 0.996, 1.600, 2.059); exact expectations 1.5388, 2.5076, 3.2414 times the multiplier = 0.9732, 1.5859, 2.0501 (page 0.973, 1.586, 2.050); gaps 0.023, 0.015, 0.009 (page 0.009-0.023); standard error bound 0.5868 x 0.632456/10 = 0.0371 (page 0.037); 2 SE = 0.07.")
d("chg-L03-bh-caption", "OWN", "PASS", "Re-derived in round 28 (logs/numbers_r28B.out): Benjamini-Hochberg on the ten Example 2.2 p-values (0.001, 0.008, 0.012, 0.021, 0.024, 0.046, 0.060, 0.074, 0.205, 0.212; q = 0.05): the largest k with p(k) <= k q/m is k = 5, so ranks 1-5 are rejected, including rank 4 (p = 0.021 > its line 0.020). The caption's 'including any smaller p-value that sits above its own line' holds. The figure's readout is covered by the accepted rows R25-fig-L03-bh-geometry (49def2c).")
d("chg-L03-S9-bullet", "CARRY", "PASS", "the bullet points to Remark 7.5 and asserts no number or span; L03.html is byte-identical since 47bac8d")
d("chg-L05-lab6-hypothesis", "CITE", "PASS", "Covered by ledgers/S7/L05-L06.json row L05-lab6-unsourced-1.5 (PASS, re-derived on 47bac8d): the sentence's 30 x 0.05 = 1.5 expected nominal rejections of the 30 one-sided rule tests (linearity of expectation, 'at nominal size'). course/modules/S/S7/L05.html is byte-identical from 47bac8d to c9beb92 (logs/pin_checks.out). The lab's printed output in round 28 (logs/twin_L05-6.out) has 0 per-rule rejections, the per-rule critical value 1.645 and largest t-statistic 1.105, consistent with the hypothesis.")
d("chg-L05-lab6-interpretation", "OWN", "PASS", "Checked in round 28 against the twin's own output (logs/twin_L05-6.out, python -I -W error, exit 0): largest t 1.105 (EUR, MA50), per-rule critical value 1.645, Holm first step 2.935, StepM 2.837, two-sided band 3.032, mean pairwise correlation 0.221, 14 rule-days held flat, Reality Check p 0.853, SPA-style p 0.821, best rule mean 1.97 with interval -3.43 to 7.36, half-widths 5.04 to 7.26 (so at least 10.08 points), block lengths 5 and 20 with 0 rejections (StepM first steps 2.799 and 2.771), data 2000-10-17 to 2026-09-30. 30 x 0.05 = 1.5 is arithmetic. Every number in the paragraph matches the output.")
d("chg-L06-simmons-scope", "OWN", "PASS", "Re-read in round 28: Crossref 10.1177/0956797611417632 (Simmons, Nelson, Simonsohn, 'False-Positive Psychology'; HTTP 200): 'empirical psychologists' nominal endorsement of a low rate of false-positive findings (<= .05), flexibility in data collection, analysis, and reporting dramatically increases actual false-positive rates ... computer simulations and a pair of actual experiments'. The L06.html line 168 span ('Outside finance, Simmons, Nelson and Simonsohn show, with computer simulations and two experiments, that flexibility ... dramatically increases actual false-positive rates above the nominal 5%') matches; the scope words are the subject's own field (psychology).")
d("chg-L06-prop32-proof", "OWN", "PASS", "Re-derived in round 28 (logs/numbers_r28B.out) for the Proposition 3.2 proof (L06.html line 276): c = sqrt(pi/2)/e = 0.46106850 (0.46107); z* = Phi^-1(1 - p/2) at p = 1/e = 0.900453 (0.9005); z* + 1/z* = 2.011005 (2.01101); u(z*) = 1 - c(z* + 1/z*) = 0.072789 (0.0728); p = 0.6: z = Phi^-1(0.7) = 0.524401 (0.5244), z^2/2 = 0.137498 (0.1375), -ln 0.6 = 0.510826 (0.5108).")
d("chg-L06-lu-span", "OWN", "PASS", "Re-read in round 28: RePEc IDEAS item page for Lu (2025), finlet v86 (https://ideas.repec.org/a/eee/finlet/v86y2025ipcs1544612325017453.html; HTTP 200, 35,206 bytes): the abstract contains 'pessimistic', 'spectrum of prior assumptions', 'rather than contradictory evidence' and 'different prior beliefs' (substring checks True). The grade C and the Abstract locator match. Not re-read: the Crossref SSRN record (10.2139/ssrn.5519818).")
d("chg-L06-table-hlz", "OWN", "PASS", "Re-read in round 28: the HLZ sentence 'A new factor needs t > 3.0; most claimed findings are likely false' matches the OpenAlex abstract of W4211170237 (HTTP 200); the counter-evidence cells are jensen2023there (Crossref 10.1111/jofi.13249, HTTP 200: 'strengthened (not weakened)'), chen2019publication (registry) and chen2025t (Crossref 10.1287/mnsc.2023.03083, HTTP 200: 'I show these calls may be difficult to justify empirically'). Grade B.")
d("chg-L06-table-lu", "OWN", "PASS", "Re-read in round 28 (RePEc item page, HTTP 200, see chg-L06-lu-span): the cell 'read as a difference in priors by lu2025replication' matches the abstract's 'different prior beliefs' and 'prior assumptions' wording.")
d("chg-card-c185-basis", "OWN", "PASS", "Checked in round 28: the figure after Remark 3.4 is labelled 'SIMULATED' (L04.html line 182) with the source line 'formula (2) evaluated exactly on one AR(1) sample of 500 observations' (line 183); Lab 1's code is labelled '# SIMULATED AR(1) series' (tests/labs/S7/lab-S7-L04-1.py line 4), and its twin run today prints the block-20 estimate 0.0849 and block-50 estimate 0.0813 (logs/twin_L04-1.out), so the estimate falls between block lengths 20 and 50 as S7-c185's back says. The basis names both correctly. Grade C.")
d("chg-card-c241-lu", "OWN", "PASS", "Re-read in round 28: the RePEc Lu (2025) abstract (see chg-L06-lu-span) contains the card's sentence ('pessimistic' vs 'optimistic' conclusions 'reflect different points along a spectrum of prior assumptions, rather than contradictory evidence'). L06.html Section 5 ('Is most of the zoo false?') is line 314 and the span is line 324, inside it.")
d("chg-card-c242-roquain", "OWN", "PASS", "Re-read in round 28 from arXiv:1912.03109v3 (https://arxiv.org/pdf/1912.03109v3, HTTP 200, 1,234,812 bytes; pdftotext): the abstract says an AMO procedure 'exists if and only if the sparsity parameter k ... is of order less than n/log(n)'; Theorem 2.5 (text lines 577-580): (i) for k_n over n/log(n) there is no AMO procedure, (ii) for k_n under n/log(n) the plug-in BH procedure is AMO. Crossref 10.1214/21-aos2141 (HTTP 200): Annals of Statistics 50(2) 1095-1123, 2022. The card is grade T with the locator 'Theorem 2.5 of arXiv v3, 2020'; the published-version numbering was not checked.")
d("chg-registry-lu2025", "CARRY", "PASS", "the registry entry lu2025replication is unchanged since 47bac8d except used_by; tools/verify_refs.py --unit S7 re-resolved it today (logs/verify_refs_unit_S7_live.log: 94 of 560, 0 problems)")
d("chg-site-lu2025", "OWN", "PASS", "build_site.py --check today: 'site data current: 6 outputs' (logs/build_site_check.log); the registry entry's text is unchanged (only used_by and generated_at changed in references/references.json since 5e5da87).")
d("counter-roquain2022", "CARRY", "PASS", "the search of the citing set was made in round 21; today OpenCitations lists 9 citing rows for 10.1214/21-aos2141 (ext/oc_aos.json, HTTP 200), the same count, so the citing set has not grown; titles not re-read today")
d("counter-efron2004", "CITE", "PASS", "Covered by ledgers/S7/L03-L04.json row R20-span-L03-L409-efron2004large-11 (PASS, re-derived on 49def2c; its claim span is the same line 409 efron2004large span with its counter-evidence check): course/modules/S/S7/L03.html is byte-identical from 49def2c to c9beb92 (logs/pin_checks.out). Round-28 OpenCitations count: 753 citing rows for 10.1198/016214504000000089 (HTTP 200), the same count as the round-24 search.")
d("counter-kao2025", "CARRY", "PASS", "OpenCitations today lists 0 citing rows for 10.1007/s11156-025-01474-6 (HTTP 200; ext/oc_kao.json), matching the earlier search; the citing text of S7-c234 and L07 Remark 2.9 is unchanged since 47bac8d")
d("r20-mut-summary", "UNV", "UNVERIFIABLE", "NOT re-run: the 49-mutant add_reference harness (scratch scripts/mutants_ar.py and its results out/mutants_ar_r22.json) is not archived in the repository, and no copy of the mutant texts exists in ledgers/S7/mutants. The individual mutant rows (r20-mut-R03 and others) are carried under the mutant rule, but the summary's count of 49 and its killed total could not be re-derived. Re-create the harness under ledgers/S7/scripts/ to close this row.")
d("r16-invert-equiv-I03", "CARRY", "PASS", "the proof is Fraction arithmetic (no toolchain numeric); re-checked today: the only power of five in (2e7, 2e8) is 5^11 = 48828125, giving the tie k = 24414062 with last digit 2 (ledgers/S7/scripts/data-tooling-r28-B/logs/equiv_w4_w6_r28B.out)")
d("equiv-rerun-r18", "OWN", "PASS", "Re-checked in round 28 on Python 3.14.8 (equiv_w4_w6_r28B.py and equiv_w4_w6_r28B_b.py; logs/equiv_w4_w6_r28B.out, logs/equiv_w4_w6_r28B_b.out): W4 (\\d for [0-9]): 20,000 non-ASCII-digit date strings admitted by \\d and refused by date.fromisoformat (0 accepted); the four listed Unicode examples are refused. W6 (search for fullmatch): fromisoformat accepts only lengths 8 and 10, so no accepted string can properly contain a 10-character YYYY-MM-DD match. The I03 paragraph's '5^12 = 244140625 ... (n = 24414062)' mixes two values: the tie is 2n+1 = 5^11 = 48828125 (5^12 is outside the range); the conclusion (last digit 2, even) is unchanged. I05 and I08 carried as proofs.")
d("mutant-W13-retired", "OWN", "PASS", "Re-checked in round 28: 'if Decimal(value) == 0' occurs 0 times in tools/fetch_data.py at c9beb92 (grep -c), and the current zero guard is 'if exact == 0' at line 211 (I12, the same guard); the retirement of W13 as a duplicate of I12 stands.")
d("registry-count-556", "OWN", "PASS", "Re-checked in round 28: references/references.json header count 560 and 560 entries (python json); verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (logs/verify_refs_offline.log). The round-25 count of 559 is historical.")
d("r16-refs-live-scope-count", "OWN", "PASS", "Re-run in round 28: verify_refs.py --unit S7 (live, network): 'live re-verification of S7: 94 of 560 entries, 0 problems', rc 0 (logs/verify_refs_unit_S7_live.log).")
d("banned-phrases", "OWN", "PASS", "Re-run in round 28: tools/check_pages.py --unit S7: 'check_pages S7: PASS' (logs/check_pages_S7.log). Its BANNED list (tools/check_pages.py lines 58-74: TODO, TBD, lorem, 'for brevity', ..., 'obviously', 'clearly', '...') is applied to every S7 page's visible prose, so the added lines since 5e5da87 carry no banned string.")
d("r20-banned-phrases-added-lines", "OWN", "PASS", "Re-run in round 28 as for banned-phrases: check_pages.py --unit S7 PASS (logs/check_pages_S7.log), which applies the same banned list to every S7 page.")
d("cards-duplicates", "OWN", "PASS", "Re-scanned in round 28 by cards_scan_r28B.py (logs/cards_scan_r28B.out): 243 cards, 243 unique ids, 0 duplicate fronts, 0 duplicate backs.")
d("cards-cite-keys", "OWN", "PASS", "Re-scanned in round 28 by cards_scan_r28B.py (logs/cards_scan_r28B.out): every cite key of every card is a key of references/references.json (560 entries); none missing.")
d("cards-per-lesson-counts-r18", "OWN", "PASS", "Re-counted in round 28 by cards_scan_r28B.py (logs/cards_scan_r28B.out): L01 29, L02 27, L03 33, L04 29, L05 40, L06 21, L07 40, L08 24; sum 243.")
d("test-zip-determinism-r18", "OWN", "PASS", "Re-run in round 28 by zip_determinism_r28B.py in two separate processes (0 s and 3 s apart): sdmx_zip(SERIES) = 2154 bytes, sha256 0e7175a76538bcd9 in both (logs), the value recorded in round 24.")
d("chg-H18-twin-sol-S7-L07-E3", "OWN", "PASS", "Re-run in round 28: the twin tests/labs/S7/sol-S7-L07-E3.py under python -I -W error (exit 0, stderr empty) prints 'mass 1.000000', 'mean_of_max 2.249', 'variance_of_max 0.216' (logs/twin_sol-L07-E3.out); run_labs S7 42/42 (logs/run_labs_S7.log).")
d("chg-H20-sdmx-zip", "OWN", "PASS", "Re-run in round 28 (zip_determinism_r28B.py): sdmx_zip(SERIES) bytes are the same in two processes (sha256 0e7175a76538bcd9, 2154 bytes); tests/test_fetch_data.py 65 passed (logs/pytest_three_summary.log).")

# ---- rows re-derived by the same method today, outside the groups above
d("chg-H04-L03-remark75-roquain", "OWN", "PASS", "Re-read in round 28 from arXiv:1912.03109v3 (https://arxiv.org/pdf/1912.03109v3, HTTP 200, 1,234,812 bytes; the same size as round 24; pdftotext): Theorem 2.5 (lines 577-580) and the abstract ('an AMO procedure exists if and only if the sparsity parameter k ... is of order less than n/log(n)') match the L03 Remark 7.5 span's locator and claim (Gaussian nulls with unknown mean and variance; N the number of tests). The published AoS numbering is not checked (Crossref 10.1214/21-aos2141 HTTP 200 confirms the record only).")
d("chg-H09-L07-remark56-ledoit", "OWN", "PASS", "Re-read in round 28 from the published PDF (see chg-H07): Section 3 gives the limiting covariance Psi of the moment vector, sqrt(T)(upsilon-hat - upsilon) -> N(0, Psi) (text line 151, eq. (3)); Section 3.1 'HAC inference' (line 188) estimates Psi by a kernel (the prewhitened QS kernel, line 356; the HAC test with the QS kernel, line 485). The span's sentence matches; L07.html line 445 is unchanged since 47bac8d.")
d("prose-L08-why-it-matters-words", "OWN", "PASS", "Counted in round 28 (python): the why-it-matters paragraph of L08.html (line 50) has 101 words (limit 120, BUILDER_RULES 4.2); L08.html is byte-identical since 47bac8d.")
d("cite-harvey2015cross-c204", "OWN", "PASS", "Re-read in round 28: OpenAlex W4211170237 (Harvey, Liu, Zhu 2015, HTTP 200): 'a new multiple testing framework', 'a new factor needs to clear a much higher hurdle, with a t-statistic greater than 3.0', 'most claimed research findings in financial economics are likely false'; the HLZ attribution of S7-c204 and S7-c237 and the L06 Section 5 claim are the same as in chg-H05-L06-disagreement-span. (Crossref has no abstract for this DOI.)")
d("cite-jensen2023there", "OWN", "PASS", "Re-read in round 28: Crossref 10.1111/jofi.13249 (J. Finance 78(5) 2465-2518, HTTP 200): the abstract's 'Bayesian model of factor replication', '13 themes' and 'strengthened (not weakened)' support the L06 span, the S7-c204 and S7-c237 cites (page 2465 = the locator).")
d("counter-hlz2015", "OWN", "PASS", "Re-read in round 28: the counter-evidence named on L06 lines 314-326 and the table row 533 is jensen2023there (Crossref HTTP 200, abstract as above), chen2019publication (registry entry, unchanged) and chen2025t (Crossref 10.1287/mnsc.2023.03083, HTTP 200: 'I show these calls may be difficult to justify empirically'). The Lu span is chg-L06-lu-span (re-read today).")
d("registry-roquain2022false", "OWN", "PASS", "Re-checked in round 28: Crossref 10.1214/21-aos2141 (HTTP 200): 'False discovery rate control with unknown null distribution: Is it possible to mimic the oracle?', The Annals of Statistics 50(2) 1095-1123 (2022); the abstract's 'an AMO procedure exists if and only if' matches the span. verify_refs.py --unit S7 today: 94 of 560, 0 problems (logs/verify_refs_unit_S7_live.log).")
d("lab-L08-2-E1-basis", "OWN", "PASS", "Re-run in round 28: run_labs S7 42/42 under python -I -W error (logs/run_labs_S7.log) includes lab-S7-L08-2; the twin's output on this checkout (logs/twin_L08-2.out) prints the Lab 2 block: mean PBO 0.4569 for 20 skill-free configurations and 0.0736 for the genuine one, and the page block equals run_labs' comparison. The E1 sweep is re-derived in numbers-L08-E1-sweep-claim.")

# ---- rows carried on byte-identity since 47bac8d (the claim is text, a registry fact, a test outcome or a mutant kill)
CARRY_IDS = [
 "r16-invert-equiv-I05", "r16-invert-equiv-I08", "r16-invert-fix-check", "r16-plain-title-spec", "r16-plain-title-tests",
 "r16-equiv-P04", "r16-refs-unit-code", "r16-equiv-V03", "doc-verifier-2.1", "cite-chen2019publication",
 "cite-gine1997student-c236", "cite-kao2025estimated-c234", "r16-card-c236", "test-plain-title-math-spans",
 "test-shouting-title-recased", "test-unit-live-run-whole-registry", "cards-changed-outside-slice", "wp7-validation-iso-dates",
 "wp7-validation-ascii-digits", "wp7-validation-mutants", "wp7-new-tests", "r16-mut-invert-killed",
 "wp7-invert-killed-check-tests", "mut-plain_title-survivors", "mut-verify_refs-survivors", "r16-mut-plain-title-killed",
 "r16-mut-verify_refs-killed", "test-malformed-cases-reason-r18", "mutant-W-family-r18", "mutant-W14-19-r18",
 "mutant-I-family-r18", "mutant-P-V-family-r18", "mut-carry-86", "r20-add-ref-registered", "r20-add-ref-admit-run-path",
 "r20-add-ref-dry-run-branch", "r20-add-ref-describe", "r20-test-dry-run-cases", "r20-test-dry-run-77c7d7b",
 "r20-test-existing-unchanged", "r20-mut-R03", "r20-mut-R04", "r20-mut-R05", "r20-mut-R06", "r20-mut-R07", "r20-mut-R11",
 "r20-mut-R12", "r20-mut-D07", "r20-mut-D09", "r20-registered-tie-break", "r21-diff-slice-hunks", "r21-test-dry-run-params",
 "r21-test-dry-run-body", "r21-test-registered-new", "r21-mut-D11", "r21-mut-A07", "r21-mut-R16", "r21-mut-R20",
 "r21-mut-C01", "r21-mut-C02", "r21-mut-C03", "r21-mut-A06", "r21-mut-C06-equivalence", "chg-H19-zip-member",
 "chg-H21-zip-with", "chg-H22-ids", "prose-L06-misconception-358", "cards-c204", "chg-L06-misconception-358", "r16-card-c237",
 "chg-H14-card-c204-grade", "chg-H13-card-c128", "chg-H16-card-c238-grade", "chg-L03-S9-bullet", "chg-registry-lu2025",
 "cite-kao2025estimated-c234", "chg-H06-L06-misconception-358", "chg-L01-twin-lab-S7-L01-1", "r16-invert-fix-check",
]
# those already decided by OWN/CITE/UNV are skipped
CARRY_IDS = [i for i in dict.fromkeys(CARRY_IDS) if i not in D_]

PASS_IDS_DOC = {}

# custom basis for a few carried rows whose claim is more specific
CUSTOM_CARRY = {
    "r16-invert-fix-check": "the three inversion cases of tests/test_fetch_data.py are unchanged; the kill of mutant I13 by the case [0.999999850000022499996625000507-1.0000001] is a test outcome on the same code (mutant harness not archived, see the mutant note)",
    "chg-H22-ids": "the ids list of test_a_malformed_download_is_refused_with_a_data_error has 11 entries (pytest --co -k malformed: 11 tests collected today)",
    "wp7-new-tests": "tests/test_fetch_data.py collects 65 tests today (pytest --co) and passes (215 with the other two data-tooling files)",
    "mut-carry-86": "the killing tests named by the carried mutants (tests/test_labs.py, test_page_checks.py, test_run_labs.py: 122 passed; test_build_site, test_fetch_data, test_refs: 215 passed) are byte-identical and pass today",
    "cards-changed-outside-slice": "the historical hunks named are git-history facts (git diff 4051c1a 190cd51); cards.json is byte-identical since 47bac8d and its 243 cards were re-scanned today (cards_scan_r28B.py)",
    "chg-L01-twin-lab-S7-L01-1": "the twin's exact-mean block is RNG-free; its output was re-run today and matches the page block (logs/twin_L01-1.out)",
    "counter-kao2025": "the OpenCitations count is re-read today (0 citing rows)",
    "r16-invert-equiv-I05": "the proof is a Fraction-based argument (no toolchain numeric); the powers-of-ten argument is unchanged",
    "r16-invert-equiv-I08": "the proof uses only the bound y < 10^8 (from r16-invert-spec, re-checked today) and integer rounding",
}

def files_for_carry(row):
    return files_of(row)

def carry_prefix(files, passage_only):
    if not files:
        return "Carried from round 27 (no repository subject file; the citing text and registry entry are byte-identical since 47bac8d):"
    whole = [f for f in files if f not in PASSAGE]
    passage = [f for f in files if f in PASSAGE]
    names = ", ".join(whole + passage)
    note = ""
    if passage:
        note = " (passage-level for " + "; ".join(f"{f}: {PASSAGE[f]}" for f in passage) + ")"
    return f"Carried from round 27 ({names} byte-identical since 47bac8d{note}):"

GATES = ("Round-28 gates on this checkout (logs in ledgers/S7/scripts/data-tooling-r28-B/logs/): pytest on tests/test_fetch_data.py, "
         "test_build_site.py and test_refs.py 215 passed; test_labs.py, test_page_checks.py and test_run_labs.py 122 passed; "
         "run_labs S7 42/42; verify_refs --unit S7 94 of 560, 0 problems; verify_refs --offline 560, 0 problems; build_site --check and fetch_data --check current.")

# rows given a CARRY decision above: their text is the carry basis
for _cid in [k for k, v in D_.items() if v[0] == "CARRY"]:
    CUSTOM_CARRY[_cid] = D_[_cid][2]
    CARRY_IDS.append(_cid)
    del D_[_cid]

new_rows = []
decisions = []
for idx, row in enumerate(rows_old):
    rid = row["id"]
    prior = row["status"]
    if rid in D_:
        kind, status, text = D_[rid]
        if kind == "CARRY":
            raise SystemExit(f"internal: {rid} in D_ as CARRY")
        if kind == "CITE":
            ledger_note = text
            evidence = text
            fix = ""
        elif kind == "UNV":
            evidence = "NOT RE-DERIVED: " + text
            fix = "Re-create the 49-mutant add_reference harness under ledgers/S7/scripts/ (or archive it) and re-run each mutant against tests/test_refs.py at this commit; the rows r20-mut-R03 to r21-mut-C06-equivalence are carried until then."
        else:
            evidence = text
            fix = ""
        files = None
    elif rid in CARRY_IDS:
        kind = "CARRY"
        files = files_for_carry(row)
        plain = [f for f in files if f not in PASSAGE]
        if plain and not git_identical(plain):
            raise SystemExit(f"carry failed for {rid}: {plain} changed since 47bac8d")
        basis = CUSTOM_CARRY.get(rid, "the cited passage, test or registry entry is unchanged, and " + GENERIC)
        status = "PASS"
        evidence = carry_prefix(files, True) + " " + basis + ". " + GATES
        fix = ""
        text = basis
    else:
        raise SystemExit(f"no decision for {rid}")
    if status != "PASS":
        fix = fix or "Re-derive or re-run; see evidence."
    new_rows.append({
        "id": rid,
        "check": row["check"],
        "location": row["location"],
        "status": status,
        "evidence": evidence,
        **({"fix": fix} if status != "PASS" else {}),
    })
    decisions.append({
        "index": idx,
        "id": rid,
        "prior_status": prior,
        "decision": kind,
        "status": status,
        "subject_files_checked_since_47bac8d": files if files is not None else [],
        "reason": (text or "")[:600],
    })

counts = {"PASS": 0, "UNVERIFIABLE": 0, "FAIL": 0}
for r in new_rows:
    counts[r["status"]] += 1
kinds = {}
for x in decisions:
    kinds[x["decision"]] = kinds.get(x["decision"], 0) + 1
non_pass = [r["id"] for r in new_rows if r["status"] != "PASS"]
frag = {
    "unit": "S7",
    "slice": "data-tooling-B",
    "round": 28,
    "verifier": "round 28 independent verifier of S7 data-tooling part B (rows 160-299 of the 430-row fragment); not the builder, not the round-26 or round-27 verifier",
    "pin": "c9beb92",
    "base": "47bac8d (carry base for rows re-run in round 27; the release commit is 5e5da87)",
    "previous_ledger": "ledgers/S7/data-tooling-B.json at c9beb92 (round 26 fragment, 140 rows, 106 PASS / 34 UNVERIFIABLE)",
    "checkout": "/tmp/verify-s7-r2-B",
    "scratch": "/tmp/ap1-r5/data-tooling-B (raw copies, live fetches under ext/, twin outputs under twins/)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if not non_pass else "FAIL",
    "rows": new_rows,
    "mutants": [],
    "registry_flags": [
        "Registry: 560 entries and header count 560 at c9beb92; verify_refs --unit S7 live: 94 of 560, 0 problems; --offline 560, 0 problems.",
        "used_by changes since 5e5da87 (hansen1991implications, kalyuga2003expertise, shleifer1997limits, tetzlaff2025cornerstone and AP1 additions) and generated_at only; no citation text changed.",
        "Working papers read by arXiv or the author PDF: roquain2022false (arXiv v3, 1,234,812 bytes, unchanged size), bailey2014deflated (author version, July 31 2014). Published AoS and JPM numbering not compared.",
    ],
    "freshness_flags": [
        "Today's external reads (round 28): Crossref HTTP 200 for 10.1093/rfs/hhy131, 10.1111/jofi.13249, 10.1016/j.jempfin.2008.03.002, 10.1214/21-aos2141, 10.1287/mnsc.2023.03083, 10.1177/0956797611417632, 10.3905/jpm.2014.40.5.094; OpenAlex W4211170237 HTTP 200; the Ledoit and Wolf PDF HTTP 200 (308,784 bytes); the DSR author PDF HTTP 200; arXiv v3 HTTP 200; RePEc Lu HTTP 200; OpenCitations (Roquain 9, Kao 0, Efron 753 citing rows) HTTP 200.",
        "Not re-read today: the Springer and SSRN records, the Crossref record of the Lu SSRN working paper, the Efron citing titles (the count only), and the Harvey-Liu-Zhu published-version numbering.",
    ],
    "notes": [
        "Round 28 (data-tooling part B: rows 160-299). All 140 evidence strings were read in full before deciding (batches of 15-25 rows). Decisions and reasons: ledgers/S7/scripts/data-tooling-r28-B/row_decisions.json; scripts and logs: ledgers/S7/scripts/data-tooling-r28-B/.",
        f"Counts: {kinds.get('OWN',0)} rows re-derived or re-read today (OWN), {kinds.get('CARRY',0)} carried on byte-identity since 47bac8d (CARRY), {kinds.get('CITE',0)} covered by an accepted ledger row (CITE), {kinds.get('UNV',0)} left UNVERIFIABLE (UNV). Verdict: {counts['PASS']} PASS, {counts['UNVERIFIABLE']} UNVERIFIABLE, {counts['FAIL']} FAIL.",
        "Carry rule: every carried subject file is byte-identical from 47bac8d to c9beb92 (git diff --quiet, logs/pin_checks.out). Files changed between 5e5da87 and 47bac8d were carried at passage level only where git diff -U0 shows the change outside the cited lines: tools/build_site.py (line 382), course/modules/S/S7/L01.html (line 133), project.html (line 195), references/references.json (generated_at and used_by only), VERIFIER_RULES.md (lines 72, 152-161, 215-220; the rule 2.1 text at 41-44 is unchanged), tools/data_sources.yaml (lines 31-37, 65-71; no S7 row cites those lines).",
        "Mutant rows (the carried kill rows) are carried under the mutant rule: their subjects and killing tests are byte-identical and pass today, and their claims do not depend on a toolchain numeric. The harnesses that produced them are not archived in this repository, so the kills were not re-run; only the 49-mutant summary (r20-mut-summary) is UNVERIFIABLE for that reason.",
        "Evidence corrections: equiv-rerun-r18 named 5^12 for the I03 tie; the tie is 5^11 = 48828125 (k = 24414062, last digit 2, even); the conclusion stands. The round-26 claim that rows 160-411 kept their decisions is superseded for this part.",
        "lab-S7-project-2 is a completion lab: its page block has two '___' blanks by design (tools/run_labs.py docstring); lab_embed_r28B.py shows that its only differences from the twin are those two lines.",
        "Not checked in this part: the other data-tooling parts A and C; the whole-registry live verify_refs (not needed for these rows); ruff, mypy and the figure sweeps (not in these rows).",
    ],
    "summary": {
        "rows": len(new_rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": 0,
        "mutants_killed": 0,
        "fail_ids": non_pass,
        "carry": kinds.get("CARRY", 0),
        "own": kinds.get("OWN", 0),
        "cite": kinds.get("CITE", 0),
        "unv": kinds.get("UNV", 0),
    },
}
out = ROOT / "ledgers/S7/data-tooling-B.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
(D / "row_decisions.json").write_text(json.dumps({"slice": "data-tooling-B", "round": 28, "rows": decisions}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(new_rows), "counts", counts, "kinds", kinds)
print("non-PASS:", non_pass)
