# E5 build plan: Macroeconomics I: Aggregates, Cycles & Policy (2026-10-28)

Unit: **E5 · Macroeconomics I: Aggregates, Cycles & Policy** · tier U · 110 h · prerequisite E1 · no Atlas milestone ·
no debate key · grading `rubric` (no autograder) · output directory `course/modules/E/E5/` (part code `E`) ·
lab twins `tests/labs/E5/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Anything not in the
curriculum is marked **NOT IN CURRICULUM**. Planner-derived statements about the tooling were checked by reading the tool
source or by running `tools/coursekit.py` (`prerequisite_closure`, `concept_owner`, `unit`) through the repo venv.

**Status: BLOCKING ISSUES EXIST (§0.3). The hours are feasible; the data for the curriculum lab and the project is not.
The architect must decide B1-B3 before the builders start.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part E, code `E`, title "Economics"; the module list of part E is E1 through E9 | `curriculum/02-economics-finance-core.yaml` (part header, E1 at its top); `curriculum.json` parts, `PART E` |
| E5 id, title "Macroeconomics I: Aggregates, Cycles & Policy" | `curriculum/02-economics-finance-core.yaml:155-156` |
| Tier `U`, hours `110` | `curriculum/02-economics-finance-core.yaml:157-158` |
| Prereqs `[E1]` (only) | `curriculum/02-economics-finance-core.yaml:159` |
| Core: "National accounts, growth accounting, the Solow model, IS-LM and AD-AS, the Phillips curve and the natural rate, central banking and fiscal policy basics." | `curriculum/02-economics-finance-core.yaml:160-162` |
| `introduces` has 13 concepts (mapped to lessons in §3) | `curriculum/02-economics-finance-core.yaml:163-176` |
| Sources: five free-text strings (Solow 1956; Hicks 1937; Friedman 1968; Phelps 1968; Blanchard 8th ed. 2021) | `curriculum/02-economics-finance-core.yaml:177-182` |
| Lab: "Growth accounting on embedded national-accounts data." | `curriculum/02-economics-finance-core.yaml:183` |
| Project "Macro dashboard v0"; brief: "Assemble GDP, inflation, unemployment, policy-rate and term-spread series from Atlas into a documented dashboard, with a one-page cycle diagnosis."; deliverable "Dashboard plus diagnosis."; grading `rubric` | `curriculum/02-economics-finance-core.yaml:184-190` (brief 186-188, deliverable 189, grading 190) |
| No `debate:` key on E5 | `curriculum/02-economics-finance-core.yaml:155-190` (absent) |
| No `atlas:` key on the E5 project; no Atlas entry names E5 (the 20 entries name CS1, CS3, S0, S4, FI1, DV4, F1, S7, QR2, MS3, PR2, PR4, FI3, CR1, AC2, CF4, QR3, GM1, SR3, GM4) | `curriculum/curriculum.json` `atlas` array (A1-A20, module fields); no E5 entry |
| JSON row for E5 matches the YAML (hours 110, prereqs E1, 13 concepts, lab, grading rubric) | `curriculum/curriculum.json:7495` (`"id": "E5"`) |
| E5 concepts all map to module E5 in `concepts` (planner check: 13 owners = E5) | `curriculum/curriculum.json` `concepts` (computed by `tools/coursekit.py` `concept_owner`) |
| E5 is referenced by the bachelor's credential (`requires`), the Macroeconomics course map, and the first-year sequence group | `curriculum/meta.yaml:63`, `:71`, `:133` |
| E6 (M-tier) requires E5 | `curriculum/02-economics-finance-core.yaml` E6 `prereqs: [E5, M7, S3]` |
| Prerequisite closure of E5 (computed with `tools/coursekit.py` `prerequisite_closure("E5")`, run by the planner): **{E1, M1, M2, P0.1}** | run output, planner |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 110 h (`curriculum/02-economics-finance-core.yaml:158`). The tool rules:

- lesson `data-hours` 6-12 (`tools/check_pages.py` `check_lesson`, line 227);
- hub `data-hours-lessons + data-hours-project = 110` (`check_pages.py` `check_hub`, line 337);
- project share 10-40% of 110, i.e. 11 to 44 h (`check_pages.py` line 339);
- lessons sum to the hub's lessons figure (`check_pages.py` `check_hub`, the lesson-hours comparison).

Chosen split: **8 lessons × 10 h = 80 h; project 30 h (27.3%)**. 80 + 30 = 110. Feasible. **No STOP condition on hours.**

### 0.3 Blocking issues (architect decision required before builders start)

**B1. The curriculum lab and the project need national-accounts and macro series that no embedded source provides.**
- The lab says "on embedded national-accounts data" (`yaml:183`). The project needs GDP, inflation, unemployment and
  policy-rate series (`yaml:186-188`).
- The only embedded snapshots are `fx_daily`, `fx_monthly` and `ust_daily`, all Federal Reserve H.10 and H.15 releases
  (`tools/data_sources.yaml:18-116`; `course/assets/data/market/MANIFEST.json` has exactly those three datasets).
- H.15's embedded series are `tbill_3m` and `cmt_10y` only (`tools/data_sources.yaml`, `ust_daily.transform.series`).
  No policy-rate series (federal funds) is in the transform.
- No national-accounts, price-index, unemployment or policy-rate source is listed in `tools/data_sources.yaml` or in
  `rejected:` (`data_sources.yaml:119-`). BLUEPRINT §5.3 lists only candidates, none of them national accounts.
- BUILDER_RULES §6.6 forbids embedding a series until its issuer's redistribution grant is quoted from the issuer's page
  (`BUILDER_RULES.md` §6.6, "Adding a dataset", steps 1-2). The planner did not read any national-accounts issuer page
  and does not name one from memory.
- **Plan's default (for the architect to confirm or replace):** (a) the L02 curriculum lab runs on a generated
  Cobb-Douglas economy labelled **SIMULATED** (BUILDER_RULES §1.7), with an honest-pending note on the lesson and a
  `DATA_REQUESTS` entry for a national-accounts series with a quoted licence; (b) the project takes its GDP, price index,
  unemployment and policy-rate series in bring-your-own-data mode (BUILDER_RULES §6.6, last bullet: the page documents and
  validates a CSV that never leaves the browser), and uses the embedded `ust_daily` yields for the yield series only.
  The architect must decide whether a verified redistributable source is to be added to `tools/data_sources.yaml` first.

**B2. The project brief says "from Atlas", and no Atlas milestone supplies these series.**
- `yaml:187-188` names Atlas. No Atlas entry names E5 (§0.1). The Atlas data layer is A2, built in CS3 (`curriculum.json`
  `atlas` array, A2 entry), and CS3 is outside the E5 prerequisite closure {E1, M1, M2, P0.1}.
- `check_projects.py` only checks `atlas/<id>.contract.md` when the project names an `atlas` key (`check_projects.py`
  line 144-146). Nothing enforces the brief's Atlas wording, so the verifier must reject any page that relies on Atlas.
- **Plan's default:** the project does not use Atlas. Its data come from B1's bring-your-own-data mode and the embedded
  `ust_daily`. The architect either accepts this reading or amends `yaml:187-188` (a curriculum change; the builders do not
  edit `curriculum/*.yaml`).

**B3. Friedman (1968) is in the curriculum's source list but not in the registry, and the review queue's candidate is the
wrong paper.**
- Curriculum source: `yaml:180`, "Friedman (1968), 'The Role of Monetary Policy', AER 58(1)".
- Not in `references/references.json` (no `friedman1968*` key; the only Friedman book is `friedman1963monetary`, used by
  LX1). Review queue entry: `references/review_queue.json:163`, "no candidate established identity".
- The review queue's candidate DOI `10.2307/2296661` is recorded there as "Reaction Functions and the Theory of Duopoly",
  Review of Economic Studies, 35(3). That is not the requested article. **It must not be admitted.**
- Consequence: no E5 page may cite Friedman 1968 (BUILDER_RULES §2.4). It goes to `REFERENCE_REQUESTS` (§7).

Non-blocking, but the architect should see them:

- **B4. Blanchard edition year.** The curriculum says "Blanchard, Macroeconomics, 8th ed. (2021)" (`yaml:182`). The
  registry record `blanchard2020macroeconomics` (`references/references.json:3085`) has year 2020 and a
  `notes.year` entry that already flags "curriculum 2021 vs record 2020". Cite the key only, with no edition or year typed
  in the prose (§5, §8). The architect decides whether to correct the curriculum string.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

8 lessons × 10 h = 80 h; project 30 h; total 110 h. Concept counts per row sum to 2+2+1+2+1+2+2+1 = 13, each concept in
exactly one row (`yaml:163-176`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:164-176`) | Lab (twin id, `tests/labs/E5/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | National accounts, price indices and measured inflation | `national-accounts`, `price-index-inflation` | `lab-E5-L01-1`: the expenditure and income identity on a SIMULATED accounts table; two price indices (Laspeyres and Paasche) on an illustrative two-good basket, in `Fraction`, the gap printed | 10 | Builder A |
| L02 | Growth accounting and the Solow residual | `growth-accounting`, `total-factor-productivity` | `lab-E5-L02-1` (**the curriculum lab**, `yaml:183`, SIMULATED per B1): growth accounting on a seeded Cobb-Douglas economy; the decomposition of output growth into input and residual terms holds exactly | 10 | Builder A |
| L03 | The Solow growth model | `solow-model` | `lab-E5-L03-1`: the capital recursion iterated against the closed-form steady state; comparative statics of the steady state by the implicit-function derivative against a finite difference | 10 | Builder B |
| L04 | Business cycles and IS–LM | `business-cycle`, `is-lm-model` | `lab-E5-L04-1`: the IS and LM lines solved exactly in `Fraction`; the fiscal and monetary multipliers against the solved shifts | 10 | Builder B |
| L05 | Aggregate demand and aggregate supply | `ad-as-model` | `lab-E5-L05-1`: the AD-AS equilibrium for a linear specification; a demand shift traced to the new price and output | 10 | Builder C |
| L06 | The Phillips curve and the natural rate | `phillips-curve`, `natural-rate-of-unemployment` | `lab-E5-L06-1`: the expectations-augmented Phillips curve on a seeded SIMULATED path; the natural rate as the unemployment rate at which inflation does not change | 10 | Builder C |
| L07 | Central-bank policy and the Taylor rule | `policy-rate`, `taylor-rule` | `lab-E5-L07-1`: the Taylor rule as a function of inflation and output gap, evaluated exactly; the policy-rate response to a 1-point inflation gap | 10 | Builder D |
| L08 | Fiscal policy and the multiplier | `fiscal-multiplier` | `lab-E5-L08-1`: the closed-economy multiplier in the simple Keynesian cross, checked against a finite sum of rounds of spending | 10 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 80/30 | none | none | - | Builder A |
| project | Macro dashboard v0 (`rubric`, §5) | none | `lab-E5-project-1` (rung 1), `lab-E5-project-2` (rung 2, `class="lab completion"`), `lab-E5-project-3` (rung 3 check) | 30 | Builder E |
| cards | `cards.json` from L01-L08 | none | none | - | Builder F (after A-E) |

Ownership rule: each builder writes only its lesson files and twins. Builder A writes the hub after L01-L02 exist. Builder E
writes the project and its rubric and exemplars, and does not depend on the lessons' text.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §7):
- L01 uses only E1 and M1/M2 concepts (`derivative` for growth rates in the lab, `exponential-and-logarithm`).
- L02 uses L01 (`national-accounts`, `price-index-inflation`) and M1 `exponential-and-logarithm` (log growth rates).
- L03 uses L02 (`growth-accounting`, `total-factor-productivity`) and M2 `implicit-function-theorem`, `derivative`.
- L04 uses E1 `comparative-statics` and `competitive-equilibrium` (for market-clearing language) and L03 for the capital
  stock only in prose.
- L05 uses L04 (`is-lm-model`) for the aggregate-demand curve.
- L06 uses L05 (`ad-as-model`) for the output side of the curve and E1 `price-elasticity` only in prose.
- L07 uses L06 (`phillips-curve`) for the inflation gap, and L04 for the output gap.
- L08 uses L04 (`is-lm-model`) and L07 (`policy-rate`) for the monetary offset.

Hours check: 8 × 10 = 80 (hub `data-hours-lessons="80"`); project 30 (hub `data-hours-project="30"`); 110 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to E5)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E1-build-plan.md` (its Architect
decisions section is binding precedent), `plans/M1-build-plan.md` and `plans/CF1-build-plan.md` (their Architect decisions
sections), this file. Study `course/modules/M/M1/` for layout and the hub and project grammar. `course/templates/` holds
the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and
   rounded only at display. A page that shows a rounded figure states its rounding rule. Precedent: AC4 KNOWN LIMITATION 3
   and CF1 L01 Remark 5.2. For E5 this covers every growth rate, every index and every multiplier.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS ("checked directly" with no lab behind it).
3. **Attribute nothing unread.** Only the registry keys in §8 may be cited, and only at book or paper level unless the builder
   has read the abstract (for locators, the locator must be read; VERIFIER §2.1). No page, table, equation, coefficient or
   date is typed from memory. Precedent: AC2, AC4 §0 ("never type a page or table from memory"). Where a textbook result is
   needed, it is a derivation on the page (grade T) or is cited at book level with no locator.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "market structures", "central banking",
   "fiscal policy basics", "welfare", "the natural rate" are used only where a derivation, a finite check or a lab computes
   the claim. E5 scope (confirm, §10 Q7): closed economy; the IS-LM and AD-AS models are static; the Solow model is
   the one-sector model with Cobb-Douglas technology; central banking is the policy rate and the Taylor rule; fiscal policy
   is the Keynesian-cross multiplier. No New Keynesian model, no determinacy, no open economy (those are E6, E8).
5. **Define before use.** Each of the 13 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Terms outside the 13 (the unemployment rate, the labour force, real and nominal GDP, the
   output gap, expected inflation, the multiplier as a ratio) are defined in prose at first use with a plain `<dfn>` and no
   `data-concept` (`tools/check_dag.py` line 47 skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions
   (A1, A2, ...) before the statement. Examples the builders must state: the Solow steady-state result needs
   0 < α < 1, s in (0, 1), n + δ > 0 and a positive capital stock; the IS-LM solution needs the slopes to make the
   system non-singular; the Keynesian-cross multiplier needs a constant marginal propensity to consume in (0, 1).
7. **Grader rule.** Not applicable (rubric-only; §5). Keep the rule in mind if an autograder is ever added.
8. **Money.** E5 has no money output. Index and rate outputs are exact rationals rounded only at display, with the rule stated.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; no element forces the page wider than 360 px. `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network
    (`tools/run_labs.py` lines 51-60). The M1 twin `tests/labs/M1/lab-M1-L04-1.py` is the model.
11. **Policy-rate and yield statements are basis-explicit.** Any yield or rate is stated with its unit (percent per year,
    or a decimal), its compounding or discount basis, and its source (`tools/data_sources.yaml` `note`, `ust_daily`).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded
  claim names its published counter-evidence (BUILDER_RULES §2.5). **The registry holds no fiscal-multiplier, Phillips-curve
  slope or Taylor-rule estimate record that this plan has checked for E5.** Those claims are either derivations (grade T,
  conditional on the stated model) or go to `REFERENCE_REQUESTS` with the counter-evidence lead (§7).
- Concepts: §1 table; `<dfn>` only for the 13 registered concepts plus plain `<dfn>` for other terms. No `<a class="concept">`
  for any concept outside the prerequisite closure {E1, M1, M2, P0.1} (§3, DAG).
- Prerequisite links: `href="../../../concepts.html#<id>"` for E1, M1, M2 and P0.1 concepts; `href="Lnn.html#def-<id>"` for
  earlier E5 lessons. A lesson never links a concept defined in a later lesson. There is no link to an E1 hub page, because
  E1 is not built (`course/modules/E/` does not exist; §6).
- Labs: code lives once in `tests/labs/E5/lab-E5-Lnn-1.py` (and `lab-E5-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match
  `lab-E5-<page>-<n>` (`check_pages.py` `check_lesson`). Standard library only (`fractions`, `math`, `random.Random(seed)`);
  seeded RNG only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab or figure that uses generated data (L02, L06, the project's worked example). Exact closed-form
  checks (L03, L04, L05, L07, L08) are not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments (precedent: M1 "Convention (project Q5)"; AC4 KNOWN 9).
- Banned strings (`tools/check_pages.py` lines 58-72 `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction (precedent: CF1 L07 Misconception 2). Growth rates state the
  convention (log or simple, annual or per period).
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that E5 must not give a different meaning (`notation/notation.json`, `symbols` array and `macros` object):

| Registered symbol | Registered meaning (locator) | E5 conflict and rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation.json:112`, module S1) | **Conflict.** Tax revenue and time horizons must not use bare `T`. Tax revenue is written `\mathrm{Tax}_t`; the tax rate is `\tau` (no registered meaning). A time horizon is written `H`. |
| `R^\ast` | return on the SDF in payoff space (AP1) | **Conflict risk.** The natural rate of interest must not be `R^\ast`. Write the natural real rate as `r^{n}` (lowercase, superscript `n`, defined on L07). |
| `R_f` | gross riskless return (AP1) | Not used. Nominal policy rate is `i`; real rate is `r`. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF (M4) | Not used. |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (M4) | Not used. Plain `\gamma` is free but is not used either. |
| `\E` (macro) | expectation operator | Use the macro for expected inflation and expectations. Do not write `E` for expectation in plain text. |
| `\R` (macro) | real numbers | Standard. |

Local symbols (allowed; `notation.json` `about`: letters conventionally local are defined per lesson): `Y` output,
`C`, `I`, `G`, `NX`, `K` capital, `L` labour (defined on L01 as the labour input, not a lag), `N` population or labour
force (defined per lesson), `n` population growth, `s` saving rate, `\delta` depreciation, `\alpha` capital share, `g` growth
rate, `u` unemployment rate, `\pi` inflation, `i` nominal interest rate, `r` real interest rate, `\phi` Taylor coefficient.
Each is defined on the lesson where it first appears and never redefined. A symbol with a registered meaning above is not
reused with another meaning in any lesson or the project.

NOTATION_REQUESTS: none. The plan uses only local symbols and the registered `\E` and `\R` macros.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson:

- **L01** `national-accounts`: the expenditure identity `Y = C + I + G + NX` (defined; T, identity by definition) and the
  income identity; real versus nominal GDP. `price-index-inflation`: Laspeyres and Paasche indices and the chain
  construction, measured inflation as a log or simple growth rate of an index (convention stated). Lab checks the identity
  and the index gap exactly. No registry key is needed: the identities are derived on the page (grade T).
- **L02** `growth-accounting`, `total-factor-productivity`: the growth-accounting identity for a Cobb-Douglas production
  function `Y = A K^\alpha L^{1-\alpha}` (assumptions stated; capital share `\alpha` in (0,1)); the Solow residual
  `A` defined as the output growth not explained by input growth (T, derivation). The curriculum lab is here. The lab is
  SIMULATED (B1). No registry source is cited for the residual's attribution: the curriculum does not attribute the residual
  to Solow 1956, and the planner has not read that paper's text. Any empirical claim about the size of the residual is grade
  C at most, names its basis, and waits for the REFERENCE_REQUESTS in §7.2 (growth-accounting measurement).
- **L03** `solow-model`: the capital accumulation equation `k_{t+1} = s f(k_t) + (1-\delta) k_t`, its steady state (T, with
  assumptions), convergence (proof of monotone convergence for Cobb-Douglas with the stated assumptions, or a numerical check
  with its tolerance, labelled as such), and comparative statics of `k^\ast` by the implicit-function theorem
  (M2 `implicit-function-theorem`). Cite `solow1956contribution` at paper level; the "Solow" result on convergence is
  a derivation here (grade T on the page).
- **L04** `business-cycle`, `is-lm-model`: the business cycle as deviations of output from trend, described in words with no
  statistic (the measurement of cycles, i.e. filters and volatility, is outside the closure, §4 DAG D2); the IS and LM
  relations, solved exactly for a linear specification; `hicks1937mr` cited at paper level for the IS-LM construction (grade B
  or C, with the counter-evidence named, see §7 REFERENCE_REQUESTS on the IS-LM critique if needed).
- **L05** `ad-as-model`: the aggregate-demand curve from IS-LM, the aggregate-supply curve (short run and long run), and
  equilibrium; one demand shock traced exactly (T for the linear case).
- **L06** `phillips-curve`, `natural-rate-of-unemployment`: the Phillips curve in its expectations-augmented form
  (stated as a model, no empirical claim without counter-evidence), and the natural rate as the unemployment rate at
  which inflation does not change (T in the model). `phelps1968money` cited at paper level for the expectations-augmented
  construction. Expected inflation is written with the `\E` macro and defined in prose (no concept link, DAG D1).
- **L07** `policy-rate`, `taylor-rule`: the policy-rate reaction function `i_t = r^{n} + \pi_t + \phi_\pi(\pi_t - \bar\pi) +
  \phi_y y_t`, with `\bar\pi` the inflation target with the parameter restrictions stated (T for the rule as defined; no empirical value of \phi_\pi or \phi_y
  is typed). The rule as a description of practice is grade C at most. `taylor1993discretion` is registry-verified but
  **not curriculum-listed for E5** (its `used_by` is E7, `references/references.json:21685`); its use is open question Q4.
- **L08** `fiscal-multiplier`: the simple Keynesian cross multiplier `1/(1-c)` with `0 < c < 1` (T, derived from a finite
  sum of rounds of spending, lab checks it exactly). The evidence on fiscal multipliers is contested; a B- or C-graded claim
  must name counter-evidence, and none is in the registry for E5 (§7 REFERENCE_REQUESTS). The lesson's conclusions are
  limited to the model.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it (for example,
  fixed prices in IS-LM, a one-sector technology in Solow).
- No lesson uses a term from E6 (New Keynesian, HANK, determinacy) or E8 (open economy, exchange rates) as a concept. Those
  are outside E5 and not in its closure.

---

## 4. DAG problems (concepts that natural E5 content would use outside the closure)

Prerequisite closure of E5 (computed): **{E1, M1, M2, P0.1}**, with 51 usable concepts (the closure's `introduces`, computed
by `tools/coursekit.py`). Owners below are from `curriculum/curriculum.json` `concepts` (planner check).

| Ref | Concept | Owner (outside closure) | Where natural E5 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `expectation` | M4 (`curriculum.json` concepts) | expected inflation in the Phillips curve (L06) and the Taylor rule's forward-looking terms (L07) | Plain prose; the term "expected inflation" defined in L06 with a plain `<dfn>`; no link (default; E1 Q2 precedent). Architect may add M4 as a prerequisite instead (CF1 Q1 precedent). |
| D2 | `coefficient-of-determination`, `empirical-distribution`, `consistent-estimator` (S0, S1, S2) and cycle-measurement statistics (no concept) | S0/S1/S2 | measuring the business cycle (L04): standard deviations, correlations, filters | Not used. L04 describes cycles in words and computes nothing statistical. (AC4 Q3 precedent: no regression.) |
| D3 | difference-equation methods | no concept in the curriculum | the Solow recursion (L03) | Plain prose and an explicit recursion; the fixed point is found by solving the steady-state equation; no concept named. |
| D4 | `lagrange-multiplier`, `kkt-conditions` (M7) | M7 | constrained optimisation in the Solow model (none needed) | Not used. The steady state and the IS-LM solution use substitution and linear algebra. |
| D5 | `gordon-growth-model` (FC4) | FC4 | steady-state growth of a balanced path (L03) | Not used; the balanced-growth path is derived in prose from the recursion (T). |
| D6 | `dynamic-is-curve`, `equilibrium-determinacy` (E6); `rational-expectations-equilibrium` (E4) | E6, E4 | forward-looking IS and Phillips curves (L06, L07) | Not used. The expectations-augmented Phillips curve is stated as an adaptive or model-consistent equation without the term "rational expectations". |
| D7 | `dynamic-programming` (CS2) | CS2 | none | Not used. |
| D8 | `policy-rate` and `taylor-rule` (E5) | E5 | (in-module) | Not a DAG issue; listed for the verifier to check that L07 defines them before the project uses them. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (§10 Q2, Q3).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring); an unlinked use of D1-D7 passes the tool, so the
verifier reads every lesson for these names (VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): rubric-graded, ladder, spec, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order, line 33)

1. **Rung 1, worked example** (`lab-E5-project-1`, SIMULATED): one fully solved, annotated computation of the GDP growth rate,
   the inflation rate from a price index, and one cycle flag, on a generated five-year path. Each step has a "why" annotation.
   Full length (tier U; BLUEPRINT §4 minimum applies from tier M).
2. **Rung 2, completion** (`lab-E5-project-2`, `class="lab completion"`, SIMULATED): the term-spread line and the output-gap
   line are removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the twin line or
   contains a blank (`tools/run_labs.py` docstring). `check_projects.py` requires a completion lab or a quiz (its
   `section.completion` or `section.quiz` test).
3. **Rung 3, independent project** (graded by rubric): the dashboard and a one-page cycle diagnosis, built from the five
   series in §5.2. `lab-E5-project-3` is the rung-3 check: it recomputes the dashboard's default state from the same inputs and
   prints the table the dashboard should show.
4. **Rung 4, stretch** (optional, not graded): a second economy's dashboard with the same rules, or a vintage analysis of one
   series (a revised and an unrevised value), with the revision size stated as a hypothesis.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A macro analyst must give a one-page diagnosis of where the economy stands in its cycle. The dashboard must
  show five series and the rules that turn them into a diagnosis. The diagnosis must cite the values it uses.
- **Inputs.** Five series, each with a named source and a stated transform:
  1. real GDP (level, quarterly or annual; **bring-your-own-data**, B1);
  2. a price index (the level from which inflation is computed; **bring-your-own-data**, B1);
  3. the unemployment rate (**bring-your-own-data**, B1);
  4. the policy rate (**bring-your-own-data**, B1; the H.15 federal funds series is not embedded, §6);
  5. the term spread, computed from the embedded `ust_daily` snapshot as `cmt_10y − tbill_3m` (percent per year), with the
     basis caveat: `tbill_3m` is on a discount basis (`tools/data_sources.yaml`, `ust_daily.note`). The builder states the
     basis convention used, or the architect approves an alternative (§10 Q5).
  The CSV schema for series 1-4 is documented on the project page and validated in the browser; the file never leaves the
  browser (BUILDER_RULES §6.6). Labs and the worked example use generated paths labelled SIMULATED.
- **Required outputs.** A dashboard (format is the student's choice: a notebook, a spreadsheet, or a static page) that shows
  the five series with units, and a one-page diagnosis file `diagnosis.md`. The diagnosis states the cycle position using the
  rule in the spec: GDP growth and output-gap signs, inflation relative to a stated target, unemployment relative to the
  natural rate, the policy rate relative to the Taylor-rule value, and the term spread sign. Every number is recomputed from
  unrounded values, with the rounding rule stated.
- **Constraints.**
  - Every number in the diagnosis cites the series, the date and the transform that produced it.
  - No claim about a series beyond its source's coverage (for example, a revision in the data).
  - Standard library or any tool the student chooses; the rubric does not depend on the tool.
  - The inputs are the five series above; no series from Atlas is used (B2).
- **Grading.** Rubric (`rubric-self`, §5.4). The spec's grading entry names the rubric. Adversarial question bank: not required
  (§10 Q6).
- **Reading list.** `ol.reading-list` cites `solow1956contribution`, `hicks1937mr`, `phelps1968money` and
  `blanchard2020macroeconomics` (registry keys only; §8). Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 30 h; every row needs a one-line rationale; `check_projects.py` lines 58-73 and the hours check)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED path, annotated line by line |
| Rung 2, completion problem | 3 | Fill the term-spread line and the output-gap line, then run the instant check |
| Data intake: the CSV schema, validation, the basis convention | 6 | Document the four CSV schemas, validate a student file, state the spread convention |
| Series transforms and the dashboard build | 8 | Growth rates, inflation, the output-gap rule, Taylor-rule value, term spread |
| Diagnosis memo | 7 | One page, every number cited with its date and transform |
| Self-assessment against exemplars | 4 | Score the memo with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **30** | Equals `data-hours-project` on the hub |

### 5.4 Rubric (`table.rubric#rubric`, `check_projects.py` `rubric_problems`, lines 58-73)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down
to 1 (the tool counts `td` cells: `check_projects.py:58-73`). Every level descriptor is observable.

1. **Data and provenance.** Level 4: names each of the five series with its source, its date range and its transform.
   Level 1: "uses the data".
2. **Computation.** Level 4: states the rounding rule and computes growth and inflation from unrounded values. Level 1: "rounds
   the numbers".
3. **Cycle diagnosis.** Level 4: states each rule and applies it to the stated values, giving the sign of each signal. Level 1:
   "a sensible diagnosis".
4. **Policy reading.** Level 4: compares the policy rate with the Taylor-rule value at the stated coefficients and states the
   gap's sign. Level 1: "discusses policy".
5. **Limits and evidence.** Level 4: names the model limits used in the diagnosis (fixed prices, one-sector technology,
   revisions) and states the counter-evidence for each claim graded B or C. Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written diagnoses on a SIMULATED
path, annotated with the descriptors each passage meets or misses. Self-assessment form (`section.rubric-self`,
`data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in M1 and E1). The page shows where the student's
scores diverge from the exemplar scores. Calibration: the verifier scores both exemplars blind, within one level per
criterion (VERIFIER §2.6).

---

## 6. Real-data policy (B1 applies)

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily` (`tools/data_sources.yaml:18-116`;
  `MANIFEST.json`). `ust_daily` gives `tbill_3m` and `cmt_10y`. Use only for the term spread (§5.2 input 5).
- **Not embedded, and no grant found:** national accounts (GDP, price index), the unemployment rate, the federal funds rate.
  `tools/data_sources.yaml` `rejected:` (`:119-`) lists only the French library and Open Source Asset Pricing. No entry
  exists for these series. **Not embedded.** Lab L02 is SIMULATED; the project uses bring-your-own-data for the four series.
- **Honest-pending note** on L02 and on the project's data page: "The curriculum names embedded national-accounts data for
  this lab; no redistributable national-accounts source is embedded yet. The lab uses a generated economy labelled SIMULATED
  (BUILDER_RULES §1.7)." Cited to the DATA_REQUESTS entry (§7).
- **DATA_REQUESTS** (for the architect; the planner does not name a source or licence from memory): a national-accounts
  series (GDP and a price index), an unemployment rate, and a policy-rate series, each with its issuer URL, the quoted
  licence sentence, the licence page, and the transform (BUILDER_RULES §6.6, steps 1-5). The BLUEPRINT §5.3 candidates are
  FRED series under their owners' terms and Treasury yields; each must be checked before use.
- No `data-files` attribute on any lab until a dataset is embedded. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in E5 |
|---|---|---|---|
| `solow1956contribution` | Solow, "A Contribution to the Theory of Economic Growth", QJE, volume 70, issue 1, year 1956, DOI 10.2307/1884513 (`references/references.json:21041`) | verified, `used_by: ["E5"]`, source string matches `yaml:178` | L03 solow-model (paper level, no locator unless read); rubric reading list |
| `hicks1937mr` | Hicks, "Mr. Keynes and the 'Classics'; A Suggested Interpretation", Econometrica, volume 5, issue 2, year 1937, DOI 10.2307/1907242 (`references/references.json:12484`) | verified, `used_by: ["E5"]`, matches `yaml:179` | L04 is-lm-model (paper level); reading list |
| `phelps1968money` | Phelps, "Money-Wage Dynamics and Labor-Market Equilibrium", JPE, volume 76, issue "4, Part 2", pages 678-711, year 1968, DOI 10.1086/259438 (`references/references.json:19130`) | verified, `used_by: ["E5"]`, matches `yaml:181` | L06 phillips-curve and natural rate (paper level); reading list |
| `blanchard2020macroeconomics` | Open Library book "Macroeconomics", Blanchard, year 2020, ISBN 9780134897899, Pearson (`references/references.json:3085`) | verified, `used_by: ["E5"]`; `notes.year` flags curriculum 2021 vs record 2020 (B4) | textbook for conventions, at book level only; cite the key, do not state an edition or year in prose; reading list |

Not curriculum-listed but registry-verified: `taylor1993discretion` (`references/references.json:21685`, `used_by: ["E7"]`).
Use for L07 requires the architect's approval (Q4). Default: not used; L07 states the rule as a definition.

Not to be used by E5: `clarida1999science`, `gali2015monetary` (`used_by` E6), `bernanke2020new` and `romer2004new` (E7), `varian2014intermediate` (E1; no E5 content is microeconomic).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Friedman (lead only)", year: "1968 (lead only)", title: "The Role of Monetary Policy", venue: "American Economic Review, volume 58, issue 1 (lead only; record not typed)", needed_for: "L06 or L07 attribution of the expectations-augmented Phillips curve or of the monetary-policy rule, if the architect permits it", confidence: "the curriculum string exists (yaml:180); the registry has no record; the review queue candidate DOI 10.2307/2296661 is a different article (review_queue.json:163) and must not be admitted"}
- {doi: null, authors: "Growth-accounting literature (lead only; no author typed)", year: "not typed", title: "growth accounting and the Solow residual, original and later measurement papers (lead only; record not typed)", venue: "not typed", needed_for: "L02 attribution of the residual and any empirical claim about its size", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Literature on fiscal multipliers (lead only; no author typed)", year: "not typed", title: "empirical estimates of government-spending multipliers", venue: "not typed", needed_for: "L08 counter-evidence for every B- or C-graded multiplier claim (BUILDER_RULES §2.5)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Literature on the Phillips-curve slope (lead only; no author typed)", year: "not typed", title: "empirical estimates of inflation-unemployment trade-offs", venue: "not typed", needed_for: "L06 counter-evidence for a B- or C-graded claim about the curve's slope", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Literature on critiques of IS-LM (lead only)", year: "not typed", title: "critiques of the IS-LM synthesis", venue: "not typed", needed_for: "L04 two-sided treatment of a grade-B claim about IS-LM", confidence: "the need is certain; no record is identified by this planner"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4).
Until resolved, the lessons teach the models with derivations and no empirical attribution, and each empirical sentence is
graded C at most with its basis named, or is removed.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for E5 (§0.1). `atlas/A8.contract.md` and `atlas/A15.contract.md` exist; neither
is needed. No contract is drafted here. The brief's Atlas wording is B2.

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/E/E5/cards.json`, ids `E5-c001` upward, `lesson` in L01-L08, one card per definition, theorem statement, key
  formula, key result and misconception (BUILDER_RULES §7). `check_pages.py` `check_cards` checks the id prefix, the lesson
  existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab 3, Derivation 2 (exact)"`.
- Cite a registry key only for an empirical or attributed claim. `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit E5            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit E5
.venv/bin/python tools/check_projects.py --unit E5
.venv/bin/python tools/run_labs.py --unit E5               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/E/E5/L01.html                        # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/E/E5/L02.html --refresh lab-E5-L02-1 # after editing a twin
.venv/bin/ruff check tests/labs/E5 && .venv/bin/ruff format --check tests/labs/E5
.venv/bin/mypy tests/labs/E5                                # strict, repository configuration
```

Not run for E5:
- `tools/run_graders.py --unit E5` is not needed: it prints "no autograder" for a rubric unit (`tools/run_graders.py` line
  138-139 skips units whose grading is not `autograder` or `both`).
- `tools/mutate_graders.py` is not needed (no autograder; VERIFIER §2.6 applies to autograders only).

Verifier only, on a quiet machine: `.venv/bin/python tools/page_smoke.py --unit E5` (not run by builders; timing-sensitive),
`.venv/bin/python tools/verify_refs.py --unit E5` (the unit ledger's run, VERIFIER §2.1), and
`.venv/bin/python tools/fetch_data.py --check` only if B1 adds a dataset.

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`,
`build_site.py --check`, `render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`,
`verify_refs.py --offline`, and the full gate in CLAUDE.md.

Flag checks: `tools/check_pages.py` and `tools/check_dag.py` accept `--unit`; `tools/check_projects.py` accepts `--unit`
(`check_projects.py` `main`); `tools/run_labs.py` accepts `--unit` and `--page`; `tools/embed_labs.py` accepts pages and
`--refresh [LAB_ID ...]`. The planner did not execute the builder commands; only the coursekit closure and concept-owner
functions were run (§0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on the E5 project (`yaml:184-190`) and no Atlas entry names E5. `check_projects.py`
   skips the contract check (line 144-146). No `atlas/E5.contract.md` is needed. B2 applies to the brief's wording.
2. **No debate.** E5 has no `debate:` key, so `check_pages.py` does not require a debate brief (the check at `check_pages.py`
   `check_unit`, keyed on `u.entry.get("debate")`). The Phillips curve, the Taylor rule and the fiscal multiplier are contested
   claims, so the two-sided rule (BUILDER_RULES §2.5) applies anyway.
3. **Rubric-only grading.** No grader, no mutants, no five alternative implementations. `check_projects.py` requires the rubric
   and two exemplars at two levels (`rubric_problems`, lines 58-73), the spec's grading entry must name "rubric"
   (`GRADING_WORDS`, line 38), and `grading_problems` checks the word only.
4. **Rung 2 must be graded instantly.** `check_projects.py` accepts a completion lab or a quiz. The plan uses a completion lab.
5. **One curriculum lab, eight required.** The curriculum names one lab (`yaml:183`); BUILDER_RULES §3.4 requires a numerical
   check per key formula. The plan adds one lab per lesson (E1 and M1 precedent; §1).
6. **E1 is not built.** `course/modules/E/` does not exist (only AC, AP, CF, M, S are built). Prerequisite links go to
   `concepts.html` anchors only. The hub must not link an E1 page. `check_dag.py` is not blocked by E1 being unbuilt, because it
   uses the curriculum closure.
7. **check_dag sees linked uses only.** Unlinked uses of D1-D7 (§4) pass the tool; the verifier reads for them.
8. **Labs must be exact.** Standard-library `fractions`, with `-W error` clean under `python -I`.
9. **The hub's data-hours rules.** `check_pages.py` lesson hours 6-12 (line 227) and hub split (lines 337-342) are satisfied by
   §1.
10. **The "first-year sequence" group in `meta.yaml:133`** lists E5 with E6 and E7 as a doctoral first-year sequence group,
    while E5 is tier U. This is a curriculum-grouping observation only; the plan does not act on it (§10 Q9).

---

## 12. Open questions for the architect (numbered; each needs a decision before the builders start)

1. **B1, data for the curriculum lab and the project.** Confirm the default: SIMULATED generated economy for L02 with an
   honest-pending note; bring-your-own-data for GDP, price index, unemployment and policy rate; `ust_daily` for yields only.
   Alternatively, a redistributable national-accounts source is to be read, quoted and added to `tools/data_sources.yaml`
   first. Decision needed.
2. **D1, expectations.** `expectation` (M4) is needed for expected inflation (L06). Default: plain prose, no link (E1 Q2
   precedent). Alternative: add M4 to E5's prerequisites (a curriculum change; CF1 Q1 precedent). Decision needed.
3. **D2-D7, the other outside concepts.** Confirm the defaults in §4 (no statistics, no difference-equation concept, no
   Lagrangian, no Gordon growth, no E6/E4 concepts). Confirm no prerequisite change.
4. **Taylor rule source.** `taylor1993discretion` is registry-verified and used by E7. Use it in L07 (paper level, with the
   architect's approval), or define the rule without a source? Default: no source; the rule is a definition.
5. **Term spread and basis.** `tbill_3m` is on a discount basis (`ust_daily.note`). Confirm the spread convention: (a) `cmt_10y`
   minus `tbill_3m` as published, with the basis caveat stated; (b) a basis conversion stated in the lesson; (c) drop the
   spread from the project. Default: (a).
6. **Adversarial?** The project is a dashboard and a diagnosis, not an IC defence or debate. No 15-angle question bank. Confirm.
7. **Scope.** Confirm the scope in §2.1 item 4: closed economy; static IS-LM and AD-AS; one-sector Solow with Cobb-Douglas; central
   banking as policy rate and Taylor rule; fiscal policy as the Keynesian-cross multiplier. No New Keynesian, no open economy.
8. **B2, Atlas wording.** Confirm that the project does not use Atlas (default), or ask for `yaml:187-188` to be edited to
   name the actual data sources (a curriculum change; builders do not edit `curriculum/*.yaml`).
9. **B3, Friedman 1968.** Confirm that E5 does not cite Friedman 1968 until a record is admitted, and that the review-queue
   candidate DOI 10.2307/2296661 is rejected (it is a different article).
10. **B4, Blanchard edition.** Confirm: cite `blanchard2020macroeconomics` with no edition or year in prose (default), or
    correct the curriculum string at `yaml:182` from 8th ed. (2021) to the record's year after checking the edition.
11. **Lesson count and hours.** Confirm 8 × 10 h lessons and a 30 h project (27%). Alternatives within the rules: 9 × 9 h and
    a 29 h project; 10 × 8 h and a 30 h project.
12. **Notation.** Confirm the conflict rules in §2.3: taxes as `\mathrm{Tax}_t` with `\tau`; natural rate as `r^{n}`; `T` never
    used for taxes or time; no new NOTATION_REQUESTS.
13. **Figures.** No live figures are planned (no chart kernel needed). Confirm, or request one figure with a kernel and test
    (BUILDER_RULES §6.4).
14. **Glossary.** Terms outside the 13 concepts (unemployment rate, labour force, output gap, expected inflation, real and
    nominal GDP, multiplier as a ratio) are plain `<dfn>` with no `data-concept`. Confirm that no GLOSSARY_REQUESTS entry is
    needed.
15. **Scope of the "first-year sequence" grouping** (`meta.yaml:133`): no action planned; confirm.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 (includes the curriculum lab), L03-L04, L05-L06, L07-L08,
   project (rubric and exemplar calibration). Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/E5.verification.json`; verifier scripts archived under `ledgers/E5/scripts/` (VERIFIER §3). No
   `ledgers/E5/mutants/` (rubric-only).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B3 must be resolved
   or named as honest gaps first.

Architect decisions: pending (§12). This plan is the planner's proposal.

## Architect decisions (2026-10-28, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank.
Module specifics: the L02 lab and project use a generated SIMULATED economy; bring-your-own-data for the four series in the project; the project does not use Atlas; Friedman (1968) is not cited; Blanchard year as the registry has it or not cited.
