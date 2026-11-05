import json

PIN = "00a84795f276456fce19d4181373cc4efba11a36"
BASE = "c93dd526025c6dffd34c54cd2c89eb62a890f885"
S = "ledgers/E4/scripts/E4-e-r10/"
rows = []

def row(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})

row("E4-e-r4-cards-L01", "2.7-cards-vs-lesson (fresh this round; changed cards re-read)",
    "course/modules/E/E4/cards.json E4-c001..c016, E4-c221 vs course/modules/E/E4/L01.html (text render scratch/txt/L01.txt lines 28, 72, 188)",
    "PASS",
    "c002 (changed): X(s)=x_s with Def 1.2 (L01.txt:28); P(X=x_s)=pi_s exactly when no other state has the same payoff, which is the card's content. c014 vs Remark 1.11 (L01.txt:72): lab_L01-1.out prints value_at_prices 340/3, expected 235/4, equal_to_expected_payoff False; q=(1/2,1/3,1/4,1/5) and pi=(1/8,3/8,3/8,1/8) differ in every state. c011 340/3, c012 596/3 (equal True), c013 235/4 all match lab_L01-1.out. L01.txt:188 worked value 55/3 - 25/2 = 35/6; the 'q != pi' step is the contrapositive of Proposition 1.10. Other E4-c001..c016 and c221 unchanged, carried by the same lab output.")

row("E4-e-r4-cards-L02", "2.7-cards-vs-lesson (fresh this round)",
    "cards.json E4-c017..c038, E4-c237, E4-c238 vs L02.html (scratch/txt/L02.txt)",
    "PASS",
    "Changed L02 hunk (L02.txt:219, utility -1/x): satisfies A4 (u'=1/x^2>0, u''=-2/x^3<0 on (0,inf)); its FOC pi_s/x_s^2 = mu q_s is correct; no card cites that hunk. c238 (q*.ebar = 1): Proposition 2.9 gives q*_s = pi_s/ebar_s, so q*.ebar = sum pi_s = 1, and Remark 2.10 (L02.txt:93) calls it the normalization. c030, c017, c036 byte-identical to round 9. Numbers: rederive_r9.py rerun this round, SUMMARY checks 79 failures 0 (E4-e-r10/rederive_r9_rerun.out).")

row("E4-e-r4-cards-L03", "2.7-cards-vs-lesson (fresh this round)",
    "cards.json E4-c039..c052, E4-c214, E4-c225 vs L03.html (scratch/txt/L03.txt)",
    "PASS",
    "New 'Complete preferences' paragraph (L03.txt:181) is a scope statement; no card cites it and none conflicts with it. Remark 3.5 (L03.txt:59) and proof (b) (L03.txt:~53): u_i' >= 0 by strict monotonicity, nonincreasing by concavity, and u_i'(x_t)=0 would make u_i constant on (x_t, inf), contradicting strict monotonicity, so the stated positivity holds. Example 3.6 MRS 4, 2, 1/2 recomputed from x=(9/4,9/2,9/4) with pi=(1/2,1/4,1/4). Lab 3 Part B 2 improvements, first (2,4,3),(2,4,1): run_labs PASS (run_labs_E4.out) with expected block equal to output. c225 'interior' is defined on the card only (the lesson uses 'strictly positive bundle'); accepted as a card reading of L03.txt:183.")

row("E4-e-r4-cards-L04", "2.7-cards-vs-lesson (fresh this round)",
    "cards.json E4-c053..c073, E4-c215..c218, E4-c226..c228, E4-c234..c236, E4-c239, E4-c240, E4-c248 vs L04.html (scratch/txt/L04.txt)",
    "PASS",
    "Def 1.3 (L04.txt:~23): rank(A)=dim row(A); complete iff M(A)=R^S, otherwise incomplete. c057 (rank only) and c248 (complete/incomplete) match it, and c248 is not a duplicate of c058 (Theorem 1.4 rank criterion). Prop 4.2 (L04.txt:178): C(A) convex cone, need not be R^S, counterexample I_2 and (-1,0); c069 and c228 match, and c228's cone definition matches the proof. Prop 4.1 proof (L04.txt:175) with \\indic (registered macro, notation.json) gives the J+1 independent indicators; c068 matches. Lab 1 values (c062..c065) match run_labs output. Card c226 augmented-rank wording matches Prop 1.5 (L04.txt:~26).")

row("E4-e-r4-cards-L05", "2.7-cards-vs-lesson (fresh this round)",
    "cards.json E4-c074..c099, E4-c219, E4-c229, E4-c241..c243 vs L05.html (scratch/txt/L05.txt)",
    "PASS",
    "Lemma 3.1 (L05.txt:49) now reads 'Under A1 (so that beta > 0)': c086 matches. Prop 3.2 (L05.txt:52): if varsigma < beta, convergence from every start; if varsigma >= beta and the start differs, the error does not vanish, so the intro's 'only when varsigma < beta' (L05.txt:21) is correct. Lab 1 numbers recomputed by hand: c0 path 0, 5, 15/4, 65/16 with error ratio -1/4 (c091); 0, 5, -5/2, 35/4 for varsigma=3 (c093); varsigma=2, delta=3/4 gives c0*=5/2, c1*=-3/16 (c219); error ratio -3/2 with c0*=2 for varsigma=3, beta=2 (c243); damped weight 4/5 = beta/(beta+varsigma) (c094). c099 Muth: references/references.json key muth1961rational, title 'Rational Expectations and the Theory of Price Movements' (doi 10.2307/1909635, verified_by crossref), so the title claim is registry-backed.")

row("E4-e-r4-cards-L06", "2.7-cards-vs-lesson (fresh this round; citation issue in its own row)",
    "cards.json E4-c100..c129, E4-c220, E4-c230, E4-c231, E4-c247 vs L06.html (scratch/txt/L06.txt)",
    "PASS",
    "Changed hunks: L06.txt:38 (residual = LHS - u; c106, c107): residual linear in (s,u) with no constant term, zero on a line has probability zero, so clearing a.s. forces zero everywhere: correct. L06.txt:82 Cov(v,p) = theta_s sigma_v^2 because Cov(v,u)=0: correct. L06.txt:132 Corollary 6.8 proof: Step 4 gives tau'_eta = tau_eta, so Step 2 gives E[v|p] = (tau_eta/P_U) Y and Var(v|p)=1/P_U; re-derived from Prop 6.7 steps 1-4 (L06.txt:108-121). Base instance (a=1, sigma_u^2=1/4): kappa=2, sigma_eta^2=2, tau_bar=3/4, theta_s=3/7, theta_u=6/7, b=7/9, V_U=2/3, x_I=1/7, x_U=-1/7 (hand derivation); alternative theta_s=1/2 gives residual -9/85 (hand derivation: b=49/67, E[v|p]=49/134, Var=85/134, x_U=-18/85, residual (1/2)(-18/85)); Part C 16/16 zero residuals and Part E seed 6 values match lab_L06-1.out. The Lemma 6.3 and 6.4 'by A1' citation is a separate FAIL row (E4-e-r10-L06-lemma-normality-citation).")

row("E4-e-r4-cards-L07", "2.7-cards-vs-lesson (carried from round 9)",
    "cards.json E4-c130..c150 vs L07.html",
    "PASS",
    "Carried from round 9 (course/modules/E/E4/L07.html and cards E4-c130..c150 byte-identical since c93dd52; L07 is not in the r9->r10 diff and the id-level comparison of cards.json shows no change for these ids). run_labs E4 12/12 PASS this round (E4-e-r10/run_labs_E4.out) confirms the Part F output cited by E4-c146.")

row("E4-e-r4-cards-L08", "2.7-cards-vs-lesson (changed cards fresh; unchanged cards carried)",
    "cards.json E4-c151..c188, E4-c223, E4-c224 vs L08.html (scratch/txt/L08.txt)",
    "PASS",
    "Carried from round 9 (course/modules/E/E4/L08.html byte-identical since c93dd52) for the unchanged cards c151..c180, c186. Fresh for changed cards c181..c185, c187, c188, c223, c224: 'Example 1.1' is defined at L08.txt:35 (a=2, sigma_v^2=sigma_eps^2=sigma_u^2=1). lab_L08-1.out: largest residual 1.332e-15 (tolerance 1e-12); slope 0.1595 vs 0.1605, difference 0.0010 (tolerance 0.02); Part C cost 0.15 lam*=0.657828572, gap 1.83e-15, Corr^2 0.088941; cost 0.12 lam*=1 gap 7.71e-03 (G(1)=0.127706 >= 0.12); cost 0.18 lam*=0 gap -6.71e-03 (G(0)=0.173287 <= 0.18); Corr^2 0.166667 (cost 0.12) down to 0.013061 (cost 0.17); Part D largest |gain| 0.0e+00, interior grid fractions with gain = cost: 0, lam=0 and lam=1 not equilibria. G(0)=ln2/4 and G(1)=ln(5/3)/4 recomputed. c185 (rewritten): gain is zero for every lam in (0,1] without noise (Prop 5.1(a)), and with noise only G(1)>0 is asserted, matching the caveat at L08.txt:169: the round-9 FAIL is resolved.")

row("E4-e-r4-cards-L09", "2.7-cards-vs-lesson (changed card fresh; others carried)",
    "cards.json E4-c189..c211, E4-c232 vs L09.html (scratch/txt/L09.txt)",
    "PASS",
    "c201 (changed, now covers states 1 and 4): lab_L09-1.out gives 500 strictly-positive-for-both bets at state 1 and 0 nonnegative-for-both on the meet {1,2,3}; at state 4 the same counts on {4,5,6}. c200: Example 2.4 values g1(1)=1/2, g2(1)=1/3, g1(3)=-2 (lab output, rederive_r8 rerun). c203: 625 = 5 x 5^3 bets with zero posteriors and nonnegative receipts, matching lab output 625 with 0 nonzero posterior. c205 two-prior receipts 2/5 and 1/5 (rederive_r8 rerun, 174 checks, 0 failures). c233 removed; no residual reference to E4-c233 anywhere in course/, tests/, tools/ or plans/ (grep). Carried from round 9 for c189..c199, c204, c206..c211, c232 (byte-identical).")

row("E4-e-r7-c154", "2.7-card-vs-current-lesson (carried from round 9)",
    "cards.json E4-c154 vs L08.html Assumption A3",
    "PASS",
    "Carried from round 9 (E4-c154 and L08.html byte-identical since c93dd52; per-id comparison shows c154 unchanged).")

row("E4-e-r4-banned", "2.9-banned-phrases-and-process-words (fresh)",
    "cards.json front, back and basis of all 243 cards (scratch/txt/cards_dump.txt)",
    "PASS",
    "grep -i -E 'round|verif|ruling|builder|architect|previous|revis|updated|we |our |TODO|FIXME' over the rendered dump: no process-word hits; the only hits are 'rounded' (c011), 'correct formula' (c148), and the phrase 'one seeded simulated draw' in SIMULATED cards (c146, c124, c125), which is the required labelling.")

row("E4-e-r4-check-pages", "2.9-structure-tools (fresh)",
    "tools/check_pages.py --all, tools/check_dag.py --all, tools/check_projects.py --all; tools/build_site.py --check",
    "PASS",
    "All three exit 0; E4 lines: 'check_dag E4: PASS', 'check_projects E4: PASS' and check_pages E4 PASS (ledgers/E4/scripts/E4-e-r10/check_pages.out, check_dag.out, check_projects.out). build_site.py --check: 'site data current: 6 outputs', exit 0.")

row("E4-e-r4-run-labs", "2.5-labs-printed-values (fresh)",
    "tests/labs/E4/lab-E4-L01-1..L09-1.py, lab-E4-project-1..3.py; tools/run_labs.py --unit E4",
    "PASS",
    "'run_labs E4: PASS (12/12)' (E4-e-r10/run_labs_E4.out). Each twin run as python -I -W error exits 0 (lab_L01-1.out, lab_L06-1.out, lab_L08-1.out, lab_L09-1.out, lab_project-1..3.out). pytest tests/test_labs.py -k E4: 13 passed (pytest_labs_E4.out).")

row("E4-e-r4-verify-refs", "2.1-citations-for-cards (fresh)",
    "tools/verify_refs.py --offline; references/references.json key muth1961rational (E4-c099)",
    "PASS",
    "verify_refs --offline: 'offline integrity: 560 entries, 0 problems' (verify_refs_offline.out). muth1961rational record: title 'Rational Expectations and the Theory of Price Movements', verified_by crossref; E4-c099 claim that the phrase appears in the title is registry-backed.")

row("E4-e-r4-delta", "2.7-delta-read (round 9 pin to this pin)",
    "git diff c93dd526..00a84795 -- course/modules/E/E4 (L01..L06, index.html, project.html, cards.json, grader/test_project.py)",
    "PASS",
    "10 files changed; L07, L08, L09 HTML byte-identical. Every lesson, index and project hunk read in rendered text (scratch/txt/*.txt vs round-9 renders). cards.json: 19 cards changed (E4-c002, c055, c057, c069, c086, c120, c181..c185, c187, c188, c201, c223, c224, c226, c228, c244), E4-c233 removed, E4-c248 added (python per-id comparison). grader/test_project.py: one new test. Every hunk is covered by a row below.")

row("E4-e-r7-new-cards", "2.7-new-cards (fresh)",
    "cards.json E4-c248 (new this round) and E4-c225..c247 (added since round 4)",
    "PASS",
    "E4-c248: 'When is a market with payoff matrix A complete or incomplete (Definition 1.3)?' matches Def 1.3 (L04.txt:23): complete when M(A)=R^S, otherwise incomplete. Ungraded, like the other definition cards. The E4-c225..c247 subset is covered by the rows above.")

row("E4-e-r7-ids-dups", "2.7-full-scan-duplicates (fresh)",
    "course/modules/E/E4/cards.json (243 cards)",
    "PASS",
    "python: 243 cards, 243 unique ids, no duplicate fronts, no duplicate backs. Id gaps E4-c202, c212, c213, c216, c233 are referenced nowhere (grep).")

row("E4-e-r7-grades", "2.3-grades-on-cards (fresh)",
    "cards.json grade and basis fields vs lesson result tables",
    "PASS",
    "Counts: T 153, C 19, ungraded 71 (the round-9 count of 20 C less the removed E4-c233 is 19). E4-c120 basis changed to 'Lemma 6.2 and Lemma 6.3 formulas': x_I = 1/7 uses the Lemma 6.2 demand and the Lemma 6.3 informed belief, so the new basis is right. E4-c248 is ungraded like the other definitions.")

row("E4-e-r7-numbers", "2.2-numbers-on-cards (fresh for changed cards; rederivations rerun)",
    "cards.json numbers on every changed and carried card",
    "PASS",
    "Changed-card numbers checked against lab output and hand derivation (rows E4-e-r4-cards-L01..L09 above). Rederive scripts rerun: rederive_r9.py 79 checks 0 failures; rederive_r8.py 174 checks 0 failures (E4-e-r10/rederive_r9_rerun.out, rederive_r8_rerun.out).")

row("E4-e-r7-notation", "2.7-notation-registry (fresh)",
    "E4 pages (L01..L09, project, index) vs notation/notation.json",
    "PASS",
    "Macros used on E4 pages: \\E, \\Prob, \\Var, \\Cov, \\Corr, \\R, \\Normal, \\indic. All are in the registry (\\indic\\{A\\} registered). Registered program symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q} appear nowhere on E4 pages with another meaning (grep). Lesson-local letters mu, varsigma, varpi are allowed by the registry 'about' note. The 'T' hits are data-grade attributes.")

row("E4-e-r7-c185", "2.7-card-vs-current-lesson (round-9 FAIL, re-checked)",
    "cards.json E4-c185 back; L08.html Misconception 1 answer and Proposition 5.1 text",
    "PASS",
    "Round-9 FAIL is resolved: the back now asserts G(1) = ln(5/3)/4 > 0 at Example 1.1 (lab_L08-1.out Part B 0.127706) and G(0)=ln2/4, and no longer asserts a positive gain for every lambda in (0,1]. Consistent with L08.txt:169 ('the page does not show that the gain is positive at every lambda').")

row("E4-e-r9-cards-L02-changed", "2.7-card-vs-current-lesson (changed or new cards, L02)",
    "cards.json E4-c017, E4-c030, E4-c036 (carried), E4-c237, E4-c238 (fresh)",
    "PASS",
    "Carried from round 9 for E4-c017, c030, c036 (byte-identical since c93dd52; L02 hunk at L02.txt:219 is not cited by them). E4-c237, c238 re-read this round (row E4-e-r4-cards-L02).")

row("E4-e-r9-cards-L04-changed", "2.7-card-vs-current-lesson (changed or new cards, L04)",
    "cards.json E4-c226, E4-c228 (fresh); E4-c053, c061, c066, c215, c239, c240 (carried)",
    "PASS",
    "Fresh: E4-c226 (Prop 1.5 augmented rank) and E4-c228 (convex cone; Prop 4.2) against L04.txt. Carried from round 9 for c053, c061, c066, c215, c239, c240: byte-identical, and the only L04 hunks since c93dd52 are L04.txt:21 and L04.txt:175, which none of them cites.")

row("E4-e-r9-cards-L05-changed", "2.7-card-vs-current-lesson (changed or new cards, L05)",
    "cards.json E4-c077, c093, c095, c099, c241, c242, c243",
    "PASS",
    "Carried from round 9 (byte-identical since c93dd52; the L05 hunks at L05.txt:21, :49 and :247 are not cited by them). c099 Muth title checked against the registry (row E4-e-r4-verify-refs). c243 rechecked (ratio -3/2, c0*=2).")

row("E4-e-r9-cards-L06-changed", "2.7-card-vs-current-lesson (changed or new cards, L06)",
    "cards.json E4-c121, c124, c125, c220, c244 (changed), c247",
    "PASS",
    "c244 (changed): sigma_eta^2 = sigma_eps^2 + kappa^2 sigma_u^2 >= sigma_eps^2 for every sigma_u^2 >= 0, true by inspection (Remark 6.10, L06.txt:136). c121, c220, c247 carried from round 9 (byte-identical; c247 and c220 rechecked by hand: x_I=1/7, x_U=-1/7, clearing 0). c124, c125 carried; lab_L06-1.out Part E 0.426617 vs 0.428571 (tolerance 0.006497) and 0.761928 vs 0.777778 (tolerance 0.023538) match.")

row("E4-e-r9-cards-L08-changed", "2.7-card-vs-current-lesson (changed or new cards, L08)",
    "cards.json E4-c165, c169, c245, c246 (carried); E4-c181, c223 (fresh)",
    "PASS",
    "c181 and c223 fresh (row E4-e-r4-cards-L08). c165, c169, c245, c246 carried (byte-identical since c93dd52; L08.html unchanged). Lab outputs unchanged for these: lab_L08-1.out.")

row("E4-e-r9-cards-L08-re-read", "2.7-card-vs-current-lesson (unchanged L08 cards whose cited text changed nearby)",
    "cards.json E4-c179, c182, c183, c184, c187, c188, c222, c224",
    "PASS",
    "c182, c183, c184, c187, c188, c224 changed this round: fresh (row E4-e-r4-cards-L08). c179 and c222 carried (byte-identical; G(0)=ln2/4 and G(1)=ln(5/3)/4 recomputed, and lab_L08-1.out Part B gain(0)=0.173287, gain(1)=0.127706).")

row("E4-e-r9-cards-L09-counts", "2.5-lesson-counts-on-cards",
    "cards.json E4-c201 (fresh), E4-c203, E4-c204 (carried), E4-c233 (removed)",
    "PASS",
    "c201 now covers states 1 and 4: 500 and 0 at each (lab_L09-1.out Parts B and C). c203 625 and c204 15625 = 5^6 (lab_L09-1.out: 'bets = 15625', 625 nonnegative bets with zero posteriors). c233 was removed and its content merged into c201; no reference to E4-c233 remains.")

row("E4-e-r8-rederive", "2.2-numbers-rederived (round-8 rows re-run)",
    "ledgers/E4/scripts/E4-e-r8/rederive_r8.py and E4-e-r9/rederive_r9.py run on the current cards and lessons",
    "PASS",
    "rederive_r8.py: 'SUMMARY checks 174 failures 0'; rederive_r9.py: 'SUMMARY checks 79 failures 0' (E4-e-r10/rederive_r8_rerun.out, rederive_r9_rerun.out).")

row("E4-e-r8-cited-labels", "2.7-cards-cite-existing-results (rerun)",
    "cards.json basis and text labels vs course/modules/E/E4 lesson text (scratch/txt)",
    "PASS",
    "cited_labels_scan.py cards.json scratch/txt: 'labels checked 236 not found anywhere 0' (cited_labels_r10.out). Six 'Assumption A_k' citations (E4-c054, c074..c076, c234, c235) are found as A_k inside their lesson's Assumptions block, not under the word 'Assumption'; no mismatch.")

row("E4-e-r8-lab-claims", "2.5-lesson-claims-about-labs (carried)",
    "L08.txt:155 (Part C values), L06.txt:66 (clearing at (1,0)), L07.txt:101 (Part F)",
    "PASS",
    "Carried from round 9 (these lines are outside the r9->r10 hunks; L07, L08 HTML byte-identical; L06 hunks are at L06.txt:38, 78, 82, 132, 144). Values re-run this round: lab_L08-1.out Part C; lab_L06-1.out Part C (16 zero residuals); run_labs E4 PASS.")

row("E4-e-r10-gates", "2.9-tool gates (round 10)",
    "ruff check and ruff format --check on tests/labs/E4 and course/modules/E/E4/grader; mypy --no-incremental and mypy --strict via run_graders on instance.py, reference.py, starter.py",
    "PASS",
    "ruff check: 'All checks passed!'; ruff format --check: '16 files already formatted'; mypy (3 grader files): 'Success: no issues found in 3 source files'; run_graders.py --unit E4 --seeds 0-49: 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.2 s)' (run_graders_E4.out).")

row("E4-e-r10-grader-collect", "2.6-project-test-count (round 10)",
    "course/modules/E/E4/grader/test_project.py vs course/modules/E/E4/project.html line 233 ('runs 43 checks')",
    "PASS",
    "Collect-only in a staged workspace (reference copied as solver.py): '43 tests collected'. The page says 43.")

row("E4-e-r10-grader-new-test", "2.6-new-grader-test and its docstring numbers (round 10)",
    "course/modules/E/E4/grader/test_project.py:382 test_gap_at_zero_fraction_is_the_limit_to_full_precision and its docstring",
    "PASS",
    "interior_oracle_check / docstring_gap_check.py: for the six (sd, cost) pairs, |gap(1e-12) - limit| = 1.02e-13, 1.09e-13, 1.11e-13, 3.26e-13, 3.49e-13, 3.54e-13, inside the docstring's '1e-13 to 4e-13'; max |oracle(0) - limit| = 1.110e-16, matching 'at most 1.1e-16'. The reference passes the suite on seeds 0-49 (run_graders). Alternatives alt_1..alt_5 pass too (E4-e-r10-alternatives).")

row("E4-e-r10-alternatives", "2.6-alternative-correct-implementations (round 10)",
    "ledgers/E4/alternatives/alt_1.py .. alt_5.py run as solver.py under the suite, seeds 0-49",
    "PASS",
    "alternatives_seeds0-49.out: alt_1 50/50, alt_2 50/50, alt_3 50/50, alt_4 50/50, alt_5 50/50 passed. No over-constraint from the new test.")

row("E4-e-r10-mutants-existing", "2.6-mutation (full E4 set, round 10)",
    "tools/mutate_graders.py --unit E4 over ledgers/E4/mutants (77 files, including 3 new round-10 mutants)",
    "FAIL",
    "'mutate_graders E4: FAIL (75/77 killed)' (E4-e-r10/mutate_E4_with_r10.out). Survivors: mutant_v9_02_stop_rule_relative_to_lower_end.py (row E4-e-r10-mutant-v9-02) and mutant_r10_02_cost_factor_relative_error.py (row E4-e-r10-mutant-r10-02). The round-9 survivor mutant_v9_06 is now KILLED by the new test test_gap_at_zero_fraction_is_the_limit_to_full_precision.")

row("E4-e-r10-mutant-v9-02", "2.6-mutation (survivor carried from round 9)",
    "ledgers/E4/mutants/mutant_v9_02_stop_rule_relative_to_lower_end.py vs course/modules/E/E4/project.html Constraints sentence 'stops when the bracket is narrower than 1e-12 times its upper end'",
    "FAIL",
    "Still SURVIVES seeds 0-49 (mutate run above). The page states the stop rule (project.html Constraints, L231 of the rendered page: 'stops when the bracket is narrower than 10^{-12} times its upper end, or after 200 halvings'), and the mutant violates it. The outputs differ only inside the final bracket, which the page permits, so no test observes it. Round-9 architect item E4d3-spec-stop-rule-and-constraints is still open. Fix: either reword the stop rule as an accuracy requirement (the grader already tests a 1e-12 relative accuracy claim) or add a test that observes the bracket rule (e.g. count of bisection iterations for a tiny root, which the solver's output cannot show). Architect decision needed.")

row("E4-e-r10-mutant-r10-02", "2.6-mutation (new survivor, round 10)",
    "ledgers/E4/mutants/mutant_r10_02_cost_factor_relative_error.py (exp(a c) scaled by 1+1e-12 in indifference_gap) vs project.html Constraints 'works in floating point at full precision'",
    "FAIL",
    "Survives all 50 seeds of the suite's default run (killed by no test). Measured effect: the gap at fraction 0.5 shifts by -2.06e-13 (sd 0.5, c 0.12) and -2.21e-13 (sd 0.75, c 0.15) (interior_oracle_check.out). The suite has no interior-fraction gap test at a 1e-14 tolerance: the reference agrees with oracle_gap to max 9.99e-16 over 54 points (fractions 0.1..1.0, sd 0.5..0.75, costs 0.12..0.30; interior_oracle_check.out). The page promises full floating-point precision (project.html Constraints). Fix: add a test that |indifference_gap(lam) - oracle_gap(lam)| <= 1e-14 * max(1, |oracle|) at several interior fractions. The reference passes (9.99e-16 max), and the mutant fails at about 2e-13.")

row("E4-e-r10-new-mutants", "2.6-new student-error mutants (round 10)",
    "ledgers/E4/mutants/mutant_r10_01_gap_zero_offset_1e-13.py, mutant_r10_03_cost_factor_missing_risk_aversion.py",
    "PASS",
    "r10_01 (gap at 0 offset by +1e-13) KILLED by test_gap_at_zero_fraction_is_the_limit_to_full_precision (seed 0). r10_03 (exp(c) in place of exp(a c)) KILLED by test_gap_is_the_oracle_gap_at_the_reported_fraction[first] (seed 0). The third new mutant r10_02 survives: row E4-e-r10-mutant-r10-02.")

row("E4-e-r10-index-claims", "2.5-labs-arithmetic-claims (index.html line 15 and line 95 hunks)",
    "course/modules/E/E4/index.html; tests/labs/E4/*.py",
    "PASS",
    "Exact Fraction arithmetic: L01 (23 Fraction uses), L02 (17), L04 (10), L05 (12), L09 (9), L03 Part A (exact; L03 twin docstring line 15 says Part B is floating point). Double precision: L03 Part B (3 float literals; line 15), L08 Parts B..D (54 float uses, Fraction count 0). Seeded simulations: one each in L06 (Part E, seed 6), L07 (Part F, seed 7), L08 (Part A, seed 20261103), each labelled SIMULATED on its page. Consistent with the index sentences.")

row("E4-e-r10-project-hunks", "2.2-numbers-on-project-page (changed hunks)",
    "course/modules/E/E4/project.html: A1 (line 185), Constraints (line 227, 231), grader paragraph (line 233), Lab 3 results (line 420)",
    "PASS",
    "Instance box: tau_bar = 2e^{-4c} - 1 (= (tau_v+tau_eps)e^{-2ac} - tau_v with a=2): tau_bar(0.150)=0.09762327, tau_bar(0.120)=0.23756678 (recomputed); tau_y(1) = 1/(1+4 sigma^2) >= 1/(1+4*0.75^2)=0.30769 (recomputed); so 0 < tau_bar < tau_y(1). instance.py draws sigma in [0.500,0.750] and c in [0.120,0.150], rounded to 3 decimals: verified. lambda* = 2 sigma sqrt(tau_bar/(1-tau_bar)) gives the Lab 3 table (lab_project-3.out): 0.5582, 0.6978, 0.8373 (c 0.120); 0.4453, 0.5567, 0.6680 (c 0.135); 0.3289, 0.4111, 0.4934 (c 0.150); informativeness 0.1920, 0.1420, 0.0889. Unrounded ratios 1.25 and 1.50 (displayed 1.2501, 1.5000). Printed gap max |.| = 3.55e-14 < 4e-14. '484 of 484' = 22 x 22 grid (lab_project-3.out). Constraint: 2^-200 = 6.2e-61, so 200 halvings end the search first when root < 6.2e-49 (about 6e-49, as stated). Page statement '43 checks' verified (row E4-e-r10-grader-collect).")

row("E4-e-r10-L06-lemma-normality-citation", "2.1-proof-citations (Lemma 6.3 and Lemma 6.4 proofs)",
    "course/modules/E/E4/L06.html line 143 (Lemma 6.3 proof: 'The vector (e, s, u) is jointly normal by A1.') and line 157 (Lemma 6.4 proof: 'is a linear image of (v, s, u), so it is jointly normal by A1')",
    "FAIL",
    "A1 says only that (v, eps, u) is jointly normal. Joint normality of a linear image of it is Assumption G(i) (L06.html line 90-91, 'A linear image of a jointly normal random vector is jointly normal'), which the proofs do not cite. The conclusion is true and G is among the hypotheses of both lemmas, so this is a citation gap, not a logic gap. Fix: change 'by A1' to 'by A1 and G(i)' in both places. Low severity.")

row("E4-e-r10-uncited-hunks", "2.7-changed-hunks-no-card (fresh)",
    "L01.txt:188 and :171, :225, :227; L02.txt:219; L03.txt:181; L04.txt:21, :175; L05.txt:21, :247; L06.txt:144; index.html; project.html",
    "PASS",
    "Each hunk read and checked: L01 worked V(x)=55/3 and the q != pi inference; L01 R1 wording (no card cites R1); L02 -1/x example; L03 scope paragraph; L04 intro and the indicator notation in Prop 4.1; L05 intro (the 'only when' follows from Prop 3.2) and the Problem solution (Psi_0(0) = 10/2 = 5); L06 Part A description matches tests/labs/E4/lab-E4-L06-1.py (closed_form(), theta_s and theta_u as exact Fractions, output line 'theta_s 3/7 theta_u 6/7'); index and project prose as above.")

mutants = [
    {"name": "mutant_v9_02_stop_rule_relative_to_lower_end.py", "description": "Bisection stop rule measured against the lower end of the bracket (round-9 mutant).", "killed_by": None},
    {"name": "mutant_v9_06_gap_at_zero_from_tiny_fraction.py", "description": "Gap at fraction 0 taken from fraction 1e-12 (round-9 survivor).", "killed_by": "test_gap_at_zero_fraction_is_the_limit_to_full_precision (new round-10 test; seed 0)"},
    {"name": "mutant_r10_01_gap_zero_offset_1e-13.py", "description": "Gap at fraction 0 offset by +1e-13 (student floating-point slip).", "killed_by": "test_gap_at_zero_fraction_is_the_limit_to_full_precision (seed 0)"},
    {"name": "mutant_r10_02_cost_factor_relative_error.py", "description": "Cost factor exp(a c) scaled by 1+1e-12 in the interior gap.", "killed_by": None},
    {"name": "mutant_r10_03_cost_factor_missing_risk_aversion.py", "description": "exp(c) used in place of exp(a c) in the gap (student error).", "killed_by": "test_gap_is_the_oracle_gap_at_the_reported_fraction[first] (seed 0)"},
]

fragment = {
    "unit": "E4",
    "slice": "e",
    "round": 10,
    "verifier": "independent verifier (Haiku 5.5), unit E4, slice e: all 243 cards in course/modules/E/E4/cards.json against L01-L09, project, index, grader (round 10)",
    "pin": PIN,
    "base": BASE + " (round-9 pin; delta " + BASE[:7] + ".." + PIN[:7] + " read in full for the E4 slice)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE10-E4-e",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE10-E4-e/scratch/txt (rendered lesson text, cards_dump.txt; not committed)",
    "verified_at": "2026-11-05T05:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: all 243 cards in course/modules/E/E4/cards.json (19 changed since c93dd52, E4-c233 removed, E4-c248 added) against the current L01..L09 text, project.html, index.html and grader/test_project.py.",
        "Carry rule: a round-9 PASS row is carried only where its cited subject is byte-identical since c93dd52 and the carry is labelled; rows whose subject changed were re-verified this round. Row ids from round 9 are all kept.",
        "Round-9 FAIL E4-e-r7-c185 is resolved. Round-9 mutant survivor v9_06 is killed by the new test. v9_02 (stop rule) remains open as the architect item.",
        "Not checked: the full 2000-line lesson HTML beyond the rendered text; the Pyodide browser run (page_smoke ran in Chromium and passed); the 50-seed run of every existing mutant (mutate_graders ran seeds 0-9, the tool default); the Muth 1961 paper itself (only the registry record was read).",
        "Alternatives were run on seeds 0-49, the same as the reference run. Mutants were run by tools/mutate_graders.py with its default seeds."
    ],
    "summary": "cards 243 (T 153, C 19, ungraded 71). Rows: total " + str(len(rows)) + ", PASS " + str(sum(1 for r in rows if r["status"] == "PASS")) + ", FAIL " + str(sum(1 for r in rows if r["status"] == "FAIL")) + ". FAIL rows: E4-e-r10-mutant-v9-02 (stop-rule survivor, architect item), E4-e-r10-mutant-r10-02 (interior gap precision survivor; add a 1e-14 interior oracle test), E4-e-r10-L06-lemma-normality-citation (A1 cited where G(i) is needed, low), and E4-e-r10-mutants-existing (aggregate of the two survivors). Mutation: 75/77 killed. Verdict FAIL."
}

with open("/Users/billyribeiro/.fanout/wt/verifyE10-E4-e/ledgers/E4/E4-e.json", "w", encoding="utf-8") as f:
    json.dump(fragment, f, ensure_ascii=False, indent=2)
print("rows", len(rows), "fail", sum(1 for r in rows if r["status"] == "FAIL"))
