# AC2 open items and questions (collated by the architect, 2026-10-27)

Requests the AC2 builders raised under the BUILDER_RULES output contract, with the architect's status. Nothing here is a
claim the lessons rely on; each item is either a gap the lessons state honestly or work for a person or a later round.
Lessons that refer to "the build report" mean this file.

## DATA_REQUESTS
| Request | Status |
|---|---|
| SEC EDGAR company facts (`https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`): a real filer for the L01-L06 examples and the project's real-data check. Needs the SEC's reuse statement quoted in `tools/data_sources.yaml` (BUILDER_RULES 6.6). `data.sec.gov` serves the JSON to a descriptive, non-personal User-Agent; plain curl to `https://www.sec.gov/os/webmaster-faq` and `https://www.sec.gov/os/accessing-edgar-data` returned HTTP 403 (2026-10-27), so the reuse statement has not been read. | OPEN, needs a person to read the SEC's statement on reuse and quote the sentence and URL. Until then every filer in AC2 is SIMULATED and the hub says so. |
| Monthly stock returns for the L05 real test (Sloan-style accrual sort). No cleared source is in the registry (BLUEPRINT 5.3 lists the Kenneth French library as not cleared). | OPEN. L05 is a SIMULATED mechanics demonstration and says so. |

## REFERENCE_REQUESTS (none of these is in `references/references.json`; none is cited as fact)
| Work | Needed for | Status |
|---|---|---|
| Beneish (1999): an open or secondary reproduction of the intercept and eight-variable coefficient table with a table locator (the registry has the paper as `beneish1999detection`; the DOI resolver redirects to the publisher page at tandfonline.com, which returned HTTP 403 to plain curl on 2026-10-27). | L08 section 2, the project's grader constants | OPEN. The constants are labelled UNCONFIRMED everywhere. A person with the paper settles them. |
| Mohanram (2005), Review of Accounting Studies (from recall; title, DOI unverified) | L07 section 5 counter-evidence | OPEN, look up before any citation |
| Dechow, Ge, Larson & Sloan (2011), Contemporary Accounting Research (from recall) | L08 section 5 | OPEN |
| Beneish, Lee & Nichols (2013), Financial Analysts Journal (from recall) | L08 sections 4-5 | OPEN |
| Jones (1991), the original Jones model (from recall) | L06 section 2 | OPEN |
| Roychowdhury (2006), real-activities earnings management (from recall) | L06 section 5 | OPEN |
| SEC documentation of the company-facts API | L01 section 1 states the input shape as the A15 specification, not as a sourced claim | OPEN |
| Passage-level locators in Penman (2013) chapters and Sloan (1996) | C-graded claims in L02-L05 | OPEN, claims stay at grade C with "passage locator not confirmed" |
| `dechow1995detecting`: the registry (Crossref, OpenAlex) lists two authors (Dechow, Sloan) for this DOI while the curriculum string says "Dechow, Sloan & Sweeney (1995)"; plain curl to the publisher page for DOI 10.2308/tar-9505096112 returned HTTP 403 (2026-10-27), so the paper body has not been read | registry/curriculum consistency | OPEN, needs a person with the paper; neither record was changed from memory |
| Out-of-sample tests of the Piotroski F-score outside the 1976-1996 sample (Mohanram 2005 above is a candidate, from recall, unverified) | L07 section 5 | OPEN |
| Joint use of the F-score and the M-score: any study that measures the false-positive rate or sensitivity of combined screening rules on a labelled sample | L08 sections 4-5 | OPEN |
| `mclean2016academic`, `hou2018replicating` (already in the registry) are cited in L05 at grade C, findings not stated | L05 section 4 | Reading them would allow stronger grades |

## GLOSSARY_REQUESTS (terms the lessons define inline; the glossary is generated from the curriculum, so these need a curriculum decision)
annual observation; as-of selection; tag priority; previous year (A15); DuPont leverage factor (A15); NOPAT; invested capital (A15);
operating accruals; earnings and cash-flow quality; cash-flow accrual and balance-sheet accrual; net operating assets;
accruals anomaly; hedge spread; earnings management; nondiscretionary and discretionary accruals; positive predictive value;
false-positive rate, sensitivity, specificity, prevalence; AND rule and OR rule of two screens.

## NOTATION
Plain KaTeX symbols defined locally on a page (tau, kappa, delta, set inclusion, bar, texttt) are allowed; the registered macros in
`notation/notation.json` must not change meaning. No new registered macro was requested.

## CONTRACT (all resolved by the architect in `atlas/A15.contract.md`)
Tie rule on equal (filed, accn) with different values (raise ValueError); the three Piotroski proxies recorded as deliberate; no
`short_term_debt` item (a stated simplification, its size shown in L03); `a1` of `modified_jones` scales with the currency unit,
the residuals and `a2`, `a3` do not; the difference between the balance-sheet and cash-flow accrual measures when short-term debt
sits in current liabilities.

## DAG
AC2 now depends on S2 (S1 through S2): OLS and the t-statistic are used in L05 and L06. Bayes' rule links to the S1 concept
`bayesian-inference`; the law of total probability has no owner in the closure and is proved on the page. `portfolio-sort` (F1,
outside the closure) appears in plain words only.
