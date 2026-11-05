"""Writes ledgers/E4/E4-b.json (round 7, slice b: L04-L06 and lab twins) from the round-6 fragment and the round-7 checks.

Carried rows: a round-6 PASS row is carried only when classify_prev_rows.py reports BYTE-IDENT for it (its cited
line ranges contain no line that differs between 4bd8cb9 and 06994db). Every other row is re-verified this round,
and its evidence names the script or the output that backs it. Run from the checkout root:
.venv/bin/python ledgers/E4/scripts/E4-b-r7/write_fragment.py
"""

import json
import re

PREV = "/Users/billyribeiro/.fanout/frags/E-E4-b.round6.json"
CLASS = "ledgers/E4/scripts/E4-b-r7/outputs/classify_prev_rows.txt"
OUT = "ledgers/E4/E4-b.json"
O = "ledgers/E4/scripts/E4-b-r7/outputs"

prev = json.load(open(PREV, encoding="utf-8"))
tag = {}
for line in open(CLASS, encoding="utf-8"):
    m = re.match(r"(\S+)\s+\S+\s+(\S+)\s+hits=", line)
    if m:
        tag[m.group(2)] = m.group(1)

# Rows re-verified this round (same id, new status and evidence). Keys are round-6 row ids.
REVERIFIED = {
    "E4b-cmd-check_pages": ("E4b-cmd-check_pages", "tools/check_pages.py --unit E4 (pin 06994db)",
        f"`.venv/bin/python tools/check_pages.py --unit E4` output: 'check_pages E4: PASS' ({O}/check_pages_E4.txt, exit 0, run by ledgers/E4/scripts/E4-b-r7/run_gates.sh)."),
    "E4b-cmd-check_dag": ("E4b-cmd-check_dag", "tools/check_dag.py --unit E4",
        f"`tools/check_dag.py --unit E4` output: 'check_dag E4: PASS' ({O}/check_dag_E4.txt, exit 0)."),
    "E4b-cmd-check_projects": ("E4b-cmd-check_projects", "tools/check_projects.py --unit E4 (unit gate, out of slice)",
        f"`tools/check_projects.py --unit E4` output: 'check_projects E4: PASS' ({O}/check_projects_E4.txt, exit 0)."),
    "E4b-cmd-run_labs": ("E4b-cmd-run_labs", "tools/run_labs.py --unit E4, --page L04, --page L05, --page L06",
        f"`tools/run_labs.py --unit E4` output 'run_labs E4: PASS (12/12)'; per page 'PASS (1/1)' for L04, L05, L06 ({O}/run_labs_*.txt, exit 0)."),
    "E4b-cmd-twins-isolated": ("E4b-cmd-twins-isolated", "python -I -W error on each of the three L04-L06 twins",
        f"Each twin run alone as `.venv/bin/python -I -W error tests/labs/E4/lab-E4-L0n-1.py`: exit 0 for L04, L05, L06 ({O}/_summary.txt lines 'twin_L04..L06 exit=0'). L06 output re-run by hand this round: Part C 'zero_residuals 16 all_zero True', Part E 'within True' twice."),
    "E4b-cmd-page-code-equals-twin": ("E4b-cmd-page-code-equals-twin", "L04.html, L05.html, L06.html lab blocks vs twins",
        f"`ledgers/E4/scripts/E4-b-r7/expected_vs_output.py` (its output {O}/expected_vs_output.txt): 'L04: code_equals_twin=True', 'L05: code_equals_twin=True', 'L06: code_equals_twin=True'."),
    "E4b-cmd-expected-equals-output": ("E4b-cmd-expected-equals-output", "L04.html expected block, L05.html expected block, L06.html expected block",
        f"Same script ({O}/expected_vs_output.txt): 'expected_equals_output=True' for L04, L05, L06, each run with exit 0 and empty stderr."),
    "E4b-cmd-ruff-mypy": ("E4b-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental on the three twins",
        f"`ruff check tests/labs/E4 tests/test_labs.py tests/test_run_labs.py`: 'All checks passed!'; `ruff format --check tests/labs/E4`: '12 files already formatted'; mypy: 'Success: no issues found in 3 source files' ({O}/ruff_check.txt, ruff_format.txt, mypy_twins.txt)."),
    "E4b-cmd-pytest-labs": ("E4b-cmd-pytest-labs", "pytest -k E4 tests/test_labs.py tests/test_run_labs.py",
        f"`pytest -o addopts='' -q -k E4 tests/test_labs.py tests/test_run_labs.py`: '13 passed, 352 deselected' ({O}/pytest_E4.txt)."),
    "E4b-cmd-page_smoke": ("E4b-cmd-page_smoke", "tools/page_smoke.py --unit E4 --pages L04 L05 L06 (run alone)",
        f"Output 'page_smoke modules/E/E4/L04.html: PASS', 'L05.html: PASS', 'L06.html: PASS', 'page_smoke E4: PASS' ({O}/page_smoke_E4.txt). The tool checks zero console errors, no external requests and no horizontal scroll at 360 px (tools/page_smoke.py lines 5-12)."),
    "E4b-cmd-verify_refs-live": ("E4b-cmd-verify_refs-live", "tools/verify_refs.py --unit E4 (live Crossref run)",
        f"'live re-verification of E4: 3 of 560 entries, 0 problems' ({O}/verify_refs_unit_E4.txt, exit 0). Recorded run; plain tool invocation, no bot check involved."),
    "E4b-cmd-verify_refs-offline": ("E4b-cmd-verify_refs-offline", "tools/verify_refs.py --offline",
        f"'offline integrity: 560 entries, 0 problems' ({O}/verify_refs_offline.txt, exit 0)."),
    "E4b-L04-math-lemma21": ("E4b-L04-math-lemma21", "course/modules/E/E4/L04.html:101-104 (Lemma 2.1, changed proof line 103)",
        "Changed line 103 read in full (ledgers/E4/scripts/E4-b-r7/outputs/view_L04.txt). The new proof adds the finite echelon reduction (first nonzero column, swap, clear below, repeat on the lower right block) and the count argument is unchanged. Each step is a row operation that preserves the row space (stated in line 102). Checked against L04 Lab 1 Part A ranks 2 and 3 (twin run). PASS."),
    "E4b-L04-math-remark32": ("E4b-L04-math-remark32", "course/modules/E/E4/L04.html:270-272 (Remark 3.2, changed line 271)",
        "Changed line 271: the kernel is now written {zeta in R^J : zeta^T A = 0} and has dimension J - rank(A) by rank-nullity (the map zeta -> zeta^T A has rank rank(A)). Example 2.3 check: J = 4, rank 3, kernel dimension 1, and (1,2,3) is replicated by (1,2,3,0) and (0,0,0,1) (line 271; independent_checks.py 'L04 Remark 3.2 kernel dim J - rank' OK). PASS."),
    "E4b6-L04-prop42-proof-link": ("E4b6-L04-prop42-proof-link", "course/modules/E/E4/L04.html:293 (Proof of Proposition 4.2)",
        "Round-6 FAIL is resolved. Changed line 293 now begins 'Let zeta, phi >= 0 with xi = zeta^T A and eta = phi^T A, and let a, b >= 0', so xi and eta are linked to the portfolios zeta and phi used in the proof. The closure a xi + b eta = (a zeta + b phi)^T A in C(A) is then checked line by line. For A = I_2, (-1,0) has a negative entry and is not in C(I_2). PASS."),
    "E4b-L05-sec5-wording": ("E4b-L05-sec5-wording", "course/modules/E/E4/L05.html:292-296 (changed line 295)",
        "Changed line 295 reads 'The forecasts are correct by construction, inside the model.' Definition 1.2 (L05 line 73) defines the equilibrium forecast as the conditional expectation of the price the model produces, so the statement holds inside the model. The next sentence disclaims any claim about real forecasts. Section 5 of the lesson otherwise unchanged. PASS."),
    "E4b-L05-math-muth-scope": ("E4b-L05-math-muth-scope", "course/modules/E/E4/L05.html:295-296",
        "Line 295 changed as above (scope limited to the model; no claim about real forecasts). Line 296 unchanged: the Muth sentence cites the title only. Registry record muth1961rational: title 'Rational Expectations and the Theory of Price Movements', Econometrica 29(3), 1961 (references/references.json, verified by crossref); the live Crossref run above reports 0 problems. PASS."),
    "E4b-grades-L05": ("E4b-grades-L05", "course/modules/E/E4/L05.html:295, 423-432 (grade table)",
        "Key-results table (lines 427-433) read this round: each row carries T (Lemma 2.1, Proposition 2.2, Corollary 2.3, Lemma 3.1, Proposition 3.2, Proposition 3.3) or a lab citation. The base-instance row (433) matches Lab 1 Parts A and B output '(4, -3/10)' and 'c0_error_ratios -1/4'. Line 295 changed and is consistent with the table. PASS."),
    "E4b3-L05-footer-muth": ("E4b3-L05-footer-muth", "course/modules/E/E4/L05.html:515 (footer), :296 (Muth line; round-6 locator 295 now holds the scope sentence)",
        "Footer line 515 unchanged ('E4 · General Equilibrium & Information in Markets · Each graded result carries a proof or a lab result.'). The Muth sentence is at line 296 (locator corrected from 295). PASS."),
    "E4b3-L05-definition12-traders": ("E4b3-L05-definition12-traders", "course/modules/E/E4/L05.html:73, 294 (unchanged), 295 (changed)",
        "Definition 1.2 (line 73) takes the traders to know the price rule and the forecast is the conditional expectation; line 295 (changed) says the forecasts are correct by construction inside the model, which follows from that definition. PASS."),
    "E4b4-muth-crossref": ("E4b4-muth-crossref", "course/modules/E/E4/L05.html:296; references/references.json muth1961rational; verify_refs --unit E4 live",
        "Title in the registry, 'Rational Expectations and the Theory of Price Movements' (Econometrica 29(3)), matches the phrase quoted on line 296 ('The phrase rational expectations appears in the title of Muth (1961)'). Live Crossref re-resolution: 0 problems (E4b-cmd-verify_refs-live). The paper itself was not opened; the attribution is to the title only, as the page states. PASS."),
    "E4b-L06-example69-remark610": ("E4b-L06-example69-remark610", "course/modules/E/E4/L06.html:228-236 (changed line 235)",
        "Changed line 235 now reads 'for every sigma_u^2 >= 0' (the variance, not the standard deviation, is the parameter of Definition 6.1). Recomputed Example 6.9 by exact Fractions: kappa = 2, sigma_eta^2 = 2, tau_eta = 1/2, tau_bar = 3/4, theta_s = 3/7, theta_u = 6/7, slope b = 7/9, V_U = 2/3, x_I = 1/7, x_U = -1/7 (independent_checks.py, all L06 checks OK; twin Part A/B/C output). Remark 6.10 algebra: sigma_eta^2 - sigma_eps^2 = kappa^2 sigma_u^2 >= 0, so sigma_eta^2 >= sigma_eps^2 > 0. PASS."),
    "E4b-L06-misconceptions": ("E4b-L06-misconceptions", "course/modules/E/E4/L06.html:493-513 (changed line 503)",
        "Changed line 503 (noise-trader misconception) now says the informed and uninformed investors are 'the optimizing agents of the model, each with the CARA utility of Definition 6.2', and that u is a primitive. Definition 6.2 (line 66) is CARA with coefficient a > 0 and w = w_0 + x(v - p); Definition 6.1 (line 57) defines the noise trader as a supply u. Line 499 ('At the base instance it is 2') matches Lab 1 Part A 'sig_eta2 2'. PASS."),
    "E4b-L06-problems-E": ("E4b-L06-problems-E", "course/modules/E/E4/L06.html:571-591 (changed line 590)",
        "Changed E3 solution (line 590): the sample is generated from the same model, so the check tests the closed form against a simulation of that model; no observed price enters. Matches the lab's Part E code (tests/labs/E4/lab-E4-L06-1.py part_e: draws v, eps, u and regresses; no data read). E2 solution numbers recomputed: 0.426617 - 3/7 = -0.001954; /0.006497 = -0.30; SE = 0.006497/3 = 0.002166; -0.001954/0.002166 = -0.90 (independent check 'L06 E2'). PASS."),
    "E4b4-notation-eta": ("E4b4-notation-eta", "course/modules/E/E4/L06.html:179-235 (eta in Prop 6.7, Step 2 line 193, Cor 6.8, Remark 6.10 line 235); course/modules/E/E4/L05.html (no eta)",
        "Corrected locator: the round-6 citation L05.html:58-60 contained no eta (the match was the substring 'beta'); a grep of L05 for \\eta finds nothing. In L06, eta is defined at line 193 ('Y - v = eps - kappa' u =: eta') before its uses at 203, 208, 218, 225 and 235. The symbol is not in notation/notation.json, so no registry meaning is overridden. PASS (evidence corrected, status unchanged)."),
    "E4b6-in-general-scan": ("E4b6-in-general-scan", "course/modules/E/E4/L04.html:271, 386; course/modules/E/E4/L05.html:292",
        "L04:271 (changed) uses 'In general' for the rank-nullity statement, which is computed in the same sentence (rank of zeta -> zeta^T A equals rank(A); kernel dimension J - rank(A)). L05:292 ('not of rational expectations in general') is a negated disclaimer. L04:386 unchanged. PASS."),
    "E4b-dag-closure": ("E4b-dag-closure", "L04-L06 text, math and links (grep scans, this round)",
        "grep over L04-L06 for out-of-closure names (state price, stochastic discount, martingale, Bayes, efficient markets, Banach, intermediate value, determinacy, Kyle, risk-neutral, fundamental theorem): no hit (exit 1 from grep, no match). Concept links present: market-completeness, rational-expectations-equilibrium, noisy-rational-expectations-equilibrium, arrow-debreu-security, random-variable, normal-distribution, expectation, conditional-expectation-elementary, vector-space, variance, multivariate-normal, linear-map, least-squares-projection, independence, expected-utility, crra-utility (E3), competitive-equilibrium (E1). check_dag E4 PASS (E4b-cmd-check_dag). PASS."),
    "E4b-concept-definitions": ("E4b-concept-definitions", "course/modules/E/E4/L04.html:77, 102, 292; L05.html:59, 73; L06.html:57, 67, 96, 169",
        "Each dfn grep'd this round: market-completeness (L04:77), rational-expectations-equilibrium (L05:73), noisy-rational-expectations-equilibrium (L06:169) with data-concept; plain dfn for payoff matrix, portfolio, attainable, rank, augmented rank, echelon form, pivot, convex cone, public signal, affine, CARA, signal, noise trader, precisions, informed fraction, posterior. Each lesson defines its own concept before first use. PASS."),
    "E4b-notation-registry": ("E4b-notation-registry", "course/modules/E/E4/L04.html, L05.html, L06.html; notation/notation.json",
        f"ledgers/E4/scripts/E4-b-r7/notation_scan.sh ({O}/notation_scan.txt): no mathbb anywhere in L04-L06 (the reals use \\R, 37 uses; expectations \\E, 43; \\Var, \\Cov, \\Corr, \\Normal used); no \\Phi, no \\gamma_3 or \\gamma_4, no R^\\ast, R_f or \\mathbb{{Q}}, no \\CE. Registered-macro meanings are unchanged. PASS."),
    "E4b-L05-notation-gamma": ("E4b-L05-notation-gamma", "course/modules/E/E4/L05.html (all), notation/notation.json",
        f"notation_scan.sh over L05 ({O}/notation_scan.txt): no gamma, Phi, T or R^\\ast symbol in L05; the new macro uses are unchanged. PASS."),
    "E4b4-notation-s": ("E4b4-notation-s", "course/modules/E/E4/L04.html (all); L06.html:57",
        f"notation_scan.sh: no bare s symbol in L04 (grep of \\(s\\b and s_ returns nothing, {O}/notation_scan.txt). L06:57 defines s = v + eps as the signal (Definition 6.1). PASS."),
    "E4b4-notation-x": ("E4b4-notation-x", "course/modules/E/E4/L04.html (all); L06.html:66, 82, 162, 169, 192, 230, 682",
        f"notation_scan.sh: no bare x symbol in L04 (holdings are zeta). L06 defines x as the risky holding in Definition 6.2 (line 66, 'x is the risky holding'), and uses it for CARA demands (lines 102, 162). PASS."),
    "E4b4-cards-L04-L06": ("E4b4-cards-L04-L06", "course/modules/E/E4/cards.json: all 228 cards; L04 27, L05 28, L06 33",
        f"Full scan this round (ledgers/E4/scripts/E4-b-r7/cards_scan.py, {O}/cards_scan.txt): 228 cards, no duplicate ids, no duplicate fronts. Process-word scan of every card: 0 hits. Numbered-reference scan of all cards: 6 unmatched strings, all examined: E4-c054 ('Assumption A3 (unrestricted holdings)', L04:60), E4-c074 (A3, L05:60), E4-c075 (A1, L05:58), E4-c076 (A2, L05:59) are the lesson's own labels 'A1 (parameters).' etc., so the card text matches the page; E4-c209 and E4-c210 ('Problem Res 1/3', L09) are out of this slice. Changed and new cards in L04-L06 read in full (rows E4b7-cards-changed and E4b7-cards-new). PASS."),
    "E4b4-independent-checks": ("E4b4-independent-checks", "ledgers/E4/scripts/E4-b-r6/independent_checks.py (re-run this round at 06994db)",
        "`.venv/bin/python -I ledgers/E4/scripts/E4-b-r6/independent_checks.py`: every check OK, last line 'ALL OK' (exact Fractions; L04 ranks, Remark 3.2 kernel, Prop 4.2 construction; L05 fixed points and error ratios; L06 Example 6.9, Parts B to D, M1 to M3, E1 and E2). PASS."),
    "E4b6-delta-review": ("E4b6-delta-review", "delta 4bd8cb9..06994db within the slice: L04.html:103, 271, 293; L05.html:295; L06.html:235, 488, 503, 590; cards.json (29 changed, 8 new in all lessons); tests/labs/E4 L04-L06 twins unchanged",
        "Round 7 delta review: every hunk read in full. L04:103 (Lemma 2.1 proof, finite echelon reduction): PASS. L04:271 (Remark 3.2, kernel written as a set, rank-nullity): PASS. L04:293 (Prop 4.2 proof now linked to xi and eta): PASS. L05:295 ('correct by construction, inside the model'): PASS. L06:235 (sigma_u^2 >= 0): PASS. L06:488 (Cov(v,p) = theta_s sigma_v^2 - theta_u Cov(v,u)): PASS, checked by hand from p = theta_s s - theta_u u with s = v + eps. L06:503 (noise trader, CARA): PASS. L06:590 (E3 solution): PASS. Changed cards in L04-L06: rows E4b7-cards-changed. Out-of-slice hunks (L07 twin, project-3 twin, index is unchanged, FINAL-ARCHITECT-RULINGS.md, L01-L03, L07-L09 pages) are not verified here. PASS."),
    "E4b-page-width-360": ("E4b-page-width-360", "tools/page_smoke.py --unit E4 --pages L04 L05 L06 (browser run, 360 px and desktop, light and dark)",
        f"page_smoke checks each page at 360 px for horizontal scroll (tools/page_smoke.py line 341-343), console errors and external requests. Output {O}/page_smoke_E4.txt: L04, L05 and L06 each PASS. No horizontal scroll reported at 360 px. PASS."),
    "E4b-banned-process-words": ("E4b-banned-process-words", "L04.html, L05.html, L06.html visible prose and code; cards.json",
        "Scans this round: process words (build, builder, verifier, round, fixer, REQUEST, ledger, planner, architect, agent, precedent) with grep -i over the three pages and over all cards: 0 hits. Banned phrases of BUILDER_RULES 1.3-1.4 (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, well known, obviously, clearly): 0 hits. Ellipses appear only in Python type hints inside lab code. PASS."),
    "E4b-struct-L04": ("E4b-struct-L04", "course/modules/E/E4/L04.html (sections, order, footer)",
        "Changed lines 103, 271, 293 are paragraph bodies (see E4b7-struct-delta-prose-only). Section order and template blocks are byte-identical to 4bd8cb9 apart from those paragraph texts. check_pages E4 PASS this round. Footer line 524 unchanged. PASS."),
    "E4b-struct-L05": ("E4b-struct-L05", "course/modules/E/E4/L05.html (sections, order, footer)",
        "Changed line 295 is a paragraph body (see E4b7-struct-delta-prose-only). Section order, ids and footer line 515 byte-identical to 4bd8cb9. check_pages E4 PASS this round. PASS."),
    "E4b-struct-L06": ("E4b-struct-L06", "course/modules/E/E4/L06.html (sections, order, footer)",
        "Changed lines 235, 488, 503, 590 are paragraph or list-item bodies (see E4b7-struct-delta-prose-only). Section order and ids byte-identical to 4bd8cb9. check_pages E4 PASS this round. PASS."),
    "E4b-simulated-labels": ("E4b-simulated-labels", "course/modules/E/E4/L06.html SIMULATED labels; L04.html and L05.html (no random draws)",
        "grep -c SIMULATED: L06 has 9 occurrences, including the Part E label in the lab block and the expectation text at lines 238 and 252. L04 and L05 contain no SIMULATED label and their twins use no random draws (tests/labs/E4/lab-E4-L04-1.py line 19, lab-E4-L05-1.py line 24: 'no random draws'), so no SIMULATED label is required there. PASS."),
    "E4b6-cards-changed": ("E4b6-cards-changed","course/modules/E/E4/cards.json: E4-c086, c107, c121, c123, c218",
        "Carried from round 6 (cards E4-c086, c107, c121, c123, c218 are JSON-identical between 4bd8cb9 and 06994db; checked by comparing the parsed objects, card_diff.py output, ledgers/E4/scripts/E4-b-r7/outputs/card_diff.txt: not in the changed list): the round-6 PASS holds for these five unchanged cards. PASS."),
}

# Rows that are new this round.
NEW_ROWS = [
    {"id": "E4b7-cards-changed", "check": "2.7-retrieval-cards (changed cards in L04-L06)",
     "location": "course/modules/E/E4/cards.json: E4-c065, c090, c094, c103, c104, c120, c122, c124, c125, c219",
     "status": "PASS",
     "evidence": "Each changed card read against its lesson text and the lab output. c065 (L04, augmented ranks (1,2,3)=2 attainable, (0,0,1) and (5,0,0)=3 not, Lab 1 Part C). c090, c094, c219 (L05; fixed point (4,-3/10) and damped-step lines in Lab 1 Parts A and E; c219 with alpha=10, beta=2, varsigma=2, delta=3/4 gives (5/2, -3/16), Part C). c103 (CARA is Definition 6.2), c104 (informed fraction, A2), c120 (x_I=1/7, Part C), c122 (16 residuals zero, Part C), c124 and c125 (sample slopes within tolerance, Part E, 'within True'). All consistent with the page and the twin output. PASS."},
    {"id": "E4b7-cards-new", "check": "2.7-retrieval-cards (new cards in L04-L06)",
     "location": "course/modules/E/E4/cards.json: E4-c226, c227, c228 (L04), c229 (L05), c230, c231 (L06)",
     "status": "PASS",
     "evidence": "Read against the lesson text: c226 = Proposition 1.5 (augmented rank); c227 = Lemma 2.1 (echelon form, pivot); c228 = convex cone and C(A) in the proof of Proposition 4.2; c229 = A2 and A3 of L05 (public signal z, normal, mean zero, independent of u and upsilon); c230 = Definition 6.1 (s = v + eps) and A2; c231 = posterior, L06 section 2 line 96. Each card is atomic and its 'back' is what the page says. No card cites a registry key, which is correct for model results. PASS."},
    {"id": "E4b7-twin-lab-L04-L06-hunks", "check": "2.5-labs (twins unchanged, page code equals twin)",
     "location": "tests/labs/E4/lab-E4-L04-1.py, lab-E4-L05-1.py, lab-E4-L06-1.py",
     "status": "PASS",
     "evidence": "git diff 4bd8cb9..06994db shows no change to the three L04-L06 twins (the changed twins are lab-E4-L07-1.py and lab-E4-project-3.py, out of slice). expected_vs_output.py: code block equals twin for all three, and expected output equals the twin run. PASS."},
    {"id": "E4b7-scan-process-banned", "check": "2.9-structure-prose (process words and banned phrases)",
     "location": "course/modules/E/E4/L04.html, L05.html, L06.html, cards.json",
     "status": "PASS",
     "evidence": "grep -i over the three pages for build, builder, verifier, verif(y|ied), round, fixer, REQUEST, unit report, ledger, planner, architect, agent, precedent: no hit (ledgers/E4/scripts/E4-b-r7/outputs/grep output, plus the card scan). grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, important to note, studies show, experts agree, well known, obviously, clearly: no hit. The only ellipses are in Python code (tuple[Fraction, ...]) inside lab blocks, which the rule allows. PASS."},
    {"id": "E4b7-struct-delta-prose-only", "check": "2.9-structure-prose (section order and template sections)",
     "location": "course/modules/E/E4/L04.html, L05.html, L06.html (headings, section tags, footers)",
     "status": "PASS",
     "evidence": "Every changed line of the three pages (L04:103, 271, 293; L05:295; L06:235, 488, 503, 590) is a paragraph or list-item body, not a heading, section, nav or footer tag (git diff -U0 output, this round). Section order, ids and the footer are therefore byte-identical to 4bd8cb9, and check_pages E4 PASS covers the template. PASS."},
]


def row_out(row):
    return {k: row[k] for k in ("id", "check", "location", "status", "evidence")}


rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in REVERIFIED:
        rid2, loc, ev = REVERIFIED[rid]
        rows.append({"id": rid2, "check": r["check"], "location": loc, "status": "PASS", "evidence": ev})
        continue
    if tag.get(rid) == "BYTE-IDENT":
        rows.append({
            "id": rid,
            "check": r["check"],
            "location": r["location"],
            "status": "PASS",
            "evidence": (f"Carried from round 6 ({r['location']} byte-identical since the previous pin 4bd8cb9; "
                         f"the cited lines contain no changed line, per classify_prev_rows.py, {CLASS}): "
                         + r["evidence"]),
        })
        continue
    raise SystemExit(f"row {rid} is {tag.get(rid)} and has no round-7 re-verification entry")

for n in NEW_ROWS:
    rows.append({**n, "evidence": n["evidence"]})

# Re-verified command rows that are not in the round-6 list are none; all listed command rows are re-run above.
missing = [k for k in REVERIFIED if k not in seen]
assert not missing, missing

fragment = {
    "unit": "E4",
    "slice": "b",
    "round": 7,
    "verifier": "Haiku independent verifier, E4-b round 7 (did not build E4)",
    "pin": "06994db1 (06994db); the checkout is detached at this pin",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin 4bd8cb9; round-6 fragment /Users/billyribeiro/.fanout/frags/E-E4-b.round6.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-E4-b",
    "scratch": "ledgers/E4/scripts/E4-b-r7/ (run_gates.sh, expected_vs_output.py, strip_view.py, notation_scan.sh, cards_scan.py, classify_prev_rows.py, write_fragment.py, outputs/)",
    "verified_at": "2026-11-04",
    "verdict": "PASS",
    "rows": [row_out(r) for r in rows],
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is lessons L04 to L06 and their three lab twins. It is not a project slice, so no mutants or alternatives are written here; the grader and the ten mutants belong to the project slice.",
        "Delta 4bd8cb9..06994db in the slice: L04.html lines 103, 271, 293; L05.html line 295; L06.html lines 235, 488, 503, 590; cards.json (E4-c065, c090, c094, c103, c104, c120, c122, c124, c125, c219 changed; c226 to c231 new). Twins unchanged.",
        "The round-6 FAIL (E4b6-L04-prop42-proof-link) is resolved: the Proposition 4.2 proof now names xi and eta.",
        "Row E4b4-notation-eta had a wrong locator in round 6 (L05.html:58-60 contains no eta); the symbol check itself stands and is corrected in the evidence.",
        "Out-of-slice observations, not verified here: cards E4-c209 and E4-c210 cite 'Problem Res 1/3' in L09 (not in this slice's pages); cards E4-c225 (L03) and E4-c232 (L09) are new; lab-E4-L07-1.py and lab-E4-project-3.py changed.",
    ],
    "summary": "",
}
counts = {}
for r in fragment["rows"]:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment["summary"] = (f"PASS E4-b round 7: rows={len(fragment['rows'])} (pass={counts.get('PASS', 0)}, fail=0, unverifiable=0). "
                       "All command gates re-run at 06994db and PASS. Round-6 FAIL resolved. Carried rows: "
                       f"{sum(1 for r in fragment['rows'] if r['evidence'].startswith('Carried from round 6'))}.")
with open(OUT, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", OUT, len(fragment["rows"]), "rows")
