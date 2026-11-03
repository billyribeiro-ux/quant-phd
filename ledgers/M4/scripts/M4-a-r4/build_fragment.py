"""Builds ledgers/M4/M4-a.json (round 4) from the rows verified in this round. Standard library only."""

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/M4/scripts/M4-a-r4"
G = f"{S}/gates"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, rid
        r["fix"] = fix
    rows.append(r)


# ---------- gates ----------
row("A-G01", "2.9 structure: check_pages --unit M4", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    f'`.venv/bin/python tools/check_pages.py --unit M4` -> "check_pages M4: PASS", exit 0 ({G}/check_pages.log). Unit-wide run; the slice pages are included.')
row("A-G02", "2.9 DAG: check_dag --unit M4", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    f'`tools/check_dag.py --unit M4` -> "check_dag M4: PASS", exit 0 ({G}/check_dag.log). check_dag sees links only; the standard-normal use before its owner lesson is not a link and is recorded at L03-STD-NORMAL-DUP.')
row("A-G03", "2.6 projects gate (unit-wide; outside slice a)", "course/modules/M/M4/project.html", "PASS",
    f'`tools/check_projects.py --unit M4` -> "check_projects M4: PASS", exit 0 ({G}/check_projects.log).')
row("A-G04", "2.5 labs: run_labs --unit M4", "tests/labs/M4/lab-M4-L01-1.py..lab-M4-L04-1.py", "PASS",
    f'`tools/run_labs.py --unit M4` -> "run_labs M4: PASS (13/13)", exit 0 ({G}/run_labs.log). Interpreter: .venv Python 3.14.8.')
row("A-G05", "2.5 twins alone under python -I -W error; page code equals twin; expected block equals stdout",
    "tests/labs/M4/lab-M4-L01-1.py..L04-1.py; course/modules/M/M4/L01.html..L04.html", "PASS",
    f"`.venv/bin/python -I {S}/m4a_r4_twins.py` (output {S}/m4a_r4_twins.out): each twin run with `python -I -W error` from an empty scratch directory: L01 exit 0, 20 stdout lines; L02 exit 0, 10 lines; L03 exit 0, 8 lines; L04 exit 0, 18 lines; zero stderr bytes. Page code block equals the twin file (after HTML unescaping) for all four; expected block equals stdout line for line; script prints 'twins PASS'.")
row("A-G06", "2.9 page_smoke (slice pages alone, Pyodide and browser)", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    f'`tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04` -> "page_smoke M4: PASS", exit 0; each lab 0.0 s; Pyodide runtime boot 1.1 s ({G}/page_smoke_slice.log).')
row("A-G07", "gate: ruff check . (repository)", "repository", "PASS",
    f'`.venv/bin/ruff check .` -> "All checks passed!", exit 0 ({G}/ruff_check.log).')
row("A-G08", "gate: ruff format --check . (repository)", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3; pyproject.toml:18", "FAIL",
    f'`.venv/bin/ruff format --check .` -> "1 file would be reformatted", at ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3:1, exit 1 ({G}/ruff_format_check.log). The file is byte-identical to a007712 (git diff --quiet a007712 4eb6788 -- ledgers/M3/retired), it is outside slice a, and the M4 pages pass the format check (473 files already formatted). Recorded as a repository gate failure so the verdict is not hidden.',
    fix='Owner of M3: either format ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py, or add "ledgers/*/retired" to [tool.ruff] extend-exclude in pyproject.toml (line 18), then re-run `.venv/bin/ruff format --check .`. No change to any M4 file is needed for this row.')
row("A-G09", "gate: mypy strict (mypy --no-incremental)", "repository (331 source files)", "PASS",
    f'`.venv/bin/mypy --no-incremental` -> "Success: no issues found in 331 source files", exit 0 ({G}/mypy.log).')
row("A-G10", "gate: relevant pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py, test_page_smoke.py, test_curriculum.py", "PASS",
    f"`.venv/bin/pytest -q -p no:cacheprovider` on the six files: all tests pass, exit 0 ({G}/pytest_relevant.log).")
row("A-G11", "2.1 citations: verify_refs; live check of blitzstein2019introduction", "references/references.json (key blitzstein2019introduction); tools/verify_refs.py", "PASS",
    f"Offline: `.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({G}/verify_refs_offline.log). Live, plain curl (no bot-check or login): GET https://api.crossref.org/works/10.1201/9780429428357 -> HTTP 200; title 'Introduction to Probability'; authors Blitzstein, Joseph K. and Hwang, Jessica; published 2019-02-08; publisher Chapman and Hall/CRC; ISBN 9780429428357; edition-number 2. Matches the registry record. A unit-wide live verify_refs run was not repeated: references/, tools/refs/, notation/ and tools/verify_refs.py are byte-identical since d0f39c09 (git diff --quiet d0f39c09 4eb6788).")
row("A-G12", "scope: slice-a delta since previous pin a007712, every hunk", "course/modules/M/M4/index.html:33; L02.html:496, :507; L03.html:487, :498; L04.html:52, :405; cards.json (M4-c199)", "PASS",
    "git diff a007712 4eb6788 for slice a read hunk by hunk (8 hunks in slice a: index 1, L02 2, L03 2, L04 2, cards M4-c199 1): index lede wording (:33); L02 references and footer (:496, :507) now say each exact result is proved or computed and the Lab 1 samples are SIMULATED; L03 references and footer (:487, :498) likewise, with Proposition 2.8 under Assumption 2.6; L04 why-it-matters (:52) adds a forward pointer 'Definition 1.1 below'; L04 E3 solution (:405) wording, re-derived (5/8 and the direction of dependence); cards M4-c199 hypothesis 'finite probability space with positive weights' (correct). L01.html, the L01-L04 twins and the L01-L04 card texts other than c199 are unchanged. cards M4-c081 (L05) and M4-c140 (L09) are outside slice a.")

# ---------- hub ----------
row("A-H01", "2.9 structure: hub section order and minimum counts (BUILDER 4)", "course/modules/M/M4/index.html:45, :58, :68, :145, :162, :173, :178", "PASS",
    "Whole hub read. Order: objectives (6 items, within 4-8), prerequisites, placement (10 items), lesson map (10 cards), ladder (4 rungs), data status, reading list. Measurable verbs throughout.")
row("A-H02", "2.9 hours arithmetic", "index.html:29, :39-42, :147; L01..L10 data-hours", "PASS",
    "data-hours-lessons=90 and data-hours-project=30 (index.html:29); the ten lessons carry data-hours=\"9\" (grep over L01..L10 html); 10 x 9 = 90; 90 + 30 = 120 = curriculum.json M4 hours 120; project 30/120 = 25% inside 10-40%. The CSS split widths 75%/25% (index.html:40) agree.")
row("A-H03", "2.9 objectives: measurable verbs and lesson mapping", "index.html:49-54", "PASS",
    "Six objectives with verbs compute, derive, state, decide, show, apply (and state); each maps to lessons 1, 2, 3, 4-5, 6, 9-10, and each lesson exists.")
row("A-H04", "2.6 prerequisites vs curriculum", "index.html:35, :60-65; curriculum.json M4 entry", "PASS",
    "curriculum.json M4 prereqs = ['M2'], tier F, hours 120, part M (read this round). The hub says M2 and, through M2, M1, and uses only M1/M2 concepts (limit, definite-integral, exponential-and-logarithm, quantifiers) with links; check_dag PASS; no M3 concept is linked.")
row("A-H05", "2.2/1.10 hub claim: matrix facts are derived from the quadratic form (Lessons 5 and 8)", "index.html:35, :62 vs L05.html:125-135 and L08.html:73, :113", "PASS",
    "L05 Definition 2.1 (covariance matrix), Proposition 2.3 'a covariance matrix is positive semidefinite' (L05.html:135, proved from w^T Sigma w = Var(w^T X)); L08 Proposition 1.3 (mean and covariance of a linear image, L08.html:73); L08 Proposition 2.1 'a singular covariance has no inverse' (L08.html:113). No M3 link (check_dag PASS).")
row("A-H06", "2.9 placement diagnostic: items, bar, skill checks", "index.html:68-143", "PASS",
    "Ten items; data-mastery 0.8 = 8 of 10 (text says the same). Items 1-8 test M1/M2 prerequisites (quantifier negation, limit 0, integral 1/2, derivative r e^{rt}, ln e^3 = 3, geometric sum 15/8, discount factor 1/(1+r), partial derivative 2xy). Items 9 and 10 carry data-skill: rung-1 quantile (answer 1) and rung-2 scale factor (answer 0.6), matching the completion problem's blank. Each correct option re-derived.")
row("A-H07", "3 attribution: placement explanation cites 'M1 Theorem 3.1'", "index.html:79 vs course/modules/M/M1/L01.html:79, :89", "PASS",
    "M1 L01.html:79 reads 'Theorem 3.1 (negating one quantifier)'. The explanation (negation of 'for every x, P(x)' is 'for some x, not P(x)') matches its statement and its use at M1 L01.html:89.")
row("A-H08", "2.2 numbers in placement answers and explanations", "index.html:90-140", "PASS",
    "Re-derived in ledgers/M4/scripts/M4-a-r4/m4a_r4_numbers.py (IDX checks): 0.5; 3; 15/8 = 1.875 (1 + 1/2 + 1/4 + 1/8); 1/(1+r); rung-1 F(0)=1/4 < 1/2 <= 3/4 = F(1) gives 1; rung-2 Var of t_5 = 5/3 and s^2 = 3/5 = 0.6. All printed digits agree.")
row("A-H09", "2.2/2.4 rung-2 skill check hypothesis and its sources", "index.html:137-140 vs L06.html:158-160 (Proposition 2.6) and L02.html:114-116 (Proposition 2.3)", "PASS",
    "L06 Proposition 2.6 'Assuming Assumption 1 ... if nu > 2, Var(t) = nu/(nu-2)' gives 5/3 at nu = 5. L02 Proposition 2.3 is stated for X on a finite probability space with positive weights (the standing assumption at L02.html:55), which is why the hub says the scale rule for Student-t is taken as a hypothesis.")
row("A-H10", "2.7/2.9 hub lesson cards agree with the lessons", "index.html:149-158 vs L01..L04 and L05..L10 pages", "PASS",
    "L01-L04 card texts read against the lessons (see the lesson rows). L05-L10 cards spot-checked against their locators: L05 Proposition 2.3 (PSD), L08 Proposition 2.1 (singular covariance), L09 'the distribution-function limit is not established on this page' (L09.html:151), L10 Cauchy and Student-t(3) lab (L10.html:76 and the lab). Other slices verify those pages in full.")
row("A-H11", "2.6 ladder: four rungs in order; names agree with project.html", "index.html:162-171 vs project.html:44-47", "PASS",
    "Rung titles Worked example, Completion problem, Independent project, Stretch, in order, identical to project.html:44-47; project.html:46 names tail_risk.py and the three functions named on the hub.")
row("A-H12", "2.8 data status and SIMULATED labels", "index.html:37, :175, :187", "PASS",
    "No data: index.html:37 and :175 say no real data, and that labs compute from formulas and seeds. grep: data-files count 0 and data-chart count 0 on every slice-a page; the only script and style sources are local (assets/).")
row("A-H13", "2.1 reading list and citation: blitzstein2019introduction", "index.html:178-184; references/references.json (key blitzstein2019introduction)", "PASS",
    "Registry record: year 2019, isbn [9780429428357], publisher Chapman and Hall/CRC, no edition field, source_strings ['Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)']. The hub says the edition is taken from the curriculum and not checked against the book, which is accurate. The live Crossref record reports edition-number 2 (A-G11), which supports the curriculum's '2nd ed.'; this is a registry flag, not a defect in the hub.")
row("A-H14", "2.6 curriculum facts for the hub: no debate, no Atlas milestone, part and tier", "index.html:31, :37; curriculum.json M4", "PASS",
    "curriculum.json M4 keys: core, hours, id, introduces, lab, part, prereqs, project, sources, tier, title. No 'debate' key and no 'atlas' key. Part M, tier F, 120 h.")
row("A-H15", "2.9 hub footer", "index.html:187", "PASS",
    "'Seeded samples are SIMULATED; no real data is used.' Accurate for the hub, which contains no sample.")

# ---------- L01 ----------
row("L01-PROSE", "2.2 numbers and claims in prose", "L01.html:37-51, :55-69, :95-99, :114-135, :277-297, :360-370", "PASS",
    "Each number re-derived with Fraction (m4a_r4_numbers.py, L01 section): Example 1.3 P(X<=1) = 5/6; Example 3.5 198, 149, pn = 148.5, 148/150 = 74/75 = 0.987 < 0.99; Example 3.6 F = 1/10, 3/10, 3/5, 4/5, 9/10, 1 and Q(1/2) = 0, Q(3/5) = 0, Q(61/100) = 1; canon bullet 1 strict rule gives 1 at p = 3/5; misconception values. 158 of 158 claims OK across the slice.")
row("L01-MATH", "2.4 definitions, Prop 2.2, Def 3.1, Prop 3.2, Remark 3.3, Prop 3.4, proofs", "L01.html:57-126", "PASS",
    "Every proof read line by line. Hypotheses stated (positive weights, distinct values, 0 < p <= 1). Remark 3.3 left-continuity covers the p = F_{k-1} case; Proposition 3.4 index ceil(pn) lies in [1, n] since 0 < pn <= n. Notation: R macro registered.")
row("L01-LAB", "2.5 lab: hypothesis, output, interpretation", "L01.html:138-270; tests/labs/M4/lab-M4-L01-1.py", "PASS",
    "Twin output equals the 20-line expected block (A-G05). Hypothesis values Q(1/20) = Q(1/10) = -2, Q(11/100) = -1, Q(1/2) = Q(3/5) = 0, Q(61/100) = 1, Q(9/10) = 2, Q(91/100) = Q(99/100) = Q(1) = 3 re-derived. 'scan equals definition at 100 of 100 points' and 'F(Q(p)) >= p at 100 of 100' hold on re-derivation. Interpretation claims only the printed grid check, not all p.")
row("L01-PROBLEMS", "2.4 problem set: 12 worked solutions", "L01.html:302-405", "PASS",
    "All twelve re-derived: M1 F and Q(1/2) = 0; M2 F(5) = 7/10, Q(7/10) = 5, Q(71/100) = 7; M3 indices 36 and 37; P1-P3 proofs; E1 Q(99/100) = 3 with F(2) = 9/10; E2 Q(3/5 + eps) = 1; E3 counting argument; R1 strict rule gives 1 at 3/5 and agrees elsewhere on a finite law; R2; R3.")
row("L01-QUIZ", "2.9 retrieval quiz: 9 items, answers and explanations", "L01.html:424-494", "PASS",
    "Answers recomputed: Q(1/2) = 1 for (1/4, 1/2, 1/4); Q(61/100) = 1; 'discontinuity' item (Proposition 2.2(d)); 198; 149; Q(F_k) = x_k; P(X <= 1) = 5/6 = 0.833; the random variable is a function; Q(1) = x_m. Each item has an explanation that cites its result.")
row("L01-GRADES", "2.3 grades on theorems and key-results rows", "L01.html:43-48, :80, :103, :114, :119, :413-418", "PASS",
    "Proposition 2.2, Proposition 3.2, Remark 3.3 and Proposition 3.4 are graded T with proofs on the page; key-results rows cite proof sections or exact arithmetic on a stated table.")
row("L01-FWD", "5 terms used before definition", "L01.html:37, :51", "PASS",
    "'infimum' (L01.html:37) is defined at :95 (inf A for a set bounded below), and the pointer at :37 says so. 'quantile' (:51) carries the pointer 'defined in Definition 3.1 below'.")

# ---------- L02 ----------
row("L02-PROSE", "2.2 numbers and claims in prose", "L02.html:51, :55, :89, :134-141, :262, :267-273, :281-293, :358-372", "PASS",
    "Re-derived: 35/12 and sqrt(35/12) = 1.708; E[L] = 12500; E[L^2] = 3125000000; Var(L) = 2968750000; sd 54486.24 cents (sqrt check: 54486.2368); R2 Var(D) = 296875 and sd 544.8624; canon E[X] = 3/10 from (-2-2+0+2+2+3)/10; misconception values 15.17, 2.92.")
row("L02-MATH", "2.4 definitions, Props 1.2-1.3, 2.2-2.4, Def 1.6 and proofs", "L02.html:57-132", "PASS",
    "Every proof read. Proposition 2.2 applies Proposition 1.3 with U = X^2, V = X, alpha = 1, beta = -2 mu, delta = mu^2. Proposition 2.3 hypotheses come from the standing assumption at L02.html:55 (finite space, positive weights). Proposition 2.4 is stated for that space. Definition 1.6 is stated as unused by the lesson, and no result uses it.")
row("L02-LAB", "2.5 lab: hypothesis, output, interpretation", "L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py", "PASS",
    "Twin output equals the 10-line expected block (A-G05): 3.469 for seed 2026 (n = 10000), 489 losses and 122250000 cents for seed 2027, mean 12225.0 cents. The three True lines are the die shortcut, the die scale rule (Var(2X) = 4 Var X) and the loss shortcut. Sample values are labelled SIMULATED and one run each.")
row("L02-PROBLEMS", "2.4 problem set: 12 worked solutions", "L02.html:298-401", "PASS",
    "M1 21/100; M2 5000, 2.25e8, 15000; M3 36 and 4; P1 sum rule; P2 minimum at c = mu; P3 Var(U+V) = 0 and Var(U)+Var(V) = 2; E1 3.469 and -0.031; E2 489 is 11 below 500; E3 35/3; R1 divisor-n identity; R2 296875 and 544.86; R3 3/10 and Q(1/2) = 0.")
row("L02-QUIZ", "2.9 retrieval quiz: 10 items", "L02.html:421-492", "PASS",
    "Answers 3.5, 1, 12, E[(X - E X)^2], 5000, 225000000, 21/100, c = E[X], 15000, 5 all recomputed with the cited propositions.")
row("L02-MISC", "2.9 misconceptions (4 wrong beliefs refuted on the page)", "L02.html:279-296", "PASS",
    "Expectation is a value (3.5 not a face); scaling by a (variance x 4, not x 2); variance is E[X^2] (agree only when E[X] = 0, which follows from Proposition 2.2); seeded sample mean equals expectation (one run, 3.469). Each refutation is computed.")
row("L02-CANON", "2.2/1.10 cross-lesson claims in 'Where the canon breaks'", "L02.html:267-273 vs L06.html:158-160 and L10.html", "PASS",
    "L06 Proposition 2.6 (under Assumption 1): nu <= 2 gives E[t^2] = infinity, the 'no finite variance' statement. L10 treats heavy tails. The mean-versus-quantile point uses L01 Example 3.6 correctly.")
row("L02-FWD-COVARIANCE", "1.10 forward pointer in P3 to Lesson 4 Proposition 1.7 and Lesson 5", "L02.html:347 vs L04.html:103-104 and L05.html:59", "PASS",
    "L04 Proposition 1.7 is the covariance shortcut, and L05 Proposition 1.1 gives bilinearity. The pointer is prose, not a link to a later concept.")
row("L02-FOOTER-SCOPE", "2.9 scope words in footer and references", "L02.html:496 (References), :507 (footer)", "PASS",
    "Was FAIL in round 3. Now: 'Each exact result is proved on the page or is an exact computation on a stated list; ... the seeded samples in Lab 1 are SIMULATED and are not proofs.' Each exact result on this page is proved or computed (checked against every proposition, example, problem and key-results row). Fixed at 4eb6788.")

# ---------- L03 ----------
row("L03-PROSE", "2.2 numbers and claims in prose", "L03.html:51, :55, :113, :138, :258, :263-268, :281, :382", "PASS",
    "Re-derived with Fraction: mu = 7/4; m2 = 163/16; m3 = 2157/32 (terms -1372, -54, +1, +35937 over 512; the value-10 term exceeds m3 by 1425/512); m4 = 149461/256; gamma3^2 = 18610596/4330747 (about 4.2973), gamma3 = 2.0730; gamma4 = 149461/26569 = 5.6254. Bernoulli p = 1/10: gamma3 = 8/3, gamma3^2 = 64/9, gamma4 = 73/9 = 8.11; p = 1/4: gamma4 = 7/3. Sample 2.065 and 5.580 against exact 2.073 and 5.625: gaps 0.008 and 0.045, rounding error at most 0.001.")
row("L03-MATH", "2.4 Props 1.1, 2.2-2.4, Example 2.5, section 3 arithmetic", "L03.html:57-114, :138", "PASS",
    "Every proof read. Proposition 2.3: sigma_Y = |a| sigma_X and Z_Y = sign(a) Z_X. Proposition 2.4: W = Z^2 constant forces Z = +-1 and E[Z] = 0 forces probability 1/2. Example 2.5: m3 = pq(q-p) and m4 = pq(1-3pq) re-derived; gamma3 = (1-2p)/sqrt(pq); gamma4 = (1-3pq)/(pq). Section 3 terms re-derived.")
row("L03-PROP28-SCOPE", "2.4 Proposition 2.8 proof needs no hypothesis the statement omits", "L03.html:127-128 (statement), :133 (proof), :122-124 (Def 2.7)", "PASS",
    "The statement names its hypothesis (Assumption 2.6). The proof uses phi(-z) = phi(z) for E[Z] = 0, phi' = -z phi for the integrations by parts, and z^k phi(z) -> 0 for the boundary terms; the integrals are finite under Assumption 2.6 for k <= 4. Nothing else is assumed. (The defect in Definition 2.7 is recorded at L03-STD-NORMAL-DUP.)")
row("L03-STD-NORMAL-DUP", "1.10 concept defined twice and used before its owner lesson: standard normal law",
    "L03.html:117-118 (Assumption 2.6), :122-124 (Definition 2.7) vs L06.html:63-66 (Definition 1.1, dfn normal-distribution) and L06.html:65 (standard normal law)", "FAIL",
    "L03 defines the standard normal law: Assumption 2.6 gives 'The standard normal density is phi(z) = (2 pi)^(-1/2) e^(-z^2/2)'; Definition 2.7 gives 'A random variable Z is standard normal when P(Z in B) = integral over B of phi(z) dz'. L06.html:65 defines the same law again: 'The standard normal law is N(0,1), with density phi(z) = e^(-z^2/2)/sqrt(2 pi). A variable Z with this law is a standard normal variable', inside the dfn of normal-distribution (curriculum.json M4 introduces 'normal-distribution', owned by L06 per plans/M4-build-plan.md). So the law is defined in L03 (lesson 3) and again in L06 (lesson 6), and used in L03 before its owner. check_dag passes because Definition 2.7 is not a dfn element. The card M4-c219 restates Definition 2.7.",
    fix="Delete Definition 2.7 and the density sentence of Assumption 2.6 from L03; use the standard normal law of L06 Definition 1.1 by a forward pointer with no dfn and no restatement. Move Proposition 2.8 (and cards M4-c219, M4-c220 with it) to L06 after Definition 1.1 and the Gaussian integral, or keep Proposition 2.8 in L03 with the law stated as the Lesson 6 law. Then re-run check_pages, check_dag and run_labs --unit M4.")
row("L03-LAB", "2.5 lab: hypothesis, output, interpretation", "L03.html:140-259; tests/labs/M4/lab-M4-L03-1.py", "PASS",
    "Twin output equals the 8-line expected block (A-G05): exact squared skewness 18610596/4330747 and kurtosis 149461/26569; Bernoulli 64/9 and 73/9 True; seed 2026, n = 20000 sample skewness 2.065 and kurtosis 5.580, labelled SIMULATED. Exact 2.073 and 5.625 match the printed decimals. The interpretation's gaps (0.008, 0.045) agree with the printed values.")
row("L03-CANON", "2.2 canon bullets; attribution to Lesson 10 Proposition 2.3", "L03.html:263-269 vs L10.html:65-66 (Assumption 1) and :150-152 (Proposition 2.3)", "PASS",
    "Law -2, 1, 3 with 2/5, 1/2, 1/10: mean 0, m2 = 3, m3 = 0, m4 = 15, gamma4 = 5/3, not symmetric (re-derived). L10 Proposition 2.3, under its Assumption 1 (density of V with nu = 3), gives E[V^4] = infinity and says the kurtosis is then undefined. The attribution matches.")
row("L03-MISC", "2.9 misconceptions (3)", "L03.html:275-287", "PASS",
    "Symmetry refuted by the section 4 law; kurtosis of every law refuted by 73/9 and 7/3 and by the point p = (1 - 1/sqrt 3)/2 with pq = 1/6 giving gamma4 = 3 (re-derived); sign reversal refuted by Proposition 2.3.")
row("L03-PROBLEMS", "2.4 problem set: 12 worked solutions", "L03.html:290-393", "PASS",
    "M1 sigma = sqrt3/4, gamma3 = 2/sqrt3 (about 1.155), gamma4 = 7/3; M2 mu = 1, gamma3 = 0, gamma4 = 1; M3 m3 = 2157/32 > 0; P1 affine invariance; P2 E[Z^2] = 1; P3 q^3 + p^3 = 1 - 3pq; E1 gaps 0.008 and 0.045; E2 64/9 and 73/9; E3 weights total 8; R1 equality case mu +- sigma; R2 73/9 about 8.11 with no tail statement; R3 symmetric implies zero m3, the converse fails by the section 4 law.")
row("L03-QUIZ", "2.9 retrieval quiz: 9 items", "L03.html:413-483", "PASS",
    "Answers 0; E[Z^3]; 1; sign change; unchanged; 5/3 (1.6667); the section 4 law; 8/3 (2.6667); zero. Each recomputed.")
row("L03-GRADES", "2.3 grades: Props 1.1, 2.2-2.4 and 2.8 (T); key-results rows", "L03.html:42-49, :57-134, :401-407", "PASS",
    "Theorems carry T on the title. Proposition 2.8 is graded T and names Assumption 2.6 in its statement (and in the key-results row at :406).")
row("L03-FOOTER-SCOPE", "2.9 scope words in footer and references", "L03.html:487 (References), :498 (footer)", "PASS",
    "Was FAIL in round 3. Now: 'Each exact result ... is proved on the page or is an exact computation on a stated table; the normal kurtosis (Proposition 2.8) is proved under Assumption 2.6'; the seeded sample is 'a SIMULATED single-run estimate and is not a proof'. Fixed at 4eb6788.")

# ---------- L04 ----------
row("L04-PROSE", "2.2 numbers and claims in prose", "L04.html:52, :130-133, :169, :300, :306-308, :318-326, :402-405", "PASS",
    "Re-derived: Example 1.9 E[Y] = 2/3, E[XY] = 0, Cov = 0, p(0,0) = 1/3 vs 1/9; Example 2.5 P(Y=0) = 2/5, P(Y=1) = 3/5, E[X] = 4/5, E[X|Y=0] = 1, E[X|Y=1] = 2/3, total expectation 4/5; M1 0.12 vs 0.1; M2 2/3; E3 ratio (1/10)/(4/25) = 5/8; canon bullet 2 marginals 1/2 vs 1/4; canon bullet 3 E[XY] = 1 vs 0.")
row("L04-TERM-ORDER", "2.9 define-before-use: 'joint table' in why-it-matters", "L04.html:52 vs L04.html:59", "PASS",
    "Was FAIL in round 3. Now 'the table of their joint probabilities (Definition 1.1 below)' carries an explicit forward pointer. Fixed at 4eb6788.")
row("L04-REMARK-1-3", "2.2 and 2.9: lab sentence vs the code and output",
    "L04.html:70 (Remark 1.3) vs L04.html:247 (Part A loop over PRODUCT and DEPENDENT), :263 (Part B is_independent(uniform)), :300 (interpretation)", "FAIL",
    "Remark 1.3 says: 'Lab 1 applies the test to every cell of two tables and prints the verdict.' The code applies is_independent to three tables: the product and dependent tables of Part A, and the uniform table of Part B (printed line 'independent False'). The interpretation at :300 says 'three exact tables', so the remark undercounts.",
    fix="L04.html:70: replace 'every cell of two tables' with 'every cell of three tables (Parts A and B)'.")
row("L04-MATH", "2.4 Defs 1.1-2.1, Props 1.4-1.8, 2.3-2.4, Remark 2.2, proofs", "L04.html:58-165", "PASS",
    "Every proof read. Proposition 1.4 (P(A and B) = 0 against P(A)P(B) > 0). Proposition 1.5 factorization over cells. Proposition 1.7 expansion and linearity. Proposition 1.8. Proposition 2.3 sums over y with P(Y=y) > 0 and the zero-probability values contribute p(x,y) = 0. Proposition 2.4.")
row("L04-LAB", "2.5 lab: hypothesis, output, interpretation", "L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py", "PASS",
    "Twin output equals the 18-line expected block (A-G05): product cell 3/50 on both sides; dependent cell 1/10 against 4/25; Example 1.9 covariance 0 with cell 1/3 against 1/9; Part C conditional expectations 1 and 2/3, total 4/5, product-table check True. The interpretation's 'three exact tables' matches the code (the remark is L04-REMARK-1-3).")
row("L04-PROBLEMS", "2.4 problem set: 12 worked solutions", "L04.html:331-434", "PASS",
    "M1 0.12 vs 0.1 (dependent); M2 2/3; M3 cells 1/8, 1/8, 3/8, 3/8 and E[XY] = 1/8 by two methods; P1 linearity; P2 two-valued Y; P3 Cov = -ab; E1 total expectation 4/5; E2 ratio 3; E3 ratio 5/8; R1 Cov 0 and dependence; R2 Cov(X,X) = Var X; R3 equal conditional expectations 0 with dependence.")
row("L04-QUIZ", "2.9 retrieval quiz: 10 items", "L04.html:453-528", "PASS",
    "Answers: not independent (1/3 vs 1/9); E[X|Y=0] = 1; E[XY] = E[X]E[Y]; E[X] = 0.8; events dependent; Cov = 0; total-expectation sum; P(Y=1) = 0.6; equal conditional expectations do not imply independence; product-table cell 3/50 = 0.06. All recomputed.")
row("L04-CANON-MISC", "2.2 canon bullets and misconceptions (3)", "L04.html:303-329", "PASS",
    "Zero covariance is not independence (Example 1.9); marginals do not fix the joint table (1/2 vs 1/4); the product rule for means fails under dependence (E[XY] = 1 vs 0 for Y = X); the conditional expectation misconception is refuted by Example 2.5.")
row("L04-FOOTER", "2.2 scope words in footer and references", "L04.html:532, :543", "PASS",
    "L04 has no seeded sample. Every printed lab value is an exact computation on a stated table and is derived in the page text (checked: 3/50, 1/10, 4/25, 1/3, 1/9, 1, 2/3, 4/5, True lines). 'Every result ... derived on the page (grade T)' holds for the results stated on the page.")

# ---------- cards ----------
row("CARDS-DUP", "2.7 full scan for duplicates (deck of 212 cards)", "course/modules/M/M4/cards.json", "PASS",
    f"{S}/m4a_r4_cards.py: 212 cards, no duplicate ids, no duplicate fronts. Near-duplicate fronts (word Jaccard >= 0.6, 55 pairs, listed in {S}/m4a_r4_cards.out) each ask a different fact; for example M4-c025 (E[X] of the die) and M4-c199 (Var of the die), M4-c047 (sample skewness) and M4-c183 (sample kurtosis). The standard-normal definition on M4-c219 is addressed under L03-STD-NORMAL-DUP.")
row("CARDS-L01", "2.7 cards for L01 (23 cards)", "cards.json: M4-c001..c016, c173, c192..c195, c197, c198", "PASS",
    f"All 23 read against L01.html ({S}/cards_slice_a.txt). All grade T with hypotheses stated where the result needs them (c005, c006, c008, c009, c013). Numbers 198, 149, 0, 1/2, 3/5, 4/5 re-derived.")
row("CARDS-L02", "2.7 cards for L02 (20 cards)", "cards.json: M4-c017..c033, c181, c182, c199", "PASS",
    "All 20 read. c030 and c033 are grade C with basis 'Lab 1 (SIMULATED)' and reproduce the twin's seed-2026 and seed-2027 lines. c199 hypothesis (finite probability space, positive weights) is correct. c029 states its hypothesis.")
row("CARDS-L03", "2.7 cards for L03 (22 cards)", "cards.json: M4-c034..c048, c183, c200, c212, c214, c215, c219, c220", "PASS",
    "All 22 read. c047 and c183 are grade C with basis and reproduce the seed-2026 lines (2.065, 5.580). c043 (5/3), c044 (law on -2, 1, 3), c045 (73/9, 7/3), c048 (64/9) re-derived. c219 is accurate to L03 Definition 2.7; its duplication with the L06 law is recorded at L03-STD-NORMAL-DUP. c220 (kurtosis 3) is accurate to Proposition 2.8.")
row("CARDS-L04", "2.7 cards for L04 (20 cards)", "cards.json: M4-c049..c066, c201, c204", "PASS",
    "All 20 read. c062 (E[X|Y=0] = 1), c064 (-ab), c065 (2/3 and 4/5), c066 (Cov(X,X) = Var X), c204 (equal conditional expectations, dependent pair) are correct. 'Section 3' on c063 is L04's canon-breaks section (section-number 3).")
row("CARDS-NUMBERS", "2.7 every card number appears in its lesson", "cards.json (L01-L04 cards) vs L01..L04.html", "PASS",
    f"{S}/m4a_r4_cards.py checks each number token in the 85 slice-a card backs against the lesson's text and TeX. Every token is found in its own lesson except one: '2/2' in M4-c219, which is the exponent z^2/2 written as z^{{2}}/2 in L03.html:118 (the density in Assumption 2.6). No card number is absent. Output {S}/m4a_r4_cards.out.")
row("CARD-M4-c219", "2.7 card truth and atomicity", "cards.json: M4-c219 (L03) and M4-c084 (L06)", "PASS",
    "M4-c219's back is true to L03 Definition 2.7 under Assumption 2.6 (moments finite for k <= 4). M4-c084 (L06) defines N(mu, sigma^2) and is not a restatement of the standard normal sentence. The remaining issue is the concept's owner, recorded at L03-STD-NORMAL-DUP.")

# ---------- notation, DAG, process, scope, data, structure, numbers ----------
row("NOTATION-A", "2.4 and 2.9 (rule 13): every symbol vs notation/notation.json",
    "L03.html:118, :123, :127-128, :133 (phi); L07.html:139 (phi_X, characteristic function); notation/notation.json", "FAIL",
    "Registered macros used on slice-a pages: \\R (L01). Registered symbols used: gamma_3 and gamma_4 (L03), whose registered meaning E[(r-mu)^3]/sigma^3 and E[(r-mu)^4]/sigma^4 (not excess) match Definition 2.2. \\operatorname{Var} and \\operatorname{Cov} are the registry's tex expansions of \\Var and \\Cov, with the same meaning. The standard normal density phi is used in L03 (and in L06), and it is not in notation/notation.json. The registry registers Phi for the standard normal CDF (module M4) and says program-wide symbols are registered, while local letters are only the listed conventional ones (alpha, beta, gamma, N, S, m, mu, sigma). phi is not in that list. The same glyph carries the characteristic function phi_X in L07 (L07.html:139), so M4 uses one symbol for two meanings.",
    fix="Architect: add \\varphi (standard normal density) to notation/notation.json as a NOTATION_REQUEST, and in L07 rename the characteristic function from phi_X to a symbol no other M4 page uses (for example psi_X), so \\varphi carries one meaning across L03, L06 and L07. Slice-a pages then need no edit beyond the L03 fix in L03-STD-NORMAL-DUP.")
row("DAG-A", "1.10 / 2.9 DAG: concept links, check_dag, define-before-use", "index.html; L01.html..L04.html", "PASS",
    "check_dag PASS (A-G02). Links in slice a point to M1 and M2 concepts or to earlier M4 lessons: L02 links random-variable (L01); L03 links random-variable, expectation, variance (L01, L02); L04 links random-variable, expectation (L01, L02). The use of the standard normal law in L03 before L06 is not a link and is recorded at L03-STD-NORMAL-DUP. Covariance ownership is a registry flag.")
row("PROCESS-A", "2.9 banned phrases (BUILDER 1.3-1.4) and process words in learner text", "index.html; L01.html..L04.html visible text", "PASS",
    "Scan of visible text (not code): no TODO, TBD, lorem, 'for brevity', 'left as an exercise', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'beyond the scope', 'you can add', 'clearly', 'obviously'; no 'verifier', 'builder', 'round N' or 'draft' in learner text. '...' occurs only inside <code> (Python tuple types).")
row("SCOPE-A", "2.2 scope words (only, all, always, every, any, same, exactly) in body text", "index.html; L01.html..L04.html body text", "PASS",
    "About 225 occurrences across the five pages, read in context. Each is backed by a stated hypothesis or computation: 'every outcome has positive probability' (positive weights, L01.html:55); L03.html:123 'the only law on this page that is not finite' (the standard normal law, the only infinite-support law there); L03.html:267 'every law the computations use is finite' with the standard-normal exception stated next; L02.html:269 'every computation uses a finite law' (Definition 1.6 is not computed).")
row("DATA-A", "2.8 data, figures, SIMULATED labels", "L01..L04.html, index.html", "PASS",
    "grep: data-files count 0 and data-chart count 0 on all five pages; no external script or stylesheet source. Seeded samples: L02 seeds 2026 and 2027, L03 seed 2026; each is labelled SIMULATED in the hypothesis and interpretation. L01 and L04 use stated exact tables only and say so.")
row("STRUCT-A", "2.9 lesson structure (BUILDER 4.2) and counts", "L01..L04.html", "PASS",
    "Order in each lesson: why-it-matters, numbered core sections, inline lab, canon-breaks, misconceptions, problem set, key-results table, retrieval quiz. why-it-matters word counts 114, 93, 97, 96 (limit 120). Misconceptions 3, 4, 3, 3. Problem set: 3 problems in each of Mechanics, Proof, Empirical, Research in every lesson (12 each). Quiz items 9, 10, 9, 10 (8-15). data-hours=\"9\" on each.")
row("NUM-A", "2.2 re-derivation of every number in slice a (own script)", f"{S}/m4a_r4_numbers.py", "PASS",
    f"`python -I -W error {S}/m4a_r4_numbers.py` -> 158 OK, 0 FAIL (output {S}/m4a_r4_numbers.out). Covers the hub placement and ladder numbers, all L01-L04 examples, proofs' numbers, the lab hypothesis values, the L03 sample gaps, and the L04 tables.")

fragment = {
    "unit": "M4",
    "slice": "a",
    "round": 4,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyD4-M4-a)",
    "pin": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b",
    "base": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-M4-a",
    "scratch": f"{S}/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "notation/notation.json does not register phi (standard normal density, used in L03 and L06). phi is also the characteristic function phi_X in L07 (L07.html:139), a different object in the same unit. Registry owner to register \\varphi for the density; the characteristic function needs another symbol. This is the NOTATION-A row.",
        "Covariance ownership: curriculum.json concept 'correlation' is labelled 'Covariance and correlation' (curriculum/01-foundations.yaml, M4 introduces). L04 Definition 1.6 defines the covariance formula (no dfn element), L05 uses it (L05.html Uses row) and defines correlation (dfn correlation, L05.html:85). plans/M4-build-plan.md open item 9 has no ruling in plans/FINAL-ARCHITECT-RULINGS.md. Architect to confirm L04 owns the covariance formula.",
        "references: live Crossref record for 10.1201/9780429428357 (fetched 2026-11-03 with plain curl) reports edition-number 2, supporting the curriculum's '2nd ed. (2019)'; the registry record has no edition field. Registry owner may record the edition from Crossref. Not a defect of the hub, which says the edition is unchecked against the book.",
        "REFERENCE_REQUESTS 1 (stable-limit source for L10 and L09) and the Blitzstein locator read are outside slice a and unchanged by this round.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 4 at 4eb6788 (delta from a007712 read hunk by hunk for slice a: index.html:33; L02.html:496, :507; L03.html:487, :498; L04.html:52, :405; cards M4-c199). "
        "Every row was re-derived this round; no row is carried from round 3. Round-3 FAIL rows L02-FOOTER-SCOPE, L03-FOOTER-SCOPE and L04-TERM-ORDER are fixed and now PASS. "
        "Round-3 FAIL L03-STD-NORMAL-DUP persists, unchanged in L03.html:117-124 and L06.html:63-66. NOTATION-A moves from PASS to FAIL because phi is unregistered and shared with L07. "
        "A-G08 is a repository format gate outside slice a (file under ledgers/M3/retired); it is recorded so the verdict is honest, and it does not depend on any slice-a file. "
        "Slice a has no grader, so mutation testing does not apply under the rulings and mutants is empty. "
        "Not checked: the Blitzstein book itself (no access; no page attributes a statement to it); a unit-wide live verify_refs run (carried reasoning above); render_curriculum.py (it writes generated files, not run); project.html, L05-L10 bodies and the other slices, except where the hub or L02/L03 cite them; a Pyodide run outside page_smoke (page_smoke ran the browser Pyodide boot and each slice lab)."
    ),
    "summary": "",
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = (
    f"Slice a round 4 at 4eb6788: {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. "
    "FAIL rows: A-G08 (repository ruff format, file under ledgers/M3/retired, outside slice a), L03-STD-NORMAL-DUP (standard normal law defined in L03 and again in L06, used before its owner), "
    "NOTATION-A (phi unregistered and shared with the L07 characteristic function), L04-REMARK-1-3 (Remark 1.3 says two tables; the lab applies the cell test to three). "
    "Gates run by me and PASS: check_pages, check_dag, check_projects, run_labs 13/13, twins alone under python -I -W error, page_smoke for the slice pages, ruff check, mypy strict, relevant pytest, verify_refs --offline, build_site --check."
)

out = ROOT / "ledgers" / "M4" / "M4-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} rows={len(rows)} counts={counts}")
sys.exit(0)
