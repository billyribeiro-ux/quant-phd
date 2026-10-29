"""Build the round-18 AC1-b fragment (verifier output) and validate it with tools/ledger.py."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

CHECKOUT = Path("/tmp/verify18-AC1-b")
sys.path.insert(0, str(CHECKOUT / "tools"))
import ledger  # noqa: E402

CARRY = "Carried from round 17 (course/modules/AC/AC1/index.html, L04.html data-hours, L05.html data-hours, L06.html data-hours byte-identical since the previous pin, fefbf8b; the delta changed none of them): "

rows: list[dict[str, str]] = []


def add(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        row["fix"] = fix
    rows.append(row)


# ---- commands (re-run this round on pin 7143726)
add(
    "AC1b-cmd-pin",
    "2.9-structure",
    "repository; course/modules/AC/AC1/L04.html, L05.html, L06.html; tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py; course/modules/AC/AC1/cards.json",
    "PASS",
    "git rev-parse HEAD = 7143726 (detached, /tmp/verify18-AC1-b; git status shows only the .venv symlink and this round's ledgers/AC1/scripts/AC1-b-r18/). git diff --stat fefbf8b 7143726 -- course/modules/AC/AC1 tests/labs/AC1: slice-b files changed: L04.html (35 lines), L05.html (6), L06.html (2), cards.json (2: card AC1-c060 only), tests/labs/AC1/lab-AC1-L04-1.py (3). L07, L08, project.html, grader/test_project.py and tests/labs/AC4 are outside slice b. Every slice-b hunk was read (scratch diff output).",
)
add(
    "AC1b-cmd-run_labs",
    "2.5-lab",
    "tools/run_labs.py --unit AC1 --page L04 / L05 / L06",
    "PASS",
    "Run this round: 'run_labs AC1: PASS (1/1)' for each of L04, L05 and L06 (exit 0). Output in ledgers/AC1/scripts/AC1-b-r18/out/.",
)
add(
    "AC1b-cmd-twins",
    "2.5-lab",
    "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py",
    "PASS",
    "python -I -W error on each twin: exit 0. Stdout compared with the page pre.expected block (HTML-unescaped, stripped, line by line): L04 20 lines equal True, L05 22 lines equal True, L06 19 lines equal True (ledgers/AC1/scripts/AC1-b-r18/out/out_L0*.txt).",
)
add(
    "AC1b-cmd-check_pages",
    "2.9-structure",
    "tools/check_pages.py --unit AC1",
    "PASS",
    "'check_pages AC1: PASS' (exit 0; ledgers/AC1/scripts/AC1-b-r18/out/check_pages.txt).",
)
add(
    "AC1b-cmd-check_dag",
    "2.9-structure",
    "tools/check_dag.py --unit AC1",
    "PASS",
    "'check_dag AC1: PASS' (exit 0; out/check_dag.txt).",
)
add(
    "AC1b-cmd-check_projects",
    "2.6-projects",
    "tools/check_projects.py --unit AC1",
    "PASS",
    "'check_projects AC1: PASS' (exit 0; out/check_projects.txt). The project slice is outside slice b.",
)
add(
    "AC1b-cmd-page_smoke",
    "2.9-structure",
    "tools/page_smoke.py --unit AC1 --pages L04 L05 L06",
    "PASS",
    "'page_smoke AC1: PASS' (exit 0). L04, L05, L06 each PASS; runtime boot with numpy 1.1 s; lab-AC1-L05-1 0.0 s; lab-AC1-L06-1 0.0 s (out/page_smoke.txt).",
)
add(
    "AC1b-cmd-lint-mypy",
    "2.5-lab",
    "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py; course/modules/AC/AC1",
    "PASS",
    ".venv/bin/ruff check tests/labs/AC1 course/modules/AC/AC1: 'All checks passed!'; ruff format --check tests/labs/AC1: '11 files already formatted'; mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files'.",
)
add(
    "AC1b-cmd-verify_refs",
    "2.1-citations",
    "tools/verify_refs.py --unit AC1; tools/verify_refs.py --offline",
    "PASS",
    "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'. tools/verify_refs.py --unit AC1 (live): 'live re-verification of AC1: 2 of 560 entries, 0 problems'. No slice-b page cites a registry key (see AC1b-cit-none).",
)
add(
    "AC1b-cmd-pytest",
    "2.5-lab",
    "pytest -q -k 'AC1 or lab'",
    "PASS",
    ".venv/bin/pytest -q -k 'AC1 or lab': exit 0; progress lines only (out/pytest.txt). No summary line is printed by this configuration and the collect-only count was not obtained; the page's test count is therefore not checked here.",
)
add(
    "AC1b-cit-none",
    "2.1-citations",
    "course/modules/AC/AC1/L04.html:561-562, L05.html:568-569, L06.html:532-533 (References sections)",
    "PASS",
    "Grep for data-ref, ref-key, data-cite and references.json in the three pages: no match. The only reference list is the empty <ol data-references></ol> (L04:562, L05:569, L06:533). The References sentences state that no source is cited. No registry key is cited, so there is no citation to check.",
)

# ---- numbers and labs
add(
    "AC1b-num-L04-lab",
    "2.2-numbers",
    "course/modules/AC/AC1/L04.html pre.expected (lines 276-295); tests/labs/AC1/lab-AC1-L04-1.py",
    "PASS",
    "Page pre.expected equals the twin output (AC1b-cmd-twins, 20 lines). Independent recomputation in ledgers/AC1/scripts/AC1-b-r18/chk_l04_r18.py (own generator, seed 2604): prepaid_paid [0, 4886040, 0, 4233446, 6325624, 0, 0, 6632381]; prepaid_balance_b [0, 3664530, 2443020, 4396595, 6860942, 4221175, 1581406, 4974286]; ni_a and ni_b equal the printed values in all eight quarters; cash_end 24,513,189; cum NI A 28,439,204, cum NI B 33,413,490; interest total 3,319,293; CFO2 27,832,482. All match.",
)
add(
    "AC1b-num-L04-prose",
    "2.2-numbers",
    "course/modules/AC/AC1/L04.html interpretation (line 296), Section 3 paragraph (line 318), misconception 2 (line 345), section 5 bullet 2 (line 330), E1-E3 solutions (lines 421-435), Remark 2.4",
    "PASS",
    "Recomputed in chk_l04_r18.py: per-quarter NI_A minus NI_B = [0, -3664530, 1221510, -1953575, -2464347, 2639767, 2639769, -3392880] equals minus the change in prepaid_balance_b in every quarter (True), so the interpretation's claim holds. Rule A lower in quarters 1, 3, 4, 7; higher in 2, 5, 6; equal in 0 (E1 counts four, three, one: correct). 3319293/27832482 = 0.1192597 (0.1193; 0.11926 unrounded, line 318). 3319293/24513189 = 0.1354085 (0.1354, E3). 6632381 // 4 = 1658095 and 6632381 - 1658095 = 4974286 (line 345). E2: 28439204 - 33413490 = -4974286.",
)
add(
    "AC1b-num-L05-lab",
    "2.2-numbers",
    "course/modules/AC/AC1/L05.html pre.expected (lines 311-332); tests/labs/AC1/lab-AC1-L05-1.py",
    "PASS",
    "Page pre.expected equals the twin output (22 lines equal). Independent recomputation in chk_l05_r18.py (own generator, seed 2605): price 80,495,111; allocation [5434051, 9440568, 29888194, 35732298] sums to the price; month-6 revenue 50,471,362; convention-2 month 6 29,888,194; difference 20,583,168; 40% balance peak 32,792,272 with 0 asset months; 0% balance min -23,333,398 with 8 asset months.",
)
add(
    "AC1b-num-L05-prose",
    "2.2-numbers",
    "course/modules/AC/AC1/L05.html interpretation (line 333), misconceptions (lines 355-365), section 4 bullets (lines 345-348), E1-E3 solutions",
    "PASS",
    "chk_l05_r18.py: shares 0.0675, 0.1173, 0.3713, 0.4439 (sum 1.0000); 50471362/80495111 = 0.627012 (0.6270); 32792272/80495111 = 0.407382 (E2 0.4074); 23333398/80495111 = 0.289873 (0.2899); the first six monthly shares of the two over-time amounts are 2,717,022 and 17,866,146 (452837 and 2977691 per month, remainders 452844 and 2977697); total 20,583,168. Interpretation text matches each figure.",
)
add(
    "AC1b-num-L06-lab",
    "2.2-numbers",
    "course/modules/AC/AC1/L06.html pre.expected (lines 277-295); tests/labs/AC1/lab-AC1-L06-1.py",
    "PASS",
    "Page pre.expected equals the twin output (19 lines equal). The printed roll-forward (liability, interest, payment, amortization, expenses) was checked by hand arithmetic in the interpretation: 71992763 x 630 / 10000 = 4535544.069 (rounds to 4,535,544); patterns total 91,239,905; F-S difference year 1 1,785,952 and year 7 -1,977,098; final payment 13,034,273 (adjustment 1).",
)
add(
    "AC1b-num-L06-prose",
    "2.2-numbers",
    "course/modules/AC/AC1/L06.html Remark 2.5 (line 120), E1 and E3 solutions, interpretation paragraph, misconceptions 1-2",
    "PASS",
    "Remark 2.5 figures checked against the printed lab lines: opening liability falls every year; interest 4,535,544 (y1) and 772,492 (y7); interest falls by 535,420 (y1 to y2, the smallest fall; y2 to y3 569,151; y3 to y4 605,008; y4 to y5 643,123; y5 to y6 683,640; y6 to y7 726,710); pattern F expense 14,820,224 falling every year to 11,057,175; amortization 10,284,680 in y1 to y6 and 10,284,683 in y7; S = 13,034,272 and 13,034,273 in y7; F above S in y1 to y4 and below in y5 to y7 (y4 13,110,645 > 13,034,272; y5 12,467,522 < 13,034,272). E1 14820224/91239905 = 0.162431 (0.1624). E3 difference 12467522 - 13034272 = -566750. Misconception 1: asset 61,708,083 less liability 63,494,035 = -1,785,952 after year 1. All match out_L06.txt.",
)
add(
    "AC1b-grades-L04",
    "2.3-grades",
    "course/modules/AC/AC1/L04.html Prop 2.1 (line 81), Prop 2.2 (line 96), Cor 2.3 (line 114), Prop 3.1 (line 303) and key-results rows 472-477",
    "PASS",
    "T-graded statements (Props 2.1, 2.2, Cor 2.3, Prop 3.1) each carry a proof on the page (proof blocks at lines 85-88, 100-111, 118-121, 308-311) that I re-derived. Key-results rows: the lab-derived 3,319,293 row is C with basis 'Lab 1, SIMULATED, one seed (2604)'; the standards row is 'open'. Grades are consistent with BLUEPRINT section 3 as applied in prior rounds; no external constant is graded here.",
)
add(
    "AC1b-grades-L05",
    "2.3-grades",
    "course/modules/AC/AC1/L05.html Prop 1.4 (line 72), Prop 2.1 (line 96), Prop 2.3 (line 110), key-results rows 488-492",
    "PASS",
    "Props 1.4, 2.1, 2.3 are T with proof blocks after each statement (lines 72, 96, 110) re-derived. P3 (key-results row 4) is T with its solution in the problem set. The 40%/0% balance row and the month-6 numbers are C with basis 'Lab 1, SIMULATED, one seed (2605)'. Consistent.",
)
add(
    "AC1b-grades-L06",
    "2.3-grades",
    "course/modules/AC/AC1/L06.html Props 2.1-2.4 (lines 79, 89, 99, 109) and key-results rows 451-455",
    "PASS",
    "Props 2.1-2.4 are T; each proof re-derived in this round (integer closure, A_t running sum, sum of recursion, articulation). Key-results: the lab-derived expense difference row is C with basis 'Lab 1, SIMULATED, one seed (2606)'; the open row names the four decisions. Consistent.",
)
add(
    "AC1b-math-L04",
    "2.4-math",
    "course/modules/AC/AC1/L04.html Prop 2.1 proof (85-88), Prop 2.2 statement (97) and proof (102-110), Cor 2.3 (115-120), Prop 3.1 proof (308-311)",
    "PASS",
    "Re-derived: C_t = sum S + sum_{s<t} K - sum(Q+O+I); C_t + R_t = sum(S+K) - sum(Q+O+I) = N^A_t; P_t = sum Q - sum E gives C_t + R_t + P_t = sum(S+K) - sum(O+I+E) = N^B_t. The new hypotheses in Prop 2.2 (zero opening balances, no equity contributions, no distributions, one-quarter collection) are the ones the proof uses (the collection term sum_{s<t} K_s needs collection lag; the zero opening terms give C_0 = 0). Cor 2.3 by subtraction. Prop 3.1 by direct algebra.",
)
add(
    "AC1b-math-L05",
    "2.4-math",
    "course/modules/AC/AC1/L05.html Def 1.3 (68), Prop 1.4 statement (72) and proof (74-83), Remark 1.5 (87), Prop 2.1 (96) and proof (98-103)",
    "PASS",
    "Re-derived Prop 1.4: f_i = floor(P w_i / W) is a non-negative integer when P >= 0; r_i = P w_i - W f_i in [0, W); sum r_i = W L with L >= 0, and sum r_i < nW gives L < n, so one extra cent for each of L distinct obligations gives sum a_i = P. The added hypothesis 'P a non-negative integer' is required for the non-negativity claim (for P < 0 the floors are negative). The sum identity itself holds for any integer P, so Prop 2.1 (which applies Prop 1.4 only for the sum) is correctly stated under Definition 1.3. Remark 1.5 scaling identity P(kw)/(kW) = Pw/W holds. Checked numerically: P = -1, weights (1,1) gives a = [0,-1], sum -1 (sum identity holds, non-negativity fails), which is why the hypothesis is needed for Prop 1.4 and not for the sum.",
)
add(
    "AC1b-math-L06",
    "2.4-math",
    "course/modules/AC/AC1/L06.html Def 1.1 (58), Defs 1.2-1.4 (lines 62-73), Props 2.1-2.4 and proofs (79-116), Remark 2.5 (120)",
    "PASS",
    "Re-derived: L_n = L_{n-1} + I_n - Y_n = 0 by the final-payment rule; A_n = 0 by the n-1 equal shares plus remainder; sum I_t = sum Y_t - L_0 and sum a_t = A_0 = L_0 give sum E^F = sum Y; S shares sum to sum Y by the remainder rule; Prop 2.4 = (-a_t) - (I_t - Y_t) = Y_t - E^F_t. The new Def 1.1 wording ('n annual contractual payments of P cents each') matches the lab (payment_cents, term_years).",
)
add(
    "AC1b-math-notation",
    "2.4-math",
    "notation/notation.json (macros and symbols); course/modules/AC/AC1/L04.html Def 2.2 and Prop 2.2 (lines 92, 97), L05.html Def 1.3 and Prop 1.4 (lines 68, 72), L06.html Def 1.1 (line 58)",
    "PASS",
    "notation/notation.json has no AC1 entry (its symbols are AP1, M4, S1 entries; schema keys macros and symbols). The symbols used in the changed sentences (C_t, R_t, P_t, N^A_t, N^B_t, P, a_i, w_i, W, n, Y_t, A_t, L_t) are each defined on the same page before first use (L04 Def 2.2 line 92; L05 Def 1.3 line 68; L06 Def 1.1 line 58 and Def 1.2-1.4). No new symbol is introduced by the delta.",
)

# ---- lab hypotheses and prose
add(
    "AC1b-L04-hypothesis-lab",
    "2.5-lab",
    "course/modules/AC/AC1/L04.html hypothesis (line 130); tests/labs/AC1/lab-AC1-L04-1.py main()",
    "PASS",
    "Hypothesis states that the cash match checks the code and not the rules: the lab computes cash_end_cents_rule_b from cash_end (the same cumulative sum) and prints cash_identical_across_rules True; the code comment and printed output agree. Balance identities, corollary and presentation identity are the four printed identities (balance_identity_rule_a/b, cumulative_difference_identity, presentation_identity). Stated as an algebraic consequence, as the lab docstring says.",
)
add(
    "AC1b-hyp-L06-few-cents",
    "2.5-lab",
    "course/modules/AC/AC1/L06.html hypothesis (line 125); tests/labs/AC1/lab-AC1-L06-1.py main() and docstring",
    "PASS",
    "The hypothesis says the final payment differs from the contractual payment by the rounding residual that the lab prints. The lab prints final_payment_cents 13034273, contractual_payment_cents 13034272 and final_payment_adjustment_cents 1 (out_L06.txt), and the docstring says the final payment absorbs the schedule's rounding.",
)
add(
    "AC1b-L05-prose-checks-m6",
    "2.5-lab",
    "course/modules/AC/AC1/L05.html paragraph after Section 2 (line 124); tests/labs/AC1/lab-AC1-L05-1.py",
    "PASS",
    "Paragraph says the difference at m < 12 equals the convention-1 over-time revenue, and that Lab 1 checks it at month 6. The lab prints month_6_difference_cents 20583168, over_time_convention_1_month_6_cents 20583168 and month_6_difference_equals_over_time_revenue True.",
)
add(
    "AC1b-L05-prose-as-much-as",
    "2.7-prose",
    "course/modules/AC/AC1/L05.html section 4 bullets (lines 345-348), line 357, line 365; scan of L04, L05, L06 for 'as much as', 'always', 'drives', 'offsets', 'raises', 'only', 'all', 'same'",
    "PASS",
    "Scripted scan (static_r18.py) of the three pages: 'as much as' 0 hits, 'always' 0, 'drives' 0, 'offsets' 0. 'only' and 'all' hits were read in context: L04 'Only the operating and financing sections differ' (Remark 3.2) is backed by the lab output (presentation_identity, cfo totals); L06 'pattern F only' (R1) is backed by Prop 2.4 stated for pattern F. 'raises' hit in L04 is Remark 1.2 ('each standard-specific question it raises as open'), a plain verb, not a causal claim. The L06 'raises' hit was not read in this scan and is not relied on. No scope claim in the changed sentences lacks a computation.",
)
add(
    "AC1b-L06-prose-S-constant",
    "2.2-numbers",
    "course/modules/AC/AC1/L06.html Remark 2.5 second sentence (line 120); Def 1.4 (line 73)",
    "PASS",
    "Pattern S is constant in years 1 to n-1 (13,034,272) and the last year takes the rounding remainder (13,034,273), as the printed expense_straight_line column shows. Def 1.4 gives E^S_t = floor(sum Y / n) in years 1 to n-1 with the remainder last; matches the twin's straight_line().",
)
add(
    "AC1b-L06-lab-docstring",
    "2.5-lab",
    "tests/labs/AC1/lab-AC1-L06-1.py docstring lines 1-20 (line 18: only floating-point step)",
    "PASS",
    "Docstring: 'The only floating-point step is the present value, which is rounded once to whole cents. Every later step is integer arithmetic.' Code: present_value_cents uses float division and round(); interest_cents, straight_line and roll_forward use integer // and * only. Claim holds (the module's round() call is the present-value step).",
)
add(
    "AC1b-L04-prose-misc2",
    "2.2-numbers",
    "course/modules/AC/AC1/L04.html misconception 2 (line 345)",
    "PASS",
    "Re-read for this round (the subject text changed; the numbers were re-derived in AC1b-num-L04-prose). 'Corollary 2.3 shows ... the balance expires to zero'; '1,658,095 first share'; '4,974,286 unexpired'; purchases in quarters 1, 3, 4 fully expired by quarter 7 (quarter 4's fourth share falls in quarter 7, inclusive); quarters 2, 5, 6 have prepaid_paid 0. All match.",
)
add(
    "AC1b-L04-interp-lab-claims",
    "2.2-numbers",
    "course/modules/AC/AC1/L04.html interpretation (line 296) and section 5 bullets (lines 329-332)",
    "PASS",
    "Interpretation: 'Every identity prints True' (true: 8 identity lines True in out_L04.txt); 'rule A lower in the quarters where that balance rises' (q1, q3, q4, q7 rise; rule A lower there: verified). Section 5 bullet 2: prepaid_balance_b is zero at quarter 0 and non-zero in quarters 1 to 7 (printed column). Misconception 3 quantities (3,319,293 cents change in the operating figure) match the printed CFO totals. No overreach found.",
)
add(
    "AC1b-L06-residual-causal",
    "2.9-structure",
    "course/modules/AC/AC1/L06.html misconception 3",
    "PASS",
    "'The lab does not separate the two roundings, so it does not attribute the one cent to either' is true of the twin: the code has one floating-point round() and the integer half-up interest; no separate printout of either rounding exists. The residual is 1 cent (final_payment_adjustment_cents 1).",
)
add(
    "AC1b-card-c059",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c059 (back); L04 misconception 2 (line 345)",
    "PASS",
    "Card: 'No. Over the full life of a payment the two rules recognize the same total, so a difference that reverses later is not a difference in total profit (Corollary 2.3).' Matches misconception 2 text (line 345) and the shares logic of the twin.",
)
add(
    "AC1b-cards-L04-L06",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c046 to c060, c122 (L04), c061 to c074 (L05), c075 to c090 (L06), c132 to c134 (L04); lesson text",
    "FAIL",
    "Every slice-b card read and checked against the current lesson text. Card AC1-c060 now cites Proposition 3.1 for the operating/financing move (matches L04 line 349 and Prop 3.1; the previous FAIL is fixed). Card AC1-c053 ('Both hold exactly in integer cents (Proposition 2.2)') omits the assumptions that the current Proposition 2.2 states explicitly (zero opening balances, no equity contributions, no distributions, one-quarter collection lag); without them the identity is false (opening cash C_0 would be missing from N^A). Card AC1-c066 ('Each allocation is a non-negative integer ... (Proposition 1.4)') omits the hypothesis that the transaction price P is a non-negative integer, which the current Proposition 1.4 states. The remaining cards match their lessons (checked numbers: 3,319,293; 24,513,189; 27,832,482; -4,974,286; 6,632,381; 20,583,168; 32,792,272; 23,333,398; 1,785,952; 1,977,098; 13,034,273; 61,708,083; 63,494,035).",
    "Add the Proposition 2.2 assumptions to card AC1-c053 and the non-negative price hypothesis to card AC1-c066 (see AC1b18-L04-keyresult-prop22 and AC1b18-L05-keyresult-prop14), then re-run tools/check_pages.py --unit AC1 and the card-scan.",
)
add(
    "AC1b-cards-dup",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json (139 cards)",
    "PASS",
    "Scripted scan (static_r18.py): 139 cards; no duplicate id; no duplicate front text; the 49 cards of L04, L05 and L06 are all present. Card 'front' texts of slice b are unique across the unit.",
)
add(
    "AC1b-struct-L04-L06",
    "2.9-structure",
    "course/modules/AC/AC1/L04.html, L05.html, L06.html section order",
    "PASS",
    "Scripted scan: sections in order s1..s10 (L04), s1..s9 (L05 and L06); each has the expected template sections (definitions, propositions with proofs, remarks, lab, misconceptions, problem set, key results, quiz, references). The new section-5 and misconception text sits in the template slots.",
)
add(
    "AC1b-dag-concepts",
    "2.8-dag",
    "tools/check_dag.py --unit AC1; L04.html:58 (def-gaap-vs-ifrs), L05.html:58 (def-revenue-recognition), L06.html:58 (def-lease-accounting)",
    "PASS",
    "check_dag AC1: PASS. Each of the three dfn ids appears once in its module (static_r18.py 'defs' output: def-gaap-vs-ifrs, def-revenue-recognition, def-lease-accounting); grep for data-concept=\"lease-accounting\" over course/modules/AC finds only L06.html. Prerequisites for these pages are the AC1 and S0/S2 closure, checked by check_dag.",
)
add(
    "AC1b-hours",
    "2.9-structure",
    "course/modules/AC/AC1/L04.html, L05.html, L06.html data-hours; course/modules/AC/AC1/index.html lines 153-155",
    "PASS",
    CARRY + "index.html lines 153-155 read this round: 'L04 · 11 h', 'L05 · 12 h', 'L06 · 12 h'; data-hours 11, 12, 12 match. Declared hours are design targets (architect ruling), not checked against pace.",
)
add(
    "AC1b-data-simulated",
    "2.9-structure",
    "course/modules/AC/AC1/L04.html lines 52, 130, 324; L05.html lines 52, 128, 340; L06.html lines 52, 125, 303",
    "PASS",
    "Each lesson labels its lab data SIMULATED (counts: L04 8, L05 9, L06 8 occurrences). Lab docstrings state SIMULATED and no company or customer is represented. No real company or filing data appears; 'Honest pending' blocks state the deferral.",
)
add(
    "AC1b-quiz-keys-cross",
    "2.9-structure",
    "course/modules/AC/AC1/L04.html quiz (lines 486-556), L05.html quiz (503-562), L06.html quiz (466-526)",
    "PASS",
    "Each quiz key re-checked against its problem or proposition: L04 numeric -90000 (M1), 205000 (M2), 30000 (unexpired balance at q3 = 120000 - 90000); L05 62000 (M2), -13200 (M3), 20583168 (P3); L06 2487, 8289, -776, 10001, 1785952 (computed). Multiple-choice keys correct (L04 q1, q3, q5, q6, q8, q9; L05 q1, q5, q6, q7, q9; L06 q1, q6, q7, q8).",
)
add(
    "AC1b-L04-quiz",
    "2.9-structure",
    "course/modules/AC/AC1/L04.html quiz items L04q1 to L04q9 (lines 486-556)",
    "PASS",
    "Nine items; keys and explanations re-derived (see AC1b-quiz-keys-cross). The L04q8 explanation ('A positive unexpired balance makes the difference negative') matches Cor 2.3 and E2.",
)
add(
    "AC1b-L05-quiz",
    "2.9-structure",
    "course/modules/AC/AC1/L05.html quiz items L05q1 to L05q9 (lines 503-562)",
    "PASS",
    "Nine items; keys re-derived. L05q1 correct option 16,667 / 33,333 / 50,000 matches the allocate() output; L05q7 'Revenue moves between obligations' matches Remark 1.5.",
)
add(
    "AC1b-L06-quiz",
    "2.9-structure",
    "course/modules/AC/AC1/L06.html quiz items L06q1 to L06q8 and numeric items (lines 466-526)",
    "PASS",
    "Eight multiple-choice and numeric items; keys re-derived (2487, 8289, -776, 10001, 1785952). The L06q6 correct option is the Prop 2.3 reason; its explanation (sum of recursion; A_0 = L_0) matches the proof.",
)
add(
    "AC1b-scope-words",
    "2.7-prose",
    "course/modules/AC/AC1/L04.html, L05.html, L06.html changed sentences: L04 lines 63, 97, 296, 330, 341, 345, 349; L05 lines 52, 72, 96; L06 line 58",
    "PASS",
    "Each changed sentence was read against its computation: 'each of the two rules it compares' (L04 63) holds for the two lab rules; 'Under the assumptions of Definition 2.2 ...' (L04 97) matches the proof's assumptions; 'Each quarter's net-income difference is minus the change in the printed prepaid_balance_b' (L04 296) verified for all eight quarters; 'Net income and cash are unchanged under a classification difference' (L04 349) matches Remark 3.2; 'with the transaction price P a non-negative integer' (L05 72) matches the proof's floors; 'annual contractual payments of P cents each' (L06 58) matches the twin. No changed sentence asserts more than its computation supports, except the two key-results/card omissions recorded in AC1b18-L04-keyresult-prop22 and AC1b18-L05-keyresult-prop14.",
)
add(
    "AC1b-L04-P2",
    "2.4-math",
    "course/modules/AC/AC1/L04.html problem P2 (lines 399-404)",
    "PASS",
    "N^A_t = N^B_t iff P_t = 0 (Cor 2.3). Example Q_1 = 40,000, horizon 4: four shares of 10,000 expensed by quarter 4, unexpired 0. Positive purchase Q_t: Q_t - floor(Q_t/4) >= 1, so P_t >= 1. Re-derived; unchanged text.",
)
add(
    "AC1b-L05-remark24-bullet",
    "2.2-numbers",
    "course/modules/AC/AC1/L05.html section 4 bullet 3 (lines 345-348); Remark 2.4 (line 121)",
    "PASS",
    "Bullet 3: 'Lab 1 shows both a liability and an asset under two billing schedules ... peak ... liability of 32,792,272 cents at 40 percent upfront billing, and its largest asset is 23,333,398 cents at 0 percent' matches the printed lines. Remark 2.4: zero at the end under Prop 2.3, may be large in between: consistent.",
)
add(
    "AC1b-card-c069",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c069; L05 paragraph after Section 2 (line 124)",
    "PASS",
    "Card: 'The convention-1 revenue from the over-time obligations through month m (the paragraph before Lab 1 in Section 2; problem P3)'. Matches line 124 and P3 solution.",
)
add(
    "AC1b-card-c050",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c050; L04 Section 2 paragraph (line 78)",
    "PASS",
    CARRY + "AC1-c050 is unchanged in the fefbf8b..7143726 cards diff (only c060 changed). Lesson line 78 still labels rule A as the lab's convention and not a framework rule.",
)
add(
    "AC1b3-L05-top-line",
    "2.9-structure",
    "course/modules/AC/AC1/L05.html line 52 (why-it-matters); course/modules/AC/AC1/L02.html income statement definition",
    "PASS",
    "Line 52 changed this round ('each obligation's timing convention sets when its revenue enters net income'). L02 lists revenue first for the income statement ('revenue, the costs that match it, and net income'), so 'the first item that L02 lists' holds. The new clause states the per-obligation convention, consistent with Definition 1.1 and the lab.",
)
add(
    "AC1b3-equal-shares",
    "2.5-lab",
    "tests/labs/AC1/lab-AC1-L05-1.py lines 17-18 (docstring), 106 (billing_schedule docstring)",
    "PASS",
    "Docstring 'as equal as whole cents allow' for the instalments; billing_schedule allocates the remainder over 12 equal weights via allocate(); over_time_schedule docstring gives equal shares with the last taking the remainder. Matches the code (read this round).",
)
add(
    "AC1b3-card-c062",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c062; L05 Definition 1.2 (line 63)",
    "PASS",
    "Card: point obligation delivered in one month, over-time delivered over twelve months (Definition 1.2). Matches the definition text.",
)
add(
    "AC1b3-card-c088",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c088; L06 misconception 1; Proposition 2.3",
    "PASS",
    "Card: year-1 pattern F 14,820,224 vs payment 13,034,272; 'Only the sums over the term are guaranteed equal (Proposition 2.3)'. Matches misconception 1 and Prop 2.3; the 'only' claim is what Prop 2.3 guarantees, no year-by-year equality is stated.",
)
add(
    "AC1b4-L06-prop21-hypothesis",
    "2.4-math",
    "course/modules/AC/AC1/L06.html Proposition 2.1 statement (line 80) and Definition 1.2",
    "PASS",
    "Hypotheses (rho, P, L_0 integers; L_0 the present value rounded once) match the twin (round(pv); payment_cents; rate_bps). Conclusion L_n = 0 and integer final adjustment verified in the printed output.",
)
add(
    "AC1b4-L06-R1-pattern-scope",
    "2.4-math",
    "course/modules/AC/AC1/L06.html R1 solution (line 425)",
    "PASS",
    "'Proposition 2.4 is proved for pattern F only'; 'at a discount rate of 0 bps the two patterns coincide in every year' verified: rate 0 gives L_0 = nP, interest 0, amortization P, pattern F = P = pattern S. Scope words checked.",
)
add(
    "AC1b4-L05-R1-scope",
    "2.7-prose",
    "course/modules/AC/AC1/L05.html problem R1 solution",
    "PASS",
    "R1 solution: 'If the two agree exactly, the test supports the convention for that contract. If they differ, the difference is evidence against the convention for that contract. The rules for identifying obligations are not stated on this page'. Matches the page's Section 3 and cites no source.",
)
add(
    "AC1b4-L05-section-ref",
    "2.7-prose",
    "course/modules/AC/AC1/L05.html Definition 1.1 (lines 57-58) and section 4 bullet 4",
    "PASS",
    "Definition 1.1: 'Those criteria are the open question of Section 3'; Section 3 is 'What the convention cannot settle' and names the four inputs. Section 4 bullet 4 cross-refers to Section 3. Correct.",
)
add(
    "AC1b4-L06-section-ref",
    "2.7-prose",
    "course/modules/AC/AC1/L06.html problem R1 solution (line 425) and section 4 bullet 4",
    "PASS",
    "R1: 'Section 4 says the identity does not cover them' matches section 4 bullet 4 ('outside the scope of Propositions 2.1 to 2.4 as stated'). Definition 1.1 cross-refers to Section 3, which is 'What the model cannot settle'. Correct.",
)
add(
    "AC1b4-L04-why-scope",
    "2.7-prose",
    "course/modules/AC/AC1/L04.html lines 52 and 322",
    "PASS",
    "'The lesson does not state what US GAAP or IFRS Standards require, because this lesson cites neither primary text' (line 52) and 'The first two are open because this lesson cites no primary text for them' (Section 4) match Remark 1.2 and the empty references list.",
)
add(
    "AC1b4-L04-corollary-sentence",
    "2.4-math",
    "course/modules/AC/AC1/L04.html section 5 bullet 1 (line 329)",
    "PASS",
    "'Corollary 2.3 says that the two differ by the unexpired balance, and says nothing about which one reports the economics better' matches Cor 2.3 (N^A - N^B = -P) and the lesson's 'no ranking' statement.",
)
add(
    "AC1b4-L05-misc1-peak",
    "2.2-numbers",
    "course/modules/AC/AC1/L05.html misconception 1 (lines 355-357 range)",
    "PASS",
    "'Lab 1 the contract billed 40 percent at signing, so its balance was a contract liability of up to 32,792,272 cents'; '0 percent ... contract asset in 8 months'; '32,792,272 ... so that does not hold here'. Matches the printed lab lines.",
)
add(
    "AC1b4-L05-interp-remainders",
    "2.2-numbers",
    "course/modules/AC/AC1/L05.html interpretation (line 333)",
    "PASS",
    "Re-derived in chk_l05_r18.py: floor 5434051/12 = 452837, remainder 452844; floor 35732298/12 = 2977691, remainder 2977697; sum of six monthly shares 2,717,022 + 17,866,146 = 20,583,168. The interpretation's arithmetic and the 'remainder' descriptions are correct.",
)
add(
    "AC1b4-L06-E3-crossing",
    "2.2-numbers",
    "course/modules/AC/AC1/L06.html E3 solution (lines 413-414) and Remark 2.5",
    "PASS",
    "First year F below S is year 5; difference 12,467,522 - 13,034,272 = -566,750 (recomputed). Consistent with Remark 2.5 'In Lab 1 pattern F is above pattern S in years 1 to 4 and below it in years 5 to 7'.",
)
add(
    "AC1b4-L06-misc3-residual",
    "2.9-structure",
    "course/modules/AC/AC1/L06.html misconception 3 (lines 326-330 range)",
    "PASS",
    "Re-read this round. The one-cent residual is the accumulated integer rounding; the lab prints the adjustment (final_payment_adjustment_cents 1). Statement consistent with Def 1.3 and the twin.",
)
add(
    "AC1b4-card-c081",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c081; L06 Definition 1.4 (line 73)",
    "PASS",
    "Card: pattern S 'each of the first n-1 years takes the floor of the total payments divided by n, and the last year takes the remainder'; matches Def 1.4 and the twin's straight_line().",
)
add(
    "AC1b4-card-c090",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c090; L06 misconception 3",
    "PASS",
    "Card: final payment 13,034,273 against 13,034,272; the one cent 'comes from rounding the present value once and each year's interest half up'. Matches misconception 3 and out_L06.txt.",
)
add(
    "AC1b4-L05-lab-billing-code",
    "2.5-lab",
    "tests/labs/AC1/lab-AC1-L05-1.py billing_schedule (lines 105-108), allocate (67-81), over_time_schedule",
    "PASS",
    "Read the code. allocate() uses floors, remainders and largest-remainder ties to lower index; billing_schedule() uses upfront = price*percent//100 and allocate(price - upfront, [1]*12); the balance is cumulative billing minus cumulative revenue (main()). Matches the page text.",
)
add(
    "AC1b4-L06-lab-straight-line",
    "2.5-lab",
    "tests/labs/AC1/lab-AC1-L06-1.py straight_line (lines 60-63); L06 Definition 1.4 (line 73)",
    "PASS",
    "straight_line(total, years): base = total // years for the first years-1 shares, remainder last. Matches Def 1.4 and the printed expense_straight_line column.",
)
add(
    "AC1b6-L05-docstring-convention2",
    "2.5-lab",
    "tests/labs/AC1/lab-AC1-L05-1.py module docstring lines 12-15 (convention 2 sentence); revenue_schedule()",
    "PASS",
    "'Convention 2 recognizes every over-time obligation in month 12 instead ... changes only the month in which each over-time amount is recognized' matches revenue_schedule(over_time_as_end=True) and the printed totals_equal_under_both_conventions True.",
)
add(
    "AC1b6-L05-hypothesis-billing",
    "2.5-lab",
    "course/modules/AC/AC1/L05.html hypothesis (line 128); twin UPFRONT_PERCENT (line 29) and the 40/0 loop in main()",
    "PASS",
    "Hypothesis 'the lab runs two billing scenarios: 40 percent billed at signing ... and 0 percent billed at signing' matches UPFRONT_PERCENT = 40 and the loop over (UPFRONT_PERCENT, 0).",
)
add(
    "AC1b6-L06-why-it-matters",
    "2.9-structure",
    "course/modules/AC/AC1/L06.html line 52 (why-it-matters)",
    "PASS",
    "'Lab 1 runs one SIMULATED lease, a seven-year lease at 6.30 percent' matches term_years 7 and rate_bps 630 in the printed header line. 'proves that the asset less the liability moves with cash paid less pattern F expense in every year' matches Prop 2.4.",
)
add(
    "AC1b6-L06-remark25-numbers",
    "2.2-numbers",
    "course/modules/AC/AC1/L06.html Remark 2.5 (line 120); L06 pre.expected block",
    "PASS",
    "All Remark 2.5 figures re-checked against out_L06.txt (see AC1b-num-L06-prose).",
)
add(
    "AC1b4-L06-remark25-causal",
    "2.6-causal",
    "course/modules/AC/AC1/L06.html Remark 2.5 (line 120)",
    "PASS",
    "'Interest is charged on the opening liability. In Lab 1 the opening liability falls in every year, because each payment exceeds the interest charged that year' — verified: payment 13,034,272 exceeds every year's interest (4,535,544 max). The direction (falling balance, falling interest) matches the printed opening_liability and interest columns.",
)
add(
    "AC1b6-locators-L05",
    "2.9-structure",
    "course/modules/AC/AC1/L05.html (current locators: lines 52, 68, 72, 96, 124, 128, 333) and tests/labs/AC1/lab-AC1-L05-1.py",
    "PASS",
    "Locators re-read in this round match the current file (grep line numbers: 52 why-it-matters, 68 Def 1.3, 72 Prop 1.4, 96 Prop 2.1, 124 paragraph, 128 hypothesis, 333 interpretation, 488 key-results row 1). The changed line 96 (Prop 2.1) and line 72 (Prop 1.4) are cited at their current numbers.",
)
add(
    "AC1b-L05-quiz-extra",
    "2.9-structure",
    "course/modules/AC/AC1/L05.html quiz L05q6 and L05q7 (lines 531-548 range)",
    "PASS",
    "L05q6 correct option 'billing totals the price and convention-1 revenue totals the price (Proposition 2.3)' and L05q7 correct option (Remark 1.5) re-checked against the propositions.",
)
add(
    "AC1b7-L04-remark12",
    "2.7-prose",
    "course/modules/AC/AC1/L04.html Remark 1.2 (line 63)",
    "PASS",
    "Changed this round: 'proves identities that hold under each of the two rules it compares'. The identities in §2 do hold under each of the two lab rules (Prop 2.2 under rule A and rule B), and the Remark still says the lesson states no framework rule.",
)
add(
    "AC1b7-L04-sec2-convention",
    "2.7-prose",
    "course/modules/AC/AC1/L04.html Section 2 paragraph (line 78)",
    "PASS",
    "Unchanged text: rule A and rule B described as the lab's conventions; rule B four shares, first three floor(payment/4), last the remainder; matches expense_rule_b() and shares() in the twin.",
)
add(
    "AC1b7-L04-sec4",
    "2.7-prose",
    "course/modules/AC/AC1/L04.html Section 4 paragraph (line 322) and honest-pending block (line 324)",
    "PASS",
    "'No real company appears in this lesson. Every ledger is generated from a seed and labelled SIMULATED.' Matches the twin's docstring and the output (SIMULATED label in 8 places).",
)
add(
    "AC1b7-L05-def13",
    "2.7-prose",
    "course/modules/AC/AC1/L05.html Definition 1.3 (line 68)",
    "PASS",
    "Unchanged in this delta. Positive integer stand-alone prices, integer P in cents, floor-plus-largest-remainder allocation: matches allocate() in the twin. Re-derived with the Prop 1.4 hypothesis (see AC1b-math-L05): the definition does not need P >= 0 for the sum identity.",
)
add(
    "AC1b7-L06-sec3",
    "2.7-prose",
    "course/modules/AC/AC1/L06.html Section 3 paragraph (line 301)",
    "PASS",
    "Unchanged: four decisions (payments fixed, discount rate, initial asset, expense pattern) named and each stated as open. Matches Section 4 bullet 4 and R2.",
)
add(
    "AC1b7-L06-R2",
    "2.7-prose",
    "course/modules/AC/AC1/L06.html R2 solution (line 432 range)",
    "PASS",
    "Four decisions named with the question and evidence type; 'None of these four questions is answered by Propositions 2.1 to 2.4' matches the propositions' scope (any schedule following Defs 1.3 and 1.4).",
)
add(
    "AC1b7-process-words",
    "2.9-structure",
    "course/modules/AC/AC1/L04.html, L05.html, L06.html (learner text); scripted word scan",
    "PASS",
    "Word scan for builder, verifier, unit report, REQUEST: 0 hits. 'round' with word boundaries: 0 hits in learner text (the only 'round' token in L06 is the Python round() call in the twin's code, not prose). 'rounds' and 'rounded' occur in mathematical and rounding prose only.",
)
add(
    "AC1b8-L04-remark32-attribution",
    "2.7-prose",
    "course/modules/AC/AC1/L04.html misconception 3 (line 349); Remark 3.2 (line 315); Prop 3.1 (line 305); card AC1-c060",
    "PASS",
    "Fixed since round 17. Line 349 now cites Remark 3.2 only for 'net income and cash are unchanged under a classification difference' (Remark 3.2 says net income, the cash balance and the change in cash are the same under both presentations) and cites Proposition 3.1 for 'operating cash flow and financing cash flow change by the same amount in opposite directions' (Prop 3.1: CFO_2 = CFO_1 + I, CFF_2 = CFF_1 - I). Card AC1-c060 cites Proposition 3.1. Lab output: cfo totals 24,513,189 and 27,832,482, difference 3,319,293 = interest total.",
)
add(
    "AC1b8-cards-new-L04",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json AC1-c132, AC1-c133, AC1-c134",
    "PASS",
    "c132: -4,974,286 = minus the unexpired part of the quarter-7 purchase of 6,632,381 (first share expensed; 6632381 - 1658095 = 4974286). c133: rule B description matches Section 2. c134: presentation 2 places interest in financing. All unchanged in this delta and consistent with the current text.",
)
add(
    "AC1b8-L04-numbers-recomputed",
    "2.2-numbers",
    "course/modules/AC/AC1/L04.html Section 3 paragraph (line 318), interpretation (line 296), section 5 bullet 2 (line 330), misconception 2 (line 345), card AC1-c056",
    "PASS",
    "3319293/27832482 = 0.1192597 (0.1193 at 4 dp; 0.11926 at 5 dp). Rule-A vs rule-B signs match the prepaid balance rising (q1, q3, q4, q7) and falling (q2, q5, q6). Unexpired at q7 4,974,286 only from the q7 purchase. Card AC1-c056 values 3,319,293, 24,513,189, 27,832,482 match out_L04.txt.",
)
add(
    "AC1b8-twins-match-pages",
    "2.5-lab",
    "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py; pre.expected blocks of L04, L05, L06",
    "PASS",
    "Re-run this round: outputs equal the pre.expected blocks line by line (20, 22, 19 lines).",
)
add(
    "AC1b8-mutants-AC1-rerun",
    "2.5-lab",
    "ledgers/AC1/mutants/ (160 files); tools/mutate_graders.py --unit AC1 --seeds 0-4",
    "PASS",
    "Re-run this round: 'mutate_graders AC1: PASS (160/160 killed)' (out/mutate.txt). These are the project-grader mutants, not slice-b mutants; slice b is pages and twins, so no new slice-b mutant is required. The round-18 grader change (test_project.py, project slice) is covered by this run.",
)
add(
    "AC1b8-cards-change-scan",
    "2.7-cards",
    "course/modules/AC/AC1/cards.json: git diff fefbf8b 7143726 -- cards.json",
    "PASS",
    "Diff: one changed line (AC1-c060 back). The other slice-b cards are byte-identical since fefbf8b and were re-read against the current text (AC1b-cards-L04-L06).",
)

# ---- new FAIL rows (round 18)
add(
    "AC1b18-L04-keyresult-prop22",
    "2.7-prose",
    "course/modules/AC/AC1/L04.html key-results row 473 (Proposition 2.2 summary); section 2 Proposition 2.2 statement (line 97)",
    "FAIL",
    "Current Proposition 2.2 (line 97) reads 'Under the assumptions of Definition 2.2 (zero opening balances, no equity contributions, no distributions, and each credit sale collected one quarter later) ...'. The key-results row 473 states the same identities ('Cash plus receivables, plus the unexpired prepaid balance under rule B, equals cumulative net income under each rule (Proposition 2.2)') with no assumption. Opening cash C_0 would be missing from N^A and N^B, so the unconditional summary is over-general; the lesson's own statement and proof require the assumptions.",
    "Add '(under the assumptions of Definition 2.2: zero opening balances, no equity contributions, no distributions, one-quarter collection lag)' to key-results row 473 in course/modules/AC/AC1/L04.html, and the same qualifier to card AC1-c053; re-run tools/check_pages.py --unit AC1.",
)
add(
    "AC1b18-L05-keyresult-prop14",
    "2.7-prose",
    "course/modules/AC/AC1/L05.html key-results row 488 (Proposition 1.4 summary); Proposition 1.4 statement (line 72); card AC1-c066",
    "FAIL",
    "Current Proposition 1.4 (line 72) reads 'Under Definition 1.3, with the transaction price P a non-negative integer, a_i is a non-negative integer for every i, and sum a_i = P'. The key-results row 488 says 'The allocation of Definition 1.3 is a non-negative integer split that sums exactly to the price (Proposition 1.4)' and card AC1-c066 says 'Yes. Each allocation is a non-negative integer ...' with no price hypothesis. For P < 0 the floors are negative (checked: P = -1, weights (1,1) gives a = [0,-1]), so the non-negativity claim fails without the hypothesis the current Proposition 1.4 states.",
    "Add 'for a non-negative transaction price' to key-results row 488 in course/modules/AC/AC1/L05.html and to card AC1-c066 (the front may stay as asked); re-run tools/check_pages.py --unit AC1.",
)

fragment = {
    "unit": "AC1",
    "slice": "AC1-b",
    "round": 18,
    "round_note": "round 18 (independent re-verification after the round-17 fixes at 7143726). Delta since the previous pin fefbf8b: L04.html (35 lines: meta description, Remark 1.2, Prop 2.2 statement, lab print line and expected block, interpretation, section 5 bullet 2, misconceptions 1-3, key-results row 1 wording), L05.html (6 lines: why-it-matters, Prop 1.4, Prop 2.1), L06.html (2 lines: Def 1.1), cards.json (card AC1-c060 back), lab-AC1-L04-1.py (print line). Every changed hunk was read and re-derived; every prior non-PASS row was re-verified.",
    "verifier": "Haiku independent verifier for slice AC1-b, round 18; did not build AC1 and shares no context with its builders",
    "pin": "7143726",
    "base": "fefbf8b (previous pin of slice b; /tmp/fanout-frags/AC1-b.round17.json is context only, its PASS rows were not trusted)",
    "checkout": "/tmp/verify18-AC1-b (detached at 7143726; .venv symlink)",
    "scratch": "/tmp/AC1-v/AC1-b-r18",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is pages and twins, not a project slice: no new student-error mutant and no alternative correct implementation is required for this slice. The 160 project-grader mutants were re-run (AC1b8-mutants-AC1-rerun) and all were killed.",
        "Carried rows (prefix 'Carried from round 17') cite only subjects not changed by the delta; the only carried text is the hours row (index.html and data-hours unchanged) and card AC1-c050 (unchanged).",
        "Lab output is SIMULATED (seeds 2604, 2605, 2606); results read off a lab are grade C naming the lab.",
        "Not checked: live reachability of any publisher or SEC source (no slice-b row cites one); pytest summary line and collect-only count (not printed by the configuration); hours on pace (architect ruling); the timing of the page_smoke run beyond the reported seconds.",
        "Scope judgement recorded: Prop 2.1 (L05) is correctly stated under Definition 1.3 for any integer P because its proof uses Prop 1.4 only for the sum identity, which holds for any integer P; the non-negativity hypothesis is needed only for Prop 1.4's non-negativity claim. Recorded as PASS (AC1b-math-L05).",
    ],
    "summary": "",
}
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = (
    f"AC1-b round 18 (L04, L05, L06 and twins; pin 7143726): {len(rows)} rows, {counts['PASS']} PASS, "
    f"{counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Verdict FAIL."
)
out = CHECKOUT / "ledgers/AC1/AC1-b.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
problems = ledger.validate(json.loads(out.read_text(encoding="utf-8")), "AC1-b")
print("rows", len(rows), counts)
print("validate", problems)
