# SC1 build plan: Stochastic Processes (planner output)

Unit: **SC1 · Stochastic Processes** · tier M · 100 h · prerequisite M6 (closure M1, M2, M4, M5, M6, P0.1) · no Atlas
milestone · no debate key · grading `both` (autograder for the verification engine, rubric for the typeset proofs) ·
output directory `course/modules/SC/SC1/` (part code `SC`) · lab twins `tests/labs/SC1/` · grader `course/modules/SC/SC1/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no file outside this plan.
Executors: Haiku builders A to E, then the cards builder F, then independent Haiku verifiers (VERIFIER_RULES).
A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement cites `file:line` read during planning. Anything not in the curriculum is
marked **NOT IN CURRICULUM**. Closure and concept-owner facts were computed by running `tools/coursekit.py`
(`prerequisite_closure("SC1")`, `concept_owner()`) through the repo venv. Ledger and registry facts were read from the
files named.

**Status: BUILD MAY START. MERGE IS GATED (§0.3). Two blocking items (B1, B2) must be decided before the merge; neither
blocks the first builder.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part SC, code `SC`, title "Stochastic Calculus & Continuous Time" | `curriculum/03-markets.yaml:489-491` |
| STUDIO-SC requires SC2 and M8 (SC1 is not a studio prerequisite) | `curriculum/03-markets.yaml:492-496` (requires at :495) |
| SC1 id and title "Stochastic Processes" | `curriculum/03-markets.yaml:505-506` |
| Tier `M`, hours `100` | `curriculum/03-markets.yaml:507-508` |
| Prereqs `[M6]` (only) | `curriculum/03-markets.yaml:509` |
| Core: "Brownian motion and its construction, quadratic variation, continuous-time martingales, the Markov property, stopping times, reflection principle." | `curriculum/03-markets.yaml:510-512` |
| `introduces` has 8 concepts (one per line) | `curriculum/03-markets.yaml:513-521` |
| Sources (free text, not keys): "Shreve, Stochastic Calculus for Finance II (2004)"; "Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991)" | `curriculum/03-markets.yaml:522-524` |
| Lab: "Quadratic-variation convergence." | `curriculum/03-markets.yaml:525` |
| Project "Reflection principle verified"; brief: "Prove the reflection principle and the running-maximum distribution, then verify both against simulation with proper discretization-bias handling."; deliverable "Proof plus verification."; grading `both` | `curriculum/03-markets.yaml:526-532` (title 527, brief 528-530, deliverable 531, grading 532) |
| No `debate:` key and no `atlas:` key on SC1 or its project | `curriculum/03-markets.yaml:505-532` (absent); no `atlas` array entry names SC1 (planner check: 0 hits in `curriculum/curriculum.json` `atlas`) |
| JSON row mirrors the YAML (id at line 9194; hours 9197; prereqs 9198-9200; sources 9212-9215; lab 9216; project 9217-9222; part "SC" 9223) | `curriculum/curriculum.json:9194-9223` |
| Hub row in the rendered curriculum: "SC1 · Stochastic Processes · M · 100 h · ← M6" | `CURRICULUM.md:693` |
| Course-map placements (Core "Stochastic Calculus for Finance"; first-year sequence "Continuous-Time Finance") | `curriculum/meta.yaml:102`, `curriculum/meta.yaml:129`; `CURRICULUM.md:71`, `:98` |
| Downstream: SC2 requires SC1 | `curriculum/03-markets.yaml:537` |
| Nearest built prerequisite: M6 (built; `course/modules/M/M6/`; ledger verdict PASS, 210 rows, 0 FAIL, 0 UNVERIFIABLE) | `ledgers/M6.verification.json` (verdict field); `course/modules/M/M6/` |
| Prerequisite closure of SC1 (computed): **{M1, M2, M4, M5, M6, P0.1}**, 83 usable concepts (M1 14, M2 13, M4 19, M5 11, M6 15, P0.1 11) | `tools/coursekit.py` `prerequisite_closure("SC1")` and `concept_owner()`, run by the planner |
| Owners of the 8 SC1 concepts: all SC1 (planner check) | `tools/coursekit.py` `concept_owner()` |
| Closure concepts that SC1 content needs (in closure): `stopping-time`, `filtration`, `martingale`, `optional-stopping-theorem`, `sigma-algebra`, `probability-space`, `random-variable`, `expectation`, `normal-distribution`, `moment-generating-function`, `multivariate-normal`, `uniform-convergence`, `dominated-convergence-theorem`, `lebesgue-integral` | `tools/coursekit.py` `concept_owner()` (owners M4, M5, M6, all in the closure) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 100 h (`curriculum/03-markets.yaml:508`). The tool rules (read in `tools/check_pages.py`):

- lesson `data-hours` between 6 and 12 (`tools/check_pages.py:221-228`);
- hub `data-hours-lessons + data-hours-project = 100` (`tools/check_pages.py:337-338`);
- project share 10 to 40 % of module hours, i.e. 10 to 40 h (`tools/check_pages.py:339-340`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py:341-342`).

Chosen split: **8 lessons × 9 h = 72 h; project 28 h (28 %)**. 72 + 28 = 100. Feasible. No STOP condition on hours.

### 0.3 Blocking issues and gates

**B1. Two prerequisite ledgers in the SC1 closure are not PASS (merge gate, not a build gate).**
- `ledgers/M2.verification.json`: verdict FAIL, one FAIL row `COVERAGE-full-prose-reread` (`course/modules/M/M2/L19.html .. L24.html`).
- `ledgers/M4.verification.json`: verdict FAIL, one UNVERIFIABLE row `M4a-R26` (`course/modules/M/M4/grader/test_project.py`,
  `project.html`, `cards.json`).
- M1 (PASS), M5 (PASS) and M6 (PASS) are clean.
- BLUEPRINT §4 (mastery learning): a module unlocks only after its prerequisites' projects pass (`BLUEPRINT.md` §4 table).
- **Recommendation (Q2):** builders A to F start now; the SC1 branch is not merged until `ledgers/M2.verification.json` and
  `ledgers/M4.verification.json` are PASS, or the architect records the open rows as agreed gaps.

**B2. The curriculum's second source has no admissible registry record (blocks the Karatzas & Shreve citation only).**
- Curriculum string: `curriculum/03-markets.yaml:524` and `curriculum/curriculum.json:9214` ("Karatzas & Shreve, Brownian Motion
  and Stochastic Calculus, 2nd ed. (1991)").
- `references/review_queue.json` (entry at line 1050-1060): reason "no candidate established identity"; candidate DOI
  10.1007/978-1-4684-0302-2 is a 1988 record in the Graduate Texts series, which does not match the 1991 second-edition string.
- `plans/reference-queue-research-2026-10-27.md:58`: verdict `not_admissible` (ISBN route). Open Library's 2nd-edition record
  lists 1991, but the ISBN lookups returned records dated 2004 and 1996. The research says "Not forced."
- `references/authorities.yaml` lists no Springer domain, so the URL route for this publisher is not open.
- **Consequence:** SC1 cites `shreve2004stochastic` only (verified, `references/references.json:20732`, `used_by` SC1 at :20760).
  The Karatzas & Shreve string is recorded as an honest gap (§7.2). No builder types its bibliographic data.
- **Decision needed (Q1):** keep the second source string as an unregistered gap, or edit `curriculum/03-markets.yaml:522-524`
  (a curriculum change; builders do not edit `curriculum/*.yaml`).

**Not blocking (checked):**
- **Real data.** None is needed (§6). The lab and the project use generated paths and exact finite walks. No DATA_REQUESTS.
- **Atlas.** No SC1 Atlas milestone (§8). No contract needed.
- **Concept gaps.** Every concept the natural content uses is either in the closure or is listed in §4 and kept out of the text.
  No missing prerequisite was found (§4, DAG question D0).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

8 lessons × 9 h = 72 h; project 28 h; total 100 h. Concept counts per row sum to 1+1+1+1+1+1+1+1 = 8, each concept in
exactly one row (`curriculum/03-markets.yaml:514-521`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `03-markets.yaml:514-521`) | Lab (twin id, `tests/labs/SC1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Brownian motion as a Gaussian process | `brownian-motion` | `lab-SC1-L01-1`: exact `Fraction` check that the variances of the increments over a dyadic partition of \([0,t]\) add to \(t\), and that \(\Cov(B_s,B_t)=\min(s,t)\) on a rational grid (finite exact check, grade C with basis named, plus the T derivation on the page) | 9 | A |
| L02 | Constructing Brownian motion | `brownian-motion-construction` | `lab-SC1-L02-1`: partial sums of a Schauder-type (Lévy–Ciesielski) series on \([0,1]\) with seeded Gaussian coefficients; the level-by-level sup-norm of the added term printed against the bound used in the proof. **SIMULATED** | 9 | A |
| L03 | Quadratic variation | `quadratic-variation` | `lab-SC1-L03-1` (**the curriculum lab**, `03-markets.yaml:525`): sum of squared increments over partitions of \([0,t]\) with \(2^k\) steps, seeded; the mean and the standard error printed against \(t\); the same sums for \(t^2\) printed (they vanish). **SIMULATED** | 9 | B |
| L04 | Continuous-time martingales | `continuous-time-martingale` | `lab-SC1-L04-1`: the expectation of the exponential martingale \(\exp(\theta B_t-\theta^2 t/2)\) by quadrature against \(1\) for three values of \(\theta\) (numerical, tolerance stated; not SIMULATED) | 9 | B |
| L05 | The Markov property | `markov-property` | `lab-SC1-L05-1`: Chapman–Kolmogorov for the Gaussian transition density, by quadrature on a grid, tolerance stated (numerical; not SIMULATED) | 9 | C |
| L06 | The reflection principle | `reflection-principle` | `lab-SC1-L06-1`: the discrete reflection identity for the symmetric simple random walk, counted exactly by enumeration for \(n\le 12\) (finite exact check; grade C, basis named) | 9 | C |
| L07 | The distribution of the running maximum | `running-maximum-distribution` | `lab-SC1-L07-1`: the exact walk-count identity of L06 used for the maximum tail; seeded Brownian paths on \([0,1]\) compared with the closed form, with the Monte Carlo standard error \se printed. **SIMULATED** | 9 | D |
| L08 | First-passage times | `first-passage-time` | `lab-SC1-L08-1`: first-passage counts of the simple random walk by enumeration for \(n\le 12\), compared with the L06 identity (exact); the truncated mean \(\E[\min(\tau_a,n)]\) printed for growing \(n\) as an illustration, not a proof (**SIMULATED** for the path sample) | 9 | D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 72/28 | none | none | - | A |
| project | Reflection principle verified (`both`) | none | `lab-SC1-project-1` (rung 1), `lab-SC1-project-2` (rung 2, `class="lab completion"`), `lab-SC1-project-3` (rung 3 reference numbers) | 28 | E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`, `bm_checks.py` (the engine, the reference solution) | none | none | - | E |
| cards | `cards.json` from L01–L08 | none | none | - | F (starts after A–D finish, §13) |

**Ownership rule.** Each builder writes only its lesson files and their twins. Builder A also writes `index.html` after L01 and
L02 exist. Builder E writes the project, the grader, the project labs, the rubric and the exemplars, and does not depend on
the lessons' prose; it uses only the definitions and notation fixed in §2.3 and the lesson titles in §1. The cards builder F
writes only `cards.json`.

**Ordering check** (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses M4 `random-variable`, `normal-distribution`, `multivariate-normal` and M6 `sigma-algebra` (in closure).
- L02 uses L01 (`brownian-motion`) and M5 `uniform-convergence` (the Weierstrass M-test step of the series).
- L03 uses L01 and L02 (the increments are Gaussian and independent) and M4 `expectation`, `variance`.
- L04 uses L01 and L03 (\(B_t^2-t\) is a martingale only after the quadratic-variation identity) and M6 `martingale`, `filtration`.
- L05 uses L01 and M4 `expectation`; the strong Markov statement uses M6 `stopping-time`.
- L06 uses L05 (strong Markov property, stated as Assumption A3 there) and M6 `stopping-time`, `martingale` only in prose.
- L07 uses L06 (reflection) and M4 `normal-distribution`.
- L08 uses L06 and L07 (the first-passage law equals the running-maximum law at a fixed level).

Hours check: 8 × 9 = 72 (hub `data-hours-lessons="72"`); project 28 (hub `data-hours-project="28"`); total 100.

**Carried-over ownership deviation (flagged, Q4).** The task asks for "about three lessons per builder". Eight concept-bearing
lessons across four lesson builders gives two per builder. Three lesson builders at three, three and two lessons, with E on
the project, is the alternative. Both keep at most five agents running at once (§13).

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to SC1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3–§8, `plans/M6-build-plan.md` (nearest built prerequisite;
its grader and hub layout are the model for SC1), `plans/E5-build-plan.md` (structure template), `plans/FINAL-ARCHITECT-RULINGS.md`,
`/Users/billyribeiro/.fanout/fixer-rules.md`, and this file. Study `course/modules/M/M6/` for the hub, project, grader panel and
cards layout. `course/templates/` holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`, exact integer
   counts) or from `math` with a stated tolerance, and rounded only at display. A page that shows a rounded figure states its
   rounding rule. Precedent: E5 §2.1.1, AC4 KNOWN 3. Every probability, every \se and every bias figure follows this rule.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS. Every "checked" claim names the lab, line or test.
3. **Attribute nothing unread.** Only the registry key `shreve2004stochastic` (§7.1) may be cited, at book level, with no locator.
   No theorem number, page, equation number or edition string is typed. Standard results without a proof on the page are
   stated as numbered Assumptions (the fixer rule on ASSUMED FACTS), not as T and not as cited. Precedent: M6 §2.1 item 3.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "almost surely", "converges", "nowhere
   differentiable", "the" in front of a path property are used only where a proof, a finite exact enumeration, or a lab computes
   the claim. A simulation of paths illustrates a theorem; it never verifies an almost-sure or pathwise statement, and the page
   says so (Q11). Finite enumerations are grade C with the basis named.
5. **Define before use.** Each of the 8 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson and never before it. Terms outside the 8 and outside the closure (for example *almost surely*, *Gaussian process*,
   *Schauder function*, *Lévy–Ciesielski series*, *discrete-monitored maximum*, *transition density*, *strong Markov property*,
   *simple random walk*, *Monte Carlo standard error*) appear in plain words at first use, with a plain `<dfn>` if they are
   defined there and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
6. **Assumptions are numbered and explicit.** Every Theorem, Proposition, Lemma and Derivation block lists its numbered
   Assumptions (A1, A2, ...) before the statement, and each result that uses a fact the page does not prove says
   "Assuming ..." in its statement (fixer rule on ASSUMED FACTS). Required examples:
   - the Brownian construction on \([0,1]\) assumes an i.i.d. standard Gaussian sequence (A1) and a summable sup-norm bound (A2);
   - the reflection principle assumes the strong Markov property at \(\tau_a\) (A3). **A3 is stated in L05 as a numbered
     Assumption with a proof sketch that names the step it skips**, and every later result that uses it says "Assuming A3";
   - the quadratic-variation limit assumes the partition sequence has mesh tending to zero (numbered within L03).
7. **Grader rule.** The grader demands an exception type only for conditions §5.5 names (fixer rule). Any other invalid input
   may raise any exception or return a value.
8. **No money.** SC1 has no money output. Probabilities are exact `Fraction` or `float` with a stated tolerance; counts are `int`.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container;
   escape `$` as `\$` inside math (fixer rule). `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py` lines 51-60; model
    `tests/labs/M6/lab-M6-L01-1.py`).
11. **Lab mutants are not graded (architect ruling).** Lab twins are demonstrations. Lab code is not mutation-tested. A sentence
    that claims a lab asserts a property must match its code and output (fixer rule and FINAL-ARCHITECT-RULINGS 9).
12. **Basis-explicit quantities.** Every probability and every bias figure states its basis: the discrete grid or the
    continuum, the number of paths, the seed, the standard error \se, and the rounding rule.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. A derivation is T only if
  every step is shown (BUILDER_RULES §3.5).
- Concepts: §3 table. `<dfn>` only for the 8 concepts of §3 plus plain `<dfn>` for other defined terms. Links to closure concepts use
  `href="../../../concepts.html#<id>"` (from `course/modules/SC/SC1/` this is `course/concepts.html`); links to earlier SC1 lessons
  use `href="Lnn.html#def-<id>"`. A lesson never links a concept defined later. A concept outside the closure is never linked (§4).
- Labs: code lives once in `tests/labs/SC1/lab-SC1-Lnn-1.py` and `lab-SC1-project-1..3.py`. The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Lab ids match `lab-SC1-<page>-<n>` (`tools/check_pages.py` `check_lesson`).
  Standard library only (`fractions`, `math`, `itertools`, `random.Random(seed)`); no NumPy; no network; no warnings (`-W error`);
  under 10 s in Pyodide (builders time each twin under CPython and report it; a Pyodide timing claim is not made without `page_smoke`).
- Labs use **no data files**. `data-files` is absent. No MANIFEST entry.
- SIMULATED label: on every lab section or figure that uses generated paths (L02, L03, L07 path sample, L08 path illustration,
  the project's worked example, the grader instance). Exact enumerations (L01 finite check, L06, L08 enumeration) and quadrature checks
  (L04, L05) are not labelled SIMULATED.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `notation/notation.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in
  code comments (precedent M1 "Convention (project Q5)"; AC4 KNOWN 9).
- Banned strings (`tools/check_pages.py:58-72`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis outside code.
- Lesson structure (BUILDER_RULES §4.2; `tools/check_pages.py:75` LESSON_SECTIONS): why-it-matters (at most 120 words), core content,
  inline lab, canon-breaks, misconceptions (at least 3), problems (at least 3 in each of mechanics, proof, empirical, research, each
  with `<details class="solution">`), key-results table, quiz (8–15 items, each with an explanation). **No debate brief** (no
  `debate` key, §0.1).
- Tier M: rungs 1–2 are kept to the minimum (BLUEPRINT §4; BUILDER_RULES §5.1).
- Output contract: the BUILDER_RULES §10 block, with the hours line filled from §1 and the REFERENCE_REQUESTS, NOTATION_REQUESTS,
  GLOSSARY_REQUESTS, DAG_DEFECTS and KNOWN_LIMITATIONS lines. Report PASS only for checks actually run.
- No `git commit`, no push, no branch changes. Builders write only under `course/modules/SC/SC1/` and `tests/labs/SC1/`
  (and `ledgers/` only for the verifier and the grader fixtures named in §5.5).

### 2.3 Notation (binding; `notation/notation.json`)

Registered macros this unit uses (`notation/notation.json`): `\E` (line 5, expectation), `\Prob` (line 9, probability measure),
`\R` (line 25), `\indic` (line 33, indicator), `\Normal` (line 37, \(\Normal(\mu,\sigma^2)\)), `\dto` (line 45), `\se` (line 101,
standard error), `\Var` and `\Cov`.

Registered symbols that SC1 must **not** give another meaning (`notation/notation.json` `symbols` array):
- **`T`** (symbols array, line 112) means the number of return observations in S1. **SC1 never uses `T` for a horizon.** Use **`H`**
  for the horizon. This is a conflict with standard texts, and the page says so once.
- **`\Phi`, `\Phi^{-1}`** (line 117) are the standard normal CDF and its inverse. SC1 may use `\Phi` only with that meaning.
- **`\mathbb{Q}`** (line 147) means a risk-neutral measure (AP1). Not used by SC1 (change of measure is SC3).
- **`R^\ast`, `R^{e\ast}`, `R_f`, `\gamma_3`, `\gamma_4`**: not used.

Local symbols (defined on the lesson where first used, never redefined): \(B_t\) Brownian motion; \(M_t=\max_{s\le t}B_s\) running
maximum; \(\tau_a=\inf\{t\ge 0: B_t=a\}\) first-passage time; \(\mathcal F_t\) filtration (M6 meaning); \(S_n\) simple random walk;
\(\theta\) exponential-martingale parameter; \(\sigma\) only where a scale is needed; \(\varphi\) only for the Gaussian density.
Use \(N\) (not \(T\)) for a number of steps and \(n\) for a grid index.

NOTATION_REQUESTS (for the architect; builders do not add macros): an almost-sure convergence arrow, an \(L^2\) convergence
arrow. No macro for Brownian motion is requested (SC1 writes \(B_t\)). Until the arrows are registered, builders write
"almost surely" and "in \(L^2\)" in words.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson:

- **L01 `brownian-motion`:** the definition of a standard Brownian motion by its finite-dimensional Gaussian laws, with
  \(B_0=0\), independent increments and \(B_t-B_s\sim\Normal(0,t-s)\) (definition, not a theorem). The covariance \(\Cov(B_s,B_t)=\min(s,t)\)
  (T, derived from the increments with every step shown). A Gaussian-process remark (plain prose). Non-differentiability is
  **not** proved here: it is a statement in "Where the canon breaks" with grade C and basis "stated, not proved on this page", or
  removed.
- **L02 `brownian-motion-construction`:** the Lévy–Ciesielski construction on \([0,1]\) from i.i.d. Gaussian coefficients and the
  Schauder functions. The proof of uniform convergence uses M5 `uniform-convergence` (the Weierstrass M-test step). Path
  continuity of the limit is proved (T). The identification of the finite-dimensional laws of the limit with those of L01 is
  proved for the dyadic times and stated for the general case with a sketch that names the skipped step (Assumption A2 for the
  step; the sketch is labelled as one). Extending from \([0,1]\) to \([0,\infty)\) is stated in one remark with the same sketch
  label. **Recommendation (Q5).**
- **L03 `quadratic-variation`:** the quadratic variation over a partition, and its limit in \(L^2\) along partitions with mesh
  tending to zero (T, derived with the variance of squared Gaussians shown). The variation of \(t\mapsto t^2\) over the same
  partitions tends to zero (T, derived). Remark: the limit is not stated as an almost-sure limit on the page (Q11). Uses the
  curriculum lab (`lab-SC1-L03-1`).
- **L04 `continuous-time-martingale`:** the continuous-time filtration \(\mathcal F_t\) of L01, the definition of a continuous-time
  martingale (M6 `martingale` extended to a continuous index, with the definition restated), \(B_t\) and \(B_t^2-t\) are martingales
  (T, derived from L01 and L03), and the exponential martingale \(\exp(\theta B_t-\theta^2 t/2)\) (T, derived). The optional-stopping
  theorem of M6 is used only with a bounded stopping time and the assumption named.
- **L05 `markov-property`:** the Markov property of \(B\) with respect to its filtration, the Gaussian transition density, the
  Chapman–Kolmogorov identity (T, derived by Gaussian convolution). The **strong Markov property at a stopping time** is
  stated as **Assumption A3** with a proof sketch that names the step it skips (the approximation of \(\tau\) by discrete stopping
  times). Every later use says "Assuming A3". (Fixer rule: a fact the page assumes without proof is a numbered Assumption.)
- **L06 `reflection-principle`:** the reflection principle for \(B\) at the first passage time \(\tau_a\), with \(a>0\): the reflected
  path after \(\tau_a\) is a Brownian motion (Assuming A3). Consequence: \(\Prob(M_t\ge a)=2\,\Prob(B_t\ge a)\) (derived from A3 and
  symmetry, with every step shown). The discrete reflection identity for the symmetric simple random walk is proved by a bijection
  and checked in the lab for \(n\le 12\) (grade C, basis named: finite enumeration).
- **L07 `running-maximum-distribution`:** the law of \(M_t\) from L06 (T, conditional on A3): the tail \(\Prob(M_t\ge a)\) for \(a>0\)
  in closed form, with the closed form written through the standard normal CDF \(\Phi\) (its registered meaning). The continuous closed
  form is the exact reference for the project. The discrete-monitored maximum on a grid is defined here, with its inequality
  \(\max_{k\le n} B_{t_k}\le M_t\) (pathwise, T), because the project's discretization-bias handling uses it.
- **L08 `first-passage-time`:** the identity \(\Prob(\tau_a\le t)=\Prob(M_t\ge a)\) (T, from L06 and L07), finiteness of \(\tau_a\) with
  probability one stated as a consequence of the tail with the limit \(t\to\infty\) shown (T). The expectation \(\E\tau_a\) is
  **not** claimed on the page (it is infinite; any claim is a numbered Assumption or removed). The lab's truncated mean is an
  illustration, labelled as such.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" names at least one hypothesis whose failure breaks the result: non-Gaussian increments,
  a non-continuous path, a stopping time that is not bounded, a discrete grid for a continuous statement, and A3 without the
  stopping-time approximation.
- No lesson uses a term from SC2 (Itô integral, Itô's lemma, geometric Brownian motion, Ornstein–Uhlenbeck, SDE schemes) or SC3
  (change of measure). Those are outside SC1 and not in its closure (§4).

---

## 4. DAG problems (concepts natural SC1 content would use outside the closure)

Prerequisite closure of SC1 (computed): **{M1, M2, M4, M5, M6, P0.1}**, 83 usable concepts. Owners below are from `concept_owner()`
(planner run).

| Ref | Concept | Owner (outside closure) | Where natural SC1 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D0 | Missing prerequisites | none | The closure holds every concept the 8 lessons use (§1 ordering check: M4 `normal-distribution`, `multivariate-normal`, `expectation`, `variance`; M5 `uniform-convergence`; M6 `sigma-algebra`, `filtration`, `martingale`, `stopping-time`, `optional-stopping-theorem`) | **No DAG_DEFECT.** Planner check: none needed. |
| D1 | `ito-integral`, `itos-lemma`, `ito-isometry` | SC2 | the quadratic variation is motivated by Itô's lemma (L03 remark) | Not used. SC1 never names an Itô object. |
| D2 | `geometric-brownian-motion`, `ornstein-uhlenbeck-process`, `sde-existence-uniqueness` | SC2 | examples of Brownian functionals (L04 exercises) | Not used. Examples are \(B_t\) and \(B_t^2-t\) only. |
| D3 | `euler-maruyama-scheme`, `milstein-scheme`, `strong-vs-weak-convergence` | SC2 | the discretization-bias discussion in the project (the grid max is a discrete scheme) | Plain prose, no link, no `<dfn>`: "the grid maximum of a sampled path". The project does not name an SDE scheme. |
| D4 | `girsanov-theorem`, `forward-measure`, `martingale-representation-theorem` | SC3 | reflection under a change of measure (not used) | Not used. |
| D5 | `feynman-kac-formula`, `kolmogorov-backward-equation`, `kolmogorov-forward-equation` | SC4 | the transition density as a PDE solution (L05 remark) | Not used. The density is stated and checked, not solved as a PDE. |
| D6 | `poisson-process`, `levy-process`, `compound-poisson-process` | SC5 | jump analogues (not used) | Not used. |
| D7 | `black-scholes-formula`, `barrier-option` | FC2, DV6 | the barrier-hitting interpretation of the reflection principle (L08 remark) | Not used. The reflection tail is stated as a probability, with no option pricing. |
| D8 | `monte-carlo-integration`, `pseudo-random-number-generator` | M8 | every seeded simulation in the labs and the grader | Plain prose "seeded simulation with `random.Random(seed)`"; no link. |
| D9 | `estimator-bias-variance` (S1), `bias-variance-tradeoff` (QR3) | S1, QR3 | the word "bias" in "discretization bias" | Plain prose: "discretization bias" is defined in the project with a plain `<dfn>`; no link, no concept. |
| D10 | Law of the iterated logarithm, invariance principle (Donsker), discrete monitoring correction | NOT IN CURRICULUM | the Brownian-bridge continuity correction is the usual cure for discrete barriers (project stretch only) | NOT IN CURRICULUM as concepts. Mentioned in the project stretch only as "a continuity correction, cited only after its record is admitted" (§7.2). |

Terms used in prose that are in no curriculum concept (NOT IN CURRICULUM): *Gaussian process*, *Schauder function*,
*Lévy–Ciesielski series*, *simple random walk*, *discrete-monitored maximum*, *transition density*, *almost surely*, *strong Markov
property*. Each is defined in plain words at first use, with a plain `<dfn>` only where a definition is given, and no `data-concept`
(BUILDER_RULES §1.10; Q2).

Possible confusion of names: M6's `martingale` and `stopping-time` are discrete-time. SC1's `continuous-time-martingale` extends
them; L04 links the M6 concepts and states the extension. It never redefines them.

`check_dag.py` checks linked uses only. An unlinked use of D1–D9 passes the tool, so the verifier reads every lesson for those
names (VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): `both` grading, ladder, spec, budget, rubric, grader

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` requires the order)

1. **Rung 1, worked example** (`lab-SC1-project-1`, SIMULATED): one fully solved, annotated check of the reflection tail
   \(\Prob(M_t\ge a)=2\,\Prob(B_t\ge a)\) for one instance generated by `make_instance(0)`. Each step has a "why" annotation.
   Tier M keeps this short (§5.3, 2 h).
2. **Rung 2, completion** (`lab-SC1-project-2`, `class="lab completion"`): the exact walk count of the discrete reflection identity
   for the simple random walk, with the cap line and the final comparison line replaced by `___`. Its twin is the completed
   solution; every page line equals the twin line or contains a blank (`tools/run_labs.py` docstring). Graded instantly.
3. **Rung 3, independent project** (graded by autograder and rubric, `both`): the three proofs of §5.4 (reflection principle, running
   maximum, first-passage identity), and the engine `bm_checks.py` (§5.5). `lab-SC1-project-3` is the rung-3 reference check: it
   prints the reference numbers for seed 0 that the engine's report must reproduce.
4. **Rung 4, stretch** (optional, not graded): the same checks for a second level \(a\) and the discretization bias of a
   Brownian-bridge continuity correction, **only after its registry record is admitted** (§7.2). Without the record, the stretch
   is limited to a finer grid and an additional nested-grid table.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py:34` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A quant research engineer must show that a Brownian path's running maximum and first-passage law follow the
  reflection principle, and that a simulation of the path on a grid reports the discretization bias honestly. The deliverable is a
  proof set and a verification engine that checks it on generated instances.
- **Inputs.** Generated instances from `make_instance(seed)` (§5.5). No dataset. Every instance is **SIMULATED**. No Atlas data.
- **Required outputs.** (a) `proofs.html`: the three proofs, typeset, with every Assumption numbered (student's own). (b)
  `bm_checks.py` with the five functions of §5.5. (c) The printed verification report for seed 0, with the rounding rule
  stated and the grid and path count given.
- **Constraints.** Standard library only (`math`, `fractions`, `itertools`, `random`). Every probability in the report is a
  `float` with the tolerance stated, or an exact integer count. Every printed number is recomputed from unrounded values and
  rounded once, at display, by the rule the spec states. The proofs state every Assumption. A simulation is not claimed to
  verify an almost-sure or pathwise statement (Q11).
- **Grading.** Both. The autograder checks the engine (§5.5); the rubric grades the proofs and the report (§5.4). The spec's
  grading entry must name **both** "autograder" and "rubric" (`tools/check_projects.py` `GRADING_WORDS`, line 38).
- **Reading list.** `ol.reading-list` cites `shreve2004stochastic` only (§7.1).

### 5.3 Time budget (`<table id="hours">`, sums to 28 h; every row needs a one-line rationale; `tools/check_projects.py`)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED instance, annotated line by line |
| Rung 2, completion problem | 3 | Fill the cap line and the comparison line, then run the instant check |
| Proofs: reflection principle, running maximum, first-passage identity | 10 | Three typeset proofs with every Assumption numbered; the reflection proof uses A3 |
| Engine `bm_checks.py` with the test suite and exact enumeration | 8 | Five functions, exact counts, tolerance checks, edge cases |
| Verification report for seed 0 (grid refinement and standard errors) | 3 | Printed values, rounding rule, the grid and path count, what the simulation does and does not show |
| Self-assessment against the exemplars | 2 | Score the rubric, then compare with the annotated scoring |
| **Total** | **28** | Equals `data-hours-project` on the hub (§1) |

Check: 2 + 3 + 10 + 8 + 3 + 2 = 28.

### 5.4 Rubric (`table.rubric#rubric`; `tools/check_projects.py` `rubric_problems`, lines 58–73)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to 1.
Every level descriptor is observable.

1. **Hypotheses.** Level 4: every theorem and derivation lists its numbered Assumptions, including A3 (strong Markov) with a
   pointer to where it is used. Level 1: "states the assumptions".
2. **Proof steps.** Level 4: every step of the reflection proof is justified by a named assumption, lemma or definition; a
   skipped step is named as a gap. Level 1: "the proof is convincing".
3. **Numbers.** Level 4: every printed value is recomputed from unrounded values, with its rounding rule and its standard error
   \se where a simulation supplies it. Level 1: "rounds the numbers".
4. **Scope.** Level 4: states what the simulation shows (a finite sample on a grid) and what it does not (an almost-sure or
   pathwise statement). Level 1: "notes some caveats".
5. **Discretization.** Level 4: reports the grid maximum against the continuous closed form for every grid in the table, states
   the direction of the bias from the nested-grid inequality (the coarse maximum is never larger), and gives the standard error at
   each grid. Level 1: "discusses the grid".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written proofs and reports on the seed-0
instance, annotated with the descriptors each passage meets or misses. Every number in the exemplars is produced by
`bm_checks.py` on seed 0; a builder never types one (E5 §5.4 precedent).
Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in M1 and M6).
The page shows where the student's scores diverge from the exemplar scores. Calibration: the verifier scores both exemplars blind,
within one level per criterion (VERIFIER §2.6).

The project is not adversarial: no question bank (architect default; Q6).

### 5.5 Autograder: `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`, and the engine `bm_checks.py`

Grader panel: `section.grader-panel#grader data-unit="SC1" data-grader="grader/" data-suite="test_project.py"
data-support="instance.py" data-solution="bm_checks.py" data-starter="starter.py" data-packages=""`
(`tools/check_projects.py` grader panel checks). No `data-packages`: standard library only.

**Instance.** `make_instance(seed: int) -> dict` is deterministic and returns a dict with keys `H` (horizon, a positive float in
time units), `a` (level, a positive float), `n_steps` (int in 4 to 256), `n_paths` (int in 400 to 800), `seed`, and `label`
set to `"SIMULATED"`. Only valid instances are generated: `H > 0`, `a > 0`, `n_steps >= 1`, `n_paths >= 2`. Seeds 0–49 must give
materially different levels and horizons, not only different labels (the answers change). Total generated draws per seed are
at most \(2\times10^5\), so each test finishes under 5 s in Pyodide and the suite under 60 s.

**Reference.** `reference.py` is the full solution. It passes every test on seeds 0–49
(`tools/run_graders.py --unit SC1 --seeds 0-49`). `starter.py` raises `NotImplementedError` in every function and the suite
must fail on it (`tools/run_graders.py` checks this).

**Engine functions (frozen signatures; Q10).** In `bm_checks.py`:
- `reflection_tail(a: float, t: float) -> float`: \(\Prob(M_t\ge a)\) by the reflection closed form. Named conditions: `a <= 0` and
  `t <= 0` raise `ValueError`.
- `discrete_max_exceedance(instance: dict, n_steps: int) -> tuple[float, float]`: estimate and standard error \se of
  \(\Prob(\max_{k\le n} B_{t_k}\ge a)\) on the instance's `n_paths` seeded paths with grid size `n_steps`. Named conditions:
  `n_steps < 1` and `n_paths < 2` raise `ValueError`.
- `nested_grid_counts(instance: dict, n_fine: int, n_coarse: int) -> tuple[int, int]`: exceedance counts on the same paths for the
  fine grid and for the coarse grid, where the coarse grid is a subset of the fine grid. Named condition: `n_coarse` must divide
  `n_fine` (otherwise `ValueError`).
- `srw_max_count(n: int, a: int) -> int`: the number of simple random walk paths of length `n` whose maximum reaches `a`
  (exact integer, by enumeration or by the identity, the builder's choice). Named conditions: `n < 1` and `a < 1` raise `ValueError`.
- `srw_terminal_count(n: int, a: int) -> int`: the number of length-`n` paths with final value at least `a`. Named conditions as
  for `srw_max_count`.

Exception table (only these; fixer rule): `ValueError` for the conditions named above. Any other invalid input may raise any
exception or return a value; the tests do not assert a type. Failure messages name the violated property and hint at the concept;
they never print the expected value (`__tracebackhide__` in every test helper that compares a value).

**Tests (`test_project.py`).** Property and number checks, each against the instance's own parameters, never a hard-coded answer:
- `reflection_tail`: equals \(\operatorname{erfc}(a/\sqrt{2t})\) to within 1e-12 (the closed form the test computes independently with
  `math.erfc`), and equals \(2\,\Prob(B_t\ge a)\) by an independent Simpson quadrature of the Gaussian density to within 1e-8.
  Strictly decreasing in `a` (both directions checked on the instance) and strictly increasing in `t`.
- Named `ValueError` for `a = 0` and `t = 0` (both sides of each boundary: `a = 1e-9` and `t = 1e-9` do not raise).
- `srw_max_count` and `srw_terminal_count`: the identity \(\texttt{srw\_max\_count}(n,a)=\texttt{srw\_terminal\_count}(n,a)+\texttt{srw\_terminal\_count}(n,a+1)\)
  holds exactly for every \(n\le 12\) and \(1\le a\le n\) of the instance; an independent brute-force enumeration over \(2^n\) paths
  agrees exactly. Named `ValueError` for `n = 0` and `a = 0` (both sides: `n = 1` and `a = 1` do not raise).
- `discrete_max_exceedance`: the estimate lies within \(5\,\se\) of `reflection_tail(a, H)` on the instance (seeded). The returned
  standard error equals the sample standard deviation of the indicators divided by \(\sqrt{N}\) with divisor \(N-1\), to 1e-12.
  Named `ValueError` for `n_steps = 0` and `n_paths = 1` (both sides).
- `nested_grid_counts`: the coarse count is never larger than the fine count (pathwise inequality, exact, no noise). Named
  `ValueError` when `n_coarse` does not divide `n_fine`.
- Edge cases: `n_steps = 1`; `n_paths = 2`; a level so small that the tail is near one; the instance horizon equal to one grid step.
- Instances: `make_instance(seed)` is deterministic (same seed, same dict); all 50 seeds give valid instances; the levels differ
  across seeds 0–49 (at least 45 distinct values, so the answers change, not only the labels).

**Mutants.** Ten student-error mutants (§5.6), written as single-change copies of the reference under `ledgers/SC1/mutants/`.
Each must be killed by `test_project.py` on seeds 0–9 (`tools/mutate_graders.py --unit SC1 --seeds 0-9`).

**Alternative correct implementations.** Five, of different styles, pass seeds 0–49 (§5.7). They live under
`ledgers/SC1/scripts/alternatives/` and are verifier-written.

**Statistical tolerance.** The Monte Carlo test bound is \(5\,\se\) (not 3 or 4), so that 50 seeds times the MC tests give a
negligible false-failure rate. Recommended in Q9.

### 5.6 Ten student-error mutants (written by the verifier; each must fail at least one test on seeds 0–9)

Each is a complete module in `ledgers/SC1/mutants/<name>.py`, with the first docstring line naming the student error.

1. Reflection factor dropped: `reflection_tail` returns \(\Prob(B_t\ge a)\), with no factor 2.
2. Scale confusion: `reflection_tail` uses \(\sqrt{t}\) in the erfc argument instead of \(\sqrt{2t}\).
3. Horizon off by one: `discrete_max_exceedance` takes the maximum over \(k\le n-1\) only (the final grid point is dropped).
4. Lookahead: the maximum includes one extra grid point beyond the horizon.
5. Standard error ignored: `discrete_max_exceedance` returns standard error 0.0 with a correct estimate.
6. Divisor error: the standard error uses divisor \(N\) instead of \(N-1\).
7. Nested grid reversed: `nested_grid_counts` returns the fine and coarse counts swapped.
8. Level doubled in first passage: `reflection_tail(a, t)` is computed as `reflection_tail(2*a, t)`.
9. Seed-0 hard-coded answer: `discrete_max_exceedance` returns a fixed constant when `instance["seed"] == 0`.
10. Invalid input accepted: `reflection_tail` accepts `t <= 0` and returns a value instead of raising `ValueError` (a condition the
    spec names).

If a mutant turns out to be equivalent on every input the page states, it moves to `ledgers/SC1/equivalent/` with a README proof
(FINAL-ARCHITECT-RULINGS 9). No survivor stays in `ledgers/SC1/mutants/`.

### 5.7 Five alternative correct implementations (verifier-written; must all pass seeds 0–49)

Written as test-only fixtures under `ledgers/SC1/scripts/alternatives/` (M6 §6.5 precedent):
(1) `reflection_tail` by `statistics.NormalDist` and the identity \(\operatorname{erfc}(x)=2(1-\Phi(\sqrt2\,x))\) (a different route to the same value);
(2) `reflection_tail` by quadrature only (Simpson), no closed form, to the 1e-8 tolerance;
(3) `srw_max_count` and `srw_terminal_count` by dynamic programming over (position, running maximum) with integer counts;
(4) `discrete_max_exceedance` with Box–Muller Gaussians on a different draw order, so the estimate differs from the reference but
    stays within \(5\,\se\);
(5) `discrete_max_exceedance` by a Brownian-bridge-free cumulative-sum construction and `nested_grid_counts` by subsampling indices
    instead of slicing.

### 5.8 Grader fixtures and what the verifier writes

The verifier writes the 10 mutants and the 5 alternatives (§5.6–5.7), runs `tools/mutate_graders.py --unit SC1 --seeds 0-9`,
and runs `tools/run_graders.py --unit SC1 --seeds 0-49` on the reference and on each alternative (the alternatives are run
by a script kept under `ledgers/SC1/scripts/`, VERIFIER §3). Each mutant's killing test is recorded in the ledger's `mutants` list.

---

## 6. Real-data policy

- **No real data.** SC1 is stochastic-process theory. Labs and the grader use generated paths, exact finite walks and closed forms.
- **Not embedded, and not needed.** `tools/data_sources.yaml` (ids `fx_daily`, `fx_monthly`, `ust_daily`, and the `rejected:`
  block at :119) has no series for SC1 and none is requested.
- Generated paths and instances are labelled **SIMULATED** on every page section and in the grader docstring (BLUEPRINT §5.3).
- No `data-files` attribute on any lab. No MANIFEST entry. No DATA_REQUESTS.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in SC1 |
|---|---|---|---|
| `shreve2004stochastic` | Shreve, *Stochastic Calculus for Finance II*; Open Library book; year 2004 (`references/references.json:20732`); `used_by: ["SC1"]` (`:20760`); source string "Shreve, Stochastic Calculus for Finance II (2004)" matches `curriculum/03-markets.yaml:523` | verified | book-level citation for the curriculum's Brownian and stochastic-calculus material; reading list; cite at book level with no locator |

Not used by SC1 by default (registry keys that exist, all of them owned by other modules; use needs architect approval, Q7):
`williams1991probability` (`references/references.json:23047`) and `billingsley2012probability` (`:2661`), both `used_by` M6; `kloeden1992numerical`
(`references/references.json:14713`, `used_by` SC2); `oksendal2003stochastic` (`used_by` SC2); `magdonismail2004maximum` (`used_by` PR5,
the maximum drawdown of a Brownian motion, not SC1 content).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Karatzas and Shreve (lead only; the curriculum string is `curriculum/03-markets.yaml:524`)", year: "1991 (curriculum string; not confirmed)", title: "Brownian Motion and Stochastic Calculus, 2nd ed.", venue: "not typed", needed_for: "the second curriculum source of SC1 (L02 and L05 attribution of the construction and the Markov material), if the architect keeps it", confidence: "the need is certain; the research verdict is `not_admissible` (plans/reference-queue-research-2026-10-27.md:58); the review-queue candidate DOI 10.1007/978-1-4684-0302-2 is a 1988 record and must not be admitted (references/review_queue.json, entry at line 1050)"}
- {doi: null, authors: "Lead only: literature on continuity corrections for discretely monitored barrier crossings (no author typed)", year: "not typed", title: "continuity correction for the discrete-monitoring of a Brownian maximum", venue: "not typed", needed_for: "project stretch (§5.1 rung 4) only; not in the graded core", confidence: "the need is a lead, not a verified source; no record identified by this planner"}
- {doi: null, authors: "Lead only: literature on the first-passage distribution of Brownian motion (no author typed)", year: "not typed", title: "textbook treatment of the reflection principle, if a second source is wanted for L06", venue: "not typed", needed_for: "L06 and L08 second citation; not required by the curriculum", confidence: "optional; the curriculum's sources are shreve2004stochastic and B2 above"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer or publisher page;
`references/authorities.yaml`). Until resolved, the lessons teach the models with derivations and no empirical attribution. Every
sentence that would need an empirical source is removed.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for SC1 (`curriculum/curriculum.json` `atlas` array: 0 entries name SC1; planner check)
and SC1's project has no `atlas:` key (`curriculum/03-markets.yaml:526-532`). `tools/check_projects.py` skips the contract check
when no `atlas` key is present. No `atlas/SC1.contract.md` is needed or drafted.

---

## 9. Cards builder (Builder F, after A–D finish)

- `course/modules/SC/SC1/cards.json`, ids `SC1-c001` upward, `lesson` in L01–L08, one card per definition, theorem statement,
  key identity, key result and misconception (BUILDER_RULES §7). `tools/check_pages.py` `check_cards` checks the id prefix, the
  lesson existence, the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab L06, discrete reflection identity (finite enumeration)"`. A result that depends on A3 says so in its `basis`.
- Cite `shreve2004stochastic` only for an attributed or book-level claim. `cite` is `[]` where the card is a model result.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.
- Ids need not be sequential (FINAL-ARCHITECT-RULINGS 2).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit SC1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit SC1
.venv/bin/python tools/check_projects.py --unit SC1
.venv/bin/python tools/embed_labs.py course/modules/SC/SC1/L01.html            # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/SC/SC1/L03.html --refresh lab-SC1-L03-1   # after editing a twin
.venv/bin/python tools/run_labs.py --unit SC1               # --page L03 for one lesson
.venv/bin/ruff check tests/labs/SC1 course/modules/SC/SC1/grader && .venv/bin/ruff format --check tests/labs/SC1 course/modules/SC/SC1/grader
.venv/bin/mypy --no-incremental <each file touched>         # strict, repository configuration
```

Grader (builder E; the reference must pass before the project is handed off):

```bash
.venv/bin/python tools/run_graders.py --unit SC1 --seeds 0-49
```

Verifier only (not run by builders): `.venv/bin/python tools/mutate_graders.py --unit SC1 --seeds 0-9`;
`.venv/bin/python tools/page_smoke.py --unit SC1` (on a quiet machine, alone, timing-sensitive; fixer rule); and
`.venv/bin/python tools/verify_refs.py --unit SC1` (the unit ledger's run, VERIFIER §2.1).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. No new dataset is added, so `fetch_data.py --check` is not required by SC1.

Flag checks: `tools/check_pages.py` and `tools/check_dag.py` accept `--unit`; `tools/check_projects.py` accepts `--unit`;
`tools/run_labs.py` accepts `--unit` and `--page`; `tools/run_graders.py` accepts `--unit` and `--seeds`; `tools/mutate_graders.py`
accepts `--unit` and `--seeds` (its mutants are read from `ledgers/<UNIT>/mutants/*.py`, `tools/mutate_graders.py` line 41).
The planner did not execute the builder commands; only the coursekit closure, concept-owner and ledger functions were run (§0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on the SC1 project and no Atlas entry names SC1 (§8). `tools/check_projects.py` skips the
   contract check.
2. **No debate.** SC1 has no `debate:` key, so `tools/check_pages.py` does not require a debate brief. The reflection principle and
   the first-passage law are derivations; no contested empirical claim is planned, so the two-sided rule (BUILDER_RULES §2.5) is not triggered.
3. **Both grading.** The autograder and the rubric and two exemplars at two levels are required (`tools/check_projects.py` rubric checks,
   lines 58–73; grader panel checks).
4. **One curriculum lab, eight lab twins.** The curriculum names one lab (`03-markets.yaml:525`); BUILDER_RULES §3.4 requires a
   numerical check per key formula; the plan adds one lab per lesson (M6 Q8 precedent).
5. **Prerequisite gates.** M2 and M4 ledgers are not PASS (§0.3 B1). Prerequisite links go to concept anchors
   (`course/concepts.html`), not to M2 or M4 hub pages, which are not the SC1 gate.
6. **Tier M rung rule.** Rungs 1–2 are minimal from tier M upward (BLUEPRINT §4). Rung 1 is 2 h and rung 2 is 3 h.
7. **Notation.** `T` (registered S1 meaning) is never used for a horizon; `H` is used (§2.3). This is a visible difference from
   textbooks and the page states it once.
8. **Runtime.** The exact walk enumerations stay at \(n\le 12\) (\(2^{12}\) paths) and the grader's draws stay within \(2\times10^5\) per
   seed. Builders time each twin under CPython and report it.
9. **Lab mutants.** Lab twins are not mutation-tested (FINAL-ARCHITECT-RULINGS 9; fixer rule). Project graders are.
10. **Five agents at a time.** The task allows up to five haiku agents. Builders A–E run together; F starts only after A–D finish (§13).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **B2, the Karatzas & Shreve source.** The second curriculum source (`curriculum/03-markets.yaml:524`) has no admissible record
   (§0.3 B2). **RECOMMENDED: keep SC1 citing `shreve2004stochastic` only; record Karatzas & Shreve as an unregistered gap
   (§7.2); do not edit the curriculum string now.** Alternative: edit the string after the architect checks the edition.
2. **B1, prerequisite gate.** M2 (one FAIL row) and M4 (one UNVERIFIABLE row) are in the closure and are not PASS.
   **RECOMMENDED: builders start now; the SC1 branch is merged only after both ledgers are PASS or the rows are agreed as gaps.**
3. **Lesson count and hours.** **RECOMMENDED: 8 lessons × 9 h = 72 h; project 28 h (28 %).** Alternatives inside the rules:
   9 lessons × 8 h = 72 h with a 28 h project; 10 lessons × 7 h = 70 h with a 30 h project. Each keeps the hub split and the 6–12 h rule.
4. **Builder allocation.** The task asks for about three lessons per builder. **RECOMMENDED: four lesson builders with two lessons
   each (A: L01, L02, index; B: L03, L04; C: L05, L06; D: L07, L08) and E for the project, as in §1.** Alternative: three lesson
   builders at 3, 3 and 2 lessons (A: L01–L03 and index; B: L04–L06; C: L07–L08) with E on the project. Either way at most
   five builders run together, and F runs after the lesson builders.
5. **L02 construction scope.** **RECOMMENDED: prove the continuity of the Lévy–Ciesielski limit completely (uniform convergence by the
   M-test, M5 `uniform-convergence`); prove the dyadic finite-dimensional laws; state the general identification of the laws as a
   numbered Assumption (A2) with a labelled sketch that names the skipped step.** No claim is graded T beyond what is proved.
6. **A3, the strong Markov property (L05, used by L06–L08).** **RECOMMENDED: state A3 as a numbered Assumption with a labelled sketch
   that names the approximation step; every later result says "Assuming A3" in its statement.** Alternative: prove A3 fully (longer
   than the 9 h lesson allows).
7. **Sources for the lessons.** Confirm `shreve2004stochastic` as the only cited key (§7.1). **RECOMMENDED: confirm.** Do not cite
   `williams1991probability`, `billingsley2012probability`, `kloeden1992numerical`, `oksendal2003stochastic` or `magdonismail2004maximum`
   from SC1 without architect approval.
8. **Project deliverable.** The curriculum says "Proof plus verification" (`03-markets.yaml:531`). **RECOMMENDED: `proofs.html` (rubric)
   plus `bm_checks.py` (autograder) and the printed seed-0 report; no notebook** (M6 Q5 precedent: a notebook is not a tool-supported deliverable).
9. **Monte Carlo tolerance.** **RECOMMENDED: the MC test bound is 5 standard errors, with seeded paths, so the 50-seed run has a negligible
   false-failure rate.**
10. **Grader interface.** **RECOMMENDED: freeze the five engine signatures of §5.5 before builder E starts** (`reflection_tail`,
    `discrete_max_exceedance`, `nested_grid_counts`, `srw_max_count`, `srw_terminal_count`) and `make_instance(seed: int) -> dict`.
11. **Exact versus simulated checks.** The curriculum asks to verify the statements "against simulation" (`03-markets.yaml:529-530`).
    A simulation cannot verify an almost-sure or pathwise statement. **RECOMMENDED: exact enumeration of the discrete walk identity
    plus seeded path simulations with \se, and the limitation stated on the page.**
12. **Notation.** **RECOMMENDED: use `H` for the horizon (registered `T` is S1's meaning; `symbols` array line 112); `\Phi` only as the
    standard normal CDF; local \(B_t\), \(M_t\), \(\tau_a\), \(S_n\); and NOTATION_REQUESTS for an almost-sure arrow and an \(L^2\) arrow,
    with the words "almost surely" and "in \(L^2\)" until approved.**
13. **Rung length.** Tier M keeps rungs 1–2 minimal. **RECOMMENDED: rung 1 is 2 h and rung 2 is 3 h (§5.3).** Confirm.
14. **Discretization handling in the project.** The curriculum asks for "proper discretization-bias handling" (`03-markets.yaml:529-530`).
    **RECOMMENDED: the graded handling is the nested-grid inequality, grid refinement tables with \se, and an explicit statement of
    the bias direction. No continuity correction is graded** (its source is a REFERENCE_REQUEST, §7.2). Alternative: admit a
    continuity-correction record first and grade it.
15. **Terms.** **RECOMMENDED: confirm that the terms in §4 are plain prose with no `data-concept`, and that no GLOSSARY_REQUESTS entry is needed.**
16. **Figures.** **RECOMMENDED: no live figures and no new JS kernel** (the architect default). The labs print tables.
17. **DAG.** **RECOMMENDED: confirm that SC1 needs no prerequisite change** (§4, D0: the closure covers the content; SC2 concepts are not used).
18. **Hub placement.** **RECOMMENDED: `section.quiz#placement data-mastery="0.8"` with nine items, at least two `data-skill` items testing
    the rung 1–2 skills (the reflection tail of one instance; the walk-count completion line), as in M6 §4.**

---

## 13. After the builders

1. **Scheduling (five agents at most).** Builders A, B, C, D and E start together. Builder F (cards) starts when A–D have finished;
   it may overlap E. The orchestrator integrates after all six have reported.
2. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
3. Independent Haiku verifiers in fresh checkouts, by slice: L01–L02 (includes the construction proof), L03–L04 (includes the curriculum
   lab), L05–L06 (includes A3), L07–L08, project (rubric and exemplar calibration; the engine's ten mutants and five alternatives).
   Failing rows return to the builder that owns the file, with only the failing rows.
4. Ledger at `ledgers/SC1.verification.json`; scripts that back a row under `ledgers/SC1/scripts/` (VERIFIER §3); mutants under
   `ledgers/SC1/mutants/` (never under `ledgers/SC1/equivalent/` unless a proof is written there).
5. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 and B2 must be resolved or
   named as honest gaps first (§0.3).

Architect decisions: pending (§12). Where the architect answers "follow the plan's recommendation", the recommendation in §12 applies.

## Architect decisions

Pending. This plan is the planner's proposal. Each of Q1–Q18 in §12 needs a decision before the named builder starts; Q1 and
Q2 are needed before the merge, and Q5, Q6, Q10 before builders B, C and E write their files.

## Architect decisions (2026-11-03, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank. plans/FINAL-ARCHITECT-RULINGS.md and ~/.fanout/fixer-rules.md bind every builder. No reference is admitted in this batch: a statement whose source is a REFERENCE_REQUEST is not made, or it is taught as a model result with no attribution.
Module specifics: 8 lessons x 9 h + 28 h project; builders A: L01, L02, index; B: L03, L04; C: L05, L06; D: L07, L08; E: project (proofs.html rubric, bm_checks.py autograder); F: cards. Only shreve2004stochastic is cited. A2 and A3 are numbered Assumptions with labelled sketches. H is the horizon symbol. The SC1 merge waits for the M2 and M4 ledgers to be PASS.
