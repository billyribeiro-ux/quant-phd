"""Writes the round-4 slice-a fragment (E1, slice a) from the evidence files in this directory (verifier, round 4)."""
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
S = "ledgers/E1/scripts/E1-a-r4/"
CARRY = "Carried from round 3 (cited passages byte-identical since the round-3 pin 8196077d; round-4 delta outside them): "
RERUN = "Re-run this round: "
OUT = []


def row(i, check, loc, status, ev, fix=None, severity=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        d["fix"] = fix
        d["severity"] = severity
    OUT.append(d)


row("E1a-01", "2.1-citations", "references/references.json key varian2014intermediate; course/modules/E/E1/index.html; L01.html:498; L02.html:488; L03.html:464", "PASS",
    RERUN + "`.venv/bin/python tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems' (exit 0, " + S + "verify_refs_offline_r4.out); `tools/verify_refs.py --unit E1` -> 'live re-verification of E1: 1 of 560 entries, 0 problems' (exit 0, " + S + "verify_refs_unit_E1_live_r4.out). The reference sections L01.html:498, L02.html:488, L03.html:464 say only varian2014intermediate is cited and no locator is attributed; the registry entry is unchanged (references/ not in the round-4 delta).")
row("E1a-02", "2.2-numbers-hub", "course/modules/E/E1/index.html (objectives, hours split, placement)", "PASS",
    CARRY + "index.html is byte-identical to the round-3 pin (git diff empty). " + S + "rederive_slice_a_r3_r4.out is byte-identical to the round-3 output (cmp), the script re-run this round: 9-question placement arithmetic (7/9 = 77.8 %, 8/9 = 88.9 %, ceil(0.8*9) = 8) and hours 9x10 = 90, 90+30 = 120 hold.")
row("E1a-03", "2.2-numbers-L01", "L01.html Example 1.6 (l.116), Remark 1.5 (l.111), Remark 2.4 (l.153), Problems M1-M3, P1-P3, E1-E3, R1-R3, quiz (ll.297-492)", "PASS",
    RERUN + "`.venv/bin/python -I " + S + "rederive_slice_a_r3_r4.py .` (copy of the round-3 script) -> " + S + "rederive_slice_a_r3_r4.out, identical to round 3: x_bar=30, y_bar=20, u_bar=600 (Example 1.6); Remark 2.4: y=80/3, MRS 4/3, 80/63 offset, 1600/63, 38/3 gain. The only round-4 L01 hunk is l.268, outside these passages.")
row("E1a-04", "2.2-numbers-L02", "L02.html Example 1.4 (l.88), Remark 1.6 (l.103), Misconception 1 (l.264-266), Problems and quiz (ll.280-472)", "PASS",
    RERUN + S + "rederive_slice_a_r3_r4.py (output identical to round 3): Example 1.4 q*=4, C(4)=36, profit 4, MC(4)=10; F=100 profit -84; sqrt(12) profit 16 sqrt(3) - 24 = 3.7128 (l.266). The round-4 L02 hunks (l.51, l.219-221, l.244-246) do not contain these numbers.")
row("E1a-05", "2.2-numbers-L03", "L03.html Example 1.5 (l.93), Remark 2.2 (l.110), Problems (ll.262-349), quiz (ll.389-449)", "PASS",
    CARRY + "L03.html is byte-identical to the round-3 pin. " + S + "rederive_slice_a_r3_r4.out (identical to round 3): p*=110/7, Q*=480/7, S(p*)=480/7; grid i/7, i=0..140: 110 positive, 1 zero, 30 negative; p*-c=(a-bc)/(b+s).")
row("E1a-06", "2.2-numbers-lab-printed", "L01 expected block (L01.html:240-257); L02 expected block (L02.html:228-246); L03 expected block (L03.html:215-222)", "PASS",
    RERUN + "`.venv/bin/python -I " + S + "twin_vs_page_r4.py .` -> " + S + "twin_vs_page_r4.out: for L01, L02, L03 the page code equals the twin (True) and the expected block equals the twin's stdout under `python -I -W error` (True). The L02 expected block now carries the new comparison 'below the profit 4.0000 at q*: True', which the twin prints.")
row("E1a-07", "2.2-numbers-prose / 2.3-mathematics", "L01.html:153 (Remark 2.4), L01.html:307 (M2)", "PASS",
    CARRY + "the passages at L01.html:153 and :307 are unchanged; the round-4 delta touches L01.html only at l.268. Remark 2.4 values re-derived by " + S + "rederive_slice_a_r3_r4.out (identical to round 3).")
row("E1a-08", "2.3-grades-propositions", "L01 Props 1.2 (l.72), 1.3 (l.82), 1.4 (l.92-95), 2.2 (l.131), 2.3 (l.141); L02 Props 1.3 (l.72), 1.5 (l.91), 2.2 (l.118); L03 Props 1.3 (l.72), 2.1 (l.98)", "PASS",
    CARRY + "those proposition blocks lie outside the round-4 hunks (L01 l.268; L02 l.51, l.219-221, l.244-246). Grades T with complete proofs re-read this round; Prop 1.4 (L01.html:95) gives x_bar = m/(2 p_x), which the round-4 L01 sentence at l.268 quotes correctly.")
row("E1a-09", "2.3-grades / 2.4-mathematics / 2.9-prose", "L02.html:130 (hypothesis), L02.html:262-266 (misconception 1)", "PASS",
    CARRY + "L02.html:130 and :262-266 are unchanged. AC(q) = F/q + c + kq, AC'(q) = k - F/q^2; minimiser sqrt(F/k) for F > 0; for F = 0 AC rises for every q > 0 (" + S + "rederive_slice_a_r3_r4.out). Profit at sqrt(12) = 16 sqrt(3) - 24 ~ 3.7128 printed by twin_L02.out.")
row("E1a-10", "2.3-grades-lab-results (C cards)", "cards E1-c014, c025, c027, c139, c140, c141, c142 (grade C; basis names Lab 1)", "PASS",
    RERUN + "twin outputs " + S + "twin_L01.out, twin_L02.out, twin_L03.out. c014: point 30 in all four L01 cases (twin_L01.out); c025: profit 4 vs -84 and grid output 4 in both (twin_L02.out); c027: 'equals closed form: True' in all four cases; c139: 'budget exhausted: True' and 'equal: True' in all four; c140: 'producing q* is better: True' in all four; c141: 110 / 1 / 30 (twin_L03.out); c142: 48/7 both. Card objects unchanged (" + S + "card_identity_r4.out: slice-a cards differing = []).")
row("E1a-11", "2.4-mathematics-L01", "L01 Props 1.2-1.4, 2.2, 2.3; Remark 1.5; Problem R2 (l.380-386)", "PASS",
    CARRY + "cited passages unchanged (round-4 L01 hunk is l.268). " + S + "rederive_slice_a_r3_r4.out (identical to round 3) re-checks the Prop 1.4 identity and Problem R2 steps.")
row("E1a-12", "2.4-mathematics-L02", "L02 Props 1.3, 1.5, 2.2; Remarks 1.6, 1.7; Problems R1, R2", "PASS",
    CARRY + "cited passages unchanged (round-4 L02 hunks are l.51, l.219-221, l.244-246). Shift identity pi(q) = pi0 - k(q-q0)^2 with pi0 = (p-c)^2/(4k) - F re-derived (" + S + "rederive_slice_a_r3_r4.out).")
row("E1a-13", "2.4-mathematics-L03", "L03 Prop 1.3 (l.79-84), Remark 1.4, Prop 2.1, Problems P1-P2", "PASS",
    CARRY + "L03.html is byte-identical to the round-3 pin. Z(p) linear with slope -b on [0,c] and -(b+s) on [c,inf); p* - c = (a-bc)/(b+s) > 0 (" + S + "rederive_slice_a_r3_r4.out).")
row("E1a-14", "2.4-mathematics-problems", "L01 R1-R3, M1-M3, P1-P3, E1-E3; L02 R1-R3, M1-M3, P1-P3, E1-E3; L03 R1-R3, M1-M3, P1-P3, P2, E1-E3", "PASS",
    CARRY + "problem blocks are outside the round-4 hunks; numeric claims re-derived in " + S + "rederive_slice_a_r3_r4.out (identical to round 3). The L02 E2 problem (l.343) is unchanged.")
row("E1a-15", "2.4-notation", "hub and L01-L03 math spans vs notation/notation.json (8 registered symbols, 26 macros)", "PASS",
    RERUN + S + "notation_scan_r3_r4.out (identical to round 3): registered macros used in no math span on any of the four pages; no registered-symbol candidate (\\Phi, \\gamma, \\ast, R_f, \\mathbb, T) in math. The new round-4 math span \\bar{x} = m/(2p_x) (L01.html:268) uses no registered symbol. Lesson-local letters (m, p_x, B, M, A, C, F, G, S, Z) are not registered (notation.json symbols list).")
row("E1a-16", "2.5-labs-L01", "tests/labs/E1/lab-E1-L01-1.py; course/modules/E/E1/L01.html lab section (l.156-259)", "PASS",
    RERUN + "`tools/run_labs.py --unit E1 --page L01` -> 'run_labs E1: PASS (1/1)', exit 0 (" + S + "run_labs_L01.out); `python -I -W error tests/labs/E1/lab-E1-L01-1.py` exit 0, stderr 0 bytes (twin_L01.err); page code equals twin (twin_vs_page_r4.out).")
row("E1a-17", "2.5-labs-L02", "tests/labs/E1/lab-E1-L02-1.py lines 86-94 (computed comparison, print at 91-93) and docstring lines 9-11; course/modules/E/E1/L02.html:130 (hypothesis), :228-246 (expected block), :247 (interpretation)", "PASS",
    RERUN + "Round-3 FAIL resolved. The twin now computes `below = pi_avg < pi_at_q_star` and prints it (twin_L02.out last line: 'case 1 at the minimum-average-cost output sqrt(F/k) = 3.4641: profit 3.7128, below the profit 4.0000 at q*: True'); 3.7128 < 4 checked by hand (16 sqrt 3 - 24 = 3.7128). The docstring (lines 9-11) describes this computation; the hypothesis (L02.html:130) predicts 'below'; the expected block equals the stdout (twin_vs_page_r4.out). `run_labs --page L02` PASS (run_labs_L02.out); twin exit 0 under -I -W error (twin_L02.err empty).")
row("E1a-18", "2.5-labs-L03", "tests/labs/E1/lab-E1-L03-1.py docstring; course/modules/E/E1/L03.html:113-223", "PASS",
    RERUN + "`tools/run_labs.py --unit E1 --page L03` -> PASS (1/1) (run_labs_L03.out); twin exit 0 under -I -W error (twin_L03.out, twin_L03.err empty); page code equals twin and expected block equals stdout (twin_vs_page_r4.out). Counts 110 / 1 / 30 and firm grid maximiser 48/7 reproduced (twin_L03.out).")
row("E1a-19", "2.9-prose-scope-words (rule 4)", "L01.html:268, L02.html:247 (new round-4 hunks); L01-L03 scope words", "PASS",
    RERUN + S + "prose_scans_r3_r4.py -> prose_scans_r3_r4.out; each scope word in the changed sentences is checked: L01.html:268 'at any given prices and income' is Prop 1.4, proved for every positive p_x, p_y, m (L01.html:95 and its proof); L02.html:247 'for case 1 only' is a finite statement and is correct as written; the one inference that needs a qualifier is recorded as E1a-38.")
row("E1a-20", "2.5-labs-runtime-seed-network", "the three L01-L03 twins", "PASS",
    RERUN + "`python -I -W error` exit 0 for lab-E1-L01-1.py, lab-E1-L02-1.py, lab-E1-L03-1.py (twin_L0*.err empty). Imports are stdlib (fractions, math); no random calls; no network. `ruff check tests/labs/E1` 'All checks passed!' and `ruff format --check tests/labs/E1` '12 files already formatted' (ruff_check_E1_labs.out, ruff_format_E1_labs.out). `mypy --no-incremental` on the three twins 'Success: no issues found in 3 source files' (mypy_slice_a_twins.out).")
row("E1a-21", "2.7-cards-L01", "cards.json E1-c001..c014, c137, c139 (16 L01 cards)", "PASS",
    CARRY + "card_identity_r4.out: the 16 L01 card objects are identical to the round-3 pin (slice-a cards differing = []). The round-4 delta touches no L01 card. No card refers to the round-4 L01.html:268 sentence (grep 'respon' in cards.json: no L01 hit).")
row("E1a-22", "2.7-cards-duplicates", "cards.json: full scan of all 154 E1 cards", "PASS",
    RERUN + S + "cards_scan_r3_r4.py -> cards_scan_r3_r4.out: 154 cards, 154 unique ids, 0 duplicate fronts, 0 duplicate backs. Near-duplicate pairs (Jaccard >= 0.45) reviewed: E1-c018/c023 ask distinct questions (the profit-maximizing output vs the supply function) with distinct answers; E1-c097/c098/c099 give the surplus of three distinct outcomes; E1-c041 (linear demand threshold) vs new E1-c155 (general definition of elastic/inelastic) are distinct statements; new E1-c156..c158 are definition cards for different concepts. No two cards state the same fact in the same words.")
row("E1a-23", "2.7-cards-L02", "cards.json E1-c015..c027, c140, c152 (15 L02 cards)", "PASS",
    CARRY + "card_identity_r4.out: the 15 L02 card objects are identical to the round-3 pin. c025, c027, c140 remain consistent with the regenerated twin_L02.out (see E1a-10).")
row("E1a-24", "2.7-cards-L03", "cards.json E1-c028..c035, c037, c141, c142 (11 L03 cards; E1-c036 absent)", "PASS",
    CARRY + "card_identity_r4.out: the 11 L03 card objects are identical to the round-3 pin. L03.html is byte-identical.")
row("E1a-25", "2.7-cards-coverage", "L01-L03 definitions, propositions, misconceptions and lab results vs cards", "PASS",
    CARRY + "the slice-a cards are byte-identical objects and each L01-L03 definition, proposition and misconception still has its card (round-3 coverage table). The round-4 lesson hunks (L01 l.268; L02 l.51, l.219-221, l.244-246) change no definition, proposition or misconception.")
row("E1a-26", "2.9-structure-hub", "course/modules/E/E1/index.html", "PASS",
    RERUN + "`tools/check_pages.py --unit E1` -> 'check_pages E1: PASS', exit 0 (" + S + "check_pages_E1.out). The per-page call `check_pages.py --page index` is not a valid invocation (the tool applies lesson rules to the hub; " + S + "check_pages_pages.out, FAIL lines for index), so the hub is evidenced by the unit run only.")
row("E1a-27", "2.9-structure-lessons", "L01.html, L02.html, L03.html", "PASS",
    RERUN + "`tools/check_pages.py --unit E1 --page L01`, `--page L02`, `--page L03` -> PASS each (" + S + "check_pages_pages.out).")
row("E1a-28", "2.9-banned-phrases-process-words", "index.html, L01.html, L02.html, L03.html (learner text, code and expected blocks excluded)", "PASS",
    RERUN + S + "banned_r4.py -> banned_r4.out: no hit for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, verifier, builder, REQUEST, unit report; no ellipsis outside code. The single 'round' hit is inside 'rounded' (L03.html), which is not a process word.")
row("E1a-29", "2.9-gates", "unit E1 (hub and L01-L03) and the repo gates that touch these files", "PASS",
    RERUN + "check_pages --unit E1 PASS; check_dag --unit E1 PASS; check_projects --unit E1 PASS; run_labs --page L01/L02/L03 PASS; page_smoke `tools/page_smoke.py --unit E1 --pages index L01 L02 L03` PASS, zero console errors, no horizontal scroll at 360 px, no external request (page_smoke_slice_a_r4.out, exit 0, 12.1 s); verify_refs offline PASS; ruff and mypy PASS on the twins (E1a-20).")
row("E1a-30", "2.9-DAG", "index.html; L01-L03 concept links and dfn; L02.html:51 ('Definition 2.1 below')", "PASS",
    RERUN + "`tools/check_dag.py --unit E1` PASS (" + S + "check_dag_E1.out); links_r3_r4.out 'links checked 72, problems 0'. The round-4 L02.html:51 sentence refers forward to Definition 2.1, which L02.html:114 defines (section 2, supply function), so the reference is inside the lesson and not a use before definition.")
row("E1a-31", "2.9-hours", "index.html data-hours-lessons=90, data-hours-project=30; L01-L03 data-hours=10", "PASS",
    RERUN + "check_pages --unit E1 PASS (hours rules). Arithmetic: 9 x 10 = 90; 90 + 30 = 120; 30/120 = 25 %. Hub and lesson data-hours attributes are unchanged by the round-4 delta (hunks touch text only).")
row("E1a-32", "2.9-hub-vs-lessons", "index.html lesson cards and objectives; L01 h1 (l.35) 'Consumer Choice'; L02 h1 (l.35) 'Producer Choice and Cost'; L03 h1 (l.35) 'Competitive Equilibrium'", "PASS",
    CARRY + "index.html is byte-identical; the h1 lines L01.html:35, L02.html:35, L03.html:35 are outside every round-4 hunk. Card titles equal the h1 values (round-3 check).")
row("E1a-33", "2.1-attribution (rule 3)", "L01-L03 prose; L01.html:498; L02.html:488; L03.html:464; references/references.json varian2014intermediate", "PASS",
    CARRY + "the reference sections are outside the round-4 hunks; references/references.json is byte-identical (no change under references/ in the delta). Only varian2014intermediate is cited; no page, table or locator is attributed to it.")
row("E1a-34", "2.9-scope-words-prose", "L01-L03 prose (every, all, always, never, any, only, exactly, each)", "PASS",
    RERUN + "prose_scans_r3_r4.out lists every scope-word hit with context; the diff against round 3 contains only the changed sentences (L01.html:268 'any'; L02.html:246-247 'each', 'only'). Universal sentences are proved or finite statements about named cases (see E1a-19). The L02 sentence that generalises case 1 is recorded as E1a-38.")
row("E1a-35", "2.8-data-figures", "index.html; L01.html; L02.html; L03.html (no figures, no data-files)", "PASS",
    RERUN + "grep -c 'data-files|<svg|<img' on the four pages: 0 each (static_checks_r4.out). No dataset, no chart, no SIMULATED label required on these pages.")
row("E1a-36", "2.9-stray-file (twin directory hygiene)", "tests/labs/E1/", "PASS",
    RERUN + "`ls tests/labs/E1` lists exactly the twelve lab-E1-*.py files (L01-L09, project-1..3); no backup or stray copy (static_checks_r4.out).")
row("E1a-37", "2.9-prose (learner claim vs page)", "course/modules/E/E1/L01.html:268 (Section 3, bullet 4)", "PASS",
    RERUN + "Round-3 FAIL resolved. The sentence now reads 'Proposition 1.4 gives the optimal bundle at any given prices and income, so x_bar = m/(2p_x) is an explicit function of p_x, and problem M3 works one change in income. The lesson does not analyze how an equilibrium responds to a change in a parameter.' Checked against L01.html:95 (Prop 1.4: x_bar = m/(2 p_x)), L01.html:311-314 (M3 'Doubling income'), and L04 being comparative statics (curriculum). No contradiction remains with the bullet heading.")
row("E1a-38", "2.9-prose / rule 4 (generalisation from one case)", "course/modules/E/E1/L02.html:247 (interpretation, sentence 'So the minimum-average-cost output does not maximize profit')", "FAIL",
    RERUN + "The lab computes the comparison for case 1 only (twin_L02.out last line; docstring lines 9-11; L02.html:247 'for case 1 only'). The next sentence then states 'So the minimum-average-cost output does not maximize profit' with no case qualifier. Read generally this is false on the Setting: p = 2, c = 0, F = 1, k = 1 gives sqrt(F/k) = 1 = q* (profit -(q-1)^2 is maximised at q = 1), so the minimum-average-cost output does maximize profit there. The sentence is correct for case 1.",
    fix="L02.html:247: replace 'So the minimum-average-cost output does not maximize profit' with 'So, in case 1, the minimum-average-cost output does not maximize profit'. Rebuild the page only if the embed tool requires it; the twin is unchanged.",
    severity="LOW")

frag = {
    "unit": "E1",
    "slice": "a",
    "round": 4,
    "verifier": "independent Haiku verifier, round 4, slice a (claude-haiku-5-5); did not build E1",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4 (round-3 pin; round-3 fragment /Users/billyribeiro/.fanout/frags/S-E1-a.round3.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-E1-a",
    "scratch": "ledgers/E1/scripts/E1-a-r4/ (all evidence scripts and outputs are kept in the repository path)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": OUT,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since round-3 pin (git diff --stat 8196077d edbb7aa8, slice files): L01.html 1 line (l.268), L02.html lines 51, 219-221, 244-246, tests/labs/E1/lab-E1-L02-1.py (computed comparison), cards.json (E1-c038/c072/c089-c091/c104/c114/c128 and new c155-c158; none of them is a slice-a card), and project/L04/L06-L09 files outside this slice. index.html, L03.html, references/, notation/, tools/ and the other L01-L03 twins are byte-identical.",
        "Round-3 FAIL E1a-17 (L02 lab printed 'below' without computing it) is resolved: the twin computes the comparison; the expected block and interpretation match. Round-3 FAIL E1a-37 (L01 bullet denied that the lesson states the price response) is resolved: L01.html:268 now cites Proposition 1.4's explicit formula.",
        "Ruling 26 severity: the only non-PASS row (E1a-38) is wording (LOW, generalisation from one case). No row is a false or unproved mathematical statement, a missing hypothesis, a wrong number, an over-graded claim, a failing gate, a surviving non-equivalent mutant, or a lab statement the code does not support. Under ruling 26 the slice is accepted if E1a-38 is fixed or listed in plans/KNOWN-ISSUES.md.",
        "ledgers/E1/scripts/E1-a-r4/ already held three tracked files from another round (card_and_term_checks.py, embed_vs_run.py, make_fragment.py, commit 09b87514); they were not run and are not evidence for this fragment. ledgers/E1/E1-a.json held a round-8 fragment of another campaign (pin ce7b3821); it is overwritten in this checkout only, as the assignment requires.",
        "Mutants: not applicable to slice a (lab twins are demonstrations; ruling in verifier-rules). mutants list is empty.",
        "Carried rows: PASS rows whose cited passages lie outside the round-4 hunks are carried with the prefix; rows re-run this round are marked 'Re-run this round'.",
    ],
    "summary": "Slice a (hub index.html, L01-L03, their lab twins and slice cards): 38 rows, 37 PASS, 1 FAIL (E1a-38, LOW, wording: a case-1 result generalised in one sentence of L02.html:247). Round-3 FAILs E1a-17 and E1a-37 are resolved and re-verified. All gates on this slice PASS at edbb7aa8: check_pages, check_dag, check_projects, run_labs (L01-L03), twins under -I -W error, page_smoke (index, L01-L03), verify_refs offline and live, ruff, mypy.",
}
problems = []
for r in OUT:
    if not r.get("evidence", "").strip():
        problems.append(r["id"])
    if r["status"] != "PASS" and not r.get("fix"):
        problems.append(r["id"] + " no fix")
print("rows", len(OUT), "PASS", sum(r["status"] == "PASS" for r in OUT), "non-PASS problems", problems)
Path(ROOT, "ledgers/E1/E1-a.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
