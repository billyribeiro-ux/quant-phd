"""Build ledgers/AC4/AC4-c.json for round 23 from the round-22 fragment (context) and this round's re-runs.

Rows re-run in round 23 get new evidence; every other PASS row is carried with the prefix required by the brief.
Usage: build_fragment_r23.py <checkout> <round22.json>
"""
import json
import sys

checkout, prev_path = sys.argv[1], sys.argv[2]
prev = json.load(open(prev_path, encoding="utf-8"))

CARRY_FILES = ("course/modules/AC/AC4/L05.html, course/modules/AC/AC4/L06.html, tests/labs/AC4/lab-AC4-L05-1.py, "
               "tests/labs/AC4/lab-AC4-L06-1.py and tools/ (git diff --quiet fd9a9b7 503d139)")
CARD_CARRY = ("course/modules/AC/AC4/cards.json changed only for AC4-c007, c020, c037, c089, c093, c095, c108, c113 "
              "and new c135 to c140 (python id-by-id compare fd9a9b7 vs 503d139); the cited card ids are unchanged")

RERUN = {
    "AC4-c-cmd-check-pages": "Round 23 (pin 503d139): .venv/bin/python tools/check_pages.py --all exit 0; output 'check_pages AC4: PASS' (ledgers/AC4/scripts/AC4-c-r23 run log in this round's scratch /tmp/AC4-v/c23).",
    "AC4-c-cmd-check-dag": "Round 23: .venv/bin/python tools/check_dag.py --all exit 0; output 'check_dag AC4: PASS'. Re-run because other AC4 lessons changed.",
    "AC4-c-cmd-check-projects": "Round 23: .venv/bin/python tools/check_projects.py --all exit 0; output 'check_projects AC4: PASS'.",
    "AC4-c-cmd-run-labs": "Round 23: .venv/bin/python tools/run_labs.py --unit AC4 exit 0; output 'run_labs AC4: PASS (10/10)'.",
    "AC4-c-twins-run": "Round 23: .venv/bin/python -I -W error on tests/labs/AC4/lab-AC4-L05-1.py and lab-AC4-L06-1.py: both exit 0, no stderr.",
    "AC4-c-page-smoke": "Round 23: .venv/bin/python tools/page_smoke.py --unit AC4 --pages L05.html L06.html exit 0; output 'page_smoke AC4: PASS'.",
    "AC4-c-lint-types-pytest": "Round 23: ruff check on both twins 'All checks passed!'; ruff format --check '2 files already formatted'; mypy --no-incremental 'Success: no issues found in 2 source files'; pytest -q tests/test_labs.py all dots, no failure lines (exit not captured past tail; the output has no F or E).",
    "AC4-c-citations": "Round 23: tools/verify_refs.py --offline 'offline integrity: 560 entries, 0 problems' exit 0; tools/verify_refs.py --unit AC4 'live re-verification of AC4: 2 of 560 entries, 0 problems' exit 0. Neither page cites a registry key.",
    "AC4-c-hours": "Round 23: index.html changed (line 49, outcome wording only; data-hours-lessons 50 and data-hours-project 20 unchanged). Lesson data-hours: L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6, L08 6; sum 50 equals data-hours-lessons 50. L05 data-hours 7 and L06 data-hours 6 unchanged. Arithmetic consistent.",
    "AC4-c-dag-concepts": "Round 23: check_dag AC4 PASS (see AC4-c-cmd-check-dag); L05/L06 pages byte-identical, so the defined and used concept locators (L05 line 49, 58, 87; L06 lines 52, 56, 62-68) are unchanged.",
    "AC4-c-cards-dup-scan": "Round 23 full duplicate scan of course/modules/AC/AC4/cards.json by ledgers/AC4/scripts/AC4-c-r23/cards_scan_r23.py: 140 cards, no duplicate ids, fronts or backs; 27 L05/L06 cards (AC4-c059 to c081, c110 to c112, c133). Round-22 evidence said 119 cards; the file had 134 at fd9a9b7 and has 140 now, so the earlier figure was a miscount and is corrected here. The changed cards are all in L01, L02, L03, L07 and L08.",
    "AC4-c-lab-L05-output": "Round 23: twin run under -I -W error exit 0; ledgers/AC4/scripts/AC4-c-r18/embed_and_expected_r18.py run with -I -W error: 'L05 embedded code equals twin: True' and 'L05 expected block equals run output: True'.",
    "AC4-c-lab-L06-output": "Round 23: twin run exit 0; embed_and_expected_r18.py: 'L06 embedded code equals twin: True' and 'L06 expected block equals run output: True'.",
    "AC4-c-r18-embed-check": "Round 23: embed_and_expected_r18.py run (exit 0): both embedded code blocks equal their twins and both expected blocks equal the run output.",
    "AC4-c-lab-mutants": "Round 23 rerun: ledgers/AC4/scripts/AC4-c-r20/run_all_mutants.py over every AC4-c mutant (r7, r8, r17, r18, r19, r20, r23); output in ledgers/AC4/scripts/AC4-c-r23/out/r23_all_mutants.out. Every student-error mutant is ERR or DIFF; the SAME files are alternatives or the out-of-scope r19_m05.",
    "AC4-c-lab-alt-impl": "Round 23 rerun: AC4-c-r7/alt01_mix_written_as_sum_minus_total.py exits 0 and every printed line equals the baseline except the two sales_price_variance_A and _B lines it does not print (DIFF in the run log; the grep-filtered diff of the other lines is 0 lines).",
    "AC4-c-L05-lab-mutants": "Round 23 rerun: AC4-c-r7 n04 and n05 are DIFF (exit 0, printed output differs from baseline) in ledgers/AC4/scripts/AC4-c-r23/out/r23_all_mutants.out (killed).",
    "AC4-c-mutants-new-r8": "Round 23 rerun of AC4-c-r8 s01-s05: s01 to s04 ERR (residual check fails); s05 DIFF (printed output differs); all killed in r23_all_mutants.out.",
    "AC4-c-alt-impl-r8": "Round 23 rerun of AC4-c-r8 alt01..alt05: all exit 0; each printed line equals the baseline except the sales_price_variance_A and _B lines, which these files do not print (checked with a grep-filtered diff, 0 lines). No alternative computes a wrong number.",
    "AC4-c-r17-ne-mutants": "Round 23 rerun of AC4-c-r17 ne01..ne07: ne01 and ne02 ERR (residual check); ne03 to ne07 DIFF (printed output differs). All seven are killed in r23_all_mutants.out.",
    "AC4-c-r17-alt-impl": "Round 23 rerun of AC4-c-r17 alt06..alt08: all exit 0. alt06 and alt08 are DIFF only because they omit the sales_price_variance_A and _B lines (grep-filtered diff 0 lines); alt07 SAME.",
    "AC4-c-r18-new-mutants": "Round 23 rerun of AC4-c-r18 r18_m01..m05: m01, m02, m03 ERR; m04 and m05 DIFF (r23_all_mutants.out). r18_m01 to m03 are the ERR set; m04 and m05 are DIFF.",
    "AC4-c-r18-equivalent-proof": "Round 23 rerun of r18_m06 (DIFF) and r17 ne06 (DIFF) and ne07 (DIFF): printed output differs from baseline, so these are not output-equivalent for the lab twin. The mathematical equivalence claimed in earlier rounds is not a finding for lab twins (architect ruling).",
    "AC4-c-r18-alt-impl-3": "Round 23 rerun of AC4-c-r18/alts: alt_r18_a and alt_r18_b exit 0 and differ from baseline only in the two omitted sales_price_variance lines (grep-filtered diff 0 lines); alt_r18_c_L05 SAME.",
    "AC4-c-r19-new-mutants": "Round 23 rerun of r19_m01..m04: m02 and m04 ERR; m01 and m03 DIFF (r23_all_mutants.out).",
    "AC4-c-r19-m05-decompose-only-survivor": "Round 23 rerun of r19_m05: SAME output (exit 0). The mutant changes only the decompose() budget units for sales price. Its printed sales_price_variance line still matches and no lesson sentence states that the lab checks the per-product breakdown, so it stays out of scope by the architect ruling (PASS, out of scope).",
    "AC4-c-r20-mutants-rerun": "Round 23 rerun: ledgers/AC4/scripts/AC4-c-r20/run_all_mutants.py output is identical line for line to ledgers/AC4/scripts/AC4-c-r20/out/r20_all_mutants.out (diff empty).",
    "AC4-c-r20-new-mutants": "Round 23 rerun: r20_m01 and r20_m03 ERR, r20_m02 DIFF (r23_all_mutants.out).",
    "AC4-c-r20-new-alts": "Round 23 rerun: alt_r20_a and alt_r20_b SAME; alt_r20_c SAME (r23_all_mutants.out).",
    "AC4-c-r20-verify-refs": "Round 23: tools/verify_refs.py --offline 560 entries, 0 problems; tools/verify_refs.py --unit AC4 2 of 560 entries, 0 problems (both exit 0).",
    "AC4-c-r20-lab-counts": "Round 23: both twins run under -I -W error exit 0 (stdout compared with the expected blocks by embed_and_expected_r18.py: True).",
    "AC4-c-cards-L05": "Round 23: cards AC4-c059 to c068 unchanged (per-id compare fd9a9b7 vs 503d139). Carried with the card-level subject byte-identical; see the full dup scan row.",
    "AC4-c-cards-L06": "Round 23: cards AC4-c069 to c081 and c110 to c112 unchanged (per-id compare); the full dup scan (AC4-c-cards-dup-scan) is re-run.",
}

NEW = [
    {"id": "AC4-c-r23-delta", "check": "Delta fd9a9b7..503d139 for this slice", "location": "course/modules/AC/AC4/L05.html; L06.html; tests/labs/AC4/lab-AC4-L05-1.py; lab-AC4-L06-1.py; tools/", "status": "PASS",
     "evidence": "git diff --quiet fd9a9b7 503d139 on these paths: no change (byte-identical). Changed files in the AC4 folder: index.html (hub outcome line 49), cards.json and L01, L02, L03, L07, L08. Hub and other-lesson hunks are outside slice c and were not verified against their lessons here; they belong to the other AC4 slices (noted in notes)."},
    {"id": "AC4-c-r23-cards-changed-ids", "check": "Changed card ids in cards.json this round", "location": "course/modules/AC/AC4/cards.json", "status": "PASS",
     "evidence": "Python id-by-id compare (fd9a9b7 vs 503d139): changed AC4-c007, c020, c037, c089, c093, c095, c108, c113; new AC4-c135 to c140. None of them is an L05 or L06 card (lessons L01, L02, L03, L07, L08)."},
    {"id": "AC4-c-r23-new-mutants", "check": "Three or more new student-error mutants of the L05 and L06 twins", "location": "ledgers/AC4/mutants/AC4-c-r23/r23_m01..m06", "status": "PASS",
     "evidence": "Six new student-error mutants written this round by ledgers/AC4/scripts/AC4-c-r23/make_r23_mutants.py: r23_m01 total contribution takes the fixed gap (ERR, residual 10000 cents); m02 sales price at budget units (DIFF, per-product lines differ, residual stays zero because the two per-product changes cancel); m03 mix base is budget units (ERR, residual -249000); m04 L05 fixed overhead flexes with units (DIFF); m05 mix sign reversed in the sum (ERR, residual 32000); m06 L05 actual revenue at budget price (DIFF). All six are killed."},
    {"id": "AC4-c-r23-alt-impl", "check": "Two new correct alternative implementations pass", "location": "ledgers/AC4/mutants/AC4-c-r23/alts/alt_r23_a_L06_mix_as_cm_sum_minus_average.py; alt_r23_b_L05_budget_totals_per_product.py", "status": "PASS",
     "evidence": "alt_r23_a computes the mix as sum CM_i q_a,i minus Q_a times CMbar_b (valid algebra, sum_i m_i CM_i = CMbar_b); alt_r23_b computes L05 budget totals per product. Both print exactly the baseline output (SAME) under -I -W error."},
    {"id": "AC4-c-r23-mutants-rerun", "check": "Every AC4-c mutant and alternative re-run", "location": "ledgers/AC4/scripts/AC4-c-r20/run_all_mutants.py; ledgers/AC4/scripts/AC4-c-r23/out/r23_all_mutants.out", "status": "PASS",
     "evidence": "run_all_mutants.py over r7, r8, r17, r18, r19, r20 and r23 (67 files): BASE L05 exit 0 17 lines, BASE L06 exit 0 16 lines; 31 DIFF, 28 ERR, 8 SAME. The 8 SAME are the alternatives alt07 (r17), alt_r18_c, alt_r20_a, alt_r20_b, alt_r20_c, alt_r23_a, alt_r23_b and the out-of-scope r19_m05. No student-error mutant survived."},
    {"id": "AC4-c-r23-cards-dup-scan-scope", "check": "Full card scan: lesson counts and banned words", "location": "course/modules/AC/AC4/cards.json; ledgers/AC4/scripts/AC4-c-r23/cards_scan_r23.py", "status": "PASS",
     "evidence": "Per lesson: L01 19, L02 20, L03 20, L04 15, L05 10, L06 17, L07 18, L08 21 (total 140). Words roughly, about, historically, typically, usually, ellipsis: hits in AC4-c033 (L03 'about that product') and AC4-c066 (L05 'no assumption about the cost function'); neither is a banned phrase. Ungraded cards are definitions and formulas (BUILDER_RULES 7 requires a grade only for graded results)."},
    {"id": "AC4-c-r23-embed-check", "check": "Embedded code and expected blocks equal the twins and run output", "location": "course/modules/AC/AC4/L05.html; L06.html; tests/labs/AC4/lab-AC4-L05-1.py; lab-AC4-L06-1.py", "status": "PASS",
     "evidence": "embed_and_expected_r18.py with -I -W error: L05 embedded code equals twin True, L05 expected equals run output True, L06 embedded True, L06 expected True."},
]

rows = []
for r in prev["rows"]:
    row = dict(r)
    rid = r["id"]
    if r["status"] != "PASS":
        raise SystemExit(f"unexpected non-PASS in round 22: {rid}")
    if rid in RERUN:
        row["evidence"] = RERUN[rid]
    elif rid in ("AC4-c-cards-c076", "AC4-c-L05-cards-verbatim-check", "AC4-c-cards-L05", "AC4-c-cards-L06",
                 "AC4-c-r17-card-c061", "AC4-c-r17-card-c063", "AC4-c-r17-card-c073", "AC4-c-r17-card-c133",
                 "AC4-c-r18-c074-scope"):
        row["evidence"] = "Carried from round 22 (" + CARD_CARRY + "): " + r["evidence"]
    else:
        row["evidence"] = "Carried from round 22 (" + CARRY_FILES + " byte-identical since the previous pin): " + r["evidence"]
    rows.append(row)
rows += NEW

frag = {
    "unit": "AC4",
    "slice": "AC4-c",
    "round": 23,
    "verifier": "independent Haiku verifier, slice AC4-c (L05, L06 and their lab twins), round 23; did not build AC4",
    "pin": "503d139",
    "base": "fd9a9b7",
    "previous_ledger": prev_path + " (pin fd9a9b7)",
    "checkout": checkout,
    "scratch": "/tmp/AC4-v/c23",
    "verified_at": "2026-10-28T14:00:00Z",
    "verdict": "PASS",
    "rows": rows,
    "mutants": prev["mutants"] + [
        {"id": "r23_m01", "description": "Round 23 student-error mutant: L06 total contribution takes the fixed gap (ERR)", "file": "ledgers/AC4/mutants/AC4-c-r23/r23_m01_L06_total_contribution_takes_fixed_gap.py"},
        {"id": "r23_m02", "description": "Round 23 student-error mutant: L06 sales price at budget units (DIFF)", "file": "ledgers/AC4/mutants/AC4-c-r23/r23_m02_L06_sales_price_at_budget_units.py"},
        {"id": "r23_m03", "description": "Round 23 student-error mutant: L06 mix base is budget units (ERR)", "file": "ledgers/AC4/mutants/AC4-c-r23/r23_m03_L06_mix_base_is_budget_units.py"},
        {"id": "r23_m04", "description": "Round 23 student-error mutant: L05 fixed overhead flexes with units (DIFF)", "file": "ledgers/AC4/mutants/AC4-c-r23/r23_m04_L05_fixed_overhead_flexes_with_units.py"},
        {"id": "r23_m05", "description": "Round 23 student-error mutant: L06 sales mix sign reversed (ERR)", "file": "ledgers/AC4/mutants/AC4-c-r23/r23_m05_L06_mix_sign_reversed_in_sum.py"},
        {"id": "r23_m06", "description": "Round 23 student-error mutant: L05 actual revenue at budget price (DIFF)", "file": "ledgers/AC4/mutants/AC4-c-r23/r23_m06_L05_actual_revenue_at_budget_price.py"},
        {"id": "alt_r23_a", "description": "Round 23 correct alternative: L06 mix as CM sum minus average (SAME)", "file": "ledgers/AC4/mutants/AC4-c-r23/alts/alt_r23_a_L06_mix_as_cm_sum_minus_average.py"},
        {"id": "alt_r23_b", "description": "Round 23 correct alternative: L05 budget totals per product (SAME)", "file": "ledgers/AC4/mutants/AC4-c-r23/alts/alt_r23_b_L05_budget_totals_per_product.py"},
    ],
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": [
        "Delta fd9a9b7..503d139 on this slice is nil for L05.html, L06.html, both twins and tools (git diff --quiet). Only AC4 cards.json and the AC4 hub index.html and L01, L02, L03, L07, L08 changed in the AC4 folder; none of those hunks is in slice c.",
        "Rows that cite cards.json for the L05 and L06 cards are carried only after a per-id compare: none of AC4-c059 to c081, c110 to c112, c133, c061, c063, c073, c074 or c076 changed.",
        "Hours: index.html changed one outcome line; the hub split (data-hours-lessons 50) equals the sum of the eight lesson data-hours values (50). Hours are design targets; no pace estimate is failed.",
        "Outside slice c, not verified this round: the changed hub outcome line (index.html line 49 'on two SIMULATED products'), the changed cards in L01, L02, L03, L07, L08, and the new AC4-c135 to c140. These belong to the other AC4 slices.",
        "Round-22 evidence row AC4-c-cards-dup-scan gave 119 cards; the correct count at fd9a9b7 is 134. Corrected in this round.",
        "Architect ruling applied: lab twin mutants that still exit 0 are recorded as out of scope unless a lesson claims the check; r19_m05 stays out of scope.",
    ],
    "could_not_check": prev["could_not_check"] + [
        "Round 23 did not re-read the full text of L05.html and L06.html line by line; the pages are byte-identical to the round-22 pin and the prior PASS rows carry, as the brief allows.",
        "Full-repo pytest and full mypy were not run in this round (scoped to tests/labs and mypy on the two twins).",
    ],
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = (f"PASS rows {n_pass}: {n_pass} PASS, 0 non-PASS. Round 23 delta on this slice is nil for the pages and twins; "
                   "cards.json changed outside L05/L06 and the card rows for L05/L06 were compared per id. All 67 AC4-c lab mutant "
                   "and alternative files re-run (31 DIFF, 28 ERR, 8 SAME: 7 alternatives and the out-of-scope r19_m05); six new student-error mutants killed, two new alternatives pass. Round-22 card count 119 corrected to 134 (fd9a9b7) and 140 (503d139).")
json.dump(frag, open(f"{checkout}/ledgers/AC4/AC4-c.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "pass", n_pass)
