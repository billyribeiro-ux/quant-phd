# AC1 open items

Open items for unit AC1 (Financial Accounting). Each section names the builder that raised it. Items are requests to the architect; no shared file was edited.

## Builder C (lessons L07, L08)

### Reference requests

- **FASB Accounting Standards Codification, Topics 718 (stock compensation) and 740 (income taxes).** Needed for the standard-specific rules in L07 §3 and L08 §3. Neither topic is in `references/references.json`. Source: curriculum yaml line 541; `review_queue.json` lines 480-488. Confidence that the keys exist as named: high. Until admitted, L07 and L08 state no measurement or recognition rule for these awards or taxes, and their key-results rows are grade C with basis "standard text not read".
- **IFRS 2 (share-based payment) standard page on ifrs.org.** Needed for the same L07 open item. The issuer index `ifrsndifrs` is in the registry, but it does not carry IFRS 2 content.
- **Income taxes under IFRS.** The build plan names "IFRS 12" for income taxes (plan, REFERENCE_REQUESTS). The income-tax standard is, to the builder's knowledge, IAS 12, and IFRS 12 is a disclosure standard. This is not verified: the architect should confirm the correct standard from the issuer page (`https://www.ifrs.org/issued-standards/`) before any key is added. No page cites either number.

### Gaps (honest)

- L07 §3 and L08 §3: the standard-specific measurement and recognition rules (forfeitures, performance conditions, valuation of awards; recognition of deferred tax assets and any valuation allowance) are not stated. They are not in the registry, and the text has not been read.
- L08: the model has a flat rate and one asset. Changing rates and multi-asset schedules are covered only by proof P3 and the model's stated assumptions.

### Plan defects noticed

- The build plan's L07 and L08 titles for the neighbouring lessons (L06 "Lease accounting (ASC 842 / IFRS 16)") are working titles. L07 and L08 link to L06 and to `project.html` using those titles. The architect should align the L06 title and the project title with the final pages.

## Builder B (lessons L04, L05, L06)

Titles as written: L04 "US GAAP vs. IFRS: Same Transactions, Two Rule Sets"; L05 "Revenue Recognition: Allocating a Price, Timing a Delivery"; L06 "Lease Accounting: A Liability, an Asset and Two Expense Patterns". Builder C's L06 cross-references should use the L06 title above, not the plan's working title.

### Reference requests

- **FASB Accounting Standards Codification, Topic 606 (revenue) and Topic 842 (leases), with the Codification entries for the criteria used in L05 Section 3 and L06 Section 3.** Not in `references/references.json`. Source: curriculum yaml line 541; `review_queue.json` lines 480-488. Confidence that the keys exist as named: high. Until admitted, L05 and L06 state no criterion for identifying obligations, for point or over-time timing, for the measure of progress, for stand-alone prices, for the discount rate, for the initial asset, or for the expense pattern a framework requires. Those questions are marked open on the pages.
- **IFRS 15 (revenue) and IFRS 16 (leases) standard pages on ifrs.org.** Not in the registry. The issuer index `ifrsndifrs` (registry title "IFRS - Issued IFRS Standards") does not carry their content. Needed for the same open questions, and for L04 Section 4.
- **The framework comparison in L04 (which framework requires which timing or classification for a transaction type).** Needs the FASB and IFRS primary texts above. L04 states identities only and cites nothing for the comparison.
- **Not requested:** `penman2013financial` is not cited by any page of L04 to L06.

Builder B did not run `tools/add_reference.py`. BUILDER_RULES §1.9 reserves shared registry writes to the architect, and the architect's decision 2 is the admission path for these keys.

### Data requests

- **A real lessee's lease note and a real entity's revenue note from SEC EDGAR filings (L05 and L06 real example).** Needs the SEC's reuse statement quoted in `tools/data_sources.yaml`, which is the same open item as the AC2 EDGAR request in `plans/AC2-open-items.md`. Until it is read and quoted, both lessons say "honest pending" and every example is SIMULATED.

### Glossary requests (terms defined inline in L04 to L06)

framework difference; timing difference; classification difference; presentation difference; revenue recognition (this unit's three-input mapping); performance obligation (this lesson's convention); point obligation; over-time obligation; allocation in proportion to stand-alone prices (largest-remainder cents); contract balance; contract liability and contract asset (this lesson's sign convention); lease accounting (this unit's model); liability at commencement; right-of-use asset; integer schedule; final-payment adjustment (rounding residual); expense pattern F (front-loaded) and pattern S (straight-line).

### Gaps (honest)

- L04 Section 4 and Remark 1.2: no rule of US GAAP or IFRS Standards is stated. The comparison question is open.
- L05 Section 3: the four standard-specific inputs (separable obligations, point or over-time, measure of progress, observable stand-alone prices) are open. Convention 2 in L05 is a comparison convention, and the page says so.
- L06 Section 3: variable payments, renewal and termination options, modifications, the discount rate choice, initial direct costs and incentives are not modelled. Their treatment is open.
- Lab results are read from SIMULATED runs with one seed each (L04 seed 2604, L05 seed 2605, L06 seed 2606). They are graded C and say so.
- The L05 and L06 labs print integer cents. Their closing identities hold by construction, and the labs say which checks are by construction.

### Plan defects noticed

- The build plan's L05 and L06 rows name ASC 606 / IFRS 15 and ASC 842 / IFRS 16 in the lesson titles. The pages keep the standard names out of the titles and text, because no standard text is registered. The architect should decide whether the titles should carry the standard names once the texts are admitted.

## Builder D (project, grader and project labs)

### Reference requests

- None. The project page cites one registry key, `penman2013financial` (registry record verified; `used_by` AC2 only), on the reading list with no claim and no locator. The project states no accounting-standard rule and grades none.

### Data requests

- None. The project uses only generated ledgers, labelled SIMULATED. The autograder's ledger comes from `grader/instance.py`, and no `data-files` attribute is used.

### Gaps (honest)

- The grader checks the statements against an oracle that reads the seeded entries directly. It does not check any standard's recognition or measurement rule, because the project states none.
- The articulation identities hold for every entry the instance generator produces. A ledger that credits accumulated depreciation by an amount other than the depreciation expense makes `depreciation_gap` nonzero. The specification says so; the suite tests the generated ledgers only.
- Five independent correct implementations were not written. Two were run against the suite: the reference and one alternate written from the specification in a different style. The reference passes 171 of 171 on seeds 0-49 through `run_graders`; the alternate passes 171 of 171 on seeds 0 and 7.
- Mutation testing (`tools/mutate_graders.py`) is the verifier's step. Four plausible wrong solutions were run by the builder against the suite on seed 3 and each failed: the working-capital sign in operating cash flow, the depreciation add-back omitted, dividends not deducted from retained earnings, and a one-month cut-off. The fifth planned mutant (a hard-coded answer for seed 0) was not written.
- Lab 3's ledger is hand-checked on paper for each figure in its interpretation (the retained earnings and the investing and financing sums). Lab 1 and Lab 2 figures were checked by hand as well.

### Dependencies on other builders (checked by hand, not by the hub's gate)

- `project.html` links to `L01.html#def-double-entry-bookkeeping`, `L02.html#def-balance-sheet` and `L03.html#def-statement-articulation`. All three anchors exist in the current pages.
- The hub (`index.html`, Builder A) must declare `data-hours-project="30"`. `check_projects.py` compares the two; the hub did not exist when this section was written, so the comparison was run against the project page itself.
- The lessons must define the balance-through-a-date, month-flow, indirect-method and articulation rules in the same terms as the specification (project page, "Conventions, in brief"). The sign convention for `payables` and `net_borrowing` is the one that matters most.

### Plan defects noticed

- The build plan's time-budget row for lessons (90 h) and the project (30 h) are consistent with this page. No plan defect in the project section.

## Builder A (hub index, lessons L01, L02, L03)

### Reference requests

- **FASB Codification topic on the statement of cash flows, and the IFRS standard on the statement of cash flows.** Not in `references/references.json`. Needed only if a later lesson states a classification or presentation rule of a standard. L02 states the activity split as the lab's convention (Definition 4.1), so no standard is cited there. Confidence that the topics exist: high. The topic and standard numbers are not typed here because they have not been read from the issuer page.
- **FASB Codification topic and IFRS standard on property, plant and equipment, covering depreciation.** Not in the registry. Needed only if L03 Definition 6.1 is to state a rule of a standard. L03 currently states straight-line depreciation as the lab's method (Remark 6.3).

### Data requests

- **An SEC EDGAR filer, for a real-data check of the three-statement identities (L03 exercise R1).** Needs the SEC reuse statement quoted in `tools/data_sources.yaml`, read from the issuer page by a person. This builder did not read it. Same open item as AC2. Until it is supplied, every ledger in L01 to L03 is SIMULATED.

### Glossary requests

Terms defined inline with a plain `<dfn>` (not registered concepts): debit; credit; journal entry; ledger; T-account; trial balance; flow; stock; retained earnings; contra-asset; direct-method cash-flow statement; indirect operating cash flow; straight-line depreciation; residual value; net equipment.

### Gaps (honest)

- L01 to L03 state no standard-specific recognition, classification or measurement rule. Their results are proofs on the page, lab computations on a SIMULATED firm, and stated conventions (grade C with the convention as basis).
- L03 describes amortization and does not compute it: the lab has no intangible asset.
- L03's firm has no taxes, interest, leases or other comprehensive items. The identities are proved without them (L02 Remark 3.3).

### Notes for the architect

- Hub and L03 lesson titles match the L04 to L08 `<h1>` titles as they stood on 2026-10-27.
- `cards.json` is not written by this builder (Builder E). The unit-level `check_pages` run fails only on that file.
- `check_pages.py --page index` treats the hub as a lesson, so the hub is checked through the unit-level run.
