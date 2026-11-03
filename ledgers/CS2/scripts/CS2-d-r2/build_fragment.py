"""Build the CS2 slice-d round-2 fragment from the verification outputs in this scripts directory."""
import json, re, sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD2-CS2-d")
S = "ledgers/CS2/scripts/CS2-d-r2"

def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
 row("gate-mutate-cs2", "2.6 mutation gate (tools/mutate_graders.py --unit CS2 --seeds 0-9)",
     "ledgers/CS2/mutants/ (114 files)", "PASS",
     f"Command run on this pin: exit 0, 'mutate_graders CS2: PASS (114/114 killed)' ({S}/mutate_gate_r2_new.txt). Before the four r2 mutants were added the same gate gave 110/110 ({S}/mutate_gate.txt)."),
 row("gate-run-graders", "2.6 autograder on reference, 50 seeds; starter fails; mypy --strict",
     "course/modules/CS/CS2/grader/", "PASS",
     f"run_graders.py --unit CS2 --seeds 0-49: 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)' ({S}/run_graders.txt)."),
 row("gate-check-projects", "2.6 check_projects.py --unit CS2", "tools/check_projects.py", "PASS",
     f"'check_projects CS2: PASS' ({S}/check_projects.txt)."),
 row("gate-check-dag", "2.9 check_dag.py --unit CS2", "tools/check_dag.py", "PASS",
     f"'check_dag CS2: PASS' ({S}/check_dag.txt)."),
 row("gate-check-pages", "2.9 check_pages.py --unit CS2 (banned phrases, cards structure, hours)", "course/modules/CS/CS2/", "PASS",
     f"'check_pages CS2: PASS' ({S}/check_pages.txt)."),
 row("gate-run-labs", "2.5 run_labs.py --unit CS2", "tests/labs/CS2/", "PASS",
     f"'run_labs CS2: PASS (14/14)' ({S}/run_labs.txt)."),
 row("gate-page-smoke", "2.9 page_smoke.py --unit CS2 --pages project.html --skip-sweep (alone)", "course/modules/CS/CS2/project.html", "PASS",
     f"'page_smoke CS2: PASS', EXIT=0 ({S}/page_smoke_project.txt). The figure sweep was skipped because project.html has no live figure."),
 row("gate-ruff-mypy", "ruff check and format --check; mypy --no-incremental", "tests/labs/CS2, course/modules/CS/CS2/grader", "PASS",
     f"ruff: 'All checks passed!' and '18 files already formatted' ({S}/ruff.txt); mypy: 'Success: no issues found in 18 source files' ({S}/mypy.txt)."),
 row("gate-verify-refs", "2.1 verify_refs.py --offline (whole registry) and --unit CS2 (live)", "references/references.json", "PASS",
     f"Offline: 'offline integrity: 560 entries, 0 problems' ({S}/verify_refs.txt). Live --unit CS2: '1 of 560 entries, 0 problems' ({S}/verify_refs_live.txt)."),
 row("gate-collect-count", "2.6 test count on the page equals collect-only count", "course/modules/CS/CS2/grader/test_project.py", "PASS",
     "pytest --collect-only -q on a copy of reference.py as streamstats.py: '171 tests collected' for QF_SEED=0 and for QF_SEED=49. Page says 171 (project.html grader section)."),
 row("labs-project-1", "2.5 lab: twin under python -I -W error; page code equals twin; expected equals output",
     "project.html:53-130 (lab-CS2-project-1); tests/labs/CS2/lab-CS2-project-1.py", "PASS",
     f"project_labs_check.py: page code == twin; twin exit 0, empty stderr; output == expected block ({S}/project_labs_check.py). Page prose: 'deque operations: 44 for n = 12, bound 4n = 48' matches the output. The argument that each value is popped at most once per deque gives count <= 4n, checked by reading the code."),
 row("labs-project-2", "2.5 lab: completion blanks; twin is the completed code; expected equals output",
     "project.html:148-190 (lab-CS2-project-2); tests/labs/CS2/lab-CS2-project-2.py", "PASS",
     f"Page code differs from the twin only by the two '___' blanks (mean = mean + delta / count; m2 = m2 + delta * (x - mean)); twin output == expected block 'count 8 / mean 1000003.750000 / sample variance 8.500000' ({S}/project_labs_check.py). Recomputed by hand: offsets sum 30, mean 3.75, sum of squared deviations 59.5, 59.5/7 = 8.5."),
 row("labs-project-3", "2.5 lab: reference numbers against exact arithmetic",
     "project.html:262-340 (lab-CS2-project-3); tests/labs/CS2/lab-CS2-project-3.py", "PASS",
     f"Twin exit 0; output == expected block (project_labs_check.py). Recomputed: sum 110046.0 / 11 = 10004.181818; median target ceil(5.5 - 1.1) = ceil(4.4) = 5; sorted 5th value 10003.2; last four min 10001.0, max 10006.3."),
 row("proj-prose-numbers", "2.2 numbers in prose (classes a, b, c)", "project.html (lede, spec, Lab 1-3 interpretations, memo, hours)", "PASS",
     f"Every number traced: 20-400 values, window 2-30, epsilon 0.05/0.1/0.2, ten probes (instance.py:27-41 matches the page list 0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1 and one seeded value), 171 checks, 1e-9 tolerances, 0.2500004 example (exact_target_example.py: qn = 5.000008, exact target 5, six-place target 4), q=0.1 example (exact target 2, float target 1; same script), Exemplar B 44 vs 48 and 8.313636 (lab outputs)."),
 row("proj-named-conditions", "2.6 spec: ten named ValueError conditions, each tested; no exception type demanded for other conditions",
     "course/modules/CS/CS2/grader/test_project.py:52-68, 146-170, 416-441, 639-699", "PASS",
     "must_raise is used only for named conditions: window 0, -3, False (4); epsilon outside (0,1) incl. NaN and both infinities, and False/True (7); quantile below 0, above 1, NaN, outside [0,1] incl. infinities (9); quantile on empty sketch (10); mean and variance before any value (1); variance(1) with one value (2); NaN update/push/add (3,5,8); minimum/maximum before push (6). Other conditions use refuse_or_correct or accept any exception (lines 71-81, 350-388, 500-634, 711-754)."),
 row("proj-spec-completeness", "2.6 spec completeness: a competent student needs no clarifying question",
     "project.html Constraints and Conventions (spec section)", "PASS",
     "Checked for: membership of quantile answers (Exact counts paragraph says 'a stored value passes only if'), window of float or string types (Constraints), NaN/infinity behaviour, ddof values, default ddof 1, cumulative versus rolling statistics (Conventions). No open question found."),
 row("proj-hours", "2.6 hours: component estimate within 30% of 30 h; hub split sums", "project.html:227-258; course/modules/CS/CS2/index.html", "PASS",
     "Components 2+3+4+4+4+6+4+3 = 30 h (page). Independent estimate for a competent student: rung 1 about 1.5 h, rung 2 about 1 h, Welford code and tests 2-3 h, Welford proof 2-3 h, deque code and tests 2-3 h, sketch design, code and tests 8-11 h, validation 3-4 h, design note 2-3 h, total about 22-29 h, within 30% of 30 h. Hub data-hours-lessons 100 + project 30 = 130 (curriculum consistent)."),
 row("proj-rubric-calibration", "2.6 rubric: blind calibration of exemplars A and B within one level",
     "project.html:346-390 (rubric, exemplar-a, exemplar-b)", "PASS",
     "Blind scoring by the verifier from the rubric text: Exemplar A C1 1, C2 1, C3 2, C4 1, C5 1, C6 1 (matches data-scores 1,1,2,1,1,1). Exemplar B 4 on all six criteria, matching its annotations. Each annotation's level claim also checked against the level descriptors."),
 row("proj-rubric-observable", "2.6 rubric: every level descriptor observable; no vague descriptor",
     "project.html rubric table (criteria C1-C6)", "PASS",
     "Each level names a countable or checkable element (named hypotheses, both cases shown, S stated as sum of squared deviations, named arithmetic, probe set and limits named, a printed lab count or agreement). No descriptor relies on an unmeasurable adjective."),
 row("proj-ladder-scope", "2.6 ladder and curriculum scope", "project.html:40-52 (ladder); curriculum/01-foundations.yaml:443-450", "PASS",
     "Rung 1 is worked and annotated (each deque rule has a 'Why:' note, plus the interpretation). Rung 2 is graded by its expected output. Rung 3 matches the curriculum brief: cumulative Welford, monotonic-deque rolling min and max, quantile sketch with a stated rank guarantee, proof of Welford's update; deliverables streamstats.py, proof.md, design.md; grading both. Rung 4 is open-ended. No atlas key (curriculum has none)."),
 row("proj-notation", "2.4 notation: symbols against notation/notation.json", "project.html math spans; notation/notation.json", "PASS",
     "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. The project uses none of them. Its local symbols (n, q, epsilon, x_i, x-bar_n, S_n, delta, m, S in Exemplar A) are defined on the page: Conventions and Exemplar B define them before use, which notation.json permits for conventionally local letters. Macros used: \\bar, \\delta, \\varepsilon, \\sum, \\dots, \\frac (no conflict)."),
 row("proj-process-words", "2.9 no process words in learner text", "project.html; cards.json; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py", "PASS",
     "Word search for builder, verifier, round, architect, ledger, reviewer, agent, fragment, pin: no hits in learner text (only Python round() in instance.py:38, 41)."),
 row("proj-dag-concepts", "2.9 / DAG: concepts used before definition or outside closure",
     "project.html lede and memo links (welford-algorithm, monotonic-deque, quantile-sketch, mathematical-induction)", "PASS",
     f"check_dag.py --unit CS2 PASS ({S}/check_dag.txt). The four linked concepts are defined in CS2 L09-L11 and in the M1 prerequisite of the unit."),
 row("proj-reading-citation", "2.1 citation on the project page (cormen2022introduction)", "project.html Reading section", "PASS",
     "Registry record: Introduction to Algorithms, fourth edition, Cormen et al., MIT Press 2022, ISBN 9780262046305, status verified (references/references.json). The page states no locator and attributes no step to the book. Live verify_refs CS2: 0 problems."),
 row("proj-exemplar-b-claims", "2.9 / 2.2 claims inside Exemplar B (probes, streams, bound, Lab 1 and Lab 3 numbers)",
     "project.html:376-390 (exemplar-b)", "PASS",
     "Probe set and epsilon values match instance.py:27-28; stream lengths 1-8 match test_project.py:818-833 (the docstring of test_sketch_rank_guarantee_on_short_streams); 44 deque operations and bound 48 match lab output; 8.313636 and the agreement match lab-CS2-project-3 output. Proof algebra re-derived by the verifier: S_{n+1} = S_n + n delta^2/(n+1) = S_n + delta (x_{n+1} - mean_{n+1}), checked."),
 row("grader-instance", "2.6 instance generator: determinism, validity, SIMULATED, docstring counts",
     "course/modules/CS/CS2/grader/instance.py:1-16 and 33-50", "PASS",
     f"Seeds 0-49: all instances valid (length 20-400, window 2-30, epsilon in {{0.05,0.1,0.2}}, ten probes, SIMULATED label, deterministic); 50 distinct (mean, window, epsilon) answers ({S}/instance_validity.py). Docstring counts re-derived by {S}/naive_counts.py: offset 0: 16 seeds, 0 naive failures; offset 10000: 23 seeds, 22 failures (seed 41 passes); offset 1000000: 11 seeds, 11 failures. All match the docstring."),
 row("grader-reference", "2.6 reference solution passes; docstring invariants of the sketch",
     "course/modules/CS/CS2/grader/reference.py:94-143", "PASS",
     f"run_graders 50/50 seeds. {S}/invariant_check.py over 24,910 insertion states: sum of g = n, g + delta <= floor(2 eps n) + 1, and for each stored value some copy has exact rank in [running g sum, running g sum + delta]: 0 violations of each. Rank target line 137 = max(1, ceil(q n - eps n)) with exact Fractions, as Conventions states."),
 row("grader-starter", "2.6 starter fails the suite", "course/modules/CS/CS2/grader/starter.py", "PASS",
     "run_graders.py checks that the starter fails the suite (gate PASS, run_graders.txt)."),
 row("grader-tests-rank", "2.6 rank guarantee tests: probes, short streams, ties, sorted, exact-target witnesses",
     "course/modules/CS/CS2/grader/test_project.py:769-885", "PASS",
     "Tests use exact Fraction counts (guarantee_holds, lines 702-708; inline checks). Witnesses at 850-885 re-derived: q = 0.1, n = 20, epsilon 0.05 gives exact target 2 and float target 1; q = 0.2500004 gives qn = 5.000008, exact target 5, and six-place target 4."),
 row("grader-messages-no-expected-value", "2.6 failure messages name the property and never print the expected value",
     "course/modules/CS/CS2/grader/test_project.py:192, 200, 218", "FAIL",
     "Three failure messages print an expected numeric value of a fixed fixture: line 200 'the sample variance of 1 and 3 is 2.'; line 218 'the sample variance is zero.'; line 192 'the population variance of one value is zero.' project.html:211 (grading mode) promises that a failing check 'never prints the expected value'.",
     "Reword the three messages to name the property without the value, e.g. line 200: 'the sample variance of the two values 1 and 3 is not the defined value'; line 218: 'a constant stream must give the variance that the page defines for it'; line 192: 'the population variance of a single value must follow Conventions'. Then rerun run_graders --unit CS2 and mutate_graders --unit CS2."),
 row("grader-new-mutants", "2.6 at least three new student-error mutants, each killed",
     "ledgers/CS2/mutants/r2_01..r2_04", "PASS",
     f"Four written by the verifier: r2_01 compression merges the minimum tuple; r2_02 rank search strictly past the target; r2_03 target from a rounded slack; r2_04 cap uses four epsilon n. Each violates the rank guarantee with an exact-count counterexample found by {S}/sketch_guarantee.py (for example r2_01: q = 0, n = 35, epsilon 0.05, answer -4.7, 2 values strictly below, slack 1.75; r2_03: q = 0.49, n = 35, answer -0.5, 19 below, bound 18.9). All four killed in the gate (mutate_gate_r2_new.txt)."),
 row("grader-alternatives", "2.6 five or more alternative correct implementations pass",
     f"{S}/alts/alt_r2_A1..A6", "PASS",
     f"Six correct alternatives all PASS seeds 0-49 ({S}/run_alts_output.txt): A1 Welford with exact Fractions; A2 rolling min/max with heaps and lazy deletion; A3 rolling min/max by scanning the window; A4 sketch that keeps every value sorted and answers the exact order statistic; A5 Welford with the M2 increment written as (x - old mean)(x - new mean); A6 the reference with the compression cap computed in floats."),
 row("mut-survivors", "2.6 surviving mutants d8_01, d9_04, d8_02 moved to equivalent/ with a proof",
     "ledgers/CS2/equivalent/README.md (d8_01_sketch_cap_counts_previous_value.py, d9_04_sketch_cap_without_plus_one.py, d8_02_sketch_insert_bisect_left.py, m14_01 docstring)", "FAIL",
     f"The gate now exits 0 because these three files were moved out of mutants/. Their correctness is not proved in README: the 'Reduction' is 'stated as a claim about the reference's proof rather than re-derived here', it cites 'design.md' (no such file in the repository), and the d8_02 tie argument ('depend only on the multiset of values and the bands') is asserted. Empirical evidence from the verifier: {S}/sketch_guarantee.py on each file, 27,732 streams and 2,815,932 queries (exhaustive over {{0,1,2}}^len, len <= 7, plus random), 0 violations (guar_*.txt); large-n run 400 streams, 0 violations. The claim that these are not student errors therefore holds on evidence, but the README gives no proof.",
     "Write the reduction as numbered lemmas with proofs in README: (1) the answer T-th rank rule, (2) rmin_{i-1} < T implies count strictly below v_i <= rmin_{i-1} + Delta_{i-1}, (3) Delta_i <= floor(2 eps n) for both variants by the band lemma, covering ties for d8_02. Remove the citation of design.md or name the file in the repository. If a lemma cannot be proved, keep the three files as alternatives that the gate must pass, not as equivalent mutants. Also rename the m14_01 copy and replace its reference docstring with a description line (the round-1 issue, still present)."),
 row("equiv-m14_01", "2.6 equivalent mutant: proof and randomized check",
     "ledgers/CS2/equivalent/m14_01_rank_target_no_clamp.py", "PASS",
     f"Argument (README) checked: every stored g >= 1, so after the first tuple the running rank is at least 1, and both targets are <= 1 when the clamp changes T. Randomized and exhaustive check {S}/equiv_check.py: 2,484,624 queries (exhaustive over {{0,1,2}}^len, len <= 6, plus 120 random streams), 0 differences from the reference."),
 row("cards-automated", "2.7 every number and every cited label of each card appears in its lesson",
     "course/modules/CS/CS2/cards.json (216 cards)", "PASS",
     f"{S}/cards_check.py: 216 cards, 0 mismatches. Card ids unique; no duplicate fronts; 41 pairs of near-identical fronts (similarity above 0.8) reviewed by hand; each asks a different question (epsilon 1/20 or 1/10, offset 10^6 or 10^9, push or pop, rotation type, alpha value)."),
 row("cards-sample", "2.7 one row per 10 cards (sampled): semantics against lesson text",
     "cards.json: CS2-c001, c011, c021, c031, c041, c051, c061, c072, c082, c092, c102, c112, c122, c132, c142, c152, c162, c172, c182, c192, c202, c212", "PASS",
     "Two layers. Automation (cards_check.py) confirmed every number and label of each sampled card occurs in its lesson. Re-derived by hand: c011 (3n+7 is O(n) with c = 10, n0 = 1, and 3n+7 <= n fails for n >= 1), c122 (six operations, as Corollary 2.3 of L09 states), c142 (k_h formula matches the M1 Mechanics arithmetic), c152 (500, 1000, 550 and 450 are right). The other sampled cards were read for their statement against standard results and against their label, not compared line by line to the lesson; c092 (Corollary 3.4 statement) and the end of c132 (Theorem 2.4 comparison count) were not read in full. This is the weakest part of the PASS, and it is stated here rather than hidden."),
 row("cards-changed-delta", "2.7 cards changed or added since the prior pin, each against the current lesson",
     "cards.json: CS2-c108, c144, c210, c211, c212, c213, c214, c216, c217", "PASS",
     f"c108 matches Proposition 3.2 (L08). c144 matches Lemma 2.3 (L11). c210: Lab 2 prints 'unsuccessful search for key 3264: found=False, probes=50' ({S}/lab_L02_out.txt). c211 and c212 match Assumption 2.1, Example 2.5, Corollary 2.3, Remark 2.4 (L02). c213 matches Definition 1.4 and Remark 1.5 (L03). c214 matches Remark 2.3 and Lab 4 output 8770 and 5120 ({S}/lab_L04_out.txt). c216 matches L09 Section 3 text at line 225 (Section 3 'Where the canon breaks' runs lines 221-229). c217 matches L11 Section 3 'Exact before the first compaction' and Problem P3."),
 row("cards-c215", "2.7 card graded T for the AVL insertion rule that the lesson says is not graded",
     "course/modules/CS/CS2/cards.json: CS2-c215 (L05)", "FAIL",
     "c215 gives the rotation choice of an AVL insertion (single rotation or double rotation at balance factor 2 or -2) and grades it T. L05 Remark 3.2 (course/modules/CS/CS2/L05.html) says 'This page does not prove that one single rotation or one double rotation restores the AVL rule after every insertion. That claim is checked, not proved'. The references paragraph of L05 says 'The insertion rule of Remark 3.2 is checked by Lab 1 and is not graded as a result.' A T grade contradicts the lesson.",
     "Either regrade c215 as C with basis 'Lab 1, Part A (checks the rule after each of 500 seeded insertions)', or restate the card as the definition the page gives without a grade claim (no claim that the rule restores the AVL property). Keep the card atomic."),
 row("cards-lab-numbers", "2.7 numbers quoted from labs match printed output",
     f"cards.json: CS2-c102, c150, c162, c166, c182, c192, c196, c197, c198-c207, c210, c214", "PASS",
     f"Lab outputs saved in {S}/lab_L05_out.txt, lab_L08_out.txt, lab_L09_out.txt, lab_L11_out.txt, lab_L02_out.txt, lab_L04_out.txt. Matches: c182 single left-left rotations 63; c162 new orders 298; c192 executions 177; c150/c166 capacities 40/120/240 and 20/60/120; c198/c203 stored items 500/220; c199/c204 compactions 151/305; c201/c206 excess 0.0212 N / 0.0442 N; c196 relative errors 1.418e-02 and 8.852e-11; c197 1.000 and 7.449e-08; c102 'a float price is refused'; c210 probes 50; c214 8770 and 5120."),
 row("cards-duplicates", "2.7 full scan for duplicate cards", "course/modules/CS/CS2/cards.json", "PASS",
     "Script scan: no duplicate ids; no duplicate fronts (normalised); similarity scan lists near-duplicates, each reviewed: parameter variants (epsilon 1/20 vs 1/10; offset 10^6 vs 10^9; alpha 0.5 vs 1 vs 2 vs 4; single left-left vs double right-left rotations) that ask different questions, so none is a duplicate."),
]

# mutant ledger from the final gate output
mutants = []
for line in (ROOT / S / "mutate_gate_r2_new.txt").read_text().splitlines():
    m = re.match(r"KILLED (\S+?): (.*) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 114, len(mutants)

sha = sys.argv[1]
frag = {
  "unit": "CS2", "slice": "d", "round": 2,
  "verifier": "independent verifier (Haiku), round 2",
  "pin": sha,
  "base": "448548f997b7957f7b1d418a28d47f50d4a80fa0",
  "checkout": str(ROOT), "scratch": S,
  "verified_at": sys.argv[2],
  "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
  "rows": rows,
  "mutants": mutants,
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Prior pin for the delta is 448548f (round-15 PASS ledger in this checkout). The round-1 fragment at /Users/billyribeiro/.fanout/frags/D-CS2-d.round1.json has one FAIL row (mut-survivors) and no PASS rows, so no PASS row was carried. Every row was re-verified on this pin.",
    "Delta since 448548f in the slice: project.html line 196 (Lab 1 seed sentence), cards.json (c108, c144, c210 replaced, c211-c217 added), mutants renamed or deleted (d8_01, d8_02, d9_04, m14_01 moved to equivalent/; r15_01-03 added), equivalent/README.md. The grader, labs and other project.html text are byte-identical to 448548f (git diff --stat empty for those paths).",
    "Not run: check_pages --all, run_labs --all (only CS2 is in scope); run_graders --all; a figure sweep (none on this page). Not verified: cards c001-c209 were checked by automation and by sampling only; c092 and c132 were not read in full; the rule-by-rule check of the 2.9 banned-phrase list was done by check_pages only.",
    "Count note, not a row: cards.json has 216 cards. plans/CS2-build-plan.md section 9 gives an 'expected total 50-80'. BUILDER_RULES section 7 asks for one card per definition, theorem, key formula, empirical result and misconception, which yields more. The architect should decide which governs.",
    "Unkilled candidates not in mutants/: sketch variants that drop the -1 in the interior delta (v2) and set the first-tuple delta from the old minimum (v6) passed 27,732 + 400 streams with no guarantee violation and were not shown to violate the spec. They are not findings, but the grader does not kill them, so they stay open.",
  ],
  "summary": "Slice d round 2: FAIL. 40 rows: 37 PASS, 3 FAIL. The mutation gate now exits 0 (114/114). FAILs: (1) mut-survivors: the three survivors moved to equivalent/ rest on an unproved reduction that cites a non-existent design.md; (2) cards-c215: T grade for a rule the lesson says is not graded; (3) grader-messages-no-expected-value: three failure messages print an expected value, against the page's promise.",
}
out = ROOT / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", sum(r["status"] == "PASS" for r in rows), "fail", sum(r["status"] == "FAIL" for r in rows), "mutants", len(mutants))
