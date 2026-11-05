# SC1 slice a, round 9 verifier: fragment builder. Written by the round-9 verifier from its own full re-read of
# index.html, L01-L03 and the three lab twins at c93dd52 (previous pin 0dee921a, the round-8 pin).
# Usage (from the checkout root): .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r9/build_fragment_r9.py
# Rows re-verified in this round carry round-9 evidence. Every other round-8 PASS row is carried only when its cited
# lines are byte-identical since 0dee921a (checked by mechanical_carry_check.py against git diff -U0 0dee921a c93dd52).
import json
import re
from pathlib import Path

ROOT = Path.cwd()
PIN = "c93dd526025c6dffd34c54cd2c89eb62a890f885"
BASE = "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3"
PREV = Path("/Users/billyribeiro/.fanout/frags/E-SC1-a.round8.json")
SCRIPTS = "ledgers/SC1/scripts/SC1-a-r9/"
prev = json.loads(PREV.read_text(encoding="utf-8"))
prev_by_id = {r["id"]: r for r in prev["rows"]}

CARRY = (
    "Carried from round 8 (cited lines byte-identical since the previous pin 0dee921a; "
    "git diff -U0 0dee921a c93dd52 does not touch them): "
)


def stripped(evidence: str) -> str:
    if evidence.startswith("Carried from round") and "): " in evidence:
        return evidence.split("): ", 1)[1]
    return evidence


# ---- rows re-verified in round 9 (check, location, status, evidence[, fix]) ----
FRESH: dict[str, dict[str, str]] = {
    "SC1a-gate-check-pages": {
        "check": "2.9-structure-tool",
        "location": "index.html, L01.html, L02.html, L03.html, cards.json",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: .venv/bin/python tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 "
        f"({SCRIPTS}check_pages.out).",
    },
    "SC1a-gate-check-dag": {
        "check": "2.9-dag-tool",
        "location": "index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 "
        f"({SCRIPTS}check_dag.out). Owners of every concept link on the four pages, and their closure membership, are in "
        f"{SCRIPTS}concept_owner_r9.out (all in {{M1, M2, M4, M5, M6, P0.1}} or SC1).",
    },
    "SC1a-gate-run-labs": {
        "check": "2.5-labs-run",
        "location": "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: tools/run_labs.py --unit SC1 --page L01, --page L02, --page L03 each -> "
        f"'run_labs SC1: PASS (1/1)', exit 0 ({SCRIPTS}run_labs_L01.txt, run_labs_L02.txt, run_labs_L03.txt). "
        "The unit-wide run was not repeated; the other units' labs are outside this slice.",
    },
    "SC1a-gate-page-smoke": {
        "check": "2.9-page-smoke",
        "location": "index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52, run alone: tools/page_smoke.py --unit SC1 --pages index.html L01.html L02.html L03.html "
        f"(no --skip-sweep; the pages carry no figure, so the sweep has nothing to sweep) -> 'page_smoke SC1: PASS', exit 0 "
        f"({SCRIPTS}page_smoke.out). The run includes the labs in Pyodide, zero console errors, zero unrendered math, no "
        "external requests and no horizontal scroll at 360 px, as the tool reports.",
    },
    "SC1a-gate-lint-types-tests": {
        "check": "2.5-ruff-mypy-pytest",
        "location": "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py; pytest -k SC1",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: ruff check on the three twins 'All checks passed!' and ruff format --check '3 files "
        f"already formatted' ({SCRIPTS}ruff.out); mypy --no-incremental on the three twins 'Success: no issues found in 3 "
        f"source files' ({SCRIPTS}mypy.out); pytest -k SC1 collects 11 tests (tests/test_labs.py) and all 11 PASSED, exit 0 "
        f"({SCRIPTS}pytest_sc1.out).",
    },
    "SC1a-gate-verify-refs": {
        "check": "2.1-citations",
        "location": "course/modules/SC/SC1/index.html:182 (data-cite shreve2004stochastic)",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 "
        f"({SCRIPTS}verify_refs.out). The key shreve2004stochastic is in references/references.json (Shreve, Stochastic "
        "Calculus for Finance II, 2004; openlibrary record); the live run was not made (a network run; references/ is not "
        "changed between the two pins).",
    },
    "SC1a-lab-L01-twin": {
        "check": "2.5-lab-L01",
        "location": "tests/labs/SC1/lab-SC1-L01-1.py; L01.html:137-206",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: {SCRIPTS}twin_check.py (run from the checkout): the page code equals the twin file "
        "exactly; the twin run as python -I -W error from an empty temporary directory exits 0 with 0 stderr bytes; stdout "
        f"equals the expected block exactly ({SCRIPTS}twin_check.out, 'lab-SC1-L01-1 ... OK').",
    },
    "SC1a-lab-L02-twin": {
        "check": "2.5-lab-L02",
        "location": "tests/labs/SC1/lab-SC1-L02-1.py; L02.html:168-279",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: {SCRIPTS}twin_check.py: page code equals the twin; run as python -I -W error from an "
        f"empty directory, exit 0, 0 stderr bytes; stdout equals the expected block exactly ({SCRIPTS}twin_check.out).",
    },
    "SC1a-lab-L03-twin": {
        "check": "2.5-lab-L03",
        "location": "tests/labs/SC1/lab-SC1-L03-1.py; L03.html:131-252",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: {SCRIPTS}twin_check.py: page code equals the twin; run as python -I -W error from an "
        f"empty directory, exit 0, 0 stderr bytes; stdout (16 z lines, 16 exact-sum lines and the headers) equals the "
        f"expected block exactly ({SCRIPTS}twin_check.out).",
    },
    "SC1a-lab-claims-L01": {
        "check": "2.5-lab-claims",
        "location": "tests/labs/SC1/lab-SC1-L01-1.py:1-9 (docstring, shown at L01.html:137-145); L01.html:136 and :208",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: printed lines 'dyadic variance sums equal t: 15 of 15 cases (depths 0 to 4)', "
        "'covariance equals min(s, t) on the grid: 81 of 81 pairs', 'Cov(B at 1/4, B at 5/8) = 1/4; min ... = 1/4' "
        f"({SCRIPTS}twin_check.out). The hypothesis (:136) and interpretation (:208) state the same counts and values; the "
        "docstring (exact Fraction arithmetic, nothing random, no file read) matches the code.",
    },
    "SC1a-lab-claims-L03": {
        "check": "2.5-lab-claims",
        "location": "course/modules/SC/SC1/L03.html:133 (hypothesis), :253 (interpretation), :343 (E1)",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52, re-read of the changed lines: :133 gives the theoretical standard error H*sqrt(2/N)/20 "
        "from Var(Q)=2H^2/N and the 400 paths, which is what the code computes (sample se = sqrt(variance/400)); :253 gives "
        "the theoretical value sqrt(2)/20 = 0.0707 at H=1, N=1 against the printed 0.0718, and 2*(1/8)/20 = 0.0125 at H=2, "
        "N=128 against the printed 0.0125; the largest |z| 2.39 (H=1, N=2) and next 1.84 are the printed values "
        f"({SCRIPTS}numbers_r9.out). :343: only z = 2.39 exceeds 2 in absolute value ({SCRIPTS}numbers_r9.out).",
    },
    "SC1a-lab-L02-docstring": {
        "check": "2.5-lab-claims",
        "location": "tests/labs/SC1/lab-SC1-L02-1.py:1-8 (docstring, shown at L02.html:171-178)",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: the docstring claims (SIMULATED; the dyadic count and the grid-supremum line hold for "
        "every seed; exact binary values at dyadic points; a level term beyond the depth of a point is exactly 0.0 there; "
        "six decimals from unrounded values) match the code at lines 190-246 and the printed lines "
        f"(216 of 216; True; 8 of 8) in {SCRIPTS}twin_check.out. The exact-zero claim holds because for m above the depth of t, "
        "|t - centre| >= 2^-m, so 1 - 2^m|t - centre| <= 0 exactly and max(0.0, .) returns 0.0.",
    },
    "SC1a-numbers-L03": {
        "check": "2.2-numbers",
        "location": "course/modules/SC/SC1/L03.html:253, :270, :275, :343, :350, :357, :368, :375, :398, :434",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: {SCRIPTS}numbers_r9.py recomputes every printed value: the theoretical se "
        "H*sqrt(2/N)/20 for all 16 cells (H=1,N=1: 0.070711 vs printed 0.0718; H=2,N=128: 0.012500 vs printed 0.0125); exact "
        "sums 5/8 (H=1,N=2), 85/32 = 2.65625 (H=2,N=8), 21845/131072 = 0.166664 (H=2,N=128), 21845/2097152 = 0.010417 "
        "(H=1,N=128), each equal to the closed form; largest |z| 2.39 and next 1.84; sqrt(2/pi) = E|Z| (P3); 4080/1536 = "
        "2.65625; 1/80 = 0.0125; 2t^2/N; c = 2; 15/24 = 0.625.",
    },
    "SC1a-numbers-L03-SE-follow": {
        "check": "2.2-numbers",
        "location": "course/modules/SC/SC1/L03.html:398 (key-results row, grade C)",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52, {SCRIPTS}numbers_r9.out: the gap printed se / (H*sqrt(2/N)/20) - 1 over the 16 cells "
        "has its largest value +13.21% at H=2, N=1 (printed 0.1601, theoretical 0.141421); the next are +9.18% (H=2, N=4) and "
        "+7.60% (H=1, N=2). 'Within 14 percent' and 'the largest, 13.2 percent, is at H=2, N=1' hold, and the means lie within "
        "+-3 se (largest |z| 2.39).",
    },
    "SC1a-exercises-L01-L03": {
        "check": "2.4-problems",
        "location": "course/modules/SC/SC1/L01.html:246-427; L02.html:351-520; L03.html:289-385",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: every worked solution in the three problem sets re-read and re-derived by hand. L01: M1 "
        "(Cov 1/3, Var 1/3), M2, M3 (Cov(B1,B2)=1; Var(3B1-B2)=9+2-6=5), P1-P3, E1 (3/64; 16*3/64=3/4), E2 (2*1/8=1/4), E3 "
        "(9*9=81), R1-R2. L02: M1 (Lambda_{2,1}: 0, 1, 0), M2 (Sigma_1(1/2)=xi0/2+xi11/2), M3 (Var U_1 = 1/4 at n=1), P1 "
        "(t=2i*2^-m), P2, P3, E1, E2 (18+24+35+54+85=216), E3 (0.233179 and 0.832555, numbers_r9.out), R1-R3. L03: M1 (E=1, "
        "Var=1), M2 (48, 32), M3 (1/N), P1-P3, E1 (only 2.39 exceeds 2), E2 (2.65625), E3 (0.0125), R1 (2t^2/N), R2 (c=2), "
        "R3 (Var=2t^2; the 'one hypothesis fails' sentence names (H1) and says (H2) does not apply, consistent with the page).",
    },
    "SC1a-attrib-L01-A1-parts": {
        "check": "2.4-assumptions",
        "location": "course/modules/SC/SC1/L01.html:37, :72-80",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52, re-read of :72-80 (the changed :80 included): parts (a) product rule for independent "
        "integrable variables, (b) finite linear combinations of independent normals are normal, (c) uncorrelated jointly "
        "normal coordinates are independent, (d) a limit on a measurable event is a random variable, (e) grouping of "
        "independent families. Each is stated as an assumption and attributed to no source. :80 names independence and "
        f"multivariate normal as the M4 concepts (owners M4, {SCRIPTS}concept_owner_r9.out).",
    },
    "SC1a-prose-L01-three-conditions": {
        "check": "2.9-prose",
        "location": "course/modules/SC/SC1/index.html:49; L01.html:51",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: index.html:49 ('define standard Brownian motion by three conditions ... derive its "
        "covariance') and L01.html:51 (three conditions: starts at zero, normal increments with variance equal to the length, "
        "independent increments over disjoint intervals) agree with Definition 1.1 at L01.html:57-65.",
    },
    "SC1a-notation-H-horizon": {
        "check": "2.4-notation",
        "location": "course/modules/SC/SC1/L03.html:120, :122, :128, :133; tests/labs/SC1/lab-SC1-L03-1.py",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: H is the horizon in Proposition 2.4 (L03.html:118-129) and in Lab 1 (HORIZONS in the "
        "twin); T is not used as a horizon or sample size on any of the four pages (grep for T in math returns only the grade "
        "and the sentence at L03.html:120 explaining the reservation).",
    },
    "SC1a-notation-macros": {
        "check": "2.4-notation",
        "location": "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: census of every backslash command in the four pages (grep, output in the session "
        "log): \\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic are the registered macros; all others are standard KaTeX or the "
        f"local symbols. \\mathbb appears once, as \\mathbb Z at L02.html:78 (the integers; \\mathbb{{Q}} is not used). "
        f"page_smoke (see SC1a-gate-page-smoke) reports zero unrendered math on the four pages ({SCRIPTS}page_smoke.out).",
    },
    "SC1a-notation-no-registered-collision": {
        "check": "2.4-notation",
        "location": "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: notation/notation.json symbols are T, \\Phi/\\Phi^{-1}, \\gamma_3, \\gamma_4, R^\\ast, "
        "R^{e\\ast}, R_f, \\mathbb{Q}; none appears on the four pages (grep: no \\Phi, \\gamma, R_f, R^\\ast, \\mathbb{Q}).",
    },
    "SC1a-notation-T-subscript": {
        "check": "2.4-notation",
        "location": "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: grep for T as a symbol in math (T_, T^, T(, T=, \\(T) finds no horizon or sample size; the "
        "only T in the four pages are the grade letter and L03.html:120.",
    },
    "SC1a-process-words": {
        "check": "2.9-prose",
        "location": "index.html, L01.html, L02.html, L03.html; lab twins L01-L03",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: case-insensitive grep for builder, verifier, fixer, ledger, draft, agent, reviewer, "
        "REQUEST, unit report and planner on the four pages and the three twins returns no hit (the only 'round' matches are "
        "inside 'around' and 'unrounded', which are ordinary words).",
    },
    "SC1a-banned-phrases": {
        "check": "2.9-prose",
        "location": "index.html, L01.html, L02.html, L03.html; lab twins",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: tools/check_pages.py --unit SC1 PASS (its banned-string list, "
        f"{SCRIPTS}check_pages.out) and a grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an "
        "exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, "
        "clearly and a horizontal ellipsis finds no hit.",
    },
    "SC1a-structure-L01-L03": {
        "check": "2.9-structure",
        "location": "course/modules/SC/SC1/L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52, counted in the files: why-it-matters 116, 101 and 120 words (limit 120); 3 misconceptions "
        "each; 12 problems each (4 tiers of 3) with 12 details.solution; 10 quiz items each (class item); data-hours=9 on each; "
        "section order as in BUILDER_RULES 4.2; check_pages PASS.",
    },
    "SC1a-scope-words-L02-L03": {
        "check": "2.4-scope",
        "location": "course/modules/SC/SC1/L02.html:122, :139, :158, :263, :316, :385, :417; L03.html:85, :104, :133, :253, :270",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52, re-read of each cited scope word: L02 'for every n' (:122) is proved by induction in "
        "Lemma 2.3; the consequence at :139 is for each dyadic time; the union bound at :158 covers a countable family; the "
        "interpretation's 'all eight observed suprema' (:263) is the printed 8 of 8; the refinement 'each unit interval' "
        "(:316) is proved; L03 'every z should lie within +-3' (:133) is a prediction checked against the 16 printed z values; "
        "'no other |z| exceeds 1.84' (:253) and 'all 16 (H, N) pairs' (:253) are printed-output statements "
        f"({SCRIPTS}numbers_r9.out); the misconception's 'for every partition' (:270) is Theorem 2.3's bound.",
    },
    "SC1a-hub-data-status": {
        "check": "2.8-data",
        "location": "course/modules/SC/SC1/index.html:37, :174-177; L01-L03",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: index.html:176 'No real data is used in SC1' and the four pages reference no data file "
        "(grep for data-files, MANIFEST, assets/data, fetch returns nothing in index, L01, L02, L03); the labs use generated "
        "paths labelled SIMULATED (L02, L03) or exact arithmetic (L01).",
    },
    "SC1a-hub-ladder-objectives": {
        "check": "2.9-structure",
        "location": "course/modules/SC/SC1/index.html:168 (rung 2 description, inside :163-171)",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: the round-8 FAIL is fixed. index.html:168 now reads 'with the identity line and the final "
        "comparison line removed'. project.html:45 ('two lines to fill'), :199 (identity = ___) and :202 (== ___), and :275 "
        "('Two lines to fill, the identity and the comparison') agree. Rungs 1, 3 and 4 (:167, :169, :170) match "
        "project.html:44, :46, :47.",
    },
    "SC1a-r6-variance-t0-L01": {
        "check": "2.4-math",
        "location": "course/modules/SC/SC1/L01.html:67 ('Standard' paragraph)",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: the round-8 FAIL is fixed. L01.html:67 now reads '(D2) and (D3) are statements about laws. "
        "(D1) is pathwise only at time 0: it says that every path starts at 0. None of the three constrains a path between its "
        "times.' This is consistent with Definition 1.1 and with the counterexample of L01.html:215-217, which keeps (D1) and "
        "changes only the paths at one random time.",
    },
    "SC1a-r8-project-rung-hours-and-check": {
        "check": "2.9-structure",
        "location": "course/modules/SC/SC1/index.html:143, :165, :168; project.html:206, :274-275",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: project.html:206 prints 'n = 6, a = 2: walks with maximum >= a: 29'; recomputed by "
        "enumeration of the 2^6 walks: 29 (and n = 2, a = 1 gives 2, index.html:143). project.html:274-275 give rung 1 = 2 h "
        "and rung 2 = 3 h (index.html:165 'the hours of each rung are on the project page' holds). index.html:168 agrees with "
        "project.html:199, :202, :275 (see SC1a-hub-ladder-objectives).",
    },
    "SC1a-r8-links-anchors": {
        "check": "2.9-structure",
        "location": "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html (107 local links)",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: {SCRIPTS}links_r9.py -> 'links checked: 107 problems: 0' ({SCRIPTS}links_r9.out): every "
        "href and src resolves and every fragment id exists in its target (including course/concepts.html anchors).",
    },
    "SC1a-r8-A3-in-L05": {
        "check": "2.4-math",
        "location": "course/modules/SC/SC1/L05.html:271, :279, :288; index.html:33, :53, :156",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: L05.html moved (one line inserted at :69), so the round-8 line numbers are stale; the "
        "current lines are :271 (Assumption A3 'strong Markov property; not proved here'), :279 ('Assumption A3 is stated for "
        "bounded stopping times') and :288 (unbounded stopping times not covered). The hub's 'stated in Lesson 5' (index.html:33) "
        "and 'strong Markov property stated as Assumption A3' (index.html:156) hold.",
    },
    "SC1a-r8-lab-mutants": {
        "check": "2.5-labs",
        "location": "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: the four round-8 single-line mutants re-run from an empty directory (exit 0, 0 stderr "
        f"bytes) and each prints lines that differ from its page's expected block (2, 10, 10 and 16 differing lines; "
        f"{SCRIPTS}lab_mutants_r9.out). Lab mutants are not graded, so they are listed for information only.",
    },
    "SC1a-numbers-L02": {
        "check": "2.2-numbers",
        "location": "course/modules/SC/SC1/L02.html:268-277 (printed block), :278 (interpretation), :405-407 (E1), :411-414 (E2), :418-421 (E3)",
        "status": "PASS",
        "evidence": f"Round 9 at c93dd52: the locators of the round-8 row were wrong (:263 is blank, :385-399 are problem headers) and are "
        "corrected here. Re-derived from the seeded run ({SCRIPTS}numbers_r9.out): each observed sup m = 1..8 (0.116589, 0.731080, "
        "0.229982, 0.327612, 0.252987, 0.198455, 0.156208, 0.128716) and each bound lambda_m 2^(-(m+1)/2) (0.832555, 0.832555, "
        "0.721013, 0.588705, 0.465412, 0.360507, 0.275342, 0.208139) match the printed lines at :268-275; 8 of 8 within bounds; "
        "grid sup |Sigma_8 - Sigma_4| = 0.348139 and bounds 5..8 sum 1.309399 (:277) match. The 216 = 18+24+35+54+85 count "
        "(:266, :278, :411-414) is re-derived.",
    },
    "SC1a-numbers-L02-36-points": {
        "check": "2.2-numbers",
        "location": "course/modules/SC/SC1/L02.html:278 (interpretation); :411-414 (E2)",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: :278 says '36 (depth, point) pairs: 2, 3, 5, 9 and 17 points at depths 0 to 4, each compared "
        "with every level from its depth to 8'. 2+3+5+9+17 = 36 and (2^n+1)(9-n) = 18, 24, 35, 54, 85 sum to 216, the printed "
        "count (:266 and :412-414). The lab loop is range(n, LEVELS + 1) (lab-SC1-L02-1.py, the dyadic loop), so 9-n levels per point.",
    },
    "SC1a-grade-L02": {
        "check": "2.3-grades",
        "location": "course/modules/SC/SC1/L02.html:74 (Lemma 2.2), :103 (Lemma 2.1), :121 (Lemma 2.3), :145 (Proposition 2.4), "
        ":289 (Theorem 2.5), :303 (Remark 2.6), :93 (Assumption 2.1, ungraded), :458-462 (key-results)",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: the round-8 locators :110, :274 and :287 were wrong (blank, printed output, blank) and are "
        "corrected here. Each T block (Lemma 2.1, 2.2, 2.3; Proposition 2.4; Theorem 2.5; Remark 2.6) is graded T and its proof "
        "is on the page under the hypotheses it lists; Assumption 2.1 carries no grade of its own; the key-results rows at "
        ":458-462 are grade T with their sources ('Proved in section ...' or 'assuming A2') as the statements give them.",
    },
    "SC1a-attrib-L02-lemma2.1-union": {
        "check": "2.4-attribution",
        "location": "course/modules/SC/SC1/L02.html:97 (Assumption 2.1(c)), :158 (the union bound in Proposition 2.4(a))",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: the round-8 locator :263 was blank and is replaced. The union bound for countable families "
        "and continuity from below are stated as Assumption 2.1(c) at :97 and used at :158, where the union over the 2^{m-1} "
        "coefficients and the increasing sets A_{m0} are both written out. No source is cited.",
    },
    "SC1a-assump-L02-grouping": {
        "check": "2.4-assumptions",
        "location": "course/modules/SC/SC1/L02.html:106 (Lemma 2.1 H2), :116 (use of Assumption 2.1(a)), :138 (A1(e) grouping in Lemma 2.3)",
        "status": "PASS",
        "evidence": "Round 9 at c93dd52: Lemma 2.1 lists 'Assuming Assumption 2.1(a)' at :106 and uses it at :116 (the monotone "
        "integral step); Lemma 2.3's grouping uses of A1(e) are at :138 and each names the blocks it groups. The round-8 locators "
        ":113 and :127-128 (the start of the proof and a closing div) are replaced.",
    },
    "SC1a-hub-concept-list": {
        "check": "2.9-structure",
        "location": "course/modules/SC/SC1/index.html:61-67, :66 (From M6 list)",
        "status": "FAIL",
        "evidence": f"Round 9 at c93dd52: each linked concept's owner matches its 'From M*' label ({SCRIPTS}concept_owner_r9.out) "
        "and every owner is in the closure. But index.html:66 lists the optional stopping theorem among the concepts 'this "
        "module uses' (index.html:35 and :60 say so). No page of SC1 uses it: the only mentions are index.html:66 and :155, and "
        "L04.html:232 reads 'Optional stopping is not used ... the optional-stopping theorem is not restated here.' "
        "The dominated convergence theorem is used (L05.html:281), so only the optional stopping item is wrong.",
        "fix": "In index.html:66, remove the optional stopping theorem item and its joining 'and', so the M6 list ends "
        "'... stopping time and dominated convergence theorem.' (restore it only if an SC1 lesson uses it).",
    },
    "SC1a-r9-hub-ost-card-L04": {
        "check": "2.9-structure",
        "location": "course/modules/SC/SC1/index.html:155 (L04 card body)",
        "status": "FAIL",
        "evidence": "Round 9 at c93dd52: the L04 card says the lesson covers 'the optional stopping theorem for a bounded stopping "
        "time'. L04.html:232 says 'Optional stopping is not used', that the optional-stopping theorem 'is not restated here', "
        "and that the lesson 'makes no claim about E[B_tau] ... for a random time tau'. The card describes content the lesson "
        "disclaims.",
        "fix": "In index.html:155, delete ', and the optional stopping theorem for a bounded stopping time' so that the card "
        "body ends 'the exponential martingale.'",
    },
    "SC1a-r9-hub-reflection-assumptions": {
        "check": "2.9-structure",
        "location": "course/modules/SC/SC1/index.html:33 (lede), :157 (L06 card); course/modules/SC/SC1/L06.html:52, :119, :149, :157",
        "status": "FAIL",
        "evidence": "Round 9 at c93dd52: the lede (index.html:33) says the reflection principle gives the distribution of the "
        "running maximum and of the first-passage time 'in closed form under Assumption A3'. The L06 card (index.html:157) says "
        "'Reflection at the first passage time under Assumption A3'. But L06.html:119: 'Assumption A3 of Lesson 5 covers only "
        "bounded stopping times, and this page does not show that tau_a is bounded, so the statement is not asserted from A3. "
        "On this page the path-level statement is not proved.' L06.html:149 says the path-level statement 'is not used below, "
        "and this page does not claim it'. The tail identity (L06.html:153, Theorem 2.5) is under Assumption A3 and "
        "Assumption A4 (L06.html:157; the why-it-matters at :52 says 'under Assumptions A3 and A4'). A4 is absent from the hub.",
        "fix": "index.html:33: replace 'under Assumption A3 (stated in Lesson 5)' by 'under Assumptions A3 and A4 (stated in "
        "Lesson 5), in its fixed-time form; the path-level reflection at the first passage time is not proved'. index.html:157: "
        "replace 'Reflection at the first passage time under Assumption A3' by 'The fixed-time reflection identity for the "
        "running maximum under Assumptions A3 and A4'.",
    },
    "SC1a-r9-hub-objective-reflection-proof": {
        "check": "2.9-structure",
        "location": "course/modules/SC/SC1/index.html:54 (objective 6)",
        "status": "FAIL",
        "evidence": "Round 9 at c93dd52: objective 6 says the student will 'Prove the reflection principle'. L06.html:119 and :149 "
        "say the path-level reflection principle (Definition 2.2) is not proved on the page and is not claimed; only the "
        "fixed-time form (Proposition 2.3, Theorem 2.5) is proved. The objective overstates what Lessons 6 to 8 deliver.",
        "fix": "index.html:54: replace 'Prove the reflection principle' by 'Prove the fixed-time reflection identity for "
        "Brownian motion (Lesson 6, Theorem 2.5), under Assumptions A3 and A4'; keep 'derive the tail of the running maximum "
        "and the first-passage identity, and name every assumption each one uses (Lessons 6 to 8)'.",
    },
    "SC1a-r9-quiz-L02-q3-explanation": {
        "check": "2.4-math",
        "location": "course/modules/SC/SC1/L02.html:489 (quiz item 3 explanation); L02.html:161 (Step 2)",
        "status": "FAIL",
        "evidence": "Round 9 at c93dd52: the explanation says 'Step 2 of Proposition 2.4 bounds the terms by m r^m with "
        "r = 2^(-1/2)'. Step 2 (L02.html:161) proves M_m <= sqrt(2 log 2) * m * r^m, with the constant sqrt(2 log 2) ~ 1.18, "
        "where M_m is the level bound. The option marked correct (the term sqrt(m) 2^(-m/2) is at most m r^m) is true with "
        "constant 1 for that term, but the explanation misstates what Step 2 proves.",
        "fix": "Replace the explanation at L02.html:489 by: 'Step 2 of Proposition 2.4 bounds the level bound M_m by "
        "sqrt(2 log 2) m r^m with r = 2^(-1/2), and sqrt(m) 2^(-m/2) <= m r^m, which is the correct option.'",
    },
}

rows = []
fresh_ids = set(FRESH)
for r in prev["rows"]:
    rid = r["id"]
    if rid in fresh_ids:
        f = FRESH[rid]
        row = {"id": rid, "check": f["check"], "location": f["location"], "status": f["status"], "evidence": f["evidence"]}
        if f["status"] != "PASS":
            row["fix"] = f["fix"]
        rows.append(row)
        continue
    rows.append({
        "id": rid,
        "check": r["check"],
        "location": r["location"],
        "status": "PASS" if r["status"] == "PASS" else "FAIL",
        "evidence": CARRY + stripped(r["evidence"]),
        **({} if r["status"] == "PASS" else {"fix": "Re-verify in round 9"}),
    })

# rows that round 9 adds (ids new to this round)
for rid in ["SC1a-r9-hub-ost-card-L04", "SC1a-r9-hub-reflection-assumptions", "SC1a-r9-hub-objective-reflection-proof",
            "SC1a-r9-quiz-L02-q3-explanation"]:
    f = FRESH[rid]
    row = {"id": rid, "check": f["check"], "location": f["location"], "status": f["status"], "evidence": f["evidence"],
           "fix": f["fix"]}
    rows.append(row)

out = {
    "unit": "SC1",
    "slice": "a",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier SC1-a round 9 (did not build SC1; full re-read of index.html (190 lines), "
    "L01 (446), L02 (560), L03 (504) and the three lab twins at c93dd52; delta from 0dee921a read hunk by hunk)",
    "pin": PIN,
    "base": BASE,
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-SC1-a",
    "scratch": SCRIPTS,
    "verified_at": "2026-11-05T05:30:00Z",
    "verdict": None,
    "rows": rows,
    "mutants": [
        {"id": "SC1a-r9-lab-mut1-L01-max-not-min",
         "description": "lab-SC1-L01-1: covariance sums max(i, j) increments instead of min(i, j); the covariance line and the 81 of 81 count change.",
         "killed_by": "run of the mutated twin differs from the L01.html expected block (" + SCRIPTS + "lab_mutants_r9.out)"},
        {"id": "SC1a-r9-lab-mut2-L02-scale-half-m",
         "description": "lab-SC1-L02-1: level_term_sup uses 2**(-m/2) instead of 2**(-(m+1)/2); the grid-supremum line prints False.",
         "killed_by": "run of the mutated twin differs from the L02.html expected block (" + SCRIPTS + "lab_mutants_r9.out)"},
        {"id": "SC1a-r9-lab-mut3-L03-divisor-n",
         "description": "lab-SC1-L03-1: standard error divides by n instead of n - 1; z values change (2.40 at H=1, N=2).",
         "killed_by": "run of the mutated twin differs from the L03.html expected block (" + SCRIPTS + "lab_mutants_r9.out)"},
        {"id": "SC1a-r9-lab-mut4-L03-closed-form-plus",
         "description": "lab-SC1-L03-1: closed form uses 4N^2 + 1 instead of 4N^2 - 1; closed form matches prints False.",
         "killed_by": "run of the mutated twin differs from the L03.html expected block (" + SCRIPTS + "lab_mutants_r9.out)"},
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Round 9 at c93dd52 (base 0dee921a, the round-8 pin). Delta for the slice read hunk by hunk: index.html:168; L01.html:51, :67, :80; "
    "L03.html:133, :253, :354-355, :357 (mechanical_carry_check.out). The twins are byte-identical to the previous pin. L05, L06 and "
    "project.html moved in the delta and were read for the hub's cross-references (L05 A3 lines moved by one; L04.html:232 and "
    "L06.html:52, :119, :149, :153, :157 read at their current lines). Round-8 rows carried only where the cited lines are "
    "unchanged (mechanical_carry_check.py); rows citing changed lines or whole pages were re-verified (FRESH).",
    "summary": "",
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
out["verdict"] = "PASS" if counts["PASS"] == len(rows) else "FAIL"
out["summary"] = (
    f"SC1-a round 9 at c93dd52: verdict {out['verdict']}. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
    f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Round-8 FAIL rows SC1a-hub-ladder-objectives and SC1a-r6-variance-t0-L01 are fixed and "
    "re-verified PASS. New FAIL rows: SC1a-hub-concept-list (OST), SC1a-r9-hub-ost-card-L04, SC1a-r9-hub-reflection-assumptions, "
    "SC1a-r9-hub-objective-reflection-proof, SC1a-r9-quiz-L02-q3-explanation. Lab mutants: 4 of 4 killed (not graded)."
)
Path(ROOT, "ledgers/SC1/SC1-a.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, out["verdict"])
