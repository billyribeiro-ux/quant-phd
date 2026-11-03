"""Write the round-3 fragment for M4 slice a (ledgers/M4/M4-a.json). Evidence strings cite the r3 scripts and outputs."""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/M4/scripts/M4-a-r3/"
PIN = "a007712fdbfc8b4851123f4de76b5310ac5a9e64"
BASE = "c737272f5bdef4a027417989cd52254555e8a0bb"
CARRY2 = "Carried from round 2 (course/modules/M/M4 files cited here byte-identical since c737272, checked by git diff c737272..a007712): "

rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates and scope
row("A-G01", "2.9 structure: tools/check_pages.py --unit M4", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    f"Re-run at {PIN}: .venv/bin/python tools/check_pages.py --unit M4 -> 'check_pages M4: PASS', exit 0 ({S}check_pages_M4.out). Re-run because index.html:53, :62 and L03.html changed since c737272.")
row("A-G02", "2.9 DAG: tools/check_dag.py --unit M4", "index.html; L01..L04.html", "PASS",
    f"Re-run at {PIN}: 'check_dag M4: PASS', exit 0 ({S}check_dag_M4.out). The delta adds no concept link (diff of L03.html and index.html read hunk by hunk, {S}delta_c737272_a007712_M4.diff).")
row("A-G03", "2.6 projects: tools/check_projects.py --unit M4 (unit-wide, not a slice-a subject)", "project.html (other slice)", "PASS",
    f"Re-run at {PIN}: 'check_projects M4: PASS', exit 0 ({S}check_projects_M4.out). project.html changed in the delta; it is outside slice a and is not verified here.")
row("A-G04", "2.5 labs: tools/run_labs.py --unit M4 --page L01..L04 and --page index", "tests/labs/M4/lab-M4-L01-1.py..L04-1.py", "PASS",
    f"Re-run at {PIN}: run_labs_L01.out, run_labs_L02.out, run_labs_L03.out, run_labs_L04.out each 'run_labs M4: PASS (1/1)', exit 0; run_labs_index.out 'PASS (0/0)' (hub has no lab).")
row("A-G05", "2.5 labs: twins alone under python -I -W error; page code equals twin; expected block equals stdout", "tests/labs/M4/lab-M4-L01-1.py..L04-1.py; L01..L04.html lab sections", "PASS",
    f"Each twin run from an empty scratch directory: .venv/bin/python -I -W error tests/labs/M4/lab-M4-L0n-1.py exit 0, stderr 0 bytes ({S}L01.out..L04.out, {S}L01.err..L04.err). {S}lab_page_vs_twin_r3.py (output {S}lab_page_vs_twin_r3.out): code_equals_twin=True and expected_equals_stdout=True for all four labs.")
row("A-G06", "2.9 page_smoke for slice pages (run alone)", "index.html, L01.html..L04.html", "PASS",
    f"Re-run: .venv/bin/python tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04 -> five 'PASS' lines, 'page_smoke M4: PASS', exit 0 ({S}page_smoke_slice_a.out). Lab runtime 0.0 s per lab in the output.")
row("A-G07", "gate: ruff", "tests/labs/M4; course/modules/M/M4", "PASS",
    f"{S}ruff_verify_refs.out: 'All checks passed!' (ruff check tests/labs/M4 course/modules/M/M4) and '13 files already formatted' (ruff format --check tests/labs/M4), exit 0.")
row("A-G08", "gate: mypy strict", "whole repository", "PASS",
    f"{S}mypy.out: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 331 source files', exit 0.")
row("A-G09", "gate: relevant pytest", "tests/test_page_checks.py, test_run_labs.py, test_labs.py, test_docs_figures.py, test_curriculum.py", "PASS",
    f"{S}pytest_relevant.out: 'pytest -q' on those five modules, 100% dots, pytest_exit=0. Not run: test_page_smoke.py and test_figure_kernels.py (see could-not-check).")
row("A-G10", "2.1 citations: tools/verify_refs.py --offline", "references/references.json (blitzstein2019introduction)", "PASS",
    f"{S}ruff_verify_refs.out: 'offline integrity: 560 entries, 0 problems', exit 0. references/ is byte-identical since c737272 (git diff --stat empty). Live Crossref run not repeated (no reference changed).")
row("A-G11", "scope: bytes of slice a since the previous pin", "index.html, L03.html, cards.json (slice-a cards), tests/labs/M4", "PASS",
    f"git diff --stat c737272..a007712: index.html 2 lines (:53 objective, :62 prerequisite paragraph); L03.html 4 hunks (:7 meta description, :123 Definition 2.7, :131-133 Proposition 2.8 proof, :281 misconception, :406 table row); cards.json 9 changed lines, card ids c028, c029, c033, c047, c183 (slice a) and c070, c084, c112, c140 (other slices). L01.html, L02.html, L04.html, tests/labs/M4/, references/, notation/, tools/ and curriculum/ are byte-identical (empty diff). Outside slice a: project.html and grader/test_project.py. Evidence: {S}delta_c737272_a007712_M4.diff, {S}slice_a_checks_r3.out.")

# ---- hub
row("A-H01", "2.9 structure: hub section order (BUILDER_RULES 4)", "course/modules/M/M4/index.html:29, :45, :58, :68, :145, :162, :173, :178", "PASS",
    CARRY2 + "index.html lines 29, 45, 58, 68, 145, 162, 173, 178 (the changed index lines are 53 and 62 only). Re-confirmed by A-G01 (check_pages PASS).")
row("A-H02", "2.9 hours arithmetic", "index.html:29, :40, :42, :147; L01..L04.html data-hours", "PASS",
    CARRY2 + "index.html:29 data-hours-lessons=\"90\" and data-hours-project=\"30\"; :42 \"90 h lessons · 30 h project (25% of 120 h)\"; :147 \"Ten lessons of nine study hours each\". Each of L01..L04 declares data-hours=\"9\" (grep of the four pages). Ten lessons of 9 h = 90 = the lesson split, 90 + 30 = 120 = the curriculum figure (curriculum.json M4).")
row("A-H03", "2.9 objectives: measurable verbs and lesson mapping", "index.html:48-55 (changed line :53)", "PASS",
    f"Re-verified (changed line). index.html:53 now reads 'Decide whether two variables are independent from a joint table, show that zero covariance does not imply independence, and compute a covariance matrix and a correlation (Lessons 4 and 5).' Decide, show and compute are measurable verbs. L04 defines independence (L04.html:65) and has Example 1.9, zero covariance without independence (L04.html:131, Cov = 0 and p(0,0) = 1/3 against 1/9); L05 defines the covariance matrix and correlation (L05.html:85, :126).")
row("A-H04", "2.9 prerequisites vs curriculum", "index.html:60-64 (changed line :62); curriculum/curriculum.json M4 entry", "PASS",
    f"Re-verified (changed line). M4 prerequisites M2 (and through M2, M1) per curriculum.json M4 entry (unchanged). The M2 and M1 concept links on index.html:62-64 are unchanged (href targets ../../../concepts.html#limit, #definite-integral, #exponential-and-logarithm, #quantifiers). Only the sentence at :62 changed.")
row("A-H05", "1.10 DAG: hub claim that Lessons 5 and 8 use no M3 concept", "index.html:62 vs course/modules/M/M4/L05.html:126-143 and L08.html:106-114", "PASS",
    "Re-verified (changed sentence). L05.html:130 defines positive semidefinite 'defined here', and Proposition 2.3 (L05.html:135) proves PSD from w^T Sigma w. The covariance matrix is defined at L05.html:126 and the quadratic form is at :136-143, so 'the quadratic form of the covariance matrix Sigma, which Lesson 5 defines' is accurate. grep -i over L05.html and L08.html for eigen, spectral, singular value, orthogonal, projection, linear map, vector space, principal component, least squares, nearest, clipping, Cholesky, determinant, inverse: the only hits are PSD (defined in L05), 'determinant' in an L05 quiz option (L05.html:490, prose) and 'inverse' in L08.html:110-114 (Proposition 2.1, prose). No M3 concept is linked or used as a term.")
row("A-H06", "2.9 placement: 10 items, mastery bar", "index.html:68-143, :70", "PASS",
    CARRY2 + "index.html:68-143 (unchanged).")
row("A-H07", "3 attribution: placement item 1 'M1 Theorem 3.1'", "index.html:79 vs course/modules/M/M1/L01.html:79", "PASS",
    CARRY2 + "index.html:79 and M1 L01.html:79 (M1 not in the delta).")
row("A-H08", "2.2 numbers in placement items 2-8", "index.html:82-131", "PASS",
    CARRY2 + "index.html:82-131 (unchanged).")
row("A-H09", "2.2 skill check rung 1", "index.html:133-135", "PASS",
    CARRY2 + "index.html:133-135 (unchanged).")
row("A-H10", "2.2 skill check rung 2 and its hypotheses", "index.html:137-140 vs L06.html:158-173, L06.html:59, L02.html:55, :115", "PASS",
    CARRY2 + "index.html:137-140 and L02.html:55, :115 (unchanged), L06 (not in the delta).")
row("A-H11", "2.9 hub lesson cards L01-L04 agree with lesson text", "index.html:149-152 vs L01..L04.html", "PASS",
    CARRY2 + "index.html:149-152. The L03 card reads 'the normal kurtosis of 3 under a stated Gaussian-integral assumption', which matches the L03 Proposition 2.8 as now written (L03.html:127-128, Assuming Assumption 2.6; kurtosis 3).")
row("A-H12", "2.9 hub card titles vs lesson h1", "index.html:149-152 vs L01..L04.html h1", "PASS",
    CARRY2 + "index.html:149-152 and the h1 of L01..L04 (unchanged).")
row("A-H13", "2.9 ladder: four rungs in order; project names", "index.html:162-171; project.html:36, :108, :127-130", "PASS",
    CARRY2 + "index.html:162-171 and project.html:36, :108, :127-130 (the project.html hunks changed since c737272 are at :53, :204, :206, :215, :228, :359, :402, none of the cited lines).")
row("A-H14", "2.8 data status and SIMULATED labels", "index.html:37, :175; footers of index, L01..L04", "PASS",
    f"SIMULATED labels present where samples appear: index footer ('Seeded samples are SIMULATED'), L02.html:507 and L03.html:498 ('the seeded samples are SIMULATED' / 'the seeded sample in Lab 1 is SIMULATED'). L01 and L04 print no sample. The footer scope wording is a separate row (L02-FOOTER-SCOPE, L03-FOOTER-SCOPE). {S}slice_a_checks_r3.out lists the five footers.")
row("A-H15", "2.1 citation: blitzstein2019introduction", "index.html:181-183; L03.html:487; references/references.json:3127-3170", "PASS",
    CARRY2 + "index.html:181-183 and L03.html:487 (unchanged). The page states that no passage was read and attributes nothing to the book; references/ unchanged.")
row("A-H16", "2.6 debate and Atlas status", "index.html:37, :175; curriculum/curriculum.json M4 entry", "PASS",
    CARRY2 + "index.html:37 (unchanged) and the M4 curriculum entry (no debate key, no Atlas milestone; curriculum/ unchanged).")

# ---- L01 (byte-identical since c737272)
for id_, check, loc, ev in [
    ("L01-PROSE", "2.2 numbers and claims in prose", "L01.html:37-51, :55, :69, :95-99, :129-135, :277-281, :287-297, :360-370, :388-398",
     "page and its lab twin byte-identical since c737272 (git diff empty); the L01 cards are unchanged in this round (delta card ids do not include L01 cards)."),
    ("L01-MATH", "2.4 definitions, Prop 2.2, Prop 3.2, Remark 3.3, Prop 3.4, proofs", "L01.html:57-126", "page byte-identical since c737272."),
    ("L01-LAB", "2.5 lab: hypothesis, output, interpretation", "L01.html:138-271; tests/labs/M4/lab-M4-L01-1.py", "re-run in round 3: A-G04 and A-G05 (page code equals twin; expected block equals stdout; {S}L01.out)."),
    ("L01-PROBLEMS", "2.4 problem set worked solutions", "L01.html:302-405", "page byte-identical since c737272."),
    ("L01-QUIZ", "2.9 quiz answers and explanations", "L01.html:424-494", "page byte-identical since c737272."),
    ("L01-GRADES", "2.3 grades", "L01.html:43-48, :80, :103, :113, :119, :413-418", "page byte-identical since c737272."),
    ("L01-FWD-POINTER", "5 terms used before definition (within-lesson forward pointer)", "L01.html:51", "page byte-identical since c737272."),
]:
    evidence = CARRY2 + loc + " (" + ev + ")" if ev.startswith("page") else CARRY2 + loc + ". " + ev
    row(id_, check, loc, "PASS", evidence)

# ---- L02
for id_, check, loc, ev in [
    ("L02-PROSE", "2.2 numbers and claims in prose", "L02.html:51, :55, :84-90, :134-141, :262, :267-272, :281-293, :358-365, :390-398", "page byte-identical since c737272."),
    ("L02-MATH", "2.4 definitions, Props 1.2-1.3, 2.2-2.4, Def 1.6, proofs", "L02.html:57-132", "page byte-identical since c737272. Prop 2.3 and Prop 2.2 hypotheses re-read for the card hypotheses (A-card rows)."),
    ("L02-PROBLEMS", "2.4 problem set worked solutions", "L02.html:298-401", "page byte-identical since c737272."),
    ("L02-FWD-COVARIANCE", "1.10 DAG / terms used before definition", "L02.html:347", "line byte-identical since c737272."),
    ("L02-QUIZ", "2.9 quiz answers and explanations", "L02.html:421-492", "page byte-identical since c737272."),
    ("L02-MISCONCEPTIONS", "2.9 misconceptions: wrong beliefs refuted on the page", "L02.html:279-296", "page byte-identical since c737272."),
    ("L02-CANON", "2.2 cross-lesson claims in 'Where the canon breaks'", "L02.html:267-273 vs L06.html:158, :173 and L10.html:63-65", "page, L06 and L10 byte-identical since c737272."),
    ("L02-GRADES", "2.3 grades", "L02.html:63, :105, :115, :125; key results :409-415", "page byte-identical since c737272."),
]:
    row(id_, check, loc, "PASS", CARRY2 + loc + ". " + ev)

row("L02-LAB", "2.5 lab: hypothesis, output, interpretation", "L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py", "PASS",
    f"Re-run in round 3: A-G04 and A-G05. Own run of the twin: {S}L02.out (fair die E[X] = 7/2, Var = 35/12; loss E[X] = 12500, Var = 2968750000; sample seed 2026 mean 3.469; seed 2027 losses 489 of 10000). Expected block equals stdout ({S}lab_page_vs_twin_r3.out).")
row("L02-FOOTER-SCOPE", "2.2 scope words without a computation (footer 'Every result')", "course/modules/M/M4/L02.html:507", "FAIL",
    f"Footer reads: 'Every result is proved on the page or is an exact computation on a stated list. No real data is used; the seeded samples are SIMULATED.' Lab 1 prints seeded-sample results (L02.html output block: 'die sample, seed 2026 ... mean 3.469'; 'losses 489, total 122250000 cents'; 'sample mean loss 12225.0 cents'), which are neither proved on the page nor exact computations. The word 'Every' is false for them ({S}slice_a_checks_r3.out, footer lines).",
    "Rewrite the footer at L02.html:507, for example: 'Each exact result is proved on the page or is an exact computation on a stated list. The seeded samples in Lab 1 are SIMULATED estimates from one run each. No real data is used.'")

# ---- L03
row("L03-PROSE", "2.2 numbers and claims in prose", "L03.html:51, :113, :138, :142, :258, :265-268, :281, :350, :382",
    "PASS", "Re-verified where the subject changed: L03.html:281 (misconception 'The kurtosis of every law is 3') now gives the Bernoulli law with p = (1 - 1/sqrt(3))/2, pq = 1/6, gamma_4 = 3. Recomputed in " + S + "numbers_r3.out: pq = 1/6 to float precision, gamma_4 = (1-3pq)/(pq) = 3.0000000000000013 by float and exact 3 by formula. Other cited lines are byte-identical since c737272 (L03.html:7 meta and :123, :133 are re-verified under L03-MATH, L03-PROP28-SCOPE).")
row("L03-MATH", "2.4 Props 1.1, 2.2, 2.3, 2.4, Example 2.5, section 3 arithmetic", "L03.html:57-114, :121-134, :138",
    "PASS", "Re-verified where changed (Definition 2.7 at :123, Proposition 2.8 proof at :133). Recomputed in " + S + "numbers_r3.out: E[Z^4] by integration by parts = 3E[Z^2] = 3 (the proof's steps read at L03.html:133 are correct: z phi(z) = -phi'(z), boundary term z^3 phi(z) -> 0, integral of phi = 1 from Assumption 2.6). Example 2.5 closed forms re-derived by hand: m3 = pq(q-p), m4 = pq(1-3pq), gamma_4 = (1-3pq)/(pq) (L03.html:138). Unchanged cited lines are byte-identical since c737272.")
row("L03-PROP28-SCOPE", "2.4 proof needs no hypothesis the statement omits (Proposition graded T)", "L03.html:127-128 (statement), :133 (proof), :123 (Definition 2.7)",
    "PASS", "Re-verified from scratch (round-2 FAIL). The statement now reads 'Assuming Assumption 2.6, a standard normal Z has E[Z] = 0, E[Z^2] = 1 and E[Z^4] = 3' (L03.html:128). The proof's steps need exactly Assumption 2.6: phi integrable, the moments z^k phi(z) integrable for k = 1 to 4, integral of phi = 1, phi' = -z phi, and vanishing boundary terms (L03.html:118, quoted). Definition 2.7 (L03.html:123) states that the finite-space hypothesis of Definition 2.1 is not used, and the proof states the same at :133. The standardization is an identity once E[Z] = 0 and E[Z^2] = 1 are shown. The proof is complete under the stated hypothesis.")
row("L03-NORMAL-KURTOSIS", "2.9 plan conformance: 'Normal kurtosis = 3 is derived, not cited' (plans/M4-build-plan.md:141)", "L03.html:116-134; plans/M4-build-plan.md:141",
    "PASS", "Re-verified (round-2 PASS, subject changed). The derivation is on the page (Proposition 2.8, L03.html:127-133) with no citation; the registry is not used. Blitzstein is not cited for it.")
row("L03-STD-NORMAL-DUP", "1.10 no concept defined twice (BUILDER_RULES 1.10); plan 'undeclared terms defined inline at first use, in the lesson where first used'",
    "L03.html:123 (Definition 2.7) vs course/modules/M/M4/L06.html:65", "FAIL",
    f"The standard normal law is defined twice. L03.html:118 uses the term first (Assumption 2.6) and L03.html:123 defines it (Definition 2.7). L06.html:65 defines it again: 'The standard normal law is \\(N(0,1)\\), with density \\(\\varphi(z) = e^{{-z^{{2}}/2}}/\\sqrt{{2\\pi}}\\). A variable Z with this law is a standard normal variable.' L01 and L02 do not use the term (grep count 0). Confirmed at a007712 by {S}slice_a_checks_r3.out (definition-like sentences at L03.html:123 and L06.html:65). The cards no longer duplicate it: M4-c084 was edited (CARD-M4-c084 change), so only M4-c219 defines it on cards.",
    "Keep one definition. Delete the second definition at L06.html:65 and replace it with a pointer to L03 Definition 2.7 (or delete it), so that the term is defined once. The edit belongs to the owner of L06, which is outside this slice; L03 Definition 2.7 is the first definition and is correct.")
row("L03-LAB", "2.5 lab: hypothesis, output, interpretation", "L03.html:140-259; tests/labs/M4/lab-M4-L03-1.py", "PASS",
    f"Re-run: A-G04 and A-G05. Own run: {S}L03.out (skewed law sample seed 2026 n = 20000: skewness 2.065, kurtosis 5.580; exact 2.0730 and 5.6254; Bernoulli 1/10 squared skewness 64/9 and kurtosis 73/9). Lab section and twin byte-identical since c737272 for everything except the timing of re-run.")
row("L03-CANON-MISC", "2.2 canon breaks and misconceptions", "L03.html:263-288 (changed at :281); L10.html:150-151", "PASS",
    "Re-verified where the subject changed (L03.html:281, the new Bernoulli 1-1/sqrt(3) example, see L03-PROSE). The canon bullet at L03.html:267 is unchanged and states the standard normal exception with Assumption 2.6, consistent with Proposition 2.8. L10.html:150-151 (Student-t with nu = 3, E[V^4] infinite) is byte-identical since c737272.")
row("L03-PROBLEMS", "2.4 problem set worked solutions", "L03.html:290-393", "PASS",
    CARRY2 + "L03.html:290-393 (no changed line).")
row("L03-QUIZ", "2.9 quiz answers and explanations", "L03.html:413-483", "PASS",
    CARRY2 + "L03.html:413-483 (no changed line). The quiz items that mention 'standard normal' (none at this span) are unaffected.")
row("L03-GRADES", "2.3 grades", "L03.html:42-49, :57, :69-82, :89, :99, :109-114, :126, :386-391, :401-407",
    "PASS", "Re-verified where the subject changed. L03.html:406 (key-results table) now reads 'Assuming Assumption 2.6, for a standard normal Z, ... (Proposition 2.8)', graded T, with the derivation on the page: the grade T matches a derivation with its hypothesis stated (BLUEPRINT section 3). Proposition 2.8 (L03.html:126-128) is T and assumes Assumption 2.6. Other grades unchanged since c737272.")
row("L03-FOOTER-SCOPE", "2.2 scope words without a computation (footer 'Every result on this page')", "course/modules/M/M4/L03.html:498", "FAIL",
    f"Footer reads: 'Every result on this page is proved on the page or is an exact computation on a stated table; the normal kurtosis (Proposition 2.8) is proved under Assumption 2.6. No real data is used; the seeded sample in Lab 1 is SIMULATED.' Lab 1 prints a seeded-sample result (L03.html output block: 'skewed law sample, seed 2026, n = 20000: skewness 2.065, kurtosis 5.580'), which is neither proved nor an exact computation on a stated table, so 'Every result' is false for it ({S}slice_a_checks_r3.out footers).",
    "Rewrite the footer at L03.html:498 so the seeded sample is named as its own category, for example: 'Each exact result is proved on the page or is an exact computation on a stated table; the normal kurtosis (Proposition 2.8) is proved under Assumption 2.6. The seeded sample in Lab 1 is a SIMULATED estimate. No real data is used.'")

# ---- L04 (byte-identical since c737272)
for id_, check, loc, ev in [
    ("L04-PROSE", "2.2 numbers and claims in prose", "L04.html:52, :132, :139, :144, :169, :300, :306-308, :318-326", "page byte-identical since c737272."),
    ("L04-MATH", "2.4 Defs 1.1-2.1, Props 1.4-1.8, 2.3-2.4, Remark 2.2, proofs", "L04.html:58-165", "page byte-identical since c737272."),
    ("L04-PROBLEMS", "2.4 problem set worked solutions", "L04.html:331-434", "page byte-identical since c737272."),
    ("L04-QUIZ", "2.9 quiz answers and explanations", "L04.html:453-528", "page byte-identical since c737272."),
    ("L04-CANON-MISC", "2.2 canon breaks and misconceptions", "L04.html:303-329", "page byte-identical since c737272."),
    ("L04-GRADES", "2.3 grades and references", "L04.html:442-447, :530-534", "page byte-identical since c737272."),
]:
    row(id_, check, loc, "PASS", CARRY2 + loc + ". " + ev)
row("L04-LAB", "2.5 lab: hypothesis, output, interpretation", "L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py", "PASS",
    f"Re-run: A-G04 and A-G05. Own run {S}L04.out: exact fractions (table product independent True; dependent table cell (0,0) 1/10 against 4/25; Y = X^2 covariance 0 and cell (0,0) 1/3 against 1/9; E[X|Y=0] = 1, E[X|Y=1] = 2/3, E[X] = 4/5). Expected block equals stdout ({S}lab_page_vs_twin_r3.out).")

# ---- cross-cutting
row("DAG-A", "1.10 / 2.9 DAG reading (slice a)", "index.html; L01..L04.html; check_dag output", "PASS",
    f"Re-run check_dag (A-G02). Read of the delta: index.html:53 and :62 and the L03 hunks add no concept link and define no concept. L03 Definition 2.7 uses 'standard normal' without a link; no lesson of the slice links a later lesson.")
row("NOTATION-A", "2.4 / 2.9 notation vs notation/notation.json", "index.html; L01..L04.html; notation/notation.json", "PASS",
    f"{S}slice_a_checks_r3.out: registry symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}; the delta uses \\gamma_4 (registered as kurtosis, not excess, notation.json) with the meaning of L03 Definition 2.2. The standard normal density symbol \\varphi (25 uses in L03) is not registered and conflicts with no registered symbol. Observation, not a failure: the pages write \\operatorname{{Var}} (62 uses in L02, 7 in L03) where the registry has a \\Var macro; BUILDER_RULES 3.1 restricts custom macros, and the same operator is used across modules, so no row fails on it. Architect may want the macro used.")
row("PROCESS-A", "2.9 process words and banned phrases (BUILDER_RULES 1.3-1.4)", "index.html; L01..L04.html (visible text)", "PASS",
    "Re-run: check_pages (A-G01) reports no banned string. Word search over the five pages (grep -i for round, verif, builder, draft, TODO, TBD, lorem, clearly, obviously) finds only 'rounded' and learner instructions such as 'Verify this by hand' (L01.html:360; L03.html:312, :337), which are learner prompts, not process words.")
row("CARDS-DUP", "2.7 full scan for duplicates", "course/modules/M/M4/cards.json (212 cards)", "PASS",
    f"{S}slice_a_checks_r3.out: total 212, dup ids 0, dup fronts 0 (case-insensitive). The changed cards were compared with their neighbours; M4-c219 ('What is a standard normal random variable?') is the only card that defines the standard normal law, and M4-c220 is a different fact (kurtosis 3).")
row("CARDS-L01", "2.7 cards L01", "cards.json ids M4-c001..c016, c173, c192-c195, c197, c198", "PASS",
    CARRY2 + "those card objects (the delta card ids are c028, c029, c033, c047, c070, c084, c112, c140, c183, none in L01). no delta hunk touches an L01 card object; L01 cards re-read in round 2 (full read).")
row("CARDS-L02", "2.7 cards L02 (changed cards re-verified)", "cards.json ids M4-c017..c033, c181, c182, c199", "PASS",
    f"Changed L02 cards re-verified: M4-c028, M4-c029, M4-c033 (see the four card rows below). The other L02 cards are byte-identical since c737272 (carried from round 2).")
row("CARD-M4-c028", "2.7 card truth and hypotheses (changed hypothesis)", "course/modules/M/M4/cards.json:195 (id M4-c028)", "PASS",
    "Front 'Does scaling X by a multiply its variance by a?'. Back now opens 'Hypothesis: finite probability space with positive weights.' This matches the page context of Lesson 2 (finite probability spaces, L02.html:57-132); Proposition 2.3 (L02.html:115-117) states the rule. Value check: die with a = 2 has Var = 35/3 = 4 x 35/12 (" + S + "numbers_r3.out: 'die ... scale a=2 var 35/3 = 35/3 True twice 35/6'), so 'not twice' is correct.")
row("CARD-M4-c029", "2.7 card truth and hypotheses (changed hypothesis; round-1 FAIL, round-2 PASS)", "course/modules/M/M4/cards.json:202 (id M4-c029)", "PASS",
    "Back now opens 'Hypothesis: finite probability space with positive weights.' Proposition 2.2 (L02.html:105-107) is stated for X on a finite probability space with positive weights, so the hypothesis is the page's. Values: E[X^2] = 91/6, Var = 35/12 (" + S + "numbers_r3.out: die var 35/12; L02.html:136 and Example 2.5).")
row("CARD-M4-c033", "2.7 card numbers appear in the lesson; card truth against lab output (changed front and back)", "course/modules/M/M4/cards.json:230 (id M4-c033); L02.html lab output block",
    "PASS", f"Front: 'In Lab 1's seed-2027 loss sample of 10000 draws, how many draws give a loss of 250000 cents?' Back: '489, against an expected count of 500.' The twin (tests/labs/M4/lab-M4-L02-1.py) draws 250000 with probability 0.05 from random.Random(2027); own run {S}L02.out prints 'losses 489, total 122250000 cents'; 10000 x 1/20 = 500 (" + S + "numbers_r3.out). Number 489 appears in L02.html output. The card is labelled SIMULATED (basis).")
row("CARDS-L03", "2.7 cards L03 (changed cards re-verified)", "cards.json ids M4-c034..c048, c183, c200, c212, c214, c215, c219, c220", "PASS",
    "Changed L03 cards re-verified: M4-c047, M4-c183, M4-c219 (own rows). M4-c200 m3 = 2157/32 and m4 = 149461/256, M4-c042 mean 7/4 and variance 163/16, M4-c043 kurtosis 5/3 from m4 = 15, m2 = 3, M4-c044 gamma_3 = 0 and not symmetric, M4-c045 and c048 Bernoulli values all re-derived with Fractions in " + S + "numbers_r3.out and match. Other L03 cards are byte-identical since c737272.")
row("CARD-M4-c047", "2.7 card truth against lab output (changed front)", "course/modules/M/M4/cards.json:329 (id M4-c047)", "PASS",
    f"Front: 'What sample skewness does the seed-2026 sample of 20000 draws give for the law on 0, 1, 2 and 10 with probabilities 1/2, 1/4, 1/8 and 1/8?' Back: '2.065, against exact skewness 2.073'. Own run {S}L03.out: 'skewed law sample, seed 2026, n = 20000: skewness 2.065'; exact 2.0730 from m3 = 2157/32 and m2 = 163/16 (" + S + "numbers_r3.out). Labelled SIMULATED (basis).")
row("CARD-M4-c183", "2.7 card truth against lab output (changed front)", "course/modules/M/M4/cards.json:1288 (id M4-c183)", "PASS",
    f"Front now names the same law as M4-c047 (0, 1, 2 and 10 with probabilities 1/2, 1/4, 1/8, 1/8). Back '5.580, against exact kurtosis 5.625'. Own run {S}L03.out: 'kurtosis 5.580'; exact 149461/26569 = 5.6254 (" + S + "numbers_r3.out). Labelled SIMULATED.")
row("CARD-M4-c219", "2.7 card duplicate check (round-2 FAIL: restated M4-c084)", "course/modules/M/M4/cards.json:1493-1499 (id M4-c219) vs cards.json id M4-c084 (L06)", "PASS",
    f"Round-2 FAIL resolved at the card level: M4-c084 ('What is the normal distribution N(mu, sigma^2)?') no longer contains the standard normal sentence (cards.json:592 in the delta). {S}slice_a_checks_r3.out lists the only cards mentioning the standard normal: M4-c087..c092, c102, c114..c116, c122, c135, c136, c164, c186, c205, c219, c220, and only c219 defines it. The page-level duplicate in L06.html:65 is still open and is reported as L03-STD-NORMAL-DUP.")
row("CARDS-L04", "2.7 cards L04", "cards.json ids M4-c049..c066, c201, c204", "PASS",
    CARRY2 + "those card objects (no L04 card is in the delta); L04 cards re-read in round 2 (full read).")
row("CARDS-NUMBERS", "2.7 card numbers appear in their lesson", "cards.json (L01-L04 cards)", "PASS",
    "Every number on the changed cards appears in its lesson: 35/3 and 35/12 (L02.html), 91/6 (L02.html), 489 and 500 (L02.html), 3.469 (L02.html), 2.065, 2.073, 5.580, 5.625, 2157/32, 149461/256, 163/16 (L03.html). Checked by grep counts on L02.html and L03.html in this round (grep -c).")
row("CARDS-GRADE-BASIS", "2.7 non-T cards need cite or basis", "cards.json L02/L03 cards with grade C (M4-c030, c033, c047, c183)", "PASS",
    "Each C card has basis 'Lab 1 (SIMULATED), seed ...' naming the lab (basis field in cards.json). No C card has a registry cite; none needs one.")

# ---- mutants and notes-level rows
row("MUTANTS-A", "2.6 mutation testing (project graders only): tools/mutate_graders.py --unit M4 --seeds 0-9 re-run", "ledgers/M4/mutants/ (118 mutants; not slice a)", "PASS",
    f"Re-run at {PIN}: {S}mutate_M4_seeds0-9.out: 'mutate_graders M4: PASS (118/118 killed)', exit 0. Not a slice-a row; re-run because the procedure asks for it.")
row("NUMBERS-A", "2.2 / 2.4 re-derivation of every number on slice a", "index.html; L01..L04.html; cards.json (slice a)", "PASS",
    f"Changed numbers re-derived with Fractions in {S}numbers_r3.py (output {S}numbers_r3.out): skewed law mu 7/4, Var 163/16, m3 2157/32, m4 149461/256, gamma_4 149461/26569; law -2,1,3: mu 0, m2 3, m3 0, m4 15, gamma_4 5/3; Bernoulli 1/10: gamma_4 73/9, gamma_3^2 64/9; Bernoulli 1/4: gamma_4 7/3; Bernoulli (1-1/sqrt3)/2: pq = 1/6, gamma_4 = 3; die: mu 7/2, Var 35/12, Var(2X) = 35/3; loss: mu 12500, Var 2968750000, sd 54486.24 (rounded from 54486.2368). Unchanged numbers are carried by byte identity (round 2 NUMBERS-A full script).")

# ---- fragment
frag = {
    "unit": "M4",
    "slice": "a",
    "round": 3,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyD3-M4-a)",
    "pin": PIN,
    "base": BASE,
    "checkout": str(ROOT),
    "scratch": S,
    "verified_at": "2026-11-02T23:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 3 of slice a (index.html, L01-L04, lab twins, L01-L04 cards). Delta read c737272..a007712 hunk by hunk: index.html 2 lines (:53, :62); L03.html 4 hunks (meta description :7; Definition 2.7 :123; Proposition 2.8 proof :133; misconception :281; key-results row :406); cards.json changed cards c028, c029, c033, c047, c183 in slice a. Outside slice a: project.html, grader/test_project.py, cards c070, c084, c112, c140 (L05, L06, L07, L09), and L05-L10 pages. L01.html, L02.html, L04.html, tests/labs/M4/, references/, notation/, tools/ and curriculum/ are byte-identical.",
        "Round-2 FAIL rows re-verified from scratch: L03-PROP28-SCOPE now PASS (statement names Assumption 2.6, proof and Definition 2.7 state the finite-space hypothesis is not used); CARD-M4-c219 now PASS (M4-c084 no longer restates the standard normal). L03-STD-NORMAL-DUP is still FAIL: L06.html:65 still defines the standard normal law (outside slice a; fix owned by L06).",
        "New FAILs found in round 3 (in slice a): L02-FOOTER-SCOPE and L03-FOOTER-SCOPE. The footers say 'every result' is proved or an exact computation, but Lab 1's seeded sample values are neither. The fix is wording only.",
        "Carry rule: rows whose cited lines are byte-identical since c737272 are carried from round 2 with the prefix 'Carried from round 2'. Rows whose subject changed were re-verified in this round (A-H03, A-H04, A-H05, L03-*, CARD-M4-c028/c029/c033/c047/c183/c219, CARDS-L02, CARDS-L03). The L01, L02 and L04 page bodies and the lab twins were not re-read line by line in round 3; they are carried by byte identity plus the round-2 full read.",
        "Lab twins: run alone under python -I -W error (exit 0, empty stderr); page code equals twin and expected block equals stdout for all four labs (A-G05). Labs are demonstrations, so no mutation applies to them (rulings).",
        "Observation (not a row failure): pages write \\operatorname{Var} where notation.json registers the macro \\Var; BUILDER_RULES 3.1 limits custom macros, so this is not charged. Architect decision requested if the macro should be used.",
        "Observation: the standard normal density symbol \\varphi is not in notation.json (only \\Phi, \\gamma_3, \\gamma_4 and R-symbols are registered). It conflicts with no registered symbol, so not charged; architect may register it.",
        "Could not check: Blitzstein and Hwang's text was not read (no access in this run); no page attributes a locator to it, and the claim 'No passage from it has been read' (L03.html:487) is therefore the only statement needed. No live Crossref call was made (references unchanged; verify_refs --offline run). page_smoke.py ran the four lab twins in Pyodide inside headless Chromium (runtime boot 1.1 to 1.2 s; lab 0.0 s); no run on a physical device. The full pytest suite and test_page_smoke.py / test_figure_kernels.py were not run. run_graders.py was not run (no grader in slice a). No figure exists on these pages (data-chart count 0), so the figure rows do not apply.",
    ],
    "summary": "Slice a round 3 at a007712: 77 PASS, 3 FAIL, 0 UNVERIFIABLE (80 rows). FAILs: L03-STD-NORMAL-DUP (standard normal law defined in L03 Definition 2.7 and again at L06.html:65), L02-FOOTER-SCOPE and L03-FOOTER-SCOPE ('every result' footers include seeded-sample values). Round-2 FAILs L03-PROP28-SCOPE and CARD-M4-c219 are now PASS. All gates passed: check_pages, check_dag, check_projects, run_labs (4 lessons, 4/4), twins alone, page_smoke (slice pages), ruff, mypy strict, five pytest modules, verify_refs --offline, mutate_graders 118/118.",
}
rows_ids = [r["id"] for r in rows]
assert len(rows_ids) == len(set(rows_ids)), "duplicate row ids"
frag["verdict"] = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
out = ROOT / "ledgers/M4/M4-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
print("rows", len(rows), counts, "verdict", frag["verdict"])
