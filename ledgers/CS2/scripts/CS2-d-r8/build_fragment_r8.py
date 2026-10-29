"""Round-8 verifier script: writes the CS2 slice d fragment (ledgers/CS2/CS2-d.json)."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB8-CS2-d")
S = "ledgers/CS2/scripts/CS2-d-r8"
C7 = "Carried from round 7 (grader/test_project.py, grader/instance.py, grader/reference.py, tests/labs/CS2 byte-identical since the previous pin 7aa909e): "
rows = [
 ("D-01", "2.1 citations: registry key used by project.html", "course/modules/CS/CS2/project.html:411-413; references/references.json", "PASS",
  C7 + "lines 411-413 and references/ unchanged by the delta. Re-run round 8: tools/verify_refs.py --offline -> 560 entries, 0 problems (ledgers/CS2/scripts/CS2-d-r8/verify_refs.out)."),
 ("D-02", "2.5 labs: Lab 1 prose and printed numbers", "course/modules/CS/CS2/project.html:55,145,389; tests/labs/CS2/lab-CS2-project-1.py", "PASS",
  C7 + "lines 55, 145, 389 outside the delta hunks. Re-run round 8: run_labs --unit CS2 PASS (14/14); twin output 'deque operations: 44 ... bound 4n = 48' matches the page."),
 ("D-03", "2.2 numbers: Lab 2 prose and expected output", "course/modules/CS/CS2/project.html:185-188; tests/labs/CS2/lab-CS2-project-2.py", "PASS",
  C7 + "lines 185-188 unchanged. Re-run round 8: run_labs CS2 PASS (14/14)."),
 ("D-04", "2.2 numbers: Lab 3 prose and expected output", "course/modules/CS/CS2/project.html:329-338; tests/labs/CS2/lab-CS2-project-3.py", "PASS",
  C7 + "lines 329-338 unchanged. Re-run round 8: run_labs CS2 PASS (14/14)."),
 ("D-05", "2.6 spec: the ten named ValueError conditions each have a test", "course/modules/CS/CS2/project.html:209; grader/test_project.py", "PASS",
  C7 + "the named list (1)-(10) in project.html:209 is unchanged; the delta edits only the infinite-value sentences (see D-33)."),
 ("D-06", "2.6 spec: value and window rules of Constraints", "course/modules/CS/CS2/project.html:209; grader/test_project.py", "PASS",
  C7 + "the value and window sentences of project.html:209 are unchanged; only the infinite-value sentences moved (D-33)."),
 ("D-07", "2.6 grader: documented test count equals collect-only count", "course/modules/CS/CS2/project.html:211; grader/test_project.py", "PASS",
  "Round 8: reference.py copied as streamstats.py into a fresh temp dir; pytest --collect-only -q on QF_SEED 0, 17, 49 -> '170 tests collected' each; the page says 170 (line 211). Full suite on seed 0: 170 passed (--assert=plain -W error)."),
 ("D-08", "2.2 numbers: rank-target example in Conventions", "course/modules/CS/CS2/project.html:219; grader/test_project.py", "PASS",
  C7 + "line 219 unchanged; round-7 probe ledgers/CS2/scripts/CS2-d-r7/spec_probes_r7.py: float ceil 1, exact 2."),
 ("D-09", "2.2 numbers: instance.py docstring naive-formula counts", "course/modules/CS/CS2/grader/instance.py:8-13", "PASS",
  C7 + "round-7 instances_r7.py result (0/16, 22/23, 11/11) for the docstring's formula order."),
 ("D-10", "2.6 instances: ranges stated on the page and in the docstring", "course/modules/CS/CS2/project.html:198; grader/instance.py:27-50", "PASS",
  C7 + "line 198 unchanged; round-7 instances_r7.py: n 20-400, window 2-30, eps in {0.05, 0.1, 0.2}, all values finite."),
 ("D-11", "2.6 autograder: reference passes and starter fails", "course/modules/CS/CS2/grader/reference.py; grader/starter.py", "PASS",
  "Round 8: run_graders --unit CS2 PASS (reference 50/50 seeds, slowest 0.3 s) (ledgers/CS2/scripts/CS2-d-r8/run_graders.out). Starter-fails part carried from round 7 (starter.py byte-identical)."),
 ("D-12", "2.6 reference: rank guarantee beyond the suite", "course/modules/CS/CS2/grader/reference.py:94-143", "PASS",
  C7 + "reference.py exact-rank check, round 8 ledgers/CS2/scripts/CS2-d-r8/guarantee_probe_r8.py: 19,500 exact checks, 0 violations."),
 ("D-13", "2.6 reference docstring claims (sketch invariants)", "course/modules/CS/CS2/grader/reference.py:95-101", "PASS",
  C7 + "reference.py unchanged."),
 ("D-14", "2.6 five alternative correct implementations pass (over-constraint)", "ledgers/CS2/scripts/CS2-d-r8/alts/*; ledgers/CS2/scripts/CS2-d-r7/alts/*", "PASS",
  "Round 8: alts_run_r8.py on 4 new full modules (alt_r8_01 two-pass fsum, alt_r8_02 float/str window coercion, alt_r8_03 delta-squared identity spliced into reference, alt_r8_04 exact stored-rank sketch spliced into reference) and 6 round-7 alternatives (alt_r7_06 with its B7 reference path changed to this checkout): each passes 50/50 seeds (ledgers/CS2/scripts/CS2-d-r8/alts_run_r8.out.txt and rerun output)."),
 ("D-15", "2.6 mutation: every grader mutant killed; at least three new mutants", "ledgers/CS2/mutants/ (86 prior + d8_01..d8_04); ledgers/CS2/scripts/CS2-d-r8/mutate_all_r8.out.txt", "FAIL",
  "Round 8: tools/mutate_graders.py --unit CS2 -> 'FAIL (87/90 killed)'. All 86 prior mutants killed. Survivors: d8_04_quantile_rounds_q_to_six_places.py (a real grader gap, see D-37); d8_01 and d8_02 survive but do not violate the guarantee (19,500 exact checks, 0 violations each), so they are not wrong solutions. Fix: kill d8_04 by the D-37 change; no change needed for d8_01/d8_02."),
 ("D-16", "gates on the grader and lab files", "tests/labs/CS2; course/modules/CS/CS2/grader", "PASS",
  "Round 8: ruff check tests/labs/CS2 course/modules/CS/CS2/grader -> exit 0; ruff format --check tests/labs/CS2 -> 14 files already formatted; mypy --no-incremental tests/labs/CS2 -> Success, 14 source files."),
 ("D-17", "2.5 labs: run alone under -I -W error, page equals twin, expected equals output", "tests/labs/CS2/lab-CS2-project-1..3.py; course/modules/CS/CS2/project.html:53-146, 262-337", "PASS",
  "Round 8: run_labs --unit CS2 -> PASS (14/14); run_labs checks the twin under python -I -W error, page code equal to twin, expected block equal to output."),
 ("D-18", "gates: check_projects, check_pages, check_dag, page_smoke (project)", "course/modules/CS/CS2/project.html", "PASS",
  "Round 8: check_projects --unit CS2 PASS; check_pages --unit CS2 PASS (and --all PASS; --page takes a page stem, the project page is checked by check_common); check_dag --unit CS2 PASS; page_smoke --unit CS2 --pages project PASS (ledgers/CS2/scripts/CS2-d-r8/page_smoke_project_r8.out.txt)."),
 ("D-19", "2.6 hours: arithmetic and estimate", "course/modules/CS/CS2/project.html:33, 233-241; course/modules/CS/CS2/index.html (data-hours-lessons)", "PASS",
  "Round 8: rung 1 2 + rung 2 3 + Welford 4 + proof 4 + deque 4 + sketch 6 + API 4 + note 3 = 30 (= data-hours-project 30, project.html:33). index.html data-hours-lessons=100; 100 + 30 = 130 (plan line 93)."),
 ("D-20", "2.6 rubric: observable descriptors and exemplar calibration", "course/modules/CS/CS2/project.html:348-391", "PASS",
  "Round 8: rubric rows C1-C6 (project.html:352-357) are unchanged by the delta; exemplar scores (data-scores) match the printed official scoring. The symbol mismatch in C2/C3 is recorded at D-36."),
 ("D-21", "2.2 numbers quoted in exemplars", "course/modules/CS/CS2/project.html:372, 383-390", "PASS",
  "Round 8: 8.313636 (Lab 3 exact sample variance), 10003.2 (5th smallest), 44 deque operations and bound 4n = 48 (Lab 1), 'True' for the 1e-9 agreement (Lab 3) all match course/modules/CS/CS2 project expected blocks (run_labs output). Exemplar B proof algebra re-derived: (n + n^2)/(n+1)^2 = n/(n+1); delta*(x_{n+1} - mean_{n+1}) = n delta^2/(n+1)."),
 ("D-22", "2.4 notation: symbols against notation/notation.json", "course/modules/CS/CS2/project.html; notation/notation.json", "PASS",
  "Round 8: registry has 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q); grep of CS2 pages for these returns nothing. Symbols used on the page (n, q, epsilon, S, delta, x-bar, R(v), R^-(v)) are not registered; notation.json lists S and m as conventionally local."),
 ("D-23", "2.9 terms and symbols defined before use: epsilon in the rank guarantee", "course/modules/CS/CS2/project.html:198, 209, 218", "PASS",
  "Round 8: epsilon is introduced as the sketch's epsilon in Inputs (198) and Constraints (209) and given its meaning in the rank guarantee (218, under Conventions). The lede's '(defined under Conventions below)' points to line 218, which defines the guarantee."),
 ("D-24", "2.9 cross-links: placement bar and rung 3", "course/modules/CS/CS2/project.html:42, 161; course/modules/CS/CS2/index.html:69-71, 161", "PASS",
  C7 + "project.html:42 unchanged; index.html unchanged by the delta."),
 ("D-25", "2.6 tooling claims on the page", "course/modules/CS/CS2/project.html:249, 257; requirements-dev.txt:2; course/assets/js/grader.js", "PASS",
  C7 + "lines 249 and 257 unchanged; requirements-dev.txt and grader.js unchanged."),
 ("D-26", "2.9 footer claim: nothing leaves the browser", "course/modules/CS/CS2/project.html:426", "PASS",
  C7 + "line 426 unchanged."),
 ("D-27", "2.7 cards: structure, ids, grades, lesson coverage", "course/modules/CS/CS2/cards.json (207 cards)", "PASS",
  "Round 8: cards.json has 207 cards (round 7 recorded 167; 40 added c168-c207, 28 changed). ids c001-c207 sequential, no duplicate ids, keys {id, lesson, front, back, grade, basis?}, grades T (134 -> recount in ledgers/CS2/scripts/CS2-d-r8/cards_dump.txt) and C; all eleven lessons L01-L11 carry cards; C cards carry basis, the one T card with a former basis (c126) has none."),
 ("D-28", "2.7 cards: every C-grade number against printed lab output", "course/modules/CS/CS2/cards.json (C cards); ledgers/CS2/scripts/CS2-d-r8/text/L*.expected.txt", "FAIL",
  "CS2-c124 (L09): back says 'the exact sample variance is 0.0872811'. The printed Lab 1 output (L09.expected.txt lines 1, 5, 9) prints 'exact sample variance 0.087281' (6 d.p.); 0.0872811 appears only in lesson prose (L09.txt, the Lab 1 paragraph). Fix: write 0.087281 as printed. Other flagged numbers were checked by hand and match printed values or exact arithmetic on them: c038 (205 = 107+98, 602 = 241+361, 19140 = 8517+10623, 21405 = 3742+17663), c098 (30+30), c155 (257/128, 772/256), c193/c196/c197 (ratios 7.87, 1.60e8, 1.34e7), c125 ('1.3' is a lemma number)."),
 ("D-29", "2.7 cards: T-grade statements agree with the current lesson text", "course/modules/CS/CS2/cards.json (T cards); course/modules/CS/CS2/L01-L11.html", "FAIL",
  "INCOMPLETE, not a found defect. Round 8 read every changed or new card against its lesson (L02 c022-c025, c155-c158, c168-c171; L03 c033-c039, c159, c172-c175; L05 c059-c069, c164, c178-c185; L06 c075, c079-c082, c160, c186; L08 c100-c115, c162-c163, c187-c192; L09 c116-c127, c193-c197; L10 c128-c139, c154, c136-c138; L11 c140-c153, c167, c198-c207) and found no defect in those except D-28, D-32. NOT re-read this round: L01, L04, L07 card statements and the unchanged L02, L03, L08, L09 cards (their lesson text is byte-identical to round 7, which passed them), and the proof bodies of L05 c056-c058, c061-c062, c064 and L06 c070-c074, c076-c078, c081-c082 in full. The round-7 PASS for these is not re-proved here."),
 ("D-30", "2.7 cards: grade matches the claim (T for proof, C for lab read-off)", "course/modules/CS/CS2/cards.json: CS2-c023, CS2-c165, all C cards", "PASS",
  "Round 8: every C card's claim is a printed lab value or a read-off (checked against the expected blocks); every T card cites a definition, proposition or lemma. Round-7 failures resolved: c023 back no longer quotes a lab print, c165 is T by Proposition 2.3 of Lesson 1 (L01)."),
 ("D-31", "2.7 cards: each card tests one fact (BUILDER_RULES section 7)", "course/modules/CS/CS2/cards.json", "PASS",
  "Round 8: the round-7 compound cards are now single questions (c022, c033, c035, c066, c113, c115, c123, c126, c150, c159, c162, c164, c166 re-read). Scan of all 207 fronts found no further two-question card."),
 ("D-32", "2.7 cards: hypotheses carried for proposition-level claims", "course/modules/CS/CS2/cards.json: CS2-c133, CS2-c134, CS2-c135 (resolved), CS2-c139 (new), CS2-c112 (plausible); course/modules/CS/CS2/L10.html Corollary 2.5, Theorem 2.3", "FAIL",
  "c133-c135 now carry Corollary 2.5's hypotheses (= Theorem 2.4's: w fixed, n values at positions 0..n-1, real values, exact comparisons; L10.txt lines 34-39), resolved. CS2-c139 cites Theorem 2.3 (the front is the rolling minimum; the new index is the front exactly when x_i is at most every window value) without the hypotheses of Theorem 2.2 (w >= 1, real values, no NaN, exact comparisons; L10.txt line 23-25). CS2-c112 cites Proposition 1.3 without its hypotheses (plausible, not confirmed). Fix: add 'Assume w >= 1, real values with no NaN and exact comparisons (Theorem 2.2)' to c139; state the Proposition 1.3 hypotheses in c112."),
 ("D-33", "2.6 spec: Constraints are complete for infinite values in every class", "course/modules/CS/CS2/project.html:209, 220; grader/test_project.py:397-410; grader/reference.py", "PASS",
  "Round 8: the spec now states an outcome for an infinite value only for WelfordAccumulator.update (project.html:209); RollingMinMax.push and QuantileSketch.add state none (209, 220). grep -n inf test_project.py returns only lines 397-410 (Welford update, raises or non-finite result), 639 (epsilon), 673 (q); no test passes an infinite value to push or add; instance values are finite (D-10). The sentence matches the grader."),
 ("D-34", "2.9 structure: Rung 3 matches the curriculum scope (rolling mean)", "course/modules/CS/CS2/project.html:216, 2 (lede); curriculum/curriculum.json (CS2 project brief); plans/CS2-build-plan.md:23", "FAIL",
  "Curriculum brief (curriculum.json /parts[2]/modules[1]/project/brief; plan line 23): 'O(1)-update rolling mean, variance (Welford), min/max (monotonic deque), approximate quantile sketch'. The page's lede says 'the online mean and variance' and Conventions line 216 says 'the Welford statistics are cumulative ... the window belongs to minimum() and maximum()'. The page deliberately drops the rolling mean the curriculum names, and nothing in the plan records that as a decision. Fix: an architect decision: either change the brief in curriculum/*.yaml and regenerate curriculum.json, or add the rolling mean to the spec."),
 ("D-35", "2.9 prose: banned and process words", "course/modules/CS/CS2/project.html; course/modules/CS/CS2/cards.json; grader/*.py; tests/labs/CS2/*.py", "PASS",
  "Round 8: grep -i for verifier, builder, round N, draft, TODO, fan-out, agent, orchestrat, workflow returns nothing in the slice."),
 ("D-36", "2.4 rubric and exemplars name the same symbols", "course/modules/CS/CS2/project.html:353-354 (C2, C3 rubric), 370 and 382 (exemplars), 370 annotation (C3)", "FAIL",
  "The rubric's C2 and C3 cells name 'M2' ('the mean is the value and M2 is zero'; 'M2 after n values is the sum of squared deviations'). The round-8 edit renamed the exemplars' symbol to S (exemplar A line 369-370 and exemplar B line 380-383), and exemplar A's C3 annotation (line 370) says 'S is named but not tied', so the calibration cites a symbol the criterion does not use. Fix: change M2 to S in C2 and C3 of the rubric (or revert the exemplars to M2)."),
 ("D-37", "2.6 grader: exact rank target tested for non-round q (project.html:219)", "course/modules/CS/CS2/grader/instance.py:41 (probes); grader/test_project.py; ledgers/CS2/mutants/d8_04_quantile_rounds_q_to_six_places.py", "FAIL",
  "Mutant d8_04 rounds q to six decimals before the exact rank target. It passes 50/50 seeds (alts_run_r8.py). project.html:219 requires the rank inequalities with 'qn and epsilon n taken as exact rationals of the q ... the autograder passes'. instance.py:41 probes are the fixed nine plus round(rng.random(), 3), so no probe has more than six decimals and the rounding never changes a target. Exact check (guarantee_probe_r8.py) with q = 0.5000004: 12 violations for the mutant, 0 for the reference (e.g. n=20, eps 0.1: v=0.36 has 7 values below and 8 at or below, but qn - eps n = 9.000008 needs 10). Fix: add a probe with at least seven decimals at a rank boundary (e.g. q = 0.5000004 with epsilon 0.05 on a 20-value stream) or change the seeded probe to round(rng.random(), 9)."),
]

FIX_EXTRA = {"D-29": "Re-read every card in the listed lessons against its lesson text and record one row per lesson with the cards it covers."}

def make_row(r):
    row = {"id": r[0], "check": r[1], "location": r[2], "status": r[3], "evidence": r[4]}
    if r[3] != "PASS":
        marker = "Fix:"
        if marker in r[4]:
            row["fix"] = r[4][r[4].index(marker) + len(marker):].strip()
        else:
            row["fix"] = FIX_EXTRA[r[0]]
    return row

frag = {
 "unit": "CS2", "slice": "d", "round": 8,
 "verifier": "independent verifier (Haiku 5.5), round 8",
 "pin": "ce7b382",
 "base": "7aa909e",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB8-CS2-d",
 "scratch": str(ROOT / S),
 "verified_at": "2026-10-28T00:00:00+00:00",
 "verdict": "FAIL",
 "rows": [make_row(r) for r in rows],
 "mutants": [
  {"id": "d8_01_sketch_cap_counts_previous_value.py", "description": "Quantile sketch compresses against the cap for n - 1 values, one value behind the count it must respect.", "killed_by": None},
  {"id": "d8_02_sketch_insert_bisect_left.py", "description": "Quantile sketch inserts a new value before any equal stored values (bisect_left), so the delta is taken from the wrong neighbour.", "killed_by": None},
  {"id": "d8_03_variance_ddof_truncated_to_int.py", "description": "variance truncates ddof to an int before it is compared, so a float ddof of 0.5 is answered as the population variance.", "killed_by": "killed in the round-8 mutate_graders run (not among the three survivors); the first failing test was not recorded"},
  {"id": "d8_04_quantile_rounds_q_to_six_places.py", "description": "quantile rounds q to six decimal places before it forms the exact rank target, a student's float-noise guard that changes the target near a whole rank.", "killed_by": None},
 ],
 "registry_flags": [],
 "freshness_flags": [
  "Delta since pin 7aa909e: project.html (lede, Constraints infinite-value sentences, Conventions infinite-value bullet, exemplars A and B); cards.json (40 new, 28 changed); lessons L05, L06, L08 text. Grader, instance, reference, starter, labs and notation/references unchanged.",
  "Lab 1 twin output unchanged; expected blocks of L01-L11 unchanged (the lesson dumps for L05, L06, L08 changed; L11 expected unchanged)."
 ],
 "notes": [
  "d8_03 was added and also killed by the r8 mutation run; it is listed for completeness. The mutation gate result is 87/90 killed: d8_01, d8_02 survive but do not violate the stated guarantee; d8_04 survives and is a real grader gap (D-37).",
  "alt_r7_06 failed in the round-8 runner only because its _REF_PATH points at the removed verifyB7-CS2-d checkout; the round-8 copy alt_r7_06_r8path.py points at this checkout and passes 50/50.",
  "The two partial round-8 alternatives (alt_r8_03, alt_r8_04) were first run without the rest of reference.py and failed on import; they were spliced into the full module (make_alts_full_r8.py) and then pass 50/50.",
  "project.html's check_pages --page takes a page stem; '--page project.html' was a mis-selection and is not a finding.",
  "Not checked: a full line-by-line re-read of every lesson's prose for unchanged cards (D-29); the unchanged round-7 PASS rows are carried, not re-proved. The full repository gate (pytest over all tests, verify_refs live, fetch_data, render_curriculum) was not run; only the slice's gates."
 ],
 "summary": "Slice d round 8: FAIL. 37 rows: 30 PASS, 7 FAIL. Fails: D-15 (mutant d8_04 survives), D-28 (c124 prints 0.0872811, lab prints 0.087281), D-29 (incomplete read of T cards), D-32 (c139 hypotheses), D-34 (curriculum brief 'rolling mean' vs page cumulative), D-36 (M2 vs S in rubric), D-37 (exact rank target for non-round q untested).",
}
out = ROOT / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(frag["rows"]), "fail", sum(1 for r in frag["rows"] if r["status"] == "FAIL"))
