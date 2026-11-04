"""Round-5 verifier (CS2-d): assembles ledgers/CS2/CS2-d.json from the round-5 evidence in this scratch directory.

Mutant rows are read from g_mutate_r5_final.txt (the output of tools/mutate_graders.py --unit CS2 --seeds 0-9).
Run: .venv/bin/python -I ledgers/CS2/scripts/CS2-d-r5/write_fragment_CS2d_r5.py <checkout root>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/CS2/scripts/CS2-d-r5"
PIN = "440ed3c8216725d498d9c6d7c746907d4d418198"
PREV = "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b"

CARRY = "Carried from round 4 (course/modules/CS/CS2/grader/*.py and tests/labs/CS2/ byte-identical since the previous pin {}): "
PCARRY = "Carried from round 4 (course/modules/CS/CS2/project.html outside lines 37 and 150 unchanged; cited lines byte-identical since the previous pin {}): "
CCARRY = "Carried from round 4 (the cited card objects in cards.json are byte-identical since the previous pin {}): "
ECARRY = "Carried from round 4 (ledgers/CS2/equivalent/ byte-identical since the previous pin {}): "
PREV8 = PREV[:8]

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- gates (run this round on the pin 440ed3c) ----
row("gate-mutate-cs2", "2.6 mutation gate: tools/mutate_graders.py --unit CS2 --seeds 0-9 (every file in mutants/)",
    "ledgers/CS2/mutants/ (128 files)", "FAIL",
    f"Run this round: .venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9 -> 'mutate_graders CS2: FAIL (127/128 killed)', EXIT 1 ({S}/g_mutate_r5_final.txt). The one survivor is r5v_01 (row grader-mutant-r5v01). The 125 carried mutants and the r5v_02, r5v_03 mutants are all KILLED.",
    "Make the suite kill ledgers/CS2/mutants/r5v_01_sketch_compression_folds_maximum_into_predecessor.py: add a rank-guarantee test at an epsilon in (0.2, 1), for example QuantileSketch(0.3) with values 1.0 and 2.0 and quantile(1.0), checking both inequalities of Conventions (see grader-mutant-r5v01).")
row("gate-run-graders", "2.6 autograder on reference, seeds 0-49; starter must fail",
    "course/modules/CS/CS2/grader/", "PASS",
    f"Run this round: .venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49 -> 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)' ({S}/g_run_graders.txt). run_graders includes check_instances over seeds 0-49 and mypy --strict on reference.py, instance.py and the starter.")
row("gate-check-projects", "2.6 check_projects.py --unit CS2", "tools/check_projects.py", "PASS",
    f"Run this round -> 'check_projects CS2: PASS', exit 0 ({S}/g_check_projects.txt).")
row("gate-check-dag", "2.9 check_dag.py --unit CS2", "tools/check_dag.py", "PASS",
    f"Run this round -> 'check_dag CS2: PASS', exit 0 ({S}/g_check_dag.txt). Independent: welford-algorithm, monotonic-deque and quantile-sketch are defined at L09.html, L10.html, L11.html (def-* ids, grep at the pin).")
row("gate-check-pages", "2.9 check_pages.py --unit CS2 (banned phrases, cards structure, hours)",
    "course/modules/CS/CS2/", "PASS",
    f"Run this round -> 'check_pages CS2: PASS', exit 0 ({S}/g_check_pages.txt).")
row("gate-run-labs", "2.5 run_labs.py --unit CS2", "tests/labs/CS2/", "PASS",
    f"Run this round -> 'run_labs CS2: PASS (14/14)', exit 0 ({S}/g_run_labs.txt).")
row("gate-page-smoke", "2.9 page_smoke.py --unit CS2 --pages project.html --skip-sweep (alone)",
    "course/modules/CS/CS2/project.html", "PASS",
    f"Run this round -> 'page_smoke CS2: PASS', exit 0 ({S}/g_page_smoke.txt).")
row("gate-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental for the CS2 slice",
    "course/modules/CS/CS2, tests/labs/CS2, ledgers/CS2/mutants/r5v_0*.py", "PASS",
    f"ruff check course/modules/CS/CS2 tests/labs/CS2 -> 'All checks passed!' ({S}/g_ruff_check.txt); ruff format --check course/modules/CS/CS2 tests/labs/CS2 ledgers/CS2/mutants/r5v_01..03 -> '21 files already formatted' (run this round). mypy --no-incremental (repository config) -> 'Success: no issues found in 331 source files' ({S}/g_mypy.txt). Outside this slice: the repository-wide 'ruff format --check .' reports ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py ({S}/g_ruff_format.txt); reported in notes, not a CS2-d finding.")
row("gate-verify-refs", "2.1 verify_refs.py --offline (whole registry) and --unit CS2 (live)", "references/references.json", "PASS",
    f"Run this round: --offline -> 'offline integrity: 560 entries, 0 problems'; --unit CS2 -> 'live re-verification of CS2: 1 of 560 entries, 0 problems' ({S}/g_verify_refs_offline.txt, g_verify_refs_live.txt). Plain network, no bypass.")
row("gate-collect-count", "2.6 test count on the page equals the collect-only count, seeds 0-49",
    "course/modules/CS/CS2/grader/test_project.py; project.html:211", "PASS",
    f"Run this round with {S}/collect_r5.py: pytest --collect-only per seed on a fresh workspace (reference.py as streamstats.py), Python 3.14.8, pytest 9.0.2 -> {{171: 50}} ({S}/collect_r5.out.txt). The page says 171 (project.html:211).")
row("gate-pytest-relevant", "2.5/2.6/2.9 tooling tests covering pages, labs, exemplars and refs",
    "tests/test_memo_exemplars.py, test_page_checks.py, test_labs.py, test_run_labs.py, test_refs.py", "PASS",
    f"Run this round: pytest -q on the five files, exit 0, no failures ({S}/g_pytest_relevant.txt).")
row("labs-project-1", "2.5 lab: twin under python -I -W error; page code equals twin; expected equals output",
    "project.html:53-144 (lab-CS2-project-1); tests/labs/CS2/lab-CS2-project-1.py", "PASS",
    f"{S}/lab_twin_r5.py (output {S}/lab_twin_r5.out.txt): twin rc 0 under -I -W error; stdout equals the expected block; page code vs twin: 0 differing lines.")
row("labs-project-2", "2.5 lab: completion blanks; twin is the completed code; expected equals output",
    "project.html:148-188 (lab-CS2-project-2); tests/labs/CS2/lab-CS2-project-2.py", "PASS",
    f"{S}/lab_twin_r5.out.txt: twin rc 0; stdout 'count 8 / mean 1000003.750000 / sample variance 8.500000' equals expected; the page code differs from the twin in exactly 4 lines, the two blanks (mean = ___, m2 = ___) and the two completed lines of the twin. Hypothesis (line 150) recomputed: offsets 2,5,1,4,9,3,6,0 give mean 15/4 and sum of squared deviations 119/2, so the sample variance is (119/2)/7 = 17/2 = 8.5, below 10 as the prediction question asks.")
row("labs-project-3", "2.5 lab: twin under python -I -W error; page code equals twin; expected equals output",
    "project.html:260-337 (lab-CS2-project-3); tests/labs/CS2/lab-CS2-project-3.py", "PASS",
    f"{S}/lab_twin_r5.out.txt: twin rc 0; stdout equals expected; page code equals twin. Recomputed: sum 110046.0, exact mean 10004.181818, exact sample variance 8.313636, ceil(5.5 - 1.1) = 5, 5th smallest 10003.2.")

# ---- project page ----
row("proj-prose-numbers", "2.2 numbers in prose: one row per number (lede 37, Lab 2 hypothesis 150, labs, interpretations)",
    "project.html (lede line 37; Lab 1 interpretation 145; Lab 2 hypothesis 150 and interpretation 188; Lab 3 interpretation 338)", "PASS",
    f"Changed this round: lede line 37 (no number) and Lab 2 hypothesis line 150 ('above or below 10'); the value 8.5 is recomputed (labs-project-2). Lab 1 '44 deque operations', bound 4n = 48: printed by the twin ({S}/lab_twin_r5.out.txt). Lab 3 values recomputed (labs-project-3). Carried for the unchanged interpretations: {PREV8}.")
row("proj-line145-amortized", "2.4/2.6 grade and claim: amortized work per value on the page vs Lesson 10",
    "project.html:37 and 145; course/modules/CS/CS2/L10.html (Corollary 2.5(a), Section 2 'amortized cost' paragraph)", "PASS",
    "The lede (line 37, changed this round from 'time' to 'work') and the Lab 1 interpretation (line 145) both say 'constant amortized work per value'. L10 defines an amortized cost as an average over a run of insertions and says it is not a bound on each insertion (L10 paragraph before Corollary 2.5); Corollary 2.5(a) gives at most 2 operations per insertion on average. Consistent; no timing is claimed.")
row("proj-process-words", "2.9 no process words in learner text", "project.html; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py", "PASS",
    "Scan of the page text and the grader for we/our/I/round/verifier/builder/draft: the only 'we' occurrences are in exemplar B's proof prose ('we have', 'we get', project.html:380-381, mathematical voice, not process). Banned-phrase gate: check_pages PASS.")
row("proj-rubric-calibration", "2.6 rubric calibration: exemplars score within one level", "project.html rubric and exemplars (lines 348-390)", "PASS",
    CARRY.format(PREV8) + "project.html:348-390 unchanged; the delta touches lines 37 and 150 only (git diff at the pin).")
row("proj-rubric-observable", "2.6 rubric descriptors are observable", "project.html rubric table (C1-C6)", "PASS",
    PCARRY.format(PREV8) + "rubric table unchanged; read again this round: every descriptor names a countable or visible element.")
row("proj-ladder-scope", "2.6 ladder present and correct (rung 1 solved, rung 2 instant, rung 3 scope)", "project.html:40-52; curriculum/01-foundations.yaml", "PASS",
    PCARRY.format(PREV8) + "ladder lines unchanged.")
row("proj-notation", "2.4 notation: every symbol vs notation/notation.json", "project.html math spans; cards.json; notation/notation.json", "PASS",
    f"notation.json registers 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q). Read this round: the CS2 page and cards use none of them with another meaning (the R^- of the strict rank in CS2 cards is not a registered symbol). Symbols M_n, S_n, lambda(i, j), N, w, K, epsilon, q, alpha are not registered and are defined in their lessons.")
row("proj-dag-concepts", "2.9 DAG: concepts used before defined, or outside the prerequisite closure",
    "project.html lede links (welford-algorithm, monotonic-deque, quantile-sketch); cards c218-c225", "PASS",
    "Links at project.html:37 target L09.html#def-welford-algorithm, L10.html#def-monotonic-deque, L11.html#def-quantile-sketch; the three def ids exist (grep at the pin). check_dag PASS (gate-check-dag). New cards cite only lessons of CS2 (L01-L09) and the lessons' own propositions.")
row("proj-reading-citation", "2.1 attribution: reading and citation section", "project.html:408-414; references/references.json", "PASS",
    PCARRY.format(PREV8) + "the Reading paragraph names no page or section and gives no locator; verify_refs PASS this round.")
row("proj-exemplar-b-claims", "2.3/2.6 exemplar B claims (each number printed by a lab or computed from printed values)",
    "project.html:376-390 (exemplar-b)", "PASS",
    PCARRY.format(PREV8) + "exemplar B lines unchanged; its numbers (44 against 48, 8.313636, True) re-derived above.")
row("proj-spec-completeness", "2.6 spec complete enough; ladder and grading mode stated", "project.html Inputs (198), Required outputs (200-207), Constraints (209), Conventions", "PASS",
    f"Read this round in full. A student's question: does the rank guarantee of Conventions apply to epsilon values such as 0.3 that Constraints accept, when Inputs list 0.05, 0.1 and 0.2? Answer on the page: Conventions define the guarantee for 'the epsilon of the sketch, as in Inputs and Constraints', and Constraints accept any epsilon strictly between 0 and 1. The guarantee therefore holds for every valid epsilon; the defect is in the grader (grader-mutant-r5v01), not in the spec.")
row("proj-hours", "2.6 hours: component sum vs declared project hours; hub split vs lesson hours", "project.html:227-246; course/modules/CS/CS2/index.html:75; L01-L11 data-hours", "PASS",
    "Project components 2+3+4+4+4+6+4+3 = 30 (declared 30). Lesson hours 8+9+10+10+9+9+10+10+10+8+7 = 100 (index.html:75 says 100), and 100 + 30 = 130 (index.html:9 says 130). Arithmetic consistent.")
row("proj-named-conditions", "2.6 named ValueError conditions each tested at its boundary", "grader/test_project.py (must_raise call sites); project.html Constraints", "PASS",
    CARRY.format(PREV8) + "test_project.py and the Constraints list are byte-identical in the cited places.")

# ---- grader ----
row("grader-instance", "2.6 instances: sample valid, differ materially", "course/modules/CS/CS2/grader/instance.py", "PASS",
    CARRY.format(PREV8) + "instance.py byte-identical; this round run_graders check_instances passes on seeds 0-49 (g_run_graders.txt).")
row("instance-docstring-counts", "2.6 instance docstring counts match the instance generator", "course/modules/CS/CS2/grader/instance.py:8-15", "PASS",
    CARRY.format(PREV8) + "instance.py byte-identical.")
row("grader-reference", "2.6 reference solution passes; reference is correct on the rank guarantee beyond the instance epsilons",
    "course/modules/CS/CS2/grader/reference.py:94-143", "PASS",
    f"run_graders 50/50 (g_run_graders.txt). Fresh: {S}/guarantee_wide_eps_r5.py on reference.py, epsilons 0.01..0.99 and 1e-6, 0.999999, streams of length 1..12 (sorted, reversed, 200 seeded shuffles), 101 probes, exact Fractions: checked 24727224, violations 0 ({S}/guarantee_wide_eps_reference_r5.out.txt).")
row("grader-starter", "2.6 starter fails (NotImplementedError)", "course/modules/CS/CS2/grader/starter.py:1-53", "PASS",
    CARRY.format(PREV8) + "starter.py byte-identical.")
row("grader-tests-rank", "2.6 rank tests and their probes/streams", "course/modules/CS/CS2/grader/test_project.py:850-885", "PASS",
    CARRY.format(PREV8) + "test_project.py byte-identical. The rank tests use the instance epsilons (instance.py EPSILONS = [0.05, 0.1, 0.2]) and boundary acceptance tests at 1e-6 and 0.999999 only (test_project.py:650-655); no test checks the guarantee at an epsilon between 0.2 and 1 (see grader-mutant-r5v01).")
row("grader-docstring-delta", "2.6 docstrings name the property and do not leak the answer", "course/modules/CS/CS2/grader/test_project.py", "PASS",
    CARRY.format(PREV8) + "test_project.py byte-identical. Round 4 changed docstrings at 549, 838, 869-874 were already checked.")
row("grader-messages-no-expected-value", "2.6 failure messages name the property and never leak the answer", "course/modules/CS/CS2/grader/test_project.py (pytest.fail and must_raise messages)", "PASS",
    CARRY.format(PREV8) + "test_project.py byte-identical; read this round: messages name the property.")
row("grader-new-mutants", "2.6 mutation test: new student-error mutants of the previous round killed",
    "ledgers/CS2/mutants/r4v_01..03", "PASS",
    f"Killed this round in {S}/g_mutate_r5_final.txt: r4v_01 by test_sketch_rank_guarantee_on_short_streams[3-0.2] (seed 0), r4v_02 by test_sketch_rank_guarantee_on_short_streams[2-0.05] (seed 0), r4v_03 by test_welford_sample_variance_of_two_values_is_defined (seed 0).")
row("grader-alternatives", "2.6 correct alternatives must pass the suite (over-constraint)",
    f"{S}/alts/ (alt_r5_1, alt_r5_2); ledgers/CS2/scripts/CS2-d-r4/alts/; CS2-d-r3/alts/; CS2-d-r2/alts/; alt_r5_ddof_string_denotes_number", "FAIL",
    f"Run this round: {S}/run_alts_r5.py seeds 0-49 ({S}/alts_run_r5.out.txt). 23 of 27 modules PASS 50/50 seeds, including the two new correct alternatives (alt_r5_1 exact Fraction Welford, alt_r5_2 naive-scan rolling window), four store-all sketches (r4 A-D), r2 A1-A6, r3 1-4 and alt1-4. FAIL 50/50: alt_h_running_sum_mean, alt_l_coerce_inputs_to_numbers, alt_f_floor_plus_one_rank, alt_r5_ddof_string_denotes_number. alt_failures_all_r5.py (seed 0) shows that each of the four fails ONLY test_rolling_non_integral_float_window_is_refused (grader/test_project.py:568-585), which demands that RollingMinMax(2.5) raise.",
    "Relax test_rolling_non_integral_float_window_is_refused (test_project.py:568-585): the page names only window < 1 (Constraints (4)) and says 'The conditions the specification does not name have no exception type required of them'. Keep the named check; for 2.5 accept either a refusal or the answer for the count it denotes, as the page allows for other non-required inputs.")
row("grader-mutant-r5v01", "2.6 mutation: plausible student error survives the suite",
    "ledgers/CS2/mutants/r5v_01_sketch_compression_folds_maximum_into_predecessor.py", "FAIL",
    f"Student error: QuantileSketch._compress also folds the last (maximum) tuple into its predecessor. Killed by no test on seeds 0-9 ({S}/g_mutate_r5_final.txt, SURVIVED). It is NOT equivalent: witness {S}/witness_r5v01_r5.out.txt: with epsilon 0.3 on [1.0, 2.0] and q = 1.0 the mutant answers 1.0 (at-or-below count 1 < qn - epsilon n = 1.4) while the reference answers 2.0 and passes. Exhaustive check over epsilon 0.01-0.99, 1e-6, 0.999999, n 1..12, 200 shuffles: reference 0 violations of 24727224 checks; mutant 2426954 violations ({S}/guarantee_wide_eps_r5v01_r5.out.txt). The mutant is equivalent only for epsilon in {0.05, 0.1, 0.2} ({S}/survivor_eps_0.05-0.2_r5v01_r5.out.txt: 0 violations), the only values the autograder instance uses, so the suite cannot tell it apart. Conventions state the guarantee for 'where epsilon is the epsilon of the sketch' and Constraints accept any epsilon strictly between 0 and 1.",
    "Add a test of the rank guarantee (both inequalities of Conventions, exact Fractions) at an epsilon between 0.2 and 1 that the suite exercises, e.g. QuantileSketch(0.3) fed 1.0 and 2.0, then quantile(1.0) must satisfy at-or-below >= qn - epsilon n. Keep the mutant in mutants/ once the suite kills it.")

# ---- cards ----
row("cards-automated", "2.7 cards: every number and every locator in a card appears in its own lesson; no duplicates",
    "course/modules/CS/CS2/cards.json (224 cards)", "PASS",
    f"{S}/cards_checks_delta_r5.py (output {S}/cards_checks_delta_r5.out.txt): 224 cards, every number in every card appears in its lesson text (no problems). The 12 'Section N' flags are a text-dump artifact: lesson headings are numbered without a space ('1Subproblems ...' in L07, and so on), so 'Section N' refers to heading N. Checked for the two changed-this-round cards that cite a section: CS2-c083 and CS2-c220 cite L07 heading 1 ('1Subproblems, recurrences and the two evaluation strategies'). The other 10 flagged cards are unchanged this round (round-4 PASS carried).")
row("cards-sample", "2.7 cards: one row per 10 cards sampled, each atomic and correct against the lesson",
    "CS2-c040, c080, c120, c140, c200, c213 (fresh sample); plus the changed set in cards-changed-delta", "PASS",
    "Fresh sample checked against the lesson text: c040 (L04 Section 1 comparison-sort definition), c080 (L06 Prop 2.2 and Lab 1 Part C path weights 10 and 2), c120 (L09 Theorem 2.1 hypotheses (1)-(4)), c140 (L11 Definition 1.1 rank definitions), c200 (L11 Lab 1 'nine probes'), c213 (L03 Definition 1.4 and Remark 1.5). All correct. Unchanged cards outside the sample: round-4 sample PASS carried.")
row("cards-changed-delta", "2.7 cards changed or added since the previous pin, each against its lesson",
    "cards.json: changed c006, c029, c033, c062, c083, c086, c093, c109, c122, c135, c157, c160, c187, c189; added c218-c225", "PASS",
    "Each changed or added card read against its lesson: c006 (L01 Prop 1.6: largest value, n-1 comparisons); c029 (L03 Prop 1.2 levels and index depth); c033 (see cards-c033); c062 (L05 Prop 3.1 hypotheses and conclusion); c083 (L07 Section 1 subproblem); c086 (L07 Def 3.1); c093 (L07 Cor 3.4 table cells 1<=i<=m, 1<=j<=n and Prop 3.5 mn entries); c109 (L08 Prop 3.3 index access; Assumption 2 of Prop 2.2); c122 (L09 Cor 2.3 six operations and hypotheses); c135 (L10 Cor 2.5(c), series and w>=1); c157 (L02 Lab 2 printed unsuccessful averages 0.2680, 0.5400, 1.0960, 2.0320, 4.0280, lines 136-144; grade C names the lab); c160 (L06 Lab 1 Part D: bfs(adj, 0), 1438 and 40000); c187 (L08 Lab 1 Part B/C: 400 messages, 177 removals); c189 (L08 Lab 1 Part C: largest comparison count 4); added c218 (L01 Prop 1.6), c219 (L03 Prop 1.2 height), c220 (L07 Section 1), c221 (L07 Def 3.1 lambda), c222 (L07 Prop 3.5), c223 (L08 Def 1.1 dead entries), c224 (L08 Prop 3.3 hash-map lookup), c225 (L09 Cor 2.3 state). All agree. Note for the builder (not a failure): c225 cites Corollary 2.3 without its hypotheses (stream, exact arithmetic); the claim is about what the update stores (Definition 1.2) and is not conditional on them, so it is not overgeneralised.")
row("cards-c215", "2.7 card CS2-c215 (L05 rotation choice)", "course/modules/CS/CS2/cards.json (CS2-c215)", "PASS",
    CARRY.format(PREV8) + "card object byte-identical.")
row("cards-lab-numbers", "2.7 cards that print lab numbers: every number is a printed lab output (grade C names the lab)",
    "cards c157, c160, c187, c189 (changed); other lab-number cards carried", "PASS",
    "Each printed number checked against the lab output in its lesson (see cards-changed-delta). The unchanged lab-number cards are byte-identical since the previous pin and carry the round-4 PASS.")
row("cards-duplicates", "2.7 full scan for duplicate cards", "course/modules/CS/CS2/cards.json", "PASS",
    f"Scan ({S}/cards_checks_delta_r5.py): 224 cards, 0 identical fronts or backs; 50 pairs with Jaccard >= 0.5 on front+back words. Inspected: every pair that involves a changed or added card (c032/c033 ask about the heap total and the list total; c115/c187/c188 ask about creations, removals and searches; c218-c225 have no near pair), and the Jaccard-1.0 pairs (c022/c168-171 differ by alpha, c150/c166 by epsilon, c184/c185, c196/c197, c198/c203, c199/c204, c201/c206 differ by the printed value or the epsilon). No duplicate question found.")
row("cards-c033", "2.7 card CS2-c033 (round-4 FAIL, re-verified)", "course/modules/CS/CS2/cards.json:230-236 (CS2-c033, L03)", "PASS",
    "Back now: 'Assume the hold run of Lab 3, as in Proposition 1.5, with N >= 1 initial pushes, N hold steps and N drain pops, so that the list never holds more than N keys. The sorted list makes at most 2N(N + 1) moves in total (Proposition 1.6).' L03 Prop 1.6 is 'Assume the same hold run as Proposition 1.5'; its proof uses that 'the list holds the same keys as the heap in the same run, so it never holds more than N keys'; L03 (the paragraph after Prop 1.5) shows the size bound holds for this run. The hypothesis is carried and the bound 2N(N+1) is the lesson's.")
row("mut-survivors", "2.6 equivalent mutants: proofs for mutants excluded from mutants/", "ledgers/CS2/equivalent/", "PASS",
    ECARRY.format(PREV8) + "ledgers/CS2/equivalent/ has no change in the delta. The new survivor r5v_01 is NOT equivalent (grader-mutant-r5v01) and is not added to equivalent/.")
row("equiv-m14_01", "2.6 equivalence of the rank target without clamp", "ledgers/CS2/equivalent/rank_target_without_clamp.py; ledgers/CS2/equivalent/README.md", "PASS",
    ECARRY.format(PREV8) + "the equivalence files are unchanged; the grader is unchanged, so the argument still holds.")

# ---- mutants list ----
mutants = []
for line in (ROOT / S / "g_mutate_r5_final.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, description, killed = m.groups()
    mutants.append({"id": name, "description": description, "killed_by": None if killed.strip() == "None" else killed.strip()})

fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 5,
    "verifier": "independent verifier (Haiku), round 5",
    "pin": PIN,
    "base": PREV,
    "checkout": str(ROOT),
    "scratch": S,
    "verified_at": "2026-11-03T18:30:00+00:00",
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round-4 pin 4eb6788f (git diff over the slice): course/modules/CS/CS2/project.html (lede line 37: 'time' -> 'work'; Lab 2 hypothesis line 150: sample-variance parenthetical), course/modules/CS/CS2/cards.json (14 changed objects, 8 added: CS2-c218 to c225), ledgers/CS2/mutants/r4v_01..03 and ledgers/CS2/scripts/CS2-d-r4/alts/alt_r4_A..D (added by commit 440ed3c, the round-4 fix). grader/, tests/labs/CS2/ and the rest of the slice are byte-identical to the previous pin. Every changed subject was re-verified; carried rows cite byte-identical subjects.",
        "Pre-existing state of the checkout: ledgers/CS2/CS2-d.json (round 15 of another checkout, pin 448548f9) was overwritten with this round's fragment, as the assignment requires. The directory ledgers/CS2/scripts/CS2-d-r5/ already held 22 tracked files from commit 44f1eb6a (Oct 28 2026, 'Batch 2: fixes for independent verification round 5'), not from this round. I did not rely on any of them, did not modify them, and reverted an accidental formatting of five of them (build_fragment_r5.py, card_number_delta_r5.py, guarantee_search_r5.py, lesson_text_r5.py, naive_offset_r5.py). Tracked old files still fail ruff format --check (not part of this slice).",
        "Outside this slice, observed: the repository-wide gate 'ruff format --check .' fails on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py (not touched by this verifier).",
        "Spec question answered from the page: the rank guarantee applies to any epsilon strictly between 0 and 1 (Constraints and Conventions); Inputs list the instance epsilons 0.05, 0.1, 0.2 only. This resolves grader-mutant-r5v01 as a grader defect.",
        "Hours rulings: 'about 500 to 800 words' (project.html:204) is a design target, not a numeric claim; not a row.",
        "Could not check: a real browser pass of the in-browser grader and a 360 px visual of project.html (page_smoke with --skip-sweep covers the automated checks only; no screenshot was taken). The Pyodide run is covered by page_smoke PASS, which pastes reference.py into the in-browser grader.",
        "Could not check: a blind self-scoring of the two exemplars against the rubric (carried from round 4; the exemplar and rubric lines are unchanged).",
        "Verifier mutants written this round: r5v_01 (fold maximum into predecessor, survives), r5v_02 (empty sketch quantile returns NaN, killed), r5v_03 (variance over the last five values, killed). Alternatives written this round: alt_r5_1 (exact Fraction Welford, PASS), alt_r5_2 (naive scan rolling window, PASS).",
        "Cards with hypotheses not carried, noted only: CS2-c225 (cites Corollary 2.3 without its stream and exact-arithmetic hypotheses; the claim is about the stored state, Definition 1.2 is the direct source). CS2-c135 carries w >= 1 and the series but not the exactness hypothesis of Theorem 2.4; not a failure, since the series is integer-valued in the lesson.",
        "The 'Section N' flags of cards-automated are a text-dump artifact (numbered headings), recorded so the next verifier does not re-open them.",
    ],
    "summary": "CS2 slice d, round 5: FAIL. One grader mutant survives (r5v_01: the rank guarantee is not tested for epsilon between 0.2 and 1; the mutant violates it at epsilon 0.3 on [1.0, 2.0] with q = 1.0). The grader over-constrains four correct alternatives through test_rolling_non_integral_float_window_is_refused, which demands an exception for an unnamed window of 2.5. All other rows PASS, including the round-4 cards-c033 FAIL, now fixed, and the changed project.html lines and the eight added cards.",
}

out = ROOT / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
print("rows", len(rows), counts, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
