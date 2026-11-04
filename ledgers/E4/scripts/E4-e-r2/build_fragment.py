# ruff: noqa: E501
"""Build the round-2 slice-e ledger fragment (ledgers/E4/E4-e.json) from the rows the checks established.

Usage (from the checkout root): python -I ledgers/E4/scripts/E4-e-r2/build_fragment.py
"""

from __future__ import annotations

import json
from pathlib import Path

SCRIPTS = "ledgers/E4/scripts/E4-e-r2"
CARDS = "course/modules/E/E4/cards.json"
SCAN = f"{SCRIPTS}/card_scan.py"
DRIVER = f"{SCRIPTS}/run_slice_e_r2.sh"
PASS = "PASS"
FAIL = "FAIL"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict[str, str]:
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        out["fix"] = fix or ""
    return out


rows: list[dict[str, str]] = [
    row(
        "E4-e-r1-scan-structure",
        "2.7-scan",
        CARDS + " (all 211 entries)",
        PASS,
        f"{SCAN} {CARDS} references/references.json, output at round 2: cards=211; ids sequential E4-c001..E4-c211 "
        "(True); 0 duplicate ids, fronts, backs, normalised fronts; cards per lesson L01 16, L02 22, L03 14, L04 21, "
        "L05 26, L06 30, L07 21, L08 38, L09 23 (sum 211); grades T 143, C 14, none 54; the one cite key "
        "muth1961rational exists in references/references.json; every T or C card has a basis. Delta from pin "
        "1c1645f3: E4-c022 onward edited and E4-c211 added, all re-read.",
    ),
    row(
        "E4-e-r1-card-references",
        "2.7-references",
        "cards.json front/back vs L01-L09 text",
        PASS,
        f"{SCRIPTS}/card_refs.py {CARDS} scratch/txt (scratch/txt written by {SCRIPTS}/html_to_text.py from each "
        "course/modules/E/E4/L0N.html): references checked=193 missing=0. CROSS items: E4-c054 'Assumption A3' and "
        "E4-c074 'Assumption A3' (L04 line 0021 and L05 line 0019-0021 print the bullet form '- A3 (...)' under the "
        "Assumptions heading, which is the item the card names); E4-c075/c076 'Assumption A1/A2' are the bullet items '- A1 (parameters)' "
        "and '- A2 (linear forecasts)' of L05.txt lines 0019-0020, read in L05; E4-c176 'Definition 7.1' printed in L07 line 0018 (cross-lesson, read "
        "in L07 and accepted). Each item was read in its own lesson.",
    ),
    row(
        "E4-e-r1-numbers",
        "2.2-numbers",
        "cards.json numeric tokens vs lesson text",
        PASS,
        f"{SCRIPTS}/card_numbers.py {CARDS} scratch/txt: numeric tokens checked=338 missing=1. The one miss, 3/32 in "
        "E4-c037, is typeset as \\tfrac{3}{32} in scratch/txt/L02.txt line 0078 (Misconception 2), and 1/8 - 1/32 = 3/32 "
        "by hand. The 28 OTHER lines in scratch/driver.out are LaTeX-typeset fractions (\\tfrac12, \\tfrac{1}{12}, \\tfrac34) or values printed "
        "in another E4 lesson; each was matched by reading the lesson line. The block values were re-derived by "
        f"{SCRIPTS}/indep_checks.py (stdlib Fractions, no lab import): 'FAILS: 0', 90 OK lines, covering L01 340/3, 56, "
        "596/3, 235/4; L02 prices, demands, wealth 9/16 and 7/16, ratios 16/9 and 16/7, 3/32; L03 MRS 4, 2, 1/2 and "
        "the 125-grid counts 0 and 2 by brute force; L04 ranks; L05 fixed points, ratios -1/4, -1, -3/2; L06 theta, "
        "b = 7/9, V_U = 2/3, x_I = 1/7, residual -9/85; L07 rho^2 and Var(p) sweeps; L08 G(0), G(1) = ln(5/3)/4, "
        "Corr^2 at lam*; L09 counts 500, 625, 15625.",
    ),
    row(
        "E4-e-r1-cite-muth1961rational",
        "2.1-citation",
        "references/references.json entry muth1961rational; E4-c099; course/modules/E/E4/L05.html line 295",
        PASS,
        "Registry: title 'Rational Expectations and the Theory of Price Movements', Muth, John F., Econometrica 29(3), "
        "p. 315, 1961, doi 10.2307/1909635, status verified (crossref). Plain curl of "
        "https://api.crossref.org/works/10.2307/1909635 at round 2 returned the same title, container Econometrica, "
        "volume 29, issue 3, page 315, author Muth John F., published-print 1961-7. L05.html line 295 cites the key with "
        "data-locator='title'. E4-c099 back (title only; no result of the paper used) matches that claim span. The "
        "round-1 defect (front said 'the model's source') is fixed: the front now reads 'Which registry key does L05 "
        "cite, and what is it used for?'.",
    ),
    row(
        "E4-e-r1-verify-refs",
        "2.1-registry",
        "references/references.json (whole registry, offline integrity)",
        PASS,
        "Command: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0. "
        "git diff 1c1645f3 67c47689 -- references/ is empty, so the registry is byte-identical to round 1. The live "
        "--unit E4 run was not executed (one plain curl of the Muth DOI instead).",
    ),
    row(
        "E4-e-r1-check-pages",
        "2.9-structure",
        "tools/check_pages.py --unit E4 (includes check_cards)",
        PASS,
        "Command: .venv/bin/python tools/check_pages.py --unit E4 -> 'check_pages E4: PASS', exit 0. Also "
        "tools/check_dag.py --unit E4 -> 'check_dag E4: PASS', exit 0. Covers cards.json ids, lesson existence, grades and "
        "registry keys; card content is covered by the rows below.",
    ),
    row(
        "E4-e-r1-run-labs",
        "2.5-labs",
        "tests/labs/E4/lab-E4-L0[1-9]-1.py (the labs whose printed values the cards cite)",
        PASS,
        f"Command: .venv/bin/python tools/run_labs.py --unit E4 -> 'run_labs E4: PASS (12/12)', exit 0. Then "
        f"sh {SCRIPTS}/run_twins.sh (python -I -W error for each of the nine twins) exit 0, output in "
        "scratch/twins.out. Every number a card quotes from a lab was matched to that output: L01 340/3, 56, 596/3, "
        "235/4, False flag; L02 residuals 0, ratios 16/9 and 16/7, demand_unchanged True; L03 0 and 2 grid improvements, "
        "states 1-2, 1-3, 2-3 MRS 4, 2, 1/2; L04 ranks 2 and 3, augmented ranks 2, 3, 3; L05 fixed points (4,-3/10), "
        "(5/2,-3/16), (2,-3/20), ratios -1/4, -1, -3/2, path values, equals_fixed_point True; L06 16 grid points, "
        "-9/85, 1/7, seed 6 slopes 0.426617 and 0.761928 with tolerances; L07 rho^2 sweeps 4/9..1/66, Var(p) 729/1444 and "
        "35937/4802, lam sweep 1/6, 1/3, 9/22, a sweep 4/9, 1/3, 1/6, seed 7 0.330625; L08 gain(0) 0.173287, gain(1) "
        "0.127706, lam* 0.657828572 gap 1.83e-15 Corr 0.088941, boundary gaps 7.71e-03 and -6.71e-03, Part D interior "
        "count 0; L09 500, 0, 625, 0, 15625 and the witness bet.",
    ),
    row(
        "E4-e-r2-delta",
        "2.7-delta",
        "git diff 1c1645f3 67c47689 -- course/modules/E/E4 tests/labs/E4",
        PASS,
        "Every hunk read: cards.json (E4-c008 onward edited, E4-c211 added); lesson HTML L01-L09, index and project diffs "
        "(282 insertions, 275 deletions), read hunk by hunk; 23 lab twin files. Card-relevant lesson changes: the gamma to "
        "varsigma renaming in L05 (and its uses in L05 to L08 prose and Lab 1), Lemma 6.2 now assumes A3 (price taking), "
        "L02 Part E wording (lesson and lab), L03 states numbered 1 to 3 (Lab 3 prints states 1 2, 1 3, 2 3, matching "
        "Example 3.6), L06 Assumption G (i) and (ii), L07 Lemma 7.4 coefficient b, L08 Lemma 2.2 variable D renamed Z and "
        "Res 2 and Lemma 4.5 citing Proposition 4.1, L09 meet wording in lab and lesson. Each rendered lesson was also read in full "
        "(scratch/txt). Every card whose text or lesson changed was re-checked against the current text; no round-1 PASS row "
        "was carried.",
    ),
    row(
        "E4-e-r2-notation",
        "2.4-notation",
        "cards.json symbols vs notation/notation.json",
        PASS,
        f"Command: .venv/bin/python -I {SCRIPTS}/notation_check.py. notation/notation.json registers 8 symbols (T, Phi, "
        "gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). Output: standalone T in card text 0; the 3 occurrences of the letter T in "
        "cards are superscript transposes theta^T and A^T (E4-c053, E4-c055), an operator, not the registered symbol T "
        "(number of observations); no Greek gamma, Phi, gamma_3, gamma_4, R^*, R_f or Q in any card. Local symbols "
        "varsigma, varpi, nu, kappa, N, G, D_I, D_U are defined in their lessons (L05.txt lines 0019-0025 and 0050; L08.txt "
        "lines 0050, 0055-0056, 0076-0077, 0086).",
    ),
    row(
        "E4-e-r2-twins-isolated",
        "2.5-labs",
        "tests/labs/E4/lab-E4-L0[1-9]-1.py run with python -I -W error",
        PASS,
        f"Command: sh {SCRIPTS}/run_twins.sh > scratch/twins.out; exit 0, 192 lines, all nine twins print their Parts A to "
        "F without warnings.",
    ),
    row(
        "E4-e-r2-indep-checks",
        "2.2-numbers",
        f"{SCRIPTS}/indep_checks.py (re-derives the card numbers from the closed forms)",
        PASS,
        f"Command: .venv/bin/python -I {SCRIPTS}/indep_checks.py -> 'FAILS: 0 []', exit 0. Re-derives values the cards "
        "state without importing the lab twins (see E4-e-r1-numbers for the list).",
    ),
    row(
        "E4-e-r2-ruff-scripts",
        "lint",
        f"{SCRIPTS}/*.py",
        PASS,
        "Command: .venv/bin/ruff check ledgers/E4/scripts/E4-e-r2 -> 'All checks passed!'; .venv/bin/ruff format --check "
        "ledgers/E4/scripts/E4-e-r2 -> '5 files already formatted'.",
    ),
    row(
        "E4-e-r2-cards-211",
        "2.7-card",
        "cards.json E4-c211 (L09, Problem Res 2)",
        PASS,
        "Front: two trivial-partition states, priors p != r in (0,1). Back: x(H)=1, x(L)=-t, t = theta/(1-theta), "
        "theta=(p+r)/2, and the label swap when p<r. Checked in indep_checks.py (L09 two-prior section, four (p,r) pairs, "
        "both receipts strictly positive: 1/3 and 1/3, 11/19 and 11/19 after the swap, 1/5 and 1/5, 4/5 and 4/5). L09.txt "
        "Res 2 solution gives the same bet and the same swap argument.",
    ),
    row(
        "E4-e-r2-grades",
        "2.3-grades",
        "cards.json grades vs BLUEPRINT section 3 and the lesson key-results tables (L01 to L09)",
        FAIL,
        "Re-graded every graded card against BLUEPRINT section 3 (T: theorem proved on the page; C: finite check or single "
        "sample) and against the key-results table of its lesson (scratch/txt/L0N.txt). All lesson key-results rows agree "
        "with the card grades except L07 line 0130, which grades the base-instance rho^2 = 1/3 and the sweep values as C, "
        "while cards E4-c141 to E4-c145 are T. The card grade is defensible under BLUEPRINT section 3 (each value is an exact "
        "instance of Proposition 7.6 or 7.7), but cards must agree with the current lesson text (VERIFIER 2.3, BUILDER_RULES 7). "
        "Every other graded card is consistent with BLUEPRINT section 3 and with its lesson: T cards are theorem-level statements "
        "proved on the page, C cards are lab finite checks or SIMULATED draws (E4-c033 to c035 and E4-c047 are exact "
        "identities that the lesson grades T in its key results). Ungraded cards are definitions, assumptions and "
        "misconceptions (no grade field, BUILDER_RULES 7). Note: L09 References says the counts of Lab 1 carry no grade of "
        "their own, while E4-c201 and c202 are graded C; this is not scored as a failure.",
        "Choose one and make card and lesson agree. Option (a): regrade E4-c141, E4-c142, E4-c143, E4-c144 and E4-c145 to C "
        "with basis 'Lab 1, Parts A to E (finite check, exact)'. Option (b, preferred because each value is an exact instance "
        "of Proposition 7.6 or 7.7): split course/modules/E/E4/L07.html key-results row 'The base-instance value rho^2 = 1/3, "
        "and the sweep values' into two rows: the base and sweep values graded T with basis 'Proposition 7.6 and Proposition "
        "7.7 (exact instances); Lab 1, Parts A to D', and the seeded check (Part F) graded C. Then re-run check_pages --unit "
        "E4 and this round's indep_checks.py.",
    ),
    row(
        "E4-e-r1-card-E4-c016",
        "2.7-card",
        "cards.json E4-c016 (L01); L01 Misconception 3 (scratch/txt/L01.txt line 0073); tests/labs/E4/lab-E4-L01-1.py main()",
        PASS,
        "Back now says Lab 1 checks its unequal probabilities once, at the start of main(), before Part A. Checked: "
        "lab-E4-L01-1.py main() calls check_probabilities(STATE_PROBABILITIES) before Part A, and Part A uses only the "
        "claim. Round-1 FAIL (Part A was said to use the unequal probabilities) is fixed. Proposition 1.4 uses no "
        "probability (L01.txt line 0030).",
    ),
    row(
        "E4-e-r1-card-E4-c099",
        "2.7-card",
        "cards.json E4-c099 (L05); course/modules/E/E4/L05.html line 295 and L05.txt line 0065",
        PASS,
        "Front now asks which key L05 cites and what it is used for; back (title only, no result used) matches "
        "L05.txt line 0065. Round-1 FAIL (front claimed the key is the model's source) is fixed.",
    ),
    row(
        "E4-e-r1-card-E4-c176",
        "2.7-card",
        "cards.json E4-c176 (L08); course/modules/E/E4/L08.html Research problem Res 1 solution (scratch/txt/L08.txt line 0201)",
        FAIL,
        "The card back says: 'The correlation is undefined, because Var(p) = 0 (Definition 7.1 requires positive "
        "variances).' Under sigma_u^2 = 0 and lambda = 0, p* = vbar - a sigma_v^2 u is constant, so Var(p) = 0 and "
        "Corr is undefined; the card is correct. The lesson text disagrees: L08.txt line 0201 (Res 1 solution, the "
        "sentence 'There the price is vbar - a sigma_v^2 u, a function of u alone, which is independent of v, so "
        "Corr(v,p)^2 = 0.') states the correlation is zero. The card and the current lesson text must agree (BUILDER_RULES "
        "7; VERIFIER 2.7). Round-1 FAIL reason (the card claimed zero correlation) is fixed in the card only.",
        "Change L08 Res 1 solution (course/modules/E/E4/L08.html, the sentence ending 'so Corr(v,p)^2 = 0') to say the "
        "correlation is undefined because Var(p) = 0 under sigma_u^2 = 0 (Definition 7.1 requires positive variances). "
        "Keep E4-c176 as it is. Re-run check_pages --unit E4 and this slice's indep check after the lesson edit.",
    ),
    row(
        "E4-e-r1-card-E4-c206",
        "2.7-card",
        "cards.json E4-c206 (L09); L09 Misconception 1 (scratch/txt/L09.txt lines 0059-0060); tests/labs/E4/lab-E4-L09-1.py Part B",
        PASS,
        "Back now cites Corollary 2.3 correctly: a bet both traders accept strictly at omega* has a state of the meet where one "
        "of them has a negative posterior, so acceptance cannot be common knowledge on the meet. Lab Part B output: 500 "
        "strict bets at state 1, 0 of them nonnegative on the meet. Round-1 FAIL is fixed.",
    ),
    row(
        "E4-e-r1-cards-001-010",
        "2.7-cards",
        "cards.json E4-c001..E4-c010 (L01)",
        PASS,
        "Each card read against L01.txt: Definitions 1.1, 1.2, 1.3, 1.6, 1.9; Propositions 1.4, 1.7, 1.8, 1.10 and A1, A2. "
        "Hypotheses match (E4-c007 and E4-c008 carry A1 and A2). Numbers per the rows above.",
    ),
    row(
        "E4-e-r1-cards-011-020",
        "2.7-cards",
        "cards.json E4-c011..E4-c020 (L01, L02)",
        PASS,
        "L01 cards c011-c016 checked against Lab 1 output (340/3, 56, 596/3, 235/4, flags) and L01.txt Misconceptions 1 to 3 "
        "(lines 0066-0073). L02 cards c017-c020 checked against Section 1, Assumptions A3 and A4, Definitions 2.1 and 2.3.",
    ),
    row(
        "E4-e-r1-cards-021-030",
        "2.7-cards",
        "cards.json E4-c021..E4-c030 (L02)",
        PASS,
        "Definition 2.2, E4-c022 (excess demand, now stated with x^i(q) and Definition 2.3, matches L02.txt line 0029), "
        "Definition 2.3, Assumption A5 (E4-c024), Lemma 2.4, Proposition 2.5, Corollary 2.7, Proposition 2.8, Proposition "
        "2.9 with w_i = theta_i and q*.ebar = 1. Hypotheses carried.",
    ),
    row(
        "E4-e-r1-cards-031-040",
        "2.7-cards",
        "cards.json E4-c031..E4-c040 (L02, L03)",
        PASS,
        "Example 2.11 prices, aggregate and bundles re-derived (indep_checks.py); Lab 2 Parts C, D, E values; Misconceptions "
        "L02 1 to 3 (E4-c036 to c038, with 3/32 and 9/16 re-derived); L03 Definitions 3.1 to 3.3 (E4-c039 to c041).",
    ),
    row(
        "E4-e-r1-cards-041-050",
        "2.7-cards",
        "cards.json E4-c041..E4-c050 (L03)",
        PASS,
        "Proposition 3.4 (a) and (b) with hypotheses (E4-c042, c043); Step 1 (E4-c044) matches L03.txt line 0031; Remark 3.5 "
        "(E4-c045); Example 3.6 with 1-based states (E4-c046, indep_checks MRS 4, 2, 1/2 and price ratios 4, 2, 1/2); Lab 3 "
        "Parts A and B (E4-c047, c048 with grid 125 and counts 0 and 2 re-derived by brute force); R2 derivative 1/12 and 1/4 "
        "re-derived (E4-c049).",
    ),
    row(
        "E4-e-r1-cards-051-060",
        "2.7-cards",
        "cards.json E4-c051..E4-c060 (L03, L04)",
        PASS,
        "E4-c051 to c052 (L03 Misconceptions 2 and 3) and E4-c053 to c060 (L04 Definitions 1.1, 1.3, Theorem 1.4, Proposition "
        "1.5, Corollary 1.6). Checked against L03.txt lines 0056-0060 and L04.txt Sections 1 and 2.",
    ),
    row(
        "E4-e-r1-cards-061-070",
        "2.7-cards",
        "cards.json E4-c061..E4-c070 (L04)",
        PASS,
        "Lemma 2.1 (E4-c061); Example 2.2 rank 2 and augmented ranks 2, 3, 3 (E4-c062 to c065, lab Part C output); Example 2.3 "
        "redundancy (E4-c064); Remark 3.1 and 3.2 (E4-c066, c067); Proposition 4.1 and 4.2 with A2, A4 and theta >= 0 "
        "(E4-c068, c069). Rank values re-derived by indep_checks.py.",
    ),
    row(
        "E4-e-r1-cards-071-080",
        "2.7-cards",
        "cards.json E4-c071..E4-c080 (L04, L05)",
        PASS,
        "L04 Misconceptions 2 to 4 (E4-c071 to c073; c071 rank 2 re-derived); L05 Assumption A1 and the model of Definition 1.1 "
        "(E4-c075 to c079 now use varsigma, matching L05.txt lines 0019-0025).",
    ),
    row(
        "E4-e-r1-cards-081-090",
        "2.7-cards",
        "cards.json E4-c081..E4-c090 (L05)",
        PASS,
        "Lemma 2.1 (E4-c081), Proposition 2.2 with the fixed point c0* = alpha/(beta+varsigma) (E4-c082, c083), Corollary 2.3 "
        "(E4-c084, c085), Lemma 3.1 (E4-c086), Proposition 3.2 (E4-c087, c088), Proposition 3.3 (E4-c089) with the damping "
        "factor 1 - nu(1 + varsigma/beta).",
    ),
    row(
        "E4-e-r1-cards-091-100",
        "2.7-cards",
        "cards.json E4-c091..E4-c100 (L05, L06)",
        PASS,
        "L05 lab cards c090 to c098 checked against Lab 1 Parts A to F output (fixed points, paths, ratios, equals_fixed_point) "
        "and Misconceptions 1 to 3 (E4-c096 to c098); E4-c099 now PASS (see its own row); E4-c095 matches Remark 4.1.",
    ),
    row(
        "E4-e-r1-cards-101-110",
        "2.7-cards",
        "cards.json E4-c101..E4-c110 (L06)",
        PASS,
        "Definition 6.1 and A1 (E4-c100 to c102), Definition 6.2 (E4-c103), A2, A3, A4 (E4-c104 to c106); E4-c107 (linear "
        "residual; Step 3 at three points) matches L06.txt lines 0029 and 0206; E4-c108 now states both parts of Assumption G "
        "(L06.txt line 0031).",
    ),
    row(
        "E4-e-r1-cards-111-120",
        "2.7-cards",
        "cards.json E4-c111..E4-c120 (L06)",
        PASS,
        "Lemma 6.2 (E4-c110, now Assume A3), Lemma 6.3 (E4-c111, c112), Lemma 6.4 (E4-c113), Proposition 6.7 (E4-c114, c115), "
        "Corollary 6.8 (E4-c116, c117), Example 6.9 base values (E4-c118, c119), x_I = 1/7 and x_U = -1/7 at (1,0) "
        "(E4-c120, re-derived by indep_checks.py).",
    ),
    row(
        "E4-e-r1-cards-121-130",
        "2.7-cards",
        "cards.json E4-c121..E4-c130 (L06, L07)",
        PASS,
        "Remark 6.10 (E4-c121); Lab 1 Part C 16 grid points, all zero (E4-c122, grade C); Part D residual -9/85 re-derived by "
        "hand and by indep_checks.py (E4-c123); Part E SIMULATED draws (E4-c124, c125); E4-c126 to c129 Misconceptions; "
        "E4-c130 Definition 7.1 correlation.",
    ),
    row(
        "E4-e-r1-cards-131-140",
        "2.7-cards",
        "cards.json E4-c131..E4-c140 (L07)",
        PASS,
        "Definitions 7.1 and 7.2, Lemma 7.3 and 7.4 (E4-c133 to c135), Remark 7.5 (E4-c136), Proposition 7.6 and 7.7 "
        "(E4-c137, c138), Remark 7.8 (E4-c139), Remark 7.9 with Var(p) = theta_s^2 (sigma_v^2 + sigma_e^2) + theta_u^2 sigma_u^2 "
        "(E4-c140, re-derived). E4-c134 now uses b for the forecast coefficient, matching Lemma 7.4 (L07.txt line 0027).",
    ),
    row(
        "E4-e-r1-cards-141-150",
        "2.7-cards",
        "cards.json E4-c141..E4-c150 (L07)",
        FAIL,
        "Cards c141 to c145 are graded T, but the L07 key-results row (scratch/txt/L07.txt line 0130) grades the base-instance "
        "value rho^2 = 1/3 and the sweep values 4/9 to 1/66, 1/6 to 9/22, 4/9 to 1/6 as C (finite check, Lab 1 Parts A to E). "
        "The values themselves are correct (indep_checks.py: rho^2 4/9, 1/3, 1/6, 1/18, 1/66; Var(p) 729/1444 and 35937/4802; "
        "lam sweep 1/6, 1/3, 9/22; a sweep 4/9, 1/3, 1/6). E4-c146 (SIMULATED, C) agrees with the lesson. See E4-e-r2-grades.",
        "Make the card and lesson grades agree. See the fix in E4-e-r2-grades.",
    ),
    row(
        "E4-e-r1-cards-151-160",
        "2.7-cards",
        "cards.json E4-c151..E4-c160 (L08)",
        PASS,
        "Assumption A1 (E4-c151, c152: Arrow-Pratt coefficient a from -U''/U' re-derived), A2, A3, A5 (E4-c153 to c155, "
        "with N = G - c from Definition 4.3); Lemma 2.1 and 2.2 (E4-c156, c157); Fact 2.3 (E4-c158); E4-c159 Corollary 2.4(a).",
    ),
    row(
        "E4-e-r1-cards-161-170",
        "2.7-cards",
        "cards.json E4-c161..E4-c170 (L08)",
        PASS,
        "Lemma 2.5 (E4-c161); Proposition 3.1 (E4-c162, c163) with kappa = a sigma_e^2/lambda; Corollary 3.2 (E4-c164); Lemma "
        "3.3 (E4-c165, c166); Proposition 4.1 (E4-c167); Proposition 4.2 (E4-c168); Definition 4.3 (E4-c169); Proposition 4.4 "
        "(E4-c170). Formulas re-derived by indep_checks.py gain_terms (gain, Corr^2 at lam*, lam 0.5 slope 0.1605).",
    ),
    row(
        "E4-e-r1-cards-171-180",
        "2.7-cards",
        "cards.json E4-c171..E4-c180 (L08)",
        FAIL,
        "Cards c171 to c175 and c177 to c180 pass (Lemma 4.5, Definition 4.6, paradox definition, Proposition 5.1(a) and (b), "
        "Proposition 5.2(a) to (c), and the Example 1.1 values G(0) = ln(2)/4 = 0.173287 and G(1) = ln(5/3)/4 = 0.127706 "
        "re-derived). E4-c176 FAILS: its back says the correlation is undefined, but L08 Res 1 solution (scratch/txt/L08.txt "
        "line 0201) says Corr(v,p)^2 = 0. See E4-e-r1-card-E4-c176 for the fix.",
        "Fix the lesson, not the card: L08 Res 1 solution (course/modules/E/E4/L08.html) must say the correlation is undefined "
        "(Var(p) = 0 under sigma_u^2 = 0; Definition 7.1) instead of 0. Then re-run this round's check.",
    ),
    row(
        "E4-e-r1-cards-181-190",
        "2.7-cards",
        "cards.json E4-c181..E4-c190 (L08, L09)",
        PASS,
        "E4-c181 to c188 checked against Lab 1 Parts A to D (seed 20261103 SIMULATED label present; residual 1.332e-15; slope "
        "0.1595 vs 0.1605; lam* 0.657828572; boundary gaps 7.71e-03, -6.71e-03; Part D no interior root; C grades on finite "
        "checks). E4-c184 is grade C with basis naming the 999-point grid (lab Part D). E4-c185 to c188 misconceptions "
        "match L08.txt Section 7 and Corollary 3.2 / Lemma 3.3(a). E4-c189 and c190 match L09 B1 and B2.",
    ),
    row(
        "E4-e-r1-cards-191-200",
        "2.7-cards",
        "cards.json E4-c191..E4-c200 (L09)",
        PASS,
        "Assumption B3 (E4-c191), Definitions 1.1 and 1.2 (E4-c192 to c195), Definition 2.2 (E4-c196, now a no-prices "
        "statement that matches L09.txt line 0035), Theorem 2.1 (E4-c197), Corollary 2.3 (E4-c198), Proof 1 (E4-c199), "
        "Example 2.4 (E4-c200, values 1/2, 1/3, -2 re-derived).",
    ),
    row(
        "E4-e-r1-cards-201-210",
        "2.7-cards",
        "cards.json E4-c201..E4-c210 (L09)",
        PASS,
        "Lab 1 Part B and C counts re-derived by exhaustive enumeration in indep_checks.py: 500 strict at state 1, 625 "
        "nonnegative on the meet, 0 with a nonzero posterior, 15625 bets (E4-c201 to c204); Section 4 two-prior numbers "
        "0.4 and 0.2 (E4-c205); Misconceptions (E4-c206 to c208: c206 fixed); Res 1 and Res 3 (E4-c209, c210).",
    ),
    row(
        "E4-e-r2-cards-211-new",
        "2.7-cards",
        "cards.json E4-c211 (new in this round's pin)",
        PASS,
        "See E4-e-r2-cards-211 (the same card, checked by indep_checks.py and against L09.txt Res 2).",
    ),
]

# The row id E4-e-r2-cards-211 is used above under a second name; keep one row for the card.
rows = [r for r in rows if r["id"] != "E4-e-r2-cards-211-new"]
rows.append(
    row(
        "E4-e-r2-cards-211",
        "2.7-card",
        "cards.json E4-c211 (L09, Problem Res 2)",
        PASS,
        "Front: two trivial-partition states, priors p != r in (0,1). Back: x(H)=1, x(L)=-t with t = theta/(1-theta), "
        "theta=(p+r)/2, and the label swap when p<r. Checked in indep_checks.py (L09 two-prior section, four (p,r) pairs, both "
        "receipts strictly positive) and against L09.txt Res 2 solution.",
    )
)

fragment = {
    "unit": "E4",
    "slice": "e",
    "round": 2,
    "verifier": "independent verifier (Haiku 5.5), slice e: all 211 cards in course/modules/E/E4/cards.json against lessons L01-L09",
    "pin": "67c47689c49435bc0e6639e3de4feded5eefdd64",
    "base": "1c1645f3b00eada2fb54d39c86d5d949e15b4fbc (round 1 pin, fragment frags/E-E4-e.round1.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE2-E4-e",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE2-E4-e/scratch",
    "verified_at": "2026-11-04T07:31:58Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Scope: all 211 cards, each read and checked against the rendered text of L01-L09 at the pin (html_to_text.py). "
        "Lesson text was read in full because cards must agree with current lesson text; it changed in every lesson since the "
        "round-1 pin. Commands run in this round: check_pages --unit E4 (PASS), check_dag --unit E4 (PASS), run_labs --unit E4 "
        "(PASS 12/12), run_twins (9 twins, python -I -W error, exit 0), verify_refs --offline (560 entries, 0 problems), the "
        "card scripts (card_scan, card_refs, card_numbers), indep_checks.py (FAILS 0), ruff check and format --check on "
        "ledgers/E4/scripts/E4-e-r2 (clean), and one plain curl of the Crossref record for muth1961rational. The whole driver is "
        "ledgers/E4/scripts/E4-e-r2/run_slice_e_r2.sh. Mutation testing does not apply to a card slice (no grader); mutants is empty. "
        "Out-of-slice observations for the builders, not scored as card rows: (1) L03 Key results (scratch/txt/L03.txt line 0119) "
        "labels the Example 3.6 MRS values as MRS_01, MRS_02, MRS_12 (0-based), while Example 3.6 and E4-c046 use 1-based states; "
        "state the convention once. (2) L08 Res 1 solution (line 0201) is the only place the cards disagree with the lesson text; "
        "that is the one FAIL."
    ),
    "summary": {
        "cards": 211,
        "cards_failed": 6,
        "failing_card_ids": ["E4-c141", "E4-c142", "E4-c143", "E4-c144", "E4-c145", "E4-c176"],
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == PASS),
        "fail": sum(1 for r in rows if r["status"] == FAIL),
        "unverifiable": 0,
    },
}

out = Path("ledgers/E4/E4-e.json")
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {out} rows={len(rows)}")
