import json, sys
from datetime import datetime, UTC

R = "ledgers/FC1/scripts/FC1-a-r3/"
rows = []
def row(id_, check, location, status, evidence, fix=""):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- tool and command rows
row("cmd-check-pages", "2.9-structure", "course/modules/FC/FC1/ (hub, L01-L03)", "PASS",
    "tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS' (exit 0); output kept in /tmp/fc1-v/a-r3/check_pages.txt")
row("cmd-check-dag", "2.9-dag", "course/modules/FC/FC1/", "PASS",
    "tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' (exit 0)")
row("cmd-page-smoke", "2.9-smoke", "FC/FC1/index.html, L01.html, L02.html, L03.html", "PASS",
    "tools/page_smoke.py --unit FC1 --pages FC/FC1/index.html FC/FC1/L01.html FC/FC1/L02.html FC/FC1/L03.html -> 'page_smoke FC1: PASS' (exit 0). The tool prints only the unit summary, so per-page detail is not shown.")
row("cmd-run-labs-L01", "2.5-labs", "course/modules/FC/FC1/L01.html lab-FC1-L01-1", "PASS",
    "tools/run_labs.py --unit FC1 --page L01 -> 'run_labs FC1: PASS (1/1)'")
row("cmd-run-labs-L02", "2.5-labs", "course/modules/FC/FC1/L02.html lab-FC1-L02-1", "PASS",
    "tools/run_labs.py --unit FC1 --page L02 -> 'run_labs FC1: PASS (1/1)'")
row("cmd-run-labs-L03", "2.5-labs", "course/modules/FC/FC1/L03.html lab-FC1-L03-1", "PASS",
    "tools/run_labs.py --unit FC1 --page L03 -> 'run_labs FC1: PASS (1/1)'")
row("cmd-twin-alone", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py, L02-1.py, L03-1.py", "PASS",
    "python -I -W error <twin> run alone: exit 0 and empty stderr for all three. " + R + "lab_page_vs_twin.py: code_eq_twin=True, expected_eq_output=True, deterministic=True for L01, L02 and L03.")
row("cmd-ruff", "2.9-gate", "repository", "PASS", "ruff check . -> 'All checks passed!'; ruff format --check . -> '340 files already formatted'")
row("cmd-mypy", "2.9-gate", "repository", "PASS", "mypy --no-incremental -> 'Success: no issues found in 229 source files'")
row("cmd-verify-refs-live", "2.1-citations", "references/references.json keys harris2002trading, mishkin2021economics (FC1 units)", "PASS",
    "tools/verify_refs.py --unit FC1 (live) -> 'live re-verification of FC1: 2 of 560 entries, 0 problems'; --offline -> '560 entries, 0 problems'")
row("cmd-numbers-recompute", "2.2-numbers", "all prose numbers in index, L01, L02, L03", "PASS",
    "Independent recomputation with fractions.Fraction in " + R + "numbers_r3.py. Matches: S1=1900, S2=2710, S10=6861.8940391 (686189 cents), 6.8619 at 4 dp, rounding-first gives 6861.90, Ex 3.6 1818.18 (181818 cents) = 18.18%, half-share stage-10 total 181790 cents, E2 2/11, M2 S2=1850, M3 equity -20, placement 7/9=77.8% and 80% of 9 = 7.2 (8 correct), hours 71.4/28.6, L03 Ex 1.4 0.6%, E3 0.03%, L03 M1 200, M2 -160 (320-480), Ex 2.5 -600 (400-1000), R2 1400 (400+1000), q7 1500 vs 2000, tie profit 1000.")
row("grep-scope-words-L03", "2.9-prose", "course/modules/FC/FC1/L03.html", "PASS",
    "Scope-word scan (every/all/only/always/same/exactly) of L03: each hit is backed by a proof (Prop 2.3, Cor 2.4, Prop 3.2 cases k=0,1,2,>=3), the finite grid is labelled as such (interpretation and Remark 3.3), or a definition (Definition 1.1 'in this sense only').")

# ---- hub
row("hub-placement-numbers", "2.2-numbers", "index.html lines 69, 80-131", "PASS",
    "Nine items: seven prerequisite (Pq1-Pq7) and two skill checks; 80% of nine is 7.2 so eight correct; 7/9 = 77.8% stated as 78 percent. Answers and explanations recomputed in " + R + "numbers_r3.py.")
row("hub-hours-arithmetic", "2.9-hours", "index.html line 29, 39-41", "PASS",
    "data-hours-lessons=50, data-hours-project=20 sum to 70; lesson data-hours 10 x 5 = 50 (L01-L03 data-hours=10 verified); 50/70=71.4%, 20/70=28.6%; bar widths 71.4% + 28.6%.")
row("hub-rung2-lab2-description", "2.6-projects-hub-claim", "index.html line 152", "FAIL",
    "Line 152 says Lab 2 on the project page is 'the coupon-timing line of the same bond with its blanks'. course/modules/FC/FC1/project.html lines 104-106 say Lab 2 is 'the discount exponent and the trade's cash flow' (the two blanks are the exponent and the cash flow; the coupon line is not blanked). Rung 2 on project.html line 46 agrees with the lab, so the hub is the outlier.",
    "Replace 'the coupon-timing line of the same bond with its blanks' with 'the discount exponent and the trade's cash flow, with its two blanks'.")
row("hub-rung1-rung2-skill-items", "2.2-numbers", "index.html lines 122-131", "PASS",
    "Coupon 10000 x 500/10000 = 500 cents; period-3 flow 500 + 10000 = 10500 cents; both match the coupon rule of project.html (coupon_bps of face, half away from zero).")
row("hub-structure-objectives-prereqs", "2.9-structure", "index.html lines 44-65, 135-171", "PASS",
    "Six objectives (4-8 required); prerequisites P0.1 and E1 titles match curriculum/01-foundations.yaml:7 and 02-economics-finance-core.yaml:19; lesson map links L01-L05; data status says no dataset is used (no data-files attribute in index, L01, L02 or L03).")
row("hub-core-reading-registry", "2.1-citations", "index.html lines 164-171; references/references.json", "PASS",
    "data-cite entries render from the registry; no page or figure is cited from the books (L03 line 341 and 564 say book level only). Registry records: harris2002trading title 'Trading and Exchanges: Market Microstructure for Practitioners', year 2002, matching L03's 'registry year 2002'; mishkin2021economics year 2021 (curriculum string 2022). The hub renders registry fields only, which the architect decision allows.")
row("hub-lesson-card-claims", "2.9-prose", "index.html lines 139-143", "PASS",
    "Each card blurb matches its lesson: L01 (intermediary, multiplier, leakage, loss buffer), L02 (venue, taxonomy, register check), L03 (quote, spread, capture, closed-sequence condition), L04 and L05 (seeded match, conservation check, business-day offsets) per L04.html and L05.html headings and the lab text.")
row("hub-placement-grade-C-text", "2.3-grades", "index.html line 114-120", "PASS",
    "'Grade C ... working paper, practitioner research or single-sample evidence' matches BLUEPRINT.md section 3 grade C row (line 161).")

# ---- L01
row("L01-prop2.2-proof", "2.4-mathematics", "L01.html lines 88-96", "PASS",
    "Re-derived: X_t + l_t = rho D_t + (1-rho) D_t = D_t under A1 and the definition of the loan; summing gives the cumulative identity.")
row("L01-prop3.1-closed-form-proof", "2.4-mathematics", "L01.html lines 102-113", "PASS",
    "Finite geometric sum with q = 1-rho; q != 1 since rho > 0; limit uses 0 <= q < 1 from A1; rho = 1 gives S_n = d, checked with 0^0 = 1. Verified numerically (numbers_r3.py, S10 = 6861.8940391).")
row("L01-prop3.5-hypothesis-A3", "2.4-mathematics", "L01.html lines 76 (A3), 131-133 (Proposition 3.5), 135-138 (proof)", "FAIL",
    "Proposition 3.5 says 'Keep A1 and A3' while replacing A2 by A2', under which 'the rest is held as cash outside the bank'. A3 (line 76) says 'No cash leaves the bank'. The variant violates A3 whenever phi < 1, so the statement assumes a hypothesis its own variant contradicts. The proof uses only A1 and the recursion D_{t+1} = phi(1-rho) D_t, so the fix is to drop A3 from the list and state that A3's no-cash-leaves clause is replaced for the variant.",
    "In Proposition 3.5 replace 'Keep A1 and A3, with 0 < rho <= 1' by 'Keep A1, with 0 < rho <= 1, and keep the no-withdrawal and no-repayment parts of A3; the cash held outside the bank is the leakage the variant adds.' Or state the proposition on A1 alone, since the proof uses nothing else.")
row("L01-Dt-definition-vs-recursion", "2.4-mathematics", "L01.html line 73 (Assumption 2.0), lines 84-86, 94-95, 131-133", "FAIL",
    "Assumption 2.0 says 'Let D_t be its deposits at stage t', which reads as the balance. But the recursion treats D_t as the deposit newly received at stage t: D_1 = (1-rho)d (line 84) excludes the stage-0 deposit d, and S_n = sum_t D_t (line 86) sums these flows. Under A3 (line 76, 'no deposit is withdrawn') the balance after stage 1 would be d + (1-rho)d = (2-rho)d, not (1-rho)d. The definition contradicts the model's own arithmetic.",
    "Redefine D_t in Assumption 2.0 as 'the deposits received at stage t' (new deposits, not the balance), and say that the balance after stage n is S_n. Keep S_n = sum D_t and the recursion as they are.")
row("L01-prop2.2-cumulative-claim", "2.4-mathematics", "L01.html lines 88-96", "PASS",
    "Cumulative identity follows from the stage identity; with the flow reading of D_t above (see L01-Dt-definition-vs-recursion) the sum is S_n.")
row("L01-prop4.1", "2.4-mathematics", "L01.html lines 149-167", "PASS",
    "Assets A - lambda = D + E - lambda; equity = assets - deposits = E - lambda (Remark 1.2); nonnegative iff lambda <= E.")
row("L01-remark3.2-R1-R3-P-problems", "2.4-mathematics", "L01.html lines 115-118, 343-446", "PASS",
    "Remark 3.2 (rho=0 gives S_n = (n+1)d); P1 difference S_{n+1}-S_n = (1-rho)^{n+1} d; P2; P3; R1 bound d/c; R2 least equity = lambda; R3 no phi gives 2d/rho. All re-derived by hand.")
row("L01-example3.3-3.6", "2.2-numbers", "L01.html lines 120-143", "PASS",
    "S1 = 1900, S2 = 2710, S10 = 6861.8940391 -> 6,861.89 dollars (686189 cents); 4-dp rounding first gives 6861.90 (Remark 3.4 correct); Example 3.6 1000/0.55 = 1818.18 (181818 cents); 1818.18 / 10000 = 18.18 percent.")
row("L01-lab1-expected-vs-output", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py; L01.html lines 172-309", "PASS",
    "Page code equals twin; expected block equals the twin's output under python -I -W error; output deterministic. Parts A to D as printed: multiplier 6.8619 at n=10, 686189 cents, limit 10 / 1000000 cents, B all True, C 181790 cents (share 0.5, recomputed) and 181818 limit, D equity 50/0/-50.")
row("L01-lab1-hypothesis-and-interpretation", "2.5-labs", "L01.html lines 171, 310", "PASS",
    "Hypothesis predicts Parts A to D and the printed values agree; interpretation says the parameters are typed in and describe no real bank, and names only what the printed numbers show.")
row("L01-key-results-lab-row-grade", "2.3-grades", "L01.html line 460", "PASS",
    "Row grades 'The exact-arithmetic checks in Lab 1 agree with Propositions ... for the typed-in parameters' as T. Lab 1 is typed-in (not SIMULATED), so the verifier rule for C does not apply; T is accepted here as a checked instance of proved propositions. Noted for the builder: the row restates a check on particular parameters, not a theorem.")
row("L01-canon-breaks-misconceptions", "2.9-prose", "L01.html lines 315-341", "PASS",
    "Canon-breaks bullets and misconceptions 1 to 3 re-read; 6,861.89 and 1900 cited correctly; statements about lab output match the printed lab output.")
row("L01-quiz-explanations", "2.7-cards-quiz", "L01.html lines 466-541", "PASS",
    "Each quiz answer and explanation recomputed: reserve 100; D_1 800; S_2/d 1.75 at rho=1/2; limit 10000; leakage smaller (q6); equity 40; 700 for 400 at rho=1/2.")
row("L01-grade-legend", "2.3-grades", "L01.html line 46", "PASS",
    "Legend entries T, A, B, D, X match BLUEPRINT.md section 3 (C row checked under the legend row L01-grade-legend-C-text).")
row("L01-uses-and-dfn", "2.5-DAG-definitions", "L01.html lines 37, 59, 81; check_dag FC1 PASS", "PASS",
    "Uses line geometric-series (used in Section 3, line 100). Dfn ids def-financial-intermediary and def-bank-money-creation are the two assigned to L01 by the hub; no other concept is defined in L01.")

# ---- L02
row("L02-prop1.4-hypothesis-scope", "2.4-mathematics", "L02.html lines 68-69 (Assumption 1.3), 73-74 (Proposition 1.4), 77-79 (proof)", "FAIL",
    "Proposition 1.4 says 'for any finite set of n trades' but Assumption 1.3 constrains only 'every trade in the classification' (line 69). Counterexample: a set of two trades, one exchange-traded and one with a venue that partly fixes its terms (outside the classification). Exchange count plus OTC count = 1, not n = 2. The proof's step 'by Assumption 1.3 each trade lies in exactly one of the two sets' needs every trade of the set to be classified, which the statement does not require.",
    "State Proposition 1.4 for 'any finite set of n trades, each of which is in the classification of Assumption 1.3' (or make Assumption 1.3 apply to every trade in the set). Re-state the Remark 1.5 and card c021 accordingly.")
row("L02-prop2.5-proof", "2.4-mathematics", "L02.html lines 117-125", "PASS",
    "Each entry has exactly one value on each axis, so each axis partitions the n entries; the statement carries the hypothesis (each entry meets Definition 2.1) explicitly.")
row("L02-remark2.6-P3", "2.4-mathematics", "L02.html lines 127-130, 340-343", "PASS",
    "Entry with k exposure values adds k to the exposure total and so exceeds n by k-1; Problem P3 gives |S|-1; verified 14 for 13 entries (Lab 2 Part D).")
row("L02-example3.1-four-combinations", "2.3-grades", "L02.html line 256 (Example 3.1), line 408 (key-results row 4); cards.json FC1-c030", "FAIL",
    "The claim 'the four combinations of form and venue all occur in the register' is a finite existence check over 12 typed-in entries, graded T in the key-results table and asserted as 'Yes' on card c030. Lab 2 prints no form-by-venue cross-tabulation (Part C prints exchange entries only), so the check is an enumeration of the register by reading, not a printed lab result and not a proof. BUILDER_RULES/verifier rule 4: an enumeration is grade C with its basis named, not T.",
    "Grade the key-results row C with basis 'Lab 2 register entries 1, 3, 4, 6 (the code of the lab)', or add a printed cross-tab to Lab 2 and grade C naming the lab. Change card c030 to match.")
row("L02-lab2-expected-vs-output", "2.5-labs", "tests/labs/FC1/lab-FC1-L02-1.py; L02.html lines 135-247", "PASS",
    "Page code equals twin; expected equals output; counts recomputed from REGISTER by hand: exposure 3,3,2,2,2; form 6,6; venue 4,8; exchange entries 1,3,5,11 with cash 1, derivative 3; three exposure classes; malformed total 14 for 13.")
row("L02-lab2-hypothesis-and-interpretation", "2.5-labs", "L02.html lines 134, 247", "PASS",
    "Hypothesis lists exactly the Part B counts and Part C result printed; the interpretation says the register is typed in and makes no market claim.")
row("L02-misconceptions-and-register-claims", "2.9-prose", "L02.html lines 279-292", "PASS",
    "'Lab 2 lists six derivative entries, and they carry all five exposure values; rates carries two' is a statement about the register contents in the lab code (derivatives: entries 3,5,6,8,10,11 with exposures equities, rates, rates, credit, fx, commodities). Exchange-traded spanning three exposure classes printed by Part C.")
row("L02-uses-line-intermediary", "2.5-DAG", "L02.html line 37 (Uses) vs body", "FAIL",
    "The Uses line declares 'financial intermediary (Lesson 1, Definition 1.1)', but the term is not used anywhere in the body of L02 (its only occurrences are the Uses line itself and the L01 link in the lesson nav at line 504). The declared dependency is not used.",
    "Remove the financial intermediary entry from the L02 Uses line (or use it in the text).")
row("L02-grade-legend", "2.3-grades", "L02.html line 46", "PASS",
    "Legend matches the template 'lesson.html' except C text (see cross-unit row grade-legend-C-text).")
row("L02-key-results-other-rows", "2.3-grades", "L02.html lines 405-409", "PASS",
    "Rows 1-3 and 5 are T with proofs or a lab check of counts; row 5 counts recomputed (exposure 3,3,2,2,2; form 6,6; venue 4,8). Row 3 cites Remark 2.6 and Lab 2 Part D correctly.")
row("L02-quiz", "2.7-cards-quiz", "L02.html lines 415-494", "PASS",
    "Answers: OTC by terms (Def 1.1); exactly one (Def 2.1); derivative count 6; exchange derivatives 3; rates for the government bond future; 1 for the two-exposure register; no size statement (Remark 3.2); 5 exposure values; form axis (Remark 2.2); exchange/OTC venues. All correct.")

# ---- L03
row("L03-prop2.3-proof-algebra", "2.4-mathematics", "L03.html lines 96-106", "PASS",
    "Re-derived: sigma q p - sigma q m_n = sigma q (m_t - m_n) + h q, using sigma^2 = 1; summing gives C - m_n sum sigma q = sum sigma q (m_t - m_n) + hV, and C + I m_n = C - m_n sum sigma q. Verified with exact integers in the lab (Part B identity True).")
row("L03-cor2.4-prop2.3-P1-P2", "2.4-mathematics", "L03.html lines 108-116, 396-413 (P1, P2)", "PASS",
    "Cor 2.4: mid-move term zero, V = 2Q (Remark 2.2) gives P = sQ and C = P since I = 0. P1 and P2 re-derived; P2 uses d * I (correct sign).")
row("L03-example2.5-numbers", "2.2-numbers", "L03.html lines 118-121, 351, 477", "PASS",
    "C = -9998*100 + 9992*100 = -600; I = 0; hV = 400; mid-move term = -1000 (100 x 10); profit -600. Re-derived in numbers_r3.py. Misconception 1 gap 10-cent is 10000 - 9990.")
row("L03-prop3.2-equilibria", "2.4-mathematics", "L03.html lines 148-159", "PASS",
    "Asymmetric profiles: a1 < a2 leads to a strict gain for dealer 2 (a1 > c) or dealer 1 (a1 = c, tie at a2 earns (a2-c)Q/2 > 0). Symmetric k=0,1,2 each checked against deviations d<a, d=a, d>a; k>=3 deviation d = a-1 gives (k-1)Q > kQ/2 iff k > 2. Re-derived.")
row("L03-remark3.3-R1-R3", "2.4-mathematics", "L03.html lines 161-163, 446-465", "PASS",
    "R1 three-dealer symmetric profiles: (c,c,c) and (c+1)^3 equilibria, (c+2)^3 not (deviation to c+1 gives Q > 2Q/3). Labelled as symmetric profiles only. R3 correctly separates the finite grid from the all-asks proof.")
row("L03-lab1-expected-vs-output", "2.5-labs", "tests/labs/FC1/lab-FC1-L03-1.py; L03.html lines 166-334", "PASS",
    "Page code equals twin; expected equals output under -I -W error; deterministic (seed 2026). Printed: 14 trades, inventory 0, cash 4000 = 4 x 1000, terminal mid 10001, spread capture 4000, mid-move -545, P&L 3455 = 4000 - 545, 121 pairs, equilibria (100,100),(101,101),(102,102) only, all symmetric.")
row("L03-lab1-hypothesis-and-interpretation", "2.5-labs", "L03.html lines 168, 333", "PASS",
    "Hypothesis predicts Part A (cash = spread x volume), Part B (identity) and Part C (three symmetric pairs in 121). Interpretation: grid is a finite check and the proof covers all asks; the mid-move sign is path-specific, as Remark 2.6 says. No overreach found.")
row("L03-grades-key-results", "2.3-grades", "L03.html lines 475-480", "PASS",
    "Proved rows are T (Prop 2.3, Cor 2.4, Prop 3.2, Example 2.5 by hand); lab-read rows are C naming Lab 1 (Parts A, B, C), as the verifier rule for lab-read results requires.")
row("L03-uses-line-exchange-otc", "2.5-DAG", "L03.html line 37 (Uses) vs body", "FAIL",
    "The Uses line declares 'exchange-traded and over-the-counter markets (Lesson 2)' with a concept link, but the body of L03 never uses exchange-traded or OTC trading; the only occurrences are the Uses line and the references (Harris title, line 564).",
    "Remove the exchange-vs-otc entry from the L03 Uses line, or use the concept in the text.")
row("L03-canon-breaks-misconceptions", "2.9-prose", "L03.html lines 336-362", "PASS",
    "Canon-breaks bullets cite Example 2.5, Remark 2.2, Assumption A2 (four items: fees, interest, inventory cost, information) and B1-B4; Harris is cited by key with registry year 2002 and no locator. Misconceptions 1 to 3 consistent with Prop 2.3 and Prop 3.2.")
row("L03-problems-and-quiz", "2.7-cards-quiz", "L03.html lines 364-560", "PASS",
    "M1 (cash 200), M2 (-160; 320 and -480), M3 (30 cents, 0.6 percent), E1 (three pairs), E2 (-545 from path), E3 (0.03 percent), quiz answers 4, 200, -1000, 121, 1000, 'a tick' all recomputed. Quiz explanation for (103,103) uses 1500 and 2000 correctly.")

# ---- cross-unit / cards / notation / prose
row("grade-legend-C-text", "2.3-grades", "L01.html line 46; L02.html line 46; L03.html line 46; course/templates/lesson.html line 48; BLUEPRINT.md line 161", "FAIL",
    "The grade legend for C reads 'single study or convention' in L01 and L02 but 'single study' in L03 and in the lesson template. BLUEPRINT section 3 defines C as 'Working paper, practitioner research, or single-sample evidence' and does not list conventions. The three lessons therefore show two different legends for one grade, and the L01/L02 text differs from the grade definition.",
    "Make the C legend identical in L01, L02 and L03 and the lesson template, and match BLUEPRINT section 3 (for example 'working paper, practitioner research or single sample'). Conventions are labelled on the page where they occur, not in the legend.")
row("cards-L01-scan", "2.7-cards", "course/modules/FC/FC1/cards.json FC1-c001..c018, c091..c094", "PASS",
    "Full scan of 22 L01 cards against lesson text: each claim matches the current L01 text (Definition 1.1, Remark 1.2, A1, Def 2.1, Prop 2.2, Prop 3.1, Remark 3.2, Prop 3.5 (card c009 repeats the A3-containing hypothesis, flagged under L01-prop3.5-hypothesis-A3), Ex 3.3, Remark 3.4, Prop 4.1, Lab 1 Parts A to D, misconceptions 1 to 3, Section 5). Numbers found in lesson text by " + R + "cards_r3.py (0 misses).")
row("cards-L02-scan", "2.7-cards", "cards.json FC1-c019..c034, c095..c096", "PASS",
    "Full scan of L02 cards. c021 and c030 need the same corrections as the lesson rows L02-prop1.4-hypothesis-scope and L02-example3.1-four-combinations; the other L02 cards match the current text and Lab 2 printed output (c028 14 for 13, c029 counts, c095 6 and 6, c096 4 and 8).")
row("cards-L03-scan", "2.7-cards", "cards.json FC1-c035..c055, c097..c098", "PASS",
    "Full scan of L03 cards: c036 Definition 1.2, c037 Example 1.4, c042 Corollary 2.4, c043 Example 2.5, c050 Proposition 3.2, c052 to c054 and c097/c098 lab printed values, c055 misconception 3. All match the current L03 text.")
row("cards-duplicates-and-numbers", "2.7-cards", "cards.json (63 cards for L01-L03)", "PASS",
    "Full duplicate scan (" + R + "cards_r3.py): no duplicate ids; near-duplicate fronts are three distinct questions (c053/c097 different quantities, c057/c063 are outside this slice, c095/c096 different counts); no near-duplicate backs above 0.7. Every number on a card appears in its lesson text (0 misses).")
row("cards-coverage", "2.7-cards", "cards.json", "PASS",
    "Card ids cited against the slice: every card's section reference (Definitions, Remarks, Propositions, Examples, Problems, Labs) exists in its lesson (checked by reading and by the lesson-text search).")
row("notation-symbols", "2.4-notation", "L01/L02/L03 math; notation/notation.json symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}", "PASS",
    "Grepped every \\(...\\) expression in index, L01, L02, L03: no use of T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f or \\mathbb{Q}. Local letters (D, X, S, E, A, lambda, phi, kappa, q, V, Q, I, P, C, m, h, a, b, d, c, k, sigma) carry one meaning each within their lesson.")
row("DAG-concepts", "2.5-DAG", "index.html lines 61-62; L01 line 37; L03 line 37; check_dag FC1 PASS", "PASS",
    "check_dag.py --unit FC1 passes. Concept links to E1 (competitive-equilibrium, bertrand-competition) and M1 (geometric-series) are in the prerequisite closure of FC1 (plans/FC1-build-plan.md section 0.1). Two Uses lines name concepts the body does not use (rows L02-uses-line-intermediary and L03-uses-line-exchange-otc).")
row("banned-phrases-and-process-words", "2.9-prose", "index.html, L01, L02, L03 visible prose", "PASS",
    "check_pages.py --unit FC1 includes the banned-string check (BUILDER_RULES 1.3-1.4) and passes; the slice contains no 'the builder', 'verifier', 'round' or 'TODO' in learner text (grep on the four pages).")
row("data-and-figures", "2.8-data", "index.html lines 159-162; L01-L03 (no data-files)", "PASS",
    "No data-files attribute and no snapshot in the slice; each lab uses typed-in or seeded SIMULATED input, labelled on the page (L03 hypothesis: 'SIMULATED customer flow from seed 2026').")
row("registry-mishkin-harris", "2.1-citations", "index.html line 169; L03 lines 341, 564", "PASS",
    "Keys in use: harris2002trading (title and year 2002 match the record; cited at book level with no locator, as the architect decision allows) and mishkin2021economics (hub renders its registry fields). No page-level claim is attributed to either book.")

# ---- verdict counts
fails = [r for r in rows if r["status"] != "PASS"]
counts = {"PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": len(fails)}
frag = {
    "unit": "FC1",
    "slice": "FC1-a",
    "round": 3,
    "verifier": "Haiku independent verifier, FC1-a round 3 (did not build FC1)",
    "pin": "ccfdf4c",
    "base": "ccfdf4c (round-2 pin). The slice files (index.html, L01.html, L02.html, L03.html, lab twins lab-FC1-L01-1..L03-1, cards.json) are byte-identical to e22feb3 and ccfdf4c; git log shows no commit after e22feb3 touches them. The round-2 fragment /Users/billyribeiro/.fanout/frags/C-FC1-a.round2.json does not exist, so no previous PASS row was carried; every row was re-verified from the pinned files.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC3-FC1-a (detached at ccfdf4c, .venv symlinked)",
    "scratch": "/tmp/fc1-v/a-r3/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "mishkin2021economics: curriculum string 'Mishkin, 13th ed. (2022)' vs registry year 2021 (notes.year). The hub renders registry fields only; no slice change needed, owner to decide.",
        "harris2002trading: curriculum string '(2003)' vs registry and Crossref year 2002. L03 states registry year 2002 and cites at book level, consistent with the architect decision."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice read in full: index.html (177 lines), L01.html (559), L02.html (512), L03.html (578), the three twins, and all 63 L01-L03 cards of cards.json (c001-c055, c091-c098).",
        "Mutants: none. The slice is hub and lessons, not a grader; ruling: lab twins are demonstrations and mutation testing applies to project graders only.",
        "Could not check: page_smoke.py prints only the unit summary, so per-page console and 360 px results are not individually visible; project.html and the grader are outside this slice (the rung 2 claim in index.html was checked against project.html only as a text fact); L04 and L05 were checked only for the hub card blurbs, not in full.",
        "Round 2 fragment absent at /Users/billyribeiro/.fanout/frags/C-FC1-a.round2.json, so the delta-based carry rule was not applied; all rows are fresh."
    ],
    "summary": f"Slice FC1-a round 3 at ccfdf4c: {counts['PASS']} PASS, {counts['FAIL']} FAIL. FAILs: L02 Proposition 1.4 scope (missing classified-trade hypothesis, counterexample given); L01 Assumption 2.0 defines D_t as a balance while the model uses new deposits (counterexample arithmetic); L01 Proposition 3.5 keeps A3 while its variant puts cash outside the bank; L02 'all four combinations occur' graded T (enumeration, should be C); hub rung 2 misdescribes project Lab 2; Uses lines in L02 and L03 name concepts never used; C grade legend text differs from BLUEPRINT and across lessons."
}
out = sys.argv[1]
json.dump(frag, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), counts)
