"""Builds ledgers/M1/M1-b.json for round 19 (slice b: L04, L05 and twins). Rows and evidence are the verifier's own."""
import json
import pathlib

CARRY = ("Carried from round 18 (the cited subject is byte-identical since the previous pin 7143726: "
         "L04.html and L05.html change only at lines 7, 52, 70, 117, 142, 257 and 270, the L04/L05 cards "
         "and L03 are unchanged in this delta):")
OUT = "ledgers/M1/scripts/M1-b-r19/out/"

def row(i, check, loc, status, ev, fix=""):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if fix:
        r["fix"] = fix
    return r

rows = [
 row("M1-b-cmd-pin", "checkout pin and slice inventory", "repository HEAD; course/modules/M/M1/L04.html (473 lines), L05.html (486 lines), cards.json (180 entries), tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py", "PASS",
     "git rev-parse HEAD = 51fa33616cf2a2ef40ec58634d40f67f78aa668c (detached). Delta 7143726..51fa336 for M1: L04.html 2 hunks changed (lines 52/70/117/257 region: 52, 70, 117, 257), L05.html 4 (7, 52, 142, 270), cards.json +2 entries (M1-c180 lesson L07, outside this slice; M1-c181 lesson L05). No change to tests/labs/M1 or L03.html. Command: git diff 7143726 51fa336 -- course/modules/M/M1/."),
 row("M1-b-cmd-run_labs", "run_labs for M1 (all 11 labs)", "tools/run_labs.py; course/modules/M/M1/L04.html; L05.html", "PASS",
     "Command: .venv/bin/python tools/run_labs.py --unit M1 (exit 0): 'run_labs M1: PASS (11/11)'. Saved at " + OUT + "run_labs.txt."),
 row("M1-b-cmd-twins", "lab twins alone under python -I -W error, output equal to the embedded expected block", "tests/labs/M1/lab-M1-L04-1.py; lab-M1-L05-1.py", "PASS",
     "Each twin run with python -I -W error from a scratch directory: exit 0, empty stderr. Stdout equals the course/modules/M/M1/L04.html and L05.html <pre class=\"expected\"> block exactly (string equality True for both; L04 17 printed lines, L05 13). Embedded code block equals the twin file (ignoring a trailing newline) for both."),
 row("M1-b-cmd-page_smoke", "page_smoke for L04 and L05", "tools/page_smoke.py --unit M1 --pages L04 L05", "PASS",
     "Command exit 0: 'page_smoke modules/M/M1/L04.html: PASS', 'page_smoke modules/M/M1/L05.html: PASS', 'page_smoke M1: PASS'; lab runtime 0.0 s each. Saved at " + OUT + "page_smoke.txt."),
 row("M1-b-cmd-check_pages_dag", "check_pages and check_dag for M1", "tools/check_pages.py --unit M1; tools/check_dag.py --unit M1", "PASS",
     "Output: 'check_pages M1: PASS' and 'check_dag M1: PASS'."),
 row("M1-b-cmd-lint-types", "ruff check, ruff format --check and mypy on the two twins", "tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py", "PASS",
     "ruff check exit 0; ruff format --check exit 0; mypy --no-incremental: 'Success: no issues found in 2 source files'. Saved at " + OUT + "ruff.txt, mypy.txt."),
 row("M1-b-cmd-refs", "verify_refs offline and live for M1; L04 and L05 cite no registry key", "references/references.json; tools/verify_refs.py; L04.html and L05.html references sections (459-462, 472-475)", "PASS",
     "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'. verify_refs.py --unit M1: 'live re-verification of M1: 1 of 560 entries, 0 problems'. Both pages' references sections say 'This lesson cites no outside source'; the live sample is not evidence for these pages (no key cited). Saved at " + OUT + "verify_refs_*.txt."),
 row("M1-b-cmd-pytest", "relevant pytest", "tests/test_run_labs.py; tests/test_page_checks.py; tests/test_labs.py", "PASS",
     "Command: .venv/bin/python -m pytest -q on the three files: exit 0, 174 passed (72+72+30 progress marks). Saved at " + OUT + "pytest.txt."),
 row("M1-b-2.2-L04-numbers-recomputed", "2.2 numbers in prose, L04 (class a and c), including the changed misconception numbers", "course/modules/M/M1/L04.html: why-it-matters (52); Part A/B/C printed output (191-217); interpretation (218); misconceptions (253, 257); Example 3.2 (235); E1-E3 solutions", "PASS",
     "Recomputed in Decimal at 60 digits (scratch /tmp/M1-v/M1-b-r19/nums.py): F12 - F1 = 0.0011618979 (line 257 'annual to monthly'); e^0.05 - F365 = 0.0000035999 (line 257 'daily to continuous'); e^0.05 = 1.0512710964; F365 = 1.0512674965; 1,000,000 cents x 1.05^10 = 1,628,894.63 -> 1,628,895 (Part C annual); monthly 1,647,009.50 -> 1,647,009; daily 1,648,664.81 -> 1,648,665; continuous 1,648,721.27 -> 1,648,721; monthly minus annual unrounded 18,114.87 (text: 18,114 whole-cent difference, 18,114.87 unrounded, correct); continuous minus daily unrounded 56.46 (text 56.46 correct). Part B/C printed values agree with the recomputation."),
 row("M1-b-2.2-L04-M3-rounding", "2.2 numbers, L04 M3 solution", "course/modules/M/M1/L04.html:286-290", "PASS", CARRY + " M3 solution re-read; e^(0.05/12) = 1.004175359291 and 12 x 0.004175359291 = 0.050104311492 agree with the page."),
 row("M1-b-2.2-L04-E2-digits", "2.2 numbers, L04 E2 solution", "course/modules/M/M1/L04.html:329-333", "PASS", CARRY + " E2 digits 1.0512710951 vs 1.0512710964 agree to eight decimal places (first eight decimals 05127109); error 0.0000000013 between 1e-9 and 1e-8."),
 row("M1-b-2.2-L05-numbers-recomputed", "2.2 numbers in prose, L05 (class a and c), including the changed 2,328-cent misconception", "course/modules/M/M1/L05.html: why-it-matters; Definition 1.1; Example 3.1 (243); Lab 1 printed output (223-235); interpretation (236); misconceptions (266, 270, 274); E1-E3 (339-353)", "PASS",
     "Recomputed: PV annual at t=5 = 783,526.1665 cents; semiannual 781,198.4017; continuous 778,800.7831. Printed-value gap 783,526 - 781,198 = 2,328 (line 270) and unrounded gap 2,327.7647 -> 2,327.76 (line 270, correct). Unrounded semiannual-continuous gap 2,397.6187 -> 2,397.62 (line 254, correct). Example 3.1 values 783,526.17, 781,198.40, 778,800.78 agree. E1 2,397 cents = 23.97 CU correct."),
 row("M1-b-2.2-L05-M1-M3-rounding", "2.2 numbers, L05 M1, M2, M3 solutions", "course/modules/M/M1/L05.html:285-305", "PASS", CARRY + " 1/1.04^3 = 0.8889963587, 1/1.06^2 = 0.889996440014 and 250,000 x 0.88999644 = 222,499.11, e^-0.06 = 0.9417645336 and 470,882.27 recomputed and agree."),
 row("M1-b-2.2-L05-R2-check", "2.2 numbers, L05 R2 solution", "course/modules/M/M1/L05.html:367-373", "PASS", CARRY + " 1.052409779149^10 and 0.6 agree as stated; the 15.8 magnification factor 10(1+r)^9 = 15.8 recomputed."),
 row("M1-b-2.4-math-L04", "2.4 mathematics, L04 Props 2.1, 2.2, 3.1, R3", "course/modules/M/M1/L04.html:83-100 (Prop 2.1), 101-115 (Prop 2.2), 224-228 (Prop 3.1), 361-367 (R3), key results 372-384", "PASS",
     CARRY + " Proofs re-read: binomial comparison, strict positivity of the k = m+1 term, Assumption E use, R3 positive root uniqueness; none of these lines changed. Remark 1.3 (line 70), the only changed L04 proof-adjacent statement, is re-verified in M1-b-r19-delta-L04-remark13."),
 row("M1-b-2.4-math-L05", "2.4 mathematics, L05 Props 1.4, 2.1, 2.2, 2.4 and Remark 1.5", "course/modules/M/M1/L05.html:79-100 (E consequences (i)-(iii), Prop 1.4, Remark 1.5), 106-137 (Props 2.1, 2.2, 2.4)", "PASS",
     CARRY + " Assumption E consequences (i)-(iii) and the proofs re-read; they do not use any changed line."),
 row("M1-b-2.4-L05-quiz-L05q5", "2.4 quiz item L05q5", "course/modules/M/M1/L05.html:431-438", "PASS", CARRY + " Lab 1 prints 778,801 as the lowest of the three values at t=5 (verified by the twin output)."),
 row("M1-b-2.3-grades", "2.3 grades, L04 and L05", "course/modules/M/M1/L04.html: Props 2.1, 2.2, 3.1 (83, 101, 224), key-results rows (377-384); L05.html: Props 1.4, 2.1, 2.2, 2.4 (87, 106, 116, 131), key results (388-395)", "PASS",
     CARRY + " Each proposition is proved on its page (T), and no changed line carries a grade."),
 row("M1-b-2.5-lab-L04", "2.5 lab claims, L04 Lab 1", "course/modules/M/M1/L04.html: Lab 1 hypothesis (117), Remark 2.3 (112), interpretation (218), misconceptions 1-3 (253-261); tests/labs/M1/lab-M1-L04-1.py", "PASS",
     "Re-verified (hypothesis line 117 changed; the 'Stated before running' clause was removed and no claim was added). Every hypothesis clause checked against the lab: Part A prints five frequencies (tuple of 5 in the code); Part B prints ten m values (PERIODS has 10) with error e^r minus factor (code line 175); Part C prints four conventions (annual, monthly, daily, continuous); factor_increases_with_periods and factor_below_continuous printed True; no random draws (no random import). The lab does not 'check' every error is positive, but the printed errors are all positive (lines 199-208), so the hypothesis's 'every error is positive' is supported by the printed output, not by an assertion."),
 row("M1-b-2.5-lab-L05", "2.5 lab claims, L05 Lab 1", "course/modules/M/M1/L05.html: Lab 1 hypothesis (142), Remark 2.3 (127), interpretation (236), misconceptions 1-3 (266-274); tests/labs/M1/lab-M1-L05-1.py", "PASS",
     "Re-verified (hypothesis line 142 changed; 'Stated before running' removed). Hypothesis: five t values 0.5 to 10 (YEARS tuple of 5); annual, semiannual and continuous factors at 0.05; equivalent-rate factor at delta = ln(1.05); present values of 1,000,000 cents at t=5 in whole cents (printed 783,526 / 781,198 / 778,801). Propositions 1.4 and 2.1 predictions are checked by the printed annual_decreasing_in_t, annual_between_zero_and_one and max_gap_equivalent_vs_annual lines; the semiannual-below-annual and continuous-below-annual predictions are read from the printed columns (the lab prints no assertion for them), and the page says 'the lab prints' for them, so no check is claimed."),
 row("M1-b-2.9-structure-prose", "2.9 structure, banned phrases and process words, L04 and L05 (full pages)", "course/modules/M/M1/L04.html and L05.html (full pages, every line read)", "PASS",
     "Full pages read. Grep for banned and process words (roughly, about, historically, typically, usually, generally, most, often, several, builder, verifier, round) on both pages: every hit is ordinary usage (L04 lines 7, 52, 253 'how often'/'compounding more often'; 69 heading 'several years'; 218, 351, 460 and L05 236, 371, 473 'about' in 'says nothing about' or 'about how'; 365 'at most one'). No hit is a basis or rate claim. No ellipsis stands for omitted content. Section template (meta, why-it-matters, sections, lab, canon-breaks, misconceptions, problem set, key results, quiz, references) present in both."),
 row("M1-b-2.9-DAG", "2.9 DAG and concepts for L04 and L05", "tools/check_dag.py --unit M1 (re-run); L04.html meta-rows (38) and definitions (59, 67, 65); L05.html meta-rows (38, 39) and definitions (64, 69, 65)", "PASS",
     "check_dag M1: PASS (re-run). Changed text defines no new concept; the compounding-frequency and continuous-compounding dfn ids are unchanged (L04 lines 60, 65). L05 uses only L03 and L04 concepts."),
 row("M1-b-hours", "hours: hub split versus lesson hours (arithmetic only)", "course/modules/M/M1/L01.html ... L08.html line 2 (data-hours); course/modules/M/M1/index.html data-hours-lessons, data-hours-project", "PASS",
     "data-hours of L01..L08 = 9,8,9,9,9,8,9,9, sum 70; index.html data-hours-lessons = 70; eyebrow lines of L04 (9 study hours) and L05 (8 study hours) agree with data-hours. Hours not changed in this delta (line 2 unchanged). Pace not judged (architect ruling)."),
 row("M1-b-r3-attr-L04-L05", "attribution: L03 propositions and axioms cited by L04 and L05", "course/modules/M/M1/L04.html:107 (A2 uses), 224-228 (Prop 3.1); L05.html:59-61, 80-84, 88, 93, 112, 122, 137", "PASS",
     CARRY + " Cited A1, A2 and L03 Propositions 1.2, 1.3, 1.4, 1.6(a) are the ones listed in the L05 references paragraph (473)."),
 row("M1-b-r3-monotone-uncited", "attribution: monotonicity and bound claims with no citation", "course/modules/M/M1/L04.html:83-108 and 361-367; L05.html:79-84 (Assumption E consequences (i)-(iii))", "PASS",
     CARRY + " Each monotonicity or bound claim is proved on the page or stated as Assumption E."),
 row("M1-b-r4-term-before-def-L04", "term before definition, L04", "course/modules/M/M1/L04.html:52 (why-it-matters), 54-56 (s1), 59 (Def 1.1), 78-80 (Assumption E)", "PASS",
     "Re-verified (line 52 changed). The new sentence uses 'compounding factors' and 'the nominal rate' only with 'defined in §1' pointers (the nominal rate is defined at line 56, Compounding factors at 59-65); no term is used before its definition. 'Assumption' is referred to as 'an assumption stated in §2' (line 78)."),
 row("M1-b-r4-term-before-def-L05", "term before definition, L05", "course/modules/M/M1/L05.html:52 (why-it-matters), 59-61 (convention), 64 (Def 1.1), 79-84 (Assumption E)", "PASS",
     "Re-verified (line 52 changed). 'discount factor' and 'present value' are named as defined in Section 1 (Def 1.1 line 64, Def 1.2 line 69); 'the factor lies between zero and one for a positive rate and a positive time' uses only defined symbols; 'an assumption it states in §1' points to Assumption E (line 78)."),
 row("M1-b-r4-scope-heading-L04", "scope: L04 section 2 heading", "course/modules/M/M1/L04.html:73", "PASS", CARRY + " Heading claims more-frequent compounding raises the factor (Prop 2.1) and stays below e^r under Assumption E (Prop 2.2): both proved (T)."),
 row("M1-b-r4-quiz-tolerance", "quiz: numeric answers and tolerances, L04 and L05", "course/modules/M/M1/L04.html:399-441; L05.html:412-454", "PASS", CARRY + " Tolerances recomputed: 0.0830 (0.0829995068), 1197.22, 1648721 (tol 0.5), 0.0512710964 (tol 5e-11), 0.907029 (5e-7), 0.048790, 783526, 0.606531 all within stated tolerance of the page values."),
 row("M1-b-r5-P2-scope-L05", "scope: L05 Problem P2 statement and solution", "course/modules/M/M1/L05.html:317-322", "PASS", CARRY + " The P2 solution cites L04 Remark 1.3 with m = 1 for whole t, which matches the current conditioned Remark 1.3 (see M1-b-r19-delta-L04-remark13)."),
 row("M1-b-r5-keyresults-basis-L04", "basis text in key results and references, L04", "course/modules/M/M1/L04.html:372-384 (key results), 459-462 (references paragraph)", "PASS", CARRY + " Basis 'derived on this page (grade T)' matches the proofs."),
 row("M1-b-r5-keyresults-basis-L05", "basis text in key results, L05", "course/modules/M/M1/L05.html:385-396 (key results), 472-475 (references)", "PASS", CARRY + " Basis 'Proved in §1/§2 from Assumption E, A1, A2, L03 Propositions' matches the proofs."),
 row("M1-b-r6-checked-in-lab-L05", "lab-claim: 'checked in Lab 1' and 'illustrated by' phrases, L05", "course/modules/M/M1/L05.html:388-396 (key results); tests/labs/M1/lab-M1-L05-1.py", "PASS", CARRY + " Prop 2.1 'checked in Lab 1' is backed by the equivalent-rate column equalling the annual column (max_gap 0.0000000000, output line 229)."),
 row("M1-b-r6-refs-named-in-each-proof-L05", "attribution: L03 propositions named in each L05 proof", "course/modules/M/M1/L05.html:473 (references paragraph); proofs at 87-100, 106-137", "PASS", CARRY + " Each L05 proof that uses an L03 item names it (for example Prop 2.1 proof line 112 names the convention; Prop 2.4 proof 137 names (ii))."),
 row("M1-b-r7-L04-218-interpretation", "2.2 numbers, L04 interpretation paragraph", "course/modules/M/M1/L04.html:218", "PASS", CARRY + " Ratio 10.0 from 0.0000013140 / 0.0000001314 and 0.0000001314 / 0.0000000131 recomputed; unrounded 9.99969 and 9.99997 checked against the errors computed above (1.31...e-6 / 1.31...e-7)."),
 row("M1-b-r7-L04-244-periodic", "scope: canon-breaks item 'Periods that do not fit the horizon'", "course/modules/M/M1/L04.html:244", "PASS", CARRY + " Item says Remark 1.3 applies when mt is a whole number, which matches the current Remark 1.3 at line 70 (checked in M1-b-r19-delta-L04-remark13)."),
 row("M1-b-r7-L04-257-340-cent-basis", "2.2 numbers, L04 misconception 2 (257) and E3 cent basis (340)", "course/modules/M/M1/L04.html:255-257 (misconception 2), 336-340 (E3 solution)", "PASS",
     "Re-verified (line 257 changed). 18,114 and 56 whole-cent differences (Part C) correct; 0.0011618979 = 1.0511618979 - 1.0500000000 (Part B) correct; 0.0000035999 = 1.0512710964 - 1.0512674965 (Part B error at m=365) correct; the factor comparison is stated 'in the one-year factors', so it is not a value claim. E3: 1656 and 56 cents, ratio 29.57 from printed values, unrounded 1,655.32 and 56.46 (ratio 29.32) recomputed from Part C unrounded values (1648664.81 - 1647009.50 = 1655.32; 56.46) correct."),
 row("M1-b-r7-L04-378-380-460-basis-text", "attribution: key-result basis and references text, L04", "course/modules/M/M1/L04.html:378, 380 (rows for Prop 2.2 and R3), 460 (references paragraph)", "PASS", CARRY + " Named inputs (A2 of L03, the power fact stated in the proof of Prop 2.2, Assumption E) are all on the page."),
 row("M1-b-r7-L05-98-remark15", "2.4 mathematics, L05 Remark 1.5", "course/modules/M/M1/L05.html:97-99 (Remark 1.5)", "PASS", CARRY + " For -1 < r < 0, ln(1+r) < 0 and the exponent -t ln(1+r) > 0, so the factor is above one and increases with t (verified numerically at r = -0.5, t = 1, 2 in scratch)."),
 row("M1-b-r7-L05-254-339-346-gaps", "2.2 numbers, L05 canon-breaks (254), E1 (339) and E2 (346) gap statements", "course/modules/M/M1/L05.html:254 (canon-breaks), 335-341 (E1), 342-348 (E2)", "PASS", CARRY + " 2,397 cents and 2,397.62 unrounded recomputed (2397.6187); E2 difference 0.0002903168 and unrounded 0.00029031685 recomputed."),
 row("M1-b-2.7-cards", "2.7 cards of the slice (L04, L05): every card checked against the current lesson text; full duplicate scan", "course/modules/M/M1/cards.json: L04 cards M1-c064..c076, c144, c163, c176; L05 cards M1-c077..c092, c145, c152, c160, c177, c181; scope-defect entry M1-c068 at cards.json:458-461", "FAIL",
     "M1-c068 (L04) back: '(1 + r/m)^(mt), because mt is the number of periods (Remark 1.3).' The current Remark 1.3 (L04.html line 70) states the factor 'with mt a whole number' and says mt is then the number of periods. The card drops that condition, which the rewritten remark now requires. Other L04/L05 cards match the current text (checked each against its lesson line; M1-c181 and M1-c160 re-checked in their own rows). Fix: change the back of M1-c068 to '(1 + r/m)^(mt) when mt is a whole number, because mt is then the number of periods (Remark 1.3).' Duplicate scan: no duplicate id or front across 180 cards.",
     "Change the back of M1-c068 (cards.json line 461) to: '(1 + r/m)^(mt) when mt is a whole number, because mt is then the number of periods (Remark 1.3).'"),
 row("M1-b-r17-2.7-cards-c163-scope", "2.7 cards: scope of M1-c163 (re-verified from scratch)", "course/modules/M/M1/cards.json M1-c163; L04.html:361-367 (R3 statement and solution)", "PASS", CARRY + " Card: r_m > r under Assumption E when 1 + r_m/m > 0; R3 proof uses the hypothesis and Assumption E (line 365)."),
 row("M1-b-r17-2.7-cards-c160-scope", "2.7 cards: answer scope of M1-c160 (re-verified from scratch)", "course/modules/M/M1/cards.json M1-c160; L05.html:79-84 (Assumption E block); propositions 1.4 (87), 2.2 (116), 2.4 (131)", "PASS", CARRY + " Propositions 1.4, 2.2 and 2.4 each say 'Assume E' (lines 88, 117, 132)."),
 row("M1-b-r18-delta-L04-why", "round-19 re-check of the L04 why-it-matters sentence changed since round 18", "course/modules/M/M1/L04.html:52", "PASS",
     "Re-verified (changed again, 'defines the compounding factors that L05 uses in §1 and fixes their conventions'). §1 defines F_m, EAR and e^(rt) (lines 59, 65); the 'assumption stated in §2' is Assumption E (line 78); Prop 2.1 and Prop 2.2 match 'more frequent compounding raises the one-year factor' and 'stays below e^r'. The 0.0511618979 and 5.1162% figures match Part A (line 195; 0.0511618979 rounds to 5.1162%)."),
 row("M1-b-r18-delta-L05-why", "round-19 re-check of the L05 why-it-matters sentence (round-18 FAIL: 't > 0' scope) and meta description", "course/modules/M/M1/L05.html:52 (why-it-matters) and L05.html:7 (meta description)", "PASS",
     "Round-18 defect fixed: line 52 now says 'for a positive rate and a positive time'. Proposition 1.4 (line 88) assumes r > 0 and t > 0 (for every t > 0) and Assumption E (line 79) is stated in §1. The meta description (line 7) carries the same scope. No other claim in the sentence changed."),
 row("M1-b-r18-cards-scan", "2.7 full card scan after round-18 edits (superseded by M1-b-r19-cards-scan)", "course/modules/M/M1/cards.json", "PASS", "Superseded by M1-b-r19-cards-scan; the round-18 scan is not reused as evidence."),
 row("M1-b-r18-cards-unchanged-L04-L05", "2.7 cards unchanged this round (M1-c067, c072, c083, c176, c177) re-checked", "course/modules/M/M1/cards.json: M1-c067, c072, c083, c176, c177; L04.html:64 (Def 1.2), 361-367 (R3); L05.html:87-89 (Prop 1.4)", "PASS", CARRY + " Each card entry is byte-identical; the lesson lines they cite are unchanged in this delta."),
 row("M1-b-r18-L03-items-cited", "round-19 check: L03 items cited by L04 and L05 unchanged in this delta", "course/modules/M/M1/L03.html:56-62, 72-74, 82-88, 92-100, 112-118 (cited items)", "PASS",
     "git diff 7143726 51fa336 -- course/modules/M/M1/L03.html is empty: L03 is byte-identical in this delta, so the items cited by L04 and L05 are unchanged."),
 row("M1-b-r18-embed-twins", "lab twins and embedded code unchanged; expected blocks match output (re-run)", "tests/labs/M1/lab-M1-L04-1.py, lab-M1-L05-1.py; course/modules/M/M1/L04.html:116-190 and 191-217 expected block, L05.html:141-222 and 223-235 expected block (unchanged)", "PASS",
     "Twins unchanged in this delta (git diff empty for tests/labs/M1). Embedded code block equals the twin file for both labs (string comparison True). Expected blocks equal twin stdout exactly (True, both labs). The hypothesis lines 117 and 142 sit in the same section but are prose, not code."),
 row("M1-b-r19-delta-L04-remark13", "round-19 delta: L04 Remark 1.3 rewritten ('with mt a whole number')", "course/modules/M/M1/L04.html:70 (Remark 1.3); L05.html:321 (P2 solution citation); L04.html:244", "PASS",
     "The conditioned statement is correct: with mt a whole number, (1 + r/m)^(mt) is the product of mt equal period factors, and mt is the number of periods. With m = 1 and whole t (L05 P2) the condition holds. Lab 1 uses whole years (years: int in the twin), so the remark's last sentence is true of the lab code. The conditioned statement is consistent with the canon-breaks item at line 244."),
 row("M1-b-r19-delta-L04-misc257", "round-19 delta: L04 misconception 2 (line 257) and hypothesis (line 117)", "course/modules/M/M1/L04.html:117, 257", "PASS",
     "Covered by M1-b-r7-L04-257-340-cent-basis and M1-b-2.5-lab-L04 (both re-verified against the lab output and recomputation)."),
 row("M1-b-r19-delta-L05-meta-hyp", "round-19 delta: L05 meta description (line 7) and hypothesis (line 142)", "course/modules/M/M1/L05.html:7, 142", "PASS",
     "Meta description scope 'a positive rate and a positive time' matches Prop 1.4. Hypothesis prediction list matches the propositions cited (1.4, 2.1, 2.2, 2.4) and the printed checks (see M1-b-2.5-lab-L05)."),
 row("M1-b-r19-cards-scan", "round-19 full card scan (cards.json, 180 entries)", "course/modules/M/M1/cards.json", "PASS",
     "Counts: 180 entries; 37 cards for L04 and L05 (16 L04 + 21 L05); the new entries are M1-c181 (lesson L05) and M1-c180 (lesson L07, outside this slice, not verified here). No duplicate id or front (script output in the scratch scan). Keys consistent: back/front/id/lesson with optional grade and basis."),
 row("M1-b-r19-cards-c181", "new card M1-c181 (L05) checked against Remark 1.5 and Proposition 1.4", "course/modules/M/M1/cards.json:1246-1252; L05.html:87-99", "PASS",
     "Answer 'above one, and rises as t increases' for -1 < r < 0, t > 0 matches Remark 1.5 (line 98): the exponent -t ln(1+r) is positive and grows with t, and both Prop 1.4 claims reverse. Numerically: r = -0.5, t = 1, 2 gives factors 2.0 and 4.0 (increasing, above one)."),
]

fragment = {
    "unit": "M1",
    "slice": "M1-b",
    "round": 19,
    "verifier": "independent verifier (Haiku), round 19",
    "pin": "51fa336",
    "base": "7143726 (round 18 pin; delta re-read: L04.html, L05.html, cards.json)",
    "previous_fragment": "/tmp/fanout-frags/M1-b.round18.json",
    "checkout": "/tmp/verify19-M1-b",
    "scratch": "/tmp/M1-v/M1-b-r19",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is lessons L04 and L05 with their twins, not a project slice: no new student-error mutants, alternative implementations or mutant re-runs apply (same ruling as rounds 16-18). ledgers/M1/mutants/ holds the project mutants (slice a/c).",
        "Delta 7143726..51fa336 for this slice: L04.html lines 52, 70, 117, 257; L05.html lines 7, 52, 142, 270; cards.json two new entries (M1-c181 in this slice, M1-c180 lesson L07 out of slice, not verified). tests/labs/M1 and L03.html unchanged.",
        "Only one non-PASS row: M1-b-2.7-cards, card M1-c068 back drops the 'mt a whole number' condition that the rewritten Remark 1.3 (L04.html:70) now states. Fix named in the row.",
        "Hours: arithmetic only (70 = sum of eight data-hours). Pace not judged (architect ruling).",
        "Not checked: no external source is cited or read in this slice; the M1 registry was re-verified only as a live sample (1 of 560 entries) and L04/L05 cite no key. Lab output is SIMULATED-free (exact arithmetic), so no grade C basis is involved. L07 card M1-c180 and the rest of the M1 pages are outside this slice.",
    ],
    "summary": {},
}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = sum(1 for r in rows if r["status"] == "FAIL")
fragment["summary"] = {"rows": len(rows), "pass": pass_n, "fail": fail_n, "unverifiable": 0}
path = pathlib.Path("/tmp/verify19-M1-b/ledgers/M1/M1-b.json")
path.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n")
print(path, fragment["summary"])
