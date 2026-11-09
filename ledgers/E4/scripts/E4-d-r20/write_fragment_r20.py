"""Round-20 writer for ledgers/E4/E4-d.json (verifier output; not a report file).

Carries round-19 PASS rows whose cited subject is byte-identical to cd4dd7df (prefix as VERIFIER_RULES requires),
re-verifies every other round-19 row against the round-20 evidence in ledgers/E4/scripts/E4-d-r20/out/, and adds the
round-20 rows. Usage: python3 -I write_fragment_r20.py <checkout-root> <prev-fragment.json> <mutate-gate-output.txt>
"""
import json
import re
import sys

root, prev_path, gate_path = sys.argv[1], sys.argv[2], sys.argv[3]
prev = json.load(open(prev_path, encoding="utf-8"))
CHANGED = ("project.html", "README", "equivalent", "FINAL-ARCHITECT", "mutant", "mutate", "E4d-cmd", "gate",
           "lab-E4", "tests/labs", "cards", "142", "E4d-lab", "E4d-hours", "E4d13-hours", "E4d16-hours", "E4d19-hub",
           "E4d-num", "E4d-math", "E4d-notation", "E4d-prose", "E4d-spec", "E4d-rubric", "E4d-exemplar", "E4d-equivalent")
import datetime
VERIFIED_AT = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()
CARRY_PREFIX = ("Carried from round 19 (grader/*, tools/*, alternatives/*, tests/labs/E4/*, references/*, "
                "notation/*, instance.py and reference.py byte-identical since cd4dd7df): ")
CAT = {
    "2.1-citations": "verify_refs --offline: 560 entries, 0 problems (out/verify_refs_offline_r20.txt); verify_refs "
                     "--unit E4 live: 3 of 560 entries, 0 problems (out/verify_refs_E4_live_r20.txt); reading keys "
                     "present in references/references.json.",
    "2.2-numbers": "Numbers recomputed in round 20: lab expected blocks reproduced (out/run_labs_E4_project.txt 3/3; "
                   "out/labs_twin_check_r20.txt); exemplar ratios recomputed (1.249999999999898, 1.500000000000611); "
                   "grid and bound values from reference.py and instance.py (scratch /tmp/e4d20).",
    "2.4-numbers": "Numbers recomputed in round 20 (see the 2.2-numbers evidence above and E4d20-num-spec-bounds).",
    "2.4-docstrings": "Docstrings read in round 20 (test_project.py and project.html Lab 3); the numbers they state match "
                      "the outputs in out/labs_twin_check_r20.txt and out/collect_count_r20.txt.",
    "2.2-prose": "Whole page read in round 20 (702 lines); process-word grep empty; check_pages PASS "
                 "(out/check_pages_E4.txt); page_smoke PASS (out/page_smoke_E4_project.txt).",
    "2.9-prose": "Whole page read in round 20; check_pages PASS (out/check_pages_E4.txt); page_smoke PASS.",
    "2.4-scope": "Scope words on the page grepped and each claim read against a computation (round 20): every/all/only "
                 "claims are derivations or computed checks; range claims checked by out/range_sweep_r20.txt.",
    "2.3-grades": "Regraded in round 20 per BLUEPRINT 3: derived propositions are T with their assumptions named; "
                  "computed lab values are C naming the lab (Proposition 5 gives the grid pattern).",
    "2.4-mathematics": "Re-derived in round 20 line by line: Lemmas 1-3, Propositions 1-5 (steps (0)-(4), the sign rule, "
                       "G(0+), the boundary cases, the closed forms). No defect found; A6 is assumed, which is stated.",
    "2.4-notation": "Macros used (\\E, \\Var, \\Corr, \\Cov, \\Normal) are registered in notation/notation.json; no "
                    "registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) appears on the page.",
    "2.5-labs": "run_labs --unit E4 --page project: 3/3 PASS; out/labs_twin_check_r20.txt: page code equals twin "
                "(Lab 2 differs only at the blank, ruling 11), twin runs under python -I -W error with empty stderr, "
                "output equals the expected block.",
    "2.6-spec": "Specification read against grader/test_project.py, instance.py, reference.py and the curriculum entry "
                "(project brief and grading both); collect-only 49 (out/collect_count_r20.txt); no missing question found.",
    "2.6-autograder": "Grader unchanged since cd4dd7df; run_graders 50/50 on reference.py (out/run_graders_E4_0_49.txt); "
                      "local pytest 49 passed on seeds 0 and 2009908600 with the documented flags.",
    "2.6-rubric": "Rubric read in round 20 (project.html:518-528); observability checked level by level; see the "
                  "C4 finding (E4d20-rubric-C4-levels).",
    "2.6-rubric-calibration": "Calibration from the blind scorer file ~/.fanout/blind/E4-d.json (A 2,2,1,2,1; B 4,4,4,4,4) "
                              "equals the data-scores at project.html:536 and :601 and the verdict lines; not scored by "
                              "this verifier (ruling 23).",
    "2.6-hours": "Hours: 1+1+5+8+5+5+3 = 28 = data-hours-project 28 = hub 28 (index.html:29); hours are design targets "
                 "under the verifier rulings; this verifier's own estimate is 15 to 24 hours.",
    "2.6-mutation": "tools/mutate_graders.py --unit E4 --seeds 0-9 in round 20: 144/144 killed "
                    "(out/mutate_graders_E4_0_9_r20.txt); the file is byte-identical to its round-19 version.",
    "2.6-equivalent": "Equivalent files and proofs re-checked in round 20 (out/literal_sign_random_r20.txt, "
                      "out/literal_price_sign_0_49.txt, out/stop_rule_equivalents_0_49.txt, out/equiv_r19_02_0_49.txt, "
                      "sweeps in E4-d-r20 and E4-d-r25).",
    "2.6-alternatives": "alt_1..alt_8 run on seeds 0-49 in round 20: 50/50 each (out/alt_*.txt); stdlib only; "
                        "no hard-coded answers.",
    "2.6-atlas": "No atlas contract for E4; no studio; project grading is both (curriculum entry E4).",
    "2.8-data": "No dataset; the labs and grader are SIMULATED and labelled (project.html:313, :358, lab hypotheses).",
    "2.9-hours": "Hours arithmetic re-run in round 20 (28 = 28 = 28; 72 + 28 = 100 on index.html:29-43).",
    "2.9-plan": "plans/E4-build-plan.md unchanged; plans/FINAL-ARCHITECT-RULINGS.md (73 lines) read in full; ruling 25 "
                "added this round.",
    "2.9-delta": "Delta cd4dd7df..d1083bf1 for slice d read hunk by hunk: project.html (10 hunks), E4 cards.json (not "
                 "in slice), equivalent README and the r19_02 file, mutants r19_01/03/04, ruling 25.",
    "2.9-banned": "check_pages PASS (banned strings, out/check_pages_E4.txt) and grep of the page for process words.",
    "2.9-dag": "check_dag --unit E4 PASS (out/check_dag_E4.txt).",
    "2.4-prose": "Whole page read in round 20; process-word and scope-word checks; check_pages and page_smoke PASS (out/).",
    "2.9-structure": "check_pages --unit E4 PASS (out/check_pages_E4.txt); anchors and href targets checked by page_smoke (no failed requests, out/page_smoke_E4_project.txt).",
    "2.9-smoke": "page_smoke --unit E4 --pages project PASS: zero console errors, in-browser grader 49 pass.",
    "2.10-dag": "check_dag PASS; Definition 6.2 (CARA) present in course/modules/E/E4/L06.html.",
    "gate": "Gate output re-run in round 20 (out/ directory of E4-d-r20).",
    "2.6-structure": "check_projects --unit E4 PASS (out/check_projects_E4.txt).",
    "2.6-spec-ladder": "check_projects PASS; ladder read in round 20 (project.html:40-53).",
}
RETIRED = {"E4d8-alternatives-r8": "retired by ruling 18: alt_r8_a/alt_r8_b are not present; alt_1..alt_8 are the verified set",
           "E4d9-alternatives-v9": "retired by ruling 18: alt_v9_* are not present; alt_1..alt_8 are the verified set"}
OVERRIDE = {
    "E4d-rubric-observable": ("FAIL", "C4 level 4 and level 3 are not separable by observable text; see E4d20-rubric-C4-levels."),
    "E4d-equivalent": ("PASS", "Equivalent files and their proofs re-checked in round 20 (see 2.6-equivalent evidence). The stale open-item paragraph of the README is E4d20-equiv-readme-literal-open-item."),
    "E4d19-mutant-r19-02": ("PASS", "Round 20: the file is in ledgers/E4/equivalent/ (ruling 25). Its sweep reproduces: out/sweep_r19_02_r25_rerun.txt (77194 interior points, worst 8.517e-15, none above 1e-14); round-20 domain sweep over sd 1e-50..1e2 and cost 0..0.34 (80072 points, worst 8.5423e-15) and a local scan (72000 points, worst 7.49e-15) found no point above 1e-14. Measured, not proved (ruling 25); the seeds 0-49 run passes 50/50 (out/equiv_r19_02_0_49.txt)."),
    "E4d-mutants-total": ("PASS", "144 files in ledgers/E4/mutants/ (141 existing plus 3 new, mutant_d20_01..03); mutate_graders 144/144 killed (out/mutate_graders_E4_0_9_r20.txt)."),
    "E4d13-mutant-gate-final": ("PASS", "tools/mutate_graders.py --unit E4 --seeds 0-9: 144/144 killed in round 20 (out/mutate_graders_E4_0_9_r20.txt)."),
    "E4d15-cmd-mutate": ("PASS", "tools/mutate_graders.py --unit E4 --seeds 0-9: 144/144 killed in round 20 (out/mutate_graders_E4_0_9_r20.txt); the round-19 survivor is moved to equivalent/."),
    "E4d-cmd-ruff": ("PASS", "ruff check . : 'All checks passed!' and ruff format --check . : '553 files already formatted' (out/ruff_check.txt, out/ruff_format.txt). Repo-wide; ledgers scripts and mutants are excluded by pyproject extend-exclude."),
    "E4d-cmd-mypy-workspace": ("PASS", "mypy --no-incremental with the repository config (files = tools, tests): 'Success: no issues found in 385 source files' (out/mypy.txt). The grader and labs are not in mypy's file list; they were checked by run_graders and run_labs."),
    "E4d-cmd-mypy-plan-command": ("PASS", "Same command and result as E4d-cmd-mypy-workspace (out/mypy.txt): 385 source files, no issues."),
    "E4d-cmd-pytest-relevant": ("PASS", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py: all pass, EXIT=0 (out/pytest_labs.txt). pytest -q tests/test_memo_exemplars.py tests/test_docs_figures.py: 28 passed (out/pytest_memo_exemplars_r20.txt)."),
    "E4d-cmd-check-pages": ("PASS", "check_pages --unit E4: PASS (out/check_pages_E4.txt), including banned strings and unique ids."),
}
NEW = [
    ("E4d20-grader-root-tolerance", "2.6-autograder", "course/modules/E/E4/grader/test_project.py:346-349 (test_fraction_is_the_oracle_root) with TOL_ROOT at :46", "FAIL",
     "Grader check is abs(lam - oracle_root) <= TOL_ROOT with TOL_ROOT = 1e-10 absolute. project.html:317 states that for an interior root in the domain the reported lambda agrees with the root of Proposition 4 to within 1e-10 times the root, and that any reported fraction within 1e-10 times the root is accepted. Oracle roots: seed 0 0.5467405024590335 (stated bound 5.47e-11, grader bound 1e-10); seed 7919 0.44492757427135565 (stated 4.45e-11, grader 1e-10). The grader accepts errors up to 1.8x and 2.2x the stated bound. Oracle and reference agree to 8.3e-14 and 2.0e-13 relative, so the stated relative bound is achievable (/tmp/e4d20 scripts oracle_gap_root.py, roots.py).",
     "Change the check to abs(lam - oracle_root(sd, cost)) <= TOL_ROOT * oracle_root(sd, cost) (interior roots; the boundary cases are exact through the boundary tests). Scratch check on a copy: reference and alt_1..alt_8 pass seeds 0-9 with the relative bound. Then re-run run_graders --seeds 0-49, the alternatives and mutate_graders."),
    ("E4d20-rubric-C4-levels", "2.6-rubric", "course/modules/E/E4/project.html:527 (C4 row, level 4 and level 3 cells); :518", "FAIL",
     "C4 level 4 requires 'names the decimals or significant digits shown for each output and the rule that produces them'. Level 3 already requires 'the decimals or significant digits shown for each output, and that every number is computed from unrounded solver output'. The rule in level 4 is the same sentence as level 3's unrounded-output statement; the blind scorer's note records this (~/.fanout/blind/E4-d.json, C4 text). A memo that meets level 3 therefore meets level 4 by this text, so the two levels are not observably separate. Not a calibration failure: the blind scores match.",
     "Give level 4 an element level 3 does not require, stated observably, for example: 'Everything in level 3, and names the rounding mode for each output and the precision of each derived number the memo shows (a ratio or a difference), with the rule that produces it.' Then re-check exemplar B (C4 4, project.html:629 shows the ratios) and exemplar A (C4 2) against the new text with a blind rescoring (ruling 23)."),
    ("E4d20-equiv-readme-literal-open-item", "2.6-equivalent", "ledgers/E4/equivalent/README.md:9-12 and :26-29 (section 'What the architect must decide')", "FAIL",
     "The README still says literal_price_sign is 'recorded here as an open item for the architect' and asks the architect to choose (a) or (b). Ruling 24 (plans/FINAL-ARCHITECT-RULINGS.md:62-67, binding) decided it: it stays equivalent, its proof stands, and ruling 9 provides the equivalent/ path. The open-item text contradicts the binding ruling.",
     "Replace the open-item paragraph (README:26-29) and the sentence at :11-12 with: 'Decision: ruling 24 (round 18) keeps this variant equivalent; its sign is unobservable in every output (b_u enters only as b_u*b_u), so ruling 9 places it here.'"),
    ("E4d20-mutants-new-d20", "2.6-mutation", "ledgers/E4/mutants/mutant_d20_01_closed_form_root_denominator_sign_slip.py; mutant_d20_02_informativeness_is_payoff_signal_correlation.py; mutant_d20_03_uninformed_slope_drops_price_term.py", "PASS",
     "Three new student-error mutants written by this verifier (not at the tolerance boundary): d20_01 a sign slip in the closed-form interior root (tau_e + tau-bar), d20_02 informativeness reported as Corr(v,s)^2 = tau_e/(tau_v+tau_e), d20_03 uninformed term without the price slope. Each is killed (out/mutate_graders_E4_0_9_r20.txt: KILLED d20_01 by test_indifference_holds_at_an_interior_fraction[first]; d20_02 by test_info_cost_far_above_one_is_accepted[10.0]; d20_03 by test_gap_is_the_oracle_gap_at_the_reported_fraction[first]). Generator: ledgers/E4/scripts/E4-d-r20/make_mutants_r20.py."),
    ("E4d20-mutant-count-144", "2.6-mutation", "ledgers/E4/mutants/ (144 files); tools/mutate_graders.py --unit E4 --seeds 0-9", "PASS",
     "Gate output: 'mutate_graders E4: PASS (144/144 killed)', exit 0 (out/mutate_graders_E4_0_9_r20.txt). Every listed mutant has a docstring whose first line names the error (ast scan, round 20).", ""),
    ("E4d20-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit E4 (all pages); --page project", "PASS",
     "run_labs --unit E4 --page project: PASS (3/3). run_labs --unit E4: PASS (12/12) (out/run_labs_E4_all.txt).", ""),
    ("E4d20-labs-twins-direct", "2.5-labs", "course/modules/E/E4/project.html #lab-E4-project-1..3; tests/labs/E4/lab-E4-project-1..3.py", "PASS",
     "scripts/E4-d-r20/labs_twin_check_r20.py: page code equals twin for labs 1 and 3; lab 2 differs only at the blank (completion, ruling 11); each twin exits 0 under python -I -W error with empty stderr; output equals the page expected block for all three (out/labs_twin_check_r20.txt).", ""),
    ("E4d20-run-graders-0-49", "2.6-autograder", "course/modules/E/E4/grader/reference.py; test_project.py; instance.py", "PASS",
     "run_graders --unit E4 --seeds 0-49: reference 50/50 (out/run_graders_E4_0_49.txt); collect-only 49 tests, matching the page's 49 (out/collect_count_r20.txt).", ""),
    ("E4d20-alternatives-0-49", "2.6-alternatives", "ledgers/E4/alternatives/alt_1.py..alt_8.py", "PASS",
     "run_candidate on seeds 0-49: alt_1..alt_8 each 50/50 (out/alt_1.txt .. out/alt_8.txt, driver ledgers/E4/scripts/E4-d-r20/run_alts_r20.sh). Six distinct styles: bisection on the gap (alt_1), Illinois (alt_2, alt_8), grid scan then bisection (alt_3), secant (alt_4), closed form (alt_6), bisection on the sign rule (alt_7); alt_5 parameterises by noise precision. Ruling 10 satisfied.", ""),
    ("E4d20-equiv-stop-rule-0-49", "2.6-equivalent", "ledgers/E4/equivalent/mutant_r6_08_reports_lower_end.py; mutant_r7_01_reports_bracket_lower_end.py; mutant_v9_02_stop_rule_relative_to_lower_end.py", "PASS",
     "Each passes seeds 0-49, 50/50 (out/stop_rule_equivalents_0_49.txt). Ruling 17 proof (bracket containment) re-read; the reported point lies inside the final bracket of width at most 1e-12 times the root, inside the 1e-10 requirement.", ""),
    ("E4d20-equiv-literal-sign", "2.6-equivalent", "ledgers/E4/equivalent/literal_price_sign.py", "PASS",
     "Passes seeds 0-49 50/50 (out/literal_price_sign_0_49.txt); 3000 random inputs, largest difference 0.0 (out/literal_sign_random_r20.txt); the algebraic argument (b_u enters only as b_u*b_u) re-read in reference.py:55-58 and :73.", ""),
    ("E4d20-num-spec-bounds", "2.4-numbers", "course/modules/E/E4/project.html:313 (Inputs); grader/instance.py:1-21", "PASS",
     "tau_bar(0.150) = 0.09762327..., tau_bar(0.120) = 0.23756678..., and 1/(1+4*0.75^2) = 0.30769... recomputed; 0 < tau_bar < 0.237567 < 0.30769 <= tau_y(1) holds on the box; instance draws rounded to three decimals (instance.py:35-36). Samples: 25 seeds, all interior, 25 distinct fractions (round-20 scratch seeds20.py).", ""),
    ("E4d20-num-exception-range", "2.4-scope", "course/modules/E/E4/project.html:325-327; grader/reference.py", "PASS",
     "30000 random draws, noise volume 1e-50..1e150 (log-uniform) and cost 0..350: 0 exceptions, 0 non-finite, 0 out of [0,1] (out/range_sweep_r20.txt). A noise volume of 1e154 raises ZeroDivisionError, which is outside the stated range (the page says any exception is allowed there). Sub-1e-50 roots are inaccurate by the 240-halving cap, as the page states (sd 1e-200 returns 2.8e-73), and the page states no accuracy there.", ""),
    ("E4d20-math-recheck", "2.4-mathematics", "course/modules/E/E4/project.html:265-301 (Lemmas 1-3, Propositions 1-5)", "PASS",
     "Re-derived in round 20: Lemma 1 (g maximized at (m-p)/(aV)); Lemma 2 (Gaussian integral); Lemma 3; Proposition 1 steps (1)-(4) (the two brackets vanish; kappa = -a/(lam tau_e); tau_y formula); Proposition 2 (Corr^2 = tau_y/(tau_v+tau_y)); Proposition 3 (G = F_U - e^{ac}F_I, sign rule, G(0+) by Omega -> 1/tau_v + a^2 sigma^2/tau_v^2); Proposition 4 (three cases, closed form); Proposition 5 (dlambda/dsigma = lambda/sigma; monotone in c). The code in reference.py matches the closed forms; no algebraic defect found.", ""),
    ("E4d20-math-a6-assumed", "2.4-mathematics", "course/modules/E/E4/project.html:260 (A6), :304 (limits)", "PASS",
     "A6 is numbered and used only where the page says. It follows from the sign rule and continuity of G on (0,1] (interior case G(0+) > 0 > G(1)), so the page's 'assumes and does not prove' is accurate, not a defect.", ""),
    ("E4d20-calibration-blind", "2.6-rubric-calibration", "course/modules/E/E4/project.html:536 and :601 (data-scores); ~/.fanout/blind/E4-d.json", "PASS",
     "Blind scorer file (ruling 23) A = [2,2,1,2,1], B = [4,4,4,4,4]; official data-scores 2,2,1,2,1 and 4,4,4,4,4. Calibration rows PASS on that basis; the C4 wording is in E4d20-rubric-C4-levels.", ""),
    ("E4d20-process-scope", "2.2-prose", "course/modules/E/E4/project.html (whole page)", "PASS",
     "Process-word grep (round, verifier, ruling, fixer, builder, architect, ledger, batch, fragment, audit, reviewer, agent): no learner-text hit (one 'hypothetical agent' in a docstring, which is an economic term). Scope words (only 16, every 21, all 4, any 7, same 13, exactly 2, none 5) each checked against a computation or derivation.", ""),
    ("E4d20-delta-read", "2.9-delta", "cd4dd7df..d1083bf1: course/modules/E/E4/project.html; ledgers/E4/equivalent/*; ledgers/E4/mutants/mutant_r19_0{1,3,4}*; plans/FINAL-ARCHITECT-RULINGS.md", "PASS",
     "Every hunk of the slice-d delta read (project.html: lede :37, Lab 1 :170, Lab 2 :242, Proposition 5 :302, Lab 3 :375 and :502, Appendix :513, rubric :518 and :527, exemplar B :629; ruling 25). Grader, reference, instance, starter, alternatives and tests/labs/E4 are byte-identical to cd4dd7df (git diff empty).", ""),
    ("E4d20-hours-verifier-estimate", "2.6-hours", "course/modules/E/E4/project.html:343-350 (#hours)", "PASS",
     "Verifier estimate per component: Rung 1 0.5-1 h; Rung 2 0.5-1 h; derivation 5-8 h; solver and local tests 2-4 h; grid 1-2 h; write-up 4-5 h; self-assessment 2-3 h. Total 15-24 h, below the declared 28 by 14 to 46 percent. Hours are design targets under the verifier rulings (fail only arithmetic inconsistencies); no arithmetic inconsistency found. Noted, not failed.", ""),
    ("E4d20-cards-outside-slice", "2.9-scope", "course/modules/E/E4/cards.json (changed in the delta)", "PASS",
     "Not in slice d; not verified by this verifier (see notes). No row depends on it.", ""),
]
rows = []
for r in prev["rows"]:
    rid, loc = r["id"], r.get("location", "")
    if rid in RETIRED:
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS",
                     "evidence": "Retired by ruling 18 (round 20): " + RETIRED[rid] + ". Previous evidence: " + r.get("evidence", "")[:200]})
        continue
    if rid in OVERRIDE:
        st, ev = OVERRIDE[rid]
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": st, "evidence": ev,
                     **({"fix": "See E4d20-rubric-C4-levels." if st == "FAIL" else ""} if st != "PASS" else {})})
        continue
    changed = any(k in loc or k in rid for k in CHANGED)
    if r["status"] == "PASS" and not changed:
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS",
                     "evidence": CARRY_PREFIX + r.get("evidence", "")})
        continue
    cat = r["check"]
    ev = CAT.get(cat) or CAT.get(cat.split("-")[0]) or "Re-verified in round 20 (see the round-20 out/ logs)."
    status, fix = "PASS", ""
    if rid == "E4d-rubric-observable":
        status, fix = "FAIL", "See E4d20-rubric-C4-levels."
    row = {"id": rid, "check": cat, "location": loc, "status": status,
           "evidence": "Re-verified round 20 at d1083bf1 (cited subject changed or re-checked): " + ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)
for item in NEW:
    rid, check, loc, st, ev = item[:5]
    fix = item[5] if len(item) > 5 else ""
    row = {"id": rid, "check": check, "location": loc, "status": st, "evidence": ev}
    if st != "PASS":
        row["fix"] = fix
    rows.append(row)
gate = open(gate_path, encoding="utf-8").read().splitlines()
mutants = []
for line in gate:
    m = re.match(r"KILLED (\S+?): (.*) -> (\S+) \(seed", line)
    if m:
        mutants.append({"id": m.group(1)[:-3], "file": f"ledgers/E4/mutants/{m.group(1)}", "description": m.group(2),
                        "killed_by": m.group(3)})
fail_ids = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "E4", "slice": "d", "round": 20, "verifier": "verifier (Haiku 5.5), E4-d round 20",
    "pin": "d1083bf1", "base": "cd4dd7df (round-19 pin); delta read hunk by hunk",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE20-E4-d", "scratch": "/tmp/e4d20 (scratch only; scripts kept in ledgers/E4/scripts/E4-d-r20/)",
    "verified_at": VERIFIED_AT, "verdict": "FAIL" if fail_ids else "PASS",
    "rows": rows, "mutants": mutants, "registry_flags": [], "freshness_flags": [],
    "notes": (
        "Calibration rows cite the blind scorer file, not this verifier's scores (ruling 23). Not checked: cards.json "
        "(changed in the delta, outside slice d); the 557 registry entries outside unit E4 (live run only for E4); "
        "the full CI gate for the whole repository (ruff check/format and mypy ran repo-wide and passed); the in-browser "
        "grader on seeds other than one (page_smoke ran one seed). Measured, not proved: the r19_02 equivalence "
        "(ruling 25). Tolerance observations, not rows: the boundary test uses TOL_GAP = 1e-8 for gap at 0 "
        "(grader test_boundary_rule_holds), and the interior informativeness test uses TOL_MOMENT = 1e-8 (no page "
        "numeric tolerance is stated for interior informativeness); no mutant was authored at either tolerance."),
    "summary": (f"E4 slice d round 20 (pin d1083bf1): verdict {'FAIL' if fail_ids else 'PASS'}. Rows {len(rows)}: "
                f"PASS {sum(r['status'] == 'PASS' for r in rows)}, FAIL {len(fail_ids)}, UNVERIFIABLE 0. Mutants "
                f"{len(mutants)}, killed {sum(1 for m in mutants if m['killed_by'])}. FAIL rows: {', '.join(fail_ids)}."),
}
out = root + "/ledgers/E4/E4-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows), "mutants", len(mutants), "fail", fail_ids)
