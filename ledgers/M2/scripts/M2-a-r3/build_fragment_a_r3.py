"""Builds the round-3 verifier fragment ledgers/M2/M2-a.json (slice a: index.html and L01-L06, lab twins, cards of L01-L06).

Every row's evidence names the script or file that backs it (paths relative to the checkout). Run:
    .venv/bin/python -I ledgers/M2/scripts/M2-a-r3/build_fragment_a_r3.py <checkout-root>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/M2/scripts/M2-a-r3/"
P = "PASS"
F = "FAIL"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        if not fix:
            raise SystemExit(f"row {rid} is not PASS and has no fix")
        item["fix"] = fix
    rows.append(item)


# ---- 2.9 gates and tool rows (run at pin 8196077d) ----
row("M2a-R1-G01", "2.9 structure gate: check_pages --unit M2", "tools/check_pages.py --unit M2", P,
    f"Run at pin 8196077d: 'check_pages M2: PASS', exit 0. Output {S}g01_check_pages.out.")
row("M2a-R1-G02", "2.9 DAG gate: check_dag --unit M2", "tools/check_dag.py --unit M2", P,
    f"'check_dag M2: PASS', exit 0. Output {S}g02_check_dag.out.")
row("M2a-R1-G03", "2.5 labs: run_labs --unit M2", "tools/run_labs.py --unit M2", P,
    f"'run_labs M2: PASS (27/27)', exit 0 (the six slice labs are among the 27). Output {S}g03_run_labs.out.")
row("M2a-R1-G04", "2.5 twins alone under python -I -W error", "tests/labs/M2/lab-M2-L01-1.py .. lab-M2-L06-1.py", P,
    f"{S}lab_slice_a_r3.py run with .venv/bin/python (CPython 3.14.8) -I -W error: each twin exit 0, stderr 0 bytes, "
    f"stdout equal to the page expected block, page code equal to the twin (ALL PASS). Output {S}g04_twins_isolated.out.")
row("M2a-R1-G05", "2.5 pytest lab suite for the six slice labs", "tests/test_labs.py -k 'M2 and (L01..L06)'", P,
    f"'6 passed', exit 0; collect-only for M2 gives 27 lab tests. Output {S}g05_pytest_labs.out.")
row("M2a-R1-G06", "2.9 page_smoke for index and L01-L06", "tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06 --skip-sweep", P,
    f"'page_smoke M2: PASS', exit 0; every page PASS; lab runtimes 0.0 s; no figures on these pages (no data-chart). "
    f"Output {S}g08_page_smoke.out. The sweep was skipped because the slice has no figures.")
row("M2a-R1-G07", "2.5 ruff and mypy on the six slice twins", "ruff check, ruff format --check, mypy --no-incremental on tests/labs/M2/lab-M2-L0[1-6]-1.py", P,
    f"'All checks passed!', '6 files already formatted', 'Success: no issues found in 6 source files'. Outputs {S}g06_ruff.out, {S}g07_mypy.out.")
row("M2a-R1-G08", "2.1 citations: verify_refs offline and live for M2", "tools/verify_refs.py --offline; tools/verify_refs.py --unit M2", P,
    f"'offline integrity: 560 entries, 0 problems'; 'live re-verification of M2: 2 of 560 entries, 0 problems'. "
    f"Outputs {S}g10_verify_refs_offline.out, {S}g11_verify_refs_live_M2.out.")
row("M2a-R1-G09", "2.6 project structure gate (unit level; slice a has no project rows)", "tools/check_projects.py --unit M2", P,
    f"'check_projects M2: PASS', exit 0. Output {S}g09_check_projects.out. run_graders and mutate_graders belong to the project slices.")

# ---- 2.9 hub (index.html) ----
row("M2a-R1-H01", "2.9 hub sections: objectives, prerequisites, placement, lessons, ladder, data, reading",
    "course/modules/M/M2/index.html:45-194", P,
    "Read in full. Seven objectives with measurable verbs (lines 48-56, count 7 by structure_slice_a_r3.py); prerequisites M1 and P0.1 "
    "linked (61-65); placement section data-mastery 0.8 with 8 items, 2 data-skill (69-137); lesson map of 24 cards (143-168); "
    "ladder with four rungs in order (174-179); data status 'No real data' (184); core reading as registry keys (190-191). "
    "Card text for L01-L06 checked against each lesson; L07-L24 card text compared only with their section headings (a loose check; those lessons belong to slices b-e). See H09 for the one fragment.")
row("M2a-R1-H02", "2.9 hours split and arithmetic", "course/modules/M/M2/index.html:29, 42, 141-142", P,
    "data-hours-lessons=240, data-hours-project=60 (line 29). Every L01-L24 page declares data-hours=\"10\" (grep count 24 x 10 h = 240). "
    "240 + 60 = 300 = curriculum (plans/M2-build-plan.md section 0). 60/300 = 20 %, inside 10-40 %. Recomputed in "
    f"{S}recompute_slice_a_r3.out (hub rows).")
row("M2a-R1-H03", "2.9 placement arithmetic", "course/modules/M/M2/index.html:71", P,
    "Eight items (6 M1/P0.1 multiple-choice, 2 skill checks). 80 % of 8 = 6.4, so at least 7 correct; 6/8 = 75 %, 7/8 = 87.5 %. "
    f"Recomputed in {S}recompute_slice_a_r3.out.")
row("M2a-R1-H04", "2.2 and 2.9 placement skill-check 2 explanation against the project", "course/modules/M/M2/index.html:135", P,
    "Fixed since round 2. Now: '3 + 0.1^2 = 3.01. This is the central difference of a cubic, worked in Lesson 5 (Misconception 3). The rung 2 "
    "completion problem asks for the second difference and the dual-number product line instead.' Checked: L05.html:218-219 "
    "(Misconception 3 is the central difference of x^3, error h^2) and project.html:45 (rung 2 blanks the second difference and the "
    "dual-number product line).")
row("M2a-R1-H05", "2.9 prerequisite links resolve; P0.1 entries honest", "course/modules/M/M2/index.html:61-65; course/concepts.html", P,
    f"{S}links_slice_a_r3.py: 0 problems (internal hrefs and anchors resolve). Concept ids quantifiers, direct-proof, proof-by-contradiction, "
    "mathematical-induction, exponential-and-logarithm are M1 in curriculum/curriculum.json concepts; evidence-grade, notation-conventions, "
    "project-ladder are P0.1. course/concepts.html shows P0.1 entries as 'not yet released' and M1 entries as 'defined here' (grep).")
row("M2a-R1-H06", "2.9 placement explanations cite M1 correctly", "course/modules/M/M2/index.html:80, 89, 98, 107 (Hq1-Hq4)", P,
    "Hq1 -> M1/L01.html Theorem 3.2 (a), negation of forall-exists is exists-forall-not (checked). Hq2 -> M1/L02.html proof by contradiction, "
    "square root of 2 and lowest terms (checked). Hq3 -> M1/L06.html geometric-sum closed form by induction (checked). Hq4 -> M1/L03.html "
    "natural logarithm inverts the exponential (checked).")
row("M2a-R1-H07", "2.9 cross-lesson pointer in L04 canon-breaks to Lesson 13 rounding", "course/modules/M/M2/L04.html:156; course/modules/M/M2/L13.html", P,
    "L13.html section 3 is 'Rounding error: a model' (grep). The pointer 'Lesson 13 treats the effect of rounding on the quotient' is accurate.")
row("M2a-R3-H08", "2.9 and 2.2 placement skill-check 1: explanation names rung 1's task; BUILDER_RULES 5.1 two-item rule",
    "course/modules/M/M2/index.html:130", F,
    "The explanation says: 'This is the worked-example task of rung 1, taught in Lesson 4.' Rung 1 (project.html:44 and 53-58) is one SIMULATED "
    "bond's price and its yield derivatives, by cash-flow formula and central difference. Skill check 1 (limit of the difference quotient of x^2 at "
    "a = 1, answer 2) is not that task. Skill check 2 (central difference of a cubic) is the only item that matches a rung 1 skill, so the "
    "'at least two items that test the skills rungs 1-2 teach' requirement (BUILDER_RULES 5.1) is not met as written. Checked against "
    "project.html and BUILDER_RULES.md section 5.1.",
    "Either re-target skill check 1 to a skill rung 1 or rung 2 teaches (for example the central difference of a simple price at a step, or "
    "the second difference of a function), or keep the derivative-by-definition item and change line 130 to say what it tests without "
    "calling it rung 1's task. Then at least two items must match rung 1 or rung 2 skills.")
row("M2a-R3-H09", "2.9 card text reads as a sentence", "course/modules/M/M2/index.html:164 (L21 card-body)", F,
    "The card text is 'When an equation defines one variable as a differentiable function of another, and the implicit derivative.' It has no main "
    "clause (a subordinate clause and a noun phrase). The other 23 card texts are noun-phrase summaries.",
    "Rewrite as a noun-phrase summary, for example: 'The implicit-function theorem: when an equation defines one variable as a differentiable "
    "function of another, and the implicit derivative.' (a complete sentence or a noun phrase, consistent with the other cards).")

# ---- 2.9 prose, notation, quizzes and structure across the slice ----
row("M2a-R1-X01", "2.9 banned phrases and placeholders", "index.html, L01-L06.html visible text and the 82 slice cards",
    P, f"{S}prose_scan_slice_a_r3.py: banned-phrase count 0 (TODO, TBD, lorem, ellipsis, for brevity, beyond the scope, obviously, clearly, "
    f"well known, studies show, and the rest of BUILDER_RULES 1.3-1.4). Output {S}prose_scan_slice_a_r3.out, TOTALS banned 0.")
row("M2a-R1-X02", "2.9 process words in learner text", "index.html, L01-L06.html visible text and cards",
    P, f"{S}prose_scan_slice_a_r3.py: process-word hits are 'fixed' only, used as a mathematical word (a fixed epsilon, fixed numbers). "
    "No builder, verifier, round, fragment, architect, ruling or ledger word appears in learner text.")
row("M2a-R1-X03", "2.4 notation: macros and registry symbols", "notation/notation.json; index.html, L01-L06.html", P,
    "Macros used in the slice: \\R (registered), and standard LaTeX commands (varepsilon, delta, dfrac, lim, bigl, bigr and others; counts in "
    f"the round-3 log). \\eta appears once in L05 as a local name, not a registered symbol. No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, "
    "R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) is used with another meaning. Plain Q(h) in L04-L05 is the difference quotient, a different symbol from "
    "the registered \\mathbb{Q} (a probability measure); recorded as a judgement. M is a limit (L01 Proposition 2.2) and an index (L01 "
    "Proposition 3.1); neither is registered (judgement).")
row("M2a-R1-X04", "2.5 quiz numeric answers and tolerances", "index.html placement; L01-L06 quizzes", P,
    f"Each numeric answer recomputed exactly in {S}recompute_slice_a_r3.out: index 2 and 3.01 (tol 1e-6); L01 1.999001 (tol 1e-6, exact "
    "2001/1001), 10000, 0.1, 3; L02 3, 0.02990099 (tol 1e-8, exact 302/10100), 0.1090909 (tol 1e-7, exact 6/55); L03 7, 2, 1.39 (tol 5e-4); "
    "L04 2, 3.31, -0.25 (tol 1e-7), 0; L05 1, 96, 2, 0; L06 1.1547 (tol 1e-4, 2/sqrt3 = 1.1547005), -3, 8.")
row("M2a-R1-X05", "2.9 retrieval quiz structure (8-15 items, explanations, one correct option)",
    "index.html placement; L01-L06 quiz sections", P,
    f"{S}structure_slice_a_r3.out and grep counts: index 8 items, L01 9, L02 9, L03 8, L04 9, L05 9, L06 9; each item has one explanation; "
    "each multiple-choice item has one data-correct option.")
row("X-GRADE-01", "2.3 grades: key-results rows, lab interpretations and cards (ruling 13)",
    "course/modules/M/M2/L05.html:338 (key-results row 4); cards.json:377, 400", F,
    "Checked every key-results row and card. Consistent with ruling 13 in L01 (T: Proposition 2.2, Example 2.3, Proposition 3.1, Proposition 4.2, "
    "Example 4.1; C: the 1000 threshold from lab output), L02 (C for 6/55 and the lab values, T for Proposition 1.1, Corollary 2.2, Example 2.3), "
    "L03, L04 and L06. Failing: L05.html:338 (key-results row 4) grades 'the three analytic derivatives are 32.0625, 0.591837 and 95.0625, and "
    "each central difference is within 1e-6' as C with source Lab 1. The value 95.0625 is derived by hand in numbered Example 2.2 "
    "(L05.html:189-191), and ruling 13 grades such a value T with that Example as basis. The lab-only values 32.0625 and 0.591837 are C "
    "(their derivations sit in the lab hypothesis, not in a numbered Example).",
    "Split row 4 of the L05 key-results table: (a) T, 'the chain-rule derivative at x = 1.5 is 95.0625' with source Example 2.2; (b) C, "
    "'Lab 1: the analytic values 32.0625 and 0.591837 and each central difference within 1e-6 of its analytic value at h = 1e-4', with source "
    "Lab 1. Then card M2-c058 is fixed under row L05-CARD-01.")
row("X-DEP-01", "2.9 and 2.4 DAG at the prose level", "index.html, L01-L06.html; check_dag output", P,
    f"{S}g02_check_dag.out: 'check_dag M2: PASS'. Concept links in the slice are to M1 and P0.1 concepts (closure of M2, see H05) or to M2's own "
    "limit (L01) and derivative (L04), each defined before its first use; no link to a later lesson; continuity, the chain rule and "
    "undeclared terms are prose only (Architect decisions Q5-Q7). L02 uses 'continuity' in prose with no dfn, as decided.")
row("X-HRS-01", "2.9 hours and why-it-matters length", "L01-L06.html headers and why-it-matters paragraphs", P,
    "data-hours=\"10\" on L01-L06. Why-it-matters word counts (structure_slice_a_r3.py): L01 85, L02 85, L03 96, L04 72, L05 93, L06 84, all <= 120. "
    "L02 and L05 changed in this round and were re-read in full.")
row("X-CARD-IDS", "2.7 cards: ids, structure, numbers and duplicates (slice cards and unit scan)",
    "course/modules/M/M2/cards.json:448, 454, 461 (L06) with :2728, 2734, 2741 (L08, L10)", F,
    f"{S}cards_dup_slice_a_r3.py over all 394 cards: no duplicate ids and no identical fronts. Near-duplicates of one fact: "
    "M2-c064 (L06, 'Is Assumption 2.1 (extreme value theorem) proved? No.', cards.json:448) and M2-c416 (L08, 'Is Assumption 1.1 (the extreme value "
    "theorem) proved in Lesson 8? No.', cards.json:2728); M2-c065 (L06, Rolle's theorem statement, cards.json:454) and M2-c417 (L08 Theorem 1.2, "
    "Rolle's theorem under Assumption 1.1, cards.json:2734); M2-c066 (L06, mean value theorem statement, cards.json:461) and M2-c418 (L10 "
    "Theorem 1.2, mean value theorem under Assumption 2.1 of Lesson 6, cards.json:2741). Ids need not be sequential (ruling 2). The 82 slice "
    "cards have ids, lesson fields and content matching their lessons (checked one by one); every number on a card appears in its lesson "
    "(c006, c025, c026, c035, c036, c046, c047, c056-c058, c069, c070 checked).",
    "Keep one card per fact. Either delete M2-c416, M2-c417 and M2-c418, or rewrite each to test a use of the result that its lesson makes "
    "(for example the remainder argument in L08 or the use in L10). Then rerun cards_dup_slice_a_r3.py; the L06 cards are then unique.")
row("X-REF-01", "2.1 core reading and references sections", "index.html:187-194; L01-L06 References sections", P,
    "Registry keys spivak2008calculus and hubbard2015vector (index.html:190-191) pass verify_refs offline and live (G08). The lesson "
    "References sections attribute no statement to either source and claim no locator (judgement: consistent with the 'No passage "
    "locator' sentence in each page). No new citation is made in the slice.")

# ---- L01 ----
row("L01-MATH-01", "2.4 mathematics: sections 2-4 of L01", "course/modules/M/M2/L01.html:55-189", P,
    f"Read line by line. Definition 2.1; Proposition 2.2 proof (epsilon/2 thresholds and triangle inequality); Example 2.3 (a_n - 2 = -1/(n+1)); "
    "Proposition 3.1 (tail) proof with N' = max(N, M); Example 4.1 (contradiction: 2 <= |1-L| + |L+1| < 2); Proposition 4.2 proof with "
    f"B = max(|a_1|..|a_{{N-1}}|, |L|+1). Re-derived in {S}recompute_slice_a_r3.out (L01 rows, all OK).")
row("L01-MATH-02", "2.2 and 2.4 problem set, misconceptions and key-results rows of L01", "L01.html:219-339", P,
    "M1 (13/(n+4) and N = 1297 for 0.01: checked), M2 (least N = 11: checked), M3, P1-P3, E1 (9.990010e-4 from 1/1001: checked by Decimal), "
    "E2, E3 (N = 10000, error at 9999 = 1e-4: checked), R1-R3. Misconception 1 cites Problem M3 (a later problem on the same page, not a concept). "
    f"Key rows 330-334 are T and row 335 is C (see L01-GRADE-01). Output {S}recompute_slice_a_r3.out.")
row("L01-LAB-01", "2.5 lab: page code, expected block, hypothesis values", "course/modules/M/M2/L01.html:87-150; tests/labs/M2/lab-M2-L01-1.py", P,
    f"{S}lab_slice_a_r3.py: page code equals the twin, expected block equals twin stdout, isolated run exit 0 with empty stderr. Hypothesis values "
    "(3/2, 1/2, 1/11, 1/101, least N = 1000, error at 999 = 1e-3) recomputed exactly.")
row("L01-GRADE-01", "2.3 grade of the threshold row", "L01.html:335; cards.json M2-c006", P,
    "C for 'least N = 1000 for 0.001 and the strict inequality fails at 999'. Example 2.3 gives N > 1/epsilon, which is 1001 for 0.001 (the row says "
    "so), and 1000 follows from the identity 1/(n+1) < 1/1000 that the lab hypothesis and E2 state by hand. Under ruling 13 this is not a numbered "
    "Example's derivation, so C with Lab 1 as basis is correct. Judgement recorded.")
row("L01-PROSE-01", "2.2 and 2.9 problem-set introduction against problem E3", "L01.html:221 and E3 at 289-294", P,
    "'Problems marked E use the output of Lab 1, except E3, which predicts a value from the formula of Example 2.3.' E3 predicts 10000 and states "
    "that no lab run checks it (L01.html:293), which matches.")
row("L01-QUIZ-01", "2.9 retrieval quiz", "L01.html:341-411", P,
    "9 items (5 multiple-choice, 4 numeric); each has an explanation; numeric answers verified (X04); Proposition 2.2 and Example 4.1 "
    "explanations match the statements.")
row("L01-CARD-01", "2.7 cards of L01", "cards.json lesson L01 (16 cards: c001-c013, c376, c390, c391)", P,
    "Each card checked against L01 text. c009 matches the current Example 4.1 (L01.html:174). c010 matches Misconception 1. c376 matches the "
    "Proposition 4.2 proof. c006 is C with basis Lab 1. No duplicate within L01 (X-CARD-IDS covers the unit-wide scan).")
row("L01-CARD-02", "2.7 card grade and basis mirror the key-results row", "cards.json M2-c006; L01.html:335", P,
    "Card c006 (C, basis 'Lab 1, a finite search over 1 to 5000; the identity |a_n - 2| = 1/(n+1) in Example 2.3') mirrors key row 335 (C, "
    "same lab and identity).")

# ---- L02 ----
row("L02-MATH-01", "2.4 mathematics: Proposition 1.1 (i)-(iii), Corollary 2.2, Examples 2.1 and 2.3",
    "course/modules/M/M2/L02.html:55-176", P,
    "Proposition 1.1 (i) split at epsilon/2; (ii) identity a_n b_n - ab = a_n(b_n - b) + b(a_n - a), bound |a_n| < |a| + 1, |b|/(|b|+1) < 1; "
    "(iii) delta = |b|/2, 1/|b_n| < 2/|b|, identity (b(a_n - a) - a(b_n - b))/(b b_n), thresholds eps|b|/4 and eps|b|^2/(4(|a|+1)) giving "
    "bracket < eps|b|^2/2. Corollary 2.2 and Examples 2.1 and 2.3 checked. Hypotheses stated in each statement.")
row("L02-MATH-02", "2.4 remark, canon-breaks, misconceptions, problems and key rows of L02", "L02.html:178-333", P,
    "Remark 3.1 (a_n = 1, b_n = 1/n gives n). Misconceptions 1-3 (f(x) = x + 1 for x != 1, f(1) = 0, limit 2, not continuous: checked). "
    "Problems M1 (limit 3), M2 (1/2), M3 (0), P1-P3, R1 (|a_n/b_n| to infinity: (|a|/2)/|b_n| > M, checked), R2, R3 (b_n = s_n - a_n, checked). "
    f"Key rows 326-329. Output {S}recompute_slice_a_r3.out.")
row("L02-LAB-01", "2.5 lab: page code, expected block, interpretation", "course/modules/M/M2/L02.html:76-152; tests/labs/M2/lab-M2-L02-1.py", P,
    f"{S}lab_slice_a_r3.py: page code equals twin, expected block equals stdout, isolated run clean. Closed forms (n+2)/(n(n+1)), "
    "(3n+2)/(n(n+1)), (5n+4)/((n+1)(n+2)) checked exactly for n = 1..5000; n = 10 gives 6/55, 16/55, 9/22; the printed rows for n = 1..10000 "
    f"match (recompute). Interpretation 'five indices only' matches GRID. Output {S}recompute_slice_a_r3.out.")
row("L02-PROSE-01", "2.2 Example 2.1 title and its sentence", "course/modules/M/M2/L02.html:159-160", P,
    "'Example 2.1 (the identity)': f(x) = x is continuous at every a, from x_n -> a giving f(x_n) = x_n -> a = f(a). Correct.")
row("L02-PROSE-02", "2.9 rhetorical-question opener (BUILDER_RULES 1.4)", "course/modules/M/M2/L02.html:51", P,
    "Fixed since round 2. The opener is now 'The limit laws state when a sum, product or quotient of two convergent sequences converges, and to "
    f"what value, under a stated hypothesis.' No question in L02 prose outside problem prompts ({S}prose_scan_slice_a_r3.out).")
row("L02-E-01", "2.2 problems E1-E3 use Lab 1 output", "course/modules/M/M2/L02.html:269-291", P,
    "E1: 12/110 = 6/55 ~ 0.109091 and printed 1.090909e-01 (checked). E2: 302/10100 = 0.0299009900..., printed 2.990099e-02 (checked). "
    "E3: (3/2)/3 = 1/2, error 3/2, closed form 9/6 (checked).")
row("L02-QUIZ-01", "2.9 retrieval quiz", "course/modules/M/M2/L02.html:335-408", P,
    "9 items (6 multiple-choice, 3 numeric); each has an explanation; numeric answers verified (X04); the item on the converse of the product law "
    "uses Problem P3 (checked).")
row("L02-CARD-01", "2.7 cards of L02", "cards.json lesson L02 (13 cards: c014-c026)", P,
    "Each card checked against L02 text (Proposition 1.1 hypotheses in c014, the three laws in c015-c017, Corollary 2.2 in c022, Example 2.3 "
    "in c023, misconceptions in c018, c019, c024). c025 and c026 are C with basis 'Lab 1, exact values from the closed forms', while key row 4 says "
    "'... on the page'. Same grade and same source (Lab 1); the basis wording differs only by 'on the page'. Judged a match, as in round 2.")

# ---- L03 ----
row("L03-MATH-01", "2.4 mathematics: sections 1-2 of L03", "course/modules/M/M2/L03.html:53-108", P,
    "Definition 1.1; Example 1.2 with delta = epsilon/3 (checked); Proposition 1.3 proof; Corollary 1.4 proof (x_n = a case); Definition 2.1; "
    "Proposition 2.2 both directions (delta = min(delta+, delta-)); Example 2.3 with delta = min(1, eps/2) on the left and eps/2 on the right (checked).")
row("L03-MATH-02", "2.2 and 2.4 problem set and key rows of L03", "L03.html:208-328", P,
    "M1 (delta = 0.01 for 2x-1 at 3), M2 (sign function), M3 (q(x) = x + 2), P1, P2 (delta = min(1, eps/(1+2|a|)), checked), P3, E1 (0.998001), "
    "E2 (1 + 4h - h^2 at h = 0.01 is 1.0399), E3 (x = 2.095 gives |3x+1-7| = 0.285 > 0.1, checked), R1, R2, R3. Key rows 319-324 grade T for "
    "Example 1.2, Proposition 1.3, Corollary 1.4, Proposition 2.2, Example 2.3 and C for the lab rows.")
row("L03-MATH-03", "2.4 problem R2 (bounded factor and zero limit)", "course/modules/M/M2/L03.html:298-301", P,
    "|f g| <= M|g| <= M eps/(M+1) < eps, from |g| < eps/(M+1) (checked by reading the chain; M >= 0).")
row("L03-LAB-01", "2.5 lab: page code, expected block, grid claim", "course/modules/M/M2/L03.html:112-173; tests/labs/M2/lab-M2-L03-1.py", P,
    f"{S}lab_slice_a_r3.py: page code equals twin, stdout equals expected block (0.81/2.2/1.39; 0.980100/2.020000/1.039900; 0.998001/2.002000/"
    "1.003999; 0.999800/2.000200/1.000400; grid True at three tolerances). Gap 1 + 4h - h^2 and f(1-h) = (1-h)^2 identities checked. "
    "38 grid points (interpretation) match the code (recompute).")
row("L03-PROSE-01", "2.2 and 2.9 problem-set introduction against E3", "L03.html:210 and E3 at 278-284", P,
    "'Problems marked E use the output of Lab 1, except E3, which predicts a result from the formula of Example 1.2.' E3 predicts from "
    "|f(x) - 7| = 3|x - 2| (checked).")
row("L03-QUIZ-01", "2.9 retrieval quiz", "course/modules/M/M2/L03.html:330-395", P,
    "8 items (5 multiple-choice, 3 numeric); each has an explanation; numeric answers 7, 2, 1.39 verified (X04); the option 'It does not exist' "
    "for the piecewise limit is correct by Proposition 2.2.")
row("L03-CARD-01", "2.7 cards of L03", "cards.json lesson L03 (14 cards: c027-c039, c392)", P,
    "Each card checked. c038 (revised) matches Misconception 2 (L03.html:197-199). c039 matches Misconception 3 (L03.html:201-203). c035 and c036 "
    "are C with basis Lab 1 and mirror key row 324 (C, Lab 1). c392 is a definition (open interval) matching L03.html:55.")

# ---- L04 ----
row("L04-MATH-01", "2.4 mathematics: sections 1-3 of L04", "course/modules/M/M2/L04.html:53-148", P,
    "Definition 1.1; Example 1.2 (|Q(h) - 2a| = |h|, delta = eps); Proposition 2.1 proof (delta = min(delta1, eps/(|f'(a)|+1)), "
    "f(x) - f(a) = (x-a)Q(x-a)); Example 3.1 (Q(h) = |h|/h, one-sided limits 1 and -1).")
row("L04-MATH-02", "2.4 problem set and key rows of L04", "course/modules/M/M2/L04.html:227 (P3); 178-296", F,
    "M1, M2 (Q(0.01) = -1.99, checked), M3 (Q(h) = -1/(2(2+h)), checked), P1 (checked), P2, E1-E3 (3.31, 3.00001e-5, 3.000001, checked), R1 "
    "(h|h|/h = |h|, checked), R2, R3. FAIL: P3 (L04.html:227, 'A constant multiple') has the displayed chain "
    "'|cQ(h) - cf'(a)| = |c||Q(h) - f'(a)| < |c|eps/(|c|+1) < eps'. For the allowed value c = 0 the first strict inequality reads 0 < 0, "
    "which is false.",
    "In P3 (L04.html:227) write '<=' in the middle step: |c||Q(h) - f'(a)| <= |c| eps/(|c|+1) < eps (the last strict inequality holds for every c). "
    "Or state the proof for c != 0 and note that c = 0 is trivial.")
row("L04-LAB-01", "2.5 lab: page code, expected block, hypothesis values", "course/modules/M/M2/L04.html:67-123; tests/labs/M2/lab-M2-L04-1.py", P,
    "lab_slice_a_r3.py: page code equals twin, stdout equals expected block (six quotients, error column, expansion True, error/h = 3.000001). "
    "Q(h) = 3 + 3h + h^2 identity checked exactly for h = 10^-1..10^-6; error 3.000001e-6 at h = 1e-6 (checked).")
row("L04-CARD-01", "2.7 duplicate scan of L04 cards (round-1 FAIL, re-verified)", "cards.json M2-c044, M2-c048, M2-c049", P,
    "M2-c044 (Example 3.1: |x| not differentiable at 0), M2-c048 (misconception 1: no derivative where one-sided quotients differ, |x| at 0) and "
    "M2-c049 (misconception 2: continuous does not imply differentiable) test three different facts. The round-1 duplicate is gone "
    "(c048 now states the misconception, not the same example question).")
row("L04-QUIZ-01", "2.9 retrieval quiz", "course/modules/M/M2/L04.html:298-368", P,
    "9 items (5 multiple-choice, 4 numeric); numeric answers 2, 3.31, -0.25 (tol 1e-7), 0 verified; the Q7 option '3.003001' is correct.")
row("L04-CARD-02", "2.7 cards of L04 (c040-c050)", "cards.json lesson L04 (11 cards)", P,
    "Each card checked against L04. c046, c047 and c050 are C with basis Lab 1 and mirror key row 292 (C, Lab 1). c042-c045 match Example 1.2, "
    "Proposition 2.1 and Example 3.1.")

# ---- L05 ----
row("L05-MATH-01", "2.4 mathematics: Lemma 1.1, Propositions 1.2, 1.3, 2.1", "course/modules/M/M2/L05.html:53-89, 175-187", P,
    "Lemma 1.1 proof: F/G - L/M = (M(F-L) - L(G-M))/(MG) (checked: M(F-L) - L(G-M) = MF - LG); bound 2/|M|^2; thresholds eps|M|/4 and "
    "eps|M|^2/(4(|L|+1)) give bracket < eps|M|^2/2. Proposition 1.2 identity (f(a+h)Q_g + g(a)Q_f) checked. Proposition 1.3 identity "
    "(g(a)Q_f - f(a)Q_g)/(g(a)g(a+h)) checked. Proposition 2.1 (G(k) and k(h) = 0 case) checked.")
row("L05-MATH-02", "2.4 Assumption 1.4 and every statement that uses it", "L05.html:91-95, 99, 105-108, 218-219, 282-284", P,
    "Assumption 1.4: (f(x+h) - f(x-h))/(2h) = f'(x) + h^2 f'''(x)/6 + o(h^2) (Taylor, correct). Uses begin 'Assuming Assumption 1.4' (lab "
    "hypothesis, lab docstring, Misconception 3, E1 prompt and solution). Exact cubic case 3 + h^2 checked. p''' = 60x^2 + 6 = 141 and c''' = "
    "120x^3 + 72x = 513 at 1.5 checked; the exact central-difference error of p is h^2 p'''/6 + h^4 (checked).")
row("L05-MATH-03", "2.2 and 2.4 problem set of L05", "course/modules/M/M2/L05.html:224-327", P,
    "M1 (2x+1), M2 (q'(x) = (1-x^2)/(x^2+1)^2, checked against central differences at h = 1e-12), M3 (w'(1) = 96, checked), P1 induction, P2 "
    "(1/g rule), P3 (f^2), E1 (2.35e-7), E2 (29/49 and 0.591836735, checked), E3 (95.0625), R1 (central difference of a cubic = p' + a h^2, "
    "checked), R2 (composition defined on I), R3 (quotient from product and reciprocal). Output "
    f"{S}recompute_slice_a_r3.out.")
row("L05-LAB-01", "2.5 lab: page code, expected block, analytic and central values", "course/modules/M/M2/L05.html:97-173; tests/labs/M2/lab-M2-L05-1.py", P,
    f"{S}lab_slice_a_r3.py: page code equals twin, stdout equals expected block. Exact central differences recomputed: |differences| 2.35e-07, "
    "3.33e-10, 8.55e-07; central values 32.062500235, 0.591836734, 95.062500855 (checked to nine decimals). Hypothesis values 32.0625, "
    "29/49, 95.0625 checked.")
row("L05-PROSE-01", "2.2 and 2.4 Misconception 3 numbers and assumption wording", "course/modules/M/M2/L05.html:218-219", P,
    "'The error is exactly h^2, which at h = 10^-4 is 10^-8' (exact for x^3). 'None of these is h^2' (true: 2.35e-7, 3.33e-10, 8.55e-7). "
    "'p'''(1.5) = 141 gives 2.35e-07' (checked). 'Assumption 1.4 is not proved on this page' (true). The rewritten why-it-matters "
    "(L05.html:51) states the proof from the definition with hypotheses, which is accurate.")
row("L05-QUIZ-01", "2.9 retrieval quiz", "course/modules/M/M2/L05.html:344-414", P,
    "9 items (5 multiple-choice, 4 numeric); numeric answers 1, 96, 2, 0 verified; explanations present; the chain-rule option 'the inner value' "
    "is correct.")
row("L05-CARD-01", "2.7 cards of L05", "cards.json:400 (M2-c058); lesson L05 cards c051-c061, c379, c393", F,
    "Cards c051-c057, c059-c061, c379 and c393 checked against L05 text and correct. c055 (T) states the chain-rule value 95.0625 with basis Example 2.2 "
    "(correct under ruling 13). FAIL: M2-c058 (cards.json:400, grade C, basis Lab 1) asks for c'(1.5) = 95.0625, a value derived by hand in "
    "numbered Example 2.2. Under ruling 13 that part is T, so the card's C grade is wrong for its first claim. Its lab claim (central difference "
    "95.062500855, absolute difference 8.55e-07) is C and correct.",
    "Make M2-c058 ask only for the Lab 1 result: 'In Lab 1, how far is the central difference of c(x) = (x^2 + 1)^3 at x = 1.5 from c'(1.5), at h = 10^-4?' "
    "with back '8.55e-07 (central difference 95.062500855 against 95.0625).' Keep grade C and basis 'Lab 1'. The value 95.0625 remains on card c055 (T).")

# ---- L06 ----
row("L06-MATH-01", "2.4 mathematics: Proposition 1.1, Theorem 2.2, Theorem 2.3, Corollary 3.1", "course/modules/M/M2/L06.html:55-109", P,
    "Proposition 1.1 proof (Q(h) <= 0 on the right, >= 0 on the left, contradiction with the limit). Theorem 2.2 proof (constant case by Problem R3 "
    "of L04; M != f(a) gives an interior maximum; Proposition 1.1). Theorem 2.3 proof (g = f - f(a) - s(x-a), Theorem 2.2). Corollary 3.1 (i)-(iii) "
    "proofs (Theorem 2.3 on [x,y] inside (a,b)). All re-derived.")
row("L06-MATH-02", "2.4 misconceptions and section 4 canon-breaks", "course/modules/M/M2/L06.html:183-208", P,
    "Misconception 1 (x^3 at 0, not an extremum). Misconception 2 (y^3 - x^3 = (y-x)(y^2+xy+x^2) and y^2+xy+x^2 = (x+y/2)^2 + 3y^2/4, both "
    "checked). Misconception 3 (c = 1/sqrt3 = 0.577, not 0.5). Canon-breaks: f(x) = x on [0,1) with f(1) = 0 (left-hand limit 1, checked), |x| on "
    "[-1,1] (f(-1) = f(1) = 1, checked), x^3 at 0.")
row("L06-MATH-03", "2.2 and 2.4 problem set of L06", "course/modules/M/M2/L06.html:210-313", P,
    "M1 (f' = 2x - 4, minimum at 2, f(2) = -3, checked), M2 (c = 2/sqrt3 ~ 1.1547 in (0,2), checked), M3 (f(-2) = -2 < 2 = f(-1), checked), P1, "
    "P2 (Rolle gives c in (x,y), inside (a,b)), P3 (g = -f), E1 (8), E2 (f(-1) = 2, f(1) = -2), E3 (odd multiples of 1/8, checked), R1, R2 "
    "(chord slope 0, f' = -1 and 1, not differentiable at 1, checked), R3 (Lipschitz bound by Theorem 2.3).")
row("L06-LAB-01", "2.5 lab docstring claim against code", "course/modules/M/M2/L06.html:116-125; tests/labs/M2/lab-M2-L06-1.py:116-124", P,
    "Fixed since round 2. The docstring now says 'It checks two things' and 'It also prints the values f(-1) and f(1) without a comparison', which "
    "matches the code: two comparisons (sign of f' at the 17 points; increase against sign of f' at midpoints) and one print. Expected block "
    "matches stdout (lab_slice_a_r3.py). Page code equals twin.")
row("L06-ASSUME-01", "2.4 Assumption 2.1 wording and dependence", "L06.html:71-73, 77-78, 86-88, 102-103, 111, 324-325", P,
    "The Assumption block carries no grade and says it is not proved. Theorem 2.2, Theorem 2.3, Corollary 3.1 and the statements that use them begin "
    "'Assuming Assumption 2.1'. Proposition 1.1 uses no assumption. Misconception 2 proves x^3 strictly increasing algebraically, with no use of "
    "Assumption 2.1; the card version adds 'Assuming Assumption 2.1' (not false; noted under CARD-01).")
row("L06-QUIZ-01", "2.9 retrieval quiz", "course/modules/M/M2/L06.html:332-406", P,
    "9 items (6 multiple-choice, 3 numeric); numeric answers 1.1547 (tol 1e-4), -3, 8 verified; the 'midpoint' item answer (c = 1/sqrt3) is correct.")
row("L06-CARD-01", "2.7 cards of L06", "cards.json:448, 454, 461, 475 (c064, c065, c066, c068); lesson L06 cards", F,
    "Twelve of the fifteen cards check against L06 text (c062, c063, c067, c068 note, c069, c070, c071, c072, c073, c074, c394, c414). c064, c065 and "
    "c066 repeat facts that L08 (c416, c417) and L10 (c418) restate: the extreme value theorem is assumed, Rolle's theorem is stated, and the mean "
    "value theorem is stated (see X-CARD-IDS). c068 (cards.json:475) says 'Assuming Assumption 2.1, f(x) = x^3 is strictly increasing'; the lesson "
    "proves this without the assumption, so the card carries an unneeded hypothesis. Not false; judged a note, not a failure.",
    "Resolve the duplicates under X-CARD-IDS (keep the L06 cards or retarget the L08 and L10 ones). Optional: drop 'Assuming Assumption 2.1, ' from "
    "the front-back of M2-c068 so the card matches the lesson's proof.")

# ---- hub and data-status claims ----
out = {
    "unit": "M2",
    "slice": "a",
    "round": 3,
    "verifier": "independent verifier (Haiku 5.5), unit M2 slice a, round 3 (final full verification)",
    "pin": "8196077d (detached checkout HEAD)",
    "base": ("Round-2 fragment /Users/billyribeiro/.fanout/frags/S-M2-a.round2.json (pin 9294b914). Delta 9294b914..8196077d in the slice: "
             "index.html:135 (skill check 2 explanation), L02.html:51 (why-it-matters), L05.html:51 (why-it-matters), L06.html:116-125 and "
             "tests/labs/M2/lab-M2-L06-1.py:3-8 (docstring), cards.json (c009, c038, c048, c144 removed, c234 changed; c416-c420 appended). "
             "L01, L03, L04, index.html otherwise, and the lab twins of L01-L05 are byte-identical. Every subject was re-verified in round 3 from "
             "scratch; no row is carried. All round-2 row ids are kept."),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-M2-a",
    "scratch": S,
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice a = index.html, L01-L06 with their six lab twins, and the 82 cards of L01-L06 (cards.json). No project grader in the slice, "
        "so mutation testing does not apply (ruling: mutation is for project graders; lab twins are demonstrations) and mutants is empty. "
        "Judgements recorded: (a) the 1000 threshold, f(-1)=2 and the lab-only values are C with Lab 1 as basis (ruling 13; their derivations sit in "
        "lab hypotheses and problem solutions, not numbered Examples); (b) card basis wording for c025/c026 and c035/c036 differs from the key-row "
        "wording only by 'on the page'; (c) M2-c048 is not a duplicate of M2-c044; (d) plain Q(h) in L04-L05 is the difference quotient, a symbol "
        "distinct from the registered \\mathbb{Q}; (e) M is a limit and an index in L01; (f) claim spans mark theorem titles and lab results, and "
        "examples are graded through the key-results tables, the convention of merged M1; (g) M2-c068's unneeded hypothesis is not false; (h) "
        "the hub card text 'simulated bond price' (L23) is a description, the label lives in L23. "
        "Tool note: structure_slice_a_r3.py counts solution words with a regex that treats raw '<' inside math as a tag, so its solution "
        "word counts are unreliable; check_pages (HTML parser, >= 15 words) passed and is the authority for that rule. "
        "Not checked: the rendered look at 360 px in both themes (page_smoke ran with --skip-sweep; these pages have no figures; page_smoke "
        "checks horizontal scroll at 360 px and passed); Spivak or Hubbard content (no locator is claimed, so none is needed); the content of "
        "lessons L07-L24 and the project, which belong to slices b-e (only the hub card texts for them were read); live Crossref record content "
        "beyond verify_refs output. Repository state: no course, test, reference or curriculum file was edited; scripts and outputs are under "
        f"{S}. Interpreter: .venv CPython 3.14.8 for all gates and twin runs."
    ),
    "summary": (
        "M2 slice a, round 3: verdict FAIL. 71 rows: 64 PASS, 7 FAIL, 0 UNVERIFIABLE (the 69 round-2 ids are kept; H04, L02-PROSE-02 and L06-LAB-01 "
        "are fixed and re-verified; two new rows, M2a-R3-H08 and M2a-R3-H09, are added). Non-PASS: M2a-R3-H08 (index.html:130, skill check 1 "
        "explanation calls the x^2 difference quotient rung 1's task; rung 1 is a bond sensitivity, so the two-item rule is not met), "
        "M2a-R3-H09 (index.html:164, card text is a fragment), L04-MATH-02 (L04.html:227, P3 displayed chain false at c = 0), X-GRADE-01 "
        "(L05.html:338, the derived value 95.0625 graded C instead of T by ruling 13), L05-CARD-01 (cards.json:400, M2-c058 same grade issue), "
        "X-CARD-IDS (cross-lesson duplicate cards M2-c064/c416, c065/c417, c066/c418) and L06-CARD-01 (its c064-c066 members of that set). "
        "All gates that run on the slice pass: check_pages, check_dag, run_labs 27/27, twins under python -I -W error with stdout equal to the "
        "expected blocks, pytest 6 lab tests, page_smoke for index and L01-L06, ruff, mypy strict on the six twins, verify_refs offline and live "
        "for M2, check_projects. 108 exact recomputations pass; 0 banned phrases; 0 rhetorical questions in prose."
    ),
}

target = root / "ledgers/M2/M2-a.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
fails = [r["id"] for r in rows if r["status"] != P]
print(f"wrote {target}: rows={len(rows)} pass={sum(r['status'] == P for r in rows)} fail={len(fails)} {fails}")
