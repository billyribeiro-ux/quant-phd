"""Round-4 fragment builder: keeps every round-3 row id, attaches the round-4 status and evidence, and writes the fragment."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
r3 = json.loads(Path("/tmp/ac2-frags/L03-L04.round3.json").read_text(encoding="utf-8"))
S = "/tmp/ac2-v/L03-L04/r4"
EV = {}  # id -> (status, evidence, fix or None)

def ok(i, ev):
    EV[i] = ("PASS", ev, None)

def bad(i, ev, fix):
    EV[i] = ("FAIL", ev, fix)

ok("L03-L04-cmd-pin", "`git rev-parse --short HEAD` -> 2607c60 (round-5 builder pin); `git status --short` at start -> `?? .venv` only. "
   "Round delta `git diff --stat 4a8690a HEAD -- course tests atlas plans references curriculum` (19 files) includes this slice: "
   "L03.html (12 lines), L04.html (22), cards.json (71; L03/L04 cards changed: c035, c038, c041, c046, c054, c056, c058, c059), "
   "tests/labs/AC2/lab-AC2-L03-1.py (4), lab-AC2-L04-1.py (5), plans/AC2-open-items.md (4). atlas/A15.contract.md and references/ are unchanged in the delta. "
   "Every hunk of those files was read. Nothing committed or pushed.")
ok("L03-L04-cmd-check_pages", f"`.venv/bin/python tools/check_pages.py --unit AC2` -> 'check_pages AC2: PASS', exit 0 ({S}/check_pages.txt).")
ok("L03-L04-cmd-check_dag", f"`.venv/bin/python tools/check_dag.py --unit AC2` -> 'check_dag AC2: PASS', exit 0 ({S}/check_dag.txt).")
ok("L03-L04-cmd-check_projects", f"`.venv/bin/python tools/check_projects.py --unit AC2` -> 'check_projects AC2: PASS', exit 0 (unit level; {S}/check_projects.txt).")
ok("L03-L04-cmd-run_labs", f"`tools/run_labs.py --unit AC2 --page L03` -> 'run_labs AC2: PASS (1/1)', exit 0; same for --page L04, exit 0 ({S}/run_labs_L03.txt, run_labs_L04.txt).")
ok("L03-L04-cmd-twins-strict", f"`.venv/bin/python -I -W error tests/labs/AC2/lab-AC2-L03-1.py` exit 0, stderr 0 bytes, 23 stdout lines; the L04 twin exit 0, stderr 0 bytes, 12 stdout lines (was 9 at 4a8690a; the three seed lines are new) ({S}/twin_L03.out, twin_L04.out, *.err).")
ok("L03-L04-cmd-twin-identity", f"ledgers/AC2/scripts/L03-L04-r4/twin_check.py: 'L03: code_equals_twin=True expected_equals_twin_stdout=True expected_lines=23' and 'L04: code_equals_twin=True expected_equals_twin_stdout=True expected_lines=12' ({S}/twin_check.txt).")
ok("L03-L04-cmd-page_smoke", f"`tools/page_smoke.py --unit AC2 --pages L03 L04` -> 'page_smoke modules/AC/AC2/L03.html: PASS', 'page_smoke modules/AC/AC2/L04.html: PASS', 'page_smoke AC2: PASS', exit 0; lab timings 0.0 s each ({S}/page_smoke.txt).")
ok("L03-L04-cmd-verify_refs", f"`tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0; `tools/verify_refs.py --unit AC2` (live) -> 'live re-verification of AC2: 7 of 560 entries, 0 problems', exit 0 ({S}/verify_refs_offline.txt, verify_refs_unit.txt).")
ok("L03-L04-cmd-ruff-mypy-pytest", f"`ruff check` on both twins -> 'All checks passed!'; `ruff format --check` -> '2 files already formatted'; `mypy --no-incremental` on both -> 'Success: no issues found in 2 source files'; `pytest -q tests/test_labs.py tests/test_page_checks.py` -> exit 0 ({S}/ruff.txt, mypy.txt, pytest.txt).")

ok("L03-L04-cite-penman2013financial", "Registry penman2013financial (references/references.json): book, Penman, ISBN 9780078025310, McGraw-Hill, 2013, status verified. Live: `curl https://openlibrary.org/books/OL25163071M.json` -> HTTP 200, title 'Financial statement analysis and security valuation', isbn_13 ['9780078025310'], publish_date 2013, publishers ['McGraw-Hill'] "
   f"({S}/penman_ol.json). The chapter passage was not reachable, so the L03 Penman claim (Section 4 bullet 4, grade C, data-locator 'passage locator not confirmed: the net-operating-asset definitions') and key-results row 7 state the locator as unconfirmed. Passes under the unconfirmed-at-C rule (ruling 1).")
ok("L03-L04-cite-sloan1996stock", "L04 Section 3 claim on Sloan (1996) (grade C, data-locator 'Crossref abstract; passage locator not confirmed'). Live: `curl https://api.crossref.org/works/10.2308/tar-9608042309` -> HTTP 200; title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?', The Accounting Review 71(3) 289-315. Crossref abstract: 'Investigates whether stock prices reflect information about future corporate earnings contained in accrual and cash flow components of currents earnings.' The page's sentence matches that scope and states no finding ("
   f"{S}/sloan_crossref.json). Registry entry verified, DOI 10.2308/tar-9608042309.")
ok("L03-L04-cite-freshness", "Registry keys penman2013financial and sloan1996stock present, status 'verified', used_by AC2; `git diff 4a8690a HEAD -- references` is empty in the round delta; verify_refs --unit AC2 PASS (above).")

ok("L03-L04-num-L03-table", f"L03 Lab 1 expected block equals the twin stdout (twin_check). Unrounded recomputation ledgers/AC2/scripts/L03-L04-r4/numbers.py: invested capital 906.9/993.5/1083.1/1153.8 USD m (2021-2024); implied rate 0.25 each year; ROIC 2024 at 0/25/30% = 0.12989/0.09742/0.09092; 2023 at 30% = 0.12594; all agree with the printed 4 dp ({S}/numbers_l03.txt).")
ok("L03-L04-num-L03-remark12", "Remark 1.2 (0.1349 -> 0.1287), Section 4 bullet 1, key-results row 5, quiz explain and card AC2-c121: unrounded 140.114391/(1038.339579 + 50) = 0.128741 -> 0.1287, matching the lab's printed hypothetical. Contract atlas/A15.contract.md lines 171-172 ('deliberate simplification: no short-term debt') match the page's wording.")
ok("L03-L04-num-L03-example33-remark35", "Example 3.3: 186.8 x 0.75 = 140.1 (unrounded 140.114); average (993.5 + 1083.1)/2 = 1038.3 (unrounded 1038.340); 140.1/1038.3 = 0.13493 -> 0.1349; year-end 140.1/1083.1 = 0.129351 from printed values and 0.129360 unrounded, both -> 0.1294 (the printed-value arithmetic rounds the same way, so the statement holds). Remark 3.5: 0.1349/0.1239 - 1 = 8.9% (unrounded 8.94%). Source: numbers_l03.txt.")
ok("L03-L04-num-L03-E1", "E1 solution: NOPAT 109.0/140.1 - 1 = -22.2% (unrounded -22.24%); average IC 1118.5/1038.3 - 1 = +7.7% (unrounded 1118.47/1038.34 = +7.72%); (1-0.222)/(1+0.077) = 0.7224 -> 0.722; 0.0974/0.1349 - 1 = -27.8% (unrounded -27.81%). Printed 1,118.5 for 2024 average matches the unrounded 1118.47. numbers_l03.txt.")
ok("L03-L04-num-L03-E2", "E2 solution: unrounded 2024 zero-tax ROIC 0.1298906 gives tau = 1 - 0.10/0.1298906 = 0.23012 -> 23.0%; with the printed 0.1299 it is 0.23018 -> 0.2302, as the page says. The 25% and 30% values 0.0974 and 0.0909 match the lab (0.09742, 0.09092); 15% and 21% values 0.1104 and 0.1026 are the lab's printed grid. Quiz item E2 (data-answer 23) and card AC2-c047 consistent.")
bad("L03-L04-num-L03-E3",
    "E3 solution (L03 problem set): 'From 906.9 to 993.5 is growth of 993.5/906.9 - 1 = 9.5%'. That arithmetic on the printed values is 9.549%, but the unrounded invested capital (lab output, numbers_l03.txt: 906.8664 -> 993.5479) gives 9.558% = 9.6% at one decimal. The page takes its own E2 standard of using unrounded values where the printed digit differs, and does not do so here. The 9.0% (9.02 unrounded) and 6.5% (6.53 unrounded) figures are correct. 'Growth slows each year' is true either way.",
    "Write 'growth of 9.6% (993.5479/906.8664 - 1 = 9.56% from the unrounded values; the printed 993.5/906.9 gives 9.5%)', or keep 9.5% and label it as the printed-value calculation.")
ok("L03-L04-num-L03-M-and-P", "M1: 200 x 0.75 = 150; 150/1000 = 0.15. M2: 600 + 250 - 80 = 770; (770 + 730)/2 = 750; NOPAT 120; ROIC 0.16. M3: 0.10/0.13 = 0.76923, tau = 0.23077 -> 0.2308 (23.1%). P2: 100/950 = 0.1053; 100/1000 = 0.1000 (exact fractions). Quiz data-answers 0.15, 0.1349, 0.1239 match.")

ok("L03-L04-num-L04-lab", f"L04 Lab 1 expected block (lines ~316-330) equals the twin stdout (twin_check). Recomputed at seed 2604 (l04_numbers.py): corr 0.82215 -> 0.8221; means -0.030767 and -0.029799 -> -0.0308, -0.0298; share above 0.01 = 0.6775; identity residuals 0.000000 (twin run). Interpretation's '67.75%' = 0.6775. Source {S}/l04_numbers.txt.")
ok("L03-L04-num-L04-E3-square", "E3 solution (L04): unrounded r = 0.8221494, r^2 = 0.6759296 -> 0.6759; 1 - r^2 = 0.3240704 -> 0.3241; var(gap)/var(cf) = 0.3285290 -> 0.3285 (l04_numbers.txt). The quiz item L04q7 (data-answer 0.6759, tolerance 0.0005) matches.")
ok("L03-L04-num-L04-M1-M4-quiz", "M1: (500-80)-(420-60) = 60; 260-240 = 20; 60-20-30 = 10; 10/1600 = 0.00625. M2: 120-150 = -30; -30/1600 = -0.01875. M3: (30-10)/1600 = 0.0125; 0.00625 + 0.0125 = 0.01875; x1600 = 30. Quiz q2 (0.00625), q3 (-0.01875), q9 (0.021875) match.")
ok("L03-L04-num-L04-M4", "M4 solution (fixed): 15/1600 = 0.009375 (debt term); 30/1600 = 0.01875 (ONCA); -10/1600 = -0.00625 (ONCL); sum 0.021875 (exact fractions). The text no longer says the balance-sheet measure 'understates by the debt change'; it says the debt term is 0.009375 and the debt term alone is not the gap. Card AC2-c056 says the same. Section 5 formula under A3' and A4' holds in 0 of 300 failing random articulated draws (l04_numbers.py).")
ok("L03-L04-num-L04-E2-two-inputs", f"E2 solution (fixed): the lab prints 0.6775 (seed 2604), 0.6800 (2605), 0.7000 (2606) via the new seed lines (lab output {S}/twin_L04.out; my recomputation identical in l04_numbers.txt). The page now says the share depends on the seed, the 0.01 threshold and the generator's move sizes (normal sd 0.20 for ONCA and 0.25 for ONCL, both lagged-value multiplicative, lab lines 'onca1'/'oncl1'). Correct.")

ok("L03-L04-grade-L03", "L03 why-it-matters (line ~51, fixed): the T-graded span is gone; the sentence cites Definition 2.1 and 'an A15 contract rule' with no grade. The remaining T claims in L03 (Proposition 2.2, Proposition 3.2, Proposition 3.4, the Section 4 intro identity, key-results rows 1-3) are each proved on the page; the proofs were re-derived (see the math rows).")
ok("L03-L04-grade-L04", "T-graded claims in L04 (Proposition 2.2, Corollary 2.3, Proposition 3.1, Proposition 4.1, the Section 5 derivation, Remark 2.4's reclassification claim, key-results rows 1-5, the 'two measures use the same denominator' claim) are each proved on the page or follow from Definition 1.3 and Definition 2.1 by substitution. None is an atlas contract rule graded T.")
ok("L03-L04-grade-contract-T", "Key-results row 6 (L03, fixed) is grade C with source 'A15 contract rule (the roic function raises ValueError); Lab 1 error case'; card AC2-c035 is grade C with basis 'A15 contract rule (the roic function)'. atlas/A15.contract.md lines 99-100: 'A non-positive average invested capital raises ValueError.' Definition 3.1 states the rule without a grade. Consistent with ruling 3.")

ok("L03-L04-math-L03-prop22", "Definition 2.1, Proposition 2.2 and proof (line ~85) and Remark 2.3 (line ~90) re-derived: ROIC(tau) = OI(1-tau)/avg IC; avg IC does not depend on tau; ratio (1-tau2)/(1-tau1) per firm-year. Remark 2.3: 1 - NI/OI = 1 - (1 - I/OI)(1 - tau) for NI = (OI - I)(1 - tau) (symbolic check); lab shows 0.25 each year with NI = round(0.75 OI) and no interest.")
ok("L03-L04-math-L03-prop32-34", "Proposition 3.2 (average of a sum) regrouping re-derived. Proposition 3.4 (line ~600-608): average lies strictly between year ends; exact counterexample in the proof: IC_{t-1} = 10, IC_t = -5, NOPAT = 1: average-based 1/2.5 = 2/5, year-end 1/(-5) = -1/5. P2: 100/950 and 100/1000 exact. Example 3.3 checked in L03-L04-num-L03-example33-remark35.")
ok("L03-L04-math-L03-problems-R", "P1, P2, P3 and R1-R3 read in full. P1 linearity argument and P3 averaging argument are correct as written. R1 (persistence test design), R2 (lease adjustment: OI + i L, IC + L) and R3 (operating-cash share s: IC(s) = E + D - (1-s)C, ROIC falls in s, s = 0 is the A15 convention) are correct, with no unsourced numbers.")
ok("L03-L04-math-L04-prop22", "Definition 2.1, Assumptions A1-A4 (line ~99), Proposition 2.2 and proof (lines ~107-122) re-derived: A4 gives CFO = dCash + capex - dLTD + D; A1 gives NI - D = dE; E = TA - L expansion; substitution gives NI - CFO = dCAo + dPPE - capex + dONCA - dCL - dONCL; A2 gives dPPE - capex = -D&A. Lab residuals 0.000000 (twin run).")
ok("L03-L04-math-L04-cor23", "Corollary 2.3 (lines ~127-134): dividing Proposition 2.2 by average TA gives (dONCA - dONCL)/TA; the clean-scenario and moving-scenario identity residuals in the twin are 0.000000.")
ok("L03-L04-math-L04-prop31", "Section 3 intro (line ~330) and Proposition 3.1 with proof (lines ~334-340) re-derived: NOA excludes STD; A3 gives STD = 0; NI - CFO - dNOA = -D&A - dPPE = -capex under A2. Statement and proof agree.")
ok("L03-L04-math-L04-prop41", "Proposition 4.1 and proof (lines ~349-356): numerator and denominator are linear in money items, so k cancels. P4 consistent.")
ok("L03-L04-math-L04-S5-formula", "Section 5 bullet 1 formula (line ~367), M4, quiz q9 and key-results row 4: (dSTD + dONCA - dONCL)/TA. l04_numbers.py: formula holds in 0 failures of 300 random articulated draws under A1, A2, A3' and A4' (CFF = dLTD + dSTD - D, CFI = -capex).")
ok("L03-L04-math-L04-S5-derivation", "Fixed. Section 5 now states A4' as the complete statement: dCash = CFO + CFI + CFF, CFI = -capex, CFF = dLTD + dSTD - D. Re-derived by hand: CFO = dCash + capex - dLTD - dSTD + D; NI - CFO = dCAo + dPPE - capex + dONCA - dCL + dSTD - dONCL; A2 gives -D&A, so NI - CFO = (dCA - dCash) - dCL - D&A + (dSTD + dONCA - dONCL). Numerically (ledgers/AC2/scripts/L03-L04-r4/l04_numbers.py, 300 draws): under A3' + A4' the Section 5 form has 0 failures; with CFI = -capex + 1 it fails 300/300; under A3' with A4 as written the Section 5 form fails 300/300 (so the extra term needs A4'). The round-3 gap is closed.")
ok("L03-L04-math-L04-E3-claim", "E3 solution (lines ~477-479): 1 - r^2 = 0.3241 and var(gap)/var(cf) = 0.3285 recomputed (l04_numbers.txt). The text now says these two figures differ, which is correct; 'the identity gives the gap exactly, but does not decompose the variance' is a correct reading.")
ok("L03-L04-math-L04-P-R-items", "P1 (under A4, CFF = dLTD - D: NI - CFO = dE - dCash - capex + dLTD, distributions cancel), P2 (ONCA and ONCL changes equal: example 25 CU, the condition is the difference), P3 (no assumption beyond Proposition 2.2 used), P4 (common unit across firms) and R1-R3 (design answers) re-derived. No unsourced numbers.")
ok("L03-L04-math-L04-notation", "notation/notation.json (unchanged in the round delta) registers 8 program-wide symbols (T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q), none used in L03/L04 with a different meaning. The macros used in L03/L04 are standard LaTeX (\\Delta, \\overline, \\tau, \\mathrm, \\frac, \\tfrac, \\dfrac, \\big, \\blacksquare); none is a registry macro (\\E, \\Prob, ...). The round's new text adds no new macro.")
ok("L03-L04-prose-L04-tolerance-rule", "Section 4 paragraph after Proposition 4.1 ('Scale invariance is the Scale convention of the A15 contract ...'). Matches atlas/A15.contract.md line 190 (Scale row: ratios and accrual ratios invariant to a common positive multiplier of money items). The 'not comparable across currencies' point is the same invariance read for one firm-year (Proposition 4.1 proof), not a contract claim beyond line 190.")
ok("L03-L04-prose-L04-remark24-overreach", "Remark 2.4 T claim (a reclassification of a non-zero amount between CFO and other cash-flow sections changes AC^CF and not AC^BS: CFO enters only AC^CF by Definition 1.3) and Section 5 bullet 2 (same claim, with the reporting-framework reference to AC1 concept gaap-vs-ifrs). Proved from definitions; no overreach.")
ok("L03-L04-prose-L04-every-later-measure", "Why-it-matters (line ~52, last sentence, unchanged): accruals feed L05 (accruals anomaly), L06 (discretionary accruals: L06 title and description), L07 (F-score cash-flow signal: L07 s4 'CFO* > ROA' accrual test) and L08 (M-score TATA: L08 line ~85 TATA = (NI - CFO)/TA). Each is present in the lessons as described.")
ok("L03-L04-prose-L04-remark24-first-sentence", "Fixed. Remark 2.4 now says: relaxing A3 to A3' changes CL; with A4 as written Proposition 2.2 still holds exactly; the extra term appears only when A4' books dSTD in financing. Numerically (l04_numbers.py): A3' with A4 as written -> Proposition 2.2 form holds in 300 of 300 draws (0 failures); A3' with A4' -> the Proposition 2.2 form fails 300/300, as the sentence implies. Correct.")
ok("L03-L04-prose-L04-remark14-unnamed-source", "Remark 1.4 (line ~85): AC^BS uses CL as published and has no non-current or separate short-term-debt or taxes-payable term. atlas/A15.contract.md lines 117-118: 'Short-term debt and taxes payable are not separate items in this contract ... the lesson states that simplification.' Consistent; passage unchanged.")
ok("L03-L04-prose-L04-unmarked-claims", "Re-read in full: Section 2 intro, Section 4 honest-pending paragraph, misconception 1 (negative accruals 'can have received a one-off cash payment' is hedged), R2 solution and R3 solution. No unmarked number or unmarked factual claim; the L05 reference resolves (L05 meta description, 'sorted-portfolio test').")
ok("L03-L04-prose-L03-claims-unmarked", "Re-read in full: why-it-matters (line ~51, now no grade and cites Definition 2.1 / A15 contract rule), Section 4 bullet 4 (Penman, grade C, locator unconfirmed), Section 4 bullet 2 and misconception 4 (conditional statements), quiz explanations (proved or lab-printed).")
ok("L03-L04-prose-L03-acquisition-overreach", "Section 4 bullet 2 (line ~622), misconception 4 (line ~645) and card AC2-c043: statements are conditional ('if the acquired operating income enters NOPAT from the acquisition date'); 'invested capital rises by the price' follows from the financing-side identity for a purchase at price. No overreach.")
ok("L03-L04-prose-L03-xref-remark12", "Remark 1.2 cross-references all resolve to the short-term-debt remark: Section 4 bullet 1 (line ~621), key-results row 5 (line ~765), quiz explanation (line ~826). Section 4 bullet 4 (line ~624) refers to the Penman claim, not to Remark 1.2.")
ok("L03-L04-math-L03-E3-causal", "E3 solution (L03, line ~724): the 2024 ROIC fall is driven by the operating-income decline (E1: NOPAT -22.2%, average capital +7.7%); slower capital growth offsets part of it (growth 9.6/9.0/6.5% unrounded: slowing). 'The generator sets equity by retained earnings': make_filer keeps 60% of NI (eq = prior + ni - round(0.4 ni)), so the artefact statement is correct.")
ok("L03-L04-process-words", "Lab 1 hypothesis (line ~95) states predictions before running; each prediction is checked against the printed output: deviation 1.4e-16 (rounding level), netting raises FY2023 ROIC (0.1349 vs 0.1239), 2020 invested capital absent, hypothetical 0.1287, the rate-range and non-positive-capital ValueErrors, conflicting tie raises and equal-valued tie does not.")
ok("L03-L04-banned-phrases", "Scanned L03.html, L04.html and the 33 L03/L04 cards for 'about', 'roughly', 'approximately', 'historically', 'typically', 'usually', ellipses, TODO/TBD/lorem and 'it can be shown'. Only hit: card AC2-c047 'About 23%', whose calculation (1 - 0.10/0.12989 = 0.2301) is on the same card (rule 2(c)). None in the new text.")
ok("L03-L04-struct-L03", "check_pages AC2 PASS; sections 1-9 and the problem tiers present; lab, quiz, references and the lesson nav in place; data-hours 8.")
ok("L03-L04-struct-L04", "check_pages AC2 PASS; sections 1-10 present; lab, quiz, references and the lesson nav in place; data-hours 9.")
ok("L03-L04-dag-concepts", "check_dag AC2 PASS. L04 concepts robust-statistics, outlier-detection and missing-data-mechanisms are defined in curriculum/01-foundations.yaml lines 595-598 under S0 (line 585), an unit prerequisite; gaap-vs-ifrs is AC1 (cited as such). No concept is used before its prerequisite.")
ok("L03-L04-xref-L04-to-L05", "L04 lines ~350-352 point to L05 ('sorted-portfolio test'); course/modules/AC/AC2/L05.html meta description (line 7) and why-it-matters (line 52) describe the sorted-portfolio accruals test; the L05 sorted-quintile section (line ~65) matches. Resolves.")
ok("L03-L04-hours", "data-hours 8 (L03) and 9 (L04), attribute unchanged in the round delta. My rough estimate: L03 four sections, nine problems in four tiers, one lab, nine quiz items, about 8 h; L04 five sections, fourteen problems, one lab, nine quiz items, about 9 h. Both within +/-30%.")
ok("L03-L04-lab-L03", "Lab 1 (lines ~93-577) runs under `-I -W error` (exit 0, stderr 0 bytes, 23 lines); the page's expected block equals the twin stdout (twin_check); run_labs and page_smoke PASS.")
ok("L03-L04-lab-L03-interpretation", "Fixed. Interpretation (line ~576) now reads: operating income rises from 179.3 to 186.8 over 2021-2023, then falls 22.2% to 145.3 in 2024 (unrounded 2024/2023 ratio 0.7776453, numbers_l03.txt). The expected block prints 179.3, 185.4, 186.8, 145.3 (twin output). Correct.")
ok("L03-L04-lab-L03-docstring", "Fixed. Twin docstring (lines 5-7) and page (lines 96-102) now say the lab 'prints the largest deviation of ROIC from its zero-tax value times (1 - tax_rate)'. Code: worst = max |ROIC(t) - ROIC(0)(1-t)|/|ROIC(0)|, printed as 1.4e-16; no assert in the file (grep returns nothing). The omitted word 'relative' is not an overreach because the printed line says 'relative'.")
ok("L03-L04-lab-L04", "Lab 1 (lines ~141-326) runs under `-I -W error` (exit 0, stderr 0 bytes, 12 lines); expected block equals twin stdout; the new seed loop (twin lines ~170-174) is seeded (2604, 2605, 2606) and deterministic; interpretation matches the output.")
ok("L03-L04-lab-L04-docstring", "Twin docstring lines 1-10 and 149-153 (shown on the page at lines 144-153) are unchanged in the delta (the only hunk is at line 167); they match the code: SIMULATED, seeded generator, clean-surplus derivation of NI, articulation by construction.")
ok("L03-L04-lab-numbering", "'Lab 1' references in L03 (lines ~94-95, 575-576) and L04 (line ~142) name the single lab of each page (lab-AC2-L03-1 and lab-AC2-L04-1).")
ok("L03-L04-cards-L03", f"All 17 L03 cards read against the lesson (cards_scan.py: 8 changed cards in the L03/L04 set, 25 of 33 byte-identical to 4a8690a). Changed: c035 (grade C, basis 'A15 contract rule (the roic function)'); c038 (adds the Proposition 3.4 hypotheses: both values positive, invested capital rising, NOPAT positive); c041 ('a gap of 4.31% (from unrounded values; the printed figures give 4.3%)': unrounded 4.3138%, printed-value 4.25% -> 4.3%, consistent); c046 (grade C, cite penman2013financial). Byte-identical and re-checked against the lesson: c032-c034, c036, c037, c039, c040, c042-c045, c047, c121. No duplicate fronts or backs in the 140-card set ({S}/cards_r4.txt).")
ok("L03-L04-cards-L04", f"All 16 L04 cards read against the lesson. Changed: c054 (adds 'a reclassification of zero changes neither', matching Remark 2.4); c056 (fixed: gap (dSTD + dONCA - dONCL)/average TA under A4', debt term 0.009375, sum 0.021875); c058 (no grade; cite sloan1996stock; claim matches the Crossref scope; no finding stated); c059 (grade and cite removed; claim is the lesson's own reasoning, matching Misconception 1). Byte-identical and re-checked: c048-c053, c055, c057, c060-c062, c137 (matches Definition 2.1).")
ok("L03-L04-cards-dup", f"ledgers/AC2/scripts/L03-L04-r4/cards_scan.py: 140 cards, ids contiguous c001-c140, 0 duplicate fronts, 0 duplicate backs ({S}/cards_r4.txt).")
ok("L03-L04-quiz-keys", "L03 quiz (9 items) and L04 quiz (9 items): keys match the worked solutions. L03: MC rate is an input (Section 2), 0.15 (M1), 'multiplied by 0.70/0.75' (Proposition 2.2), 0.1349, average-denominator option (Proposition 3.4), 0.1239, short-term debt omission (Remark 1.2), E2 23 (0.2301), ValueError option. L04: 0.00625 (M1), -0.01875 (M2), 'ONCA-ONCL over TA' (Corollary 2.3), distributions cancel (P1), debt inside CL (Section 5), CFO change (Remark 2.4), 0.6759 (E3), articulation is algebra not a finding, 0.021875 (M4).")
ok("L03-L04-mutants", "not applicable to this slice (no project mutants).")

rows = []
for r in r3["rows"]:
    i = r["id"]
    status, ev, fix = EV[i]
    row = {"id": i, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
    if fix:
        row["fix"] = fix
    rows.append(row)
assert set(EV) == {r["id"] for r in r3["rows"]}, (set(EV) ^ {r["id"] for r in r3["rows"]})
fails = [r for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "AC2",
    "slice": "L03-L04",
    "round": 4,
    "verifier": "round-4 independent verifier for AC2 slice L03-L04 (fresh checkout; re-read both pages, both twins, the cards and the contract; re-derived every number, the Remark 2.4 and Section 5 algebra by script, and re-ran every command row)",
    "pin": "2607c60",
    "base": "4a8690a (round-3 pin; delta used to pick the rows to re-verify)",
    "checkout": "/tmp/verify-ac2r4-l34 (detached worktree at 2607c60; untracked: .venv symlink and ledgers/AC2/)",
    "scratch": S,
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 4 of the L03-L04 slice at pin 2607c60. Every round-3 row id is kept. Every command row was re-run on the pin. "
        f"All {sum(1 for r in r3['rows'] if r['status'] != 'PASS')} round-3 FAIL rows are fixed and re-verified: the M4 attribution, the E2 inputs, the why-it-matters T grade, the contract-rule T grades (key-results row 6, card c035), the Section 5 A4' statement, the Remark 2.4 first sentence, the Lab 1 interpretation, the lab docstring, cards c041 and c056, and card c059 (grade and cite removed). "
        "Re-verification by script (ledgers/AC2/scripts/L03-L04-r4/): twin_check.py, numbers.py (unrounded L03 values), l04_numbers.py (L04 panel values, seed shares, and the algebra in 300 random draws per variant), cards_scan.py, build_fragment.py. "
        "New finding this round: L03 problem E3 computes growth 9.5% from printed values where the unrounded growth is 9.56% (9.6%). Every other rounded-input figure checked (Example 3.3, misconception 2's 4.31%, E1, E2, Remark 3.5, Remark 1.2's 0.1287) rounds the same way from unrounded and printed values. "
        "Honest notes that are not FAILs: the L04 Section 4 phrase 'has no accrual value' describes a call that raises ValueError under the contract's missing-item rule (atlas line 188); the wording is acceptable, and 'raises ValueError' would match the contract more directly. "
        "The Penman and Sloan passages were not readable; both claims stay at grade C with the locator stated as unconfirmed (ruling 1). Real EDGAR data is still honestly pending; every filer is SIMULATED."
    ),
    "summary": (
        f"AC2 L03-L04 round 4 (pin 2607c60): verdict {'FAIL' if fails else 'PASS'}. {len(rows)} rows: "
        f"{sum(1 for r in rows if r['status']=='PASS')} PASS, {len(fails)} FAIL, "
        f"{sum(1 for r in rows if r['status']=='UNVERIFIABLE')} UNVERIFIABLE. FAIL: "
        + "; ".join(f"{r['id']} ({r['check']})" for r in fails)
        + ". All other round-3 defects are fixed and verified."
    ),
}
out = root / "ledgers/AC2/L03-L04.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "fails", [r["id"] for r in fails])
