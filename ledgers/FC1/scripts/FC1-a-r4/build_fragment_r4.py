"""FC1-a round 4: write the fragment ledgers/FC1/FC1-a.json (rows are the round-3 ids kept, plus three new ids)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path.cwd()
R = "ledgers/FC1/scripts/FC1-a-r4/out/"
P = "PASS"
F = "FAIL"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        assert fix, rid
        item["fix"] = fix
    rows.append(item)


row("a-r1-gate-check-pages", "2.9-structure", "course/modules/FC/FC1/ (index.html, L01-L03.html, cards.json)", P,
    f"tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS' EXIT=0 ({R}check_pages_unit.out); --all EXIT=0 ({R}check_pages_all.out).")
row("a-r1-gate-check-dag", "2.9-DAG", "course/modules/FC/FC1/", P,
    f"tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS' EXIT=0 ({R}check_dag_unit.out); --all EXIT=0 ({R}check_dag_all.out).")
row("a-r1-gate-check-projects", "2.6-project-tool", "course/modules/FC/FC1/project.html (tool gate only; project rows belong to other slices)", P,
    f"tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS' EXIT=0 ({R}check_projects_unit.out).")
row("a-r1-gate-run-labs", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py, lab-FC1-L02-1.py, lab-FC1-L03-1.py", P,
    f"tools/run_labs.py --unit FC1 --page L01 / L02 / L03 -> 'run_labs FC1: PASS (1/1)' each, EXIT=0 ({R}run_labs_L01.out, run_labs_L02.out, run_labs_L03.out).")
row("a-r1-twins-isolated", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py, L02-1.py, L03-1.py", P,
    f"Run alone as python -I -W error <twin>: EXIT=0 and empty stderr for all three ({R}twin_L01.out, twin_L02.out, twin_L03.out; {R}twin_page_r4.out reports stderr_bytes=0).")
row("a-r1-page-code-equals-twin", "2.5-labs", "course/modules/FC/FC1/L01.html, L02.html, L03.html (lab <code data-run> and expected block)", P,
    f"ledgers/FC1/scripts/FC1-a-r4/twin_page_r4.py -> {R}twin_page_r4.out: page code equals the twin after outer newlines (L01 107 lines, L02 95, L03 150): True for all three; each expected block equals the twin's own stdout: True for all three; no @@ markers left.")
row("a-r1-page-smoke", "2.9-structure", "index.html, L01.html, L02.html, L03.html", P,
    f"tools/page_smoke.py --unit FC1 --pages index L01 L02 L03 -> PASS for each page and 'page_smoke FC1: PASS' EXIT=0 ({R}page_smoke.out); lab runtimes 0.0 s each in Pyodide.")
row("a-r1-ruff-mypy-twins", "2.5-labs", "tests/labs/FC1/*.py and the whole repository", P,
    f"ruff check . -> 'All checks passed!' ({R}ruff_check.out); ruff format --check . -> '553 files already formatted' ({R}ruff_format.out); mypy --no-incremental -> 'Success: no issues found in 385 source files' ({R}mypy_full.out).")
row("a-r1-pytest-relevant", "2.9-structure", "tests/test_labs.py -k FC1; test_page_checks.py, test_page_smoke.py, test_refs.py, test_run_labs.py; test_docs_figures.py", P,
    f"pytest tests/test_labs.py -k FC1 -> 8 passed ({R}pytest_labs_fc1.out); test_page_checks/test_page_smoke/test_refs/test_run_labs all pass EXIT=0 ({R}pytest_page_checks.out); test_docs_figures EXIT=0 ({R}pytest_docs_figures.out); collect-only FC1 = 8 ({R}collect_fc1.out).")
row("a-r1-verify-refs-offline", "2.1-citations", "references/references.json (keys cited by the slice: harris2002trading, mishkin2021economics)", P,
    f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({R}verify_refs_offline.out); tools/verify_refs.py --unit FC1 -> 'live re-verification of FC1: 2 of 560 entries, 0 problems' ({R}verify_refs_unit_live.out).")
row("a-r1-notation-scan", "2.4-notation", "index.html and L01-L03 KaTeX math (16, 259, 33, 306 segments)", P,
    f"ledgers/FC1/scripts/FC1-a-r4/slice_scan_r4.py -> {R}slice_scan_r4.out: no \\mathbb, R_f, \\Phi, \\gamma_3, \\gamma_4, \\SR, \\emgamma, R^\\ast, \\mathbb{{Q}} and no bare T in any math segment; single-letter symbols are local letters defined on first use; macros are KaTeX built-ins or Greek letters; no \\R or registered macro is misused.")
row("a-r1-process-banned-scan", "2.9-prose", "index.html, L01-L03.html and the three twins", P,
    f"slice_scan_r4.py: banned={{}} process={{}} ellipses=0 on all four pages and the three twins ({R}slice_scan_r4.out). The two '...' in the L02 twin are Python tuple[str, ...] type syntax in code.")
row("a-r1-no-external-no-figures", "2.8-figures", "index.html, L01-L03.html", P,
    f"slice_scan_r4.py: external=[] on all four pages; grep counts of <img, <svg, <iframe, data-chart, data-files and assets/data are 0 on each page (this round).")
row("a-r1-hub-structure", "2.9-structure", "course/modules/FC/FC1/index.html (lines 1-176, read in full)", P,
    "Read in full: six objectives (lines 47-54), prerequisites (57-65), placement section.quiz#placement with nine items (67-133; class=\"item\" count 9), lessons card-grid with L01-L05 links (139-143), ladder with four rung-title entries in order (147-157), data status (159-162), core reading (164-171). Order as BUILDER_RULES 4.1. Objective 3 (line 50) and the L03 card (line 141) read 'customer-buy volume', matching Definition 2.1 W in L03 line 88.")
row("a-r1-hub-hours", "2.9-hours", "index.html line 29, lines 39-41; L01-L03 line 2", P,
    "index.html line 29: data-hours-lessons=\"50\", data-hours-project=\"20\" (sum 70 = curriculum FC1 hours, curriculum/curriculum.json line 7730). Split bar 71.4% / 28.6% (50/70=71.43%, 20/70=28.57%); line 41 '28.6% of the 70 module hours'. L01, L02, L03 data-hours=\"10\" (line 2 each); five lessons x 10 = 50.")
row("a-r1-hub-placement-arithmetic", "2.2-numbers", "index.html lines 69, 72-131", P,
    f"Recomputed in ledgers/FC1/scripts/FC1-a-r4/numbers_fc1a_r4.py -> {R}numbers_fc1a_r4.out (81 OK, 0 BAD): 7/9 = 77.8% (below the 80% bar; 8/9 = 88.9% passes); 110/1.1 = 100; 1 + 1/2 + 1/4 = 1.75; 100 - P = P - 20 gives P = 60 and q = 40; 1000 x 1.05^2 = 1102.50; coupon 10000 x 500/10000 = 500; period-3 flow 500 + 10000 = 10500. Every explain line agrees.")
row("a-r1-hub-lesson-titles", "2.9-structure", "index.html lines 139-141 vs L01/L02/L03 h1 (line 35)", P,
    "Card titles equal each lesson's h1 verbatim: 'Money, Banks and Financial Intermediaries', 'Markets, Exchanges and the Instrument Taxonomy', 'Dealers, Market Makers and the Bid–Ask Spread'. Card bodies match the lesson content (read in full this round).")
row("a-r1-hub-prereq-titles", "2.9-structure", "index.html lines 35, 59-62; curriculum/curriculum.json", P,
    "curriculum/curriculum.json line 7728 FC1 title 'The Financial System, Markets & Instruments'; line 6224 P0.1 'How to Study This Program'; line 7340 E1 'Microeconomics' (grepped this round). The hub uses the same strings. Prerequisite links use concept anchors only (index lines 61-62).")
row("a-r1-hub-reading-and-year", "2.1-citations", "index.html lines 164-171 (data-cite keys), line 166 (text)", P,
    "data-cite keys mishkin2021economics and harris2002trading exist in references/references.json (verify_refs offline: 0 problems). Registry years: harris2002trading 2002 (Crossref); mishkin2021economics 2021 (Open Library). The hub renders the registry record and states no year of its own. Line 166 names McLeay, Radia & Thomas (2014) as not in the registry and not cited; grep: no FC1 slice page cites it. Grep of course/ shows the two keys are cited only in FC1 pages (L03 line 564 and L04/L05 at book level, no page, table or figure locator).")
row("a-r1-hub-rung-claims", "2.6-project", "index.html lines 149-154 vs course/modules/FC/FC1/project.html lines 42-47", P,
    "project.html is byte-identical since 8196077d (git diff stat shows no change). Hub rung 1 'a fully solved set of SIMULATED cash instruments ... coupon cash flow of a bond' vs project rung 1 'one bond and one trade, both simulated (not market data)'; hub rung 2 'the discount exponent and the trade's cash flow, with its two blanks' vs project rung 2 'fill in the two blanks, the discount exponent ... and the trade's cash flow. It is graded instantly.'; rung 4 'not graded' in both; skip rule identical to project.html line 44.")
row("a-r1-hub-data-status", "2.8-data", "index.html lines 159-162", P,
    "Text 'No dataset is used' agrees with the grep this round: no data-files, assets/data or data-chart marker on any slice page; labs are typed-in or seeded (L03 seed 2026, labelled SIMULATED at its hypothesis, L03 line 168).")
row("a-r1-l01-example-3.3-numbers", "2.2-numbers", "L01.html lines 122, 127, 403, 459; Lab 1 Part A", P,
    f"{R}numbers_fc1a_r4.out: S_1 = 1900, S_2 = 2710; S_10 = 1000 x (1 - 0.9^11)/0.1 = 6861.8940391 exactly (68618940391/10^7); cents half up 686189; multiplier 6.8619 to four places; 6.8619 x 1000 = 6861.90 (Remark 3.4); limit 10000. All OK.")
row("a-r1-l01-prop-2.2", "2.4-mathematics", "L01.html lines 88-96", P,
    "Statement under Assumption 2.0 (A1 X_t = rho D_t, A2 l_t = D_t - X_t). Proof: X_t + l_t = rho D_t + (1 - rho) D_t = D_t, summed over t = 0..n. Re-derived by hand; no hypothesis missing.")
row("a-r1-l01-prop-3.1", "2.4-mathematics", "L01.html lines 102-113 (statement line 104)", P,
    f"Statement assumes Assumption 2.0 with d > 0 (the standing Section 2 setup, line 84). Closed form = geometric sum (q = 1 - rho, q != 1 since rho > 0); limit d/rho for 0 < rho <= 1; rho = 1 gives S_n = d. numbers_fc1a_r4.out: closed form equals partial sums for n = 0..24 and rho in {1/10, 1/2, 1/5, 1/4, 1}: OK.")
row("a-r1-l01-prop-3.5", "2.4-mathematics", "L01.html line 132 (statement), line 137 (proof)", P,
    f"Re-verified. Statement (line 132) now assumes Assumption 2.0 with d > 0, A2' and A1 with 0 < rho <= 1. Proof: D_{{t+1}} = phi(1-rho) D_t; kappa = phi(1-rho) <= 1-rho < 1; 1-kappa-rho = (1-rho)(1-phi) >= 0; equality iff phi = 1 or rho = 1. Identity d/rho - d/(1-kappa) = d(1-rho)(1-phi)/(rho(1-kappa)) and the sign hold on a 36-point grid ({R}numbers_fc1a_r4.out: 'identity and sign on grid: True'). The equality clause needs d > 0 (d = 0 gives 0 = 0), which the statement now states. Residual omissions are tracked in a-r1-key-rows-1-6, a-r1-l01-card-c153-locator and a-r4-l01-canon-bullet-prop35.")
row("a-r1-l01-prop-4.1", "2.4-mathematics", "L01.html lines 149-162 (Assumption 4.0, Prop 4.1, proof)", P,
    "Assumption 4.0 gives lambda >= 0, A = K + E, deposits fixed at K. Proof: assets A - lambda = K + E - lambda; by Remark 1.2 equity = (K + E - lambda) - K = E - lambda; nonnegative iff lambda <= E. Re-derived by hand; Part D checked in numbers_fc1a_r4.out.")
row("a-r1-l01-problems", "2.4-mathematics", "L01.html lines 349-446 (M1-M3, P1-P3, E1-E3, R1-R3)", P,
    "Re-verified; the round-3 FAILs are fixed. M1 (reserves 100, loan 400, D_1 400), M2 (1850; 800, 600, 450), M3 (-20; test fails) correct. P1 and P2 and R1 and R3 now state d > 0 (lines 376, 383, 426, 440). P2 'unbounded above has no finite limit' correct. E1 (686189 cents, 6.8619), E2 (181818/1000000 = 0.181818; 2/11; 18.18 percent with base stated), E3 (100) correct. R1 bound d/c and R3 (d/rho > 0) correct. Evidence in numbers_fc1a_r4.out.")
row("a-r1-l01-quiz", "2.4-mathematics", "L01.html lines 466-541 (Q1-Q10)", P,
    f"Re-derived keys: Q1 100; Q2 800; Q3 n+1 (S_n/d at rho = 0; defined since d != 0 is the Section 2 setup); Q4 1.75; Q5 10000; Q6 'smaller' with d > 0 in the prompt (line 504), explanation line 510 = d(1-rho)(1-phi)/(rho(1-kappa)) > 0; Q7 residual; Q8 40; Q9 'None'; Q10 700. All agree ({R}numbers_fc1a_r4.out).")
row("a-r1-l01-misconceptions-canon", "2.9-prose", "L01.html lines 313-341 (misconceptions 328-339; canon bullets 316-321)", P,
    "Misconceptions 1-3 (lines 328-339): 1000 + 900 = 1900 (printed 1.9000, 190000 cents in twin output); 6.8618940391 printed as 6.8619; equity is the residual (Definition 1.1). Canon bullets 2-4 (lines 319-321) correct. Canon bullet 1 (line 318) is the blocking row a-r4-l01-canon-bullet-prop35, which this row does not cover.")
row("a-r1-l01-lab-hypothesis-interpretation", "2.5-labs", "L01.html lines 171 and 310 vs twin output (expected block lines 279-309)", P,
    "Hypothesis: Part A partial sums True, multiplier 6.8619, limit 10 (printed 10.0000 as 1/reserve ratio; the interpretation says the lab does not compute a limit, which matches twin lines 226-227); Part B True, True; Part C 181818 vs 1000000 cents (printed 181818 and 1000000); Part D 50, 0, -50 and sign test True, True, False. Note (not a finding): Part B's balance is true by construction (twin loans = deposits minus reserves); the page does not present it as an independent test.")
row("a-r1-l01-key-rows-1-6", "2.3-grades", "L01.html lines 454-459 (rows 1-6)", F,
    "Rows 1, 2, 4, 5, 6 now carry their hypotheses: row 2 (line 455) 'assuming Assumption 2.0 with d > 0 and rho > 0'; row 4 (line 457) 'For rho = 0 and d > 0'; row 6 (line 459) Example 3.3, T with the Example as basis (ruling 13). Row 3 (line 456) 'Proved in Section 3, assuming A2' and d > 0' omits A1 with 0 < rho <= 1, which Proposition 3.5 (line 132) states and which the rho in d/rho needs. Row 1 (line 454) T, Proposition 2.2, Section 2 PASS.",
    "Line 456, source cell: change to 'Proved in Section 3, assuming A2&prime;, A1 with 0 &lt; &rho; &le; 1, and d &gt; 0'.")
row("a-r1-l01-why-it-matters", "2.9-prose", "L01.html line 51", P,
    "81 words by the scan (limit 120). Forward reference 'defined in Section 1, Definition 1.1' is explicit and the definition is at line 59. Accepted under the round-3 convention for a why-it-matters paragraph.")
row("a-r1-l01-grade-lab-row7", "2.3-grades", "L01.html line 460 (key-results row 7)", P,
    "Grade C with basis 'Lab 1, Parts A to D (typed-in parameters)'. The row rests only on printed lab output, so C is required by ruling 13.")
row("a-r1-l01-cards-lab-T", "2.7-cards", "cards.json FC1-c014, FC1-c092, FC1-c093, FC1-c125", P,
    f"All four are grade C with basis naming Lab 1 Parts A, C, D and B. Each statement matches {R}twin_page_r4.out and twin_L01 output: Part A True; Part C 181790 and 686189 cents; Part D sign test True, True, False; Part B True, True.")
row("a-r1-l01-card-c153-locator", "2.7-cards", "cards.json FC1-c153 (back)", F,
    "Back: 'Exactly when φ = 1 or ρ = 1, for an initial deposit d > 0 as in Section 2 (Proposition 3.5).' It carries d > 0 but omits A1 with 0 < ρ ≤ 1, which the Proposition 3.5 statement (L01 line 132) and cards c009 and c152 both carry. The round-3 PASS checked only d > 0 and is withdrawn.",
    "Back: change to 'Exactly when φ = 1 or ρ = 1, for an initial deposit d > 0 and A1 with 0 < ρ ≤ 1, as in Section 2 (Proposition 3.5).'")
row("a-r1-l01-cards-other", "2.7-cards", "cards.json, the other L01 cards (c001-c018, c091, c094, c103, c104, c110, c111, c122, c136, c146-c148)", P,
    "Round-3 FAILs fixed: c008, c009, c016 and c152 now state d > 0 as the lesson does. The other L01 cards match the lesson text (ledgers/FC1/scripts/FC1-a-r4/cards_r4.py: 0 duplicate ids, fronts or backs; every number on every L01-L03 card appears in its lesson text). The c153 defect is recorded in a-r1-l01-card-c153-locator.")
row("a-r1-l02-prop-1.4-2.5", "2.4-mathematics", "L02.html lines 71-79, 116-124", P,
    "Prop 1.4 under Assumption 1.3: E and O disjoint with union the n trades, so |E| + |O| = n. Prop 2.5: each entry counted under exactly one value on an axis, so counts sum to n. Re-derived by hand.")
row("a-r1-l02-remark-2.6-P2-P3", "2.4-mathematics", "L02.html lines 126-129 (Remark 2.6), 331-344 (P2, P3)", P,
    "Remark 2.6: an entry with k exposure values pushes the total above n by k - 1 ('one less than the number of exposure values'); for the two-value case by 1, matching Lab 2 Part D (14 for 13). P2: |E| + |O| = n + 1 for the doubly recorded trade, so Assumption 1.3 is needed. P3: |S| - 1 >= 1. All correct.")
row("a-r1-l02-lab-hypothesis-output", "2.5-labs", "L02.html lines 133, 246 vs twin output (lines 229-245) and numbers_fc1a_r4.out", P,
    "Hypothesis: 12 entries well formed; exposure 3, 3, 2, 2, 2; form 6, 6; venue 4, 8; Part C one cash and three derivatives over three exposure classes; Part D rejected and 14 for 13. Each recomputed from the REGISTER literal in numbers_fc1a_r4.py and printed identically by the twin. The 'Lab 2' label is tracked in a-r4-l02-lab-numbering.")
row("a-r1-l02-examples-misconceptions", "2.9-prose", "L02.html lines 253-256 (Example 3.1), 279-289 (misconceptions 1-3)", P,
    "Example 3.1 entries 1, 3, 4, 6 are (cash, exchange), (derivative, exchange), (cash, OTC), (derivative, OTC) as read from REGISTER. Misconception 2: six derivative entries 3, 5, 6, 8, 10, 11 carry all five exposure values; rates carries 5 and 6 (futures on a government bond, interest rate swap). Misconception 3: Part C prints three exposure classes. All correct.")
row("a-r1-l02-problems", "2.4-mathematics", "L02.html lines 299-395", P,
    "M1 rates/derivative/exchange; M2 counts 2, 1, 1, 1, 0 summing to 5; M3 no venue fails the venue reconciliation. P1 c + v = n. P2 and P3 correct. E1 (4 and 8 sum to 12), E2 (3 of 4 exchange entries = 75 percent, base stated), E3 (commodities, equities, rates). R1 three rates entries (4, 5, 6); R2 a third venue type or a rule; R3 FX-times-equity product violates Definition 2.1. All consistent with the register.")
row("a-r1-l02-key-rows-1-4", "2.3-grades", "L02.html lines 404-407", P,
    "Row 1 T Prop 1.4 (Section 1); row 2 T Prop 2.5 (Section 2); row 3 T Remark 2.6 with Lab 2 Part D; row 4 C Example 3.1 with a hand-reading basis (enumeration graded C, not T, per the scope-word rule).")
row("a-r1-l02-grade-lab-row5", "2.3-grades", "L02.html line 408 (key-results row 5)", P,
    "Grade C with basis 'Lab 2, Part B (typed-in register)'. Printed by the lab, not derived by hand on the page: C is correct.")
row("a-r1-l02-cards-lab-T", "2.7-cards", "cards.json FC1-c029, c030, c033, c034, c095, c096", P,
    "c029 exposure counts (C, Part B) and c095 form counts, c096 venue counts (C, Part B) match the twin output; c030 (C) states the hand reading and says Lab 2 Part C does not print the four combinations; c033 (C) hand reading of entries 3, 5, 6, 8, 10, 11; c034 (C, Part C) matches the printed three exposure classes.")
row("a-r1-l02-cards-other", "2.7-cards", "cards.json, the other L02 cards (c019-c028, c031, c032, c115, c116, c120, c127, c149, c150)", P,
    "Each matches the lesson text. c027 and c028 grade T match Prop 2.5 and Remark 2.6 with Problem P3. c115 matches Example 2.4. c150 'A claim with terms' matches the L02 why-it-matters sentence. No duplicate (cards_r4.py).")
row("a-r1-l02-forward-pointers", "2.9-DAG", "L02.html line 270; L04.html line 57 and 84; L05.html lines 58 and 63", P,
    "L02 canon bullet 3 names Lesson 4 (order types and limit order book) and Lesson 5 (clearing and settlement); the dfn elements exist at L04.html:57 (def-order-types), :84 (def-limit-order-book), L05.html:58 (def-clearing-and-settlement). No L02 use of those concepts before a lesson that defines them.")
row("a-r1-l02-why-it-matters", "2.9-prose", "L02.html line 50 (changed this round)", P,
    "Re-verified: 'a list of entries defined in Definition 2.1 (counting rule: Proposition 2.5)'. Definition 2.1 (line 98) defines a register as a finite list of entries. 114 words (limit 120). The 'venue' and 'exchange' words in the paragraph precede Definition 1.1 with the explicit pointer 'This lesson defines the two kinds of market'.")
row("a-r1-l03-prop-2.3", "2.4-mathematics", "L03.html lines 96-106 (statement 97-100, proof 103-106)", P,
    f"Identity re-derived: P = C + I m_n = sum sigma q (p - m_n) = sum sigma q (m_t - m_n) + h V (sigma^2 = 1). {R}numbers_fc1a_r4.out: identity and Remark 2.2 hold on 300 random sequences (sign, mid, shares, closed and open).")
row("a-r1-l03-cor-2.4-remark-2.2", "2.4-mathematics", "L03.html lines 93-116", P,
    "Remark 2.2: I = 0 implies sum sigma q = 0 so V = 2W. Corollary 2.4: all mids equal m, closed, then mid-move term zero, P = hV = 2hW = sW, and P = C since I = 0. Correct. Part A prints 4000 = 4 x 1000 (twin output).")
row("a-r1-l03-example-2.5", "2.4-mathematics", "L03.html lines 118-121, 351, 477; cards c043, c139, c140", P,
    "-9998 x 100 + 9992 x 100 = -600; spread term 2 x 200 = 400; mid-move term (-1)(100)(10000 - 9990) = -1000; 400 - 1000 = -600. 'The mid fell after it bought' matches the mid path (10000 then 9990). Recomputed in numbers_fc1a_r4.out.")
row("a-r1-l03-prop-3.2", "2.4-mathematics", "L03.html lines 148-159 (B1-B4, Def 3.1, Prop 3.2)", P,
    f"Asymmetric profiles: a1 < a2 with a1 > c gives dealer 2 a tie gain at a1; a1 = c gives dealer 1 a tie gain at a2. Symmetric k = 0, 1, 2 equilibria (profits 0, N/2, N; no deviation strictly gains). k >= 3: deviation to a - 1 earns (k-1)N > kN/2 iff k > 2. Brute force on asks 100..140, N = 1000: equilibria exactly (100,100), (101,101), (102,102) ({R}numbers_fc1a_r4.out).")
row("a-r1-l03-R1-three-dealers", "2.4-mathematics", "L03.html lines 445-451 (res-1)", P,
    "(c,c,c) and (c+1,c+1,c+1) equilibria; (c+2,c+2,c+2) not, since the deviation to c+1 wins all N and earns N > 2N/3. Symmetric profiles only, as stated. Correct.")
row("a-r1-l03-lab-output", "2.5-labs", "L03.html lines 167-168, 319-333 vs twin output", P,
    "Hypothesis and interpretation match the expected block: Part A 14 trades, cash 4000 = 4 x 1000 True; Part B terminal mid 10001, spread capture 4000, mid-move term -545, mark-to-mid 3455 = 4000 - 545 True, V = 2000 (total shares 2000); Part C 121 pairs; equilibria (100,100), (101,101), (102,102), symmetric True. Remark 2.6 cross-reference matches.")
row("a-r1-l03-problems", "2.4-mathematics", "L03.html lines 370-467", P,
    "M1 cash 200 = sW = 200; M2 cash -160, hV = 320, mid-move -480, sum -160; M3 spread 30, 0.6 percent; P1 P = hV at terminal mid; P2 dM/dm_n = -sum sigma q = I, zero when closed; P3 correct; E1 matches Part C; E2 -545 with terminal 10001; E3 6/20000 = 0.03 percent; R1 correct; R2 cash 1400, spread term 400, mid-move +1000 (only the mid-move term changes); R3 correct.")
row("a-r1-l03-key-rows", "2.3-grades", "L03.html lines 475-480", P,
    "Row 1 T Prop 2.3; row 2 T Cor 2.4; row 3 T Example 2.5 computed by hand (ruling 13); row 4 T Prop 3.2 (proved for all whole-cent asks); row 5 C (Lab 1 Parts A and B, SIMULATED); row 6 C (Lab 1 Part C, finite grid). Grades match the lesson basis.")
row("a-r1-l03-misconceptions-canon", "2.9-prose", "L03.html lines 336-362 (canon 338-343, misconceptions 349-359)", P,
    "Canon 339 (Example 2.5 gives positive capture and negative profit: correct); 340 (V = 2W only for closed; Prop 2.3 without one mid: correct); 341 (A2 excludes four items: fees, interest, inventory cost, information: correct; Harris cited by key with registry year 2002, no passage claimed: correct); 342 (one tick size). Misconceptions 1-3 match 400, -600, -1000, the trade-count point and (c+1,c+1), (c+2,c+2) equilibria.")
row("a-r1-l03-quiz", "2.4-mathematics", "L03.html lines 490-558 (nine items)", P,
    "Keys recomputed: Q1 a - b; Q2 4; Q3 200; Q4 -1000 (-600 = 400 + M); Q5 'every trade at the terminal mid' (sufficient; 'closed' is not); Q6 121; Q7 (103,103) not an equilibrium with profit 1500 against 2000 by deviating to 102; Q8 1000; Q9 tick. All agree.")
row("a-r1-l03-notation-Q", "2.4-notation", "L03.html Definition 2.1, Remark 2.2, Corollary 2.4, lines 88, 93, 110, 115, 340", P,
    "L03 math has no Q symbol and no \\mathbb{Q}; single-letter symbols C, I, M, N, P, V, W, a, b, c, d, h, i, j, k, m, n, p, q, s, t are defined locally (Definition 2.1 for C, I, P, V, W; B3 for N; Definition 1.2 for m, h, s).")
row("a-r1-l03-references-harris", "2.1-citations", "L03.html lines 341, 564; references/references.json harris2002trading", P,
    "Key harris2002trading exists (verify_refs offline: 0 problems; live unit run: 0 problems). Year 2002 is the registry's own year, as the architect ruling requires. The lesson claims no passage and gives no locator.")
row("a-r1-l03-why-it-matters", "2.9-prose", "L03.html line 51 (changed this round)", P,
    "Re-verified: '(Definition 1.2; mark-to-mid is Definition 2.1)'. Definition 1.2 (lines 61-62) defines the mid m = (a+b)/2 and the half-spread; Definition 2.1 (line 88) defines mark-to-mid. 'Proposition 2.3 in Section 2' sources match. 120 words (limit 120).")
row("a-r1-l03-cards", "2.7-cards", "cards.json, all 39 L03 cards (c035-c055, c097, c098, c105-c108, c112, c113, c117, c128-c131, c137-c140, c151)", P,
    "Each card matches its lesson text (read in full this round). Grades: c037, c041, c042, c050, c055, c112, c139, c140, c151 T; c052, c053, c054, c097, c098 C with SIMULATED or finite-grid basis. No duplicate (cards_r4.py).")
row("a-r1-cards-grade-convention", "2.7-cards", "cards.json, 98 L01-L03 cards", P,
    "Grades T for proved or hand-derived results (Example-based values, ruling 13) and C for values printed by a lab; definitional cards carry no grade. Each card with a basis names a lab part or hand reading.")
row("a-r1-cards-dup-gaps", "2.7-cards", "cards.json FC1-c025, FC1-c033 (round-2 FAIL), full scan", P,
    "ledgers/FC1/scripts/FC1-a-r4/cards_r4.py -> out/cards_r4.out: 98 slice cards; 0 duplicate ids; 0 duplicate fronts; 0 duplicate backs; every number on a card appears in its lesson. Manual near-duplicate review of pairs c006/c103 (balance sheet every stage versus cumulative), c007/c104 (closed form versus limit), c013/c122 (equity after loss versus sign), c041/c151 (identity versus closedness) asks distinct facts. The round-2 FAIL (c025/c033) is cleared.")
row("a-r1-dag-definitions", "2.9-DAG", "L01 dfn lines 59, 81; L02 lines 58, 92; L03 lines 57, 61; L04 and L05 dfn elements", P,
    "Grep this round: each of the six data-concept dfn elements appears once in its lesson (financial-intermediary, bank-money-creation, exchange-vs-otc, asset-class-taxonomy, market-maker, bid-ask-spread). The plain <dfn>tick</dfn> (L03 line 130) has no data-concept and is allowed. The 10 curriculum concepts are defined once across L01-L05 (check_dag passes).")
row("a-r1-prose-future-concepts", "2.9-DAG", "L02.html lines 103, 113, 255, 284, 303, 378, 447, 453, 481; L01 and L03 class=\"concept\" links", P,
    "Grep this round: futures, swap and bond-price words appear in L02 prose and examples only (no data-concept, no link, no dfn), as the Architect default requires for FC2 and FI1 concepts. The only concept links on the slice are bertrand-competition (index line 61, L03 line 37) and geometric-series (index line 62, L01 line 37), both in the closure.")
row("a-r1-define-before-use", "2.9-prose", "L01-L03 and index.html", P,
    "Each of the six slice concepts is defined before its first use within its lesson, with two exceptions that carry explicit forward pointers in the why-it-matters paragraphs (L01 line 51 'financial intermediary'; L03 line 51 'dealer', 'mark-to-mid'). Accepted under the round-3 convention.")
row("a-r1-scope-words", "2.9-prose", "index.html, L01-L03 prose (counts from slice_scan_r4.out)", P,
    "Scope words traced in context: L02 line 407 'all occur' (four-combination enumeration, graded C with basis, not T); L02 line 251 'across the values' (prose); L03 lines 137, 156, 158, 447, 449, 542 'all N shares' (demand and tie rules, definitional); L03 line 333 'all values are whole cents' (integer arithmetic in the lab); L03 line 478 'for all whole-cent asks' (Prop 3.2 proof covers k >= 0 and d >= c); L01 'every stage' (Props 2.2, 3.1 proofs); L01 'any' and 'never' in definitions and remarks (no hidden claim).")
row("a-r1-prose-attributions", "2.9-prose", "index.html line 166; L01 line 545; L02 line 497; L03 lines 341, 564", P,
    "Each page says the lesson cites no registry source or cites a key at book level with no passage locator. No page, table or figure locator is typed for harris2002trading or mishkin2021economics on any FC1 page. The P0.1 explanation attribution in index lines 106 and 120 is a separate row (a-r4-hub-p01-attribution).")
row("a-r1-structure-counts", "2.9-structure", "L01, L02, L03 section lists", P,
    "Each lesson: why-it-matters, core sections 1-4 with Definitions, Assumptions, Propositions, Proofs, Remarks, Examples; inline lab; canon-breaks (4 bullets); misconceptions (3); problem set (3 problems in each of the four tiers, each with a solution); key results (L01 7 rows, L02 5, L03 6); retrieval quiz (L01 10, L02 10, L03 9 items, within 8-15); references.")
row("a-r1-hours-lessons", "2.9-hours", "L01-L03 data-hours and index.html", P,
    "data-hours=10 on L01, L02, L03 (line 2 of each); hub lessons 50 = 5 x 10 (L04 and L05 are other slices).")
row("a-r1-mutants-not-applicable", "2.5-labs", "tests/labs/FC1 twins L01-L03; index.html and L01-L03 have no grader", P,
    "No project grader in this slice, so mutation testing does not apply (ruling 9; VERIFIER 2.6 applies to project graders). Lab-claim mutants were run instead (a-r2-lab-mutants).")
row("a-r2-delta-hunks", "2.9-structure", f"git diff 8196077d..edbb7aa8 for index.html, L01-L03.html, cards.json, tests/labs/FC1, plans/FINAL-ARCHITECT-RULINGS.md", P,
    "Delta: 24 insertions and 24 deletions across index.html (lede line 33; objective 3 line 50; card line 141), L01.html (lines 117, 131, 318, 376, 383, 426, 440, 455-457, 504, 510 plus the 'lowers' sentence at 318), L02.html (line 50), L03.html (line 51), cards.json (c008, c009, c016, c099 [L04, other slice], c152). tests/labs/FC1 unchanged. plans/FINAL-ARCHITECT-RULINGS.md gained rulings 25 and 26. tools/, notation/ and references/ unchanged (git diff stat empty). Every hunk read; diff saved at ledgers/FC1/scripts/FC1-a-r4/slice_delta_8196077d_to_edbb7aa8.diff (227 lines). Ruling 26 applied (see notes).")
row("a-r2-numbers-recompute", "2.2-numbers", "ledgers/FC1/scripts/FC1-a-r4/numbers_fc1a_r4.py", P,
    f"Exact Fraction recomputation of every slice number ({R}numbers_fc1a_r4.out): 81 OK, 0 BAD. Covers Example 3.3, 3.6, E2 and the leakage cents, Prop 3.5 identity on a grid, the L02 register counts, Example 2.5, M1, M2, R2, Q7 and Q8 of L03, cards c010, c011, c014, c043, c053.")
row("a-r2-lab-mutants", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py, L02-1.py, L03-1.py (lab-claim mutants, copies in /tmp/fc1a-r4-mut)", P,
    f"ledgers/FC1/scripts/FC1-a-r4/lab_mutants_r4.py -> {R}lab_mutants_r4.out: three lab-claim mutants each flip the printed claim to False: L01 closed-form exponent (partial-sum claim), L02 well-formed check accepts two values (malformed-entry rejection claim), L03 spread capture doubled (mark-to-mid identity claim). The page's printed claims are sensitive to their defects.")
row("a-r2-cards-near-dup-scan", "2.7-cards", "cards.json, 98 L01-L03 cards", P,
    "cards_r4.py exact duplicate scan (ids, fronts, backs): none. Manual near-duplicate review as in a-r1-cards-dup-gaps: no two cards test the same fact.")
row("a-r3-l01-d-remark-3.2", "2.4-mathematics", "L01.html line 117 (Remark 3.2); also problem P2 lines 383-385", P,
    "Remark 3.2 now reads 'Take d > 0 and set rho = 0'; with d > 0, S_n = (n+1)d unbounded, so no limit. P2 states 'Take d > 0' and the 'unbounded above, so no finite limit' argument is valid.")
row("a-r3-gates-full", "2.9-gates", "ledgers/FC1/scripts/FC1-a-r4/gates_r4.sh (24 commands, output in out/)", P,
    "All 24 commands EXIT=0: check_pages (unit and --all), check_dag (unit and --all), check_projects (unit), run_labs (L01, L02, L03), twins alone under -I -W error, page_smoke (index, L01-L03), ruff check, ruff format --check, mypy --no-incremental, pytest test_labs -k FC1, pytest page_checks/page_smoke/refs/run_labs, pytest test_docs_figures, verify_refs --offline, verify_refs --unit FC1, fetch_data --check, build_site --check, collect-only FC1 = 8. Not run: run_graders (no grader in slice a), mutate_graders (no project grader in slice a), render_curriculum (no curriculum change in the delta).")

# new rows
row("a-r4-l01-canon-bullet-prop35", "2.4-mathematics (missing hypothesis)", "course/modules/FC/FC1/L01.html line 318 (canon-breaks bullet 1)", F,
    "The bullet says 'Proposition 3.5 shows that one departure, leakage, does not raise the limit, and lowers it when φ < 1 and ρ < 1.' The strict 'lowers' needs d > 0: at d = 0 both limits are 0, so no reduction occurs. Proposition 3.5 (line 132) states d > 0 and the bullet does not restate it. Standing Section 2 setup (line 84) is the only support.",
    "Line 318: change 'and lowers it when φ < 1 and ρ < 1' to 'and, for d > 0, lowers it when φ < 1 and ρ < 1'.")
row("a-r4-hub-p01-attribution", "2.9-prose (attribution not read; LOW)", "course/modules/FC/FC1/index.html lines 106 and 120 (placement explanations for Pq5 and Pq7)", F,
    "Both explanations attribute the grade definition to '(P0.1, evidence grade)'. No P0.1 module page exists in course/modules/ (no P directory); curriculum/01-foundations.yaml:16 labels the concept only 'Evidence grade (T/A/B/C/D/X)' without the definition. The C definition is confirmed at BLUEPRINT.md:161 and in this lesson's own grade legend (L01.html lines 43-46, L02.html line 45). Severity LOW: wording and attribution only; no grade or number is wrong.",
    "Lines 106 and 120: delete '(P0.1, evidence grade)' from each explanation, or replace it with '(the grade legend on each lesson page)'.")
row("a-r4-l02-lab-numbering", "2.9-prose (presentation; LOW)", "course/modules/FC/FC1/L02.html lines 128, 132, 251, 255, 260, 284, 288, 295, 351, 358, 365, 406-408, 437, 442, 497", F,
    "The lesson's only lab is twin lab-FC1-L02-1 (its first lab), but its heading and 16 later references say 'Lab 2'. L03's lab is 'Lab 1' and L01's is 'Lab 1'. The label 'Lab 2' also names the project's completion problem (project.html line 105), so a learner can read two different labs as one. Severity LOW: presentation only; every printed value is correct.",
    "In L02.html rename the heading 'Lab 2 · A consistency check on a typed-in register' to 'Lab 1 · …' and every 'Lab 2' in the lesson text to 'Lab 1'. The twin id lab-FC1-L02-1 and the lab output do not change.")

fragment = {
    "unit": "FC1",
    "slice": "FC1-a",
    "round": 4,
    "verifier": "Claude Haiku 5.5 independent verifier, FC1-a round 4 (final full verification for the S-tagged slice per ruling 26; did not build FC1; read verifier-rules.md, VERIFIER_RULES.md, CLAUDE.md, BUILDER_RULES.md, plans/FC1-build-plan.md with its Architect decisions, plans/FINAL-ARCHITECT-RULINGS.md rulings 1-26, and the round-3 fragment as context only; did not trust its PASS rows)",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d (round-3 pin). Slice delta 8196077d..edbb7aa8 read hunk by hunk: ledgers/FC1/scripts/FC1-a-r4/slice_delta_8196077d_to_edbb7aa8.diff (227 lines).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-FC1-a",
    "scratch": "/tmp/fc1a-r4-mut/ (lab-claim mutant copies only)",
    "verified_at": "2026-11-09T07:59:10+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [
        {"id": "lab-mut-r4-L01-closed-form-exponent", "description": "Lab 1 twin closed form uses (1-rho)^n instead of (1-rho)^(n+1): the exact partial-sum check prints False.", "killed_by": "L01 printed claim 'the partial sums equal the closed form exactly for n = 0 to 10: True' flips to False"},
        {"id": "lab-mut-r4-L02-well-formed-accepts-two-values", "description": "Lab 2 twin well-formed check accepts two values on one axis: the malformed-entry rejection prints False.", "killed_by": "L02 printed claim 'malformed entry rejected: True' flips to False"},
        {"id": "lab-mut-r4-L03-spread-capture-doubled", "description": "Lab 3 twin spread capture doubled (2*half*V): the mark-to-mid identity prints False.", "killed_by": "L03 printed claim 'mark-to-mid P&L equals spread capture plus mid-move term: True' flips to False"},
    ],
    "registry_flags": [
        "harris2002trading: curriculum yaml 385 says 2003; registry (Crossref) says 2002. Pages cite the key with the registry year only (architect ruling). No record edit.",
        "mishkin2021economics: curriculum yaml 384 says 2022; registry (Open Library) says 2021. The hub renders the registry record; no FC1 lesson cites it.",
        "McLeay, Radia & Thomas (2014), Bank of England QB Q1: not in references.json; not cited on any slice page (REFERENCE_REQUEST outstanding per plan section 6).",
    ],
    "freshness_flags": ["none required: FC1-a has no debate brief (the curriculum entry has no debate key) and cites no 2025-2026 work."],
    "notes": [
        "Scope: slice a = hub index.html, L01.html, L02.html, L03.html, twins tests/labs/FC1/lab-FC1-L01-1.py, L02-1.py, L03-1.py, and the 98 L01-L03 cards in cards.json (the file has 155 cards; the 57 L04-L05 cards and the L04/L05 pages belong to other slices and were not verified here, except where the hub or an L01-L03 row cites them).",
        "Round 4 re-verified every round-3 row from scratch at edbb7aa8 (no carry was needed because every cited subject was re-read). Row ids are kept: 77 round-3 ids, plus three new (a-r4-l01-canon-bullet-prop35, a-r4-hub-p01-attribution, a-r4-l02-lab-numbering). Round-3 status changes: a-r1-l01-prop-3.5, a-r1-l01-problems, a-r1-l01-quiz, a-r1-l01-cards-other, a-r3-l01-d-remark-3.2 are PASS now (round-3 d>0 defects fixed). a-r1-l01-key-rows-1-6 and a-r1-l01-card-c153-locator are FAIL now (their d>0 part is fixed, but A1 0<rho<=1 is missing: a round-3 PASS on c153 was incomplete).",
        "Ruling 26 severity: blocking-kind rows (missing hypothesis) are a-r4-l01-canon-bullet-prop35, a-r1-l01-key-rows-1-6 and a-r1-l01-card-c153-locator. LOW rows (attribution wording, presentation) are a-r4-hub-p01-attribution and a-r4-l02-lab-numbering. Round 4 is the last full verification for this S-tagged slice: each row above is fixed and the unit gate re-run, not re-verified; the LOW rows, if deferred by a fixer, go to plans/KNOWN-ISSUES.md with these ledger ids (that file does not exist yet at this pin).",
        "Lab twins are demonstrations, not graders (ruling 9): no mutation score is claimed for them. Three lab-claim mutants were run and killed (a-r2-lab-mutants).",
        "Not run: run_graders.py and mutate_graders.py (no FC1-a grader); render_curriculum.py and fetch_data snapshot rebuild (no curriculum or data change in the delta); Chromium screenshots beyond page_smoke (the slice has no figures). The McLeay citation is not checked (not cited).",
        "Advisory, not rows: the L01 Part B balance check is true by construction (loans defined as deposits minus reserves, twin lines 238 and 241); the page does not claim otherwise. L01 quiz Q3 uses S_n/d and so presupposes d != 0, the Section 2 setup; not a missing hypothesis of the answer.",
    ],
    "summary": "",
}
pass_n = sum(1 for r in rows if r["status"] == P)
fail_n = sum(1 for r in rows if r["status"] == F)
fragment["summary"] = (
    f"FC1-a round 4 at edbb7aa8: {len(rows)} rows = 77 round-3 ids kept plus 3 new. {pass_n} PASS, {fail_n} FAIL, 0 UNVERIFIABLE. "
    "Verdict FAIL. Blocking-kind (missing hypothesis): a-r4-l01-canon-bullet-prop35 (L01 line 318, 'lowers' needs d > 0), "
    "a-r1-l01-key-rows-1-6 (L01 line 456, row 3 omits A1 0 < rho <= 1), a-r1-l01-card-c153-locator (FC1-c153 back omits A1). "
    "LOW (attribution and presentation): a-r4-hub-p01-attribution (index lines 106, 120), a-r4-l02-lab-numbering (L02 'Lab 2' labels). "
    "All lab twins, page code, expected blocks, gates, numbers (81 OK), cards integrity, notation and banned-phrase scans pass."
)
out = ROOT / "ledgers/FC1/FC1-a.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", pass_n, "fail", fail_n)
