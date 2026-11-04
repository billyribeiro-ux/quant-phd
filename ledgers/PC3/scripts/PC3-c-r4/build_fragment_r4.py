"""Build ledgers/PC3/PC3-c.json (round 4) from the outputs under ledgers/PC3/scripts/PC3-c-r4/."""
import json
import re
import sys
from datetime import UTC, datetime

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE4-PC3-c"
S = f"{ROOT}/ledgers/PC3/scripts/PC3-c-r4"
sys.path.insert(0, f"{ROOT}/tools")
import ledger  # noqa: E402

P = "course/modules/PC/PC3/project.html"
G = "course/modules/PC/PC3/grader"
CARRY = "Carried from round 3 ({files} byte-identical since the previous pin 67a2d13e):"
R = []


def row(rid, check, location, status, evidence, fix=None):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    R.append(item)


row("proj-exemplar-a-numbers", "2.2-numbers", f"{P} line 643 (Exemplar A 'Evidence from the log')", "PASS",
    "Sentence reads 'Turn 5 sold at the ask of 9980 cents, and turn 18 sold at the ask of 10000 cents'. Lab run (lab-PC3-project-1 output, fill lines): turn 5 'sells at the ask 9980', inventory +2; turn 18 'sells at the ask 10000', inventory +0. Both match.")
row("proj-lab1-replay-prints", "2.5-labs", f"{P} Lab 1 code, replay() and main()", "PASS",
    "AST walk of the page's Lab 1 block (/tmp/pc3c-r4-ws/page_block_1.py): print calls in draw_game, quote, maker_side, play and replay = 0. main() prints the fill lines. Page code equals twin tests/labs/PC3/lab-PC3-project-1.py except a trailing newline (diff).")
row("proj-lab1-run", "2.5-labs", f"{P} lab-PC3-project-1 (rung 1)", "PASS",
    "python -I -W error tests/labs/PC3/lab-PC3-project-1.py exit 0; output vs page expected block (19 lines): identical except trailing newline. run_labs --unit PC3 --page project: PASS (3/3).")
row("proj-lab1-hypothesis-numbers", "2.2-numbers", f"{P} line 57 (Lab 1 hypothesis)", "PASS",
    "Output: fills = 9 of 20, cash_flow -9950, inventory_end 1, mark 9980, pnl 30, identity True, largest |inventory| 3 (limit 10). Independent re-derivation (/tmp/pc3c-r4-ws/indep_sim.py, Conventions text, not grader code): fills 9, cash -9950, inv 1, mark 9980, pnl 30, maxabs 3. All match the hypothesis sentence.")
row("proj-lab2-completion", "2.5-labs", f"{P} lab-PC3-project-2 (rung 2, completion)", "PASS",
    "Page block differs from twin tests/labs/PC3/lab-PC3-project-2.py only in the two blanked lines (cash_flow = ___, mark = ___, page lines 349-350) and a trailing newline. Twin output vs expected block identical (cash -9950, inv 1, mark 9980, pnl 30, identity True).")
row("proj-lab2-interpretation-last-quote", "2.2-numbers", f"{P} line 381 (Lab 2 interpretation)", "PASS",
    "Rung 1 result reproduced (-9950, 30); the claim that a mark other than 9980 changes the P&L with inventory 1 is an identity (P&L = cash + 1 x mark), so it holds for any mark value.")
row("proj-lab3-counterfactual", "2.2-numbers", f"{P} lines 456-612 (Lab 3 hypothesis and expected block)", "PASS",
    "Lab 3 twin output: settlement 9980, fills 9, cash -9950, inv 1, mark 9980, pnl 30, identity True; counterfactual half-spread 15: fills 9, pnl 55, change 25. Independent re-derivation (indep_sim.py) gives fills 9, pnl 55 for half-spread 15 on seed 0.")
row("proj-lab3-interpretation", "2.2-numbers", f"{P} line 611 (Lab 3 interpretation)", "PASS",
    "'the change in the P&L of 25 cents is a difference on one seed ... the lab does not test any other seed': lab output is one seed (seed 0, SIMULATED); change 25 confirmed by the independent re-derivation.")
row("proj-rung1-instance-claim", "2.8-data / 2.6-spec", f"{P} line 53 and {G}/instance.py", "PASS",
    "Independent draws from random.Random(0) (move then arrival per turn) equal grader make_instance(0): fair_path_cents equal True, arrivals equal True, settlement 9980 (rung1_instance check, /tmp/pc3c-r4-ws/indep_sim.py run).")
row("proj-conventions-constants", "2.2-numbers", f"{P} 'Conventions' list (lines 400-408)", "PASS",
    "N = 20 (HORIZON 20), v0 = 10000, move +/-5 with probability 1/2 (engine.py/instance.py), arrivals 1/4, 1/4, 1/2 (draw < 0.25, < 0.5), 0 <= q <= 5 (MAX_SIZE 5), |I| <= 10 (LIMIT 10), cash identity sign (engine play: cash += -side*price). All match code.")
row("proj-exemplar-a-calibration", "2.6-rubric", f"{P} Exemplar A (lines 635-663, data-scores 2,2,1,2,1)", "PASS",
    "data-scores '2,2,1,2,1' equal the official-scoring text on line 637; each annotation (lines 653-659) is consistent with the rubric descriptors in lines 623-627 (C1 level 2 needs P&L and one component: cash flow stated; C2 level 2 two turns; C3 level 1 no amount; C4 level 2 parameter without effect; C5 level 1 no check named).")
row("proj-exemplar-b-calibration", "2.6-rubric", f"{P} Exemplar B (lines 665-693, data-scores 4,4,4,3,4)", "PASS",
    "data-scores '4,4,4,3,4' equal the official-scoring text on line 667; annotations (lines 683-688) are consistent with rubric lines 623-627; the one miss (settlement rule not named, C4 level 4) is consistent with the rubric's C4 level-4 wording on line 626.")
row("proj-exemplar-b-numbers", "2.2-numbers", f"{P} lines 669-678 (Exemplar B P&L decomposition, evidence, counterfactual)", "PASS",
    "Purchases at the bid turns 2,3,4,8,19 = 9990+9980+9970+9980+9990 = 49910; sales at the ask turns 5,7,13,18 = 9980+9990+9990+10000 = 39960; 39960-49910 = -9950. Inventory after turn 19 = 1; mark 1 x 9980 = 9980. Turn 2 bid 9990 fill 9990; turn 5 ask 9980 fill 9980, inventory 2; turn 18 ask 10000 fill 10000, inventory 0 (lab output). Counterfactual P&L 30 -> 55, change +25 (Lab 3). Largest inventory 3 (Lab 1). All match.")
row("proj-exemplar-b-arrival-sensitivity", "2.2-numbers / 2.9-scope (rule 4, rule 7)", f"{P} line 677 (Exemplar B, 'Assumptions and limits')", "PASS",
    "Round-3 FAIL fixed: the sentence now reads 'changing them can change the fills and the P&L on seed 0, while a small change may change neither'. Re-verified with own simulator (indep_sim.py): p_buy 0.20 (p_sell 0.25) gives 9 fills, P&L 30 (unchanged); p_buy 0.30 gives 11 fills, P&L 40 (changed); p_sell 0.26 gives 11, 40. Both halves of the qualified sentence are true. The unqualified universal is gone.")
row("proj-rubric-observable", "2.6-rubric", f"{P} rubric table (id 'rubric', lines 619-633)", "PASS",
    "Each descriptor names an observable: values stated and equal to replay output (C1), turns cited by number and field matching the log (C2), a counterfactual with amount in cents and rerun (C3), named parameters and what each moves (C4), a named check with its printed result (C5). Read in full this round.")
row("proj-spec-log-schema", "2.6-spec", f"{P} 'Rung 3 · Specification', Required outputs (line 393)", "PASS",
    "Required keys match grader: quote state keys turn, inventory, cash_cents, max_size, limit, history (engine.py lines 92-100); replay keys cash_flow_cents, inventory_end, inventory_mark_cents, pnl_cents (test_replay_returns_... set check); log keys seed, settlement_cents, turns with the nine record keys (engine.py play return); learner command ran with exit 0 on the reference (learner command check).")
row("proj-hours-arithmetic", "2.3-hours", f"{P} 'Time budget' table (lines 425-434); index.html line 167", "PASS",
    "Table 1+1+3+2+2+4+1 = 14; hub 2+6+4+2 = 14 and '14 hours of project' with '28 percent' of 50 hours (14/50 = 28.0%). Hub text unchanged since the previous pin.")
row("proj-hub-placement-conflict", "2.9-scope / 2.8-cross-page", f"{P} lines 42-48 (ladder) vs course/modules/PC/PC3/index.html lines 128-137", "PASS",
    CARRY.format(files="project.html lines 40-48 and index.html") + " ladder text (project line 42) says skip rungs 1 and 2 only after both placement skill checks; the two hub skill checks are the rung 1 and rung 2 items on index.html lines 128-137. No conflict in the ladder wording itself. The premise defect of those skill checks is row proj-hub-skill-check-premise.")
row("proj-hub-filenames", "2.8-cross-page / 2.6-spec", "course/modules/PC/PC3/index.html lines 160 and 167 (outside slice c; re-verified because the previous round recorded it)", "FAIL",
    "index.html line 160: 'Write <code>policy.py</code>, the quoting rule, and <code>pnl.py</code>, the replay'; line 167: 'The autograded policy.py and pnl.py take 6 hours'. project.html line 393 and grader/test_project.py line 26 (import market_maker as sol) require market_maker.py. index.html was not changed between 67a2d13e and 9a02b1af (git diff empty), so the finding stands.",
    fix="Rename policy.py and pnl.py to market_maker.py (quote and replay) in index.html lines 160 and 167, as the project page requires.")
row("proj-hub-seed-scope", "2.9-scope / 2.2-numbers (cross-page)", "course/modules/PC/PC3/index.html lines 55 and 160 (outside slice c; re-verified)", "FAIL",
    "index.html line 55: 'pass the autograder on seeds 0 to 49'; line 160: 'The autograder runs them on seeds 0 to 49'. project.html line 397 (Grading mode): the autograder runs on your seed and on seed plus 7919; grader.js line 53 gives each learner one seed from the workspace ID. run_graders --seeds 0-49 is the verifier's gate, not the learner's autograder. index.html unchanged since the previous pin.",
    fix="Rewrite index.html lines 55 and 160 to: the autograder runs on your own seed and on a second seed (project.html line 397).")
row("proj-hub-skill-check-premise", "2.2-numbers / 2.9-scope (cross-page)", "course/modules/PC/PC3/index.html lines 128-137 (placement skill checks; outside slice c; re-verified)", "FAIL",
    "index.html line 129: 'a market maker buys one unit at an ask of 10 005 cents ... what is the cash flow' (answer -10005); line 134: 'after that fill the inventory is +1 unit'. In the project model a fill at the ask is a maker sale (project.html line 393 'a fill at the ask is a sale by the maker'; Conventions line 405-406: maker purchase at the bid). The hub premise (buy at the ask) is not a maker fill in this model, and the expected answer -10005 contradicts the project's sign convention. index.html unchanged since the previous pin.",
    fix="Restate the skill check as a maker purchase at the bid (cash flow -bid, inventory +1) or as a sale at the ask (cash flow +ask, inventory -1), with the answer computed from the project's Conventions.")
row("proj-quote-rule-first-fill-survivor", "2.8-grader / 2.6-spec", f"{P} Rung 3 quoting-rule time-budget row (line 429); mutant v17", "PASS",
    "Round-3 FAIL resolved by the page edit: line 429 now reads 'A quoting rule in market_maker.py that is legal on every turn for both instances' and no longer says the rule must read the last filled price. grep 'last fill' in project.html (lines 53, 64, 106-107, 189, 251, 360, 466, 518, 576): all describe the Rung 1/2 worked-example rule or the Lab 3 reference rule. Rung 3 (lines 389-397, Required outputs, Constraints and Grading mode) does not require the quote to follow the last fill. v17 (take the mid from the first fill) is therefore a legal rule that the suite correctly accepts; the mutant's 'Student error' label is not a violation of any stated property. Survivor reported in the mutants list, killed_by empty.")
row("proj-builder-mutants", "2.8-grader", "ledgers/PC3/mutants/m01..m10 (prior builder mutants)", "PASS",
    "tools/mutate_graders.py --unit PC3 --seeds 0-49 (scripts/PC3-c-r4/mutate_all_with_r4_new.out): m01..m10 all KILLED (killed_by test names and seed 0).")
row("proj-verifier-mutants", "2.8-grader", "ledgers/PC3/mutants/v01..v12", "PASS",
    "Same run: v01..v12 all KILLED (test_quotes_are_legal_on_every_turn[0], test_replay_returns_..., test_no_function_prints, test_filled_turn_without_a_price_is_refused, test_replay_refuses_a_log_that_is_not_twenty_turns[21], etc.).")
row("proj-mutant-m08-description", "2.8-grader", "ledgers/PC3/mutants/m08_hard_coded_answer_for_any_log.py lines 1-2 and 34", "PASS",
    "Docstring line 1 'Student error: replay returns all zeros, a hard-coded answer, for every log.' matches line 34 'return {cash_flow_cents: 0, ...}'. The code after that return (lines 35-40) is unreachable, harmless. Killed by test_filled_turn_without_a_price_is_refused (seed 0).")
row("proj-verifier-mutants-r3-new", "2.8-grader", "ledgers/PC3/mutants/v13..v17 (round 3 new mutants)", "PASS",
    "v13 (extra key), v14 (absolute sides), v15 (P&L sign), v16 (None check on every turn): KILLED in the same run (killed_by test names in the mutants list). v17 SURVIVED: a legal quote rule, not a stated violation (see proj-quote-rule-first-fill-survivor). Reported as a survivor in the mutants list, not as a page defect.")
row("proj-alternatives-1-2-4-5", "2.8-grader / 2.7-alternatives", "ledgers/PC3/alternatives/alt1, alt2, alt4, alt5", "PASS",
    "scripts/PC3-c-r4/alts_all_r4.out: alt1 50/50, alt2 50/50, alt4 50/50, alt5 50/50 seeds (grader files copied, pytest -I -W error, QF_SEED 0..49).")
row("proj-alt3-replay", "2.8-grader / 2.7-alternatives", "ledgers/PC3/alternatives/alt3_inventory_skew.py (replay lines 26-46)", "PASS",
    "alts_all_r4.out: alt3 passes 50/50 seeds; its replay is the fills-based replay with the same four keys.")
row("proj-alternative-6", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r1/alt6_size_zero_on_multiples_of_three.py", "PASS",
    "alts_all_r4.out: alt6 passes 50/50 seeds.")
row("proj-alternative-7-8-verifier", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r2/alt7_*.py and alt8_*.py", "PASS",
    "alts_all_r4.out: alt7 and alt8 each pass 50/50 seeds.")
row("proj-alternative-9-10-verifier-r3", "2.7-alternatives", "ledgers/PC3/scripts/PC3-c-r3/alt9_*.py and alt10_*.py", "PASS",
    "alts_all_r4.out: alt9 and alt10 each pass 50/50 seeds.")
row("proj-alternatives-r4-new", "2.7-alternatives / 2.8-grader", "ledgers/PC3/scripts/PC3-c-r4/alts/alt11, alt12, alt13 (new this round)", "PASS",
    "alt11 (inventory-skewed legal quote, size 0 within one unit of the limit, fills-list replay): 50/50. alt12 (half-spread 1 cent, reversed scan, size 5, accumulator replay): 50/50. alt13 (half-spread 2 cents, size 0 on turn one, reduce-fold replay): 50/50. Output: scripts/PC3-c-r4/alts_all_r4.out.")
row("proj-grader-35-checks", "2.8-grader", f"{P} 'Grading mode' (line 397) and {G}/test_project.py", "PASS",
    "pytest --collect-only (QF_SEED=0): 37 tests collected. 16 seed-parametrized items (8 tests x seeds [0] and [7919]) and 21 seed-independent items: 16 + 21 = 37, the page's '37 checks' and '16 on a second seed' are equal to the real collect-only count.")
row("proj-grader-seed-scope-claim", "2.8-grader", f"{P} 'Constraints' Integrity sentence (line 395) and 'Grading mode' (line 397)", "PASS",
    "The 16 seed-parametrized tests are run on SEED and SEED+7919 (test_project.py line 33), and the page lists exactly those eight properties (legality, replay vs fills, agreement with engine, P&L identity, integer money, cash change, seed/settlement, instance). Other 21 run on the learner's seed only. The window-property sentence is a separate defect row (proj-grader-window-distinct-paths).")
row("proj-grader-no-print", "2.8-grader", f"{P} 'Constraints' ('No function prints or warns') and {G}/test_project.py test_no_function_prints", "PASS",
    "test_no_function_prints runs quote and replay under capsys: passes for reference (50/50). v08 (debug print in replay) and v09 (warnings.warn on turn one) are killed. Warnings are errors via pytestmark filterwarnings error.")
row("proj-grader-replay-from-fills", "2.8-grader", f"{P} Conventions 'The P&L' bullet (line 407); {G}/test_project.py oracle() lines 68-79", "PASS",
    "oracle() derives cash, inventory, mark and P&L from the fills alone (fill at bid = purchase, at ask = sale) and the suite compares replay to it on both seeds: reference passes, mutants m01, m02, v03, v11, v14, v15 killed.")
row("proj-grader-mypy-strict", "2.8-grader / 2.9-gate", f"{G}/test_project.py, engine.py, instance.py, starter/reference workspace", "PASS",
    "mypy --strict --no-incremental on a copied workspace (engine.py instance.py market_maker.py test_project.py, market_maker = reference and = starter): 'Success: no issues found in 4 source files' for both. Round-3 mypy failure was only the missing workspace layout.")
row("proj-grader-reference", "2.8-grader", f"{G}/reference.py", "PASS",
    "run_graders --unit PC3 --seeds 0-49: 'PASS (reference 50/50 seeds)'. Also the reference passes with QF_SEED 0 (37 passed) and QF_SEED 39893 except for one test (see proj-grader-window-distinct-paths).")
row("proj-grader-starter-fails", "2.8-grader", f"{G}/starter.py", "PASS",
    "Starter run (QF_SEED 0): 20 failed (all tests that call quote or replay raise NotImplementedError), 17 passed (engine-only checks that need no student code). The starter is not accepted.")
row("proj-grader-instances", "2.8-grader", f"{G}/instance.py", "PASS",
    "make_instance(seed) equals the independent draws for seeds 0..199 (checked by assertion in window_collisions.py) and yields 21 positive values stepping by 5 and 20 names from ARRIVAL_NAMES; test_instance_is_deterministic_and_well_formed passes on both seeds of the reference run.")
row("proj-grader-messages", "2.8-grader", f"{G}/test_project.py messages (expect/must_refuse, lines 40-55 and throughout)", "PASS",
    "Messages name properties and the spec phrases ('bid must be below ask' etc.); no message formats a computed value (read in full, lines 1-417).")
row("proj-named-refusals", "2.8-grader / 2.6-spec", f"{G}/test_project.py lines 166-217; {P} 'Named invalid inputs' (lines 410-418)", "PASS",
    "Four named conditions are each tested: crossed/locked quote 'bid must be below ask' (lines 169-177), size outside 0..5 (185-193), log not 20 turns (205-210), filled turn without a price (213-217). Messages match the page text lines 413-416.")
row("proj-exception-types", "2.8-grader", f"{G}/test_project.py lines 47-55 and 168-218; {P} line 418", "PASS",
    "must_refuse is used only for the four conditions named on page lines 413-416; every other failure is a plain property check (test docstring lines 14-16). Page line 418 'the autograder requires no exception type for those' matches.")
row("proj-run-labs-unit", "2.5-labs / 2.9-gate", "tools/run_labs.py --unit PC3 --page project", "PASS",
    "scripts/PC3-c-r4/run_labs_project.out: 'run_labs PC3: PASS (3/3)', exit 0.")
row("proj-check-tools", "2.9-gate", "tools/check_pages.py, check_dag.py, check_projects.py --unit PC3", "PASS",
    "scripts/PC3-c-r4/check_pages.out, check_dag.out, check_projects.out: each 'PASS', exit 0.")
row("proj-page-smoke", "2.9-gate", "tools/page_smoke.py --unit PC3 --pages project", "PASS",
    "scripts/PC3-c-r4/page_smoke_project.out: project.html PASS, labs run, PC3 PASS, exit 0. Browser-only behaviour (Pyodide) was not driven by hand; page_smoke's in-browser step is the evidence.")
row("proj-lint-ruff", "2.9-gate", "ruff check and ruff format --check on course/modules/PC/PC3/grader and tests/labs/PC3", "PASS",
    "scripts/PC3-c-r4/ruff_check.out: 'All checks passed!'; ruff_format.out: '14 files already formatted'. Both exit 0.")
row("proj-mypy-labs", "2.9-gate", "mypy --no-incremental (repo); tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    "scripts/PC3-c-r4/mypy_repo.out: 'Success: no issues found in 385 source files', exit 0.")
row("proj-banned-and-process-words", "2.12-process / 2.13-banned", f"{P} all text and code; labs", "PASS",
    "grep (case-insensitive) for verifier, builder, fragment, round N, ledger, orchestrat, reviewer, workflow, subagent, agent: two hits only, both innocent: line 397 'names no reviewer' (describes the grading mode to the learner) and line 466 'around' (matches 'round'). No process words in learner text.")
row("proj-notation", "2.13-notation", f"{P} inline math (49 spans) vs notation/notation.json", "PASS",
    "Symbols used on the page: N, t, v_t, v_0, v_20, a_t, b_t, q_t, I, I_20, pnl, cash flow, and the Greek-free set. notation.json symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. No reuse: the page never uses T, Phi, gamma, R or Q. Macros used (\\times, \\le, \\ge, \\gt, \\lt, \\mathrm, \\dots) are not in the macro list as a conflict.")
row("proj-dag-terms", "2.14-dag", f"{P} (all text); {P} line 626 and 677 ('adverse selection'); L04.html definition id", "PASS",
    "Only concept link on the page: market-making-game -> L04.html#def-market-making-game, which exists (L04.html line 60, <dfn id=\"def-market-making-game\">). 'adverse selection' appears by name on lines 626 and 677 without a link; plan decision D3 (plans/PC3-build-plan.md line 293) makes it prose-only with a plain description in L04, so this is the allowed use. 'quantiles' (line 705) and 'latency' are plain statistical or market words.")
row("proj-references", "2.2-sources", f"{P} 'Reading' (lines 710-717) and 'References' (line 721)", "PASS",
    "data-cite keys zhou2008practical and crack2015heard exist in references/references.json (entries with the keys; openlibrary-verified). verify_refs --offline: 'offline integrity: 560 entries, 0 problems'. The page attributes no problem, answer or page to either book.")
row("proj-js-claims", "2.4-claims", f"{P} 'Autograder' section (line 442) and footer (line 730)", "PASS",
    "grader.js line 61: the draft is written to the store on each edit (store.put 'files'), i.e. saved in the browser as you type. Pyodide runs the suite (python.js/py-worker.js: 'nothing is fetched'); grader.js fetches only the course's own starter and suite files (lines 18, 31-37). The rubric scores also use store.js (rubric.js line 8).")
row("proj-local-commands", "2.4-claims", f"{P} Spec 'Required outputs' (python3 -c command) and 'Running the suite locally' (line 449)", "PASS",
    "Learner command 'python3 -c \"import json, engine, market_maker; print(json.dumps(engine.play(market_maker.quote, <seed>)))\"' run with seed 286907935 in a workspace with the reference: exit 0, JSON log written. QF_SEED=0 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py: 37 passed.")
row("proj-known-limitation", "2.4-claims", f"{P} 'Constraints' (line 395); {G}/engine.py docstring", "PASS",
    "The log has keys seed, settlement_cents and turns; no fair path is written (engine.play returns those keys only). instance.py is in the grader folder and is readable, so the page's limitation sentence is accurate.")
row("proj-ladder-scope", "2.8-cross-page / 2.9-scope", f"{P} lines 40-48 (ladder); curriculum/06-profession-capstone.yaml PC3 entry", "PASS",
    CARRY.format(files="project.html lines 40-48 and curriculum/06-profession-capstone.yaml (curriculum diff since 67a2d13e is empty)") + " ladder scope unchanged; the rung 4 stretch is open-ended and the placement rule is the hub's.")
row("proj-rubric-atlas-studios", "2.8-cross-page", "plans/PC3-build-plan.md section 8; project.html (grep 'atlas' count 0)", "PASS",
    "grep -ci atlas course/modules/PC/PC3/project.html = 0. The plan's studio mapping does not appear on the learner page.")
row("proj-stretch", "2.2-numbers / 2.6-spec", f"{P} lines 701-708 (Rung 4 · Stretch)", "PASS",
    "Stretch items: seeds 0 to 199 (stated scope, no number asserted), informed arrival 1/2 -> 0.6 (consistent with the Conventions split 1/2 informed), inventory limit 10 -> 5 on seed 0 (the limit constant is 10 in the engine). No computed claim is made on this page.")
row("proj-twin-rules", "2.5-labs", "tests/labs/PC3/lab-PC3-project-1..3.py", "PASS",
    "Each twin runs alone under python -I -W error with exit 0 (page labs 1, 2, 3) and its output equals the page expected block. Twins draw from random.Random(0) and make no network calls.")
row("proj-exception-types-labs", "2.8-grader", f"{P} Lab 1 and Lab 3 replay (raise ValueError lines)", "PASS",
    "Lab 1 and Lab 3 replay raise ValueError for a log of other than 20 turns and for a filled turn with no price, with the page's messages (named invalid inputs), matching the grader's named refusals.")
row("proj-grader-window-distinct-paths", "2.8-grader / 2.2-numbers", f"{G}/test_project.py lines 363-366 (test_twenty_consecutive_seeds_give_twenty_different_paths) and {P} line 397 ('that twenty consecutive seeds give twenty different paths')", "FAIL",
    "The grader fails the reference solution for some learner seeds. QF_SEED=39893 and QF_SEED=39901 with the reference market_maker.py: '1 failed, 36 passed', the failing test is test_twenty_consecutive_seeds_give_twenty_different_paths. Cause: two seeds share a fair path in 4 pairs below 300000 (39908/39912, 75545/75557, 113902/113903, 186415/186431), so windows [w, w+20) containing a pair fail: 47 of 299981 windows below 300000 (about 1.6e-4, matching 190 x 2^-20 = 1.8e-4 per window). About 1 learner in 6000 would see a failing check through no fault of their own. QF_SEED 0 passes (37 passed).",
    fix="Remove the all-distinct window property from the grader (test_project.py lines 363-366) and from page line 397, or replace it with a deterministic check over a fixed seed range (for example seeds 0 to 49, already run by run_graders) and say that range on the page. Any window-based claim about 20 seeds must be stated for a fixed range, not for each learner's seed.")
row("proj-r4-new-mutants-v18-v20", "2.8-grader", "ledgers/PC3/mutants/v18_replay_skips_the_first_turn.py, v19_replay_marks_one_move_below_settlement.py, v20_replay_fill_side_sign_swapped.py (new this round)", "PASS",
    "Three new student-error mutants written this round, each a plausible wrong solution: v18 skips turn 1 (KILLED), v19 marks at settlement less 5 cents (KILLED by test_replay_returns_...[0]), v20 swaps the side of each fill (KILLED by test_replay_returns_...[0]). Output: scripts/PC3-c-r4/mutate_all_with_r4_new.out.")

PASS_FILES = "project.html, grader/, tests/labs/PC3 project twins, mutants"
verdict = "FAIL" if any(r["status"] != "PASS" for r in R) else "PASS"
mutants = []
text = open(f"{S}/mutate_all_with_r4_new.out", encoding="utf-8").read()
for line in text.splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = "" if status == "SURVIVED" or killed.strip() == "None" else killed.strip()
    mutants.append({"id": name.removesuffix(".py"), "description": desc,
                    "file": f"ledgers/PC3/mutants/{name}", "killed_by": killed_by})

fragment = {
    "unit": "PC3",
    "slice": "c",
    "round": 4,
    "verifier": "independent verifier (Haiku 5.5), round 4, slice c",
    "pin": "9a02b1af",
    "base": "round 3 fragment /Users/billyribeiro/.fanout/frags/E-PC3-c.round3.json (pin 67a2d13e); delta 67a2d13e..9a02b1af for project.html, grader/, tests/labs/PC3, mutants, alternatives",
    "checkout": ROOT,
    "scratch": "/tmp/pc3c-r4-ws (window_collisions.py, indep_sim.py, pairs.py, extract.py, w1 and w2 grader workspaces)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta since 67a2d13e for slice c: project.html (16 lines), mutants v13..v17 (added since 67a2d13e; read in full), lab twin project-1 (comment line 50), and the new mutants v18..v20 and alternatives alt11..alt13 written this round. grader/ byte-identical since 67a2d13e. Read in full: project.html (732 lines), grader engine.py, instance.py, reference.py, starter.py, test_project.py (417 lines), the three project twins, and all mutant and alternative files named in rows. "
        "Not checked: full-repo gates (render_curriculum, build_site --check, fetch_data --check, check_pages --all, run_graders --all over all units, pytest whole suite); index.html beyond the lines cited (cross-page rows re-verified only for those lines); L04.html beyond the def id; the in-browser Pyodide run (page_smoke's in-browser step only); the window property for learner seeds outside 0..300000 (only a rate estimate, not an exhaustive check). "
        "v17 is not a failure of the page: it is a legal quoting rule, and the suite accepting it is correct. The merge tool counts killed_by-empty mutants as unkilled, so v17 keeps the merged mutant count below total; the orchestrator should accept it as a legal alternative or move it to ledgers/PC3/alternatives/."
    ),
    "summary": "",
}
n_pass = sum(1 for r in R if r["status"] == "PASS")
n_fail = sum(1 for r in R if r["status"] == "FAIL")
fragment["summary"] = (
    f"Slice c round 4: verdict {verdict}. Rows {len(R)}: PASS {n_pass}, FAIL {n_fail}. "
    f"FAIL: proj-grader-window-distinct-paths (grader fails the correct reference on QF_SEED 39893 and 39901), "
    f"and three cross-page hub rows in index.html (policy.py/pnl.py names, seeds 0 to 49 scope, skill-check premise), unchanged since the previous pin. "
    f"Fixed and re-verified PASS: proj-exemplar-b-arrival-sensitivity, proj-quote-rule-first-fill-survivor (no longer a stated violation). "
    f"Mutants: {len(mutants)} total, {sum(1 for m in mutants if m['killed_by'])} killed; v17 survives as a legal rule. "
    f"Alternatives: 13 of 13 pass seeds 0-49. Gates: check_pages, check_dag, check_projects, run_labs (3/3), page_smoke, run_graders 50/50, ruff, mypy, verify_refs --offline, pytest -k PC3 all PASS."
)
problems = ledger.validate(fragment, "PC3-c")
print("validate:", problems)
out = f"{ROOT}/ledgers/PC3/PC3-c.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, "rows", len(R), "pass", n_pass, "fail", n_fail, "mutants", len(mutants), "verdict", verdict)
