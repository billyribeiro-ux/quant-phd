# Builds ledgers/FC2/FC2-d.json (round 19). Carry rows are only emitted after their cited old ranges are proved
# unchanged by out/line_map_r19.json (difflib, aa659725 -> 95f3f8cb).
import json, re, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyD19-FC2-d"
S = f"{ROOT}/ledgers/FC2/scripts/FC2-d-r19"
M = json.load(open(f"{S}/out/line_map_r19.json"))
PREV = json.load(open("/Users/billyribeiro/.fanout/frags/D-FC2-d.round17.json"))
PREV_ROWS = {r["id"]: r for r in PREV["rows"]}
CHANGED = {f: {int(k) for k, v in M[f]["map"].items() if not v[1]} for f in M}
SHORT = {"project.html": "course/modules/FC/FC2/project.html", "test_project.py": "course/modules/FC/FC2/grader/test_project.py"}

def nr(path, a, b=None):
    """New line range for old lines a..b of a file; raises if any cited old line changed."""
    b = a if b is None else b
    mp = M[path]["map"]
    for k in range(a, b + 1):
        if k in CHANGED[path]:
            raise SystemExit(f"CHANGED {path}:{k} inside cited range {a}-{b}")
    lo, hi = mp[str(a)][0], mp[str(b)][0]
    assert hi - lo == b - a, (path, a, b, lo, hi)
    return f"{lo}" if a == b else f"{lo}-{hi}"

PH = "course/modules/FC/FC2/project.html"
TP = "course/modules/FC/FC2/grader/test_project.py"
CARRIED_FILES = ("course/modules/FC/FC2/project.html (cited lines unchanged)")
rows, carried = [], []

def carry(rid, loc, extra=""):
    prev = PREV_ROWS[rid]
    assert prev["status"] == "PASS", rid
    ev = ("Carried from round 17 (cited lines byte-identical since the previous pin aa659725, proved line-for-line "
          "by out/line_map_r19.json; the cited ranges contain no changed line): " + prev["evidence"] + (" " + extra if extra else ""))
    rows.append({"id": rid, "check": prev["check"], "location": loc, "status": "PASS", "evidence": ev})
    carried.append(rid)

def row(rid, check, loc, ev, status="PASS"):
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

def L(path, a, b=None):
    return f"{SHORT.get(path, path)}:{nr(path, a, b)}"

# ---- carried: cited subject byte-identical (mapped) ----
carry("fc2d-ladder-claims", f"{PH}:{nr('course/modules/FC/FC2/project.html', 40, 50)}")
carry("fc2d-lab1-hypothesis-terms", f"{PH}:{nr('course/modules/FC/FC2/project.html', 55)}")
carry("fc2d-r6-project-line335", f"{PH}:{nr('course/modules/FC/FC2/project.html', 37)}, :{nr('course/modules/FC/FC2/project.html', 285)}, :{nr('course/modules/FC/FC2/project.html', 335)}, :{nr('course/modules/FC/FC2/project.html', 495)}, :{nr('course/modules/FC/FC2/project.html', 511)}")
carry("fc2d-r7-project-anchor-links", f"{PH}:{nr('course/modules/FC/FC2/project.html', 37)}, :{nr('course/modules/FC/FC2/project.html', 282)}")
carry("fc2d-hours", f"{PH}:{nr('course/modules/FC/FC2/project.html', 339, 357)}; course/modules/FC/FC2/index.html:29 (file unchanged)")
carry("fc2d-reading-theorem-locator", f"{PH}:{nr('course/modules/FC/FC2/project.html', 652, 660)}")
carry("fc2d-references-no-locator", f"{PH}:{nr('course/modules/FC/FC2/project.html', 652, 660)}")
carry("fc2d-rubric-observable", f"{PH}:{nr('course/modules/FC/FC2/project.html', 504, 516)}")
carry("fc2d-exemplar-numbers", f"{PH}:{nr('course/modules/FC/FC2/project.html', 520, 583)}")
carry("fc2d-exemplar-annotations", f"{PH}:{nr('course/modules/FC/FC2/project.html', 520, 641)}")
carry("fc2d-exemplar-brief-structure", f"{PH}:{nr('course/modules/FC/FC2/project.html', 489, 499)} (brief), :{nr('course/modules/FC/FC2/project.html', 518)} (intro sentence), :{nr('course/modules/FC/FC2/project.html', 525, 573)} (B headings), :{nr('course/modules/FC/FC2/project.html', 589, 626)} (A headings)")
carry("fc2d-spec-explanation-labels", f"{PH}:{nr('course/modules/FC/FC2/project.html', 301)} (spec), :{nr('course/modules/FC/FC2/project.html', 327)} (P4), :{nr('course/modules/FC/FC2/project.html', 329)} (model-free definition); {TP}:{nr(TP, 42, 43)}, {nr(TP, 674, 686)}")
carry("fc2d-grader-messages", f"{TP}:{nr(TP, 450, 650)}; {PH}:{nr('course/modules/FC/FC2/project.html', 305, 316)}")
carry("fc2d-grader-instance-validity", "course/modules/FC/FC2/grader/instance.py:41-60, 102-111, 118-131 (file unchanged)")
carry("fc2d-grader-instance-diversity", "course/modules/FC/FC2/grader/instance.py:6-9, 134-142 (file unchanged)")
carry("fc2d-r5-grader-exact-ties", f"{TP}:{nr(TP, 271, 291)}, {nr(TP, 795, 822)}")
carry("fc2d-r6-new-tie-tests", f"{TP}:{nr(TP, 809, 850)}")
carry("fc2d-new-tests", f"{TP}:{nr(TP, 682, 686)}")
carry("fc2d-r16-lab-docstrings-L04-L06", "tests/labs/FC2/lab-FC2-L04-1.py:7-11; tests/labs/FC2/lab-FC2-L06-1.py:4-9 (files unchanged)")
carry("fc2d-r16-equivalence-wording-scope", "ledgers/FC2/equivalent/README.md (file unchanged)")
carry("fc2d-r15-mut-c-explanation-net-as-gross", "ledgers/FC2/equivalent/r15_c_parity_explanation_prints_gross_where_net_belongs.py; ledgers/FC2/equivalent/README.md (files unchanged)")
carry("fc2d-r15-mut-d-convexity-explanation-side", "ledgers/FC2/equivalent/r15_d_convexity_explanation_reverses_the_chord_side.py (file unchanged)")
carry("fc2d-curriculum-scope", "curriculum/02-economics-finance-core.yaml:425-431 (file unchanged since aa659725)")
carry("fc2d-r14-delta", f"{PH}:{nr('course/modules/FC/FC2/project.html', 518)}; {TP}:{nr(TP, 682, 686)}; tests/labs/FC2/lab-FC2-L04-1.py; tests/labs/FC2/lab-FC2-L06-1.py; ledgers/FC2/equivalent/ (unchanged)")

O = f"ledgers/FC2/scripts/FC2-d-r19/out"
MUT = f"{O}/mutate_graders_FC2_0-49_r19.out"
def gate(rid, check, loc, out, extra=""):
    row(rid, check, loc, f"{check} -> see {O}/{out}. {extra}".strip())

gate("fc2d-gate-check-projects", "tools/check_projects.py --all (FC2 line)", "tools/check_projects.py", "check_projects.out", "Output 'check_projects FC2: PASS'.")
gate("fc2d-gate-check-pages", "tools/check_pages.py --all (FC2 line)", "tools/check_pages.py", "check_pages.out", "Output 'check_pages FC2: PASS'.")
gate("fc2d-gate-check-dag", "tools/check_dag.py --all (FC2 line)", "tools/check_dag.py", "check_dag.out", "Output 'check_dag FC2: PASS'.")
gate("fc2d-gate-run-labs", "tools/run_labs.py --unit FC2", "course/modules/FC/FC2/*.html lab sections; tests/labs/FC2", "run_labs.out", "Output 'run_labs FC2: PASS (11/11)', exit 0.")
gate("fc2d-gate-page-smoke", "tools/page_smoke.py --unit FC2 --pages modules/FC/FC2/project.html", "course/modules/FC/FC2/project.html", "page_smoke_project_r19.out", "Output 'page_smoke FC2: PASS', exit 0 (also page_smoke_FC2.out).")
gate("fc2d-gate-run-graders", "tools/run_graders.py --unit FC2 --seeds 0-49", "course/modules/FC/FC2/grader", "run_graders.out", "Output 'run_graders FC2: PASS (reference 50/50 seeds)', exit 0; seeds 50-83 reference 34/34 (reference_50-83_r19.out).")
gate("fc2d-gate-ruff", "ruff check and ruff format --check on grader and tests/labs/FC2", "course/modules/FC/FC2/grader; tests/labs/FC2", "ruff_check.out", "'All checks passed!' and '15 files already formatted', exit 0 both.")
row("fc2d-gate-mypy", ".venv/bin/mypy --no-incremental (repo, strict) and grader strict on a staged copy (reference.py as scanner.py)", "pyproject.toml; course/modules/FC/FC2/grader",
    f"Repo: 'Success: no issues found in 386 source files' ({O}/mypy_repo.out). Grader: run on the bare grader dir fails with import-not-found for 'scanner' (the grader's solution is staged under that name at grading time, so this is a harness artefact, recorded in {O}/mypy_grader.out); on a staged copy (test_project.py, instance.py, scanner.py = reference.py) 'Success: no issues found in 3 source files' ({O}/mypy_grader_staged.out).")
gate("fc2d-gate-pytest", "pytest tests -q -k FC2 (FC2-relevant tests)", "tests/", "pytest_FC2.out", "12 tests, exit 0. Out of slice: a broader pytest -k project run also selects tests/test_lx1_project_lab3.py (LX1, not FC2) which fails in test_a_population_sd_variant_of_the_two_pass_check_raises (see pytest_relevant.out); recorded as a note, not an FC2 row.")
gate("fc2d-gate-verify-refs", "tools/verify_refs.py --offline", "references/references.json", "verify_refs.out", "'offline integrity: 560 entries, 0 problems', exit 0.")
row("fc2d-collect-count", "pytest --collect-only on the staged grader for QF_SEED 0..49 and 50..83", "course/modules/FC/FC2/project.html:322; course/modules/FC/FC2/grader/test_project.py",
    f"Page states 105 checks at project.html:322 ('collects <strong>105 checks</strong>... the count is 105 for each of the seeds 0 to 49'). Re-counted: 105 on every seed 0-49 ({O}/collect_per_seed_r19.out) and 105 on every seed 50-83 ({O}/collect_50-83_r19.out). Only grep hits for 99/105 counts in FC2 pages: project.html:322 and none stale elsewhere in course/ or tools/.")
row("fc2d-seeds-84", "reference passes and suite collects on seeds 0-83", "course/modules/FC/FC2/grader/test_project.py",
    f"Reference scanner passes 50/50 on seeds 0-49 (run_graders.out) and 34/34 on seeds 50-83 ({O}/reference_50-83_r19.out). Collect 105 on all 84 seeds.")
row("fc2d-starter-fails", "starter.py fails the suite on every seed", "course/modules/FC/FC2/grader/starter.py",
    f"Starter scanner: 0 pass, 50 fail on seeds 0-49 ({O}/starter_reference_r19.out).")
row("fc2d-alternatives", "eight alternative correct implementations pass all seeds", "ledgers/FC2/scripts/FC2-d-r14/alts/alt1..alt5, FC2-d-r14/alt6_round6_alternative.py, FC2-d-r15/alts/alt7_integer_scaled.py, alt8_decimal_60.py",
    f"Each alternative run as scanner.py against the CURRENT grader (new one-strike tests and 6.5-chord test included), seeds 0-49, same pytest flags as run_graders: 50/50 pass for all eight ({O}/alts_r19.out; runner {S}/run_alts_r19.sh).")
row("fc2d-alt-r14-float-no-cutoff", "float-epsilon alternative (no exact cutoff) passes the exact-tie tests", "ledgers/FC2/scripts/FC2-d-r14/alts/alt3_float_epsilon_cutoff.py; course/modules/FC/FC2/grader/test_project.py (exact-tie tests)",
    f"alt3_float_epsilon_cutoff passes 50/50 against the current grader ({O}/alts_r19.out), including the new 6.5-chord test (test_project.py:884-891).")
row("fc2d-alt-r6-overconstraint", "round-6 alternative passes", "ledgers/FC2/scripts/FC2-d-r14/alt6_round6_alternative.py",
    f"alt6_round6_alternative passes 50/50 against the current grader ({O}/alts_r19.out).")
row("fc2d-mutate-builder", "tools/mutate_graders.py --unit FC2 --seeds 0-49 (all standing mutants)", "ledgers/FC2/mutants/ (111 files)",
    f"Re-run on pin 95f3f8cb: 'mutate_graders FC2: PASS (111/111 killed)', exit 0 ({MUT}). r17_a is killed by test_one_strike_convexity_rejects_df_below_the_range, r17_c by test_one_strike_convexity_rejects_two_calls_for_one_strike, r17_d by test_convexity_half_cent_tie_on_a_chord_of_6_point_5_rounds_once_up (all listed in {MUT}). Previous FAIL (108/111) resolved.")

def killed(name):
    for line in open(f"{S}/out/mutate_graders_FC2_0-49_r19.out", encoding="utf-8"):
        if line.startswith(f"KILLED {name}"):
            return line.split(" -> ")[-1].strip()
    raise SystemExit("not killed: " + name)

group = {
    "fc2d-mut-new-r14": ["r14_a", "r14_b", "r14_c", "r14_d", "r14_e"],
    "fc2d-mut-v03": ["v03"], "fc2d-mut-v04": ["v04"], "fc2d-mut-v05": ["v05"], "fc2d-mut-v06": ["v06"],
    "fc2d-mut-v01-boundary": ["v01"], "fc2d-mut-v02-labels": ["v02"],
    "fc2d-r5-mut-swap-weights": ["r5_b"], "fc2d-r5-mut-skip-first": ["r5_c"],
    "fc2d-r6-mut-new": ["r6_a", "r6_b", "r6_c"], "fc2d-r7-mut-new": ["r7_a", "r7_b", "r7_c"],
    "fc2d-r16-mut-a-parity-explanation-names-P5": ["r16_a"], "fc2d-r16-mut-b-convexity-without-convex-word": ["r16_b"],
    "fc2d-r16-mut-c-float-chord-weights": ["r16_c"], "fc2d-r15-mut-b-convexity-names-P4": ["r15_b"],
}
import os
for rid, keys in group.items():
    parts = []
    for k in keys:
        names = [f for f in os.listdir(f"{ROOT}/ledgers/FC2/mutants") if f.startswith(k + "_") or f == k + ".py"]
        assert len(names) == 1, (k, names)
        parts.append(f"{names[0]} -> {killed(names[0])}")
    status = "PASS"
    row(rid, "standing mutant killed by the grader (re-run, mutate_graders FC2 0-49)", f"ledgers/FC2/mutants/{keys[0]}*",
        "KILLED in " + MUT + ": " + "; ".join(parts))

assert not any(f.startswith("r5_d") for f in os.listdir(f"{ROOT}/ledgers/FC2/mutants"))
row("fc2d-r5-mut-direction", "ledgers/FC2/mutants has no r5_d file (direction mutant absent, as before)", "ledgers/FC2/mutants/",
    "os.listdir: no file starting r5_d (checked in the r19 build step).")
row("fc2d-r15-mut-a-parity-explanation-direction", "wording-only parity explanation mutant is an equivalent (ruling 34)", "ledgers/FC2/equivalent/r15_a_parity_explanation_reverses_the_positive_gap_trade.py; ledgers/FC2/equivalent/README.md",
    "Moved from mutants/ to equivalent/ (ruling 34, file present, not in the standing mutant set; mutate_graders reports 111, none is r15_a). README unchanged since aa659725.")
row("fc2d-r15-alt-integer-decimal", "alt7 integer-scaled and alt8 decimal-60 alternatives pass", "ledgers/FC2/scripts/FC2-d-r15/alts/alt7_integer_scaled.py; alt8_decimal_60.py",
    f"Both pass 50/50 against the current grader ({O}/alts_r19.out).")
row("fc2d-r16-explanation-check-no-overconstraint", "explanation-label check does not over-constrain correct wording", "course/modules/FC/FC2/grader/test_project.py:705-717 (test_scan_explanations_are_nonempty_and_name_the_rule); ledgers/FC2/scripts/FC2-d-r19/out/alts_r19.out",
    f"The label-set check still kills r15_b (mutate run) and the eight alternatives, which use their own wording, pass 50/50 ({O}/alts_r19.out).")
row("fc2d-r17-equivalent-probe-one-strike-scan-df", "one-strike scan df probe is behaviourally equivalent (scan re-validates via convexity_violations)", "ledgers/FC2/scripts/FC2-d-r17/equiv_candidates/r17_b_scan_skips_df_check_for_one_strike_chain.py; course/modules/FC/FC2/grader/test_project.py:651-680 (one-strike tests)",
    f"Re-probed this round: scan with its own df/strike checks removed for one-strike chains still raises ValueError because scan calls convexity_violations, which validates df, strikes and lengths unconditionally. Probes scan_df_checked_only_multi_strike and scan_strike_checked_only_multi_strike pass the whole suite and the candidate tests (ledgers/FC2/scripts/FC2-d-r19/out/probe_scan_one_strike_r19.out, candidate_scan_probes_r19.out): equivalent, not a finding. The early-return probe scan_early_return_one_strike is killed by test_one_strike_chain_scans_without_convexity.")
row("fc2d-r17-plain-float-parity", "plain-float parity gap mutant r17_e is killed", "ledgers/FC2/mutants/r17_e_parity_gap_in_plain_float.py",
    "KILLED in " + MUT + ": " + killed("r17_e_parity_gap_in_plain_float.py"))
row("fc2d-r17-new-tie-test-no-overconstraint", "new 6.5-chord tie test does not over-constrain", f"{TP}:895-902",
    f"The test asserts an exact half-cent gross of 1 at strike 2 on the chain [1,2,7]/[7,7,4]/[8,9,11]. Reference passes all 84 seeds; all eight alternatives (including float-epsilon alt3 and decimal alt8_decimal_60) pass 50/50 ({O}/alts_r19.out). Over-constraint not found.")
row("fc2d-r17-test-comment-856", "test_project.py comment on the non-dyadic tie is true", f"{TP}:884-888",
    f"The corrected comment says 5/6 and 1/6 are not exact in binary floating point and that converting those float weights to Fraction loses the tie. Checked: 5/6 and 1/6 are not exact floats (ledgers/FC2/scripts/FC2-d-r19/out/float_claims_r19.out: Fraction(5/6) != 5/6 and Fraction(1/6) != 1/6); Fraction(float weights)*2 + Fraction(float weights)*5 = 90071992547409921/36028797018963968 != 5/2, so the tie is lost (float_claims_r19.out). The previous false claim (float keeps the tie) is gone. Plain float on this chain gives exactly 2.5 (float_claims_r19.out), which the comment no longer claims either way.")
row("fc2d-r17-plain-float-convexity", "plain-float convexity chord (r17_d) is killed by a test the fixer added", f"{TP}:895-902; course/modules/FC/FC2/project.html:310",
    "KILLED: r17_d_convexity_chord_and_gross_in_plain_float.py -> " + killed("r17_d_convexity_chord_and_gross_in_plain_float.py") + f" ({MUT}). Test comment arithmetic re-derived: 5/6*7 + 1/6*4 evaluates to 6.500000000000001 in float, while the single-division form (5*7+1*4)/6 gives 6.5 ({O}/float_form_check_r19.out); the test comment states the first form, which is the chord weighting written on the line above it. Float gross for r17_d: int((-sd+0.5)//1) = 0 (float_claims_r19.out). project.html:310 states exact fractions with one rounding (text unchanged since aa659725, old line 308); the test and the mutant agree with it. 8 alternatives pass the test.")
row("fc2d-spec-errors-scope", "every named condition is checked in every function that receives its input (project.html:309-316), including one-strike chains", f"{PH}:307-316 (Constraints, money sentence at 310, named conditions 311-316); {TP}:651-680 (five one-strike tests)",
    "Previous FAIL: no one-strike test for convexity_violations df, zero-strike or two-call checks; mutants r17_a and r17_c survived. Now: test_one_strike_convexity_rejects_df_below_the_range (651), _df_above_the_range (658), _a_zero_strike (664), _two_calls_for_one_strike (670), _accepts_one_matching_quote_at_the_df_ends (676). r17_a and r17_c are KILLED (mutate run). Other functions: parity_gap df and zero strike covered at test_project.py:294-320; scan df, strike, length and cost covered at 450-620 and 641-650 for multi-strike chains and one-strike length and cost (600-619, 641-649). One-strike scan df/strike is checked through convexity_violations, which scan calls unconditionally (probe evidence above), so it is equivalent, not a gap.")
row("fc2d-rubric-calib-A", "blind calibration of exemplar A (rubric C1..C5) matches the page within one level", "course/modules/FC/FC2/project.html:587-640 (article#exemplar-a, data-scores 2,1,2,2,1); ~/.fanout/blind/FC2-d.json",
    "Blind scores A=[2,1,2,2,1]; page data-scores 2,1,2,2,1: identical on every criterion (within one level). Blind file produced by a separate scorer per ruling 23 (not verified by this verifier).")
row("fc2d-rubric-calib-B", "blind calibration of exemplar B matches the page within one level", "course/modules/FC/FC2/project.html:523-586 (article#exemplar-b, data-scores 4,4,3,3,3); ~/.fanout/blind/FC2-d.json",
    "Blind scores B=[4,3,3,3,3]; page data-scores 4,4,3,3,3: C1 4=4, C2 3 vs 4 (one level), C3-C5 3=3. Within one level on every criterion, so PASS by VERIFIER_RULES calibration rule 2. Blind file records C2 and other judgement calls.")
row("fc2d-lab1", "lab 1 page block and expected output match the twin; docstring tie claims match the code", "course/modules/FC/FC2/project.html:56-165 (block at 56, docstring lines 56-61); tests/labs/FC2/lab-FC2-project-1.py",
    f"Page block equals twin (page_twin_r19.out: page==twin True). Twin runs under python -I -W error, exit 0. Expected block equals twin stdout (checked in this round). Docstring now says a signed gap ties toward +inf and a gross amount ties up in magnitude; the code is round_cents(gap) = floor(x+1/2) for the signed gap and round_cents(abs(gap)) for the gross (lab-FC2-project-1.py:27-29, 62). Matches.")
row("fc2d-lab2", "lab 2 page block equals twin apart from the three blanks; docstring tie claims match the code", "course/modules/FC/FC2/project.html:170-280; tests/labs/FC2/lab-FC2-project-2.py",
    "Page block differs from the twin only at the three blanked lines (lines 59, 61, 74: parity_gap call, two net expressions) (page_twin_r19.out, diff above). Twin exit 0 under -I -W error. Docstring matches round_cents (defined at lines 25-27; used for the signed gap and the gross at lines 60 and 73).")
row("fc2d-lab3", "lab 3 page block and expected output match the twin; docstring tie claims match the code", "course/modules/FC/FC2/project.html:380-488; tests/labs/FC2/lab-FC2-project-3.py",
    "Page block equals twin (page==twin True). Twin exit 0 under -I -W error; expected block equals stdout. Docstring matches the code as for lab 1.")
row("fc2d-lab-twins-pure", "twins are pure stdlib and run alone under python -I -W error", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py",
    f"python -I -W error on each twin: exit 0 ({O}/twin_project_{{1,2,3}}.r19.out, .err empty).")
row("fc2d-rederive-numbers", "numbers printed in project.html re-derived with an independent script", "course/modules/FC/FC2/project.html:56-488",
    f"Independent re-derivation script (ledgers/FC2/scripts/FC2-d-r17/rederive_r17.py, run with -I) output identical to the r17 output ({O}/rederive_r19.out vs ledgers/FC2/scripts/FC2-d-r17/out/rederive_r17.out). No printed number changed in the delta; the delta changes only docstrings and the count.")
row("fc2d-simulated-label", "SIMULATED label on every lab and grader chain", "course/modules/FC/FC2/project.html (18 occurrences, grep -c); grader/instance.py",
    "grep -c SIMULATED project.html = 18 (same as round 17); docstrings of the three twins still say SIMULATED; instance.py unchanged.")
row("fc2d-process-banned", "no process words in learner text", "course/modules/FC/FC2/project.html; tests/labs/FC2/lab-FC2-project-{1,2,3}.py; grader/test_project.py",
    "grep -i -E 'verifier|fixer|ruling|round [0-9]' project.html = 0; word scan of the new docstring and test comment text found no process word ('rounds' and 'round' are the arithmetic verb, not a process word).")
row("fc2d-notation", "every symbol in the delta is the notation registry's", "course/modules/FC/FC2/project.html; notation/notation.json",
    "The delta adds prose ('signed gap', 'gross amount', 'magnitude') and no new symbol; notation.json unchanged since aa659725 (git diff empty).")
row("fc2d-no-external", "no external link or resource", "course/modules/FC/FC2/project.html",
    "grep -c 'https?://' project.html = 0 (round 19).")
row("fc2d-dag-closure", "check_dag reports no concept outside the unit's prerequisite closure", "tools/check_dag.py --all (FC2 line)", f"check_dag FC2: PASS ({O}/check_dag.out).")
row("fc2d-grader-stdlib", "grader is standard library only; test imports unchanged", "course/modules/FC/FC2/grader/instance.py, reference.py, starter.py; test_project.py",
    "The delta to test_project.py adds only test functions (git diff aa659725 95f3f8cb: no import hunk); reference, instance and starter unchanged. The staged suite runs with -I.")

row("fc2d-r17-delta-hunks", "every hunk of the slice-d delta read (git diff aa659725 95f3f8cb)", "git diff aa659725 95f3f8cb -- course/modules/FC/FC2 tests/labs/FC2 ledgers/FC2/mutants",
    "Hunks read: project.html @@ -56 (rung 1 docstring, old 59), @@ -169 (rung 2 docstring, old 172), @@ -317 (grading count 99 to 105, old 320), @@ -378 (rung 3 docstring, old 381); test_project.py @@ -648 (five one-strike tests, 651-680 new), @@ -853 (comment at 887-888 new and the 6.5-chord test at 895-902 new); tests/labs/FC2/lab-FC2-project-{1,2,3}.py docstring hunks (line 4-5 each); mutants r17_a, r17_c, r17_d, r17_e added (new in the delta, standing set now 111). Changed-line proof: out/line_map_r19.json lists exactly these old lines as changed (project.html 59, 172, 320, 381; test_project.py 856; lab twins 4; L04.html 421 outside slice). No other FC2 slice-d hunk.")

# ---- coverage: every previous id appears exactly once ----
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
missing = [i for i in PREV_ROWS if i not in ids]
extra = [i for i in ids if i not in PREV_ROWS]
print("rows", len(rows), "missing", missing, "extra", extra)
assert not missing, missing
mutants = []
for line in open(f"{S}/out/mutate_graders_FC2_0-49_r19.out", encoding="utf-8"):
    if line.startswith("KILLED "):
        head, _, rest = line[len("KILLED "):].partition(": ")
        desc, _, killed_by = rest.rpartition(" -> ")
        mutants.append({"id": head, "description": desc.strip(), "killed_by": killed_by.strip(), "status": "KILLED"})
assert len(mutants) == 111, len(mutants)
from datetime import datetime, timezone
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
    "unit": "FC2", "slice": "d", "round": 19,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 19 (closing delta verification, rulings 30 and 37; did not build FC2)",
    "pin": "95f3f8cb",
    "base": "aa6597255304919b9c4e5e5ca07763ae3e13d45c (round-17 pin; previous full fragment ~/.fanout/frags/D-FC2-d.round17.json, read as context; the round-18 path named in the task does not exist; its PASS rows were not trusted, its non-PASS rows were re-verified)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD19-FC2-d (detached at 95f3f8cb, .venv symlinked, vendor copied)",
    "scratch": "ledgers/FC2/scripts/FC2-d-r19/ (build_fragment_r19.py, map_lines_r19.py, run_alts_r19.sh, page_twin_r19.py, float_claims_r19.py, page_twin, probe_scan_one_strike/, out/)",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "hull2021options, stoll1969relationship, cox1979option: registry records carry no edition, volume or issue; the page quotes none (carried from round 17; references/references.json unchanged in the delta; verify_refs offline 560 entries, 0 problems)."
    ],
    "freshness_flags": [
        "plans/FC2-open-items.md:56 still says the test count is 75 for seeds 0 to 49 (confirmed by pytest --collect-only at that time). Stale: the suite collects 105 on every seed 0-83 at 95f3f8cb (collect_per_seed_r19.out, collect_50-83_r19.out). File not in slice d and not edited by this verifier."
    ],
    "notes": [
        "Delta scope (aa659725..95f3f8cb, slice d files): course/modules/FC/FC2/project.html hunks at old lines 56-61 (rung 1 docstring), 172-175 (rung 2 docstring), 320-322 (grading count 99 to 105), 381-384 (rung 3 docstring); course/modules/FC/FC2/grader/test_project.py: five one-strike tests at 651-680, the comment at 884-888, the 6.5-chord test at 895-902; tests/labs/FC2/lab-FC2-project-{1,2,3}.py docstrings. Every other changed hunk in the delta is outside slice d (see below) and was not verified here.",
        "Outside slice d, observed only: course/modules/FC/FC2/L04.html line 421 (explanation text cites Proposition 2.3 and Remark 2.4; not verified this round); course/modules/FC/FC2/cards.json (cards for FC2 are another slice); tests/test_lx1_project_lab3.py (LX1 unit, new in the delta). Note for the user: at 95f3f8cb 'pytest tests -k project' fails tests/test_lx1_project_lab3.py::test_a_population_sd_variant_of_the_two_pass_check_raises (AssertionError at line 101, ledgers/FC2/scripts/FC2-d-r19/out/pytest_relevant.out). This is not an FC2 row; the FC2-relevant pytest run passes.",
        "Ruling 37 was followed: no new mutant was written into ledgers/FC2/mutants or equivalent/. The two scan-side probes (scan_df_checked_only_multi_strike, scan_strike_checked_only_multi_strike) and the early-return probe are scratch files under ledgers/FC2/scripts/FC2-d-r19/probe_scan_one_strike/, used only to decide the spec-errors-scope row; they are not mutants. The verifier-rules procedure of at least three new student-error mutants is superseded for this closing round by ruling 37.",
        "Scan one-strike checks: scan calls convexity_violations unconditionally, which re-validates df_ppm, strikes and lengths. Removing scan's own one-strike checks therefore changes no observable behaviour (both probes pass the whole suite and the candidate tests). The early-return probe (scan returns [] for one strike) is killed by test_one_strike_chain_scans_without_convexity. This is why spec-errors-scope is PASS. Candidate tests in candidate_scan_one_strike_r19.py were written, then found unnecessary; they are not added to the grader.",
        "Calibration (rubric): ~/.fanout/blind/FC2-d.json gives A=[2,1,2,2,1] and B=[4,3,3,3,3] against page data-scores A=2,1,2,2,1 and B=4,4,3,3,3. Every criterion is within one level (VERIFIER_RULES calibration rule 2), so PASS. The blind file was produced by a separate scorer; this verifier did not run the stripping script and did not verify the blind file's provenance. This verifier saw the data-scores attributes of the two exemplar article tags while locating them, but not the exemplar prose or annotations; the blind comparison used only the blind file.",
        "The 6.5-chord test comment says 'Plain float arithmetic gives the chord 6.500000000000001'. True for the expression the comment writes, 5/6*7 + 1/6*4 (float_form_check_r19.out). A different float ordering, (5*7+1*4)/6, gives exactly 6.5. The comment's claim is about the written expression and is accepted, with this scope recorded.",
        "The 6.5-chord test is the only new test that exercises a float-vs-exact difference on a non-zero-gross chain; eight alternatives (alt1 to alt8) pass it, so it does not over-constrain. Alternatives: ledgers/FC2/scripts/FC2-d-r14/alts/alt1..alt5, FC2-d-r14/alt6_round6_alternative.py, FC2-d-r15/alts/alt7_integer_scaled.py, alt8_decimal_60.py; runner run_alts_r19.sh.",
        "Mypy: the bare grader directory fails strict mypy with import-not-found for 'scanner' because the reference is staged under that name at grading time; the staged copy passes strict. Recorded as a harness artefact, not a defect.",
        "Could not check: a browser screenshot of the page (not part of the gate list for this slice); the blind scorer's own run (provenance not verifiable here); the L04 and cards.json deltas (other slices)."
    ],
    "summary": ""
}
rows_pass = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = (f"FC2-d round 19 on 95f3f8cb (closing delta over aa659725, rulings 30 and 37): {rows_pass} PASS of {len(rows)} rows, "
                   f"{len(rows) - rows_pass} non-PASS. Base non-PASS rows re-verified: fc2d-mutate-builder (now 111/111 killed), "
                   f"fc2d-spec-errors-scope (one-strike checks now tested; scan-side gap is equivalent), fc2d-r17-plain-float-convexity (r17_d killed by the 6.5-chord test), "
                   f"fc2d-r17-test-comment-856 (comment now true). Gates re-run: check_pages, check_dag, check_projects, run_labs, page_smoke, run_graders (0-49 and 50-83), ruff, mypy (repo and staged grader), pytest FC2, verify_refs: all PASS. Mutants 111/111 killed; eight alternatives 50/50 each.")
out = f"{ROOT}/ledgers/FC2/FC2-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, "verdict", verdict)
