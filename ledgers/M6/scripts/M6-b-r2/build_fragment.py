import json, datetime
P = "PASS"; F = "FAIL"
rows = []
def r(id_, check, location, status, evidence, fix=None):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        row["fix"] = fix
    rows.append(row)

r("M6-b-cmd-pin", "pin and inventory of the slice at e22feb3", "course/modules/M/M6/L05.html..L08.html; tests/labs/M6/lab-M6-L05-1.py..L08-1.py; course/modules/M/M6/cards.json",
  P, "git -C checkout log -1 = e22feb3; git status: only untracked .venv symlink. Delta from round-1 pin 55b5634: git diff --stat 55b5634 e22feb3 touches L05-L08 pages, labs L05/L06/L07 (docstrings and one comment), cards.json; notation/, references/, tools/ unchanged. All slice rows re-verified (round-1 PASS rows carried only where the subject is byte-identical; none is, since every page changed).")
r("M6-b-inventory", "every line of the four pages, twins and cards read", "L05.html (503 lines), L06.html (486), L07.html (537), L08.html (516); twins; cards M6-c043..c084 and c125..c127 (44 slice cards)",
  P, "Read in full with the Read tool in this round (page bodies, embedded expected blocks, problem sets, quizzes, key-results tables, references). Round 1 counted 42 cards; this pin has 44 (c063 removed, c125-c127 added).")
r("M6-b-check-pages", "tools/check_pages.py --unit M6 --page L05..L08", "course/modules/M/M6/L05.html..L08.html",
  P, "Output: 'check_pages M6 L05: PASS', 'check_pages M6 L06: PASS', 'check_pages M6 L07: PASS', 'check_pages M6 L08: PASS' (exit 0 each).")
r("M6-b-check-dag", "tools/check_dag.py --unit M6", "M6 DAG",
  P, "Output 'check_dag M6: PASS'. Concept use outside the closure {M1,M2,M4,M5,P0.1}: multiple-integral (M2), expectation and conditional-expectation-elementary (M4) are inside; in-unit concepts (sigma-algebra, lebesgue-integral, probability-space, radon-nikodym-theorem, conditional-expectation-l2, filtration, martingale, fubini-theorem) are defined in M6 lessons; L07 names orthogonal projection and inner product only in plain prose (plan section 12 default).")
r("M6-b-run-labs", "tools/run_labs.py --unit M6; each twin run as python -I -W error", "tests/labs/M6/lab-M6-L05-1.py..L08-1.py",
  P, "'run_labs M6: PASS (15/15)'. Direct runs: exit 0 and empty stderr for L05, L06, L07, L08 (scratch /tmp/M6-v/M6-b/out-L0n.txt, err-L0n.txt).")
r("M6-b-embed-match", "embedded code and expected output equal the twin and a fresh run", "course/modules/M/M6/L05.html..L08.html (pre data-run; pre.expected)",
  P, "ledgers/M6/scripts/M6-b-r2/embed_check.py (python -I): L05 expected_equals_output True, code_equals_twin True; same for L06, L07, L08.")
r("M6-b-page-smoke", "tools/page_smoke.py --unit M6 --pages L05 L06 L07 L08", "the four pages",
  P, "'page_smoke modules/M/M6/L05..L08.html: PASS' (labs: L05 1.1 s incl. boot, L06, L07 0.0 s, L08 0.6 s); 'page_smoke M6: PASS'.")
r("M6-b-ruff-mypy", "ruff, ruff format, mypy --no-incremental on the four twins", "tests/labs/M6/lab-M6-L05-1.py..L08-1.py",
  P, "ruff check: 'All checks passed!'; ruff format --check: '4 files already formatted'; mypy: 'Success: no issues found in 4 source files'.")
r("M6-b-registry", "citations: verify_refs live and offline; slice cites no key", "L05..L08 references sections; references/references.json; curriculum/01-foundations.yaml:286-288",
  P, "tools/verify_refs.py --unit M6: 'live re-verification of M6: 2 of 560 entries, 0 problems'. --offline: 'offline integrity: 560 entries, 0 problems'. The four pages carry empty data-references and state that they cite no key. Bibliographic lines quoted in the references sections (Williams 1991, Billingsley 2012) match curriculum/01-foundations.yaml:287-288 (read in this round); the pages say they did not read the books, which is accurate.")
r("M6-b-hours", "declared hours and hub split", "data-hours in L05..L08; index.html data-hours-lessons",
  P, "L05..L08 data-hours=9 each; all 12 lessons 9; index data-hours-lessons=108 = 12x9; data-hours-project=42; 108+42=150 (curriculum hours 150). Pace not judged (architect ruling).")
r("M6-b-numbers", "displayed numbers recomputed from unrounded values", "L05 lines 217-250, 251, 342-349; L06 lines 235-249; L07 lines 277-294; L08 lines 228-259",
  P, "ledgers/M6/scripts/M6-b-r2/recompute_r2.py (python -I -W error): pi/4=0.7853981634; quadrature error +1.302e-7 and -1.302e-7; 9*(arctan2-pi/4)=2.8957549896, 10*(...)=3.2175055440; block value 0.3217505544; M1 I1=I2=4/3; M2 f=(1/2,1/2,1,2), M3 17/8 both; L07 cell averages 1, 6/5, 6/7; MSE of cell average 767/140=5.4785714286 (recomputed independently); E[X]=1; projection coefficients 6/7, -1/5, 12/35 and value 1 on cell {0,1,2}; L08 M2 E[S2]=-2/3, weights 1/9,2/9,2/9,4/9; M3 cell average 2/3. Remark 2.4 example mu=(1,1), nu=(2,0) total masses 2.")
r("M6-b-quiz-numeric", "quiz data-answer and tolerance against exact value", "L05 quiz q2 (1.3333, tol 1e-4), q5 (0.7854, 5e-5), q8 (0.3217505544, 1e-10); L06 q2 (2), q5 (0.3333, 5e-5); L07 q2 (1.5), q5 (1.2), q9 (5.4785714286, 1e-8); L08 q5 (0.6667, 5e-5), q6 (-0.6667, 5e-5)",
  P, "Differences from exact values: 3.3e-5 (<1e-4), 1.8e-6 (<5e-5), 3.4e-12 (<1e-10), 3.3e-5 (<5e-5), 2.9e-11 (<1e-8), 3.3e-5 (<5e-5), 3.3e-5 (<5e-5); all within tolerance, scratch recompute_r2.py.")
r("M6-b-L05-math", "re-derivation of Thm 1.2, Prop 3.1, Prop 3.2 and Remark 3.3", "L05.html Theorem 1.2 (line 70-83), Prop 3.1 (113-127), Prop 3.2 (129-144), Remark 3.3 (146-149)",
  P, "Re-derived each step: G'=f and H'=f by quotient rule; int_0^1 f dy = 1/(1+x^2); int_0^1 f dx = -1/(1+y^2); substitution x=a t gives block value arctan2-arctan1 for every a>0; f>=0 on Q_k since x>a_k>=y; f^+ >= N c. Assumption-number references (Assumption 2, 3, 4) match the lists at lines 117-120, 133-136.")
r("M6-b-L06-math", "re-derivation of Lemma 1.2, Thm 2.2 (a)(b)(c), Props 2.2 and 2.3, Remark 2.4", "L06.html Lemma 1.2 (63-75), Thm 2.2 (93-108), Prop 2.2 (110-124), Prop 2.3 (126-139), Remark 2.4 (141-144)",
  P, "Re-derived: both directions of Lemma 1.2; (c) via nu(A)=sum g mu over mu-null points; (b) via A={omega}; (a) by splitting A by mu>0 with Lemma 1.2; Prop 2.2 by A={omega} and distributive law; Prop 2.3 with A={omega_0}. Remark 2.4 example: mu=(1,1), nu=(2,0), density at point 1 is 2.")
r("M6-b-L07-math", "re-derivation of Prop 1.1, Thm 2.2 (orthogonality, Pythagoras, uniqueness), Prop 2.4 (tower)", "L07.html Prop 1.1 (60-73), Def 2.1 (78-80), Thm 2.2 (82-101), Remark 2.3 (103-106), Prop 2.4 (108-126)",
  P, "Re-derived: E[(X-Y)1_{B_j}] = E[X1_{B_j}] - Y_j P(B_j) = 0; E[(X-Y')^2]=E[(X-Y)^2]+E[D^2]; uniqueness via E[(Y-Y')^2]=0; tower property by summing Y_j P(B_j) over the fine cells inside each coarse cell. Defects in the tie-count explanation and in the L2 wording are separate rows.")
r("M6-b-L08-math", "re-derivation of Prop 2.1, Def 2.2, Prop 2.2, Prop 2.3 and Remark 2.4", "L08.html Prop 2.1 (72-85), Def 2.2 (87-90), Prop 2.2 (92-105), Prop 2.3 (107-120), Remark 2.4 (122-125)",
  P, "Re-derived: P(B)=prod q(h_i); P(B and X_{k+1}=s)=P(B)q(s); average of X_{k+1} on B = p-(1-p)=2p-1; S_k constant on B; compensated walk M_k = S_k - k(2p-1) is a martingale; fair walk S_k^2 - k martingale (R1). Cells at levels 0..9 total 1023.")
r("M6-b-problems-L05-L08", "worked solutions recomputed (mechanics, proof, empirical, research)", "L05 M1-M3, P1-P3, E1-E3, R1-R3; L06 M1-M3, P1-P3, E1-E3, R1-R3; L07 M1-M3, P1-P3, E1-E3, R1-R3; L08 M1-M3, P1-P3, E1-E3, R1-R3",
  P, "All numerical solutions recomputed (see M6-b-numbers). Exact arithmetic re-run for L06 M2/M3/E1/E2, L07 M1/M3/E2, L08 M2/M3. The text defects found in L06 R3 and L07 E3 are separate FAIL rows (M6-b-r2-L06-R3-question, M6-b-r2-L07-E3-tie).")
r("M6-b-grades", "grade attributes on claim blocks and key-results tables", "L05 Thm 1.2, Props 3.1-3.2 (data-grade T); L06 Lemma 1.2, Thm 2.2, Props 2.2-2.3; L07 Prop 1.1, Thm 2.2, Prop 2.4; L08 Props 2.1-2.3; key-results tables L05..L08",
  P, "Every proved Theorem/Proposition/Lemma carries data-grade=T; assumptions listed; Assumption F, T, RN, CE and Remark 2.6 are marked not proved and not graded; L08 lab-based row is 'not graded' (see M6-b-r2-card-c081-grade).")
r("M6-b-scope-words", "scope words (every, all, only, always, never, any, same) backed by a computation or a stated hypothesis", "L05..L08 prose; labs' 'all' claims",
  P, "grep with context; each universal claim checked: 'all 16 events' (L06 Part A, printed all_events_match True), 'every cell' (L08 Part B, 1023 of 1023 printed), 'all 125 candidates' (L07 Part C, printed), 'every path' (L08 E3, 1024 per level). The R1 use of Assumption T is a separate FAIL row (M6-b-r2-L05-T-not-used).")
r("M6-b-banned-process", "banned phrases and process words in learner text and cards", "L05..L08 pages; cards.json slice",
  P, "grep -i for builder, verifier, REQUESTS, unit report, round (as a word), TODO, TBD, lorem, studies show, clearly, obviously: no hits. Banned phrases such as 'roughly' and 'historically': no hits; 'about' appears only with a computed value (error about 10^-7, shown at 1.30e-7).")
r("M6-b-dag-links", "every in-page link and anchor used by the meta rows exists", "L05 meta (sigma-algebra, lebesgue-integral, multiple-integral, fubini-theorem); L06 meta; L07 meta (conditional-expectation-l2, radon-nikodym-theorem); L08 meta (filtration, martingale, expectation)",
  P, "grep id= anchors: def-sigma-algebra (L01), def-probability-space (L02), def-lebesgue-integral (L03), def-radon-nikodym-theorem (L06), def-conditional-expectation-l2 (L07), def-fubini-theorem (L05), def-filtration and def-martingale (L08): each count 1.")
r("M6-b-dup-cards", "exact duplicate fronts across the unit's cards", "course/modules/M/M6/cards.json (122 cards)",
  P, "Python scan: 0 exact duplicate fronts, 122 unique ids. The former near-duplicate M6-c063 is gone (ids run c061, c062, c064). Near-duplicates remaining in the slice are a separate FAIL row (M6-b-r2-card-near-dup).")
r("M6-b-card-T-basis", "theorem-grade cards and cards with a graded result carry a basis", "cards M6-c044, c047, c048, c050-c053, c055, c058-c060, c062, c064-c065, c067-c068, c070, c072-c073, c076, c078-c080, c082-c084 (T); c049, c061, c071, c081 (C)",
  P, "T cards are theorem statements of the lesson (no basis required, BUILDER_RULES section 7). C cards carry a basis field naming Lab 1 (c049 'Lab 1, Parts B and C'; c061 'Lab 1, basis: exact fraction computation in Part A'; c071 'Lab 1, basis: exact cell averages in Part A'; c081 'Lab 1, Part B (exact enumeration of the ten-step tree)').")
r("M6-b-card-hub-agreement", "hub descriptions for L05..L08 agree with the lessons", "course/modules/M/M6/index.html lines 147-150 (cards L05-L08)",
  P, "Hub descriptions: Fubini interchange for finite products and the function whose integrals disagree (L05); finite case of Radon-Nikodym checked exactly (L06); conditional expectation as projection with tower property (L07); filtrations, fair walk martingale, biased walk not (L08). Each matches the lesson title and key results.")
r("M6-b-quiz-answers", "each data-correct option and its explanation", "L05..L08 quiz sections",
  P, "Options checked against the lesson text and printed lab output: L05 q1, q3, q4, q6, q7, q9, q10; L06 q1, q3, q4, q6, q7, q8; L07 q1, q3, q4, q6, q7, q8; L08 q1-q4, q8-q10. Explanations cite existing items (Definition 1.1, Proposition 2.3, Remark 3.3, Problem E3).")
r("M6-b-mutants", "project-grader mutants (architect ruling)", "ledgers/M6/mutants/",
  P, "Not applicable: the architect ruling limits mutation testing to project graders; slice M6-b has lessons and lab twins only; no grader. Recorded as N/A with PASS status.")
r("M6-b-notation", "every symbol checked against notation/notation.json", "L05..L08 pages (raw TeX and macros)",
  P, "Registered macros used: \\E, \\Prob, \\indic only; grep for raw \\mathbb{E}, \\mathbb{P}, \\mathbf{1}: 0 hits in L05..L08 (fixed since round 1). Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}: no occurrence in the slice. Local letters p (weights in L07, step probability in L08), C, H, N, S, M, Q_k, a_k are defined in each lesson where used.")
r("M6-b-lab-claims", "every sentence about what a lab prints, checks or contains vs code and output", "L05 lines 153-154, 251, 259 hypothesis/interpretation; L06 148, 249; L07 141, 294; L08 129, 259",
  P, "Checked each hypothesis and interpretation sentence against code and printed output: L05 Part C block 0 quadrature (1.60e-12) and six partial sums; L06 16 events, 32 events, one failure (mask 16), 16 misses, flags; L07 flags and count 0 of 125 ties; L08 1023 of 1023, 0 of 1023, 10240 mismatched, -1/3 increment, -10/3. Two sentences need fixes and are separate FAIL rows (M6-b-r2-L06-interp-16-misses; the L08 Part-label wording is accepted as sequence, see row note).")
r("M6-b-L05-sigma-finite", "round-1 FAIL: sigma-finite reason", "L05.html:87 versus L05.html:147-150 and 256",
  P, "Now reads 'Each space in this lesson is either finite or the unit square with area (Lebesgue measure), and each is sigma-finite, because each is a countable union of sets of finite measure.' Consistent with Section 4 and Prop 3.2.")
r("M6-b-L05-lab1-blocks", "round-1 FAIL: lab hypothesis claims vs block-integral check", "L05.html:147-165 (Remark 3.3, lab hypothesis, docstring), 197-203, 218-226",
  P, "Hypothesis now says block 0 alone is quadrature-checked and partial sums are of the closed form; code confirms (block_check on Q_0 = (0.5,1] x [0,0.5]); output 'block_0_quadrature ... error -1.60e-12'. The docstring of block_integral_closed states the scaling argument.")
r("M6-b-L05-lab1-docstring", "round-1 FAIL: substitution docstring", "L05.html:158-160 and tests/labs/M6/lab-M6-L05-1.py",
  P, "Docstring now reads 'substitution y = s^2 (first order) or x = s^2 (second order)', matching inner_over_y (y = s*s, dy = 2s ds) and inner_over_x.")
r("M6-b-L05-quiz-cite", "round-1 FAIL: quiz explanation cites Remark 2.1 for continuity", "L05.html:427",
  P, "Now: 'Assumption F lists measurability and integrability (items 2 and 3); continuity is not among its items.' Matches Assumption F at lines 90-95.")
r("M6-b-L05-canon-logic", "round-1 FAIL: canon-breaks logic", "L05.html:257",
  P, "Now: 'Existence of both iterated integrals is therefore not enough to justify an interchange.' Matches Remark 2.1 and Prop 3.2.")
r("M6-b-L06-E2-lemma", "round-1 FAIL: E2 solution cites Lemma 1.2 for points outside A", "L06.html:345-346",
  P, "Now: every point of A has mu > 0 when A avoids point 5, so f mu = nu there directly; the candidate integral equals nu(A) minus nu(5) when A contains point 5. Re-derived.")
r("M6-b-L06-point-index", "round-1 FAIL: 'point 4' used for two indexings", "L06.html:148, 153-158, 196-197, 265-266, 338-339, 343-346 and lab twin docstrings",
  P, "Now the text says point 5 (index 4 in code) throughout; the only fourth-point reference is Part A's fourth point (index 3, mu = 3/8). grep 'point 4' in L05-L08 finds no misuse.")
r("M6-b-L06-prop-order", "round-1 FAIL: proposition numbering order", "L06.html:110-139",
  P, "Proposition 2.2 (integrals against a density) now precedes Proposition 2.3 (no density when mu vanishes); numbering is in page order.")
r("M6-b-L07-general-definition", "round-1 FAIL: why-it-matters vs Remark 2.6", "L07.html:52 versus 134-136",
  P, "Now: 'The general definition is Assumption CE (Remark 2.6), not proved here.' Consistent with Remark 2.6 and Assumption CE.")
r("M6-b-L07-L2-undefined", "round-1 FAIL: L2 used before definition", "L07.html:56",
  P, "Section 1 now defines the space in plain words: every function here is square-integrable (its second moment is finite; the space of such functions is written L2). Defined before the first use in Definition 2.1.")
r("M6-b-L07-smallest-of-125", "round-1 FAIL: average vs 125 candidates", "L07.html:141, 294, 399, 508",
  P, "Hypothesis and quiz now say no candidate among the 125 has a smaller error; the average (1, 6/5, 6/7) is not among the candidates, and the printed count of ties is 0. Code: part_c checks best <= e for all 125 candidates. (The tie explanation's missing uniqueness step is a separate FAIL row.)")
r("M6-b-notation-macros", "round-1 FAIL: raw TeX instead of registered macros", "L05 (1 use), L07 (120 E, 20 P, 29 1), L08 (37 E, 7 P, 2 1)",
  P, "Re-counted: raw \\mathbb{E}, \\mathbb{P}, \\mathbf{1} absent from L05..L08; \\E (120+37), \\Prob (20+7), \\indic (1+29+2) used instead.")
r("M6-b-card-c081", "round-1 FAIL: card M6-c081 content and grade field", "course/modules/M/M6/cards.json id M6-c081 (line 546)",
  P, "Card now has grade C and basis 'Lab 1, Part B (exact enumeration of the ten-step tree)'; back says the first-cell increment is -1/3 at every level, which the lab prints (increment -1/3 at levels 0..9) and which equals 2p-1 (Prop 2.3). Content correct; the grade mismatch with the lesson table is a separate FAIL row.")
r("M6-b-card-density-dup", "round-1 FAIL: duplicate density cards", "cards.json M6-c061 and M6-c063",
  P, "M6-c063 no longer exists; the remaining density card M6-c061 covers the 'probability between 0 and 1' fact only. The 'unique at every point' fact is M6-c064 (distinct).")
r("M6-b-L05-T-not-used", "Assumption T 'not used in any proof on this page' vs R1 problem", "L05.html:101 (Assumption T 'not used in any proof on this page') versus L05.html:365 and 367 (R1: 'so Assumption T gives equality'; 'This is the nonnegative case of Assumption T')",
  "FAIL", "The R1 problem statement uses Assumption T to conclude equality of the two iterated integrals of g = 1/(xy), and its solution names Assumption T as the reason equality holds. Line 101 says T is not used in any proof on the page. The solution itself computes both integrals as +infinity directly, so the conclusion does not depend on T; the claim in the problem statement does.",
  "Either reword R1 to 'show directly that both iterated integrals are +infinity; this is the nonnegative case of Assumption T, which also gives equality' or change line 101 to 'Assumption T is used only in Problem R1, as an illustration, and in no proof of a result on this page.'")
r("M6-b-r2-L06-R3-question", "research problem R3 answers a different question than it asks", "L06.html:375-378 (R3 question says 'on a countable space'; solution argues about 'a general space')",
  "FAIL", "The question asks why the uniqueness statement of Assumption RN is needed on a countable space. The solution gives reasons for a general space ('On a general space, a point may have measure zero ...') and never addresses countable spaces.",
  "Rewrite the solution to address a countable space (points of zero weight are the only places the density is free, and Assumption RN is needed only for the general space), or change the question to 'on a general space'.")
r("M6-b-r2-L07-E3-tie", "tie count explanation omits the uniqueness step", "L07.html:399 (E3 solution); 294 (Part C interpretation: 'The count of candidates with equal error is 0, because ... not one of the 125 integer-valued functions')",
  "FAIL", "candidates_with_equal_mse 0 is justified only by the average not being among the 125 integer-valued candidates. A candidate with the minimal error would be a second minimizer over all G-measurable functions, which Theorem 2.2(a) rules out. The page never cites that uniqueness step; E3 asserts 'A tie would need a candidate equal to the average at every point' without a reason.",
  "In E3 and in the Part C interpretation, add: a tie would be a second minimizer over all G-measurable functions, which Theorem 2.2(a) excludes, so it would equal the cell average; the average is not integer-valued, so no candidate qualifies.")
r("M6-b-r2-L06-interp-16-misses", "interpretation attributes identity of the 16 misses to lab output", "L06.html:249 ('The candidate density gives 16 misses, which are the 16 events that contain point 5') versus lab twin output 'candidate_density_misses 16' (line 243 of the embedded block)",
  "FAIL", "The lab prints only the count 16 and the flag False. The identity with the events containing point 5 is shown by Problem E2 (L06.html:345-346), not by the lab output that the interpretation paragraph describes.",
  "Move the identity to a sentence citing Problem E2: 'The 16 misses are the events that contain point 5 (Problem E2); the lab prints their count.'")
r("M6-b-r2-card-c081-grade", "card grade disagrees with the lesson's key-results row", "cards.json M6-c081 (grade C) versus L08.html:405 key-results row 'On the ten-step tree ... (Lab 1, Part B) | not graded'",
  "FAIL", "The same result is graded C on the card and 'not graded' in the lesson table. BUILDER_RULES section 7 and the rule that cards agree with the current lesson text are both breached.",
  "Either grade the key-results row 'C' with basis 'Lab 1, Part B' (and regenerate cards.json through the card generator), or remove the grade from card M6-c081 and keep the lab statement as prose.")
r("M6-b-r2-card-near-dup", "one fact per card: near-duplicates in the slice", "cards.json M6-c049 vs M6-c052 (both: agreement with the closed forms does not test integrability); M6-c048 vs M6-c053 (both: f+ has infinite integral via the blocks)",
  "FAIL", "M6-c049 (Lab 1 gives closed forms and quadrature, agreement to 1e-7, does not test integrability) and M6-c052 (agreement with each closed form does not test that the integral of |f| is finite) state the same fact with different grades. M6-c048 and M6-c053 both derive that the positive part integral is infinite from the blocks. BUILDER_RULES section 7 requires one fact per card.",
  "Merge M6-c049 into M6-c052 (keep the C basis on the lab fact only if the lab sentence is kept), and merge M6-c053 into M6-c048, or retitle one of each pair to test a different fact.")
frag = {
 "unit": "M6", "slice": "M6-b", "round": 2,
 "verifier": "independent verifier (Haiku), slice M6-b (L05-L08 and lab twins), round 2; did not build M6",
 "pin": "e22feb3", "base": "none",
 "checkout": "/tmp/verifyC2-M6-b", "scratch": "/tmp/M6-v/M6-b",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "verdict": "FAIL",
 "rows": rows, "mutants": [], "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Round 2 re-verified every page of the slice; no round-1 PASS row is carried because every slice file changed between 55b5634 and e22feb3.",
  "Mutation testing is not applicable to lesson slices (architect ruling); no grader in this slice.",
  "Not checked: live reads of Williams 1991 and Billingsley 2012 (the pages do not cite them; the curriculum sources were read only as yaml lines 287-288); pytest over the whole test suite (run_labs and page_smoke cover the twins); hours pace (architect ruling)."
 ],
 "summary": {}
}
frag["summary"] = {"rows": len(rows), "pass": sum(1 for x in rows if x["status"]=="PASS"), "fail": sum(1 for x in rows if x["status"]=="FAIL"), "unverifiable": sum(1 for x in rows if x["status"]=="UNVERIFIABLE")}
json.dump(frag, open("/tmp/verifyC2-M6-b/ledgers/M6/M6-b.json","w"), indent=1, ensure_ascii=False)
print(frag["summary"])
