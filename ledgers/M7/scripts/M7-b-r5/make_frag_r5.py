"""Build ledgers/M7/M7-b.json (round 5, slice M7-b) from the round-4 rows plus round-5 decisions.
Carried rows keep their round-4 id and check; their evidence carries the round-4 text behind a prefix."""
import json, pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
r4 = json.loads(pathlib.Path("/tmp/fanout-frags/B-M7-b.round4.json").read_text(encoding="utf-8"))
CARRY = "Carried from round 4 (cited lines outside every hunk of git diff 2657ab5..09b8751; the files themselves changed, so the carry is per cited line range): "
REVERIFY = "Re-verified in round 5 on pin 09b8751: "
FAIL_PENDING = {}
# round-5 status overrides: id -> (status, location, evidence, fix)
OVR = {
 "M7b-dag-prose-terms": ("FAIL", "L06.html:7, 60, 412; cards.json M7-c097 back",
   REVERIFY + "link check PASS (check_dag M7). Prose 'variance' still used for w'Sigma w outside the closure: L06.html:7 (meta description 'why the variance falls'), L06.html:60 (Definition 1.1 'this form is the portfolio variance of the return'), L06.html:412 ('which is the portfolio variance only under the covariance hypothesis'), cards.json M7-c097 back ('the quadratic term is the portfolio variance'). Plan section 2 lists variance as outside the closure (M7 closure = P0.1, M1, M2, M3). Efficient frontier and convexity prose pass (plan section 2 rows). Details: M7b-r5-L06-meta-variance, M7b-r4-L06-variance-term.",
   "Replace the residual 'variance' prose for w'Sigma w with 'risk term' (L06.html:7, 60, 412; cards M7-c097 back), or drop the conditional identity."),
 "M7b-cards-L06-c097-c108": ("FAIL", "cards.json M7-c097, M7-c099, M7-c102; L06.html:56, 60, 412",
   REVERIFY + "cards.json M7-c102 and M7-c110 now match the lesson (risk term). M7-c097 back (cards.json line 621) says 'the quadratic term is the portfolio variance only under that hypothesis' and uses 'covariance matrix'; M7-c099 back (line 635) repeats the covariance disclaimer. See M7b-r5-covariance-scope (plan B1 allows 'covariance' only in the disclaimer sentence L06.html:56).",
   "Rewrite the M7-c097 back without 'covariance' and 'variance' (say the unit takes Sigma as an input and does not identify w'Sigma w with a risk measure); drop the restated disclaimer from M7-c099 or cite L06.html:56 only."),
 "M7b-r4-L06-variance-term": ("FAIL", "L06.html:7, 60, 412; cards.json M7-c097 back",
   REVERIFY + "Fixed in round 5 at L06.html:52, 90, 150, 405, 424, 549, 586 and lab header line 313 (names changed to 'risk term'; grep shows no 'variance' for w'Sigma w there). Still open: L06.html:7 (meta description, not in the round-4 list), L06.html:60 and 412 (conditional 'portfolio variance' remarks), cards.json M7-c097 back. Proposition 2.1 proof is unaffected (T grade stands).",
   "Use 'risk term' in L06.html:7, 60, 412 and cards.json M7-c097 back, as already done elsewhere on the page."),
 "M7b-cards-duplicates": ("FAIL", "cards.json: M7-c058/M7-c069, M7-c059/M7-c071",
   REVERIFY + "Pairs with the same locator and the same claim are still present: M7-c058 ('g <= p*, hence d* <= p*', Prop 1.3) and M7-c069 (L04.html:287 'weak duality gives only d* <= p*'); M7-c059 (Prop 1.4 bound) and M7-c071 (L04.html:295 zero grid gap forces zero true gap). M7-c082/M7-c092 pair is resolved (M7-c092 now tests Theorem 3.1 complementary slackness).",
   "Remove or reword one card of each duplicate pair (M7-c069 and M7-c071 against M7-c058 and M7-c059) and rebuild cards.json."),
 "M7b-cards-L04-c056-c065": ("PASS", "cards.json M7-c056..c065; L04.html:55-268, 254-256",
   REVERIFY + "M7-c061 now names the minimiser x-hat (cards.json line 399) matching L04.html:107. Other cards c056-c060, c062-c065 agree with the page; the duplicate pairs are a separate row (M7b-cards-duplicates).", None),
 "M7b-cards-L05-c073-c084": ("PASS", "cards.json M7-c073..c084; L05.html:58-172",
   REVERIFY + "M7-c079 now uses x-hat (line 512) matching Theorem 2.3 (L05.html:115); M7-c083 (line 540) now states the Theorem 2.3 hypothesis (Q SPD, rows of A and G_i for i in S independent), matching Definition 3.3 (L05.html:156) and Theorem 2.3 (L05.html:114-115). Other cards agree.", None),
 "M7b-cards-L05-c085-c096": ("PASS", "cards.json M7-c085..c093; L05.html:128-180, 390-496",
   REVERIFY + "M7-c086 (line 561) uses x-bar and mu-bar matching Example 3.6 at L05.html:176; M7-c092 (line 606) now states Theorem 3.1 with mu-bar >= 0 and complementary slackness (L05.html:141) and cites Remark 3.2 (L05.html:150); M7-c093 (line 613) uses x-hat matching L05.html:420. Lab values (multiplier -36/19, 11/19) match the printed lab output.", None),
 "M7b-cards-L06-c109-c120": ("PASS", "cards.json M7-c108..c118; L06.html:404-430, 552",
   REVERIFY + "M7-c110 (lines 713-714) now says 'risk term' with 0.123809, matching the lab Part A row (lab-M7-L06-1 output). Values 0.5722548, 0.558861, zero set {A4} recomputed in ledgers/M7/scripts/M7-b-r5/indep_r5.py.", None),
 "M7b-r3-L05-def33-theorem23-hypothesis": ("PASS", "L05.html:156; Theorem 2.3 at L05.html:114-115; cards.json M7-c083",
   REVERIFY + "L05.html:156 now reads 'Theorem 2.3 identifies it when Q is symmetric positive definite and the rows of A and of G_i for i in S are linearly independent'. That is Theorem 2.3's hypothesis applied to the stacked constraint matrix [A; G_S] (full row rank), so the sentence is correct. Card M7-c083 matches it.", None),
 "M7b-r4-card-c092-CS": ("PASS", "cards.json M7-c092; L05.html:141",
   REVERIFY + "cards.json line 606 now states complementary slackness and mu-bar >= 0 (Theorem 3.1, L05.html:141) and cites Remark 3.2 (L05.html:150). Hypothesis now complete.", None),
 "M7b-r4-L05-E3-PD": ("PASS", "L05.html:499, 372 (old 496, 369); tests/labs/M7/lab-M7-L05-1.py:72-83, 102 (old 255-261 for the embedded copy is now 258-264)",
   REVERIFY + "L05.html:499 (E3) now says the printed line is an exact leading-minor test for this Q and that Remark 2.4 proves positive definiteness by completing the square. Recomputed: leading minors of Q_A = [[4,1,0],[1,3,1],[0,1,2]] are 4, 11, 18 (all positive), and the completing-the-square identity of Remark 2.4 expands to 4x1^2+3x2^2+2x3^2+2x1x2+2x2x3 (checked by hand). Lab prints q_positive_definite True (lab output).", None),
 "M7b-r4-L05-references-one-instance": ("PASS", "L05.html:630 (old 627); tests/labs/M7/lab-M7-L05-1.py:24-28, 37 (Q_A, Q_B)",
   REVERIFY + "L05.html:627 now reads 'Lab 1 checks two small instances in exact arithmetic: Part A has three variables and Part B has two.' Part A Q_A is 3x3 (twin line 24-28) and Part B Q_B is 2x2 (line 37). Matches L05.html:183 and 390.", None),
 "M7b-r4-cards-xstar": ("PASS", "cards.json M7-c061, M7-c079, M7-c086, M7-c093; L04.html:107, L05.html:115, 176, 420",
   REVERIFY + "Each card now uses the notation of its lesson: M7-c061 x-hat (L04.html:107), M7-c079 x-hat (L05.html:115), M7-c086 x-bar (L05.html:176), M7-c093 x-hat (L05.html:420). grep finds no residual x* on cards M7-c056..c120 or on L04-L06 pages.", None),
 "M7b-r3-L06-def11-variance-identity": ("PASS", "L06.html:60",
   CARRY + "L06.html:60 is byte-identical to the previous pin (outside every hunk). The conditional identity 'If Sigma is the covariance matrix ... this form is the portfolio variance' is correct as written. The remaining prose-use residual is tracked in M7b-r4-L06-variance-term and M7b-r5-covariance-scope.", None),
}
CARRIED_PASS = ["M7b-L04-prop32", "M7b-L04-quiz-hypotheses", "M7b-L04-causal", "M7b-L04-term-before-definition",
  "M7b-L05-lemma14", "M7b-L06-partD-true",
  "M7b-L06-R1-unproved", "M7b-r3-L01-convexity-definition", "M7b-r3-L05-remark24-decomposition",
  "M7b-r3-L06-prop34-no-sign", "M7b-2.2-numbers-L04", "M7b-2.3-grades-L04",
  "M7b-2.4-L04-proofs", "M7b-2.5-L04-misc", "M7b-L05-prop34-step", ]
REV_PASS = {
 "M7b-cmd-check-pages": "`.venv/bin/python tools/check_pages.py --unit M7 --page L04` (and L05, L06): 'check_pages M7 L04: PASS', 'L05: PASS', 'L06: PASS' on pin 09b8751. Banned-string scan included.",
 "M7b-cmd-check-dag": "`.venv/bin/python tools/check_dag.py --unit M7`: 'check_dag M7: PASS'.",
 "M7b-cmd-run-labs": "`.venv/bin/python tools/run_labs.py --unit M7 --page L04|L05|L06`: 'run_labs M7: PASS (1/1)' three times.",
 "M7b-lab-L04-twin-run": "`.venv/bin/python -I -W error tests/labs/M7/lab-M7-L04-1.py` exit 0; `ledgers/M7/scripts/M7-b-r5/embed_compare.py` (copy of the round-4 script): 'L04 code == twin: True', 'L04 expected == run output: True'.",
 "M7b-lab-L05-twin-run": "`-I -W error` run of lab-M7-L05-1.py exit 0; embed_compare: code == twin True, expected == run output True (output saved at /tmp/M7-v/b5/lab-L05-1.out, which the L05 page block matches).",
 "M7b-lab-L06-twin-run": "`-I -W error` run of lab-M7-L06-1.py exit 0; embed_compare: code == twin True, expected == run output True.",
 "M7b-lab-lint-types": "`.venv/bin/ruff check tests/labs/M7` -> 'All checks passed!'; `ruff format --check tests/labs/M7` -> '11 files already formatted'; `.venv/bin/mypy --no-incremental tests/labs/M7` -> 'Success: no issues found in 11 source files'.",
 "M7b-lab-pytest": "`.venv/bin/pytest -q tests/test_labs.py -k M7` -> 11 tests, '[100%]'.",
 "M7b-smoke": "`.venv/bin/python tools/page_smoke.py --unit M7 --pages L04 L05 L06` -> 'page_smoke modules/M/M7/L06.html: PASS', 'page_smoke M7: PASS'.",
 "M7b-refs-live": "`.venv/bin/python tools/verify_refs.py --unit M7` -> 'live re-verification of M7: 2 of 560 entries, 0 problems'; `--offline` -> 'offline integrity: 560 entries, 0 problems'. The slice cites no key (L05.html:627 'cites no outside source').",
 "M7b-citation-boyd-attribution": "`grep -ci boyd` on L04.html, L05.html, L06.html, cards.json -> 0 each.",
 "M7b-2.2-numbers-L05": "Re-derived with Fraction arithmetic: Part A objective 551/722 = 0.7631578947 (matches lab 'objective 0.7631578947'); Part B objective -9/4 and mu_hat (0, 5/2) (L05.html:387-389 block); leading minors 4, 11, 18. Other L05 numbers unchanged (outside hunks).",
 "M7b-2.2-numbers-L06": "ledgers/M7/scripts/M7-b-r5/indep_r5.py (own Fraction solver, sigma read from the lab generator): eq16 objective 0.8200021338530642, nn16 objective 1.3922569654003556, difference 0.5722548315472913 (printed-values difference 0.572255). Weights at gamma=16 0.425603..-0.409145 and nn 0.389418, 0.224792, 0.385790, 0 reproduce the page. Risk term nn16 0.184631 matches L06.html:588.",
 "M7b-2.2-misc-numbers": "L06.html:405 (risk column 0.123809 -> 0.115780, return 0.113798 -> 0.106241, turnover 0.558861), 428 (weights 0.434783 -> 0.388425 etc.), 454 (w'Sigma w = 1 with Sigma = 2I, f = 17/40), 504 (0.572255), 511, all match the lab output and indep_r5.py. L05.html:393, 485 match output (old 390, 482).",
 "M7b-2.3-grades-L06": "L06.html:548-552 key-results grades: Theorem 1.3 T, Proposition 2.1 T (proof at L06.html:91-103 re-read: the two minimality inequalities give (g1-g2)/2 (V1-V2) <= 0 and R2 >= R1), Proposition 2.3 T (inclusion of feasible sets), Proposition 3.4 T.",
 "M7b-2.4-L05-proofs": "L05.html Theorem 2.3 proof (Lemma 1.3, first block row), Theorem 3.1 proof (Lemma 1.4, complementary slackness), Remark 2.4 completing-square identity and Remark 3.2 example re-read and re-checked by hand. Unchanged proofs (Lemma 1.3/1.4, Proposition 2.1) carried.",
 "M7b-2.4-L06-proofs": "L06.html Theorem 1.3 (KKT solve, lambda formula, 1'b = b'Sigma b > 0), Proposition 2.1 (re-read), Proposition 2.3 (inclusion of feasible sets), and the Section 3 proofs (unchanged) re-read.",
 "M7b-2.4-quiz": "Quiz numeric keys re-read against the outputs: L05 objective_hat -9/4 (explain line 591), L06 0.184631 (line 588), and L06 difference 0.572255 (line 504). Other keys unchanged.",
 "M7b-2.9-structure": "check_pages M7 L04/L05/L06 PASS (structure check); section order unchanged (hunks changed text only).",
 "M7b-2.9-banned": "check_pages banned-string scan PASS on L04, L05, L06 (command above).",
 "M7b-2.9-process-words": "`grep -n -i -w -E 'build|builder|verifier|round|requests?|unit report'` on L04.html, L05.html, L06.html, cards.json -> no matches.",
 "M7b-hours": "data-hours L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10: sum 77. index.html data-hours-lessons=\"77\", data-hours-project=\"33\", total 110 (= 77 + 33). index.html:141 'Lessons 1, 2, 7 declare 9 hours and the others 10 hours' is consistent with these values. (Pace not checked, architect ruling.)",
 "M7b-L04-lab-numbering": "grep -c 'Lab 2' on L04.html, L05.html, L06.html -> 0 each.",
 "M7b-L05-why-xref": "L05.html:52 cites Proposition 3.4 for the midpoint result; Proposition 3.4 (L05.html:161) is 'Q SPD and F midpoint convex, then at most one minimiser', matching the sentence.",
 "M7b-L05-why-scope": "L05.html:52 re-read: 'Lab 1 solves a three-variable equality problem ... Lesson 6 applies the problem to mean-variance portfolio choice.' Forward pointer to L06, not a use before definition.",
 "M7b-L06-why-scope": "L06.html:52 re-read: 'a quadratic risk term, a linear reward for return, and linear constraints'; 'a sum of absolute values' is the turnover description (Definition 3.2 at L06.html:124-125). Matches Lab 1 description.",
 "M7b-L06-partB-count": "L06.html:150 and 168-170: 15 zero sets, lab output 'nonneg' rows show 1 candidate passing per gamma and 15 sets enumerated (2^4 - 1 = 15 sets leave an asset free).",
 "M7b-L06-misc2": "L06.html:427-428 weights at gamma=1 (0.434783 to 0.388425, 0.526836 to 0.203679, 0.562535 to 0.407895, -0.524154 to 0) match lab output lines; 'the weights of A1 to A3 all change' checked by these numbers.",
 "M7b-L06-covariance-docstring": "L06.html:56 is the only page sentence allowed to say 'covariance' under plan B1; the lab docstring (twin lines 1-30) contains no 'covariance'. Sentence re-read and matches.",
 "M7b-L06-term-before-definition": "L06.html:52 re-read: the term 'turnover' not used before Definition 3.2; 'a sum of absolute values' precedes it (L06.html:124-125).",
 "M7b-L06-lab-claims-ok": "L06.html:405 interpretation sentence by sentence against lab output (return and risk columns, A4 negative at all five gammas, zero set {A4}, 0.558861, 20 of 20). Matches.",
 "M7b-r3-lab-hypothesis-vs-output": "L06.html:150 predictions (budget exact, 15 sets, one passing candidate per gamma, risk nonincreasing, objective at least equality) all match lab output. L04.html:126, 249 and L05.html:183, 390 match output.",
 "M7b-r3-notation": "No registered symbol changed meaning. L06 uses 'risk term w^T Sigma w' and V(gamma); the registered Sigma and mu are unchanged. L04 changed only 'a fractions.Fraction'.",
 "M7b-r3-L06-def31-scope": "L06.html:120 re-read: 'Section 1 and Part A of Lab 1 use the budget constraint alone. Proposition 2.3 and Part B of Lab 1 add the nonnegativity constraint. The sector constraint is defined here and not used on this page.' 'sector' occurs only at L06.html:120 (grep).",
}

REV_PASS.update({
 "M7b-cards-L04-c066-c072": "cards.json M7-c067..c071 read against L04.html:259-295; M7-c069 (line 449) re-read against L04.html:287 and the lab output (line 11 'dual value at lambda = (0, 0), nu = 0 (no multipliers): -199/300'); -1/2 - (-199/300) = 49/300 (exact). Other cards unchanged.",
 "M7b-2.2-numbers-L05": "L05 numbers rechecked: Part A objective 551/722 = 0.7631578947 (from x=(13,3,3)/19 and c=(-1,0,2); lab prints 0.7631578947), det K = 19 (L05.html:393 block), lambda = (-36/19, 11/19); Part B objective -9/4 and mu-bar (0, 5/2) (L05.html:387-389 output block). The L05 page moved lines >= 257 by +3 (docstring insertion at L05.html:256); the cited lines are the same content at the shifted numbers (L05.html:156, 175-179, 393, 401-402, 442, 465-499).",
 "M7b-L05-misc3": "L05.html:420 (old 417) re-read: 'With Ax = b, the gradient at the minimiser is -A'lambda*, ... zero exactly when lambda* = 0, because A has full row rank. In Remark 2.4 the multipliers are (-36/19, 11/19), which Lab 1 prints'. Matches lab output line 'lambda -36/19 11/19'.",
 "M7b-L05-lab-variables": "L05.html:393 (old 390) re-read: 'three variables in Part A and two in Part B, examines four candidate sets, and says nothing about larger problems.' Part A Q_A 3x3 and Part B Q_B 2x2 (twin lines 24-28, 37); four candidate sets printed (lab lines 'candidate {} ...' to '{1,2}').",
 "M7b-r3-lab-hypothesis-vs-output": "L04.html:126, 249; L05.html:183 (prediction: one passing set, grid 33 x 33 on [0,2]^2, nonzero KKT determinant, residuals exact zero) and L05.html:393 (old 390) match lab output (passing_candidates 1, grid_points 1089, grid_points_below_candidate 0, determinant 19). L06.html:150 predictions match lab output (see M7b-L06-partB-count).",
 "M7b-2.4-quiz": "Quiz numeric keys re-read against the outputs: L05 explain line 591 (old 588) prints objective_hat -9/4; L06 0.184631 (line 588); L06 difference 0.572255 (line 504). Other keys unchanged.",
 "M7b-footer-L05-L06": "L05.html:630 (old 627) re-read: 'Lab 1 checks two small instances in exact arithmetic: Part A has three variables and Part B has two. It does not establish any fact about data, markets or the performance of any solver.' Matches twin. L05 footer at 641 is the same content shifted +3 (old 638). L06.html:646 and 657 unchanged (no net line shift in L06).",
})
CARRIED_PASS += ["M7b-L05-canon-heading", "M7b-2.3-grades-L05"]


LOC_NEW = {
 "M7b-L05-canon-heading": "course/modules/M/M7/L05.html:399 (old 396; L05 lines >= 257 shifted +3 by the docstring insertion at L05.html:256)",
 "M7b-2.3-grades-L05": "course/modules/M/M7/L05.html:530-545 (key results; old 527-542)",
 "M7b-2.2-numbers-L05": "course/modules/M/M7/L05.html:156, 175-179, 393, 401-402, 442, 465-499 (old 390, 398-399, 439, 462-496); ledgers/M7/scripts/M7-b-r3/num_L05_indep.py",
 "M7b-2.4-quiz": "course/modules/M/M7/L04.html:423-506; L05.html:547-626 (old 544-623); L06.html:558-641",
 "M7b-r3-lab-hypothesis-vs-output": "course/modules/M/M7/L04.html:126, 249; L05.html:183, 393 (old 390); tests/labs/M7/lab-M7-L04-1.py docstring; lab-M7-L05-1.py docstring",
 "M7b-L05-lab-variables": "course/modules/M/M7/L05.html:393 (old 390)",
 "M7b-L05-misc3": "course/modules/M/M7/L05.html:420 (old 417)",
 "M7b-footer-L05-L06": "course/modules/M/M7/L05.html:630, 641 (old 627, 638); L06.html:646, 657; L04.html footer",
 "M7b-2.2-misc-numbers": "course/modules/M/M7/L06.html:405, 414, 428, 504, 511; L05.html:393, 485 (old 390, 482); L04.html:287, 291",
 "M7b-r4-L05-references-one-instance": "course/modules/M/M7/L05.html:630 (old 627); tests/labs/M7/lab-M7-L05-1.py:24-28, 37",
}

rows = []
for r in r4["rows"]:
    rid = r["id"]
    if rid in OVR:
        st, loc, ev, fix = OVR[rid]
        row = {"id": rid, "check": r["check"], "location": loc, "status": st, "evidence": ev}
    elif rid in CARRIED_PASS:
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": CARRY + r["evidence"][:500]}
    elif rid in REV_PASS:
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": REVERIFY + REV_PASS[rid]}
    else:
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
               "evidence": CARRY + r["evidence"][:500]}
    if rid in LOC_NEW:
        row["location"] = LOC_NEW[rid]
    if row["status"] != "PASS":
        row["fix"] = OVR[rid][3]
    rows.append(row)
NEW = [
 {"id": "M7b-r5-L06-meta-variance", "check": "Page-level prose uses the M4-outside word 'variance' for w'Sigma w; the meta description must agree with Proposition 2.1 (risk term)",
  "location": "course/modules/M/M7/L06.html:7 (meta description)", "status": "FAIL",
  "evidence": REVERIFY + "L06.html:7: 'why the variance falls and the return falls as the risk-aversion parameter rises'. Proposition 2.1 (L06.html:90) is now titled 'the risk term and the return do not rise'; the page text uses 'risk term' everywhere else. The meta description is learner-visible and still uses the overstated word.",
  "fix": "Change L06.html:7 to 'why the risk term does not rise and the return does not rise as the risk-aversion parameter rises', then run check_pages M7 --page L06."},
 {"id": "M7b-r5-covariance-scope", "check": "Plan B1 (plans/M7-build-plan.md:75-76): 'covariance' may appear in prose only in the L06.html:56 disclaimer sentence, with no link",
  "location": "course/modules/M/M7/L06.html:60, 412; course/modules/M/M7/cards.json M7-c097 back (line 621), M7-c099 back (line 635)", "status": "FAIL",
  "evidence": REVERIFY + "grep -i covariance on the slice: L06.html:56 (the disclaimer, allowed), L06.html:60 ('If Sigma is the covariance matrix of the one-period returns'), L06.html:412 ('only under the covariance hypothesis of Definition 1.1'), cards.json line 621 (M7-c097 back, 'does not check that Sigma is a covariance matrix'), cards.json line 635 (M7-c099 back, 'estimating a covariance matrix is outside M7'). Four uses beyond the one sentence the Architect decision allows.",
  "fix": "Remove 'covariance' from L06.html:60 and 412 and from cards M7-c097 and M7-c099 (state that the unit takes Sigma as an input and does not identify w'Sigma w with any risk measure), or record an architect decision that widens the B1 allowance; then rebuild cards.json and re-run check_pages M7."},
]
rows += NEW
pinned = "09b8751"
frag = {
 "unit": "M7", "slice": "M7-b", "round": 5,
 "verifier": "round-5 independent verifier for slice M7-b (L04 to L06 and their lab twins); did not build M7 and shares no context with its builders",
 "pin": pinned, "base": "2657ab5",
 "checkout": "/tmp/verifyB5-M7-b (detached worktree at 09b8751; .venv symlink)",
 "scratch": "/tmp/M7-v/b5", "verified_at": "2026-10-28",
 "verdict": None,
 "registry_flags": [], "freshness_flags": [],
 "rows": rows, "mutants": [],
 "notes": ("Delta from 2657ab5 (the round-4 pin): one commit 09b8751. Changed on the slice: L04.html line 134 (article fix); L05.html lines 156, 256-261 docstring, 341-348 and 384-387 output names, 496-499 (E3), 591, 627; L06.html lines 52, 90, 103, 120, 150, 174, 275-349 names, 405, 424, 428, 454, 504, 549, 586-588; cards.json (c061, c069, c079, c083, c086, c089, c092, c093, c102, c110); twins lab-M7-L04-1.py, lab-M7-L05-1.py, lab-M7-L06-1.py; plans/M7-build-plan.md section 7.4 (project, outside this slice). "
   "Lesson slice: no project mutants are owed; the mutant run is not applicable (mutants list empty). Not checked: pace of hours (architect ruling); live web (no citation key changed; verify_refs live run recorded). "
   "Not verified by me: SEC or other external sources (none cited). Lab outputs were re-run on this pin; the page expected blocks match the runs."),
 "summary": {},
}
v = [r for r in rows if r["status"] != "PASS"]
frag["summary"] = {"rows": len(rows), "pass": len(rows) - len(v), "fail": len(v), "unverifiable": 0,
                   "fail_ids": [r["id"] for r in v]}
frag["verdict"] = "FAIL" if v else "PASS"
out = ROOT / "ledgers/M7/M7-b.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out, frag["summary"], frag["verdict"])
