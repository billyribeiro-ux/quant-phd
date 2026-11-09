# SC2 build plan: Itô Calculus & SDEs (planner output)

Unit: **SC2 · Itô Calculus & SDEs** · tier M · 100 h · prerequisite SC1 (closure M1, M2, M4, M5, M6, P0.1, SC1) · no Atlas
milestone · no debate key · grading `both` (autograder for the numerical engine, rubric for the workbook) · output directory
`course/modules/SC/SC2/` (part code `SC`) · lab twins `tests/labs/SC2/` · grader `course/modules/SC/SC2/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no file outside this plan.
Executors: Haiku builders A to E, then the cards builder F, then independent Haiku verifiers (VERIFIER_RULES). A builder never
verifies and never writes a ledger.

Evidence convention: every curriculum statement cites `file:line` read during planning. Anything not in the curriculum is marked
**NOT IN CURRICULUM**. Closure and concept-owner facts were computed by running `tools/coursekit.py`
(`prerequisite_closure("SC2")`, `concept_owner()`) through `.venv/bin/python`. Ledger and registry facts were read from the files
named. Tool behaviour that this planner did not re-read is marked "per SC1 plan" and cited to that plan.

**Status: BUILD MAY START ON THE BRANCH THAT CARRIES SC1 (`claude/fanout-b3`). MERGE IS GATED (§0.3): SC1 is not on `main`, and
the closure member P0.1 has neither a built module nor a ledger. No blocking defect in the content was found.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part SC, code `SC`, title "Stochastic Calculus & Continuous Time" | `curriculum/03-markets.yaml:489-491` |
| STUDIO-SC requires SC2 and M8 | `curriculum/03-markets.yaml:492-496` (requires at :495) |
| SC2 id `SC2`, title "Itô Calculus & SDEs" | `curriculum/03-markets.yaml:533-534` |
| Tier `M`, hours `100` | `curriculum/03-markets.yaml:535-536` |
| Prereqs `[SC1]` (only) | `curriculum/03-markets.yaml:537` |
| Core: "The Itô integral, Itô's lemma, GBM, Ornstein–Uhlenbeck, existence and uniqueness, Euler–Maruyama and Milstein." | `curriculum/03-markets.yaml:538-540` |
| `introduces` has 9 concepts, one per line: `ito-integral`, `ito-isometry`, `itos-lemma`, `geometric-brownian-motion`, `ornstein-uhlenbeck-process`, `sde-existence-uniqueness`, `euler-maruyama-scheme`, `milstein-scheme`, `strong-vs-weak-convergence` | `curriculum/03-markets.yaml:541-550` |
| Sources (free text, not keys): "Øksendal, Stochastic Differential Equations, 6th ed. (2003)"; "Kloeden & Platen, Numerical Solution of Stochastic Differential Equations (1992)" | `curriculum/03-markets.yaml:551-553` |
| Lab: "Euler–Maruyama strong vs. weak convergence." (the curriculum lab) | `curriculum/03-markets.yaml:554` |
| Project "Itô derivations workbook"; brief: "Derive the dynamics of ten transformed processes (log price, bond price, ratios), and verify each numerically."; deliverable "Workbook."; grading `both` | `curriculum/03-markets.yaml:555-561` (title 556, brief 557-559, deliverable 560, grading 561) |
| No `debate:` key and no `atlas:` key on SC2 or its project | `curriculum/03-markets.yaml:533-561` (absent); no entry in the `atlas` array of `curriculum/curriculum.json` names SC2 (planner check) |
| JSON row mirrors the YAML (id 9226; hours 9229; prereqs 9230; lab 9249; project title 9251, deliverable 9253; part "SC" 9256) | `curriculum/curriculum.json:9226-9256` |
| Hub row in the rendered curriculum | `CURRICULUM.md:699` (studio row :689) |
| Course-map placements (Core "Stochastic Calculus for Finance"; first-year sequence "Continuous-Time Finance") | `curriculum/meta.yaml:102`, `curriculum/meta.yaml:129` |
| Downstream modules that require SC2: SC3 `[SC2]`, SC4 `[SC2, M8]`, SC5 `[SC2]`, SC6 `[SC2, M7]` | `curriculum/03-markets.yaml:566`, `:592`, `:620`, `:649` |
| Nearest built prerequisite: SC1 (built; `course/modules/SC/SC1/`; ledger PASS, 758 rows, 0 FAIL, 0 UNVERIFIABLE) | `ledgers/SC1.verification.json` (top-level `verdict`); `course/modules/SC/SC1/` |
| Prerequisite closure of SC2 (computed): **{SC1, M1, M2, M4, M5, M6, P0.1}** | `tools/coursekit.py` `prerequisite_closure("SC2")`, run by the planner |
| Concepts whose owner module is in the closure: **91** (M1 14, M2 13, M4 19, M5 11, M6 15, P0.1 11, SC1 8; per-module counts as in `plans/SC1-build-plan.md` §0.1, plus SC1's own 8) | `tools/coursekit.py` `concept_owner()`; `plans/SC1-build-plan.md:42` |
| Owners of the 9 SC2 concepts: all SC2 | `tools/coursekit.py` `concept_owner()` (planner check) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 100 h (`curriculum/03-markets.yaml:536`). The tool rules:

- lesson `data-hours` 6 to 12 (`tools/check_pages.py:221-228`, the bound at :227);
- hub `data-hours-lessons + data-hours-project = 100` (`tools/check_pages.py:337-338`);
- project share 10 to 40 % of module hours, i.e. 10 to 40 h (`tools/check_pages.py:339-340`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py:341-342`);
- time-budget rows sum to `data-hours-project` and each row has a rationale (`tools/check_projects.py:107-120`).

Chosen split: **9 lessons × 8 h = 72 h; project 28 h (28 %)**. 72 + 28 = 100. Feasible. **No STOP condition on hours.**

### 0.3 Blocking issues and gates

**G1. SC1 is not on `main` (merge gate; not a build gate).** SC1 is committed on the current branch `claude/fanout-b3` only:
`git log main -- course/modules/SC/SC1` is empty and HEAD is not an ancestor of `main` (planner check). SC2 links to SC1 concept
anchors in `course/concepts.html` and its closure depends on SC1. **Recommendation (Q1):** builders branch from
`claude/fanout-b3`; the SC2 branch merges only after SC1 is on `main`.

**G2. Closure member P0.1 has no built module and no ledger (merge gate; SC2 uses none of its concepts).** `course/modules/`
contains AC, AP, BK, CF, CS, E, FC, LX, M, PC, S, SC (no P0); `ledgers/` has no `P0.1.verification.json`; the P0.1 plan exists
(`plans/P0.1-build-plan.md`, title line 1). The BLUEPRINT §4 mastery rule (a module unlocks only after its prerequisites' projects
pass, `BLUEPRINT.md` §4 table) cannot be checked for P0.1. **Recommendation (Q3):** record P0.1 as an agreed gap for the SC2 merge
because no SC2 content depends on it; no builder links a P0.1 concept.

**G3. Update to the SC1 plan (not blocking).** `plans/SC1-build-plan.md` §0.3 B1 says the M2 and M4 ledgers are FAIL and
UNVERIFIABLE. The current ledgers read PASS: `ledgers/M2.verification.json` (462 rows, 0 FAIL, 0 UNVERIFIABLE, verified 2026-11-09),
`ledgers/M4.verification.json` (240 rows, verified 2026-11-09). M1, M5 and M6 are PASS. The SC2 closure is therefore clean except
P0.1 (G2).

**G4. Øksendal edition string (non-blocking; same class as E5 B4).** The source string says "6th ed. (2003)"
(`curriculum/03-markets.yaml:552`). The registry record `oksendal2003stochastic` (`references/references.json:18497`) has year 2003
and no edition field. Cite the key only, with no edition typed in prose (§5, §7). **Decision (Q6):** keep the string or correct it
after the architect checks the edition.

**G5. The bond-price transform needs a model outside the closure (non-blocking; resolved in §5.2).** The brief's "bond price"
(`03-markets.yaml:557-559`) would naturally use the Vasicek model, whose concept `vasicek-model` is owned by FI2 (outside the
closure, §4 D5). **Resolution (Q8):** the spec supplies the affine bond-price form with instance constants; SC2 derives its Itô
dynamics only.

**G6. Atlas (none).** The brief does not name Atlas and no Atlas entry names SC2 (§0.1). No `atlas/SC2.contract.md` is needed.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

9 lessons × 8 h = 72 h; project 28 h; total 100 h. Concept counts per row sum to 1+1+1+1+1+1+1+1+1 = 9, each concept in exactly one
row (`curriculum/03-markets.yaml:541-550`).

| Lesson | Title (working) | Concept it defines (`introduces`, `03-markets.yaml:542-550`) | Lab (twin id, `tests/labs/SC2/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | The Itô integral for simple integrands | `ito-integral` | `lab-SC2-L01-1`: a step integrand fixed in advance; the variance of the Itô sum checked exactly as \(\sum_k H_k^2\,\Delta t_k\) in `Fraction`; a seeded Monte Carlo estimate with its \se. **SIMULATED** (Monte Carlo part) | 8 | A |
| L02 | Itô isometry and the \(L^2\) extension | `ito-isometry` | `lab-SC2-L02-1`: the left-endpoint sum has mean 0; the right-endpoint sum (anticipating) has mean exactly \(T\); Monte Carlo with \se. **SIMULATED** | 8 | A |
| L03 | Itô's lemma | `itos-lemma` | `lab-SC2-L03-1`: the pathwise identity \(B_H^2 = 2\sum_k B_{t_k}\Delta B_k + \sum_k \Delta B_k^2\) on a seeded path (residual printed); the sum of squared increments printed against \(H\). **SIMULATED** | 8 | A |
| L04 | Geometric Brownian motion | `geometric-brownian-motion` | `lab-SC2-L04-1`: the exact GBM solution against an Euler sample on the same increments; \(\E[S_H]\) against the closed form, Monte Carlo \se. **SIMULATED** | 8 | B |
| L05 | The Ornstein–Uhlenbeck process | `ornstein-uhlenbeck-process` | `lab-SC2-L05-1`: the exact OU mean and variance against a seeded Monte Carlo sample at several times; the variance limit printed against the stationary value. **SIMULATED** | 8 | B |
| L06 | Existence and uniqueness of SDE solutions | `sde-existence-uniqueness` | `lab-SC2-L06-1`: Picard iterates for the OU equation on a fixed seeded path; the sup-error of each iterate printed. **SIMULATED** | 8 | C |
| L07 | The Euler–Maruyama scheme | `euler-maruyama-scheme` | `lab-SC2-L07-1`: pathwise error of the Euler scheme for OU at step sizes \(H/2^k\), root-mean-square over paths, with \se. **SIMULATED** | 8 | C |
| L08 | The Milstein scheme | `milstein-scheme` | `lab-SC2-L08-1`: Milstein against Euler for GBM at the same step sizes; the Milstein correction term printed. **SIMULATED** | 8 | D |
| L09 | Strong versus weak convergence of SDE schemes | `strong-vs-weak-convergence` | `lab-SC2-L09-1` (**the curriculum lab**, `03-markets.yaml:554`): Euler for GBM, strong error (pathwise) and weak error (error in \(\E[S_H]\)) at step sizes \(H/2^k\), with \se. **SIMULATED** | 8 | D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 72/28 | none | none | - | A |
| project | Itô derivations workbook (`both`) | none | `lab-SC2-project-1` (rung 1), `lab-SC2-project-2` (rung 2, `class="lab completion"`), `lab-SC2-project-3` (rung 3 reference numbers) | 28 | E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`; the student deliverable `ito_checks.py` (§5.5) | none | none | - | E |
| cards | `cards.json` from L01–L09 | none | none | - | F (starts after A–D finish, §13) |

**Ownership rule.** Each builder writes only its lesson files and their twins. Builder A also writes `index.html` after L01–L03 exist.
Builder E writes the project, the grader, the project labs, the rubric and the exemplars, and does not depend on the lessons' prose;
it uses only the definitions and notation fixed in §2.3 and the lesson titles in §1. The cards builder F writes only `cards.json`.

**Ordering check** (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses SC1 `brownian-motion` (link to `course/concepts.html`), M4 `random-variable`, `normal-distribution`, M6 `filtration`
  (all in closure). Adapted and predictable processes are plain prose (§4, D13).
- L02 uses L01 (`ito-integral`) and M6 `conditional-expectation-l2`, `lebesgue-integral`.
- L03 uses L02 (`ito-isometry` for the \(L^2\) limit), SC1 `quadratic-variation`, M2 `taylor-theorem`.
- L04 uses L03 (`itos-lemma`) and M4 `normal-distribution`; the log-normal law is plain prose (D13).
- L05 uses L03 (`itos-lemma` for the integrating factor) and L02 (`ito-isometry` for the variance).
- L06 uses L02 (isometry bound in the Picard estimate), M5 `contraction-mapping`, `banach-fixed-point-theorem`, `cauchy-sequence`,
  `completeness-of-reals` (in closure). Gronwall's lemma and Lipschitz continuity are proved or defined inline (D13).
- L07 uses L06 (`sde-existence-uniqueness`) and L02; `expectation`, `variance` (M4).
- L08 uses L07 (`euler-maruyama-scheme`) and L03 (`itos-lemma` for the correction term).
- L09 uses L07 and L08 and M5 `uniform-convergence` (in closure) for the sup-norm error statements.

Hours check: 9 × 8 = 72 (hub `data-hours-lessons="72"`); project 28 (hub `data-hours-project="28"`); total 100.

**Builder allocation (flagged, Q2).** The task asks for "about three lessons per builder" for builders A to E. Nine lessons across
four lesson builders gives 3, 2, 2, 2, with E on the project (§1 table, Q2 for the alternative). At most five builders run at once
(§13).

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to SC2)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3–§8, `plans/SC1-build-plan.md` (nearest built prerequisite;
its grader and hub layout are the model for SC2), `plans/E5-build-plan.md` (structure template), `plans/FINAL-ARCHITECT-RULINGS.md`,
`/Users/billyribeiro/.fanout/fixer-rules.md`, and this file. Study `course/modules/SC/SC1/` for the hub, project, grader panel and
cards layout. `course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`, exact integer counts)
   or from `math` with a stated tolerance, and rounded only at display. A page that shows a rounded figure states its rounding rule.
   Precedent: `plans/E5-build-plan.md` §2.1 item 1; fixer rule line 6. Every mean, \se and residual figure follows this rule.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what the
   printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS. Every "checked" claim names the lab, line or test that did the check.
3. **Attribute nothing unread.** Only the registry keys `oksendal2003stochastic` and `kloeden1992numerical` (§7.1) may be cited, at
   book level, with no locator, no edition and no theorem number. No page, equation, edition or year is typed from memory. A result
   attributed to a book and not proved on the page is not graded T (BLUEPRINT §3 requires a proof on the page or a precise citation).
   Precedent: SC1 §2.1 item 3; `plans/E5-build-plan.md` §2.1 item 3. Fixer rule: unread standard content is "not stated here" or removed.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "almost surely", "converges", "the" in front of a path
   property, "strong", "weak", "exact" are used only where a proof, an exact check or a lab computes the claim. A simulation illustrates a
   theorem; it never verifies an almost-sure or pathwise statement, and the page says so (Q11).
5. **Define before use.** Each of the 9 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson and
   never before it. Terms outside the 9 concepts (adapted process, predictable process, simple integrand, Lipschitz, linear growth,
   log-normal law, Stratonovich integral, Picard iterate, root-mean-square error, weak order) appear in plain words at first use, with a
   plain `<dfn>` where they are defined and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`, per
   `plans/E5-build-plan.md` §2.1 item 5).
6. **Assumptions are numbered and explicit.** Every Theorem, Proposition, Lemma and Derivation block lists its numbered Assumptions
   (A1, A2, ...) before the statement. Required examples:
   - the Itô integral of a simple integrand assumes a partition and an adapted, piecewise constant integrand (A1);
   - the isometry extension assumes \(\E\int_0^H H_s^2\,ds<\infty\) (A2) and states the density argument as a sketch (§3, rule on sketches);
   - Itô's lemma assumes \(f\in C^2\) (A3);
   - existence and uniqueness assume a global Lipschitz condition and linear growth (A4), stated for the drift and the diffusion;
   - the Euler and Milstein order statements assume A4 and smoothness of the coefficients (A5, stated, not derived).
   Any result that uses a fact the page does not prove says "Assuming ..." in its statement (fixer rule, line 12).
7. **Grader rule.** The grader demands an exception type only for conditions §5.5 names (fixer rule, line 19). Any other invalid input
   may raise any exception or return a value.
8. **No money.** SC2 has no money output. Probabilities and moments are exact `Fraction` or `float` with a stated tolerance; counts are `int`.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container;
   escape `$` as `\$` inside math (fixer rule, line 14). `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py` lines 51-60, per SC1 plan §2.1 item 10;
    model `tests/labs/SC1/lab-SC1-L03-1.py`).
11. **Lab mutants are not graded (architect ruling 9 and fixer rule line 18).** Lab twins are demonstrations. A sentence that claims a
    lab asserts a property must match its code and output.
12. **Basis-explicit quantities.** Every mean, \se, residual and error figure states its basis: the grid (the step \(H/2^k\)), the
    number of paths, the seed, the \se, and the rounding rule.
13. **Discretization is never called exact.** A discrete-grid quantity is labelled as such. The Euler and Milstein paths are approximations
    of the solution, and any statement about a limit as the step tends to zero is a numbered Assumption or a grade-C lab result.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A derivation is T only if every
  step is shown (BUILDER_RULES §3.5). A proof sketch is never graded T; it is graded C with the skipped step named, or it is stated as
  an Assumption (fixer rule, line 12; FINAL-ARCHITECT-RULINGS 13).
- Concepts: §3 table. `<dfn>` only for the 9 concepts plus plain `<dfn>` for other defined terms. Links to closure concepts use
  `href="../../../concepts.html#<id>"` (from `course/modules/SC/SC2/` this is `course/concepts.html`). Links to earlier SC2 lessons use
  `href="Lnn.html#def-<id>"`. A lesson never links a concept defined later. A concept outside the closure is never linked (§4).
  SC1 concepts are linked by their `concepts.html` anchors (`brownian-motion`, `quadratic-variation`, `markov-property`,
  `continuous-time-martingale`), not by SC1 lesson pages (BUILDER_RULES §4.1).
- Labs: code lives once in `tests/labs/SC2/lab-SC2-Lnn-1.py` and `lab-SC2-project-1..3.py`. The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Lab ids match `lab-SC2-<page>-<n>` (`tools/check_pages.py` `check_lesson`).
  Standard library only (`fractions`, `math`, `random.Random(seed)`); no NumPy; no network; no warnings (`-W error`); under 10 s in
  Pyodide (builders time each twin under CPython and report it; no Pyodide timing claim is made without `page_smoke`).
- Labs use **no data files**. `data-files` is absent. No MANIFEST entry.
- SIMULATED label: on every lab section and figure that uses generated paths (all nine labs, except the exact identity in L03, which
  is labelled SIMULATED because its path is seeded), the project's worked example, and the grader instance. Exact finite identities
  (L01 Fraction sum, L03 pathwise identity) are stated as exact.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in code
  comments (fixer rule, line 14; precedent M1 "Convention (project Q5)").
- Banned strings (`tools/check_pages.py:58-72`, read as BANNED at :58): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis outside code.
- Lesson structure (BUILDER_RULES §4.2; `tools/check_pages.py:75` LESSON_SECTIONS): why-it-matters (at most 120 words), core content,
  inline lab, canon-breaks, misconceptions (at least 3), problems (at least 3 in each of mechanics, proof, empirical, research, each
  with `<details class="solution">`), key-results table, quiz (8–15 items, each with an explanation). **No debate brief** (no `debate`
  key, §0.1).
- Tier M: rungs 1–2 are kept to the minimum (BLUEPRINT §4; BUILDER_RULES §5.1).
- Output contract: the BUILDER_RULES §10 block, with the hours line filled from §1 and the REFERENCE_REQUESTS, NOTATION_REQUESTS,
  GLOSSARY_REQUESTS, DAG_DEFECTS and KNOWN_LIMITATIONS lines. Report PASS only for checks actually run.
- No `git commit`, no push, no branch changes. Builders write only under `course/modules/SC/SC2/` and `tests/labs/SC2/`
  (and `ledgers/` only for the verifier and the grader fixtures named in §5.8).

### 2.3 Notation (binding; `notation/notation.json`)

Registered macros this unit uses (`notation/notation.json`): `\E` (line 5, expectation), `\Prob` (line 9), `\Var` (line 13), `\Cov`
(line 17), `\R` (line 25), `\indic` (line 33), `\Normal` (line 37, \(\Normal(\mu,\sigma^2)\)), `\dto` (line 45), `\se` (line 101,
standard error).

Registered symbols that SC2 must **not** give another meaning (`notation/notation.json` `symbols` array):
- **`T`** (line 112) means the number of return observations in S1. **SC2 never uses `T` for a horizon.** Use **`H`** for the horizon,
  as SC1 does (`plans/SC1-build-plan.md` §2.3). The page says so once.
- **`\Phi`, `\Phi^{-1}`** (line 117): not used by SC2.
- **`\mathbb{Q}`** (line 147) and **`R^\ast`, `R^{e\ast}`, `R_f`** (lines 132–142): not used. Change of measure is SC3.
- **`\gamma_3`, `\gamma_4`** (lines 122, 127): not used.

Local symbols (defined on the lesson where first used, never redefined): \(B_t\) Brownian motion (SC1 convention); \(H\) horizon;
\(t_k\) grid times, \(\Delta t_k\) and \(\Delta B_k\) increments; \(\mu\) drift and \(\sigma\) volatility of GBM; \(\kappa\) mean-reversion
speed, \(\theta\) long-run level and \(x_0\) starting value of OU (SC1 used \(\theta\) for another quantity; SC1 and SC2 are separate
units and SC2 never uses SC1's meaning); \(H_k\) an integrand value on step \(k\); \(\bar t\) the maturity of the bond transform (the
letter \(M\) is not used, because SC1 uses \(M_t\) for the running maximum); \(p\) the power in the power transform; \(X_t\) the OU
process; \(S_t\) the GBM process.

NOTATION_REQUESTS: none new. The almost-sure and \(L^2\) arrows requested under SC1 (`plans/SC1-build-plan.md` §2.3) are not
registered; SC2 writes "almost surely" and "in \(L^2\)" in words.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson:

- **L01 `ito-integral`.** Adapted and predictable processes (plain dfn, D13). The Itô integral \(\int_0^H H_s\,dB_s\) of a simple
  integrand (piecewise constant on a partition, value at the left endpoint). Linearity and \(\E\int H\,dB=0\) (T, derived). The
  definition is for simple integrands only; the extension is L02. Remark: the integrand's value at the left endpoint is what makes the
  integral a martingale; the right endpoint is discussed in L02 (Stratonovich remark, plain).
- **L02 `ito-isometry`.** For simple integrands: \(\E[(\int H\,dB)^2]=\E\int H^2\,ds\) (T, full derivation from the independence of
  increments). The \(L^2\) extension to adapted integrands with A2 (\(\E\int H^2<\infty\)): the density argument is a **sketch**; it is
  stated as a sketch, names the skipped step (approximation in \(L^2\) of \(H\) by simple processes), and is graded C with the basis
  "proof sketch; step skipped: density of simple integrands". Lab: the left-endpoint sum has mean 0 and the right-endpoint sum has mean
  \(H\) (exact in expectation: \(\E[B_{t_{k+1}}\Delta B_k]=\Delta t_k\)), with Monte Carlo \se.
- **L03 `itos-lemma`.** Itô's lemma for \(f\in C^2\) in one variable with a standard Brownian motion: \(df(B_t)=f'(B_t)\,dB_t+\tfrac12 f''(B_t)\,dt\)
  (T for polynomial \(f\), full proof via the discrete identity and the quadratic variation of SC1; for general \(f\in C^2\) the proof is
  a sketch and is graded C, or the general statement is Assumption-backed; see Q5). The general time-dependent, diffusion-driven form
  \(df(t,X_t)\) with \(dX_t=a\,dt+b\,dB_t\) is stated and derived for the functions used in later lessons (T for polynomials and
  \(\exp\)). Remark: \(dB_t^2=dt\) is a convention for the quadratic variation, not an algebraic identity.
- **L04 `geometric-brownian-motion`.** The GBM SDE \(dS_t=\mu S_t\,dt+\sigma S_t\,dB_t\), its explicit solution
  \(S_t=s_0\exp\big((\mu-\sigma^2/2)t+\sigma B_t\big)\) (T, derived with Itô's lemma applied to \(\log\)), the log-normal law of
  \(S_t\) (plain prose "the logarithm is normal", T from `normal-distribution`), \(\E[S_t]=s_0 e^{\mu t}\) (T). The Itô correction
  \(-\sigma^2/2\) is the central example of L03. Lab: exact solution against Euler on the same increments.
- **L05 `ornstein-uhlenbeck-process`.** \(dX_t=\kappa(\theta-X_t)\,dt+\sigma\,dB_t\); its explicit solution by the integrating factor
  \(e^{\kappa t}\) and Itô's lemma (T); the mean \(\E X_t\) (T) and the variance \(\Var X_t\) by the isometry of L02 (T). The variance limit
  \(\sigma^2/(2\kappa)\) as \(t\to\infty\) (T). The long-run law as "the Gaussian law with that variance" (plain; the convergence in law
  is stated as a limit of the mean and variance, not as a theorem about the law). Remark: half-life is not defined here (D4).
- **L06 `sde-existence-uniqueness`.** Global Lipschitz condition (plain dfn: Lipschitz; A4) and linear growth. The Picard iteration
  and the \(L^2\) estimate, with **Gronwall's inequality proved inline as a lemma** (T; NOT IN CURRICULUM as a concept, D13). Uniqueness
  of solutions (T, proved). Existence (T if the Picard bound is completed on the page; otherwise a labelled sketch graded C). The
  banach fixed point (M5) is cited as the abstract analogue, with the contraction obtained on a weighted norm (plain prose, link to
  `banach-fixed-point-theorem`). Lab: Picard iterates for OU on a fixed path, the sup-error of each iterate printed.
- **L07 `euler-maruyama-scheme`.** The Euler–Maruyama scheme \(X_{k+1}=X_k+a(X_k)\Delta t+b(X_k)\Delta B_k\). The one-step local error
  in \(L^2\) of order \(\Delta t\) for the drift and of \(\Delta t^{1/2}\) for the stochastic part, under A4 (T, derived). The global
  strong order 1/2 is stated under A4 and A5 with a **sketch**; it is graded C with the basis "proof sketch; book-level attribution to
  `kloeden1992numerical` (no locator); lab L07". Lab: pathwise RMS error at step sizes \(H/2^k\).
- **L08 `milstein-scheme`.** The Milstein scheme adds \(\tfrac12 b(X_k)b'(X_k)(\Delta B_k^2-\Delta t)\) to Euler. Derivation from
  the Itô–Taylor expansion of \(b(X_t)\) using L03 (T for the one-step local error order \(\Delta t\)). The global strong order 1 is
  the same kind of sketch as L07 (grade C). Lab: Milstein against Euler for GBM, where \(b'\neq 0\).
- **L09 `strong-vs-weak-convergence`.** Strong error \(\E|X_H-X^{\Delta}_H|\) (or its root-mean-square form) and weak error
  \(|\E g(X_H)-\E g(X^{\Delta}_H)|\) for a test function \(g\). The difference in what each detects is stated in words. The numerical
  orders (strong 1/2 for Euler, weak 1 for Euler) are **observed** in the curriculum lab and graded C with basis `lab-SC2-L09-1`.
  Theory for the weak order is **not** stated on the page beyond the definition (the generator and Kolmogorov route is SC4, D7).

Lesson-level constraints:
- Each lesson's "Where the canon breaks" names at least one hypothesis whose failure breaks the result: a non-adapted integrand
  (L02, anticipating integrand; the right-endpoint sum has mean \(H\)), a non-\(C^2\) function (L03, \(|B_t|\)), a non-Lipschitz drift
  (L06, finite-time blow-up or non-uniqueness), a non-constant diffusion for Euler (L08), a discrete grid for a continuous statement (L07,
  L09), and a stochastic-volatility or square-root diffusion (plain mention only, D11).
- Each lesson names at least one misconception with its evidence (for example: "the Itô correction is zero because
  \(dB^2=dt\) is an identity" (L03); "Euler is exact for GBM" (L04: exact for the logarithm, not for the price path); "the Milstein
  term vanishes when the diffusion is constant" (L08)).
- No lesson uses a term from SC3 (change of measure, Girsanov, risk-neutral measure) or SC4 (PDE and Feynman–Kac). Those are outside
  SC2 and not in its closure (§4).

---

## 4. DAG problems (concepts that natural SC2 content would use outside the closure)

Prerequisite closure of SC2 (computed): **{SC1, M1, M2, M4, M5, M6, P0.1}**, 91 concepts (§0.1). Owners below are from
`concept_owner()` (planner run).

| Ref | Concept | Owner (outside closure) | Where natural SC2 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `monte-carlo-integration` | M8 | every simulation estimate in the labs and the grader ("the Monte Carlo average with its standard error") | Plain prose, no link, no `<dfn>`. Same as SC1 D8. |
| D2 | `pseudo-random-number-generator` | M8 | seeded paths (`random.Random(seed)`) | Plain prose "seeded generator"; no link. |
| D3 | `numerical-quadrature` | M8 | none (the Gaussian expectations are closed forms) | Not used. |
| D4 | `stationarity`, `mean-reversion-half-life` | S3 | the stationary OU law (L05) and the half-life \(\ln 2/\kappa\) | Not used as a concept. L05 states the variance limit as a limit; no half-life is defined. |
| D5 | `vasicek-model`, `short-rate-model`, `bond-price-yield` | FI2, FI1 | the bond transform in the project (brief "bond price", `03-markets.yaml:557-559`) | Spec-supplied affine form \(P(t,x)=\exp(-A(\bar t-t)-B(\bar t-t)x)\) with instance constants; no link; the model's origin is not claimed (Q8). |
| D6 | `black-scholes-formula`, `bsm-pde` | FC2, DV1 | a one-sentence remark that GBM is the stock model of option pricing (L04) | Optional plain prose; not used otherwise. |
| D7 | `feynman-kac-formula`, `kolmogorov-backward-equation`, `kolmogorov-forward-equation` | SC4 | the generator and the PDE view of L09's weak error | Not used. L09 states the weak error as a definition and a lab result. |
| D8 | `girsanov-theorem`, `martingale-representation-theorem`, `equivalent-martingale-measure`, `stochastic-discount-factor` | SC3, AP1 | drift change (not used) | Not used. |
| D9 | `log-return` | CS1 | the increment of \(\log S\) in L04 | Plain prose "change in the logarithm of the price"; no link. |
| D10 | `poisson-process`, `levy-process`, `compound-poisson-process` | SC5 | jump analogues (not used) | Not used. |
| D11 | `cir-model` (FI2), `heston-model` (DV3) | FI2, DV3 | the square-root and stochastic-volatility diffusions named as canon-breaks (L06, L08) | Plain mention only, no link, no analysis. |
| D12 | `policy-iteration` | SC6 | none | Not used. |
| D13 | NOT IN CURRICULUM: lognormal law, Lipschitz continuity, linear growth, Gronwall's lemma, adapted and predictable process, simple integrand, Stratonovich integral, Picard iterate, root-mean-square error, weak order | none | L01, L02, L04, L06, L07, L09 | Plain words at first use. Gronwall's lemma is proved inline in L06 (T) and not named as a concept. Lipschitz is a plain `<dfn>` in L06. |

**Missing prerequisite check.** Every mathematical concept SC2's natural content uses is in the closure: M2 `taylor-theorem`,
`derivative`, `partial-derivative`; M4 `normal-distribution`, `expectation`, `variance`, `random-variable`, `independence`; M5
`contraction-mapping`, `banach-fixed-point-theorem`, `uniform-convergence`, `cauchy-sequence`, `completeness-of-reals`; M6
`filtration`, `stopping-time`, `conditional-expectation-l2`, `lebesgue-integral`, `doob-maximal-inequality`, `martingale`; SC1
`brownian-motion`, `quadratic-variation`, `markov-property`, `continuous-time-martingale`. **No DAG_DEFECT**; D1 and D2 are the only
M8 uses and are plain prose, as in SC1.

`check_dag.py` checks linked uses only (`plans/E5-build-plan.md` §4 cites this). An unlinked use of D1–D13 passes the tool, so the
verifier reads every lesson for those names (VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): `both` grading, ladder, spec, budget, rubric, grader

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` RUNGS requires the order)

1. **Rung 1, worked example** (`lab-SC2-project-1`, SIMULATED): one fully solved, annotated derivation and check of the log-price
   transform (T1 in §5.2) on the instance generated by `make_instance(0)`. Each step has a "why" annotation. Tier M keeps it short (2 h).
2. **Rung 2, completion** (`lab-SC2-project-2`, `class="lab completion"`, SIMULATED): the Itô correction line of the log-price drift and
   the residual's correction line are replaced by `___`. Its twin is the completed solution; every page line equals the twin line or
   contains a blank (`tools/run_labs.py` docstring, per SC1 plan §5.1). Graded instantly (`tools/check_projects.py:90`).
3. **Rung 3, independent project** (graded by autograder and rubric, `both`): the workbook of ten derivations (§5.2) and the engine
   `ito_checks.py` (§5.5). `lab-SC2-project-3` is the rung-3 reference check: it prints the reference numbers for seed 0 that the
   engine's residual must reproduce (§5.5, draw-order contract).
4. **Rung 4, stretch** (optional, not graded): a two-dimensional transform (the ratio of two GBMs driven by correlated Brownian motions,
   with the two-dimensional Itô formula) checked with the same residual method. Recorded as optional; not in the autograder.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py:34` SPEC_TERMS requires context, inputs, required outputs, constraints, grading)

- **Context.** A derivatives analyst must show, for ten transformed processes, the Itô dynamics of each transform of two base processes
  (GBM and OU), and must check each dynamics numerically on generated instances. The deliverable is a workbook of derivations and an
  engine that checks them.
- **Inputs.** Generated instances from `make_instance(seed)` (§5.5). No dataset. Every instance is **SIMULATED**. No Atlas data (G6).
- **Base processes (given).** GBM: \(dS_t=\mu S_t\,dt+\sigma S_t\,dB_t\), \(S_0=s_0\). OU: \(dX_t=\kappa(\theta-X_t)\,dt+\sigma\,dB_t\),
  \(X_0=x_0\). Both have the Itô-exact solutions of L04 and L05.
- **The ten transforms.** Each is \(Y_t=f(t,\cdot)\) of a base state; the coefficients are defined on the base state \(x\) (the value
  of \(S\) or \(X\) at time \(t\)):
  1. \(Y=\log S\) (base GBM; domain \(S>0\)).
  2. \(Y=S^{p}\) (base GBM; \(p\) from the instance, \(p\notin\{0,1\}\); domain \(S>0\)).
  3. \(Y=1/S\) (base GBM; domain \(S>0\)).
  4. \(Y=e^{-rt}S\) (base GBM; \(r\) from the instance).
  5. \(Y=S/(a+S)\) (base GBM; \(a>0\) from the instance; domain \(S>0\)).
  6. \(Y=c+bX\) (base OU; \(b\neq 0\), \(c\) from the instance).
  7. \(Y=X^2\) (base OU).
  8. \(Y=\exp(X)\) (base OU).
  9. \(Y=P(t,X_t)=\exp\big(-A(\bar t-t)-B(\bar t-t)X_t\big)\) (base OU; \(\bar t\) the maturity, \(\bar t>H\)), with
     \(B(\tau)=(1-e^{-\kappa\tau})/\kappa\) and \(A(\tau)=a_0(B(\tau)-\tau)-a_1B(\tau)^2\), where \(a_0,a_1\) are instance constants.
     The spec gives \(A\) and \(B\) as the model input; their derivation is not SC2 content (D5). The student derives the dynamics of
     \(P\) only.
  10. \(Y=e^{\kappa t}X_t\) (base OU; time-dependent).
- **Instance ranges (planner proposal; the grader author fixes them and the verifier checks the spread).** \(\mu\in[-0.05,0.10]\),
  \(\sigma\in[0.1,0.5]\), \(\kappa\in[0.5,3.0]\), \(\theta\in[-0.2,0.2]\), \(s_0\in[0.5,2.0]\), \(x_0\in[-0.5,0.5]\), \(r\in[0,0.05]\),
  \(p\in\{2,3,0.5\}\), \(a\in[0.5,2.0]\), \(b\in[0.5,2.0]\cup[-2.0,-0.5]\), \(c\in[-1,1]\), \(a_0\in[0,0.2]\), \(a_1\in[0,0.05]\),
  \(H\in[0.5,2.0]\), \(\bar t\in[H+0.5,H+2.0]\).
- **Required outputs.** (a) `workbook.html` or `workbook.md` (student's choice of format; no notebook, SC1 Q8 precedent): one derivation
  per transform, each showing every Itô term (the drift term from \(\tfrac12 f''b^2\), the diffusion term, and the time term). (b)
  `ito_checks.py` with the three functions of §5.5. (c) The printed residual report for seed 0, with the grid, the path count, the
  mean, the \se, the band and the rounding rule.
- **Constraints.** Standard library only (`math`, `fractions`, `itertools`, `random`). Every printed number is recomputed from unrounded
  values and rounded once, at display, by the rule the spec states. The workbook states every Assumption (A3 for \(C^2\), the domain
  \(S>0\)). A simulation is not claimed to verify an almost-sure or pathwise identity: the residual is a discrete check on a grid (Q11).
- **Grading.** Both. The autograder checks `ito_checks.py` (§5.5); the rubric grades the workbook and the report (§5.4). The spec's
  grading entry must name **both** "autograder" and "rubric" (`tools/check_projects.py:38` GRADING_WORDS).
- **Reading list.** `ol.reading-list` cites `oksendal2003stochastic` and `kloeden1992numerical` (registry keys, §7.1). Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 28 h; every row needs a rationale; `tools/check_projects.py:107-120`)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved T1 derivation and check on the SIMULATED instance, annotated line by line |
| Rung 2, completion problem | 3 | Fill the two correction lines, then run the instant check |
| Ten derivations in the workbook | 10 | One Itô derivation per transform, every term shown, one Assumption block |
| Engine `ito_checks.py` with its tests | 8 | Three functions, the named ValueError conditions, the residual loop and the band |
| Residual report for seed 0 | 3 | Printed values, grid and path count, the band and rounding rule, what the check does and does not show |
| Self-assessment against the exemplars | 2 | Score the rubric, then compare with the annotated scoring |
| **Total** | **28** | Equals `data-hours-project` on the hub (§1) |

Check: 2 + 3 + 10 + 8 + 3 + 2 = 28.

### 5.4 Rubric (`table.rubric#rubric`; `tools/check_projects.py:58` `rubric_problems`)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to 1.
Every level descriptor is observable.

1. **Itô terms.** Level 4: every derivation shows the drift term from \(\tfrac12 f''b^2\), the diffusion term \(f'b\), and the time term,
   and names the Assumption (A3, the domain) used at each step. Level 1: "applies Itô's lemma".
2. **Derivation steps.** Level 4: every step of the GBM log derivation and the OU integrating-factor derivation is justified by a named
   rule or Assumption; a skipped step is named as a gap. Level 1: "the derivation is convincing".
3. **Numerical check.** Level 4: reports for every transform the residual mean, its \se, the band and the grid, with the rounding rule,
   and states whether the band was met. Level 1: "checks the results".
4. **Scope.** Level 4: states that the residual is a discrete check on a grid, not a proof of the continuous identity, and names the
   transforms whose residual is exact (T1, T6) and those whose residual is approximate (T2–T5, T7–T10). Level 1: "notes some caveats".
5. **Notation and reuse.** Level 4: uses \(H\) for the horizon and \(\bar t\) for maturity, names the SC1 results used (quadratic
   variation, Brownian motion) and the SC2 lessons used for each derivation. Level 1: "uses the notes".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, excerpts of a workbook (the T1 and T7 derivations
and the seed-0 report) on the seed-0 instance, annotated with the descriptors each passage meets or misses. Every number in the
exemplars is produced by `ito_checks.py` on seed 0; a builder never types one (SC1 §5.4 precedent). Self-assessment form
(`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in M1 and SC1). The page shows where the
student's scores diverge from the exemplar scores. Calibration: the verifier scores both exemplars blind, within one level per
criterion (VERIFIER §2.6). Blind scoring is done by a dedicated scorer that never opens the project page (FINAL-ARCHITECT-RULINGS 23).

The project is not adversarial: no question bank (architect default, as in SC1 §5.4).

### 5.5 Autograder: `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`, and the student deliverable `ito_checks.py`

Grader panel: `section.grader-panel#grader data-unit="SC2" data-grader="grader/" data-suite="test_project.py"
data-support="instance.py" data-solution="ito_checks.py" data-starter="starter.py" data-packages=""`
(`tools/check_projects.py:122-137`). `reference.py` and `instance.py` must exist in the grader directory (`check_projects.py:132`).
No `data-packages`: standard library only.

**Instance.** `make_instance(seed: int) -> dict` is deterministic. It returns keys `s0`, `x0`, `mu`, `sigma`, `kappa`, `theta`, `r`, `p`,
`a`, `b`, `c`, `a0`, `a1`, `H`, `tbar`, `n_steps` (int in 16 to 64), `n_paths` (int in 200 to 400), `seed`, and `label` set to
`"SIMULATED"`. Only valid instances are generated (ranges of §5.2; \(\sigma>0\), \(\kappa>0\), \(H>0\), \(\bar t>H\), \(s_0>0\)).
Seeds 0–49 must give materially different parameters (at least 45 distinct values of \(\sigma\), so the answers change, not only the
labels). Draws per call of `residual` are at most \(n_{\text{steps}}\times n_{\text{paths}}\le 2.6\times 10^4\), and the suite stays
under \(6\times 10^5\) draws per seed. The per-test limit of 5 s in Pyodide and the 60 s suite limit are measured by `page_smoke`
(not by the builder).

**Student deliverable and reference.** `ito_checks.py` (student) exposes three functions, with these frozen signatures:
- `value(transform: str, t: float, x: float, instance: dict) -> float`: \(f(t,x)\) for the ten transforms of §5.2 (the transform itself).
  Named conditions: an unknown `transform` raises `ValueError`; `x <= 0` raises `ValueError` for transforms 1–5 (domain \(S>0\)).
- `coefficients(transform: str, t: float, x: float, instance: dict) -> tuple[float, float]`: the drift \(\mu_Y(t,x)\) and diffusion
  \(\sigma_Y(t,x)\) of \(Y=f(t,X_t)\) at base state \(x\), so that \(dY=\mu_Y\,dt+\sigma_Y\,dB\). Named conditions as for `value`.
- `residual(transform: str, instance: dict, n_steps: int) -> tuple[float, float]`: mean and \se over `instance["n_paths"]` base paths
  on \([0,H]\) with `n_steps` steps, of the discrete Itô residual
  \(R=\big[f(H,x_N)-f(0,x_0)\big]-\sum_k\big[\mu_Y(t_k,x_k)\,\Delta t+\sigma_Y(t_k,x_k)\,\Delta B_k\big]\),
  where \(x_k\) is the base path and \(\Delta t=H/n_{\text{steps}}\). The base path is the **exact** GBM solution on the grid for
  transforms 1–5 (\(x_{k+1}=x_k\exp((\mu-\sigma^2/2)\Delta t+\sigma\Delta B_k)\)) and the **Euler** scheme for the OU base for transforms
  6–10 (\(x_{k+1}=x_k+\kappa(\theta-x_k)\Delta t+\sigma\Delta B_k\)), with \(\Delta B_k=\sqrt{\Delta t}\,z_k\) and \(z_k\) the draw of the
  contract below. The OU base is Euler so that the affine transform 6 has an exactly affine increment. Named conditions: unknown `transform` raises `ValueError`; `n_steps < 1` raises
  `ValueError`; `instance["n_paths"] < 2` raises `ValueError`.
- **Draw-order contract (stated on the page).** One RNG per call, `random.Random(instance["seed"])`, consumed **path-major**: for
  path \(j\) then step \(k\), one `gauss(0.0, 1.0)` draw. A different draw order is not valid. Fixed by FINAL-ARCHITECT-RULINGS 21:
  an alternative on another order cannot be valid, and the page says so. The suite enforces the order by pinning the seed-0 residual of
  transform 7 to the value printed by `lab-SC2-project-3` (a fixture of one simulation output, not a coefficient; Q9).

`reference.py` is the full solution (excluded from deployment, BLUEPRINT §7). `starter.py` raises `NotImplementedError` in every
function, and the suite must fail on it.

**Tests (`test_project.py`).** Property and number checks, each against the instance's own parameters, never a hard-coded coefficient:
- `value`: equals the §5.2 formula to 1e-12 for each transform at three \((t,x)\) points per instance; `x = 1e-9` for transform 1 is
  accepted and `x = 0` raises `ValueError` (both sides of the boundary).
- `coefficients`: each \(\mu_Y\) and \(\sigma_Y\) equals the grader's own Itô coefficient, computed from `value` by central differences
  (step \(10^{-5}\) in \(t\) and in \(x\)) and the base coefficients, to a tolerance \(10^{-6}\max(1,|\text{expected}|)\). Exact checks:
  \(\sigma_Y\) of transform 1 equals \(\sigma\), of transform 6 equals \(b\sigma\), of transform 10 equals \(e^{\kappa t}\sigma\), each to 1e-12.
- `coefficients` named `ValueError`: unknown name; \(x=0\) for transforms 1–5 raises; \(x=10^{-9}\) for transform 1 does not.
- `residual`, exact cases: for transform 1 (exact GBM base; the log increment is exactly \((\mu-\sigma^2/2)\Delta t+\sigma\Delta B_k\)) and
  transform 6 (Euler OU base; the affine map gives exactly the Euler increment) the residual is zero pathwise to 1e-10. The maximum
  absolute residual over paths is checked, not only the mean. Transform 10 is **not** exact (its time factor changes within the step),
  and it is tested in the statistical case.
- `residual`, statistical cases: for transforms 2–5 and 7–10 the mean residual lies within the band \(5\,\se + A\), where \(A\) is the
  allowance for the \(O(\Delta t)\) discretization bias. The planner's constraint, which the grader author must check on seeds 0–49 and
  report on the page: \(A\) is smaller than one quarter of the smallest Itô term that the mutants of §5.6 remove, namely
  \(\sigma^2 H/2\) over the instance ranges. If the instance ranges cannot satisfy this at the instance's `n_steps`, the statistical
  residual tests are dropped, and the coefficient tests (which kill every mutant of §5.6 by a difference of at least \(\sigma^2/2\) in
  the drift) carry the kill (Q10). The allowance is not \(c\,H\Delta t\) with a constant fixed in advance: the bias depends on
  \(\kappa^2(\theta-x)^2\) along the path, so it is a Taylor-remainder bound computed by the grader author.
- `residual` named `ValueError`: `n_steps = 0` raises and `n_steps = 1` does not; `n_paths = 1` raises and `n_paths = 2` does not;
  unknown name raises.
- `make_instance`: deterministic (same seed, same dict); all 50 seeds valid; at least 45 distinct \(\sigma\) values across seeds 0–49.
- Failure messages name the violated property and hint at the concept (for example, "the drift of a function of a diffusion needs the
  second-order term; see the Itô lemma lesson"); they never print the expected value (`__tracebackhide__` in every test helper that
  compares a value; fixer rule, line 19).

**Mutants.** Ten student-error mutants (§5.6), written as single-change copies of `reference.py` under `ledgers/SC2/mutants/`. Each must
be killed by `test_project.py` on seeds 0–9 (`tools/mutate_graders.py --unit SC2 --seeds 0-9`).

**Alternative correct implementations.** Five, of different styles, pass seeds 0–49 (§5.7). They live under
`ledgers/SC2/scripts/alternatives/` and are verifier-written (FINAL-ARCHITECT-RULINGS 10).

**Statistical tolerance.** The Monte Carlo band is \(5\,\se\) (SC1 §5.5 precedent), so 50 seeds give a negligible false-failure rate
(Q10).

### 5.6 Ten student-error mutants (written by the verifier; each must fail at least one test on seeds 0–9)

Each is a complete module in `ledgers/SC2/mutants/<name>.py`, with the first docstring line naming the student error.

1. Log-price drift omits the Itô correction: `coefficients(1, ...)` returns \(\mu\) instead of \(\mu-\sigma^2/2\).
2. Log-price diffusion scaled by the state: returns \(\sigma x\) instead of \(\sigma\) (chain-rule factor applied twice).
3. Reciprocal drift has the sign of the Itô term flipped: returns \((-\mu-\sigma^2)/x\) instead of \((\sigma^2-\mu)/x\).
4. Discounted price drift uses \(+r\) instead of \(-r\) (sign of the discount factor).
5. Power transform drift omits the \(p(p-1)\sigma^2/2\) term.
6. Affine transform diffusion uses \(\sigma\) instead of \(b\sigma\) (scale forgotten).
7. Square-of-OU drift omits the \(\sigma^2\) term of \(d(X^2)\).
8. Exponential-of-OU drift omits the \(\tfrac12\sigma^2 e^{X}\) term.
9. Bond price diffusion writes \(-\sigma B(\bar t-t)\) instead of \(-\sigma B(\bar t-t)\,P\) (additive instead of multiplicative).
10. Time-scaled OU drift omits the product-rule term of \(e^{\kappa t}\): uses \(e^{\kappa t}\kappa(\theta-x)\) instead of \(\kappa e^{\kappa t}\theta\).

If a mutant turns out to be equivalent on every input the page states, it moves to `ledgers/SC2/equivalent/` with a README proof
(FINAL-ARCHITECT-RULINGS 9). No survivor stays in `ledgers/SC2/mutants/`. A mutant that differs only inside a stated tolerance is equivalent
under ruling 22.

### 5.7 Five alternative correct implementations (verifier-written; must all pass seeds 0–49)

Written as test-only fixtures under `ledgers/SC2/scripts/alternatives/`, each with the same draw order (§5.5):
(1) `coefficients` as a table of closed-form lambdas per transform, `residual` by a per-step loop;
(2) `coefficients` by generic numerical Itô: \(\mu_Y=\partial_t f+a\,\partial_x f+\tfrac12 b^2\partial_{xx}f\) and \(\sigma_Y=b\,\partial_x f\) with central
    differences of `value` (step \(10^{-5}\)), to the tolerance of §5.5;
(3) `coefficients` by a class per transform with `drift` and `diffusion` methods and a dispatch dictionary;
(4) `coefficients` written in the state \(y=f\) (for transform 1, \(x=e^{y}\)) and inverted before evaluation, with the same closed forms;
(5) `residual` by cumulative sums over the step increments (no per-step loop), with `coefficients` by closed forms.
Alternatives (2) and (4) are valid only if they pass the tolerance tests on all 50 seeds; a numerical alternative that is wrong on an exact
rule is a mutant, not an alternative (FINAL-ARCHITECT-RULINGS 10).

### 5.8 Grader fixtures and what the verifier writes

The verifier writes the 10 mutants and the 5 alternatives (§5.6–5.7), runs `tools/mutate_graders.py --unit SC2 --seeds 0-9`, and runs
`tools/run_graders.py --unit SC2 --seeds 0-49` on the reference and on each alternative (the alternatives are run by a script kept under
`ledgers/SC2/scripts/`, VERIFIER §3). Each mutant's killing test is recorded in the ledger's `mutants` list. The page's collect-only test
count is updated after the suite is final (fixer rule, line 19).

---

## 6. Real-data policy

- **No real data.** SC2 is stochastic-calculus theory. The labs and the grader use generated paths, exact identities and closed forms.
- **Not embedded, and not needed.** `tools/data_sources.yaml` (ids `fx_daily`, `fx_monthly`, `ust_daily`; the `rejected:` block) has no
  series for SC2 and none is requested.
- Generated paths and instances are labelled **SIMULATED** on every page section and in the grader docstring (BLUEPRINT §5.3).
- No `data-files` attribute on any lab. No MANIFEST entry. No DATA_REQUESTS.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in SC2 |
|---|---|---|---|
| `oksendal2003stochastic` | Øksendal, *Stochastic Differential Equations*; Crossref book; year 2003; DOI 10.1007/978-3-642-14394-6; `status: verified`; `used_by: ["SC2"]` (`references/references.json:18497`, `:18529`); source string matches `curriculum/03-markets.yaml:552` except the edition (G4) | verified | book-level citation for the SDE theory of L03, L06; reading list; cite at book level, no locator, no edition typed |
| `kloeden1992numerical` | Kloeden & Platen, *Numerical Solution of Stochastic Differential Equations*; Crossref book; year 1992; DOI 10.1007/978-3-662-12616-5; `status: verified`; `used_by: ["SC2"]` (`references/references.json:14715`, `:14751`); matches `curriculum/03-markets.yaml:553` | verified | book-level citation for the scheme theory of L07–L09 (the attributed orders are grade C, §3); reading list |

Registry keys that exist but are **not** used by SC2 by default (owned by other modules; use needs architect approval, Q7):
`shreve2004stochastic` (SC1, `references/references.json:20732`), `glasserman2003monte` (M8), `vasicek1977equilibrium`
(`references/references.json:22046`, FI2), `heston1993closed` (DV3), `williams1991probability` (M6).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Itô (lead only; author name only, no work typed)", year: "not typed", title: "the original work introducing the stochastic integral with respect to Brownian motion (lead only; record not typed)", venue: "not typed", needed_for: "L01 and L03 attribution of the integral and of the lemma, if the architect permits attribution (the curriculum names no original paper for SC2)", confidence: "the need is a lead; no record is in the registry (no key matches `ito` or `itô` in references/references.json; planner check)"}
- {doi: null, authors: "Milstein (lead only)", year: "not typed", title: "the original work introducing the scheme with the Milstein correction (lead only; record not typed)", venue: "not typed", needed_for: "L08 attribution of the scheme, if the architect permits it", confidence: "the need is a lead; no registry record found by the planner"}
- {doi: null, authors: "Maruyama (lead only)", year: "not typed", title: "the original work on the Euler scheme for stochastic differential equations (lead only; record not typed)", venue: "not typed", needed_for: "L07 attribution of the scheme, if the architect permits it", confidence: "the need is a lead; no registry record found by the planner"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; `references/authorities.yaml`).
Until resolved, the lessons teach the schemes with derivations and no empirical or historical attribution.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for SC2 (`curriculum/curriculum.json` `atlas` array: no entry names SC2; §0.1) and SC2's
project has no `atlas:` key (`curriculum/03-markets.yaml:555-561`). `tools/check_projects.py:144-146` skips the contract check when no
`atlas` key is present. No `atlas/SC2.contract.md` is needed or drafted.

---

## 9. Cards builder (Builder F, after A–D finish)

- `course/modules/SC/SC2/cards.json`, ids `SC2-c001` upward, `lesson` in L01–L09, one card per definition, theorem statement, key
  identity, key result and misconception (BUILDER_RULES §7). `tools/check_pages.py:366` `check_cards` checks the id prefix, the lesson
  existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab L04, exact GBM solution (derivation 1)"`. A result that depends on A2 or A5 says so in its `basis`. A sketch-proved result
  is graded C with its basis, never T (§3).
- Cite `oksendal2003stochastic` or `kloeden1992numerical` only for an attributed or book-level claim. `cite` is `[]` where the card is a
  model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.
- Ids need not be sequential (FINAL-ARCHITECT-RULINGS 2).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit SC2            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit SC2
.venv/bin/python tools/check_projects.py --unit SC2
.venv/bin/python tools/embed_labs.py course/modules/SC/SC2/L01.html            # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/SC/SC2/L09.html --refresh lab-SC2-L09-1   # after editing a twin
.venv/bin/python tools/run_labs.py --unit SC2               # --page L09 for one lesson
.venv/bin/ruff check tests/labs/SC2 course/modules/SC/SC2/grader && .venv/bin/ruff format --check tests/labs/SC2 course/modules/SC/SC2/grader
.venv/bin/mypy --no-incremental <each file touched>         # strict, repository configuration
```

Grader (builder E; the reference must pass before the project is handed off):

```bash
.venv/bin/python tools/run_graders.py --unit SC2 --seeds 0-49
```

Verifier only (not run by builders): `.venv/bin/python tools/mutate_graders.py --unit SC2 --seeds 0-9`;
`.venv/bin/python tools/page_smoke.py --unit SC2` (on a quiet machine, alone, timing-sensitive); and
`.venv/bin/python tools/verify_refs.py --unit SC2` (the unit ledger's run, VERIFIER §2.1).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. No new dataset is added, so `fetch_data.py --check` is not required by SC2.

Flag checks: `tools/check_pages.py` and `tools/check_dag.py` accept `--unit`; `tools/check_projects.py` accepts `--unit`; `tools/run_labs.py`
accepts `--unit` and `--page`; `tools/run_graders.py` accepts `--unit` and `--seeds`; `tools/mutate_graders.py` reads its mutants from
`ledgers/<UNIT>/mutants/*.py` (per SC1 plan §10, not re-read by this planner).

The planner did not execute the builder commands. Only the coursekit closure, concept-owner and ledger reads were run (§0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on the SC2 project (`curriculum/03-markets.yaml:555-561`) and no Atlas entry names SC2 (§8).
   `tools/check_projects.py:144-146` skips the contract check.
2. **No debate.** SC2 has no `debate:` key (`curriculum/03-markets.yaml:533-561`), so `tools/check_pages.py:412-413` does not require a
   debate brief. No contested empirical claim is planned, so the two-sided rule (BUILDER_RULES §2.5) is not triggered by SC2 content.
3. **Both grading.** The autograder, the rubric and two exemplars at two levels are required (`tools/check_projects.py:122-139`; grader
   panel and rubric checks; `GRADING_WORDS` at :38).
4. **One curriculum lab, nine lab twins.** The curriculum names one lab (`03-markets.yaml:554`); BUILDER_RULES §3.4 requires a numerical
   check per key formula; the plan adds one lab per lesson (SC1 precedent, `plans/SC1-build-plan.md` §11 item 4). The curriculum lab is
   `lab-SC2-L09-1`.
5. **Prerequisite gates.** SC1 is not on `main` (G1); P0.1 has no ledger or built module (G2). Prerequisite links go to concept anchors
   (`course/concepts.html`), not to SC1 lesson pages.
6. **Tier M rung rule.** Rungs 1–2 are minimal from tier M upward (BLUEPRINT §4). Rung 1 is 2 h and rung 2 is 3 h.
7. **Notation.** `T` (registered S1 meaning) is never used for a horizon; `H` is used (§2.3).
8. **Runtime.** The Euler, Milstein and residual loops stay within the draw budgets of §5.5. Builders time each twin under CPython and
   report it; the verifier measures Pyodide timing with `page_smoke`.
9. **Lab mutants.** Lab twins are not mutation-tested (FINAL-ARCHITECT-RULINGS 9; fixer rule, line 18). Project graders are.
10. **Five agents at a time.** Builders A–E run together where the dependency allows; F starts only after A–D finish (§13).
11. **Sketch-proved results.** Several convergence statements are graded C (§3); a verifier must not raise them to T.

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **G1, SC1 on `main`.** **RECOMMENDED:** builders start on `claude/fanout-b3`, which contains SC1; the SC2 branch merges only after
   SC1 is on `main`. Alternative: merge SC1 first.
2. **Lesson count, hours and builder allocation.** **RECOMMENDED: 9 lessons × 8 h = 72 h; project 28 h (28 %); builders A (L01–L03 and
   index), B (L04–L05), C (L06–L07), D (L08–L09), E (project).** Alternatives inside the rules: 8 lessons × 9 h with a 28 h project
   (SC1 pattern, builders A: L01–L02 and index; B: L03–L04; C: L05–L06; D: L07–L08); or 3 lesson builders at 3, 3 and 3 lessons with D
   unused (three builders A, B, C, then E).
3. **G2, P0.1 in the closure.** **RECOMMENDED: record P0.1 as an agreed gap for the SC2 merge; no SC2 content uses a P0.1 concept.**
   Alternative: build P0.1 first.
4. **Discrete-simulation tools (D1, D2).** `monte-carlo-integration` and `pseudo-random-number-generator` are owned by M8, outside the
   closure. **RECOMMENDED: plain prose, no link, as in SC1 D8.** Alternative: add M8 to SC2's prerequisites (a curriculum change;
   `curriculum/03-markets.yaml:537` would change). Not recommended, because STUDIO-SC already requires M8 and the labs need only seeded
   sampling.
5. **Itô's lemma and Gronwall (L03, L06).** **RECOMMENDED:** prove the polynomial case of Itô's lemma fully (T); state the general
   \(C^2\) case with a labelled sketch graded C; prove Gronwall's inequality inline (T), so no outside concept is needed. Alternative: state
   the general lemma as Assumption A3 without a sketch.
6. **Øksendal edition (G4).** **RECOMMENDED: keep the curriculum string; the page cites `oksendal2003stochastic` with no edition or year
   in prose.** Alternative: the architect checks the edition and corrects `curriculum/03-markets.yaml:552`.
7. **Book-level attribution (§7.1).** **RECOMMENDED:** attribute the scheme orders and the SDE theory to the two keys at book level, with
   no locator; the attributed result is graded C with its lab basis unless the page proves it (§3). No other registry key is cited.
8. **Bond-price transform (G5, D5).** **RECOMMENDED:** the spec supplies \(A\), \(B\) and the instance constants \(a_0\), \(a_1\); the
   student derives only the dynamics of \(P\); the page does not claim the formula is a market model. Alternative: drop transform 9 and use a
   ninth transform of the OU process (the count of ten is then kept with another OU transform).
9. **Pinned fixture (draw-order contract).** **RECOMMENDED:** the suite pins the seed-0 residual of transform 7 to the value printed by
   `lab-SC2-project-3`, to 1e-12, so a different draw order fails. The pinned value is a simulation output, not a coefficient, and it does not
   reveal the answer for any other transform. Alternative: no pin; the order is stated and the verifier checks it by reading.
10. **Monte Carlo band and allowance.** **RECOMMENDED:** band = \(5\,\se + A\), where \(A\) is a Taylor-remainder bound on the \(O(\Delta t)\)
    bias, computed by the grader author, reported on the page, and required to be below one quarter of \(\sigma^2 H/2\) over the instance
    ranges (§5.5). If the constraint fails, drop the statistical residual tests and let the coefficient tests carry the kill. Exact residual
    tests (transforms 1 and 6) at 1e-10. Confirm this rule, or name an alternative.
11. **Exact versus simulated checks.** **RECOMMENDED:** exact identities (L01 sum, L03 pathwise identity, the exact residual cases) plus
    seeded paths with \se; the page states that a simulation does not verify a pathwise or almost-sure identity.
12. **Project deliverable "Workbook."** `03-markets.yaml:560`. **RECOMMENDED: a workbook document (HTML or Markdown, student's choice)
    graded by the rubric, plus `ito_checks.py` graded by the autograder and the seed-0 report; no notebook** (SC1 Q8 precedent).
13. **Rung lengths and placement quiz.** **RECOMMENDED: rung 1 is 2 h, rung 2 is 3 h (§5.3); hub placement `section.quiz#placement
    data-mastery="0.8"` with nine items, at least two `data-skill` items on the rung 1–2 skills (the log-price correction and the completion
    line), as in SC1 Q18.**
14. **Lab placement of the curriculum lab.** **RECOMMENDED: the curriculum lab `lab-SC2-L09-1` sits in L09 with the strong and weak
    convergence definitions; L07 and L08 carry their own scheme labs.**
15. **Terms and figures.** **RECOMMENDED:** no live figures and no new JS kernel (architect default); terms in §4 D13 are plain prose with
    no `data-concept`; no GLOSSARY_REQUESTS entry.
16. **DAG.** **RECOMMENDED: confirm that SC2 needs no prerequisite change (§4, "Missing prerequisite check").**

---

## 13. After the builders

1. **Scheduling (five agents at most).** Builders A, B, C, D and E start together where their files do not depend on each other. Builder
   E does not depend on lesson prose, so it starts first. Builder F (cards) starts when A–D have finished; it may overlap E. The
   orchestrator integrates after all six have reported.
2. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
3. Independent Haiku verifiers in fresh checkouts, by slice: L01–L03 (includes the Itô integral and the lemma's proof status), L04–L05
   (includes the GBM and OU labs), L06–L07 (includes the Picard and Euler sketch grades), L08–L09 (includes the curriculum lab), project
   (rubric and exemplar calibration; the engine's ten mutants and five alternatives). Failing rows return to the builder that owns the
   file, with only the failing rows.
4. Ledger at `ledgers/SC2.verification.json`; scripts that back a row under `ledgers/SC2/scripts/` (VERIFIER §3); mutants under
   `ledgers/SC2/mutants/` (equivalents under `ledgers/SC2/equivalent/` with a README proof only).
5. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. G1 and G2 must be resolved or
   named as honest gaps first (§0.3).

Architect decisions: pending (§12). Where the architect answers "follow the plan's recommendation", the recommendation in §12 applies.

## Architect decisions

Pending. This plan is the planner's proposal. Each of Q1–Q16 in §12 needs a decision before the named builder starts; Q1, Q2 and Q3 are
needed before the merge, and Q4, Q5, Q8, Q9 and Q10 before builders A, C and E write their files.
