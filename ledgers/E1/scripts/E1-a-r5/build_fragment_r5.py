"""Build the round-5 fragment for E1 slice a (delta verification from the round-4 pin). Writes ledgers/E1/E1-a.json only."""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/E1/scripts/E1-a-r5/"
CARRY_L01 = "Carried from round 4 (L01.html, L03.html, references/, notation/, tools/, tests/labs/E1/lab-E1-L01-1.py, lab-E1-L03-1.py byte-identical since the round-4 pin edbb7aa8; delta_files_slice_a_r5.out): "
CARRY_L02 = "Carried from round 4 (cited passages byte-identical since the round-4 pin edbb7aa8; the only round-5 L02.html hunk is l.247, see " + S + "delta_slice_a_hunks_r5.diff): "

def row(i, check, location, status, evidence, fix=None):
    r = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
    row("E1a-01", "2.1-citations", "references/references.json key varian2014intermediate; course/modules/E/E1/index.html; L01.html:498; L02.html:488; L03.html:464", "PASS",
        "Re-run this round: `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' (exit 0, " + S + "verify_refs_offline_r5.out); `tools/verify_refs.py --unit E1` -> 'live re-verification of E1: 1 of 560 entries, 0 problems' (exit 0, " + S + "verify_refs_unit_E1_live_r5.out). references/ unchanged in the delta (delta_files_slice_a_r5.out). Only varian2014intermediate is cited in the reference sections."),
    row("E1a-02", "2.2-numbers-hub", "course/modules/E/E1/index.html (eyebrow l.42; objectives; hours split; placement)", "PASS",
        "Re-run this round: index.html changed at l.42 only (delta_slice_a_hunks_r5.diff): the eyebrow now reads '90 h lessons · 30 h project (25% of the 120 h)'. Arithmetic re-checked: 9 x 10 = 90; 90 + 30 = 120; 30/120 = 25 %; curriculum/curriculum.json E1 'hours': 120 (command output in " + S + "static_checks_r5.out). The 9-question placement arithmetic is re-derived in " + S + "rederive_slice_a_r5.out, identical to the round-4 output (7/9 = 77.8 %, 8/9 = 88.9 %, ceil(0.8*9) = 8)."),
    row("E1a-03", "2.2-numbers-L01", "L01.html Example 1.6 (l.116), Remark 1.5 (l.111), Remark 2.4 (l.153), Problems M1-M3, P1-P3, E1-E3, R1-R3, quiz (ll.297-492)", "PASS",
        CARRY_L01 + "rederive_slice_a_r5.out (python -I, re-run this round) identical to the round-4 output: x_bar=30, y_bar=20, u_bar=600 (Example 1.6); Remark 2.4: y=80/3, MRS 4/3, 80/63 offset, 1600/63, 38/3 gain. twin_L01_r5.out matches the expected block (see E1a-06)."),
    row("E1a-04", "2.2-numbers-L02", "L02.html Example 1.4 (l.88), Remark 1.6 (l.103), Misconception 1 (l.264-266), Problems and quiz (ll.280-472)", "PASS",
        "Re-run this round: " + S + "rederive_slice_a_r5.out identical to round 4: Example 1.4 q*=4, C(4)=36, profit 4, MC(4)=10; F=100 profit -84; sqrt(12) profit 16 sqrt(3) - 24 = 3.7128 (L02.html:266, twin_L02_r5.out). The round-5 L02.html hunk (l.247) contains no number that is not printed by twin_L02_r5.out."),
    row("E1a-05", "2.2-numbers-L03", "L03.html Example 1.5 (l.93), Remark 2.2 (l.110), Problems (ll.262-349), quiz (ll.389-449)", "PASS",
        CARRY_L01 + "rederive_slice_a_r5.out: p*=110/7, Q*=480/7, S(p*)=480/7; grid i/7, i=0..140: 110 positive, 1 zero, 30 negative (also printed by twin_L03_r5.out)."),
    row("E1a-06", "2.2-numbers-lab-printed", "L01 expected block (L01.html:240-257); L02 expected block (L02.html:228-246); L03 expected block (L03.html:215-222)", "PASS",
        "Re-run this round: `python -I " + S + "twin_vs_page_r5.py .` -> " + S + "twin_vs_page_r5.out: for L01, L02, L03 the page code equals the twin (True) and the expected block equals the twin's stdout under `python -I -W error` (True). twin_L0{1,2,3}_r5.err are 0 bytes. twin_L02_r5.out is byte-identical to the round-4 twin output (cmp)."),
    row("E1a-07", "2.2-numbers-prose / 2.3-mathematics", "L01.html:153 (Remark 2.4), L01.html:307 (M2)", "PASS",
        CARRY_L01 + "L01.html:153 and :307 unchanged; Remark 2.4 values re-derived in " + S + "rederive_slice_a_r5.out (identical to round 4)."),
    row("E1a-08", "2.3-grades-propositions", "L01 Props 1.2 (l.72), 1.3 (l.82), 1.4 (l.92-95), 2.2 (l.131), 2.3 (l.141); L02 Props 1.3 (l.72), 1.5 (l.91), 2.2 (l.118); L03 Props 1.3 (l.72), 2.1 (l.98)", "PASS",
        CARRY_L02 + "L02 Props 1.3/1.5/2.2 lie outside l.247; L01 and L03 byte-identical. Grades T with complete proofs re-read this round in the same lines (Prop 1.5 proof, L02.html:92-100, uses only the constant-shift argument stated there). Prop 1.5 hypothesis 'same p, c, k' is the one card E1-c019 cites."),
    row("E1a-09", "2.3-grades / 2.4-mathematics / 2.9-prose", "L02.html:130 (hypothesis), L02.html:262-266 (misconception 1)", "PASS",
        CARRY_L02 + "L02.html:130 and :262-266 unchanged. AC(q) = F/q + c + kq, AC'(q) = k - F/q^2; minimiser sqrt(F/k) for F > 0 (L02.html:266, true on q > 0 by the sign of AC'). Profit at sqrt(12) = 16 sqrt(3) - 24 ~ 3.7128 printed by twin_L02_r5.out."),
    row("E1a-10", "2.3-grades-lab-results (C cards)", "cards E1-c014, c025, c027, c139, c140, c141, c142 (grade C; basis names Lab 1)", "PASS",
        "Re-run this round against " + S + "twin_L01_r5.out, twin_L02_r5.out, twin_L03_r5.out: c014 point 30 in all four L01 cases and the 60-step grid (61 points); c025 profit 4 and -84, same output 4 (cases 1 and 4); c027 grid j/12, j=0..72, 'equals closed form: True' in all four cases; c139 'budget exhausted: True' and 'equal: True' in all four; c140 'producing q* is better: True' in all four (4 > -12, 3 > -5, 16/3 > 0, -84 > -100); c141 110 / 1 / 30; c142 48/7 for F=0 and F=100 (changed back text 'Lesson 2, Proposition 1.5; Lab 1' cross-references L02.html:92 and L03 misconception 3). Basis strings name the lab, as BUILDER_RULES §7 requires."),
    row("E1a-11", "2.4-mathematics-L01", "L01 Props 1.2-1.4, 2.2, 2.3; Remark 1.5; Problem R2 (l.380-386)", "PASS",
        CARRY_L01 + "rederive_slice_a_r5.out re-checks the Prop 1.4 identity and Problem R2 steps (identical to round 4)."),
    row("E1a-12", "2.4-mathematics-L02", "L02 Props 1.3, 1.5, 2.2; Remarks 1.6, 1.7; Problems R1, R2", "PASS",
        CARRY_L02 + "pi(q) = pi0 - k(q-q0)^2 with pi0 = (p-c)^2/(4k) - F re-derived (rederive_slice_a_r5.out)."),
    row("E1a-13", "2.4-mathematics-L03", "L03 Prop 1.3 (l.79-84), Remark 1.4, Prop 2.1, Problems P1-P2", "PASS",
        CARRY_L01 + "Z(p) linear with slope -b on [0,c] and -(b+s) on [c,inf); p* - c = (a-bc)/(b+s) > 0 (rederive_slice_a_r5.out)."),
    row("E1a-14", "2.4-mathematics-problems", "L01 R1-R3, M1-M3, P1-P3, E1-E3; L02 R1-R3, M1-M3, P1-P3, E1-E3; L03 R1-R3, M1-M3, P1-P3, P2, E1-E3", "PASS",
        CARRY_L02 + "problem blocks lie outside the l.247 hunk; L01 and L03 byte-identical; numeric claims re-derived in " + S + "rederive_slice_a_r5.out (identical to round 4)."),
    row("E1a-15", "2.4-notation", "hub and L01-L03 math spans vs notation/notation.json (8 registered symbols, 26 macros)", "PASS",
        "Re-run this round: " + S + "notation_scan_r5.out identical to the round-4 output (cmp). notation/ is unchanged in the delta. The round-5 L02.html hunk (l.247) adds no math span; its only math is \\(-F\\), which was already present. Lesson-local letters are not registered."),
    row("E1a-16", "2.5-labs-L01", "tests/labs/E1/lab-E1-L01-1.py; course/modules/E/E1/L01.html lab section (l.156-259)", "PASS",
        "Re-run this round: `tools/run_labs.py --unit E1 --page L01` -> 'run_labs E1: PASS (1/1)', exit 0 (" + S + "run_labs_L01_r5.out); `python -I -W error tests/labs/E1/lab-E1-L01-1.py` exit 0, stderr 0 bytes (twin_L01_r5.err); twin unchanged in the delta; page code equals twin (twin_vs_page_r5.out)."),
    row("E1a-17", "2.5-labs-L02", "tests/labs/E1/lab-E1-L02-1.py lines 86-94 (computed comparison, print at 91-93) and docstring lines 9-11; course/modules/E/E1/L02.html:130 (hypothesis), :228-246 (expected block), :247 (interpretation)", "PASS",
        "Re-run this round: the round-3 'printed but not computed' FAIL stays resolved. The twin computes below = pi_avg < pi_at_q_star and prints 'case 1 at the minimum-average-cost output sqrt(F/k) = 3.4641: profit 3.7128, below the profit 4.0000 at q*: True' (twin_L02_r5.out last line; 16 sqrt 3 - 24 = 3.7128 < 4 checked by hand). The round-5 interpretation at L02.html:247 now restricts that computation to 'case 1' and matches the twin's 'for case 1 only' docstring. The expected block (L02.html:246) equals the stdout (twin_vs_page_r5.out). `run_labs --page L02` PASS (run_labs_L02_r5.out); twin exit 0 under -I -W error, stderr empty."),
    row("E1a-18", "2.5-labs-L03", "tests/labs/E1/lab-E1-L03-1.py docstring; course/modules/E/E1/L03.html:113-223", "PASS",
        "Re-run this round: `tools/run_labs.py --unit E1 --page L03` -> PASS (1/1) (run_labs_L03_r5.out); twin exit 0 under -I -W error (twin_L03_r5.out, twin_L03_r5.err 0 bytes); L03.html byte-identical; page code equals twin and expected block equals stdout (twin_vs_page_r5.out). Counts 110 / 1 / 30 and grid maximiser 48/7 reproduced (twin_L03_r5.out)."),
    row("E1a-19", "2.9-prose-scope-words (rule 4)", "L01.html:268; L02.html:247 (round-5 changed sentence); L01-L03 scope words", "PASS",
        "Re-run this round: " + S + "prose_scans_r5.py -> prose_scans_r5.out, identical to the round-4 scan (cmp, exit 0). L02.html:247 now reads 'So, in case 1, the minimum-average-cost output does not maximize profit'; the qualifier is correct because the lab computes case 1 only (twin_L02_r5.out last line). L01.html:268 is byte-identical to round 4 and its 'any given prices and income' is Prop 1.4, proved for every positive p_x, p_y, m (L01.html:94-95)."),
    row("E1a-20", "2.5-labs-runtime-seed-network", "the three L01-L03 twins", "PASS",
        "Re-run this round: `python -I -W error` exit 0 for lab-E1-L01-1.py, lab-E1-L02-1.py, lab-E1-L03-1.py (stderr empty). Twins are byte-identical to the round-4 pin (delta_files_slice_a_r5.out lists no L01-L03 twin). `ruff check tests/labs/E1` 'All checks passed!' and `ruff format --check tests/labs/E1` '12 files already formatted' (" + S + "ruff_check_E1_labs_r5.out, ruff_format_E1_labs_r5.out). `mypy --no-incremental` on the three twins 'Success: no issues found in 3 source files' (mypy_slice_a_twins_r5.out). `pytest tests/test_page_checks.py tests/test_run_labs.py -q` exit 0 (pytest_page_checks_run_labs_r5.out)."),
    row("E1a-21", "2.7-cards-L01", "cards.json E1-c001..c014, c137, c139 (16 L01 cards)", "PASS",
        "Re-run this round (card_identity_r5.py -> card_identity_r5.out): the 16 L01 cards changed only in the five fronts E1-c004, c005, c006, c009, c010, which now begin 'Under the Setting (p_x > 0, p_y > 0, m > 0)' and match the Setting block at L01.html:56-59. Backs unchanged. c006 back (m/(2 p_x), m/(2 p_y)), u_bar = m^2/(4 p_x p_y) matches Prop 1.4 (L01.html:94-95). c001, c002, c003, c007, c008, c011-c014, c137, c139 unchanged. Slice-a card ids and lessons are the round-4 set (16/15/11)."),
    row("E1a-22", "2.7-cards-duplicates", "cards.json: full scan of all E1 cards (now 156)", "PASS",
        "Re-run this round: " + S + "cards_scan_r5.py -> cards_scan_r5.out: 156 cards, 156 unique ids, 0 duplicate fronts, 0 duplicate backs. 21 near-duplicate pairs (Jaccard >= 0.45) reviewed. New pairs from the round-5 delta: E1-c159/c160 (0.73; Cournot vs Bertrand volume, fee, profit: 200/3, 160/3, 20000/9 -> 2222 vs 100, 20, 0), E1-c088/c159 (0.66) and c088/c160 (0.71) (c088 is now monopoly only: 50, 70, 2500). Distinct questions, distinct answers. Other pairs as in round 4 (c097/c098/c099 distinct surpluses; c018/c023; c041/c155; c156-c158). No two cards state the same fact in the same words."),
    row("E1a-23", "2.7-cards-L02", "cards.json E1-c015..c027, c140, c152 (15 L02 cards)", "PASS",
        "Re-run this round: changed cards E1-c019 (back now opens 'Under the Setting (p > 0, F >= 0, c >= 0, k > 0)', matching L02.html:56-59 with q >= 0) and E1-c024 (front now names Lab 1 case 1, p = 10, c = 2, k = 1, F = 12, matching the Lab 1 case 1 line of the expected block). c024 back: AC'(q) = k - F/q^2 (L02.html:266); 16 sqrt(3) - 24 = 3.7128 < 4 (twin_L02_r5.out). c025, c027, c140, c152 unchanged; their numbers are printed by twin_L02_r5.out (see E1a-10)."),
    row("E1a-24", "2.7-cards-L03", "cards.json E1-c028..c035, c037, c141, c142 (11 L03 cards; E1-c036 absent)", "PASS",
        "Re-run this round: E1-c033 back now opens 'Under the Setting (a > 0, b > 0, c >= 0, k > 0, a > bc, n >= 1)', which is the L03.html:56-59 Setting, and Prop 2.1 (L03.html:99-100) is stated for every F >= 0. E1-c142 back now cites 'Lesson 2, Proposition 1.5; Lab 1' (L02.html:92 is Prop 1.5); 48/7 in both cases (twin_L03_r5.out). Other cards unchanged; c141 110/1/30 matches twin_L03_r5.out."),
    row("E1a-25", "2.7-cards-coverage", "L01-L03 definitions, propositions and misconceptions vs cards", "PASS",
        "Re-run this round: " + S + "coverage_lesson_only_r5.py -> coverage_lesson_only_r5.out (lesson-restricted matching). Every Definition/Proposition block has a card in the same lesson: L01 Def 1.1 c001, Prop 1.2 c004, Prop 1.3 c005/c011, Prop 1.4 c006/c007/c010/c014, Def 2.1 c003, Prop 2.2 c009/c012, Prop 2.3 c010/c013/c139; L02 Def 1.1 c015, Def 1.2 c016/c017, Prop 1.3 c018/c022/c027/c152, Prop 1.5 c019/c025, Def 2.1 c022, Prop 2.2 c023; L03 Def 1.1 c028, Def 1.2 c029, Prop 1.3 c030/c037, Prop 2.1 c033. The three misconceptions per lesson: L01 c011 (maximizing = buying as much as possible), c012 (MRS = ratio of quantities), c013 (MRS = price ratio at every bundle); L02 c024 (min average cost), c019 (fixed cost lowers output), c026 (shut down on negative profit); L03 c034 (one firm's supply = market supply), c035 (shortage above p*), c033 (fixed cost raises price)."),
    row("E1a-26", "2.9-structure-hub", "course/modules/E/E1/index.html", "PASS",
        "Re-run this round: `tools/check_pages.py --unit E1` -> 'check_pages E1: PASS', exit 0 (" + S + "check_pages_E1_r5.out). The per-page form `--page index` is not a valid invocation for the hub (round-4 finding, unchanged); the hub is evidenced by the unit run."),
    row("E1a-27", "2.9-structure-lessons", "L01.html, L02.html, L03.html", "PASS",
        "Re-run this round: `tools/check_pages.py --unit E1 --page L01`, `--page L02`, `--page L03` -> PASS each (check_pages_L01_r5.out, check_pages_L02_r5.out, check_pages_L03_r5.out). Each exit 0."),
    row("E1a-28", "2.9-banned-phrases-process-words", "index.html, L01.html, L02.html, L03.html (learner text, code and expected blocks excluded)", "PASS",
        "Re-run this round: " + S + "banned_r4_r5.py -> banned_r5.out: no BANNED/PROCESS hit for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, verifier, builder, REQUEST, unit report; no ellipsis outside code. The single 'round' hit is inside 'rounded' (L03.html), not a process word. The round-5 L02.html:247 sentence contains none of these."),
    row("E1a-29", "2.9-gates", "unit E1 (hub and L01-L03) and the repo gates that touch these files", "PASS",
        "Re-run this round at dde0486b: check_pages --unit E1 PASS; check_dag --unit E1 PASS (check_dag_E1_r5.out); check_projects --unit E1 PASS; run_labs --page L01/L02/L03 PASS (1/1 each); page_smoke `tools/page_smoke.py --unit E1 --pages index L01 L02 L03` 'page_smoke E1: PASS', exit 0 (page_smoke_slice_a_r5.out); verify_refs offline PASS and live E1 PASS (E1a-01); ruff and mypy PASS on the twins (E1a-20)."),
    row("E1a-30", "2.9-DAG", "index.html; L01-L03 concept links and dfn; L02.html:51 ('Definition 2.1 below')", "PASS",
        "Re-run this round: `tools/check_dag.py --unit E1` PASS (check_dag_E1_r5.out). L02.html:51 is unchanged; 'Definition 2.1' is defined at L02.html:114, inside the lesson. The round-5 L02.html:247 sentence introduces no concept link."),
    row("E1a-31", "2.9-hours", "index.html data-hours-lessons=90, data-hours-project=30; L01-L03 data-hours=10", "PASS",
        "Re-run this round: check_pages --unit E1 PASS (hours rules). index.html data-hours-lessons=\"90\", data-hours-project=\"30\" (static_checks_r5.out); L01-L03 and the hub card kickers 'L0x · 10 h'. Arithmetic: 9 x 10 = 90; 90 + 30 = 120; 30/120 = 25 %. The curriculum total is 120 (curriculum/curriculum.json, E1 'hours')."),
    row("E1a-32", "2.9-hub-vs-lessons", "index.html lesson cards and objectives; L01 h1 (l.35) 'Consumer Choice'; L02 h1 (l.35) 'Producer Choice and Cost'; L03 h1 (l.35) 'Competitive Equilibrium'", "PASS",
        "Re-run this round (static_checks_r5.out): hub lesson card titles equal the h1 values in order (Consumer Choice; Producer Choice and Cost; Competitive Equilibrium); hub kickers 'L01-L03 · 10 h' equal the lesson eyebrows '10 study hours'. The only round-5 hub change is the eyebrow (E1a-02)."),
    row("E1a-33", "2.1-attribution (rule 3)", "L01-L03 prose; L01.html:498; L02.html:488; L03.html:464; references/references.json varian2014intermediate", "PASS",
        CARRY_L02 + "references/ unchanged (delta_files_slice_a_r5.out); the reference sections are outside the l.247 hunk. No page, table or locator is attributed to varian2014intermediate."),
    row("E1a-34", "2.9-scope-words-prose", "L01-L03 prose (every, all, always, never, any, only, exactly, each)", "PASS",
        "Re-run this round: prose_scans_r5.out identical to the round-4 scan (cmp, exit 0). The changed sentences (L02.html:246-247) are scoped: 'for case 1 only' and 'So, in case 1'. The generalisation of round 4 (E1a-38) is removed; see E1a-38."),
    row("E1a-35", "2.8-data-figures", "index.html; L01.html; L02.html; L03.html (no figures, no data-files)", "PASS",
        "Re-run this round: grep -c 'data-files|<svg|<img' on the four pages: 0 each (static_checks_r5.out). No dataset, chart or SIMULATED label is required on these pages."),
    row("E1a-36", "2.9-stray-file (twin directory hygiene)", "tests/labs/E1/", "PASS",
        "Re-run this round: `ls tests/labs/E1` lists exactly the twelve lab-E1-*.py files (L01-L09, project-1..3) (" + S + "ls_tests_labs_E1_r5.out). No backup or stray copy."),
    row("E1a-37", "2.9-prose (learner claim vs page)", "course/modules/E/E1/L01.html:268 (Section 3, bullet 4)", "PASS",
        CARRY_L01 + "L01.html:268 unchanged since round 4. Its statement 'Proposition 1.4 gives the optimal bundle at any given prices and income, so x_bar = m/(2 p_x) is an explicit function of p_x' matches L01.html:94-95 (x_bar = m/(2 p_x)); M3 (L01.html:311-314) works one change in income. The round-3 FAIL is resolved."),
    row("E1a-38", "2.9-prose / rule 4 (generalisation from one case)", "course/modules/E/E1/L02.html:247 (interpretation)", "PASS",
        "Re-run this round, fresh: round-4 FAIL resolved. L02.html:247 now reads 'So, in case 1, the minimum-average-cost output does not maximize profit: its profit is about 3.71, against 4 at the optimum' (delta_slice_a_hunks_r5.diff). The qualifier matches the lab, which computes the comparison for case 1 only (twin_L02_r5.out last line; twin docstring lines 9-11). Counter-check: with p = 2, c = 0, F = 1, k = 1, sqrt(F/k) = 1 = q*, so the unqualified sentence would be false; the qualified one is true."),
]

fragment = {
    "unit": "E1",
    "slice": "a",
    "round": 5,
    "verifier": "independent Haiku verifier, round 5, slice a (claude-haiku-5-5); did not build E1",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "edbb7aa8de20e6d2f3035c463a79a318c22623c4 (round-4 pin; round-4 fragment /Users/billyribeiro/.fanout/frags/S-E1-a.round4.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS5-E1-a",
    "scratch": S,
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta from the round-4 pin edbb7aa8 to dde0486b in the slice: course/modules/E/E1/index.html (l.42 eyebrow), L02.html (l.247 interpretation), cards.json (slice-a cards E1-c004, c005, c006, c009, c010, c019, c024, c033, c142; new cards E1-c159, c160 are L06 and are checked only by the full duplicate scan). Other E1 files in the delta (L04, L06, L07, project.html, lab-E1-L04-1.py, lab-E1-project-1.py) are outside slice a. plans/KNOWN-ISSUES.md and plans/FINAL-ARCHITECT-RULINGS.md changed in the delta; they concern E3 and are not slice-a subjects.",
        "Round-4 non-PASS row E1a-38 (LOW, generalisation of a case-1 result in L02.html:247) is fixed in the page and re-verified fresh; it is not listed in KNOWN-ISSUES.md.",
        "Scripts under ledgers/E1/scripts/E1-a-r5/ are all this round's (rederive_slice_a_r5.py etc. are copies of the round-4 scripts with output compared by cmp). Two tracked files already present in that directory (card_term_checks.py, embed_vs_run.py) were not run and are not evidence.",
        "Definition and theorem cards without a grade field (c001-c003, c015-c017, c022, c028-c029 and others) follow BUILDER_RULES section 7: only graded results other than theorems carry a grade, so this is not a finding.",
        "Mutants: not applicable to slice a (lab twins are demonstrations; no project grader in slice a). The mutants list is empty by design.",
        "Not checked: a live Crossref resolution of varian2014intermediate beyond verify_refs --unit E1 (the registry was not changed, so no new live claim was needed); no browser screenshot was taken beyond page_smoke.",
    ],
    "summary": "Slice a (hub index.html, L01-L03, their twins and slice cards), round 5, pin dde0486b: 38 rows, 38 PASS, 0 FAIL, 0 UNVERIFIABLE. Round-4 FAIL E1a-38 is fixed (L02.html:247 now scopes the case-1 result) and re-verified. All slice gates pass at dde0486b: check_pages (unit and per lesson), check_dag, check_projects, run_labs (L01-L03), twins under python -I -W error, page_smoke (index, L01-L03), verify_refs offline and live E1, ruff, mypy, pytest test_page_checks and test_run_labs.",
}

problems = []
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

problems = ledger.validate(fragment, "E1-a")
print("validate:", problems)
out = ROOT / "ledgers/E1/E1-a.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", sum(r["status"] == "PASS" for r in rows))
