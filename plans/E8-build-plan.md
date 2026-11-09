# E8 build plan: International Macro & the Dollar (2026-11-09)

Unit: **E8 · International Macro & the Dollar** · tier M · 120 h · prerequisites E5 and S2 · no Atlas milestone ·
debate present ("Is UIP failure a risk premium or mispricing?") · grading `both` (autograder for the monitor, rubric for
the memo) · output directory `course/modules/E/E8/` (part code `E`) · lab twins `tests/labs/E8/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Registry facts cite
`references/references.json:LINE` (line of the record's `"key"`). Tooling facts cite the tool file and line. Anything not
in the curriculum, the registry or the tools is marked **NOT IN CURRICULUM**. No bibliographic data is typed from memory.

**Status: BLOCKING ISSUES EXIST (§0.3). Hours are feasible. The curriculum lab and the project data are not: the embedded
snapshots contain spot FX and U.S. yields only. The architect must decide B1 before the builders start.**

Structure follows `plans/E5-build-plan.md` (nearest built prerequisite, sections 0-13) and the architect rulings in
`plans/FINAL-ARCHITECT-RULINGS.md` and `/Users/billyribeiro/.fanout/fixer-rules.md`.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part E, code `E`, title "Economics"; module list E1 to E9 | `curriculum/02-economics-finance-core.yaml:18` (E1), `:271` (E8), `:312` (E9) |
| E8 id `E8`, title "International Macro & the Dollar" | `curriculum/02-economics-finance-core.yaml:271-272` |
| Tier `M`, hours `120` | `curriculum/02-economics-finance-core.yaml:273-274` |
| Prereqs `[E5, S2]` | `curriculum/02-economics-finance-core.yaml:275` |
| Core: "Balance of payments, UIP failure, CIP deviations, the trilemma, Mundell–Fleming, Dornbusch overshooting, the dominant-currency paradigm, the global financial cycle, safe assets and convenience yields." | `curriculum/02-economics-finance-core.yaml:276-279` |
| `introduces` has 12 concepts (mapped to lessons in §1) | `curriculum/02-economics-finance-core.yaml:280-292` |
| Sources: nine free-text strings | `curriculum/02-economics-finance-core.yaml:293-302` |
| Lab: "Fama UIP regression on embedded FX and rate data." | `curriculum/02-economics-finance-core.yaml:303` |
| Project "CIP-basis monitor"; brief "Compute cross-currency bases from public rates and FX data, relate them to quarter-ends and dollar-funding stress, and explain the mechanism."; deliverable "Monitor plus a mechanism memo."; grading `both` | `curriculum/02-economics-finance-core.yaml:304-310` (title 305, brief 306-308, deliverable 309, grading 310) |
| Debate: "Is UIP failure a risk premium or mispricing?" | `curriculum/02-economics-finance-core.yaml:311` |
| No `atlas:` key on the E8 project; no Atlas entry names E8 (planner check: the `atlas` array has 20 entries, none with E8) | `curriculum/curriculum.json` `atlas` array; `curriculum/02-economics-finance-core.yaml:304-311` |
| JSON row for E8 matches the YAML (hours 120, prereqs E5 and S2, debate, project) | `curriculum/curriculum.json:7622` (`"id": "E8"`), `:7663` (debate) |
| E8 is in the CFA "Economics" topic map | `curriculum/meta.yaml:155` |
| E8 is in the Master's and PhD credentials; not in the Bachelor's | planner check: `tools/coursekit.py` `curriculum()["credentials"]`; `curriculum/meta.yaml:63` (BS-FIN `requires`, no E8) |
| X1 (part X) requires E8; X1 covers "UIP and CIP in data" | `curriculum/05-macro-alternatives.yaml:23` (`prereqs: [E8, S3]`), `:25-26` (core text) |
| E9 requires E8 | `curriculum/02-economics-finance-core.yaml:316` |
| Prerequisite closure of E8 (planner, `tools/coursekit.py` `prerequisite_closure("E8")`): **{CS1, E1, E5, M1, M2, M3, M4, P0.1, S0, S1, S2}**, 11 modules, 150 concepts | run output, planner; closure of E5 `{E1, M1, M2, P0.1}` and of S2 `{CS1, M1, M2, M3, M4, P0.1, S0, S1}` (same tool) |
| Modules whose closure contains E8 (so E8 may NOT use their concepts): X1, X2, E9, GM5 | planner check: `prerequisite_closure(m)` contains `E8` for X1, X2, E9, GM5 |
| Built prerequisites: E5 (built, `course/modules/E/E5/`, 10 files), E1 (built). S2 is NOT built (`course/modules/S/` contains S7 only) | `ls course/modules/E`, `ls course/modules/S` |
| No ledger for E8 exists | `ls ledgers/` (no `E8`) |
| E8 topological index 41 (after E5 at 25, S2 at 28) | `curriculum/curriculum.json` `topological_order`, planner check |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 120 h (`curriculum/02-economics-finance-core.yaml:274`). Tool rules:

- lesson `data-hours` 6-12 (`tools/check_pages.py:225-228`);
- hub `data-hours-lessons + data-hours-project = 120` (`tools/check_pages.py:335-338`);
- project share 10-40% of 120, i.e. 12 to 48 h (`tools/check_pages.py:340`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py:342`).

Chosen split: **8 lessons × 10 h = 80 h; project 40 h (33.3%)**. 80 + 40 = 120. Feasible. No STOP condition on hours.

### 0.3 Blocking issues and decisions (architect decision required before builders start)

**B1. The curriculum lab and the project cannot use embedded data as the curriculum describes it.** BLOCKING.
- The lab is "Fama UIP regression on embedded FX and rate data" (`yaml:303`). A UIP regression needs (i) a forward or
  futures exchange rate and (ii) a foreign interest rate, on the same basis as the U.S. rate. Neither is embedded.
- The embedded FX series are **spot rates only**: "Spot rates only: a currency position's return also earns the interest
  differential, which these series do not contain." (`tools/data_sources.yaml`, `fx_daily.note`; the same statement is in
  `fx_monthly.note`). Their columns are AUD, CAD, CHF, EUR, GBP, JPY (daily) and ten currencies monthly
  (`course/assets/data/market/MANIFEST.json`, `fx_daily.columns`, `fx_monthly.columns`).
- The embedded rate series are two U.S. Treasury series, `tbill_3m` (discount basis) and `cmt_10y`
  (`tools/data_sources.yaml`, `ust_daily.transform.series`; `ust_daily.note`). No foreign rate and no forward is embedded.
- The project brief says "public rates and FX data" (`yaml:306-308`). The same gap applies. The cross-currency basis needs
  a forward rate and two money-market rates on one day-count basis. None is embedded.
- BUILDER_RULES §6.6 forbids embedding a series until its issuer's redistribution grant is quoted from the issuer's page.
  The planner did not read any forward-rate or foreign-rate issuer page and names none from memory.
- **Plan's default (architect to confirm or replace):**
  (a) the L03 curriculum lab runs on a seeded **SIMULATED** panel in which the UIP premium is generated, labelled SIMULATED
  on the page, with an honest-pending note that says the embedded snapshots cannot test UIP, and a `DATA_REQUESTS` entry
  (§7.3). The lab keeps the curriculum's name, and its page says what it does not show;
  (b) the project takes its four inputs (spot, forward, USD money-market rate, foreign money-market rate) in
  **bring-your-own-data** mode (BUILDER_RULES §6.6, last bullet): the page documents the CSV schema, and the file never
  leaves the browser. The embedded `fx_daily` spot series is used only in the rung-4 stretch (§5.1), and no embedded series
  is used for the basis itself;
  (c) the architect may instead add a verified redistributable forward and rate source to `tools/data_sources.yaml` first.

**B2. Project wording: "public rates and FX data" (`yaml:306-308`).** Resolve with B1. Default: the word "public" is
read as "data the student supplies or the embedded snapshots", and the page states that no public forward or foreign-rate
series is embedded. No Atlas wording exists in the E8 brief (verified: no `atlas` key, no "Atlas" in `yaml:304-311`), so
the E5-style B2 (Atlas) does not apply.

**B3. Rey (2013) is a curriculum source with no registry record.** NOT blocking, but it must be named.
- `yaml:298` lists "Rey (2013), Jackson Hole Economic Policy Symposium".
- The review queue holds it with the reason "no candidate established identity" and `used_by: ["E8"]`
  (`references/review_queue.json:269`; `references/SEED_REPORT.md:34`).
- Default: E8 does not cite Rey (2013). Global-financial-cycle claims cite `mirandaagrippino2020us` (registered, §7.1).
  Rey (2013) goes to REFERENCE_REQUESTS (§7.2) as a lead only.

**B4. Concepts owned by modules that depend on E8 are forbidden to E8.** NOT blocking; a hard DAG rule.
- X1, X2, E9 and GM5 have E8 in their prerequisite closure (planner check, §0.1). If E8 used their concepts (for example
  `purchasing-power-parity`, `currency-carry-trade`, `dollar-factor`, `sudden-stop`), the curriculum would contain a cycle.
- Default: E8 names none of those concepts, in plain prose or with a link. §4 gives the replacement wording.

Non-blocking flags for the architect:

- **B5. Registry year conflict on one candidate.** `burnside2010peso` is recorded as year 2010, DOI 10.1093/rfs/hhq138,
  RFS 24(3) (`references/references.json:4279`). Its curriculum string (used by X2, not E8) says 2011. If E8 cites this key,
  the page uses the record's year or no year. The registry is not edited.
- **B6. Federal Reserve download change.** `tools/data_sources.yaml` header states that the Board plans to remove its
  "Build Your Package" option "the week of 2026-11-09" (today is 2026-11-09). The snapshots are pinned by SHA-256 and the
  labs read the committed CSVs, so E8 does not depend on a refetch. Builders never run `fetch_data.py --fetch`.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

8 lessons × 10 h = 80 h; project 40 h; total 120 h. Concept counts per row sum to 1+2+1+1+2+1+2+2 = 12, each concept in
exactly one row (`yaml:281-292`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:281-292`) | Lab (twin id, `tests/labs/E8/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Balance of payments and the dollar price of foreign money | `balance-of-payments` | `lab-E8-L01-1`: the accounting identity on a SIMULATED accounts table, sign convention stated; a quote-convention inversion checked exactly in `Fraction` | 10 | Builder A |
| L02 | Covered and uncovered interest parity | `covered-interest-parity`, `uncovered-interest-parity` | `lab-E8-L02-1`: CIP forward computed exactly from spot and two rates; UIP-implied expected spot; closed-form checks, no SIMULATED label (exact) | 10 | Builder A |
| L03 | The forward-premium puzzle and the UIP debate | `forward-premium-puzzle` | `lab-E8-L03-1` (**the curriculum lab**, `yaml:303`, SIMULATED per B1): Fama regression of the spot change on the forward premium on a seeded panel with a generated premium; prints the slope and its standard error | 10 | Builder B |
| L04 | Cross-currency basis: CIP deviations and dollar funding | `cross-currency-basis` | `lab-E8-L04-1`: basis computed exactly from SIMULATED quotes on quarter-end and other dates; the two groups counted and compared | 10 | Builder B |
| L05 | The trilemma and the Mundell–Fleming model | `impossible-trinity`, `mundell-fleming-model` | `lab-E8-L05-1`: the linear model solved exactly in `Fraction` under fixed and floating regimes; the policy multipliers against the solved shifts | 10 | Builder C |
| L06 | Dornbusch overshooting | `dornbusch-overshooting` | `lab-E8-L06-1`: a discrete-time version (§4, D5) iterated and compared with the closed-form jump; the difference printed and stated | 10 | Builder C |
| L07 | The dominant currency and the global financial cycle | `dominant-currency-paradigm`, `global-financial-cycle` | `lab-E8-L07-1`: invoicing-share exposure computed exactly; a SIMULATED common-factor panel with the variance share of the common factor computed in closed form | 10 | Builder D |
| L08 | Safe assets and convenience yields | `safe-asset`, `safe-asset-convenience-yield` | `lab-E8-L08-1`: the yield wedge between two claims with the same cash flows, computed exactly on SIMULATED prices | 10 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 80/40 | none | none | - | Builder A |
| project | CIP-basis monitor (`both`, §5) | none | `lab-E8-project-1` (rung 1), `lab-E8-project-2` (rung 2, `class="lab completion"`), `lab-E8-project-3` (rung 3 check) | 40 | Builder E |
| grader | `grader/` (instance, reference, starter, suite) | none | none | within 40 h | Builder E |
| cards | `cards.json` from L01-L08 | none | none | - | Builder F (after A-E) |

**Ownership rule.** Each lesson builder writes only its lesson files and twins. Builder A writes `index.html` after L01 and
L02 exist. Builder E writes `project.html`, `grader/`, and the three project labs, and depends on no lesson text: the
project's concept list is fixed in §5.2. Builder F writes only `cards.json`.

**Ownership deviation (flagged, §12 Q11).** The brief asks for "about three lessons per builder" across builders A to E.
Eight lessons cannot give three lessons to each of five builders, and builder E owns the project. The recommended split
gives two lessons to each of builders A to D. The 3-3-2 alternative leaves one lesson builder with no lessons and is not
recommended.

**Ordering check (no lesson links a later definition; `tools/check_dag.py` checks linked uses, §4):**
- L01 uses only E5 `national-accounts` (defined at `course/modules/E/E5/L01.html`, the anchor `def-national-accounts`) and M1 `exponential-and-logarithm`.
- L02 uses L01 (`balance-of-payments` only in prose) and M1 `discount-factor`, `present-value`; M4 `expectation`.
- L03 uses L02 (both parity concepts), S2 `hac-standard-errors`, `ols-estimator`, and S1 `sharpe-ratio` only in prose.
- L04 uses L02 and L03 (`uncovered-interest-parity`, `covered-interest-parity`), M1 `compounding-frequency` only in prose.
- L05 uses E5 `is-lm-model` (closure) and L02 `covered-interest-parity` for the open-economy interest link.
- L06 uses L02 (`uncovered-interest-parity`), L05 (`mundell-fleming-model`), E5 `ad-as-model` (closure), M2 `derivative`.
- L07 uses L04 (`cross-currency-basis`) and L01 (`balance-of-payments`); M4 `correlation`, `covariance`.
- L08 uses L07 (`global-financial-cycle`) and L04; M4 `variance`; S1 `estimator` only in prose.

Hours check: 8 × 10 = 80 (hub `data-hours-lessons="80"`); project 40 (hub `data-hours-project="40"`); 120 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to E8)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` (its Architect decisions
section is binding precedent), `plans/FINAL-ARCHITECT-RULINGS.md`, this file. Study `course/modules/E/E5/` (built) and
`course/modules/E/E1/` for layout, the hub grammar and the project grammar. `course/templates/` holds the skeletons.
`course/modules/S/S7/grader/` is the reference autograder layout. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded
   only at display, with the rule stated. This covers every spot rate, forward premium, basis (in basis points), index and
   multiplier. Precedent: AC4 KNOWN LIMITATION 3; CF1 L01 Remark 5.2; E5 §2.1 item 1.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. A slope from SIMULATED data is not evidence about real currencies, and the page says so.
   Precedent: M1 LESSON_TEXT_DEFECTS; E5 §2.1 item 2.
3. **Attribute nothing unread.** Only registry keys listed in §7.1 may be cited. A key is cited at paper or book level unless
   the builder has read the abstract; a locator (`data-locator`) needs the locator read in the source. No page, table,
   equation, coefficient, sample period or currency list is typed from memory. Precedent: E5 §2.1 item 3.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "the dollar", "all currencies", "markets",
   "central banks", "safe assets" are used only where a derivation, a finite check or a lab computes the claim.
   Scope of E8 (proposed; architect confirms, §12 Q7): six currencies in the embedded FX snapshot and any currency the
   student supplies; closed-form and discrete-time models; the Mundell–Fleming and Dornbusch models are the textbook
   linear models of §3, not the New Keynesian models of E6; no exchange-rate forecasting claim beyond the cited evidence.
5. **Define before use.** Each of the 12 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, never earlier. Plain terms (§3, "plain dfn") are defined with `<dfn>` and no `data-concept`
   (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation lists its numbered Assumptions (A1, A2, ...)
   before the statement. Required: CIP needs no-arbitrage with proportional transaction costs set to zero (A stated);
   UIP needs risk neutrality or a stated premium term; the Mundell–Fleming solution needs the slopes to make the system
   non-singular; the Dornbusch closed form needs its speed-of-adjustment and the stated sticky-price assumption; the
   Keynesian-style convergence needs its stated bounds.
7. **Grader rule.** APPLIES (E8 is autograded, §5.3). Enumerate every condition, boundary and error type the page states for
   each graded function; give each its own isolated test, in both directions of every inequality; a test may demand an
   exception only for a condition the page names (fixer rules; FINAL-ARCHITECT-RULINGS 9-10, 35-37).
8. **Money.** The monitor outputs basis in basis points and rates in percent or decimal; there is no money output. If the
   optional notional P&L is added, it is an integer number of cents (BLUEPRINT §3 guardrails; fixer rules "Money is integer
   cents"). Default: no money output (§12 Q13).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; quiz options use `min-inline-size:0`; `$` is escaped as `\$` inside math (fixer rules).
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `tools/run_labs.py` runs each twin as `python -I -W error <twin>` with no network
    (`tools/run_labs.py:51-60`). `tests/labs/M1/lab-M1-L04-1.py` is the model.
11. **Rates and yields are basis-explicit.** Every rate or yield states its unit (percent per year or decimal), its
    compounding (simple, periodic, continuous), its day-count, and its source. The U.S. 3-month bill is on a discount basis
    (`tools/data_sources.yaml`, `ust_daily.note`); a page that uses it states the basis and does not mix it with a
    money-market rate without a stated conversion.
12. **Quote convention is fixed on every page.** Spot and forward rates are USD per unit of foreign currency, the convention
    of the embedded snapshots (`MANIFEST.json`, `fx_daily.transform`: CAD, CHF, JPY inverted "to USD per unit"). A page that
    uses another convention states it and the inversion.
13. **Sign conventions are stated once.** The forward premium, the basis and the CIP deviation each state a sign and an
    example. A sign error is a student error in the grader (§5.5).
14. **Honest-pending.** Where a source is not admitted, the lesson or project says so in one visible sentence, and it names the
    DATA_REQUEST or REFERENCE_REQUEST. Precedent: LX1 L04 ruling 14 (FINAL-ARCHITECT-RULINGS 14).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded claim
  names its published counter-evidence (BUILDER_RULES §2.5). The debate (§3, L03) grades both sides.
- Concepts: §1 table for the 12 owned concepts; plain `<dfn>` for other terms (§3 lists them per lesson). No
  `<a class="concept">` for any concept outside the closure {CS1, E1, E5, M1, M2, M3, M4, P0.1, S0, S1, S2} (§0.1).
- Prerequisite links: `href="../../../concepts.html#<id>"` for closure concepts (E5 and S2 included; S2 is not built, so no
  S2 page link exists). E5 is built, so a link to `../E5/Lnn.html#def-<id>` is allowed when the anchor exists (the
  builder greps the E5 page first). A lesson never links a concept defined in a later lesson.
- Labs: code lives once in `tests/labs/E8/lab-E8-Lnn-1.py` and `lab-E8-project-1..3.py`. The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-E8-<page>-<n>`
  (`tools/check_pages.py`, `check_lesson`). Standard library only (`fractions`, `math`, `random.Random(seed)`, `decimal` if
  used); seeded RNG only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab or figure that uses generated data (L03, L04, L07 common-factor panel, L08 prices, the
  project's worked example and exemplars). Exact closed-form labs (L01, L02, L05, L06) are not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments.
- Banned strings (`tools/check_pages.py:58-72` `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Growth and depreciation rates state the convention (log or simple,
  annual or per period).
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols and macros that E8 must not give a different meaning (`notation/notation.json`, `symbols` and `macros`):

| Registered item | Registered meaning (locator) | E8 conflict and rule |
|---|---|---|
| `T` | number of return observations (`notation.json`, module S1) | **Do not use bare `T`** for a time horizon or a tenor. Tenor in days is `d`; the horizon is `H`. |
| `R_f` | gross riskless return (AP1) | Not used. Interest factors are written `1 + i\tau` with the rate `i` and the accrual fraction `\tau`. |
| `R^\ast`, `R^{e\ast}` | SDF payoff-space returns (AP1) | Not used. Foreign rates are `i^\ast`; never `R^\ast`. |
| `\mathbb{Q}` | risk-neutral measure (AP1) | Not used. Risk-neutral expectation is written `\E` with a note, not `\mathbb{Q}`. |
| `\Phi`, `\gamma_3`, `\gamma_4` | M4 registrations | Not used. |
| `\E` (macro) | expectation operator | Used for expectations of random quantities (expected depreciation, `\E_t[S_{t+1}]`). |
| `\Cov`, `\Corr`, `\Var` (macros) | covariance, correlation, variance | Used as registered. |
| `\se` (macro) | standard error | Used for the Fama-regression standard error in L03. |
| `\indic` (macro) | indicator function | Used for quarter-end flags. |
| `\R` (macro) | real numbers | Standard. |

Local symbols (allowed; each defined on the lesson where first used and never redefined): `S_t` spot (USD per unit of
foreign currency), `F_t` forward exchange rate on the same convention, `i` U.S. nominal rate, `i^\ast` foreign nominal rate,
`\tau` day-count accrual fraction, `d` days to maturity, `b_t` cross-currency basis, `\Delta s_{t+1}` the log change of the
spot rate, `f_t - s_t` the forward premium, `y` output, `e` the nominal exchange rate in the Mundell–Fleming lesson (USD per
unit), `\Delta` and `\beta` in the regression. `\tau` is also the tax rate in E5 (`plans/E5-build-plan.md` §2.3); the two
meanings are in different modules and E8 defines `\tau` locally on L02. **Open (§12 Q12):** confirm, or rename the accrual
fraction to `\theta` if the verifier reads the E5 collision as a defect.

NOTATION_REQUESTS: none. The plan uses local symbols and registered macros only.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the BUILDER_RULES §4.2 structure. Mandatory content, by lesson:

- **L01 `balance-of-payments`.** The accounting identity (current account, capital and financial accounts, with the sign
  convention stated once) derived from the definition of a payment (T, identity by definition). The link between the trade
  balance and national income, using the E5 concept `national-accounts` (closure). Quote convention: USD per unit of foreign
  currency (§2.1 item 12). Plain dfns: current account, financial account, trade balance, and the spot rate. Lab checks the
  identity and the inversion exactly. No registry key is needed for the identities (grade T, derived on the page). "Where the
  canon breaks": the identity holds by construction; the measurement errors in balance-of-payments statistics are not
  modelled here and the page says so.

- **L02 `covered-interest-parity`, `uncovered-interest-parity`.** CIP: no-arbitrage between a forward contract and two
  deposits, with assumptions (no transaction costs, no default, deposits of equal maturity). Derivation of the CIP forward
  rate from spot and the two rates (T, under the stated assumptions; the day-count is stated per leg). UIP: the expected
  change in the spot rate equals the interest differential when investors are risk-neutral (a stated assumption A-UIP); the
  premium term is introduced as the deviation of the forward premium from expected depreciation, defined in plain prose
  (`risk-premium`, plain dfn, §4 D2). Expectations use `\E` (M4 `expectation`, closure). Empirical claims about CIP holding in
  practice are not made here; they are deferred to L04 and graded there. The lesson's Misconceptions include: "CIP is an
  empirical regularity, not an arbitrage condition" (the wrong belief) and why (the identity, with the assumptions).

- **L03 `forward-premium-puzzle`.** The Fama regression `\Delta s_{t+1} = \alpha + \beta (f_t - s_t) + \varepsilon_{t+1}`
  (defined; the regression is a model, not a result). Under UIP with a constant premium, `\beta = 1`; the puzzle is the
  finding that the estimated slope is different from one, graded only after the builder reads the Fama (1984) abstract
  (`fama1984forward`). Standard errors: S2 `hac-standard-errors` and `ols-estimator` (closure). The **curriculum lab** is
  here, SIMULATED per B1, with the honest-pending sentence. The DEBATE BRIEF is here (see the next paragraph). Misconceptions
  (at least 3): "a slope of 1 is required by any model" (false: it is required by a model with risk neutrality); "a
  negative slope means investors are irrational" (not shown; the model admits a time-varying premium); "the puzzle is
  solved by using a different sample" (the sample dependence needs the source).
  - **Debate brief (required; `yaml:311`; `tools/check_pages.py:412-413` requires a `section.debate` in some lesson).**
    Resolution: "Is UIP failure a risk premium or mispricing?" Sections: the resolution; strongest case for a risk premium;
    strongest case for mispricing (or limits to arbitrage); graded evidence on both sides; the state of the literature;
    what evidence would settle it. Candidate keys, all registry-verified but **not read by the planner**: for the risk-premium
    side `lustig2011common`, `brunnermeier2008carry`, `menkhoff2012carry`, `menkhoff2012currency`, `verdelhan2017share`,
    `koijen2018carry`; for the mispricing side `du2018deviations` (curriculum source, CIP deviations), `jiang2021foreign`
    (curriculum source), `krishnamurthy2012aggregate` (curriculum source), `he2022treasury`; a counter-argument to
    carry-based premia: `burnside2010peso` (peso-problem explanation; B5 year note). Freshness (BLUEPRINT §3): the debate needs
    2025-2026 work. The registry holds `bis2025triennial` (2025, primary) and `bis2024market` (2024, primary); neither is read
    yet. No 2025-2026 academic paper on UIP is identified in the registry, so a REFERENCE_REQUEST (§7.2) is raised. Both sides
    are graded B or C with the counter-evidence named (BUILDER_RULES §2.5).

- **L04 `cross-currency-basis`.** The basis as the CIP deviation: the difference between the observed dollar rate implied by
  the forward and the dollar money-market rate, with the sign and the day-count stated (§2.1 item 13). Empirical claims
  about the basis after 2008 and at quarter-ends are graded C or B, with registry keys: `du2018deviations` (curriculum
  source) and the BIS primaries as candidates only. The mechanism is described in plain prose (dollar funding through FX
  swaps; dealer balance-sheet capacity) with no FI4 concept link (§4 D7). Lab: SIMULATED quotes; the quarter-end and other
  groups are counted and compared. Where the canon breaks: the basis is an observed deviation with frictions (balance-sheet
  costs, counterparty risk), which the CIP identity of L02 does not contain.

- **L05 `impossible-trinity`, `mundell-fleming-model`.** The trilemma as a consequence of the interest-parity condition plus
  the three policy choices (fixed rate, free capital flows, independent policy rate), derived in the linear model (T under
  stated assumptions). The Mundell–Fleming model as the IS-LM-BoP system with a fixed or floating rate, solved exactly for a
  linear specification. Concept links: E5 `is-lm-model` (closure). Names of the model's authors appear only as the concept
  name; no attribution is made (§7.2 REFERENCE_REQUESTS). The trilemma is cited at book level (`obstfeld1996foundations`).
  Where the canon breaks: the model has fixed prices and no expectations; the E6 New Keynesian model is not used.

- **L06 `dornbusch-overshooting`.** A monetary expansion with sticky goods prices and UIP makes the exchange rate jump above its
  new long-run level and then return. The continuous-time saddle-path solution uses ODE methods that no closure concept
  supplies (§4 D5), so the lesson derives a discrete-time version with the same overshooting logic and states the continuous
  result only as a cited result graded B with `dornbusch1976expectations`, or as a plain statement that the page does not
  derive it. The lab compares the discrete iteration with the closed form and prints the difference with its tolerance.
  "Where the canon breaks": perfect foresight, a closed economy and a single good; the rational-expectations term is not used
  (E4 concept, §4 D6). The long-run relation uses no concept link: the real exchange rate is constant in the long run is
  plain prose (§4 D1).

- **L07 `dominant-currency-paradigm`, `global-financial-cycle`.** The dominant-currency paradigm: most trade is invoiced in a
  few currencies, so a currency's exchange rate matters for the prices of trade it does not invoice. Exposure is computed
  exactly for an invoicing-share example (T, identity by definition). The global financial cycle: a common factor in
  cross-border capital flows and asset prices, and the claim that U.S. monetary policy moves it, graded only after reading
  `mirandaagrippino2020us` (registered, `references/references.json:17450`). Variance shares are computed with `\Var` and
  `\Cov` (M4 closure). The identification of policy shocks is described in words (no E7 concept link, §4 D8). Where the canon
  breaks: the common-factor claim is an association in a sample and the page says what the sample is.

- **L08 `safe-asset`, `safe-asset-convenience-yield`.** A safe asset: an asset whose payoffs are not sensitive to the
  state, which makes its price higher than the price of a claim with the same cash flows and some risk. The convenience
  yield as the wedge between yields of two claims with the same cash flows, computed exactly (T, identity under the stated
  assumption that the cash flows are identical). Empirical evidence on Treasury convenience yields: `he2022treasury` and
  `krishnamurthy2012aggregate` (both registry-verified; `krishnamurthy2012aggregate` is a curriculum source) and
  `jiang2021foreign` (foreign safe-asset demand and the dollar). Each is graded at most B and the counter-evidence is named.
  Misconception examples (planner proposals, graded when written): "Treasuries are riskless"; "a convenience yield is a
  commodity storage yield" (the commodity concept is X3-owned: §4 D9, not used). Cards for this lesson cite only what is read.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it.
- No lesson uses a term from E6 (New Keynesian, determinacy, Taylor principle), E7 (high-frequency surprise, local
  projections), E9 (sudden stop, currency-crisis models, sovereign default), X1, X2 (purchasing-power parity, carry
  trade, dollar factor) or X3 (commodity convenience yield) as a concept (§4).

---

## 4. DAG problems (concepts that natural E8 content would use outside the closure)

Prerequisite closure of E8 (computed, §0.1): **{CS1, E1, E5, M1, M2, M3, M4, P0.1, S0, S1, S2}**, 150 concepts. Owners
below are from `curriculum/curriculum.json` `concepts` (planner check with `tools/coursekit.py` `concept_owner`). Topological
index from `curriculum/curriculum.json` `topological_order`. "E8 in closure of owner" is the planner's computed check.

| Ref | Concept or term | Owner (outside closure) | Topo index; E8 in owner's closure? | Where natural E8 content would use it | Resolution in this plan |
|---|---|---|---|---|---|
| D1 | `purchasing-power-parity`, `ppp-half-life` | X1 | 71; **yes (cycle)** | Dornbusch long-run level; real exchange rate | **Forbidden as a concept.** Plain prose: "the real exchange rate is constant in the long run" stated as the assumption the model imposes. No link. |
| D2 | `risk-premium` (no concept of that name in the curriculum; `equity-risk-premium` is AP2's) | none | - | UIP premium (L02, L03) | Plain dfn in L02. No link. |
| D3 | `forward-rate` (bond concept), `term-spread`, `yield-to-maturity`, `bond-price-yield` | FI1 | 18; no | forward exchange rate; yield comparisons (L08) | Use the phrase "forward exchange rate" (plain dfn) and never the bare "forward rate" on E8 pages (name collision with FI1). Yields are plain prose with the basis stated (§2.1 item 11). |
| D4 | `interest-rate-swap`, `forward-contract`, `cost-of-carry-forward-price`, `put-call-parity` | FC2 | 30; no | the CIP forward as a cost-of-carry price (L02) | Plain prose derivation from two deposits. No link. Alternative: add FC2 as a prerequisite (§12 Q6). |
| D5 | ODE and saddle-path methods (no concept in the curriculum; `linear-difference-equation`, `perfect-foresight` also absent) | none | - | continuous-time Dornbusch solution (L06) | Discrete-time version only (L06); the continuous result is cited at paper level and graded B, or the page says it is not derived. §12 Q5. |
| D6 | `rational-expectations-equilibrium` | E4 | 29; no | Dornbusch expectations (L06) | Not used. Expectations are stated as perfect foresight in the discrete model (plain prose; no concept). |
| D7 | `sofr`, `bank-reserves`, `repo-haircut`, `dealer-balance-sheet-constraint`, `central-bank-balance-sheet`, `swap-spread`, `treasury-basis-trade` | FI4 | 33; no | dollar funding and dealer capacity (L04, L08) | Plain prose descriptions with no links. Alternative: add FI4 as prerequisite (§12 Q6). |
| D8 | `high-frequency-monetary-surprise`, `portfolio-balance-channel`, `local-projections`, `narrative-shock-identification` | E7 | 74; no | U.S. policy shocks and the global financial cycle (L07) | Not used as concepts; describe the identification in words; cite `mirandaagrippino2020us` at paper level. §12 Q6. |
| D9 | `commodity-convenience-yield` | X3 | 125; no | a name collision with `safe-asset-convenience-yield` (L08) | Not used. The E8 concept is named in full on every use ("convenience yield on safe assets"). |
| D10 | `currency-carry-trade`, `dollar-factor`, `global-fx-volatility-risk`, `hml-fx`, `fx-momentum`, `fx-value` | X2 | 124; **yes (cycle)** | the debate's carry evidence (L03) | **Forbidden as concepts.** Describe the strategy in plain words ("borrow in a low-yield currency and lend in a high-yield one"); cite `lustig2011common` and the other carry keys (§7.1). |
| D11 | `sudden-stop`, `currency-crisis-models`, `sovereign-default-model`, `banking-crisis` | E9 | 92; **yes (cycle)** | capital-flow reversals (L07, L08) | **Forbidden as concepts.** No E9 term is used; crisis episodes are not discussed. |
| D12 | `bretton-woods-system` | LX1 | 36; no | the historical fixed-rate system for the trilemma (L05) | Plain prose "a fixed-rate system" only. LX1 L04 holds this concept as "definition pending" (FINAL-ARCHITECT-RULINGS 14), so it is not a usable definition. |
| D13 | `new-keynesian-model`, `taylor-principle`, `equilibrium-determinacy`, `new-keynesian-phillips-curve` | E6 | 55; no | policy rules in open economies (L05, L06) | Not used. Architect may ask for an E6 link; default no. |
| D14 | `fisher-relation` | CF1 | 11; no | nominal versus real rates in UIP with inflation (L02, L06) | Plain prose only; the relation is derived on the page if used (T). No link. |
| D15 | `stochastic-discount-factor`, `arbitrage-linear-program` | AP1 | 64; no | a pricing-kernel reading of the UIP premium (L03) | Not used. The premium is described as an expected excess return (M4 `expectation`, closure). |
| D16 | `libor-sofr-transition`, `libor-market-model`, `multi-curve-discounting` | FI6 (FI2) | 93; no | rate-benchmark choice for the basis (L04) | Not used. The money-market rates are "the dollar and foreign money-market rates", with the day-count stated. |
| D17 | `dynamic-programming`, `principle-of-optimality` | CS2 / M7 | n/a | none | Not used. |
| D18 | `expectation`, `variance`, `covariance`, `correlation`, `conditional-expectation-elementary`, `normal-distribution` | M4 | in closure | expected depreciation, variance shares (L02, L07) | **In closure; used with links.** |
| D19 | `ols-estimator`, `ols-asymptotics`, `hac-standard-errors`, `omitted-variable-bias`, `coefficient-of-determination`, `frisch-waugh-lovell-theorem` | S2 | in closure | the Fama regression (L03) | **In closure; used with concepts.html links** (S2 has no built page). |
| D20 | `discount-factor`, `present-value`, `compounding-frequency`, `exponential-and-logarithm` | M1 | in closure | CIP discounting and log changes (L01, L02) | **In closure; used with links.** |
| D21 | `national-accounts`, `is-lm-model`, `ad-as-model`, `business-cycle`, `policy-rate` | E5 | in closure (E5 built) | identity link (L01); IS-LM (L05); AD (L06) | **In closure; used with links** to the E5 lesson anchors if they exist (builder greps first), else to `concepts.html`. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Rows D1, D10 and D11 are cycle prohibitions and need no
architect decision; the others need the architect's confirmation (§12 Q4-Q6).** `tools/check_dag.py` checks linked uses
only (`tools/check_dag.py` docstring); an unlinked use of D1-D13 passes the tool, so the verifier reads every lesson for
these names (VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): autograded and rubric-graded (`both`), ladder, spec, rubric, grader

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` `RUNGS` order)

1. **Rung 1, worked example** (`lab-E8-project-1`, SIMULATED): one fully solved, annotated computation of one day's
   cross-currency basis from a generated quote row, every step with a "why" annotation, and the quarter-end flag for that
   date. Full length (tier M: rungs 1-2 kept to the minimum, BUILDER_RULES §5.1).
2. **Rung 2, completion** (`lab-E8-project-2`, `class="lab completion"`, SIMULATED): the day-count line and the sign line of
   the basis function are blanked (`___`). Graded instantly. Its twin is the completed solution; every page line equals the
   twin line or contains a blank (`tools/run_labs.py` docstring). `tools/check_projects.py:89-90` requires a completion lab or a quiz.
3. **Rung 3, independent project** (graded by autograder and by rubric): the monitor (`monitor.py`) and the mechanism memo
   (`memo.md`), built from the four inputs in §5.2. `lab-E8-project-3` is the rung-3 check: it recomputes the default
   instance from the reference and prints the table the monitor should show.
4. **Rung 4, stretch** (optional, not graded): the same monitor on the embedded `fx_daily` spot series with a user-supplied
   forward series. The stretch reads `fx_daily.csv` through `data-files` (BUILDER_RULES §6.6) only if the builder lists it
   there; no basis is computed from embedded data alone.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py:34` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A macro-finance analyst must report whether the cross-currency basis for one dollar pair widened on
  quarter-ends and in stress weeks, and explain the mechanism. Four inputs and fixed conventions turn the data into a
  monitor and a memo.
- **Inputs.** Four daily series, each a CSV that the student supplies (bring-your-own-data; the schema is on the page and the
  file never leaves the browser; B1):
  1. spot rate, USD per unit of foreign currency (`date, spot`);
  2. forward rate for one stated tenor on the same convention (`date, forward`);
  3. the dollar money-market rate for the same tenor, percent per year (`date, usd_rate`);
  4. the foreign money-market rate for the same tenor, percent per year (`date, foreign_rate`).
  Every row has a date in ISO form; a missing or non-numeric value is invalid (§5.5, failure behaviour). The page documents
  the schema; the validation is run by the grader's suite on a student file (E5 open item: no browser validator exists in
  `course/assets/js`; the page says so and the architect decides, §12 Q7).
- **Conventions (fixed by the page; the architect approves, §12 Q8).** Day count per leg stated on the page (default
  proposal: actual/360 on both legs; the planner does not assert this is the market convention, the architect decides).
  Accrual `\tau` = days / basis per leg. The basis in basis points, sign as stated in L04. Quarter-end: the last weekday
  (Monday to Friday) of March, June, September or December; no holiday calendar (stated). Rounding: no rounding inside
  functions; display rounds to 0.1 bp with the rule stated.
- **Required outputs.**
  - `monitor.py` exposing the functions in §5.4, typed, with docstrings that state units;
  - `memo.md`, a memo of at most two pages that states the basis on quarter-end and non-quarter-end dates for the student's
    data, the count of observations in each group, and the mechanism with its evidence.
- **Constraints.**
  - Every number in the memo cites the series, the date range and the convention that produced it (§5.4 rubric 1).
  - No claim about data beyond the supplied file's coverage.
  - Standard library only; the browser suite runs under Pyodide with no extra packages (`data-packages=""`, §11).
  - No Atlas series is used (E8 names no Atlas milestone).
- **Grading.** Both: the autograder grades `monitor.py` (`grader/test_project.py` in Pyodide and locally), and the rubric grades
  `memo.md` (`rubric-self`, §5.6). The spec's grading entry names both words "autograder" and "rubric"
  (`tools/check_projects.py:38` `GRADING_WORDS`; `:41-50` `grading_problems`).
- **Reading list.** `ol.reading-list`: `du2018deviations`, `fama1984forward`, `lustig2011common`, `mirandaagrippino2020us`,
  `krishnamurthy2012aggregate`. Registry keys only (§7.1). Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 40 h; a one-line rationale on each row; `tools/check_projects.py:58-73` and the hours check)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED quote row, annotated line by line |
| Rung 2, completion problem | 3 | Fill the day-count line and the sign line, then run the instant check |
| Data intake: the four CSV schemas, the validation rules, the conventions statement | 6 | Document the schemas, validate a student file, state each leg's day count and the sign |
| Monitor implementation to the spec (§5.4 functions) | 12 | Implement the basis, the quarter-end flags and the table to the stated signatures |
| Suite runs (local pytest and the browser run) and fixes | 6 | Read each failure message, fix the named property, rerun both modes |
| Mechanism memo | 8 | Two pages; every number cited with its series, date range and convention |
| Self-assessment against exemplars | 3 | Score the memo with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **40** | Equals `data-hours-project` on the hub |

### 5.4 Autograder design (`grader/`; `tools/check_projects.py:122-137`; `tools/run_graders.py`; `tools/mutate_graders.py`)

Panel attributes (`section.grader-panel#grader`, in `project.html`): `data-unit="E8"`, `data-grader="grader/"`,
`data-suite="test_project.py"`, `data-support="instance.py"`, `data-solution="reference.py"` (the reference is not published;
`course/modules/S/S7/project.html:188` is the pattern), `data-starter="starter.py"`, `data-packages=""`. The data-solution
attribute names a file that the deploy step excludes (BLUEPRINT §7; ruling 4: no deploy step yet).

Functions the student implements (the signatures are the contract; the builder states them on the page):

- `implied_usd_rate(spot, forward, foreign_rate, tau_usd, tau_foreign) -> float`: the dollar rate implied by the forward
  and the spot with the foreign leg accrued; units decimal per year; raises `ValueError` for a non-positive spot or forward
  and for a non-positive accrual fraction (the page names these two conditions, and only these).
- `cross_currency_basis_bp(spot, forward, usd_rate, foreign_rate, tau_usd, tau_foreign) -> float`: the basis in basis points,
  sign as stated on the page (observed minus implied, or the reverse, fixed by the page).
- `is_quarter_end(date_iso) -> bool`: the last weekday of March, June, September or December.
- `monitor_table(rows) -> list[dict]`: one dict per row with the date, the basis and the quarter-end flag; raises `ValueError`
  on a missing or non-numeric field (the page names this condition).

**`grader/instance.py`**: `make_instance(seed: int) -> dict` (a required name; `tools/check_projects.py:136`). Deterministic
for each seed; generates a SIMULATED panel of about 60 business days, with quarter-end dates, two weekend quarter-end dates in
some seeds (boundary), a stressed window, and an instance-specific set of true bases so that the answers change with the
seed, not only the labels. Generates only valid instances. `tools/run_graders.py` checks that instances differ across seeds
(`check_instances`, `run_graders.py:79-103`).

**`grader/reference.py`**: the full solution, stdlib only. Must pass all tests for seeds 0 to 49 (`tools/run_graders.py
--seeds 0-49`).

**`grader/test_project.py`** (pytest). Tests check properties and numbers, not hard-coded answers:
- the identity test: with the forward set to the CIP forward for a zero basis, `cross_currency_basis_bp` returns 0 within 1e-9 bp;
- sign: a planted basis of +x bp returns +x bp, and a planted −x bp returns −x bp (both directions);
- units: a planted basis of 5 bp returns 5 (not 0.0005);
- day-count: two cases with the same rates and 90 versus 91 days on the USD leg differ by the expected factor (the expected factor is computed in the test from the stated convention);
- quote inversion: the same economics quoted the other way gives the same basis on the stated convention;
- quarter-end: a weekend quarter-end is flagged according to the stated rule (the last weekday), in both directions;
- no lookahead: changing the next row's forward does not change the current row's basis;
- invalid input: a zero or negative spot raises `ValueError`; a non-numeric field raises `ValueError` in `monitor_table`; a
  valid row is not rejected (the other direction of each inequality);
- determinism: the same seed gives the same instance;
- performance: the suite runs under 5 s per test in Pyodide and under 60 s in total.
Failure messages name the violated property and the concept hint and never print the expected value (`__tracebackhide__`
and no expected-value print, fixer rules).

**Ten student-error mutants** (`ledgers/E8/mutants/`, each a single-change copy of `reference.py` whose first docstring line
names the error; `tools/mutate_graders.py` reads them and requires at least three, `tools/mutate_graders.py` `mutate`):
1. "Uses 365 as the USD-leg basis where the page states the 360 basis for both legs."
2. "Divides the spot by the forward instead of the forward by the spot (inverted quote)."
3. "Drops the foreign-leg accrual factor from the implied rate."
4. "Takes the basis sign as implied minus observed where the page defines observed minus implied."
5. "Returns the basis as a decimal where the page requires basis points."
6. "Uses the next row's forward in the current row's basis (one-row lookahead)."
7. "Flags the last calendar day of each quarter as quarter-end, ignoring weekends."
8. "Skips rows with a missing or non-positive quote instead of raising ValueError (silent drop)."
9. "Returns the seed-0 table values for every seed (hard-coded answer)."
10. "Compounds the foreign leg annually, (1 + i*)^tau, where the page specifies simple accrual (1 + i* tau)."

Each must fail at least one test on at least one seed in 0-9. A mutant that differs from the reference only where the page
states nothing is moved to `ledgers/E8/equivalent/` with a README proof (ruling 9). Mutant 8 (skipping rows) must be killed
only if the page names the ValueError (§5.4 invalid-input bullet); if the page does not name it, the mutant is equivalent
on the page's stated contract and the README says so (ruling 9).

**Five alternative correct implementations** (`ledgers/E8/alternatives/`, all stdlib, all in different styles; each must
pass seeds 0-49; ruling 10, and a float-based alternative wrong on a stated exact rule is a mutant, not an alternative):
1. `fraction_exact.py`: exact `fractions.Fraction` arithmetic, rounding only at output.
2. `decimal_context.py`: `decimal.Decimal` with an explicit context, quantized only at output.
3. `dataclass_rows.py`: frozen dataclass rows and a validation layer that raises `ValueError` on the named conditions.
4. `streaming.py`: a single-pass generator with a state dictionary for the quarter-end flags.
5. `functional.py`: `functools.reduce`, `map` and closures; no classes.

### 5.5 Failure behaviour and invalid input

- Failing tests name the violated property (for example "the basis changes sign when the observed rate is mirrored") and
  give a concept hint ("check the order of the two legs in the definition"). They never reveal the answer.
- Only the conditions named on the page raise an exception; no other input is rejected (fixer rules: a TypeError from a
  correct implementation must pass unless the page says so).

### 5.6 Rubric (`table.rubric#rubric`; `tools/check_projects.py:58-73` `rubric_problems`)

Five criteria, one table row each, with exactly four level cells from level 4 down to level 1. Every descriptor is observable.

1. **Data and conventions.** Level 4: names each of the four inputs with its tenor, quote convention, day count per leg, and
   the source (student file or SIMULATED); states the sign convention. Level 1: "uses the data".
2. **Basis computation.** Level 4: states the formula the monitor uses, applies it to a stated row with unrounded values, and
   checks the sign with a planted case. Level 1: "computes the basis".
3. **Quarter-end analysis.** Level 4: lists the quarter-end dates in the sample, states the flag rule, and compares the basis
   on quarter-end and other dates with the counts in each group. Level 1: "discusses quarter-ends".
4. **Mechanism.** Level 4: explains the mechanism (dollar funding through FX swaps, dealer balance-sheet capacity) in words
   with a registry key for each empirical claim, and says what the sample does not show. Level 1: "explains the mechanism loosely".
5. **Limits and evidence.** Level 4: names each claim graded B or C with its counter-evidence key, and states the monitor's
   limits (no holiday calendar, quote quality, the SIMULATED path if used). Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**: fully written memos on a SIMULATED
panel, annotated with the descriptors each passage meets or misses (`data-score`, `data-score-s` attributes as in E5). The
self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`).
Calibration: a dedicated blind scorer scores both exemplars with a stripping script (FINAL-ARCHITECT-RULINGS 15 and 23),
within one level on every criterion.

### 5.7 Question bank

Not required. The project is not an adversarial review (no IC defence, debate or referee report), so no 15-angle
question bank is needed (`tools/check_projects.py` checks a question bank only if `id="question-bank"` exists). §12 Q12
confirms the default. The debate lives in L03 as a lesson brief, not in the project.

---

## 6. Real-data policy (B1 applies)

- **Embedded (redistributable, grant quoted, checked in `tools/data_sources.yaml`):** `fx_daily` (six currencies, daily,
  2000-01-03 to 2026-09-30; spot only), `fx_monthly` (ten currencies, month-end, 1971-01 to 2026-09; spot only), and
  `ust_daily` (`tbill_3m`, discount basis; `cmt_10y`). Source: `tools/data_sources.yaml:18-116`; `MANIFEST.json`.
  The licence sentence is the Board's "public domain" statement (`fx_daily.licence`, `ust_daily.licence`).
- **What the embedded data cannot do for E8:** test UIP or CIP (no forward, no foreign rate); compute a basis (no forward,
  no foreign rate); measure convenience yields (no safe-asset comparator). Stated on L02, L03, L04 and the project page.
- **Not embedded, and no grant found:** forward exchange rates; foreign money-market rates; the dollar money-market rate on the
  same basis as the forward tenor; BIS or other statistics on FX swaps. `tools/data_sources.yaml` `rejected:` (lines 119-)
  lists only the French library and Open Source Asset Pricing; no entry exists for these series.
- **Honest-pending note** on L03 and on the project's data section: "The curriculum names an embedded-data lab for this topic.
  The embedded snapshots hold spot exchange rates and U.S. Treasury yields only, so the forward and foreign-rate inputs this
  test needs are not embedded. The lab runs on a seeded SIMULATED panel, labelled SIMULATED." Cited to the DATA_REQUESTS (§7.3).
- **Candidates only (BLUEPRINT §5.3):** FRED series under their owners' terms, BIS statistics where the terms permit, and
  central-bank releases. Each must be checked by the architect against BUILDER_RULES §6.6 steps 1-5 before any embedding. The
  planner names no source as cleared.
- No `data-files` attribute on any lab until a dataset is embedded. Rung 4 may list `fx_daily.csv` (§5.1) only if the builder
  confirms the file name in MANIFEST (`tools/check_pages.py` `check_data_files`).

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (every key below exists in `references/references.json`; checked by grep and by the planner's script)

| Key | Record (as read, planner) | Status | Use in E8 |
|---|---|---|---|
| `fama1984forward` | Fama, "Forward and spot exchange rates", JME, volume 14, issue 3, year 1984 (`references/references.json:8376`); source string "Fama (1984), JME 14(3)" (`yaml:294`) | verified, `used_by: ["E8"]` | L03 forward-premium puzzle (paper level until the abstract is read); reading list |
| `dornbusch1976expectations` | Dornbusch, "Expectations and Exchange Rate Dynamics", JPE, volume 84, issue 6, year 1976 (`references/references.json:7094`); matches `yaml:295` | verified, `used_by: ["E8"]` | L06 overshooting (paper level) |
| `du2018deviations` | Du, Tepper & Verdelhan, "Deviations from Covered Interest Rate Parity", JF, volume 73, issue 3, year 2018 (`references/references.json:7218`); matches `yaml:296` | verified, `used_by: ["E8"]` | L02 and L04 (CIP deviations); debate; reading list |
| `gopinath2020dominant` | Gopinath et al., "Dominant Currency Paradigm", AER, volume 110, issue 3, year 2020 (`references/references.json:10648`); matches `yaml:297` | verified, `used_by: ["E8"]` | L07 dominant-currency paradigm (paper level) |
| `mirandaagrippino2020us` | Miranda-Agrippino & Rey, "U.S. Monetary Policy and the Global Financial Cycle", REStud, volume 87, issue 6, year 2020 (`references/references.json:17450`); matches `yaml:299` | verified, `used_by: ["E8"]` | L07 global financial cycle; reading list |
| `krishnamurthy2012aggregate` | Krishnamurthy & Vissing-Jorgensen, "The Aggregate Demand for Treasury Debt", JPE, volume 120, issue 2, year 2012 (`references/references.json:15046`); matches `yaml:300` | verified, `used_by: ["E8"]` | L08 safe assets; debate (mispricing side); reading list |
| `jiang2021foreign` | Jiang, Krishnamurthy & Lustig, "Foreign Safe Asset Demand and the Dollar Exchange Rate", JF, volume 76, issue 3, year 2021 (`references/references.json:13592`); matches `yaml:301` | verified, `used_by: ["E8"]` | L08 and L07; debate |
| `obstfeld1996foundations` | Obstfeld & Rogoff, "Foundations of International Macroeconomics", book, year 1996, Open Library-verified (`references/references.json:18351`); matches `yaml:302` | verified, `used_by: ["E8"]` | L05 trilemma at book level, no locator |

**Candidates registered but not curriculum-listed for E8 (usable only after the builder reads each abstract; each may
already be used by another module; citing them adds E8 to its `used_by` through the tools, not by hand):**
`lustig2011common` (`references/references.json:16316`, X2; carry risk factors in currency markets), `brunnermeier2008carry`
(`:4062`, X2), `menkhoff2012carry` (`:16813`, X2), `menkhoff2012currency`
(`:16861`, X2), `verdelhan2017share` (`:22185`, X2), `koijen2018carry` (`:14798`, F3), `burnside2010peso` (`:4279`, X2; B5),
`he2022treasury` (`:12278`, FI4; treasury inconvenience yields), `meese1983empirical` (`:16733`, X1; exchange-rate
predictability), `bis2025triennial` (`:2775`, X1; primary, 2025, FX market survey), `bis2024market` (`:2735`, GM5; primary, 2024,
carry-trade unwind). Freshness: `bis2025triennial` and `bis2024market` are the only registry entries from 2024-2025 in this
area that the planner found. Neither is read.

Not to be used by E8 without a new reason: `reinhart2009this` (E9, LX1), `obstfeld1996models` (E9), `blanchard2019public` (E9),
`blanchard2020macroeconomics` (E5; B4 of the E5 plan).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Rey (lead only)", year: "2013 (lead only)", title: "Jackson Hole Economic Policy Symposium paper (lead only; record not typed)", venue: "Jackson Hole Economic Policy Symposium (lead only)", needed_for: "L07 global financial cycle, the curriculum's source at yaml:298; the page cites mirandaagrippino2020us instead until it is admitted", confidence: "the curriculum string exists (yaml:298); the review queue holds it with no candidate (references/review_queue.json:269; SEED_REPORT.md:34)"}
- {doi: null, authors: "Mundell and Fleming (lead only; named in the curriculum concept name, yaml:287)", year: "not typed", title: "Mundell–Fleming model (lead only; record not typed)", venue: "not typed", needed_for: "L05 attribution, only if the architect permits one; default: the model is named and not attributed", confidence: "the names are in the curriculum concept name only; no registry record was identified"}
- {doi: null, authors: "Literature on UIP and currency risk premia, 2025-2026 (lead only; no author typed)", year: "2025-2026 (lead only)", title: "post-2024 work on the forward-premium puzzle and currency risk premia", venue: "not typed", needed_for: "L03 debate freshness (BLUEPRINT §3, Freshness; VERIFIER §2.1)", confidence: "the need is certain; the planner identified no record"}
- {doi: null, authors: "Literature on dollar funding and the cross-currency basis, counter-evidence (lead only)", year: "not typed", title: "empirical studies of the cross-currency basis and its drivers (lead only)", venue: "not typed", needed_for: "L04 two-sided treatment of a grade-B or C claim about quarter-end basis moves (BUILDER_RULES §2.5)", confidence: "the need is certain; the planner identified no record beyond the registry keys in §7.1"}
- {doi: null, authors: "Literature on fiscal and convenience-yield evidence, counter-evidence (lead only)", year: "not typed", title: "empirical estimates of safe-asset convenience yields (lead only)", venue: "not typed", needed_for: "L08 counter-evidence for each convenience-yield claim (BUILDER_RULES §2.5)", confidence: "the need is certain; `he2022treasury` is the only registry candidate found"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page;
`references/authorities.yaml`). Until resolved, the lessons teach the models with derivations and no empirical attribution,
and each empirical sentence is graded C at most with its basis named, or is removed.

### 7.3 DATA_REQUESTS (for the architect; the planner names no source or licence from memory)

- A forward exchange-rate series for the six currencies of `fx_daily` at one stated tenor (for the lab's real-data check and
  the project's example): source URL, licence sentence quoted from the issuer's page, licence page, and transform
  (BUILDER_RULES §6.6 steps 1-5).
- A foreign money-market rate for each of those currencies and a dollar money-market rate on the same tenor and day count:
  the same five steps.
- Candidate issuers, to be checked (BLUEPRINT §5.3): BIS statistics where the terms permit; FRED series under their owners'
  terms. The architect checks each before embedding.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for E8 (§0.1). No `atlas/E8.contract.md` is drafted. No `atlas/` file is read by
the E8 tools (`tools/check_projects.py` checks a contract only when the project names an `atlas` key).

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/E/E8/cards.json`, ids `E8-c001` upward, `lesson` in L01-L08, one card per definition, theorem statement, key
  formula, key result and misconception (BUILDER_RULES §7). `tools/check_pages.py:366-398` (`check_cards`) checks the id prefix,
  the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab 2, Derivation 1 (exact)"`.
- A card for a SIMULATED result names the SIMULATED lab in `basis` (L03, L04, L07, L08).
- Cite a registry key only for an empirical or attributed claim. `cite` is `[]` where the card is a model result.
- A card for the debate uses only keys whose records the lesson has read (VERIFIER §2.1).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit E8            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit E8
.venv/bin/python tools/check_projects.py --unit E8
.venv/bin/python tools/run_labs.py --unit E8               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/E/E8/L01.html                       # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/E/E8/L03.html --refresh lab-E8-L03-1 # after editing a twin
.venv/bin/ruff check tests/labs/E8 && .venv/bin/ruff format --check tests/labs/E8
.venv/bin/mypy tests/labs/E8                               # strict, repository configuration
```

Builder E (project), targeted:

```bash
.venv/bin/python tools/run_graders.py --unit E8 --seeds 0-49   # reference 50/50, starter fails, instances differ
.venv/bin/python tools/mutate_graders.py --unit E8 --seeds 0-9 # ten mutants, each killed or moved to equivalent/
.venv/bin/ruff check course/modules/E/E8/grader && .venv/bin/mypy course/modules/E/E8/grader
```

Verifier only, on a quiet machine: `.venv/bin/python tools/page_smoke.py --unit E8` (not run by builders; timing-sensitive),
`.venv/bin/python tools/verify_refs.py --unit E8` (the unit ledger's run, VERIFIER §2.1). `tools/fetch_data.py --check` only
if B1 adds a dataset (and never `--fetch`, B6).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`,
`build_site.py --check`, `render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`,
`verify_refs.py --offline`, and the full gate in CLAUDE.md.

Flag checks: `tools/check_pages.py`, `tools/check_dag.py`, `tools/check_projects.py` accept `--unit`; `tools/run_labs.py`
accepts `--unit` and `--page`; `tools/run_graders.py` and `tools/mutate_graders.py` accept `--unit` and `--seeds`;
`tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`. The planner did not execute the builder commands; only the
coursekit closure, concept-owner, topological-order and credential functions were run (§0.1, §4).

---

## 11. Tooling assumptions that do not hold for this unit, and tooling facts that do (flagged)

1. **Debate required.** E8 has `debate:` (`yaml:311`). `tools/check_pages.py:412-413` requires a `section.debate` on some lesson.
   The plan places it in L03 (§3).
2. **Autograder plus rubric.** `grading: both`. `tools/check_projects.py:122-137` requires the grader panel and the listed
   grader files (`reference.py`, `instance.py`, the suite, the starter). `tools/check_projects.py:138-139` requires the rubric
   and two exemplars at two levels (`rubric_problems`, `:58-73`).
3. **No Atlas milestone.** No `atlas:` key on the E8 project (`yaml:304-310`); no Atlas entry names E8.
4. **Mutants.** `tools/mutate_graders.py` reads `ledgers/E8/mutants/*.py` and requires at least three. The plan writes ten
   (§5.4). Equivalent mutants go to `ledgers/E8/equivalent/` with a README (ruling 9).
5. **Alternatives.** `ledgers/E8/alternatives/` holds five stdlib alternatives (§5.4; ruling 10).
6. **Rung 2 must be graded instantly.** `tools/check_projects.py:89-90` accepts a completion lab or a quiz. The plan uses a
   completion lab (`lab-E8-project-2`).
7. **One curriculum lab, eight required.** The curriculum names one lab (`yaml:303`); BUILDER_RULES §3.4 requires a
   numerical check per key formula. The plan adds one lab per lesson (E5 precedent).
8. **Prerequisite pages.** E5 and E1 are built, so E5 page links are allowed when anchors exist. S2 is not built, so S2
   concepts link only to `concepts.html` (`tools/check_dag.py` checks concept existence, not the page).
9. **check_dag sees linked uses only.** Unlinked uses of D1-D13 (§4) pass the tool; the verifier reads for them.
10. **Lesson hours and hub split** are satisfied by §1 (`tools/check_pages.py:225-228`, `:335-342`).
11. **The Fed snapshots are pinned, not refetched.** Builders never refetch (B6).
12. **Grader `data-solution` and deploy.** The panel names `reference.py` (S7 pattern). The repository has no deploy step
    (ruling 4); the exclusion of `reference.py` from deploy is recorded for the owner, not a defect of this slice.
13. **Browser validator for the CSV schema does not exist** (E5 open item; `course/assets/js` has no validator). The page
    says so (§5.2; §12 Q7).
14. **Registry year discrepancy (B5)** for `burnside2010peso` (record 2010 versus curriculum 2011, used by X2). Not E8's to fix.

---

## 12. Open questions for the architect (numbered; each needs a decision before the builders start)

1. **B1, data for the curriculum lab and the project (BLOCKING).** Confirm the default: a SIMULATED Fama panel for L03 with
   the honest-pending note; bring-your-own-data for the forward rate, the foreign money-market rate and the dollar
   money-market rate; the embedded `fx_daily` spot series only in the rung-4 stretch. Alternative: a redistributable forward
   and rate source is read, quoted and added to `tools/data_sources.yaml` first. **Recommended: the default.**
2. **B2, project wording "public rates and FX data" (`yaml:306-308`).** Confirm that the page reads "public" as "supplied or
   embedded", and states that no public forward or foreign-rate series is embedded. Builders do not edit `curriculum/*.yaml`.
   **Recommended: confirm the reading; ask the curriculum owner to reword the brief at a later date (not a build blocker).**
3. **B3, Rey (2013).** Confirm that E8 cites `mirandaagrippino2020us` for the global financial cycle and that Rey (2013) is a
   REFERENCE_REQUEST (§7.2). **Recommended: confirm.**
4. **D1, D10, D11 (cycle prohibitions).** Confirm that E8 uses no concept owned by X1, X2 or E9 (each has E8 in its closure,
   §0.1), and uses plain prose for the substance (§4). **Recommended: confirm; these are not optional, because the alternative
   is a cycle.**
5. **D5, Dornbusch in discrete time.** Confirm that L06 derives a discrete-time version and cites the continuous result at paper
   level (B) or says it is not derived, because no ODE concept exists in the curriculum (§4). Alternative: a curriculum
   change adding an ODE concept to a closure module (not recommended for this unit). **Recommended: discrete time.**
6. **D4, D7, D8, D13, D14, D15 (outside-closure concepts used in plain prose).** Confirm the defaults in §4: no prerequisite
   change. Alternatives within the rules: add FC2 (D4), FI4 (D7), E7 (D8) or E6 (D13) to E8's prerequisites. None of them
   creates a cycle (planner check: E8 is not in their closures), but each is a curriculum change and each adds a prerequisite
   burden. **Recommended: no change.**
7. **Scope and browser validator.** Confirm the scope in §2.1 item 4 (six currencies in `fx_daily` and any student currency;
   closed-form and discrete-time models; no New Keynesian model; no forecasting claim beyond the evidence). Confirm whether the
   CSV validator is built by the architect (E5 precedent: none exists) or the page states that checks are by hand. **Recommended:
   confirm the scope; the page states that the validation runs in the grader suite on the student's file in Pyodide.**
8. **Project conventions (the autograder's exact rules).** Approve the conventions in §5.2: day count per leg (default
   proposal actual/360 on both legs), the sign of the basis, basis points as the unit, the quarter-end rule (last weekday, no
   holiday calendar), and no rounding inside functions. The planner does not assert any of these is the market convention.
   **Recommended: approve as proposed, with the day count left to the architect's final choice.**
9. **Debate placement and sides.** Confirm the debate brief in L03 (§3), and that the candidate keys in §3 are read by the
   L03 builder before any side is graded. **Recommended: confirm.**
10. **Lesson count and hours.** Confirm 8 × 10 h lessons and a 40 h project (33.3%). Alternatives within the rules: 9 × 8 h and a
    48 h project (40%, the maximum); 8 × 10 h and a 40 h project as proposed; 10 × 8 h and a 40 h project. **Recommended: 8 × 10 h
    and 40 h.**
11. **Builder ownership.** The brief asks for about three lessons per builder across A to E. Confirm the recommended 2-2-2-2
    split for A to D with E on the project (§1), or the 3-3-2 alternative with one lesson builder idle. **Recommended: 2-2-2-2.**
12. **Notation and questions on scope.** Confirm the local symbols and the `\tau` collision with E5 (§2.3). Confirm that the
    project does not use an adversarial question bank (§5.7). **Recommended: confirm both.**
13. **Money.** Confirm that the project has no money output (basis in bp, rates in percent). If the architect wants a notional
    P&L, it is an integer number of cents (fixer rules). **Recommended: no money output.**
14. **Figures.** No live figure is planned (no chart kernel). Confirm, or request one figure with a kernel and test (BUILDER_RULES
    §6.4), for example the basis on quarter-end versus other dates. **Recommended: none in this build.**
15. **Glossary.** Plain dfn terms (risk premium, forward exchange rate, spot rate, current account, financial account, trade balance,
    day-count, quarter-end, dollar funding, safe-asset price wedge) carry no `data-concept`. Confirm that no GLOSSARY_REQUESTS
    entry is needed. **Recommended: confirm.**
16. **B5 and B6.** Confirm that E8 does not cite `burnside2010peso` with a year (use the record only), and that builders never
    run `fetch_data.py --fetch` because of the Board's announced download change (B6). **Recommended: confirm both.**

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02, L03-L04 (includes the curriculum lab and the debate),
   L05-L06, L07-L08, project (autograder: the reference, the alternatives, the ten mutants; rubric: blind scoring of the
   exemplars by a dedicated scorer, FINAL-ARCHITECT-RULINGS 23). Failing rows return to the builder that owns the file, with
   only the failing rows.
3. Ledger at `ledgers/E8.verification.json`; verifier scripts archived under `ledgers/E8/scripts/` (VERIFIER §3); mutants under
   `ledgers/E8/mutants/` (ten), equivalents under `ledgers/E8/equivalent/` with README, alternatives under
   `ledgers/E8/alternatives/` (five).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B3 must be
   resolved or named as honest gaps first. B4 is a rule already satisfied by §4.
5. Closing: a delta verification (FINAL-ARCHITECT-RULINGS 30) from the last full fragment, not a fresh full re-verification.

---

**Architect decisions: pending (§12).** This plan is the planner's proposal. Where the plan states a recommendation for an open
question, the recommended decision applies unless the architect replaces it.

**Could not establish (planner):**
- Content of any E8 source beyond its registry record: no abstract or paper was read. Every empirical grade is left to the builder.
- Whether the Fama (1984) sample or the Dornbusch model matches any claim the curriculum makes beyond the source string.
- Any forward-rate, foreign money-market-rate or quarter-end basis data source, its licence, or its terms. None was checked.
- The market day-count convention for the USD and foreign legs; §12 Q8 leaves it to the architect.
- Whether the E5 lesson anchors exist for every E5 concept E8 links (the builder greps the built E5 pages).
- Whether the Board's Build-Your-Package change (B6) has taken effect; the planner did not fetch the Federal Reserve page.
