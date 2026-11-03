"""Build the round-3 fragment for M4 slice a (ledgers/M4/M4-a.json). Row evidence cites the r3 scripts and logs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
G = "ledgers/M4/scripts/M4-a-r3/m4a_r3_gates"
S = "ledgers/M4/scripts/M4-a-r3"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---------------- gates
row(
    "A-G01",
    "2.9 structure: check_pages --unit M4",
    "course/modules/M/M4/index.html, L01.html..L04.html",
    "PASS",
    f"Run at a007712: .venv/bin/python tools/check_pages.py --unit M4 -> 'check_pages M4: PASS', exit 0 ({G}/check_pages.log).",
)
row(
    "A-G02",
    "2.9 DAG: check_dag --unit M4",
    "course/modules/M/M4/index.html, L01..L04.html",
    "PASS",
    f"Run at a007712: tools/check_dag.py --unit M4 -> 'check_dag M4: PASS', exit 0 ({G}/check_dag.log). check_dag reads only data-concept definitions, so it does not see the L03 normal-law definition (row L03-STD-NORMAL-DUP).",
)
row(
    "A-G03",
    "2.6 projects: check_projects --unit M4 (unit-wide, outside slice a)",
    "course/modules/M/M4/project.html",
    "PASS",
    f"Run at a007712: tools/check_projects.py --unit M4 -> 'check_projects M4: PASS', exit 0 ({G}/check_projects.log). project.html is another slice and is not verified here.",
)
row(
    "A-G04",
    "2.5 labs: run_labs --unit M4",
    "tests/labs/M4/lab-M4-L01-1.py..L04-1.py",
    "PASS",
    f"Run at a007712: tools/run_labs.py --unit M4 -> 'run_labs M4: PASS (13/13)', exit 0 ({G}/run_labs.log).",
)
row(
    "A-G05",
    "2.5 labs: twins alone under python -I -W error; page code equals twin; expected block equals stdout",
    "tests/labs/M4/lab-M4-L01-1.py..L04-1.py; course/modules/M/M4/L01..L04.html",
    "PASS",
    f"{S}/m4a_r3_twins.py run as python3 -I -W error from empty scratch dirs (output {S}/m4a_r3_twins.out): L01 exit 0, stderr 0 bytes, 20 stdout lines; L02 10; L03 8; L04 18; page_code_equals_twin True and expected_equals_stdout True for all four; 'ALL OK'.",
)
row(
    "A-G06",
    "2.9 page_smoke (slice pages alone)",
    "course/modules/M/M4/index.html, L01..L04.html",
    "PASS",
    f"Run at a007712: tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04 -> 'page_smoke M4: PASS', exit 0, each lab 0.0 s ({G}/page_smoke.log). Playwright browser, not a real Pyodide run (see notes).",
)
row(
    "A-G07",
    "gate: ruff check .",
    "whole repository",
    "PASS",
    f"Run at a007712: .venv/bin/ruff check . -> 'All checks passed!', exit 0 ({G}/ruff_check_final.log).",
)
row(
    "A-G08",
    "gate: ruff format --check .",
    "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3",
    "FAIL",
    f"Run at a007712: .venv/bin/ruff format --check . -> '1 file would be reformatted' (ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3:1), exit 1 ({G}/ruff_format_final.log). The file was added by commit a007712 (git log -- that path); the round-2 pin c737272 reported '473 files already formatted'. Outside slice a; this is a repository gate failing at the pin.",
    "Owner of the M3 retired ledger artifact: run .venv/bin/ruff format on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py (formatting only), then re-run .venv/bin/ruff format --check . until it reports 0 files to reformat.",
)
row(
    "A-G09",
    "gate: mypy strict (mypy --no-incremental)",
    "whole repository",
    "PASS",
    f"Run at a007712: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 331 source files', exit 0 ({G}/mypy.log).",
)
row(
    "A-G10",
    "gate: relevant pytest",
    "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py, test_page_smoke.py, test_curriculum.py",
    "PASS",
    f"Run at a007712: .venv/bin/pytest -q <six files> -p no:cacheprovider -> all dots, exit 0 ({G}/pytest_relevant.log).",
)
row(
    "A-G11",
    "2.1 citations: verify_refs (blitzstein2019introduction)",
    "references/references.json:3127-3170",
    "PASS",
    "Carried from round 1 (references/, tools/ and notation/ byte-identical since the previous pin d0f39c09: git diff --quiet d0f39c09 a007712 -- references tools notation exits 0). Round-1 live run at d0f39c09: tools/verify_refs.py --unit M4 (live, Crossref) -> '1 of 560 entries, 0 problems' (D-M4-a.round1.json, row A-G10). Re-run this round: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ("
    + G
    + "/verify_refs_offline.log). The live Crossref run was not repeated this round.",
)
row(
    "A-G12",
    "scope: slice-a delta since the previous pin c737272 (a007712)",
    "index.html:52, :62; L03.html:7, :123, :133, :281, :406; cards.json M4-c028, c029, c033, c047, c183, c219, c084",
    "PASS",
    "git diff c737272 a007712 read hunk by hunk for slice a (index.html: objective 4 and the prerequisite sentence; L03.html: meta description, Definition 2.7, Proposition 2.8 proof, misconception 2, key-results row; cards.json: wording of c028, c029, c033, c047, c183). c084 is read because c219 was compared with it. Other delta hunks belong to other slices and are not in this fragment. Each changed subject carries its own row below; the previous non-PASS rows are re-verified there.",
)

# ---------------- hub index.html
row(
    "A-H01",
    "2.9 structure: hub section order and minimum counts (BUILDER 4)",
    "course/modules/M/M4/index.html:29, :45, :58, :68, :145, :162, :173, :178",
    "PASS",
    "Re-read index.html lines 1-189 in full. Order: objectives (:45), prerequisites (:58), placement (:68), lessons (:145), ladder (:162), data (:173), reading (:178). Counts: 6 objectives (min 4, measurable verbs), 10 placement items, 10 lesson cards, 4 rungs.",
)
row(
    "A-H02",
    "2.9 hours arithmetic",
    "index.html:29, :39-42, :147; L01..L10 data-hours",
    "PASS",
    "data-hours-lessons=90 and data-hours-project=30 (:29); 10 lessons with data-hours=9 (grep over L01..L10); 90 + 30 = 120 = curriculum.json M4 hours 120; 30/120 = 25% (:42); hours-split widths 75%/25% (:40).",
)
row(
    "A-H03",
    "2.9 objectives: measurable verbs and lesson mapping",
    "index.html:49-54",
    "PASS",
    "Six objectives with verbs compute, derive, decide, state, show, apply; each maps to lessons 1, 2, 3, 4-5, 6, 9-10. Objective 4 'show that zero covariance does not imply independence' is L04 Example 1.9 (L04.html:131-133), with the covariance matrix in L05.",
)
row(
    "A-H04",
    "2.9 prerequisites vs curriculum",
    "index.html:35, :61-65",
    "PASS",
    "curriculum.json M4 prereqs ['M2']; the hub says M2 and, through M2, M1. Concept links in the hub and in every M4 page point only to M1 and M2 concepts (concept-owner scan: M4 59 links, M2 10, M1 4; no M3 link). check_dag PASS.",
)
row(
    "A-H05",
    "2.2/1.10 hub claim: matrix facts are derived from the quadratic form in Lessons 5 and 8",
    "index.html:35, :62 vs L05.html Definition 2.1, Proposition 2.3 and L08.html Proposition 1.3, Proposition 2.1",
    "PASS",
    "L05 defines the covariance matrix (Definition 2.1) and proves it positive semidefinite (Proposition 2.3); L08 proves mean and covariance of a linear image (Proposition 1.3) and that a singular covariance has no inverse (Proposition 2.1). The claim holds; L05 and L08 are other slices, read here only for this claim.",
)
row(
    "A-H06",
    "2.9 placement diagnostic: items, bar, skill checks",
    "index.html:68-143",
    "PASS",
    "Ten items (data-mastery 0.8 = 8 of 10). Items 1-8 test M1/M2 prerequisites (negation, limit 0, integral 1/2, derivative r e^{rt}, ln e^3 = 3, geometric sum 15/8, discount 1/(1+r), partial derivative 2xy); items 9 and 10 carry data-skill (rung 1 quantile, rung 2 scale). Option keys verified by hand.",
)
row(
    "A-H07",
    "3 attribution: placement explanation cites 'M1 Theorem 3.1'",
    "index.html:79 vs course/modules/M/M1/L01.html:79",
    "PASS",
    "M1 L01.html:79 reads 'Theorem 3.1 (negating one quantifier)'. The explanation (negation of 'for every x, P(x)' is 'for some x, not P(x)') matches. course/modules/M/M1 unchanged between c737272 and a007712 (git diff --quiet).",
)
row(
    "A-H08",
    "2.2 numbers in placement answers and explanations",
    "index.html:90-140",
    "PASS",
    "Recomputed: numeric answers 0.5 (tol 0.001), 3, 1.875 (15/8), 1 (rung 1: F(0)=1/4 < 1/2, F(1)=3/4 >= 1/2), 0.6 (= 3/5, from Var of t_5 = 5/3 and s^2 = 3/5). Script "
    + S
    + "/m4a_r3_numbers.py (112 checks, FAILS 0).",
)
row(
    "A-H09",
    "2.2/2.4 skill check (rung 2) hypothesis and its sources",
    "index.html:137-140 vs L06.html:158-160 (Proposition 2.6) and L02.html:105-107 (Proposition 2.3)",
    "PASS",
    "L06 Proposition 2.6 (assuming Assumption 1): for positive integer nu > 2, Var = nu/(nu-2), so Var = 5/3 at nu = 5. L02 Proposition 2.3 is stated on a finite probability space, which is what the hub says. The scale rule for Student-t is labelled a hypothesis, as the hub states.",
)
row(
    "A-H10",
    "2.7/2.9 hub lesson cards L01-L10 agree with lesson titles and results",
    "index.html:149-158 vs L01..L10 h1 and theorem titles",
    "PASS",
    "L01-L04 card texts read against the lessons (see lesson rows). L05 card: bound on correlation (Proposition 1.5), covariance matrix positive semidefinite (Proposition 2.3). L06 card: Definition 1.1, Proposition 1.5, Definition 2.5, Proposition 2.6. L07 card: Proposition 1.3 (normal MGF by completing the square), Proposition 2.5 (two-point law). L08 card: Proposition 1.3, Proposition 2.1. L09 card: Chebyshev (Proposition 1.1), weak law (Theorem 1.3), Proposition 2.3, distribution-function limit stated not established (Assumption 1 and Definition 2.4). L10 card: Definition 1.1, Lab 1, Definition 2.4. Titles match the h1 lines. L05-L10 bodies belong to other slices.",
)
row(
    "A-H11",
    "2.9 ladder: four rungs in order; names agree with project.html",
    "index.html:162-171 vs project.html:44-47, :108, :202-224",
    "PASS",
    "Rung titles Worked example, Completion problem, Independent project, Stretch in order (project.html:44-47 uses the same four). Hub names tail_risk.py, matched_scale, simulate_losses and quantile_99; project.html:202 and :108 name the same functions. Rung 2 blanks: matched factor and quantile index (project.html:45, :148).",
)
row(
    "A-H12",
    "2.8 data status and SIMULATED labels",
    "index.html:37, :175, :187",
    "PASS",
    "No data: index.html:37 and :175 say no real data and that labs compute from formulas and seeds; no data-files attribute and no data-chart on any slice-a page (scan output "
    + S
    + "/m4a_r3_prose.out). The seeded samples in L02 and L03 are labelled SIMULATED on their pages (rows below).",
)
row(
    "A-H13",
    "2.1 reading list and citation blitzstein2019introduction",
    "index.html:178-184; references/references.json:3127-3170",
    "PASS",
    "Registry record: year 2019, ISBN 9780429428357, publisher Chapman and Hall/CRC, no edition field, source_strings ['Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)'], status verified (Crossref). The hub's description of that record matches it, and the hub says the 2nd ed. was not checked against the book. No locator or attributed statement appears on any slice-a page (no data-locator; index.html:181 is an empty data-cite list item).",
)
row(
    "A-H14",
    "2.6 curriculum facts for the hub: no debate, no Atlas milestone, part and tier",
    "index.html:31, :37",
    "PASS",
    "curriculum.json M4 entry keys: id, title, tier F, hours 120, prereqs, core, introduces, sources, lab, project, part M. No debate key and no atlas key. Part code M is titled 'Mathematics'. Plan lines 22-23 agree.",
)
row(
    "A-H15",
    "2.9 hub footer",
    "index.html:187",
    "PASS",
    "Footer: 'Seeded samples are SIMULATED; no real data is used.' Accurate for the hub, which contains no sample.",
)

# ---------------- L01
row(
    "L01-PROSE",
    "2.2 numbers and claims in prose",
    "L01.html:37-51, :55-69, :95-99, :129-135, :277-297, :360-370",
    "PASS",
    "Re-derived with Fraction: Example 1.3 P(X <= 1) = 5/6; Example 3.5 ceil(148.5) = 149 and 148/150 = 74/75 = 0.987 < 0.99; Example 3.6 F-values 1/10, 3/10, 3/5, 4/5, 9/10, 1 and Q(1/2) = 0, Q(3/5) = 0, Q(61/100) = 1; canon bullet 1 strict-rule value 1 at p = 3/5. Script "
    + S
    + "/m4a_r3_numbers.py.",
)
row(
    "L01-MATH",
    "2.4 definitions, Prop 2.2, Def 3.1, Prop 3.2, Remark 3.3, Prop 3.4 and proofs",
    "L01.html:57-126",
    "PASS",
    "Each proof read in full. Prop 2.2(d) jump p_k; Prop 3.2 infimum argument; Remark 3.3 left-continuity handles p = F_{k-1} with F_{k-2} < F_{k-1} from positive weights; Prop 3.4 ceiling index. No gaps found.",
)
row(
    "L01-LAB",
    "2.5 lab: hypothesis, output, interpretation",
    "L01.html:138-270; tests/labs/M4/lab-M4-L01-1.py",
    "PASS",
    "Twin output equals the 20-line expected block (A-G05). Hypothesis values (Q(1/20) = Q(1/10) = -2, Q(11/100) = -1, Q(1/2) = Q(3/5) = 0, Q(61/100) = 1, Q(9/10) = 2, Q(91/100) = Q(99/100) = Q(1) = 3) re-derived. Interpretation consistent with the printed lines, including the eps = 1e-9 jump lines.",
)
row(
    "L01-PROBLEMS",
    "2.4 problem set worked solutions (12 problems)",
    "L01.html:302-405",
    "PASS",
    "All twelve solutions re-derived: M1 (F and Q(1/2)=0), M2 (F(5)=7/10, Q(7/10)=5, Q(71/100)=7), M3 (indices 36 and 37), P1-P3, E1 (Q(99/100)=3), E2, E3, R1 (strict rule gives 1 at p = 3/5), R2, R3.",
)
row(
    "L01-QUIZ",
    "2.9 retrieval quiz: 9 items, answers and explanations",
    "L01.html:424-494",
    "PASS",
    "Answers re-derived: Q(1/2)=1 for (1/4,1/2,1/4); Q(61/100)=1; no continuity at x_k; 198; 149; P(X<=1)=0.833; Q(F(x_k))=x_k; 5/6 decimal; Q(1)=x_m. Every item has an explanation div.",
)
row(
    "L01-GRADES",
    "2.3 grades on theorems and key-results rows",
    "L01.html:43-48, :80, :103, :114, :119, :413-418",
    "PASS",
    "Props 2.2, 3.2, 3.4 and Remark 3.3 are graded T with proofs on the page. Key-results rows graded T cite proof sections or exact arithmetic on a stated table.",
)
row(
    "L01-FWD",
    "5 terms used before definition: quantile (L01.html:51) and infimum (L01.html:37)",
    "L01.html:37, :51",
    "PASS",
    "Both forward uses carry explicit pointers ('defined in §3 where it is first used', 'defined in Definition 3.1 below').",
)

# ---------------- L02
row(
    "L02-PROSE",
    "2.2 numbers and claims in prose",
    "L02.html:51, :55, :84-90, :134-141, :262, :267-273, :281-293, :358-372",
    "PASS",
    "Re-derived: 35/12 and sqrt(35/12) = 1.708; 91/6 = 15.17; Var 2.92; E[L] = 12500; E[L^2] = 3125000000; Var(L) = 2968750000; sd 54486.24; D = L/100 Var 296875 and sd 544.8624; expected count 500 and 11 below; 489 x 250000 = 122250000; mean 12225.0; loss-table mean 3/10 (canon). Script "
    + S
    + "/m4a_r3_numbers.py.",
)
row(
    "L02-MATH",
    "2.4 definitions, Props 1.2-1.3, 2.2-2.4, Def 1.6 and proofs",
    "L02.html:57-132",
    "PASS",
    "Proofs read in full; Prop 2.2 applies Prop 1.3 with U = X^2, V = X; Prop 2.4 sums nonnegative terms with p_k > 0; Def 1.6 is stated as unused by the lesson, and it is.",
)
row(
    "L02-LAB",
    "2.5 lab: hypothesis, output, interpretation",
    "L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py",
    "PASS",
    "Twin output equals the 10-line expected block (A-G05): 3.469 (seed 2026), 489 losses and 122250000 cents (seed 2027). The interpretation's three 'True' lines are the three printed True lines (lines 253, 254, 256). The difference -0.031 is printed.",
)
row(
    "L02-PROBLEMS",
    "2.4 problem set worked solutions (12 problems)",
    "L02.html:298-401",
    "PASS",
    "M1 21/100; M2 cents values 5000, 2.25e8, 15000; M3 36 and 4; P1-P3 proofs (P3: U and V=-U give Var 0 vs 2); E1-E3 (489 is 11 below 500; ratio of scale check); R1-R3 (296875 and 544.8624 currency units; mean 3/10 versus quantile 0).",
)
row(
    "L02-QUIZ",
    "2.9 retrieval quiz: 10 items",
    "L02.html:421-492",
    "PASS",
    "Answers 3.5, 1, 12, E[(X-E X)^2], 5000, 225000000, 21/100, c = E[X], 15000, 5 all re-derived with explanations.",
)
row(
    "L02-MISC",
    "2.9 misconceptions: 4 wrong beliefs refuted on the page",
    "L02.html:279-296",
    "PASS",
    "Four labelled wrong beliefs (expectation is a value, scaling by a, variance is E[X^2], seeded sample mean equals expectation), each refuted with a computed number from this lesson.",
)
row(
    "L02-CANON",
    "2.2/1.10 cross-lesson claims in 'Where the canon breaks'",
    "L02.html:267-273 vs L06.html:158-160 (Proposition 2.6) and L10.html",
    "PASS",
    "L06 Proposition 2.6 (under its Assumption 1): for nu <= 2, E[t^2] = infinity, which is the 'no finite variance' statement. L10 treats heavy tails (L10.html Definition 1.1). The mean-versus-quantile example recomputed: E[X] = 3/10, Q(1/2) = 0.",
)
row(
    "L02-FWD-COVARIANCE",
    "1.10 forward pointer in P3 to Lesson 4 Proposition 1.7 and Lesson 5",
    "L02.html:347 vs L04.html:103-104 and L05.html Proposition 1.1 and its Problem M3 (L05.html:320-330)",
    "PASS",
    "L04 Proposition 1.7 is the covariance shortcut. L05 gives bilinearity (Proposition 1.1) and works Var(X+Y) through it in Problem M3, so 'Lesson 5 develops it' holds.",
)
row(
    "L02-FOOTER-SCOPE",
    "2.9 scope words: 'every result is proved or an exact computation' (footer and references)",
    "L02.html:496 (References) and :507 (footer)",
    "FAIL",
    "Footer (line 507): 'Every result is proved on the page or is an exact computation on a stated list. No real data is used; the seeded samples are SIMULATED.' The same claim is at line 496. Lab 1 prints seeded-sample results ('die sample, seed 2026 ... mean 3.469'; 'loss sample, seed 2027 ... losses 489, total 122250000 cents'). Those are neither proofs nor exact computations, and the page itself grades them C (cards.json M4-c030 and M4-c033: grade C, basis 'Lab 1 (SIMULATED)'). The 'every' claim is false as written.",
    "Rewrite L02.html:496 and :507 to separate the two kinds of result, for example: 'Each exact result is proved on the page or is an exact computation on a stated list. The seeded samples in Lab 1 are SIMULATED single-run estimates, graded C, and are not proofs.'",
)

# ---------------- L03
row(
    "L03-PROSE",
    "2.2 numbers and claims in prose",
    "L03.html:51, :55-76, :113, :138, :258, :263-268, :281, :350-350, :382",
    "PASS",
    "Re-derived: mu = 7/4; m2 = 163/16; m3 = 2157/32 (terms -1372, -54, +1, +35937 over 512; the value-10 term exceeds m3 by 1425/512); m4 = 149461/256; gamma_3^2 = 18610596/4330747; skewness 2.0730 and kurtosis 5.6254 (4 dp), 2.073 and 5.625 (3 dp); Bernoulli p = 1/10 gives gamma_3 = 8/3, gamma_4 = 73/9 = 8.11, squared skew 64/9; p = 1/4 gives gamma_4 = 7/3; gaps 0.008 and 0.045. Script "
    + S
    + "/m4a_r3_numbers.py (112 checks, FAILS 0).",
)
row(
    "L03-MATH",
    "2.4 Props 1.1, 2.2, 2.3, 2.4, Example 2.5 and section 3 arithmetic",
    "L03.html:57-114, :138",
    "PASS",
    "Proofs read in full. Prop 2.3: sigma_Y = |a| sigma_X, Z_Y = sign(a) Z_X. Prop 2.4 equality case: W = Z^2 constant forces Z = +-1 and E[Z] = 0 forces probability 1/2. Example 2.5: m3 = pq(q-p), m4 = pq(1-3pq), gamma_3 = (1-2p)/sqrt(pq), gamma_4 = (1-3pq)/(pq). All re-derived.",
)
row(
    "L03-PROP28-SCOPE",
    "2.4 Proposition 2.8 proof needs no hypothesis the statement omits (was FAIL in round 2)",
    "L03.html:127-128 (statement), :133 (proof), :122-124 (Definition 2.7)",
    "PASS",
    "Re-verified from scratch. The statement names its hypothesis (Assumption 2.6). Definition 2.7 (L03.html:123, changed at a007712) states that the kurtosis of the standard normal is E[Z^4] with Z itself as the standardized variable and that the finite-space hypothesis of Definition 2.1 is not used. The proof (L03.html:133, changed) uses only E[Z] = 0, E[Z^2] = 1 and Assumption 2.6, and says the Definition 2.1 hypothesis is not used. Proof steps re-derived: odd integrand; integration by parts with zero boundary terms; E[Z^4] = 3 E[Z^2] = 3.",
)
row(
    "L03-STD-NORMAL-DUP",
    "1.10 concept defined twice and used before its owner lesson: standard normal law",
    "L03.html:117-118 (Assumption 2.6 density sentence), :122-124 (Definition 2.7) vs course/modules/M/M4/L06.html:63-66 (Definition 1.1, dfn normal-distribution)",
    "FAIL",
    "L03 defines the standard normal law and its density phi (Assumption 2.6: 'The standard normal density is phi(z) = ...'; Definition 2.7: 'A random variable Z is standard normal when P(Z in B) = integral over B of phi(z) dz'). L06.html:65 defines it again: 'The standard normal law is N(0,1), with density phi(z) = e^(-z^2/2)/sqrt(2 pi). A variable Z with this law is a standard normal variable.' The concept normal-distribution is owned by L06 (plans/M4-build-plan.md:96; curriculum.json concept 'Normal distribution', module M4), and BUILDER_RULES 1.10 forbids a concept used before its lesson and defined twice. check_dag passes only because Definition 2.7 is not a dfn element.",
    "Architect ruling needed, because a DAG link from L03 to L06 is forbidden. Either (a) remove the standard-normal definition and density sentence from L03 (Assumption 2.6 and Definition 2.7) and move the normal-kurtosis result to L06, where Proposition 1.5 currently gives only E[Z] = 0 and E[Z^2] = 1 and E[Z^4] = 3 would have to be added; or (b) request that normal-distribution be owned by L03, and change L06 Definition 1.1 to a link. Card M4-c219 and the key-results row at L03.html:406 change with either option. Re-run check_dag and the cards check after the change.",
)
row(
    "L03-LAB",
    "2.5 lab: hypothesis, output, interpretation",
    "L03.html:140-259; tests/labs/M4/lab-M4-L03-1.py",
    "PASS",
    "Twin output equals the 8-line expected block (A-G05): sample skewness 2.065 and kurtosis 5.580 for seed 2026, n = 20000, against exact 2.073 and 5.625. The interpretation's gaps 0.008 and 0.045 are correct, and the rounding bound (0.001) is correct.",
)
row(
    "L03-CANON",
    "2.2 canon bullets; attribution to Lesson 10 Proposition 2.3",
    "L03.html:263-269 vs L10.html:65-66 (Assumption 1) and :150-152 (Proposition 2.3)",
    "PASS",
    "Law -2, 1, 3 with 2/5, 1/2, 1/10: mean 0, m2 = 3, m3 = 0, m4 = 15, gamma_4 = 5/3, not symmetric (re-derived). L10 Proposition 2.3 (under its Assumption 1): E[V^4] = infinity for the Student-t with nu = 3, so the L03 sentence is accurate.",
)
row(
    "L03-MISC",
    "2.9 misconceptions (3)",
    "L03.html:275-287",
    "PASS",
    "Symmetry misconception refuted by the section 4 law; kurtosis-of-every-law refuted by 73/9 and 7/3 and the point p = (1 - 1/sqrt 3)/2 with pq = 1/6 gives gamma_4 = 3 (re-derived); sign-of-a misconception by Proposition 2.3.",
)
row(
    "L03-PROBLEMS",
    "2.4 problem set worked solutions (12 problems)",
    "L03.html:290-393",
    "PASS",
    "M1 (p = 1/4: sigma = sqrt3/4, gamma_3 = 2/sqrt3 about 1.155, gamma_4 = 7/3); M2 (0 and 2: gamma_4 = 1); M3 (m3 = 2157/32, positive sign); P1-P3 identities; E1 gaps; E2 64/9 and 73/9; E3 weights total 8; R1 equality case; R2 73/9 about 8.11 and the tail point; R3.",
)
row(
    "L03-QUIZ",
    "2.9 retrieval quiz: 9 items",
    "L03.html:413-483",
    "PASS",
    "Answers 0, E[Z^3], 1, sign change, unchanged, 5/3 (1.6667), the section 4 law, 8/3 (2.6667), zero all re-derived with explanations.",
)
row(
    "L03-GRADES",
    "2.3 grades: Props 1.1, 2.2-2.4 and 2.8 (T); key-results rows",
    "L03.html:42-49, :57-134, :401-407",
    "PASS",
    "Theorems carry T on the title. Proposition 2.8 is graded T and names Assumption 2.6 in its statement and in the key-results row (line 406). The row 'Arithmetic on the page' (line 407) is correct.",
)
row(
    "L03-FOOTER-SCOPE",
    "2.9 scope words: 'every result is proved or an exact computation' (footer and references)",
    "L03.html:487 (References) and :498 (footer)",
    "FAIL",
    "Footer (line 498): 'Every result on this page is proved on the page or is an exact computation on a stated table; the normal kurtosis (Proposition 2.8) is proved under Assumption 2.6. No real data is used; the seeded sample in Lab 1 is SIMULATED.' Lab 1 prints a seeded-sample result (sample skewness 2.065 and kurtosis 5.580, seed 2026, n = 20000) which is neither a proof nor an exact computation, and the page's own card M4-c047 and M4-c183 grade it C with basis 'Lab 1 (SIMULATED), seed 2026'. The same sentence is at line 487.",
    "Rewrite L03.html:487 and :498 to separate the kinds of result, for example: 'Each exact result is proved on the page or is an exact computation on a stated table; the normal kurtosis (Proposition 2.8) is proved under Assumption 2.6. The seeded sample in Lab 1 is a SIMULATED single-run estimate, graded C, and is not a proof.'",
)

# ---------------- L04
row(
    "L04-PROSE",
    "2.2 numbers and claims in prose",
    "L04.html:52, :130-133, :169, :300, :306-308, :318-326",
    "PASS",
    "Re-derived: Example 1.9 E[Y] = 2/3, E[XY] = 0, Cov = 0, p(0,0) = 1/3 vs 1/9; Example 2.5 P(Y=0) = 2/5, P(Y=1) = 3/5, E[X] = 4/5, E[X|Y=0] = 1, E[X|Y=1] = 2/3, total 4/5; canon bullet 2 p(0,0) = 1/2 vs 1/4; canon bullet 3 E[XY] = 1 vs E[X]E[Y] = 0. Script "
    + S
    + "/m4a_r3_numbers.py.",
)
row(
    "L04-TERM-ORDER",
    "5 terms used before definition: 'joint table'",
    "L04.html:52 (why-it-matters) vs L04.html:59 (Definition 1.1)",
    "FAIL",
    "The why-it-matters paragraph says 'the joint table of their probabilities records which' before Definition 1.1 defines a joint table, and it gives no forward pointer. L01 gives its forward term an explicit pointer ('defined in Definition 3.1 below'). Minor, but it breaks the define-before-use rule (BUILDER_RULES 8).",
    "L04.html:52: replace 'the joint table of their probabilities' with 'the table of joint probabilities (Definition 1.1 below)'.",
)
row(
    "L04-MATH",
    "2.4 Defs 1.1-2.1, Props 1.4-1.8, 2.3-2.4, Remark 2.2 and proofs",
    "L04.html:58-165",
    "PASS",
    "All proofs read. Prop 1.4 (P(A and B) = 0 vs P(A)P(B) > 0); Prop 1.5 factorization over cells; Prop 1.7 expansion; Prop 1.8; Prop 2.3 sum over y with P(Y=y) > 0; Prop 2.4 (P(X=x | Y=y) = P(X=x)). Covariance is defined in Definition 1.6 and is not a dfn element; see registry flag on the ownership of the covariance concept.",
)
row(
    "L04-LAB",
    "2.5 lab: hypothesis, output, interpretation",
    "L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py",
    "PASS",
    "Twin output equals the 18-line expected block (A-G05): product table cell 3/50 both sides; dependent table cell 1/10 vs 4/25; Example 1.9 covariance 0 with cell 1/3 vs 1/9; Part C E[X|Y=0] = 1, E[X|Y=1] = 2/3, total 4/5 equal to E[X]. Interpretation: three exact tables, as the code shows.",
)
row(
    "L04-PROBLEMS",
    "2.4 problem set worked solutions (12 problems)",
    "L04.html:331-434",
    "PASS",
    "M1 product 0.12 vs 0.1 (dependent); M2 2/3; M3 cells 1/8, 1/8, 3/8, 3/8 and E[XY] = 1/8 by two methods; P1-P3 (P3 Cov = -ab); E1 total expectation; E2 ratio 3; E3 ratio 5/8 = 0.625; R1 Cov 0 with dependence; R2; R3.",
)
row(
    "L04-QUIZ",
    "2.9 retrieval quiz: 10 items",
    "L04.html:453-528",
    "PASS",
    "Answers: not independent (1/3 vs 1/9); E[X|Y=0] = 1; E[XY] = E[X]E[Y]; E[X] = 0.8; events dependent; Cov = 0; total-expectation sum; P(Y=1) = 0.6; equal conditional expectations do not imply independence; product-table cell 0.06. All re-derived.",
)
row(
    "L04-CANON-MISC",
    "2.2 canon bullets and misconceptions (3)",
    "L04.html:303-329",
    "PASS",
    "Zero covariance is not independence (Example 1.9); marginals do not fix the joint table (1/2 vs 1/4); product rule for means under dependence; conditional expectation limited to finite tables; misconception on zero covariance, disjoint events and conditional expectation each refuted by a printed or computed value.",
)
row(
    "L04-FOOTER",
    "2.2 scope words in footer and references ('every result ... derived on the page')",
    "L04.html:532, :543",
    "PASS",
    "L04 has no seeded sample. Every printed lab value (Parts A-C) is an exact computation on a stated table and is derived in the page text (3/50, 1/10, 4/25, 1/3, 1/9, 1, 2/3, 4/5). The 'grade T' phrasing matches the key-results table.",
)

# ---------------- cards
row(
    "CARDS-DUP",
    "2.7 full scan for duplicates (cards.json, all 212 cards)",
    "course/modules/M/M4/cards.json",
    "PASS",
    f"Script {S}/m4a_r3_prose.py: duplicate fronts across the deck: []; duplicate ids: none. Near pairs test distinct facts: c023 (scale rule) and c028 (misconception on scaling); c046 (sign reversal) and c215 (general affine map, skewness) overlap in content but differ in question and hypothesis; c061 and c065 are complementary (under independence vs not).",
)
row(
    "CARDS-L01",
    "2.7 cards L01: 16 numbered cards plus c173, c192-c195, c197, c198 (23)",
    "cards.json",
    "PASS",
    "All 23 read against the lesson. Hypotheses stated where the result needs them (c005, c006, c008, c009, c013, c022, c024). Numbers 198, 149, 0, 1/2 and the grid check appear in L01 (script output: missing = []).",
)
row(
    "CARDS-L02",
    "2.7 cards L02: 17 numbered cards plus c181, c182, c199 (20)",
    "cards.json",
    "PASS",
    "All 20 read. c029 has its hypothesis (finite, positive weights) after the round-2 fix. c030 and c033 are grade C with basis 'Lab 1 (SIMULATED)' and their numbers (3.469, 489) are reproduced by the twin (A-G05). c181 (1.708) and c031 (54486.24) appear in L02.",
)
row(
    "CARDS-L03",
    "2.7 cards L03: 15 numbered cards plus c183, c200, c212, c214, c215, c219, c220 (22)",
    "cards.json",
    "PASS",
    "All 22 read against Section 2-4 and the quiz. c047 and c183 are grade C with basis and reproduce the twin's seed-2026 lines (2.065, 5.580). c042, c043, c044, c045, c048, c200 numbers verified (7/4, 163/16, 5/3, 7/3, 64/9, 2157/32, 149461/256). The normal-law cards (c219, c220) are correct against the L03 text; their definition duplication is the L03-STD-NORMAL-DUP row.",
)
row(
    "CARDS-L04",
    "2.7 cards L04: 18 numbered cards plus c201, c204 (20)",
    "cards.json",
    "PASS",
    "All 20 read. c062 (E[X|Y=0] = 1 from (0*1/10 + 1*2/10 + 2*1/10)/(2/5)), c064 (Cov = -ab), c065 (2/3 and 4/5), c066 (Cov(X,X) = Var X), c204 (equal conditional expectations, dependent pair) re-derived.",
)
row(
    "CARDS-NUMBERS",
    "2.7 every card number appears in its lesson",
    "cards.json (L01-L04 cards) vs L01..L04.html",
    "PASS",
    f"Script {S}/m4a_r3_prose.py: 85 slice-a cards checked; numbers absent from the lesson text: []. Lab-output numbers in cards appear in the expected blocks.",
)
row(
    "CARD-M4-c219",
    "2.7 card truth and duplicates (was FAIL in round 2)",
    "cards.json, ids M4-c219 (L03) and M4-c084 (L06)",
    "PASS",
    "Re-verified. The round-2 duplicate was c084 restating the standard-normal sentence. a007712 changed c084 to 'The law with density ... for sigma > 0 (Definition 1.1)', so c219 and c084 no longer duplicate each other. The remaining issue about the standard normal definition sits in row L03-STD-NORMAL-DUP and must be re-checked when that row is fixed.",
)

# ---------------- notation, DAG, process, data, structure
row(
    "NOTATION-A",
    "2.4/2.9 symbols vs notation/notation.json (NOTATION rule 13)",
    "index.html; L01..L04.html",
    "PASS",
    f"Registered macros in use: R (L01 Definition 1.1, 3.1 etc.) with meaning real numbers. gamma_3 and gamma_4 (L03) match the registry meaning (E[Z^3], E[Z^4], not excess). Not used on slice a: T, R^*, Phi, Q, SR. Standard LaTeX used where the registry has a macro (the operatorname Var and operatorname Cov forms for the Var and Cov macros) with the same meaning. phi (density) is not registered; it is used only inside L03 (Assumption 2.6, Definition 2.7, Proposition 2.8) and no symbol inside slice a has two meanings. Scan: "
    + S
    + "/m4a_r3_prose.out.",
)
row(
    "DAG-A",
    "1.10 / 2.9 DAG reading of slice a (concepts used before defined, defined twice)",
    "index.html; L01..L04.html",
    "PASS",
    "check_dag PASS (A-G02). Reading: L02 links random-variable (L01); L03 links random-variable, expectation, variance (L01, L02); L04 links random-variable, expectation (L01, L02); every concept link on slice-a pages points to M1 or M2 concepts or to an earlier M4 lesson. Defined-twice defect in slice a is the L03-STD-NORMAL-DUP row, which check_dag cannot see. Covariance ownership is a registry flag.",
)
row(
    "PROCESS-A",
    "2.9 banned phrases (BUILDER 1.3-1.4) and process words in learner text",
    "index.html; L01..L04.html visible text",
    "PASS",
    f"Scan {S}/m4a_r3_prose.out: banned_hits = [] on all five pages (TODO, TBD, lorem, clearly, obviously, for brevity, left as an exercise, studies show, ...). process_hits are only 'Verify' and 'verify' as learner instructions in problems (L01 E1, L02 E3, L03 E2). check_pages BANNED gate PASS.",
)
row(
    "SCOPE-A",
    "2.2 scope words (only, all, always, every, any, exactly, same) in body text",
    "index.html; L01..L04.html body text",
    "PASS",
    "Each scope word in body text is backed by a stated hypothesis or a computation: 'every moment of a finite law is defined' (finite sums); 'the only law on this page that is not finite' (L03.html:122-124, the other laws are finite tables); 'every computation uses a finite law' (L02.html:270). The two footer-level 'every result' claims are their own rows (L02-FOOTER-SCOPE, L03-FOOTER-SCOPE).",
)
row(
    "DATA-A",
    "2.8 data, figures and SIMULATED labels",
    "L01..L04.html, index.html",
    "PASS",
    f"Scan {S}/m4a_r3_prose.out: data-files count 0, data-chart count 0, no non-local script src on any slice-a page. Seeded samples are labelled SIMULATED in their hypotheses (L02.html:146, L03.html:142) and footers. No figures on slice-a pages.",
)
row(
    "STRUCT-A",
    "2.9 lesson structure (BUILDER 4.2) and counts",
    "L01..L04.html",
    "PASS",
    "why-it-matters word counts 114, 97, 97, 98 (limit 120). Misconceptions 3, 4, 3, 3 (minimum 3). Problem set: 3 problems in each of Mechanics, Proof, Empirical, Research in every lesson, each with details.solution. Retrieval quiz 9, 10, 9, 10 items (8 to 15), each with an explanation. Lab sections carry hypothesis, data-run code, expected block and interpretation. Order: why, core, inline lab, canon, misconceptions, problems, key results, quiz, references.",
)
row(
    "NUM-A",
    "2.2 re-derivation of every number in slice a (own script)",
    f"{S}/m4a_r3_numbers.py",
    "PASS",
    f"{S}/m4a_r3_numbers.py run with python -I -W error: 112 OK lines, FAILS: 0 (output {S}/m4a_r3_numbers.out). Covers hub, L01-L04 prose, examples, placement answers, cards numbers and the L03 sample-check gaps.",
)

fragment = {
    "unit": "M4",
    "slice": "a",
    "round": 3,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyD3-M4-a)",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "checkout": str(ROOT),
    "scratch": S + "/",
    "verified_at": "2026-11-03T12:00:00+00:00",
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "notation/notation.json does not register phi, the standard normal density, used in L03 Assumption 2.6, Definition 2.7 and Proposition 2.8 and in L06 Definition 1.1. phi is also the characteristic function phi_X in L07 and L09 (other slices). The registry owner must decide one symbol for each meaning.",
        "Ownership of the covariance concept: L04 Definition 1.6 defines Cov(X,Y) (not a dfn element) while the curriculum concept 'Covariance and correlation' (module M4) is assigned to L05 by plans/M4-build-plan.md. Plan open item 9 (M4-open-items.md) asks the architect to confirm. plans/FINAL-ARCHITECT-RULINGS.md has no M4 ruling on it.",
        "blitzstein2019introduction has no edition field in references/references.json; '2nd ed. (2019)' comes only from the curriculum (source_strings). The hub says so and does not assert it. Architect or registry owner may want the edition confirmed against the book.",
    ],
    "freshness_flags": [],
    "notes": (
        "Slice a = index.html, L01-L04.html, cards for L01-L04 in cards.json, and lab twins tests/labs/M4/lab-M4-L01-1..L04-1.py. "
        "Delta c737272..a007712 for slice a read hunk by hunk (A-G12). Previous non-PASS rows re-verified from scratch: L03-PROP28-SCOPE now PASS; L03-STD-NORMAL-DUP still FAIL; CARD-M4-c219 now PASS. "
        "Round-2 PASS rows for unchanged subjects were re-checked where cheap and otherwise carried only where the cited subject is byte-identical (references/tools/notation byte-identical since d0f39c09 for A-G11). "
        "Not checked: the Blitzstein book (no access; the pages attribute no statement to it); a live Crossref run (carried from round 1); a real Pyodide run (page_smoke used the Playwright browser); L05-L10 page bodies and project.html except where the hub or L02/L03 cite them; run_graders and mutate_graders (slice a contains no grader, so mutation testing does not apply under the rulings); the M3 ruff format failure belongs to another unit and was recorded, not fixed. "
        "The checkout held an uncommitted round-3 draft at ledgers/M4/M4-a.json from an earlier attempt; it was not used as evidence and this fragment replaces it. Gate logs are in "
        + G
        + "/."
    ),
    "summary": "",
}
statuses = [r["status"] for r in rows]
fragment["summary"] = (
    f"Slice a round 3 at a007712: {statuses.count('PASS')} PASS, {statuses.count('FAIL')} FAIL, "
    f"{statuses.count('UNVERIFIABLE')} UNVERIFIABLE ({len(rows)} rows). FAIL rows: A-G08 (repository ruff format gate, file in ledgers/M3/retired), "
    "L02-FOOTER-SCOPE and L03-FOOTER-SCOPE (footers and references say every result is proved or exact while Lab 1 prints seeded-sample results), "
    "L03-STD-NORMAL-DUP (standard normal law defined in L03 and again in L06, a concept owned by L06), "
    "L04-TERM-ORDER (minor: 'joint table' used before Definition 1.1). Round-2 FAIL rows L03-PROP28-SCOPE and CARD-M4-c219 now PASS. "
    "Gates run and PASS: check_pages, check_dag, check_projects, run_labs 13/13, twins alone under python -I -W error with page code and expected blocks equal, page_smoke for the slice pages, ruff check, mypy strict, six pytest modules, verify_refs --offline."
)
out = ROOT / "ledgers" / "M4" / "M4-a.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {out} rows={len(rows)} verdict={fragment['verdict']}")
