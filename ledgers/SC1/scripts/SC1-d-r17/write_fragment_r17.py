"""Build ledgers/SC1/SC1-d.json (round 17) from the round-16 fragment: re-verified rows get round-17 evidence,
byte-identical subjects are carried with the prefix, and the non-PASS rows carry a fix. Usage: <checkout root>."""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-d.round16.json").read_text(encoding="utf-8"))
OUT = "ledgers/SC1/scripts/SC1-d-r17/out/"

GATE = ("Round 17 (verifier): re-run on pin 700bf33f: check_pages, check_dag, check_projects SC1 PASS; run_labs SC1 11/11 "
        "and project 3/3 PASS; run_graders 50/50 and 200/200 PASS; page_smoke project PASS (in-browser grader: All 136 tests "
        "pass on seed 847353195); mutate_graders 90/90 killed; mypy --no-incremental 385 files PASS; ruff check and "
        "ruff format --check PASS; verify_refs --offline 560 entries, 0 problems (" + OUT + "*_r17.txt).")
ALT = ("Round 17 (verifier): the 47 alternatives of the verified folders re-run on seeds 0-49 with run_one_r17.py: 47/47 pass "
       "(" + OUT + "alternatives_carried_r17.txt). The five new alternatives alt_r17_1..5 pass 50/50 (" + OUT +
       "alternatives_new_r17.txt; alt_r17_3 failed first because of a verifier-side SE error, fixed before the recorded run).")
MUT = ("Round 17 (verifier): tools/mutate_graders.py --unit SC1 --seeds 0-9 with the four new mutants r17_01..r17_04: 90/90 "
       "killed (" + OUT + "mutate_graders_unit_r17b.txt); existing mutant files unchanged since the previous pin.")
LAB = ("Round 17 (verifier): run_labs --page project 3/3 (" + OUT + "run_labs_project_r17.txt). Twins run with python -I -W error: "
       "exit 0, empty stderr, output equal to each expected block up to the final newline (" + OUT + "twin_vs_page_r17.txt). "
       "Page code equals the twin for Labs 1 and 3 (diff is the final newline only); Lab 2 differs only at the two ___ blanks.")
REF = ("Round 17 (verifier): reference.py read in full; the round-17 delta is its docstring (lines 2-5, wording only). "
       "run_graders 0-49 50/50 and 0-199 200/200 PASS; the docstring claim that a same-order implementation reproduces Lab 3's "
       "printed digits was checked with two round-17 alternatives on seed 0, all 5 rows equal at 6 dp (" + OUT +
       "docstring_digits_r17.txt).")
REG = ("Round 17 (verifier): references/references.json record shreve2004stochastic re-read: type book, year 2004, status "
       "verified, used_by SC1; the round-17 regeneration changed generated_at and the Black & Scholes used_by entry only; "
       "verify_refs --offline 560 entries, 0 problems (" + OUT + "verify_refs_offline_r17.txt).")
HUNK = ("Round 17 (verifier): project.html:162 and :235 re-read (the only lines changed since 56cc575a: links to P1/P2 of the "
        "statements section). Every number and claim in them re-derived (" + OUT + "indep_numbers_r17.txt) and supported by "
        "Lab 1 output and grader/test_project.py:401-416 and :455-462.")
OUTSIDE = ("Round 17 (verifier): the cross-reference is read again in its source this round: L01.html Definition 1.1; "
           "L05.html Assumptions A3 and A4(b),(c),(g),(h), Sections 1 and 3; L06.html Proposition 1.3 and Corollary 1.4; "
           "L08.html Proposition 1.2 (first-passage identity) and Corollary 1.3; index.html id=placement and data-hours-project=28. "
           "L01, L03, index.html and cards.json changed since the pin outside this slice; the cited items are unchanged in substance.")
ALTS_RE = re.compile(r"alternativ|alt_|alt[0-9]|alt-|-alt|alt\b|ag-overconstraint|ag-alternatives", re.I)
MUT_RE = re.compile(r"mutant|mutate", re.I)
GATE_RE = re.compile(r"gate|run-graders|page-smoke|tools-gates|collect|ruff|mypy|verify|ag-count|ag-instances|ag-starter|r7-starter|starter-fails|sample-|reference-sweep|reference-200|instances|r7-reference|r11-recompute|r11-mypy|r11-collect|r12-collect|r14-collect|r14-starter|r14-sample", re.I)
LAB_RE = re.compile(r"\blab|twin|Lab [0-9]|\bLabs\b")
REF_RE = re.compile(r"reference\.py|ag-reference", re.I)
REG_RE = re.compile(r"registry|references\.json|shreve|reading", re.I)
HUNK_RE = re.compile(r"project\.html:(162|235)\b|lines? (162|235)\b|(?<![0-9.])(162|235)(?![0-9])")
OUT_RE = re.compile(r"L01|Lesson 1\b|L03|Lesson 3\b|index\.html|cards")

CARRY_FILES = ("project.html except lines 162 and 235; grader/test_project.py, grader/instance.py, grader/starter.py and "
               "tests/labs/SC1/* byte-identical since the previous pin 56cc575a")

def classify(row):
    key = row["id"] + " " + row["location"] + " " + row["check"]
    if row["status"] != "PASS":
        return "fail"
    if REF_RE.search(key):
        return REF
    if REG_RE.search(key):
        return REG
    if HUNK_RE.search(key) and not re.search(r"alternativ", key, re.I):
        return HUNK
    if MUT_RE.search(key):
        return MUT
    if ALTS_RE.search(key):
        return ALT
    if LAB_RE.search(key):
        return LAB
    if GATE_RE.search(key):
        return GATE
    if OUT_RE.search(key):
        return OUTSIDE
    return "carry"

def strip_prefix(ev):
    return re.sub(r"^Round 16 \(verifier\): ", "", ev)

rows = []
fail_ids = []
OVERRIDE_FAIL = {"SC1-d-r7-alt4-ruling10": ("2.6-mutation (architect ruling)", "plans/SC1-build-plan.md section 5.7(4); FINAL-ARCHITECT-RULINGS 10", "Round 17 (verifier): the ruling cited by this row (FINAL-ARCHITECT-RULINGS 10) requires five alternatives of different styles that pass seeds 0-49; it says nothing about draw order. The plan item 5.7(4) asks for a Box-Muller alternative on a different draw order, which the page forbids (project.html:233; test_project.py:419-423 and 641-652), so no recorded ruling covers it. Carried PASS was wrong; see SC1-d-r17-plan-5-7-item4-draw-order.", "Architect records a ruling replacing plan 5.7(4) with a same-order alternative or removing the draw-order tests (see SC1-d-r17-plan-5-7-item4-draw-order)."),
}
for r in prev["rows"]:
    if r["id"] in OVERRIDE_FAIL:
        chk, loc, ev, fx = OVERRIDE_FAIL[r["id"]]
        rows.append({"id": r["id"], "check": chk, "location": loc, "status": "FAIL", "evidence": ev, "fix": fx, "verdict": "CONFIRMED"})
        fail_ids.append(r["id"])
        continue
    cat = classify(r)
    if cat == "fail":
        if r["id"] == "SC1-d-r15-plan-5-5-within-5se":
            rows.append({
                "id": r["id"], "check": "2.6-spec (plan 5.5 conformance)",
                "location": "plans/SC1-build-plan.md:431-432 (section 5.5, Tests bullet 'discrete_max_exceedance') vs "
                            "course/modules/SC/SC1/grader/test_project.py:401-416 and 455-462",
                "status": "FAIL",
                "evidence": "Round 17 (verifier): the plan requires the estimate to 'lie within 5 se of reflection_tail(a, H) on "
                            "the instance'. The suite instead checks the one-step estimate against tail/2 within 5 target standard "
                            "errors plus 1/N (test_project.py:401-416, and the same for seed 2nd instance at 410-416) and the grid "
                            "estimate one-sided, estimate <= tail + band, at n_steps 4 and at the instance's n_steps (455-462). The "
                            "grid's own continuum target is not reflection_tail(a, H) (page line 236: the bias is never negative), so "
                            "the plan's literal wording is not the grid's law. No ruling for this deviation exists in "
                            "plans/FINAL-ARCHITECT-RULINGS.md (rulings 1-20 contain no SC1 entry) or plans/SC1-open-items.md "
                            "(checked again this round). Plan unchanged since 56cc575a.",
                "fix": "Architect records a ruling (plans/SC1-open-items.md) that the one-step target is tail/2 and the grid check is "
                       "a one-sided bound by the continuous tail; or amend plan 5.5 to that wording. Then this row can pass without "
                       "a code change.",
                "verdict": "CONFIRMED",
            })
            fail_ids.append(r["id"])
        continue
    if cat == "carry":
        ev = "Carried from round 16 (" + CARRY_FILES + "): " + strip_prefix(r["evidence"])
        rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})
    else:
        rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS", "evidence": cat})

NEW = [
    {"id": "SC1-d-r17-plan-5-7-item4-draw-order", "check": "2.6-spec (plan 5.7 conformance)",
     "location": "plans/SC1-build-plan.md:468-478 (section 5.7 item 4, Box-Muller on a different draw order) vs project.html:233 "
                 "and grader/test_project.py:419-423 and 641-652",
     "status": "FAIL",
     "evidence": "Round 17 (verifier): no verified alternative implements plan 5.7(4). The Box-Muller files of rounds 1-7 "
                 "(ledgers/SC1/scripts/SC1-d-r1..r7/alternatives/alt4_*) are not in the verified set. The page (project.html:233) "
                 "states that an implementation drawing the same values in a different order fails the tests, and the suite enforces "
                 "it (test_one_step_draws_are_the_seeded_gaussians; test_discrete_estimate_matches_an_explicit_count_on_the_stated_draws). "
                 "A 5.7(4) alternative therefore cannot pass the suite that the page describes. Items 5.7(1), (2), (3), (5) are "
                 "satisfied by verified alternatives (see SC1-d-r17-plan-5-7-items-1-2-3-5).",
     "fix": "Architect records a ruling that plan 5.7(4) is replaced by a same-order alternative (for example alt_r17_1 or alt_r17_5, "
            "which use random.Random(seed).gauss in the page's order) or that the Box-Muller alternative may use a different draw "
            "order only if the page's draw-order statement and its two tests are removed. The verifier cannot choose between these.",
     "verdict": "CONFIRMED"},
    {"id": "SC1-d-r17-gates", "check": "gate", "location": "repository and course/modules/SC/SC1 (targeted gate for the slice)",
     "status": "PASS", "evidence": GATE + " Not run: the full repository pytest suite and the live verify_refs run (network)."},
    {"id": "SC1-d-r17-collect", "check": "2.6-autograder (test count)", "location": "course/modules/SC/SC1/grader/test_project.py; project.html:7, 226, 297",
     "status": "PASS", "evidence": "Round 17 (verifier): collect-only in a scratch copy with the reference as bm_checks.py: '136 tests collected' (" + OUT + "collect_count_scratch_r17.txt). A collect in the repository root fails only because bm_checks.py is absent there; that is the expected learner-solution import, not a defect."},
    {"id": "SC1-d-r17-relevant-pytest", "check": "2.5/2.6 tooling", "location": "tests/test_labs.py, tests/test_page_smoke.py; tests/labs/SC1",
     "status": "PASS", "evidence": "Round 17 (verifier): pytest -q tests/test_labs.py tests/test_page_smoke.py: EXIT=0 (" + OUT + "pytest_relevant_r17.txt). tests/labs holds no pytest files (pytest exit 5 recorded in " + OUT + "pytest_labs_r17.txt)."},
    {"id": "SC1-d-r17-lab-outputs", "check": "2.5-labs", "location": "project.html Labs 1-3 (lines 56-210, 166-209, 305-429) vs tests/labs/SC1/lab-SC1-project-{1,2,3}.py",
     "status": "PASS", "evidence": LAB + " Expected blocks of Labs 1-3 (project.html:155-161, 207-209, 419-429) compared with the twin output: equal."},
    {"id": "SC1-d-r17-numbers-recompute", "check": "2.2-numbers / 2.4-mathematics",
     "location": "project.html lines 57, 162, 306, 430, 493, 505, 576, 588, 601, 613-616 and the Lab 1/3 expected blocks",
     "status": "PASS", "evidence": "Round 17 (verifier): independent re-derivation (ledgers/SC1/scripts/SC1-d-r17/indep_numbers_r17.py, output in out/indep_numbers_r17.txt): tail 0.08649666 (prints 0.086497); one-step estimate 0.05954825 (0.059548), sample SE 0.01073457, target 0.04324833, target SE 0.00921764, band 0.04814159, |difference| 0.01629992 (0.016300), 1.5185 sample SE, 1.7683 target SE; grid estimates and SEs for n=1,4,16,64,256 and tail-minus-estimate values (0.026948, 0.037215, 0.020788, -0.001799, 0.004361) match; 64-step excess 0.001799 = 0.1398 SE; nested counts 35, 29, 27, 22 vs fine 40; walk n=12, a=3: 1588 and 794 (=4096 walks); Simpson difference 9.1316e-15. Every prose number on the page matches."},
    {"id": "SC1-d-r17-within-band-claims", "check": "2.2-numbers / 2.6-spec", "location": "project.html:57, 162, 306 (Lab 3 expectation), 430; grader/test_project.py:455-462",
     "status": "PASS", "evidence": "Round 17 (verifier): Lab 3 expectation 'the estimate lies within five standard errors of that tail' for n=4,16,64,256 holds with |p - tail|/SE = 3.79, 1.85, 0.14, 0.35 (ind. script). The Lab 1 band inequality and the 5-SE rule use the target SE as the docstring states."},
    {"id": "SC1-d-r17-seed32-comment", "check": "2.6-autograder (comment accuracy)", "location": "course/modules/SC/SC1/grader/test_project.py:470-478",
     "status": "PASS", "evidence": "Round 17 (verifier): the comment's claim (seed 32, grids 16, 32, 64 give estimate 0.0 at the instance's own level) re-derived: make_instance(32) H=0.584, a=2.444, N=639; hits 0 at each of 16, 32, 64 (out/indep_numbers_r17.txt, seed-32 block)."},
    {"id": "SC1-d-r17-word-counts", "check": "2.9-structure (word counts)", "location": "project.html:463 (exemplar A body 668 words, exemplar B 422 words); :443 (400-900)",
     "status": "PASS", "evidence": "Round 17 (verifier): five memo blocks per exemplar, headings removed, tags removed without inserting spaces, whitespace split (the brief's 'run of characters between spaces'): A = 668, B = 422, both as printed. If each tag is instead counted as a space the counts are 670 and 424; the page's convention is the textContent one and is stated by the brief. Brief item 1 (Summary <= 80 words): exemplar A Summary = 80 words, B = 53 (" + OUT + "word_counts_r17.txt)."},
    {"id": "SC1-d-r17-blind-exemplars", "check": "2.6-rubric calibration (ruling 15)", "location": "project.html exemplars A (line 465) and B (line 547); ledgers/SC1/scripts/SC1-d-r17/out/blind_extract_r17.txt",
     "status": "PASS", "evidence": "Round 17 (verifier): scored from the blind extract (memo prose and rubric descriptors only; annotations, verdicts and data-score attributes removed by blind_extract_r16.py run on this pin). Exemplar A: C1 4, C2 4, C3 4, C4 3 (no continuum statement, only almost surely), C5 4 = 4,4,4,3,4. Exemplar B: C1 2 (P3 unlisted), C2 2 (symmetry step, no gap), C3 2 (0.0865 no rounding statement), C4 2 ('hold for every grid'), C5 2 (grids 1 and 64 omitted; direction from one seed) = 2,2,2,2,2. Both equal the official data-scores. Caveat: the page's verdict lines were visible during the full read earlier in this round, so independence is partial."},
    {"id": "SC1-d-r17-new-alternatives", "check": "2.6-autograder (five alternatives)", "location": "ledgers/SC1/scripts/SC1-d-r17/alternatives/alt_r17_1..5",
     "status": "PASS", "evidence": ALT},
    {"id": "SC1-d-r17-carried-alternatives", "check": "2.6-autograder (carried alternatives)", "location": "ledgers/SC1/scripts/SC1-d-r8..r16 verified folders (47 files)",
     "status": "PASS", "evidence": ALT},
    {"id": "SC1-d-r17-mutants-new", "check": "2.6-mutation", "location": "ledgers/SC1/mutants/r17_01..r17_04",
     "status": "PASS", "evidence": "Round 17 (verifier): four new student-error mutants written from reference.py (ledgers/SC1/scripts/SC1-d-r17/make_mutants_r17.py): r17_01 erfc argument 2 sqrt(t) (killed by test_reflection_tail_is_the_erfc_closed_form), r17_02 only a == 0 guarded (killed by test_reflection_tail_rejects_negative_level), r17_03 erfc doubled (killed by the closed-form test), r17_04 srw terminal threshold (n+a)//2 (killed by test_srw_counts_match_enumeration_for_n_up_to_12[1]). The plan's ten mutants m01-m10 are present and killed."},
    {"id": "SC1-d-r17-mutate-all", "check": "2.6-mutation", "location": "ledgers/SC1/mutants/ (90 top-level files)",
     "status": "PASS", "evidence": MUT},
    {"id": "SC1-d-r17-draw-order-contract", "check": "2.6-spec / 2.9-prose", "location": "project.html:233; grader/reference.py:2-5; grader/test_project.py:419-423, 626-652",
     "status": "PASS", "evidence": "Round 17 (verifier): the stated draw order (path by path, step by step, random.Random(seed).gauss(0, sqrt(H/n))) is in reference.py _grid_paths and in test_project.py _explicit_paths; the two explicit-count tests enforce it, as the page says. Consistent."},
    {"id": "SC1-d-r17-plan-5-7-items-1-2-3-5", "check": "2.6-spec (plan 5.7 conformance)", "location": "plans/SC1-build-plan.md:468-478 items 1, 2, 3, 5",
     "status": "PASS", "evidence": "Round 17 (verifier): item 1 (statistics.NormalDist tail): alt_r17_2 and verified alt_r8_a / alt_r12_1 pass 50/50. Item 2 (Simpson only, 1e-8 tolerance; the suite's 1e-12 closed-form test also passes): alt_r17_4 and alt_r8_b / alt_r12_2 pass 50/50. Item 3 (DP over position and running maximum): alt_r17_2 and alt_r8_c pass 50/50. Item 5 (cumulative sums, index subsampling): alt_r17_5 and alt_r15_5 pass 50/50."},
    {"id": "SC1-d-r17-plan-5-5-sweep", "check": "2.6-spec (plan 5.5 bullets)", "location": "plans/SC1-build-plan.md:389-441 vs grader/test_project.py",
     "status": "PASS", "evidence": "Round 17 (verifier): every 5.5 bullet except the within-5-SE item is covered: reflection_tail erfc (186-188), Simpson 1e-8 (191-194), strict decrease and increase (197-213), ValueError a=0, t=0 with 1e-9 accepted (222-245); srw identity and enumeration for n<=12 (277-299), ValueError n=0, a=0 with n=1, a=1 accepted (341-373); estimate standard error divisor N-1 to 1e-12 (388-392), ValueError n_steps=0 and n_paths=1 (489-510); nested coarse <= fine (517-521), ValueError on non-divisor (556-562); edge cases (n_steps=1, n_paths=2, tiny level, one-step horizon: 401-451, 493-510); instances: determinism and 50 valid seeds with >=45 distinct levels (159-178; this round 49 distinct levels and 50 distinct horizons). Frozen signatures match starter.py (SC1-d-spec-signatures)."},
    {"id": "SC1-d-r17-crossrefs", "check": "2.9-prose / 2.4-attribution", "location": "project.html:37, 42-46, 210, 222-224, 231-243, 247, 250, 531-537, 659 vs L01-L08",
     "status": "PASS", "evidence": OUTSIDE + " Internal lesson cross-references only; no bibliographic data is typed here."},
    {"id": "SC1-d-r17-continuity-attribution", "check": "2.9-prose (attribution)", "location": "project.html:243 (A0 with continuous paths as in Theorem 2.5 and Remark 2.6 of Lesson 2)",
     "status": "PASS", "evidence": "Round 17 (verifier): course/modules/SC/SC1/L02.html Theorem 2.5 states 'a Brownian motion on [0, 1] with continuous paths' and Remark 2.6 concludes 'every path of W is continuous'; the attribution is read and matches."},
    {"id": "SC1-d-r17-notation", "check": "2.9-notation", "location": "project.html (symbols H, T, Phi, erfc, Prob, se, indic, Normal, tau_a, M_t, rho, K, N); notation/notation.json",
     "status": "PASS", "evidence": "Round 17 (verifier): notation.json registers T (number of return observations, S1), \\Phi (standard normal CDF), \\Prob, \\se, \\indic, \\Normal, \\R, \\N. The page uses T only to say that it is not the horizon (project.html:231), uses \\Phi as the standard normal CDF (lines 231, 256, 534), and uses \\Prob, \\se, \\indic, \\Normal as registered. H, a, N, n, t, tau, rho, K, M_t are not registered and carry one meaning each on the page."},
    {"id": "SC1-d-r17-process-words", "check": "2.9-prose (learner text)", "location": "project.html (whole page)",
     "status": "PASS", "evidence": "Round 17 (verifier): grep for round, verifier, builder, fixer, architect, ruling, batch in project.html: no hits in learner prose (only 'exemplar' and 'rubric', which are the page's own terms)."},
    {"id": "SC1-d-r17-ui-claims", "check": "2.9-prose (claims about the UI)", "location": "project.html:220, 226, 289, 464 (footer), 532-534 (completion), course/assets/js/grader.js:33-61, labs.js:133-141, rubric.js:149",
     "status": "PASS", "evidence": "Round 17 (verifier): grader.js:53 shows 'Your instance seed is ... (derived from your workspace ID)' (matches project.html:220); grader.js:59-61 saves the draft 400 ms after input (matches 'saved shortly after you stop typing'); labs.js:133-141 grades completion labs on output (matches 'graded instantly'); rubric.js:149 hides [data-reveal] and annotations until the official scoring is revealed (matches line 463). The seed and the reveal were read in code, not clicked in a browser."},
    {"id": "SC1-d-r17-registry-shreve", "check": "2.1-citations", "location": "references/references.json (shreve2004stochastic); project.html reading list 649",
     "status": "PASS", "evidence": REG},
    {"id": "SC1-d-r17-docstring-digits", "check": "2.6-autograder (docstring claim)", "location": "course/modules/SC/SC1/grader/reference.py:2-5",
     "status": "PASS", "evidence": REF},
    {"id": "SC1-d-r17-instances", "check": "2.6-autograder (instances)", "location": "course/modules/SC/SC1/grader/instance.py; project.html:266",
     "status": "PASS", "evidence": "Round 17 (verifier): seeds 0-49: 0 invalid instances, 49 distinct levels, 50 distinct horizons, 47 distinct grid sizes, 48 distinct path counts, 50 distinct one-step estimates (" + OUT + "instances_r17.txt). Seed 0: H 2.083, a 2.474, N 487, n_steps 66 (matches page line 266)."},
    {"id": "SC1-d-r17-learner-claims-lab2", "check": "2.5-labs (completion)", "location": "project.html:167, 210 (Lab 2 hypothesis and interpretation)",
     "status": "PASS", "evidence": "Round 17 (verifier): Lab 2 twin output 29 / 22 / 7 / True (" + OUT + "twin_vs_page_r17.txt); 29 = 22 + 7 as the identity says; enumeration over 2^6 walks in the twin. The page's claim that the engine tests check every n up to 12 is test_project.py:277-299 (range(1, 13))."},
    {"id": "SC1-d-r17-delta-hunks", "check": "2.9-prose / 2.6", "location": "project.html:162 and :235 (only hunks since 56cc575a)",
     "status": "PASS", "evidence": HUNK},
]
rows += NEW

MUTANTS = []
for line in Path(root, OUT, "mutate_graders_unit_r17b.txt").read_text(encoding="utf-8").splitlines():
    if not line.startswith("KILLED "):
        continue
    body, _, killed_by = line.rpartition(" -> ")
    name, _, desc = body[len("KILLED "):].partition(": ")
    MUTANTS.append({"id": name, "description": desc.strip(), "killed_by": killed_by.strip()})
assert len(MUTANTS) == 90, len(MUTANTS)
verdict = "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS"
frag = {
    "unit": "SC1", "slice": "d", "round": 17,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 17 (did not build SC1-d; read the whole project.html, grader and labs; re-ran the gates; blind exemplar scoring from the blind extract; five new alternatives and four new mutants; re-ran the 47 carried alternatives)",
    "pin": "700bf33f",
    "base": "56cc575a (round-16 pin); delta read: project.html hunks 162 and 235, reference.py docstring (lines 2-5), references/references.json (generated_at; Black & Scholes used_by), L01/L03/index.html/cards.json outside the slice",
    "checkout": str(root), "scratch": "/tmp/sc1d17/", "scripts_dir": "ledgers/SC1/scripts/SC1-d-r17/",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": MUTANTS,
    "registry_flags": [],
    "freshness_flags": ["references/references.json regenerated at 2026-11-09T03:40:24 (generated_at only for SC1; SC1 record shreve2004stochastic byte-identical in content)"],
    "notes": ("Round 17 on 700bf33f (base 56cc575a). Whole project.html read (1-666), grader/reference.py, starter.py, instance.py and "
              "test_project.py read in full, the three lab twins compared with the page. Gates re-run (out/). Mutants: 90 files, 90/90 killed on seeds 0-9. "
              "Alternatives: 5 new (alt_r17_1..5) all 50/50 after a verifier-side SE fix; 47 carried alternatives 47/47 on seeds 0-49. "
              "Blind exemplar scores A 4,4,4,3,4 and B 2,2,2,2,2 from the blind extract, equal to the official scores (partial independence, see row). "
              "Not checked: full repository pytest suite; live verify_refs; reference seeds 200-499; in-browser UI clicks (self-assessment form, storage round trip, seed display); Pyodide per-test timing (only the suite total 1.7 s); L01-L08 and index.html as pages (other slices; cited items only); cards.json (no cards in this slice); hours beyond arithmetic (design targets)."),
    "summary": ("SC1-d round 17 on 700bf33f: verdict FAIL. Three FAIL rows, all plan-conformance: plan 5.5 'within 5 se of reflection_tail' (unrecorded deviation, row SC1-d-r15-plan-5-5-within-5se); plan 5.7(4) Box-Muller on a different draw order, which the page's draw-order contract makes unpassable (row SC1-d-r17-plan-5-7-item4-draw-order, and SC1-d-r7-alt4-ruling10 whose carried PASS cited a ruling that does not cover it). Gates, labs, numbers, mutants (90/90), 52 alternatives and prose claims pass."),
}
Path(root, "ledgers/SC1/SC1-d.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
from collections import Counter
print("rows", len(rows), Counter(r["status"] for r in rows), "fail ids", fail_ids + [r["id"] for r in NEW if r["status"] == "FAIL"])
