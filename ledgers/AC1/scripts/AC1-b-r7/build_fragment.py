"""Writes ledgers/AC1/AC1-b.json (round 7, slice AC1-b: L04, L05, L06 and their twins) from the rows verified in round 7."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
S = "scripts/AC1-b-r7/"
R = []


def row(id_, check, location, evidence, status="PASS"):
    R.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})


row("AC1b-cmd-pin", "2.9-structure",
    "repository; course/modules/AC/AC1/L04.html, L05.html, L06.html; tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py; course/modules/AC/AC1/cards.json",
    "git rev-parse HEAD = de53f7e883dc4d6f6dacd6042d13acd197afba5d (checkout /tmp/verify7-AC1-b, detached). git diff --stat d57df1e de53f7e for the slice: L04.html 8 lines, L05.html 8 lines, L06.html 10 lines, cards.json 2 lines (only AC1-c102, an L07 card). The three twins are not in the diff; the tests/labs/AC1 diff touches only lab-AC1-L07-1.py.")
row("AC1b-cmd-run_labs", "2.5-lab", "tools/run_labs.py --unit AC1 --page L04 / L05 / L06",
    "Re-run: each page printed 'run_labs AC1: PASS (1/1)', exit 0 (/tmp/AC1-v/AC1-b-r7/run_labs_L04.out, _L05.out, _L06.out).")
row("AC1b-cmd-twins", "2.5-lab", "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py",
    "python -I -W error on each twin: exit 0; outputs 20, 22 and 19 lines (/tmp/AC1-v/AC1-b-r7/lab-AC1-L0{4,5,6}-1.out). Seeds 2604, 2605, 2606 in the printed headers.")
row("AC1b-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit AC1",
    "Re-run: 'check_pages AC1: PASS', exit 0 (/tmp/AC1-v/AC1-b-r7/check_pages.out).")
row("AC1b-cmd-check_dag", "2.9-structure", "tools/check_dag.py --unit AC1",
    "Re-run: 'check_dag AC1: PASS', exit 0 (/tmp/AC1-v/AC1-b-r7/check_dag.out).")
row("AC1b-cmd-check_projects", "2.6-projects", "tools/check_projects.py --unit AC1",
    "Re-run: 'check_projects AC1: PASS', exit 0 (/tmp/AC1-v/AC1-b-r7/check_projects.out).")
row("AC1b-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit AC1 --pages L04 L05 L06",
    "Re-run: each page PASS (runtime boot 1.1 s with numpy; lab 0.0 s), 'page_smoke AC1: PASS', exit 0 (/tmp/AC1-v/AC1-b-r7/smoke.out).")
row("AC1b-cmd-lint-mypy", "2.5-lab", "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py",
    "Re-run: ruff check tests/labs/AC1 'All checks passed!'; ruff format --check 'already formatted' (11 files); mypy --no-incremental on the three twins 'Success: no issues found in 3 source files'.")
row("AC1b-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --unit AC1; tools/verify_refs.py --offline",
    "Re-run: live 'live re-verification of AC1: 2 of 560 entries, 0 problems'; offline 'offline integrity: 560 entries, 0 problems'. No slice row cites a registry key (see AC1b-cit-none).")
row("AC1b-cmd-pytest", "2.5-lab", "pytest -q -k 'AC1 or lab'",
    "Re-run: exit 0; progress lines all dots (72 + 71 per line, 100 percent), /tmp/AC1-v/AC1-b-r7/pytest.out.")
row("AC1b-cit-none", "2.1-citations", "course/modules/AC/AC1/L04.html:560-561, L05.html:568-569, L06.html:532-533 (References sections)",
    "Grep for data-ref, ref-key, data-cite, references.json in the three pages: the only match is the empty <ol data-references></ol> at L04:561, L05:569, L06:533. The References sentences say no source is cited (L04:560, L05:568, L06:532).")
row("AC1b-num-L04-lab", "2.2-numbers", "course/modules/AC/AC1/L04.html pre.expected (lines 275-294); tests/labs/AC1/lab-AC1-L04-1.py",
    "ledgers/AC1/scripts/AC1-b-r7/embed_compare.py: L04 code block identical to the twin (True); pre.expected identical to the run output (True), 20 lines.")
row("AC1b-num-L04-prose", "2.2-numbers", "course/modules/AC/AC1/L04.html line 295 (interpretation), line 317 (Section 3 paragraph), line 344 (misconception 2), lines 328-331 (section 5), lines 364-396",
    "ledgers/AC1/scripts/AC1-b-r7/recheck_r7.py (own generator, seed 2604): prepaid_balance_b 0, 3664530, 2443020, 4396595, 6860942, 4221175, 1581406, 4974286; purchases only in quarters 1, 3, 4, 7 (4886040, 4233446, 6325624, 6632381). Per-quarter NI difference rule A minus rule B: 0, -3664530, 1221510, -1953575, -2464347, 2639767, 2639769, -3392880, so rule A is lower in quarters 1, 3, 4, 7 and higher in 2, 5, 6, equal in 0 (matches line 295). (NI_A - NI_B) = -(change in prepaid_balance_b) in every quarter: True. Cumulative -4974286. 3319293/27832482 = 0.1192597 -> 0.1193 (line 317). 3319293/24513189 = 0.1354085 -> 0.1354 (E3, line 434).")
row("AC1b-num-L05-lab", "2.2-numbers", "course/modules/AC/AC1/L05.html pre.expected (lines 311-332); tests/labs/AC1/lab-AC1-L05-1.py",
    "embed_compare.py: L05 code identical to the twin (True); pre.expected identical to the run output (True), 22 lines.")
row("AC1b-num-L05-prose", "2.2-numbers", "course/modules/AC/AC1/L05.html line 333 (interpretation), lines 357 (misconception 1), 426 (P3 solution), 345-347 (section 4 bullets), 437, 444, 451 (E1-E3)",
    "recheck_r7.py: shares 5434051, 9440568, 29888194, 35732298 over 80495111 = 0.0675, 0.1173, 0.3713, 0.4439 (sum 1.0000). 50471362/80495111 = 0.6270115 (0.6270). 32792272/80495111 = 0.4073822 (0.4074). 23333398/80495111 = 0.2898735 (0.2899). floor(5434051/12) = 452837 with month-12 remainder 452844; floor(35732298/12) = 2977691 with remainder 2977697; 6 x 452837 + 6 x 2977691 = 2717022 + 17866146 = 20583168 = printed month-6 difference.")
row("AC1b-num-L06-lab", "2.2-numbers", "course/modules/AC/AC1/L06.html pre.expected (lines 277-295); tests/labs/AC1/lab-AC1-L06-1.py",
    "embed_compare.py: L06 code identical to the twin (True); pre.expected identical to the run output (True), 19 lines.")
row("AC1b-num-L06-prose", "2.2-numbers", "course/modules/AC/AC1/L06.html Definition 1.2 (62-63), Remark 2.5 (120), interpretation (296), misconceptions (320-328), M1-M4 (341-364), E1-E3 (400-414), R1 (425)",
    "recheck_r7.py (own generator, seed 2606): term 7, payment 13034272, rate 630 bps, L0 71992763 (PV 71992763.4 rounded once). Interest 4535544, 4000124, 3430973, 2825965, 2182842, 1499202, 772492; amortization 10284680 x6 and 10284683; F 14820224, 14284804, 13715653, 13110645, 12467522, 11783882, 11057175; S 13034272 x6 and 13034273; F minus S year 1 1785952, year 7 -1977098; sum F = sum payments = 91239905. E1 14820224/91239905 = 0.1624313 (0.1624). E2 0.063 x 71992763 = 4535544.069. E3 year 5 F minus S = -566750. M1 PV 24868.52 -> 24869, interest 2487, closing 17356. M2 8289 x2 and 8291. M3 closing year 2 9092, interest year 3 909, final 10001, S 10000, 10000, 10001. M4 asset 16580, liability 17356, change -776 = 10000 - 10776.")
row("AC1b-grades-L04", "2.3-grades", "course/modules/AC/AC1/L04.html lines 81, 96, 114, 303 (T) and key-results rows 471-475",
    "Props 2.1, 2.2, Cor 2.3 and 3.1 are marked T and proved on the page (proofs at 85-88, 95-111, 113-121, 307-310). Row 475 (presentation 2 exceeds presentation 1 by 3,319,293) is C and names Lab 1, SIMULATED, seed 2604.")
row("AC1b-grades-L05", "2.3-grades", "course/modules/AC/AC1/L05.html lines 72, 95, 110 (T) and key-results rows 488-492",
    "Prop 1.4, Prop 2.1 and Prop 2.3 are T with proofs (76-83, 99-102, 114-117). Row 492 (peak liability 32,792,272 and 8 contract-asset months) is C and names Lab 1 (seed 2605).")
row("AC1b-grades-L06", "2.3-grades", "course/modules/AC/AC1/L06.html lines 79, 89, 99, 109 (T) and key-results rows 451-455",
    "Props 2.1-2.4 are T with proofs (83-86, 93-96, 103-106, 113-116). Row 455 (1,785,952 and -1,977,098) is C and names Lab 1 (seed 2606).")
row("AC1b-math-L04", "2.4-math", "course/modules/AC/AC1/L04.html Prop 2.1 proof (85-88), Prop 2.2 (95-111), Cor 2.3 (113-121), Prop 3.1 proof (307-310)",
    "Re-derived: rule A and rule B change only NI and the prepaid balance, cash unchanged; Prop 2.2 identities hold per quarter (lab balance_identity True both rules; recheck_r7.py); Cor 2.3 holds with -4974286 = -P7; Prop 3.1: CFO2 = CFO1 + I, CFF2 = CFF1 - I, sum unchanged (27832482 - 24513189 = 3319293 = interest total).")
row("AC1b-math-L05", "2.4-math", "course/modules/AC/AC1/L05.html Def 1.3 (68), Prop 1.4 and proof (72-83), Remark 1.5 (87), Prop 2.1 and proof (96-102), Prop 2.3 and proof (110-117)",
    "Re-derived the remainder argument: r_i = P w_i - W f_i with 0 <= r_i < W, sum r_i = W L, so L < n and L distinct indices get one extra cent. Scaling invariance P k w_i / (k W) = P w_i / W. Prop 2.1 monthly shares sum to a_i. Prop 2.3 D12 = P - P = 0. Definition 1.3 on the M1 example: floors 16666, 33333, 50000; sum 99999; remainders 4, 2, 0; first obligation gets the cent (line 380).")
row("AC1b-math-L06", "2.4-math", "course/modules/AC/AC1/L06.html Def 1.2-1.4 (62-74), Props 2.1-2.4 and proofs (79-116), Remark 2.5 (120)",
    "Re-derived: Prop 2.4 change in (A - L) = Y_t - E^F_t for all seven years of Lab 1 (recheck_r7.py); Prop 2.3 sums; Prop 2.1 integrality; rate 0 bps check (pattern_check: F = P in every year, S = P): the R1 claim at line 425 holds.")
row("AC1b-math-notation", "2.4-math", "notation/notation.json (26 macros, 8 symbols); course/modules/AC/AC1/L04.html, L05.html, L06.html LaTeX",
    "LaTeX commands used on the three pages: cdot, dots, ge, le, lfloor, mathrm, rfloor, rho, sum. None is a registry macro (registry names \\E, \\Prob, \\Var, ... \\emgamma). \\dots appears once (L05 line 68, w_1, ..., w_n, a sequence in notation).")
row("AC1b-L04-hypothesis-lab", "2.5-lab", "course/modules/AC/AC1/L04.html hypothesis (line 130); tests/labs/AC1/lab-AC1-L04-1.py lines 110-113",
    "cash_rule_a = cumulative(cash_change)[-1] and cash_rule_b = cash_end[-1] are the same list's last element, so 'compares one expression with itself' is accurate; the hypothesis discloses that the match checks the code.")
row("AC1b-hyp-L06-few-cents", "2.5-lab", "course/modules/AC/AC1/L06.html hypothesis (line 125); tests/labs/AC1/lab-AC1-L06-1.py lines 39-45",
    "randint(4, 7) years, randint(120_000_00, 300_000_00) cents, randint(400, 800) bps: matches 4-7 years, 120,000.00-300,000.00 CU, 4.00-8.00 percent. Printed final_payment_adjustment_cents 1 matches the hypothesis text.")
row("AC1b-L05-prose-checks-m6", "2.9-structure", "course/modules/AC/AC1/L05.html paragraph after Section 2 (line 124); tests/labs/AC1/lab-AC1-L05-1.py lines 173-179",
    "Line 124 states the month-m difference equals the convention-1 over-time revenue through month m and that Lab 1 checks it at month 6. Twin lines 173-177 compute over_time_month_6; prints at 178-179. Output: month_6_difference_cents 20583168 = over_time_convention_1_month_6_cents 20583168; equality True.")
row("AC1b-L05-prose-as-much-as", "2.9-structure", "course/modules/AC/AC1/L05.html section 4 bullets (lines 345-347), line 357, line 365",
    "grep 'as much as' in L04-L06: 0 matches. Section 4 bullet 3 (line 347) gives 32,792,272 (40 percent liability) and 23,333,398 (0 percent asset); output max_contract_liability_cents 32792272 and max_contract_asset_cents 23333398.")
row("AC1b-L06-prose-S-constant", "2.9-structure", "course/modules/AC/AC1/L06.html Remark 2.5 second sentence (line 120); Definition 1.4 (73)",
    "The sentence 'Pattern S is constant in years 1 to n-1, and the last year takes the rounding remainder (13,034,273 against 13,034,272 in Lab 1)' is unchanged; recompute: S = 13034272 x 6 then 13034273 from total 91239905; lab final_payment_cents 13034273, contractual 13034272.")
row("AC1b-L06-lab-docstring", "2.5-lab", "tests/labs/AC1/lab-AC1-L06-1.py docstring lines 1-20 (line 18: only floating-point step); generate() lines 39-45; present_value_cents lines 48-52",
    "Docstring 'Seeded term (4 to 7 years), annual payment (120,000.00 to 300,000.00 CU), and rate (4.00 to 8.00 percent)' matches generate() (line 40 docstring). present_value_cents uses float and round() once; every later step is integer (interest_cents, straight_line, roll_forward).")
row("AC1b-L04-prose-misc2", "2.2-numbers", "course/modules/AC/AC1/L04.html Misconception 2 (line 344)",
    "Recomputed: 6632381 // 4 = 1658095 first share; unexpired 4974286 after it. Purchases in quarters 1 (4886040), 3 (4233446), 4 (6325624) and 7 (6632381) only; quarters 2, 5, 6 have prepaid_paid 0 (generator). Quarter 4's purchase is fully expired at quarter 7, so the list is complete.")
row("AC1b-L04-interp-lab-claims", "2.9-structure", "course/modules/AC/AC1/L04.html interpretation (line 295) and section 5 bullets (lines 328-331)",
    "Line 295: 24,513,189 cents under both rules (page pre.expected line 284), 'same expression' (twin lines 110-111), -4,974,286 (page pre.expected line 289), quarter pattern (recheck). Bullet 2 (line 329): zero at quarter 0 and non-zero at quarters 1 to 7 (balances 3664530 ... 4974286, recheck_r7.py).")
row("AC1b-L06-residual-causal", "2.2-numbers", "course/modules/AC/AC1/L06.html Misconception 3 (lines 326-330)",
    "The one-cent residual is the accumulated effect of the single PV rounding and the half-up interest rounding: with exact PV and exact interest the closing payment equals P exactly (algebra of Definition 1.3); the lab does not separate the roundings, as the text says. Lab 1 prints final_payment_adjustment_cents 1 (pre.expected line 287).")
row("AC1b-card-c059", "2.9-structure", "course/modules/AC/AC1/cards.json AC1-c059 (back); lesson L04 Misconception 2 (line 344)",
    "Back: -4,974,286 at quarter 7, purchase 6,632,381 with first share expensed, purchases in quarters 1, 3, 4 fully expired. Matches line 344 and page pre.expected line 289.")
row("AC1b-cards-L04-L06", "2.9-structure", "course/modules/AC/AC1/cards.json AC1-c046 to c060, c122 (L04), c061 to c074 (L05), c075 to c090 (L06); lesson sections",
    "All 46 L04-L06 cards read against their lesson text in round 7: each back matches the cited definition, proposition, section or lab output (c052 Prop 2.1; c050 Section 2 with the new 'conventions of this lab' wording; c069 the paragraph before Lab 1; c086 and c090 against lab output). No card number absent from its lesson.")
row("AC1b-cards-dup", "2.9-structure", "course/modules/AC/AC1/cards.json (125 cards)",
    "recheck_r7.py: 125 cards, 0 duplicate ids, 0 duplicate fronts (case-insensitive). Verified in this round with the same script.")
row("AC1b-struct-L04-L06", "2.9-structure", "course/modules/AC/AC1/L04.html, L05.html, L06.html section order",
    "Section order matches the template in each page: why-it-matters, section 1, section 2, section 3, section 4, canon breaks (section 5), misconceptions, problem set (Mechanics, Proof, Empirical, Research), key results, retrieval quiz, references, lesson nav.")
row("AC1b-dag-concepts", "2.9-structure", "tools/check_dag.py --unit AC1; L04.html:58 (def-gaap-vs-ifrs), L05.html:58 (def-revenue-recognition), L06.html:58 (def-lease-accounting)",
    "check_dag AC1 PASS. Each dfn id appears once in the AC1 pages (grep). Uses are defined earlier: L04 uses L01-L03 concepts; L05 uses gaap-vs-ifrs (L04); L06 uses depreciation-and-amortization (L03), revenue-recognition (L05).")
row("AC1b-hours", "2.9-structure", "course/modules/AC/AC1/L04.html, L05.html, L06.html data-hours; course/modules/AC/AC1/index.html hub cards and data-hours-lessons",
    "data-hours: L04 11, L05 12, L06 12; hub cards 'L04 · 11 h', 'L05 · 12 h', 'L06 · 12 h'. AC1 lessons L01-L08 sum 11+12+11+11+12+12+11+10 = 90 = hub data-hours-lessons=\"90\". Hours are design targets; not paced (architect ruling).")
row("AC1b-data-simulated", "2.5-lab", "course/modules/AC/AC1/L04.html lines 52, 130, 323; L05.html lines 52, 128, 340; L06.html lines 52, 125, 303; twins docstrings",
    "Each page's why-it-matters and lab hypothesis label the generated data SIMULATED; each twin docstring says SIMULATED. Each page has an honest-pending block and no real company, contract or lease is embedded.")
row("AC1b-quiz-keys-cross", "2.9-structure", "course/modules/AC/AC1/L04.html, L05.html, L06.html quiz sections (data-kind, data-answer, data-correct)",
    "Numeric keys: L04 -90000, 205000, 30000; L05 62000, -13200, 20583168; L06 2487, 8289, -776, 10001, 1785952; each equals the worked solution cited in its explanation (M1-M4, P3, lab output). Each multiple-choice item has exactly one data-correct option and the explanations agree with the keys.")
row("AC1b-L04-quiz", "2.2-numbers", "course/modules/AC/AC1/L04.html quiz items L04q1 to L04q9 (lines 486-554)",
    "Keys and explanations re-read: L04q1 Corollary 2.3; q3 Prop 3.1 (interest moved); q5 Prop 2.1 proof; q6 Remark 1.2; q8 E2 (cumulative difference negative); q9 Prop 3.1 sum unchanged.")
row("AC1b-L05-quiz", "2.9-structure", "course/modules/AC/AC1/L05.html quiz items L05q1 to L05q9 (lines 503-562)",
    "Keys and explanations re-read, including the changed L05q9 explanation (line 561): 'This lesson cites no primary text for the governing criteria, so they are open here.' Consistent with Section 3 and Definition 1.2.")
row("AC1b-L06-quiz", "2.9-structure", "course/modules/AC/AC1/L06.html quiz items L06q1 to L06q8 and numeric items (lines 466-526)",
    "Keys and explanations re-read, including the changed L06q8 explanation (line 520): 'This lesson cites no primary text on that point, so the requirement is open here.' Numeric items match M1-M4 and E3 values.")
row("AC1b-scope-words", "2.9-structure", "course/modules/AC/AC1/L04.html, L05.html, L06.html: changed sentences (L04 63, 78, 295, 321; L05 52, 68, 462, 561; L06 120, 301, 425, 432, 520) and scope words only, all, every, same, any, exactly, guaranteed, zero, always",
    "Changed sentences checked for their scope words: 'every year' in L06 120 (verified for all 7 years) and in L06 425 (coincide at 0 bps: interest 0, amortization = payment, verified); 'raises' in L04 63 (the lesson does raise such questions: Section 4, section 5 bullet 4, R2); 'only' in L06 425 ('only where its expense equals') is an explicit condition. grep: 0 matches for banned phrases 'roughly half', 'about 6%', 'historically', 'typically'; the single ellipsis-like token is \\dots in L05 line 68 (sequence notation).")
row("AC1b-L04-P2", "2.2-numbers", "course/modules/AC/AC1/L04.html problem P2 (lines 398-404)",
    "Example Q1 = 40,000 cents, four shares of 10,000 expensed by end of quarter 4, unexpired 0; quarter 4 has no purchase; agreement at one date only; a positive purchase gives P_t = Q_t - floor(Q_t/4) + ... >= 1 as argued. Consistent with Corollary 2.3.")
row("AC1b-L05-remark24-bullet", "2.9-structure", "course/modules/AC/AC1/L05.html section 4 bullet 3 (line 347); Remark 2.4 (line 121)",
    "Bullet: 'a balance is a timing wedge' with 32,792,272 cents at 40 percent and 23,333,398 cents at 0 percent; both match lab output. Remark 2.4 says the balance can be large in between; that is the wording used.")
row("AC1b-card-c069", "2.9-structure", "course/modules/AC/AC1/cards.json AC1-c069; L05 paragraph after Section 2 (line 124)",
    "Back says the difference is the convention-1 over-time revenue through month m, referring to the paragraph before Lab 1 and P3. Matches line 124 and P3 (line 424-426).")
row("AC1b-card-c050", "2.9-structure", "course/modules/AC/AC1/cards.json AC1-c050; L04 Section 2 paragraph (line 78)",
    "Back: rule A expenses in full; rule B shares divided by four rounded down, last share the remainder. Matches the changed line 78 (both conventions of this lab; rule B shares) and the lab code.")
row("AC1b3-L05-top-line", "2.9-structure", "course/modules/AC/AC1/L05.html line 52 (why-it-matters)",
    "Re-verified (sentence changed this delta): 'Revenue is the first item that L02 lists for the income statement (revenue, the costs that match it, and net income)'. course/modules/AC/AC1/L02.html line 64 lists 'revenue, the costs that match it, and net income' in that order. The lab uses one SIMULATED contract with four obligations (page pre.expected line 311).")
row("AC1b3-equal-shares", "2.9-structure", "tests/labs/AC1/lab-AC1-L05-1.py lines 17-18 (docstring), 106 (billing_schedule docstring); tests/labs/AC1/lab-AC1-L06-1.py line 61 (straight_line docstring); L05 Definition 1.2-1.4 text (lines 63, 73, 92)",
    "L05 twin: billing 'as equal as whole cents allow' (line 18; code allocate(price - upfront, [1]*12) at line 108). L06 twin straight_line docstring: each year but the last takes total // years, the last the remainder. Matches the page text.")
row("AC1b3-card-c062", "2.9-structure", "course/modules/AC/AC1/cards.json AC1-c062; L05 Definition 1.2 (line 63)",
    "Back: point obligation delivered in one month; over-time obligation delivered over twelve months. Matches Definition 1.2 and the twin's delivery_month field and MONTHS.")
row("AC1b3-card-c088", "2.9-structure", "course/modules/AC/AC1/cards.json AC1-c088; L06 misconception 1 (line 320); Proposition 2.3 (line 100)",
    "Back: 'Only the sums over the term are guaranteed equal (Proposition 2.3)'. Prop 2.3 proves sum equality; pre.expected shows year-by-year differences (279-285, 294), so per-year equality is not claimed.")
row("AC1b4-L06-prop21-hypothesis", "2.5-lab", "course/modules/AC/AC1/L06.html Proposition 2.1 statement (line 80) and Definition 1.2 (lines 62-63)",
    "Prop 2.1 hypothesis: integer rate in bps, integer payment, L0 the PV rounded once. Matches generate() (rate randint 400-800 bps, integer payment) and present_value_cents (round once).")
row("AC1b4-L06-R1-pattern-scope", "2.9-structure", "course/modules/AC/AC1/L06.html R1 solution (line 425)",
    "Re-verified (changed this delta). 'Proposition 2.4 is proved for pattern F only' (matches proof at line 115). At 0 bps: pattern_check(120000, 5, 0) gives F = 120000 in every year and S = 120000 (interest 0, amortization = payment): the 'coincide in every year' claim is true. Section 4 bullet at line 311 says the identity is outside scope for variable payments, options and modifications.")
row("AC1b4-L05-R1-scope", "2.9-structure", "course/modules/AC/AC1/L05.html R1 solution (line 462)",
    "Re-verified (changed this delta): 'The rules for identifying obligations are not stated on this page, and this lesson cites no primary text for them.' Matches Definition 1.1 (line 58) and Section 3 (line 338).")
row("AC1b4-L05-section-ref", "2.9-structure", "course/modules/AC/AC1/L05.html Definition 1.1 (lines 57-58) and Section 4 bullet 4 (line 348)",
    "Definition 1.1 says the criteria are the open question of Section 3; bullet 4 says 'Section 3 names them'. Section 3 lists the four open inputs (line 338). Locators corrected: bullet 4 is at line 348 in the current file.")
row("AC1b4-L06-section-ref", "2.9-structure", "course/modules/AC/AC1/L06.html R1 solution (line 425) and section 4 bullet (line 311)",
    "Line 425: 'Section 4 says the identity does not cover them' (variable payments, options, modifications). Line 311: 'A lease with any of them is outside the scope of Proposition 2.1 to 2.4 as stated.' Consistent.")
row("AC1b4-L04-why-scope", "2.9-structure", "course/modules/AC/AC1/L04.html lines 52 and 321",
    "Line 52: 'The lesson does not state what US GAAP or IFRS Standards require, because this lesson cites neither primary text.' Line 321 (changed): 'this lesson states none of those rules'. Both are consistent with Remark 1.2 (line 63).")
row("AC1b4-L04-corollary-sentence", "2.9-structure", "course/modules/AC/AC1/L04.html section 5 bullet 1 (line 328)",
    "Text: 'Corollary 2.3 says that the two differ by the unexpired balance, and says nothing about which one reports the economics better.' Matches Corollary 2.3 (line 115).")
row("AC1b4-L05-misc1-peak", "2.2-numbers", "course/modules/AC/AC1/L05.html Misconception 1 (lines 355-357)",
    "'a contract liability of up to 32,792,272 cents', 'a contract asset in 8 months', 'a peak balance of 32,792,272' match page pre.expected lines 323, 327 (max_contract_liability_cents 32792272, months_with_contract_asset 8).")
row("AC1b4-L05-interp-remainders", "2.2-numbers", "course/modules/AC/AC1/L05.html interpretation (line 333)",
    "Remainder numbers recomputed: 452,837 (remainder 452,844) and 2,977,691 (remainder 2,977,697); six months each give 2,717,022 and 17,866,146, total 20,583,168 (recheck_r7.py).")
row("AC1b4-L06-E3-crossing", "2.2-numbers", "course/modules/AC/AC1/L06.html E3 solution (lines 413-414) and Remark 2.5 cross-reference",
    "F below S first in year 5: 12467522 - 13034272 = -566750; F above S in years 1-4 (year 4: 13110645 vs 13034272). Recomputed in recheck_r7.py.")
row("AC1b4-L06-misc3-residual", "2.9-structure", "course/modules/AC/AC1/L06.html Misconception 3 (lines 326-330)",
    "Text matches the algebra: the schedule closes exactly by construction (Prop 2.1); the one-cent adjustment is the accumulated integer-step residual. Verified against lab output final_payment_adjustment_cents 1.")
row("AC1b4-card-c081", "2.9-structure", "course/modules/AC/AC1/cards.json AC1-c081; L06 Definition 1.4 (line 73)",
    "Back: first n-1 years take floor(total payments / n), last year the remainder, a lab convention. Matches Definition 1.4 and straight_line in the twin.")
row("AC1b4-card-c090", "2.2-numbers", "course/modules/AC/AC1/cards.json AC1-c090; L06 Misconception 3 (lines 326-330)",
    "Back: final payment 13,034,273 against contractual 13,034,272, rounding of PV and interest. Matches the page pre.expected lines 285-287.")
row("AC1b4-L05-lab-billing-code", "2.5-lab", "tests/labs/AC1/lab-AC1-L05-1.py billing_schedule (lines 105-108), allocate (67-81), over_time_schedule (84-88); L05 page code block (lines 129-310)",
    "embed_compare.py: the page code block is identical to the twin (True). Current locators verified by grep: billing_schedule def line 105, allocate def line 67, over_time_schedule def line 84.")
row("AC1b4-L06-lab-straight-line", "2.4-math", "tests/labs/AC1/lab-AC1-L06-1.py straight_line (lines 60-63); L06 Definition 1.4 (line 73)",
    "straight_line: base = total // years, last year takes total - base*(years-1); matches the Definition 1.4 text (floor of total divided by n, last year the remainder). Locators corrected from the round 6 fragment.")
row("AC1b6-L05-docstring-convention2", "2.5-lab", "tests/labs/AC1/lab-AC1-L05-1.py docstring lines 12-15 (convention 2 sentence); revenue_schedule lines 91-102; main() lines 122-179",
    "Convention 2 sentence ('recognizes every over-time obligation in month 12 instead ... the allocation and the total are the same under both conventions') is at twin lines 12-15. revenue_schedule over_time branches at lines 95-99 and 102; main at 122. Output matches the docstring.")
row("AC1b6-L05-hypothesis-billing", "2.5-lab", "course/modules/AC/AC1/L05.html hypothesis (line 128); twin UPFRONT_PERCENT (line 29), the billing scenario loop (lines 148-149) and the billing docstring (line 17)",
    "Hypothesis: 40 percent billed at signing and 0 percent (contract asset) scenarios; code runs upfront_percent in (UPFRONT_PERCENT, 0). Matches.")
row("AC1b6-L06-why-it-matters", "2.9-structure", "course/modules/AC/AC1/L06.html line 52",
    "'a seven-year lease at 6.30 percent': output term_years 7, rate_bps 630. 'two expense patterns total the same payments at different dates': sum_expense identities True (lines 290-291). 'asset less the liability moves with cash paid less pattern F expense in every year': articulation_every_year True.")
row("AC1b6-L06-remark25-numbers", "2.2-numbers", "course/modules/AC/AC1/L06.html Remark 2.5 (line 120); L06 pre.expected block, page lines 279-285",
    "Interest year 1 4535544 and year 7 772492; amortization 10284680 (years 1-6) and 10284683 (year 7); pattern F 14820224 ... 11057175 falls each year; pattern S 13034272 and 13034273; F above S in years 1-4 and below in years 5-7. All printed in the page pre.expected block (lines 279-285).")
row("AC1b4-L06-remark25-causal", "2.2-numbers", "course/modules/AC/AC1/L06.html Remark 2.5 (line 120)",
    "Re-verified (sentence rewritten in this delta to rest on the printed numbers). 'In Lab 1 pattern F falls in every year, as the printed output shows: amortization is 10,284,680 cents in years 1 to 6 and 10,284,683 in year 7, and interest falls from one year to the next by at least 535,420 cents (the smallest fall, from year 1 to year 2).' Recomputed: interest falls 535420, 569151, 605008, 643123, 683640, 726710 (minimum 535420); F falls 535420, 569151, 605008, 643123, 683640, 726707, all positive; the year 7 amortization rise of 3 cents is below every interest fall. The sentence no longer claims that the structure forces the fall.")
row("AC1b6-locators-L05", "2.9-structure", "course/modules/AC/AC1/L05.html (current locators) and tests/labs/AC1/lab-AC1-L05-1.py (current locators)",
    "Round 6 cited L05 locators one line off. Current locators checked by grep this round: page interpretation 333; section 3 heading 336; section 4 heading 343; section 5 heading 353; P3 problem 423 (solution 425); R1 problem 459 (solution 462); key-results allocation row 488 and row 492; quiz L05q1 506. Twin: generate 50, allocate 67, over_time_schedule 84, revenue_schedule 91, billing_schedule 105, over_time_month_6 173. The fragment cites these current locators, so the round 6 fault is superseded; no page content change is needed.")
row("AC1b-L05-quiz-extra", "2.9-structure", "course/modules/AC/AC1/L05.html quiz L05q6 and L05q7 (lines 531-548)",
    "L05q6 key 'billing totals the price and convention-1 revenue totals the price (Proposition 2.3)' and L05q7 key 'revenue moves between obligations, and the total is unchanged (Remark 1.5)' match the proofs and Remark 1.5.")
row("AC1b7-L04-remark12", "2.9-structure", "course/modules/AC/AC1/L04.html Remark 1.2 (line 63)",
    "Re-verified (changed this delta): 'it marks each standard-specific question it raises as open. Problem R2 lists the standard-specific questions this lesson leaves open.' The questions raised are in Section 4 (line 321), section 5 bullet 4 (line 331) and R2 (line 449); each is marked open there.")
row("AC1b7-L04-sec2-convention", "2.9-structure", "course/modules/AC/AC1/L04.html Section 2 paragraph (line 78)",
    "Re-verified (changed this delta): 'both are conventions of this lab; this page states neither as a framework rule'. Rule A and rule B as coded: rule A expense = opex + interest + prepaid_paid in the paid quarter; rule B shares as described (twin shares() lines 54-57). The page makes no framework claim.")
row("AC1b7-L04-sec4", "2.9-structure", "course/modules/AC/AC1/L04.html Section 4 paragraph (line 321)",
    "Re-verified (changed this delta): 'It needs the rule each framework applies to each type of transaction, and this lesson states none of those rules.' The lesson's own rules (rule A, rule B, presentations) are labelled conventions, not framework rules, so the claim is accurate.")
row("AC1b7-L05-def13", "2.9-structure", "course/modules/AC/AC1/L05.html Definition 1.3 (line 68)",
    "Re-verified (changed this delta): the parenthetical 'the price each obligation would carry if sold alone, used here as allocation weights' is a gloss of the weights; the twin's generate() draws stand-alone prices as positive integers (lines 60-66). No claim about a standard.")
row("AC1b7-L06-sec3", "2.9-structure", "course/modules/AC/AC1/L06.html Section 3 paragraph (line 301)",
    "Re-verified (changed this delta): 'Each of these is a standard-specific question. This lesson cites no primary text, so the answer is open here and the lesson states no claim about it.' The four decisions listed match the model (line 301 list; Definitions 1.2-1.4).")
row("AC1b7-L06-R2", "2.9-structure", "course/modules/AC/AC1/L06.html R2 solution (line 432)",
    "Re-verified (changed this delta): 'None of these four questions is answered by Propositions 2.1 to 2.4, which hold for any schedule that follows Definitions 1.3 and 1.4.' Consistent with Props 2.1-2.4 proofs (lines 83-116), which use only Definitions 1.3-1.4.")
row("AC1b7-process-words", "2.9-structure", "course/modules/AC/AC1/L04.html, L05.html, L06.html (learner text)",
    "grep -i -E 'builder|verifier|round [0-9]|unit report|REQUESTS' on the three pages: 0 matches. No process words in learner text.")

frag = {
    "unit": "AC1",
    "slice": "AC1-b",
    "round": 7,
    "round_note": "round 7 (independent re-verification after the round-6 fixes at de53f7e; delta from d57df1e, the round-6 pin)",
    "verifier": "Haiku independent verifier for slice AC1-b (L04, L05, L06 and twins); did not build AC1 and shares no context with its builders",
    "pin": "de53f7e883dc4d6f6dacd6042d13acd197afba5d",
    "base": "d57df1e (round 6 pin; round 6 fragment /tmp/fanout-frags/AC1-b.round6.json, context only; its PASS rows were not trusted)",
    "checkout": "/tmp/verify7-AC1-b (detached; .venv symlink; vendor copied)",
    "scratch": "/tmp/AC1-v/AC1-b-r7",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice is pages and twins, not a project slice: the at-least-3 new student-error mutants and the five alternative correct implementations apply to project slices only; mutants is empty for this slice.",
        "Delta since d57df1e: L04.html (lines 63, 78, 295, 321), L05.html (lines 52, 68, 462, 561), L06.html (lines 120, 301, 425, 432, 520), cards.json (AC1-c102 only, an L07 card outside this slice). The three twins are byte-identical to d57df1e; lab-AC1-L07-1.py changed and is outside this slice.",
        "Every row was re-derived this round: no PASS row is carried. Subjects changed in the delta were re-read in full; unchanged subjects were re-read and re-checked against the same evidence.",
        "Round 6 FAIL rows: AC1b4-L06-remark25-causal now PASS (rewritten sentence rests on printed numbers, recomputed). AC1b6-locators-L05 now PASS (current locators cited; the fragment locators were the fault, not the page).",
        "Lab output is SIMULATED (seeds 2604, 2605, 2606); results read off a lab are grade C naming that lab, and the rows keep that basis.",
        "Not checked: live reachability of any publisher or SEC source (no slice row cites a registry key); the grade of the Beneish or any other external constant (not in this slice); hours on pace (architect ruling: hours are design targets, not fail conditions); the pytest test count (pytest -q printed dots and exit 0 but no summary line; collect-only count not taken).",
    ],
    "summary": "",
    "rows": R,
    "mutants": [],
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in R:
    counts[r["status"]] += 1
frag["summary"] = (f"AC1-b round 7 (L04, L05, L06 and twins; pin de53f7e): {len(R)} rows, {counts['PASS']} PASS, "
                   f"{counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Verdict "
                   f"{'PASS' if counts['PASS'] == len(R) else 'FAIL'}.")
frag["verdict"] = "PASS" if counts["PASS"] == len(R) else "FAIL"
out = root / "ledgers/AC1/AC1-b.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, len(R), counts)
