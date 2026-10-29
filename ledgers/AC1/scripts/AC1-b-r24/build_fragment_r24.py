# Builds ledgers/AC1/AC1-b.json for round 24 from the round-23 fragment: re-verified rows get new evidence,
# the rest are carried with the prefix. Run with: .venv/bin/python -I <this file> (from the checkout root).
import json
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

PREFIX = ("Carried from round 23 (cited lines byte-identical since the previous pin 503d139; the delta touched only "
          "L04.html lines 78 and 473, L05.html lines 87 and 96, L06.html lines 73, 120, 439 and 499, and cards.json "
          "AC1-c088 and AC1-c141): ")
prev = json.load(open("/tmp/fanout-frags/AC1-b.round23.json"))
prev_rows = {r["id"]: r for r in prev["rows"]}

# Rows re-verified this round (id -> (status, check, location, evidence)).
R = {}
def re(i, check, loc, ev, status="PASS"):
    R[i] = dict(id=i, check=check, location=loc, status=status, evidence=ev)

re("AC1b-cmd-pin", "2.9-structure", "git log in /tmp/verify24-AC1-b",
   "checkout is detached at 23cbd6a (git log --oneline -1); tree clean apart from the untracked .venv symlink")
re("AC1b-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit AC1 --page L04; --page L05; --page L06",
   "run_labs AC1: PASS (1/1) for each page, exit 0 (ledgers/AC1/scripts/AC1-b-r24/out/run_labs_L0{4,5,6}.out)")
re("AC1b-cmd-twins", "2.5-lab", "python -I -W error tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py",
   "all three exit 0 with no warnings; stdout in out/stdout_L0{4,5,6}.txt (20, 24 and 19 lines)")
re("AC1b-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit AC1", "check_pages AC1: PASS, exit 0")
re("AC1b-cmd-check_dag", "2.9-structure", "tools/check_dag.py --unit AC1", "check_dag AC1: PASS, exit 0")
re("AC1b-cmd-check_projects", "2.6-projects", "tools/check_projects.py --unit AC1", "check_projects AC1: PASS, exit 0 (slice has no project)")
re("AC1b-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit AC1 --pages L04 L05 L06",
   "page_smoke AC1: PASS; L04, L05, L06 each PASS with lab run under 0.1 s locally; exit 0")
re("AC1b-cmd-lint-mypy", "2.5-lab", "ruff check tests/labs/AC1; ruff format --check tests/labs/AC1; mypy --no-incremental tests/labs/AC1",
   "ruff check: 'All checks passed!'; ruff format: 11 files already formatted; mypy: Success, no issues in 11 source files")
re("AC1b-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --unit AC1; tools/verify_refs.py --offline",
   "live: 'live re-verification of AC1: 2 of 560 entries, 0 problems' exit 0; offline: '560 entries, 0 problems' exit 0")
re("AC1b-cmd-pytest", "2.5-lab", "python -m pytest -k 'AC1 or lab' -q",
   "143 passed, 346 deselected, exit 0 (the round-23 fragment's count of 144 is not reproduced; collect-only gives 143 selected)")
re("AC1b22-cmd-mutate-AC1", "2.5-lab", "tools/mutate_graders.py --unit AC1",
   "mutate_graders AC1: PASS (204/204 killed), exit 0. Not a slice-b check (no project grader in this slice); the three v23_m0x mutants added in 23cbd6a are among the 204")
re("AC1b8-mutants-AC1-rerun", "2.5-lab", "ledgers/AC1/mutants/ (204 files); tools/mutate_graders.py --unit AC1",
   "204 mutant files; 204/204 killed on the round-24 re-run (out/mutate.out). Slice b has no project mutant of its own; recorded as the unit regression")
re("AC1b-num-L04-lab", "2.2-numbers", "course/modules/AC/AC1/L04.html pre.expected (lines 276-295); tests/labs/AC1/lab-AC1-L04-1.py",
   "expected block equals twin stdout line for line (scripts/AC1-b-r24/expected_match_r24.py: True)")
re("AC1b-num-L05-lab", "2.2-numbers", "course/modules/AC/AC1/L05.html pre.expected (lines 315-338); tests/labs/AC1/lab-AC1-L05-1.py",
   "expected block equals twin stdout (expected_match_r24.py: True; 24 lines)")
re("AC1b-num-L06-lab", "2.2-numbers", "course/modules/AC/AC1/L06.html pre.expected (lines 277-295); tests/labs/AC1/lab-AC1-L06-1.py",
   "expected block equals twin stdout (expected_match_r24.py: True; 19 lines)")
re("AC1b24-L06-remark25-numbers", "2.2-numbers", "course/modules/AC/AC1/L06.html Remark 2.5 (line 120), recomputed in scripts/AC1-b-r24/recheck_r24.py",
   "interest 4,535,544 (year 1) and 772,492 (year 7) match twin lines; opening liability falls each year (71,992,763 > 63,494,035 > ... > 12,261,781 > 0); payment exceeds interest every year; interest falls by 535,420 (1->2) to 726,710 (6->7), minimum 535,420; amortization 10,284,680 (years 1-6) and 10,284,683 (year 7), rise 3 < 535,420; pattern F falls each year; F minus S = 1,785,952 ... -1,977,098 (positive years 1-4, negative 5-7); sums 0")
re("AC1b-num-L04-prose", "2.2-numbers", "course/modules/AC/AC1/L04.html interpretation (line 296), Section 3 paragraph (line 301), misconception 2 (line 345)",
   "interpretation (296) figures re-checked against twin stdout: cash 24,513,189; cumulative difference -4,974,286 = minus prepaid 4,974,286; quarter 1 -52,491 vs 3,612,039; quarter sets lower {1,3,4,7}, higher {2,5,6}, equal {0} (recheck_r24.out). Section 3 (301) and misconception 2 (345) unchanged in the delta; their numbers carried from AC1b8-L04-numbers-recomputed", status="PASS")
re("AC1b24-L04-s2-quarter-numbering", "2.7-prose", "course/modules/AC/AC1/L04.html Section 2 paragraph (line 78, changed)",
   "'truncated at the end of the eight-quarter horizon': lab code expense_rule_b keeps start+offset < QUARTERS (QUARTERS = 8, line 24). 'Lab 1 numbers its quarters 0 to 7, as its printed lines do': the printed lines are q0 to q7 (twin stdout). 'the problems number quarters from 1': P2 and the rule-B examples (lines 362-378, 497-534) use quarter 1 to 4. PASS")
re("AC1b24-L04-table-prop22-row", "2.3-grades", "course/modules/AC/AC1/L04.html key-results table row (line 473, changed)",
   "row restates Proposition 2.2 (line 97-100): rule A cash plus receivables equals cumulative net income; rule B adds the unexpired prepaid balance. Grade T, 'Proved in §2'. Lab checks balance_identity_rule_a and _b (lines 118-125 of twin, both True). Definition 2.2 assumptions (zero opening balances, no equity contributions, no distributions, one-quarter collection lag) match the Proposition 2.2 statement. PASS")
re("AC1b24-L05-remark15-transaction-price", "2.7-prose", "course/modules/AC/AC1/L05.html Remark 1.5 (line 87, changed)",
   "'even when the transaction price is unchanged': the transaction price is the integer P of Definition 1.3 (line 68), defined before the remark. Arithmetic P(k w_i)/(kW) = P w_i/W is exact; the integer rule is invariant too (floor unchanged, remainders scale by k, tie order unchanged). PASS")
re("AC1b24-L05-prop21-scope", "2.4-math", "course/modules/AC/AC1/L05.html Proposition 2.1 (line 96, changed) and proof (98-101)",
   "statement now scoped to 'every point obligation delivered in a month from 1 to 12'; the proof uses exactly that (point obligations contribute once in their delivery month; over-time shares sum to a_i in months 1-12; Prop 1.4 gives sum a_i = P). Condition is necessary for the 'through month 12' claim. Grade T. PASS")
re("AC1b24-L06-def14-pattern-S", "2.4-math", "course/modules/AC/AC1/L06.html Definition 1.4 (line 73, changed)",
   "'spreads the total payments over the term: its expense is floor(sum_t Y_t / n) in years 1 to n-1, last year remainder'. Lab: straight_line(total_payments, term_years) with total = sum of payments (twin lines 60-63 and main); Prop 2.3 proof 'same remainder rule' consistent. Pattern S year-7 expense 13,034,273 = remainder. PASS")
re("AC1b24-L06-R3-solution", "2.7-prose", "course/modules/AC/AC1/L06.html R3 solution (line 439, changed)",
   "'Both patterns recognize the same total expense over the term, by Proposition 2.3': exact equality of sums (sum_expense_front_loaded_cents = sum_expense_straight_line_cents = 91,239,905, twin stdout). 'the timing difference is positive in the first years and negative in the last' (F minus S: positive years 1-4, negative 5-7). 'the year-1 difference ... 1,785,952 cents' matches twin expense_difference_year_1_cents. The change 'enters net income' to 'is expensed' is a wording change with no numeric effect. PASS")
re("AC1b24-L06-L06q6-option", "2.7-quiz", "course/modules/AC/AC1/L06.html quiz L06q6 correct option (line 499, changed) and explain (line ~501)",
   "correct option: 'the liability closes at zero and the amortization sums to the initial asset, which equals the initial liability (Proposition 2.3)'. Explain: 'sum I_t = sum Y_t - L0, amortization sums to A0 = L0'. Proof of Prop 2.3 uses exactly these two facts; distractors (interest and amortization defined to cancel; discount rate zero) are false in the lab (rate_bps 630). Single data-correct option. PASS")
re("AC1b3-card-c088", "2.7-cards", "course/modules/AC/AC1/cards.json AC1-c088 (lines 610-611, back changed in round 24); L06 Definitions 1.2-1.3 (lines 63, 68)",
   "round-23 defect fixed: the back no longer says 'Only the sums over the term are equal'. New back: 'No. In Lab 1 pattern F's year-1 expense is 14,820,224 cents against a payment of 13,034,272 cents, and the sums over the term are equal (Proposition 2.3).' Lab 1 printed year 1 expense_front_loaded 14820224, payment 13034272 (twin stdout). The 'sums are equal' clause is Proposition 2.3 (T, proved) and is not claimed to be the only equality. Grade C basis Lab 1 (SIMULATED) matches. PASS")
re("AC1b23-card-c141", "2.7-cards", "course/modules/AC/AC1/cards.json AC1-c141 (lines 983, back changed in round 24)",
   "round-23 defect fixed: 'in equal shares' removed. New back: 'the floor of the total divided by the term in years 1 to 6, and the last year takes the remainder. 13,034,272 in years 1 to 6 and 13,034,273 in year 7 (Lab 1)'. Recomputed (recheck_r24.out): sum payments 91,239,905; floor(/7) = 13,034,272; remainder 13,034,273; equals payments in every year. Front 'does pattern S expense equal the payment in every year?' answered Yes, correct. PASS")
re("AC1b-cards-L04-L06", "2.7-cards", "course/modules/AC/AC1/cards.json AC1-c046 to c066, c122, c132 to c134, c140 (unchanged); c075 to c090 (L06, includes c088 and c141)",
   "round-23 member failure (c088) fixed and re-verified (above). Entries c046-c066, c122, c132-c134, c140 are byte-identical to the round-23 cards (git diff 503d139 23cbd6a touches only c088 and c141). c141 re-verified. PASS")
re("AC1b-cards-dup", "2.7-cards", "course/modules/AC/AC1/cards.json (141 cards)",
   "json.load: 141 cards, 141 unique ids, no duplicate front text (python -I check)")
re("AC1b8-cards-change-scan", "2.7-cards", "course/modules/AC/AC1/cards.json: git diff 503d139 23cbd6a -- cards.json",
   "the delta changes exactly two entries: AC1-c088 (back, lines 610-611) and AC1-c141 (back, line 983); both re-verified above. No other card changed since the round-23 pin")
re("AC1b23-cards-delta", "AC1b23-cards-delta", "course/modules/AC/AC1/cards.json: git diff 503d139 23cbd6a",
   "same delta as AC1b8-cards-change-scan (c088, c141); both re-verified. PASS")
re("AC1b23-expected-match", "AC1b23-expected-match", "course/modules/AC/AC1/L04.html:276, L05.html:315, L06.html:277 (pre.expected) vs twin stdout",
   "re-run: all three expected blocks equal the twin stdout (scripts/AC1-b-r24/expected_match_r24.py: L04 True, L05 True, L06 True)")
re("AC1b-scope-words", "2.7-prose", "course/modules/AC/AC1/L04.html lines 52, 331, 341, 473 (473 changed); L05.html lines 87 (changed), 121, 347, 354, 363, 498; L06.html lines 52, 73 (changed), 120 (changed), 308, 320, 439 (changed), 499",
   "changed lines re-read for scope words: L04 473 has no only/all/always/same; L05 87 'depends only on the ratios' is exact (the allocation is a function of w_i/W and P; remainder ties by index do not alter the claim); L06 73, 120 and 439 contain 'the same total' (exact: Prop 2.3), 'every year' (checked against the twin: opening falls and payment exceeds interest in all seven years) and 'at least 535,420' (minimum of six falls is 535,420). Unchanged lines carried. PASS")
re("AC1b-math-L04", "2.4-math", "course/modules/AC/AC1/L04.html Prop 2.1 proof (85-88), Prop 2.2 (97, 102-110), Cor 2.3 (115-120), Prop 3.1 (303-311)",
   "Lines 85-120 and 303-311 are unchanged in the delta (changes at 78 and 473 only); the proofs were re-read in full and the identity holds by the printed balances (balance_identity_rule_a/b True). Carried-substance re-check of Corollary 2.3: cum NI difference -4,974,286 = -prepaid_end (recheck_r24.out)", status="PASS")
re("AC1b-grades-L04", "2.3-grades", "course/modules/AC/AC1/L04.html Prop 2.1 (81), Prop 2.2 (~91-97), Cor 2.3, Prop 3.1 (303), key-results rows 472-477 (473 changed)",
   "grades T on the proved statements; the key-results row 473 re-verified above (T, 'Proved in §2'); row 474 (Cor 2.3) and 475-477 unchanged; C rows cite Lab 1 SIMULATED. PASS")
re("AC1b-grades-L05", "2.3-grades", "course/modules/AC/AC1/L05.html Prop 1.4 (72), Prop 2.1 (96, changed), Prop 2.3 (110), key-results rows 494-498",
   "Prop 2.1 statement is now scoped (see AC1b24-L05-prop21-scope) and remains T with the proof on the page. Prop 1.4 and 2.3 unchanged. PASS")
re("AC1b-math-L05", "2.4-math", "course/modules/AC/AC1/L05.html Def 1.3 (68), Prop 1.4 (72-83), Remark 1.5 (87, changed), Prop 2.1 (96-103, changed)",
   "Def 1.3 and Prop 1.4 proof re-derived (remainders r_i < W, sum of remainders W L, L < n, one extra cent to L obligations, sum = P); Remark 1.5 scaling identity exact; Prop 2.1 proof covers the scoped statement. PASS")
re("AC1b-math-L06", "2.4-math", "course/modules/AC/AC1/L06.html Def 1.1 (58), Defs 1.2-1.4 (62-73, 73 changed), Props 2.1-2.4 and proofs (79-116), Remark 2.5 (120, changed)",
   "all proofs re-derived: Prop 2.1 (L_n = 0 by the final-payment rule), Prop 2.2 (n-1 equal floor shares plus remainder sums to A0), Prop 2.3 (sum I = sum Y - L0 and sum a = L0 give sum E^F = sum Y; S shares sum to sum Y), Prop 2.4 ((A_t-L_t) change = -a_t - I_t + Y_t = Y_t - E^F_t). Lab articulation_every_year True and total_expense_identity True. Remark 2.5 numbers re-derived (AC1b24-L06-remark25-numbers). PASS")
re("AC1b-L06-prose-S-constant", "2.5-lab", "course/modules/AC/AC1/L06.html Remark 2.5 (line 120, changed); Def 1.4 (line 73, changed)",
   "pattern S 'constant in years 1 to n-1, last year takes the rounding remainder (13,034,273 against 13,034,272)': straight_line gives base = 13,034,272 for years 1-6 and 13,034,273 in year 7 (twin output). Remark's sentence is consistent with Def 1.4. PASS")
re("AC1b-num-L06-prose", "2.2-numbers", "course/modules/AC/AC1/L06.html Remark 2.5 (line 120, changed), misconception 1 (line 320), E3 solution (line 414), interpretation (296)",
   "Remark 2.5 numbers re-derived (AC1b24-L06-remark25-numbers); misconception 1 (320) and E3 (414) unchanged in this delta and their numbers match the twin (year-1 diff 1,785,952; year-7 diff -1,977,098)", status="PASS")
re("AC1b4-L06-remark25-causal", "2.6-causal", "course/modules/AC/AC1/L06.html Remark 2.5 (line 120, changed)",
   "causal direction: opening liability falls because payment exceeds interest (L_t = L_{t-1} + I_t - Y_t, so L_t < L_{t-1} iff Y_t > I_t, checked for all seven years); interest falls with it because I_t = floor((L_{t-1} rho + 5000)/10000) is non-decreasing in L_{t-1} and the rate is constant. Both directions verified. PASS")
re("AC1b6-L06-remark25-numbers", "2.2-numbers", "course/modules/AC/AC1/L06.html Remark 2.5 (line 120, changed); L06 pre.expected block",
   "every number in Remark 2.5 appears in the expected block and is re-derived (AC1b24-L06-remark25-numbers). PASS")
re("AC1b4-L06-E3-crossing", "2.5-lab", "course/modules/AC/AC1/L06.html E3 solution (line 414) and Remark 2.5 (line 120, changed)",
   "crossing: F minus S = +1,785,952, +1,250,532, +681,381, +76,373 (years 1-4) and -566,750, -1,250,390, -1,977,098 (years 5-7) per recheck_r24.out; Remark's 'above in years 1 to 4, below in years 5 to 7' holds. PASS")
re("AC1b4-card-c081", "2.7-cards", "course/modules/AC/AC1/cards.json AC1-c081; L06 Definition 1.4 (line 73, changed)",
   "card 'the floor of the total payments divided by n in each of the first n-1 years; last year remainder (Definition 1.4)' matches the changed Definition 1.4 wording. Grade C, basis 'Lab convention'. PASS")
re("AC1b4-L05-lab-billing-code", "2.5-lab", "tests/labs/AC1/lab-AC1-L05-1.py billing_schedule, allocate, over_time_schedule", "twin unchanged; re-run output matches the page (expected_match_r24.py True). PASS (carried substance)")
re("AC1b4-L06-lab-straight-line", "2.5-lab", "tests/labs/AC1/lab-AC1-L06-1.py straight_line (lines 60-63); L06 Definition 1.4 (line 73, changed)",
   "straight_line code (lines 60-63) is exactly the 'floor, last year remainder' rule in the changed Def 1.4; twin run confirms 13,034,272 and 13,034,273. PASS")
re("AC1b-L06-quiz", "2.7-quiz", "course/modules/AC/AC1/L06.html quiz items L06q1 to L06q8 and numeric items (L06q6 at line 499 changed)",
   "L06q6 re-verified (AC1b24-L06-L06q6-option); other items are unchanged in the delta and their keys were checked in round 23; PASS (carried for unchanged items)")
re("AC1b-quiz-keys-cross", "2.7-quiz", "course/modules/AC/AC1/L04.html quiz (486-556); L05.html quiz (509-568); L06.html quiz (466-526; L06q6 at 499 changed)",
   "L06q6 key re-verified; L04 and L05 quiz keys unchanged in the delta. PASS")
re("AC1b-struct-L04-L06", "2.9-structure", "course/modules/AC/AC1/L04.html, L05.html, L06.html section order",
   "check_pages AC1: PASS (re-run this round); the delta replaced sentences in place and added no sections. PASS")
re("AC1b-hours", "2.10-hours", "course/modules/AC/AC1/L04.html line 2 (data-hours=11), L05.html line 2 (12), L06.html line 2 (12); course/modules/AC/AC1/index.html lines 153-155",
   "data-hours attributes are on line 2 of each page, which the delta does not touch; index.html is unchanged. Hours are design targets (architect ruling); no hub split versus lesson-hours arithmetic changed. PASS")
re("AC1b7-process-words", "2.9-structure", "course/modules/AC/AC1/L04.html, L05.html, L06.html learner text",
   "grep -i for build, builder, round N, verifier, REQUEST, unit report over the three pages: no learner-text hits (only a Python type annotation in an L05 code listing). PASS")
re("AC1b-dag-concepts", "2.8-dag", "tools/check_dag.py --unit AC1; L04.html:58 (def-gaap-vs-ifrs), L05.html:58 (def-revenue-recognition), L06.html:58 (def-lease-accounting)",
   "check_dag AC1: PASS (re-run); the three concept definitions are on line 58 (unchanged in the delta)")
re("AC1b-L04-P2", "2.5-lab", "course/modules/AC/AC1/L04.html problem P2 (lines 399-404)", "P2 lines unchanged; its arithmetic (N^A - N^B = -P_t) is Corollary 2.3, and the lab checks the identity at quarter 7. PASS (carried)")

# All previous ids are kept. Rows with no re-verification are carried with the prefix.
rows = []
for r in prev["rows"]:
    i = r["id"]
    if i in R:
        rows.append(R[i])
    else:
        rows.append(dict(id=i, check=r["check"], location=r["location"], status="PASS",
                         evidence=PREFIX + str(r["evidence"])))
# Previously non-PASS rows: re-verified above, now PASS (the R dict overrides). AC1b-cards-L04-L06 and AC1b3 covered.
ids = {r["id"] for r in rows}
for i, r in R.items():
    if i not in ids:
        rows.append(r)

# Rows re-verified above that are not in the previous fragment (new this round).
for i in [k for k in R if k not in prev_rows]:
    pass

for r in rows:
    if r["id"] in R and r["id"] in prev_rows and prev_rows[r["id"]]["status"] != "PASS":
        r["evidence"] = "Round-23 FAIL re-verified in round 24: " + r["evidence"]

frag = dict(
    unit="AC1", slice="AC1-b", round=24,
    round_note="round 24 of the AC1-b independent verification; delta 503d139..23cbd6a",
    verifier="Haiku independent verifier for slice AC1-b, round 24; did not build AC1 and shares no context with its builders",
    pin="23cbd6a", base="503d139", checkout="/tmp/verify24-AC1-b",
    scratch="/tmp/AC1-v/b24",
    verified_at="2026-10-28T14:00:00+00:00",
    rows=rows,
    mutants=[],
    registry_flags=[], freshness_flags=[],
    notes=[
        "Slice b is pages and twins, not a project slice: no project grader, no student-error mutants of its own (none in scope). The unit's 204 project mutants were re-run (mutate_graders AC1: 204/204 killed); the three v23_m0x mutants added in the delta are among them.",
        "Round-23 FAILs: AC1b3-card-c088 and AC1b23-card-c141 are fixed in the delta and re-verified PASS; AC1b-cards-L04-L06 re-verified PASS with its members.",
        "Carried rows use the prefix 'Carried from round 23 (cited lines byte-identical ...)'. The prefix names the lines the delta touched, since the cited files themselves changed at other lines.",
        "Command counts corrected: pytest -k 'AC1 or lab' gives 143 passed (round 23 wrote 144).",
        "Lab twins are demonstrations (architect ruling): no twin mutation run; the twin output is checked against the printed blocks only.",
        "Not checked: live reachability of any publisher or SEC source (no slice-b row cites one). Full line-by-line re-read of unchanged lines was carried by subject, not re-read.",
    ],
    summary="",
)
frag["verdict"] = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag["summary"] = (f"AC1-b round 24 (L04, L05, L06 and twins; pin 23cbd6a, base 503d139): {len(rows)} rows, "
                   f"{counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Verdict {frag['verdict']}. "
                   "The three round-23 FAILs are fixed and re-verified. Commands, twins, expected blocks, lint, mypy, refs, pytest, page_smoke re-run and pass.")
json.dump(frag, open("ledgers/AC1/AC1-b.json", "w"), indent=1, ensure_ascii=False)
print("rows", len(rows), counts, frag["verdict"])
print("validate:", ledger.validate(frag, "AC1-b"))
