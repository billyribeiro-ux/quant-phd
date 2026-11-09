"""Build ledgers/PC3/PC3-c.json (round 14, slice c) from the round-13 rows, the carry test and this round's outputs.

Rows that cite no changed line are carried (status PASS, prefixed). Every other row, and every new row, carries the
evidence of this round's own run, with the output file that shows it. Run from the checkout root.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "ledgers/PC3/scripts/PC3-c-r14/out"
R13 = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-c.round13.json"))
PLAN = json.load(open(OUT / "carry_plan.json"))
S = "ledgers/PC3/scripts/PC3-c-r14/"


def out(name):
    return (OUT / name).read_text(encoding="utf-8")


# ---- mutants (this round's run of tools/mutate_graders.py --unit PC3 --seeds 0-49) ----
mut_rows = {}
for line in out("mutate_PC3_0-49_all_r14.out").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed.strip() == "None" else killed.strip()
    desc = re.sub(r"^Student error: ", "", desc).strip()
    mut_rows[name] = {"id": name, "description": desc, "killed_by": killed_by}
mut_list = [mut_rows[k] for k in sorted(mut_rows)]
assert len(mut_list) == 70, len(mut_list)
survivors = [m["id"] for m in mut_list if m["killed_by"] is None]
assert survivors == sorted(["r14_01_replay_rounds_fill_prices_to_the_dime.py",
                            "r14_03_quote_locks_the_market_at_the_limit_mid_game.py",
                            "s14_01_quote_prints_on_turn_thirteen_at_inventory_seven.py",
                            "s14_02_replay_refuses_a_fill_off_the_dime_grid.py"]), survivors


def group(prefixes):
    names = [m["id"] for m in mut_list if any(m["id"].startswith(p) for p in prefixes)]
    dead = [m for m in mut_list if m["id"] in names and m["killed_by"]]
    return names, len(dead)


def mut_evidence(prefixes, label):
    names, dead = group(prefixes)
    return (f"Re-run this round: tools/mutate_graders.py --unit PC3 --seeds 0-49 "
            f"(ledgers/PC3/scripts/PC3-c-r14/out/mutate_PC3_0-49_all_r14.out): {label} {dead} of {len(names)} KILLED "
            f"({', '.join(names)}).")


def surv_evidence(name, label):
    m = mut_rows[name]
    assert m["killed_by"] is None, name
    return (f"Re-run this round: tools/mutate_graders.py --unit PC3 --seeds 0-49 "
            f"(out/mutate_PC3_0-49_all_r14.out): {label} SURVIVED (no test killed it on seeds 0-49).")


# ---- rows ----
R = {}  # id -> (status, location, check, evidence, fix)
r13 = {r["id"]: r for r in R13["rows"]}


def fresh(rid, status, location, evidence, fix=None, check=None):
    R[rid] = dict(status=status, location=location, check=check or r13.get(rid, {}).get("check", "2.6"),
                  evidence=evidence, fix=fix)


CMD = "tools/{tool} --unit PC3 ... this round (output: ledgers/PC3/scripts/PC3-c-r14/out/{out})"

# gate commands, this round
fresh("proj-check-tools", "PASS", "tools/check_pages.py --unit PC3; tools/check_dag.py --unit PC3; tools/check_projects.py --unit PC3",
      "Re-run this round: " + out("check_pages.out").strip().splitlines()[-2] + "; " + out("check_dag.out").strip().splitlines()[-2]
      + "; " + out("check_projects.out").strip().splitlines()[-2] + " (out/check_pages.out, check_dag.out, check_projects.out).")
fresh("proj-r8-check-tools", "PASS", "tools/check_pages.py --unit PC3; tools/check_dag.py --unit PC3; tools/check_projects.py --unit PC3",
      "Same run as proj-check-tools (out/check_pages.out, out/check_dag.out, out/check_projects.out): all three PASS, exit 0.")
fresh("proj-run-labs-unit", "PASS", "tools/run_labs.py --unit PC3 --page project",
      "Re-run this round: '" + out("run_labs_project.out").strip().splitlines()[-2] + "' (out/run_labs_project.out).")
fresh("proj-r8-run-labs-page-smoke", "PASS", "tools/run_labs.py --unit PC3 --page project; tools/run_graders.py --unit PC3 --seeds 0-49; tools/page_smoke.py --unit PC3 --pages project.html",
      "Re-run this round: run_labs '" + out("run_labs_project.out").strip().splitlines()[-2] + "'; run_graders '"
      + out("run_graders.out").strip().splitlines()[-2] + "'; page_smoke '" + out("page_smoke_project.out").strip().splitlines()[-2]
      + "' (out/*.out).")
fresh("proj-page-smoke", "PASS", "tools/page_smoke.py --unit PC3 --pages project.html",
      "Re-run this round: '" + out("page_smoke_project.out").strip().splitlines()[-2] + "' (out/page_smoke_project.out). The page's pyodide/browser run is the page_smoke run; the self-assessment form was not separately exercised.")
fresh("proj-lab1-run", "PASS", "tools/run_labs.py --unit PC3 --page project; tests/labs/PC3/lab-PC3-project-1.py under python -I -W error",
      "Re-run this round: run_labs '" + out("run_labs_project.out").strip().splitlines()[-2] + "'. Twin run alone: python -I -W error exit 0, stderr 0 bytes, stdout equals the page's expected block (out/twin_vs_page.out).")
fresh("proj-twin-rules", "PASS", "tests/labs/PC3/lab-PC3-project-1..3.py run with python -I -W error from a scratch directory",
      "Re-run this round (ledgers/PC3/scripts/PC3-c-r14/twin_vs_page.py): lab 1, 2 and 3 twins exit 0 with empty stderr under python -I -W error from /tmp/pc3c-r14-lab{1,2,3}; out/twin_vs_page.out.")
fresh("proj-exception-types-labs", "PASS", "tests/labs/PC3/lab-PC3-project-1..3.py",
      "Re-checked this round: the lab twins raise only the two named ValueErrors in replay (lab-PC3-project-1.py lines 108-109 and 115-116; lab-PC3-project-3.py lines 96-97 and 101-102); the labs never call replay on an invalid log, and all three runs exit 0 with empty stderr (out/twin_vs_page.out).")
fresh("proj-r5-labs-page-vs-twin", "PASS", "project labs 1-3: page code vs tests/labs/PC3/lab-PC3-project-1..3.py",
      "Re-run this round (ledgers/PC3/scripts/PC3-c-r14/twin_vs_page.py and out/twin_identity_check.out): labs 1 and 3 page code identical to the twin apart from the final newline; lab 2 differs only in the two blank lines '    cash_flow = ___' and '    mark = ___'. Expected blocks equal the twin stdout for all three labs.")
fresh("proj-lab1-replay-prints", "PASS", "course/modules/PC/PC3/project.html lab-PC3-project-1 (lines 55-240) against tests/labs/PC3/lab-PC3-project-1.py",
      "Re-run this round: the page's expected block (project.html lines 219-237) equals the twin's stdout (twin_vs_page.py: 'expected == twin stdout: True'); per-fill lines and the four numbers match ledgers/PC3/scripts/PC3-c-r14/out/numbers_r14.out.")
fresh("proj-lab1-hypothesis-numbers", "PASS", "course/modules/PC/PC3/project.html line 57 (Lab 1 hypothesis)",
      "Re-derived this round (ledgers/PC3/scripts/PC3-c-r14/numbers_r14.py, out/numbers_r14.out): 9 fills, cash flow -9950, inventory 1, settlement 9980, mark 9980, P&L 30, max |inventory| 3 (limit 10). Every number in the line-57 hypothesis matches.")
fresh("proj-lab2-completion", "PASS", "course/modules/PC/PC3/project.html lab-PC3-project-2 (lines 242-380) against tests/labs/PC3/lab-PC3-project-2.py",
      "Re-run this round: the page code differs from the twin only at the two blanks (out/twin_identity_check.out); the twin runs exit 0 and its stdout equals the expected block (out/twin_vs_page.out).")
fresh("proj-lab2-interpretation-last-quote", "PASS", "course/modules/PC/PC3/project.html line 381 (Lab 2 interpretation)",
      "Read this round: 'a mark at any price other than the settlement value of 9980 cents changes the P&L' holds by arithmetic (mark = 1 x price, P&L = -9950 + price); the blanks are the cash-flow and mark lines of the twin (lab-PC3-project-2.py lines 105-106).")
fresh("proj-lab3-counterfactual", "PASS", "course/modules/PC/PC3/project.html lines 457-612 (Lab 3) against tests/labs/PC3/lab-PC3-project-3.py",
      "Re-run this round: the twin's stdout equals the page's expected block (out/twin_vs_page.out); the counterfactual (half-spread 15): 9 fills, P&L 55, change 25 is reproduced by numbers_r14.py (out/numbers_r14.out).")
fresh("proj-lab3-interpretation", "PASS", "course/modules/PC/PC3/project.html line 611 (Lab 3 interpretation)",
      "Read this round: 'It is not an estimate ... and the lab does not test any other seed' holds; the lab's play() is called only with SEED = 0 (tests/labs/PC3/lab-PC3-project-3.py line 24 and lines 118, 132).")
fresh("proj-r10-instances-20-seeds", "PASS", "course/modules/PC/PC3/grader/instance.py lines 27-53; grader/test_project.py instance tests",
      "Re-run this round: pytest collect and reference pass (out/collect_counts_r14.out); instances for 20 sampled seeds are valid and the reference answers vary with the seed (out/instance_answers.out: 6 distinct PnL values of 20 sampled seeds, 14 of the 50 fixed seeds; cash flow and ending inventory differ across seeds).")
fresh("proj-grader-instances", "PASS", "course/modules/PC/PC3/grader/instance.py; grader/test_project.py test_instance_is_deterministic_and_well_formed and test_fixed_seeds_0_to_49_give_fifty_different_paths",
      "Re-run this round: reference suite 486 passed for seed 0 (out/collect_counts_r14.out); instance answers vary across seeds (out/instance_answers.out).")
fresh("proj-r8-collect-counts", "PASS", "course/modules/PC/PC3/grader/test_project.py; collect-only counts",
      "Re-run this round (out/collect_counts_r14.out): collect-only 486 for seeds 0, 7 and 49, 495 for seed 100; the reference suite passes 486 of 486 for seed 0. Page line 397 says 486 (seeds 0-49) and 495 (other seeds): equal.")
fresh("proj-r8-pytest-pc3", "PASS", "pytest -k PC3",
      "Re-run this round: '" + out("pytest_k_PC3.out").strip() + "' (out/pytest_k_PC3.out).")
fresh("proj-r8-verify-refs", "PASS", "tools/verify_refs.py --offline",
      "Re-run this round: '" + out("verify_refs_offline.out").strip().splitlines()[-2] + "' (out/verify_refs_offline.out).")
fresh("proj-lint-ruff", "PASS", "ruff check and ruff format --check on course/modules/PC/PC3/grader, tests/labs/PC3 and tests",
      "Re-run this round: ruff check '" + out("ruff_check.out").strip().splitlines()[-1] + "'; ruff format --check '" + out("ruff_format.out").strip().splitlines()[-1] + "' (out/ruff_*.out).")
fresh("proj-mypy-labs", "PASS", "mypy --no-incremental (repo config)",
      "Re-run this round: '" + [l for l in out("mypy_repo.out").splitlines() if l.startswith("Success") or "error" in l][0] + "' (out/mypy_repo.out).")
fresh("proj-grader-mypy-strict", "PASS", "scratch copy: engine.py, instance.py, test_project.py, market_maker.py (= reference.py)",
      "Re-run this round: mypy --strict --no-incremental on the four scratch modules: '" + out("mypy_strict_scratch.out").strip() + "' (out/mypy_strict_scratch.out).")
fresh("proj-grader-reference", "PASS", "course/modules/PC/PC3/grader/reference.py via tools/run_graders.py --unit PC3 --seeds 0-49",
      "Re-run this round: '" + out("run_graders.out").strip().splitlines()[-2] + "' (out/run_graders.out); reference suite 486 passed for seed 0 (out/collect_counts_r14.out).")
fresh("proj-grader-starter-fails", "PASS", "course/modules/PC/PC3/grader/starter.py in a scratch copy with test_project.py",
      "Re-run this round (out/starter_fails_r14.out): starter.py as market_maker.py gives '" + out("starter_fails_r14.out").strip() + "' for seed 0.")
fresh("proj-grader-35-checks", "PASS", "course/modules/PC/PC3/project.html line 397; grader/test_project.py",
      "Re-run this round: 9 per-seed tests x 51 seeds + 24 seed-only + 3 seed-free = 486 (seed 0, 7, 49) and 9 x 52 + 24 + 3 = 495 (seed 100), out/collect_counts_r14.out. The per-seed list in line 397 matches the nine parametrised tests (test_quotes_are_legal..., test_replay_returns..., test_replay_agrees..., test_pnl_is_..., test_money_..., test_cash_moves..., test_a_log_carries..., test_instance_is_..., test_no_function_prints...).")
fresh("proj-builder-mutants", "PASS", "ledgers/PC3/mutants/m01..m10",
      mut_evidence(["m0", "m10"], "m01..m10:"))
fresh("proj-mutant-m08-description", "PASS", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py line 1",
      mut_evidence(["m08"], "m08:") + " Its docstring first line reads as a hard-coded answer error.")
fresh("proj-verifier-mutants", "PASS", "ledgers/PC3/mutants/v01..v16 and v18..v26 (v17 absent)",
      mut_evidence(["v01", "v02", "v03", "v04", "v05", "v06", "v07", "v08", "v09", "v10", "v11", "v12", "v13", "v14", "v15", "v16",
                    "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26"], "v01..v16, v18..v26:"))
for rid, prefixes, label in [
    ("proj-verifier-mutants-r3-new", ["v13", "v14", "v15", "v16"], "v13..v16:"),
    ("proj-r4-new-mutants-v18-v20", ["v18", "v19", "v20"], "v18..v20:"),
    ("proj-grader-v21-replay-scales-by-size", ["v21"], "v21:"),
    ("proj-grader-v22-zero-fill-price-refused", ["v22"], "v22:"),
    ("proj-r5-mutant-v23-first-fill-price", ["v23"], "v23:"),
    ("proj-grader-v24-stderr-print-survives", ["v24"], "v24:"),
    ("proj-grader-v25-last-filled-totals-survives", ["v25"], "v25:"),
    ("proj-grader-v26-logging-warning-survives", ["v26"], "v26:"),
    ("proj-verifier-mutants-r7-new", ["v27", "v28", "v29", "v30"], "v27..v30:"),
    ("proj-verifier-mutants-r8-new", ["v31", "v32", "v33", "v34"], "v31..v34:"),
    ("proj-verifier-mutants-r9-new", ["v35", "v36", "v37", "v38"], "v35..v38:"),
    ("proj-verifier-mutants-r10-new", ["v39", "v40", "v41", "v42"], "v39..v42:"),
    ("proj-verifier-mutants-r11-new", ["v43", "v44", "v45", "v46"], "v43..v46:"),
    ("proj-grader-v44-limit-lock-survives", ["v44"], "v44:"),
]:
    fresh(rid, "PASS", "ledgers/PC3/mutants/" + label.rstrip(":"), mut_evidence(prefixes, label))
fresh("proj-r13-mutants-r13_01-05", "PASS", "ledgers/PC3/mutants/r13_01..r13_05",
      mut_evidence(["r13_"], "r13_01..r13_05:"))

# ---- rows re-verified this round (their cited subject changed, or the row needs a fresh run) ----
fresh("proj-conventions-constants", "PASS", "course/modules/PC/PC3/project.html lines 402-407 (Conventions) and 393; grader/instance.py; grader/engine.py",
      "Re-read this round: N = 20 (line 402), v0 = 10000 cents, moves of +/-5 cents with probability 1/2 (line 402), arrival probabilities 1/4, 1/4, 1/2 (line 404), |I| <= 10 (line 405), q_t in 0..5 and b_t < a_t (line 403). instance.py START_CENTS 10000, MOVE_CENTS 5, draw thresholds 0.25 and 0.5; engine.py MAX_SIZE 5, LIMIT 10: all equal. Line 407 changed this round; its math spans are identical to the previous pin (out/math_spans_check.out), only the words changed.")
fresh("proj-hours-arithmetic", "PASS", "course/modules/PC/PC3/project.html lines 421-438 (time budget); course/modules/PC/PC3/index.html line 167",
      "Re-derived: 1 + 1 + 3 + 2 + 2 + 4 + 1 = 14 (lines 425-433 of the table, the total row 434 reads 14); 14 / 50 = 28.0 %; index.html line 167 reads '14 hours of project, which is 28 percent of the module' and 'the lines sum to 1 + 1 + 3 + 2 + 2 + 4 + 1 = 14'. Own estimate of the build (not measured): roughly 13 to 16 hours for a student who writes quote and replay to this spec and runs the suite, inside 30 % of 14. Line 432 changed this round (the analysis rationale wording only; no hour changed).")
fresh("proj-rubric-atlas-studios", "PASS", "course/modules/PC/PC3/project.html (whole page); plans/PC3-build-plan.md lines 510-511; curriculum/06-profession-capstone.yaml lines 173-183; curriculum/curriculum.json",
      "Re-checked this round: the PC3 project block has no atlas key (curriculum/06-profession-capstone.yaml project block); curriculum.json 'atlas' array has 20 entries and none mentions PC3 (python json check). The page has no atlas milestone or studio requirement, and the plan (lines 510-511) says the same. PC3 is not a studio unit.")
fresh("proj-banned-and-process-words", "PASS", "course/modules/PC/PC3/project.html; grader/*.py; tests/labs/PC3/lab-PC3-project-*.py",
      "Re-run this round: grep (case-insensitive, fixed strings) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, verifier, fixer, builder, draft, ' we ', ' our ', ' I ', please, placeholder and ellipses: zero hits in the page and the code (the only 'round' hits are 'around' in project.html line 466 and reference.py lines 5 and 21).")
fresh("proj-notation", "PASS", "notation/notation.json (8 symbols); course/modules/PC/PC3/project.html math spans (49 spans)",
      "Re-run this round: the page's 49 math spans use only I, N, a, b, q, t, v, pnl and the words of 'cash flow'; none of the 8 notation.json symbols (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q) occurs, so no collision. Changed lines 407, 432, 696: math spans identical at 407 (out/math_spans_check.out); no math at 432 or 696.")
fresh("proj-exemplar-a-numbers", "PASS", "course/modules/PC/PC3/project.html lines 635-662 (exemplar A) against ledgers/PC3/scripts/PC3-c-r14/out/numbers_r14.out",
      "Re-derived: purchases at the bid on turns 2, 3, 4, 8, 19 = 9990+9980+9970+9980+9990 = 49910; sales at the ask on turns 5, 7, 13, 18 = 9980+9990+9990+10000 = 39960; cash flow 39960 - 49910 = -9950; inventory 1; mark 1 x 9980 = 9980; P&L 30 = -9950 + 9980. Turn 2 bid 9990 fill 9990; turn 5 ask 9980 fill 9980 inventory after 2; turn 18 ask 10000 fill 10000 inventory after 0 (all match the log, numbers_r14.out). Counterfactual half-spread 15: 9 fills, P&L 55, change +25. Largest |inventory| 3. Every number in exemplar A matches.")
fresh("proj-exemplar-b-numbers", "PASS", "course/modules/PC/PC3/project.html lines 664-690 (exemplar B) against ledgers/PC3/scripts/PC3-c-r14/out/numbers_r14.out",
      "Re-derived: P&L 30 and cash flow -9950 (numbers_r14.out); turn 5 sold at the ask of 9980 (turn 5 fill 9980, side -1, numbers_r14.out). Exemplar B states no other number that the log contradicts.")
fresh("proj-exemplar-a-calibration", "PASS", "course/modules/PC/PC3/project.html lines 635-662 (passage text) against rubric lines 623-627; ledgers/PC3/scripts/PC3-c-r14/blind_scores.json",
      "Scored this round from the rubric and the passage text only (blind_extract.py output; verdict and annotations removed): C1 4, C2 4, C3 4, C4 3, C5 4. Official 4,4,4,3,4 and every annotation (lines 653-658) are within one level: match on all five. Blindness is not certified for this verifier: see proj-exemplar-scores-blind-disclosure.")
fresh("proj-exemplar-b-calibration", "PASS", "course/modules/PC/PC3/project.html lines 664-692 (passage text) against rubric lines 623-627; ledgers/PC3/scripts/PC3-c-r14/blind_scores.json",
      "Scored this round from the rubric and the passage text only: C1 2, C2 2, C3 1, C4 2, C5 1. Official 2,2,1,2,1 and the annotations (lines 682-688) match within one level on all five. Blindness is not certified for this verifier: see proj-exemplar-scores-blind-disclosure.")
fresh("proj-exemplar-scores-blind-disclosure", "FAIL",
      "course/modules/PC/PC3/project.html lines 635, 653, 655, 664, 680-690 (data-scores and annotations); this verifier's blind record ledgers/PC3/scripts/PC3-c-r14/blind_scores.json",
      "Verifier-side blind condition not met. Before writing the blind record I ran grep on project.html, which printed lines 635-690 (data-scores, the official-scoring paragraphs and the annotation asides). The blind scores in blind_scores.json were then derived from the descriptors and the passage text, and they match the official levels within one level (A 4,4,4,3,4; B 2,2,1,2,1), but this verifier cannot certify a blind scoring. The disclosure is recorded in blind_scores.json and in the notes.",
      fix="A fresh verifier who has not read project.html lines 635-690 re-scores exemplars A and B from the rubric (lines 617-631) and the passage text only, and records the scores before any grep of the page. The page-side leak is proj-exemplar-scores-in-served-html.")
fresh("proj-exemplar-scores-in-served-html", "FAIL",
      "course/modules/PC/PC3/project.html line 635 (article data-scores=\"4,4,4,3,4\", data-level=\"4\") and line 664 (data-scores=\"2,2,1,2,1\"); annotation asides lines 651-660 and 680-690; course/assets/js/rubric.js line 149",
      "Still present at 8e5751c: grep -n 'data-scores=' returns lines 635 and 664; the annotation asides are in the served HTML; rubric.js line 149 hides only '.annotation, [data-reveal]' (setRevealed) and does not keep the data out of the source. The round-14 change at line 696 now discloses this in the self-assessment paragraph, which is accurate ('both are in the page source'), but the leak the round-13 row describes is not removed.",
      fix="Move the official levels and the annotations out of the served HTML: load them from a JSON payload on the reveal action, or inject them into the DOM only when the reveal control is pressed. Then re-run tools/page_smoke.py --unit PC3 --pages project.html and confirm the self-assessment table still renders.")
fresh("proj-plan-5-6-tests-not-in-suite", "FAIL",
      "plans/PC3-build-plan.md lines 420-423 (Inventory limit bullet, changed) and 430-432 (Seed consistency bullet, changed); course/modules/PC/PC3/grader/test_project.py lines 400-408 and 541-552",
      "Inventory bullet (420-423): accurate. grep for the inventory bound on game logs finds only line 552 (a hand-built instance check) and no |inventory_after| <= 10 assertion; test_fills_stop_at_the_inventory_limit_in_each_direction exists at test_project.py line 542. Seed bullet (430-432): the new sentence 'a copied log carries the other seed in its seed field, so this check is what would refuse it' is wrong. test_a_log_carries_its_own_seed_and_settlement (lines 400-408) plays engine.play(sol.quote, seed) and checks log['seed'] == seed and the settlement of make_instance(seed); the engine writes seed=int(seed) (engine.py line 100), so the check never receives a copied log and cannot refuse one. The copied-log refusal is not tested.",
      fix="Reword plan lines 430-432 to say that no test refuses a log copied from another seed, or add a test that passes a seed-0 log to the seed-7 check (and then update the counts on project.html line 397 and re-run collect-only for seeds 0, 7 and 100). Keep the inventory bullet as it is.")
fresh("proj-plan-file-names", "PASS", "plans/PC3-build-plan.md lines 67-70, 317, 337, 340, 348 against project.html lines 46, 393, 429-430, 443 and index.html lines 160, 167 and grader/starter.py line 1",
      "Carried from round 13 (cited lines unchanged since e919577: the plan change is at 420-423 and 430-432, project.html changed lines are 407, 432, 696, none cited here): " + r13["proj-plan-file-names"]["evidence"])
fresh("proj-grader-replay-from-fills", "FAIL", "course/modules/PC/PC3/project.html line 407 (Conventions: 'the cash flow the sum of the fill cash flows ... carry no rounding'); course/modules/PC/PC3/grader/test_project.py lines 249-263 and 283-293",
      "Re-verified: test_replay_returns_the_fills_cash_flow_inventory_and_pnl (lines 249-263) and test_replay_sums_the_fills_not_the_running_totals (283-293) do check the cash flow as the sum over fills. But every fill price in the suite's hand-built logs is a multiple of 10 cents (10010, 9990, 10020, 10000 and 0; grep of test_project.py, e.g. lines 286, 302, 315, 327, 474), so a replay that rounds fill prices to the dime is not refused: mutant r14_01 survives (out/mutate_PC3_0-49_all_r14.out). The sentence 'carry no rounding' is therefore not tested for non-dime prices.",
      fix="Add a hand-built log with a sale at 9995 and a purchase at 10003 (or similar non-dime prices) that asserts replay == oracle(log); this also kills s14_02 and r14_01. Update the seed-only count on project.html line 397 (24 -> 25: totals 487 and 496) and re-run collect-only for seeds 0, 7 and 100.")
fresh("proj-no-print-rare-branch-survivors", "FAIL",
      "course/modules/PC/PC3/grader/test_project.py test_no_function_prints_or_warns (lines 411-444) and the direct sweep (direct_states, lines 118-135); project.html line 395 ('Neither quote nor replay prints or warns'); ledgers/PC3/mutants/s14_01_quote_prints_on_turn_thirteen_at_inventory_seven.py",
      "Mutant s14_01 (a debugging print in quote when turn == 13 and inventory == 7) SURVIVES mutate_graders --seeds 0-49 (out/mutate_PC3_0-49_all_r14.out). The no-print test calls quote only on the game of each seed, on the hand-built logs, and on direct_states(), which sweep turns 1 and 20 only (lines 123-124). The fixed seeds reach inventory only in -8..8 (out/reach_check.out) and not (turn 13, inventory 7) (out/reach_check.out: False). The page (line 395) states the universal rule 'Neither quote nor replay prints or warns', so the test does not check the stated behaviour on every state.",
      fix="Sweep direct_states() over turns 1 to 20 (or 2 to 19 as well) at every inventory from -10 to 10 in test_no_function_prints_or_warns and in the quote legality sweep, and update the page's third-check description (project.html line 397) and the test docstrings to say so. The count stays 486 and 495.")
fresh("proj-direct-legal-sweep-turn20-no-history", "FAIL",
      "course/modules/PC/PC3/grader/test_project.py test_a_direct_quote_is_legal_at_every_inventory_within_the_limit (lines 497-506) and direct_states (lines 118-135); project.html line 395 ('A quote must have its bid below its ask') and line 397 (third check)",
      "The sweep covers turns 1 and 20 only (direct_states lines 123-124). Mutant r14_03 (a locked quote when the inventory is -10 on turns 2 to 19) SURVIVES (out/mutate_PC3_0-49_all_r14.out); the fixed seeds never reach (turn 2-19, inventory -10) (out/reach_check.out). The control s14_03 (a locked quote on turn 1 at +10) is killed by this test, so the sweep works where it reaches. The universal rule 'A quote must have its bid below its ask' (line 395) is not checked on turns 2 to 19 at the limit.",
      fix="Extend direct_states() to every turn from 1 to 20 (the history passed for turn t is the t-1 unfilled records, as now), keep the same assertions, and state the coverage in the docstring and on project.html line 397. The counts 486 and 495 do not change.")
fresh("proj-r12-survivor-reachability", "PASS", "ledgers/PC3/scripts/PC3-c-r12/r12_probe_reach.py",
      "Carried from round 13 (cited script and the engine and reference it runs are byte-identical since e919577): " + r13["proj-r12-survivor-reachability"]["evidence"])

# ---- new round-14 rows ----
fresh("proj-r14-grader-rounding-survivor", "FAIL", "ledgers/PC3/mutants/r14_01_replay_rounds_fill_prices_to_the_dime.py; course/modules/PC/PC3/project.html line 406 ('A maker purchase at the bid b changes cash by -b') and line 407 ('carry no rounding')",
      surv_evidence("r14_01_replay_rounds_fill_prices_to_the_dime.py", "r14_01:") + " The mutant books cash at round(price, -1); the mutant's quote is the reference quote (mid +/- 10 around the last fill or 10000), so by induction every fill price is a multiple of 10 on every seed, and the rounding changes nothing that any seed's game produces.",
      fix="See proj-grader-replay-from-fills: add a non-dime fill to the hand-built replay tests.")
fresh("proj-r14-grader-locked-market-survivor", "FAIL", "ledgers/PC3/mutants/r14_03_quote_locks_the_market_at_the_limit_mid_game.py; course/modules/PC/PC3/project.html line 395 ('A quote must have its bid below its ask')",
      surv_evidence("r14_03_quote_locks_the_market_at_the_limit_mid_game.py", "r14_03:") + " The mutant returns a locked quote when the inventory it sees is -10 on turns 2 to 19. No fixed seed reaches that state (out/reach_check.out), and the direct sweep covers turns 1 and 20 only.",
      fix="See proj-direct-legal-sweep-turn20-no-history: sweep every turn 1 to 20 at inventories -10 to 10.")
fresh("proj-r14-grader-print-survivor", "FAIL", "ledgers/PC3/mutants/s14_01_quote_prints_on_turn_thirteen_at_inventory_seven.py; course/modules/PC/PC3/project.html line 395 ('Neither quote nor replay prints or warns')",
      surv_evidence("s14_01_quote_prints_on_turn_thirteen_at_inventory_seven.py", "s14_01:") + " A new student-error mutant written by this verifier: a debugging print on turn 13 at inventory +7, which no fixed seed reaches (out/reach_check.out).",
      fix="See proj-no-print-rare-branch-survivors: sweep every turn in the no-print and legality checks.")
fresh("proj-r14-grader-offgrid-survivor", "FAIL", "ledgers/PC3/mutants/s14_02_replay_refuses_a_fill_off_the_dime_grid.py; course/modules/PC/PC3/project.html line 395 ('Money is an integer number of cents everywhere') and line 407",
      surv_evidence("s14_02_replay_refuses_a_fill_off_the_dime_grid.py", "s14_02:") + " A new student-error mutant written by this verifier: replay refuses any fill price that is not a multiple of 10. The page names no refusal for it, and integer cents are valid input, so the refusal is a fault the suite must catch. For this mutant's own quote every fill is a multiple of 10 (induction as for r14_01), and no hand-built test uses a non-dime fill price, so only a non-dime hand-built log can trigger it.",
      fix="See proj-grader-replay-from-fills: add a non-dime hand-built fill with replay == oracle(log).")
fresh("proj-r14-mutant-control-s14_03", "PASS", "ledgers/PC3/mutants/s14_03_quote_locks_the_market_on_turn_one_at_inventory_ten.py",
      mut_evidence(["s14_03"], "s14_03 (control, turn 1 at +10):") + " The direct sweep on turn 1 catches it, so the sweep is effective where it reaches.")
fresh("proj-r14-mutants-aggregate", "FAIL", "ledgers/PC3/mutants/ (70 files: m01-m10, v01-v49 without v17, r13_01-05, r14_01-04, s14_01-03)",
      "tools/mutate_graders.py --unit PC3 --seeds 0-49: 'mutate_graders PC3: FAIL (66/70 killed)' (out/mutate_PC3_0-49_all_r14.out). Survivors: r14_01, r14_03, s14_01, s14_02 (rows proj-r14-grader-*-survivor). Every other mutant is killed; the list of killing tests is in the mutants array.",
      fix="Close the four survivors as their rows say, then re-run tools/mutate_graders.py --unit PC3 --seeds 0-49 and require 70/70.")
fresh("proj-r14-plan-cash-identity-sign", "FAIL", "plans/PC3-build-plan.md line 424 ('Cash identity: cash_after changes by exactly -ask on a buy fill and +bid on a sell fill')",
      "Contradicts the page: project.html line 406 says 'A maker purchase at the bid b changes cash by -b ... A maker sale at the ask a changes cash by +a' and engine.py lines 83-86 book cash as -side x price with a maker sale at the ask (side -1) giving +ask. The plan's sentence gives -ask on a customer buy (maker sale, cash +ask) and +bid on a customer sell (maker purchase, cash -bid): the sign and the price are the wrong way round for the maker's cash_after, which is the field it names. test_cash_moves_by_the_fill_price_on_each_turn (grader test lines 370-384) checks the page's version, so the plan and the suite disagree.",
      fix="Rewrite plan line 424 as: 'cash_after changes by exactly +ask on a maker sale at the ask and by -bid on a maker purchase at the bid (integers), as in project.html Conventions'.")
fresh("proj-r14-plan-instance-sample-count", "FAIL", "plans/PC3-build-plan.md line 406 ('the test counts distinct paths over 20 sampled seeds')",
      "course/modules/PC/PC3/grader/test_project.py lines 531-535 (test_fixed_seeds_0_to_49_give_fifty_different_paths) count distinct paths over range(50) and expect 50; the page (project.html line 397) says the same. The plan's '20 sampled seeds' does not describe the test. Re-run this round: 50 distinct paths (out/instance_answers.out lists the reference answers for 20 sampled seeds).",
      fix="Change plan line 406 to 'over the fifty fixed seeds 0 to 49'.")
fresh("proj-r14-plan-reference-description", "FAIL", "plans/PC3-build-plan.md lines 407-408 ('quote posts a symmetric quote around the last fair value the public history implies (the last filled price, or start_cents before any fill)')",
      "course/modules/PC/PC3/grader/reference.py lines 21-26 and 5-7: quote uses the last filled price from the history, or 10000 cents before any fill; it does not estimate a fair value. The phrase 'the last fair value the public history implies' describes an estimate the reference does not compute, and the parenthesis then says what it does. The page's Rung 1 text (project.html line 53) names the last filled price as the mid.",
      fix="Replace 'the last fair value the public history implies' with 'the last filled price in the public history'.")
fresh("proj-r14-plan-inventory-bullet", "PASS", "plans/PC3-build-plan.md lines 420-423 (changed this round) against course/modules/PC/PC3/grader/test_project.py lines 541-552",
      "Re-verified: the bullet says a hand-built order that would breach the limit is recorded filled: false (test_fills_stop_at_the_inventory_limit_in_each_direction, test_project.py line 542, hand-built custom instance, both directions) and that the suite does not assert |inventory_after| <= 10 on game logs (grep: no such assertion; the only inventory_after checks are lines 108, 278, 552, 584). Both statements are accurate.")
fresh("proj-r14-self-assessment-disclosure", "PASS", "course/modules/PC/PC3/project.html line 696 (changed this round) against course/assets/js/rubric.js line 149 and project.html lines 635, 664",
      "Re-verified: 'The page's script hides the annotations and the official levels' is true of the hidden attribute only for '.annotation, [data-reveal]' (rubric.js line 149), and 'both are in the page source' is true (project.html lines 635 and 664 carry data-scores; the annotation asides are in the HTML). The sentence is accurate; the leak it describes remains (proj-exemplar-scores-in-served-html).")
fresh("proj-r14-settlement-rule-definition", "PASS", "course/modules/PC/PC3/project.html line 407 (changed this round); the rubric C4 cell (line 626) that names 'the settlement rule'",
      "Re-read: line 407 now defines 'The settlement rule is that the game is settled at its settlement value v20', the term the C4 level 4 and level 3 cells use. The definition is in the same bullet as the inventory mark, and the value v20 is defined in the same sentence and on line 402 (fair value v_20). No term is used before it is defined on the page.")
fresh("proj-r14-lab-draw-equals-instance", "PASS", "tests/labs/PC3/lab-PC3-project-1..3.py draw_game(0) against course/modules/PC/PC3/grader/instance.py make_instance(0) (project.html line 53 claim)",
      "Re-run this round (ledgers/PC3/scripts/PC3-c-r14/lab_draw_vs_instance.py, out/lab_draw_vs_instance.out): each lab's fair path and arrivals equal instance.make_instance(0): 'path equal=True arrivals equal=True' for labs 1, 2 and 3. Page line 53 ('the fair path and arrivals that grader/instance.py generates for seed 0') is accurate.")
fresh("proj-r14-reading-keys", "PASS", "course/modules/PC/PC3/project.html lines 714-715 (data-cite) against references/references.json",
      "Re-run this round: references.json entries contain keys 'zhou2008practical' (openlibrary, 'A practical guide to quantitative finance interviews') and 'crack2015heard' (openlibrary, 'Heard on the street: quantitative questions from Wall Street job interviews'); 560 entries in total, matching verify_refs --offline (out/verify_refs_offline.out). The page cites by key only and attributes no problem to either book.")
fresh("proj-r14-l04-cited-sentences", "PASS", "course/modules/PC/PC3/L04.html line 60 (anchor def-market-making-game) and the 'queue of resting orders' and 'does not model learning' sentences; project.html line 37 and rubric line 626",
      "Re-read this round: L04.html line 60 has <dfn id=\"def-market-making-game\" data-concept=\"market-making-game\">, matching the page link. The statements the rubric and page rely on ('this game does not model that queue'; 'this lesson does not model learning') are present in L04.html. L04.html changed at lines 65, 72 and 83 this round (not cited here; out of this slice).")
fresh("proj-r14-reach-and-instances", "PASS", "course/modules/PC/PC3/grader/test_project.py lines 411-418 (docstring: 'branches that a game of the fixed seeds never takes') against the fixed-seed reach",
      "Re-run this round (ledgers/PC3/scripts/PC3-c-r14/reach_check.py, out/reach_check.out): the reference rule on seeds 0-49 reaches inventory -8..8 only; (turn 2-19, inventory -10) is not reached; the docstring's claim that the log that ends at inventory -10 is not reached by a fixed-seed game is true.")
fresh("proj-r14-alternatives-15", "PASS", "ledgers/PC3/alternatives/alt1..alt6; ledgers/PC3/scripts/PC3-c-r13/alts/*.py (5); ledgers/PC3/scripts/PC3-c-r14/alts/alt_r14_a..d (4)",
      "Re-run this round (ledgers/PC3/scripts/PC3-c-r14/run_alts_r14.py, out/alts_r14.out): all 15 correct alternatives pass the checkout's suite on seeds 0-49 (0 of 50 failing seeds for each). The runner is sanity-checked: reference.py 0 of 50, v37 (locked quote on turn 20) 50 of 50, r14_01 0 of 50 (out/runner_sanity_r14.out). The four new alternatives are: alt_r14_a reverse scan with break; alt_r14_b turn-keyed max lookup; alt_r14_c size 0 at the limit; alt_r14_d int() on every money value.")
fresh("proj-r14-lint-mypy-pytest", "PASS", "ruff check and ruff format --check (course/modules/PC/PC3/grader, tests/labs/PC3, tests); mypy --no-incremental; mypy --strict on the grader modules; pytest -k PC3",
      "Re-run this round: see proj-lint-ruff, proj-mypy-labs, proj-grader-mypy-strict and proj-r8-pytest-pc3 (each with its out/ file).")


# ---- assemble ----
MANUAL_CARRY = {
    "proj-grader-no-print": "cited project.html line 395 is unchanged; the '407' the mechanical test matched is a grader test line (test_project.py 391-407), and grader/ is byte-identical",
}
rows = []
for r in R13["rows"]:
    rid = r["id"]
    if rid in R:
        e = R[rid]
        rows.append(dict(id=rid, check=r["check"], location=e["location"], status=e["status"], evidence=e["evidence"],
                         **({"fix": e["fix"]} if e["status"] != "PASS" else {})))
    elif rid in PLAN["carry"] or rid in MANUAL_CARRY:
        why = MANUAL_CARRY.get(rid, "no changed line is cited (carry test, out/carry_plan.json)")
        rows.append(dict(id=rid, check=r["check"], location=r["location"], status="PASS",
                         evidence=("Carried from round 13 (cited files byte-identical since the previous pin e919577; "
                                   f"the round-14 changed lines are project.html 407, 432, 696, plans/PC3-build-plan.md 420-423 and 430-432, "
                                   f"L04.html 65, 72, 83; {why}): " + r["evidence"])))
    else:
        raise SystemExit(f"row {rid} has neither fresh evidence nor a carry decision")
seen = {r["id"] for r in R13["rows"]}
for rid, e in R.items():
    if rid not in seen:
        rows.append(dict(id=rid, check=e["check"], location=e["location"], status=e["status"], evidence=e["evidence"],
                         **({"fix": e["fix"]} if e["status"] != "PASS" else {})))
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
for r in rows:
    assert r["status"] in ("PASS", "FAIL", "UNVERIFIABLE")
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]
counts = {k: sum(1 for r in rows if r["status"] == k) for k in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"

notes = [
    "Delta: e919577 (round-13 pin) to 8e5751c. Changed hunks in this slice: project.html lines 407 (Conventions, P&L bullet), 432 (hours rationale) and 696 (self-assessment paragraph); plans/PC3-build-plan.md lines 420-423 (inventory bullet) and 430-432 (seed bullet). Outside the slice but cited: L04.html lines 65, 72, 83 (not cited by any row except the re-read of its queue, learning and anchor sentences); L06.html and cards.json (other slices). grader/, tests/labs/PC3/, ledgers/PC3/alternatives/, rubric.js, grader.js, index.html, references/ and notation/ are byte-identical to e919577 (git diff --name-only).",
    "Blind calibration: the blind record is ledgers/PC3/scripts/PC3-c-r14/blind_scores.json (extraction script blind_extract.py). Disclosure: a grep of project.html printed lines 635-690 (data-scores, official-scoring paragraphs and annotation asides) before the blind record was written, so the verifier cannot certify a blind scoring. The scores derived from the descriptors and the passage text (A 4,4,4,3,4; B 2,2,1,2,1) match the official levels and every annotation within one level; the process gap is row proj-exemplar-scores-blind-disclosure (FAIL).",
    "Pre-existing artifacts: this checkout already held untracked files from an earlier attempt at this slice: ledgers/PC3/PC3-c.json (round 14, verdict FAIL, dated Nov 5 14:54), ledgers/PC3/mutants/r14_01..r14_04 and ledgers/PC3/scripts/PC3-c-r14/ (prior outputs). They were not produced in this run and were not trusted: every gate, every mutant (all 70, including r14_01..r14_04) and every alternative was re-run in this run, and the fragment was rebuilt from those outputs. The prior fragment file is overwritten.",
    "Mutants: 70 files run with tools/mutate_graders.py --unit PC3 --seeds 0-49 (out/mutate_PC3_0-49_all_r14.out): 66 killed, 4 survive: r14_01 (fill prices rounded to the dime), r14_03 (locked quote at inventory -10 on turns 2-19), s14_01 (debug print on turn 13 at inventory +7), s14_02 (replay refuses fill prices off the 10-cent grid). New student-error mutants written this round: s14_01, s14_02, s14_03 (s14_03 is a control and is killed). The four survivors each violate a sentence of project.html (line 395 or 406-407); see their rows for the cited sentences and the fixes.",
    "Alternatives: 15 correct implementations pass seeds 0-49 each: ledgers/PC3/alternatives alt1-alt6; ledgers/PC3/scripts/PC3-c-r13/alts (5); new ledgers/PC3/scripts/PC3-c-r14/alts/alt_r14_a..d (4). Runner: ledgers/PC3/scripts/PC3-c-r14/run_alts_r14.py, sanity-checked against reference.py and two killed mutants (out/runner_sanity_r14.out).",
    "Gates (outputs in ledgers/PC3/scripts/PC3-c-r14/out/): check_pages --unit PC3 PASS; check_dag --unit PC3 PASS; check_projects --unit PC3 PASS; run_labs --unit PC3 --page project 3/3 PASS; run_graders --unit PC3 --seeds 0-49 reference 50/50 PASS; page_smoke --unit PC3 --pages project.html PASS; verify_refs --offline 560 entries 0 problems; ruff check and ruff format --check on the PC3 grader, tests/labs/PC3 and tests PASS; mypy --no-incremental Success (385 files); mypy --strict on the four scratch grader modules Success; pytest -k PC3 9 passed; collect-only 486 (seeds 0, 7, 49) and 495 (seed 100); reference suite 486 passed; starter.py 420 failed, 66 passed.",
    "Labs: project labs 1-3 twins run alone under python -I -W error with exit 0 and empty stderr; lab 1 and lab 3 page code equals the twin apart from the final newline; lab 2 page code differs from the twin only at the two blank lines; each expected block equals the twin stdout.",
    "Numbers: re-derived independently (ledgers/PC3/scripts/PC3-c-r14/numbers_r14.py): 9 fills, cash flow -9950, inventory 1, mark 9980, P&L 30, max |inventory| 3; counterfactual half-spread 15: 9 fills, P&L 55, change 25. Exemplar sums 49910 and 39960 re-derived. Hours 1+1+3+2+2+4+1 = 14, 28.0 %.",
    "Plan findings: plans/PC3-build-plan.md line 406 (sample count), 407-408 (reference description), 424 (cash identity sign) and 430-432 (copied-log claim) are wrong against the code and the page; line 420-423 is accurate.",
    "Not checked: the self-assessment form (JavaScript, section.rubric-self) beyond page_smoke; a separate in-browser Pyodide run for each learner seed (only the page_smoke run, one seed); the learner's own workspace seed (only seeds 0-49, seed 100 for the count and the page's own seed rules); the older mutant and alternative files (m01-m10, v01-v49, r13, and alternatives from rounds 2-12) were re-run by mutate_graders and carried rather than re-read line by line; L04.html, L06.html and cards.json (other slices; only the sentences the project page cites were read); ruff and mypy over the whole repository (only the PC3 paths and the repository-wide mypy run were run); verify_refs --unit PC3 (the whole-registry offline run was run); the hours estimate is the verifier's own estimate, not a measurement.",
    "Process: the verifier is Haiku 5.5, round 14, slice c; no commit or push; no file under course/, tools/, tests/ or references/ was edited.",
]

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 14,
    "verifier": "independent verifier (Haiku 5.5), round 14, slice c; did not build PC3",
    "pin": "8e5751c",
    "base": "round 13 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round13.json (pin e919577). Delta e919577..8e5751c for slice c: project.html 407, 432, 696; plans/PC3-build-plan.md 420-423 and 430-432; L04.html 65, 72, 83 (outside the slice, cited sentences re-read); ledgers/PC3/mutants r13_01..r13_05 (added, killed).",
    "checkout": str(ROOT),
    "scratch": "ledgers/PC3/scripts/PC3-c-r14/ (every script and output under out/); /tmp/pc3c-r14-* scratch copies",
    "verified_at": "2026-11-08T00:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [{"id": m["id"], "description": m["description"], "killed_by": m["killed_by"]} for m in mut_list],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": (f"PC3-c round 14: verdict {verdict}. Rows {len(rows)}: PASS {counts['PASS']}, FAIL {counts['FAIL']}, "
                f"UNVERIFIABLE {counts['UNVERIFIABLE']}. Mutants {sum(1 for m in mut_list if m['killed_by'])}/{len(mut_list)} killed; "
                f"survivors: {', '.join(survivors)}."),
}
dest = ROOT / "ledgers/PC3/PC3-c.json"
dest.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", dest, counts, verdict)
