"""Write the round-4 E3 slice-a fragment (ledgers/E3/E3-a.json). Rows are the round-3 ids plus new ids; no PASS row is carried."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyC4-E3-a")
S = "ledgers/E3/scripts/E3-a-r4/"
rows = []
def row(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

row("E3a-cmd-check_pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/index.html, L01.html, L02.html, L03.html", "PASS",
    "Re-run at b276325: output 'check_pages E3: PASS', exit 0 (" + S + "gates.out).")
row("E3a-cmd-check_dag", "tools/check_dag.py --all | grep E3", "course/modules/E/E3/*.html", "PASS",
    "Output 'check_dag E3: PASS', exit 0 (" + S + "gates.out).")
row("E3a-cmd-run_labs", "tools/run_labs.py --unit E3 --page L01|L02|L03", "course/modules/E/E3/L01.html, L02.html, L03.html", "PASS",
    "'run_labs E3: PASS (1/1)' for L01, L02 and L03, each exit 0 (" + S + "gates.out).")
row("E3a-cmd-twin-isolated", "python -I -W error on each twin; page code block equals twin", "tests/labs/E3/lab-E3-L01-1.py, lab-E3-L02-1.py, lab-E3-L03-1.py", "PASS",
    "Each twin exits 0 under -I -W error. " + S + "twin_equal.py prints 'page-code == twin: True' for L01, L02 and L03 (code blocks 6017/6145/5590 chars, twin files differ only by one trailing newline).")
row("E3a-cmd-pytest-labs", "pytest tests/test_labs.py -k E3 -q", "tests/test_labs.py", "PASS",
    "15 tests passed, exit 0 (" + S + "gates.out).")
row("E3a-cmd-ruff-mypy", "ruff check and format --check on tests/labs/E3; mypy --no-incremental on the three twins", "tests/labs/E3/*.py", "PASS",
    "'All checks passed!', '11 files already formatted', mypy 'Success: no issues found in 3 source files', all exit 0 (" + S + "gates.out).")
row("E3a-cmd-offline-registry", "tools/verify_refs.py --offline", "references/references.json (pratt1964risk cited by index.html and L02.html)", "PASS",
    "'offline integrity: 560 entries, 0 problems', exit 0 (" + S + "gates.out).")
row("E3a-cmd-page_smoke", "tools/page_smoke.py --unit E3 (browser run)", "course/modules/E/E3/index.html, L01.html, L02.html, L03.html", "PASS",
    "'page_smoke modules/E/E3/index.html|L01.html|L02.html|L03.html: PASS' with lab-E3-L01-1, L02-1, L03-1 each run; exit 0 (" + S + "gates.out). Round 3 could not run this; it runs in this checkout.")
row("E3a-cmd-verify_refs-live", "live Crossref check of the registry key used by the slice (pratt1964risk); whole-registry live run NOT performed", "references/references.json key pratt1964risk; index.html data-cite; L02.html line 616", "PASS",
    "Plain curl: GET https://api.crossref.org/works/10.2307/1913738 returned HTTP 200. Crossref title 'Risk Aversion in the Small and in the Large', container Econometrica, volume 32, issue 1/2, page 122, issued 1964-01. Matches the registry record (pratt1964risk). Recorded in " + S + "crossref_pratt.json is in /tmp/e3a-r4/.")
row("E3a-hub-structure", "hub index.html structure, hours, placement, ladder, data status, reading list", "course/modules/E/E3/index.html", "PASS",
    "Eight lessons of 7 h = 56 h; data-hours-project 14; 56+14=70 matches curriculum/02-economics-finance-core.yaml line 91 (hours: 70) and prereqs [E1, M4] (line 92). Hours split 80%/20% matches 56/70. Placement: 6/8=75% below the 80% bar, 7/8=87.5% above it (text correct). Placement answers 50 (100/2), 1 (variance of {0,2}), 0.5 (1/x at 2), 90.909 (100/1.1), 5000 (1/2 x 100^2) recomputed. Unlocks E4 (curriculum line 128), AP2 (line 227), AP7 (line 431) list E3 as prerequisite. Data-status and core-reading prose matches the lessons (Lesson 2 names Pratt for the name only).")
row("E3a-numbers-hub", "numbers in hub prose", "course/modules/E/E3/index.html, sections #placement, #lessons, #data, #reading", "PASS",
    "All figures recomputed (see E3a-hub-structure). The 'Data status' claim that Lesson 2 uses exact fractions for the gamble's mean and variance is backed by mean_and_variance() in tests/labs/E3/lab-E3-L02-1.py (Fraction arithmetic), and floats for certainty equivalents in Lessons 2 and 3 are backed by the twins.")
row("E3a-numbers-L01", "numbers in L01 prose, examples, problems, misconceptions, quiz and interpretation", "course/modules/E/E3/L01.html: Example 1.4 (lines ~ 83-84), M1 (solution), M2, M3, E1-E3, R3, misconceptions, quiz", "PASS",
    "Recomputed exactly in " + S + "recompute_L01.py (output recompute_L01.out): EV 150 CU; EU quadratic 45000 CU squared; M1 EV 59, EU 4030, u(59)=3481, difference 549; M2 mixture weights 1/6, 1/3, 1/2 and 400/3 CU; M3 65 and 95; Example 3.4 37500; E1 difference 7500; E2 40000; R3 25000 vs 22500; quiz 5/12 and 50. Lab printed values 15000/12500/15000 (EU linear), 45000/21250/37500 (EU quadratic) and the Part B values 39375, 40000, 41250 match. Round-3 FAIL on 'Remark 2.4 says' sentence not present in this round.")
row("E3a-numbers-L02", "numbers in L02 prose, examples, problems, misconceptions, quiz and interpretation", "course/modules/E/E3/L02.html: Example 1.5, Example 2.3, Section 3 and Lab 1 interpretation, canon-breaks, misconceptions, E1-E3, quiz", "PASS",
    "Recomputed in " + S + "recompute.py (recompute.out): Example 1.5 EU 9.743416, CE 94.934165, premium 5.065835 CU, 9493 and 507 cents; Lab Part B ratios 5.065835, 4.619495, 4.528811, 4.504565, 4.500046 with gaps 0.565835, 0.119495, 0.028811, 0.004565, 0.000046; 0.565835 is 11.17% of the exact premium and 12.57% of the approximation (E2); 900 CU half-variance is 177.66 times the exact premium ('about 178', misconception 1); E1 gap 0.004565 and factor 6.31 vs (0.25/0.1)^2=6.25. Linear premium 0 at all scales.")
row("E3a-numbers-L03", "numbers in L03 prose, examples, problems, misconceptions, quiz and interpretation", "course/modules/E/E3/L03.html: Example 2.5, M1-M3, E1-E3, R1, misconceptions, lab interpretation, quiz", "PASS",
    "Recomputed in " + S + "recompute.out: CE at gamma 0, 0.25, 0.5, 1, 2, 4 = 11250.0000, 10931.7733, 10615.8009, 10000.0000, 8888.8889, 7337.6161 (rounded 11250, 10932, 10616, 10000, 8889, 7338); 80000/9 exact; Example 2.5 1600 and 2000; mech-1 r_A(4)=1/8 and r_R=1/2; mech-2 3000 cents, expected prize 7000; mech-3 9000; E2 M = 9/80000; E3 bound (k+1)/2 = 5.5 for k=10; E1 rounding 10615.8009 -> 10616. Falling order on grid True.")
row("E3a-math-L01", "L01 propositions, proofs, definitions, problems", "course/modules/E/E3/L01.html sections 1-3, problems M1-M3, P1-P3, R1-R3", "PASS",
    "Read entire lesson. Prop 2.2 (mixture is a lottery; weights sum to 1), Prop 2.3 (linearity; finite split), Prop 3.1 (affine), Prop 3.3 (positive affine keeps ranking, b>0 needed; P2 gives b<0 reversal), R1 (maximizer is best outcome; equality condition) re-derived. Statements carry the needed hypotheses (A1, b>0). Remark 2.4 disclaims any representation result, consistent with R2.")
row("E3a-math-L02-proofs", "L02 proofs of Prop 1.1, 1.3, 3.1 and Arrow-Pratt results", "course/modules/E/E3/L02.html lines ~ 88-127 (Prop 1.1, 1.3), 166-200 (Prop 3.1), 130-160 (Section 2)", "FAIL",
    "Each proof step re-derived: Prop 1.1 (IVT via F1, injectivity via F5); Prop 1.3 Steps 1-3 and (b) (tangent-line bound, averaging, strictness under A4); Prop 2.2 (b cancels); Example 2.3 (r_A=1/(2w)); Prop 3.1 Steps 1-3 (expansion, continuity of inverse via F4, division by eps^2 giving 1/2 r_A s^2). The logic is valid, but the statements of Prop 1.3 and Prop 3.1 omit F1, which their proofs need (CE existence). Recorded as the new FAIL row E3a-L02-F1-hypothesis-omitted.")
row("E3a-math-L03-proofs", "L03 propositions, proofs, definitions, problems", "course/modules/E/E3/L03.html sections 1-2, problems M1-M3, P1-P3, E1-E3, R1-R3", "PASS",
    "Read entire lesson. Prop 1.2 (via M1 Prop 1.4 and 1.6(b)), Prop 1.4 (limit via A2: u_gamma = L (e^h-1)/h), Prop 1.7 (derivatives; r_A=gamma/w), Thm 2.1 (g=ln u'+gamma ln w, constant via F1; F1/F2 stated), Prop 2.4 (closed form, M^{1/s}; gamma=1 case), Prop 2.6 (homogeneity), Prop 2.7 (affine invariance), Remark 2.8 (rounding bound (k+1)/2 re-derived), R1 limits (gamma>1 to 0; 0<gamma<1 positive) re-derived. Hypotheses of Thm 2.1 include F1 and F2 as stated.")
row("E3a-lab-L01", "Lab 1 (L01) hypothesis, code, expected block, interpretation", "course/modules/E/E3/L01.html lines ~ 161-325; tests/labs/E3/lab-E3-L01-1.py", "PASS",
    "Twin equals page code; run_labs PASS; expected block equals the run. Hypothesis predictions (45000/21250/37500; six True in Part B; six order checks in Part C; ValueError messages) match the printed output. Docstring describes Parts A-D correctly. Interpretation sentences are supported by the printed lines.")
row("E3a-lab-L02", "Lab 1 (L02) hypothesis, code, expected block, interpretation", "course/modules/E/E3/L02.html lines ~ 195-369; tests/labs/E3/lab-E3-L02-1.py", "PASS",
    "Twin equals page code; run_labs PASS. Hypothesis: sqrt CE below 100 (Prop 1.3), exact premium above 4.5 CU approximation by a positive gap (0.565835), ratio approaching 4.5 with shrinking gap (gaps 0.565835 to 0.000046), linear premium zero: all match output. The docstring says 'floating-point at full double precision' and 'half up' which the code does (half_up_cents uses Decimal ROUND_HALF_UP). Interpretation sentence 'Part C prints zero premiums at three scales' matches.")
row("E3a-lab-L03", "Lab 1 (L03) hypothesis, code, expected block, interpretation", "course/modules/E/E3/L03.html lines ~ 179-323; tests/labs/E3/lab-E3-L03-1.py", "PASS",
    "Twin docstring now names itertools, math and fractions, and the module imports itertools (used in pairwise). Twin equals page code; run_labs PASS. Hypothesis predictions (11250, 10000, 80000/9 -> 8889, falling order) match output. The interpretation paragraph labels the checks as numerical evidence on one grid, consistent with the code.")
row("E3a-grades", "grade labels and evidence grades in key-results tables", "course/modules/E/E3/L01.html lines ~ 463-471; L02.html lines ~ 520-528; L03.html lines ~ 465-474", "PASS",
    "L01 and L02 key-results rows graded T with proofs cited; L03 key-results row for the lab checks graded C with 'Lab 1, floating-point checks ... not a proof'. Each graded result traces to a proof on the page or a lab (C). Footer statements updated to match.")
row("E3a-citations-pratt", "citation of Pratt (1964) in hub and L02", "course/modules/E/E3/index.html (Core reading, data-cite pratt1964risk), L02.html line 616", "PASS",
    "Registry record pratt1964risk (references/references.json): Econometrica 32, issue 1/2, page 122, 1964, DOI 10.2307/1913738, verified_by crossref. Live Crossref check above confirms it. L02 names Pratt for the name only, and attributes no result to him, consistent with the prose.")
row("E3a-notation", "symbols and macros against notation/notation.json", "course/modules/E/E3/index.html, L01.html, L02.html, L03.html", "PASS",
    "Macros used in the slice: \\E (151), \\Var (15), \\R (1), \\Prob (1), all registered in notation/notation.json macros. Registered program symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q do not occur in the slice. gamma, pi, varepsilon, zeta, xi, eta, kappa, R(h), s, K are lesson-local (notation.json 'about': gamma is conventionally local). No program symbol is given a second meaning.")
row("E3a-dag-crossunit", "DAG: concepts and cross-unit references used by L01-L03 and the hub", "course/modules/E/E3/L03.html lines ~ 50-65, 76-94, 124-136; concepts.html", "PASS",
    "L03 cites M1 Lesson 3 (exp/log, A2 addition, Props 1.4, 1.6(b)) and M2 derivative. M4 prereqs [M2] (curriculum/01-foundations.yaml line 194) and M1 defines exp/log (course/modules/M/M1/L03.html lines 60-63, 92, 118, verified by reading). Concept anchors used: expectation, variance, random-variable, derivative, utility-maximization show 'not yet released' in concepts.html; exponential-and-logarithm and discount-factor show 'defined here'. Hub text matches this.")
row("E3a-banned-phrases", "banned phrases and scope/placeholder markers in learner prose", "course/modules/E/E3/index.html, L01.html, L02.html, L03.html", "PASS",
    "ledgers/E3/scripts/E3-a-r4/prose_grep.py: 'banned: 0' for all four pages.")
row("E3a-prose-process-words", "process words in learner text (verifier, build, round, fixed, batch, slice, pin)", "course/modules/E/E3/index.html, L01.html, L02.html, L03.html", "PASS",
    "prose_grep.out.txt: 'process' hits are 'fixed lottery(ies)' (a lottery held fixed), 'round to the nearest whole cent' (arithmetic), 'Review deck' (product feature) and 'Predicted ... before running' (lab hypothesis convention). None is process language about the build or review. Round-3 hits at index.html:154 and :166, L01.html:564, L02.html:132 and :604 are gone.")
row("E3a-L03-remark-2.2-sentence", "round-3 FAIL: 'Remark 2.2 gives the limit' sentence", "course/modules/E/E3/L03.html line 332", "PASS",
    "Now reads 'Remark 2.2 states what Theorem 2.1 does not say.' Remark 2.2 (about line 120-ish, 'what the theorem does not say') states exactly that, so the cross-reference is supported.")
row("E3a-L02-key-result-hypothesis", "round-3 FAIL: missing mean-zero hypothesis in the L02 key-results Prop 3.1 row", "course/modules/E/E3/L02.html line 527", "PASS",
    "Row now reads 'Assuming F3, F4 and F5, for a gamble X with E X = 0, ...'. Mean-zero hypothesis present. (The Prop 1.3 row in the same table lacks F1; that defect is the separate FAIL row E3a-L02-F1-hypothesis-omitted.)")
row("E3a-L02-unnumbered-calculus-facts", "round-3 FAIL: calculus facts used without numbered assumptions", "course/modules/E/E3/L02.html lines 56-62 (F1-F6) and proof lines", "PASS",
    "F1 to F6 listed as numbered assumptions. Every proof that uses a calculus fact cites an F-number (IVT -> F1, Taylor Lagrange -> F2, Taylor Peano -> F3, inverse continuity -> F4, derivative positivity -> F5, elementary derivatives -> F6). grep for 'fact of calculus' returns nothing. Residual F1 omission in two statements is logged separately.")
row("E3a-L03-unnumbered-mvt", "round-3 FAIL: mean value theorem used without assumption in L03 Theorem 2.1 proof", "course/modules/E/E3/L03.html Theorem 2.1 and its proof (lines ~ 126-129); F1 at lines 64-70", "PASS",
    "Theorem 2.1 statement now starts 'Assuming F1 and F2'; proof says 'By F1, a function with zero derivative on an interval is constant'. F1 is numbered and stated.")
row("E3a-L02-uses-standard-deviation", "round-3 FAIL: unused 'standard deviation' in L02 Uses list", "course/modules/E/E3/L02.html line 37", "PASS",
    "Line 37 now reads 'variance' only. Standard deviation is not used elsewhere in L02 (grep).")
row("E3a-L02-F1-hypothesis-omitted", "omitted hypothesis: CE existence needs F1 (intermediate value), but statements of Prop 1.3 and Prop 3.1 assume only F2/F5 and F3/F4/F5", "course/modules/E/E3/L02.html line 104 (Prop 1.3 statement 'Assuming F2 and F5'), line 524 (key row), line 173 (Prop 3.1 'Assuming F3, F4 and F5'), line 527 (key row), line 98-ish (Definition 1.2 'unique c of Proposition 1.1'); proof Step 3 (Prop 1.3) and Step 2 (Prop 3.1)", "FAIL",
    "Definition 1.2 defines CE as the unique c of Prop 1.1, whose existence needs F1 (the image of an interval is an interval). Prop 1.3 Step 3 ('Let c = CE(X; u)') and Prop 3.1 Step 2 ('c_eps = CE(W_eps; u)') use that existence, so F1 is needed but absent from both statements and both key-results rows. Remark 1.4 also lists only F2 and F5. Fix: write 'Assuming F1, F2 and F5' for Prop 1.3 (statement, key row, Remark 1.4) and 'Assuming F1, F3, F4 and F5' for Prop 3.1 (statement and key row).")
row("E3a-L02-quiz-q7-distractor", "quiz item L02q7 has two correct options: v = -u also leaves r_A unchanged", "course/modules/E/E3/L02.html lines 580-586 (name=\"L02q7\"), explain at ~588; Proposition 2.2 at ~line 117-118", "FAIL",
    "For v = -u: v' = -u', v'' = -u'', so r_A^v = -v''/v' = -(-u'')/(-u') = -u''/u' = r_A^u. The option 'v = -u' is therefore also a transformation under which r_A is unchanged, yet it is marked incorrect; the item has two correct answers. The Prop 2.2 proof ('because b != 0 cancels') shows b != 0 suffices, while the statement says b > 0, so the item and the statement disagree. Fix: replace the distractor 'v = -u' with 'v = e^{u}' (r_A^v = r_A - u', which differs), and align the item text with Prop 2.2 (positive b) or rewrite Prop 2.2 to 'b != 0' and the item to 'a nonzero b'.")
row("E3a-cards-hypotheses-omitted", "flashcards for L01-L03 must carry the hypotheses of the proposition they cite (VERIFIER rule 10)", "course/modules/E/E3/cards.json ids E3-c019 (line 123-125), E3-c022 (142-145), E3-c027 (176-179), E3-c041 (275-276), E3-c043 (288-290)", "FAIL",
    "E3-c019 cites Prop 1.1 with only 'Under A1 to A3' (statement needs F1 and F5). E3-c022 cites Prop 1.3(a) with only 'Under A1 to A3' (needs F2, F5, and F1 for existence). E3-c027 cites Prop 3.1 with 'Under A1 and A5' (needs F3, F4, F5). E3-c041 cites Prop 1.7 with no hypothesis (needs F2). E3-c043 cites Thm 2.1 with 'A3 and A4' (statement also assumes F1 and F2). Fix: prefix each card's answer with the 'Assuming ...' hypotheses of the cited statement, as the lesson does.")

frag = {
    "unit": "E3",
    "slice": "E3-a",
    "round": 4,
    "round_note": "Round 4 independent verification of E3-a at pin b276325 (detached worktree /Users/billyribeiro/.fanout/wt/verifyC4-E3-a). Previous round 3 at ccfdf4c; delta for the slice files: index.html (3 prose hunks), L01.html (2 hunks), L02.html (multiple hunks), L03.html (multiple hunks), tests/labs/E3/lab-E3-L03-1.py (docstring only). Every hunk was read. No PASS row is carried from round 3: every row was re-run or re-derived in this round.",
    "verifier": "Haiku independent verifier, E3-a round 4 (did not build E3)",
    "pin": "b276325",
    "base": "ccfdf4c (round-3 pin; slice files changed since then, see round_note)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC4-E3-a (detached at b276325, .venv symlinked)",
    "scratch": "/tmp/e3a-r4/",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "references/references.json: verify_refs --offline '560 entries, 0 problems'. Live check run only for pratt1964risk (plain curl, HTTP 200, record matches). No registry edits.",
        "notation/notation.json: no program symbol given a second meaning in the slice."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/E/E3/index.html, L01.html, L02.html, L03.html, tests/labs/E3/lab-E3-L01-1.py, lab-E3-L02-1.py, lab-E3-L03-1.py, and the L01-L03 cards of cards.json (E3-c001 to E3-c055).",
        "Mutants: not required. The project-grader mutation rule does not apply to lab twins or lesson pages (ruling). No mutants were written for this slice. Lab twins were checked by re-running them and recomputing their printed values independently.",
        "Could not check: the whole-registry live verify_refs run (only the one key was checked live); the full repository gate (ruff/mypy/pytest on other units were not run as they are outside slice a); the other E3 slices (L04-L08, project) are out of scope.",
        "Hypothesis-level judgments on scope words ('every', 'all', 'only') were checked for the claims that carry a result (Section 'Key results', 'Where the canon breaks', hub Data status). Pure quantifiers in definitions and proofs were not individually graded.",
        "The Prop 1.4 limit in L03 rests on Assumption A2 (the limit (e^h-1)/h -> 1), which is stated as an assumption on the page, not proved. Accepted as a named numbered Assumption.",
        "Prop 3.1 proof divides by pi(eps) in the eta(pi) step; if pi(eps)=0 for some eps the division is undefined, but eta is only needed as a limit and the conclusion is unaffected. Not a row-level defect."
    ],
    "summary": {}
}
counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
frag["summary"] = counts
out = ROOT / "ledgers/E3/E3-a.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(counts, out)
