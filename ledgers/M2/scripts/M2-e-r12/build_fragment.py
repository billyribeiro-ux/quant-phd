"""Build the round-12 fragment for M2 slice e (rows keep every round-11 id)."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB12-M2-e")
P = "Carried from round 11 (course/modules/M/M2/project.html byte-identical since the previous pin): "
G = "Carried from round 11 (course/modules/M/M2/grader/ and tests/labs/M2/lab-M2-project-{1,2,3}.py byte-identical since the previous pin): "
CARDS_CHANGED = ("M2-c282, c284, c286, c315, c326, c348, c349, c350, c357, c360, c361, c363, c364 (the 13 cards changed since f42f432)")

def carry(prefix, r11):
    return prefix + r11

prev = {r["id"]: r for r in json.load(open("/Users/billyribeiro/.fanout/frags/B-M2-e.round11.json"))["rows"]}

rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("e-auto-run", "run_graders reference passes the suite on seeds 0-49", "course/modules/M/M2/grader/reference.py", "PASS",
    "Fresh on ff38842: `.venv/bin/python tools/run_graders.py --unit M2 --seeds 0-49` -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)' (exit 0).")
row("e-auto-instances", "instance.py deterministic and varies by seed", "course/modules/M/M2/grader/instance.py", "PASS",
    carry(G, prev["e-auto-instances"]["evidence"]))
row("e-mut-existing", "all existing grader mutants killed", "ledgers/M2/mutants/", "PASS",
    "Fresh: `.venv/bin/python tools/mutate_graders.py --unit M2` -> 'mutate_graders M2: PASS (110/110 killed)' (exit 0; 107 pre-existing plus my three new mutants; every line reads KILLED, 0 survivors). Output in /tmp/m2e_r12/mutate_r12.txt.")
row("e-mut-r6_01", "round-6 mutant r6_01 (step capped at one) killed", "course/modules/M/M2/grader/test_project.py:282-308", "PASS",
    "Fresh mutate run: 'KILLED r6_01_fd_step_silently_capped_at_one.py ... -> test_large_positive_step_is_accepted (seed 0)'.")
row("e-mut-r6_02", "round-6 mutant r6_02 (hessian step capped) killed", "course/modules/M/M2/grader/test_project.py:546-580", "PASS",
    "Fresh mutate run: 'KILLED r6_02_hessian_step_silently_capped_at_a_thousandth.py -> test_hessian_positive_step_...'.")
row("e-mut-new-killed", "at least three new student-error mutants of my own, each killed", "ledgers/M2/mutants/r12_01..r12_03", "PASS",
    "Three new mutants written from course/modules/M/M2/grader/reference.py, each a student error that violates a stated size or output contract: r12_01 hessian_fd rounds entries to six places -> KILLED by test_hessian_positive_step_is_accepted (seed 0); r12_02 fd_derivative refuses steps above 1e5 although project.html line 209 says accepted 'from 10^-300 to 10^6' -> KILLED by test_large_positive_step_is_accepted (seed 0); r12_03 hessian_fd refuses steps below 1e-3 although project.html line 209 says accepted 'by hessian_fd ... from 10^-4 to 1' -> KILLED by test_hessian_is_a_square_list_of_lists_of_floats[inst0] (seed 0). Syntax checked with ast.parse.")
row("e-alternatives", "five alternative correct implementations pass; this round two of them, 50 seeds each", "course/modules/M/M2/grader/test_project.py", "PASS",
    "Fresh: ledgers/M2/scripts/M2-e-r12/run_alt.sh on alts/alt1_exact_engine.py (exact Fraction prices, integer half-even rounding, dual-number and reciprocal forms) -> '50/50 seeds pass, 0 fail'; alts/alt2_float_reordered_engine.py (math.fsum sums, reciprocal and reordered finite-difference forms, mixed entries times 0.25/h^2) -> '50/50 seeds pass, 0 fail'. The first draft of alt1 failed 19 seeds only because my decimal-rounding code overflowed at prec 80 on the suite's large instance; it was replaced by exact integer rounding and then passed (not a grader finding).")
row("e-messages", "grader messages name the property and never print expected values", "course/modules/M/M2/grader/test_project.py", "PASS",
    carry(G, prev["e-messages"]["evidence"]))
row("e-pyodide-local", "page_smoke and local reference run pass", "course/modules/M/M2/grader/test_project.py", "PASS",
    "Fresh: `.venv/bin/python tools/page_smoke.py --unit M2 --pages project.html` -> 'page_smoke M2: PASS' (exit 0); run_graders PASS above.")
row("e-test-count", "page's test count equals collect-only count", "course/modules/M/M2/project.html (says 85 tests)", "PASS",
    "Fresh: copied grader/test_project.py and reference.py (as sensitivity_engine.py) and instance.py into a scratch dir; `QF_SEED=0 python -m pytest --collect-only -q test_project.py` -> '85 tests collected'. project.html line 211 says 'runs 85 tests'.")
row("e-valueerror-scope", "ValueError only for the three named conditions", "course/modules/M/M2/grader/test_project.py; course/modules/M/M2/project.html Conventions (Constraints)", "PASS",
    carry(P, prev["e-valueerror-scope"]["evidence"]))
row("e-scheme-types", "scheme type cases match the page", "course/modules/M/M2/project.html Grading mode and Conventions", "PASS",
    carry(P, prev["e-scheme-types"]["evidence"]))
row("e-hours", "hours table and declared total", "course/modules/M/M2/project.html Time budget", "PASS",
    carry(P, prev["e-hours"]["evidence"]))
row("e-hours-arith", "hours components sum to the total", "course/modules/M/M2/project.html Time budget", "PASS",
    carry(P, prev["e-hours-arith"]["evidence"]))
row("e-ladder", "four-rung ladder in order", "course/modules/M/M2/project.html:40-48", "PASS",
    carry(P, prev["e-ladder"]["evidence"]))
row("e-spec-questions", "specification names every required output and function", "course/modules/M/M2/project.html Rung 3 (line 46)", "PASS",
    carry(P, prev["e-spec-questions"]["evidence"]))
row("e-rubric-calibration", "rubric exemplars calibrate the five criteria", "course/modules/M/M2/project.html The rubric and Two exemplars (lines 398-507)", "PASS",
    carry(P, prev["e-rubric-calibration"]["evidence"]))
row("e-rubric-observable", "every rubric level is observable", "course/modules/M/M2/project.html rubric table (line 402)", "PASS",
    carry(P, prev["e-rubric-observable"]["evidence"]))
row("e-rubric-adversarial", "rubric resists a generous self-score", "course/modules/M/M2/project.html Self-assessment and rubric table", "PASS",
    carry(P, prev["e-rubric-adversarial"]["evidence"]))
row("e-atlas-studio", "atlas and build plan unchanged", "curriculum/meta.yaml; plans/M2-build-plan.md", "PASS",
    "git diff f42f432..ff38842 -- curriculum/meta.yaml plans/M2-build-plan.md: no change (only course/modules/M/M2 cards and L20-L24 lessons changed).")
row("e-labs-run", "project labs run under -I -W error and via run_labs", "tests/labs/M2/lab-M2-project-{1,2,3}.py", "PASS",
    "Fresh: `python -I -W error tests/labs/M2/lab-M2-project-N.py` exit 0 with empty stderr for N = 1, 2, 3 (outputs in /tmp/m2e_r12/lab{1,2,3}.out); `tools/run_labs.py --unit M2` -> 'run_labs M2: PASS (27/27)'.")
row("e-labs-page-twin", "page code and expected blocks equal the twins and their output", "course/modules/M/M2/project.html Lab 1-3 blocks", "PASS",
    "Fresh: run_labs M2 PASS 27/27 (the tool compares each inline lab with its twin byte-for-byte and its expected block with the run output).")
for rid in ["e-lab1-numbers", "e-lab2-numbers", "e-lab3-numbers", "e-lab3-interpretation", "e-report-spec", "e-exemplar-numbers", "e-sin-ratio", "e-formulas"]:
    loc = prev[rid]["location"]
    row(rid, prev[rid]["check"], loc, "PASS", carry(P, prev[rid]["evidence"]))
row("e-cards-correct", "every card agrees with the current lesson text", "course/modules/M/M2/cards.json (379 cards); L01-L24.html", "FAIL",
    "All 379 cards read against their cited lesson passages and lab output this round. Two cards do not agree. (a) M2-c058 (L05, cards.json line of id M2-c058): front 'In Lab 1, what is the composite c(x) = (x^2 + 1)^3 central-difference error at x = 1.5?' asks about c(x), but the back's 'analytic value 95.0625' is c'(1.5) = 6x(x^2+1)^2 = 95.0625 (L05 line 156: 'Lab 1 prints the analytic chain-rule derivative at 1.5 as 95.062500000'); c(1.5) = 3.25^3 = 34.328. (b) M2-c285 (L19 Remark 3.2): front asks 'what is the coefficient of s^2 along a unit direction d?', but the back gives only g''(0) = d^T H(p) d; the coefficient is (1/2) g''(0) (L19 line 53: 'The coefficient of s^2 is (1/2) g''(0) = (1/2) d^T H(p) d'). All other cards agree, including the 13 changed cards (see e-cards-delta).",
    "Fix M2-c058 front to ask for the central-difference error of the derivative c'(x) at x = 1.5 (c'(1.5) = 95.0625, the value the lab compares with); fix M2-c285 back to state that the coefficient of s^2 is (1/2) g''(0) = (1/2) d^T H(p) d, then keep the axis remark. Then re-run check_pages and the card checks.")
row("e-cards-delta", "changed and added cards agree with their lessons, carry the hypotheses, and are correctly graded", "course/modules/M/M2/cards.json: " + CARDS_CHANGED, "PASS",
    "git diff f42f432..ff38842 -- cards.json: 13 cards changed (26 back lines), no id added or removed. Each re-read against its lesson: M2-c282/c284/c286 (L19 lines 31, 45, 247 state 'Assuming Assumption 2.1 of Lesson L06'); c315 and c326 (L21 line 25 'Assumption 1.3 (intermediate value theorem)'; L22 line 38 uses the same name), so the round-11 'intermediate value property' wording is gone; c348/c349/c350 (L23 lines 146, 150, 154 each begin 'Assuming Assumption 2.1'); c357 (L23 lines 44-47 and 162 match the 'exact rational ... floats ... rounded once' wording); c360/c361/c363/c364 (L24 lines 31, 35, 46, 50 match the hypotheses and bounds). Grades: all T with basis None; no new claim beyond the lesson. Round-11 FAIL rows are resolved.")
row("e-cards-atomic", "cards are single facts", "course/modules/M/M2/cards.json", "PASS",
    "Re-read of all 379 cards this round; each back states one fact or one proof step. No card combines two independent claims beyond a theorem with its hypotheses.")
row("e-cards-dup", "no duplicate cards or fronts", "course/modules/M/M2/cards.json", "PASS",
    "Fresh python check: 379 unique ids; 0 duplicate fronts (case-insensitive, stripped).")
row("e-cards-numbers", "every card number is re-derived and appears in its lesson", "course/modules/M/M2/cards.json", "PASS",
    "Every card with a number was re-derived: (i) 76 C-graded cards and the lab-number cards (e.g. M2-c006, c025, c026, c035-c036, c046-c050, c056-c058, c069-c070, c085-c086, c092-c093, c105-c107, c125-c127, c139-c141, c156-c158, c170-c172, c191-c197, c207-c209, c232-c234, c244-c245, c259-c261, c271-c273, c287-c289, c301, c313-c314, c328-c329, c336, c341-c346, c352-c354, c367-c370, c381-c385) against the fresh output of each twin (tests/labs/M2/lab-M2-L*.py run under -I -W error, outputs in /tmp/m2e_r12/labout/); (ii) analytic numbers re-derived by hand or in python (e.g. 95.0625, 29/49, 8/3, 1/60, 2/(3 sqrt 3) = 0.3849002, 2e-18 offset 2.8e-18 and 2.1e-12 cents for the L23 E3 solution, 9.990/10.101/98.91/101.11 and the L13 intervals, 1.8e-8 and 6.3e-6 minimising steps, H_16384 - 1 = 9.2813). Lesson-side interval numbers were found in L13 lines 48, 175, 229, 235. A mechanical substring check of every number against the lesson text also reports no missing number (weak check: small integers match trivially; this row rests on the manual re-derivation above).")
row("e-cards-labels", "numbered labels cited by cards exist in the cited lesson", "course/modules/M/M2/cards.json", "PASS",
    "Mechanical check (ledgers/M2/scripts/M2-e-r12/check_cards_mech.py) over all 379 cards: every Theorem/Proposition/Assumption/Example/Definition/Corollary/Remark/Lemma/Lesson label resolves in its lesson or the lesson it names. The only 50 flags are 'Misconception n'; these labels are generated by the CSS counter in course/assets/css/course.css:941-955 ('Misconception ' counter(mis)), and each cited misconception was matched to its position in the lesson's Misconceptions list. Problem and Remark labels cited by cards (e.g. Problem L08-R2, L09 Remark 1.3, L12 Problem R3) were checked by hand.")
row("e-cards-grades", "grades are T, C or absent; C has basis, T has none", "course/modules/M/M2/cards.json", "PASS",
    "Fresh python check: 241 T, 76 C, 62 absent; 0 violations (every C has a basis, no T has a basis, no other grade value).")
row("e-cards-delta-removed", "removed cards are gone and no id collision remains", "course/modules/M/M2/cards.json: M2-c389, M2-c388", "PASS",
    "git diff f42f432..ff38842 -- cards.json shows no line changed in an id field; the 379 ids are unique; M2-c388 (L10) and M2-c389 (L08) are each present once.")
row("e-data-figures", "no data figures or embedded data on the project page", "course/modules/M/M2/project.html", "PASS",
    carry(P, prev["e-data-figures"]["evidence"]))
row("e-structure", "page structure and check_pages", "course/modules/M/M2/", "PASS",
    "Fresh: `tools/check_pages.py --unit M2` -> 'check_pages M2: PASS' (exit 0).")
row("e-banned-phrases", "no process words in learner text", "course/modules/M/M2/*.html, cards.json", "PASS",
    "Fresh: check_pages M2 PASS (banned-phrase list of tools/check_pages.py BANNED applied to pages); the same 15 patterns applied to all 379 cards: 0 hits.")
row("e-dag", "no concept used outside the prerequisite closure", "course/modules/M/M2/", "PASS",
    "Fresh: `tools/check_dag.py --unit M2` -> 'check_dag M2: PASS' (exit 0). Changed lesson text in L19-L24 cites only Lesson 6 and earlier lessons of the unit.")
row("e-notation", "symbols match notation/notation.json", "notation/notation.json; course/modules/M/M2/ changed lines", "PASS",
    "Registered symbols (notation.json 'symbols': T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q) do not occur in any changed M2 line (f42f432..ff38842). The changed lines use L (Lipschitz constant, L24 R2, defined locally in that sentence) and V, delta, Delta, M_2, M_3, which are not registered. Program-wide registry unchanged.")
row("e-citations", "no unread attributions; references are registry keys", "course/modules/M/M2/project.html:547-551", "PASS",
    carry(P, prev["e-citations"]["evidence"]))
row("e-hours-declared-spec", "declared hours match the page's time budget", "course/modules/M/M2/project.html:35", "PASS",
    carry(P, prev["e-hours-declared-spec"]["evidence"]))

ids = {r["id"] for r in rows}
missing = [i for i in prev if i not in ids]
assert not missing, missing
extra = [i for i in ids if i not in prev]
assert not extra, extra

mutants = [
    {"id": "r12_01_hessian_entries_rounded_to_six_places", "description": "hessian_fd returns entries rounded to six decimal places (early output rounding).", "killed_by": "test_hessian_positive_step_is_accepted (seed 0)"},
    {"id": "r12_02_fd_refuses_steps_above_one_hundred_thousand", "description": "fd_derivative refuses steps above 1e5 although project.html line 209 says steps are accepted from 1e-300 to 1e6.", "killed_by": "test_large_positive_step_is_accepted (seed 0)"},
    {"id": "r12_03_hessian_refuses_steps_below_a_thousandth", "description": "hessian_fd refuses steps below 1e-3 although project.html line 209 says Hessian steps are accepted from 1e-4 to 1.", "killed_by": "test_hessian_is_a_square_list_of_lists_of_floats[inst0] (seed 0)"},
]

frag = {
    "unit": "M2",
    "slice": "e",
    "round": 12,
    "verifier": "independent verifier (Haiku 5.5), slice e",
    "pin": "ff388424d9d056b7a57868dab5ae7f7cdeef60f6",
    "base": "f42f4329dcb0b5c2257e40cd6c27e734fa700d46 (round-11 pin); round-11 fragment /Users/billyribeiro/.fanout/frags/B-M2-e.round11.json",
    "checkout": str(ROOT),
    "scratch": "/tmp/m2e_r12",
    "verified_at": "2026-10-29T00:00:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "cards.json changed since f42f432: 13 cards (c282, c284, c286, c315, c326, c348, c349, c350, c357, c360, c361, c363, c364); no id added or removed.",
        "L20-L24 lesson HTML changed (Assumption 3.1 placement, R2 wording, E3 solution, table rows); these are not in slice e but are the sources the cards cite.",
        "project.html, grader/ and the project lab twins are byte-identical to f42f432 (git diff --quiet exit 0); their rows are carried.",
    ],
    "notes": [
        "Fresh gate outputs on ff38842: check_pages M2 PASS; check_dag M2 PASS; check_projects M2 PASS; run_graders M2 PASS (50/50); mutate_graders M2 PASS (110/110); run_labs M2 PASS (27/27); page_smoke M2 PASS (project.html); verify_refs --offline: 560 entries, 0 problems; ruff check and ruff format --check on grader and tests/labs/M2 clean; mypy --no-incremental: no issues in 255 files; collect of test_project.py: 85 tests; tests/test_run_labs.py and tests/test_page_checks.py pass; ruff check . all checks passed.",
        "Read all 379 cards against their lesson passages (targeted: the theorem, example, misconception or lab cited by each card, read in full) and against the fresh output of all 27 lab twins. Not read line by line: the full prose of every lesson, except for the sections the cards cite and the changed passages of L19-L24.",
        "Not run: the full pytest suite, render_curriculum, fetch_data, verify_refs without --offline (no live access attempted), tools/build_site --check (outside slice e), and the rest of the M2 pages (other slices).",
        "Non-blocking observation: the reference grader computes bond prices in floats (v**t and round()), while project.html line 211 describes the price test as 'against an exact rational calculation'. An exact-rational engine (alt1) also passes 50/50, so no finding; the test expectations are still the page's claim.",
        "Two FAIL cards are low-severity wording/answer defects (M2-c058 front, M2-c285 back); the rest of the slice is clean. Round-11 FAIL rows (e-cards-correct about 'intermediate value property', e-cards-delta) are resolved.",
    ],
    "summary": "Slice e round 12: FAIL. Grader, project labs, project.html rubric, hours and the 85-test count all PASS on ff38842 (project.html, grader and project labs unchanged since f42f432, so their rows are carried, and the gates were re-run). Three new student-error grader mutants (r12_01..03) are killed, all 110 mutants are killed, and two alternative correct engines pass 50/50 seeds each. cards.json: the 13 changed cards agree with their lessons and the round-11 intermediate-value wording fix is in place, but two cards still fail: M2-c058 asks for the central-difference error of c(x) while its answer is c'(1.5), and M2-c285 asks for the s^2 coefficient but gives only g''(0) without the factor 1/2. Both are low severity; fix per e-cards-correct.",
}
out = ROOT / "ledgers" / "M2" / "M2-e.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, len(rows), "rows")
