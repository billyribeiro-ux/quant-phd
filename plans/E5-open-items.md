# E5 open items and gaps (Builder E: project, rung labs, rubric and exemplars; 2026-10-28)

Requests and gaps raised by Builder E under the BUILDER_RULES §10 output contract, for `course/modules/E/E5/project.html`
and `tests/labs/E5/lab-E5-project-1..3.py`. Each item is a gap the page states, or work for the architect.

## DATA_REQUESTS
- Real GDP, a price index, an unemployment rate and a policy rate for a macro dashboard. None is named here. Each needs
  an issuer URL, a licence sentence quoted from the issuer's page, the licence page, and the transform (BUILDER_RULES
  §6.6 steps 1-5). The project asks the student to supply all four as CSV (bring-your-own-data, schemas in the Data
  section), so the page does not depend on this request being met.
- Browser validation of the four bring-your-own CSV schemas. The project page documents the schemas and says that the
  checks are run by hand; no validator exists in `course/assets/js`, and the architect's rule against new JS kernels
  means one needs a decision. Until it exists, the page says so.

## REFERENCE_REQUESTS
- None required. The project cites only four registry keys in its reading list (`solow1956contribution`,
  `hicks1937mr`, `phelps1968money`, `blanchard2020macroeconomics`), each at book or paper level, with no attributed
  passage.
- Friedman (1968) is not cited (architect decision B3). The review-queue candidate DOI 10.2307/2296661 must not be
  admitted (`references/review_queue.json`).
- No B- or C-graded claim is made on the page. The Limits section says so, so no counter-evidence is needed here.

## NOTATION_REQUESTS
- None. The page uses the local symbols `g_t`, `\pi_t`, `y_t`, `\bar\pi`, `r^{n}`, `u^{\ast}`, `i^{\ast}_t`, `\phi_\pi`,
  `\phi_y` and `\tilde Y_t`, each defined in the Conventions section, and no registered symbol with another meaning.

## GLOSSARY_REQUESTS
- Terms defined inline on the project page, as plain definitions with no concept link: annualised GDP growth, inflation
  (year on year), window, trend, output gap, cycle flag, term spread, stated parameters, Taylor-rule value, policy gap,
  rounding (Conventions section). None is one of the 13 E5 concepts.

## CONTRACT_CHANGE_REQUESTS
- None. E5 has no Atlas milestone, and the project uses no Atlas series (architect decision B2).

## DAG_DEFECTS
- None. `tools/check_dag.py --unit E5` passes. The project links no concept, so no prerequisite is needed.

## Items the architect should see
- The Lab 2 term spread (rung 2) is SIMULATED, from yields drawn around the policy rate with seed 2027. It is not the
  H.15 spread of rung 3, and the page says so.
- The Lab 3 table mixes SIMULATED macro series with the REAL term spread from `ust_daily.csv`. Each column is labelled
  with its source in the lab's header line and in the hypothesis.
- Exemplar A (Limits) says that a discount rate is below the yield on the same bill, so a spread built on the yield
  would be smaller than the published one. This direction rests on the standard money-market yield relation, which the
  page does not derive, cite or compute. The size is not stated. A verifier should check the direction against a
  reference the architect approves.

## KNOWN_LIMITATIONS
- The four macro series are SIMULATED in every lab. No real macro data is shown anywhere on the project page.
- The stated parameters (target 2.0, natural real rate 2.0, natural unemployment rate 4.0, Taylor coefficients 0.5)
  are assumptions of the dashboard. They are not estimates, and the page does not attribute them to any source.
- The output gap uses a trend fitted to the same 20-quarter window, so it is not a real-time measure. The page names
  this in the Limits exemplar and in the conventions.
- Rubric exemplars A and B were written and annotated by Builder E. Their official scores have not been checked by a
  blind scorer; the verifier's calibration pass (VERIFIER §2.6, rubric projects) is the check.
- The project's cards (`cards.json`) are not written here (Builder F). `check_pages.py --unit E5` reports only that file
  as missing for the project's unit.
- `lab-E5-project-2` is a completion lab. Its blanked code is hand-written from the twin with the two blanks at the
  term-spread and output-gap lines, and `run_labs.py` confirms every other line matches the twin.

## Builder D (L07, L08): open items

Lessons written: L07 (Central-Bank Policy and the Taylor Rule) and L08 (Fiscal Policy and the Multiplier). Labs:
`lab-E5-L07-1` and `lab-E5-L08-1`, both exact (`fractions`), with illustrative inputs. Neither is labelled SIMULATED,
because both are closed-form checks (plan §2.2).

### DATA_REQUESTS
- None. Neither lab reads a dataset, and neither page makes an empirical claim.

### REFERENCE_REQUESTS
- None. L07 cites no source; the Taylor rule is a definition (architect default, Q4). The registry key
  `taylor1993discretion` is not used. L08 makes no graded claim about empirical multipliers, so the fiscal-multiplier
  literature lead (plan §7.2, third bullet) is not needed by these pages. It is needed only if the architect wants an
  empirical sentence added.

### GLOSSARY_REQUESTS
- None. Plain `<dfn>` with no `data-concept`: inflation target, inflation gap, natural real rate (L07); lump-sum tax
  and stage of spending (L08). The output gap is not redefined: L07 uses the definition of L04 (Definition 1.1), with the
  percent-of-trend convention stated on the page.

### DAG_DEFECTS
- None. Links used: `price-index-inflation` (L01, `L01.html#def-price-index-inflation`), `business-cycle` (L04),
  `is-lm-model` (L04), `policy-rate` (L07), `comparative-statics` (E1, `concepts.html`). `check_dag.py --unit E5` passes.

### Cross-lesson dependencies (to re-check if these change)
- L07 converts L01's simple inflation (Definition 2.2, a fraction per period) to percent per period, and converts L04's
  output gap (Definition 1.1, in units of output) to percent of trend output. If L01 or L04 changes its convention, the
  conversion sentence in L07 §1 changes with it.
- L08 Remark 2.5 quotes L04's IS–LM result (the spending multiplier is smaller than 1/(1 - c) when b > 0 and d > 0)
  and its name for the ratio (Definition 4.1). If L04 changes either, L08 Remark 2.5 changes with it.
- Hub and nav titles: L07 and L08 use the h1 strings in the Builder A list. Builder B's L03 and L04 h1s are
  "The Solow growth model" and "Business cycles and the IS–LM model", which differ in capitalisation or wording from that
  list. The orchestrator should align them.

### NOTATION
- The lump-sum tax is written \(\mathrm{Tax}\) in L08 (not bare \(T\), notation.json `T` entry). The natural real rate is
  \(r^{n}\) (L07), not \(R^{\ast}\). No registered macro is redefined.

### KNOWN_LIMITATIONS (Builder D)
1. The shared stylesheet has no `min-inline-size: 0` on quiz `fieldset` elements (`course/assets/css/course.css`, the
   `.quiz fieldset` rule at line 1468). A quiz option label with a long line of text pushed L08 to 402 px at 360 px wide.
   L08 avoids it by shortening the option text. The CSS change belongs to the design system, so it is requested here,
   not made.
2. The L07 rule is not estimated. Its coefficients (3/2 and 1/2) and its natural real rate (1) are illustrative inputs
   for the arithmetic. The page says so and cites no value.
3. The L07 rule returns a negative nominal rate at some grid points (Lab 1, Part A). The page imposes no lower bound and
   says so (Remark 2.3, Problem R3).
4. L08 holds the policy rate and prices fixed. It does not compute the multiplier under an interest-rate rule or in
   IS–LM (Remark 2.5). It does not compute the multiplier with imports or with a time path.
5. L08 has no empirical estimate of any fiscal multiplier. The page says so and grades nothing as B or C.

## Slice b (L04-L06): round-10 decisions (fixer, 2026-10-29)

### Decision 1: expected inflation in L06 is `\pi^{e}_t`, not the registered `\E` macro
- Options checked: `notation/notation.json` registers `\E` as `\mathbb{E}` with the meaning "expectation operator". Expected
  inflation is a forecast value fixed by the rule in A3 (L06 §1 says the model has no random variables), so writing it
  with `\E` would apply the expectation operator to a non-random quantity.
- Chosen: L06 writes `\pi^{e}_t` (32 uses, 0 uses of `\E`). `\pi^{e}_t` is a local symbol, defined in L06 §1 before A1.
- Plan updated to match: `plans/E5-build-plan.md` notation table row for `\E`, the NOTATION_REQUESTS line, and the L06
  row of §3. No NOTATION_REQUESTS is needed because no new macro is registered.

### Decision 2: L05 demand curve is the linear form A1, not a derivation from IS-LM
- Lesson state: L05.html Remark 1.2 says the lesson does not derive its demand curve from IS-LM and takes A1 as the model.
  The IS-LM output is affine in `1/P` (L04 Proposition 3.2 with `\bar m = M/P`), so it is not linear in `P` unless `b = 0`.
- Chosen: the plan follows the lesson. `plans/E5-build-plan.md` §3 L05 row and the §2.2 cross-reference now say the
  demand curve is A1, with the Remark 1.2 caveat. The plan's earlier wording ("the aggregate-demand curve from IS-LM")
  is withdrawn.
- Status: this is a deviation from the planner's recommendation. The architect has not ratified it (plan §12 says the
  architect decisions are pending). It stays open until the architect confirms or reverses it.

### Decision 3: L04 cross-reference
- L04.html why-it-matters paragraph (line 52): "unique equilibrium (Definition 3.1 below)" becomes "(Proposition 3.2 below)". Uniqueness is
  stated in Proposition 3.2; Definition 3.1 defines the equilibrium and `D`.

### Lab docstring wording (fixer, round 10)
- The docstrings of `lab-E5-L04-1`, `lab-E5-L05-1` and `lab-E5-L06-1` said every value is an exact fraction. The labs also
  print decimals rounded to six or ten places and print `True` or `False` checks. The docstrings now say so. The printed
  output is unchanged; the pages were re-embedded with `tools/embed_labs.py --refresh`.

## Architect rulings (batch 3, round 11)

- **Decision 2 ratified.** L05 takes the aggregate-demand curve as the linear form A1 and says on the page that it does
  not derive it from IS-LM (Remark 1.2 states the caveat). The build plan is corrected to match the lesson; a derivation
  from IS-LM is out of scope for this module and is not required.
- **Expected inflation is `\pi^{e}_t`.** It is a non-random forecast under A3, so the expectation operator `\E` does not
  apply to it. `\pi^{e}_t` is an unregistered, lesson-local symbol with no registry conflict. The plan is corrected to
  match L06.
