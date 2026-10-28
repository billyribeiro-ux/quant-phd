# FC1 open items (Builder A: hub, L01, L02)

Scope of this file: the hub `course/modules/FC/FC1/index.html`, lessons L01 and L02, and their lab twins
`tests/labs/FC1/lab-FC1-L01-1.py` and `tests/labs/FC1/lab-FC1-L02-1.py`. Lessons L03 to L05, the project, the grader and
`cards.json` belong to other builders.

## Requests

- **REFERENCE_REQUESTS.** (1) McLeay, Radia & Thomas (2014), Bank of England Quarterly Bulletin Q1, named at
  `curriculum/02-economics-finance-core.yaml:386`. Not in the registry and not cited. Needed only if a lesson states a
  claim about real bank money creation, which L01 does not do. Confidence in the citation string: as given, unverified.
  (2) A settlement-cycle primary source for L05, if any settlement period is stated as a fact. (3) A spread-evidence
  source for L03, if any empirical claim about spreads is made. Neither is cited by Builder A.
- **GLOSSARY_REQUESTS.** None needed for L01 or L02. Terms used in prose without `<dfn>`: stylised bank, reserve ratio,
  leakage, stage, equity (defined in L01 Section 1 as assets minus liabilities), exposure, form, venue, cash instrument,
  derivative, OTC (defined in L02 Definition 1.1 as "over-the-counter").
- **NOTATION_REQUESTS.** None. L01 uses local letters \(d\), \(D_t\), \(S_n\), \(X_t\), \(\ell_t\), \(\rho\), \(\varphi\), \(\kappa\), \(q\),
  \(E\), \(A\) and \(\ell\) (loss). None is a registered symbol and none reuses \(T\), \(R_f\), \(\mathbb{Q}\) or \(\Phi\).
- **DATA_REQUESTS.** None. Both lessons use typed-in parameters and no snapshot.
- **CONTRACT_CHANGE_REQUESTS.** None (no Atlas milestone).
- **DAG_DEFECTS.** None found in L01 or L02 by `check_dag.py --unit FC1`, which reports only the definitions still missing
  from L03 to L05 (`order-types`, `limit-order-book`, and the other L03 to L05 concepts).

## Decisions taken by Builder A that the architect should confirm

1. **Project scope in the hub.** The architect decision says the project covers cash instruments only. The hub describes
   a "cash-instrument engine" and a bond coupon in basis points. The hub's placement skill items and rung 1 and rung 2 text
   assume: face value in integer cents, coupon in integer basis points, the coupon at each period equal to
   `face_cents * coupon_bps / 10000` rounded half up, and principal at the last period. Builder D must match this, or the hub
   text must change. The hub does not mention the order-book simulator that the architect decision also names; Builder D
   should state whether it is part of the project.
2. **Hub lesson titles.** The hub cards and the L02 next link use these titles. The L03, L04 and L05 `<h1>` must match:
   - L03: "Dealers, Market Makers and the Bid–Ask Spread"
   - L04: "Order Types and the Limit Order Book"
   - L05: "Clearing, Settlement and the Trade Lifecycle"
3. **Hub prerequisite text.** The hub names E1 competitive equilibrium and Bertrand competition as used concepts, and says
   that the project's pricing uses present-value and discount-factor material. Those links must exist in the lessons or
   project that use them, or the hub sentence must change at integration.
4. **Forward pointers in L02.** L02 Section 4 names L04 (order types and the limit order book) and L05 (clearing and
   settlement) as the lessons that define those terms. The L04 and L05 builders must define them under those names.
5. **Registry year conflicts (architect Q3).** The hub's core reading cites `mishkin2021economics` and `harris2002trading` by
   key only, and renders the registry's own fields. No lesson cites a locator, page, table or figure from either book, and
   no edition or year is typed on the site.
6. **Hours.** Lessons L01 and L02 declare 10 h each. The hub declares `data-hours-lessons="50"` and `data-hours-project="20"`.
   The hub check reports "lessons declare 40 h" until L03 to L05 are built.

## Verification status (Builder A, not a verifier)

- `check_pages.py --unit FC1 --page L01`: PASS. `--page L02`: PASS.
- `check_pages.py --unit FC1`: fails only for L03 to L05 (missing), `project.html` (missing) and `cards.json` (missing,
  Builder E). The hub's own checks pass.
- `check_dag.py --unit FC1`: fails only for the L04 and L05 concepts that are not yet defined.
- `run_labs.py --unit FC1 --page L01`: PASS (1/1). `--page L02`: PASS (1/1).
- `ruff check`, `ruff format --check` and `mypy --no-incremental` pass on the two lab twins.
- Not run by Builder A: `check_projects.py`, `run_graders.py`, `mutate_graders.py`, `cards.json` checks, and the
  `check_pages.py --all` and `check_dag.py --all` gates. Those belong to the integration step.
- The verifier must re-run the five alternative-implementation and ten-mutant grader checks; they are not part of Builder A's work.

# FC1 open items (Builder B: lessons L03 and L04)

Scope: `course/modules/FC/FC1/L03.html`, `L04.html`, and the twins `tests/labs/FC1/lab-FC1-L03-1.py` and
`lab-FC1-L04-1.py`. Builder A owns the hub, L01 and L02. Builders C, D and E own L05, the project and the grader, and
`cards.json`.

## Requests (Builder B)

- **REFERENCE_REQUESTS.** None. Every result on L03 and L04 is proved on the page or checked by Lab 1, so neither lesson
  makes an empirical claim about markets. The spread-evidence source named in the build plan (section 6) is therefore not
  needed. `harris2002trading` is cited by key at book level only, with the registry's own year 2002, and no passage
  locator is confirmed (no claim is attributed to it).
- **GLOSSARY_REQUESTS.** None needed beyond in-text definitions. Terms defined in prose (plain `<dfn>` without
  `data-concept`, or in a definition block): tick, last trade price, price-time priority, crossed, closed sequence,
  mark-to-mid, mid-move term, relative spread. The two registered concepts are `market-maker` and `bid-ask-spread` (L03
  Definitions 1.1 and 1.2), `order-types` and `limit-order-book` (L04 Definitions 1.1 and 2.1).
- **NOTATION_REQUESTS.** None. Symbols used: \(m\), \(h\), \(s\), \(a\), \(b\), \(p\), \(\sigma_t\), \(q_t\), \(C\), \(I\), \(V\),
  \(P\), \(Q\), \(c\), \(k\), \(G\), \(R\), \(X\), \(\alpha\), \(\beta\), \(\pi_i\), all local. The terminal mid is \(m_n\)
  (n the number of trades), so the registered symbol \(T\) is not used.
- **DATA_REQUESTS.** None. Both labs use generated flows labelled SIMULATED (seed 2026); no snapshot and no `data-files`.
- **CONTRACT_CHANGE_REQUESTS.** None (no Atlas milestone).
- **DAG_DEFECTS.** None from L03 and L04. The plan's L04 plain-prose item `order-book-data-structure` (CS2) is not used,
  so no DAG defect arises. `check_dag.py --unit FC1` reports PASS with L01 to L04 present.
- **CSS request (shared file, not edited).** The quiz fieldsets on L03 and L04 carry `style="min-inline-size: 0"` so
  that long KaTeX options do not force horizontal scroll at 360 px. `course/assets/css/course.css` has a `.quiz fieldset`
  rule with no `min-inline-size`. The architect should add `min-inline-size: 0` there and remove the inline style.

## Integration points for other builders

1. Lesson titles, which the hub and L02 must match: L03 "Dealers, Market Makers and the Bid–Ask Spread"; L04 "Order Types
   and the Limit Order Book". Both `<h1>` values match Builder A's listing.
2. Hours: L03 and L04 each declare `data-hours="10"`, so lessons total 50 with L05 at 10.
3. Links into earlier lessons: L03 links `L02.html#def-exchange-vs-otc` (Builder A's anchor, present). L04 links
   `L03.html#def-bid-ask-spread`. L04 links `L05.html` as its next lesson.
4. Cards (Builder E): card candidates from L03 and L04 are the two L03 definitions, Proposition 2.3 and Corollary 2.4,
   Proposition 3.2, the two L04 definitions, and Propositions 2.2 and 2.3 of L04. Each is graded T and needs no cite.
   Note that both lessons number their propositions from 2, so card text should name the lesson, for example "L04
   Proposition 2.3".

## Verification status (Builder B, not a verifier)

- `check_pages.py --unit FC1 --page L03`: PASS. `--page L04`: PASS.
- `check_dag.py --unit FC1`: PASS.
- `run_labs.py --unit FC1 --page L03`: PASS (1/1). `--page L04`: PASS (1/1).
- `embed_labs.py` on both pages: 2 markers each; the expected blocks are the twins' printed output.
- `ruff check`, `ruff format --check` and `mypy --no-incremental` pass on both twins.
- Not run by Builder B: `check_pages.py --unit FC1` (whole unit, needs L05, the project and cards), `check_projects.py`,
  `run_graders.py`, `mutate_graders.py`, `check_pages.py --all`, `check_dag.py --all`. Verifier and integration only.

# FC1 open items (Builder D: project, grader and project labs)

## Requests (Builder D)

- GLOSSARY_REQUESTS: basis point; holder and the long and short side (defined in the project conventions block, no
  `data-concept`); settlement period; face and coupon (each defined with `<dfn>` on the project page, no `data-concept`).
- REFERENCE_REQUESTS: none. The reading list cites `harris2002trading` and `mishkin2021economics` by key only, with no
  statement attributed to either (architect decision, Q3). McLeay, Radia and Thomas is not cited (Q4).
- NOTATION_REQUESTS: none.
- DATA_REQUESTS: none (no embedded data; every value is SIMULATED).
- CONTRACT_CHANGE_REQUESTS: none (no Atlas milestone).
- DAG_DEFECTS (plain prose, no link, no `data-concept`): futures, swaps and options (FC2) are named in the project
  Context only to say they are not part of this project. Bond pricing uses the M1 `discount-factor` and
  `present-value` concepts, which are inside FC1's closure and are linked.

## Decisions taken by Builder D (the architect should confirm)

1. **Project scope.** The architect decision says the project "covers cash instruments only (a trade-lifecycle and
   order-book simulator)". Builder D read the parenthesis as the scope of the cash instruments and built: a fixed-rate
   bond (`Bond`, `events()`, `bond_price_cents`) and the settlement event of a cash trade (`CashTrade`). The order-book
   simulator is rung 4 (stretch, not graded). If the simulator is meant as a graded component, the interface, the hours
   and the suite all change; this is a request, not a silent choice.
2. **Interface (frozen in `grader/reference.py`).** `Bond(face_cents, coupon_bps, periods)`; `bond_price_cents(bond,
   yield_bps)`; `CashTrade(quantity, price_cents, side, settlement_day)`. The planner's `Future`, `Swap` and `Option`
   are removed, as the architect decided.
3. **Events.** One event per period. The face is added to the last period's coupon in that one event, so periods are
   never repeated.
4. **Rounding.** Exact `Fraction` arithmetic, one rounding per output, to the nearest cent, halves away from zero. A
   trade's amount is an exact integer (quantity times price), so it has no rounding step.
5. **Named conditions (the only ones that require `ValueError`).** `periods < 1`, `face_cents <= 0`, `coupon_bps < 0`
   (Bond); `yield_bps <= -10000` (bond_price_cents); `quantity < 1`, `price_cents < 0`, `side` not in {+1, -1},
   `settlement_day < 1` (CashTrade). Each has its own test on both sides of its bound.
6. **Hand fixtures** (architect Q10): A `Bond(10000, 500, 1)` at 500 bps gives `[(1, 10500)]` and price 10000; B the same
   bond at -500 bps gives 11053; C `Bond(10001, 5000, 2)` gives `[(1, 5001), (2, 15002)]`; D `Bond(1, 5000, 1)` gives
   `[(1, 2)]`; E `CashTrade(10, 9850, 1, 2)` gives `[(2, -98500)]`; and a rounding fixture, `Bond(10000, 500, 3)` at 400
   bps, where rounding once gives 10278 and rounding each term first gives 10277.
7. **Instances.** `make_instance` seeds `random.Random("FC1-cash-engine/<seed>")`. Seeds 0 to 49 give distinct cases.

## Shared-asset defect (for the architect, not patched by Builder D)

- `course/assets/js/refs.js` renders a registry DOI as one unbreakable link (for `harris2002trading`, the label is
  `doi:10.1093/oso/9780195144703.001.0001`). At 360 px this forces a 5 px page-level horizontal scroll on any page that
  cites that key. `project.html` carries a page-level rule, `.reading-list a, .references a { overflow-wrap: anywhere; }`,
  which clears it. The shared fix belongs in `course.css` or `refs.js`. The hub and the lesson pages that cite
  `harris2002trading` (L03, L04, L05 at this writing) will hit the same overflow until it is fixed.

## Verification status (Builder D; not a verifier)

- `check_projects.py --unit FC1`: PASS.
- `check_dag.py --unit FC1`: PASS.
- `check_pages.py --unit FC1`: FAIL (1 problem): `cards.json is missing` (Builder E). The project page has no problems.
- `run_labs.py --unit FC1`: PASS (8/8). `--page project`: PASS (3/3).
- `run_graders.py --unit FC1 --seeds 0-49`: PASS (reference 50/50 seeds; starter fails the suite; mypy strict clean).
- `mutate_graders.py --unit FC1 --seeds 0-9`: PASS (10/10 killed). Mutants are in `ledgers/FC1/mutants/`.
- Five alternative correct implementations in `ledgers/FC1/alternatives/` pass seeds 0 to 49 (run by a scratch harness
  outside the repo).
- `pytest --collect-only`: 47 tests. The page quotes 47.
- `page_smoke.py --unit FC1 --pages project`: PASS (360 px and both themes; the in-browser grader passes 47 tests).
- `ruff check` and `ruff format --check` on the grader, the twins and `ledgers/FC1`: pass. `mypy --strict` on the reference,
  instance, starter and the three project twins: pass.
- Not run by Builder D: `check_pages --all`, `check_dag --all`, `build_site.py --check`, `render_curriculum.py`,
  `verify_refs.py`, `fetch_data.py --check`, `check_pages.py` on the whole unit (needs `cards.json`). Integration only.

## Known limitations (Builder D)

- The starter stubs raise `NotImplementedError`. Each failing test is named for its property, but the traceback is not
  replaced with a property message.
- The suite cannot tell a module that memorises the seed-0 price and computes everything else correctly from a correct
  module. Mutant `m10` covers the constant-only case, which the suite does kill.
- The project covers two cash objects. Futures, swaps, options and bond yield-to-maturity are not in it.
