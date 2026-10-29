import json, pathlib, subprocess
ROOT = pathlib.Path("/tmp/verify23-CF1-b")
prev = json.load(open("/tmp/fanout-frags/CF1-b.round22.json"))
prev_rows = {r["id"]: r for r in prev["rows"]}
PIN_PREV = "fefbf8b"
PAGES = "course/modules/CF/CF1/L03.html, course/modules/CF/CF1/L04.html, tests/labs/CF1/lab-CF1-L03-1.py, tests/labs/CF1/lab-CF1-L04-1.py"
CARRY = "Carried from round 22 (%s byte-identical since the previous pin):"
CARD_CARRY = "Carried from round 22 (course/modules/CF/CF1/cards.json entries named here byte-identical since the previous pin):"
CARD_SUBJ_NEW = "course/modules/CF/CF1/cards.json"

# Re-verified this round (new evidence, command or changed subject)
NEW = {
 "CF1-b-cmd-check-pages": "Re-run round 23 at 503d139: .venv/bin/python tools/check_pages.py --all -> 'check_pages CF1: PASS', rc 0 (ledgers/CF1/scripts/CF1-b-r23/out/check_pages.out).",
 "CF1-b-cmd-check-dag": "Re-run round 23: tools/check_dag.py --all -> 'check_dag CF1: PASS', rc 0 (out/check_dag.out).",
 "CF1-b-cmd-run-labs": "Re-run round 23: tools/run_labs.py --unit CF1 -> 'run_labs CF1: PASS (9/9)', rc 0 (out/run_labs.out).",
 "CF1-b-lab-twin-direct": "Re-run round 23: python -I -W error tests/labs/CF1/lab-CF1-L03-1.py and lab-CF1-L04-1.py -> rc 0, empty stderr (out/twin_L03.stdout, out/twin_L04.stdout).",
 "CF1-b-lab-twin-lint": "Re-run round 23: ruff check on both twins 'All checks passed!'; ruff format --check tests/labs/CF1/ '9 files already formatted'; mypy --no-incremental on both twins 'Success: no issues found in 2 source files'.",
 "CF1-b-lab-L03-1": "Re-read course/modules/CF/CF1/L03.html l.123 hypothesis (0.0918, 12-case grid, no random numbers; the code is shown from l.124 and is the twin, offset 123 lines) and l.242 interpretation (gap 0.00 at 0.00 inflation, rising table 36913.22, 113637.49, 194368.27 in the expected block starting l.218). Twin stdout identical to page expected block (out/compare_expected).",
 "CF1-b-lab-L04-1": "Re-read L04.html l.145 hypothesis (roots 10 and 20 per cent, NPV at 5 per cent negative, crossover 20 per cent, grid -0.5 to 1.0 step 0.0001, bisection of every sign change; twin code offset 145 lines, all_roots at l.190-209) and l.300 interpretation; expected block starts l.271; twin stdout identical to expected block (out/compare_expected).",
 "CF1-b-lab-L03-E2-claim": "Re-run round 23: copy with INFLATION=0.00 (ledgers/CF1/mutants/CF1-b-r17/copy_E2.py) prints 'mixed minus real, cents: 0.00', both mixed NPVs 263709.14 USD, table row 0.00 0.00; E2 claim at L03.html l.338-342 matches.",
 "CF1-b-lab-L03-E3-claim": "Re-run round 23: copy with REAL_RATE=0.10 (copy_E3.py) prints nominal rate 0.133000 and consistency gap 0.000000; E3 claim at L03.html l.345-348 matches.",
 "CF1-b-numbers-L03": "Recomputed round 23 by ledgers/CF1/scripts/CF1-b-r23/recompute_numbers_r23.py (out/recompute_numbers.out): 0.0918, gap 0.0018, 263709.14, 113637.49 (share 0.4309 = 43.1%), 194368.27 (73.706% = 73.7%), 36913.22 (14.0%), 257.7097, 0.048544, 1061.208, 94.545, 0.070711, 2.06, 0.522167, 0.133, 190.476, 0.07625, 0.025 all match the page.",
 "CF1-b-numbers-L04": "Recomputed round 23 (out/recompute_numbers.out): -680.27 (5%), 189.04 (15%), 18181.82 / 27272.73 (10%), 8333.33 each (20%), 0.322314 (R1), 147.93 / 81.82 (R2), 0.732051, 0.884437 and 0.130662 (M2), FV 250.00 and -750.00 USD (R3, 25000 and -75000 cents), 0 (Remark 5.1), 0.30 (E2 crossover) all match the page.",
 "CF1-b-prose-banned-scan": "Re-run round 23 grep over L03.html and L04.html for roughly|about|historically|typically|usually|generally|often|always|only|all|same|drives|offsets|raises|as much as|ellipsis|process words: no banned phrase; each scope word was read in place (e.g. L03 l.98 'Every sum is finite' follows from finitely many nonzero terms; L04 l.140 'twice as much' is 200,000 vs 100,000 USD).",
 "CF1-b-cards-duplicate-scan": "Re-run round 23 on cards.json (110 cards): all ids unique, no duplicate front and no duplicate back (Python scan).",
 "CF1-b-cards-L03-L04-other-29": "Round 23: the 9 L03/L04 cards changed since fefbf8b (CF1-c033, c034, c035, c047, c048, c049, c054, c088, c091) were re-read against the lesson text in this round (rows CF1-b-r23-card-*). The other 31 L03/L04 cards are byte-identical since fefbf8b, so their round-17 evidence is carried.",
 "CF1-b-r6-verify-refs": "Re-run round 23: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' rc 0; tools/verify_refs.py --unit CF1 -> 'live re-verification of CF1: 2 of 560 entries, 0 problems' rc 0 (out/vr_offline.out, out/vr_live.out). L03/L04 cite no registry key.",
 "CF1-b-r6-page-smoke": "Re-run round 23: tools/page_smoke.py --unit CF1 --pages L03 L04 -> both PASS, lab runtimes 0.0 s and 0.1 s, 'page_smoke CF1: PASS', rc 0 (out/page_smoke.out).",
 "CF1-b-r6-pytest-labs": "Re-run round 23: python -I -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -> all dots, rc 0 (out/pytest.out).",
 "CF1-b-r6-delta-coverage": "Round 23 delta: git diff --stat fefbf8b 503d139 -- course/modules/CF/CF1 tests/labs/CF1: changed files are L01, L05, L06, cards.json, grader/test_project.py, index.html, project.html (CF1) and AC1/AC4 labs; L03.html, L04.html and both CF1 twins are NOT in the diff (git diff --quiet exit 0).",
 "CF1-b-r8-cards-c033-c034-c088": "Re-verified round 23: cards.json CF1-c033 (Definition 1.1, P_t=(1+pi)^t), CF1-c034 (Definition 1.2, see row CF1-b-r23-card-c034), CF1-c088 (Definition 1.1, C^r_t = C^n_t/P_t) against L03.html l.56-57 (Definition 1.1), l.85-86 (Definition 2.1), l.61-64 (Definition 1.2) and the changed basis wording; all PASS.",
 "CF1-b-r17-delta-coverage": "Superseded for the round-23 delta by CF1-b-r6-delta-coverage (fefbf8b..503d139 re-computed): no change to L03.html, L04.html or the two twins.",
 "CF1-b-r17-index-card-titles-L03-L04": "Re-run round 23: course/modules/CF/CF1/index.html l.138-139 card titles 'Inflation and Real Cash Flows' and 'Internal Rate of Return and Its Pitfalls' match L03.html l.35 and L04.html h1; index diff since fefbf8b touched only the placement paragraph and L05/ladder lines.",
 "CF1-b-r17-cards-count": "Re-run round 23: cards.json has 110 cards (c110 added, lesson L01); 40 cards have lesson L03 or L04 (c033-c061, c088, c091-c095, c103, c105-c108), as before.",
 "CF1-b-r17-cards-L04-changed": "Re-verified round 23: CF1-c054 (changed back; grade T, basis Theorem 4.1) against L04.html Theorem 4.1 statement l.127 and proof l.130: r* = dC/dK - 1 with dK = K_B - K_A, dC = C_B - C_A, the ratio positive and dK nonzero (see CF1-b-r23-card-c054). The other changed-L04 cards are re-verified in CF1-b-r23-card-c047-c049-c091; the unchanged ones (c051, c053, c056, c058, c060, c094) are carried.",
 "CF1-b-r17-cards-L03-changed": "Round 23: cards CF1-c036, c042, c103, c105 are byte-identical since fefbf8b (not in the round-23 diff), so the round-17 evidence is carried.",
 "CF1-b-r17-lab-output-identical": "Re-run round 23: both twin outputs equal the page expected blocks line for line (out/compare_expected run: L03 24 lines identical; L04 29 lines identical).",
 "CF1-b-r17-mutant-m1-L04-cost": "Re-run round 23: mut01_L04.py (PROJECT_P final flow -13,100,000) exit 0, output line 0 differs from expected (out/mutants_existing.out) -> KILLED against the expected block. Lab-twin mutant: out of scope for the grader rule (architect ruling); recorded as killed.",
 "CF1-b-r17-mutant-m2-L04-break": "Re-run round 23: mut02_L04.py (break after first root) exit 0, line 9 'sign changes ... 2' becomes '1' -> KILLED against the expected block.",
 "CF1-b-r17-mutant-m3-L03-nominal-exponent": "Re-run round 23: mut04_L03.py (price level one year short) line 3 '30900000.00' becomes '30000000.00' -> KILLED.",
 "CF1-b-r17-mutant-m4-L03-grid": "Re-run round 23: mut06_L03.py (grid last value 0.04) line 23 '194368.27' becomes '153491.20' -> KILLED.",
 "CF1-b-r17-mutant-m5-L03-additive": "Re-run round 23: mut07_L03.py (additive nominal rate 0.090000) line 0 -> KILLED.",
 "CF1-b-r17-mutant-grid-end": "Re-run round 23: mut03_L04.py (grid ends at 0.9999 instead of 1.0) exits 0 and its output is identical to the expected block. Out of scope: lab twins are demonstrations (architect ruling), and no printed line or lesson sentence claims the lab checks the grid endpoint. The lesson's sentence (L04.html l.145) that the scan runs from -0.5 to 1.0 is a description that the unmutated code satisfies (twin l.18-19, page l.163-164). PASS.",
 "CF1-b-r17-mutant-t0-identity": "Re-run round 23: mut05_L03.py (mixed_identity sums from t >= 0) exits 0 with identical output. Equivalent mutant: the t = 0 term is C * ((1+pi)**0 - 1) / (1+r)**0 = 0 for every pi and r, so the sum is unchanged. PASS (equivalent).",
 "CF1-b-r17-mutant-control": "Re-run round 23: mut00_L04.py (unchanged copy) exits 0 and matches the expected block (out/mutants_existing.out). Control behaves as expected.",
 "CF1-b-r17-ruff-mypy-twins": "Re-run round 23: ruff check and ruff format --check and mypy --no-incremental on both twins all clean (see CF1-b-lab-twin-lint).",
 "CF1-b-r17-hours-arithmetic": "Re-run round 23: index.html l.29 data-hours-lessons=48 (6 x 8 h, L01-L06 each 8 h on the hub cards), data-hours-project=12; curriculum/curriculum.json CF1 hours 60 = 48 + 12; L03.html l.2 and L04.html l.2 data-hours=8. Consistent. Pace not judged (architect ruling).",
 "CF1-b-r17-L03-E1-E2": "Round 23: E1 division 194368.27/263709.14 = 0.73706 (73.7%), 36913.22/... = 14.0%, 113637.49/... = 43.1%; E2 re-run (see CF1-b-lab-L03-E2-claim). PASS.",
 "CF1-b-r17-math-L04-R2-R3-E2": "Round 23: R2 arithmetic (147.93, 81.82, sqrt(3)-1 = 0.732051), R3 FV (250.00, -750.00), E2 (IRR 20%/25%, crossover 0.30, NPVs 9090.91, 27272.73, -11111.11, -14814.81) re-computed in recompute_numbers_r23.py; the page text matches. PASS.",
 "CF1-b-cmd-dag-concepts": "Re-run round 23 (check_dag above).",
}
# Carried rows that are NOT re-run this round (subject byte-identical since fefbf8b)
CARD_IDS = {"CF1-b-r5-cards-scope-c037", "CF1-b-cards-L03-finiteness-and-positivity", "CF1-b-cards-L04-one-sign-change"}

rows = []
for rid in [r["id"] for r in prev["rows"]]:
    p = prev_rows[rid]
    if rid in NEW:
        rows.append({"id": rid, "check": p["check"], "location": p["location"], "status": "PASS", "evidence": NEW[rid]})
    elif rid in CARD_IDS or "cards" in p["location"]:
        rows.append({"id": rid, "check": p["check"], "location": p["location"], "status": p["status"],
                     "evidence": CARD_CARRY + " " + p["evidence"]})
    else:
        rows.append({"id": rid, "check": p["check"], "location": p["location"], "status": p["status"],
                     "evidence": CARRY % PAGES + " " + p["evidence"]})

NEW_ROWS = [
 ("CF1-b-r23-delta-coverage", "2.9-structure", "git diff --stat fefbf8b 503d139 for CF1 slice b",
  "git diff --name-only fefbf8b 503d139: L03.html, L04.html and the two twins are unchanged (git diff --quiet exit 0). Changed CF1 files are L01, L05, L06, index.html (L05 card and placement paragraph), project.html, cards.json and grader (other slices). Changed cards in this slice: CF1-c033, c034, c035, c047, c048, c049, c054, c088, c091 (L03/L04); c110 is new and belongs to L01 (out of slice). Also course/assets/data/program.json, curriculum/01-foundations.yaml (CS2 prerequisite only) and AC1/AC4 labs changed, none read by these lessons."),
 ("CF1-b-r23-card-c033-c035-c088", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c033, CF1-c035, CF1-c088 vs L03.html l.57, l.64, l.86-87",
  "CF1-c033 (Definition 1.1: P_t = (1+pi)^t, base year 0, P_0 = 1) matches L03.html l.57. CF1-c035 (consistent discounting; Definition 2.1 l.85-86) matches. CF1-c088 (C^r_t = C^n_t/P_t, base-year money; Definition 1.1 l.57) matches. Basis changes ('Definition x (the lesson's definition)') name the lesson's own definition; grade C is the convention rule (BLUEPRINT). PASS."),
 ("CF1-b-r23-card-c034", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c034 vs L03.html l.61-64 and l.67",
  "Relation 1+n = (1+r)(1+pi) and r = (1+n)/(1+pi)-1 match Definition 1.2 (l.62-64). The back also says 'an exact definition of the real rate ... not an empirical claim': that sentence is on L03.html l.67, the paragraph after Definition 1.2, not in Definition 1.2 itself; the card cites only '(Definition 1.2)'. The claim is supported by the page, so the row is PASS; the locator should read 'Definition 1.2 and the paragraph after it' (non-blocking note)."),
 ("CF1-b-r23-card-c047-c049-c091", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c047, c048, c049, c091 vs L04.html Definition 1.1 (l.56-57), Definition 1.2 (l.61-62), Definition 3.1 (l.95-96)",
  "c047 (NPV profile, sum t=0..N, r>-1, one period per year) matches Definition 1.1. c048 (IRR is a rate r>-1 with NPV(r)=0; set of roots on (-1,inf)) matches Definition 1.2. c049 (first part of the multiple-IRR problem, more than one IRR) matches Definition 3.1 and c091 (second part: mutually exclusive pair whose IRR and NPV rankings disagree at the rate that applies) matches Definition 3.1. Grade C, basis 'Definition x (the lesson's definition)'. PASS."),
 ("CF1-b-r23-card-c054", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c054 vs L04.html Theorem 4.1 (statement l.127, proof l.130)",
  "The back r* = (C_B - C_A)/(K_B - K_A) - 1, with K_B - K_A not zero and the ratio positive, is Theorem 4.1 with dC/dK; K is the outlay (-K at t=0) and C the inflow at t=1 (L04.html Theorem 4.1 statement). The front restricts to 'one inflow at t = 1, all four amounts positive', which is the theorem's hypothesis. The grade T with basis 'Theorem 4.1, proved in Section 4' matches the page's T claim. Numerical check: Example 4.2 gives 20 per cent (recompute_numbers_r23.py). PASS."),
 ("CF1-b-r23-card-L03-L04-changed-set", "2.7-cards", "course/modules/CF/CF1/cards.json: the 9 changed L03/L04 cards by id",
  "Set diff against the round-17 pin (python compare of cards.json at fefbf8b and 503d139) lists exactly the changed L03/L04 ids c033, c034, c035, c047, c048, c049, c054, c088, c091, each re-verified in the rows above; no L03/L04 card was added or removed (40 before and after)."),
 ("CF1-b-r23-mutant-m01-L03-deflate", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py nominal_flows (l.155-157); mutant ledgers/CF1/mutants/CF1-b-r23/r23_m01_L03_deflate_nominal_flows.py",
  "Student error: deflating the real flows instead of inflating them. Output line 3 becomes '1  30000000  29126213.59' against expected '30900000.00'. KILLED (exit 0, output differs)."),
 ("CF1-b-r23-mutant-m02-L04-first-flow-t1", "2.5-labs", "tests/labs/CF1/lab-CF1-L04-1.py npv (twin l.23-28, page l.168-173); mutant ledgers/CF1/mutants/CF1-b-r23/r23_m02_L04_npv_discounts_first_flow_at_t1.py",
  "Student error: every flow discounted one period late (t+1). Output line 3 'rate 0.05 NPV -680.27' becomes '-647.88'; KILLED."),
 ("CF1-b-r23-mutant-m03-L04-zero-root-skipped", "2.5-labs", "tests/labs/CF1/lab-CF1-L04-1.py all_roots (twin l.56, page l.201); mutant ledgers/CF1/mutants/CF1-b-r23/r23_m03_L04_strict_sign_change_skips_exact_zero.py",
  "Student error: skipping a grid point whose NPV is exactly zero. The lab then fails with IndexError (exit 1) on project A's IRR; KILLED."),
 ("CF1-b-r23-twin-expected-identical", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py, lab-CF1-L04-1.py vs the page expected blocks",
  "Both twin outputs match the embedded expected blocks line for line (24 and 29 lines; script ledgers/CF1/scripts/CF1-b-r23/compare_expected.py)."),
 ("CF1-b-r23-alt-implementations", "2.5-labs", "project graders: none in slice b",
  "Not applicable: slice b has no project grader; lab twins are demonstrations (architect ruling). No alternative implementation check was run for this slice."),
]
for rid, check, loc, ev in NEW_ROWS:
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

mutants = [
 {"id": "m00-L04-control", "file": "tests/labs/CF1/lab-CF1-L04-1.py", "description": "control: unchanged copy", "killed_by": "none (must match expected)", "mutant_file": "ledgers/CF1/mutants/CF1-b-r17/mut00_L04.py", "result": "matches expected (control)"},
 {"id": "m01-L04-cost-of-P", "file": "tests/labs/CF1/lab-CF1-L04-1.py", "description": "PROJECT_P final flow -13,200,000 changed to -13,100,000", "killed_by": "output line 0", "mutant_file": "ledgers/CF1/mutants/CF1-b-r17/mut01_L04.py", "result": "KILLED"},
 {"id": "m02-L04-first-root-only", "file": "tests/labs/CF1/lab-CF1-L04-1.py", "description": "all_roots stops after the first sign change", "killed_by": "output line 9", "mutant_file": "ledgers/CF1/mutants/CF1-b-r17/mut02_L04.py", "result": "KILLED"},
 {"id": "m03-L04-grid-end", "file": "tests/labs/CF1/lab-CF1-L04-1.py", "description": "grid ends at 0.9999 instead of 1.0", "killed_by": "none; exit 0, identical output", "mutant_file": "ledgers/CF1/mutants/CF1-b-r17/mut03_L04.py", "result": "SURVIVES, out of scope (lab twin, no printed line or lesson assertion depends on the endpoint)"},
 {"id": "m04-L03-price-level-one-year-short", "file": "tests/labs/CF1/lab-CF1-L03-1.py", "description": "nominal_flows uses (1+pi)**(t-1) for t>=1", "killed_by": "output line 3", "mutant_file": "ledgers/CF1/mutants/CF1-b-r17/mut04_L03.py", "result": "KILLED"},
 {"id": "m05-L03-identity-from-t0", "file": "tests/labs/CF1/lab-CF1-L03-1.py", "description": "mixed_identity sums from t >= 0", "killed_by": "none; equivalent", "mutant_file": "ledgers/CF1/mutants/CF1-b-r17/mut05_L03.py", "result": "SURVIVES, equivalent (t=0 term is zero for every pi)"},
 {"id": "m06-L03-last-inflation-rate", "file": "tests/labs/CF1/lab-CF1-L03-1.py", "description": "INFLATION_GRID last value 0.05 changed to 0.04", "killed_by": "output line 23", "mutant_file": "ledgers/CF1/mutants/CF1-b-r17/mut06_L03.py", "result": "KILLED"},
 {"id": "m07-L03-additive-nominal-rate", "file": "tests/labs/CF1/lab-CF1-L03-1.py", "description": "nominal rate taken as r + pi", "killed_by": "output line 0", "mutant_file": "ledgers/CF1/mutants/CF1-b-r17/mut07_L03.py", "result": "KILLED"},
 {"id": "r23-m01-L03-deflate-nominal-flows", "file": "tests/labs/CF1/lab-CF1-L03-1.py", "description": "student error: real flows deflated instead of inflated", "killed_by": "output line 3", "mutant_file": "ledgers/CF1/mutants/CF1-b-r23/r23_m01_L03_deflate_nominal_flows.py", "result": "KILLED"},
 {"id": "r23-m02-L04-npv-first-flow-at-t1", "file": "tests/labs/CF1/lab-CF1-L04-1.py", "description": "student error: every flow discounted one period late", "killed_by": "output line 3", "mutant_file": "ledgers/CF1/mutants/CF1-b-r23/r23_m02_L04_npv_discounts_first_flow_at_t1.py", "result": "KILLED"},
 {"id": "r23-m03-L04-exact-zero-skipped", "file": "tests/labs/CF1/lab-CF1-L04-1.py", "description": "student error: grid points with NPV exactly zero skipped", "killed_by": "exit 1, IndexError", "mutant_file": "ledgers/CF1/mutants/CF1-b-r23/r23_m03_L04_strict_sign_change_skips_exact_zero.py", "result": "KILLED"},
]
frag = {
 "unit": "CF1", "slice": "CF1-b", "round": 23,
 "verifier": "independent Haiku verifier, CF1 slice b (L03, L04 and their lab twins), round 23; did not build CF1 and shares no context with the builders or earlier verifiers",
 "pin": "503d139",
 "base": "fefbf8b (previous slice-b pin, round 17 content; the file given as previous fragment is named round22 but its content is round 17)",
 "previous_ledger": "/tmp/fanout-frags/CF1-b.round22.json",
 "checkout": "/tmp/verify23-CF1-b (detached at 503d139, .venv symlinked)",
 "scratch": "/tmp/cf1-v/CF1-b-r23",
 "verified_at": "2026-10-28T12:00:00+00:00",
 "verdict": "PASS",
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Delta fefbf8b..503d139 for this slice: L03.html, L04.html and both lab twins are byte-identical. Changed cards in L03/L04: c033, c034, c035, c047, c048, c049, c054, c088, c091 (all re-read in this round). Index L03/L04 card titles unchanged. Every previous PASS row whose cited subject is byte-identical is carried with the round-22 prefix; every row whose subject changed or that is a command row was re-run or re-read.",
  "Not a fail, noted for the builder: CF1-c034 back cites '(Definition 1.2)' for 'an exact definition ... not an empirical claim', which is stated in the paragraph after Definition 1.2 (L03.html l.67); tightening the locator would remove the ambiguity.",
  "Out of this slice but seen in the delta: cards.json CF1-c110 (lesson L01) cites Assumption 4.0 and Remark 4.3 of L01 and Problem R3 of L01; not verified here (slice a)."  ,
  "Commands re-run on 503d139 this round: check_pages --all (CF1 PASS), check_dag --all (CF1 PASS), run_labs --unit CF1 (9/9), both twins under python -I -W error (rc 0), page_smoke --unit CF1 --pages L03 L04 (PASS), pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py (rc 0), ruff check and format --check on the twins, mypy --no-incremental on the twins, verify_refs --offline (560 entries, 0 problems), verify_refs --unit CF1 (2 of 560, 0 problems). Scripts: ledgers/CF1/scripts/CF1-b-r23/.",
  "Mutants: 10 lab-twin mutants and control re-run (ledgers/CF1/mutants/CF1-b-r17/ and CF1-b-r23/), 3 new student-error mutants written and killed. Lab-twin mutants are out of the grader rule (architect ruling); the two survivors (grid end, t=0 identity) are recorded as out of scope and equivalent with reasons.",
  "Not run: the full gate; tests/test_figure_kernels.py and other repo-wide pytest (outside this slice); run_graders and mutate_graders (no project grader in slice b); alternative correct implementations (N/A, lab demonstrations).",
  "Could not check: no external source is cited by L03 or L04 (registry keys: none), so no publisher or SEC page was contacted and no access statement is made. Hours are checked only for arithmetic (48 + 12 = 60, 8 h per lesson); pace is not judged.",
 ],
 "summary": {},
}
rows_all = frag["rows"]
frag["summary"] = {"rows": len(rows_all), "pass": sum(r["status"] == "PASS" for r in rows_all), "non_pass": [r["id"] for r in rows_all if r["status"] != "PASS"]}
out = ROOT / "ledgers/CF1/CF1-b.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, frag["summary"])
