"""Round 19 fragment builder for CF1 slice c (L05, L06, lab twins). Run with python -I from the checkout.

Carries round-18 PASS rows whose cited subject is unchanged since pin 7143726, re-verifies rows whose subject
changed or is a command row, and adds round-19 rows. Writes ledgers/CF1/CF1-c.json.
"""
import json
import re
import sys

PREV = "7143726"
CHANGED_L06_LINES = ("211", "327", "364", "366")
R18 = "/tmp/fanout-frags/CF1-c.round18.json"
SCRATCH = "/tmp/cf1-v/c19"
CK = "/tmp/verify19-CF1-c"

r18 = json.load(open(R18, encoding="utf-8"))

NEW = {}


def new(rid, status, evidence):
    NEW[rid] = (status, evidence)


# ---- command rows, re-run in this round -------------------------------------------------------
new("CF1-c-cmd-pin", "PASS",
    "git rev-parse HEAD = 51fa33616cf2a2ef40ec58634d40f67f78aa668c in /tmp/verify19-CF1-c (detached); "
    "git status: only untracked .venv symlink and ledgers/CF1/scripts/CF1-c-r19/.")
new("CF1-c-cmd-check_pages", "PASS",
    "tools/check_pages.py --all: 'check_pages CF1: PASS' (exit 0; output " + SCRATCH + "/check_pages.out).")
new("CF1-c-cmd-check_dag", "PASS",
    "tools/check_dag.py --all: 'check_dag CF1: PASS' (exit 0; " + SCRATCH + "/check_dag.out).")
new("CF1-c-cmd-run_labs", "PASS",
    "tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)' (exit 0; " + SCRATCH + "/run_labs.out).")
new("CF1-c-cmd-page_smoke", "PASS",
    "tools/page_smoke.py --unit CF1 --pages L05 L06: 'page_smoke modules/CF/CF1/L05.html: PASS', "
    "'page_smoke modules/CF/CF1/L06.html: PASS', 'page_smoke CF1: PASS' (exit 0; " + SCRATCH + "/smoke.out).")
new("CF1-c-cmd-ruff-mypy-labs", "PASS",
    "ruff check on the two twins: exit 0; ruff format --check on the two twins: exit 0; mypy --no-incremental: "
    "'Success: no issues found in 153 source files' (exit 0). ruff check . over the repository: 'All checks passed!' "
    "(exit 0). Repository-wide ruff format --check . reports one file, plans/M2-build-plan.md:193:19, outside "
    "slice c and recorded in the notes, not in this row.")
new("CF1-c-cmd-pytest-labs", "PASS",
    "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py: exit 0 (output " + SCRATCH + "/pytest.out).")
new("CF1-c-cmd-verify_refs", "PASS",
    "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (exit 0); "
    "tools/verify_refs.py --unit CF1: 'live re-verification of CF1: 2 of 560 entries, 0 problems' (exit 0).")
new("CF1-c-cmd-twin-vs-page", "PASS",
    "ledgers/CF1/scripts/CF1-c-r14/twin_vs_page.py /tmp/verify19-CF1-c under python -I: L05 and L06 'expected identical "
    "to twin output: True'; code identical ignoring one trailing newline: True for both (strict: False for both, the "
    "same trailing-newline difference; output " + SCRATCH + "/twin_vs_page.out).")
new("CF1-c-twin-freshness", "PASS",
    "git diff --quiet 7143726 51fa336 -- tests/labs/CF1 (unchanged); the page code blocks match the twins per "
    "CF1-c-cmd-twin-vs-page.")
new("CF1-c-lab-L05-1-run", "PASS",
    "python -I -W error tests/labs/CF1/lab-CF1-L05-1.py: exit 0; output reproduces the embedded L05 lab output "
    "(run_labs PASS 9/9).")
new("CF1-c-lab-L06-1-run", "PASS",
    "python -I -W error tests/labs/CF1/lab-CF1-L06-1.py: exit 0 (" + SCRATCH + "/lab-CF1-L06-1.py.out); printed lines "
    "match the output block ending at L06.html line 205 (run_labs PASS).")
new("CF1-c-cmd-mutants-na-r13", "PASS",
    "ls ledgers/CF1/mutants | wc -l = 175 (project-grader mutants, slice d). Lab-twin mutants are under "
    "ledgers/CF1/scripts/CF1-c-r18/mutants and CF1-c-r17/mutants, re-run in round 19 (see CF1-c-r19-mutants-lab-rerun).")
new("CF1-c-r17-mutants-project-grader", "PASS",
    "Re-run in round 19: tools/mutate_graders.py --unit CF1 --seeds 0-9: 'mutate_graders CF1: PASS (167/167 killed)', "
    "0 survivors, exit 0 (" + SCRATCH + "/mutate_r19.out). The grader changed in this delta (test_project.py +43 lines); "
    "the count rose from 154 (round 18) to 167 because the mutant directory gained files. Project-grader mutants are "
    "slice d's; recorded here as carried verification.")
new("CF1-c-cards-duplicates", "PASS",
    "python -I scan of course/modules/CF/CF1/cards.json: 109 cards, no duplicate ids, no duplicate fronts (round 19).")
new("CF1-c-cards-dupes-r12-cross", "PASS",
    "cards.json all 109 cards: no duplicate id and no duplicate front (round-19 scan, same run as CF1-c-cards-duplicates).")
new("CF1-c-hours", "PASS",
    "grep data-hours: L05.html and L06.html data-hours=\"8\" (both unchanged in the delta); index.html data-hours-lessons=\"48\" "
    "unchanged (git diff 7143726 51fa336 for index.html is empty).")
new("CF1-c-concepts", "PASS",
    "check_dag CF1: PASS; L06.html line 63 md5 c2f39e1eb7ef7b91990b72adbb97ace9, identical at 7143726 and 51fa336.")
new("CF1-c-struct-L06", "PASS",
    "check_pages CF1: PASS; L06.html is 465 lines; the changed lines in this delta are 211, 327, 364 and 366 (git diff 7143726 "
    "51fa336), each re-verified below; page_smoke L06: PASS.")
new("CF1-c-banned-scan", "PASS",
    "ledgers/CF1/scripts/CF1-c-r16/banned_scan_r16.py: exit 0 on L05.html and L06.html learner text (" + SCRATCH + "/banned.out). "
    "The scan does not list the word 'twin'; see CF1-c-r19-L06-line211-twin-term.")
new("CF1-c-prose-process-path", "FAIL",
    "L06.html line 211 (new sentence this delta) says 'a re-run of the twin's code': 'twin' is the repository's build "
    "term for tests/labs twins (BUILDER_RULES.md line 285) and appears in no learner-facing text elsewhere in L01-L06 "
    "(grep -c -i twin = 0 for L01-L04; L05 and L06 only this sentence). The banned-scan process-word list (build, round, "
    "verifier, REQUESTS, unit report, agent) does not include it, so the scan passes, but the sentence is process "
    "vocabulary. See CF1-c-r19-L06-line211-twin-term.")
new("CF1-c-r19-L06-line211-twin-term", "FAIL",
    "L06.html line 211: 'Calling the lab's own quantile function on the same 50000 draws, without the printing step (a re-run "
    "of the twin's code, not a line of its output), gives 14896.623057 and 143406.126569 cents'. The learner has no twin; "
    "the lab is the code block on the page (from line 112). The numbers and the re-run claim are correct (see "
    "CF1-c-num-L06-s3-quantile-unrounded), so only the wording fails.")
new("CF1-c-num-L06-s3-quantile-unrounded", "PASS",
    "L06.html line 211 (changed). Own recomputation (ledgers/CF1/scripts/CF1-c-r19/recompute_l06.py, python -I): "
    "q10 14896.623057, q90 143406.126569 (matches), difference 128509.503511 which rounds to 128509.50; printed-difference "
    "gap 128509.51 - 128509.503511 = 0.006489, i.e. 0.0065. The lab computes quantiles unrounded and prints two decimals "
    "(tests/labs/CF1/lab-CF1-L06-1.py quantile() at lines 43-46, printed at line 76), so the unrounded values are not in the output "
    "(" + SCRATCH + "/lab-CF1-L06-1.py.out). Process wording is the separate FAIL row.")
new("CF1-c-num-L06-E3-width", "PASS",
    "L06.html E3 solution (line 327, changed): 143406.13 - 14896.62 = 128509.51 cents = 1285.10 currency units (1285.0951 rounds to "
    "1285.10); unrounded 128509.5035 cents from the re-run (recomputed 128509.503511, rounds to 128509.50 and 1285.10 currency "
    "units from 1285.095035).")
new("CF1-c-grade-L06", "PASS",
    "L06.html key-results table (lines 361-368, changed rows 364 and 366): 'Proved in §2' rows for Propositions 2.1 and 2.3 are "
    "grade T; the new hypotheses 'identically distributed ... variance sigma^2' (Prop 2.1, line 71) and 'common mean mu and common "
    "variance sigma^2' (Prop 2.3, line 96) match the statements. Lab rows remain C. Grades agree with BLUEPRINT section 3 (T = proved).")
new("CF1-c-r18-E1-E2-arithmetic", "PASS",
    "Re-computed in round 19: E1 ratio 5464.72/4400.22 = 1.24192 (page 1.2419); two-sided 2(1-Phi(1.2419)) = 0.21427 (page 0.2143); "
    "E2 band 0.0552 +/- 1.96*0.0010 = 0.05324 to 0.05716 (page 0.0532 to 0.0572); E3 width 1285.10. Lab 1 SE ratio "
    "4400.22/221.01 = 19.91 (page 19.9) and sqrt(500) = 22.36 (page 22.4). Matches L06.html lines 313, 320, 327, 206.")
new("CF1-c-cards-L05", "PASS",
    "cards.json L05 cards CF1-c062..c074, c096..c098, c102, c109 re-checked in round 19; the only changed L05 card is CF1-c096 "
    "(see CF1-c-r17-cards-c096-grade); the others are byte-identical (git diff 7143726 51fa336 shows one changed card).")
new("CF1-c-r17-cards-c096-formula", "PASS",
    "cards.json CF1-c096 back: '(tau_S - 1) + (-CUM_(tau_S - 1)) / C_(tau_S) (Definition 1.1)' vs L05.html line 60 (Definition 1.1 "
    "display: (tau_S - 1) + (-CUM_(tau_S-1))/C_(tau_S)) and line 58 definition; same formula. Front 'How is the fractional simple payback computed?' matches.")
new("CF1-c-r17-cards-c096-grade", "PASS",
    "cards.json CF1-c096: grade 'C', basis 'convention, Definition 1.1 (linear interpolation inside the payback year)'. L05.html "
    "line 62 says 'It is a convention, and it is not a finding.' The module's own grade legend gives C to 'single study or convention' "
    "(L01.html line 46) and its key-results table grades the decision rule C as 'A convention stated in Section 1' (L01.html line 468). "
    "BLUEPRINT section 3 has no separate convention grade. Grade C is consistent with the unit's use. The prior T was an over-grade.")
new("CF1-c-r18-grade-definition-T", "PASS",
    "Round-19 re-verification (subject changed: CF1-c096 is now C, not T). A convention is not a theorem, so T (BLUEPRINT section 3: "
    "'proved on the page') is an over-grade; C matches the legend used in L01 (line 46). CF1-c062 (T, Definition 1.1) is a definition "
    "with a proof-free formula; its grade was not re-examined here (its subject is unchanged; carried by CF1-c-cards-L05 for the L05 set).")
new("CF1-c-r17-cards-delta", "PASS",
    "git diff -U0 7143726 51fa336 -- course/modules/CF/CF1/cards.json: one hunk (line 773-774): grade T -> C and basis changed for CF1-c096. "
    "No other card changed in this delta.")
new("CF1-c-delta-L06-line211-given-model", "PASS",
    "L06.html line 211: grep -c 'given the model' = 0 (removed in this delta, as stated in the earlier row).")
new("CF1-c-delta-cross-slice-notes", "UNVERIFIABLE",
    "Count claim verified: project.html now says 'collects 154 checks' (line 192); copying grader/test_project.py as capbudget.py "
    "(reference.py) plus instance.py into scratch: 154 tests collected (" + SCRATCH + "/collect_count.out). Not verified by this slice: "
    "the project.html C2 annotation sentence (changed line, 'each flow from year 1 includes the shield') and the grader's new "
    "tests (slice d's to check). Cards CF1-c054, c056, c058, c060, c094 (L04) are byte-identical in this delta.")

# ---- round-19 new rows ------------------------------------------------------------------------------
new("CF1-c-r19-delta", "PASS",
    "git diff --stat 7143726 51fa336 for slice c inputs: L06.html (8 lines, hunks at 211, 327, 364, 366), cards.json (1 card CF1-c096), "
    "project.html and grader (slice d), curriculum/01-foundations.yaml and curriculum.json (CS2 prereq M1, not CF1). L05.html, "
    "tests/labs/CF1, index.html, references/, tools/, notation/ and atlas/ are unchanged (git diff --quiet).")
new("CF1-c-r19-mutants-lab-rerun", "PASS",
    "All 17 lab-twin mutants (ledgers/CF1/scripts/CF1-c-r17/mutants: c17_L06_01..05; CF1-c-r18/mutants: r18_L05_01..04, "
    "r18_L06_06..10, alt_r18_a..c) re-run under python -I -W error (" + SCRATCH + "/mut/). Killed (output differs or exit 1): "
    "c17_L06_01, 02, 03, 05; r18_L05_01..04 (03 exits 1, ZeroDivisionError); r18_L06_06..09. Equivalent on displayed output: "
    "c17_L06_04 (identical, zero draws: 0 exact-zero NPVs, zero_check.out) and r18_L06_10 (SE 0.001021 at n and n-1 both print 0.0010; "
    "identical output). Alternatives alt_r18_a..c identical to the correct twin (exit 0). Lab-twin mutants are out of scope for "
    "grading (architect ruling): no lab sentence claims an assertion.")
new("CF1-c-r19-alt-impls", "PASS",
    "Three alternative correct implementations (plain sum instead of fsum; fmean for mean; direct power discount) run under "
    "python -I -W error: output identical to the correct L06 twin (" + SCRATCH + "/mut/alt_r18_*.out).")
new("CF1-c-r19-recompute-L06", "PASS",
    "ledgers/CF1/scripts/CF1-c-r19/recompute_l06.py (python -I): closed forms 79078.68 and 49379.84; sample sd ratio 1.0008; "
    "share 0.0552 with SE 0.0010 (0.001021); z at n=50000 0.625; quantiles, width and gap as in CF1-c-num-L06-s3-quantile-unrounded.")
new("CF1-c-r19-prop-statements-unchanged", "PASS",
    "L06.html Proposition 2.1 (line 71) and Proposition 2.3 (line 96) statements are unchanged in this delta; only the key-results "
    "rows at 364 and 366 restate them, and their hypotheses now match the statements (see CF1-c-grade-L06).")
new("CF1-c-r19-E1-prob-scope", "PASS",
    "L06.html E1 solution (line 313): 'Under the normal reading of Remark 2.4, which this lesson does not test' precedes the "
    "probability, and Remark 2.4 (line 106) says the normal reading is not proved (unchanged).")
new("CF1-c-r19-coverage-note", "PASS",
    "Scope of round 19: slice c inputs checked by delta; everything in the delta re-verified; unchanged subjects carried with the "
    "round-18 origin; command rows re-run. Not checked: alternative implementations of the project grader (slice d).")

NEW["CF1-c-cards-L05-other"] = ("PASS",
    "cards.json: CF1-c062 to c067, c068, c069 to c074, c097, c098 (L05) are byte-identical in this delta (git diff 7143726 51fa336 "
    "changes only CF1-c096). CF1-c068 back ('2.750 years, for SIMULATED flows ... does not depend on the 10 per cent rate') matches L05.html "
    "line 70 and the lab output (lab-CF1-L05-1 prints simple_payback 2.750 at the rate 0.1 run).")
NEW["CF1-c-r16-L06-line66-share-se-binomial"] = ("PASS",
    "L06.html line 66 (unchanged) and Section 3 sentence at line 211 (changed paragraph; the share sentence is unchanged): "
    "'0.0552, with a standard error of 0.0010 from the binomial formula'. Recomputed: sqrt(0.055220*(1-0.055220)/50000) = 0.001021 "
    "(page 0.0010); lab-CF1-L06-1.py lines 78-79 compute and print 'share_npv_below_zero 0.0552 se 0.0010' (" + SCRATCH + "/lab-CF1-L06-1.py.out).")

# ---- carry rules ----------------------------------------------------------------------------------
RERUN_IDS = set(NEW)
out_rows = []
seen = set()
problems = []
for row in r18["rows"]:
    rid = row["id"]
    seen.add(rid)
    if rid in NEW:
        status, ev = NEW[rid]
        out_rows.append({"id": rid, "check": row["check"], "location": row["location"], "status": status, "evidence": ev})
        continue
    loc = row["location"]
    touched = any(re.search(r"(?<![0-9])%s(?![0-9])" % ln, loc) for ln in CHANGED_L06_LINES) or "c096" in loc
    if row["status"] != "PASS":
        problems.append(rid)
        out_rows.append({"id": rid, "check": row["check"], "location": loc, "status": "UNVERIFIABLE",
                         "evidence": "Not re-verified in round 19; previous non-PASS row. " + row["evidence"]})
        continue
    if touched:
        problems.append(rid)
    prefix = ("Carried from round 18 (cited subject byte-identical since the previous pin %s; the changed hunks in this delta are "
              "L06.html lines 211, 327, 364, 366 and cards.json entry CF1-c096 only): " % PREV)
    out_rows.append({"id": rid, "check": row["check"], "location": loc, "status": "PASS", "evidence": prefix + row["evidence"]})

for rid in NEW:
    if rid not in seen:
        out_rows.append({"id": rid, "check": "new", "location": "round 19", "status": NEW[rid][0], "evidence": NEW[rid][1]})

print("touched carried rows (must be empty):", problems)
print("rows", len(out_rows))
json.dump({"row_ids": [r["id"] for r in out_rows]}, open(SCRATCH + "/row_ids.json", "w"))
json.dump(out_rows, open(SCRATCH + "/rows_draft.json", "w"), indent=1)

# ---- fragment writer ----------------------------------------------------------------------------
FIX = {
    "CF1-c-prose-process-path": "Remove the word 'twin' from L06.html line 211 (see CF1-c-r19-L06-line211-twin-term); the scan list is not the defect.",
    "CF1-c-r19-L06-line211-twin-term": "In L06.html line 211 replace \"a re-run of the twin's code\" with \"a re-run of the code of Lab 1, with the printing step left out\"; change nothing else in the sentence.",
    "CF1-c-delta-cross-slice-notes": "Slice d verifier to check the project.html C2 annotation sentence (changed line) and the grader's new tests; the count 154 is verified here.",
}
DEFAULT_CHECK = {"num": "2.2-numbers", "cards": "2.7-cards", "cmd": "2.5-labs", "lab": "2.5-labs", "mut": "2.5-labs",
                 "grade": "2.3-grades", "math": "2.4-math", "prop": "2.4-math", "E1": "2.4-math", "delta": "2.9-structure"}
for r in out_rows:
    if r["id"] in FIX:
        r["fix"] = FIX[r["id"]]
    if r["check"] == "new":
        key = next((k for k in DEFAULT_CHECK if k in r["id"]), None)
        r["check"] = DEFAULT_CHECK.get(key, "2.9-structure")
    if r["status"] != "PASS" and "fix" not in r:
        r["fix"] = "Re-verify this row in a later round."
mutants = [
    {"id": "c17_L06_01_population_sd_for_se", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_01_population_sd_for_se.py",
     "description": "Student uses the population SD (pstdev) for the standard error of the mean instead of the sample SD; Definition 1.2 requires the sample SD.",
     "killed_by": "lab output: se_cents 4400.22 becomes 4378.16 at n = 100 (re-run round 19); the page quotes 4400.22 (L06.html line 206)"},
    {"id": "c17_L06_02_quantile_rank_floor_plus_one", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_02_quantile_rank_floor_plus_one.py",
     "description": "Quantile rank taken as floor(p n) + 1 instead of ceil(p n); Definition 1.2 gives the nearest-rank rule.",
     "killed_by": "lab output: quantile_10_npv_cents 14896.62 becomes 14898.90 (re-run round 19)"},
    {"id": "c17_L06_03_discount_exponent_off_by_one", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_03_discount_exponent_off_by_one.py",
     "description": "Discount exponent off by one year in the simulated NPV.",
     "killed_by": "lab output: n 100 mean_npv_cents 122997.73 (re-run round 19); the page quotes 84543.40"},
    {"id": "c17_L06_05_se_divides_by_n_minus_one", "file": "ledgers/CF1/scripts/CF1-c-r17/mutants/c17_L06_05_se_divides_by_n_minus_one.py",
     "description": "Standard error divides the sample SD by sqrt(n - 1) instead of sqrt(n).",
     "killed_by": "lab output: se_cents 4400.22 becomes 4422.38 at n = 100 (re-run round 19)"},
    {"id": "r18_L06_06_quantile_zero_based_index", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L06_06_quantile_zero_based_index.py",
     "description": "Quantile read at a zero-based index, one place too low.",
     "killed_by": "lab output: quantile_10_npv_cents 14898.90 (re-run round 19); the page quotes 14896.62"},
    {"id": "r18_L06_07_receipt_range_excludes_high", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L06_07_receipt_range_excludes_high.py",
     "description": "Receipts drawn from LOW to HIGH - 1, so the top of the range is never drawn.",
     "killed_by": "lab output: n 10000 mean 79565.55 and n 50000 sd 49580.53 (re-run round 19); the page quotes 79216.82"},
    {"id": "r18_L06_08_expected_uses_low_plus_high", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L06_08_expected_uses_low_plus_high.py",
     "description": "Closed-form expected NPV uses low plus high instead of the mean receipt.",
     "killed_by": "lab output: expected_npv_cents_closed_form 458157.35 (re-run round 19); the page quotes 79078.68"},
    {"id": "r18_L06_09_quantile_uses_round_not_ceil", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L06_09_quantile_uses_round_not_ceil.py",
     "description": "Quantile rank rounds p n instead of taking the ceiling.",
     "killed_by": "lab output: quantile_90_npv_cents 143412.00 (re-run round 19); the page quotes 143406.13"},
    {"id": "r18_L05_01_tail_varies_year4", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L05_01_tail_varies_year4.py",
     "description": "Lab tail draws vary year 4 as well as years 5 and 6, which the lab's stated design excludes.",
     "killed_by": "lab output: distinct_discounted_payback 990 (re-run round 19); the page says years 5 and 6 only"},
    {"id": "r18_L05_02_discount_exponent_minus_one", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L05_02_discount_exponent_minus_one.py",
     "description": "Discount exponent t - 1 in the NPV of Lab 1.",
     "killed_by": "lab output: project A npv_cents 318304.14 (re-run round 19); the page quotes 289367.40"},
    {"id": "r18_L05_03_fraction_over_cumulative", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L05_03_fraction_over_cumulative.py",
     "description": "Fractional payback divides by the cumulative flow instead of the year's flow.",
     "killed_by": "lab run exits 1 with ZeroDivisionError (re-run round 19); no output produced"},
    {"id": "r18_L05_04_npv_uses_simple_sum", "file": "ledgers/CF1/scripts/CF1-c-r18/mutants/r18_L05_04_npv_uses_simple_sum.py",
     "description": "NPV computed from undiscounted sums.",
     "killed_by": "lab output: project A npv_cents -300000.00 (re-run round 19); the page quotes 289367.40"},
]
frag = {
    "unit": "CF1",
    "slice": "CF1-c",
    "round": 19,
    "verifier": "independent verifier (Haiku), round 19, slice c (L05, L06, lab twins)",
    "pin": "51fa33616cf2a2ef40ec58634d40f67f78aa668c",
    "base": "7143726a21ba709ef3e7c54375338021df2dfc01 (round 18 pin; previous rows carried only where the cited subject is byte-identical)",
    "checkout": CK,
    "scratch": SCRATCH,
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": out_rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since 7143726 for slice c: L06.html lines 211, 327, 364 and 366 (four pairs of changed lines) and cards.json entry CF1-c096 (grade T -> C, basis convention). L05.html, tests/labs/CF1, references, tools, notation, atlas, index.html are byte-identical.",
        "The only FAIL is wording: L06.html line 211 uses the build term 'twin' in learner text. Its numbers, the re-run claim and the 0.0065-cent gap are verified (CF1-c-num-L06-s3-quantile-unrounded).",
        "Card CF1-c096 grade C with basis 'convention' is accepted: L01.html line 46 legend ('single study or convention') and L01.html line 468 use C for conventions; BLUEPRINT section 3 has no convention grade.",
        "Equivalent lab-twin mutants (not in the mutants list): c17_L06_04 and r18_L06_10, identical output on seed 6 (proof rows in CF1-c-r19-mutants-lab-rerun).",
        "Alternative implementations (r18 alts a, b, c) produce identical output: the lab checks are not over-constrained for these.",
        "Repository-wide 'ruff format --check .' reports plans/M2-build-plan.md:193:19 (outside slice c; not a CF1 row). ruff check . passes.",
        "The project grader (slice d) collects 154 tests with reference.py copied as capbudget.py and instance.py alongside; the mutation run gives 167/167 killed. project.html's C2 annotation sentence is slice d's to check.",
        "Hours not re-estimated (architect ruling): data-hours=8 on L05 and L06 unchanged.",
    ],
    "summary": "Slice c round 19: verdict FAIL on one wording row (L06.html line 211 'twin'). Numbers in the changed L06 paragraphs, E1-E3, the key-results rows, the card CF1-c096 grade and every command row were re-run or recomputed and pass. Lab twins: 17 mutants and 3 alternatives re-run; 2 equivalent on displayed output; no survivors that a lesson sentence claims to detect.",
}
json.dump(frag, open(CK + "/ledgers/CF1/CF1-c.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote fragment", len(out_rows), "rows")
