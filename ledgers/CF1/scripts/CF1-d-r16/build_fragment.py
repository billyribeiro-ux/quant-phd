"""Build the round-16 CF1 slice-d fragment from the round-15 fragment, the round-16 re-runs and the delta rows."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/CF1-d.round15.json").read_text(encoding="utf-8"))
out_dir = ROOT / "ledgers/CF1/scripts/CF1-d-r16/out"
FILES = (
    "course/modules/CF/CF1/project.html, course/modules/CF/CF1/grader/*, tests/labs/CF1/*, "
    "course/modules/CF/CF1/index.html, course/modules/CF/CF1/L01.html to L04.html, "
    "references/references.json, plans/CF1-build-plan.md and the pre-existing ledgers/CF1/mutants files"
)
CARDS = FILES + "; cards.json entries cited here other than CF1-c068 and CF1-c099"
LESSON = FILES + "; L05.html and L06.html cited lines (the round-16 edits are L05 lines 93-96 and 101 and L06 lines 63 and 66, none cited here)"

RERUN = {
    "cards-missing-grade-or-basis": "Re-run round 16 (python -I scan of cards.json): 103 entries, every entry has a grade in {T,A,B,C,D,X} and a cite or basis; no entry lacks either. Grades 74 T, 29 C. Lesson counts L01 18, L02 17, L03 16, L04 20, L05 17, L06 15.",
    "cards-duplicate-scan": "Re-run round 16 (python -I): 103 unique ids (CF1-c001 to CF1-c103 in sequence), 103 unique fronts, no duplicate back text. The changed cards CF1-c068 and CF1-c099 do not duplicate any other card.",
    "cards-numbers-in-lesson": "Re-run round 16. CF1-c068 number 2.750 years appears in the lab-CF1-L05-1 output (2.750 for Project A simple_payback) and in L05 line 101. CF1-c099 states no number. Other changed cards of round 15 unchanged (see carried rows).",
    "cards-grade-semantics": "Re-run round 16: CF1-c068 grade C, basis 'Lab 1 (SIMULATED flows)', matches the SIMULATED lab output (grade C names the lab rule). CF1-c099 grade T, basis 'Definition 1.2', matches a definition stated in L06 line 63. All other grade and basis pairs are carried (unchanged entries).",
    "r15-cards-numbers-and-grades": "Re-run round 16 with python -I: 103 entries, 74 T and 29 C, unique ids and fronts (see cards-missing-grade-or-basis).",
    "r13-l06-unrounded-difference-basis": "Re-verified round 16: L06.html line 211 still states the unrounded quantiles 14896.623057 and 143406.126569 and the unrounded difference 128509.5035 with the 0.0065-cent gap; the lab prints quantiles at two decimals (lab-CF1-L06-1 output lines 'quantile_10_npv_cents 14896.62' and 'quantile_90_npv_cents 143406.13'). Line 66, changed in round 16, does not touch this basis.",
    "proj-verify-refs": "Re-run round 16: tools/verify_refs.py --offline printed 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit CF1 (live, network) printed 'live re-verification of CF1: 2 of 560 entries, 0 problems'. references/references.json is unchanged since the round-15 pin.",
    "proj-page-smoke": "Re-run round 16: tools/page_smoke.py --unit CF1 --pages project.html printed 'page_smoke CF1: PASS'.",
    "proj-check-dag": "Re-run round 16: tools/check_dag.py --all printed 'check_dag CF1: PASS' (and AC1, AC2, AC4, AP1).",
    "proj-structure-and-gates": "Re-run round 16: tools/check_projects.py --all printed 'check_projects CF1: PASS'; tools/check_pages.py --unit CF1 printed 'check_pages CF1: PASS'.",
    "proj-pytest-lab-helper": "Re-run round 16: tools/run_labs.py --unit CF1 printed 'run_labs CF1: PASS (9/9)'.",
    "proj-grader-reference-50-seeds": "Re-run round 16: tools/run_graders.py --all --seeds 0-49 printed 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)' (command output observed in this round; the run was not written to a file).",
    "proj-ruff-format": "Re-run round 16: .venv/bin/ruff check and ruff format --check on course/modules/CF/CF1/grader and tests/labs/CF1: 'All checks passed!' and '13 files already formatted'.",
    "proj-mypy-grader-gate": "Re-run round 16: .venv/bin/mypy --no-incremental on course/modules/CF/CF1/grader and tests/labs/CF1: 'Success: no issues found in 13 source files'.",
    "proj-collect-count-50-seeds": "Re-run round 16: the collect-only count on the reference and starter for seeds 0, 7 and 49 is 138 in every case (ledgers/CF1/scripts/CF1-d-r16/collect.py).",
    "r15-page-count-138": "Re-run round 16: collect-only count 138 for seeds 0, 7 and 49; project.html line 192 states 138 (unchanged).",
    "proj-mutants-killed": "Re-run round 16: tools/mutate_graders.py --unit CF1 printed 'mutate_graders CF1: PASS (139/139 killed)' over all 139 flat files in ledgers/CF1/mutants/ (136 previous plus the three new r16 mutants). Output in ledgers/CF1/scripts/CF1-d-r16/out/mutate_r16_full.out.",
    "r13-mutants-full-run": "Re-run round 16: 139/139 killed (ledgers/CF1/scripts/CF1-d-r16/out/mutate_r16_full.out); every KILLED line names the killing test.",
    "proj-equivalent-mutant-proof": "Re-verified round 16: all 139 flat files in ledgers/CF1/mutants/ are KILLED. None is an equivalent mutant on the list; no equivalent-mutant proof is needed for the three round-16 mutants because each is killed.",
    "proj-alternatives-correct": "Re-run round 16: all 47 alternative engines in ledgers/CF1/scripts/*/alts/ and */e/alts/ (rounds 9 to 16) PASS 50/50 seeds (ledgers/CF1/scripts/CF1-d-r16/out/alts_all_prior.out).",
    "r15-alternatives-rerun-all-prior": "Re-run round 16: the 47 alternative engines (rounds 9 to 16) all PASS 50/50 seeds (ledgers/CF1/scripts/CF1-d-r16/out/alts_all_prior.out; 0 failures).",
    "r13-run-graders-50": "Re-run round 16: tools/run_graders.py --all --seeds 0-49 printed 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)'.",
    "r13-twins-under-python-I-W-error": "Re-run round 16: tests/labs/CF1/lab-CF1-project-1.py, -project-2.py, -project-3.py, L05-1 and L06-1 each exit 0 under python -I -W error.",
    "proj-lab1-twin-output": "Re-run round 16: lab-CF1-project-1.py under -I -W error exit 0; its printed lines match the expected block of project.html lines 118-130 (e.g. 'step 7, NPV at 0.10: 926.00 dollars', 'step 8 ... 1865.14').",
    "proj-lab2-completion-twin": "Re-run round 16: lab-CF1-project-2.py under -I -W error exit 0; the page expected block (project.html lines 174-175) is the output of the completed code.",
    "proj-lab3-sanity-run": "Re-run round 16: lab-CF1-project-3.py under -I -W error exit 0; output lines match project.html lines 360-372 (two roots [0.1, 0.2], IRR 0.153177, payback 2.370000 and 2.753500, mean 885.85, sd 2445.52, se 54.68, 787 of 2000 negative).",
    "proj-hours-arithmetic-split": "Re-verified round 16: index.html lines 29-41 show 48 h lessons and 12 h project, 20.0% of the 60 module hours; the six L01 to L06 pages each declare data-hours=\"8\" (6 x 8 = 48); 48 + 12 = 60; split 80.0% and 20.0%. project.html line 33 data-hours-project=\"12\" and the hours table total 12 (1+1+4+2+1+1+2).",
    "proj-hours-table": "Re-verified round 16: project.html hours table rows 1, 1, 4, 2, 1, 1, 2 sum to 12, matching data-hours-project=\"12\" (line 33) and the hub split.",
    "proj-exemplar-numbers": "Re-verified round 16 with own code (independent recompute of the rung-1 project MC draws, seed 42, volatility 0.2, 2000 draws): mean 885.85, sd 2445.52, se 54.68, 787 negative, min -4808.83, max 13800.44; 2445.52/885.85 = 2.76 (2.7607); (926.00-885.85) = 40.15; 40.15/54.68 = 0.73 (0.7343); 787/2000 = 39.35 percent; NPV 926.00, discounted payback 2.7535 (2.75 per the printed 2.7535), simple payback 2.37 all recomputed from reference flows.",
    "proj-about-39-percent": "Re-verified round 16: 787/2000 = 0.3935, i.e. 39.35 percent, matching project.html line 373.",
    "proj-lab3-recomputed-numbers": "Re-verified round 16: own code recomputed the Lab 3 values (see proj-exemplar-numbers) and lab-CF1-project-3.py prints the same figures.",
    "r15-lab3-two-root-and-mc-numbers": "Re-verified round 16: irr_roots([-100, 230, -132]) = [0.1, 0.2] (reference); the MC figures above reproduce lab-CF1-project-3.py.",
    "proj-spec-count-118-hub": "Re-verified round 16: collect count 138 (seeds 0, 7, 49) and project.html line 192 states 138.",
}

CARRY_NEW = {
    "cards-count-vs-plan": ("FAIL", "Re-verified round 16 (unchanged finding): cards.json has 103 entries; per lesson L01 18, L02 17, L03 16, L04 20, L05 17, L06 15 (python -I count). plans/CF1-build-plan.md line 240 still says 'the planner expects four to six per lesson', and the file is byte-identical since the previous pin. Every lesson is over the planned range. BUILDER_RULES section 7 asks for one card per definition, theorem, key formula, key result and misconception and sets no count, so the disagreement is between the plan sentence and the cards, which needs an architect ruling: amend the plan sentence to the BUILDER_RULES rule, or trim the cards. Fix: owning builder or architect; no card change is required by BUILDER_RULES."),
    "cards-changed-r12-c027-c042-c068-c101-c103": ("PASS", "Round 16 re-verified CF1-c068 (edited in round 16: front 'In Lab 1, what simple payback does Project A show?', back '2.750 years, for SIMULATED flows. The simple rule uses no discount rate, so the figure does not depend on the 10 per cent rate (Lab 1; Section 1).'): L05 Definition 1.1 (line 58) defines CUM_t as the undiscounted cumulative flow and tau_S without a rate (Section 1, so 'Section 1' is correct); lab-CF1-L05-1 prints 'project A simple_payback 2.750' from payback(flows) with no rate argument (tests/labs/CF1/lab-CF1-L05-1.py lines 30 and 68); grade C with basis Lab 1 matches SIMULATED. CF1-c027, c042, c101, c102, c103 carried from round 15 (byte-identical entries; cited lesson lines unchanged)."),
    "cards-misconception-locator": ("PASS", "Re-verified round 16 for the card that changed in this delta: CF1-c068 is the only changed card cited here in the body text, and its locator is L05 Section 1 and Lab 1 (verified above). Remaining cards carried from round 15 (entries byte-identical)."),
    "lesson-l05-rewrites": ("PASS", "Re-verified round 16: L05.html line 96 (Remark 2.3) now reads 'as Proposition 3.1 (Section 3) shows'; Proposition 3.1 is stated in Section 3 at line 209 (section 3 begins line 206), so the reference is correct. Line 101 (Lab 1 hypothesis) reads 'Proposition 3.1 (Section 3) gives a lower NPV for B', same locator. Lab 1 output: B simple_payback 2.750 and NPV -96168.29, consistent with the text. Line 107 and 117 cited here are byte-identical since the previous pin; carried for those lines."),
    "lesson-l06-rewrites": ("PASS", "Re-verified round 16: L06 lines 129, 138 and 147 cited here are byte-identical since the previous pin (the round-16 L06 edits are at lines 63 and 66). Line 66 was re-read in round 16: Definition 1.2 (line 63) gives the sample mean, quantiles, share and the standard error of the mean; Lab 1 prints mean (mean_npv_cents), se (se_cents), quantiles and share (share_npv_below_zero), so 'Lab 1 reports each of them' holds; the share's standard error is given by the binomial formula sqrt(p(1-p)/n) at L06 line 211 (Section 3), so 'Section 3 gives its binomial formula' holds; Lab 1 prints sd_npv_cents_sample at 50000 draws only (lab line 72), and se_cents for each n uses the sample stdev of the first n draws (lab lines 65 to 66)."),
    "r13-l06-unrounded-difference-basis": (None, None),
}
NEW_ROWS = [
    ("r16-delta-coverage", "git diff --stat c093bf5 c5daab2 for course/modules/CF/CF1, tests/labs/CF1, ledgers/CF1/mutants, tools, references", "course/modules/CF/CF1/L05.html; L06.html; cards.json; ledgers/CF1/mutants/r15e files; ledgers/CF1/mutants/r16_* (new in this round)", "PASS", "git diff --stat c093bf5 c5daab2 -- course/modules/CF/CF1 tests/labs/CF1 ledgers/CF1/mutants references tools: 6 files changed (L05.html 4 lines, L06.html 2 lines, cards.json 6 lines, three new r15e mutant files). project.html, grader/*, tests/labs/CF1/*, index.html, plans/CF1-build-plan.md and references/references.json are byte-identical to the round-15 pin. Every hunk in the slice was read: L05 lines 93-96 and 101, L06 lines 63 and 66, cards.json CF1-c068 and CF1-c099. The three r16 mutants are authored in this round."),
    ("r16-cards-c068-simple-payback-rewrite", "cards.json CF1-c068 (front and back rewritten)", "course/modules/CF/CF1/cards.json CF1-c068; course/modules/CF/CF1/L05.html Definition 1.1 (line 58), Section 1; tests/labs/CF1/lab-CF1-L05-1.py lines 30 and 69", "PASS", "Definition 1.1 (L05 line 58): CUM_t is the cumulative undiscounted flow and tau_S uses no rate. The lab's simple payback is payback(flows) with no rate parameter (lab line 30, printed at line 68). The output 'project A simple_payback 2.750' (run in round 16 under python -I -W error, exit 0) matches the back text. The phrase 'does not depend on the 10 per cent rate' is true of the lab formula and is not overreached."),
    ("r16-cards-c099-standard-error-definition", "cards.json CF1-c099 (back rewritten)", "course/modules/CF/CF1/cards.json CF1-c099; course/modules/CF/CF1/L06.html line 63 (Definition 1.2)", "PASS", "Definition 1.2 (L06 line 63) says the sample standard deviation is the square root of the sum of squared deviations from the sample mean divided by n-1, and the standard error is the sample standard deviation divided by sqrt(n). The back text 'divides the sum of squared deviations from the sample mean by n-1, divided by the square root of n' is the same statement. Grade T, basis Definition 1.2, is consistent with a definition."),
    ("r16-l06-line66-and-section3-share-se", "course/modules/CF/CF1/L06.html lines 63, 66 and 211 (round-16 rewrite of the paragraph after Definition 1.2)", "course/modules/CF/CF1/L06.html lines 63, 66, 211; tests/labs/CF1/lab-CF1-L06-1.py lines 65-72 and 189; lab-CF1-L06-1 output", "PASS", "Line 66: 'Lab 1 prints the sample standard deviation at 50000 draws only' (lab prints sd_npv_cents_sample once, at n=50000, line 72); 'each standard error of the mean that it reports is computed from the sample standard deviation of the draws at that size' (lab lines 65-66 use statistics.stdev(sample) of the first n draws). 'The standard error of the share ... is not defined in Definition 1.2; Section 3 gives its binomial formula' is right: line 211 gives sqrt(p(1-p)/n) at the estimated p, and lab line 189 computes se_negative = sqrt(negative*(1-negative)/N_MAX). Recomputed: sqrt(0.0552*0.9448/50000) = 0.00102, printed 0.0010."),
    ("r16-l05-remark-2-3-and-lab1-hypothesis", "course/modules/CF/CF1/L05.html lines 96 and 101", "course/modules/CF/CF1/L05.html lines 96, 101, 209; lab-CF1-L05-1 output", "PASS", "Both references to Proposition 3.1 are followed by '(Section 3)'. Proposition 3.1 is at L05 line 209 inside Section 3 (line 206). Claim 'B's flows after year 3 are smaller than A's' checked: A years 4-6 are 300000, 200000, 100000 cents (PROJECT_A tuple, L05 line 126 and lab line 126: t = 4, 5, 6); B years 4-6 are 0 (PROJECT_B, lab line 127), and the lab prints NPV B -96168.29 < A 289367.40."),
    ("r16-mutants-new-three", "ledgers/CF1/mutants/r16_01_irr_grid_evenly_spaced_in_rate.py; r16_02_monte_carlo_one_normal_per_revenue_year.py; r16_03_irr_roots_rounded_to_six_decimals.py", "ledgers/CF1/scripts/CF1-d-r16/make_mutants.py; tools/mutate_graders.py --unit CF1", "PASS", "Three student-error mutants written from the reference solution (grader/reference.py): (r16_01) IRR search grid spaced evenly in the rate instead of log x, KILLED by test_irr_finds_both_roots_of_a_two_sign_change_flow; (r16_02) one standard normal drawn per revenue year instead of one per draw, KILLED by test_monte_carlo_draws_follow_the_seeded_gauss_stream; (r16_03) IRR roots rounded to six decimals, KILLED by test_irr_can_return_a_negative_root (the 1e-7 precision is not the test that caught it; the mutant is still killed). The first build of these mutants failed to import (a second docstring before the future import); it was corrected and the re-run is the one recorded (out/mutate_r16_full.out)."),
    ("r16-mutants-full-run", "ledgers/CF1/mutants/*.py (139 files)", "tools/mutate_graders.py --unit CF1; ledgers/CF1/scripts/CF1-d-r16/out/mutate_r16_full.out", "PASS", "mutate_graders CF1: PASS (139/139 killed); exit 0. The 136 earlier flat mutants and the 3 new round-16 mutants are all KILLED with a named failing test."),
    ("r16-alternatives-three-new", "ledgers/CF1/scripts/CF1-d-r16/alts/alt_r16_a, alt_r16_b, alt_r16_c", "ledgers/CF1/scripts/CF1-d-r16/make_alts.py; run_alts.py", "PASS", "Three genuinely different correct engines run 50/50 seeds with PASS: (a) after-tax flow by the algebra EBITDA(1 - tax) + depreciation * tax, Monte Carlo as affine a0 + (a1 - a0) * m, Fisher by expm1(log1p) (PASS 50/50); (b) IRR grid of 8001 points instead of 4001 over the same window (PASS 50/50); (c) payback recomputing the cumulative sum from the start at each year (PASS 50/50). No over-constraint found."),
    ("r16-alternatives-rerun-all-prior", "ledgers/CF1/scripts/*/alts/*.py and */e/alts/*.py (47 files, rounds 9 to 16)", "ledgers/CF1/scripts/CF1-d-r16/out/alts_all_prior.out", "PASS", "All 47 alternative engines PASS 50/50 seeds (47 lines 'PASS 50/50 seeds', 0 failures), including the three round-16 alternatives."),
    ("r16-collect-count-138", "course/modules/CF/CF1/grader/test_project.py; project.html line 192", "ledgers/CF1/scripts/CF1-d-r16/collect.py output", "PASS", "pytest --collect-only on the reference and starter for seeds 0, 7 and 49: 138 tests each. project.html line 192 states 138; equals the count."),
    ("r16-run-gates", "tools/check_projects.py; check_pages.py; check_dag.py; run_labs.py; run_graders.py; mutate_graders.py; page_smoke.py; verify_refs.py", "commands listed in notes", "PASS", "check_projects CF1 PASS; check_pages CF1 PASS; check_dag CF1 PASS; run_labs CF1 PASS (9/9); run_graders CF1 PASS (50/50 seeds); mutate_graders CF1 PASS (139/139); page_smoke CF1 PASS (project.html); verify_refs --offline 560 entries 0 problems; verify_refs --unit CF1 live 2 of 560 entries 0 problems."),
    ("r16-project-lab-numbers-recomputed", "course/modules/CF/CF1/project.html lines 360-372 and 373-374, 433-434; grader/reference.py", "own script (python -I) recomputing the rung-1 flows, NPV, paybacks, IRR root, Fisher value, MC draws", "PASS", "Recomputed with own code: flows -9000, 3150, 4000, 5000 (dollars); NPV 926.00; simple payback 2.37; discounted 2.7535; IRR root 0.153177; Fisher 0.0815; MC seed 42, volatility 0.2, 2000 draws: mean 885.85, sd 2445.52, se 54.68, 787 negative, min -4808.83, max 13800.44. Exemplar arithmetic: 2445.52/885.85 = 2.76; 926.00-885.85 = 40.15; 40.15/54.68 = 0.73; 787/2000 = 39.35 percent. All match the page."),
    ("r16-banned-process-words-scan", "course/modules/CF/CF1/cards.json; L05.html; L06.html; project.html", "grep -i -E 'roughly half|about 6%|historically|ellipsis|builder|verifier|round N|unit report|REQUESTS|built'", "PASS", "No banned phrase or process word in the changed sentences or cards. The only matches are code tuples in L05 lines 126-128, not prose."),
    ("r16-live-registry-refs", "references/references.json; tools/verify_refs.py", "tools/verify_refs.py --unit CF1 (live) and --offline", "PASS", "Live: 2 of 560 entries re-verified, 0 problems (keys graham2001theory and glasserman2003monte, cited by CF1-c071 and CF1-c084). Offline integrity 560 entries, 0 problems. Registry flags below are unchanged."),
]

CARRY_EXTRA_NOTE = "Carried from round 15 (" + FILES + " byte-identical since the previous pin c093bf5): "

rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in CARRY_NEW:
        status, ev = CARRY_NEW[rid]
        if status is None:
            ev = None
        if status is not None:
            rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
            continue
    if rid in RERUN:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RERUN[rid]})
        continue
    prefix = CARDS if ("cards" in rid or "card" in rid or "c0" in rid) else (LESSON if ("lesson" in rid or "l05" in rid or "l06" in rid) else FILES)
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                 "evidence": "Carried from round 15 (" + prefix + " byte-identical since the previous pin c093bf5): " + r["evidence"]})
for rid, loc, check, status, ev in NEW_ROWS:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

# r13-l06-unrounded-difference-basis: re-verified in RERUN
mut = []
for line in (out_dir / "mutate_r16_full.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+): (.*) -> (.*)$", line)
    if m:
        name, desc, killed = m.group(1), m.group(2), m.group(3)
        mut.append({"file": f"ledgers/CF1/mutants/{name}", "description": desc, "killed_by": killed})
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = "Architect ruling on the cards count: amend plans/CF1-build-plan.md line 240 to the BUILDER_RULES section 7 rule (one card per definition, theorem, key formula, key result and misconception), or trim cards.json to four to six per lesson with the owning builder."
verdict_fail = any(r["status"] != "PASS" for r in rows)
frag = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 16,
    "verifier": "independent verifier (Haiku), round 16 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
    "pin": "c5daab2 (detached, /tmp/verify16-CF1-d)",
    "base": "c093bf5 (round-15 pin); delta computed with git diff c093bf5 c5daab2 and read per hunk",
    "checkout": "/tmp/verify16-CF1-d",
    "scratch": "/tmp/CF1-v/d16",
    "verified_at": "2026-10-28",
    "verdict": "FAIL" if verdict_fail else "PASS",
    "rows": rows,
    "mutants": mut,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": "Scripts: ledgers/CF1/scripts/CF1-d-r16/ (make_mutants.py, make_alts.py, run_alts.py, collect.py, build_fragment.py) and outputs in ledgers/CF1/scripts/CF1-d-r16/out/ (mutate_r16_full.out, alts_all_prior.out). Mutants r16_01..03 in ledgers/CF1/mutants/. registry_flags are carried unchanged: references/references.json is byte-identical since the round-15 pin.",
    "summary": f"CF1-d round 16: {len(rows)} rows, {sum(r['status']=='PASS' for r in rows)} PASS, {sum(r['status']!='PASS' for r in rows)} non-PASS (cards-count-vs-plan, carried and re-verified). Mutants {len(mut)}/{len(mut)} killed including 3 new student-error mutants. 47 alternative engines (including 3 new) PASS 50/50 seeds. Lab twins, graders, page smoke and registry gates PASS.",
}
out = ROOT / "ledgers/CF1/CF1-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "mutants", len(mut), "verdict", frag["verdict"], "previous ids kept", len(seen), "all kept", seen <= {r["id"] for r in rows})
