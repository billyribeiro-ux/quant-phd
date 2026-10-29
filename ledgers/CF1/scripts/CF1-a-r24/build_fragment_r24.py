"""Build the round-24 CF1-a fragment from the round-23 rows plus this round's re-verification."""
import json
import pathlib

ROOT = pathlib.Path("/tmp/verify24-CF1-a")
prev = json.loads(pathlib.Path("/tmp/fanout-frags/CF1-a.round23.json").read_text())
CARRY = "Carried from round 23 (files byte-identical since the previous pin 503d139): "
FRESH = {
    "CF1-a-gate-check-pages": ("check_pages.py --unit CF1 exit 0, 'check_pages CF1: PASS' (out/check_pages.out)", "PASS"),
    "CF1-a-gate-check-dag": ("check_dag.py --all exit 0: 'check_dag CF1: PASS', 'check_dag AP1: PASS', 'check_dag AC4: PASS' (out/check_dag.out)", "PASS"),
    "CF1-a-gate-run-labs": ("run_labs.py --unit CF1 exit 0, 'run_labs CF1: PASS (9/9)' (out/run_labs.out)", "PASS"),
    "CF1-a-gate-page-smoke": ("page_smoke.py --unit CF1 --pages L01 L02 index exit 0, 'page_smoke CF1: PASS' (out/page_smoke.out)", "PASS"),
    "CF1-a-gate-lint-types": ("ruff check . and ruff format --check . ('All checks passed!', '220 files already formatted'); mypy --no-incremental 'Success: no issues found in 153 source files' (out/ruff.out, out/mypy.out)", "PASS"),
    "CF1-a-gate-pytest": ("pytest -q -k CF1 tests: exit 0, all dots (out/pytest_CF1.out)", "PASS"),
    "CF1-a-cite-verify-refs": ("verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' exit 0; verify_refs.py --unit CF1: 'live re-verification of CF1: 2 of 560 entries, 0 problems' exit 0 (out/verify_refs_offline.out, out/verify_refs_live_CF1.out)", "PASS"),
    "CF1-a-hub-scope-simulated": ("Re-verified round 24: index.html line 161 now lists Example 1.2 and Example 5.3 on L01 and the machine of L02 Section 4. L01.html line 67-68 ('A SIMULATED project costs 10,000 dollars'), line 171-172 ('A SIMULATED project pays 120 dollars'), line 153 (L02, 'generated from a seeded generator' in lab docstring, lab-CF1-L01-1.py line 3-5 and L02.html line 153 'Lab 2 builds one SIMULATED project'); the L01 lab (L01.html line 180-181) and L02 lab (L02 line 164) carry the SIMULATED docstrings", "PASS"),
    "CF1-a-hub-data-file-claim": ("Re-verified round 24: grep for .csv, .parquet, market/, data/, fetch( in course/modules/CF/CF1/{index,L01,L02}.html returns no match, so 'No CF1 page embeds a dataset or reads a market data file' holds for these pages", "PASS"),
    "CF1-a-hub-numbers-claim": ("Re-verified round 24: index.html line 161 sentence 'Each numeric answer ... read from a printed SIMULATED lab output; ... L01 E1 to E3 and quiz item 8, and L02 E1 to E3 and quiz item 8'. L01.html E1-E3 read printed Lab 1 output (lines 405-419); L02.html E1-E3 read printed Lab 2 table or NPV (lines 363, 370, 377)", "PASS"),
    "CF1-a-L01-read-full": ("Re-read round 24: the two changed hunks (L01.html line 90 Remark 2.2 and line 466 grade-table row) read in full; all other lines are byte-identical to the round-23 pin and carried from the round-23 full read (see the scope note in notes)", "PASS"),
    "CF1-a-L01-math-props": ("Re-verified round 24: L01.html line 90 (Remark 2.2) is the only changed line in lines 79-106; the proofs of Propositions 2.1 are unchanged and carried from round 23 (byte-identical)", "PASS"),
    "CF1-a-L01-grades": ("Re-verified round 24: L01.html line 466 now reads 'With different borrowing and lending rates the decision on one project can change with the rate that applies; the one instance in Problem R3 flips sign between the two rates' graded T; Problem R3 (L01.html lines 442-446) gives -1 + 1.05/1.06 = -0.009434 (recomputed: -0.009433962) and -1 + 1.05/1.03 = +0.019417 (recomputed: 0.019417475), so the sign flips and T is supported by the computation on the page. The card CF1-c110 still grades the same claim C: see CF1-a-r23-c110", "PASS"),
    "CF1-a-r23-c110": ("course/modules/CF/CF1/cards.json CF1-c110 (unchanged since 503d139): grade 'C', basis 'Assumption 4.0 and Remark 4.3; Problem R3'. L01.html line 466 (the changed row, still T) and Problem R3 (line 446) state the same claim as computed. The card and the page disagree on the grade of the same claim (C against T). Not fixed in round 24: the builder changed the row wording but not the grade", "FAIL"),
    "CF1-a-mutants": ("Re-run round 24: ledgers/CF1/scripts/CF1-a-r24/run_mut18_rerun (out/mutants_lab_rerun.out): 'killed 67 survived 3 total 70'; the 3 survivors (r9_m07, n05, r17_probe) are lab-twin mutants out of scope per the architect ruling and are dispositioned in CF1-a-r23-survivors", "PASS"),
    "CF1-a-r23-numbers": ("Re-run round 24: ledgers/CF1/scripts/CF1-a-r23/recompute_r23.py (python -I -W error) exit 0; R3 values -0.009433962 and 0.019417476 (page: -0.009434 and +0.019417, consistent)", "PASS"),
    "CF1-a-r23-lab-twins": ("Re-run round 24: python -I -W error tests/labs/CF1/lab-CF1-L01-1.py and lab-CF1-L02-1.py exit 0; stdout equals the embedded <pre class=\"expected\"> of L01.html (1087 chars) and L02.html (1119 chars) exactly (out/twin_*.out)", "PASS"),
    "CF1-a-r23-survivors": ("Re-run round 24: run_mut18.py gives the same 3 survivors as round 23; lab mutants are out of scope (architect ruling: mutation applies to project graders only)", "PASS"),
    "CF1-a-r23-check-liveness": ("tests/labs/CF1/lab-CF1-L02-1.py unchanged since 503d139 (lab files byte-identical); the shield check remains live per round 23", "PASS"),
}
NEW = [
    {
        "id": "CF1-a-r24-delta",
        "check": "round-24 delta for the slice",
        "location": "git diff --stat 503d139 23cbd6a -- course/modules/CF/CF1 tests/labs/CF1",
        "status": "PASS",
        "evidence": "Only course/modules/CF/CF1/L01.html (4 lines) and index.html (6 lines) changed; cards.json, L02.html, the lab twins and notation/references/tools unchanged (git diff --quiet on cards.json and L02.html both exit 0)",
    },
    {
        "id": "CF1-a-r24-hub-skill-check-wording",
        "check": "hub skill checks rung 1 and rung 2: new definitions of EBITDA and tax shield",
        "location": "course/modules/CF/CF1/index.html lines 122, 127",
        "status": "PASS",
        "evidence": "Rung 1 answer 375 recomputed: 400 x 0.75 + 0.25 x 300 = 375 (600/2 = 300 depreciation). The new phrase 'EBITDA, meaning revenue less cash operating cost' matches L02.html line 87 (EBITDA_t = R_t - K_t). Rung 2 answer 75 = 0.25 x 300. The new phrase 'the tax saved by the depreciation deduction' matches L02.html line 292 ('Its only cash effect is the tax it saves') and Corollary 2.3. Explain text unchanged",
    },
    {
        "id": "CF1-a-r24-hub-data-status-examples",
        "check": "hub data-status sentence naming examples that are SIMULATED or generated",
        "location": "course/modules/CF/CF1/index.html line 161",
        "status": "PASS",
        "evidence": "The new clause 'so are Example 1.2 and Example 5.3 on L01 and the machine of L02 Section 4' is checked against L01.html line 67 (Example 1.2, 'A SIMULATED project'), line 171 (Example 5.3, 'A SIMULATED project'), and L02.html line 153 ('Lab 2 builds one SIMULATED project ... generated from a seeded generator'). L01.html has exactly two blocks of class example (lines 66 and 170), so no third L01 example is left unlabelled. The earlier 'worked examples' wording was narrowed, not widened",
    },
    {
        "id": "CF1-a-r24-L01-remark22-part-c",
        "check": "L01 Remark 2.2 consequence attributed to Lab 1 Part C",
        "location": "course/modules/CF/CF1/L01.html line 90",
        "status": "PASS",
        "evidence": "Lab 1 Part C (L01.html line 262-272 code, expected output line 304 'additivity holds to within 1e-6 dollars for all fifty pairs: True') checks that the NPV of the sum of two generated 4-flow projects equals the sum of their NPVs, at RATE = 0.08 only. The remark's sentence 'the NPV of a bundle of projects that share one rate is the sum of their NPVs' is the general claim, which is Proposition 2.1 (proved on page); the lab checks it for pairs at one rate, and the sentence does not claim a different rate. Re-run: twin output contains 'True' for Part C",
    },
    {
        "id": "CF1-a-r24-L01-keyresults-R3-row",
        "check": "L01 key-results row on two borrowing and lending rates",
        "location": "course/modules/CF/CF1/L01.html line 466",
        "status": "PASS",
        "evidence": "'the decision on one project can change with the rate that applies; the one instance in Problem R3 flips sign between the two rates'. Problem R3 flows -1 and 1.05 give -0.009434 at the 6 percent borrowing rate and +0.019417 at the 3 percent lending rate (recomputed in recompute_r23.py: -0.009433962264, 0.019417475728), so the sign flips. The existence claim 'can change' is proved by the one computed instance; 'the one instance' is accurate because R3 is the only two-rate problem on the page (grep 'R3' in L01.html lines 323, 342, 446). Grade T is supported for the row; the card disagreement is CF1-a-r23-c110",
    },
    {
        "id": "CF1-a-r24-banned-scan",
        "check": "banned phrases and scope words in the changed hunks",
        "location": "git diff 503d139 23cbd6a -- course/modules/CF/CF1",
        "status": "PASS",
        "evidence": "grep -iE 'roughly|about|historically|...|build|round|verifier|generally|typically|always|only|all |same|drives|offsets|raises' over the added lines returns no match",
    },
    {
        "id": "CF1-a-r24-gate-ruff-mypy-pytest",
        "check": "ruff, mypy, and CF1 pytest rerun",
        "location": "ruff check .; ruff format --check .; mypy --no-incremental; pytest -q -k CF1 tests",
        "status": "PASS",
        "evidence": "ruff 'All checks passed!' and '220 files already formatted'; mypy 'Success: no issues found in 153 source files'; pytest CF1 subset all dots, exit 0 (out/ruff.out, out/mypy.out, out/pytest_CF1.out)",
    },
]
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FRESH:
        ev, st = FRESH[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
    else:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": r["status"],
                     "evidence": CARRY + r["evidence"]})
rows += NEW
verdict = "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS"
nonpass = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "CF1",
    "slice": "CF1-a",
    "round": 24,
    "verifier": "independent Haiku verifier, round 24, slice CF1-a (hub index.html, L01, L02 and their lab twins); did not build CF1",
    "pin": "23cbd6a",
    "base": "503d139",
    "previous_fragment": "/tmp/fanout-frags/CF1-a.round23.json (pin 503d139)",
    "checkout": "/tmp/verify24-CF1-a",
    "scratch": "/tmp/cf1-v/CF1-a",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 503d139..23cbd6a touches only L01.html (line 90 Remark 2.2, line 466 key-results row) and index.html (lines 122, 127, 161). Lab twins, labs, cards.json, L02.html, notation, references and tools are unchanged.",
        "Scope note on CF1-a-L01-read-full: the full page was not re-read line by line this round; the two changed hunks were read in full and every other line is byte-identical to the round-23 pin, which round 23 read in full. This is carried, not re-read.",
        "Not run this round: alternative implementations and new student-error mutants; they apply to project graders, and the lab twins and graders are unchanged since round 23 (CF1-a-r23-alt-implementations carried).",
        "Not checked: any external source (no citation changed); the full-unit page_smoke run was not repeated (only the slice pages).",
    ],
    "summary": (
        f"Slice CF1-a round 24 (pin 23cbd6a, base 503d139): {verdict}. Non-PASS: {', '.join(nonpass) or 'none'}. "
        "The round-23 FAIL on CF1-c110 is not fixed: the card still grades the two-rate claim C while L01.html line 466 grades it T. "
        "All other rows PASS: gates re-run (check_pages, check_dag, run_labs 9/9, page_smoke, verify_refs offline and live, ruff, mypy, pytest CF1), "
        "twins match embedded output, 70 lab mutants re-run (67 killed, 3 dispositioned), changed hunks re-verified, R3 and Example numbers recomputed."
    ),
}
out = ROOT / "ledgers/CF1/CF1-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n")
print(verdict, len(rows), nonpass)
