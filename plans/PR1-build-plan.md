# PR1 build plan: Mean-Variance in Practice (2026-11-09)

Unit: **PR1 · Mean-Variance in Practice** · tier M · 70 h · prerequisites AP2, S2 · no Atlas milestone · no debate key ·
grading `both` (autograder for the allocators, rubric for the report) · output directory `course/modules/PR/PR1/`
(part code `PR`, title "Portfolio Construction & Risk", `curriculum/04-quant.yaml:234-235`) · lab twins `tests/labs/PR1/` ·
grader `course/modules/PR/PR1/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders A to F, then
independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Statements about the
tooling were checked by reading the tool source, or by running `tools/coursekit.py` (`prerequisite_closure`,
`concept_owner`, `Unit.built`) through `.venv/bin/python -I`. The planner read no source paper and no abstract. Every
attribution in this plan is at paper level, taken from the registry record. Items the planner could not establish are
listed in §11.4.

**Status: BLOCKING QUESTIONS EXIST (§0.3). The hours are feasible. The lesson count must be decided (Q1), because
"about three lessons per builder" for five lesson builders cannot fit 70 h (§0.2). No redistributable return series is
embedded, so the default is generated (SIMULATED) data with an honest-pending note (§6).**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part PR, code `PR`, title "Portfolio Construction & Risk" | `curriculum/04-quant.yaml:233-235` |
| Studio STUDIO-PR requires `[PR2, PR4]`, not PR1 (its brief names Atlas A11 / A12) | `curriculum/04-quant.yaml:237-247` (requires line 239; brief 242-246) |
| PR1 id and title "Mean-Variance in Practice" | `curriculum/04-quant.yaml:249-250` |
| Tier `M` | `curriculum/04-quant.yaml:251` |
| Hours `70` | `curriculum/04-quant.yaml:252` |
| Prereqs `[AP2, S2]` | `curriculum/04-quant.yaml:253` |
| Core text: "Estimation error, 1/N, shrinkage, Black–Litterman, robust optimization." | `curriculum/04-quant.yaml:254` |
| `introduces` has 6 concepts: mean-variance-estimation-error, error-maximization, equal-weight-portfolio, covariance-shrinkage, black-litterman-model, robust-portfolio-optimization | `curriculum/04-quant.yaml:255-261` |
| Sources (6 free-text strings): Michaud (1989), FAJ 45(1); Chopra & Ziemba (1993), JPM 19(2); DeMiguel, Garlappi & Uppal (2009), RFS 22(5); Ledoit & Wolf (2004), JMVA 88(2); Ledoit & Wolf (2017), RFS 30(12); Black & Litterman (1992), FAJ 48(5) | `curriculum/04-quant.yaml:262-268` |
| Lab (the curriculum lab): "Optimizer instability under resampling." | `curriculum/04-quant.yaml:269` |
| Project "Allocator shoot-out"; brief: "Compare sample MV, shrinkage MV, Black–Litterman, minimum variance and 1/N out of sample with turnover costs, and explain the ranking."; deliverable "Code plus report."; grading `both` | `curriculum/04-quant.yaml:270-276` (title 271, brief 272-274, deliverable 275, grading 276) |
| No `atlas:` key on the PR1 project; no debate key on PR1 | `curriculum/04-quant.yaml:249-276` (absent) |
| No Atlas entry names PR1 (the 20 atlas entries name AC2, CF4, CR1, CS1, CS3, DV4, F1, FI1, FI3, GM1, GM4, MS3, PR2, PR4, QR2, QR3, S0, S4, S7, SR3) | `curriculum/curriculum.json` `atlas` array (computed by the planner) |
| JSON row for PR1 matches the YAML (hours 70, prereqs, 6 introduces, lab, grading both) | `curriculum/curriculum.json:10068-10100` (`id` 10068, `part` 10100) |
| PR1 is a prerequisite of PR2, PR3 and two further modules | `curriculum/04-quant.yaml:281` (PR2 `prereqs: [PR1]`), `:309`, `:334`, `:393` |
| PR2 (outside this unit) introduces risk-parity and risk-budgeting and its project uses Atlas A11 | `curriculum/04-quant.yaml:277-300` (PR2 concepts 283-289; project 296-300) |
| PR1 is in the Master's in Finance / Financial Engineering requires list | `curriculum/meta.yaml:93-99` (PR1 at line 98) |
| PR1 is in the course "Portfolio Management" | `curriculum/meta.yaml:107` |
| PR1 is in the CFA topic "Portfolio Management and Wealth Planning" | `curriculum/meta.yaml:162` |
| Topological index: PR1 at 47, AP2 at 34, S2 at 28 (of 134) | `curriculum/curriculum.json` `topological_order` (computed) |
| Prerequisite closure of PR1 (computed with `prerequisite_closure("PR1")`): {AP2, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1, S2} (13 modules) | run output, planner |
| Built inside the closure (`course/modules/<PART>/<ID>/index.html` exists): E1, E3, M1, M2, M3, M4, M7. **Unbuilt**: AP2, CS1, P0.1, S0, S1, S2 | `Unit.built` in `tools/coursekit.py`, run by the planner |
| Concepts usable without definition from the closure: 174 (sum of the closure modules' `introduces`) | run output, planner |

### 0.2 Hours feasibility

The curriculum figure is 70 h (`curriculum/04-quant.yaml:252`). The tool rules:

- lesson `data-hours` 6 to 12 (`tools/check_pages.py:227`);
- hub `data-hours-lessons + data-hours-project = 70` (`tools/check_pages.py:337-338`, inside `check_hub` at 325);
- project share 10 to 40 % of 70, i.e. 7 to 28 h (`tools/check_pages.py:339`);
- lessons sum to the hub's lessons figure (`check_hub`, `tools/check_pages.py:332-342`).

Chosen split: **8 lessons, 50 h in total (6, 6, 7, 6, 7, 6, 6, 6); project 20 h (28.6 %)**. 50 + 20 = 70. Feasible.

**The "about three lessons per builder" request cannot be met.** With a 20 h project the lessons total 50 h, and 9 lessons
at the 6 h minimum need 54 h, so at most eight lessons fit. With the smallest project the rules allow (7 h), the lessons
total 63 h, which holds at most 10 lessons. Five builders at three lessons each would need 15 lessons (at least 90 h).
The plan therefore uses 8 lessons for the four lesson builders A to D (two each), with E owning the project and F the
cards. The alternatives are in Q1.

### 0.3 Blocking issues (architect decision required before builders start)

**B1. Lesson count and builder shape (decision needed; Q1).** See §0.2. Default: 8 lessons, two per builder A to D.

**B2. No redistributable return data (honest gap, not blocking).** The only embedded snapshots are `fx_daily`, `fx_monthly`
and `ust_daily` (`tools/data_sources.yaml:19-52`, `:53-90`, `:91-118`; `course/assets/data/market/MANIFEST.json` lists
those three). None is an equity or multi-asset return series for the five allocators. The issuers of the Kenneth French
library and of the Open Source Asset Pricing site grant no redistribution right (`tools/data_sources.yaml:119-136`, the
`rejected:` list). Default: all returns are generated (SIMULATED), with an honest-pending note on the project and the
labs, and a DATA_REQUEST (§6). The FX spot panel is an optional stretch with a stated caveat (§6, Q7).

**B3. Ordering dependency on AP2 (not blocking the plan; blocking the verification of L01 to L08 against AP2).** The direct
prerequisite AP2 is unbuilt (`course/modules/AP/` holds AP1 only). AP2 is planned (`plans/AP2-build-plan.md`) and lists PR1
as a direct dependant (`plans/AP2-build-plan.md:43`). Links to AP2 concepts (`efficient-frontier`, `minimum-variance-portfolio`,
`tangency-portfolio`, `linear-factor-model`) resolve through `concepts.html` anchors, which `build_site.py` generates from
the curriculum. The content those concepts stand for can be checked only once AP2 is built (topological index 34 for AP2,
47 for PR1, `curriculum/curriculum.json` `topological_order`). Recommended: build PR1 after AP2 is verified (Q15).

**B4. Attribution limit (honest gap).** No abstract of the six registry sources was read. The plan therefore makes no
claim about what any of them finds. Under VERIFIER §2.1 a builder must read the abstract before a locator or a finding is
attributed. Until then the sentence is a naming sentence with no grade and no `data-cite` (FINAL-ARCHITECT-RULINGS 39,
`plans/FINAL-ARCHITECT-RULINGS.md:143-145`).

Non-blocking, for the architect:

- **DeMiguel year.** The registry record has `year` 2007 and `years` [2007, 2009] with `print_year` 2009
  (`references/references.json:6730` block, key line 6730); the curriculum string says (2009) (`curriculum/04-quant.yaml:265`).
  The print year agrees with the string. Default: cite the key, do not type a year in prose (Q14).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

8 lessons (50 h) + project (20 h) = 70 h. Concept counts per row: 1+1+1+1+1+1+0+0 = 6, each concept in exactly one row
(`curriculum/04-quant.yaml:255-261`).

| Lesson | Title (working) | Concept it defines (`introduces`, `04-quant.yaml:256-261`) | Lab (twin id, `tests/labs/PR1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Mean-variance inputs and the estimation error | `mean-variance-estimation-error` | `lab-PR1-L01-1`: unconstrained mean-variance weights in `Fraction` for a two-asset case, at the true mean and at a perturbed estimate; the weight change printed | 6 | Builder A |
| L02 | Optimizer error maximization (**the curriculum lab**) | `error-maximization` | `lab-PR1-L02-1`: "Optimizer instability under resampling" (`04-quant.yaml:269`). SIMULATED: seeded resamples of a four-asset model, the spread of the optimizer's weights printed | 6 | Builder A |
| L03 | The 1/N benchmark | `equal-weight-portfolio` | `lab-PR1-L03-1`: exact `Fraction` check that the 1/N weights equal the mean-variance and minimum-variance weights when the assets are identical and uncorrelated, and differ otherwise | 7 | Builder B |
| L04 | Covariance shrinkage | `covariance-shrinkage` | `lab-PR1-L04-1`: a sample covariance of rank below N (T < N) and its shrunk version; the smallest eigenvalue printed before and after shrinkage | 6 | Builder B |
| L05 | Black–Litterman | `black-litterman-model` | `lab-PR1-L05-1`: the posterior mean in precision form in `Fraction` for a two-asset, one-view case, checked against a second algebraic form | 7 | Builder C |
| L06 | Robust portfolio optimization | `robust-portfolio-optimization` | `lab-PR1-L06-1`: the worst case of a linear objective over a box of expected returns, enumerated at the four vertices in `Fraction` and compared with the penalty formula | 6 | Builder C |
| L07 | Turnover, costs and out-of-sample evaluation | none (plain `<dfn>` for turnover, transaction cost, rebalancing, look-ahead) | `lab-PR1-L07-1`: a rolling backtest on one seed with the correct timing and a planted look-ahead variant; both net Sharpe ratios printed | 6 | Builder D |
| L08 | Ranking the allocators: evidence and limits | none | `lab-PR1-L08-1`: over seeds 0 to 29, the count of seeds in which 1/N has the higher out-of-sample net Sharpe ratio than sample mean-variance; SIMULATED | 6 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 50 / 20 | none | none | - | Builder A (after L01 and L02 exist) |
| project | Allocator shoot-out (`both`) | none | `lab-PR1-project-1` (rung 1), `lab-PR1-project-2` (rung 2, `class="lab completion"`), `lab-PR1-project-3` (rung 3 check) | 20 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01 to L08 | none | none | - | Builder F (after A to D) |

Totals: lessons 6+6+7+6+7+6+6+6 = 50 h; project 20 h; unit 70 h. Hub: `<main data-hours-lessons="50" data-hours-project="20">`.
Project share: 20 / 70 = 28.6 % (`check_pages.py:339` band 10 to 40 %).

Ownership rule: each builder writes only the files named in its row. Builder A writes the hub after L01 and L02 exist (the
E5 precedent, `plans/E5-build-plan.md:119`). Builder E writes the project, the grader, the project labs and the rubric and
exemplars, and does not depend on the lessons' prose. The lesson-to-builder shape is Q1.

Ordering (no lesson links a definition in a later lesson; `tools/check_dag.py` checks linked uses, §4):

- L02 uses L01 (`mean-variance-estimation-error`), the 1/N idea is not needed there.
- L03 uses L02 (`error-maximization`, `href="L02.html#def-error-maximization"`) to motivate the benchmark.
- L04 uses L03 (`equal-weight-portfolio`) as the benchmark the shrunk estimator is compared with.
- L05 uses L04 (`covariance-shrinkage`): the Black–Litterman covariance input is the sample covariance, and L04 explains why
  a shrunk covariance is an alternative input.
- L06 uses L05 (`black-litterman-model`): the robust allocator is applied to an expected-return vector that may come from L05.
- L07 uses L01 to L06 (no new concept); L08 uses L03, L04 and L07 only.

Hours check: 6+6+7+6+7+6+6+6 = 50 (hub `data-hours-lessons="50"`); project 20 (hub `data-hours-project="20"`); total 70.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to PR1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `VERIFIER_RULES.md` §2, `plans/PR1-build-plan.md`
(this file), `plans/M7-build-plan.md` §7 and §8 (the autograder precedent for a portfolio problem), `plans/AP2-build-plan.md`
(the notation decisions this plan reuses, §2.3), `plans/FINAL-ARCHITECT-RULINGS.md`, `/Users/billyribeiro/.fanout/fixer-rules.md`
(binding defect classes), and `plans/E5-build-plan.md` (structure template). Study `course/modules/M/M7/` for the grader
layout and `course/templates/` for the four skeletons (`hub.html`, `lesson.html`, `project.html`, `studio.html`). Imitate
structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) where the
   lab is exact, or from unrounded floats with a stated tolerance, and rounded only at display. The rounding rule is stated
   where a rounded figure appears (precedent: `plans/AC4-build-plan.md`, CF1 L01 Remark 5.2). For PR1 this covers every
   weight, every Sharpe ratio, every turnover and every cost.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Every "shows", "confirms" or "equals" names the printed line that carries it. Precedent:
   M1 LESSON_TEXT_DEFECTS ("checked directly" with no lab behind it).
3. **Attribute nothing unread.** Only the registry keys in §7 may be cited, and only at paper level unless the builder has read
   the abstract (VERIFIER §2.1). No page, table, equation, coefficient, year or finding is typed from memory. The six sources
   are cited by key; what they find is not stated until the abstract is read (B4).
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "for each", "market structures", "the
   ranking", "robust", "optimal" are used only where a derivation, a finite check or a lab computes the claim. Scope of the
   unit (Q7): one period, long-only, budget-constrained allocators; the sample is a window of T past returns; the instance
   generator is the only data source; no transaction-cost model beyond the proportional one stated in §5.2.
5. **Define before use.** Each of the 6 concepts is defined once, with `<dfn id="def-<id>" data-concept="<id>">`, in its
   assigned lesson and never before it. Terms outside the 6 are defined at first use with a plain `<dfn>` and no
   `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`; E5 precedent): `turnover` (one-way turnover),
   `transaction cost`, `rebalancing`, `look-ahead`, `out-of-sample`, `net return`, `window`.
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions
   (A1, A2, ...) before the statement. The statements that must be stated this way:
   - **1/N result (L03):** A1 the N assets are identical in mean (μ = mι) and variance (Σ = σ²I, σ > 0); A2 no short sales
     are required (the common point is interior); conclusion: the mean-variance and minimum-variance weights are ι/N.
   - **Shrinkage lift (L04):** A1 S is symmetric positive semidefinite; A2 δ ∈ [0,1]; A3 target F = (tr S / N) I; conclusion:
     the smallest eigenvalue of (1-δ)S + δF is at least δ·tr(S)/N, and it is positive when δ > 0 and S ≠ 0.
   - **Black–Litterman posterior mean (L05):** A1 Gaussian prior μ ~ N(μ_eq, τS) with τ > 0 and S positive definite; A2 views
     q = Pμ + ε with ε ~ N(0, Ω), Ω positive definite diagonal; A3 S treated as known. Conclusion: the posterior mean in
     precision form. Both precisions are positive definite, so their sum is invertible without assuming P has full rank.
   - **Worst case over a box (L06):** A1 ε ≥ 0 componentwise; A2 the uncertainty set is the box |μ_i - μ̂_i| ≤ ε_i; conclusion:
     min over the box of μ'w equals μ̂'w - ε'|w|.
   - **Sharpe ratio (L07, L08):** the per-period convention is stated; no annualization is applied (Q11).
   The builder must derive each formula on the page. The planner gives the statements, not a source for the derivation.
7. **Grader rule.** Applies in full (autograder). See §5.5 and fixer-rules item 19: every exception type the page names, every
   condition, boundary and inequality direction gets its own isolated test; a correct implementation may raise any exception
   for an invalid input the page does not name.
8. **Money.** PR1 has no currency amounts in the curriculum entry. Cost rates are decimal fractions per unit of one-way
   turnover (for example 0.001 is 10 basis points), and the page states the conversion. If the spec ever adds a notional or a
   trade list in currency, every amount is an integer number of cents with largest-remainder rounding (Q8).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; KaTeX display lines are split where needed; no element forces the page wider than 360 px.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard (`tools/run_labs.py:51-59`, the M7 precedent `plans/M7-build-plan.md:262-265`).
11. **Basis explicit.** Every return, rate and Sharpe ratio states its period (one period = one month in the generated
    instance, labelled as a model unit), its convention (simple per-period returns, no annualization), and its source
    (SIMULATED, §6). Every cost rate states decimal per unit of one-way turnover.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A B- or C-graded
  claim names its published counter-evidence (BUILDER_RULES §2.5). The lesson on 1/N (L03) and the one on the ranking (L08)
  cite counter-evidence for each graded claim, or the claim stays ungraded (B4).
- Concepts: §1 table; `<dfn>` only for the 6 registered concepts, plus plain `<dfn>` for the other terms of §2.1 item 5. A
  `<a class="concept">` link is allowed for any of the 174 closure concepts (§4.1); no link for any concept outside the closure.
- Prerequisite links: `href="../../../concepts.html#<id>"` for closure concepts (for example `kkt-conditions`, M7;
  `covariance-matrix`, M4; `efficient-frontier`, AP2, unbuilt but in the closure). `href="Lnn.html#def-<id>"` for earlier
  PR1 lessons. A lesson never links a concept defined in a later lesson. The hub links no unbuilt page.
- Labs: code lives once in `tests/labs/PR1/lab-PR1-Lnn-1.py` (and `lab-PR1-project-1.py` to `-3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type an expected output. Lab ids match
  `lab-PR1-<page>-<n>` (`check_pages.py`, `check_lesson`). Standard library only (`fractions`, `math`, `random.Random(seed)`);
  seeded RNG only; no network; under 10 s in Pyodide; no warnings under `-W error`. No `data-files` attribute (no dataset is
  embedded; §6).
- SIMULATED label: on every lab, figure or project example that uses generated returns (L02, L07, L08, the project's
  rung 3 check and exemplars). Exact closed-form labs (L01, L03, L04, L05, L06) use illustrative numbers typed in the twin,
  labelled "illustrative inputs", not SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references
  in code comments (precedent: M1 "Convention (project Q5)").
- Banned strings (`tools/check_pages.py:58-72` `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` (the regex `\.\.\.` applies everywhere).
- Percent changes state the base and the direction. Growth rates and returns state the convention (simple, per period).
- A finite enumeration (L06 vertices, L08 seed count) is grade C with its basis named, not grade T (M1 L06 precedent).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent).
- Quiz explanations are read against their lesson (CF1 KNOWN 6 precedent).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered macros used by PR1 (`notation/notation.json`, `macros`): `\E` (line 5), `\Cov` (line 17), `\R` (line 25),
`\tr` (line 61), `\diag` (line 65), `\SR` (line 69, the Sharpe ratio, the AP2 precedent `plans/AP2-build-plan.md:115`).

Registered symbols and PR1's rule (`notation/notation.json`, `symbols`):

| Registered symbol | Registered meaning (locator) | PR1 rule |
|---|---|---|
| `T` | number of return observations (periods) in a sample (`notation.json:112`, module S1) | **Used with this meaning only.** T is the window length: the number of past returns on which an estimate is built. Consistent with S1. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF (M4) | Not used. |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (M4) | Not used. Risk aversion is written plain `\gamma` (local, defined in L01). |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` | AP1 | Not used. The riskless rate is not needed in PR1. |

Local symbols (allowed; `notation.json` `about` says letters conventionally local are defined per lesson where used):

| Symbol | Meaning (defined where first used) | Note |
|---|---|---|
| `N` | number of assets | local |
| `T` | window length (registered meaning above) | local use is the registered one |
| `H` | total number of simulated periods | not registered |
| `K` | number of rebalancing dates | not registered |
| `w`, `w_0` | weight vector; the initial holding (1/N, §5.2) | local |
| `\iota` | vector of ones | not registered (grep: absent). AP2 precedent: `\iota`, not `\mathbf{1}` (`plans/AP2-build-plan.md:203, 251`) |
| `\Sigma` | population covariance (assumed known in L05) | local |
| `S` | sample covariance with divisor T - 1 | local |
| `\hat\mu` | sample mean of the window | local |
| `\Sigma_\delta` | shrunk covariance `(1-\delta) S + \delta (\tr S / N) I` | local |
| `\delta` | shrinkage intensity in [0,1] | local (not the BLUEPRINT registered letter) |
| `\tau` | Black–Litterman scale of the prior covariance | not registered |
| `\mu_{\mathrm{eq}}` | equilibrium prior mean (reverse optimization) | **Do not write `\pi`** for the prior; `\pi` is the constant |
| `P`, `q`, `\Omega` | view matrix, view vector, view-error covariance | local |
| `\epsilon` | robust uncertainty radius | local; not `\varepsilon` in prose |
| `c` | proportional cost rate per unit of one-way turnover | local |

`NOTATION_REQUESTS: none.` The plan uses only local symbols and registered macros. `\iota`, `\Sigma`, `\tau`, `\Omega` and
`\delta` are not registered, and no registered symbol takes a new meaning.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2): Why it matters (at most 120 words, `check_pages.py:243`),
core content in Definition, Theorem, Proof, Example and Remark blocks, the inline lab, "Where the canon breaks", misconceptions
(at least 3, `check_pages.py:279`), a problem set with at least 3 problems in each of Mechanics, Proof, Empirical and Research
(each with `<details class="solution">`), a key-results table, and a quiz of 8 to 15 items (`check_pages.py:302`). The debate
brief is not required (no `debate` key, §0.1). Every lesson declares `data-hours` (6, 6, 7, 6, 7, 6, 6, 6 as in §1).

- **L01 `mean-variance-estimation-error`.** The mean-variance problem with the objective `(γ/2) w'Σw - μ'w` s.t. `ι'w = 1`,
  stated as a model, with its closed form without the long-only constraint (T, derivation, Assumption: Σ positive definite).
  The estimation error: the weights are a function of estimated inputs, and a perturbation of μ̂ moves them (T for the
  two-asset example, derivation by the implicit-function theorem of M2, `implicit-function-theorem`, in closure, or by the
  direct inverse). The lab prints the two weight vectors in `Fraction`. The word "estimation error" is defined here and in
  no other lesson. Canon breaks: the model assumes known inputs; the window length T is a design choice.
- **L02 `error-maximization`.** The optimizer's weights are a nonlinear function of the estimates. The statement that the
  optimizer tends to overweight assets with large positive estimation errors is an empirical and theoretical claim with
  published discussion (Michaud, `michaud1989markowitz`, paper level only, B4). Until the abstract is read, the claim is a
  naming sentence (no grade). The lab (curriculum lab, SIMULATED) prints the mean and spread of the unconstrained weights
  across seeded resamples and the weights from the true inputs. The lesson states only what the printed table shows
  (resample count and seed fixed in the twin). Canon breaks: resampling is one remedy and is not derived here.
- **L03 `equal-weight-portfolio`.** The 1/N portfolio is `w = ι/N` and uses no estimate. Theorem (T, Assumptions A1 and A2 of
  §2.1 item 6): under identical means and variances and zero covariances the mean-variance and minimum-variance weights are
  `ι/N`. Outside those assumptions the two differ, with the gap in the lab. The literature claim that 1/N is hard to beat
  out of sample (DeMiguel et al., `demiguel2007optimal`) is graded B only after the abstract is read and the counter-evidence
  named (B4). Canon breaks: the theorem's hypotheses are the whole content; a practitioner's 1/N with unequal risk is not
  covered.
- **L04 `covariance-shrinkage`.** The sample covariance `S` of T < N observations is singular (T-1 ≤ N-1 < N). The shrunk
  covariance `Σ_δ = (1-δ)S + δ(tr S/N)I` is positive definite for δ > 0 and S ≠ 0 (Theorem T, Assumptions of §2.1 item 6;
  the proof uses that the target is a multiple of the identity, so the eigenvalues combine in closed form). The intensity δ
  is given in this unit (Q5). The Ledoit–Wolf papers (`ledoit2004well`, `ledoit2017nonlinear`) are cited at paper level
  only; their intensity formulas are not stated here because the planner did not read them. The lesson's Remark names the
  penalty view (ridge and lasso are outside the closure, §4) only in plain prose. Canon breaks: the target is one choice;
  a different target changes the answer.
- **L05 `black-litterman-model`.** Reverse optimization sets `μ_eq = γ S w_mkt` as a model definition (not a result; no
  grade beyond "definition"). The posterior mean in precision form (Theorem T, Gaussian conjugate update, Assumptions A1 to
  A3 of §2.1 item 6) is `μ_BL = [(τS)^{-1} + P'Ω^{-1}P]^{-1}[(τS)^{-1} μ_eq + P'Ω^{-1} q]`. The allocator of §5.2 uses
  `μ_BL` as the mean and `S` as the covariance in the long-only mean-variance problem (a model choice stated on the page;
  Q9). The lab checks the precision form against a second algebraic form in `Fraction`. Canon breaks: the views are given
  and their error covariance is a modelling choice; the prior is an equilibrium assumption.
- **L06 `robust-portfolio-optimization`.** The worst case over the box `|μ_i - μ̂_i| ≤ ε_i` of the linear objective `μ'w` is
  `μ̂'w - ε'|w|` (Theorem T, Assumptions A1 and A2 of §2.1 item 6; the minimizing vertex is `μ_i = μ̂_i - ε_i sign(w_i)`).
  For long-only w this is `μ̂'w - ε'w`. The lab checks the four vertices of a two-asset box and reports the minimum; a
  finite enumeration is grade C with the basis named (§2.2). The robust allocator is a stretch item (§5.1 rung 4), not
  graded (Q10). Canon breaks: a box is one uncertainty set; the radius is a choice; the robust allocator is not optimal in
  every sense.
- **L07 `transaction-cost` and out-of-sample evaluation (no concept).** The rolling protocol: at rebalancing date `t` the
  allocator sees only the returns `r_{t-T}` to `r_{t-1}` (no look-ahead, the rule of §5.2). The one-way turnover
  `τ_t = Σ_i |w_{t,i} - w_{t-1,i}|` (not halved), the cost `c τ_t`, the gross return `w_t' r_t`, and the net return. The
  per-period Sharpe ratio uses the registered macro `\SR` and the sample standard deviation with divisor K - 1. The lab
  runs one seed with the correct timing and with a planted look-ahead; both net Sharpe ratios are printed. The lesson says
  that one seed is one run. Canon breaks: no drift in holdings (the previous target is used, §5.2); one cost rate; one
  period.
- **L08 Ranking the allocators: evidence and limits (no concept).** The difference of two Sharpe ratios on the same
  returns has a standard error under a named assumption (the i.i.d. case, `sharpe-ratio-standard-error-iid`, S1, in closure).
  The lesson applies that formula to the ranking. Two sides, each graded only after the abstract is read: "1/N is hard to
  beat" (`demiguel2007optimal`) and "shrinkage improves out-of-sample risk" (`ledoit2017nonlinear`). The lab reports a
  count over seeds 0 to 29 under the stated model; it is grade C with that basis and says that the count is about the
  generator, not about markets. Canon breaks: the instance generator fixes the answer's direction; a finite set of seeds
  is a finite enumeration.

Lesson-level constraints:

- Each lesson's "Where the canon breaks" names at least one model limit and what changes without it.
- No lesson uses a term from PR2 (risk parity, risk budgeting, volatility targeting) or PR4 (value-at-risk, expected
  shortfall) as a concept. These are outside the closure (§4.2, D6 and D7).

---

## 4. DAG problems (concepts that natural PR1 content would use outside the closure)

### 4.1 Closure concepts PR1 links (in closure; a link is allowed)

The closure of PR1 is {AP2, CS1, E1, E3, M1, M2, M3, M4, M7, P0.1, S0, S1, S2} (§0.1). The concepts natural PR1 content
links, with the owner module and built status:

| Concept (id) | Owner (in closure) | Built? | Used in |
|---|---|---|---|
| `mean-variance-optimization`, `quadratic-programming`, `kkt-conditions`, `lagrange-multiplier`, `linear-portfolio-constraints`, `convex-set`, `convex-function`, `lagrangian-duality` | M7 | built | L01, L03, the project |
| `covariance-matrix`, `variance`, `correlation`, `expectation`, `multivariate-normal`, `law-of-large-numbers`, `central-limit-theorem`, `normal-distribution` | M4 | built | L01, L02, L04, L05 |
| `positive-semidefinite-matrix`, `eigendecomposition`, `spectral-theorem`, `eigenvalue-clipping`, `nearest-correlation-matrix`, `orthogonal-projection` | M3 | built | L04 |
| `implicit-function-theorem`, `derivative`, `gradient`, `hessian` | M2 | built | L01 (derivation) |
| `efficient-frontier`, `minimum-variance-portfolio`, `tangency-portfolio`, `linear-factor-model` | AP2 | unbuilt (B3) | L01, L03 (prose context only) |
| `sharpe-ratio`, `sharpe-ratio-standard-error-iid`, `bootstrap`, `bayesian-inference`, `estimator-bias-variance` | S1 | unbuilt | L02, L07, L08 |
| `robust-statistics` | S0 | unbuilt | not used unless needed |
| `ols-estimator`, `omitted-variable-bias` | S2 | unbuilt | not used |
| `python-function-scope`, `python-data-structures`, `unit-test`, `type-hints`, `numpy-vectorization`, `simple-return`, `log-return` | CS1 | unbuilt | the grader and the simple-return convention (§2.1 item 11) |
| `evidence-grade`, `citation-registry`, `robustness-check`, `replication`, `project-ladder` | P0.1 | unbuilt | the reading list and the rubric |
| `exponential-and-logarithm`, `present-value`, `discount-factor` | M1, E1 | built | not needed |

Unbuilt modules' concepts are linked through `concepts.html` anchors only (B3).

### 4.2 Outside concepts and resolutions (rows the architect confirms; Q13)

| Ref | Concept (owner, outside closure) | Where natural PR1 content would use it | Resolution in this plan |
|---|---|---|---|
| D1 | `backtest-cost-model` (QR2), `implementation-shortfall`, `square-root-impact-law`, `efficient-execution-frontier` (MS3) | the cost model of L07 | Plain prose: "proportional cost per unit of one-way turnover". No link, no `<dfn>` with `data-concept`. |
| D2 | `ridge-regression`, `lasso` (QR3) | the penalty view of shrinkage (L04 Remark) | Plain prose, no link, no name of the method beyond "a penalty". |
| D3 | `cholesky-decomposition`, `condition-number` (M8) | numerical solution of the QP and the ill-conditioning of S (L01, L02 and the project) | Plain prose, no link. The reference solver uses no Cholesky (§5.5); the alternatives may. |
| D4 | `empirical-bayes-shrinkage` (S7), `bayesian-replication-shrinkage` (F5) | the motivation of shrinkage in L04 and L05 | Not used as terms. The Black–Litterman Bayesian reading uses `bayesian-inference` (S1, in closure). |
| D5 | `backtest-overfitting`, `probability-of-backtest-overfitting`, `deflated-sharpe-ratio` (S7) | selection by ranking in L08 | Plain prose: "selection on the same data". No link. |
| D6 | `risk-parity`, `risk-budgeting`, `volatility-targeting` (PR2) | none in PR1 (PR2 requires PR1, `04-quant.yaml:281`) | **Must not be used in PR1.** A use is a DAG defect (`check_dag.py` only sees links; the verifier reads for the names). |
| D7 | `value-at-risk`, `expected-shortfall` (PR4) | none | Not used. |
| D8 | Atlas components (A-series, for example A11) | none (no Atlas, §8) | Not used. |
| D9 | `stochastic-discount-factor` (AP1) | none | Not used. |

No missing prerequisite was found: every concept natural PR1 content needs is either in the closure (§4.1) or a plain-prose
term (`turnover`, `transaction cost`, `rebalancing`, `look-ahead`, `out-of-sample`, `net return`, `window`). These are not
curriculum concepts, so they are defined in prose with a plain `<dfn>` (§2.1 item 5). No DAG_DEFECT is raised. Each row
needs the architect's confirmation (Q13).

`tools/check_dag.py` checks linked uses only (its docstring); an unlinked use of D1 to D9 passes the tool, so the verifier
reads every lesson and the project for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): autograder and rubric, ladder, spec, hours, rubric, grader design

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` requires the rung order)

BUILDER_RULES §5.1 with tier M: rungs 1 and 2 are kept to the minimum (BLUEPRINT §4; `plans/M7-build-plan.md` pattern).

1. **Rung 1, worked example** (`lab-PR1-project-1`, illustrative inputs): one fully solved computation of the 1/N weights and
   the minimum-variance weights on a fixed three-asset window of six returns, in `Fraction`. Each step carries a "why"
   annotation. Two pages of text at most.
2. **Rung 2, completion** (`lab-PR1-project-2`, `class="lab completion"`, illustrative inputs): the one-way turnover line and
   the cost line of the worked window are replaced by `___`. Graded instantly. The twin is the completed solution; every page
   line equals the twin line or contains a blank (`tools/run_labs.py` completion rule; M7 precedent).
   `tools/check_projects.py:90` requires a completion lab or a quiz for rung 2.
3. **Rung 3, independent project** (graded: autograder and rubric). Builder: `allocators.py` (the student's unit-local file,
   §5.5.1) and `report.md`. `lab-PR1-project-3` is the rung-3 check: it runs the reference on seed 3 and prints the table the
   report should show (the same pattern as the M7 rung-3 check, `plans/M7-build-plan.md:176`; Builder E confirms the M7 twin
   and copies its mechanism).
4. **Rung 4, stretch** (optional, not graded): (a) add the box-robust allocator of L06 and report its out-of-sample
   Sharpe ratio beside the five; (b) a Ledoit–Wolf intensity only after the builder has read the paper (B4); (c) an
   out-of-sample run on the embedded FX spot panel with the spot-only caveat (§6, Q7).

### 5.2 Spec (`dl.spec`; `tools/check_projects.py:34` requires the terms context, inputs, required outputs, constraints and grading)

- **Context.** A portfolio analyst compares five ways to set long-only weights for a multi-asset portfolio and must say which
  one held up out of sample, and why the ranking can be trusted or not. The analyst gets the same returns for all five.
- **Inputs.** One generated return window per seed (SIMULATED, §6) with the following keys from `make_instance(seed)` (§5.5.1):
  `returns` (H rows, N columns, one row per period), `names`, `window` (T = 60), `gamma` (risk aversion, a positive number),
  `delta` (shrinkage intensity in [0, 1]), `tau` (positive), `w_mkt` (the market weights, positive, sum 1), `P` (k by N), `q`
  (length k), `omega` (k positive diagonal values), `cost_rate` (decimal per unit of one-way turnover, non-negative). Every
  number is a period number; there is no annualization.
- **Required outputs.**
  - `allocators.py` exposing the functions of §5.5.1 with the stated names and signatures.
  - `report.md`: at most two pages. It ranks the five allocators by the out-of-sample per-period net Sharpe ratio on the
    run for seed 3, states the standard error of each adjacent difference under a named assumption, names the model limits,
    and gives the counter-evidence for each claim graded B or C.
- **Definitions the spec must state (each is also a mutant's violated rule, §5.5.3).**
  - Sample mean `μ̂ = (1/T) Σ_s r_s` and sample covariance `S = (1/(T-1)) Σ_s (r_s - μ̂)(r_s - μ̂)'` over the window.
  - Equal weight: `w = ι/N`.
  - Sample mean-variance: minimize `(γ/2) w'Sw - μ̂'w` s.t. `ι'w = 1`, `w ≥ 0`.
  - Shrinkage mean-variance: the same problem with `Σ_δ = (1-δ)S + δ (tr S / N) I` in place of `S`.
  - Minimum variance: minimize `w'Sw` s.t. `ι'w = 1`, `w ≥ 0`.
  - Black–Litterman: `μ_eq = γ S w_mkt`; `μ_BL` as in L05 with `τ`, `P`, `q`, `omega`; then the sample mean-variance problem with `μ_BL` in place of `μ̂`, covariance `S`.
  - Rebalancing: at each date `t = T+1, ..., H` (K = H - T dates) the allocator sees only rows `t-T` to `t-1`, never row `t`.
  - Holdings: the initial holding is `w_0 = ι/N`, charged at the first rebalance. The previous target is used for turnover (no drift).
  - One-way turnover `τ_t = Σ_i |w_{t,i} - w_{t-1,i}|` (not halved). Cost `c_t = cost_rate × τ_t`.
  - Gross return `g_t = w_t' r_t`; net return `n_t = g_t - c_t`.
  - Per-period Sharpe ratio: `mean(n_t) / sd(n_t)` with the sample standard deviation (divisor K - 1). No annualization.
  - Long-only constraints apply to all five allocators. All weights are returned as lists of floats with N entries.
- **Constraints.**
  - Every number in the report is computed from unrounded values; state the rounding rule (two decimals for Sharpe ratios,
    four for weights).
  - Every number in the report cites the allocator, the seed and the period range it came from.
  - No claim about a series beyond its generator (the report's claims are about the generated model).
  - Standard library only. NumPy is not used by the reference; a student may use it locally.
  - No real data is used (§6); the FX stretch is optional and labelled.
- **Failure behaviour (the only conditions named; §5.5.2).**
  - A window with T ≤ N raises `ValueError` in `sample_mv`, `min_variance` and `black_litterman`, which use S. In
    `shrinkage_mv` it raises `ValueError` only when `delta = 0`.
  - `delta` outside [0, 1] raises `ValueError`.
  - A window that is ragged (rows of unequal length), or contains a non-finite value, raises `ValueError`.
  - A negative `cost_rate` raises `ValueError`.
  - Any other invalid input may raise any exception that carries a message.
- **Grading.** Both: the autograder (`grader/test_project.py`) checks the allocators and the engine, and the rubric (§5.4)
  grades `report.md`. The spec's grading entry names both the autograder and the rubric (`tools/check_projects.py:41-55`
  requires both words for "both").
- **Reading list.** `ol.reading-list` cites `michaud1989markowitz`, `chopra1993effect`, `demiguel2007optimal`,
  `ledoit2004well`, `ledoit2017nonlinear`, `black1992global` (registry keys only; §7). Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 20 h; every row needs a one-line rationale; `tools/check_projects.py:90-120` region)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate the three-asset window) | 1 | One solved window, annotated line by line |
| Rung 2, completion problem (fill the turnover and cost lines, run the instant check) | 1 | Two lines with blanks, then the lab's own check |
| Core: the five allocators, the QP solver, the shrinkage and Black–Litterman formulas | 6 | Main code; the tests of §5.5.2 check each |
| Out-of-sample engine: rolling windows, timing, turnover, costs, net returns | 3 | The timing rule is the most common error; the engine test checks it |
| Run the suite and the self-check against the reference on seed 3 | 2 | `pytest` locally and the same suite in Pyodide |
| Report: ranking, standard errors, model limits, counter-evidence | 5 | Two pages, every number cited with seed and period range |
| Self-assessment against the two exemplars | 2 | Score the report with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **20** | Equals `data-hours-project` on the hub |

### 5.4 Rubric (`table.rubric#rubric`, `tools/check_projects.py:58-73`)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to
1 (the tool counts `td` cells; `rubric_problems`, `tools/check_projects.py:58-73`). Every level descriptor is observable.
The builder writes levels 3 and 2 with the same observable form.

1. **Inputs and estimation error.** Level 4: states, for each allocator, which inputs come from the window and which are
   given (`delta`, `tau`, `w_mkt`, views, `cost_rate`), and the window length, and computes the change in weights from one
   perturbed estimate. Level 1: "uses the data".
2. **Out-of-sample protocol.** Level 4: states the rebalancing rule, the first holding and the drift convention, and shows the
   date range of the window used for the first and the last rebalance. Level 1: "splits the data sensibly".
3. **Costs and turnover.** Level 4: defines one-way turnover with absolute values and the cost rate in decimal and in basis
   points, and reports gross and net Sharpe ratios side by side. Level 1: "considers costs".
4. **Ranking and uncertainty.** Level 4: ranks the five allocators by the per-period net Sharpe ratio and gives the standard
   error of each adjacent difference under a named assumption (`sharpe-ratio-standard-error-iid`). Level 1: "ranks them".
5. **Limits and evidence.** Level 4: names the model limits used in the ranking (generated returns, fixed `delta`, the window
   length, one cost rate) and gives counter-evidence for each claim graded B or C, with its key. Level 1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written reports on the seed-3 run
of the reference, annotated with the descriptors each passage meets or misses. Self-assessment form (`section.rubric-self`,
`data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in M1 and E1). The page shows where the student's
scores diverge from the exemplar scores. The exemplar numbers come from the reference run (not typed by hand); the rounding
rule is stated.

Calibration (FINAL-ARCHITECT-RULINGS 15 and 23, `plans/FINAL-ARCHITECT-RULINGS.md:35-37`, `:59-61`): a separate scorer who
never opens the project page scores the exemplars' prose, using a stripping script that drops annotations, verdict lines and
`data-score(s)` attributes, and the verifier compares the blind scores with the official ones within one level per criterion.
Adversarial question bank: not required (Q6).

### 5.5 Grader design (Builder E; `grading: both`, autograder part)

Frozen interfaces (Q4; M7 Q4 precedent). Names and signatures are fixed by this plan and may not change without a
CONTRACT_CHANGE_REQUEST to the architect.

#### 5.5.1 Files and interfaces

- `course/modules/PR/PR1/grader/instance.py`: `make_instance(seed: int) -> dict[str, Any]`. Deterministic: the same seed gives
  the same instance. It generates `N` in {4, 5, 6}, `H = 120` periods (so `T = 60`, `K = 60`), a positive definite covariance
  of the form `A'A/N + ε I` (scaled to monthly volatilities in a stated range), a drift vector, `gamma` in [2, 5], `delta` in
  [0.2, 0.8], `tau` in [0.02, 0.1], `w_mkt` positive with sum 1, `P` and `q` for one or two views, `omega` positive, and
  `cost_rate` in {0.0005, 0.001, 0.002}. Every instance is validated inside the generator (the window's sample covariance has
  full rank; the spec's ranges hold). The docstring says **SIMULATED: generated inputs, not market data.** Seeds 0 to 49 change
  the answers (which constraints bind, which weights are zero), not only the labels (BUILDER_RULES §5.3).
- `course/modules/PR/PR1/grader/reference.py`: the full solution (the reference). It passes every test for seeds 0 to 49 under
  `tools/run_graders.py --unit PR1 --seeds 0-49`. It uses an active-set search for the long-only QPs, with an exact KKT check
  of each returned solution, and float arithmetic with the tolerances of §5.5.4.
- `course/modules/PR/PR1/grader/starter.py`: stubs raising `NotImplementedError`. The starter must fail the suite
  (`tools/run_graders.py` checks this).
- `course/modules/PR/PR1/grader/test_project.py`: the pytest suite (§5.5.2).
- The student's file is `allocators.py` (unit-local, not an Atlas path; no `atlas:` key, §8). Its functions:
  - `equal_weight(n: int) -> list[float]`
  - `sample_mv(window: list[list[float]], gamma: float) -> list[float]`
  - `shrinkage_mv(window: list[list[float]], gamma: float, delta: float) -> list[float]`
  - `black_litterman(window: list[list[float]], w_mkt: list[float], tau: float, P: list[list[float]], q: list[float], omega: list[float], gamma: float) -> list[float]`
  - `min_variance(window: list[list[float]]) -> list[float]`
  - `run_backtest(instance: dict[str, Any], method: str) -> dict[str, Any]`, where `method` is one of `"equal_weight"`,
    `"sample_mv"`, `"shrinkage_mv"`, `"black_litterman"`, `"min_variance"`, and the returned dict has the keys `weights`
    (K lists), `turnover` (K floats), `gross` (K floats), `net` (K floats) and `sharpe` (a float).
- `data-solution="allocators.py"` in the grader panel. The panel carries `data-unit="PR1"`, `data-grader="grader/"`,
  `data-suite="test_project.py"`, `data-support="instance.py"`, `data-solution="allocators.py"`, `data-starter="starter.py"`
  (`tools/check_projects.py:122-135` for the required attributes and files; M7 §7.5 pattern). `data-support` must be present
  (T4, §11).

Grader panel HTML (for Builder E):

```html
<section class="grader-panel" id="grader" data-unit="PR1" data-grader="grader/" data-suite="test_project.py"
         data-support="instance.py" data-solution="allocators.py" data-starter="starter.py"></section>
```

#### 5.5.2 Tests (property and number checks; one isolated test per named condition; both directions)

Each test finishes in under 5 s in Pyodide and the suite in under 60 s (BUILDER_RULES §5.3.4). The timing of the suite is
measured by Builder E before the verifier starts; a Fraction-based solver that exceeds the limit is replaced (Q16).

| Test | Property or number checked | Spec item |
|---|---|---|
| `test_instance_valid_and_varies` | every seed in 0 to 49 gives a valid instance; the instances differ in N and in `Σ` | §5.5.1 |
| `test_budget_and_long_only` | for all five methods, weights sum to 1 (tolerance 1e-9) and are ≥ 0 (tolerance 1e-12) | §5.2 constraints |
| `test_equal_weight_exact` | `equal_weight(n)` equals `1/n` in every entry | §5.2 definition |
| `test_sample_covariance_convention` | `S` of a fixed 3-by-2 window equals the hand value with divisor T - 1 (number) | §5.2 definition |
| `test_shrinkage_formula_and_intensity` | at `delta = 0` the shrunk matrix is `S`; at `delta = 1` it is `(tr S / N) I`; at an intermediate `delta` the fixed example's value matches | §5.2 definition |
| `test_shrinkage_min_eigenvalue` | the smallest eigenvalue of `Σ_δ` is at least `delta · tr(S)/N` (tolerance 1e-12 relative) | L04 Theorem |
| `test_min_variance_kkt_residual` | the KKT residual of the minimum-variance solution is below 1e-8 | §5.2 definition, §5.5.4 |
| `test_sample_mv_kkt` | the KKT residual of the sample mean-variance solution is below 1e-8, with multipliers of the bounds ≥ 0 | §5.2 definition |
| `test_black_litterman_precision_form` | `μ_BL` equals the precision-form value computed independently in the test, at `tau != 1` on each seed | L05 Theorem |
| `test_turnover_zero_when_unchanged` | turnover is 0 when the new weights equal the previous target | §5.2 turnover |
| `test_turnover_swap_example` | moving 0.2 of weight from one asset to another gives one-way turnover 0.4 (not 0, not 0.2) | §5.2 turnover |
| `test_costs_reduce_net_return` | `net_t = gross_t - cost_rate · turnover_t` on every date (tolerance 1e-12) | §5.2 net return |
| `test_no_lookahead_perturbation` | changing the realized return at date `t` leaves `weights_t` unchanged for every `t`, for every method | §5.2 rebalancing |
| `test_sharpe_formula` | `sharpe` equals mean/sd of the net returns with divisor K - 1 on a fixed series (number) | §5.2 Sharpe |
| `test_weights_match_reference_on_each_seed` | every method's weights on each seed 0 to 49 equal the reference weights (tolerance 1e-7); the optimum is unique because the QP's matrix is positive definite | §5.5.4 |
| `test_error_window_too_short_raises` | `T = N` raises `ValueError` in `sample_mv`, `min_variance`, `black_litterman`; `T = N + 1` is accepted; `shrinkage_mv` raises at `delta = 0` with `T ≤ N` and is accepted at `delta > 0` | §5.2 failure behaviour |
| `test_error_delta_range_raises` | `delta = -1e-9` and `delta = 1 + 1e-9` raise `ValueError`; `delta = 0` and `delta = 1` are accepted | §5.2 failure behaviour |
| `test_error_ragged_or_nonfinite_raises` | a ragged window and a window with a NaN each raise `ValueError` | §5.2 failure behaviour |
| `test_error_negative_cost_raises` | `cost_rate = -1e-12` raises `ValueError`; `cost_rate = 0` is accepted | §5.2 failure behaviour |
| `test_other_invalid_inputs_raise_something` | other invalid inputs (for example an unknown method name) raise any exception with a message; a silent wrong answer fails | §5.5.5 |

Failure messages name the violated property and give a hint at the concept (for example "the KKT residual of the minimum-
variance solution is above tolerance: check the sign of the multiplier of the budget constraint"). They never print the
expected value. `__tracebackhide__` is set in the helpers so a failing check does not print the expected value (fixer-rules
item 19).

#### 5.5.3 Ten student-error mutants (`ledgers/PR1/mutants/`; each a single-change copy of the reference)

The first docstring line of each mutant names the student error (VERIFIER §2.6). Each mutant violates a rule that §5.2 states,
so each is a student error and not an equivalent (FINAL-ARCHITECT-RULINGS 9, `plans/FINAL-ARCHITECT-RULINGS.md:18-20`).
`tools/mutate_graders.py --unit PR1 --seeds 0-9` must kill all ten.

| ID | File | Student error (first docstring line) | Spec rule violated | Planned killing test |
|---|---|---|---|---|
| M01 | `m01_one_over_n_minus_1.py` | "Equal weight divides by N - 1, so the weights do not sum to one." | budget `ι'w = 1` | `test_equal_weight_exact` |
| M02 | `m02_sample_cov_divisor_t.py` | "Sample covariance divides by T instead of T - 1." | §5.2 definition of `S` | `test_sample_covariance_convention` |
| M03 | `m03_lookahead_window.py` | "The window for date t includes the return realized at t (one-period look-ahead)." | rebalancing rule | `test_no_lookahead_perturbation` |
| M04 | `m04_turnover_on_levels.py` | "Turnover is the sum of absolute weights, not of their changes." | one-way turnover definition | `test_turnover_zero_when_unchanged` |
| M05 | `m05_signed_turnover.py` | "Turnover sums signed changes, so swapping weight between two assets costs nothing." | one-way turnover definition with absolute values | `test_turnover_swap_example` |
| M06 | `m06_shrinkage_swapped.py` | "The shrinkage weights are reversed: the sample covariance gets delta and the target gets 1 - delta." | definition of `Σ_δ` | `test_shrinkage_formula_and_intensity` |
| M07 | `m07_bl_no_tau.py` | "The Black–Litterman prior precision uses S instead of tau S, ignoring the scale tau." | L05 formula with `τ` | `test_black_litterman_precision_form` |
| M08 | `m08_min_var_sigma_not_inverse.py` | "Minimum variance uses S applied to the ones vector instead of its inverse, so the first-order condition fails." | definition of minimum variance and KKT | `test_min_variance_kkt_residual` |
| M09 | `m09_short_sales_in_sample_mv.py` | "Sample mean-variance drops the long-only constraint, so short positions appear." | long-only constraint | `test_budget_and_long_only` |
| M10 | `m10_hardcoded_seed0.py` | "The allocator returns the reference weights of seed 0 for every seed." | the answers depend on the seed (§5.5.1) | `test_weights_match_reference_on_each_seed` |

#### 5.5.4 Numeric policy and tolerances (stated on the page; FINAL-ARCHITECT-RULINGS 22, `plans/FINAL-ARCHITECT-RULINGS.md:55-58`)

- The QP solutions are unique because `S` (and `Σ_δ`, and `S` plus the Black–Litterman terms) is positive definite (A1
  of the spec). Comparisons with the reference use the tolerances of §5.2 and §5.5.2 and no looser ones.
- Float arithmetic in the reference; the labs use `Fraction` where the numbers are illustrative. The tolerances are: weight
  sums 1e-9; long-only 1e-12; KKT residual 1e-8 after scaling by the largest diagonal of `S`; weight match with the reference
  1e-7; Sharpe formula 1e-12 relative.
- Any mutant that differs from the reference only inside a stated tolerance is an equivalent and goes to `ledgers/PR1/equivalent/`
  with a README proof (FINAL-ARCHITECT-RULINGS 9 and 25). None is planned.

#### 5.5.5 Exception and acceptance rules (binding; M7 §7.4 precedent)

1. A test demands a specific exception type only for a condition the page names (§5.2 failure behaviour). For every other
   invalid case the suite accepts any exception that carries a message, and fails only on a silent wrong answer.
2. **Five alternative correct implementations must pass seeds 0 to 49** (FINAL-ARCHITECT-RULINGS 10, `plans/FINAL-ARCHITECT-RULINGS.md:21-22`).
   They are verifier-written, stored under `ledgers/PR1/alternatives/alt_1.py` to `alt_5.py` (never under `course/`, which
   `deployment` excludes, BLUEPRINT §7 lines 400-401), and run by a verifier script under `ledgers/PR1/scripts/`
   (`tools/run_graders.py` runs only the reference, §11.2). The five, each a different method:
   - alt_1: active-set enumeration in `fractions.Fraction`, with an exact KKT check. (If it is too slow for 50 seeds, `Fraction`
     is used only for the final KKT check, and a window of seeds 0 to 9 needs the architect's approval (Q16); this is not
     assumed.)
   - alt_2: projected gradient on the simplex-like set, returning only after an exact KKT check, falling back to an active-set
     search otherwise (the FINAL-ARCHITECT-RULINGS 19 pattern, `plans/FINAL-ARCHITECT-RULINGS.md:45-48`).
   - alt_3: cyclic coordinate descent on the bound-constrained QP with the same KKT check.
   - alt_4: log-barrier interior point (Newton steps) for the long-only QP, with a KKT check.
   - alt_5: primal active-set method with Cholesky solves of the reduced KKT system.
   Alternatives may compute `S` with a different algorithm (two-pass or Welford), which must agree on the tests.
3. Mutants: §5.5.3, exactly ten, each in `ledgers/PR1/mutants/`. Every mutant must fail at least one test (killed).
4. Dual mode. The identical suite runs in Pyodide and under local pytest (`--assert=plain -W error`). The suite is stdlib
   only, so no `data-packages` attribute is needed (M7 §7.4 item 4).

---

## 6. Real-data policy (B2 applies)

- **Embedded (redistributable, grant quoted):** `fx_daily`, `fx_monthly`, `ust_daily` (`tools/data_sources.yaml:19-52`,
  `:53-90`, `:91-118`). Their licence sentences are quoted at `tools/data_sources.yaml:23-26`, `:57-60` and `:95-98`
  (the Board's public-domain sentence; the licence page is `https://www.federalreserve.gov/disclaimer.htm`).
- **Not embedded:** an equity return series, a multi-asset return panel with total returns, or any series that a PR1 lab or the
  project reads as returns. `tools/data_sources.yaml:119-136` (`rejected:`) lists the French library and Open Source Asset
  Pricing, both not cleared.
- **The FX spot panel (optional stretch only, Q7).** The `fx_daily` series give six spot rates (AUD, CAD, CHF, EUR, GBP, JPY,
  `tools/data_sources.yaml:44-51`). Their note states that these are spot rates only and that a currency position's return
  also earns an interest differential the series do not contain (`tools/data_sources.yaml:28-30`). A stretch using them must
  say so on the page and must not be graded or called a market return.
- **Honest-pending note** (on the project page and on L02, L07 and L08): "No redistributable return series is embedded for
  this unit. Every return in the labs and the project is generated from a seeded model and labelled SIMULATED."
- **DATA_REQUESTS (for the architect; the planner names no source or licence from memory):** an equity or multi-asset total-
  return series with a quoted reuse grant (BUILDER_RULES §6.6 steps 1 to 5: source URL, series identifier, the quoted licence
  sentence, the licence page, and the transform). The BLUEPRINT §5.3 candidates are not cleared sources and must be checked
  before any use.
- No `data-files` attribute on any lab. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`; all six read by the planner)

| Key | Record (as read) | Status | Use in PR1 |
|---|---|---|---|
| `michaud1989markowitz` | Michaud, "The Markowitz Optimization Enigma: Is 'Optimized' Optimal?", FAJ, volume 45, issue 1, year 1989, DOI 10.2469/faj.v45.n1.31 (`references/references.json:17256`) | verified, `used_by: ["PR1"]`, source string matches `04-quant.yaml:263` | L02 (error maximization, paper level, B4); reading list |
| `chopra1993effect` | Chopra & Ziemba, "The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice", JPM, volume 19, issue 2, year 1993, DOI 10.3905/jpm.1993.409440 (`references/references.json:5313`) | verified, `used_by: ["PR1"]`, matches `04-quant.yaml:264` | L01 and L02 (input errors, paper level, B4); reading list |
| `demiguel2007optimal` | DeMiguel, Garlappi & Uppal, "Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?", RFS, volume 22, issue 5, `years` [2007, 2009], `print_year` 2009, DOI 10.1093/rfs/hhm075 (`references/references.json:6730`) | verified, `used_by: ["PR1"]`, matches `04-quant.yaml:265` (print year) | L03 and L08 (B, counter-evidence needed, B4); reading list. Year not typed in prose (Q14) |
| `ledoit2004well` | Ledoit & Wolf, "A well-conditioned estimator for large-dimensional covariance matrices", JMVA, volume 88, issue 2, year 2004, DOI 10.1016/s0047-259x(03)00096-4 (`references/references.json:15402`) | verified, `used_by: ["PR1"]`, matches `04-quant.yaml:266` | L04 (paper level); reading list |
| `ledoit2017nonlinear` | Ledoit & Wolf, RFS, volume 30, issue 12, year 2017, DOI 10.1093/rfs/hhx052 (`references/references.json:15482`). The registry title differs from the curriculum string, which has no title; do not type a title | verified, `used_by: ["PR1"]`, matches `04-quant.yaml:267` | L04 Remark and L08 (B, counter-evidence needed, B4); reading list |
| `black1992global` | Black & Litterman, "Global Portfolio Optimization", FAJ, volume 48, issue 5, year 1992, DOI 10.2469/faj.v48.n5.28 (`references/references.json:3010`) | verified, `used_by: ["PR1"]`, matches `04-quant.yaml:268` | L05 (paper level); reading list |

Registry rule: `tools/check_pages.py` and `tools/check_projects.py` accept only keys whose `status` is `verified`
(`tools/coursekit.py` `registry_keys`). A key is cited by its record only; the builder never types a title, year, author
list, page or coefficient from memory.

Not curriculum-listed, not cited by default: `markowitz1952portfolio` (`references/references.json:16544`, `used_by: ["AP2"]`)
for the mean-variance origin (Q10); `efron1979bootstrap` (`used_by: ["S1"]`) for the resampling of L02 (not needed; Q10).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Literature on Bayes–Stein shrinkage of expected returns (lead only; no author, year or title typed)", year: "not typed", title: "not typed", venue: "not typed", needed_for: "L05 or L04 counter-evidence for a B-graded claim about shrinking expected returns", confidence: "the need is certain; no record identified by this planner"}
- {doi: null, authors: "Literature on the sensitivity of mean-variance weights to expected-return errors (lead only)", year: "not typed", title: "not typed", venue: "not typed", needed_for: "L01 or L02 counter-evidence for a B-graded claim about estimation error", confidence: "the need is certain; no record identified by this planner"}
- {doi: null, authors: "Literature on out-of-sample evaluation of Black–Litterman allocations (lead only)", year: "not typed", title: "not typed", venue: "not typed", needed_for: "L05 two-sided treatment of a B-graded claim", confidence: "the need is certain; no record identified by this planner"}
- {doi: null, authors: "Literature on the critique of 1/N and of optimized portfolios (lead only)", year: "not typed", title: "not typed", venue: "not typed", needed_for: "L03 and L08 two-sided treatment; the counter-evidence named for DeMiguel et al. (B4)", confidence: "the need is certain; no record identified by this planner"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN or an allow-listed issuer page). Until then the lessons
teach the models by derivation and no empirical attribution beyond the six keys, and each empirical sentence is graded C at most
with its basis named, or is removed.

### 7.3 DATA_REQUESTS

See §6. Only if the architect wants real return data: one request per source, with the fields of BUILDER_RULES §6.6.

---

## 8. Atlas milestone

None. No Atlas entry names PR1 (§0.1, computed from the `atlas` array), and the PR1 entry has no `atlas:` key
(`curriculum/04-quant.yaml:270-276`). `tools/check_projects.py:144-146` therefore skips the contract check. No
`atlas/PR1.contract.md` is needed or drafted. The studio brief that names Atlas (`curriculum/04-quant.yaml:242-246`) is
STUDIO-PR's, not PR1's. The PR2 project names Atlas A11 (`curriculum/04-quant.yaml:296-300`); PR2 is outside this unit.

---

## 9. Cards builder (Builder F, after A to D)

- `course/modules/PR/PR1/cards.json`, ids `PR1-c001` upward, `lesson` in L01 to L08 (`tools/check_pages.py:366-400`
  `check_cards`: id prefix, lesson existence, grades, registry keys).
- One card per definition (the six concepts), per theorem statement (the six results of §2.1 item 6 and the 1/N theorem),
  per key formula (the precision-form posterior mean, the shrunk covariance, the worst-case identity, the one-way turnover)
  and per misconception (BUILDER_RULES §7).
- Grade T for every derived result, with `"basis"` naming the derivation or the lab that establishes it, for example
  `"basis": "Lab 3, Theorem 3.1 (exact)"`. A result the lab establishes only numerically is graded C with its basis named
  (FINAL-ARCHITECT-RULINGS 13, `plans/FINAL-ARCHITECT-RULINGS.md:28-31`): a card and the key-results row it mirrors carry
  the same grade and basis.
- `cite` lists a registry key only for an empirical or attributed claim (§7.1), and only after the abstract is read (B4).
  Model results have `cite: []`.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit PR1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit PR1
.venv/bin/python tools/check_projects.py --unit PR1
.venv/bin/python tools/run_labs.py --unit PR1               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/PR/PR1/L01.html                       # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/PR/PR1/L02.html --refresh lab-PR1-L02-1   # after editing a twin
.venv/bin/ruff check tests/labs/PR1 && .venv/bin/ruff format --check tests/labs/PR1
.venv/bin/mypy tests/labs/PR1                               # strict, repository configuration
```

Grader (verifier and Builder E; the reference and the instance generator are the only files run by these):

```bash
.venv/bin/python tools/run_graders.py --unit PR1 --seeds 0-49        # reference, 50 seeds (BUILDER_RULES §5.3.2)
.venv/bin/python tools/mutate_graders.py --unit PR1 --seeds 0-9      # verifier only: ten mutants in ledgers/PR1/mutants/
.venv/bin/ruff check course/modules/PR/PR1/grader && .venv/bin/ruff format --check course/modules/PR/PR1/grader
MYPYPATH=course/modules/PR/PR1/grader .venv/bin/mypy --no-incremental --strict course/modules/PR/PR1/grader/reference.py course/modules/PR/PR1/grader/instance.py course/modules/PR/PR1/grader/starter.py
```

Not run by builders: `tools/page_smoke.py --unit PR1` (timing-sensitive; the verifier runs it alone on a quiet machine).
The five alternatives (§5.5.5) are run by a verifier script under `ledgers/PR1/scripts/`, not by any command above (§11.2).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json` (no curriculum change is
planned), `verify_refs.py --offline`, and the full gate in `CLAUDE.md`.

Flag checks: `tools/check_pages.py`, `tools/check_dag.py`, `tools/check_projects.py` accept `--unit`; `tools/run_labs.py` accepts
`--unit` and `--page`; `tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`; `tools/run_graders.py` and
`tools/mutate_graders.py` accept `--unit` and `--seeds` (`tools/mutate_graders.py` docstring).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** The Atlas branch of `check_projects.py` (`:144-146`) does not run. No contract file is needed (§8).
2. **`run_graders.py` tests only the reference.** It copies the panel's solution into a workspace and runs the suite
   (`tools/run_graders.py:43-65`: `panel`, `workspace`, `run_suite`). It has no mode for the five alternatives, so a verifier
   script under `ledgers/PR1/scripts/` must copy each alternative into a temporary workspace and run the suite (the M7 T2
   precedent, `plans/M7-build-plan.md:395-398`). This is a tooling addition, not a builder decision (Q15).
3. **`run_graders.py` imports NumPy at module level** (`tools/run_graders.py:35`). The local harness therefore needs NumPy,
   but the suite and the reference are stdlib only. This is not a PR1 defect.
4. **The grader-panel parser has no guard for a missing `data-support`.** `tools/check_projects.py:131` calls
   `grader.get("data-support").split()` with no `None` check, so a missing attribute raises an exception rather than a FAIL
   row (M7 T4, `plans/M7-build-plan.md:403-405`). The panel must carry `data-support` (§5.5.1). Recorded for the architect.
5. **`check_dag.py` sees linked uses only** (its docstring). Unlinked uses of D1 to D9 (§4.2) pass the tool; the verifier reads
   for them.
6. **Rung 2 must be graded instantly.** `check_projects.py:90` accepts a completion lab or a quiz. The plan uses a completion
   lab.
7. **Five alternatives and ten mutants are not checked by the tools.** `check_projects.py` checks the rubric and the panel
   only. The counts are enforced by the plan and by `mutate_graders.py` (which needs at least three mutants,
   `tools/mutate_graders.py`, `mutants` count), and by the verifier.
8. **The rubric checks run because grading is `both`** (`tools/check_projects.py:138-139` region; `rubric_problems`
   `:58-73`): 5 criteria, each with four `td` cells, exemplars at two levels.
9. **Hub hours.** `check_hub` computes the lesson sum from each lesson's `data-hours` (`tools/check_pages.py:332-342`). Every
   lesson must declare `data-hours` exactly as the hub's split implies (6, 6, 7, 6, 7, 6, 6, 6).
10. **Hours feasibility is a tool rule, not a plan choice.** The 6-to-12 rule for lessons and the 10-to-40 % project band are
    applied to the 70 h figure in §0.2.
11. **Determinism across runtimes (honest risk).** The instance generator uses seeded normal draws. CPython and Pyodide may
    differ in the last bits of `math` functions, so the weight comparison uses tolerance 1e-7 (§5.5.4), and the instance
    validity check uses a margin. Builder E verifies the suite in both runtimes.
12. **Timing.** The suite target is under 60 s in Pyodide. Fraction-based search is the likely cost. Builder E measures it before
    the verifier starts (Q16).

### 11.4 Could not establish (planner)

- The content of the six registry sources: no abstract was read. Nothing in this plan states a finding of any of them (B4).
- The exact text of the Ledoit–Wolf intensity formula. It is not used; δ is given (Q5).
- Whether the Black–Litterman weight construction in §5.2 matches the paper's own allocation convention. The plan states it as a
  model choice (Q9); a builder who wants the paper's convention must read the paper first.
- The Pyodide runtime of the suite and of any Fraction solver. Not measured.
- Whether the registry's `ledoit2017nonlinear` title is the one a reader would expect. It differs from the curriculum's
  description, and no title is typed (§7.1).
- The status of AP2's concept ids. AP2 is unbuilt; its concept ids are the curriculum's `introduces` keys (B3).

---

## 12. Open questions for the architect (numbered; each with a RECOMMENDED decision)

1. **Lesson count and builder shape (B1).** The brief asks for about three lessons per builder for builders A to E. At 70 h
   with a 20 h project only eight lessons fit (§0.2). **RECOMMENDED:** eight lessons, two each for builders A to D (A: L01, L02
   and the hub; B: L03, L04; C: L05, L06; D: L07, L08); E owns the project, grader and project labs; F owns the cards.
   Alternative: nine lessons of 6 h (54 h) and a 16 h project (22.9 %), with A, B and C three lessons each and D taking the
   project labs, E the grader.
2. **Hours split.** **RECOMMENDED:** 50 h lessons, 20 h project (28.6 %), as §1. Alternative within the rules: 56 h lessons
   (eight lessons of 7 h) and a 14 h project (20 %).
3. **Labs per lesson.** The curriculum names one lab (`curriculum/04-quant.yaml:269`); BUILDER_RULES §3.4 asks for a
   numerical check of each key formula. **RECOMMENDED:** one lab per lesson (eight twins, one of which is the curriculum lab,
   `lab-PR1-L02-1`) plus three project labs (M7 Q13 precedent, `plans/M7-build-plan.md:451-452`).
4. **Grading "both".** The curriculum says `both` (`curriculum/04-quant.yaml:276`). **RECOMMENDED:** the allocators and the
   engine are autograded (§5.5), and `report.md` is rubric-graded (§5.4), as BLUEPRINT §5.2 specifies ("Code is autograded;
   the memo or report is rubric-graded").
5. **Shrinkage intensity.** **RECOMMENDED:** the intensity `delta` is given by the instance (§5.5.1), not estimated by the
   Ledoit–Wolf formula, because the planner has not read that formula. The formula is a rung-4 stretch only after the builder
   reads the paper (B4).
6. **Adversarial project.** **RECOMMENDED:** not adversarial; no 15-angle question bank (architect default,
   `plans/E5-build-plan.md:563-564` and `plans/AP2-build-plan.md:816`).
7. **Scope and data.** **RECOMMENDED:** one period, long-only, budget-constrained allocators; SIMULATED generated returns for the
   labs, the grader and the exemplars; the FX spot panel only as an optional, labelled, ungraded stretch with its spot-only
   caveat (§6).
8. **Money.** **RECOMMENDED:** no currency amounts. Cost rates are decimal per unit of one-way turnover; if a notional is added
   later, integer cents with largest-remainder rounding (BUILDER_RULES money rule).
9. **Black–Litterman allocator definition.** **RECOMMENDED:** `μ_BL` (precision form, a derivation) with the sample covariance
   `S` in the long-only mean-variance problem, and `μ_eq = γ S w_mkt` as a model definition. The posterior covariance is not
   used. The page states the choice in one sentence.
10. **Robust allocator and Mean-variance origin.** **RECOMMENDED:** the robust allocator (L06) is a rung-4 stretch, not graded;
    `markowitz1952portfolio` (AP2's key) is not cited by PR1.
11. **Sharpe convention.** **RECOMMENDED:** per period, sample standard deviation with divisor K - 1, no annualization (the M7 Q3
    precedent of stating one period).
12. **Notation.** **RECOMMENDED:** the §2.3 table: `T` = window (registered meaning), `H` total periods, `K` rebalances, `\iota`
    for ones (AP2 precedent), `\mu_{\mathrm{eq}}` for the prior (never `\pi`), `\tau`, `\Omega`, `P`, `q`, `\delta`, `c`, `\gamma`
    local; `\SR` for the Sharpe ratio. NOTATION_REQUESTS: none.
13. **DAG defaults (§4.2).** **RECOMMENDED:** D1 to D5 and D7 to D9 are plain prose with no link; D6 (PR2 concepts) is forbidden in PR1.
    No prerequisite change.
14. **Source strings.** **RECOMMENDED:** cite the six keys only. For `demiguel2007optimal`, the registry carries `years` [2007,
    2009] and `print_year` 2009, and the curriculum string gives 2009 (`curriculum/04-quant.yaml:265`). No year is typed in
    prose. No curriculum string is changed.
15. **Alternatives' location and runner.** **RECOMMENDED:** `ledgers/PR1/alternatives/alt_1.py` to `alt_5.py`, written by the
    verifier and never by the builder, plus a verifier script under `ledgers/PR1/scripts/` that runs the suite on each
    (§5.5.5, §11.2). A test module under `tests/` is an alternative if the architect prefers that.
16. **Runtime and the Fraction alternative.** **RECOMMENDED:** the reference uses floats. alt_1 uses `Fraction` for the final KKT
    check only if the 50-seed run exceeds the time budget; a seeds 0 to 9 window for any alternative needs the architect's
    approval, as E3 had (FINAL-ARCHITECT-RULINGS 10). Builder E measures the suite first.
17. **Build order.** **RECOMMENDED:** build PR1 after AP2 is verified (B3). If the architect wants PR1 built earlier, each lesson
    that relies on AP2 content carries an honest-pending note.
18. **Placement.** **RECOMMENDED:** `data-mastery="0.8"` (the M1 and M7 bar, `course/modules/M/M1/index.html:67`), at least two
    `data-skill` items on what rungs 1 and 2 teach (the 1/N and minimum-variance computation, the turnover line), the others on
    the M4, M7 and S1 prerequisites.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L02 (includes the curriculum lab), L03 to L04, L05 to L06,
   L07 to L08, and the project (grader, mutants, alternatives, rubric and blind exemplar scoring by a separate scorer).
   Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/PR1.verification.json`; verifier scripts under `ledgers/PR1/scripts/`; mutants under `ledgers/PR1/mutants/`
   (exactly the ten of §5.5.3); alternatives under `ledgers/PR1/alternatives/`; any equivalent mutant under
   `ledgers/PR1/equivalent/` with a README proof (VERIFIER §3).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 must be resolved
   first, and B2 and B4 must be named as honest gaps in the final report.

Architect decisions: pending (§12). This plan is the planner's proposal.
