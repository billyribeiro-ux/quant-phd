# FC2 open items and gaps (Builder D: project page, grader, rung labs; 2026-10-28)

Requests and gaps raised by Builder D under the BUILDER_RULES §10 output contract, and the places where the build
departs from `plans/FC2-build-plan.md`. Nothing here is a claim the project relies on beyond what the page states.

## DATA_REQUESTS
- D1 (plan §8.2, still open): an options-quote source for the arbitrage scanner, with an issuer statement that permits
  copying and redistribution, quoted in `licence` with its page in `licence_url`. None is cleared. Until one is, every
  chain on the project page, in Lab 1 and Lab 3, and in the autograder is SIMULATED (plan §7 B1). Source URL, series,
  licence and transform: to be supplied by the architect after reading the terms. No candidate's terms were read.
- The registry and `tools/data_sources.yaml` record no option-quote source (checked by `grep` on 2026-10-28), so the
  project page states the honest-pending note in its Inputs section.

## REFERENCE_REQUESTS
None. The project page cites only `hull2021options`, `stoll1969relationship` and `cox1979option` in its reading list,
all verified in the registry (checked through `coursekit.registry_keys`). No editions, volumes or locators are quoted
(plan §7 Q5). The note asks for no locator from them.

## NOTATION_REQUESTS
None. The page uses the local letters C, P, S, K, df, gross and net, and no registered symbol with another meaning.

## GLOSSARY_REQUESTS (terms the project defines inline, for the architect to decide on glossary entries)
- synthetic forward, S − K df (project conventions; plan §7 Q12).
- chord and the chord weights (project conventions and the convexity test).
- gross amount and net amount (project constraints and Lab 1 hypothesis).
- half-spread, defined as half of a leg's bid–ask spread (project conventions, P6). It is the FC1 concept
  `bid-ask-spread` used in plain prose (see DAG_DEFECTS).
- the three legs of a finding (project conventions, P6).

## CONTRACT_CHANGE_REQUESTS
None. FC2 has no Atlas milestone (plan §7 Q15).

## DAG_DEFECTS
- `bid-ask-spread` (FC1, plan §0.2): the cost model uses the half-spread, and FC2's closure does not include FC1 unless
  the architect's prerequisite change (plan §7 Q2, applied to the curriculum) is in effect. The project uses the word in
  plain prose with no link. `tools/check_dag.py --unit FC2` reports PASS, because the check reads links and definitions
  only.
- No other DAG defect: the project links only `arbitrage-opportunity`, `put-call-parity` and
  `option-arbitrage-bounds`, all defined in FC2 lessons (L01, L05).

## Departures from the plan (for the architect to confirm or reverse)
1. **Cost leg count (plan silent on the number of legs).** The plan says the half-spread is "paid per leg" (§4.2) and gives
   the boundary as `gross == fee + spread` (§5.5), which is one leg. This build charges three legs per finding,
   `3 × (fee + half-spread)`, because a parity finding trades three legs and a convexity finding trades three calls.
   The boundary tests use 3 × (fee + half-spread) (for example, a 45-cent gross at fee 10 and half-spread 5 has net zero).
   If one leg is intended, change `LEGS_PER_FINDING` in `grader/reference.py` and the spec's constraints and P6, then
   regenerate the mutants (m03 and m04 depend on it).
2. **df_ppm in convexity_violations.** The plan says "discounted second difference" (§4.3). Quotes are present values
   (P5), so the test is not discounted and its sign does not depend on df_ppm. `df_ppm` is validated, and a test checks that
   the list does not change with it. The gross is undiscounted.
3. **Lab 3 is not a call to the student's scanner.** Plan §4.1 says `lab-FC2-project-3` "calls the scanner". A lab runs
   in its own directory and cannot import the student's `scanner.py`. Lab 3 therefore computes the reference findings of
   its chain with the same arithmetic as Lab 1 and prints them, and the page tells the student to compare their
   `scan` output on that chain with the printed table.
4. **Six strikes on every chain.** Plan §5.5 allows six or seven. The generator always draws six strikes, so the test
   count is the same for every seed (75 for seeds 0 to 49, confirmed by `pytest --collect-only`).
5. **Mutant 5 (plan §5.6).** The plan's "convexity on the input order" mutant is only meaningful when unsorted strikes are
   accepted. The reference rejects them, so mutant m05 is the one that drops the ordering check and accepts shuffled
   strikes. The other nine follow the plan.
6. **Five alternative implementations.** They were written and run as scratch fixtures in `/tmp/fc2-alt/`, not archived
   under `ledgers/FC2/scripts/`, because the plan gives archiving to the verifier (plan §13). All five pass seeds 0 to 49
   after their length messages were fixed to name the two lengths, which is a condition the spec names. Alternative 4
   handles unequal spacing (it compares adjacent slopes), so it counts.
7. **Mutants written here.** The task asked for the ten student-error mutants in `ledgers/FC2/mutants/`. They are written,
   and `tools/mutate_graders.py --unit FC2 --seeds 0-9` reports 10/10 killed. No `ledgers/FC2.verification.json` was written,
   because a builder never writes a ledger.
8. **Named conditions tested, unnamed types not.** The suite requires `ValueError` only for the four conditions the spec
   names (strictly increasing and positive strikes, df_ppm range, one quote per strike, non-negative cost terms). It does
   not test booleans or floats as inputs, because the spec does not name them, so no test enforces them.

## KNOWN_LIMITATIONS
- Every chain is SIMULATED (DATA_REQUESTS D1). The project's Lab 1 and Lab 3 chains and the autograder's generated chains
  are not market quotes, and the page says so.
- The cost model is a stated simplification: mid quotes, a flat half-spread on each leg, a flat fee per contract, and
  three legs per finding (departure 1). It does not model partial fills, size, or the time at which quotes were taken.
- Parity findings depend on the supplied discount factor (P4), which the project does not model. The convexity test
  uses no model.
- Lab 1 and Lab 2 share one chain, so Lab 2 is a repeat of Lab 1 with three blanks, as plan §4.1 specifies.
- The grader's instances always have six strikes on an evenly spaced grid. Uneven grids are tested only by hand-built
  chains (the 100/110/150 case and Lab 3's chain), not by the generator.
- The suite's conditional tests (for example, the planted-violation tests) return early for seeds whose planted kind is
  different. Each has a sibling test for the other kind, so no seed is left unchecked, but a single test does not cover
  every seed.
- The rubric's C4 and C5 level-4 descriptors ask a student to quantify effects (the size of the factor's effect, and the
  direction of a settlement's effect on the net). Exemplar B states that it does not do so, and scores 3 there.
- Two instances are checked in the suite (the seed and seed plus 7919). A fixed answer that matched both seeds would pass
  the scan oracle tests on those two seeds, but not on the other 48.
- The labs and the grader do not test the hub's placement quiz, which is Builder A's page.
