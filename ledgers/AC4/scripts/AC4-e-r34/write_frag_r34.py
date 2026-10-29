"""Builds the round-34 AC4-e fragment from the round-30 fragment on disk, the round-34 command outputs and the mutant runs."""
import json, re, subprocess, sys, datetime, pathlib

ROOT = pathlib.Path(sys.argv[1])
S = ROOT / "ledgers/AC4/scripts/AC4-e-r34"
O = S / "out"
prev = json.load(open("/tmp/fanout-frags/AC4-e.round33.json"))
PREFIX = ("Carried from round 33 (files byte-identical since the previous pin; project.html lines cited and cards.json "
          "objects cited unchanged since 5aeaaf0; the file AC4-e.round33.json records round 30 and pin 5aeaaf0): ")

reverify = {
 "proj-rubric-observability": ("PASS",
   "Round 34 re-verified: the two residual descriptors are gone. C2 level 2 (project.html line 315) now reads 'At least two variances tied to a case figure, and no more than one variance with no case figure, named product or input count', a count a reader can apply. C4 level 1 (line 317) now reads 'No recommendation, or a recommendation that names no action for any unfavourable variance it discusses'. The C4 level 1/2 overlap (a memo with no action and an observation fits both) is resolved by the scoring rule on line 308: 'A memo that recommends no action for any unfavourable variance scores 1 on C4'."),
 "proj-rubric-C2-terms": ("PASS",
   "Re-verified round 34: the C2 level 2 and level 3 cells (project.html line 315) use only the terms defined on line 308 (tied to a case figure, named product, input count)."),
 "proj-rubric-exhaustive": ("PASS",
   "Re-verified round 34: the rubric table (project.html lines 313-319) has five criteria C1-C5, each with four cells; the C2 and C4 cells changed on lines 315 and 317 and still fill all four levels."),
 "proj-calib-A-annotation": ("FAIL",
   "Re-verified round 34: the C2 line (project.html line 345) says the mix variance is 'tied to the computed shift of +462,857 cents shown in the memo'. Lab 1 computes the sales mix variance as -462,857 (project.html line 142 and line 238: 'step 6 sales mix variance (cents): -462857'). The memo's +462,857 has the wrong sign, and the annotation calls it the computed shift, which it is not. The C2 level 2 score is unaffected because volume and price already give two tied variances. The other annotation lines (C1, C2 level 3, C3, C4, C5) were re-read and match the memo text on lines 330-340."),
 "proj-card-c023": ("PASS",
   "Re-verified round 34 (the round-33 FAIL is resolved): cards.json AC4-c023 back now reads 'R_BE = pQ* = F/(m/p), where m/p is the contribution margin ratio, with m > 0 (Proposition 2.2).' L02.html line 71 states 'Let m > 0' before the same formula, so the hypothesis is stated."),
 "proj-r30-rubric-observability": ("PASS", "Re-verified round 34: the round-33 FAIL is resolved (see proj-rubric-observability)."),
 "proj-r30-card-c023-hypothesis": ("PASS", "Re-verified round 34: the round-33 FAIL is resolved (see proj-card-c023): cards.json AC4-c023 now states 'with m > 0' before the formula, matching L02.html line 71."),
 "proj-card-c078": ("PASS",
   "Re-verified round 34 (the round-33 FAIL is resolved): cards.json AC4-c078 back now reads 'with a budget that has budgeted units (Q_b > 0), for any actual units, actual selling prices and actual kilograms, provided the actual material price equals the standard price pi'. L06.html line 79 states 'with Q_b > 0 and the actual material price equal to pi' and 'for any actual units, actual selling prices and actual kilograms'. Card grade T matches Proposition 2.1 on the page."),
 "proj-cards-structure": ("FAIL",
   "Re-verified round 34: cards.json holds 141 card objects with 141 unique ids (54 graded T, 52 graded C, 35 with no grade field); the same count is at 5aeaaf0 (git show). The round-33 row's '134 cards' is a wrong count."),
 "proj-r17-cards-counts": ("FAIL",
   "Re-verified round 34: the subject states 'cards.json: 134 cards'. The file has 141 card objects at both 5aeaaf0 and 455dd92, so the count in this row is wrong. The round-17 changed-set claim (10 changed and 3 added) was not re-derived this round."),
 "proj-r15-grader-count-527": ("PASS",
   "Re-verified round 34 under the current wording: project.html line 265 says the grader 'collects 563 checks on every seed'; the collect-only count of the reference workspace is 563 (ledgers/AC4/scripts/AC4-e-r34/out/collect_ws.out). The earlier 527 in this row's subject is no longer on the page."),
 "proj-collect-count": ("PASS",
   "Re-verified round 34: project.html line 265 says 563 checks; the reference workspace collects 563 tests (ledgers/AC4/scripts/AC4-e-r34/collect_ws.py run on grader/reference.py, output in out/collect_ws.out). The raw pytest collect in the checkout fails with ModuleNotFoundError budget_engine because the grader imports the learner module; run_graders builds the workspace and passes."),
 "proj-r12-count-matches-page": ("PASS",
   "Re-verified round 34: 563 on the page equals the 563 collected in the reference workspace."),
 "proj-banned-phrases": ("PASS",
   "Re-verified round 34: grep of the changed lines (project.html 315, 317, 345; cards.json AC4-c023 and AC4-c078 objects) for roughly, about N, historically, typically, usually, ellipsis, verifier, builder: no hits; the card scan over all 141 objects also has no hits."),
 "proj-autograder-rerun-mutants-m01-m37": ("PASS",
   "Re-run round 34: mutate_graders --unit AC4 --seeds 0-49 reports 147/147 killed (ledgers/AC4/scripts/AC4-e-r34/out/mutate_ac4.out), covering every top-level mutant in ledgers/AC4/mutants present at that time; the three round-34 mutants were run separately and killed (see proj-r34-mutants-new-student-errors)."),
 "proj-r14-mutants-all-rerun": ("PASS",
   "Re-run round 34 on seeds 0-49: 147/147 top-level mutants killed (mutate_ac4.out). Lab-twin subdirectory mutants out of scope per the architect ruling."),
 "proj-r15-mutants-all-rerun": ("PASS",
   "Re-run round 34 on seeds 0-49: 147/147 top-level mutants killed, plus 3 new round-34 mutants killed (the file count now 150). Lab-twin subdirectory mutants out of scope."),
 "proj-check-pages": ("PASS", "Re-run round 34: 'check_pages AC4: PASS' exit 0 (ledgers/AC4/scripts/AC4-e-r34/out/check_pages.out)."),
 "proj-check-dag": ("PASS", "Re-run round 34: 'check_dag AC4: PASS' exit 0 (out/check_dag.out)."),
 "proj-check-projects": ("PASS", "Re-run round 34: 'check_projects AC4: PASS' exit 0 (out/check_projects.out)."),
 "proj-page-smoke": ("PASS", "Re-run round 34: 'page_smoke AC4: PASS' exit 0 for project.html (out/page_smoke_project.out)."),
 "proj-ruff-mypy": ("PASS", "Re-run round 34: ruff check 'All checks passed!' exit 0; ruff format '220 files already formatted' exit 0; mypy --no-incremental 'Success: no issues found in 153 source files' exit 0."),
 "proj-run-labs-ac4": ("PASS", "Re-run round 34: 'run_labs AC4: PASS (10/10)' exit 0 (out/run_labs.out)."),
 "proj-run-graders-ac4": ("PASS", "Re-run round 34: 'run_graders AC4: PASS (reference 50/50 seeds, slowest 0.3 s)' exit 0 (out/run_graders.out)."),
 "proj-r13-verify-refs": ("PASS", "Re-run round 34: verify_refs --unit AC4 'live re-verification of AC4: 2 of 560 entries, 0 problems' exit 0; --offline 'offline integrity: 560 entries, 0 problems' exit 0."),
 "proj-citations-reading": ("PASS", "Re-run round 34: the same verify_refs runs above; the reading-list keys resolve (0 problems)."),
}

new_rows = [
 {"id": "proj-r34-delta-scope", "check": "Round-34 source delta since 5aeaaf0 is confined to four files and touches only the lines named in this slice",
  "location": "git diff 5aeaaf0 455dd92 -- course tests tools references plans atlas curriculum notation benchmarks",
  "status": "PASS",
  "evidence": "4 files, 8 insertions and 8 deletions: project.html lines 315, 317, 345 (C2 and C4 rubric cells, the exemplar A C2 line); cards.json AC4-c023 and AC4-c078 back; L03.html lines 328 and 490 (out of slice, checked below); L04.html line 74 (out of slice, checked below). The grader, tests/labs, instance.py and the mutant set's top-level files are byte-identical."},
 {"id": "proj-r34-rubric-C4-level-overlap", "check": "C4 level 1 and level 2 do not both fit a memo with no action and an observation", "location": "course/modules/AC/AC4/project.html line 308 (scoring rule) and line 317 (C4 row)", "status": "PASS",
  "evidence": "Line 308 states 'A memo that recommends no action for any unfavourable variance scores 1 on C4, whatever else it says', and the C4 level 1 cell (line 317) matches that sentence."},
 {"id": "proj-r34-exemplar-B-unchanged", "check": "Exemplar B passages, scores and annotations are byte-identical since 5aeaaf0", "location": "course/modules/AC/AC4/project.html lines 357-382", "status": "PASS",
  "evidence": "Not among the changed lines (diff hunks at 312, 342 only). Carried from the round-33 rows proj-calib-B-scores, proj-calib-B-annotation, proj-exemplar-B-consequences, proj-exemplar-B-threshold and proj-exemplar-B-verdict, whose subjects are unchanged."},
 {"id": "proj-r34-L03-second-line", "check": "L03 interpretation: the 9.10 avoidable make cost is printed on the second line of Lab 1 (out of slice, checked for the cards and the Lab 1 citation)",
  "location": "course/modules/AC/AC4/L03.html line 328; tests/labs/AC4/lab-AC4-L03-1.py output", "status": "PASS",
  "evidence": "Run round 34: out/twin_l03.out line 1 'Part K, make or buy: 20,000 units a year (SIMULATED)', line 2 'avoidable make cost per unit (variable + dedicated fixed / units): 9.10'. The statement 'second line of Lab 1's output, after its title' is right."},
 {"id": "proj-r34-L03-R2-arithmetic", "check": "L03 R2 solution: break-even other-use contribution is 14,000 and both costs are 196,000 at it", "location": "course/modules/AC/AC4/L03.html line 490 (R2 solution)", "status": "PASS",
  "evidence": "Recomputed: 182,000 + 40,000 = 222,000; 210,000 - 40,000 = 170,000; difference 52,000. 182,000 + X < 210,000 - X iff 2X < 28,000 iff X < 14,000. At X = 14,000 both are 196,000. The added sentence 'Let X be the contribution of the other use, so X = 40,000 here' is consistent."},
 {"id": "proj-r34-L04-remark-1-3", "check": "L04 Remark 1.3: Lab 1's rate function raises an error for an inexact division and the printed run does not reach that case (out of slice)",
  "location": "course/modules/AC/AC4/L04.html line 74; tests/labs/AC4/lab-AC4-L04-1.py lines 47-51", "status": "PASS",
  "evidence": "Lab code line 51 raises ValueError 'does not divide evenly by driver units'. Run round 34: out/twin_l04.out ends 'allocated total: 100,000.00, equals pool: True' and 'exit 0' with no ValueError, so the printed run does not reach that case."},
 {"id": "proj-r34-mutants-new-student-errors", "check": "Three new student-error mutants written this round are each killed on seeds 0-49", "location": "ledgers/AC4/mutants/r34e_01_mix_measured_against_master_profit.py; r34e_02_flexed_variable_cost_truncated_revenue_rounded.py; r34e_03_efficiency_divided_by_actual_units.py", "status": "PASS",
  "evidence": "Written by ledgers/AC4/scripts/AC4-e-r34/make_r34e.py; killed by runfiles.py (out not separately saved; output in this row): r34e_01 killed by test_every_grader_seed_reconciles_exactly[30] (seed 0); r34e_02 by test_every_grader_seed_reconciles_exactly[4] (seed 0); r34e_03 by test_every_grader_seed_reconciles_exactly[29] (seed 0). Each is a plausible student error: the mix against the master profit, a truncated variable cost, an efficiency per unit."},
 {"id": "proj-r34-alternatives-correct", "check": "Three further correct implementations pass the whole suite on seeds 0-49 (over-constraint test)", "location": "ledgers/AC4/scripts/AC4-e-r34/alts/alt34_a_divmod_half_up.py; alt34_b_mix_derived_from_total.py; alt34_c_floor_half_fraction.py", "status": "PASS",
  "evidence": "runfiles.py seeds 0-49: alt34_a (integer divmod half-up for revenue and variable cost) 50/50; alt34_b (sales mix derived as total less the other three, an exact identity by algebra) 50/50; alt34_c (math.floor(x + 1/2) on Fraction) 50/50. Each is a valid algorithm that the page's half-up rule permits."},
 {"id": "proj-r34-collect-reference-count", "check": "Collect-only count of the reference workspace equals the page's 563", "location": "ledgers/AC4/scripts/AC4-e-r34/collect_ws.py; out/collect_ws.out", "status": "PASS",
  "evidence": "'563 tests collected' rc 0 with -W error. The raw pytest collect in the checkout (out/collect_ac4.out) errors on ModuleNotFoundError budget_engine, expected because the grader imports the learner module, which the workspace supplies."},
 {"id": "proj-r34-check-cards-numbers", "check": "The changed cards' numbers appear in their lessons", "location": "course/modules/AC/AC4/cards.json AC4-c023, AC4-c078", "status": "PASS",
  "evidence": "The only numbers in the new text are 2.1, 2.2 and 0 (in m > 0 and Q_b > 0); L02.html line 71 has 'm > 0' and L06.html line 79 has 'Q_b > 0'."},
]

mutant_rows = []
line_re = re.compile(r"^KILLED (\S+?\.py): (.*) -> (.*)$")
for ln in (O / "mutate_ac4.out").read_text(encoding="utf-8").splitlines():
    m = line_re.match(ln)
    if m:
        mutant_rows.append({"file": f"ledgers/AC4/mutants/{m.group(1)}", "description": m.group(2), "killed_by": m.group(3)})
new_mutant_kills = {
 "r34e_01_mix_measured_against_master_profit.py": ("Sales mix variance is the actual mix contribution less the master budget profit, so the volume effect is counted again inside the mix.", "test_every_grader_seed_reconciles_exactly[30] (seed 0)"),
 "r34e_02_flexed_variable_cost_truncated_revenue_rounded.py": ("Flexed variable cost is truncated toward zero while flexed revenue is rounded half up to the whole cent.", "test_every_grader_seed_reconciles_exactly[4] (seed 0)"),
 "r34e_03_efficiency_divided_by_actual_units.py": ("Efficiency variance is divided by the actual total units, giving a per-unit figure in place of cents.", "test_every_grader_seed_reconciles_exactly[29] (seed 0)"),
}
for name, (desc, killed) in new_mutant_kills.items():
    mutant_rows.append({"file": f"ledgers/AC4/mutants/{name}", "description": desc, "killed_by": killed})

rows = []
prev_ids = set()
for r in prev["rows"]:
    prev_ids.add(r["id"])
    if r["id"] in reverify:
        st, ev = reverify[r["id"]]
        row = {"id": r["id"], "check": r["check"], "location": r["location"], "status": st, "evidence": ev}
    elif r["status"] == "PASS":
        row = {"id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": PREFIX + r["evidence"]}
    else:
        row = {"id": r["id"], "check": r["check"], "location": r["location"], "status": "FAIL", "evidence": r["evidence"]}
    if row["status"] != "PASS":
        row["fix"] = {
          "proj-calib-A-annotation": "Replace 'the computed shift of +462,857 cents shown in the memo' with 'the magnitude of the computed mix shift (462,857 cents), which the memo gives the wrong sign'. Lab 1 computes -462,857 (project.html line 142).",
          "proj-cards-structure": "Correct the count in this row to 141 (the file is unchanged in count since 5aeaaf0); no page or card change needed.",
          "proj-r17-cards-counts": "Restate the count as 141 cards and re-derive the round-17 changed set from git history if that claim is to stand.",
        }.get(row["id"], "Correct the row to the observed evidence.")
    rows.append(row)
for r in new_rows:
    rows.append(r)

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert prev_ids <= set(ids), "a previous id was dropped"

counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
          "fail": sum(r["status"] == "FAIL" for r in rows),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows), "mutants": len(mutant_rows)}
frag = {
  "unit": "AC4", "slice": "AC4-e", "round": 34,
  "verifier": "Claude Haiku 5.5 (independent verifier, round 34, slice AC4-e; did not build AC4)",
  "pin": "455dd92",
  "base": "5aeaaf0 (the pin the previous fragment on disk records; that file is named round33 but its content is round 30, pin 5aeaaf0; the delta was computed from 5aeaaf0)",
  "checkout": str(ROOT), "scratch": "/tmp/ac4e34",
  "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
  "verdict": "FAIL" if counts["fail"] else "PASS",
  "rows": rows, "mutants": mutant_rows,
  "registry_flags": prev["registry_flags"],
  "freshness_flags": [],
  "notes": ("Not checked: (1) the Pyodide browser UI, the self-assessment JavaScript and the reveal of annotations were not driven; page_smoke and source reading only. "
            "(2) The lab-twin mutants in the AC4-a/b/c/d subdirectories of ledgers/AC4/mutants are out of scope per the architect ruling and were not run through the grader. "
            "(3) build_site --check was not run this round (no site-data input changed in the delta). "
            "(4) Hours rows carried: the hours table lines are unchanged; no pace estimate was failed. "
            "(5) Carried rows are carried only where the cited lines/objects are byte-identical; the round-33 file's rows were not trusted as PASS on their own. "
            "(6) The L03 and L04 lesson changes were checked only for the citations they make to Lab 1 (out of slice). "
            "(7) Exemplar A and B annotations were scored against the rubric text by reasoning; no machine test exists."),
  "summary": counts,
}
out = ROOT / "ledgers/AC4/AC4-e.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1), encoding="utf-8")
print(counts, frag["verdict"])
