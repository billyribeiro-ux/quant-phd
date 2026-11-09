"""Write the round-2 verifier fragment for M7 slice a to ledgers/M7/M7-a.json and validate it with tools/ledger.py.

Run from the checkout root: python -I -W error ledgers/M7/scripts/M7-a-r2/write_fragment.py
Every row cites a command or a script under ledgers/M7/scripts/M7-a-r2/ (see gate_commands.sh) or a file:line.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import ledger  # noqa: E402

ROOT = Path.cwd()
OUT = ROOT / "ledgers/M7/M7-a.json"
S = "ledgers/M7/scripts/M7-a-r2"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, evidence: str) -> None:
    rows.append({"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence})


row(
    "M7a-cmd-check_pages",
    "2.9 structure: tools/check_pages.py --unit M7 and --page L01/L02/L03",
    "course/modules/M/M7/index.html, L01.html, L02.html, L03.html",
    "Observed: `check_pages.py --unit M7` exit 0 'check_pages M7: PASS' (unit run includes the hub, index.html line 414 of the tool); "
    "`--page L01`, `--page L02`, `--page L03` each exit 0 PASS. `--page index` is not a supported mode (the tool only takes "
    "lesson pages; exit 1 with 'missing section why-it-matters'), so the hub is checked by the unit run only. "
    f"Command record: {S}/gate_commands.sh.",
)
row(
    "M7a-cmd-check_dag",
    "2.9 DAG: tools/check_dag.py --unit M7",
    "L01-L03 links and dfn; hub concept links",
    "Observed: exit 0 'check_dag M7: PASS'. Concept links in the slice (grep of concepts.html#): gradient, hessian, "
    "positive-semidefinite-matrix, eigendecomposition, spectral-theorem, implicit-function-theorem, envelope-theorem (M2/M3 closure); "
    "convex-function (L01 to L03), lagrange-multiplier (L02 to L03). Each dfn is defined once (convex-set and convex-function in L01 "
    "lines 57 and 82; lagrange-multiplier in L02 line 63; kkt-conditions in L03 line 62).",
)
row(
    "M7a-cmd-check_projects",
    "2.6 project-level gate: tools/check_projects.py --unit M7 (not in slice; unit-level run only)",
    "course/modules/M/M7/project.html (not in slice)",
    "Observed: exit 0 'check_projects M7: PASS'. Reported only because the hub links project.html and rung titles are checked here.",
)
row(
    "M7a-cmd-run_labs",
    "2.5 labs: tools/run_labs.py --unit M7 --page L01|L02|L03",
    "L01.html#lab-M7-L01-1, L02.html#lab-M7-L02-1, L03.html#lab-M7-L03-1",
    "Observed: each page exit 0, 'run_labs M7: PASS (1/1)'.",
)
row(
    "M7a-lab-twin-direct",
    "2.5 labs: each twin run alone under python -I -W error; expected block equals output",
    "tests/labs/M7/lab-M7-L01-1.py, lab-M7-L02-1.py, lab-M7-L03-1.py",
    f"Observed: `python -I -W error` on each twin exit 0, empty stderr. {S}/lab_check.py prints, for L01, L02, L03: "
    "expected_equals_output=True with 14, 13 and 22 lines (outputs in twin_L01.out, twin_L02.out, twin_L03.out).",
)
row(
    "M7a-lab-code-equals-twin",
    "2.5 labs: page code equals twin",
    "L01.html, L02.html, L03.html <code data-run>",
    f"{S}/lab_check.py: page_code_equals_twin=True for L01, L02, L03 (HTML-unescaped <code data-run> text versus the twin file).",
)
row(
    "M7a-lab-runtime-seed",
    "2.5 labs: seeded, no network, under 10 s",
    "tests/labs/M7/lab-M7-L0[123]-1.py",
    "L02 uses a fixed LCG (SEED=1); L01 and L03 use no randomness; all imports are stdlib (fractions, itertools, math). "
    "page_smoke timing: lab-M7-L01-1 0.6 s, lab-M7-L02-1 0.0 s, lab-M7-L03-1 0.0 s (page_smoke_index_L01_L03.out).",
)
row(
    "M7a-cmd-page_smoke",
    "2.9 browser smoke: tools/page_smoke.py --unit M7 --pages index L01 L02 L03",
    "index.html, L01.html, L02.html, L03.html",
    "Observed: exit 0, 'page_smoke M7: PASS' (page_smoke_index_L01_L03.out): zero console errors, zero external requests, "
    "no 360 px overflow, labs run in Pyodide.",
)
row(
    "M7a-cmd-ruff-mypy",
    "2.5 code quality: ruff check, ruff format --check, mypy --no-incremental --strict on the three twins; repo-wide gates",
    "tests/labs/M7/lab-M7-L01-1.py, L02, L03; whole repository",
    "Observed: ruff check (twins) 'All checks passed!'; ruff format --check (twins) '3 files already formatted'; "
    "mypy --no-incremental --strict (twins) 'Success: no issues found in 3 source files'; repo-wide `ruff check .` exit 0, "
    "`ruff format --check .` exit 0 (553 files), `mypy --no-incremental` exit 0 (385 files). Outputs in ruff_*.out, mypy_*.out.",
)
row(
    "M7a-cmd-pytest-labs",
    "2.5 labs: pytest tests/test_labs.py -k M7",
    "tests/test_labs.py",
    "Observed: `pytest tests/test_labs.py -k M7 -q` exit 0, 11 passed (pytest_labs_M7.out). The -k M7 selection also covers the L04-L08 and project twins.",
)
row(
    "M7a-cmd-verify_refs",
    "2.1 citations: tools/verify_refs.py --unit M7 (live) and --offline (registry)",
    "index.html reading list; L01-L03 reference sections; references/references.json",
    "Observed: live `verify_refs.py --unit M7` exit 0 'live re-verification of M7: 2 of 560 entries, 0 problems'; "
    "`verify_refs.py --offline` exit 0 'offline integrity: 560 entries, 0 problems' (verify_refs_*.out). "
    "The M7 keys are boyd2004convex and stokey1989recursive (references.json entries; M7 is the only used_by).",
)
row(
    "M7a-hub-hours",
    "2.9 hours: hub split sums to curriculum; lessons sum to the rest; project 10-40 %",
    "index.html line 29 (data-hours-lessons=77, data-hours-project=33), lines 42, 141, 143-150; L01-L03 data-hours",
    "110 = 77 + 33 (curriculum hours 110, course/curriculum 01-foundations.yaml:301). 33/110 = 30 %. Lesson data-hours: "
    "L01 9 (L01.html line 2), L02 9, L03 10; L04 10, L05 10, L06 10, L07 9, L08 10 (grep). Sum 9+9+10+10+10+10+9+10 = 77. "
    "Hub text 'Lessons 1, 2, 7 declare 9 hours and the others 10 hours' (line 141) and card kickers (lines 143-150) agree.",
)
row(
    "M7a-hub-placement",
    "2.9 placement diagnostic: count, bar, skill items, arithmetic",
    "index.html lines 71-137",
    "Nine items (lines 75, 80, 85, 94, 99, 108, 117, 126, 131). Seven prerequisite items (M2 lines 75, 80; M3 lines 85, 94, 108; "
    "M1 logic line 99; M2 derivative line 131) and two skill checks (data-skill lines 117, 126). Answers recomputed: "
    "d/dx1 (x1^2+3x1x2) at (1,0) = 2; mixed partial = 3; PSD identity; smaller eigenvalue of [[2,1],[1,2]] = 1; Sigma-stationarity "
    "with budget: Sigma w* = lambda 1; diag(1,2) multiplier 2/3 = 0.6667 (u=(1,1/2), s=3/2); derivative of x^2 at 3 = 6. "
    "Bar 80 % of 9 = 7.2, so 8 correct needed; 7/9 = 77.8 %, 8/9 = 88.9 % (line 73) recomputed.",
)
row(
    "M7a-hub-objectives-ladder",
    "2.9 hub: 4-8 measurable objectives, prerequisites, lesson map, four-rung ladder in order",
    "index.html lines 45-69, 139-163",
    "Eight objectives (lines 49-56) with measurable verbs. Prerequisite links to M2 and M3 with concept links (lines 64-65). "
    "Lesson map L01-L08 with data-progress-key (lines 143-150). Ladder: four span.rung-title in order 'Worked example', "
    "'Completion', 'Independent', 'Stretch' (lines 158-161); check_projects PASS confirms the four titles.",
)
row(
    "M7a-hub-prose-crossrefs",
    "2.2/2.9 hub cross-references: other pages and registry",
    "index.html lines 49-176",
    "Targets exist: M2/index.html, M3/index.html, M1 Lesson 1 Theorem 3.1 'negating one quantifier' (course/modules/M/M1/L01.html "
    "block-title), project.html 'Lab 2' (project.html line 171), L02 Problem R3 (L02.html line 421), L02 Prop 3.2(c). "
    "Concept links resolve in check_dag.",
)
row(
    "M7a-hub-naming",
    "2.9 hub prose: module names",
    "index.html lines 35, 64-65",
    "Curriculum titles: M2 'Single & Multivariable Calculus' (curriculum/01-foundations.yaml:123), M3 'Linear Algebra' (:158). "
    "The hub uses 'M2 Calculus' as a short label, which is a shorthand of the full title, not a different module name. Non-blocking; noted.",
)
row(
    "M7a-hub-covariance-B1",
    "B1 architect decision: covariance appears only in a no-link disclaimer",
    "index.html line 167; L01-L03 (none)",
    "grep 'covariance' over index.html, L01.html, L02.html, L03.html: one hit, index.html line 167 'estimating a covariance matrix is "
    "outside M7', plain text with no concept link and no href. Zero hits in L01-L03.",
)
row(
    "M7a-hub-data-status",
    "2.8 data: no data-files; SIMULATED or hand-chosen labels where inputs are used",
    "index.html section#data (line 167); L01-L03 labs; L03 line 140",
    "grep: no data-files attribute and no <svg> in index.html, L01-L03. SIMULATED appears in the L01 lab docstring (line 165), "
    "L02 lab docstring (line 157), L03 lab docstring and line 140 (hand-chosen, SIMULATED, not market data).",
)
row(
    "M7a-L01-structure",
    "2.9 lesson structure (BUILDER 4.2 order), minimums, data-hours 9",
    "L01.html",
    "Order: why-it-matters (line 51), core sections 1-3 (lines 53-104), Lab 1 inline (lines 157-310), canon-breaks (line 312), "
    "misconceptions (line 323, 3 entries), problem set (line 341, 12 problems, 3 per tier, each with a solution of at least 33 words), "
    "key-results (line 446), quiz (line 462, 11 items), references. data-hours=9 (line 2). why-it-matters 116 words (<=120).",
)
row(
    "M7a-L01-math",
    "2.4 mathematics: Definitions 1.1, 2.1; Example 1.2; Propositions 1.3, 2.3, 3.2; Lemma 3.1; Examples 2, 3.2a, 3.3",
    "L01.html lines 55-148",
    f"Read in full. Recomputed (recompute_L01_L03.py, all OK): Lemma 3.1 identity on all 3125 cases of Q1 and Q2; Example 1.2 "
    "midpoint (1/2,1/2) has squared norm 1/2; Example 3.3 eigenvalues 3,1 (Q1) and 3,-1 (Q2); Hessians 2Q (6,2) and (6,-2); "
    "Proposition 3.2 proof steps (i)=>(ii) with y=0, lambda=1/2 gives gap = q(x)/4; (ii)=>(iii) with x=V e_i; R3 2x2 eigen condition "
    "checked on a grid in [-3,3]^3. Proposition 1.3 and 2.3 proofs are complete; Assumption 1 is stated as an assumption.",
)
row(
    "M7a-L01-problems",
    "2.4/2.9 problem set: worked solutions (M1-M3, P1-P3, E1-E3, R1-R3)",
    "L01.html lines 341-444",
    "All 12 solutions read. Recomputed: M2 (2 - (-2) chord 1, difference 1, Lemma 3.1 = 1); M3 (q(1,1)=6, gap 6 = 1/4 * 24); "
    "P3 (q(v)=mu|v|^2 < 0 gives gap q(v)/4 < 0); E1 (3 x 184 = 552 = 3125 - 2573); E3 (eigenvalues 3,1 from 6,2); "
    "R1 (x'Qx = x1^2+x2^2); R3 (Q1 conditions 4 >= 0 and 3 >= 0).",
)
row(
    "M7a-L01-lab-prose",
    "2.2 lab statements vs printed output (hypothesis, interpretation, canon-breaks, misconceptions)",
    "L01.html lines 159, 302-336 and expected block 295-308",
    "Hypothesis (line 159) predicts 3125 of 3125 for both identity lines, Q1 chord 3125, Q2 failures = 3 x 184; printed "
    "lines 297-302 agree. Interpretation (line 309): 552 = 3125 - 2573 (checked), 3/2 vs 1, -1/2 = (1/4)(-2) (checked). "
    "Misconception 2 'eigenvalue -2 of the Hessian 2Q2' is printed on line 306 (checked).",
)
row(
    "M7a-L01-grades",
    "2.3 grades: each claim span re-graded against BLUEPRINT section 3; key-results table",
    "L01.html block titles (lines 67, 93, 109, 134), key-results lines 452-456",
    "The four block-title claim spans (lines 67, 93, 109, 134: Propositions 1.3, 2.3, 3.2 and Lemma 3.1) and the five key-results rows (lines 452-456) are T; their proofs are complete on the page, with "
    "Assumption 1 stated where used (Prop 3.2 (iii) conditional on it, and the table says so, line 456). Lab results are not claim "
    "spans; they are read as printed output and graded C on the cards (c012, c178, c189). No over-grading found.",
)
row(
    "M7a-L01-quiz",
    "2.9 retrieval quiz: 11 items, answers and explanations",
    "L01.html section#quiz lines 462-546",
    "11 items (lines 467, 476, 481, 486, 495, 500, 505, 514, 523, 531, 537), each with a data-correct answer and an explanation. "
    "Numeric keys recomputed: 4 (Hessian (1,1) entry 2*2), 1, -0.5 (gap for Q2 at x=(1,0),y=(0,1)), 3125, -2 (x'Q2x at (1,-1)).",
)
row(
    "M7a-L02-structure",
    "2.9 lesson structure, minimums, data-hours 9",
    "L02.html",
    "Order: why-it-matters (line 51), core sections 1-3 (lines 53-143), Lab 1 (lines 148-293), canon-breaks (line 295), misconceptions "
    "(line 306, 3 entries), problem set (line 324, 12 problems, 3 per tier, solutions at least 21 words), key-results (line 429), quiz "
    "(line 445, 11 items). data-hours=9 (line 2). why-it-matters 115 words.",
)
row(
    "M7a-L02-math",
    "2.4 mathematics: Definition 2.1, Assumption 1, Theorem 2.2, Examples 2.5-2.6, Proposition 2.4, Propositions 3.2, 3.3",
    "L02.html lines 55-146",
    "Read in full. Theorem 2.2 proof re-derived: p.d = -|r|^2 < 0; gamma'(0)=d using g.d = 0; f(gamma(t)) = f + t p.d + o(t). "
    "Example 2.5 (h = y^2 - x^3, grad h = 0 at origin), Example 2.6 (f = y^3, h = x, witness (0,-y)) checked. Proposition 3.2 (a)-(d) "
    "re-derived; (d) identity f(w)-f(w*) = (1/2)d'Sigma d checked on exact fractions. Proposition 3.3 identity checked. "
    "Assumption 1 is an assumption, not proved on the page (line 69).",
)
row(
    "M7a-L02-attribution-M2-L21",
    "2.1 attribution: 'M2 Lesson 21 (Theorem 1.3) states and proves the one-dependent-variable form'",
    "L02.html line 69 and references line 533; course/modules/M/M2/L21.html",
    "Read: M2 L21 block-title 'Theorem 1.3 (the implicit-function theorem, one dependent variable)' at L21.html line 68, followed by a "
    "Proof block at line 73; the page title is 'L21 · The implicit-function theorem'. Attribution matches.",
)
row(
    "M7a-L02-problems",
    "2.4/2.9 problem set: worked solutions (M1-M3, P1-P3, E1-E3, R1-R3)",
    "L02.html lines 324-427",
    "All 12 solutions read. Recomputed: M1 (x=y=1/2, lambda=1); M2 diag(1,2) (u=(1,1/2), lambda=2/3, w*=(2/3,1/3), f=1/3); M3 "
    "(f(w*+d)=11/6, increase 3/2 = (1/2)(1+2)); E1 (4*47+2*17-5*9 = 177 over 55); E3 (lambda/2 = 177/110); R3 (c^2/(2s), derivative c/s). "
    "P2 (Sigma=0) checked.",
)
row(
    "M7a-L02-lab-prose",
    "2.2 lab statements vs printed output (hypothesis, interpretation, canon-breaks, misconception 1)",
    "L02.html lines 150, 279-292, 311",
    "Hypothesis (line 150) predicts budget = 1, residual zero, 36 of 36 twice; printed lines 287-291 agree. Interpretation (line 292) "
    "values: Sigma rows, lambda = 177/55, w = (47/55, 17/55, -9/55), f = 177/110 all printed and recomputed (recompute_L01_L03.out). "
    "Misconception 1 residual line (line 311) matches printed line 288.",
)
row(
    "M7a-L02-grades",
    "2.3 grades: claim spans and key-results",
    "L02.html key-results lines 435-439; block titles lines 73, 103, 121, 139",
    "Theorem 2.2 (T, under Assumption 1, line 435), Prop 2.4 (T), Prop 3.2 (T), Prop 3.3 (T), Example 2.6 (T, computed). "
    "Lab results are not in the key-results table; they are graded C on the cards (c027-c030, c168, c169, c181). No over-grading.",
)
row(
    "M7a-L02-quiz",
    "2.9 retrieval quiz: 11 items, answers and explanations",
    "L02.html section#quiz lines 445-529",
    "11 items (lines 450, 459, 468, 473, 478, 487, 496, 501, 510, 515, 524). Numeric answers recomputed: 0.6667 (lambda), 0.3333 (w2), "
    "5 (A=2: 2*2+1), 3.2182 (177/55 = 3.218181..., four places 3.2182; tolerance 0.00005 accepts it), 0.3333 (f*=1/3). "
    "The round-1 answer 3.2181 (a truncation) is no longer the answer: the page answer is 3.2182, and 3.218181... is the expansion (line 512).",
)
row(
    "M7a-L03-structure",
    "2.9 lesson structure, minimums, data-hours 10",
    "L03.html",
    "Order: why-it-matters (line 51), core sections 1-4 with Lab 1 inline (lines 53-302), canon-breaks (line 310), misconceptions "
    "(line 321, 3 entries), problem set (line 339, 12 problems, 3 per tier, solutions at least 26 words), key-results (line 444), quiz "
    "(line 462, 9 items), references (line 538). data-hours=10 (line 2). why-it-matters 95 words. No debate field in the curriculum entry "
    "(01-foundations.yaml 298-327), so no debate brief is required.",
)
row(
    "M7a-L03-math",
    "2.4 mathematics: Definitions 1.1-1.2; Remark 1.3; Lemmas 1.4, 1.5; Theorem 2.1; Examples 2.3, 3.1, 4.1, 4.2; Remark 4.3",
    "L03.html lines 55-307",
    "Read in full. Lemma 1.5 identity checked symbolically (theta(1-theta)/2 coefficients, cross term); Theorem 2.1 proof chain "
    "f(x) >= phi(x) >= phi(x*) = f(x*) checked; Example 2.3 (f(-1)=-1, midpoint -1/8 > average -1/2) checked; Example 3.1 (gradient of "
    "x^2 at 0 is 0) checked; Example 4.1 (grad f = (1/2,4/5), lambda2 = 3/10, nu = -1/2, p* = -1/2) and Example 4.2 (grad f = (1/2,1/2), "
    "nu = -1/2, f = -1/4) checked; Remark 4.3 Sigma^{-1} mu = (14/15, -11/30), weights sum 17/30 checked. "
    "P3 expansion (f(w) = -1/2 + (3/10) w2 + (1/2) d'Sigma d for w = (1-w2, w2)) checked at four points.",
)
row(
    "M7a-L03-problems",
    "2.4/2.9 problem set: worked solutions (M1-M3, P1-P3, E1-E3, R1-R3)",
    "L03.html lines 339-442",
    "All 12 solutions read. Recomputed: M1 (x=y=1/2, lambda=1, p*=1/2); M2 f(3/5,2/5) = -6/25 = -0.24 > -0.25; M3 grad (0,13/10), "
    "nu=0 forced, f(1/2,1/2) = -1/10 > -1/2; P1 counterexample -x^2 at x=1,y=-1 (0 > -1); P2 Lemma 1.4 identity (x-y)^2; "
    "E1 norm sqrt(1/2) = 0.7071; E3 -1/4; R1 f=-x^2 maximum at 0; R2 Slater strict part fails; R3 (K1) false for every multiplier.",
)
row(
    "M7a-L03-lab-prose",
    "2.2 lab statements vs printed output (hypothesis, interpretation, expected block, misconceptions)",
    "L03.html lines 154, 280-301, 302",
    "Hypothesis (line 154): residuals zero at both candidates; grid minima -1/2 at w1=1 and -1/4 at w1=1/2; off-solution residual (-1/2, 1/2); "
    "dual residual 3/10. All printed on lines 282-301 and recomputed (recompute_L01_L03.out, 'L03 active grid minimum value and k', "
    "'L03 inactive grid minimum value and k', 'L03 Ex4.1 dual residual flip'). Interpretation: the lab does not show multiplier uniqueness; "
    "the page does not claim it.",
)
row(
    "M7a-L03-grades",
    "2.3 grades: claim spans, key-results and lab rows",
    "L03.html key-results lines 450-456; block-title claim spans lines 78, 90, 104",
    "Lemma 1.4 (line 78), Lemma 1.5 (line 90), Theorem 2.1 (line 104) are T with proofs on the page; Examples 4.1-4.2 and 3.1 are derivations on the page. "
    "The Lab 1 row (line 456) is C, naming Lab 1 and noting the grid is not a proof (matches the lab docstring, twin lines 163-165). "
    "No over-grading found.",
)
row(
    "M7a-L03-quiz",
    "2.9 retrieval quiz: 9 items, answers and explanations",
    "L03.html section#quiz lines 462-536",
    "9 items (lines 467, 476, 484, 489, 495, 504, 513, 521, 527). Numeric answers recomputed: 0.3 (lambda2), -0.5 (nu), -0.25 (inactive value). "
    "Explanations match the lesson text.",
)
row(
    "M7a-L03-misconceptions",
    "2.9 misconceptions: three entries with wrong belief, reason and evidence",
    "L03.html section#misconceptions lines 321-337",
    "Three entries: KKT point is optimum (x^3 / (x^2-1)^2 examples: f=(x^2-1)^2 KKT points x=+-1 are global minima with value 0, x=0 a "
    "local maximum, checked); complementary slackness (Example 4.1 slack constraint, positive multiplier 3/10); stationarity alone "
    "(Remark 4.3). Each has a wrong belief, why it is wrong and evidence.",
)
row(
    "M7a-notation-x-ast",
    "2.4 notation: x^\\ast (registered as the AP1 SDF payoff inside R^\\ast) must not be reused for the minimizer",
    "L02.html, L03.html, index.html (starred superscripts)",
    f"Round 1 FAIL is fixed. Python count over the four pages: x^\\ast = 0 occurrences; w^* = 6 (index) and 45 (L02); w^\\ast = 27 and "
    "p^\\ast = 5 (L03). The registry binds R^\\ast (notation/notation.json, 'R^\\ast ... where it is written x^\\ast') and no other "
    "starred symbol. w and p are not registered symbols, so the reuse is gone.",
)
row(
    "M7a-notation-ones-glyph",
    "2.4 notation: the bold-one glyph \\mathbf{1} (ones vector) against registered macro \\indic (tex \\mathbf{1}, indicator)",
    "index.html (5 uses), L01 (7), L02 (42), L03 (4); notation/notation.json macros '\\indic'",
    "M7 uses \\mathbf{1} for the vector of ones (for example L02 line 116, 1^T w = 1). The registry's \\indic has tex \\mathbf{1} and "
    "meaning 'indicator function'. M7 never writes \\indic, so no registered macro is applied with another meaning. The same glyph is "
    "the ones vector in other modules (grep: 17 files under course/modules use \\mathbf{1}, e.g. AC2/L06, AP1/L01, S7/L04). This is a "
    "program-wide registry question, not a slice defect; recorded in registry_flags for the architect. PASS for this slice.",
)
row(
    "M7a-notation-diag-local",
    "2.4 notation: registered macros used as registered",
    "index.html, L01.html, L02.html (\\operatorname{diag})",
    "Registry macro \\diag has tex \\operatorname{diag}. The pages write \\operatorname{diag} directly. The rendered output is identical, and "
    "\\operatorname is a LaTeX primitive, not a custom macro. Non-blocking; the builder may write \\diag.",
)
row(
    "M7a-notation-local-letters",
    "2.4 notation: locally defined letters (lambda, mu, nu, N, S, F, c, d, s, u, p*, gamma, Sigma, L_c, Lambda, V, phi, theta)",
    "L01-L03",
    "Each local letter is defined where first used: F (L03 line 57), p^* (L03 line 57), gamma(t) curve (L02 line 83), Sigma (L02 line 114; "
    "L03 line 140), mu (L03 line 140), L_c (L01 line 94), Lambda and V (L01 Assumption 1 line 130). Registered symbols T, Phi, gamma_3, gamma_4, "
    "R_f, R^{e*}, \\mathbb{Q} do not occur on the slice pages (grep). \\R is used with its registered meaning.",
)
row(
    "M7a-dag-closure",
    "2.9/DAG: no concept used outside the prerequisite closure by name or link; no forward link",
    "index.html, L01-L03",
    "Links only to M2/M3 closure concepts and to the unit's own earlier definitions. Out-of-closure words appear only as plain prose "
    "(build plan 8.2 item 5): 'variance' (index 9 hits, L01 2, L02 8), 'Bellman', 'efficient frontier' and 'dynamic programming' "
    "(index, prose only, no href), and 'covariance' only in the B1 disclaimer (index line 167). Forward mention 'Lesson 3 uses ... Theorem 2.1' "
    "(L01 line 102) and 'Lesson 2' (L01 line 106) are prose cross-references, not concept links.",
)
row(
    "M7a-dfn-ownership",
    "2.9 concept definitions: each slice concept defined once in its assigned lesson",
    "L01 (convex-set, convex-function), L02 (lagrange-multiplier), L03 (kkt-conditions)",
    "Each dfn id appears once: def-convex-set (L01 line 57), def-convex-function (L01 line 82), def-lagrange-multiplier (L02 line 63), "
    "def-kkt-conditions (L03 line 62). L01 line 38 links its own two definitions; L03 line 37 links to L01 and L02.",
)
row(
    "M7a-banned-phrases",
    "2.9 banned phrases (BUILDER 1.3-1.4) and filler",
    "index.html, L01-L03 visible prose and twin docstrings",
    "Scanned for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, "
    "studies show, experts agree, it is well known, obviously, clearly, ellipsis placeholders: none. The two '...' in L01 are the "
    "'{-2, ..., 2}' grid text in the lab code (line 254) and the lab output (line 295), not placeholders. Scope words checked one by one (every, all, always, any, never, only): "
    "each is backed by a computation or a proof on the page (for example 'Q1 passes every case', 3125 of 3125).",
)
row(
    "M7a-process-words",
    "2.9 no process words in learner text",
    "index.html, L01-L03, lab twins",
    "Scanned for verifier, builder, round, draft, placeholder, pending, we checked. The one substring hit for 'round ' is 'around' (L02 line 55), an ordinary word. None found.",
)
row(
    "M7a-cards-scan",
    "2.7 cards: full scan of L01-L03 cards for duplicates and ids",
    "course/modules/M/M7/cards.json (77 cards with lesson L01-L03; 199 over the file)",
    f"{S}/cards_check.py output (cards_check.out): 77 L01-L03 cards read in full (all printed and read). No duplicate ids over the file. "
    "Near-identical fronts involving an L01-L03 card: M7-c043 vs M7-c216 (same example, different facts: KKT point yes, minimizer no) and "
    "M7-c202 vs M7-c203 (different instances). Not duplicates. Keys complete; every non-T card has a basis.",
)
row(
    "M7a-cards-L01",
    "2.7 cards L01: every card checked against the lesson text (24 cards, all read)",
    "cards.json lesson L01: M7-c001..c009, c011..c016, c165, c177, c178, c179, c184, c189, c190, c191, c201",
    "All 24 read against the current L01 text. Checked against lines: Definition 1.1 (c001), Definition 2.1 (c002), Example 1.2 and "
    "Proposition 1.3 (c003, c004), Proposition 2.3 (c005), Lemma 3.1 (c006), Example 3.2a (c007), Proposition 3.2 (c008), Example 3.3 "
    "(c009), Problem R1 (c011), lab counts 552 and 2573 (c012, c178), Problem R2 (c013), misconceptions (c014-c016, c177), Problem P3 (c165), "
    "Hessian/eigen values (c179, c201), lab numbers -1/2 (c189). No card contradicts the lesson.",
)
row(
    "M7a-cards-L02",
    "2.7 cards L02: every card checked against the lesson text (25 cards, all read)",
    "cards.json lesson L02: M7-c017..c033, c168, c169, c176, c181, c185, c192, c193, c225",
    "All 25 read. Definition 2.1 (c017), Theorem 2.2 hypotheses (c018), Example 2.5 (c019), Example 2.6 (c020), Proposition 2.4 (c021), "
    "Proposition 3.2 (c022, c023), Proposition 3.3 (c024), Problem P3 (c025), Problem M2 (c026), lab rows 4 2 5, 177/55, -9/55, 36 of 36, "
    "f=177/110, weights (c027-c030, c168, c169, c181), misconceptions (c031-c033), Remark 2.3 (c176), Section 3 (c185), Definition 2.1 "
    "stationary (c192), Section 1 local minimizer (c193), Section 1 feasible set (c225). No card contradicts the lesson.",
)
row(
    "M7a-cards-L03",
    "2.7 cards L03: every card checked against the lesson text (28 cards, all read)",
    "cards.json lesson L03: M7-c036..c053, c160, c161, c173, c187, c194, c195, c202, c203, c216, c217, c220, c221",
    "All 28 read. Round-1 FAIL on M7-c041 is fixed: the back now reads 'That condition on Sigma is sufficient for convexity; the lesson "
    "does not prove that it is necessary' (cards.json). Other cards match Definitions 1.1-1.2, Remark 1.3, Lemmas 1.4-1.5, Theorem 2.1, "
    "Examples 2.3, 3.1, 4.1, 4.2, Remark 4.3, the lab grid minima (c173, C with basis) and the three misconceptions (c051-c053). "
    "Number tokens 2/3 (c026) and -1/8 (c217) occur in the lesson as \\tfrac23 and -\\tfrac18.",
)
row(
    "M7a-cards-numbers",
    "2.7 cards: every card number appears in its lesson",
    "cards.json L01-L03",
    "cards_check.py: 77 cards; the only two tokens not found as plain text are '2/3' (c026, L02 line 341 as \\tfrac23) and '-1/8' "
    "(c217, L03 as -\\tfrac18); both are present in typeset form. No other number token is missing.",
)
row(
    "M7a-cards-grades",
    "2.3 grades on cards: T for theorem and derived formula, C with basis for lab results",
    "cards.json L01-L03 (grades: T 64, C 13)",
    "All 13 C cards carry a basis naming Lab 1 (SIMULATED) or exact arithmetic (c012, c027, c028, c029, c030, c049, c050, c168, c169, "
    "c173, c178, c181, c189). The T cards state theorems or derivations on the page.",
)
row(
    "M7a-misconceptions-counts",
    "2.9 misconceptions: at least three per lesson, each with wrong belief and reason",
    "L01-L03 section#misconceptions",
    "Three misconception entries in each of L01, L02, L03 (counted: <li class=\"misconception\"> 3 per page), each with a wrong belief "
    "(class wrong) and a reason.",
)
row(
    "M7a-mutants",
    "2.6 mutation testing scope for this slice",
    "lab twins L01-L03 and the L01-L03 pages",
    "No project grader in this slice. Per the round ruling, lab twins are demonstrations and mutation testing applies to project graders "
    "only; no lab-mutation finding is raised (no lesson sentence claims that a lab detects a specific mutant). The ledger lists no mutants.",
)

# checks added this round on the subject of the L02 and hub cross references are above; nothing carried from round 1.
fragment = {
    "unit": "M7",
    "slice": "a",
    "round": 2,
    "verifier": "Haiku independent verifier, M7 slice a round 2 (did not build M7)",
    "pin": "9294b914",
    "base": "aeb512b6 (round-1 pin). Between them the slice files changed: L01.html, L02.html, L03.html, cards.json (and references.json, "
    "L04-L08, project and grader, outside this slice). index.html and tests/labs/M7/lab-M7-L01-1.py, lab-M7-L02-1.py, lab-M7-L03-1.py are byte-identical to aeb512b6, "
    "but every hub row was re-checked this round and none is carried.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-M7-a (detached at 9294b914, .venv symlinked)",
    "scratch": "/tmp/m7a_*.txt (copies of every output are in ledgers/M7/scripts/M7-a-r2/)",
    "verified_at": "2026-11-08",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "boyd2004convex and stokey1989recursive: records unchanged; verify_refs live 2 of 560 entries 0 problems; offline 560 entries 0 problems. "
        "No correction requested. The pages cite the Stokey record with three authors, as the hub states (index.html line 176).",
        "Notation (architect, not a slice defect): the bold-one glyph \\mathbf{1} is the ones vector in M7 and in other modules, while "
        "notation/notation.json binds the macro \\indic to tex \\mathbf{1} with meaning 'indicator function'. A NOTATION_REQUEST is needed: either "
        "register a ones-vector macro (for example \\ones) or change the tex of \\indic. If the architect rules that this is a collision, row "
        "M7a-notation-ones-glyph flips to FAIL for every M7 page that writes the ones vector.",
        "Notation (minor): the pages write \\operatorname{diag} where the registry macro \\diag would be used. Same rendering.",
        "Notation (local, for the architect): plain gamma is used in M7 for a curve (L02 line 83) and for risk aversion (L03 line 140). "
        "Both are defined locally, which the registry permits for conventionally local letters, but the \\emgamma note says plain gamma is kept for risk aversion.",
    ],
    "freshness_flags": [],
    "notes": [
        "Slice A: index.html (182 lines), L01.html (563), L02.html (546), L03.html (553), their three twins, and the 77 L01-L03 cards in cards.json. "
        "Every line of the four pages was read; the twins were read in full. Page code equals twin text and each expected block equals the twin's "
        "output (lab_check.py).",
        "Round-1 FAILs: M7a-notation-x-ast (x^\\ast reused for the minimizer) is FIXED at this pin (zero x^\\ast; w^*, w^\\ast, p^\\ast). "
        "M7a-cards-L03 (M7-c041 read as an iff) is FIXED (the back now says 'sufficient'). Both re-verified from scratch this round.",
        "Delta since the round-1 pin (aeb512b6..9294b914): L01 (4 lines), L02 (42), L03 (46), cards.json (80). Every changed hunk in the slice pages was "
        "read through the full re-read; the changes are wording and typesetting, and the two that change a claim (L02 quiz 3.2182; the L03 "
        "cards) were re-derived.",
        "Scripts (ledgers/M7/scripts/M7-a-r2/): gate_commands.sh (the commands run, in order); lab_check.py; recompute_L01_L03.py (65 OK checks, "
        "exit 0; output in recompute_L01_L03.out); cards_check.py (output cards_check.out); write_fragment.py (writes this fragment). "
        "Four other tracked files already sit in this folder at the pin (build_fragment.py, cards_dupes.py, recheck_L01_L03_indep.py, scan_text.py). "
        "They came with the checkout; I did not run them and did not use them as evidence.",
        "Not checked, honestly: run_graders.py, mutate_graders.py and the alternative solvers (project slice, not in A); L04-L08 and their cards "
        "(other slices); tools/build_site.py --check and render_curriculum.py (generated files outside this slice); the full pytest suite "
        "(only -k M7 tests/test_labs.py); page_smoke on a quiet machine (run once here, PASS, timing 0.6 s max for a lab). No external paper was "
        "read: the pages cite no source locator beyond the registry keys, and their claims are derivations on the page.",
        "Judgment noted, not a row: BUILDER 2.1 asks for <span class=\"claim\" data-grade> markup on every substantive claim. The slice uses claim spans "
        "only on theorem, proposition, lemma and example titles. check_pages does not require more, and no ungraded claim was found that a grade "
        "would change. Non-blocking.",
        "Hub note: 'M2 Calculus' is a short label (curriculum title 'Single & Multivariable Calculus'). Non-blocking.",
        "Tool note: check_pages --page index is not a supported mode; the hub is checked by the unit run (PASS).",
    ],
    "summary": {},
}

problems = ledger.validate(fragment, "M7-a")
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": 0, "unverifiable": 0}
fragment["summary"] = counts
problems = ledger.validate(fragment, "M7-a")
OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("validate:", problems if problems else "[] (valid)")
print("counts:", counts)
print("wrote", OUT)
