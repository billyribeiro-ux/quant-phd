# CF1 open items (Builder A: hub, L01, L02)

Written by the Builder A pass on the CF1 hub and lessons L01 and L02. Each line is a request for the architect or the
verifier. None of them is a bibliographic claim: topics only, as the architect's decision Q7 requires.

## REFERENCE_REQUESTS (topics only)

- A verified textbook source for the textbook statement of the NPV decision rule, the one-rate market and the NPV
  ranking dependence on the rate. Needed for: L01 Section 1 (the rule is a convention, grade C, whose reason is proved
  in Section 4 and so needs no source). Note: the curriculum's textbook string (Brealey, Myers & Allen, 14th ed., 2023)
  has no registry key whose record matches it. `brealey2022principles` is not cited, per architect decision Q3.
- No other request. L01 and L02 cite no registry key. Every result on those pages is a proof, a computation on the page,
  or a printed output of a SIMULATED lab, and each carries its basis.

## GLOSSARY_REQUESTS

No `glossary.json` exists in the repository. The terms that L01 and L02 define, for the architect to place if a glossary
is created:

- net present value (L01, Definition 1.1)
- incremental cash flow (L02, Definition 1.1)
- depreciation tax shield (L02, Corollary 2.3)
- net working capital investment (L02, Definition 3.1)
- one-rate market (L01, Assumption 4.0)

## DATA_REQUESTS

None. The module embeds no dataset. Every project and lab figure is generated and labelled SIMULATED (plan section 9).

## CONTRACT_CHANGE_REQUESTS

None.

## DAG_DEFECTS

None for L01 and L02. The architect's decision Q1 added AC1 to the prerequisites, so the concepts used on these pages
(present value, discount factor, annuity, geometric series, balance sheet, depreciation and amortization, accrual
accounting) are in the closure, and each one is linked.

Unit-level, outside Builder A's pages: `check_dag --unit CF1` reports `internal-rate-of-return` and
`multiple-irr-problem` as not defined with `<dfn>` on any page. Those are L04 concepts and the L04 builder defines them.

## KNOWN_LIMITATIONS

- L01 and L02 use standard KaTeX commands (`\mathrm`, `\dfrac`, `\dots`, `\ldots`, `\bigl`, `\bigr`, `\tfrac`, `\text`,
  `\ast`). They do not use the custom macros in `notation/notation.json`, which define none of these. The symbol `r^\ast`
  (the rate at which two NPVs are equal, Problem P3) is not checked against the symbol registry.
- The hub's "Core reading" lists `graham2001theory` by key only. No figure from it is quoted.
- The hub's lesson cards name L03 to L06 by their working titles from the plan. Their pages are written by other
  builders, and the titles should be checked against those pages at integration.
- Lab 1 and Lab 2 are standard-library scripts that print SIMULATED results. They are not evidence about any firm.
- L01 Remark 5.2 and Problem M1 show rounding effects on purpose. The page states which values are computed from the
  unrounded numbers, and the verifier should recheck them.
- The hub's placement items and the lesson quizzes use the explanation text as the reason for the answer. The
  verifier should read each explanation against its lesson.
