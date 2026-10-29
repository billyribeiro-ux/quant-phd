"""Verifier r8: builds ledgers/M4/M4-d.json from the observed outputs of round 8 (scripts in this directory)."""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB8-M4-d")
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

R8 = ROOT / "ledgers/M4/scripts/M4-d-r8"
PROJ = ROOT / "course/modules/M/M4/project.html"

# href anchors in project.html must resolve to ids (P-14)
html = PROJ.read_text(encoding="utf-8")
hrefs = set(re.findall(r'href="#([^"]+)"', html))
ids = set(re.findall(r'\bid="([^"]+)"', html))
missing_anchors = sorted(h for h in hrefs if h not in ids)

# mutate output parse (mutants and killers)
mut_lines = (R8 / "mutate_M4_seeds0-9_r8.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED) ([^:]+): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = None if killer.strip() == "None" else killer.strip()
    mutants.append({"id": name, "description": desc, "killed_by": killed_by})

CARRY = "Carried from round 7 (byte-identical since the round-7 pin 7aa909e): "
P = "course/modules/M/M4/project.html"
G = "course/modules/M/M4/grader/test_project.py"

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
    row("P-01", "2.6-prose-numbers", f"{P}:57, 136-137", "PASS",
        "Re-verified: hypothesis (8.4e9 cents^2, (nu-2)/nu = 0.6 at nu = 5, ceil(0.99*20000) = 19800) matches the lab-1 expected block "
        "(portfolio variance 8400000000.0; matched factor 0.600000); run_labs --unit M4: 13/13 (fresh)."),
    row("P-02", "2.6-lab-prose", f"{P}:147-192", "PASS",
        CARRY + "project.html:147-192 lab 2 and its expected block; run_labs 13/13 on this pin (fresh)."),
    row("P-03", "2.6-lab-prose", f"{P}:266-314", "PASS",
        CARRY + "project.html:266-314 lab 3 prose; run_labs 13/13 on this pin."),
    row("P-04", "2.6-code-reading", f"{P}:58-135", "PASS",
        CARRY + "project.html:58-135 lab 1 code; twin tests/labs/M4/lab-M4-project-1.py exits 0 under python -I -W error (fresh)."),
    row("P-05", "2.9-numbers-derived", f"{P}:325, 429", "PASS",
        CARRY + "derived values unchanged; recomputed in round 7."),
    row("P-06", "2.6-conventions", f"{P}:209-217", "PASS",
        CARRY + "Conventions subsection unchanged; matched_scale and quantile_99 definitions match grader/reference.py:19-25 and :95-104."),
    row("P-07", "2.9-numbers-derived", f"{P}:211, 214, 482", "PASS",
        CARRY + "lines unchanged; numbers recomputed in round 7."),
    row("P-08", "2.9-numbers-derived", f"{P}:228", "PASS",
        CARRY + "line 228 unchanged; the disclosed survivors m11, m17, n02, v4_m02 named there are SURVIVED in the r8 mutate run (see G-09 to G-12)."),
    row("P-09", "2.6-test-count", f"{P}:206; {G}", "PASS",
        "pytest --collect-only -q on grader/ with reference.py as tail_risk.py, python -I -W error: '132 tests collected'; project.html:206 says 132 checks (fresh)."),
    row("P-10", "2.9-structure", f"{P}:330-343", "PASS",
        CARRY + "rubric block unchanged."),
    row("P-11", "2.6-rubric-and-limits", f"{P}:348-462", "PASS",
        "Changed sentence at project.html:453 (limitations) re-verified: 'relative variance tolerance is 0.30 of the target' matches "
        "grader/test_project.py:41 (TOL_T_VARIANCE = 0.30) and :78 (abs(measured / target - 1.0)). Other lines in 348-462 carried from round 7 (byte-identical)."),
    row("P-12", "2.6-rubric-and-limits", f"{P}:354-461", "PASS",
        "Same as P-11: the only changed line in this range is 453 and it is re-verified; the rest carried from round 7 (byte-identical)."),
    row("P-13", "2.9-links", f"{P}:33, 237-243; course/modules/M/M4/index.html", "PASS",
        CARRY + "lines 33 and 237-243 unchanged; index.html unchanged (not in the delta)."),
    row("P-14", "2.9-links", f"{P} (all href=\"#...\")", "PASS" if not missing_anchors else "FAIL",
        "Every href=\"#x\" in project.html resolves to an id (fresh scan, %d anchors); new anchor #conventions at line 209 is used at lines 37 and 57; "
        "missing: %s." % (len(hrefs), missing_anchors or "none"),
        "Add the missing ids: " + ", ".join(missing_anchors)),
    row("P-15", "2.9-banned-process-words", f"{P}; cards.json; grader/*.py", "PASS",
        "grep -i -E 'round[- ]?[0-9]|verifier|builder|fanout|haiku|TODO|FIXME|checkout|slice' over the three files: zero hits (fresh)."),
    row("P-16", "2.6-prose", f"{P}", "PASS",
        CARRY + "lines unchanged."),
    row("P-17", "2.5-page-smoke", f"{P}", "PASS",
        "tools/page_smoke.py --unit M4 --pages course/modules/M/M4/project.html --skip-labs --skip-sweep: 'page_smoke M4: PASS', exit 0 "
        "(ledgers/M4/scripts/M4-d-r8/page_smoke_project_r8.txt; fresh)."),
    row("P-18", "2.6-conventions-vs-grading", f"{P}:204 vs 209-217", "PASS",
        CARRY + "line 204 unchanged; the not-graded items it names (item 1, item 2, item 4, item 5) still match the suite's comments (test_project.py:31-41)."),
    row("P-19", "2.6-prose", f"{P}:259", "PASS",
        CARRY + "line 259 unchanged."),
    row("P-20", "2.9-claims", f"{P}:248-250", "PASS",
        CARRY + "autosave sentence unchanged; the round-7 PASS rests on the round-7 browser evidence for this byte-identical sentence."),
    row("P-21", "2.6-prose-notation", f"{P}:37, 57", "PASS",
        "New text 'matched to the same covariance (the matched factor is defined under Conventions)' and 'with nu the Student-t degrees of "
        "freedom (defined under Conventions)': Conventions (project.html:209-212) defines the matched factor (nu-2)/nu and the Student-t return with W chi-square(nu); anchor id=\"conventions\" at 209 (fresh)."),
    row("P-22", "2.6-limits", f"{P}:453", "PASS",
        "'relative variance tolerance is 0.30 of the target': grader/test_project.py:41 TOL_T_VARIANCE = 0.30 and :78 relative error (fresh)."),
    row("G-01", "2.6-autograder-reference", G, "PASS",
        "tools/run_graders.py --unit M4 --seeds 0-49: 'PASS (reference 50/50 seeds)'; direct grader run of reference.py as tail_risk.py, seeds 0-49: 50 ok (ledgers/M4/scripts/M4-d-r8/grader_check_r8.sh; fresh)."),
    row("G-02", "2.6-autograder-starter", "course/modules/M/M4/grader/starter.py", "PASS",
        "starter.py as tail_risk.py, python -I -W error pytest: '130 failed, 1 passed, 1 skipped' (round 7 was 129 failed; the added student_t parametrization fails the stub too). A starter that fails is expected (fresh)."),
    row("G-03", "2.6-alternative-implementations", "ledgers/M4/scripts/M4-d-r6/alts/alt1..alt5; ledgers/M4/scripts/M4-d-r7/alt6, alt7", "PASS",
        "Each of the seven alternative correct implementations, run with grader_check_r8.sh over seeds 0-49: '50 ok' for all seven (fresh, after the grader change)."),
    row("G-04", "2.6-autograder-structure", f"{G}:31-42", "PASS",
        CARRY + "lines 31-42 unchanged."),
    row("G-05", "2.6-autograder-structure", f"{G}:229-237", "PASS",
        CARRY + "lines 229-237 unchanged."),
    row("G-06", "2.6-mutation", "ledgers/M4/mutants/r6_01_three_asset_last_factor_column_dropped.py", "PASS",
        "mutate_graders --unit M4 --seeds 0-9 (r8 run): KILLED r6_01 -> test_gaussian_loss_variance_matches_portfolio_covariance."),
    row("G-07", "2.6-mutation", "ledgers/M4/mutants/r6_02_student_t_chi_square_twice_the_degrees.py", "PASS",
        "mutate_graders r8: KILLED r6_02 -> test_student_t_loss_variance_matches_matched_covariance."),
    row("G-08", "2.6-mutation", "ledgers/M4/mutants/r6_03_pivot_tolerance_rejects_small_positive_variance.py", "PASS",
        "mutate_graders r8: KILLED r6_03 -> test_one_position_with_a_tiny_positive_variance (fresh)."),
    row("G-09", "2.6-mutation", "ledgers/M4/mutants/m11_loss_sign_flipped.py", "PASS",
        "SURVIVED on the r8 run. Disclosed: project.html:204 lists the sign of the loss as an item the suite does not grade and :228 says 'The suite does not test the sign of the loss'. Not a new survivor."),
    row("G-10", "2.6-mutation", "ledgers/M4/mutants/m17_student_t_second_seed.py", "PASS",
        "SURVIVED on the r8 run. Disclosed: project.html:228 'The suite does not check the stream order'."),
    row("G-11", "2.6-mutation", "ledgers/M4/mutants/n02_one_chi_square_per_asset.py", "FAIL",
        "SURVIVED on the r8 run and disclosed (project.html:228: 'does not check that the Student-t family uses one chi-square variable per draw'). "
        "But the mutant's first docstring line is the reference's 'Reference solution for the M4 project...' (line 1 of the file), so the mutant-hygiene rule "
        "(first docstring line describes the error) fails, and the mutate tool reports its description as that sentence.",
        "Rewrite the first docstring line of ledgers/M4/mutants/n02_one_chi_square_per_asset.py to describe the error (for example "
        "'Student-t draws use one chi-square variable per asset, not per draw.') and re-run tools/mutate_graders.py --unit M4 --seeds 0-9."),
    row("G-12", "2.6-mutation", "ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py", "PASS",
        "SURVIVED on the r8 run. Disclosed: project.html:228 'The suite therefore does not check the matched factor inside simulate_losses at those values'."),
    row("G-13", "2.6-autograder-tests", f"{G}:89-457", "PASS",
        "The only change in test_project.py since 7aa909e is the parametrized test at 165-171 (student_t added); reference passes 50/50, 132 collected, and existing tests are unchanged (fresh)."),
    row("G-14", "2.6-instances", "course/modules/M/M4/grader/instance.py:1-48", "PASS",
        CARRY + "instance.py unchanged; the instances differ across seeds (round-7 sample of 20 seeds)."),
    row("G-15", "2.6-mutation", "ledgers/M4/mutants/r7_01_student_t_seed_fixed.py; " + G + ":165-171", "PASS",
        "Round-7 FAIL is fixed: r7_01 (Student-t family ignores the seed) is KILLED in the r8 run -> test_different_seed_gives_different_losses[student_t-4] (seed 0)."),
    row("G-16", "2.6-mutation", "ledgers/M4/mutants/r8_03_student_t_matched_scale_on_first_asset_only.py; " + G + ":41, 78", "FAIL",
        "NEW survivor (verifier round 8): the matched factor is applied only to asset 0's return, so the cross-covariance term is scaled by E[scale] (about 0.92 at nu = 5) "
        "instead of 1. Survives all 50 seeds (grader_check_r8.sh) and the seeds 0-9 mutate run. Conventions (project.html:209-211) state R = sqrt((nu-2)/W) L Z for every asset, so the "
        "violated behaviour is stated. The only variance check is the relative 0.30 tolerance (test_project.py:41, :78), which the page itself says cannot separate modest "
        "errors (project.html:453).",
        "Add a test that isolates the cross term: with positions (w1, w2) and (w1, -w2), Var(loss+) - Var(loss-) = 4 w1 w2 Cov(r1, r2); compare the Student-t sample value against the matched "
        "4 w1 w2 Sigma_12 with a tolerance tight enough to reject an 8 percent cross-term bias at the instance's draw count and seeds, check alternatives alt1-alt7 still pass, then re-run "
        "tools/mutate_graders.py --unit M4 and confirm r8_03 is KILLED. This verifier has not confirmed that such a tolerance exists."),
    row("G-17", "2.6-mutation", "ledgers/M4/mutants/r8_01_*.py, r8_02_*.py", "PASS",
        "Two new student-error mutants of this verifier: r8_01 (chi-square drawn once per run) KILLED -> test_student_t_loss_variance_matches_matched_covariance (seed 5); "
        "r8_02 (quantile index one low at multiples of 100) KILLED -> test_quantile_99_convention_on_small_lists (seed 0). Both are also 50/50 fail in grader_check_r8.sh."),
    row("L-01", "2.5-labs", "tests/labs/M4/lab-M4-project-{1,2,3}.py", "PASS",
        "tools/run_labs.py --unit M4: 'run_labs M4: PASS (13/13)'; each project twin exits 0 under python -I -W error (fresh)."),
    row("L-02", "2.5-labs", "tests/labs/M4", "PASS",
        CARRY + "the project lab twins and their expected blocks are unchanged; run_labs 13/13 on this pin."),
    row("L-03", "2.5-labs", "tests/labs/M4/lab-M4-L01-1.py .. lab-M4-L10-1.py", "PASS",
        "Covered by run_labs --unit M4 13/13 on this pin (expected blocks equal the twins' stdout under the page's rule) (fresh)."),
    row("L-04", "2.5-labs-prose", "tests/labs/M4/lab-M4-L10-1.py:60-65; course/modules/M/M4/L10.html:234-236", "PASS",
        "Round-7 FAIL is fixed: the docstring now says the cancellation is about 2e-6 times each term and about six digits are lost, and that the printed values are unaffected. "
        "ledgers/M4/scripts/M4-d-r8/l10_precision_r8.py (80-digit decimal) gives relative error 5.5e-11 at x = 1000 and x^3 P(|V| > x) = 2.205307642577 exact vs 2.205308 printed; "
        "the printed Part-D line 2.205308 is unaffected. The page function equals the twin (ledgers/M4/scripts/M4-d-r8/l10_page_vs_twin_r8.py)."),
    row("C-01", "2.7-cards-count", "course/modules/M/M4/cards.json", "PASS",
        "191 cards; grade counts T 170, C 21 (round 7: T 171, C 20; c191 moved T to C); per lesson L01 17, L02 19, L03 16, L04 19, L05 18, L06 16, L07 15, L08 17, L09 24, L10 30 (fresh)."),
    row("C-02", "2.7-cards-vs-lesson", "course/modules/M/M4/cards.json vs L01-L10.html", "PASS",
        "Fresh check of the 24 cards changed or added in this delta (c007, c037, c038, c040, c041, c044, c045, c046, c063, c088, c092, c129, c130, c134, c135, c136, c137, c140, "
        "c144, c156, c163, c164, c180, c191) against the lesson text (grep of L01/L03/L04/L05/L06/L08/L09/L10); each back is a substatement of the cited lesson item. "
        "Other cards carried from round 7 (byte-identical)."),
    row("C-03", "2.7-cards-numbers", "course/modules/M/M4/cards.json (changed cards)", "PASS",
        "Recomputed: Example 2.5 gamma_3 = (1-2p)/sqrt(pq), gamma_4 = (1-3pq)/(pq); p = 1/10 gives 8/3 and 73/9; p = 1/4 gives 7/3; law on -2,1,3 with 2/5,1/2,1/10 has mean 0 and m3 = 0; "
        "Chebyshev sigma^2/(n eps^2) with n = 2, eps = 1/2, sigma^2 = 1 gives 2; marginal table in c063 gives p(0,0) = 1/2 vs product 1/4; c191 covariance [[S1^2, rho S1 S2], [rho S1 S2, S2^2]] (fresh)."),
    row("C-04", "2.7-cards-lab-numbers", "course/modules/M/M4/cards.json (lab-sourced numbers)", "PASS",
        CARRY + "lab-sourced numbers; the lesson twins' outputs are unchanged and run_labs passes; L10 Part D 2.205308 re-verified at 80 digits."),
    row("C-05", "2.7-cards-numbers", "course/modules/M/M4/cards.json", "PASS",
        CARRY + "unchanged card; sqrt(2968750000) = 54486.2... recomputed in round 7."),
    row("C-06", "2.7-cards-vs-lesson", "course/modules/M/M4/cards.json vs L01-L10.html", "PASS",
        CARRY + "unchanged cards; changed cards checked fresh under C-02."),
    row("C-07", "2.7-cards-duplicates", "course/modules/M/M4/cards.json", "PASS",
        "Python scan on 191 entries (fresh): no duplicate fronts, backs or ids."),
    row("N-01", "2.4-notation", "notation/notation.json; course/modules/M/M4/", "PASS",
        "notation.json registers gamma_3 (skewness, module M4) and gamma_4 (kurtosis, not excess, module M4); the changed cards use these symbols, and the local gamma in c019 is a constant in a formula, which notation.json allows per lesson (fresh)."),
    row("D-01", "2.9-dag", "course/modules/M/M4/", "PASS",
        "tools/check_dag.py --unit M4: 'check_dag M4: PASS' (fresh)."),
    row("T-01", "2.9-gates", "ledgers/M4/scripts/M4-d-r8/", "PASS",
        "check_pages, check_dag, check_projects: PASS; run_graders 50/50; run_labs 13/13; ruff check and ruff format --check on grader/ and tests/labs/M4: pass; mypy --no-incremental: 'Success: no issues found in 255 source files'; pytest test_memo_exemplars.py and test_page_checks.py: pass; page_smoke project: PASS (fresh)."),
]

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
nonpass = [r for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not nonpass else "FAIL"
frag = {
    "unit": "M4",
    "slice": "d",
    "round": 8,
    "verifier": "independent verifier (Haiku), not a builder of M4",
    "pin": "ce7b382",
    "base": "7aa909e (round-7 pin; previous fragment /Users/billyribeiro/.fanout/frags/B-M4-d.round7.json)",
    "checkout": str(ROOT),
    "scratch": "/tmp/M4-d-r8-scratch",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 7aa909e..ce7b382 for slice d: project.html (lede, rung 1, lab-1 hypothesis, grading-mode count 131 to 132, limitations), grader/test_project.py (student_t parametrization), tests/labs/M4/lab-M4-L10-1.py (docstring), cards.json (about 24 cards changed or added). Every hunk was read.",
        "The round-7 FAIL rows G-15 (r7_01 survivor) and L-04 (false docstring) are fixed and re-verified.",
        "New survivor r8_03 (G-16) is the only new surviving grader mutant; it violates the Conventions' Student-t return and is not caught by the 0.30 tolerance. FAIL.",
        "Mutant hygiene: n02's first docstring line does not describe the error (G-11). FAIL.",
        "Survivors m11, m17, n02, v4_m02 are the disclosed set (project.html:204, 228) and are not counted as new.",
        "Not checked: the browser (Chrome) rendering of project.html beyond page_smoke; the L10 lesson page outside its docstring sentence; every line of unchanged cards beyond byte-identity; verify_refs not run (references/ unchanged in this delta; registry not read in this slice).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": len(nonpass),
        "unverifiable": 0,
        "mutants_total": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
        "new_mutants_round8": 3,
        "new_mutants_round8_killed": 2,
    },
}
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("missing anchors:", missing_anchors)
print("validate:", ledger.validate(frag, "M4-d"))
print("verdict:", verdict, frag["summary"])
