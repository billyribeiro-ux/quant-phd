"""Assemble the round-6 FC2-d fragment from the round-5 rows, the round-6 re-runs and the round-6 new rows.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r6/build_fragment_r6.py <repo_root>
Carried rows keep their round-5 evidence with a prefix naming the subject that is byte-identical or per-card identical.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

root = sys.argv[1]
S = os.path.join(root, "ledgers", "FC2", "scripts", "FC2-d-r6")
r5 = json.load(open("/Users/billyribeiro/.fanout/frags/D-FC2-d.round5.json", encoding="utf-8"))
r5rows = {r["id"]: r for r in r5["rows"]}


def read(name: str) -> str:
    return open(os.path.join(S, name), encoding="utf-8").read().strip()


CARD_PFX = ("Carried from round 5 (course/modules/FC/FC2/cards.json per-card JSON object identical between 440ed3c and "
            "142ecfc, ledgers/FC2/scripts/FC2-d-r6/card_delta.out; the lesson file byte-identical): ")


def page_pfx(lines: str) -> str:
    return ("Carried from round 5 (course/modules/FC/FC2/project.html lines " + lines + " byte-identical between 440ed3c "
            "and 142ecfc; the only changed lines are 55 and 321): ")


CARRY_CARD = {"fc2d-r2-card-" + c: c for c in ["c010", "c132", "c020", "c030", "c041", "c051", "c061", "c071", "c082",
                                              "c092", "c102", "c112", "c120", "c142"]}
CARRY_CARD.update({"fc2d-r4-card-" + c: c for c in ["c093", "c123", "c124", "c149", "c150", "c152", "c153", "c151"]})
CARRY_CARD.update({"fc2d-r5-card-" + c: c for c in ["c005", "c055", "c154"]})
CARRY_CARD["fc2d-r2-cards-lab-numbers"] = "c012, c013, c095, c147, c148"
CARRY_CARD["fc2d-r4-cards-sample"] = "the 14 sampled cards c010 to c142 and the seven round-4 cards"

CARRY_PAGE = {
    "fc2d-r2-numbers-lab1": "70-77 and 147-162 (Lab 1 chain and printed output); grader/ unchanged",
    "fc2d-r2-numbers-lab3": "376-486",
    "fc2d-r2-numbers-exemplars": "520-634",
    "fc2d-r2-hours": "33 and 345-352; index.html byte-identical",
    "fc2d-r2-reading-keys": "653-657; references/references.json and notation/notation.json byte-identical",
    "fc2d-r2-autograder-panel-claims": "285 and 671; course/assets byte-identical",
    "fc2d-r2-hub-placement-claim": "42; index.html byte-identical",
    "fc2d-r2-rubric-C2-level2": "504-512",
    "fc2d-r2-rubric-calibration": "520-586",
    "fc2d-r2-grader-named-conditions-only": "309-316; grader/ byte-identical",
    "fc2d-r3-footer-no-upload": "285 and 671",
    "fc2d-r3-exemplar-scores-match-text": "520-521 and 584-586",
    "fc2d-r5-page-hunk-error-conditions": "309-316",
}
CARRY_GRADER = {
    "fc2d-r2-grader-messages": "grader/test_project.py and grader/reference.py (course/modules/FC/FC2/grader byte-identical)",
    "fc2d-r2-grader-over-constraint-trade-verb": "grader/test_project.py byte-identical",
    "fc2d-r3-instance-docstring-bounds": "grader/instance.py byte-identical",
}

RERUN = {
    "fc2d-r2-gate-mutate": "Re-run this round on 142ecfc: tools/mutate_graders.py --unit FC2 --seeds 0-9 (rc 0), "
                           "ledgers/FC2/scripts/FC2-d-r6/mutate_fc2_r6.out: 'mutate_graders FC2: PASS (72/72 killed)'. "
                           "The 68 prior mutants and the four round-6 mutants w6_a..w6_d (ledgers/FC2/mutants) all KILLED.",
    "fc2d-r2-gate-run-graders": "Re-run: tools/run_graders.py --unit FC2 --seeds 0-49, rc 0, ledgers/FC2/scripts/FC2-d-r6/"
                                "run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)'.",
    "fc2d-r2-gate-check-projects": "Re-run: check_projects.py --unit FC2 -> 'check_projects FC2: PASS' (check_projects_fc2.out); "
                                   "--all rc 0 with FC2 PASS (check_projects_all.out).",
    "fc2d-r2-gate-check-dag": "Re-run: check_dag.py --unit FC2 -> 'check_dag FC2: PASS'; --all rc 0 (check_dag_all.out).",
    "fc2d-r2-gate-check-pages": "Re-run: check_pages.py --unit FC2 -> 'check_pages FC2: PASS'; --all rc 0, 21 PASS lines "
                                "(check_pages_all.out).",
    "fc2d-r2-gate-run-labs": "Re-run: tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)', rc 0 (run_labs_fc2.out).",
    "fc2d-r2-lab-twins-isolated": "Re-run twins_isolated.py (python -I): lab-FC2-project-1, -2, -3 twins each run alone under "
                                  "python -I -W error: rc 0, stderr 0 bytes (twins_isolated.out).",
    "fc2d-r2-lab-page-equals-twin": "twins_isolated.out: expected block equals twin stdout for all three labs (True); page code "
                                    "equals twin for labs 1 and 3 (True). Lab 2 is a completion lab; lab2_completion_rule.py: "
                                    "blank lines 58, 60, 73 only, 'rule holds: True' (lab2_completion_rule.out).",
    "fc2d-r2-gate-page-smoke": "Re-run: tools/page_smoke.py --unit FC2 --pages project -> 'page_smoke modules/FC/FC2/project.html: "
                               "PASS', 'in-browser grader: All 90 tests pass', labs 1-3 run (page_smoke_project.out), rc 0.",
    "fc2d-r2-gate-ruff-mypy": "ruff check . -> 'All checks passed!' (ruff_check.out); ruff format --check on tests/labs/FC2, "
                              "course/modules/FC/FC2, ledgers/FC2 -> '15 files already formatted' (ruff_format_fc2.out); repo-wide "
                              "ruff format --check reports one file outside FC2, ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py "
                              "(ruff_format_repo.out). mypy --no-incremental tests/labs/FC2 -> 'Success: no issues found in 11 source "
                              "files' (mypy_labs.out). mypy --strict --no-incremental on a scratch copy (reference.py as scanner.py, "
                              "instance.py, test_project.py in /tmp/fc2d-r6-mypy) -> 'Success: no issues found in 3 source files' "
                              "(mypy_grader_strict.out).",
    "fc2d-r2-gate-pytest-fc2": "Re-run: .venv/bin/python -m pytest tests/labs/FC2 tests/test_labs.py tests/test_run_labs.py "
                               "tests/test_page_checks.py tests/test_memo_exemplars.py -k 'FC2 or fc2 or project or grader' -q, rc 0 "
                               "(pytest_fc2.out, all dots).",
    "fc2d-r2-gate-verify-refs": "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', rc 0 "
                                "(verify_refs_offline.out). Live: verify_refs.py --unit FC2 -> 'live re-verification of FC2: 3 of "
                                "560 entries, 0 problems', rc 0 (verify_refs_live_FC2.out).",
    "fc2d-r2-collect-count": "collect_count.py (python -I) on reference.py as scanner.py, seeds 0..49: 'collected 90 for 50 seeds' "
                             "(collect_count.out). project.html line 320 states 90; line 320 is unchanged.",
    "fc2d-r2-starter-suite-fails": "instances_and_links.py: starter.py as scanner.py, QF_SEED=0: '82 failed, 8 passed', rc 1 "
                                   "(instances_and_links.out).",
    "fc2d-r2-banned-phrases": "page_text_checks.py over the whole project.html (673 lines, page_text_checks.out): no banned-phrase "
                              "hit (TODO, TBD, lorem, ellipsis, for brevity, details omitted, beyond the scope, left as an exercise, "
                              "you can add more, it is important to note, studies show, experts agree, well known, obviously, clearly, "
                              "historically, roughly, approximately, let us); no we/our/us. 'about' hedges at lines 486 (about 62.67, "
                              "188/3 = 62.667, checked exactly) and 590 (about 226 and about 540 and about 63, equal to the exact "
                              "values 226, 540 and 63 cents).",
    "fc2d-r2-notation": "page_text_checks.out: no backslash macro on the page; symbols C, P, S, K, df, D and the labels P1 to P6 "
                        "are the FC2 local letters (defined on the page, line 336). The registered symbols of notation/notation.json "
                        "(T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) do not occur on the page except that "
                        "T is not used (maturity is tau). Card FC2-c103 uses Phi with the registered meaning (standard normal CDF).",
    "fc2d-r2-dag": "check_dag.py --unit FC2 -> 'check_dag FC2: PASS' (check_dag_fc2.out). The changed hunks add only internal "
                   "anchors (href #conventions and #exemplars); no concept link is added. FC2 prerequisites M4, CF1, FC1 in "
                   "curriculum/02-economics-finance-core.yaml line 399-400 (unchanged since the round-5 pin).",
    "fc2d-r2-instances": "instances_and_links.py: 40 seeds (0..19 and 1000..1019) all valid, 40 distinct (kind, index, amount, "
                         "strikes, spot, df) tuples (instances_and_links.out).",
    "fc2d-r2-grader-over-constraint-case": "run_alts.py (python -I under .venv): alt1_integer_only 50/50, alt2_slope_test 50/50, "
                                           "alt3_decimal 50/50, alt4_validate_first 50/50, alt5_floor_half 50/50, "
                                           "alt7_cross_multiplied_integers 50/50 seeds; each agrees with reference.py 3000/3000 "
                                           "on random chains (alts_r6_verifier.out). Plus alt8_forward_price_fraction 50/50 and 3000/3000 "
                                           "(alts_r6_alt8.out).",
    "fc2d-r2-alternatives-pass": "Six tracked alternatives and alt8 pass seeds 0..49 (alts_r6_verifier.out, alts_r6_alt8.out). The float "
                                 "alternative of plan 5.5 item 3 is not in the tracked set; see notes (round 5 recorded it failing "
                                 "test_parity_exact_tie_at_a_non_dyadic_discount_factor, grader/test_project.py lines 273-278, "
                                 "which enforces project.html line 308 'computed from exact fractions').",
    "fc2d-r2-mut-r7-docstrings": "mutant_docstrings.py: 72 mutants; every first docstring line names the error; changed-line counts "
                                 "2 to 8 (mutant_docstrings.out).",
    "fc2d-r2-mut-new-killed": "mutate_fc2_r6.out: v07_convexity_indices_returned_in_decreasing_order, "
                              "v08_convexity_scan_skips_first_interior_strike, v09_parity_explanation_omits_P3_no_income, "
                              "v10_convexity_gross_from_rounded_chord all KILLED.",
    "fc2d-r2-mut-r5d-resolved": "ls ledgers/FC2/mutants shows no r5_d file; r5_a, r5_b, r5_c KILLED in mutate_fc2_r6.out.",
    "fc2d-r2-mut-equivalents": "All 72 mutants are KILLED in mutate_fc2_r6.out, and a killed mutant is by definition not equivalent "
                               "to reference.py, so no listed mutant is equivalent.",
    "fc2d-r2-cards-full-scan": "cards_scan.py on 153 cards (cards_scan.out): unique ids, fronts and backs; grades T and C; lessons "
                               "L01..L08. 38 near-duplicate pairs (ratio >= 0.6). New pair FC2-c072 / FC2-c155 (0.683) reviewed: "
                               "distinct claims (c072: parity cost and payoff; c155: bound and convexity triples), both matching "
                               "L05 Lab 1 output lines 268 to 271; not a duplicate. Other top pairs as in round 5 (c005 / c154 "
                               "distinct claims, weak versus strict part of Proposition 2.2).",
    "fc2d-r2-cards-refs-numbers": "cards_scan.out: every numbered item cited by a card occurs in its lesson except FC2-c076 "
                                  "'(Section 5)', which is the L05 heading '5 Where the canon breaks' (L05.html line 314). New "
                                  "card FC2-c103 cites Proposition 1.4 (L07.html line 95).",
    "fc2d-r3-df-ppm-link": "instances_and_links.py: 18 internal href targets in project.html, 0 missing (instances_and_links.out). "
                           "The #conventions anchor (line 325) exists.",
    "fc2d-r3-mut-new-killed": "mutate_fc2_r6.out: q3_a_df_rounded_to_four_places, q3_b_gross_tie_toward_zero, "
                              "q3_c_convexity_charges_two_legs, q3_d_convexity_explanation_omits_P5 all KILLED.",
    "fc2d-r3-mut-prior-untracked": "mutate_fc2_r6.out: r3_a_half_spread_halved_again, r3_b_puts_longer_than_strikes_accepted, "
                                   "r3_c_net_field_reports_gross, r3_d_parity_explanation_names_P5_for_P4 all KILLED.",
    "fc2d-r4-mut-u4-new-killed": "mutate_fc2_r6.out: u4_a_parity_explanation_omits_P6, u4_b_cost_ignores_half_spread, "
                                 "u4_c_discounted_strike_floor_division all KILLED.",
    "fc2d-r5-mut-w5-new-killed": "mutate_fc2_r6.out: w5_a_parity_gap_truncated_toward_zero, w5_b_length_check_rejects_only_short_lists, "
                                 "w5_c_gross_rounded_up_to_ceiling all KILLED.",
    "fc2d-r5-alt7-cross-multiplied": "alts_r6_verifier.out: alt7_cross_multiplied_integers 50/50 seeds; 3000/3000 agreement with reference.py.",
    "fc2d-r5-explanation-direction-untested": "direction_probe.py: a direction-swapped parity explanation passes seeds 0..9 "
                                             "(direction_probe.out, survives all seeds). The spec (project.html line 301) "
                                             "requires the labels, not the direction; not a grader fault under the ruling; "
                                             "noted for the architect.",
    "fc2d-r3-scope-changed-hunks": "Delta 440ed3c..142ecfc inside the FC2 slice, all hunks read: project.html line 55 and line 321 "
                                   "(two sentences); cards.json FC2-c072 (back shortened) and FC2-c103 (front rewritten) changed, "
                                   "FC2-c155 added (card_delta.out). No change to grader/, labs, lessons, index.html, references, "
                                   "notation, curriculum, tools or course/assets. Each changed row is re-verified below "
                                   "(fc2d-r6-card-c072, fc2d-r6-card-c103, fc2d-r6-card-c155, fc2d-r5-page-hunk-lab1-hypothesis, "
                                   "fc2d-r6-page-line321-anchor, fc2d-r6-page-conventions-definitions).",
    "fc2d-r5-page-hunk-lab1-hypothesis": "Re-verified: line 55 changed again. New text: 'The parity gap, the synthetic forward S - K df "
                                         "and the chord (...) are defined in Conventions and assumptions, below.' and '(both terms "
                                         "are defined under P6 ...)' is retained. P6 (project.html line 333) defines the fee and the "
                                         "half-spread; the conventions (line 336) define the parity gap, the synthetic forward and "
                                         "the chord; Lab 1 numbers unchanged (fc2d-r2-numbers-lab1). Agrees.",
    "fc2d-r2-spec-questions": "Re-verified on 142ecfc: spec lines 280-336 read; the only change in that range is line 321, a "
                              "cross-reference inside the grading paragraph, which adds no spec content. The questions a student "
                              "would still have are unchanged: which strike a convexity record reports and what its gross is are "
                              "answered by Lab 1's printed output (round-5 evidence unchanged).",
}

NEW = {
    "fc2d-r6-card-c072": ("2.7", "course/modules/FC/FC2/cards.json line 499 (FC2-c072); L05.html lines 268-270, 325, 458", "PASS",
        "Changed this round (back shortened; the bound and convexity clause moved to FC2-c155). Back: 'The parity cost is zero at "
        "each of the five strikes, 80 to 120 USD. The parity payoff is zero at all 40 (strike, expiry spot) pairs (Lab 1).' Lab 1 "
        "printed output: L05.html line 268 'parity cost ... by strike: [0, 0, 0, 0, 0]' and line 269 'parity portfolio payoff "
        "nonzero at 0 of 40 (strike, expiry spot) pairs' (so zero at all 40); strikes 8000..12000 cents = 80 to 120 USD (line 325 "
        "'five strikes, 80 to 120 USD'). Grade C with basis 'Lab 1 (SIMULATED ...)' matches the C row at L05.html line 458. Agrees."),
    "fc2d-r6-card-c103": ("2.7", "course/modules/FC/FC2/cards.json line 714 (FC2-c103); L07.html lines 82-84, 95-98, 105, 362", "PASS",
        "Changed this round (front rewritten to ask for the Black-Scholes put form). Back 'P = C - S + K e^{-r tau} = K e^{-r tau} "
        "Phi(-d2) - S Phi(-d1) (Proposition 1.4)' is the displayed identity at L07.html line 98. The hypothesis 'Under A1 to A5, A7 "
        "and A8' (line 96) is carried by the front. Proposition 1.4 is graded T (line 95 data-grade=T; table line 362). Proof line 105 "
        "uses Lemma 1.2 (Phi(-x) = 1 - Phi(x)). d1, d2 are defined at lines 82-84. Phi is the registered symbol (notation.json "
        "'\\\\Phi' = standard normal CDF) with that meaning. Agrees; the card's C is defined at L07.html line 82."),
    "fc2d-r6-card-c155": ("2.7", "course/modules/FC/FC2/cards.json line 1087 (FC2-c155); L05.html lines 270-271, 286, 458", "PASS",
        "New this round (split from the back of FC2-c072). 'No. No model-free bound is violated, and no convexity triple is violated "
        "(Lab 1).' Lab 1 printed output: L05.html line 270 'model-free bound violations: 0' and line 271 'convexity in strike, triples "
        "checked 10, violated 0' (for the synthetic set). The card claims no more than the lab checks: the interpretation (line 286) "
        "says the lab tests the lower bound at D = 9/10 only and no other value of D, and the card does not generalise. Grade C with "
        "basis matches L05.html line 458. Agrees."),
    "fc2d-r6-page-line321-anchor": ("2.9", "course/modules/FC/FC2/project.html line 321 and line 517", "PASS",
        "Changed this round: '(under Two exemplars, below)' with href '#exemplars'. The anchor id=exemplars is the h3 'Two exemplars' "
        "at line 517, which precedes the self-assessment (line 636) and the exemplars it scores. Internal link check: 18 targets, 0 "
        "missing (instances_and_links.out)."),
    "fc2d-r6-page-conventions-definitions": ("2.9", "course/modules/FC/FC2/project.html line 55 and lines 325-336", "PASS",
        "Changed this round: line 55 says the parity gap, the synthetic forward S - K df and the chord are defined in Conventions and "
        "assumptions, below. Line 336 defines the parity gap C - P - (S - K df), the synthetic forward S - K df and the chord (the "
        "straight line through the calls at the two neighbouring strikes); the anchor id=conventions is at line 325. Each term named "
        "on line 55 is defined there. The changed hunk adds no concept link."),
    "fc2d-r6-mut-w6-new-killed": ("2.6", "ledgers/FC2/mutants/w6_a..w6_d; ledgers/FC2/scripts/FC2-d-r6/write_mutants_r6.py", "PASS",
        "Written this round, one line changed in reference.py each (assert count == 1). w6_a convexity counts a call on the chord "
        "(killed by test_convexity_boundary_equal_to_chord_is_not_flagged, seed 0); w6_b chord weights by own-neighbour distance "
        "(test_unequal_grid_no_false_positive, seed 0); w6_c finding kept at net zero (test_finding_with_net_exactly_zero_is_not_returned, "
        "seed 0); w6_d half-spread charged once per finding (test_scan_matches_exhaustive_oracle_second_chain, seed 0). All KILLED "
        "(mutate_fc2_r6.out, 72/72)."),
    "fc2d-r6-alt8-forward-price": ("2.6", "ledgers/FC2/scripts/FC2-d-r6/alts/alt8_forward_price_fraction.py", "PASS",
        "New alternative (plan 5.5 item 5): parity through the forward F = S / df with exact Fractions, (F - K) df, in a full "
        "reference-derived module. alts_r6_alt8.out: 50/50 seeds pass the suite; 3000/3000 agreement with reference.py."),
}


def stamp(evidence: str, prefix: str) -> str:
    return prefix + evidence


rows = []
for old in r5["rows"]:
    rid = old["id"]
    if rid == "fc2d-r2-scope-curriculum-brief":
        ev = ("Re-verified from scratch on 142ecfc (not carried). curriculum/02-economics-finance-core.yaml lines 427-429 still read "
              "'Given an embedded option-chain snapshot, detect put-call parity and convexity violations net of a stated cost "
              "model'; the curriculum is byte-identical since the round-5 pin. project.html line 285 says 'No market data is "
              "embedded ... every chain on this page and in the autograder is a simulation, labelled SIMULATED'. plans/FC2-build-plan.md "
              "B1 (line 449) records the planner's SIMULATED recommendation; the binding architect decision (plan line 634, module "
              "specifics line 635) allows SIMULATED with an honest-pending note and a DATA_REQUEST (plans/FC2-open-items.md D1, "
              "line 7). So the page follows the architect's decision, but the brief the curriculum states (embedded snapshot) is "
              "not met, and no curriculum amendment has been made. The row stays FAIL until the architect amends the brief text "
              "(curriculum/02-economics-finance-core.yaml lines 427-429) to the SIMULATED-chain scope or clears D1 with a sourced "
              "snapshot.")
        rows.append({"id": rid, "check": old["check"], "location": old["location"], "status": "FAIL", "evidence": ev,
                     "fix": "Architect: amend the brief at curriculum/02-economics-finance-core.yaml lines 427-429 to the "
                            "SIMULATED-chain scope decided in plans/FC2-build-plan.md line 634, or clear D1 with a sourced snapshot."})
    elif rid in RERUN:
        rows.append({"id": rid, "check": old["check"], "location": old["location"], "status": "PASS", "evidence": RERUN[rid]})
    elif rid in CARRY_CARD:
        rows.append({"id": rid, "check": old["check"], "location": old["location"], "status": "PASS",
                     "evidence": stamp(old["evidence"], CARD_PFX + "[" + CARRY_CARD[rid] + "] ")})
    elif rid in CARRY_PAGE:
        rows.append({"id": rid, "check": old["check"], "location": old["location"], "status": "PASS",
                     "evidence": stamp(old["evidence"], page_pfx(CARRY_PAGE[rid]) + " ")})
    elif rid in CARRY_GRADER:
        rows.append({"id": rid, "check": old["check"], "location": old["location"], "status": "PASS",
                     "evidence": stamp(old["evidence"], "Carried from round 5 (" + CARRY_GRADER[rid] + "): ")})
    else:
        raise SystemExit("unclassified round-5 row " + rid)

for rid, (check, loc, status, ev) in NEW.items():
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

mutants = []
for line in read("mutate_fc2_r6.out").splitlines():
    m = re.match(r"KILLED (\S+)\.py: (.*) -> (.*)$", line)
    if m:
        mutants.append({"name": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
assert len(mutants) == 72, len(mutants)

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for rid in r5rows:
    assert rid in ids, "round-5 id dropped: " + rid
counts = {"PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": sum(r["status"] == "FAIL" for r in rows),
          "UNVERIFIABLE": 0}
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"

notes = (
    "Round 6 on 142ecfc (round-5 pin 440ed3c). Delta inside FC2 slice: course/modules/FC/FC2/project.html line 55 and line 321; "
    "cards.json FC2-c072 and FC2-c103 changed, FC2-c155 added (card_delta.out: 150 identical, 3 differ). No change to grader/, "
    "labs, lessons, index.html, references, notation, curriculum, tools, course/assets. Every round-5 id is kept. "
    "Observations, not rows: (a) plan 5.5 item 3 (float alternative) fails the tracked exact-tie test (round-5 record: "
    "alts_r4_set_at_pin.out, alt3_float_arithmetic 0/50, grader/test_project.py lines 273-278); the page (line 308) says money is "
    "'computed from exact fractions', so the float alternative does not follow the page's stated method and was not counted; plan "
    "5.5 item 3 and project.html line 308 conflict, flagged for the architect. Six tracked alternatives plus alt8 pass. "
    "(b) Repo-wide 'ruff format --check .' fails on ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py, outside FC2. "
    "(c) Trade direction of the parity explanation is not tested (direction_probe.out); the spec requires labels, not direction. "
    "(d) Rubric C2 level 4 ('the gap between the net and zero') is implicit; Exemplar A's C3 annotation is one level off the cell "
    "wording (carried). (e) plans/FC2-open-items.md lines 26-34 still describe bid-ask-spread as a DAG defect; the curriculum now "
    "lists FC1 as a prerequisite (round-5 observation, still true of the plan text; plan not in this slice's delta). "
    "Not checked: the full repo gate (render_curriculum.py, build_site.py --check, fetch_data.py --check, full pytest, repo-wide "
    "mypy, verify_refs over all units); the self-assessment form in a live browser; lessons L01-L07 beyond the cited passages; "
    "the hub index.html beyond the placement sentence (byte-identical, not re-read)."
)

fragment = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 6 (did not build FC2)",
    "pin": "142ecfc2bd27061de18bd67e83df81e69f5c249d",
    "base": "440ed3c216725d498d9c6d7c746907d4d418198 (round-5 pin)",
    "checkout": root,
    "scratch": "/tmp/fc2d-r6-mypy (strict mypy copy); /tmp/fc2d-r6-alts (copies of the tracked alts); /tmp/fc2d-r6-alt8 (alt8)",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": f"{len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, 0 UNVERIFIABLE. 72 mutants, 72 killed. "
               f"The only FAIL is fc2d-r2-scope-curriculum-brief (curriculum brief text vs SIMULATED page; architect action).",
}
dest = os.path.join(root, "ledgers", "FC2", "FC2-d.json")
json.dump(fragment, open(dest, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", dest, "rows", len(rows), counts, verdict, "mutants", len(mutants))
