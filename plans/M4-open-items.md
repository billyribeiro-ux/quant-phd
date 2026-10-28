# M4 open items (Builder A: hub, L01 to L03)

Status at writing: hub, L01, L02, L03 and labs `lab-M4-L01-1` to `lab-M4-L03-1` are built. Their checks are listed in the builder report.

1. **Normal skewness and kurtosis (Lesson 3, Remark 2.6).** The plan asks for the normal kurtosis 3 to be derived in L03. The normal density is defined by L06, so L03 cannot derive it without using an undefined concept. L03 gives a forward pointer to Lesson 6. Lesson 6 must derive E[Z^3] = 0 and E[Z^4] = 3 for the standard normal.
2. **Variance of a sum (Lesson 2, Problem P3).** The problem points to Lesson 5 for the general formula for Var(U + V). Lesson 5 must state that formula with covariance, or the pointer must change.
3. **Infinite fourth moment (Lesson 3, canon section).** The page says Lessons 6 and 10 meet laws whose fourth moment is infinite. Lesson 6 or Lesson 10 must show such a law, for example a Student-t with nu at most 4, with the hypothesis stated.
4. **Infinite variance (Lesson 2, canon section).** The page says Lesson 6 gives a Student-t with nu at most 2 that has no finite variance. Lesson 6 must state this with its hypothesis.
5. **Blitzstein locator (all lessons).** No passage from *Introduction to Probability* has been read: no copy was available to the builder. No locator or attributed statement appears on these pages. The registry record for `blitzstein2019introduction` has year 2019 and no edition field, so the curriculum's "2nd ed." is not confirmed (plan Q6).
6. **Stable-limit source (REFERENCE_REQUESTS, plan item 1).** Needed for the L10 remark on the stable limit of sample means under infinite variance. No registry key covers it. The architect must nominate a DOI or ISBN.
7. **Placement skill check (hub, rung 2).** The second skill item asks for the matched scale factor (nu - 2)/nu for nu = 5, which is 0.6. Lesson 6 must derive the Student-t variance nu/(nu - 2), so that the explanation on the hub is backed by a proof.
8. **Lesson 4 to 10 and project.** The hub links all ten lessons and project.html. The hub's hours check fails until L04 to L10 declare 9 h each (27 h of 90 h are built). `project.html` and `cards.json` are missing (Builders D and E).

## Builder B (lessons L04 to L07)

9. **Covariance before L05 (L04 §1, Definition 1.6).** L04 uses the covariance formula to state Proposition 1.8 and Example 1.9. It is defined there inline, not with `<dfn>`, because the plan puts the `correlation` concept in L05. L05 links back to it. Architect to confirm, or move the covariance definition to L04 under the concept list.
10. **Continuous extension (L05 to L06).** Propositions 1.1 and 1.5 of L05 are proved for finitely many values. L06 and L07 use the same rules for variables with densities, by linearity of the definite integral (M2) and Tonelli's theorem for multiple integrals (M2). These are cited to M2 concepts, not proved in full on the page.
11. **Student-t for positive integer nu only (L06 Definition 2.5).** The chi-square is defined as a sum of squared normals, so non-integer nu is not defined on the page. The Cauchy distribution is not defined anywhere in L04 to L07, which leaves its definition to L10 (plan Q15).
12. **Example 2.5 of L05 (explicit assumption).** The construction of the two-asset matrix assumes the rules of Proposition 1.1 for standard normal draws and the values Var(Z) = 1 and Cov(Z1, Z2) = 0. The example states this assumption and does not claim it is proved.
13. **Student-t kurtosis and MGF (not computed).** L06 Remark 2.7 and L07 Remark 1.5 say these are not computed here. Nothing in L04 to L07 depends on them.

# M4 open items (Builder D: project, grader, project labs)

Status at writing: `project.html`, `grader/` (instance, reference, starter, test_project with 45 checks), labs
`lab-M4-project-1` to `-3`, `ledgers/M4/mutants/` (11 files) and `ledgers/M4/scripts/` (five alternatives, the generator
and the runner) are written. Checks are listed in the builder report.

1. **Sign convention is untestable under the frozen interface (CONTRACT_CHANGE_REQUEST, plan §5.3 test 2 and mutant 5).**
   `simulate_losses` has no mean-return input. Both laws are symmetric, so \(-R\) has the law of \(R\), and a sign flip
   leaves the loss distribution unchanged. Mutant `m11_loss_sign_flipped` SURVIVES (10 of 11 killed). The page says so
   under "What the suite does not test". Fix needed from the architect: an optional mean-return argument, default zero,
   so the sign test "long position with positive mean gives negative mean loss" can run.
2. **Test 1 measures the loss variance, not the return covariance (plan §5.3 test 1).** The frozen functions return
   losses only, so the test checks \(\operatorname{Var}(\ell) = w^{\top}\Sigma w\), which equals the return-covariance
   statement for a fixed portfolio. Recorded as a deviation from the plan's wording.
3. **Student-t variance tolerance is 0.60 (plan gave no value).** Measured on seeds 0-49 with five correct streams, the
   largest relative error is 0.52 at nu = 3 and 0.31 at nu = 4. The test therefore sees an inflation \(\nu/(\nu-2)\) only
   above 1.6 times, that is nu of 5 or less. A correct student at a seed outside 0-49 could still exceed 0.60 at nu = 3,
   a false failure whose rate was not measured beyond seed 49. Architect to decide (for example, a per-seed check with a
   larger draw count, or a robust statistic), or accept and keep the page statement.
4. **Five alternatives are not run by any listed command (plan §Tooling 1, Q9).** They live in `ledgers/M4/scripts/alt_1..5.py`
   and are run by `ledgers/M4/scripts/run_alternatives.py --seeds 0-49` (6 implementations, all pass 50/50 seeds). Q9
   asks for a pytest module under `tests/`; the architect should choose the location.
5. **Mutants written by the builder (plan §5.6 says the verifier writes them).** The orchestrator asked the builder to
   write ten student-error mutants; they are generated by `ledgers/M4/scripts/make_variants.py` from the reference, one
   substitution each. The verifier should review the set and may add its own.
6. **Lab 3 is stream-free (plan §Rung 3 said the report must print the same lines as the student's module).** Five correct
   implementations draw differently, so no sampled number can be required to match. Lab 3 prints closed forms only; the
   report quotes its own sampled numbers with the seed.
7. **Reading list cites `blitzstein2019introduction` with no locator and no attributed statement.** No passage has been read.
8. **Rung 4 stretch items are not graded and state no result.**

## Builder C (lessons L08 to L10)

14. **Plan error: Student-t(3) has finite variance (L10, curriculum lab).** The plan (§Lesson content guidance, L10) says that for Cauchy and Student-t(3) the sample mean does not settle. Student-t(3) has variance \(\nu/(\nu-2) = 3\) (Lesson 6), so only the Cauchy law (no mean) fails the mean and variance hypotheses. L10 follows the mathematics: t(3) is heavy-tailed (Proposition 1.5) with finite variance 3 (Remark 2.2) and infinite fourth moment (Proposition 2.3). The architect must confirm the revised L10 statement and the lab's Part C reading.
15. **Lesson 9 proofs cover finitely valued laws only.** Every law in L09 takes finitely many values, so Chebyshev, the weak law and the characteristic-function step are proved in full. Statement 2.5 (the CLT in the distribution-function sense) is a reduction: Steps (i) (the normal characteristic function \(e^{-t^2/2}\)) and (ii) (convergence of characteristic functions implies convergence of distribution functions) are named, not proved, not cited and not graded. Architect to decide whether a read source with a locator is admitted, or the statement stays a reduction.
16. **Stable-limit remark (L10 Remark 2.5).** The Cauchy sample mean has the standard Cauchy law for every \(n\). Stated without a source and without a grade, as directed. This is REFERENCE_REQUESTS item 1 of the plan; no registry key is proposed.
17. **Cross-lesson ids used by L08 to L10 (Builder B must match).** `L04.html#def-independence`, `L05.html#def-covariance-matrix`, `L06.html#def-normal-distribution`, `L06.html#def-student-t-distribution`, `L07.html#def-characteristic-function`, `L07.html#def-moment-generating-function`. Facts relied on: Lesson 6 standard normal mean 0 and variance 1, the normal MGF \(e^{s^2/2}\) at \(\mu = 0\), the Student-t variance \(\nu/(\nu-2)\) for \(\nu > 2\), and the Student-t density at \(\nu = 3\), \(\frac{2}{\pi\sqrt3}(1 + t^2/3)^{-2}\). Lesson 4: factorization of expectations for independent variables. If any of these differs in the final B pages, L08 to L10 must change with it.
18. **Cauchy law defined in L10 by its density** (Definition 1.2), not by the ratio of normals (plan Q15 preference) and not in L06. The distribution function is derived in Proposition 1.3.
19. **Multivariate normal density quoted, not derived (L08 Definition 2.1, Remark 2.2).** The change-of-variables step is not stated. No result on the page uses the density. Architect to decide whether the quoted density stays.
20. **Lab-observed results carry no grade.** Lab output (L08 Part B, L09 Parts A to C, L10 Parts A to D) is labelled as simulation output in the key-results tables and is not graded. Rule 3 (a grade-C span needs a registry key) and the plan's grading scheme do not give a keyless grade for a single-run result. Architect to confirm.
21. **Blitzstein not read (all three lessons).** No locator is written and no statement is attributed to it. The references section says so, as in L03.

## Builder E (cards, L01 to L10)

Status at writing: `course/modules/M/M4/cards.json` has 163 cards (M4-c001 to M4-c163), between 13 and 20 in each lesson. No card cites a registry key, because no Blitzstein locator was read. Cards for lab output are grade C with a basis naming the lab. Cards for the lessons' own proofs and examples are grade T.

10. **Normal kurtosis claim (L03 Remark 2.6 and misconception 2).** The text says Lesson 6 derives the normal skewness 0 and kurtosis 3. Lesson 6 contains no such derivation (`grep` for kurtosis and skew finds only Remark 2.7, which says the Student-t kurtosis is not computed). No card states the normal kurtosis. Lesson 6 or Lesson 3 must change, and item 1 above stays open.
11. **Lesson-text numbers on the cards.** Every number on a card was checked to appear in its lesson text (the check passed for all 163 cards). Cards follow the lesson text as it stood when read; a later lesson edit requires the affected card to be re-read.
