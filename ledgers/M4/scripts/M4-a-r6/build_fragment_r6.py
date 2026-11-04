"""Build ledgers/M4/M4-a.json (round 6, slice a) from the rows verified in this round.

Run from the checkout root: .venv/bin/python ledgers/M4/scripts/M4-a-r6/build_fragment_r6.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

G = "ledgers/M4/scripts/M4-a-r6/gates/"
P = "course/modules/M/M4/"

rows = [
    # ---- gates run on the pin (142ecfc2) ----
    {"id": "A-G01", "check": "2.9 structure: check_pages --unit M4 (slice pages and unit)", "location": P + "index.html, L01.html..L04.html",
     "status": "PASS", "evidence": f"{G}check_pages.log: 'check_pages M4: PASS', exit 0 (run this round)."},
    {"id": "A-G02", "check": "2.9 DAG: check_dag --unit M4", "location": P + "index.html, L01.html..L04.html",
     "status": "PASS", "evidence": f"{G}check_dag.log: 'check_dag M4: PASS', exit 0. The tool does not read prose; the prose forward references are row DAG-A."},
    {"id": "A-G03", "check": "2.6 projects gate, unit-wide (outside slice a; recorded because the rules name it)", "location": P + "project.html",
     "status": "PASS", "evidence": f"{G}check_projects.log: 'check_projects M4: PASS', exit 0."},
    {"id": "A-G04", "check": "2.5 labs: run_labs --unit M4", "location": "tests/labs/M4/lab-M4-L01-1.py..lab-M4-L04-1.py",
     "status": "PASS", "evidence": f"{G}run_labs.log: 'run_labs M4: PASS (13/13)', exit 0."},
    {"id": "A-G05", "check": "2.5 twins alone under python -I -W error; page code equals twin; expected block equals stdout",
     "location": "tests/labs/M4/lab-M4-L01-1.py..L04-1.py; " + P + "L01.html..L04.html",
     "status": "PASS", "evidence": "ledgers/M4/scripts/M4-a-r6/twins_r6.py (run: .venv/bin/python -I ledgers/M4/scripts/M4-a-r6/twins_r6.py <checkout>): each twin exit 0, empty stderr, code_equals_twin=[True], expected_equals_stdout=[True] for L01 (20 lines), L02 (10), L03 (8), L04 (18); 'twins PASS'."},
    {"id": "A-G06", "check": "2.9 page_smoke (slice pages, alone)", "location": P + "index.html, L01.html..L04.html",
     "status": "PASS", "evidence": f"{G}page_smoke_slice.log: 'page_smoke M4: PASS', exit 0 (L01..L04 each PASS; each lab under 1 s)."},
    {"id": "A-G07", "check": "gate: ruff check . (repository)", "location": "repository",
     "status": "PASS", "evidence": f"{G}ruff_check.log: 'All checks passed!', exit 0. Also ruff check tests/labs/M4/ exit 0."},
    {"id": "A-G08", "check": "gate: ruff format --check . (repository; not an M4 file)",
     "location": "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3",
     "status": "FAIL",
     "evidence": f"{G}ruff_format.log: '1 file would be reformatted', exit 1. The file is unchanged since its last commit a007712f (git diff 142ecfc2 empty for it). Same finding as round 5 A-G08. Slice files pass: ruff format --check on tests/labs/M4/lab-M4-L01..L04 -> '4 files already formatted', exit 0.",
     "fix": "Run ruff format on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py (owner: M3 or repo maintainer; the verifier does not edit it)."},
    {"id": "A-G09", "check": "gate: mypy strict (mypy --no-incremental)", "location": "repository (331 source files)",
     "status": "PASS", "evidence": f"{G}mypy.log: 'Success: no issues found in 331 source files', exit 0."},
    {"id": "A-G10", "check": "gate: relevant pytest", "location": "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py, test_page_smoke.py, test_curriculum.py",
     "status": "PASS", "evidence": f"{G}pytest_relevant.log: all dots, exit 0 (-q -p no:cacheprovider)."},
    {"id": "A-G11", "check": "2.1 citations: verify_refs --offline, and verify_refs --unit M4 (live Crossref)", "location": "references/references.json (blitzstein2019introduction); tools/verify_refs.py",
     "status": "PASS", "evidence": f"{G}verify_refs.log: 'offline integrity: 560 entries, 0 problems'. {G}verify_refs_live_M4.log: 'live re-verification of M4: 1 of 560 entries, 0 problems', exit 0. Plain curl of https://api.crossref.org/works/10.1201/9780429428357 (ledgers/M4/scripts/M4-a-r6/crossref_blitzstein.json): edition-number 2, ISBN 9780429428357, publisher Chapman and Hall/CRC, published 2019-02-08, type book."},
    {"id": "A-G12", "check": "scope: delta since previous pin 440ed3c8, every hunk in slice a read", "location": P + "L01.html:270; L02.html:51; L03.html:122, :262, :276, :401, :482, :493; cards.json (c014, c015, c032, c036, c037, c201, c219 removed, c220, c233 merged into c201)",
     "status": "PASS", "evidence": "git diff 440ed3c8 142ecfc2 -- course/modules/M/M4/L01..L04.html index.html tests/labs/M4: the only slice-file hunks are L01 interpretation line 270, L02 why-it-matters line 51, L03 Proposition/Assumption renumbering (2.8 -> 2.7 at :122, :262, :276, :401, :482, :493), and the cards hunk. Twins and index.html are byte-identical since 440ed3c8. Each hunk was read and re-verified (see rows L01-PROSE, L02-PROSE, L03-PROSE, CARDS-L03, CARD-M4-c219)."},
    {"id": "A-G13", "check": "2.1/2.8 generated-artefact gates: build_site --check, fetch_data --check, render_curriculum (no diff)", "location": "tools/build_site.py; tools/fetch_data.py; tools/render_curriculum.py; curriculum/curriculum.json; CURRICULUM.md",
     "status": "PASS", "evidence": f"{G}build_site_check.log: 'site data current: 6 outputs'. {G}fetch_data_check.log: 'fetch_data: 3 datasets, 0 problems'. {G}render_curriculum.log: 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'; git status afterwards shows no change to curriculum/curriculum.json or CURRICULUM.md."},

    # ---- hub index.html ----
    {"id": "A-H01", "check": "2.9 structure: hub section order and minimum counts (BUILDER 4)", "location": P + "index.html",
     "status": "PASS", "evidence": "index.html sections in order: header, objectives (6 items), prerequisites, placement (10 items), lessons (10 cards), ladder (4 rungs), data, reading. check_pages PASS (A-G01)."},
    {"id": "A-H02", "check": "2.9 hours arithmetic: hub split vs lesson hours", "location": P + "index.html:29, :40, :42; L01..L10 data-hours",
     "status": "PASS", "evidence": "data-hours-lessons=90, data-hours-project=30; grep data-hours: L01..L10 each 9 (10 x 9 = 90). 90 + 30 = 120 = curriculum.json M4 hours 120. 30/120 = 25% matches the bar widths 75%/25% (index.html:40). Project data-hours-project=30 (project.html)."},
    {"id": "A-H03", "check": "2.9 objectives: measurable verbs, each mapped to a lesson", "location": P + "index.html:49-54",
     "status": "PASS", "evidence": "Six objectives with verbs Compute, Derive, Compute, Decide/show/compute, Derive, State/decide. Each maps to a lesson whose content was read: Lesson 1 (quantile convention, Prop 3.2), Lesson 2 (shortcut, scale rule, cents), Lesson 3 (zero skewness, Prop 2.4), Lessons 4-5 (independence, Example 1.9, covariance matrix), Lesson 6 (Prop 2.6), Lessons 9-10 (LLN/CLT hypotheses, lab output, not re-read here: other slices)."},
    {"id": "A-H04", "check": "2.6 prerequisites vs curriculum", "location": P + "index.html:35, :60-64; curriculum.json M4, M2, M1 entries",
     "status": "PASS", "evidence": "curriculum: M4 prereqs ['M2'], M2 prereqs ['M1'], M1 prereqs ['P0.1']; titles 'Single & Multivariable Calculus' (M2) and 'Precalculus & Mathematical Reasoning' (M1) match index.html:35. 'Linear algebra is not a prerequisite' consistent with the M4 entry (no M3)."},
    {"id": "A-H05", "check": "2.2/1.10 hub claim: matrix results proved from the quadratic form, which Lesson 5 defines", "location": P + "index.html:62, :64; L05.html (quadratic-form statement)",
     "status": "PASS", "evidence": "L05.html Section 2 states w^T Sigma w = Var(sum w_i X_i) >= 0 and symmetry of Sigma; index.html:62 says Lesson 5 defines the quadratic form, which is accurate as a statement in L05. No M3 concept is linked (grep data-concept in index.html: limit, definite-integral, exponential-and-logarithm, quantifiers only)."},
    {"id": "A-H06", "check": "2.9 placement diagnostic: items, bar, skill checks (BUILDER 5.1)", "location": P + "index.html:68-141",
     "status": "PASS", "evidence": "Ten items: eight M1/M2 prerequisite items (Q1-Q8) and two data-skill items (rung 1 and rung 2). data-mastery=0.8 = eight of ten. Two data-skill items present (BUILDER 5.1 requires at least two). Text at :70 and :164 states the skip rule as bar AND both skill checks, which is the BUILDER 5.1 rule (BUILDER_RULES.md, 'A placement pass means meeting the hub quiz's data-mastery bar and answering every item marked data-skill')."},
    {"id": "A-H07", "check": "3 attribution: 'M1 Theorem 3.1' in the first placement explanation", "location": P + "index.html:79; course/modules/M/M1/L01.html:79-82",
     "status": "PASS", "evidence": "M1/L01.html:79 'Theorem 3.1 (negating one quantifier)': neg(for all x P(x)) iff exists x not P(x), and neg(exists x P(x)) iff for all x not P(x). Explanation at index:79 matches."},
    {"id": "A-H08", "check": "2.2 numbers in placement answers and explanations", "location": P + "index.html:75-140",
     "status": "PASS", "evidence": "Recomputed: negation (Q1) 'some student has not passed'; limit 1/n -> 0 (Q2); int_0^1 x dx = 0.5 (Q3, tol 0.001); d/dt e^{rt}=r e^{rt} (Q4); ln(e^3)=3 (Q5); 1+1/2+1/4+1/8=1.875 (Q6, (15/16)/(1/2)=15/8); discount factor 1/(1+r) (Q7); d/dx(x^2 y)=2xy (Q8). Rung 1: F(0)=1/4<1/2<=F(1)=3/4 so 0.5 quantile = 1 (answer 1). Rung 2: nu=5, Var=5/3 (L06.html:158 Prop 2.6 nu/(nu-2)); s^2=3/5=0.6. All keys match the data-answer attributes."},
    {"id": "A-H09", "check": "2.2/2.4 rung-2 skill check hypothesis and its sources", "location": P + "index.html:138-140; L06.html:158-159 (Prop 2.6, Assumption 1); L02.html:115-117 (Prop 2.3)",
     "status": "PASS", "evidence": "L02 Proposition 2.3 is stated for a finite probability space (so the hub correctly says it does not cover the Student-t, which has infinitely many values). L06 Proposition 2.6 gives Var = nu/(nu-2) for nu > 2 under Assumption 1. The hub labels the scale rule as a hypothesis."},
    {"id": "A-H10", "check": "2.7/2.9 hub lesson map and cards agree with the lessons", "location": P + "index.html:148-159; L01..L10 h1 and data-hours",
     "status": "PASS", "evidence": "Card titles match the h1 of L01 (Random Variables, Distributions and Quantiles), L02 (Expectation and Variance), L03 (Skewness and Kurtosis), L04 (Independence and Conditional Expectation (Elementary)), L05 (Covariance, correlation and the covariance matrix), L06 (Normal and Student-t distributions), L07 (Moment-generating and characteristic functions), L08 (The Multivariate Normal), L09 (Laws of Large Numbers and the Central Limit Theorem), L10 (Heavy Tails and Infinite Variance). L01..L04 card bodies checked against the lesson text in this round. L05..L10 card bodies: headings and lab descriptions checked only (L05..L10 belong to other slices)."},
    {"id": "A-H11", "check": "2.6 ladder: four rungs in order; the placement skip rule agrees between hub and project.html",
     "location": P + "index.html:70, :164 vs " + P + "project.html:42",
     "status": "FAIL",
     "evidence": "index.html:164 and :70: skip rungs 1-2 only if the placement bar is met AND both skill checks are answered. project.html:42 reads 'If you met the placement bar on the module page, skip rungs 1 and 2 and start at rung 3.' That omits the skill-check condition. BUILDER_RULES.md section 5.1 (lines 191-195) requires bar AND every data-skill item. Rung names and order agree (index.html:166-169 vs project.html:44-47; project Lab 1 = worked example, project Lab 2 = completion problem, quantile_99 and matched_scale names match tests/labs/M4/lab-M4-project-1.py).",
     "fix": "Change project.html:42 to: 'If you met the placement bar on the module page and answered both skill checks there, skip rungs 1 and 2 and start at rung 3.' (project.html is outside slice a; its owner must make the edit.)"},
    {"id": "A-H12", "check": "2.8 data status and SIMULATED labels", "location": P + "index.html:37, :175, :187",
     "status": "PASS", "evidence": "grep open(, data/ and urllib/requests in tests/labs/M4/lab-M4-L01..L04-1.py and project labs: no file or network reads. Seeded samples are labelled SIMULATED in L02 (lab hypothesis, :146) and L03 (:137). The curriculum sources list names only Blitzstein."},
    {"id": "A-H13", "check": "2.1 reading list and citation: blitzstein2019introduction", "location": P + "index.html:181-183; references/references.json:3127-3170",
     "status": "PASS", "evidence": "Registry record: year 2019, years [2019], isbn [9780429428357], publisher 'Chapman and Hall/CRC', no edition field, source string 'Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)', used_by M4. index.html:183 states exactly this, and states that the edition is taken from the curriculum and not checked against the book. Crossref (plain curl, A-G11) reports edition-number 2, consistent with that statement. No passage from the book is read or attributed."},
    {"id": "A-H14", "check": "2.6 curriculum facts for the hub: no debate, no Atlas milestone, part and tier", "location": P + "index.html:2, :31, :37; curriculum.json M4 entry; atlas/",
     "status": "PASS", "evidence": "curriculum M4 entry: tier F, hours 120, part M; parts list gives M = 'Mathematics'. M4 entry has no 'debate' value (None; M1 is None too). grep -rl M4 atlas/ returns nothing. Hub meta: 'Tier F · 120 hours · Part M, Mathematics' matches."},
    {"id": "A-H15", "check": "2.9 hub footer", "location": P + "index.html:187",
     "status": "PASS", "evidence": "Footer states seeded samples are SIMULATED and no real data is used. Consistent with A-H12."},

    # ---- L01 ----
    {"id": "L01-PROSE", "check": "2.9 prose: why-it-matters (<=120 words), definitions, claims about the lab", "location": P + "L01.html:51, :55-69, :95-99, :114-135, :270, :277-297, :360-370",
     "status": "PASS", "evidence": "why-it-matters = 114 words (python word count). Definitions 1.1, 1.2, 2.1, 3.1 match the proofs. Interpretation at :270 (changed this round) says the scan equals the definition 'at those 100 points only' and that Q moves to the next support value above F(x). The lab output (twins_r6.py) confirms both claims. Example 3.5 (148.5 -> 149) and Example 3.6 values re-derived."},
    {"id": "L01-MATH", "check": "2.4 mathematics: Prop 2.2, Prop 3.2, Remark 3.3, Prop 3.4, Examples 3.5-3.6 re-derived", "location": P + "L01.html:57-135",
     "status": "PASS", "evidence": "Re-derived: F values -> 1/10, 3/10, 3/5, 4/5, 9/10, 1; Q(1/20)=-2, Q(1/10)=-2, Q(11/100)=-1, Q(1/2)=0, Q(3/5)=0, Q(61/100)=1, Q(9/10)=2, Q(91/100)=3, Q(99/100)=3, Q(1)=3 (matches lab output). Prop 2.2(d) jump = p_k. Remark 3.3 left-continuity proof (u_n in (F_{k-1}, p]) correct. Prop 3.4 index ceil(pn) with F_j=j/n correct. Each proof uses only earlier results."},
    {"id": "L01-LAB", "check": "2.5 lab: hypothesis, code, expected block, interpretation", "location": P + "L01.html:138-270; tests/labs/M4/lab-M4-L01-1.py",
     "status": "PASS", "evidence": "Page code equals twin (twins_r6.py: code_equals_twin=[True]). Expected block equals stdout (expected_equals_stdout=[True], 20 lines). Lab hypothesis at :140 predicts the printed quantiles and the 100-of-100 counts, matching the output. Docstring claims ('exact fractions', 'checks ... on 100 grid points', 'prints Q at F(x) and just above') match the code."},
    {"id": "L01-PROBLEMS", "check": "2.4 problem set: worked solutions re-derived", "location": P + "L01.html:302-405",
     "status": "PASS", "evidence": "M1 (F and Q(1/2)=0 for the parity variable), M2 (F(5)=7/10, Q(7/10)=5, Q(71/100)=7), M3 (ceil(36)=36, ceil(36.04)=37), P1-P3, E1 (Q(99/100)=3 from F(2)=9/10), E2 (Q(3/5)=0, Q(3/5+eps)=1), E3 (100 of 100 count), R1 (strict convention: Q^s(3/5)=1), R2, R3 all re-derived and correct."},
    {"id": "L01-QUIZ", "check": "2.4 quiz: keys and explanations", "location": P + "L01.html:424-494",
     "status": "PASS", "evidence": "Nine items: correct options Q(1/2)=1 for (1/4,1/2,1/4); 1 for Q(61/100); distribution function is not continuous at x_k (Prop 2.2(d)); 198 and 149 (ceil); Q(F_k)=x_k; P(X<=1)=5/6=0.833 (tol 0.0005); random variable = function; Q(1)=x_m. All keys correct."},
    {"id": "L01-GRADES", "check": "2.3 grades: T for proved claims; no lab-derived claim graded T", "location": P + "L01.html:43-48, :80, :103, :114, :119, :413-418",
     "status": "PASS", "evidence": "Props 2.2, 3.2, Remark 3.3, Prop 3.4 graded T and proved on the page. Example values computed exactly. The lab outputs are restated as exact (not graded C) because they are exact computations of a stated table (BUILDER 4)."},
    {"id": "L01-FWD", "check": "2.9/1.10 forward references in L01", "location": P + "L01.html:37, :51, :95",
     "status": "PASS", "evidence": "L01 cites only M1 (quantifiers) and its own sections; no later-lesson pointer (grep Lesson N in L01: only 'Lesson 1 of 10' eyebrow)."},

    # ---- L02 ----
    {"id": "L02-PROSE", "check": "2.9 prose: why-it-matters (changed this round, <=120 words), definitions", "location": P + "L02.html:51, :55-101, :147, :262",
     "status": "PASS", "evidence": "why-it-matters = 105 words; the changed sentence says Lab 1 checks the shortcut on a die and a two-point loss and the scale rule on the die. That matches the lab (twins_r6.py L02: 'definition and shortcut agree' lines and 'Var(2X) ... True' line are for the die)."},
    {"id": "L02-MATH", "check": "2.4 mathematics: Defs 1.1, 2.1; Props 1.2, 1.3, 2.2, 2.3, 2.4; Examples 1.4, 1.5, 2.5, 2.6 re-derived", "location": P + "L02.html:57-142",
     "status": "PASS", "evidence": "Die: E=7/2, E[X^2]=91/6, Var=35/12, sd=1.708 (sqrt(35/12)=1.70783). Loss: E=12500, E[L^2]=3125000000, Var=2968750000, sd=54486.2368 -> 54486.24. Scale: Var(2X)=35/3=4*35/12. Prop 2.2 proof: E[(X-mu)^2]=E[X^2]-2mu^2+mu^2. All re-derived."},
    {"id": "L02-LAB", "check": "2.5 lab: hypothesis, code, expected block, interpretation", "location": P + "L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py",
     "status": "PASS", "evidence": "twins_r6.py: code equals twin; stdout equals expected block (10 lines); exit 0; stderr empty. Seeded values reproduced: die mean 3.469 (variance 2.902), mean minus 7/2 = -0.031; loss 489 losses, total 122250000 cents, mean 12225.0, variance 2906799375.0 (= 250000^2 * p(1-p) with p = 489/10000, checked). Interpretation at :262 numbers (0.031, 489, 12225.0) match."},
    {"id": "L02-PROBLEMS", "check": "2.4 problem set: worked solutions re-derived", "location": P + "L02.html:298-401",
     "status": "PASS", "evidence": "M1 Var=21/100; M2 mean 5000, Var 2.25e8, sd 15000; M3 36 and 4; P1-P3 proofs correct (P3: Var(U+V)=0 vs 2); E1-E3 numbers (3.469, -0.031, 489 vs 500 i.e. 11 below, 35/3); R1 sample variance identity; R2 Var(D)=296875, sd 544.8624 (= 54486.24/100, checked); R3 expectation 3/10 and Q(1/2)=0."},
    {"id": "L02-QUIZ", "check": "2.4 quiz: keys and explanations", "location": P + "L02.html:421-492",
     "status": "PASS", "evidence": "Ten items with correct keys: 3.5; Var=1 (5-4); Var(2X)=12; Definition 2.1; 5000; 2.25e8; 21/100; c=E[X]; 15000; E[3X-1]=5."},
    {"id": "L02-MISC", "check": "2.9 misconceptions: three or more, each with the wrong belief and the correction", "location": P + "L02.html:279-296",
     "status": "PASS", "evidence": "Four misconceptions. The variance = E[X^2] claim: the two agree only when E[X]=0 (Prop 2.2 gives E[X^2]-Var = mu^2), for X = +-1 both equal 1. Die numbers 15.17 and 2.92 re-derived (91/6, 35/12)."},
    {"id": "L02-CANON", "check": "2.4 canon section: finite-law scope, the mean vs the quantile, squared units", "location": P + "L02.html:267-273 vs L06.html:158-159 (Prop 2.6), L01.html:135 (Example 3.6)",
     "status": "PASS", "evidence": "E[X] = 3/10 for the L01 Example 3.6 table re-derived ((-2-2+0+2+2+3)/10). Claim that Prop 2.6 of L06 gives no finite variance for nu <= 2 is accurate (L06.html:158-159). The Lesson-6 and Lesson-10 pointer in the same sentence is a DAG issue, recorded in DAG-A."},
    {"id": "L02-FWD-COVARIANCE", "check": "1.10/2.9 L02 Problem P3 uses a result from Lesson 4 and Lesson 5 before they are introduced", "location": P + "L02.html:347",
     "status": "FAIL",
     "evidence": "L02.html:347: 'Lesson 4 (Proposition 1.7) gives the shortcut for that term, and Lesson 5 develops it.' Lesson 4 Proposition 1.7 is the covariance shortcut (L04.html:103-104); the covariance concept is introduced in L04 (Definition 1.6), later than L02. M4-build-plan.md:113 says 'No lesson links a later definition'. The counterexample itself (V = -U, Var(U+V)=0 vs 2) is correct. M4-open-items.md item 2 records the builder's intention to change this pointer if L05 does not state the formula.",
     "fix": "Delete the forward pointer, or move the sentence to L04 (after Prop 1.7). Keep the counterexample (it needs only Props 2.2 and 2.4 of L02)."},
    {"id": "L02-FOOTER-SCOPE", "check": "2.9 footer and references scope", "location": P + "L02.html:496-507",
     "status": "PASS", "evidence": "References: 'Each exact result ... is proved on the page or is an exact computation on a stated list of values. The seeded samples ... are SIMULATED single-run estimates.' Footer repeats this. Consistent with the lab."},

    # ---- L03 ----
    {"id": "L03-PROSE", "check": "2.9 prose: why-it-matters (<=120 words), definitions 2.1-2.2, Prop 1.1, Prop 2.2 proof", "location": P + "L03.html:51, :55-86",
     "status": "PASS", "evidence": "why-it-matters = 97 words. Def 2.2: kurtosis E[Z^4] without subtracting 3, stated. Prop 2.2 proof: E[Z^j]=E[(X-mu)^j]/sigma^j. Prop 2.3 proof: Z_Y = sign(a) Z_X, cubes change sign, fourth powers do not. Prop 2.4 proof: W=Z^2, Var(W)=gamma4-1, equality case gives Z=+-1 and P(Z=1)=1/2."},
    {"id": "L03-MATH", "check": "2.4 mathematics: Example 2.5 closed forms, section 3 central moments, section 4 counterexample, Prop 2.7 normal kurtosis", "location": P + "L03.html:110-128, :133, :260, :276",
     "status": "PASS", "evidence": "Re-derived with fractions: mu=7/4, m2=163/16, m3=34512/512=2157/32 (terms -1372, -54, +1, +35937 over 512, sum 34512), m4=1195688/2048=149461/256; gamma3^2 = 18610596/4330747, gamma3 = 2.0730, gamma4 = 149461/26569 = 5.6254. Bernoulli: gamma3=(1-2p)/sqrt(pq); p=1/10 -> 8/3 and 73/9 (8.11); p=1/4 -> 7/3. Section 4 law -2,1,3 with 2/5,1/2,1/10: mean 0, gamma3 = 0, m2=3, m4=15, gamma4=5/3. Prop 2.7: integration by parts E[Z^2]=1, E[Z^4]=3 under Assumption 2.6 (boundary terms vanish). p=(1-1/sqrt3)/2 gives pq=1/6 and gamma4=3."},
    {"id": "L03-LAB", "check": "2.5 lab: hypothesis, code, expected block, interpretation", "location": P + "L03.html:135-254; tests/labs/M4/lab-M4-L03-1.py",
     "status": "PASS", "evidence": "twins_r6.py: code equals twin; stdout equals expected block (8 lines); exit 0. Printed: 163/16, 2157/32, 149461/256, 18610596/4330747, skewness 2.0730, kurtosis 5.6254, Bernoulli closed forms True, sample skewness 2.065 and kurtosis 5.580 (seed 2026, n=20000), exact 2.073 and 5.625. The interpretation gaps 0.008 and 0.045 match the printed values; rounding bound 0.001 is correct."},
    {"id": "L03-NUMBERING", "check": "2.9 numbering: each block number in the lesson is unique and sequential (one counter per section, as in L01 and L02)",
     "location": P + "L03.html:70 (Definition 2.1), :75 (Definition 2.2), :80 (Proposition 2.2), :90 (Prop 2.3), :100 (Prop 2.4), :110 (Example 2.5), :117 (Assumption 2.6), :122 (Prop 2.7)",
     "status": "FAIL",
     "evidence": "Section 2 numbers are 2.1, 2.2 (Definition), 2.2 (Proposition), 2.3, 2.4, 2.5, 2.6, 2.7. 'Definition 2.2' and 'Proposition 2.2' are two different blocks with the same number. With one counter per section (the convention of L01 and L02, where Definition 2.1, Proposition 2.2, Proposition 2.3 ... share one sequence), the Proposition after Definition 2.2 would be 2.3, and so on. Round 5's gap (2.6 then 2.8) was closed by renumbering 2.8 to 2.7, which removed the gap and kept the duplicate. In-text references to 'Proposition 2.2' (:71, :106, :111, :133, :253, :309, :325, :397) are unambiguous only by the word 'Proposition'.",
     "fix": "Renumber the section 2 blocks in one sequence: Def 2.1, Def 2.2, Prop 2.3 (standardized moments), Prop 2.4 (affine), Prop 2.5 (kurtosis at least 1), Example 2.6 (Bernoulli), Assumption 2.7, Prop 2.8 (normal kurtosis). Update every in-text reference in L03, the key-results table, and the cards that cite these numbers (cards.json: M4-c038, c039, c040, c041, c046, c214, c215, c220, c225, c226, c229 and the Prop 2.2 citations). Then re-run check_pages, check_dag and the twin check."},
    {"id": "L03-STD-NORMAL-DUP", "check": "2.9 duplication: the standard normal law is defined once (L06 Definition 1.1), with a pointer in L03", "location": P + "L03.html:118, :123; L06.html:64-65",
     "status": "PASS", "evidence": "L03 does not restate the density; L06.html:65 gives the normal density and the standard normal law. The defect in use-before-definition is recorded in DAG-A, not as a duplicate."},
    {"id": "L03-PROP28-SCOPE", "check": "2.4 scope: Prop 2.7 names Assumption 2.6 wherever its result is used", "location": P + "L03.html:122-123, :149, :163, :288, :369, :380, :401, :493",
     "status": "PASS", "evidence": "Every use of the normal kurtosis (Prop 2.7) is accompanied by 'under Assumption 2.6' or 'Assuming Assumption 2.6' (lines 123, 149 'Proposition 2.7, whose moments are integrals and are finite only under Assumption 2.6', 163, 288, 369, 380, 401, 493). Assumption 2.6 lists the facts used without proof: evenness, normalization, finiteness of |z|^k phi, the derivative identity."},
    {"id": "L03-CANON", "check": "2.4 canon section: symmetry vs zero skewness, kurtosis not peakedness, finiteness, sample is an estimate", "location": P + "L03.html:258-265",
     "status": "PASS", "evidence": "Example in the first bullet re-derived (mean 0, gamma3=0, gamma4=5/3, not symmetric). Second bullet: Prop 2.4 gives >=1; Bernoulli p=1/10 gives 73/9 with two values. Third bullet: Lesson 10 pointer and Student-t nu=3 infinite fourth moment, not verified here (L10 belongs to another slice); the pointer is recorded in DAG-A."},
    {"id": "L03-MISC", "check": "2.9 misconceptions: three or more", "location": P + "L03.html:270-282",
     "status": "PASS", "evidence": "Three misconceptions: zero skewness = symmetric (corrected by the section 4 law); kurtosis of every law is 3 (Bernoulli 73/9 and 7/3; p=(1-1/sqrt3)/2 gives 3); sign reversal (Prop 2.3, sign(a)^4 = 1). All correct."},
    {"id": "L03-PROBLEMS", "check": "2.4 problem set: worked solutions re-derived", "location": P + "L03.html:286-388",
     "status": "PASS", "evidence": "M1 (p=1/4: sigma=sqrt3/4, gamma3=2/sqrt3=1.155, gamma4=7/3); M2 (0/2 law, gamma4=1); M3 (m3=2157/32); P1-P3 proofs correct; E1 gaps 0.008 and 0.045; E2 64/9 and 73/9; E3 weights total 8; R1 equality case; R2 gamma4 of Bernoulli 8.11 and no tail beyond two values; R3 symmetric law gamma3=0."},
    {"id": "L03-QUIZ", "check": "2.4 quiz: keys and explanations", "location": P + "L03.html:408-478",
     "status": "PASS", "evidence": "Nine items: m1=0; skewness is E[Z^3]; kurtosis of the symmetric two-point law 1; Y=-X changes sign; kurtosis unchanged under 5X+3; 5/3 = 1.6667; the law of -2,1,3 has zero skewness and is not symmetric; Bernoulli p=1/10 skewness 8/3 = 2.6667 (0.8/0.3); symmetric law has zero skewness. All keys correct."},
    {"id": "L03-GRADES", "check": "2.3 grades: T for proved claims; the simulated sample is graded C where it is read", "location": P + "L03.html:42-49, :57-134, :401-407",
     "status": "PASS", "evidence": "Prop 2.2-2.7 and Example 2.5 graded T and proved on the page. Sample skewness 2.065 and kurtosis 5.580 are not restated as T anywhere; cards c047 and c183 grade them C with basis 'Lab 1 (SIMULATED), seed 2026'."},
    {"id": "L03-FOOTER-SCOPE", "check": "2.9 footer and references scope", "location": P + "L03.html:480-493",
     "status": "PASS", "evidence": "References and footer state that the seeded sample is a SIMULATED single-run estimate and that the normal kurtosis is proved only under Assumption 2.6, which is used without proof and cited to no source."},

    # ---- L04 ----
    {"id": "L04-PROSE", "check": "2.9 prose: why-it-matters (<=120 words), Defs 1.1, 1.2, 2.1, Remark 1.3, Remark 2.2", "location": P + "L04.html:52-70, :137-145",
     "status": "PASS", "evidence": "why-it-matters = 101 words. Example 1.9 'gives a dependent pair with E[XY]=E[X]E[Y]' is correct (0 = 0*2/3). Remark 1.3 'applies the test to every cell of three tables (Parts A and B)': the code's is_independent checks every cell (L04.html:219-222) and the output prints one verdict per table. Remark 2.2 scope is accurate."},
    {"id": "L04-TERM-ORDER", "check": "1.10 terms used before definition within L04", "location": P + "L04.html:52 vs :59, :131",
     "status": "PASS", "evidence": "The why-it-matters paragraph names Definition 1.1 and Example 1.9 before they appear. Both are later in the same lesson and are labelled, so this is an in-lesson forward label, not a concept used before its introduction."},
    {"id": "L04-REMARK-1-3", "check": "2.5 lab description vs code: Remark 1.3 and Part A/B", "location": P + "L04.html:70, :174-186; tests/labs/M4/lab-M4-L04-1.py:180-184",
     "status": "PASS", "evidence": "Lab docstring: 'Part A: two joint tables ... applied to every cell, and the verdict is printed with the cell (0, 0)'. Code and output agree (Part A prints two verdicts and cell (0,0); Part B prints one table and its verdict)."},
    {"id": "L04-MATH", "check": "2.4 mathematics: Props 1.4, 1.5, 1.7, 1.8, 2.3, 2.4; Example 1.9, Example 2.5 re-derived", "location": P + "L04.html:73-165",
     "status": "PASS", "evidence": "Prop 1.4 (P(A)P(B)>0 vs 0). Prop 1.5 factorization. Prop 1.7 expansion. Example 1.9: E[XY]=E[X^3]=0, p(0,0)=1/3 vs 1/9. Example 2.5 table: P(Y=0)=2/5, P(Y=1)=3/5, E[X]=4/5, E[X|Y=0]=1, E[X|Y=1]=2/3, total expectation 4/5. Prop 2.3 and 2.4 proofs correct."},
    {"id": "L04-LAB", "check": "2.5 lab: hypothesis, code, expected block, interpretation", "location": P + "L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py",
     "status": "PASS", "evidence": "twins_r6.py: code equals twin; stdout equals expected block (18 lines); exit 0. Printed values: product cell 3/50, dependent cell 1/10 vs 4/25 (ratio 5/8), Part B covariance 0 and cell 1/3 vs 1/9, Part C 4/5, 1, 2/3, 2/5, 3/5, total 4/5 equals E[X] True. Interpretation at :300 matches."},
    {"id": "L04-PROBLEMS", "check": "2.4 problem set: worked solutions re-derived", "location": P + "L04.html:331-434",
     "status": "PASS", "evidence": "M1 (0.3, 0.7, 0.4, 0.6; 0.12 vs 0.1, dependent); M2 (E[X|Y=1]=2/3, E[X]=0.7); M3 (cells 1/8,1/8,3/8,3/8; E[XY]=1/8); P1-P3 correct; E1 sum 4/5; E2 ratio 3; E3 ratio 5/8 = 0.625; R1 Cov=0 and dependent; R2 Cov(X,X)=Var; R3 conditional expectations 0 and dependence."},
    {"id": "L04-QUIZ", "check": "2.4 quiz: keys and explanations", "location": P + "L04.html:453-527",
     "status": "PASS", "evidence": "Ten items with correct keys: dependent (1/3 vs 1/9); E[X|Y=0]=1 ((2/10+2/10)/(2/5)); E[XY]=E[X]E[Y]; E[X]=4/5; events dependent; Cov=0; total-expectation sum with weights; P(Y=1)=3/5; R3 counterexample; product cell 3/50 = 0.06."},
    {"id": "L04-CANON-MISC", "check": "2.4/2.9 canon section and misconceptions", "location": P + "L04.html:303-329",
     "status": "PASS", "evidence": "Four canon bullets re-derived: marginals do not fix the table (p(0,0)=1/2 vs 1/4); product rule example (X=+-1, Y=X: E[XY]=1 vs 0). Three misconceptions with correct corrections (zero covariance; disjoint events; E[X|Y] constant)."},
    {"id": "L04-FOOTER", "check": "2.9 references and footer scope", "location": P + "L04.html:530-543",
     "status": "PASS", "evidence": "'This lesson cites no outside source' and 'Every result ... is derived on the page (grade T)'. Accurate: no registry key is cited on the page."},
    {"id": "L04-FWD", "check": "2.9/1.10 forward pointers to Lesson 5 in L04", "location": P + "L04.html:52, :99",
     "status": "FAIL",
     "evidence": "L04.html:52: 'Lesson 5 develops the correlation and the covariance matrix.' L04.html:99: 'L05 defines the correlation from it and proves its properties.' Both link a later lesson's definition. M4-build-plan.md:113: 'No lesson links a later definition.' Low severity: no result of L04 depends on L05.",
     "fix": "Reword without a later definition reference, e.g. 'Correlation and the covariance matrix are developed later in this module.' (Or record an Architect ruling that forward pointers are allowed.)"},

    # ---- cards ----
    {"id": "CARDS-DUP", "check": "2.7 duplicates: full scan of cards.json (220 cards)", "location": P + "cards.json",
     "status": "PASS", "evidence": "Python scan: 220 cards, 0 duplicate ids, 0 duplicate fronts, 0 cards missing id/lesson/front/back/grade. Grades: T 200, C 20. Near-duplicates M4-c061 and M4-c065 test the same Proposition 2.4 from opposite directions; they are distinct questions, not duplicate cards."},
    {"id": "CARDS-L01", "check": "2.7 cards for L01 vs current lesson text", "location": P + "cards.json: M4-c001..c016, c173, c192..c195, c197, c198",
     "status": "PASS", "evidence": "23 cards read and checked against L01 text. Hypotheses carried where the proposition needs them (c005, c006, c008, c009, c010, c013, c014, c197, c198). c014 back updated this round to state the hypotheses; still correct. c015 front matches Misconception 3 (L01.html:296-297)."},
    {"id": "CARDS-L02", "check": "2.7 cards for L02 vs current lesson text", "location": P + "cards.json: M4-c017..c033, c181, c182, c199",
     "status": "PASS", "evidence": "20 cards read. c032 back now states hypotheses; still correct. c030 and c033 are C with basis Lab 1 (SIMULATED), values 3.469 and 489 match the lab output. c031 value 54486.24 matches Example 2.6."},
    {"id": "CARDS-L03", "check": "2.7 cards for L03 vs current lesson text (numbers cite the current labels)", "location": P + "cards.json: M4-c034..c048, c183, c200, c212, c214, c215, c219(removed), c220, c222..c229",
     "status": "PASS", "evidence": "29 L03 cards read (c219 removed this round; see CARD-M4-c219). Cards cite 'Definition 2.2' (c037, c224) and 'Proposition 2.2' (c038, c214, c225, c229), Prop 2.3 (c039, c046, c215), Prop 2.4 (c040), Example 2.5 (c041, c045, c048, c226), Prop 2.7 (c220) and Assumption 2.6 (c220). All match the current text. Note: these labels change if L03-NUMBERING is fixed."},
    {"id": "CARDS-L04", "check": "2.7 cards for L04 vs current lesson text", "location": P + "cards.json: M4-c049..c066, c201, c204, c233(merged)",
     "status": "PASS", "evidence": "20 L04 cards read (c233 merged into c201 this round). Definition 1.1, 1.2, Remark 1.3, Props 1.4, 1.5, 1.7, 1.8, Example 1.9, Def 2.1, Remark 2.2, Props 2.3, 2.4, Example 2.5, Section 3 table, Problems P3, R2, R3 all exist in L04 and say what the cards say."},
    {"id": "CARDS-NUMBERS", "check": "2.7 every card number appears in its lesson", "location": P + "cards.json (slice a cards) vs L01..L04.html",
     "status": "PASS", "evidence": "Numbers checked: 198, 149, 148.5, 3/5, 61/100, 35/3, 35/12, 91/6, 12500, 2968750000, 54486.24, 489, 500, 3.469, 2.065, 2.073, 5.580, 5.625, 73/9, 7/3, 64/9, 2157/32, 149461/256, 163/16, 18610596/4330747 (in the L03 lab expected block, L03.html:247), 1.708, 1.875 and 2/3. Each appears in its lesson or is derived in it."},
    {"id": "CARD-M4-c219", "check": "2.7 card M4-c219 (round 5 FAIL: no grade field)", "location": P + "cards.json (M4-c219 removed; formerly lesson L03)",
     "status": "PASS", "evidence": "git diff 440ed3c8 142ecfc2 -- cards.json: the card was removed. Scan: every remaining card has a grade field (grades T 200, C 20). The fact it recorded (Assumption 2.6 takes phi even, normalized, etc.) is still stated in L03.html:118."},

    # ---- cross-cutting ----
    {"id": "NOTATION-A", "check": "1.13/2.4 notation: one meaning per symbol across the unit; registry symbols (notation/notation.json) keep their meaning",
     "location": P + "L03.html:118, :123, :128 (phi = standard normal density, 25 uses); " + P + "L06.html:65 (density); " + P + "L08.html:238, :379, :465 (density product); " + P + "L07.html:52, :129 (phi_X(t) = characteristic function); " + P + "L09.html:100 (phi_W(t) = E[e^{itW}])",
     "status": "FAIL",
     "evidence": "phi is not registered in notation/notation.json. Within M4 it is the standard normal density (L03, L06, L08) and the characteristic function phi_X(t) (L07, 30 occurrences; L09, 11 occurrences). The registry says a letter may be local to a lesson, but one unit must not give one glyph two meanings across lessons (BUILDER 3.2 and verifier 2.4 'no collisions'). Registered symbols used in slice a conform: gamma_3 = E[(X-mu)^3]/sigma^3 (L03 Def 2.2 with Z) and gamma_4 = E[Z^4] not excess (L03 Def 2.2, 'without subtracting 3'). T, Phi, R^*, Q, R_f: not used in slice a.",
     "fix": "Give phi one meaning in M4. Either rename the standard normal density (L03 Assumption 2.6, L06 Def 1.1 and the density uses in L06 and L08) to a symbol not used in the unit, or rename the characteristic function (L07, L09). Request the chosen symbol under NOTATION_REQUESTS if it is to be registered. This is a fix for the owners of L03, L06, L07, L08 and L09."},
    {"id": "NOTATION-REG", "check": "1.13 registered symbols used in slice a conform to notation.json", "location": P + "L03.html (gamma_3, gamma_4); notation/notation.json",
     "status": "PASS", "evidence": "notation.json: gamma_3 = skewness E[(r-mu)^3]/sigma^3; gamma_4 = kurtosis not excess, 3 under normality. L03 uses gamma_3 = E[Z^3] (Z standardized) and gamma_4 = E[Z^4] with the normal value 3 (Prop 2.7). Same meaning."},
    {"id": "DAG-A", "check": "1.10/2.9 DAG: no concept used before it is introduced; no link to a later definition (plan line 113)",
     "location": P + "L03.html:118, :123 (standard normal law, Lesson 6 Def 1.1); " + P + "L03.html:262 (Student-t law and Lesson 10); " + P + "L02.html:270 (Student-t, Lesson 6 Prop 2.6; Lesson 10)",
     "status": "FAIL",
     "evidence": "check_dag passes (A-G02) because it reads the registry, not the prose. In the prose: L03 Assumption 2.6 and Proposition 2.7 use 'the standard normal law' and its density, which the curriculum introduces in Lesson 6 (normal-distribution), and L03:262 uses the Student-t law (Lesson 6). L02:270 uses the Student-t law with nu <= 2 (Lesson 6). BUILDER_RULES.md section 1.10 forbids use before introduction; M4-build-plan.md:113 says 'No lesson links a later definition.' M4-open-items.md item 1 and item 4 record that the builder planned these pointers and that Lesson 6 would supply the facts. No Architect ruling in plans/FINAL-ARCHITECT-RULINGS.md allows them (round-5 notes flagged the same residual for the Architect).",
     "fix": "Either (a) the Architect rules that L03 and L02 may point forward to L06 and L10 by name, recorded in plans/M4-build-plan.md; or (b) L03 states the density formula inline in Assumption 2.6 (phi(z) = e^{-z^2/2}/sqrt(2 pi)) and Proposition 2.7 is moved to Lesson 6 as open item 1 proposes; L02:270 drops the Student-t and Lesson 10 pointer (Lesson 6 Prop 2.6 is the place for it). L03:262 drops the Lesson 10 example or moves it to Lesson 10."},
    {"id": "PROCESS-A", "check": "2.9 process words and banned phrases (BUILDER 1.3-1.4)", "location": P + "index.html; L01.html..L04.html; cards.json (slice a)",
     "status": "PASS", "evidence": "grep (case-insensitive) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, verifier, builder, round N, draft: no hits. 'Verify' occurs only as a learner instruction in problems. Ellipses appear only as math \\dots."},
    {"id": "SCOPE-A", "check": "4 scope words (only, all, always, every, any, exactly) carry a computation or a stated hypothesis", "location": P + "index.html:37, :175; L01.html:55, :99, :270, :279-281, :375-377; L02.html:135, :146, :289; L03.html:112-113, :262, :270, :370; L04.html:131-133, :322, :326",
     "status": "PASS", "evidence": "Each scope word was checked: 'every' in L01 Prop 2.2 scope and 'at all 6 support points' (computed); 'only when E[X]=0' (L02:289) follows from Var = E[X^2]-mu^2; 'exactly two values' (L03 Prop 2.4) proved in both directions; 'every law ... is finite' (L03:262) true for slice-a laws; the Lab 1 grid check (100 points) is described as a finite check only. Index 'SIMULATED throughout' and 'no lab reads a data file' verified by grep."},
    {"id": "DATA-A", "check": "2.8 data: none; SIMULATED labels present where samples are shown", "location": P + "index.html:37, :175; L02.html:146; L03.html:137",
     "status": "PASS", "evidence": "No dataset is named in the curriculum M4 entry; no lab reads a file or the network (grep); samples are seeded and labelled SIMULATED on the page that shows them."},
    {"id": "STRUCT-A", "check": "2.9 structure: BUILDER 4.2 order (why, core, inline labs, canon breaks, misconceptions, problems, quiz, references) and minimum counts", "location": P + "L01.html..L04.html",
     "status": "PASS", "evidence": "Each lesson has why-it-matters (<=120 words: 114, 105, 97, 101), numbered sections, a lab inline in the argument, canon breaks, at least three misconceptions (3, 4, 3, 3), Mechanics/Proof/Empirical/Research problem tiers with worked solutions, a quiz, and references. check_pages PASS (A-G01)."},
    {"id": "NUM-A", "check": "2.2 numbers in prose: one row per number, recomputed", "location": P + "L01.html, L02.html, L03.html, L04.html, index.html (all decimals and fractions in prose)",
     "status": "PASS", "evidence": "All decimals in slice a re-derived by the verifier: 0.833 (5/6), 0.625 (5/8), 0.06, 0.0, 1.708, 15.17, 2.92, 54486.24, 544.8624, 8.11, 1.155, 2.6667, 1.6667, 2.0730, 5.6254, 2.073, 5.625, 2.065, 5.580, 3.469, 0.031, 0.008, 0.045, 0.987 (74/75), 0.6, 0.8. Exact fractions re-derived in the same passes. No hedged number ('about', 'roughly') lacks a computation on the page."},
    {"id": "GRADE-A", "check": "2.3 grades in slice a: T only on proved or exactly computed claims; C on simulated results", "location": P + "L01..L04.html grade blocks; cards.json",
     "status": "PASS", "evidence": "Key-results tables: T rows are proofs or exact computations on stated tables. Simulated outputs appear as C only in cards c030, c033, c047, c183. No simulated value is graded T in slice a."},
    {"id": "ASSUMP-A", "check": "2.4 assumptions: each unproved fact is a named numbered Assumption, and each result that uses it says so", "location": P + "L03.html:116-119 (Assumption 2.6); L03.html:122-123, :149, :163, :288, :369, :380, :401, :493",
     "status": "PASS", "evidence": "The only unproved fact in slice a is the Gaussian integral (Assumption 2.6), listed with its contents. The Student-t scale rule is labelled as a hypothesis on the hub (index.html:138-140). No other unproved fact in L01..L04."},
]

fragment = {
    "unit": "M4",
    "slice": "a",
    "round": 6,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyD6-M4-a)",
    "pin": "142ecfc2bd27061de18bd67e83df81e69f5c249d",
    "base": "440ed3c8216725d498d9c6d7c746907d4d418198",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD6-M4-a",
    "scratch": "ledgers/M4/scripts/M4-a-r6/",
    "verified_at": "2026-11-04T03:07:41+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "notation/notation.json does not register phi; phi is the standard normal density in L03, L06, L08 and the characteristic function in L07, L09 (NOTATION-A).",
        "references/references.json blitzstein2019introduction has no edition field; Crossref (plain curl, A-G11) reports edition-number 2, matching the registry source string '2nd ed. (2019)'. The hub (index.html:183) states the edition is not checked against the book, which is accurate. Registry owner may record the edition.",
    ],
    "freshness_flags": [],
    "notes": [
        "Carry: no round-5 PASS row was carried. Every subject was re-read this round (the delta since 440ed3c8 touched L01, L02, L03 and cards.json; index.html and tests/labs/M4 L01-L04 are byte-identical).",
        "Round-5 FAIL rows: A-G08 still FAIL (repo file unchanged); NOTATION-A still FAIL; L03-NUMBERING still FAIL (now a duplicate number 2.2, not a gap); CARD-M4-c219 now PASS (card removed, all cards graded).",
        "New FAIL rows this round: A-H11 (project.html:42 skip rule omits the skill checks), L02-FWD-COVARIANCE (L02:347), L04-FWD (L04:52, :99), DAG-A (L03:118, :123, :262; L02:270 use Lesson 6 and Lesson 10 concepts before introduction).",
        "Possible but not a row: lowercase p is the quantile level in L01 Definition 3.1 and the weight function p(omega) in L01 Section 1 and the Bernoulli parameter in L03. Each use is distinguished by its arguments and labels. Recorded here, not as a FAIL, because no registered symbol is involved.",
        "Mutation testing: not applicable. Slice a has no project grader; lab twins are demonstrations (verifier rules). mutants is empty.",
        "Lab twins: each runs under python -I -W error with empty stderr. The 'Predicted before running' hypothesis lines are the lab convention in this unit and are not counted as process words.",
        "Cards: 220 cards in the file; 92 are slice-a cards (L01 23, L02 20, L03 29, L04 20).",
    ],
    "summary": "",
}

fragment["summary"] = (
    "Slice a round 6 at 142ecfc: {n} rows; {p} PASS, {f} FAIL, 0 UNVERIFIABLE. FAIL rows: A-G08 (repo ruff format, M3 retired file, outside slice); "
    "A-H11 (placement skip rule in project.html:42 vs index and BUILDER 5.1); L02-FWD-COVARIANCE (L02:347); L03-NUMBERING (duplicate number 2.2, L03:75 and :80); "
    "L04-FWD (L04:52, :99); NOTATION-A (phi: density vs characteristic function); DAG-A (L03:118, :123, :262 and L02:270 use Lesson 6 and Lesson 10 concepts before introduction)."
).format(n=len(rows), p=sum(r["status"] == "PASS" for r in rows), f=sum(r["status"] == "FAIL" for r in rows))

if __name__ == "__main__":
    out = ROOT / "ledgers" / "M4" / "M4-a.json"
    out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    problems = ledger.validate(json.loads(out.read_text(encoding="utf-8")), "M4-a")
    print("rows", len(rows), "PASS", sum(r["status"] == "PASS" for r in rows), "FAIL", sum(r["status"] == "FAIL" for r in rows))
    print("validate:", problems)
