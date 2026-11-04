import json

SCRIPT_RECOMPUTE = "ledgers/BK4/scripts/BK4-b-r1/recompute_L04_L05.py"
SCRIPT_TWIN = "ledgers/BK4/scripts/BK4-b-r1/twin_page_check.py"
L04 = "course/modules/BK/BK4/L04.html"
L05 = "course/modules/BK/BK4/L05.html"
TWIN4 = "tests/labs/BK4/lab-BK4-L04-1.py"
TWIN5 = "tests/labs/BK4/lab-BK4-L05-1.py"
CARDS = "course/modules/BK/BK4/cards.json"

def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
    # ---- gates and commands (PASS)
    row("BK4b-gate-check-pages", "2.9-structure", f"{L04}; {L05}", "PASS",
        "Ran `.venv/bin/python tools/check_pages.py --unit BK4 --page L04` -> 'check_pages BK4 L04: PASS'; `--page L05` -> 'check_pages BK4 L05: PASS'; full `check_pages.py --unit BK4` -> 'check_pages BK4: PASS'. Lesson hours data-hours=7 (6-12 range)."),
    row("BK4b-gate-check-dag", "2.9-DAG", f"{L04}; {L05}; course/concepts.html:477,483,485", "PASS",
        "Ran `tools/check_dag.py --unit BK4` -> 'check_dag BK4: PASS'. Links resolve: L04 bank-money-creation (concepts.html:483), L04 settlement-cycle (L01.html:64 def-settlement-cycle), L05 clearing-and-settlement (concepts.html:477), trade-lifecycle (concepts.html:485), payment-system (L01.html:59). Plain-prose use of 'variance' (M4, outside closure) in L05 is allowed by the architect default (plans/BK4-build-plan.md Architect decisions)."),
    row("BK4b-gate-check-projects", "2.6-structure (unit gate)", "course/modules/BK/BK4/project.html", "PASS",
        "Ran `tools/check_projects.py --unit BK4` -> 'check_projects BK4: PASS'. Unit-level command, outside this slice's prose."),
    row("BK4b-run-labs", "2.5-labs", f"{L04}:155-357; {L05}:160-336", "PASS",
        "Ran `tools/run_labs.py --unit BK4 --page L04` -> 'run_labs BK4: PASS (1/1)'; `--page L05` -> 'run_labs BK4: PASS (1/1)'."),
    row("BK4b-twin-isolated-run", "2.5-labs", f"{TWIN4}; {TWIN5}", "PASS",
        f"`.venv/bin/python -I {SCRIPT_TWIN} <checkout>` (run in a temp dir): L04 exit=0 stderr='' ; L05 exit=0 stderr=''. Page code block equals twin after HTML unescape (L04 equal=True, L05 equal=True). Expected block equals twin stdout exactly (L04 True, L05 True)."),
    row("BK4b-twin-lint", "2.5-labs / BUILDER 6.1", f"{TWIN4}; {TWIN5}", "PASS",
        "`.venv/bin/ruff check` -> 'All checks passed!'; `ruff format --check` -> '2 files already formatted'; `.venv/bin/mypy --no-incremental` on both twins -> 'Success: no issues found in 2 source files'."),
    row("BK4b-pytest-labs", "2.5-labs", "tests/test_labs.py", "PASS",
        "`.venv/bin/python -m pytest tests/test_labs.py -k 'BK4 and (L04 or L05)' -q` -> 2 passed."),
    row("BK4b-page-smoke", "2.9-page_smoke", f"{L04}; {L05}", "PASS",
        "`.venv/bin/python tools/page_smoke.py --unit BK4 --pages L04 L05` -> 'page_smoke modules/BK/BK4/L04.html: PASS', 'page_smoke modules/BK/BK4/L05.html: PASS', 'page_smoke BK4: PASS' (labs lab-BK4-L04-1 and lab-BK4-L05-1 ran, 0.0 s each)."),
    row("BK4b-verify-refs", "2.1-citations", "references/references.json (bisndbasel)", "PASS",
        "`.venv/bin/python tools/verify_refs.py --unit BK4` (live) -> 'live re-verification of BK4: 2 of 560 entries, 0 problems'."),
    row("BK4b-citation-bisndbasel", "2.1-attribution / scope", f"{L05}:347", "PASS",
        "Span data-cite='bisndbasel' text 'Basel III: international regulatory framework for banks' matches the registry title prefix (references/references.json, bisndbasel, url https://www.bis.org/committees/bcbs/standards, index page). The sentence is limited to index level and says the operational-risk section was not read, which is consistent with the registry."),
    row("BK4b-cmd-recompute", "2.2/2.4/2.5 (independent recomputation)", SCRIPT_RECOMPUTE, "PASS",
        f"`python3 -I {SCRIPT_RECOMPUTE}` -> 'SUMMARY failures: 0'. About 110 checks, all PASS; script written by this verifier with Fraction arithmetic, separate from the lab code."),
    # ---- numbers (PASS)
    row("BK4b-numbers-L04-prose", "2.2 numbers (c)", f"{L04}:52,56-69,72-75,90,151-153,356,392-393,405-406,420-424,429-433", "PASS",
        "Recomputed by script: reserves 1,900,000 and 2,100,000 cents (Remark 1.3); coverage 9/10 -> 9000 bps, 11/10 -> 11000 bps, 113/120 -> floor 9416 (Remark 2.8, exact 28250/3 before floor); 9500 bps for 19/20 (M3); coverage 2/3 (M1), 1/3 (M2); E1 lowest 6875 at 21/25; E2 first >=10600 is 10625 at 1/5; E3 both sides -31/784; R2 x*=1/2; R1 threshold 20/19 = 1.0526315789 to 10 dp."),
    row("BK4b-numbers-L04-lab-table", "2.5 lab output vs prose", f"{L04}:318-355 (printed block) and 356 (interpretation)", "PASS",
        "All 13 printed rows (6 computed for rho=19/20 with 99/100 omitted; 7 computed for rho=21/20) re-derived: reserves_left, claims_left, coverage, bps all equal the printed values; 15 and 21 pairs; difference identity holds in every pair; interpretation row 21/50 (1,060,000; 1,160,000; 53/58; 9137) matches. Haircut rows 399/400 -> 199/200 -> 9950 and 20/19 -> effective 1 -> 10000 match lines 354-355."),
    row("BK4b-numbers-L05-prose", "2.2 numbers (c)", f"{L05}:95,153,162,392,435-436,442", "PASS",
        "Recomputed: Example 2.2 E[C]=(1/8)(2500)(7)=17500/8=4375/2=2187.5 cents, half-up 2188; Example 2.7 169/512 and 192/512 and 64/512; M1 1250; M3 1875; E2 difference 19140625 = 2*2500^2*(7/64)*(2+4+8); E3 448/512 = 7/8; Part D variances 57421875/4 (A3) and 133984375/4 (A4)."),
    row("BK4b-lab-table-L05", "2.5 lab output vs prose", f"{L05}:304-334 (printed block) and 335 (interpretation)", "PASS",
        "All eight Part B patterns: probabilities 343,49,49,7,49,7,7,1 over 512 and costs 0,10000,5000,15000,2500,12500,7500,17500 cents match the printed lines (script 'printed pattern probabilities/costs' PASS). Part C 1875 PASS. Part D no-cost 7/8 and 343/512 PASS."),
    # ---- mathematics (PASS)
    row("BK4b-math-L04-props", "2.4 mathematics", f"{L04}:94-153", "PASS",
        "Re-derived Prop 2.2 (reserves C0(rho-x), claims C0(1-x)); Prop 2.4 theta-1=(rho-1)/(1-x); Prop 2.5 numerator (rho-y)(1-x)-(rho-x)(1-y)=(y-x)(rho-1) (P1 expansion checked); Prop 2.6 theta-rho=x(rho-1)/(1-x) and equality set (script 'Prop 2.6 equality set' PASS); Prop 2.7 floor argument. Grid identity checks PASS. Assumptions 1-3 listed before each statement (L04:79-86)."),
    row("BK4b-math-L05-props", "2.4 mathematics", f"{L05}:83-154", "PASS",
        "Re-derived Prop 2.1 (E[1_F]=P(F)); Prop 2.2 (sum P(x)C(x), each factor sums to 1); Prop 2.4 (proof uses marginals only); Prop 2.5 (Var4-Var3 = 2k^2 p(1-p) sum_{i<j} l_i l_j; zero iff at most one l_i positive); Prop 2.6 ((1-p)^3 < 1-p). Random parameter checks (400 + 300 draws, exact Fractions) PASS for all five; zero-set check PASS."),
    row("BK4b-math-L04-R-problems", "2.4 / 2.5 problems", f"{L04}:428-433", "PASS",
        "R1 (rho*=1/(1-h); x=0 gives rho(1-h)<1 below it) re-derived; R2 (x*=(rho-c)/(1-c), theta=c, grid check PASS); R3 (x=r/C0 and x<=rho iff r<=Res0). Solutions correct. Note R1 uses 'admissible' undefined (see BK4b-L04-admissible-undefined)."),
    row("BK4b-math-L05-R-problems", "2.4 problems", f"{L05}:449-469", "PASS",
        "R1: E[C]=n p k l, ratio Var4/Var3 = n (script n=4 check PASS). R2: P(U) in [p,3p] gives no-fail in [5/8,7/8]; example distribution on 4-point space gives marginals 1/8 and no-fail 5/8 (script PASS); comonotone gives 7/8. R3: product of nonnegatives is monotone. All PASS."),
    row("BK4b-problems-L04-M-P-E", "2.4 problems", f"{L04}:401-424", "PASS",
        "M1 (2/3), M2 (1/3), M3 (9500 bps), P1 (expansion correct), P2 (equality set correct), P3 (floor argument correct), E1 (6875 at 21/25), E2 (10625 at 1/5), E3 (-31/784 both sides). Worked solutions present in details.solution."),
    row("BK4b-problems-L05-P-E", "2.4 problems", f"{L05}:399-445", "PASS",
        "P1 (E[1_A]=P(A)), P2 (Var of sum with A1+A3, only covariance uses A3), P3 (no-cost probabilities; (1-p)^2<1 argument), E1 (4375/2, 2188, 21.88 dollars), E2 (19140625, A4 larger), E3 (343/512 vs 7/8=448/512) all correct."),
    # ---- labs statements (PASS)
    row("BK4b-lab-L04-statements", "2.5 lab statements", f"{L04}:157,356", "PASS",
        "Hypothesis (157) predicts: 19/20 all coverage below 1 with 99/100 omitted; 21/20 none below 1, none omitted; identity and difference identity hold; haircut threshold 20/19. Printed output agrees for each. Interpretation (356) cites 15 and 21 pairs, row 21/50 values and monotone trends, all matching the printed block."),
    row("BK4b-lab-L05-statements", "2.5 lab statements", f"{L05}:158,162,335", "PASS",
        "Hypothesis (162) predicts 4375/2 and 2188, 1875 for equal delays, 343/512 and 7/8, equal means, larger A4 variance; all match the printed block. Interpretation (335) states the values for one parameter set and disclaims estimation; consistent."),
    row("BK4b-lab-docstrings-L04-other", "2.5 docstrings", f"{TWIN4}:1-25,30-60,66-123,130-163", "PASS",
        "Module docstring, Row, cents, coverage_of, state_after, print_path_table, check_differences, main, and the 'SIMULATED' label match the code and printed output. 'the lab counts those shares and prints the count' matches 'omitted rows' output line."),
    row("BK4b-lab-docstrings-L05", "2.5 docstrings", TWIN5, "PASS",
        "Module docstring (parts A to D, SIMULATED, one rounding step) matches main() and round_half_up usage (called once, on closed form). pattern_cost_cents, comonotone_outcomes, closed_form_mean docstrings match code."),
    # ---- misconceptions, quiz, key results, grades (PASS)
    row("BK4b-misconceptions-L04-1-2", "2.9 misconceptions", f"{L04}:391-392", "PASS",
        "Misconception 1 (rho=1 gives theta=1 under A1-A3; measured 1-h <1 under Assumption 4) matches Prop 2.4 and Remark 4.1. Misconception 2 (halving gives 19/40, not 9/10) matches Remark 2.8."),
    row("BK4b-misconceptions-L05", "2.9 misconceptions", f"{L05}:353-363", "PASS",
        "Misconception 1 (same mean, Prop 2.4; Part D prints 4375/2 both laws), 2 (169/512 vs 192/512; Example 2.7), 3 (Part B delays (1,2,4) gives 4375/2; Part C (2,2,2) gives 1875) all match."),
    row("BK4b-quiz-L04", "2.9 quiz", f"{L04}:452-531", "PASS",
        "10 items (8-15). Keyed answers re-derived: (rho-x)/(1-x); 0.9; exactly 1; 11000; falls; 9416; x>rho means payments exceed reserves; below 1; 1.0526315789; tokenization definition. Explanations match the lesson text."),
    row("BK4b-quiz-L05", "2.9 quiz", f"{L05}:492-574", "PASS",
        "10 items. Keys re-derived: p kappa sum l; 750; 343/512; 169; same mean; A4 larger variance (all delays positive); 2188; A3 needs independence; no failure rate given; definition of operational risk. Explanations match."),
    row("BK4b-key-results-L04", "2.3 grades", f"{L04}:437-450", "PASS",
        "Six T rows each cite Proposition 2.2/2.4/2.5/2.6/2.7 or Remark 4.1 with Lab 1 checks; each claim re-derived above."),
    row("BK4b-key-results-L05", "2.3 grades", f"{L05}:473-490", "PASS",
        "Five T rows cite Props 2.1, 2.2, 2.4, 2.5, 2.6 and Example 2.7; two C rows name Lab 1 Parts A/B and D with 'SIMULATED parameters, one set'. Grades agree with BLUEPRINT evidence rules (proved = T; lab read-off = C)."),
    row("BK4b-grades-claim-spans", "2.3 grades", f"{L04}:369-376 (Remark 4.1 span); {L05}:99-154 (T titles)", "PASS",
        "Claim spans: Remark 4.1 theta_h span graded T conditional on Assumption 4 (acceptable, the assumption is named). All theorem titles carry data-grade T and are proved on the page."),
    row("BK4b-why-length", "2.9 structure", f"{L04}:52; {L05}:51", "PASS",
        "Why-it-matters word counts (script-free count of visible text): L04 = 102 words, L05 = 119 words; both at or under 120."),
    row("BK4b-banned-and-process-words", "2.9 banned phrases / 1.3-1.4", f"{L04}; {L05}; {TWIN4}; {TWIN5}", "PASS",
        "check_pages banned-phrase check PASS. Manual grep for builder|verifier|round|fixer|request|planner|architect|orchestr|plan: only 'ledger' (L04:60, :527) used as a domain term (a token recorded on a ledger)."),
    row("BK4b-notation", "2.4 notation", f"notation/notation.json (macros, symbols); {L04}; {L05}", "PASS",
        "Macros used in these pages: \\E, \\Var, \\Cov, \\Prob, \\indic, \\R-free; all are registered in notation.json macros. Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q} do not appear in L04 or L05. Local symbols (rho, theta, h, x, y, c, C_0, D, Res, p, kappa, ell, F_i, Omega, P(x)) are defined on first use; 'admissible' is not (see its own row)."),
    row("BK4b-hours", "2.9 hours", f"{L04}:2; {L05}:2", "PASS",
        "data-hours=7 on both pages (within 6-12). The hub split is outside this slice."),
    row("BK4b-cards-L04-L05-scan", "2.7 cards (L04 and L05 cards, full read)", CARDS, "PASS",
        "Read all 32 cards BK4-c059 to BK4-c090 (L04 18, L05 14) against the lesson text. Each front/back matches the lesson's definition, proposition, example or lab output, grades agree (T with basis for proved results, C with 'Lab 1, Part ...; SIMULATED' for c086 and c087), and every card number appears in its lesson. Exception: BK4-c076 (separate row)."),
    row("BK4b-cards-duplicates", "2.7 duplicates", CARDS, "PASS",
        "Scan of all 90 cards in the unit deck (script inline, normalized fronts): no exact duplicate fronts. Word-set Jaccard >= 0.5 pairs: (c049,c050) 0.84 and (c045,c055) 0.56 are in L02/L03 (outside slice); (c068,c069,c070,c076) are different propositions. No duplicate within L04/L05 cards."),
    row("BK4b-cards-grades-basis", "2.7 cards grade and basis", CARDS, "PASS",
        "Graded cards carry basis: BK4-c068 to c071 (T, Propositions 2.4-2.7), c073 (T, Remark 4.1), c081 to c083 (T), c085 and c089 (T, Example 2.7), c086 and c087 (C, Lab 1 Parts B/D, SIMULATED). Definition cards carry cite []."),
    row("BK4b-dag-prose-terms", "2.9 DAG (unlinked names)", f"{L04}; {L05}", "PASS",
        "Unlinked outside-closure names read in both pages: 'variance' (M4) in L05 prose, 'haircut' and 'run' (FI4/SR1 plain prose, L04:380-385), 'bank money', 'central' not used. All allowed as plain prose by the architect default; no link, no dfn. No DAG_DEFECT."),
    row("BK4b-registry-citation-consistency", "2.1 registry", f"{L05}:347, {L05}:579", "PASS",
        "L04 cites no registry key (L04:536). L05 cites only bisndbasel, at index level (L05:347, L05:579). No other data-cite in L04 or L05."),
    # ---- FAIL rows
    row("BK4b-L04-assumption4-scope", "2.9 scope words / internal consistency", f"{L04}:85", "FAIL",
        "Text: 'This assumption is used only in Remark 4.1 and in Problem R1.' Assumption 4 is also used in Misconception 1 (L04:391, 'measured at (1-h) of face value'), in the key-results row (L04:447, 'Under the valuation convention of Assumption 4'), in quiz item L04q8 (L04:508), and in the Lab 1 haircut check (L04:157 hypothesis; lab code haircut_check, L04:189 and :283-294).",
        "Replace the sentence with: 'This assumption is used in Remark 4.1, Problem R1, Misconception 1, the key-results table and the Lab 1 haircut check.'"),
    row("BK4b-L04-seeded_path-docstring", "2.5 lab docstrings vs code", f"{TWIN4}:61-64 (page {L04}:218-221)", "FAIL",
        "Docstring: 'the fixed share 99/100 is appended ... so that the path reaches a share above both reserve ratios of this lab'. False: 99/100 = 0.99 < 21/20 = 1.05, and the rho=21/20 table prints x=99/100 as a computed row (coverage 6, 60000 bps; L04:341), not omitted. Also 'Return length distinct shares' is inaccurate: the function returns length+1 shares, and 99/100 is duplicated when 99 is sampled (120 of seeds 0-1999 sample 99).",
        "Docstring-only edit (no code change, so the printed output is unchanged): say the function returns length+1 shares, that 99/100 exceeds 19/20 but not 21/20, and that the appended 99/100 duplicates a sampled 99/100 for some seeds. Do not change the sampler range, because that changes the seed-7 output; if the code changes, re-run embed_labs --refresh lab-BK4-L04-1."),
    row("BK4b-L04-haircut-docstring", "2.5 lab docstrings vs code", f"{TWIN4}:127 (page {L04}:284-287)", "FAIL",
        "Docstring: 'coverage on either side of it'. The two printed ratios are 21/20 (effective 399/400, 9950 bps, below the threshold 20/19) and 20/19 (effective 1, 10000 bps, at the threshold). Neither is above it, so 'either side' is wrong.",
        "Change the docstring to: 'and coverage just below the threshold and at it.'"),
    row("BK4b-L04-misconception3", "2.9 internal consistency / scope 'only'", f"{L04}:393", "FAIL",
        "Text: 'The ratio is unchanged only when rho=1.' Proposition 2.6 (L04:132-137) gives equality theta=rho iff x=0 or rho=1, and with x=0 (no redemption) the ratio is unchanged for any rho (e.g. 19/20 at x=0 gives 19/20). The 'only' has no x>0 hypothesis.",
        "Change to: 'The ratio is unchanged only when rho=1 for a share x>0; with no redemption (x=0) it stays at rho (Proposition 2.6).'"),
    row("BK4b-cards-c076", "2.7 cards agree with lesson", f"{CARDS} (BK4-c076)", "FAIL",
        "Back: 'Under Assumptions 1 to 3, only when rho = 1.' The same unhedged 'only' as L04:393; Proposition 2.6 (L04:132-137) gives equality also at x=0.",
        "Change the back to: 'Under Assumptions 1 to 3, only when rho = 1 for a share x > 0; at x = 0 it stays at rho (Proposition 2.6).'"),
    row("BK4b-L04-admissible-undefined", "2.9 terms defined before use", f"{L04}:376 (first use), :391, :428-429, :470, :477, :484, :508", "FAIL",
        "'admissible share' (and 'admissible') is first used at L04:376 and never defined. The conditions it stands for (0 <= x < 1 and x <= rho) are the hypotheses of Proposition 2.2 (L04:95) but the term is not named or linked there.",
        "At Proposition 2.2 or Definition 2.1, add: 'A share x is admissible for a ratio r when 0 <= x < 1 and x <= r.' Then use 'admissible for rho(1-h)' in Remark 4.1 and in the problems."),
    row("BK4b-L04-remark3.2-FC1-paraphrase", "2.1 attribution (FC1)", f"{L04}:368; course/modules/FC/FC1/L01.html:81", "FAIL",
        "Text: 'FC1 defines bank money creation, within its model, as the increase in total deposits that follows a loan'. FC1 L01.html:81 defines it as 'the increase in total deposits that results when the bank makes a loan and the proceeds are deposited back at the same bank'. The redeposit condition is dropped.",
        "Quote the FC1 definition: 'the increase in total deposits that results when the bank makes a loan and the proceeds are deposited back at the same bank'."),
    row("BK4b-L04-def1.2-section4-claim", "2.9 cross-reference accuracy", f"{L04}:69", "FAIL",
        "Text: 'It does not value the reserve assets at market prices, and Section 4 treats that case.' Section 4 treats only a constant haircut to face value, and says it is 'not a sale' (L04:374-380). It does not model market prices.",
        "Change to: '... and Section 4 treats only a constant haircut to face value.'"),
    row("BK4b-L05-why-overreach", "2.5 lab statements overreach", f"{L05}:51", "FAIL",
        "Text: 'Lab 1 checks the expected cost ..., and shows that dependent failures leave the mean unchanged while the variance of the comonotone case is never smaller.' Lab 1 prints one parameter set (Part D, L05:330-334); the lesson's own interpretation says 'The lab shows these values for one parameter set' (L05:335). The general results are Propositions 2.4 and 2.5 (L05:117-139), not lab output.",
        "Change to: 'Propositions 2.4 and 2.5 show that dependent failures leave the mean unchanged and that the comonotone variance is never smaller; Lab 1 checks both for one parameter set.'"),
    row("BK4b-L05-why-terms", "2.9 terms defined before use", f"{L05}:51 (first uses of 'comonotone' and 'fail patterns')", "FAIL",
        "'comonotone' is first used at L05:51 and first defined at A4 (L05:73); 'fail patterns' is used at L05:51 before the definition in Proposition 2.2 (L05:100). The reader meets undefined terms in the opening paragraph.",
        "Rephrase the opening sentence without the two terms, e.g. 'shows that dependent failures leave the mean unchanged, and that the variance is never smaller when all three trades fail together.'"),
    row("BK4b-L05-why-ungraded-claim", "2.3 grades (ungraded substantive claim)", f"{L05}:51", "FAIL",
        "Opening sentence 'A settlement system depends on many steps, and a step that fails or runs late leaves a trade unsettled.' is a substantive claim about real settlement systems with no grade and no registry key (BUILDER_RULES 2.1). No source is on the page for it, and no registry record covers settlement-system design (plans/BK4-build-plan.md section 0.3).",
        "Remove the sentence, or restate it as the model premise: 'In this model a step that fails leaves the trade unsettled (Definition 1.2).'"),
    row("BK4b-L05-M2-citation", "2.4 proof citation hypotheses", f"{L05}:385", "FAIL",
        "Solution: 'By Proposition 2.6 the probability that no trade fails is (7/8)^3.' Proposition 2.6 (L05:142-144) concerns Prob(C=0) and needs ell_i >= 1 and kappa >= 1, which M2 does not state. The value is the pattern probability P(0,0,0) from the product formula in Proposition 2.2 (L05:100-109). The number is correct.",
        "Replace 'By Proposition 2.6' with 'By the product formula for the pattern (0,0,0) in Proposition 2.2'."),
]

fragment = {
    "unit": "BK4",
    "slice": "BK4-b",
    "round": 1,
    "verifier": "Haiku independent verifier, BK4-b round 1 (did not build BK4; first independent verification of this slice)",
    "pin": "1c1645f3b00eada2fb54d39c86d5d949e15b4fbc",
    "base": "none: first independent verification of BK4-b (round 1)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE1-BK4-b (detached at 1c1645f, .venv symlinked)",
    "scratch": "tempfile.TemporaryDirectory for twin runs only; all kept scripts are under ledgers/BK4/scripts/BK4-b-r1/",
    "verified_at": "2026-11-03",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "references/references.json bisndbasel used_by is ['BK1'] but L05 cites it (L05:347, :579). BK4 should appear in used_by at integration (plans/BK4-build-plan.md section 12, Q12). Not a row here; architect runs the registry tool.",
        "Registry titles and locators for the cited key were read; no record edited."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice: course/modules/BK/BK4/L04.html, L05.html, lab twins tests/labs/BK4/lab-BK4-L04-1.py and lab-BK4-L05-1.py, and the L04 and L05 cards of cards.json (BK4-c059 to BK4-c090). Read every line of both pages and both twins. Cards read in full.",
        "Mutants: none. The slice is lessons and lab twins, not a grader; per the rulings lab twins are demonstrations and mutation testing applies to grader/ only. No mutant is listed, so none is counted as a survivor.",
        "Not checked (outside slice): L01-L03, index.html, project.html, grader/, the other cards, the unit hub hours split, Duffie and Zhu, the SEC T+1 rule (neither is stated in L04 or L05; L05 cites bisndbasel only, at index level).",
        "Not checked: the Basel III operational-risk section (the page says it was not read and does not state it; no locator was needed).",
        "Not checked: no figures or charts in the slice, so no SVG, dark-mode or 360 px figure review. page_smoke ran both pages at both widths and both themes (PASS).",
        "Not run: run_graders, mutate_graders (grader is outside this slice), full ruff and mypy over the repository, full pytest, render_curriculum, build_site, fetch_data.",
        "Output note: check_pages, check_dag, check_projects, run_labs, page_smoke, verify_refs (live) were run on this pin exactly as the commands state; results recorded in the rows.",
    ],
    "summary": None,
}

# verdict is PASS only if every row is PASS
statuses = [r["status"] for r in rows]
fragment["verdict"] = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
counts = {s: statuses.count(s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = {"rows": len(rows), **counts, "mutants": 0, "mutants_killed": 0}

with open("ledgers/BK4/BK4-b.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), counts, fragment["verdict"])
