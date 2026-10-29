"""Builds the round-38 AC4-e fragment from the round-35 fragment plus this round's fresh evidence."""
import json, sys, datetime

PREV = "/tmp/fanout-frags/AC4-e.round35.json"
prev = json.load(open(PREV, encoding="utf-8"))
sel = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = sys.argv[2]
hot = set(sel["hot"])
PIN_NOTE = "5aeaaf0"

FRESH = {
    "proj-card-c078": ("PASS", "course/modules/AC/AC4/cards.json (AC4-c078 back); course/modules/AC/AC4/L06.html Proposition 2.1 (line 79); L06.html line 56 (Q_b defined)",
        "Round 35 FAIL resolved. The back now reads 'with a budget that has budgeted units (Q_b > 0), for any actual units, actual selling prices and actual kilograms, provided the actual material price equals the standard price pi'. Proposition 2.1 (L06.html line 79) reads 'Under Definitions 1.1 and 1.2, with Q_b > 0 and the actual material price equal to pi'. Q_b is defined at L06.html line 56. Card object diffed against pin 5aeaaf0 with python json: only AC4-c023 and AC4-c078 differ."),
    "proj-r30-card-c023-hypothesis": ("PASS", "course/modules/AC/AC4/cards.json (AC4-c023 back); course/modules/AC/AC4/L02.html line 70-71 (Proposition 2.2 'Let m > 0')",
        "Round 35 FAIL resolved. The back now reads 'R_BE = pQ* = F/(m/p), where m/p is the contribution margin ratio, with m > 0 (Proposition 2.2).' Proposition 2.2 (L02.html line 71) starts 'Let m > 0.' Checked by json diff against 5aeaaf0 (see proj-card-c078)."),
    "proj-r30-rubric-observability": ("PASS", "course/modules/AC/AC4/project.html line 315 (C2 level 2 cell) and line 317 (C4 level 1 cell); scoring rule line 308",
        "Round 35 FAIL resolved. C2 level 2 now reads 'At least two variances tied to a case figure.' (the untestable 'described in general terms' is gone). C4 level 1 now reads 'No recommendation, or a recommendation that names no action for any unfavourable variance it discusses.' Both use terms defined at line 308 (tied to a case figure; action). A separate observability defect in C2 level 3 is row proj-r38-rubric-C2-level3-monotone."),
    "proj-r38-rubric-C2-level3-monotone": ("FAIL", "course/modules/AC/AC4/project.html line 315 (C2 row, column 3 Proficient); scoring rule line 308",
        "Witness: a memo whose four variance paragraphs each name the products involved but state no case number. Level 3 of C2 reads 'Each of the four variances tied to a case figure, a named product or an input count'. Under line 308, 'a named product' alone satisfies the disjunction, so the level 3 descriptor is fully met. Level 2 reads 'At least two variances tied to a case figure', which this memo does not meet (zero variances tied to a case figure). The scoring rule takes the highest level whose descriptor is fully met, so the memo scores 3 while failing level 2: the rubric is not monotone and a Proficient C2 needs no case figure at all."),
    "proj-calib-A-annotation": ("PASS", "course/modules/AC/AC4/project.html lines 343-351 (exemplar A annotation); lab output from tests/labs/AC4/lab-AC4-project-1.py (run this round)",
        "Recomputed from the lab: volume 542,857 (step 4) = flexed 3,142,857 - master 2,600,000 (steps 1-2); price 180,000 (step 3); mix -462,857 (step 6); efficiency -40,000 (step 5); total 220,000 (step 7). Hand check of the mix: budget unit margins 5,000-3*200 = 4,400 (Standard) and 9,000-5*200 = 8,000 (Deluxe); flexed units 1,500*1,000/1,400 = 1,071.43 and 428.57; (1,200-1,071.43)*4,400 + (300-428.57)*8,000 = -462,857. The memo's +462,857 is the wrong sign, as annotated. Sum 542,857+180,000-462,857-40,000 = 220,000, matching the memo's Result. Annotation claims (efficiency untied; Standard earns the smaller margin; no input price stated) checked against memo text lines 331-340."),
    "proj-rubric-exhaustive": ("PASS", "course/modules/AC/AC4/project.html lines 312-318 (rubric table)",
        "Every (C4 and C2) combination of states is covered by some level: C4 levels 1-2 cover zero actions, some-but-not-all actions, and all actions without observation; the zero-action case is fixed by the scoring rule at line 308. Coverage only; monotonicity of C2 is row proj-r38-rubric-C2-level3-monotone."),
    "proj-rubric-C2-terms": ("PASS", "course/modules/AC/AC4/project.html line 308 (scoring rule terms) and lines 315, 343-345",
        "Terms used in the C2 rows ('tied to a case figure', 'named product', 'input count') are each defined in the scoring-rule paragraph at line 308 before use. The logical defect in the level 3 cell is a separate FAIL row."),
    "proj-r30-exemplars-calibration": ("PASS", "course/modules/AC/AC4/project.html lines 326-386; ledgers/AC4/scripts/AC4-e-r38/out/pytest_memo_page_checks.out",
        "pytest tests/test_memo_exemplars.py and tests/test_page_checks.py run this round: 55 passed, exit 0 (includes test_annotations_agree_with_the_exemplar_scores and test_every_exemplar_number_is_pinned_to_its_computation). Exemplar B annotations unchanged since the pin."),
    "proj-banned-phrases": ("PASS", "course/modules/AC/AC4/project.html; course/modules/AC/AC4/cards.json",
        "Regex scan this round for roughly, about N, historically, ellipsis, typically, usually, half of: no matches in project.html or cards.json. Process words (builder, verifier, round) grepped in project.html: no matches."),
    "proj-r15-no-banned-phrases-changed-lines": ("PASS", "course/modules/AC/AC4/project.html (whole file scan this round)", "Covered by the whole-file scan in proj-banned-phrases; no matches."),
    "proj-r23-banned-and-placeholders": ("PASS", "course/modules/AC/AC4/cards.json; course/modules/AC/AC4/project.html", "Whole-file scan this round (proj-banned-phrases); no banned phrases or placeholders found."),
    "proj-r30-pytest-generic": ("PASS", "tests/test_memo_exemplars.py; tests/test_page_checks.py; ledgers/AC4/scripts/AC4-e-r38/out/pytest_memo_page_checks.out", "Run this round: 55 passed, exit 0."),
    "proj-r30-collect-563": ("PASS", "course/modules/AC/AC4/grader/test_project.py; ledgers/AC4/scripts/AC4-e-r38/out/collect_ac4_ws.out", "pytest --collect-only on the reference solution in the run_graders workspace: 563 tests collected (exit 0). Also 563 with QF_SEED 3, 29 and 49."),
    "proj-collect-count": ("PASS", "course/modules/AC/AC4/grader/test_project.py; course/modules/AC/AC4/project.html line 265", "563 collected this round on the reference workspace; page line 265 says 563 checks."),
    "proj-r18-grading-count-563": ("PASS", "course/modules/AC/AC4/project.html line 265; grader/test_project.py", "563 collected this round (ledgers/AC4/scripts/AC4-e-r38/out/collect_ac4_ws.out); page says 563 checks."),
    "proj-r23-collect-count-seeds": ("PASS", "grader/test_project.py via collect_ws38.py with QF_SEED 3, 29, 49", "563 tests collected for each seed this round."),
    "proj-r18-collect-all-seeds": ("PASS", "grader/test_project.py; ledgers/AC4/scripts/AC4-e-r38/out/run_graders.out", "Collection checked on seeds 3, 29, 49 this round (563 each); run_graders.py --unit AC4 --seeds 0-49: reference 50/50 seeds PASS. Grader file unchanged since 5aeaaf0."),
    "proj-r17-collect-seeds": ("PASS", "grader/test_project.py; run_graders.out", "Re-run this round: reference 50/50 seeds; collection 563 on seeds 3, 29, 49."),
    "proj-r18-gates": ("PASS", "tools/check_pages.py --all; check_dag.py --all; check_projects.py --all; run_labs; page_smoke; ruff; mypy (outputs in ledgers/AC4/scripts/AC4-e-r38/out/)", "All re-run this round: check_pages AC4 PASS, check_dag AC4 PASS, check_projects AC4 PASS, run_labs AC4 PASS (10/10), page_smoke AC4 PASS, ruff check 'All checks passed', ruff format 220 files formatted, mypy 'no issues found in 153 source files'."),
    "proj-r18-check-tools": ("PASS", "tools/check_pages.py; check_dag.py; check_projects.py", "Re-run this round; AC4 PASS in all three."),
    "proj-r18-page-smoke": ("PASS", "tools/page_smoke.py --unit AC4 --pages project.html", "Re-run this round: page_smoke AC4 PASS, exit 0."),
    "proj-r18-run-labs": ("PASS", "tools/run_labs.py --unit AC4", "Re-run this round: run_labs AC4 PASS (10/10), exit 0. Twins project-1 and project-2 also run under python -I -W error, exit 0."),
    "proj-r18-verify-refs": ("PASS", "tools/verify_refs.py --unit AC4; tools/verify_refs.py --offline", "Re-run this round: live AC4 '2 of 560 entries, 0 problems'; offline '560 entries, 0 problems'."),
    "proj-r30-verify-refs": ("PASS", "references/references.json; tools/verify_refs.py", "Re-run this round (same outputs as proj-r18-verify-refs)."),
    "proj-r23-verify-refs": ("PASS", "tools/verify_refs.py --unit AC4 (live) and --offline", "Re-run this round: as proj-r18-verify-refs."),
    "proj-r23-gates-pages-dag-projects": ("PASS", "tools/check_pages.py --all; check_dag.py --all; check_projects.py --all", "Re-run this round: AC4 PASS in each."),
    "proj-r23-gates-labs-smoke-graders": ("PASS", "tools/run_labs.py --unit AC4; page_smoke.py --unit AC4; run_graders.py --unit AC4 --seeds 0-49", "Re-run this round: run_labs 10/10; page_smoke PASS; run_graders reference 50/50."),
    "proj-r23-gates-build-ruff-mypy": ("PASS", "ruff check .; ruff format --check .; mypy --no-incremental", "Re-run this round: ruff check passed; ruff format 220 files formatted; mypy no issues in 153 files. tools/build_site.py --check was NOT re-run this round (outside slice e)."),
    "proj-r30-ruff-mypy-buildsite": ("PASS", "ruff; mypy (repository configuration)", "Re-run this round: ruff check and format clean; mypy clean. build_site --check not re-run (outside slice e)."),
    "proj-r30-gates-check-tools": ("PASS", "tools/check_pages.py; check_dag.py; check_projects.py (--all)", "Re-run this round: AC4 PASS in each."),
    "proj-r30-page-smoke": ("PASS", "course/modules/AC/AC4/project.html via tools/page_smoke.py", "Re-run this round: PASS."),
    "proj-r30-run-graders-reference": ("PASS", "course/modules/AC/AC4/grader; tools/run_graders.py --unit AC4 --seeds 0-49", "Re-run this round: reference 50/50 seeds PASS."),
    "proj-r30-run-labs-twins": ("PASS", "tests/labs/AC4/lab-AC4-project-1.py; lab-AC4-project-2.py", "Re-run this round under python -I -W error: both exit 0 ('step 8 four variances sum to total: True')."),
    "proj-run-labs-ac4": ("PASS", "tests/labs/AC4 via tools/run_labs.py --unit AC4", "Re-run this round: 10/10 PASS."),
    "proj-run-graders-ac4": ("PASS", "course/modules/AC/AC4/grader", "Re-run this round: reference 50/50 PASS."),
    "proj-page-smoke": ("PASS", "course/modules/AC/AC4/project.html", "Re-run this round: PASS."),
    "proj-check-pages": ("PASS", "course/modules/AC/AC4/*.html and cards.json", "Re-run this round: check_pages AC4 PASS."),
    "proj-check-dag": ("PASS", "course/modules/AC/AC4/", "Re-run this round: check_dag AC4 PASS."),
    "proj-check-projects": ("PASS", "course/modules/AC/AC4/project.html", "Re-run this round: check_projects AC4 PASS."),
    "proj-ruff-mypy": ("PASS", "course/modules/AC/AC4/grader; tests/labs/AC4", "Re-run this round: ruff and mypy clean."),
    "proj-r23-cards-L03-L04-carry-note": ("PASS", "tests/labs/AC4/lab-AC4-L03-1.py; tests/labs/AC4/lab-AC4-L04-1.py; course/modules/AC/AC4/L03.html line 325; L04.html lines 74, 321",
        "L04 twin changed this round (new 'Uneven pool' line, output line 321 of L04.html). Re-run: L04 twin exit 0, last line 'Uneven pool (100000 cents over 3 driver units): refused', matching L04.html line 321. L03 twin run: 'avoidable make cost per unit ... 9.10' is its second line after the title, as the L03 interpretation (line 325) now says."),
    "proj-r17-cards-c058": ("PASS", "course/modules/AC/AC4/cards.json (AC4-c058); course/modules/AC/AC4/L04.html line 59 (Definition 1.1), line 487 (Key results row)",
        "L04 gained 6 lines above Key results, so the summary line moved from 481 to 487 (the cited text is unchanged). Card text 'The activity method, which assigns each pool by its own driver (Definition 1.1, stage one)' is unchanged and matches Definition 1.1 at line 58-59."),
    "proj-r23-delta-scope": ("PASS", "course/modules/AC/AC4/* and tests/labs/AC4/* diffed 5aeaaf0..81ff53b", "Changed this delta: project.html lines 315, 317, 345; cards.json AC4-c023 and AC4-c078; L03.html lines 325 and 487 (outside slice e, checked where cards cite them); L04.html lines 74 and 275-321; tests/labs/AC4/lab-AC4-L04-1.py. grader/ unchanged; project labs unchanged."),
    "proj-r30-delta-scope": ("PASS", "course/modules/AC/AC4/*; tests/labs/AC4/*; ledgers/AC4/mutants", "Same delta as proj-r23-delta-scope (5aeaaf0..81ff53b), plus 43 new files under ledgers/AC4/mutants from earlier rounds."),
    "proj-r30-mutants-top-level": ("PASS", "ledgers/AC4/mutants/*.py (157 top-level files)", "Re-run this round: mutate_graders --unit AC4 --seeds 0-49 over 153 top-level mutants: 153/153 KILLED (out/mutate_ac4.out). The 4 new r38e mutants (01, 03, 04, 05) were run with runfiles.py: all KILLED. r38e_02 is equivalent (see notes)."),
    "proj-autograder-rerun-mutants-m01-m37": ("PASS", "ledgers/AC4/mutants (top level and AC4-e-r23 subdirectory)", "Re-run this round: 153/153 top-level KILLED; AC4-e-r23 fx23_01..06 6/6 KILLED (runfiles.py, seeds 0-49)."),
    "proj-mutant-descriptions": ("PASS", "ledgers/AC4/mutants/ (157 top-level files)", "Each top-level mutant docstring read by the runner; the four new r38e files carry a one-sentence student-error description in their docstring."),
}

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FRESH:
        st, loc, ev = FRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": st, "evidence": ev})
        continue
    if rid in hot:
        # re-run this round by the mutate, gate or memo command above; the subject is a mutant file or gate output
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": "Re-run this round: mutant or gate command in ledgers/AC4/scripts/AC4-e-r38/out/ (mutate_ac4.out: 153/153 KILLED; run_cmds outputs all PASS). " + "Prior evidence: " + r["evidence"][:300]})
        continue
    assert r["status"] == "PASS", rid
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                 "evidence": "Carried from round 35 (the cited subject is byte-identical since the pin 5aeaaf0; the 5aeaaf0..81ff53b delta touched only project.html lines 315, 317, 345, cards.json AC4-c023/c078, L03/L04 text outside the cited lines, and lab-AC4-L04-1.py): " + r["evidence"]})

new_rows = [
    {"id": "proj-r38-mutants-new-student-errors", "check": "Four new student-error mutants of the project grader are caught",
     "location": "ledgers/AC4/mutants/r38e_01_volume_variance_reported_as_magnitude.py; r38e_03_master_budget_skips_unsold_products.py; r38e_04_efficiency_skips_unbudgeted_products.py; r38e_05_price_variance_against_standard_cost.py",
     "status": "PASS",
     "evidence": "runfiles.py seeds 0-49: r38e_01 KILLED by test_single_product_has_no_mix_variance (seed 0); r38e_03 KILLED by test_price_change_on_an_unsold_product_has_no_price_variance (seed 0); r38e_04 KILLED by test_product_with_no_budgeted_units (seed 0); r38e_05 KILLED by test_every_grader_seed_reconciles_exactly[30] (seed 0). Each is a plausible student error that the page's spec covers (volume sign both ways; master budget covers every product; efficiency counts actual output of every product; price variance against budgeted selling price)."},
    {"id": "proj-r38-equivalent-total-sum-of-parts", "check": "Mutant: total taken as the sum of the four variances is equivalent",
     "location": "ledgers/AC4/scripts/AC4-e-r38/equivalent/r38e_02_total_is_sum_of_the_four_parts.py; course/modules/AC/AC4/grader/reference.py variance_decomposition",
     "status": "PASS",
     "evidence": "Proof: with sales_volume = flexed - master, sales_mix = actual_mix_contribution - flexed, sales_price = sum(u*(ap-bp)), efficiency = I*(sum(s*u) - A), actual_mix_contribution = sum(u*(bp - s*I)) - F, the sum of the four equals sum(u*ap) - I*A - F - master = actual_profit - master for every input. So the mutant returns the same dict on every input; it is not killed and is not a student error the spec forbids. Out of the mutants list (equivalent). It is caught in principle only by an independent oracle, and the grader has one (test_four_variances_and_total_match_oracle), so the reconciliation test does not depend on this identity."},
    {"id": "proj-r38-alternatives-correct", "check": "Three alternative correct engines pass the grader (over-constraint check)",
     "location": "ledgers/AC4/scripts/AC4-e-r38/alts/alt38_a_decimal_half_up.py; alt38_b_total_from_ledger.py; alt38_c_floor_half_and_type_check.py",
     "status": "PASS",
     "evidence": "runfiles.py seeds 0-49: each PASS 50/50 seeds. a: nearest cent via Decimal quantize ROUND_HALF_UP; b: total computed from the actual ledger (units times actual price, less input cost, less fixed) less master instead of actual_profit - master; c: floor(x + 1/2) for flexed revenue and variable cost, and type() is bool check instead of isinstance."},
    {"id": "proj-r38-mutants-all-rerun-count", "check": "Every project mutant (top level and subdirectory) is re-run this round",
     "location": "ledgers/AC4/mutants/*.py (157 top-level files, incl. r38e); ledgers/AC4/mutants/AC4-e-r23/ (6 files)",
     "status": "PASS",
     "evidence": "mutate_graders --unit AC4 --seeds 0-49 (out/mutate_ac4.out): 'mutate_graders AC4: PASS (153/153 killed)', exit 0, run before the four r38e files were added; those four were then run with runfiles.py (all KILLED except r38e_02 which is equivalent and moved to equivalent/). Subdirectory AC4-e-r23 fx23_01..06: 6/6 KILLED."},
    {"id": "proj-r38-lab-L04-output-line", "check": "L04 page output line for the new uneven-pool refusal matches the twin",
     "location": "course/modules/AC/AC4/L04.html line 321 and Remark 1.3 line 74; tests/labs/AC4/lab-AC4-L04-1.py",
     "status": "PASS",
     "evidence": "Twin run python -I -W error: exit 0; last line 'Uneven pool (100000 cents over 3 driver units): refused'. L04.html line 321 is that line and is the last line of the output block. exact_rate (lab lines 46-52) raises ValueError when cost % driver_total != 0, so 'raises an error' in Remark 1.3 is true of the lab's rate function. (L04 is outside slice e; checked because it is a cited dependency of the cards.)"},
    {"id": "proj-r38-exemplar-A-annotation-arithmetic", "check": "Exemplar A figures and annotation claims recomputed",
     "location": "course/modules/AC/AC4/project.html lines 331-340 (memo) and 345-351 (annotation)",
     "status": "PASS",
     "evidence": "Recomputed by hand and by the lab (see proj-calib-A-annotation). Efficiency -40,000 = 200 * (5,100 - 5,300); total 220,000 matches the memo's Result sentence only if the mix is negative, which the annotation says."},
    {"id": "proj-r38-banned-and-process-scan", "check": "No banned phrases or process words in the changed rubric, annotation and cards",
     "location": "course/modules/AC/AC4/project.html; course/modules/AC/AC4/cards.json", "status": "PASS",
     "evidence": "Regex scan for roughly, about N, historically, ellipsis, typically, usually, half of, and grep for builder/verifier/round in project.html: no matches; cards.json: no banned matches, 141 ids unique."},
]

rows = [r for r in rows if r["id"] not in {x["id"] for x in new_rows}] + new_rows
prev_ids = {r["id"] for r in prev["rows"]}
for rid, (st, loc, ev) in FRESH.items():
    if rid not in prev_ids:
        rows.append({"id": rid, "check": "Rubric C2 level 3 is at least as strict as level 2 (highest fully met level)", "location": loc, "status": st, "evidence": ev})
# the FAIL row for the C2 level 3 defect is new, not in the previous fragment
assert len({r["id"] for r in rows}) == len(rows)
for r in rows:
    if r["status"] != "PASS" and "fix" not in r:
        r["fix"] = ("Change the C2 level 3 cell (project.html line 315, column 3) to 'Each of the four variances tied to a case "
                    "figure.' so that level 3 cannot be met by a memo with no case figure; keep 'a named product or an input count' "
                    "only as a further condition in level 4 (already there). Re-run tests/test_memo_exemplars.py.")

n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
mut = list(prev["mutants"])
for name, killed in [
    ("ledgers/AC4/mutants/r38e_01_volume_variance_reported_as_magnitude.py", "test_single_product_has_no_mix_variance (seed 0)"),
    ("ledgers/AC4/mutants/r38e_03_master_budget_skips_unsold_products.py", "test_price_change_on_an_unsold_product_has_no_price_variance (seed 0)"),
    ("ledgers/AC4/mutants/r38e_04_efficiency_skips_unbudgeted_products.py", "test_product_with_no_budgeted_units (seed 0)"),
    ("ledgers/AC4/mutants/r38e_05_price_variance_against_standard_cost.py", "test_every_grader_seed_reconciles_exactly[30] (seed 0)"),
]:
    mut.append({"file": name, "description": "Round-38 student error: " + name.split("_", 2)[2].replace(".py", "").replace("_", " ") + ".", "killed_by": killed})

frag = {
    "unit": "AC4",
    "slice": "AC4-e",
    "round": 38,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 38, slice AC4-e; did not build AC4)",
    "pin": "81ff53b",
    "base": "5aeaaf0 (the latest AC4-e fragment on disk is round 35, pinned at 5aeaaf0; the round-37 fragment named in the brief is not present in /tmp/fanout-frags, so the delta was computed from 5aeaaf0)",
    "checkout": "/tmp/verify38-AC4-e",
    "scratch": "/tmp/ac4e38",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL" if n_fail else "PASS",
    "rows": rows,
    "mutants": mut,
    "registry_flags": prev.get("registry_flags", []),
    "freshness_flags": [],
    "notes": (
        "Delta 5aeaaf0..81ff53b for slice e: project.html lines 315, 317 (rubric C2 level 2, C4 levels 1-2) and 345 (exemplar A C2 annotation); cards.json AC4-c023 and AC4-c078 (only changed cards); L03.html lines 325 and 487 and L04.html lines 74 and 275-321 (lesson text, outside slice e, read where cited); tests/labs/AC4/lab-AC4-L04-1.py (lesson lab, output line added); ledgers/AC4/mutants (43 files, earlier rounds' mutants). grader/ unchanged. "
        "Not checked: (1) tools/build_site.py --check (in CLAUDE.md gates, outside this slice) was not re-run; (2) the Pyodide browser UI was not driven (page_smoke only); (3) the lab-twin mutants are out of scope by the architect ruling and were not run; (4) collection of the 563 checks was run on the reference solution in the run_graders workspace via ledgers/AC4/scripts/AC4-e-r38/collect_ws38.py, because a bare pytest on grader/ fails with 'No module named budget_engine' (run_cmds collect_ac4.out, exit 2, same as round 36); (5) the grader was run at seeds 0-49 for mutants and reference, but collection was checked on seeds 3, 29, 49 only; (6) SEC/EDGAR and external sources not in this slice. "
        "Equivalent mutant ledgers/AC4/scripts/AC4-e-r38/equivalent/r38e_02 has a proof row (proj-r38-equivalent-total-sum-of-parts). Rows marked 'Carried from round 35' keep their round-35 evidence: their cited subjects were checked against the delta above. Scripts: ledgers/AC4/scripts/AC4-e-r38/ (run_cmds.sh, make_r38e.py, make_r38e_b.py, make_alts38.py, select_rows.py, build_frag_r38.py, collect_ws38.py, runfiles.py, out/). "
        "Housekeeping: stale copies of round-36 scripts (make_r36e.py.old-r36-copy, write_frag_r36.py.old-r36-copy) remain in ledgers/AC4/scripts/AC4-e-r38/; the glob rm needed to delete them was refused by the safety check and was not forced. Also a first launch of run_cmds.sh used round-36 paths and failed harmlessly before the corrected run."
    ),
    "summary": {"rows": len(rows), "pass": n_pass, "fail": n_fail, "unverifiable": 0, "mutants": len(mut)},
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "pass", n_pass, "fail", n_fail, "mutants", len(mut), "verdict", frag["verdict"])
