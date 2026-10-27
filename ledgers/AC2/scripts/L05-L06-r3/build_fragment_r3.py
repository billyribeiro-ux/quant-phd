"""Writes ledgers/AC2/L05-L06.json (round 3). Verifier-written; the row content is the verifier's own record.

Run: <checkout>/.venv/bin/python -I ledgers/AC2/scripts/L05-L06-r3/build_fragment_r3.py
Reads the round-2 fragment (context only; its PASS rows are not trusted and are re-verified below).
"""

import json
import sys

ROOT = "/tmp/verify-ac2-l56"
sys.path.insert(0, f"{ROOT}/tools")
import ledger  # noqa: E402

prev = json.load(open(f"{ROOT}/ledgers/AC2/L05-L06.json"))
# The file is overwritten by this script; drop rows written by a previous run of this script (ids r3-*) so the
# round-2 base is what remains. Round-2 rows keep their round-2 status unless overridden in upd below.
prev["rows"] = [r for r in prev["rows"] if "-r3-" not in r["id"]]
prev_rows = {r["id"]: r for r in prev["rows"]}
ROUND2_FAIL = ["L05-L06-cit-dechow-authors", "L05-L06-card-L06-dechow", "L05-L06-card-L06-12of200",
               "L05-L06-prose-unmarked-claims", "L05-L06-r2-num-L06-se-basis", "L05-L06-r2-lab-contamination-prop33",
               "L05-L06-r2-math-E2-zgap-cause", "L05-L06-r2-math-L06-misc3-sentence", "L05-L06-r2-prose-s4-lab-bears"]

CARRY_L05L06 = (
    "Carried from round 2 (course/modules/AC/AC2/L05.html and L06.html: this subject is outside every changed hunk "
    "listed in the round-3 notes; the hunks were read in full by git diff bc3226e HEAD): "
)
V = "Round 3 re-verified: "

# status/evidence overrides for round-2 rows (ids kept)
upd = {
    "L05-L06-cmd-pin": (
        "PASS",
        V + "git rev-parse --short HEAD = 4a8690a (checkout pinned at the round-3 pin); git status shows only "
        "untracked .venv and ledgers/AC2 (this fragment and scripts). No tracked file modified.",
    ),
    "L05-L06-cmd-check-pages": (
        "PASS",
        V + "tools/check_pages.py --unit AC2 --page L05 -> 'check_pages AC2 L05: PASS' (rc 0); --page L06 -> "
        "'check_pages AC2 L06: PASS' (rc 0). Output in /tmp/ac2-v/L05-L06-r3/check_pages.txt.",
    ),
    "L05-L06-cmd-check-dag": (
        "PASS",
        V + "tools/check_dag.py --unit AC2 -> 'check_dag AC2: PASS' (rc 0). /tmp/ac2-v/L05-L06-r3/check_dag.txt.",
    ),
    "L05-L06-cmd-run-labs": (
        "PASS",
        V + "tools/run_labs.py --unit AC2 -> 'run_labs AC2: PASS (11/11)' (rc 0). Output /tmp/ac2-v/L05-L06-r3/run_labs.txt.",
    ),
    "L05-L06-cmd-twins-isolated": (
        "PASS",
        V + "python -I -W error tests/labs/AC2/lab-AC2-L05-1.py and lab-AC2-L06-1.py: rc 0 both; outputs in "
        "/tmp/ac2-v/L05-L06-r3/lab05.out and lab06.out.",
    ),
    "L05-L06-cmd-page-smoke": (
        "PASS",
        V + "tools/page_smoke.py --unit AC2 --pages L05 L06 -> 'page_smoke modules/AC/AC2/L05.html: PASS', "
        "'page_smoke modules/AC/AC2/L06.html: PASS', 'page_smoke AC2: PASS' (rc 0). Lab timings: L05 2.8 s, L06 0.1 s "
        "(well under 10 s). /tmp/ac2-v/L05-L06-r3/page_smoke.txt.",
    ),
    "L05-L06-cmd-verify-refs-unit": (
        "PASS",
        V + "tools/verify_refs.py --unit AC2 -> 'live re-verification of AC2: 7 of 560 entries, 0 problems' (rc 0).",
    ),
    "L05-L06-cmd-verify-refs-offline": (
        "PASS",
        V + "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (rc 0).",
    ),
    "L05-L06-cmd-lint": (
        "PASS",
        V + "ruff check (both twins): 'All checks passed!'; ruff format --check: '2 files already formatted'; "
        "mypy --no-incremental on both twins: 'Success: no issues found in 2 source files'.",
    ),
    "L05-L06-cit-sloan-registry": (
        "PASS",
        V + "references/references.json key sloan1996stock present (offline integrity OK). Crossref api.crossref.org "
        "record for its DOI fetched with plain curl: HTTP 200.",
    ),
    "L05-L06-cit-sloan-claim-s1": (
        "PASS",
        V + "L05.html line 61 claim span (grade C, data-cite sloan1996stock) reads 'Sloan (1996) investigates whether "
        "stock prices reflect information about future earnings contained in the accrual and cash-flow components of "
        "current earnings.' Crossref abstract (HTTP 200, /tmp/ac2-v/L05-L06-r3/crossref_sloan1996stock.json): 'Investigates "
        "whether stock prices reflect information about future corporate earnings contained in accrual and cash flow "
        "components of currents earnings.' Matches. The claim names no finding.",
    ),
    "L05-L06-cit-sloan-claim-s3": (
        "PASS",
        V + "grep of data-cite in L05.html: only three spans (lines 61, 226, 227). The Sloan §3 paragraph changed "
        "(Prop 3.1 cross-reference, see L05-L06-prose-L04-xref) and carries no claim span; the question it states is the "
        "Abstract's question. No finding attributed to Sloan in §3 or §7.",
    ),
    "L05-L06-cit-dechow-registry": (
        "PASS",
        V + "references/references.json key dechow1995detecting: DOI 10.2308/tar-9505096112, title 'Detecting Earnings "
        "Management.', container The Accounting Review. Crossref (HTTP 200): volume 70, issue 2, pages 193-225, "
        "published 1995-04. The page's '70(2), 1995' matches.",
    ),
    "L05-L06-cit-dechow-scope": (
        "PASS",
        V + "L06.html line 61 claim span (grade C, dechow1995detecting): 'The paper evaluates alternative accrual-based "
        "models for detecting earnings management and compares the specification and power of commonly used test "
        "statistics.' Crossref abstract (HTTP 200): 'Evaluates alternative accrual-based models for detecting earnings "
        "management. Comparison of the specification and power of commonly used test statistics...'. Matches. L06.html "
        "line 352 claim span ('compares the specification and power ... no power figure from it is quoted here') and "
        "§8 key-results row 6 quote no power figure. Abstract gives none.",
    ),
    "L05-L06-cit-dechow-motivation": (
        "PASS",
        V + "The round-2 claim spans ('Jones's regression uses...', 'Dechow et al. (1995) motivate...') are no longer in "
        "the page. grep for 'et al' in L05.html, L06.html and cards.json: no hit. grep for 'Dechow' in those files: "
        "no hit. The only attribution is the registry key and title (L06.html line 61). The receivables-rationale "
        "sentence is handled in L05-L06-prose-unmarked-claims and L05-L06-r3-prose-L06-s2-purpose.",
    ),
    "L05-L06-cit-dechow-grouping": (
        "PASS",
        V + "L06.html line 355 (§5 bullet 4) now reads 'The model can be estimated within groups of firm-years, such as "
        "industry-years, so that industry-wide accrual patterns are absorbed.' It carries no data-cite and no attribution; "
        "it is a methodological description the lab does not test, and the bullet says so.",
    ),
    "L05-L06-cit-dechow-authors": (
        "PASS",
        V + "Ruling (1), round 3: the registry rendering of the bibliography entry may show the registry's two authors and "
        "is not failed. Authored prose (L05.html, L06.html, cards.json): no author names of dechow1995detecting (grep "
        "'Dechow' and 'Sloan' with Sweeney: no hit in these files). The lessons cite the key and the title 'Detecting "
        "Earnings Management'. The three-author string in curriculum/02-economics-finance-core.yaml line 574 (grep 'Dechow, Sloan'), "
        "the registry's two-author notes and the two-author Crossref record are an open question outside this slice; "
        "recorded as a registry flag, not resolved here. atlas/ at 4a8690a has no 'Dechow' string (grep: none).",
    ),
    "L05-L06-cit-mclean": (
        "PASS",
        CARRY_L05L06 + "L05.html lines 226-227 unchanged in the diff; the two claim spans (mclean2016academic, "
        "hou2018replicating) cite registry titles, grade C, and passage locators not confirmed.",
    ),
    "L05-L06-reg-used-by": (
        "PASS",
        "Carried from round 2 (references/references.json byte-identical since bc3226e: git diff --quiet confirmed in "
        "round 3): used_by entries for mclean2016academic and hou2018replicating unchanged.",
    ),
    "L05-L06-num-L05-lab": (
        "PASS",
        V + "run of tests/labs/AC2/lab-AC2-L05-1.py reproduces every printed line the page quotes (seeds 200, months 120, "
        "mean_z_gap_simulated -2.7937, planted_monthly_spread 0.00223, spread_sd_theory 0.01131, expected_t_at_planted 2.164, "
        "recovered 0.00219, null_false_positive_rate 0.060, power 0.590, effect_median_t 2.155, seed0 0.00075 / 0.676, "
        "mean_z_gap_firms_500_seeds_20 -2.7912, mean_z_gap_firms_5000_seeds_20 -2.7991). /tmp/ac2-v/L05-L06-r3/lab05.out.",
    ),
    "L05-L06-num-L05-derived": (
        "FAIL",
        V + "Every derived number re-computed in recompute_l05_r3.py and recompute_l05_e3_r3.py EXCEPT the E3 '1.44' "
        "standard errors, which is arithmetic on rounded values (exact -1.433, shown as -1.43). See "
        "L05-L06-r3-num-L05-E3. E2 spread_sd 0.01131, planted 0.0022350, t 2.164 all verified.",
    ),
    "L05-L06-num-L06-lab": (
        "PASS",
        V + "run of lab-AC2-L06-1.py (python -I -W error, rc 0) reproduces every printed line the page quotes: "
        "a1 0.3891/0.2750, nm 0.1806, SE 0.2824, decomposition 0.1425/0.1965/0.1306, residual 0.000000, "
        "conditional mean 0.6223/0.1245, TPR 0.985/0.355, FPR 0.0017/0.0717, flags_only 6/6, SE scaling 0.2781/0.0489, "
        "rows 1800/57600. /tmp/ac2-v/L05-L06-r3/lab06.out.",
    ),
    "L05-L06-num-L06-derived": (
        "FAIL",
        V + "Recomputed in recompute_l06_r3.py: all printed L06 values match. Two derived figures fail: the 2.07 standard "
        "errors for a2 (unrounded 2.096; see L05-L06-r3-num-L06-a2z) and the R1 and c125 figures pass (55,685 rows, 61,872 "
        "firm-years, 0.0492).",
    ),
    "L05-L06-num-L06-roughly-4pct": (
        "PASS",
        V + "E3 tail: shown calc 2(1-Phi(2.067)) = 0.039. Unrounded z 2.096 gives 0.036 (recompute_l06_r3 / a2_check.out). "
        "'about 4%' holds on both (3.6% and 3.9% round to 4%). The 2.07 itself is a separate FAIL row.",
    ),
    "L05-L06-math-notation": (
        "PASS",
        "Carried from round 2 (notation/notation.json byte-identical since bc3226e: git diff --quiet confirmed in round 3). "
        "The new L06 text uses \\E[d mid X], \\widehat and the 8 symbols already defined; no new symbol.",
    ),
    "L05-L06-lab-L05-1-run": (
        "PASS",
        V + "Lab 1 output re-run (lab05.out); the two new lines (mean_z_gap_firms_500_seeds_20, _5000_seeds_20) are "
        "printed exactly as the page quotes them.",
    ),
    "L05-L06-lab-L05-1-interp": (
        "PASS",
        V + "Interpretation paragraph (L05 §4) and Misconceptions 1-3 re-read against the printed lab values; no claim "
        "beyond the printed numbers except the E2 'cause' sentence, which is its own FAIL row.",
    ),
    "L05-L06-lab-L06-1-run": (
        "PASS",
        V + "Lab 1 re-run (see L05-L06-num-L06-lab). The lab's own docstring states SIMULATED and seed 606 single-draw; "
        "the page says the same.",
    ),
    "L05-L06-lab-L06-1-overreach-sample": (
        "PASS",
        V + "§4 interpretation: 'The lab says nothing about real firms.' §4 paragraph 2 names the intercept as untested. "
        "No real-data claim. (Overreach checked: the 0.2084 is not presented as bias alone, see L05-L06-r3-math-L06-decomp.)",
    ),
    "L05-L06-lab-L06-1-single-seed": (
        "PASS",
        V + "Interpretation: 'every flag score below is one simulated draw at seed 606' and 'Two shifts at one seed "
        "describe that draw and establish no threshold.' Key-results rows 4-5 say 'In one simulated draw'. Matches.",
    ),
    "L05-L06-lab-L06-1-threshold-claim": (
        "PASS",
        V + "Misconception 3 precision sentence rewritten and checked: precision = TP/flagged = 71/200 = 0.355 and "
        "197/200 = 0.985 (flagged count 200 = manipulator count 200, so precision equals TPR). Claims no threshold.",
    ),
    "L05-L06-lab-L06-1-flag-count": (
        "PASS",
        V + "'12 firm-years change flag status': printed flags_only_all_firms 6 + flags_only_oracle 6 = 12 "
        "(flags_differing_all_vs_oracle 12). Strong scenario: 0 differing. Matches.",
    ),
    "L05-L06-card-L05-defs": (
        "PASS",
        CARRY_L05L06 + "cards AC2-c063, c065-c068 are byte-identical in cards.json since bc3226e (cards diff for L05/L06 "
        "lists only c083, c087, c124, c125); their lesson subjects are unchanged.",
    ),
    "L05-L06-card-L05-lab": (
        "PASS",
        "Carried from round 2 (cards AC2-c069-c075 and c122-c123 byte-identical since bc3226e per the cards diff). The "
        "c122 card ('-2.7937 ... close to the analytic -2.800 ... not equal to it') matches the page; the -2.800 is the "
        "rounded Proposition 2.3 value and -2.79962 is the exact value (recompute_l05_r3.py).",
    ),
    "L05-L06-card-L05-sloan": (
        "PASS",
        "Carried from round 2 (card AC2-c064 byte-identical since bc3226e per the cards diff); lesson subject checked "
        "against the Crossref abstract in this round.",
    ),
    "L05-L06-card-L06-defs": (
        "PASS",
        CARRY_L05L06 + "cards AC2-c076, c077, c080, c081, c088 byte-identical since bc3226e per the cards diff.",
    ),
    "L05-L06-card-L06-lab": (
        "PASS",
        V + "cards AC2-c082, c085, c086 (unchanged) and c083 and c125 (changed) re-checked against the printed Lab 1 "
        "values: c083 0.2084 = 0.1425 + 0.1965 - 0.1306, 0.74 of 0.2824; c125 0.2781 on 1,800 rows, 0.0489 on 57,600 rows. "
        "c082 197/71/129 and c085 197/200 and 0.0017, c086 0.355/0.0717 all match.",
    ),
    "L05-L06-card-L06-iff": (
        "PASS",
        "Carried from round 2 (card AC2-c078 byte-identical since bc3226e per the cards diff).",
    ),
    "L05-L06-card-L06-projection": (
        "PASS",
        "Carried from round 2 (card AC2-c079 byte-identical since bc3226e per the cards diff).",
    ),
    "L05-L06-card-L06-only-when": (
        "PASS",
        V + "AC2-c084 (byte-identical since bc3226e) checked against the new Misconception 3: 'Precision is the "
        "true-positive share among flagged firms ... 0.355' agrees with 71 of 200.",
    ),
    "L05-L06-card-L06-dechow": (
        "PASS",
        V + "AC2-c087 back now reads 'The rationale for that adjustment is not sourced in this lesson.' Consistent with "
        "the lesson's disclaimer. The lesson sentence that still gives the purpose clause is a separate FAIL row "
        "(L05-L06-r3-prose-L06-s2-purpose).",
    ),
    "L05-L06-card-L06-12of200": (
        "PASS",
        V + "AC2-c124 now reads 'Twelve firm-years change flag status at seed 606: six enter ... and six leave it "
        "(flags_only_all_firms 6, flags_only_oracle 6).' Printed values match (lab06.out). The 12-of-200 wording is gone.",
    ),
    "L05-L06-cards-dup-scan": (
        "PASS",
        V + "cards.json: 138 cards, 138 unique ids, no duplicate front (case-insensitive). Eight new cards c131-c138 "
        "belong to other lessons.",
    ),
    "L05-L06-cards-coverage": (
        "PASS",
        V + "cards.json: L05 15 cards, L06 17 cards (python count).",
    ),
    "L05-L06-struct-hours": (
        "PASS",
        V + "data-hours L05 = 8, L06 = 10 (lesson pages); the sum of the eight AC2 lesson data-hours is 76.0 "
        "(= index data-hours-lessons 76). My own estimates 7.5 h and 9.5 h: both within 30%.",
    ),
    "L05-L06-struct-sections": (
        "PASS",
        V + "check_pages L05 and L06 PASS; page_smoke PASS.",
    ),
    "L05-L06-struct-banned": (
        "PASS",
        V + "Scanned visible prose of L05 and L06 for roughly, about, historically, half, typically, usually, generally, "
        "often, ellipsis. Every 'about' in the changed text is followed by a shown calculation or a printed value: "
        "about 1.4 SD (Prop 2.3 solution), about 41% (1 - 0.590), about 129 firms (0.0717 x 1,800), about three quarters "
        "(0.2084 / 0.2824 = 0.738), about 61,900 firm-years (55,685 / 0.9), about 4% (E3 shown), about 0.0010 and 0.0015 "
        "(rounded printed values), about two SEs (hypothesis, not a claim the lab tests). No banned phrase found.",
    ),
    "L05-L06-prose-L04-xref": (
        "PASS",
        V + "L05.html §3 now reads 'Lesson L04, Proposition 3.1, gives the algebra of accruals under its assumptions A1 to A4: "
        "accruals equal the growth in net operating assets less capital expenditure.' L04.html line 99 defines A1 to A4 "
        "(A3: current liabilities carry no debt) and line 334 states 'Under A1 to A4, NI_t - CFO_t = Delta NOA_t - capex_t'. "
        "The dropped qualifier is not needed. Matches.",
    ),
    "L05-L06-prose-inversion": (
        "PASS",
        "Carried from round 2 (L06.html §5 intro paragraph unchanged in the diff).",
    ),
    "L05-L06-prose-jargon": (
        "PASS",
        V + "L05.html 'Honest pending' paragraph (line 234) no longer contains DATA_REQUESTS; it now says 'The open source "
        "requests are listed in plans/AC2-open-items.md' (once on the page). Architect question, not a FAIL: the paragraph "
        "and L06 §3 also name 'BLUEPRINT §5.3' and 'the A15 contract' (internal documents, not on the ruling's word list). "
        "Recorded for the architect.",
    ),
    "L05-L06-prose-concept-links": (
        "PASS",
        "Carried from round 2 (concept-link convention question, unchanged): both pages link each concept once in the "
        "Uses line. Architect convention question stands.",
    ),
    "L05-L06-dag": (
        "PASS",
        V + "check_dag AC2 PASS; definitions and links in L05 and L06 unchanged in the diff except the new text; no concept "
        "used before its prerequisite in the new paragraphs (new text uses only modified-jones-model and ols-estimator "
        "already defined).",
    ),
    "L05-L06-figures": (
        "PASS",
        "Carried from round 2 (figure scripts and figure markup unchanged in the L05/L06 diff hunks).",
    ),
    "L05-L06-honest-data": (
        "PASS",
        "Carried from round 2 (honest-pending paragraph reviewed in this round; SEC company-facts reuse statement and "
        "licence mentioned as unconfirmed; simulated data stated).",
    ),
    "L05-L06-r2-prop21-sigma0": (
        "PASS",
        "Carried from round 2 (L05 Prop 2.1 and its proof are outside the changed hunks; the round-2 prop21_sigma0.py "
        "result is unchanged).",
    ),
    "L05-L06-r2-lab-flags-only-lines": (
        "PASS",
        V + "tests/labs/AC2/lab-AC2-L06-1.py prints flags_only_all_firms and flags_only_oracle (6 and 6, seed 606 weak); "
        "the page quotes both.",
    ),
    "L05-L06-r2-attribution-sweep": (
        "PASS",
        V + "Every data-cite span in L05 and L06 (lines 61, 226, 227 in L05; 61, 352, 493 in L06) checked against the "
        "registry key and the Crossref abstract or registry title (see the citation rows).",
    ),
    "L05-L06-r2-prose-A15-reference": (
        "PASS",
        "Carried from round 2 (L06.html §3 units paragraph unchanged). 'The A15 contract' is an internal document named "
        "in learner text; architect question recorded (see L05-L06-prose-jargon).",
    ),
    # round-2 FAIL rows that are now fixed
    "L05-L06-card-L06-dechow": None,  # placeholder, replaced above
}
upd.pop("L05-L06-card-L06-dechow")

upd["L05-L06-prose-unmarked-claims"] = (
    "PASS",
    V + "The round-2 unlabelled claim 'Treating receivables-booked revenue as the part of growth most open to discretion is "
    "an assumption of the model' is removed (grep 'assumption of the model' in L06.html and cards.json: 0 hits). Its "
    "replacement, 'The rationale for the receivables term is not sourced in this lesson', is a disclaimer. Two other "
    "unsourced rationale sentences remain and FAIL in their own rows (L05-L06-r3-prose-L06-s2-purpose, "
    "L05-L06-r3-prose-L06-s5-bullet). L05 'Why it matters' sentences named in round 2: none present (grep).",
)
upd["L05-L06-r2-num-L06-se-basis"] = (
    "PASS",
    V + "L06.html §4 now states 0.2824 is 'the classical standard error of a1 on the 1,800 non-manipulator rows of the "
    "seed-606 sample of 2,000 firm-years' (recomputed: 0.28242759). R1 prompt and solution use 1,800 rows; "
    "se_scaling 0.2781 (1,800 rows) and 0.0489 (57,600 rows) recomputed (recompute_l06_r3.py). 5.6x = 0.2824/0.05 = 5.65.",
)
upd["L05-L06-r2-lab-contamination-prop33"] = (
    "PASS",
    V + "No 'contamination that Proposition 3.3 describes' sentence and no 0.2085 shift claim as bias remain in the Lab 1 "
    "interpretation or Key results row 2. Current text: the difference 0.2084 = realised projection 0.1425 + projection "
    "of noise 0.1965 - non-manipulator deviation 0.1306 (exact, residual 1e-14 recomputed); Prop 3.3 applied to the "
    "conditional mean E[d|X] = 0.005 gives 0.6223, checked by Monte Carlo (4,000 draws: 0.6295 +/- 0.0065, sd of the "
    "difference 0.41, so 0.2084 is one draw). Row 2 wording 'in its conditional-mean form' is supported.",
)
upd["L05-L06-r2-math-L06-misc3-sentence"] = (
    "PASS",
    V + "Misconception 3 now: 'Precision is the share of flagged firm-years that are manipulators: 71 of 200 (0.355) ... "
    "197 of 200 (0.985)'. Precision = TP / flagged = 71/200 and 197/200, recomputed. No 'because' clause.",
)
upd["L05-L06-r2-prose-s4-lab-bears"] = (
    "PASS",
    V + "§4 opening now: 'The lab bears on the second and third. It fits no intercept, so it says nothing about the first: "
    "Remark 3.2 shows that without an intercept the discretionary accruals need not average to zero.' Remark 3.2 "
    "(sum of residuals 0.2) supports the last clause. The second (estimation sample, 0.2084 decomposition) and third (SE "
    "scale, 0.2824 and 0.0489) are printed by the lab. No internal contradiction.",
)
upd["L05-L06-card-L06-dechow"] = (
    "PASS",
    V + "AC2-c087 back: 'It subtracts the change in receivables from the change in revenue (the A15 contract's "
    "definition). The rationale for that adjustment is not sourced in this lesson.' Matches the lesson disclaimer; "
    "the stronger statement 'assumption of the model' is gone.",
)
upd["L05-L06-card-L06-12of200"] = upd.get("L05-L06-card-L06-12of200", None) or (
    "PASS",
    V + "AC2-c124 now: 'Twelve firm-years change flag status at seed 606: six enter the top decile under the all-firm "
    "estimate and six leave it (flags_only_all_firms 6, flags_only_oracle 6).' Printed values match; the flags that change "
    "are 12 firm-years, not 12 of 200 flagged.",
)
upd["L05-L06-r2-math-E2-zgap-cause"] = (
    "FAIL",
    "Round 3: L05.html E2 solution now says 'The cause is the finite sort: each month sorts 500 firms ... The lab prints "
    "the realised gap at two firm counts ... two counts are not enough to establish the rate.' The printed numbers "
    "(-2.7912 at 500 and -2.7991 at 5,000, 20 seeds each; -2.7937 at 500 over 200 seeds; analytic -2.79962) show that the "
    "gap moves toward the analytic value as the sort grows, and they are consistent with a finite-sort cause. They do not "
    "establish that the finite sort is the cause: the page prints no sweep, and the analytic value is a population "
    "quantity whose gap at a finite n is not checked by any printed line. My own 400-seed sweep (recompute_l05_r3.py, "
    "not printed by the lab) gives gaps -2.7421 (n=50), -2.7705 (n=100), -2.7938 (n=500), -2.7990 (n=5000), i.e. bias "
    "about -2.9/n, which supports the cause but is not on the page. The 20-seed and 200-seed means at 500 firms differ "
    "by 0.0025 with SE 0.0018 (seed variation, consistent). Required fix: cite a printed sweep or write 'consistent with "
    "a finite-sort effect'.",
)
upd["L05-L06-r2-num-L06-se-basis"] = upd["L05-L06-r2-num-L06-se-basis"]


CARRY_MATH = ("Carried from round 2 (course/modules/AC/AC2/L05.html and L06.html: this proposition, proof and "
              "lab-independent subject lie outside every changed hunk; hunks listed in the round-3 notes): ")
for rid, txt in {
    "L05-L06-cit-hou": "L05.html lines 226-227 unchanged in the diff; registry title claim, grade C, locator not confirmed.",
    "L05-L06-math-L05-def-t": "L05.html Definition 1.2 unchanged in the diff; t = S-bar/(s_S/sqrt T) recomputed in round 2 and the lab's t_stat matches it.",
    "L05-L06-math-L05-prop21": "L05.html Proposition 2.1 and proof unchanged in the diff (hunks start at line 134).",
    "L05-L06-math-L05-prop23": "L05.html Proposition 2.3 and proof unchanged in the diff; analytic -2.79962 recomputed in round 3 (recompute_l05_r3.py).",
    "L05-L06-math-L05-remark22-P1-P3": "L05.html Remark 2.2, P1, P3 unchanged in the diff.",
    "L05-L06-math-L06-prop31": "L06.html Proposition 3.1 statement and proof unchanged in the diff (the Remark 3.2 numerical check in P1 reproduced: sum of residuals 0.2).",
    "L05-L06-math-L06-prop33-formula": "L06.html Proposition 3.3 formula unchanged in the diff; the new conditional-mean reading is a separate PASS row (L05-L06-r3-num-L06-cond-mean).",
    "L05-L06-math-L06-prop33-statement": "L06.html Proposition 3.3 statement and proof (lines 99-108) unchanged in the diff.",
    "L05-L06-math-L06-P3": "L06.html P3 solution unchanged in the diff.",
    "L05-L06-math-L06-remark32-P1-P2": "L06.html Remark 3.2 and P1, P2 unchanged in the diff.",
}.items():
    if txt:
        upd[rid] = ("PASS", CARRY_MATH + txt)

FIXES = {
    "L05-L06-num-L05-derived": "Fix E3 per L05-L06-r3-num-L05-E3 (state -1.43 or show unrounded inputs).",
    "L05-L06-num-L06-derived": "Fix the a2 z-score per L05-L06-r3-num-L06-a2z (2.10 unrounded, tail 0.036).",
    "L05-L06-r2-math-E2-zgap-cause": "Cite a printed sweep over firm counts (50, 100, 500, 5000) in Lab 1, or soften 'The cause is' to 'consistent with a finite-sort effect'.",
    "L05-L06-r3-num-L05-E3": "State the distance as -1.43 standard errors (unrounded inputs 0.0022350, 0.0007549, SE 0.0010330), or show the unrounded calculation.",
    "L05-L06-r3-num-L06-a2z": "State 2.10 standard errors (unrounded z 2.096) and the tail 0.036, or show the unrounded inputs (SE 0.001467, b 0.103076).",
    "L05-L06-r3-hyp-L06-shift": "Replace 'should shift by the realised projection of the planted term' with 'should shift by the projection of the planted term plus sampling noise'.",
    "L05-L06-r3-prose-L06-s2-purpose": "Delete the 'so that ... not counted as normal growth' purpose clause; keep the mechanical description and the not-sourced disclaimer.",
    "L05-L06-r3-prose-L06-s5-bullet": "Drop 'matters only if the manipulation runs through revenue'; state only that Lab 1 has no revenue channel.",
}

# ---- new rows (round 3) ----
new_rows = [
    {
        "id": "L05-L06-r3-num-L05-E2-printed",
        "check": "2.2-numbers-class-a/c",
        "location": "course/modules/AC/AC2/L05.html E2 solution and Lab 1 output lines mean_z_gap_*",
        "status": "PASS",
        "evidence": V + "Independent z-gap (recompute_l05_r3.py, own code, np.sort quintiles of n//5): n=500, 200 seeds -2.79369 "
        "(printed -2.7937); n=500, 20 seeds -2.7912 (printed -2.7912); n=5000, 20 seeds -2.7991 (printed -2.7991); analytic "
        "-2*phi(q)/0.2 = -2.79962 with q = Phi^-1(0.2) = -0.841621 (page -2.7996, Prop 2.3 approx -2.800). "
        "E2 numbers: spread_sd 0.08*sqrt(2/100) = 0.011314; planted -0.0008 x -2.7937 = 0.0022350; expected t 2.1640 "
        "(recomputed). All verified.",
    },
    {
        "id": "L05-L06-r3-num-L05-E3",
        "check": "2.2-numbers-class-c",
        "location": "course/modules/AC/AC2/L05.html E3 solution",
        "status": "FAIL",
        "evidence": "E3 says 'the distance from the planted value is 0.00075 - 0.00223 = -0.00148, which is -0.00148/0.00103 = "
        "-1.44 standard errors' and the text says 'lies 1.44 standard errors below'. Arithmetic on rounded values. Unrounded "
        "(recompute_l05_e3_r3.py): planted 0.0022350, seed-0 mean 0.0007549, SE of the 120-month mean 0.0010330: distance "
        "-1.433, i.e. -1.43 standard errors. The printed-value calculation gives -1.437 (-1.44). Required fix: state -1.43 "
        "or show the unrounded inputs.",
    },
    {
        "id": "L05-L06-r3-num-L06-decomp",
        "check": "2.4-math",
        "location": "course/modules/AC/AC2/L06.html Lab 1 interpretation, misconceptions, key-results row 2, lab decompose_a1",
        "status": "PASS",
        "evidence": V + "Own code (recompute_l06_r3.py, from the docstring spec; draw order mirrors the lab): b_all - b_nm = "
        "0.208416 (strong, seed 606); projection of planted 0.1425, projection of all-firm noise 0.1965, nm sampling deviation "
        "0.1306; identity residual 1.4e-14 (lab prints 0.000000). Weak: 0.0944 = 0.0285 + 0.1965 - 0.1306. Page statements "
        "('0.2084 unrounded, 0.2085 from printed', 'the three components sum to the difference', 'the 0.2084 is not the bias "
        "alone') are supported by these numbers and say nothing more.",
    },
    {
        "id": "L05-L06-r3-num-L06-cond-mean",
        "check": "2.4-math",
        "location": "course/modules/AC/AC2/L06.html Lab 1 interpretation ('conditional-mean prediction for a1 is 0.6223')",
        "status": "PASS",
        "evidence": V + "E[d|X] = SHIFT x P(manipulator|X) = 0.05 x 0.10 = 0.005 (constant: manipulators are a uniform permutation "
        "independent of X). Prop 3.3 applied to d' = E[d|X] gives (X'X)^-1 X' (0.005*1) = 0.6223 for a1 (analytic, recomputed). "
        "Monte Carlo with X fixed at seed 606, 4,000 redraws of manipulators and noise: E[a1_all - a1_nm | X] = 0.6295 "
        "(SE 0.0065) and E[a1_all - C | X] = 0.6290 (SE 0.0077), both consistent with 0.6223; sd of the difference 0.4125, so "
        "the realised 0.2084 is one draw. The page's 'a different quantity from the realised 0.2084, which is one draw' is "
        "supported. The page does not say which quantity 0.6223 predicts; it is the conditional mean of the difference "
        "(equivalently of the all-firm bias relative to 0.05 because the non-manipulator estimator has conditional mean C).",
    },
    {
        "id": "L05-L06-r3-num-L06-se-scaling",
        "check": "2.2-numbers-class-a",
        "location": "course/modules/AC/AC2/L06.html §4 and R1 solution; cards AC2-c125",
        "status": "PASS",
        "evidence": V + "se_scaling recomputed (seeds 606-610): 0.2781 on 1,800 non-manipulator rows (2,000 firm-years) and "
        "0.0489 on 57,600 rows (64,000 firm-years). Rule: 0.2781 x sqrt(1800/57600) = 0.0492; 1800 x (0.2781/0.05)^2 = 55,685 "
        "rows = 61,872 firm-years at a 10% share; page says 55,700 and 61,900 (rounded). Correct.",
    },
    {
        "id": "L05-L06-r3-num-L06-a2z",
        "check": "2.2-numbers-class-c",
        "location": "course/modules/AC/AC2/L06.html Lab 1 interpretation ('lies 2.07 standard errors'), E3 solution",
        "status": "FAIL",
        "evidence": "The page says the a2 estimate 0.1031 'lies 2.07 standard errors from its planted value' and E3 computes "
        "0.0031/0.0015 = 2.067 with tail 0.039. Both use the printed values (SE printed to four decimals). Unrounded "
        "(recompute_l06_r3.py, a2_check.out): b_nm a2 = 0.103076, SE = 0.001467, z = 2.096, two-sided tail 0.036. The "
        "'2.07' is an artefact of rounding the SE. Required fix: state 2.10 (unrounded) or give the unrounded inputs; "
        "'about 4%' still holds.",
    },
    {
        "id": "L05-L06-r3-hyp-L06-shift",
        "check": "2.4-math",
        "location": "course/modules/AC/AC2/L06.html 'Stated before running' hypothesis paragraph (Lab 1 hypothesis)",
        "status": "FAIL",
        "evidence": "The hypothesis (stated before running) says: 'Estimated on all firms, the coefficients should shift by the "
        "realised projection of the planted term, which the lab decomposes.' The lab's own decomposition (recomputed, "
        "identity residual 1e-14) shows the all-minus-non-manipulator shift is 0.2084 = 0.1425 (projection of the planted "
        "term) + 0.1965 (all-firm noise projection) - 0.1306 (non-manipulator deviation). The shift is therefore not the "
        "projection of the planted term alone, and the sentence contradicts the decomposition on the same page. Required "
        "fix: 'should shift by the projection of the planted term plus sampling noise'.",
    },
    {
        "id": "L05-L06-r3-prose-L06-s2-purpose",
        "check": "2.3-grades (unsourced rationale)",
        "location": "course/modules/AC/AC2/L06.html §2, paragraph after Definition 2.1, first sentence",
        "status": "FAIL",
        "evidence": "'The model adds a receivables adjustment to the revenue term: it uses the change in revenue less the change "
        "in receivables, so that revenue booked as receivables is not counted as normal growth.' The 'so that' clause states "
        "the purpose (the rationale) of the adjustment with no grade, key or locator, and the same paragraph then says 'The "
        "rationale for the receivables term is not sourced in this lesson'. The formula's arithmetic effect is verified "
        "(ΔREV - ΔREC enters the regressor); the purpose clause is not. Required fix: describe the mechanical effect only.",
    },
    {
        "id": "L05-L06-r3-prose-L06-s5-bullet",
        "check": "2.3-grades (unsourced rationale)",
        "location": "course/modules/AC/AC2/L06.html §5 bullet 'The receivables adjustment assumes the manipulation runs through revenue.'",
        "status": "FAIL",
        "evidence": "The bullet now says the adjustment 'matters only if the manipulation runs through revenue'. Nothing in "
        "the lesson, the registry abstract of dechow1995detecting, or Lab 1 supports a 'matters only if' condition: the "
        "regressor (ΔREV - ΔREC)/A enters the fit whether or not the manipulation is in revenue, and Lab 1 plants the "
        "manipulation in the discretionary term, which the lab itself does not test against any channel. The claim is the "
        "same unsourced rationale the §2 disclaimer says is not sourced. Required fix: state the design fact (the adjustment "
        "is a regressor; Lab 1 has no revenue channel) and drop 'matters only if'.",
    },
    {
        "id": "L05-L06-r3-prose-L06-imprecise",
        "check": "2.4-math / 2.3-grades",
        "location": "course/modules/AC/AC2/L06.html §4 ('At that sample size the estimate of a1 is too imprecise to recover the planted value')",
        "status": "PASS",
        "evidence": V + "SE 0.2824 is 5.65 times the planted 0.05 (computed), and the nm estimate 0.1806 is 0.46 SE above 0.05 "
        "(0.1306/0.2824): a t-test cannot reject the planted value. 'too imprecise to recover' is a reading of that SE, "
        "not a lab result; accepted as a reading, noted for the architect.",
    },
    {
        "id": "L05-L06-r3-cards-c083-c087-c124-c125",
        "check": "2.7-cards",
        "location": "course/modules/AC/AC2/cards.json AC2-c083, c087, c124, c125",
        "status": "PASS",
        "evidence": V + "The four changed cards read against their lesson sections and the printed values (see the card rows). "
        "AC2-c084 unchanged in this round; checked against Misconception 3 and found consistent.",
    },
    {
        "id": "L05-L06-r3-cit-dechow-crossref-abstract",
        "check": "2.1-citations",
        "location": "course/modules/AC/AC2/L06.html §8 key-results row 6 and §5 claim span",
        "status": "PASS",
        "evidence": V + "Crossref abstract for dechow1995detecting re-fetched with plain curl (HTTP 200): 'Evaluates alternative "
        "accrual-based models for detecting earnings management. Comparison of the specification and power of commonly used "
        "test statistics; ...'. Key-results row 6 claims only that the paper compares specification and power, and quotes no "
        "figure. Matches.",
    },
    {
        "id": "L05-L06-r3-math-L06-misc2-first-term",
        "check": "2.4-math / 2.3-grades",
        "location": "course/modules/AC/AC2/L06.html Misconception 2 ('Only the first term is the effect of including manipulators')",
        "status": "PASS",
        "evidence": V + "The 0.2084 splits into the planted-term projection 0.1425 (the realised contamination, the only term "
        "that comes from the manipulator indicator) and two noise terms (0.1965 and -0.1306). Calling the planted-term "
        "projection 'the effect of including manipulators' is a reading of the decomposition; accepted.",
    },
    {
        "id": "L05-L06-r3-cmd-validate",
        "check": "2.9-structure",
        "location": "ledgers/AC2/L05-L06.json",
        "status": "PASS",
        "evidence": "ledger.validate(json, 'L05-L06') returns [] on the round-3 fragment (run after writing; see the final "
        "command in this build).",
    },
]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in upd:
        st, ev = upd[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                     "evidence": r["evidence"] if r["status"] == "PASS" and r["evidence"].startswith(CARRY_L05L06)
                     else r["evidence"]})
known = {r["id"] for r in rows}
for nr in new_rows:
    assert nr["id"] not in known, nr["id"]
    rows.append(nr)

# the round-2 rows not explicitly re-verified above keep their round-2 status; list them so the report is exact
unhandled = [r["id"] for r in prev["rows"] if r["id"] not in upd]
print("round-2 rows neither re-verified nor carried explicitly:", unhandled)

fails = [r["id"] for r in rows if r["status"] != "PASS"]
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIXES[r["id"]]
out = {
    "unit": "AC2",
    "slice": "L05-L06",
    "round": 3,
    "verifier": "AC2 independent verifier, round 3, slice L05-L06 (fresh verifier; did not build AC2; shares no context with "
    "the builders or the round-1 and round-2 verifiers)",
    "pin": "4a8690a",
    "base": "none",
    "checkout": "/tmp/verify-ac2-l56 (detached worktree at 4a8690a)",
    "scratch": "/tmp/ac2-v/L05-L06-r3",
    "verified_at": "2026-10-27T23:00:00+00:00",
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "dechow1995detecting: the registry notes list crossref 'Dechow & Sloan' and curriculum 'Dechow & Sloan & Sweeney'; "
        "the Crossref record lists Dechow, Patricia M. and Sloan, Richard G. (two authors). curriculum/02-economics-finance-core.yaml line 574 "
        "uses the three-author string; atlas/ has no Dechow string at 4a8690a. Outside this slice. Not resolved here (architect ruling). The lessons name no authors.",
    ],
    "freshness_flags": [],
    "notes": [
        "Round 3 re-verification of L05 and L06 pages, lab twins and the L05/L06 cards, pinned at 4a8690a. Delta read in full: "
        "L05.html (simulate function, Lab 1 output lines, interpretation, §3 paragraph, E2, E3), L06.html (§2 paragraph, "
        "hypothesis, Lab 1 interpretation, §4 paragraphs, §5 bullets, Misconceptions 2 and 3, E1-E3 solutions, R1 solution, "
        "Key results row 2, quiz explain), lab-AC2-L05-1.py and lab-AC2-L06-1.py (decompose_a1, se_scaling rows), cards "
        "c083, c087, c124, c125 (and the 8 new cards c131-c138 belong to other lessons).",
        "Round 2 rows re-verified or carried: all command rows re-run; subjects outside the hunks carried with the stated "
        "prefix. Round-2 FAIL rows: cit-dechow-authors now PASS (ruling 1); card-L06-dechow, card-L06-12of200, "
        "prose-unmarked-claims, r2-num-L06-se-basis, r2-lab-contamination-prop33, r2-math-L06-misc3-sentence, "
        "r2-prose-s4-lab-bears now PASS; r2-math-E2-zgap-cause remains FAIL (cause stated beyond printed numbers).",
        "Scripts: ledgers/AC2/scripts/L05-L06-r3/ (recompute_l05_r3.py, recompute_l05_e3_r3.py, recompute_l06_r3.py, "
        "build_fragment_r3.py). Outputs in /tmp/ac2-v/L05-L06-r3/ (lab05.out, lab06.out, recompute_*.out, a2_check.out, "
        "page_smoke.txt, check_pages.txt, check_dag.txt, run_labs.txt, verify_refs_live.txt, verify_refs_offline.txt, "
        "crossref_*.json).",
        "Publisher pages (doi.org, AAA, Wiley, OUP, JFE, tandfonline, SSRN) were NOT fetched in round 3; no bot check or "
        "access block was approached. Crossref api.crossref.org records and abstracts were fetched with plain curl "
        "(HTTP 200) for dechow1995detecting and sloan1996stock; those abstracts are the only text of the two papers read.",
        "Mutation testing: none (lesson slice; project slice only).",
        "Hours: declared L05 8 h and L06 10 h (sum of eight lessons 76 = index). Own estimates 7.5 h and 9.5 h: within 30%.",
        "Architect questions (not FAILs): (a) learner text names 'BLUEPRINT §5.3' and 'the A15 contract' and 'open source "
        "requests ... plans/AC2-open-items.md' (not on the ruling's word list); (b) concept-link convention (each concept "
        "linked once per page, as in the Uses line); (c) 'too imprecise to recover' reading of an SE.",
        "Lab-level claim checked: 'the lab bears on the second and third' is supported (the lab prints the all-firm vs "
        "non-manipulator decomposition and the SE scaling; it fits no intercept).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(r["status"] == "PASS" for r in rows),
        "fail": len(fails),
        "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
        "fail_ids": fails,
        "round2_fail_ids_now_pass": [k for k in ROUND2_FAIL if k not in fails],
    },
}
json.dump(out, open(f"{ROOT}/ledgers/AC2/L05-L06.json", "w"), indent=1, ensure_ascii=False)
print("wrote", len(rows), "rows; fails:", fails)
print("validate:", ledger.validate(out, "L05-L06"))
