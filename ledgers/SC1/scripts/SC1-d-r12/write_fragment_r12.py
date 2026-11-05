"""Build ledgers/SC1/SC1-d.json (round 12) from the round-11 fragment (carried rows keep their ids) plus round-12 rows.

Every round-12 row cites a command or file whose output is kept under ledgers/SC1/scripts/SC1-d-r12/out/.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-d.round11.json").read_text(encoding="utf-8"))
OUT = "ledgers/SC1/scripts/SC1-d-r12/out"
CARRY = "Carried from round 11 (grader/*.py, tests/labs/SC1/*.py, ledgers/SC1/mutants/*.py byte-identical since the previous pin 11d7077):"
REVER = "Re-verified in round 12 (project.html read in full at 5db69a9; the delta lines 57, 462 and 584 read again):"
LESSON = "Re-verified in round 12 (L01.html, L02.html, L05.html, index.html changed at the listed lines only; cited lines read again):"

OVERRIDE = {
    "SC1-d-r11-mutate-gate": ("PASS", "Folder hygiene resolved at 5db69a9: the six SC1a lab-twin mutants moved to ledgers/SC1/lab-mutants/ (git rename, content unchanged). ledgers/SC1/mutants/*.py now holds 68 grader mutants (66 earlier + r12_05, r12_06); `tools/mutate_graders.py --unit SC1 --seeds 0-9` counts all of them (68 total, see round-12 rows SC1-d-r12-mutant-survivors). The gate-count defect of round 11 is gone; the new survivors are a separate FAIL row."),
    "SC1-d-r10-mutant-folder-hygiene": ("PASS", "ls ledgers/SC1/mutants/ at 5db69a9 lists only m*.py, r*.py and the subfolders SC1-a-r10, SC1-a-r11; ledgers/SC1/lab-mutants/ holds the six SC1a-* files (ls output in ledgers/SC1/scripts/SC1-d-r12/out/mutate_SC1_0-9_r12b.txt lists 68 .py entries, none SC1a-*)."),
    "SC1-d-exemplar-a-scope": ("PASS", REVER + " project.html:462 now states that exemplar A is an excerpt with three of five sections and the appendix. ledgers/SC1/scripts/SC1-d-r12/exemplar_words.py (output out/exemplar_words.txt) gives exemplar A body 122 words (Summary 49, The checks 55, Discretization 18), which matches the stated 122, and three sections plus appendix (headings in project.html:467-512). The disclosure is accurate."),
    "SC1-d-calib-B": ("FAIL", "Blind scoring of exemplar B (ledgers/SC1/scripts/SC1-d-r12/blind_extract.py output /tmp copy, annotations and data-scores hidden): C1 4, C2 4, C3 4 on the first pass, C4 3, C5 4. Applying the rubric's own C3 level-3 element ('every number the report quotes is printed by run_report.py', the brief's Numbers bullet at project.html:443 and the C3 level-3 descriptor at project.html:447-458) gives C3 at most 2: exemplar B quotes 1.52 standard errors (project.html Checks passage, '0.016300 / 0.010735') and the derived sampling error -0.016300 (Discretization passage), neither printed by Lab 1 or Lab 3 (out/recompute_r12.txt). Official C3 4 is therefore 2 levels above the rule-based score, which fails the within-one-level calibration bar. Official C1, C2, C4, C5 agree with the blind scores."),
    "SC1-d-exemplar-a-annotations": ("FAIL", "One clause of the exemplar A annotations is wrong: the C3 level-2 annotation says the 1.52 derivation is not shown, but the passage shows it. The other annotations agree with the passage. See SC1-d-r12-exemplarA-annotation-C3 for the fix."),
    "SC1-d-pathwise-define-before-use": ("FAIL", REVER.replace("project.html read in full at 5db69a9; the delta lines 57, 462 and 584 read again", "L01.html:67 is byte-identical to 11d7077 (L01 hunks are lines 75, 112, 215 only)") + " 'pathwise' is first used at course/modules/SC/SC1/L01.html:67 ('(D1) is pathwise only at time 0'), and its only definition is in the conventions bullet at project.html:231, the last page of the unit. grep -n -i pathwise course/modules/SC/SC1/*.html gives L01:67 as the first hit."),
    "SC1-d-A1-label": ("PASS", LESSON + " project.html Statements (line 242) cites A0 as Definition 1.1 of Lesson 1 with continuous paths as in Theorem 2.5 and Remark 2.6 of Lesson 2; L01.html:58 is Definition 1.1 (standard Brownian motion); L02.html:289 is Theorem 2.5 and L02.html:303 is Remark 2.6. All three labels exist and are used as stated."),
    "SC1-d-A3-A4-usage": ("PASS", LESSON + " L05.html:63-69 lists A4(a) to A4(i) with (b) freezing, (c) hitting times, (g) joint measurability and (h) measurability at a stopping time, which are the parts P1 cites (project.html:246). L05.html:266-282 is Assumption A3 (strong Markov, bounded rho). The project's reliance is correct."),
    "SC1-d-L05-A4-i": ("PASS", LESSON + " project.html cites no A4(i) (grep 'A4' in project.html shows only A4(b), A4(c), A4(g), A4(h), A4 generally). A4(i) is at L05.html:69 and is unused by the project page."),
    "SC1-d-index-rung2-text": ("PASS", LESSON + " index.html:168 still reads 'Graded instantly in your browser' for the completion problem, and the only index.html change (line 69) is outside the cited line."),
    "SC1-d-lab2-attribution": ("PASS", REVER + " project.html:209 cites Corollary 1.4 of Lesson 6 as proved from Proposition 1.3. L06.html:75 is Proposition 1.3 (discrete reflection identity), L06.html:87-95 is Corollary 1.4 with statement #{M_N>=a}=#{S_N>=a}+#{S_N>a} (integer walk, so S_N>a is S_N>=a+1, which is the Lab 2 identity). L06 is byte-identical to 11d7077."),
}
FIXES = {
    "SC1-d-calib-B": "Remove the derived numbers 1.52 and -0.016300 from exemplar B (or print them from run_report.py), or amend the C3 level-3 descriptor to allow a quantity derived from printed values when its derivation is shown; then the official C3 score for B is re-derived by the rule.",
    "SC1-d-pathwise-define-before-use": "Define 'pathwise' in plain words at its first use, course/modules/SC/SC1/L01.html:67 (for example: 'a statement that holds on every path'), or reword that sentence without the term; the project conventions bullet at project.html:231 may keep its definition.",
    "SC1-d-exemplar-a-annotations": "Delete the clause 'and the passage does not say so' from the exemplar A C3 level-2 annotation in project.html.",
}
ADD_PREFIX_BY_LOC = ("course/modules/SC/SC1/grader", "grader/", "tests/labs", "ledgers/SC1/mutants", "plans/", "references/", "ledgers/SC1/scripts/SC1-d-r11")

rows = []
for r in prev["rows"]:
    r = dict(r)
    rid = r["id"]
    if rid in OVERRIDE:
        status, ev = OVERRIDE[rid]
        r["status"] = status
        r["evidence"] = ev
    elif r["status"] == "PASS":
        loc = r.get("location", "")
        if "project.html" in loc:
            r["evidence"] = REVER + " " + r["evidence"]
        elif any(x in loc for x in ("L0", "index.html", "cards.json")):
            r["evidence"] = "Carried from round 11 (cited lines unchanged at 5db69a9; file changed at other lines only): " + r["evidence"]
        elif loc.startswith(ADD_PREFIX_BY_LOC) or loc.startswith("repository") or "tools/" in loc:
            r["evidence"] = CARRY + " " + r["evidence"]
        else:
            r["evidence"] = CARRY + " " + r["evidence"]
    if r["status"] != "PASS":
        r["fix"] = FIXES.get(rid, r.get("fix", ""))
    rows.append(r)

ADD = []
def add(rid, check, location, status, evidence, fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix or ""
    ADD.append(row)

# --- round-12 FAIL rows (defects found this round)
add("SC1-d-r12-mutant-tiny-level", "2.6-mutation", "course/modules/SC/SC1/grader/test_project.py (reflection_tail tests, lines 221-248); ledgers/SC1/mutants/r12_05_tiny_level_guard_returns_one.py", "FAIL",
    f"Mutant r12_05 returns 1.0 for any level below 1e-6. It survives all 50 seeds 0-9 (out/mutate_SC1_0-9_r12b.txt: SURVIVED, killed_by None). The page's conventions bullet (project.html:234) states the value must agree with erfc(a/sqrt(2t)) to within 1e-10 for every a > 0 and t > 0. The suite only checks a = 1e-9 with tolerance 1e-8 (test_reflection_tail_tiny_level_gives_a_tail_near_one) and the instance levels. Numerical gap, out/tiny_and_samples_r12.txt: a = 1e-7, t = 2 gives |1 - erfc| = 5.64e-8; a = 1e-6, t = 0.5 gives 1.13e-6.",
    "Add a test over a grid of small levels, for example a in (1e-7, 1e-6, 1e-4) and t in (instance H, 2.0), requiring abs(sol.reflection_tail(a, t) - math.erfc(a / math.sqrt(2 * t))) <= 1e-10 (failure message names the 1e-10 closed-form property, no value). Then re-run tools/mutate_graders.py --unit SC1 --seeds 0-9.")
add("SC1-d-r12-mutant-tiny-time", "2.6-mutation", "course/modules/SC/SC1/grader/test_project.py (reflection_tail tests, lines 234-244); ledgers/SC1/mutants/r12_06_tiny_time_guard_returns_zero.py", "FAIL",
    "Mutant r12_06 returns 0.0 for any time below 1e-6. It survives seeds 0-9 (out/mutate_SC1_0-9_r12b.txt: SURVIVED). At a = 1e-3, t = 1e-7 the closed form is 0.0015654 (out/tiny_and_samples_r12.txt), so the mutant's error 1.57e-3 violates the 1e-10 statement at project.html:234. The only small-time test (test_reflection_tail_time_just_above_zero_is_accepted) checks a = instance level, where the true value is 0 to float precision.",
    "Add the same small-time case: a = 1e-3 with t in (1e-7, 1e-4), compared with math.erfc to 1e-10. Re-run mutate_graders for SC1.")
add("SC1-d-r12-exemplarB-brief", "2.9-structure-and-prose (report brief conformance of the exemplar that claims to follow it)", "course/modules/SC/SC1/project.html: exemplar B Summary (about line 532-534), The checks, Limitations; brief at lines 442-446", "FAIL",
    "Exemplar B says it is 'written to this brief' (project.html:462), but three brief elements are missing. (1) Summary must give 'the three results and the one number that shows each holds' (brief item 1, :442-446): B's Summary (69 words, out/exemplar_words.txt) names the closed form only, plus the one-step and nested numbers; P1 (reflection) and P3 (first passage) have no number there. (2) The checks must give 'the walk identity, each with its printed value' (item 3): B prints 1588 and 794 but never states the identity, which 1588 = 794 + 794 illustrates. (3) Limitations must say 'what the rounding does' (item 5): B's Limitations paragraph has no rounding statement.",
    "Give the Summary a number for P3 (for example the first-passage check or its closed form), state the walk identity in The checks with its two counts, and add one sentence on the rounding rule to Limitations. Keep the body within 400 to 900 words (B is 504 words now).")
add("SC1-d-r12-exemplarA-annotation-C3", "2.9-structure-and-prose (annotation accuracy)", "course/modules/SC/SC1/project.html: exemplar A annotation, 'Meets C3 level 2' li (annotation block of exemplar A)", "FAIL",
    "The annotation says the 1.52 'is derived from the printed 0.016300 and 0.010735, and the passage does not say so'. The exemplar A passage says 'which is 1.52 standard errors (0.016300 / 0.010735, both printed by Lab 1)', so it does show the division; only the claim 'printed by neither lab' is correct. The annotation misstates the passage.",
    "Delete the clause 'and the passage does not say so' from the exemplar A C3 annotation; keep 'printed by neither lab'.")

# --- round-12 PASS rows (checks run this round)
gates = [
    ("SC1-d-r12-gate-page-tools", "gate", "tools/check_pages.py, check_dag.py, check_projects.py --unit SC1", "PASS", "Run at 5db69a9 with .venv/bin/python: 'check_pages SC1: PASS', 'check_dag SC1: PASS', 'check_projects SC1: PASS' (exit 0 each; the commands are the repo tools, no script of mine)."),
    ("SC1-d-r12-gate-run-labs", "gate", "tools/run_labs.py --unit SC1", "PASS", "'run_labs SC1: PASS (11/11)' (exit 0); out/run_labs_SC1.txt holds the run's output."),
    ("SC1-d-r12-gate-run-graders", "gate", "tools/run_graders.py --unit SC1 --seeds 0-49", "PASS", "out/run_graders_0-49.txt: 'run_graders SC1: PASS (reference 50/50 seeds, slowest 0.6 s)', exit 0."),
    ("SC1-d-r12-gate-mutate", "gate", "tools/mutate_graders.py --unit SC1 --seeds 0-9", "FAIL", "out/mutate_SC1_0-9_r12b.txt: 66 of the 68 .py mutants are killed; r12_05 and r12_06 survive (their rows are SC1-d-r12-mutant-tiny-level and -tiny-time). Gate verdict FAIL: 'mutate_graders SC1: FAIL (66/68 killed)'.", "Kill r12_05 and r12_06 with the tests in the two rows above; re-run the gate until 68/68 (the gate then passes on the grader, not on the mutant set)."),
    ("SC1-d-r12-gate-page-smoke", "gate", "tools/page_smoke.py --unit SC1 --pages project", "PASS", "out/page_smoke_project.txt: 'in-browser grader: All 134 tests pass on seed 1482436701', 'page_smoke modules/SC/SC1/project.html: PASS', 'page_smoke SC1: PASS' (exit 0). Pyodide run of the same suite."),
    ("SC1-d-r12-gate-ruff-mypy", "gate", "ruff check ., ruff format --check ., mypy --no-incremental (repo root)", "PASS", "out/ruff_full.txt 'All checks passed!'; out/ruff_fmt.txt '559 files already formatted'; out/mypy_full.txt 'Success: no issues found in 385 source files' (exit 0 each)."),
    ("SC1-d-r12-gate-pytest", "gate", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_docs_figures.py", "PASS", "out/pytest_sc1_related.txt: all dots, exit 0."),
    ("SC1-d-r12-gate-verify-refs", "registry", "tools/verify_refs.py --offline; tools/verify_refs.py --unit SC1 (live)", "PASS", "out/verify_refs_offline.txt: 'offline integrity: 560 entries, 0 problems'; out/verify_refs_unit_SC1_live.txt: 'live re-verification of SC1: 1 of 560 entries, 0 problems' (live Open Library record for shreve2004stochastic, plain requests; no bot check hit)."),
    ("SC1-d-r12-collect-count", "2.6-tests-count", "course/modules/SC/SC1/grader/test_project.py (script ledgers/SC1/scripts/SC1-d-r12/collect_count.sh)", "PASS", "out/collect_count.txt: '134 tests collected' for QF_SEED 0, 1, 7 and 49 (script collect_count.sh, scratch copy of the panel layout with bm_checks.py = reference.py). The page states 134 at project.html:7, :225 and :296."),
]
for g in gates:
    add(*g)
ADD[-2]["fix"] = ADD[-2].get("fix", "")

add("SC1-d-r12-alternatives", "2.6-autograder-alternatives", "ledgers/SC1/scripts/SC1-d-r12/alternatives/alt_r12_1..5.py (run by run_alternatives_r12.py)", "PASS",
    "Five round-12 alternatives, each a complete bm_checks module with different routes: (1) reflection_tail via statistics.NormalDist (2(1-Phi(a/sqrt t))) and DP walk counts; (2) reflection_tail by Simpson's rule alone, 8000 intervals, no closed form, and index-based nested counts; (3) reflection_tail via 1-erf and statistics.stdev; (4) closed-form erfc with a cumulative-sum path build and the SE from p(1-p)/(N-1); (5) Fraction-exact SE and Pascal-row binomial counts. Each passes seeds 0-49 in out/alternatives_r12.txt (50/50 for 1 to 5 and for the reference). Alternative 2 was first written with a factor-2 error of mine, fixed before that run, so the run shows the fixed file.")
add("SC1-d-r12-mutants-new-r12-01-04", "2.6-mutation", "ledgers/SC1/mutants/r12_01..r12_04.py", "PASS",
    "Four new student-error mutants, each killed on seed 0 (out/mutate_SC1_0-9_full_r12.txt): r12_01 step-major draw order (killed by test_discrete_estimate_matches_an_explicit_count_on_the_stated_draws, the order the page states at project.html:232-233); r12_02 srw_terminal_count returns a probability (test_srw_counts_match_enumeration_for_n_up_to_12[3]); r12_03 over-constraint: a > n raises ValueError (test_srw_reflection_identity_holds_exactly[4]); r12_04 coarse maximum over the first n_coarse points (test_nested_counts_match_an_explicit_subsample_of_the_fine_paths).")
add("SC1-d-r12-mutants-all-existing", "2.6-mutation", "ledgers/SC1/mutants/*.py (68 files, tools/mutate_graders.py --unit SC1 --seeds 0-9)", "FAIL",
    "Every existing mutant (m01-m41, r8_01-r8_07, r9_01-r9_04, r10_01-r10_06, r11_01-r11_04, r12_01-r12_06) is re-run at 5db69a9: 66 killed, 2 survive (r12_05, r12_06). All earlier mutants remain killed on seed 0 (out/mutate_SC1_0-9_r12b.txt). The FAIL is the two survivors only.",
    "See SC1-d-r12-mutant-tiny-level and SC1-d-r12-mutant-tiny-time.")
add("SC1-d-r12-sample-20-seeds", "2.6-autograder-instances", "course/modules/SC/SC1/grader/instance.py; ledgers/SC1/scripts/SC1-d-r12/tiny_and_samples_r12.py", "PASS",
    "Seeds 0, 3, ..., 57 (20 seeds): every instance valid (H in 0.25-4.0, a in 0.25-2.5, n_steps in 4-256, n_paths in 400-800, n_steps*n_paths <= 200000; out/tiny_and_samples_r12.txt). Levels are 20 distinct values, and the seed-by-seed tail values are 20 distinct numbers (answers change, not labels).")
add("SC1-d-r12-blind-exemplar-A", "2.3-calibration", "project.html exemplar A (blind text: ledgers/SC1/scripts/SC1-d-r12/blind_extract.py)", "PASS",
    "Blind rule-based scores from the annotation-free text (the verifier had printed lines 464-471, 518-523 and 580-600 earlier, which included the verdict paragraphs, so this is disclosed as not fully blind): C1 1 (no numbered assumptions for any result), C2 2 (P1 skips the restart symmetry with no gap named; P2, P3 absent), C3 2 (decimals 0.0865, 0.0595 have no rounding statement), C4 2 (The results hold for every grid, as the run shows), C5 1 (no numbers in Discretization). Official 1,2,2,2,1: within one level on every criterion.")
add("SC1-d-r12-blind-exemplar-B", "2.3-calibration", "project.html exemplar B (blind text)", "PASS",
    "Blind rule-based scores: C1 4 (A3 tied to rho <= t; A4(b), (c), (g), (h) named), C2 4 (steps justified; the 'so B_t >= a implies M_t >= a' step is by definition), C3 2 on strict reading (derived 1.52 and -0.016300, see SC1-d-calib-B; a first pass gave 4), C4 3 (no statement on the continuum), C5 4. The official score 4,4,4,3,4 differs on C3 only, which is the FAIL row SC1-d-calib-B.")
add("SC1-d-r12-annotations-B-accuracy", "2.3-calibration", "project.html exemplar B annotations", "PASS",
    "Each annotation's claim checked against the passage: the C4 level-4 miss (no continuum statement) matches the passage; the C2 level-4 names (A4(b), (c), (g), (h), A3) match the P1 text; the C5 level-4 claim (every grid, direction, SE at each grid) matches the discretization numbers, which equal the Lab 3 expected block (project.html Lab 3 output).")
add("SC1-d-r12-exemplarB-numbers-values", "2.2-numbers", "project.html exemplar B Summary, The checks, Discretization", "PASS",
    "Every value in B recomputed independently (out/recompute_r12.txt): tail 0.086497; Simpson difference below 1e-14 (Lab 1 prints 9.13e-15); one-step 0.059548, SE 0.010735, target 0.043248, target SE 0.009218, band 0.048142, difference 0.016300; grid estimates, SEs, tail-minus-estimate for 1, 4, 16, 64, 256 steps; nested counts 35, 29, 27, 22 against 40; walk counts 1588 and 794. All equal. The only issue is the printing rule (SC1-d-calib-B).")
add("SC1-d-r12-page-vs-twin", "2.5-labs", "project.html Labs 1-3 vs tests/labs/SC1/lab-SC1-project-{1,2,3}.py (script page_vs_twin.py, out/page_vs_twin.txt)", "PASS",
    "Lab 1 and Lab 3 page code equals the twin except one trailing newline (page code has none); Lab 2 page code equals the twin with the two blanks (___) replacing the identity and the comparison, every other line identical (completion rule). Each expected block equals the twin's output under python -I -W error (out/page_vs_twin.txt: 'expected == output: True' for 1, 2, 3).")
add("SC1-d-r12-lab-numbers", "2.2-numbers", "project.html Labs 1-3 and interpretations (recompute_r12.py)", "PASS",
    "Lab 1: 1.52 = 0.016300/0.010735 (1.5184) and 1.77 = 0.016300/0.009218 (1.7683) reproduce. Lab 3: 64-step estimate is 0.1398 SE above the tail (page 0.14); one-step printed 0.026948 minus target 0.043248 equals -0.016300 (page sign and value); each of the five grids' estimate is within 5 SE of the tail (true for 1, 4, 16, 64, 256). Lab 2: n=6, a=2: 29, 22, 7 (independent DP, out/recompute_r12.txt).")
add("SC1-d-r12-walk-identity", "2.4-mathematics", "project.html Lab 2 and Lab 3 walk counts; L06.html Corollary 1.4", "PASS",
    "Independent DP over (position, running max) gives 1588 walks reaching 3 of 2^12 = 4096 and 794 ending at 3 or above for n=12; 29, 22, 7 for n=6, a=2. The identity #{max>=a} = #{S_n>=a} + #{S_n>=a+1} holds at n=12, a=3 (1588 = 794 + 794, out/recompute_r12.txt).")
add("SC1-d-r12-P1-proof", "2.4-mathematics", "project.html Appendix P1 (exemplar B; statement at project.html:246-248)", "PASS",
    "Re-derived each step of P1: K = {tau <= t} = {M_t >= a} by continuity and the intermediate value theorem; P(tau = t) = 0 from B_t normal (A0, Definition 1.1); freezing with f(z,y) = 1{z2=1}1{y(z1)<0} gives fbar(z) = 1/2 1{z2=1}1{z1>0} because B~ is standard BM independent of F_rho (A3); the identity P(K) = P(B_t>=a) + P(K)/2 gives P(M_t>=a) = 2P(B_t>=a). Each use names A3, A4(b), A4(c), A4(g) or A4(h), which exist at L05.html:63-69 and L05.html:266-282.")
add("SC1-d-r12-P2-P3-proofs", "2.4-mathematics", "project.html exemplar B P2 and P3 (line 587-590) and statements (lines 250-258)", "PASS",
    "P2: erfc(x) = 2(1 - Phi(x sqrt 2)) by w = z/sqrt2, so erfc(a/sqrt(2t)) = 2(1 - Phi(a/sqrt t)). P3: {tau_a <= t} = {M_t >= a} for a>0 by continuity; P(tau_a < inf) = lim erfc(a/sqrt(2n)) = erfc(0) = 1 by continuity from below. All correct.")
add("SC1-d-r12-notation", "2.13-notation", "project.html math (259 delimited expressions); notation/notation.json", "PASS",
    "Registered symbols (notation.json symbols: T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q): project.html uses T only inside the sentence that says T has another meaning (project.html Conventions and exemplar B 'not T'), and Phi only as the standard normal CDF (6 uses). Registered macros used (\\Prob, \\Normal, \\indic) exist in notation.json. Local symbols B, M, H, a, t, tau, rho, K, N (path count, defined at project.html:57), n and F are defined where used.")
add("SC1-d-r12-hours", "2.6-hours", "project.html table#hours (lines 271-282)", "PASS",
    "The table sums 2 + 3 + 10 + 8 + 3 + 2 = 28 (data-hours-project=28). Independent estimate: rung 1 about 1 h, rung 2 about 0.5 h, three proofs 8-12 h, engine plus tests 6-10 h, report 3 h, self-assessment 2 h: total about 24.5 h, which is -12.5% of 28, inside the 30% bar.")
add("SC1-d-r12-banned-and-process-words", "2.9-prose", "project.html, tests/labs/SC1/lab-SC1-project-{1,2,3}.py, grader/*.py", "PASS",
    "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, important to note, studies show, experts agree, well known, obviously, clearly: 0 hits. 'builder', 'verifier', 'REQUEST', 'unit report': 0 hits. 'round' occurs on 35 lines, all as 'rounded' or round(), with no process sense. Ellipses: none in prose.")
add("SC1-d-r12-pathwise-only-l01", "2.9-define-before-use", "course/modules/SC/SC1/L01.html:67 (see SC1-d-pathwise-define-before-use)", "PASS",
    "Scope note only: the project page itself defines 'pathwise' before any use on that page (project.html:231 is the first occurrence on the page; 429 and 455 use it afterward). The failure is on L01.html, recorded in SC1-d-pathwise-define-before-use.")
add("SC1-d-r12-spec-tolerance-and-errors", "2.6-spec", "project.html Conventions (lines 231-237) vs grader/test_project.py (lines 185-188, 221-245) and reference.py", "PASS",
    "Tolerance 1e-10 (project.html:234) equals test_project.py:187; the ValueError list (project.html:237) equals reference.py and the must_raise tests (n_steps<1, n_paths<2, n_fine<1, n_coarse<1, non-divisor, n<1, a<1, a<=0, t<=0). The page's note that other invalid inputs may raise any exception matches the tests (no type assertion outside the named conditions). The architect deviation from plan 5.5 (1e-12 in plan) is recorded in round 11 and is not repeated here.")
add("SC1-d-r12-reading-and-registry", "2.1-citations", "project.html reading list (line 621); references/references.json:20734", "PASS",
    "The key shreve2004stochastic record: title 'Stochastic Calculus for Finance II', year 2004, Shreve, Steven E., book, ISBN 9781475742961; the page cites it 'at book level' with no passage. The live check (out/verify_refs_unit_SC1_live.txt) returned 0 problems for SC1's one entry. The Karatzas & Shreve string is not cited anywhere on project.html.")
add("SC1-d-r12-interpretation-claim-lab3-grid-direction", "2.2-numbers and grades", "project.html Lab 3 interpretation (line 429) and the exemplar A annotation", "PASS",
    "The Lab 3 interpretation says a single seed cannot order the rows by bias; the printed values (tail minus estimate 0.026948, 0.037215, 0.020788, -0.001799, 0.004361) confirm that ordering is not monotone in n, so the claim is accurate.")

# mutants from the r12b gate output
mutants = []
for line in (root / OUT / "mutate_SC1_0-9_r12b.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" or status == "SURVIVED" else killed.strip()
    mutants.append({"name": name, "description": desc, "killed_by": killed_by})

all_rows = rows + ADD
ids = [r["id"] for r in all_rows]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
verdict = "FAIL" if any(r["status"] != "PASS" for r in all_rows) else "PASS"
counts = {s: sum(1 for r in all_rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 12 (did not build SC1; re-read the whole project page, the grader, the labs and the delta 11d7077..5db69a9)",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9 (round-11 pin)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-SC1-d",
    "scratch": "/tmp/sc1d-r12/ (exemplar blind text, scratch copies for collect-only and the alternatives run); durable scripts and outputs under ledgers/SC1/scripts/SC1-d-r12/",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": all_rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 12. Verdict FAIL: "
        "(1) SC1-d-pathwise-define-before-use is unchanged (L01.html:67 first use); "
        "(2) two new grader survivors r12_05 (tiny-level guard) and r12_06 (tiny-time guard) violate the 1e-10 statement at project.html:234 and survive seeds 0-9; "
        "(3) exemplar B fails three brief elements (Summary three results; walk identity; rounding in Limitations) and quotes derived numbers (1.52, -0.016300) that the rubric's C3 level 3 excludes, so the official C3 4 for B is not calibrated; "
        "(4) exemplar A annotation misstates the passage (1.52 derivation is shown). "
        "Round-11 FAILs that are fixed: mutate-gate and folder hygiene (SC1a files moved to lab-mutants/), exemplar A scope (now disclosed as an excerpt). "
        "Exemplar blind scoring: A matches official 1,2,2,2,1; B blind 4,4,4,3,4 on the first pass, 4,4,2,3,4 on the strict rule (C3 element). "
        "Architect deviations (tolerance 1e-10 vs plan 1e-12; exemplar data-level naming reversed vs plan 5.4; plan 5.7(4) draw order treated as a mutant, Ruling 10) are kept as PASS rows from round 11, not re-litigated. "
        "Blind-scoring caveat: before scoring, this verifier printed the exemplar verdict paragraphs and two annotation blocks with sed (for location), so the blind scores are not fully blind; the blind text was then extracted with annotations and data attributes removed, and scored from that text."
    ),
    "summary": (
        f"SC1 slice d round 12 on 5db69a9: verdict {verdict}. Rows {len(all_rows)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, UNVERIFIABLE {counts['UNVERIFIABLE']}. "
        f"Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed (r12_05, r12_06 survive). Alternatives: five new round-12 alternatives and the reference pass seeds 0-49."
    ),
}
out_path = root / "ledgers/SC1/SC1-d.json"
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out_path, verdict, counts, len(mutants))
