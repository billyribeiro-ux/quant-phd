import json
import sys

out = sys.argv[1]
M = "course/modules/FC/FC2/"
rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        assert fix, id_
        r["fix"] = fix
    rows.append(r)


row(
    "d-p-no-file-claim",
    "2.9-prose: claim about the page vs its code",
    M + "project.html:285; course/assets/js/grader.js:46,75-78",
    "PASS",
    "project.html:285 now reads 'Nothing on this page uploads a file. The autograder panel can load a .py file from your device into the editor, and the file is read in this browser.' grader.js:46 creates input type=file (accept .py); grader.js:78 editor.value = await file.text(). The claim matches the code (round 1 finding fixed).",
)
row(
    "d-p-rubric-C3-P1-P4",
    "2.9 rubric wording vs conventions",
    M + "project.html:509",
    "PASS",
    "Level 3 now reads 'the labels P1 to P6 that it depends on, as the conventions define them' (project.html:509); the conventions define P1 to P6 at lines 328-333. Whether parity depends on P5 is raised separately in d-p-parity-P5.",
)
row(
    "d-p-exemplarA-C2-score",
    "2.3 grade of exemplar A against the rubric cells",
    M + "project.html:585, :605-606",
    "PASS",
    "Official C2 = 1 (data-scores='2,1,1,2,1', line 583). Exemplar A says no cost model is stated (line 601 'The costs are important'), and the level-1 cell is 'No cost model, or the costs are ignored.' Consistent.",
)
row(
    "d-p-exemplarB-C3-level4",
    "2.3 grade of exemplar B: level-4 shortfall",
    M + "project.html:519, :521, :577",
    "PASS",
    "Exemplar B now scores C3 3 (data-scores='4,4,3,3,3'). The miss at line 577 correctly names that the level-4 cell needs a failure consequence for each assumption (P1, P2, P5 on the convexity finding are absent: lines 561-573 give none). The level-3 'meets' claim at line 542 is disputed in d-p-parity-P5.",
)
row(
    "d-p-unequal-spacing-claim",
    "2.5 grader claim vs suite (unequal grid)",
    M + "project.html:320; grader/test_project.py:357-364",
    "PASS",
    "test_convexity_matches_oracle_on_an_uneven_grid (grader/test_project.py:357-364) checks convexity_violations against oracle_convexity on strikes 100,110,150,160,220 (answer [1,3], hand-verified: chord 42 at 110, chord 65/7 at 160). The page's 'including a chain with unequal spacing' is now enforced.",
)
row(
    "d-p-reading-convexity-bound",
    "2.9 term/theorem locator used against lesson",
    M + "project.html:657; L05 'Theorem 3.2 (convexity in strike)'",
    "PASS",
    "project.html:657 cites 'Theorem 3.2 of Lesson 5' for convexity in strike; the lesson text reads 'Theorem 3.2 (convexity in strike) Under A2, A3, A5 and (N)'. The parity relation is Theorem 1.2 of Lesson 5, which the sentence does not attach to 3.2.",
)
row(
    "d-p-spec-message-df",
    "2.6 spec wording vs reference",
    M + "project.html:312; grader/reference.py:26",
    "PASS",
    "reference.py:26 now raises 'df_ppm must lie in 1 to 1000000', the same wording as project.html:312. The plan's table (§4.4) said '1..1000000'; the page is the binding spec.",
)
row(
    "d-g-instance-spot-docstring",
    "2.9 docstring claim vs code",
    M + "grader/instance.py:6 vs :56",
    "PASS",
    "instance.py:6 now says spot between 80.00 and 200.00; code draws rng.randrange(8_000, 20_001) (line 56) = 8000..20000 cents inclusive. Matches.",
)
row(
    "d-g-overconstrained-message",
    "2.5 over-constraint on error messages",
    M + "grader/test_project.py:496-507",
    "PASS",
    "The short-list tests now assert only ValueError (lines 496-507), with no wording demanded for those conditions. test_length_message_names_both_lengths (531-536) checks the two lengths for scan. The page (line 313) says the message names the lengths, which that test enforces for scan.",
)
row(
    "d-c-ungraded",
    "2.3 BLUEPRINT s3: every substantive claim carries a grade",
    M + "cards.json",
    "FAIL",
    "27 of 130 cards have no 'grade' field (e.g. FC2-c040 single-curve identity 1+L_i = DF_{i-1}/DF_i; FC2-c090 'n+1 nodes at time n, not 2^n'; FC2-c081 'R_f = 1 + r_1'). Round 1 found 36; the count fell to 27 but the rule still fails. A grade-less card is not a checkable claim under BLUEPRINT section 3.",
    fix="Give every card a grade field: T for proved or definitional-with-proof statements (e.g. c090, c040 on the page), C or D with a basis for empirical or convention statements. Definitions with no claim may be marked as such in the schema if the builder adopts that rule.",
)
row(
    "d-c-simulated-graded-T",
    "2.3 architect rule (e): SIMULATED-lab results are grade C",
    M + "cards.json",
    "PASS",
    "Round-1 list fixed: FC2-c038, c072, c073, c074, c079 are now grade C (cards.json). The remaining T cards with SIMULATED in basis are proved on the page: FC2-c036 (telescoping proof, lab only illustrates), FC2-c056 and FC2-c057 (values written in L04 Example 2.5 at lines 'Holding the call to expiry gives 10 USD ... 6.70' and 'Exercising at date 1 ... 18.10'; checked by hand: 10e^-0.4=6.70, 20e^-0.1=18.10, 20e^-0.3=14.82). Basis strings should name the page example first (noted, not a fail).",
)
row(
    "d-c-notation-R-star",
    "2.4 notation conformity (notation/notation.json R^\\ast)",
    M + "cards.json; L03.html",
    "PASS",
    "No card or L03 text uses R^\\ast. The par rate is written R_{par} (L03.html: 30 occurrences of R_{\\mathrm{par}}; cards FC2-c042, c044, c050 use R_par). Round-1 conflict fixed.",
)
row(
    "d-c-h-number",
    "2.2 card number appears in its lesson",
    M + "cards.json FC2-c046; L03.html",
    "PASS",
    "FC2-c046 '-4415468 cents' appears in L03 text ('value to the fixed payer ... in cents: -4415468'); lab-FC2-L03-1 prints -4415468; recomputed -0.01 x 4.415468355 x 1e8 = -4415468.36 cents.",
)
row(
    "d-c-full-text",
    "2.7 every card's prose claim vs its lesson text",
    M + "cards.json (130 cards)",
    "UNVERIFIABLE",
    "Every card was read (all 130). Checked: numbers (script ledgers/FC2/scripts/FC2-d-r2/card_check_r2.py: every number token occurs in its own lesson text), cross-references (card_refs_r2.py; all Problem labels resolve to the named lesson), recomputation of closed-form numbers, lab-printed numbers against lab outputs, hypotheses of cited theorems (L05 Theorems 1.2, 2.2, 3.2, 4.1, Corollary 3.4; L06 Theorem 1.4; L07 Lemma 2.2). Not done: a line-by-line comparison of each card's claim with the full text of L01-L08 paragraphs (the lessons are other slices), so the full card-to-paragraph match is not established.",
    fix="Read each card against its lesson paragraph in L01-L08 and record the paragraph locator per card.",
)
row(
    "d-g-collect-75",
    "2.5 test count on page equals real collect-only count",
    M + "project.html:320; grader/test_project.py",
    "PASS",
    "The page now states 84 (project.html:320). 'pytest --collect-only' on grader/reference.py (as scanner.py) gives '84 tests collected' at QF_SEED=0 and QF_SEED=49; the parametrize lists are seed-independent and the five alternatives each report '84 passed' on all seeds 0-49 (witnesses_and_seeds.py output).",
)
row(
    "d-g-reference-suite",
    "2.5 reference passes every seed",
    M + "grader/reference.py; grader/test_project.py",
    "PASS",
    "tools/run_graders.py --unit FC2 --seeds 0-49: 'PASS (reference 50/50 seeds, slowest 0.2 s)'. Also 84 passed at QF_SEED=0 and 49 under --assert=plain -W error.",
)
row(
    "d-g-starter-fails",
    "2.5 starter fails the suite",
    M + "grader/starter.py",
    "PASS",
    "starter.py unchanged since pin 55b5634. Run with QF_SEED=0: '75 failed, 9 passed'. The suite fails on the starter.",
)
row(
    "d-g-alt-correct-impls",
    "2.5 over-constraint: five alternative correct implementations (architect ruling b)",
    "ledgers/FC2/scripts/FC2-d-r2/alt1_fraction_scanner.py, alt2_integer_scanner.py, alt3_float_scanner.py, alt4_slope_scanner.py, alt5_forward_scanner.py",
    "PASS",
    "Five genuinely different correct implementations: (1) Fraction throughout with independent validation; (2) integer-only arithmetic with a half-up division helper; (3) float arithmetic with floor(x+0.5) on the float result; (4) convexity by comparing adjacent slopes (valid on unequal spacing); (5) parity through the forward F = S/df. Each passes all 84 tests at every seed 0-49 (witnesses_and_seeds.py: 50/50 each). Two other over-constraints are separate FAIL rows (d-g-overconstrain-explanation-case, d-g-overconstrain-new-list).",
)
row(
    "d-g-mutants",
    "2.6 every mutant killed; >=3 new student-error mutants",
    "ledgers/FC2/mutants/ (m01-m14, m21-m30 committed; m41-m46 new this round)",
    "PASS",
    "tools/mutate_graders.py --unit FC2 --seeds 0-49: 'PASS (30/30 killed)'. Six new student-error mutants written this round by make_mutants.py: m41 cost on two legs; m42 convexity gross floored; m43 convexity findings in reverse order; m44 convexity explanation without P1; m45 call discounted in the parity gap; m46 half-spread charged once. All killed (killed_by listed in mutants).",
)
row(
    "d-g-instance-other-claims",
    "2.9 instance docstring other ranges",
    M + "grader/instance.py:1-18",
    "PASS",
    "Discount factor 0.930000-0.999000 (randrange(930000, 999001), line 60); fee 0-40 (randrange(0, 41)); half-spread 1-150 (randrange(1, 151)); six strikes on an even step (STRIKE_OFFSETS of 6). The 'half a cent' residual claim holds by construction (puts = half_up(C - S + K df), line 72) and the half-cent rejection (lines 89-90). Labelled SIMULATED (line 99).",
)
row(
    "d-p-labs-run",
    "2.5 labs run: run_labs, -I -W error, seeded",
    "tests/labs/FC2/lab-FC2-project-1.py, -2.py, -3.py; course/modules/FC/FC2/project.html",
    "PASS",
    "tools/run_labs.py --unit FC2: 'PASS (11/11)'. Each project twin run as 'python -I -W error' exits 0. Twins unchanged since pin (not in the diff). page_smoke was NOT run (see d-p-page-smoke).",
)
row(
    "d-p-lab-numbers",
    "2.2 numbers printed by project labs and the page",
    M + "project.html Lab 1 (lines 56-162), Lab 2 (166-275), Lab 3 (374-486)",
    "PASS",
    "Recomputed: Lab 1 gaps 0,120,0,0,-20,0 and chord-less-call 50,100,-75,75; findings 2 (net 75 and 30); cost 45. Lab 2 expected output identical to Lab 1 (the completed lines are the same). Lab 3: gaps 0,-60,0,0,226,540; chord-less-call 35, 470/3, -188/3, 59; gross 63, net 3; findings 3 (226/166, 540/480, 63/3); cost 60. Interpretation sentences checked (e.g. 'the chord is 625 cents', 'minus 188/3 ... minus 62.67'). Labs print exactly these (run output).",
)
row(
    "d-p-exemplar-B-numbers",
    "2.2 exemplar numbers (values)",
    M + "project.html:521-581",
    "PASS",
    "Parity at 6500: 151-1100-(5000-6175) = 226; at 7000: 90-1200-(5000-6650) = 540; convexity at 6000: chord 802/3, chord less call -188/3, gross 63, net 3; cost 3x(8+12)=60. All arithmetic re-derived. The rule violation is a separate row.",
)
row(
    "d-p-costs-and-classes",
    "2.4 mathematics: parity sign and convexity direction (reference explanations)",
    "grader/reference.py:79-99; project.html:335",
    "PASS",
    "Positive parity gap: sell call, buy put and underlying, borrow discounted strike (reference.py:81; project.html:335). Negative: reverse (reference.py:84). Convexity: middle call above chord, sell middle, buy wings in chord weights (reference.py:97). Directions match the page. The label set in the parity text is handled in d-p-parity-P5.",
)
row(
    "d-p-concepts-dag",
    "2.8 DAG: concepts used on project page inside closure",
    M + "project.html:37, :54, :335 (data-concept links); tools/check_dag.py --all",
    "PASS",
    "tools/check_dag.py --all: 'check_dag FC2: PASS'. The project's concept links (arbitrage-opportunity, put-call-parity, option-arbitrage-bounds) point to FC2's own L01 and L05.",
)
row(
    "d-p-notation-project",
    "2.4 notation conformity for the project page",
    M + "project.html; notation/notation.json",
    "PASS",
    "Project symbols are S, K, C, P, df, df_ppm (local, not registered). No registered symbol is redefined on the page (no T, no gamma, no R^\\ast, no R_f).",
)
row(
    "d-p-citations",
    "2.1 citations on the project page",
    M + "project.html:653-657 (data-cite); references/references.json",
    "PASS",
    "data-cite keys hull2021options, stoll1969relationship, cox1979option: all three present in references/references.json (entries list). 'verify_refs.py --unit FC2' (live): 3 of 560 entries, 0 problems. The page quotes no locator from these works (line 657).",
)
row(
    "d-p-hours",
    "2.9 hours arithmetic (not pace)",
    M + "project.html:338-355; index.html:29; L01-L08 data-hours",
    "PASS",
    "Time-budget rows 2+3+5+9+3+5+3 = 30 (project.html:344-351) = data-hours-project 30 (project.html:33; index.html:29). Lesson hours 6+8+9+7+8+8+8+6 = 60 = data-hours-lessons 60; 60+30 = 90, matching 'the unit's 90 hours' (line 351). Pace not assessed.",
)
row(
    "d-p-structure",
    "2.9 structure and banned phrases in project page",
    M + "project.html",
    "PASS",
    "tools/check_projects.py --all: 'check_projects FC2: PASS'. Sections present in order: Context, Inputs, Required outputs, Constraints, Grading; Rung 1-4 headings. Banned-phrase scan: 'about' appears only in exemplar A (lines 589, 593), where it is the deliberately annotated shortfall. No process words (build, builder, round, verifier, REQUESTS) in learner text.",
)
row(
    "d-p-scope-words",
    "2.7 scope words: 'every', 'only', 'all', 'same', 'always' need a computation or hypothesis",
    M + "project.html (lines 37, 282, 285, 308, 320, 329, 344, 485, 499, 510, 511)",
    "PASS",
    "Each scope word was read in context. The strong claims are backed: 'the output is exactly' (Lab 1 lines 163) by the printed run; 'every strike of two seeded chains' (line 320) by test_parity_gap_matches_exact_rounding_seed/_second_chain (6 indices each); 'every interior strike' (line 320) by the oracle tests; 'only the findings that survive the cost' (line 37, 308) by scan's net>0 rule and boundary test; 'the same expiry' (line 329) is an assumption (P2), not a computation. 'Every page of this project' (line 282) is vacuous: the project has one page.",
)
row(
    "d-c-numeric-recompute",
    "2.2 card numbers recomputed",
    M + "cards.json; ledgers/FC2/scripts/FC2-d-r2/card_check_r2.py",
    "PASS",
    "Recomputed with own code: BS call 10.450584 and put 5.573526 (c109, c118); d1=0.35, d2=0.15 (c114); L=4.877058 (c126); tree u,d,R,q for 4 steps (c115: 1.105171, 0.904837, 1.012578, 0.537808); one-step V1=12.1623 (c116); tree errors at 1,2,400 steps (c110 -91.01 cents, c111 sign pattern, c117 -0.4998 cents); 50e^0.025=51.2658 (c021); forward payoffs and cash (c023, c024); value 237.11 (c027); state prices 1/20, 17/20 and -1/5, 11/10 (c008, c013); parity-type numbers 40.48 (c076). All match. The one basis problem (c045) is a separate row.",
)
row(
    "d-c-cross-refs",
    "2.7 card cross-references resolve in the named lesson",
    M + "cards.json; ledgers/FC2/scripts/FC2-d-r2/card_refs_r2.py",
    "PASS",
    "Script reported 11 'Problem X' tokens not found as literal text; each is a problem label in the named lesson's problem set (e.g. L07 'M1 · The arguments d1 and d2' for c114; L07 'M3 · Tree parameters for four steps' for c115; L07 'E3 · Check the one-step price' for c116; L08 'M3 · Halvings for a tolerance' for c125; L03 'P2 · The par rate and the swap value' for c046; L05 'E2 · Reading the planted convexity error' for c074; L01 'E3' for c014). 'Section 5' (c076) is L05's heading '5 Where the canon breaks'. Theorem/Remark/Example/Corollary references resolve.",
)
row(
    "d-c-hypotheses-sample",
    "2.7 card hypotheses vs theorem statements (sample)",
    M + "cards.json c064, c066, c067, c069, c070, c071, c084, c106",
    "PASS",
    "Hypotheses agree with the lesson statements: c064 'A1 to A5' = Theorem 1.2 'Under A1, A2, A3, A4 and A5'; c066 'A1 to A5 and (N)' = Theorem 2.2; c069 'A2, A3, A5 and (N)' = Theorem 3.2; c070 = Corollary 3.4; c071 'A1 to A5, (N), r >= 0' = Theorem 4.1; c084 = Theorem 1.4 'A1, A2, A3, A5 and A6'; c106 'r > 0 and sigma > 0' = Lemma 2.2. c067 matches Remark 2.3 (parts a and c use (N)).",
)
row(
    "d-c-grades-T-proofs",
    "2.3 grades of proof-backed cards",
    M + "cards.json",
    "FAIL",
    "Proof-backed T cards check out (c004-c006, c019, c041, c084, c089, c093, c100-c101, c103-c104, c120-c121). FC2-c102 is graded T but says 'It is stated under A7 and used, not derived' (cards.json c102 back) and L07 says 'The formula is stated and used, not derived' (L07 section 4). Plan §5.3 item 7 requires grade C with a citation unless derived.",
    fix="Grade FC2-c102 as C with basis 'stated under A7, not derived on the page' (plan §5.3 item 7), or add a derivation and keep T.",
)
row(
    "d-g-ruff",
    "gate: ruff on grader, labs, round-2 scripts",
    "course/modules/FC/FC2/grader; tests/labs/FC2; ledgers/FC2/",
    "PASS",
    "'ruff check .' (repo): 'All checks passed!'; 'ruff format --check .': 340 files already formatted. My round-2 scripts and mutant files were formatted and checked clean.",
)
row(
    "d-gate-dag-labs-refs",
    "gate: check_dag, check_pages, check_projects, verify_refs for FC2",
    "tools/",
    "PASS",
    "check_dag --all: FC2 PASS. check_pages --all: FC2 PASS. check_projects --all: FC2 PASS. verify_refs --offline: 560 entries, 0 problems. verify_refs --unit FC2 (live): 3 of 560 entries, 0 problems.",
)
row(
    "d-p-parity-P5",
    "2.4 assumption dependency of parity findings (P5, present values taken at one moment)",
    M
    + "project.html:332 (P5), :542 (exemplar B C3 'meets' P1-P4, P6 for parity); grader/reference.py:87-89 (parity explanation)",
    "FAIL",
    "P5 says 'Every quote is a present value at the valuation date and is taken at one moment.' The parity gap C - P - (S - K df) combines the call, the put and the spot, so a parity finding depends on those three quotes being taken at one moment (a stale quote creates a spurious gap). Yet the parity explanation (reference.py:87-89) and the exemplar's level-3 'meets' (project.html:542, 'P1 to P4 and P6 for the two parity findings') omit P5, while the level-3 cell requires 'the labels P1 to P6 that it depends on' (project.html:509). Exemplar B's C3 level-3 score (data-scores 3) rests on that claim.",
    fix="Either add P5 to the parity dependencies (reference.py _explain_parity and exemplar B line 542, with 'taken at one moment' stated), or write why the parity gap does not depend on P5 and keep the exemplar's claim as is.",
)
row(
    "d-p-exemplarA-C3-score",
    "2.3 grade of exemplar A against the rubric cells (C3)",
    M + "project.html:583 (data-scores '2,1,1,2,1'), :613, :617-618",
    "FAIL",
    "Exemplar A C3 is scored 1 ('No assumption named', rubric cell level 1). But its own passage says 'The parity findings depend on the discount factor' (line 613), which names an assumption for some findings. The level-2 cell is 'Names assumptions for some findings', so the level-2 cell is met. The annotation (line 618) misses level 2 because it 'names no assumption by label', a requirement the level-2 cell does not state.",
    fix="Score exemplar A C3 as 2 (data-scores '2,1,2,2,1', official scoring line 585 to read 'C3 2'), and rewrite the line-618 annotation to say what level 2 lacks.",
)
row(
    "d-p-numbers-rule-exemplar-B",
    "2.2 exemplar numbers vs the page's own numbers rule",
    M + "project.html:498 (rule), :517 (exemplar header), :537 (exemplar B passage)",
    "FAIL",
    "The rule at line 498 says 'Every number the note quotes is either a chain input or a value that scanner.py returns, with its unit'. Exemplar B quotes 802/3 cents ('it equals 802/3 cents') and 'one third and two thirds', which are neither. The exemplar header (line 517) allows 'a product of inputs that the passage shows', which is a different rule from line 498.",
    fix="Make the two rules the same (line 498 to allow products of inputs shown in the passage, or remove 802/3 from exemplar B and state the chord value as 'minus 188/3 cents, printed by Lab 3').",
)
row(
    "d-p-message-claims",
    "2.5 claims about error messages not enforced by the grader (architect ruling a)",
    M + "project.html:309-316; grader/test_project.py:426-536",
    "FAIL",
    "The page says 'Each message names its condition' (line 309) and quotes message content: 'the message says that the strikes must be strictly increasing and positive' (311), 'df_ppm must lie in 1 to 1000000' (312), 'the message names the lengths' (313), 'the message says that the cost terms must be non-negative' (314). The tests check substrings only: 'strictly increasing' (426-464), 'df_ppm' (481-487), 'non-negative' (541, 548), the two digits only for scan with calls too short (531-536). 'positive' is never checked; the message for puts too short (504-507) and for calls too long and puts too long (510-521) and for convexity_violations with short calls (496-501) are not checked at all; 'Each message names its condition' is therefore not enforced.",
    fix="Change line 309 to 'The grader checks the exception type. For some conditions it also checks a word in the message: ...', listing only the words test_project.py matches; or add the matches to the tests.",
)
row(
    "d-p-c4-no-arbitrage-label",
    "2.5 terms used with the wrong meaning: 'no-arbitrage rules'",
    M + "project.html:510 (C4 level 3), conventions P1, P2, P5 at lines 328-332",
    "FAIL",
    "C4 level 3 says 'findings that use only the no-arbitrage rules (P1, P2, P5)'. P1 is European exercise, P2 one expiry, P5 present-value quotes taken at one moment (lines 328-332). None is the no-arbitrage hypothesis, which the lessons state as A3. The convexity test uses the no-arbitrage argument of the lessons, but the page's own labels do not express it.",
    fix="Say 'the model-free rules (P1, P2, P5)' or 'the labels P1, P2 and P5, which the convexity test uses without a discount factor'; do not call P1, P2 or P5 no-arbitrage rules.",
)
row(
    "d-g-overconstrain-explanation-case",
    "2.5 over-constraint: explanation wording (architect ruling b; witness)",
    M + "grader/test_project.py:576-584; project.html:301",
    "FAIL",
    "test_scan_explanations_are_nonempty_and_name_the_rule requires the lowercase substrings 'parity' and 'convex' (lines 582-583). The page (line 301) requires only that the explanation 'names the rule and the assumptions ... by the labels'. Witness w1 (ledgers/FC2/scripts/FC2-d-r2/witnesses_and_seeds.py, same as alt1 with 'Parity (P1, ...)' and 'Convexity in strike (P1, ...)'): 13/50 seeds pass, 37 fail (first failing seeds 0, 2, 3, 4, 5), each failing in test_scan_explanations_are_nonempty_and_name_the_rule. A correct explanation that starts a sentence with a capital is rejected.",
    fix="Compare case-insensitively: rule = 'parity' if kind == 'parity' else 'convex', tested as rule in text.lower().",
)
row(
    "d-g-overconstrain-new-list",
    "2.5 over-constraint: identity of the returned list (witness)",
    M + "grader/test_project.py:184-190; project.html:301",
    "FAIL",
    "test_scan_returns_a_new_list_each_call asserts 'first is not second' (line 189). The page (line 301) says scan 'returns one record for each finding'; it says nothing about object identity. Witness w2 (memoised scan returning the same list for the same chain; witnesses_and_seeds.py): fails on 50/50 seeds (only this test) while being a correct scanner.",
    fix="Delete the identity assertion (line 189) and keep the equality of the two results (line 190).",
)
row(
    "d-c-c045-rounding-basis",
    "2.2 ratio/rounding basis stated when rounding differs",
    M + "cards.json FC2-c045 (lab-FC2-L03-1 prints 0.049026 and 4902625)",
    "FAIL",
    "The back says 'The par rate is 0.049026 ... The fixed payment is 4902625 cents, which is 49,026.25 dollars.' 0.049026 x 1,000,000 = 49,026.00 dollars, not 49,026.25. The payment uses the unrounded par rate: R = (1 - DF_5)/sum DF_i = 0.04902624503..., and 1e6 x R = 49,026.245 dollars = 4,902,624.5 cents, which rounds to 4902625 cents. The card does not state this basis.",
    fix="Write: 'The par rate is 0.049026 to six places. The fixed payment at the unrounded par rate, 0.0490262450, is 4902625 cents (49,026.25 dollars).'",
)
row(
    "d-c-notation-R-plain",
    "2.4 notation conformity: gross riskless return written R (plan §5.1 requires R_f)",
    M + "cards.json FC2-c105, c106, c107; plan §5.1; notation/notation.json R_f",
    "FAIL",
    "notation.json registers R_f as the gross riskless return for the period. Plan §5.1 says the one-period binomial uses R_f. The L07 cards write R = e^{rh} for the gross riskless return per step (c105 'R = e^{rh}', c106 '0 < d < R < u', c107 'e^{-rτ} equals R^{-n}'), which is the same meaning under a different symbol.",
    fix="Use R_f for the per-step gross return in L07 (R_f = e^{rh} for the step of length h), in the cards and the lesson text.",
)
row(
    "d-p-page-smoke",
    "2.5 page_smoke for the project page (Chromium)",
    M + "project.html",
    "UNVERIFIABLE",
    "tools/page_smoke.py --unit FC2 --pages project.html --skip-sweep failed at launch: 'BrowserType.launch: Executable doesn't exist at .../chrome-headless-shell'. The Playwright browser is not installed in this environment and was not installed (no package installs allowed). The page's dark/light, 360 px and Pyodide run were not exercised.",
    fix="Install the Playwright browser through the project's own setup (not a global install) and rerun page_smoke for project.html.",
)

counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1

mutants = [
    {
        "id": "m01_parity_strike_not_discounted",
        "description": "Parity uses the strike K instead of the discounted strike K df (both entry points).",
        "killed_by": "test_parity_gap_matches_exact_rounding_seed[0] (seed 0)",
    },
    {
        "id": "m02_parity_sign_flipped",
        "description": "Parity gap sign flipped: parity_gap_cents returns the negated gap.",
        "killed_by": "test_parity_gap_matches_exact_rounding_second_chain[2] (seed 0)",
    },
    {
        "id": "m03_cost_charged_once",
        "description": "Cost charged once per finding (one leg) instead of per leg (three legs).",
        "killed_by": "test_scan_matches_exhaustive_oracle_second_chain (seed 0)",
    },
    {
        "id": "m04_costs_ignored",
        "description": "Costs ignored: gross violations are reported as findings with no cost netting.",
        "killed_by": "test_scan_matches_exhaustive_oracle_second_chain (seed 0)",
    },
    {
        "id": "m05_no_ordering_check_input_order",
        "description": "Ordering not checked: convexity is computed in the input order of strikes, so shuffled strikes are accepted.",
        "killed_by": "test_strikes_equal_neighbours_are_rejected_by_scan (seed 0)",
    },
    {
        "id": "m06_convexity_first_difference",
        "description": "Convexity tested with the first difference: a violation is a call that falls between neighbours, not a second difference.",
        "killed_by": "test_convexity_matches_exhaustive_oracle_seed (seed 0)",
    },
    {
        "id": "m07_rounding_truncates_toward_zero",
        "description": "Rounding by truncation toward zero instead of half up, so an exact half cent goes down in magnitude.",
        "killed_by": "test_parity_gap_matches_exact_rounding_second_chain[2] (seed 0)",
    },
    {
        "id": "m08_df_read_as_parts_per_thousand",
        "description": "df_ppm read as parts per thousand: the discount factor is df_ppm / 1000.",
        "killed_by": "test_parity_gap_matches_exact_rounding_seed[5] (seed 0)",
    },
    {
        "id": "m09_net_rule_at_least_zero",
        "description": "Net-of-cost rule uses >= 0: a finding whose net amount is exactly zero is kept.",
        "killed_by": "test_finding_with_net_exactly_zero_is_not_returned (seed 0)",
    },
    {
        "id": "m10_seed0_answer_hard_coded",
        "description": "Hard-coded answer: scan returns seed 0's findings for any chain.",
        "killed_by": "test_strikes_equal_neighbours_are_rejected_by_scan (seed 0)",
    },
    {
        "id": "m11_convexity_on_discounted_quotes",
        "description": "Convexity test run on call quotes discounted by df_ppm (P5 says quotes are present values, so no discounting).",
        "killed_by": "test_scan_matches_exhaustive_oracle_seed (seed 2)",
    },
    {
        "id": "m12_midpoint_chord_ignores_spacing",
        "description": "Convexity chord uses equal weights of one half on the two neighbours, wrong on an uneven strike grid.",
        "killed_by": "test_unequal_grid_no_false_positive (seed 0)",
    },
    {
        "id": "m13_gross_rounds_half_even",
        "description": "Gross amount rounded with Python round(), which sends an exact half cent to the even cent, not up.",
        "killed_by": "test_half_cent_gross_rounds_once_up (seed 0)",
    },
    {
        "id": "m14_convexity_skips_last_interior",
        "description": "Convexity scan stops one strike early, so a violation at the last interior strike is never reported.",
        "killed_by": "test_convexity_findings_come_in_strike_order (seed 0)",
    },
    {
        "id": "m21_df_lower_bound_zero_accepted",
        "description": "Student error: df_ppm = 0 accepted, so the range lower bound is off by one.",
        "killed_by": "test_parity_gap_df_range_lower_boundary (seed 0)",
    },
    {
        "id": "m22_df_upper_bound_one_too_high",
        "description": "Student error: df_ppm = 1000001 accepted, so the range upper bound is off by one.",
        "killed_by": "test_parity_gap_df_range_upper_boundary (seed 0)",
    },
    {
        "id": "m23_zero_strike_accepted_by_parity",
        "description": "Student error: parity_gap_cents accepts a strike of zero, because the check uses < instead of <=.",
        "killed_by": "test_parity_gap_rejects_a_nonpositive_strike_and_accepts_one (seed 0)",
    },
    {
        "id": "m24_convexity_flags_call_on_chord",
        "description": "Student error: a call exactly on the chord is flagged, so the test uses <= 0 instead of < 0.",
        "killed_by": "test_convexity_boundary_equal_to_chord_is_not_flagged (seed 0)",
    },
    {
        "id": "m25_zero_net_finding_kept",
        "description": "Student error: a finding whose net amount is exactly zero is kept, so the net test uses >= 0 instead of > 0.",
        "killed_by": "test_finding_with_net_exactly_zero_is_not_returned (seed 0)",
    },
    {
        "id": "m26_negative_half_spread_accepted",
        "description": "Student error: a negative half-spread is accepted, because the cost check only looks at the fee.",
        "killed_by": "test_negative_half_spread_is_rejected_and_zero_is_accepted (seed 0)",
    },
    {
        "id": "m27_equal_weights_on_uneven_grid",
        "description": "Student error: the chord uses equal weights on the two neighbours, which is right only on an even grid.",
        "killed_by": "test_unequal_grid_no_false_positive (seed 0)",
    },
    {
        "id": "m28_half_cent_gross_rounds_half_down",
        "description": "Student error: the gross of a half-cent tie rounds toward zero, so an exact 2.5 cents gives 2 instead of 3.",
        "killed_by": "test_half_cent_gross_rounds_once_up (seed 0)",
    },
    {
        "id": "m29_parity_findings_in_reverse_strike_order",
        "description": "Student error: parity records are built from the strikes in reverse order, which breaks the required strike order.",
        "killed_by": "test_parity_findings_come_in_strike_order (seed 0)",
    },
    {
        "id": "m30_puts_length_not_checked",
        "description": "Student error: the quote-length check ignores the put list, so a short put list is not rejected.",
        "killed_by": "test_puts_shorter_than_strikes_is_rejected (seed 0)",
    },
    {
        "id": "m41_cost_charged_on_two_legs",
        "description": "Student error: each finding is charged two legs of fee plus half-spread instead of three.",
        "killed_by": "test_scan_matches_exhaustive_oracle_second_chain (seed 0)",
    },
    {
        "id": "m42_convexity_gross_floored",
        "description": "Student error: the convexity gross is floored, so a 0.5-cent or 1.5-cent violation loses its half cent.",
        "killed_by": "test_convexity_half_cent_gross_rounds_once_up (seed 0)",
    },
    {
        "id": "m43_convexity_findings_reversed",
        "description": "Student error: convexity findings are emitted in reverse strike order.",
        "killed_by": "test_convexity_findings_come_in_strike_order (seed 0)",
    },
    {
        "id": "m44_convexity_explanation_without_P1",
        "description": "Student error: the convexity explanation omits the European-exercise label P1 it depends on.",
        "killed_by": "test_scan_explanations_are_nonempty_and_name_the_rule (seed 2)",
    },
    {
        "id": "m45_call_discounted_in_parity",
        "description": "Student error: the call is discounted by df in the parity gap, as if it were a payment at expiry.",
        "killed_by": "test_scan_matches_exhaustive_oracle_seed (seed 0)",
    },
    {
        "id": "m46_spread_charged_once",
        "description": "Student error: the half-spread is charged once per finding while the fee is charged on each of three legs.",
        "killed_by": "test_scan_matches_exhaustive_oracle_second_chain (seed 0)",
    },
]

fragment = {
    "unit": "FC2",
    "slice": "FC2-d (project.html rubric and exemplars, grader/ (instance, reference, starter, test_project), project labs lab-FC2-project-1..3, cards.json, project mutants)",
    "round": 2,
    "verifier": "Claude Haiku 5.5 (independent verifier, FC2 slice d, round 2; not the builder)",
    "pin": "e22feb3 (detached checkout /tmp/verifyC2-FC2-d)",
    "base": "55b5634 (round 1 pin; delta computed from it)",
    "previous_ledger": "/tmp/fanout-frags/C-FC2-d.round1.json",
    "checkout": "/tmp/verifyC2-FC2-d",
    "scratch": "/tmp/fc2-v/d2",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 2. Delta from 55b5634 to e22feb3 for this slice: project.html, grader/instance.py, grader/reference.py, "
        "grader/test_project.py, cards.json changed; starter.py, lab-FC2-project-1..3.py unchanged. Carried rows were "
        "re-verified because their cited subjects changed (no row carried on the strength of round 1 alone). "
        "Scripts: ledgers/FC2/scripts/FC2-d-r2/ (make_mutants.py, alt1..alt5, card_check_r2.py, card_refs_r2.py, "
        "witnesses_and_seeds.py). Not checked: page_smoke (no Chromium); a full claim-by-claim comparison of all 130 cards "
        "against the full text of L01-L08 (lessons are other slices); lab outputs of L01-L08 were run and read only for the "
        "card numbers. The round-2 mutants m41-m46 were made with make_mutants.py; the first attempt had a docstring placement "
        "bug (SyntaxError, reported as collection errors) and was corrected before the reported run. No git operations."
    ),
    "summary": {},
}
fragment["summary"] = {
    "rows": len(rows),
    "PASS": counts.get("PASS", 0),
    "FAIL": counts.get("FAIL", 0),
    "UNVERIFIABLE": counts.get("UNVERIFIABLE", 0),
    "mutants": len(mutants),
    "mutants_killed": len(mutants),
}
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print(fragment["summary"])
