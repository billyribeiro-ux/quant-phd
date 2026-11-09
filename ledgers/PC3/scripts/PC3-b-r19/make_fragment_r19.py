"""Round 19 PC3-b fragment builder: carries round-18 PASS rows whose subjects are byte-identical, re-verifies the rest."""
import json
import re
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE19-PC3-b")
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-PC3-b.round18.json").read_text(encoding="utf-8"))
OUT = "ledgers/PC3/scripts/PC3-b-r19/out"
PIN_PREV = "50559266"

RE_ROWS = {
    "gate-run-labs-unit": ("2.5-labs", "tools/run_labs.py --unit PC3",
        f"Re-run at cd4dd7df: 'run_labs PC3: PASS (9/9)', exit 0 ({OUT}/run_labs_unit.out)."),
    "gate-check-pages": ("2.9-prose", "tools/check_pages.py --unit PC3 ; tools/check_pages.py --all",
        f"Re-run: 'check_pages PC3: PASS' exit 0 for --unit ({OUT}/check_pages_unit.out) and --all ({OUT}/check_pages_all.out)."),
    "gate-check-dag": ("2.9-DAG", "tools/check_dag.py --all",
        f"Re-run: 'check_dag LX1: PASS', 'check_dag LX2: PASS', 'check_dag PC3: PASS', exit 0 ({OUT}/check_dag_all.out). The DAG and concept rows for L04-L06 are re-read in the carried rows below."),
    "gate-check-projects": ("2.6-structure", "tools/check_projects.py --unit PC3",
        f"Re-run: 'check_projects PC3: PASS', exit 0 ({OUT}/check_projects_unit.out). Project rows belong to slices c and d."),
    "gate-page-smoke-slice": ("2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)",
        f"Re-run alone: L04, L05 and L06 each 'PASS', 'page_smoke PC3: PASS', exit 0 ({OUT}/page_smoke_slice.out). The shell has no 'timeout' builtin, so the run used no timeout wrapper."),
    "gate-ruff-mypy-twins": ("2.5-labs", "ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; ruff check .; ruff format --check .; mypy --no-incremental",
        f"ruff check tests/labs/PC3 'All checks passed!' ({OUT}/ruff_check_twins.out); ruff format --check tests/labs/PC3 '9 files already formatted' ({OUT}/ruff_format_twins.out); repo ruff check 'All checks passed!' ({OUT}/ruff_check_repo.out); repo format '553 files already formatted' ({OUT}/ruff_format_repo.out); mypy --no-incremental 'Success: no issues found in 385 source files' exit 0 ({OUT}/mypy.out)."),
    "gate-pytest-lab-tooling": ("2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_docs_figures.py -q",
        f"Re-run: all dots, exit 0 ({OUT}/pytest_labs_tooling.out)."),
    "gate-verify-refs-offline": ("2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit PC3 (live)",
        f"Re-run: 'offline integrity: 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_offline.out); live 'live re-verification of PC3: 2 of 560 entries, 0 problems', exit 0 ({OUT}/verify_refs_unit_live.out)."),
    "gate-run-graders-unit": ("2.6-structure", "tools/run_graders.py --unit PC3 --seeds 0-49",
        f"Re-run: 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.6 s)', exit 0 ({OUT}/run_graders_unit.out). Project graders belong to slices c and d."),
    "gate-fetch-data-check": ("2.8-data", "tools/fetch_data.py --check",
        f"Re-run: 'fetch_data: 3 datasets, 0 problems', exit 0 ({OUT}/fetch_data_check.out). No L04-L06 page reads a data file (data-files lists empty for these pages)."),
    "gate-build-site-check": ("2.9-prose", "tools/build_site.py --check",
        f"Re-run: 'site data current: 6 outputs', exit 0 ({OUT}/build_site_check.out)."),
    "gate-render-curriculum-diff": ("2.9-prose", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
        f"Re-run: 'wrote curriculum/curriculum.json and CURRICULUM.md', exit 0; the git diff over the two generated files is empty, exit 0 ({OUT}/render_curriculum_diff.out). git status shows no tracked file changed by the run."),
    "r16-gates-ruff-format-repo": ("2.5-labs", "ruff check . ; ruff format --check . (repo)",
        f"Re-run: 'All checks passed!' exit 0 and '553 files already formatted' exit 0 ({OUT}/ruff_check_repo.out, {OUT}/ruff_format_repo.out)."),
    "r16-gate-check-dag-all": ("2.9-DAG", "tools/check_dag.py --all",
        f"Re-run: exit 0, PC3 PASS ({OUT}/check_dag_all.out)."),
    "twin-run-alone-L04-L06": ("2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py",
        f"Each twin run alone as 'python3 -I -W error <twin>' from the checkout: exit 0 for all three, stderr 0 bytes, stdout 52, 25 and 21 lines ({OUT}/pc3b_r19_lab-PC3-L04-1.py.out, {OUT}/pc3b_r19_lab-PC3-L05-1.py.out, {OUT}/pc3b_r19_lab-PC3-L06-1.py.out; rc and stderr size from the shell)."),
    "twin-page-code-equals-twin": ("2.5-labs", "L04.html, L05.html, L06.html data-run blocks vs the three twins",
        f"ledgers/PC3/scripts/PC3-b-r19/twin_check.py at cd4dd7df: 'L04 lab-PC3-L04-1: page_code_eq_twin=True ... L05 ... True ... L06 ... True', 'ALL OK' ({OUT}/twin_check_r19.out)."),
    "twin-expected-equals-stdout": ("2.5-labs", "L04.html, L05.html, L06.html pre.expected vs twin stdout",
        f"Same run ({OUT}/twin_check_r19.out): expected_eq_stdout=True for L04 (52 lines), L05 (25), L06 (21)."),
    "r16-sim-independent": ("2.5-labs", "ledgers/PC3/scripts/PC3-b-r16/sim_game_independent.py",
        f"Re-run at cd4dd7df with python3 -I: 'mid == 10000 - 10*I_{{t-1}} at every turn, seeds 0..499: True'; 'P&L identity, seeds 0..499: True'; 'largest |inventory| over seeds 0..499: 8 (limit 10)' ({OUT}/sim_game_independent_r19.out)."),
    "r16-numbers-rederivation": ("2.2-numbers", "all numbers in L04-L06 prose, quiz, key results and problems",
        f"Re-run this round: ledgers/PC3/scripts/PC3-b-r17/verify_numbers_r17.py -> {OUT}/verify_numbers_r17_rerun.out (no FAIL), ledgers/PC3/scripts/PC3-b-r18/verify_numbers_r18.py -> {OUT}/verify_numbers_r18_rerun.out ('SUMMARY pass=24 fail=0'), and ledgers/PC3/scripts/PC3-b-r19/verify_numbers_r19.py -> {OUT}/verify_numbers_r19.out (exact Fractions: A(10%)=3310/1331, break-even 399300/331, NPV(1200)=-105000000/1331, NPV(1300)=1550000000/1331, rounded break-evens 1164.1005, 1206.3444, 1249.0469, differences 42.2439 and 42.7025, slope 21.2366, M3 33275/331, m* ratio 0.7540)."),
    "r16-twin-page-and-run": ("2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py; the three pages",
        f"Re-run this round: twin exit 0 and page code equals twin for all three ({OUT}/twin_check_r19.out; {OUT}/run_labs_unit.out)."),
    "r16-prose-scan": ("2.9-prose", "ledgers/PC3/scripts/PC3-b-r16/prose_scan.py on L04, L05, L06",
        f"Re-run this round with the copy ledgers/PC3/scripts/PC3-b-r19/prose_scan.py: banned 0, process 0, ellipsis 0 for L04 (scope sentences 39), L05 (60) and L06 (41) ({OUT}/prose_scan_r19.out). The scope sentences are the round-18 set; none is new."),
    "r18-counts-and-judgement": ("2.7-cards", "course/modules/PC/PC3/cards.json (L04-L06: 111 cards)",
        f"Re-run this round: ledgers/PC3/scripts/PC3-b-r19/cards_slice.py and cards_scan_r19.py -> {OUT}/cards_scan_r19.out and {OUT}/cards_L04_L06.txt: 187 cards in the unit, L04 40, L05 30, L06 41 (111); no duplicate ids or fronts. Judgement carried from round 18: PC3-c192 and PC3-c064 ask different questions."),
    "card-duplicate-scan": ("2.7-cards", "course/modules/PC/PC3/cards.json (187 PC3 cards)",
        f"Re-run this round ({OUT}/cards_scan_r19.out): 187 cards, 'dup ids []', 'dup fronts []', 'dup backs []'."),
    "card-cite-empty": ("2.7-cards", "cards.json 'cite' fields, all 187 PC3 cards",
        f"Re-run this round ({OUT}/cards_scan_r19.out): 'cite nonempty []': no PC3 card carries a registry key."),
    "card-number-in-lesson": ("2.7-cards", "cards.json numbers vs own lesson text, L04-L06 cards",
        f"Re-run this round by a script over all 111 L04-L06 cards (front and back, numbers vs the stripped lesson text, {OUT}/cards_scan_r19.out): no number in a card is absent from its own lesson, except 0 to 3, which are symbols or indices. The changed cards PC3-c067 (5 ... 9990, 9980, 40, 30 appear in L04.html Remark 2.4 and E3) and PC3-c191 (u*, I, m, A, l, h defined in L06.html Proposition 3.1 and 3.2) pass."),
    "card-key-results-agreement": ("2.7-cards", "cards.json L04-L06 entries vs key-results tables (L04.html lines 620-625, L05.html lines 474-477, L06.html lines 452-454)",
        "Re-read this round: L04 key results (Proposition 2.2, 2.3, 3.1, Corollary 3.3, Proposition 4.1) agree with cards PC3-c066, c068, c069, c071, c073; L05 key results (Proposition 3.2; Proposition 3.3 appends and 2n bound; Problem P3; seed-5 agreement) agree with PC3-c090, c091, c182, c095, c101; L06 key results (Proposition 3.1, Proposition 3.2, the 10-percent break-even) agree with PC3-c110, c111, c147. The key-result row for Corollary 3.3 in L04 and the L06 Corollary 3.3 card are consistent with the sentence on the page."),
    "card-full-scan-L04": ("2.7-cards", "course/modules/PC/PC3/cards.json: the 40 L04 cards",
        f"Read this round, card by card (front and back, {OUT}/cards_L04_L06.txt): definitions, assumptions A1-A6, Propositions 2.2, 2.3, 3.1, 4.1, Remarks 1.2, 2.4, 3.4, 4.2, Example 1.3, Problems R1, R3, M1, E1-E3 and the seed-0 and seed-1 lab cards agree with the page and the printed lab output (out/pc3b_r19_lab-PC3-L04-1.py.out). PC3-c067 and PC3-c191 are re-verified in r19-card-PC3-c067-seed0 and r18-card-PC3-c191-when-degenerate. Duplicates: none. PASS."),
    "card-full-scan-L05": ("2.7-cards", "course/modules/PC/PC3/cards.json: the 30 L05 cards",
        f"Read this round, card by card ({OUT}/cards_L04_L06.txt): Definitions 1.1, 1.3, 3.1, Propositions 2.1, 3.2, 3.3, Remarks 2.2, 3.4, 3.6, Example 3.5, Problems M2, P3 and the seed-5 cards agree with the page and the printed lab output ({OUT}/pc3b_r19_lab-PC3-L05-1.py.out: naive 1351 and 5239; deque 354, 382, 387; pushes 200; pops 199 at window 8, 194 at window 200; five edge checks True). The deque-count and P3 claims are recomputed in r19-L05-deque-P3-bounds. PASS."),
    "card-full-scan-L06": ("2.7-cards", "course/modules/PC/PC3/cards.json: the 41 L06 cards",
        f"Read this round, card by card ({OUT}/cards_L04_L06.txt): Propositions 1.1, 2.1, 3.1, 3.2, Corollary 3.3, Remarks 2.2, 4.3, Example 4.2, Problems M2, M3, E1-E3, R3 and the lab-number cards agree with the page and {OUT}/pc3b_r19_lab-PC3-L06-1.py.out (forward payoff 0 and 100 cents; NPV -12513148 at 200 units; 4894816 at 1600). PC3-c191 re-verified in r18-card-PC3-c191-when-degenerate. PASS."),
    "L04-scope-and-banned-phrases": ("2.9-prose", "L04.html visible prose; ledgers/PC3/scripts/PC3-b-r19/prose_scan.py at cd4dd7df",
        f"Re-run at cd4dd7df ({OUT}/prose_scan_r19.out): 'L04 banned=0 process=0 ellipsis=0 scope_sentences=39'. The one changed sentence (line 127, 'Proposition 3.1 and Example 3.2 use it.') has no scope word and no banned phrase. The 39 scope sentences are the round-18 set, none new."),
    "notation-registry-L04-L06": ("2.4-notation", "course/modules/PC/PC3/L04.html line 127 (x^{+}); L06.html line 60; notation/notation.json",
        "Re-verified this round against the changed line 127. notation/notation.json is byte-identical since the round-18 pin and has 8 program-wide symbols (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q) plus macros; it has no positive-part symbol, so x^{+} reuses no registered meaning. x^{+} is defined locally in L04 line 127 before its first use at line 131 (Proposition 3.1), and L06 line 60 restates the same definition in its hypotheses, with the same meaning. The notation.json 'about' says letters with conventional local meaning are defined in each lesson, which is what is done. PASS."),
    "r18-L04-section3-math": ("2.4-mathematics", "L04.html lines 127-160 (positive-part sentence; Section 3 statements and proofs)",
        f"Re-derived this round: Proposition 3.1 closed form (enumeration of the three arrival cases, sum (1-p)h - p[(v-a)^+ + (b-v)^+]); Example 3.2 values 5, 0 and 5/2 at v=10000, 10020, 9985; Corollary 3.3 E = h/2 - (v-a)/2 zero iff v=a+h; Remark 3.4 h/2 = (2h)/4. Output: {OUT}/verify_numbers_r18_rerun.out (SUMMARY pass=24 fail=0) and {OUT}/verify_numbers_r19.out. The sentence at line 127 now names only Proposition 3.1 and Example 3.2, which use x^{{+}} (lines 131 and 145)."),
    "r18-L04-positive-part-sentence": ("2.4-mathematics / 2.9-prose (scope word, notation)", "course/modules/PC/PC3/L04.html line 127",
        "FIXED at cd4dd7df. Line 127 now reads 'Write \\(x^{+}=\\max(x,0)\\) for the positive part of a real number \\(x\\). Proposition 3.1 and Example 3.2 use it.' Checked: x^{+} appears in the Proposition 3.1 statement (line 131: (v-a)^{+}, (b-v)^{+}) and in Example 3.2 (line 145: (v-10010)^{+}, (9990-v)^{+}). Corollary 3.3 and Remark 3.4 are not named, so the sentence is true of the section as written. The round-18 'statements of this section' claim is gone (git diff 50559266..cd4dd7df line 127 hunk)."),
    "r18-card-PC3-c191-when-degenerate": ("2.7-cards", "course/modules/PC/PC3/cards.json lines 1578-1579 (PC3-c191), against L06.html lines 131-137",
        f"FIXED at cd4dd7df. The front now asks 'What condition on [l, h] is sufficient to fix the sign of the NPV?' and the back says 'A sufficient condition: ... h < u* or l > u* ... The condition is sufficient, not necessary: a zero-width range with l = h = u* also fixes the sign, at zero.' Verified: the page's Corollary 3.3 (L06.html line 132) says 'The sign is fixed when the whole interval lies strictly on one side of u*, that is, when h<u* or l>u*'; the proof (line 137) gives NPV(u) = mA(u-u*), so NPV is zero on [l,h] when l=h=u* (Proposition 3.2 allows l_j=h_j, so that range is admissible). Sufficiency and the zero-width exception are both true (recomputed in {OUT}/verify_numbers_r19.out and by the algebra). PASS."),
    "card-PC3-c187-articulation": ("2.7-cards", "cards.json PC3-c187 (L06) vs L06.html line 75 and course/modules/AC/AC1/L03.html line 57",
        "Carried from round 18 (cards.json entry PC3-c187 and L06.html byte-identical since the previous pin 50559266; the delta does not touch either): the card states the balance-sheet cash identity that L06.html line 75 states."),
}

NEW_ROWS = [
    {"id": "r19-delta-scope", "check": "2.9-prose / 2.10-delta", "location": "git diff -U0 50559266 cd4dd7df over the slice files",
     "status": "PASS",
     "evidence": f"Command: git diff -U0 50559266 cd4dd7df -- course/modules/PC/PC3/L04.html course/modules/PC/PC3/L05.html course/modules/PC/PC3/L06.html course/modules/PC/PC3/cards.json tests/labs/PC3 notation references course/modules/PC/PC3/project.html > {OUT}/delta_slice_b_r19.diff. Hunks: L04.html @@ -127 +127 (one line, the positive-part sentence); cards.json @@ -569 +569 (PC3-c067 front) and @@ -1578,2 +1578,2 (PC3-c191 front and back). L05.html, L06.html, tests/labs/PC3, notation/, references/ and project.html: 0 lines changed. Every hunk was read in full. The commit cd4dd7df also changes plans/FINAL-ARCHITECT-RULINGS.md, plans/M5-open-items.md and files of other units; none is in the slice or a PC3 lesson, so no PC3-b row depends on them. The round-18 pin's line numbers are unchanged because every hunk is a one-line replacement."},
    {"id": "r19-card-PC3-c067-seed0", "check": "2.7-cards / 2.2-numbers / 2.5-labs", "location": "cards.json line 569 (PC3-c067) vs L04.html Remark 2.4 (lines 120-122) and Problem E3 (lines 582-585); tests/labs/PC3/lab-PC3-L04-1.py Part 1",
     "status": "PASS",
     "evidence": f"New front 'Remark 2.4 (seed 0, SIMULATED). What is the difference between marking the units at the settlement value and at the last quote's mid?'. Back: difference = inventory x (mid - settlement); seed 0 final mid 9990, settlement 9980, one unit held, mid gives 40 and settlement 30. Lab output ({OUT}/pc3b_r19_lab-PC3-L04-1.py.out): turn 20 quote 9980 bid and 10000 ask (mid 9990), 'inventory at the end = 1 units', 'cash flow = -9950 cents', 'settlement fair value v_20 = 9980 cents', 'P&L = cash + inventory mark = 30 cents'. Hence mid marking = -9950 + 9990 = 40 and difference 10 = 1 x (9990 - 9980). Remark 2.4 and E3 state the same numbers. The grade C fits single-path simulated evidence (BLUEPRINT section 3, grade C), and basis names Lab 1 Part 1 with SIMULATED, as the plan requires. PASS."},
    {"id": "r19-card-PC3-c191-label", "check": "2.7-cards / 2.3-grades", "location": "cards.json lines 1578-1581 (PC3-c191) vs L06.html Corollary 3.3 (line 131 title, line 132 statement)",
     "status": "PASS",
     "evidence": "The front label '(the sign is fixed on one side)' is not the page's corollary title ('a range that straddles the break-even does not fix the sign'), but the page's statement at line 132 contains the one-side sentence ('The sign is fixed when the whole interval [l,h] lies strictly on one side of u*, that is, when h<u* or l>u*'), and the card's content matches it. The basis 'Corollary 3.3, a consequence of Propositions 3.1 and 3.2' matches the page's 'This is a consequence of the two propositions'. No claim is attributed to Corollary 3.3 that the page does not make. Not a failure."},
    {"id": "r19-L06-numbers-recheck", "check": "2.2-numbers", "location": "L06.html lines 154, 306, 325, 362, 398, 412, 437; Example 4.2 line 149; cards PC3-c115, c116, c121, c124, c125, c126, c127, c147, c148, c149, c150, c179",
     "status": "PASS",
     "evidence": f"Own script ledgers/PC3/scripts/PC3-b-r19/verify_numbers_r19.py (exact Fraction arithmetic) -> {OUT}/verify_numbers_r19.out: A(8%) = 2.5770970 (2.577096987...), A(10%) = 3310/1331, A(12%) = 2.4018313; break-evens 1164.1005, 1206.3444, 1249.0469 (rounded 4 dp); 1206.3444-1164.1005 = 42.2439 (42.24) and 1249.0469-1206.3444 = 42.7025 (42.70); slope (1249.0469-1164.1005)/4 = 21.2366 (21.24); break-even 10% = 399300/331 (1206.34); NPV(1200, 10%) = -105000000/1331 = -78888.05; NPV(1300) = 1550000000/1331 = 1164537.94; NPV(200) = -12513148.01 (exact -16655000000/1331, printed -12513148); NPV(1600) = 4894815.93 (printed 4894816); M3 u* = 33275/331 = 100.5287 (about 100.53); R3 margin ratio 0.75396 (0.7540), fall 24.6 percent; M2 NPV 500/121 = 4.1322. Every displayed value agrees with the page and with the printed lab output ({OUT}/pc3b_r19_lab-PC3-L06-1.py.out). PASS."},
    {"id": "r19-L05-deque-P3-bounds", "check": "2.2-numbers / 2.4-mathematics", "location": "L05.html Problem P3 (line 408-412, solution), Proposition 3.3 (lines 136-142), Remark 3.4 (line 147), lab twin tests/labs/PC3/lab-PC3-L05-1.py",
     "status": "PASS",
     "evidence": f"Own script ledgers/PC3/scripts/PC3-b-r19/deque_p3_r19.py ({OUT}/deque_p3_r19.out), on the page's pseudocode order (while-loop, append, expiry, output): P3 holds for every strictly increasing sequence with 1 <= n <= 30 and every 1 <= k <= n (n-1 while-loop tests; k=1 included, because the expiry runs after the loop); 2000 random sequences: outputs equal the window maxima, comparisons <= 2n, pushes = n, pops <= n; Remark 3.4 example: step k+1 removes k entries, all by the while loop. Lab seed-5 counts ({OUT}/pc3b_r19_lab-PC3-L05-1.py.out) agree: 1351 and 5239 naive, 354, 382 and 387 deque comparisons, pushes 200, pops 199 (window 8) and 194 (window 200). PASS."},
]

BY_ID = {r["id"]: r for r in prev["rows"]}
FILES_BY_PREFIX = [
    (("L04",), "course/modules/PC/PC3/L04.html (the cited passage; the one changed line of the file, 127, is outside it)"),
    (("L05",), "course/modules/PC/PC3/L05.html"),
    (("L06",), "course/modules/PC/PC3/L06.html"),
    (("lab-L04",), "course/modules/PC/PC3/L04.html and tests/labs/PC3/lab-PC3-L04-1.py (outside the changed line 127)"),
    (("lab-L05",), "course/modules/PC/PC3/L05.html and tests/labs/PC3/lab-PC3-L05-1.py"),
    (("lab-L06",), "course/modules/PC/PC3/L06.html and tests/labs/PC3/lab-PC3-L06-1.py"),
]


def core(ev: str) -> str:
    pat = re.compile(r"^Carried from round \d+ \((?:[^()]|\([^()]*(?:\([^()]*\))?[^()]*\))*\):?\s*")
    while True:
        new = pat.sub("", ev, count=1)
        if new == ev:
            return ev.strip()
        ev = new


def carry_files(rid: str, loc: str) -> str:
    for keys, files in FILES_BY_PREFIX:
        if any(rid.startswith(k) for k in keys):
            return files
    if "cards.json" in loc or "card" in rid.lower():
        return "course/modules/PC/PC3/cards.json (the cited entries; the changed entries are PC3-c067 and PC3-c191 only)"
    if "notation" in loc or "references" in loc:
        return "notation/notation.json and references/references.json"
    if "L04" in loc:
        return "course/modules/PC/PC3/L04.html (the cited passage; line 127 is outside it)"
    if "L05" in loc:
        return "course/modules/PC/PC3/L05.html"
    if "L06" in loc:
        return "course/modules/PC/PC3/L06.html"
    if "project" in loc:
        return "course/modules/PC/PC3/project.html (unchanged since 50559266)"
    if "tests/labs" in loc or "lab-PC3" in loc:
        return "tests/labs/PC3 twins (unchanged since 50559266)"
    return "the cited files (byte-identical since 50559266)"


rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RE_ROWS:
        check, loc, ev = RE_ROWS[rid]
        rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})
        continue
    if rid in ("r18-L04-positive-part-sentence", "r18-card-PC3-c191-when-degenerate", "card-full-scan-L06", "card-full-scan-L04", "card-full-scan-L05", "L04-scope-and-banned-phrases", "card-full-scan-L06"):
        continue
    if rid in ("notation-registry-L04-L06", "r18-L04-section3-math", "card-duplicate-scan", "card-number-in-lesson", "card-cite-empty", "card-key-results-agreement", "r18-counts-and-judgement", "r16-sim-independent", "r16-numbers-rederivation", "r16-twin-page-and-run", "r16-prose-scan", "card-PC3-c187-articulation"):
        continue
    if rid.startswith("gate-") or rid.startswith("twin-") or rid.startswith("r16-gate"):
        continue
    if r["status"] != "PASS":
        raise SystemExit(f"unhandled non-PASS row {rid}")
    if rid in ("r17-L06-part1-prose-five-spot-values",):
        pass
    files = carry_files(rid, r["location"])
    ev = (f"Carried from round 18 ({files} byte-identical since the previous pin {PIN_PREV}; "
          f"the round-19 delta (L04.html line 127, cards.json PC3-c067 and PC3-c191) does not touch the cited subject): "
          + core(r["evidence"]))
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})

# rows re-verified above (kept ids, in round-18 order) must be inserted at the position of their round-18 id
ordered = []
new_by_id = {r["id"]: r for r in rows}
for r in prev["rows"]:
    rid = r["id"]
    if rid in new_by_id:
        ordered.append(new_by_id[rid])
    elif rid in ("r18-L04-positive-part-sentence", "r18-card-PC3-c191-when-degenerate", "card-full-scan-L06", "card-full-scan-L04", "card-full-scan-L05", "L04-scope-and-banned-phrases"):
        ordered.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RE_ROWS[rid][2] if rid in RE_ROWS else ""})
# fix any rows that have no RE_ROWS evidence (should not happen)
for o in ordered:
    if not o["evidence"]:
        raise SystemExit("empty evidence for " + o["id"])
ordered += NEW_ROWS
ids = [o["id"] for o in ordered]
assert len(ids) == len(set(ids)), "duplicate ids"
missing = [r["id"] for r in prev["rows"] if r["id"] not in ids]
assert not missing, missing

fragment = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 19,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 19 (did not build PC3)",
    "pin": "cd4dd7df",
    "base": "50559266 (round-18 pin). Delta 50559266..cd4dd7df in this slice: L04.html line 127 (one-line change: 'Proposition 3.1 and Example 3.2 use it.'); cards.json line 569 (PC3-c067 front) and lines 1578-1579 (PC3-c191 front and back). L05.html, L06.html, tests/labs/PC3, notation/, references/ and project.html are unchanged (git diff -U0 empty).",
    "checkout": str(ROOT),
    "scratch": str(ROOT / OUT),
    "verified_at": "2026-11-09T05:50:00+00:00",
    "verdict": "PASS",
    "rows": ordered,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b = L04, L05, L06 lesson pages, the lab twins tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py, and the L04-L06 cards of course/modules/PC/PC3/cards.json (111 cards). Project files, graders, hub and slices a, c and d are not judged here; their gate runs are recorded for completeness only.",
        "Round-19 method: git diff -U0 50559266 cd4dd7df restricted to the slice files (ledgers/PC3/scripts/PC3-b-r19/out/delta_slice_b_r19.diff); every hunk read in full; both round-18 FAIL rows re-verified and fixed (L04 line 127; PC3-c191); the round-18 'card-full-scan-L06' FAIL depended on c191 and is now PASS; the 111 L04-L06 cards were read card by card this round; carried rows have byte-identical subjects and keep their ids.",
        "Line numbers: L04.html lines are the same as round 18 (the round-19 change is a one-line replacement). Carried rows keep the round-18 location text.",
        "Mutation testing: not applicable to this slice (lab twins, cards and prose; no grader in slice b). mutants is empty.",
        "Registry: references/references.json unchanged in the round-19 delta; no L04-L06 page or card cites it.",
        "Could not check: the Pyodide browser runtime beyond page_smoke's PASS (console and external-request internals were not re-read); the 360 px layout of the three pages (page_smoke is the only evidence); the full pytest suite (only the lab-tooling, page-check and docs-figures modules); the live verify_refs over the whole registry (only the offline whole-registry run and the live PC3 run); the carried passages of L04-L06 that are not in the round-19 delta were not re-read line by line this round, they are carried by byte identity of the file outside line 127 and by the round-18 reading; historical round-14/15/16/17 delta rows are carried as historical; the Remark 2.4 seed-0 sentence on L04 carries no SIMULATED tag of its own (the E3 title and the card carry it), which the rules here do not require, recorded as a judgement and not a row.",
    ],
    "summary": "",
}
n = len(ordered)
fragment["summary"] = (f"Slice b (L04-L06, twins, L04-L06 cards), round 19 at cd4dd7df. {n} rows, all PASS. "
                       "The two round-18 FAILs (L04 line 127 scope sentence; PC3-c191 sufficiency) are fixed and re-verified; the dependent card-full-scan-L06 row is PASS. "
                       "All gates (run_labs 9/9, check_pages, check_dag --all, check_projects, page_smoke for L04-L06 alone, ruff, mypy strict, lab-tooling pytest, verify_refs offline and live PC3, fetch_data, build_site, render_curriculum, run_graders seeds 0-49, twins under python -I -W error, page code and expected blocks equal to twin output) PASS.")
out = ROOT / "ledgers/PC3/PC3-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", n, "pass", sum(r["status"] == "PASS" for r in ordered))
