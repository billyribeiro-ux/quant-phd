"""Build ledgers/CF1/CF1-a.json (round 23) from the round-22 rows: carry rule applied, changed subjects re-verified.

Usage: .venv/bin/python -I ledgers/CF1/scripts/CF1-a-r23/build_fragment_r23.py <checkout>
"""
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
prev = json.load(open("/tmp/fanout-frags/CF1-a.round22.json", encoding="utf-8"))
CARRY = ("course/modules/CF/CF1/index.html, L01.html, L02.html, tests/labs/CF1/lab-CF1-L01-1.py, "
         "lab-CF1-L02-1.py, notation/, references/, tools/")
PREFIX = f"Carried from round 22 ({CARRY} byte-identical since the previous pin 7143726): "

RERUN = {
    "CF1-a-gate-check-pages": ("check_pages unit-wide", "tools/check_pages.py --unit CF1",
        "Re-run round 23: exit 0, 'check_pages CF1: PASS' (scripts/CF1-a-r23/out/check_pages.out)"),
    "CF1-a-gate-check-dag": ("check_dag over all units", "tools/check_dag.py --all",
        "Re-run round 23: exit 0, 'check_dag CF1: PASS' and 'check_dag AP1: PASS' (scripts/CF1-a-r23/out/check_dag.out)"),
    "CF1-a-gate-run-labs": ("run_labs for CF1 (every lab, python -I -W error)", "tools/run_labs.py --unit CF1",
        "Re-run round 23: exit 0, 'run_labs CF1: PASS (9/9)' (scripts/CF1-a-r23/out/run_labs.out)"),
    "CF1-a-gate-page-smoke": ("page_smoke for index, L01, L02 and their labs",
        "tools/page_smoke.py --unit CF1 --pages L01 L02 index",
        "Re-run round 23: exit 0; 'page_smoke modules/CF/CF1/L01.html: PASS', 'L02.html: PASS', 'index.html: PASS', "
        "'page_smoke CF1: PASS' (scripts/CF1-a-r23/out/page_smoke_L01_L02_hub.out); the full-unit run also ends 'page_smoke CF1: PASS' (out/page_smoke.out)"),
    "CF1-a-gate-lint-types": ("ruff check and format; repository mypy", "ruff check .; ruff format --check .; mypy --no-incremental",
        "Re-run round 23: ruff 'All checks passed!', '220 files already formatted'; mypy 'Success: no issues found in 153 source files' (scripts/CF1-a-r23/out/ruff.out, mypy.out)"),
    "CF1-a-gate-pytest": ("relevant pytest files (CF1 subset)", "pytest -q -k CF1 tests",
        "Re-run round 23: exit 0, all dots (scripts/CF1-a-r23/out/pytest_CF1.out)"),
    "CF1-a-cite-verify-refs": ("citation integrity offline and live for CF1",
        "tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1",
        "Re-run round 23: offline 'integrity: 560 entries, 0 problems' exit 0; live CF1 '2 of 560 entries, 0 problems' exit 0 (scripts/CF1-a-r23/out/verify_refs_offline.out, verify_refs_live_CF1.out)"),
}

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RERUN:
        check, loc, ev = RERUN[rid]
        rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
    elif rid == "CF1-a-mutants":
        rows.append({"id": rid, "check": "re-run all 70 slice-a lab mutants with python -I -W error against the twins",
                     "location": "ledgers/CF1/scripts/CF1-a-r18/run_mut18.py (run against this checkout)",
                     "status": "PASS",
                     "evidence": "Re-run round 23: 'killed 67 survived 3 total 70' (scripts/CF1-a-r23/out/mutants_all_slice_a.out). "
                                 "The three survivors are dispositioned in CF1-a-r23-survivors: PASS, equivalent or out of scope"})
    elif rid == "CF1-a-cards-L01-L02":
        rows.append({"id": rid, "check": "cards CF1-c001 to CF1-c032, CF1-c089, CF1-c090 (lessons L01 and L02) against the current lesson text",
                     "location": "course/modules/CF/CF1/cards.json; scripts/CF1-a-r23/card_delta_r23.py",
                     "status": "PASS",
                     "evidence": "Changed in-slice entries re-verified this round in CF1-a-r23-cards-changed-subjects (c001, c014, c018, c021, c024). "
                                 "The other entries of this range are byte-identical since 7143726 (card_delta_r23.py). "
                                 "CF1-c110 (new) is in CF1-a-r23-c110. Carried from round 22 for the unchanged entries: " + r["evidence"]})
    elif rid.startswith("CF1-a-"):
        rows.append({**r, "evidence": PREFIX + r["evidence"]})
    else:
        rows.append(r)

new = [
 {"id": "CF1-a-r23-delta", "check": "delta since the previous pin 7143726 for every slice file",
  "location": "git diff --quiet 7143726 503d139 -- <slice files>; scripts/CF1-a-r23/card_delta_r23.py",
  "status": "PASS",
  "evidence": "index.html, L01.html, L02.html, both twins, notation/, references/, tools/ and course/templates: identical (git diff --quiet). Changed in the slice: cards.json only (c001, c014, c018, c021, c024 changed; c110 added). "
              "The fragment file named round22 records round 18 and pin 7143726; d160ac3 (the round-22 pin by commit history) was also checked: since d160ac3 only c014 changed and c110 was added."},
 {"id": "CF1-a-r23-cards-changed-subjects", "check": "changed cards CF1-c001, c014, c018, c021, c024 against the lesson text",
  "location": "course/modules/CF/CF1/cards.json; L01.html lines 55 (conventions), 330-341 (Section 7); L02.html lines 56, 90, 122 (Definitions 1.1, 2.1, 3.1)",
  "status": "PASS",
  "evidence": "CF1-c021 back 'OCF_t = EBIT_t - tau x EBIT_t + D_t ...' equals L02.html Definition 2.1 (line 90). CF1-c024 back equals Definition 3.1 (line 122: NWC from operating lines; I_t = NWC_t - NWC_(t-1); cash effect -I_t). "
              "CF1-c018 back equals Definition 1.1 (line 56); 'Section 1 gives the rules' matches L02.html line 71 ('Three rules decide which flows belong'). "
              "CF1-c001 back matches L01 Definition 1.1 and 'Flows fall at period ends' (L01.html line 55). CF1-c014 back: 'Section 7, third misconception' is the loan-rate item (L01.html line 341, third item of Section 7). "
              "Grades T to C for c001, c018, c021, c024: definitions are stipulations, not proofs, and the lesson legend (Ttheorem / Csingle study or convention) makes C the honest grade; the basis states it. c014 grade unchanged (C)."},
 {"id": "CF1-a-r23-c110", "check": "card CF1-c110 (new, L01) grade agrees with the lesson grade table",
  "location": "course/modules/CF/CF1/cards.json CF1-c110; course/modules/CF/CF1/L01.html line 466 (grade table row)",
  "status": "FAIL",
  "evidence": "The card text is accurate: Assumption 4.0 needs one rate; the proof of Proposition 4.1 does not apply with two rates; the decision can change with the rate (Remark 4.3; Problem R3). "
              "Problem R3 arithmetic checks: -1 + 1.05/1.06 = -0.009434 and -1 + 1.05/1.03 = +0.019417 (scripts/CF1-a-r23/recompute_r23.py). "
              "But the card grade is C with basis 'Assumption 4.0 and Remark 4.3; Problem R3', while L01.html line 466 grades the same claim ('With different borrowing and lending rates the decision on one project depends on which rate applies (Problem R3)') as T with basis 'Problem R3'. The card and the lesson disagree on the grade of one claim.",
  "fix": "Builder decision: set CF1-c110 to grade T with basis 'Problem R3' to match L01.html line 466 (the claim is exact arithmetic on the page), or change L01.html line 466 to C with a stated basis; then re-run tools/build_site.py --check and tools/render_curriculum.py if cards are generated from the curriculum source."},
 {"id": "CF1-a-r23-numbers", "check": "numbers in the changed card text and the lesson prose recomputed",
  "location": "scripts/CF1-a-r23/recompute_r23.py (python -I -W error)",
  "status": "PASS",
  "evidence": "Recomputed: L02 Section 6 working-capital PV at 8% = -130.4952 (rounds to -130.50); L02 NPV at 8% 534.24, minus 2000 = -1465.76; L02 M3 incremental NPV 82.6446 (lesson 82.64), charged -417.3554 (lesson -417.3553... and -417.36 to the cent); "
              "L01 Example 1.2 unrounded 13452.6152 (13,452.62; lesson 13,452.615 unrounded); rounded-term sum 13452.62; Remark 1.3 rounded-factor sum 13452.26; A(0.10,3) = 2.486852 and 2.487 with 0.7513; Example 5.3 298.42; M1 4.1322 (4.13); M2 19.7658 (19.77); Section 7 E 200 and -83.33; R3 -0.009434 and +0.019417. Every value matches the printed text."},
 {"id": "CF1-a-r23-lab-twins", "check": "lab twins re-run and compared with the embedded output",
  "location": "tests/labs/CF1/lab-CF1-L01-1.py; tests/labs/CF1/lab-CF1-L02-1.py; course/modules/CF/CF1/L01.html line 308",
  "status": "PASS",
  "evidence": "Both twins exit 0 under python -I -W error (scripts/CF1-a-r23/out/twin_L01.out, twin_L02.out). The twin line 'balance at date 5, in dollars: 0.000000' matches L01.html line 308. run_labs CF1 PASS (9/9). Twins byte-identical since 7143726."},
 {"id": "CF1-a-r23-alt-implementations", "check": "archived alternative correct implementations of the two labs re-run",
  "location": "ledgers/CF1/scripts/CF1-a-r17/alts/*.py; ledgers/CF1/scripts/CF1-a-r18/alts/*.py",
  "status": "PASS",
  "evidence": "The L02 alternatives alt_r17_a, alt_r17_b, alt_r17_c and alt_r18_c print stdout identical to the L02 twin (md5 ac6ab3df...). alt_r18_b (Horner NPV, geometric annuity) prints stdout identical to the L01 twin (md5 d0b56fe9...). "
              "alt_r18_a (fsum, L01) differs in one line only: 'balance at date 5, in dollars: -0.000000' against the twin's '0.000000'. That is a floating-point sign of zero; the line 'the balance ends at zero to within 1e-6 dollars: True' is the same in both, and no lesson sentence quotes the balance line. PASS."},
 {"id": "CF1-a-r23-survivors", "check": "the three surviving slice-a lab mutants are out of scope or equivalent",
  "location": "ledgers/CF1/mutants/CF1-a-r9/r9_m07_no_tax_credit.py; CF1-a-r11/n05_l02_identity_check_stubbed_true.py; CF1-a-r17/r17_probe_l02_identity_exact_equality.py",
  "status": "PASS",
  "evidence": "r9_m07 (no tax credit): the Lab 2 seed has EBIT of 1100, 1800, 800 and 600 (lab table), all positive, so the credit branch is not exercised; L02.html Remark 2.4 says the lab 'does not test any firm's tax position' and claims no test of the branch. Out of scope. "
              "n05 (identity check replaced by True): equivalent over the lab's input space. Proposition 2.2 is exact algebra; a sweep over 80,000 (revenue, cost) pairs drawn from the lab's ranges with its constants gives worst deviation 0.0 and 0 failures (scripts/CF1-a-r23/identity_sweep.py). "
              "The lesson sentence 'The lab checks each year's operating cash flow against Proposition 2.2' (L02.html line 51) is true of the code as written, and no input can distinguish the stub, so the mutant is equivalent. "
              "r17_probe (exact float equality instead of 1e-6): the lab prints the same True on its seed; L02.html line 272 says 'confirm ... numerically' and states no tolerance. Out of scope. PASS for all three."},
 {"id": "CF1-a-r23-check-liveness", "check": "the printed True checks in the L02 lab can fail on a wrong shield",
  "location": "tests/labs/CF1/lab-CF1-L02-1.py (shield check); course/modules/CF/CF1/L02.html line 272",
  "status": "PASS",
  "evidence": "The shield check compares the OCF difference with and without depreciation against depreciation x tax rate; the r18_m05 mutant (compares OCF, not the difference) is KILLED in the re-run (out/mutants_all_slice_a.out). The identity check cannot fail (see CF1-a-r23-survivors); L02.html line 272 does not claim that it can."},
]
rows = rows + new

fragment = {
    "unit": "CF1", "slice": "CF1-a", "round": 23,
    "verifier": "independent Haiku verifier, round 23, slice CF1-a (hub index.html, L01, L02 and their lab twins); did not build CF1 and shares no context with the builders",
    "pin": "503d139", "base": "7143726", "previous_fragment": "/tmp/fanout-frags/CF1-a.round22.json (records round 18 and pin 7143726)",
    "checkout": str(root), "scratch": "/tmp/CF1-a-r23-scratch",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [], "freshness_flags": [],
    "notes": [
        "Delta: cards.json only (CF1-c001, c014, c018, c021, c024 changed; CF1-c110 added); all slice page and lab files byte-identical since 7143726. No new student-error mutants: the slice is lesson pages and lab twins (lab mutants are demonstrations under the architect ruling; the project graders are not in this slice).",
        "Changed subjects re-verified (CF1-a-r23-cards-changed-subjects); the new card CF1-c110 fails on grade (CF1-a-r23-c110).",
        "Equivalent-mutant proof for n05 in CF1-a-r23-survivors; sweep in scripts/CF1-a-r23/identity_sweep.py.",
    ],
    "summary": "Slice CF1-a round 23 (pin 503d139, delta from 7143726): FAIL, one row. CF1-a-r23-c110: the new card CF1-c110 is graded C while L01.html line 466 grades the same claim T. All other rows PASS: gates re-run (check_pages, check_dag, run_labs 9/9, page_smoke, ruff, mypy, pytest CF1, verify_refs offline and live), 70 mutants re-run (67 killed, 3 dispositioned PASS), changed cards re-verified, numbers recomputed.",
}
out = root / "ledgers/CF1/CF1-a.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "verdict", fragment["verdict"], "written", out)
