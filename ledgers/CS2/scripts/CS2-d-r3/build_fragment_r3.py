"""Build the round-3 fragment ledgers/CS2/CS2-d.json from the rows recorded by this round's checks and the
mutation gate output (ledgers/CS2/scripts/CS2-d-r3/mutate_gate_r3.txt). Usage: python -I build_fragment_r3.py <repo_root>"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
S = "ledgers/CS2/scripts/CS2-d-r3"
gate = (root / S / "mutate_gate_r3.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in gate:
    m = re.match(r"^KILLED (\S+?): (.*) -> (.*)$", line)
    if m:
        killer = re.sub(r"\s*\(seed \d+\)$", "", m.group(3)).strip()
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": killer})
assert len(mutants) == 118, len(mutants)

P = lambda status, rid, check, loc, ev, fix=None: dict(  # noqa: E731
    [("id", rid), ("check", check), ("location", loc), ("status", status), ("evidence", ev)]
    + ([("fix", fix)] if fix else [])
)

rows = [
    P("PASS", "gate-mutate-cs2", "2.6 mutation gate: tools/mutate_graders.py --unit CS2 --seeds 0-9 must exit 0",
      "ledgers/CS2/mutants/ (118 files)",
      f"Run on pin a007712 after adding r3_01..r3_04: 'mutate_graders CS2: PASS (118/118 killed)', EXIT=0 "
      f"({S}/mutate_gate_r3.txt). The 118 kill lines are the source of the mutants list of this fragment."),
    P("PASS", "gate-run-graders", "2.6 autograder on reference: run_graders.py --unit CS2 --seeds 0-49",
      "course/modules/CS/CS2/grader/",
      f"'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.3 s)', EXIT=0 ({S}/run_graders.txt). Rerun after the three "
      "grader message edits (test_project.py lines 192, 200, 218)."),
    P("PASS", "gate-check-projects", "2.6 tools/check_projects.py --unit CS2", "tools/check_projects.py",
      f"'check_projects CS2: PASS', EXIT=0 ({S}/check_projects.txt)."),
    P("PASS", "gate-check-dag", "2.9 tools/check_dag.py --unit CS2", "tools/check_dag.py",
      f"'check_dag CS2: PASS', EXIT=0 ({S}/check_dag.txt)."),
    P("PASS", "gate-check-pages", "2.9 tools/check_pages.py --unit CS2 (banned phrases, card structure, hours)",
      "course/modules/CS/CS2/", f"'check_pages CS2: PASS', EXIT=0 ({S}/check_pages.txt)."),
    P("PASS", "gate-run-labs", "2.5 tools/run_labs.py --unit CS2 (every lab twin, python -I -W error)", "tests/labs/CS2/",
      f"'run_labs CS2: PASS (14/14)', EXIT=0 ({S}/run_labs.txt)."),
    P("PASS", "gate-page-smoke", "2.9 tools/page_smoke.py --unit CS2 --pages project.html (console, math, requests, in-browser grader on reference)",
      "course/modules/CS/CS2/project.html", f"'page_smoke CS2: PASS', EXIT=0 ({S}/page_smoke_project.txt). The page has no live figure, so no figure sweep."),
    P("PASS", "gate-ruff-mypy", "2.6 ruff check, ruff format --check, mypy --no-incremental (strict) on the labs and grader",
      "tests/labs/CS2, course/modules/CS/CS2/grader",
      f"ruff: 'All checks passed!' and '18 files already formatted' ({S}/ruff.txt); mypy: 'Success: no issues found in 18 source files' ({S}/mypy.txt)."),
    P("PASS", "gate-verify-refs", "2.1 tools/verify_refs.py --offline and --unit CS2 (live)", "references/references.json",
      f"Offline: 'offline integrity: 560 entries, 0 problems' ({S}/verify_refs.txt). Live --unit CS2: '1 of 560 entries, 0 problems' ({S}/verify_refs_live.txt)."),
    P("PASS", "gate-collect-count", "2.6 documented count: 171 checks on each seed (pytest --collect-only on reference)",
      "course/modules/CS/CS2/grader/test_project.py",
      f"Collected 171 for all 50 seeds 0-49 ({S}/collect_counts.txt: 'distinct counts: [171] seeds: 50'). Page says 171 (project.html, Grading mode)."),
    P("PASS", "labs-project-1", "2.5 lab: page code == twin, twin under python -I -W error exit 0, output == expected block",
      "project.html:53-130 (lab-CS2-project-1); tests/labs/CS2/lab-CS2-project-1.py",
      f"{S}/project_labs_check.txt: 'page code == twin: True', twin exit 0, empty stderr, 'output == expected block: True'. Output: deque operations 44, bound 4n = 48."),
    P("PASS", "labs-project-2", "2.5 lab: completion page with two blanks; twin output equals expected block",
      "project.html:148-190 (lab-CS2-project-2); tests/labs/CS2/lab-CS2-project-2.py",
      f"{S}/project_labs_check.txt: page differs from twin only at the two '___' blanks (diff shown); twin exit 0; output == expected block 'count 8 / mean 1000003.750000 / sample variance 8.500000'. Hand check: offsets 2,5,1,4,9,3,6,0 have sum 30 (mean 3.75) and sum of squared deviations 59.5, and 59.5/7 = 8.5."),
    P("PASS", "labs-project-3", "2.5 lab: twin output equals expected block; numbers recomputed",
      "project.html:262-340 (lab-CS2-project-3); tests/labs/CS2/lab-CS2-project-3.py",
      f"{S}/project_labs_check.txt: exit 0, output == expected block. Hand check: stream sum 110046.0, /11 = 10004.181818; 4.4 = 5.5 - 1.1, ceil 5; 5th smallest 10003.2; last four min 10001.0 max 10006.3."),
    P("PASS", "proj-prose-numbers", "2.2 every number in project.html prose (lede, spec, labs, memo, exemplars)",
      "course/modules/CS/CS2/project.html",
      "Traced each number to its source: 20-400 values and windows 2-30 (grader/instance.py make_instance); epsilon 0.05/0.1/0.2 (instance.py:28); ten probes = nine fixed (instance.py:27) plus one seeded; 171 checks (collect_counts.txt); 1e-9 tolerances (test_project.py:84-85); Lab 1 44 vs 48; Lab 2 8.5; Lab 3 10004.181818, 8.313636, 4.4, rank 5, 10003.2; exact target example q=0.1 n=20 eps=0.05 gives exact target 2 and float target 1; q=0.2500004 gives qn = 5.000008, exact target 5, six-place target 4 (computed with Fraction in this round). Exemplar A/B figures match the labs (Exemplar B: 44 vs 48, 8.313636, the True agreement)."),
    P("PASS", "proj-named-conditions", "2.6 ValueError only for the ten named conditions",
      "course/modules/CS/CS2/grader/test_project.py:52-68, 146-170, 416-441, 639-699",
      f"Every must_raise call (fail_messages.py over the suite, {S}/fail_messages.txt) maps to a named condition of Constraints: window 0, -3, False (4); mean, variance before any value (1); variance(1) with one value (2); NaN update, push, add (3, 5, 8); minimum, maximum before push (6); epsilon outside (0,1) incl. NaN, infinities, False, True (7); quantile below 0, above 1, NaN, infinities (9); quantile on an empty sketch (10). Other invalid inputs use refuse_or_correct or accept any exception."),
    P("PASS", "proj-spec-completeness", "2.6 spec complete; list of open questions",
      "project.html Inputs, Constraints, Conventions, Named errors",
      "Read in full. Questions a student could ask and their answers on the page: whether quantile returns a float (signature in Required outputs); what an infinite value does (Constraints: raises, or mean and variance non-finite; RollingMinMax/add unspecified); ddof strings and floats (Constraints); memory bound (Conventions: none). No open question found."),
    P("PASS", "proj-hours", "2.6 hours: estimate within 30 percent of 30 h; hub split sums",
      "project.html:227-258; course/modules/CS/CS2/index.html; curriculum/01-foundations.yaml:416-420",
      "Page components 2+3+4+4+4+6+4+3 = 30. Independent estimate: rung 1 1-2 h, rung 2 about 1 h, Welford code and tests 2-3 h, proof 2-3 h, deque code and tests 2-3 h, sketch design, code and tests 8-11 h, validation and property tests 3-4 h, design note 2-3 h: total 21-30 h, inside 30 +/- 30 %. Lesson study hours L01-L11 (data-hours attributes) sum to 100 = hub; 100 + 30 = 130 = curriculum CS2 hours."),
    P("PASS", "proj-rubric-calibration", "2.6 rubric calibration: blind scores within one level of exemplar annotations",
      "project.html:346-390 (rubric, exemplar-a, exemplar-b)",
      "Blind scoring from the rubric text: Exemplar A C1 1, C2 1, C3 2, C4 1, C5 1, C6 1 (data-scores 1,1,2,1,1,1); Exemplar B 4 on all six (data-scores 4,4,4,4,4,4). Each annotation's level claim checked against the descriptors (for example Exemplar B C5 names both inequalities, the ten probes, and the memory, adversarial-order and domain limits)."),
    P("PASS", "proj-rubric-observable", "2.6 rubric: every level descriptor observable",
      "project.html rubric table (criteria C1-C6)",
      "Each level names a countable or checkable element: named hypotheses H1-H3 and where cited; base case shown or not; S named as the sum of squared deviations; both inequalities with slack; ten probes and streams named; a printed lab count or agreement. No descriptor depends on an unmeasurable adjective (the word 'fast' appears only in Exemplar A's annotated weak passage)."),
    P("PASS", "proj-ladder-scope", "2.6 ladder: rung 1 solved and annotated; rung 2 instant; rung 3 matches curriculum scope; rung 4 open",
      "project.html:40-52 (ladder); curriculum/01-foundations.yaml:443-450",
      "Rung 1 (Lab 1) is fully solved, with a Why note on each deque rule. Rung 2 (Lab 2) is graded by its expected output. Rung 3 matches the curriculum brief (cumulative Welford, monotonic-deque rolling min and max, quantile sketch with a stated rank guarantee, proof of Welford's update; deliverables streamstats.py, proof.md, design.md; grading both). Rung 4 is two open extensions."),
    P("PASS", "proj-notation", "2.4 / notation: every symbol and macro vs notation/notation.json",
      "project.html math spans (34 spans); notation/notation.json",
      "Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q: none used on the page. Macros used: \\bar, \\delta, \\varepsilon, \\sum, \\dots, \\frac, \\le, \\cdot (none conflicts). Local letters n, q, x, S, delta, a, epsilon, x-bar are defined before use (Conventions; Exemplar B definitions; 'a = x-bar_n - x-bar_{n+1}' in Exemplar B). S and m are conventionally local per the notation file."),
    P("PASS", "proj-process-words", "2.9 no process words in learner text",
      "project.html; cards.json; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py",
      "Word scan (builder, verifier, round, architect, ledger, reviewer, agent, fragment, pin, slice, iteration, orchestrator, workflow): only 'round' as rounding (project.html, test_project.py, instance.py, lab-project-3) and 'iteration' as a loop term (cards.json, c-cards about loops). No process word."),
    P("PASS", "proj-dag-concepts", "2.9 DAG: concepts used by the project are defined in the prerequisite closure",
      "project.html lede and memo links (welford-algorithm, monotonic-deque, quantile-sketch, mathematical-induction)",
      "Anchors exist: L09.html#def-welford-algorithm, L10.html#def-monotonic-deque, L11.html#def-quantile-sketch (grep), concepts.html#mathematical-induction defined in M1 (course/modules/M/M1/L06.html). CS2 prereqs are [CS1, M1] (curriculum/01-foundations.yaml:420). check_dag CS2 PASS."),
    P("PASS", "proj-reading-citation", "2.1 reading citation: registry key, no locator invented",
      "project.html Reading section; references/references.json",
      "Key cormen2022introduction; the page gives no page or section and attributes no step to the book. verify_refs --unit CS2 (live): 0 problems."),
    P("PASS", "proj-exemplar-b-claims", "2.2 Exemplar B claims (probe set, stream lengths, lab numbers, proof algebra)",
      "project.html:376-390 (exemplar-b)",
      "Probes and epsilons match instance.py:27-28; stream lengths 1-8 and epsilons 0.05, 0.1, 0.2 match test_project.py:818-820; 44 and 48 match Lab 1 output; 8.313636 and the True agreement match Lab 3 output; the sum of squares recurrence S_{n+1} = S_n + n delta^2/(n+1) = S_n + delta (x_{n+1} - mean_{n+1}) re-derived by hand; the constant-stream claim matches test_sketch_constant_stream_returns_the_constant (test_project.py:791)."),
    P("PASS", "grader-instance", "2.6 instances: 20 seeds valid and materially different; docstring counts re-derived",
      "course/modules/CS/CS2/grader/instance.py:1-16 and 33-50",
      f"Every seed 0-49 valid (length 20-400, window 2-30, epsilon in {{0.05,0.1,0.2}}, ten probes, SIMULATED label) and deterministic (run_graders and test_instance_is_deterministic). Docstring counts re-derived with the offset drawn by the generator itself ({S}/naive_offsets.py): offset 0: 16 seeds, 0 naive failures; offset 10000: 23 seeds, 22 failures, seed 41 passes; offset 1000000: 11 seeds, 11 failures. Matches the docstring."),
    P("PASS", "grader-reference", "2.6 reference solution: passes; sketch invariants and the rank rule",
      "course/modules/CS/CS2/grader/reference.py:94-143",
      f"run_graders 50/50 seeds. {S}/lemma_check.py on reference: 1,500 random streams, 34,297 states after each add, 0 failures of sum g = n, first tuple g=1 Delta=0, copy invariant, band bound, rank guarantee at 41 probes k/40 with exact counts. Rank target line 137 uses exact Fractions as Conventions states."),
    P("PASS", "grader-starter", "2.6 starter fails the suite; every method raises NotImplementedError",
      "course/modules/CS/CS2/grader/starter.py",
      "starter.py lines 13-53: each method raises NotImplementedError. run_graders CS2 checks that the starter fails the suite (gate PASS, run_graders.txt)."),
    P("PASS", "grader-tests-rank", "2.6 fixed rank witnesses are exact and match their text",
      "course/modules/CS/CS2/grader/test_project.py:850-885",
      "Recomputed in this round: q=0.1, n=20, epsilon=0.05 on the stream 1..20: exact target ceil(Fraction(0.1)*20 - Fraction(0.05)*20) = 2 and the float target = 1. q=0.2500004: qn = 5.000008, exact target 5, the six-decimal q 0.25 gives target 4 with qn - eps n = 4.000008 (exact)."),
    P("PASS", "grader-messages-no-expected-value", "2.6 failure messages never print the expected value",
      "course/modules/CS/CS2/grader/test_project.py:192, 200, 218 (the round-2 fix)",
      f"The three round-2 messages now name the property: line 192 'the population variance of a single value must follow Conventions.'; line 200 names the two inputs, not the value 2; line 218 'must follow Conventions'. Scan of all 109 pytest.fail and must_* messages ({S}/fail_messages.txt): the only printed values are inputs, the learner's answer, the ddof passed, the probe index, or the tolerance. Rerun after the edit: run_graders PASS and mutate_graders 118/118."),
    P("PASS", "grader-new-mutants", "2.6 new student-error mutants written by this verifier: killed by the suite",
      "ledgers/CS2/mutants/r2_01..r2_04, r3_01..r3_04",
      f"r3_01 Welford mean divides by count - 1 (killed; 28 failing tests on seed 0); r3_02 compression drops removed weight (21 failing); r3_03 quantile returns the last value within the target (23 failing); r3_04 new tuple stored with g = 0 (38 failing). Written by {S}/make_r3_mutants.py and tested with {S}/kill_detail.py. Each is a single-change copy of reference.py with the docstring error first (diff shown). r2_01..r2_04 from round 2 still kill."),
    P("PASS", "grader-alternatives", "2.6 over-constraint: correct alternatives pass seeds 0-49",
      "ledgers/CS2/scripts/CS2-d-r3/alts/, ledgers/CS2/equivalent/, ledgers/CS2/scripts/CS2-d-r2/alts/",
      f"{S}/alts_seed_pass.txt: alt_r3_1 (ddof string/float coerced), alt_r3_2 (rolling window as a sorted list), alt_r3_3 (compression scanned left to right), alt_r3_4 (integer ceiling for the target), and the four equivalent variants (d8_01, d9_04, d8_02, rank_target_without_clamp) each pass 50 of 50 seeds. Round-2 alternatives A1-A6 re-run: see {S}/alts_r2_seed_pass.txt."),
    P("PASS", "mut-survivors", "2.6 sketch variants kept out of mutants/: each satisfies the rank guarantee (proofs in README)",
      "ledgers/CS2/equivalent/README.md (Lemmas 0-3; d8_01, d9_04, d8_02); course/modules/CS/CS2/grader/test_project.py",
      f"The round-2 FAIL cited a missing design.md and asserted the tie argument. The README now proves the claim by Lemma 0 (bookkeeping), Lemma 1 (copy invariant, insertion case for bisect_right and bisect_left, compression case), Lemma 2 (band g+Delta <= max(1, C_n)), and Lemma 3 (rank guarantee). Re-derived each step by hand; no gap found. design.md no longer cited (grep). Numerical check of Lemmas 1-3 and the guarantee: {S}/lemma_check.py on d8_01, d9_04, d8_02 (bisect_left) and reference: 1,500 streams, 34,297 states each, 0 failures. The three files are spec-correct alternatives, so the grader is right to pass them (over-constraint check above)."),
    P("PASS", "equiv-m14_01", "2.5/2.6 equivalence: rank target without max(1,.) clamp is extensionally equal to reference",
      "ledgers/CS2/equivalent/rank_target_without_clamp.py; README section for m14_01",
      f"Proof (README): every stored g >= 1 and g_1 = 1, so both targets are at most 1 whenever the clamp changes the target, and the loop returns values[0] in both versions. Check {S}/equiv_m14.py over 1,213 streams (all over {{0,1,2}}, length <= 6, plus random) x 4 epsilons x 44 probes: 213,488 checks, 0 differences."),
    P("PASS", "cards-automated", "2.7 every card number and label appears in its lesson (script over all 216 cards)",
      "course/modules/CS/CS2/cards.json (216 cards)",
      f"{S}/cards_check.txt: cards=216; no NUMBER mismatch; 12 LABEL flags, each a numbered-heading reference: 'Section 4' (c010, L01), 'Section 1' (c040, L04; c070, c071, L06; c083, L07; c102, c103, L08; c116, L09), 'Section 3' (c049, L04; c209, L02; c215, L05) and 'Problem M3' (c205, L11). The lesson headings are numbered ('4Misconceptions', '1Binary search and its probe count', '3 Where the canon breaks', '3Insertion and rotations', 'M3 · Forty values at epsilon one tenth'), which the script does not parse; each flag was resolved by hand against the heading list. Note: the round-2 fragment reported 0 mismatches for the same script; this round reproduces 12 flags of the heading kind on the same lesson files."),
    P("PASS", "cards-sample", "2.7 one card in ten sampled (21 cards) checked against the lesson text",
      "course/modules/CS/CS2/cards.json: c005, c015, c025, c035, c045, c055, c065, c075, c085, c095, c105, c115, c125, c135, c145, c155, c165, c175, c195, c209, c212",
      "Each checked against the cited statement: c005 Proposition 1.4 (sum n(n-1)/2); c015 Assumption 2.1 (uniform buckets, 1/m, Problem P2); c025 successful cost 1 + (n-1)/(2m) (L02 Theorem/Proposition 2.x proof); c035 and c175 Lab 3 ratios 3.5282 to 4.5050 and 4378444 moves; c045 Remark 1.4(b); c055 Proposition 2.1 hypotheses (1)-(6) and Corollary 2.2; c065 Lab 1 Part B height 64 vs 7 and log_phi 65 = 8.6747 (recomputed); c075 Lab 1 Part A on 40 seeded graphs; c085 Definition 2.1; c095 Problem R2 and Example 2.4; c105 Proposition 1.3; c115 Lab 1 Part C 185 levels (lab output); c125 and c195 Lab 1 offset 1e9 (lab output 8.728109e-02, naive 0); c135 Corollary 2.5(c); c145 Theorem 2.2(a); c155 Lab 2 2.0078 and 3.0156 (lab output); c165 Remark 2.2 (n = 1001); c209 Section 3, fourth limit; c212 Remark 2.4."),
    P("PASS", "cards-changed-delta", "2.7 cards changed since the round-2 pin agree with the current lesson text and carry the proposition hypotheses",
      "course/modules/CS/CS2/cards.json: c076, c088, c109, c110, c131, c146, c149, c151, c205, c207, c215",
      "c076 = Lemma 2.1 hypotheses (finite undirected graph; BFS as Definition 1.1) and Proposition 2.2. c088 = Theorem 2.2 hypotheses and Corollary 2.3 (A >= 0 integer). c109 and c110 = Assumption 2 of Proposition 2.2 (every listed price has a live order) and Proposition 3.3 (L prices). c131 = Theorem 2.2 hypotheses (w >= 1, real values with no NaN, exact comparisons) and Theorem 2.3. c146, c149, c151 = Theorem 2.2 hypotheses (1)-(3) (values added in order, epsilon in (0,1) with Definition 2.1 capacities, exact arithmetic) plus Corollary 2.6 (n >= 1); c151's bounds 198430 and 18213 recomputed. c205 = Problem M3 worked solution (level 1 holds 20 items of weight 2, total 40); re-derived from Definition 2.1 (k_0 = 20, k_1 = 60). c207 = Theorems 2.4 and 2.5 (R(v) >= R-hat(v) >= qn, holds for every stream). c215 see its row."),
    P("PASS", "cards-c215", "2.7 round-2 FAIL: AVL rotation card graded T with no proof on the page",
      "course/modules/CS/CS2/cards.json: CS2-c215 (L05)",
      f"c215 is now grade C with basis 'Lab 1, Part A (checks the rule after each of 500 seeded insertions)'. L05 Remark 3.2 says the single or double rotation restoring the AVL rule is 'checked, not proved', and Lab 1 Part A checks the balance invariant after every insertion (lab text). Lab output (lab_L05.out): rotation calls 340 = 63 + 53 + 2*55 + 2*57, matching the page's 340 total. Card wording matches Section 3 of L05."),
    P("PASS", "cards-lab-numbers", "2.2/2.7 card numbers from labs equal the printed lab output",
      f"course/modules/CS/CS2/cards.json (lab-derived cards); {S}/lab_L05.out, lab_L11.out, lab_L09.out, lab_L02.out",
      "L05 (c182 63, c183 53, c184 55, c185 57, 340 total); L11 (c150 capacities 40/120/240, c166 20/60/120, c198 500, c203 220, c199 151, c204 305, c201 0.0212 N, c206 0.0442 N, c202 0.0000 N); L09 (c195 8.728109e-02 at 1e9, c196 1.418e-02 vs 8.852e-11 gives ratio 1.60e8 at 1e6, c197 1.000 vs 7.449e-08 gives 1.34e7 at 1e9); L02 (c155 2.0078 and 3.0156; 257/128 and 772/256 as stated); L08 c115 185 created."),
    P("PASS", "cards-duplicates", "2.7 full duplicate scan of the 216 cards",
      f"course/modules/CS/CS2/cards.json; {S}/cards_dup_scan.txt",
      "216 unique ids; no duplicate normalised fronts or backs. 35 front pairs with similarity > 0.8 reviewed: parameter variants that ask different numbers (alpha 0.25/0.5/1/2/4; epsilon 1/20 vs 1/10; offsets 10^6 vs 10^9; capacities; rotation types; lab counts for different parts). None is a duplicate."),
    P("FAIL", "mut-d4_02-escape", "2.6 mutation: a sketch that skips a repeated maximum (d4_02) breaks the guarantee; the suite must catch it by a sketch test",
      "ledgers/CS2/mutants/d4_02_sketch_skips_repeat_of_maximum.py; course/modules/CS/CS2/grader/test_project.py (sketch rank tests, lines 769-885)",
      f"d4_02 is killed only by test_rolling_non_integral_float_window_is_refused on seed 0 ({S}/kill_detail_accidental24.txt shows one failing test). It violates the rank guarantee of Conventions: exact-count search finds 218,790 violations ({S}/guarantee_search.py). Smallest witness: stream [0.0, 2.0, 2.0], epsilon 0.05, q = 0.5 ({S}/witness_repeat_max.py). A copy of d4_02 with the whole-number window check restored (rebased/d4_02_rebased.py) passes the whole suite on 38 of 50 seeds ({S}/run_seeds_pass.py), so a student who makes this error passes the autograder on 76 % of seeds. Seed 3 fails only test_sketch_guarantee_holds_on_sorted_streams; the other sketch tests do not catch it.",
      "Add a test to test_project.py, for example test_sketch_rank_guarantee_with_repeated_maximum: values [0.0, 2.0, 2.0], epsilon 0.05, q 0.5, both inequalities checked with exact Fraction counts, as the other rank tests do. Verified in a scratch copy: passes the reference and fails d4_02 on seeds 0 and 3. This raises the collected count to 172, so the page's '171 checks' (project.html Grading mode and the Exemplar text) must change to 172 and collect_counts must be rerun. Then add d4_02 to the mutation gate's kill list with that test as killer."),
    P("FAIL", "mut-killer-attribution", "2.6 mutation record: each mutant's killed_by names the test that detects its described error",
      "ledgers/CS2/mutants/ (70 of 118 files lack the whole-number window check of the current reference.py)",
      f"70 mutants lack 'if window != int(window):' (reference.py:59-60), so each is a copy of an older reference, not a single-change copy. For 24 of them the gate's first failing test in file order is test_rolling_non_integral_float_window_is_refused (list {S}/accidental24.lst; per-mutant failing counts in kill_detail_accidental24.txt). For f5_02 that test is its described error, so its record is correct. For 22 others the window test is not the described error but other tests also fail, so their kills are real but recorded wrongly. d4_02 has no other failing test: it is the escape in mut-d4_02-escape.",
      "Rebase every mutant in ledgers/CS2/mutants/ onto the current reference.py so that its only difference is its described change (the 70 files lack only the window check, so the rebase is one inserted check each, with the one student error kept). Rerun tools/mutate_graders.py --unit CS2 --seeds 0-9 and record each mutant's killed_by from a run of the rebased file, not from the first failing test in file order. Re-check d4_02 after the test is added (see mut-d4_02-escape)."),
]

CITE = {"proj-prose-numbers", "grader-tests-rank", "proj-process-words", "cards-duplicates", "cards-lab-numbers",
        "proj-exemplar-b-claims", "cards-c215", "labs-project-2"}
for r in rows:
    if r["id"] in CITE:
        r["evidence"] += f" Re-derived by {S}/checks_r3.py (output {S}/checks_r3.txt)."
mutants_list = mutants
fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 3,
    "verifier": "independent verifier (Haiku), round 3",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "checkout": str(root),
    "scratch": S,
    "verified_at": "2026-11-03T03:40:29Z",
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": mutants_list,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round-2 pin c737272 in the slice: cards.json (c076, c088, c109, c110, c131, c146, c149, c151, c205, c207, c215), grader/test_project.py (three messages, lines 192, 200, 218), ledgers/CS2/equivalent/ (README rewritten with Lemmas 0-3; d8_02 changed; rank_target_without_clamp.py added), ledgers/CS2/mutants/r2_01..r2_04 and the new r3_01..r3_04, and the alternatives. project.html, reference.py, instance.py, starter.py and the lab twins are byte-identical to c737272 (git diff --stat empty for those paths). Their PASS rows were re-verified on this pin, not carried.",
        "Count of mutants: 118 files in ledgers/CS2/mutants/ (114 from earlier rounds + 4 new); 118/118 killed. The four equivalent or spec-correct variants in ledgers/CS2/equivalent/ are not mutants and pass 50/50 seeds.",
        "Not checked: the in-browser grader was exercised only through page_smoke (reference solution); I did not run the browser on the new test or on the rebased mutants. The page-level rubric word count of design.md (500-800 words) is a student requirement and was not measured. Freshness (2025-2026 work) for the Cormen citation was not assessed; the page cites no claim from it. Lesson-level claims outside the cards (for example the full Lemma and Theorem texts of L01-L10) belong to slices a-c and were used only where a card cites them.",
        "Card automation: cards_check.py reports 12 LABEL flags on this pin, all numbered-heading references that the script does not parse (see cards-automated). The round-2 fragment reported 0 for the same script; the difference is not explained by any lesson change between the two pins (no CS2 lesson file changed).",
        "Mutant gate killed_by is the first failing test in pytest file order (mutate_graders.py regex); it is not the test that detects the described error. The 24 accidental kills are listed in mut-killer-attribution.",
    ],
    "summary": "Slice d round 3: FAIL. Rows: 40 PASS, 2 FAIL (mut-d4_02-escape, mut-killer-attribution); all 40 round-2 row ids kept. Round-2 FAILs are resolved: mut-survivors (README now proves the three spec-correct variants with Lemmas 0-3, and the lemmas hold numerically), cards-c215 (regraded C with a lab basis), grader-messages-no-expected-value (messages reworded). Mutation gate exits 0 (118/118), but the record shows a real spec-violating sketch error that the suite misses on 38 of 50 seeds.",
}

out = root / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mutants_list), "verdict", fragment["verdict"])
