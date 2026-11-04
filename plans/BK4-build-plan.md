# BK4 build plan: Payments, Market Infrastructure & Fintech (2026-11-03)

Unit: **BK4 · Payments, Market Infrastructure & Fintech** · tier U · 50 h · prerequisite FC1 · no Atlas milestone ·
no debate key · grading `both` (autograder for the simulator, rubric for the memo) · output directory
`course/modules/BK/BK4/` (part code `BK`) · lab twins `tests/labs/BK4/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no check tools run. This file is the only
file written. Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and
never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Anything not in the
curriculum is marked **NOT IN CURRICULUM**. Registry facts cite `references/references.json` by key and line. Tool
behaviour is cited by file and line, or was run by the planner with `tools/coursekit.py` through `.venv/bin/python`
(`prerequisite_closure`, `concept_owner`, `units`, `curriculum()["topological_order"]`).

**Status: no blocking issue stops the builders on the lab, grader and project work. Two decisions are needed before the
lesson builders start: lesson count and hours (Q1) and builder ownership (Q2). Settlement facts in L01 and L05 are blocked
until the SEC T+1 rule is admitted (B1, Q6).**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part BK, code `BK`, title "Financial Institutions"; its studio STUDIO-BK | `curriculum/02-economics-finance-core.yaml:962-963`, `:965` |
| STUDIO-BK requires BK1 and FI1 (not BK4; studio not part of this unit) | `curriculum/02-economics-finance-core.yaml:967` |
| BK4 id and title | `curriculum/02-economics-finance-core.yaml:1071-1072` |
| Tier `U`, hours `50` | `curriculum/02-economics-finance-core.yaml:1073-1074` |
| Prereqs `[FC1]` (only) | `curriculum/02-economics-finance-core.yaml:1075` |
| Core: "Payment systems, clearing and settlement, CCPs and netting, T+1, stablecoins and tokenization, operational risk." | `curriculum/02-economics-finance-core.yaml:1076-1078` |
| `introduces` has **9** concepts, each owned by BK4 in `concepts` (planner check: 9 owners = BK4) | `curriculum/02-economics-finance-core.yaml:1079-1088`; `curriculum/curriculum.json` `concepts` |
| Sources: "BIS CPMI publications (primary)"; "Duffie & Zhu (2011), Review of Asset Pricing Studies 1(1)"; "SEC T+1 settlement rule (primary)" | `curriculum/02-economics-finance-core.yaml:1089-1092` |
| Lab: "Multilateral netting: exposure before and after a CCP." | `curriculum/02-economics-finance-core.yaml:1093` |
| Project "Clearing-house simulator"; brief: simulate a CCP default waterfall (margin, default fund, CCP capital) under a member default, and size the margin needed for a target cover | `curriculum/02-economics-finance-core.yaml:1094-1098` (title `:1095`, brief `:1096-1098`) |
| Project deliverable "Simulator plus memo."; grading `both` | `curriculum/02-economics-finance-core.yaml:1099-1100` |
| No `debate:` and no `atlas:` key on BK4 or its project (planner grep of lines 1070-1101 returns nothing) | `curriculum/02-economics-finance-core.yaml:1071-1100` (absent) |
| No Atlas entry names BK4 (planner check of the `atlas` array, A1 to A20) | `curriculum/curriculum.json` `atlas` |
| JSON row mirrors the YAML (hours 50, prereqs FC1, 9 concepts, lab, project, grading both) | `curriculum/curriculum.json:8530` (`"id": "BK4"`) |
| BS-FIN credential requires BK4; course map "Financial Markets & Institutions" lists FC1, BK1, FI4, BK4 | `curriculum/meta.yaml:63`, `curriculum/meta.yaml:79` |
| FC1 (direct prerequisite) introduces `clearing-and-settlement` and `trade-lifecycle` | `curriculum/02-economics-finance-core.yaml:381-382` |
| FC1 prereqs `[P0.1, E1]`; FC1 is built on disk | `curriculum/02-economics-finance-core.yaml:367`; `course/modules/FC/FC1/index.html` exists |
| Prerequisite closure of BK4 (planner run of `prerequisite_closure("BK4")`): **{E1, FC1, M1, M2, P0.1}**. Hours of the closure, 596 (FC1 70, E1 120, M1 100, M2 300, P0.1 6). Usable concepts from the closure's `introduces`: 61 | run output, planner; `tools/coursekit.py` `prerequisite_closure`, `units` |
| Topological positions (`curriculum.json` `topological_order`): BK4 index 32; FC1 26; FC2 30; BK1 31; FI4 33; SR1 49; SR4 73; PR4 86 | `curriculum/curriculum.json` `topological_order` (planner run) |
| Registry: `bisndcpmi` (CPMI publications index page, issuer-verified, used_by BK4) | `references/references.json:2853` |
| Registry: `duffie2011central` (Duffie & Zhu, RAPS 1(1), 2011, Crossref-verified, used_by BK4) | `references/references.json:7411` |
| Registry: `bisndbasel` (Basel III framework index page, used_by BK1 only) | `references/references.json:2815` |
| SEC T+1 rule: no registry record; review queue entry "add manually with an authoritative URL", used_by BK4 | `references/review_queue.json:830`; `references/SEED_REPORT.md:71` |
| `sec.gov` and `bis.org` are allow-listed issuer domains | `references/authorities.yaml:13` (sec.gov), `:22` (bis.org) |
| Embedded data: only `fx_daily`, `fx_monthly`, `ust_daily`; no payment, settlement, CCP or national-accounts snapshot | `tools/data_sources.yaml:19`, `:53`, `:91` (ids) |
| Notation registry: `T` (number of return observations) at line 112; macro `\R` at line 25; the symbols array starts at line 110 | `notation/notation.json:112`, `:25`, `:110` |
| Templates exist: hub, lesson, project, studio | `course/templates/` |
| `course/modules/BK/` does not exist; `tests/labs/BK4/` does not exist | planner listing |
| Binding precedents: FC1 plan (nearest built prerequisite; the same closure and grading pattern); E5 plan (structure template, sections 0-13); fixer rules; FINAL-ARCHITECT-RULINGS items 1-10 | `plans/FC1-build-plan.md`, `plans/E5-build-plan.md`, `/Users/billyribeiro/.fanout/fixer-rules.md`, `plans/FINAL-ARCHITECT-RULINGS.md` |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 50 h (`curriculum/02-economics-finance-core.yaml:1074`). Tool rules:

- each lesson declares 6-12 study hours (`tools/check_pages.py:221-228`);
- hub `data-hours-lessons + data-hours-project = 50` (`tools/check_pages.py:337-338`);
- project share 10-40 % of 50, i.e. 5 to 20 h (`tools/check_pages.py:339-340`);
- the lesson hours sum to the hub's lessons figure (`tools/check_pages.py:341-342`).

Chosen split: **5 lessons × 7 h = 35 h; project 15 h (30 %)**. 35 + 15 = 50. Feasible. Alternative in Q1: 4 × 9 h = 36 h
and a 14 h project (28 %). No STOP condition on hours. Hours are design targets and are not changed on a verifier's
estimate (FINAL-ARCHITECT-RULINGS is silent; the fixer-rules HOURS bullet applies).

### 0.3 Blocking and non-blocking issues

**B1. The SEC T+1 rule has no registry record (blocks settlement facts in L01 and L05, not the build).**
- The curriculum names it (`yaml:1092`) and the lesson core names T+1 (`yaml:1077`, `:1085`).
- No record exists (`references/references.json` has no `sec` T+1 key; `references/review_queue.json:830`;
  `references/SEED_REPORT.md:71`).
- BUILDER_RULES §2.4 forbids typing the record. The architect admits it through `tools/add_reference.py` from
  `sec.gov` (allow-listed, `references/authorities.yaml:13`).
- **Default:** until admitted, the settlement period is a parameter of the labs (the FC1 precedent, `plans/FC1-build-plan.md`
  §6 item 2). No lesson states that a market settles on T+1 as a fact.

**B2. The Duffie & Zhu paper has not been read by the planner.**
- The registry key is verified (`references/references.json:7411`), and its title and venue match the curriculum string
  (`yaml:1091`).
- Any statement about what the paper finds must come from its abstract, read by the builder (VERIFIER_RULES §2.1).
  **NOT ESTABLISHED in this plan:** the paper's findings. No claim about them appears below.

**B3. The CPMI key is an index page, not a report.**
- `bisndcpmi` points to `https://www.bis.org/committees/cpmi/publications` (`references/references.json:2853`).
- It supports a statement that the CPMI publishes on payment and market infrastructure at index level only. A statement
  about a specific CPMI report, principle or data item needs its own admitted record (REFERENCE_REQUEST, §7.2).

**B4. Real data: none, by design (non-blocking).**
- The curriculum names no dataset for BK4 (`yaml:1071-1100`). The registry and `tools/data_sources.yaml` hold no payment,
  settlement, CCP or stablecoin series (`tools/data_sources.yaml:19`, `:53`, `:91`).
- Default: all labs and the project use generated inputs labelled **SIMULATED** (BUILDER_RULES §1.7). See §6.

**B5. "About three lessons per builder" is not achievable for this unit (non-blocking; architect decides, Q2).**
- Builders A to E are fixed by the orchestration request: A to D own lessons, E owns project.html, the grader and the
  project labs. With 5 lessons, the lesson load is 2, 1, 1, 1 (or 2, 2, 1 if E also took a lesson, which the request
  excludes).
- Arithmetic bound: a lesson is at least 6 h and the project at least 5 h (10 %). So the unit holds at most
  (50 − 5) / 6 = 7 lessons. Nine lessons at about three per builder cannot fit.

**B6. Hub prerequisite link to a built page (non-blocking).**
- FC1 is built (`course/modules/FC/FC1/index.html`), so a hub link `../../FC/FC1/index.html` is possible. E5 could not link
  E1 because E1 was unbuilt (`plans/E5-build-plan.md` §11 item 6). Q14 decides.

**Not established by the planner (no claim in this plan depends on them):**
- The findings of Duffie & Zhu (2011) (B2).
- Any settlement-cycle fact, including the T+1 rule's effective date and scope (B1).
- The design, size or history of any payment system, CCP, stablecoin or tokenization platform. No registry source covers
  them (§7.2).
- Any empirical result on CCP effects, margin procyclicality, stablecoin redemption or operational-loss frequency.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms, Q1 and Q2)

5 lessons × 7 h = 35 h; project 15 h; total 50 h. Concept counts per row sum to 2+2+2+2+1 = 9, each concept in exactly one
row (`yaml:1080-1088`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:1080-1088`) | Lab (twin id, `tests/labs/BK4/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Payment systems and the settlement cycle | `payment-system` (`:1080`), `settlement-cycle` (`:1085`) | `lab-BK4-L01-1`: gross real-time and deferred net liquidity on a SIMULATED three-bank day, in integer cents, the peak intraday need printed for each design | 7 | Builder A |
| L02 | Central counterparties and multilateral netting | `central-counterparty` (`:1081`), `multilateral-netting` (`:1082`) | `lab-BK4-L02-1` (**the curriculum lab**, `yaml:1093`): multilateral netting exposure before and after a CCP on a seeded SIMULATED four-member trade set, exact integers | 7 | Builder A |
| L03 | The CCP default waterfall and margin cover | `ccp-default-waterfall` (`:1083`), `margin-cover` (`:1084`) | `lab-BK4-L03-1`: the waterfall layers for seeded SIMULATED losses; the margin for a target cover checked against a brute-force search | 7 | Builder B |
| L04 | Stablecoins and tokenization | `stablecoin` (`:1086`), `tokenization` (`:1087`) | `lab-BK4-L04-1`: reserve coverage of a stablecoin under a seeded SIMULATED redemption path, exact in `Fraction` | 7 | Builder C |
| L05 | Operational risk in market infrastructure | `operational-risk` (`:1088`) | `lab-BK4-L05-1`: the expected cost of settlement failures for three trades by exact enumeration of all fail patterns, against the closed form | 7 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 35 / 15 | none | none | - | Builder A |
| project | Clearing-house simulator (`both`, §5): `project.html`, the grader, the rubric and exemplars | none | `lab-BK4-project-1` (rung 1), `lab-BK4-project-2` (rung 2, `class="lab completion"`), `lab-BK4-project-3` (rung 3 check) | 15 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` (§5.5) | none | none | - | Builder E (last builder, per the request) |
| cards | `cards.json` from L01-L05 | none | none | - | Builder F (after A-E) |

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes `index.html` after L01 and L02
exist. Builder E writes the project, grader and rubric and does not depend on the lesson wording, only on the frozen
interface in §5.2.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses only, §4):
- L01 uses FC1's `clearing-and-settlement` and `trade-lifecycle` (in the closure, linkable, `yaml:381-382`) for the
  settlement context; defines `payment-system` first, then `settlement-cycle`.
- L02 uses L01's `payment-system` (a link to `Lnn.html#def-payment-system`) to explain why a CCP is not a payment system;
  defines `central-counterparty`, then `multilateral-netting`.
- L03 uses L02's `central-counterparty` and `multilateral-netting`; defines `ccp-default-waterfall`, then `margin-cover`.
- L04 uses L01's `settlement-cycle` and the closure's FC1 `bank-money-creation` (linkable, `yaml:373`) for the comparison
  with bank money; defines `stablecoin`, then `tokenization`.
- L05 uses L01's `settlement-cycle` for the delay and L04 only in prose; defines `operational-risk`.

Hours check: 5 × 7 = 35 (hub `data-hours-lessons="35"`); project 15 (hub `data-hours-project="15"`); total 50.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to BK4)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/FC1-build-plan.md` (its Architect
decisions section is binding precedent), `plans/E5-build-plan.md`, `plans/FINAL-ARCHITECT-RULINGS.md` and this file. Study
`course/modules/FC/FC1/` for the closest built layout (hub, lessons, grader panel). `course/templates/` holds the skeletons.
Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`, or integer
   cents) and rounded only at display. A rounded figure states its rounding rule (half up, to the cent). Precedents:
   AC4 KNOWN LIMITATION 3, CF1 L01 Remark 5.2, FC1 §2.1 item 1. For BK4 this covers every coverage ratio, every margin,
   every netting total.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only
   what the printed numbers show (fixer-rules, lab-statement bullet). Precedent: M1 LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Only the registry keys in §7 may be cited. Index-level keys (`bisndcpmi`, `bisndbasel`)
   support index-level statements only. `duffie2011central` supports paper-level attribution; any statement of its
   findings needs the abstract read by the builder (B2). No page, table, equation, coefficient or date is typed from
   memory (fixer-rules, attribution bullet; VERIFIER §2.1).
4. **Scope words need a computation.** "every", "all", "any", "always", "never", "each CCP", "the market", "the industry",
   "market infrastructure", "systemic" are used only where a proof, a finite check, a lab or an explicit enumeration makes
   the claim (fixer-rules, scope-words bullet). The scope of BK4 is stated on the hub: one defaulting member at a time, a fixed set of
   scenarios, and the settlement and netting rules as defined in the page.
5. **Define before use.** Each of the 9 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Terms outside the 9 (initial margin, variation margin, default fund, CCP capital, novation,
   gross settlement, net settlement, real-time gross settlement, reserves, redemption, scenario) are defined in prose at first
   use with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation lists its numbered Assumptions (A1, A2, ...)
   before the statement (fixer-rules, ASSUMED FACTS bullet). Examples the builders must state: the waterfall's layer order
   is an assumed rule of the simulator (A1); the cover-sizing result needs an integer target in 1 to 10000 basis points and a
   non-empty scenario set (A1, A2); the netting identity needs obligations fixed before netting (A1).
7. **Grader rules (apply, because BK4 is graded by an autograder).** The fixer-rules PROJECT GRADERS bullet and FINAL-ARCHITECT-RULINGS 9-10 apply
   to `grader/` (§5.5): a test demands an exception only for a condition the page names (§5.2 table); every named condition
   has an isolated test in both directions of its inequality; ten student-error mutants; five alternative correct
   implementations pass seeds 0-49; a failing check does not print the expected value (`__tracebackhide__`); the collect-only
   count quoted on the page is updated.
8. **Money is integer cents.** Every money value in the simulator and in the labs is a Python `int` in cents, computed from
   exact integer arithmetic (or `Fraction`) and rounded once by the rule in §5.3. No float money, no tolerance on money.
   Precedent: FC1 §2.1 item 8, AC4 Q9/Q10. Coverage ratios are integer basis points, floor-rounded, stated on the page.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container (fixer-rules, no-horizontal-scroll wording in the money and process-words bullet). Enforced by `page_smoke.py`, which the verifier runs.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network
    (`tools/run_labs.py`). Precedent: `tests/labs/M1/lab-M1-L04-1.py`.
11. **Mutants of labs are not graded.** A lab that still exits 0 under a mutation is not a defect unless a lesson sentence
    claims the lab asserts that property (FINAL-ARCHITECT-RULINGS 9; fixer-rules, LAB MUTANTS bullet). Labs do not gain asserts to kill
    mutants. Mutation testing applies to `grader/` only.
12. **Basis-explicit rates and ratios.** A coverage ratio, a reserve ratio or a share states its numerator, denominator,
    unit (cents, share, basis points) and rounding rule (fixer-rules, causal and ratio bullet; E5 §2.1 item 11).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation on the page. A B- or
  C-graded claim names its published counter-evidence (BUILDER_RULES §2.5). **The registry holds no record for CCP
  effects on counterparty risk, margin procyclicality, stablecoin redemption behaviour, tokenization or operational-loss
  frequency.** Those claims are either derivations (grade T, conditional on the stated model), graded C with the basis named
  and the counter-evidence lead named, or removed. The lead goes to REFERENCE_REQUESTS (§7.2).
- Concepts: the §1 table; `<dfn>` only for the 9 registered concepts plus plain `<dfn>` for other terms. No
  `<a class="concept">` for any concept outside the prerequisite closure {E1, FC1, M1, M2, P0.1} (§4, DAG).
- Prerequisite links: `href="../../../concepts.html#<id>"` for FC1, E1, M1, M2 and P0.1 concepts (the concept index, the
  pattern BUILDER_RULES §4.1 gives for prerequisite modules); `href="Lnn.html#def-<id>"` for earlier BK4 lessons. A lesson
  never links a concept defined in a later lesson. A hub link to FC1's built hub is Q14.
- Labs: code lives once in `tests/labs/BK4/lab-BK4-Lnn-1.py` (and `lab-BK4-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match
  `lab-BK4-<page>-<n>`. Standard library only (`fractions`, `math`, `random.Random(seed)`, `itertools`); seeded RNG only;
  no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: every lab and every figure that uses generated or illustrative parameter sets carries **SIMULATED**.
  The planner's default is to label all five lesson labs and all project inputs, because no real data is used (§6).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`). Request
  changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments (E5 §2.2; precedent M1 "Convention (project Q5)").
- Banned strings (`tools/check_pages.py`, `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis `...` outside code.
- Percent and basis-point statements state the base and the direction. Growth and rate statements state the convention.
- A finite enumeration is grade C with its basis named, not grade T (E5 §2.2; precedent M1 L06). An exact enumeration used
  as a lab check is labelled as a check, with its basis.
- Every "checked" or "verified" claim names the lab, the line or the test that did the check (fixer-rules, lab-statement bullet).
- Hub lesson titles match each lesson's `<h1>` at integration (CF1 KNOWN 3).
- Quiz explanations are read against their lesson (CF1 KNOWN 6).
- Settlement and market facts are stated only from an admitted source (B1). Until then, a settlement period is a lab
  parameter with the value and its unit printed by the lab (FC1 §6 item 2 precedent).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols and macros that BK4 must not give a different meaning (`notation/notation.json:110-`, `:112`, `:25`):

| Registered symbol | Registered meaning (locator) | BK4 conflict and rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation.json:112`, module S1) | **Conflict risk.** The rule name "T+1" (`yaml:1077`, `:1085`) is a convention label, not a symbol. In math, a settlement lag is `d` (business days) and no bare `T` appears. In prose, "T+1" appears only as the name of the rule, never as a time index or a count. Q7. |
| `R_f` | gross riskless return (AP1) | Not used. A rate is `r` or `y`, defined on first use. |
| `R^\ast`, `R^{e\ast}` | SDF payoff-space objects (AP1) | Not used. |
| `\mathbb{Q}` | risk-neutral measure (AP1) | Not used. Never write `Q` for a quantity. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and quantile (M4) | Not used. The margin sizing is an empirical order statistic, not a normal quantile. |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (M4) | Not used. |
| `\E`, `\Var`, `\Cov`, `\Corr` (macros) | expectation, variance, covariance, correlation (`notation.json:4-`) | Allowed where the page uses them. The margin text uses "volatility" in prose and no macro (M3 precedent, FINAL-ARCHITECT-RULINGS 3). |
| `\R` (macro) | real numbers (`notation.json:25`) | Standard. Use `\R`, never `\mathbb{R}` (FINAL-ARCHITECT-RULINGS 1). |

Local symbols (allowed; `notation.json` `about`: letters conventionally local are defined per lesson): `N` number of
members, `i` a member index, `d` a settlement lag in business days, `IM_i` (write `\mathrm{IM}_i`) initial margin posted by
member i, `DF_i` (write `\mathrm{DF}_i`) default-fund contribution of member i, `K` CCP capital, `L_s` loss in scenario `s`
out of `S` scenarios, `k` an order-statistic index, `c` a target cover level as a fraction (in code, the integer
`target_bps`), `x` a redemption share, `\rho` a reserve-to-claims ratio, `h` a haircut, `p` a fail probability. Each is
defined on the lesson where it first appears and never redefined. Money is written in cents, with the unit stated.

NOTATION_REQUESTS: none. The plan uses only local symbols and the registered `\R` and `\E` macros.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2): why it matters (at most 120 words), core
content, inline labs, where the canon breaks, misconceptions (at least 3), problem set (at least 3 in each of Mechanics,
Proof, Empirical and Research, each with a worked solution), key-results table, and a retrieval quiz of 8-15 items.
**Hours note:** nine problem sets of twelve items each in 7 h is tight; the builder reduces the lesson's depth before it
reduces any required part (the hours are design targets, §0.2).

- **L01 · `payment-system`, `settlement-cycle`.**
  - `payment-system`: the two designs named in the definition (`yaml:1080`), real-time gross settlement and deferred net
    settlement. Definitions and the liquidity arithmetic are grade T. Any statement about which real systems use which
    design is removed unless an admitted source covers it (REFERENCE_REQUEST, §7.2).
  - `settlement-cycle`: the period between trade and settlement as a parameter `d`. The T+1 rule is named, not stated as
    fact, until B1 is closed (Q6).
  - Links: FC1 `clearing-and-settlement` and `trade-lifecycle` (`yaml:381-382`) for the settlement context.
  - Lab `lab-BK4-L01-1` (SIMULATED): three banks, a seeded day of payments in integer cents. The lab prints the peak
    intraday liquidity need under gross real-time settlement and the net debit under deferred net settlement for each bank.
    The hypothesis states which need is larger for the seed printed. The interpretation is limited to the printed day.
  - Misconception to correct: net settlement removes the need for liquidity (it reduces, it does not remove, the amount
    moved; the lab prints the net debit).

- **L02 · `central-counterparty`, `multilateral-netting` (curriculum lab, `yaml:1093`).**
  - `central-counterparty`: novation, so that the CCP becomes the counterparty to each side. Definition, grade T as a
    contract structure stated on the page.
  - `multilateral-netting`: the net obligation of each member is the sum of its signed trade obligations. The identity that
    the sum of net obligations is zero (with no outside party) is grade T, with the assumption that obligations are fixed
    before netting (A1).
  - Paper-level attribution: `duffie2011central` (`references/references.json:7411`) may be cited at paper level for the
    question it asks (its title is "Does a Central Clearing Counterparty Reduce Counterparty Risk?", the registry title).
    Its answer is not stated on the page until the builder has read the abstract (B2).
  - Claim "a CCP reduces counterparty risk": graded **B** at most, two-sided. Counter-evidence must be named. None is in the
    registry (REFERENCE_REQUEST, §7.2). Until admitted, the sentence is graded C with its basis, or removed.
  - Lab `lab-BK4-L02-1` (SIMULATED, the curriculum lab): four members, six seeded trades; the gross notional, the gross
    exposure before novation and the net obligations after netting, all in integer cents. The hypothesis states the sign
    and size relation the printed numbers must show, then the lab checks the zero-sum identity.
  - Canon break: the CCP as one counterparty abstracts from its own default risk and from the default waterfall, which L03
    supplies.

- **L03 · `ccp-default-waterfall`, `margin-cover`.**
  - `ccp-default-waterfall`: the layer order of §5.2 (defaulter initial margin, defaulter default fund, CCP capital,
    surviving members' default funds pro rata with the rounding rule of §5.3). The order is an assumed rule of the
    model (A1), and the page says so. Grade T for the arithmetic identity that the layers sum to the loss (the uncovered
    part is named).
  - `margin-cover`: the cover of a margin `M` over `S` scenario losses, `cover(M) = #{s : L_s <= M} / S`, written in integer
    basis points with floor rounding (§5.3). The sizing result: the minimal margin with cover at least `target_bps` is the
    `k`-th smallest scenario loss, `k = ceil(target_bps · S / 10000)`. Derivation (grade T, assumptions A1 integer target in
    1 to 10000, A2 non-empty scenario set): for an integer margin `M`, `10000·#{L_s <= M} // S >= t` holds iff
    `#{L_s <= M} >= t·S/10000`, which holds iff `#{L_s <= M} >= k`, which holds iff `M >= L_(k)`. The builder writes this
    proof and the lab checks it by brute-force search.
  - Canon break: the scenario set is the model's, not the market's. Without a time to close out, the waterfall ignores
    the path of losses during the close-out period.
  - Outside-closure terms used in prose only (§4): futures margining and variation margin for cleared derivatives; the
    recovery waterfall of lending (its owner's name collides with `ccp-default-waterfall`, D7).
  - Lab `lab-BK4-L03-1` (SIMULATED): seeded losses for one default. The lab prints each layer's amount for three
    scenarios (one within the margin, one reaching the default fund, one reaching the surviving members), the sizing result
    for two targets, and the brute-force minimal margin for the same targets. The two must agree.

- **L04 · `stablecoin`, `tokenization`.**
  - `stablecoin`: a token whose value is meant to track a reference unit, with the reserve-to-claims ratio `\rho = \mathrm{Res}_0 / C_0`
    as its basis-explicit measure. Definition grade T as a definition.
  - Derivation (grade T, assumptions A1 redemptions paid at par from reserves, A2 no new issuance, A3 no fee): after a
    redemption share `x` of claims (with `0 <= x < 1`), the coverage is `(\rho - x) / (1 - x)`. The coverage is below 1
    if and only if `\rho < 1`. Derive and prove it on the page; the lab checks it exactly.
  - Claims about observed stablecoin redemption, runs or issuer reserves: none in this plan (no registry record; §7.2).
    Such a sentence is removed or graded C with its basis named. Any "widely claimed" sentence is graded D and flagged.
  - `tokenization`: a definition of a recorded claim on an asset that transfers on a shared record. Definition only. Any
    claim about the efficiency of tokenized settlement is removed until a source is admitted.
  - Links: FC1 `bank-money-creation` (`yaml:373`) for the comparison with bank deposits.
  - Lab `lab-BK4-L04-1` (SIMULATED): a seeded path of redemption shares and two reserve ratios, coverage in `Fraction`,
    rounded to basis points by the stated rule. The hypothesis states that coverage is below 1 exactly when `\rho < 1`, and the
    lab prints both cases.
  - Canon break: the derivation assumes par redemptions with no haircut. A forced sale of reserves at a discount (a haircut
    `h`) lowers reserves and is outside the lab; the lesson names it as the limit.

- **L05 · `operational-risk`.**
  - Definition: a loss from failed or inadequate processes, people, systems or external events. Definition grade T.
  - Index-level Basel reference only: `bisndbasel` (`references/references.json:2815`) supports the statement that the
    Basel III framework exists at index level. A statement of its operational-risk section needs the section read and a
    locator, which the planner did not do. Q13 (REFERENCE_REQUEST for the operational-risk standard, lead only).
  - Settlement-fail cost model: each of three trades fails with probability `p` (a Fraction), a failed trade costs `c` cents
    per business day of delay, and the delay is `d_i` days. Expected cost by exact enumeration over all `2^3` fail patterns
    equals the closed form `3 · p · c · d` when every failure lasts `d` business days (a planner-stated form, to be re-derived by the builder). The lab checks both (grade T for
    the closed form; the enumeration is a check).
  - Claims about the frequency of real settlement failures or operational losses: none (no record).
  - Lab `lab-BK4-L05-1` (SIMULATED, illustrative parameters): the enumeration and the closed form, both in `Fraction`,
    and the rounding rule for cents (half up, once).
  - Canon break: the model has independent failures and a fixed cost per day. Dependence and recovery actions are outside.

---

## 4. DAG problems (concepts that natural BK4 content would use outside the closure)

Prerequisite closure of BK4 (computed by the planner): **{E1, FC1, M1, M2, P0.1}**. Owners and topological positions below
are from `curriculum/curriculum.json` `concepts` and `topological_order` (planner run). Each row has a resolution, so no
DAG_DEFECT blocks the build. `check_dag.py` checks linked uses only (`tools/check_dag.py` docstring), so the verifier reads
every lesson for the unlinked names in column 2.

| Ref | Concept(s) | Owner, topo index | Where natural BK4 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `futures-margining`, `futures-contract` | FC2, 30 | variation margin for cleared derivatives (L03); futures central clearing (L02) | Plain prose. "Variation margin" is a plain `<dfn>` in L03. No link. Q3 |
| D2 | `repo-haircut`, `bank-reserves`, `central-bank-balance-sheet` | FI4, 33 | haircut on a reserve asset (L04, stress); central-bank money in RTGS (L01) | Plain prose, names only. No link. |
| D3 | `central-clearing-mandate`, `treasury-market-liquidity` | SR4, 73 | clearing of government-bond trades (L02 context) | Not used. No claims. |
| D4 | `credit-default-swap` | CR2, 99 | CCP clearing of credit derivatives (L02 context) | Not used. |
| D5 | `bank-run`, `uninsured-deposit-run`, `run-on-repo`, `liquidity-spiral` | SR1, 49 | redemption runs on a stablecoin (L04) | Plain prose, names only. No claim without a source. |
| D6 | `stablecoin-reserve-run`, `crypto-risk-factors` | X4, 119 | stablecoin reserve runs (L04) | Plain prose. No link (X4 is a later module). |
| D7 | `recovery-waterfall` | CR4, 101 | a name collision: the recovery waterfall of lending versus `ccp-default-waterfall` (L03) | Plain prose. BK4 says "CCP default waterfall" only. No cross-link, to avoid two definitions of one term. |
| D8 | `value-at-risk`, `expected-shortfall`, `stress-testing` | PR4, 86 | margin models and stress scenarios (L03, project) | Not used. The sizing rule is an order statistic. |
| D9 | `monte-carlo-integration` | M8, 38 | seeded scenario sampling (L03, project) | Plain prose ("seeded scenarios"). Not used as a method. |
| D10 | `variance`, `covariance-matrix` | M4, 12 | margin volatility in prose (L03) | Plain prose only (FINAL-ARCHITECT-RULINGS 3 precedent). Not used. |
| D11 | `liquidity-coverage-ratio`, `net-stable-funding-ratio` | BK1, 31 | a liquidity-ratio analogy for stablecoin reserves (L04) | Not used. |
| D12 | `safe-asset-convenience-yield` | E8, 41 | a stablecoin as a safe asset (L04) | Not used. |
| D13 | `model-risk-management` | LX2, 37 | model failure as operational risk (L05) | Plain prose, optional. No link. |

In-closure concepts the builders may link (not DAG issues): FC1 `clearing-and-settlement`, `trade-lifecycle`,
`bank-money-creation`, `financial-intermediary` (`yaml:373-374`); M1 `present-value`, `discount-factor` (`01-foundations.yaml`,
the M1 block; closure member); M2 `derivative` (closure member).

### 4.1 Missing-prerequisite questions (DAG questions for the architect)

- **DQ1. Add FC2 as a prerequisite of BK4?** FC2 (`futures-contract`, `futures-margining`) would make variation margin a
  defined term. Topological order allows it (FC2 index 30, before BK4 index 32). The closure would grow from 5 modules to
  9: it adds AC1, CF1, FC2 and M4, which is 390 h of additional closure (planner run). **Recommended: no** (Q3). The plan
  keeps variation margin as plain prose in L03, which is what the curriculum's BK4 text needs (`yaml:1076-1078` names no
  futures).
- **DQ2. Add FI4 (`repo-haircut`, `bank-reserves`) as a prerequisite?** Not possible without reordering: FI4 has topological
  index 33, after BK4 (index 32), so adding it would put a prerequisite after its dependent. **Recommended: no.**
- **DQ3. Add a CR4 or PR4 concept?** Not needed. D7 and D8 are resolved in prose.

---

## 5. Project (`project.html`, Builder E): `both` (autograder + rubric), ladder, spec, grader, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py:33` requires the order)

1. **Rung 1, worked example** (`lab-BK4-project-1`, SIMULATED): one fully solved, annotated default on a four-member CCP,
   with a generated scenario set of 40 losses. Each step has a "why" annotation: the layer order, the survivor share, the
   cover sizing. Tier U: full length.
2. **Rung 2, completion** (`lab-BK4-project-2`, `class="lab completion"`, SIMULATED): the survivor-share line and the
   sizing-index line are removed (`___`). Graded instantly by its instant check. Its twin is the completed solution; every
   page line equals the twin line or contains a blank (`tools/run_labs.py` completion rule, as in FC1 §5.1).
3. **Rung 3, independent project** (graded): the simulator `clearing_house.py` to the §5.2 interface (autograder), and a
   one-to-two-page memo `memo.md` (rubric). `lab-BK4-project-3` is the rung-3 check: it recomputes the default state of the
   page's reference instance and prints the waterfall table the student's simulator must reproduce.
4. **Rung 4, stretch** (optional, not graded): a second default in the same scenario set, with the surviving pool reduced
   by the first default's payments, or a re-margining after one netting cycle. No ceiling. Not graded.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A clearing house novates each trade and holds margin from its members. When one member defaults, its margin
  and default fund are used first, then the clearing house's own capital, then the surviving members' default funds. The
  student builds the loss waterfall for one default and sizes the defaulter's margin for a target cover.
- **Inputs.** Generated SIMULATED inputs from `grader/instance.py` (no data files, §6): a member set `{1..N}` with
  `N` from 4 to 6; for each member, an initial margin `IM_i` and a default-fund contribution `DF_i` (integer cents, `DF_i >= 1`);
  the clearing house capital `K` (integer cents, `K >= 0`); the defaulting member's id; a list of `S` scenario losses
  `L_s` (integer cents, `L_s >= 0`, `S` from 40 to 80); a target cover `target_bps` from {9900, 9950, 9975}.
- **Interface (frozen before building; Q9).** `clearing_house.py` exposes:
  - `waterfall(loss_cents: int, defaulter_id: int, initial_margin_cents: dict[int, int], default_fund_cents: dict[int, int], ccp_capital_cents: int) -> Waterfall`.
  - `Waterfall`, a frozen dataclass with fields `margin_cents: int`, `default_fund_cents: int`, `ccp_capital_cents: int`,
    `survivor_cents: dict[int, int]` (surviving member id to cents, every surviving member present, zero allowed), and
    `uncovered_cents: int`.
  - `margin_for_cover(losses_cents: list[int], target_bps: int) -> int`.
  - `cover_bps(losses_cents: list[int], margin_cents: int) -> int`.
- **Rules (stated on the page; the simulator follows them exactly).**
  - Layers, with `L` the loss and `IM_d`, `DF_d` the defaulter's margin and default fund:
    `a1 = min(L, IM_d)`; `a2 = min(L - a1, DF_d)`; `a3 = min(L - a1 - a2, K)`; `R = L - a1 - a2 - a3`.
  - Surviving default funds: `T` is the sum of the surviving members' `DF_i`. If `R >= T`, each survivor pays its whole `DF_i`
    and `uncovered = R - T`. If `R < T`, `share_i = (R · DF_i) // T` for each survivor; the remainder
    `r = R - sum(share_i)` (with `0 <= r`) goes one cent each to the first `r` surviving members with `DF_i > 0`, in ascending
    id order; `uncovered = 0`. Members with `DF_i = 0` receive zero.
  - Invariant (checked by the grader): `a1 + a2 + a3 + sum(survivor_cents) + uncovered = L`.
  - `cover_bps(L, M) = (10000 · #{s : L_s <= M}) // S` (an integer; floor). The margin with cover at least `target_bps`
    is `sorted(L)[k - 1]` with `k = ceil(target_bps · S / 10000)`, computed in integers as `-((-target_bps * S) // 10000)`.
- **Exception table (named conditions only; these are the only conditions the grader requires an exception for).**

| Condition the page names | Exception | Message must name |
|---|---|---|
| `margin_for_cover`: `losses_cents` empty | `ValueError` | "at least one scenario is needed" |
| `margin_for_cover`: `target_bps` outside 1 to 10000 | `ValueError` | the allowed range |
| `margin_for_cover` or `cover_bps`: a negative loss | `ValueError` | "losses cannot be negative" |
| `waterfall`: a negative amount or a negative loss | `ValueError` | the amount that is negative |
| `waterfall`: `defaulter_id` not among the member ids | `ValueError` | the defaulter id |

  Any other invalid input may raise any exception or return; no test requires a type for it.
- **Required outputs.** `clearing_house.py` with the interface above and a docstring stating the conventions (sign,
  integer cents, rounding). `memo.md` (the rubric memo, §5.4).
- **Constraints.** Integer cents; standard library only; no network; the same code runs in Pyodide and under pytest.
- **Grading.** Both: an autograder (the test suite, §5.5) and a rubric (the memo, §5.4). The spec names both, "autograder"
  and "rubric" (`check_projects.py:38`, `:41-49`).
- **Reading list.** `ol.reading-list` cites `duffie2011central` and `bisndcpmi` (registry keys only; §7). The builder
  reads the Duffie & Zhu abstract before the memo cites it (B2).

### 5.3 Rounding and conventions (stated once; used in every output)

- Period convention: the settlement date is period 0; the scenario index starts at 1.
- Money: integer cents throughout. A share is `(R · DF_i) // T` (floor on a non-negative integer); the remainder rule of §5.2
  makes the shares sum exactly to `R`. No rounding of an intermediate value.
- Cover: integer basis points, floored; a target is compared as `10000 · count >= target_bps · S` (no division).
- Negative losses are rejected (§5.2 exception table); the rounding rule never sees a negative value.

### 5.4 Rubric (`table.rubric#rubric`, `check_projects.py` `rubric_problems`)

Five criteria (4-7 required). Each criterion row has a criterion name in a `th` and exactly four `td` cells for levels 4
down to 1 (`check_projects.py:58-73`). Every level descriptor is observable.

1. **Waterfall order and layer amounts.** L4: names each layer in order, gives its cents for a stated scenario, and states
   that a layer is used only after the one before is exhausted. L1: "describes the waterfall".
2. **Margin sizing.** L4: states the target in basis points, the value of `k`, the sorted position used, and checks cover at
   the chosen margin and at one cent below. L1: "sets a margin".
3. **Survivor sharing and rounding.** L4: states the pro rata rule and the remainder rule, and shows the survivor cents sum
   to the residual for a stated scenario. L1: "shares the losses".
4. **Interpretation and recommendation.** L4: recommends one margin with the cover it achieves and the count of scenarios
   that reach the surviving members or leave an uncovered loss, and compares one alternative. L1: "makes a recommendation".
5. **Limits and evidence.** L4: names the model limits used (one default at a time, a fixed scenario set, no close-out
   period, no procyclicality), and for each claim graded B or C names its counter-evidence or the REFERENCE_REQUEST
   status. L1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written memos on a SIMULATED
instance, each passage annotated with the descriptors it meets or misses (`check_projects.py` requires levels 1-4 and at
least two). Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`,
as in M1, E1 and E5). The page shows where the student's scores diverge from the exemplar scores. Calibration: the verifier
scores both exemplars blind, within one level per criterion (VERIFIER §2.6). Adversarial question bank: not required (Q6).

### 5.5 Autograder design (`grader/`, Builder E)

Files (`course/modules/BK/BK4/grader/`): `instance.py`, `reference.py` (the full solution; excluded from deployment,
BLUEPRINT §7; FINAL-ARCHITECT-RULINGS 4 for the deploy rule), `starter.py` (stubs raising `NotImplementedError`),
`test_project.py`. Grader panel on `project.html`: `<section class="grader-panel" id="grader" data-unit="BK4" data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="clearing_house.py" data-starter="starter.py">`
(`check_projects.py` `check_unit`, grader-panel block). `data-packages` is empty (standard library only).

- `instance.py`: `make_instance(seed: int) -> dict` (the exact signature `check_projects.py` tests). Deterministic per seed
  from `random.Random(seed)`. Labelled **SIMULATED** in the docstring. Validity for every seed: member ids `1..N`; `DF_i >= 1`;
  `IM_i >= 0`; `K >= 0`; the defaulter is a member; `S` in 40 to 80; all losses non-negative integers; `target_bps` in the
  listed set. Each instance includes at least one scenario within the defaulter's margin, one reaching the default fund,
  and one reaching the surviving members. Materiality: across seeds 0-49 the margin answer `margin_for_cover` differs for at
  least 40 seeds, and the uncovered totals differ (answers change, not only labels; the verifier checks 20 sampled seeds).
- `reference.py`: the full solution in integers, following §5.2 and §5.3 exactly. Passes every test on seeds 0-49.
- `starter.py`: stubs that raise `NotImplementedError`. The suite fails on it, naming the property, not a stack trace.
- `test_project.py` (properties and numbers; each test recomputes its expected value from the instance and an oracle
  written separately from `reference.py`; no hard-coded answers; `__tracebackhide__` in every helper so a failure prints no
  expected value):
  - conservation: `a1 + a2 + a3 + sum(survivor_cents) + uncovered = L` for every scenario of every seed in the test;
  - layer order fixtures: a fixed fixture with `IM_d = 100`, `DF_d = 50`, `K = 30`, survivors `{1: 40, 2: 60}`. Losses 80
    (margin only), 120 (margin and default fund), 170 (margin, default fund and capital), 200 (survivors pay 8 and 12),
    205 (survivors pay 10 and 15), 300 (survivors pay 40 and 60, uncovered 20). These are hand-computed on the page, not
    seed-derived (Q10). Each case is an isolated test, both sides of each boundary (for example 180 and 181);
  - remainder rule fixture: survivors `{1: 1, 2: 1, 3: 1}`, the residual `R = 1` goes to member 1, and `R = 2` to members 1 and
    2 (kills a last-survivor rule and a truncation rule);
  - a loss equal to the margin is covered (`L = M`), an isolated test (kills a strict-inequality cover);
  - sizing fixtures: losses `[10, 20, 30, 40, 50]` with `target_bps` 8000 give 40, with 8001 give 50, with 10000 give 50;
    losses `[10, 20, 30, 40]` with 5000 give 20 (kills an off-by-one and a strict count); `S = 1` returns the one loss;
  - sizing against a brute-force search over integer margins on every seed (minimal `M` with `cover_bps(L, M) >= target`);
  - cover fixtures: one of three losses covered gives 3333; the cover is floored;
  - monotonicity: `margin_for_cover` is non-decreasing in `target_bps` on each seed;
  - integer output: every money field is an `int`;
  - exception table (§5.2): each named condition raises `ValueError` naming the condition, and the boundary values 1 and 10000
    are accepted (both directions of each inequality). No other exception is tested;
  - instance dependence: across seeds 0-49 there are at least 3 distinct sizing answers.
  - failure messages name the violated property and give a hint at the concept. They never print the answer.
- Dual mode: the same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (must all pass seeds 0-49; the verifier writes them as test-only fixtures in
  a scratch checkout and archives the scripts under `ledgers/BK4/scripts/`, FINAL-ARCHITECT-RULINGS 10): (1) list
  comprehensions and `sorted()` for sizing, a generator for the waterfall; (2) a class-based `ClearingHouse` with methods that
  return the frozen `Waterfall`; (3) `Fraction` throughout, with `math.ceil` on the exact `Fraction(target_bps * S, 10000)`
  and a floor on the exact share; (4) integer-only, with ceiling division `-((-x) // y)`; (5) bisection over integer margins
  on the `cover_bps` predicate, with no sort. A float implementation is an alternative only if it applies the same rules to
  exact values; a float that is wrong on the stated rule is a mutant, not an alternative (FINAL-ARCHITECT-RULINGS 10).
- **Student-error mutants (ten).** The verifier writes ten single-change copies of `reference.py` to
  `ledgers/BK4/mutants/*.py`, each opening with a one-line docstring that names the student error. `tools/mutate_graders.py
  --unit BK4 --seeds 0-9` must kill each. The mutants:
  1. the default fund is used before the defaulter's margin (layer order swapped);
  2. the clearing house capital is used before the default fund (layer order swapped);
  3. the surviving members are charged by count (equal shares), not by their contributions;
  4. the remainder cents go to the last surviving member, not the first;
  5. survivor shares are truncated with no remainder rule, so the invariant breaks;
  6. the uncovered loss is dropped, not reported;
  7. the sizing index is `floor` instead of `ceil`;
  8. the cover counts strictly below the margin (`L_s < M`), a strict-inequality error;
  9. the sizing returns the largest loss for every target (no quantile);
  10. a hard-coded answer for seed 0 (the sizing returns the seed-0 margin for every instance).
  Each mutant must fail at least one test. A mutant that differs from the reference only where the page states nothing is moved to
  `ledgers/BK4/equivalent/` with a README proof (FINAL-ARCHITECT-RULINGS 9).

### 5.6 Time budget (`<table id="hours">`, sums to 15 h; every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED default, annotated line by line |
| Rung 2, completion problem | 2 | Fill the survivor-share line and the sizing-index line, then run the instant check |
| Waterfall layers and survivor sharing | 3 | Layer order, the remainder rule, the uncovered loss |
| Margin sizing and the cover check | 3 | Order statistic, ceiling index, integer cover in basis points |
| Edge cases and the suite on seeds 0-9 | 2 | Exception table, instance validity, the local pytest run |
| Memo (rubric) | 2 | One to two pages with the five rubric criteria |
| Self-assessment against the exemplars | 1 | Score the memo with the rubric, compare with exemplar-a and exemplar-b |
| **Total** | **15** | Equals `data-hours-project` on the hub |

The planner's own estimate of the autograder part (waterfall, sizing, tests) is 8 h for a student who has the rules. The
component table allots 8 h to those parts (3 + 3 + 2). The verifier estimates each component independently (VERIFIER §2.6).

---

## 6. Real-data policy

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily` (`tools/data_sources.yaml:19`, `:53`,
  `:91`). None of them carries a payment, settlement, CCP, stablecoin or operational series. **None is used by BK4.**
- **Not embedded, and no grant found:** no payment-system, settlement, CCP margin, stablecoin reserve or operational-loss
  series exists in `tools/data_sources.yaml` or in its `rejected:` list. The curriculum names no dataset (`yaml:1071-1100`).
- **Default:** all labs and project inputs are generated and labelled **SIMULATED**. No `data-files` attribute. No MANIFEST
  entry. No DATA_REQUEST line (the curriculum asks for none). No honest-pending note is needed, because the curriculum's lab
  line names no embedded data (`yaml:1093`); the SIMULATED label is the disclosure.
- If a reviewer later wants a real CCP or payment series, it goes to DATA_REQUESTS with its issuer URL, a quoted licence
  sentence, the licence page and the transform (BUILDER_RULES §6.6, steps 1-5).

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in BK4 |
|---|---|---|---|
| `duffie2011central` | Duffie & Zhu, "Does a Central Clearing Counterparty Reduce Counterparty Risk?", Review of Asset Pricing Studies, volume 1, issue 1, 2011, pages 74-95, DOI 10.1093/rapstu/rar001 (`references/references.json:7411`); `used_by: ["BK4"]`; the curriculum string `yaml:1091` matches | verified (Crossref) | L02 at paper level for the question; the answer only after the abstract is read (B2); reading list |
| `bisndcpmi` | "CPMI publications", Bank for International Settlements, `https://www.bis.org/committees/cpmi/publications`, issuer-verified, index page (`references/references.json:2853`); `used_by: ["BK4"]`; curriculum string `yaml:1090` | verified (issuer, index level) | index-level statements only (for example, the CPMI publishes on payment and market infrastructure). No specific report, no locator. Reading list |
| `bisndbasel` | "Basel III: international regulatory framework for banks", Bank for International Settlements, `https://www.bis.org/committees/bcbs/standards`, issuer-verified (`references/references.json:2815`); `used_by: ["BK1"]` | verified (issuer, index level) | L05, document level only, to name the framework. Not the operational-risk section (not read). Registry `used_by` must gain BK4 at integration (Q12) |

Not cited by BK4: `harris2002trading` (`references/references.json:11536`, used by FC1; a market-microstructure book, not needed
here), `mishkin2021economics` (FC1), `bis2014basel` (SR4), `bis2025triennial` (X1).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "SEC (lead only)", year: "not typed", title: "Securities Exchange Act rule on the standard settlement cycle (T+1), the primary document named in the curriculum (lead only; record not typed)", venue: "U.S. Securities and Exchange Commission (issuer; `sec.gov` allow-listed, `references/authorities.yaml:13`)", needed_for: "L01 and L05 settlement-cycle facts (B1). Until admitted, the settlement period is a lab parameter", confidence: "the curriculum string exists (`yaml:1092`), the review queue names it (`references/review_queue.json:830`), the registry has no record; the planner did not read the rule and types no citation"}
- {doi: null, authors: "Literature on central counterparties and counterparty risk (lead only; no author typed)", year: "not typed", title: "empirical and model evidence on whether a CCP reduces counterparty risk, including the concentration and mutualisation counter-evidence", venue: "not typed", needed_for: "L02 counter-evidence for the B-graded claim (BUILDER_RULES §2.5); the memo's criterion 5", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "CPMI-IOSCO standards for financial market infrastructures (lead only; record not typed)", year: "not typed", title: "the principles for financial market infrastructures, the standard for CCP waterfalls and margin (lead only)", venue: "Bank for International Settlements (issuer; `bis.org` allow-listed, `references/authorities.yaml:22`)", needed_for: "L03 and the project's rule that CCP resources are used in a stated order, if the builder wants a standard cited (otherwise the order is an assumed rule of the model, A1)", confidence: "the lead is a topic only; the planner did not read it and types no record. The architect verifies the title before any admission"}
- {doi: null, authors: "Literature on margin procyclicality (lead only; no author typed)", year: "not typed", title: "evidence on margin requirements rising in stress", venue: "not typed", needed_for: "L03 and the memo's limits criterion (counter-evidence for any claim on margin behaviour in stress)", confidence: "the need is certain; no record is identified"}
- {doi: null, authors: "Literature on stablecoin reserves and redemptions (lead only; no author typed)", year: "not typed", title: "evidence on stablecoin reserve composition and redemption behaviour", venue: "not typed", needed_for: "L04 any observed-behaviour claim; without it, L04 states the derivation only (no empirical claim)", confidence: "the need is certain; no registry key mentions stablecoins (planner grep of `references/references.json`)"}
- {doi: null, authors: "Basel Committee operational-risk standard (lead only; section not read)", year: "not typed", title: "the operational-risk section of the Basel III framework (lead only)", venue: "Bank for International Settlements (issuer)", needed_for: "L05 any statement about the operational-risk standard (a locator needs the section read)", confidence: "a lead within `bisndbasel`; no separate record is identified by this planner"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4).
Until resolved, the lessons teach the models by derivation (grade T, conditional on the stated assumptions), and each empirical
sentence is graded C at most with its basis named, or is removed.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for BK4 (`curriculum/curriculum.json` `atlas` array; no entry names BK4). No
`atlas/BK4.contract.md` is needed, and none is drafted. `check_projects.py` skips the contract check when the project has no
`atlas` key (`tools/check_projects.py:144-146`).

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/BK/BK4/cards.json`, ids `BK4-c001` upward (`tools/check_pages.py` `check_cards` checks the id prefix, the
  lesson existence, the grades and the registry keys). Ids need not be sequential (FINAL-ARCHITECT-RULINGS 2).
- One card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7). Each lesson
  contributes at least one card.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab BK4-L03-1, Derivation 2 (exact)"`.
- Cite a registry key only for an empirical or attributed claim (`duffie2011central` for the question it asks, at paper level).
  `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit BK4            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit BK4
.venv/bin/python tools/check_projects.py --unit BK4
.venv/bin/python tools/run_labs.py --unit BK4               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/BK/BK4/L01.html                             # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/BK/BK4/L02.html --refresh lab-BK4-L02-1     # after editing a twin
.venv/bin/python tools/run_graders.py --unit BK4 --seeds 0-49                                    # grader builder (Builder E)
.venv/bin/ruff check tests/labs/BK4 course/modules/BK/BK4/grader && .venv/bin/ruff format --check tests/labs/BK4 course/modules/BK/BK4/grader
.venv/bin/mypy tests/labs/BK4 course/modules/BK/BK4/grader
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit BK4 --seeds 0-9`,
`.venv/bin/python tools/page_smoke.py --unit BK4` (not run by builders; timing-sensitive), and
`.venv/bin/python tools/verify_refs.py --unit BK4` (the unit ledger's run, VERIFIER §2.1).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`,
`build_site.py --check`, `render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`,
`verify_refs.py --offline`, and the full gate in CLAUDE.md.

Flag checks: `check_pages.py`, `check_dag.py` and `check_projects.py` accept `--unit`; `run_labs.py` accepts `--unit` and
`--page`; `run_graders.py` and `mutate_graders.py` accept `--unit` and `--seeds`; `embed_labs.py` accepts pages and
`--refresh [LAB_ID ...]` (FC1 §11, verified against the tool docstrings at planning time). The planner did not execute the
builder commands; it ran only the coursekit closure and concept-owner functions (§0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on BK4's project (`yaml:1094-1100`) and no Atlas entry names BK4. `check_projects.py`
   skips the contract check (`tools/check_projects.py:144-146`).
2. **No debate.** BK4 has no `debate:` key (`yaml:1071-1100`), so `check_pages.py:412-413` does not require a debate brief.
   Its contested claims (CCP effects, margin procyclicality, stablecoin behaviour) are under the two-sided rule (BUILDER_RULES
   §2.5) anyway.
3. **Both grading.** The spec names "autograder" and "rubric" (`check_projects.py:38`, `:41-49`). The rubric is 5 criteria
   with 4 levels and two exemplars at two levels (`check_projects.py:58-73`).
4. **Rung 2 must be graded instantly.** `check_projects.py` accepts a completion lab or a quiz. The plan uses a completion lab.
5. **One curriculum lab, five lesson labs needed.** The curriculum names one lab (`yaml:1093`); BUILDER_RULES §3.4 requires a
   numerical check per key formula. The plan adds one lab per lesson, plus one more for the stablecoin ratio if the builder
   needs it (the planner's default is one per lesson, §1).
6. **FC1 is built, so the hub may link FC1's hub** (`course/modules/FC/FC1/index.html`). Q14 decides.
7. **check_dag sees linked uses only.** Unlinked uses of D1-D13 (§4) pass the tool. The verifier reads for them.
8. **Labs must be exact.** Standard-library `fractions` and integers, with `-W error` clean under `python -I`.
9. **The hub's hours rules.** `check_pages.py` lesson hours 6-12 (lines 221-228) and the hub split (lines 337-342) are met by §1.
10. **Pyodide.** `run_graders.py` imports numpy at module level (FC1 §8.2 item 1). The BK4 grader and labs are standard-library
    only, so `data-packages=""` is intended. Unverified that the Pyodide runner accepts an empty list. The verifier checks.
11. **BK directory absent.** `course/modules/BK/` does not exist, so the first BK page creates it. `tools/coursekit.py` derives
    the output path from the part code (`Unit.directory`).

---

## 12. Open questions for the architect (numbered; each with the planner's recommended decision)

1. **Lesson count and hours (Q1).** Recommended: 5 lessons × 7 h = 35 h, project 15 h (30 %). Alternative within the rules:
   4 lessons × 9 h = 36 h and a 14 h project (28 %), with L02 holding the curriculum lab and L04 (stablecoins and tokenization)
   plus operational risk. The planner prefers 5 lessons because it keeps two concepts per lesson and gives the project the
   time the autograder needs. **Decision needed before the lesson builders start.**
2. **Builder ownership (Q2, B5).** Recommended: Builder A owns L01, L02 and `index.html`; B owns L03; C owns L04; D owns L05;
   E owns `project.html`, the grader and the project labs; F owns the cards. "About three lessons per builder" is not
   achievable (B5); the architect accepts the 2, 1, 1, 1 split or names another.
3. **DAG: FC2 as a prerequisite (DQ1).** Recommended: no. Variation margin is plain prose in L03. Adding FC2 pulls in AC1, CF1,
   FC2 and M4 (390 h of closure, planner run). Decision needed.
4. **DAG: the plain-prose list (§4, D1-D13).** Recommended: confirm the defaults in §4 (no link, no `data-concept`), and that
   no prerequisite changes. Decision needed for D1 and D7 in particular.
5. **Duffie & Zhu, the abstract (B2).** Recommended: the builder reads the abstract before L02 or the memo cites the paper's
   finding. The planner states no finding. Confirm.
6. **SEC T+1 admission (B1).** Recommended: admit the rule through `tools/add_reference.py` from
   `sec.gov` before L01 and L05 state any settlement fact. Until then, the settlement period is a lab parameter (§2.2). Decision
   needed; it blocks settlement facts only.
7. **Notation: "T+1" and `T`.** Recommended: no bare `T` in math. The settlement lag is `d`. "T+1" appears only as the rule's
   name in prose. Confirm.
8. **Real data (B4).** Recommended: none; all labs and the project use SIMULATED inputs (§6). No DATA_REQUEST. Confirm.
9. **Frozen interface and conventions (§5.2, §5.3).** Recommended: freeze the four functions, the `Waterfall` dataclass, the
   layer order, the remainder rule and the cover rule before building. Precedent: FC1 Q9, E1 Q5/Q6. Decision needed before Builder E.
10. **Hand-computed fixtures (§5.5).** Recommended: permit the hand-computed fixtures (layer order, remainder rule, sizing) in
    `test_project.py` alongside the seed-derived tests. They are stated on the project page and are not seed answers. Confirm.
11. **Lab for L03 and L04 claims.** Recommended: keep the waterfall and cover labs as described. The stablecoin lab (L04) covers
    only the derivation, with no observed-behaviour claim. Confirm the L04 scope.
12. **Registry `used_by` for `bisndbasel` and `bisndcpmi`.** Recommended: the architect runs the registry tool at integration
    so that BK4 appears in `used_by` for each key the module cites. Builders do not edit `references/references.json`. Confirm.
13. **Operational-risk standard (L05).** Recommended: the operational-risk section is not cited until the builder reads it and a
    locator is admitted (§7.2 item 6). Until then L05 defines the term and names the framework at document level. Confirm.
14. **Hub link to FC1 (B6).** Recommended: link the hub to FC1's built hub (`../../FC/FC1/index.html`) and the concept anchors.
    The check that a prerequisite hub link resolves is run at integration. Confirm.
15. **Mutants and alternatives.** Recommended: ten student-error mutants and five alternative correct implementations, as the
    request requires (FINAL-ARCHITECT-RULINGS 9 and 10). Confirm.
16. **Adversarial?** Recommended: no. The project is a simulator and a memo, not an IC defence or debate. No 15-angle question
    bank. Confirm.
17. **Scope.** Recommended scope: one defaulting member at a time, a fixed scenario set, the layer order as an assumed rule, no
    futures, swap or option objects (those are FC2 material), and no real-time or intraday model beyond the L01 lab. Confirm.
18. **Hub placement.** Recommended: `data-mastery="0.8"` (the AC4, M1, E1 and FC1 bar), eight items, at least two `data-skill`
    items testing the worked example's waterfall order and the completion problem's survivor-share line. The others test FC1
    (`clearing-and-settlement`, `trade-lifecycle`) and M1 (`present-value`). Confirm.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 (includes the curriculum lab), L03, L04-L05, project
   (autograder with the ten mutants and five alternatives; rubric and exemplar calibration). Failing rows return to the builder
   that owns the file, with only the failing rows.
3. Ledger at `ledgers/BK4.verification.json`; verifier scripts archived under `ledgers/BK4/scripts/` (VERIFIER §3); mutants
   under `ledgers/BK4/mutants/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B2 must be
   resolved, or named as honest gaps, first.

Architect decisions: pending (§12). This plan is the planner's proposal. Where the architect decides, the decisions are recorded
in an "Architect decisions" block at the end of this file, and the FINAL-ARCHITECT-RULINGS items 1-10 apply unchanged.

## Architect decisions

Pending. No decision has been taken for BK4. Until one is recorded here, the defaults in §12 apply to every builder, except
that the lesson builders do not start before Q1 and Q2 are decided.

## Architect decisions (2026-11-03, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank. plans/FINAL-ARCHITECT-RULINGS.md and ~/.fanout/fixer-rules.md bind every builder. No reference is admitted in this batch: a statement whose source is a REFERENCE_REQUEST is not made, or it is taught as a model result with no attribution.
Module specifics: 5 lessons x 7 h + 15 h project; builders A: L01, L02, index; B: L03; C: L04; D: L05; E: project, grader, project labs; F: cards. FC2 is not added as a prerequisite. The settlement period is a lab parameter, with no statement of the SEC T+1 rule until a record is admitted.
