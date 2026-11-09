# Architect rulings for the final verification round (binding for fixers and verifiers)

1. **Registered macro `\R`.** Real numbers are written `\R` (BUILDER_RULES 3.1, notation/notation.json). All `\mathbb{R}`
   in module pages was replaced by `\R` mechanically.
2. **Ids of cards need not be sequential.** check_pages does not require it. Gaps and out-of-order appended ids are not defects.
3. **M3 and M4 vocabulary (M3 plan B1, option a).** M3 uses the words correlation, covariance, variance, standard deviation
   and Gaussian as plain prose without a link, because their M4 concepts are outside M3's prerequisite closure. The project
   title "Covariance-matrix doctor" is accepted. A verifier must not fail M3 for this.
4. **grader/reference.py deployment (BLUEPRINT 400-401).** The repository has no deploy step yet (only CI). The rule applies
   when a deploy step is added and is recorded for the owner. It is not a defect of any module and must not fail a slice.
5. **FC1 project scope.** The binding architect decision for FC1 limits the project to cash instruments (a bond and a trade
   that settles later). The curriculum source brief for FC1 was edited to match; futures, swaps and options belong to FC2.
6. **E3 project estimates kappa.** The logit choice model needs a choice-sensitivity parameter, so the project estimates
   kappa alongside gamma and lambda. This needs no curriculum scope change. State on the page that kappa is the choice-noise
   scale that the likelihood needs.
7. **E3 exemplars are excerpts** (see plans/E3-open-items.md).
8. **E3 plan 6.5 items 6, 7, 9** are not applicable (see plans/E3-open-items.md).
9. **Mutants.** A mutant that survives and violates a behaviour stated on the page must be killed by a new grader test. A
   mutant that differs from the reference only where the page states nothing is moved to `ledgers/<UNIT>/equivalent/` with a
   README proof. Never leave a survivor in `ledgers/<UNIT>/mutants/`. The first docstring line of a mutant names the student error.
10. **Alternatives.** Every project grader needs five correct alternative implementations of different styles that pass
    seeds 0-49 (E3: seeds 0-9 because of run time). A float-based alternative that is wrong on a stated exact rule is a mutant, not an alternative.
11. **Rung 2 completion labs.** The twin's docstring "Rung 2 completed solution" with the page showing the same program with
    `___` blanks is the established convention of the program (M1, merged, and every module since). It is not a defect.
12. **M3 concept `level-slope-curvature`.** L08 labels principal directions of simulated yield changes and defines no yield-curve
    factor, so the registered concept name was changed in `curriculum/01-foundations.yaml` to "Level-like, slope-like and
    curvature-like principal directions" (the id is unchanged) and the generated outputs were regenerated.
13. **T versus C for worked values.** A value that the page derives by hand in a numbered Example (with its hypotheses) is
    graded T with the Example as basis, even when a lab also prints it. A value that appears only in lab output, or that
    rests on SIMULATED data the page does not derive, is graded C naming the lab. A card and the key-results row it mirrors
    carry the same grade and basis.
14. **Honest-pending definitions.** A concept whose definition waits for a source that is not admitted may carry a visible
    "definition pending" dfn (LX1 L04, `bretton-woods-system`), with the model the lesson does define stated separately. This is
    an explicit honest-pending state and is not a defect. It ends when the source is admitted.
15. **Blind exemplar scoring.** A verifier extracts the memo prose of each exemplar with a script that drops the annotation
    elements, the verdict lines and the `data-score(s)` attributes, scores that prose by the rubric descriptors, and only then
    compares with the official scores. The page keeps its annotations for learners; they are not moved out of the HTML.
16. **LX1 notation.** `P_t` is the price level of L02, L03 and the project. L01's observed asset price is `A_t`.
17. **E4 stop-rule and midpoint variants.** The E4 page requires the reported root and gap to lie within 1e-10 of the oracle.
    The stop rule and the midpoint report described on the page are the reference's own convention. A variant that differs only
    inside the 1e-12 stop tolerance (mutant_r6_08, mutant_r7_01, mutant_v9_02) is therefore indistinguishable at the stated accuracy
    and is not a student error: it lives in ledgers/E4/equivalent with this ruling as its proof. The page says so in one sentence.
18. **Retired alternatives.** Rows about alternative files that no longer exist (alt_r8_*, alt_v9_*) are retired; the current
    alt_1 to alt_8 are the verified set.
19. **M7 alternatives.** M7's grader accepts any allocation that satisfies the KKT conditions stated on the page. An alternative
    whose primary method is a different solver (projected gradient, ADMM, interior point, dual ascent) and which returns its
    answer only after an exact KKT check, falling back to the active-set search otherwise, is a valid alternative of a different
    style. Rows that ask for a "different method" are satisfied by the four front-end solvers in ledgers/M7/scripts/M7-d-r12fix.
20. **Process safety.** Agents never kill processes by pattern (no pkill, no killall).
21. **SC1 plan sections 5.5 and 5.7(4).** The built page and grader are authoritative. Plan 5.5 is amended: the one-step
    estimate is checked against tail/2 within 5 target standard errors plus 1/N, and the grid estimate is checked one-sided
    (estimate at most the continuous tail plus the band), because the grid bias is never negative. Plan 5.7(4) is replaced:
    the page states that a different draw order fails the tests, so a Box-Muller alternative on another order cannot be valid.
    The five alternatives are the verified same-order set (alt_r17_*); the draw-order statement and its two tests stay.
22. **Tolerance versus stated accuracy (E4-d).** The page's stated agreement is binding on the grader: where the page says
    1e-14 for the gap, the three listed comparisons use 1e-14 * max(1, |expected|). A mutant that then still survives and
    differs from the reference only inside a stated tolerance is equivalent and goes to ledgers/E4/equivalent with its proof
    (ruling 9). Equivalent-mutant proofs always live in ledgers/<U>/equivalent/ with a README, never only in scripts/.
23. **Blind scoring is done by a dedicated scorer.** A verifier who has read the exemplar annotations cannot be blind. Blind
    scoring of rubric exemplars is a separate agent that never opens the project page: it runs a stripping script over the
    file and reads only the script's output.
24. **E4 mutant_v17_02 is not equivalent.** It differs from the reference by up to 1.57e-14 over the page's whole domain
    (sd down to 1e-50), which exceeds the page's stated 1e-14 gap precision, so it is a student error. It returns to
    ledgers/E4/mutants/ and the grader gains a test that computes the exact Proposition 3 gap from the Proposition 1
    coefficients at a domain point where the mutant misses. The equivalence section in ledgers/E4/equivalent/README.md is
    retracted. literal_price_sign stays equivalent: its sign is unobservable in any output (b_u enters only as b_u*b_u), the
    proof stands, and ruling 9 already provides the equivalent/ path for it.
25. **Mutants that differ only below the stated accuracy.** A mutant whose every output stays within the page's stated
    accuracy of the reference on all inputs searched (E4 mutant_r19_02: worst gap error 8.5e-15 against 1e-14 over 77,194 interior
    points) cannot be separated by any test the page justifies. It goes to ledgers/<U>/equivalent/ with a README section that
    states the sweep as evidence and says plainly that the bound is measured, not proved (ruling 9). Contrast ruling 24, where
    a point beyond the stated accuracy was found, so a test was added. A verifier does not author further mutants that
    sit at the tolerance boundary; new mutants are student errors that a learner could plausibly write.
26. **Convergence policy.** Fresh verifiers find new, mostly small defects every round (strict sweep of the older slices:
    107 rows, then 64, then 81), so verification alone does not reach zero. Rule: a slice is accepted when a verification round
    returns no row of these kinds: a false or unproved mathematical statement, a missing hypothesis, a wrong number, an
    over-graded claim, a failing gate, a surviving non-equivalent mutant, a lab statement the code does not support. For the
    older slices (tag S) round 4 is the last full verification; every row it returns is fixed and the unit gate re-run, but
    the slice is not verified again. Rows still open at that point, and any LOW row (wording, presentation, card style)
    deferred by a fixer, are listed in plans/KNOWN-ISSUES.md with their ledger ids so that nothing is hidden.
27. **E3 whole-cent ties under CRRA.** The half-up rule on the page holds exactly for the lottery tasks whose certainty
    equivalent is computed in exact arithmetic. For CRRA with gamma != 0 the certainty equivalent is a floating-point number, so
    an exact tie (for example gamma = 1/2 with a rational certainty equivalent) may be rounded to either neighbour. The page
    says so in one sentence; the grader accepts either neighbour on such a tie and requires the half-up result everywhere
    else. The tie mutants (f05, m06, r13n01, w05) stay in equivalent/ with a README proof amended to this scope.
28. **E3 gamma clamps and dead stall branch.** The page states the estimator's domain as gamma in (0,1). First try to build
    fixtures with gamma_hat above 0.999 and below 0.001 (a simulated participant with very low noise) and add a
    local-maximum test; if the reference estimator converges there, mutants r11_03 and r12d_03 return to mutants/ and are
    killed. If it does not converge there, the page states the supported range as [0.001, 0.999] and the mutants stay in
    equivalent/. A branch no input can reach (e12_03, negligible step) is dead code: delete it from the reference and delete
    the mutant, with a README line saying so.
29. **E3 notation.** One meaning per symbol across E3: rename the L01 mixture weight (tau), the L03 affine constant (eta),
    the L01-L03 affine-transform utility (v, to \tilde u) and the L05 EIS (epsilon, to psi) to symbols that appear nowhere
    else in E3 (grep pages, cards and twins first); update lessons, lab twins (re-embed), and cards together. Do not use
    "convex/convexity" as a term in L06: state u'' >= 0 as L02 states concavity. Forward-premise orderings in L03, L07 and
    L08 are LOW and go to plans/KNOWN-ISSUES.md.
30. **Delta verification closes a fixed slice.** Ruling 26 stopped full re-verification, but a ledger can read PASS only
    when a verifier sets every row to PASS. The closing step is therefore a delta verification: the verifier starts from the
    last full fragment, re-verifies from scratch every non-PASS row and every row whose subject changed in
    `git diff <pin of that fragment>..HEAD`, carries every other row with its evidence under the carry prefix of the
    verifier rules, and does not hunt for new defects outside those rows (observations are notes). Its fragment becomes the
    slice's ledger. A delta round that still returns a ruling-26 defect is fixed and delta-verified once more.
31. **M5 project alternatives.** The page is authoritative: its sweep is synchronous (project.html:244) and the stop rule is
    the page's. An in-place (Gauss-Seidel) sweep or a residual-bound stop changes the iteration count the tests check, so
    they are not valid alternatives of this project. plans/M5-build-plan.md lines 304-306 and plans/M5-open-items.md
    decision 3 are amended to say so; ledgers/M5/alternatives/not_accepted/ keeps the two files as documented non-accepted variants.
32. **E3 estimator range and half-up.** The stated range of the estimator is narrowed to gamma in [0.001, 0.99]: only there is
    the reference shown to reach a point that passes the local-maximum check (a fit at gamma_hat 0.994 stops on a flat
    direction). A clamp of the reported gamma at or above 0.99 is then a no-op inside the stated range, so the clamp mutants
    (r11_03, r12d_03, v15d_03) stay in equivalent/ with a README that says "none found in N trials" where it is a
    measured claim. `_half_up` is made exact (floor of the exact Fraction value plus one half) so that the tie mutants
    differ from it only at exact ties; the four tie files are regenerated from the current reference and the README
    states exactly that difference set. The page says the range in one sentence.
33. **E3 notation letters.** One meaning per symbol across E3 (ruling 29): rename the Epstein-Zin exponent a = 1 - 1/psi in
    L05 and L08 and the L06 prospect value W to letters used nowhere else in E3 (grep pages, cards and twins first);
    L01's rho is renamed too (plan 4: never rho); the Theorem 2.1 proof's tilde u in L03 becomes \check u. Re-embed the
    L05, L06 and L08 labs. The L05-L08 footers state "Each graded result carries a proof or a lab result labelled C."
34. **Free-text explanations (FC2 project).** The page states the labels an explanation must name, not its wording. Mutants
    that change only the wording (r15_a, r15_c, r15_d) violate no stated behaviour: they go to ledgers/FC2/equivalent/ with a
    README (ruling 9). The grader keeps the label-set check that kills r15_b.
