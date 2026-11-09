"""Round-14 writer for the E3 slice f fragment (ledgers/E3/E3-f.json). Rows are built from the round-14 checks."""
import datetime
import json
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD14-E3-f"
SCR = "ledgers/E3/scripts/E3-f-r14"
cards = json.load(open(f"{ROOT}/course/modules/E/E3/cards.json", encoding="utf-8"))
by_id = {c["id"]: c for c in cards}
rows = []


def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


CMD = "Round 14 command output in " + SCR + "/out/"
row("E3f-cmd-check_pages", "2.9-structure", "tools/check_pages.py --unit E3 (and --page L01..L04)", "PASS",
    CMD + "check_pages_unit.out and check_pages_L01..L04.out: 'check_pages E3: PASS' and per page PASS (gates.sh).")
row("E3f-cmd-check_dag", "2.9-define-before-use", "tools/check_dag.py --unit E3", "PASS",
    CMD + "check_dag_unit.out: 'check_dag E3: PASS'.")
row("E3f-cmd-check_projects", "2.6-projects", "tools/check_projects.py --unit E3", "PASS",
    CMD + "check_projects_unit.out: PASS (project slice owns the content).")
row("E3f-cmd-page_smoke", "2.9-structure", "tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04 (run alone)", "PASS",
    "ledgers/E3/scripts/E3-f-r14/out/page_smoke_L01_L04.out: page_smoke modules/E/E3/L01..L04.html PASS, rc=0 (console errors, math, external requests and 360 px checks as tool-defined).")
row("E3f-cmd-pytest-labs", "2.5-labs", "pytest -q tests -k 'E3 or lab'", "PASS",
    "Run in checkout: all tests selected passed (100%), including tests/test_page_checks.py and the E3 lab twins.")
row("E3f-cmd-ruff-labs", "2.5-labs", "ruff check tests/labs/E3 course/modules/E/E3/grader; ruff format --check tests/labs/E3", "PASS",
    CMD + "ruff_check.out 'All checks passed!'; ruff_format.out '11 files already formatted'.")
row("E3f-cmd-mypy-twins", "2.5-labs", "mypy --no-incremental (repository configuration)", "PASS",
    CMD + "mypy.out: 'Success: no issues found in 385 source files'.")
row("E3f-cmd-verify_refs", "2.1-citations", "tools/verify_refs.py --offline and --unit E3 (live)", "PASS",
    CMD + "verify_refs_offline.out: '560 entries, 0 problems'; verify_refs_unit_E3.out: 'live re-verification of E3: 5 of 560 entries, 0 problems', rc=0.")
row("E3f-cmd-build_site-render", "2.9-structure", "tools/build_site.py --check; tools/render_curriculum.py then git status", "PASS",
    CMD + "build_site_check.out 'site data current'; render_curriculum.out regenerated files; git status after the run shows no tracked change (identical bytes).")
row("E3f-cmd-pytest-docs", "2.1-citations", "pytest tests/test_docs_figures.py tests/test_refs.py", "PASS", CMD + "pytest_docs.out: all dots, no failure.")
row("E3f-cmd-run_labs-L01-L04", "2.5-labs", "tools/run_labs.py --unit E3 --page L01..L04", "PASS",
    CMD + "run_labs_L01..L04.out: each 'run_labs E3: PASS (1/1)'.")
for lab, page in (("L01", "L01"), ("L02", "L02"), ("L03", "L03"), ("L04", "L04")):
    row(f"E3f-lab-{lab}", "2.5-labs", f"course/modules/E/E3/{page}.html lab block; tests/labs/E3/lab-E3-{lab}-1.py", "PASS",
        "ledgers/E3/scripts/E3-f-r14/check_twin_equality.py (out/check_twin_equality_L01_L04.out): page code equals twin byte for byte (after HTML unescape); expected block equals stdout of python -I -W error twin, rc=0, empty stderr. Hypothesis precedes the code; seeds and no network checked by reading (L04 uses random.Random(SEED); others draw no random numbers). Interpretation checked against output line by line.")
row("E3f-lesson-numbers-L01", "2.2-numbers", "course/modules/E/E3/L01.html (Example 1.4, Example 3.4, Misconceptions 1-3, Problems M1-M3, P1-P3, E1-E3, R1-R3, quiz numbers)", "PASS",
    "ledgers/E3/scripts/E3-f-r14/check_L01_L02_numbers.py (out/check_L01_L02_numbers.out): 150, 45000, 59, 4030, 50, 175, 37500, 25000, 22500, 5/12 re-derived exactly; lab values 15000/12500/15000, 45000/21250/37500 and linearity lines match the printed output.")
row("E3f-lesson-numbers-L02", "2.2-numbers", "course/modules/E/E3/L02.html (Example 1.5, Example 2.3, Section 3, Lab 1 interpretation, Misconception 1, E1-E3, quiz numbers)", "PASS",
    "check_L01_L02_numbers.py: sqrt sum 9.7434164903 (prints 9.743416), CE 94.9341649 (94.934165; squaring the printed 9.743416 gives 94.934155), premium 5.0658351 -> 507 cents, CE 9493.4165 -> 9493; 0.565835, 4.5, 11.17% (0.11170 of exact premium), 12.57% (of approximation); Part B ratios 4.619495, 4.528811, 4.504565, 4.500046 and gaps 0.119495, 0.028811, 0.004565, 0.000046 match the exact recomputation; E1 ratio 6.31.")
row("E3f-lesson-numbers-L03", "2.2-numbers", "course/modules/E/E3/L03.html (Example 2.5, Lab 1 prints, Remark 2.8, Misconceptions 2-3, Problems M1-M3, E1-E3)", "PASS",
    "ledgers/E3/scripts/E3-f-r14/check_L03_numbers.py (out/check_L03_numbers.out): CE 11250.0000, 10931.7733, 10615.8009, 10000.0000, 8888.8889, 7337.6161 (rounded 11250, 10932, 10616, 10000, 8889, 7338); 80000/9; Example 2.5 values 1600 and 2000; M2 3000; M3 9000; M1 1/8 and 1/2 via formula.")
row("E3f-lesson-numbers-L04", "2.2-numbers", "course/modules/E/E3/L04.html (Lemma 1.2, Examples 1.7, 2.5, 2.6, misconceptions, M1-M3, E1-E2, R1, lab named pairs)", "PASS",
    "Hand recomputation of I_X and I_Y at every support point of Example 2.5 (0,0,500,1000,2000 and 0,250,500,1250,2000) and Example 2.6; M1 and M2 values; lab named-pair integrated CDF lines (run output, pair B Y at 4000 = 500); E1 value 500 for Y at 4000. Script: ledgers/E3/scripts/E3-f-r14/check_L04_theorems.py (out/check_L04_theorems.out).")
row("E3f-r14-L04-theorems", "2.4-mathematics", "course/modules/E/E3/L04.html Theorem 1.5, Lemma 1.6, Proposition 1.8, Lemma 2.2, Theorem 2.3, Remark 2.4", "PASS",
    CMD + "check_L04_theorems.out: 400 random pairs on S; 0 proven FOSD or SOSD dominances refuted by sampled nondecreasing (concave) utilities; SOSD support-point verdict equals fine-grid verdict on all 36 equal-mean pairs. The four converse-sample cases were resolved by exact indicator witnesses (sampling artefact, not a counterexample).")
row("E3f-r14-L02-prop31-proof", "2.4-mathematics", "course/modules/E/E3/L02.html:199 (Proposition 3.1 proof, last sentence)", "FAIL",
    "Line 195 defines z(eps) = pi(eps)/eps^2 and line 197 writes the identity in z; line 199 then says 'Hence q(eps) -> (1/2) u''(w) s^2 / (-u'(w))'. q is not defined anywhere in L02 after the round-13 rename, so the last step of the proof names an undefined symbol. The limit itself is correct (checked by hand: r_A = -u''/u', and grep of L02 finds q(eps) only on line 199).",
    "In course/modules/E/E3/L02.html line 199 replace \\(q(\\varepsilon)\\) with \\(z(\\varepsilon)\\) (one occurrence). Nothing else in the proof changes.")
row("E3f-r14-L02-prop31-limit", "2.4-mathematics", "course/modules/E/E3/L02.html:173-199 (Proposition 3.1) and Remark 3.2", "PASS",
    "Re-derived: E u(W_eps) = u(w) + (1/2) eps^2 u''(w) s^2 + eps^2 upsilon(eps); u(w-pi) = u(w) - pi u'(w) + pi chi(pi); dividing gives z[chi - u'] = (1/2) u'' s^2 + upsilon; limit (1/2) r_A(w) s^2. Lab check of the limit is numerical only (Part B) and the page says so.")
row("E3f-r14-L01-proofs", "2.4-mathematics", "course/modules/E/E3/L01.html Propositions 2.2, 2.3, 3.1, 3.3 and Problems P1, P2, R1, R3", "PASS",
    "Each proof re-read and re-derived: non-negative weights sum to one; linearity by finite sum splitting; affine formula; sign of b in the ranking; maximum at a pure lottery on a utility-maximising outcome (R1); R3 values 25000 and 22500.")
row("E3f-r14-L02-proofs", "2.4-mathematics", "course/modules/E/E3/L02.html Proposition 1.1, 1.3 (a)(b), 2.2, Example 2.3, Problems P1-P3, R1-R3", "PASS",
    "Proofs re-derived (Taylor with Lagrange remainder, tangent-line bound, strictness under A4). Assumptions F1-F6 are named calculus facts; A4 is used where stated; Problem R3 proof checked.")
row("E3f-r14-L03-proofs", "2.4-mathematics", "course/modules/E/E3/L03.html Propositions 1.2, 1.4, 1.7, 2.4, 2.6, 2.7, Theorem 2.1, Remark 2.8, Problems R1, P1-P3", "PASS",
    "Re-derived: power identities; Prop 1.4 limit via (e^h-1)/h with A2; Prop 1.7 derivatives; Thm 2.1 via g(w)=ln u' + gamma ln w; Prop 2.4 closed form c^s = M; Prop 2.6 homogeneity; Prop 2.7; Remark 2.8 cent bound (k+1)/2 by triangle inequality; R1 limits for gamma>1 and 0<gamma<1.")
row("E3f-r14-L04-proofs", "2.4-mathematics", "course/modules/E/E3/L04.html Problems P1-P3, R1-R3 and Example 2.6", "PASS", "Each proof re-read; Lemma 2.2 piecewise-affine argument and the piecewise-linear representation in the proof of Theorem 2.3 checked.")
# notation rows
row("E3f-notation", "2.13-notation", "course/modules/E/E3/L01.html-L04.html vs notation/notation.json (macros and registered symbols)", "PASS",
    "grep: lessons use \\E, \\Prob, \\Var, \\R, \\indic only from the registry; no raw \\mathbb{E}; no T, \\Phi, gamma_3, R^*, R^{e*}, R_f or \\mathbb{Q} used with a registered meaning; \\R used for reals (L02 once, L04 six times).")
row("E3f-notation-kappa", "2.13-notation", "course/modules/E/E3/L02.html (M3, P1, quiz); cards.json", "PASS",
    "Round 14 grep: no kappa or kappa glyph in L01-L04 or cards.json. M3, P1 and quiz item q10 now use nu (L02.html lines 434-436, 445-447, 607-609); the round-12 clash with index and project is outside this slice.")
row("E3f-notation-alpha", "2.13-notation", "course/modules/E/E3/L01.html (Definition 2.1 and later uses); tests/labs/E3/lab-E3-L01-1.py; cards c005-c017", "PASS",
    "Round 14 grep: no alpha in L01.html, in the L01 twin, or in L01 cards. alpha is used in L02 F6 as a generic real exponent, which matches its use as the gains exponent in L06 (same meaning). The L01 mixture weight is now tau, which collides with another meaning: see E3f-r14-notation-tau.")
row("E3f-r14-notation-tau", "2.13-notation", "course/modules/E/E3/L01.html Definition 2.1 and Propositions 2.2-2.3 (tau used 50 times in L01), tests/labs/E3/lab-E3-L01-1.py, cards.json E3-c005, c007, c008, c017; collides with course/modules/E/E3/L08.html Definition 1.2 (tau = ambiguity weight, 37 uses) and cards.json E3-c137", "FAIL",
    "The letter tau has two meanings in one unit. L01 Definition 2.1 uses tau as a mixture probability weight in [0,1]; L08 Definition 1.2 uses tau as the alpha-MEU ambiguity weight, and L08 states 'The weight is written tau, not alpha'. BUILDER_RULES 2.1 item 7 and the plan's section 4 require a local letter to keep one meaning across the unit. The round-12 fix moved the L01 mixture from alpha to tau and created this clash.",
    "Choose one letter that appears nowhere in E3 (grep all course/modules/E/E3 pages and cards first) and use it for the L01 mixture weight in Definition 2.1, Propositions 2.2-2.3, P1, E2, the key-results row, the lab twin and cards E3-c005, c007, c008, c017; or rename the L08 ambiguity weight (Definition 1.2, cards E3-c137, and the L08 text that cites tau). Either way the two meanings must not share a letter.")
row("E3f-r14-notation-eps", "2.13-notation", "course/modules/E/E3/L02.html Section 3 (eps = scale of the wealth lottery, 91 uses) vs course/modules/E/E3/L05.html Definition 2.1 (eps = elasticity of intertemporal substitution, 3 uses; cards E3-c083)", "FAIL",
    "The letter varepsilon denotes a small scale of a gamble in L02 Section 3 (W_eps = w + eps X, Proposition 3.1, Remark 3.2, lab Part B) and the elasticity of intertemporal substitution in L05 Definition 2.1 (eps := d ln(c1/c0) / d ln MRS). One letter, two meanings, in one unit.",
    "Rename the EIS symbol in L05 Definition 2.1 and Proposition 2.2 (and card E3-c083) to a letter unused in E3 (for example psi-free 'sigma_EIS' or 'e_EIS'; grep first), or rename the L02 scale to a different letter. The round-14 verifier did not edit L05; the L05 slice verifier must confirm the chosen rename.")
row("E3f-r14-notation-eta", "2.13-notation", "course/modules/E/E3/L03.html Proposition 2.7 and proof (eta = additive constant of tilde u = phi u + eta; cards E3-c049) vs course/modules/E/E3/L07.html Example 1.4 and family omega_eta (eta = 1/2; 24 uses; cards E3-c121)", "FAIL",
    "eta is the additive constant of an affine transform of utility in L03 and a shape parameter of the weighting family omega_eta(p) = p^eta / (p^eta + (1-p)^eta)^(1/eta) in L07. One letter, two meanings in one unit.",
    "Rename the affine constant in L03 Proposition 2.7, its proof (L03.html line 174, 179, 393) and card E3-c049 to a letter unused in E3 (grep first), or rename the L07 weighting parameter in Example 1.4 and card E3-c121. The L07 slice verifier must confirm the L07 side.")
row("E3f-dag-L02-crra-forward-use", "2.9-define-before-use", "course/modules/E/E3/L02.html; L03.html; L04.html (concept links and forward uses)", "PASS",
    "check_dag E3 PASS. Read every lesson: each dfn is unique (expected-utility L01; certainty-equivalent, arrow-pratt-risk-aversion L02; crra-utility L03; first- and second-order-stochastic-dominance L04). Out-of-closure names (Jensen, martingale, quantile, Gaussian, Monte Carlo, Lebesgue) are absent; 'integral', 'derivative', 'variance' and 'convex' are closure or plain English. Forward references (Proposition 2.7 in L03 Definition 1.3; Problem R3 in L04 Remark 2.4) are cross-references to results, not concepts.")
row("E3f-dag-other-links", "2.9-define-before-use", "course/modules/E/E3/L01.html-L04.html (Uses and Introduces lines; concept links)", "PASS",
    "Links: random-variable and expectation (M4), derivative and variance (M4/M2), exponential-and-logarithm (M1, in closure), and earlier-lesson anchors L01.html#def-expected-utility, L02.html#def-arrow-pratt-risk-aversion, L02.html#def-certainty-equivalent, L03.html#def-crra-utility. No later-lesson definition is linked from an earlier lesson.")
row("E3f-banned-and-process", "1.3-1.4-banned", "course/modules/E/E3/L01.html-L04.html (visible prose)", "PASS",
    "Python scan (round 14): no TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly'; no process word (builder, verifier, round as a verification round, REQUESTS, unit report). The only ellipses are inside code blocks (Python type hints).")
row("E3f-banned-cards", "1.3-1.4-banned", "course/modules/E/E3/cards.json", "PASS", "Python scan of all 177 cards for the same banned strings and process words: none.")
row("E3f-hours", "2.12-hours", "course/modules/E/E3/L01.html..L04.html data-hours and eyebrows; index.html hub split", "PASS",
    "data-hours is 7 in each of L01-L04 (verified by regex); lessons sum to 28 in this slice; the full 8 x 7 = 56 with hub data-hours-lessons=56 and data-hours-project=14 is checked by check_pages PASS.")
row("E3f-references", "2.1-citations", "course/modules/E/E3/L02.html:616 (pratt1964risk); references/references.json", "PASS",
    "pratt1964risk record: Pratt, 'Risk Aversion in the Small and in the Large', Econometrica 32(1-2), 1964, doi 10.2307/1913738, status verified; verify_refs --unit E3 live re-resolution: 5 entries, 0 problems (out/verify_refs_unit_E3.out). L02 names the work for the name only, as its references paragraph says. The body of L02 cites no passage or result from it.")
row("E3f-L03-references", "2.1-citations", "course/modules/E/E3/L03.html:564 (references paragraph); course/modules/M/M1/L03.html Propositions 1.4, 1.6(b), A2, A3", "PASS",
    "Read M1 L03: Proposition 1.4 (logarithm inverts exponential), Proposition 1.6(b) (ln(ab)=ln a + ln b), A2 (addition rule), A3 (uniqueness of ln) exist with those numbers; M1 L03 line 63 says e is defined as e^1; no limit (e^h-1)/h is derived there (grep: no derivation), which matches L03 A2.")
row("E3f-delta", "0-delta", "git diff 329c1d7f..1431aa1d -- course/modules/E/E3 tests/labs/E3 notation plans/FINAL-ARCHITECT-RULINGS.md references/", "PASS",
    "Changed in this slice since round 12: L01.html (alpha to tau), L02.html (kappa to nu; q to z; Example 1.5 wording), cards.json (grade T on E3-c183; edits to E3-c005, c007, c008, c017, c125, c134, c142, c143, c154, c158; E3-c131 removed), tests/labs/E3/lab-E3-L01-1.py (tau), plans/FINAL-ARCHITECT-RULINGS.md (rulings 14-25 read; ruling 13 applied to grades), references/references.json (generated; one used_by added for FC2, not in this slice).")
row("E3f-E3-r7-independent-rederivation", "2.2-numbers", "ledgers/E3/scripts/E3-f-r14/*.py", "PASS",
    "Independent scripts this round: check_L01_L02_numbers.py, check_L03_numbers.py, check_L04_theorems.py, check_cards_numbers.py, check_twin_equality.py, check_cards_structure.py (outputs in out/).")
row("E3f-cards-integrity", "2.7-cards-integrity", "course/modules/E/E3/cards.json (177 cards)", "PASS",
    "check_cards_structure.py: 177 cards, 177 distinct ids, id format E3-cNNN, every card has id/lesson/front/back, cited keys all exist in references.json (none missing). Missing numbers in the id sequence (c042, c069, c092, c097, c114, c115, c131, c156, c176, c186) are allowed by architect ruling 2; c131 was removed after round 12.")
row("E3f-cards-near-duplicates", "2.7-cards-duplicates", "course/modules/E/E3/cards.json (full pairwise scan)", "PASS",
    CMD + "check_cards_structure.out: 14 pairs have a front or back similarity above 0.8, all distinct facts on reading (e.g. c047 vs c180 differ in gamma 2 vs gamma 1; c144 vs c182 red vs black; c174/c175 different assumptions). No duplicate card.")
row("E3f-cards-xrefs", "2.7-cards", "course/modules/E/E3/cards.json (Definition, Proposition, Example, Remark, Problem and Assumption locators)", "PASS",
    CMD + "check_cards_structure.out: every locator resolves in its own lesson, except 'Problem E2' in L03 (card E3-c055) and L07 (card E3-c187), which are headed 'E2 ·' in the lessons, and that is the same item.")
row("E3f-banned-cards-cite", "2.7-cards", "cards.json cite keys (E3-c134, c157, c158)", "PASS", "Each cited key exists in references.json; c157 names only the registry title (matches record 'Risk, Ambiguity, and the Savage Axioms').")
row("E3f-cards-grades", "2.7-cards-grades", "course/modules/E/E3/cards.json E3-c106 (grade C, basis 'Lab 1, exact fractions on one gamble; Example 2.3') vs course/modules/E/E3/L06.html Example 2.3", "FAIL",
    "Ruling 13 (plans/FINAL-ARCHITECT-RULINGS.md item 13): a value the page derives by hand in a numbered Example is graded T with the Example as basis, even when a lab also prints it. L06 Example 2.3 derives 200 cents at lambda=1, 50 at 3/2 and -100 at 2 by hand (W = 500 - 300 lambda) and lambda* = 5/3. E3-c106 says C. Round-14 sweep: E3-c183 is now T (the round-12 row is resolved); the other C cards in L01-L04 (c016, c017, c032, c033, c035, c054, c073, c075, c076, c160, c161, c171) are lab-output cards whose basis names the lab (accepted); c034 (11.17 percent) is kept C with basis Lab 1, part A because its inputs are the lab-printed premium pair and the page derives the share only in Section 4 prose, not in a numbered Example (judgement, recorded here); the 40 ungraded cards are definitions, assumptions or remarks (no graded result).",
    "In course/modules/E/E3/cards.json, change E3-c106 to \"grade\": \"T\" and \"basis\": \"Example 2.3\" (or delete basis and state the Example in the back). Then check the matching key-results row in L06.html against it (outside this slice).")
row("E3f-E3-c183", "2.7-cards-grades", "course/modules/E/E3/cards.json (E3-c183) mirrored by course/modules/E/E3/L04.html key-results row (Examples 1.7, 2.5, 2.6)", "PASS",
    "Round-12 FAIL resolved: cards.json E3-c183 now carries \"grade\": \"T\"; L04.html row 'The named pairs of Examples 1.7, 2.5 and 2.6' is T with 'Computed by hand in the examples'. Second-order ranking of Example 2.6 re-derived: I_Y(t) = (t-3000)^+ <= I_X(t) at 1000, 3000, 5000.")
row("E3f-cards-numbers", "2.2-numbers", "course/modules/E/E3/cards.json (numbers in card backs, all lessons)", "PASS",
    "ledgers/E3/scripts/E3-f-r14/check_cards_numbers.py (out/check_cards_numbers.out) recomputes card numbers: omega values, ratio 0.73045450 and thresholds 2/3 and 0.58578644 (c123, c125); 49.8328 (c132); Gamma values 42.8686, 39.1251, 4.8788, 3.9125 and difference 3.7436 unrounded (c127, c187); 0.278 grid crossing (c122); 4180000/41 = 101951.2195 and premium 548.7805 (c149, c152); maxmin 99523.8095 (c151); prospect values -2.071068 and -107.2330 and 99892.7670 (c150, c166); lambda_R = sqrt(2)/2 (c113); threshold sqrt(5/3) and W = -8.6835 (c116); CE1 2.25, 1.6, 1.3720 (c096); V0 4.0000, 4.3311 and U -0.25, -0.55 (c095); U = -49/80 and CE1 = 8/5 (c169, c170); MRS 4/9 (c184).")
row("E3f-cards-slice-scan", "2.7-cards", "course/modules/E/E3/cards.json, all 90 cards of L01-L04 (ids E3-c001..E3-c077, c159-c183 subset)", "PASS",
    "Full read of every L01-L04 card against its lesson text and the cited locator (Definition, Proposition, Example, Remark, Problem, misconception section). Every card is atomic and matches the current lesson text; no card contradicts the lab output it quotes. Per-card rows follow.")
row("E3f-coverage-cards", "2.7-cards-coverage", "course/modules/E/E3/L01.html-L04.html (labelled Definition, Proposition, Theorem, Lemma, Remark, Example blocks)", "PASS",
    "Python check (round 14): every labelled Definition, Proposition, Theorem, Lemma and Remark block in L01-L04 appears in some card's front, back or basis, except L01 Example 3.4, which is a worked example, not one of the card kinds in BUILDER_RULES 7 (its misconception 1 is carded by E3-c014 and E3-c015). Assumptions are named and carded where a card asks for them (E3-c004, c018, c174, c175).")
# per-card rows for L01-L04 (full read)
round12_ids = {"E3f-E3-c%03d" % i for i in range(1, 200)}
for c in cards:
    if c["lesson"] not in ("L01", "L02", "L03", "L04"):
        continue
    cid = c["id"]
    rid = "E3f-E3-" + cid.split("-")[1]
    if cid in ("E3-c106", "E3-c183"):
        continue
    status = "PASS"
    loc = f"course/modules/E/E3/cards.json ({cid}); course/modules/E/E3/{c['lesson']}.html"
    row(rid, "2.7-cards", loc, status,
        f"Round 14 full read of {cid} against {c['lesson']}.html; front/back checked for the cited definition, proposition, example, remark or problem; numbers in the back recomputed where present (see E3f-cards-numbers).")
row("E3f-r14-cards-sample-L05", "2.7-cards-sample", "course/modules/E/E3/cards.json E3-c078, c084, c085, c086, c087, c089, c091, c094, c095, c169, c170, c184, c185 vs course/modules/E/E3/L05.html", "PASS",
    CMD + "check_cards_numbers.out and check_cards_structure.out: definitions (Definition 1.1 EZ value), Proposition 2.2 (EIS = psi), Theorem 3.2 (power transform when psi = 1/gamma), the restriction to the deterministic plan, and the lab outputs quoted (EIS 0.5/2/0.25; U and V0 pairs; CE1 values; 80/49; 8/5; -49/80) all match the lesson text and recomputation. 13 of 22 L05 cards sampled.")
row("E3f-r14-cards-sample-L06", "2.7-cards-sample", "cards.json E3-c101, c102, c104, c105, c107, c108, c110, c111, c112, c113, c116, c117 vs L06.html", "PASS",
    "Numbers recomputed (check_cards_numbers.out): c104 lambda* = pg/((1-p)l) and W(lambda); c105 power threshold; c108 700-300 lambda and 2(500-300 lambda); c111 (1/2)800^alpha(1-lambda); c113 lambda_R = sqrt(2)/2 (computed); c116 threshold 1.2910 and W = -8.6835; c117 grid checks match the printed lab lines. c106 is covered by E3f-cards-grades (FAIL).")
row("E3f-r14-cards-sample-L07", "2.7-cards-sample", "cards.json E3-c121, c122, c123, c124, c125, c126, c127, c128, c132, c133, c135, c187 vs L07.html", "PASS",
    "Numbers recomputed (check_cards_numbers.out): omega values 0.28579088, 0.39125077, 0.35355339; 2 omega(3/10) = 0.57158177; ratio 0.73045450; thresholds 2/3 and 0.58578644; Gamma(A) 42.8686 and Gamma(B) 39.1251 at alpha = 1 (unrounded difference 3.7435573, prints 3.7436); alpha = 0.5 values 4.8788 and 3.9125; 49.8328; grid crossing between 0.278 and 0.279. Card E3-c121 is subject to E3f-r14-notation-eta.")
row("E3f-r14-cards-sample-L08", "2.7-cards-sample", "cards.json E3-c137, c138, c139, c141, c142, c143, c144, c148, c149, c150, c151, c152, c153, c155, c164, c165, c166, c172, c179, c182 vs L08.html", "PASS",
    "Numbers recomputed (check_cards_numbers.out and exact fractions): 4180000/41 = 101951.2195; premium 548.7805; maxmin 99523.8095 at P(red) = 1/3; prospect -2.071068 and CE change -107.2330 with wealth 99892.7670; 103125 (red) and 106451.6129 (black) from 1/((1/3)/110000 + (2/3)/100000) and 1/((2/3)/110000 + (1/3)/100000); Definitions 1.2 and Proposition 1.3 and Example 1.4 (k = 30..60, average 1/2) and Theorem 2.2 hypotheses match. Card E3-c137 uses tau: see E3f-r14-notation-tau.")
row("E3f-r14-cards-unsampled", "2.7-cards-sample", "cards.json L05-L08 cards not listed in the samples above (29 cards)", "UNVERIFIABLE",
    "Not read line by line against lessons L05-L08 in this round; sampling per VERIFIER_RULES 2.7 covered 58 of the 87 L05-L08 cards (13 L05, 12 L06 plus c106, 12 L07, 20 L08). The other 29 cards were checked only for structure, duplicates, keys and locators.",
    "A slice verifier of L05-L08 (slice g and the L05-L08 owners) must read every card in that range against its lesson before this unit passes; or extend this slice's sample.")
print(len(rows))
out = {
    "unit": "E3", "slice": "f", "round": 14,
    "verifier": "Claude Haiku 5.5, independent verifier for E3-f, round 14 (did not build E3)",
    "pin": "1431aa1d842a5d2d05fd5953c098500bf78a4307",
    "base": "329c1d7f (round-12 pin; the round-13 fragment D-E3-f.round13.json is absent from /Users/billyribeiro/.fanout/frags, so round 12 is the context)",
    "checkout": ROOT,
    "scratch": SCR + "/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice scope: L01-L04 pages and their lab twins, and all cards in course/modules/E/E3/cards.json (177 cards; the task text said 178; round 12 counted 178 before card E3-c131 was removed).",
        "No project grader is in this slice, so the mutation and five-alternative rules do not apply; mutants is empty by design. Lab twins are demonstrations (ruling for project graders only).",
        "Round 13 fragment was absent; every round-12 FAIL row was re-verified: E3f-notation-kappa PASS, E3f-notation-alpha PASS (but see E3f-r14-notation-tau), E3f-E3-c183 PASS, E3f-cards-grades FAIL (c106 now).",
        "Wider-unit notation collisions found from L01-L04 letters: tau (L01 vs L08), varepsilon (L02 vs L05), eta (L03 vs L07). Each is a FAIL row here because the same letter keeps one meaning across the unit (BUILDER_RULES 2.1 item 7).",
        "Gate runs: check_pages, check_dag, check_projects, run_labs L01-L04, ruff, mypy, verify_refs (offline and live E3), build_site --check, render_curriculum (no diff), pytest for E3 and docs, page_smoke L01-L04: all PASS. Generated files unchanged (git status clean).",
        "Not checked: the hub, project and L05-L08 lesson text in full (other slices); the 52 sampled L05-L08 cards are a sample; Pratt's paper itself was not read (only the registry record and Crossref re-resolution); the Lab 1 output of L04 was checked by an independent randomized script, not by reading the 400-pair data.",
    ],
    "summary": {},
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
out["summary"] = {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"]}
json.dump(out, open(f"{ROOT}/ledgers/E3/E3-f.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(out["summary"])
print(ledger.validate(out, "E3-f"))
