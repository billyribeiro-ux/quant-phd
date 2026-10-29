"""Round-7 verifier script: writes the slice-d fragment with per-mutant killers (first failing test, every seed 0-9
until one kills), the row list, and the verdict computed from the rows (not asserted).

Usage (from the checkout root): .venv/bin/python ledgers/CS2/scripts/CS2-d-r7/build_fragment_r7.py
"""

from __future__ import annotations

import ast
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "ledgers/CS2/scripts/CS2-d-r7"))

from coursekit import unit  # noqa: E402
from run_graders import PYTEST_FLAGS, panel, workspace  # noqa: E402

SCRIPTS = "ledgers/CS2/scripts/CS2-d-r7"
u = unit("CS2")
cfg = panel(u)


def failing(work: Path, seed: int) -> list[str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *PYTEST_FLAGS, "-rf", cfg["suite"]],
        cwd=work,
        capture_output=True,
        text=True,
        check=False,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"},
        timeout=600,
    )
    return sorted(set(re.findall(r"^FAILED \S+::(\S+)", result.stdout, flags=re.M)))


mutants = []
for path in sorted((ROOT / "ledgers/CS2/mutants").glob("*.py")):
    description = (ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or "").splitlines()[0]
    killer = None
    for seed in range(10):
        work = workspace(u, path, cfg)
        try:
            names = failing(work, seed)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        if names:
            killer = f"{names[0]} (seed {seed}; {len(names)} failing tests on that seed)"
            break
    mutants.append({"id": path.name, "description": description, "killed_by": killer})

rows = [
    {"id": "D-01", "check": "2.1 citations: registry key used by project.html",
     "location": "course/modules/CS/CS2/project.html:411-413; references/references.json:5962",
     "status": "PASS",
     "evidence": "Re-verified in round 7. tools/verify_refs.py --offline: 560 entries, 0 problems. The only key cited is cormen2022introduction, whose record is an Open Library book (url openlibrary.org/books/OL34192801M, Introduction to Algorithms, Fourth Edition). project.html:413 says the record names no page or section and no step is attributed to it, which matches the record (no locator)."},
    {"id": "D-02", "check": "2.5 labs: Lab 1 prose and printed numbers",
     "location": "course/modules/CS/CS2/project.html:55,145,389; tests/labs/CS2/lab-CS2-project-1.py",
     "status": "PASS",
     "evidence": "python -I -W error tests/labs/CS2/lab-CS2-project-1.py exits 0, empty stderr; output 'deque operations: 44 for n = 12 values, bound 4n = 48'. Page expected block equals output (run_labs CS2 PASS 14/14). Step 9 value 1 is in the window at step 12 (window [1, 47, 61, 35]); 44 <= 48 matches the page."},
    {"id": "D-03", "check": "2.2 numbers: Lab 2 prose and expected output",
     "location": "course/modules/CS/CS2/project.html:185-188; tests/labs/CS2/lab-CS2-project-2.py",
     "status": "PASS",
     "evidence": "Twin run under -I -W error: count 8, mean 1000003.750000, sample variance 8.500000. Hand check: offsets 2,5,1,4,9,3,6,0 have mean 3.75 and sum of squared deviations 59.5, and 59.5/7 = 8.5."},
    {"id": "D-04", "check": "2.2 numbers: Lab 3 prose and expected output",
     "location": "course/modules/CS/CS2/project.html:329-338; tests/labs/CS2/lab-CS2-project-3.py",
     "status": "PASS",
     "evidence": "Twin output equals the page block (count 11, exact mean 10004.181818, exact sample variance 8.313636, Welford agrees, True, last-4 min 10001.0 max 10006.3, k = 5, 5th smallest 10003.2). Sum of the 11 strings = 110046.0 (110046/11 = 10004.1818). q n - eps n = 5.5 - 1.1 = 4.4, ceil = 5."},
    {"id": "D-05", "check": "2.6 spec: the ten named ValueError conditions each have a test",
     "location": "course/modules/CS/CS2/project.html:209; course/modules/CS/CS2/grader/test_project.py:146-157,170-210,416-451,639-699,757-763,878,882",
     "status": "PASS",
     "evidence": "Mapped (1) mean/variance before any value, (2) variance(1) with one value, (3) update NaN, (4) window < 1 and False, (5) push NaN, (6) minimum/maximum before a push, (7) epsilon outside (0,1), NaN, infinities, False and True, (8) add NaN, (9) quantile q outside [0,1] or NaN or infinite, (10) quantile on an empty sketch to tests. must_raise (test_project.py:52) is used only for these conditions; every other invalid input uses refuse_or_correct or must_accept."},
    {"id": "D-06", "check": "2.6 spec: value and window rules of Constraints",
     "location": "course/modules/CS/CS2/project.html:209; test_project.py:250-259,338-395,500-622,711-754",
     "status": "PASS",
     "evidence": "Each rule has a test: boolean, padded string, string and None values for update, push and add; whole float window 3.0, float 2.5, string, padded string and None windows; ddof as string or float, both denoting 0/1 and denoting other numbers, None must raise. Read in full (test_project.py lines 1-882)."},
    {"id": "D-07", "check": "2.6 grader: documented test count equals collect-only count",
     "location": "course/modules/CS/CS2/project.html:211; grader/test_project.py",
     "status": "PASS",
     "evidence": "Round 7: pytest --collect-only -q on the reference solution for QF_SEED 0..49 (script run in a scratch directory): 170 tests collected on all 50 seeds (32 + 17 + 1 runs at 170). The page says 170."},
    {"id": "D-08", "check": "2.2 numbers: rank-target example in Conventions",
     "location": "course/modules/CS/CS2/project.html:219; grader/test_project.py:850-865",
     "status": "PASS",
     "evidence": "ledgers/CS2/scripts/CS2-d-r7/spec_probes_r7.py: float target ceil(0.1*20 - 0.05*20) = 1; exact ceil(Fraction(0.1)*20 - Fraction(0.05)*20) = 2. The page's claim (exact 2, float 1) matches."},
    {"id": "D-09", "check": "2.2 numbers: instance.py docstring naive-formula counts",
     "location": "course/modules/CS/CS2/grader/instance.py:8-13; ledgers/CS2/scripts/CS2-d-r7/instances_r7.py",
     "status": "PASS",
     "evidence": "Re-run round 7 with the docstring's order (s += x, ss += x*x, mean = s/n): fails 0 of 16 seeds at offset 0, 22 of 23 at 10,000 (seed 41 passes, relative error 6.97e-10), 11 of 11 at 1,000,000. Matches the docstring exactly."},
    {"id": "D-10", "check": "2.6 instances: ranges stated on the page and in the docstring",
     "location": "course/modules/CS/CS2/project.html:198; grader/instance.py:27-50; ledgers/CS2/scripts/CS2-d-r7/instances_r7.py",
     "status": "PASS",
     "evidence": "Seeds 0..49: 20 <= n <= 400, window 2..30, epsilon in {0.05, 0.1, 0.2}, 10 probes in [0,1], all values finite (0 invalid). 50 distinct exact means and 50 distinct exact sample variances (materially different answers). Offsets 0, 10,000, 1,000,000 with decimals 1 or 6, as page line 198 says."},
    {"id": "D-11", "check": "2.6 autograder: reference passes and starter fails",
     "location": "course/modules/CS/CS2/grader/reference.py; grader/starter.py",
     "status": "PASS",
     "evidence": ".venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49: PASS (reference 50/50). Starter, seed 0: 167 failed, 3 passed (the three that call no method), so the suite fails on the starter."},
    {"id": "D-12", "check": "2.6 reference: rank guarantee beyond the suite",
     "location": "course/modules/CS/CS2/grader/reference.py:94-143; ledgers/CS2/scripts/CS2-d-r7/sketch_docstring_r7.py",
     "status": "PASS",
     "evidence": "sketch_docstring_r7.py: 300 random streams (ties, sorted, small-integer, large-offset), 27,683 add states, probes 0..1 plus a random probe after every add, exact counts: 0 guarantee failures. The round-6 fuzz (40,000 probe checks) is not re-cited."},
    {"id": "D-13", "check": "2.6 reference docstring claims (sketch invariants)",
     "location": "course/modules/CS/CS2/grader/reference.py:95-101; ledgers/CS2/scripts/CS2-d-r7/sketch_docstring_r7.py",
     "status": "PASS",
     "evidence": "sketch_docstring_r7.py: sum(g) = n after every add (0 failures); g + delta <= floor(2 eps n) + 1 (0 failures); for each stored value some copy of it has exact rank in [G_i, G_i + delta_i] (0 failures)."},
    {"id": "D-14", "check": "2.6 five alternative correct implementations pass (over-constraint)",
     "location": "ledgers/CS2/scripts/CS2-d-r7/alts/alt_r7_01..05; ledgers/CS2/scripts/CS2-d-r6/alts/",
     "status": "PASS",
     "evidence": "ledgers/CS2/scripts/CS2-d-r7/alts_run_r7.py on five new alternatives: weighted-average Welford mean; rolling min/max over a sorted window copy with bisect; rank target ceil((q - eps) n) as one Fraction; variance by one formula with a ddof membership test; brute-force rolling scan. Each passes 50/50 seeds (alts_run_r7.out.txt). Round-6 alternatives alt_2..alt_5 and alt_r6_01 are carried from the round-6 run (their files are unchanged)."},
    {"id": "D-15", "check": "2.6 mutation: every grader mutant killed; at least three new mutants",
     "location": "ledgers/CS2/mutants/ (83 prior + r7_01, r7_02, r7_03); ledgers/CS2/scripts/CS2-d-r7/killers_r7.py",
     "status": "PASS",
     "evidence": "tools/mutate_graders.py --unit CS2 --seeds 0-9: 83/83 (mutate_r7.out.txt). Per-mutant attribution of every failing test: killers_all_r7.out.txt (83/83) and killers_new_r7.out.txt (r7_01 killed by 12 tests, r7_02 by 3 tests on seeds 1-9, r7_03 by 25 tests). r7_02 (drops repeated values) is not killed on seed 0 but is killed on seeds 1-49 (15 tests), which satisfies the window 0-9 rule. Note: the tool's killed_by names the first FAILED line in file order, not the test for the mutant's described defect (for example s3_10 is listed under an unrelated rolling test); the per-mutant list in this fragment uses the full attribution."},
    {"id": "D-16", "check": "gates on the grader and lab files",
     "location": "tests/labs/CS2; course/modules/CS/CS2/grader",
     "status": "PASS",
     "evidence": ".venv/bin/ruff check tests/labs/CS2 course/modules/CS/CS2/grader: All checks passed. ruff format --check: 18 files already formatted. .venv/bin/mypy --no-incremental tests/labs/CS2 course/modules/CS/CS2/grader: Success, no issues in 18 source files."},
    {"id": "D-17", "check": "2.5 labs: run, alone under -I -W error, page equals twin, expected equals output",
     "location": "tests/labs/CS2/lab-CS2-project-1..3.py; course/modules/CS/CS2/project.html:53-146, 262-337",
     "status": "PASS",
     "evidence": "tools/run_labs.py --unit CS2: PASS (14/14). Each project twin run alone with python -I -W error: exit 0, empty stderr. Lab code and expected blocks in project.html are byte-identical to the twins (no change in the round-6..7 delta)."},
    {"id": "D-18", "check": "gates: check_projects, check_pages, check_dag, page_smoke (project alone)",
     "location": "course/modules/CS/CS2/project.html; ledgers/CS2/scripts/CS2-d-r7/page_smoke_project_r7.out.txt",
     "status": "PASS",
     "evidence": "check_projects --unit CS2: PASS. check_pages --unit CS2: PASS. check_dag --unit CS2: PASS. page_smoke --unit CS2 --pages project: PASS, in-browser grader 'All 170 tests pass' on seed 1407517440, zero console errors, no horizontal scroll at 360 px (page_smoke_project_r7.out.txt)."},
    {"id": "D-19", "check": "2.6 hours: arithmetic and estimate",
     "location": "course/modules/CS/CS2/project.html:33, 233-241; course/modules/CS/CS2/index.html (data-hours-lessons); curriculum/curriculum.json (CS2 hours 130)",
     "status": "PASS",
     "evidence": "Rung table 2+3+4+4+4+6+4+3 = 30 = data-hours-project (project.html:33). Lesson study hours 8+9+10+10+9+9+10+10+10+8+7 = 100 = data-hours-lessons; 100 + 30 = 130 = curriculum CS2 hours. My own estimate of the deliverables (rungs 1-2 about 2-4 h, Welford code and tests 2-4 h, Welford proof 3-5 h, deque 3-5 h, sketch and its tests 6-10 h, API and validation 3-5 h, note 2-3 h) is 24-40 h, which is within 30% of 30 h (21-39 h) at the middle of the range."},
    {"id": "D-20", "check": "2.6 rubric: observable descriptors and exemplar calibration",
     "location": "course/modules/CS/CS2/project.html:348-391",
     "status": "PASS",
     "evidence": "Six criteria, four levels each, all descriptors observable (checked each level text). Exemplar A scored 1,1,2,1,1,1 and Exemplar B 4,4,4,4,4,4, matching data-scores. Caveat: I read the annotations in the same pass as the exemplar text, so this is a close reading, not a separate blind pass."},
    {"id": "D-21", "check": "2.2 numbers quoted in exemplars",
     "location": "course/modules/CS/CS2/project.html:372, 383-390",
     "status": "PASS",
     "evidence": "8.313636 (Lab 3 exact variance), median answer 10003.2 (Lab 3), 44 operations against 4n = 48 (Lab 1), 1e-9 agreement True (Lab 3); the proof's algebra in exemplar B (lines 380-381) re-derived: a = -delta/(n+1), cross term zero, n a^2 + n^2 delta^2/(n+1)^2 = n delta^2/(n+1)."},
    {"id": "D-22", "check": "2.4 notation: symbols against notation/notation.json",
     "location": "course/modules/CS/CS2/project.html; notation/notation.json",
     "status": "PASS",
     "evidence": "Registry symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (macros E, Prob, Var, ...). The page uses n, q, epsilon, v, x_i, m_n, M_n, delta, S_n; none is a registry symbol, so there is no collision."},
    {"id": "D-23", "check": "2.9 terms and symbols defined before use: epsilon in the rank guarantee",
     "location": "course/modules/CS/CS2/project.html:198, 209, 218",
     "status": "PASS",
     "evidence": "Round-6 FAIL resolved: project.html:218 now reads 'where <em>ε</em> is the epsilon of the sketch, as in Inputs and Constraints' before the two inequalities use εn. The name is introduced at Inputs (198) and Constraints (209)."},
    {"id": "D-24", "check": "2.9 cross-links: placement bar and rung 3",
     "location": "course/modules/CS/CS2/project.html:42, 161; course/modules/CS/CS2/index.html:69-71, 161",
     "status": "PASS",
     "evidence": "Re-read round 7. index.html:161 and project.html:42 both say a skip needs the placement bar and both skill checks. index.html lines 34-37 and 169-172 changed only in the word 'seeded' -> 'generated' (not cited by this row)."},
    {"id": "D-25", "check": "2.6 tooling claims on the page",
     "location": "course/modules/CS/CS2/project.html:249, 257; requirements-dev.txt:2; course/assets/js/grader.js",
     "status": "PASS",
     "evidence": "requirements-dev.txt:2 pins pytest==9.0.2. grader.js and py-worker.js are unchanged since the round-6 pin (git diff --stat empty). Python 3.14 is the repository pin (round 6, D-25)."},
    {"id": "D-26", "check": "2.9 footer claim: nothing leaves the browser",
     "location": "course/modules/CS/CS2/project.html:426; course/assets/js/grader.js; py-worker.js",
     "status": "PASS",
     "evidence": "grader.js and py-worker.js are unchanged since the round-6 pin, so the round-6 static reading holds (fetch only for the grader's own files; postMessage only). page_smoke reports zero requests to any host but the local server (page_smoke_project_r7.out.txt)."},
    {"id": "D-27", "check": "2.7 cards: structure, ids, grades, lesson coverage",
     "location": "course/modules/CS/CS2/cards.json (167 cards)",
     "status": "PASS",
     "evidence": "167 cards, ids CS2-c001..CS2-c167 contiguous and unique; no duplicate front or back; grades T 129 (no basis), C 38 (every one with basis); lessons L01-L11 all covered. Note for the architect (not a row failure): the plan (plans/CS2-build-plan.md section 9) expects 50-80 cards; the count is 167."},
    {"id": "D-28", "check": "2.7 cards: every C-grade number against printed lab output",
     "location": "course/modules/CS/CS2/cards.json (C cards); ledgers/CS2/scripts/CS2-d-r7/text/L01-L11.expected.txt; card_numbers_r7.py",
     "status": "PASS",
     "evidence": "All 38 C cards checked against the printed expected blocks (run_labs PASS): e.g. c022/c157 (Lab 2 averages), c035 (ratios 3.5282-4.5050 and 1.9858-2.3778), c038/c039 (205/602, 19140/21405, 4933/4514, 10623/17663), c066 (height 11, 12.9186), c123-c126 (errors; 1.602e8 and 1.342e7 recomputed), c113 (levels: replayed Part C, 8 levels, 10 orders: l08_levels_r7.py), c155 (257/128, 772/256, 1.0078125). card_numbers_r7.py: every number on every card occurs verbatim in its lesson or expected block (0 missing)."},
    {"id": "D-29", "check": "2.7 cards: T-grade statements agree with the current lesson text",
     "location": "course/modules/CS/CS2/cards.json (129 T cards); course/modules/CS/CS2/L01-L11.html; ledgers/CS2/scripts/CS2-d-r7/cite_check_r7.py",
     "status": "PASS",
     "evidence": "Round 6 left this UNVERIFIABLE (spot check only). Round 7 read every T card against its lesson's definitions, propositions, lemmas, theorems, remarks, examples and problem solutions (L01-L11 text dumps, sections 1-4 read in full, cited problems R1, R2, P1, P3, M2, E1 read). Every cited label (175 citations) exists in its lesson (cite_check_r7.py; 11 'Section N' references match the lesson headings). Arithmetic re-derived: c044-c048, c061, c069, c094, c096, c127, c144, c151, c152, c155. Grade and atomicity/hypothesis issues are in D-30 to D-32."},
    {"id": "D-30", "check": "2.7 cards: grade matches the claim (T for proof, C for lab read-off)",
     "location": "course/modules/CS/CS2/cards.json: CS2-c023, CS2-c165; L01.html Key results; L02.html Key results",
     "status": "FAIL",
     "evidence": "CS2-c023 (T): the back's second clause, 'Lab 2 prints 50 probes for the absent key 3264', is a lab read-off, which the rules grade C with a basis. Lesson 2 'Key results' grades Lab 2 counts C (L02 Key results row 'Lab 2 counts ... 1275 total probes'). CS2-c165 (T): the front asks what Lab 1 prints ('What does Lab 1 print as the first n with n^2 > 1000 n?'). Lesson 1 Key results grades 'first failure at n = 1001' as C (Lab 1). The value is also proved (Problem M2, Proposition 2.3), so the card can be T if it asks the proved claim.",
     "fix": "CS2-c023: keep the Proposition 1.4 statement as a T card; move 'Lab 2 prints 50 probes for the absent key 3264' to a separate C card with basis 'Lab 2, colliding set of 50 keys'. CS2-c165: either grade it C with basis 'Lab 1, Part (counts in the counting model)' or rephrase the front to the proved claim ('What is the first integer n with n^2 > 1000 n?') with grade T and cite Problem M2 / Proposition 2.3."},
    {"id": "D-31", "check": "2.7 cards: each card tests one fact (BUILDER_RULES section 7)",
     "location": "course/modules/CS/CS2/cards.json: CS2-c022, c033, c035, c066, c113, c115, c123, c126, c150, c159, c162, c164, c166",
     "status": "FAIL",
     "evidence": "BUILDER_RULES section 7: 'Each card tests one fact.' These cards test several independent facts in one back. CS2-c115: 185 created, 177 removed, 362 searches, largest comparison count 4. CS2-c162: 298 new orders, 102 cancellations, 117 traded messages, 177 executions. CS2-c164: 340 calls, and the four kinds 63/53/55/57. CS2-c166 and c150: capacities, stored items, compactions, and two maxima. CS2-c123 and c126: the best method, the error trend and a 7.87x ratio, and the 1.60e8 and 1.34e7 ratios. CS2-c033: the moves bound and the per-push cost. CS2-c022 and c035: five averages, and two ratio ranges. CS2-c066: three facts. CS2-c113: two levels/orders claims. CS2-c159 and c162/c163: two or more counts.",
     "fix": "Split each listed card into one-fact cards with the same grade and basis (for example one card per printed count), keeping the back checkable against the same lab line. Renumber ids sequentially afterwards."},
    {"id": "D-32", "check": "2.7 cards: hypotheses carried for proposition-level claims",
     "location": "course/modules/CS/CS2/cards.json: CS2-c133, CS2-c134, CS2-c135; L10.html Corollary 2.5",
     "status": "FAIL",
     "evidence": "L10.html Corollary 2.5 states 'Hypotheses. Those of Theorem 2.4' (w >= 1 fixed; n >= 1 values at positions 0..n-1; real values with exact comparisons). CS2-c133 ('At most 2 ... amortized O(1)'), c134 ('At most w indices') and c135 ('As many as w entries') state Corollary 2.5 parts without that hypothesis line, while the back of c132 does carry its own hypotheses.",
     "fix": "Prefix each of c133, c134 and c135 with 'Assume w >= 1 is fixed, n >= 1 values are inserted at positions 0 to n - 1, and the values are real with exact comparisons (Corollary 2.5).'"},
    {"id": "D-33", "check": "2.6 spec: Constraints are complete for infinite values in every class",
     "location": "course/modules/CS/CS2/project.html:209, 220; grader/reference.py:66-91 (RollingMinMax.push), 112-120 (QuantileSketch.add); ledgers/CS2/scripts/CS2-d-r7/spec_probes_r7.py",
     "status": "FAIL",
     "evidence": "project.html:209 says: 'For an infinite value, the call raises, or the mean and the sample variance that follow are not finite numbers.' Conventions (220) says the same rule covers an infinite value in the stream. RollingMinMax and QuantileSketch have no mean or variance, so the disjunct has no outcome for them. spec_probes_r7.py: RollingMinMax.push(inf) returns with maximum() = inf; QuantileSketch.add(inf) returns with quantile(1.0) = inf; neither raises. A competent student must ask whether push(inf) and add(inf) raise. The suite does not test this, so the reference is not contradicted by a test, but the spec does not answer the question.",
     "fix": "State the outcome per class in Constraints: for example 'RollingMinMax.push(x) and QuantileSketch.add(x) with an infinite x raise ValueError, or the values that follow are not required to satisfy the specification.' Or name infinite values as outside the specification with no requirement. Then make the reference and the wording agree."},
    {"id": "D-34", "check": "2.9 structure: Rung 3 matches the curriculum scope (rolling mean)",
     "location": "course/modules/CS/CS2/project.html:216, 2 (lede); curriculum/curriculum.json (CS2 project brief); plans/CS2-build-plan.md:23",
     "status": "FAIL",
     "evidence": "The curriculum brief for CS2's project reads 'Implement O(1)-update rolling mean, variance (Welford), min/max (monotonic deque) and an approximate quantile sketch'. project.html:216 states 'Both describe every value added so far, not a window ... the Welford statistics are cumulative.' So the page implements the cumulative (online) mean and variance, not the 'rolling' mean named in the scope. The page's choice is stated, but Rung 3 does not match the curriculum scope exactly. The plan (line 23) records the scope as 'rolling mean' and does not record a decision to change it.",
     "fix": "Architect decision needed: either add a windowed rolling mean and variance to the Rung 3 interface (with the same O(1) update and a grader test) and its proof, or record in the plan and the curriculum that 'rolling' means the online running statistic, and amend the curriculum text (then regenerate; not by hand)."},
    {"id": "D-35", "check": "2.9 prose: banned and process words",
     "location": "course/modules/CS/CS2/project.html; course/modules/CS/CS2/cards.json; grader/*.py",
     "status": "PASS",
     "evidence": "grep (case-insensitive) for verifier, builder, architect, TODO, TBD, lorem, placeholder, for brevity, left as an exercise, draft, orchestrat, campaign, fan-out: 0 hits in the project page, cards and grader files (one 'round' hit is in a code comment, not learner text). check_pages (banned-phrase check) PASS."},
]

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "CS2",
    "slice": "d",
    "round": 7,
    "verifier": "independent verifier (Haiku 5.5), round 7",
    "pin": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4",
    "base": "44f1eb6a417ce687a9b88c7ee917e72566b29892",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-CS2-d",
    "scratch": f"/Users/billyribeiro/.fanout/wt/verifyB7-CS2-d/{SCRIPTS}",
    "verified_at": dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice d: project.html (rubric, exemplars, spec, labs 1-3), grader (instance, reference, starter, test_project), project labs 1-3 and cards.json (167 cards). Delta from round-6 pin 44f1eb6 to 7aa909e: project.html lines 198 and 218; cards.json (10 cards: c033, c067, c084, c092-c095, c107, c109, c110, c133, c137, c165); lesson pages L01-L11 and index.html changed (read for card agreement, not re-graded).",
        "Round 6 rows: D-23 resolved (PASS). D-29 split into D-29 (statement agreement, PASS) and D-30..D-32 (grade, atomicity, hypotheses, FAIL).",
        "Not checked: a line-by-line read of every lesson's problem-set solutions (only the problems the cards cite: P1, P3, R1, R2, M2, E1); the Pyodide run was one seed only (page_smoke); no independent timing (hours are estimates); no second blind scoring pass for the rubric exemplars; the full repository gate was not run (targeted gates for this slice only).",
        "Mutant attribution: tools/mutate_graders.py names the first FAILED line in file order; the per-mutant killed_by in this fragment is the first failing test on the first killing seed from ledgers/CS2/scripts/CS2-d-r7/build_fragment_r7.py.",
    ],
    "summary": "",
}
fragment["summary"] = (
    f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE; "
    f"{len(mutants)} grader mutants, {sum(1 for m in mutants if m['killed_by'])} killed."
)
out = ROOT / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(fragment["summary"], "verdict", fragment["verdict"], "->", out)
