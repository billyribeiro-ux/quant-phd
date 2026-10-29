"""Build the round-20 fragment for AC4 slice c from the round-19 fragment and this round's re-checks.

Carried rows keep their round-19 check and their round-19 evidence, prefixed as the brief requires, and only
where the cited subject is outside the changed lines (L05.html 97, 254, 311; L06.html 276).
Re-verified rows get new evidence from this round's commands and reads.
Usage: build_fragment_r20.py <checkout> <round19-fragment>
"""
from __future__ import annotations

import datetime
import json
import pathlib
import sys

checkout = pathlib.Path(sys.argv[1])
prev = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))

CARRY = "Carried from round 19 (course/modules/AC/AC4/L05.html and L06.html: cited lines byte-identical since the previous pin; changed lines are L05 97, 254, 311 and L06 276, none cited here): "

NEW = {
    "AC4-c-cmd-check-pages": ("tools/check_pages.py --all", "tools/check_pages.py", "PASS", "Round 20 (pin fd9a9b7): .venv/bin/python tools/check_pages.py --all exit 0; output lines for AC4 include 'check_pages AC4: PASS' (/tmp/AC4-c-v20/check_pages.out)."),
    "AC4-c-cmd-check-dag": ("tools/check_dag.py --all", "tools/check_dag.py", "PASS", "Round 20: tools/check_dag.py --all exit 0; 'check_dag AC4: PASS' (/tmp/AC4-c-v20/check_dag.out)."),
    "AC4-c-cmd-check-projects": ("tools/check_projects.py --all", "tools/check_projects.py", "PASS", "Round 20: tools/check_projects.py --all exit 0; 'check_projects AC4: PASS' (/tmp/AC4-c-v20/check_projects.out)."),
    "AC4-c-cmd-run-labs": ("tools/run_labs.py --unit AC4", "tools/run_labs.py", "PASS", "Round 20: tools/run_labs.py --unit AC4 exit 0; 'run_labs AC4: PASS (10/10)' (/tmp/AC4-c-v20/run_labs.out)."),
    "AC4-c-twins-run": ("python -I -W error run of each twin", "tests/labs/AC4/lab-AC4-L05-1.py; tests/labs/AC4/lab-AC4-L06-1.py", "PASS", "Round 20: both twins exit 0 with 0 stderr bytes under python -I -W error (run dirs /tmp/AC4-c-v20/run-L05, run-L06); L05 prints 17 lines, L06 prints 16 lines; both match the embedded output via run_labs."),
    "AC4-c-page-smoke": ("tools/page_smoke.py --unit AC4 --pages L05.html L06.html", "tools/page_smoke.py", "PASS", "Round 20: exit 0, 'page_smoke AC4: PASS' (/tmp/AC4-c-v20/page_smoke.out)."),
    "AC4-c-lint-types-pytest": ("ruff check, ruff format --check, mypy --no-incremental on both twins; pytest tests/test_labs.py", "tests/labs/AC4/lab-AC4-L05-1.py; tests/labs/AC4/lab-AC4-L06-1.py", "PASS", "Round 20: 'All checks passed!' (ruff check); '2 files already formatted'; mypy 'Success: no issues found in 2 source files'; pytest tests/test_labs.py exit 0."),
    "AC4-c-citations": ("tools/verify_refs.py --offline; tools/verify_refs.py --unit AC4; grep for registry keys in both pages", "course/modules/AC/AC4/L05.html; course/modules/AC/AC4/L06.html", "PASS", "Round 20: offline 'integrity: 560 entries, 0 problems' (exit 0); live '--unit AC4: 2 of 560 entries, 0 problems' (exit 0). Neither page cites a registry key: L05 and L06 references sections read 'This lesson cites no registry source' (L05.html line 466, L06.html line 495) with an empty data-references list."),
    "AC4-c-numbers": ("recomputed every number in the changed prose from the twin inputs", "course/modules/AC/AC4/L05.html lines 97, 254, 311; course/modules/AC/AC4/L06.html line 276; rest of both pages carried", "PASS", "Round 20 recomputation: master contribution 600*1500+400*1900 = 1,660,000 on 1,000 units (lab prints master_contribution 1660000), so 1,660 per unit; 150*1660 = 249,000; 265,000-249,000 = 16,000; mix at budget shares 690*1500+460*1900 = 1,909,000 and 1,925,000-1,909,000 = 16,000; flexed 1,425,000; static 140,000; flexible -125,000. All match the printed twin output."),
    "AC4-c-grades": ("re-read Prop 2.1/2.2 grades and key-results table", "course/modules/AC/AC4/L05.html Prop 2.1 and 2.2; course/modules/AC/AC4/L06.html Prop 2.1 and 2.2", "PASS", "Round 20: the changed lines are not claims or grade attributes; Prop 2.1 (L05 line 67 block) and Prop 2.2 (L05 line 77) still carry data-grade=\"T\". Carried from round 19 for the grade attributes, re-read this round."),
    "AC4-c-banned-phrases": ("grep of both pages' visible prose and both twins for BUILDER_RULES 1.2/1.3 strings and scope words", "course/modules/AC/AC4/L05.html; course/modules/AC/AC4/L06.html; tests/labs/AC4/lab-AC4-L05-1.py; tests/labs/AC4/lab-AC4-L06-1.py", "PASS", "Round 20: no TODO/TBD/lorem/'for brevity'/'beyond the scope'/'roughly'/'historically'/'about <digit>'/'it can be shown'/'it is important to note'. Ellipses found (L05 lines 148, 164, 175; L06 lines 167, 185, 190 and the twins) are Python code or math (\\dots), not omitted content. New sentences (L05 97, 254; L06 276) contain no banned string."),
    "AC4-c-structure": ("count h2 sections and template sections in both pages", "course/modules/AC/AC4/L05.html sections 1-10; course/modules/AC/AC4/L06.html sections 1-9", "PASS", "Round 20: <h2 id=\"s1\"> to <h2 id=\"s10\"> in L05 (10 h2) and s1 to s9 in L06 (9 h2); the four changed lines are <p> lines (git diff -U0 51fa336 fd9a9b7), so no heading, class or quiz markup moved."),
    "AC4-c-math-L05": ("re-derive Prop 2.1 proof and P1 solution after the round-19 fix", "course/modules/AC/AC4/L05.html Prop 2.1 (lines 67-72), Prop 2.2 (lines 77-82), P1 (lines 309-312), P2 (line 318), P3", "PASS", "Round 20 re-derivation of the changed P1 solution (L05.html line 311): the claim is Pi_m = Pi_b(q_b) with Pi_b(q) = sum_i (p_i - c_i) q_i - F. Definition 1.1 (line 49) defines the master budget as the plan built from the budgeted units, prices, standard costs and fixed costs, which is exactly the evaluation of the budget rules at budgeted inputs. Prop 2.1's statement (line 67 block) defines Pi_b as that budget operating profit at units q. The second fact the solution now cites is one function at one argument gives one value, which is not a premise about input values. The solution names two facts and no third premise, so the round-19 FAIL is resolved. Numeric check: 600*1500 + 400*1900 - 500,000 = 1,160,000 = master budget (lab prints master_operating_profit 1160000); Pi_b at actual units 650, 500 gives 1,425,000 (lab prints flexed_operating_profit 1425000). Prop 2.2 (line 77-82) and P2 (line 318) unchanged and re-derived: (Pi_f - Pi_m) = 265,000 = sum CM_i(q_a,i - q_b,i) = 1500*50 + 1900*100 = 265,000."),
    "AC4-c-math-L06": ("re-derive Prop 2.1/2.2 and the Section 4 bullet 1 statement", "course/modules/AC/AC4/L06.html Prop 2.1 (lines 78-79) and proof (83-88); Prop 2.2 and proof (92-98); Section 4 bullet 1 (line 279)", "PASS", "Carried from round 19 (course/modules/AC/AC4/L06.html lines 78-98 byte-identical since the previous pin): the round-19 derivation stands. Locator correction this round: Section 4 bullet 1 is at line 279 (round 19 wrote 270, a stale round-18 number). Its fifth-term statement is unchanged; the four bullets are at lines 279-282 and the changed line 276 introduces them."),
    "AC4-c-L05-hypothesis-causal": ("re-read the changed Lab 1 hypothesis at L05.html line 97 against the twin output", "course/modules/AC/AC4/L05.html line 97 (Lab 1 hypothesis)", "PASS", "Round 20: the changed sentence is 'On the convention that each extra unit earns the budget average contribution of 1,660 cents per unit (1,660,000 cents on 1,000 budgeted units, as the lab prints), the 150 extra units account for 249,000 cents of the 265,000 cents of volume-and-mix part, and the shift in mix toward B accounts for the other 16,000 cents.' Checked: lab prints master_contribution 1660000 and volume_and_mix_variance 265000; 150*1660 = 249,000; 265,000-249,000 = 16,000 = check of mix at budget shares (1,925,000 - 1,909,000). The 'on the convention' qualifier is what makes 'account for' a stated assumption rather than a finding. Mix is positive because actual B units 500 exceed the 460 B units at budget share of 1,150 (lab sales_mix_variance 16000)."),
    "AC4-c-L05-s5-volume-term": ("re-read Section 4 bullets and the Section 5 paragraph at L05.html line 254", "course/modules/AC/AC4/L05.html Section 4 bullets (lines 246-248) and Section 5 paragraph (line 254)", "PASS", "Round 20: the changed line 254 now reads 'Section 4 sets out three limits.' Section 4 has exactly three <li> bullets (L05.html lines 246, 247, 248: relevant range, split of mixed costs, standard is an assumption). The earlier 'a fourth applies here' is gone and no sentence on the page refers to a fourth limit (grep 'fourth' returns no match in L05 or L06). The paragraph's statement that a flexed budget removes the volume-and-mix effect matches bullet 3 (line 248)."),
    "AC4-c-L05-round7-edits": ("re-read the round-7 edit lines including line 254", "course/modules/AC/AC4/L05.html lines 49, 67, 77-78, 251-254, 372-375, 464-470", "PASS", "Round 20: lines 49, 67, 77-78 and 372-375, 464-470 unchanged (git diff -U0 51fa336 fd9a9b7 shows hunks only at 97, 254, 311); line 254 re-read as above: 'Section 4 sets out three limits.' matches the three bullets."),
    "AC4-c-r17-prose-rescan": ("re-read the visible prose ranges including changed lines 97, 254 and 276", "course/modules/AC/AC4/L05.html lines 43-254, 262-271, 336, 350; course/modules/AC/AC4/L06.html lines 52-108, 259-291, 318-398", "PASS", "Round 20 rescan of the changed sentences only, against the rest of the ranges (carried). L05 97: checked numerically above. L05 254: checked against the three bullets. L06 276: 'Four limits are set out below.' followed by four <li> bullets at lines 279-282. No new scope word lacks a computation: 'account for' (L05 97) is inside the 'on the convention' clause; 'set out below' (L06 276) is a count of four bullets."),
    "AC4-c-r17-lab-claims": ("re-check lab-output claims including L05.html line 97", "course/modules/AC/AC4/L05.html line 97 and 238, 263, 267, 271; course/modules/AC/AC4/L06.html line 112, 119-120, 259; tests/labs/AC4/lab-AC4-L05-1.py line 191-197; lab-AC4-L06-1.py line 119-120, 140-141, 231-241", "PASS", "Round 20: line 97 says 'Lab 1 prints that 265,000 as one figure' and the twin prints volume_and_mix_variance 265000 once (L05 output); 'Lesson L06, Lab 1, computes the two parts ... and prints them separately' matches L06 output lines sales_volume_variance 249000 and sales_mix_variance 16000. Other cited lines carried, unchanged."),
    "AC4-c-r18-L05-hypothesis-1660-average": ("re-check the 1,660 average convention wording at L05.html line 97", "course/modules/AC/AC4/L05.html line 97; tests/labs/AC4/lab-AC4-L05-1.py output master_contribution 1660000", "PASS", "Round 20: lab output master_contribution 1660000 (run /tmp/AC4-c-v20/run-L05/out.txt); 1,660,000 on 1,000 budgeted units gives 1,660 per unit; the new sentence states the average as a convention, not as a finding."),
    "AC4-c-r18-scope-rescan": ("scope-word rescan of visible prose of both pages", "course/modules/AC/AC4/L05.html and L06.html visible prose", "PASS", "Round 20: word-boundary scan for only, all, always, as much as, same, drives, offsets, raises, ellipsis (Python script over tags-stripped lines). Hits inspected: L05 'only' (line 403, quiz option), 'offsets' (line 336, flexible variance offsets part of the static variance, carried), 'all' (lines 93, 422: 'All money is in integer cents' and quiz option); L06 'only' (lines 239, 268, 340, 363), 'raises' (141, 268), 'always' (line 470, quiz option), 'all' (292: 'it is all mix', with the computed example at line 292). Changed sentences checked as in the rows above. No hit lacks a computation or a stated scope."),
    "AC4-c-lab-L05-output": ("run the L05 twin and compare with the page output; re-check the changed hypothesis line", "tests/labs/AC4/lab-AC4-L05-1.py; course/modules/AC/AC4/L05.html lines 93-241", "PASS", "Round 20: run_labs AC4 PASS (10/10); isolated twin run exit 0, 0 stderr bytes, 17 lines (/tmp/AC4-c-v20/run-L05/out.txt), identical to the embedded output; line 97 is the hypothesis paragraph (checked above)."),
    "AC4-c-lab-L06-output": ("run the L06 twin and compare with the page output", "tests/labs/AC4/lab-AC4-L06-1.py; course/modules/AC/AC4/L06.html lines 110-261", "PASS", "Round 20: run_labs AC4 PASS (10/10); isolated twin run exit 0, 0 stderr bytes, 16 lines (/tmp/AC4-c-v20/run-L06/out.txt), matching the embedded output. The changed line 276 is outside this range."),
    "AC4-c-r18-mutants-rerun": ("re-run every earlier AC4-c mutant and alternative", "ledgers/AC4/mutants/AC4-c-r7, AC4-c-r8, AC4-c-r17, AC4-c-r18, AC4-c-r19; ledgers/AC4/scripts/AC4-c-r20/run_all_mutants.py", "PASS", "Round 20 re-run of every file under ledgers/AC4/mutants/AC4-c-r* (scripts/AC4-c-r20/out/r20_all_mutants.out): 59 files, of which 25 ERR (residual ValueError or AssertionError) and 28 DIFF (exit 0, stdout differs from the embedded output) are killed; 6 are SAME: 5 correct alternatives (alt07, alt_r18_c, alt_r20_a, alt_r20_b, alt_r20_c) and r19_m05. The alternatives that DIFF (r7 alt01, r8 alt01-05, r17 alt06, alt08, r18 alt_a, alt_b, and the equivalent-claimed r17 ne06, ne07 and r18 m06) differ from the baseline only by omitting the two printed per-product sales-price lines (sales_price_variance_A/B); every other printed value matches. Lab-twin mutants are out of scope by the architect ruling; none is a grader."),
    "AC4-c-r18-new-mutants": ("re-run r18 mutants", "ledgers/AC4/mutants/AC4-c-r18/r18_m01..m05", "PASS", "Round 20 re-run: r18_m01, m02, m03 ERR (residual or non-whole-cent ValueError); m04 and m05 DIFF (exit 0, stdout differs). All killed."),
    "AC4-c-r18-equivalent-proof": ("re-run the equivalence-claimed mutants", "ledgers/AC4/mutants/AC4-c-r18/r18_m06_L06_allowance_floor_equivalent.py; ledgers/AC4/mutants/AC4-c-r17/ne06, ne07", "PASS", "Round 20 re-run: each exits 0; the only stdout difference from the baseline is the omission of the two sales_price_variance_A/B lines; all printed totals equal the baseline. Equivalent for the printed values; out of scope for a lab twin."),
    "AC4-c-r18-alt-impl-3": ("re-run the r18 alternatives", "ledgers/AC4/mutants/AC4-c-r18/alts/alt_r18_a, alt_r18_b, alt_r18_c", "PASS", "Round 20 re-run: alt_r18_c SAME (exit 0, identical stdout); alt_r18_a and alt_r18_b exit 0 with identical totals and the two per-product lines omitted (the only difference)."),
    "AC4-c-r19-new-mutants": ("re-run r19 mutants m01-m04", "ledgers/AC4/mutants/AC4-c-r19/r19_m01..m04", "PASS", "Round 20 re-run: r19_m01 DIFF, m02 ERR (residual), m03 DIFF, m04 ERR (AssertionError). All killed."),
    "AC4-c-r19-m05-decompose-only-survivor": ("re-run r19_m05 and check whether a lesson sentence claims the lab checks the decomposition", "ledgers/AC4/mutants/AC4-c-r19/r19_m05_L06_sales_price_budget_units_in_decompose_only.py; course/modules/AC/AC4/L06.html line 268", "PASS", "Round 20 re-run: exit 0, stdout identical to the baseline. Out of scope per the architect ruling: the lesson sentence at L06.html line 268 claims only that the lab raises an error when the four variances do not reconcile, and the mutant still reconciles on the case printed (the mutated function does not change any printed or residual value). No FAIL."),
}


LOCATOR_FIX = {
    "AC4-c-L06-P1-step-reason": ("course/modules/AC/AC4/L06.html P1 solution (line 340, 'Step 1 writes the actual revenue ...')", "round 19 cited line 331, which is blank"),
    "AC4-c-L06-R1-unanswered": ("course/modules/AC/AC4/L06.html R1 solution (Research tier, lines 389-390)", "round 19 cited lines 378-381, which are the E3 solution and the E3 block"),
    "AC4-c-L06-R3-standard": ("course/modules/AC/AC4/L06.html R3 (lines 401-405)", "round 19 cited lines 392-395, which are R2 text"),
    "AC4-c-L06-E1-static-variance": ("course/modules/AC/AC4/L06.html E1 prompt (line 363) against E1 solution (line 365)", "round 19 cited line 354 (P3 solution) and 356 (blank)"),
    "AC4-c-L06-operating-variance-term": ("course/modules/AC/AC4/L06.html E1 prompt (line 363)", "round 19 cited line 354"),
    "AC4-c-L06-P3-r8": ("course/modules/AC/AC4/L06.html line 345 (P2 prompt, 'Show that if the actual units are split in the budget shares ...') and P3 (lines 351-354)", "round 19 labelled line 345 as P3; line 345 is the P2 prompt"),
    "AC4-c-L06-q4-sufficient": ("course/modules/AC/AC4/L06.html line 449 (prompt 'Which sufficient condition makes the sales mix variance zero?') and options 451-453", "round 19 cited prompt line 440 and options 442-444"),
    "AC4-c-L06-honest-pending-r7": ("course/modules/AC/AC4/L06.html references lines 494-496 and honest pending line 499", "round 19 cited lines 484-486 and 490"),
    "AC4-c-L06-section1-ref": ("course/modules/AC/AC4/L06.html line 52, Section 1 (line 56), Section 4 heading (line 274)", "round 19 cited Section 4 heading at line 265"),
    "AC4-c-L06-interp-sentences": ("course/modules/AC/AC4/L06.html line 268 (interpretation after the lab)", "round 19 cited line 259, which is lab output 'sales_mix_variance 16000'"),
    "AC4-c-r18-L06-def12-model-scope": ("course/modules/AC/AC4/L06.html line 65; course/modules/AC/AC4/L05.html line 54 (Definition 1.2 model scope); tests/labs/AC4/lab-AC4-L05-1.py lines 19-22", "round 19 cited L05 line 63, which is blank"),
    "AC4-c-r18-P2-stale": ("", ""),
}
LOCATOR_FIX.pop("AC4-c-r18-P2-stale")


def carried(row: dict) -> dict:
    rid = row["id"]
    if rid in NEW:
        check, loc, status, ev = NEW[rid]
        out = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
        if rid == "AC4-c-math-L06":
            out["evidence"] = ev
        return out
    loc = row["location"]
    ev = CARRY + row["evidence"]
    if rid in LOCATOR_FIX:
        new_loc, why = LOCATOR_FIX[rid]
        ev = CARRY + f"Locator corrected in round 20 ({why}): " + row["evidence"]
        loc = new_loc
    return {"id": rid, "check": row["check"], "location": loc, "status": row["status"], "evidence": ev}


NEW_ROWS = [
    {"id": "AC4-c-r20-delta", "check": "git diff -U0 51fa336 fd9a9b7 on this slice",
     "location": "course/modules/AC/AC4/L05.html hunks at lines 97, 254, 311; course/modules/AC/AC4/L06.html hunk at line 276; tests/labs/AC4, cards.json, tools/ unchanged",
     "status": "PASS",
     "evidence": "git diff --stat 51fa336 fd9a9b7 -- course/modules/AC/AC4 tests/labs/AC4: L01, L02, L07, L08 (other slices) and L05 (3 lines), L06 (1 line) changed; the twins, cards.json and tools/ are not in the delta. Each hunk is a one-for-one replacement (16 insertions, 16 deletions across the six files), so no other line number moved."},
    {"id": "AC4-c-r20-P1-fact-count", "check": "round-19 FAIL: P1 solution names one fact or two",
     "location": "course/modules/AC/AC4/L05.html line 311 (P1 solution); line 49 (Definition 1.1); line 67 block (Prop 2.1)",
     "status": "PASS",
     "evidence": "P1 now names two facts: Definition 1.1 (line 49: the master budget combines budgeted units, prices, standard costs and fixed costs into operating profit) and 'one function evaluated at one argument gives one value'. The solution's only premises are these two and the definition of Pi_b in the Prop 2.1 statement; the second fact is not a premise about input values. The round-19 FAIL row is resolved on this text."},
    {"id": "AC4-c-r20-L05-s4-three-limits", "check": "line 254 'Section 4 sets out three limits' against Section 4",
     "location": "course/modules/AC/AC4/L05.html line 254; Section 4 bullets at lines 246-248",
     "status": "PASS",
     "evidence": "Section 4 has exactly three <li> bullets (lines 246, 247, 248). Line 254 now says three limits, and the 'fourth applies here' clause is gone; grep for 'fourth' in L05 and L06 finds none."},
    {"id": "AC4-c-r20-L06-four-limits", "check": "line 276 'Four limits are set out below' against Section 4",
     "location": "course/modules/AC/AC4/L06.html line 276; Section 4 bullets at lines 279-282",
     "status": "PASS",
     "evidence": "Four <li> bullets follow at lines 279, 280, 281, 282 (actual material price; one material; standard sets both sides; reference point). The round-19 phrase 'follow from them' is replaced by 'are set out below', which is a count and not a causal claim."},
    {"id": "AC4-c-r20-lab-counts", "check": "run both twins under python -I -W error and compare with page output",
     "location": "tests/labs/AC4/lab-AC4-L05-1.py; tests/labs/AC4/lab-AC4-L06-1.py; tools/run_labs.py --unit AC4",
     "status": "PASS",
     "evidence": "run_labs AC4: PASS (10/10). Isolated runs exit 0, stderr 0 bytes: L05 17 lines, L06 16 lines (/tmp/AC4-c-v20/run-L05/out.txt, run-L06/out.txt)."},
    {"id": "AC4-c-r20-mutants-rerun", "check": "re-run every AC4-c mutant and alternative (r7, r8, r17, r18, r19, r20)",
     "location": "ledgers/AC4/mutants/AC4-c-r7..r20; ledgers/AC4/scripts/AC4-c-r20/run_all_mutants.py; ledgers/AC4/scripts/AC4-c-r20/out/r20_all_mutants.out",
     "status": "PASS",
     "evidence": "59 files: 25 ERR, 28 DIFF (all killed: non-zero exit or stdout differing from the embedded output), 6 SAME. The 6 SAME are 5 correct alternatives (alt07, alt_r18_c, alt_r20_a, alt_r20_b, alt_r20_c) and r19_m05 (decompose-only; out of scope, lesson line 268 claims only the reconciliation error). The DIFF alternatives (r7 alt01, r8 alt01-05, r17 alt06, alt08, r18 alt_a, alt_b) and the equivalence-claimed r17 ne06, ne07 and r18 m06 differ only by omitting the two printed lines sales_price_variance_A and _B; every other printed value equals the baseline. Lab-twin mutants are out of scope by the architect ruling."},
    {"id": "AC4-c-r20-new-mutants", "check": "three new student-error mutants of the twins",
     "location": "ledgers/AC4/mutants/AC4-c-r20/r20_m01_L06_mix_margin_at_actual_price.py; r20_m02_L05_actual_material_at_standard_kg.py; r20_m03_L06_budget_contribution_from_actual_units.py; ledgers/AC4/scripts/AC4-c-r20/make_r20_mutants.py",
     "status": "PASS",
     "evidence": "m01 (mix margin at actual price): ValueError residual -6000. m02 (actual material at standard kg): exit 0, printed values differ from the embedded L05 output (DIFF, caught by the embedded-output comparison). m03 (budget contribution from actual units): ValueError residual -265000. All three killed."},
    {"id": "AC4-c-r20-new-alts", "check": "three new alternative correct implementations",
     "location": "ledgers/AC4/mutants/AC4-c-r20/alts/alt_r20_a_L06_mix_as_sum_minus_total_average.py; alt_r20_b_L06_efficiency_loop.py; alt_r20_c_L05_flexed_units_as_budget_share_check.py",
     "status": "PASS",
     "evidence": "alt_r20_a (mix as sum CM_i q_a,i minus Q_a times budget average) and alt_r20_b (efficiency as a per-product loop) exit 0 with stdout identical to the L06 baseline; alt_r20_c (int() on already-int units; a no-op check) exit 0 with stdout identical to the L05 baseline. None over-constrains the lab."},
    {"id": "AC4-c-r20-scope-words", "check": "scope-word and banned-string scan of the changed sentences",
     "location": "course/modules/AC/AC4/L05.html lines 97, 254, 311; L06.html line 276",
     "status": "PASS",
     "evidence": "No banned string (BUILDER_RULES 1.2/1.3) and no unqualified scope word in the four changed lines. 'account for' (L05 97) sits inside 'On the convention that ...' and is computed (249,000 = 150 x 1,660); 'sets out three limits' and 'set out below' are counts checked against the bullets."},
    {"id": "AC4-c-r20-locator-drift", "check": "every round-19 line locator on the slice re-checked against the current file",
     "location": "course/modules/AC/AC4/L05.html and L06.html locators listed in LOCATOR_FIX (build_fragment_r20.py)",
     "status": "PASS",
     "evidence": "Round 19 cited round-18 line numbers for many L06 anchors (Section 4 heading, P1, P3, R1, R2/R3, E1, quiz item 4, references, honest pending) and two L05 anchors (line 63 blank). Each was corrected this round to the current line that holds the cited subject (grep and awk on the current file); the subject text is unchanged. The round-19 locator drift does not change any claim."},
    {"id": "AC4-c-r20-verify-refs", "check": "citations: offline integrity and live re-verification",
     "location": "tools/verify_refs.py --offline; tools/verify_refs.py --unit AC4",
     "status": "PASS",
     "evidence": "offline: '560 entries, 0 problems' (exit 0). live AC4: '2 of 560 entries, 0 problems' (exit 0). Neither page cites a registry key (L05 and L06 references sections, data-references empty)."},
]


def main() -> None:
    rows = [carried(r) for r in prev["rows"]]
    ids = {r["id"] for r in rows}
    for nr in NEW_ROWS:
        assert nr["id"] not in ids, nr["id"]
        rows.append(nr)
    # the NEW dict entries that name round-19 ids replaced their rows; verify no id was dropped
    assert {r["id"] for r in prev["rows"]} <= {r["id"] for r in rows}
    mutants = list(prev["mutants"])
    for name in [
        "ledgers/AC4/mutants/AC4-c-r20/r20_m01_L06_mix_margin_at_actual_price.py",
        "ledgers/AC4/mutants/AC4-c-r20/r20_m02_L05_actual_material_at_standard_kg.py",
        "ledgers/AC4/mutants/AC4-c-r20/r20_m03_L06_budget_contribution_from_actual_units.py",
    ]:
        mutants.append({"id": pathlib.Path(name).stem, "description": "Round 20 mutant (AC4-c-r20): student-error", "file": name})
    for name in [
        "ledgers/AC4/mutants/AC4-c-r20/alts/alt_r20_a_L06_mix_as_sum_minus_total_average.py",
        "ledgers/AC4/mutants/AC4-c-r20/alts/alt_r20_b_L06_efficiency_loop.py",
        "ledgers/AC4/mutants/AC4-c-r20/alts/alt_r20_c_L05_flexed_units_as_budget_share_check.py",
    ]:
        mutants.append({"id": pathlib.Path(name).stem, "description": "Round 20 alternative correct implementation (AC4-c-r20)", "file": name})
    statuses = [r["status"] for r in rows]
    verdict = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
    frag = {
        "unit": "AC4",
        "slice": "AC4-c",
        "round": 20,
        "verifier": "independent Haiku verifier, slice AC4-c (L05, L06 and their lab twins), round 20; did not build AC4",
        "pin": "fd9a9b7",
        "base": "51fa336",
        "previous_ledger": "/tmp/fanout-frags/AC4-c.round19.json (pin 51fa336)",
        "checkout": str(checkout),
        "scratch": "/tmp/AC4-c-v20",
        "verified_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verdict": verdict,
        "rows": rows,
        "mutants": mutants,
        "registry_flags": [
            "Live verify_refs --unit AC4: 2 of 560 entries, 0 problems; offline 560 entries, 0 problems; neither AC4-c page cites a registry key."
        ],
        "freshness_flags": [],
        "notes": [
            "Delta 51fa336..fd9a9b7 on this slice: L05.html lines 97, 254, 311 and L06.html line 276 only. Every other row is carried from round 19 with its subject byte-identical; carried rows whose cited line numbers were stale are listed in LOCATOR_FIX and corrected in the evidence.",
            "Architect rulings applied: hours are design targets (no pace estimate used; data-hours 7 and 6 unchanged); lab twins are demonstrations, so a twin mutant that exits 0 is out of scope unless a lesson sentence claims a check (L06 line 268 claims only the reconciliation error, which the twin still raises).",
            "The round-19 FAIL (AC4-c-math-L05, P1 solution) is re-verified and PASS: the solution now names two facts, both stated on the page.",
            "Alternatives that omit the two per-product sales-price lines are correct: they compute identical totals; only the printed subset differs.",
        ],
        "could_not_check": [
            "Full-repo pytest and full mypy were not run: scoped to tests/test_labs.py and mypy on the two twins; the full gate is not this slice's.",
            "No external source was consulted: neither lesson cites a registry key and no published figure is quoted, so no page was fetched.",
            "Visual rendering was not inspected by eye; page_smoke (Chromium, light and dark, 360 px) passed.",
            "The r19_m05 decompose-only mutant is out of scope by the architect ruling and was not fixed (report only).",
        ],
        "summary": f"rows {len(rows)}: {sum(s=='PASS' for s in statuses)} PASS, {sum(s!='PASS' for s in statuses)} non-PASS. Round-19 FAIL AC4-c-math-L05 re-verified PASS (P1 names two facts). Round-20 delta: L05 97, 254, 311 and L06 276, all re-checked. Mutants: 59 files re-run (25 ERR, 28 DIFF, 6 SAME: 5 alternatives and the out-of-scope r19_m05); 3 new student-error mutants killed; 3 new alternatives pass. Locator drift from round 19 corrected.",
    }
    out = checkout / "ledgers/AC4/AC4-c.json"
    out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", out, verdict, len(rows))


main()
