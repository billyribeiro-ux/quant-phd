import json, pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
S = "ledgers/M2/scripts/M2-c-r8/"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/B-M2-c.round7.json"))
prev_rows = {r["id"]: r for r in prev["rows"]}
CARRY_FILES = ("course/modules/M/M2/L14.html, L15.html, L18.html and tests/labs/M2/lab-M2-L14-1.py, L15-1.py, L18-1.py "
               "(cmp: byte-identical between pins 7aa909e95b75 and ce7b3821c288); the L14/L15/L18 card entries are identical in cards.json")
def carried(rid):
    r = dict(prev_rows[rid])
    r["evidence"] = f"Carried from round 7 ({CARRY_FILES}): " + r["evidence"]
    return r
def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    return r

rows = []
rows.append(row("M2c-gate-check-pages", "2.9-structure", "tools/check_pages.py --all", "PASS",
  S + "check_pages.out: 'check_pages M2: PASS' (exit 0) at pin ce7b382."))
rows.append(row("M2c-gate-check-dag", "2.9-dag", "tools/check_dag.py --all", "PASS",
  S + "check_dag.out: 'check_dag M2: PASS' (exit 0). The round-8 edits add no concept link; L16 R3 now cites Proposition 2.1 of its own lesson and Proposition 3.2 of L13 (L13 is in the prerequisite closure of L16)."))
rows.append(row("M2c-gate-run-labs", "2.5-labs", "tools/run_labs.py --unit M2", "PASS",
  S + "run_labs_M2.out: 'run_labs M2: PASS (27/27)' (exit 0)."))
rows.append(row("M2c-labs-twin-isolated", "2.5-labs", "tests/labs/M2/lab-M2-L13-1.py .. lab-M2-L18-1.py", "PASS",
  S + "twins_isolated.out: each of the six twins run as .venv/bin/python -I -W error exits 0 with 0 bytes stderr (twin_L1x.err). Twin L13 was re-run after its docstring edit; two consecutive runs give the same md5 (2fb84683...). " + S + "twin_vs_page.out (script twin_vs_page.py): page code == twin and page expected block == twin output for L13..L18."))
rows.append(row("M2c-gate-page-smoke", "2.9-smoke", "tools/page_smoke.py --unit M2 --pages L13 L14 L15 L16 L17 L18", "PASS",
  S + "page_smoke.out: 'page_smoke M2: PASS' (exit 0); each of the six pages PASS."))
rows.append(row("M2c-gate-ruff-mypy-pytest", "2.5-labs", "ruff check/format tests/labs/M2; mypy --no-incremental on the six L13-L18 twins; pytest tests/test_labs.py -k M2", "PASS",
  S + "ruff_check.out 'All checks passed!' (exit 0); ruff_format.out '27 files already formatted' (exit 0); mypy.out 'Success: no issues found in 6 source files' (exit 0); pytest_labs_M2.out 27 passed (exit 0)."))
rows.append(row("M2c-verify-refs", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
  S + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' (exit 0). The References sections of L13, L16, L17 were re-read and cite no registry key except the two named M2 sources, which are in references/references.json (spivak2008calculus, hubbard2015vector; both present)."))
rows.append(row("M2c-banned-scan", "1.3-1.4-banned", "course/modules/M/M2/L13..L18.html visible text and cards.json", "PASS",
  S + "banned_scan_r8.out: 51 hits (44 'approx' mathematical term, 6 'previous' lesson-nav, 1 ellipsis in an L15 lab docstring), the same kinds as round 7. No TODO, TBD, placeholder, verifier, builder, round, revised or corrected in the visible text of L13, L16, L17 (scanned this round) or in any L13-L18 card."))
rows.append(row("M2c-scope-words", "2.9-scope-words", "changed sentences: L13.html line 154 (lab docstring), L16.html line 326 (R3), L17.html line 202 (Section 4 bullet 2)", "PASS",
  "L13 line 154 'the same Python installation' replaces 'the same Python build': the lab is deterministic (no RNG, no I/O; two runs give identical output), so 'the same on every run' is supported. L16 line 326 names its own Proposition 2.1 and Lesson L13 Proposition 3.2 explicitly. L17 line 202 'The formula can fail without the continuity hypothesis' is now a possibility claim and is supported by Problem R2 (solution, L17.html lines 316-318: f(tu)/t -> sin(theta) for cos(theta) != 0, D_(0,1) f(0) = 0, so the directional derivative is not linear in u; recomputed in numcheck_L17_r8.out). The round-7 wording 'fails without' is no longer used."))
rows.append(row("M2c-notation", "2.4-notation", "notation/notation.json vs L13-L18 text", "PASS",
  "notation.json registers T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q. A regex over the six pages (LaTeX \\T, \\Phi, \\gamma_3, \\gamma_4, \\ast, R_f, \\mathbb{Q}, R^\\ast, R^{e\\ast}) finds 0 uses of each (round-8 run). The new text introduces no symbol."))
rows.append(row("M2c-structure-order", "2.9-structure", "BUILDER_RULES 4.2 order in L13-L18", "PASS",
  S + "structure_r8.out: all six pages in order why-it-matters, s1, lab, canon-breaks, misconceptions, problem-set, key-results, quiz, references (re-run this round)."))
rows.append(row("M2c-why-it-matters-length", "2.9-structure", "why-it-matters paragraph of L13-L18", "PASS",
  S + "structure_r8.out: word counts 106, 102, 89, 95, 83, 107 (all at most 120). The L13, L16 and L17 why-it-matters paragraphs (L13 line 51, L16 line 51, L17 line 51) are unchanged by the round-8 diff."))
rows.append(row("M2c-misconceptions", "2.9-structure", "misconceptions sections of L13-L18", "PASS",
  "Re-read this round: L13 section 6 (L13.html lines 236-252, three items, each 'wrong' paragraph then a correction with numbers recomputed: 32.6, 301.1 / 301.0, the truncation-only claim); L16 section 5 (lines 211-227, three items); L17 section 5 (lines 208-224, three items). L14, L15, L18 carried from round 7 (see carry prefix in the L14/L15/L18 rows)."))
rows.append(row("M2c-problem-tiers", "2.9-structure", "problem-set tiers of L13-L18", "PASS",
  S + "structure_r8.out: problems 12 and solutions 12 on each of the six pages; L13, L16, L17 tier layout re-read (L13 lines 258-331, L16 lines 233-331, L17 lines 230-329)."))
rows.append(row("M2c-quiz", "2.9-structure", "retrieval quizzes of L13-L18", "PASS",
  S + "structure_r8.out: quiz items 10 and explain blocks 10 on each page; multiple-choice items have one data-correct option (L13: 7 mc + 3 numeric). L13 quiz answers re-derived (L13.html lines 378-461: 1 central, 2 at 1e-8, 2.5, 4 f(x+h) and f(x-h), 0.1, |t| central 0, 2 subtraction exact)."))
rows.append(row("M2c-hours", "2.9-hours", "data-hours on L13-L18; hub index.html", "PASS",
  "grep 'data-hours' on L13..L18: 10 each (the attribute is on line 2 of each page and is unchanged by the round-8 diff). course/modules/M/M2/index.html is not in the round-8 delta (git diff --stat lists only L13, L16, L17, cards.json and the L13 twin in M2), so the hub split is byte-identical to the round-7 pin; round-7 hours arithmetic carried for it."))
rows.append(row("M2c-card-duplicates", "2.7-cards", "course/modules/M/M2/cards.json (all 379 cards)", "PASS",
  S + "card_dups_r8.out: no duplicate ids, no duplicate backs; a front-text duplicate check gives 0. The round-8 cards.json delta also touches L08, L10, L19, L23 entries (not this slice); the M2 card count is 379 (round 7 said 380)."))
rows.append(row("M2c-cards-L13", "2.7-cards", "cards.json, lesson L13 (M2-c181..c201, c380, c381)", "PASS",
  "Card M2-c187 (cards.json line 1325) now states 'For delta > 0 and M_3 > 0 (Lesson L13, Section 4)', matching L13.html line 143 and P3 (line 301); the round-7 FAIL on missing hypotheses is fixed. Re-read against the current lesson: c181-c201 and c380, c381 agree with the lesson numbers (Example 2.3 intervals, E1 ratio interval, Lab 1 values 1.364e-02, 4.530e-05, 10.03, 100.00, 6.603e-09, 2.154e-07, 1.548e-06, 5.859e-11). The proviso h* <= h0 that the sibling card M2-c186 carries is missing from M2-c187; that is tracked in row M2c-L13-balanced-proviso."))
for rid in ("M2c-cards-L14", "M2c-cards-L15"):
    rows.append(carried(rid))
rows.append(row("M2c-cards-L16", "2.7-cards", "cards.json, lesson L16 (M2-c239..c249)", "PASS",
  "The eleven L16 card entries are identical to the round-7 pin (per-lesson comparison, round-8 run) and were re-read against the CHANGED L16.html (Prop 2.1, Prop 3.1, Example 1.3 values 18.778112198 and 8.389056099, Lab 1 values, Misconceptions 1-3). The round-8 R3 edit is not cited by any card. All pass."))
rows.append(row("M2c-cards-L17", "2.7-cards", "cards.json, lesson L17 (M2-c251..c264)", "PASS",
  "The fourteen L17 card entries are identical to the round-7 pin and were re-read against the CHANGED L17.html: c252 (61.9602 degrees), c254 (Theorem 2.2 hypotheses), c256 (Theorem 3.1), c257 ('only in the four axis directions'), c258 (corner (1,1), 45 degrees), c259-c261 (Lab 1 values), c262-c264 (Misconceptions 1-3). The round-8 edit at L17.html line 202 is not cited by any card's wording. All pass."))
rows.append(carried("M2c-cards-L18"))
rows.append(row("M2c-L13-numbers", "2.2-numbers", "L13 prose numbers: Example 2.3, E1, E2, E3, R1, R3, Section 5, Misconceptions, Key results", "PASS",
  S + "numcheck_L13_r8.out recomputes every L13 number with an independent script: Example 2.3 intervals 0.0135914/0.0137280 and 4.4854e-5/4.5760e-5; E1 interval 9.990/10.101 and central 98.91/101.11; R1 2*sqrt(1e-3/e) = 0.0383604 (page 0.038360 is correct to six decimals); E3 cube root 6.2578e-6 and log10 -5.2036 (nearer 1e-5); CORR 4.1 h* 1.8076e-8 and B(h*) 4.9136e-8 (page 4.9e-8); R3 2^-53/1e-8 = 1.110e-8 and e times it 3.018e-8; E2 2delta/h 4.44e-8 and 4.44e-7, truncation 1.359e-9, ratio 326.7; M3 sin(0.01)/0.01 - 1 = -1.6667e-5; lab unrounded ratios: fwd/cen at 1e-2 = 301.00, fwd 1e-2/1e-3 = 10.030, cen = 100.0006, fwd 1e-9/1e-8 = 32.63; the two full-precision central errors at 1e-5 and 1e-7 differ by 4.4e-16 (< 1e-15, as the page says)."))
rows.append(row("M2c-L13-lab1", "2.5-labs", "L13 Lab 1 hypothesis, expected block, interpretation", "PASS",
  S + "twin_vs_page.out: L13 page code == twin and expected block == output. twins_isolated.out: exit 0, 0 stderr. The docstring change (line 154) is the only twin difference from round 7 and does not touch any printed value; the interpretation's claims match the expected block (10.03, 100.00, the 1e-08 and 1e-05 minima, 6.603e-09, 2.154e-07)."))
rows.append(row("M2c-L13-theorems", "2.4-mathematics", "L13 Theorem 2.1, 2.2, Corollary 4.1, Proposition 3.2 (proof), P1-P3", "PASS",
  "Re-derived this round from the page text (L13.html lines 71-135, 114-123, 301-303): Theorem 2.1 Taylor remainder of order one; Theorem 2.2 Taylor order two and the intermediate value theorem for m; Proposition 3.2 triangle inequality giving 2 delta/h and delta/h; Corollary 4.1 B'(h) = M/2 - 2delta/h^2, B'' = 4delta/h^3 > 0, B(h*) = 2 sqrt(M delta); P3 B_c' = M3 h/3 - delta/h^2, B_c'' > 0, B_c(h*) = 3 delta/(2 h*). All correct under the stated hypotheses."))
rows.append(row("M2c-L13-prop32-hypotheses", "2.4-mathematics", "L13.html Prop 3.2 hypotheses (lines 116, 125) and Corollary 4.1 hypotheses (line 133), with uses at lines 122, 129-135, 143, 229, 301, 367", "PASS",
  "Proposition 3.2 (line 116) states its three hypotheses; line 125 names all three; the proof (line 122) uses the first and the third; the second (exact arithmetic after evaluation) is used at line 122. Corollary 4.1 (line 133) carries the same hypotheses plus 'f'' continuous on [x, x+h0]'. Round-6 FAILs (Prop 3.2 hypotheses) remain fixed."))
for rid in ("M2c-L14-numbers", "M2c-L14-lab1", "M2c-L14-theorems", "M2c-L15-numbers", "M2c-L15-theorems", "M2c-L15-lab1"):
    rows.append(carried(rid))
rows.append(row("M2c-L16-numbers", "2.2-numbers", "L16.html Example 1.3 (line 72), Lab 1 hypothesis (line 112) and interpretation (line 197), E1 (line 289), E3 (line 303), R3 (line 328)", "PASS",
  S + "numcheck_L16_r8.out recomputes: F_x(1,2) = 18.778112198 and F_y(1,2) = 8.389056099; F(2,1) = 4 + e^2 = 11.389 is the largest |F| on the 12-point grid; max |F_xxx| on the grid = 7.389 (= e^2); 8e^2 = 59.112; E1 truncation 1.23e-10 and rounding 8.88e-11 (delta = 2^-53 * 8 = 8.88e-16); E3 F_xy = F_yx = 2 + 3e^2 = 24.167168; R3 truncation 3.333e-10, rounding 1e-10, total 4.333e-10; lab hypothesis rounding 1.14e-10. Every number on the page agrees with these values."))
rows.append(row("M2c-L16-prop21-31", "2.4-mathematics", "L16 Remark 1.2, Proposition 2.1 (line 79-84) and proof (lines 86-89), Proposition 3.1 (lines 97-105)", "PASS",
  "Proposition 2.1 hypotheses (segment inside U, continuous third derivative of t -> f(t,a2) on [a1-h,a1+h]) are the hypotheses of L13 Theorem 2.2 applied to phi; the proof uses Remark 1.2 and Theorem 2.2 correctly. Proposition 3.1: both axis quotients are 0 for every t != 0 (direct), and g((1/k,1/k)) = 1/2 as in L15 Example 3.4 (L15.html line 132 read this round); Corollary 3.2 of L15 is at L15.html line 116."))
rows.append(row("M2c-L16-R3-dependence", "2.4-mathematics", "course/modules/M/M2/L16.html line 326 (R3 statement) and line 328 (R3 solution)", "PASS",
  "The R3 solution arithmetic (truncation 3.33e-10, rounding delta/h = 1e-10, total 4.33e-10) and the identification of the violated hypothesis (exactness of the evaluation points a1 +- h, Proposition 3.2 of L13 third hypothesis) are correct and consistent with L13.html line 116 and Section 5. Re-read this round after the round-8 wording change at line 326."))
rows.append(row("M2c-L16-R3-xref", "2.9-structure", "course/modules/M/M2/L16.html line 326 (R3 statement): 'Bound the total error using Proposition 2.1 of this lesson and Proposition 3.2 of Lesson L13'", "PASS",
  "Round-7 FAIL fixed: Proposition 2.1 is in L16 (L16.html line 80, the central difference of a partial), and Proposition 3.2 is in L13 (L13.html line 115). xref_r8.out: every numbered reference in L16 resolves in the named lesson."))
rows.append(row("M2c-L17-numbers", "2.2-numbers", "L17.html Example 1.2 (line 66), Lab 1 hypothesis (line 119), E2 (line 293), E3 (line 300), R1 (line 311), Section 4 (line 204)", "PASS",
  S + "numcheck_L17_r8.out: gradient (1, 1.8775825619), length 2.1272790782, angle 61.9602 degrees; E3 delta = 0.03975 degrees = 6.94e-4 rad, 1-cos = 2.407e-7, |g|(1-cos) = 5.12e-7 (page 5e-7); R1 max-norm value 2.8776 at (1,1), rescaled gradient direction (0.5326, 1) with value 2.410182 (page 2.410182); E2 derivative formula phi''' = 6u1^2 u2 - u2^3 cos y checked by hand from f_xxy = 2 and f_yyy = -cos y (multiplicity 3 for f_xxy); bound 7 and truncation 1.2e-12 and rounding order 1e-10 are hand arithmetic, not script output."))
rows.append(row("M2c-L17-theorems", "2.4-mathematics", "L17.html Definition 2.1, Theorem 2.2 proof (lines 88-94), Theorem 3.1 proof (line 111), Section 4 (lines 201-204)", "PASS",
  "Theorem 2.2 proof re-read: telescoping with p_k in B since |p_k - a| <= |t|; mean value theorem on each coordinate step (L06); q_k -> a; continuity of each partial at a gives the limit. Theorem 3.1 identity |g - (u.g)u|^2 = |g|^2 - (u.g)^2 is correct. Section 4 bullet 1: g(tu) = cos(theta) sin(theta) for t != 0 (checked). Section 4 bullet 2 is the round-8 changed sentence (see M2c-scope-words)."))
rows.append(row("M2c-L17-lab1", "2.5-labs", "L17.html Lab 1 hypothesis (line 119), expected block (lines 187-193), interpretation (line 194)", "PASS",
  S + "twin_vs_page.out covers L17 (page code == twin; expected == output). Output: angle 62 degrees sampled, gradient angle 61.96, length 2.127279, both True lines; the interpretation's claims match. Lab not changed this round."))
for rid in ("M2c-L18-numbers", "M2c-L18-theorems", "M2c-L18-assumption1", "M2c-L18-lab1"):
    rows.append(carried(rid))
rows.append(row("M2c-grades", "2.3-grades", "grade tags in L13-L18", "PASS",
  "Key-results tables re-read: L13.html lines 365-372 (T for Theorems 2.1, 2.2, Proposition 3.2, Corollary 4.1, Example 2.3 intervals under Assumption 1; C for Lab 1 outputs); L16.html lines 340-344; L17.html lines 337-341. Each C row names Lab 1 as its basis. L14, L15, L18 carried from round 7."))
rows.append(row("M2c-attribution", "2.1-citations", "references sections of L13-L18 and any attributed claim", "PASS",
  "L13 section 10 (lines 463-467), L16 section 9 (lines 431-435), L17 section 9 (lines 432-436) re-read: no passage locator is claimed, and the two M2 sources are named as in curriculum/01-foundations.yaml lines 146-147 (Spivak, Calculus; Hubbard and Hubbard). references/references.json holds spivak2008calculus and hubbard2015vector. The round-8 diff touches none of these section lines (hunks at L13 line 154, L16 line 326, L17 line 202)."))
rows.append(row("M2c-labs-data", "2.5-labs", "L13-L18 lab blocks and data-files", "PASS",
  "grep for data-files in the six pages and the six twins: none. Each lab computes from closed forms (exp, sin, cos, the function g) with no fetched or embedded dataset; no simulated data is presented as real."))
rows.append(row("M2c-L13-balanced-proviso", "2.4-mathematics", "course/modules/M/M2/L13.html line 143 ('For delta > 0 and M_3 > 0, its smallest value is at h* = (3 delta/M_3)^(1/3).') and course/modules/M/M2/cards.json line 1325 (M2-c187 back)", "FAIL",
  "The central analogue of Corollary 4.1 is stated without the proviso that Corollary 4.1 carries. The bound (M_3/6)h^2 + delta/h is derived with M_3 = max|f'''| on [x - h_0, x + h_0] (L13.html line 143), so it is a bound only for h in (0, h_0] (the same range as Corollary 4.1, L13.html line 129). Its derivative B_c'(h) = M_3 h/3 - delta/h^2 is negative on (0, h*), so when h* > h_0 the smallest value of the bound on its range is at h_0, not at h*. Concrete: delta = 2^-52, M_3 = e, h_0 = 1e-6 gives h* = 6.2578e-6 > h_0, and the minimum on (0, h_0] is at h_0 (numcheck: B_c(h_0) = 2.2250e-10 > B_c(h*) = 5.3224e-11, as expected for a global minimum outside the range). Corollary 4.1 (L13.html line 135) states 'provided h* <= h_0'; M2-c186 (cards.json line 1322) carries that proviso; line 143 and M2-c187 do not. Verdict is about the statement, not the arithmetic: P3 (L13.html line 301) is correct for the formula on (0, infinity).",
  fix="In L13.html line 143 change 'its smallest value is at h* = (3 delta/M_3)^(1/3)' to 'its smallest value is at h* = (3 delta/M_3)^(1/3), provided h* <= h_0 (otherwise the smallest value on (0, h_0] is at h_0), as in Corollary 4.1'. In cards.json M2-c187 back (line 1325) add 'provided h* <= h_0' after '(3 delta/M_3)^(1/3), the minimizer' with the same wording. Re-run render-free gates that read the card text (check_pages, page_smoke)."))

frag = {
  "unit": "M2", "slice": "c", "round": 8,
  "verifier": "Haiku 5.5 independent verifier (B8)",
  "pin": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089",
  "base": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4 (round-7 pin; round-7 fragment /Users/billyribeiro/.fanout/frags/B-M2-c.round7.json used as context only; its PASS rows were not trusted, carried rows re-checked for byte identity)",
  "checkout": str(ROOT),
  "scratch": str(ROOT / "ledgers/M2/scripts/M2-c-r8"),
  "verified_at": "2026-10-28",
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": ("Slice L13-L18 and their six lab twins. No project grader, so no mutation test (ruling: lab twins are demonstrations). "
            "Round-8 delta for the slice (git diff 7aa909e..ce7b382 restricted to slice paths): L13.html line 154, L16.html line 326, L17.html line 202, cards.json (M2-c187 back; other lessons' cards not in this slice), tests/labs/M2/lab-M2-L13-1.py docstring line 5. "
            "L14, L15, L18 HTML and all of L14-L18 twins except L13 are byte-identical to the round-7 pin (cmp), and their card entries are identical (per-lesson comparison). "
            "Round-7 FAIL rows M2c-cards-L13 and M2c-L16-R3-xref are fixed (now PASS). New FAIL row M2c-L13-balanced-proviso (L13 line 143 and card M2-c187 omit the h* <= h_0 proviso that Corollary 4.1 and card M2-c186 carry). "
            "Scanner note: xref_r8.py reports 'L18 Theorem 2.2 -> MISSING' for L18.html line 347 'by Theorem 2.2 and Proposition 3.2 of Lesson L13'; the qualifier follows the list, the reference resolves to L13 Theorem 2.2 (L13.html line 83). Not a finding. "
            "Not checked this round: the live verify_refs run (network; no registry key is cited in the slice beyond the two named M2 sources); a fresh line-by-line re-read of L14, L15, L18 (carried by byte identity per the rules); browser execution beyond page_smoke; render_curriculum.py (no curriculum yaml changed in the delta)."),
  "summary": ("Slice c, round 8: 48 rows, 47 PASS and 1 FAIL (M2c-L13-balanced-proviso: the central balanced-step claim in L13 line 143 and card M2-c187 omits the h* <= h_0 proviso). "
              "All gates pass at ce7b382 (check_pages, check_dag, check_projects, run_labs 27/27, twins isolated, page_smoke, ruff, mypy, pytest -k M2, verify_refs offline, build_site --check). "
              "Round-7 FAILs M2c-cards-L13 and M2c-L16-R3-xref are fixed."),
}
out = pathlib.Path(S) / "" 
json.dump(frag, open("ledgers/M2/M2-c.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(rows), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
