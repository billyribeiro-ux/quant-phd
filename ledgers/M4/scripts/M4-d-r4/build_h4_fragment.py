"""Builds ledgers/M4/M4-d.json (round 4, slice d) from the round-4 gate outputs (h4_*)."""
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD4-M4-d")
OUT = ROOT / "ledgers/M4/scripts/M4-d-r4"
MUT = (OUT / "h4_mutate_M4_0-9_final.out").read_text(encoding="utf-8").splitlines()

mutants = []
for line in MUT:
    m = re.match(r"KILLED (\S+\.py): (.*?) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(1)[:-3], "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 130, len(mutants)
assert all(not m["killed_by"].startswith("SURV") for m in mutants)

def carry(files, text):
    return f"Carried from round 3 ({files} byte-identical since the previous pin a007712f): {text}"

def mkey(name):
    hits = [m["killed_by"] for m in mutants if m["id"].startswith(name)]
    assert hits, name
    return f"{name}: KILLED, {hits[0]}"

rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("d1-2.6-ladder", "2.6 ladder: rung 1 solved, rung 2 instant, rung 3 scope, rung 4 open",
    "course/modules/M/M4/project.html#ladder, #rungs, #spec, #stretch", "PASS",
    "Re-verified (project.html:57 changed: 'Assuming Assumption 1 (Conventions item 6)' added to the hypothesis; the rung prose at lines 44-47 is unchanged). Lab 1 twin tests/labs/M4/lab-M4-project-1.py and Lab 3 twin lab-M4-project-3.py are byte-identical; run_labs M4 13/13 (ledgers/M4/scripts/M4-d-r4/h4_run_labs_M4.out). The hypothesis arithmetic: w'Sigma w = 9e12*4e-4 + 4e12*9e-4 + 2*6e12*1e-4 = 8.4e9; (nu-2)/nu = 3/5 = 0.6 at nu = 5; ceil(0.99*20000) = 19800. Conventions item 6 is Assumption 1 (project.html:216, the sixth li of the Conventions list).")
row("d1-2.6-spec-questions", "2.6 spec: questions a competent student would have to ask",
    "course/modules/M/M4/project.html#conditions; course/modules/M/M4/grader/reference.py:65", "PASS",
    "Re-verified: project.html #conditions (lines 219-226) unchanged (the project.html delta is at lines 57 and 325 only). reference.py: the delta changes only the simulate_losses docstring (lines 59-64); the validation block (lines 65-74) and quantile_99 (lines 97-100) are unchanged in text and the docstring matches the code (r = L Z; r = sqrt((nu-2)/W) L Z, equivalently sqrt(s) sqrt(nu/W) L Z). run_graders M4 50/50 (h4_run_graders_M4_0-49.out).")
row("d1-2.6-hours", "2.6 hours: component sum and own estimate within 30 %",
    "course/modules/M/M4/project.html#budget; data-hours-project", "PASS",
    carry("project.html lines 231-248 and the data-hours-project attribute", "no delta hunk touches the budget section; the project.html hunks are at lines 57 and 325 only (git diff a007712f 4eb6788f)."))
row("d1-2.6-autograder-reference", "2.6 autograder: run_graders seeds 0-49 on reference.py",
    "course/modules/M/M4/grader/reference.py", "PASS",
    "Re-run: tools/run_graders.py --unit M4 --seeds 0-49 -> 'run_graders M4: PASS (reference 50/50 seeds, slowest 0.7 s)', exit 0 (h4_run_graders_M4_0-49.out). reference.py changed in its docstring only (lines 59-64); the code is unchanged and was re-read at lines 65-100.")
row("d1-2.6-instances", "2.6 instances: valid, and answers change across seeds",
    "course/modules/M/M4/grader/instance.py", "PASS",
    "Re-verified: instance.py changed in the docstring only (lines 5-8: factor entries rounded to 6 dp, product entries to 12 dp), and the code (lines 32-35: round(..., 6) for factor entries, round(sum, 12) for cov) matches it. Invariant sweep over seeds 0-1999 (python -I in /tmp/M4-d-r4-count): 0 invalid instances (n_assets in {2,3}, positions whole cents in [100000, 5000000], nu in 3..8, n_draws in the fixed set and never a multiple of 100 and <= 19987, cov symmetric, Cholesky pivots positive). nu counts 3:346 4:330 5:347 6:317 7:343 8:317; n_assets 2:984, 3:1016.")
row("d1-2.6-mut-own", "2.6 mutation: at least 3 verifier-written student-error mutants, all killed",
    "ledgers/M4/mutants/v1_01 .. v1_06", "PASS",
    "Re-run this round: " + "; ".join(mkey(f"v1_0{i}") for i in range(1, 7)) + " (ledgers/M4/scripts/M4-d-r4/h4_mutate_M4_0-9_final.out).")
row("d1-2.6-mut-existing", "2.6 mutation: the existing mutants re-run on seeds 0-9",
    "ledgers/M4/mutants/*.py (130 files at the end of this round)", "PASS",
    "Re-run this round: tools/mutate_graders.py --unit M4 --seeds 0-9 -> 'mutate_graders M4: PASS (130/130 killed)', exit 0 (h4_mutate_M4_0-9_final.out; 130 KILLED lines, no SURVIVED line). The 130 files are the 127 of round 3 plus the three new v8_01..v8_03 written by this verifier. An earlier run before v8 was written gave 127/127 (h4_mutate_M4_0-9.out).")
row("d1-2.6-mut-m11", "2.6 mutation: m11 loss sign flipped",
    "ledgers/M4/mutants/m11_loss_sign_flipped.py; project.html Conventions item 2", "PASS",
    "Re-verified: " + mkey("m11_loss_sign_flipped") + " (h4_mutate_M4_0-9_final.out). Conventions item 2 (project.html:212, 'The loss is positive when the portfolio falls') is outside every delta hunk.")
row("d1-2.6-mut-r9_03", "2.6 mutation: r9_03 chi-square reused on alternate draws",
    "ledgers/M4/mutants/r9_03_*.py; project.html Conventions item 5 and #contract-notes", "PASS",
    "Re-verified: " + mkey("r9_03_student_t_chi_square_reused") + " (h4_mutate_M4_0-9_final.out). The page still states the requirement at project.html:215 (Conventions item 5, one chi-square variable per draw), which the delta does not touch.")
row("d1-2.6-mut-v4_m02", "2.6 mutation: v4_m02 matched factor skipped for small nu",
    "ledgers/M4/mutants/v4_m02_*.py; project.html Grading mode and #contract-notes; test_project.py", "PASS",
    "Re-verified: " + mkey("v4_m02_matched_factor_skipped_for_small_nu") + " (h4_mutate_M4_0-9_final.out). project.html:206 (Grading mode) and :228 (contract-notes) are unchanged by the delta.")
row("d1-2.6-mut-m17", "2.6 mutation: m17 equivalent mutant",
    "ledgers/M4/equivalent/m17_student_t_second_seed.py and README.md; project.html:215 (Conventions item 5)", "PASS",
    carry("ledgers/M4/equivalent/ (m17 and README.md) and project.html:215", "the delta touches project.html only at lines 57 and 325."))
row("d1-2.6-alternatives", "2.6 alternatives: five alternative correct implementations pass",
    "ledgers/M4/scripts/alt_1.py .. alt_5.py; ledgers/M4/scripts/run_alternatives.py; course/modules/M/M4/grader/reference.py", "PASS",
    "Re-run this round: ledgers/M4/scripts/run_alternatives.py --seeds 0-9 -> reference.py, alt_1, alt_2, alt_3, alt_4, alt_5 each 'PASS (10/10 seeds)', exit 0 (h4_run_alternatives_0-9.out). alt_1..alt_5 and run_alternatives.py are byte-identical since a007712f; the reference.py change is a docstring. Seeds 0-49 not run this round.")
row("d1-2.6-starter", "2.6 starter: an empty implementation fails the suite",
    "course/modules/M/M4/grader/starter.py", "PASS",
    carry("grader/starter.py", "the starter is the same file; run_graders M4 (50/50 reference seeds) includes the starter-must-fail check per tools/run_graders.py docstring."))
row("d1-2.6-messages", "2.6 messages: failure messages name the property and give a hint",
    "course/modules/M/M4/grader/test_project.py (new tests after line 180)", "PASS",
    carry("grader/test_project.py lines 181-613 except the comment at line 373", "the only test_project.py hunk is the comment at line 373 (re-read below); the tests and their check() messages are unchanged."))
row("d1-2.6-count-and-pyodide", "2.6 count and pyodide: the page's test count equals collect-only, and 137 + 1 is correct",
    "course/modules/M/M4/grader/test_project.py; course/modules/M/M4/project.html#grading-mode", "PASS",
    "Re-verified in scratch copy /tmp/M4-d-r4-count (test_project.py, instance.py, reference.py as tail_risk.py): pytest --collect-only -> '138 tests collected'. QF_SEED 0, 1, 2 -> '137 passed, 1 skipped'; QF_SEED 3, 4, 5 -> '138 passed'. page_smoke --unit M4 --pages project -> 'in-browser grader: All 137 tests pass on seed 2118200738' (h4_page_smoke_project.out; that seed is a nu 3 or 4 instance). project.html:206 states 138 checks and the 137 + 1 case at nu 3 or 4 (676 of 2000 seeds have nu 3 or 4).")
row("d1-2.6-grader-comment-numbers", "2.6 grader comments: the numbers in the grader comments match the code",
    "course/modules/M/M4/grader/test_project.py:31-48 and the changed comment at line 373", "PASS",
    "Re-verified: the changed comment (test_project.py:373) reads 'quantile_99 runs on three losses, on one loss, on 100 losses and on 101 losses', and the code (lines 380-383) calls quantile_99 on [3, 1, 2], [7], range(100) and range(101). Lines 31-48 are carried from round 3 (byte-identical since a007712f): the file's only hunk is line 373.")
row("d1-rubric-observable", "2.6 rubric: every criterion descriptor is observable from the report",
    "course/modules/M/M4/project.html#rubric (table, line 332 onward)", "PASS",
    carry("project.html #rubric (lines 332 onward)", "the delta hunks are at lines 57 and 325. The C1 row (line 336) asks for the A1 and A3 integrals; the changed A3 hypothesis (independence of W and Z) is not a criterion the rubric grades, so the descriptors remain observable."))
row("d1-rubric-calibration", "2.6 rubric calibration: exemplar annotations match the descriptors",
    "course/modules/M/M4/project.html#exemplar-a, #exemplar-b", "PASS",
    carry("project.html #exemplar-a and #exemplar-b", "the exemplar text is at lines 348 onward, outside the delta hunks. Exemplar B's proof (line 429) states 'With Z and W independent', consistent with the new A3 hypothesis at line 325. Observation, not a FAIL: exemplar B does not write E[T^4] = 3 nu^2 E[W^-2] explicitly, which the rubric level-4 text (line 336) does not require."))
row("d1-rubric-question-bank", "2.6 rubric question bank: every question is answered by the page",
    "course/modules/M/M4/project.html", "PASS",
    carry("project.html", "the question bank (lines 470 onward) is outside the delta hunks."))
row("d1-atlas", "2.6 atlas: the project's atlas entries match the curriculum",
    "curriculum/meta.yaml:194-276; course/modules/M/M4/project.html", "PASS",
    carry("curriculum/meta.yaml", "the atlas section and project.html's atlas attributes are unchanged; check_projects M4 PASS (h4_check_projects.out)."))
row("d1-studio", "2.6 studio: the studio entry is correct",
    "curriculum/01-foundations.yaml:73-76", "PASS",
    carry("curriculum/01-foundations.yaml", "the studio entry is unchanged."))
row("d1-lab-project-1", "2.6 labs: Lab 1 runs and its page code equals its twin",
    "course/modules/M/M4/project.html#lab-M4-project-1; tests/labs/M4/lab-M4-project-1.py", "PASS",
    "Re-verified after the delta: run_labs M4 13/13 (h4_run_labs_M4.out); check_pages M4 PASS (h4_check_pages.out). The only Lab 1 text change is the hypothesis sentence at project.html:57; tests/labs/M4 is byte-identical since a007712f.")
row("d1-lab-project-2", "2.6 labs: Lab 2 runs and its page code equals its twin",
    "course/modules/M/M4/project.html#lab-M4-project-2; tests/labs/M4/lab-M4-project-2.py", "PASS",
    carry("tests/labs/M4/lab-M4-project-2.py and project.html #lab-M4-project-2", "run_labs M4 13/13 this round (h4_run_labs_M4.out)."))
row("d1-lab-project-3", "2.6 labs: Lab 3 runs and its page code equals its twin",
    "course/modules/M/M4/project.html#lab-M4-project-3; tests/labs/M4/lab-M4-project-3.py", "PASS",
    carry("tests/labs/M4/lab-M4-project-3.py", "run_labs M4 13/13 this round (h4_run_labs_M4.out); the Lab 3 rung-3 prose is unchanged."))
row("d1-prose-numbers", "2.6 prose numbers: every number in the project prose matches its computation",
    "course/modules/M/M4/project.html (Labs, Report, Exemplars A and B)", "PASS",
    "Re-derived the numbers in the changed hypothesis (project.html:57): 8.4e9, 0.6, 19800 (see d1-2.6-ladder). The changed appendix sentence (project.html:325) introduces no number. Other numbers are carried from round 3 (project.html is byte-identical there).")
row("d1-prose-scope", "2.6 prose scope words: each universal is backed by a computation or a hypothesis",
    "course/modules/M/M4/project.html (lines 57 and 325); grader/instance.py docstring", "PASS",
    "Scope words in the two changed project.html sentences: 'Assuming Assumption 1 (Conventions item 6)' is an explicit hypothesis; 'assuming Assumption 1 and that the chi-square variable W is independent of the standard normal Z' is an explicit hypothesis. The changed instance.py docstring has 'nu > 2 always' (line 9), backed by rng.randrange(3, 9) (code line 38). No new scope word enters the other changed text.")
row("d1-prose-process-words", "2.6 prose: no process words in learner text",
    "course/modules/M/M4/project.html", "PASS",
    "grep -i -n 'round|verifier|ledger|builder|TODO' project.html: the only hits are round, rounded, rounding, unrounded and round() in the cent rule and the numerical statements (lines 61, 103-104, 204, 206, 212, 272-273, 293, 305, 350, 418); no process word.")
row("d1-prose-banned-phrases", "2.6 prose: banned phrases absent",
    "course/modules/M/M4/project.html", "PASS",
    "tools/check_pages.py BANNED list (line 58) is applied to visible prose; check_pages M4 PASS (h4_check_pages.out). The changed sentences were read against the list.")
row("d1-dag", "2.6 DAG: concepts used are in the prerequisite closure",
    "course/modules/M/M4/project.html", "PASS",
    "check_dag M4 PASS (h4_check_dag.out). The changed sentences use Assumption 1 and the chi-square variable, both defined in the module.")
row("d1-notation", "2.6 notation: symbols match notation/notation.json and are not reused",
    "notation/notation.json; course/modules/M/M4/project.html", "PASS",
    "notation/notation.json (8 symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) is byte-identical. In M4 pages gamma_3 and gamma_4 are the skewness and kurtosis (L03.html, cards.json); Phi is the standard normal CDF (cards.json:953). The symbols W (chi-square), Z (standard normal), nu, s (matched factor) and R (return) in the changed text are module-local (project.html:211), not registry symbols, and none reuses a registry symbol's meaning.")
row("d1-cites", "2.6 citations: every cited source is a registry key",
    "course/modules/M/M4/project.html#reading; references/references.json", "PASS",
    carry("project.html #reading and references/references.json", "verify_refs --offline: 560 entries, 0 problems (h4_verify_refs_offline.out)."))
row("d1-structure", "2.6 structure: sections, headings and the proof appendix are in place",
    "course/modules/M/M4/project.html", "PASS",
    "check_pages M4 PASS (h4_check_pages.out); page_smoke project PASS (h4_page_smoke_project.out). The structural delta is two sentences (lines 57 and 325); no heading changed.")
row("d1-cards-schema", "2.6 cards schema: every entry has id, lesson, front, back, grade",
    "course/modules/M/M4/cards.json", "PASS",
    "Re-checked: 212 entries, 212 unique ids, lessons L01..L10; 192 entries with keys id, lesson, front, back, grade and 20 C entries with the extra key basis; grades T 192, C 20.")
row("d1-cards-numbers-in-lesson", "2.6 cards: every card number appears in its lesson",
    "course/modules/M/M4/cards.json vs course/modules/M/M4/L01.html..L10.html", "PASS",
    "The three changed cards: M4-c081 (L05) cites Proposition 2.4 and 2^2 <= 1 (L05.html:149-150, 301); M4-c140 (L09) cites Proposition 2.3(b), Assumption 1 and Section 4 (L09.html:132, 294); M4-c199 (L02) cites Proposition 2.2, Example 2.5, 91/6, 35/12, 7/2 (L02.html:135-136, 281).")
row("d1-cards-labs", "2.6 cards: the C cards match their labs",
    "course/modules/M/M4/cards.json (the 20 C cards); tests/labs/M4/lab-M4-L02..L10-1.py", "PASS",
    carry("cards.json C entries and tests/labs/M4", "none of the three changed cards is a C card; run_labs M4 13/13 (h4_run_labs_M4.out)."))
row("d1-cards-math", "2.6 cards math: every card's claim is correct",
    "course/modules/M/M4/cards.json (all 212 entries read)", "PASS",
    "The three changed entries were re-derived: M4-c199 Var(X) = 91/6 - (7/2)^2 = 182/12 - 147/12 = 35/12 (L02.html:136), and the change is the hypothesis clause only; M4-c081 the 2^2 <= 1 contradiction; M4-c140 has no numerical claim. The other 209 entries are byte-identical since a007712f (git diff shows exactly three cards.json entries changed in this delta). Carried from round 3 for those 209.")
row("d1-cards-lesson-statements", "2.6 cards vs lesson: each card agrees with the current lesson statement and its hypotheses",
    "course/modules/M/M4/cards.json vs the L01..L10 propositions and examples", "FAIL",
    "M4-c140 (cards.json:978-981, back at line 981) states 'The statement needs i.i.d. copies with finitely many values and finite positive variance sigma^2'. The lesson's own sentence on the same claim, L09.html:294 (misconception 'The central limit theorem needs the variables to be normal'), reads 'The statement needs i.i.d. copies with finite positive variance', with no finitely-many-values clause. Definition 2.4 (L09.html:147) states the CLT for X with no finitely-valued restriction. The finitely-valued hypothesis belongs to Proposition 2.3 (L09.html:132: 'Under the i.i.d. hypotheses of this section, with the variables finitely valued'), so the card attributes Proposition 2.3's hypothesis to the CLT statement. The other changed cards agree: M4-c199 (L02.html:55, finite probability space with positive weights) and M4-c081 (L05.html:149-150, 301).",
    "In cards.json M4-c140 back, remove 'with finitely many values' from 'The statement needs i.i.d. copies ...' so it reads 'The statement needs i.i.d. copies with finite positive variance sigma^2', and attribute the finitely-valued hypothesis to Proposition 2.3(b): 'Proposition 2.3(b), for finitely valued laws under Assumption 1 of Section 2, gives the limit e^(-t^2/2) ...'. This matches L09.html:294 and L09.html:132.")
row("d1-cards-duplicates", "2.6 cards: no duplicate cards",
    "course/modules/M/M4/cards.json", "PASS",
    "Python check on cards.json: 212 unique ids; no duplicate normalized front and no duplicate normalized back. M4-c199 'What is Var(X) for a fair six-sided die?' is distinct from M4-c029 'Is Var(X) always equal to E[X^2]?' and from M4-c181.")
row("d1-cards-c191-grade", "2.6 cards: M4-c191 grade and hypotheses",
    "course/modules/M/M4/cards.json (M4-c191, line 1339)", "PASS",
    carry("cards.json M4-c191 (line 1339)", "the entry is unchanged; grade T."))
row("d1-cards-hypotheses", "2.6 cards: every card that cites a proposition carries its hypotheses",
    "course/modules/M/M4/cards.json (M4-c140 back, line 981; M4-c199 line 1389; M4-c081 line 567)", "FAIL",
    "Round-3 FAILs fixed and still correct: M4-c028, M4-c029, M4-c070, M4-c199 carry 'Hypothesis: finite probability space with positive weights' or 'finitely many values' matching L02.html:55 and L05.html:60. M4-c081 (line 567) states 'for a vector with finitely many values Proposition 2.4 needs 2^2 <= 1' and matches L05.html:150. NEW FAIL: M4-c140 (line 981) now carries the Proposition 2.3(b) hypothesis 'finitely many values' in the wrong clause (the CLT statement), so the card over-states the CLT's hypotheses against L09.html:147 and :294; the Proposition 2.3(b) hypothesis is missing from the clause that cites it.",
    "Same fix as d1-cards-lesson-statements: cards.json M4-c140 back: 'The statement needs i.i.d. copies with finite positive variance sigma^2 ...' and 'Proposition 2.3(b), for finitely valued laws under Assumption 1 of Section 2, gives the limit ...'.")
row("d1-data", "2.6 data: inputs are SIMULATED and labelled",
    "course/modules/M/M4/project.html (Inputs); grader/instance.py", "PASS",
    "instance.py docstring and the 'label': 'SIMULATED' key (instance.py:42) are unchanged in meaning; the only instance.py change is the docstring rounding description, verified against code (see d1-2.6-instances). No real data is used.")
row("d1-freshness-registry", "2.6 freshness: registry entries are current",
    "references/references.json (blitzstein2019introduction)", "PASS",
    carry("references/references.json", "verify_refs --offline 560 entries, 0 problems (h4_verify_refs_offline.out); the live verify was not run."))
row("d1-gates-repo", "2.6 gates: the repository gates for the slice pass",
    "pyproject.toml; tests/labs/M4; tests/test_labs.py, test_run_labs.py, test_page_smoke.py, test_page_checks.py, test_refs.py", "PASS",
    "ruff check on the slice paths: 'All checks passed!' (h4_ruff_check.out); ruff format --check on the slice paths: '42 files already formatted' (h4_ruff_format.out); mypy --no-incremental: 'Success: no issues found in 331 source files' (h4_mypy.out); pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_page_checks.py tests/test_refs.py: exit 0 (h4_pytest_relevant.out); verify_refs --offline exit 0.")
row("d1-tools-structure", "2.6 tools: the tooling that checks the unit is intact",
    "tools/*.py", "PASS",
    carry("tools/*.py", "tools/ is byte-identical; the M4 gates above were run with it."))
row("d2-2.6-constraints-exceptions", "2.6 constraints: the page names what the suite does not test",
    "course/modules/M/M4/project.html:204 (Constraints) and :228 (What the suite does not test)", "PASS",
    carry("project.html lines 204 and 228", "the delta hunks are at lines 57 and 325 only; the Student-t sign (item 2) and the Student-t draw order (item 5) remain listed as untested."))
row("d3-2.6-mut-new-student-error", "2.6 mutation: this verifier's new student-error mutants, all killed",
    "ledgers/M4/mutants/v8_01..v8_03 (written this round); v7_01..v7_04 (round 3, committed)", "PASS",
    "Three new student-error mutants written this round by this verifier: " + "; ".join(mkey(n) for n in ["v8_01", "v8_02", "v8_03"]) + " (h4_mutate_M4_0-9_final.out). Each has a one-line docstring naming its error; they were written by a one-off python script run inline from reference.py (the script is not saved in the checkout). Round-3 v7_01..v7_04 are re-run and KILLED.")

fragment = {
    "unit": "M4",
    "slice": "d",
    "round": 4,
    "verifier": "independent verifier (Haiku), unit M4, slice d, round 4; not a builder of M4",
    "pin": "4eb6788f (checkout detached at the pin)",
    "base": "a007712f (round-3 pin; delta from git diff a007712f 4eb6788f)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-M4-d",
    "scratch": "/tmp/M4-d-r4-count (collect-only and invariant copies); outputs under ledgers/M4/scripts/M4-d-r4/h4_*",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: the round-4 delta a007712f..4eb6788f in the M4 slice: project.html (lines 57 and 325), grader/instance.py (docstring), grader/reference.py (docstring), grader/test_project.py (comment at line 373), cards.json (M4-c081, M4-c140, M4-c199), and the 9 mutant files v6_01..v6_05 and v7_01..v7_04 newly tracked. Out of slice, read only where cited: L02.html, L03.html, L04.html, index.html (text changes in references, footer, a solution and the lede).",
        "Checkout state at start: clean at 4eb6788f apart from the .venv symlink (pinned to the main repo's .venv). ledgers/M4/scripts/M4-d-r4/ already held untracked files from an earlier attempt (build_fragment_r4.py, sweep_r4.py, gauss_sweep_r4.py, run_alt_r4.sh and others); none was used as evidence. Every gate was re-run with h4_* outputs.",
        "Mutants: three new student-error mutants v8_01..v8_03 were written to ledgers/M4/mutants/ by this verifier; all 130 files were run.",
        "Could not check: (a) run_alternatives on seeds 0-49 (asked 0-9); (b) a full line-by-line re-read of project.html (501 lines): only the two delta hunks, the sections they touch, and the carried sections were read; (c) the Appendix A proofs beyond the changed A3 statement and exemplar B; (d) an interactive browser run of the grader (page_smoke headless only); (e) verify_refs live (offline only); (f) the full repository pytest suite (targeted suites only); (g) ruff format on the whole repository (the one M3 retired file flagged in round 3 is out of slice); (h) the 209 carried cards.json entries are carried per entry, not re-derived; (i) the lesson pages L02, L03, L04 and index.html were read only at the changed hunks.",
    ],
    "summary": (
        "Slice d round 4: %d rows, %d PASS, %d FAIL. Two FAIL rows, both on one defect: M4-c140 (cards.json:981) attributes Proposition 2.3's finitely-many-values hypothesis to the CLT statement, which L09.html:294 and Definition 2.4 (L09.html:147) do not state; the round-3 hypothesis fix over-corrected. The other round-3 FAIL rows are fixed and re-verified. Gates: check_pages, check_dag, check_projects, run_labs 13/13, run_graders 50/50, mutate_graders M4 seeds 0-9 130/130 killed (exit 0), run_alternatives seeds 0-9 10/10 for reference and alt_1..alt_5, page_smoke project, ruff, mypy, relevant pytest, verify_refs offline, collect-only 138 with 137+1 at nu 3 or 4."
        % (len(rows), sum(r["status"] == "PASS" for r in rows), sum(r["status"] != "PASS" for r in rows))
    ),
}
bad_rows = [r for r in rows if r["status"] != "PASS"]
fragment["verdict"] = "PASS" if not bad_rows else "FAIL"
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, len(rows), "rows", len(mutants), "mutants", "verdict", fragment["verdict"])
