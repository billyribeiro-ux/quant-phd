"""Build the round-13 fragment for M2 slice e from the evidence collected in this round."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import ledger  # noqa: E402

S = "ledgers/M2/scripts/M2-e-r13"
CARRY = "Carried from round 12 (grader/, tests/labs/M2/lab-M2-project-{1,2,3}.py byte-identical since pin ff388424; project.html delta is 2 prose lines, lines 224 and 227): "
CARRY_PH = "Carried from round 12 (course/modules/M/M2/project.html lines not in the delta byte-identical since pin ff388424): "
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows.append(r)


row("e-auto-run", "reference.py passes the whole suite on seeds 0-49 under browser flags", "course/modules/M/M2/grader/reference.py", "PASS",
    f"tools/run_graders.py --unit M2 --seeds 0-49 -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)' ({S}/run_graders_M2.out)")
row("e-auto-instances", "instance.py deterministic per seed and varies across seeds", "course/modules/M/M2/grader/instance.py", "PASS",
    f"same run_graders M2 PASS on seeds 0-49 ({S}/run_graders_M2.out)")
row("e-mut-existing", "all existing grader mutants killed", "ledgers/M2/mutants/", "PASS",
    f"tools/mutate_graders.py --unit M2 --seeds 0-49 -> 'mutate_graders M2: PASS (113/113 killed)' ({S}/mutate_M2_all.out); 110 existing mutants, 3 new")
row("e-mut-r6_01", "student-error mutant r6_01 (fd step silently capped at one) killed", "course/modules/M/M2/grader/test_project.py:282-308", "PASS",
    f"KILLED r6_01_fd_step_silently_capped_at_one.py in {S}/mutate_M2_all.out")
row("e-mut-r6_02", "student-error mutant r6_02 (hessian step capped at a thousandth) killed", "course/modules/M/M2/grader/test_project.py:546-580", "PASS",
    f"KILLED r6_02_hessian_step_silently_capped_at_a_thousandth.py in {S}/mutate_M2_all.out")
row("e-mut-new-killed", "round-12 mutants r12_01..03 killed; round-13 mutants r13_01..03 killed", "ledgers/M2/mutants/r12_01..r12_03, r13_01..r13_03", "PASS",
    f"KILLED lines for r12_01_hessian_entries_rounded_to_six_places, r12_02_fd_refuses_steps_above_one_hundred_thousand, r12_03_hessian_refuses_steps_below_a_thousandth, r13_01_bond_price_rounds_each_cash_flow_before_summing (test_price_is_the_half_even_rounding_of_the_exact_price), r13_02_dprice_dy_per_percentage_point (test_first_derivative_matches_the_central_difference_of_the_price), r13_03_hessian_diagonal_uses_double_step (test_hessian_positive_step_is_accepted) in {S}/mutate_M2_all.out")
row("e-alternatives", "two alternative correct engines pass the suite on seeds 0-49", "course/modules/M/M2/grader/test_project.py", "PASS",
    f"sh {S}/run_alt.sh alts/alt1_exact_engine.py -> '50/50 seeds pass, 0 fail'; alt2_float_reordered_engine.py -> '50/50 seeds pass, 0 fail'")
row("e-messages", "failure messages and assertions", "course/modules/M/M2/grader/test_project.py", "PASS", CARRY + "test_project.py identical; full suite run in browser (page_smoke) passes 85 tests")
row("e-pyodide-local", "suite runs in the browser grader with local files", "course/modules/M/M2/project.html", "PASS",
    f"tools/page_smoke.py --unit M2 --pages project -> 'in-browser grader: All 85 tests pass on seed 728889329'; 'page_smoke M2: PASS' ({S}/page_smoke_M2_project.out)")
row("e-test-count", "test count on page equals collect-only count", "course/modules/M/M2/project.html:211", "PASS",
    f"collect-only in scratch copy of grader + reference as sensitivity_engine.py: '85 tests collected' ({S}/collect_only.out); project.html:211 says 'runs 85 tests'")
row("e-valueerror-scope", "ValueError only for conditions the page names", "course/modules/M/M2/grader/test_project.py; course/modules/M/M2/project.html (The three ValueError conditions)", "PASS",
    CARRY + "ValueError bullet unchanged (the delta changed only the Automatic differentiation and Tolerances bullets)")
row("e-scheme-types", "scheme argument types named on page", "course/modules/M/M2/project.html (Grading mode and Conventions)", "PASS", CARRY_PH + "scheme-type bullet unchanged")
row("e-hours", "hours design targets", "course/modules/M/M2/project.html (Time budget)", "PASS", CARRY_PH + "Time budget unchanged")
row("e-hours-arith", "hours arithmetic between hub split and lesson hours", "course/modules/M/M2/project.html (Time budget)", "PASS", CARRY_PH + "Time budget unchanged")
row("e-ladder", "four-rung ladder in order", "course/modules/M/M2/project.html:40-48", "PASS", f"tools/check_projects.py --unit M2 -> 'check_projects M2: PASS' ({S}/check_projects.out)")
row("e-spec-questions", "specification names context, inputs, outputs, constraints, grading mode", "course/modules/M/M2/project.html Rung 3 (line 46)", "PASS", CARRY_PH + "Rung 3 specification unchanged; check_projects PASS")
row("e-rubric-calibration", "rubric calibrated with two exemplars", "course/modules/M/M2/project.html (The rubric and Two exemplars, lines 398-507)", "PASS", CARRY_PH + "rubric and exemplars unchanged")
row("e-rubric-observable", "rubric rows observable", "course/modules/M/M2/project.html rubric table (line 402)", "PASS", CARRY_PH + "rubric table unchanged")
row("e-rubric-adversarial", "self-assessment and rubric resist adversarial answers", "course/modules/M/M2/project.html (Self-assessment and rubric table)", "PASS", CARRY_PH + "unchanged")
row("e-atlas-studio", "curriculum entry and build plan agree with project", "curriculum/meta.yaml; plans/M2-build-plan.md", "PASS", "git diff ff388424..fca6bb1 shows neither file changed; carried from round 12")
row("e-labs-run", "all project labs run", "tests/labs/M2/lab-M2-project-{1,2,3}.py", "PASS",
    f"tools/run_labs.py --unit M2 -> 'run_labs M2: PASS (27/27)' ({S}/run_labs_M2.out); twins under python -I -W error exit 0 with empty stderr ({S}/twin_project_{{1,2,3}}.err)")
row("e-labs-page-twin", "page lab code equals twin; expected block equals output", "course/modules/M/M2/project.html Lab 1-3 blocks", "PASS",
    f"run_labs M2 PASS (page code byte-identical to twin, expected output matches) ({S}/run_labs_M2.out)")
row("e-lab1-numbers", "Lab 1 numbers in prose match output", "course/modules/M/M2/project.html:57, :116", "PASS", CARRY_PH + "lines unchanged; run_labs PASS")
row("e-lab2-numbers", "Lab 2 numbers in prose match output", "course/modules/M/M2/project.html:121, :195", "PASS", CARRY_PH + "lines unchanged; run_labs PASS")
row("e-lab3-numbers", "Lab 3 numbers in prose match output", "course/modules/M/M2/project.html:267-377", "PASS", CARRY_PH + "lines unchanged; run_labs PASS")
row("e-lab3-interpretation", "Lab 3 interpretation sentence", "course/modules/M/M2/project.html:377", "PASS", CARRY_PH + "line unchanged")
row("e-report-spec", "report specification", "course/modules/M/M2/project.html:207, :270", "PASS", CARRY_PH + "lines unchanged")
row("e-exemplar-numbers", "exemplar numbers", "course/modules/M/M2/project.html:409-507", "PASS", CARRY_PH + "exemplar block unchanged")
row("e-sin-ratio", "sin central-difference ratio statement", "course/modules/M/M2/project.html:226", "PASS",
    "line 226 unchanged by delta; the ratio 3.9999842-3.9999851 is a grader constant, and the order check passes on seeds 0-49 (run_graders M2 PASS)")
row("e-formulas", "formulas in the Hessian, AD and ratio bullets", "course/modules/M/M2/project.html:214-227", "PASS",
    "re-verified: delta to project.html is two prose lines (224 'round-off' to 'rounding error'; 227 'round-off' to 'rounding error' in Tolerances); no formula changed; formulas match grader reference.py hessian_fd (lines 91-111) and sensitivities (lines 140-154)")
row("e-cards-correct", "every card agrees with its current lesson text", "course/modules/M/M2/cards.json; course/modules/M/M2/L21.html, L22.html, L23.html; cards in L01-L24", "FAIL",
    "Re-verified all 395 cards: changed cards (25 existing, 16 new) and every card of L21, L22, L23 read against the current lesson text. Round-12 failures are fixed: M2-c058 now asks for c'(1.5) and its central-difference error (L05 table line 94 prints 95.062500855 and 8.55e-07); M2-c285 now gives the 1/2 factor. Still failing: M2-c386 (cites 'at par' in Section 1 of L23; the phrase is absent from L23 body, see L23.html:38); M2-c163 (examples use [0,1], not [0,b]); M2-c394 (Problem R3 asks for a proof, does not prove it). Rows e-cards-at-par, e-cards-c163 and e-cards-c394 carry the detail.",
    "Fix the three rows below, then re-check the card against its lesson.")
row("e-cards-delta", "cards changed since round-12 pin agree with lessons", "course/modules/M/M2/cards.json", "PASS",
    "Changed existing cards: c058, c084, c163, c178, c180, c188, c189, c380, c205, c217, c265, c280, c281, c285, c299, c303, c309, c317, c336, c346, c347, c351, c385, c365, c388, c389. Each read against lesson text (L05 line 94; L07 lines 55-56; L11 lines 128-134; L12 lines 144, 152, 205-240; L13 line 46; L14 lines 35-39, 178; L18 line 28; L19 lines 22-27, 181; L20 line 39; L24 line 55; L10 lines 24-27; L08 lines 26, 33-34), wording-only changes accepted except c163 and c386/c394 (separate rows). Numbers for c346/c351/c385 match twin_L23.out (3.9279, 3.9634, 7.8807, 7.9396, remainder -15 cents).")
row("e-cards-new-390-405", "16 new cards agree with lesson text", "course/modules/M/M2/cards.json (M2-c390..c405)", "PASS",
    "Each new card read against its lesson: c390 L01 Prop 3.1 (line 90), c391 L01 Prop 4.2/Example 4.1 (lines 95, 113), c392 L03 Section 1 (line 22), c393 L05 Assumption 1.4 (line 42), c395 L07 Example 4.1, Prop 4.2, Remark 4.3 (lines 219-226), c396 L08 line 26 (no grade, not proved here), c397 L08 Remark 3.2 (line 144), c398 L12 Assumption 2.2 (line 205) and Problem L12-R3 (line 359 in HTML), c399 L14 Assumption 1 (line 35), c400 L17 Assumption 1 and Examples 1.2, 2.3 (lines 25, 27, 45), c401 L18 Assumption 1 and Problem R1 (line 144), c402 L20 Assumption 3.1 and Example 3.1 (lines 123-125), c403 L21 Assumption 1.3 (line 25-26), c404 L22 Assumption 1.1 and Example 1.5 (lines 39, 41), c405 L24 Assumption 4.1 (line 56). Cards have no duplicate fronts or backs (checked).")
row("e-cards-L21-L23", "cards of the changed lessons L21 to L23 agree with the changed text and lab outputs", "course/modules/M/M2/cards.json (L21, L22, L23 cards); L21.html:198, :319; L22.html:370; L23.html:82, :96-99, :375-379", "PASS",
    f"Lab numbers re-derived by running tests/labs/M2/lab-M2-L23-1.py under python -I -W error ({S}/twin_L23.out): price 108110.895779 -> 108111; P' -851466.739529 (diff 1.6e-03); P'' 8376648.511919 (diff 1.9); first-order error 4.037716e+02; second-order -1.506081e+01; ratios 3.9279/7.8807, 3.9634/7.9396; +0.01 exact 100000 vs 100015 (diff -15); -0.01 exact 117060 vs 117044 (diff 16). Misconception numbering checked in L21, L22, L23 Misconceptions blocks. M2-c322 and c317 match L21 example text.")
row("e-cards-at-par", "card M2-c386 cites a definition of 'at par' in L23 Section 1", "course/modules/M/M2/cards.json (M2-c386); course/modules/M/M2/L23.html:38", "FAIL",
    "Card back: 'A bond priced at its face value is said to be at par (Section 1).' grep -n -i 'at par' L23.html returns only L23.html:38, the Introduces note, which says the phrase is defined in Section 1. Section 1 (L23.html lines ~21-35) contains no such definition; grep -i 'par' finds no other use.",
    "Either add the sentence 'A bond priced at its face value is at par' to L23 Section 1 (Definition 1.1 area), or remove the card's '(Section 1)' reference and the L23.html:38 claim. Owner of L23 must change the lesson; card M2-c386 then re-checked.")
row("e-cards-c163", "card M2-c163 describes the worked examples' intervals", "course/modules/M/M2/cards.json (M2-c163); course/modules/M/M2/L11.html (Misconception 3, line ~134)", "FAIL",
    "Card and L11 Misconception 3 say the worked examples check integrability 'using polynomials on [0, b] with b > 0 (Corollary 1.2)'. The worked examples integrate over [0,1] (L11 text lines 41, 45 'integrable on [0, 1]'); no example uses a general [0,b].",
    "Replace '[0, b] with b > 0' with '[0, 1]' in M2-c163 and in L11 Misconception 3 (L11 is outside this slice; route to the L11 owner), then re-check.")
row("e-cards-c394", "card M2-c394 describes what Problem R3 does", "course/modules/M/M2/cards.json (M2-c394); course/modules/M/M2/L06.html:161", "FAIL",
    "Card back: 'Problem R3 proves that a derivative bounded by M gives this bound, assuming Assumption 2.1.' L06 line 161 is a prompt: 'prove that |f(x) - f(y)| <= M|x - y|'. The lesson gives no proof, so the card asserts that the lesson contains the proof.",
    "Change the card back to 'Problem R3 asks for a proof that a derivative bounded by M gives this bound, assuming Assumption 2.1.'")
row("e-cards-dup", "no duplicate cards", "course/modules/M/M2/cards.json", "PASS", "python3 check: 395 unique ids, 0 duplicate fronts, 0 duplicate backs")
row("e-cards-numbers", "numbers in cards appear in their lesson or are computed", "course/modules/M/M2/cards.json", "PASS",
    f"ledgers/M2/scripts/M2-e-r13/check_cards_mech.py (dump_text.py output) flagged 50 items, all 'Misconception N' labels and none a number ({S}/check_cards_mech.out); L21-L23 numbers re-derived from twin output above")
row("e-cards-atomic", "one claim per card; unchanged cards carried", "course/modules/M/M2/cards.json", "PASS", CARRY_PH + "unchanged cards in unchanged lessons; changed and new cards read individually above")
row("e-cards-labels", "labels cited (Theorem, Assumption, Example, Misconception) exist in the lesson", "course/modules/M/M2/cards.json", "PASS",
    f"check_cards_mech.py flags only 'Misconception N' because lesson Misconceptions blocks are list items with no printed numbers; the three changed lesson blocks (L21 line 116, L22 line 162, L23 line 165) were counted by hand; other lessons carried from round 12. Labels cited by the new cards exist (see e-cards-new-390-405).")
row("e-cards-grades", "grades and bases", "course/modules/M/M2/cards.json", "PASS", "grades: T 241, C 76, None 78 (python3 Counter). Each C card carries a basis naming Lab 1 or SIMULATED data (checked on all 76).")
row("e-cards-delta-removed", "removed cards", "course/modules/M/M2/cards.json", "PASS", "M2-c388 and M2-c389 are present (changed, not removed); no id from round 12 is missing (379 old ids all present)")
row("e-data-figures", "figures and data in project", "course/modules/M/M2/project.html", "PASS", CARRY_PH + "project.html:57, :109-110 numbers unchanged")
row("e-structure", "page structure and checks", "course/modules/M/M2/", "PASS", f"tools/check_pages.py --unit M2 -> 'check_pages M2: PASS' ({S}/check_pages.out)")
row("e-banned-phrases", "no banned or process words in learner text", "course/modules/M/M2/*.html, cards.json", "PASS", f"tools/check_pages.py --unit M2 PASS (banned strings in visible prose, {S}/check_pages.out); the delta replaced 'round-off' with 'rounding error' in project.html")
row("e-dag", "concept use within prerequisite closure", "course/modules/M/M2/", "PASS", f"tools/check_dag.py --unit M2 -> 'check_dag M2: PASS' ({S}/check_dag.out)")
row("e-notation", "notation symbols vs notation/notation.json", "notation/notation.json; course/modules/M/M2/ changed lines", "PASS",
    "notation.json lists 8 symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q); none is used in M2 cards or project with another meaning. R(h) in cards M2-c284 and M2-c291 is the remainder of the L19 second-order expansion, not a registry symbol. Delta changed no symbol.")
row("e-citations", "citations and registry keys", "course/modules/M/M2/project.html:547-551", "PASS",
    "tools/verify_refs.py --offline -> '560 entries, 0 problems' (verify_refs_offline.out); project.html:547-551 unchanged by delta")
row("e-hours-declared-spec", "declared hours in spec", "course/modules/M/M2/project.html:35", "PASS", CARRY_PH + "line 35 unchanged")

fragment = {
    "unit": "M2",
    "slice": "e",
    "round": 13,
    "verifier": "independent verifier (Haiku 5.5), slice e",
    "pin": "fca6bb104984c6a724fc214d8073158e610e995a",
    "base": "ff388424d9d056b7a57868dab5ae7f7cdeef60f6 (round-12 pin); round-12 fragment /Users/billyribeiro/.fanout/frags/B-M2-e.round12.json",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB13-M2-e",
    "scratch": "/tmp/m2e_r13",
    "verified_at": "2026-10-29T00:00:00Z",
    "verdict": "FAIL",
    "mutants": [
        {"name": "r13_01_bond_price_rounds_each_cash_flow_before_summing.py",
         "description": "bond_price_cents rounds each discounted cash flow to whole cents before summing (per-term rounding).",
         "killed_by": "test_price_is_the_half_even_rounding_of_the_exact_price[inst0] (seed 0)"},
        {"name": "r13_02_dprice_dy_per_percentage_point.py",
         "description": "sensitivities reports dprice_dy per percentage point of yield (divided by 100).",
         "killed_by": "test_first_derivative_matches_the_central_difference_of_the_price[inst0] (seed 0)"},
        {"name": "r13_03_hessian_diagonal_uses_double_step.py",
         "description": "hessian_fd diagonal uses step 2h with divisor (2h)^2.",
         "killed_by": "test_hessian_positive_step_is_accepted (seed 0)"},
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since round-12 pin (ff388424..fca6bb1) touches project.html (2 prose lines), cards.json (25 changed, 16 added), and lessons L21, L22, L23 and the L23 lab twin; grader/, tests/labs/M2/lab-M2-project-*.py and notation/ are unchanged.",
        "All 110 existing mutants and the 3 new ones are killed on seeds 0-49; run_graders M2 50/50; alternative engines alt1 and alt2 pass 50/50.",
        "Mechanical check_cards_mech.py reports 50 'Misconception N' flags; these are list-item labels in lesson Misconceptions blocks, not wrong citations (L21-L23 verified by hand).",
        "Outside this slice, not edited: L23.html:38 claims 'at par' is defined in Section 1 (false, see e-cards-at-par); L11 Misconception 3 says [0, b] (see e-cards-c163). Owners of L11 and L23 must fix the lesson text.",
        "Round-12 FAIL rows are resolved: M2-c058 and M2-c285 are fixed. Round-12 'PASS' rows that depended only on unchanged files are carried with the prefix named in each row.",
    ],
    "rows": rows,
    "summary": {
        "text": "Slice e round 13: FAIL. Grader, project labs, project.html rubric, hours, the 85-test count, and all 113 mutants are PASS on fca6bb1. Two round-12 card failures (c058, c285) are fixed. Three card rows fail: M2-c386 cites an 'at par' definition that L23 Section 1 does not contain; M2-c163 says the examples use [0, b] where they use [0, 1]; M2-c394 says Problem R3 proves a result it asks the reader to prove.",
        "counts": {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows)},
    },
}
problems = ledger.validate(fragment, "M2-e")
print("validate:", problems)
Path("ledgers/M2/M2-e.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", fragment["summary"]["counts"]["pass"], "fail", fragment["summary"]["counts"]["fail"])
