import json, sys
O = "ledgers/AC4/scripts/AC4-b-r30/out/"
M = "ledgers/AC4/mutants/AC4-b-r30/"
S = "ledgers/AC4/scripts/AC4-b-r30/"
L03 = "course/modules/AC/AC4/L03.html"
L04 = "course/modules/AC/AC4/L04.html"
T03 = "tests/labs/AC4/lab-AC4-L03-1.py"
T04 = "tests/labs/AC4/lab-AC4-L04-1.py"
rows = []

def row(rid, check, location, evidence, status="PASS", fix=""):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    rows.append(d)

# ---- command rows (re-run this round) ----
row("AC4b-cmd-pin", "2.9-structure", "git HEAD of /tmp/verify30-AC4-b",
    "HEAD 5aeaaf0 (detached), git status clean apart from the untracked .venv symlink. Delta base: the round-29 fragment "
    "file on disk (/tmp/fanout-frags/AC4-b.round29.json) records pin 503d139 and contains one row only, so the delta was "
    "computed from 503d139 to 5aeaaf0 (a superset of any later delta). Changed in slice: course/modules/AC/AC4/L03.html "
    "(Gamma notation, Prop 2.2 one-year assumption, Lab 1 interpretation, Misconception 1-2, P1), L04.html (why-it-matters, "
    "Lab 1 docstring line, Misconception 1 ratio), lab-AC4-L03-1.py and lab-AC4-L04-1.py docstrings, cards.json (L02/L06 only "
    "in this window; no L03/L04 card object changed).")
row("AC4b-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit AC4 --page L03; --page L04",
    "Output " + O + "check_pages_L03.out 'check_pages AC4 L03: PASS' rc=0; " + O + "check_pages_L04.out 'check_pages AC4 L04: PASS' rc=0.")
row("AC4b-cmd-check_dag", "DAG/concepts", "tools/check_dag.py --all",
    "Output " + O + "check_dag.out: 'check_dag AC4: PASS' (and all other units PASS), rc=0.")
row("AC4b-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit AC4 --page L03; --page L04",
    "Output " + O + "run_labs_L03.out 'run_labs AC4: PASS (1/1)' rc=0; " + O + "run_labs_L04.out 'run_labs AC4: PASS (1/1)' rc=0. "
    "The page filter limits the run to the slice; the other AC4 labs belong to other slices.")
row("AC4b-cmd-twins-isolated", "2.5-labs",
    "tests/labs/AC4/lab-AC4-L03-1.py; tests/labs/AC4/lab-AC4-L04-1.py under python -I -W error",
    "Ran both twins directly: rc=0 both, stderr 0 bytes (" + O + "twin_L03.out/.err, twin_L04.out/.err). Compared each "
    "page's <pre class=\"expected\"> block (html-unescaped) with the twin stdout: equal for both. The data-run code block "
    "(html-unescaped) equals the twin file for both. Runtime 0.0 s per lab in page_smoke.")
row("AC4b-cmd-page_smoke", "2.5-labs", "tools/page_smoke.py --unit AC4 --pages L03 L04 --skip-sweep",
    "Output " + O + "page_smoke.out: 'page_smoke modules/AC/AC4/L03.html: PASS', 'page_smoke modules/AC/AC4/L04.html: PASS', "
    "'page_smoke AC4: PASS', rc=0. Lab timing 0.0 s each (limit 10 s). --skip-sweep was used because the figure sweep "
    "covers figures, which these lessons do not contain.")
row("AC4b-cmd-ruff-mypy", "gates", "ruff check and ruff format --check on the two twins; mypy --no-incremental on the twins",
    "Output " + O + "ruff.out 'All checks passed!' and '2 files already formatted', rc=0; " + O + "mypy.out 'Success: no issues "
    "found in 2 source files', rc=0.")
row("AC4b-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit AC4",
    "Output " + O + "verify_refs_offline.out 'offline integrity: 560 entries, 0 problems' rc=0; " + O + "verify_refs_live_unit.out "
    "'live re-verification of AC4: 2 of 560 entries, 0 problems' rc=0. The live check fetched the two AC4 records (see "
    "AC4b-cite-datar2020horngrens and AC4b-cite-kaplan1998cost).")
row("AC4b-cmd-pytest", "gates", "pytest tests/test_labs.py -k 'AC4 and (L03 or L04)'",
    "Output " + O + "pytest.out: two dots, [100%], no failures (the -q summary line was cut by tail; exit status not captured, "
    "so this row rests on the absence of any failure line).", status="PASS")
row("AC4b-cards-L03-L04", "2.7-cards",
    "course/modules/AC/AC4/cards.json: every L03 and L04 card (AC4-c031..c044, c045..c058, c121..c124, c126, c131, c136, c122)",
    "Re-read each card back against the current lesson text. No card contradicts its lesson. Card AC4-c033 gives the "
    "make-or-buy difference at 25,000.00 CU without its sign (the lesson says in favour of making); the card does not "
    "contradict the lesson, so PASS. Card AC4-c040 names 25,000.00, AC4-c126 names 11.10 and 10.50, AC4-c041 names 9.25: "
    "each matches Lab 1 output. Duplicate scan: no duplicate card ids or fronts among the 141 cards.")
row("AC4b23-cards-c037", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c037; " + L03 + " Proposition 1.2 (lines 63-69)",
    "Card back 'The two totals differ by the difference of their relevant costs, so the common cost cancels' matches the "
    "Gamma_A - Gamma_B = R_A - R_B proof on lines 64 and 69 after the Gamma rename; object unchanged since 503d139.")
row("AC4b23-cards-c136", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c136; " + L03 + " Remark 1.3 (line 74)",
    "Card back cites Proposition 1.2 and Remark 1.3; Remark 1.3 on line 74 states the proposition gives no profit. PASS.")
row("AC4b23-card-identity", "2.7-cards", "course/modules/AC/AC4/cards.json (L03 and L04 card objects)",
    "git diff 503d139 5aeaaf0 -- course/modules/AC/AC4/cards.json shows hunks only for AC4-c016, c023, c026, c074, c078, "
    "c135 and the new c141 (L02, L06). No L03 or L04 card object changed in this window.")
row("AC4b23-card-numbers", "2.7-cards", "every number on L03 and L04 card backs",
    "Scripted check (run this round): each digit string on each card back appears in the html-stripped lesson text. "
    "Zero missing for all 32 L03/L04 cards.")
row("AC4b23-prose-changed-cards", "2.9-structure", "cards AC4-c037, AC4-c136 (carried prose)",
    "Both cards are unchanged; each sentence was re-read against the current lesson text this round (see AC4b-cards-L03-L04). PASS.")
row("AC4b-hours-L03-L04", "hours", "L03.html and L04.html data-hours attribute and eyebrow; plans/AC4-build-plan.md hours table",
    "L03 data-hours=6, L04 data-hours=6, both eyebrows '6 study hours'. Plan table lessons L01..L08 = 6+7+6+6+7+6+6+6 = 50, "
    "hub data-hours-lessons=50 (course/modules/AC/AC4/index.html line 29). Lesson hours sum to the hub split. The pace of "
    "the lessons is not tested (architect ruling: hours are design targets).")
row("AC4b23-hub-hours", "hours", "course/modules/AC/AC4/L01..L08.html data-hours; index.html line 29",
    "Lesson data-hours values 6,7,6,6,7,6,6,6 (sum 50) match the hub split 50/20 and the plan's hour table. PASS.")
row("AC4b23-slice-delta", "2.9-structure", "git diff 503d139 5aeaaf0 for the slice files",
    "Every hunk in L03.html, L04.html and the two twin docstrings was read (see rows AC4b-L03-*, AC4b-L04-*). No other "
    "slice file changed in this window.")

# ---- notation ----
row("notation-T-L03", "notation: a registered symbol never takes another meaning (BUILDER_RULES 3.2)",
    L03 + " lines 64, 69, 88-98, 433 and the Gamma symbols in Proposition 1.2 and its proof",
    "Re-verified: the previous FAIL (T_A, T_B where T is registered in notation/notation.json as the number of return "
    "observations) is fixed. grep for \\bT\\b in the math of L03 and L04 returns 0. The math tokens of both pages were "
    "listed and compared with the eight registry symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q-blackboard): none "
    "is used with another meaning. Locally defined letters (Gamma, Delta, K, R_A, R_B, Q, m, l, v, F, p, S, h, H, C, c, B, "
    "beta, A, N_k, C_k, A_p, V_p, s_k, h_p, X in R2) are defined in their lesson (notation/notation.json: only program-wide "
    "symbols are registered). X is the exception, see L03-R2.")
row("notation-Gamma-L03", "notation: Gamma_A and Gamma_B defined before use", L03 + " Proposition 1.2 (line 64)",
    "Gamma_A and Gamma_B are introduced in the statement of Proposition 1.2 as the total future costs, before the proof and "
    "the Problem P1 solution use them. PASS.")

# ---- L03 page rows ----
row("L03-num-ex21", "2.2 numbers", L03 + " Example 2.1 and line 98 (lines 83, 98)",
    "Recomputed: 20,000 x (4.00+3.00+1.50) + 12,000 = 182,000; 20,000 x 10.50 - 3,000 = 207,000; difference 25,000. "
    "Per unit 9.10 = 8.50 + 0.60 (12,000/20,000); net buy 10.35 = 10.50 - 0.15. 20,000 x 1.25 = 25,000. "
    "Substitution 20,000(8.50-10.50)+12,000+3,000 = -25,000. Matches Lab 1 lines 296-298 (" + O + "twin_L03.out).")
row("L03-prop22", "2.4 math (T): Proposition 2.2 with the one-year assumption", L03 + " lines 86-96",
    "Proof re-derived: (Q(m+l+v)+F) - (Qp - S) = Q(m+l+v-p)+F+S; the book value B and the 2.00 allocation are common and "
    "do not enter. The added assumption (one year, undiscounted) is the scope the Section 5 bullet 'The model is one year "
    "and has no discounting' states (line 370). PASS.")
row("L03-prop12", "2.4 math (T): Proposition 1.2 and Remark 1.3", L03 + " lines 63-75",
    "Re-derived: Gamma_A - Gamma_B = (K+R_A)-(K+R_B) = R_A - R_B; sign argument valid for every K. Remark 1.3 (full-cost "
    "statement reports K) is consistent with Proposition 1.2. PASS.")
row("L03-prop41", "2.4 math (T): Proposition 4.1 and proof", L03 + " lines 347-355",
    "Proof: first H hours are free, excess max(0,h-H) displaces D at c per hour, net C - c*max(0,h-H). Numbers: h=6,000, "
    "H=4,000, C=15,000, c=5.00: excess 2,000, lost 10,000, net 5,000 (" + O + "twin_L03.out). PASS.")
row("L03-lab1-output", "2.5-labs: lab output and interpretation", L03 + " Lab 1 (lines 100-329) and " + T03,
    "The lab prints (twin_L03.out, 36 lines) match the expected block exactly. The 9.10 avoidable, 11.10 full, 10.50 buy, "
    "-25,000.00, 9.25 break-even, -2,000.00 keep-or-drop, 5,000.00 special order and the 2.50 vs 5.00 naive comparison all "
    "recomputed by hand above. The sunk and overhead changes print an unchanged difference (-25,000.00). The lab has no "
    "assert statement; its docstring now says 'prints whether', which matches what it prints. PASS.")
row("L03-lab1-interp", "2.5-labs: Lab 1 interpretation paragraph (line 328)", L03 + " line 328",
    "Every figure in the paragraph is printed or recomputed: 11.10 with the overhead, 9.10 without it (the avoidable line), "
    "9.10 below 10.50, scrap 0.15, break-even 9.25 printed, the difference unchanged under book value and overhead changes "
    "(printed). Causal direction checked: removing the 2.00 gives 9.10 < 10.50, so the overhead is the cause of the reversal. "
    "PASS on content.")
row("L03-interp-first-line", "2.5-labs: locator 'first line of Lab 1' (line 328)", L03 + " line 328",
    "The sentence says the 9.10 avoidable make cost per unit is 'printed on the first line of Lab 1'. In " + O + "twin_L03.out "
    "the first line is the title 'Part K, make or buy: 20,000 units a year (SIMULATED)'; the 9.10 figure is on the second "
    "line ('avoidable make cost per unit ... 9.10'). The locator is one line off.",
    status="FAIL",
    fix="Replace 'printed on the first line of Lab 1' with 'printed on the second line of Lab 1's output' (or 'the first figure line of Lab 1').")
row("L03-sec2-model", "2.4/2.9: Section 2 inputs and claims", L03 + " lines 77-79",
    "Inputs match Lab 1 (units 20,000, material 4.00, labour 3.00, variable overhead 1.50, dedicated fixed 12,000, allocated "
    "2.00, buy 10.50, scrap 3,000, book value 20,000). PASS.")
row("L03-sec3-ex31", "2.2 numbers and 2.4: Example 3.1 and Remark 3.2", L03 + " lines 335-341",
    "Contribution 6,000; operating income -1,000; firm profit -1,000 kept, -3,000 dropped; difference -2,000; avoidable "
    "fixed 4,000 leaves 2,000 towards the common cost. Lab 1 lines 314-319 print the same. Remark 3.2 rule is right. PASS.")
row("L03-sec4", "2.2 numbers: Section 4 and Remark 4.2", L03 + " lines 345-362",
    "3,000 units x 5.00 = 15,000; 6,000 - 4,000 spare = 2,000 excess x 5.00 = 10,000; net 5,000. Per-hour shortcut 5.00/2 = "
    "2.50 against 5.00 per hour. Matches Lab 1 lines 321-327. PASS.")
row("L03-s5-canon", "2.4: Section 5 assumptions", L03 + " lines 366-374",
    "Four bullets; each named assumption is one the lab does not model, and the bullets' statements (one year, no "
    "discounting, supervisor contract, equipment alternative use) match the Proposition 2.2 and 4.1 assumptions. PASS.")
row("L03-misc", "2.2 numbers and wording: misconceptions 1-4", L03 + " lines 379-395",
    "1: 13.10 = 11.10 + 2.00 (lab 306); 2: 50,000 book value leaves -25,000 (lab 302-303); 3: 6,000 - 4,000 = 2,000 "
    "covers part of 3,000; firm profit -3,000 (lab 316-317); 4: 2.50 vs 5.00, net gain 5,000 (lab 321-327). PASS.")
row("L03-ex-problems-mech", "2.2 numbers: M1-M3", L03 + " lines 404-424",
    "M1: 7,000 - 6,500 = 500 and Delta = 1,000(5-6.5)+2,000 = 500. M2: book value not entering, scrap 15,000 relevant. "
    "M3: -15,000 keep, -10,000 drop, 5,000 gain from dropping. All recomputed. PASS.")
row("L03-ex-problems-proof", "2.4 math: P1-P3", L03 + " lines 429-449",
    "P1 follows from subtracting K. P2: beta terms cancel. P3: c* = 15,000/2,000 = 7.50 and 5.00 < 7.50 accepts. PASS.")
row("L03-ex-problems-emp", "2.2 numbers: E1-E3", L03 + " lines 454-474",
    "E1: p = 8.50 + 15,000/20,000 = 9.25, recomputed to 0. E2: excess 0, net 15,000. E3: keep -3,000 vs drop -5,000, "
    "change -2,000 unchanged decision. PASS.")
row("L03-ex-problems-research", "2.4: R1-R3 solutions", L03 + " lines 480-499",
    "R1 states no horizon or rate is computed (honest). R2: making 182,000+40,000 = 222,000; buying 210,000-40,000 = "
    "170,000; difference 52,000; crossover X = 14,000 with both at 196,000 (182,000+14,000 = 210,000-14,000). R3 is "
    "conceptual. The R2 arithmetic is correct; its definition of X is the defect in row L03-R2.")
row("L03-R2", "2.4 notation: X defined before use (R2 solution, line 490)", L03 + " line 490",
    "The solution writes 'Making costs 182,000 + X and buying costs 210,000 - X' and 'when X < 14,000'. X is not defined "
    "anywhere in the statement or the solution (the statement gives a contribution of 40,000.00 a year and no symbol). "
    "A term used before it is defined.",
    status="FAIL",
    fix="Add to the solution: 'Let X be the contribution of the other use, so X = 40,000 here.' before the first use of X.")
row("L03-keyresults", "2.3 grades: key-results table (section 8)", L03 + " lines 509-516",
    "T rows are the three proved propositions (1.2, 2.2, 4.1), each in its section. C rows are Lab 1 figures (SIMULATED) "
    "and the stated convention. Row 510 states Proposition 2.2 without the one-year assumption that the proposition itself "
    "now carries (line 88); the row cites the proposition, so the scope is stated where the proof is. Not a misstatement. PASS.")
row("L03-quiz", "2.9-structure: quiz answers and explanations", L03 + " lines 522-583",
    "Options marked correct: scrap cash (correct), 50,000 sunk unchanged (correct), line B kept because profit falls (correct), "
    "all of the hours is wrong, only excess hours (correct). Numeric answers -25,000 (lines 536-538), 11.10 (541-543), 5,000 "
    "(564-566) and 9.25 (578-580) match the recomputed values. PASS.")
row("L03-refs", "2.1 citations: datar2020horngrens", L03 + " line 587",
    "The citation is held 'for terminology only' with 'passage locator not confirmed'. The registry record (references/"
    "references.json key datar2020horngrens, title 'Horngren's Cost Accounting', Datar and Rajan, Pearson, ISBN 9780136708230, "
    "verified by openlibrary) matches the textbook named. The page's claim is terminology only; no passage is read or "
    "claimed. The record's year (2020) differs from the curriculum (2021), but the page states no year. PASS.")
row("AC4b-cite-datar2020horngrens", "2.1 citations: datar2020horngrens (live)", "references/references.json; live verify_refs --unit AC4",
    "Live: 'live re-verification of AC4: 2 of 560 entries, 0 problems'. The page makes no content claim from the book. PASS.")
row("AC4b-cite-kaplan1998cost", "2.1 citations: kaplan1998cost", "references/references.json; " + L04 + " line 548",
    "Registry title 'Cost & effect: using integrated cost systems to drive profitability and performance' (Kaplan, HBS "
    "Press, 1998) matches the page's 'a book on integrated cost systems'. The page says 'orientation only' and that no "
    "passage is confirmed. Live verify passed. PASS.")

# ---- L04 page rows ----
row("L04-s1-defs", "2.9: Section 1 definitions and Proposition 1.2 proof", L04 + " lines 55-75",
    "Definition 1.1 two-stage; Proposition 1.2 sum over products of C_k N_kp/N_k = sum C_k (re-derived). Remark 1.3: the "
    "division raises ValueError in the lab (checked below: exact_rate(10,000,001 by 10,000) raises). PASS.")
row("L04-remark13-lab", "2.5 labs: Remark 1.3 says Lab 1 raises on uneven division", L04 + " lines 73-75; " + T04,
    "Imported the twin's functions (scratch module, main() removed) under python -I -W error: exact_rate(10_000_001, 10_000) "
    "raised ValueError 'pool: 10000001 does not divide evenly by 10000 driver units'; exact division returns 1000. Output "
    + S + "claims_L04.py. PASS.")
row("L04-ex21-22", "2.2 numbers: Examples 2.1 and 2.2", L04 + " lines 79-93",
    "Volume: 100,000/10,000 hours = 10.00; X 80,000 (8.00 per unit), Y 20,000 (10.00), Y margin 5.00. Activity: rates 500, 50, "
    "5.00; X 45,000 (4.50), Y 55,000 (27.50); total 100,000; Y full cost 42.50 vs price 30 (loses 12.50). Matches lab "
    "lines 284-298. PASS.")
row("L04-s2-counts", "2.2 numbers: setup and inspection counts in the prose", L04 + " line 86",
    "Y 60 setups and 300 inspections for 2,000 units; X 20 and 100 for 10,000 units. Matches Example 2.2 and the lab "
    "driver counts (lab lines 92-93). PASS.")
row("L04-prop31-reallocation", "2.4 math and numbers: Proposition 3.1 paragraph", L04 + " lines 107",
    "A_X-V_X = 45,000-80,000 = -35,000; A_Y-V_Y = 55,000-20,000 = +35,000. Lab 1 lines 301 and 304. PASS.")
row("L04-prop32", "2.4 math: Proposition 3.2 and proof", L04 + " lines 110-119",
    "Proof re-derived: N_kp = s_k h_p gives A_p = (h_p/H) sum C_k = V_p. Lab counts not proportional: 20/8,000 = 0.0025 and "
    "60/2,000 = 0.03 (recomputed). Statement says 'if', with no converse claimed (card AC4-c053 agrees). PASS.")
row("L04-lab1-output", "2.5 labs: output and hypothesis", L04 + " lines 121-317 and " + T04,
    "twin_L04.out (exit 0, empty stderr) equals the expected block exactly, 38 lines (lines 278-315). Hypothesis numbers 4.50, 27.50, 8.00, "
    "10.00, -35,000/+35,000, positive/negative margins, and 22.50 after cutting Y's setups to 20 match the printed output. "
    "The lab has no assert statements; 'equals pool: True' lines are printed, which is what the interpretation says. PASS.")
row("L04-lab1-interp", "2.5 labs: interpretation (line 316)", L04 + " line 316",
    "'confirms the arithmetic of Examples 2.1 and 2.2 and the two identities' (printed equals-pool True twice and the totals "
    "agree line); 'the lab does not measure whether 60 or 20 setups is the true figure' (no measurement in the code). PASS.")
row("L04-s4-ex41", "2.2 numbers and 2.4: Example 4.1 and Remark 4.2", L04 + " lines 321-331",
    "Keep: 30,000 - 45,000 - 10,000 = -25,000 (equals the printed activity-based annual margin of Y); drop: -10,000; change "
    "+15,000. The 25,000 counterfactual (all 55,000 stops) is -25,000 vs 0 (E3). PASS.")
row("L04-s5-canon", "2.4/2.9: Section 5 canon-breaks", L04 + " lines 335-343",
    "Bullet 1: 55,000 to 45,000 and 27.50 to 22.50 match Lab 1 sensitivity (lines 312-314). Bullet 2 example: 10 + 30 = 40 "
    "over two driver units = 20 each; separately 10 and 30. Bullet 4 points to Problems R1 and the machine pool of Example "
    "4.1; R1 exists and says cost to serve includes stay-behind cost. PASS.")
row("L04-misc-ratios", "2.2 numbers: misconception 1 ratios (line 350)", L04 + " line 350",
    "Y 0.03 setups per labour hour = 60/2,000; X 0.0025 = 20/8,000 (12 times, 0.03/0.0025 = 12). Inspections 0.15 vs 0.0125 "
    "(12 times). Machine hours 1.00 vs 0.75 per labour hour: ratio 1.00/0.75 = 4/3 (corrected from 1.33; the stated 4/3 is "
    "exact). Charges 15.00, 7.50, 5.00 sum to 27.50. PASS.")
row("L04-misc2-3", "2.2 numbers: misconceptions 2 and 3 (lines 354-358)", L04 + " lines 354-358",
    "35,000 moved; unit overhead 10.00 to 27.50 is a change of 17.50. Dropping Y: 45,000 saved, 30,000 contribution lost, "
    "net 15,000. PASS.")
row("L04-problems-mech", "2.2 numbers: M1-M3", L04 + " lines 370-388",
    "M1: 60,000/150 = 400; 20,000 and 40,000. M2: 30,000/4,000 = 7.50; 22.50 and 15.00 per unit. M3: 14,000/700 = 20; full "
    "unit 28.00. PASS.")
row("L04-problems-proof", "2.4 math: P1-P3", L04 + " lines 395-414",
    "P1 uses Example 2.1 volume allocation and the sum. P2 zero-sum from Proposition 3.1. P3: 0.002 setups per hour gives 16 and "
    "4 setups; shares 16/20 and 4/20 equal 8,000/10,000 and 2,000/10,000. PASS.")
row("L04-problems-emp", "2.2 numbers: E1-E3", L04 + " lines 421-438",
    "E1: machine rate 60,000/8,000 = 7.50; X 55,000 (5.50), Y 45,000 (22.50); total 100,000. E2: 20,000/250 = 80; X 8,000, "
    "Y 12,000; X 48,000 (4.80), Y 52,000 (26.00). E3: all-stops change +25,000; machine-stays change +15,000. PASS.")
row("L04-problems-research", "2.2 numbers: R2 and R1, R3", L04 + " lines 446-464",
    "R2 numbers recomputed: rates 40,000/70 = 571.43 and 40,000/90 = 444.44; Y setup overhead 28,571.43 and 31,111.11; "
    "changes -1,428.57 and +1,111.11; per unit -0.714 and +0.556 (displayed -0.71 and +0.56, rounded from the unrounded "
    "figures, which the page states). R1 and R3 are conceptual and consistent with the lab. PASS.")
row("L04-keyresults", "2.3 grades: key-results table (section 8)", L04 + " lines 474-481",
    "T rows are Propositions 1.2, 3.1, 3.2 (proved). C rows are Lab 1 figures and Example 4.1, the latter conditional on the "
    "stated avoidability. The convention row is labelled a convention. PASS.")
row("L04-quiz", "2.9-structure: quiz answers", L04 + " lines 491-543",
    "q1 correct option matches Proposition 1.2 proof; q2 4.5; q3 10 (Y volume per unit); q4 35,000; q5 correct option gives "
    "0.0025 and 0.03; q6 42.50; q7 15,000; q8 correct option: part of a pool stays. All verified. PASS.")
row("L04-refs", "2.1 citations: kaplan1998cost", L04 + " line 548", "See AC4b-cite-kaplan1998cost. PASS.")

# ---- the mutation rows (project-slice requirement does not apply; lab-claim checks instead) ----
row("L03-L04-lab-mutants", "2.5 labs: student-error mutants of the two twins (archived)",
    M + "m_L03_*.py (3), m_L04_*.py (4)",
    "Seven lab mutants, each run under python -I -W error and compared with the page's expected block: all 7 change stdout "
    "(exit 0 for six, exit 1 for m_L04_volume_rate_uses_units). The brief's project-slice mutant requirement does not apply to "
    "a lesson-and-twin slice; these are supporting evidence only (architect ruling on lab mutants). Scripts: "
    + S + "run_mut.py.", status="PASS")

fragment = {
    "unit": "AC4",
    "slice": "AC4-b",
    "round": 30,
    "verifier": "round-30 independent verifier (Haiku) for slice AC4-b: L03, L04 and their lab twins; did not build AC4 and shares no context with the builders or earlier verifiers",
    "pin": "5aeaaf0",
    "base": "503d139 (delta base; the previous round-29 fragment on disk records 503d139 and one row)",
    "checkout": "/tmp/verify30-AC4-b (detached worktree at 5aeaaf0; .venv symlink; vendor copied)",
    "scratch": "/tmp/AC4-v/AC4-b/r30/",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "rows": rows,
    "mutants": [
        {"id": "m_L03_book_value_in_relevant_cost", "description": "student adds the sunk book value to the relevant difference", "killed_by": "stdout differs from expected block"},
        {"id": "m_L03_fullcost_decision_uses_relevant", "description": "full-cost decision uses the avoidable cost without allocated overhead", "killed_by": "stdout differs from expected block"},
        {"id": "m_L03_special_order_naive_hours", "description": "lost contribution charged on all order hours, not the excess", "killed_by": "stdout differs from expected block"},
        {"id": "m_L04_setups_driven_by_inspections", "description": "setups assigned by the inspection driver counts", "killed_by": "stdout differs from expected block"},
        {"id": "m_L04_stage_two_divides_by_hours", "description": "stage two divides by labour hours instead of units (per-unit print)", "killed_by": "stdout differs from expected block"},
        {"id": "m_L04_stage_one_half_allocation", "description": "each pool allocation halved (rounded down)", "killed_by": "stdout differs from expected block"},
        {"id": "m_L04_volume_rate_uses_units", "description": "volume rate spreads the pool by units instead of labour hours", "killed_by": "ValueError (uneven rate), exit 1"},
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-29 fragment on disk (/tmp/fanout-frags/AC4-b.round29.json) contains only one row (notation-T-L03) despite its summary of 64 rows, so previous row ids could not be carried by value; the ids kept are those named in the round-23 builder (AC4b-*, AC4b23-*) plus notation-T-L03.",
        "Carry rule: no PASS row was carried. Page rows were re-verified because L03.html and L04.html changed since 503d139. Card rows were re-verified because the card objects are byte-identical, and the lesson text they cite changed.",
        "Mutants: this is a lesson-and-twin slice (not a project slice); the seven archived lab mutants are supporting evidence only. No grader files are in scope, so no alternative implementations were written.",
        "run_labs was run with --page L03 and --page L04; the other AC4 labs belong to other slices and were not run.",
        "pytest was filtered to the two AC4 lab tests; exit status was not captured.",
        "The published-data check (Horngren 2020 vs curriculum 2021 year) is noted only; the page states no year.",
    ],
    "summary": {},
}
fragment["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": sum(1 for r in rows if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    "fail_ids": [r["id"] for r in rows if r["status"] != "PASS"],
}
fragment["verdict"] = "PASS" if fragment["summary"]["fail"] == 0 and fragment["summary"]["unverifiable"] == 0 else "FAIL"
json.dump(fragment, open("ledgers/AC4/AC4-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(fragment["summary"], fragment["verdict"])
