import json, sys
prev = json.load(open("/tmp/fanout-frags/CF1-b.round16.json"))
PIN_PREV = "2c8162b"
L03 = "course/modules/CF/CF1/L03.html"
L04 = "course/modules/CF/CF1/L04.html"
S = "ledgers/CF1/scripts/CF1-b-r17/"
rerun = {  # row id -> (check, location, evidence) for rows re-run or re-verified this round
 "CF1-b-cmd-check-pages": ("2.9-structure", "tools/check_pages.py --all",
   "Ran .venv/bin/python tools/check_pages.py --all on pin fefbf8b: 'check_pages CF1: PASS' (also AC1, AC2, AC4, AP1 PASS)."),
 "CF1-b-cmd-check-dag": ("DAG/concepts", "tools/check_dag.py --all",
   "Ran .venv/bin/python tools/check_dag.py --all: 'check_dag CF1: PASS' (and AC1, AC2, AC4, AP1 PASS)."),
 "CF1-b-cmd-run-labs": ("2.5-labs", "tools/run_labs.py --unit CF1",
   "Ran .venv/bin/python tools/run_labs.py --unit CF1: 'run_labs CF1: PASS (9/9)'."),
 "CF1-b-lab-twin-direct": ("2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py, tests/labs/CF1/lab-CF1-L04-1.py",
   "Ran .venv/bin/python -I -W error on both twins: exit 0 each (outputs in ledgers/CF1/scripts/CF1-b-r17/l03.out, l04.out). Outputs compared with the page expected blocks by " + S + "compare_expected.py: L03 24 lines IDENTICAL, L04 29 lines IDENTICAL."),
 "CF1-b-lab-twin-lint": ("2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py, tests/labs/CF1/lab-CF1-L04-1.py",
   "ruff check and ruff format --check on both twins: 'All checks passed!', '2 files already formatted'; mypy --no-incremental on both: 'Success: no issues found in 2 source files'."),
 "CF1-b-lab-L03-1": ("2.5-labs", L03 + " l.122-126, l.123 hypothesis, l.242 interpretation; tests/labs/CF1/lab-CF1-L03-1.py",
   "Hypothesis (l.123): outlay 1,000,000 USD and five inflows 300,000 USD (lab REAL_FLOWS = -100_000_000 and five 30_000_000 cents: matches); real rate 0.06, inflation 0.03 (REAL_RATE, INFLATION); expected nominal rate 0.0918 (printed 0.091800); 12-case grid (INFLATION_GRID 4 x REAL_RATE_GRID 3 = 12, printed 'grid of 12 cases'); no random numbers (no random import). Every printed claim in the hypothesis is printed by the run. Output identical to page block."),
 "CF1-b-lab-L04-1": ("2.5-labs", L04 + " l.143-145, l.146-299 (lab), l.299-300 interpretation; tests/labs/CF1/lab-CF1-L04-1.py",
   "Hypothesis (l.145): two sign changes at 10 and 20 per cent (printed 'sign changes ... 2', roots 0.100000, 0.200000); scan from -0.5 to 1.0 step 0.0001 (GRID_LOW, GRID_HIGH, GRID_STEP); NPV at 5 per cent negative (printed -680.27); A higher IRR, B higher NPV at 10 per cent (printed); crossover 0.200000 (printed). Interpretation l.300: 'over six test rates' = six rates in closed-form gap tuple (-0.4, 0.0, 0.05, 0.15, 0.5, 2.0); gap 0.000000 printed. All consistent with output."),
 "CF1-b-lab-L03-E2-claim": ("2.5-labs", L03 + " E2 solution (l.339-342)",
   "Lab copy with INFLATION = 0.00 (" + S + "e2_e3_claims.py): mixed-minus-real prints '0.00' and the table row 0.00 prints 0.00; nominal flows equal real flows; mixed NPV at nominal rate also 263709.14 USD. Solution claims hold."),
 "CF1-b-lab-L03-E3-claim": ("2.5-labs", L03 + " E3 solution (l.346-348)",
   "Lab copy with REAL_RATE = 0.10 (" + S + "e2_e3_claims.py): nominal rate printed 0.133000 (= 1.10 x 1.03 - 1); largest consistency gap 0.000000 printed; real NPV becomes 137236.03 USD (changed, as the E3 solution says the student should check)."),
 "CF1-b-numbers-L03": ("2.2-numbers", L03 + " Example 1.4 (l.79), Example 2.5 (l.118), Sec 3 (l.248), misconceptions (l.257-269), M1-M3 (l.282-298), P3 (l.323), E1 (l.332-334), E3 (l.346-348), R2 (l.366), R3 (l.373), key results (l.385-391)",
   "Recomputed with " + S + "recompute_numbers.py (independent of the page): nominal 0.0918; mixed-minus-real USD at inflation 0, 0.01, 0.03, 0.05 = 0.00, 36913.22, 113637.49, 194368.27 (matches Lab 1 output); 113637.49/263709.14 = 0.43092 (43.1 per cent); E1 194368.27/263709.14 = 0.73706 (73.7); 36913.22 -> 0.13998 (14.0); Example 2.5 PV 257.7097 and real flows 97.0874, 94.2596, 91.5142, real rate 0.048544; P3 sqrt(0.005) = 0.070711; R2 ratio 2.06; R3 b = 1.06/2.03 = 0.522167 gives zero error (1.7e-17); M1 0.066; M2 1061.208; M3 0.057692; section 3 two-line 0.07625, implied inflation 0.025. All match the page."),
 "CF1-b-numbers-L04": ("2.2-numbers", L04 + " Example 3.2 (l.101-103), Prop 3.3 (l.109-110), Example 4.2 (l.135), Remark 5.1 (l.307), R1-R3 (l.424, l.431, l.436-438), misconceptions (l.322-334), E2 (l.406), E3 (l.413), M2 (l.356), quiz (l.474-535)",
   "Recomputed with " + S + "recompute_numbers.py: P NPV at 0,5,10,15,20,25,30 per cent = -2000.00, -680.27, 0, 189.04, 0, -480.00, -1183.43 (matches printed profile); closed roots 0.1, 0.2; Example 4.2 NPVs 18181.82/27272.73 at 10 per cent, 8333.33 each at 20 per cent; E2 A'=(-100000,+120000): IRR_A 20 per cent, NPV at 10 per cent 9090.91, at 35 per cent -11111.11 (A) and -14814.81 (B); crossover 0.30; R1 NPV at 10 per cent 0.322314; R2 147.93 and 81.82, IRR_A 0.732051; R3 FV 250.00 at 15 per cent and -750.00 at 5 per cent; Remark 5.1 FV at 20 per cent = 0; M2 IRR 13.07; M1 0.21. All match."),
 "CF1-b-r5-recompute-delta": ("2.2-numbers", S + "recompute_numbers.py (the round-5/6 scripts are absent from this checkout; this row is re-run with the round-17 script)",
   "The round-6 scripts named by the previous row are absent; the same numbers were recomputed this round with " + S + "recompute_numbers.py (L03 and L04 sections, output above). Only numbers of the L03 and L04 pages are covered; the other pages of CF1 are out of this slice."),
 "CF1-b-cards-L04-one-sign-change": ("2.7-cards", "course/modules/CF/CF1/cards.json CF1-c051, CF1-c052, CF1-c058 against " + L04 + " Theorem 2.1 (l.79), Corollary 2.2 (l.85-86)",
   "CF1-c051 (front and back changed): front asks the count of IRRs for outlay plus non-negative inflows, not all zero; back 'Exactly one ... strictly decreasing (Theorem 2.1)' matches l.79. CF1-c052 unchanged: matches Corollary 2.2 l.86. CF1-c058 (back changed): 'False in general' ... 'two IRRs, 10 and 20 per cent' and NPV at 5 per cent -680.27 (Prop 3.3 and lab output l.274); matches l.322 misconception 1."),
 "CF1-b-cards-L03-L04-other-29": ("2.7-cards", "course/modules/CF/CF1/cards.json: every L03 and L04 card (40 cards: c033-c061, c088, c091-c095, c103, c105-c108)",
   "Per-card comparison of " + S + "cards_prev.json (2c8162b) and cards_new.json (fefbf8b). Changed L03/L04 cards re-read against the lesson: c036, c042, c051, c053, c054, c056, c058, c060, c094 (changed); c103, c105, c106, c107, c108 (new). Each checked against its lesson line in this round's rows CF1-b-r17-cards-L03-changed and CF1-b-r17-cards-L04-changed. Unchanged cards c033-c035, c037-c041, c043-c050, c052, c055, c057, c059, c061, c088, c091-c093, c095 carried: their card text is byte-identical in the JSON."),
 "CF1-b-cards-duplicate-scan": ("2.7-cards", "course/modules/CF/CF1/cards.json",
   "" + S + "card_scan.py: 109 cards, no duplicate id, no duplicate normalised front; every 'Theorem/Definition/Example/Remark/Proposition/Corollary/Problem/Lab 1' label in the basis and back of the 40 L03/L04 cards occurs in its lesson page."),
 "CF1-b-hours-L03-L04": ("hours", L03 + " l.2; " + L04 + " l.2; index.html (CF1) hours split and card text",
   "data-hours=8 on L03 and L04 (l.2 of each), and on L01, L02, L05, L06 (line 2 of each). index.html data-hours-lessons=48, data-hours-project=12, eyebrow '60 hours', '48 h lessons · 12 h project (20.0% of the 60 module hours)'; 6 x 8 = 48; 48 + 12 = 60; 12/60 = 20.0%. Consistent, no arithmetic inconsistency."),
 "CF1-b-r6-mutation-scope": ("2.5-labs", "ledgers/CF1/mutants/CF1-b-r17/ (lab-twin mutants) and ledgers/CF1/scripts/CF1-b-r17/run_mutants.py",
   "Slice b is a lesson slice (L03, L04 and their twins); the project-grader mutant rule does not apply to it. This round ran 7 student-error mutants of the lab twins plus an unmodified control (mutants list in this fragment): 5 killed, 2 survivors each explained (grid endpoint, t >= 0 term): see the rows CF1-b-r17-mutant-grid-end and CF1-b-r17-mutant-t0-identity. No grader in this slice."),
 "CF1-b-r6-verify-refs": ("2.1-citations", "tools/verify_refs.py --unit CF1; tools/verify_refs.py --offline",
   "Ran .venv/bin/python tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (rc 0). Ran tools/verify_refs.py --unit CF1: 'live re-verification of CF1: 2 of 560 entries, 0 problems' (rc 0). L03 and L04 cite no registry key (l.476 and l.542 are empty ol data-references), so no publisher or SEC host is contacted by this slice."),
 "CF1-b-r6-page-smoke": ("2.5-labs", "tools/page_smoke.py --unit CF1 --pages L03 L04",
   "Ran .venv/bin/python tools/page_smoke.py --unit CF1 --pages L03 L04 (rc 0): 'page_smoke modules/CF/CF1/L03.html: PASS' (runtime boot 1.1 s; lab-CF1-L04-1 0.1 s), 'page_smoke modules/CF/CF1/L04.html: PASS', 'page_smoke CF1: PASS'. Well under 10 s."),
 "CF1-b-r6-pytest-labs": ("2.5-labs", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
   "Ran .venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py (rc 0; 100 percent dots, no failure). Output in ledgers/CF1/scripts/CF1-b-r17/pytest.out."),
 "CF1-b-r6-delta-coverage": ("2.9-structure", "git diff --stat 2c8162b fefbf8b -- course/modules/CF/CF1 tests/labs/CF1; slice files only",
   "Slice-b delta from 2c8162b to fefbf8b: " + L04 + " 1 line (l.549, next link), cards.json (18 cards changed across the unit, 9 of them L03/L04; 5 new L03/L04 ids c103, c105-c108), index.html (L03 and L04 card titles; L05 card title), tests/labs/CF1/lab-CF1-L05-1.py not in slice. " + L03 + " and both lab twins byte-identical (git diff --quiet exit 0). Every changed line of the slice is covered by a row of this round."),
}
new = []
def add(id_, check, loc, status, ev):
    new.append({"id": id_, "check": check, "location": loc, "status": status, "evidence": ev})
add("CF1-b-r17-delta-coverage", "2.9-structure", "git diff --stat 2c8162b fefbf8b -- course/modules/CF/CF1 tests/labs/CF1", "PASS",
    "Slice-b delta from 2c8162b to fefbf8b: L04.html 1 line changed (l.549, next link text); cards.json changed (per-card comparison, " + S + "cards_prev.json vs cards_new.json: 18 existing cards changed across the unit, 9 of them L03/L04; 9 new ids c101-c109, of which c103, c105, c106, c107, c108 are L03/L04); index.html changed (L03 and L04 card titles checked, rows below); L03.html and both twins byte-identical. Every changed slice line has a row here.")
add("CF1-b-r17-L04-l549-next-link", "2.9-structure", L04 + " l.549 (lesson-nav next link)", "PASS",
    "L04.html l.549: 'L05 · Payback and Its Discounted Form' is byte-equal to the course/modules/CF/CF1/L05.html h1 (l.36: 'Payback and Its Discounted Form'). The link target L05.html exists. Verified by grep.")
add("CF1-b-r17-index-card-titles-L03-L04", "2.9-structure", "course/modules/CF/CF1/index.html l.138-139 (L03, L04 cards) against L03.html l.35 and L04.html l.35", "PASS",
    "index.html L03 card title 'Inflation and Real Cash Flows' = L03 h1 (l.35); L04 card title 'Internal Rate of Return and Its Pitfalls' = L04 h1 (l.35). Card bodies name the same topics as the lesson sections (Fisher relation, consistent discounting; IRR, multiple IRRs, ranking conflict).")
add("CF1-b-r17-cards-L03-changed", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c036, CF1-c042, CF1-c103, CF1-c105 against " + L03 + " l.71 (Thm 1.3), l.247-248, l.118 (Ex 2.5), l.240-241 (Lab 1 output), l.102-105 (Thm 2.3)", "PASS",
    "CF1-c036 front/back: 'n = r + pi + r pi (Theorem 1.3)' equals l.71 exactly. CF1-c042 (front now 3 per cent only): back '113,637.49 dollars, against a real NPV of 263,709.14 dollars' matches Lab 1 output line 240 ('0.03  113637.49') and line 228/226. CF1-c103 (new): '194,368.27 dollars' matches output line 241 ('0.05  194368.27'); grade C with basis 'Lab 1 (SIMULATED inputs)' matches the page's grade of the same numbers (l.390-391). CF1-c105 (new): 'By exactly r pi' matches Thm 1.3 l.71 and grade T.")
add("CF1-b-r17-cards-L04-changed", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c051, c053, c054, c056, c058, c060, c094, c106, c107, c108 against " + L04 + " l.79, l.86, l.113, l.127-130, l.135, l.145, l.300, l.322, l.330, l.451-456", "PASS",
    "c051 back = Thm 2.1 l.79 ('strictly decreasing'); c053 back = Prop 3.3 l.109 formula, the IRR part removed from the answer; c054 back 'provided dK is not zero and dC/dK is positive' = Thm 4.1 hypothesis l.127 (uniqueness of the crossover); c056 back 'Two sign changes, bisected to 0.100000 and 0.200000' = Lab 1 lines 280-282; c058 back 'False in general' with NPV -680.27 = output line 274 and misconception l.322; c060 NPV 189.04 = output line 276 and l.330; c094 '27,272.73 against 18,181.82' = output line 289 and Ex 4.2 l.135; c106 = Thm 2.1 l.79 (non-negative IRR iff sum non-negative: the proof l.82 gives x* <= 1 iff P(1) >= 0); c107 = Prop 3.3 l.110 and l.453; c108 '0.200000, the IRR of their difference B minus A' = output line 292 ('crossover rate, the IRR of the difference: 0.200000'). Grades T/C match key results l.450-457 and the grade used on the page (Lab results C, proofs T).")
add("CF1-b-r17-cards-count", "2.7-cards", "course/modules/CF/CF1/cards.json (109 cards; 40 with lesson L03 or L04)", "PASS",
    S + "card_scan.py: 109 cards, no duplicate ids or normalised fronts, the 40 L03/L04 ids equal the set listed in CF1-b-cards-L03-L04-other-29 (c033-c036, c037-c061 subset, c088, c091-c095, c103, c105-c108).")
add("CF1-b-r17-lab-output-identical", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py, tests/labs/CF1/lab-CF1-L04-1.py vs their page expected blocks", "PASS",
    "python -I -W error run of each twin, compared line by line with the page's <pre class=\"expected\"> block (" + S + "compare_expected.py): L03.html 24 lines identical, L04.html 29 lines identical.")
add("CF1-b-r17-mutant-m1-L04-cost", "2.5-labs", "tests/labs/CF1/lab-CF1-L04-1.py PROJECT_P (l.159); mutant ledgers/CF1/mutants/CF1-b-r17/mut01_L04.py", "PASS",
    "Student error: inflow/cost of P changed (-13_100_000 for -13_200_000). Killed: the first differing output line is 0-based index 0 (PROJECT_P cash flows line, 'NPV' values change). Recorded in mutants list.")
add("CF1-b-r17-mutant-m2-L04-break", "2.5-labs", "tests/labs/CF1/lab-CF1-L04-1.py all_roots (l.190-209); mutant mut02_L04.py", "PASS",
    "Student error: the root search stops at the first root (break). Killed: 'sign changes of the NPV profile on the grid: 2' becomes ': 1' (0-based output line 9); the page's claim that the search 'does not stop at the first root' (L04 l.145) is what this mutant breaks and the lab's output detects it.")
add("CF1-b-r17-mutant-m3-L03-nominal-exponent", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py nominal_flows (l.155-157); mutant mut04_L03.py", "PASS",
    "Student error: nominal flow uses the price level one year short. Killed: 0-based output line 3 '1  30000000  30900000.00' becomes '30000000.00'; the page's E-solution figures and the misconception l.269 would then differ.")
add("CF1-b-r17-mutant-m4-L03-grid", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py INFLATION_GRID (l.141); mutant mut06_L03.py", "PASS",
    "Student error: last inflation rate changed from 0.05 to 0.04. Killed: 0-based output line 23 '0.05  194368.27' becomes '0.04  153491.20'; the page's quoted 194,368.27 at 0.05 (l.241, l.391, c103) would be contradicted.")
add("CF1-b-r17-mutant-m5-L03-additive", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py main() (l.194-198) ; mutant mut07_L03.py", "PASS",
    "Student error: nominal rate taken as the additive r + pi. Killed: 0-based line 0 'nominal rate 0.091800' becomes '0.090000'.")
add("CF1-b-r17-mutant-grid-end", "2.5-labs", "tests/labs/CF1/lab-CF1-L04-1.py all_roots (l.196, steps = round(...) - 1); mutant mut03_L04.py", "PASS",
    "Survivor, out of scope: the grid ends at 0.9999 instead of 1.0. Printed output is identical because both roots (0.1, 0.2) are interior to the grid. The page's description 'from -0.5 to 1.0' (L04 l.145) is a statement about the shipped code, which reads GRID_HIGH = 1.0 (l.164) and steps = round((1.0 + 0.5)/0.0001) (l.196); the lab's expected block does not show the endpoint, and no page or grader claim is violated by the printed output. Not a FAIL: the lab output is not required to reveal its grid endpoint.")
add("CF1-b-r17-mutant-t0-identity", "2.4-mathematics", "tests/labs/CF1/lab-CF1-L03-1.py mixed_identity (l.165-167); mutant mut05_L03.py", "PASS",
    "Equivalent mutant: the sum changed from t >= 1 to t >= 0. The added t = 0 term is real[0] * ((1+pi)**0 - 1)/(1+r)**0 = real[0] * 0 = 0 for every input, so the identity value and all printed lines are unchanged. Proof row; not in the mutants list.")
add("CF1-b-r17-mutant-control", "2.5-labs", "mut00_L04.py (unchanged copy of tests/labs/CF1/lab-CF1-L04-1.py)", "PASS",
    "Control: the unmodified twin in the mutation harness reproduces the expected block exactly (first diff: none), so the harness is not rejecting valid code.")
add("CF1-b-r17-L03-E1-E2", "2.2-numbers", L03 + " E1 (l.332-334), E2 (l.339-342)", "PASS",
    "E1: 194368.27/263709.14 = 0.73706 -> 73.7 per cent; 36913.22 -> 14.0; 113637.49 -> 43.1 (recomputed in recompute_numbers.py). E2: lab copy with inflation 0.00 prints 0.00 (e2_e3_claims.py).")
add("CF1-b-r17-math-L04-R2-R3-E2", "2.4-mathematics", L04 + " R2 (l.431), R3 (l.438), E2 (l.406), R1 (l.424), M2 (l.356)", "PASS",
    "Re-derived: R2 NPV_B - NPV_A = (C_B - C_A)/(1+r) > 0 (sign and the equal-outlay argument); IRRs C/K - 1; example IRR_A = sqrt(3) - 1 = 0.732051 and the NPVs 147.93 and 81.82; R1 factorization -(5x-1)(x-1) and NPV 0.322314 at 10 per cent; E2 crossover 1.3 - 1 = 0.30 and the 35 per cent NPVs; M2 root x = 0.884437, r = 0.130662. All consistent with the page and with scripts/recompute_numbers.py.")
add("CF1-b-r17-hours-arithmetic", "hours", "course/modules/CF/CF1/index.html (data-hours-lessons=48, data-hours-project=12, eyebrow l.31, l.41)", "PASS",
    "6 lessons x 8 h = 48 h lessons; 48 + 12 = 60 h; 12/60 = 20.0 per cent; index eyebrow '48 h lessons · 12 h project (20.0% of the 60 module hours)'. No arithmetic inconsistency between hub split and lesson hours. Pace not judged (architect ruling).")
add("CF1-b-r17-ruff-mypy-twins", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py, tests/labs/CF1/lab-CF1-L04-1.py", "PASS",
    "ruff check, ruff format --check: pass; mypy --no-incremental on the two files: 'Success: no issues found in 2 source files' (" + S + "mypy.out).")
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in rerun:
        check, loc, ev = rerun[rid]
        rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
    else:
        ev = r["evidence"]
        if "cards.json" in r["location"]:
            files = "course/modules/CF/CF1/cards.json entries cited (each card text byte-identical in cards_prev.json and cards_new.json)"
        elif L03 in r["location"]:
            files = L03
        elif L04 in r["location"]:
            files = L04 + " (cited lines unchanged; the only changed line is l.549)"
        else:
            files = "the cited files (tests/labs/CF1 twins, references, tools)"
        prefix = "Carried from round 16 (" + files + " byte-identical since the previous pin): "
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                     "evidence": prefix + ev})
rows += new
print("prev", len(prev["rows"]), "rerun", sum(1 for r in prev["rows"] if r["id"] in rerun), "new", len(new), "total", len(rows))
json.dump(rows, open("/tmp/cf1-v/CF1-b-r17/rows.json", "w"), indent=1)
