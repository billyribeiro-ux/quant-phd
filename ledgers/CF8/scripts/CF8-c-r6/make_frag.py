import json, subprocess
from datetime import datetime, timezone
OUT = "ledgers/CF8/CF8-c.json"
C = "Carried from round 5 (%s byte-identical since the round-5 pin 04626e9): "
R = "Re-verified on r6: "
rows = []
def row(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

row("proj-ladder", "check_projects --unit CF8", "course/modules/CF/CF8/project.html", "PASS",
    R + "check_projects CF8: PASS (ledgers/CF8/scripts/CF8-c-r6/check_projects_CF8.out); project hours 10 agree with index data-hours-project=10.")
row("proj-check-pages", "check_pages --unit CF8", "course/modules/CF/CF8/project.html", "PASS",
    R + "check_pages CF8: PASS (check_pages_CF8.out).")
row("proj-dag", "check_dag --unit CF8", "project.html concept links", "PASS",
    R + "check_dag CF8: PASS (check_dag_CF8.out).")
row("proj-labs-run", "run_labs --unit CF8; twins under python -I -W error", "project.html lab-CF8-project-1..3; tests/labs/CF8/lab-CF8-project-{1,2,3}.py", "PASS",
    R + "run_labs CF8: PASS (8/8) (run_labs_unit_CF8.out); each project twin run alone under python -I -W error exits 0 with 0 bytes stderr (twins_project_r6.out). Page code equals twin for project-3 after the docstring edit.")
row("proj-lab1-claims", "Lab 1 hypothesis, code and interpretation (lines 55-168)", "project.html lines 55-168; tests/labs/CF8/lab-CF8-project-1.py", "PASS",
    R + "lab 1 block unchanged in this delta; indep_numbers.py re-run under -I -W error: output identical to round 5 (indep_numbers.out LAB1): weeks 1-13 draws 2000.00 (w1), 142.86 (w11), 1500.00 (w12), 1500.00 (w13); peak 314286 cents; pinch week 13, headroom -114286 cents; DSO five-day impact 571429 cents.")
row("proj-lab2-claims", "Lab 2 hypothesis and interpretation (completion rung)", "project.html lines 172-254 (lab-CF8-project-2)", "PASS",
    C % "project.html lines 172-254 and tests/labs/CF8/lab-CF8-project-2.py" + "run_labs 8/8 PASS on r6.")
row("proj-lab3-claims", "Lab 3 hypothesis, docstring and interpretation", "project.html lines 330-454 (shifted +4 from 326-450 by the cumulative docstring edit); tests/labs/CF8/lab-CF8-project-3.py",
    "PASS", R + "the lab 3 docstring (project.html 402-407 and twin lines 75-80) changed. Its new claims were checked against the code: the sum is over sale days -300 to 91-lag (truncated, so not the total flow by day 91); for lag 30, 45 and 80 the difference of cumulative(lag-5) and cumulative(lag) equals the sum of daily sales over days 92-lag to 96-lag exactly (python -I -W error run in /tmp/cf8c-r6-indep/docchk.py). LAB3 output identical to round 5 (indep_numbers.out). twin_p3 exit 0.")
row("proj-cumulative-docstring", "New docstring of cumulative() reads correctly against its code", "project.html lines 402-407; tests/labs/CF8/lab-CF8-project-3.py lines 75-80", "PASS",
    R + "claims verified by python check (docchk.py): truncation at day -300 stated correctly; two calls differing only in lag share a start and differ by the flow of the sale days 92-lag to 96-lag. Note for the author (not a FAIL): 'the flow in the days between the two lags' is loose; the exact span is sale days 92-lag to 96-lag for a 5-day change.")
row("proj-spec-data", "Inputs: autograder cases are generated; labs 1-3 cases are written out", "project.html line 264 (Inputs dd, changed); grader/instance.py; tests/labs/CF8/lab-CF8-project-{1,2,3}.py",
    "PASS", R + "line 264 changed (adds 'and the cases of Labs 1 to 3 are written out in their code'). Verified: lab 1 and lab 2 define literal SALES, PURCHASES, OPEX and scalar constants (lab-CF8-project-1.py lines 21-30, lab-CF8-project-2.py lines 16-25); lab 3 defines a literal CASE dict (lab-CF8-project-3.py lines 20-32). instance.py draws collection lags randint(35,80) (line 38) and payment lags randint(25,50) (line 39), matching the page; the minimum cash and commitment are positive whole cents (lines 30, 34). Real company filings not embedded: no data file in the unit; the page says so at line 264.")
row("proj-conventions-rounding", "Conventions 'Rounding' bullet", "project.html line 286", "PASS",
    C % "line 286" + "rounding rule matches reference.py _half_up and test_each_residue_of_a_cent_rounds_half_up (run_graders 50/50 PASS).")
row("proj-conventions-windows", "Conventions 'Action cash impact' bullet (DSO and DPO windows)", "project.html line 284", "PASS",
    R + "line 284 unchanged. Window math re-derived: DSO shortening by d moves sale days 92-lag .. 91-lag+d (range(91-lag+1, 91-lag+d+1)); DPO lengthening by d moves purchase days 92-lag-d .. 91-lag (range(91-lag-d+1, 91-lag+1)); both match reference.py action_cash_impact and the page text (checked by hand against the reference code, lines 128-147).")
row("proj-exemplar-A-numbers", "Exemplar A figures", "project.html lines 481-499 (shifted from 480-494)", "PASS",
    R + "figures match indep_numbers.out LAB1: draws in weeks 1, 11, 12 and 13; peak 3,142.86 dollars; pinch week 13 at -1,142.86 dollars; 5 x 800000 / 7 = 571428.57 cents, 571429 cents, 5,714.29 dollars.")
row("proj-exemplar-B-numbers", "Exemplar B figures", "project.html lines 501-518 (shifted from 500-515)", "PASS",
    R + "figures match indep_numbers.out LAB1: minimum liquidity 10857.14 dollars; pinch week 13; peak 3,142.86 leaves 6,857.14 of the 10,000.00 commitment (10000 - 3142.86 = 6857.14); minimum cash 400000 cents and threshold 1200000 cents match lab 1 constants.")
row("proj-exemplar-calibration", "Exemplar data-scores match official scoring", "project.html line 481 (exemplar-a data-scores=2,2,2,2,2) and line 501 (exemplar-b data-scores=4,4,4,4,4)", "PASS",
    R + "both articles carry five scores, one per criterion C1-C5, and the printed Official scoring lines (lines 482, 502) match them. Correction to the round-5 evidence text, which read 'exemplar-b data-scores=4,4,4,4': the attribute has five values; the status is unchanged.")
row("proj-rubric-observable", "Rubric table criteria are observable", "project.html rubric lines 463-475 (shifted from 461-471)", "PASS",
    C % "the rubric table (byte-identical lines, now 463-475)" + "rubric level text unchanged.")
row("proj-memo-sections", "Memo five-section spec and rubric alignment", "project.html line 460 (was 456) and spec line 266", "PASS",
    C % "the memo section lines" + "section names match the Required outputs dd (line 266).")
row("proj-hours", "Hours table and page sentence", "project.html hours table lines 297-304; index.html data-hours-*", "PASS",
    C % "lines 297-304" + "index.html data-hours-lessons=40 and data-hours-project=10 (grep, r6): 40+10=50.")
row("proj-reading-bates", "Reading entry for Bates et al.", "project.html line 539 (shifted from 535); references/references.json key bates2009us", "PASS",
    R + "entry text changed to 'on why U.S. firms hold so much more cash than they used to'. The registry title (references.json entry bates2009us, title field) is 'Why Do U.S. Firms Hold So Much More Cash than They Used To?', J. Finance 64(5), 1985-2021, doi 10.1111/j.1540-6261.2009.01492.x. The entry states no claim from the paper and is a topic description taken from the registry title. The paper's body was not read by this verifier; no claim from it is used on the page, so no attribution beyond the title is made.")
row("proj-grader-reference", "reference.py passes the suite on every seed", "course/modules/CF/CF8/grader/reference.py", "PASS",
    R + "grader and reference unchanged in this delta (git diff 04626e9 9fd6aed under grader/ is empty). run_graders CF8: PASS (reference 50/50 seeds) (run_graders_CF8.out). Reference copied as treasury_forecast.py: pytest --assert=plain -W error passes 100/100 on seeds 0, 13, 49 (ref_pytest_r6.out).")
row("proj-grader-starter", "starter.py docstring and stub", "course/modules/CF/CF8/grader/starter.py", "PASS",
    C % "starter.py")
row("proj-grader-alternatives", "Five alternative correct engines pass the suite", "grader/test_project.py vs alternatives alt1..alt5", "PASS",
    R + "five alternative correct implementations (alt1_sevenths, alt2_float, alt3_bisect, alt4_cumflow_pinch, alt5_daymap, taken from /tmp/cf8c-r5-alts) rerun against the current test_project.py (identical to r5 copies): 100 passed on seeds 0, 13, 49 each (alternatives_r6.txt).")
row("proj-grader-mutants", "Mutation testing: existing and new student-error mutants are all killed", "ledgers/CF8/mutants/ (59 files)", "PASS",
    R + "mutate_graders CF8: PASS (59/59 killed) (mutate_graders_CF8_all_r6.out). Four new student-error mutants of my own: r6-m1-round-floor (money floored, not half up); r6-m2-pinch-latest-tie (pinch takes the later tie); r6-m3-required-equals-peak (required = capped peak); r6-m4-dpo-window-short (DPO window one day short). All four killed at seed 0. Five r5 mutants n01-n05 are also in the directory and were in the 59.")
row("proj-grader-equivalent-r3-04", "Round-3 equivalent mutant not in the mutant set", "grader/test_project.py", "PASS",
    C % "grader/test_project.py and starter.py" + "unchanged.")
row("proj-grader-instances", "instance.py deterministic and varies by seed", "course/modules/CF/CF8/grader/instance.py", "PASS",
    R + "file read in full (48 lines); unchanged in this delta; run_graders checks determinism and seed variation (PASS).")
row("proj-grader-messages", "must_raise and pytest.fail messages", "grader/test_project.py", "PASS",
    C % "grader/test_project.py")
row("proj-grader-exception-table", "Exception types only for conditions the page names", "grader/test_project.py lines 545-606; project.html line 268", "PASS",
    C % "grader/test_project.py lines 545-606" + "exception conditions (horizon, negative commitment, action name) match project.html line 268.")
row("proj-grader-stdlib", "Grader and reference are standard library only", "grader/test_project.py lines 767-791; reference.py imports", "PASS",
    C % "grader/test_project.py lines 767-791" + "reference.py imports only math, collections.abc, fractions, typing.")
row("proj-test-count", "Test count on the page equals the collect-only count", "project.html line 270 (Grading dd)", "PASS",
    R + "line 270 says 100 checks; pytest --collect-only on the reference copy: '100 tests collected'.")
row("proj-starter-docstring", "starter.py docstring", "course/modules/CF/CF8/grader/starter.py", "PASS",
    C % "starter.py" + "page_smoke CF8 PASS (page_smoke_CF8.out).")
row("proj-spec-interest-scope", "Interest and fees scope statement", "project.html lines 268 and 285", "PASS",
    C % "lines 268 and 285" + "the 'no interest, fee or tax' scope line is consistent with the engine having no such key.")
row("proj-pytest-version", "Local-run pytest text", "project.html line 319-320", "PASS",
    C % "lines 319-320")
row("proj-notation", "Symbols used on the page are CF8-local or registry-consistent", "project.html (day-count bullet line 277 and others)", "PASS",
    R + "notation/notation.json has 8 program-wide entries (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q); none is used on the page with another meaning (grep). The changed docstring adds no symbol. Day-count bullet line 277 carried.")
row("cards-count-numbers", "Numbers in cards appear in their lessons", "course/modules/CF/CF8/cards.json, 74 cards", "PASS",
    R + "card_numbers.py rerun: output identical to round 5. Four cards flagged ABSENT (c031, c053, c054, c057) are an artefact: the lesson prints the numbers with LaTeX thousands grouping (e.g. 1{,}488{,}640), checked by hand against L02/L04. 'cards with absent numbers 4' is the script's own count.")
row("cards-lab-numbers", "Numbers cited from labs match lab output", "cards c010, c011, c040, c042, c052-c054, c056, c057, c069-c073", "PASS",
    R + "c052 (881,834 cents, Example 2.5, L04 line 335) re-checked; L04 and L05 twins unchanged or docstring-only; run_labs 8/8 PASS; other cards carried from round 5 (byte-identical).")
row("cards-sample-lesson-agreement", "Cards agree with the current lesson text", "cards.json c001-c074", "PASS",
    R + "the five changed cards (c049, c050, c051, c052, c065) re-read against L04 Theorem 2.1 (assumptions (1)-(3)), Corollary 2.2, Theorem 2.3 and Theorem 2.4 (assumptions (1)-(5)), and L05 Remark 2.4; the fronts state the hypotheses the theorems need. Other 69 cards carried from round 5 (byte-identical since 04626e9).")
row("cards-duplicates-exact", "No exact duplicate cards", "course/modules/CF/CF8/cards.json", "PASS",
    R + "python check: 74 unique ids, 0 duplicate (front, back) pairs.")
row("cards-near-dup-049-053", "c049 and c053 are distinct", "cards c049, c053", "PASS",
    C % "c049 front/back and c053" + "the c049 basis changed only in the section label; the questions differ (liquidity versus headroom).")
row("cards-near-dup-034-044", "c034 and c044 are distinct", "cards c034, c044", "PASS",
    C % "cards c034 and c044")
row("cards-process-words", "No process words in learner text", "cards.json; project.html; project-3 docstring", "PASS",
    R + "grep for round, builder, verifier, revision, this slice in cards.json, project.html and lab-CF8-project-3.py: no match except the word 'rounded' in ordinary sense.")
row("cards-grades-basis", "Grades and basis fields are consistent", "cards.json grade and basis fields", "PASS",
    R + "the changed cards keep grade T and cite a labelled result (basis now 'Theorem 2.1 (Section 1)' etc.). Cards without a grade field (30) and without a basis field (19) are the carried definition and misconception cards as in round 5; this is a stated card format, not a defect in this slice.")
row("cards-labels", "Lesson field agrees with each card's cited lesson", "cards.json lesson field", "PASS",
    C % "cards.json lesson fields" + "lesson counts L01 13, L02 18, L03 15, L04 14, L05 14 (r6 python check).")
row("cards-hypotheses", "Theorem cards state the hypotheses", "cards c043, c052, c053, c055 (round-4 fixes), c016, c021, c022, c027", "PASS",
    R + "fronts of c049-c052 and c065 unchanged in hypothesis content; they state 0 <= B0 <= K and no interest/fee for the theorems that need it (L04 Theorem 2.1 assumptions (2)-(3); Theorem 2.4 assumption (5)). Other cards carried from round 5.")
row("cards-notation-collisions", "Card symbols do not collide with notation registry", "cards.json (c027 Delta Rev, c062 N_Y, c065 x_{0.05})", "PASS",
    R + "c065 now uses x_{0.05}, matching L05 Remark 2.4 and P2; notation/notation.json registers no x, no N_Y, no Delta Rev (checked by python listing of all 8 symbols).")
row("cards-section-citations-L04", "Cards cite Section numbers that exist in L04", "cards c049, c050, c051, c052 (basis); course/modules/CF/CF8/L04.html", "PASS",
    R + "round-5 FAIL fixed. L04 has h2 headings 1 (line 53), 3 (line 342), 4, 5, 6, 7, 8. Theorems 2.1 (line 71), Corollary 2.2 (line 87), Theorem 2.3 (line 308), Theorem 2.4 (line 323) and Example 2.5 (line 332) all sit between line 53 and line 342, i.e. under heading 1. Cards now cite 'Section 1', which is accurate. Cross-slice note for the L04 verifier: the page has no heading 2 and its blocks are numbered 2.x under section 1; that numbering is an L04 defect, not decided here.")
row("tests-labs-memo", "pytest for labs and memo exemplars", "tests/test_labs.py, tests/test_memo_exemplars.py", "PASS",
    R + "pytest -q tests/test_labs.py tests/test_memo_exemplars.py: all passed (pytest_labs_memo.out).")
row("gate-check-pages-unit", "check_pages --unit CF8", "tools/check_pages.py", "PASS", R + "PASS (check_pages_CF8.out).")
row("gate-verify-refs", "verify_refs --offline", "tools/verify_refs.py", "PASS",
    R + "offline integrity: 560 entries, 0 problems (verify_refs_offline.out).")
row("cards-ruff-mypy", "ruff and mypy", "tests/labs/CF8; course/modules/CF/CF8/grader; repo", "PASS",
    R + "ruff check and ruff format --check on tests/labs/CF8 and grader: all checks passed, 12 files formatted (ruff.out). mypy --no-incremental: Success, 229 source files (mypy.out).")

frag = {
 "unit": "CF8", "slice": "CF8-c", "round": 6,
 "verifier": "Claude Haiku 5.5, independent verifier for CF8-c, round 6 (did not build CF8)",
 "pin": "9fd6aed",
 "base": "round-5 pin 04626e9; round-5 fragment /Users/billyribeiro/.fanout/frags/C-CF8-c.round5.json. Delta 04626e9..9fd6aed inside this slice: project.html (hunks at 264, 402-407 and 539 plus a +4 line shift after 407), cards.json (c049, c050, c051, c052, c065), tests/labs/CF8/lab-CF8-project-3.py (docstring of cumulative). grader/ and starter.py, lab-CF8-project-1/2.py, instance.py unchanged.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC6-CF8-c",
 "scratch": "/tmp/cf8c-r6-indep, /tmp/cf8c-r6-alts, /tmp/cf8c-r6-ref",
 "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
 "verdict": "PASS",
 "rows": rows,
 "mutants": [
  {"id": "r6-m1-round-floor", "description": "Money is rounded down (floor) instead of half up, so a half-cent receipt is dropped.", "killed_by": "test_receipts_match_the_day_by_day_oracle (seed 0)"},
  {"id": "r6-m2-pinch-latest-tie", "description": "Covenant pinch takes the latest week on a tie in headroom, not the earliest.", "killed_by": "test_pinch_week_breaks_a_tie_toward_the_earliest_week (seed 0)"},
  {"id": "r6-m3-required-equals-peak", "description": "Required commitment is the capped peak, so a commitment that binds is reported as sufficient.", "killed_by": "test_required_commitment_is_the_uncapped_peak_draw (seed 0)"},
  {"id": "r6-m4-dpo-window-short", "description": "DPO change postpones one day fewer than the stated days, so the window is off by one.", "killed_by": "test_dpo_lengthening_matches_the_day_oracle (seed 0)"}
 ],
 "registry_flags": [],
 "freshness_flags": ["course/modules/CF/CF8/project.html (lines 264, 402-407, 539 and +4 shift after 407), course/modules/CF/CF8/cards.json (c049, c050, c051, c052, c065) and tests/labs/CF8/lab-CF8-project-3.py changed since 04626e9; all touched rows re-verified on 9fd6aed. Carried rows cite the post-shift line numbers for content that is byte-identical."],
 "notes": "Scope for this round: slice c only (project.html rubric, grader, project labs, cards.json, project mutants). Mutants: 59/59 killed (55 existing and 4 new). Alternatives: 5/5 pass on seeds 0, 13, 49. Two items are for other slices or the author, not FAILs: (a) L04 page numbering (no heading 2; blocks 2.x under heading 1); (b) the cumulative() docstring phrase 'the flow in the days between the two lags' is loose (exact span: sale days 92-lag to 96-lag for a 5-day change). Not run: full-workspace pytest (only the labs/memo tests named in the plan); the r5 indep_numbers.py script was reused (same file, identical output), so its independence is inherited from round 5; the 'Lab 2' and 'Lab 3' interpretation prose was checked against the printed output by run_labs (page expected block equals twin output), not re-derived line by line. Not checked: the 69 unchanged cards were not re-read this round; they are carried from round 5 under the byte-identical rule.",
 "summary": "CF8-c round 6: PASS. 48 rows PASS (carried rows noted); 0 FAIL. Round-5 FAIL cards-section-citations-L04 fixed (cards cite Section 1, which contains Theorems 2.1-2.4). Mutants 59/59 killed; five alternative engines pass; gates check_pages, check_dag, check_projects, run_labs 8/8, run_graders 50/50, page_smoke, ruff, mypy, verify_refs all PASS."
}
json.dump(frag, open(OUT, "w"), indent=1, ensure_ascii=False)
print("rows", len(rows), "non-pass", [r["id"] for r in rows if r["status"] != "PASS"])
