"""Writes the round-2 slice-a fragment ledgers/M4/M4-a.json (verifier output, no prose beyond the rows)."""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)


S = "ledgers/M4/scripts/M4-a-r2/"
# ---- gates (round 2 re-runs on pin c737272) ----
row("A-G01", "2.9 structure: check_pages", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    "Round 2: .venv/bin/python tools/check_pages.py --unit M4 -> 'check_pages M4: PASS', exit 0.")
row("A-G02", "2.9 DAG: check_dag", "course/modules/M/M4/*.html (slice a pages)", "PASS",
    "Round 2: .venv/bin/python tools/check_dag.py --unit M4 -> 'check_dag M4: PASS', exit 0. Independent reading in DAG-A.")
row("A-G03", "2.6 projects: check_projects (unit-wide)", "course/modules/M/M4/project.html (not in slice a)", "PASS",
    "Round 2: .venv/bin/python tools/check_projects.py --unit M4 -> 'check_projects M4: PASS', exit 0. project.html changed since d0f39c09 (16 lines); re-run on c737272.")
row("A-G04", "2.5 labs: run_labs", "tests/labs/M4/lab-M4-L01-1.py..L04-1.py and their page sections", "PASS",
    "Round 2: .venv/bin/python tools/run_labs.py --unit M4 -> 'run_labs M4: PASS (13/13)', exit 0.")
row("A-G05", "2.5 labs: twins alone under python -I -W error; page code equals twin; expected block equals stdout",
    "tests/labs/M4/lab-M4-L01-1.py..L04-1.py; course/modules/M/M4/L01..L04.html", "PASS",
    S + "m4a_r2_twins.py (run .venv/bin/python -I ...): each twin run from an empty scratch directory with python -I -W error exits 0 with empty stderr; L01 20 lines, L02 10, L03 8, L04 18 stdout lines equal the page expected blocks; page data-run code equals the twin (after html.unescape, trailing newline stripped). Output ends 'ALL OK'.")
row("A-G06", "2.9 page_smoke (slice pages alone)", "course/modules/M/M4/index.html, L01..L04.html", "PASS",
    "Round 2: .venv/bin/python tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04 -> each page PASS, labs 0.0 s each, 'page_smoke M4: PASS', exit 0.")
row("A-G07", "gate: ruff", "whole repository", "PASS",
    "Round 2: .venv/bin/ruff check . -> 'All checks passed!'; .venv/bin/ruff format --check . -> '473 files already formatted'.")
row("A-G08", "gate: mypy strict", "whole repository", "PASS",
    "Round 2: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 331 source files', exit 0.")
row("A-G09", "gate: relevant pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py, test_page_smoke.py, test_curriculum.py", "PASS",
    "Round 2: .venv/bin/pytest -q <those six files> -p no:cacheprovider -> 389 dots across six lines, no failures, exit 0.")
row("A-G10", "2.1 citations: verify_refs", "references/references.json (blitzstein2019introduction, lines 3127-3170)", "PASS",
    "Carried from round 1 (references/references.json and tools/ byte-identical since the previous pin d0f39c09, checked with git diff --quiet): the live run recorded in round 1 (verify_refs_live at pin d0f39c09) stands. Round 2 re-ran .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0. The live Crossref run was not repeated in round 2.")
row("A-G11", "scope: bytes of slice a since the previous pin", "index.html, L01..L04.html, cards.json (L01-L04 cards), tests/labs/M4/lab-M4-L01..L04-1.py", "PASS",
    "git diff d0f39c09 c737272 for the slice files: index.html 1 line (L03 card), L01.html 10 lines, L02.html 4, L03.html 32, L04.html 2 (hypothesis paragraph), cards.json 57 lines (wording, c029, c195, c005, c008, c010, c211 and c213 removed, c219 and c220 added). Twins unchanged. Every hunk was read and is covered by the rows below.")

# ---- hub ----
row("A-H01", "2.9 structure: hub section order (BUILDER_RULES 4)", "course/modules/M/M4/index.html:29 main, :45 objectives, :58 prerequisites, :68 placement, :145 lessons, :162 ladder, :173 data, :178 reading", "PASS",
    "Re-read index.html lines 1-190 in full. Order matches BUILDER_RULES 4 (objectives, prerequisites, placement, lessons, ladder, data, reading). Minimum counts: 6 objectives, 10 placement items, 10 lesson cards, 4 rungs.")
row("A-H02", "2.9 hours arithmetic", "index.html:29, :40, :42, :147; L01..L04.html data-hours", "PASS",
    "index.html:29 data-hours-lessons=90, data-hours-project=30; :42 '90 h lessons · 30 h project (25% of 120 h)'; 10 lessons x 9 h = 90; 90 + 30 = 120; 30/120 = 25% (hours-split widths 75%/25%, :40); L01..L04 data-hours=9; curriculum M4 hours 120.")
row("A-H03", "2.9 objectives: measurable verbs and lesson mapping", "index.html:48-55", "PASS",
    "Six objectives with measurable verbs (compute, derive, decide, state); each maps to a lesson (L01, L02, L03, L04-L05, L06, L09-L10) that teaches it.")
row("A-H04", "2.9 prerequisites vs curriculum", "index.html:35, :60-64; curriculum/curriculum.json M4 entry", "PASS",
    "Prerequisites M2 and M1 match the curriculum M4 entry; the 'matrix facts' sentence at :64 is prose, not a link to M3, consistent with plans/M4-build-plan.md Q2 and FINAL-ARCHITECT-RULINGS item 3.")
row("A-H05", "1.10 DAG: hub claim that matrix facts come from the quadratic form in Lessons 5 and 8", "index.html:35, :62 vs course/modules/M/M4/L05.html:131 and L08.html:308", "PASS",
    "Corrected locators. Round 1 cited L05.html:54 (a section heading) and L08.html:170 (empty), which do not show the claim. L05.html:131 (Proposition 2.3 proof, positive semidefiniteness from w^T Sigma w) and L08.html:308 ('quadratic form' in the positive-definiteness discussion) carry it. No M3 link: grep found no M3 concept link in M4 slice pages.")
row("A-H06", "2.9 placement: 10 items, mastery bar", "index.html:68-143, :70", "PASS",
    "Ten items (eight M1/M2 items, two data-skill items at :133 and :137). Bar 80 percent = 8 of 10 (:70). Matches BUILDER_RULES and plans/M4-build-plan.md.")
row("A-H07", "3 attribution: placement item 1 'M1 Theorem 3.1'", "index.html:79 vs course/modules/M/M1/L01.html:79", "PASS",
    "M1/L01.html:79 'Theorem 3.1 (negating one quantifier)'; the negation of 'for every' is 'for some ... not' (M1 :89 applies it). M1 byte-identical since d0f39c09.")
row("A-H08", "2.2 numbers in placement items 2-8", "index.html:82-131", "PASS",
    "Checked by hand against the options and explanations: int_0^1 x dx = 1/2; ln(e^3)=3; 1+1/2+1/4+1/8 = 15/8 = 1.875 (also in " + S + "m4a_r2_numbers.py); one-year discount factor 1/(1+r); d/dx(x^2 y) = 2xy. All match.")
row("A-H09", "2.2 skill check rung 1", "index.html:133-135", "PASS",
    "Law 0,1,2 with 1/4,1/2,1/4: F(0)=1/4 < 1/2 <= F(1)=3/4, so Q(1/2)=1 by L01 Proposition 3.2 (L01.html:103-110). Recomputed in " + S + "m4a_r2_numbers.py.")
row("A-H10", "2.2 skill check rung 2 and its hypotheses", "index.html:137-140 vs course/modules/M/M4/L06.html:158-173 (Proposition 2.6), L06.html:59 (Assumption 1), L02.html:55 and :115", "PASS",
    "L06.html:158 'Proposition 2.6 (mean and variance of the Student-t)'; L06.html:173 gives Var = nu/(nu-2) for nu>2 and infinite second moment for nu<=2. nu=5: Var = 5/3, s^2 = 3/5 = 0.6 (checked by hand). The scale-rule hypothesis is stated as an assumption on the page (index.html:140) and L02.html:55 limits Proposition 2.3 to finite spaces, so the hub correctly labels it not proved.")
row("A-H11", "2.9 hub lesson cards L01-L04 agree with lesson text", "index.html:149-152 (L03 card changed at :151)", "PASS",
    "L03 card now names 'the normal kurtosis of 3 under a stated Gaussian-integral assumption', matching L03 Assumption 2.6 (L03.html:116-119), Definition 2.7 (:121-124) and Proposition 2.8 (:126-134). L01, L02, L04 card wording matches the lesson text (checked against L01 Definition 3.1, L02 Example 2.5, L04 Definition 1.2 and Definition 2.1).")
row("A-H12", "2.9 hub card titles vs lesson h1", "index.html:149-152 vs L01..L04.html h1", "PASS",
    "Card titles equal the h1s: L01.html:35 'Random Variables, Distributions and Quantiles'; L02.html:35 'Expectation and Variance'; L03.html:35 'Skewness and Kurtosis'; L04.html:36 'Independence and Conditional Expectation (Elementary)'.")
row("A-H13", "2.9 ladder: four rungs in order; project names", "index.html:162-171; course/modules/M/M4/project.html:36, :108, :127-130", "PASS",
    "Four rung-title items in order (Worked example, Completion problem, Independent project, Stretch). project.html:36 'Tail-Risk Simulator'; quantile_99 at project.html:108; matched_scale and simulate_losses/tail_risk.py named in project.html (grep counts 6, 5, 5) as the hub states.")
row("A-H14", "2.8 data status and SIMULATED labels", "index.html:37, :175; L01..L04.html footers and lab docstrings", "PASS",
    "index.html:175 'No real data is used in M4'. L02 footer and L03 footer and L03 lab hypothesis label the seeded samples SIMULATED; L01 and L04 labs use exact tables with no randomness (verified in lab code).")
row("A-H15", "2.1 citation: blitzstein2019introduction", "index.html:181-183; L01..L04.html References; references/references.json:3127-3170", "PASS",
    "Registry record at references.json:3127-3170: year 2019, isbn 9780429428357, publisher 'Chapman and Hall/CRC', source string 'Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)'. index.html:183 states exactly this (year, ISBN, publisher, edition from curriculum, not checked against the book). references.json byte-identical since d0f39c09.")
row("A-H16", "2.6 debate and Atlas status", "curriculum/curriculum.json M4 entry; index.html:37", "PASS",
    "Python check of the M4 entry: keys id, title, tier, hours 120, prereqs, core, introduces, sources, lab, project, part; no debate or atlas key or string. index.html:37 says 'no debate brief and no Atlas milestone'. Consistent.")

# ---- lessons ----
row("L01-PROSE", "2.2 numbers and claims in prose", "L01.html:37-51, :55, :69 (Example 1.3), :95-99, :129-135, :277-281, :287-297, :360-370, :388-398", "PASS",
    "Example 1.3: P(X<=1)=1/2+1/3=5/6 (numbers script). Example 3.5: 0.99x200=198, 0.99x150=148.5, ceil=149, 148/150=74/75=0.987 < 0.99. Example 3.6: F values 1/10, 3/10, 3/5, 4/5, 9/10, 1 and Q(1/2)=0, Q(3/5)=0, Q(61/100)=1 (recomputed). Lab expected block matches stdout. The new pointer in the why-it-matters paragraph (L01.html:51) is covered by L01-FWD-POINTER.")
row("L01-MATH", "2.4 definitions, Prop 2.2, Prop 3.2, Remark 3.3, Prop 3.4, proofs", "L01.html:57-126", "PASS",
    "Re-derived each proof: Prop 2.2(a)-(d) (L01.html:88-91); Prop 3.2 infimum argument (:107-110) uses 2.2(b),(c) correctly; Remark 3.3 (:112-116) incl. left-continuity at p=F_(k-1) (k=1 excluded since p>0); Prop 3.4 (:118-126) with 0<pn<=n. Definition 3.1 uses \\R (registered macro, notation.json:25). No gaps.")
row("L01-LAB", "2.5 lab: hypothesis, output, interpretation", "L01.html:138-271; tests/labs/M4/lab-M4-L01-1.py", "PASS",
    "Twin run (" + S + "m4a_r2_twins.py): exit 0, 20 lines equal the expected block. Hypothesis predictions (L01.html:140: Q values at 1/20, 1/10, 11/100, 1/2, 3/5, 61/100, 9/10, 91/100, 99/100, 1) equal the printed values. Interpretation (:270) describes the grid check and the epsilon line accurately; 'scan equals definition at 100 of 100 points' is the printed line.")
row("L01-PROBLEMS", "2.4 problem set worked solutions", "L01.html:302-405", "PASS",
    "M1 (F, Q(1/2)=0), M2 (F(5)=7/10, Q(7/10)=5, Q(71/100)=7), M3 (index 36 and 37 for 40 values: 40x0.901=36.04), P1-P3, E1 (Q(99/100)=3), E2, E3, R1 (Q^s(3/5)=1), R2, R3 re-derived; all solutions correct and complete.")
row("L01-QUIZ", "2.9 quiz answers and explanations", "L01.html:424-494", "PASS",
    "q1 Q(1/2)=1 for 1/4,1/2,1/4 (explanation correct); q2 Q(61/100)=1; q3 jump (Prop 2.2(d)); q4 198; q5 149; q6 Q(F_k)=x_k; q7 P(X<=1)=5/6=0.8333 within tolerance 0.0005; q8 Definition 1.1; q9 Q(1)=x_m. All match the lesson.")
row("L01-GRADES", "2.3 grades", "L01.html:43-48 legend, :80, :103, :113, :119, :413-418", "PASS",
    "Prop 2.2, Prop 3.2, Remark 3.3, Prop 3.4 and the table rows are T; each is proved on the page (Proof blocks at :88, :107, :115, :125). No A-D claim on the page.")
row("L01-FWD-POINTER", "5 terms used before definition (within-lesson forward pointer)", "L01.html:51 'a quantile (defined in Definition 3.1 below)'", "PASS",
    "Within-lesson pointer, not a cross-lesson link: the why-it-matters paragraph glosses the term informally and names its definition (Definition 3.1, L01.html:98-99) and the meta row introduces quantile-function there. The round-1 rule that forbade a forward pointer targeted links to later lessons (plan 'No lesson links a later definition'), so this is accepted.")

row("L02-PROSE", "2.2 numbers and claims in prose", "L02.html:51, :55, :84-90, :134-141, :262, :267-272, :281-293, :358-365, :390-398", "PASS",
    "Example 1.4: E = 7/2. Example 1.5: E[L]=12500 (250000/20 integer). Example 2.5: sqrt(35/12)=1.7078, '1.708'. Example 2.6: E[L^2]=3125000000, Var=2968750000, sd=54486.237 -> '54486.24'. Canon bullet 3: E[X]=3/10 for the L01 table (checked by hand). Lab expected block equals stdout (twin run).")
row("L02-MATH", "2.4 definitions, Props 1.2-1.3, 2.2-2.4, Def 1.6, proofs", "L02.html:57-132", "PASS",
    "Prop 1.2 grouping proof (:69); Prop 1.3 (:77-79); Def 1.6 with no result depending on it (:92-95); Def 2.1 (:99-102); Prop 2.2 expansion (:109-112) correct; Prop 2.3 (:119-122); Prop 2.4 (:129-132). All re-derived.")
row("L02-LAB", "2.5 lab: hypothesis, output, interpretation", "L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py", "PASS",
    "Twin run exit 0; 10 lines equal the expected block (die 7/2, 91/6, 35/12; loss 12500, 3125000000, 2968750000; sd 54486.24; seeded die mean 3.469; loss count 489). Three True lines confirm the shortcut and the scale rule (:262).")
row("L02-PROBLEMS", "2.4 problem set worked solutions", "L02.html:298-401", "PASS",
    "M1 Var = 21/100; M2 sd 15000 cents; M3 36 and 4; P1 linearity; P2 E[(X-c)^2] = Var + (mu-c)^2 expansion correct; P3 (revised, L02.html:347) gives 0 and 2 (see L02-FWD-COVARIANCE); E1-E3 consistent with lab output (489 vs 500, 3.469, scale 35/3); R1 sample variance identity; R2 Var(D)=296875 (numbers script), sd 544.8624 (by hand); R3 E=3/10, Q(1/2)=0.")
row("L02-FWD-COVARIANCE", "1.10 DAG / terms used before definition (plan: no lesson links a later definition)", "L02.html:347 (P3 solution, last sentence)", "PASS",
    "Round-1 FAIL re-verified. The solution no longer names covariance: grep -i covariance over L01.html, L02.html and L03.html finds no such token. It now says 'The general formula for Var(U + V) has an extra term that depends on how U and V move together. Lesson 4 (Proposition 1.7) gives the shortcut for that term, and Lesson 5 develops it.' That is the rewording the round-1 fix specified; Proposition 1.7 (L04.html:103-104) is the covariance shortcut. Carries no undefined term.")
row("L02-QUIZ", "2.9 quiz answers and explanations", "L02.html:421-492", "PASS",
    "q1 E=3.5; q2 Var=5-4=1; q3 Var(2X)=12; q4 Definition 2.1; q5 5000; q6 225000000; q7 21/100; q8 c=E[X]; q9 15000; q10 E[3X-1]=5. All correct; explanations match.")
row("L02-MISCONCEPTIONS", "2.9 misconceptions: labelled wrong beliefs are refuted on the page", "L02.html:279-296", "PASS",
    "The revised third misconception (:289) is correct: Var = E[X^2] - (EX)^2 agrees with E[X^2] only when E[X]=0, and the example X=-1 or 1 with probability 1/2 each gives Var = E[X^2] = 1 (numbers script). Other misconceptions refuted on the page (3.5 is not a face; 4x not 2x; sample mean is an estimate).")
row("L02-CANON", "2.2 cross-lesson claims in 'Where the canon breaks'", "L02.html:267-273 vs L06.html:158, :173 and L10.html:63-65", "PASS",
    "Bullet 2: Lesson 6 Proposition 2.6 gives infinite second moment for nu<=2 (L06.html:173) under Assumption 1 (L06.html:59). Bullet 3: E[X]=3/10 and Q(1/2)=0 for the L01 table, recomputed. Bullet 4 and 1 consistent.")
row("L02-GRADES", "2.3 grades", "L02.html:63, :105, :115, :125; key results :409-415", "PASS",
    "Props 1.2, 1.3, 2.2, 2.3, 2.4 and the key-results rows are T and each is proved on the page; Example 2.6 and the lab claims are computed or labelled SIMULATED (C in the card, see CARDS-L02).")

row("L03-PROSE", "2.2 numbers and claims in prose", "L03.html:51, :113, :138, :142, :258, :265-268, :281, :350, :382", "PASS",
    "Recomputed: gamma_3 = 8/3 and gamma_4 = 73/9 = 8.11 for p=1/10; gamma_4 = 7/3 for p=1/4; m_3 = 2157/32, m_4 = 149461/256, m_2 = 163/16, skewness 2.0730, kurtosis 5.6254; m_2=3, m_4=15, gamma_4=5/3 for the law on -2,1,3; sample gaps 0.008 and 0.045 from the printed values. Intro sentence (:51) does not list the normal result; that omission is not false and is noted only.")
row("L03-MATH", "2.4 Props 1.1, 2.2, 2.3, 2.4, Example 2.5, section 3 arithmetic", "L03.html:57-114, :138", "PASS",
    "Re-derived: Prop 1.1 (:64); Prop 2.2 (:86); Prop 2.3 (:96) with sign(a)^3 and sign(a)^4; Prop 2.4 (:106) including the equality case; Example 2.5 m3 = pq(q-p), m4 = pq(1-3pq), gamma_3=(1-2p)/sqrt(pq), gamma_4=(1-3pq)/(pq). Section 3: m3 terms -1372/512, -54/512, +1/512, +35937/512 sum to 34512/512 = 2157/32 and the 10-term alone 35937/512 minus 1425/512 (numbers script).")
row("L03-PROP28-SCOPE", "2.4 proof needs no hypothesis the statement omits (Proposition graded T)", "L03.html:127-128 (statement), :133 (proof sentence 'the standardized variable of Definition 2.1 is Z itself'), :69-72 (Definition 2.1)", "FAIL",
    "Definition 2.1 (L03.html:70-71) standardizes a variable 'on a finite probability space with positive weights'. A standard normal Z lives on no finite space (Definition 2.7 says it is the only non-finite law on the page, :123). The Proposition 2.8 proof (:133) invokes Definition 2.1 to conclude gamma_4 = E[Z^4]. The conclusion is right (numerically int z^4 phi = 3, numbers script), but the statement 'Its kurtosis is therefore gamma_4 = 3' relies on extending the kurtosis definition to a non-finite law, which the page never states.",
    "In L03.html:133 replace 'the standardized variable of Definition 2.1 is Z itself' with 'Since E[Z] = 0 and E[Z^2] = 1, Z is already standardized (mu = 0, sigma = 1), so the standardization of Definition 2.2 leaves Z unchanged and gamma_4 = E[Z^4] = 3'. State once, in Definition 2.7 or before Proposition 2.8, that for a standard normal Z the kurtosis is E[Z^4] under Definition 2.2 and that the finite-space hypothesis of Definition 2.1 is not used. Re-run check_pages and check_dag.")
row("L03-NORMAL-KURTOSIS", "2.9 plan conformance: L03 spec 'Normal kurtosis = 3 is derived, not cited' (round-1 FAIL)", "L03.html:116-134; plans/M4-build-plan.md:141", "PASS",
    "Round-1 FAIL resolved: Assumption 2.6 (:116-119) names the Gaussian facts used without proof, as BUILDER_RULES 3.3 and rule 9 require; Proposition 2.8 (:126-134) derives E[Z]=0, E[Z^2]=1, E[Z^4]=3 by oddness and two integrations by parts, each boundary term checked. I re-derived the integrations by parts by hand and numerically (int z^4 phi = 3.000000000000, numbers script). Scope and duplication defects are separate rows L03-PROP28-SCOPE and L03-STD-NORMAL-DUP.")
row("L03-STD-NORMAL-DUP", "1.10 no concept defined twice (BUILDER_RULES 1.10); verifier 2.9 'nothing defined twice'", "L03.html:121-124 (Definition 2.7) vs course/modules/M/M4/L06.html:65 (sentence 'The standard normal law is N(0,1), with density phi(z) ... A variable Z with this law is a standard normal variable') and L06.html:103 (Proposition 1.5, E[Z]=0, E[Z^2]=1)", "FAIL",
    "The standard normal law is defined twice: Definition 2.7 in L03 (new in this round) and in the L06 normal-distribution block at L06.html:65. L06 Proposition 1.5 proves E[Z]=0 and E[Z^2]=1 again, which L03 Proposition 2.8 also states. The plan's L03 spec requires the normal kurtosis to be derived in L03, so the definition cannot wait for L06; a later lesson must link the earlier definition instead of restating it.",
    "Keep one definition. Option (a, matches the plan): keep L03 Definition 2.7 and replace the standard-normal sentence at L06.html:65 with a back-reference to L03 Definition 2.7 (a later lesson may link an earlier definition); L06 Proposition 1.5 cites L03 Proposition 2.8 for the first two moments. Option (b): if the architect moves normal kurtosis to L06, delete L03 Definition 2.7, Proposition 2.8, Assumption 2.6 usage, the L03 card M4-c219 and M4-c220, and the L03 table row. The L06 change is outside slice a and must be made by the L06 owner.")
row("L03-LAB", "2.5 lab: hypothesis, output, interpretation", "L03.html:140-259; tests/labs/M4/lab-M4-L03-1.py", "PASS",
    "Twin run exit 0; 8 lines equal the expected block (incl. 2.0730, 5.6254, 64/9, 73/9, sample 2.065 and 5.580). Hypothesis (:142) predictions equal the printed exact values. Interpretation (:258) gaps 0.008 and 0.045 are correct from the printed three-decimal values; error bound 0.001 is correct for rounding.")
row("L03-CANON-MISC", "2.2 canon breaks and misconceptions", "L03.html:263-288; L10.html:150-151 (Proposition 2.3)", "PASS",
    "Bullet 1 and misconception 1: the law on -2,1,3 has mean 0, gamma_3=0 and is not symmetric (checked). Bullet 3 (:267) states the finite-moment exception correctly and cites L10 Proposition 2.3 (L10.html:150-151: E[V^4]=infinity under Assumption 1). Misconception 2 (:281): 3 is the kurtosis of the standard normal only among laws named on the page (73/9, 7/3 and 5/3 computed by the numbers script; the other named values checked by hand).")
row("L03-PROBLEMS", "2.4 problem set worked solutions", "L03.html:290-393", "PASS",
    "M1 (sigma=sqrt3/4, gamma_3=2/sqrt3, gamma_4=7/3); M2 (gamma_4=1); M3 (m3 terms); P1-P3 (P3 identity q^3+p^3=1-3pq verified); E1 gaps; E2 Bernoulli closed forms; E3 weights total 8; R1 kurtosis exactly one; R2 Bernoulli kurtosis 8.11 and no tail; R3 symmetric implies gamma_3=0, one-way implication. All correct.")
row("L03-QUIZ", "2.9 quiz answers and explanations", "L03.html:413-483", "PASS",
    "q1 m1=0; q2 E[Z^3]; q3 kurtosis 1; q4 sign flip; q5 kurtosis unchanged; q6 5/3 = 1.6667 within 0.001; q7 correct option; q8 8/3 = 2.6667 within 0.001 (gamma_3 for p=1/10, numbers script); q9 zero skewness for symmetric law. Explanations match Proposition 2.3/2.4 and R3.")
row("L03-GRADES", "2.3 grades", "L03.html:42-49, :57, :69-82, :89, :99, :109-114, :126 (Prop 2.8 T), :386-391, :401-407, :406", "PASS",
    "Props 1.1, 2.2, 2.3, 2.4, 2.8 and Example 2.5 are T; Prop 2.8 is T conditional on the named Assumption 2.6, the same form used for Assumption 1 elsewhere in M4. Key-results rows match the statements. The lab figures are labelled SIMULATED where used (E1).")

row("L04-PROSE", "2.2 numbers and claims in prose", "L04.html:52, :132, :139, :144, :169, :300, :306-308, :318-326", "PASS",
    "Example 1.9 and Example 2.5 recomputed (E[XY]=0=E[X]E[Y]; p(0,0)=1/3 vs 1/9; E[X|Y=0]=1, E[X|Y=1]=2/3, P(Y=0)=2/5, P(Y=1)=3/5, total = 4/5). 'Lesson 5 builds the correlation and the covariance matrix' matches L05.html dfn ids def-correlation and def-covariance-matrix. Canon bullet 2 marginals example checked (p(0,0)=1/2 vs 1/4).")
row("L04-MATH", "2.4 Defs 1.1-2.1, Props 1.4-1.8, 2.3-2.4, Remark 2.2, proofs", "L04.html:58-165", "PASS",
    "Prop 1.4 (:80) correct; Prop 1.5 factorization (:90-94) correct; Def 1.6 and Prop 1.7 expansion (:107-118) correct (linearity only); Prop 1.8 (:127); Prop 2.3 (:154); Prop 2.4 (:164). Definition 1.6 is used only as a formula (no result depends on its properties, as the page says).")
row("L04-LAB", "2.5 lab: hypothesis, output, interpretation", "L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py", "PASS",
    "Twin run exit 0; 18 lines equal the expected block. Revised hypothesis (:174) 'the printed cell (0,0) shows the failure' is correct: Part A prints joint 1/10 against product 4/25 for the dependent table. Other predictions (Part B covariance 0, cell 1/3 vs 1/9; Part C values) equal the output.")
row("L04-PROBLEMS", "2.4 problem set worked solutions", "L04.html:331-434", "PASS",
    "M1 dependent (0.12 vs 0.1); M2 2/3; M3 cells 1/8,1/8,3/8,3/8 and E[XY]=1/8; P1 linearity; P2 two-valued Y; P3 Cov = -ab; E1 total expectation 4/5; E2 ratio 3; E3 ratio 5/8 (numbers script); R1 Y=|X| Cov 0 and dependence; R2 Cov(X,X)=Var; R3 equal conditional expectations, dependent. All correct.")
row("L04-QUIZ", "2.9 quiz answers and explanations", "L04.html:453-528", "PASS",
    "q1 No; q2 1 (tolerance 0.0001); q3 product identity; q4 0.8; q5 dependent; q6 0 covariance; q7 total-expectation sum; q8 0.6; q9 No (R3); q10 0.06. All correct.")
row("L04-CANON-MISC", "2.2 canon breaks and misconceptions", "L04.html:303-329", "PASS",
    "Zero covariance (Example 1.9); marginals do not fix the joint table (checked); product rule fails for Y=X with +-1 (E[XY]=1, E[X]E[Y]=0, checked); conditional expectation scope (Remark 2.2). Misconceptions correct.")
row("L04-GRADES", "2.3 grades and references", "L04.html:442-447, :530-534", "PASS",
    "Props 1.4, 1.5, 1.7, 1.8, 2.3, 2.4 and Example 1.9 are T and proved on the page; no registry source is cited, consistent with the plan's Q5 and with the references section.")

# ---- cross-cutting ----
row("DAG-A", "1.10 / 2.9 DAG reading (slice a)", "index.html; L01..L04.html; check_dag output", "PASS",
    "Concept links read directly. L01: quantifiers (M1), defined random-variable and quantile-function locally. L02: limit and definite-integral (M2); random-variable (L01). L03: variance (L02), expectation (L02), random-variable (L01); skewness and kurtosis defined locally. L04: random-variable (L01), expectation (L02); independence and conditional-expectation-elementary defined locally. Cross-lesson result links are to L04 Prop 1.7 and L05 (no concept link, no definition). The standard normal law is defined in both L03 and L06; see L03-STD-NORMAL-DUP.")
row("NOTATION-A", "2.4 / 2.9 notation vs notation/notation.json", "index.html; L01..L04.html; notation/notation.json", "PASS",
    "\\R is registered (notation.json:25) and used in L01 (Definitions 1.1, 2.1, 3.1) and L05. No \\mathbb remains in slice a (grep). gamma_3 and gamma_4 are used with the registered meaning (notation.json symbols: skewness and kurtosis, 3 under normality). \\Phi is not used in slice a. phi (standard normal density) is not registered and is defined locally in L03 Assumption 2.6, which notation.json's header allows. Registry note in registry_flags.")
row("PROCESS-A", "2.9 process words and banned phrases (BUILDER_RULES 1.3-1.4)", "index.html; L01..L04.html (text, scripts stripped)", "PASS",
    "Grep over the stripped text of the five pages for TODO, TBD, lorem, beyond the scope, for brevity, details omitted, left as an exercise, you can add more, important to note, studies show, experts agree, well known, obviously, clearly, let us, we will, in this section, process words (builder, verifier, round, revised, previous, draft, placeholder, now). No hits. The math ellipses in x_1, ..., x_m are notation, not omitted content.")
row("CARDS-DUP", "2.7 full scan for duplicates (cards.json, all 212 cards)", "course/modules/M/M4/cards.json", "PASS",
    "Script " + S + "cards_scan_r2.py (run with .venv/bin/python -I): cards 212, duplicate ids [], duplicate fronts [], duplicate backs []. Per-lesson counts printed there: L01 23, L02 20, L03 22, L04 20. Ids need not be sequential (FINAL-ARCHITECT-RULINGS item 2).")
row("CARDS-L01", "2.7 cards L01 (23 cards, full read)", "cards.json ids M4-c001..c016, c173, c192-c195, c197, c198", "PASS",
    "All 23 read against L01 text. Changed cards c005 (Prop 2.2(a)), c008 (Prop 3.2), c010 (Prop 3.4 with y_1<...<y_n), c195 (Prop 2.2(b)-(c)) agree with the lesson hypotheses and locators. c007 uses Definition 3.1. No card claims a result not on the page.")
row("CARDS-L02", "2.7 cards L02 (20 cards, full read)", "cards.json ids M4-c017..c033, c181, c182, c199", "PASS",
    "All read. c029 is handled in CARD-M4-c029. c030 and c033 are grade C (SIMULATED seed results, labelled); numbers 3.469, 489, 500 appear in L02. c031 (54486.24) and c181/c182/c199 numbers appear in Examples 2.5-2.6.")
row("CARD-M4-c029", "2.7 card truth and hypotheses (round-1 FAIL)", "course/modules/M/M4/cards.json:199 (id M4-c029)", "PASS",
    "Round-1 FAIL resolved. Front 'Is Var(X) always equal to E[X^2]?' back 'No. Var(X) = E[X^2] - (E[X])^2 (Proposition 2.2), so the two agree only when E[X] = 0. For the die E[X^2] = 91/6 and Var(X) = 35/12 (Example 2.5).' Correct; numbers appear in L02.html:135-136 and :289.")
row("CARDS-L03", "2.7 cards L03 (22 cards, full read: c034-c048, c183, c200, c212, c214, c215, c219, c220)", "cards.json ids as listed", "PASS",
    "All L03-lesson cards read and checked against L03 text, including the Bernoulli, skew-law, sign and affine cards (numbers recomputed). c047 and c183 (grade C, SIMULATED) state 2.065/5.580 against 2.073/5.625 as the lab prints. c220 (kurtosis of the standard normal) matches Proposition 2.8. c219 is handled in CARD-M4-c219.")
row("CARD-M4-c219", "2.7 duplicate cards (BUILDER_RULES 1.10; verifier 2.7 'no duplicates')", "course/modules/M/M4/cards.json:1493-1499 (id M4-c219) vs cards.json:589-593 (id M4-c084, L06)", "FAIL",
    "M4-c219 'What is a standard normal random variable?' restates the standard normal definition already on M4-c084 ('What is the normal distribution N(mu, sigma^2)?', whose back gives the standard normal density phi(z) = e^(-z^2/2)/sqrt(2 pi), Definition 1.1 of L06). Same fact, same concept, two cards; this is the card-side of L03-STD-NORMAL-DUP.",
    "Delete card M4-c219 from cards.json (its definition is covered by M4-c084), or, if the L03 definition is kept and L06's is removed, delete M4-c084 instead and keep M4-c219. Keep M4-c220. Re-run check_pages (it validates card numbers against lesson text).")
row("CARDS-L04", "2.7 cards L04 (20 cards, full read: c049-c066, c201, c204)", "cards.json ids as listed", "PASS",
    "All read against L04 text. c058 (Example 1.9), c061 (Prop 2.4), c063 (section 3), c064 (P3: Cov = -ab), c066 (R2) and c204 (R3) agree with the lesson.")
row("CARDS-NUMBERS", "2.7 card numbers appear in their lesson", "cards.json (L01-L04 cards)", "PASS",
    "Every number on the L01-L04 cards (for example 198, 149, 3/5, 91/6, 35/12, 489, 3.469, 2.065, 5.580, 73/9, 7/3, 163/16, 2157/32, 149461/256, 1/9, 3/50) appears in the same lesson's text or lab output.")
row("MUTANTS-A", "2.6 mutation testing (project graders only)", "ledgers/M4/mutants/ (not in slice a)", "PASS",
    "Slice a has no project grader (grader/ and project.html are outside it); the ruling in the verifier brief limits mutation testing to project graders. No mutants written for slice a; none listed. Lab twins are demonstrations.")
row("NUMBERS-A", "2.2 / 2.4 re-derivation of every number on slice a (own script)", S + "m4a_r2_numbers.py", "PASS",
    "Run: .venv/bin/python -I " + S + "m4a_r2_numbers.py -> 'OK 86  BAD 0' plus the numeric Gaussian integrals int phi = 1, int z^2 phi = 1, int z^4 phi = 3 to 1e-9. Covers Example 2.5 closed forms, section 3 and section 4 moments, the L01 CDF and quantile table, the L02 die and loss, the L02 P3 counterexample, the L04 tables and their conditional expectations, and the hub arithmetic.")

fragment = {
    "unit": "M4",
    "slice": "a",
    "round": 2,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyD2-M4-a)",
    "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "base": "d0f39c09598ffefaf0ec18d5d1077cfacd42998b",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-M4-a",
    "scratch": "ledgers/M4/scripts/M4-a-r2/",
    "verified_at": "2026-11-02T22:10:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "notation/notation.json does not register phi, the standard normal density used in L03 Assumption 2.6 and L06; phi is also the characteristic function phi_X in L07 and L09. Registry owner to decide one symbol for each.",
    ],
    "freshness_flags": [],
    "notes": "Round 2 of slice a (index.html, L01-L04, lab twins, and the L01-L04 cards). Delta read: d0f39c09..c737272 touches index.html (L03 card), L01 (10 lines: \\R macro, Definition 3.1 pointer), L02 (4 lines: misconception, P3), L03 (32 lines: Assumption 2.6, Definition 2.7, Proposition 2.8, canon, table, footer), L04 (1 line: lab hypothesis), cards.json (wording, c029, c195, c005, c008, c010; c211 and c213 removed; c219 and c220 added). Round-1 rows L02-FWD-COVARIANCE, L03-NORMAL-KURTOSIS and CARD-M4-c029 were re-verified from scratch: the first two PASS, the third PASS. Every row whose subject changed was re-verified. Carried: A-G10 live verify_refs (references.json byte-identical since d0f39c09). Not checked: Blitzstein's text (no access; the pages attribute nothing to it), the 2nd-edition claim against the book, whether a newer printing exists, live Crossref in round 2, and real Pyodide (page_smoke ran in the playwright browser, as in round 1). Lab runtime 0.0 s per page in page_smoke; no runtime claim in the pages is above 10 s. Not required by the slice rules and not failed: BUILDER_RULES 3.4 asks for a lab numerical check of every key formula; L03 has labs for Example 2.5 and section 3 only, so Props 2.3, 2.4 and 2.8 have no lab check (verified here by script instead). Two L03 prose items are noted but not failed: the why-it-matters paragraph (L03.html:51) and the meta description (L03.html:7) do not mention the normal result, which is not a false statement.",
    "summary": "",
}
n = len(R)
fail = [r for r in R if r["status"] == "FAIL"]
passn = [r for r in R if r["status"] == "PASS"]
fragment["summary"] = (
    f"Slice a round 2: {len(passn)} PASS, {len(fail)} FAIL, 0 UNVERIFIABLE across {n} rows. "
    "FAIL rows: L03-PROP28-SCOPE (Proposition 2.8 proof applies Definition 2.1 outside its finite-space hypothesis), "
    "L03-STD-NORMAL-DUP (standard normal law defined in L03 Definition 2.7 and in L06.html:65, BUILDER_RULES 1.10), "
    "CARD-M4-c219 (card restates the standard normal definition of M4-c084). "
    "Round-1 FAIL rows L02-FWD-COVARIANCE, L03-NORMAL-KURTOSIS and CARD-M4-c029 re-verified and now PASS. "
    "All gates passed on c737272: check_pages, check_dag, check_projects, run_labs 13/13, twins alone under python -I -W error, page_smoke, ruff, mypy, six pytest modules, verify_refs --offline."
)
out = ROOT / "ledgers/M4/M4-a.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", n, "pass", len(passn), "fail", len(fail))
