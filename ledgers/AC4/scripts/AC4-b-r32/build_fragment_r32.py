import json, pathlib, datetime
ROOT = pathlib.Path("/tmp/verify32-AC4-b")
PASS, FAIL = "PASS", "FAIL"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        r["fix"] = fix
    rows.append(r)
O = "ledgers/AC4/scripts/AC4-b-r32/out/"
# command rows
row("AC4b-cmd-pin", "2.9-structure", "git HEAD of /tmp/verify32-AC4-b", PASS,
    "out/git_head.out: HEAD 845ae46ef51bf2a8693fc15c284ba0bcdd0c54c7, detached; only untracked paths are .venv and this round's ledger folders. Delta base is 5aeaaf0, the pin recorded in the round-31 fragment (/tmp/fanout-frags/AC4-b.round31.json, field pin).")
row("AC4b-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit AC4 --page L03; --page L04", PASS,
    O + "check_pages_L03.out: 'check_pages AC4 L03: PASS', rc=0; " + O + "check_pages_L04.out: 'check_pages AC4 L04: PASS', rc=0.")
row("AC4b-cmd-check_dag", "DAG/concepts", "tools/check_dag.py --all", PASS,
    O + "check_dag.out: 'check_dag AC4: PASS' among all units, rc=0.")
row("AC4b-cmd-run_labs", "2.5-labs", "tools/run_labs.py --unit AC4 --page L03; --page L04", PASS,
    O + "run_labs_L03.out: 'run_labs AC4: PASS (1/1)', rc=0; " + O + "run_labs_L04.out: 'run_labs AC4: PASS (1/1)', rc=0.")
row("AC4b-cmd-twins-isolated", "2.5-labs", "tests/labs/AC4/lab-AC4-L03-1.py; tests/labs/AC4/lab-AC4-L04-1.py under python -I -W error", PASS,
    O + "twin_L03.rc and twin_L04.rc are 0; twin_L03.err and twin_L04.err are 0 bytes. " + O + "exact_match.out (script ledgers/AC4/scripts/AC4-b-r32/exact_match.py): the page's expected block and the twin stdout are IDENTICAL (36 and 38 lines), and the page's embedded code equals the twin file.")
row("AC4b-cmd-page_smoke", "2.5-labs", "tools/page_smoke.py --unit AC4 --pages L03 L04 --skip-sweep", PASS,
    O + "page_smoke.out: 'page_smoke modules/AC/AC4/L03.html: PASS', 'page_smoke modules/AC/AC4/L04.html: PASS', 'page_smoke AC4: PASS', rc=0. --skip-sweep is applicable: grep finds no svg, select or range control in L03.html or L04.html; the only inputs are quiz answers.")
row("AC4b-cmd-ruff-mypy", "gates", "ruff check and ruff format --check on the two twins; mypy --no-incremental on the two twins", PASS,
    O + "ruff_check.out: 'All checks passed!' and '2 files already formatted', rc=0; " + O + "mypy.out: 'Success: no issues found in 2 source files', rc=0.")
row("AC4b-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit AC4", PASS,
    O + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', rc=0; " + O + "verify_refs_live_unit.out: 'live re-verification of AC4: 2 of 560 entries, 0 problems', rc=0.")
row("AC4b-cmd-pytest", "gates", "pytest tests/test_labs.py -k 'AC4 and (L03 or L04)' -q", PASS,
    O + "pytest.out: two passing tests ('..', [100%]), rc=0.")
# cards
row("AC4b-cards-L03-L04", "2.7-cards", "course/modules/AC/AC4/cards.json: the 35 cards whose lesson is L03 or L04 (AC4-c031..c044, c045..c058, c121, c122, c123, c124, c126, c131, c136)", PASS,
    "Every card read against its lesson this round (cards dump, scripts ledgers/AC4/scripts/AC4-b-r32/cards_L03_L04.py). Checked against L03.html and L04.html: c031-c036 (Definition 1.1, Example 2.1 figures, Lab 1 lines 302-310, 317-327, Example 3.1); c037 and c136 (Proposition 1.2, Remark 1.3); c038-c039 (Proposition 2.2 and 4.1 formulas, sign convention, 'Making is cheaper when Delta is negative' matches 'Making is cheaper when Delta < 0' at line 90); c040-c044 (Lab 1 figures 25,000, 9.25, -2,000, 5,000); c045-c058 (Definition 1.1, Propositions 1.2, 3.1, 3.2, Example 2.2, Example 4.1, the 17.50 change, the 15,000 change, Problem E1 and E2); c121-c131 (Proposition 2.2 with the book value, Lab 1 product line B, per-hour shortcut 2.50 vs 5.00, full-cost 11.10 vs 10.50, Remark 3.2). No card contradicts its lesson. Scripted check: every digit string on every card appears in the stripped lesson text, zero missing (out/cards_L03_L04.out). Note: round 31 stated 32 cards; the count is 35.")
row("AC4b23-cards-c037", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c037; course/modules/AC/AC4/L03.html Proposition 1.2 (lines 63-69)", PASS,
    "Back: 'The two totals differ by the difference of their relevant costs, so the common cost cancels' matches Gamma_A - Gamma_B = R_A - R_B (line 69). PASS.")
row("AC4b23-cards-c136", "2.7-cards", "course/modules/AC/AC4/cards.json AC4-c136; course/modules/AC/AC4/L03.html Remark 1.3 (line 74)", PASS,
    "Back cites Proposition 1.2 and Remark 1.3; line 74 says Proposition 1.2 'does not give the profit of either one'. PASS.")
row("AC4b23-card-identity", "2.7-cards", "course/modules/AC/AC4/cards.json (L03 and L04 card objects)", PASS,
    "git diff 5aeaaf0 845ae46 -- course/modules/AC/AC4/cards.json changes only AC4-c023 (L02) and AC4-c078 (L06); no L03 or L04 card object changed.")
row("AC4b23-card-numbers", "2.7-cards", "every number on every L03 and L04 card", PASS,
    O + "cards_L03_L04.out: 35 cards, missing [] for each (script cards_L03_L04.py).")
row("AC4b23-prose-changed-cards", "2.9-structure", "cards AC4-c037, AC4-c136 (carried prose)", PASS,
    "Both card objects unchanged in the delta; both cited passages (lines 63-69, 74) re-read this round and agree.")
# hours
row("AC4b-hours-L03-L04", "hours", "course/modules/AC/AC4/L03.html and L04.html data-hours attribute (line 2) and eyebrow (line 34); plans/AC4-build-plan.md hours table (line 81-82)", PASS,
    "L03 data-hours=6 and eyebrow '6 study hours'; L04 data-hours=6 and eyebrow '6 study hours'. Plan table rows L03 and L04 each 6. Arithmetic: no inconsistency. Own pace estimate not used as a fail criterion (architect ruling).")
row("AC4b23-hub-hours", "hours", "course/modules/AC/AC4/L01..L08.html data-hours; course/modules/AC/AC4/index.html line 29", PASS,
    "Lesson data-hours 6,7,6,6,7,6,6,6 sum to 50, matching index.html data-hours-lessons=50 and data-hours-project=20 (50/20 split). Plan line 95 gives the same sum.")
row("AC4b23-slice-delta", "2.9-structure", "git diff 5aeaaf0 845ae46 for the slice files", PASS,
    "ledgers/AC4/scripts/AC4-b-r32/out/delta_stat.out: course/modules/AC/AC4/L03.html changed (2 lines: 328 and 490); cards.json and project.html changed but not in this slice. course/modules/AC/AC4/L04.html and tests/labs/AC4/lab-AC4-L03-1.py and lab-AC4-L04-1.py are unchanged. Every L03 hunk was read (out/delta_L03.out).")
# notation
row("notation-T-L03", "notation", "course/modules/AC/AC4/L03.html and L04.html math", PASS,
    "grep for a bare T symbol in the math of both pages returns no match. The registered T (notation/notation.json: number of return observations) is not used here.")
row("notation-Gamma-L03", "notation", "course/modules/AC/AC4/L03.html Proposition 1.2 (line 64), proof (line 69), problem P1 (line 433)", PASS,
    "Gamma_A and Gamma_B are introduced in the Proposition 1.2 statement before the proof and P1 use them.")
row("L03-R2-X-defined", "notation", "course/modules/AC/AC4/L03.html R2 solution (line 490)", PASS,
    "X is not in notation/notation.json (8 registered symbols listed). Line 490 now reads 'Let X be the contribution of the other use, so X = 40,000 here' before the first use of X in the same solution. The only other X in the page is the grade legend 'X refuted' (line 48), which is not math.")
row("notation-B-local", "notation", "course/modules/AC/AC4/L03.html line 64 (alternatives A and B), line 95 (book value B), line 438 (P2 book value B)", PASS,
    "Non-blocking observation. B names an alternative in Proposition 1.2 and the book value in the Proposition 2.2 proof and P2. B is not registered, so no registry rule is broken, and each meaning is defined where it is used. Recommended later edit: rename the book value to a different letter. Product line 'B' in Lab 1 and Example 3.1 is a name, not math.")
# L03 pages
row("L03-why-and-s1-defs", "2.9-structure", "course/modules/AC/AC4/L03.html lines 51, 55-60, 62-75", PASS,
    "Definition 1.1 and the three-word gloss (future, cash, differs) agree with the lab's rule docstring (lab lines 109-112). Proposition 1.2 and Remark 1.3 re-derived (L03-prop12).")
row("L03-num-ex21", "2.2 numbers", "course/modules/AC/AC4/L03.html Example 2.1 (line 83) and line 98", PASS,
    "Recomputed: 20,000 x (4.00+3.00+1.50) + 12,000 = 182,000; 20,000 x 10.50 - 3,000 = 207,000; difference 25,000. Line 98: 20,000 x (8.50-10.50) + 12,000 + 3,000 = -25,000; per unit 9.10 = 8.50 + 0.60 (12,000/20,000); 10.35 = 10.50 - 0.15 (3,000/20,000); 10.35 - 9.10 = 1.25, times 20,000 = 25,000. Matches twin_L03.out lines 2-7 (out/twin_L03.out).")
row("L03-prop22", "2.4 math (T)", "course/modules/AC/AC4/L03.html Proposition 2.2 (lines 86-91) and proof (lines 93-96)", PASS,
    "Re-derived: (Q(m+l+v)+F) - (Qp-S) = Q(m+l+v-p)+F+S. The book value B and the 2.00 allocation are the same under both alternatives and do not enter. Sign: Delta < 0 means making is cheaper, and the lab's -25,000 (twin_L03.out line 7) agrees.")
row("L03-prop12", "2.4 math (T)", "course/modules/AC/AC4/L03.html Proposition 1.2 and Remark 1.3 (lines 63-75)", PASS,
    "Gamma_A - Gamma_B = (K+R_A)-(K+R_B) = R_A - R_B; the sign argument holds for every K. Remark 1.3 (the full-cost statement reports K) is consistent with the proposition.")
row("L03-prop41", "2.4 math (T)", "course/modules/AC/AC4/L03.html Proposition 4.1 and proof (lines 347-355)", PASS,
    "Proof: the first H hours are free, excess max(0,h-H) displaces D at c per hour, net C - c*max(0,h-H). Numbers: h=6,000, H=4,000, C=15,000, c=5.00: excess 2,000, lost 10,000, net 5,000 (line 357).")
row("L03-lab1-output", "2.5 labs", "course/modules/AC/AC4/L03.html Lab 1 (lines 100-329); tests/labs/AC4/lab-AC4-L03-1.py", PASS,
    "exact_match.out: the 36-line expected block equals the twin's stdout under python -I -W error. Each figure in the hypothesis (line 102) is printed: 11.10 full cost, 10.50 buy, -25,000 difference, make decision, buy under full cost, unchanged difference at 20,000 and 50,000 book value, overhead 13.10 and -25,000, 9.50 price keeps make, product B kept, accept with 5,000 net and reject under the per-hour shortcut.")
row("L03-lab1-interp", "2.5 labs", "course/modules/AC/AC4/L03.html line 328 (Lab 1 interpretation)", PASS,
    "Every figure is printed or recomputed: 11.10 (twin_L03.out line 3), 9.10 (line 2), 10.50 (line 4), 9.10 below 10.50, 0.15 scrap (line 98 and Example 2.1), break-even 9.25 (twin_L03.out line 21, and E1). Unchanged difference at book values 20,000 and 50,000 (lines 11-13) and with the allocated overhead (lines 15-17). The limits named (one year, no supplier reliability or quality) are not modelled by the code; the code has no horizon term.")
row("L03-interp-first-line", "2.5 labs", "course/modules/AC/AC4/L03.html line 328: 'printed on the second line of Lab 1's output, after its title'", PASS,
    "Fixed since round 31. out/twin_L03.out line 1 is the title 'Part K, make or buy: 20,000 units a year (SIMULATED)'; line 2 is 'avoidable make cost per unit (variable + dedicated fixed / units): 9.10'. The second-line wording is exact.")
row("L03-sec2-model", "2.4/2.9 structure", "course/modules/AC/AC4/L03.html lines 77-79", PASS,
    "Inputs match the base case in the page's embedded code (L03.html lines 208-218): units 20,000; material 4.00; labour 3.00; variable overhead 1.50; dedicated fixed 12,000; allocated 2.00; buy 10.50; scrap 3,000; book value 20,000.")
row("L03-sec3-ex31", "2.2 numbers", "course/modules/AC/AC4/L03.html Example 3.1 (lines 335-341) and Remark 3.2 (lines 339-340)", PASS,
    "Contribution 6,000; operating income -1,000; firm profit -1,000 kept, -3,000 dropped; change -2,000; avoidable fixed 4,000 leaves 2,000 towards the common cost. Lab lines 313-319 print the same figures.")
row("L03-sec4", "2.2 numbers", "course/modules/AC/AC4/L03.html Section 4 (lines 345-362) and Remark 4.2", PASS,
    "3,000 units x 5.00 = 15,000; spare 4,000 hours; excess 2,000 x 5.00 = 10,000; net 5,000. Per-hour shortcut 5.00/2 = 2.50 against 5.00 per hour (line 361). Lab lines 320-327 print 6000, 4000, 2000, 15,000, 10,000, 5,000, accept, 2.50, reject.")
row("L03-s5-canon", "2.4 / wording", "course/modules/AC/AC4/L03.html Section 5 (lines 366-374)", PASS,
    "Four bullets; the lab does not model overhead changes, supervisor horizon, equipment alternative use, or supplier quality (code has no such terms). Non-blocking note: the first bullet says Proposition 2.2 'assumes' the overhead is unchanged; the statement has no overhead term, and the proof (line 95) carries the condition. The wording is accepted as a reading of the proof.")
row("L03-misc", "2.2 numbers and wording", "course/modules/AC/AC4/L03.html misconceptions 1-4 (lines 379-395)", PASS,
    "1: raising the allocation to 4.00 gives full cost 13.10 and relevant difference -25,000 (L03.html expected block lines 306-307). 2: book value 50,000 gives -25,000 (expected block lines 302-303). 3: 6,000 - 4,000 = 2,000 towards the 3,000 common cost; firm profit -3,000 on dropping (expected block lines 316-317). 4: naive 2.50 vs 5.00 reject, correct accept with 5,000 (expected block lines 324-327).")
row("L03-ex-problems-mech", "2.2 numbers", "course/modules/AC/AC4/L03.html M1-M3 (lines 404-424)", PASS,
    "M1: 7,000 - 6,500 = 500; Delta = 1,000(5-6.5)+2,000 = 500. M2: book value not entering, scrap 15,000 relevant. M3: 20,000 - 25,000 - 10,000 = -15,000 keep; -10,000 drop; change 5,000 favours drop.")
row("L03-ex-problems-proof", "2.4 math", "course/modules/AC/AC4/L03.html P1-P3 (lines 429-449)", PASS,
    "P1 follows from subtracting K. P2: beta terms cancel. P3: c* = 15,000 / 2,000 = 7.50; the displaced product must earn more than 7.50 to reject; 5.00 accepts.")
row("L03-ex-problems-emp", "2.2 numbers", "course/modules/AC/AC4/L03.html E1-E3 (lines 454-474)", PASS,
    "E1: p = 8.50 + 15,000/20,000 = 9.25; recomputed to 0. E2: excess 0, net 15,000, still accept. E3: keep -3,000 vs drop -5,000; decision keep unchanged.")
row("L03-ex-problems-research", "2.4 / wording", "course/modules/AC/AC4/L03.html R1 and R3 (lines 480-499)", PASS,
    "R1 says no horizon or rate is computed, consistent with the lab. R3 is qualitative (no number). R2 is checked in row L03-R2.")
row("L03-R2", "2.4 notation", "course/modules/AC/AC4/L03.html R2 solution (line 490)", PASS,
    "Fixed since round 31. X is now defined before use. Recomputed: making 182,000 + 40,000 = 222,000; buying 210,000 - 40,000 = 170,000; difference 52,000. 182,000 + X < 210,000 - X iff X < 14,000 (2X < 28,000); at X = 14,000 both are 196,000.")
row("L03-keyresults", "2.3 grades", "course/modules/AC/AC4/L03.html key-results table (lines 509-516)", PASS,
    "T rows are Propositions 1.2, 2.2 and 4.1, each proved in its section. C rows cite Lab 1 (SIMULATED) or the stated convention (Section 5). Grades match BLUEPRINT 3 for these claim types.")
row("L03-quiz", "2.9 structure", "course/modules/AC/AC4/L03.html quiz (lines 522-583)", PASS,
    "Correct options: scrap cash; 50,000 sunk unchanged; line B kept because profit falls; spare hours only beyond spare capacity. Numeric answers -25,000 (182,000 vs 207,000), 11.10, 5,000, 9.25 recomputed. Explanations cite Definition 1.1, Proposition 2.2, Remark 3.2, Proposition 4.1 and Problem E1 correctly.")
row("L03-refs", "2.1 citations", "course/modules/AC/AC4/L03.html line 587; references/references.json key datar2020horngrens (line 6505)", PASS,
    "The page holds the citation for terminology only, with 'passage locator not confirmed'. Registry: 'Horngren's Cost Accounting', Datar and Rajan, 2020, verified_by openlibrary. No content claim is made from the book. Curriculum yaml line 638 says '17th ed. (2021)'; the registry records 2020 and the page states no year, so no mismatch on the page.")
row("AC4b-cite-datar2020horngrens", "2.1 citations", "references/references.json line 6505; verify_refs live AC4", PASS,
    "Live: 2 of 560 entries, 0 problems. The registry record matches the page's use (terminology). The year difference between the registry (2020) and the curriculum (2021, yaml line 638) is noted only.")
row("AC4b-cite-kaplan1998cost", "2.1 citations", "references/references.json line 14107; course/modules/AC/AC4/L04.html line 548", PASS,
    "Registry title 'Cost & effect: using integrated cost systems to drive profitability and performance', Kaplan 1998, Harvard Business School Press. The page says 'a book on integrated cost systems' and makes no content claim.")
# L04
row("L04-s1-defs", "2.4 math (T)", "course/modules/AC/AC4/L04.html Definition 1.1 (line 59), Proposition 1.2 (line 64), proof (line 69)", PASS,
    "Sum over products of C_k N_kp/N_k = sum over k of C_k (sum over p of N_kp)/N_k = sum of C_k. Definition and proposition agree with the code's two-stage functions (lab lines 185-194).")
row("L04-remark13-lab", "2.5 labs", "course/modules/AC/AC4/L04.html Remark 1.3 (line 74) against tests/labs/AC4/lab-AC4-L04-1.py", FAIL,
    "Re-run this round: exact_rate(10_000_001, 10_000) raises ValueError (out/remark13_check.out), so the function does what the sentence says. But Lab 1's printed run never reaches that branch: main() calls exact_rate only with exact inputs (twin lines calling exact_rate at 58, 68, 115). Mutant m_L04_exact_check_removed (floor division in exact_rate) exits 0 with stdout identical to the expected block (out/mutants_r32.out). Per the lab ruling, a survivor counts against a lesson sentence that claims the lab enforces the property; line 74 says 'Lab 1 requires this division to be exact in cents and raises an error otherwise'. The printed run does not demonstrate or check that.",
    "Either (a) add a guarded call in the twin's main() that catches the ValueError for an uneven pool and prints its message, then re-embed the expected block with tools/embed_labs.py --refresh and re-run run_labs for AC4 L04; or (b) reword line 74 to: 'the rate function raises an error for an uneven division; the printed run does not reach that case'.")
row("L04-ex21-22", "2.2 numbers", "course/modules/AC/AC4/L04.html Examples 2.1 and 2.2 (lines 79-93)", PASS,
    "Volume rate 100,000 / 10,000 = 10.00; X 80,000 = 8.00, Y 20,000 = 10.00; Y 25.00 cost, 5.00 margin. Setups 40,000/80 = 500; inspections 20,000/400 = 50; machine 40,000/8,000 = 5.00. X 45,000 (4.50), Y 55,000 (27.50). Y 42.50, loss 12.50. Lab lines 297-298 print 4.50 and 27.50.")
row("L04-s2-counts", "2.2 numbers", "course/modules/AC/AC4/L04.html line 86", PASS,
    "Y 60 setups and 300 inspections for 2,000 units; X 20 and 100 for 10,000 units. Matches Example 2.2 and the lab driver counts.")
row("L04-prop31-reallocation", "2.4 math and numbers", "course/modules/AC/AC4/L04.html Proposition 3.1 (lines 97-107)", PASS,
    "A_X - V_X = 45,000 - 80,000 = -35,000; A_Y - V_Y = 55,000 - 20,000 = +35,000 (lab lines 301 and 304). Proof: sums of V_p and A_p both equal the pool.")
row("L04-prop32", "2.4 math (T)", "course/modules/AC/AC4/L04.html Proposition 3.2 and proof (lines 109-116)", PASS,
    "N_kp = s_k h_p gives N_k = s_k H and A_p = (h_p/H) sum C_k = V_p. Counts not proportional: 20/8,000 = 0.0025 and 60/2,000 = 0.03 (recomputed).")
row("L04-lab1-output", "2.5 labs", "course/modules/AC/AC4/L04.html Lab 1 (lines 121-317); tests/labs/AC4/lab-AC4-L04-1.py", PASS,
    "exact_match.out: the 38-line expected block equals the twin's stdout (python -I -W error, rc=0, stderr empty). Hypothesis numbers 4.50, 27.50, 8.00, 10.00, -35,000/+35,000, 22.50 and the Y margin signs are printed (lines 297-314).")
row("L04-lab1-interp", "2.5 labs", "course/modules/AC/AC4/L04.html line 316", PASS,
    "'confirms the arithmetic of Examples 2.1 and 2.2 and the two identities': the printed 'equals pool: True' lines and 'totals agree: True' are printed. The lab does not decide which method is correct (it prints each method's result), as the sentence says.")
row("L04-s4-ex41", "2.2 numbers and 2.4", "course/modules/AC/AC4/L04.html Example 4.1 and Remark 4.2 (lines 321-331)", PASS,
    "Keep: 30,000 - 45,000 - 10,000 = -25,000, equal to the printed activity-based margin of Y (line 308). Drop: -10,000. Change +15,000. The 25,000 counterfactual (if all 55,000 stopped) is 30,000 - 55,000 = -25,000 against 0 (recomputed, E3).")
row("L04-s5-canon", "2.4 / wording", "course/modules/AC/AC4/L04.html Section 5 (lines 335-343)", PASS,
    "Bullet 1: 55,000 to 45,000 and 27.50 to 22.50 match lab lines 312-314. Bullet 2: 10 + 30 = 40 over two driver units = 20 each; separately 10 and 30. Bullet 3 and 4 are statements of what the lab does not test; the code confirms no cost of measurement and no cost-to-serve test.")
row("L04-misc-ratios", "2.2 numbers", "course/modules/AC/AC4/L04.html line 350", PASS,
    "Ratios computed: Y 60/2,000 = 0.03 setups per hour; X 20/8,000 = 0.0025; ratio 12. Inspections 300/2,000 = 0.15 and 100/8,000 = 0.0125; ratio 12. Machine hours 2,000/2,000 = 1.00 and 6,000/8,000 = 0.75; ratio 4/3. Y's overhead 27.50 per unit = 15.00 + 7.50 + 5.00 (30,000, 15,000 and 10,000 over 2,000 units).")
row("L04-misc2-3", "2.2 numbers", "course/modules/AC/AC4/L04.html lines 354-358", PASS,
    "35,000 moved; unit overhead 10.00 to 27.50 is +17.50. Dropping Y: 45,000 stops, 30,000 contribution lost, net 15,000. Consistent with Example 4.1.")
row("L04-problems-mech", "2.2 numbers", "course/modules/AC/AC4/L04.html M1-M3 (lines 370-388)", PASS,
    "M1: 60,000/150 = 400; 20,000 and 40,000. M2: 30,000/4,000 = 7.50; 22.50 and 15.00 per unit. M3: 14,000/700 = 20; full unit 28.00.")
row("L04-problems-proof", "2.4 math", "course/modules/AC/AC4/L04.html P1-P3 (lines 395-414)", PASS,
    "P1 is the single-pool identity. P2 zero-sum from Proposition 3.1. P3: 0.002 setups per hour gives 16 and 4 setups; shares 16/20 = 8,000/10,000 and 4/20 = 2,000/10,000.")
row("L04-problems-emp", "2.2 numbers", "course/modules/AC/AC4/L04.html E1-E3 (lines 421-438)", PASS,
    "E1: 60,000/8,000 = 7.50; X 55,000 (5.50), Y 45,000 (22.50); total 100,000. E2: 20,000/250 = 80; X 8,000 and Y 12,000; X 48,000 (4.80), Y 52,000 (26.00). E3: +25,000 if all stop, +15,000 under the Example 4.1 assumption.")
row("L04-problems-research", "2.2 numbers", "course/modules/AC/AC4/L04.html R1-R3 (lines 444-464)", PASS,
    "R2 recomputed: rates 40,000/70 = 571.43 and 40,000/90 = 444.44; Y setup overhead 28,571.43 and 31,111.11; changes -1,428.57 and +1,111.11; per unit -0.714 and +0.556 (displayed -0.71 and +0.56). R1 and R3 are qualitative and state their limits.")
row("L04-keyresults", "2.3 grades", "course/modules/AC/AC4/L04.html key-results table (lines 474-481)", PASS,
    "T rows: Propositions 1.2, 3.1, 3.2. C rows: Lab 1 figures and Example 4.1 (conditional on the stated avoidability). The convention row cites Definition 1.1.")
row("L04-quiz", "2.9 structure", "course/modules/AC/AC4/L04.html quiz (lines 491-543)", PASS,
    "Correct options: q1 (exact sum with positive driver totals), q5 (0.0025 and 0.03), q8 (part of a pool stays). Numeric answers: 4.5; 10; 35,000; 42.5; 15,000 recomputed.")
row("L04-refs", "2.1 citations", "course/modules/AC/AC4/L04.html line 548", PASS,
    "See AC4b-cite-kaplan1998cost. No content claim from the book.")
# mutants
row("L03-L04-lab-mutants", "2.5 labs (student-error twin mutants, archived r30 set)", "ledgers/AC4/mutants/AC4-b-r30/m_L03_*.py (3), m_L04_*.py (4)", PASS,
    "All seven archived mutants re-run under python -I -W error (out/archived_mutants_r32.out): six exit 0 with stdout different from the expected block; m_L04_volume_rate_uses_units exits 1 (ValueError). All seven are killed. Lab-twin mutants are supporting evidence only (architect ruling).")
row("L03-L04-lab-mutants-r32", "2.5 labs (new student-error twin mutants)", "ledgers/AC4/mutants/AC4-b-r32/*.py (4 mutants, scripts make_and_run_mutants.py, run_archived.py)", PASS,
    "m_L03_decision_inverted: exit 0, stdout differs (killed). m_L04_stage_one_counts_reversed: exit 0, stdout differs (killed). m_L03_excess_hours_unclamped: exit 0 and stdout identical; the clamp is inert on this data (6,000 - 4,000 > 0) and no lesson sentence claims the lab checks it: out of scope, equivalent on the lab's data. m_L04_exact_check_removed survives and is recorded against row L04-remark13-lab (FAIL).")
row("L03-L04-no-project-slice", "2.6 projects", "this slice has no grader or project file", PASS,
    "Lesson-and-twin slice. No grader files in scope; no alternative correct implementations were written. The grader-level mutation test does not apply to this slice.")

mutants = [
 {"id": "m_L03_book_value_in_relevant_cost", "description": "student adds the sunk book value to the relevant difference", "killed_by": "stdout differs from expected block (r30 archive)"},
 {"id": "m_L03_fullcost_decision_uses_relevant", "description": "full-cost decision uses the avoidable cost without allocated overhead", "killed_by": "stdout differs from expected block (r30 archive)"},
 {"id": "m_L03_special_order_naive_hours", "description": "lost contribution charged on all order hours, not the excess", "killed_by": "stdout differs from expected block (r30 archive)"},
 {"id": "m_L04_setups_driven_by_inspections", "description": "setups assigned by the inspection driver counts", "killed_by": "stdout differs from expected block (r30 archive)"},
 {"id": "m_L04_stage_two_divides_by_hours", "description": "stage two divides by labour hours instead of units (per-unit print)", "killed_by": "stdout differs from expected block (r30 archive)"},
 {"id": "m_L04_stage_one_half_allocation", "description": "each pool allocation halved (rounded down)", "killed_by": "stdout differs from expected block (r30 archive)"},
 {"id": "m_L04_volume_rate_uses_units", "description": "volume rate spreads the pool by units instead of labour hours", "killed_by": "ValueError (uneven rate), exit 1 (r30 archive)"},
 {"id": "m_L03_decision_inverted", "description": "student reverses the relevant-cost comparison (make when net buy cost is lower)", "killed_by": "stdout differs from expected block"},
 {"id": "m_L04_stage_one_counts_reversed", "description": "student zips stage-one driver counts against products in reverse order", "killed_by": "stdout differs from expected block"},
 {"id": "m_L04_exact_check_removed", "description": "student replaces the exact-division check in exact_rate with floor division", "killed_by": None},
]
verified_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
counts = {s: sum(1 for r in rows if r["status"] == s) for s in (PASS, FAIL)}
frag = {
  "unit": "AC4",
  "slice": "AC4-b",
  "round": 32,
  "verifier": "round-32 independent verifier (Haiku) for slice AC4-b: L03, L04 and their lab twins; did not build AC4 and shares no context with the builders or earlier verifiers",
  "pin": "845ae46",
  "base": "5aeaaf0 (delta base; the round-31 fragment /tmp/fanout-frags/AC4-b.round31.json records pin 5aeaaf0)",
  "checkout": "/tmp/verify32-AC4-b (detached worktree at 845ae46; .venv symlink; vendor copied)",
  "scratch": "/tmp/AC4-v/AC4-b/r32/",
  "verified_at": verified_at,
  "verdict": "FAIL",
  "rows": rows,
  "mutants": mutants,
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Delta since 5aeaaf0: L03.html lines 328 (Lab 1 interpretation) and 490 (R2 solution) only. L04.html, the twins, and the L03/L04 card objects are unchanged. Every L03 and L04 row was re-derived this round, not carried, so no 'Carried from round 31' prefix is used.",
    "Fixed since round 31: L03-interp-first-line (now second line of output, verified) and L03-R2 (X defined, verified).",
    "New finding this round: L04-remark13-lab is FAIL. Mutant m_L04_exact_check_removed survives because Lab 1's printed run never reaches the ValueError branch, while line 74 claims Lab 1 'raises an error otherwise'.",
    "Notation: B is used as an alternative (Proposition 1.2) and as the book value (Proposition 2.2 proof, P2) in L03. B is not registered, so no registry rule breaks; recorded as a PASS observation with a recommended rename.",
    "Card count: 35 L03/L04 cards (round 31 stated 32).",
    "Not in this slice and not checked: project.html, cards for L01, L02, L05-L08, the lesson pages of other slices, check_projects, run_graders, mutate_graders (no grader files in this slice), and the full-gate pytest suite. The L02 and L06 card hunks in the delta belong to other slices.",
    "Pyodide timing: page_smoke ran in the local Chromium harness with --skip-sweep; the lab runs took 0.0 s each in page_smoke's report. No live figure exists on L03 or L04, so the sweep does not apply.",
    "Lab mutants are lab-twin demonstrations and are not graded as project mutants; the ruling is applied: only m_L04_exact_check_removed is a finding, because line 74 claims the behaviour.",
  ],
  "summary": {"rows": len(rows), "pass": counts[PASS], "fail": counts[FAIL], "unverifiable": 0, "fail_ids": [r["id"] for r in rows if r["status"] != PASS]},
}
out = ROOT / "ledgers/AC4/AC4-b.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts)
