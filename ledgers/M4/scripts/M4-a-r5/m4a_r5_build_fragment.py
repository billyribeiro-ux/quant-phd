"""Builds the round-5 fragment ledgers/M4/M4-a.json for M4 slice a (hub, L01-L04, lab twins, slice cards).

Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-a-r5/build_fragment_r5.py
Every row cites the script, log or file it rests on. Statuses were set by the verifier after the checks listed.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/M4/scripts/M4-a-r5"
G = f"{S}/gates"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---------- gates (repository commands, exit codes in G/exit_codes.txt) ----------
row("A-G01", "2.9 structure: check_pages --unit M4", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    f"`tools/check_pages.py --unit M4` -> 'check_pages M4: PASS', exit 0 ({G}/check_pages.log, exit_codes.txt).")
row("A-G02", "2.9 DAG: check_dag --unit M4", "course/modules/M/M4/index.html, L01.html..L04.html", "PASS",
    f"`tools/check_dag.py --unit M4` -> 'check_dag M4: PASS', exit 0 ({G}/check_dag.log). Links only; the forward "
    "pointer of L03 to Lesson 6 is prose, not a link Concept links point to earlier lessons only; the later-lesson hrefs in L01-L04 are the Next buttons (L04.html:539 href=L05.html, same pattern on the other pages).")
row("A-G03", "2.6 projects gate (unit-wide; outside slice a)", "course/modules/M/M4/project.html", "PASS",
    f"`tools/check_projects.py --unit M4` -> 'check_projects M4: PASS', exit 0 ({G}/check_projects.log).")
row("A-G04", "2.5 labs: run_labs --unit M4", "tests/labs/M4/lab-M4-L01-1.py..lab-M4-L04-1.py", "PASS",
    f"`tools/run_labs.py --unit M4` -> 'run_labs M4: PASS (13/13)', exit 0 ({G}/run_labs.log).")
row("A-G05", "2.5 twins alone under python -I -W error; page code equals twin; expected block equals stdout",
    "tests/labs/M4/lab-M4-L01-1.py..L04-1.py; course/modules/M/M4/L01.html..L04.html", "PASS",
    f"`.venv/bin/python -I {S}/m4a_r5_twins.py` (output {S}/m4a_r5_twins.out): L01 exit 0, 20 stdout lines; L02 exit 0, "
    "10; L03 exit 0, 8; L04 exit 0, 18; stderr 0 bytes each; page code block equals the twin (after HTML unescape) for "
    "all four, including the L04 docstring changed this round; expected block equals stdout line for line; 'twins PASS'. "
    "Interpreter: .venv Python 3.14.8 (`.venv/bin/python --version`).")
row("A-G06", "2.9 page_smoke (slice pages alone, Pyodide and browser)", "index.html, L01.html..L04.html", "PASS",
    f"`tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04` -> 'page_smoke M4: PASS', exit 0; each lab 0.0 s "
    f"({G}/page_smoke_slice.log).")
row("A-G07", "gate: ruff check . (repository)", "repository", "PASS",
    f"`.venv/bin/ruff check .` -> 'All checks passed!', exit 0 ({G}/ruff_check.log).")
row("A-G08", "gate: ruff format --check . (repository)",
    "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py:3; pyproject.toml:18", "FAIL",
    f"`.venv/bin/ruff format --check .` -> '1 file would be reformatted, 473 files already formatted', exit 1 "
    f"({G}/ruff_format_check.log, exit_codes.txt). The file is outside slice a and is unchanged since 4eb6788 "
    "(`git diff --quiet 4eb6788 440ed3c -- ledgers/M3/retired` exits 0). No M4 page fails the format check.",
    "Owner of M3: format ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py (ruff format), or add "
    "\"ledgers/*/retired\" to [tool.ruff] extend-exclude in pyproject.toml, then re-run `.venv/bin/ruff format --check .`. "
    "No change to any M4 slice-a file is needed.")
row("A-G09", "gate: mypy strict (mypy --no-incremental)", "repository (331 source files)", "PASS",
    f"`.venv/bin/mypy --no-incremental` -> 'Success: no issues found in 331 source files', exit 0 ({G}/mypy.log).")
row("A-G10", "gate: relevant pytest", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_docs_figures.py, "
    "test_page_smoke.py, test_curriculum.py", "PASS",
    f"`.venv/bin/pytest -q -p no:cacheprovider` on the six files: all dots, exit 0 ({G}/pytest_relevant.log, exit_codes.txt).")
row("A-G11", "2.1 citations: verify_refs --offline; live plain-curl check of blitzstein2019introduction",
    "references/references.json (blitzstein2019introduction); tools/verify_refs.py", "PASS",
    f"Offline: `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({G}/verify_refs_offline.log). "
    "Registry record (read this round): doi 10.1201/9780429428357, year 2019, isbn [9780429428357], publisher Chapman and "
    "Hall/CRC, no edition field, source string 'Blitzstein & Hwang, Introduction to Probability, 2nd ed. (2019)'. "
    "Live, plain curl, no login or bot check: `curl -s https://api.crossref.org/works/10.1201/9780429428357` -> HTTP 200; "
    "title 'Introduction to Probability'; authors Blitzstein, Hwang; published 2019-02-08; publisher Chapman and Hall/CRC; "
    "edition-number 2; ISBN 9780429428357. Matches the registry.")
row("A-G12", "scope: slice-a delta since previous pin 4eb6788, every hunk read", "course/modules/M/M4/L01.html:111-115; "
    "L02.html:395-397; L03.html:117-124, :262, :276; L04.html:70, :181-184; tests/labs/M4/lab-M4-L04-1.py:10; cards.json", "PASS",
    "`git diff 4eb6788 440ed3c` for slice a (read hunk by hunk): L01 Remark 3.3 proof rewritten (left-continuity, now "
    "fix p and u_n); L02 R3 wording 'half the probability'; L03 Assumption 2.6 now points to Lesson 6 Definition 1.1, "
    "Definition 2.7 removed, Proposition 2.8 statement names the Lesson 6 law, §4 moments bullet adds the Student-t pointer; "
    "L04 Remark 1.3 says three tables, lab description and twin docstring say 'then the cell-by-cell independence verdict'; "
    "cards: new slice-a cards c222-c229 and c233 (read and checked here). index.html, L05-L10, M1, M2 (L23 only), "
    "references/, notation/, tools/ (incl. check_pages.py) and BUILDER/VERIFIER rules are byte-identical or unrelated. "
    "Every changed hunk was re-verified below (rows L01-*, L02-*, L03-*, L04-*, CARDS-*).")

# ---------- hub ----------
HUB = "index.html (byte-identical since 4eb6788; re-read in full this round, text in {S}/text/index.txt)".format(S=S)
row("A-H01", "2.9 structure: hub section order and minimum counts (BUILDER 4)", "course/modules/M/M4/index.html", "PASS",
    f"{HUB}: objectives (6, within 4-8), prerequisites, placement (10 items), lesson map (10 cards), ladder (4 rungs), data status, core reading.")
row("A-H02", "2.9 hours arithmetic", "index.html data-hours-lessons=90, data-hours-project=30; L01..L10 data-hours",
    "PASS", "data-hours-lessons=\"90\" and data-hours-project=\"30\"; the sum of data-hours over L01..L10 html is 90 (grep, "
    "this round); 90 + 30 = 120 = curriculum M4 hours 120; project 30/120 = 25% inside 10-40%.")
row("A-H03", "2.9 objectives: measurable verbs and lesson mapping", "index.html objectives list", "PASS",
    f"{HUB}: six objectives with verbs compute, derive, state, decide, show, compute/apply; each maps to lessons that exist.")
row("A-H04", "2.6 prerequisites vs curriculum", "index.html prerequisites; curriculum.json M4 entry", "PASS",
    f"{HUB}: prerequisites M2 and M1; curriculum.json M4 prereqs ['M2'] (read this round). M2 assumes M1, so the hub's M1 mention is consistent; the hub uses only M1/M2 concepts; M3 is not linked (check_dag PASS).")
row("A-H05", "2.2/1.10 hub claim: matrix facts derived from the quadratic form (Lessons 5 and 8)",
    "index.html prerequisites; L05.html Proposition 2.3; L08.html", "PASS",
    "L05 Definition 2.1 (covariance matrix) and Proposition 2.3 (PSD) read in the L05 text this round; L08 Proposition 1.3 (mean and covariance of a linear image) and Proposition 2.1 (a singular covariance has no inverse) read this round. No M3 link.")
row("A-H06", "2.9 placement diagnostic: items, bar, skill checks", "index.html placement section", "PASS",
    f"{HUB}: ten items; data-mastery 0.8 = 8 of 10; items 1-8 test M1/M2 (quantifier negation, limit 0, integral 1/2, "
    "derivative r e^{rt}, ln e^3 = 3, geometric sum 15/8, discount 1/(1+r), partial derivative 2xy: each re-derived); items 9-10 "
    "are the rung skill checks (answers 1 and 0.6, see A-H08).")
row("A-H07", "3 attribution: placement explanation cites 'M1 Theorem 3.1'", "index.html; course/modules/M/M1/L01.html:79",
    "PASS", "M1 L01.html:79 (read this round) reads 'Theorem 3.1 (negating one quantifier)', and the hub's negation statement matches it.")
row("A-H08", "2.2 numbers in placement answers and explanations", "index.html placement answers",
    "PASS", f"Re-derived with {S}/m4a_r5_numbers.py: 15/8 = 1.875; 1/(1+r); rung-1 quantile F(0)=1/4 < 1/2 <= 3/4 = F(1) gives 1; "
    "rung-2 Var of Student-t(5) = 5/3 and s^2 = 3/5 = 0.6; all printed digits agree.")
row("A-H09", "2.2/2.4 rung-2 skill-check hypothesis and its sources", "index.html rung-2 check vs L06 Proposition 2.6 and L02 Proposition 2.3",
    "PASS", "L06 Proposition 2.6 (text read this round): 'Assuming Assumption 1 ... if nu > 2, Var(t) = nu/(nu-2)', giving 5/3 at nu = 5. "
    "L02 Proposition 2.3 (Var(aX+b) = a^2 Var X) is stated for X on a finite probability space with positive weights (L02 §1-§2 "
    "standing assumption, L02 text line 22). The hub states the scale rule for Student-t as a hypothesis, which is accurate.")
row("A-H10", "2.7/2.9 hub lesson cards agree with the lessons", "index.html lesson map vs L01-L04 (this round) and L05-L10",
    "PASS", "L01-L04 lesson-map descriptions read against the lessons this round (see L01-*..L04-* rows). L08 Proposition 2.1 and L09 "
    "(L09.html:151, the distribution-function limit 'not established on this page') read this round. The L10 Cauchy and Student-t(3) "
    "lab entry is carried from round 4: L05.html through L10.html are byte-identical since the previous pin "
    "(`git diff --quiet 4eb6788 440ed3c -- course/modules/M/M4/L05.html ... L10.html` exits 0).")
row("A-H11", "2.6 ladder: four rungs in order; names agree with project.html", "index.html ladder vs project.html:44-47",
    "PASS", "Rung titles Worked example, Completion problem, Independent project, Stretch, in order. project.html:44-47 (read this round) and index.html:166-169 carry the same four titles in the same order; project.html:46 names tail_risk.py.")
row("A-H12", "2.8 data status and SIMULATED labels", "index.html data status and footer",
    "PASS", "No data: index.html says no real data and that labs compute from formulas and seeds. grep this round: data-files count 0 and "
    "data-chart count 0 on every slice-a page; no external src/href (see DATA-A).")
row("A-H13", "2.1 reading list and citation: blitzstein2019introduction", "index.html core reading; references/references.json",
    "PASS", "Hub says the edition is taken from the curriculum and not checked against the book, which is accurate. The live Crossref "
    "record reports edition-number 2, consistent with the curriculum's '2nd ed.' (A-G11). Registry flag only (see registry_flags).")
row("A-H14", "2.6 curriculum facts for the hub: no debate, no Atlas milestone, part and tier", "index.html; curriculum.json M4",
    "PASS", "curriculum.json M4 entry (read this round): id M4, part M, tier F, title Probability, hours 120, prereqs ['M2'], lab and project entries, no debate and no atlas key.")
row("A-H15", "2.9 hub footer", "index.html footer", "PASS",
    "'Seeded samples are SIMULATED; no real data is used.' Accurate for the hub, which contains no sample.")

# ---------- L01 ----------
row("L01-PROSE", "2.2 numbers and claims in prose", "L01.html:37-51, :55-69, :95-99, :114-135, :277-297, :360-370", "PASS",
    f"Re-derived with Fraction in {S}/m4a_r5_numbers.py (L01 checks): F values 1/10, 3/10, 3/5, 4/5, 9/10, 1; Q(1/2)=0, Q(3/5)=0, "
    "Q(61/100)=1; Example 3.5 pn = 198 and 148.5 -> ceil 149; 74/75 = 0.987 < 0.99; P(X<=1) = 5/6 = 0.833; M2 F(5) = 7/10; M3 "
    "40 p = 36 and 36.04 -> 36, 37; R1 strict rule at 3/5 gives 1; quiz Q(1/2) = 1 for (1/4,1/2,1/4); E1 F(2) = 9/10. All OK.")
row("L01-MATH", "2.4 definitions, Prop 2.2, Def 3.1, Prop 3.2, Remark 3.3, Prop 3.4, proofs", "L01.html:57-126", "PASS",
    "Every proof read this round. Remark 3.3 (rewritten this round): for u_n up to p with F_{k-1} < p <= F_k, eventually "
    "u_n in (F_{k-1}, p] subset of (F_{k-1}, F_k], so Q(u_n) = x_k = Q(p); the choice of k covers every p in (0,1] since "
    "F_0 = 0 < p <= F_m = 1. Prop 3.2 and Prop 3.4 hypotheses stated (positive weights, distinct values); index ceil(pn) in [1,n].")
row("L01-LAB", "2.5 lab: hypothesis, output, interpretation", "L01.html:138-270; tests/labs/M4/lab-M4-L01-1.py", "PASS",
    f"Twin output equals the 20-line expected block ({S}/m4a_r5_twins.out). Q values at the ten probes and 'scan equals "
    "definition at 100 of 100', 'F(Q(p)) >= p at 100 of 100', 'Q(F(x)) = x ... True' and the eps lines re-derived "
    f"({S}/m4a_r5_numbers.py). The interpretation claims only the grid check, and says the proof covers every p.")
row("L01-PROBLEMS", "2.4 problem set: 12 worked solutions", "L01.html:302-405", "PASS",
    "All twelve re-derived (M1 F and Q(1/2)=0; M2 F(5)=7/10, Q(7/10)=5, Q(71/100)=7; M3 indices 36 and 37; P1-P3; E1 Q(99/100)=3; "
    "E2 Q(3/5+eps)=1; E3 counting; R1 strict rule; R2; R3). Solutions are inside details.solution (12 per lesson).")
row("L01-QUIZ", "2.9 retrieval quiz: 9 items, answers and explanations", "L01.html:424-494", "PASS",
    "Nine items; each answer recomputed (Q(1/2)=1; Q(61/100)=1; discontinuity item (Prop 2.2(d)); 198; 149; Q(F_k)=x_k; "
    "5/6 = 0.833; the random variable is a function; Q(1)=x_m). Each explanation cites its result.")
row("L01-GRADES", "2.3 grades on theorems and key-results rows", "L01.html:43-48, :80, :103, :114, :119, :413-418", "PASS",
    "Proposition 2.2, Proposition 3.2, Remark 3.3, Proposition 3.4 are graded T with proofs on the page; key-results rows cite proof "
    "sections or exact arithmetic on a stated table.")
row("L01-FWD", "5 terms used before definition", "L01.html:37, :51", "PASS",
    "'infimum' is first used in §3, where it is defined (the header at :12 says so); 'quantile' at :51 "
    "carries 'defined in Definition 3.1 below'.")

# ---------- L02 ----------
row("L02-PROSE", "2.2 numbers and claims in prose", "L02.html:51, :55, :89, :134-141, :262, :267-273, :281-293, :358-372", "PASS",
    f"Re-derived ({S}/m4a_r5_numbers.py, L02 checks): 35/12, sqrt(35/12) = 1.708; E[L] = 12500; E[L^2] = 3125000000; "
    "Var(L) = 2968750000; sd 54486.24 (54486.2368); R2 Var(D) = 296875, sd 544.8624; canon E[X] = 3/10; misconceptions 15.17 and "
    "2.92; M1 21/100; M2 225000000 and 15000; E1/E2 counts 500 vs 489 (difference 11). All OK.")
row("L02-MATH", "2.4 definitions, Props 1.2-1.3, 2.2-2.4, Def 1.6 and proofs", "L02.html:57-132", "PASS",
    "Every proof read. Prop 2.2 applies Prop 1.3 with U = X^2, V = X, alpha = 1, beta = -2 mu, delta = mu^2 (checked). Prop 2.3 "
    "and Prop 2.4 are stated for the §2 standing assumption (finite, positive weights, L02.html:55). Def 1.6 is stated as unused "
    "by any result, and no result uses it.")
row("L02-LAB", "2.5 lab: hypothesis, output, interpretation", "L02.html:144-263; tests/labs/M4/lab-M4-L02-1.py", "PASS",
    f"Twin output equals the 10-line expected block ({S}/m4a_r5_twins.out). Seeded values reproduced by an independent script "
    f"({S}/m4a_r5_seeded.py -> m4a_r5_seeded.out): die seed 2026 mean 3.469, variance 2.902, minus 3.5 = -0.031; loss seed 2027 "
    "489 losses, total 122250000, mean 12225.0, variance 2906799375.0. The three True lines are the shortcut for the die and loss "
    "and the scale rule for the die. Values labelled SIMULATED, one run each.")
row("L02-PROBLEMS", "2.4 problem set: 12 worked solutions", "L02.html:298-401", "PASS",
    "All twelve re-derived, including the changed R3: for the table of L01 Example 3.6, expectation 3/10 (sum of six products), "
    "Q(1/2)=0 with F(0)=3/5 >= 1/2 and F(-1)=3/10 < 1/2; 'half the probability is at or below this value' describes the quantile. "
    "M1 21/100; M2 5000, 2.25e8, 15000; M3 36 and 4; P1-P3; E1-E3; R1 divisor-n identity; R2 296875 and 544.86; R3.")
row("L02-QUIZ", "2.9 retrieval quiz: 10 items", "L02.html:421-492", "PASS",
    "Ten items; answers 3.5, 1, 12, E[(X - EX)^2], 5000, 225000000, 21/100, c = E[X], 15000, 5 recomputed with the cited propositions.")
row("L02-MISC", "2.9 misconceptions (4 wrong beliefs refuted on the page)", "L02.html:279-296", "PASS",
    "Expectation is a value (3.5 is not a face); scaling by a (variance x 4, not x 2); variance is E[X^2] (agree only when E[X] = 0, "
    "example ±1 with prob 1/2 gives 1 and 1); a seeded sample mean (3.469) is one run, not the expectation. Each computed.")
row("L02-CANON", "2.2/2.9 'where the canon breaks' claims", "L02.html:267-273 vs L06.html Proposition 2.6 and L10", "PASS",
    "L06 Proposition 2.6 (read this round, under Assumption 1): nu <= 2 gives E[t^2] = infinity, so 'no finite variance' is "
    "stated with its hypothesis; L10 treats heavy tails. The mean-versus-quantile point (3/10 vs 0) re-derived.")
row("L02-FWD-COVARIANCE", "5 forward reference: covariance shortcut (L02 Problem P3)", "L02.html:347 vs L04.html Proposition 1.7; L05.html Proposition 1.1",
    "PASS", "L04 Definition 1.6 and Proposition 1.7 (shortcut, read this round); L05 Proposition 1.1 bilinearity read this round. The pointer is prose.")
row("L02-FOOTER-SCOPE", "2.9 footer and references scope words", "L02.html:496 (References), :507 (footer)", "PASS",
    "'Each exact result on this page is proved on the page or is an exact computation on a stated list of values. The seeded samples "
    "in Lab 1 are SIMULATED single-run estimates and are not proofs.' Accurate for L02 (every computation is finite).")

# ---------- L03 ----------
row("L03-PROSE", "2.2 numbers and claims in prose", "L03.html:51, :55, :113, :138, :258, :263-268, :281, :382", "PASS",
    f"Re-derived ({S}/m4a_r5_numbers.py, L03 checks): mu = 7/4; m2 = 163/16; m3 = 2157/32 (terms -1372, -54, +1, +35937 over 512; "
    "the value-10 term exceeds m3 by 1425/512); m4 = 149461/256; gamma3^2 = 18610596/4330747; gamma3 = 2.0730 (2.072997); "
    "gamma4 = 149461/26569 = 5.6254 (5.62539); Bernoulli p = 1/10: gamma3 = 8/3, gamma3^2 = 64/9, gamma4 = 73/9 = 8.11; p = 1/4: "
    "gamma4 = 7/3; sigma = sqrt3/4; gamma3 = 2/sqrt3 = 1.155. Sample gaps 2.073-2.065 = 0.008 and 5.625-5.580 = 0.045 (rounding "
    "error <= 0.001 each). All OK.")
row("L03-MATH", "2.4 definitions, Props 1.1, 2.2-2.4, Example 2.5, Assumption 2.6, Prop 2.8 and proofs", "L03.html:57-134", "PASS",
    "Every proof read. Prop 2.3: sigma_Y = |a| sigma_X, Z_Y = sign(a) Z_X. Prop 2.4 (equality case): W = Z^2 constant forces Z = ±1, "
    "E[Z] = 0 forces 1/2; converse computed. Example 2.5: m3 = pq(q-p), m4 = pq(1-3pq) re-derived with q^3+p^3 = 1-3pq. "
    "Prop 2.8: integration by parts with u = z and u = z^3, v = -phi, boundary terms zero, E[Z^2] = 1 and E[Z^4] = 3 (re-derived). "
    "Prop 2.8 applies gamma_4 to a non-finite law; the proof says so and §4 names the exception, so the extension is stated.")
row("L03-PROP28-SCOPE", "2.4 Prop 2.8 hypotheses (named Assumption 2.6); no unstated assumption", "L03.html:117-118, :122-128",
    "PASS", "Statement names Assumption 2.6 and the Lesson 6 standard normal law. Proof uses phi even (E[Z]), phi' = -z phi and "
    "z^k phi -> 0 (integration by parts), and integrals finite for k <= 4 (Assumption 2.6). Nothing else is assumed. Definition "
    "2.7 (the old restatement) is removed; the numbering defect is L03-NUMBERING.")
row("L03-STD-NORMAL-DUP", "1.10 concept defined twice and used before its owner lesson: standard normal law",
    "L03.html:117-128 vs L06.html Definition 1.1 (text line 25-26)", "PASS",
    "Defined once now: L06 Definition 1.1 gives N(0,1) with density e^{-z^2/2}/sqrt(2 pi) and names a standard normal variable "
    "(read this round). L03 has no definition: Assumption 2.6 says 'defined in Lesson 6, Definition 1.1; its formula is not restated "
    "here'. The round-4 fix option 'keep Proposition 2.8 in L03 with the law stated as the Lesson 6 law' is what was done, so the "
    "duplication row passes. Residual, recorded in notes: L03 still uses the law by name before L06 (plain-text pointer, no hyperlink; "
    "open item 1 of plans/M4-open-items.md says L03 cannot derive it without an undefined concept). Architect to rule.")
row("L03-NUMBERING", "2.9 structure: consecutive numbering of theorem-like blocks", "L03.html:117-122 (Assumption 2.6 then Proposition 2.8)",
    "FAIL", "Blocks in §2 are numbered 2.1, 2.2, 2.3, 2.4, Example 2.5, Assumption 2.6, Proposition 2.8: no 2.7 exists on the page "
    "(removed Definition 2.7 left a gap). Every other lesson in slice a numbers consecutively (L01 1.1-3.4; L02 1.1-2.6; L04 1.1-2.5).",
    "Renumber 'Proposition 2.8' to 'Proposition 2.7' at L03.html:122, :262, :276, :401, :482, :493 and in cards.json card M4-c220 "
    "back ('Proposition 2.8' -> 'Proposition 2.7'); then re-run check_pages --unit M4 and page_smoke for L03.")
row("L03-LAB", "2.5 lab: hypothesis, output, interpretation", "L03.html:140-259; tests/labs/M4/lab-M4-L03-1.py", "PASS",
    f"Twin output equals the 8-line expected block ({S}/m4a_r5_twins.out). Seeded sample reproduced independently "
    f"({S}/m4a_r5_seeded.out): skewness 2.065, kurtosis 5.580. Exact 2.073 and 5.625 (independent float: 2.072997, 5.625390). "
    "Gaps 0.008 and 0.045 stated as computed from the printed three-decimal values; the page says the lab prints exact values on the line after the sample (true).")
row("L03-CANON", "2.2/2.9 canon breaks: -2,1,3 law; Student-t(3) kurtosis", "L03.html:153-156 vs L10.html:66 and :64",
    "PASS", "Law -2, 1, 3 with 2/5, 1/2, 1/10: mean 0, m2 = 3, m3 = 0, m4 = 15, gamma4 = 5/3, not symmetric (re-derived). L10 "
    "Proposition 2.3 (text line 66), under its Assumption 1 (density of V with nu = 3): E[V^4] = infinity; the page says the kurtosis is then undefined. Matches.")
row("L03-MISC", "2.9 misconceptions (refuted on the page)", "L03.html:159-164", "PASS",
    "Symmetry refuted by the §4 law; 'every law has kurtosis 3' refuted by 73/9 and 7/3; 3 is not special: p = (1 - 1/sqrt3)/2 gives "
    "pq = 1/6 and gamma4 = 3 (re-derived with fractions and floats); sign reversal refuted by Prop 2.3 (kurtosis unchanged).")
row("L03-PROBLEMS", "2.4 problem set: 12 worked solutions", "L03.html:167-260", "PASS",
    "M1 sigma = sqrt3/4, gamma3 = 2/sqrt3, gamma4 = 7/3; M2 mu = 1, gamma3 = 0, gamma4 = 1; M3 m3 = 2157/32, gamma3 > 0; "
    "P1 affine invariance; P2 E[Z^2] = 1; P3 q^3 + p^3 = 1 - 3pq; E1 gaps 0.008 and 0.045; E2 64/9 and 73/9; E3 weights total 8; "
    "R1 equality case mu ± sigma; R2 73/9 about 8.11, no tail statement; R3 symmetric about mean gives zero third moment. All re-derived.")
row("L03-QUIZ", "2.9 retrieval quiz: 9 items", "L03.html:413-483", "PASS",
    "Nine items; answers m1 = 0; E[Z^3]; kurtosis 1 at the symmetric law; sign change; unchanged under Y = 5X+3; 5/3 (1.6667); "
    "§4 law statement; 8/3 (2.6667); zero for symmetric law. Each recomputed.")
row("L03-GRADES", "2.3 grades on theorems and assumptions", "L03.html:42-49, :57-134, :401-407", "PASS",
    "Theorems carry T in their titles; Proposition 2.8 is graded T and names Assumption 2.6 in its statement (and in its key-results "
    "row). Assumption 2.6 is an unproved, named assumption, so the T grade is conditional by statement.")
row("L03-FOOTER-SCOPE", "2.9 references and footer scope words", "L03.html:487 (References), :498 (footer)", "PASS",
    "'Each exact result on this page is proved on the page or is an exact computation on a stated table; the normal kurtosis "
    "(Proposition 2.8) is proved under Assumption 2.6'; sample described as a SIMULATED single-run estimate. Accurate.")

# ---------- L04 ----------
row("L04-PROSE", "2.2 numbers and claims in prose", "L04.html:52, :130-133, :169, :300, :306-308, :318-326, :402-405", "PASS",
    f"Re-derived ({S}/m4a_r5_numbers.py, L04 checks): Example 1.9 E[Y] = 2/3, E[XY] = 0, Cov = 0, p(0,0) = 1/3 vs 1/9; Example 2.5 "
    "P(Y=0) = 2/5, P(Y=1) = 3/5, E[X] = 4/5, E[X|Y=0] = 1, E[X|Y=1] = 2/3, total 4/5; M1 0.12 vs 0.1; M2 2/3; E3 (1/10)/(4/25) = 5/8; "
    "canon 1/2 vs 1/4; canon E[XY] = 1 vs 0; quiz P(Y=1) = 3/5; product-table cell 3/50 = 0.06. All OK.")
row("L04-TERM-ORDER", "5 terms used before definition", "L04.html:52 vs :59", "PASS",
    "'the table of their joint probabilities (Definition 1.1 below)' carries an explicit forward pointer; the joint table is defined at :59 (Definition 1.1).")
row("L04-REMARK-1-3", "2.2 and 2.9: lab sentence vs the code and output", "L04.html:70 (Remark 1.3) vs tests/labs/M4/lab-M4-L04-1.py:72-91 (Parts A, B, C in main) and the printed output",
    "PASS", "Remark 1.3 now reads 'applies the test to every cell of three tables (Parts A and B) and prints the verdict for each'. "
    "The code applies is_independent to the product table and the dependent table (Part A) and to the uniform table (Part B): three "
    "tables. Printed lines: 'table product independent True', 'table dependent independent False', 'independent False'. Matches.")
row("L04-MATH", "2.4 definitions, Props 1.4-1.8, 2.3-2.4, Def 1.6, Def 2.1, Remark 2.2 and proofs", "L04.html:58-165", "PASS",
    "Every proof read. Prop 1.4 (P(A and B) = 0 against P(A)P(B) > 0). Prop 1.5 factorization over cells. Prop 1.7 expansion and "
    "linearity. Prop 1.8. Prop 2.3 sums over y with P(Y=y) > 0 (zero-probability values contribute p(x,y) = 0). Prop 2.4.")
row("L04-LAB", "2.5 lab: hypothesis, output, interpretation", "L04.html:172-301; tests/labs/M4/lab-M4-L04-1.py", "PASS",
    f"Twin output equals the 18-line expected block ({S}/m4a_r5_twins.out). Lab description (Part B 'then the cell-by-cell independence "
    "verdict') and the twin docstring match the code. Product cell 3/50 on both sides; dependent cell 1/10 vs 4/25; Example 1.9 "
    "covariance 0 with cell 1/3 vs 1/9; Part C 1, 2/3, total 4/5, product-table check True. 'The lab checks three exact tables' matches.")
row("L04-PROBLEMS", "2.4 problem set: 12 worked solutions", "L04.html:194-300", "PASS",
    "M1 0.12 vs 0.1; M2 2/3; M3 cells 1/8, 1/8, 3/8, 3/8 and E[XY] = 1/8 by two methods; P1; P2; P3 Cov = -ab; E1 total 4/5; "
    "E2 ratio 3; E3 ratio 5/8; R1 Cov 0 and dependence; R2 Cov(X,X) = Var X; R3 equal conditional expectations 0 with dependence.")
row("L04-QUIZ", "2.9 retrieval quiz: 10 items", "L04.html:453-528", "PASS",
    "Ten items recomputed (not independent: 1/3 vs 1/9; E[X|Y=0] = 1; E[XY] = E[X]E[Y]; E[X] = 4/5; events dependent; Cov = 0; "
    "total-expectation sum; P(Y=1) = 3/5; equal conditional expectations do not imply independence; product-table cell 3/50).")
row("L04-CANON-MISC", "2.9 misconceptions and canon", "L04.html:181-190", "PASS",
    "Zero covariance is not independence (Example 1.9); marginals do not fix the joint table (1/2 vs 1/4); the product rule for means "
    "fails under dependence (E[XY] = 1 vs 0 for Y = X); the conditional-expectation misconception is refuted by Example 2.5.")
row("L04-FOOTER", "2.9 footer and references scope words", "L04.html:302 (References), :306 (footer)", "PASS",
    "No seeded sample in L04; every printed lab value is an exact computation on a stated table. 'Every result on this page is derived "
    "on the page (grade T)' holds for the results stated on the page.")

# ---------- cards ----------
row("CARDS-DUP", "2.7 full scan for duplicates (deck of 225 cards)", "course/modules/M/M4/cards.json", "PASS",
    f"`.venv/bin/python -I {S}/m4a_r5_cards.py` ({S}/m4a_r5_cards.out): 225 cards; 0 duplicate ids; 0 duplicate normalised fronts; "
    "0 duplicate backs. Near-duplicate fronts (word Jaccard >= 0.6, 83 pairs in the deck, computed this round) each ask a different "
    "fact: for example c034/c222 (moment vs central moment), c042/c227 (mean vs variance of the same law), c047/c183 (sample skewness vs "
    "kurtosis), c200/c228 (m3 vs m4), c201/c233 (P(X=x) vs P(Y=y), identical wording up to the variable names: different sums, kept).")
row("CARDS-L01", "2.7 retrieval cards: slice-a L01 cards read against the lesson", "cards.json: M4-c001..c016, c173, c192..c195, c197, c198", "PASS",
    "All 23 read against L01.html (text this round). Grades T with hypotheses where needed (c005, c006, c008, c009, c013). Checked: "
    "c011 (198), c015 (149), c012 (0), c014 (Q(3/5)=0), c192 (Q(p)=1 exactly for p in (3/5, 4/5]), c198 (left-continuity, Remark 3.3, "
    "with p_n for the sequence; the lesson uses u_n: same content).")
row("CARDS-L02", "2.7 retrieval cards: slice-a L02 cards read against the lesson", "cards.json: M4-c017..c033, c181, c182, c199", "PASS",
    "All 20 read. c030 and c033 are grade C with basis 'Lab 1 (SIMULATED), seed 2026/2027' and reproduce the seeded lines (3.469; 489). "
    "c031 (54486.24), c181 (sqrt(35/12) about 1.708), c182 (2968750000), c199 (35/12 with hypothesis) correct. c029 states its hypothesis.")
row("CARDS-L03", "2.7 retrieval cards: slice-a L03 cards read against the lesson", "cards.json: M4-c034..c048, c183, c200, c212, c214, c215, c219, c220, c222..c229", "PASS",
    "All 30 slice-a L03 cards read this round. Numbers re-derived (c042 7/4, c043 5/3, c045 73/9 and 7/3, c048 64/9, c200 2157/32, "
    "c227 163/16, c228 149461/256, c047/c183 seeded lines). New cards c222-c229 match Section 1-3 (central moments, kurtosis formulas, "
    "Var(Z) = 1 as stated in Definition 2.1 and Proposition 2.2). c219 is judged in its own row (CARD-M4-c219). c220 is correct "
    "except for the numbering in L03-NUMBERING, which its back will need once that is renamed.")
row("CARDS-L04", "2.7 retrieval cards: slice-a L04 cards read against the lesson", "cards.json: M4-c049..c066, c201, c204, c233", "PASS",
    "All 21 read. c062 (E[X|Y=0] = 1), c064 (-ab), c065 (2/3 and 4/5), c066 (Cov(X,X) = Var X), c204 (equal conditional expectations, "
    "dependent pair), c233 (P(Y=y) = sum over x) are correct. c063 refers to 'Section 3', which is L04's canon-breaks section.")
row("CARDS-NUMBERS", "2.7 every card number appears in its lesson text", "cards.json (94 slice-a cards) vs L01..L04.html",
    "PASS", f"`{S}/m4a_r5_cards.py` ({S}/m4a_r5_cards.out): 94 slice-a cards; number tokens missing from their lesson text: 0.")
row("CARD-M4-c219", "2.7 card atomic, graded, and inside BUILDER 7 card kinds",
    "course/modules/M/M4/cards.json, card M4-c219 (lesson L03)", "FAIL",
    f"The card restates Assumption 2.6 (its back matches L03.html:117-118). It has no 'grade' and no 'basis' field, while every other "
    f"slice-a card carries a grade ({S}/m4a_r5_cards.out: 'slice-a cards without a grade field: ['M4-c219']'). BUILDER 7 requires each "
    "card to carry its grade and lists the kinds that get cards (definition, theorem statement, key formula, key empirical result, "
    "misconception); an assumption is none of them. The round-4 row passed this card without checking the grade field.",
    "Either delete card M4-c219 (Assumption 2.6 is already stated on the page), or add \"grade\" and \"basis\" to it, using the grade "
    "the Architect assigns to an assumed-without-proof fact. If L03-NUMBERING is fixed, the card's back is unchanged.")

# ---------- notation, DAG, process, scope, data, structure, numbers ----------
row("NOTATION-A", "2.4 and 2.9 (rule 13): every symbol vs notation/notation.json",
    "L03.html:117-133 (φ, 25 uses), L07.html:52, :129 (φ_X), L09 (φ_{Z_n}(t), read this round); notation/notation.json (unchanged since 4eb6788)", "FAIL",
    "Macros used on slice-a pages: \\R (L01, registered), \\operatorname (standard, same meaning as the registered \\Var/\\Cov "
    f"expansions), \\gamma_3 and \\gamma_4 (registered M4 meanings, consistent with Definition 2.2), \\varphi (L03: the standard "
    "normal density). \\varphi is not registered in notation/notation.json (`git diff --quiet 4eb6788 440ed3c -- notation` exits 0), and "
    "L07 uses the same glyph for the characteristic function phi_X (L07.html:52 and :129), so M4 uses one symbol for two meanings. "
    "The indicator written as 1_A (L04.html:378) is the registered object without the \\indic macro; same meaning, not a conflict.",
    "Architect: register \\varphi for the standard normal density in notation/notation.json (NOTATION_REQUESTS), and in L07 rename the "
    "characteristic function (phi_X in L07, phi_{Z_n} in L09) to a symbol no other M4 page uses (for example psi_X), so \\varphi carries one meaning across "
    "L03, L06, L07 and L09. Slice-a pages need no edit beyond the notation request and the L03 numbering fix.")
row("DAG-A", "2.9 DAG: check_dag and independent reading of use-before-definition",
    "index.html; L01.html..L04.html", "PASS",
    "check_dag --unit M4 PASS (A-G02). Links in slice a go to M1/M2 concepts or to earlier M4 lessons (L02 -> L01; L03 -> L01, L02; "
    "L04 -> L01, L02). The standard-normal use in L03 is a text pointer to L06 Definition 1.1 (see L03-STD-NORMAL-DUP), not a link.")
row("PROCESS-A", "2.9 / rule 12: banned phrases and process words in learner text", "index.html; L01..L04 text dumps", "PASS",
    f"Text scan ({S}/text/*.txt, script regexes this round): no TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'left as an exercise', "
    "'it is important', 'clearly', 'obviously', 'well known', 'studies show', 'experts agree', 'you can add', ellipsis placeholders; no "
    "'builder', 'verifier', 'round N', 'draft', 'revised', 'fixed' used as process words. 'Predicted/Stated before running' is the labs' "
    "stated-expectation convention, not a build process; noted in notes.")
row("SCOPE-A", "2.9 / rule 4: scope words (only, all, always, every, any, same, exactly)", "index.html; L01..L04 text",
    "PASS", "Scope words read in context across the five pages (text scan this round: 'every' index 4, L01 22, L02 7, L03 9, L04 17; 'only' 1, 9, 6, 13, 8; 'exactly' 1, 7, 9, 12, 4). Each occurrence is "
    "backed by a stated hypothesis or a computation. 'Every outcome has positive probability' is the positive-weight hypothesis; 'the "
    "only law on this page that is not finite' (L03) is the standard normal; 'Every computation in this lesson uses a finite law' (L02) "
    "is true for all L02 computations; 'Every kurtosis ... is E[Z^4]' (L03) is the definition.")
row("DATA-A", "2.8 data: no data files, no figures, no external requests", "index.html, L01..L04.html", "PASS",
    "grep this round: data-files = 0, svg = 0, external src/href = 0 on all five pages; the seeded samples (L02 seeds 2026, 2027; L03 seed "
    "2026) are labelled SIMULATED in the hypothesis and interpretation; L01 and L04 use exact tables only and say so.")
row("STRUCT-A", "2.9 structure: template order, minimum counts, hours, why-it-matters length", "L01..L04.html", "PASS",
    "Order in each lesson: why-it-matters, numbered core sections, inline labs, canon-breaks, misconceptions, problem set, key-results "
    "table, retrieval quiz, references. why-it-matters word counts 114, 97, 97, 101 (limit 120). Misconceptions 3, 4, 3, 3 (min 3). "
    "Problem set: 12 solutions per lesson (3 in each of Mechanics, Proof, Empirical, Research). Quiz items 9, 10, 9, 10 (8-15). "
    "data-hours 9 each. Hub split 90/30 and the hours sum 90 over L01-L10 (A-H02). NUMBERING: L03 has a gap (L03-NUMBERING).")
row("NUM-A", "2.2 numbers, independent re-derivation (all slice-a numbers)", f"{S}/m4a_r5_numbers.py", "PASS",
    f"`.venv/bin/python -I {S}/m4a_r5_numbers.py` -> 93 checks, 93 OK, 'FAILS: none' ({S}/m4a_r5_numbers.out). Covers the hub placement "
    "numbers, all L01-L04 examples, problems, quizzes, the L03 sample gaps, and the L04 tables. Seeded samples re-derived in "
    f"{S}/m4a_r5_seeded.py.")

# ---------- fragment ----------
frag = {
    "unit": "M4",
    "slice": "a",
    "round": 5,
    "verifier": "Claude Haiku 5.5 independent verifier (verifyD5-M4-a)",
    "pin": "440ed3c8216725d498d9c6d7c746907d4d418198",
    "base": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-M4-a",
    "scratch": f"{S}/",
    "verified_at": "2026-11-03T20:30:15+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "notation/notation.json does not register \\varphi (standard normal density, used in L03 and L06) and the same glyph is "
        "the characteristic function phi_X in L07 (L07.html:52, :129). Registry owner to register \\varphi for the density; L07 needs "
        "another symbol for the characteristic function. NOTATION-A.",
        "curriculum.json concept 'correlation' is labelled 'Covariance and correlation' (M4 introduces). L04 Definition 1.6 gives the "
        "covariance formula (no dfn element), L05 defines correlation (dfn correlation). plans/M4-build-plan.md open item 9 has no "
        "ruling in plans/FINAL-ARCHITECT-RULINGS.md. Architect to confirm L04 owns the covariance formula.",
        "references/references.json blitzstein2019introduction has no edition field, while the live Crossref record (plain curl, "
        "this round) reports edition-number 2 and the registry source string says '2nd ed. (2019)'. Registry owner may record the "
        "edition from Crossref. The hub states its edition is unchecked against the book, which is accurate.",
    ],
    "freshness_flags": [],
    "notes": (
        "Round 5 at 440ed3c (delta from 4eb6788 for slice a: L01 Remark 3.3 proof; L02 R3 wording; L03 Assumption 2.6, Definition 2.7 "
        "removed, Proposition 2.8 statement, §4 bullet; L04 Remark 1.3 and lab description; lab-M4-L04-1 docstring; new cards c222-c229 "
        "and c233). Every changed hunk was read and re-verified. Every row was re-derived this round; no row is carried except the "
        "L05-L10 part of A-H10 (byte-identical pages). Round-4 FAIL rows: A-G08 still FAIL (M3 file unchanged); L03-STD-NORMAL-DUP now "
        "PASS (the round-4 fix option 'keep Proposition 2.8 in L03 with the law stated as the Lesson 6 law' was taken: one definition "
        "in L06, pointer in L03, no restatement); NOTATION-A still FAIL (registry unchanged, L07 unchanged); L04-REMARK-1-3 now PASS. "
        "New this round: L03-NUMBERING (FAIL, low: 2.7 missing) and CARD-M4-c219 (FAIL, low: no grade or basis; the round-4 row did not "
        "check the grade field). "
        "Residual for the Architect (not a row): BUILDER 1.10 says no concept is used before it is introduced, and plans/M4-open-items.md "
        "item 1 says L03 cannot derive the normal moments without an undefined concept. L03 still uses the standard normal law by name "
        "before Lesson 6 (a plain-text pointer). The round-4 fix allowed this option; the Architect should confirm it or move Proposition "
        "2.8 to Lesson 6. "
        "Mutation testing: slice a has no grader, so mutants is empty (verifier rules: mutation applies to project graders). "
        "Lab twins are demonstrations: the twins run under python -I -W error, and no lab claims a property the code does not check "
        "(checked against the docstrings and printed lines). "
        "Process note: 'Predicted/Stated before running' in the lab texts is a lab convention, not a build process; not counted as a "
        "process word. "
        "Cards: the deck has 225 cards; 94 are slice-a (L01 23, L02 20, L03 30, L04 21); all 94 read and checked; numbers 0 missing; "
        "exact duplicates 0; near-duplicates (Jaccard >= 0.6) are distinct facts."
    ),
    "summary": (
        "Slice a round 5 at 440ed3c: 78 rows, 74 PASS and 4 FAIL, 0 UNVERIFIABLE. FAIL rows: A-G08 (repo ruff format, file under ledgers/M3/retired, "
        "unchanged, outside slice a), NOTATION-A (phi unregistered and shared with the L07 characteristic function), L03-NUMBERING "
        "(Proposition 2.8 after Assumption 2.6 with no 2.7), CARD-M4-c219 (no grade or basis). All gates re-run this round and PASS "
        "except ruff format: check_pages, check_dag, check_projects, run_labs 13/13, twins under python -I -W error, page_smoke "
        "slice pages, ruff check, mypy strict, relevant pytest, verify_refs --offline, plus a live Crossref check of "
        "blitzstein2019introduction (HTTP 200, record matches). Own scripts: m4a_r5_numbers.py (93 OK), m4a_r5_seeded.py, "
        "m4a_r5_cards.py (0 missing, 0 duplicates)."
    ),
}

out = ROOT / "ledgers" / "M4" / "M4-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
statuses = {}
for r in rows:
    statuses[r["status"]] = statuses.get(r["status"], 0) + 1
print("rows", len(rows), statuses)
print("wrote", out)
