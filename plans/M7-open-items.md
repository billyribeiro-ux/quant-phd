# M7 open items

Written by Builder E (project, grader, project labs). Items for the architect or for other builders. Nothing here is
a learner-facing statement.

## Builder E (project, grader, project labs)

1. **Deviation from plan §7.1 item 3 (lab-M7-project-3).** The plan says this lab "runs the reference's certificate on
   one seed". The lab twin's code is published on the project page, and `grader/reference.py` must not ship (plan T6).
   A seed-0 answer printed on the page would also be the hard-coded answer that mutant m05 represents. Built instead:
   a certificate checker, with the four residuals of the page restricted to the budget and the bounds, applied to the
   Lab 1 answer and to two wrong variants. Architect to confirm or choose another route.
2. **Interface (plan §14 Q4).** Frozen as written on the page: `allocate(instance)` takes the decoded case (the JSON
   payload of `make_instance(seed)`, not the `make_instance` output). Field names: `gamma`, `mu`, `sigma`, `w0`,
   `lower`, `upper`, `sector`, `sector_caps`, `turnover_limit`. Output: `weights`, `multipliers` (keys `budget`,
   `lower`, `upper`, `sector`, `turnover_plus`, `turnover_minus`, `turnover_total`), `certificate` (keys
   `primal_residual`, `stationarity_residual`, `dual_residual`, `complementary_slackness`). Architect to confirm
   before the verifier writes the five alternative solvers.
3. **Objective check (plan §7.3).** The plan's "objective equals the reference optimum" needs an oracle inside the
   suite, and the suite cannot import the reference (it is not shipped). The suite therefore certifies optimality by
   the KKT certificate and the sufficiency proposition on the page (proved there), plus feasible comparators. Architect
   to confirm this replacement.
4. **Exception types (plan §7.4.1).** `ValueError` is required for every condition the page names (each has a test,
   refused and accepted at its boundary). Other invalid input (wrong type, boolean, text, None) is accepted with any
   exception that carries a message. The reference raises `TypeError` for wrong types.
5. **Five alternative implementations (plan §7.4.2, Q7).** Not written by Builder E, by design. The verifier writes
   them under `ledgers/M7/scripts/`. The suite is written to accept any method that meets the stated tolerance
   (1e-8 absolute on each residual, 1e-9 on the start checks and on the certificate agreement).
6. **Numeric policy (Q6).** The case stores decimal inputs (at most three digits after the point) as JSON floats. The
   reference reads each float through `Fraction(repr(x))`, so its arithmetic is exact. Other solvers use floats.
7. **Pyodide timing not measured.** Local runs: the reference passes seeds 0 to 49 in about 1 second each at most
   (`run_graders.py` slowest 0.9 s to 1.2 s). Per-test time in Pyodide (plan limit 5 s per test, 60 s per suite) is
   not measured here; `page_smoke.py` is the place to check it.
8. **Reading list.** Both registry keys from the curriculum sources are listed without any claim about their
   content (`boyd2004convex`, `stokey1989recursive`). Plan §9.1 allows this; the verifier should confirm that no
   locator is needed.
9. **Cross-page dependencies on other builders.** The project page assumes: `index.html` declares
   `data-hours-project="33"` and `data-hours-lessons="77"` and links `project.html`; lesson pages exist with the
   concept ids the project links to (`envelope-theorem` in M2, a prerequisite, is linked through
   `../../../concepts.html`). `check_pages --unit M7` reports `cards.json is missing` (Builder F).
10. **Mutants.** Ten student-error mutants in `ledgers/M7/mutants/`, generated from the reference by a script kept
    in `/tmp/m7scratch` (not in the repository). Each is a single change. All are killed by `mutate_graders.py --unit M7
    --seeds 0-9`. If the reference changes, the mutants must be regenerated; the script is not part of the repository.

## Builder F (cards.json, L01 to L08): items for the architect and the lesson authors

Written by Builder F. Each item cites the lesson text and the lab code it concerns. Nothing here is a learner-facing statement.

1. L02, the Lab 1 quiz answer (Section 8): "3.2181… to four places" for λ = 177/55. The value is 3.218181…, which rounds to 3.2182 at four places; 3.2181 is a truncation.
2. L05, Proposition 3.4: "F is convex, that is, for x, y in F the midpoint is in F". This defines convexity of F by midpoints only, while L01 Definition 1.1 requires every λ in [0, 1]. The proof uses only the midpoint, so the statement is true as written under either definition, but the words "convex" and "that is" disagree.
3. L06, Lab 1 hypothesis and lab docstring: "enumerates the 16 sets of assets fixed at zero". The code (tests/labs/M7/lab-M7-L06-1.py, nonnegative_candidates) skips the all-fixed mask (`if not free: continue`), so 15 candidate sets are evaluated. Either the text says 15, or the code evaluates the all-zero set (which has no budget solution).
4. L04, Lab 2 docstring: "for the two-asset problem of Lab 1". Lab 1 is the L03 lab, and the L04 page calls its own lab Lab 2. Harmless, but ambiguous.
5. L07, Remark 1.3 uses A(s) = (0, 1), an infinite action set, although Definition 1.1 requires finite A(s). The remark says so explicitly; no change is requested unless the architect wants the remark moved out of the definitional flow.
6. Card grading note: the L03 and L04 Proposition 3.2 cards are graded C and cite boyd2004convex with no locator read, as the pages do. No registry change is requested.
7. Card coverage: 159 cards for L01 to L08 (L01 16, L02 19, L03 20, L04 17, L05 24, L06 24, L07 21, L08 18). Each definition, theorem, proposition, lemma, remark that the key-results table cites, each misconception and each key-results row has at least one card.
