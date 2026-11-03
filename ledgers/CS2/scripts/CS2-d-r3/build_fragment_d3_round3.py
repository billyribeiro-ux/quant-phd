import json, re, sys
ROOT = '/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d'
S = 'ledgers/CS2/scripts/CS2-d-r3'
rows = []
def row(i, check, loc, status, ev, fix=None):
    r = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("gate-mutate-cs2", "2.6 mutation gate: tools/mutate_graders.py --unit CS2 --seeds 0-9 (every file in mutants/)",
    "ledgers/CS2/mutants/ (122 files)", "PASS",
    f"Command on pin a007712 plus the verifier's four new mutants: exit 0, 'mutate_graders CS2: PASS (122/122 killed)' ({S}/g_mutate_final.txt). Mutants r3_01..04 were already untracked in the checkout when this round began and are counted; their authorship was not checked. Four round-3 mutants (r3v_01..04) are new in this round.")
row("gate-run-graders", "2.6 autograder on reference, 50 seeds; starter must fail the suite",
    "course/modules/CS/CS2/grader/", "PASS",
    f"tools/run_graders.py --unit CS2 --seeds 0-49: 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 ({S}/g_run_graders.txt). run_graders.py:162-164 runs the starter against the suite and requires it to fail.")
row("gate-check-projects", "2.6 check_projects.py --unit CS2", "tools/check_projects.py", "PASS",
    f"'check_projects CS2: PASS', exit 0 ({S}/g_check_projects.txt).")
row("gate-check-dag", "2.9 check_dag.py --unit CS2", "tools/check_dag.py", "PASS",
    f"'check_dag CS2: PASS', exit 0 ({S}/g_check_dag.txt).")
row("gate-check-pages", "2.9 check_pages.py --unit CS2 (banned phrases, cards structure, hours)", "course/modules/CS/CS2/", "PASS",
    f"'check_pages CS2: PASS', exit 0 ({S}/g_check_pages.txt).")
row("gate-run-labs", "2.5 run_labs.py --unit CS2", "tests/labs/CS2/", "PASS",
    f"'run_labs CS2: PASS (14/14)', exit 0 ({S}/g_run_labs.txt).")
row("gate-page-smoke", "2.9 page_smoke.py --unit CS2 --pages project.html --skip-sweep (alone)", "course/modules/CS/CS2/project.html", "PASS",
    f"'page_smoke CS2: PASS', exit 0 ({S}/g_page_smoke.txt). project.html has no live figure, so the figure sweep does not apply.")
row("gate-ruff-mypy", "ruff check and format --check on the CS2 grader and labs; mypy --no-incremental", "tests/labs/CS2, course/modules/CS/CS2/grader", "PASS",
    f"ruff: 'All checks passed!' and '18 files already formatted', exit 0 ({S}/g_ruff.txt). mypy --no-incremental on the repository: 'Success: no issues found in 331 source files', exit 0 ({S}/g_mypy.txt).")
row("gate-verify-refs", "2.1 verify_refs.py --offline (whole registry) and --unit CS2 (live)", "references/references.json", "PASS",
    f"Offline: 'offline integrity: 560 entries, 0 problems' ({S}/g_verify_refs_offline.txt). Live: 'live re-verification of CS2: 1 of 560 entries, 0 problems' ({S}/g_verify_refs_live.txt).")
row("gate-collect-count", "2.6 test count on the page equals the collect-only count, seeds 0-49", "course/modules/CS/CS2/grader/test_project.py; project.html grader section", "PASS",
    f"Reference copied as streamstats.py into a scratch directory; QF_SEED=s pytest --collect-only -q for s = 0..49: 171 collected for every seed ({S}/collect_counts_r3.txt). project.html:211 says 171.")
row("labs-project-1", "2.5 lab: twin under python -I -W error; page code equals twin; expected equals output",
    "project.html:53-146 (lab-CS2-project-1); tests/labs/CS2/lab-CS2-project-1.py", "PASS",
    f"{S}/check_labs.py (output {S}/project_labs_check_r3.txt): the page code equals the twin except for the final newline; the twin exits 0 under python -I -W error with empty stderr; its output equals the expected block (deque operations: 44 for n = 12, bound 4n = 48). Each value is appended once per deque and popped at most once, so pushes plus pops is at most 4n; the code is read.")
row("labs-project-2", "2.5 lab: completion blanks; twin is the completed code; expected equals output",
    "project.html:148-190 (lab-CS2-project-2); tests/labs/CS2/lab-CS2-project-2.py", "PASS",
    f"Page code differs from the twin only in the two '___' lines (mean = mean + delta / count; m2 = m2 + delta * (x - mean)); twin output equals the expected block 'count 8 / mean 1000003.750000 / sample variance 8.500000' ({S}/project_labs_check_r3.txt). Recomputed by hand: offsets 2,5,1,4,9,3,6,0 sum 30, mean 3.75, sum of squared deviations 59.5, 59.5/7 = 8.5.")
row("labs-project-3", "2.5 lab: reference numbers against exact arithmetic", "project.html:262-340 (lab-CS2-project-3); tests/labs/CS2/lab-CS2-project-3.py", "PASS",
    f"Twin exit 0 under python -I -W error; output equals expected block ({S}/project_labs_check_r3.txt). Recomputed: sum 110046.0, mean 10004.181818, sample variance 8.313636; qn - epsilon n = 4.4, target ceil(4.4) = 5; 5th smallest 10003.2; last four minimum 10001.0, maximum 10006.3.")
row("proj-prose-numbers", "2.2 numbers in prose (classes a, b, c)", "project.html (lede, spec, Lab 1-3 interpretations, memo, hours)", "PASS",
    "Traced every number: 20-400 values (instance.py:35), window 2-30 (instance.py:39), epsilon 0.05/0.1/0.2 (instance.py:28,40), ten probes (instance.py:27,41: nine fixed plus one seeded), 171 checks (collect count), 1e-9 tolerances (test_project.py:84-85), 0.2500004 witness (qn = 5.000008, exact target 5, six-place target 4; recomputed with Fraction), 0.1/20/0.05 float target 1 versus exact 2 (recomputed), 44 vs 48 (lab output), 8.313636 and 10003.2 (lab output and recomputation), 30 h and 130 h (see proj-hours). Prose exception: the grader docstring sentence in grader-tests-rank.")
row("proj-named-conditions", "2.2 named ValueError conditions: each has a test; must_raise only for named conditions", "course/modules/CS/CS2/grader/test_project.py (must_raise call sites)", "PASS",
    "Read every must_raise call: window 0/-3/False (416-425), epsilon outside (0,1) including NaN, infinities, False and True (639-646), q below 0, above 1, NaN, outside [0,1] (658-676), empty sketch (693-699), NaN add and push, mean/variance before any value, variance(1) with one value, minimum/maximum before push (170-185, 436-441), and the fresh-object checks (888-902). The other exception tests accept any exception type or a correct answer, as Constraints says.")
row("proj-spec-completeness", "2.2 specification completeness and internal consistency", "project.html Constraints, Inputs, Conventions, Named errors", "PASS",
    "Read the full specification (project.html:192-226). Checked: membership of quantile answers (Exact counts paragraph), window types, NaN and infinity, ddof values, default ddof 1, cumulative versus rolling statistics. Every stated condition has a test or is marked as unconstrained. No open question found.")
row("proj-hours", "2.2 hours arithmetic: time budget vs hub split", "project.html:227-246; course/modules/CS/CS2/index.html:29; L01-L11 data-hours", "PASS",
    "Budget 2+3+4+4+4+6+4+3 = 30 (project.html:227-246 table total 30; data-hours-project=30). Lesson data-hours 8+9+10+10+9+9+10+10+10+8+7 = 100 (L01-L11.html); index.html:29 data-hours-lessons=100 and data-hours-project=30; 100+30 = 130 matches the hub title 'Tier F · 130 hours'. Hours are design targets (ruling), and the arithmetic is consistent.")
row("proj-rubric-calibration", "2.3 rubric scoring by the verifier, blind to the annotations", "project.html:348-390 (rubric-memo, exemplar-a, exemplar-b)", "PASS",
    "Scored Exemplar A from the rubric text and descriptors only: C1 1, C2 1, C3 2, C4 1, C5 1, C6 1, equal to data-scores 1,1,2,1,1,1. Exemplar B: 4 on all six, equal to data-scores 4,4,4,4,4,4. Each annotation's level claim also matches the descriptor it cites.")
row("proj-rubric-observable", "2.3 each rubric level names a checkable element", "project.html rubric table (C1-C6)", "PASS",
    "Each level names a countable or checkable element: a numbered hypothesis list, both induction cases, the S definition, the arithmetic named, the probe set and limits named, a lab count or agreement printed. No descriptor relies on an unmeasurable adjective.")
row("proj-ladder-scope", "2.2 ladder matches the curriculum brief and the grading modes", "project.html:40-52 (ladder); curriculum/01-foundations.yaml:443-450", "PASS",
    "Rung 1 worked and annotated (Why notes at the deque rules), rung 2 graded by its expected output, rung 3 deliverables streamstats.py, proof.md, design.md with both autograding and rubric grading, rung 4 open-ended. The brief's cumulative Welford, monotonic-deque rolling min and max, and quantile sketch with a stated guarantee are all present.")
row("proj-notation", "2.2 notation: every symbol against notation/notation.json", "project.html math spans; notation/notation.json", "PASS",
    "notation.json registers T, Phi and Phi^-1, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. The project uses none of them (checked the list of symbols on the page: n, q, S, S_n, x_i, x_1, x-bar, delta, epsilon, a, i, qn). S, n, m are conventionally local per the registry's 'about' text, and delta and epsilon are defined on the page before use (Lab 2 hypothesis; Conventions). Macros used (\\bar, \\delta, \\varepsilon, \\sum, \\dots, \\frac, \\cdot, \\le) are standard TeX, not registry macros, and none conflicts.")
row("proj-process-words", "2.2 no process words in learner text", "project.html; cards.json; grader/*.py; tests/labs/CS2/lab-CS2-project-*.py", "PASS",
    "Case-insensitive search for builder, verifier, round, architect, ledger, reviewer, agent, fragment, pin, checkout, rebuild: no hits (the only 'round' is Python's round() in instance.py, which the search excludes).")
row("proj-dag-concepts", "2.9 concept links and DAG closure", "project.html lede and memo links", "PASS",
    f"check_dag CS2 PASS ({S}/g_check_dag.txt). Anchors exist: L09.html#def-welford-algorithm, L10.html#def-monotonic-deque, L11.html#def-quantile-sketch (one each), concepts.html#mathematical-induction.")
row("proj-reading-citation", "2.1 reading section and registry record", "project.html Reading section; references/references.json", "PASS",
    f"Registry record cormen2022introduction: Cormen, Leiserson, Rivest, Stein; Introduction to Algorithms, fourth edition; MIT Press, 2022; ISBN 9780262046305; status verified; pages null. The page names no locator and attributes no step to the book. Live verify_refs CS2 gives 0 problems ({S}/g_verify_refs_live.txt).")
row("proj-exemplar-b-claims", "2.2 claims in Exemplar B and its annotations", "project.html:376-390 (exemplar-b)", "PASS",
    "Probe set and epsilon values match instance.py:27-28; stream lengths 1-8 match test_project.py:818-833; 44 operations versus bound 48 match the Lab 1 output; 8.313636 and the agreement match Lab 3 output. Proof algebra re-derived: a = -delta/(n+1), S_{n+1} = S_n + n a^2 + ... = S_n + n delta^2/(n+1) = S_n + delta (x_{n+1} - mean_{n+1}).")
row("grader-instance", "2.4 instance.py: validity, SIMULATED label, docstring counts", "course/modules/CS/CS2/grader/instance.py:1-16, 33-50", "PASS",
    f"Seeds 0-49: lengths 20-400, windows 2-30, epsilon in {{0.05, 0.1, 0.2}}, ten probes; run_graders PASS. Docstring counts re-derived with the naive formula (s += x, ss += x*x, mean = s/n, var = (ss - n mean^2)/(n-1)) against Fraction: offset 0: 0 of 16 seeds fail; offset 10000: 22 of 23 fail, seed 41 passes; offset 1000000: 11 of 11 fail ({S}/naive_counts.py).")
row("grader-reference", "2.6 reference solution: invariants stated in its docstring; exact rank target", "course/modules/CS/CS2/grader/reference.py:94-143", "PASS",
    f"run_graders 50/50 seeds. The docstring invariants (sum of g = n; g + delta <= floor(2 eps n) + 1; each stored value has a copy of exact rank in [R_i, R_i + delta_i]) were checked over 17,094 insertion states ({S}/ref_invariant.py): 0 failures of each. Rank target at line 137 is max(1, ceil(Fraction(q) n - Fraction(eps) n)), as Conventions states.")
row("grader-starter", "2.6 starter.py raises NotImplementedError in every method; the suite must fail on it", "course/modules/CS/CS2/grader/starter.py:1-53", "PASS",
    f"starter.py has NotImplementedError in every method (13-50). run_graders checks that the starter fails the suite (run_graders.py:162-164); gate-run-graders PASS ({S}/g_run_graders.txt).")
row("grader-tests-rank", "2.6 grader docstrings and witnesses: rank-target witnesses (q = 0.1; q = 0.2500004)",
    "course/modules/CS/CS2/grader/test_project.py:850-885 (docstring at 869-874)", "FAIL",
    "Witness numbers re-derived: q = 0.1, n = 20, epsilon 0.05: float target 1, exact target 2 (1.0000000000000000555 is the exact difference). q = 0.2500004: qn = 5.000008, exact target 5, six-place target 4, qn - epsilon n = 4.000008. Test docstring line 872 reads 'the answer 4 has four values at or below it, one short of qn - epsilon n = 4.000008'. That is arithmetically wrong: 4 is 0.000008 short of 4.000008, and it is one value short of the integer count 5 that the inequality needs. The assertions themselves are correct.",
    "Reword test_project.py:872 to: 'the answer 4 has four values at or below it, but the inequality needs at least 4.000008, so five are needed.' No test logic changes.")
row("grader-messages-no-expected-value", "2.6 failing messages never print an expected value (page promise)",
    "course/modules/CS/CS2/grader/test_project.py (all pytest.fail and must_raise messages)", "PASS",
    f"Round-2 FAIL is closed: lines 192, 200 and 218 no longer print a value ({S}/fail_messages.txt). Every remaining message names a property, a named condition, a probe index, or the learner's own returned value. Messages at lines 120-122 state the grader's own instance ranges and fail only if the grader is broken, not for a learner.")
row("grader-new-mutants", "2.6 new student-error mutants written by the verifier (at least three)", "ledgers/CS2/mutants/r3v_01..04 (new this round)", "PASS",
    f"r3v_01 quantile target uses ceil(qn + eps n): killed by the rank-guarantee tests (several, seeds 0-9). r3v_02 quantile returns the predecessor of the target-reaching value: killed by test_sketch_rank_target_is_exact_where_a_float_target_is_one_short and test_sketch_rank_guarantee_with_ties (seeds 0-4). r3v_03 count returns float: killed by test_welford_count_is_read_only_int. r3v_04 minimum before push returns inf: killed by test_rolling_minimum_before_push_raises. Gate output in {S}/g_mutate_final.txt.")
row("grader-alternatives", "2.6 alternative correct implementations must pass (over-constraint check)",
    "ledgers/CS2/scripts/CS2-d-r2/alts/ (6), ledgers/CS2/scripts/CS2-d-r3/alts/ (4 new), alts_r3 from the earlier attempt (4)", "PASS",
    f"14 correct alternatives pass seeds 0-49: round-2 A1-A6; four earlier round-3 files (alt_r3_1..4); and four new ones in {S}/alts/: alt1 (reference with M2 increment delta^2 (n-1)/n and mean as old mean + (x - old)/n); alt2 (reference Welford with a sorted exact-order-statistic sketch and windowed scan); alt3 (exact Fraction Welford, GK sketch with the cap computed exactly); alt4 (both deques keep equal values, the looser tie rule of Lesson 10 Remark). One wrong alternative in r3/alts (floor of window 2.5) is killed, which the specification requires.")
row("mut-survivors", "2.6 surviving grader-mutant set: equivalents not violating a stated behaviour (round-2 FAIL)",
    "ledgers/CS2/equivalent/README.md; d8_01, d8_02, d9_04, rank_target_without_clamp.py", "PASS",
    f"Round-2 FAIL closed: README now states Lemmas 0-3 with proofs (copy invariant under insertion and compression; band bound; rank guarantee of Conventions). Re-derived every step: insertion cases for bisect_right and bisect_left, the interior-tuple band g_s + Delta_s, the bound K - 1 <= floor(x), and #(<v_i) <= floor(qn + eps n). design.md is no longer cited. Numerical check ({S}/equiv_guarantee.py): 13,516 streams (exhaustive over {{0,1,2}}^len, len <= 7, plus 400 random) and 4,149,159 guarantee checks per variant, 0 violations for reference, d8_01, d9_04 and d8_02. rank_target_without_clamp matched the reference on all 4,149,159 queries. All four pass the suite on seeds 0-49.")
row("equiv-m14_01", "2.6 equivalence of m14_01 (rank target without clamp) to the reference",
    "ledgers/CS2/equivalent/rank_target_without_clamp.py", "PASS",
    "README proof re-derived: after the first tuple the running rank is at least 1, so unclamped target <= 0 and clamped target 1 both return values[0]; the functions are identical for n >= 1. Checked by {S}/equiv_guarantee.py: 0 differences in 4,149,159 queries.")
row("cards-automated", "2.4 cards.json: 216 cards, ids, duplicates, numbers against lesson text, grade and basis rules",
    "course/modules/CS/CS2/cards.json", "PASS",
    f"216 cards; 216 unique ids; 0 duplicate fronts; 0 duplicate backs; every number in each card's front and back occurs in its lesson's text ({S}/cards_numbers.py, 0 unmatched). Grades: 141 T with no basis, 75 C each with basis. 35 pairs of near-identical fronts (similarity above 0.8) were reviewed: each pair differs in parameter or question (epsilon 1/20 or 1/10, alpha values, push or pop, rotation type, n values), so none is a duplicate. Read all 216 backs.")
row("cards-sample", "2.4 cards: sampled claims re-derived from the lesson text",
    "cards: CS2-c011, c097, c099, c108, c122, c142, c144, c152", "PASS",
    "c011: 3n+7 <= 10n for n >= 1 and 3n+7 <= n never holds (L01 Example 2.1). c097/c099: LCS of ACGTACG and TGCATGC is 3, 49 cells, memoized recursion 47 calls and 28 stored, no-memo 183 calls (recomputed in Python). c122: six operations (L09 Corollary 2.3). c142: k_h formula (L11 Definition 2.1). c144: Lemma 2.3 telescoping (L11). c152: 500 and 1000 values with R^-(1000) = 500 <= 550 and R(1000) = 1000 >= 450. c108: Proposition 3.2 (L08).")
row("cards-changed-delta", "2.4 every card whose text changed since the previous pin, and the round-2 changed set",
    "cards: CS2-c076, c088, c109, c110, c131, c146, c149, c151, c205, c207, c215; round-2 set c108, c144, c210-c217", "PASS",
    "c076: Lemma 2.1 hypotheses (L06 line 28-29) and Proposition 2.2 (L06 line 33). c088: Theorem 2.2 and Corollary 2.3 hypotheses (L07). c109/c110: Assumption 2 (L08 line 57) and Proposition 3.2/3.3 (L08 lines 69-83). c131: Theorem 2.2/2.3 hypotheses (L10 lines 29-35). c146/c149: Theorem 2.2(b), Corollary 2.6 (L11 lines 37-60). c151: 198430 and 18213 recomputed from (L+1)(L+2)(L+3)/(3 eps) + (L+1) (L11 line 169). c205: L11 line 186-188 (Problem M3). c207: Theorem 2.5 upper count and Theorem 2.4 (L11 lines 47-55). c108: L08 Proposition 3.2. c144: Lemma 2.3 (L11 line 44). c210: L02 line 147 prints 'probes=50'. c211/c212: Example 2.5, Remark 2.4 (L02 lines 49-51). c213: Definition 1.4, Remark 1.5 (L03 lines 33-36). c214: L04 Remark 2.3 and lab numbers 8770, 5120 (L04 lines 56, 236-238). c216: L09 line 134. c217: Problem P3 and Section 3 (L11 lines 166, 201-203).")
row("cards-c215", "2.4 card c215 grade (round-2 FAIL: T for a rule the lesson says is checked, not proved)",
    "course/modules/CS/CS2/cards.json: CS2-c215 (L05)", "PASS",
    "c215 is now grade C with basis 'Lab 1, Part A (checks the rule after each of 500 seeded insertions)'. L05 Remark 3.2 (line 49) says the repair claim 'is checked, not proved', and line 298 says the insertion rule is checked, not proved. The back matches L05 Section 3 (line 43). Round-2 FAIL closed.")
row("cards-lab-numbers", "2.4 cards citing lab outputs: numbers equal the printed lab outputs",
    "cards c022-c024, c034-c039, c066, c068, c097, c099, c113-c115, c123-c124, c136, c138, c150, c154, c157-c159, c162-c164, c166, c168-c171, c174-c175, c180-c199, c198-c206", "PASS",
    "Each card number occurs in its lesson's printed lab output (cards_numbers.py). Derived values recomputed: 7.286e-15/9.258e-16 = 7.87, 1.418e-2/8.852e-11 = 1.60e8, 1/7.449e-8 = 1.34e7; 257/128 = 2.0078125 and 772/256 = 3.015625; rotations 63+53+2(55+57) = 340; 1/log2(phi) = 1.440420; LCS and memo counts (above). Lab 1 capacities 40/120/240 and 20/60/120 agree with L11 k_h formula.")
row("cards-duplicates", "2.4 no duplicate cards", "course/modules/CS/CS2/cards.json", "PASS",
    "Normalised-front and back scans: 0 duplicates. Near-identical pairs listed in cards-automated each ask a different question (parameter variants), so none is a duplicate.")

# ---- mutants from the gate output
mutants = []
for line in open(f'{ROOT}/{S}/g_mutate_final.txt', encoding='utf-8'):
    m = re.match(r'^(KILLED|SURVIVED) (\S+?\.py): (.*?) -> (.*)$', line.rstrip('\n'))
    if not m:
        continue
    status, name, desc, killed = m.groups()
    if status != 'KILLED':
        raise SystemExit('survivor: ' + name)
    mutants.append({"id": name[:-3], "description": desc.strip(),
                    "file": f"ledgers/CS2/mutants/{name}", "killed_by": killed.strip()})
assert len(mutants) == 122, len(mutants)

counts = {'PASS': sum(r['status'] == 'PASS' for r in rows), 'FAIL': sum(r['status'] == 'FAIL' for r in rows)}
verdict = 'PASS' if counts['FAIL'] == 0 else 'FAIL'
frag = {
 "unit": "CS2", "slice": "d", "round": 3,
 "verifier": "independent verifier (Haiku), round 3",
 "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
 "base": "c737272f5bdef4a027417989cd52254555e8a0bb (round-2 pin)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d",
 "scratch": S,
 "verified_at": "2026-11-03T09:01:37Z",
 "verdict": verdict,
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Delta since the round-2 pin c737272f (git diff --stat over the slice): course/modules/CS/CS2/cards.json (c076, c088, c109, c110, c131, c146, c149, c151, c205, c207 reworded or regraded; c215 regraded C with a basis); course/modules/CS/CS2/grader/test_project.py (three failure messages at lines 192, 200, 218 reworded); ledgers/CS2/equivalent/README.md (proofs of Lemmas 0-3 added; design.md citation removed); equivalent/rank_target_without_clamp.py (renamed from m14_01); equivalent/d8_02 docstring; four round-2 mutants r2_01..04 moved into mutants/. project.html, the three project labs and reference.py/instance.py/starter.py are byte-identical to c737272f (git diff --stat empty for those paths), so their round-2 PASS rows were re-verified here rather than carried, as the task asked.",
  "Pre-existing state: at the start of this round the checkout already had untracked files from an earlier interrupted attempt: ledgers/CS2/mutants/r3_01..04, and ledgers/CS2/scripts/CS2-d-r3/ (build_fragment_r3.py, make_fragment_r3.py, mutate_gate_r3.txt, alts/alt_f_floor_plus_one_rank.py and others). I did not rely on any of their outputs; I re-ran the gates and the mutant set myself. r3_01..04 are counted in the 122 mutants (killed by the gate); the tracked CS2-d.json was modified and is overwritten by this fragment.",
  "Count note for the architect, not a row: cards.json has 216 cards; plans/CS2-build-plan.md section 9 gives an 'expected total 50-80'. BUILDER_RULES section 7 asks for one card per definition, theorem, key formula, empirical result and misconception, which yields more. The architect should decide which governs.",
  "Deployment note, not a row (outside the slice): BLUEPRINT.md (line ~399) says deployment excludes every grader/reference.py. No deployment configuration exists in this repository (no vercel.json, no deploy step in .github/workflows/ci.yml), so the exclusion cannot be checked from this checkout. 20 reference.py files are committed under course/. The in-browser grader panel fetches the suite, instance.py and starter only (course/assets/js/grader.js:18-30).",
  "Equivalence is not a finding: the four files under equivalent/ satisfy the rank guarantee of Conventions (proved in the README and checked numerically), so the spec does not forbid them and the grader is not required to kill them.",
  "Minor over-spec reading, not a row: Constraints says that for a ddof other than 0 or 1 'the call raises an exception of any type, and it returns nothing'; the tests treat any return as a failure, which matches the sentence."
 ],
 "summary": f"Slice d round 3: verdict {verdict}. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL. The mutation gate exits 0 (122/122 killed, 4 new verifier mutants). FAIL (minor, wording only): grader-tests-rank, test_project.py:872 says 4 is 'one short of qn - epsilon n = 4.000008'; the inequality needs five values. Round-2 FAILs (mut-survivors, cards-c215, grader-messages-no-expected-value) are closed on re-verification. No numeric claim on project.html is wrong."
}
out = f'{ROOT}/ledgers/CS2/CS2-d.json'
json.dump(frag, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
open(out, 'a', encoding='utf-8').write('\n')
print('rows', len(rows), counts, 'verdict', verdict, 'mutants', len(mutants))
