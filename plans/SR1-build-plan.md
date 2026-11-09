# SR1 build plan: Runs, Liquidity & Fire Sales (planner output, 2026-11-09)

Unit: **SR1 · Runs, Liquidity & Fire Sales** · tier M · 50 h · prerequisites BK1, E4 · no Atlas milestone ·
no debate key · grading `both` (autograder for the solver, rubric for the memo) · output directory
`course/modules/SR/SR1/` (part code `SR`) · lab twins `tests/labs/SR1/` · ledger `ledgers/SR1.verification.json`
(fragments `ledgers/SR1-<slice>.json`, mutants `ledgers/SR1/mutants/`, alternatives `ledgers/SR1/alternatives/`,
equivalents `ledgers/SR1/equivalent/`).

Planner: Haiku, plan only. This file is the only file written. No curriculum, registry, notation, course or git edits,
no commit, no push. Executors: Haiku builders A to E (lessons, hub, project, grader) and F (cards), then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum fact cites `file:line` read during planning. Tool facts cite the tool source or a
coursekit run (run through `.venv/bin/python` with `tools/coursekit.py`). Anything not in the curriculum is marked
**NOT IN CURRICULUM**. The planner read no paper and typed no bibliographic data from memory. Only registry records
(title, authors, container, volume, issue, pages, DOI) were read, not the papers themselves.

**Status: BLOCKING ISSUES EXIST (§0.3).** B1 (the repo concepts that L04 needs are owned by a module outside SR1's
closure), B2 (the direct prerequisite BK1 is neither built nor planned), and B3 (no redistributable data for the
project's 2023 calibration) need an architect decision before the owning builders start. The hours are feasible (§0.2).

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part SR, code `SR`, order 21, title "Systemic Risk & Financial Stability" | `curriculum/05-macro-alternatives.yaml:417-419` |
| SR1 block: id, title "Runs, Liquidity & Fire Sales" | `curriculum/05-macro-alternatives.yaml:433-434` |
| Tier `M` | `curriculum/05-macro-alternatives.yaml:435` |
| Hours `50` | `curriculum/05-macro-alternatives.yaml:436` |
| Prereqs `[BK1, E4]` (only) | `curriculum/05-macro-alternatives.yaml:437` |
| Core: "Bank runs, liquidity spirals, fire sales, the run on repo." | `curriculum/05-macro-alternatives.yaml:438` |
| `introduces` has **6** concepts: `diamond-dybvig-model`, `bank-run`, `uninsured-deposit-run`, `liquidity-spiral` ("Loss and margin spirals"), `fire-sale`, `run-on-repo` | `curriculum/05-macro-alternatives.yaml:439-445` |
| Sources: four strings (Diamond & Dybvig (1983), JPE 91(3); Brunnermeier & Pedersen (2009), RFS 22(6); Shleifer & Vishny (2011), JEP 25(1); Gorton & Metrick (2012), JFE 104(3)) | `curriculum/05-macro-alternatives.yaml:446-450` |
| Lab: "Margin-spiral simulator." (the curriculum lab) | `curriculum/05-macro-alternatives.yaml:451` |
| Project "Run dynamics model"; brief: "Extend Diamond–Dybvig with uninsured-depositor information, and calibrate the run threshold to the 2023 regional-bank episode."; deliverable "Model plus memo."; grading `both` | `curriculum/05-macro-alternatives.yaml:452-458` (title 453, brief 454-456, deliverable 457, grading 458) |
| No `debate:` key and no `atlas:` key on SR1 | `curriculum/05-macro-alternatives.yaml:433-458` (absent) |
| JSON row for SR1 matches the YAML (hours 50, prereqs BK1 and E4, six concepts, grading both) | `curriculum/curriculum.json:11161` (`"id": "SR1"`) |
| No Atlas entry names SR1. The SR Atlas milestone is A19 (SR3, `curriculum/05-macro-alternatives.yaml:500-504`); A20 is GM4 (`curriculum/05-macro-alternatives.yaml:377-384`) | `curriculum/curriculum.json` `atlas` array (planner check) |
| The six SR1 concepts all map to module SR1 | `curriculum/curriculum.json` `concepts` (planner check with `coursekit.concept_owner()`) |
| Downstream: GM5 requires SR1 | `curriculum/05-macro-alternatives.yaml:389` (`prereqs: [GM4, SR1]`) |
| Downstream: SR2 requires SR1 and AP6 | `curriculum/05-macro-alternatives.yaml:463` |
| Downstream: SR3 requires SR1 and PR4 | `curriculum/05-macro-alternatives.yaml:486` |
| Downstream: SR4 requires SR1, FI4 and LX2 | `curriculum/05-macro-alternatives.yaml:509` |
| Studio STUDIO-SR requires SR3 (not SR1) | `curriculum/05-macro-alternatives.yaml:421-423` |
| SR1 is a requirement of the PhD credential | `curriculum/meta.yaml:124` (PHD-FIN `requires`) |
| SR1 sits in the field course "Intermediation & Macro-Finance" with AP6 and SR2 | `curriculum/meta.yaml:134` |
| Prerequisite closure of SR1 (run by the planner with `coursekit.prerequisite_closure("SR1")`): **{AC1, BK1, CF1, E1, E2, E3, E4, FC1, FI1, M1, M2, M3, M4, M7, P0.1}** | planner run output |
| Topological position of SR1: index **49** (0-based) | `curriculum/curriculum.json:1036` (`topological_order`), read through `coursekit` (planner run) |
| BK1 (direct prerequisite, in the closure): tier `U`, hours `90`, prereqs `[FC1, FI1, AC1]`; introduces `delegated-monitoring`, `maturity-transformation`, `deposit-franchise` | `curriculum/02-economics-finance-core.yaml:978-994` (hours 981, prereqs 982, introduces 987-994); `curriculum/curriculum.json:8423` |
| BK1 is **not built**: `course/modules/BK/` contains only `BK4`; BK1 has no plan file | `ls course/modules/BK` (planner run); `plans/` has no `BK1-build-plan.md` |
| The `concepts.html` anchors of BK1 concepts exist but show "not yet released" | `course/concepts.html:559` (`maturity-transformation` · "not yet released") |
| FI4 (owner of `repurchase-agreement` and `repo-haircut`) is outside the SR1 closure and not built; its prereqs are `[FI1, E5]` | `curriculum/03-markets.yaml:121-130` (id 121, prereqs 125, `introduces` 129; `repurchase-agreement` at 130, `repo-haircut` at 131); `FI4` is not in `coursekit.built_units()` |
| FI4 is topologically before SR1 and its closure does not contain SR1 (so adding FI4 to SR1's prereqs creates no cycle) | `coursekit`: `prerequisite_closure("FI4")` = {AC1, CF1, E1, E5, FI1, M1, M2, P0.1}; FI4 topo index 33 (`plans/FI4-build-plan.md:41`) |
| LX1 (owner of `lender-of-last-resort` and `financial-panic`) is built, outside the closure | `coursekit.built_units()` includes LX1; `coursekit.concept_owner()` |
| Nearest built direct prerequisite: **E4** (built; `course/modules/E/E4/` exists); the E4 plan is `plans/E4-build-plan.md` | `curriculum/02-economics-finance-core.yaml:124-128` (E4 id, prereqs `[E2, E3, M7]`); `course/modules/E/` listing |
| Built units that already use SR1 concepts in plain prose (no link, so no DAG tool failure) | `plans/LX1-build-plan.md:309-310` (`bank-run`, `fire-sale` as plain prose); `plans/BK4-build-plan.md:368`; `plans/FI4-build-plan.md:270` |
| No existing page links an SR1 concept or defines one (`data-concept="bank-run"` etc. absent) | `grep` over `course/modules` (planner run, no matches) |
| Notation registry: macros `\E` `\Prob` `\Var` `\Cov` `\Corr` `\R` `\N` `\indic` `\Normal` `\iid` `\dto` `\pto` `\argmax` `\argmin` `\tr` `\diag` and the M-tier macros | `notation/notation.json:5-108` |
| Registered symbols SR1 must not reuse: `T` (S1), `\Phi` (M4), `\gamma_3`, `\gamma_4` (M4), `R^\ast`, `R^{e\ast}`, `R_f` (AP1), `\mathbb{Q}` (AP1) | `notation/notation.json:111-150` (`T` 111-115; `\Phi` 116-120; `\gamma_3` and `\gamma_4` 121-130; `R^\ast` 131-135; `R^{e\ast}` 136-140; `R_f` 141-145; `\mathbb{Q}` 146-150) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 50 h (`curriculum/05-macro-alternatives.yaml:436`). The tool rules:

- lesson `data-hours` 6 to 12 (`tools/check_pages.py` `check_lesson`, about lines 219-228);
- hub `data-hours-lessons + data-hours-project = 50` (`tools/check_pages.py` `check_hub`, about lines 325-342);
- project share 10 to 40% of 50, i.e. 5 to 20 h (BUILDER_RULES §4.3, `BUILDER_RULES.md:168-173`);
- lessons sum to the hub's lessons figure (`check_pages.py` `check_hub`).

**Chosen split: 4 lessons × 9 h = 36 h; project 14 h (28%).** 36 + 14 = 50. Feasible. **No STOP condition on hours.**
The alternative in §12 Q1 (5 × 8 h and a 10 h project) is also feasible.

### 0.3 Blocking issues (architect decision required before the owning builders start)

**B1. The repo concepts that L04 teaches are owned by FI4, which is outside SR1's closure.**
- SR1's core names "the run on repo" (`yaml:438`). The concepts `repurchase-agreement` and `repo-haircut` are owned by
  FI4 (`curriculum/03-markets.yaml:130-131`). FI4 is not in SR1's closure (§0.1).
- The architect defaults (plans/E4-build-plan.md, "Architect decisions", and the E5 precedent) say "concepts outside the
  closure are plain prose with no link and no dfn". Under that default L04 would use "repo" and "haircut" without
  defining them, which breaks BUILDER_RULES §1.10 and §8 ("Define before use").
- **Plan's default (for the architect to confirm or replace):** add FI4 to SR1's prerequisites (a curriculum change at
  `curriculum/05-macro-alternatives.yaml:437` and in `curriculum/curriculum.json`). The coursekit check shows no cycle
  (§0.1). Builders do not edit `curriculum/*.yaml`. Until the change is made, L04 uses the plain-sentence rule of §4 D1-D2.

**B2. The direct prerequisite BK1 is neither built nor planned.**
- BK1 is a direct prerequisite (`yaml:437`) and sits in the closure (§0.1). `course/modules/BK/` holds only BK4, and
  `plans/` has no BK1 plan.
- BK1 is topologically earlier than SR1 (index 31 against 49; `plans/BK4-build-plan.md:45` and the coursekit run). The
  fan-out order therefore places BK1 first.
- The concepts SR1 would link from BK1 (`delegated-monitoring`, `maturity-transformation`, `deposit-franchise`) show
  "not yet released" on `course/concepts.html:559` until BK1 is built. A link would land on that stub.
- **Plan's default:** SR1 builders wait until BK1 is built and its concepts are released. The architect may instead let
  SR1 proceed with plain prose for the three BK1 concepts (§4 D15 lists them as linkable only after BK1 exists).

**B3. No redistributable data exists for the project's 2023 calibration.**
- The brief asks to "calibrate the run threshold to the 2023 regional-bank episode" (`yaml:455-456`). The data an honest
  calibration needs are uninsured-deposit shares and deposit outflows. The planner found none in the embedded data.
- Embedded data: `fx_daily`, `fx_monthly` and `ust_daily` only (`tools/data_sources.yaml:19`, `:53`, `:91`). No deposit,
  bank-balance-sheet or repo series. `rejected:` begins at `tools/data_sources.yaml:119`, and it does not list any bank
  data.
- Candidate sources are named in BLUEPRINT §5.3 (`BLUEPRINT.md:310-317`, including FFIEC call reports), but none is
  checked for this unit. The planner did not read any issuer's terms and does not name a licence from memory.
- The Federal Reserve's own SVB review is in the registry as `frb2023fed` (`references/references.json:9107`, primary,
  issuer URL). The planner did not read it. A figure from it may be quoted with a locator only after the builder reads
  the page (BUILDER_RULES §1.2(b)). Embedding its numbers as a dataset is not permitted without a verified reuse
  statement.
- **Plan's default:** the calibration target is a SIMULATED target with an honest-pending note on the project page and a
  DATA_REQUEST (§6). The architect may instead approve quoting one figure from `frb2023fed` once it is read.

Non-blocking, but the architect should see them:

- **B4. Brunnermeier–Pedersen year.** The curriculum says "(2009)" (`yaml:448`). The registry record
  `brunnermeier2008market` (`references/references.json:4106`) has a `year` field of 2008 and a `print_year` of 2009
  (`years: [2008, 2009]`). Cite the key only, with no year typed in prose (§5, §7). The architect decides whether a
  registry note is needed.
- **B5. "About three lessons per builder" is not feasible.** The brief's fan-out asks for about three lessons per builder.
  Five builders at three lessons each would need about 15 lessons, which at the 6 h minimum is 90 h. The lesson budget is
  36 h, so the split is one lesson per builder (§1, §12 Q2).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

4 lessons × 9 h = 36 h; project 14 h; total 50 h. The six concepts map to the four lessons so that each concept is defined
in exactly one lesson (`yaml:439-445`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `yaml:439-445`) | Lab twin id (`tests/labs/SR1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Deposit contracts and the bank run | `diamond-dybvig-model` (`yaml:440`), `bank-run` (`yaml:441`) | `lab-SR1-L01-1`: the two-date Diamond–Dybvig payoffs with sequential service for three depositors, in `Fraction`; every pure profile checked for Nash equilibrium; a finite enumeration (grade C, basis named) | 9 | Builder A |
| L02 | Uninsured depositors and the run decision | `uninsured-deposit-run` (`yaml:442`) | `lab-SR1-L02-1`: the run condition for an uninsured depositor on an exact grid of uninsured shares and liquidation values, in `Fraction`; no SIMULATED data | 9 | Builder B |
| L03 | Loss spirals and fire sales | `liquidity-spiral` (`yaml:443`), `fire-sale` (`yaml:444`) | `lab-SR1-L03-1` (**the curriculum lab**, `yaml:451`): margin-spiral simulator, a deterministic price–margin map iterated from a stated start, both convergent and divergent regimes; the closed-form fixed point printed beside the iterates; labelled **SIMULATED** | 9 | Builder C |
| L04 | The run on repo | `run-on-repo` (`yaml:445`) | `lab-SR1-L04-1`: the collateral haircut ladder under falling collateral prices, the minimum haircut at which the lender is covered, in `Fraction`; closed form, not SIMULATED | 9 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours 36/14 | none | none | – | Builder A (writes after L01 exists; the integrator fixes the lesson titles at the end, §13) |
| project | Run dynamics model (`both`, §5) | none | `lab-SR1-project-1` (rung 1), `lab-SR1-project-2` (rung 2, `class="lab completion"`), `lab-SR1-project-3` (rung 3 check) | 14 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | – | Builder E |
| cards | `cards.json` from L01 to L04 | none | none | – | Builder F (after A to E) |

**Ownership rule.** Each builder writes only its own lesson page and twins. Builder A writes the hub after L01 exists.
Builder E writes the project, its rubric, exemplars and grader, and does not depend on the lessons' prose. Builder F
writes only `cards.json`. No builder edits `curriculum/`, `references/`, `notation/`, `course/index.html` or
`course/concepts.html`.

Ordering check (every use of a concept is inside the closure or an earlier lesson of SR1; `check_dag.py` checks linked
uses, §4 covers unlinked ones):
- L01 uses E2 `nash-equilibrium` (the withdrawal game), E3 `expected-utility` (only if an expected-payoff comparison is
  written), BK1 `maturity-transformation` and `delegated-monitoring` (linked only after BK1 exists, B2).
- L02 uses L01 `bank-run` and `diamond-dybvig-model`, and M4 `random-variable` for the depositor's belief.
- L03 uses L01 `bank-run`, L02 `uninsured-deposit-run` (only in prose), M2 `finite-difference-derivative` (the spiral's
  slope check), M3 `linear-map` (the affine price–margin map).
- L04 uses L03 `fire-sale` and `liquidity-spiral`, FI4 `repurchase-agreement` and `repo-haircut` (B1), M1 `present-value`
  only if a haircut is discounted.

Hours check: 4 × 9 = 36 (hub `data-hours-lessons="36"`); project 14 (hub `data-hours-project="14"`); total 50.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to SR1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `VERIFIER_RULES.md` §2, `plans/FINAL-ARCHITECT-RULINGS.md`,
`/Users/billyribeiro/.fanout/fixer-rules.md`, this file, and `plans/E4-build-plan.md` (the nearest built prerequisite's plan,
whose precedents this plan adopts). Study `course/modules/E/E4/` (hub, lessons, project, grader panel, rubric) and
`course/modules/M/M1/` for layout. `course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier unit)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded
   only at display, with the rule stated (fixer-rules: recompute from unrounded values; E4 §2.1 item 1). For SR1 this covers every threshold, haircut,
   fraction and iterate.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Every "checked", "verified" or "shown" claim names the lab, line or test (fixer-rules: lab statements match code and output).
3. **Attribute nothing unread.** Cite only the registry keys in §7.1, and only at paper level unless the builder has read the
   abstract (VERIFIER §2.1). No page, table, equation, coefficient or year is typed unless read. The planner did not read
   the four papers; the builder reads each abstract before naming its claim (fixer-rules: attribute nothing unread).
4. **Scope words need a computation, a witness or an explicit hypothesis.** "every", "all", "never", "always", "any", "only",
   "same", "drives", "exactly", "market structures", "systemic", "runs always" are used only where a derivation, a finite check
   or a lab computes the claim (fixer-rules: scope words). SR1 scope (confirm, §12 Q7): one bank or one fund at a time; two or three
   dates; finite depositor sets in the labs; one risky asset and one collateral class in the project; no general-equilibrium
   spillovers; no policy response except where the lesson defines a lender of last resort; no claim that runs are
   empirically self-fulfilling.
5. **Define before use.** Each of the six concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Terms outside the six (deposit insurance, the insured and uninsured depositor, the liquid
   buffer, the haircut, the margin call, the fire-sale discount, the sequential-service rule, common knowledge, the run
   threshold) are defined in the sentence where first used, as plain prose, with a plain `<dfn>` and no `data-concept` (or
   no `<dfn>`), per §4.
6. **Propositions state every hypothesis, numbered.** Every Theorem, Proposition and Derivation block lists numbered
   Assumptions (A1, A2, ...) before the statement, and its proof cites them. Examples the builders must state: the payoff
   ordering that makes early withdrawal a best response to a run (L01); the finite depositor set and the sequential-service
   rule (L01, L02); the monotone map and the slope condition of the spiral (L03); the strictly positive collateral value and
   the haircut's range (L04).
7. **Grader rule.** Applies to the project grader (§5.5). A test may demand an exception only for a condition the page names.
   The page names three conditions (§5.5). Every other invalid input may raise any exception or return (fixer-rules: project graders).
8. **Money.** The model is normalised: deposits equal one unit, and every output is a dimensionless fraction or threshold.
   If the builder introduces a currency amount, it is integer cents, rounded once, half up, and stated on the page (fixer-rules: money is integer cents). The planner recommends the normalised form.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; no element widens the page past 360 px. `page_smoke.py` is the verifier's check; builders do not run it.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network
    (`tools/run_labs.py`, E5 §2.1 item 10).
11. **Lab hypotheses before runs.** Each lab's `p.hypothesis` states the expected result before the expected-output block is
    embedded. Every RNG is seeded with `random.Random(seed)`. The standard library only (`fractions`, `math`, `random`,
    `itertools`); no NumPy or SciPy in labs; under 10 s in Pyodide.
12. **Iteration and bisection are stated, not assumed.** A lab or the solver that iterates or bisects states its start, bracket,
    tolerance, stop rule and convergence or sign-change assumption. The printed residual at the reported point is the evidence
    (E4 §2.1 item 12).
13. **Graded-instantly completion problem.** The rung-2 completion lab (`class="lab completion"`) shows `___` blanks. Every page
    line equals its twin line or contains a blank (`tools/run_labs.py` completion rule).
14. **Architect rulings apply.** Ruling 1: use the macro `\R`, never `\mathbb{R}`. Ruling 2: card ids need not be sequential.
    Ruling 9: a mutant that survives and violates a stated behaviour gets a new test; a mutant that differs only where the page
    states nothing goes to `ledgers/SR1/equivalent/` with a README proof. Ruling 10: five correct alternatives must pass seeds
    0 to 49 (§5.6). Ruling 13: a worked value derived by hand in a numbered Example is graded T with the Example as basis; a
    value only a lab prints is graded C naming the lab. Ruling 14: the honest-pending definition rule applies to any concept
    waiting for a source. HOURS ruling: declared hours are design targets; do not change them to match an estimate.
    LAB MUTANTS ruling: lab twins are demonstrations; mutation testing applies to the project grader only.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- **Evidence.** Every claim carries a grade (T, A, B, C, D or X, BLUEPRINT §3) and a registry key or a derivation. A B- or
  C-graded claim names its published counter-evidence (BUILDER_RULES §2.5). The run mechanisms are contested; the two-sided rule
  applies even though SR1 has no debate key. **No registry record establishes an empirical claim about runs, fire sales or
  repo runs that this plan has checked.** Such claims are C at most, with the basis named, or go to §7.2.
- **Concept links.** Closure concepts (AC1, BK1, CF1, E1 to E4, FC1, FI1, M1 to M4, M7, P0.1):
  `<a class="concept" data-concept="<id>" href="../../../concepts.html#<id>">`. Earlier SR1 lessons: `href="Lnn.html#def-<id>"`.
  A lesson never links a concept defined in a later lesson. There is no link to a BK1, E2 or E4 hub page (BUILDER_RULES §4.1).
  BK1 concepts link only after B2 is resolved. FI4 concepts link only if B1 adds FI4 to the prerequisites.
- **Labs.** Code lives once in `tests/labs/SR1/lab-SR1-Lnn-1.py` (and `lab-SR1-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match
  `lab-SR1-<page>-<n>` (`tools/check_pages.py:258`). Lab ids are numbered in display order.
- **SIMULATED label.** Required on any lab, figure or grader instance that uses generated data or seeded draws: the L03
  curriculum lab, the rung-1 and rung-2 project instances, `instance.py`, the calibration target, and the exemplars. Exact
  closed-form and finite checks (L01 enumeration, L02, L04) are not labelled SIMULATED.
- **Never hand-edit generated files**: `CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`. Request changes in the output contract.
- **Learner-visible text.** No process words in the page (build, builder, round, verifier, REQUESTS, unit report) and no planning
  references in code comments (E3 §2.2 precedent).
- **Banned strings** (`tools/check_pages.py` `BANNED`, about lines 58-73): TODO, TBD, lorem, "for brevity", "details omitted",
  "beyond the scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree",
  "it is well known", "obviously", "clearly", and any ellipsis `...` outside code.
- **Percent changes** state the base and the direction. **Rates** (repo rates, haircuts, interest) state the unit, the
  compounding and the day-count basis. **Growth or return rates** state their convention.
- **A finite enumeration is grade C with its basis named**, not grade T (M1 L06 precedent). Used in L01 and in the project's
  instance guard.
- **Hub lesson titles** match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent). **Quiz explanations** are read against
  their lesson (CF1 KNOWN 6 precedent).
- **No `git commit`, no push.** The builder reports files written, commands run with exact output, and every gap in the
  BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered items that SR1 must use or must not reuse:

| Registered item | Registered meaning (locator) | SR1 rule |
|---|---|---|
| `\E` (macro) | expectation operator (`notation.json:5-8`) | Use the macro for every expectation. Never write raw `\mathbb{E}`. |
| `\Prob` (macro) | probability measure (`notation.json:9-12`) | Use the macro for every probability. Never write raw `\mathbb{P}`. |
| `\Var`, `\Cov`, `\Corr` (macros) | variance, covariance, correlation (`notation.json:13-24`) | Use the macros if used. |
| `\R` (macro) | real numbers (`notation.json:25-28`) | **Use `\R` (architect ruling 1).** |
| `\Normal` (macro) | normal distribution (`notation.json:37-40`) | Use for every normal law if one is used. |
| `\indic` (macro) | indicator function (`notation.json:33-36`) | Use for indicators of depositor types or states. |
| `T` | number of return observations (`notation.json:111-115`, S1) | **Never used.** Dates are `t = 0, 1, 2`; horizons are `H`. Tax-like totals are not used. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (`notation.json:116-120`, M4) | **Not used.** |
| `\gamma_3`, `\gamma_4` | skewness and kurtosis (`notation.json:121-130`, M4) | **Not used.** Plain `\gamma` is not used either. |
| `R^\ast`, `R^{e\ast}`, `R_f` | SDF return, projection of 1, gross riskless return (`notation.json:131-145`, AP1) | **Not used.** No bare `R` for a gross return either, to avoid a visual clash with `R^\ast`. |
| `\mathbb{Q}` | equivalent martingale measure (`notation.json:146-150`, AP1) | **Not used.** Do not write `Q` for a measure. |

Local symbols (allowed; each defined on the lesson where it first appears and never redefined): `t` the date (0, 1, 2);
`lambda` the early-withdrawal share (the fraction of impatient depositors); `mu` the uninsured share of deposits;
`theta` the bank's fundamental (asset quality, on a stated scale); `kappa` the liquidation value per unit of the long asset
(in `(0, 1]`, §5.2); `ell` the liquid buffer (in `(0, 1)`); `x` a withdrawal fraction; `s` a margin or collateral value;
`h` a haircut. A symbol with a registered meaning above is never reused with another meaning.

NOTATION_REQUESTS: **none.** The plan needs no new macro. The builder uses only the local symbols above and the registered
macros.

---

## 3. Lesson content plan (what each lesson must establish; the builder decides the argument)

For each lesson the builder writes the BUILDER_RULES §4.2 structure in order: why it matters (at most 120 words), numbered core
sections of Definition, Theorem, Proof, Example and Remark blocks, the inline lab (before "where the canon breaks"), where the
canon breaks (at least one model limit and what changes without it), misconceptions (at least 3), a problem set (at least 3 each
in Mechanics, Proof, Empirical and Research, each with a `<details class="solution">` of at least 15 words), a key-results table
(claim, grade, keys), a quiz (8 to 15 items, each with an explanation), and references (`<ol data-references>` of registry keys).
**No debate brief**: SR1 has no `debate` key (`yaml:433-458`).

- **L01 `diamond-dybvig-model`, `bank-run`.** Three dates, one bank, a deposit contract that pays one unit to an early
  withdrawer at `t = 1` and a return to a late withdrawer at `t = 2`, a long asset that is illiquid at `t = 1`, and sequential
  service. Each depositor's payoff depends on the withdrawal fraction (definition). Early withdrawal is a best response when
  enough others withdraw early (Proposition with Assumptions A1 to A3; grade T conditional on them). The run and the no-run
  profile are both pure Nash equilibria in the stated parameter region (E2 `nash-equilibrium`). The lab enumerates the profiles
  of three depositors exactly (grade C, finite enumeration). The lesson states the sunspot reading of a run as a model
  property, not an empirical one. The fundamentals reading is named as the contrast and is not claimed (§7.2 R-SR1-1).
- **L02 `uninsured-deposit-run`.** Deposit insurance covers an insured share of deposits and not the rest (definition, plain
  prose: the insurance limit is a stated parameter, not a fact about any country). Uninsured depositors face the full loss and
  are modelled to withdraw when the bank's liquid buffer, net of the liquidation discount, cannot cover the uninsured claims that
  are due (definition of the run condition, Assumption A1 on the buffer and A2 on the liquidation value `kappa`). The lab
  computes the run condition on an exact grid (T on the stated model; the grid is a finite check, grade C). The lesson's
  "where the canon breaks": a fixed insurance limit, no information about the bank's assets, and no policy response.
  Counter-evidence for B or C claims is required before any empirical sentence is kept (§7.2 R-SR1-4; `jiang2024monetary`
  candidate, §7.1, Q10).
- **L03 `liquidity-spiral`, `fire-sale`.** A forced sale at a discount lowers the price, which raises the margin requirement,
  which forces further sales (definition; Assumption A1 on the affine map and A2 on the slope below one for convergence). The
  curriculum lab (`yaml:451`) iterates the affine map from a stated start and prints the iterates beside the closed-form fixed
  point, in both regimes; the lab is labelled **SIMULATED** (it is a model simulation). The fire-sale discount is defined in
  prose (no concept link). The lesson states that the spiral's empirical size is not claimed (§7.2 R-SR1-3). Shleifer and
  Vishny (paper level, after the abstract is read) and Brunnermeier and Pedersen (paper level, after the abstract is read) are
  the attribution sources for the mechanisms; no page, table or coefficient is typed from them. The price-impact term is plain
  prose; no MS1 or MS3 concept is linked.
- **L04 `run-on-repo`.** A repurchase agreement lends cash against collateral with a haircut. Under falling collateral values
  the lender's required haircut rises, and the borrower can be unable to roll the funding (definition; FI4
  `repurchase-agreement` and `repo-haircut` per B1, otherwise plain sentences). The lab computes the minimum haircut at which the
  lender is covered under a stated price path, exactly (T for the stated model; the path is a finite check). Gorton and Metrick
  (paper level, after the abstract is read) are the attribution for the run on repo. The lesson's limits: one collateral class,
  no central-clearing margin, no dealer balance-sheet constraint (plain prose, §4 D3).

Lesson-level constraints: no lesson uses a term from SR2 (leverage cycle, procyclical leverage, collateral equilibrium), SR3
(CoVaR, MES, network contagion) or SR4 (Volcker, central clearing mandate). Those are outside SR1 and later in the topological
order (§4 D11-D12). The word "contagion" is not used as a concept.

---

## 4. DAG problems (concepts that natural SR1 content would use outside the closure)

Closure of SR1 (computed, §0.1): {AC1, BK1, CF1, E1, E2, E3, E4, FC1, FI1, M1, M2, M3, M4, M7, P0.1}. Owners below are from
`curriculum/curriculum.json` `concepts` (planner check).

| Ref | Concept or term | Owner (outside closure) | Where natural SR1 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `repurchase-agreement` (FI4; `curriculum/03-markets.yaml:130`) | FI4 | the run on repo (L04) | **B1.** Default if B1 is not resolved: a plain sentence defining repo at first use ("a sale of collateral with an agreement to buy it back"), no `<dfn>`, no link. If B1 adds FI4: link `../../../concepts.html#repurchase-agreement`. |
| D2 | `repo-haircut` (FI4; `curriculum/03-markets.yaml:131`) | FI4 | the lender's margin and the lab (L04) | As D1. |
| D3 | `dealer-balance-sheet-constraint` (FI4; `curriculum/03-markets.yaml:136`) | FI4 | dealers as forced sellers (L03, optional) | Not used unless needed; if used, a plain sentence, no link. |
| D4 | `lender-of-last-resort`, `financial-panic` (LX1; built, not in closure) | LX1 | the policy backstop of a run (L01, L04) | Plain sentence at first use stating the meaning in the sentence; no `<dfn>`, no link. Not a DAG defect (LX1 is built and does not link SR1). |
| D5 | `margin-cover`, `ccp-default-waterfall` (BK4; built, not in closure) | BK4 | central-clearing margin in repo runs (L04, optional) | Not used unless needed; plain sentence if used. |
| D6 | `futures-margining` (FC2; built, not in closure) | FC2 | variation margin in the spiral (L03) | Plain sentence if used; no link. |
| D7 | `slow-moving-capital`, `intermediary-asset-pricing` (AP6; not built) | AP6 | intermediaries as the marginal sellers in a fire sale (L03) | Not used by default. If used, plain sentence. |
| D8 | `value-at-risk`, `stress-testing` (PR4; not built) | PR4 | margin setting (L03) | Not used. |
| D9 | `banking-crisis` (E9; not built, later) | E9 | aggregate framing (L01, L04) | Not used by default. |
| D10 | `ldi-collateral-spiral` (BK3; not built) | BK3 | an example of a collateral spiral (L03) | Not used by default. A plain example sentence is allowed if B3 is resolved in its favour. |
| D11 | `leverage-cycle`, `procyclical-leverage`, `collateral-equilibrium` (SR2; later) | SR2 | none | **Forbidden in SR1.** A use would be a DAG defect because SR2 requires SR1 (`yaml:463`). |
| D12 | `covar`, `marginal-expected-shortfall`, `network-contagion` (SR3; later) | SR3 | none | **Forbidden in SR1** (SR3 requires SR1, `yaml:486`). |
| D13 | `stablecoin-reserve-run` (X4; outside the closure) | X4 | none | Not used. |
| D14 | Deposit insurance; the sequential-service rule; the run threshold; common knowledge; global games or threshold equilibria with private information; the fire-sale discount; price impact (no concept id in `concepts`) | none | L01 to L03 | Plain sentence at first use, no `<dfn>`, no link. Global games and private-information threshold equilibria are **not** used in SR1 (R-SR1-2 is lead only). |
| D15 | Concepts in the closure that SR1 may link: E2 `nash-equilibrium`, `bayesian-nash-equilibrium`, `signaling`; E1 `competitive-equilibrium`; E3 `expected-utility`; BK1 `delegated-monitoring`, `maturity-transformation`, `deposit-franchise` (linkable only after B2); FC1 `financial-intermediary`, `clearing-and-settlement`, `market-maker`; M1 `present-value`, `discount-factor`; M2 `finite-difference-derivative`; M3 `linear-map`; M4 `expectation`, `random-variable`, `normal-distribution`; M7 `kkt-conditions`, `lagrange-multiplier` | in closure | as noted | Link via `concepts.html#<id>` as in §2.2. Not DAG issues. |

Each row has a resolution, so no DAG_DEFECT blocks the build **except B1 and B2, which the architect must decide**. Each row
needs the architect's confirmation (§12 Q3, Q4, Q5). `check_dag.py` checks linked uses only (`tools/check_dag.py` docstring);
an unlinked use of D1 to D14 passes the tool, so the verifier reads every lesson and the project for these names
(VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): ladder, spec, model, grader, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py` requires the order, line 4-5 and 85-90)

1. **Rung 1, worked example** (`lab-SR1-project-1`, SIMULATED instance): one fully solved, annotated run of the solver on one
   generated instance, with a "why" note on each step: the run condition, the bracket, the root search, the residual, the
   calibration step. From tier M upward, rungs 1 and 2 are kept to the minimum (BUILDER_RULES §5.1).
2. **Rung 2, completion** (`lab-SR1-project-2`, `class="lab completion"`, SIMULATED instance): the residual-check line of the
   root search is removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the twin line or
   contains a blank (`tools/check_projects.py` requires a completion lab or a quiz, lines 85-90).
3. **Rung 3, independent project (graded):** (a) the autograded solver `solver.py` and the calibration function to the §5.2
   interface, and (b) the memo `memo.md`, rubric-graded (§5.6). `lab-SR1-project-3` is the rung-3 check: it calls the solver on
   the reference case and prints the run threshold and the calibrated buffer for the calibration target the memo must use.
4. **Rung 4, stretch** (optional, not graded): a second collateral class in the repo model, or the comparison of a fundamental
   threshold with a sunspot run region, with the comparison stated as a hypothesis before it is run.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py` requires the terms and the grading words, lines 34 and 38-49)

Terms: Context (2 to 4 sentences), Inputs, Required outputs, Constraints, Grading, Reading list.

- **Context.** A bank funds long-term assets with uninsured and insured deposits. In the 2023 regional-bank episode, uninsured
  depositors withdrew quickly. The question is how large the run threshold is for a given uninsured share and liquidation value,
  and what the threshold implies for the 2023 calibration target.
- **Inputs.** No dataset is embedded (§6). The instance supplies the uninsured share `mu`, the liquidation value `kappa` and the
  liquid buffer `ell`. The calibration target `target_threshold` is supplied by the instance or by the student (§6, B3).
- **Model (planner proposal, §12 Q8; the planner has not derived any equation).** Three dates, one bank, deposits normalised to
  one unit, a fraction `mu` of deposits uninsured. The bank holds a liquid buffer `ell` and a long asset whose value at `t = 2`
  depends on a public fundamental `theta` on a stated scale. Uninsured depositors observe `theta` and withdraw early when the
  buffer, after liquidating the long asset at the discount `kappa`, cannot cover the uninsured claims. The run threshold is the
  fundamental level at which the uninsured run condition holds with equality. The builder derives the equation, its uniqueness
  (or the stated selection rule) and the monotone dependence on `mu`; the verifier re-derives them. **The planner has not
  derived any equation of this model.** No registry key is cited for the model until §7.2 is resolved.
- **Required outputs.**
  - `solver.py` with the frozen interface below.
  - `memo.md` with the sections named in the rubric (§5.6).
  - Frozen interface (§12 Q9):
    - `solve_model(uninsured_share: float, liquidation_value: float, liquid_buffer: float) -> dict[str, float]`, returning exactly
      the keys `run_threshold` (the fundamental threshold, in `[0, 1]`; `0.0` when `uninsured_share == 0`, the convention the
      page states) and `run_fraction` (the fraction of uninsured deposits that withdraw early at the threshold, in `[0, 1]`).
    - `calibrate_buffer(target_threshold: float, uninsured_share: float, liquidation_value: float) -> float`, returning a liquid
      buffer in `(0, 1)` whose `run_threshold` equals `target_threshold` to `1e-8`.
- **Constraints.**
  - Floats at full precision inside the solver; the memo displays a stated number of significant digits and states the rule.
  - Valid input and the exception table (§5.5); no other exception type is required.
  - Standard library only; no network; the same code runs in Pyodide and under pytest.
  - The solver's tolerance and its root-search bracket are documented constants on the page, not arguments of the interface.
- **Grading.** Autograder (`grader/test_project.py`, dual-mode) for `solver.py` and `calibrate_buffer`; rubric (`rubric-memo`,
  §5.6) for the memo. The spec names both "autograder" and "rubric" (`tools/check_projects.py` `GRADING_WORDS`, line 38).
- **Reading list.** `ol.reading-list` cites `diamond1983bank`, `brunnermeier2008market`, `shleifer2011fire` and
  `gorton2012securitized` (registry keys only, §7.1). Candidate keys (§7.1) are added only after the architect approves them.

### 5.3 Time budget (`<table id="hours">`, sums to 14 h; every row has a one-line rationale; `tools/check_projects.py` lines 107-118)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved SIMULATED instance, annotated line by line (tier M keeps rung 1 minimal) |
| Rung 2, completion problem | 1 | Fill the residual-check line, then run the instant check |
| Model derivation: run condition, threshold equation, monotone dependence on `mu` | 3 | Derive from §5.2 with numbered assumptions |
| `solver.py`, `calibrate_buffer` and the local test run | 4 | Implement the frozen interface, pass seeds 0 to 49, handle the three named conditions |
| Calibration intake and the calibration target (B3) | 2 | State the target, its basis (SIMULATED or quoted with locator), and the attainable range |
| Write-up `memo.md` | 2 | Model, method, results, limits, graded claims |
| Self-assessment against exemplars | 1 | Score the memo with the rubric, then compare with `exemplar-a` and `exemplar-b` |
| **Total** | **14** | Equals `data-hours-project` on the hub |

### 5.4 Calibration and attainable range (`grader/instance.py` and the page)

- The calibration target is a run threshold in `[0, 1]`. The attainable range of `calibrate_buffer` is the range of
  `run_threshold` as the buffer ranges over `(0, 1)`, which the builder derives and states on the page. A target outside it
  raises the third named `ValueError`.
- Under §6 the target is SIMULATED unless B3 is resolved. The memo must say which case it is in.

### 5.5 Grader (`course/modules/SR/SR1/grader/`, Builder E)

**Files:** `instance.py`, `reference.py` (the full solution; excluded from deployment, BLUEPRINT §7), `starter.py` (stubs that
raise `NotImplementedError`; the suite must fail on it), `test_project.py`. No Atlas path.

**Grader panel** on `project.html`: `<section class="grader-panel" id="grader" data-unit="SR1" data-grader="grader/"
data-suite="test_project.py" data-support="instance.py" data-solution="solver.py" data-starter="starter.py"></section>`.
`data-packages` is empty (standard library only). `tools/run_graders.py` reads these attributes (E4 §5.4 locator).

**Instance generator (`make_instance(seed: int) -> dict[str, float]`).** Deterministic: `random.Random(seed)` only. Draws
`mu` from the documented range, `kappa` and `ell` from their documented ranges, and a calibration target inside the attainable
range. The docstring says **SIMULATED**. Validity guard per seed: every parameter finite and in its range; the reference run
threshold is strictly inside `(0, 1)` when `mu > 0` (so the threshold test is meaningful); `run_fraction` is in `[0, 1]`. The
instances must differ materially across seeds 0 to 49 (`tools/run_graders.py` `check_instances`, E4 §5.3 locator).

**Exception table** (the tests demand these, and only these; fixer-rules: project graders):

| Condition the page names | Exception | Message must name |
|---|---|---|
| `uninsured_share` below 0 or above 1 (each boundary tested in both directions) | `ValueError` | "uninsured share must lie in [0, 1]" |
| `liquidation_value` not in `(0, 1]` (each boundary tested in both directions) | `ValueError` | "liquidation value must lie in (0, 1]" |
| `target_threshold` outside the attainable range stated on the page | `ValueError` | "target threshold is not attainable" |

Each named condition gets its own isolated test per boundary and direction. `liquidation_value = 1` is valid (no discount).
`uninsured_share = 0` is valid and returns the stated no-run convention. Any other invalid input may raise any exception or
return.

**Test properties** (`test_project.py`; each test recomputes its expectation with an oracle written separately from
`reference.py`):
- range and finiteness: `run_threshold` and `run_fraction` in `[0, 1]`; all outputs finite floats;
- equilibrium identity: at the reported `run_threshold` the run condition holds to `1e-9` when `0 < run_threshold < 1`;
- no-run convention: `uninsured_share = 0` gives `run_threshold = 0.0` and `run_fraction = 0.0`;
- calibration: `solve_model(...)["run_threshold"]` at the buffer returned by `calibrate_buffer` equals the target to `1e-8`;
- monotone dependence on `mu`: `run_threshold` is nondecreasing in `uninsured_share` on a fixed grid. **The test is written only
  if the page states the derivation** (builder derives; verifier checks; otherwise removed);
- independence of method: the reference and the five alternatives (§5.6) agree on `run_threshold` and `run_fraction` within
  `1e-6` on seeds 0 to 49;
- hard-coded answer detection: values change across seeds 0 to 49;
- failure messages name the violated property and hint at the concept (for example "the run condition should hold at the
  reported threshold: check the liquidation proceeds against the uninsured claims"); a failing check **never prints the expected
  value** (`__tracebackhide__` in the helpers, as in E3 §6.7). The collect-only count of the suite is quoted on the page.

**Dual mode.** Identical suite in Pyodide and under local pytest; each test under 5 s in Pyodide; the suite under 60 s.

**Integrity.** Never claim the tests are secret. Integrity rests on per-seed instances (BUILDER_RULES §5.3 item 6).

### 5.6 Student-error mutants and alternatives (written by the verifier, not the builder)

**Ten student-error mutants** (verifier writes each as a complete module to `ledgers/SR1/mutants/<name>.py`, each docstring's
first line naming the student error; `tools/mutate_graders.py --unit SR1 --seeds 0-9` must kill all ten):
1. The insured share used where the uninsured share belongs (`mu` and `1 - mu` swapped in the run condition).
2. The liquidation discount applied to the whole balance sheet, not to the liquidated part only (wrong asset base).
3. Insured depositors counted in the withdrawal fraction (insured depositors assumed to run).
4. No fire-sale discount: `kappa` replaced by 1 inside the solver (the liquidation price is ignored).
5. Root search with no sign-change check: returns the upper bracket when no root is bracketed.
6. The withdrawal fraction reported as `run_threshold` (unit confusion between the fundamental and the fraction).
7. The no-run case (`uninsured_share = 0`) returns 1.0 (always run) instead of the stated convention.
8. Hard-coded answer for seed 0 (a constant threshold for the seed-0 instance).
9. Root search stopped after a fixed 20 steps with no residual check (the residual then exceeds `1e-9` on many instances).
10. Calibration searches the wrong direction: `calibrate_buffer` returns the buffer whose threshold is closest to `1 - target`.

The verifier may add one standard-error or wrong-tolerance mutant; those are not counted in the ten. A mutant that differs from
the reference only where the page states nothing is moved to `ledgers/SR1/equivalent/` with a README proof (ruling 9).

**Five alternative correct implementations** (verifier writes each to `ledgers/SR1/alternatives/alt_<n>.py`; each passes seeds 0
to 49, ruling 10):
1. Bisection on the fundamental with a residual check (the reference's style).
2. Secant or regula falsi with a sign-change safeguard on the same residual.
3. Grid scan of the fundamental followed by bisection refinement.
4. Case analysis of the piecewise-linear run condition, solved in closed form, with a residual check (valid only if the builder
   shows the case split on the page; otherwise replaced by alternative 5).
5. A solver parameterised by the uninsured claim's shortfall variable instead of the buffer, with a different bracket and the
   same outputs.

A damped fixed-point alternative is not required and is accepted only if it converges on every seed in 0 to 49 (E4 architect
ruling of 2026-11-05). Each alternative is a float implementation. A float-based alternative that is wrong on a stated exact rule
is a mutant, not an alternative (ruling 10).

### 5.7 Rubric (memo; `both` requires it, `tools/check_projects.py` `rubric_problems`, lines 58-72)

Five criteria in one `table.rubric#rubric`, each with four observable levels (level 4 down to level 1). Each level descriptor
names something a grader can see.

1. **Model specification.** States the timing, the deposits, the buffer, the long asset, the liquidation value and the
   equilibrium selection, with numbered assumptions. Level 4: lists each assumption with a number and states which result uses it.
   Level 1: "describes the model".
2. **Solver and calibration.** States the root-search method, the bracket, the tolerance and the stop rule; reports the residual
   at each reported threshold; states the calibration target and its basis (SIMULATED or quoted with locator). Level 4: gives the
   residual and the basis for each number. Level 1: "the solver works".
3. **Comparative statics.** Reports how the run threshold responds to the uninsured share and the liquidation value, with the sign
   and the grid. Level 4: states each sign as the solver gives it on the stated grid and says which points the sign holds on.
   Level 1: "runs get more likely".
4. **Numerical rigour and rounding.** States the display rule and computes every number from unrounded values. Level 4: names the
   number of significant digits shown and the rule. Level 1: "rounds the numbers".
5. **Limits and evidence.** Names the model's limits (one bank, a fixed insurance limit, a public fundamental, no policy response,
   the normalised deposit unit, one collateral class). Level 4: grades every empirical claim, names its registry key or says "no
   registry key; not claimed". Level 1: "notes some caveats".

**Exemplars** at two levels: `exemplar-a` (`data-level="4"`) and `exemplar-b` (`data-level="2"`), excerpts of memos on a SIMULATED
instance, each annotated with the descriptors it meets or misses, with `data-scores` and `data-criterion` as in M1
(`course/modules/M/M1/project.html`). Self-assessment form `section.rubric-self` with `data-rubric="rubric"` and
`data-exemplars="exemplar-a exemplar-b"`. The page shows where the student's scores diverge from the exemplar scores.
Calibration: a **separate scorer agent that never opens the project page** scores both exemplars blind, within one level per
criterion (architect ruling 23; VERIFIER §2.6). The page keeps its annotations for learners (ruling 15).

**Adversarial question bank:** not required (§12 Q14). The memo is not an investment-committee defence.

---

## 6. Real-data policy (B3 applies)

- **Embedded (redistributable, grant quoted):** none relevant. `fx_daily`, `fx_monthly` and `ust_daily` are embedded
  (`tools/data_sources.yaml:19`, `:53`, `:91`) and do not bear on bank runs, deposits or repo. No MANIFEST entry is added.
- **Not embedded, and no grant found:** deposit and uninsured-deposit series, bank balance sheets, repo rates and haircuts, and
  the 2023 episode's outflows. `tools/data_sources.yaml` `rejected:` (line 119) does not list any of them. **Not embedded.**
- **SIMULATED everywhere data is generated:** the L03 curriculum lab, the rung-1 and rung-2 instances, every `make_instance` draw,
  the calibration target unless B3 resolves, and the exemplars. Each carries a visible **SIMULATED** label.
- **Honest-pending note** on the project's data page and on L03: "The 2023 calibration target needs deposit-flow data that no
  redistributable source is embedded for yet. The target is a SIMULATED value (BUILDER_RULES §1.7). The request is in the
  DATA_REQUESTS of this plan (§7.2, D-SR1-1)."
- **DATA_REQUESTS** (for the architect; the planner names no licence from memory): one uninsured-deposit and deposit-flow series
  for the 2023 episode, with its issuer URL, the quoted licence sentence, the licence page and the transform (BUILDER_RULES §6.6
  steps 1-5). The candidates named in BLUEPRINT §5.3 are FFIEC call reports and SEC EDGAR/XBRL filings (`BLUEPRINT.md:310-317`);
  each must be checked before use.
- **Bring-your-own-data.** The project may offer a student-supplied CSV of deposit flows that never leaves the browser (BUILDER_RULES
  §6.6, last bullet). This is optional and needs the schema documented and validated; it is not required for the grader.
- No `data-files` attribute on any lab. No figures (§12 Q13).

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Curriculum string | Status and use in SR1 |
|---|---|---|---|
| `diamond1983bank` | "Bank Runs, Deposit Insurance, and Liquidity", Diamond & Dybvig, Journal of Political Economy, volume 91, issue 3, pages 401-419, year 1983, DOI 10.1086/261155 (`references/references.json:6775`); `used_by: ["SR1"]` | "Diamond & Dybvig (1983), JPE 91(3)" (`yaml:447`) | **Matches.** L01 and L02 at paper level after the abstract is read; reading list. |
| `brunnermeier2008market` | "Market Liquidity and Funding Liquidity", Brunnermeier & Pedersen, Review of Financial Studies, volume 22, issue 6, pages 2201-2238, DOI 10.1093/rfs/hhn098 (`references/references.json:4106`); record `year` 2008, `print_year` 2009; `used_by: ["SR1"]` | "Brunnermeier & Pedersen (2009), RFS 22(6)" (`yaml:448`) | **Matches on journal, volume and issue. Year field conflict (B4):** cite the key only and type no year in prose. L03 at paper level after the abstract is read; reading list. |
| `shleifer2011fire` | "Fire Sales in Finance and Macroeconomics", Shleifer & Vishny, Journal of Economic Perspectives, volume 25, issue 1, pages 29-48, year 2011, DOI 10.1257/jep.25.1.29 (`references/references.json:20695`); `used_by: ["SR1"]` | "Shleifer & Vishny (2011), JEP 25(1)" (`yaml:449`) | **Matches.** L03 at paper level after the abstract is read; reading list. |
| `gorton2012securitized` | "Securitized banking and the run on repo", Gorton & Metrick, Journal of Financial Economics, volume 104, issue 3, pages 425-451, year 2012, DOI 10.1016/j.jfineco.2011.03.016 (`references/references.json:10785`); `used_by: ["SR1"]` | "Gorton & Metrick (2012), JFE 104(3)" (`yaml:450`) | **Matches.** L04 at paper level after the abstract is read; reading list. |

**Candidate keys that are registry-verified but not curriculum-listed for SR1.** Using any of them needs the architect's
approval (Q10, Q11).

| Key | Record (as read) | Candidate use |
|---|---|---|
| `jiang2024monetary` | "Monetary tightening and U.S. bank fragility in 2023: Mark-to-market losses and uninsured depositor runs?", DOI 10.1016/j.jfineco.2024.103899, `verified_by: crossref` (`references/references.json:13636`); `used_by: ["BK1"]` | Two-sided counter-evidence or alternative explanation for the uninsured-depositor run claims in L02 and the memo's limits (rubric criterion 5). The title is read from the registry; its content is not read by the planner. The builder reads the abstract before any claim. |
| `frb2023fed` | "The Fed - Review of the Federal Reserve's Supervision and Regulation of Silicon Valley Bank" (2023), primary, `verified_by: issuer` (`references/references.json:9107`); `used_by: ["GM5"]` | The episode's narrative source for the project context and, if read and approved, one quoted figure with locator (B3). |

**Not to be used by SR1:** `adrian2010liquidity` (`:183`, SR2), `geanakoplos2010leverage`, `brunnermeier2014macroeconomic` (SR2),
`cftc1999hedge` (`:4986`, GM5), `bis2024market`, `snb2015swiss` (GM5), `diamond1984financial` (BK1, delegated monitoring; cite only
if the architect approves). Their `used_by` values belong to later or other modules.

### 7.2 REFERENCE_REQUESTS (lead only; no bibliographic record typed by the planner)

- **R-SR1-1 (needed only if L01 or L02 keeps a fundamentals-based run claim).** {doi: null, authors: "not typed", year: "not typed",
  title: "empirical evidence distinguishing self-fulfilling from fundamentals-based bank runs (topic only)", venue: "not typed",
  needed_for: "two-sided treatment of the run mechanism (BUILDER_RULES §2.5)", confidence: "the need is certain; no record identified
  by this planner". Default: the run is taught as a model property with no empirical claim.
- **R-SR1-2 (needed only if the project extends to private information).** {doi: null, authors: "not typed", year: "not typed",
  title: "threshold equilibria with dispersed information in bank-run models (topic only)", venue: "not typed", needed_for: "a
  dispersed-information extension of the project", confidence: "the need is certain; no record identified". Default: not used.
- **R-SR1-3 (needed only if L03 keeps an empirical claim about the size of spirals or fire-sale discounts).** {doi: null, authors:
  "not typed", year: "not typed", title: "empirical estimates of fire-sale or margin-spiral price effects (topic only)", venue:
  "not typed", needed_for: "counter-evidence for a B or C claim", confidence: "the need is certain; no record identified". Default:
  no empirical claim is made.
- **R-SR1-4 (freshness; needed if any empirical sentence about 2023 uninsured-deposit runs is kept).** {doi: null, authors: "not
  typed", year: "2025-2026 (topic only)", title: "2025-2026 work on the 2023 regional-bank episode and uninsured-deposit runs
  (topic only)", venue: "not typed", needed_for: "the freshness check (BLUEPRINT §3) and the two-sided treatment", confidence:
  "the need is certain; no record identified by this planner". Default: no empirical sentence about 2023 is kept beyond the
  primary-source episode narrative.

No request is raised for Diamond and Dybvig's, Brunnermeier and Pedersen's, Shleifer and Vishny's, or Gorton and Metrick's
papers: all four are registered (§7.1). The architect resolves each request through `tools/add_reference.py` (DOI, ISBN, or an
allow-listed issuer page; BUILDER_RULES §2.4). Until then the lessons teach the models by derivation and the mechanisms at paper
level, and each empirical sentence is removed or graded C with its basis named.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for SR1 (no `atlas:` key at `yaml:433-458`; no Atlas entry names SR1, §0.1). No
`atlas/SR1.contract.md` is needed. `check_projects.py` skips the contract check when the project names no `atlas` key
(`tools/check_projects.py` lines 144-146). The Atlas milestone that uses systemic-risk data is A19, which is SR3's
(`yaml:500-504`), not SR1's.

---

## 9. Cards builder (Builder F, after A to E)

- `course/modules/SR/SR1/cards.json`, ids `SR1-c001` upward (sequential ids are not required, architect ruling 2), `lesson` in
  L01 to L04. One card per definition, theorem statement, key formula, key result and misconception (BUILDER_RULES §7).
  `check_pages.py` `check_cards` checks the id prefix, the lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab 1, Derivation 2 (exact)"`.
- Cite a registry key only for an attributed claim (`diamond1983bank` on L01, `shleifer2011fire` and `brunnermeier2008market`
  on L03, `gorton2012securitized` on L04, each after the abstract is read). `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis` (the L03 curriculum lab). No card cites a §7.1 candidate key
  unless the architect approves it.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit SR1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit SR1
.venv/bin/python tools/check_projects.py --unit SR1
.venv/bin/python tools/run_labs.py --unit SR1               # --page L03 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/SR/SR1/L01.html                           # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/SR/SR1/L03.html --refresh lab-SR1-L03-1   # after editing a twin
.venv/bin/python tools/run_graders.py --unit SR1 --seeds 0-49                                # after grader files exist
.venv/bin/ruff check tests/labs/SR1 course/modules/SR/SR1/grader && .venv/bin/ruff format --check tests/labs/SR1
.venv/bin/mypy tests/labs/SR1 course/modules/SR/SR1/grader                                    # strict, repository configuration
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit SR1 --seeds 0-9` (the ten mutants, §5.6),
`.venv/bin/python tools/ledger.py --unit SR1 --check` (after fragments exist), `.venv/bin/python tools/page_smoke.py --unit SR1`
(timing-sensitive; not run by builders), and `.venv/bin/python tools/verify_refs.py --unit SR1` (the unit ledger's registry run,
VERIFIER §2.1).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. `tools/fetch_data.py --check` is not needed (no dataset is added).

Flags checked by the planner in the tool sources: `check_pages.py` (`--unit`, `--all`, `--page`), `check_dag.py` (`--unit`,
`--all`), `check_projects.py` (`--unit`, `--all`), `run_labs.py` (`--unit`, `--all`, `--page`), `run_graders.py` (`--unit`,
`--all`, `--seeds`), `mutate_graders.py` (`--unit`, `--all`, `--seeds`; enforces three mutants minimum), `ledger.py` (`--unit`,
`--check`). The planner did not execute the builder commands.

---

## 11. Tooling assumptions that do not hold for SR1 (flagged)

1. **No Atlas milestone.** No `atlas:` key on SR1 (`yaml:433-458`); no Atlas entry names SR1. `check_projects.py` skips the
   contract check (lines 144-146). No `atlas/SR1.contract.md` is drafted.
2. **No debate.** SR1 has no `debate:` key, so `check_pages.py` does not require a debate brief (`check_pages.py:412-413`). The run
   mechanisms and the repo-run evidence are contested in the literature, so the two-sided rule (BUILDER_RULES §2.5) applies anyway.
3. **Two grading modes.** `grading: both` requires the grader panel, the autograder words, the rubric and two exemplars at two
   levels (`check_projects.py` grader-panel check at about line 123; `GRADING_WORDS` line 38; `rubric_problems` from line 58;
   E4 §11 item 3 gives the same locators, read by its planner).
4. **Ten mutants and five alternatives are not enforced by a tool.** `mutate_graders.py` enforces three mutants minimum; the ten
   and the five are verifier duties recorded in the ledger's `mutants` list and the alternatives folder.
5. **One curriculum lab, four lesson twins.** The curriculum names one lab (`yaml:451`). The plan adds one lab per lesson (E4 and
   E5 precedent) and three project labs. The curriculum lab is `lab-SR1-L03-1` (§1).
6. **Prerequisite status.** BK1 is not built (§0.1, B2). E4 is built. The hub and lessons link prerequisite concepts through
   `concepts.html` anchors only (BUILDER_RULES §4.1); a BK1 anchor currently reads "not yet released" (`course/concepts.html:559`).
7. **`check_dag` sees linked uses only.** Unlinked names of out-of-closure concepts (§4) pass the tool. The verifier reads every
   lesson and the project for them.
8. **The SR part directory does not exist.** `course/modules/SR/` is absent (planner `ls`). The first builder creates
   `course/modules/SR/SR1/` only; no other SR directory is created.
9. **Hours rules.** Lesson hours 6 to 12 (`check_pages.py` `check_lesson`) and hub split (`check_hub`) are satisfied by §1.
10. **The first-year and PhD groupings** (`curriculum/meta.yaml:124`, `:134`) place SR1 in the PhD requirements and the field course
    "Intermediation & Macro-Finance". This is a curriculum-grouping fact; the plan does not act on it.

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Lesson count and hours.** RECOMMENDED: 4 lessons × 9 h = 36 h and a 14 h project (28%). Alternative within the rules: 5 lessons
   × 8 h and a 10 h project (20%); the L01 and L03 concept split of §1 then changes. Hours stay as declared once set (HOURS ruling).
2. **File ownership.** RECOMMENDED: Builder A owns L01 and the hub; B owns L02; C owns L03 (the curriculum lab); D owns L04; E owns the
   project, grader and project labs; F owns cards. This is one lesson per builder, because the brief's "about three lessons per
   builder" needs about 15 lessons and 90 h against a 36 h budget (B5).
3. **B1, repo concepts (FI4).** RECOMMENDED: add FI4 to SR1's prerequisites (`curriculum/05-macro-alternatives.yaml:437` and
   `curriculum/curriculum.json`). FI4 is topologically earlier (index 33 against 49) and its closure excludes SR1, so there is no cycle.
   Without the change, L04 uses plain sentences that define repo and haircut in the sentence (§4 D1-D2), and the default rule of
   "no dfn" must be read as applying only to terms defined elsewhere.
4. **D3 to D10 and D14, other outside terms.** RECOMMENDED: confirm the defaults in §4 (plain sentences; no links; no SR2, SR3 or X4
   concept). Confirm no further prerequisite change beyond FI4.
5. **B2, BK1 build order.** RECOMMENDED: build BK1 before SR1 (topological order: BK1 index 31, SR1 index 49). The BK1 concepts show
   "not yet released" until BK1 is built, so SR1 links to them only after that. If the architect wants SR1 earlier, the builders use
   plain sentences for the three BK1 concepts instead.
6. **D15, closure links.** RECOMMENDED: link closure concepts as in §2.2 and §4 D15. No other change.
7. **Scope.** RECOMMENDED: as §2.1 item 4 (one bank at a time; two or three dates; finite depositor sets in labs; one risky asset and one
   collateral class in the project; no general equilibrium; no policy response beyond a defined lender of last resort; no claim that
   runs are empirically self-fulfilling). Confirm.
8. **Project model.** RECOMMENDED: the one-bank, three-date, public-fundamental model of §5.2 with `solve_model` and
   `calibrate_buffer`. The curriculum names no model (`yaml:452-458`). Decision needed before the project is built.
9. **Solver interface (freeze before building).** RECOMMENDED: the two functions and the keys of §5.2, with exactly three named `ValueError`
   conditions (§5.5). Any other condition is unspecified.
10. **Candidate key `jiang2024monetary`.** RECOMMENDED: approve it as the two-sided counter-evidence for the uninsured-run claims in
    L02 and the memo's limits, after the builder reads the abstract. Default if not approved: no empirical claim about 2023 is kept.
11. **Candidate key `frb2023fed`.** RECOMMENDED: approve it as the episode's narrative source for the project context. Quoting one figure
    with a locator needs the builder to read the page first. Default: no figure is quoted.
12. **B3, calibration data.** RECOMMENDED: SIMULATED calibration target with an honest-pending note and DATA_REQUEST D-SR1-1 (§6).
    Alternative: quote one figure from `frb2023fed` once it is read and approved (Q11).
13. **Figures.** RECOMMENDED: none in SR1. A figure of the run threshold against the uninsured share would need a kernel and a test
    under `tests/test_figure_kernels.py` first (BUILDER_RULES §6.4).
14. **Adversarial question bank.** RECOMMENDED: none. The memo is not an investment-committee defence or a debate.
15. **Notation.** RECOMMENDED: the local symbols of §2.3 and the forbidden list (`T`, `\Phi`, `\gamma_3`, `\gamma_4`, `R^\ast`,
    `R^{e\ast}`, `R_f`, `\mathbb{Q}`, bare `R` for a return). No NOTATION_REQUESTS.
16. **B4, Brunnermeier and Pedersen year.** RECOMMENDED: cite `brunnermeier2008market` by key, with no year in prose; the architect
    decides whether a registry note is added. Builders never edit the record.
17. **Mutant and alternative counts.** RECOMMENDED: ten mutants under `ledgers/SR1/mutants/` and five alternatives under
    `ledgers/SR1/alternatives/`, each alternative passing seeds 0 to 49 (ruling 10). If the suite exceeds 60 s in Pyodide, the seed
    window is the architect's call (E3 used seeds 0 to 9).
18. **Curriculum lab placement.** RECOMMENDED: the margin-spiral lab at L03 (the lesson that defines `liquidity-spiral` and `fire-sale`).
    The alternative is L02, which would put the spiral before the fire-sale concept.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 (with the hub), L02, L03 (includes the curriculum lab
   `lab-SR1-L03-1`), L04, the project (the rubric and exemplar calibration by the separate blind scorer, the ten mutants and five
   alternatives, and the grader's runs), and the cards. Failing rows return to the owning builder, with only the failing rows.
3. Ledger at `ledgers/SR1.verification.json`, built from fragments under `ledgers/SR1-<slice>.json` (`tools/ledger.py --unit SR1 --check`).
   Verifier scripts are archived under `ledgers/SR1/scripts/` (VERIFIER §3). Mutants under `ledgers/SR1/mutants/`, alternatives under
   `ledgers/SR1/alternatives/`, equivalents under `ledgers/SR1/equivalent/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B2 must be resolved, or
   named as honest gaps, before the L04 and L02 builders start. B3 is a named gap if it stays open.

Architect decisions: pending (§12). This plan is the planner's proposal. Where a question has a RECOMMENDED decision, that decision
is the default that the builders follow until the architect says otherwise.

## Architect decisions (pending, binding once recorded). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all; no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank.
Module specifics (proposal): 4 lessons × 9 h + 14 h project; builders A: L01 and index; B: L02; C: L03; D: L04; E: project and grader; F: cards. Project model: the one-bank public-fundamental model with `solve_model` and `calibrate_buffer`. Two architect decisions are needed before their owners start: B1 (add FI4 to the prerequisites, or accept plain sentences in L04) and B2 (build BK1 first, or accept plain sentences for its three concepts). B3 (calibration data) is needed before the project's calibration section is written.
