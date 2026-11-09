# BK3 build plan: Insurance & Pensions (2026-11-09)

Unit: **BK3 · Insurance & Pensions** · tier M · 60 h · prerequisites BK1, FI1 · no Atlas milestone · no debate key ·
grading `both` (autograder and rubric) · output directory `course/modules/BK/BK3/` (part code `BK`) · lab twins `tests/labs/BK3/`.
Structure template: `plans/E5-build-plan.md` (sections 0 to 13). Nearest built prerequisite read in full: `plans/FC1-build-plan.md`
(see §0.4). Part precedent for a `both` project, read where cited: `plans/BK4-build-plan.md` §1 (outline), §5.5 (autograder design), its
2026-11-04 architect ruling, and the first 60 lines of `plans/BK4-open-items.md`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no check tools run, no file written except this one.
Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement cites `file:line` read by the planner. Anything the curriculum does not state is
marked **NOT IN CURRICULUM**. Registry facts cite `references/references.json` by line. Tool facts cite the tool's line.
Closed forms in §3 and §5 are planner derivations: the builder re-derives them and the verifier re-checks them.

**Status: the plan is complete for the lessons and the project design. Blocking items are in §0.3 and §12 (Q1, Q2, Q3, Q5, Q8).
Builders for the project (E) must not start until the simulator interface in §5.2 is frozen by the architect (Q8).**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part BK, title "Financial Institutions" (code `BK`) | `curriculum/02-economics-finance-core.yaml:961-963` (`order: 8`, `code: BK`, `title`) |
| BK3 id, title "Insurance & Pensions" | `curriculum/02-economics-finance-core.yaml:1043-1044` |
| Tier `M`, hours `60` | `curriculum/02-economics-finance-core.yaml:1045-1046` |
| Prereqs `[BK1, FI1]` (only) | `curriculum/02-economics-finance-core.yaml:1047` |
| Core: "Actuarial basics, insurer balance sheets and regulation, pension funding and discount-rate choice, liability-driven investment and its 2022 failure mode." | `curriculum/02-economics-finance-core.yaml:1048-1050` |
| `introduces` has 7 concepts (assigned to lessons in §1): `actuarial-present-value`, `insurer-balance-sheet`, `insurance-capital-regulation`, `pension-funding-ratio`, `liability-discount-rate`, `liability-driven-investment`, `ldi-collateral-spiral` | `curriculum/02-economics-finance-core.yaml:1051-1058` |
| Sources: Koijen & Yogo (2015), AER 105(1); Novy-Marx & Rauh (2011), JF 66(4); Bank of England, Financial Stability Report on the 2022 LDI episode (primary) [V] | `curriculum/02-economics-finance-core.yaml:1059-1062` |
| Lab: "Pension funding ratio under discount-rate choices." (names no dataset) | `curriculum/02-economics-finance-core.yaml:1063` |
| Project "LDI collateral-spiral model"; brief: "Model a leveraged LDI fund's collateral needs under a gilt-yield shock, find the forced-selling threshold, and evaluate the central-bank backstop."; deliverable "Simulator plus post-mortem."; grading `both` | `curriculum/02-economics-finance-core.yaml:1064-1070` (brief 1066-1068, deliverable 1069, grading 1070) |
| No `debate:` key, no `atlas:` key, no `data` field on BK3 | `curriculum/02-economics-finance-core.yaml:1043-1070` (absent) |
| BK3 JSON row mirrors the YAML (hours 60, prereqs BK1 and FI1, 7 concepts, 3 sources, lab, project, grading both) | `curriculum/curriculum.json:8497-8528` (`"id": "BK3"` at 8497) |
| BK3 is named by no Atlas milestone | `curriculum/curriculum.json` `atlas` array (no `BK3` string; planner check) |
| BK3 is in no bachelor's credential requires list; it is a target of the RISK track | `curriculum/meta.yaml:63` (bachelor `requires`, no BK3); `curriculum/meta.yaml:189` (`targets: [PR4, SR3, SR4, BK3]`) |
| STUDIO-BK requires BK1 and FI1, not BK3 | `curriculum/02-economics-finance-core.yaml:967` |
| Course-catalogue line for BK3 (same content as the YAML) | `CURRICULUM.md:566-568` |
| Topological position of BK3 is 45 (the order has 134 entries, indices 0-133); its prerequisites come earlier: BK1 31, FI1 18, FC1 26, AC1 4, CF1 11, M2 and M1 earlier still | `curriculum/curriculum.json` `topological_order` (planner check with `tools/coursekit.py`) |

### 0.2 Prerequisite closure and hours feasibility

**Closure (computed):** `tools/coursekit.py` `prerequisite_closure("BK3")` (run by the planner through `.venv/bin/python`) returns
**{AC1, BK1, CF1, E1, FC1, FI1, M1, M2, P0.1}**. The closure's concepts are the `introduces` lists of those nine modules
(`tools/coursekit.py` line 239-249 walks the `prereqs` of each entry). Sizes: AC1 12, BK1 11, CF1 10, E1 13, FC1 10, FI1 16,
M1 14, M2 13, P0.1 11 concepts.

Built status (`course/modules/`): built are AC1, CF1, E1, FC1, M1 and M2. **Not built:** P0.1 (no `course/modules/P0/`), **BK1** (`course/modules/BK/`
holds BK4 only) and **FI1** (`course/modules/FI/` does not exist).

Hours (`curriculum/02-economics-finance-core.yaml:1046`, 60 h). Tool rules: lesson `data-hours` 6-12 (`tools/check_pages.py` line
227-228); hub `data-hours-lessons + data-hours-project = 60` and lesson sum equal to the hub lessons figure (`check_pages.py`
lines 341-342); project 10-40% of 60, i.e. 6 to 24 h (`check_pages.py` lines 339-340).

Chosen split: **5 lessons × 9 h = 45 h; project 15 h (25.0%)**. 45 + 15 = 60. Feasible. No STOP condition on hours.

Why not more lessons: with a project of at least 6 h (10%), lessons can total at most 54 h, which allows at most nine 6-h lessons.
Four lesson builders with about three lessons each would need twelve lessons, at least 72 h. This is infeasible (§12 Q3).

### 0.3 Blocking issues (architect decision required)

**B1. Both direct prerequisites are unbuilt.** BK1 and FI1 have no pages (`course/modules/BK/` has only BK4; `course/modules/FI/`
does not exist). Their concept anchors exist in `course/concepts.html` but read "not yet released": for example
`economic-value-of-equity` at `course/concepts.html:557` and `duration` at `course/concepts.html:341`. BK3 links to those anchors, so
until BK1 and FI1 are built, every such link lands on "not yet released". BLUEPRINT §9 Phase 2 fans out in topological order
(`curriculum.json` `topological_order`), and BK1 (31) and FI1 (18) precede BK3 (45) in that order.
**Planner's recommendation:** plan now; start BK3 builders after the BK1 and FI1 ledgers are PASS (§12 Q1). The project and
lesson text do not depend on BK1 or FI1 pages, only on their concept names.

**B2. The Builder allocation in the brief cannot be "about three lessons per builder".** See §0.2. Recommended allocation in §1 (2, 1,
1, 1 lessons for A to D; Builder E owns the project). **Architect decision (§12 Q2, Q3).**

**B3. The simulator interface is not frozen.** The project needs a fixed Python interface (§5.2) and fixed integer rules before
Builder E starts. The candidate in §5.2 is the planner's proposal. **Architect decision (§12 Q8).**

**B4. The 2022 episode has no registry source.** The curriculum core names "its 2022 failure mode" (yaml:1049-1050) and the source list
names the Bank of England FSR (yaml:1062). The registry has no record for it. It is listed as a `primary` document, flagged `V`, and
"add manually with an authoritative URL" (`references/review_queue.json:819-822`; `references/SEED_REPORT.md:70`). The domain
`bankofengland.co.uk` is on the allow-list (`references/authorities.yaml:23` and `:41`). **Until admitted, no page states any fact about
what happened in 2022** (§3, L05; §5.4 criterion 5). The models themselves do not need it. **Architect action: REFERENCE_REQUEST (§7.2).**

**B5. No redistributable data exists for the gilt-yield shock.** The curriculum names no dataset (yaml:1043-1070). The only embedded
snapshots are `fx_daily`, `fx_monthly` and `ust_daily` (`tools/data_sources.yaml:19`, `:53`, `:91`; `course/assets/data/market/MANIFEST.json`
lists exactly those three). `ust_daily` covers U.S. Treasury bills and constant-maturity yields, not gilts. **Default: SIMULATED with an
honest-pending note (§6).** Not a blocker under the default.

Non-blocking, but the architect should see them:

- **B6. The two in-scope papers are registered, but the planner did not read them.** `koijen2015cost` (`references/references.json:14758`;
  "The Cost of Financial Frictions for Life Insurers", AER 105(1), 445-475, `used_by` BK3, status verified) and `novymarx2011public`
  (`references/references.json:18154`; "Public Pension Promises: How Big Are They and What Are They Worth?", JF 66(4), 1211-1249, `used_by`
  BK3, status verified). The curriculum strings match these records on authors, venue, volume and year (yaml:1060-1061). No
  claim beyond the title may be made until a builder or verifier reads the abstract (VERIFIER_RULES §2.1). §7.1 sets the grade.
- **B7. Citation rule number.** The E5 plan cites BUILDER_RULES §2.5 for counter-evidence. In `BUILDER_RULES.md` the counter-evidence rule is
  §1.5 (lines 58-59). §2.5 is the working-papers rule (lines 96-97). This plan uses §1.5.

### 0.4 Template and precedent read

- **Structure template:** `plans/E5-build-plan.md`, sections 0 to 13, copied in order (with a `both` grader added under §5).
- **Nearest built prerequisite:** the distance-2 built prerequisites of BK3 are AC1, CF1, FC1 and M2 (BK1 and FI1 at distance 1 are not built;
  BK1 requires FC1, FI1 and AC1, and FI1 requires M2 and CF1, `curriculum/curriculum.json` prereqs). The planner chose **FC1**, a direct
  prerequisite of BK1, and read `plans/FC1-build-plan.md` in full. The tie is recorded here; the choice is not binding.
- **Same-part `both` precedent:** `plans/BK4-build-plan.md` (built, `both`, five lessons, 15 h project) and its open items.
  BK4 is not a prerequisite of BK3; it is read for the part's conventions only.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms, §12 Q2 and Q3)

5 lessons × 9 h = 45 h; project 15 h; total 60 h. Concept counts per row sum to 2+1+2+1+1 = 7, each concept in exactly one row
(`yaml:1051-1058`). Hub `data-hours-lessons="45"`, `data-hours-project="15"`.

| Lesson | Title (working; must match the lesson `<h1>` and the hub entry) | Concepts it defines (`introduces`, yaml:1051-1058) | Lab (twin id, `tests/labs/BK3/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Actuarial present value and the insurer's balance sheet | `actuarial-present-value`, `insurer-balance-sheet` | `lab-BK3-L01-1`: present value of a level benefit paid while alive, with a constant survival probability, by the finite sum and by the geometric closed form, exact in `Fraction`; inputs labelled illustrative (not data) | 9 | Builder A |
| L02 | Insurance capital regulation | `insurance-capital-regulation` | `lab-BK3-L02-1`: an insurer balance sheet under parallel yield shocks; the identity assets = liabilities + capital checked exactly; the stylised capital-ratio threshold solved in closed form | 9 | Builder A |
| L03 | Pension funding and the choice of liability discount rate | `liability-discount-rate`, `pension-funding-ratio` | `lab-BK3-L03-1` (**the curriculum lab**, yaml:1063): the funding ratio under three discount-rate choices on illustrative cash flows, exact in `Fraction`, the monotone direction printed | 9 | Builder B |
| L04 | Liability-driven investment: duration matching and its residual | `liability-driven-investment` | `lab-BK3-L04-1`: DV01 matching of a bond portfolio to a liability; the first-order hedge checked by a finite difference of exact bond prices; the convexity residual printed | 9 | Builder C |
| L05 | The LDI collateral spiral and the central-bank backstop | `ldi-collateral-spiral` | `lab-BK3-L05-1`: the one-step margin-call threshold in closed form against a brute-force search over integer shocks; a SIMULATED model path with and without the backstop, in integer cents | 9 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 45 / 15 | none | none | - | Builder A (after L01 and L02 exist) |
| project | LDI collateral-spiral model (`both`, §5): `project.html`, grader, rubric, exemplars | none | `lab-BK3-project-1` (rung 1), `lab-BK3-project-2` (rung 2, `class="lab completion"`), `lab-BK3-project-3` (rung 3 check) | 15 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` (§5.5) | none | none | - | Builder E (last builder, owns project.html, grader and project labs) |
| cards | `cards.json` from L01-L05 | none | none | - | Builder F (after A-E) |

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes `index.html` after L01 and L02 exist, so the
lesson map is right; the cross-check runs at integration. Builder E writes the project, grader and rubric from §5 and does not depend on
the lesson wording, only on the frozen interface in §5.2. Builder D is the lesson that uses the most project vocabulary; it must not
define the project's interface.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses only, §4):

- L01 uses M1 `present-value`, `annuity`, `geometric-series`, `discount-factor` and AC1 `balance-sheet` (all in the closure); defines
  `actuarial-present-value`, then `insurer-balance-sheet`.
- L02 uses L01's `insurer-balance-sheet` (link `L01.html#def-insurer-balance-sheet`) and BK1 `basel-iii-capital` (in the closure; anchor
  exists, §0.3 B1); defines `insurance-capital-regulation`.
- L03 uses L01's `actuarial-present-value` (link), FI1 `spot-rate` and `curve-bootstrapping` (in the closure), M1 `present-value`, M2
  `derivative` (for the monotone direction); defines `liability-discount-rate`, then `pension-funding-ratio`.
- L04 uses L03's `pension-funding-ratio` and `liability-discount-rate` (links), FI1 `duration`, `dv01`, `convexity` (in the closure),
  M2 `finite-difference-derivative` and `taylor-theorem`; defines `liability-driven-investment`.
- L05 uses L04's `liability-driven-investment` (link) and FI1 `dv01` (link); defines `ldi-collateral-spiral`. It names the swap, the repo
  haircut and the backstop in plain prose (§4).

Hours check: 5 × 9 = 45 (hub `data-hours-lessons="45"`); project 15 (hub `data-hours-project="15"`); total 60 = curriculum (yaml:1046).

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to BK3)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` (its §2), this file, and the
FINAL-ARCHITECT-RULINGS and fixer-rules documents named in §2.1. Study `course/modules/BK/BK4/` (the part's built layout) and
`course/modules/M/M1/` (hub and project grammar). `course/templates/` holds the skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded only at
   display, with the rounding rule stated (half up, to the stated place). Money is integer cents throughout (fixer-rules, "Money is integer
   cents"). Precedents: E5 §2.1 item 1; FC1 §2.1 item 8.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what the
   printed numbers show. Every "checked" or "verified" claim names the lab, the line or the test that did the check (fixer-rules line 7).
3. **Attribute nothing unread.** Only the keys in §7.1 may be cited, at paper level, with no locator, page, table or coefficient unless the
   builder has read it (VERIFIER §2.1). Unread standard or regulation content is ungraded ("not stated here") or removed (fixer-rules,
   "GRADES for unread standards"). No bibliographic data from memory (BUILDER §1.1).
4. **Scope words need a computation, a witness or an explicit hypothesis.** "every", "all", "never", "always", "any", "same", "drives",
   "offsets", "exactly", "only", "insurers", "pension funds", "the regulator" are used only where a derivation or a lab computes the claim.
   BK3 scope (confirm, §12 Q7): one insurer or one fund at a time; one stylised capital rule; discount rates as chosen inputs;
   deterministic shocks; no named regulatory regime; no historical calibration; no mortality table.
5. **Define before use.** Each of the 7 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson and
   never before it. Terms outside the 7 (for example "solvency ratio", "forced sale", "margin call", "haircut", "swap", "gilt", "survival
   probability") are plain `<dfn>` without `data-concept` at first use, or plain prose if not defined (`check_dag.py` skips a `<dfn>` without
   `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation lists numbered Assumptions (A1, A2, ...) before its
   statement. Examples the builders must state: the APV geometric closed form needs `0 < p v < 1` and a finite horizon `n >= 1`; the
   funding-ratio monotonicity needs `A > 0`, `1 + y > 0`, cash flows `c_t >= 0` not all zero; the DV01 match is first order and needs the
   liability and the portfolio to be priced by the same curve shift; the threshold closed form needs `N D_h > 0` (§3, L05).
7. **Grader rule.** Applies to the project grader (§5.5): tests demand an exception type only for conditions the project page names
   (fixer-rules, "PROJECT GRADERS"); one isolated test per named condition, in both directions of each inequality.
8. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; `wbr` in long identifiers; quiz options use
   `fieldset` with `min-inline-size:0`; `$` is written `\$` inside math (fixer-rules, "Money ... No horizontal scroll"). Enforced by
   `page_smoke.py`, run by verifiers only.
9. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
   guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py` line 55). Model: `tests/labs/M1/lab-M1-L04-1.py`.
10. **Labs are demonstrations, not graders.** A mutated lab that still exits 0 is not a defect unless a lesson sentence claims the lab asserts
    that property (FINAL-ARCHITECT-RULINGS is silent here; fixer-rules, "LAB MUTANTS (architect ruling)"). Do not add asserts to labs to kill mutants.
11. **Process words are banned in learner text.** No "build", "builder", "round", "verifier", "REQUESTS", "unit report" (fixer-rules line 14).
    The process sense of "round" is banned: the spiral's iterations are "steps", never "rounds". The arithmetic terms "rounding" and
    "rounded" are allowed. Planning references are not allowed in code comments.
12. **Rung 2 completion labs.** The twin is the completed solution, the page shows the same program with `___` blanks, and every page line
    equals the twin line or contains a blank (FINAL-ARCHITECT-RULINGS 11; `run_labs.py` completion rule).
13. **T versus C for worked values.** A value the page derives by hand in a numbered Example, with its hypotheses, is graded T with the
    Example as basis. A value that appears only in lab output, or rests on SIMULATED inputs the page does not derive, is graded C naming the
    lab (FINAL-ARCHITECT-RULINGS 13). A card and the key-results row it mirrors carry the same grade and basis.
14. **Honest-pending definitions.** A concept or claim waiting for an unadmitted source carries a visible "pending" note and the model the
    lesson does define, stated separately (FINAL-ARCHITECT-RULINGS 14). This applies to every 2022 statement (B4).
15. **Two-sided contested claims.** The discount-rate choice, the value of pension promises and any LDI or insurer evidence are contested.
    A claim graded B or C names its published counter-evidence (BUILDER_RULES §1.5). No registry counter-evidence exists for BK3 (§7.2), so
    such a claim is graded C at most, is stated as a model result, or is removed.
16. **Grades for the models.** Derivations on the page are T (§3). An empirical statement about insurers, pensions or LDI funds is C at most
    (§7.1) and waits for an admitted source.
17. **Mutants and alternatives (project).** Ten student-error mutants, each a single-change copy of the reference, first docstring line naming
    the student error, under `ledgers/BK3/mutants/`. A mutant that differs from the reference only where the page states nothing is moved
    to `ledgers/BK3/equivalent/` with a README proof (FINAL-ARCHITECT-RULINGS 9). Five alternative correct implementations of different
    styles pass seeds 0-49 (FINAL-ARCHITECT-RULINGS 10). A float alternative that is wrong on a stated exact rule is a mutant, not an alternative.
18. **Failing checks never print the expected value** (`__tracebackhide__` in every helper; fixer-rules, "PROJECT GRADERS").
19. **Scope of the project's model.** The project uses the stated integer-unit model of §5.2 only. No day counts, no accrued interest, no
    coupon calendar, no instrument-level pricing beyond the duration and margin rules stated on the page.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation (BUILDER_RULES §2.1-2.2).
- Concepts: §1 table; `<dfn data-concept>` only for the 7 registered concepts. A concept outside the closure of §0.2 is plain prose,
  with no `<a class="concept">` (§4). Prerequisite links: `href="../../../concepts.html#<id>"` for closure concepts; `href="Lnn.html#def-<id>"`
  for earlier BK3 lessons. A lesson never links a concept defined in a later lesson.
- Labs: code lives once in `tests/labs/BK3/lab-BK3-Lnn-1.py` (and `lab-BK3-project-1..3.py`). The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids are `lab-BK3-<page>-<n>` (`check_pages.py`
  line 258). Standard library only (`fractions`, `math`, `random.Random(seed)` if any); no network; under 10 s in Pyodide; no warnings
  (`-W error`).
- SIMULATED label: on every lab, figure or project input that uses generated paths or illustrative inputs presented as a path. Exact closed
  forms (L01 APV, L03 funding ratio, L04 DV01, L05 threshold) are not labelled SIMULATED, but their inputs are labelled "illustrative inputs,
  not data" on the page.
- Money: integer cents in the project (§5.3). Lab money in cents where a cash amount appears.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`). Request changes; do not write them.
- Banned strings (`tools/check_pages.py` lines 58-72 `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously",
  "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Growth rates and yields state the unit (per cent per year, decimal) and the compounding
  or discount basis.
- Hub lesson titles match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent).
- Quiz explanations are read against their lesson (CF1 KNOWN 6 precedent).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that BK3 must not give a different meaning (`notation/notation.json` `symbols` array and `macros` object; read in full):

| Registered symbol | Registered meaning (locator) | BK3 rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation.json` `symbols`, module S1) | **Do not use `T`** for maturity or horizon. Use `n` for the number of periods and `\tau` for a maturity in years. |
| `R_f` | gross riskless return (AP1) | Not used. Rates are `y` (yield), `r` (a rate in prose), `v = 1/(1+y)` (discount factor). |
| `\mathbb{Q}` (symbol and macro meaning as AP1) | a risk-neutral measure (AP1) | Not used. Never write `Q` for a quantity. |
| `R^\ast`, `R^{e\ast}` | SDF payoff-space returns (AP1) | Not used. |
| `\Phi`, `\Phi^{-1}`, `\gamma_3`, `\gamma_4` | M4 | Not used (no Gaussian draws; deterministic shocks). |
| `\E`, `\Var`, `\Cov`, `\Corr`, `\R`, `\N`, `\indic`, `\Normal`, ... (macros) | registered macros | The macros may be used for their registered meanings. `\E` is the expectation operator; the APV uses it only where stated. |

Local symbols (allowed; defined in the lesson where first used and never redefined): `A` assets (market value), `L` liabilities (present
value), `K_c` capital (`K_c = A - L`), `c_t` cash flow at period `t`, `p` survival probability per period, `v` discount factor, `y` yield,
`D` duration in years, `D_h` overlay duration in hundredths of a year (§5.2 `overlay_duration_cy`), `N` overlay notional, `\kappa` the capital-rule
parameter, `B_r` remaining liquid buffer at step `r`, `M_r` margin call due at step `r`, `S_r` forced sale at step `r`, `\lambda` price-impact
coefficient (basis points per 10^9 cents sold), `G` backstop capacity remaining, `\bar y` backstop trigger yield. **Capacity is `G`, not `K`;
`K` is not used as a symbol in BK3.** `DV01` is an FI1 concept name, not a symbol. **No symbol may be used for two meanings
across BK3.** The grader's identifiers are code names, not math symbols.

NOTATION_REQUESTS: none. The plan uses local symbols and registered macros only.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2), in order. Each lesson has at least 3 problems per tier
(Mechanics, Proof, Empirical, Research), each with a full worked solution in `<details class="solution">` (BUILDER_RULES §4.2 item 7). The
Empirical tier may use only registered sources at the grades of §7.1, or the model's own outputs. The Research tier is a question with
an answer key that names the registered source or the lab result behind each claim.

- **L01 · `actuarial-present-value`, `insurer-balance-sheet`.**
  - Core: an insurer's liabilities are the present value of promised payments. Assumptions for a level benefit `b` paid at the end of
    each period `t = 1, ..., n` while the insured is alive, with a constant per-period survival probability `p`, `0 < p <= 1`, and a constant
    yield `y > -1`, `v = 1/(1+y)`. Derivation (T): `APV = b \sum_{t=1}^{n} (pv)^t = b\, pv\,(1-(pv)^n)/(1-pv)` when `pv != 1` (geometric series, M1
    `geometric-series`). Planner's arithmetic check of the two forms: `pv = 1/2`, `n = 3` gives `1/2 + 1/4 + 1/8 = 7/8` and
    `(1/2)(1 - 1/8)/(1/2) = 7/8`. The builder derives the form on the page; the lab checks it exactly.
  - Insurer balance sheet: assets `A`, liabilities `L`, capital `K_c = A - L`; the identity is definitional. AC1 `balance-sheet` is linkable.
  - `\E` is used only if the builder states an expectation over survival; otherwise survival enters as the product `p^t`, which is the
    model's own assumption (no expectation concept is linked, §4 D6).
  - Where the canon breaks: a constant survival probability, one yield, no lapses, no options in the contract, no default risk on the
    insurer's liabilities.
  - Lab `lab-BK3-L01-1`: the finite sum and the closed form agree exactly for three parameter sets; all inputs illustrative (not data).
  - Remark (T): APV is linear in `b`; the derivation is the one-line sum.
- **L02 · `insurance-capital-regulation`.**
  - Core: capital is `A - L` under the valuation the model uses. A stylised rule: the insurer must hold capital of at least `\kappa L`,
    `0 < \kappa < 1`, a parameter of the model (not a named regime). A parallel rise of yields by `s` basis points lowers the value of
    assets by `D_A A s/10000` and the value of liabilities by `D_L L s/10000` (first order, M2 `derivative`); the capital ratio change follows
    (T, first order, stated as such). The threshold shock at which the rule binds is solved in closed form (T, with `\kappa`, `A`, `L`,
    durations as inputs).
  - Relationship to BK1: the stylised rule can be compared with BK1 `basel-iii-capital` (linkable anchor; §0.3 B1). The comparison is
    descriptive, with no claim about any bank or insurer regime.
  - Paper: `koijen2015cost` is cited at paper level for the existence of research on financial frictions at life insurers. Grade C.
    Its findings are not stated (§7.1). Counter-evidence is REFERENCE_REQUEST §7.2 (C-grade rule, §1.5).
  - Where the canon breaks: the rule ignores risk weights, lapses and asset-liability mismatch beyond duration; the first-order formula
    misses convexity (linked to L04).
  - Lab `lab-BK3-L02-1`: the identity `A = L + K_c` checked exactly under four parallel shocks; the threshold shock by closed form and by
    search over integer basis points.
- **L03 · `liability-discount-rate`, `pension-funding-ratio`. The curriculum lab (yaml:1063) is here.**
  - Core: the discount rate chosen for pension liabilities is a model input. Three choices in the lab: a flat yield `y`; a spot curve
    `(y_t)` built from zero rates (FI1 `spot-rate`, `curve-bootstrapping`); and a higher rate representing an assumed return on assets (an
    input, not an observed quantity). The funding ratio is `FR = A / L(\cdot)`, where `L` is the present value of the cash flows `c_t >= 0`.
  - Derivation (T): under A1 `A > 0`, A2 `1 + y > 0`, A3 `c_t >= 0` with some `c_t > 0`, `L(y) = \sum_t c_t (1+y)^{-t}` is strictly decreasing in
    `y` (M2 `derivative`: `dL/dy = -\sum_t t c_t (1+y)^{-t-1} < 0`), so `FR(y)` is strictly increasing in `y`. A higher discount rate gives a
    higher funding ratio for the same assets. This is the mechanism the lab shows, not a claim about any plan.
  - Paper: `novymarx2011public` is cited at paper level for the question of how large public pension promises are and what they are worth.
    Grade C. Its numbers are not stated. Counter-evidence on the discount-rate choice is REFERENCE_REQUEST §7.2; the discount-rate choice
    is contested, so the page names that the choice is a model input and that the counter-evidence is pending (§2.1 item 15).
  - Where the canon breaks: a single flat rate ignores the term structure; the spot-curve choice assumes the curve is the right discount
    object; no default or longevity risk is in the cash flows.
  - Lab `lab-BK3-L03-1`: the funding ratio under the three choices on illustrative cash flows, exact in `Fraction`, printed to four decimals,
    half up (stated); the monotone direction printed as a check of the T result above.
- **L04 · `liability-driven-investment`.**
  - Core: LDI matches the interest-rate sensitivity of the assets to that of the liabilities. First-order (T): a price `P` with modified
    duration `D` moves by about `-D P \Delta y`; the dollar duration `DV01 = D P / 10000` per basis point (FI1 `duration`, `dv01`). A
    portfolio is matched when its total DV01 equals the liability DV01. An overlay of rate derivatives with notional `N` and duration `D_h`
    contributes `N D_h / 10000` per basis point. The hedge notional that matches the liability is solved in closed form (T; the derivation is
    shown). The overlay is described in plain prose (§4 D1: swap, FC2).
  - Residual: the first-order match leaves a second-order term. Its size is `\tfrac12` times the convexity times the price times `(\Delta y)^2`
    (T, from the second-order Taylor expansion, M2 `taylor-theorem`). The page states the convexity normalisation it uses, because the FI1 page
    that defines it is not built (§0.3 B1); the normalisation must be the one stated on the page, not recalled.
  - Where the canon breaks: a parallel shift is the only move; the first-order match is valid for small shocks; no basis risk between the
    liability curve and the asset curve; no collateral (L05 is the collateral mechanism).
  - Lab `lab-BK3-L04-1`: DV01 matching solved exactly; the first-order and the exact price change compared by a finite difference of exact
    bond prices (M2 `finite-difference-derivative`); the second-order residual printed against the convexity formula.
- **L05 · `ldi-collateral-spiral`.**
  - Core: a derivative overlay with notional `N` and duration `D_h` has a margin call when yields rise. The model (stated as the model; T
    conditional on it). Let `Y_r` be the cumulative yield move in basis points at step `r`, `Y_0 = s_0` the initial shock. The cumulative margin
    due is `Due(Y) = round_half_up(N D_h Y / 10^6)` in cents, where `D_h` is in hundredths of a year (so `N D_h Y / 10^6 = N (D_h/100)(Y/10000)`).
    At step `r` the new call is `M_r = Due(Y_r) - Due(Y_{r-1})` (with `Due(Y_{-1}) = 0`). The fund pays `P_r = min(M_r, B_r)` from its remaining
    liquid buffer `B_r` (`B_0 = B`, `B_{r+1} = B_r - P_r`). The unpaid part is a forced sale `S_r = M_r - P_r` of bonds at market. The part of
    `S_r` not absorbed by the backstop (below) moves yields by `I_r = round_half_up(\lambda S_r^{unabsorbed} / 10^9)` basis points, so
    `Y_{r+1} = Y_r + I_r`. The path stops at the first step with `S_r = 0` or `I_r = 0`, or after 50 steps; the stop rule is stated on the page.
    The repeated steps are the spiral.
  - Threshold (T, first step, no impact, from the model above): the smallest integer shock `s >= 0` with `Due(s) > B` is
    `s^* = ceil((2B+1) \cdot 10^6 / (2 N D_h))` when `N D_h > 0`. Derivation: `round_half_up(x) >= B+1` iff `x >= B + 1/2`, and `x = N D_h s / 10^6`.
    At step 0 the first forced sale is positive exactly when `s >= s^*`. When `N D_h = 0` no margin call is possible; the page states that the
    threshold is then absent. Worked check (for the grader fixture): `N = 10^8`, `D_h = 500`, `B = 10^6` gives `x = 50000 s`, so `s^* = 21`
    (`50000 \cdot 20 = 10^6 < 10^6 + 1/2 \le 50000 \cdot 21`).
  - Backstop: a central bank absorbs forced sales up to remaining capacity `G` once the cumulative yield move reaches `\bar y`
    (`Y_r >= \bar y`); absorbed sales have no price impact and do not change the margin due. Stated as a model rule; no historical claim
    about any central bank.
  - Episode: the curriculum's "2022 failure mode" (yaml:1049-1050) is named, and no fact about 2022 is stated until the source in §7.2 is
    admitted (§0.3 B4). The lesson says so in one sentence (honest-pending).
  - Where the canon breaks: no price impact in the first step; no counterparties and no default of the overlay; the buffer is a fixed number;
    the backstop capacity is a parameter, not a forecast.
  - Lab `lab-BK3-L05-1`: the closed-form threshold against a brute-force search over integer shocks (exact), then a SIMULATED model path (labelled
    SIMULATED, model output with illustrative inputs) with and without the backstop, in integer cents.

Lesson-level constraints:

- Each lesson's "Where the canon breaks" names at least one model limit and what changes without it (for example, the flat rate in L03, the
  parallel shift in L04, the fixed buffer in L05).
- No lesson uses an E6 (New Keynesian) or E8 (open economy) term as a concept.
- Debate brief: none (no `debate` key, yaml:1043-1070; `check_pages.py` line 412). The contested claims of L03 and L05 are handled by §2.1 item 15.

---

## 4. DAG problems (concepts that natural BK3 content would use outside the closure)

Prerequisite closure (§0.2): **{AC1, BK1, CF1, E1, FC1, FI1, M1, M2, P0.1}**. Owners and lines are from the curriculum files; topological
positions from `curriculum.json` `topological_order`. An out-of-closure concept is plain prose, with no link and no `<dfn data-concept>`.
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring, lines 1-12), so the verifier reads every page for the names in this table.

| Ref | Concept (owner, locator, topo) | Where natural BK3 content would use it | Resolution in this plan |
|---|---|---|---|
| D1 | `interest-rate-swap` (FC2, `curriculum/02-economics-finance-core.yaml:411`; FC2 topo 30) | the LDI rate overlay (L04, L05, project) | plain prose "rate overlay" or "interest-rate swap" with no link; DAG question §12 Q9 |
| D2 | `futures-margining` (FC2, yaml:410) | margin calls on the overlay (L05) | plain prose "margin call"; no link (Q9) |
| D3 | `repurchase-agreement`, `repo-haircut` (FI4, `curriculum/03-markets.yaml:130-131`; FI4 topo 33) | leverage financing and the haircut on collateral (L05, project buffer) | plain prose "haircut"; the buffer is a parameter (Q10) |
| D4 | `fire-sale`, `liquidity-spiral` ("Loss and margin spirals", SR1, `curriculum/05-macro-alternatives.yaml:443-444`; SR1 topo 49, after BK3) | the general mechanism of the LDI spiral | BK3 defines only the LDI instance (`ldi-collateral-spiral`). The general margin spiral is plain prose. Overlap flagged for SR1's builder (Q11). |
| D5 | `lender-of-last-resort` (LX1, `curriculum/06-profession-capstone.yaml:34`; LX1 topo 36) and `policy-backstop` (GM5, `curriculum/05-macro-alternatives.yaml:400`; GM5 topo 132) | the central-bank backstop in L05 and the project | plain prose; the backstop is a model parameter (Q10) |
| D6 | `expectation` (M4, `curriculum/01-foundations.yaml:202`; M4 topo 12) | expected payments in the APV (L01) | plain prose, as E5 D1; M4 would be cheap to add (its only prerequisite is M2, already in the closure); Q12 |
| D7 | `normal-distribution` (M4, `curriculum/01-foundations.yaml:212`) | any Gaussian yield shock | not used. Shocks are deterministic. |
| D8 | `term-premium` (FI3, `curriculum/03-markets.yaml:99`; FI3 topo 63) | the risk premium inside a long yield, L03 choice of discount rate | plain prose; no claim about its size |
| D9 | `swap-spread` (FI4, `curriculum/03-markets.yaml:138`) | the choice between a swap curve and a government curve (L03) | plain prose "swap curve" |
| D10 | `stress-testing` (PR4, `curriculum/04-quant.yaml:347`; PR4 topo 86) | the parallel-shock table in L02 | plain prose "stress test" |
| D11 | `central-counterparty` (BK4, `curriculum/02-economics-finance-core.yaml:1081`; BK4 topo 32) | contrast with bilateral collateral | not used |
| D12 | mortality tables, life expectancy, survival curves | the survival input in L01 | **NOT IN CURRICULUM** as a concept (planner grep of `curriculum.json` `concepts` names for "mortal" and "surviv": no match). Survival is a model input, labelled illustrative. |
| D13 | gilts, named solvency regimes, pension regulation | the project's gilt-yield shock (named in the brief, yaml:1067) and any comparison | **NOT IN CURRICULUM** as concepts. Plain words only; no regime is named (§7.2). |
| D14 | `leverage-cycle` (SR2, topo 120), `gz-credit-spread` (CR3), `credit-default-swap` (CR2) | context of leverage and credit spreads | not used |

### 4.1 Missing-prerequisite questions (DAG questions for the architect)

- **Q-DAG-A (D1, D2): FC2 is not a prerequisite.** FC2 introduces the swap and margining (yaml:410-411; FC2 topo 30, before BK3 at 45).
  FC2's prerequisites are M4, CF1 and FC1 (planner read of `curriculum.json`; the FC1 plan §0 lists M4 and CF1 only). Adding FC2
  adds FC2 and M4 to the closure (FC1 and CF1 are already in it). Default: plain prose.
- **Q-DAG-B (D3, D9): FI4 is not a prerequisite.** Adding FI4 adds E5 to the closure (FI4 prerequisites FI1 and E5, `curriculum/03-markets.yaml`).
  Default: plain prose.
- **Q-DAG-C (D4): SR1 comes after BK3** (topo 49 vs 45) and its `liquidity-spiral` overlaps BK3's `ldi-collateral-spiral`. A link from
  BK3 to SR1 would be a forward reference, so none is made. Default: plain prose, and the overlap goes to the SR1 builder.
- **Q-DAG-D (D5): LX1 and GM5 are not prerequisites.** LX1 (topo 36) needs E5 as well. GM5 (topo 132) is after BK3. Default: plain prose.
- **Q-DAG-E (D6): M4 for expectation** (cheap; §12 Q12).

Each row has a resolution, so no DAG_DEFECT blocks the build; each row is confirmed or changed by the architect (§12). Prerequisite
changes are curriculum changes; the planner and the builders do not edit `curriculum/*.yaml`.

---

## 5. Project (`project.html`, Builder E): `both` (autograder + rubric), ladder, spec, grader, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` line 33 `RUNGS` requires the order)

Tier M: rungs 1 and 2 are kept to the minimum (BUILDER_RULES §5.1 lines 188-189; BLUEPRINT §4 lines 222-223). A placement pass skips
rungs 1-2 (BUILDER_RULES §5.1 lines 191-195).

1. **Rung 1, worked example** (`lab-BK3-project-1`, SIMULATED inputs): one fully solved, annotated margin call for one step of the model
   (one `N`, one `D_h`, one shock of 25 bps, one buffer), each step with a "why" note. Minimal (one instance, no spiral).
2. **Rung 2, completion** (`lab-BK3-project-2`, `class="lab completion"`): the margin-call line is removed (`___`); the forced-sale line is
   removed as well. Graded instantly. The twin is the completed solution (FINAL-ARCHITECT-RULINGS 11). Minimal: two blanks.
3. **Rung 3, independent project** (graded by autograder and rubric): the simulator `ldi_model.py` to the §5.2 interface, and a post-mortem
   memo (rubric, §5.4). Scope: the leveraged LDI fund in the brief, the gilt-yield shock as a parameter, the forced-selling threshold, and
   the backstop evaluation (with and without).
   `lab-BK3-project-3` is the rung-3 check: it recomputes the default instance's threshold and the with/without-backstop paths from the same
   inputs and prints the table the student's simulator must reproduce on that instance.
4. **Rung 4, stretch** (optional, not graded): a second overlay with its own duration and a stated price-impact calibration; or a backstop
   capacity schedule with a stated hypothesis. No ceiling.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading)

Terms present: Context (2-4 sentences), Inputs, Required outputs, Constraints, Grading (the grading entry names both "autograder" and
"rubric": `check_projects.py` `GRADING_WORDS`, lines 36-38, and `grading_problems`, lines 41-49).

- **Context.** An LDI fund holds long bonds against a pension liability and hedges the liability's rate sensitivity with a derivative overlay
  that posts collateral when yields rise. The analyst must size the collateral need under a gilt-yield shock, find the shock at which the
  fund must sell bonds, and assess whether a central-bank backstop changes the outcome.
- **Inputs.** Generated, illustrative parameters (SIMULATED) in `grader/instance.py`, or typed by the student for the memo. No embedded data
  (§6). The gilt-yield shock is a number of basis points, never a series.
- **Frozen interface (planner proposal; the architect freezes it before Builder E starts, §12 Q8).** `ldi_model.py` exposes:
  - `@dataclass(frozen=True) class Fund` with integer fields: `assets_cents` (> 0), `asset_duration_cy` (>= 0, modified duration of the
    bond portfolio in hundredths of a year), `overlay_notional_cents` (>= 0), `overlay_duration_cy` (>= 0, in hundredths of a year), `buffer_cents`
    (>= 0), `impact_bps_per_gcent` (>= 0, price impact in basis points per 10^9 cents sold), `backstop_trigger_bps` (>= 0), and
    `backstop_capacity_cents` (>= 0). All money is integer cents.
  - `margin_call_cents(fund: Fund, cumulative_bps: int) -> int`: the cumulative margin due `Due(Y) = round_half_up(N * D_h * Y / 10**6)` (§3 L05),
    with the exact `Fraction`, one rounding, for `cumulative_bps >= 0`; a negative value raises `ValueError` naming the rule ("a yield move must be
    a non-negative number of basis points"). The margin of one step is the difference of two such values (§3 L05).
  - `threshold_bps(fund: Fund) -> int | None`: the smallest integer `s >= 0` with `margin_call_cents(fund, s) > fund.buffer_cents`, computed by the
    closed form of §3 L05 (the first step, no impact); returns `None` when `overlay_notional_cents * overlay_duration_cy == 0`.
  - `run_steps(fund: Fund, shock_bps: int, backstop: bool) -> list[Step]` where `Step` is a frozen dataclass with the step index, the cumulative
    yield move `Y_r`, the margin call `M_r`, the buffer paid `P_r`, the forced sale `S_r`, the amount the backstop absorbed and the price-impact
    move `I_r` (§3 L05). Step 0 uses the initial shock. The path stops at the first step with `S_r = 0` or `I_r = 0`, or after 50 steps (the cap
    makes the path finite); the stop rule and the cap are stated on the page.
  - The memo reports totals (forced sales, absorbed amounts, the number of steps) computed from the `run_steps` output; no further function is in
    the contract.
- **Rounding rule (the page states it once).** Half up on the exact `Fraction`, `round_half_up(x) = floor(x + 1/2)`, for non-negative
  amounts; one rounding per output, never per intermediate term, except in `run_steps`, where each step's margin call and price-impact move
  are rounded once. Basis points are integers.
- **Required outputs.** `ldi_model.py` with the classes and functions above and a short module-docstring "conventions" block (units,
  sign rule, rounding rule, step definition). The memo `memo.md` (rubric). No other files are required by the grader.
- **Constraints.**
  - Integer cents; valid input (exception table, §5.4 only).
  - Standard library only; no network; the same code runs in Pyodide and under pytest.
  - The student's memo quotes only its own simulator outputs and the registry keys of §7.1 at the grades stated there.
- **Grading.** Both: autograder (`grader/test_project.py`, dual-mode) for `ldi_model.py`, and rubric (§5.4) for the memo. The spec's grading entry names
  "autograder" and "rubric" (`check_projects.py` `GRADING_WORDS`).
- **Reading list.** `ol.reading-list` cites `koijen2015cost` and `novymarx2011public` at paper level (§7.1). Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 15 h; every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved margin call, annotated line by line |
| Rung 2, completion problem | 1 | Two blanks (margin call, forced sale), then the instant check |
| Fund object and `margin_call_cents` | 3 | Integer inputs, one rounding, the negative-shock condition |
| `threshold_bps` closed form and the boundary | 2 | Derive `s^*` and test both sides of the boundary |
| `run_steps` with price impact and the backstop | 3 | Step order, cap of 50 steps, absorbed and unabsorbed sales |
| Tests on seeds 0-9 and the self-check against the conventions block | 2 | Local pytest run, re-read of the conventions block |
| Memo: with and without backstop, the threshold, limits | 2 | Two tables from `run_steps` and one paragraph per claim |
| Self-assessment against exemplars | 1 | Score the memo with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **15** | Equals `data-hours-project` on the hub |

### 5.4 Rubric (memo; `table.rubric#rubric`, `check_projects.py` `rubric_problems`, lines 58-71)

Five criteria. Each criterion is one table row: the criterion name in a `th`, exactly four `td` cells for levels 4 down to 1. Every level
descriptor is observable (BUILDER_RULES §5.4 item 1).

1. **Inputs and assumptions.** Level 4: names each input (notional, overlay duration, buffer, impact, backstop trigger and capacity) with its
   unit and states that it is an illustrative assumption, not data. Level 1: "states the assumptions".
2. **Mechanism.** Level 4: states the margin-call formula, the forced-sale rule and the price-impact step, and ties each to a line of
   `run_steps` output. Level 1: "explains the spiral".
3. **Threshold.** Level 4: reports the threshold from `threshold_bps` and checks it against the first step of `run_steps`. Level 1: "a sensible
   threshold".
4. **Backstop evaluation.** Level 4: compares with and without the backstop on the same inputs and states the capacity and the trigger that
   drive any difference. Level 1: "discusses the backstop".
5. **Limits and evidence.** Level 4: names the model limits used (no price impact in the first step, the fixed buffer, the parallel shift), states
   the counter-evidence for each claim graded B or C, and states that no fact about 2022 is stated because the source is not admitted, or cites the
   admitted source. Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written memos on the default instance, annotated with the
descriptors each passage meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`).
Calibration: the verifier scores both exemplars blind, within one level per criterion (VERIFIER §2.6; FINAL-ARCHITECT-RULINGS 15 and 23): a dedicated
scorer that never opens the project page, runs the stripping script, and reads only its output.

Adversarial question bank: not required (§12 Q15; architect default for every module).

### 5.5 Autograder design (`grader/`, Builder E)

Files (`course/modules/BK/BK3/grader/`): `instance.py`, `reference.py` (the full solution; excluded from deployment, BLUEPRINT §7 and
FINAL-ARCHITECT-RULINGS 4), `starter.py` (stubs raising `NotImplementedError`), `test_project.py`. Grader panel on `project.html`:
`<section class="grader-panel" id="grader" data-unit="BK3" data-grader="grader/" data-suite="test_project.py" data-support="instance.py"
data-solution="ldi_model.py" data-starter="starter.py">` (`check_projects.py` lines 122-138 require the attributes and the files). `data-packages`
is empty (standard library only).

- `instance.py`: `make_instance(seed: int) -> dict` (the exact signature `check_projects.py` line 136 tests). Deterministic per seed from
  `random.Random(seed)`. Labelled **SIMULATED** in the docstring. Validity for every seed: all integers in the stated ranges, `assets_cents > 0`,
  `buffer_cents >= 0`, the impact and backstop fields in range, and the first-step threshold `threshold_bps` lies in `1..10000` (so the linear
  search of the grader is exhaustive over the instance's range). Every seed has a forced-sale branch reached at some step.
  Materiality: across seeds 0-49, `threshold_bps` takes at least 10 distinct values, and the forced-sale totals differ (the answers change, not only
  the labels; the verifier checks 20 sampled seeds).
- `reference.py`: the full solution, following §5.2 exactly, with `Fraction` for the rounding and integers elsewhere. Passes every test on seeds 0-49.
- `starter.py`: stubs that raise `NotImplementedError`. The suite fails on it, naming the property, not a stack trace.
- `test_project.py` (properties and numbers; each test recomputes its expected value from the instance and an oracle written separately from
  `reference.py`; no hard-coded answers; `__tracebackhide__` in every helper so a failure prints no expected value):
  - cumulative margin due: `margin_call_cents(Y)` equals `round_half_up(N D_h Y / 10^6)` for the seed's own `N`, `D_h` and shocks; zero gives
    zero; non-decreasing in `Y` on each seed (tested on the grid of the instance's shocks);
  - margin rounding: a fixture whose exact value ends in `.5` rounds up (half-up, one isolated test; kills truncation);
  - threshold closed form: `threshold_bps` equals the smallest `s` with `margin_call_cents(s) > B`, found by a linear search over `s` in
    `0..10000` on each of seeds 0-9 (the search is the oracle); both sides of the boundary (`s^* - 1` gives no call above the buffer, `s^*` does);
  - threshold `None`: an isolated test when `N * D_h == 0`;
  - steps: step 0 carries the initial shock; each later step's margin call equals `Due(Y_r) - Due(Y_{r-1})`; the stop rule (first step with
    `S_r = 0` or `I_r = 0`) and the 50-step cap hold; a fixture with a buffer larger than the first call stops at step 0 with no forced sale; the
    buffer paid never exceeds the buffer held;
  - price impact: each impact move equals `round_half_up(lambda (S - absorbed) / 10^9)` for the step's forced sale `S` (§3 L05);
  - backstop: with capacity `G` and trigger `\bar y`, the absorbed amount is `min(S, G_remaining)` once the cumulative move reaches the trigger, and
    zero before it; a backstop with zero capacity equals no backstop (both directions);
  - hand-computed fixtures: one fixed fixture per function (for example `N = 10^8` cents, `D_h = 500` (5.00 years), `s = 25`, `B = 10^6`), computed
    on the page (not seed-derived; Q10 precedent);
  - integer output: every money field is an `int`; every basis-point field is an `int`;
  - exception table (§5.2, only the named conditions raise `ValueError`): a negative shock (`margin_call_cents`, `run_steps`); the boundary `shock_bps = 0`
    accepted; `N` or `D_h` negative (the page states "must be non-negative"); each is an isolated test in both directions of the inequality;
  - instance dependence: across seeds 0-49, at least 10 distinct threshold values.
  - Failure messages name the violated property and hint at the concept (for example "the margin call must use the cumulative move, not the step move").
    They never print the answer.
- Dual mode: the same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (must all pass seeds 0-49; the verifier writes them as test-only fixtures in a scratch checkout and
  archives the scripts under `ledgers/BK3/scripts/`; FINAL-ARCHITECT-RULINGS 10):
  1. list comprehensions and a generator for the steps, with the closed-form threshold;
  2. a class-based `Fund` with methods returning frozen `Step` records;
  3. `Fraction` throughout, with one half-up rounding per output;
  4. integer-only, with the threshold by ceiling division `-((-x) // y)` and the half-up rule by integer arithmetic;
  5. bisection over integer shocks on the predicate `margin_call_cents(s) > B`, with no closed form.
- **Student-error mutants (ten).** The verifier writes ten single-change copies of `reference.py` to `ledgers/BK3/mutants/*.py`, each opening with a
  one-line docstring naming the student error. `tools/mutate_graders.py --unit BK3 --seeds 0-9` must kill each (`tools/mutate_graders.py` lines 41-43
  require at least three). The mutants:
  1. the duration is used in years without the hundredths scale (margin 100 times too large);
  2. the threshold uses `>=` in place of `>` (a call equal to the buffer triggers a sale);
  3. the margin call is truncated toward zero instead of rounded half up (breaks the `.5` fixture);
  4. the forced sale is computed before the buffer is applied (sales not reduced by the buffer);
  5. the price impact is applied to the cumulative forced sales instead of the step's sales (double counting);
  6. the initial shock is applied twice (step 0 counted again at step 1);
  7. the backstop absorbs without a capacity limit;
  8. the backstop engages one step late (it reads the next step's yield: a lookahead);
  9. the overlay's sign is reversed (a fall in yields produces the call);
  10. a hard-coded answer for seed 0 (the threshold is the seed-0 value for every instance).
  Each mutant must fail at least one test. A mutant that differs from the reference only where the page states nothing is moved to
  `ledgers/BK3/equivalent/` with a README proof (FINAL-ARCHITECT-RULINGS 9). A mutant that refuses inputs above an arbitrary threshold is not
  required to be killed unless the page states an upper limit (FINAL-ARCHITECT-RULINGS 36).
- After the suite is final, update the collect-only count quoted on the page (fixer-rules, "PROJECT GRADERS").

### 5.6 The reference does not reach the learner

`reference.py` is excluded from the deployed site (BLUEPRINT §7 and §400-401). The repository has no deploy step yet (FINAL-ARCHITECT-RULINGS 4);
the rule is recorded for the owner and is not a defect of this module.

---

## 6. Real-data policy (no data is needed by the curriculum; SIMULATED is the default)

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily` (`tools/data_sources.yaml:19`, `:53`, `:91`). None is a
  gilt, insurer or pension series. **Not used.**
- **Not embedded, and no grant found:** gilt yields (the curriculum names no source for them; the planner has read no issuer's terms and does
  not assume them), insurer and pension data, mortality tables. `tools/data_sources.yaml` `rejected:` (line 119) lists the French library and the
  Open Source Asset Pricing site only. No entry exists for these series.
- **Default (§12 Q5):** SIMULATED. The lab (L03) uses illustrative cash flows and yields typed on the page, labelled "illustrative inputs, not
  data". The project uses generated parameters (`grader/instance.py`) labelled SIMULATED on the page, and the gilt-yield shock is a number of
  basis points.
- **Honest-pending note** on L05 and on the project's inputs page: "The 2022 episode is named in the curriculum. No source for it is admitted
  yet, so this page states no fact about it. The shock and the parameters are illustrative and do not describe any fund." Cited to the
  REFERENCE_REQUEST in §7.2 and the DATA_REQUEST below.
- **DATA_REQUESTS** (for the architect; the planner does not name a source, a licence or a series ID from memory): a UK gilt par-yield series
  (issuer URL, the quoted licence sentence, the licence page, the transform; BUILDER_RULES §6.6 steps 1-5). The Bank of England domain is on the
  allow-list (`references/authorities.yaml:23`), which is a route to a page, not a licence grant. Until a licence sentence is quoted from that page,
  no series is embedded and no MANIFEST entry is added.
- No `data-files` attribute on any BK3 lab. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in BK3 and grade |
|---|---|---|---|
| `koijen2015cost` | Koijen & Yogo, "The Cost of Financial Frictions for Life Insurers", AER 105(1), 445-475, DOI 10.1257/aer.20121036 (`references/references.json:14758`); `used_by: ["BK3"]`; status verified | verified; matches yaml:1060 | L02 insurer frictions, **paper level, grade C**; no finding stated (abstract not read by the planner; VERIFIER §2.1 requires the builder or verifier to read the abstract before any claim beyond the title) |
| `novymarx2011public` | Novy-Marx & Rauh, "Public Pension Promises: How Big Are They and What Are They Worth?", JF 66(4), 1211-1249, DOI 10.1111/j.1540-6261.2011.01664.x (`references/references.json:18154`); `used_by: ["BK3"]`; status verified | verified; matches yaml:1061 | L03 pension liabilities and discount rates, **paper level, grade C**; the discount-rate debate is contested, so the claim names pending counter-evidence (§7.2) |

Not used by BK3, though registered: `diamond1984financial` (`used_by` BK1; `references/references.json:6815`), `shleifer2011fire` (`used_by`
SR1; "Fire Sales in Finance and Macroeconomics"), `bisndbasel` (a Basel III framework record). `shleifer2011fire` would support the fire-sale point of
§4 D4, but its `used_by` is SR1 and the planner did not read it; it is not cited unless the architect approves (§12 Q13).

Planner grep of `references/references.json` keys and titles for "insur", "pension", "actuar", "mortal", "gilt" and "liability" found only the
two keys above (plus unrelated matches). **Other registry keys are not cited.**

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Bank of England (issuer; authors per the publication)", year: "2022 episode (per curriculum string; year of the publication not typed)", title: "Financial Stability Report on the 2022 LDI episode (primary)", venue: "primary publication of the Bank of England", needed_for: "L05 and the project memo, every fact about the 2022 episode; the curriculum's own source (yaml:1062)", confidence: "the curriculum string and its [V] flag are the only lead (`references/review_queue.json:819-822`, `references/SEED_REPORT.md:70`); the domain `bankofengland.co.uk` is allow-listed (`references/authorities.yaml:23`, `:41`); the stable URL must be found by `tools/add_reference.py`, not typed"}
- {doi: null, authors: "Literature on the discount-rate choice for pension liabilities (lead only; no author typed)", year: "not typed", title: "counter-evidence to the use of a higher expected return as a pension discount rate", venue: "not typed", needed_for: "L03 two-sided treatment of a contested claim (BUILDER_RULES §1.5)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Literature on LDI funds and on insurer behaviour under rate shocks (lead only)", year: "not typed", title: "empirical evidence on collateral needs and forced selling in liability-driven strategies", venue: "not typed", needed_for: "L05 and project criterion 5: any empirical statement beyond the model (grade B or C needs counter-evidence)", confidence: "the need is certain; no record is identified by this planner"}
- {doi: null, authors: "Actuarial basics textbook (lead only; no author typed)", year: "not typed", title: "an actuarial mathematics text covering annuities, survival and reserves", venue: "not typed", needed_for: "L01 book-level reference for the survival-weighted present value, if the architect wants one; the page can instead derive the result (T) without it", confidence: "optional; the derivation in §3 L01 needs no source"}
- {doi: null, authors: "Stylised insurer capital rule sources (lead only)", year: "not typed", title: "primary text of a named insurance capital regime", venue: "not typed", needed_for: "only if the architect allows a named regime; the default is the stylised rule of §3 L02 with no regime named", confidence: "optional; default is no regime"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until resolved,
the lessons teach the models with derivations, and each empirical sentence is graded C at most or removed. The 2022 episode is not stated (§0.3 B4).

### 7.3 DATA_REQUESTS and NOTATION_REQUESTS

- DATA_REQUESTS: the gilt par-yield series of §6 (source URL, licence quote, licence page, transform). None is filed yet.
- NOTATION_REQUESTS: none.
- GLOSSARY_REQUESTS: "funding ratio" (a concept, owned here); "forced sale", "margin call", "haircut" as plain `<dfn>` in L05 (no `data-concept`).

---

## 8. Atlas milestone

None. BK3 is named by no Atlas milestone (`curriculum/curriculum.json` `atlas` array has no BK3 entry; §0.1). The project has no `atlas:` key
(yaml:1064-1070). `check_projects.py` skips the contract check (lines 144-146). No `atlas/BK3.contract.md` is needed.

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/BK/BK3/cards.json`, ids `BK3-c001` upward (`check_pages.py` `check_cards`, line 382, requires the id prefix; gaps and
  out-of-order ids are not defects, FINAL-ARCHITECT-RULINGS 2), `lesson` in L01-L05, one card per definition (7 concepts), theorem or
  derivation statement, key formula, key result and misconception (BUILDER_RULES §7).
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab L03-1 and Derivation 3.2 (exact)"`.
- Cite a registry key (§7.1) only for an empirical or attributed claim, and only at grade C. `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`. A card and the key-results row it mirrors carry the same grade and basis.
- No card states a fact about 2022 (§0.3 B4).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit BK3            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit BK3
.venv/bin/python tools/check_projects.py --unit BK3
.venv/bin/python tools/run_labs.py --unit BK3               # --page L03 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/BK/BK3/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/BK/BK3/L03.html --refresh lab-BK3-L03-1  # after editing a twin
.venv/bin/python tools/run_graders.py --unit BK3 --seeds 0-49   # builder-E, after reference.py exists
.venv/bin/ruff check tests/labs/BK3 course/modules/BK/BK3/grader && .venv/bin/ruff format --check tests/labs/BK3 course/modules/BK/BK3/grader
.venv/bin/mypy tests/labs/BK3 course/modules/BK/BK3/grader  # strict; learner-module imports carry a type-ignore with the reason (BK4 open items, decision 5)
```

Verifier only, not builders: `.venv/bin/python tools/mutate_graders.py --unit BK3 --seeds 0-9`, `.venv/bin/python tools/verify_refs.py --unit BK3`
(registry identity, VERIFIER §2.1), `.venv/bin/python tools/page_smoke.py --unit BK3` on a quiet machine (not run by builders; timing-sensitive).
Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`, and the full
gate in CLAUDE.md.

Flag checks: `check_pages.py`, `check_dag.py` and `check_projects.py` accept `--unit`; `run_labs.py` accepts `--unit` and `--page`;
`embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`. The planner did not execute the builder commands; only the coursekit closure and
concept-owner functions were run (§0.2).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key (yaml:1064-1070); no Atlas entry names BK3. The brief's wording has no Atlas reference, so no B2-type
   issue arises.
2. **No debate.** No `debate:` key (yaml:1043-1070); `check_pages.py` line 412 does not require a debate brief. The contested claims of L03 and L05 are
   handled by two-sided treatment (§2.1 item 15).
3. **Both grading.** The spec names both "autograder" and "rubric" (`GRADING_WORDS`, `check_projects.py` lines 36-38). Rubric checks at lines 58-71;
   autograder checks at lines 122-138.
4. **Rung 2 must be graded instantly.** `check_projects.py` accepts a completion lab or a quiz; the plan uses a completion lab.
5. **One curriculum lab, five required.** The curriculum names one lab (yaml:1063); BUILDER_RULES §6.1 and §3.4 require a numerical check per key
   formula. The plan adds one lab per lesson, as BK4 and FC1 did (§1).
6. **BK1 and FI1 are unbuilt.** Concept anchors read "not yet released" (§0.3 B1). `check_dag.py` uses the curriculum closure, so the tool is not blocked.
7. **check_dag sees linked uses only.** Unlinked uses of the §4 names pass the tool; the verifier reads for them (VERIFIER §2.9).
8. **Labs must be exact.** Standard-library `fractions`, `-W error` clean under `python -I`.
9. **The hub's data-hours rules.** Lesson hours 6-12 (`check_pages.py` line 227) and the hub split (lines 339-342) are satisfied by §1.
10. **The placement diagnostic.** `check_pages.py` lines 351-354 require `section.quiz#placement` with `data-mastery` and at least two `data-skill`
    items. The FC1 plan (§4) uses 0.8 as the bar, citing AC4, M1 and E1; the planner has not verified that bar in the tool source and proposes 0.8 (§12 Q14).
11. **Lesson sections.** `check_pages.py` line 75 `LESSON_SECTIONS` requires `why-it-matters`, `canon-breaks`, `misconceptions`, `problems`,
    `key-results`, `quiz` and `references`. A lesson needs a `references` section even when it cites one key or none.
12. **Mutant and alternative minimums.** The tool requires at least three mutants (`tools/mutate_graders.py` lines 41-43). The task requires ten
    mutants and five alternatives (FINAL-ARCHITECT-RULINGS 10). The plan follows the task.

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **B1, sequencing.** BK1 and FI1 are unbuilt; their concept anchors read "not yet released" (`course/concepts.html:557`, `:341`).
   **RECOMMENDED:** build BK3 after the BK1 and FI1 ledgers are PASS, per the topological fan-out (BLUEPRINT §9 Phase 2; topo 18, 31 < 45).
   If the architect instead starts now, the links to BK1 and FI1 concepts show "not yet released" until those modules exist; the
   `check_dag.py` closure check still passes, because it uses the curriculum, not the pages.
2. **Lesson count and hours.** **RECOMMENDED:** 5 lessons × 9 h and a 15 h project (25%), the BK4 pattern (BK4: five lessons, 15 h project).
   Alternatives within the rules: 6 × 8 h with a 12 h project (20%); 8 × 6 h with a 12 h project. Four lessons × 9 h with a 24 h project (40%)
   is inside the rule but overweights the project.
3. **Builder allocation (against "about three lessons per builder").** Twelve lessons would need at least 72 h of lesson time (6 h minimum each),
   which is more than the 54 h left after a 6 h project minimum. **RECOMMENDED:** A owns L01, L02 and `index.html`; B owns L03; C owns L04; D owns
   L05; E owns the project, grader, rubric, exemplars and the project labs; F owns the cards. Builder D owns one lesson, and that is intended.
4. **Registry records.** `koijen2015cost` and `novymarx2011public` match the curriculum strings (yaml:1060-1061). **RECOMMENDED:** cite both at paper
   level, grade C, and state no finding beyond the title until the abstract is read by a builder or verifier; a claim that cannot be read is
   removed.
5. **Data.** **RECOMMENDED:** SIMULATED with an honest-pending note; no embedded series; the DATA_REQUEST in §6 filed for a UK gilt par-yield
   series with its licence sentence quoted from the issuer's page before any use.
6. **B4, the 2022 episode.** **RECOMMENDED:** admit the Bank of England FSR through `tools/add_reference.py` (allow-listed domain) before L05 is
   written. Until admitted, L05 and the memo state no fact about 2022 (the honest-pending sentence of §3 L05).
7. **Scope.** **RECOMMENDED:** confirm the BUILDER §2.1 item 4 scope: one insurer or fund; one stylised capital rule; discount rates as inputs; deterministic
   shocks; no named regime; no historical calibration; no mortality table; no CCP; no repo model beyond a haircut parameter.
8. **Frozen simulator interface (BLOCKING for Builder E).** **RECOMMENDED:** freeze §5.2 as written (the `Fund` fields, `margin_call_cents`,
   `threshold_bps` with `None`, `run_steps` with the 50-step cap, the half-up rule, the non-negative-shock `ValueError`), with the two formulas of
   §3 L05 as the reference model. Constants are integers in the spec.
9. **D1, D2 (FC2: swap, futures margining).** **RECOMMENDED:** plain prose, no prerequisite change (§4.1 Q-DAG-A).
10. **D3, D5 (FI4 repo and haircut; LX1 and GM5 backstop).** **RECOMMENDED:** plain prose; the buffer and the backstop are model parameters (§4.1 Q-DAG-B and -D).
11. **D4 (SR1 overlap).** **RECOMMENDED:** BK3 defines only `ldi-collateral-spiral`; the general margin spiral stays plain prose; the overlap goes to
    the SR1 builder as a note (§4.1 Q-DAG-C). SR1 comes after BK3, so no link is made from BK3.
12. **D6 (expectation, M4).** **RECOMMENDED:** plain prose, as E5 D1 (E5 plan §4). Alternative: add M4 to BK3's prerequisites (cheap: M4 needs only M2, already
    in the closure). Architect decides.
13. **`shleifer2011fire`.** **RECOMMENDED:** not cited by BK3 (its `used_by` is SR1; the planner did not read it).
14. **Placement bar.** **RECOMMENDED:** `data-mastery="0.8"` with nine items, at least two `data-skill` items on the worked example and completion
    lines, and the rest on prerequisites (AC1 balance sheet, FI1 duration and present value, M1 annuity). The bar is the FC1 plan's proposal; the
    planner did not verify it in the tool source.
15. **Adversarial and question bank.** **RECOMMENDED:** not adversarial; no 15-angle question bank (architect default for every module).
16. **Rung minimums (tier M).** **RECOMMENDED:** one worked-example instance and one completion problem with two blanks (§5.1), per BUILDER §5.1 and
    BLUEPRINT §4.
17. **Mutants and alternatives.** **RECOMMENDED:** ten mutants and five alternatives (§5.5) per FINAL-ARCHITECT-RULINGS 10 and the task. The
    fixer-rules minimum of three alternatives is met.
18. **Citation rule number.** **RECOMMENDED:** counter-evidence is BUILDER_RULES §1.5 (B7). The E5 plan's citation of §2.5 is incorrect and should not be copied.
19. **Notation.** **RECOMMENDED:** the §2.3 local symbols, with `\tau` for maturity and `n` for periods, and no `T`, `R_f`, `Q`, `\Phi` or `\gamma` symbols.
20. **Glossary.** **RECOMMENDED:** the terms of §7.3 as plain `<dfn>` without `data-concept`; no GLOSSARY_REQUESTS entry.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 (with the hub), L03 (includes the curriculum lab), L04-L05, the project
   (autograder: ten mutants and five alternatives; rubric: blind scoring by a dedicated scorer, FINAL-ARCHITECT-RULINGS 23), and the cards.
   Failing rows return to the owning builder with only the failing rows.
3. Ledger at `ledgers/BK3.verification.json`; verifier scripts archived under `ledgers/BK3/scripts/` (VERIFIER §3); mutants under
   `ledgers/BK3/mutants/`; equivalents with README under `ledgers/BK3/equivalent/`.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 through B5 must be resolved or named as
   honest gaps first. Never merged incomplete (an unfinished unit breaks `check_pages --all`).

Architect decisions: pending (§12). This plan is the planner's proposal.

## Architect decisions

Pending (§12). When recorded, follow the defaults stated for every module: concepts outside the prerequisite closure are plain prose with no link and
no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all; no real
data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in
`plans/BK3-open-items.md`; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader;
not adversarial, no question bank.

---

## Open gaps the planner could not establish

- The content of `koijen2015cost` and `novymarx2011public` beyond their registry titles: the planner has no paper text and did not read the abstracts.
- The Bank of England FSR's stable URL, authors and year: not in the registry, and not typed here.
- Whether the Bank of England yield-curve data may be redistributed: not read; no licence is assumed.
- The FC1 choice as "nearest built prerequisite" is one of four distance-2 candidates (AC1, CF1, FC1, M2); the tie is recorded in §0.4.
- The placement bar of 0.8 is the FC1 plan's proposal; the tool source checks only that `data-mastery` is present (`check_pages.py` lines 351-354).
- The effect of citing a registry key whose `used_by` does not list the citing module (`shleifer2011fire`) was not checked against the registry tooling.
- No check tool was run; every tooling statement above is a read of the tool source or of a registry or curriculum file.
