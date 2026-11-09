"""Build ledgers/E5/E5-d.json (round 1, closing delta, verifier K1) from the base fragment H-E5-d.round1.json.

Rows whose cited subject changed between d9de2fe5 and f117a7a0 are re-verified here (fresh evidence text cites
k1out/ outputs). All other rows keep their id and check and are carried with the carry prefix. No row is FAIL.
"""
import json, sys

BASE = "/Users/billyribeiro/.fanout/frags/H-E5-d.round1.json"
OUT = "ledgers/E5/E5-d.json"
base = json.load(open(BASE, encoding="utf-8"))
O = "ledgers/E5/scripts/E5-d-r1/k1out/"

CARRY = "Carried from round 1 (the cited files and card entries byte-identical since the previous pin d9de2fe5; the delta changed only L02.html lines 269, 281, 405, cards.json line 230 (E5-c033) and the mutant moves): "

FRESH = {
    "proj-lab2-gap-survivor": (
        "project.html line 45 (Rung 2) says the instant check 'does not separate the log gap from the percent-of-trend gap ... and both print -0.18 at 2026 Q3, so a percent-of-trend line passes it'. "
        "Fresh at f117a7a0: ledgers/E5/scripts/E5-d-r1/k1_equiv.py (output " + O + "equiv_check.out) runs the two moved mutants ledgers/E5/equivalent/m02_gap_percent_of_trend.py and ledgers/E5/equivalent/r4_m05_gap_percent_of_trend.py with -I -W error against the lab-2 expected block (project.html line 306): both print 'growth 0.21, inflation 1.90, term spread 0.83, output gap (%): -0.18' and both return PASSES_CHECK. "
        "Independent recompute: log gap -0.183842, percent-of-trend gap -0.183673 (both -0.18 to two decimals), matching project.html line 62 and line 307. The two survivors are no longer under ledgers/E5/mutants/ (ruling 9, ruling 41)."),
    "proj-lab2-gap-survivor-doc": (
        "ledgers/E5/equivalent/README.md quotes project.html line 45 and says the two mutants 'violate no behaviour the check promises'. Fresh: line 45 text matches the quotation; k1_equiv.py output (" + O + "equiv_check.out) confirms both mutants pass the instant check. "
        "git diff -M d9de2fe5..f117a7a0 shows the two files as pure renames (0 changed lines) from ledgers/E5/mutants/project-2/m02_gap_percent_of_trend.py and ledgers/E5/mutants/project-2-r4/r4_m05_gap_percent_of_trend.py into ledgers/E5/equivalent/. The README's evidence path ledgers/E5/scripts/E5-d-r5/out/mutants_r5.out exists (ls) and was not re-run."),
    "proj-lab2-student-errors": (
        "Fresh standing run (run_standing_mutants.py, compare_output tolerance 1e-6 against project.html lab-2 expected block): " + O + "standing_mutants.out, total 19 files under ledgers/E5/mutants/project-2*. "
        "14 student-error mutants KILLED (each line in the mutants list below). 5 correct alternatives PASSES_CHECK: project-2-r4/alt01_statistics_linear_regression.py, project-2-r4/alt02_spread_rounded_inputs.py, project-2/alt/alt01_index_from_one.py, alt02_statistics_module.py, alt03_gap_via_ratio_log.py. No survivor remains under ledgers/E5/mutants/."),
    "proj-adversarial-and-mutants": (
        "project.html #spec Grading mode (line 323) unchanged. Fresh: tools/mutate_graders.py --unit E5 exit 0 with no mutant output (" + O + "mutate_graders_E5.out); the standing lab-2 set (" + O + "standing_mutants.out) gives 14 killed and 5 alternatives PASSES_CHECK; ledgers/E5/mutants/ holds no survivor and ledgers/E5/equivalent/ holds the two README-justified files (ruling 41). No new mutants were authored (ruling 37)."),
    "cards-c032-basis-vs-key-row": (
        "Fresh: cards.json E5-c032 (line 219 block; basis 'Proposition 2.4; Definition 2.1', grade T) is unchanged. L02.html Definition 2.1 (line 96), Proposition 2.4 (lines 120-123) and the key-results row 406 ('In each period the residual changes ... Proposition 2.4; Lab 1 averages') are unchanged, so the card still matches its lesson. Grades agree (T). The basis strings differ (card: Definition 2.1; row: Lab 1 averages); this is the same observation as the base round, not a FAIL kind under ruling 26."),
    "cards-changed-c033": (
        "cards.json line 230 (E5-c033 back, the only changed card): 'Theorem 2.3 identifies the residual with TFP growth only inside the model of Assumption 1.3, when the chosen alpha is the economy's own alpha, where A is known.' "
        "L02.html Theorem 2.3 (line 108) is stated 'computed with the alpha of the economy', so the added condition is the theorem's own hypothesis, now written out; the proof (Theorem 1.4 with the same alpha by Assumption 1.3) supports it. Grade T matches the lesson's T. Basis 'Definition 2.1; Proposition 2.4; Theorem 2.3' matches the lesson. No new number. Not an over-grade, no missing hypothesis."),
    "cards-c034-missing-hypothesis": (
        "Fresh: cards.json E5-c034 (line 235) unchanged; L02.html Proposition 2.4 (line 120-123) and the second misconception (lines 284-285) unchanged (git diff -U0 hunks are 269, 281, 405 only). The card's claim, that the average residual depends on alpha whenever average capital and labour growth differ, is Proposition 2.4's own statement; grade T and basis match."),
    "cards-changed-c032-c040-c099-grade-basis": (
        "cards.json: git diff -U0 d9de2fe5..f117a7a0 -- course/modules/E/E5/cards.json shows one hunk, @@ -230 +230 @@, i.e. only E5-c033's back changed. E5-c032 (line 219), E5-c034 (235), E5-c040 and E5-c099 are byte-identical; their grade and basis fields are unchanged. E5-c033 grade T and basis 'Definition 2.1; Proposition 2.4; Theorem 2.3' agree with L02.html (see cards-changed-c033)."),
    "lessons-delta-hunks": (
        "git diff -U0 d9de2fe5..f117a7a0 -- course/modules/E/E5/L02.html: hunks at lines 269, 281, 405 only (this delta). Line 269 (Where the canon breaks) and line 281 (misconception 1) add 'with the chosen alpha equal to the economy's own alpha', restating Theorem 2.3's hypothesis (L02.html line 108-110); line 405 (key-results row) adds the same condition to the T row. "
        "No new number, claim or grade; the Lab 1 numbers quoted in misconception 1 (line 283) and the interpretation (line 262) are reproduced by the twin: " + O + "lab_L02_twin.out (exit 0) prints average residual 0.016254 at alpha 0.2 and 0.010665 at alpha 0.4. Other hunks of the previous delta are not in this delta."),
    "cards-delta-coverage": (
        "cards.json: exactly one changed entry in this delta (E5-c033 back, line 230). No card added or removed. Python check (json load): 140 cards, 140 unique ids, 0 duplicate fronts. Changed card's lesson (L02) and its grade match the lesson's T."),
    "cards-lab-numbers": (
        "E5-c033 back contains no lab number (checked: text is in the cards-changed-c033 row). Other listed cards are carried; the lab numbers they cite are reproduced fresh: tests/labs/E5/lab-E5-L02-1.py output " + O + "lab_L02_twin.out lists average log growth 0.029453, shares 0.362162 / 0.180872 / 0.456966, average residual 0.016254 and 0.010665, and the simple-growth average 0.029907 that L02 lines 262 and 359 quote. Misconception 3 numbers (1.1**0.3 = 1.029006, simple 0.029006, 0.3 ln 1.1 = 0.028593, weighted 0.030000) re-derived with python -I."),
    "cards-scope-and-duplicates": (
        "cards.json: 140 cards, 140 unique ids and 0 duplicate fronts (python -I json check, this round). The changed back of E5-c033 uses 'only inside the model of Assumption 1.3'; the scope is the model (the same as Theorem 2.3's hypothesis), not a universal claim. No new scope words beyond that."),
    "cards-numbers-in-lesson": (
        "The changed E5-c033 back (cards.json line 230) contains no numeric value, so no number in it needs a lesson match. Other cards carried."),
    "cards-remark-labels": (
        "Fresh: the changed line (cards.json line 230) carries no 'Remark' label in its basis or back; git diff of the hunk shows only the phrase change. L02.html has no Remark label added (git diff of L02.html shows no Remark token)."),
    "proj-process-words": (
        "Fresh: check_pages.py --all (" + O + "check_pages.out) reports E5: PASS, which includes the banned-string scan. Changed text scanned: git diff d9de2fe5..f117a7a0 -- course/modules/E/E5 added lines grep -i for ruling, round, verif, fix, blind, architect, delta, closing, pin, ledger, mutant, fragment, slice, reviewer, audit, todo, tbd returns only 'input', 'own' and 'Delta' inside the new sentences (no process word)."),
    "proj-dag": (
        "Fresh: check_dag.py --all (" + O + "check_dag.out): 'check_dag E5: PASS'. The changed L02 sentences add no concept name or link (no new <a class=\"concept\">, no new <dfn>); course/concepts.html unchanged since d9de2fe5 (not in git diff)."),
    "cmd-check-pages": "Fresh: tools/check_pages.py --all (" + O + "check_pages.out): 'check_pages E5: PASS' and every unit PASS, exit 0.",
    "cmd-check-dag": "Fresh: tools/check_dag.py --all (" + O + "check_dag.out): 'check_dag E5: PASS', every unit PASS, exit 0.",
    "cmd-check-projects": "Fresh: tools/check_projects.py --all (" + O + "check_projects.out): 'check_projects E5: PASS', every unit PASS, exit 0.",
    "cmd-run-labs": "Fresh: tools/run_labs.py --unit E5 (" + O + "run_labs_E5.out): 'run_labs E5: PASS (11/11)', exit 0. L02 twin also run alone under python -I -W error (" + O + "lab_L02_twin.out), exit 0; project-2 twin run alone under -I -W error exit 0.",
    "cmd-page-smoke-project": "Fresh: tools/page_smoke.py --unit E5 (" + O + "page_smoke_E5.out): 'page_smoke modules/E/E5/project.html: PASS' with lab-E5-project-1, -2, -3 runtimes; exit 0.",
    "cmd-page-smoke-changed-pages": "Fresh: tools/page_smoke.py --unit E5 (" + O + "page_smoke_E5.out): PASS for L01 to L08, index.html and project.html (L02.html is the changed page), 'page_smoke E5: PASS', exit 0.",
    "cmd-pytest": "Fresh (relevant subsets, not the whole tests/ suite): pytest tests/test_labs.py -k E5 (" + O + "pytest_labs_E5.out), test_memo_exemplars.py, test_page_checks.py, test_page_smoke.py, and test_curriculum.py with test_docs_figures.py: each exit 0 with 100% dots (outputs under " + O + "pytest_*.out).",
    "cmd-verify-refs": "Fresh: tools/verify_refs.py --offline (" + O + "verify_refs_offline.out): 'offline integrity: 560 entries, 0 problems', exit 0.",
    "cmd-ruff-mypy": "Fresh: ruff check . ('All checks passed!', " + O + "ruff_check.out); ruff format --check . ('555 files already formatted', " + O + "ruff_format.out); mypy --no-incremental ('Success: no issues found in 386 source files', " + O + "mypy.out). All exit 0.",
    "cmd-build-site": "Fresh: tools/build_site.py --check (" + O + "build_site_check.out): 'site data current: 6 outputs', exit 0.",
    "cmd-render-curriculum": "Fresh: tools/render_curriculum.py (" + O + "render_curriculum.out): 'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)', wrote curriculum/curriculum.json and CURRICULUM.md; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 (" + O + "render_diff.out).",
    "cmd-fetch-data": "Fresh: tools/fetch_data.py --check (" + O + "fetch_data_check.out): 'fetch_data: 3 datasets, 0 problems', exit 0.",
    "cmd-lab2-standing-mutants": "Fresh: run_standing_mutants.py over ledgers/E5/mutants/project-2* (" + O + "standing_mutants.out): total 19; 14 KILLED, 5 PASSES_CHECK (the alternatives). Equivalent files run separately in " + O + "equiv_check.out (both PASSES_CHECK, as the page's line 45 says).",
}

CMD_ALL = {"cmd-check-pages", "cmd-check-dag", "cmd-check-projects"}

rows = []
seen = set()
for r in base["rows"]:
    rid = r["id"]
    seen.add(rid)
    nr = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS"}
    if rid in FRESH:
        ev = FRESH[rid]
        nr["evidence"] = ev
    else:
        nr["evidence"] = CARRY + r["evidence"]
    if rid == "lessons-delta-hunks":
        nr["location"] = "course/modules/E/E5/L02.html lines 269, 281, 405 (this delta); L02.html line 108 (Theorem 2.3); line 262, 283, 359 (Lab 1 numbers)"
    if rid == "proj-lab2-gap-survivor":
        nr["location"] = "course/modules/E/E5/project.html line 45 (Rung 2), lines 62 and 306-307; ledgers/E5/equivalent/m02_gap_percent_of_trend.py, r4_m05_gap_percent_of_trend.py"
    if rid == "proj-lab2-gap-survivor-doc":
        nr["location"] = "ledgers/E5/equivalent/README.md; course/modules/E/E5/project.html line 45"
    if rid == "proj-lab2-student-errors":
        nr["location"] = "tests/labs/E5/lab-E5-project-2.py; ledgers/E5/mutants/project-2*/ (19 files)"
    if rid == "proj-adversarial-and-mutants":
        nr["location"] = "course/modules/E/E5/project.html #spec Grading mode (line 323); tests/labs/E5; ledgers/E5/mutants; ledgers/E5/equivalent"
    if rid == "cards-changed-c033":
        nr["location"] = "course/modules/E/E5/cards.json E5-c033 (line 230); course/modules/E/E5/L02.html Theorem 2.3 (line 108), Proposition 2.4 (line 120)"
    if rid == "cards-c032-basis-vs-key-row":
        nr["location"] = "course/modules/E/E5/cards.json E5-c032 (line 219); L02.html Definition 2.1 (line 96), Proposition 2.4, key-results row line 406"
    if rid == "cards-c034-missing-hypothesis":
        nr["location"] = "course/modules/E/E5/cards.json E5-c034 (line 235); L02.html Proposition 2.4 (line 120-123), misconception (lines 284-285)"
    rows.append(nr)
assert len(rows) == len(base["rows"]) == 80, len(rows)
assert set(FRESH) <= seen, set(FRESH) - seen

for rid in list(FRESH):
    if rid not in seen:
        raise SystemExit("unknown fresh id " + rid)

KILL = "KILLED fresh at f117a7a0: " + O + "standing_mutants.out, "
mut_specs = [
    ("r4_m01_spread_sign_reversed", "ledgers/E5/mutants/project-2-r4/r4_m01_spread_sign_reversed.py", "student error: spread sign reversed", "token 27: -0.83 differs from 0.83 beyond tolerance 1e-06"),
    ("r4_m02_spread_previous_quarter", "ledgers/E5/mutants/project-2-r4/r4_m02_spread_previous_quarter.py", "student error: spread taken from the previous quarter", "token 27: 1.01 differs from 0.83 beyond tolerance 1e-06"),
    ("r4_m03_gap_time_index_off_by_one", "ledgers/E5/mutants/project-2-r4/r4_m03_gap_time_index_off_by_one.py", "student error: gap trend read at an off-by-one time index", "token 31: -0.67 differs from -0.18 beyond tolerance 1e-06"),
    ("r4_m04_gap_trend_at_window_start", "ledgers/E5/mutants/project-2-r4/r4_m04_gap_trend_at_window_start.py", "student error: gap trend read at the window start", "token 31: 9.10 differs from -0.18 beyond tolerance 1e-06"),
    ("r5_m01_spread_sum_not_difference", "ledgers/E5/mutants/project-2-r5/r5_m01_spread_sum_not_difference.py", "student error: spread as a sum, not a difference", "token 27: 3.83 differs from 0.83 beyond tolerance 1e-06"),
    ("r5_m02_gap_growth_not_level", "ledgers/E5/mutants/project-2-r5/r5_m02_gap_growth_not_level.py", "student error: gap built from growth, not from the level", "token 31: 0.05 differs from -0.18 beyond tolerance 1e-06"),
    ("r5_m03_gap_trend_window_19", "ledgers/E5/mutants/project-2-r5/r5_m03_gap_trend_window_19.py", "student error: trend window of 19 quarters", "token 31: 0.30 differs from -0.18 beyond tolerance 1e-06"),
    ("m01_gap_intercept_only", "ledgers/E5/mutants/project-2/m01_gap_intercept_only.py", "student error: gap uses the trend intercept only", "token 31: 9.10 differs from -0.18 beyond tolerance 1e-06"),
    ("m03_gap_lagged_output", "ledgers/E5/mutants/project-2/m03_gap_lagged_output.py", "student error: gap uses lagged output", "token 31: -0.24 differs from -0.18 beyond tolerance 1e-06"),
    ("m04_gap_window_24", "ledgers/E5/mutants/project-2/m04_gap_window_24.py", "student error: trend window of 24 quarters", "token 31: -2.14 differs from -0.18 beyond tolerance 1e-06"),
    ("m05_spread_reversed", "ledgers/E5/mutants/project-2/m05_spread_reversed.py", "student error: spread sign reversed", "token 27: -0.83 differs from 0.83 beyond tolerance 1e-06"),
    ("m06_spread_fixed_offset", "ledgers/E5/mutants/project-2/m06_spread_fixed_offset.py", "student error: spread replaced by a fixed offset", "token 27: 0.80 differs from 0.83 beyond tolerance 1e-06"),
    ("m07_gap_sign_flipped", "ledgers/E5/mutants/project-2/m07_gap_sign_flipped.py", "student error: gap sign flipped", "token 31: 0.18 differs from -0.18 beyond tolerance 1e-06"),
    ("m08_gap_log10", "ledgers/E5/mutants/project-2/m08_gap_log10.py", "student error: gap uses log base 10", "token 31: -0.08 differs from -0.18 beyond tolerance 1e-06"),
]
BASE_DESC = {m["id"]: m["description"] for m in base["mutants"]}
for i, p, d, k in mut_specs:
    assert i in BASE_DESC and "SURVIVES" not in BASE_DESC[i], i
mutants = [{"id": i, "description": BASE_DESC[i], "killed_by": KILL + p.split("/")[-1] + " " + k} for i, p, d, k in mut_specs]

registry_flags = base["registry_flags"]
freshness_flags = [
    "ledgers/E5/scripts/E5-d-r5/ and ledgers/E5/mutants/project-2-r5/ are cited by earlier rounds; not re-run in this closing delta (only the lab-2 standing set was re-run).",
    "No E5 blind scorer file in ~/.fanout/blind/ (checked this round: the directory lists no E5 file, ruling 23): exemplar calibration is carried, not re-scored.",
    "ledgers/E5/equivalent/README.md cites ledgers/E5/scripts/E5-d-r5/out/mutants_r5.out as survival evidence; that file exists but was not re-run (the fresh run is " + O + "equiv_check.out).",
]

notes = [
    "Delta (ruling 30): git diff d9de2fe5..f117a7a0 over the E5 slice paths changed only course/modules/E/E5/L02.html (hunks at lines 269, 281, 405), course/modules/E/E5/cards.json (one hunk, line 230, card E5-c033 back), the two mutant moves into ledgers/E5/equivalent/ (pure renames, 0 changed lines) and ledgers/E5/equivalent/README.md (new). project.html, index.html, L01 and L03 to L08, the lab twins and the registry/tools/curriculum/notation paths are unchanged in this delta. Other units (E3, M2, M4, M6, CS2, E2, FC2, BK4) changed in the same range and are not in this slice.",
    "Ruling 41 verified: project.html line 45 states that the instant check does not separate the log gap from the percent-of-trend gap and that both print -0.18 at 2026 Q3. Fresh run (" + O + "equiv_check.out): both moved mutants PASSES_CHECK against the lab-2 expected block; recompute log gap -0.183842 and percent gap -0.183673, matching project.html lines 62 and 307. The move to equivalent/ with the README is accepted under ruling 41. The ledger lists only the 14 mutants the check kills, each with fresh killed_by evidence; the merged verdict is no longer blocked by a survivor.",
    "Ruling 37: no new mutants were authored in this closing round. The standing set was re-run: 14 killed and 5 correct alternatives PASSES_CHECK (" + O + "standing_mutants.out, total 19).",
    "Ruling 26 kinds checked on the changed text: no false or unproved statement (the added condition 'with the chosen alpha equal to the economy's own alpha' restates Theorem 2.3's hypothesis, 'computed with the alpha of the economy', and the proof uses Theorem 1.4 with the same alpha); no missing hypothesis; no wrong number (Lab 1 numbers and misconception 3 numbers re-derived; " + O + "lab_L02_twin.out); no over-graded claim (grades unchanged, T for the theorem-level rows); no failing gate; no surviving non-equivalent mutant; no lab statement the code does not support. No FAIL row was found.",
    "Observations carried, not FAIL: (a) E5-c032 basis 'Proposition 2.4; Definition 2.1' differs from the key-results row 406 basis 'Proposition 2.4; Lab 1 averages' (grades agree, T); (b) project.html line 42 'If you pass the placement check on the module page' does not name the bar or the two skill checks (index line 72); (c) card E5-c040 answers 'No' to 'Is zero a steady state' while stating that zero is a fixed point (correct under Definition 2.1, k* > 0); (d) i^{\\ast} is the IS-LM rate in L04 and the Taylor-rule value in the project and is not in notation/notation.json (registry flag, Architect).",
    "Gates re-run at f117a7a0 (all exit 0): ruff check, ruff format --check, mypy --no-incremental (386 files), check_pages --all, check_dag --all, check_projects --all (E5 PASS in each), run_labs --unit E5 (11/11), page_smoke --unit E5 (L01-L08, index, project PASS), render_curriculum with git diff --exit-code (clean), build_site --check, verify_refs --offline (560 entries, 0 problems), fetch_data --check (3 datasets, 0 problems), mutate_graders --unit E5 (exit 0, no E5 grader output), pytest subsets (test_labs -k E5, test_memo_exemplars, test_page_checks, test_page_smoke, test_curriculum with test_docs_figures), standing lab-2 mutants. Outputs under ledgers/E5/scripts/E5-d-r1/k1out/.",
    "Observation (not a ruling-26 kind, not changed in this delta): most mutant files under ledgers/E5/mutants/project-2* open with the generic line 'Rung 2 completed solution' instead of naming the student error as ruling 9 asks; the files were not changed since d9de2fe5, so this is carried for the Architect, not a FAIL here. The ledger descriptions name the error.",
    "Calibration (ruling 23): no E5 blind scorer file exists in ~/.fanout/blind/, so the base calibration rows (proj-calib-exA-blind, proj-calib-exB) are carried, not re-scored. Exemplar A's score and verdict text are unchanged in this delta.",
    "Not checked: the whole tests/ suite (only the relevant subsets listed above); run_graders --all --seeds 0-49 (no E5 project grader change in this delta; not run); plain-curl access checks to the H.15 licence page (the verify_refs offline integrity passed; not repeated); L01 and L03 to L08 prose outside the hunks (carried); exemplars were not re-scored blind.",
]

summary = ("E5-d closing delta round 1 (verifier K1), pin f117a7a0, base d9de2fe5: %d rows, all PASS. Changed hunks in L02 (3), card E5-c033 and the two mutant moves were re-verified from scratch; every gate re-run exits 0. "
           "Ruling 41 applied: the two percent-of-trend mutants live in ledgers/E5/equivalent/ and the ledger lists the 14 mutants the instant check kills, each with fresh killed_by evidence. No new mutants (ruling 37).") % len(rows)

frag = {
    "unit": "E5",
    "slice": "E5-d",
    "round": 1,
    "verifier": "Claude Haiku 5.5, independent closing-delta verifier K1 for E5-d, round 1 (ruling 30, 37, 41; did not build E5)",
    "pin": "f117a7a0",
    "base": "d9de2fe5 (round-1 fragment ~/.fanout/frags/H-E5-d.round1.json, all 80 rows PASS)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyK1-E5-d",
    "scratch": "ledgers/E5/scripts/E5-d-r1/k1out (outputs); ledgers/E5/scripts/E5-d-r1/k1_gates.sh, k1_equiv.py, k1_build_fragment.py (scripts)",
    "verified_at": "2026-11-09",
    "verdict": "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": summary,
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OUT, "a", encoding="utf-8").write("\n")
print("wrote", OUT, "rows", len(rows), "mutants", len(mutants), "fresh", len(FRESH))
