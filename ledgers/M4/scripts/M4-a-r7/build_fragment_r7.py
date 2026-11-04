"""Assemble the round-7 fragment for unit M4, slice a (hub, L01-L04, lab twins). Output: ledgers/M4/M4-a.json."""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/M4/scripts/M4-a-r7/"
G = S + "gates/"
R = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)


# ---- gates (re-run this round on pin 9373ef3) ----
row("A-G01", "2.9 structure: check_pages --unit M4", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    G + "check_pages.log: 'check_pages M4: PASS', exit 0 (run this round).")
row("A-G02", "2.9 DAG: check_dag --unit M4 (tool only; prose forward references are row DAG-A)",
    "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    G + "check_dag.log: 'check_dag M4: PASS', exit 0 (run this round). The tool reads the registry, not prose.")
row("A-G03", "2.6 projects gate, unit-wide (outside slice a; recorded because the rules name it)",
    "course/modules/M/M4/project.html", "PASS", G + "check_projects.log: 'check_projects M4: PASS', exit 0 (run this round).")
row("A-G04", "2.5 labs: run_labs --unit M4", "tests/labs/M4/lab-M4-L01-1.py..lab-M4-L04-1.py", "PASS",
    G + "run_labs.log: 'run_labs M4: PASS (13/13)', exit 0 (run this round).")
row("A-G05", "2.5 twins alone under python -I -W error; page code equals twin; expected block equals stdout",
    "tests/labs/M4/lab-M4-L01-1.py..L04-1.py; course/modules/M/M4/L01.html..L04.html", "PASS",
    S + "twins_r7.py (run: .venv/bin/python -I " + S + "twins_r7.py <checkout>): L01 exit 0, stdout 20 lines; "
    "L02 exit 0, 10 lines; L03 exit 0, 8 lines; L04 exit 0, 18 lines; each stderr empty; code_equals_twin=True and "
    "expected_equals_stdout=True for all four; output 'ALL OK'.")
row("A-G06", "2.9 page_smoke (slice pages, alone)", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    G + "page_smoke_slice.log: 'page_smoke M4: PASS', exit 0 (run this round with --pages index.html L01.html L02.html L03.html L04.html).")
row("A-G07", "gate: ruff check . (repository)", "repository", "PASS",
    G + "ruff_check.log: 'All checks passed!', exit 0; ruff check tests/labs/M4/ exit 0 (run this round).")
row("A-G08", "gate: ruff format --check . (repository)", "repository", "PASS",
    G + "ruff_format.log: '551 files already formatted', exit 0 (run this round). The round-6 failure "
    "(ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py) no longer occurs at pin 9373ef3.")
row("A-G09", "gate: mypy strict (mypy --no-incremental)", "repository", "PASS",
    G + "mypy.log: 'Success: no issues found in 385 source files', exit 0 (run this round).")
row("A-G10", "gate: relevant pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py, "
    "test_page_smoke.py, test_curriculum.py", "PASS", G + "pytest_relevant.log: all dots, exit 0 (run this round).")
row("A-G11", "2.1 citations: verify_refs --offline and verify_refs --unit M4 (live Crossref)",
    "references/references.json (blitzstein2019introduction)", "PASS",
    G + "verify_refs_offline.log: 'offline integrity: 560 entries, 0 problems', exit 0; " + G +
    "verify_refs_live_M4.log: 'live re-verification of M4: 1 of 560 entries, 0 problems', exit 0 (run this round).")
row("A-G12", "scope: delta since previous pin 142ecfc2, every hunk in slice a read",
    "course/modules/M/M4/L01.html:51; L02.html:270, :347; L03.html (78 changed lines, numbering and text); "
    "L04.html:52, :99; cards.json", "PASS",
    "git diff --stat 142ecfc2 9373ef3: slice-a subject files changed are L01, L02, L03, L04, cards.json. index.html, "
    "tests/labs/M4, notation/, references/, curriculum/, M1/ and tools/ are byte-identical (git diff --quiet). Every hunk "
    "in L01-L04 and cards.json was read this round (git diff 142ecfc2 9373ef3 -- <file>). project.html and grader/ changed "
    "but are outside slice a. Each changed prose claim was checked: L01 why-it-matters (118 words); L02 Lesson-6/10 pointers "
    "removed, P3 now 'This lesson does not develop that term'; L03 renumbered 2.1-2.8 with all cross-references updated; "
    "L04 forward pointers now 'developed later in this module'.")
row("A-G13", "2.1/2.8 generated-artefact gates: build_site --check, fetch_data --check, render_curriculum (no diff)",
    "tools/build_site.py; tools/fetch_data.py; curriculum/curriculum.json; CURRICULUM.md", "PASS",
    G + "build_site_check.log: 'site data current: 6 outputs', exit 0; " + G +
    "fetch_data_check.log: 'fetch_data: 3 datasets, 0 problems', exit 0; render_curriculum.py then "
    "'git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json' exit 0 (run this round).")

# ---- hub ----
row("A-H01", "2.9 structure: hub section order and minimum counts (BUILDER 4)", "course/modules/M/M4/index.html", "PASS",
    "Read in full (index.txt). Sections in order: header, objectives (6), prerequisites, placement diagnostic (10 items: "
    "8 M1/M2 + 2 data-skill), lessons (10 cards), ladder (4 rungs: worked example, completion problem, independent project, "
    "stretch), data status, core reading, footer. check_pages M4 PASS (G01).")
row("A-H02", "2.9 hours arithmetic: hub split vs lesson hours", "course/modules/M/M4/index.html:29, :42; L01..L04 data-hours",
    "PASS", "index.html:29 data-hours-lessons=\"90\" data-hours-project=\"30\"; L01..L04 data-hours=\"9\" each (grep); "
    "90 + 30 = 120 = curriculum.json M4 hours 120; 30/120 = 25%, which is the figure printed at index.html:42.")
row("A-H03", "2.9 objectives: measurable verbs, each mapped to a lesson", "course/modules/M/M4/index.html:49-54", "PASS",
    "Six objectives: Compute (L1), Derive (L2), Compute (L3), Decide/show/compute (L4, L5), Derive (L6), State/decide (L9, L10). "
    "Each lesson named exists and its content was read.")
row("A-H04", "2.6 prerequisites vs curriculum", "course/modules/M/M4/index.html:35, :60-64; curriculum.json M4 entry",
    "PASS", "Read this round: curriculum.json parts[1].modules[3] = {id M4, tier F, hours 120, prereqs [\"M2\"]}. Hub says "
    "M4 assumes M2 and, through M2, M1; the M2 prerequisite is the stated one.")
row("A-H05", "2.2/1.10 hub claim: matrix results proved from the quadratic form, which Lesson 5 defines",
    "course/modules/M/M4/index.html:62, :64; course/modules/M/M4/L05.html", "PASS",
    "Carried from round 6 (index.html and L05.html byte-identical since the previous pin, git diff --quiet): L05 "
    "states w^T Sigma w = Var(sum w_i X_i) >= 0 and the symmetry of Sigma, so the hub sentence is accurate.")
row("A-H06", "2.9 placement diagnostic: items, bar, skill checks (BUILDER 5.1)", "course/modules/M/M4/index.html:68-141",
    "PASS", "Read raw markup (index.html:68-141). Ten items: 8 without data-skill, 2 with data-skill (rung 1 at line 133, "
    "rung 2 at line 138). data-mastery=\"0.8\" = 8 of 10. Keys: five data-correct MC items and five numeric items "
    "(answers 0.5, 3, 1.875, 1, 0.6 with tolerances).")
row("A-H07", "3 attribution: 'M1 Theorem 3.1' in the first placement explanation", "course/modules/M/M4/index.html:79; course/modules/M/M1/L01.html:79",
    "PASS", "M1/L01.html is byte-identical since the previous pin. Line 79 'Theorem 3.1 (negating one quantifier)': the negation "
    "of 'for all x P(x)' is 'there exists x not P(x)'. Matches the hub explanation.")
row("A-H08", "2.2 numbers in placement answers and explanations", "course/modules/M/M4/index.html:75-140", "PASS",
    "Recomputed (G-script numbers_r7.log): negation (Q1) 'some student has not passed'; lim 1/n = 0 (Q2); int_0^1 x dx = 0.5 (Q3, tol 0.001); "
    "d/dt e^{rt} = r e^{rt} (Q4); ln(e^3) = 3 (Q5); 1+1/2+1/4+1/8 = 15/8 = 1.875 (Q6, tol 0.0005); discount 1/(1+r) (Q7); "
    "d/dx(x^2 y) = 2xy (Q8); rung 1 quantile 1 (F(0)=1/4<1/2<=F(1)=3/4); rung 2 s^2 = 3/5 = 0.6 with Var = 5/3 (L06 Prop 2.6, nu=5).")
row("A-H09", "2.2/2.4 rung-2 skill check hypothesis and its sources", "course/modules/M/M4/index.html:138-140; L06.html:158-159; L02.html:116-117",
    "PASS", "index.html:140 states the scale rule as a hypothesis, not proved. L02 Proposition 2.3 (line 116) is stated in the finite-space setting of "
    "L02 (line 55). L06 Proposition 2.6 (line 158) under Assumption 1 gives Var = nu/(nu-2) for nu > 2, so Var = 5/3 at nu = 5. "
    "Hub DAG note: see DAG-HUB-PREVIEW.")
row("A-H10", "2.7/2.9 hub lesson map and cards agree with the lessons", "course/modules/M/M4/index.html:148-159; L01..L10 h1 and data-hours",
    "PASS", "Titles at index.html:149-152 match the L01..L04 h1 titles and the curriculum introduces list. Hours 9 each (G-data-hours). "
    "Card-lesson mapping for L01..L04 checked in CARDS-L01..L04.")
row("A-H11", "2.6 ladder: the placement skip rule agrees between hub and project.html",
    "course/modules/M/M4/index.html:70, :164 vs course/modules/M/M4/project.html:42", "FAIL",
    "index.html:70 'To skip rungs 1 and 2, you must reach the bar and answer both skill checks.' index.html:164 'To skip them, reach the "
    "placement bar and answer both skill checks.' project.html:42 'If you met the placement bar on the module page, skip rungs 1 and 2 and start "
    "at rung 3.' (no skill-check condition; project.html:42 is byte-identical to the round-6 pin). BUILDER_RULES.md:191-193: 'A placement pass means "
    "meeting the hub quiz's data-mastery bar and answering every item marked data-skill.' The hub follows the rule; project.html:42 does not.",
    "project.html:42: change the condition to 'If you met the placement bar on the module page and answered both skill checks, skip rungs 1 and 2 "
    "and start at rung 3.' (project.html is outside slice a; route to its owner). Hub text needs no change.")
row("A-H12", "2.8 data status and SIMULATED labels", "course/modules/M/M4/index.html:37, :175, :187", "PASS",
    "index.html:37 and :175 say no real data is read and every seeded sample is SIMULATED. grep for open(, urllib, socket, requests, "
    "subprocess, http and data/ in tests/labs/M4/lab-M4-L01..L04-1.py: no hit. The four twins ran with no network (twins_r7.py). "
    "No svg, no data-files in index or L01..L04 (grep).")
row("A-H13", "2.1 reading list and citation: blitzstein2019introduction", "course/modules/M/M4/index.html:181-183; references/references.json",
    "PASS", "Registry record (python read this round): year 2019, years [2019], isbn [9780429428357], publisher 'Chapman and Hall/CRC', "
    "no edition key, source string 'Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)'. Hub index.html:183 states the edition "
    "comes from the curriculum and is not checked against the book. Live verify_refs --unit M4 PASS (G11). No passage is attributed.")
row("A-H14", "2.6 curriculum facts for the hub: no debate, no Atlas milestone, part and tier",
    "course/modules/M/M4/index.html:2, :31, :37; curriculum.json M4 entry", "PASS",
    "curriculum.json M4: tier F, hours 120, part M, no debate key, no milestone mentions M4 (python scan of milestones), "
    "sources [\"Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)\"]. index.html:37 says no debate brief and no Atlas milestone: consistent.")
row("A-H15", "2.9 hub footer", "course/modules/M/M4/index.html:187", "PASS",
    "Footer: 'Seeded samples are SIMULATED; no real data is used.' Consistent with A-H12.")

# ---- L01 ----
row("L01-PROSE", "2.9 prose: why-it-matters (<=120 words), definitions, interpretation text",
    "course/modules/M/M4/L01.html:51, :55-99, :114-119, :270, :277-297, :360-400", "PASS",
    "why-it-matters = 118 words (word count, python; limit 120). Definitions 1.1, 1.2, 2.1, 3.1 match their proofs. Line 270 interpretation "
    "(changed this round) is accurate: the grid check covers j/100 only, the proof covers (0,1], and the eps line is one value of eps. "
    "Read in full (scratch view of all 292 non-empty lines).")
row("L01-MATH", "2.4 mathematics: Prop 2.2, Prop 3.2, Remark 3.3, Prop 3.4, Examples 3.5-3.6 re-derived",
    "course/modules/M/M4/L01.html:80-135", "PASS",
    "Re-derived with exact fractions: F values 1/10, 3/10, 3/5, 4/5, 9/10, 1; Q(1/2)=0, Q(3/5)=0, Q(61/100)=1; 148/150=74/75 approx 0.987 < 0.99; "
    "ceil(148.5)=149; ceil(198)=198. Proposition 2.2 (a)-(d), the proof of 3.2 (infimum), Remark 3.3 left-continuity (u_n in (F_{k-1}, p]) and "
    "Proposition 3.4 proof all check. Lab 1 printed values match (see L01-LAB).")
row("L01-LAB", "2.5 lab: hypothesis, code, expected block, interpretation", "course/modules/M/M4/L01.html:138-270; tests/labs/M4/lab-M4-L01-1.py",
    "PASS", "twins_r7.py: code equals twin, expected equals stdout (20 lines, exact, data-tolerance 0), exit 0, stderr empty under -I -W error. "
    "Docstring claims (no randomness, no network, scan vs definition on 100 points, F(Q(p))>=p, Q(F(x))=x) match the code. "
    "Predicted values at l.140 match stdout lines 252-264.")
row("L01-PROBLEMS", "2.4 problem set: worked solutions re-derived", "course/modules/M/M4/L01.html:302-405", "PASS",
    "M1 (F, Q(1/2)=0); M2 (F(5)=7/10, Q(7/10)=5, Q(71/100)=7); M3 (ceil(36)=36, ceil(36.04)=37); P1-P3 proofs check; E1 (F(2)=9/10 < 99/100 <= F(3)=1); "
    "E2 (Q(3/5)=0, Q(3/5+eps)=1); E3 (grid count argument); R1 (strict rule gives Q^s(3/5)=1 and agrees elsewhere; checked at each case); "
    "R2 (left-continuity); R3 (grid vs proof).")
row("L01-QUIZ", "2.4 quiz: keys and explanations", "course/modules/M/M4/L01.html:424-494", "PASS",
    "Keys re-derived: Q(1/2)=1 for (1/4,1/2,1/4); Q(61/100)=1; the distribution function is not continuous at x_k (Prop 2.2(d)); 198 and 149; "
    "Q(F_k)=x_k; P(X<=1)=5/6 approx 0.833; X is a function Omega to R; Q(1)=x_m.")
row("L01-GRADES", "2.3 grades: T for proved claims; no lab-derived claim graded T", "course/modules/M/M4/L01.html:43-48, :80, :103, :114, :119, :413-418",
    "PASS", "Props 2.2, 3.2, Remark 3.3, Prop 3.4 graded T and proved on the page; Example 3.5 and 3.6 exact computations graded T. "
    "Lab outputs are restated as exact values (not graded T). Grade legend at l.43-48 matches BLUEPRINT section 3.")
row("L01-FWD", "2.9/1.10 forward references in L01", "course/modules/M/M4/L01.html:37, :51, :95", "PASS",
    "Only backward or M1 references; 'defined in Definition 3.1 below' (l.51) points to the same lesson. grep 'Lesson N': only the eyebrow.")

# ---- L02 ----
row("L02-PROSE", "2.9 prose: why-it-matters (<=120 words), definitions", "course/modules/M/M4/L02.html:51, :55-101, :147, :262", "PASS",
    "why-it-matters = 105 words. Line 51: 'Lab 1 checks the shortcut ... on a die and on a two-point loss ... and the scale rule on the die' "
    "matches the lab docstring (scale check on the die only). Definitions 1.1, 1.6, 2.1 match the text.")
row("L02-MATH", "2.4 mathematics: Defs 1.1, 2.1; Props 1.2, 1.3, 2.2, 2.3, 2.4; Examples 1.4, 1.5, 2.5, 2.6",
    "course/modules/M/M4/L02.html:57-142", "PASS",
    "Die E=7/2, E[X^2]=91/6, Var=35/12, sd 1.70783 (1.708). Loss E=12500, E[L^2]=3125000000, Var=2968750000, sd 54486.2368 (54486.24). "
    "Scale: Var(2X)=35/3=4*35/12. Proofs of Props 1.2, 1.3, 2.2, 2.3, 2.4 checked line by line.")
row("L02-LAB", "2.5 lab: hypothesis, code, expected block, interpretation", "course/modules/M/M4/L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py",
    "PASS", "twins_r7.py: exit 0, stderr empty, code equals twin, expected (10 lines) equals stdout. Printed: die mean 3.469, minus 3.5 = -0.031; "
    "489 losses, 12225.0 cents mean; three True lines (shortcut die, scale die, shortcut loss). Docstring matches code.")
row("L02-PROBLEMS", "2.4 problem set: worked solutions re-derived", "course/modules/M/M4/L02.html:298-401", "PASS",
    "M1 Var = 21/100; M2 mean 5000, Var 2.25e8, sd 15000; M3 36 and 4; P1 (linearity); P2 E[(X-c)^2]=Var+(mu-c)^2; P3 (V=-U: Var U=1, Var V=1, Var(U+V)=0, sides 0 and 2; "
    "re-derived; line 347 now says 'This lesson does not develop that term', so no forward pointer); E1 (3.469, -0.031); E2 (489 vs 500, 11 below); "
    "E3 (35/3); R1 (sample variance = Var of empirical law); R2 (Var(D)=296875, sd 544.8624); R3 (expectation 3/10, quantile 0).")
row("L02-QUIZ", "2.4 quiz: keys and explanations", "course/modules/M/M4/L02.html:421-492", "PASS",
    "Keys re-derived: 3.5; Var=5-4=1; Var(2X)=12; Definition 2.1; 5000; 2.25e8; 21/100; c=E[X]; 15000 cents; E[3X-1]=5.")
row("L02-MISC", "2.9 misconceptions: three or more, each with the wrong belief and the correction", "course/modules/M/M4/L02.html:279-296", "PASS",
    "Four misconceptions. 'Expectation is always a value': 3.5 not a face. 'Scaling multiplies Var by a': 35/3 = 4*35/12. 'Var = E[X^2]': 91/6 = 15.17, "
    "35/12 = 2.92; the two agree only when E[X]=0 (computed). 'Seeded mean equals expectation': 3.469 vs 3.5.")
row("L02-CANON", "2.4 canon section: finite-law scope, the mean vs the quantile, squared units", "course/modules/M/M4/L02.html:267-273; L01.html:135",
    "PASS", "Line 270 (changed): a law with E[X^2]=infinity has no finite variance; every law the lesson uses is finite. Line 271: E[X]=3/10 for L01 Example 3.6 "
    "((-2-2+0+2+2+3)/10), Q(1/2)=0 correct. Line 272 squared units correct.")
row("L02-FWD-COVARIANCE", "1.10/2.9 L02 Problem P3 uses a result from a later lesson before it is introduced",
    "course/modules/M/M4/L02.html:347", "PASS",
    "Round-6 FAIL resolved: line 347 now reads 'The general formula ... has an extra term ... This lesson does not develop that term.' "
    "No L02 text names Lesson 4-10 concepts (grep 'Lesson [3-9]|Lesson 10': none in L02 text).")
row("L02-FOOTER-SCOPE", "2.9 footer and references scope", "course/modules/M/M4/L02.html:496-507", "PASS",
    "References: 'Each exact result ... is proved on the page or is an exact computation on a stated list of values. The seeded samples ... are SIMULATED single-run estimates'. Accurate.")

# ---- L03 ----
row("L03-PROSE", "2.9 prose: why-it-matters (<=120 words), definitions 2.1-2.2, Props 1.1, 2.3 proof",
    "course/modules/M/M4/L03.html:51, :55-86", "PASS",
    "why-it-matters = 97 words. Def 2.1 refers to Proposition 2.3 (standardized moments) for mean 0 and variance 1, which is the correct block. "
    "Def 2.2 kurtosis without subtracting 3, stated. Prop 2.3 proof (E[Z^j] = m_j / sigma^j) checked.")
row("L03-MATH", "2.4 mathematics: Example 2.6 closed forms, section 3 central moments, section 4 counterexample, Prop 2.5 and Prop 2.8",
    "course/modules/M/M4/L03.html:110-128, :133, :260, :276", "PASS",
    "Example 2.6 re-derived: m3 = pq(q-p), m4 = pq(1-3pq), gamma3 = (1-2p)/sqrt(pq), gamma4 = (1-3pq)/(pq); p=1/10: 8/3 and 73/9, gamma3^2=64/9. "
    "Section 3 (numbers_r7.log): mu=7/4, m2=163/16, m3=2157/32 (terms -1372, -54, +1, +35937 over 512, sum 34512), m4=149461/256, "
    "gamma3^2 = 18610596/4330747 (sqrt 2.0730), gamma4 = 149461/26569 = 5.62539 (5.6254). Section 4: values -2,1,3 with 2/5,1/2,1/10: "
    "mean 0, m2=3, m3=0, m4=15, gamma4=5/3. Prop 2.8 integration by parts re-derived (E[Z^2]=1, E[Z^4]=3). p=(1-1/sqrt3)/2 gives pq=1/6, gamma4=3.")
row("L03-LAB", "2.5 lab: hypothesis, code, expected block, interpretation", "course/modules/M/M4/L03.html:135-254; tests/labs/M4/lab-M4-L03-1.py",
    "PASS", "twins_r7.py: exit 0, stderr empty, code equals twin, expected (8 lines) equals stdout. Printed 163/16, 2157/32, 149461/256, "
    "18610596/4330747, 2.0730, 149461/26569, 5.6254, True, True, sample skewness 2.065, kurtosis 5.580, exact 2.073 and 5.625. "
    "Lines 253 and E1 gaps 0.008 and 0.045 recomputed (0.008 and 0.045), rounding bound 0.001 is correct.")
row("L03-NUMBERING", "2.9 numbering: each block number in the lesson is unique and sequential (one counter per section)",
    "course/modules/M/M4/L03.html:70 (Def 2.1), :75 (Def 2.2), :80 (Prop 2.3), :90 (Prop 2.4), :100 (Prop 2.5), :110 (Example 2.6), :117 (Assumption 2.7), :122 (Prop 2.8)",
    "PASS", "Round-6 FAIL resolved. Section 2 numbers are 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, each once. Every cross-reference inside L03 "
    "(lines 71, 96, 106, 113, 123, 149, 163, 180, 209, 211, 223-227, 242, 248, 254, 262, 276, 278, 309, 327, 334, 370, 400-402, 475) points to the block with that number "
    "(grep of Proposition/Definition/Example/Assumption/Lesson 2 references).")
row("L03-STD-NORMAL-DUP", "2.9 duplication: the standard normal law is defined once (L06 Definition 1.1); L03 must not restate its density",
    "course/modules/M/M4/L03.html:118 (density formula), :122-123; course/modules/M/M4/L06.html:64-65 (Definition 1.1)", "FAIL",
    "L03.html:118 'Let f(z) = e^{-z^2/2}/sqrt(2 pi) for real z, the density of the standard normal law.' L06.html:65 'The standard normal law is N(0,1), "
    "with density phi(z) = e^{-z^2/2}/sqrt(2 pi)'. The same law and the same density are defined in two lessons. The round-6 PASS row stated that L03 does not "
    "restate the density, and that was wrong: the Assumption at L03:116-119 restates it.",
    "Remove the density formula and the name 'standard normal law' from L03 (Assumption 2.7 and Proposition 2.8, the card M4-c220, the "
    "key-result row, misconception line 276 and the hub lesson-card text at index.html:151), or move Assumption 2.7 and Proposition 2.8 into L06 after "
    "its Definition 1.1 and drop the normal-kurtosis claim from L03. Keep the Bernoulli kurtosis examples in L03, which need no normal law.")
row("L03-PROP28-SCOPE", "2.4 scope: Proposition 2.8 names Assumption 2.7 wherever its result is used",
    "course/modules/M/M4/L03.html:122-123, :262, :276, :401", "PASS",
    "Every use of Proposition 2.8 is accompanied by 'Assuming Assumption 2.7' or 'under Assumption 2.7' (lines 123, 262, 276 and key-result row 401). "
    "Assumption 2.7's statement says it is used without proof and lists its contents (line 117-119).")
row("L03-CANON", "2.4 canon section: symmetry vs zero skewness, kurtosis not peakedness, finiteness, sample is an estimate",
    "course/modules/M/M4/L03.html:258-265", "PASS",
    "Law -2, 1, 3 with probabilities 2/5, 1/2, 1/10: mean 0, m3 = -16/5+1/2+27/10 = 0, not symmetric (value -2 has prob 2/5; value 2 has prob 0). "
    "gamma4 = 15/9 = 5/3 (m2=3, m4=15). Bernoulli p=1/10 has 73/9 and two values. Sample estimate statement accurate.")
row("L03-MISC", "2.9 misconceptions: three or more", "course/modules/M/M4/L03.html:270-282", "PASS",
    "Three misconceptions: zero skewness = symmetric (corrected by section 4); kurtosis of every law is 3 (Bernoulli 73/9 and 7/3; the "
    "p=(1-1/sqrt3)/2 example gives 3 by Example 2.6); sign reversal leaves skewness unchanged (Prop 2.4 gives sign(a)). Each correct as read.")
row("L03-PROBLEMS", "2.4 problem set: worked solutions re-derived", "course/modules/M/M4/L03.html:286-388", "PASS",
    "M1 (p=1/4: sigma=sqrt3/4, gamma3=2/sqrt3, gamma4=7/3) re-derived; M2 (0/2 law: mu=1, m2=m4=1, gamma3=0, gamma4=1, equality case of Prop 2.5); "
    "M3 (m3=2157/32, positive); P1 (affine invariance) proof; P2 (E[Z^2]=1 by linearity); P3 (q^3+p^3=1-3pq) algebra checked; E1 gaps 0.008 and 0.045; "
    "E2 64/9 and 73/9; E3 weights 4,2,1,1 sum 8; R1 (kurtosis 1 only for symmetric two-point law); R2 (fat-tail claim needs tail probabilities); R3 (symmetry implies zero skewness, converse fails by Section 4 law).")
row("L03-QUIZ", "2.4 quiz: keys and explanations", "course/modules/M/M4/L03.html:408-478", "PASS",
    "Keys re-derived: m1=0; skewness is E[Z^3]; kurtosis of the symmetric two-point law 1; Y=-X changes sign; kurtosis unchanged under 5X+3; "
    "5/3 = 1.6667; the law on -2, 1, 3 (skewness 0, not symmetric); Bernoulli p=1/10 skewness 8/3 = 2.6667 (sqrt(pq)=0.3); symmetric law skewness 0.")
row("L03-GRADES", "2.3 grades: T for proved claims; the simulated sample is graded C where it is read",
    "course/modules/M/M4/L03.html:42-49, :57-134, :401-407", "PASS",
    "Props 1.1, 2.3-2.5, 2.8 and Example 2.6 are graded T and proved on the page; Prop 2.8 is T under the named Assumption 2.7. The "
    "simulated sample (2.065, 5.580) is not restated as T anywhere on the page (grep).")
row("L03-FOOTER-SCOPE", "2.9 footer and references scope", "course/modules/M/M4/L03.html:480-493", "PASS",
    "References and footer state the seeded sample is a SIMULATED single-run estimate and that the normal kurtosis is proved only under Assumption 2.7, "
    "which is used without proof and is not cited. Accurate.")

# ---- L04 ----
row("L04-PROSE", "2.9 prose: why-it-matters (<=120 words), Defs 1.1, 1.2, 2.1, Remark 1.3, Remark 2.2",
    "course/modules/M/M4/L04.html:52-70, :137-145", "PASS",
    "why-it-matters = 104 words. Line 52 (changed this round): 'The correlation and the covariance matrix are developed later in this module' "
    "names no lesson and uses no later definition. Example 1.9 correctly gives a dependent pair with E[XY] = E[X]E[Y] = 0.")
row("L04-TERM-ORDER", "1.10 terms used before definition within L04", "course/modules/M/M4/L04.html:52 vs :59, :98, :131",
    "PASS", "Why-it-matters names Definition 1.1 and Example 1.9 before they appear; both are labelled and later in the same lesson. "
    "'Covariance' is used in Example 1.9 after Definition 1.6 at line 98.")
row("L04-REMARK-1-3", "2.5 lab description vs code: Remark 1.3 and Parts A/B", "course/modules/M/M4/L04.html:70, :174-186; tests/labs/M4/lab-M4-L04-1.py",
    "PASS", "Remark 1.3 says 'Lab 1 applies the test to every cell of three tables (Parts A and B)': Part A has two tables and Part B one, and "
    "is_independent checks all cells (code lines 219-222). Verdict printed with cell (0,0): lines 283-286 of stdout.")
row("L04-MATH", "2.4 mathematics: Props 1.4, 1.5, 1.7, 1.8, 2.3, 2.4; Example 1.9, Example 2.5 re-derived",
    "course/modules/M/M4/L04.html:73-169", "PASS",
    "Prop 1.4, 1.5 (regrouping), 1.7 (expansion), 1.8. Example 1.9: E[XY]=E[X^3]=0, p(0,0)=1/3 vs 1/9. Example 2.5: marginals 2/5, 3/5; "
    "E[X]=4/5; E[X|Y=0]=1; E[X|Y=1]=2/3; total 4/5 (numbers_r7.log). Props 2.3, 2.4 proofs check.")
row("L04-LAB", "2.5 lab: hypothesis, code, expected block, interpretation", "course/modules/M/M4/L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py",
    "PASS", "twins_r7.py: exit 0, stderr empty, code equals twin, expected (18 lines) equals stdout. Printed 3/50 both sides; dependent cell 1/10 vs 4/25; "
    "Part B covariance 0, cell 1/3 vs 1/9, independent False; Part C E[X|Y=0]=1, E[X|Y=1]=2/3, total 4/5 = E[X], product table True.")
row("L04-PROBLEMS", "2.4 problem set: worked solutions re-derived", "course/modules/M/M4/L04.html:331-434", "PASS",
    "M1 (0.12 vs 0.1, dependent); M2 (E[X|Y=1]=2/3, E[X]=0.7); M3 (cells 1/8, 1/8, 3/8, 3/8; E[XY]=1/8); P1 covariance shortcut; P2 two-valued Y; "
    "P3 Cov(1_A,1_B) = -ab; E1 (sum 4/5); E2 (ratio 3); E3 (ratio 5/8 = 0.625); R1 (Cov=0, dependent); R2 (Cov(X,X)=Var); R3 (equal conditional means, dependent).")
row("L04-QUIZ", "2.4 quiz: keys and explanations", "course/modules/M/M4/L04.html:453-527", "PASS",
    "Keys re-derived: dependent (1/3 vs 1/9); E[X|Y=0] = (2/10+2/10)/(2/5) = 1; E[XY]=E[X]E[Y] for independence; E[X]=4/5; events with positive probability and "
    "no common outcome are dependent; P(Y=1)=3/5; product-table cell 3/50.")
row("L04-CANON-MISC", "2.4/2.9 canon section and misconceptions", "course/modules/M/M4/L04.html:303-329", "PASS",
    "Four canon bullets re-derived: marginals do not fix the table (p(0,0)=1/2 vs 1/4); product rule fails for X=Y=+-1 (E[XY]=1 vs 0). "
    "Three misconceptions correct: zero covariance is not independence, disjoint events are dependent, E[X|Y=y] need not equal E[X].")
row("L04-FOOTER", "2.9 references and footer scope", "course/modules/M/M4/L04.html:530-543", "PASS",
    "'This lesson cites no outside source. Every result ... is derived on the page (grade T)'. No registry key is cited on the page (grep). Accurate.")
row("L04-FWD", "2.9/1.10 forward pointers to later lessons in L04",
    "course/modules/M/M4/L04.html:52, :98, :99", "PASS",
    "Round-6 FAIL resolved: line 52 and line 99 no longer name Lesson 5 or say 'L05 defines the correlation'; they say 'developed later in this module'. "
    "The title at line 98, 'covariance, defined here and studied in L05', is a pointer to a later lesson that names no definition used earlier; the covariance "
    "formula is defined on this page at line 99. Recorded as a pointer, not a use.")

# ---- cards ----
row("CARDS-DUP", "2.7 duplicates: full scan of cards.json (229 cards)", "course/modules/M/M4/cards.json", "PASS",
    S + "cards_dag_r7.log: cards total 229; dup ids [], dup fronts [], dup backs []; grades T 204, C 25; missing fields []. "
    "Per-lesson counts L01 23, L02 20, L03 29, L04 20.")
row("CARDS-L01", "2.7 cards for L01 vs current lesson text", "course/modules/M/M4/cards.json: M4-c001..c016, c173, c192..c195, c197, c198",
    "PASS", "All 23 cards read and checked against L01 (current text). Hypotheses present where the proposition needs them (c005, c006, c008, c009, c013, "
    "c014, c197, c198). c011 (198), c015 (148.5, 149), c012 (Q(1/2)=0) match the lesson numbers. c030 and c033 are C-graded lab results (L02). "
    "No card contradicts the current text.")
row("CARDS-L02", "2.7 cards for L02 vs current lesson text", "course/modules/M/M4/cards.json: M4-c017..c033, c181, c182, c199",
    "PASS", "All 20 cards read. c023 (scale and shift), c028 (35/3 = 4 x 35/12), c029 (only when E[X]=0), c032 (Problem P2), c031 and c182 (2968750000, 54486.24) "
    "match the page. c030 (3.469) and c033 (489 of 10000) are C-graded lab results and match the printed output.")
row("CARDS-L03", "2.7 cards for L03 vs current lesson text (numbers cite the current labels)",
    "course/modules/M/M4/cards.json: M4-c034..c048, c183, c200, c212, c214, c215, c220, c222..c229", "PASS",
    "All 29 L03 cards read. Numbers cite the renumbered blocks: Prop 2.3 (c038, c214, c225, c229), Prop 2.4 (c039, c046, c215), Prop 2.5 (c040), "
    "Example 2.6 (c041, c045, c048, c226), Prop 2.8 with Assumption 2.7 (c220). c220 restates the density formula, which is the duplication flagged in "
    "L03-STD-NORMAL-DUP. Other cards are correct against the text.")
row("CARDS-L04", "2.7 cards for L04 vs current lesson text", "course/modules/M/M4/cards.json: M4-c049..c066, c201, c204",
    "PASS", "All 20 L04 cards read. c054, c057, c060, c061, c066 carry the finite-values hypothesis in the front. c062 (1 from (2/10+2/10)/(2/5)), c063, c064 (Problem P3), "
    "c065 (2/3 vs 4/5), c066 (Problem R2) match the page.")
row("CARDS-NUMBERS", "2.7 every card number appears in its lesson", "course/modules/M/M4/cards.json (slice a cards) vs L01..L04.html", "PASS",
    S + "cards_dag_r7.log: 'card number not in lesson' reports only M4-c043 (5/3) and M4-c044 (2/5), which appear in L03 as TeX \\tfrac53 and \\tfrac25 "
    "(line 260); all other numbers present in plain text of the lesson or the lab output.")
row("CARD-M4-c219", "2.7 card M4-c219 (round 5 FAIL: no grade field)", "course/modules/M/M4/cards.json", "PASS",
    "No card with id M4-c219 remains; every one of the 229 cards has a grade in T or C (cards_dag_r7.log: missing fields []).")

# ---- notation ----
row("NOTATION-A", "1.13/2.4 notation: one meaning per symbol across the unit; registry symbols keep their meaning",
    "course/modules/M/M4/index.html, L01..L04.html (slice a); cross-slice: L06.html:65, L07.html, L08.html, L09.html", "PASS",
    "Slice a: no phi, varphi or Phi symbol in index.html, L01..L04 (TeX scan). L03 now uses f for the density (line 118). The round-6 "
    "conflict is no longer in slice a. NOT resolved unit-wide: course/modules/M/M4/L06.html:65 uses phi(z) for the normal density, while "
    "L07.html and L09.html use varphi_X(t) for the characteristic function, and L08 uses varphi for the density. This is a cross-slice FAIL for "
    "the slices that own L06-L09; see notes.")
row("NOTATION-REG", "1.13 registered symbols used in slice a conform to notation.json", "course/modules/M/M4/L03.html (gamma_3, gamma_4); notation/notation.json",
    "PASS", "notation.json: gamma_3 = E[(r-mu)^3]/sigma^3; gamma_4 = E[(r-mu)^4]/sigma^4 not excess, 3 under normality. L03 Def 2.2 uses "
    "gamma_3 = E[Z^3], gamma_4 = E[Z^4] with Z = (X-mu)/sigma, the same meaning. T (number of observations) is not used as a symbol in slice a "
    "(L04 T occurrences are the grade letter). Phi (standard normal CDF) is not used in slice a.")
row("NOTATION-MACRO", "1.13 registry macros: pages may use only the registered macros (BUILDER 3.1-3.2)",
    "course/modules/M/M4/index.html, L01..L04.html", "PASS",
    "Slice a uses the registered \\R (L01, 4 uses) and writes \\operatorname{Var} directly (103 uses) where the registry macro \\Var expands to exactly "
    "\\operatorname{Var}. Not a new symbol and no meaning change. Expectation is written E[...] in plain text, not with the registered \\E macro. "
    "Recorded as a note for the builder; not a meaning conflict.")

# ---- DAG ----
row("DAG-A", "1.10/2.9 DAG: no concept used before it is introduced; no link to a later definition (plan line 113)",
    "course/modules/M/M4/L03.html:118, :122-123, :262, :276, :401", "FAIL",
    "check_dag passes (G02) because it reads the registry, not prose. In prose, L03 uses the term 'standard normal law' six times "
    "(lines 118, 122, 123, 262, 276, 401). That law is the concept of L06 (normal-distribution, Definition 1.1, L06.html:64-65), which is "
    "a later lesson. The plan's prose-only list (plans/M4-build-plan.md, 'Undeclared terms') does not include 'normal', and "
    "the Architect decisions (Q3) list only moment, chi-square, Cauchy, determinant, order statistic. L03's uses precede the definition.",
    "Either move Assumption 2.7 and Proposition 2.8 (with the card M4-c220, the key-result row at line 401, the misconception at line 276, "
    "and the hub text at index.html:151) into L06 after its Definition 1.1, or remove the named law from L03 and state the Bernoulli examples only. "
    "The same change fixes L03-STD-NORMAL-DUP. Recheck with grep 'standard normal' in L01..L04 (must be empty).")
row("DAG-HUB-PREVIEW", "1.10 hub (not a lesson): a placement item uses Student-t, a Lesson 6 concept",
    "course/modules/M/M4/index.html:138-140", "PASS",
    "The hub is not a lesson node, so 'a lesson never links a later definition' does not bind it. The hub names the source ('Lesson 6') and labels the "
    "item as a hypothesis-based skill check. Recorded for the architect: hub previews of later concepts are used by name on the placement page.")
row("DAG-L02-L04-USES", "1.10 concepts used in slice a lessons are backward or in their own closure",
    "course/modules/M/M4/L01.html..L04.html", "PASS",
    "L01 uses M1 quantifiers and M2 limit/infimum (infimum defined in section 3 where first used). L02 uses L01 random variable, distribution, and M2 "
    "integral. L03 uses L02 expectation, variance, Prop 2.4 (zero variance). L04 uses L01 and L02 only (independence, conditional expectation are "
    "its own dfn). No slice-a lesson links a concept defined in a later lesson (grep 'Lesson [5-9]|Lesson 10' in L01-L04: none, apart from the "
    "L04 pointer at line 98-99 and the L03 standard-normal issue in DAG-A).")

# ---- process, scope, data, structure, numbers, grades, assumptions ----
row("PROCESS-A", "2.9 process words and banned phrases (BUILDER 1.3-1.4)", "course/modules/M/M4/index.html; L01.html..L04.html; cards.json (slice a)", "PASS",
    "Case-insensitive grep of prose for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, "
    "it is important to note, studies show, experts agree, well known, obviously, clearly, can be shown, easy to see, roughly, historically, "
    "approximately, trivial, of course, let us, in summary, ellipsis: no hit in prose (the only ellipses are Python type hints in lab code). "
    "Process words (round, revised, verifier, builder, previous, changed): no hit in learner text.")
row("SCOPE-A", "4 scope words (only, all, always, every, any, exactly) carry a computation or a stated hypothesis",
    "course/modules/M/M4/index.html:37, :175; L01.html:55, :99, :270, :279, :375-377; L02.html:135, :146, :289; L03.html:262, :270; L04.html:131-133, :322",
    "PASS", "'every' in L01 Prop 2.2 scope and 'at all 6 support points' (computed, lab prints True); L02:289 'only when E[X]=0' follows from "
    "Var = E[X^2] - mu^2; L03:262 'every law ... is finite' follows from the finite sums; L04:131 'every cell' is checked by the lab; L04:322 "
    "'Disjoint events with positive probability are not independent' follows from Prop 1.4.")
row("DATA-A", "2.8 data: none; SIMULATED labels present where samples are shown", "course/modules/M/M4/index.html:37, :175; L02.html:146; L03.html:137",
    "PASS", "No dataset is named in curriculum M4 (sources line names only the book); no lab reads a file (A-H12). Seeded samples are labelled SIMULATED on the page that shows them (L02:146, L03:137).")
row("STRUCT-A", "2.9 structure: BUILDER 4.2 order and minimum counts", "course/modules/M/M4/L01.html..L04.html", "PASS",
    "Each lesson has why-it-matters (118, 105, 97, 104 words: all <= 120), numbered sections, inline labs, canon breaks, at least three misconceptions "
    "(3, 4, 3, 3), a problem set (M1-M3, P1-P3, E1-E3, R1-R3 in each), a retrieval quiz (9-10 items), references and a footer. check_pages M4 PASS (G01).")
row("NUM-A", "2.2 numbers in prose: one row per number, recomputed", "course/modules/M/M4/L01.html, L02.html, L03.html, L04.html, index.html",
    "PASS", S + "numbers_r7.log (exact fractions and floats): 1.708, 54486.24, 544.8624, 296875, 15.17, 2.92, 0.625, 0.06, 0.12, 0.8, 0.6, 0.6667, "
    "0.987, 2.0730, 5.6254, 5.625, 1.155, 8.11, 2.6667, 1.6667, 0.008, 0.045, 1425/512, 1.875, 0.031 (3.469 - 3.5 = -0.031) all match the page. No prose number uses a "
    "rounding inconsistent with its exact value.")
row("GRADE-A", "2.3 grades in slice a: T only on proved or exactly computed claims; C on simulated results",
    "course/modules/M/M4/L01..L04.html grade blocks; cards.json", "PASS",
    "Key-result tables: T rows are proofs or exact computations on stated tables. Simulated outputs are C only in cards c030, c033, c047, c183 (grep). "
    "Hub placement answers are not graded as results.")
row("ASSUMP-A", "2.4 assumptions: each unproved fact is a named numbered Assumption, and each result that uses it says so",
    "course/modules/M/M4/L03.html:116-119 (Assumption 2.7); L03.html:122-123, :262, :276, :401", "PASS",
    "The only unproved fact in slice a is the Gaussian integral and its calculus facts, named as Assumption 2.7 with its contents (line 117-119). "
    "Prop 2.8 and its uses name it (see L03-PROP28-SCOPE). The scale rule for Student-t variables is labelled as a hypothesis on the hub (index.html:138-140). "
    "Subject to DAG-A and L03-STD-NORMAL-DUP for the placement of the result.")

data = {
    "unit": "M4",
    "slice": "a",
    "round": 7,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyD7-M4-a)",
    "pin": "9373ef398589097500ea849e30ff9da423b98943",
    "base": "142ecfc2bd27061de18bd67e83df81e69f5c249d",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD7-M4-a",
    "scratch": S,
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "blitzstein2019introduction: registry record carries no edition field; '2nd ed. (2019)' comes from the curriculum "
        "source string only and is not verified against the book (index.html:183 says so)."
    ],
    "freshness_flags": [],
    "notes": (
        "Mutants: slice a is lessons, hub and lab twins, not a project; mutation testing applies to project graders only (rulings), so none written. "
        "Cross-slice items recorded for their owners: (1) NOTATION-A unit-wide: phi is the normal density in L06.html:65 and L08 but the characteristic "
        "function in L07 and L09 (varphi_X(t)); (2) project.html:42 placement rule (A-H11); (3) L06 must define the standard normal law before L03 uses it "
        "if the normal-kurtosis result stays in L03 (DAG-A). Judgment calls, stated: L04 Definition 1.6 title 'studied in L05' is a pointer, not a use "
        "(L04-FWD PASS); the hub's Student-t placement item is not a lesson use (DAG-HUB-PREVIEW PASS, architect to confirm); symbol p is used for a quantile "
        "level and for weights p(omega) in L01 (local letter, not registered; not a FAIL). Not checked: the grader and project page content (other slices); "
        "the L05-L10 pages; Blitzstein's text (not read; the lessons attribute nothing to it); the live Crossref record beyond verify_refs --unit M4."
    ),
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in R:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
data["summary"] = (f"Slice a round 7 at 9373ef3: {len(R)} rows; {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
                   f"{counts['UNVERIFIABLE']} UNVERIFIABLE. FAIL rows: A-H11 (placement skip rule, project.html:42 vs BUILDER 5.1), "
                   "DAG-A (L03 uses 'standard normal law' from L06 before L06), L03-STD-NORMAL-DUP (L03:118 restates the L06 density).")
if counts["FAIL"] or counts["UNVERIFIABLE"]:
    data["verdict"] = "FAIL"
else:
    data["verdict"] = "PASS"
out = ROOT / "ledgers/M4/M4-a.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts, data["verdict"])
