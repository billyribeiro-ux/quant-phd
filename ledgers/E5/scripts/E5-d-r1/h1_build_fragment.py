"""Builds ledgers/E5/E5-d.json (closing delta, round 1, verifier H1) from the rows below. Run with python -I."""
import json, sys

CARRY = "Carried from round 1 (files byte-identical since the previous pin 2a805c83): "
FRESH = "Fresh at d9de2fe5 (h1out/ outputs): "
O = "ledgers/E5/scripts/E5-d-r1/h1out/"
rows = []

def row(id_, check, location, evidence, status="PASS"):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

# ---- base non-PASS row, re-verified from scratch (subject changed in index.html line 37) ----
row("idx-data-status-labs-simulated",
    "Index data sentence: course labs labelled SIMULATED or illustrative; project Lab 3 labels the term spread REAL",
    "course/modules/E/E5/index.html line 37 (Data meta-row); project.html lines 352-353 and 497; tests/labs/E5/lab-E5-project-3.py",
    FRESH + "the round-1 FAIL text ('The labs use SIMULATED numbers') is gone. New line 37: 'The course labs use SIMULATED numbers or "
    "illustrative parameters, each labelled as such. Project Lab 3 reads the term spread from the embedded H.15 snapshot and labels it REAL.' "
    "Each course lab is labelled: L01 'SIMULATED' (L01.html line 156), L02 'SIMULATED' (line 137), L03 'illustrative parameters' (line 192), "
    "L04 (line 182), L05 (line 120), L06 'The lab is SIMULATED' (line 114), L07 'illustrative inputs' (line 124), L08 'illustrative' (line 92) "
    "(grep of course/modules/E/E5/L0n.html and tests/labs/E5/*.py). Project Lab 3 prints 'REAL: term spread from ust_daily.csv' "
    "(project.html line 528 and lab-E5-project-3.py) and its prose says 'The term spread is REAL' (project.html line 353).")

# ---- base rows whose subject changed: re-verified fresh ----
row("proj-lab2-gap-survivor",
    "Lab 2 hypothesis, rung-2 ladder and interpretation match the lab check (round-4 FAIL re-verified)",
    "project.html line 45 (Rung 2) and lines 303-307 (Lab 2 interpretation); tests/labs/E5/lab-E5-project-2.py; ledgers/E5/mutants/project-2*",
    FRESH + "numbers.out: log gap -0.1838416 (-0.18), percent-of-trend gap -0.1836727 (-0.18), same sign True, recomputed from the seeded path "
    "(seed 2026, 24 quarters) with the window-trend convention of project.html 'Window and trend'. The text of line 45 and the printed block "
    "(project.html 306 'output gap (%): -0.18') agree. standing_mutants.out: r4_m05_gap_percent_of_trend.py and m02_gap_percent_of_trend.py "
    "print PASSES_CHECK, as line 45 states. The two conventions definitions (project.html lines 61-62) define the log gap and mention the percent-of-trend gap.")
row("proj-honest-pending",
    "Honest-pending data note on the project page",
    "course/modules/E/E5/project.html line 343 (section#data, p.honest-pending)",
    FRESH + "line 343 now says 'the missing source is an open data gap of this module'. No redistributable national-accounts source is embedded "
    "(course/assets/data/market/MANIFEST.json holds only fx_daily, fx_monthly, ust_daily; plans/E5-open-items.md line 6 and 67 carry the DATA_REQUESTS section). "
    "The lab is labelled SIMULATED (project.html 343, 328-329). PASS.")
row("cards-c032-basis-vs-key-row",
    "E5-c032 (changed): grade, basis and statement against L02 Proposition 2.4 and Definition 2.1; key-results row",
    "course/modules/E/E5/cards.json E5-c032; L02.html Definition 2.1, Proposition 2.4 (lines 96-123), key-results row line 406",
    FRESH + "E5-c032 back: Res(t;a)-Res(t;a') = -(a-a')(dlnK-dlnL) matches Definition 2.1 (Res = dlnY - a dlnK - (1-a) dlnL, L02 line 98) "
    "and Proposition 2.4 (line 122); the decomposition holds for every alpha 'by Definition 2.1' (true: Res is defined as the leftover). Grade T matches the key-results row 406 (grade T). "
    "OBSERVATION (not a ruling-26 kind, not FAIL): ruling 13 asks a card and its key-results row to carry the same basis; c032 basis is "
    "'Proposition 2.4; Definition 2.1' and row 406 basis is 'Proposition 2.4; Lab 1 averages at alpha = 0.2 and 0.4'. The grades agree.")
row("cards-changed-c033",
    "E5-c033 (changed): residual-measures-technology card, hypothesis and statement",
    "course/modules/E/E5/cards.json E5-c033 back; L02.html Definition 2.1, Proposition 2.4 (lines 120-123), Theorem 2.3 with Assumption 1.3 (line 69)",
    FRESH + "back now says 'the average residual depends on that alpha whenever the average growth of capital and of labour differ (Proposition 2.4)'. "
    "Proposition 2.4 (L02 line 123): given alpha != alpha', the two average residuals coincide iff average K growth = average L growth; "
    "the chosen share ranges over (0,1) (Definition 2.1, line 97). 'Only inside the model of Assumption 1.3' matches Assumption 1.3 (line 69, A_t positive, same alpha). PASS.")
row("cards-c034-missing-hypothesis",
    "E5-c034 (changed): 'does the choice of alpha matter' card, hypothesis and basis",
    "course/modules/E/E5/cards.json E5-c034 back and basis; L02.html Proposition 2.4 (line 123) and misconception (lines 284-285)",
    FRESH + "basis now 'Definition 2.1; Proposition 2.4' (Definition 2.1 is the residual identity; Proposition 2.4 gives the change). "
    "Average residuals at alpha = 0.2 and 0.4 differ by 0.005589 (L02 Lab 1 print lines 257-258; recomputed 0.016254 - 0.010665 = 0.005589, "
    "and 0.2 x (0.035556 - 0.007610) = 0.005589 from numbers.out). 'a different number for each alpha whenever ... differ' holds for every pair alpha != alpha' in (0,1). PASS.")
row("cards-changed-c040",
    "E5-c040 (changed): 'Is zero a steady state of the recursion' card, answer and basis",
    "course/modules/E/E5/cards.json E5-c040 front/back/basis; L03.html Definition 2.1 (line 93), Proposition 2.2 (line 98), Remark 2.3 (line 111), Assumption A4 (line 73)",
    FRESH + "Definition 2.1 (L03 line 93): a steady state is a number k* > 0 with g(k*) = k*. Under that definition zero is not a steady state, so the answer 'No' is correct; "
    "the card also says zero is a fixed point, g(0) = 0 under A1 (Remark 2.3, line 111), which is true. A4 (k_0 > 0, line 73) and Remark 2.3 ('A4 excludes zero ... keeps capital at zero') match. "
    "OBSERVATION (wording only): 'No ... although zero is a fixed point' can read as contradictory to a learner; it is correct under the definition.")
row("cards-changed-c099",
    "E5-c099 (changed): inflation-change card, numbers and claim against L06 Corollary 3.2 and section 5",
    "course/modules/E/E5/cards.json E5-c099 back; L06.html Corollary 3.2 (line 278-284), section 5 misconceptions (lines 303-307), Assumptions A1-A3 (lines 63-74), Proposition 2.1 (beta_t > 0, line 93)",
    FRESH + "Under A1-A3 change in inflation = -beta_t (u_t - u^n) (L06 line 284). beta_t = kappa/(nu P_{t-1}) > 0 (Proposition 2.1, line 93), so the change is nonzero exactly when the gap is nonzero (line 284: 'zero exactly when u_t - u^n = 0 because beta_t > 0'). "
    "Numbers: -(5/6)(-0.01) = +0.008333 (L06 line 307, exactly 1/120). '(§5)' points to section 5 (line 303, 'Misconceptions'), which carries the same sentence (line 307). PASS.")
row("cards-changed-c032-c040-c099-grade-basis",
    "Changed cards keep the grade and basis of their lesson basis (T) and no card duplicates another",
    "course/modules/E/E5/cards.json (E5-c032, c033, c034, c040, c099)",
    FRESH + "card_structure.out: 140 cards, 140 unique ids, no duplicate fronts or backs, every cited Definition/Proposition/Remark/Assumption label appears in the card's own lesson (cited labels absent: []). "
    "Ids: missing 135 only (ruling 2 allows gaps). grades: c032 T, c033 T, c034 T, c040 T, c099 T.")
row("lesson-L01-def-1-6",
    "L01 Definition 1.6 (changed): deflator 'is a price index (Section 2 gives the indices)'",
    "course/modules/E/E5/L01.html line 89 (Definition 1.6); Section 2 of L01.html (Definition 2.1 Laspeyres and Paasche indices, line 105)",
    FRESH + "the pointer is accurate: section 2 'Price indices and measured inflation' gives the indices (Definitions 2.1-2.3). The statement that real GDP is nominal GDP divided by a deflator with D_0 = 1 and D_t > 0 is unchanged. PASS.")
row("lessons-delta-hunks",
    "Changed lesson hunks in L01, L02 and L03 (the delta from 2a805c83): every claim re-derived",
    "course/modules/E/E5/L01.html line 89; L02.html lines 51, 131, 269, 281, 285, 379, 406, 436, 439; L03.html lines 52, 393, 581",
    FRESH + "L02 l.51/131: the average residual changes whenever average K and L growth differ (Proposition 2.4 averaged; numbers.out 'avg dlnK 0.0355562, avg dlnL 0.0076104'). "
    "L02 l.269: by Definition 1.1, A_t is the only term in output other than K_t and L_t (alpha is an exponent parameter). "
    "L02 l.281 and 285: Theorem 2.3 'inside the model of Assumption 1.3' (A_t known) and 'an identity for every alpha by Definition 2.1' (the residual is defined as the leftover) are accurate. "
    "L02 l.379: 0.3 -> 0.5 gives -(0.5-0.3)(dlnK-dlnL) = -0.2(...), arithmetic correct. L02 l.406/436/439: T row, correct option and explanation match Proposition 2.4. "
    "L02 E2 (l.359-361): 0.2 x 0.027947 = 0.005589, consistent with 0.016254 - 0.010665 (lab prints lines 257-258). "
    "L03 l.52: convergence 'conditional on Assumption 3.1' (monotone convergence, used without proof, line 127; Proposition 3.1 'Assuming Assumption 3.1', line 133); Lab 1 Part C checks the sign of g(k)-k on 50 grid values (tests/labs/E5/lab-E5-L03-1.py line 11, 86). "
    "L03 l.393: n+delta dependence of the steady state is exactly Proposition 2.2 (k* = (s/(n+delta))^(1/(1-alpha)), line 100). "
    "L03 l.581: (k*)^alpha is the typeset form of the same quantity as Remark 2.5 (i) (line 121). No ruling-26 defect found.")
row("lab-twins-L04-L06-delta",
    "Lab twins L04 to L06 and their pages (unchanged in this delta); each twin runs alone under -I -W error",
    "tests/labs/E5/lab-E5-L04-1.py, lab-E5-L05-1.py, lab-E5-L06-1.py; course/modules/E/E5/L04-L06.html",
    FRESH + "twins_I_W_error.out: all 11 E5 twins exit 0 with -I -W error. run_labs_E5.out 'run_labs E5: PASS (11/11)'. L04-L06 and their twins are not in the 2a805c83..HEAD diff (git diff --stat).")
row("cards-delta-coverage",
    "Every card whose text changed since the base pin is re-verified (ruling 30)",
    "course/modules/E/E5/cards.json",
    FRESH + "python diff of cards.json by id, 2a805c83 vs HEAD: changed ids E5-c032, c033, c034, c040, c099 (no additions or removals). Each has a row above (c032 with the basis note, c033, c034, c040, c099).")
row("cmd-page-smoke-changed-pages",
    "page_smoke for the pages changed in the delta (index, L01, L02, L03, project) and the rest of E5",
    "course/modules/E/E5/index.html, L01-L08.html, project.html",
    FRESH + "page_smoke_E5.out: index.html PASS, L01 PASS, L02 PASS, L03 PASS, L04 PASS, ... 'page_smoke E5: PASS', exit 0 (run with --unit E5 --pages L01..L08 index project).")
row("changed-hunks-L07-L08-index",
    "L07 and L08 hunks (earlier delta) and index hunks of this delta",
    "course/modules/E/E5/L07.html line 52 and 227; L08.html line 52; index.html lines 37, 51, 60, 147, 161",
    "L07 and L08 are not in the 2a805c83..HEAD diff (git diff --stat), so their earlier hunks stand as verified at 2a805c83 (carried). "
    "Index hunks re-verified fresh: l.37 (idx-data-status-labs-simulated), l.51 and l.147 (the average residual wording matches Proposition 2.4), "
    "l.60 (prerequisite concepts resolve, see idx-prereq-build-status), l.161 ('SIMULATED 24-quarter path' matches project Lab 1 and the rung 1 text, project.html 78 and 82). PASS.")
row("idx-prereq-build-status",
    "Index prerequisites and P0.1 status sentence (line 35 and changed line 60)",
    "course/modules/E/E5/index.html lines 35 and 60; course/concepts.html entries",
    FRESH + "index line 60 links resolve: comparative-statics (E1 L04), competitive-equilibrium (E1 L03), derivative (M2 L04), implicit-function-theorem (M2 L21), exponential-and-logarithm (M1 L03) each define data-concept/def ids in the built module (grep course/modules). "
    "evidence-grade, notation-conventions, project-ladder are 'not yet released' in course/concepts.html lines 39, 40, 44. Line 35 names P0.1 as not yet released. PASS.")
row("cmd-lab2-standing-mutants",
    "Standing lab-2 mutant set re-run (ruling 37: no new mutants)",
    "ledgers/E5/mutants/project-2*/; project.html lab-2 expected block (second pre.expected)",
    FRESH + "standing_mutants.out: total 21; 14 KILLED (r4_m01-m04, r5_m01-m03, m01, m03-m08); 5 correct alternatives PASS (project-2-r4 alt01 and alt02; project-2/alt alt01-03); 2 survivors (r4_m05 and m02, percent-of-trend gap) documented by project.html line 45. "
    "No new mutants authored in this round.")
row("cmd-check-projects", "tools/check_projects.py --all", "tools/check_projects.py --all",
    FRESH + "check_projects.out: 'check_projects E5: PASS', exit 0.")
row("cmd-check-dag", "tools/check_dag.py --all", "tools/check_dag.py --all",
    FRESH + "check_dag.out: 'check_dag E5: PASS', exit 0 (covers the changed index.html concept links).")
row("cmd-check-pages", "tools/check_pages.py --all", "tools/check_pages.py --all",
    FRESH + "check_pages.out: 'check_pages E5: PASS', exit 0 (banned strings and structure, covers the changed L01, index and project).")
row("cmd-run-labs", "tools/run_labs.py --unit E5", "tests/labs/E5/*; course/modules/E/E5/*.html",
    FRESH + "run_labs_E5.out: 'run_labs E5: PASS (11/11)', exit 0; the changed project-3 twin and page block agree (run_labs compares page code to twin).")
row("cmd-page-smoke-project", "tools/page_smoke.py --unit E5 --pages L01-L08 index project", "course/modules/E/E5 pages",
    FRESH + "page_smoke_E5.out: 'page_smoke E5: PASS', exit 0.")
row("cmd-pytest", "pytest tests/test_labs.py -k E5; pytest tests/test_page_checks.py; pytest tests/test_memo_exemplars.py", "tests/",
    FRESH + "pytest_labs_E5.out 11 passed, exit 0; pytest_page_checks.out 41 passed, exit 0; pytest_memo_exemplars.out 14 passed, exit 0.")
row("cmd-verify-refs", "tools/verify_refs.py --offline; tools/verify_refs.py --unit E5", "references/references.json",
    FRESH + "verify_refs_offline.out 'offline integrity: 560 entries, 0 problems', exit 0; verify_refs_E5.out 'live re-verification of E5: 4 of 560 entries, 0 problems', exit 0 (the tool's own live path).")
row("proj-hours",
    "Hours arithmetic: hub split and lesson hours against the project",
    "index.html lines 29, 31, 42 (data-hours, eyebrow, split); project.html line 33 and #hours-table",
    CARRY + "index.html lines 29, 31, 42 and project.html line 33 are outside every hunk of the delta. Re-derived: 8 lessons x 10 h = 80 h (index.html line 144); 80 + 30 = 110 h; 30/110 = 27.27% (27.3%); 80/110 = 72.7%. Project hours table total 30 (project.html line 571). PASS.")
row("proj-adversarial-and-mutants",
    "Grading mode, mutants and alternatives for the project; no process words in learner text",
    "course/modules/E/E5/project.html #spec Grading mode (line 323); tests/labs/E5; ledgers/E5/mutants; index.html and L01-L08 changed text",
    FRESH + "mutate_graders_E5.out: 'exit 0', no output (no grader mutant files directly under ledgers/E5/mutants/*.py). standing set as in cmd-lab2-standing-mutants. "
    "grep of index.html and L01-L08 and project.html for mutant|grader|alternative|adversar|verifier|ledger|fixer: only project.html 323 'No adversarial review is used for this project' (a grading-mode statement, not process language about the build). Round-half-to-even only in the lesson text. PASS.")
row("proj-notation",
    "Notation of the project page against notation/notation.json",
    "course/modules/E/E5/project.html LaTeX spans and the changed Taylor-rule bullet (line 372-373); notation/notation.json",
    FRESH + "the changed bullet renames the plain-text Taylor value 'i' to 'i_star' (the page and twin, same symbol as the conventions line 70, i^{\\ast}_t). "
    "No new symbol is introduced; notation/notation.json is unchanged in the delta. OBSERVATION (carried from base registry flags, not a ruling-26 kind): i^{\\ast} names the IS-LM equilibrium rate in L04 and the Taylor-rule value in the project, and i^{\\ast} is not in notation.json. PASS.")
row("proj-dag",
    "Project page concept use and DAG",
    "course/modules/E/E5/project.html; tools/check_dag.py --all; course/modules/E/E5/index.html concept links",
    FRESH + "check_dag.out 'check_dag E5: PASS'. Concept links on the project page are the same as the index (E1, M1, M2 definitions, not yet released P0.1 entries). PASS.")
row("proj-reading-list",
    "Project reading list against references/references.json",
    "course/modules/E/E5/project.html #reading (lines 757-769); references/references.json",
    CARRY + "project.html lines 757-769 are outside every hunk; references/ unchanged in the delta; verify_refs (cmd-verify-refs) PASS.")
row("proj-process-words",
    "No process words in learner text",
    "project.html whole page; index.html; L01-L08 changed text; tools/check_pages.py banned strings",
    FRESH + "check_pages E5 PASS (banned strings); grep (see proj-adversarial-and-mutants) finds no process words in the changed text.")
row("cards-scope-and-duplicates", "Card scope, ids and duplicates",
    "course/modules/E/E5/cards.json",
    FRESH + "card_structure.out: 140 cards, 140 unique ids, 140 unique fronts, no duplicate backs; c135 absent (ruling 2 allows gaps).")
row("cards-numbers-in-lesson", "Every numeric token of each card appears in its lesson",
    "course/modules/E/E5/cards.json; course/modules/E/E5/L01-L08.html",
    FRESH + "card_numbers_strict.out: 'tokens not in own lesson, not in any twin output: []'. card_structure.out lists only E5-c102 '1.226' and '1.236', which appear in the L06 expected block as 1.226000 and 1.236000 (L06.html line 231).")
row("cards-sample-2", "E5-c020 against L01 Proposition 2.6 and misconception 4",
    "cards.json E5-c020; L01.html Proposition 2.6 and Lab 1 Part C",
    FRESH + "c020 numbers recomputed: nominal growth 105/995 = 0.105528; deflator 4/23 = 0.173913 (Paasche 27/23); real growth (1100/995)/(27/23) - 1 = -0.058254 (h1out/numbers.out, lines for c019-c022). The card is unchanged and L01 Proposition 2.6 is unchanged (not in the delta hunks except the Definition 1.6 pointer). PASS.")
row("cards-sample-3", "E5-c030 against L02 Definition 2.2",
    "cards.json E5-c030; L02.html Definition 2.2 (lines 103-104)",
    CARRY + "cards.json E5-c030 and L02 Definition 2.2 (lines 103-104) are outside every hunk.")
row("cards-sample-4", "E5-c040 against L03 Remark 2.3", "cards.json E5-c040; L03.html Remark 2.3 (line 111)",
    FRESH + "see cards-changed-c040. PASS.")
row("cards-sample-5", "E5-c050 against L03 Proposition 4.2 and Assumption 4.1",
    "cards.json E5-c050; L03.html Assumption 4.1 (line 155-156), Proposition 4.2 (lines 160-165)",
    CARRY + "E5-c050 is byte-identical (not among the five changed ids); L03 Proposition 4.2 and Assumption 4.1 (lines 155-165) are outside every hunk (the L03 hunk at 393 touches a list item, not Proposition 4.2). Proposition 4.2 derivative formulas re-derived by hand in this round: at the steady state H_k = -(1-alpha)(n+delta), so dk*/ds = k*/((1-alpha)s) and dk*/dn = dk*/ddelta = -k*/((1-alpha)(n+delta)).")
for n, loc, lesson_part in [
    ("cards-sample-6", "E5-c060 against L04 Definition 3.1", "L04.html Definition 3.1"),
    ("cards-sample-7", "E5-c070 against L04 Proposition 3.2 and Remark 1.2", "L04.html"),
    ("cards-sample-8", "E5-c080 against L05 Proposition 2.2", "L05.html"),
    ("cards-sample-9", "E5-c090 against L06 section 1", "L06.html section 1"),
    ("cards-sample-10", "E5-c100 against L06 Definition 1.2 and Lab 1 Part C", "L06.html"),
    ("cards-sample-11", "E5-c110 (Taylor rule) against L07 Definition 1.4", "L07.html Definition 1.4"),
    ("cards-sample-12", "E5-c120 (fiscal multiplier) against L08 Definition 1.2", "L08.html Definition 1.2"),
    ("cards-sample-13", "E5-c130 (no estimate of the multiplier) against L08 page statement", "L08.html Proposition 2.2 and the statement near line 274"),
]:
    row(id_ := n, loc, lesson_part, CARRY + "the card and " + lesson_part + " are outside every hunk of 2a805c83..HEAD (L04-L08 unchanged in the delta; cards not in the changed-id list). PASS.")
row("cards-derivations",
    "Derivation-type cards: values and hypotheses",
    "cards.json E5-c014, c022, c035, c051, c052, c062, c064, c065, c079, c080, c099, c102, c122-c125, c128, c129",
    FRESH + "c099 re-verified (cards-changed-c099); c022 basket A values re-derived (numbers.out c022 line). c035 values 1.029006, 0.029006 and 0.028593 re-derived (numbers.out c035 line). c051 10/7 = 1.4285714286 and c052 k* = 5.5843115042, (k*)^0.3 = 1.6752934513 re-derived (numbers.out c051, c052 lines). "
    "Remaining derivation cards (c062-c065, c079, c080, c102, c122-c125, c128, c129) cite lesson blocks outside the delta hunks, so they are CARRIED from round 1 (byte-identical).")
row("cards-lab-numbers",
    "Lab-number cards: numbers equal the printed lab values and appear in the lesson",
    "cards.json E5-c019-c021, c033-c034, c036, c048, c051-c052, c067-c069, c082-c087, c100-c104, c113-c117, c127-c129, c141",
    FRESH + "c033 and c034 carry no lab number after the delta; c019, c020, c021 and c022 re-derived in h1out/numbers.out (ln 1.25 = 0.223144, diff 0.026856; 160, 20, 180; 5/4, 27/23, 7/92). "
    "Other lab-number cards are CARRIED (byte-identical; their lesson lab blocks are outside the hunks); card_numbers_strict.out shows every token is in its lesson.")
row("cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental", "repository; tests/labs/E5 twins",
    FRESH + "ruff_check.out 'All checks passed!' exit 0; ruff_format.out '555 files already formatted' exit 0; mypy.out 'Success: no issues found in 386 source files' exit 0.")
row("proj-lab2-student-errors", "Lab 2 student-error mutants fail; alternatives pass",
    "tests/labs/E5/lab-E5-project-2.py; ledgers/E5/mutants/project-2*/",
    FRESH + "standing_mutants.out (see cmd-lab2-standing-mutants): 14 killed, 5 correct alternatives pass, 2 documented survivors (not grader findings: project.html line 45 states that the instant check does not separate the log and percent-of-trend gaps).")
row("cmd-build-site", "tools/build_site.py --check", "course/index.html, concepts.html, data",
    FRESH + "build_site_check.out 'site data current: 6 outputs', exit 0.")
row("cmd-render-curriculum", "tools/render_curriculum.py and git diff --exit-code CURRICULUM.md curriculum/curriculum.json", "CURRICULUM.md; curriculum/curriculum.json",
    FRESH + "render_curriculum.out 'curriculum valid ... wrote curriculum/curriculum.json and CURRICULUM.md', exit 0; render_diff.out (git diff --exit-code) exit 0 (no change).")
row("cmd-fetch-data", "tools/fetch_data.py --check", "course/assets/data/market/",
    FRESH + "fetch_data_check.out 'fetch_data: 3 datasets, 0 problems', exit 0.")
row("cards-changed-c014-c016", "E5-c014 and E5-c016 against L01 Propositions 2.4 and 2.6",
    "cards.json E5-c014, E5-c016; L01.html Propositions 2.4 and 2.6 (lines 124-151)",
    CARRY + "the cards and the Propositions 2.4 and 2.6 blocks are outside the hunks (the only L01 hunk is Definition 1.6 at line 89). Proposition 2.6 uses the deflator form, which Definition 1.6 still defines. PASS.")
row("cards-changed-c041-c045", "E5-c041 to c045 against L03 Propositions and Remark 2.5",
    "cards.json E5-c041..c045; L03.html Proposition 2.2 (lines 97-101), Proposition 4.2, Remark 2.5 (lines 120-122)",
    CARRY + "the cards are byte-identical and the cited Propositions and Remark 2.5 statements are outside the hunks. The hunks at L03 lines 393 and 581 are a list item and a hidden explanation; both were re-verified in lessons-delta-hunks. PASS.")
row("cards-remark-labels", "Remark, Definition, Proposition, Assumption and Problem labels cited by cards exist in the card's lesson",
    "cards.json basis and back fields; L01-L08.html",
    FRESH + "card_structure.out: 'cited labels absent from own lesson: []'.")
row("proj-exA-c2-annotation", "Exemplar A computation annotation and memo text (C2 level 4)",
    "project.html #exemplar-a Computation (line 623-628)",
    FRESH + "memo Computation paragraph (project.html line 624) names growth_annualised, inflation_yoy, output_gap, taylor_value and read_quarter_spreads, which are defined in the Lab 3 block (project.html lines 352-520), and says rounding applies only to the printed output. PASS.")
row("proj-exA-length", "Exemplar A memo within the brief's 600-word body limit; headings as the brief requires",
    "project.html #exemplar-a memo (lines 601-657); brief item (line 548-555)",
    FRESH + "h1out/words.out (h1_words.py): six memo paragraphs, 586 body words, 593 with the six headings. Limit is 600 (project.html line 321).")
row("proj-lab2-one-pair", "Lab 2 reads one SIMULATED pair of yields (latest of 24) and the docstring says so",
    "project.html Lab 2 docstring (lines 199-215) and interpretation (line 307); tests/labs/E5/lab-E5-project-2.py",
    CARRY + "project.html lines 199-215 and the lab-2 twin are outside every hunk. The lab-2 output block (lines 302-306) is unchanged.")
row("proj-spec-ladder", "Project ladder, spec, data, lab-3 section, brief and stretch items",
    "project.html #ladder (lines 40-47), #spec (311-323), #data (327-344), #lab-3-section (347-376), #brief (546-556), #stretch (748-756)",
    FRESH + "ladder rung 1 now refers to the cycle flag defined under Conventions (anchor id=conventions, line 51) and rung 2 to the output gap definitions (lines 61-62). Spec, data and stretch text match the lab outputs (lab-3 table lines 530-533 recomputed in numbers.out).")
row("proj-rubric-observable", "Rubric table: each level observable",
    "project.html table#rubric (lines 580-588)",
    CARRY + "table#rubric (lines 580-588) is outside every hunk.")
row("proj-calib-exB", "Exemplar B calibration scores and annotations",
    "project.html #exemplar-b data-scores=2,2,2,2,1 (line 669)",
    CARRY + "exemplar B is outside every hunk. Ruling 23: no E5 blind scorer file exists in ~/.fanout/blind/ (listing: BK4-c, CS2-d, E1-d, E3-d, E4-d, FC2-d, LX1-c, M5-d, PC3-c), so the base calibration rows are carried.")
row("proj-calib-exA-blind", "Exemplar A calibration scores (blind)",
    "project.html #exemplar-a data-scores=4,4,4,4,3 (line 596)",
    CARRY + "data-scores attribute unchanged. Ruling 23: no dedicated blind scorer file for E5 in ~/.fanout/blind/, so the base calibration row is carried per the closing-delta rule. NOTE: the Exemplar A memo's Data paragraph (line 613, punctuation only) and the verdict text (lines 598 and 663) changed in this delta; a blind scorer is needed to re-calibrate, and none was run.")
row("proj-conventions-gaps", "Conventions: log gap defined, percent-of-trend gap contrasted, window and trend",
    "project.html #conventions (lines 51-72)",
    FRESH + "numbers.out: log gap -0.1838416 and percent-of-trend gap -0.1836727 at 2026 Q3, both -0.18 to two decimals, same sign. Conventions text unchanged (outside the hunks).")
row("proj-lab1-numbers", "Lab 1 hypothesis, expected block, interpretation",
    "project.html lines 81-82 and 189-195; tests/labs/E5/lab-E5-project-1.py",
    FRESH + "numbers.out recompute: growth 0.209242 -> 0.21; inflation 1.896020 -> 1.90; gap -0.183842 -> -0.18; the flag 'mixed' (growth positive, gap negative). run_labs E5 PASS.")
row("proj-lab3-table", "Lab 3 expected table against its twin",
    "project.html lines 527-541 (printed table); tests/labs/E5/lab-E5-project-3.py with data/ust_daily.csv",
    FRESH + "numbers.out (independent recompute, all four rows): 2025 Q4 3.15 | 1.92 | 0.11 | 3.91 | 1.44 | 3.94 | -2.49 | 0.37; 2026 Q1 2.51 | 1.98 | 0.19 | 4.07 | 1.65 | 4.06 | -2.40 | 0.60; 2026 Q2 2.48 | 1.85 | 0.24 | 4.12 | 1.53 | 3.90 | -2.36 | 0.80; 2026 Q3 0.21 | 1.90 | -0.18 | 4.10 | 1.53 | 3.75 | -2.22 | 0.96. All equal the printed table. run_labs PASS.")
row("proj-lab3-expected-prose", "Lab 3 expected prose values and signs",
    "project.html lines 353 and 542",
    FRESH + "line 353 values (growth 0.21, inflation 1.90, output gap -0.18, unemployment 4.10, policy 1.53, Taylor 3.75, policy gap -2.22, spread 0.96) match numbers.out. Signs: inflation minus 2.0 negative, unemployment minus 4.0 positive, policy gap negative, spread positive. Days 62, 61, 63, 64 (line 542) match numbers.out.")
row("proj-lab3-days-and-spread", "Lab 3 day counts and the spread's quarter means",
    "project.html #data-spread (lines 341-344); course/assets/data/market/ust_daily.csv; MANIFEST.json",
    FRESH + "numbers.out: header date,tbill_3m,cmt_10y; 6690 rows; first 2000-01-03, last 2026-09-30; day counts 62, 61, 63, 64 for 2025 Q4..2026 Q3; spread means 0.374, 0.604, 0.798, 0.957 (0.96 two decimals). MANIFEST ust_daily retrieved 2026-10-20 (line 71).")
row("proj-data-licence", "Embedded H.15 snapshot licence and source note quoted on the project page",
    "project.html #data-spread (line 342); tools/data_sources.yaml line 101; course/assets/data/market/MANIFEST.json",
    CARRY + "project.html line 342 is outside every hunk; MANIFEST.json and tools/data_sources.yaml are unchanged in the delta, and the licence text is identical in MANIFEST (lines 10, 37, 68).")
row("proj-basis-claims", "Spread basis caveat (discount-rate bill, constant-maturity 10-year) and its limit in the memo",
    "project.html #data-spread (line 344) and Exemplar A Limits (line 658)",
    FRESH + "tools/data_sources.yaml line 101: 'tbill_3m is the 3-month bill's secondary-market rate on a discount basis'; project line 342 quotes the same. Memo Limits (line 658) names the mixed basis and gives no direction, as the verdict (line 598) says.")
row("proj-taylor-exA", "Exemplar A Taylor-rule value, policy gap and sensitivity",
    "project.html #exemplar-a Policy reading (lines 645-651)",
    FRESH + "numbers.out: Taylor value 3.752108 -> 3.75; policy gap 1.53 - 3.752 = -2.22; taylor bounds for inflation in [1.895,1.905] and gap in [-0.185,-0.175] are [3.75, 3.77]; phi_y 0.5 -> 1.0 changes the value by 0.5 x gap = -0.0919 (about -0.09) and the policy gap becomes -2.133 (about -2.13); half-range -0.0925 to -0.0875. All as the memo says.")
row("proj-exB-numbers", "Exemplar B numbers and annotations (wrong convention, wrong quarter, omitted terms)",
    "project.html #exemplar-b (lines 669-735)",
    CARRY + "exemplar B is outside every hunk. Arithmetic checked: 2 + 0.5 x (-0.18) = 1.91 (the memo's rule value) and 2026 Q2 gap 0.24 (Lab 3 table, 2026 Q2 row, project.html line 532).")
row("proj-atlas-disclosure", "Spec inputs disclose the series sources and the Atlas status",
    "project.html #spec Inputs (lines 316-317); curriculum/02-economics-finance-core.yaml lines 184-190",
    CARRY + "project.html lines 316-317 and curriculum/ are outside the hunks (curriculum and tools unchanged in the delta).")
row("proj-page-length-and-voice", "Brief: one-page memo, six headings in order; exemplar headings",
    "project.html #brief (lines 546-555); Exemplar A h5 headings (lines 601-657)",
    FRESH + "six headings in order (Summary, Data, Computation, Diagnosis, Policy reading, Limits) match the brief (line 548-555). Memo body 586 words (proj-exA-length).")
row("proj-no-network-no-file-input", "Project page makes no network request and takes no file input",
    "project.html #data (lines 327-344)",
    CARRY + "project.html lines 329 and 340 are outside the hunks; the delta adds no input element (grep 'type=\"file\"' finds none).")
row("proj-delta-window-definition", "Conventions: window and trend definition",
    "project.html #conventions 'Window and trend' (lines 59-60)",
    CARRY + "project.html lines 59-60 are outside every hunk; the window (20 quarters ending at t) matches the lab code (WINDOW = 20).")
row("proj-delta-exA-limits", "Exemplar A Limits (C5 direction wording)",
    "project.html #exemplar-a Limits (line 658) and annotation (line 663)",
    FRESH + "Limits names the target direction (a higher target lowers the Taylor value, because the inflation term enters with coefficient 0.5: a one-point rise in the target moves the value by -0.5), the trend's end-point with no direction ('this memo does not say which way') and the spread basis with no direction. The verdict (598) and the miss (663) say exactly this. PASS.")
row("proj-exA-c5-verdict", "C5 verdict and miss wording in exemplar A consistent with the memo Limits",
    "project.html lines 598 and 663",
    FRESH + "598 'C5 falls short of level 4: the memo gives a direction for the target, but names the trend's end-point and the spread's basis as limits and gives no direction for either.' 663 'Misses C5 level 4: names the trend's end-point and the spread's basis as limits, but gives no direction for either.' Both match memo line 658. Data scores 4,4,4,4,3 unchanged.")
row("proj-evidence-scale-sentence",
    "Project line 557 evidence-scale definitions of B and C match the program's BLUEPRINT scale",
    "course/modules/E/E5/project.html line 557; BLUEPRINT.md lines 160-161 and 171",
    FRESH + "BLUEPRINT.md line 160 (B: 'Published in a top peer-reviewed venue, but not robustly replicated or actively contested'), line 161 (C: 'Working paper, practitioner research, or single-sample evidence'); project line 557 uses the same wording, and the counter-evidence rule matches BLUEPRINT line 171. PASS.")
row("proj-lab3-definition-exact-counts",
    "Lab 3 counts 64 days in 2026 Q3 and uses exact fractions for the spread (project 'Lab 3' docstring)",
    "project.html Lab 3 docstring (lines 364-365); tests/labs/E5/lab-E5-project-3.py",
    FRESH + "numbers.out: 2026 Q3 count 64; the quarter mean is an exact Fraction in read_quarter_spreads (Lab 3 block) and equals 0.956875 -> 0.96.")
row("proj-line42-placement-skip",
    "Project line 42 (changed): 'If you pass the placement check on the module page, skip to rung 3' against the module's skip rule",
    "course/modules/E/E5/project.html line 42; course/modules/E/E5/index.html lines 71-72 and 159",
    FRESH + "index line 72: 'To skip rungs 1 and 2, you must reach the bar and answer both skill checks.' The project sentence refers to the module page's placement check by name without restating the bar or the two skill checks. "
    "The reference is complete only if 'pass' means that rule. OBSERVATION (wording; not a ruling-26 kind): 'pass' is undefined on the project page. PASS.")
row("proj-lab2-gap-survivor-doc",
    "The two surviving lab-2 mutants are documented on the page, not hidden (ruling 9 / verifier rule 11)",
    "project.html line 45; ledgers/E5/mutants/project-2/m02_gap_percent_of_trend.py; ledgers/E5/mutants/project-2-r4/r4_m05_gap_percent_of_trend.py",
    FRESH + "project.html line 45 states that the instant check does not separate the log gap from the percent-of-trend gap and that a percent-of-trend line passes it. So these are not new grader findings. They are still files in ledgers/E5/mutants/ (ruling 9 asks that survivors not stay there); see notes.")

# ---- mutants (standing set, no new mutants) ----
mutants = [
    {"id": "r4_m01_spread_sign_reversed", "description": "student error: spread sign reversed", "killed_by": "KILLED fresh: standing_mutants.out, token 27 -0.83 vs 0.83 beyond 1e-6"},
    {"id": "r4_m02_spread_previous_quarter", "description": "student error: spread uses previous quarter", "killed_by": "KILLED fresh: token 27 1.01 vs 0.83"},
    {"id": "r4_m03_gap_time_index_off_by_one", "description": "student error: gap time index off by one", "killed_by": "KILLED fresh: token 31 -0.67 vs -0.18"},
    {"id": "r4_m04_gap_trend_at_window_start", "description": "student error: trend evaluated at window start", "killed_by": "KILLED fresh: token 31 9.10 vs -0.18"},
    {"id": "r4_m05_gap_percent_of_trend", "description": "student error: percent-of-trend gap instead of log gap; SURVIVES the instant check, documented on project.html line 45 (not a grader finding)", "killed_by": ""},
    {"id": "r5_m01_spread_sum_not_difference", "description": "student error: spread as sum, not difference", "killed_by": "KILLED fresh: token 27 3.83 vs 0.83"},
    {"id": "r5_m02_gap_growth_not_level", "description": "student error: gap from growth, not level", "killed_by": "KILLED fresh: token 31 0.05 vs -0.18"},
    {"id": "r5_m03_gap_trend_window_19", "description": "student error: trend window 19 quarters", "killed_by": "KILLED fresh: token 31 0.30 vs -0.18"},
    {"id": "m01_gap_intercept_only", "description": "student error: gap uses intercept only", "killed_by": "KILLED fresh: token 31 9.10 vs -0.18"},
    {"id": "m02_gap_percent_of_trend", "description": "student error: percent-of-trend gap (earlier copy); SURVIVES, documented on project.html line 45 (not a grader finding)", "killed_by": ""},
    {"id": "m03_gap_lagged_output", "description": "student error: gap uses lagged output", "killed_by": "KILLED fresh: token 31 -0.24 vs -0.18"},
    {"id": "m04_gap_window_24", "description": "student error: gap window 24 quarters", "killed_by": "KILLED fresh: token 31 -2.14 vs -0.18"},
    {"id": "m05_spread_reversed", "description": "student error: spread reversed", "killed_by": "KILLED fresh: token 27 -0.83 vs 0.83"},
    {"id": "m06_spread_fixed_offset", "description": "student error: spread with fixed offset", "killed_by": "KILLED fresh: token 27 0.80 vs 0.83"},
    {"id": "m07_gap_sign_flipped", "description": "student error: gap sign flipped", "killed_by": "KILLED fresh: token 31 0.18 vs -0.18"},
    {"id": "m08_gap_log10", "description": "student error: gap uses log10", "killed_by": "KILLED fresh: token 31 -0.08 vs -0.18"},
]

notes = [
    "Delta: git diff 2a805c83..d9de2fe5 over course/modules/E/E5, tests/labs/E5 and ledgers/E5/mutants touches L01 (line 89), L02 (9 hunks), L03 (3 hunks), cards.json (changed ids E5-c032, c033, c034, c040, c099; none added or removed), index.html (lines 37, 51, 60, 147, 161), project.html (lines 42, 44-45, 343, 372-373, 557, 598, 613, 663) and tests/labs/E5/lab-E5-project-3.py (docstring lines 19-20). L07, L08, L04-L06 and all twins other than project-3 are unchanged in this delta. Shared paths tools/, references/, notation/, curriculum/, plans/E5*, course/index.html, course/concepts.html and course/assets/data are unchanged since 2a805c83 (git diff --stat empty).",
    "Ruling 37: no new mutants were authored. The standing set (16 mutants and 5 correct alternatives, total 21) was re-run: standing_mutants.out, 14 killed, 5 alternatives PASS, 2 survivors (r4_m05, m02) documented on project.html line 45. The two survivors are still files under ledgers/E5/mutants/. Ruling 9 asks that survivors not stay there unless they are killed or moved to equivalent/ with a proof; the closing round does not change them, so this is an Architect decision. The merged ledger verdict (tools/ledger.py) will read FAIL until that is decided, because the two survivors have no killed_by.",
    "Ruling 26 kinds checked on the changed text: no false or unproved statement, no missing hypothesis, no wrong number, no over-graded claim, no failing gate, no non-equivalent surviving mutant, no lab statement the code does not support. Every changed number was recomputed independently (numbers.out). No FAIL row was found.",
    "Base FAIL row idx-data-status-labs-simulated is re-verified PASS: the sentence was changed in the delta and now scopes SIMULATED to the course labs and REAL to project Lab 3, which matches the labels in the lab code and output.",
    "OBSERVATION (not FAIL, not a ruling-26 kind): card E5-c032 basis 'Proposition 2.4; Definition 2.1' differs from the key-results row (line 406) basis 'Proposition 2.4; Lab 1 averages'. Grades agree (T). Ruling 13 asks the same basis; the textual difference predates the delta (the delta added Definition 2.1 to the card).",
    "OBSERVATION (wording): project.html line 42 'If you pass the placement check on the module page' does not restate the bar or the two skill checks the module page requires (index line 72). Consider naming them.",
    "OBSERVATION (wording): card E5-c040 answers 'No' to 'Is zero a steady state of the recursion' while stating that zero is a fixed point. It is correct under Definition 2.1 (k* > 0); a clearer front would help learners.",
    "OBSERVATION (notation, carried from the base registry flags): i^{\\ast} names the IS-LM equilibrium rate in L04 and the Taylor-rule value in the project, and i^{\\ast} is not in notation/notation.json. Ruling 13 asks for one meaning per symbol; this is for the Architect.",
    "Calibration (ruling 23): no E5 blind scorer file exists in ~/.fanout/blind/. The base calibration rows are carried. Exemplar A's memo Data paragraph (line 613) changed punctuation in this delta, and the verdict text changed; a blind re-score is recommended before the calibration is treated as current.",
    "Carried from round 1 (files byte-identical since 2a805c83, except the cited lines listed in each row): L04-L08 lesson text and their cards, the L01-L03 blocks outside the hunks, references/, notation/, curriculum/, tools/, and the project lab twins other than project-3. Carry prefix used on each carried row.",
    "Registry flags carried from the base fragment (not changed by this delta): references/references.json blanchard2020macroeconomics has year 2020 while curriculum yaml says 8th ed. (2021) (the page prints no year); curriculum/02-economics-finance-core.yaml lines 186-187 still say the brief uses 'Atlas' series (architect decision B2); plans/E5-open-items.md names u^{\\ast} for the natural rate while the page uses u^n.",
    "Not checked: the rubric exemplars were not re-scored blind (ruling 23); the lesson prose of L04 to L08 outside the delta was not re-read (carried); plain-curl access checks to the H.15 licence page were not repeated (the verifier rules allow the tool's own verify_refs path, which passed: verify_refs_E5.out).",
]

registry_flags = [
    "references/references.json blanchard2020macroeconomics: record year 2020 while curriculum yaml line 182 says '8th ed. (2021)'. The page prints no year. Architect to decide; not changed by this delta.",
    "curriculum/02-economics-finance-core.yaml lines 186-187 still say the brief uses series 'from Atlas'; the page uses no Atlas series (architect decision B2). Not changed by this delta.",
    "plans/E5-open-items.md names u^{\\ast} for the natural rate of unemployment; the page and L06 use u^n. Stale planning note.",
    "i^{\\ast} is the IS-LM equilibrium rate in L04 and the Taylor-rule value in the project; i^{\\ast} is not in notation.json. Architect to decide whether to rename one.",
]
freshness_flags = [
    "ledgers/E5/scripts/E5-d-r5/ and ledgers/E5/mutants/project-2-r5/ are cited by earlier rounds; not re-run in this closing delta (not in its rows).",
    "No E5 blind scorer file in ~/.fanout/blind/ (ruling 23): exemplar calibration is carried, not re-scored.",
]

frag = {
    "unit": "E5",
    "slice": "E5-d",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent closing-delta verifier H1 for E5-d, round 1 (ruling 30; did not build E5)",
    "pin": "d9de2fe5",
    "base": "2a805c83 (round-1 fragment ~/.fanout/frags/G-E5-d.round1.json, FAIL on idx-data-status-labs-simulated; its base 95f3f8cb)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyH1-E5-d",
    "scratch": "ledgers/E5/scripts/E5-d-r1/h1out (outputs), ledgers/E5/scripts/E5-d-r1/h1_*.py and h1_gates.sh (scripts)",
    "verified_at": "2026-11-09",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": ("E5-d closing delta, pin d9de2fe5 (base 2a805c83): %d rows, all PASS. The base FAIL row idx-data-status-labs-simulated is "
                "re-verified PASS. Changed hunks in L01, L02, L03, five cards, index.html, project.html and the project-3 twin were re-derived "
                "from scratch; gates re-run (ruff, mypy, check_pages/dag/projects, run_labs, page_smoke, pytest, verify_refs, build_site, "
                "render_curriculum, fetch_data, mutate_graders, standing set). Two documented lab-2 survivors remain in ledgers/E5/mutants/ "
                "(Architect decision, see notes)." % len(rows)),
}

out = sys.argv[1]
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows), "status counts", {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")})
