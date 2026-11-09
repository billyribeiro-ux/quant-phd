"""PC3-b round 18: build the slice-b fragment ledgers/PC3/PC3-b.json from the round-17 fragment.

Usage: python -I ledgers/PC3/scripts/PC3-b-r18/make_fragment_r18.py <round-17-fragment> <checkout-root>

Rule (verifier-rules.md, round after the first): every round-17 row id is kept. A row is either
re-verified in this round (RE below, with the evidence named here) or carried with the prefix
'Carried from round 17 (...)' when its cited subject is unchanged since the round-17 pin 700bf33f.
"""
import json
import sys
from pathlib import Path

prev_path = Path(sys.argv[1])
root = Path(sys.argv[2])
S = "ledgers/PC3/scripts/PC3-b-r18/out"
prev = json.loads(prev_path.read_text(encoding="utf-8"))

RE = {
    "gate-run-labs-unit": ("2.5-labs", "tools/run_labs.py --unit PC3",
        f"Re-run at 50559266: 'run_labs PC3: PASS (9/9)', exit 0 ({S}/run_labs_unit.out)."),
    "gate-check-pages": ("2.9-prose", "tools/check_pages.py --unit PC3 ; tools/check_pages.py --all",
        f"Re-run: 'check_pages PC3: PASS', exit 0 ({S}/check_pages_unit.out); --all exit 0 ({S}/check_pages_all.out)."),
    "gate-check-dag": ("2.9-DAG", "tools/check_dag.py --all",
        f"Re-run: 'check_dag LX1: PASS', 'check_dag LX2: PASS', 'check_dag PC3: PASS', exit 0 ({S}/check_dag_all.out)."),
    "gate-check-projects": ("2.6-structure", "tools/check_projects.py --unit PC3",
        f"Re-run: 'check_projects PC3: PASS', exit 0 ({S}/check_projects_unit.out). Project rows belong to slices c and d."),
    "gate-page-smoke-slice": ("2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)",
        f"Re-run alone: L04, L05, L06 each 'PASS', 'page_smoke PC3: PASS', exit 0 ({S}/page_smoke_slice.out)."),
    "gate-ruff-mypy-twins": ("2.5-labs", "ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; ruff check . ; ruff format --check . ; mypy --no-incremental",
        f"ruff check tests/labs/PC3: 'All checks passed!' ({S}/ruff_check_twins.out); ruff format --check tests/labs/PC3: '9 files already formatted' ({S}/ruff_format_twins.out); mypy --no-incremental: 'Success: no issues found in 385 source files', exit 0 ({S}/mypy.out)."),
    "gate-pytest-lab-tooling": ("2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_docs_figures.py",
        f"Re-run: exit 0 for the lab-tooling modules ({S}/pytest_labs_tooling.out) and for the page-check and docs-figures modules ({S}/pytest_page_checks.out, all dots, exit 0)."),
    "gate-verify-refs-offline": ("2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit PC3",
        f"Re-run: 'offline integrity: 560 entries, 0 problems', exit 0 ({S}/verify_refs_offline.out); live PC3 run 'live re-verification of PC3: 2 of 560 entries, 0 problems', exit 0 ({S}/verify_refs_unit_PC3.out)."),
    "gate-run-graders-unit": ("2.6-structure", "tools/run_graders.py --unit PC3 --seeds 0-49",
        f"Re-run: 'run_graders PC3: PASS (reference 50/50 seeds, slowest 0.5 s)', exit 0 ({S}/run_graders_unit.out). Project graders belong to slices c and d."),
    "gate-fetch-data-check": ("2.8-data", "tools/fetch_data.py --check",
        f"Re-run: 'fetch_data: 3 datasets, 0 problems', exit 0 ({S}/fetch_data_check.out)."),
    "gate-build-site-check": ("2.9-prose", "tools/build_site.py --check",
        f"Re-run: 'site data current: 6 outputs', exit 0 ({S}/build_site_check.out)."),
    "gate-render-curriculum-diff": ("2.9-prose", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json",
        f"Re-run: exit 0; the git diff over the two generated files is empty ({S}/render_curriculum_diff.out)."),
    "r16-gates-ruff-format-repo": ("2.5-labs", "ruff check . ; ruff format --check . (repo)",
        f"Re-run: 'All checks passed!' exit 0 ({S}/ruff_check_repo.out); '553 files already formatted' exit 0 ({S}/ruff_format_repo.out)."),
    "r16-gate-check-dag-all": ("2.9-DAG", "tools/check_dag.py --all",
        f"Re-run: exit 0, PC3 PASS ({S}/check_dag_all.out)."),
    "twin-run-alone-L04-L06": ("2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py",
        f"Each twin run alone as 'python -I -W error <twin>' from /tmp: exit 0 for all three, stderr empty; stdout 52, 25 and 21 lines ({S}/pc3b_r18_lab-PC3-L04-1.py.out, {S}/pc3b_r18_lab-PC3-L05-1.py.out, {S}/pc3b_r18_lab-PC3-L06-1.py.out). Twin files unchanged since 700bf33f."),
    "twin-page-code-equals-twin": ("2.5-labs", "L04.html, L05.html, L06.html data-run blocks vs the three twins",
        f"ledgers/PC3/scripts/PC3-b-r17/twin_check.py run at this pin: 'L04 lab-PC3-L04-1: page_code_eq_twin=True ... L05 ... True ... L06 ... True', 'ALL OK' ({S}/twin_check_r18.out)."),
    "twin-expected-equals-stdout": ("2.5-labs", "L04.html, L05.html, L06.html pre.expected vs twin stdout",
        f"Same run ({S}/twin_check_r18.out): expected_eq_stdout=True and expected_lines equal stdout_lines for L04 (52), L05 (25), L06 (21)."),
    "r16-twin-page-and-run": ("2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py; the three pages",
        f"Re-run at this pin: twin exit 0 and page code equals twin for all three ({S}/twin_check_r18.out; {S}/run_labs_unit.out)."),
    "r16-sim-independent": ("2.5-labs", "ledgers/PC3/scripts/PC3-b-r16/sim_game_independent.py",
        f"Re-run at this pin: 'mid == 10000 - 10*I_{{t-1}} at every turn, seeds 0..499: True'; 'P&L identity, seeds 0..499: True'; 'largest |inventory| over seeds 0..499: 8 (limit 10)' ({S}/sim_game_independent.out)."),
    "notation-registry-L04-L06": ("2.4-notation", "course/modules/PC/PC3/L04.html line 127 (new x^{+} definition); L06.html line 60; notation/notation.json",
        "The new symbol x^{+}=max(x,0) (L04 line 127) and its L06 definition (line 60) are not in notation/notation.json (8 symbols, the macro list has no positive part), so no registered meaning is reused. \\max is standard KaTeX and page_smoke reports no katex-error (run this round). First use of (v-a)^{+} is Proposition 3.1 at line 131, after the definition at line 127. Symbols N, t, p, L, C, I, v, a, b, q, h, m, sigma, f, c, W were read at lines 56, 72-77, 93-97 and 131 with the same meanings as before. PASS."),
    "r17-L05-meta-description-comparisons": ("2.9-prose", "course/modules/PC/PC3/L05.html line 7 (meta name=description)",
        "FIXED. Line 7 now reads 'a monotonic deque whose correctness is proved and whose comparisons of stored values number at most twice the number of inputs'. The body uses the same qualifier: line 52 ('at most twice the input length in comparisons of stored values'), line 137 (Proposition 3.3: 'the number of comparisons made by the while-loop tests is at most 2n'), and the proof of Proposition 3.3 counts those tests. Lab output (out/pc3b_r18_lab-PC3-L05-1.py.out) prints 'deque comparisons at most 2n = 400: True' and 387 comparisons at window 200 (<= 400). The meta-description check is therefore consistent with the body. The remaining L05 lines are byte-identical to 700bf33f."),
    "L04-lab-section-locator": ("2.9-prose", "L04.html lines 72, 83 vs lab section (h3 at line 181) under h2 s4 (line 163)",
        "Round 18 line numbers. Line 72 (A1) points to 'Lab 1 (Section 4)'; line 83 (Remark 1.2) names Lab 1 and the unit project. Both lines are unchanged. The Section 4 h2 id=s4 is at line 163 and the h3 'Lab 1 · The game on seed 0...' at line 181, both after the new line 127 insertion. The claim that the lab is in Section 4 holds. PASS."),
    "L04-example-3.2-values": ("2.4-mathematics", "L04.html lines 144-145 (Example 3.2); lab Part 2 output",
        f"Example 3.2 (now lines 144-145) states E=5-1/2[(v-10010)^+ + (9990-v)^+] and the values 5 at v=10000, 0 at 10020, 5/2 at 9985. Re-derived exactly by verify_numbers_r18.py ({S}/verify_numbers_r18.out: 'Example 3.2 E at v=... equals ...' PASS). The lab (tests/labs/PC3/lab-PC3-L04-1.py, Part 2) prints E=5/2 at 9985, 5 at 10000 and 0 at 10020 (run at this pin). PASS."),
    "L04-prop-3.1-closed-form": ("2.4-mathematics", "L04.html lines 130-142 (Prop 3.1 statement at 131, proof at 135-140)",
        f"Round 18 re-derivation: enumeration of the three arrival outcomes (uninformed buy (1-p)/2 with contribution a-v, uninformed sell (1-p)/2 with v-b, informed p with -(v-a)^+ or -(b-v)^+ by A4) equals the closed form (1-p)h - p[(v-a)^+ + (b-v)^+] exactly (Fraction arithmetic) at 21 grid points for three quotes at p=1/2 ({S}/verify_numbers_r18.out, first three lines PASS). The proof's step 'the bracket equals a-b=2h by A6' is correct. The new paragraph at line 127 does not alter the statement."),
    "L04-corollary-3.3": ("2.3-grades", "L04.html lines 149-155 (Corollary 3.3 statement at 150, proof at 154-155)",
        f"Statement and proof (p=1/2, v>=a: E=h/2-(v-a)/2, zero iff v=a+h) re-derived exactly ({S}/verify_numbers_r18.out: 'Corollary 3.3 linear form ...' and 'zero exactly at v = a+h' PASS). Grade T is supported by Proposition 3.1 and a two-line proof. The Corollary statement contains no positive part (see r18-L04-positive-part-sentence). PASS."),
    "L04-remark-3.4-inventory-zero": ("2.4-mathematics", "L04.html lines 159-160 (Remark 3.4)",
        "Remark 3.4 (now lines 159-160): '(1-p)h cents per turn', and at p=1/2 'h/2 cents per turn, one quarter of the quoted spread 2h'. Re-derived: h/2 = (2h)/4 exactly ({S}/verify_numbers_r18.out 'Remark 3.4 h/2 is one quarter of 2h' PASS). PASS."),
    "L04-proposition-4.1-remark-4.2-sd": ("2.4-mathematics", "L04.html lines 166-172 (Prop 4.1 statement at 167, proof 172), Remark 4.2 at 176-177",
        "Proposition 4.1 (mean 0, variance 25 I^2) re-derived: E[I eps]=0, E[(I eps)^2]=25 I^2 (line 172). Remark 4.2 standard deviation 5|I| cents: I=3 gives 15 and I=10 gives 50 ({S}/verify_numbers_r18.out 'sd of fair-move term' PASS). Lab Part 3 prints variance 225 at I=3 and 2500 at I=10 (run at this pin). PASS."),
    "L04-remark-4.2-inventory-independence": ("2.4-mathematics", "L04.html line 177 (Remark 4.2, I=10 case)",
        "At I=10, quote 9990/10010, p=1/2, v=10000: the informed arrival does not trade (v inside the quote); the uninformed sell is refused (|11|>L=10); only the uninformed buy contributes a-v=10 with probability (1-p)/2=1/4, so E=10/4=5/2 ({S}/verify_numbers_r18.out 'Remark 4.2 I=10 ... = 5/2' PASS). Against 5 at I=0 (Prop 3.1 at v=10000). PASS."),
    "L04-scope-and-banned-phrases": ("2.9-prose", "L04.html visible prose; scripted scan (ledgers/PC3/scripts/PC3-b-r16/prose_scan.py) at this pin",
        f"Re-run ({S}/prose_scan_r18.out): 'L04 banned=0 process=0 ellipsis=0 scope_sentences=39'. The new sentence at line 127 contains no scope word and no banned phrase. The 39 scope sentences are the same as in round 17 except that the line numbers after 127 moved by +2; the round-17 review of each scope word still applies (carried for the unchanged sentences). PASS."),
    "L04-A1-project-consistency": ("2.9-prose", "L04.html line 72 and line 83 vs project.html lines 53-57, 76-81",
        "Carried from round 17 (L04.html line 72 and line 83 byte-identical; the cited project.html lines 53-57 and 76-81 are not among the project.html hunks at 397, 450 and 623 changed since 700bf33f, so the cited passages are byte-identical). PASS."),
    "r16-prose-scan": ("2.9-prose", "ledgers/PC3/scripts/PC3-b-r16/prose_scan.py on L04, L05, L06 at this pin",
        f"Re-run ({S}/prose_scan_r18.out): banned 0, process 0, ellipsis 0 for L04, L05 and L06; scope sentences L04=39, L05=60, L06=41 (all reviewed in round 17 and carried; none new in the round-18 delta). PASS."),
    "card-full-scan-L04": ("2.7-cards", "course/modules/PC/PC3/cards.json: the 40 L04 cards",
        "Carried from round 17 (the 39 L04 cards other than PC3-c062 and PC3-c192 are byte-identical since 700bf33f; the scan count is now 40). The two changed or new cards are re-verified in r18-card-PC3-c062 and r18-card-PC3-c192. PASS."),
    "card-full-scan-L06": ("2.7-cards", "course/modules/PC/PC3/cards.json: the 41 L06 cards",
        "Carried from round 17 for the 38 L06 cards not changed since 700bf33f; PC3-c112, PC3-c123 and the new PC3-c191 are re-verified in r18-card-PC3-c112, r18-card-PC3-c123-basis and r18-card-PC3-c191 (the last is a FAIL). The row is therefore not PASS for the full scan while c191 stands. The scan therefore finds one failing card, see r18-card-PC3-c191-when-degenerate."),
    "card-full-scan-L05": ("2.7-cards", "course/modules/PC/PC3/cards.json: the 30 L05 cards",
        "Carried from round 17 (cards PC3-c084..c101, c142..c146, c169..c170 byte-identical since 700bf33f; no L05 card changed). PASS."),
    "card-duplicate-scan": ("2.7-cards", "course/modules/PC/PC3/cards.json (187 PC3 cards)",
        f"Re-run ({S}/cards_r18.out): 187 cards, 111 for L04-L06 (L04 40, L05 30, L06 41); no duplicate ids. Front-text Jaccard >= 0.45 gives 55 pairs; the highest-scoring pairs were read (c110/c183/c184 are different targets: NPV, monotonicity, break-even; c097/c145 are the naive and deque counts; c027/c028 are different probabilities; c117/c150 and c116/c148 are different rates or sizes). Nearest-neighbour whole-card similarity for the new cards: c191 nearest c112 at 0.42 (different questions: c112 asks what the bounds decide when the range straddles; c191 asks when the interval fixes the sign); c192 nearest c064 at 0.42 (c064 asks when a trade fills, c192 asks what a fill is). No pair is a duplicate. PASS."),
    "card-key-results-agreement": ("2.7-cards", "cards.json L04-L06 entries vs key-results tables (L04.html 619-629, L05.html 472-477, L06.html 448-454)",
        "L06.html is byte-identical since 700bf33f; the L04 key-results table (L04.html lines 619-629) differs only by the +2 shift from the Section 3 insertion. Key-results rows that mention Definition 1.1 or Corollary 3.3 were read against the changed cards PC3-c062 and PC3-c112 and agree. PASS."),
    "card-number-in-lesson": ("2.7-cards", "cards.json numbers vs own lesson text",
        "Re-checked for the changed cards: PC3-c062 numbers (+5, -5, 1/2, 5 as q-bar) appear in L04.html lines 62-63 and Remark 1.2 (line 83); PC3-c112 and PC3-c191 contain no lesson numbers other than the symbols u*, I, m, A, l, h, which are defined in L06.html lines 112, 122 and 132; PC3-c192 numbers: none beyond L. PASS."),
    "card-cite-empty": ("2.7-cards", "cards.json 'cite' fields, all 187 PC3 cards",
        f"Re-run ({S}/cards_r18.out): 'cards with empty cite-list but cite key present: 0'; no PC3 card has a non-empty cite list. PASS."),
    "card-PC3-c112-corollary-boundary": ("2.7-cards", "course/modules/PC/PC3/cards.json line 954 (PC3-c112) vs L06.html lines 112, 122, 131-137",
        "Re-verified. The new front carries every hypothesis of Corollary 3.3: r>-1 fixed (Prop 3.1 H1, line 112); C_0=-I with I>0 and C_t=um with m>0, u>=0, n>=1 (Prop 3.1 H2-H3); A (Prop 3.1 line 112); factor ranges 0<l_j<=h_j with products l, h (Prop 3.2 H1 line 122, Corollary line 132). Back: 'the unit count l gives a loss and h a gain' follows from Prop 3.1 proof line 137 (NPV(u)=mA(u-u*)). The back no longer contains the one-sided rule, which is now in c191. Grade T basis matches. PASS."),
    "r18-delta-scope": ("2.9-prose", f"git diff --name-only 700bf33f 50559266 restricted to the slice-b files",
        f"Slice-b files changed since 700bf33f: course/modules/PC/PC3/L04.html (2 lines inserted after line 126, new lines 127-128), course/modules/PC/PC3/L05.html (line 7 only), course/modules/PC/PC3/cards.json (PC3-c062 back; PC3-c112 front and back; PC3-c123 basis; new PC3-c191 at line 1576 and PC3-c192 at line 1585). Not changed: L06.html, tests/labs/PC3/lab-PC3-L0{4,5,6}-1.py, notation, curriculum, references. project.html and grader/test_project.py changed (slices c and d). Command: git diff --stat 700bf33f 50559266 -- <the files>. PASS (scope complete)."),
    "r18-L04-section3-math": ("2.4-mathematics", "L04.html lines 127-160 (new positive-part paragraph; Section 3 statements and proofs)",
        f"All Section 3 claims re-derived with exact fractions in {S}/verify_numbers_r18.out (24 checks, 0 FAIL): Prop 3.1 closed form, Example 3.2 values (5, 0, 5/2), Corollary 3.3 linear form and zero set, Remark 3.4. The inserted paragraph (line 127) defines x^{{+}} correctly; the Prop 3.1 hypotheses H1-H3 are unchanged and sufficient (the proof uses only A1, A2, A4, A5 and A6). PASS."),
    "r18-card-PC3-c062": ("2.7-cards", "course/modules/PC/PC3/cards.json line 530-535 (PC3-c062) vs L04.html lines 60-65",
        "Back now says 'a quoted size q_t from 0 up to q-bar = 5, the largest size'. Definition 1.1 (L04.html line 63) reads 'a quoted size q_t in {0,1,...,q-bar}, with q-bar=5'. Same content; the card's '0 up to 5' is the same set of integers. Other content matches lines 62-64. PASS."),
    "r18-card-PC3-c112": ("2.7-cards", "course/modules/PC/PC3/cards.json line 954-959 (PC3-c112)",
        "See the carried-and-re-verified row card-PC3-c112-corollary-boundary (this round's text). PASS."),
    "r18-card-PC3-c123-basis": ("2.7-cards", "course/modules/PC/PC3/cards.json line 1042-1050 (PC3-c123 basis)",
        f"Basis changed from 'printed NPV signs at the bounds' to 'printed break-evens'. The back (1164.10 at 8 percent, 1249.05 at 12 percent) is printed by the lab (tests/labs/PC3/lab-PC3-L06-1.py Part 2: 'rate 8%: ... break-even units 1164.10', 'rate 12%: ... 1249.05'; {S}/pc3b_r18_lab-PC3-L06-1.py.out) and by L06.html line 154 and 410; the exact values are re-derived in {S}/verify_numbers_r18.out (break-even 8%, 10%, 12%). Grade C with basis naming the lab is consistent with the card's content. PASS."),
    "r18-card-PC3-c191": ("2.7-cards", "course/modules/PC/PC3/cards.json line 1576-1584 (PC3-c191)",
        f"FAIL. Front: 'When does the whole interval [l, h] fix the sign of the NPV?' Back: 'When the whole interval lies strictly on one side of the break-even ... that is h < u* or l > u*'. The back is a sufficient condition (L06.html line 132: 'The sign is fixed when ...') but the card answers the 'when' question as if it were the complete condition. The degenerate range l = h = u* (admissible: a single-point factor range [u*, u*] gives l = h = u* by Proposition 3.2) makes NPV(u) = mA(u-u*) = 0 on the whole range (L06.html line 137), so the sign is fixed (at zero) while the range is not strictly on one side. Re-derived in {S}/verify_numbers_r18.out ('Corollary 3.3 degenerate range ...' PASS, the exact zero)."),
    "r18-card-PC3-c192": ("2.7-cards", "course/modules/PC/PC3/cards.json line 1585-1590 (PC3-c192)",
        "Definition: 'A trade of one unit between the maker and the customer at a quoted price. It occurs only when A5 allows it: the quoted size is at least 1 and the inventory after the trade satisfies |I| <= L.' L04.html line 64 (Definition 1.1, third step) states the same fill definition and 'it occurs only when A5 allows it'; A5 (line 76) says 'A trade fills only if q_t >= 1 and the inventory after the trade satisfies |I| <= L, with L=10'. L is defined at line 56. Not a duplicate of c064 (definition versus condition). PASS."),
    "r18-cited-external-passages": ("2.1-citations", "FC2/L02.html line 88 (def-cost-of-carry-forward-price), FC2/L05.html line 59 (def-put-call-parity), FC2/L02.html line 59 (def-forward-contract), CF1/L01.html (def-net-present-value), AC1/L03.html (def-statement-articulation), PC3/L01.html (def-fermi-estimation), PC3/L03.html (def-expected-value-game)",
        "Cross-module definitions cited by the slice-b pages. Files that changed since 700bf33f (FC2/L02.html, FC2/L05.html) change only at lines 51, 398, 450 (FC2 L02) and 7, 51, 71, 140, 144, 310 (FC2 L05), none of them a cited definition line (88, 59, 59). CF1/L01, AC1/L03, PC3/L01, PC3/L03 are byte-identical since 700bf33f. Every anchor is present in course/concepts.html (13 checked by grep: bid-ask-spread, expectation, limit-order-book, market-maker, big-o-complexity, binary-heap, hash-map, monotonic-deque, unit-test, cost-of-carry-forward-price, forward-contract, net-present-value, put-call-parity, statement-articulation). PASS."),
}
CARRY_NOTE = {
    "L04": ("Carried from round 17 (course/modules/PC/PC3/L04.html passage byte-identical since the previous pin; the only change "
            "is a two-line insertion at lines 127-128, so round-17 line numbers at or after 127 are +2 at round 18):"),
    "L05": ("Carried from round 17 (course/modules/PC/PC3/L05.html passage byte-identical since the previous pin; the only change "
            "is line 7, re-verified as r17-L05-meta-description-comparisons):"),
    "L06": "Carried from round 17 (course/modules/PC/PC3/L06.html and tests/labs/PC3/lab-PC3-L06-1.py byte-identical since the previous pin):",
    "card": ("Carried from round 17 (the cited course/modules/PC/PC3/cards.json entries byte-identical since the previous pin; the "
             "changed entries PC3-c062, c112, c123 and the new c191, c192 are re-verified in the r18 card rows):"),
    "lab": "Carried from round 17 (tests/labs/PC3 twins byte-identical since the previous pin):",
    "hist": "Carried from round 17 (historical git diff, unchanged since the previous pin):",
    "gen": "Carried from round 17 (cited files byte-identical since the previous pin):",
}


def group(rid: str) -> str:
    if rid.startswith(("L04", "r16-L04", "lab-L04")):
        return "L04"
    if rid.startswith(("L05", "r16-L05", "lab-L05")):
        return "L05"
    if rid.startswith(("L06", "r16-L06", "r17-L06")):
        return "L06"
    if rid.startswith(("card", "r16-card", "r17-card")):
        return "card"
    if rid.startswith(("twin", "r16-twin")):
        return "lab"
    if rid.startswith(("delta", "r16-delta", "r17-delta")):
        return "hist"
    return "gen"


# FIX texts for FAIL rows (every non-PASS row needs a fix)
FIX = {
    "card-full-scan-L06": "Resolve r18-card-PC3-c191-when-degenerate (see its fix); the L06 scan then has no failing card.",
}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RE:
        check, loc, ev = RE[rid]
        status = "FAIL" if rid in ("r18-L04-positive-part-sentence", "r18-card-PC3-c191", "card-full-scan-L06") else "PASS"
        row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
        if rid == "r17-L05-meta-description-comparisons":
            row["status"] = "PASS"
            row["location"] = r["location"]
        if rid in FIX:
            row["fix"] = FIX[rid]
        rows.append(row)
        continue
    g = group(rid)
    if rid in ("L04-definitions-A1-A6-notation", "L04-prop-2.2-2.3-identity"):
        note = CARRY_NOTE["L04"] + " (lines before 127 unchanged)."
    else:
        note = CARRY_NOTE[g]
    rows.append({
        "id": rid,
        "check": r["check"],
        "location": r["location"],
        "status": r["status"],
        "evidence": f"{note} {r['evidence']}",
    })

# RE entries that are new in round 18 (not round-17 ids) are emitted here; c191 and c112 are emitted in new_rows
ids_prev = {r["id"] for r in prev["rows"]}
for rid, (check, loc, ev) in RE.items():
    if rid in ids_prev or rid in ("r18-card-PC3-c191", "r18-card-PC3-c112"):
        continue
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

# the L04-carried rows whose cited passage lies after line 127 keep round-17 line numbers (see note)

new_rows = [
    {
        "id": "r18-L04-positive-part-sentence",
        "check": "2.4-mathematics / 2.9-prose (scope word, notation)",
        "location": "course/modules/PC/PC3/L04.html line 127",
        "status": "FAIL",
        "evidence": ("The inserted sentence reads 'Write x^{+}=max(x,0) for the positive part of a real number x. The statements of this section "
                     "use it.' The positive part appears in: Proposition 3.1 statement (line 131, yes); Example 3.2 text (line 145, text not statement); "
                     "the Corollary 3.3 proof (line 155); Remark 3.4 text (lines 159-160, none). The Corollary 3.3 statement (line 150) and the "
                     "Remark 3.4 statement contain no positive part, so 'the statements of this section use it' is not true of every statement. "
                     "Checked by grep -n '{+}' on L04.html and by reading lines 125-160 with strip_lines.py "
                     f"(ledgers/PC3/scripts/PC3-b-r18/strip_lines.py)."),
        "fix": "Replace the second sentence with 'Proposition 3.1 and Example 3.2 use it.' (One sentence, no math change.)",
    },
    {
        "id": "r18-card-PC3-c191-when-degenerate",
        "check": "2.7-cards",
        "location": "course/modules/PC/PC3/cards.json line 1576-1584 (PC3-c191), against L06.html lines 132 and 137",
        "status": "FAIL",
        "evidence": ("Front: 'When does the whole interval [l, h] fix the sign of the NPV?'. Back: 'When the whole interval lies strictly on one side "
                     "of the break-even ... that is h < u* or l > u*'. This is a sufficient condition (the page's Corollary 3.3 says 'The sign is "
                     "fixed when ...'), but the card gives it as the complete answer to 'when'. Degenerate range l = h = u* is admissible "
                     "(Proposition 3.2 allows l_j = h_j) and gives NPV = mA(u-u*) = 0 on all of [l,h] (L06.html line 137), so the sign is fixed "
                     "(at zero) while the range is not strictly on one side. Verified exactly in "
                     f"{S}/verify_numbers_r18.out (the 'degenerate range' check)."),
        "fix": ("Change the front to 'What condition on [l, h] is sufficient to fix the sign of the NPV?' or add to the back: 'This condition "
                "is sufficient, not necessary: a zero-width range with l = h = u* also fixes the sign, at zero.'"),
    },
]
rows.extend(new_rows)
extra = [
    {
        "id": "r18-counts-and-judgement",
        "check": "2.7-cards",
        "location": "course/modules/PC/PC3/cards.json (L04-L06: 111 cards)",
        "status": "PASS",
        "evidence": (f"Re-run ({S}/cards_r18.out): L04 40, L05 30, L06 41 (111); whole PC3 unit 187 cards; no duplicate ids. "
                     "Judgement (not a row): the L04 card PC3-c192 overlaps the A5 condition of PC3-c064 in wording, but asks a different "
                     "question (what a fill is versus when a trade fills); not a duplicate."),
    },
]
rows.extend(extra)

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
frag = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 18,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 18 (did not build PC3)",
    "pin": "50559266",
    "base": ("700bf33f334486d7b5b4f22d4f82f3e25d4b39b6 (round-17 pin). Delta 700bf33f..50559266 in this slice: L04.html lines 127-128 "
             "(inserted positive-part paragraph); L05.html line 7 (meta description); cards.json PC3-c062 back, PC3-c112 front and back, "
             "PC3-c123 basis, new PC3-c191 and PC3-c192. L06.html, tests/labs/PC3 twins, notation and references are unchanged in the slice."),
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE18-PC3-b (detached at 50559266; .venv symlinked)",
    "scratch": f"/Users/billyribeiro/.fanout/wt/verifyE18-PC3-b/{S}",
    "verified_at": "2026-11-09T05:30:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: slice b = L04, L05, L06 lesson pages, the lab twins tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py, and the L04-L06 cards of course/modules/PC/PC3/cards.json. Project files, graders, hub and slices a, c and d are not judged here (their gate runs are recorded for completeness only).",
        "Round-18 method: git diff 700bf33f..50559266 restricted to the slice files; every hunk read in full (L04 lines 124-160, L05 lines 1-12 and 135-140, cards c062, c112, c123, c191, c192 and their neighbours); the round-17 FAIL (L05 meta description) re-checked against the body; every round-17 row id is kept; rows whose subject is byte-identical are carried with the carry prefix; rows whose subject changed are re-verified with new evidence.",
        "Line numbers: L04.html lines at or after 127 are +2 relative to round 17. Carried L04 rows keep their round-17 location text and say so in the carry prefix; re-verified L04 rows use round-18 numbers.",
        "Mutation testing: not applicable to this slice (lab twins, cards and prose; no grader in slice b). mutants is empty.",
        "Registry: references/references.json changed in the delta (generated_at and a used_by entry); no L04-L06 page or card cites it (data-references lists are empty). No registry flag.",
        "Could not check: the Pyodide browser runtime beyond page_smoke's PASS (console-error and external-request internals not re-read); the 360 px layout of the three pages (page_smoke is the only evidence); the full pytest suite (only the lab-tooling, page-check and docs-figures modules); the live verify_refs over the whole registry (only the offline whole-registry run and the live PC3 run); the 'historical' round-14/15/16 delta rows are carried as historical; the 'sim independent' script is run as in round 16, not re-read line by line; the 55 front-text pairs above Jaccard 0.45 were not each read, only the top pairs and the nearest neighbours of the changed cards.",
    ],
    "summary": (f"Slice b (L04-L06, twins, L04-L06 cards), round 18 at 50559266. {len(rows)} rows: {n_pass} PASS, {n_fail} FAIL, 0 UNVERIFIABLE. "
                "The round-17 FAIL (L05 meta description) is fixed and verified. Two new FAILs from the round-18 delta: (1) L04.html line 127 says 'the statements of this section use it' but the Corollary 3.3 and Remark 3.4 statements contain no positive part (low severity; fix: name Proposition 3.1 and Example 3.2); (2) PC3-c191 answers 'when does the interval fix the sign' with a sufficient condition, and the degenerate range l = h = u* also fixes the sign (at zero) (fix: say 'sufficient' or add the zero-width case). All gates (run_labs 9/9, check_pages, check_dag --all, check_projects, page_smoke for L04-L06 alone, ruff, mypy strict, pytest modules, verify_refs offline and live PC3, fetch_data, build_site, render_curriculum, run_graders seeds 0-49, twins under python -I -W error) PASS."),
}
out = root / "ledgers/PC3/PC3-b.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", n_pass, "fail", n_fail, "verdict", verdict)
