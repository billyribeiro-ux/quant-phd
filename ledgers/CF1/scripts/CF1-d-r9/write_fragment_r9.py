"""Build ledgers/CF1/CF1-d.json (round 9) from the round-8 rows (carried where subjects are byte-identical) and round-9 checks."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
PREV = json.loads(pathlib.Path("/tmp/fanout-frags/CF1-d.round8.json").read_text(encoding="utf-8"))
S = "ledgers/CF1/scripts/CF1-d-r9/"

FRESH = {}  # id -> (status, location, check, evidence, fix)
def fresh(rid, check, location, evidence, status="PASS", fix=None):
    FRESH[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        FRESH[rid]["fix"] = fix

CARRY_FILES = {
    "proj-npv-empty-overconstraint": "course/modules/CF/CF1/project.html line 213 and grader/test_project.py lines 109-111",
    "proj-capex-float-overconstraint": "course/modules/CF/CF1/project.html line 188 and grader/test_project.py parameter capex-float",
    "proj-named-errors-untested": "course/modules/CF/CF1/project.html line 213 and grader/test_project.py lines 233-290, 404-432, 541-550",
    "proj-capex-negative-untested": "course/modules/CF/CF1/grader/test_project.py parameter capex-negative",
    "proj-wc-timing-unenforced": "course/modules/CF/CF1/project.html line 202 and grader/test_project.py working-capital tests",
    "proj-exemplar-b-locator": "course/modules/CF/CF1/project.html line 428 (Exemplar B, 2 Cash flows)",
    "proj-rung1-step-line-wording": "course/modules/CF/CF1/project.html lines 44 and 55",
    "proj-browser-storage-claim": "course/modules/CF/CF1/project.html line 238 and course/assets/js/grader.js",
    "proj-must-raise-text-claim": "course/modules/CF/CF1/grader/test_project.py lines 54-60",
    "proj-exemplar-b-crossing-claim": "course/modules/CF/CF1/project.html line 425 (Exemplar B, 1 Recommendation)",
    "proj-tangent-root-claim": "course/modules/CF/CF1/project.html line 207 and grader/test_project.py lines 141-145",
    "proj-tangent-endpoint-reported": "course/modules/CF/CF1/project.html line 207 and grader/test_project.py lines 148-163",
    "proj-spec-formulas-and-window": "course/modules/CF/CF1/project.html lines 199-215 and grader/reference.py",
    "proj-lab2-completion-twin": "tests/labs/CF1/lab-CF1-project-2.py and course/modules/CF/CF1/project.html lines 134-179",
    "proj-lab3-sanity-run": "tests/labs/CF1/lab-CF1-project-3.py and course/modules/CF/CF1/project.html lines 249-375",
    "proj-exemplar-a-quote": "course/modules/CF/CF1/project.html lines 401-419 (Exemplar A)",
    "proj-exemplar-numbers": "course/modules/CF/CF1/project.html lines 400-440 (Exemplar B line 433 and the annotation lines are unchanged)",
    "proj-about-39-percent": "course/modules/CF/CF1/project.html line 374 (Lab 3 interpretation)",
    "proj-registry-reading-list": "course/modules/CF/CF1/project.html lines 456-463 and references/references.json",
    "proj-high-end-test-spec-justified": "course/modules/CF/CF1/grader/test_project.py lines 155-160",
    "proj-lessons-cross-ref": "course/modules/CF/CF1/project.html line 431 and L04 Remark 4.3",
    "proj-irr-close-roots-missed": "course/modules/CF/CF1/project.html line 207 and grader/reference.py irr_roots",
    "proj-irr-grid-convention-unenforced": "course/modules/CF/CF1/project.html lines 192 (IRR grid text, unchanged in the hunk) and 207 and grader/reference.py _GRID_POINTS",
    "proj-irr-window-unenforced": "course/modules/CF/CF1/project.html line 207 and grader/test_project.py lines 164-190",
    "proj-irr-window-end-intervals": "course/modules/CF/CF1/project.html line 206 and grader/test_project.py lines 197-216",
    "proj-tolerance-relative-only": "course/modules/CF/CF1/project.html line 209 and grader/test_project.py line 63",
    "proj-tolerance-rationale": "course/modules/CF/CF1/project.html line 209 and grader/test_project.py lines 12, 333, 345, 360, 369, 394, 501",
    "proj-fisher-tolerance-zero-cases": "course/modules/CF/CF1/project.html line 209 and grader/test_project.py lines 304, 307",
    "proj-ladder-skip-condition": "course/modules/CF/CF1/project.html line 42",
    "proj-window-end-high-unenforced": "course/modules/CF/CF1/project.html line 207 and grader/test_project.py lines 156-161",
    "proj-cards-c071-not-established": "course/modules/CF/CF1/cards.json CF1-c071 and course/modules/CF/CF1/L05.html section 4",
    "cards-misconception-locator": "course/modules/CF/CF1/cards.json and the L02, L05, L06 misconception sections",
    "cards-prose-garbled-c067": "course/modules/CF/CF1/cards.json CF1-c067 and course/modules/CF/CF1/L05.html R2",
    "cards-changed-c014-c037-c047-c057": "course/modules/CF/CF1/cards.json CF1-c014, c037, c047, c057 and L03/L04 (lesson files unchanged)",
    "cards-changed-c016-c044-c051-c052": "course/modules/CF/CF1/cards.json CF1-c044, c051, c052 (cards unchanged; c016 re-verified this round)",
    "proj-lab2-docstring-claim": "tests/labs/CF1/lab-CF1-project-2.py lines 1-10 and course/modules/CF/CF1/project.html lines 134-179",
    "proj-tolerance-claim-note": "course/modules/CF/CF1/project.html line 209 and grader/test_project.py lines 63, 226-227, 298-308, 339-398, 510",
    "proj-memo-rubric-caption": "course/modules/CF/CF1/project.html rubric caption (table id rubric-memo)",
    "proj-unrounded-gap-claim": "course/modules/CF/CF1/project.html line 433 (the Uncertainty paragraph is unchanged; only the Evidence paragraph at line 436 changed) and tests/labs/CF1/lab-CF1-project-3.py",
    "proj-sign-changes-convention": "course/modules/CF/CF1/project.html line 205 and tests/labs/CF1/lab-CF1-project-1.py output step 6",
    "proj-irr-grid-close-pair-example": "course/modules/CF/CF1/project.html line 206",
    "proj-named-errors-tax-share-one": "course/modules/CF/CF1/project.html line 213 and grader/test_project.py lines 417-420",
    "proj-equivalent-mutant-proof": "ledgers/CF1/mutants/ (no equivalent mutant kept); the round-9 equivalent draft is proved in proj-mutants-round9-new",
    "proj-mutants-round4-new": "ledgers/CF1/mutants/m25..m30 (re-run this round)",
    "proj-mutants-round5-new": "ledgers/CF1/mutants/m31..m35 (re-run this round)",
    "proj-mutants-round6-new": "ledgers/CF1/mutants/m37..m40 (re-run this round)",
}
CARRY_OVERRIDES = {  # carried rows whose cited location was corrected this round
    "proj-never-prints-or-mutates-unenforced": "course/modules/CF/CF1/project.html line 190 (Constraints; round 8 cited line 192, which is the Grading mode line)",
}
PREV_BY_ID = {r["id"]: r for r in PREV["rows"]}

def carried(rid, files=None):
    r = dict(PREV_BY_ID[rid])
    assert r["status"] == "PASS", rid
    fl = files or CARRY_FILES.get(rid) or r["location"]
    r["location"] = CARRY_OVERRIDES.get(rid, r["location"]) if rid in CARRY_OVERRIDES else r["location"]
    r["evidence"] = ("Carried from round 8 (" + fl + " byte-identical since the previous pin 2c8162b): "
                     "round-8 basis: " + r["evidence"])
    return r

# ---- fresh round-9 rows ----
fresh("proj-count-cause-wording",
      "2.9 prose / 2.6: the 76-check count and its stated cause",
      "course/modules/CF/CF1/project.html line 192 (Grading mode); grader/test_project.py lines 404-433, 542-548",
      "Round-8 FAIL resolved. Line 192 now says 'no parametrize list's length depends on the seed'. Re-derived: "
      "every parametrize list is a literal list of pytest.param entries whose number of entries is fixed (16 at lines 404-433, "
      "4 at line 104, 2 at lines 233, 286, 312, 542-548). Values read PROJECT, so values depend on the seed but list lengths do not. "
      "Collect-only on the reference for seeds 0-49 gives 76 each (ledgers/CF1/scripts/CF1-d-r9/collect.out, collect_seeds.py).")
fresh("proj-mc-mean-three-se-false-failure",
      "2.6 / ruling (b): the Monte Carlo mean test rejects the spec-following reference on some seeds",
      "course/modules/CF/CF1/grader/test_project.py lines 528-539; course/modules/CF/CF1/project.html line 209 (Tolerances: 'The Monte Carlo mean lies within three standard errors')",
      "The reference solution fails this test on seed 152890303 (page_smoke seed; pytest reproduction: '1 failed, 75 passed', "
      "ledgers/CF1/scripts/CF1-d-r9/seed_check.py output; z = -3.033) and on 6 of seeds 0-1999 "
      "(ledgers/CF1/scripts/CF1-d-r9/mc_z_scan_0_2000.out: seed 664 z = -3.602, seed 104 z = -3.405, seed 1254 z = -3.378). "
      "The reference is the instructor's solution and follows the spec exactly, so a correct learner engine fails with about 0.3 percent probability per seed; "
      "the draws are a fixed seeded sequence, so a 3-SE test on them is a statistical false-failure rate, not a property a correct engine must have. "
      "Ruling (b) applies: a correct solution must not fail.",
      status="FAIL",
      fix="Replace the 3-SE check with an exact identity on the same seeded draws: the NPV is affine in the multiplier m (NPV = a + b*m, since revenue "
          "and the working-capital flows scale with m), so the mean of the draws equals a + b*mean(m) exactly, computed from the same gauss stream (to 1e-6 cents); "
          "this still fails a missing mean-one correction; or state a false-failure rate that is negligible (for example 6 SE) and quote it on the page. "
          "Then update project.html line 209 to match what is checked.")
fresh("proj-page-smoke",
      "2.5 / command: page_smoke --unit CF1 --pages project",
      "course/modules/CF/CF1/project.html in-browser grader (light desktop)",
      "Command output (ledgers/CF1/scripts/CF1-d-r9/page_smoke_project.out): 'in-browser grader: 75 of 76 tests pass on seed 152890303' and "
      "'page_smoke CF1: FAIL (1 pages)', exit 1. Not a timing failure: pytest on the same seed fails the same test "
      "(test_monte_carlo_mean_is_within_three_standard_errors_of_the_deterministic_npv, z = -3.033), see proj-mc-mean-three-se-false-failure.",
      status="FAIL",
      fix="Fix proj-mc-mean-three-se-false-failure; then re-run page_smoke --unit CF1 --pages project.")
fresh("proj-grader-reference-50-seeds", "2.5 / command: run_graders --unit CF1 --seeds 0-49",
      "course/modules/CF/CF1/grader; tools/run_graders.py",
      "Re-run this round: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)' (ledgers/CF1/scripts/CF1-d-r9/graders.out). "
      "Note: seed 152890303, which page_smoke uses, is outside 0-49 and fails (see proj-mc-mean-three-se-false-failure).")
fresh("proj-mutants-killed", "2.6 / command: mutate_graders --unit CF1 --seeds 0-9 (all 53 mutants)",
      "ledgers/CF1/mutants/m01..m53; tools/mutate_graders.py",
      "Re-run this round: 'mutate_graders CF1: PASS (53/53 killed)' (ledgers/CF1/scripts/CF1-d-r9/mutate53b.out; copied to mutate.out). "
      "The 47 round-8 mutants were copied unchanged from /tmp/verify8-CF1-d/ledgers/CF1/mutants.")
fresh("proj-mutants-round7-new", "2.6 / mutants m41..m44 killed", "ledgers/CF1/mutants/m41..m44",
      "Re-run: KILLED m41 (test_irr_finds_a_root_in_the_last_grid_interval), m42 (..._first_grid_interval), m43 (test_fisher_round_trip_is_exact), m44 (test_real_flows_at_the_real_rate...).")
fresh("proj-mutants-round8-new", "2.6 / mutants m45..m47 killed", "ledgers/CF1/mutants/m45..m47",
      "Re-run: KILLED m45 (test_payback_ignores_flows_after_the_cut_off), m46 (test_irr_finds_both_roots_of_a_two_sign_change_flow), m47 (test_fisher_rejects_rates_at_or_below_minus_one[inflation]).")
fresh("proj-mutants-round9-new",
      "2.6 / ruling (g): at least three new student-error mutants, and the equivalent-mutant proof",
      "ledgers/CF1/mutants/m48..m53; ledgers/CF1/scripts/CF1-d-r9/make_mutants_r9.py",
      "Six new student-error mutants written from grader/reference.py (each one edit, asserted to match once): m48 volatility read as variance "
      "(KILLED by test_monte_carlo_draws_follow_the_seeded_gauss_stream), m49 one normal reused for all draws (KILLED same test), m50 irr_roots returns the "
      "discount factor (KILLED test_irr_finds_both_roots_of_a_two_sign_change_flow), m51 irr_roots skips bisection and returns the grid-interval midpoint "
      "(KILLED same test), m52 depreciation over life + 1 (KILLED test_depreciation_shield_is_depreciation_times_tax_rate), m53 discounted payback reads the rate "
      "as a percentage (KILLED test_discounted_payback_uses_discounted_flows). "
      "A first draft of m51 (only the midpoint changed to lo, with bisection kept) SURVIVED and is equivalent: the bisection stops when hi - lo <= 1e-15 * hi, "
      "so lo and the midpoint differ from the root by at most 1e-15 relative, far inside the 1e-7 rate tolerance. That draft was deleted and is not in the mutants list.")
fresh("proj-alternatives-correct",
      "2.6 / ruling (b): alternative correct engines pass the suite on seeds 0-49",
      "ledgers/CF1/scripts/CF1-d-r9/alts/ (10 engines), run_variants.py",
      "Re-run this round: 'seeds failing 0 of 50' for all ten: alt_r7_1..3, alt_r8_1..3 (round-8 files), and new alt_r9_1 (IRR grid of 30001 points, "
      "bisection to 1e-13 relative), alt_r9_2 (discounting by multiplication with (1+r)^-t), alt_r9_3 (Fisher via expm1/log1p), alt_r9_4 (NPV by Horner's rule, "
      "Monte Carlo multiplier as exp(z*v)/exp(v^2/2)). Output: ledgers/CF1/scripts/CF1-d-r9/variants.out.")
fresh("proj-collect-count-50-seeds", "2.9 / the 76 count on every seed",
      "course/modules/CF/CF1/grader/test_project.py; course/modules/CF/CF1/project.html line 192",
      "collect_seeds.py (pytest --collect-only -q on reference.py, -I, seeds 0-49): {'76': (50, [0, 1, 2])} (ledgers/CF1/scripts/CF1-d-r9/collect.out).")
fresh("proj-structure-and-gates", "2.9 / command: check_projects --all, check_pages --unit CF1, check_dag --all",
      "tools/check_projects.py, tools/check_pages.py, tools/check_dag.py",
      "Re-run this round: 'check_projects CF1: PASS' (and AC1, AC2, AC4, AP1 PASS); 'check_pages CF1: PASS'; 'check_dag CF1: PASS' (ledgers/CF1/scripts/CF1-d-r9/ outputs in this session).")
fresh("proj-check-dag", "DAG: check_dag --all", "tools/check_dag.py",
      "Re-run: 'check_dag CF1: PASS'.")
fresh("proj-pytest-lab-helper", "2.5 / command: run_labs --unit CF1", "tests/labs/CF1/*.py; tools/run_labs.py",
      "Re-run: 'run_labs CF1: PASS (9/9)' (the six lesson twins and three project twins).")
fresh("proj-lab1-twin-output", "2.5 / project lab 1 twin output", "tests/labs/CF1/lab-CF1-project-1.py; course/modules/CF/CF1/project.html lines 56-131",
      "run_labs CF1 PASS (9/9) includes lab-CF1-project-1; the expected output in project.html is that twin's output (round-8 check of steps 3-9 carried in proj-exemplar-b-locator).")
fresh("proj-lab3-recomputed-numbers", "2.2 numbers: lab 3 figures on the page",
      "course/modules/CF/CF1/project.html lines 374, 434; tests/labs/CF1/lab-CF1-project-3.py",
      "run_labs CF1 PASS (9/9) re-ran lab-CF1-project-3. The page figures (39.35 percent, 787 of 2,000, 0.73 SE) are carried from round 8: the lab and the cited lines are byte-identical, and the round-8 recomputation stands.")
fresh("proj-ruff-format", "2.9 / ruff on grader and labs",
      "course/modules/CF/CF1/grader; tests/labs/CF1", "Re-run: 'All checks passed!' (ruff check) and '13 files already formatted' (ruff format --check); ledgers/CF1/scripts/CF1-d-r9/ruff.out.")
fresh("proj-mypy-grader-gate", "2.9 / mypy --strict on grader and labs",
      "course/modules/CF/CF1/grader/*.py; tests/labs/CF1", "Re-run: 'Success: no issues found in 13 source files' (mypy --strict --ignore-missing-imports --no-incremental); ledgers/CF1/scripts/CF1-d-r9/mypy.out.")
fresh("proj-verify-refs", "2.1 citations: verify_refs offline and live for CF1",
      "tools/verify_refs.py; references/references.json",
      "Re-run: 'offline integrity: 560 entries, 0 problems'; 'live re-verification of CF1: 2 of 560 entries, 0 problems' (ledgers/CF1/scripts/CF1-d-r9/verify_refs_*.out).")
fresh("proj-test-count-72", "2.9 / test count on the page equals the collected count",
      "course/modules/CF/CF1/project.html line 192; grader/test_project.py",
      "Row id kept from earlier rounds. Page says 76 checks; collect-only gives 76 on seeds 0-49 (proj-collect-count-50-seeds). PASS.")
fresh("proj-hours-table", "2.9 / project hours table", "course/modules/CF/CF1/project.html lines 216-230",
      "Re-derived: 1 + 1 + 4 + 2 + 1 + 1 + 2 = 12 (the Total row says 12); 48 lesson hours from six data-hours=8 (L01-L06); 48 + 12 = 60 = the hub's 60 hours.")
fresh("proj-hours-arithmetic-split", "hub split: hours arithmetic", "course/modules/CF/CF1/index.html lines 25-41; L01-L06 data-hours",
      "data-hours-lessons=48 and data-hours-project=12; each lesson data-hours=8 (L01 to L06); 12/60 = 20.0%, matching the hub's '48 h lessons · 12 h project (20.0% of the 60 module hours)'. PASS.")
fresh("proj-banned-phrases", "2.9 banned phrases in changed passages", "course/modules/CF/CF1/project.html; L01, L02, L05, L06 changed passages; cards.json",
      "Scan of every added line of the round-9 delta (/tmp/cf1-v/d/r9/delta.diff): 'about 0.0532 to 0.0572' appears with its calculation (0.0552 plus or minus 1.96 times 0.0010) on the same line, as the rule allows. No ellipsis, 'roughly', 'historically' or 'typically' added.")
fresh("proj-registry-graham-glasserman", "2.1 citations: Exemplar B evidence and the registry",
      "course/modules/CF/CF1/project.html line 436 (Exemplar B, 5 Evidence); references/references.json entries glasserman2003monte and graham2001theory",
      "Changed line 436 now says the registry records Glasserman (2003) under glasserman2003monte. Registry entry: title 'Monte Carlo Methods in Financial Engineering', year 2003, book, Springer (verified_by crossref); graham2001theory: title 'The theory and practice of corporate finance: evidence from the field', Journal of Financial Economics 60(2-3), pages 187-243. Both match the page. No figure is quoted from either (project.html line 436 read in full). Registry flags stay as recorded.")
fresh("proj-tolerance-six-checks-enumerated", "2.6 / the six 1e-6 checks named on the page",
      "course/modules/CF/CF1/project.html line 209; grader/test_project.py lines 339, 355, 364, 378, 398, 510",
      "The page names: depreciation shield (339), working-capital flows (the year-1 flow at 355 and every year at 378), the one-year project (364), the real-rate NPV (398), and the Monte Carlo draws (510). That is six close() calls with absolute=1e-6 (read at each line). The 349 check uses an explicit 1e-6 bound and is not counted; the page does not list it. Consistent.")
fresh("proj-count-cause-wording-note", "placeholder", "", "", status="PASS")
del FRESH["proj-count-cause-wording-note"]
fresh("proj-stdlib-and-no-instance-import-unenforced", "2.6 / constraint: standard library only, no import of instance.py",
      "course/modules/CF/CF1/project.html line 190 (Constraints); grader/test_project.py lines 554-566",
      "Round-8 row cited line 192; the constraint sentence is at line 190 (line 192 is Grading mode). The test lists every non-stdlib import of capbudget and fails on any, including instance. Re-run in the suite: reference passes on 50 seeds. PASS.")
fresh("proj-never-prints-or-mutates-unenforced", "2.6 / constraint: no printing, no warnings, no mutation of arguments",
      "course/modules/CF/CF1/project.html line 190 (Constraints); grader/test_project.py lines 42, 444-469",
      "Round-8 row cited line 192; the sentence 'never prints or warns' is at line 190. Enforcement: pytestmark filterwarnings('error') (line 42) turns a warning into a failure; test_functions_never_print (461-469) and test_input_project_is_not_changed (444-448) and test_flow_list_arguments_are_not_changed (451-458) enforce the rest. Mutants m10 (print and mutate) KILLED in the re-run. PASS.")
fresh("proj-error-message-unenforced", "2.6 / ruling (a): message wording is not graded",
      "course/modules/CF/CF1/project.html line 190 and line 213; grader/test_project.py lines 54-60",
      "Line 190 says the autograder checks the exception type and not the message; must_raise (54-60) checks only ValueError. PASS.")
fresh("proj-mc-draw-method-unenforced", "2.6 / Monte Carlo draw method (line 209) and the draws test",
      "course/modules/CF/CF1/project.html line 209; grader/test_project.py lines 501-513",
      "test_monte_carlo_draws_follow_the_seeded_gauss_stream checks each draw against gauss(0,1) in order with the exact multiplier (rel 1e-9, abs 1e-6). Mutants m14, m25, m26, m33, m35, m48, m49 are KILLED on seed 0 in the re-run. The 3-SE mean test is a separate check and fails (proj-mc-mean-three-se-false-failure). PASS for the draw-method statement.")
fresh("cards-missing-grade-or-basis", "cards: every card has a grade and cite or basis", "course/modules/CF/CF1/cards.json",
      "Programmatic re-run over all 100 cards: no card lacks grade or (cite or basis); grades only 'T' (74) and 'C' (26).")
fresh("cards-duplicate-scan", "cards: duplicate ids and fronts", "course/modules/CF/CF1/cards.json",
      "Programmatic re-run over all 100 cards: 0 duplicate ids, 0 duplicate fronts; ids run CF1-c001 to CF1-c100 (the ids of L03 and L04 are carried; c088 is an L03/L04 card).")
fresh("cards-grade-semantics", "cards: grade T and C semantics", "course/modules/CF/CF1/cards.json",
      "T cards cite a proposition, a problem or a definition; C cards cite a SIMULATED lab output, a stated convention, or a registry key with no finding. Re-read the 67 cards of L01, L02, L05 and L06 this round (C: c002, c003, c010, c013, c014, c027, c028, c032, c068-c071, c074, c081-c084, c089, c096-c098); the 33 L03/L04 cards are carried (unchanged). PASS for the re-read cards.")
fresh("cards-arithmetic-recomputed", "cards: arithmetic recomputed",
      "course/modules/CF/CF1/cards.json CF1-c009, c011, c016, c017, c029, c032",
      "Exact recomputation: c009 NPV 3452.6152 -> 3,452.62, sum 13452.6152 -> 13,452.615; c011 -83.33; c016 -0.009434 and +0.019417; c017 crossing 1/12 and (1+r)^-2(10-120r); c029 750.00; c032 PV of -690, 10, 0, 680 at t = 1..4 at 8% = -130.4952 -> -130.50. All match the card text.")
fresh("cards-lab-derived-numbers", "cards: lab-derived numbers", "course/modules/CF/CF1/cards.json CF1-c074, c097, c098; tests/labs/CF1/lab-CF1-L05-1.py",
      "lab-CF1-L05-1 re-run: D -132231.40, A 289367.40 cents; A minus B 385535.69; tails min 121251.71 and max 693692.91. Card text matches.")
fresh("cards-numbers-in-lesson", "cards: every card number appears in its lesson or lab output", "course/modules/CF/CF1/cards.json; lab outputs",
      "Cards from labs matched to re-run outputs: c010 and c013 (L01 Lab 1: gap below 1e-6 True, 7,000.00 and -46.94); c027 and c032 (L02 Lab 2: 534.24, -1,465.76, 2,000.00; flows -690, 10, 0, 680); c068-c070, c074, c098 (L05 Lab 1); c081-c083 (L06 Lab 1). L03 and L04 numbers are carried and were not re-checked this round.")
fresh("cards-cite-keys-and-locators", "cards: cite keys in the registry and locators", "cards.json CF1-c071, CF1-c084; references/references.json",
      "CF1-c071 cites graham2001theory and CF1-c084 cites glasserman2003monte; both keys exist (references/references.json). The c084 locator 'Remark 2.4' exists in L06. Registry flag stays (glasserman used_by lists M8 only).")
fresh("cards-changed-c071-c084", "cards: c071 and c084 agree with the current lesson text", "cards.json CF1-c071, CF1-c084; L05 section 4; L06 Remark 2.4",
      "c084 back now says 'The normal claim is not proved, cited or graded here; it is used only as a reading aid ...'. L06 Remark 2.4 (line 106): 'is not proved, cited or graded here. This lesson uses it only as a reading aid'. Agrees. c071 unchanged; L05 section 4 unchanged. PASS.")
fresh("cards-c080-positive-variance-dropped", "cards: c080 with P2", "cards.json CF1-c080; L06 Problem P2 (line 291-299) and P2 solution (line 352 region) and key-result row line 367",
      "New front: 'every pair of receipts sharing the same positive correlation' matches P2's common pairwise covariance rho*sigma^2. Back: 'Each covariance term has the sign of the common correlation, so the variance is larger ...' matches the P2 solution ('for rho > 0 the variance is larger than under independence'). Expectation statement matches the L06 quiz explain (L06q8 explain: 'the expectation does not depend on correlation'). PASS.")
fresh("cards-c065-payback-basis", "cards: c065 with L05 Proposition 2.2 and its conventional definition",
      "cards.json CF1-c065; L05.html line 86 (Proposition 2.2: conventional = C0 < 0 and Ct >= 0 for t >= 1, r >= 0, tau_D >= tau_S)",
      "Card front defines the scope (conventional flows, rate zero or more, both paybacks exist), matching L05 line 86. Back: 'discounting cannot shorten payback: the discounted year is the same or later, because each discounted flow is at most its undiscounted flow'. Each discounted flow t >= 1 is C_t/(1+r)^t <= C_t when C_t >= 0 and r >= 0, so the discounted cumulative flow never exceeds the undiscounted one and reaches zero no earlier. Consistent with Proposition 2.2 and the L05 line 229 sentence. PASS.")
fresh("cards-changed-c071-lesson-agreement", "cards: c065, c071, c084 agree with the lesson text",
      "cards.json CF1-c065, c071, c084, c085; L05.html Prop 2.2 (line 86), section 4, L05q4; L06.html Remark 2.4 (line 106)",
      "Re-read the three changed cards against their lessons: c065 (above), c084 (above), c071 (unchanged, section 4 unchanged). c085 unchanged and consistent with L06 section 5. PASS.")
fresh("cards-c012-npv-falls-scope", "cards: c012 states NPV falls with the rate in general, but Proposition 3.1 is for a conventional stream",
      "course/modules/CF/CF1/cards.json CF1-c012 (back text); L01.html line 111 (Remark 3.2), line 338 (second misconception), line 99 (Proposition 3.1)",
      "The L01 text was changed this round to say 'for a conventional stream the NPV falls as the rate rises' (Remark 3.2, the second misconception at line 338, and the Prop 3.1 statement 'Let the stream be conventional' at line 99). Card CF1-c012 still reads 'NPV falls strictly as the rate rises (Proposition 3.1)' with no scope, and its scope is wider than Prop 3.1. The general claim is false: for flows (0, -1, 2) (not conventional: C_0 = 0 and C_1 < 0) NPV(4) = -0.12 and NPV(5) = -0.111, so NPV rises between 4 and 5 (derivative (1+r)^-3 times (1+r-4)). The card is T and cites Prop 3.1, so the overreach is a graded error.",
      status="FAIL",
      fix="Change CF1-c012 back to: 'False. For a conventional stream, NPV falls strictly as the rate rises (Proposition 3.1), so a positive NPV at one rate can be negative at a higher one. The rate must be justified before the result is read.'")
fresh("index-ladder-rung1-worked-example", "hub ladder: rung 1 'Worked example' wording (changed this round)",
      "course/modules/CF/CF1/index.html line 161 (The project ladder, Worked example); course/modules/CF/CF1/project.html lines 42-43 (Rung 1) and lines 56-131 (Lab 1)",
      "New hub text: 'A year-1 worked after-tax operating cash flow and working-capital line ... Lab 2 prints the later years and the NPV of the same project.' "
      "The rung-1 worked example is Lab 1 on the project page: it works all three years (steps 3, flows at t = 0 to 3, step 6), and prints the NPV at 10 percent, 926.00 dollars (step 7), so the hub's 'year-1' description omits the content and the NPV is printed in rung 1, not only in Lab 2. "
      "Lab 2 (the completion problem, project.html lines 134-179) does print the flows and the NPV on its expected-output line, which is correct.",
      status="FAIL",
      fix="Replace the Worked example text with: 'Lab 1 works a three-year SIMULATED machine project step by step: depreciation, working capital, and each year's revenue, cost, tax and flow, then the NPV at 10 percent (926.00 dollars). Lab 2 completes the cash-flow line and prints the same flows and NPV.'")
fresh("lesson-l01-conventional-rewrites", "lessons: L01 rewritten sentences (meta, why-it-matters, Remark 3.2, Lab 1 hypothesis and interpretation, the second misconception, the Lab 1 example numbers)",
      "course/modules/CF/CF1/L01.html lines 7, 51, 111, 174-175, 338, 371, 407; tests/labs/CF1/lab-CF1-L01-1.py",
      "Re-ran the L01 twin: Part A flows -10000, 3000..3800 (conventional: C0 < 0, C_t > 0 for t >= 1); NPV 7000.00 at 0.00, 4635.81 at 0.05, 2744.72 at 0.10, 1211.49 at 0.15, -46.94 at 0.20; 'strictly decreasing on this grid: True' (all printed values in the page match). Part B 100 of 200 positive (page says 100 of 200). The 'conventional' definition at line 95 (C_t >= 0 for t >= 1, one positive; C_0 unused) supports Prop 3.1 and the scope added in Remark 3.2 and in the second misconception (line 338). The -200, 120, 120 example at line 371: NPV 40.00 at 0 and -16.67 at 0.20, matches. PASS.")
fresh("lesson-l02-rewrites", "lessons: L02 rewritten sentences (why-it-matters, Lab 2 interpretation, accrual sentence, references)",
      "course/modules/CF/CF1/L02.html lines 67, 76, 85, 94; tests/labs/CF1/lab-CF1-L02-1.py",
      "Re-ran the L02 twin: 'SIMULATED machine', depreciation 3000.00, sunk study 2000.00, shield 750.00, identity and shield checks True, working-capital sum 0.00, NPV 534.24, -1465.76, difference 2000.00 (all as printed on the page). Definitions: EBITDA and EBIT at line 87; net working capital Definition 3.1 at line 122; Corollary 2.3 at line 105 (the depreciation tax shield); Proposition 3.2 at line 127. The accrual sentence matches AC1 L01 accrual-accounting definition (line 82) and concepts.html line 101 ('defined here' to AC1). Concept links: balance-sheet and depreciation-and-amortization also point to AC1 (concepts.html lines 103, 106). PASS.")
fresh("lesson-l05-rewrites", "lessons: L05 rewritten sentences (Lab 1 interpretation and explain of quiz item 1)",
      "course/modules/CF/CF1/L05.html line 107 (Lab 1 interpretation), line 117 (quiz item 1 explain); tests/labs/CF1/lab-CF1-L05-1.py",
      "Re-ran the L05 twin: A simple 2.750 and discounted 3.469; B simple 2.750 and discounted none; D 2.000 and none; tails: 1 distinct simple payback (2.750), 1 distinct discounted payback (3.469), NPV range 121251.71 to 693692.91, 1000 distinct NPVs. B flows (-1e6, 3e5, 4e5, 4e5, 0, 0, 0): cumulative discounted at year 3 is -96168.29 and stays negative through year 6, so 'never turns non-negative in any year (years 0 to 6)' is correct. A and B agree in years 0-3 (flows identical). Explain: discounted payback can fall after year 3, so it is not guaranteed to match; consistent with the lab's A and B divergence after year 3. PASS.")
fresh("lesson-l06-rewrites", "lessons: L06 rewritten sentences (quantile band, misconception, E2 solution)",
      "course/modules/CF/CF1/L06.html line 129 (section 3), line 138 (misconception), line 147 (E2 solution); tests/labs/CF1/lab-CF1-L06-1.py",
      "Re-ran the L06 twin: quantiles 14896.62, 79457.94, 143406.13 cents. Unrounded (ledgers/CF1/scripts/CF1-d-r9 and /tmp/cf1-v/d/r9/run/L06_unrounded.py, same code): 14896.623057, 79457.938852, 143406.126569; width 128509.503511 -> 128509.50 (unrounded) and 143406.13 - 14896.62 = 128509.51 (printed). Both statements on the page are right. E2: 0.0552 +/- 1.96 x 0.0010 = 0.05324 to 0.05716, shown as 0.0532 to 0.0572. SE sqrt(0.0552*0.9448/50000) = 0.00102 rounds to 0.0010. Remark 2.4 (line 106) says the normal reading is a reading aid and is not tested. PASS.")
fresh("index-card-and-hub-wording", "hub: L01 card body and hub wording (lines 138, 135)",
      "course/modules/CF/CF1/index.html lines 135-138",
      "L01 card body now says 'the fall of NPV with the rate for conventional flows', consistent with L01 line 95 and Prop 3.1. Lesson count line 'Six lessons of eight study hours each' and the L01-L06 data-hours=8 agree. PASS.")
fresh("proj-exemplar-b-evidence-line", "2.2 / Exemplar B evidence line (changed this round)",
      "course/modules/CF/CF1/project.html line 436", "Same as proj-registry-graham-glasserman: the registry records glasserman2003monte; no figure quoted. PASS.")
fresh("lab-run-summary", "placeholder", "", "", status="PASS")
del FRESH["lab-run-summary"]

# ---- compose rows ----
ids_fresh = set(FRESH)
rows = []
for r in PREV["rows"]:
    rid = r["id"]
    if rid in FRESH:
        rows.append(FRESH[rid]); continue
    if rid == "cards-count-vs-plan":
        rows.append({"id": rid, "check": "cards: per-lesson card count against the plan",
                     "location": "plans/CF1-build-plan.md line 240; course/modules/CF/CF1/cards.json",
                     "status": "FAIL",
                     "evidence": "Re-counted this round: 100 cards: L01 18, L02 16, L03 15, L04 20, L05 16, L06 15 (python over cards.json). plans/CF1-build-plan.md line 240 says 'the planner expects four to six per lesson (one per definition, key result and misconception)'. The count is unchanged since round 8.",
                     "fix": "Cut each lesson's cards to four to six (one per definition, key result and misconception) or record an architect ruling in plans/CF1-build-plan.md changing the expected count."})
        continue
    if rid in ("proj-hours-table",):
        rows.append(FRESH.get(rid, carried(rid))); continue
    if rid.startswith("proj-") or rid.startswith("cards-"):
        rows.append(carried(rid)); continue
    rows.append(carried(rid))

# add rows not present in round 8
for rid, row in FRESH.items():
    if rid not in PREV_BY_ID:
        rows.append(row)
# dedupe ids keep first occurrence
seen = set(); out = []
for r in rows:
    if r["id"] in seen: continue
    seen.add(r["id"]); out.append(r)
rows = out

# mutants from the full run
MUT = []
desc_src = ROOT / "ledgers/CF1/mutants"
import ast
for line in (ROOT / S / "mutate53b.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (.*)$", line)
    if not m: continue
    status, fname, desc, killed = m.groups()
    if status != "KILLED": raise SystemExit("survivor " + fname)
    MUT.append({"file": "ledgers/CF1/mutants/" + fname, "description": desc, "killed_by": killed})
assert len(MUT) == 53, len(MUT)

statuses = [r["status"] for r in rows]
verdict = "FAIL"
frag = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 9,
    "verifier": "Claude Haiku 5.5 (independent verifier, CF1-d round 9; did not build CF1; no shared context with builders or earlier verifiers)",
    "pin": "96dd532 (detached, /tmp/verify9-CF1-d); delta since the round-8 pin 2c8162b",
    "base": "2c8162b (round-8 pin; previous fragment /tmp/fanout-frags/CF1-d.round8.json). Delta in slice (git diff --stat 2c8162b 96dd532 -- course/modules/CF/CF1): L01.html (meta, why-it-matters, Remark 3.2, Lab 1 hypothesis and interpretation, misconception 1), L02.html (why-it-matters, Lab 2 interpretation, accrual sentence, references), L05.html (Lab 1 interpretation, quiz item 1 explain), L06.html (section 3 band, misconception, E2 solution), cards.json (CF1-c065, c080, c084), index.html (L01 card body, ladder rung 1 Worked example), project.html (line 192 Grading mode, line 436 Exemplar B evidence). grader/ and tests/labs/CF1 are byte-identical to the round-8 pin (no hunk in the delta).",
    "checkout": "/tmp/verify9-CF1-d",
    "scratch": "/tmp/cf1-v/d/r9",
    "verified_at": "2026-10-28",
    "verdict": verdict,
    "rows": rows,
    "mutants": MUT,
    "registry_flags": [
        "glasserman2003monte: used_by lists M8 only; CF1 cites it (project.html Exemplar B section 5, L06 Remark 2.4, cards CF1-c084). Unchanged since round 7; add CF1 with tools/add_reference.py or confirm the architect's ruling.",
        "damodaran2012investment: used_by lists CF4 only; CF1 lists it in the project reading list (project.html reading section). Unchanged since round 7.",
    ],
    "freshness_flags": [],
    "notes": (
        "Commands run this round on 96dd532: run_graders --unit CF1 --seeds 0-49 (PASS 50/50, graders.out); mutate_graders --unit CF1 --seeds 0-9 (53/53 killed after the m51 correction; mutate53b.out); "
        "page_smoke --unit CF1 --pages project (FAIL: seed 152890303, page_smoke_project.out); seed_check.py on seed 152890303 (1 failed, 75 passed); mc_z_scan.py seeds 0-1999 (6 seeds with |z|>3 on the reference, mc_z_scan_0_2000.out); "
        "run_variants.py over 10 alternative engines x 50 seeds (0 failing each, variants.out); collect_seeds.py seeds 0-49 (76 each); run_labs --unit CF1 (9/9); check_projects --all, check_pages --unit CF1, check_dag --all (PASS); "
        "ruff check and format --check on grader and tests/labs/CF1 (PASS); mypy --strict on grader and labs (PASS); verify_refs --offline (560, 0 problems) and --unit CF1 (2 of 560, 0 problems); "
        "lesson twins L01, L02, L05, L06 run with python -I -W error (exit 0); L06 unrounded quantiles from the lab code (L06_unrounded.py); exact card arithmetic. "
        "Not run: the full repository gate; pytest over tests/ beyond run_labs; browser tests beyond page_smoke; the L03/L04 twins (unchanged); project lab 3 numbers beyond run_labs. "
        "Not judged: hours design targets (architect ruling); lesson prose not changed this round and not cited by a card or the page; index.html lines other than 135-161. "
        "The grader is unchanged, so its rows are carried by byte identity, but every command that tests it was re-run. "
        "Carried rows whose page location moved (round-8 cited project.html line 192 for constraint sentences that are at line 190) are corrected to line 190 and marked."
    ),
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] != "PASS")
frag["verdict"] = "PASS" if n_fail == 0 and all(m["killed_by"] for m in MUT) else "FAIL"
frag["summary"] = (
    f"CF1-d round 9: FAIL. Rows {len(rows)}: PASS {n_pass}, non-PASS {n_fail}. Mutants {len(MUT)}/{len(MUT)} killed. "
    "Non-PASS: proj-mc-mean-three-se-false-failure (the reference fails the 3-SE Monte Carlo mean test on seed 152890303 and on 6 of seeds 0-1999), "
    "proj-page-smoke (its consequence), cards-c012-npv-falls-scope (card overgeneralises Proposition 3.1 after the lesson was scoped to conventional streams), "
    "index-ladder-rung1-worked-example (hub describes rung 1 as a year-1 line, but Lab 1 works all years and prints the NPV), cards-count-vs-plan (100 cards, 15 to 20 per lesson, against the plan's four to six). "
    "Resolved this round: proj-count-cause-wording (the new cause sentence is right: no parametrize list length depends on the seed; collect gives 76 on 50 seeds)."
)
out = ROOT / "ledgers/CF1/CF1-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", n_pass, "nonpass", n_fail, "mutants", len(MUT), "verdict", frag["verdict"])
