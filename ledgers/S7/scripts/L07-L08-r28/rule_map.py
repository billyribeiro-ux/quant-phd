"""Round 28: map each numeric row of the round-27 ledger to the derive_numbers.py checks that re-derive its numbers.

A row is matched by the first rule whose pattern occurs in its id, check or location (lower case). Rules run from
specific to general. Rows that match no rule are reported by build_fragment.py and are not marked PASS.
"""
import re

RULES = [
    (r"ex1\.4|example 1\.4|short-vol|misconception 1\b|c205|s7-c205", ["L07-ex1.4-V", "L07-ex1.4-normal", "L07-ex1.4-se-nonnormal", "L07-ex1.4-se-normal", "L07-ex1.4-ratio", "L07-ex1.4-annualized"]),
    (r"lab 1|lab1|l07-lab1|ar\(1\)|ar1|remark 1\.5|remark1\.5", ["L07-lab1-se-V082", "L07-lab1-se-V122", "L07-lab1-normal-too-high-pct", "L07-lab1-normal-too-low-pct", "L07-misc-ar1-factor", "L07-rem1.5-minTRL-AR1"]),
    (r"ex2\.3|example 2\.3|ex23", ["L07-ex2.3-annualized", "L07-ex2.3-bracket", "L07-ex2.3-se", "L07-ex2.3-PSR0", "L07-ex2.3-PSR0-argument", "L07-ex2.3-normal-se", "L07-ex2.3-normal-PSR", "L07-ex2.3-normal-arg"]),
    (r"ex2\.8|example 2\.8|ex28|after example 2\.8|sec2-annualized|num-sec2|minimum track|minTRL", ["L07-ex2.8-unit", "L07-ex2.8-minTRL", "L07-ex2.8-normal-minTRL", "L07-ex2.8-cost-days", "L07-ex2.8-cost-pct", "L07-ex2.8-annual-benchmark-daily", "L07-ex2.8-margin", "L07-ex2.8-mintrl-0.5", "L07-ex2.8-years-0.5", "L07-ex2.8-psr-benchmark", "L07-z95", "L07-z95-sq", "L07-sec2-years-1", "L07-sec2-years-0.5", "L07-sec2-years-2", "L07-annualized-b", "L07-annualized-years-1"]),
    (r"remark 2\.7|remark2\.7|rem27|rem2\.7|hedge", ["L07-rem2.7-minTRL-q252", "L07-rem2.7-years-q252", "L07-rem2.7-minTRL-q52", "L07-rem2.7-years-q52", "L07-rem2.7-minTRL-q12", "L07-rem2.7-years-q12", "L07-rem2.7-hedge-minTRL", "L07-rem2.7-hedge-years", "L07-rem2.7-appendix-59.895"]),
    (r"problem p4|\bp4\b|sampling frequenc|across sampling", ["L07-P4-q252", "L07-P4-q52", "L07-P4-q12", "L07-P4-limit"]),
    (r"remark 2\.9|remark2\.9|rem2\.9|t_beta|tbeta|t-beta|2\.9-", ["L07-rem2.9-T-ratio", "L07-rem2.9-normal-stat-kr", "L07-rem2.9-normal-median-half", "L07-lab4-b", "L07-lab4-sd-first", "L07-lab4-mean-T", "L07-lab4-pred", "L07-lab4-mc-se-V1.117"]),
    (r"example 3\.2|ex3\.2|ex32|definition 3\.1|dsr-|dsr |num-sec3|section 3|sec3", ["L07-ex3.2-bracket", "L07-ex3.2-SR0", "L07-ex3.2-annualized", "L07-ex3.2-DSR", "L07-ex3.2-DSR-arg", "L07-ex3.2-DSR-PSR-cite", "L07-ex3.2-unit-N2-bracket", "L07-ex3.2-unit-N3-bracket", "L07-M3-bracket25"]),
    (r"problem m5|\bm5\b|paired or naive|m5-", ["L07-M5-paired-theta", "L07-M5-paired-Z", "L07-M5-naive-Z", "L07-M5-paired-p", "L07-M5-naive-p", "L07-M5-annual-1", "L07-M5-annual-2", "L07-M5-se-paired", "L07-M5-se-naive"]),
    (r"problem m1|problem m2|problem m3|problem m4|\bm1\b|\bm2\b|\bm3\b|\bm4\b|m-problems|m1-m5|m1-m3|mechanics|problems-m-p|num-m-problems", ["L07-M1-bracket", "L07-M1-se", "L07-M1-normal-se", "L07-M1-PSR0", "L07-M1-annual", "L07-M2-bench", "L07-M2-PSR", "L07-M2-arg", "L07-M3-SR0", "L07-M3-DSR-arg", "L07-M3-N2-N3", "L07-M3-zN-limit", "L07-M4-days-0", "L07-M4-years-0", "L07-M4-margin", "L07-M4-days-0.5", "L07-M4-years-0.5", "L07-M4-shrink", "L07-M4-req-grew"]),
    (r"participation|\bpr\b|npr|section 4|sec4|num-sec4|lab 3|lab3|l07-lab3|two effective|effective n|effective-n|matching", ["L07-sec4-PR", "L07-sec4-PR-formula-denominator", "L07-lab3-PR-ratio", "L07-P3b-sigma", "L07-E3-hurdle-coef"]),
    (r"example 5\.5|ex5\.5|ex55|paired|misconception 6|misconception-6|misconception 5|c162|c219|s7-c219|misconceptions-new", ["L07-ex5.5-theta", "L07-ex5.5-se", "L07-ex5.5-Z", "L07-ex5.5-p", "L07-ex5.5-naive-v", "L07-ex5.5-naive-se", "L07-ex5.5-naive-Z", "L07-ex5.5-naive-p", "L07-ex5.5-se-ratio", "L07-ex5.5-annual-se", "L07-ex5.5-annual-diff", "L07-Ex5.5-annualized-1", "L07-Ex5.5-annualized-2"]),
    (r"problem e4|\be4\b|undersized", ["L07-E4-mean", "L07-E4-naive-mean", "L07-E4-naive-sd", "L07-E4-naive-sd-steps", "L07-E4-pow-paired", "L07-E4-mc-se"]),
    (r"problem e3|\be3\b|two clusters|e3-|e3 ", ["L07-E3-bracket100", "L07-E3-exact-max100-vs-approx", "L07-E3-hurdle-coef", "L07-E3-mean-Qk-root", "L07-E3-sd-Y", "L07-E3-EmaxY", "L07-E3-overstate", "L07-P3b-sigma"]),
    (r"problem e1|\be1\b|skewness and kurtosis cancel|where skewness", ["L07-E1-normal-at-4/3", "L07-E1-negskew-at-4/3", "L07-E1-root"]),
    (r"problem p5|\bp5\b|paired variance|special cases|jk|jobson", ["L07-P5b-coefficient", "L07-P5b-E-s4", "L07-P5b-E-s2"]),
    (r"problem p3|\bp3\b|cross-sectional dispersion under", ["L07-P3b-sigma"]),
    (r"problem r2|\br2\b|committee|r2-|0\.97", ["L07-R2-z", "L07-R2-bound", "L07-R2-posterior"]),
    (r"problem r4|\br4\b|after a search|minTRL after", ["L07-R4-T-1", "L07-R4-years", "L07-R4-search-factor", "L07-R4-fixed-hurdle-days", "L07-R4-fixed-hurdle-years", "L07-R4-rho05-T-1", "L07-R4-rho05-years", "L07-R4-cross-sd-ratio", "L07-R4-rho-equivalent"]),
    (r"lab 4|lab4|l07-lab-4|part 1|part 2|part 3|part1|part2|part3|crash|size of|prop 5\.4|proposition 5\.4|prop5\.4|rejection|naive test|l07-439|r25-hunk-l07-439", ["L07-lab4-b", "L07-lab4-sd-first", "L07-lab4-mean-T", "L07-lab4-pred", "L07-lab4-mc-se-V1.117", "L07-lab4-mc-se-prop", "L07-lab4-gap-se", "L07-lab4-naive-to-true", "L07-lab4-E-V-shrink", "L07-lab4-prop5.4-naive-rho-0.5", "L07-lab4-prop5.4-naive-rho0.5", "L07-P5b-coefficient", "L07-P5b-E-s4", "L07-P5b-E-s2"]),
    (r"quiz", ["L07-ex1.4-V", "L07-ex1.4-annualized", "L07-sec4-PR", "L07-ex2.8-psr-benchmark", "L07-rem2.9-normal-median-half", "L07-z95", "L07-rem2.7-minTRL-q252", "L07-lab4-E-V-shrink"]),
    (r"example 3\.3|ex3\.3|hand|split with in-sample ab|lab 1 .*l08", ["L08-ex3.3-mean", "L08-ex3.3-sd", "L08-ex3.3-R1", "L08-ex3.3-R2", "L08-ex3.3-R3", "L08-ex3.3-oos-s1", "L08-ex3.3-oos-s2", "L08-ex3.3-oos-s3", "L08-ex3.3-lambda"]),
    (r"problem m1|counting|binom|split count|number of splits|s = 10|s = 16", ["L08-M1-S-counts-4", "L08-M1-S16", "L08-M1-S8", "L08-M1-S6", "L08-M1-in-sample-S16", "L08-M1-binom10-5"]),
    (r"problem m2|logit|\bm2\b|rank 4", ["L08-M2-logit-r4", "L08-M2-logit-r7"]),
    (r"problem m3|from logits|\bm3\b", ["L08-M3-PBO"]),
    (r"problem p1|odd n|odd-n|\bp1\b|e\[\\widehat|e\[pbo|expected pbo", ["L08-P1-EPBO-N2", "L08-P1-EPBO-N3", "L08-P1-EPBO-N4", "L08-P1-EPBO-N5", "L08-P1-EPBO-N21", "L08-remark4.2-N20-formal"]),
    (r"problem p2|\bp2\b|leverage|shift|every logit|omitted|biased|canon|section 7|sec7|bullet", ["L08-P2-sd-AB", "L08-P2-shifted-AB", "L08-P2-shifted-AC", "L08-P2-logits-changed", "L08-P2-PBO-2of6-to-6of6"]),
    (r"problem p4|\bp4\b|dispers|how dispersed|p4-kr|kr-quiz", ["L08-E2-sd-mean-no", "L08-E2-sd-0", "L08-E2-ratio", "L08-lab4-sd-expected", "L08-lab4-SR0-from-disp"]),
    (r"problem e1|\be1\b|how strong|edge must|drift|e1-", ["L08-E1-pi", "L08-E1-delta", "L08-E1-mu", "L08-E1-annual", "L08-E1-10/19", "L08-E1-sd-root"]),
    (r"problem e2|\be2\b|correlated and censored|common factor|e2-|e2-solution", ["L08-E2-sd-mean-no", "L08-E2-sd-0", "L08-E2-ratio"]),
    (r"problem e3|\be3\b|died|dying|regime|e3-", ["L08-E3-binom-k1", "L08-E3-binom-k2", "L08-E3-delta5", "L08-E3-delta4", "L08-E3-delta3", "L08-E3-win5", "L08-E3-win4", "L08-E3-win3", "L08-E3-PBO-low", "L08-E3-PBO-high", "L08-E3-null-value"]),
    (r"problem r3|\br3\b|tools disagree|romano", ["L08-R3-edge", "L08-R3-Bonf", "L08-R3-full-prob", "L08-R3-DSR-N2000", "L08-R3-DSR", "L08-R3-500-edge", "L08-R3-500-win", "L08-R3-500-pbo", "L08-R3-500-PBO-unrounded"]),
    (r"lab 3|lab3|l08-lab3|edge in a growing|two-trial|rise", ["L08-lab3-p", "L08-lab3-2p(1-p)", "L08-lab3-arg", "L08-lab3-edge-stdized", "L08-lab3-rise", "L08-lab3-se-diff", "L08-lab3-ratio", "L08-lab3-select-prob", "L08-lab3-max-mean-n19", "L08-lab3-max-sd-n19", "L08-lab3-max-mean-n20", "L08-lab3-max-sd-n20", "L08-lab3-max-mean-n199", "L08-lab3-max-sd-n199", "L08-lab3-max-mean-n1999", "L08-lab3-max-sd-n1999"]),
    (r"lab 4|lab4|l08-lab4|key-results|key results|fx|currenc|dsr 0\.489|sign rule|null grid|kr-863|sec7-and-key", ["L08-lab4-ann", "L08-lab4-p-value", "L08-lab4-SR0-from-disp", "L08-lab4-sd-expected", "L08-lab4-null-share-SE", "L08-lab4-sd-gap"]),
    (r"lab 2|lab2|pure noise|20 configurations|l08-num-lab2", ["L08-remark4.2-N20-formal", "L08-P1-EPBO-N2"]),
    (r"theorem 4\.1|thm4\.1|eq \(3\)|section 4|sec4|remark 4\.2|remark4\.2|null value|exchangeable", ["L08-P1-EPBO-N2", "L08-P1-EPBO-N3", "L08-P1-EPBO-N21", "L08-remark4.2-N20-formal"]),
    (r"l08-", ["L08-ex3.3-mean", "L08-M1-S-counts-4", "L08-M2-logit-r4", "L08-M3-PBO", "L08-P1-EPBO-N21", "L08-lab3-p", "L08-lab4-ann"]),
    (r"l07-", ["L07-z95", "L07-ex2.3-PSR0", "L07-ex3.2-DSR"]),
]


def match(text):
    t = text.lower()
    for pat, checks in RULES:
        if re.search(pat, t):
            return checks, pat
    return None, None
