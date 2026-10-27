"""Round-5 fragment builder for AC2 L03-L04: carries round-4 row ids, applies this round's verdicts, validates."""
import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1])
prev = json.load(open("/tmp/ac2-frags/L03-L04.round4.json", encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]

C = "Carried from round 4 ("
NEW = {}  # id -> (status, check, location, evidence)

def row(i, status, check, location, evidence, fix=None):
    NEW[i] = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        NEW[i]["fix"] = fix

# Command rows: all re-run this round (outputs in /tmp/ac2-v/L03-L04/r5)
row("L03-L04-cmd-pin", "PASS", "2.9-structure", "repository",
    "`git rev-parse --short HEAD` -> 11b3477 (round-6 builder pin); `git status --short` -> `?? .venv` only. Delta `git diff --stat 2607c60 HEAD -- course tests atlas plans references curriculum` (9 files) touches this slice in: L03.html (line 724, E3 solution), L04.html (line 370, honest-pending sentence), cards.json (c058 grade/basis added; c064 is L05). tests/labs/AC2/lab-AC2-L03-1.py and lab-AC2-L04-1.py, atlas/, references/, notation/, plans/ are unchanged in the delta (not in the stat). Every hunk read. Nothing committed or pushed.")
row("L03-L04-cmd-check_pages", "PASS", "2.9-structure", "tools/check_pages.py --unit AC2",
    "`.venv/bin/python tools/check_pages.py --unit AC2` -> 'check_pages AC2: PASS', exit 0 (/tmp/ac2-v/L03-L04/r5/check_pages.txt).")
row("L03-L04-cmd-check_dag", "PASS", "2.9-structure", "tools/check_dag.py --unit AC2",
    "`.venv/bin/python tools/check_dag.py --unit AC2` -> 'check_dag AC2: PASS', exit 0 (/tmp/ac2-v/L03-L04/r5/check_dag.txt).")
row("L03-L04-cmd-check_projects", "PASS", "2.6-projects", "tools/check_projects.py --unit AC2",
    "`.venv/bin/python tools/check_projects.py --unit AC2` -> 'check_projects AC2: PASS', exit 0 (/tmp/ac2-v/L03-L04/r5/check_projects.txt).")
row("L03-L04-cmd-run_labs", "PASS", "2.5-lab", "tools/run_labs.py --unit AC2 --page L03 and --page L04",
    "`tools/run_labs.py --unit AC2 --page L03` -> 'run_labs AC2: PASS (1/1)', exit 0; `--page L04` -> 'run_labs AC2: PASS (1/1)', exit 0 (/tmp/ac2-v/L03-L04/r5/run_labs_L03.txt, run_labs_L04.txt).")
row("L03-L04-cmd-twins-strict", "PASS", "2.5-lab", "tests/labs/AC2/lab-AC2-L03-1.py, tests/labs/AC2/lab-AC2-L04-1.py",
    "`.venv/bin/python -I -W error tests/labs/AC2/lab-AC2-L03-1.py` exit 0, stderr 0 bytes, 23 stdout lines; the L04 twin exit 0, stderr 0 bytes, 12 stdout lines (/tmp/ac2-v/L03-L04/r5/twin_L03.out, twin_L04.out, twin_L03.rc, twin_L04.rc, *.err).")
row("L03-L04-cmd-twin-identity", "PASS", "2.5-lab", "course/modules/AC/AC2/L03.html, L04.html vs the twins",
    "ledgers/AC2/scripts/L03-L04-r5/twin_check.py (own script, this round): 'L03: code_equals_twin=True expected_equals_twin_stdout=True expected_lines=23' and 'L04: code_equals_twin=True expected_equals_twin_stdout=True expected_lines=12' (/tmp/ac2-v/L03-L04/r5/twin_check.txt).")
row("L03-L04-cmd-page_smoke", "PASS", "2.9-structure", "tools/page_smoke.py --unit AC2 --pages L03 L04",
    "`tools/page_smoke.py --unit AC2 --pages L03 L04` -> 'page_smoke modules/AC/AC2/L03.html: PASS', 'page_smoke modules/AC/AC2/L04.html: PASS', 'page_smoke AC2: PASS', exit 0; lab lab-AC2-L04-1 0.0 s (/tmp/ac2-v/L03-L04/r5/page_smoke.txt).")
row("L03-L04-cmd-verify_refs", "PASS", "2.1-citation", "tools/verify_refs.py --offline; tools/verify_refs.py --unit AC2",
    "`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0; `tools/verify_refs.py --unit AC2` (live) -> 'live re-verification of AC2: 7 of 560 entries, 0 problems', exit 0 (/tmp/ac2-v/L03-L04/r5/verify_refs_offline.txt, verify_refs_unit.txt).")
row("L03-L04-cmd-ruff-mypy-pytest", "PASS", "2.5-lab", "both twins; tests/test_labs.py, tests/test_page_checks.py",
    "`ruff check` on both twins -> 'All checks passed!'; `ruff format --check` -> '2 files already formatted'; `mypy --no-incremental` on both -> 'Success: no issues found in 2 source files'; `pytest -q tests/test_labs.py tests/test_page_checks.py` -> exit 0 (/tmp/ac2-v/L03-L04/r5/ruff_mypy_pytest.txt).")

row("L03-L04-cite-penman2013financial", "PASS", "2.1-citation",
    "course/modules/AC/AC2/L03.html Section 4 bullet 4 (line 624, claim grade C, data-locator 'passage locator not confirmed') and key-results row 7 (line 767); references/references.json key penman2013financial",
    "Registry entry unchanged in the delta (references/ not in the stat). Live re-fetch this round: `curl https://openlibrary.org/books/OL25163071M.json` -> HTTP 200, title 'Financial statement analysis and security valuation', isbn_13 ['9780078025310'], publish_date 2013, publishers ['McGraw-Hill'] (/tmp/ac2-v/L03-L04/r5/penman_ol.json). The chapter passage is not reachable; the claim stays at grade C with the locator stated as unconfirmed (ruling 1). Line 624 is unchanged in the round delta.")
row("L03-L04-cite-sloan1996stock", "PASS", "2.1-citation",
    "course/modules/AC/AC2/L04.html line 352 (claim grade C, data-cite sloan1996stock, data-locator 'Crossref abstract; passage locator not confirmed'); course/modules/AC/AC2/cards.json AC2-c058 (grade C, same basis); references/references.json key sloan1996stock",
    "Re-fetched this round: `curl https://api.crossref.org/works/10.2308/tar-9608042309` -> HTTP 200; title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?', The Accounting Review 71(3) 289-315; abstract 'Investigates whether stock prices reflect information about future corporate earnings contained in accrual and cash flow components of currents earnings.' The page sentence matches that scope and states no finding (/tmp/ac2-v/L03-L04/r5/sloan_crossref.json). Locator correction: the round-4 row cited L04 line 344; the claim is at line 352 (line 344 is unrelated text). Card AC2-c058 now carries grade C and basis 'Crossref abstract; passage locator not confirmed', matching the page (re-verified because the card changed).")
row("L03-L04-cite-freshness", "PASS", "2.1-citation", "registry keys penman2013financial, sloan1996stock",
    "`git diff --stat 2607c60 HEAD -- references` is empty (references/ absent from the round delta). Both keys present with status 'verified', used_by AC2; `verify_refs --unit AC2` PASS (L03-L04-cmd-verify_refs).")
row("L03-L04-num-L03-table", "PASS", "2.2-number", "course/modules/AC/AC2/L03.html Lab 1 expected block (lines ~553-575)",
    "Expected block equals twin stdout (twin_check, this round). Unrounded invested capital from the twin's own functions (ledgers/AC2/scripts/L03-L04-r5/l03_numbers.py): 906.866437, 993.547906, 1083.131252, 1153.813992 USD m (2021-2024), all agreeing with the printed 1-dp values. ROIC 2024 at 0/25/30%: 0.129891, 0.097418, 0.090923 (printed 0.1299, 0.0974, 0.0909); FY2023 at 30% 0.125945 (printed 0.1259); at 15%/21% for 2024: 0.1104, 0.1026. (/tmp/ac2-v/L03-L04/r5/l03_numbers.txt)")
row("L03-L04-num-L03-remark12", "PASS", "2.2-number", "course/modules/AC/AC2/L03.html Remark 1.2, Section 4 bullet 1, key-results row 5, quiz explain, card AC2-c121",
    "140.114391/(1038.339579 + 50) = 0.128741 -> 0.1287, matching the lab's printed hypothetical (recomputed this round from the twin's unrounded values). Contract atlas/A15.contract.md lines 171-172 ('deliberate simplification: no short-term debt') unchanged.")
row("L03-L04-num-L03-example33-remark35", "PASS", "2.2-number", "course/modules/AC/AC2/L03.html Example 3.3, Remark 3.5, misconceptions 2 and 3, key-results row 4",
    "Recomputed this round: 186.8 x 0.75 = 140.1 (unrounded 140.114); average (993.5+1083.1)/2 = 1038.3 (unrounded 1038.340); 140.114/1038.340 = 0.134941 -> 0.1349; year-end 140.114/1083.131 = 0.129360 -> 0.1294. Remark 3.5: 0.1349/0.1239 - 1 = 8.9% (printed-value arithmetic, 8.878%). Unchanged text.")
row("L03-L04-num-L03-E1", "PASS", "2.2-number", "course/modules/AC/AC2/L03.html problem E1 (solution)",
    "Recomputed this round: NOPAT 2024/2023 - 1 = -22.2% (printed 109.0/140.1 gives -22.2%; unrounded -22.235%); average IC 2024/2023 - 1 = +7.7% (unrounded 1118.472622/1038.339579 = +7.72%); (1-0.222)/(1+0.077) = 0.7224 -> 0.722; 0.0974/0.1349 - 1 = -27.8% (unrounded 0.097418/0.134941 - 1 = -27.81%). Unchanged text; the E3 causal sentence below relies on these figures (see L03-L04-math-L03-E3-causal).")
row("L03-L04-num-L03-E2", "PASS", "2.2-number", "course/modules/AC/AC2/L03.html problem E2 solution and quiz item E2; card AC2-c047",
    "Recomputed this round: 1 - 0.10/0.1298906 = 0.23012 -> 23.0%; with printed 0.1299, 0.23018 -> 0.2302 (as the page says). Lab grid 0.0974 (25%) and 0.0909 (30%) match; 0.1104 and 0.1026 (15%, 21%) match. Quiz E2 (23) consistent. Unchanged text.")
row("L03-L04-num-L03-E3", "PASS", "2.2-number", "course/modules/AC/AC2/L03.html problem E3 solution (line 724, changed this round)",
    "Round-4 FAIL is fixed. Line 724 now says growth of 9.6% 'from the unrounded values 906.8664 and 993.5479', 9.56% by 993.5479/906.8664 - 1, 'which the printed figures give as 9.5%' (printed 993.5/906.9 - 1 = 9.549%, which rounds to 9.5%): all re-derived (/tmp/ac2-v/L03-L04/r5/l03_numbers.txt: 9.5584%, printed 9.5490%). 993.547906 -> 1083.131252 is 9.0% (9.0165% unrounded) and 6.5% (6.5258% unrounded) are correct and labelled as unrounded. Note (not a FAIL): Lab 1 prints invested capital to one decimal, so the 6-decimal values are not on the page; they are reproduced from the twin's own functions, the same convention as E2's 0.12989.")
row("L03-L04-num-L03-M-and-P", "PASS", "2.2-number", "course/modules/AC/AC2/L03.html problems M1-M3, P2, quiz items",
    "Recomputed this round: M1 200x0.75/1000 = 0.15; M2 600+250-80 = 770, (770+730)/2 = 750, NOPAT 120, ROIC 0.16; M3 0.10/0.13 -> tau = 0.2308 (23.1%); P2 100/950 = 0.1053 and 100/1000 = 0.1000. Quiz data-answers 0.15, 0.1349, 0.1239 match. Unchanged text.")
row("L03-L04-num-L04-lab", "PASS", "2.2-number", "course/modules/AC/AC2/L04.html Lab 1 expected block (lines ~316-330), interpretation, problems E1 and E2",
    "Expected block equals twin stdout (twin_check). Twin output (/tmp/ac2-v/L03-L04/r5/twin_L04.out): correlation_moving 0.8221; means -0.0308 and -0.0298; share_of_firms_gap_above_0.01 0.6775 (seed 2604), 0.6800 (2605), 0.7000 (2606); identity residuals 0.000000. Interpretation '67.75%' = 0.6775. Unchanged lines (L04 changed only at line 370).")
row("L03-L04-num-L04-E3-square", "PASS", "2.2-number", "course/modules/AC/AC2/L04.html problem E3 solution; quiz item L04q7 (data-answer 0.6759, tolerance 0.0005)",
    "Not re-derived from the unrounded panel this round (the lab prints r to 4 dp only; the round-4 script ledgers/AC2/scripts/L03-L04-r4/l04_numbers.py gave r = 0.8221494, r^2 = 0.6759296, 1 - r^2 = 0.3240704, var(gap)/var(cf) = 0.3285290). Arithmetic check: 0.8221494^2 = 0.675930 -> 0.6759. Solution text (line ~477-479) and quiz item unchanged in this round's delta; carried on that basis.")
row("L03-L04-num-L04-M1-M4-quiz", "PASS", "2.2-number", "course/modules/AC/AC2/L04.html problems M1-M3 and quiz items q2, q3, q9 (data-answer 0.00625, -0.01875, 0.021875)",
    "Recomputed this round: M1 (500-80)-(420-60) = 60; 260-240 = 20; 60-20-30 = 10; 10/1600 = 0.00625. M2 120-150 = -30; -30/1600 = -0.01875. M3 (30-10)/1600 = 0.0125; 0.00625 + 0.0125 = 0.01875; x1600 = 30. Quiz q2, q3, q9 match. Unchanged text.")
row("L03-L04-num-L04-M4", "PASS", "2.2-number", "course/modules/AC/AC2/L04.html problem M4 solution (line ~422); card AC2-c056 back",
    "Recomputed this round: 15/1600 = 0.009375 (debt term); 30/1600 = 0.01875 (ONCA); -10/1600 = -0.00625 (ONCL); sum 0.021875. Unchanged text and card c056 byte-identical since 2607c60.")
row("L03-L04-num-L04-E2-two-inputs", "PASS", "2.2-number", "course/modules/AC/AC2/L04.html problem E2 solution (line ~472)",
    "Lab output (twin_L04.out) prints 0.6775 (seed 2604), 0.6800 (2605), 0.7000 (2606); the solution's statement that the share depends on the seed, the 0.01 threshold and the generator's move sizes matches. Unchanged lines.")
row("L03-L04-grade-L03", "PASS", "2.3-grades", "course/modules/AC/AC2/L03.html why-it-matters (line ~51) and the T-graded claims (Proposition 2.2, 3.2, 3.4, Section 4 intro identity, key-results rows 1-3)",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 byte-identical since 2607c60; git diff hunk confined to line 724): the why-it-matters sentence cites Definition 2.1 and 'an A15 contract rule' with no grade; the T claims are proved on the page (proofs re-read this round, see the math rows).")
row("L03-L04-grade-L04", "PASS", "2.3-grades", "course/modules/AC/AC2/L04.html Propositions 2.2, 3.1, 4.1, Corollary 2.3, Remark 2.4 (line 138), Section 5 bullets (lines 367-368), key-results table, Sloan claim (line 352)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): T claims are proved on the page or follow from Definitions 1.3 and 2.1 by substitution. The Sloan claim (line 352) is grade C (re-checked under cite-sloan1996stock).")
row("L03-L04-grade-contract-T", "PASS", "2.3-grades", "course/modules/AC/AC2/L03.html Definition 3.1 and key-results row 6; course/modules/AC/AC2/cards.json AC2-c035",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 and AC2-c035 byte-identical since 2607c60): key-results row 6 is grade C with source 'A15 contract rule (the roic function raises ValueError); Lab 1 error case'; card AC2-c035 grade C, basis 'A15 contract rule (the roic function)'. atlas/A15.contract.md lines 99-100 match.")
row("L03-L04-math-L03-prop22", "PASS", "2.4-math", "course/modules/AC/AC2/L03.html Definition 2.1, Proposition 2.2 and proof (line 85), Remark 2.3 (line 90)",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 byte-identical since 2607c60): ROIC(tau) = OI(1-tau)/avg IC; average IC does not depend on tau; ratio (1-tau2)/(1-tau1); Remark 2.3 identity 1 - NI/OI = 1 - (1 - I/OI)(1 - tau) for NI = (OI - I)(1 - tau) re-checked symbolically.")
row("L03-L04-math-L03-prop32-34", "PASS", "2.4-math", "course/modules/AC/AC2/L03.html Proposition 3.2 (line 587), Proposition 3.4 (line 603) and proof (line 608), problem P2 (line 692), key-results row 3",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 byte-identical since 2607c60): Proposition 3.2 regrouping re-derived; Proposition 3.4 counterexample IC_{t-1}=10, IC_t=-5, NOPAT=1: average-based 1/2.5 = 2/5, year-end 1/(-5) = -1/5, re-checked.")
row("L03-L04-math-L03-problems-R", "PASS", "2.4-math", "course/modules/AC/AC2/L03.html problems P1, P2, P3, R1, R2, R3",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 byte-identical since 2607c60): P1 linearity and P3 averaging arguments and R1-R3 design answers re-read; no unsourced numbers.")
row("L03-L04-math-L04-prop22", "PASS", "2.4-math", "course/modules/AC/AC2/L04.html Definition 2.1, Assumptions A1-A4 (line ~99), Proposition 2.2 and proof (lines ~107-122)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): A4 gives CFO = dCash + capex - dLTD + D; A1 gives NI - D = dE; substitution gives NI - CFO = dCAo + dPPE - capex + dONCA - dCL - dONCL; A2 gives dPPE - capex = -D&A. Twin residuals 0.000000 (this round).")
row("L03-L04-math-L04-cor23", "PASS", "2.4-math", "course/modules/AC/AC2/L04.html Corollary 2.3 and proof (lines ~127-134)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): dividing Proposition 2.2 by average TA gives (dONCA - dONCL)/TA; twin identity residuals 0.000000.")
row("L03-L04-math-L04-prop31", "PASS", "2.4-math", "course/modules/AC/AC2/L04.html Section 3 intro (line ~330), Proposition 3.1 and proof (lines ~334-340)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): NOA excludes STD; A3 gives STD = 0; NI - CFO - dNOA = -D&A - dPPE = -capex under A2.")
row("L03-L04-math-L04-prop41", "PASS", "2.4-math", "course/modules/AC/AC2/L04.html Proposition 4.1 and proof (lines ~349-356), problem P4",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): numerator and denominator are linear in money items, so k cancels.")
row("L03-L04-math-L04-S5-formula", "PASS", "2.4-math", "course/modules/AC/AC2/L04.html Section 5 bullet 1 formula (line ~367), problem M4, quiz q9, key-results row 4",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): (dSTD + dONCA - dONCL)/TA; the round-4 random-draw check (300 articulated draws under A1, A2, A3', A4') has 0 failures (ledgers/AC2/scripts/L03-L04-r4/l04_numbers.py, not re-run).")
row("L03-L04-math-L04-S5-derivation", "PASS", "2.4-math", "course/modules/AC/AC2/L04.html Section 5 bullet 1 derivation (line 367); key-results row 4; card AC2-c056 front",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): A4' is the complete statement (dCash = CFO + CFI + CFF, CFI = -capex, CFF = dLTD + dSTD - D); re-derived by hand: NI - CFO = (dCA - dCash) - dCL - D&A + (dSTD + dONCA - dONCL).")
row("L03-L04-math-L04-E3-claim", "PASS", "2.4-math", "course/modules/AC/AC2/L04.html problem E3 solution (lines ~477-479)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): 1 - r^2 = 0.3241 and var(gap)/var(cf) = 0.3285 are reported as different figures; 'the identity gives the gap exactly, but does not decompose the variance' is a correct reading.")
row("L03-L04-math-L04-P-R-items", "PASS", "2.4-math", "course/modules/AC/AC2/L04.html problems P1-P4, R1-R3 (lines ~429-507); Section 3 intro and Proposition 3.1 hypothesis",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): P1 (NI - CFO = dE - dCash - capex + dLTD under A4), P2 (ONCA and ONCL changes equal), P3, P4 and R1-R3 re-read; no unsourced numbers.")
row("L03-L04-math-L04-notation", "PASS", "2.4-math", "notation/notation.json; course/modules/AC/AC2/L03.html, L04.html",
    "notation/notation.json unchanged in the delta; `grep -o '\\\\[A-Za-z]+'` over both lessons: \\Delta, \\tau, \\overline, \\mathrm, \\tfrac, \\times, \\big, \\gt, \\frac, \\blacksquare, \\qquad, \\ne, \\le, \\dfrac. None is a registry macro (registry keys include \\E, \\Prob, \\Var, \\se ...). The new E3 text adds \\% only (standard). No conflict.")
row("L03-L04-prose-L04-tolerance-rule", "PASS", "2.9-structure", "course/modules/AC/AC2/L04.html Section 4 paragraph after Proposition 4.1 (line ~358)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): matches atlas/A15.contract.md line 190 (Scale row: ratios and accrual ratios invariant to a common positive multiplier of money items).")
row("L03-L04-prose-L04-remark24-overreach", "PASS", "2.3-grades", "course/modules/AC/AC2/L04.html Remark 2.4 T claim (line 138) and Section 5 bullet 2 (line 368)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): CFO enters only AC^CF by Definition 1.3, so a reclassification changes AC^CF and not AC^BS; proved from the definitions.")
row("L03-L04-prose-L04-every-later-measure", "PASS", "2.9-structure", "course/modules/AC/AC2/L04.html line 52 (why-it-matters, last sentence)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): accruals feed L05, L06, L07 (s4 'CFO* > ROA' accrual test) and L08 (TATA = (NI - CFO)/TA, line ~85); each present as described.")
row("L03-L04-prose-L04-remark24-first-sentence", "PASS", "2.9-structure", "course/modules/AC/AC2/L04.html Remark 2.4 first sentence (line 138)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): A3' with A4 as written -> Proposition 2.2 form holds; the extra term appears only under A4' (round-4 draw check; not re-run).")
row("L03-L04-prose-L04-remark14-unnamed-source", "PASS", "2.1-citation", "course/modules/AC/AC2/L04.html Remark 1.4 (line ~85)",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60): matches atlas/A15.contract.md lines 117-118 (short-term debt and taxes payable are not separate items; the lesson states that simplification).")
row("L03-L04-prose-L04-unmarked-claims", "PASS", "2.3-grades", "course/modules/AC/AC2/L04.html line 90 (Section 2 intro), line 360 (Section 4 honest-pending paragraph, now line 370), line 378 (misconception 1), line 497 (R2 solution)",
    "Section 4 honest-pending paragraph (line 370, changed this round: 'The open item is listed in plans/AC2-open-items.md') re-read: no number and no unmarked factual claim; the open-items file has the SEC reuse-statement item (DATA_REQUESTS). Other spans carried from round 4 (L04 lines outside 370 byte-identical since 2607c60). The L05 reference resolves.")
row("L03-L04-prose-L03-claims-unmarked", "PASS", "2.3-grades", "course/modules/AC/AC2/L03.html line 51, Section 4 bullet 4 (Penman, line 624), Section 4 bullet 2 and misconception 4, quiz explanations",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 byte-identical since 2607c60): why-it-matters cites Definition 2.1 and the contract with no grade; Penman bullet is grade C with the locator unconfirmed; bullets and misconceptions are conditional.")
row("L03-L04-prose-L03-acquisition-overreach", "PASS", "2.3-grades", "course/modules/AC/AC2/L03.html Section 4 bullet 2 (line 622), misconception 4 (line 645); card AC2-c043",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 and AC2-c043 byte-identical since 2607c60): statements are conditional ('if the acquired operating income enters NOPAT from the acquisition date'); no overreach.")
row("L03-L04-prose-L03-xref-remark12", "PASS", "2.9-structure", "course/modules/AC/AC2/L03.html Section 4 bullet 4 (line 624); Remark 1.2 cross-references (lines ~621, ~765, ~826)",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 byte-identical since 2607c60): cross-references resolve to the short-term-debt remark; bullet 4 refers to Penman, not to Remark 1.2.")
row("L03-L04-math-L03-E3-causal", "FAIL", "2.4-math", "course/modules/AC/AC2/L03.html problem E3 solution, line 724 (sentences 'The fall in ROIC in 2024 is driven by ... and the slower capital growth offsets part of it' and 'With NOPAT fixed, slower capital growth raises ROIC')",
    "Re-verified from the unrounded values (l03_numbers.txt, and the E1 figures): NOPAT fell 22.24% (140.114 -> 108.959 USD m, ratio 0.7776); average invested capital ROSE 7.72% (1038.340 -> 1118.473 USD m); ROIC at 25% went 0.134941 -> 0.097418, a fall of 27.81%. Holding average capital flat would give a fall of 22.24% only. So the realised capital growth DEEPENS the ROIC fall (ratio 0.7224 vs 0.7776); it does not offset it. The sentence 'the slower capital growth offsets part of it' therefore states the direction wrongly as written. The only sense in which slower growth 'pushes the other way' is a counterfactual against continued 9.0% growth (with that counterfactual the 2024 fall would be 28.67%, against 27.81% actual), which the page does not state. The 'with NOPAT fixed, slower capital growth raises ROIC' clause is correct only in that same counterfactual sense. The round-4 PASS on this row was wrong.",
    "Replace the last two sentences of line 724 with: 'The fall in ROIC in 2024 is driven by the operating-income decline (Problem E1). Average invested capital rose 7.7% in 2024, which deepens the fall (ROIC down 27.8%, against 22.2% if capital had been flat). Growth slowed from 9.0% to 6.5%, so capital grew less than it would have at the 2023 rate; that moderates the deepening relative to that counterfactual, which the lab does not compute.' Or drop the causal attribution entirely and keep the growth figures.")

row("L03-L04-cards-L03", "PASS", "2.7-cards", "course/modules/AC/AC2/cards.json, ids AC2-c032..c047 and AC2-c121 (17 cards with lesson L03)",
    "Carried from round 4 (cards AC2-c032..c047 and AC2-c121 byte-identical since 2607c60; ledgers/AC2/scripts/L03-L04-r5/cards_scan.py: the changed-card list vs 2607c60 is c058, c064, c103, c107, c119, c123, c130, c134 and none of the 17 L03 cards): each read against its lesson text, and c035 and c046 re-checked as above.")
row("L03-L04-cards-L04", "PASS", "2.7-cards", "course/modules/AC/AC2/cards.json, ids AC2-c048..c062 and AC2-c137 (16 cards with lesson L04)",
    "Re-verified card AC2-c058 (changed this round: grade C and basis 'Crossref abstract; passage locator not confirmed' added; its cite sloan1996stock and the lesson's claim at line 352 match; the card states no finding). AC2-c059 is unchanged (no grade, no cite; claim matches Misconception 1). Other 15 L04 cards byte-identical since 2607c60 (cards_scan.py) and carried from round 4 (scope of that round's reading).")
row("L03-L04-cards-dup", "PASS", "2.7-cards", "course/modules/AC/AC2/cards.json (all 140 cards); ledgers/AC2/scripts/L03-L04-r5/cards_scan.py",
    "cards_scan.py this round: 140 cards, ids contiguous AC2-c001..c140, 0 duplicate fronts, 0 duplicate backs (/tmp/ac2-v/L03-L04/r5/cards_r5.txt).")
row("L03-L04-quiz-keys", "PASS", "2.2-number", "course/modules/AC/AC2/L03.html quiz (9 items), L04.html quiz (9 items)",
    "Carried from round 4 (quiz items in L03.html lines outside 721-724 and L04.html lines outside 370 byte-identical since 2607c60): keys match the worked solutions (E2 23, 0.1349, 0.1239, 0.15; L04 0.00625, -0.01875, 0.021875, 0.6759 with tolerance 0.0005).")
row("L03-L04-mutants", "PASS", "2.6-projects", "not applicable to this slice (no project mutants)",
    "not applicable to this slice (no project mutants).")
row("L03-L04-lab-L03", "PASS", "2.5-lab", "course/modules/AC/AC2/L03.html Lab 1 (lines ~93-577); tests/labs/AC2/lab-AC2-L03-1.py",
    "Lab 1 runs under `-I -W error` (exit 0, stderr 0 bytes, 23 lines); page expected block equals twin stdout (twin_check, this round); run_labs and page_smoke PASS. Twin unchanged in the delta.")
row("L03-L04-lab-L03-interpretation", "PASS", "2.5-lab", "course/modules/AC/AC2/L03.html Lab 1 interpretation (line 576)",
    "Re-verified: printed operating income 179.3, 185.4, 186.8, 145.3 (twin output); 2024/2023 unrounded ratio 0.7776453 (line 576 says 0.7776); fall 22.2%. Interpretation correct; line 576 unchanged.")
row("L03-L04-lab-L03-docstring", "PASS", "2.5-lab", "tests/labs/AC2/lab-AC2-L03-1.py docstring lines 1-10 and the page's lab description (lines 96-102)",
    "Twin unchanged in the delta. The docstring says the lab prints the largest deviation of ROIC from its zero-tax value times (1 - tax_rate); the code (`worst = max |ROIC(t) - ROIC(0)(1-t)| / |ROIC(0)|`) prints it as 1.4e-16 with the word 'relative'; no assert in the file.")
row("L03-L04-lab-L04", "PASS", "2.5-lab", "course/modules/AC/AC2/L04.html Lab 1 (lines ~141-326); tests/labs/AC2/lab-AC2-L04-1.py",
    "Lab 1 runs under `-I -W error` (exit 0, stderr 0 bytes, 12 lines); expected block equals twin stdout; seeds 2604, 2605, 2606 printed; interpretation matches the output.")
row("L03-L04-lab-L04-docstring", "PASS", "2.5-lab", "tests/labs/AC2/lab-AC2-L04-1.py lines 1-10, 149-153 (shown on the page at lines 144-153)",
    "Twin unchanged in the delta; docstring matches the code: SIMULATED, seeded generator, clean-surplus derivation of NI, articulation by construction.")
row("L03-L04-lab-numbering", "PASS", "2.9-structure", "course/modules/AC/AC2/L03.html lines ~94-95, 576; course/modules/AC/AC2/L04.html line ~142",
    "Carried from round 4 (course/modules/AC/AC2/L03.html and L04.html lines named here byte-identical since 2607c60; hunks at lines 724 and 370 only): 'Lab 1' names the single lab of each page.")
row("L03-L04-banned-phrases", "PASS", "2.9-structure", "course/modules/AC/AC2/L03.html, L04.html (all prose, labs, quiz); the changed lines; cards",
    "Re-scanned this round: 'about' occurs 16 times in L03/L04, every use non-numeric ('about the', 'a fact about', 'a claim about'); 'around' once ('noise around zero'); no 'roughly', 'approximately', 'historically', 'typically', 'usually', ellipsis, TODO/TBD/lorem or 'it can be shown'. Changed line 724 and line 370 contain none. Card AC2-c047 'About 23%' is backed by its own calculation (rule 2(c)).")
row("L03-L04-process-words", "PASS", "2.9-structure", "course/modules/AC/AC2/L03.html Lab 1 hypothesis (line 95); changed lines 724 and 370",
    "Carried from round 4 (course/modules/AC/AC2/L03.html lines outside 721-724 and L04.html lines outside 370 byte-identical since 2607c60): no 'builder', 'this build', 'REQUESTS', 'unit report' in learner text (grep this round on both pages, zero hits). The changed sentences contain none.")
row("L03-L04-struct-L03", "PASS", "2.9-structure", "course/modules/AC/AC2/L03.html",
    "check_pages AC2 PASS (this round); sections 1-9 and problem tiers present; data-hours 8 unchanged; lab, quiz, references and lesson nav in place.")
row("L03-L04-struct-L04", "PASS", "2.9-structure", "course/modules/AC/AC2/L04.html",
    "check_pages AC2 PASS (this round); sections 1-10 present; data-hours 9 unchanged; lab, quiz, references and nav in place.")
row("L03-L04-dag-concepts", "PASS", "2.9-structure", "check_dag; course/modules/AC/AC2/L03.html, L04.html; curriculum/01-foundations.yaml; curriculum/02-economics-finance-core.yaml",
    "check_dag AC2 PASS (this round, /tmp/ac2-v/L03-L04/r5/check_dag.txt). Concepts unchanged; L04 robust-statistics, outlier-detection, missing-data-mechanisms are S0 (a unit prerequisite); gaap-vs-ifrs is AC1.")
row("L03-L04-xref-L04-to-L05", "PASS", "2.9-structure", "course/modules/AC/AC2/L04.html lines ~342-352; course/modules/AC/AC2/L05.html Section 3 and Lab 1",
    "Carried from round 4 (course/modules/AC/AC2/L04.html lines outside 370 byte-identical since 2607c60; L05.html unchanged at its cross-referenced lines): the sorted-portfolio test references resolve.")
row("L03-L04-hours", "PASS", "2.6-hours", "course/modules/AC/AC2/L03.html data-hours=8; L04.html data-hours=9",
    "`grep data-hours` unchanged in the delta; my estimate: L03 four sections, nine problems, one lab, nine quiz items, about 8 h; L04 five sections, fourteen problems, one lab, nine quiz items, about 9 h; both within +/-30%.")

# Keep every round-4 id, in order
rows = []
for i in prev_ids:
    if i not in NEW:
        raise SystemExit(f"missing row {i}")
    rows.append(NEW[i])
extra = set(NEW) - set(prev_ids)
assert not extra, extra

fails = [r["id"] for r in rows if r["status"] == "FAIL"]
unv = [r["id"] for r in rows if r["status"] == "UNVERIFIABLE"]
pas = [r["id"] for r in rows if r["status"] == "PASS"]
summary = (f"AC2 L03-L04 round 5 (pin 11b3477): verdict FAIL. {len(rows)} rows: {len(pas)} PASS, {len(fails)} FAIL, "
           f"{len(unv)} UNVERIFIABLE. FAIL: {', '.join(fails)} (2.4-math; the round-4 PASS was wrong: average invested capital rose, so realised capital growth deepens the 2024 ROIC fall rather than offsetting it). The round-4 FAIL L03-L04-num-L03-E3 is fixed and re-verified PASS (9.56% from unrounded values; printed 9.5%).")

frag = {
    "unit": "AC2",
    "slice": "L03-L04",
    "round": 5,
    "verifier": "round-5 independent verifier for AC2 slice L03-L04 (fresh checkout at 11b3477; re-read the round delta hunks, both pages' changed lines, both twins, the 140-card set; re-ran every command row; re-derived the E3 growth figures and the ROIC decomposition from the twin's unrounded values)",
    "pin": "11b3477",
    "base": "2607c60 (round-4 pin; delta used to pick the rows to re-verify)",
    "checkout": "/tmp/verify-ac2r5-l34 (detached worktree at 11b3477; untracked: .venv symlink and ledgers/AC2/)",
    "scratch": "/tmp/ac2-v/L03-L04/r5",
    "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": ("Round 5 of the L03-L04 slice at pin 11b3477. Round delta for this slice: L03.html line 724 (E3 solution), L04.html line 370 (honest-pending sentence), cards.json (c058 grade C and basis added; c064 is an L05 card). Lab twins and the L03/L04 lab blocks are unchanged. Every round-4 row id is kept (68). The round-4 FAIL (E3 growth) is fixed. The new FAIL is in the E3 solution's causal sentence, which round 4 passed in error. Not a FAIL, noted: Lab 1 prints invested capital to one decimal, so the 6-decimal unrounded values quoted in the E3 solution are not on the page; they are reproduced from the twin's own functions (same convention as E2's 0.12989). Locator correction: the Sloan claim is at L04 line 352 (round 4 cited 344). Real EDGAR data is still honestly pending; every filer is SIMULATED."),
    "summary": summary,
}
out = ROOT / "ledgers/AC2/L03-L04.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(summary)
print("rows", len(rows))
