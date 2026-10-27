"""Round 7 (AC2 project slice): builds ledgers/AC2/project.json from the round-6 fragment plus this round's re-checks."""
import json
from pathlib import Path

CHECKOUT = Path("/tmp/verify-ac2r7-p")
R6 = json.loads(Path("/tmp/ac2-frags/project.round6.json").read_text(encoding="utf-8"))
CARRY = ("Carried from round 6 (course/modules/AC/AC2/project.html, course/modules/AC/AC2/grader/*, "
         "tests/labs/AC2/lab-AC2-project-{1,2,3}.py, atlas/A15.contract.md, references/references.json, "
         "course/assets/js/grader.js, course/assets/vendor/pyodide/pyodide-lock.json byte-identical since ff9284f; "
         "git diff --quiet ff9284f HEAD verified this round): ")
CARD_CARRY = ("Carried from round 6 (cards.json records other than AC2-c024, AC2-c075 and AC2-c107 byte-identical since "
              "ff9284f; those three re-verified in rows r7-cards-c024, r7-cards-c075, r7-cards-c107): ")
HUB = ("Re-verified round 7: course/modules/AC/AC2/index.html read in full this round (20,429 bytes; the only delta "
       "since ff9284f is the L06 card body line 149). ")

NEW = {
    "r6-cards-c075": ("PASS", "AC2-c075 back and basis re-verified. Back and basis now state 0.00223495 'printed as planted_spread_8dp' "
        "and SD 0.0113137 'research problem R1'. Ran tests/labs/AC2/lab-AC2-L05-1.py with python -I -W error (rc 0): prints "
        "planted_spread_8dp 0.00223495 and spread_sd_theory_7dp 0.0113137 (lines 6-7 of output). Recomputed "
        "((1.959964+0.841621)*0.0113137/0.00223495)^2 = 201.13 (inline python -I, output 201.13). "
        "L05.html R1 (line 351) uses s = 0.0113137. Prior FAIL (basis said 0.0022350, not a printed value) is fixed."),
    "r6-cards-c107": ("PASS", "AC2-c107 back re-verified against L08.html section 2 (line 93), the live DOI chain and the Wikipedia page. "
        "curl -s -o /dev/null -D - -L https://doi.org/10.2469/faj.v55.n5.2296 gives 302 to "
        "https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296 then HTTP 403 (2026-10-27). "
        "curl -sL https://en.wikipedia.org/wiki/Beneish_M-score gives HTTP 200; the page's formula is -4.84 + 0.92 DSRI + 0.528 GMI "
        "+ 0.404 AQI + 0.892 SGI + 0.115 DEPI - 0.172 SGAI + 4.679 TATA - 0.327 LVGI, its formula footnote [1] is "
        "'Messod D. Beneish. The Detection of Earnings Manipulation. Scribd. Retrieved 2017-01-08', and its threshold "
        "sentence is -1.78. The card's locators resolve: misconception 2 (L08.html section 6 list item 2), problem E1 "
        "(id E1, line 527), quiz item 5 (line 607, the 5th item), and the lab (lab-AC2-L08-1.py UNCONFIRMED_* constants). "
        "The paper was not read; the card says so."),
    "r6-beneish-researchgate": ("PASS", "Claim no longer in learner text: grep -i researchgate over course/modules/AC/AC2/*.html and "
        "plans/*.md returns no match (round-7 checkout). The replacement access statement (DOI 302 then tandfonline HTTP 403) "
        "was reproduced with plain curl in row r6-cards-c107. Row subject removed, so the UNVERIFIABLE status is retired."),
    "r6-open-items-beneish-jstor": ("PASS", "plans/AC2-open-items.md line 16 (REFERENCE_REQUESTS, Beneish 1999) no longer "
        "mentions JSTOR (grep -c -i jstor = 0). The row now states the DOI resolver redirect to tandfonline.com and HTTP 403, "
        "reproduced with plain curl on 2026-10-27 (curl -s -o /dev/null -D - -L https://doi.org/10.2469/faj.v55.n5.2296: 302, "
        "then 403). The JSTOR claim was for the Piotroski record and remains only in L08 section 2 (not in this slice's rows)."),
    "r6-open-items-sec": ("PASS", "plans/AC2-open-items.md line 10 states plain curl to https://www.sec.gov/os/webmaster-faq and "
        "https://www.sec.gov/os/accessing-edgar-data returned HTTP 403 (2026-10-27). Reproduced: both URLs return HTTP/2 403 "
        "to plain curl this round. Also reproduced: https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json returns 200 "
        "(3,789,099 bytes) with a descriptive non-personal User-Agent, consistent with the row's data.sec.gov statement."),
    "r6-hub-data-status": ("PASS", HUB + "Data status (index.html section id=data) says SIMULATED only; the SEC access statement "
        "reproduced (403 on both sec.gov pages); tools/data_sources.yaml has no SEC entry (grep -i 'sec|edgar' = no match in its 139 lines)."),
    "r6-hub-placement-count": ("PASS", HUB + "Nine placement items (Pq1, Pq2, Pq3, Pq4, median, Pq6, three data-skill items); "
        "six prerequisite items (four AC1, two S0) and three skill checks; mastery 0.8 gives 8 of 9 (7/9 = 78%), matching quiz.js "
        "passed = overall && skilled (lines 60-69). The gross-margin item answer 0.4 = (500-300)/500 and the median item 2 are correct."),
    "r6-hub-hours": ("PASS", HUB + "data-hours-lessons=76 equals the eight lesson cards 9+10+8+9+8+10+10+12 = 76; each lesson's data-hours "
        "(L01 9, L02 10, L03 8, L04 9, L05 8, L06 10, L07 10, L08 12) matches its card; data-hours-project=34; 76+34 = 110; "
        "69.1%/30.9% split matches 76/110 and 34/110."),
    "r6-hub-cards-bodies": ("PASS", HUB + "Eight lesson card bodies read against each lesson. L06 body changed to 'The modified Jones model "
        "as the A15 contract defines it (registry key dechow1995detecting), its estimation, and a planted manipulation that the model "
        "is tested to recover': L06 section 1 cites the model to the accrual-model literature, Section 2 defines it, Lab 1 plants "
        "manipulation; consistent. Other bodies unchanged and consistent with their lessons (L05 SIMULATED note, L08 constants status)."),
    "r6-hub-l05-card-reverify": ("PASS", HUB + "L05 card body (SIMULATED portfolio study, honest-pending note for real data) "
        "unchanged; consistent with L05.html and the lab."),
    "r6-cards-count-schema": ("PASS", "Re-run this round on course/modules/AC/AC2/cards.json: 140 records, ids exactly AC2-c001..AC2-c140 "
        "in order, no duplicate ids, fronts or backs; lessons L01 17, L02 18, L03 17, L04 16, L05 15, L06 17, L07 20, L08 20 (sum 140); "
        "grade present on 86 records (T 36, C 49, D 1), absent on 54 definition or formula cards; every C or D card has a basis or cite. "
        "Card c013 cites 'A15 contract rule' in its text without a grade field; the grade rule (BUILDER_RULES 7) applies to graded results, and the claim is a contract rule of the lesson, not a graded result."),
    "r6-cards-adjacent-hunks": ("PASS", CARD_CARRY + "round-6 basis: cards c038, c039, c041, c047, c058, c064, c073, c083, c084, c086, c109, c124, c125 "
        "checked against the lesson hunks of the previous window; none of those records changed since ff9284f."),
    "r6-cards-c123": ("PASS", "Carried from round 6 (cards.json record AC2-c123 byte-identical since ff9284f): round-6 basis: AC2-c123 expected t at the planted spread. Arithmetic re-checked this round: 0.00223495 / (0.0113137 / sqrt(120)) = 2.164, matching lab-AC2-L05-1.py output expected_t_at_planted 2.164."),
    "r6-cards-c130": ("PASS", "Carried from round 6 (cards.json record AC2-c130 byte-identical since ff9284f; L07.html section 5 table changed only by the Ivey link, re-read): round-6 basis: AC2-c130 Piotroski conditions count, eight conditions match and s7 is a proxy."),
    "r6-run-graders-0-49": ("PASS", "Re-run this round: .venv/bin/python tools/run_graders.py --unit AC2 --seeds 0-49 printed 'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.6 s)' (ledgers/AC2/scripts/project-r7/run_graders_0-49.txt, rc 0)."),
    "r6-mutate-50": ("FAIL", "Re-run this round: tools/mutate_graders.py --unit AC2 --seeds 0-9 over 53 mutants (m01-m16, p01-p37): 52 killed, 1 survived (m16, see r7-mut-m16). Output in ledgers/AC2/scripts/project-r7/mutate_r7.txt, rc 1. Round-6 result 50/50 was for the 50 mutants then present; the three new mutants are 2 killed and 1 survived."),
    "r6-page-smoke-project": ("PASS", "Re-run this round: tools/page_smoke.py --unit AC2: modules/AC/AC2/project.html PASS (in-browser grader: 'All 236 tests pass on seed 440225566'), index.html PASS, concepts.html PASS, review.html PASS, AC2 PASS."),
    "r6-run-labs-and-gates": ("PASS", "Re-run this round: tools/run_labs.py --unit AC2: 'run_labs AC2: PASS (11/11)'; check_pages --unit AC2 PASS; check_projects --unit AC2 PASS; check_dag --unit AC2 PASS."),
    "r6-project-labs-isolated": ("PASS", "Re-run this round: python -I -W error on tests/labs/AC2/lab-AC2-project-1.py, -2.py and -3.py: rc 0 each (3, 4, 3 output lines)."),
    "r6-impls-50": ("PASS", "Re-run this round: five alternative correct implementations (V1 svd 1e-8, V2 svd 1e-12, V3 condition 1e12, V4 cholesky pivot, V5 strict-bool svd 1e-10; copies of /tmp/verify-ac2-p/ledgers/AC2/scripts/project-r3/impls) through harness_r7.py over seeds 0-49: 50/50 seeds each (ledgers/AC2/scripts/project-r7/impls_0-49_r7.txt). No over-constraint."),
    "r6-mutants-new-m11-m13": ("PASS", CARRY + "m11-m13 remain in ledgers/AC2/mutants and were killed again this round (mutate_r7.txt)."),
    "r6-collect-236": ("PASS", CARRY + "round-6 basis: pytest --collect-only 236 on the reference; re-confirmed this round by the in-browser run 'All 236 tests pass' (page_smoke r6-page-smoke-project)."),
    "r6-lint-types": ("PASS", CARRY + "round-6 basis: ruff and mypy on grader and lab twins (not re-run this round; grader and twins byte-identical)."),
    "proj-r4-cards-lab-numbers": ("PASS", CARD_CARRY + "round-6 basis: cards c009, c016, c026, c031, c039, c041, c047, c069-c075, c082-c086, c104, c113-c114, c117, c121-c125 vs lab output. AC2-c075 re-verified in r6-cards-c075 (lab prints planted_spread_8dp and SD 0.0113137; 201 months recomputed this round)."),
    "proj-r5-cards-L02": ("PASS", CARD_CARRY + "round-6 basis: L02 cards. AC2-c024 (changed back) re-verified in r7-cards-c024. Definition 4.1 renamed '(four ratios)' in L02 since ff9284f; cards c134, c135 and c017-c019 still cite Definition 4.1, whose content is the four ratios (current ratio, debt to assets, DSO, gross margin)."),
    "proj-r5-cards-L05": ("PASS", CARD_CARRY + "round-6 basis: L05 cards. AC2-c075 re-verified in r6-cards-c075 this round."),
    "proj-r5-cards-L08": ("PASS", CARD_CARRY + "round-6 basis: L08 cards. AC2-c107 re-verified in r6-cards-c107 this round."),
    "proj-r4-cards-changed-wording": ("PASS", CARD_CARRY + "round-6 basis: cards whose text changed since 4a8690a; none of the listed records changed since ff9284f except AC2-c024, AC2-c075 and AC2-c107, re-verified in the r7-cards rows."),
    "r6-cards-c107-lesson": ("PASS", "AC2-c107 back re-verified against L08.html section 2 (line 93) this round: the access record now reads 'DOI resolver redirects to the publisher page at tandfonline.com, which returned HTTP 403 to plain curl on 2026-10-27', reproduced (see r6-cards-c107). The earlier ResearchGate sentence is gone: grep -i researchgate over course/modules/AC/AC2 finds nothing."),
    "r3-sec-pending": ("PASS", "Re-run this round: curl -s -o /dev/null -D - -L https://www.sec.gov/os/webmaster-faq -> HTTP/2 403 (final URL same). Also https://www.sec.gov/os/accessing-edgar-data -> HTTP/2 403."),
    "proj-r5-beneish-source-reread": ("PASS", "Re-verified round 7 (L08.html section 2 and cards AC2-c107..c109 changed since ff9284f): AC2-c107 re-verified (r6-cards-c107); c108 (registry verifies title, journal, volume, issue, pages) matches references/references.json entry beneish1999detection (title 'The Detection of Earnings Manipulation'; doi 10.2469/faj.v55.n5.2296); c109 (no cut-off as a rule; Wikipedia threshold -1.78 unconfirmed) matches the lesson's section 2 and the Wikipedia page (threshold sentence read, curl HTTP 200). L08 section 2 access sentences reproduced as in r6-cards-c107."),
    "r3-banned-numbers": ("PASS", "Re-run this round: grep -rn -E '4\\.697|2\\.22' over course/modules/AC/AC2, tests/labs/AC2, atlas, plans, references, curriculum, tools: no match."),
    "r3-wiki-beneish": ("PASS", "Re-run this round: curl -sL https://en.wikipedia.org/wiki/Beneish_M-score -> HTTP 200; formula constants -4.84, 0.92, 0.528, 0.404, 0.892, 0.115, -0.172, 4.679, -0.327 and the threshold -1.78 match reference.py and instance.py constants (proj-beneish-values-match-wiki)."),
}

NEW_ROWS = [
    {"id": "r7-cards-c024", "check": "2.7-cards", "location": "course/modules/AC/AC2/cards.json AC2-c024; L02.html canon-breaks bullet 1 and quiz L02q3 (lines ~665-840)",
     "status": "PASS", "evidence": "Changed back re-derived: total assets equal liabilities plus equity in each year, averaging is linear, so average TA / average equity = 1 + average liabilities / average equity, and the factor rises with each liability (payables included). Matches the L02 bullet and the Q3 option and explain text (changed since ff9284f, read in full). reference.py dupont() uses _average for both factors, as the card and lesson state."},
    {"id": "r7-cards-c075", "check": "2.7-cards", "location": "course/modules/AC/AC2/cards.json AC2-c075; L05.html R1 solution line ~351",
     "status": "PASS", "evidence": "python -I -W error tests/labs/AC2/lab-AC2-L05-1.py rc 0: planted_spread_8dp 0.00223495, spread_sd_theory_7dp 0.0113137. Recomputed months for 80% power, two-sided 5%: (2.801585 x 0.0113137 / 0.00223495)^2 = 201.13, so about 201. Card basis names the printed key."},
    {"id": "r7-cards-c107", "check": "2.1-access", "location": "course/modules/AC/AC2/cards.json AC2-c107; references/references.json beneish1999detection (doi 10.2469/faj.v55.n5.2296)",
     "status": "PASS", "evidence": "curl -s -o /dev/null -D - -L https://doi.org/10.2469/faj.v55.n5.2296 -> 302 location https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, then HTTP 403 (2026-10-27). Wikipedia 'Beneish M-score' (curl, HTTP 200) carries the same constants and -1.78 threshold and cites 'The Detection of Earnings Manipulation. Scribd'. Card locators (misconception 2, problem E1, quiz item 5, the lab) resolve to L08.html lines 482-490, 527 and 607. The paper was not read; the card says so; no bypass attempted."},
    {"id": "r7-mut-m14", "check": "2.6-mutation", "location": "ledgers/AC2/mutants/m14_modified_jones_regressors_unscaled.py",
     "status": "PASS", "evidence": "tools/mutate_graders.py --unit AC2 --seeds 0-9: KILLED by test_modified_jones_coefficients_are_the_least_squares_fit (seed 0). Mutant: revenue-less-receivables regressor left unscaled by lagged assets."},
    {"id": "r7-mut-m15", "check": "2.6-mutation", "location": "ledgers/AC2/mutants/m15_dso_without_365_days.py",
     "status": "PASS", "evidence": "tools/mutate_graders.py --unit AC2 --seeds 0-9: KILLED by test_single_ratio_numbers (seed 0). Mutant: DSO without the 365 factor."},
    {"id": "r7-mut-m16", "check": "2.6-mutation", "location": "ledgers/AC2/mutants/m16_previous_year_is_earliest_in_window.py; course/modules/AC/AC2/grader/test_project.py (no test with two period ends inside 350-380 days)",
     "status": "FAIL", "evidence": "SURVIVED tools/mutate_graders.py --unit AC2 --seeds 0-9: _previous returns the EARLIEST period end in the 350-380 day window instead of the latest. The spec says latest: project.html line 254 Conventions and atlas/A15.contract.md line 186 ('the latest period end in the mapping that is 350 to 380 days earlier'). Witness (ledgers/AC2/scripts/project-r7/witness_m16.txt, python -I): statements with 2020-12-31, 2019-12-28 and 2020-01-02; reference _previous returns 2020-01-02, m16 returns 2019-12-28. Both 2019-12-28 (369 days) and 2020-01-02 (364 days) lie in the window (a 52/53-week fiscal year case). The generated instances never hold two period ends in one window, so no test fails.",
     "fix": "Add a grader test (not a reference change) that builds a statements mapping with two period ends inside 350-380 days of the period asked for (e.g. 2019-12-28 and 2020-01-02 relative to 2020-12-31) and asserts that the latest one is used by dupont or piotroski_f_score; then re-run mutate_graders for m16 (must be killed) and the five alternative implementations (must still pass 50/50)."},
    {"id": "r7-mutate-53", "check": "2.6-mutation", "location": "tools/mutate_graders.py --unit AC2 --seeds 0-9; ledgers/AC2/scripts/project-r7/mutate_r7.txt",
     "status": "FAIL", "evidence": "53 mutants (m01-m16, p01-p37): 52 KILLED, 1 SURVIVED (m16). Script exit 1: 'mutate_graders AC2: FAIL (52/53 killed)'.",
     "fix": "Kill m16 by the grader test described in r7-mut-m16. The other 52 are killed on seed 0."},
    {"id": "r7-impls-v1-v5", "check": "2.6-autograder", "location": "ledgers/AC2/scripts/project-r7/impls/V1..V5; harness_r7.py; impls_0-49_r7.txt",
     "status": "PASS", "evidence": "Five alternative correct implementations over seeds 0-49: V1 50/50, V2 50/50, V3 50/50, V4 50/50, V5 50/50. No over-constraint."},
    {"id": "r7-grader-reference-50", "check": "2.6-autograder", "location": "course/modules/AC/AC2/grader/reference.py; tools/run_graders.py --unit AC2 --seeds 0-49",
     "status": "PASS", "evidence": "run_graders AC2: PASS (reference 50/50 seeds, slowest 0.6 s); ledgers/AC2/scripts/project-r7/run_graders_0-49.txt rc 0."},
    {"id": "r7-gates-commands", "check": "2.9-tooling", "location": "tools/check_pages.py, check_projects.py, check_dag.py, run_labs.py, page_smoke.py (--unit AC2)",
     "status": "PASS", "evidence": "run_labs AC2: PASS (11/11); check_pages AC2 PASS; check_projects AC2 PASS; check_dag AC2 PASS; page_smoke AC2 PASS (project, index, concepts, review; in-browser grader 'All 236 tests pass')."},
    {"id": "r7-hub-whole-read", "check": "2.9-structure", "location": "course/modules/AC/AC2/index.html (all 20,429 bytes)",
     "status": "PASS", "evidence": HUB + "Hours, placement (nine items, six prerequisite and three skill checks, 8 of 9 bar, no S2 item and the hub says so), the ladder sentence (matches quiz.js lines 56-77), data status, reading list, and the L05/L06 card lines were all checked against the lessons and the code. The hub's 'six to twelve study hours' is a loose range; the lessons are 8 to 12 h, inside it."},
    {"id": "r7-data-sec-reachability", "check": "2.8-data", "location": "plans/AC2-open-items.md line 10; index.html data status",
     "status": "PASS", "evidence": "curl to www.sec.gov/os/webmaster-faq and www.sec.gov/os/accessing-edgar-data: HTTP 403 (reproduced). curl to data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json: HTTP 200 with a descriptive User-Agent (no bypass of any page). The reuse statement remains unread, so every AC2 filer stays SIMULATED."},
    {"id": "r7-dechow-doi-access", "check": "2.1-access", "location": "plans/AC2-open-items.md line 24; references/references.json dechow1995detecting (doi 10.2308/tar-9505096112)",
     "status": "PASS", "evidence": "curl -s -o /dev/null -D - -L https://doi.org/10.2308/tar-9505096112 -> 302 to publications.aaahq.org/accounting-review/article/70/2/193/18940/Detecting-Earnings-Management, then HTTP 403. The row's statement (publisher page HTTP 403 to plain curl) is reproduced; the paper body was not read."},
    {"id": "r7-cards-schema", "check": "2.7-cards", "location": "course/modules/AC/AC2/cards.json (140 records)",
     "status": "PASS", "evidence": "Re-run: 140 records, ids AC2-c001..AC2-c140, no duplicate id, front or back; lessons all exist; C and D cards carry basis or cite. Grade absent on 54 definition and formula cards (BUILDER_RULES 7 requires a grade only for graded results)."},
]

NEW_IDS = {r["id"] for r in NEW_ROWS}
rows = []
for r in R6["rows"]:
    rid = r["id"]
    if rid in NEW:
        status, evidence = NEW[rid]
    elif rid in NEW_IDS:
        continue
    elif "index.html" in r["location"] or "hub" in r["location"].lower():
        status = r["status"]
        evidence = HUB + "Round-6 basis retained: " + r["evidence"]
    elif r["status"] == "PASS" and "cards" in r["location"]:
        status = "PASS"
        evidence = CARD_CARRY + "Round-6 basis: " + r["evidence"]
    elif r["status"] == "PASS":
        status = "PASS"
        evidence = CARRY + "Round-6 basis: " + r["evidence"]
    else:
        raise SystemExit(f"unhandled non-PASS round-6 row {rid}")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": evidence,
                 **({"fix": (next(x["fix"] for x in NEW_ROWS if x["id"] == "r7-mut-m16") if rid == "r6-mutate-50" else "")} if False else {})})
    if status == "FAIL":
        rows[-1]["fix"] = "See the row's evidence; fix named in r7-mut-m16 (grader test for the latest period end when two period ends fall in the 350-380 day window)." if rid == "r6-mutate-50" else "Fix named in the row's evidence."

# the three new rows about cards/plans appended in front of the carried sequence
for r in NEW_ROWS:
    if r["status"] == "FAIL" and "fix" not in r:
        raise SystemExit("FAIL row without fix: " + r["id"])
rows.extend(NEW_ROWS)

# restore the explicit fix on round-6 FAIL rows that remain FAIL in this round
for r in rows:
    if r["status"] != "PASS" and "fix" not in r:
        r["fix"] = "See evidence."

mutant_ids = [m for m in R6["mutants"]]
extra = [
    {"description": "MUTANT m14: modified Jones divides the intercept and PP&E regressors by lagged assets but leaves the revenue-less-receivables regressor unscaled.",
     "file": "ledgers/AC2/mutants/m14_modified_jones_regressors_unscaled.py", "killed_by": "test_modified_jones_coefficients_are_the_least_squares_fit (seed 0)"},
    {"description": "MUTANT m15: days_sales_outstanding returns receivables over revenue without the 365-day factor.",
     "file": "ledgers/AC2/mutants/m15_dso_without_365_days.py", "killed_by": "test_single_ratio_numbers (seed 0)"},
    {"description": "MUTANT m16: _previous picks the earliest period end in the 350-380 day window instead of the latest (SURVIVED on seeds 0-9).",
     "file": "ledgers/AC2/mutants/m16_previous_year_is_earliest_in_window.py", "killed_by": None},
]
mutants = mutant_ids + extra
killed = sum(1 for m in mutants if m.get("killed_by"))
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment = {
    "unit": "AC2",
    "slice": "project",
    "round": 7,
    "verifier": "Claude Haiku 5.5 (independent project-slice verifier, round 7; did not build AC2; fresh context)",
    "pin": "6adfd01",
    "base": "round-6 fragment (/tmp/ac2-frags/project.round6.json, pin ff9284f) read as context; project.html, grader/*, project labs, atlas, references, grader.js and pyodide-lock byte-identical since ff9284f (git diff --quiet verified)",
    "checkout": "/tmp/verify-ac2r7-p (detached at 6adfd01)",
    "scratch": "/tmp/ac2-v/project-r7; archived scripts in ledgers/AC2/scripts/project-r7/",
    "verified_at": "2026-10-27",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": R6["registry_flags"],
    "freshness_flags": [],
    "notes": R6["notes"] + [
        "Round 7 delta since ff9284f: cards.json (c024, c075, c107), index.html (L06 card body), plans/AC2-open-items.md (SEC, Beneish, dechow rows), and lesson text in L02, L05, L06, L07, L08 read as context for the cards.",
        "Mutant m16 survives: the latest-period-end rule is not tested when two period ends fall inside the window. Fix in r7-mut-m16. All other 52 mutants killed on seed 0.",
        "ResearchGate claim removed from learner text; the old UNVERIFIABLE row is re-verified as PASS because its subject no longer exists (grep returns no match).",
    ],
    "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"],
                "fail_ids": [r["id"] for r in rows if r["status"] == "FAIL"],
                "unverifiable_ids": [r["id"] for r in rows if r["status"] == "UNVERIFIABLE"],
                "mutants": len(mutants), "mutants_killed": killed},
    "verdict": "FAIL" if counts["FAIL"] or counts["UNVERIFIABLE"] or killed != len(mutants) else "PASS",
}
out = CHECKOUT / "ledgers/AC2/project.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants), killed)
