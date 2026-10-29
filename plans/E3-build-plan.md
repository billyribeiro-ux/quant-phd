# E3 build plan: Decision Theory Under Risk & Ambiguity (planner output, 2026-10-28)

Unit: **E3 · Decision Theory Under Risk & Ambiguity** · tier U · 70 h · prerequisites E1, M4 · no Atlas milestone ·
no debate · grading `both` (autograder for the preference-estimation engine, rubric for the instrument and report) ·
output directory `course/modules/E/E3/` (part code `E`) · lab twins `tests/labs/E3/` · ledger `ledgers/E3.verification.json`.

Planner: Haiku, plan only. No lesson content, no curriculum edits, no registry edits, no git operations (no commit, no
push, no branch change). The repository's git status reports the current branch as `HEAD`; the requested branch
`claude/fanout-b3` is the orchestrator's to create or check out. Executors: Haiku builders, then independent Haiku
verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Anything not in the
curriculum is marked **NOT IN CURRICULUM**. Closed forms in §6 are planner hand checks to be re-derived by the builder
and checked by the verifier; they are not sourced.

---

## 0. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| E3 id, title "Decision Theory Under Risk & Ambiguity" | `curriculum/02-economics-finance-core.yaml:88-89` |
| Tier `U`, hours `70`, prereqs `[E1, M4]` | `curriculum/02-economics-finance-core.yaml:90-92` |
| Core text: "Expected utility, Arrow–Pratt risk aversion, stochastic dominance, Epstein–Zin recursive preferences, prospect theory, ambiguity aversion." | `curriculum/02-economics-finance-core.yaml:93-95` |
| `introduces` has 12 concepts, listed in §3 | `curriculum/02-economics-finance-core.yaml:96-108` |
| Sources: five strings (Pratt 1964; Kahneman & Tversky 1979; Epstein & Zin 1989; Ellsberg 1961; Gilboa & Schmeidler 1989) | `curriculum/02-economics-finance-core.yaml:109-114` |
| Lab: "Certainty equivalents of one gamble under four preference models." | `curriculum/02-economics-finance-core.yaml:115` |
| Project "Preference elicitation"; brief: "Design and run an in-page lottery questionnaire, estimate the participant's risk-aversion and loss-aversion parameters by MLE, and report the uncertainty."; deliverable "Instrument plus estimation report."; grading `both` | `curriculum/02-economics-finance-core.yaml:116-123` (brief 118-121, grading 123) |
| No `debate:` key, no `atlas:` key on E3 | `curriculum/02-economics-finance-core.yaml:88-123` (absent) |
| JSON row for E3 matches the YAML (title, tier U, hours 70, prereqs E1 and M4, 12 concepts, 5 sources, lab, project, grading both) | `curriculum/curriculum.json:7418` (`"id": "E3"`), read by planner script |
| All 12 concepts map to module E3 in the `concepts` dict | `curriculum/curriculum.json` `concepts` (planner script: 12 owners = E3) |
| No atlas milestone names E3 | `curriculum/curriculum.json` `atlas` (20 entries; no `module` is E3) |
| Textual row in the generated CURRICULUM.md | `CURRICULUM.md:379` |
| E3 is a prerequisite of AP2, AP7, E4, and two markets modules (downstream) | `curriculum/03-markets.yaml:227` (`prereqs: [M7, S1, E3]`), `:431` (`[AP5, E3]`); `curriculum/02-economics-finance-core.yaml:128` (E4 `[E2, E3, M7]`); AP2 and AP7 rows in `curriculum.json` (AP2 `← M7, S1, E3`, AP7 `← AP5, E3`, `CURRICULUM.md` lines 635, 672). Concept IDs must not change once built. |
| Tier order: F < U < M < D (rank 1–4) | `curriculum/meta.yaml:9-21`; so rungs 1–2 of a tier-U project stay at full length (BUILDER_RULES §5.1; BLUEPRINT §4 applies the minimum "from tier M upward") |
| Topological order (`curriculum.json` `topological_order`): M4 at index 12, E1 at 16, E3 at 24 | planner script, read from `curriculum/curriculum.json` |
| Part E exists (code `E`, title "Economics"); STUDIO-E requires E6, E7 (not E3) | `curriculum/02-economics-finance-core.yaml:4-8` |

### 0.1 Prerequisite closure (computed)

Planner walked `prereqs` recursively in `curriculum/curriculum.json` (same walk as `tools/coursekit.py`
`prerequisite_closure`; the tool itself was not executed by the planner):

- E1 prereqs `[M2]`; M2 prereqs `[M1]`; M1 prereqs `[P0.1]`; P0.1 prereqs `[]`.
- M4 prereqs `[M2]`.
- **Closure of E3 = {E1, M1, M2, M4, P0.1}.** Concepts usable without definition: the concepts introduced by M1 (14),
  M2 (13), M4 (19), P0.1 (11) and E1 (13). E1 and M4 are not yet built, so links go through `concepts.html` anchors only.

Concepts E3 may link (examples, all inside the closure): M4 `random-variable`, `expectation`, `variance`,
`quantile-function`, `conditional-expectation-elementary`, `heavy-tailed-distribution`; M2 `derivative`; M1
`present-value`, `discount-factor`; E1 `utility-maximization`, `price-elasticity`.

---

## 1. Feasibility of the hours (no conflict; no STOP condition)

The curriculum figure is 70 h (`curriculum/02-economics-finance-core.yaml:91`). Tool rules:

- each lesson `data-hours` 6–12 (`tools/check_pages.py` line 228);
- hub `data-hours-lessons + data-hours-project = 70` (`tools/check_pages.py` lines 337–338);
- project share 10–40% of 70, i.e. 7 to 28 h (`tools/check_pages.py` lines 339–340);
- lessons sum to the hub's lessons figure (`tools/check_pages.py` lines 341–342).

**Chosen split: 8 lessons × 7 h = 56 h; project 14 h (20%).** 56 is inside the lesson-sum rule (8 lessons of 6–12 h),
and 56 + 14 = 70. Feasible.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to E3)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3–§8, `VERIFIER_RULES.md` §2 (what the verifier
checks), this file, and `plans/E1-build-plan.md` (the most recent worked example, including its architect decisions).
Study `course/modules/M/M1/` (hub, lessons, project, grader panel, rubric and exemplars) for layout. Imitate structure,
not wording. `course/templates/` holds the four skeletons.

### 2.1 Lessons from the verification campaigns (binding; each was a real defect in an earlier unit)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) or
   from float values stated to full precision, and rounded only at display. A page that shows a rounded figure names its
   rounding rule. Precedent: E1 §2.1 item 1; AC4 KNOWN LIMITATION 3; CF1 L01 Remark 5.2.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names
   only what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS (a "checked directly" phrase with no lab
   behind it). Every "checked", "verified", "shown" claim names the lab, line or test that did it.
3. **Attribute nothing unread.** Cite only the five curriculum keys (§8). No locator, page, table, equation number, or
   empirical number is typed unless the builder has read it in a source. A textbook or paper result without a confirmed
   locator is either a derivation on the page (grade T) or cited at the work level with no locator. Precedent: E1 §2.1
   item 3; AC2; AC4 §1.
4. **Scope words need a computation or an explicit hypothesis.** "every", "all", "never", "always", "any", "for every
   lottery", "in general", "market structures" and "welfare" are used only where a proof, a finite check, or a lab
   computes the claim. Otherwise the scope is written as a stated hypothesis (for example "for finite-support lotteries").
   Precedent: E1 §2.1 item 4 and Q8.
5. **Define before use.** Each of the 12 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its
   assigned lesson, and never before it. A lesson uses a concept only after the lesson that defines it. The verifier
   reads for unlinked uses (VERIFIER §2.9): `check_dag.py` checks linked uses only.
6. **Propositions state every hypothesis, numbered.** Every Theorem, Proposition and Lemma block lists numbered
   Assumptions (A1, A2, …) before the statement, and the proof cites them by number. Examples: lottery support finite;
   utility strictly increasing and twice differentiable on the stated domain; wealth strictly positive where a power
   function is used; γ ≠ 1 in the power form. Precedent: E1 §2.1 item 6.
7. **Notation registry is binding.** Use only macros in `notation/notation.json`. Never give a registered symbol a
   second meaning (§4). Letters that the registry leaves local (γ, λ, α, β, δ, ψ, θ, κ, u, v, w, p, x, V) are defined in
   the lesson where first used and reused with the same meaning across the unit.
8. **Grader tests demand an exception type only for conditions the page names.** The spec lists the named invalid-input
   conditions and their exception type (§5.4). Other invalid input may raise any exception or return. **Five alternative
   correct implementations must pass** the suite (§6.4). **Ten student-error mutants** live in `ledgers/E3/mutants/`
   (§6.5). Precedent: E1 §2.1 item 7.
9. **Integer cents for money.** Every money output of the engine (certainty equivalent, risk premium, lottery prize,
   expected payoff) is an `int` number of cents, computed once and rounded once, half up, by the rule stated on the
   project page. No float money output, no tolerance on money. Parameter estimates (γ̂, λ̂, κ̂) are dimensionless floats
   and are tested with stated tolerances, not with cent equality. Precedent: E1 §2.1 item 8, E1 architect Q6.
10. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
    container; no element widens the page past 360 px. `page_smoke.py` is the verifier's check; builders do not run it.
11. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>` with no network.
    Precedent: E1 §2.1 item 10; M1 twin `tests/labs/M1/lab-M1-L04-1.py`.
12. **Hypothesis before run.** Each lab's `p.hypothesis` states the expected result before the expected-output block
    is embedded. Each lab is seeded if it draws random numbers (`random.Random(seed)`), uses the standard library only,
    and runs under 10 s in Pyodide.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- **Evidence.** Every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key (`data-cite`) or a derivation.
  A grade-T claim is a derivation or a theorem shown in full (BUILDER_RULES §3.5). Over-grading and under-grading both fail.
- **Contested claims are two-sided** (BLUEPRINT §3; BUILDER_RULES §2.5). Any B- or C-graded claim names its published
  counter-evidence. Loss aversion (L06) and probability weighting (L07) are contested; the lesson states the counter-side.
- **Concepts.** `<dfn id="def-<id>" data-concept="<id>">` only for the 12 concepts in §3. Terms outside the 12 appear in
  prose and, if emphasised, as plain `<dfn>` without `data-concept` (E1 architect precedent, AC4 Q4). A concept outside the
  closure is written in plain words with no link (see §7 DAG table).
- **Concept links.** Closure concepts: `<a class="concept" data-concept="<id>" href="../../../concepts.html#<id>">`.
  Earlier E3 lessons: `href="Lnn.html#def-<id>"`. A lesson never links a concept defined in a later lesson.
- **Labs.** Code lives once in `tests/labs/E3/lab-E3-Lnn-1.py` (and `lab-E3-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output by hand. Lab ids
  match `lab-E3-<page>-<n>` (`tools/check_pages.py` lines 255–258). Standard library only (`fractions`, `math`, `random`,
  `itertools`); no NumPy or SciPy; no network; under 10 s in Pyodide; no warnings (`-W error`).
- **SIMULATED label.** Required wherever a figure, lab or grader uses generated preferences, generated lotteries, or
  generated participants. Exact computations (closed forms, identities) are not labelled SIMULATED (E1 §2.2 precedent).
- **Never hand-edit generated files**: `CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`.
  Request changes in the output contract; never write them.
- **Learner-visible text.** No process words in the page (build, builder, round, verifier, REQUESTS, unit report) and no
  planning references in code comments (E1 §2.2 precedent).
- **Banned strings.** `tools/check_pages.py` lines 58–73: TODO, TBD, lorem, "for brevity", "details omitted", "beyond
  the scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree",
  "it is well known", "obviously", "clearly", and any ellipsis `...` outside code.
- **Percent changes** state the base and the direction (CF1 L07 precedent).
- **A finite enumeration is grade C with its basis named**, not grade T (M1 L06 precedent).
- **Hub lesson titles** match each lesson's `<h1>` at integration (CF1 KNOWN 3 precedent).
- **Quiz explanations** are read against their lesson (CF1 KNOWN 6 precedent).
- **No `git commit`, no push.** The builder reports files written, commands run with exact output, and every gap in the
  BUILDER_RULES §10 output contract.

---

## 3. Outline and file ownership (fixed by this plan; the architect confirms)

Lessons: 8 × 7 h = 56 h. Concepts: 12, each in exactly one row (count per row: 1+2+1+2+2+2+1+1 = 12, matching
`curriculum/02-economics-finance-core.yaml:96-108`).

| Lesson | Title (working) | Concepts it defines (from `introduces`, yaml 97–108) | Lab twin id (`tests/labs/E3/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Expected utility | `expected-utility` | `lab-E3-L01-1`: expected utility of finite lotteries in exact `Fraction`; linearity in the probabilities checked exactly | 7 | Builder A |
| L02 | Risk aversion and the certainty equivalent | `arrow-pratt-risk-aversion`, `certainty-equivalent` | `lab-E3-L02-1`: certainty equivalent and risk premium for \(u(w)=\sqrt{w}\) and \(u(w)=w\) on one lottery; the second-order (Pratt) premium \(\tfrac12 r_A \Var\) compared against the exact premium, with the error printed | 7 | Builder A |
| L03 | Constant relative risk aversion | `crra-utility` | `lab-E3-L03-1`: CRRA certainty equivalent in integer cents over a grid of γ; the γ→1 limit (log) checked; homogeneity \(CE(kx)=k\,CE(x)\) checked | 7 | Builder B |
| L04 | Stochastic dominance | `first-order-stochastic-dominance`, `second-order-stochastic-dominance` | `lab-E3-L04-1`: finite-support pairs; CDF test (FOSD) and integrated-CDF test (SOSD) on seeded pairs; each verdict checked against the expected-utility ranking over a grid of nondecreasing (concave) utilities | 7 | Builder B |
| L05 | Recursive preferences and the elasticity of intertemporal substitution | `epstein-zin-preferences`, `elasticity-of-intertemporal-substitution` | `lab-E3-L05-1`: two-period Epstein–Zin value of a consumption plan with a risky second period; identity: the value equals the CRRA expected-utility value when \(\psi = 1/\gamma\) | 7 | Builder C |
| L06 | Prospect theory and loss aversion | `prospect-theory`, `loss-aversion` | `lab-E3-L06-1`: reference-dependent value function over gains and losses; the sign of a gamble's value flips across the loss-aversion threshold, computed exactly for a stated λ | 7 | Builder C |
| L07 | Probability weighting | `probability-weighting` | `lab-E3-L07-1`: a weighting function's endpoints and overweighting of small probabilities; an exhibited pair where the probability-weighted (1979-form) value ranks a first-order-dominated lottery higher, checked by the FOSD test from L04 | 7 | Builder D |
| L08 | Ambiguity aversion and the four-model comparison | `ambiguity-aversion` | `lab-E3-L08-1` (**the curriculum lab**): certainty equivalents of one gamble under four preference models (expected utility with CRRA, prospect value, maxmin expected utility over a prior set, Epstein–Zin under a stated timing; §10 Q2); plus an Ellsberg-type two-urn check computed from its stated prior set | 7 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 56 / 14 | none | none | – | Builder A |
| project | Preference elicitation (`both`), §5–§6 | none | `lab-E3-project-1` (rung 1), `lab-E3-project-2` (rung 2, `class="lab completion"`), `lab-E3-project-3` (rung 3 check) | 14 | Builder E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | – | Builder E |
| cards | `cards.json` from L01–L08 | none | none | – | Builder F (after A–D) |

Ownership rule: each builder writes only its lesson files and twins. Builder A writes the hub after L01–L02 exist, so the
lesson map is right; the hub cross-check runs at integration. Builder E's grader is independent of the lessons.

Ordering check (no lesson links a later definition):
- L01 uses M4 `random-variable`, `expectation` only.
- L02 uses L01 (`expected-utility`) and M2 `derivative` (for \(u''\)).
- L03 uses L02 (`certainty-equivalent`, `arrow-pratt-risk-aversion`); CRRA has constant \(r_R=\gamma\).
- L04 uses L01 (EU), L02 (concavity, stated with M2 `derivative`), M4 `random-variable` (distribution functions).
- L05 uses L01 (EU), L03 (CRRA), and M1 `discount-factor` for the discount factor β.
- L06 uses L02 (certainty equivalent, as the reference point's counterpart) and L03 (power forms).
- L07 uses L06 (value function) and L04 (the FOSD test used in the exhibit).
- L08 uses L01, L03, L05, L06, L07 (all four models) and the maxmin rule defined inside L08.

Hours check: 8 × 7 = 56 (hub `data-hours-lessons="56"`); project 14 (hub `data-hours-project="14"`); total 70.

---

## 4. Notation (`notation/notation.json`)

Registered symbols and macros that E3 must not reuse with another meaning (from `notation/notation.json` `symbols` and
`macros`; the registry is binding, BUILDER_RULES §3.2):

| Registered symbol | Registered meaning | E3 consequence |
|---|---|---|
| `T` | number of return observations (S1) | never use `T` for a horizon or a sample size; use t = 0, 1 and "two periods" |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and quantile (M4) | never use `\Phi` for a probability-weighting function |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (M4) | never subscript γ; plain `\gamma` is the CRRA coefficient, which the registry's `\emgamma` note leaves free |
| `R^\ast`, `R^{e\ast}`, `R_f` | SDF return, projection of 1, gross riskless return (AP1) | never use `R_f`; use `r_A(w)`, `r_R(w)` for the Pratt measures (lowercase, no clash with the `\R` macro) |
| `\mathbb{Q}` | equivalent martingale measure (AP1) | never use `\mathbb{Q}` for a prior; use `\mathcal{P}` for the set of priors |
| `\E`, `\Var`, `\Cov`, `\Prob`, `\R`, `\indic`, `\Normal` | registered macros | use the macros, not raw `\mathbb{E}` |

Local letters E3 will use (defined in the first lesson that uses them; none is registered):
- `w` wealth, `x` outcome, `p` probability, `u` Bernoulli utility, `v` value function (prospect model), `V` recursive value,
  `CE` certainty equivalent (write `\mathrm{CE}`), `π` risk premium (write as a word or `\pi_{\mathrm{rp}}` if needed; `\pi` is not registered);
- `γ` CRRA coefficient, `ψ` elasticity of intertemporal substitution, `θ = (1-\gamma)/(1-1/\psi)` (Epstein–Zin exponent),
  `β` discount factor (E3 only; the M1 `discount-factor` concept is the same object), `λ` loss aversion, `α`, `δ` value and weighting exponents
  (Tversky–Kahneman form), `κ` logit choice precision (not `μ`, which is local to other lessons);
- `𝒫` (`\mathcal{P}`) the set of priors in the maxmin rule.

Planner's proposal: no `NOTATION_REQUESTS` are required. An optional request is the macro `\CE` for the certainty
equivalent, because it recurs in L02, L03, L06, L08 and the project (§9).

Notation conflicts the planner foresees (for the verifier):
1. Epstein–Zin literature often writes ρ for \(1/\psi\) or \(1-1/\psi\); this plan writes \(1-1/\psi\) in full, uses ψ for the EIS,
   θ for the exponent ratio, and never ρ, so that one symbol has one meaning across the unit.
2. Tversky–Kahneman use β for the loss-value exponent; this plan uses β for the EZ discount factor, so the loss exponent is δ on the losses side and α on the gains side (§10 Q7).
3. Pratt's "relative risk aversion" is written \(r_R\), not \(R\), to avoid the `\R` macro.

---

## 5. Hub, lessons and labs (common to all owners)

- **Hub (`index.html`, Builder A).** `<main data-hours-lessons="56" data-hours-project="14">`. 4–8 measurable objectives
  (verbs such as "derive", "compute", "test", "estimate", "compare"). Prerequisites: E1 and M4, with links to the closure
  concepts in `../../../concepts.html#<id>`. Placement: `<section class="quiz" id="placement" data-unit="E3" data-page="placement" data-mastery="0.8">`
  (the E1 and M1 bar), with at least two `data-skill` items that test what rungs 1–2 teach (the worked example's expected-utility
  computation and the completion problem's missing step) and the rest testing E1 and M4 prerequisites. Lesson map links
  L01–L08 and `project.html`. Project ladder `ol.ladder` with four `rung-title` entries in order. Tier U keeps rungs 1–2 at full length.
- **Lessons (Builders A–D).** Each lesson `<html data-hours="7">` and follows BUILDER_RULES §4.2 in order: why it matters
  (≤120 words), numbered core sections of Definition/Theorem/Proof/Example/Remark blocks, inline lab (before "where the canon
  breaks"), where the canon breaks, misconceptions (≥3; each with the wrong belief and the evidence), problem set (≥3 in each
  of mechanics, proof, empirical and research tiers, each with `<details class="solution">` of ≥15 words), key-results table
  (claim, grade, keys), quiz (8–15 items, each with an explanation), references (`<ol data-references>` of registry keys).
  No debate brief: E3 has no `debate` key (§0).
- **Labs.** One inline lab per lesson, id `lab-E3-Lnn-1` (the number is the display order), `data-runtime="python"`, hypothesis
  stated before running, interpretation names only what the printed numbers show. No `data-files` (§8).
- **Lesson content guidance (what each must establish; builders decide the argument).**
  - **L01 Expected utility.** A finite lottery as a random variable with probabilities (M4 `random-variable`, `expectation`).
    Expected utility \(\E u(x)=\sum_i p_i u(x_i)\) as a definition. Linearity in probabilities (T, one line). State that the
    axiomatic representation is not proved here (REFERENCE_REQUEST R1).
  - **L02 Risk aversion.** Concave Bernoulli utility (defined by \(u''\le 0\), M2 `derivative`, no link to M7 concepts) implies
    \(\CE \le \E x\) for finite lotteries (T, with Assumptions). Arrow–Pratt measures \(r_A(w)=-u''(w)/u'(w)\),
    \(r_R(w)=-w\,u''(w)/u'(w)\) (T, definitions). Small-risk premium \(\pi \approx \tfrac12 r_A(w)\Var(x)\) as a second-order
    approximation with the error term named (T approximation, not an equality). The lab prints the exact premium and the
    approximation error.
  - **L03 CRRA.** \(u(w)=w^{1-\gamma}/(1-\gamma)\) for \(\gamma\ne1\), \(u(w)=\ln w\) at γ = 1; constant relative risk aversion
    \(r_R=\gamma\) (T). Certainty equivalent \(\CE = (\sum_i p_i x_i^{1-\gamma})^{1/(1-\gamma)}\) for positive outcomes (T).
    Homogeneity: \(\CE(kx)=k\,\CE(x)\) (T). The γ→1 limit is the logarithm (T, one line of limit: M2 `derivative` and
    the L'Hôpital-free expansion shown on the page).
  - **L04 Stochastic dominance.** FOSD: \(F\le G\) pointwise (distribution functions, M4 `random-variable`) ⇔ \(\E u(X)\ge\E u(Y)\)
    for all nondecreasing \(u\). Prove the ⇒ direction for finite support by summation by parts; prove ⇐ by indicator utilities
    (T, Assumptions A1 finite support). SOSD: \(\int_{-\infty}^t F\le \int_{-\infty}^t G\) for all t, with equal means ⇔
    \(\E u(X)\ge\E u(Y)\) for nondecreasing concave \(u\). State the full SOSD characterisation as cited (REFERENCE_REQUEST R2);
    prove only the finite-support case that the lab checks.
  - **L05 Recursive preferences.** Two-period Epstein–Zin (planner's form; the builder re-derives it): with
    with \(1-1/\psi\) written out in full, \(V_0=\big[(1-\beta)c_0^{\,1-1/\psi}+\beta\,(\E_0 V_1^{\,1-\gamma})^{(1-1/\psi)/(1-\gamma)}\big]^{1/(1-1/\psi)}\),
    and the exponent ratio \(\theta=(1-\gamma)/(1-1/\psi)\) of §4. No symbol ρ is used (§4 note 1).
    Two periods only (no infinite horizon, no fixed point, no Bellman operator; §7 DAG table). EIS defined as the elasticity of
    the consumption ratio with respect to the marginal rate of substitution, stated for the two-period plan (T definition).
    Identity: with \(\psi = 1/\gamma\) the exponent \(\theta=1\) and the EZ value equals the CRRA expected-utility value (T,
    checked by the lab to exact arithmetic on a finite tree).
  - **L06 Prospect theory and loss aversion.** Reference-dependent value \(v(x)=x^{\alpha}\) for gains and
    \(v(x)=-\lambda(-x)^{\delta}\) for losses, reference point 0 (definition following KT 1979, locator not read: no page or
    equation number may be typed unless read; REFERENCE_REQUEST R5 for counter-evidence on magnitudes). Loss aversion
    \(\lambda>1\) is a parameter, not a theorem; the lesson says so, and gives the contested-evidence side (grade B/C with
    counter-evidence named; topic only, REFERENCE_REQUEST R5).
  - **L07 Probability weighting.** Weighting \(w(p)\) with \(w(0)=0\), \(w(1)=1\) and the Tversky–Kahneman inverse-S form as one
    example (definition, shape stated as a hypothesis, not a theorem). Exhibit: the 1979 form applied to probabilities one at a
    time can rank a first-order-dominated lottery higher (a finite pair; the FOSD test from L04 certifies the dominance; T
    for the exhibit). Cumulative/rank-dependent repair named as REFERENCE_REQUEST R3, not derived here.
  - **L08 Ambiguity aversion.** Ellsberg-type urn: the two-urn comparison with a stated prior set (not the paper's numbers
    unless read: REFERENCE_REQUEST R4 and the Ellsberg record `ellsberg1961risk` cited by key only). Maxmin expected utility
    \(V(f)=\min_{P\in\mathcal{P}}\E_P u(f)\) (Gilboa & Schmeidler, key `gilboa1989maxmin`, locator not read). Singleton prior
    gives expected utility (T). Ambiguity aversion defined as \(\CE(f)\le\CE_{\bar P}(f)\), with \(\bar P\) the average prior (T
    definition). The curriculum lab (four models) is here: §6 spec for the four CEs and the timing rule (§10 Q2).

---

## 6. Project (`project.html`, Builder E): ladder, spec, engine, grader

### 6.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py` line 33 requires the order)

1. **Rung 1, worked example** (`lab-E3-project-1`): one fully solved, annotated case: a generated (SIMULATED) participant's
   three answers to a choice pair; the certainty equivalents computed under the CRRA and the loss-averse CRRA value; the
   choice likelihood step. Each step has a "why" note.
2. **Rung 2, completion** (`lab-E3-project-2`, `class="lab completion"`): the log-likelihood contribution of one choice with
   the sign and the logit terms removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals
   the twin line or contains a blank (`tools/run_labs.py` completion rule).
3. **Rung 3, independent project (graded):** (a) the autograded engine `elicit.py` to the §6.2 interface, and (b) the
   instrument and report, rubric-graded (§6.6). `lab-E3-project-3` is the rung-3 check: it calls the engine on the reference case and
   prints the estimates with their standard errors.
4. **Rung 4, stretch** (optional, not graded): a second model of the choice noise (for example a probit link), with the
   comparison stated as a hypothesis; or a probability-weighted value added to the engine with its identification argument.

### 6.2 Spec (`dl.spec`; `tools/check_projects.py` lines 34–49 require the terms and both grading words)

Terms: Context (2–4 sentences), Inputs, Required outputs, Constraints, Grading.

- **Context.** A participant answers a short questionnaire of choices between a sure amount and a lottery, or between two
  lotteries. The answers identify the participant's curvature of value (risk aversion γ), the asymmetry of the value
  function around the reference point (loss aversion λ), and the noise in the answers (κ). The question is how precisely each
  can be estimated from one questionnaire.
- **Inputs.** (a) the instrument: a list of at least 12 choice pairs written by the student, each lottery given as integer
  prizes in cents and exact probabilities as fractions; (b) the participant's responses as a JSON list of `{pair_id, choice}`,
  produced in the browser (§8, personal data).
- **Required outputs.**
  - `elicit.py` (the student module; name proposed, §10 Q5) with:
    - `certainty_equivalent_cents(model: str, prizes_cents: list[int], probabilities: list[Fraction], params: dict[str, float], wealth_cents: int) -> int`, where `model` is `"crra"` or `"prospect"` (below);
    - `log_likelihood(responses: list[dict[str, object]], params: dict[str, float]) -> float`;
    - `estimate(responses: list[dict[str, object]]) -> dict[str, float]` with keys `gamma_hat`, `lambda_hat`, `kappa_hat`, `se_gamma`, `se_lambda`, `se_kappa`, `log_likelihood`.
  - `instrument.json` (the pairs, with the design rationale in the report).
  - `report.md` with the sections named in the rubric (§6.6).
- **Models (planner proposal, §10 Q4).** Two models share the `certainty_equivalent_cents` interface.
  - `"crra"` (expected utility over final wealth, used for the γ = 1 log case, the homogeneity identity and the rung-1 example):
    \(u(W)=W^{1-\gamma}/(1-\gamma)\) for γ ≠ 1 and \(\ln W\) at γ = 1, with final wealth \(W = \texttt{wealth\_cents} + x\) and \(W>0\);
    \(\CE\) is the sure amount \(c\) with \(u(c)=\E u(W)\), reported as a change from wealth.
  - `"prospect"` (the estimator's model; a loss-averse power value on changes from the reference point 0, without probability
    weighting; the simplification is stated in the report). Restricted to γ ∈ [0, 1) so that \(v\) is finite and continuous at 0:
    \(v(x)=x^{1-\gamma}\) for \(x\ge 0\), \(v(x)=-\lambda(-x)^{1-\gamma}\) for \(x<0\), λ > 0, \(v(0)=0\), strictly increasing.
    Lottery value \(V=\sum_i p_i v(x_i)\); certainty equivalent \(\CE=v^{-1}(V)\) (closed form: \(V^{1/(1-\gamma)}\) if \(V\ge0\), else \(-(-V/\lambda)^{1/(1-\gamma)}\)).
  - Choice probability (logit): \(P(\text{choose }A)=1/(1+\exp[-\kappa(\CE_A-\CE_B)])\), κ > 0. Likelihood: product over responses of \(P\) (chosen) or \(1-P\) (not chosen).
  - `estimate` uses the `"prospect"` model only; its parameters are γ ∈ [0, 1), λ > 0, κ > 0 (the bounds are part of the spec).
- **Constraints.**
  - Integer cents for every money output (`certainty_equivalent_cents`): computed in float at full precision, rounded once, half up to the nearest cent; the rounding rule is stated in the spec and the module docstring. Estimates are floats with a stated tolerance.
  - Valid input and the exception table (§6.3); no other exception type is required.
  - Standard library only; no network; the same code runs in Pyodide and under pytest.
  - Probabilities are exact `Fraction`s; the sum of probabilities must equal 1 exactly.
- **Grading.** Autograder (`grader/test_project.py`, dual-mode) for `elicit.py`; rubric (`rubric-memo`, §6.6) for the instrument
  and the report. The spec names both "autograder" and "rubric" (`tools/check_projects.py` lines 38–49).
- **Reading list.** `ol.reading-list` cites the five curriculum keys that the project uses: `pratt1964risk`,
  `kahneman1979prospect`, `epstein1989substitution`, `ellsberg1961risk`, `gilboa1989maxmin` (§8).

### 6.3 Exception table (grader tests demand these, and only these)

| Condition the page names | Exception | Message must name |
|---|---|---|
| `model` not `"crra"` or `"prospect"` | `ValueError` | the allowed names |
| probabilities negative, or not summing to exactly 1 (as `Fraction`) | `ValueError` | "probabilities must sum to 1" |
| `model == "crra"` and `wealth_cents + x <= 0` for some prize x | `ValueError` | "wealth plus prize must stay positive" |
| `responses` empty, or no response whose lotteries mix gains and losses (λ unidentified) | `ValueError` | the condition, e.g. "need mixed-sign lotteries to identify loss aversion" |

Any other invalid input may raise any exception or return.

### 6.4 Five alternative correct implementations (must all pass; the verifier writes them as test-only fixtures under `ledgers/E3/scripts/`)

1. Closed-form CRRA CE and a grid search for the MLE.
2. Newton iteration on the log-likelihood with an analytic gradient, stopped at the first-order condition.
3. Coordinate search (for example, Nelder–Mead written by hand) on the negative log-likelihood.
4. Bisection inversion of \(v\) for the certainty equivalent (no closed form), followed by the same half-up rounding.
5. A float implementation of items 1–4 combined with the same half-up rule applied to the value of the float, not to a rounded intermediate.

Note: "Fraction throughout" is **not** available for general γ (power functions are irrational in general). §10 Q6 decides the
test design for this; the planner's recommendation is that the cent tests use exact-known cases (γ = 0, the risk-neutral case,
and the homogeneity identity) and the float cases avoid instances whose unrounded CE lies within 1e-6 of a half cent (the
instance generator enforces this guard).

### 6.5 Student-error mutants (verifier writes ten complete modules to `ledgers/E3/mutants/*.py`; each docstring's first line describes the error)

1. CRRA with no log limit at γ = 1 (raises `ZeroDivisionError` on γ = 1 instances; the spec requires the γ = 1 case).
2. Certainty equivalent set to the expected prize (risk neutral), ignoring curvature.
3. Certainty equivalent computed as \(u^{-1}(u(\E x))\) rather than \(u^{-1}(\E u(x))\).
4. Loss aversion applied to gains instead of losses (kink reversed).
5. Probability weights applied to outcomes in listed order rather than rank order (dependence on outcome ordering).
6. Ranking test for FOSD with the inequality reversed (\(F\ge G\) tested instead of \(F\le G\)).
7. SOSD tested on the CDFs rather than on the integrated CDFs (the FOSD test with a different name).
8. Certainty equivalent rounded by truncation instead of half up (breaks the cent-exact checks on instances whose value is near x.5).
9. Epstein–Zin exponent with EIS and risk aversion swapped (\(\psi\) and \(\gamma\) interchanged in θ).
10. Log-likelihood that omits the \(1-P\) term for the unchosen alternative (uses only chosen options).

The verifier may add a hard-coded answer for seed 0 and a standard-error mutant (SE from the Hessian without inverting it);
those are not counted in the ten student-error mutants. `tools/mutate_graders.py` enforces only a minimum of three (§10 Q8).

### 6.6 Rubric (memo and instrument; `both` requires it, `tools/check_projects.py` `rubric_problems`, lines 58–72)

Five criteria, each with four observable levels (level 4 down to level 1). Each descriptor names something a grader can see.

1. **Instrument design.** States the pairs, the prize scale in cents, and why the pairs contain gains and losses. Level 4:
   lists the pairs with cents and exact probabilities and shows the mixed-sign pairs. Level 1: "a reasonable set of questions".
2. **Estimation model.** States the value function, the logit choice rule and the likelihood with its two terms. Level 4:
   writes the likelihood, names the simplification (no probability weighting), and states which parameters are identified by
   which pairs.
3. **Uncertainty.** Reports `se_gamma`, `se_lambda`, `se_kappa` with the convergence check and the asymptotic assumption.
   Level 4: states that standard errors are from the observed information at the estimate, names the sample size, and
   states when they are unreliable.
4. **Interpretation and limits.** Says what the estimates do and do not say (one participant, hypothetical stakes, noise
   parameter confounded with curvature if the design is poor). Level 4: names at least two limits with a direction of bias.
5. **Evidence.** Every empirical claim is graded with a registry key and a locator actually read. Level 4: every claim
   carries grade and key; no locator is invented.

**Exemplars** at two levels: `exemplar-a` (`data-level="2"`) and `exemplar-b` (`data-level="4"`), fully written memos on a
SIMULATED participant, each annotated with the descriptors it meets or misses, with `data-scores` and `data-criterion` as in
M1 (`course/modules/M/M1/project.html` lines 341–352, 405–476). Self-assessment form `section.rubric-self` with
`data-rubric="rubric" data-exemplars="exemplar-a exemplar-b"`. The page shows where the student's scores diverge from the exemplar scores.

Adversarial question bank: **not required.** The memo is not an IC defence or a debate (curriculum yaml 116–123 names a
"plus estimation report" deliverable, not a defence); `tools/check_projects.py` only requires the bank when the page has
`id="question-bank"`. §10 Q9 asks the architect to confirm.

### 6.7 Grader design (Builder E)

**Files** (`course/modules/E/E3/grader/`): `instance.py`, `reference.py` (the full solution; excluded from deployment,
BLUEPRINT §7), `starter.py` (stubs raising `NotImplementedError`), `test_project.py`. No Atlas path; the solution is unit-local
(`check_projects.py` lines 144–146 do not apply).

Grader panel on `project.html`: `<section class="grader-panel" id="grader" data-unit="E3" data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="elicit.py" data-starter="starter.py"></section>`.
`data-packages` is empty (standard library only).

- **`instance.py`**: `make_instance(seed: int) -> dict[str, object]`. Deterministic per seed. Generates a participant
  (`"prospect"` parameters γ ∈ [0.1, 0.8], λ ∈ [1, 3], κ ∈ [0.5, 5], drawn within these ranges; γ = 1 is outside the estimator's
  domain and is tested only under the `"crra"` model), a design of at least 12 pairs with mixed-sign lotteries, and the simulated
  choices with `random.Random(seed)`.
  Labelled **SIMULATED** in the docstring. Validity: positive prizes in cents, probabilities summing to 1 exactly, and the
  identification guard (the Hessian of the log-likelihood at the true parameters is negative definite, checked in `instance.py`
  itself). Guard against near-half-cent CE values (§6.4).
- **`reference.py`**: the full solution with the rules in §6.2. Passes every test on seeds 0–49
  (`tools/run_graders.py --unit E3 --seeds 0-49`).
- **`starter.py`**: `NotImplementedError` stubs; the suite must fail on it (`tools/run_graders.py` checks this).
- **`test_project.py`**: properties and numbers; each test recomputes its expectation from the instance's own parameters
  with an oracle written separately from `reference.py`:
  - `"crra"` model: CE monotone in each prize; CE ≤ expected final wealth for γ > 0 (risk aversion); CE equals expected final wealth at γ = 0;
  - `"crra"` model: the γ = 1 log case matches the γ → 1 limit to 1e-6 (tolerance stated);
  - `"prospect"` model: CE equals the sure amount whose value equals the lottery value (checked by recomputing \(v\) at the CE, to the cent);
  - homogeneity: \(\CE(kx)=k\CE(x)\) to the cent (integer k);
  - FOSD and SOSD verdicts on the instrument's pairs match the expected-utility ranking over a finite grid of utilities (no
    fixed answers);
  - integer output: every CE return value is an `int`; rounding half up on a stated set of exact-known values;
  - MLE properties: score ≈ 0 at `estimate`'s output (tolerance 1e-4 relative); the log-likelihood at the estimate is ≥ its
    value at each of ±small perturbations; `se_*` are positive and finite; the estimate lies within 4 standard errors of the
    seed's true parameter on at least 47 of seeds 0–49 (count threshold, §10 Q12);
  - exception table (§6.3): the named conditions raise `ValueError` naming the condition; no other type required;
  - failure messages name the violated property and hint at the concept; they never print the answer.
- **Dual mode**: identical suite in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.

### 6.8 Time budget (`<table id="hours">`, sums to 14 h, every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved SIMULATED participant, annotated line by line |
| Rung 2, completion problem | 1 | Fill the likelihood contribution, then run the instant check |
| Instrument design and the in-browser questionnaire | 3 | Choose at least 12 mixed-sign pairs in cents, check probabilities sum to 1 |
| `elicit.py` and the local test run | 4 | Implement the §6.2 interface, pass seeds 0–49, handle the exception table |
| Uncertainty and report (`report.md`) | 3 | Standard errors from the observed information, convergence check, limits |
| Self-assessment against exemplars | 2 | Score the report, then compare with `exemplar-a` and `exemplar-b` |
| **Total** | **14** | Equals `data-hours-project` on the hub |

---

## 7. DAG problems and resolutions (concepts that natural content would use outside the closure)

Closure = {E1, M1, M2, M4, P0.1}. Owners from `curriculum/curriculum.json` `concepts`.

| Concept or term | Owner | Where natural content uses it | Resolution in this plan |
|---|---|---|---|
| `maximum-likelihood-estimation`, `mle-asymptotic-normality`, `fisher-information`, `confidence-interval`, `estimator` | S1 | project: MLE and its standard errors (§6) | Plain prose, no link; the log-likelihood and its Hessian are written out from M2 `derivative` and `hessian`. **DAG_DEFECT** reported (CF1 Q2 precedent: no statistics prerequisite added). §10 Q3 |
| `convex-function`, `convex-set` | M7 | concavity of \(u\) and Jensen (L02, L04) | Concave defined by \(u''\le 0\) with M2 `derivative`; no link, no M7 name. §10 Q3 |
| `convexity` | FI1 | same as above | Not used as a term |
| `bellman-equation`, `principle-of-optimality` | M7 | Epstein–Zin recursion (L05) | Two-period backward recursion in plain words; no infinite horizon; no fixed point. §10 Q11 |
| `risk-neutral-probability` (FC2), `equivalent-martingale-measure` (AP1) | FC2, AP1 | "risk-neutral" wording (L01, L02) | Say "risk-neutral" (linear \(u\)) only; no probability is named; `\mathbb{Q}` is not used |
| `equity-risk-premium` (AP2), `equity-premium-puzzle` (AP3) | AP2, AP3 | the word "risk premium" (L02) | Define "certainty-equivalent risk premium" in L02 with no link; note the term collision in the lesson |
| logit choice model; reference-dependent value; probability weighting function (beyond E3's own) | none (not curriculum concepts) | project model (§6.2), L06, L07 | Plain prose; `probability-weighting` is E3's own and is defined once in L07 |
| `expected-value-game` (PC3), `stochastic-discount-factor` (AP1) | PC3, AP1 | not used | Avoid the names |

Concept IDs used by E3's own closure links are all present in the closure (§0.1). No concept is used before its lesson
(§3 ordering check). **Verifier note:** `check_dag.py` sees only linked uses; the verifier must read every lesson and the
project for the unlinked names in this table (VERIFIER §2.9).

---

## 8. Registry keys the module may cite

Verified in `references/references.json` (status verified, crossref). Each key's `used_by` is `["E3"]` only, and each record's
year, container and volume/issue match the curriculum's source string (read by planner):

| Key | Record (as read) | Curriculum string (yaml 110–114) | Use in E3 |
|---|---|---|---|
| `pratt1964risk` | Pratt, "Risk Aversion in the Small and in the Large", Econometrica, 1964, volume 32, issue 1/2 | Pratt (1964), Econometrica 32(1-2) | L02 (Arrow–Pratt measures), project reading list |
| `kahneman1979prospect` | Kahneman & Tversky, "Prospect Theory: An Analysis of Decision under Risk", Econometrica, 1979, volume 47, issue 2 | Kahneman & Tversky (1979), Econometrica 47(2) | L06, L07, project reading list |
| `epstein1989substitution` | Epstein & Zin, "Substitution, Risk Aversion, and the Temporal Behavior of Consumption and Asset Returns: A Theoretical Framework", Econometrica, 1989, volume 57, issue 4 | Epstein & Zin (1989), Econometrica 57(4) | L05, project reading list |
| `ellsberg1961risk` | Ellsberg, "Risk, Ambiguity, and the Savage Axioms", QJE, 1961, volume 75, issue 4 | Ellsberg (1961), QJE 75(4) | L08, project reading list |
| `gilboa1989maxmin` | Gilboa & Schmeidler, "Maxmin expected utility with non-unique prior", Journal of Mathematical Economics, 1989, volume 18, issue 2 | Gilboa & Schmeidler (1989), Journal of Mathematical Economics 18(2) | L08, project reading list |

Rules: cite by key only; no locator unless the builder has read the source (the planner read none of the five papers; the
abstract page of each is the minimum read before any claim is attributed to it). Attribution is limited to what the paper
states; "Pratt's approximation" is a derivation on the page (grade T), with the key cited at work level only.

Keys in the registry that belong to other modules and must **not** be cited from E3: `rothschild1976equilibrium` (used by E2;
a 1976 QJE insurance paper, not the 1970 increasing-risk paper; do not confuse), `bansal2004risks` (AP4), `weil1989equity` (AP3),
`stokey1989recursive` (M7), `mehra1985equity`, `campbell1999force`, `holmstrom1979moral` (E2). Velleman (`velleman2019prove`) is
not curriculum-listed for E3 and is not cited (§10 Q7).

### 8.1 REFERENCE_REQUESTS (topics and leads only; no bibliographic data typed from memory)

Each line gives the topic and the lead name only. The architect resolves each through `tools/add_reference.py` (DOI, ISBN, or an
allow-listed issuer page; `references/authorities.yaml`). DOI and bibliographic fields are `null` until resolved.

- R1. **Axiomatic expected-utility representation** (L01 states EU as a definition; if the lesson claims the representation, a
  primary source is needed). Lead only: von Neumann & Morgenstern, 1944 (book). DOI: null. Confidence the lead names a real
  work: high; citation string: unverified.
- R2. **Full characterisation of second-order stochastic dominance** (L04; the planner proves only the finite-support case).
  Lead only: Rothschild & Stiglitz, 1970 (*Journal of Economic Theory*, "increasing risk"). Not `rothschild1976equilibrium`. DOI: null.
- R3. **Rank-dependent or cumulative repair of the 1979 weighting** (L07 names the repair without deriving it). Lead only:
  Quiggin, 1982 (rank-dependent utility); Tversky & Kahneman, 1992 (cumulative prospect theory). DOI: null.
- R4. **Ambiguity and expected-utility generalisations** (L08 uses the maxmin rule; optional comparison with the Ellsberg
  evidence). Lead only: Schmeidler, 1989 (Choquet expected utility); Klibanoff, Marinacci & Mukerji, 2005 (smooth ambiguity,
  optional). DOI: null.
- R5. **Two-sided evidence on loss aversion and reference dependence** (L06 grade B/C claims need counter-evidence named).
  Topic only, no lead name: estimates of the loss-aversion coefficient from lottery-choice experiments, and published critiques
  of the magnitude and of the reference-point assumption. Needed before any magnitude is quoted.
- R6. **Lottery-choice elicitation designs** (project instrument design; optional). Lead only: Holt & Laury, 2002 (lottery-choice
  risk-aversion elicitation). DOI: null.

No line of this list is admitted until the architect runs `add_reference.py`. If none is admitted, L01 states EU as a
definition, L04 proves only the finite case, L06 and L07 carry the contested-evidence claims as grade-C with "No registry
source is cited for the magnitude" and no number, and the project reading list stays on the five curriculum keys.

---

## 9. Real-data policy

- **No real data.** The curriculum names no dataset for E3 (`curriculum/02-economics-finance-core.yaml:88-123` has no data
  field). No snapshot in `course/assets/data/market/MANIFEST.json` is about preferences or lotteries (the three snapshots are
  `fx_daily`, `fx_monthly` and `ust_daily`; `tools/data_sources.yaml`).
- **Labs and grader use generated data labelled SIMULATED**: generated lotteries, generated participants, and generated
  responses. Exact computations (closed forms, identities, exact FOSD checks) are not labelled SIMULATED.
- **Participant data is personal.** The student's in-browser answers are personal data. They are stored only in the browser
  (IndexedDB, as the program's progress store does, BLUEPRINT §6) or exported by the student; they never leave the browser and
  are never sent to a server. The page says so. No response is embedded in any file.
- **No `data-files`** on any lab; no MANIFEST entry; no `DATA_REQUESTS` entry. A real-subject elicitation dataset would be a
  request for the architect, not proposed here.
- **No figures.** The planner proposes none (CF1 Q6 precedent: no new JS kernels). If a CE-versus-γ curve is wanted, it needs
  a kernel and a test under `tests/test_figure_kernels.py` first (BUILDER_RULES §6.4) (§10 Q5).

---

## 10. Open questions for the architect (numbered; each needs a decision before the builders start)

1. **Hours split.** 8 lessons × 7 h = 56 h and a 14 h project (20%). Confirm, or give another split within §1 (lessons 6–12 h
   each; project 7–28 h).
2. **Curriculum lab model set.** The curriculum lab (yaml line 115) names "four preference models" without listing them.
   Recommendation: expected utility with CRRA (L03), the loss-averse prospect value (L06), maxmin over a stated prior set (L08),
   and Epstein–Zin under a stated timing (L05). Epstein–Zin needs a timing rule for a one-shot gamble: the planner recommends
   a two-period tree in which the gamble resolves in period 1 and the sure amount is paid in period 0 and period 1. Decision
   needed before L08 is built. Alternative: drop Epstein–Zin from the four-model lab and use probability weighting instead.
3. **Maximum likelihood, standard errors and confidence language without the S1 concepts.** The project's MLE and standard
   errors use S1 concepts (`maximum-likelihood-estimation`, `mle-asymptotic-normality`, `fisher-information`), which are outside
   the closure (`curriculum.json` `concepts`). Recommendation (CF1 Q2 precedent): write the likelihood, score and Hessian in plain
   calculus with M2 concepts, no link, and report a DAG_DEFECT. Alternative: add S1 as a prerequisite (a curriculum change;
   not proposed). Decision needed.
4. **Project model.** The curriculum names only "risk-aversion and loss-aversion parameters by MLE" (yaml 116–121). §6.2
   proposes a loss-averse power value without probability weighting (γ restricted to [0, 1) so the value is finite at the
   reference point; the γ = 1 log case is kept only for the `"crra"` model), a logit choice rule with precision κ, and three
   estimated parameters. Confirm, or name a different model. Freeze the three signatures in §6.2 before building (precedent: E1 Q4–Q5,
   AC4 Q7).
5. **Solution file name and in-page instrument.** Proposed `elicit.py` (module-local; no contract file exists). The in-page
   questionnaire needs a form. A plain HTML form with no JavaScript cannot store answers across a session; a small script is
   required, which is a new interactive component with no kernel test. Recommendation: a plain HTML form whose answers are
   exported as JSON in the browser, with no server and no figure. Confirm.
6. **Integer cents versus irrational CE.** CRRA and loss-averse CEs are irrational for general γ, so "Fraction throughout" fails
   for the five alternative implementations (§6.4). Recommendation: exact tests only for γ = 0 and the homogeneity identity;
   float implementations with one half-up rule, plus the near-half-cent guard in `instance.py`. Confirm, or restrict γ to
   integer values in the spec.
7. **Symbols.** Confirm the local symbols in §4 (ψ for EIS, θ for the EZ exponent, λ for loss aversion, α and δ for the
   value and weighting exponents, κ for the logit precision, `r_A`/`r_R` for the Pratt measures). The planner recommends not
   using β except for the EZ discount factor, and not registering any new symbol.
8. **Mutant count.** The brief asks for ten student-error mutants. `tools/mutate_graders.py` enforces only at least three
   (its line 29 check), and VERIFIER_RULES §2.6 says "at least 3". Confirm ten as the plan's requirement; the tool will not enforce it.
9. **Adversarial?** The memo is not an IC defence or a debate, so no question bank. Confirm.
10. **Plain terms outside the 12 concepts.** Terms such as "risk premium", "ambiguity", "reference point", "logit choice",
    "lottery", "prize", "certainty-equivalent risk premium" are used in prose and may be plain `<dfn>` without `data-concept`
    (the E1 precedent; `tools/check_dag.py` skips a `<dfn>` with no `data-concept`). Confirm; no GLOSSARY_REQUESTS are needed
    unless the architect wants a glossary entry.
11. **Epstein–Zin scope.** Two periods only; no infinite horizon, no fixed point, no Bellman operator (M7 is outside the closure;
    `curriculum.json` concept `bellman-equation`). Confirm.
12. **Count threshold for the identification test.** The "within 4 standard errors on at least 47 of seeds 0–49" threshold (§6.7)
    is a planner proposal to keep the deterministic suite from failing by chance. Confirm, or name another threshold.
13. **Reference requests.** Confirm which of R1–R6 (§8.1) the architect admits through `add_reference.py`. The planner recommends
    admitting R2 and R3 (they are needed for claims the lessons would otherwise have to omit) and deferring R1, R4 and R6.
    R5 must be admitted or the L06 and L07 contested-evidence claims are written without a magnitude.
14. **Scope words.** "market structures" and "welfare" are not used. Confirm that E3's scope words are limited to finite lotteries,
    the two-period Epstein–Zin case and the stated models (§2.1 item 4).

---

## 11. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit E3            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit E3
.venv/bin/python tools/check_projects.py --unit E3
.venv/bin/python tools/run_labs.py --unit E3               # --page L08 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/E/E3/L01.html                        # per page, after twins are written
.venv/bin/python tools/embed_labs.py course/modules/E/E3/L05.html --refresh lab-E3-L05-1  # after editing a twin
.venv/bin/python tools/run_graders.py --unit E3 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit E3 --seeds 0-9       # verifier only
.venv/bin/python tools/ledger.py --unit E3 --check                    # verifier only, after fragments exist
.venv/bin/ruff check tests/labs/E3 course/modules/E/E3/grader && .venv/bin/ruff format --check tests/labs/E3
.venv/bin/mypy                                                         # strict, repository configuration
```

Flags checked by the planner in the tool sources: `check_pages.py` (`--unit`, `--all`, `--page`), `check_dag.py`
(`--unit`, `--all`), `check_projects.py` (`--unit`, `--all`), `run_labs.py` (`--unit`, `--all`, `--page`), `run_graders.py`
(`--unit`, `--all`, `--seeds`, default 0–49), `mutate_graders.py` (`--unit`, `--all`, `--seeds`, default 0–9), `ledger.py`
(`--unit`, `--check`). The planner did not execute these commands.

Not run by builders: `page_smoke.py` (verifiers only, on a quiet machine). Repo-wide gates (`check_pages.py --all`,
`check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`, `render_curriculum.py` with the `git diff --exit-code`
check, `verify_refs.py --offline`, `fetch_data.py --check`) belong to the architect, once, before any merge. The full gate in
CLAUDE.md is not run per builder.

---

## 12. Tooling assumptions that do not hold for E3 (flagged)

1. **No Atlas milestone.** No atlas entry names E3 (`curriculum.json` `atlas`), and the project has no `atlas:` key
   (yaml 116–123). `check_projects.py` skips the contract check (lines 144–146). No `atlas/E3.contract.md` is needed. The
   planner did not draft one. `atlas/` contains `A15.contract.md` and `A8.contract.md` only.
2. **No debate.** E3 has no `debate:` key (yaml 88–123), so `check_pages.py` line 412 does not require a debate brief.
3. **Tier U graded `both`.** The rubric and exemplars are required by `check_projects.py` (`rubric_problems`, lines 58–72) and
   the grading words by `grading_problems` (lines 41–49). Two exemplars at two levels (level 4 and level 2).
4. **One curriculum lab, eight twins.** The curriculum names one lab (yaml 115). The plan adds one lab per lesson (M1 Q2 precedent)
   and three project labs; the curriculum lab is in L08 (§3).
5. **No tool checks the formulas.** Nothing in `tools/` checks the Epstein–Zin recursion, the maxmin rule or the
   dominance tests; the labs, the grader's oracle and the verifier do (VERIFIER_RULES §2.5 and §2.4).
6. **check_dag sees linked uses only.** Unlinked names of out-of-closure concepts (§7) pass `check_dag.py`. The verifier reads
   every lesson and the project for them.
7. **Prerequisite pages are not built.** `course/modules/E/` does not exist; `course/modules/M/` contains only M1 (M4 and M2
   are not built). The hub and lessons link their concepts through `concepts.html` anchors only.
8. **Mutant and alternative-implementation counts are not enforced by a tool.** `mutate_graders.py` enforces three mutants
   (§10 Q8); the five alternative implementations (§6.4) and the "ten" count are verifier duties that the ledger's `mutants`
   list will show.
9. **Labs must be exact or stated-precision.** Labs use the standard library. Power-function CEs are float; the lab prints the
   rounding rule and an error column where it compares to an exact value (§10 Q6).
10. **Registry strings match.** The five curriculum sources match their registry records (year, container, volume and issue);
    `check_pages.py` checks only that each key is verified, so the identity check is the verifier's (VERIFIER §2.1).

---

## 13. Output contract for the builders (BUILDER_RULES §10, filled)

```
UNIT: E3
FILES WRITTEN: (per owner; see §3)
HOURS: lessons=56 project=14 total=70 (curriculum=70)
SELF-CHECK: (run the §11 commands; report the exact output; do not report PASS for a check you did not run)
REFERENCE_REQUESTS: §8.1 R1–R6
NOTATION_REQUESTS: none required (optional: \CE macro, §4)
GLOSSARY_REQUESTS: none required (§10 Q10)
DATA_REQUESTS: none
CONTRACT_CHANGE_REQUESTS: none (no Atlas milestone)
DAG_DEFECTS: maximum-likelihood-estimation and its S1 relatives (project); convex-function (M7, L02/L04); bellman-equation (M7, L05 not named) — §7
KNOWN_LIMITATIONS: E1 and M4 unbuilt at planning; no registry locators for the five E3 papers; no empirical number
```

---

## 14. After the builders

1. Orchestrator integrates; runs the §11 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01–L02, L03–L04, L05–L06, L07–L08, project (writes the ten
   mutants and the five alternative implementations; scripts archived under `ledgers/E3/scripts/`), and cards.
3. Ledger at `ledgers/E3.verification.json` from fragments under `ledgers/E3/` (`tools/ledger.py --unit E3`).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed.

Architect decisions: pending (§10). This plan is the planner's proposal. Where the same issue arose in E1, M1, AC4 or CF1, the
precedent is reused as stated in §2 and §7.

## Architect decisions (2026-10-28, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank.
Module specifics: the four preference models of the curriculum lab are expected utility with CRRA, prospect theory, Epstein-Zin and max-min (alpha-MEU) ambiguity aversion; for a one-shot gamble Epstein-Zin uses a two-date timing convention stated on the page; certainty equivalents without a closed form are computed by a stated bisection with a stated tolerance and money stays in integer cents at the interface; MLE, convexity and Bellman are plain prose.
