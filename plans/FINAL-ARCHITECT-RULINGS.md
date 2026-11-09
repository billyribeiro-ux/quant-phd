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
