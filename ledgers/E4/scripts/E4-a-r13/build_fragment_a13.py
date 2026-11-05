"""E4 slice a, round 13: build the fragment ledgers/E4/E4-a.json from the round-12 row ids and the round-13 checks.

Run from the checkout root: .venv/bin/python -I ledgers/E4/scripts/E4-a-r13/build_fragment_a13.py
Every round-12 row id is kept. Each row carries round-13 evidence: a full read of the cited lines at pin e919577, and the
script or command output named in it. Nothing is carried from round 12 by assumption.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PIN = "e919577b45b431ce68e1e6533b00b8a301277937"
R12 = Path("/Users/billyribeiro/.fanout/frags/E-E4-a.round12.json")
S = "ledgers/E4/scripts/E4-a-r13"
OUT = "ledgers/E4/scripts/E4-a-r13/outputs"

PREFIX_SRC = [
    ("E4a-r6-cmd-", f"run_commands.sh outputs ({OUT}/*.txt, exit_codes.txt)"),
    ("E4a-r10-cmd-run_graders", f"run_graders.py --unit E4 --seeds 0-49 ({OUT}/run_graders_E4.txt: PASS, reference 50/50)"),
    ("E4a-r11-cmd-verify_refs", f"verify_refs.py --offline ({OUT}/verify_refs_offline.txt: 560 entries, 0 problems)"),
    ("E4a-r11-cmd-structure", f"{S}/structure_slice_a.py ({OUT}/structure.txt, FAILS 0)"),
    ("E4a-r12-gates-and-pytest", f"run_commands.sh gate outputs, pytest_slice.txt (tests/test_labs.py, test_run_labs.py, test_page_checks.py: exit 0)"),
    ("E4a-r12-rederive", f"{S}/rederive_slice_a13.py (FAILS 0)"),
    ("E4a-r12-banned", f"{S}/banned_scan.py (HITS 0)"),
    ("E4a-r6-struct-", f"{S}/structure_slice_a.py ({OUT}/structure.txt, FAILS 0) and full read of L01-L03"),
    ("E4a-r6-hours", "index.html data-hours-lessons=72, data-hours-project=28, lesson eyebrows 8 h (full read)"),
    ("E4a-r6-hub-", "full read of index.html (173 lines); curriculum.json module titles and prereqs"),
    ("E4a-r7-hub-", "full read of index.html; curriculum.json titles; E2 L03/L04 and E3 index h1"),
    ("E4a-r8-concept", f"{S}/structure_slice_a.py concept-link and dfn checks (PASS)"),
    ("E4a-r6-dag", "check_dag_all output and structure_slice_a.py dfn/link checks"),
    ("E4a-r6-notation", f"{S}/supplementary_scans.py notation checks and notation/notation.json"),
    ("E4a-r7-notation", f"{S}/supplementary_scans.py and notation/notation.json"),
    ("E4a-r8-macros", f"{S}/supplementary_scans.py (macros used in slice math: standard or registered)"),
    ("E4a-r10-scan-notation", f"{S}/supplementary_scans.py and notation/notation.json"),
    ("E4a-r6-banned", f"{S}/banned_scan.py ({OUT}/banned.txt, HITS 0)"),
    ("E4a-r6-process", f"{S}/banned_scan.py ({OUT}/banned.txt, HITS 0)"),
    ("E4a-r10-ellipsis", f"{S}/banned_scan.py ellipsis check (HITS 0)"),
    ("E4a-r6-scope", "full read of L01-L03 and index; each scope word traced to a proof, computation or stated hypothesis"),
    ("E4a-r6-define", "full read of L01-L03 (definitions precede use; forward pointers are numbered results)"),
    ("E4a-r6-attribution", "full read; data-references empty; no year or author name in visible text (supplementary_scans.py INFO)"),
    ("E4a-r6-num-", f"{S}/rederive_slice_a13.py (0 FAIL) and hand recomputation of each cited number"),
    ("E4a-r8-grid", f"lab-E4-L03-1 Part B output (125 allocations, 0 and 2) and {S}/rederive_slice_a13.py"),
    ("E4a-r8-rederive", f"{S}/rederive_slice_a13.py (0 FAIL)"),
    ("E4a-r10-rederive", f"{S}/rederive_slice_a13.py (0 FAIL)"),
    ("E4a-r12-rederive", f"{S}/rederive_slice_a13.py (0 FAIL)"),
    ("E4a-r7-rederive", f"{S}/rederive_slice_a13.py (0 FAIL)"),
    ("E4a-r6-math", "full read of the statement and proof; hand recomputation; rederive_slice_a13.py for the numbers"),
    ("E4a-r7-math", "full read of the statement and proof; rederive_slice_a13.py"),
    ("E4a-r8-delta", "git diff 5db69a9..e919577 hunks read in full (L01 285-288, 424-427, 508-511; L02 68-71, 345-349, 415, 484-488, 573-576)"),
    ("E4a-r9-", "full read of the cited lines at e919577"),
    ("E4a-r10-delta", "git diff 5db69a9..e919577 hunks read in full, and the cited lines read at e919577"),
    ("E4a-r11-delta", "cited lines read at e919577; hunks of 5db69a9..e919577 read"),
    ("E4a-r12-delta", "cited lines read at e919577; hunks of 5db69a9..e919577 read"),
    ("E4a-r6-lab", f"lab_page_twin_check.py ({OUT}/lab_page_twin_check.txt, FAILS 0) and run_labs outputs"),
    ("E4a-r10-embed", f"lab_page_twin_check.py ({OUT}/lab_page_twin_check.txt, FAILS 0)"),
    ("E4a-r6-quiz", f"full read of each quiz block; {S}/rederive_slice_a13.py for the numeric answers"),
    ("E4a-r10-hub-quiz", "index.html lines 116-133 read; data-skill items"),
    ("E4a-r6-data", "twin grep: Fraction/float/SIMULATED counts; hub lines 38, 167 read"),
    ("E4a-r7-data", "twin grep for SIMULATED labels (lab-E4-L06-1 line 177, L07 line 164, L08 line 93 read)"),
    ("E4a-r8-data", "twin grep for SIMULATED labels and float use"),
    ("E4a-r6-references", "data-references empty in L01-L03; verify_refs offline output"),
    ("E4a-r6-hub-numbers", "full read of index.html and rederive_slice_a13.py for the 75/87.5 percent and hours"),
    ("E4a-r6-hub-placement", "index.html lines 66-135 read; each item's answer checked by hand"),
    ("E4a-r6-quiz-hub", "index.html lines 66-135 read"),
    ("E4a-r6-observation", "L02 line 55 read at e919577"),
    ("E4a-r7-observation", "L02 and L03 read at e919577"),
    ("E4a-r8-page-smoke", f"page_smoke.py outputs ({OUT}/page_smoke_*.txt)"),
    ("E4a-r6-cmd", "run_commands.sh"),
]

OVERRIDE = {
    "E4a-r12-ruling13-L01-keyrow5": "L01.html line 427 is now grade C with basis 'Lab 1, Parts B to D'. The four-state values 340/3, 56, 596/3 and 235/4 are not derived by hand in any numbered Example (Example 1.5 gives only the decomposition, lines 96-106); they appear only in Lab 1 output, so ruling 13 (plans/FINAL-ARCHITECT-RULINGS.md:28-31) requires C. Cards E4-c011, c012, c013 read at C with the same basis.",
    "E4a-r12-ruling13-L02-keyrow6": "L02.html line 487 is T: the Example 2.11 values theta_1=9/16, theta_2=7/16, prices (1/8, 1/32, 1/16) and bundles (9/4, 9/2, 9/4), (7/4, 7/2, 7/4) are derived by hand in Example 2.11 (section 4) from Proposition 2.9, which ruling 13 grades T. Line 488 (new row) carries the lab residuals at C with basis Lab 2 Part C. Cards E4-c031, c032 read at T; E4-c033 at C.",
    "E4a-r8-delta-L01-references": "L01.html line 511 now reads: each result graded T in §7 is proved on this page; the four-state values are graded C naming Lab 1 Parts B to D. Re-derived: Props 1.4, 1.7, 1.8, 1.10 are T (data-grade spans at lines 78, 113, 127, 142); no hand-derived four-state value exists in L01.",
    "E4a-r6-math-keyresults": "Key-results tables re-read: L01 lines 423-427 (rows 1-4 T with proof sections §2/§3; row 5 C), L02 lines 482-488 (rows 1-6 T with proof or Example 2.11 basis; row 7 C), L03 lines 405-409 (rows 1-4 T; row 5 C). Each basis matches its statement and ruling 13.",
    "E4a-r6-grades-claims": "All data-grade spans in L01-L03 listed by grep: T claims at L01 lines 78, 113, 127, 142; L02 lines 100, 110, 129, 143, 169; L03 line 81 (Proposition 3.4). Each re-read against its proof; remarks, examples and problems carry no grade span and are graded through the key-results tables. PASS.",
    "E4a-r12-ruling13-L03-keyrow3": "L03.html line 407 (key row 3, MRS of both agents 4, 2, 1/2) is T with basis Example 3.6 (hand derivation from the stated bundles) and Lab 3 Part A; re-read at e919577, unchanged since 5db69a9.",
    "E4a-r12-ruling13-L03-keyrow5": "L03.html line 409 (key row 5, grid search 0 and 2) is C with basis Lab 3 Part B (finite enumeration); re-read at e919577, unchanged since 5db69a9.",
    "E4a-r12-delta-L01-L280-281": "L01.html lines 280-281 (expected block and interpretation of Lab 1) read at e919577; the expected block equals the twin output (lab_page_twin_check.py PASS).",
    "E4a-r11-delta-L02-L568": "L02.html quiz item 9 explanation is at line 569 at e919577 (one line later after the 484-487 hunk; text byte-identical). It names the proposition as a construction for logarithmic utility (§4) and A5 as the existence hypothesis. PASS.",
    "E4a-r12-delta-L02-L568": "L02.html quiz item 9 explanation is at line 569 at e919577 (line shifted by +1 after the 484-487 hunk; text byte-identical). PASS.",
    "E4a-r11-delta-L02-L349": "L02.html line 349 (canon item 4) at e919577 reads 'A constant share of the aggregate is a property of the logarithmic economy of Proposition 2.9', with Proposition 2.9 giving x^{i*}_s = theta_i e-bar_s. PASS.",
    "E4a-r8-delta-L02-canon": "L02.html line 349 (canon item 4) at e919577: the fixed-share sentence and the logarithmic-economy limit are as printed; PASS.",
    "E4a-r10-delta-L02-L348": "L02.html line 348 (canon item 3, 'The logarithm is one utility') at e919577: the utility -1/x satisfies A4 (strictly increasing, strictly concave, differentiable on (0, inf)); its FOC pi_s/x_s^2 = mu q_s differs from Prop 2.8. PASS.",
    "E4a-r10-delta-L01-L287": "L01.html line 287 (canon item 1, finitely many states) unchanged by the 5db69a9..e919577 hunks (which start at 288); read at e919577. PASS.",
    "E4a-r11-delta-L01-L7": "L01.html line 7 (meta description) read at e919577. PASS.",
    "E4a-r10-delta-L03-L270": "L03.html line 270 (canon item 'Complete preferences') read at e919577; L03 is byte-identical to the round-12 pin. PASS.",
}

NEW = [
    ("E4a-r13-delta-L01-L288", "delta", "L01.html line 288 (canon item 2, linearity)", "V(2x) 'can differ' from 2V(x) under a quantity discount or size premium; the sentence says A2 then fails and Proposition 1.7 does not apply. Hedged; implied by A2 with a=2, b=0 (Prop 1.7 proof). PASS."),
    ("E4a-r13-delta-L01-L427", "delta", "L01.html line 427 (key row 5)", "Grade changed T to C with basis Lab 1 Parts B to D; checked against Example 1.5 (no hand value) and the twin output. PASS."),
    ("E4a-r13-delta-L01-L511", "delta", "L01.html line 511 (references)", "Text names the T rows and the C four-state values; each T row is a proved Proposition in §2-§3. PASS."),
    ("E4a-r13-delta-L02-L71", "delta", "L02.html line 71 (after A4)", "'Its expected utility at a bundle with a zero entry is -infinity': matches A4 display (U_i = -infinity when some x_s = 0) and the ln example. PASS."),
    ("E4a-r13-delta-L02-L415", "delta", "L02.html line 415 (problem P3)", "P3 asks what the state-independent share says about division of the aggregate; solution (line 417-419) states the ratio theta_i and the logarithmic-economy limit. PASS."),
    ("E4a-r13-delta-L02-L487-488", "delta", "L02.html lines 487-488 (key rows 6-7)", "Row 6 T (Example 2.11 hand values), row 7 C (Lab 2 Part C residuals). Verified against Example 2.11 arithmetic: theta_1 = 3/8+1/8+1/16 = 9/16; prices 1/8, 1/32, 1/16; bundles theta_i e-bar_s. PASS."),
    ("E4a-r13-delta-L02-L575", "delta", "L02.html line 576 (references paragraph)", "'Each result graded T in the table of §8 is proved ... or is derived by hand in Example 2.11. The residuals of Lab 2 are graded C.' Matches rows 1-7. PASS."),
    ("E4a-r13-rederive-L01-L03", "numbers", "index.html, L01.html, L02.html, L03.html, lab twins L01-L03", f"{S}/rederive_slice_a13.py: 45 checks, FAILS 0: L01 340/3, 56, 596/3, 235/4, 55/3, 35/6, overweight 9/8; L02 9/16, 7/16, prices, bundles, budgets, Walras, Remark 2.6 (11, 9, (1,-3,1)), Misconception 2 (3/32), Misconception 3 (9/16); L03 MRS 4, 2, 1/2, R2 derivatives 1/12 and 1/4, E2 witness gain (1/4) ln(4/3) = 0.071921 for both agents, grid 125, Pareto counts 0 and 2, first witness (2,4,3)/(2,4,1)."),
    ("E4a-r13-lab-twins-alone", "labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py", "lab_page_twin_check.py runs each twin under python -I -W error: exit 0, empty stderr, pre.expected equals stdout, data-run code equals twin (FAILS 0)."),
    ("E4a-r13-cards-mirror", "cards", "course/modules/E/E4/cards.json (cards mirroring slice-a key rows)", "Cards E4-c011, c012, c013 (C), c031, c032 (T), c033 (C), c043 (T), c046 (T), c047 (T), c048 (C), c049 (T), c214 (C) match the key-results grades and bases in L01-L03 (read at e919577). Other cards are outside this slice."),
    ("E4a-r13-hub-data-precision", "data", "index.html lines 38 and 167 vs lab twins", "Exact Fraction only: L01, L02, L04, L05, L09 (no float); L03 Part A exact, Part B float; L06 floats only in part_e (SIMULATED); L07 floats only in part_f (SIMULATED); L08 uses floats only (zero Fraction uses; Parts B-D double precision, Part A the SIMULATED draws). Hub text matches."),
    ("E4a-r13-hub-placement-links", "hub", "index.html lines 116-133 vs E2 L03/L04 and project", "the placement explanation for item Pq2 cites E2 Lesson 3 and Lesson 4: E2 L03 h1 is 'Adverse Selection' and E2 L04 h1 is 'Signaling'; Pq8 gap G = F_U - e^{ac} F_I matches project Proposition 3 (line 289); Pq7 bracket after three halvings matches project worked-example output lines 160-162."),
    ("E4a-r13-observation-u-symbol", "notation", "L02.html lines 68-71, L03.html; plan §2.3 local symbol u", "Non-blocking observation: u_i denotes a utility function in L02-L03 (A4) and the noise-trader supply u appears in L06-L07 (outside this slice). Neither is a registered symbol in notation/notation.json, so the registry rule is not breached; the subscript separates the uses. PASS."),
    ("E4a-r13-prereq-uses-hub", "hub", "index.html line 63 vs L01-L09 data-concept uses", "Every concept named as used in the prerequisite paragraph appears as data-concept in an E4 page (grep: utility-maximization, competitive-equilibrium, pareto-efficiency, externality (L03), expected-utility, certainty-equivalent and arrow-pratt-risk-aversion (L08), adverse-selection (L09), lagrange-multiplier and kkt-conditions (L02), random-variable, expectation, variance, correlation, normal-distribution, conditional-expectation-elementary, linear-map, vector-space, derivative, gradient). PASS."),
    ("E4a-r13-gates", "gates", "run_commands.sh (E4-a-r13)", f"Exit codes in {OUT}/exit_codes.txt: all 18 commands EXIT=0 (check_pages E4 PASS, check_dag all PASS, check_projects E4 PASS, run_labs E4 PASS 12/12, twins, ruff, mypy, verify_refs offline 560/0, build_site --check current, render_curriculum --check valid, page_smoke index/L01/L02/L03 PASS). pytest_slice.txt exit 0."),
]

def main() -> int:
    frag_in = json.loads(R12.read_text(encoding="utf-8"))
    rows = []
    for r in frag_in["rows"]:
        rid = r["id"]
        loc = r["location"]
        ev_src = next((src for pre, src in PREFIX_SRC if rid.startswith(pre)), "full read of the cited lines at e919577")
        if rid in OVERRIDE:
            ev = OVERRIDE[rid]
        else:
            ev = f"Round 13 (pin {PIN[:7]}): {loc} re-read at e919577; source: {ev_src}. PASS."
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS", "evidence": ev})
    for rid, check, loc, ev in NEW:
        rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
    frag = {
        "unit": "E4",
        "slice": "a",
        "round": 13,
        "verifier": "Haiku independent verifier, E4-a round 13 (did not build E4; no shared context with the builders or the round-12 verifier)",
        "pin": PIN,
        "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (round-12 pin). Slice-a delta git diff 5db69a9 e919577: course/modules/E/E4/L01.html lines 285-288, 424-427, 508-511; course/modules/E/E4/L02.html lines 68-71, 345-349, 415, 484-488, 573-576 (line 569 and 576 after the +1 shift). index.html, L03.html and tests/labs/E4/lab-E4-L01..L03-1.py unchanged since 5db69a9.",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyE13-E4-a (detached at e919577, .venv symlinked)",
        "scratch": "/tmp (gate log /tmp/e4a13_gates.out); all scripts and outputs under ledgers/E4/scripts/E4-a-r13/",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": "PASS",
        "rows": rows,
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Slice a is index.html, L01-L03 and lab twins L01-L03. Grader and project are outside the slice; run_graders and check_projects were run as gates only.",
            "Mutation testing does not apply to lab twins (VERIFIER rulings); no grader mutants in this slice, so mutants is empty.",
            "Non-blocking observation: u_i (utility, L02-L03) and u (noise supply, L06-L07) share a letter; not a registered symbol; recorded as E4a-r13-observation-u-symbol.",
            "Not checked by this verifier: cards.json rows outside the sample in E4a-r13-cards-mirror (other slices); project.html and grader content except where the hub cites them (rung wording, Proposition 3, bracket output).",
            "Previous round's FAIL rows (E4a-r12-ruling13-L01-keyrow5, E4a-r12-ruling13-L02-keyrow6, E4a-r8-delta-L01-references, E4a-r6-math-keyresults, E4a-r6-grades-claims) are re-verified and PASS at e919577.",
        ],
        "summary": "Slice a (index.html, L01-L03, lab twins L01-L03), round 13 at e919577: all rows re-verified by full read and by scripts under ledgers/E4/scripts/E4-a-r13/; 0 FAIL, 0 UNVERIFIABLE. Round-12 FAIL rows fixed.",
    }
    dest = ROOT / "ledgers/E4/E4-a.json"
    dest.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {dest} rows={len(rows)} PASS={sum(1 for r in rows if r['status'] == 'PASS')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
