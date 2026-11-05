"""Build the round-11 fragment for M2 slice e from the round-10 fragment (context) and this round's evidence files."""
import json, re, sys
from datetime import datetime, UTC
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "ledgers/M2/scripts/M2-e-r11"
PREV = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-M2-e.round10.json").read_text(encoding="utf-8"))
prev_rows = {r["id"]: r for r in PREV["rows"]}

CARRY = "Carried from round 10 (byte-identical since the previous pin 47a36d8c: {files}):"
CARRY_FILES = {
    "proj": "course/modules/M/M2/project.html, course/modules/M/M2/grader/*, tests/labs/M2/*",
    "lesson": "the lesson page(s) named in the row and the cards.json entries of those lessons, which are unchanged",
    "hub": "course/modules/M/M2/index.html, plans/M2-build-plan.md, curriculum M2 entry",
    "tools": "tools/*, notation/*, grader/* and tests/labs/M2/*",
}

def carry(row_id, files_key, extra=""):
    prev = prev_rows[row_id]
    ev = CARRY.format(files=CARRY_FILES[files_key]) + " " + prev["evidence"] + (" " + extra if extra else "")
    return {"id": row_id, "check": prev["check"], "location": prev["location"], "status": "PASS", "evidence": ev}

def row(row_id, check, location, status, evidence):
    r = {"id": row_id, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = "see evidence"
    return r

R = {}  # re-verified rows, round 11
R["e2-check-pages"] = row("e2-check-pages", "2.9 structure", "course/modules/M/M2/", "PASS",
    "`.venv/bin/python tools/check_pages.py --unit M2` -> 'check_pages M2: PASS', exit 0 (ledgers/M2/scripts/M2-e-r11/check_pages_M2.out). "
    "This includes the banned-string scan and the cards.json checks (unique ids, lesson exists, grade valid, cited keys known) on the 394-card file.")
R["e2-check-dag"] = row("e2-check-dag", "2.9 DAG", "course/modules/M/M2/", "PASS",
    "`tools/check_dag.py --unit M2` -> 'check_dag M2: PASS', exit 0 (ledgers/M2/scripts/M2-e-r11/check_dag_M2.out).")
R["e2-check-projects"] = row("e2-check-projects", "2.6 spec, ladder, hours, rubric", "course/modules/M/M2/project.html", "PASS",
    "`tools/check_projects.py --unit M2` -> 'check_projects M2: PASS', exit 0 (ledgers/M2/scripts/M2-e-r11/check_projects_M2.out). project.html is byte-identical to the round-10 pin.")
R["e2-run-graders"] = row("e2-run-graders", "2.6 autograder 1", "course/modules/M/M2/grader/reference.py", "PASS",
    "`tools/run_graders.py --unit M2 --seeds 0-49` -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 (ledgers/M2/scripts/M2-e-r11/run_graders_M2.out).")
R["e2-run-labs-project"] = row("e2-run-labs-project", "2.5 labs", "project.html lab-M2-project-1..3", "PASS",
    "`tools/run_labs.py --unit M2 --page project` -> 'run_labs M2: PASS (3/3)', exit 0 (ledgers/M2/scripts/M2-e-r11/run_labs_M2_project.out); "
    "full unit `tools/run_labs.py --unit M2` -> 'PASS (27/27)', exit 0 (run_labs_M2.out).")
R["e2-lab-page-code-equals-twin"] = row("e2-lab-page-code-equals-twin", "2.5 labs: page code equals twin",
    "project.html lab blocks 1-3; tests/labs/M2/lab-M2-project-1..3.py", "PASS",
    "Ran ledgers/M2/scripts/M2-e-r10/page_code_vs_twin_r10.py on this checkout (output ledgers/M2/scripts/M2-e-r11/page_code_vs_twin_r11.out): "
    "lab-M2-project-1 (49 lines) and -3 (79 lines) identical after strip; lab-M2-project-2 (68 lines) differs only in the Rung 2 blanks "
    "`return Dual(self.value * o.value, ___)` and `return ___` in second_difference, which is the completion convention (ruling 11).")
R["e2-lab-twin-clean-and-expected"] = row("e2-lab-twin-clean-and-expected", "2.5 labs: twin under python -I -W error; expected block equals output",
    "tests/labs/M2/lab-M2-*.py (27 twins)", "PASS",
    "Each of the 27 twins run alone as `python -I -W error <absolute path>` from a temporary directory: 27 exit 0 (ledgers/M2/scripts/M2-e-r11/twins_alone_r11.out). "
    "`run_labs.py --unit M2` PASS 27/27, so each expected block equals its printed output (run_labs_M2.out).")
R["e2-page-smoke-project"] = row("e2-page-smoke-project", "2.9 page_smoke", "course/modules/M/M2/project.html", "PASS",
    "`tools/page_smoke.py --unit M2 --pages project` -> 'page_smoke modules/M/M2/project.html: PASS' and 'page_smoke M2: PASS'; in-browser grader 'All 89 tests pass' (ledgers/M2/scripts/M2-e-r11/page_smoke_project.out).")
R["e2-pytest-local-and-count"] = row("e2-pytest-local-and-count", "2.6 autograder 5 and page test count", "course/modules/M/M2/grader/test_project.py", "PASS",
    "The grader run in a scratch workspace (test_project.py, instance.py, reference.py as sensitivity_engine.py): `pytest --collect-only` -> '89 tests collected' (pytest_collect_M2.out); "
    "QF_SEED=0,1,2,3 -> '89 passed' each (pytest_M2_seed0..3.out). project.html line 211 says 'runs 89 tests', equal to the collected count.")
R["e2-ruff"] = row("e2-ruff", "gate: ruff", "tests/labs/M2, course/modules/M/M2/grader", "PASS",
    "`ruff check tests/labs/M2 course/modules/M/M2/grader` -> 'All checks passed!'; `ruff format --check tests/labs/M2` -> '27 files already formatted' (ledgers/M2/scripts/M2-e-r11/ruff_check_M2.out).")
R["e2-mypy-labs"] = row("e2-mypy-labs", "gate: mypy strict on labs", "tests/labs/M2", "PASS",
    "`mypy tests/labs/M2 --no-incremental` -> 'Success: no issues found in 27 source files', exit 0 (ledgers/M2/scripts/M2-e-r11/mypy_labs_M2.out).")
R["e2-mypy-grader-command"] = row("e2-mypy-grader-command", "plan section 8 grader mypy command", "course/modules/M/M2/grader/test_project.py", "PASS",
    "Plan section 8 scratch-workspace command: `mypy --strict --no-incremental test_project.py instance.py sensitivity_engine.py` -> 'Success: no issues found in 3 source files' (ledgers/M2/scripts/M2-e-r11/mypy_grader_strict_M2.out).")
R["e2-pytest-labs-tests"] = row("e2-pytest-labs-tests", "gate: pytest for lab tests", "tests/test_labs.py, tests/test_run_labs.py -k M2", "PASS",
    "`pytest tests/test_labs.py tests/test_run_labs.py -k M2` -> all passed, exit 0 (ledgers/M2/scripts/M2-e-r11/pytest_labs_M2.out).")
R["e2-verify-refs"] = row("e2-verify-refs", "2.1 citations: keys cited by project.html", "references/references.json; course/modules/M/M2/project.html", "PASS",
    "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' (verify_refs_offline.out). "
    "`tools/verify_refs.py --unit M2` (live, plain HTTP to Crossref) -> 'live re-verification of M2: 2 of 560 entries, 0 problems', exit 0 (verify_refs_M2_live.out). "
    "references.json changed only in BK4 and LX1 used_by lines (delta_since_47a36d8c_r11.out); no M2 key changed.")
R["e2-project-lab1-numbers"] = row("e2-project-lab1-numbers", "numbers in prose vs unrounded values (Lab 1)",
    "course/modules/M/M2/project.html Lab 1 hypothesis and interpretation", "PASS",
    "Independent recomputation with the page's formulas (ledgers/M2/scripts/M2-e-r11/lab_prose_numbers_r11.py, output lab_prose_numbers_r11.out): unrounded price 1081108.9578 (rounds to 1081109), dP/dy -8514667.3953, d2P/dy2 83766485.1192, duration 7.875864; "
    "the central difference at step 1e-5 differs by 1.557e-2, a relative 1.83e-9, as the page states (about 1.8e-9). Every quoted Lab 1 figure matches the printed run.")
R["e2-project-lab3-numbers"] = row("e2-project-lab3-numbers", "numbers in prose vs unrounded values (Lab 3)",
    "course/modules/M/M2/project.html Lab 3 hypothesis and interpretation", "PASS",
    "Recomputed (lab_prose_numbers_r11.out): unrounded price 2721581.2909, rounds to 2721581; dP/dy -23407826.805475 (page prints the same). "
    "The printed central-error value 7.111207e-04 at step 1e-6 is the run's own output (run_labs confirms the expected block); my independent evaluation order gives 1.41e-3, so this figure is round-off-dominated and is quoted only as printed, which the page says ('printed as').")
R["e2-project-notation"] = row("e2-project-notation", "notation registry: no symbol reused with another meaning",
    "project.html math; cards.json; L22-L24", "PASS",
    "notation/notation.json (8 registered symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) against project.html math and card text, scanned by notation_and_refs_scan_r11.py (output notation_and_refs_scan_r11.out): "
    "0 hits for every registered symbol in the project math and in the card text. Project math uses only C, F, H, P, and lower-case letters, none registered. "
    "Plain-text Q (18 card hits) is a partition or a difference quotient and never the registered \\mathbb{Q}; no \\mathbb{R} appears (the \\R macro is used, ruling 1).")
R["e2-banned-phrases"] = row("e2-banned-phrases", "banned phrases", "project.html; cards.json; grader/*.py; labs; L22, L23, L24", "PASS",
    "banned_and_process_scan_r11.py over cards.json, project.html text, grader/test_project.py and grader/instance.py: BUILDER_RULES 1.3 strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, ellipsis) and 1.4 filler (it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, roughly, historically): 0 BANNED hits (banned_and_process_scan_r11.out).")
R["e2-project-process-words"] = row("e2-project-process-words", "no process words in learner text", "project.html; cards.json; grader/test_project.py messages", "PASS",
    "Same scan (banned_and_process_scan_r11.out) for verifier, verification, builder, fragment, reviewer, revised, corrected, fixed in, ledger, updated: 0 hits. The only matches of 'round ' are mathematical (round to, round-half-even, an interval around).")
R["e2-grader-reference"] = row("e2-grader-reference", "reference solution passes the suite", "course/modules/M/M2/grader/reference.py", "PASS",
    "run_graders on reference.py: 50/50 seeds (run_graders_M2.out); the collected suite on the reference passes 89/89 on seeds 0-3 (pytest_M2_seed0..3.out).")
R["e2-grader-alternatives"] = row("e2-grader-alternatives", "five alternative correct implementations pass", "ledgers/M2/scripts/M2-e-r11/run_alternatives_r11.py", "PASS",
    "run_alternatives_r11.py ran all 24 alternative implementations (round 3: 5, rounds 5-9: 12, round 10: 5, round 11: 2) as sensitivity_engine.py in scratch copies against test_project.py: 24 of 24 pass 50/50 seeds 0-49 (alternatives_r11.out).")
R["e2-mutants-existing"] = row("e2-mutants-existing", "every existing mutant killed", "ledgers/M2/mutants/", "PASS",
    "`tools/mutate_graders.py --unit M2 --seeds 0-9` -> 'mutate_graders M2: PASS (175/175 killed)', exit 0 (ledgers/M2/scripts/M2-e-r11/mutate_graders_M2.out). Covers the 171 existing mutants and the 4 new w11e mutants.")
R["e2-cards-count"] = row("e2-cards-count", "cards: count and grades", "course/modules/M/M2/cards.json", "PASS",
    "cards.json has 394 cards (round-10 pin: 397). Removed M2-c408 (L08), M2-c411 (L10), M2-c412 (L08); none added (card_delta_r11.py output in ledgers/M2/scripts/M2-e-r11/). Gaps in ids are allowed (ruling 2). "
    "No card count is quoted in index.html, project.html or the lessons (grep of 'N cards' returned nothing).")
R["e2-cards-dup-ids-fronts"] = row("e2-cards-dup-ids-fronts", "cards: duplicate scan (ids and fronts)", "course/modules/M/M2/cards.json", "PASS",
    "card_dupes_r11.py (card_dupes_r11.out): no duplicate ids, no exact duplicate fronts, no exact duplicate backs. 61 pairs at token-Jaccard >= 0.45 were read; they ask different results "
    "(e.g. c363/c364 Propositions 4.2/4.3; c188/c189 forward/central error; c380, c399, c400, c401, c409 'which derivatives does Assumption 1 of Lesson N assume', each for its own lesson's assumption). "
    "The semantic duplicates found in earlier rounds (c412 Rolle = c065; c411 MVT = c066; c408 EVT-not-proved = c064 in content) are gone.")
R["e2-cards-numbers"] = row("e2-cards-numbers", "cards: every number appears in the card's lesson", "course/modules/M/M2/cards.json", "PASS",
    "card_numbers_r11.py (card_numbers_r11.out): every number in every card's front and back appears in that card's lesson page text. 394 cards checked, 0 missing.")
R["e2-cards-locators"] = row("e2-cards-locators", "cards: lesson page exists for every card", "course/modules/M/M2/cards.json", "PASS",
    "check_pages M2 PASS (check_pages_M2.out) and card_numbers_r11.py, which reads course/modules/M/M2/L01..L24.html for each card's lesson field without error.")
R["e2-cards-grades"] = row("e2-cards-grades", "cards: grades and bases", "course/modules/M/M2/cards.json", "PASS",
    "Grades over 394 cards: T 236, C 77, no grade key 81 (definitions and structural cards, as in round 10). Every C card has a basis key (77 of 77). Recomputed in the round-11 scripts.")
R["e2-cards-L01"] = row("e2-cards-L01", "cards L01", "course/modules/M/M2/cards.json (L01: 16 cards); L01.html", "PASS",
    "Re-read all 16 L01 cards. The changed card M2-c390 now reads 'The limit of (a_n) is fixed by its tail, so the first M - 1 terms do not affect it (Section 3).' L01 Section 3 says 'Proposition 3.1 says that the early terms cannot change a limit. The limit of (a_n) is fixed by its tail, and the first terms are free' (lesson_text_r11.py on L01.html). "
    "Card M2-c006 numbers recomputed: at n = 999 the error is 1/1000 = 1.000000e-03 (not below 0.001); at n = 1000 it is 1/1001 = 9.990010e-04. Precision note, not a fail: the card's 'limit' presumes a limit exists, as the lesson's wording does; the card is ungraded.")
R["e2-cards-L08"] = row("e2-cards-L08", "cards L08", "course/modules/M/M2/cards.json (L08: 19 cards); L08.html", "PASS",
    "Re-read all 19 remaining L08 cards (c097-c114, c397). Removed c408 and c412 (round-10 FAIL resolved). Checked against L08 text (lesson_text_r11.py): Assumption 1.1 is the extreme value theorem, assumed as Assumption 2.1 of Lesson 6; Theorem 2.1 hypotheses (n >= 0, x0 and x in an open interval I with derivatives up to n+1) match c100. "
    "Numbers recomputed: c102 xi = 1 - (1 - x)^(1/(n+2)) lies in (0, x); c103/c104 bound ratio 2^(n+2)(1-x), in [2^(n+1), 2^(n+2)); c107 R_1(0.9) = 8.1 and xi = 0.535841; c111 bound equals 2 at x = 1/2 and the remainder (1/2)^n.")
R["e2-cards-L10"] = row("e2-cards-L10", "cards L10", "course/modules/M/M2/cards.json (L10: 15 cards); L10.html Theorem 1.2, Proof of Theorem 2.1, Proposition 4.1", "PASS",
    "Re-read all 15 L10 cards after removing c411 (a restatement of M2-c066, the mean value theorem in L06). Numbers recomputed exactly (l10_cards_recompute_r11.py, l10_cards_recompute_r11.out): "
    "c139 U_n - L_n = 3/n and at n = 256 L = -1.00585175, U = -0.99413300, with -1 between; c140 U_n - L_n = 3/(4n), brackets 1/2; c141 central difference 0.59171598 against f(0.3) = 0.5917159763; c136 = 1/2; c138 = -1. "
    "Cross-references checked in the text: 'Section 5' is the lesson's 'Where the canon breaks', Remark 1.3 and Misconception 1 exist, Example 2.2 and 3.2 exist, and Lesson 9 Definition 1.3 defines the integral used by c135 and c137.")
R["e10-cards-c412-duplicates-c065"] = row("e10-cards-c412-duplicates-c065", "cards: no duplicate cards (semantic)", "course/modules/M/M2/cards.json, M2-c412 (L08) and M2-c065 (L06)", "PASS",
    "M2-c412 is deleted (card_dupes_r11.out: no card states Rolle's theorem twice with the same hypotheses; M2-c065 (L06) and M2-c066 (L06, MVT) each remain once). "
    "A grep of the working tree finds no reference to M2-c412, M2-c408 or M2-c411 (notation_and_refs_scan_r11.out).")
R["e3-cards-whole-set-mechanical"] = row("e3-cards-whole-set-mechanical", "cards: whole-set mechanical checks", "course/modules/M/M2/cards.json", "PASS",
    "card_numbers_r11.out (0 missing numbers over 394 cards), card_dupes_r11.out (no exact duplicates), card_delta_r11.py (delta since 47a36d8c: M2-c390 changed, c408/c411/c412 removed), check_pages (PASS). Per-lesson counts: L01 16, L02 13, L03 14, L04 11, L05 13, L06 14, L07 23, L08 19, L09 18, L10 15, L11 16, L12 17, L13 23, L14 20, L15 20, L16 11, L17 15, L18 16, L19 13, L20 14, L21 16, L22 15, L23 24, L24 18 (sum 394).")
R["e6-card-M2-c408-c409"] = row("e6-card-M2-c408-c409", "cards: new cards", "course/modules/M/M2/cards.json; M2-c409 (L16)", "PASS",
    "M2-c408 (L08) is removed in this pin; no file refers to it (notation_and_refs_scan_r11.out). M2-c409 (L16, 'Which derivative does Assumption 1 of Lesson 16 assume, and is it proved?') is unchanged and matches L16's 'the page assumes it and does not prove it' (carried wording).")
R["e6-instances-50"] = row("e6-instances-50", "instances over seeds 0-49", "course/modules/M/M2/grader/instance.py", "PASS",
    "run_graders --seeds 0-49 runs the instance validity and determinism checks on seeds 0-49 and reports PASS (run_graders_M2.out). instance.py is byte-identical to the round-10 pin.")
R["e5-alternatives"] = row("e5-alternatives", "alternative correct implementations pass", "ledgers/M2/scripts/M2-e-r11/alts_r11/*.py and the earlier alts directories", "PASS",
    "alternatives_r11.out: 24 of 24 alternatives pass 50/50 seeds (see e2-grader-alternatives).")
R["e5-twins-alone"] = row("e5-twins-alone", "lab twins alone under python -I -W error", "tests/labs/M2/*.py (27)", "PASS",
    "twins_alone_r11.out: 27 of 27 exit 0 when run alone under python -I -W error.")
R["e5-fragment-gate-set"] = row("e5-fragment-gate-set", "gate set run this round", "repo gates for M2", "PASS",
    "Re-run this round: check_pages, check_dag, check_projects (PASS); run_labs M2 27/27 and project 3/3; run_graders 50/50; page_smoke project PASS; pytest 89 passed on seeds 0-3; pytest labs PASS; ruff and mypy (labs and grader strict) PASS; verify_refs offline and live PASS; build_site.py --check 'site data current: 6 outputs' (build_site_check.out); mutate_graders 175/175.")
R["e5-mutants-new-r5"] = row("e5-mutants-new-r5", "round-5 new mutants killed", "ledgers/M2/mutants/", "PASS",
    "The round-5 mutants (r5_01..r5_04) are in ledgers/M2/mutants/ and are killed in the 175/175 run (mutate_graders_M2.out).")
R["e6-mutants-new-v6e"] = row("e6-mutants-new-v6e", "three or more new student-error mutants killed", "ledgers/M2/mutants/v6e_01..v6e_04", "PASS",
    "v6e_01..04 are killed in the 175/175 run (mutate_graders_M2.out).")
R["e7-round7-mutants-v7e"] = row("e7-round7-mutants-v7e", "new student-error mutants (at least 3)", "ledgers/M2/mutants/v7e_01..v7e_04", "PASS",
    "v7e_01..04 are killed in the 175/175 run (mutate_graders_M2.out).")
R["e7-alternatives-new"] = row("e7-alternatives-new", "alternatives: correct engines not over-constrained", "ledgers/M2/scripts/M2-e-r7/alts_new and M2-e-r9/alts_r9", "PASS",
    "alternatives_r11.out: alt_r7_a and alt_r7_b, alt_r9_a..c all pass 50/50 seeds.")
R["e7-twins-27-alone"] = row("e7-twins-27-alone", "twins alone under python -I -W error", "tests/labs/M2/*.py (27)", "PASS",
    "twins_alone_r11.out: 27 of 27 exit 0.")
R["e9-delta-read"] = row("e9-delta-read", "full read of the delta in the slice", "course/modules/M/M2/cards.json, grader/test_project.py, project.html", "PASS",
    "Delta since the previous pin 47a36d8c, read in full (delta_since_47a36d8c_r11.out and card_delta_r11.py): course/modules/M/M2/cards.json (M2-c390 back text changed; M2-c408, M2-c411, M2-c412 removed). "
    "Byte-identical since 47a36d8c: course/modules/M/M2/project.html, grader/ (all three files), tests/labs/M2/, all L01-L24 pages, index.html, plans/M2-build-plan.md, notation/, tools/. Other delta: references/references.json (BK4 and LX1 used_by only, no M2 key), curriculum/02-economics-finance-core.yaml and curriculum/curriculum.json (one brief line of a non-M2 unit), and tests/labs of units other than M2.")
R["e9-mutants-new-v9e"] = row("e9-mutants-new-v9e", "new student-error grader mutants (at least 3)", "ledgers/M2/mutants/v9e_01..v9e_05", "PASS",
    "v9e_01..05 are killed in the 175/175 run (mutate_graders_M2.out).")
R["e9-alternatives-r9"] = row("e9-alternatives-r9", "new alternative correct implementations (over-constraint check)", "ledgers/M2/scripts/M2-e-r9/alts_r9/", "PASS",
    "alternatives_r11.out: alt_r9_a, alt_r9_b, alt_r9_c each 50/50 seeds.")
R["e10-alternatives-r10"] = row("e10-alternatives-r10", "five new alternative correct implementations of different styles pass", "ledgers/M2/scripts/M2-e-r10/alts_r10/", "PASS",
    "alternatives_r11.out: alt1..alt5 of round 10 each 50/50 seeds (run again this round).")
R["e10-mutants-r10-new"] = row("e10-mutants-r10-new", "five new student-error mutants of my own, killed", "ledgers/M2/mutants/w10e_01..w10e_05", "PASS",
    "w10e_01..05 are killed in the 175/175 run (mutate_graders_M2.out).")
R["e10-cards-changed-c027-c047-c177-c352"] = row("e10-cards-changed-c027-c047-c177-c352", "changed cards re-read against the current lesson text",
    "course/modules/M/M2/cards.json M2-c027 (L03), M2-c047 (L04), M2-c177 (L12), M2-c352 (L23)", "PASS",
    carry("e10-cards-changed-c027-c047-c177-c352", "lesson").get("evidence") and "")
R["e10-cards-changed-c027-c047-c177-c352"]["evidence"] = CARRY.format(files="the four cards and their lesson pages L03, L04, L12, L23 are unchanged") + " " + prev_rows["e10-cards-changed-c027-c047-c177-c352"]["evidence"]

# carried rows (subject byte-identical since 47a36d8c)
CARRY_IDS = {
    "e2-hours-arithmetic": "hub",
    "e2-project-lab2-numbers": "proj",
    "e2-project-exemplar-numbers": "proj",
    "e2-project-spec-signatures": "proj",
    "e2-project-tolerances-conventions": "proj",
    "e2-project-rubric-calibration": "proj",
    "e2-project-rubric-observable": "proj",
    "e2-project-adversarial-atlas-studio": "proj",
    "e2-project-data-simulated": "proj",
    "e2-scope-words": "proj",
    "e2-grader-instance-claims": "proj",
    "e2-grader-messages": "proj",
    "e2-grader-valueerror-scope": "proj",
    "e2-grader-no-print": "proj",
    "e2-grader-instances": "proj",
    "e2-mutants-written": "tools",
    "e2-mut-v2-01": "tools",
    "e2-mut-v2-02": "tools",
    "e2-mut-v2-03": "tools",
    "e4-mutants-new-r4": "tools",
    "e6-card-M2-c349": "lesson",
    "e6-card-M2-c350": "lesson",
    "e6-card-M2-c363-c365": "lesson",
    "e6-card-M2-c404-c405": "lesson",
    "e6-L24-E3-unrounded-difference": "lesson",
    "e7-L22-L24-lesson-numbers": "lesson",
    "e8-ad-float-return-contract": "proj",
    "e9-ad-int-zero-at-origin": "proj",
    "e9-fd-int-zero-at-origin": "proj",
    "e10-cards-c413-new-L15": "lesson",
    "e10-sin-ratio-range": "proj",
    "e10-hours-estimate-under-ruling": "hub",
    "e10-spec-clarifying-questions": "proj",
    "e10-links-anchors": "proj",
    "e2-cards-L02": "lesson", "e2-cards-L03": "lesson", "e2-cards-L04": "lesson", "e2-cards-L05": "lesson",
    "e2-cards-L06": "lesson", "e2-cards-L07": "lesson", "e2-cards-L09": "lesson", "e2-cards-L11": "lesson",
    "e2-cards-L12": "lesson", "e2-cards-L13": "lesson", "e2-cards-L14": "lesson", "e2-cards-L15": "lesson",
    "e2-cards-L16": "lesson", "e2-cards-L17": "lesson", "e2-cards-L18": "lesson", "e2-cards-L19": "lesson",
    "e2-cards-L20": "lesson", "e2-cards-L21": "lesson", "e2-cards-L22": "lesson", "e2-cards-L23": "lesson",
    "e2-cards-L24": "lesson", "e2-cards-L19-L21-untouched-proof": "lesson",
}
CARRY_NOTES = {
    "e2-cards-L22": " Note: L22 has 15 cards (c323-c332, c334-c337, c404); id c333 is absent, which ruling 2 allows.",
    "e2-cards-L23": " Re-checked this round: L23 has 24 cards, matching the count above; c341 and c382 numbers recomputed (108110.895779 and 108111).",
    "e2-cards-L19-L21-untouched-proof": "",
}
rows = []
for pid, prow in prev_rows.items():
    if pid in R:
        rows.append(R[pid])
    elif pid in CARRY_IDS:
        r = carry(pid, CARRY_IDS[pid], CARRY_NOTES.get(pid, "").strip())
        if pid == "e2-cards-L19-L21-untouched-proof":
            r["evidence"] = r["evidence"]
        rows.append(r)
    else:
        raise SystemExit(f"row {pid} not classified")

# rows that were FAIL in round 10 and are re-verified now are in R (e2-cards-L08 and e10-cards-c412-duplicates-c065)
assert all(r["status"] == "PASS" for r in rows if r["id"] in ("e2-cards-L08", "e10-cards-c412-duplicates-c065"))

# new rows of round 11
rows.append(row("e11-cards-c390-changed", "cards: changed card re-read (hypotheses and lesson agreement)",
    "course/modules/M/M2/cards.json M2-c390 (L01); L01.html Section 3", "PASS",
    "Old back: 'Changing the first M - 1 terms does not change the tail's limit (Section 3).' New back: 'The limit of (a_n) is fixed by its tail, so the first M - 1 terms do not affect it (Section 3).' "
    "The new back agrees with L01 Section 3 (Proposition 3.1 text, lesson_text_r11.py). Precision note (not a fail): both wordings presuppose that the limit exists, as Proposition 3.1's hypothesis a_n -> L does; the card is ungraded and mirrors the lesson sentence."))
rows.append(row("e11-cards-deleted-c408-c411", "cards: removed cards justified (no coverage loss of a graded claim)",
    "course/modules/M/M2/cards.json M2-c408 (L08), M2-c411 (L10) removed", "PASS",
    "M2-c411 restated M2-c066 (L06 mean value theorem, same hypotheses and conclusion), so it was a duplicate. M2-c408 answered 'No, the extreme value theorem is assumed, not proved' for Assumption 1.1 of L08, the same answer as M2-c064 (L06); it was a duplicate in content. "
    "After the removals, the statement of Rolle's theorem is carried by M2-c065 (L06) and M2-c099 (L08) applies it in the proof of Theorem 2.1; the mean value theorem statement is carried by M2-c066 (L06) and M2-c134 (L10) applies it. "
    "So the Lesson 8 and Lesson 10 restatements lost only duplicates, and the results are still covered by their L06 cards. Unchanged cards c064, c065, c066, c099, c100 and c134 were read and are correct."))
rows.append(row("e11-mutants-new-w11e", "new student-error mutants (at least 3), killed",
    "ledgers/M2/mutants/w11e_01..w11e_04", "PASS",
    "Four new student-error mutants, each a full module with a docstring first line naming the student error: w11e_01 forward quotient by floor division (truncates the derivative); w11e_02 step read with int(), refusing steps below 1; w11e_03 duration divides by the price in dollars; w11e_04 yield check compares basis points with -1 (refuses any yield below -0.01 percent, where the page requires a yield above -1 to be accepted). All four killed in the 175/175 run (mutate_graders_M2.out)."))
rows.append(row("e11-alternatives-new-r11", "alternative correct implementations of new styles pass seeds 0-49",
    "ledgers/M2/scripts/M2-e-r11/alts_r11/alt6_*.py, alt7_*.py", "PASS",
    "alt6: Hessian by the page's own formula with a shift helper, bond price and sensitivities by iterative discount powers; alt7: price in 400-digit Decimal rounded half to even, derivatives in float. Both 50/50 seeds (alternatives_r11.out). "
    "Two of my own early attempts failed for reasons in my implementations, not in the grader, and were corrected: an AD-based Hessian (test function uses math.sin, which a dual number cannot take; the page defines hessian_fd by finite differences) and a 60-digit Decimal context (a yield just above -1 makes the price about 10**120 cents). The grader is not over-constrained by either."))
rows.append(row("e11-build-site-check", "site data and program map current", "tools/build_site.py --check", "PASS",
    "`tools/build_site.py --check` -> 'site data current: 6 outputs', exit 0 (ledgers/M2/scripts/M2-e-r11/build_site_check.out)."))
rows.append(row("e11-curriculum-regeneration-out-of-slice", "generated curriculum outputs (not in slice e)",
    "curriculum/curriculum.json; CURRICULUM.md", "PASS",
    "Not re-generated: the delta in curriculum/ is one brief line of a non-M2 unit in curriculum/02-economics-finance-core.yaml, which is outside slice e. The M2 entry and the M2 hours are unchanged (the hub index.html and plans/M2-build-plan.md are byte-identical since 47a36d8c)."))

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert set(prev_rows) <= set(ids), "a previous row id was dropped"

mutants = []
for line in (OUT / "mutate_graders_M2.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+): (.*) -> (\S+)", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 175, len(mutants)

notes = [
    "Round 11, slice e (project.html, grader/*, project labs, all M2 cards.json, mutants, alternatives), pin ccaeeaf4 (checkout detached), previous pin 47a36d8c (round 10). Delta read in full: see e9-delta-read.",
    "Round-10 FAIL e2-cards-L08 and e10-cards-c412-duplicates-c065 are resolved: M2-c412 is deleted and no duplicate of Rolle's theorem remains. Two other cards were deleted in the same pin (M2-c408, M2-c411), both justified in e11-cards-deleted-c408-c411. The card count is 394.",
    "Only cards.json changed in the M2 slice, so every other subject is byte-identical to 47a36d8c and its round-10 PASS is carried with the prefix 'Carried from round 10'. Every command gate was re-run this round.",
    "Mutants: 175 of 175 killed (171 existing, 4 new w11e). No survivor. No equivalent mutants are needed (none moved to ledgers/M2/equivalent/).",
    "Alternatives: 24 of 24 correct implementations pass 50/50 seeds 0-49 (the round-3 files need a reference_core.py copy of reference.py, which the runner provides).",
    "Lab 2 (project.html) shows blanks and its twin the full solution: the Rung 2 convention, ruling 11, not a defect.",
    "Precision observations, not fails: c390 and the L01 Section 3 sentence presuppose that the limit exists (Proposition 3.1 hypothesis a_n -> L). L22 has 15 cards (c333 absent, allowed by ruling 2).",
    "Housekeeping: ledgers/M2/scripts/M2-e-r11/ already held tracked files from commit ff388424 (an earlier campaign's round 11 for M2). I wrote make_mutants_r11.py there, overwrote that tracked file, and restored it with git checkout. My copy of the script is make_mutants_v11e.py. No other tracked file was modified.",
    "The checkout's ledgers/M2/M2-e.json (tracked, 54 rows) is replaced by this round's fragment, as the task specifies.",
    "Not checked: a line-by-line read of all 24 lesson pages (about 1 MB) was not done this round, because no lesson changed except through the card set; the lessons were read by script and for every changed or deleted card. The cards of lessons L02-L07, L09, L11-L24 are carried from round 10 because their cards and pages are byte-identical.",
    "Not checked: verify_refs live over all 560 entries (only the M2 entries, 2 of 560, were re-resolved live). The live Crossref run is the CI job's.",
]

fragment = {
    "unit": "M2",
    "slice": "e",
    "round": 11,
    "verifier": "Haiku 5.5 independent verifier (round 11, slice e)",
    "pin": "ccaeeaf4" + "",
    "base": PREV["base"],
    "checkout": str(ROOT),
    "scratch": "/var/folders/.../m2e_r11_* (alternative runs, scratch grader workspaces); every backing script is in ledgers/M2/scripts/M2-e-r11/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": "",
}
fragment["pin"] = __import__("subprocess").run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
fragment["verdict"] = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
n = len(rows)
fragment["summary"] = f"Slice e round 11: {fragment['verdict']}. {n} rows, {sum(r['status']=='PASS' for r in rows)} PASS. Mutants {len(mutants)}/{len(mutants)} killed. Cards: 394 (c408, c411, c412 removed; c390 changed)."
out = ROOT / "ledgers/M2/M2-e.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", n, "verdict", fragment["verdict"], "mutants", len(mutants))
