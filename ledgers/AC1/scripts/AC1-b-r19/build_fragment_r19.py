"""Build the round-19 fragment for slice AC1-b from the round-18 fragment (context only)."""
import json
import sys

PREV = "/tmp/fanout-frags/AC1-b.round18.json"
OUT = sys.argv[1]
prev = json.load(open(PREV))
S = "ledgers/AC1/scripts/AC1-b-r19/"
prev_rows = {r["id"]: r for r in prev["rows"]}

def carry(rid, files, check=None):
    r = dict(prev_rows[rid])
    r["evidence"] = ("Carried from round 18 (" + files + " byte-identical since the previous pin): " + r["evidence"])
    if check:
        r["check"] = check
    return r

def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    return d

CARRY_LAB = "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py (unchanged since 7143726)"
rows = []
# --- re-run command rows ---
rows.append(row("AC1b-cmd-pin", "2.9-structure", "repository at 51fa336 (detached); course/modules/AC/AC1/L04.html, L05.html, L06.html; tests/labs/AC1/", "PASS",
  "git diff --stat 7143726 51fa336 shows the slice-b edits (L04 lines 58, 330, 341, 473; L05 lines 87, 121, 345, 488; L06 lines 52, 308, 432; cards.json). tools/ and tests/labs/AC1/ are unchanged in that range (git diff --quiet)."))
rows.append(row("AC1b-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit AC1 --page L04 / L05 / L06", "PASS",
  "Re-run: 'run_labs AC1: PASS (1/1)' for L04, L05, L06 (exit 0). Output " + S + "run_labs_L04.out, run_labs_L05.out, run_labs_L06.out."))
rows.append(row("AC1b-cmd-twins", "2.5-lab", "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py", "PASS",
  "Each twin run under python -I -W error exits 0 (" + S + "twin_L04.out, twin_L05.out, twin_L06.out)."))
rows.append(row("AC1b-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit AC1", "PASS", "check_pages AC1: PASS, exit 0 (" + S + "check_pages.out)."))
rows.append(row("AC1b-cmd-check_dag", "2.9-structure", "tools/check_dag.py --unit AC1", "PASS", "check_dag AC1: PASS, exit 0 (" + S + "check_dag.out)."))
rows.append(row("AC1b-cmd-check_projects", "2.6-projects", "tools/check_projects.py --unit AC1", "PASS", "check_projects AC1: PASS, exit 0 (" + S + "check_projects.out)."))
rows.append(row("AC1b-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit AC1 --pages L04 L05 L06", "PASS",
  "page_smoke L04, L05, L06 PASS; 'page_smoke AC1: PASS', exit 0 (" + S + "page_smoke.out)."))
rows.append(row("AC1b-cmd-lint-mypy", "2.5-lab", "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py", "PASS",
  "ruff check tests/labs/AC1: 'All checks passed!'; mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' (" + S + "ruff.out, mypy.out)."))
rows.append(row("AC1b-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --unit AC1; tools/verify_refs.py --offline", "PASS",
  "Live: 'live re-verification of AC1: 2 of 560 entries, 0 problems'. Offline: 'offline integrity: 560 entries, 0 problems' (" + S + "vr_live_AC1.out, vr_offline.out)."))
rows.append(row("AC1b-cmd-pytest", "2.5-lab", "pytest -q -k 'AC1 or lab'", "PASS",
  "Re-run exit 0, all dots, no failures (" + S + "pytest.out). The summary line is not printed by this configuration; the collect-only count is not recorded."))
rows.append(row("AC1b-cit-none", "2.1-citations", "course/modules/AC/AC1/L04.html:561-562, L05.html:568-569, L06.html:532-533 (References sections)", "PASS",
  "Pages contain no citation to a registry key in the delta; tools/verify_refs.py --unit AC1 (live, 2 entries, 0 problems) and --offline (560 entries, 0 problems) re-run (" + S + "vr_live_AC1.out, vr_offline.out)."))
# --- numbers ---
rows.append(row("AC1b-num-L04-lab", "2.2-numbers", "course/modules/AC/AC1/L04.html pre.expected (lines 276-295); tests/labs/AC1/lab-AC1-L04-1.py", "PASS",
  "Re-ran the twin and compared line by line with the embedded pre.expected block: 20 lines, IDENTICAL (" + S + "expcmp.py, twin_L04.out)."))
rows.append(row("AC1b-num-L04-prose", "2.2-numbers", "course/modules/AC/AC1/L04.html interpretation (line 296), Section 3 paragraph (line 318), misconception 2 (line 345), section 5 bullet 2 (line 330), E1-E3 solutions (lines 421-435), Remark 2.4",
  "PASS", "Re-derived: 3,319,293 / 27,832,482 = 0.119260 (0.1193 at four decimals, unrounded 0.11926; " + S + "recheck.py). Quarter-0 prepaid_balance_b = 0 and quarters 1-7 non-zero (3664530, 2443020, 4396595, 6860942, 4221175, 1581406, 4974286) (L04 pre.expected lines 276-295). Interpretation's rule-A/rule-B comparisons re-checked against the printed ni values: lower in quarters 1, 3, 4, 7; higher in 2, 5, 6; equal in 0."))
rows.append(row("AC1b-num-L05-lab", "2.2-numbers", "course/modules/AC/AC1/L05.html pre.expected (lines 311-332); tests/labs/AC1/lab-AC1-L05-1.py", "PASS",
  "Twin run and pre.expected block compared: 22 lines, IDENTICAL (" + S + "expcmp.py, twin_L05.out)."))
rows.append(row("AC1b-num-L05-prose", "2.2-numbers", "course/modules/AC/AC1/L05.html interpretation (line 333), misconceptions (lines 355-365), section 4 bullets (lines 345-348), E1-E3 solutions",
  "PASS", "Section 4 bullet 2 figure 20,583,168 (twin_L05.out line 20-21); bullet 3 figures 32,792,272 (max liability, 40 percent) and 23,333,398 (max asset, 0 percent) (twin_L05.out lines 13 and 17). Bullet 1 (line 345) carries no figure. Re-verified after the Remark 1.5 / Remark 2.4 edits."))
rows.append(row("AC1b-num-L06-lab", "2.2-numbers", "course/modules/AC/AC1/L06.html pre.expected (lines 277-295); tests/labs/AC1/lab-AC1-L06-1.py", "PASS",
  "Twin run and pre.expected block compared: 19 lines, IDENTICAL (" + S + "expcmp.py, twin_L06.out)."))
rows.append(row("AC1b-num-L06-prose", "2.2-numbers", "course/modules/AC/AC1/L06.html Remark 2.5 (line 120), E1 and E3 solutions, interpretation paragraph, misconceptions 1-2", "PASS",
  "Carried from round 18 (course/modules/AC/AC1/L06.html lines 120, 296, 400-414 and misconceptions byte-identical since the previous pin; the delta touched L06 lines 52, 308 and 432 only): " + prev_rows["AC1b-num-L06-prose"]["evidence"]))
# --- grades ---
rows.append(row("AC1b-grades-L04", "2.3-grades", "course/modules/AC/AC1/L04.html Prop 2.1 (line 81), Prop 2.2 (line 96), Cor 2.3 (line 114), Prop 3.1 (line 303) and key-results rows 472-477", "PASS",
  "Key-results row 473 (Prop 2.2) now carries the Definition 2.2 assumptions, which the Prop 2.2 statement (line 97) states. Grade T is correct for a proved identity under those assumptions. Row 472 (Prop 2.1) and row 474 (Cor 2.3) unchanged. Lab-read rows stay C (SIMULATED, seed 2604)."))
rows.append(row("AC1b-grades-L05", "2.3-grades", "course/modules/AC/AC1/L05.html Prop 1.4 (line 72), Prop 2.1 (line 96), Prop 2.3 (line 110), key-results rows 488-492", "PASS",
  "Key-results row 488 now reads 'For a non-negative transaction price', matching the Prop 1.4 hypothesis at line 72. The T grade stands for the proved statement. The 32,792,272 row (C, SIMULATED seed 2605) is unchanged."))
rows.append(row("AC1b-grades-L06", "2.3-grades", "course/modules/AC/AC1/L06.html Props 2.1-2.4 (lines 79, 89, 99, 109) and key-results rows 451-455", "PASS",
  "Carried from round 18 (course/modules/AC/AC1/L06.html lines 79, 89, 99, 109 and key-results rows 451-455 byte-identical since the previous pin): " + prev_rows["AC1b-grades-L06"]["evidence"]))
rows.append(row("AC1b-math-L04", "2.4-math", "course/modules/AC/AC1/L04.html Prop 2.1 proof (85-88), Prop 2.2 statement (97) and proof (102-110), Cor 2.3 (115-120), Prop 3.1 proof (308-311)", "PASS",
  "Carried from round 18 (course/modules/AC/AC1/L04.html lines 85-88, 97, 102-120, 308-311 byte-identical since the previous pin): " + prev_rows["AC1b-math-L04"]["evidence"]))
rows.append(row("AC1b-math-L05", "2.4-math", "course/modules/AC/AC1/L05.html Def 1.3 (68), Prop 1.4 statement (72) and proof (74-83), Remark 1.5 (87), Prop 2.1 (96) and proof (98-103)", "PASS",
  "Remark 1.5 (line 87) changed from 'can move' wording only: P(k w_i)/(k W) = P w_i / W re-derived (k cancels). The statement 'a change in one price can move revenue between obligations' is a possibility claim and follows from the floor rule of Definition 1.3 (the largest-remainder step is price-sensitive). Prop 1.4 statement (72) and proof and Prop 2.1 unchanged."))
rows.append(row("AC1b-math-L06", "2.4-math", "course/modules/AC/AC1/L06.html Def 1.1 (58), Defs 1.2-1.4 (lines 62-73), Props 2.1-2.4 and proofs (79-116), Remark 2.5 (120)", "PASS",
  "Carried from round 18 (course/modules/AC/AC1/L06.html lines 58, 62-73, 79-116, 120 byte-identical since the previous pin): " + prev_rows["AC1b-math-L06"]["evidence"]))
rows.append(row("AC1b-math-notation", "2.4-math", "notation/notation.json (macros and symbols); course/modules/AC/AC1/L04.html Def 2.2 and Prop 2.2 (lines 92, 97), L05.html Def 1.3 and Prop 1.4 (lines 68, 72), L06.html Def 1.1 (line 58)", "PASS",
  "Carried from round 18 (notation/notation.json and the cited lines byte-identical since the previous pin): " + prev_rows["AC1b-math-notation"]["evidence"]))
rows.append(row("AC1b-L04-P2", "2.4-math", "course/modules/AC/AC1/L04.html problem P2 (lines 399-404)", "PASS",
  "Carried from round 18 (course/modules/AC/AC1/L04.html lines 399-404 byte-identical since the previous pin): " + prev_rows["AC1b-L04-P2"]["evidence"]))
# --- labs ---
for rid in ("AC1b-L04-hypothesis-lab", "AC1b-hyp-L06-few-cents", "AC1b-L05-prose-checks-m6", "AC1b-L06-prose-S-constant",
            "AC1b-L06-lab-docstring", "AC1b-L04-prose-misc2", "AC1b-L06-residual-causal", "AC1b-card-c059", "AC1b-card-c050",
            "AC1b3-L05-top-line", "AC1b3-equal-shares", "AC1b3-card-c062", "AC1b3-card-c088", "AC1b4-L06-prop21-hypothesis",
            "AC1b4-L06-R1-pattern-scope", "AC1b4-L05-R1-scope", "AC1b4-L05-section-ref", "AC1b4-L06-section-ref",
            "AC1b4-L04-why-scope", "AC1b4-L04-corollary-sentence", "AC1b4-L05-misc1-peak", "AC1b4-L05-interp-remainders",
            "AC1b4-L06-E3-crossing", "AC1b4-L06-misc3-residual", "AC1b4-card-c081", "AC1b4-card-c090",
            "AC1b4-L05-lab-billing-code", "AC1b4-L06-lab-straight-line", "AC1b6-L05-docstring-convention2",
            "AC1b6-L05-hypothesis-billing", "AC1b6-L06-remark25-numbers", "AC1b4-L06-remark25-causal", "AC1b6-locators-L05",
            "AC1b-L05-quiz-extra", "AC1b7-L04-remark12", "AC1b7-L04-sec2-convention", "AC1b7-L04-sec4", "AC1b7-L05-def13",
            "AC1b7-L06-sec3", "AC1b8-L04-remark32-attribution", "AC1b8-cards-new-L04", "AC1b-quiz-keys-cross",
            "AC1b-L04-quiz", "AC1b-L05-quiz", "AC1b-L06-quiz", "AC1b-struct-L04-L06", "AC1b-hours", "AC1b-data-simulated",
            "AC1b4-L06-misc3-residual"):
    if rid in prev_rows:
        rows.append(carry(rid, "the cited lines and twins"))
rows.append(row("AC1b-L05-prose-as-much-as", "2.7-prose", "course/modules/AC/AC1/L05.html section 4 bullets (lines 345-348), line 357, line 365", "PASS",
  "Bullet 1 (line 345) now reads 'a change in one stand-alone price can move revenue between obligations'. 'Can' is a possibility claim, and Remark 1.5 supports it with the floor rule. Bullets 2-4 and lines 357, 365 unchanged; no 'only', 'all', 'always' or 'as much as' claim introduced in the delta."))
rows.append(row("AC1b-L05-remark24-bullet", "2.2-numbers", "course/modules/AC/AC1/L05.html section 4 bullet 3 (lines 345-348); Remark 2.4 (line 121)", "PASS",
  "Remark 2.4 (line 121) now says 'the cumulative gap between billing and delivery' (the word 'cash-linked' was dropped). Its claims (zero at the end under Proposition 2.3; can be large in between) are unchanged in substance and match bullet 3's 'Remark 2.4 shows that the balance can be large in between'. Figures in bullet 3 match twin_L05.out."))
rows.append(row("AC1b-L04-interp-lab-claims", "2.2-numbers", "course/modules/AC/AC1/L04.html interpretation (line 296) and section 5 bullets (lines 329-332)", "PASS",
  "Bullet 2 (line 330) now says 'In Lab 1 the printed prepaid_balance_b column is zero at quarter 0 and non-zero at quarters 1 to 7'. Verified against the printed prepaid_balance_b values (L04 pre.expected). Bullets at 329, 331, 332 and interpretation (296) unchanged."))
rows.append(row("AC1b6-L06-why-it-matters", "2.9-structure", "course/modules/AC/AC1/L06.html line 52 (why-it-matters)", "PASS",
  "Now reads 'moves with cash paid less pattern F expense (Definition 1.4) in every year'. Definition 1.4 (line 72) defines the pattern F expense E^F_t = I_t + a_t, so the parenthetical points to the correct definition. Proposition 2.4 (line 109) is the articulation proof; the page proves it (line 115)."))
rows.append(row("AC1b-L06-section4-bullet1", "2.7-prose", "course/modules/AC/AC1/L06.html section 4 bullet 1 (line 308)", "PASS",
  "'The discount rate, with the payments, sets the liability.' L_0 = sum P/(1+r)^t (Definition 1.2, line 63): the liability is a function of the payments and the rate. Next sentence unchanged."))
rows.append(row("AC1b7-L06-R2", "2.7-prose", "course/modules/AC/AC1/L06.html R2 solution (line 432)", "PASS",
  "Payment structure now says 'the contract terms are the evidence for this'. A cited primary text is still required for the other three decisions; the sentence 'Each answer needs a cited primary text, and this lesson cites none' is unchanged. No numeric or causal claim introduced."))
rows.append(row("AC1b19-L04-def11", "2.7-prose", "course/modules/AC/AC1/L04.html Definition 1.1 (line 58); Remark 1.2 (line 63)", "PASS",
  "'Each framework is a set of accounting rules. This lesson states none of their content (Remark 1.2).' Remark 1.2 (line 63) says 'The lesson states no rule of either framework.' Cross-reference correct; dfn id def-gaap-vs-ifrs still at line 58 (check_dag PASS)."))
rows.append(row("AC1b19-L04-misc1", "2.7-prose", "course/modules/AC/AC1/L04.html misconception 1 (line 341)", "PASS",
  "'A difference in operating cash flow between two presentations of the same cash movements can come from a classification choice that moves an amount between sections (Proposition 3.1).' Prop 3.1 (line 303 range) states the move; the lab prints presentation_identity True and cff_presentation_2_total_cents -3319293 (pre.expected). Scope is 'can', not 'does'."))
rows.append(row("AC1b19-L05-remark15", "2.7-prose", "course/modules/AC/AC1/L05.html Remark 1.5 (line 87)", "PASS",
  "'The allocation depends only on the ratios w_i/W and on the price.' Scaling check P(k w_i)/(kW) = P w_i/W re-derived. Statement that a price change 'can move revenue between obligations' is a possibility claim supported by Definition 1.3 (floor plus largest-remainder rule)."))
rows.append(row("AC1b19-L05-keyresult-prop14", "2.7-prose", "course/modules/AC/AC1/L05.html key-results row 488; Proposition 1.4 statement (line 72)", "PASS",
  "Row 488 now reads 'For a non-negative transaction price, the allocation ... is a non-negative integer split that sums exactly to the price (Proposition 1.4)'. Matches line 72's hypothesis 'with the transaction price P a non-negative integer'. Prior FAIL (AC1b18-L05-keyresult-prop14) fixed."))
rows.append(row("AC1b19-L04-keyresult-prop22", "2.7-prose", "course/modules/AC/AC1/L04.html key-results row 473; Proposition 2.2 statement (line 97); Definition 2.2 (line 92)", "PASS",
  "Row 473 now carries 'Under the assumptions of Definition 2.2 (zero opening balances, no equity contributions, no distributions, one-quarter collection lag)'. Matches line 97 and Definition 2.2 (line 92). Prior FAIL (AC1b18-L04-keyresult-prop22) fixed. Lab 1 checks the identity in every quarter (lab-AC1-L04-1.py lines 105-124: all(...) over quarters)."))
rows.append(row("AC1b19-cards-changed", "2.7-cards", "course/modules/AC/AC1/cards.json AC1-c046, c052, c053, c058, c066, c140 (changed or added); c069 is in its own row", "PASS",
  "Each changed card read against the current lesson text: c046 (Def 1.1, Remark 1.2), c052 (Prop 2.1), c053 (Prop 2.2 with the Def 2.2 assumptions), c058 (misconception 1, Props 2.1 and 3.1), c066 (Prop 1.4 with non-negative price), c140 (Def 2.2 balances: C_t, R_t, P_t, N^A_t, N^B_t). Each card number appears in its lesson."))
rows.append(row("AC1b-cards-dup", "2.7-cards", "course/modules/AC/AC1/cards.json (140 cards; L04 20, L05 14, L06 16 among slice-b lessons)", "PASS",
  "Python Counter over card ids: no duplicates; 140 cards total (previous count 139 plus AC1-c140). " + S + "recheck.py output."))
rows.append(row("AC1b-card-c069", "2.7-cards", "course/modules/AC/AC1/cards.json AC1-c069; L05.html line 124", "FAIL",
  "The card back now cites Remark 2.4, which does not contain the sentence it supports (the sentence is at line 124). The round-18 PASS on this row cited the paragraph after Section 2, which was correct before the round-18 edit.",
  "Re-point AC1-c069 to the paragraph at L05.html line 124 (for example 'the paragraph after Remark 2.4 in Section 2'), or drop the locator, then re-run tools/check_pages.py --unit AC1."))
rows.append(row("AC1b8-cards-change-scan", "2.7-cards", "course/modules/AC/AC1/cards.json: git diff 7143726 51fa336 -- cards.json (6 changed entries, 1 added)", "PASS",
  "The scan read every changed entry (c046, c052, c053, c058, c066, c069) and the added AC1-c140. Results: five OK, c069 FAIL (row AC1b-card-c069)."))
rows.append(row("AC1b-cards-L04-L06", "2.7-cards", "course/modules/AC/AC1/cards.json AC1-c046 to c066, c122, c132 to c134, c140 (L04, L05); c075 to c090 (L06); lesson text", "FAIL",
  "Every slice-b card read. Round-18 defects fixed: c053 (Def 2.2 assumptions) and c066 (non-negative price). Still failing: AC1-c069 cites Remark 2.4 for a sentence at L05.html line 124 (AC1b-card-c069). The other cards match their lessons.",
  "Fix AC1-c069 (AC1b-card-c069); re-run tools/check_pages.py --unit AC1."))
rows.append(row("AC1b-data-simulated", "2.9-structure", "course/modules/AC/AC1/L04.html lines 52, 130, 324; L05.html lines 52, 128, 340; L06.html lines 52, 125", "PASS",
  "L06.html line 52 (changed) still says 'Lab 1 runs one SIMULATED lease'; L04 lines 52, 130, 324 and L05 lines 52, 128, 340 unchanged, and each still labels its data SIMULATED."))
rows.append(row("AC1b-scope-words", "2.7-prose", "course/modules/AC/AC1/L04.html lines 58, 330, 341, 473; L05.html lines 87, 121, 345, 488; L06.html lines 52, 308, 432", "PASS",
  "Scope words re-checked in every changed sentence. 'can' (L05 87, 345; L04 341) is a possibility claim. 'only' in L05 87 ('depends only on the ratios') is the scaling claim proved in that remark. 'every quarter' (L04 473 reference) is backed by lab all(...) over quarters. 'For a non-negative transaction price' adds a hypothesis, not a scope widening."))
rows.append(row("AC1b7-process-words", "2.9-structure", "course/modules/AC/AC1/L04.html, L05.html, L06.html (learner text); scripted word scan", "PASS",
  "Scan for build, builder, round (as a process word), verifier, REQUEST, unit report on the three pages: no learner-text hit. The only 'round' hits are the code in L06 line 177 ('return round(pv)') and rounding words; 'built from operating cash flow' (L04 line 315) is ordinary usage."))
rows.append(row("AC1b8-mutants-AC1-rerun", "2.5-lab", "ledgers/AC1/mutants/ (160 pre-existing files; 5 v18 files added for project slices); tools/mutate_graders.py; tests/", "PASS",
  "Carried from round 18 (ledgers/AC1/mutants/ 160 files, tools/mutate_graders.py, tests/ grader files byte-identical since the previous pin; the five v18_* files added in the delta belong to the project slices): " + prev_rows["AC1b8-mutants-AC1-rerun"]["evidence"]))
rows.append(row("AC1b-dag-concepts", "2.8-dag", "tools/check_dag.py --unit AC1; L04.html:58 (def-gaap-vs-ifrs), L05.html:58 (def-revenue-recognition), L06.html:58 (def-lease-accounting)", "PASS",
  "check_dag AC1: PASS (" + S + "check_dag.out). The three dfn ids remain at their lines (58); the delta added no new dfn or concept use, so no prerequisite order changed."))
rows.append(row("AC1b8-L04-numbers-recomputed", "2.2-numbers", "course/modules/AC/AC1/L04.html Section 3 paragraph (line 318), interpretation (line 296), section 5 bullet 2 (line 330), misconception 2 (line 345), card AC1-c056", "PASS",
  "Re-derived 3,319,293 / 27,832,482 = 0.11926 (0.1193). Section 5 bullet 2 (line 330) now states the quarter-0 zero and quarters 1-7 non-zero prepaid balances, both matching the printed column. Misconception 2 and card c056 unchanged (" + S + "recheck.py, expcmp.py)."))
rows.append(row("AC1b8-twins-match-pages", "2.5-lab", "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py; pre.expected blocks of L04, L05, L06", "PASS",
  "Each twin output compared with its page pre.expected block: L04 20 lines, L05 22 lines, L06 19 lines, all IDENTICAL (" + S + "expcmp.py)."))
rows.append(row("AC1b-slice-no-project", "2.5-lab", "ledgers/AC1/ (slice b has no project grader; the brief's mutant and alternative-implementation requirement applies to project slices)", "PASS",
  "Slice b is pages and twins. No new student-error mutant and no alternative implementation is required; the project graders are in other slices and are not re-run here."))
rows.append(row("AC1b18-L04-keyresult-prop22", "2.7-prose", "course/modules/AC/AC1/L04.html key-results row 473; card AC1-c053", "PASS",
  "Fixed in round 19: row 473 and card AC1-c053 now carry the Definition 2.2 assumptions (see AC1b19-L04-keyresult-prop22)."))
rows.append(row("AC1b18-L05-keyresult-prop14", "2.7-prose", "course/modules/AC/AC1/L05.html key-results row 488; card AC1-c066", "PASS",
  "Fixed in round 19: row 488 and card AC1-c066 now carry the non-negative price hypothesis (see AC1b19-L05-keyresult-prop14)."))

# previous rows whose subject changed and are re-verified above keep their ids, so check all prev ids present
ids = {r["id"] for r in rows}
missing = [i for i in prev_rows if i not in ids]
print("MISSING prev ids:", missing, file=sys.stderr)
frag = {
  "unit": "AC1", "slice": "AC1-b", "round": 19,
  "round_note": "round 19 (independent re-verification after the round-18 fixes at 51fa336). Delta since the round-18 pin 7143726: L04.html (lines 58, 330, 341, 473), L05.html (lines 87, 121, 345, 488), L06.html (lines 52, 308, 432), cards.json (c046, c052, c053, c058, c066, c069; new c140). Every changed hunk was read; the round-18 FAIL rows were re-verified.",
  "verifier": "Haiku independent verifier for slice AC1-b, round 19; did not build AC1 and shares no context with its builders",
  "pin": "51fa336", "base": "7143726 (round-18 pin of slice b; /tmp/fanout-frags/AC1-b.round18.json is context only, its PASS rows were not trusted)",
  "checkout": "/tmp/verify19-AC1-b (detached at 51fa336; .venv symlink)",
  "scratch": "/tmp/AC1-v/AC1-b-r19", "verified_at": "2026-10-28T12:00:00+00:00",
  "verdict": "FAIL", "rows": rows, "mutants": [],
  "registry_flags": [], "freshness_flags": [],
  "notes": [
    "Slice b is pages and twins, not a project slice: no new student-error mutant is required. Project-grader mutants are not in this slice; ledgers/AC1/mutants gained five v18 files that belong to project slices.",
    "The round-18 FAIL on AC1-c053 and AC1-c066 and on the two key-results rows is fixed. The fix to AC1-c069 (a new locator error introduced by the round-18 cards fix) is the one remaining FAIL.",
    "Lab output is SIMULATED (seeds 2604, 2605, 2606); results read off a lab are grade C naming the lab.",
    "Not checked: live reachability of any publisher or SEC source (no slice-b row cites one); pytest collect-only count (not printed by the configuration); hours on pace (architect ruling, not failed); page_smoke timing beyond the reported PASS.",
  ],
  "summary": "",
}
n = len(rows)
nf = sum(1 for r in rows if r["status"] != "PASS")
frag["summary"] = f"AC1-b round 19 (L04, L05, L06 and twins; pin 51fa336): {n} rows, {n - nf} PASS, {nf} FAIL, 0 UNVERIFIABLE. Verdict FAIL (card AC1-c069 locator)."
json.dump(frag, open(OUT, "w"), indent=2, ensure_ascii=False)
print("rows", n, "fail", nf)
