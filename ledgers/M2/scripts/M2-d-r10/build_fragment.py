import json, datetime, pathlib
S = "ledgers/M2/scripts/M2-d-r10/"
C = "Carried from round 9 (course/modules/M/M2/L19.html byte-identical since b6865c7): "
def carry(id_, check, loc, ev):
    return {"id": id_, "check": check, "location": loc, "status": "PASS", "evidence": C + ev + " Re-read in full this round; no defect found."}
def ok(id_, check, loc, ev):
    return {"id": id_, "check": check, "location": loc, "status": "PASS", "evidence": ev}
def bad(id_, check, loc, ev, fix):
    return {"id": id_, "check": check, "location": loc, "status": "FAIL", "evidence": ev, "fix": fix}

rows = []
# gates re-run this round on pin e8b10b8
rows += [
 ok("G-check-pages", "gate", "tools/check_pages.py --unit M2", S+"check_pages_M2.out: 'check_pages M2: PASS', exit 0."),
 ok("G-check-dag", "gate", "tools/check_dag.py --all", S+"check_dag.out: all units PASS, exit 0."),
 ok("G-check-projects", "gate", "tools/check_projects.py --all", S+"check_projects.out: all units PASS, exit 0."),
] + [ok(f"G-run-labs-L{n}", "2.5-labs", f"tools/run_labs.py --unit M2; course/modules/M/M2/L{n}.html <pre class=expected>",
      S+"run_labs_M2.out: 'run_labs M2: PASS (27/27)', exit 0; expected block equals twin stdout (see G-page-vs-twin).") for n in range(19,25)]
rows += [
 ok("G-twins-isolated", "2.5-labs", "tests/labs/M2/lab-M2-L19-1.py .. lab-M2-L24-1.py", S+"twins_isolated.out: python -I -W error exit 0, stderr 0 bytes for all six."),
 ok("G-page-smoke", "2.9-smoke", "tools/page_smoke.py --unit M2 --pages L19..L24", S+"page_smoke_slice.out: six pages PASS, 'page_smoke M2: PASS', exit 0."),
 ok("G-ruff", "gate", "tests/labs/M2/ (six slice twins)", S+"ruff.out: 'All checks passed!' exit 0 (ruff check tests/labs/M2/)."),
 ok("G-ruff-format", "gate", "tests/labs/M2/", S+"ruff_format_twins.out: '27 files already formatted', exit 0."),
 ok("G-mypy", "gate", "mypy --no-incremental (full repo)", S+"mypy_full.out: 'Success: no issues found in 255 source files', exit 0."),
 ok("G-pytest-labs", "gate", "tests/test_labs.py -k M2", S+"pytest_labs_M2.out: 27 passed, exit 0."),
 ok("G-pytest-docs-figures", "gate", "tests/test_docs_figures.py", S+"pytest_docs.out: 14 passed, exit 0 (re-run this round)."),
 ok("G-verify-refs", "gate", "tools/verify_refs.py --offline", S+"verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0."),
 ok("G-build-site", "gate", "tools/build_site.py --check", S+"build_site_check.out: 'site data current: 6 outputs', exit 0."),
 ok("G-page-vs-twin", "2.5-labs", "course/modules/M/M2/L19..L24.html <code data-run> vs tests/labs/M2/lab-M2-L19..L24-1.py",
    S+"page_vs_twin.out and page_vs_twin.py: code equals twin for all six pages after the single trailing newline the code block omits (recorded in the .out file as True under rstrip)."),
]
# L19 (byte-identical since b6865c7; carried)
for id_, ev in [
 ("L19-math-def-ex", "Example 1.2 Hessian [[6,8],[8,4]] and Definition 1.1 re-derived by hand."),
 ("L19-math-thm21", "Theorem 2.1 proof Steps 1-3 re-checked (double MVT, bound, limit in k)."),
 ("L19-math-ex22", "Example 2.2 limits f_xy(0,0)=-1, f_yx(0,0)=1 re-derived."),
 ("L19-math-thm31", "Theorem 3.1 proof: phi(0)=phi'(0)=0, |h^T M h|<=2|h|^2 max|M_ij| re-checked."),
 ("L19-math-prop33", "Proposition 3.3 proof: E(s)/E(s/2) -> 8 re-derived (1/6 over 1/48)."),
 ("L19-math-remark-R2-R3", "Problem R2 bound n|h|^2 and R3 threshold m/4 re-derived."),
 ("L19-prose-lab-numbers", "Lab 1 printed values vs expected block: 2.26e-11, 1.94e-11, ratios 3.9509/7.8836 etc. match; prediction 0.41218/2.14872 matches closed form."),
 ("L19-scope-words", "Scope words checked (only, every, every point); each backed by a stated hypothesis."),
 ("L19-canon-misconception-quiz", "Misconceptions 1-3 and quiz keys (f_xy=2 at (1,1) for x^2 y; g''(0)=2; 12 for x^3 y; 2 for e^x y; 8 for E(s)/E(s/2)) re-derived."),
]:
    rows.append(carry(id_, "2.4-math" if not id_.startswith(("L19-prose","L19-scope","L19-canon")) else "2.4-prose", "course/modules/M/M2/L19.html", ev))

rows += [
 ok("L20-math-thm12", "2.4-math", "course/modules/M/M2/L20.html Theorem 1.2 and proof (lines 62-72)", "5/3 re-derived; one-variable sums and monotone Corollary 2.3 of L09 cited correctly (L09.html line 114)."),
 ok("L20-math-prop22", "2.4-math", "L20.html Proposition 2.2 and proof (lines 81-89)", "Both orders re-derived: 2x+2x^2 then 5/3; y/2+1/3 then 5/3."),
 ok("L20-math-ex31", "2.4-math", "L20.html Example 3.1 (lines 207-212)", "d/dy[y/(x^2+y^2)] and d/dx[-x/(x^2+y^2)] re-derived; outer values pi/4 and -pi/4 under Assumption 3.1; f(t,0)=1/t^2 checked."),
 ok("L20-math-prop24", "2.4-math", "L20.html Proposition 2.4 and proof (lines 192-202)", "Midpoint sums: sum x_i/n=1/2, sum x_i^2/n = 1/3-1/(12n^2) (n=1 gives 1/4); induction step re-derived; exact fractions in lab match 5/3-1/(6n^2) for n=1..32."),
 ok("L20-prose-lab", "2.5-labs", "L20.html Lab 1 hypothesis, expected block (lines 181-188)", "run_labs PASS; printed values 3/2, 13/8, 53/32, 213/128, 853/512, 3413/2048 and errors -1/6..-1/6144 recomputed."),
 ok("L20-quiz-misc", "2.4-quiz", "L20.html quiz and R1-R3 solutions", "Keyed answers 3, 5/3, 1.3333 (4/3), -1/(6n^2), pi/4 and -pi/4 re-derived; R3 tag example 1/2 vs 1 correct."),
 ok("L20-problems-res2", "2.4-problems", "L20.html R2 question line 328 and solution line 330", "Previous FAIL re-verified: the question now asks why the half-open square does not satisfy the continuity hypothesis, and the solution answers it (not closed rectangle; unbounded at origin, f(t,0)=1/t^2)."),
 ok("L20-prose-lab-interp", "2.5-labs", "L20.html interpretation (line 189)", "Lab checks n in {1,2,4,8,16,32} and the odd-squares identity to n=50 as stated (lab main())."),
 ok("L20-remark23-no-proof-depends", "2.4-math", "L20.html Remark 2.3 (line 93)", "Proposition 2.2 and Theorem 1.2 proofs do not use the general statement; lab does not invoke it (lab docstring lines 106-107)."),
 bad("STRUCT-define-before-use", "2.4-structure", "course/modules/M/M2/L20.html line 206",
     "Line 206 (new in e8b10b8; absent at b6865c7) reads 'The next example, under Assumption 3.1, shows ...'. Assumption 3.1 is first defined at line 210. The previous round's FAIL at line 51 was cleared by rewording line 51, but the same term is now used before its definition at line 206. Lines 209, 212, 214, 225 are after the definition or carry the explicit pointer 'stated below on this page'.",
     "Delete 'under Assumption 3.1' from line 206 (the example's own sentence at line 209 already states the assumption), or move the Assumption 3.1 block above line 206."),
]
rows += [
 ok("L21-math-thm12", "2.4-math", "L21.html Theorem 1.2 and proof (lines 67-80)", "Box R inside U; sign change at y0-c and y0+c; uniqueness via strict monotonicity; continuity; MVT differentiability formula (y2-y1)/h = -F_x/F_y re-derived; F_y>0 on R places (x1,eta) in R."),
 ok("L21-math-thm21-ex22", "2.4-math", "L21.html Theorem 2.1 (line 87), Example 2.2 (line 97)", "Chain rule step re-derived; -0.75 from closed form and -2x/2y both equal -0.75; misconception F_y/F_x = 4/3 correct."),
 ok("L21-math-ex31-32", "2.4-math", "L21.html Example 3.1 (line 192) and Example 3.2 (line 196); Section 3 bullets", "dx/dy = -y/sqrt(1-y^2) zero at y=0; F_y=2y=0 and F_x=2 at (1,0); x^2+g^2 >= x^2 > 0; F=y^3-x example re-derived."),
 bad("L21-problems", "2.4-problems", "course/modules/M/M2/L21.html line 308 (Research R1 solution)",
     "The solution applies Theorem 2.1 without the page's own required prefix ('Assuming Assumption 1.3'), although Theorem 2.1 rests on Theorem 1.2 and therefore on the intermediate value assumption; it then says 'The sign rests on the stated hypothesis and on nothing else', which is false for the same reason. The derivative formula dy/dP0 = 1/P'(y) and the negative sign are otherwise correct (G_P0 = -1, G_y = P'(y) < 0).",
     "Prefix the solution with 'Assuming Assumption 1.3,' and replace 'and on nothing else' with 'and on Assumption 1.3 for the existence of y(P0)'."),
 ok("L21-prose-lab", "2.5-labs", "L21.html Lab 1 (lines 105-185)", "run_labs PASS; residuals 0, 2.2e-16, -1.1e-16, 0; F_y 2.77..2.40 range; differences 6.2e-13, 5.2e-14, 3.7e-12, 3.9e-12 as printed; E1-E3 solutions consistent."),
]
rows += [
 ok("L22-math-lemma-thm13", "2.4-math", "L22.html Lemma 1.2 and Theorem 1.3 (lines 62-84)", "Interior first-order condition and chain-rule proof re-derived."),
 ok("L22-math-remark14", "2.4-math", "L22.html Remark 1.4 (line 88)", "G(a,x)=f_x(x,a), dG/dx = f_xx != 0; L21 Theorem 1.2 applies; uniqueness of zero in J from F_y != 0 on I x J; hypotheses correctly stated."),
 ok("L22-math-ex15-prop21", "2.4-math", "L22.html Example 1.5 (line 93), Example 2.2 (line 250), Proposition 2.1 (line 239)", "f_x zero at a-1, f_xx=-a/(1+x)^2; V=a ln a-(a-1); V'=ln a; Prop 2.1 gives x*(1)+0=a/2 and a/2 = V' re-derived."),
 ok("L22-math-ex23-P2", "2.4-math", "L22.html Example 2.3 (line 255), P2 (line 325)", "V(a)=max(a,0); one-sided derivatives 1 and 0 at a=0; f_a(1,a)=1, f_a(0,0)=0 matching the one-sided derivatives."),
 ok("L22-prose-lab", "2.5-labs", "L22.html Lab 1 interpretation (line 230), misconception 3 (line 278)", "run_labs PASS; x_hat errors 9.1e-9.. and 5.4e-12 largest Part B error match printed values; 0.5*0.666667*1e-16 = 3.3e-17 recomputed."),
 ok("L22-lab-naive-partial", "2.5-labs", "L22.html Lab 1 Part B naive partial (lab lines 210-212; expected lines 227-229)", "Frozen-product central difference is 0 by construction; reduced partial equals x_hat; expected output matches run_labs."),
 ok("L22-prop21-hypothesis", "2.4-math", "L22.html Proposition 2.1 (line 239) hypotheses", "Hypotheses (g C^1 on U, c C^1, F satisfies H1-H3) suffice for the chain-rule proof (line 245)."),
]
rows += [
 ok("L23-math-prop21", "2.4-math", "L23.html Proposition 2.1 and proof (lines 67-76)", "P' and P'' term formulas re-derived; signs under positive cash flows verified."),
 ok("L23-math-prop22", "2.4-math", "L23.html Proposition 2.2 and proof (lines 79-86)", "v=1/(1+r), 1-v=rv, sum v^t=(1-v^N)/r, price F re-derived; r=0 case covered."),
 ok("L23-math-thm31-prop32-33", "2.4-math", "L23.html Theorem 3.1 (line 229), Proposition 3.2 (line 239), Proposition 3.3 (line 249)", "Lagrange remainder (1/6)P'''(theta)Delta^3; P''' = -sum t(t+1)(t+2)c_t(1+y)^(-t-3) < 0 re-derived; first-order error (1/2)P''(theta)Delta^2 >= 0."),
 ok("L23-prose-numbers", "2.5-numbers", "L23.html why-it-matters (line 51), interpretation (line 222), E1/E3 (lines 350, 362-364), misconceptions (lines 277, 285)",
    "Independent recomputation (ledgers/M2/scripts/M2-d-r10/recheck_numbers.out): P(0.04)=108110.895779..., rounds to 108111; P'=-851466.739529; P''=8376648.511919; -P'/P=7.875864; P''/P=77.482001; errors 403.7716, -15.0608 at +0.01 and 102.797, -1.91110 at +0.005, 25.9363, -0.240704 at +0.0025; rounded exact-minus-expansion -15 and 16 cents; P(0.05)=100000 and P(0.03)=117060 match the lab. All printed values and ratios match."),
 bad("PLAN-Q12-sensitivity-type", "plan-decisions", "course/modules/M/M2/L23.html canon-breaks (line 267) and E3 solution (line 364); plans/M2-build-plan.md Architect decision Q12",
    "Binding Architect decision Q12 (plans/M2-build-plan.md, 'Architect decisions 2026-10-28') says bond prices are integer cents and sensitivities are floats with a stated tolerance. The page instead states that the price, its derivatives and the Taylor terms are exact rational numbers (line 267) and that the money path keeps the derivatives as exact rationals (line 364). The page states no float tolerance for P' or P''; the only tolerance language is the data-tolerance attribute of the expected block and the central-difference differences in the interpretation.",
    "Either state the float tolerance for the sensitivities (P'(y0) and P''(y0) as floats with a numeric tolerance, as Q12 requires) and reword lines 267 and 364, or record with the architect that Q12 is superseded by exact rationals."),
 ok("L23-problems-quiz", "2.4-problems", "L23.html M1-M3, P1-P3, R1-R3, quiz items 1-8 (lines 297-478)", "M1 1000 (50/1.05+1050/1.05^2 = 1000.000), M3 -200/1.04^3, quiz q8 P'=-1777.07 for c1=-1, c2=1000 at 0.04 recomputed; quiz key answers 1000, -200 correct."),
 ok("L23-cards-meta-introduces", "2.8-meta", "L23.html meta-row line 38 and meta description line 7", "'Introduces: none' is consistent with plans table (L23 concept 'none'); duration and convexity appear only as unlinked preview text in the lab docstring (line 91) and meta description; no dfn, no link (Q8)."),
 ok("L23-notation-F", "2.3-notation", "L23.html line 80-85 (face value F)", "F is the face value only in this lesson; no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^e*, R_f, Q) is used; notation.json registry checked."),
 ok("L23-money-int-cents", "2.5-money", "L23.html Lab 1 Part C (lines 201-207) and canon-breaks (line 267)", "price_cents uses round(Fraction) (half-even, integer); expected block 108111, 100000, 117060; 100015 and 117044 approximations rounded; no float in the money path of the lab code."),
]
rows += [
 ok("L24-math-thm21", "2.4-math", "L24.html Theorem 2.1 and proof (lines 59-67)", "D+ = 1, D- = -1, D0 = 0 for |x| at 0 for every h>0 re-derived; no derivative at 0 follows."),
 ok("L24-math-prop31-32", "2.4-math", "L24.html Propositions 3.1-3.2 and proofs (lines 73-94)", "D+ - f' = (1/2) h f''(xi); D0 - f' = (1/12) h^2 (f'''(xi1)+f'''(xi2)), bound (1/6) M3 h^2 re-derived."),
 ok("L24-math-prop42-43", "2.4-math", "L24.html Propositions 4.2-4.3 and proofs (lines 105-123)", "Triangle bound 2 delta/h; g(h)=Ah+B/h minimum h=sqrt(B/A)=2 sqrt(delta/M2), value 2 sqrt(M2 delta); central h*^3=3 delta/M3 re-derived; R1 solution 10x round-off recomputed."),
 ok("L24-prose-lab-table", "2.5-labs", "L24.html Lab 1 (lines 134-244) and interpretation (line 243)", "run_labs PASS; error table recomputed independently (ledgers/M2/scripts/M2-d-r10/recheck_numbers.out) to 3 significant digits at every k=1..15; minima k=8 forward and k=5 central; predicted minimizers 1.807e-8 and 6.257e-6 recomputed."),
 ok("L24-problems-quiz", "2.4-problems", "L24.html M1-M3, P1-P3, E1-E3, R1-R3, quiz (lines 280-463)", "M1 quotients of x^2 (2+h, 2-h, 2); M3 12.61 and bound 0.63 >= 0.61; R1 ratio of round-off terms; quiz answer 1 for delta=0.5, M2=2 re-derived."),
 ok("L24-meta-introduces", "2.8-meta", "L24.html meta-row line 38", "'Introduces: none' consistent with the plan table; cancellation defined in Section 4 (line 98) and first used after it."),
 ok("L24-AD-link", "2.8-links", "L24.html R3 (line 373) and L14.html heading", "L14 is 'Automatic Differentiation: Forward and Reverse Mode'; forward-mode statement matches its title."),
 ok("L24-solution-unrounded-errors", "2.5-labs", "L24.html E3 solution (line 348) and interpretation (line 243)", "Recomputed central errors 5.858691309867936e-11 at h=1e-5 and 5.858735718788921e-11 at h=1e-7: values match 5.858691e-11 and 5.858736e-11, difference 4.4e-16 = one ulp of e (4.44e-16)."),
]
rows += [
 ok("CARDS-slice", "2.10-cards", "course/modules/M/M2/cards.json, the 96 cards of L19-L24",
    "All 96 cards read this round (ids M2-c280..c294, c295..c307, c308..c322, c323..c337, c338..c357, c358..c375, c387). Numbers match lab outputs and lesson statements; card hypotheses match the lesson statements; no duplicate ids or fronts; gaps (c290, c344, c356, c366, c369, c374, c376..c386) are unused ids, not defects."),
 ok("CARDS-c299-uses-nowhere", "2.10-cards", "cards.json M2-c299 (L20 general iterated-integral statement)", "Back text 'No proof on this page depends on it' matches L20 Remark 2.3; card changed in this delta (front reworded); consistent."),
 ok("CARDS-slice-remark-check", "2.10-cards", "cards.json Remark cards M2-c285, M2-c292, M2-c299, M2-c351", "Remark 3.2, Theorem 2.1 misconception, Remark 2.3, Remark 3.4 cards agree with the current lesson text."),
 ok("DAG-prereq-use", "2.11-dag", "tools/check_dag.py --all (gate); L19-L24 uses lines", "check_dag M2 PASS; L19 uses L04, L08, L16, L17; L20 uses L01, L09, L10; L21 uses L04, L16, L18 (plan table); L22 uses L04, L16, L21; L23 uses M1 L05/L06 by link, L08, L21 (R1); L24 uses L08, L13, L14 (R3). All prerequisites are earlier in M2 or in M1 and linked by data-concept."),
 ok("DAG-links-anchors", "2.11-dag", "data-concept links in L19-L24", "Targets present: L01 def-limit, L04 def-derivative, L08 def-taylor-theorem, L09 def-definite-integral, L13 def-finite-difference-derivative, L16 def-partial-derivative, L17 def-gradient, L21 def-implicit-function-theorem, L22 def-envelope-theorem, concepts.html present-value, discount-factor, geometric-series (M1 L05 and L06 anchors exist)."),
 ok("DAG-architect-decisions", "2.11-dag", "plans/M2-build-plan.md Architect decisions Q2-Q8, concept table lines 85-90", "Q2: no M3 link in L19 (none). Q3: Fubini not named; Remark 2.3 states the general fact without proof. Q4: no Lagrange multiplier in L22 (grep). Q5-Q7: no dfn for prose-only terms (only hessian, multiple-integral, implicit-function-theorem, envelope-theorem). Q8: duration/convexity unlinked. Q12 deviation logged as PLAN-Q12-sensitivity-type."),
 ok("HOURS", "2.12-hours", "course/modules/M/M2/index.html line 142 and L19-L24 data-hours", "24 lessons x 10 h = 240 (hub data-hours-lessons=240); project 60; total 300 (hub header). Each of L19-L24 declares data-hours=10."),
 ok("STRUCT-process-words", "2.12-structure", "L19-L24 learner text", "grep for revise, round, corrected, fixed, builder, verifier, previous, now, we, I: only mathematical uses of 'previous' (lab code: previous error over current error) and 'fixed'/'fixed step' as mathematics."),
 ok("STRUCT-scope-words", "2.12-structure", "L19-L24 scope words (only, all, always, every, any, same, exactly, never)", "Each occurrence checked: L20 'never assumes every integrand is covered' is a restriction; L23 'every cash flow positive' is a stated hypothesis; L22 'every x maximizes' at a=0 follows from f=ax; no unsupported scope claim found."),
 ok("STRUCT-define-before-use-other", "2.12-structure", "L19-L24 defined terms", "Assumption 1.3 (L21), Assumption 1.1 (L22), Assumption 4.1 (L24), Definition 4.1 (L24), o(s^k) (L19 section 3), omega (L19 Theorem 3.1), H1-H3 (L22) defined before their main use; only L20 line 206 is out of order."),
 ok("REF-registry", "2.13-refs", "tools/verify_refs.py --offline; references in L19-L24", "560 entries, 0 problems; spivak2008calculus and hubbard2015vector present in references/references.json; no bibliographic claim attributed (pages say no locator confirmed)."),
 ok("NOTATION-registry", "2.13-notation", "notation/notation.json vs L19-L24 symbols", "Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q: none used in L19-L24. Macro usage: \\mathbb{R} written out (expansion of registered \\R); no unregistered macro used."),
]

frag = {
 "unit": "M2", "slice": "d", "round": 10,
 "verifier": "Haiku 5.5 independent verifier, slice d (L19-L24), round 10",
 "pin": "e8b10b8", "base": "b6865c7",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB10-M2-d",
 "scratch": "/Users/billyribeiro/.fanout/wt/verifyB10-M2-d/ledgers/M2/scripts/M2-d-r10",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": ["cards.json M2 changed in delta b6865c7..e8b10b8 (ids c299, c326, c345-type wording, c388 is L10 and outside this slice); L19 byte-identical since b6865c7 so its rows are carried."],
 "notes": [
   "Delta b6865c7..e8b10b8 in the slice: L20.html (lines 51, 206, 209-214, 225, 330), L21.html, L22.html, L23.html, L24.html, cards.json. L19.html and the six twins are byte-identical since b6865c7; L19 rows are carried from round 9.",
   "Round 9 FAIL L20-problems-res2 is cleared (R2 question reworded and answered). Round 9 FAIL STRUCT-define-before-use is NOT cleared: the forward reference moved from line 51 to line 206 in this round's edit.",
   "New FAIL L21-problems (R1 solution: 'rests on nothing else' and missing Assuming-Assumption-1.3 prefix).",
   "New FAIL PLAN-Q12-sensitivity-type (binding Architect decision Q12 vs exact-rational wording in L23).",
   "No mutants created: the slice is lesson pages, and mutation testing applies to project graders only (rulings). Lab twins are demonstrations.",
   "Not checked: browser render of the six pages (page_smoke only); no network access used; no published source read, so no locator was verified (none cited as a grade basis); plans/M2-open-items.md not re-read.",
 ],
 "summary": "Slice d (L19-L24), round 10 at e8b10b8, delta from b6865c7. Verdict FAIL. 79 rows: 76 PASS, 3 FAIL. FAILs: STRUCT-define-before-use (L20 line 206 uses Assumption 3.1 before line 210; low), L21-problems (L21 line 308 R1 solution: missing Assuming Assumption 1.3 and 'rests on nothing else' is false; low), PLAN-Q12-sensitivity-type (L23 line 267/364 exact rationals vs Q12 floats with stated tolerance; low). All gates re-run on the pin and PASS. Every L19-L24 number recomputed independently (recheck_numbers.out).",
}
pathlib.Path("ledgers/M2/M2-d.json").write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(len(rows), sum(r["status"]=="PASS" for r in rows), sum(r["status"]=="FAIL" for r in rows))
