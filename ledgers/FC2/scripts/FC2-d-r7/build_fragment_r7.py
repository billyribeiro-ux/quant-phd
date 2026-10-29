import json, re, subprocess
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyC7-FC2-d")
S = "ledgers/FC2/scripts/FC2-d-r7/"
old = json.loads(Path("/Users/billyribeiro/.fanout/frags/C-FC2-d.round6.json").read_text())

# Mutants from the round-7 run of tools/mutate_graders.py --unit FC2
mut_lines = (ROOT / S / "mutate_graders_r7.out").read_text().splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"^(KILLED|SURVIVED) (\S+)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({
        "name": name,
        "description": desc,
        "killed_by": killed if status == "KILLED" else "SURVIVED (ruled non-finding, see notes)",
    })

carried = "Carried from round 6 (course/modules/FC/FC2/grader/ and tests/labs/FC2/ byte-identical between pins 9fd6aed and 0d2d0f3; checked by git diff): "
rows = []
def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})

row("fc2d-gate-check-projects", "tools/check_projects.py --all", "tools/check_projects.py",
    "PASS", f"{S}check_projects.out: 'check_projects FC2: PASS', rc=0 (run this round on 0d2d0f3).")
row("fc2d-gate-check-pages", "tools/check_pages.py --all", "tools/check_pages.py",
    "PASS", f"{S}check_pages.out: 'check_pages FC2: PASS', rc=0 (this round). A single-unit invocation I tried with a positional argument exited 2 (usage); the --all run is the gate.")
row("fc2d-gate-check-dag", "tools/check_dag.py --all", "tools/check_dag.py",
    "PASS", f"{S}check_dag.out: 'check_dag FC2: PASS', rc=0 (this round).")
row("fc2d-gate-run-labs", "tools/run_labs.py --unit FC2", "project labs lab-FC2-project-1..3",
    "PASS", f"{S}run_labs.out: 'run_labs FC2: PASS (11/11)', rc=0 (this round).")
row("fc2d-gate-page-smoke", "tools/page_smoke.py --unit FC2", "course/modules/FC/FC2/project.html",
    "PASS", f"{S}page_smoke.out: 'page_smoke FC2: PASS', rc=0 (this round).")
row("fc2d-gate-run-graders", "tools/run_graders.py --unit FC2 --seeds 0-49", "course/modules/FC/FC2/grader",
    "PASS", f"{S}run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)', rc=0 (this round).")
row("fc2d-gate-ruff-mypy", "ruff check and format --check; mypy --no-incremental on grader", "course/modules/FC/FC2/grader/*.py; tests/labs/FC2; new mutants",
    "PASS", f"{S}ruff_r7.out: 'All checks passed!' for the three new mutants (rc=0); ruff format --check on grader and labs: '15 files already formatted' (round-6 scratch, grader unchanged); mypy --no-incremental reference.py instance.py: 'Success: no issues found in 2 source files'. test_project.py is not mypy-checked here because it imports scanner, which is not in the checkout (same as round 6).")
row("fc2d-gate-pytest", "pytest -k 'FC2 or project' over tests/", "tests/",
    "PASS", f"{S}pytest_fc2.out: rc=0 (this round, filtered to FC2/project selection; not the full repo suite).")
row("fc2d-gate-verify-refs", "tools/verify_refs.py --offline", "references/references.json",
    "PASS", f"{S}verify_refs.out: 'offline integrity: 560 entries, 0 problems', rc=0 (this round). The live run was not run.")
row("fc2d-collect-count", "pytest --collect-only on the reference solution, seeds 0-49", "course/modules/FC/FC2/project.html:320 ('collects 90 checks')",
    "PASS", "Run this round in /tmp/fc2d-r7-count with the grader copied and reference.py as scanner.py: 'N tests collected' gave 90 for every seed 0..49 (50 of 50). The page's figure 90 matches.")
row("fc2d-seeds-84", "grader suite on reference, seeds 0-49", "course/modules/FC/FC2/grader/test_project.py",
    "PASS", f"{S}run_graders.out: reference 50/50 seeds pass under --assert=plain -W error (this round).")
row("fc2d-starter-fails", "starter.py as scanner.py fails the suite", "course/modules/FC/FC2/grader/starter.py",
    "PASS", carried + "round-6 evidence ledgers/FC2/scripts/FC2-d-r6/count_out.txt '82 failed, 8 passed'.")
row("fc2d-alternatives", "five alternative correct implementations pass; over-constraint check", "ledgers/FC2/scripts/FC2-d-r6/alts_r6.out; ledgers/FC2/scripts/FC2-d-r7/alt7_make.py",
    "PASS", "Round-6 alternatives carried (grader byte-identical). New alt7 this round (Decimal floor-half-up rounding plus Lagrange cross-multiplied chord, with no Fraction in the test): passes all 50 seeds under python -I -W error --assert=plain (no FAIL lines), and agrees with reference.scan on 4000 random chains (28726 reference findings, 0 disagreements; ledgers/FC2/scripts/FC2-d-r7/alt7_diff_check.py).")
row("fc2d-mutate-builder", "tools/mutate_graders.py --unit FC2 (all mutants)", "ledgers/FC2/mutants/",
    "PASS", f"{S}mutate_graders_r7.out: 50/51 killed this round (51 = 48 prior + 3 new). The one survivor r5_d_explanation_direction_reversed is the ruled non-finding (see fc2d-r5-mut-direction). The tool exits 1 on that survivor.")
row("fc2d-mut-v03", "mutant v03", "ledgers/FC2/mutants/v03_parity_gross_bankers_round.py", "PASS", f"{S}mutate_graders_r7.out: KILLED by test_half_cent_gross_rounds_once_up (seed 0).")
row("fc2d-mut-v04", "mutant v04", "ledgers/FC2/mutants/v04_convexity_returns_one_based_index.py", "PASS", f"{S}mutate_graders_r7.out: KILLED by test_convexity_matches_exhaustive_oracle_second_chain (seed 0).")
row("fc2d-mut-v05", "mutant v05", "ledgers/FC2/mutants/v05_convexity_findings_before_parity.py", "PASS", f"{S}mutate_graders_r7.out: KILLED by test_findings_are_in_parity_then_convexity_order (seed 0).")
row("fc2d-mut-v06", "mutant v06", "ledgers/FC2/mutants/v06_gross_rounds_signed_gap_then_abs.py", "PASS", f"{S}mutate_graders_r7.out: KILLED by test_negative_half_cent_gross_rounds_once_up_in_magnitude (seed 0).")
row("fc2d-mut-v01-boundary", "mutant v01", "ledgers/FC2/mutants/v01_convexity_zero_net_kept.py", "PASS", f"{S}mutate_graders_r7.out: KILLED by test_convexity_finding_with_net_exactly_zero_is_not_returned (seed 0).")
row("fc2d-mut-v02-labels", "mutant v02", "ledgers/FC2/mutants/v02_parity_explanation_names_P1_only.py", "PASS", f"{S}mutate_graders_r7.out: KILLED by test_scan_explanations_are_nonempty_and_name_the_rule (seed 1).")
row("fc2d-r5-mut-swap-weights", "mutant r5_b", "ledgers/FC2/mutants/r5_b_swapped_chord_weights.py", "PASS", f"{S}mutate_graders_r7.out: KILLED by test_unequal_grid_no_false_positive (seed 0).")
row("fc2d-r5-mut-skip-first", "mutant r5_c", "ledgers/FC2/mutants/r5_c_parity_loop_skips_first_strike.py", "PASS", f"{S}mutate_graders_r7.out: KILLED (seed 0).")
row("fc2d-r5-mut-direction", "mutant r5_d (survivor, ruled)", "ledgers/FC2/mutants/r5_d_explanation_direction_reversed.py; grader/test_project.py; project.html spec (explanation sentence)",
    "PASS", f"{S}mutate_graders_r7.out: SURVIVED. Ruling kept (round 6): project.html spec states 'The explanation is a non-empty string that names the rule and the assumptions the finding depends on, by the labels in the conventions'. The page requires no sign or direction statement in the explanation string; direction appears in the settlement rubric (C5), not in the grader spec. Under the ruling that a new surviving grader mutant is FAIL only when the page states the violated behaviour, this is not a finding. Recorded as a survivor, not hidden.")
row("fc2d-r5-grader-exact-ties", "round-5 FAIL: exact-tie mutant", "course/modules/FC/FC2/grader/test_project.py:273-279, 713-727",
    "PASS", carried + f"{S}mutate_graders_r7.out: r5_a_float_discount_ties KILLED (this round).")
row("fc2d-r6-new-tie-tests", "round-6 tie tests", "course/modules/FC/FC2/grader/test_project.py:273-279, 713-727",
    "PASS", carried + "the three tests are present and pass on reference and alt7 (50/50 seeds each).")
row("fc2d-r6-alt6-overconstraint", "round-6 alt6 over-constraint", "ledgers/FC2/scripts/FC2-d-r6/alt6_integer_crossmul.py",
    "PASS", carried + "alt6 result; alt7 this round also passes (see fc2d-alternatives).")
row("fc2d-r6-mut-new", "round-6 new mutants r6_a..c", "ledgers/FC2/mutants/r6_a_ties_away_from_zero_on_negative_gap.py; r6_b_convexity_strike_is_left_neighbour.py; r6_c_zero_fee_rejected.py",
    "PASS", f"{S}mutate_graders_r7.out: all three KILLED this round.")
row("fc2d-r7-mut-new", "round-7 new student-error mutants r7_a..c (>= 3 required)", "ledgers/FC2/mutants/r7_a_duplicate_strikes_accepted.py; r7_b_parity_loop_skips_last_strike.py; r7_c_discounted_strike_floored.py",
    "PASS", f"{S}mutate_graders_r7.out: r7_a KILLED by test_strikes_equal_neighbours_are_rejected_by_scan (seed 0); r7_b KILLED by test_cost_is_charged_per_leg_not_once (seed 0); r7_c KILLED by test_half_cent_gross_rounds_once_up (seed 0). Each is one edit of reference.py (diff reviewed). An earlier version failed for a spurious reason (a second docstring broke the __future__ import, so it was a collection error); fixed and re-run, so the kills above are real assertion kills.")
row("fc2d-grader-stdlib", "stdlib-only grader", "course/modules/FC/FC2/grader/instance.py, reference.py, test_project.py", "PASS", carried + "test_module_imports_standard_library_only passes on reference and alt7.")
row("fc2d-grader-messages", "error-message tests", "course/modules/FC/FC2/grader/test_project.py", "PASS", carried + "suite passes 50/50 this round.")
row("fc2d-grader-instance-validity", "instance generator validity", "course/modules/FC/FC2/grader/instance.py:46-59, 102, 109-110", "PASS", carried + f"{S}run_graders.out 50/50.")
row("fc2d-grader-instance-diversity", "instance diversity", "course/modules/FC/FC2/grader/instance.py:6-9, 74-80", "PASS", carried + f"{S}run_graders.out 50/50.")
row("fc2d-lab1", "project lab 1 page block", "course/modules/FC/FC2/project.html lab-FC2-project-1; tests/labs/FC2/lab-FC2-project-1.py", "PASS",
    f"{S}lab-project-1.out: twin run python -I -W error, rc=0 (this round); run_labs PASS 11/11. The page block is unchanged this round (delta hunks are lines 37, 282, 538 only).")
row("fc2d-lab2", "project lab 2 page block", "course/modules/FC/FC2/project.html lab-FC2-project-2; tests/labs/FC2/lab-FC2-project-2.py", "PASS",
    f"{S}lab-project-2.out: twin run python -I -W error, rc=0 (this round); run_labs PASS 11/11.")
row("fc2d-lab3", "project lab 3 page block", "course/modules/FC/FC2/project.html:486 and the lab-FC2-project-3 block; tests/labs/FC2/lab-FC2-project-3.py", "PASS",
    f"{S}lab-project-3.out: twin output lists findings kept 3: parity 6500 gross 226 net 166; parity 7000 gross 540 net 480; convexity 6000 gross 63 net 3; parity 4500 gross 60 net 0, dropped. This matches the page's interpretation text at project.html:486 and the exemplar figures. rc=0.")
row("fc2d-lab-twins-pure", "twins run alone under python -I -W error", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py", "PASS",
    f"{S}lab-project-{{1,2,3}}.out: each rc=0 with -I -W error this round.")
row("fc2d-rubric-observable", "rubric table observable levels", "course/modules/FC/FC2/project.html rubric table (about lines 503-514)", "PASS",
    carried + "the rubric table is not in the delta hunks (37, 282, 538).")
row("fc2d-rubric-calib-A", "exemplar A passage and annotation", "course/modules/FC/FC2/project.html article#exemplar-a", "PASS",
    carried + "exemplar-a block not in the delta hunks.")
row("fc2d-rubric-calib-B", "exemplar B passage and annotation", "course/modules/FC/FC2/project.html:538 (exemplar-b findings paragraph)", "PASS",
    f"Re-read this round. The only change is the added formula '(500 + 2 × 151) / 3 = 802/3'. Re-derived: chord weights on 5000 and 6500 at strike 6000 are 500/1500 = 1/3 and 1000/1500 = 2/3; chord = 500/3 + 302/3 = 802/3; 330 - 802/3 = 188/3 = 62.67, rounded half up to 63; net 63 - 60 = 3. Parity 6500: 151 - 1100 - (5000 - 6175) = 226; net 166. Parity 7000: 90 - 1200 - (5000 - 6650) = 540; net 480. All match {S}lab-project-3.out.")
row("fc2d-exemplar-numbers", "exemplar numbers", "course/modules/FC/FC2/project.html exemplar-a and exemplar-b blocks", "PASS",
    f"Exemplar B numbers re-derived this round (see fc2d-rubric-calib-B). Exemplar A block carried from round 6 (not in the delta).")
row("fc2d-exemplar-annotations", "exemplar annotations", "course/modules/FC/FC2/project.html annotation blocks", "PASS",
    carried + "annotation blocks are not in the delta hunks.")
row("fc2d-spec-explanation-labels", "explanation labels match spec", "course/modules/FC/FC2/project.html:301, grader/test_project.py PARITY_ and convexity label tests, reference.py _explain_parity, _explain_convexity", "PASS",
    "Re-checked this round. Spec states the explanation names the rule and the assumptions by the labels in the conventions (project.html spec text). reference.py _explain_parity names P1, P2, P3, P4, P6; _explain_convexity names P1, P2, P5, P6. Consistent with the conventions list.")
row("fc2d-spec-errors-scope", "named error conditions and scope", "course/modules/FC/FC2/project.html:306-316", "PASS",
    carried + "lines 306-316 not in the delta hunks.")
row("fc2d-hours", "hours arithmetic", "course/modules/FC/FC2/project.html time-budget table; course/modules/FC/FC2/index.html:29", "PASS",
    "Re-computed this round: components 2 + 3 + 5 + 9 + 3 + 5 + 3 = 30, equal to the table total 30 and to data-hours-project=30 at index.html:29. Hub lessons 60 + project 30 = 90, matching '30 of the unit's 90 hours' in the table. No hours figure changed this round.")
row("fc2d-cards-sample", "card sample and reads", "course/modules/FC/FC2/cards.json (142 cards)", "PASS",
    "Round 7: every one of the 142 cards was read this round (front, back, grade and basis). The cards changed since round 6 were checked against the current lesson text: c047 (A8′, Proposition 1.3, Problem P3: L03 lines 66-82, 422, 357); c048 (A8′ and Proposition 1.3 at L03:422; Definition 1.1 of Lesson 2 at L02:58); c050 (A8, Proposition 3.3 at L03:424, Lab 3 Part B at L03:306); c059 (Proposition 2.3 uses A2, A3, A5, L04:249, Remark 2.4 at L04:110); c060 (Proposition 2.2 uses A2, A3, L04:249); c064 (Theorem 1.2 at L05:63, Remark 1.3 at L05:70); c078 (Theorem 2.2 under A1-A5 and (N), L05:84-85; min(S_τ, K) at L05:95); c085 (Theorem 1.4 hypotheses A1, A2, A3, A5, A6 at L06:77-78; Example 1.6 at L06:98); c087 (Theorem 1.4 at L06:77); c113 (Proposition 1.4 under A1-A5, A7, A8 at L07:95-97); c144 (Proposition 3.3 at L03:424). Numbers in the cards re-derived with python: 51.2658 (c021), 4.877058 (c126), 0.5378084 -> 0.537808 (c115), 0.577493 and 12.1623 (c116), 40.48 (c076), 6.56 (c056), 14.58 (c057), 17 (c061), 114.15 (c131), 10.450584 and 5.573526 (c109, c118), -91 cents and -0.0049977 (c110, c117), and the signs of the nine error values (c111). All match. Gaps in the ids (c031, c077) predate this round (see fc2d-cards-ids). Subject-level limit: I did not re-derive every number in every unchanged card; the round-6 numeric pass is carried for those (see fc2d-cards-numbers).")
row("fc2d-cards-dups", "no duplicate cards", "course/modules/FC/FC2/cards.json FC2-c064 (c145 removed)", "PASS",
    "Round 6 FAIL fixed: FC2-c145 is removed (cards.json now has 142 entries; c144 is the last). Checks this round (ledgers/FC2/scripts/FC2-d-r7/card_numbers_r7.py and the inline check): unique ids, unique fronts, unique backs. Near-duplicate fronts (token Jaccard > 0.5): c042/c045 (definition of the par rate vs the Lab 3 printed value), c042/c050, c105/c115 (general n vs four-step), c116/c126, c126/c131 (same question at different inputs). Each asks a different fact, so none is a duplicate. c063 and c064 are on one identity, but c063 asks the identity and c064 asks whether it holds for every strike.")
row("fc2d-cards-numbers", "card numbers appear in lesson", "course/modules/FC/FC2/cards.json", "PASS",
    "Round 6 numeric pass carried for unchanged cards (byte-identical entries). Changed cards this round add hypothesis labels only, no new numbers. Spot re-derivations this round are listed in fc2d-cards-sample.")
row("fc2d-cards-grades", "grades and basis", "course/modules/FC/FC2/cards.json FC2-c049 and the 34 ungraded cards", "PASS",
    "Round 6 FAIL fix carried: c049 is C with basis. Changed graded cards each carry grade T and (where a computed result) a basis. 34 cards have no grade field: they state definitions, assumptions or formulas (e.g. c001, c016-c018, c033-c035, c039-c040, c088, c139-c144), which BUILDER_RULES §7 does not require to be graded.")
row("fc2d-cards-ids", "card ids", "course/modules/FC/FC2/cards.json", "PASS",
    f"Ids are unique and increase to FC2-c144 (142 cards). Gaps at FC2-c031 and FC2-c077 are present at pins 04626e9, 9fd6aed and 0d2d0f3 (script ledgers/FC2/scripts/FC2-d-r7/card_ids_pins_r7.py output: missing [31, 77] for each). BUILDER_RULES §7 says ids 'run upward', which they do. Noted, not a FAIL.")
row("fc2d-cards-c132", "card c132 against L05", "course/modules/FC/FC2/cards.json FC2-c132; L05.html Theorem 4.1 and Remark 4.2", "PASS",
    carried + "entry c132 is not in the cards.json diff, and Remark 4.2 (L05 line 309 region) and Theorem 4.1 (L05 line 300) hypotheses are A1-A5, (N), r ≥ 0 as the card states.")
row("fc2d-reading-theorem-locator", "theorem locator on the reading list", "course/modules/FC/FC2/project.html #reading; course/modules/FC/FC2/L05.html", "PASS",
    carried + "L05 Theorem 1.2 and Theorem 3.2 are still at the cited lines (L05 changes this round are inside paragraphs, not new lines).")
row("fc2d-references-no-locator", "references carry no locator", "course/modules/FC/FC2/project.html #reading and data-cite", "PASS",
    carried + "project.html http count this round: 0 (see fc2d-no-external).")
row("fc2d-notation", "notation against notation/notation.json", "course/modules/FC/FC2/project.html (C, P, S, K, df, D, P1..P6, R_f)", "PASS",
    carried + "D = e^{-rτ} is used for the discount factor in the lessons (L05 Theorem 1.2 restatement, L05 line 475), and project.html:335 says so. No symbol reused.")
row("fc2d-simulated-label", "SIMULATED label on the chain", "course/modules/FC/FC2/project.html (SIMULATED count 18; lede line 37; spec 285-289)", "PASS",
    "Re-checked this round: the word SIMULATED appears 18 times in project.html and remains on the lede (line 37) after the edit; the chain is labelled in the spec and the autograder text.")
row("fc2d-process-banned", "no process words in learner text", "course/modules/FC/FC2/project.html, cards.json", "PASS",
    "Re-run this round: regex for builder, verifier, ledger, fragment, TODO, placeholder, round N, pinned, this build, agent, reviewer: 0 hits in project.html text and 0 in cards.json.")
row("fc2d-ladder-claims", "ladder claims", "course/modules/FC/FC2/project.html #ladder (lines 41-50)", "PASS", carried + "lines 41-50 not in the delta.")
row("fc2d-curriculum-scope", "curriculum scope of the page", "curriculum/02-economics-finance-core.yaml:425-431; project.html:37, 285", "PASS",
    carried + "project.html:37 has changed text this round; the SIMULATED statement and the scope sentence are unchanged in meaning.")
row("fc2d-no-external", "no external links on the project page", "course/modules/FC/FC2/project.html", "PASS",
    "Re-run this round: grep count of 'http' in project.html = 0. The page-smoke run (fc2d-gate-page-smoke) passes.")
row("fc2d-new-tests", "tests added by the round-6 delta", "course/modules/FC/FC2/grader/test_project.py", "PASS", carried + "the grader file is unchanged since round 6.")
row("fc2d-lab1-hypothesis-terms", "lab 1 hypothesis terms", "course/modules/FC/FC2/project.html:55 and :333", "PASS", carried + "line 55 unchanged; P6 at line 333 defines fee and half-spread.")
row("fc2d-r6-project-line335", "model-free defined before the rubric uses it", "course/modules/FC/FC2/project.html:335 and :37", "PASS",
    "Line 335 defines model-free. Line 37 (lede) now uses the term first, with a link to '#conventions' (the anchor is at project.html:325, '<h3 id=\"conventions\">'), so the term is introduced by reference before its definition. This is a forward link, not an undefined term.")
row("fc2d-r7-project-anchor-links", "new in-page links resolve", "course/modules/FC/FC2/project.html:37, :282 (href=\"#conventions\")", "PASS",
    "grep: id=\"conventions\" at project.html:325. Both links resolve to it.")
row("fc2d-r7-cards-changed-hypotheses", "cards whose hypothesis labels changed", "course/modules/FC/FC2/cards.json (c047, c048, c050, c059, c060, c064, c078, c085, c087, c113, c144)", "PASS",
    "Each added hypothesis label was checked against the lesson statement it names (see fc2d-cards-sample). No label names an assumption or result the lesson does not state.")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 7 (did not build FC2)",
    "pin": "0d2d0f3",
    "base": "9fd6aed (round-6 pin); the delta is listed in notes",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC7-FC2-d",
    "scratch": "/tmp/fc2d-r7-* (count dir, alt7 dir, nums and binomial scripts, ids script); not in the ledger",
    "verified_at": "2026-10-29T12:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [{"name": m["name"], "description": m["description"], "killed_by": m["killed_by"]} for m in mutants],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 7 on pin 0d2d0f3 (round-6 pin 9fd6aed). Delta inside this slice: project.html hunks at lines 37 (lede adds a link to #conventions), 282 (spec context adds the same link) and 538 (exemplar B adds '(500 + 2 × 151) / 3 = 802/3'); cards.json: c047, c048, c050, c059, c060, c064 (text), c078, c085, c087, c113, c144 (text) and c145 removed. Grader, tests/labs/FC2 and the FC2 lesson files that the grader and labs use are byte-identical to 9fd6aed (git diff empty). L04, L05, L06 lesson text changed (why-it-matters and a few sentences); the cards were checked against the current lesson text. "
        "Round-6 FAIL fc2d-cards-dups is fixed (c145 removed; no duplicate fronts or backs). "
        "Mutants: 51 (48 prior and 3 new, r7_a..c). 50 killed, 1 survivor r5_d, a ruled non-finding (see fc2d-r5-mut-direction). The mutate tool exits 1 because of r5_d. "
        "Not run or not possible: test_project.py collect-only and mypy need scanner.py (absent in the checkout) and were run on a scratch copy with reference.py as scanner.py; the full repo gate; the live verify_refs run; a browser check of the autograder panel. The ledger helper check (ledger.validate) was not run on this fragment because the helper's validate signature was not read in this round. "
        "Scripts: the card-count loop was run inline in a scratch dir (collect_count_r7.sh is a copy of that loop, not separately executed). "
        "Open observation, not a FAIL: card id gaps at FC2-c031 and FC2-c077 predate this round."
    ),
    "summary": (
        "FC2-d round 7: verdict " + verdict + ". All gates in this slice pass on 0d2d0f3 (check_pages, check_dag, check_projects, run_labs 11/11, run_graders 50/50, page_smoke, ruff, mypy on reference and instance, pytest FC2 filter, verify_refs offline). "
        "The round-6 FAIL (fc2d-cards-dups, duplicate c145) is fixed. Collect count is 90 on every seed, matching the page. "
        "Mutants: 50 of 51 killed, including the three new student-error mutants r7_a..c; r5_d survives and is the ruled non-finding. "
        "A new alternative implementation (Decimal and Lagrange) passes all 50 seeds and agrees with the reference on 4000 random chains."
    ),
}
out = ROOT / "ledgers/FC2/FC2-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("written", out, verdict, len(rows), "rows", len(mutants), "mutants")
