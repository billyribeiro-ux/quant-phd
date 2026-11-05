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
