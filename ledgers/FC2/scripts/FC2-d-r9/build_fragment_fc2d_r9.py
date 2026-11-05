"""Build ledgers/FC2/FC2-d.json (round 9) from the round-8 fragment, the fresh round-9 evidence and the mutate output."""

import json
import re
import sys

ROOT = sys.argv[1]
R8 = "/Users/billyribeiro/.fanout/frags/D-FC2-d.round8.json"
PIN = "1e272e5a641f18412703b37778a44db6f7391a69"
BASE = "2d755599d8d74df292e3e43025f0458c4053802e"
O = "ledgers/FC2/scripts/FC2-d-r9"

r8 = json.load(open(R8, encoding="utf-8"))
prev = {r["id"]: r for r in r8["rows"]}

def carry(subject):
    return "Carried from round 8 (" + subject + " byte-identical since the previous pin 2d755599): "

# fresh rows: id -> (status, evidence)
FRESH = {
 "fc2d-r2-gate-mutate": ("PASS", f"{O}/mutate_fc2_r9_all.out: 'mutate_graders FC2: PASS (83/83 killed)', rc 0 (the 79 prior mutants plus the four round-9 mutants y9_a..y9_d). Re-run with --seeds 0-9 ({O}/mutate_fc2_seeds0-9.out, 79/79 before the new mutants): x8_a is KILLED by test_negative_cost_is_rejected_even_when_no_finding_is_kept, x8_b by test_two_strike_chain_still_checks_df_and_strikes_for_convexity, x8_c by test_one_strike_chain_checks_the_quote_lengths (seed 0). Round-9 fixer output (mutate_fc2_fixer_r9.out in the round-8 folder) was not trusted; this run is the verifier's own."),
 "fc2d-r2-gate-run-graders": ("PASS", f"{O}/run_graders.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.3 s)', rc 0."),
 "fc2d-r2-gate-check-projects": ("PASS", f"{O}/check_projects_fc2.out: 'check_projects FC2: PASS' rc 0; {O}/check_projects_all.out: 'check_projects FC2: PASS' rc 0."),
 "fc2d-r2-gate-check-dag": ("PASS", f"{O}/check_dag_fc2.out: 'check_dag FC2: PASS' rc 0; {O}/check_dag_all.out: 'check_dag FC2: PASS' rc 0."),
 "fc2d-r2-gate-check-pages": ("PASS", f"{O}/check_pages_fc2.out: 'check_pages FC2: PASS' rc 0; {O}/check_pages_all.out: 'check_pages FC2: PASS' rc 0."),
 "fc2d-r2-gate-run-labs": ("PASS", f"{O}/run_labs_fc2.out: 'run_labs FC2: PASS (11/11)', rc 0."),
 "fc2d-r2-lab-twins-isolated": ("PASS", "The three project twins run by this verifier with '.venv/bin/python -I -W error' from /tmp (ledgers/FC2/scripts/FC2-d-r9/page_vs_twin_r9.py): lab 1 rc 0 stderr 0 B, 16 stdout lines; lab 2 rc 0 stderr 0 B, 16 lines; lab 3 rc 0 stderr 0 B, 17 lines."),
 "fc2d-r2-lab-page-equals-twin": ("PASS", "page_vs_twin_r9.py over course/modules/FC/FC2/project.html (three data-run blocks): lab 1 0 lines differ from tests/labs/FC2/lab-FC2-project-1.py; lab 3 0 lines differ; lab 2 differs at lines 58, 60, 73 only, the three blanks ('gap = ___', 'net = ___' twice). Expected blocks equal the twins' stdout (the page interpretation text was re-read for lab 1 and lab 3)."),
 "fc2d-r2-gate-page-smoke": ("PASS", f"{O}/page_smoke_project.out: 'page_smoke modules/FC/FC2/project.html: PASS', 'in-browser grader: All 94 tests pass on seed 857373843', rc 0."),
 "fc2d-r2-gate-ruff-mypy": ("PASS", f"{O}/ruff_check_repo.out 'All checks passed!' rc 0; {O}/ruff_format_repo.out '553 files already formatted' rc 0; {O}/mypy.out 'Success: no issues found in 385 source files' rc 0 (mypy --no-incremental)."),
 "fc2d-r2-gate-pytest-fc2": ("PASS", f"{O}/pytest_fc2.out: 'pytest -q tests/test_curriculum.py tests/test_labs.py -k FC2 or fc2' 12 passed, rc 0."),
 "fc2d-r2-gate-verify-refs": ("PASS", f"{O}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' rc 0. The live unit run ('verify_refs --unit FC2') was not re-run: it needs the network and references/ is unchanged since 2d755599 (git diff empty); carried from round 8 for the live part (ledgers/FC2/scripts/FC2-d-r8/verify_refs_unit_FC2.out: 'live re-verification of FC2: 3 of 560 entries, 0 problems')."),
 "fc2d-r2-collect-count": ("PASS", f"{O}/collect_count.out: 'collected 94 for 50 seeds; first seeds [0, 1, 2, 3, 4]', rc 0 (collect_count_r9.py, python -I, reference.py as scanner.py). project.html line 320 states 94."),
 "fc2d-r2-starter-suite-fails": ("PASS", "starter.py copied as scanner.py into an empty temp dir with test_project.py and instance.py, QF_SEED=0, 'python -I -m pytest -q -W error test_project.py': '86 failed, 8 passed', rc 1."),
 "fc2d-r2-numbers-lab1": ("PASS", "Re-derived by hand this round (C-P-(S-K df) at 9000..11500: 0, 120, 0, 0, -20, 0; cost 3 x 15 = 45; nets -45, 75, -45, -45, -25, -45; chord-less-call 50, 100, -75, 75 at 9500, 10000, 10500, 11000; kept 9500 parity net 75 and 10500 convexity net 30). Line 163 'the other four parity gaps are exactly zero: at those four strikes the call and the put satisfy parity exactly' matches the four zero gaps (9000, 10000, 10500, 11500). The lab 1 twin is byte-identical to the round-8 twin."),
 "fc2d-r2-numbers-lab3": ("PASS", f"tests/labs/FC2/lab-FC2-project-3.py output this round: cost 60; gaps 226 (6500) and 540 (7000), net 166 and 480; convexity at 6000 chord less call -188/3, gross 63, net 3; 3 findings kept. Matches project.html lines 486 and 538."),
 "fc2d-r2-numbers-exemplars": ("PASS", "Exemplar B passage (project.html 521-580): cost 8+12 = 60, net 166, 480, 3, gross 226, 540, 63, discounted strikes 6175 and 6650, chord 802/3, call 330, chord less call -188/3 all match the lab 3 output above. Exemplar A (585-633): 226, 540, 63 as 'about' values match. Numbers unchanged by the round-9 hunks (only data-level attributes changed)."),
 "fc2d-r2-hours": ("PASS", "project.html line 33 data-hours-project=\"30\"; index.html line 29 data-hours-lessons=\"60\" and data-hours-project=\"30\", 30 of 90 = 33.3% (index.html line 41). Time-budget table (project.html 345-352) 2+3+5+9+3+5+3 = 30 (cells re-read this round; only the self-assessment row text changed)."),
 "fc2d-r2-banned-phrases": ("PASS", "Added lines of project.html in 2d755599..1e272e5a scanned for process words (round, now, changed, fixed, revised, updated, we, our, draft, previous): none. 'lab shows' (line 163) is pre-existing wording of the interpretation. 'about' appears only as the approximate-value wording in Exemplar A (line 590) and the Lab 3 interpretation."),
 "fc2d-r2-notation": ("PASS", "notation/notation.json has no entry D, tau or r (grep count 0), so the page's new 'D' (line 336: 'which Lesson 5 writes as D', L05.html line 55 'Write D = e^{-r tau}') conflicts with no registered meaning. The page's local symbols C, P, S, K, df are defined at lines 335-336 as before; the label P is disclosed as a label on the same line."),
 "fc2d-r2-dag": ("PASS", f"{O}/check_dag_fc2.out 'check_dag FC2: PASS' rc 0 (fresh). The round-9 hunks add no concept link (the only link text edited is the lede, whose links are unchanged); curriculum/02-economics-finance-core.yaml is unchanged since 2d755599 (git diff empty)."),
 "fc2d-r2-autograder-panel-claims": ("PASS", "Lede (project.html line 37) 'generated from the seed shown in the autograder panel': course/assets/js/grader.js line 53 prints 'Your instance seed is ${seed} (derived from your workspace ID)', so the seed is shown in the panel. Lines 285 and 671 and grader.js unchanged: carried from round 8 (no upload call; file read in the browser)."),
 "fc2d-r2-scope-curriculum-brief": ("FAIL", "Re-verified from scratch on 1e272e5: curriculum/02-economics-finance-core.yaml lines 427-429 still read 'Given an embedded option-chain snapshot, detect put-call parity and convexity violations'. The page (project.html line 285, 'No market data is embedded') and plans/FC2-build-plan.md line 635 (SIMULATED chain with a DATA_REQUEST, binding) describe a simulated chain. The yaml file is unchanged since 2d755599 (git diff empty), so the mismatch is unchanged."),
 "fc2d-r2-rubric-calibration": ("PASS", "Rubric cells (project.html 504-512) read blind: exemplar A C3 is level 2 (names the discount factor for the parity findings, line 614, no label P1 to P6, so level 3 is not met); official data-scores 2,1,2,2,1 (line 584) and data-level now 1 (the lowest criterion). Exemplar B data-scores 4,4,3,3,3 with data-level 3 (line 520). Agrees with the rubric."),
 "fc2d-r2-spec-questions": ("PASS", "The round-9 spec change at project.html line 308 states the two tie rules (signed gap toward plus infinity; gross as magnitude rounded half up). The code (reference.py: _half_up(gap) for the signed gap, _half_up(abs(gap)) for the gross, _half_up(-diff) for the convexity gross) implements exactly this, so a student who reads line 308 has the rounding rule. No new question is left open by the hunks read (lines 37, 163, 308, 320, 332-336, 348-352, 518-520, 584)."),
 "fc2d-r2-grader-messages": ("PASS", "test_project.py changed lines (the four new tests at 565-606 and the module docstring at 9-12) read in full: assertion texts state the property ('the message must name the two puts', 'a half-spread of zero is valid') and print no expected value; ValueError messages in reference.py unchanged (carried, reference.py byte-identical)."),
 "fc2d-r2-grader-named-conditions-only": ("PASS", "Every pytest.raises in test_project.py, including the four new tests (565-606), names ValueError and a condition listed at project.html lines 309-316: negative fee or half-spread (scan), df_ppm 0 and PPM+1 (convexity, two strikes), strictly increasing strikes (convexity, two strikes), one quote per strike (convexity 2 strikes; scan 1 strike)."),
 "fc2d-r2-grader-over-constraint-case": ("PASS", f"{O}/alts_r9.out: alt1..alt10 each 50/50 seeds pass the suite, and 3000/3000 random chains agree with reference.py for each alternative."),
 "fc2d-r2-grader-over-constraint-trade-verb": ("PASS", "grep of test_project.py for 'trade' finds no test on trade verbs (no match); the explanation check (test_scan_explanations_are_nonempty_and_name_the_rule) asserts rule words and labels only."),
 "fc2d-r2-alternatives-pass": ("PASS", f"{O}/alts_r9.out: ten alternative correct implementations (alt1..alt10 in ledgers/FC2/scripts/FC2-d-r8/alts, unchanged) each pass seeds 0..49 (50/50) under the 1e272e5 suite, and agree with reference.py on 3000/3000 random chains."),
 "fc2d-r2-mut-r7-docstrings": ("PASS", f"{O}/mutate_fc2_r9_all.out: all 83 mutant files open with a one-line docstring that describes the error (the output prints each first line)."),
 "fc2d-r2-mut-new-killed": ("PASS", f"{O}/mutate_fc2_r9_all.out: v07..v10 KILLED."),
 "fc2d-r2-mut-equivalents": ("PASS", f"{O}/mutate_fc2_r9_all.out: 83/83 KILLED on seeds 0..9, so every mutant differs from the reference on a tested input (no equivalent mutant in the set)."),
 "fc2d-r2-cards-full-scan": ("PASS", f"{O}/cards_scan_r9.py over course/modules/FC/FC2/cards.json (159 cards): ids unique, fronts unique. Near-duplicate fronts (SequenceMatcher ratio > 0.75): c160/c162 (0.96: call vs put lower bound), c005/c154 (0.87, both unchanged), c084/c163 (0.85: cost vs uniqueness), c066/c161 (0.83: call vs put range), c161/c162 (0.82), c126/c131, c102/c145, c069/c070, c114/c126, c042/c045. Each pair asks a different quantity; no two cards ask the same question."),
 "fc2d-r2-cards-refs-numbers": ("PASS", f"{O}/cards_scan_r9.py: every Theorem, Lemma, Proposition, Definition, Remark, Example, Assumption number on every card appears in its lesson file ('numbered references not found: 0')."),
 "fc2d-r2-card-c120": ("FAIL", "course/modules/FC/FC2/cards.json FC2-c120 (line 838): front 'For S > 0, K > 0 and tau > 0, what is the vega ...'. L08.html Lemma 2.1 (line 68-70) states 'For sigma > 0, the derivative dC/dsigma ... equals S phi(d1) sqrt(tau)'. The front omits sigma > 0, the lemma's stated hypothesis; the back states the positivity clause 'for sigma > 0' but gives the formula unqualified. Card does not carry the proposition's hypothesis as the rules require."),
 "fc2d-r3-scope-changed-hunks": ("PASS", "Every hunk changed in the slice since 2d755599 is read: project.html (hunks at 34, 37, 160-163, 317-323, 332-336, 348-352, 515-520, 581-584), test_project.py (docstring 9-12; new tests 565-606), cards.json (458, 579, 838-845, 1103-1135). Nothing else in the slice changed (instance.py, reference.py, starter.py, labs, lessons, index.html, grader.js unchanged)."),
 "fc2d-r3-mut-new-killed": ("PASS", f"{O}/mutate_fc2_r9_all.out: q3_a..q3_d KILLED."),
 "fc2d-r3-mut-prior-untracked": ("PASS", f"{O}/mutate_fc2_r9_all.out: r3_a..r3_d KILLED."),
 "fc2d-r3-exemplar-scores-match-text": ("PASS", "project.html 520 and 584 data-scores (4,4,3,3,3 and 2,1,2,2,1) agree with the official-scoring sentences (522, 586) and with the per-criterion annotations (lines 530-578 for B, 594-631 for A), read this round. data-level (3 and 1) is the lowest criterion score, which is what line 518 now says."),
 "fc2d-r4-mut-u4-new-killed": ("PASS", f"{O}/mutate_fc2_r9_all.out: u4_a..u4_c KILLED."),
 "fc2d-r5-mut-w5-new-killed": ("PASS", f"{O}/mutate_fc2_r9_all.out: w5_a..w5_c KILLED."),
 "fc2d-r5-alt7-cross-multiplied": ("PASS", f"{O}/alts_r9.out: alt7_cross_multiplied_integers.py 50/50 seeds pass the suite; 3000/3000 agreement."),
 "fc2d-r5-explanation-direction-untested": ("PASS", f"{O}/direction_probe_r9.out: a parity explanation with the trade direction swapped passes seeds 0..9 ('survives all seeds: True'). Not a FAIL: the spec requires the explanation to name the rule and the labels (project.html line 313), not the trade direction; the direction is stated in the conventions (line 336)."),
 "fc2d-r6-page-line321-anchor": ("PASS", "project.html line 321 is byte-identical to round 8 (the hunk at 317-323 changes only line 320). The anchor id=\"exemplars\" exists once (grep count 1, the h3 'Two exemplars' at line 517); the 'Two exemplars' link target is therefore present."),
 "fc2d-r6-page-conventions-definitions": ("PASS", "project.html lines 325-336 read this round: line 336 defines C, P, S, K, df and 'which Lesson 5 writes as D' (L05.html line 55 'Write D = e^{-r tau} for the discount factor'). The parity gap, synthetic forward and chord are defined in the same block (line 336). Line 55 unchanged."),
 "fc2d-r6-mut-w6-new-killed": ("PASS", f"{O}/mutate_fc2_r9_all.out: w6_a..w6_d KILLED."),
 "fc2d-r6-alt8-forward-price": ("PASS", f"{O}/alts_r9.out: alt8_forward_price_fraction.py 50/50 seeds pass; 3000/3000 agreement."),
 "fc2d-r7-cards-delta-read": ("PASS", "The cards.json delta since 2d755599 (40 lines; hunks at 458-466, 579-586, 838-845, 1103-1135) read in full this round: c066 split, c084 split, c120 and c121 front qualified, c160..c163 added. Each changed card is checked against its lesson text (see fc2d-r9-card-* rows)."),
 "fc2d-r7-mut-s7-new-killed": ("PASS", f"{O}/mutate_fc2_r9_all.out: s7_a..s7_d KILLED."),
 "fc2d-r8-alt-9-10": ("PASS", f"{O}/alts_r9.out: alt9_integer_only_parity.py and alt10_cross_multiplied_convexity_no_fraction.py each 50/50 seeds pass the suite and 3000/3000 agree with reference.py."),
 "fc2d-r8-exemplar-level-labels": ("PASS", "Fixed in 1e272e5 (outcome: fixed). project.html line 351 now reads 'compare with Exemplar B and Exemplar A'; data-level is 3 on Exemplar B (line 520) and 1 on Exemplar A (line 584), the lowest criterion score of each (B 4,4,3,3,3; A 2,1,2,2,1), and line 518 defines it. No 'exemplar level' wording remains (grep)."),
 "fc2d-r8-mut-x8-a": ("PASS", f"Fixed in 1e272e5 (outcome: fixed). x8_a KILLED on seed 0 by test_negative_cost_is_rejected_even_when_no_finding_is_kept ({O}/mutate_fc2_r9_all.out)."),
 "fc2d-r8-mut-x8-b": ("PASS", f"Fixed in 1e272e5 (outcome: fixed). x8_b KILLED on seed 0 by test_two_strike_chain_still_checks_df_and_strikes_for_convexity ({O}/mutate_fc2_r9_all.out)."),
 "fc2d-r8-mut-x8-c": ("PASS", f"Fixed in 1e272e5 (outcome: fixed). x8_c KILLED on seed 0 by test_one_strike_chain_checks_the_quote_lengths ({O}/mutate_fc2_r9_all.out)."),
 "fc2d-r7-card-c156": ("PASS", "Historical row, subject no longer exists: FC2-c156 was removed at 2d755599 (round-8 notes) and is not in cards.json at 1e272e5 (grep). Replacement cards FC2-c158 and FC2-c159 are verified in fc2d-r8-card-c158 and fc2d-r8-card-c159. Not a live claim."),
 "fc2d-r7-card-c157": ("PASS", "Historical row, subject no longer exists: FC2-c157 was removed at 2d755599 and is not in cards.json at 1e272e5 (grep). Replacement card FC2-c159 is verified in fc2d-r8-card-c159. Not a live claim."),
}

NEW_ROWS = [
 ("fc2d-r9-card-c066", "card", "course/modules/FC/FC2/cards.json FC2-c066 (line 458); L05.html Theorem 2.2(a) (line 84-95)", "PASS", "Front 'Under A1 to A5 and (N), what range does a European call price C lie in?' carries Theorem 2.2's hypotheses (A1, A2, A3, A4, A5, (N)). Back '0 ≤ C ≤ S (Theorem 2.2(a))' matches the theorem's item (a) and its proof (L05.html line 95)."),
 ("fc2d-r9-card-c084", "card", "course/modules/FC/FC2/cards.json FC2-c084 (line 579); L06.html Theorem 1.4(b) (line 78-82)", "PASS", "Front 'Under A1, A2, A3, A5 and A6, what is the cost of the one-period replicating portfolio?' carries the hypotheses of Theorem 1.4. Back 'V_0 = (q V_1(u) + (1 − q) V_1(d)) / R_f with q = (R_f − d)/(u − d), and 0 < q < 1 (Theorem 1.4(b))' matches the theorem's item (b) (L06.html line 80 and its proof)."),
 ("fc2d-r9-card-c121", "card", "course/modules/FC/FC2/cards.json FC2-c121 (line 845); L08.html line 55 (fixed inputs S, K, r, tau) and Lemma 2.2 (line 87-89)", "FAIL", "Front 'For S > 0, K > 0 and tau > 0, what are the limits of the Black–Scholes call value as sigma tends to infinity and to zero?' omits the rate r, which L08.html line 55 fixes ('Fix the spot S > 0, the strike K > 0, the rate r and the maturity tau > 0'). The back's limit L = max(S − K e^{−r tau}, 0) depends on r, so the card is not self-contained. The limits themselves (S as sigma grows, L as sigma falls to 0) agree with Lemma 2.2."),
 ("fc2d-r9-card-c160", "card", "course/modules/FC/FC2/cards.json FC2-c160 (line 1107); L05.html Theorem 2.2(b) (line 88)", "PASS", "Front carries A1 to A5 and (N) and defines D = e^{−r tau} (L05.html line 55). Back 'C ≥ max(S − DK, 0) (Theorem 2.2(b))' matches item (b)."),
 ("fc2d-r9-card-c161", "card", "course/modules/FC/FC2/cards.json FC2-c161 (line 1114); L05.html Theorem 2.2(c) (line 91)", "PASS", "Front carries the hypotheses and D. Back '0 ≤ P ≤ DK (Theorem 2.2(c))' matches item (c)."),
 ("fc2d-r9-card-c162", "card", "course/modules/FC/FC2/cards.json FC2-c162 (line 1121); L05.html Theorem 2.2(d) (line 92)", "PASS", "Front carries the hypotheses and D. Back 'P ≥ max(DK − S, 0) (Theorem 2.2(d))' matches item (d)."),
 ("fc2d-r9-card-c163", "card", "course/modules/FC/FC2/cards.json FC2-c163 (line 1128); L06.html Theorem 1.4(a) (line 78) and its proof (line 80)", "PASS", "Front carries A1, A2, A3, A5, A6. Back 'Yes, because u ≠ d and S_0 > 0 (Theorem 1.4(a))' matches the proof of item (a) in L06.html line 80."),
 ("fc2d-r9-cards-changed-set-coverage", "card", "cards.json changed hunks 458, 579, 838-845, 1103-1135", "PASS", "Every changed or added card in the round-9 delta is covered: c066, c084, c120, c121, c160, c161, c162, c163. Cards with unchanged entries are carried. No duplicate ids or fronts (cards_scan_r9.py)."),
 ("fc2d-r9-tie-rule-prose", "prose", "project.html lines 59-63, 170-173 (code docstrings of Lab 1 and Lab 2) vs line 308 (spec)", "PASS", f"Lab 1/2 docstrings say 'a tie going toward plus infinity' for every money value; the spec at line 308 adds that a gross amount is the magnitude of the gap rounded half up. For a non-negative gross, round-half-up and round-toward-plus-infinity are the same integer, and the lab computes round_cents(abs(gap)) (tests/labs/FC2/lab-FC2-project-1.py) which is the spec's rule. No contradiction with the printed output; wording is looser than line 308. Observation, not a FAIL."),
 ("fc2d-r9-grader-weak-assertion", "grader", "course/modules/FC/FC2/grader/test_project.py lines 595-606 (test_one_strike_chain_checks_the_quote_lengths)", "PASS", "The new assertion 'assert \"2\" in str(caught.value)' is weak (any message containing the digit 2 passes), but the named condition is covered: the reference message 'calls and puts need one quote per strike: 1 strikes, 1 calls, 2 puts' is checked by the mutate gate (x8_c KILLED). Observation only."),
 ("fc2d-r9-mut-y9-new-killed", "mutant", "ledgers/FC2/mutants/y9_a..y9_d", "PASS", f"Four new student-error mutants written this round (y9_a discounted strike rounded to a cent; y9_b convexity chord rounded before the test; y9_c convexity trades two legs; y9_d convexity kept at zero net). All four KILLED on seed 0 ({O}/mutate_fc2_r9_all.out)."),
 ("fc2d-r9-alternatives-rerun", "alternative", "ledgers/FC2/scripts/FC2-d-r8/alts (alt1..alt10, unchanged)", "PASS", f"{O}/alts_r9.out: all ten pass 50/50 seeds under the 1e272e5 suite and agree with reference.py on 3000/3000 random chains each."),
]

rows = []
for r in r8["rows"]:
    rid = r["id"]
    if rid in FRESH:
        st, ev = FRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev,
                     **({"fix": r.get("fix", "")} if st == "FAIL" else {})})
    else:
        subj = r["location"]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": carry(subj) + r["evidence"]})
for rid, check, loc, st, ev in NEW_ROWS:
    rows.append({"id": rid, "check": check, "location": loc, "status": st, "evidence": ev,
                 **({"fix": "Amend the card front to 'For S > 0, K > 0, r, tau > 0 ...' (add the rate r fixed by L08.html line 55)."} if rid.endswith("c121") and st == "FAIL" else {})})

fails = [r for r in rows if r["status"] != "PASS"]
for r in fails:
    if r["id"] == "fc2d-r2-card-c120":
        r["fix"] = "Add 'for sigma > 0' to the front, e.g. 'For S > 0, K > 0, tau > 0 and sigma > 0, what is the vega ...?' (Lemma 2.1, L08.html line 68-70)."
    if r["id"] == "fc2d-r2-scope-curriculum-brief":
        r["fix"] = "Architect: amend the brief in curriculum/02-economics-finance-core.yaml lines 427-429 to the SIMULATED-chain scope in plans/FC2-build-plan.md line 635, or clear D1 with a sourced snapshot."
    r.setdefault("fix", "")

mut_lines = open(f"{ROOT}/{O}/mutate_fc2_r9_all.out", encoding="utf-8").read().splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"KILLED (\S+): (.*) -> (.*)$", line)
    if m:
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})
survivors = [line for line in mut_lines if line.startswith("SURVIVED")]
assert len(mutants) == 83 and not survivors, (len(mutants), survivors)

summary_counts = {"rows": len(rows), "PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": len(fails)}
frag = {
 "unit": "FC2",
 "slice": "FC2-d",
 "round": 9,
 "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 9 (did not build FC2)",
 "pin": PIN,
 "base": f"{BASE} (round-8 pin); the delta inside FC2-d is listed in notes",
 "checkout": ROOT,
 "scratch": f"{O}/ (round-9 probes, alternatives run, collect count, card scan, page-vs-twin check, direction probe, mutate outputs)",
 "verified_at": "2026-11-05T01:15:35+00:00",
 "verdict": "FAIL" if fails else "PASS",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": (
  "Round 9 on pin 1e272e5 (round-8 pin 2d75559). Delta inside FC2-d (git diff 2d75559 1e272e5 on the slice files): "
  "project.html (lede seed wording line 37; lab 1 interpretation line 163; grading count 90 to 94 line 320; hours table "
  "self-assessment wording 351; exemplar intro 518; data-level 3 and 1 on lines 520 and 584); grader/test_project.py (module docstring "
  "9-12 states two tie rules; four new tests at 565-606); cards.json (c066 split to c066 and c160-c162 wording; c084 split to c084 and c163; "
  "c120 and c121 fronts qualified; c160-c163 added; c156 and c157 absent since 2d75559). No change to instance.py, reference.py, starter.py, "
  "the labs twins, lessons, index.html, grader.js, notation, references, curriculum/02 or plans. Round-8 FAIL rows fixed: "
  "fc2d-r2-gate-mutate (83/83 now), fc2d-r8-mut-x8-a/b/c, fc2d-r8-exemplar-level-labels. Still FAIL: fc2d-r2-scope-curriculum-brief. "
  "New FAIL: fc2d-r2-card-c120 (front omits sigma > 0, the lemma's stated hypothesis) and fc2d-r9-card-c121 (front omits the fixed rate r). "
  "Observations (not rows): (a) the lab 1 and lab 2 docstrings say 'a tie going toward plus infinity' for every money value, looser than "
  "line 308 but consistent with the code for non-negative grosses; (b) the explanation direction is still untested by the suite (not required by the spec); "
  "(c) the one-strike length test asserts only that the digit 2 appears in the message. Not run: the full repo gate (render_curriculum.py, "
  "build_site.py --check, fetch_data.py --check, run_graders for other units, pytest for all of tests/, verify_refs live for FC2); "
  "verify_refs --unit FC2 (live) was not re-run because references/ is unchanged since 2d75559; the collect-only on the grader directory alone errors by design (needs scanner.py) and was replaced by collect_count_r9.py, which copies reference.py as scanner.py."
 ),
 "summary": (f"{summary_counts['rows']} rows: {summary_counts['PASS']} PASS, {summary_counts['FAIL']} FAIL. "
             "FAIL: fc2d-r2-scope-curriculum-brief (curriculum brief still says 'embedded snapshot'), fc2d-r2-card-c120 (vega card front omits sigma > 0), "
             "fc2d-r9-card-c121 (limits card front omits the fixed rate r). Mutants: 83, all KILLED on seeds 0-9 (4 new: y9_a..y9_d)."),
}
json.dump(frag, open(f"{ROOT}/ledgers/FC2/FC2-d.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "fails", [r["id"] for r in fails], "mutants", len(mutants))
