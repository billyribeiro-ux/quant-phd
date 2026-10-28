import json, re, pathlib
R = pathlib.Path("/tmp/verify14-AC4-e")
O = R / "ledgers/AC4/scripts/AC4-e-r14/out"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round13.json"))
CARRY = ("Carried from round 13 (cited subject byte-identical since eaf6d87; the only lines changed in this delta are "
         "project.html line 260, cards.json AC4-c073 and test_project.py line 445): ")
RE = {  # rows re-verified this round: id -> (status, evidence)
 "proj-autograder-rerun-mutants-m01-m37": ("PASS", "Re-run this round: tools/mutate_graders.py --unit AC4 --seeds 0-49 printed 'mutate_graders AC4: PASS (103/103 killed)' (out/mutate_graders_r14_seeds0-49.out); the four new r14e mutants were run with the same workspace/run_suite code on seeds 0-49 and all four are KILLED (see proj-r14-mutants-new-student-errors). 107 mutant files in ledgers/AC4/mutants."),
 "proj-mutant-descriptions": ("PASS", "Re-run: out/checks_r14.out 'mutants checked: 107 without a description: []'. Every file's first docstring line names the student error."),
 "proj-mutant-m07-empty-name": ("PASS", "Re-run inside the 103/103 kill run (out/mutate_graders_r14_seeds0-49.out); m07 unchanged and killed."),
 "proj-mutant-m12-duplicate-names": ("PASS", "Re-run inside the 103/103 kill run (out/mutate_graders_r14_seeds0-49.out); m12 unchanged and killed."),
 "proj-autograder-reference": ("PASS", "Re-run: out/run_graders.out 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)'. test_project.py changed only at line 445 (a comment), so the reference still passes."),
 "proj-collect-count": ("PASS", "Re-run: pytest --collect-only on the reference workspace prints '461 tests collected'; project.html line 265 states 461 checks on every seed."),
 "proj-autograder-alternatives": ("PASS", "Re-run this round on seeds 0-49 (runfiles, ledgers/AC4/scripts/AC4-e-r14): alt13_a, alt13_b, alt_r12_a..e and alt14_a, alt14_b all PASS 50/50. No alternative fails a sentence of the page."),
 "proj-autograder-alt-decimal": ("PASS", "Re-run: ledgers/AC4/scripts/AC4-e-r13/alts/alt_r12_a_decimal_half_up.py (copied to the r12 set) PASS 50/50 seeds on the current test_project.py."),
 "proj-r12-alternatives-new": ("PASS", "Re-run this round: alt_r12_a_decimal_half_up, alt_r12_b_fraction_floor_strip, alt_r12_c_total_from_actual, alt_r12_d_loop_totals, alt_r12_e_compare_rounding each PASS 50/50 seeds."),
 "proj-r13-alternatives-new": ("PASS", "Re-run this round: alt13_a_integer_divmod.py PASS 50/50; alt13_b_fraction_floor.py PASS 50/50."),
 "proj-cards-structure": ("PASS", "Re-run: python scan of cards.json gives 131 cards, 131 unique ids, fields back/front/id/lesson present on each card."),
 "proj-cards-duplicates": ("PASS", "Re-run: no duplicate front and no duplicate back among the 131 cards (python Counter scan)."),
 "proj-check-pages": ("PASS", "Re-run: out/check_pages.out 'check_pages AC4: PASS'."),
 "proj-check-dag": ("PASS", "Re-run: out/check_dag.out 'check_dag AC4: PASS' (and CF1, AP1 PASS)."),
 "proj-check-projects": ("PASS", "Re-run: out/check_projects.out 'check_projects AC4: PASS'."),
 "proj-page-smoke": ("PASS", "Re-run: out/page_smoke_ac4.out, 'page_smoke AC4: PASS', rc=0 (Pyodide/Chromium smoke over the AC4 pages, project included; project.html changed only at line 260 text)."),
 "proj-run-labs-ac4": ("PASS", "Re-run: out/run_labs.out 'run_labs AC4: PASS (10/10)'. tests/labs/AC4 is byte-identical to eaf6d87 (not in the delta)."),
 "proj-run-graders-ac4": ("PASS", "Re-run: out/run_graders.out 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)', rc=0."),
 "proj-ruff-mypy": ("PASS", "Re-run: ruff check and ruff format --check on grader and tests/labs/AC4 pass (out/ruff.out, 'already formatted', rc=0); repository mypy --no-incremental 'Success: no issues found in 153 source files' (out/mypy_repo.out, rc=0). Running mypy on the grader directory alone reports budget_engine import-not-found, which is expected because the grader is copied next to budget_engine.py at run time (out/mypy.out); the repository run is the gate."),
 "proj-r13-verify-refs": ("PASS", "Re-run: out/verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc=0; out/verify_refs_live_ac4.out 'live re-verification of AC4: 2 of 560 entries, 0 problems' rc=0. references/references.json unchanged in this delta."),
 "proj-banned-phrases": ("PASS", "Re-run: the changed project.html line 260 (497 characters of text) contains none of roughly/about /historically/usually/typically/half of/ellipsis (grep count 0); line 265 and 306 unchanged. Cards: c073 back contains none of these phrases."),
 "proj-conventions-no-spending-claim": ("PASS", "Re-read project.html line 260: 'The case holds the input price and the fixed overhead at budget, so the engine has no input price variance and no fixed overhead variance; the stretch section asks you to add them.' variance_decomposition returns only sales_price, sales_volume, sales_mix, efficiency and total (checked by type listing), and line 398 asks for the input price and fixed overhead variances."),
 "proj-inputs-every-number-int": ("PASS", "Re-run: variance_decomposition on a sample case returns int for every key (sales_price, sales_volume, sales_mix, efficiency, total); line 260 sentence 'every number it returns is an int' matches."),
 "proj-r13-spec-mix-sentence": ("PASS", "Re-read project.html line 260 (changed this delta): 'The sales mix variance uses the whole-cent flexed profit, so it differs from the mix variance computed with the exact, unrounded flexed profit by less than one cent.' The comparison is now between two mix variances, which is the quantity the grader checks (test_mix_is_within_one_cent_of_the_exact_fraction, oracle exact_mix). Re-derived: flexed revenue and flexed variable cost each move by a value in (-1/2, 1/2] cent (halves up, _nearest_cent), so the mix error equals minus (revenue move minus variable-cost move), which lies in (-1, 1). Random check of 20000 cases (out/mix_bound_random.out, scripts/AC4-e-r14/mixcheck.py): max |mix - exact mix| = 0.98333 < 1."),
 "proj-r13-mix-tolerance-test": ("PASS", "Re-read test_project.py lines 443-450 (test_mix_is_within_one_cent_of_the_exact_fraction, seeds 0-49, assertion '< 1'). The assertion is right (see proj-r13-spec-mix-sentence); the comment on line 445 is handled in proj-r13-grader-mix-comment."),
 "proj-grader-comments": ("FAIL", "The comment on test_project.py line 445 was corrected this delta: it now says 'at most half a cent' (true; the first clause that round 13 flagged is fixed). Its second clause, 'so their difference is less than one cent', does not follow from 'at most half a cent' (that gives a difference of at most one). Strictness needs the halves-up rule. Same defect as proj-r13-grader-mix-comment. All other grader comments are carried in their rows and unchanged."),
 "proj-r13-grader-mix-comment": ("FAIL", "test_project.py line 445 now reads: 'Each rounding moves a flexed amount by at most half a cent, so their difference is less than one cent.' The first clause is true (the halves-up rule gives moves in (-1/2, 1/2]). The inference is not: 'at most half' gives |difference| <= 1, and strictness (<1) holds only because a move of exactly -1/2 never occurs (halves round up, so the only exact-half move is +1/2). Fix the comment to: 'Each rounding moves a flexed amount by at most half a cent, and an exact half cent always moves up, so the two moves cannot differ by a full cent.' The assertion is unchanged and correct."),
 "proj-cards-changed-lessons": ("PASS", "Re-verified: AC4-c073 (L06) now matches L06.html line 98 (Proposition 2.2(c), sum of kilograms; the counterexample of 50 kg above and 50 kg below giving E = 0). The L05 and L06 cards not changed in this delta are carried (cards.json objects byte-identical; AC4-c061, c078 and the round-12 sample re-checked in earlier rounds)."),
 "proj-r13-card-c073-scope": ("PASS", "Re-verified against L06.html line 98 and Definition 1.2 (line 64-72): card back 'Total kilograms used above the total standard allowance for the actual output make E negative (Definition 1.2; Proposition 2.2(c)).' matches (c): E negative when sum kg > sum s q, which is a sufficient condition as the card states. 'An excess on one product that is offset by a shortfall on another leaves the sum, and so E, at zero' matches the lesson's 50 kg / 50 kg counterexample (E = 0 with no product on its allowance). Definition in card: E = -pi x sum (kg - s q) matches Definition 1.2 with pi the standard price per kilogram."),
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RE:
        st, ev = RE[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
    else:
        assert r["status"] == "PASS", rid
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": CARRY + r["evidence"]})
rows.append({"id": "proj-r14-mutants-new-student-errors", "check": "Four new student-error mutants written this round are each killed by the suite on seeds 0-49",
  "location": "ledgers/AC4/mutants/r14e_01_fixed_overhead_scales_with_volume.py; r14e_02_efficiency_standard_on_budget_units.py; r14e_03_price_variance_on_budget_units.py; r14e_04_flexed_revenue_halves_down.py",
  "status": "PASS", "evidence": "Run via scripts/AC4-e-r14/runfiles.py (same workspace and run_suite as mutate_graders): r14e_01 KILLED by test_every_grader_seed_reconciles_exactly[26] (seed 0); r14e_02 KILLED by test_every_grader_seed_reconciles_exactly[26] (seed 0); r14e_03 KILLED by test_every_grader_seed_reconciles_exactly[26] (seed 0); r14e_04 KILLED by test_flexed_zero_units_leaves_only_fixed_overhead (seed 0). Each is a plausible learner error the page describes: flexed fixed overhead scaled with volume (the page says fixed overhead is held at budget and profit = rounded revenue less rounded variable cost less F); efficiency on budgeted units (page: efficiency is s times sum of q times AU less AQ); price variance on budgeted units (page: sum of (ap minus bp) times AU); flexed revenue rounded half down (page: each amount to the nearest whole cent, halves up)."})
rows.append({"id": "proj-r14-alternatives-correct", "check": "Two further spec-correct alternatives pass the whole suite on seeds 0-49 (over-constraint check)",
  "location": "ledgers/AC4/scripts/AC4-e-r14/alts/alt14_a_mix_as_residual.py; alt14_b_divmod_nearest.py",
  "status": "PASS", "evidence": "alt14_a computes the sales mix as the residual (actual profit less master profit, minus sales price, sales volume and efficiency). This is an exact identity of the page's definitions (the sum of the four variances equals the total with no residual, page line 257-258 and Proposition 2.1 analogue), so it is a correct implementation; it PASSes 50/50 seeds. alt14_b rounds with q, r = divmod(numerator, denominator) and q + (2r >= denominator), halves up, and PASSes 50/50 seeds. Neither has a numerical cutoff, so no different-cutoff variant is needed for this unit."})
rows.append({"id": "proj-r14-mix-rounding-bound", "check": "The mix error is strictly less than one cent (proof and random check)",
  "location": "course/modules/AC/AC4/project.html line 260; grader/reference.py _nearest_cent and variance_decomposition",
  "status": "PASS", "evidence": "Proof: _nearest_cent rounds x.5 up, so a flexed move is +1/2 or in (-1/2, 1/2). Mix error = -(revenue move - variable move) in (-1, 1). Random check on 20000 cases (ledgers/AC4/scripts/AC4-e-r14/mixcheck.py, out/mix_bound_random.out): max |mix - exact mix| = 0.9833 (strict)."})
rows.append({"id": "proj-r14-mutants-all-rerun", "check": "Every committed mutant is re-run on seeds 0-49 by the current grader",
  "location": "ledgers/AC4/mutants (107 .py files)", "status": "PASS",
  "evidence": "out/mutate_graders_r14_seeds0-49.out: 103/103 KILLED (the 103 files present when the run started), plus the four r14e files KILLED above (107/107). Every mutant has a docstring that names the error (proj-mutant-descriptions)."})
mut_lines = (O / "mutate_graders_r14_seeds0-49.out").read_text().splitlines()
mutants = []
for ln in mut_lines:
    m = re.match(r"KILLED (\S+)\.py: (.*?) -> (.*)$", ln)
    if m:
        mutants.append({"id": m.group(1), "file": f"ledgers/AC4/mutants/{m.group(1)}.py", "description": m.group(2), "killed_by": m.group(3)})
new = {
 "r14e_01_fixed_overhead_scales_with_volume": ("Student error: the flexed budget scales the fixed overhead with the actual volume, so the flexed profit subtracts a volume-proportional share of the fixed overhead.", "test_every_grader_seed_reconciles_exactly[26] (seed 0)"),
 "r14e_02_efficiency_standard_on_budget_units": ("Student error: the efficiency variance takes the standard input allowance on the budgeted units instead of the actual units.", "test_every_grader_seed_reconciles_exactly[26] (seed 0)"),
 "r14e_03_price_variance_on_budget_units": ("Student error: the sales price variance multiplies each price difference by the budgeted units instead of the actual units.", "test_every_grader_seed_reconciles_exactly[26] (seed 0)"),
 "r14e_04_flexed_revenue_halves_down": ("Student error: the flexed revenue rounds exact half cents down, not up, so a flexed amount that ends in one half is taken to the lower cent.", "test_flexed_zero_units_leaves_only_fixed_overhead (seed 0)"),
}
for k, (d, kb) in new.items():
    mutants.append({"id": k, "file": f"ledgers/AC4/mutants/{k}.py", "description": d, "killed_by": kb})
assert len(mutants) == 107, len(mutants)
nonpass = [r["id"] for r in rows if r["status"] != "PASS"]
verdict = "FAIL" if nonpass else "PASS"
frag = {
 "unit": "AC4", "slice": "AC4-e", "round": 14,
 "verifier": "Claude Haiku 5.5 (independent verifier, round 14, slice AC4-e; did not build AC4)",
 "pin": "cef676e", "base": "eaf6d87 (round-13 pin; previous fragment /tmp/fanout-frags/AC4-e.round13.json used as context only)",
 "checkout": "/tmp/verify14-AC4-e", "scratch": "/tmp/ac4-v/e14",
 "verified_at": "2026-10-28T22:00:00+00:00", "verdict": verdict,
 "rows": rows, "mutants": mutants,
 "registry_flags": [], "freshness_flags": [],
 "notes": ("Delta eaf6d87..cef676e for this slice: project.html line 260 (Conventions sentence on the sales mix variance) only; "
           "cards.json AC4-c073 back only; grader/test_project.py line 445 comment only (test_mix_is_within_one_cent_of_the_exact_fraction, assertion unchanged); "
           "mutants fx13_* (10 files) and this round's r14e_* (4 files). reference.py, instance.py, starter.py, tests/labs/AC4, lesson pages, index.html, references.json are byte-identical. "
           "Not checked: the live verify_refs run is the only network call and it passed; no browser screenshot beyond page_smoke; the 51 non-function Lab 2 twin outputs were not re-derived (labs byte-identical, run_labs PASS)."),
 "summary": {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": len(nonpass), "unverifiable": 0,
             "mutants_killed": len(mutants), "mutants": len(mutants)},
}
out = R / "ledgers/AC4/AC4-e.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n")
json.dump(frag, open("/tmp/fanout-frags/AC4-e.round14.json", "w"), indent=2, ensure_ascii=False)
print("rows", len(rows), "nonpass", nonpass, "mutants", len(mutants), "verdict", verdict)
