"""Round-8 fragment builder for M2-e (verifier-authored). Writes ledgers/M2/M2-e.json."""
import json
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB8-M2-e")
S = "ledgers/M2/scripts/M2-e-r8/"
C = "Carried from round 7 (project.html lines {r} byte-identical since the previous pin 7aa909e; the only changed line of project.html is 226): "
G = "Carried from round 7 (course/modules/M/M2/grader/*.py and tests/labs/M2/lab-M2-project-{{1,2,3}}.py byte-identical since 7aa909e; verified by git diff --quiet): "

def carry(ranges, text):
    return C.format(r=ranges) + text

rows = [
 ("e-auto-run", "2.6-autograder-1", "course/modules/M/M2/grader/reference.py", "PASS",
  f"Re-run this round: `tools/run_graders.py --unit M2 --seeds 0-49` -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)' (exit 0; {S}run_graders.out). Reference copied as sensitivity_engine.py, `python -I -W error -m pytest --assert=plain test_project.py` -> 85 passed (ledgers/M2/scripts/M2-e-r8/pytest_ref_r8.out)."),
 ("e-auto-instances", "2.6-autograder-2", "course/modules/M/M2/grader/instance.py", "PASS",
  G + "round-7 evidence ledgers/M2/scripts/M2-e-r7/sin_ratio_r7.out (100 instances valid; 70 distinct x0; 100 of 100 distinct face values). Re-derived this round for the sin claim (see e-sin-ratio)."),
 ("e-mut-existing", "2.6-mutation-existing", "ledgers/M2/mutants/", "PASS",
  f"Re-run this round: `tools/mutate_graders.py --unit M2 --seeds 0-9` -> 'mutate_graders M2: PASS (96/96 killed)' (exit 0; {S}mutate_all_r8.log). Includes 86 earlier mutants, the five round-7 r7_* mutants and five new round-8 r8_* mutants."),
 ("e-mut-r6_01", "2.6-mutation-survivor", "course/modules/M/M2/grader/test_project.py:282-308", "PASS",
  G + f"KILLED by test_large_positive_step_is_accepted (re-run: {S}mutate_all_r8.log)."),
 ("e-mut-r6_02", "2.6-mutation-survivor", "course/modules/M/M2/grader/test_project.py:546-580", "PASS",
  G + f"KILLED by test_hessian_positive_step_is_accepted (re-run: {S}mutate_all_r8.log)."),
 ("e-mut-new-killed", "2.6-mutation-new", "ledgers/M2/mutants/r6_03*, r6_04*, r6_05*, r7_01*..r7_05*, r8_01*..r8_05*", "PASS",
  f"Own round-8 mutants (generator {S}make_mutants_r8.py, written into ledgers/M2/mutants/): r8_01 yield divided by 1000 (KILLED by test_price_is_the_half_even_rounding_of_the_exact_price); r8_02 Hessian diagonal without the -2f(x) term (KILLED by test_hessian_matches_the_analytic_hessian); r8_03 price returned as round(price, 2) float (KILLED by test_price_is_an_integer_number_of_cents); r8_04 final year dropped from the cash flows (KILLED by test_price_is_the_half_even_rounding_of_the_exact_price); r8_05 reflected subtraction sign error (KILLED by test_reflected_operators_are_defined). All r6_* and r7_* KILLED in the same log."),
 ("e-alternatives", "2.6-over-constraint", "course/modules/M/M2/grader/test_project.py", "PASS",
  f"Re-run this round against the current suite, seeds 0-49: altA (Richardson central, fsum forward, Fraction bond maths) 50/50; altB (Decimal at 400 digits, tuple dual) 50/50 ({S}run_alts_r8.out, {S}run_alts_r7.py); altC (new this round: math.fsum price, reordered Hessian mixed term, yield check written as < -9999 bp, int(round(..)) return) 50/50 ({S}run_alts_r8.out). Sources in /tmp/m2e_r8/alts/."),
 ("e-messages", "2.6-messages", "course/modules/M/M2/grader/test_project.py", "PASS",
  G + "round-7 reading of the added messages (lines 282-308, 546-580). The round-7 reading of the messages stands: the file is byte-identical, and no failure message names an expected value."),
 ("e-pyodide-local", "2.6-same-suite", "course/modules/M/M2/grader/test_project.py", "PASS",
  f"`tools/page_smoke.py --unit M2 --pages project` -> 'page_smoke M2: PASS' (exit 0; {S}page_smoke_project.out; 'All 85 tests pass on seed 1400071285'). Local pytest on the reference under -W error: 85 passed."),
 ("e-test-count", "2.6-test-count", "course/modules/M/M2/project.html:211", "PASS",
  f"Re-run: collected 85 tests (`pytest --collect-only -q`, {S}pytest_ref_r8.out) = the 85 printed at project.html:211."),
 ("e-valueerror-scope", "2.6-exceptions", "course/modules/M/M2/grader/test_project.py; course/modules/M/M2/project.html:225", "PASS",
  G + "project.html:225 unchanged."),
 ("e-scheme-types", "2.6-spec-accuracy", "course/modules/M/M2/project.html:211", "PASS",
  carry("211", "project.html:211 and test_project.py:338-348 unchanged; the scheme cases match the sentence.")),
 ("e-hours", "2.6-hours", "course/modules/M/M2/project.html:33, :239-245", "PASS",
  carry("33, 239-245", "the hub split and hour lines are unchanged.")),
 ("e-hours-arith", "2.6-hours-arith", "course/modules/M/M2/project.html:239-245", "PASS",
  carry("239-245", "arithmetic unchanged.")),
 ("e-ladder", "2.6-ladder", "course/modules/M/M2/project.html:40-48", "PASS",
  carry("40-48", "rung text unchanged.")),
 ("e-spec-questions", "2.6-spec-questions", "course/modules/M/M2/project.html:199-212", "PASS",
  carry("199-212", "specification questions unchanged.")),
 ("e-rubric-calibration", "2.6-rubric", "course/modules/M/M2/project.html:400-404, :418-507", "PASS",
  carry("400-404, 418-507", "rubric and calibration text unchanged.")),
 ("e-rubric-observable", "2.6-rubric-observable", "course/modules/M/M2/project.html:400 (C1 level 4), :404 (C5 level 3)", "PASS",
  carry("400, 404", "observable level text unchanged.")),
 ("e-rubric-adversarial", "2.6-rubric-adversarial", "course/modules/M/M2/project.html:395-407", "PASS",
  carry("395-407", "adversarial rubric text unchanged.")),
 ("e-atlas-studio", "2.6-atlas", "curriculum/meta.yaml; plans/M2-build-plan.md:22", "PASS",
  "curriculum/meta.yaml and plans/M2-build-plan.md unchanged since 7aa909e (git diff --quiet). Carried from round 7."),
 ("e-labs-run", "2.6-labs-run", "tests/labs/M2/lab-M2-project-{1,2,3}.py", "PASS",
  f"Re-run: `tools/run_labs.py --unit M2` -> 'run_labs M2: PASS (27/27)' (exit 0; {S}run_labs_M2.out). The three project twins are byte-identical since 7aa909e."),
 ("e-labs-page-twin", "2.6-labs-page-twin", "course/modules/M/M2/project.html:58, :107, :270, :350", "PASS",
  f"run_labs.py compares each page's lab code with its twin and each expected block with the twin output (lines 79-101 of tools/run_labs.py); re-run PASS 27/27 ({S}run_labs_M2.out)."),
 ("e-lab1-numbers", "2.6-lab1-numbers", "course/modules/M/M2/project.html:57, :116", "PASS",
  carry("57, 116", "lines and lab twin unchanged; the numbers are the lab output covered by run_labs PASS.")),
 ("e-lab2-numbers", "2.6-lab2-numbers", "course/modules/M/M2/project.html:121, :195", "PASS",
  carry("121, 195", "lines unchanged.")),
 ("e-lab3-numbers", "2.6-lab3-numbers", "course/modules/M/M2/project.html:267-377", "PASS",
  carry("267-377", "lines unchanged.")),
 ("e-lab3-interpretation", "2.6-lab3-interpretation", "course/modules/M/M2/project.html:377 (and the Lab 1 interpretation at :116)", "PASS",
  carry("116, 377", "lines unchanged.")),
 ("e-report-spec", "2.6-report-spec", "course/modules/M/M2/project.html:207, :270", "PASS",
  carry("207, 270", "lines unchanged.")),
 ("e-exemplar-numbers", "2.6-exemplar-numbers", "course/modules/M/M2/project.html:418, :429, :454, :470, :481, :494, :507", "PASS",
  carry("418-507", "exemplar lines unchanged.")),
 ("e-sin-ratio", "2.6-sin-ratio", "course/modules/M/M2/project.html:226", "PASS",
  f"Re-derived this round with {S}sin_ratio_r8.py over the 100 instance points (seeds 0-49 and seed+7919, 70 distinct x0): plain central quotient error ratio min 3.9999842, max 3.9999851 (output {S}sin_ratio_r8.out), matching project.html:226 'between 3.9999842 and 3.9999851, rounded to seven decimal places'."),
 ("e-formulas", "2.6-formulas", "course/modules/M/M2/project.html:214-227", "PASS",
  "Line 226 changed only by a line break and the cross-reference 'defined in the last subsection of this part' -> 'defined under What the suite does not check, below' (project.html:229 is that heading; Richardson is defined in line 230). Each tolerance on line 226 re-checked against test_project.py: 1e-6 at 151/195/678, 1e-9 at 301/367/377/388-434/579/702/706, 1e-5 at 472/501, 1e-4 at 691/783, 1e-6 at 484 (symmetry), 1e-6 at 778, 1e-9 at 702/706. Lines 214-227 otherwise byte-identical."),
 ("e-cards-correct", "2.6-cards-vs-lessons", "course/modules/M/M2/cards.json (379 cards); course/modules/M/M2/L01-L24.html", "UNVERIFIABLE",
  "NOT COMPLETE. Read in full against their lesson text this round: the 2 added cards M2-c388, c389 (theorem statements match L08 and L10 blocks exactly), the Lab 1 part A card (27 checks = 9 values of k times 3 values of x, matches the lab-M2-L07-1 output), c163 (matches L11 edited text), c187 (matches L13 Section 4 h*=(3 delta/M3)^(1/3)), c330/c331/c335 (g_y c_a matches L22 Proposition 2.1), c310 (hypotheses match L21 Theorem 1.2), c346 (ratio order matches lab-M2-L23-1 code), c326 (Remark 1.4 matches L22), c328 (ln a values match L22 lab output), c093, c103, c104, c084, c085. Also read the cards that cite changed lesson sentences (L08 Example 2.4, L11, L12, L16, L17, L20 Example 3.1 and Remark 2.3, L22, L23). Not read this round: the remaining ~300 cards against their lessons. Round-7 gave no per-card PASS, so nothing is carried. Per the rules, UNVERIFIABLE counts as FAIL."),
 ("e-cards-atomic", "2.6-cards-atomic", "course/modules/M/M2/cards.json: M2-c093, c194, c341, c345, c346", "PASS",
  "c194, c341, c345 byte-identical to round 7 (git diff 7aa909e..ce7b382 has no hunk on them). c093 and c346 re-read this round: c093 is one question (the closed form against the recursion); c346 is one question (the first-order error ratios). Removed in this round, so no longer atomic cards to check: c290, c344, c356."),
 ("e-cards-dup", "2.6-cards-dup", "course/modules/M/M2/cards.json", "PASS",
  f"{S}cards_check_r8.out: 379 cards, 379 unique ids, no duplicate ids. Normalized-front collision 'In Lab 1, what is P'(y0)/P''(y0) for the SIMULATED bond at y0 = 0.04' is two different questions (M2-c342 P', M2-c343 P''), not a duplicate."),
 ("e-cards-numbers", "2.6-cards-numbers", "course/modules/M/M2/cards.json", "PASS",
  "ledgers/M2/scripts/M2-e-r8/cards_check_r8.out: 14 number tokens (fractions such as 1/2, 1/6, 2/6) are not literal in their lesson text. Each is a TeX fraction in the raw lesson source (for example frac1 2 or tfrac 1 6 in L19, L23, L24) or, for c242, h^2/6 written as a TeX fraction with numerator h^2 and denominator 6 in L16. Checked against the raw lesson HTML."),
 ("e-cards-labels", "2.6-cards-labels", "course/modules/M/M2/cards.json: M2-c143, c144, c160, c180, c135, c137", "PASS",
  f"{S}cards_check_r8.out: 495 label references checked, 4 unmatched by the regex, all 'Section N' pointers; read by hand: c143 and c144 (L10 'Section 5' = 'Where the canon breaks', text matches), c160 (L11 'Section 4' = 'Where the canon breaks', text matches Example 3.2 limits), c180 (L12 'Section 4', text matches non-integer exponents). c135 (Theorem 2.1 in L10) and c137 (Corollary 3.1 in L10) exist."),
 ("e-cards-grades", "2.6-cards-grades", "course/modules/M/M2/cards.json", "PASS",
  f"{S}cards_check_r8.out: grades T 240, C 77 with basis, no grade 62 (the 62 cards carry no grade field; round 7 accepted this). No T card has a basis, no C card lacks one, no grade outside {{T, C}}."),
 ("e-data-figures", "2.6-data-figures", "course/modules/M/M2/project.html", "PASS",
  carry("57, 107, 355 (and figure data)", "figure and data lines unchanged; run_labs PASS.")),
 ("e-structure", "2.6-structure", "course/modules/M/M2/", "PASS",
  f"Re-run: `tools/check_pages.py --all` -> 'check_pages M2: PASS' ({S}check_pages.out); `tools/check_projects.py --all` -> 'check_projects M2: PASS'; `ruff check` and `ruff format --check` on course/modules/M/M2 and tests/labs/M2 -> all passed (ruff_check.out); `mypy --no-incremental` -> 'Success: no issues found in 255 source files'."),
 ("e-banned-phrases", "2.6-banned-phrases", "course/modules/M/M2/*.html, cards.json", "PASS",
  f"{S}banned_scan_r8.py over L01-L24, project.html and cards.json: the process-word patterns (round, verifier, builder, revised, corrected, fixed in, was added, changed, draft, placeholder, TODO, lorem, for brevity, clearly, obviously, simply, just, indeed) have no hit in the changed sentences; the remaining hits are ordinary mathematics or navigation text (out {S}banned_scan_r8.out)."),
 ("e-dag", "2.6-dag", "course/modules/M/M2/", "PASS",
  f"Re-run: `tools/check_dag.py --all` -> 'check_dag M2: PASS' ({S}check_dag.out). The newly cited lessons are earlier than the citing lesson (Lesson 9 before L11/L12, Lesson 13 before L16/L19, Lesson 21 before L22)."),
 ("e-notation", "2.6-notation", "notation/notation.json; course/modules/M/M2/", "PASS",
  "notation/notation.json holds 8 registry symbols (T, Phi, gamma_3, R*, ...). None occurs in the changed lines. The new symbols in changed lines (L(f,P) in L12, g and c in L22, G(a,x) in L22 Remark 1.4, M in L08 Example 2.4) are not registry symbols, and each is defined in its own lesson."),
 ("e-citations", "2.6-citations", "course/modules/M/M2/project.html:547-551", "PASS",
  carry("547-551", "lines unchanged.")),
 ("e-hours-declared-spec", "2.6-hours-declared", "course/modules/M/M2/project.html:35", "PASS",
  carry("35", "line unchanged.")),
 ("e-cards-delta-removed", "2.6-cards-removed", "course/modules/M/M2/cards.json: M2-c290, c344, c356 (removed)", "PASS",
  "grep -rl for M2-c290, M2-c344 and M2-c356 over course, plans, curriculum, tools, tests, references and notation: no hits. Removal leaves L19 with 14 cards and L23 with 23 cards (cards_check_r8.out)."),
]

out_rows = [{"id": i, "check": c, "location": l, "status": s, "evidence": e} for i, c, l, s, e in rows]

frag = {
    "unit": "M2",
    "slice": "e",
    "round": 8,
    "verifier": "independent verifier (Haiku 5.5), slice e",
    "pin": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089",
    "base": "previous pin 7aa909e95b757b1abf7b75186d5fa1ed7d1945a4 (round 7); round-7 fragment /Users/billyribeiro/.fanout/frags/B-M2-e.round7.json",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-M2-e",
    "scratch": "/tmp/m2e_r8",
    "verified_at": "2026-10-28T00:00:00Z",
    "verdict": "FAIL",
    "rows": out_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [],
    "summary": "",
}

frag["mutants"] = [
    {"name": "r8_01_yield_divided_by_one_thousand.py", "description": "_yield_rate divides basis points by 1000 instead of 10000", "killed_by": "test_price_is_the_half_even_rounding_of_the_exact_price (seed 0)"},
    {"name": "r8_02_hessian_diagonal_drops_factor_two.py", "description": "hessian_fd diagonal is (f(x+h) - f(x) + f(x-h)) / h^2", "killed_by": "test_hessian_matches_the_analytic_hessian (seed 0)"},
    {"name": "r8_03_price_returned_as_rounded_float.py", "description": "bond_price_cents returns round(price, 2), a float", "killed_by": "test_price_is_an_integer_number_of_cents (seed 0)"},
    {"name": "r8_04_cash_flows_stop_one_year_early.py", "description": "_cash_flows omits the final year", "killed_by": "test_price_is_the_half_even_rounding_of_the_exact_price (seed 0)"},
    {"name": "r8_05_reflected_subtraction_sign_error.py", "description": "_Dual.__rsub__ keeps the sign of the derivative", "killed_by": "test_reflected_operators_are_defined (seed 0)"},
]
frag["registry_flags"] = []
frag["freshness_flags"] = ["cards.json changed since round 7: 11 card objects changed (c093, c163, c187, c310, c330, c335, c388 added, c389 added, c290/c344/c356 removed); project.html changed only at line 226 and in the Richardson cross-reference"]
frag["notes"] = [
    "Grader, instance and project lab twins are byte-identical to the round-7 pin 7aa909e; their rows are carried where the cited subject is unchanged, and the command rows were re-run this round.",
    "Round-8 fresh mutants: 5 (r8_01..r8_05), all KILLED; all 96 mutants killed by tools/mutate_graders.py --unit M2 --seeds 0-9.",
    "Alternatives: altA, altB (carried from round 7) and altC (new) pass 50/50 seeds each against the current suite.",
    "Cards: the full read of all 379 cards against their lesson text was not completed in this round; e-cards-correct stays UNVERIFIABLE.",
    "Lesson-side changes (L08, L11, L12, L13, L16, L17, L19, L20, L22, L23, L24 not in slice) were read only where a slice card cites the changed sentence; the L08 lab twin change and the L13 twin change are outside slice e.",
]
frag["summary"] = "Slice e round 8: FAIL. 44 rows: 43 PASS (fresh or carried with prefix), 0 FAIL, 1 UNVERIFIABLE (e-cards-correct: the full card-against-lesson read of 379 cards is not complete). All grader, mutation, alternative, labs, page, DAG, structure and sin-ratio commands pass on the pin."
for r in frag["rows"]:
    if r["status"] != "PASS":
        r["fix"] = ("Read every card in cards.json against the text of its lesson (L01-L24) and record a row per card batch; "
                    "for each card that disagrees with its lesson, edit the card in curriculum/ or the lesson source and regenerate. "
                    "Not a grader or lab defect.")
import sys
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402
errs = ledger.validate(frag, "M2-e")
print("validate:", errs)
out = ROOT / "ledgers/M2/M2-e.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n")
print("rows", len(frag["rows"]), "statuses", {s: sum(1 for r in frag["rows"] if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")})
