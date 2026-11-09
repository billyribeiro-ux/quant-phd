"""Build ledgers/M3/M3-d.json for the M3 slice d closing delta (round 1, pin 2a805c83, base 95f3f8cb).

Reads the base fragment (read-only), the standing-mutant parse (closing_mutants.py output) and writes the fragment.
Every base row id is kept. Rows re-verified this round carry fresh evidence; every other base PASS row is carried
with the carry prefix; the one base FAIL (cards-L08) is re-verified and reads PASS. New rows are appended.
"""
import datetime
import json
import re
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyG1-M3-d"
OUT = f"{ROOT}/ledgers/M3/scripts/M3-d-r1/out"
BASE = "/Users/billyribeiro/.fanout/frags/F2-M3-d.round1.json"
base = json.load(open(BASE, encoding="utf-8"))
mut_entries = json.load(open("/private/tmp/verifyG1-M3-d-txt/mutants_entries.json", encoding="utf-8"))
mut_by_id = {m["id"]: m for m in mut_entries}

CARRY_PREFIX = "Carried from round 1 ({loc} byte-identical since the previous pin 95f3f8cb; base fragment F2-M3-d.round1): "
CARRY_CHAIN = re.compile(r"^(Carried from round \d+ \((?:[^()]|\([^()]*\))*\): )+")


def killed_names(prefixes):
    """Return 'id: killed_by' pairs for mutants whose id starts with any regex prefix."""
    out = []
    for m in mut_entries:
        if any(re.match(p, m["id"]) for p in prefixes):
            out.append(f"{m['id']} KILLED by {m['killed_by']}")
    return out


def group_row(rid, check, location, prefixes, extra=""):
    names = killed_names(prefixes)
    ev = "; ".join(names) + f" (all in out/closing_mutate_M3_seeds0-9.out, EXIT 0, 184/184). {extra}".strip()
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": ev}


FRESH = {}
FRESH["gate-check-pages"] = ("2.9 pages", "tools/check_pages.py --unit M3",
    "check_pages M3: PASS EXIT 0 (out/closing_check_pages_M3.out), run at 2a805c83; covers the changed L07, L08, L09 pages and cards.json.")
FRESH["gate-check-dag"] = ("2.9 DAG", "tools/check_dag.py --unit M3",
    "check_dag M3: PASS EXIT 0 (out/closing_check_dag_M3.out). L07 now cites Lesson 4 (a prerequisite already in its closure).")
FRESH["gate-check-projects"] = ("2.6 projects", "tools/check_projects.py --unit M3",
    "check_projects M3: PASS EXIT 0 (out/closing_check_projects_M3.out).")
FRESH["gate-run-labs"] = ("2.5 labs", "tools/run_labs.py --unit M3",
    "run_labs M3: PASS (12/12) EXIT 0 (out/closing_run_labs_M3.out): every page lab equals its twin and every expected block equals the twin output. "
    "Twins alone under python -I -W error, EXIT 0 with empty stderr: L01-L06 (out/closing_twin_L01..L06.out/.err), L07, L08, L09 (out/closing_twin_L07/L08/L09).")
FRESH["gate-run-graders"] = ("2.6 grader", "tools/run_graders.py --unit M3 --seeds 0-49",
    "run_graders M3 --seeds 0-49: PASS (reference 50/50 seeds, slowest 0.4 s) EXIT 0 (out/closing_run_graders_M3.out). Grader byte-identical since 95f3f8cb.")
FRESH["gate-page-smoke"] = ("2.9 smoke", "tools/page_smoke.py --unit M3 --pages L07 L08 L09",
    "page_smoke M3 --pages L07 L08 L09: PASS EXIT 0 in Chromium, labs lab-M3-L07-1, L08-1, L09-1 run in the browser (out/closing_page_smoke_L07_L08_L09.out). "
    "The project page is byte-identical since 95f3f8cb and is carried (base run out/page_smoke_project_delta.out).")
FRESH["gate-ruff"] = ("ruff", "ruff check tests/labs/M3 course/modules/M/M3/grader",
    "ruff check: All checks passed EXIT 0 (out/closing_ruff_check.out); ruff format --check: 16 files already formatted EXIT 0 (out/closing_ruff_format.out).")
FRESH["gate-mypy"] = ("mypy", "mypy --no-incremental",
    "mypy --no-incremental: Success: no issues found in 386 source files, EXIT 0 (out/closing_mypy.out).")
FRESH["gate-collect-only"] = ("2.6 grader count", "pytest --collect-only -q on the staged reference grader (/private/tmp/verifyG1-M3-d-ws/ref)",
    "198 tests collected, EXIT 0 (out/closing_collect_only_M3.out). The page statement of the count is project.html line 239 ('runs 198 tests'); "
    "the base row cited line 247, which is a clipping bullet, so the location is corrected here. Page count equals collected count.")
FRESH["gate-pytest-relevant"] = ("tooling pytest", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_docs_figures.py",
    "EXIT 0 (out/closing_pytest_relevant.out). The five test files are byte-identical since 95f3f8cb.")
FRESH["gate-mutate-m3"] = ("2.6 mutation", "tools/mutate_graders.py --unit M3 --seeds 0-9",
    "'mutate_graders M3: PASS (184/184 killed)' EXIT 0 (out/closing_mutate_M3_seeds0-9.out). 184 mutant files map one-to-one to 184 KILLED lines; 0 files without a KILLED line; 0 KILLED lines naming a collection failure.")
FRESH["gate-reference-starter"] = ("2.6 grader runs", "staged reference and starter copies, QF_SEED=0, -W error",
    "staged reference: 198 passed, EXIT 0 (out/closing_reference_seed0.out); staged starter: 197 failed, 1 passed, EXIT 1 (out/closing_starter_seed0.out).")
FRESH["gate-alternatives-seeds-0-49"] = ("2.6 alternatives", "sh ledgers/M3/scripts/M3-d-r1/run_alts_r1.sh: ledgers/M3/alternatives/*.py x seeds 0-49",
    "all 10 correct alternatives PASS seeds 0-49 against the current grader (out/closing_alts_seeds0-49.out).")
FRESH["alternatives-count-and-seeds"] = ("2.6 alternatives count", "ledgers/M3/alternatives/ (10 files)",
    "ls ledgers/M3/alternatives | wc -l = 10; all 10 PASS seeds 0-49 (out/closing_alts_seeds0-49.out).")
FRESH["mutants-existing-140"] = ("2.6 mutation (all existing)", "ledgers/M3/mutants/ (184 files)",
    "ledgers/M3/mutants/ holds 184 files; the standing run kills all 184 by named tests (out/closing_mutate_M3_seeds0-9.out; mapping by ledgers/M3/scripts/M3-d-r1/closing_mutants.py).")
FRESH["mutants-collection-only-kills"] = ("2.6 mutation (kill validity)", "ledgers/M3/mutants/r12d_m02, r12d_m03, r12d_m04",
    "; ".join(f"{i} KILLED by {mut_by_id[i]['killed_by']}" for i in
              ["r12d_m02_min_eigenvalue_first_jacobi_value", "r12d_m03_projection_keeps_negatives_down_to_minus_0p01",
               "r12d_m04_weights_scale_row_by_first_volatility"]) +
    " (out/closing_mutate_M3_seeds0-9.out). grep 'collection' over the run output: 0 hits; 0 collection-only kills.")
FRESH["mutants-v12d-new-student-errors"] = ("2.6 mutation (new this round)", "ledgers/M3/mutants/v12d_01..v12d_04",
    "; ".join(f"{m['id']} KILLED by {m['killed_by']}" for m in mut_entries if m["id"].startswith("v12d_"))
    + " (out/closing_mutate_M3_seeds0-9.out).")
FRESH["cards-L07"] = ("10-cards-lesson", "cards c115-c129, c168, c177, c194-c196, c209 vs L07.html (line 56 changed)",
    "L07.html changed at line 56 only: the inner product and norm are cited as 'Lesson 4, Definition 1.2', which is L04.html line 74 "
    "'(inner product, norm, orthogonality)'; the old 'Lesson 6' citation was wrong (L06.html line 56 says these terms are Lesson 4 Definition 1.2). "
    "No card cites the changed sentence. Cards read against the closing twin output (out/closing_twin_L07.out: all checks True; 1.3325 0.8488 -0.4120; 0.8951; rank 2 of 3) "
    "match c124, c125, c126 and c177. Card references resolve in L07 (out/closing_card_refs.out).")
FRESH["cards-L08"] = ("10 cards lesson (ruling 26 FAIL re-verified)", "cards-c145 and cards c138, c141, c174 in cards.json; L08.html line 312 (misconception) and the L08 Key results table lines 423-440",
    "Base FAIL (c145 graded T with 'depends on the data' and no witness) is closed. M3-c145 is now grade C with basis 'Theorem 2.1 and the Lab 1 panel (one SIMULATED case)' and no longer claims the level-like label depends on the data. "
    "Its back text was checked claim by claim: 'components are ordered by their eigenvalues (Definition 1.3)' matches L08.html line 82 (lambda_1 >= ... >= lambda_n); "
    "'Theorem 2.1 concerns the squared movement along each direction' matches line 100 (maximum of u^T M u over unit u); 'PC1 is level-like' and 'planted scale 8 bp per day on the level factor' match "
    "tests/labs/M3/lab-M3-L08-1.py lines 46-48 and 'best-matching component PC1, |cosine| 0.9994' in out/closing_twin_L08.out; 'the lab does not vary the planted scales' matches the fixed scales at lines 46-48. "
    "Grade C names the lab, as ruling 13 requires for a claim resting on SIMULATED data. c138 (T): Remark 2.4 (L08.html line 132) proves no single kappa gives M' = kappa M (M_jj > 0 by the e_j + t e_l argument; c^2 != c). "
    "c141 and c174 (C): 'a share of the total over all six eigenvalues' matches the twin's printed shares (lam / sum(lam)) and the key-results rows at lines 433-434. "
    "The card references Definition 1.3 and Theorem 2.1 resolve in L08. No other L08 card or key-results row depends on the changed text. The 'does not support' claim is a conservative C, not an over-grade.")
FRESH["cards-L09"] = ("10-cards-lesson", "cards c146-c167, c181-c183, c185, c202, c208 vs L09.html (lines 52, 200-201, 353 changed)",
    "L09.html changed in three places: line 52 (why-it-matters: 'Method 1, Section 4, built on Definition 3.1'; Method 1 at line 182 does compute B by Definition 3.1, so it is correct), "
    "lines 200-201 (the twin docstring, same text as tests/labs/M3/lab-M3-L09-1.py), and line 353 (Section 5: 'Rescaling can change the eigenvalues again (Problem R2)'; R2 at lines 466-471 gives diag(1,4) -> diag(1,1), eigenvalues {1,4} vs {1,1}, so the sentence is true). "
    "No card cites those sentences. Cards c161, c162, c163, c164, c175, c217 match the closing twin output (out/closing_twin_L09.out: 0.6400000000; 23 of 40; 23 of 23; 0.175527 and 0.163280; -0.800000 1.900000 1.900000). "
    "c182 (Method 2: 500 steps, tolerance 1e-12) matches the code. c167 is covered under its own row. Card references resolve in L09 (out/closing_card_refs.out).")
FRESH["cards-lab-numbers"] = ("10 cards lab numbers", "cards.json grade-C cards; tests/labs/M3 twins L07, L08, L09 (re-run this round); L01-L06 C cards carried",
    "Re-verified this round against the closing twin outputs: c141 (0.7587 to 0.9791), c174 (75.9, 18.1, 5.2), c145 (PC1 level-like, 8 bp per day) in out/closing_twin_L08.out; "
    "c139, c140 (0.9994, 0.9985, 0.9990) in out/closing_twin_L08.out; c124, c125, c126, c177 in out/closing_twin_L07.out; c161, c162, c163, c164, c175, c217 in out/closing_twin_L09.out. "
    "The L01-L06 C cards (every grade-C card whose lesson is L01-L06) are carried from round 1: their cards and twins are byte-identical and the twins re-ran EXIT 0 (out/closing_twin_L01..L06.out).")
FRESH["cards-structure"] = ("10 cards structure", "course/modules/M/M3/cards.json (210 records)",
    "210 records, 210 unique ids, 0 duplicate fronts, 0 duplicate backs (out/closing_cards_scan.out). Key sets: 50 without grade (keys back, front, id, lesson), 121 with grade only, 39 with grade and basis; "
    "every T card has no basis and every C card has one (grade/basis mismatch list empty). The base count 38 with basis is now 39 because c145 gained a basis; 122 T-only is now 121.")
FRESH["cards-id-sequence"] = ("10 cards ids", "course/modules/M/M3/cards.json",
    "ids M3-c001..M3-c219 in ascending file order (out/closing_scan.out: True); missing numbers 37, 101, 102, 148, 176, 191, 201, 204, 206 (same as base; gaps are not defects, ruling 2).")
FRESH["cards-numbers-cited"] = ("10 cards numbers cited", "cards.json front and back; L05, L07, L08, L09, L06 pages",
    "card_refs closing run (out/closing_card_refs.out) flags 9 references (c089, c127, c143, c168, c183, c195, c196, c203, c205). Each is a Definition, Example, Proposition, Theorem, Remark or Fact that exists in its own lesson, "
    "checked with grep counts on the lesson text (L05 Proposition 2.3 = 2; L07 Remark 1.4 = 5; L08 Theorem 2.1 = 4; L07 Theorem 2.2 = 4; L09 Proposition 3.3 = 4; L07 Theorem 1.2 = 4; L05 Theorem 2.2 = 5; L06 Fact 1.2 = 4). "
    "The flags come from the script's 'Lesson N' context heuristic, not from missing items. Changed c138, c145 cite Remark 2.4, Definition 1.3, Theorem 2.1, all present in L08.")
FRESH["cards-labels-cited"] = ("10 cards labels (ruling 13)", "cards.json grade and basis fields for c138, c141, c145, c174; L08 Key results table",
    "c141 (C) mirrors key-results row 'Multiplying one tenor's column by ten moves the first share ... ' (C, Lab 1 output); c174 (C) mirrors the combined C row for the three shares; "
    "c138 (T) mirrors no key-results row (Remark 2.4 is not in the table); c145 (C) mirrors no key-results row. No mismatch of grade and key-results row for the changed cards.")
FRESH["cards-duplicate-scan"] = ("10 cards duplicates", "course/modules/M/M3/cards.json (all 210 records)",
    "no duplicate front or back (out/closing_cards_scan.out: duplicate fronts [], duplicate backs []). The changed c145 front is unique; the near pairs named by the base (c097/c219, c179/c218) are unchanged records.")
FRESH["cards-sample-20"] = ("10 cards read", "cards.json (all 210 records read as data; the 4 changed records read against the lessons)",
    "the cards.json diff since 95f3f8cb has exactly 4 changed records (M3-c138, c141, c145, c174; 13 lines); no record was added or removed. All four were read in full against L08.html and out/closing_twin_L08.out. Other records byte-identical.")
FRESH["cards-c167-misconception"] = ("10-cards-lesson", "cards.json M3-c167 vs L09.html Definition 2.1 and Remark 2.2 and the twin",
    "M3-c167 is unchanged; the twin docstring changed but not its output: out/closing_twin_L09.out prints 23 of 23 strictly closer, so 'a SIMULATED Lab 1 case ... strictly closer' holds. Grade C naming the lab stands.")
FRESH["cards-c209-c213-new"] = ("10 cards new", "cards.json M3-c209 (L07), M3-c210 to M3-c213 (L08), M3-c214 (L08)",
    "M3-c209 read against L07 Section 1 (line 56 changed only in its citation; the card says 'defined in Section 1' and is unaffected). M3-c210 to c213 read against L08 Section 3 (unchanged) and Section 1. "
    "M3-c214 (C, SIMULATED six-tenor panel, PC1 level-like, planted scale 8 bp per day) matches out/closing_twin_L08.out and the lesson text at line 312.")
FRESH["cards-c204"] = ("10-cards-ids", "cards.json (no M3-c204)",
    "no record M3-c204 (out/closing_cards_scan.out: missing numbers include 204).")
FRESH["cards-c163-lab-count"] = ("10-cards-lab-numbers", "cards.json M3-c163; tests/labs/M3/lab-M3-L09-1.py",
    "M3-c163 is unchanged and says 'All 23'; closing twin output prints 'alternating-projection output passes is_correlation and is strictly closer to A than R: 23 of 23' (out/closing_twin_L09.out).")
FRESH["cards-sample-lesson-text-current"] = ("10 cards current text", "L01.html, L08.html, L09.html, cards.json",
    "cards read against the current L08.html (misconception text at line 312) and L09.html (lines 52, 200-201, 353); the changed cards agree with the current text. L01 cards c016-c019 are unchanged and L01.html is unchanged.")
FRESH["dag-m4-concepts-by-name"] = ("14 DAG names", "project.html; cards.json; L01-L09 text changed in this delta",
    "cards.json contains 'correlation' 18 times and 'variance' once (plain prose, ruling 3); 'covariance', 'expectation', 'Gaussian', 'standard deviation', 'Cholesky', 'IEEE' 0 times (out/closing_scan.out). "
    "Changed L07-L09 text uses correlation, Gaussian, standard deviation, yield (plain prose, ruling 3) and eigenvalues (in closure). No new named concept outside the prerequisite closure.")
FRESH["dag-cholesky-named-in-grader"] = ("14-dag-names", "course/modules/M/M3/grader/*.py; cards.json",
    "grep -i -c 'cholesky|IEEE' over grader/reference.py, instance.py, starter.py, test_project.py: 0 each; cards.json: 0 (out/closing_scan.out).")
FRESH["project-no-process-words"] = ("12 process words", "project.html; cards.json; grader/*.py; tests/labs/M3/lab-M3-project-*.py; changed L07-L09",
    "closing_scan.out: cards.json and changed pages contain 'fixed' only in learner senses ('a fixed grid', 'one fixed matrix C0', 'the fixed rank 2 factor', 'columns of U and V are fixed by A', 'Fixed seed', 'Fixed points of P'), "
    "'delta' only as the math symbol in the L09 proof, and 'Previous' only as the navigation label. No verifier, ledger, ruling, round, or pin wording. grader and project lab files are byte-identical since 95f3f8cb.")
FRESH["project-hours"] = ("4 hours arithmetic", "L01-L09 data-hours; index.html data-hours-lessons, data-hours-project; project.html hours table",
    "L01-L09 data-hours 12, 11, 12, 12, 12, 11, 11, 12, 12 = 105 (out/closing_scan.out); index.html data-hours-lessons=105 and data-hours-project=45; project.html data-hours-project=45. "
    "The data-hours attributes did not change in this delta (no data-hours line in the diff). The project table column sum (2+3+14+8+12+6 = 45) is carried from round 1 (project.html byte-identical since 95f3f8cb).")
FRESH["notation-registry"] = ("13 notation", "notation/notation.json; project.html; L07-L09; cards.json",
    "notation/notation.json unchanged since 95f3f8cb; cards.json 0 backslashes (out/closing_scan.out); changed lines in L07, L08, L09 and c138, c141, c145, c174 add no macro and no \\mathbb (L07-L09 \\mathbb count 0).")
FRESH["notation-R-macro"] = ("13 notation macro", "project.html; L07; L08; L09; cards.json",
    "cards.json has no backslash macro (0). L07-L09 have no \\mathbb (0 each). The changed project.html lines are not in this delta.")
FRESH["links-and-anchors"] = ("links", "course/modules/M/M3/project.html; index.html; L07; L08; L09",
    "check_pages M3 PASS (out/closing_check_pages_M3.out) covers anchors. The added lines in the L07-L09 hunks contain no href or src (grep count 0). index.html is byte-identical since 95f3f8cb.")

NEW = []
NEW.append({"id": "delta-L07-citation", "check": "1 lesson citation (delta hunk)", "location": "course/modules/M/M3/L07.html line 56",
    "status": "PASS", "evidence": "The new citation 'Lesson 4, Definition 1.2' for the inner product and norm is correct: L04.html line 74 is 'Definition 1.2 (inner product, norm, orthogonality)'. The old 'Lesson 6' was wrong, since L06.html line 56 defers these terms to Lesson 4, Definition 1.2. Lesson 4 is in L07's prerequisite closure (check_dag PASS)."})
NEW.append({"id": "delta-L08-misconception-text", "check": "1 lesson math (delta hunk); 3 proof", "location": "course/modules/M/M3/L08.html line 312 (Misconceptions item 3)",
    "status": "PASS", "evidence": "Checked claim by claim: 'components are ordered by their eigenvalues (Definition 1.3)' (L08.html line 82: lambda_1 >= ... >= lambda_n); 'Theorem 2.1 is about the squared movement along each direction' (line 100: maximum of u^T M u over unit u, and M = X~^T X~/(T-1) so u^T M u is the squared movement); 'In Lab 1 the first component is level-like on one simulated panel' (out/closing_twin_L08.out: PC1 best matches the planted level shape, |cosine| 0.9994); 'the lab does not vary the planted scales' (lab-M3-L08-1.py fixes scales 8, 4, 2 at lines 46-48). The paragraph states no unproved T claim."})
NEW.append({"id": "delta-L09-twin-docstring", "check": "2.5 lab twin (delta hunk); 1 lab statement vs code", "location": "tests/labs/M3/lab-M3-L09-1.py lines 9-11 and course/modules/M/M3/L09.html lines 200-201 (embedded copy)",
    "status": "PASS", "evidence": "Docstring item 4 now reads 'off-diagonal entries 0.5 plus the symmetrised noise (N + N^T) / 2, where N has independent Gaussian entries of standard deviation 0.35; unit diagonal; size 5'. Code (lab lines 85-88): noise = rng.normal(0.0, 0.35, size=(size, size)); noise = (noise + noise.T) / 2.0; a = 0.5 + noise; diagonal set to 1.0. Matches. Alternating projections: TOL 1e-12, MAX_ITER 500, is_correlation tolerances 1e-12 and -1e-8 match the text. run_labs (out/closing_run_labs_M3.out) confirms the page code equals the twin and the expected block equals its output. Twin alone EXIT 0 (out/closing_twin_L09.out)."})
NEW.append({"id": "delta-L09-section5-and-why", "check": "1 prose numbers; 3 proof (Problem R2)", "location": "course/modules/M/M3/L09.html lines 52, 353, 466-471",
    "status": "PASS", "evidence": "Section 5 'Rescaling can change the eigenvalues again (Problem R2)': R2 solution diag(1,4) with D = B gives C = diag(1,1), eigenvalues {1,4} versus {1,1}, so the claim is supported by a worked solution (hand check). Why-it-matters 'built on Definition 3.1': Method 1 (line 182) computes B = A_0 by Definition 3.1. The count sentence '23 ... in all 23' matches out/closing_twin_L09.out (23 of 23 both)."})
NEW.append({"id": "delta-notation-local-N-L09", "check": "13 notation (LOW observation, not a ruling-26 kind)", "location": "course/modules/M/M3/L09.html line 79 and lines 200-201",
    "status": "PASS", "evidence": "notation/notation.json says N is conventionally local and defined where used. In L09 the letter N is defined twice with different objects: line 79 'let N = Q M Q^T' (a proof in Section 1) and the lab docstring 'N has independent Gaussian entries' (a noise matrix). Each use defines its own N, so no registered meaning is changed. LOW observation for the fixer: a different letter for the noise would remove the overlap. Not a ruling-26 defect; not a FAIL."})
NEW.append({"id": "delta-scope-no-new-mutants", "check": "ruling 37 (closing round writes no mutants)", "location": "ledgers/M3/mutants/, ledgers/M3/alternatives/, ledgers/M3/equivalent/, ledgers/M3/retired/",
    "status": "PASS", "evidence": "git diff --quiet 95f3f8cb 2a805c83 over these four directories: unchanged. No mutant was authored in this round; the standing set of 184 was run (out/closing_mutate_M3_seeds0-9.out)."})

# Rows carried from the base, with the same subject; each cites its location.
rows_out = []
base_ids = [r["id"] for r in base["rows"]]
fresh_group_ids = {
    "mutants-new-student-errors": ("2.6 mutation", "ledgers/M3/mutants/v4d_02..v4d_04", [r"^v4d_0[234]"]),
    "mutants-v2d-01-05": ("2.6 mutation", "ledgers/M3/mutants/v2d_01..v2d_05", [r"^v2d_0[1-5]"]),
    "mutants-v3d-02-05": ("2.6 mutation", "ledgers/M3/mutants/v3d_02..v3d_05", [r"^v3d_0[2-5]"]),
    "mutants-v5d-new-student-errors": ("2.6 mutation", "ledgers/M3/mutants/v5d_02, v5d_03, v5d_05, v5d_06", [r"^v5d_0(2|3|5|6)"]),
    "mutants-r6-new-student-errors": ("2.6 mutation", "ledgers/M3/mutants/r6d_m02..r6d_m04", [r"^r6d_m0[234]"]),
    "mutants-r7-new-student-errors": ("2.6 mutation", "ledgers/M3/mutants/r7d_m01..r7d_m03", [r"^r7d_m0[123]"]),
    "mutants-v8d-new-student-errors": ("2.6 mutation", "ledgers/M3/mutants/v8d_01..v8d_04", [r"^v8d_0[1-4]"]),
    "mutants-v9d-new-student-errors": ("2.6 mutation", "ledgers/M3/mutants/v9d_01..v9d_04", [r"^v9d_0[1-4]"]),
    "mutants-v10d-new-student-errors": ("2.6 mutation", "ledgers/M3/mutants/v10d_01..v10d_04", [r"^v10d_0[1-4]"]),
    "mutants-v11d-new-student-errors": ("2.6 mutation", "ledgers/M3/mutants/v11d_01..v11d_03", [r"^v11d_0[1-3]"]),
}
equiv_fresh = {
    "mutants-v5d-04-accepted-stop-rule": ("alternative-stop-either", "ledgers/M3/alternatives/alt10_stop_when_either_gap_or_change.py", "alt10_stop_when_either_gap_or_change PASS seeds 0-49 (out/closing_alts_seeds0-49.out); file byte-identical since 95f3f8cb."),
    "equivalent-r6d-m04": ("alternative-gap-only-stop", "ledgers/M3/alternatives/alt7_dykstra_gap_only_stop.py", "alt7_dykstra_gap_only_stop PASS seeds 0-49 (out/closing_alts_seeds0-49.out)."),
    "equivalent-r11d-m02": ("alternative-step-only-stop", "ledgers/M3/alternatives/alt8_dykstra_step_only_stop.py", "alt8_dykstra_step_only_stop PASS seeds 0-49 (out/closing_alts_seeds0-49.out)."),
    "equivalent-r15d-m03-label": ("alternative-full-budget", "ledgers/M3/alternatives/alt9_dykstra_runs_full_budget.py", "alt9_dykstra_runs_full_budget PASS seeds 0-49 (out/closing_alts_seeds0-49.out)."),
}
fresh_grader = {
    "grader-test-count-and-purity": ("2.6 count; purity", "grader/test_project.py test_functions_print_nothing, test_inputs_are_not_mutated; project.html line 239",
        "collect-only = 198 (out/closing_collect_only_M3.out) = the count at project.html line 239 (the base's line 247 was a mis-citation). grader/test_project.py is byte-identical since 95f3f8cb, so the purity tests are unchanged."),
}
fresh_gate_verify = None

CARRY_ONLY_NOTE = "subject byte-identical since 95f3f8cb (verified with git diff --quiet on the cited files)."

fresh_ids = set(FRESH) | set(fresh_group_ids) | set(equiv_fresh) | set(fresh_grader)
for r in base["rows"]:
    rid = r["id"]
    if rid in FRESH:
        check, loc, ev = FRESH[rid]
        rows_out.append({"id": rid, "check": r.get("check", check), "location": loc, "status": "PASS", "evidence": ev})
    elif rid in fresh_group_ids:
        check, loc, prefixes = fresh_group_ids[rid]
        rows_out.append(group_row(rid, check, loc, prefixes))
    elif rid in equiv_fresh:
        check, loc, ev = equiv_fresh[rid]
        rows_out.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
    elif rid in fresh_grader:
        check, loc, ev = fresh_grader[rid]
        rows_out.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
    elif rid == "gate-verify-refs":
        ev = ("Carried from round 1 (references/references.json byte-identical since the previous pin 95f3f8cb; M3 records unchanged): base live run "
              "verify_refs --unit M3: 2 of 560 entries, 0 problems. Re-run offline this round: 560 entries, 0 problems, EXIT 0 (out/closing_verify_refs_offline.out).")
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})
    else:
        if r["status"] != "PASS":
            raise SystemExit(f"base non-PASS row not re-verified: {rid}")
        base_ev = CARRY_CHAIN.sub("", r["evidence"])
        prefix = CARRY_PREFIX.format(loc=r["location"])
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": prefix + base_ev})

missing_fresh = [i for i in FRESH if i not in base_ids]
rows_out.extend(NEW)
ids_seen = [r["id"] for r in rows_out]
assert len(ids_seen) == len(set(ids_seen)), "duplicate ids"
assert all(i in ids_seen for i in base_ids), "a base row id was dropped"

counts = {"PASS": sum(1 for r in rows_out if r["status"] == "PASS")}
verdict = "PASS" if counts["PASS"] == len(rows_out) else "FAIL"
mutants = [{"id": m["id"], "description": m["description"], "file": m["file"], "killed_by": m["killed_by"]} for m in mut_entries]

frag = {
    "unit": "M3",
    "slice": "d",
    "round": 1,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, closing delta round 1 (ruling 30); shares no context with the builders",
    "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
    "base": "F2-M3-d.round1 (pin 95f3f8cb21c2cd9fc904430bd30a6b734d01f672); delta 95f3f8cb..2a805c83 on this slice: course/modules/M/M3/L07.html line 56, L08.html line 312, L09.html lines 52, 200-201, 353, cards.json (M3-c138, c141, c145, c174), tests/labs/M3/lab-M3-L09-1.py lines 9-11. Rulings 30, 37 and 26 (FAIL kinds) apply.",
    "checkout": ROOT,
    "scratch": "ledgers/M3/scripts/M3-d-r1/",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows_out,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
}
print("rows:", len(rows_out), "PASS:", counts["PASS"], "verdict:", verdict, "mutants:", len(mutants))
print("fresh rows from base ids:", sorted(set(FRESH) & set(base_ids)))
print("new rows:", [r["id"] for r in NEW])
json.dump(rows_out, open("/private/tmp/verifyG1-M3-d-txt/rows_out.json", "w"), indent=1)
json.dump(mutants, open("/private/tmp/verifyG1-M3-d-txt/mutants_out.json", "w"), indent=1)
