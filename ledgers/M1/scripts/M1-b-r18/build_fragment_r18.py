# Builds ledgers/M1/M1-b.json for round 18 (M1 slice b: L04, L05 and their twins). Rows are the verifier's own findings.
import json, sys, datetime
ROOT = sys.argv[1]
CMD = "ledgers/M1/scripts/M1-b-r18/"
PAGE = "course/modules/M/M1/"
R = []
def row(id_, check, location, status, evidence, fix=""):
    d = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

row("M1-b-cmd-pin", "command: checkout pin and slice inventory", "repository HEAD; course/modules/M/M1/L04.html, L05.html, cards.json, index.html; tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py",
    "PASS", "git rev-parse HEAD = 7143726a21ba709ef3e7c54375338021df2dfc01 (detached checkout /tmp/verify18-M1-b). git diff --stat fefbf8b 7143726: L04.html and L05.html each one line changed (L04 line 52, L05 line 52, the why-it-matters paragraph); cards.json changed (M1-c060, c160, c163, c175 removed); tests/labs/M1 not in the diff.")
row("M1-b-cmd-run_labs", "command: run_labs for M1", "tools/run_labs.py; course/modules/M/M1/L04.html; L05.html", "PASS",
    "`.venv/bin/python tools/run_labs.py --unit M1` -> 'run_labs M1: PASS (11/11)' (" + CMD + "run_labs_M1.out, exit 0). The L04 and L05 Lab 1 blocks are included in the 11.")
row("M1-b-cmd-twins", "command: lab twins alone under python -I -W error", "tests/labs/M1/lab-M1-L04-1.py; tests/labs/M1/lab-M1-L05-1.py", "PASS",
    "`.venv/bin/python -I -W error <twin>` exit 0 for both (" + CMD + "twin_L04.out, twin_L05.out). Printed lines equal the page expected blocks (run_labs PASS above).")
row("M1-b-cmd-page_smoke", "command: page_smoke for L04 and L05", "tools/page_smoke.py --unit M1 --pages L04 L05", "PASS",
    "`.venv/bin/python tools/page_smoke.py --unit M1 --pages L04 L05` -> 'page_smoke modules/M/M1/L04.html: PASS', 'page_smoke modules/M/M1/L05.html: PASS', 'page_smoke M1: PASS' (" + CMD + "page_smoke.out, exit 0). Lab run times 0.0 s.")
row("M1-b-cmd-check_pages_dag", "command: check_pages and check_dag for M1", "tools/check_pages.py --unit M1; tools/check_dag.py --unit M1", "PASS",
    "'check_pages M1: PASS' and 'check_dag M1: PASS' (" + CMD + "check_pages.out, check_dag.out, exit 0 each).")
row("M1-b-cmd-lint-types", "command: ruff and mypy on the two twins", "tests/labs/M1/ (both twins)", "PASS",
    "`ruff check tests/labs/M1` 'All checks passed!'; `ruff format --check tests/labs/M1` '11 files already formatted'; `mypy --no-incremental` on both twins 'Success: no issues found in 2 source files' (" + CMD + "ruff.out, mypy.out, exit 0).")
row("M1-b-cmd-refs", "command: verify_refs live and offline; L04/L05 cite no registry key", "references/references.json; tools/verify_refs.py; L04.html and L05.html references sections", "PASS",
    "`tools/verify_refs.py --unit M1` -> 'live re-verification of M1: 1 of 560 entries, 0 problems' (the tool re-checks one entry live); `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' (" + CMD + "refs_live.out, refs_offline.out). `grep -c 'data-cite|references.json'` on L04.html and L05.html = 0; both reference sections say the lesson cites no outside source (L04.html:459-462, L05.html:472-475).")
row("M1-b-cmd-pytest", "command: relevant pytest", "tests/test_run_labs.py; tests/test_page_checks.py; tests/test_labs.py", "PASS",
    "`.venv/bin/python -m pytest -q tests/test_run_labs.py tests/test_page_checks.py tests/test_labs.py` exit 0; three progress lines of 72, 72 and 30 dots (174 tests) (" + CMD + "pytest.out).")
row("M1-b-2.2-L04-numbers-recomputed", "2.2 numbers in prose, L04 (class a and c)",
    "course/modules/M/M1/L04.html: why-it-matters (52); Part A/B/C printed output (191-217); interpretation (218); misconceptions (251-262); Example 3.2 (~236); E1-E3 solutions", "PASS",
    "Independent recomputation with Decimal at 80 digits (" + CMD + "recompute_l04_l05.py, .out): EAR 0.0500000000, 0.0506250000, 0.0509453369, 0.0511618979, 0.0512674965; e^0.05 = 1.0512710964; every printed factor and error matches; cents 1628895, 1647009, 1648665, 1648721 (unrounded 1628894.6268, 1647009.4977, 1648664.8138, 1648721.2707); monthly-annual 18114.87 unrounded, daily-continuous 56.46; monthly-daily 1655.32 unrounded, ratio 29.32; 1656/56 = 29.5714. Interpretation ratios 9.99969 and 9.99997 match the script; the printed-digit ratio for the second pair is 10.03, which rounds to the stated 10.0 at one decimal. Why-it-matters 0.0511618979 and 5.1162%: match.")
row("M1-b-2.2-L04-M3-rounding", "2.2 numbers, L04 M3 solution", "course/modules/M/M1/L04.html:286-290 (M3 solution)", "PASS",
    "Recomputed: e^(0.05/12) = 1.004175359291, r_12 = 12 x 0.004175359291 = 0.050104311493; 0.0501043115 to ten places and 0.050104 to six (" + CMD + "recompute_l04_l05.out). Check (1+0.0501043115/12)^12 = 1.0512710964 to ten places (recomputed as 1.0512710964 at the unrounded value; the 7e-12 difference in r moves the factor by about 7e-12, below the tenth place).")
row("M1-b-2.2-L04-E2-digits", "2.2 numbers, L04 E2 solution", "course/modules/M/M1/L04.html:329-333 (E2 solution)", "PASS",
    "Factor 1.0512710951 and e^0.05 = 1.0512710964 share the decimals 05127109 (first eight); they differ at the ninth (5 vs 6). Printed error 0.0000000013 lies between 1e-9 and 1e-8 (recomputed).")
row("M1-b-2.2-L05-numbers-recomputed", "2.2 numbers in prose, L05 (class a and c)",
    "course/modules/M/M1/L05.html: why-it-matters; Definition 1.1; Example 3.1 (242-246); Lab 1 printed output (223-235); interpretation (236); misconceptions (264-275); E1-E3 (339-352)", "PASS",
    "Recomputed with Decimal (" + CMD + "recompute_l04_l05.out): equivalent rate ln(1.05) = 0.0487901642; annual/semiannual/continuous and equivalent-rate columns at t = 0.5, 1, 2, 5, 10 match; equivalence gap below 1e-76 (printed 0.0000000000); t = 5 cents 783526, 781198, 778801 (unrounded 783526.1665, 781198.4017, 778800.7831); annual-semiannual 2328 (unrounded 2327.76), semiannual-continuous 2397 (unrounded 2397.62), annual-continuous 4725; E1 23.97 CU; E3 613913.25 cents; Example 3.1 values 783,526.17, 781,198.40, 778,800.78. Lab 1 'max gap' 0.0000000000 and both checks True match the lab output.")
row("M1-b-2.2-L05-M1-M3-rounding", "2.2 numbers, L05 M1, M2, M3 solutions", "course/modules/M/M1/L05.html:285-305 (M1, M2, M3 solutions)", "PASS",
    "Recomputed: 1.04^3 = 1.124864, 1/1.124864 = 0.8889963587 -> 0.888996; 1/1.1236 = 0.889996440014, 250000 x 0.88999644 = 222499.11 -> 222,499; e^-0.06 = 0.9417645336, 500000 x = 470882.27 -> 470,882 (" + CMD + "recompute_l04_l05.out).")
row("M1-b-2.2-L05-R2-check", "2.2 numbers, L05 R2 solution", "course/modules/M/M1/L05.html:367-373 (R2 problem and solution)", "PASS",
    "(1/0.6)^(1/10) = 1.052409779149 -> r = 0.052410 to six places; 1.052409779149^10 = 1.6666666667 (10 places); 1/1.6666666667 = 0.6000000000; with 1.0524097791 the power is 1.6666666659 (diff 8e-10); 10(1+r)^9 = 15.8367 and the 4.9e-11 change in 1+r gives about 7.8e-10 in the power, consistent with the 'about 15.8 times' sentence (" + CMD + "recompute_l04_l05.out).")
row("M1-b-2.4-math-L04", "2.4 mathematics, L04 Props 2.1, 2.2, 3.1, R3",
    "course/modules/M/M1/L04.html:83-100 (Prop 2.1 and proof), 101-115 (Prop 2.2 and proof), 224-228 (Prop 3.1), 361-367 (R3), key results 372-384", "PASS",
    "Re-read every step. Prop 2.1: binomial terms, the factor prod(1 - j/m) rises with m, the k = m+1 term is strictly positive for r > 0. Prop 2.2: 0 < 1 + r/m < e^(r/m) by Assumption E, raise to the power m, (e^(r/m))^m = e^r by A2. Prop 3.1: sum law of L03 (A2). R3: positive m-th root unique, 1 + r_m/m = e^(r/m), r_m = m(e^(r/m)-1) > r via e^x - 1 > x (Assumption E). Even-m counterexample checked: (-e^(r/m))^m = e^r for even m, so the hypothesis 1 + r_m/m > 0 is needed for that case (" + CMD + "recompute_l04_l05.out for numeric witnesses).")
row("M1-b-2.4-math-L05", "2.4 mathematics, L05 Props 1.4, 2.1, 2.2, 2.4 and Remark 1.5",
    "course/modules/M/M1/L05.html:79-100 (E consequences (i)-(iii), Prop 1.4 and proof, Remark 1.5), 106-137 (Props 2.1, 2.2, 2.4 and proofs)", "PASS",
    "Re-read. Prop 1.4: b^(-s) = b^(t-s) b^(-t) by A2 with the convention, b^(t-s) > 1, so b^(-s) > b^(-t); b^(-t) = 1/b^t by L03 Prop 1.3. Remark 1.5: for -1 < r < 0 both claims reverse. Prop 2.1: convention b^u = e^(u ln b). Prop 2.2: 1 + r < e^r by E, so delta < r, then exponent order by (ii). Prop 2.4: A - B = r^2/4 > 0, x -> x^t increasing, reciprocal reverses. All steps follow from E, A1, A2, L03 Props 1.3, 1.4 (as cited).")
row("M1-b-2.4-L05-quiz-L05q5", "2.4 quiz item L05q5", "course/modules/M/M1/L05.html:431-438 (L05q5 options and explain)", "PASS",
    "Options 783,526 / 781,198 / 778,801 cents; the marked answer (continuous at 5%, 778,801) is the smallest, matching Lab 1 printed values; explain cites Example 3.1, Lab 1 and Props 2.2, 2.4 (both assume E on the page).")
row("M1-b-2.3-grades", "2.3 grades, L04 and L05", "course/modules/M/M1/L04.html: Props 2.1, 2.2, 3.1 (83, 101, 224) and key-results rows (377-384); L05.html: Props 1.4, 2.1, 2.2, 2.4 (87, 106, 116, 131) and key results (388-395)", "PASS",
    "Every proposition is marked T and is proved on its page from stated assumptions (E, A1-A3 of L03); Lab 1 outputs are cited only as checks (interpretation rows), not as the basis of any T claim. Lab-read claims are graded C in cards M1-c073, c074, c076, c090, c091, c092 (checked against Lab 1 output). Assumption E is labelled as an assumption, not a result (L04.html:79, L05.html:81-82).")
row("M1-b-2.5-lab-L04", "2.5 lab claims, L04 Lab 1", "course/modules/M/M1/L04.html: Lab 1 hypothesis (117-119), Remark 2.3 (112), interpretation (218), misconceptions 1-3 (251-262); tests/labs/M1/lab-M1-L04-1.py", "PASS",
    "Hypothesis matches the code: Part A five frequencies (1,2,4,12,365), Part B ten values of m beside e^r, Part C four conventions over 10 years, no random draws (module-level code, no random import). Interpretation 'every printed row' and 'ten values, so it does not prove convergence' match output. Remark 2.3 matches the output. No lab claim exceeds its output.")
row("M1-b-2.5-lab-L05", "2.5 lab claims, L05 Lab 1", "course/modules/M/M1/L05.html: Lab 1 hypothesis (142-145), Remark 2.3 (~120-125), interpretation (236), misconceptions 1-3 (264-275); tests/labs/M1/lab-M1-L05-1.py", "PASS",
    "Hypothesis matches the code: five times 0.5, 1, 2, 5, 10; annual, semiannual, continuous at 0.05 and the equivalent-rate factor; present values at t = 5. Interpretation's 'both checks print True' matches output; 'semiannual below annual in every row' and 'continuous below annual in every row' checked against the five printed rows; 'The lab uses one rate and five times' matches.")
row("M1-b-2.9-structure-prose", "2.9 structure, banned phrases and process words, L04 and L05",
    "course/modules/M/M1/L04.html and L05.html (full pages)", "PASS",
    "Banned-string scan (grep -i for roughly, about, historically, typically, usually, generally, often, most, some, several, many, ellipsis, round, build, builder, verifier, REQUEST) returned only: 'several' in a remark heading (L04.html:69), 'ROUND_HALF_EVEN' in code, and repeating-decimal ellipses 1.6666... (L05.html:371), 1.0066666... (L04.html:278) and 1/0.6, each with its exact value stated (1/0.6 = 5/3 exactly). Those are notation for repeating decimals, not omitted content. No placeholder, no 'it can be shown'. Every section template present (why-it-matters, sections, canon-breaks, misconceptions, problem set with worked solutions, key results, quiz, references).")
row("M1-b-2.9-DAG", "2.9 DAG and concepts for L04 and L05", "tools/check_dag.py --unit M1; L04.html meta-rows (38) and definitions (59, 67); L05.html meta-rows (38) and definitions (64, 72)", "PASS",
    "check_dag M1: PASS. Prerequisites: L04 uses exponential-and-logarithm (L03); L05 uses L03 plus compounding-frequency and continuous-compounding (L04). Concepts defined once in their own module (dfn ids compounding-frequency, continuous-compounding in L04; discount-factor, present-value in L05). No concept used before its prerequisite in these two pages.")
row("M1-b-hours", "hours: hub split versus lesson hours (arithmetic only)", "course/modules/M/M1/L01.html ... L08.html line 2 (data-hours); course/modules/M/M1/index.html data-hours-lessons, data-hours-project", "PASS",
    "data-hours: L01 8, L02 9, L03 9, L04 9, L05 8, L06 9, L07 9, L08 9; sum 70 = index.html data-hours-lessons=\"70\" and the split line '70 h lessons · 30 h project (30%)'. No hours arithmetic inconsistency. Pace not judged (architect ruling: hours are design targets).")
row("M1-b-r3-attr-L04-L05", "attribution: L03 propositions and axioms cited by L04 and L05 (re-read after the L03 text change)",
    "course/modules/M/M1/L04.html:107 (A2 uses), 224-228 (Prop 3.1), L05.html:59-61, 80-84, 88, 93, 112, 122, 137", "PASS",
    "L03.html (changed this round in text only): A1 positivity (L03:56-62), A2 addition, A3 unique inverse; Prop 1.2 e^0 = 1 (L03:72-74); Prop 1.3 e^(-x) = 1/e^x (L03:82-88); Prop 1.4 ln(e^x) = x and e^(ln y) = y (L03:92-100); Prop 1.6(a) ln 1 = 0 (L03:112-118). Every L03 item cited in L04/L05 has the statement the page uses. Proposition numbers unchanged by this round's L03 edit.")
row("M1-b-r3-monotone-uncited", "attribution: monotonicity and bound claims with no citation", "course/modules/M/M1/L04.html:83-108 and 361-367; L05.html:79-84 (Assumption E consequences (i)-(iii))", "PASS",
    "Monotonicity in m (Prop 2.1), the bound (Prop 2.2) and the strict monotone power facts are proved on the page from E and A1/A2 (L04.html:90-100, L05.html:81-84); no outside citation is needed or made.")
row("M1-b-r4-term-before-def-L04", "term before definition, L04", "course/modules/M/M1/L04.html:52 (why-it-matters), 54-56 (s1), 59 (Def 1.1), 78-80 (Assumption E)", "PASS",
    "why-it-matters uses 'periodic factor', 'effective annual rate', 'continuous factor' and says 'each defined in §1' (Def 1.1 at L04.html:59 defines F_m, EAR_m; Def 1.2 defines the continuous factor). The 'exponential bound' is named in §2 heading (L04.html:73) and defined as Assumption E (L04.html:78-79) before Prop 2.2.")
row("M1-b-r4-term-before-def-L05", "term before definition, L05", "course/modules/M/M1/L05.html:52 (why-it-matters), 59-61 (convention), 64 (Def 1.1), 79-84 (Assumption E)", "PASS",
    "Real power convention (L05.html:59-61) precedes Def 1.1 and Prop 1.4, which use it. Assumption E (L05.html:79-84) precedes Prop 1.4 (line 87). why-it-matters (line 52) names 'a valuation', 'discount factor' and 'present value', defined at lines 65 and 70 (inside §1, as the paragraph says).")
row("M1-b-r4-scope-heading-L04", "scope: L04 section 2 heading", "course/modules/M/M1/L04.html:73 (section 2 heading)", "PASS",
    "Heading: 'More frequent compounding raises the factor, and under the exponential bound stated below, stays below e^r'. Prop 2.1 (r > 0, strictly increasing in whole m) and Prop 2.2 (under E, r > 0, F_m(r) < e^r for whole m >= 1) match the heading's two claims.")
row("M1-b-r4-quiz-tolerance", "quiz: numeric answers and tolerances, L04 and L05",
    "course/modules/M/M1/L04.html:399-441 (data-answer and data-tolerance); L05.html:412-454", "PASS",
    "Each numeric answer is within its tolerance of the computed value: L04 0.0830 (|0.0829995068-0.0830| = 4.9e-7 <= 5e-5); 1197.22 (|1197.2173631-1197.22| = 0.0026 <= 0.005); 1648721 (|1648721.2707-1648721| = 0.27 <= 0.5); 0.0512710964 (|0.0512710964-0.0512710963760| = 2.4e-11 <= 5e-11). L05 0.907029 (4.8e-7 <= 5e-7); 0.048790 (1.6e-7); 783526 (|783526.1665-783526| = 0.17 <= 0.5); 0.606531 (|0.6065306597-0.606531| = 3.4e-7 <= 5e-7) (" + CMD + "recompute_l04_l05.out).")
row("M1-b-r5-P2-scope-L05", "scope: L05 Problem P2 statement and solution", "course/modules/M/M1/L05.html:317-322 (P2 statement and solution)", "PASS",
    "P2 states 'for r > 0 and a whole number t >= 0'; the solution uses Remark 1.3 of L04 with m = 1 (L04.html:69-70) and A2 with induction for whole t, so the scope is the stated one.")
row("M1-b-r5-keyresults-basis-L04", "basis text in key results and references, L04", "course/modules/M/M1/L04.html:372-384 (key results), 459-462 (references paragraph)", "PASS",
    "Key-result rows cite the in-page proofs (Prop 2.1 'from the binomial theorem'; Prop 2.2 'from Assumption E, A2 of L03, and the power fact'; R3 'from A1 and A2 of L03, Assumption E, and the strict monotonicity') and match the proofs read above. References paragraph calls E an assumption that the page does not derive.")
row("M1-b-r5-keyresults-basis-L05", "basis text in key results, L05", "course/modules/M/M1/L05.html:385-396 (key results), 472-475 (references)", "PASS",
    "Rows for Props 1.4, 2.1, 2.2, 2.4 cite Assumption E, A1, A2, L03 Props 1.3, 1.4, 1.6(a) and the convention of §1; each matches the proof read above. Prop 2.1 is 'checked in Lab 1' (a check, not the basis).")
row("M1-b-r6-checked-in-lab-L05", "lab-claim: 'checked in Lab 1' and 'illustrated by' phrases, L05", "course/modules/M/M1/L05.html:388-396 (key results); tests/labs/M1/lab-M1-L05-1.py", "PASS",
    "Prop 2.1 'checked in Lab 1': lab prints equivalent_continuous equal to annual in every row (max gap 0.0000000000). Props 2.2 and 2.4 'illustrated by the printed columns': the lab's printed continuous and semiannual columns are below annual in all five rows. No row claims the lab proves the propositions.")
row("M1-b-r6-refs-named-in-each-proof-L05", "attribution: L03 propositions named in each L05 proof", "course/modules/M/M1/L05.html:473 (references paragraph); proofs at 87-100, 106-137", "PASS",
    "Prop 1.4 names L03 Props 1.3, 1.4, 1.6(a) (all re-read in L03, see M1-b-r3-attr-L04-L05); Props 2.2 and 2.4 name E, A1, A2 and L03 Prop 1.4 as stated. No L03 item is cited that the page does not use.")
row("M1-b-r7-L04-218-interpretation", "2.2 numbers, L04 interpretation paragraph", "course/modules/M/M1/L04.html:218 (interpretation)", "PASS",
    "Monthly 0.0511618979 vs annual 0.0500000000; Part C cents 1,628,895 / 1,647,009 / 1,648,665 / 1,648,721; monthly adds 18,114 (181.14 CU) and unrounded 18,114.87; continuous adds 56 over daily, unrounded 56.46 (" + CMD + "recompute_l04_l05.out).")
row("M1-b-r7-L04-244-periodic", "scope: canon-breaks item 'Periods that do not fit the horizon'", "course/modules/M/M1/L04.html:244 (canon-breaks, 'Periods that do not fit the horizon')", "PASS",
    "States that Remark 1.3 applies when mt is a whole number, that the non-whole case is not defined here, and that Lab 1 uses whole years. Matches Remark 1.3 (L04.html:69-70) and Lab 1 code (PERIODS integer, years = 1 or 10).")
row("M1-b-r7-L04-257-340-cent-basis", "2.2 numbers, L04 misconception 2 and E3 cent basis", "course/modules/M/M1/L04.html:255-257 (misconception 2), 336-340 (E3 solution)", "PASS",
    "Printed whole-cent differences 18,114 and 56; E3 uses 1648665 - 1647009 = 1656 and 1648721 - 1648665 = 56; unrounded gaps 1,655.32 and 56.46; ratio 1656/56 = 29.57 (printed) and 29.32 (unrounded) (" + CMD + "recompute_l04_l05.out).")
row("M1-b-r7-L04-378-380-460-basis-text", "attribution: key-result basis and references text, L04", "course/modules/M/M1/L04.html:378, 380 (rows for Prop 2.2 and R3), 460 (references paragraph)", "PASS",
    "Row 378 (Prop 2.2) and row 380 (R3) name only the in-page proofs and L03 items; line 460 states the lesson cites no outside source and that Lab 1 checks formulas numerically. Matches the proofs read this round.")
row("M1-b-r7-L05-98-remark15", "2.4 mathematics, L05 Remark 1.5", "course/modules/M/M1/L05.html:97-99 (Remark 1.5)", "PASS",
    "For -1 < r < 0: 0 < 1 + r < 1, ln(1 + r) < 0, exponent -t ln(1+r) > 0 for t > 0, factor > 1 by (i), increasing in t by (ii). 'Both of its claims reverse' matches Prop 1.4 (factor in (0,1) and decreasing) (re-derived).")
row("M1-b-r7-L05-254-339-346-gaps", "2.2 numbers, L05 canon-breaks and E1, E2 gap statements", "course/modules/M/M1/L05.html:254 (canon-breaks), 335-341 (E1), 342-348 (E2)", "PASS",
    "254: semiannual and continuous differ by 2,397 cents (printed) and 2,397.62 (unrounded). E1: 23.97 CU. E2: 0.9759000729 - 0.9756097561 = 0.0002903168 (printed), 0.00029031685 unrounded, 0.0002903169 to ten places (" + CMD + "recompute_l04_l05.out).")
row("M1-b-2.7-cards", "2.7 cards of the slice (L04, L05), full duplicate scan", "course/modules/M/M1/cards.json: all 178 cards; L04 cards M1-c064..c077, c144, c163, c176; L05 cards M1-c077..c092, c145, c152, c160, c177", "PASS",
    "Full scan (" + CMD + "cards_scan.py, cards_scan.out): 178 cards, 0 duplicate ids, 0 duplicate fronts, 0 grade/basis inconsistencies. The two round-17 defects are fixed (rows M1-b-r17-2.7-cards-c163-scope and M1-b-r17-2.7-cards-c160-scope). Every L04 and L05 card re-checked against the page text this round.")
row("M1-b-r17-2.7-cards-c163-scope", "2.7 cards: scope of M1-c163 (re-verified from scratch)", "course/modules/M/M1/cards.json M1-c163; L04.html:361-367 (R3 statement and solution)", "PASS",
    "Front now reads 'For r > 0 and whole m >= 1, with 1 + r_m/m > 0, is the nominal rate r_m whose one-year factor is e^r above r?'. Back: 'Yes, r_m > r under Assumption E (Problem R3). The condition 1 + r_m/m > 0 is needed, since for even m the root -e^(r/m) gives a negative r_m.' R3 (L04.html:361-367) states the hypothesis and gives the even-m root. Witness m = 2, r = 0.05: r_2 = -4.050627, (1 + r_2/2)^2 = e^0.05 = 1.0512710964, r_2 > r False, so the condition is needed in that case. Positive root gives r_m > r by e^x - 1 > x (E). Card now agrees with M1-c072, which keeps the hypothesis.")
row("M1-b-r17-2.7-cards-c160-scope", "2.7 cards: answer scope of M1-c160 (re-verified from scratch)", "course/modules/M/M1/cards.json M1-c160; L05.html:79-84 (Assumption E block); propositions 1.4 (87), 2.2 (116), 2.4 (131)", "PASS",
    "Front: 'In Lesson 5, is the exponential bound 1 + x < e^x for x > 0 derived in that lesson?'. Back: 'No. The page takes it as Assumption E and does not derive it from L03's A1 to A3. Propositions 1.4, 2.2 and 2.4 assume it.' L05.html:79-80 says 'this lesson does not derive E from them. E is taken here as an assumption of this page'; Props 1.4 (line 87), 2.2 (116) and 2.4 (131) each open 'Assume E'. The headline now claims only what the page says about this lesson.")
row("M1-b-r18-delta-L04-why", "round-18 change: L04 why-it-matters sentence ('compounding factors that L05 uses')", "course/modules/M/M1/L04.html:52", "PASS",
    "New text: 'This lesson fixes the compounding factors that L05 uses: the periodic factor, the effective annual rate, and the continuous factor e^(rt), each defined in §1.' L05 uses the periodic factor as (1+r/m)^(-mt) (L05.html:64-70, Def 1.1), the annual effective rate r in (1+r)^(-t) (Def 1.1; L05 Uses row line 38 names the effective annual rate), and e^(-rt) (Def 1.1). Each factor is defined in L04 §1 (Defs 1.1-1.2). Claim supported.")
row("M1-b-r18-delta-L05-why", "round-18 change: L05 why-it-matters and meta description, 't > 0' scope of the between-zero-and-one claim", "course/modules/M/M1/L05.html:52 (why-it-matters) and L05.html:7 (meta description)", "FAIL",
    "The rewritten sentence changed only 'the program needs' to 'a valuation needs' (no defect). The unchanged sentence on the same paragraph says 'the factor lies between zero and one for a positive rate'. Proposition 1.4 (L05.html:87-89) and card M1-c083 require t > 0, and the discount factor at t = 0 equals 1 (quiz L05q7, L05.html:452: 'the annual factor is (1+r)^0 = 1'). The same omission is in the meta description (line 7: 'why it lies between zero and one for a positive rate'). Witness: r = 0.05, t = 0, DF = 1, not strictly between zero and one.",
    "Replace 'for a positive rate' with 'for a positive rate and a positive time' in the why-it-matters (L05.html:52) and in the meta description (L05.html:7); rebuild the generated site data with tools/build_site.py (meta description is generated into course/index.html only if it reads from the page: check before editing).")
row("M1-b-r18-cards-scan", "2.7 full card scan after round-18 edits (M1 cards)", "course/modules/M/M1/cards.json (178 cards); removed M1-c175 (L03, outside this slice)", "PASS",
    "cards_scan.py: 178 cards, 0 duplicate ids, 0 duplicate fronts, grade/basis consistent for all cards (86 T, 41 C, 51 with no grade). Lessons present: L01-L08. Removal of M1-c175 (L03 'ln(1/y)') and edit of M1-c060 (L03) are outside this slice and were not judged here.")
row("M1-b-r18-cards-unchanged-L04-L05", "2.7 cards unchanged this round (M1-c067, c072, c083, c176, c177) re-checked", "course/modules/M/M1/cards.json: M1-c067, c072, c083, c176, c177; L04.html:64 (Def 1.2), 361-367 (R3); L05.html:87-89 (Prop 1.4)", "PASS",
    "c067 e^(rt) = Def 1.2 (L04.html:64); c072 r_m = m(e^(r/m)-1) with 1 + r_m/m > 0 = R3 (L04.html:361-367); c083 strictly between 0 and 1 for r > 0, t > 0 = Prop 1.4; c176 e^r - 1 = Def 1.2 (L04.html:64); c177 strictly decreasing for t >= 0 = Prop 1.4 (L05.html:87-89, 'strictly decreasing for t >= 0'). Byte-identical since the previous pin; re-read this round, not carried.")
row("M1-b-r18-L03-items-cited", "round-18 check: L03 text edits do not change items cited by L04 and L05", "course/modules/M/M1/L03.html:56-62, 72-74, 82-88, 92-100, 112-118 (cited items); L03 edits in this round: lines changed in the why-it-matters, Assumption text and the Lab 1 interpretation", "PASS",
    "git diff fefbf8b 7143726 on L03.html changed prose (why-it-matters, the 'every proposition' sentence, a lab interpretation, the product-rule sentence). Propositions 1.2, 1.3, 1.4, 1.6, A1-A3 keep their numbers and statements; every use in L04 and L05 (A1, A2, Prop 1.2, 1.3, 1.4, 1.6(a)) still matches.")
row("M1-b-r18-embed-twins", "lab twins and embedded code unchanged; expected blocks match output", "tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py; course/modules/M/M1/L04.html:116-190, L05.html:141-222", "PASS",
    "git diff fefbf8b 7143726 shows no change to tests/labs/M1; run_labs M1 PASS (11/11) confirms the embedded code and the expected blocks agree with the twins (" + CMD + "run_labs_M1.out).")

fragment = {
    "unit": "M1",
    "slice": "M1-b",
    "round": 18,
    "verifier": "independent verifier (Haiku), round 18",
    "pin": "7143726",
    "base": "fefbf8b (round 17 pin; delta re-read)",
    "previous_fragment": "/tmp/fanout-frags/M1-b.round17.json",
    "checkout": "/tmp/verify18-M1-b",
    "scratch": "/tmp/M1-v/M1-b-r18",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta fefbf8b..7143726 for this slice: L04.html line 52 and L05.html line 52 (why-it-matters, one sentence each); cards.json entries M1-c160 and M1-c163 changed (the two round-17 defects), M1-c060 (L03), M1-c175 (L03) removed. Every L04/L05 row was re-verified this round from the current pages; none is carried, because L04.html and L05.html are not byte-identical to the previous pin.",
        "Previous non-PASS rows re-verified from scratch: M1-b-2.7-cards, M1-b-r17-2.7-cards-c163-scope, M1-b-r17-2.7-cards-c160-scope now PASS (fixes checked against the page text and the R3 witness).",
        "New round-18 failure: M1-b-r18-delta-L05-why (missing 't > 0' in a sentence on the rewritten paragraph, also in the meta description). Fix named in the row.",
        "Mutants: none required. Slice b is lessons L04 and L05 with their twins, not a project slice (same ruling as rounds 16 and 17); the three new student-error mutants and the alternative-implementation check apply to project slices only. ledgers/M1/mutants/ holds the project mutants, which belong to slice a/c.",
        "Hours: arithmetic only (70 = sum of the eight lesson data-hours). Pace not judged (architect ruling).",
        "Not checked: the M1 registry was re-verified live for one entry only (tool output '1 of 560 entries'); L04 and L05 cite no registry key, so the live sample is not evidence for these pages. No external source (SEC, Springer, etc.) is read or cited in this slice. Project.html, the grader and L01-L03, L06-L08 are outside this slice except where L03 text is cited.",
    ],
    "summary": {},
}
fragment["summary"] = {
    "rows": len(R),
    "pass": sum(r["status"] == "PASS" for r in R),
    "fail": sum(r["status"] == "FAIL" for r in R),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in R),
}
out = sys.argv[2]
json.dump(fragment, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out, fragment["summary"], fragment["verdict"])
