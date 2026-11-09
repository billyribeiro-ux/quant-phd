"""Builds ledgers/CF8/CF8-c.json (round 1, closing delta on pin 95f3f8cb). Run with python -I from the checkout root."""
import json

CARRY6 = "Carried from round 6 (project.html, grader/, tests/labs/CF8/lab-CF8-project-{1,2,3}.py byte-identical since the previous pin 9fd6aed; git diff --quiet 9fd6aed HEAD confirmed): "
CARRY6_CARDS = "Carried from round 6 (cards.json entries unchanged since 9fd6aed, checked by id): "
CARRY6_L03 = "Carried from round 6 (L03/L04/L05 and their labs byte-identical since 9fd6aed): "
R = "Re-verified on round 1 (pin 95f3f8cb): "

rows = [
 ("proj-ladder", "check_projects --unit CF8", "course/modules/CF/CF8/project.html", "PASS",
  R + "check_projects CF8: PASS (ledgers/CF8/scripts/CF8-c-r1/check_projects_CF8.out, exit 0). Project hours 10 agree with index.html data-hours-project=10 (line 29)."),
 ("proj-check-pages", "check_pages --unit CF8", "tools/check_pages.py", "PASS",
  R + "check_pages CF8: PASS (check_pages_CF8.out, exit 0)."),
 ("proj-dag", "check_dag --unit CF8", "project.html concept links", "PASS",
  R + "check_dag CF8: PASS (check_dag_CF8.out, exit 0)."),
 ("proj-labs-run", "run_labs --unit CF8; twins under python -I -W error", "project.html lab-CF8-project-1..3; tests/labs/CF8/lab-CF8-project-{1,2,3}.py", "PASS",
  R + "run_labs CF8: PASS (8/8) (run_labs_CF8.out, exit 0). Each project twin run alone with python -I -W error exits 0 with 0 bytes stderr (twin_p1/p2/p3 .out and .err)."),
 ("proj-lab1-claims", "Lab 1 hypothesis, code and interpretation", "project.html lines 55-168; tests/labs/CF8/lab-CF8-project-1.py", "PASS",
  CARRY6 + "lab 1 block and twin unchanged; run_labs 8/8 and twin_p1 exit 0 re-run on r1 (twin_p1.out: peak 3142.86 dollars, pinch week 13, headroom -1142.86 dollars)."),
 ("proj-lab2-claims", "Lab 2 hypothesis and interpretation (completion rung)", "project.html lines 172-254; tests/labs/CF8/lab-CF8-project-2.py", "PASS",
  CARRY6 + "run_labs 8/8 and twin_p2 exit 0 on r1 (twin_p2.out: lowest headroom -1142.86 dollars)."),
 ("proj-lab3-claims", "Lab 3 hypothesis, docstring and interpretation", "project.html lines 330-454; tests/labs/CF8/lab-CF8-project-3.py", "PASS",
  CARRY6 + "twin_p3 exit 0 on r1 (twin_p3.out: pinch week 13, headroom -1642.86 dollars; 5-day DSO and DPO impacts 5000.00 dollars)."),
 ("proj-cumulative-docstring", "New docstring of cumulative() reads correctly against its code", "project.html lines 402-407; tests/labs/CF8/lab-CF8-project-3.py lines 75-80", "PASS",
  CARRY6 + "docstring unchanged since 9fd6aed (git diff empty for the twin and project.html)."),
 ("proj-spec-data", "Inputs: autograder cases are generated; labs 1-3 cases are written out", "project.html line 264; grader/instance.py; tests/labs/CF8/lab-CF8-project-{1,2,3}.py", "PASS",
  CARRY6 + "project.html and grader/instance.py unchanged; lab-CF8-project-1..3 literal case definitions unchanged."),
 ("proj-conventions-rounding", "Conventions 'Rounding' bullet", "project.html line 286", "PASS",
  CARRY6 + "line 286 unchanged; run_graders CF8 PASS (reference 50/50 seeds) re-run on r1 (run_graders_CF8.out)."),
 ("proj-conventions-windows", "Conventions 'Action cash impact' bullet (DSO and DPO windows)", "project.html line 284", "PASS",
  CARRY6 + "line 284 unchanged; grader/reference.py action_cash_impact unchanged."),
 ("proj-exemplar-A-numbers", "Exemplar A figures", "project.html lines 481-499", "PASS",
  CARRY6 + "exemplar A text unchanged; figures match the lab 1 outputs (twin_p1.out)."),
 ("proj-exemplar-B-numbers", "Exemplar B figures", "project.html lines 501-518", "PASS",
  CARRY6 + "exemplar B text unchanged; figures match the lab 1 outputs (twin_p1.out)."),
 ("proj-exemplar-calibration", "Exemplar data-scores match official scoring", "project.html line 481 (exemplar-a data-scores=2,2,2,2,2) and line 501 (exemplar-b data-scores=4,4,4,4,4)", "PASS",
  CARRY6 + "project.html unchanged. No blind scorer file for CF8 exists in ~/.fanout/blind/ (the ten files there are BK4-c, CS2-d, E1-d, E3-d-fresh, E3-d, E4-d, FC2-d, LX1-c, M5-d, PC3-c), so the base calibration row is carried (ruling 23)."),
 ("proj-rubric-observable", "Rubric table criteria are observable", "project.html rubric lines 463-475", "PASS",
  CARRY6 + "rubric table unchanged."),
 ("proj-memo-sections", "Memo five-section spec and rubric alignment", "project.html line 460 and spec line 266", "PASS",
  CARRY6 + "memo section lines unchanged."),
 ("proj-hours", "Hours table and page sentence", "project.html hours table lines 297-304; index.html data-hours-*", "PASS",
  R + "index.html changed in this delta (objectives and data-status hunks only); line 29 still reads data-hours-lessons=\"40\" data-hours-project=\"10\" (grep on r1), 40+10=50. project.html table lines 297-304 carried (unchanged)."),
 ("proj-reading-bates", "Reading entry for Bates et al.", "project.html line 539; references/references.json key bates2009us", "PASS",
  CARRY6 + "project.html line 539 unchanged. references/references.json changed in this delta only in generated_at and in unit usage lists; the bates2009us entry (line 1963-1971: doi 10.1111/j.1540-6261.2009.01492.x, title 'Why Do U.S. Firms Hold So Much More Cash than They Used To?') is unchanged. The paper body was not read; no claim from it is used on the page."),
 ("proj-grader-reference", "reference.py passes the suite on every seed", "course/modules/CF/CF8/grader/reference.py", "PASS",
  R + "grader/ byte-identical since 9fd6aed; run_graders CF8: PASS (reference 50/50 seeds, slowest 0.3 s) (run_graders_CF8.out, exit 0)."),
 ("proj-grader-starter", "starter.py docstring and stub", "course/modules/CF/CF8/grader/starter.py", "PASS",
  CARRY6 + "starter.py unchanged; page_smoke CF8 PASS on r1 (page_smoke_CF8.out)."),
 ("proj-grader-alternatives", "Five alternative correct engines pass the suite", "grader/test_project.py vs alternatives alt1..alt5", "PASS",
  CARRY6 + "grader/test_project.py unchanged; alternatives_r6.txt (100 passed on seeds 0, 13, 49 each, five engines) is the base evidence and is not re-run this round."),
 ("proj-grader-mutants", "Mutation testing: existing and new student-error mutants are all killed", "ledgers/CF8/mutants/ (59 files)", "PASS",
  R + "mutate_graders --unit CF8: PASS, 59/59 KILLED (mutate_graders_CF8.out, exit 0; the four r6 mutants r6-m1..m4 killed at seed 0). No new mutant is written this round (ruling 37)."),
 ("proj-grader-equivalent-r3-04", "Round-3 equivalent mutant not in the mutant set", "grader/test_project.py", "PASS",
  CARRY6 + "grader/test_project.py and starter.py unchanged."),
 ("proj-grader-instances", "instance.py deterministic and varies by seed", "course/modules/CF/CF8/grader/instance.py", "PASS",
  CARRY6 + "instance.py unchanged; run_graders CF8 PASS on r1 (determinism and seed variation are checked there)."),
 ("proj-grader-messages", "must_raise and pytest.fail messages", "grader/test_project.py", "PASS",
  CARRY6 + "grader/test_project.py unchanged."),
 ("proj-grader-exception-table", "Exception types only for conditions the page names", "grader/test_project.py lines 545-606; project.html line 268", "PASS",
  CARRY6 + "grader/test_project.py and project.html line 268 unchanged."),
 ("proj-grader-stdlib", "Grader and reference are standard library only", "grader/test_project.py lines 767-791; reference.py imports", "PASS",
  CARRY6 + "grader/ unchanged."),
 ("proj-test-count", "Test count on the page equals the collect-only count", "project.html line 270 (Grading dd)", "PASS",
  CARRY6 + "line 270 unchanged (100 checks); the collect-only count of 100 is the base evidence (ref_pytest_r6.out)."),
 ("proj-starter-docstring", "starter.py docstring", "course/modules/CF/CF8/grader/starter.py", "PASS",
  R + "page_smoke CF8: PASS (page_smoke_CF8.out); starter.py byte-identical since 9fd6aed."),
 ("proj-spec-interest-scope", "Interest and fees scope statement", "project.html lines 268 and 285", "PASS",
  CARRY6 + "lines 268 and 285 unchanged."),
 ("proj-pytest-version", "Local-run pytest text", "project.html lines 319-320", "PASS",
  CARRY6 + "lines 319-320 unchanged."),
 ("proj-notation", "Symbols used on the page are CF8-local or registry-consistent", "project.html; notation/ registry", "PASS",
  CARRY6 + "project.html unchanged; notation/ byte-identical since 9fd6aed (git diff --quiet). The card-side symbol check is in cards-notation-collisions."),
 ("cards-count-numbers", "Numbers in cards appear in their lessons", "course/modules/CF/CF8/cards.json, 80 cards", "PASS",
  R + "cards_r1_checks.py (cards_r1_checks.out): 80 cards, 0 with numbers absent from their lesson after normalising the LaTeX thousands grouping {,} that the lessons print (for example 1{,}500{,}000 and 12{,}000{,}000 in L02.html line 157, Example 3.4, and 1{,}488{,}640 in text/L04.txt line 248). Without that normalisation card_numbers.py (card_numbers.out) lists c031, c053, c054, c077, c078, which are the same grouping artefact."),
 ("cards-lab-numbers", "Numbers cited from labs match lab output", "cards c010, c011, c040, c042, c052-c054, c056, c057, c069-c073, c075-c080", "PASS",
  R + "changed cards re-checked against the current outputs (plain-text lesson dumps and the twin run in ledgers/CF8/scripts/CF8-c-r1/text/, from extract_text_r1.py): c011 48.67 and 45.63 (text/L01.txt lines 274-275); c019, c075 37.24 and 44.59 (text/L02.txt line 203; (1/0.98)^(365/20)-1 = 0.44585 on python -I); c031, c077 678,082.19 and 4.52 percent (text/L02.txt lines 211-212; text/lab_CF8_L02_1_r1.out); c042, c053, c054 week-6 draw 539,905, headroom -139,905 and week-11 cumulative flow -1,488,640 (text/L04.txt lines 201, 206 and 248); c056 88,640 and 1,288,640 (text/L04.txt lines 229, 252); c057, c078 pinch week 11 at -888,640 (text/L04.txt lines 206, 211); c069, c079 0.8380 (1676) and 0.1780 (356) (text/L05.txt lines 111-112); c071, c080 365525 and 99 of 2000, 0.0495 (text/L05.txt line 118). Carried, unchanged cards: c010, c040, c070, c072, c073 (identical by id to 9fd6aed)."),
 ("cards-sample-lesson-agreement", "Cards agree with the current lesson text", "cards.json c001-c080", "PASS",
  R + "every card whose subject changed (22 edited, 6 new: c075-c080) and every L01 and L02 card (L01 and L02 changed in this delta) was read against the current lesson text (L01, L02 plain-text extraction in /tmp/cf8c-r1-txt). L03, L04 and L05 unchanged, and their unchanged cards are carried. Theorem-statement mismatch is recorded under cards-hypotheses, not here."),
 ("cards-duplicates-exact", "No exact duplicate cards", "course/modules/CF/CF8/cards.json", "PASS",
  R + "cards_r1_checks.out: 80 unique ids, 0 duplicate (front, back) pairs. New near-neighbours checked: c019 (simple cost) vs c075 (compounded cost) and c031 (dollar ΔI) vs c077 (margin m*), each asking a different quantity."),
 ("cards-near-dup-049-053", "c049 and c053 are distinct", "cards c049, c053", "PASS",
  R + "c049 asks whether a draw or repayment changes liquidity; c053 asks whether drawing gives more covenant headroom. Fronts differ; c049 is unchanged, c053 changed in the back only."),
 ("cards-near-dup-034-044", "c034 and c044 are distinct", "cards c034, c044", "PASS",
  CARRY6_CARDS + "c034 and c044 identical to 9fd6aed (python -I check on r1)."),
 ("cards-process-words", "No process words in learner text", "cards.json; project.html; project-3 docstring", "PASS",
  R + "cards_r1_checks.py process-word scan over all 80 cards (round, builder, verifier, revision, this slice, fanout, ruling, blind): no hit. project.html and the project-3 twin are byte-identical to 9fd6aed."),
 ("cards-grades-basis", "Grades and basis fields are consistent", "cards.json grade and basis fields", "PASS",
  R + "grade T 26, C 24, no grade 30 (definition and misconception cards, as before); no basis 19. Every changed T card cites a labelled result on the page: c007 Proposition 4.1; c008 Problem M1; c017 Proposition 1.5; c018 Proposition 2.1; c021 and c023 Proposition 3.2; c022 Corollary 3.3; c027 Problem R1; c050 Corollary 2.2; c052 Theorem 2.4; c076 Proposition 3.2. New c075-c080 carry grade and basis."),
 ("cards-labels", "Lesson field agrees with each card's cited lesson", "cards.json lesson field", "PASS",
  R + "lesson counts L01 13, L02 21, L03 15, L04 15, L05 16 (total 80; cards_r1_checks.out). Each new card's content lies in its lesson: c075-c077 in L02 (Convention 1.2, Example 1.4, Proposition 3.2, Example 3.4); c078 in L04 Lab 1; c079-c080 in L05 Lab 1 and Remark 2.4."),
 ("cards-hypotheses", "Theorem cards state the hypotheses", "cards c052 (front); c043, c053, c055, c016, c021, c022, c027", "FAIL",
  R + "CF8-c052 is graded T and cites Theorem 2.4 (course/modules/CF/CF8/L04.html line 324). Theorem 2.4 assumption (3) is 'Every receipt is a collection of receivables' (L04.html line 324); the proof at L04.html line 328 uses it: 'By Assumption (3) receipts equal collections'. The card's front (cards.json line 378) lists weekly sales, the DSO slip from week 1, uncollected collections, 0 <= B0 <= K and no interest, but not assumption (3), and its back claims 'cumulative receipts ... fall by exactly dS/7'. That claim is false without assumption (3): a receipt that is not a collection (for example a cash sale) does not move with DSO. c021, c022, c023 paraphrase Assumption 3.0 but cite it by name, so they are PASS with this note only; c027 states r > 0. Other changed T cards state their hypotheses.",
  "Add to the CF8-c052 front the clause 'and every receipt is a collection of receivables' (Theorem 2.4 assumption (3)); optionally also 'under the L03 flows and credit-line rule', as CF8-c049 does. Then re-verify c052 and this row."),
 ("cards-notation-collisions", "Card symbols do not collide with notation registry", "cards.json (c027 Delta Rev, c062 N_Y, c065 x_{0.05}, c018 q, c024 δ, c031/c077 R0)", "PASS",
  R + "notation/ unchanged; notation.json registers 8 program-wide entries (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q). None is used on a changed card with another meaning. R0 (c031, c077) spells the lesson's Rev_0 (L02 Example 3.4) differently; it is not a registry symbol (note only)."),
 ("cards-section-citations-L04", "Cards cite Section numbers that exist in L04", "cards c050, c052 (basis); course/modules/CF/CF8/L04.html", "PASS",
  R + "L04 h2 headings: section 1 at line 53, section 3 at line 342, section 4 at 350. Corollary 2.2, Theorem 2.1, Theorem 2.3, Theorem 2.4 and Example 2.5 sit between lines 53 and 342, i.e. under Section 1, as c050 and c052 cite. c053, c054, c056 cite Section 4 (Misconceptions, line 350), which is correct."),
 ("tests-labs-memo", "pytest for labs and memo exemplars", "tests/test_labs.py, tests/test_memo_exemplars.py", "PASS",
  R + "pytest -q tests/test_labs.py tests/test_memo_exemplars.py: exit 0 (pytest_labs_memo.out)."),
 ("gate-check-pages-unit", "check_pages --unit CF8", "tools/check_pages.py", "PASS",
  R + "check_pages CF8: PASS (check_pages_CF8.out)."),
 ("gate-verify-refs", "verify_refs --offline", "tools/verify_refs.py", "PASS",
  R + "offline integrity: 560 entries, 0 problems (verify_refs_offline.out, exit 0)."),
 ("cards-ruff-mypy", "ruff and mypy", "tests/labs/CF8; course/modules/CF/CF8/grader; repo", "PASS",
  R + "ruff check and ruff format --check on tests/labs/CF8 and grader: All checks passed; 12 files already formatted (ruff.out). mypy --no-incremental: Success: no issues found in 386 source files (mypy.out)."),
 ("gate-build-site-check", "build_site --check (site data current; cards.json changed)", "tools/build_site.py", "PASS",
  R + "build_site.py --check: site data current: 6 outputs (build_site_check.out, exit 0)."),
]

mutants = [
 {"id": "r6-m1-round-floor", "description": "Money is rounded down (floor) instead of half up, so a half-cent receipt is dropped. (standing, carried from round 6)",
  "killed_by": "test_receipts_match_the_day_by_day_oracle (seed 0); re-run r1 mutate_graders CF8 KILLED"},
 {"id": "r6-m2-pinch-latest-tie", "description": "Covenant pinch takes the latest week on a tie in headroom, not the earliest. (standing, carried from round 6)",
  "killed_by": "test_pinch_week_breaks_a_tie_toward_the_earliest_week (seed 0); re-run r1 KILLED"},
 {"id": "r6-m3-required-equals-peak", "description": "Required commitment is the capped peak, so a commitment that binds is reported as sufficient. (standing, carried from round 6)",
  "killed_by": "test_required_commitment_is_the_uncapped_peak_draw (seed 0); re-run r1 KILLED"},
 {"id": "r6-m4-dpo-window-short", "description": "DPO change postpones one day fewer than the stated days, so the window is off by one. (standing, carried from round 6)",
  "killed_by": "test_dpo_lengthening_matches_the_day_oracle (seed 0); re-run r1 KILLED"},
]

notes = (
 "Closing delta (ruling 30) on pin 95f3f8cb from base round-6 fragment C-CF8-c.round6.json (pin 9fd6aed). "
 "Delta in slice paths: course/modules/CF/CF8/cards.json (22 edited cards: c007, c008, c011, c017, c018, c019, c021, c022, c023, c027, c031, c042, c050, c052, c053, c054, c056, c057, c060, c062, c069, c071; 6 new: c075-c080; 80 cards in all) and ledgers/CF8/mutants (r6 files, already the standing set). "
 "Outside the slice paths but read because they change cards' subjects: L01.html, L02.html, index.html, lab-CF8-L02-1.py, references/references.json (bates entry unchanged). "
 "project.html, grader/, lab-CF8-project-{1,2,3}.py, notation/, tools/ (checked gates), L03/L04/L05 and their labs are byte-identical to 9fd6aed. "
 "Not authored this round: no new mutants (ruling 37). Standing set 59/59 killed. "
 "Observations (notes, not FAIL): "
 "(a) cards-sample / c050: the back drops the tie clause; Corollary 2.2 (L04.html) and Definition 1.2 say 'the earlier week on a tie'. 'The week of least cumulative net flow' presupposes uniqueness. Restoring the clause is advised (LOW). "
 "(b) c053 (C) and c056 (C) fronts omit the L03 flows-and-rule clause that Theorem 2.1 and Theorem 2.3 assumption (1) state; c049 includes it. Grade C; not a FAIL under the accepted round-4/6 convention, but consistent with c049 the clause could be added. "
 "(c) c021-c023 paraphrase Assumption 3.0 and drop item (5) 'r > 0'; they cite Assumption 3.0 by name, and the claims need at least r > -1. LOW. "
 "(d) c031 and c077 write 'revenue R0' where L02 Example 3.4 writes Rev_0; spelling only. "
 "(e) Nothing re-read in L03, L04, L05 beyond the cards that cite them; the 50 unchanged L03-L05 cards are carried by id. "
 "Git: ledgers/CF8/scripts/CF8-c-r1/ already held tracked files from an older batch (commit e22feb33: alt_v1_decimal.py, alt_v2_sevenths.py, alt_v3_prefix.py, make_v_mutants.py, recheck_project_labs.py, run_solution_suite.py, witness_unenforced.py); they were not modified or read as evidence. "
 "Not checked: whole-workspace pytest; the five alternative engines were not re-run (grader unchanged; base evidence carried); the Bates paper body; no blind exemplar scorer exists for CF8, so exemplar calibration is carried from base."
)

summary = (
 "CF8-c round 1 (closing delta, pin 95f3f8cb): FAIL. 49 rows: 48 PASS (re-verified or carried by byte-identical subject), 1 FAIL: cards-hypotheses, CF8-c052 front omits Theorem 2.4 assumption (3) 'every receipt is a collection of receivables', which its receipts claim depends on. Fix: add the clause to the c052 front and re-verify. Gates all PASS: check_pages, check_dag, check_projects, run_labs 8/8, run_graders 50/50, page_smoke, mutate_graders 59/59, twins under -I -W error, pytest labs+memo, ruff, mypy, verify_refs, build_site --check."
)

fragment = {
 "unit": "CF8",
 "slice": "CF8-c",
 "round": 1,
 "verifier": "Claude Haiku 5.5, independent verifier for CF8-c, round 1 (closing delta; did not build CF8)",
 "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
 "base": "round-6 fragment /Users/billyribeiro/.fanout/frags/C-CF8-c.round6.json, pin 9fd6aed (delta 9fd6aed..95f3f8cb in slice paths)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-CF8-c",
 "scratch": "/tmp/cf8c-r1-txt (plain-text lessons), /tmp/cf8c-r1-old-cards.json (cards.json at 9fd6aed)",
 "verified_at": "2026-11-09T15:55:16+00:00",
 "verdict": "FAIL",
 "rows": [{"id": i, "check": c, "location": l, "status": s, "evidence": e, **({"fix": f} if s != "PASS" else {})}
          for (i, c, l, s, e, *rest) in [(r[0], r[1], r[2], r[3], r[4], *( [r[5]] if len(r) > 5 else []))
                                         for r in rows] for f in [rest[0] if rest else ""]],
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [
   "course/modules/CF/CF8/cards.json (22 edited, 6 new), course/modules/CF/CF8/L01.html, L02.html, index.html and tests/labs/CF8/lab-CF8-L02-1.py changed since 9fd6aed; every card whose subject changed is re-read; project.html, grader/ and the project twins did not change.",
   "ledgers/CF8/scripts/CF8-c-r1/ contains tracked files from commit e22feb33 that are not this round's evidence."
 ],
 "notes": notes,
 "summary": summary,
}
# the list comprehension above is replaced by an explicit build for clarity
rows_out = []
for r in rows:
    row = {"id": r[0], "check": r[1], "location": r[2], "status": r[3], "evidence": r[4]}
    if r[3] != "PASS":
        row["fix"] = r[5]
    rows_out.append(row)
fragment["rows"] = rows_out
with open("ledgers/CF8/CF8-c.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print("rows", len(rows_out), "non-PASS", [r["id"] for r in rows_out if r["status"] != "PASS"])
