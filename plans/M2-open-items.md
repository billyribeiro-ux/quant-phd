# M2 open items (Builder D: lessons L19 to L24)

Items that need an architect decision, a sibling builder's output, or a registry action. Not learner text.

## Dependencies on other builders' pages

1. **L09 must state the one-variable Riemann-sum convergence used in L20 Theorem 1.2.** L20 needs that Riemann sums of
   \(x\), \(x^2\) on \([0,1]\) and of \(y\) on \([0,2]\) converge to their integrals for every choice of tags as the mesh
   tends to 0. L20 cites this as "the result of Lesson L09 for continuous functions". Check L09 states it with arbitrary tags.
2. **L08 must prove or state the Lagrange form of Taylor's theorem with remainder of order 1, 2 and 3.** Used in L19
   Proposition 3.3, L23 Theorem 3.1 and Proposition 3.3, and L24 Propositions 3.1 and 3.2. L08 must define
   `def-taylor-theorem` (the L19, L23 and L24 links point to `L08.html#def-taylor-theorem`).
3. **L04 must define `def-derivative`, L09 `def-definite-integral`, L13 `def-finite-difference-derivative`, L16
   `def-partial-derivative`, L17 `def-gradient`, L01 `def-limit`.** The L19 to L24 links point to these ids.
4. **L14 must describe forward-mode automatic differentiation.** L24 Research R3 says "forward-mode automatic
   differentiation is defined" in L14.
5. **gradient (L17) and jacobian (L18) are not defined in this worktree.** `check_dag.py --unit M2` reports both as
   "introduced by M2 but never defined", which is Builders C's output, not mine. My pages use neither as a dfn.
6. **The hub (index.html, Builder A) must link L19 to L24 and set `data-hours-lessons`.** The six lessons are 10 h each,
   so with L01 to L18 at 10 h the lesson total is 240 h, matching the hub's 240.

## Architect decisions taken on the page (please confirm)

7. **L20 Fubini.** The architect's Q3 says the Fubini statement is hypothesis-stated, without proof and without a locator.
   I named it in Remark 2.3, said it is not proved, gave it no grade and no `<dfn>`, and used it nowhere. The alternative
   is to state it with a hypothesis and no grade. Confirm.
8. **L21 existence part of the implicit-function theorem.** Assumed result 1.2 is assumed, not proved, with no grade and no
   citation. The derivative formula (Theorem 2.1) is graded T given the assumption.
9. **L23 duration and convexity.** The plan (§0 Q8) puts these in `03-markets.yaml`, module MKT. `curriculum/curriculum.json`
   gives the concepts "Macaulay and modified duration" and "Convexity" module FI1, not MKT. L23 names them only in the
   lab's docstring and the meta description as a preview, with no dfn and no link. The problem title "Convexity of the
   price" was renamed to avoid the bond term. Confirm the module discrepancy is for the architect's curriculum notes.

## Registry

10. **No registry key is cited by any graded span on these pages.** `spivak2008calculus` and `hubbard2015vector` are named
    as sources in each References section, with no locator, because no locator has been read or confirmed. Two gaps follow:
    (a) a REFERENCE_REQUEST for a confirmed locator of the implicit-function theorem, Taylor's theorem with remainder and
    the Schwarz symmetry result, from either Spivak or Hubbard, so that Assumed result 1.2 (L21) can be graded T by citation;
    (b) neither record carries an edition field, as recorded in the plan's Q14.

## Hypotheses stated on the pages, not measured

11. **L24 round-off model.** Definition 4.1 assumes an error of at most \(\delta\) in each evaluation of \(f\). The L24 lab
    uses \(\delta = 2.22 \times 10^{-16}\) and \(M_2 \approx M_3 \approx e\) to predict minimizers; neither is measured.
    The lab prints only the true errors on a decade grid.

## Lab results with limited scope

12. **L22 golden-section accuracy.** The printed maximizer is off by about 1e-8, the square root of machine precision, because
    the objective is flat at its maximum. The lab's Part A statements rely on this printed limit and say so.
13. **L23 integer cents.** The rounding of the price is half-even on a float, and the lab's \(P'\) and \(P''\) are floats.
    The lab uses one SIMULATED bond with fixed cash flows.

## Not mine

14. **Grader and project (Builder E), cards (Builder F).** Not written by Builder D. `cards.json` must cover L19 to L24
    (quiz data-cards="cards.json" on each of my pages).
15. **Mutants and ledgers.** Not written by Builder D.

---

# Builder A: hub (index.html) and lessons L01 to L06

Requests and gaps under the BUILDER_RULES §10 contract. Each item is a gap the pages state, or work for the architect or a later builder.

## DATA_REQUESTS
None. The unit embeds no dataset; the labs compute exact rationals or closed forms.

## REFERENCE_REQUESTS
None. `spivak2008calculus` and `hubbard2015vector` are registered and verified. No statement is attributed to either, because no passage locator has been read. The hub's core reading and each lesson's References section say so.

## NOTATION_REQUESTS
None. Only standard KaTeX commands are used.

## GLOSSARY_REQUESTS (terms defined in the text, without a `<dfn>`)
- sequence (L01 §1)
- continuity, in the sequential form used in M2 (L02 §2); the epsilon-delta form is M5's concept and is not used here
- open interval; the limit of a function, Definition 1.1 (L03 §1), which keeps the L01 meaning and adds no concept
- one-sided limits, Definition 2.1 (L03 §2)
- difference quotient (L04 Definition 1.1)
- local maximum, local minimum, local extremum, critical point (L06 §1)
- nondecreasing, increasing (L06 §3); Lipschitz (L06 Problem R3, prose only)

## CONTRACT_CHANGE_REQUESTS
None. M2 has no Atlas milestone.

## DAG_DEFECTS
- None in L01 to L06 or the hub. `limit` is defined in L01 (`def-limit`) and `derivative` in L04 (`def-derivative`).
- Unit-level `check_dag.py --unit M2` at the last run reported `gradient` and `jacobian` as introduced but not yet defined. Those belong to the lessons that define them.
- Name collisions avoided by Architect decisions Q5 to Q7: no page names or links `epsilon-delta-continuity`, `riemann-stieltjes-integral`, `lebesgue-integral`, `lagrange-multiplier` or `fubini-theorem`.

## KNOWN_LIMITATIONS
- **Grade-C lab results carry no registry key.** The rule "a grade-C span needs a registry key" conflicts with the M1 and AC1 convention and with the lesson rule that a lab result is graded C naming the lab. Builder A follows the convention: each lab result is a grade C whose basis is the named lab. No key is cited, because no registry source supports a lab's output. The architect should decide.
- **The extreme value theorem is assumed (L06 Fact 2.1).** Its proof uses the completeness of the reals, which the unit does not construct. Theorems 2.2 and 2.3 list it as a hypothesis, and it carries no grade.
- **Lemma 1.1 (L05) is proved by reference to L02 Proposition 1.1,** with the substitutions stated on the page. A written-out version would be longer.
- **Continuity is sequential (L02 §2).** The epsilon-delta equivalence is not proved.
- **The placement skill items test material taught later:** the difference quotient (L04) and the central-difference expansion (L05), as the hub says.
- **P0.1 is not yet released,** so the P0.1 links open "not yet released" entries, as in M1.
- **Hub hours check** reported `lessons declare 210 h; the hub says 240 h` at the last run. The check passes once all 24 lesson pages declare 10 h each.
- **cards.json is missing.** Builder F writes it after Builders A to D.
- **Labs.** Each twin uses the Python standard library only (`fractions`, `math`, `itertools`, `collections.abc`). Five of six use exact rational arithmetic; L05 uses floats for central differences. None is a simulation, so none carries a SIMULATED label. Pyodide was exercised only through `page_smoke.py`.
- **Quiz wrapping at 360 px.** Each lesson sets `min-inline-size: 0` on its quiz fieldsets, and L02 and L06 also set `flex-wrap: wrap` on their option labels. Without these, math inside an option overflowed 360 px, because `label.option` is a flex row in `course.css`. These are inline styles, not a change to the shared stylesheet.


## Builder B: lessons L07 to L12 (Architect review)

Items that need an architect decision, a sibling builder's output, or a registry action. Not learner text.

1. **Lab function in L07 is 1/(1 - x), not exp.** The plan's row (`curriculum/01-foundations.yaml` lab, and M2-build-plan
   section 3) says "Taylor polynomials of exp at 0". The derivative of exp is not established in the prerequisite closure
   (M1 pages contain no derivative of exp), so L07 uses 1/(1 - x), whose derivatives are proved in Proposition 1.4. Decision
   needed: keep 1/(1 - x), or state exp' = exp as an assumed fact.
2. **L20 cites L09 for continuous functions; L09 proves the monotone case only.** L20 (Builder D, Theorem 1.2 input) says
   "the result of Lesson L09 for continuous functions". L09 Corollary 2.3 proves that every Riemann sum of a monotone f
   with mesh delta lies within delta times |f(b) - f(a)| of the integral, for every choice of tags. That covers x, x^2 on
   [0,1] and y on [0,2], so L20 should cite Corollary 2.3, not "continuous functions". Continuity-based integrability is
   not proved anywhere in M2 pages of this batch.
3. **Mean value theorem and extreme value theorem (L06 dependency).** L08 Theorem 1.2 (Rolle), L10 Theorem 1.2 (mean value
   theorem) and L11 (via L10) use the mean value theorem "from Lesson 6". L06 takes the extreme value theorem as an assumed
   fact. L06 must state the mean value theorem with hypotheses: continuous on [p, q] and differentiable on (p, q). L08 and
   L10 say so explicitly.
4. **Chain and product rules (L05 dependency).** L07 Proposition 1.4, L10 Example 2.2 (quotient rule), L11 Theorem 2.1
   (product rule) and Theorem 3.1 (chain rule) need these rules stated in L05 with hypotheses. Differentiable functions are
   continuous (L04) and the limit laws are in L02; L11 and L12 cite both.
5. **Forward pointers from L09 to later lessons.** L09 Misconception 2 cites L10 Theorem 2.1 (fundamental theorem) and
   L11 Lemma 1.1 (linearity) by name. These are prose pointers, not concept links. Each named result exists in L10 and L11
   as written (checked on these pages).
6. **Cards (Builder F).** cards.json for L07 to L12 is not written by this builder. Cards should cover: Definition 1.1 and
   1.2 (L07), Proposition 1.4 and Theorem 2.1 (L07 and L08), Theorem 2.1 (L08, Taylor's theorem), Theorem 2.2 and Corollary
   2.3 (L09), Theorem 2.1 (L10), Theorem 2.1 and Theorem 3.1 (L11), Theorem 2.2 and Theorem 3.3 (L12). Each lesson's
   quiz has 9 to 10 items, so each lesson needs cards.
7. **Hours.** Lessons L07 to L12 each declare 10 study hours (60 h for this batch). The hub split is the architect's.
8. **Prose terms, not registered concepts.** Taylor polynomial (L07 Definition 2.1), partition, mesh, upper and lower sum,
   Riemann sum, monotone function (L09), antiderivative (L10), improper integral (L12). These are plain prose per the
   architect's Q7 decision. Decide whether any needs a GLOSSARY_REQUEST.
9. **Registry.** No registry key is cited in L07 to L12. No REFERENCE_REQUESTS are needed for these lessons.
10. **Data.** No dataset is used. Lab 1 in L11 and L10 uses midpoint quadrature and a central difference in floating point,
    which are numerical checks and are labelled as such. No DATA_REQUESTS.

---

# Builder C: lessons L13 to L18 (finite differences, AD, several variables)

Requests and gaps raised by Builder C under the BUILDER_RULES §10 output contract. Nothing here is a claim the lessons
rely on without saying so. Each item is either a gap the pages state, or work for a sibling builder or the architect.

## Dependencies on other builders' pages
1. **The derivative of exp is exp is used but not proved in L01 to L12.** L13 Example 2.3 takes f'(1) = e, and the
   exponential step of L14 Proposition 3.1 uses d/dx exp(g) = exp(g) g'. Both pages say the fact is assumed and not
   proved. No M2 lesson among L01 to L06 states it (checked: L04 and L05 contain no exp derivative). Architect: decide
   whether L05 (or L04) proves it, or whether M1 supplies it. If L05 proves it, L13 and L14 can drop the assumption.
2. **L03 must define the limit of a function of one variable with epsilon and delta.** L15 Section 3 says the
   several-variable limit is "the limit of a function at a point as Lesson L03 uses it for one variable, with the
   distance |x - a| in place of the distance on the line". If L03 uses a different formulation, L15 must change.
3. **L05 must state the product, quotient and chain rules; L06 must state the mean value theorem with its hypotheses.**
   L14 Proposition 3.1 and Proposition 5.2, L16 Example 1.3, L17 Theorem 2.2 and L18 Theorem 4.1 cite them. L17 and L18
   use the MVT with hypotheses: differentiable on the open interval, continuous on the closed one.
4. **L08 must state Taylor's theorem with the Lagrange remainder of order 1 and order 2, with hypotheses.** L13
   Theorems 2.1 and 2.2 state the hypotheses they need (C2 and C3 on the closed interval), which hold under any usual
   version. L08 must define `def-taylor-theorem`, as L13 and L16 link it.
5. **Anchors used by L13 to L18 links.** `L01.html#def-limit`, `L04.html#def-derivative` and `L08.html#def-taylor-theorem`
   exist in the worktree. L13 to L18 define `def-finite-difference-derivative`, `def-automatic-differentiation`,
   `def-partial-derivative`, `def-gradient` and `def-jacobian`, which are the anchors Builder D links to.
6. **Hub.** The hub (Builder A) must link L13 to L18 and set `data-hours-lessons` to 240 with the 10 h lessons.

## Architect decisions taken on the pages (please confirm)
7. **Continuity in L15 is a limit statement in prose.** Section 3 defines "continuous at a" as "the limit as x tends to a
   equals f(a)", with no `<dfn>` and no link, per Q5. The sequence form (Proposition 3.1) and the two examples are proved
   on the page.
8. **Open set, Euclidean norm, dot product and "matrix" are prose terms.** L15 Definition 2.3 defines an open set in
   prose with no `<dfn>`, per Q7. L18 Definition 2.1 says "matrix" means a rectangular array and defines the product Ah in
   the text, per Q2. The jacobian dfn sits on L18 as the curriculum requires.
9. **Automatic differentiation in L14 is the forward mode with dual numbers, and the reverse mode is worked on one graph.**
   The general cost count for either mode is not proved, and the page says so. A REFERENCE_REQUEST below asks for a source.

## Registry
10. **No registry key is cited by any graded span on L13 to L18.** `spivak2008calculus` and `hubbard2015vector` are named in
    each References section with "no passage locator confirmed". No rounding-error source is cited: the rounding model of
    L13 Section 3 is stated as an assumption of the page.

## REFERENCE_REQUESTS
11. **Automatic differentiation, a source for the reverse-mode pass and its cost.** L14 Section 5 and Misconception 2 need a
    source for the general statement of the forward and reverse counts, which L14 does not prove. Candidate from memory,
    not verified: Griewank and Walther, *Evaluating Derivatives* (2nd ed., SIAM, 2008). DOI null; confidence medium; the
    architect must resolve it through `add_reference.py`, and no page cites it until then.
12. **Floating-point model, optional.** The registry holds `goldberg1991every` (used_by M8). L13 Section 5 would cite it for a
    rounding statement only with a confirmed locator. No request is needed while the pages cite nothing from it.

## GLOSSARY_REQUESTS (terms used in prose on L13 to L18 without a `<dfn>`)
- open set, open ball (L15 Definition 2.3; plain prose by Q7)
- Euclidean norm, dot product (L15 Definition 1.1)
- limit of a function of several variables; continuity at a point in the limit sense (L15 Section 3; by Q5)
- directional derivative (L17 Definition 2.1; the gradient is a dfn in L17)
- differentiable at a point, with the array of Definition 3.1 (L18 Definition 3.1)
- evaluation error bound and rounding model (L13 Definition 3.1 and Proposition 3.2)
- dual number, tangent and value (L14 Definition 2.1; the terms are the page's own)
- adjoint (L14 Section 5)

## DATA_REQUESTS
None. The labs compute from closed forms, with no embedded snapshot.

## NOTATION_REQUESTS
None. The pages use \R from notation.json and standard KaTeX commands (\partial, \nabla, \varepsilon, \exp, \sin, \cos).

## CONTRACT_CHANGE_REQUESTS
None. M2 has no Atlas milestone.

## DAG_DEFECTS
None found by `check_dag.py --unit M2` on the current worktree, which reports PASS. The name collisions of plan §2 (continuity
M5, Riemann-Stieltjes M5, Fubini M6, Lagrange multiplier M7) do not occur in L13 to L18. Candidate for the architect: the exp
derivative of item 1 is needed from a prerequisite or from L05.

## Hypotheses stated on the pages, not measured
14. **L13 rounding model.** Proposition 3.2 assumes a stored evaluation error of at most delta and exact subtraction and
    division. It does not model the rounding of x + h, which changes the step by a relative 2^-53/h. L13 Section 5 says so.
    The predicted minima (forward near 1.8e-8, central near 6.3e-6 with delta = 2^-52) are predictions; the lab prints only a
    decade grid.
15. **L14 correctness on 251 points.** Proposition 3.1 is proved on the page; the lab checks two functions on one grid.
    The page says the lab does not prove the proposition or cover branches.
16. **L17 and L18 directional and remainder checks.** Theorem 2.2 and Theorem 4.1 are proved; the lab checks one point and
    360 directions (L17) or 25 points and one direction (L18). The page says so.

## Lab results with limited scope
17. **L13 central minimum is a tie at three digits.** The printed central errors at 1e-5 and 1e-7 are both 5.859e-11 to three
    digits; the full-precision values differ by about 4e-16. The page says the sweep does not resolve that minimum.
18. **L14 grid tolerance.** The printed "below 1e-12" results are one double-precision run of the lab on the stated grid.
19. **L15 sampled maxima.** The 1-degree sample gives the maximum of |g| exactly (the angle pi/4 is a sample) and the maximum
    of |f|/r as a lower bound, 0.3849 against the exact 0.3849002. The page says the sample cannot show a larger value between
    samples.
20. **L17 steepest direction at 62 degrees.** The gradient is at 61.96 degrees; the 1-degree grid can only report 62. The page
    states this.
21. **L18 remainder ratio.** For this quadratic map the ratio equals |k| exactly, so the check tests Example 4.2's algebra in one
    direction, not the limit in all directions. The page says so.

## Not mine
22. **Grader and project (Builder E), cards (Builder F).** `cards.json` is missing, so `check_pages.py --unit M2` reports one
    failure, "cards.json is missing". Builder F must cover L13 to L18 (the quizzes name `data-cards="cards.json"`).
23. **Mutants and ledgers.** Not written by Builder C.
24. **Shared stylesheet: quiz fieldsets need `min-inline-size: 0`.** `course/assets/css/course.css` sets `.quiz fieldset`
    without `min-inline-size: 0`, so a quiz option label can widen the page past 360 px. L13 and L15 hit it, and each was
    fixed on the page by shortening the option text (L13 q4; L15 q7, whose two labels now use words where the math was).
    The fix belongs in course.css, which is outside this builder's directory, so it is a request to the architect.

## Builder F (cards.json, L01 to L24)

Written: `course/modules/M/M2/cards.json` (375 cards, `M2-c001` to `M2-c375`). Cards carry no `cite` key, since no card
cites a registry key. Every card with grade C or D carries a `basis`. `check_pages.py --unit M2` reports PASS.

1. **L11, key-results row "Integrable functions form a vector space".** Lemma 1.1 proves closure under sums and scalar
   multiples and linearity of the integral. It does not prove the vector-space axioms. The card states only what Lemma 1.1
   proves. Lesson owner: reword the row.
2. **L14, Proposition 3.1 is graded T, but its proof uses that the derivative of exp is exp.** Section 3 says this is
   "assumed here ... not proved on this page", and the proposition's hypotheses do not list it (Rule 6). Either list it as a
   hypothesis or grade the proposition down. The card records the assumption in its back.
3. **L08, Theorem 1.2 (Rolle) is graded T, citing Lesson 6.** The Lesson 6 mean value theorem takes Fact 2.1 (extreme value
   theorem) as assumed, and Fact 2.1 carries no grade. Verifier to decide whether the T grade needs the assumption stated.
4. **L09, Misconception 2 gives a forward pointer for the value 1/6** (Lesson 10, Theorem 2.1; Lesson 11, Lemma 1.1). The
   card omits the value. Lesson owner: keep or remove the forward pointer.
5. **Lab-dependent cards.** Grade-C cards quote printed values from `tests/labs/M2/lab-M2-Lnn-1.py` output (L01 to L24,
   including L23 and L24's decade table). If a twin's output changes, these cards must be regenerated from the page.
6. **Not carded (remarks, outside the mandated list):** L07 Remark 4.3, L08 Remark 3.2, L09 Remark 1.4. Add if the
   architect wants remarks carded.
