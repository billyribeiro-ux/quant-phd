# CS6 build plan: Parallel & High-Performance Computing (2026-11-09)

Unit: **CS6 · Parallel & High-Performance Computing** · tier M · 90 h · prerequisites CS5 and M8 · no Atlas milestone ·
no debate key · grading `autograder` (curriculum), with a recommended change to `both` (open question Q1) · output directory
`course/modules/CS/CS6/` (part code `CS`) · lab twins `tests/labs/CS6/` · autograder files `course/modules/CS/CS6/grader/`.
Planner: Haiku, plan only. No lesson text, no git operations, no commits. Executors: Haiku builders, then independent Haiku
verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement cites `file:line` read during planning. `J:` means `curriculum/curriculum.json`
(key path given). `R:` means `references/references.json` (line given). `T:` means a tool source line. `P:` means a prior plan.
Anything not established is marked **NOT ESTABLISHED** or **ASSUMPTION** and goes to §12. Planner-derived facts about the graph
were computed with `tools/coursekit.py` (`prerequisite_closure`, `concept_owner`, `built_units`) through `.venv/bin/python`.

**Status: BLOCKING ISSUES EXIST (§0.3, items B1 to B3). The hours are feasible. The language target (B2) and the grading mode
against the deliverables (B1) need an architect decision before the builders start.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part CS, code `CS`, title "Computing & Software Engineering" | `curriculum/01-foundations.yaml:367-369` |
| Studio STUDIO-CS requires CS2 and CS5 only (not CS6) | `curriculum/01-foundations.yaml:370-373` |
| CS6 entry starts | `curriculum/01-foundations.yaml:541` (`- id: CS6`) |
| Title "Parallel & High-Performance Computing" | `curriculum/01-foundations.yaml:542` |
| Tier `M`, hours `90` | `curriculum/01-foundations.yaml:543-544` |
| Prereqs `[CS5, M8]` (only) | `curriculum/01-foundations.yaml:545` |
| Core: Amdahl's law, threads vs. processes, SIMD, GPU programming model, parallel RNG streams, profiling, latency vs. throughput engineering | `curriculum/01-foundations.yaml:546-548` |
| `introduces` has 8 concepts: `amdahls-law`, `threads-vs-processes`, `python-gil`, `simd-vectorization`, `gpu-programming-model`, `parallel-rng-streams`, `profiling`, `latency-vs-throughput` | `curriculum/01-foundations.yaml:549-557` |
| Sources: two free-text strings (Amdahl 1967, AFIPS; Hennessy & Patterson, 6th ed. 2017) | `curriculum/01-foundations.yaml:558-560` |
| Lab: "Parallel Monte Carlo with independent RNG streams: reproducibility check." | `curriculum/01-foundations.yaml:561` |
| Project "Parallel risk run"; brief: parallelize a full-portfolio Monte Carlo VaR with reproducible RNG streams, achieving a measured speedup and reconciling the result to the serial run | `curriculum/01-foundations.yaml:562-566` |
| Project deliverable "Code, scaling plot, reconciliation test." | `curriculum/01-foundations.yaml:567` |
| Project grading `autograder` | `curriculum/01-foundations.yaml:568` |
| No `debate:` key; no `atlas:` key on the project | `curriculum/01-foundations.yaml:541-568` (absent) |
| JSON row mirrors the YAML (id, hours 90, prereqs, eight concepts with `module: CS6`, lab, grading) | `curriculum/curriculum.json` line 6817 (`"id": "CS6"`), key path `parts[].modules[]` with `part: CS` |
| Topological position: index 51 of 134 (after CS5 at 21 and M8 at 38) | `J:topological_order` |
| No atlas entry names CS6 (the atlas list names CS1, CS3, S0, ..., not CS6) | `J:atlas` (computed: `CS6` absent) |
| CS6 is a target of the Quant Developer track (targets CS6, QR2, MS2, DV4) | `curriculum/meta.yaml:186`; `J:tracks` QDEV |
| Credential table row "Quant Developer \| CS6, QR2, MS2, DV4 \| 38 \| 3,966 \| 1.84" and its dependency line "CS6 ... ← CS5, M8" | `CURRICULUM.md:160` and `CURRICULUM.md:299` |
| No module lists CS6 as a prerequisite | `J:parts[].modules[].prereqs` (computed: no dependents) |
| Direct prerequisite CS5: id line 512, prereqs `[CS2, CS4]` at 516, hours 130 at 515 | `curriculum/01-foundations.yaml:512-516` |
| Direct prerequisite M8: id line 329, hours 110 at 332, prereqs `[M2, M3, CS1, FC2]` at 333 | `curriculum/01-foundations.yaml:329-333` |
| CS2 (built, the nearest built CS prerequisite through CS5): prereqs `[CS1, M1]` | `curriculum/01-foundations.yaml:417-421` |
| Prerequisite closure of CS6 (computed): {AC1, CF1, CS1, CS2, CS3, CS4, CS5, E1, FC1, FC2, M1, M2, M3, M4, M8, P0.1}, 16 modules, 1,786 module hours | planner run of `coursekit.prerequisite_closure("CS6")` |
| Closure of CS5: {CS1, CS2, CS3, CS4, M1, P0.1} | planner run of `coursekit.prerequisite_closure("CS5")` |
| Closure of M8: {AC1, CF1, CS1, E1, FC1, FC2, M1, M2, M3, M4, P0.1} | planner run of `coursekit.prerequisite_closure("M8")` |
| Built units that CS6 may cite: M1-M7, CS2, E1-E5, FC1, FC2, AC1, CF1 (in closure); CS1, CS3, CS4, CS5, M8, P0.1 are in the closure but not built or not built as pages (`course/modules/CS/` holds only CS2) | planner run of `coursekit.built_units()`; `ls course/modules/CS` |
| The eight CS6 concepts are owned by CS6 (none is owned elsewhere) | planner run of `coursekit.concept_owner()`; `J:concepts` |
| Notation: T = return observations; Phi and Phi^-1 = standard normal CDF; gamma_3, gamma_4 registered; R^ast, R^{e ast}, R_f, Q registered (AP1); macros include \E, \Var, \Prob, \R, \N | `notation/notation.json:5-8` (\E), `:25-28` (\R), `:29-32` (\N), `:112-114` (T), `:117-120` (Phi), `:122-129` (gamma), `:132-150` (AP1) |
| Pyodide is pinned at 314.0.7 with packages numpy, scipy, pytest | `tools/vendor_spec.yaml:53-59` |
| The local runner runs only `runtime="python"` labs; any other runtime "has no local runner yet" | `tools/run_labs.py:70-71` |
| BLUEPRINT assigns C++20 to CS5, CS6, DV4 and the CS studio, run via Emscripten to WASM at build time | `BLUEPRINT.md:332` |
| BLUEPRINT names Python the primary language for every lab and most projects | `BLUEPRINT.md:331` |
| No Emscripten or C++ toolchain in the vendor spec | `tools/vendor_spec.yaml` (no `emscripten` or C++ entry; grep confirmed) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 90 h (`curriculum/01-foundations.yaml:544`). Tool rules:
- lesson `data-hours` 6-12 (`tools/check_pages.py:227`);
- hub `data-hours-lessons + data-hours-project = 90` (`tools/check_pages.py:337-338`);
- project share 10-40% of 90, i.e. 9 to 36 h (`tools/check_pages.py:340`);
- lessons sum to the hub's lessons figure.

Chosen split (§1): **7 lessons, 62 h; project 28 h (31.1%)**. 62 + 28 = 90. Feasible. No STOP condition on hours.

### 0.3 Blocking issues (architect decision required before builders start)

**B1. Grading mode `autograder` versus the deliverables "scaling plot" and "measured speedup".**
- The curriculum grades the project `autograder` (`yaml:568`) but its brief asks for a measured speedup (`yaml:565-566`) and
  its deliverable includes a scaling plot (`yaml:567`).
- An autograder in Pyodide cannot check a wall-clock speedup. Timings are not byte-comparable, and the browser is a single
  Pyodide interpreter (§11, item 3). The autograder can check the reconciliation (exact equality of serial and parallel results)
  and the invariance properties (§5.5), but not the speedup or the plot.
- **Plan's default (the architect confirms or replaces):** keep `autograder` as the curriculum states. The reconciliation and all
  numerical properties are autograded. The speedup run and the scaling plot are performed on the reader's own machine, are
  not graded by the autograder, and the page says so in one sentence. This leaves a required deliverable ungraded.
- **Recommended instead (Q1):** change `yaml:568` to `both` and add a rubric for the scaling report (speedup claim tied to the
  measured numbers, an Amdahl fit with its failure stated, the reconciliation evidence). The curriculum edit is the architect's.

**B2. The language target is undecided: BLUEPRINT names C++20 for CS6; the toolchain runs Python only.**
- BLUEPRINT assigns C++20 to CS6 (`BLUEPRINT.md:332`) and names Python for every lab (`BLUEPRINT.md:331`).
- The local runner executes only `runtime="python"` labs and reports other runtimes as having no runner (`tools/run_labs.py:70-71`).
  The vendor spec has no Emscripten or C++ entry, so a C++ grader cannot run in the browser or in `run_graders.py` (§11, item 4).
- **Plan's default:** every runnable lab and the grader are Python (stdlib, plus NumPy in L05 only). C++ appears only as static,
  annotated code labelled "static code, not run" (BUILDER_RULES §1.6). The C++ implementation path is out of scope for the
  autograder.
- Architect decision needed (Q2). Without it, the builders cannot know whether the grader is Python or C++.

**B3. Build order: CS5 and M8 are in CS6's prerequisites and are not built.**
- `course/modules/CS/` holds only CS2 (`ls course/modules/CS`). There is no page or plan for M8 (`plans/` has no M8 file) and no
  page or plan for CS5.
- BLUEPRINT §9 builds in topological order (`BLUEPRINT.md:448`); CS5 (index 21) and M8 (index 38) come before CS6 (index 51)
  in `J:topological_order`.
- Concept links from CS6 go to `concepts.html` anchors of CS5 and M8 concepts (BUILDER_RULES §4.1). Whether those anchors
  resolve before CS5 and M8 are built is NOT ESTABLISHED: `tools/build_site.py:195-213` writes module hrefs only for built
  modules, and the concept anchor behaviour for unbuilt modules was not read (§11, item 6).
- **Recommended (Q3):** build CS6 after CS5 and M8. If the architect allows an earlier start, the verifier must confirm that
  every CS5 and M8 anchor resolves.

Non-blocking, reported:
- **N1. VaR and expected shortfall are needed by the project and sit outside the closure** (owner PR4; `curriculum/04-quant.yaml:339-340`).
  Resolution in §4: plain prose with an explicit order-statistic definition in the spec. Q4 asks the architect to confirm.
- **N2. The data for the project.** No embedded dataset is named for CS6 (`yaml:558-566`). The project uses a SIMULATED
  portfolio (§6). No honest gap in the curriculum text.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

7 lessons: 8 + 8 + 10 + 10 + 8 + 8 + 10 = **62 h**. Project **28 h**. Total **90 h**. Concept counts per row sum to
1+1+1+2+1+1+1 = **8**, each concept in exactly one row (`yaml:549-557`).

| Lesson | Title (working) | Concepts it defines (`yaml:550-557`) | Lab (twin id, `tests/labs/CS6/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Latency, throughput and what a measurement is | `latency-vs-throughput` | `lab-CS6-L01-1`: a seeded job stream served one job at a time versus in batches, a deterministic model in integer microseconds; mean latency and throughput as exact `Fraction`s | 8 | A |
| L02 | Profiling: finding where the time goes | `profiling` | `lab-CS6-L02-1`: a four-stage pipeline instrumented with operation counters on a seeded input; each stage's share of operations as an exact `Fraction`; the dominant stage named | 8 | A |
| L03 | Amdahl's law and the limit of speedup | `amdahls-law` | `lab-CS6-L03-1`: exact speedup table S(p) = 1/((1-f)+f/p) at f = 9/10 and p in {1, 2, 4, 8, 16, 64}; the bound 1/(1-f) checked; a tick-level schedule reproduces S(p) exactly | 10 | B |
| L04 | Threads, processes and the GIL | `threads-vs-processes`, `python-gil` | `lab-CS6-L04-1`: a deterministic round-robin model with one interpreter lock; CPU-bound tasks gain nothing from threads in the model; waiting tasks overlap | 10 | B |
| L05 | SIMD vectorization | `simd-vectorization` | `lab-CS6-L05-1`: lane-blocked integer sums for lane widths 4, 8, 16 (operation counts, exact equality with the scalar sum); a NumPy ufunc sum checked for equality with the Python loop | 8 | C |
| L06 | The GPU programming model | `gpu-programming-model` | `lab-CS6-L06-1`: a lockstep (SIMT) issue model with w = 32 lanes as a stated parameter; issued-slot counts with and without divergence, exact integers | 8 | C |
| L07 | Independent parallel RNG streams | `parallel-rng-streams` | `lab-CS6-L07-1` (**the curriculum lab**, `yaml:561`): a chunked Monte Carlo estimate on per-chunk seeded streams; bit-identical results under reversed and seeded-shuffled completion order; the estimate changes when the chunk size changes; the error shrinks with n | 10 | D |
| index | Hub: objectives (4-8 verbs), prerequisites (CS5, M8 links), placement test, lesson map, ladder, hours split 62 / 28 | none | none | - | A |
| project | Parallel risk run (`autograder`, §5) | none | `lab-CS6-project-1` (rung 1), `lab-CS6-project-2` (rung 2, `class="lab completion"`), `lab-CS6-project-3` (rung 3 check) | 28 | E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py`; solution file `riskrun.py` in the panel | none | none | - | E |
| cards | `cards.json` from L01-L07 | none | none | - | F (after A-E) |

Ownership: **A** writes the hub `index.html` and L01-L02. **B** writes L03-L04. **C** writes L05-L06. **D** writes L07 (the
curriculum lab). **E** writes `project.html`, the grader folder and the three project labs, and depends on no lesson's text
(the spec is self-contained). **F** writes `cards.json` after A-E. Each builder writes only its own pages and twins.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses no CS6 concept; uses `limit` only in prose.
- L02 uses L01 (`latency-vs-throughput`) and CS2 `big-o-complexity` (`yaml:427`, prose or link).
- L03 uses L02 (`profiling`, the shares as the input to the bound) and M2 `limit` (`J:concepts` owner M2; closure).
- L04 uses CS5 `memory-hierarchy` (prose link, closure) and L01 for latency; defines no term from L03 by link.
- L05 uses CS1 `numpy-vectorization` (closure) and CS5 `memory-hierarchy` (closure).
- L06 uses L05 (`simd-vectorization`) for the lane model.
- L07 uses L04 (`threads-vs-processes`) for the chunk executor, L03 for the speedup of chunks, and M8
  `pseudo-random-number-generator`, `monte-carlo-integration` (closure) and CS4 `deterministic-computation` (closure).

Hours check: 8 + 8 + 10 + 10 + 8 + 8 + 10 = 62 (hub `data-hours-lessons="62"`); project 28 (hub `data-hours-project="28"`); 90 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to CS6)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md` (§1-§10), `BLUEPRINT.md` §3-§8, `plans/FINAL-ARCHITECT-RULINGS.md`,
`/Users/billyribeiro/.fanout/fixer-rules.md`, this file, and `plans/CS2-build-plan.md` (the nearest built prerequisite's
plan; its grader, rubric and hub conventions). Study `course/modules/CS/CS2/` (layout, `grader-panel` attributes at
`project.html:250`, ladder markup at `project.html:43-47`). Templates: `course/templates/`. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`, integers) and
   rounded only at display. A rounded figure states its rounding rule. Precedent: CS2 §4.1 item 1; CF1 L01 Remark 5.2.
2. **Lab statements match code and output.** The hypothesis states exactly what the twin prints; the interpretation names only
   what the printed numbers show. A hypothesis naming a quantity the code does not print is a FAIL (CS2 §4.1 item 2).
3. **Attribute nothing unread.** Only the keys in §7 may be cited, at paper or book level, and only with a locator the
   builder has read. No page, table, edition or year is typed from memory. The Hennessy record has no edition field (§7), so
   the edition in the curriculum string is not repeated in prose.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "the GIL serializes", "parallel speedup",
   "reproducible", "exact", "stable" each need a derivation on the page, a lab that computes the claim, or a stated hypothesis.
   Precedent: CS2 §4.1 item 4; E5 §2.1 item 4.
5. **Define before use.** Each of the 8 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson
   and never before it. Terms outside the 8 (chunk, scenario, value at risk, expected shortfall, speedup, efficiency, race condition,
   lock, shared state, estimator) are defined in prose at first use with a plain `<dfn>` and no `data-concept`
   (`tools/check_dag.py` skips a `<dfn>` without `data-concept`; `check_dag.py` docstring).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation lists numbered Assumptions (A1, A2, ...) before the
   statement. Required: Amdahl's law needs the timing model (fixed total work W, fraction f in [0, 1] of it perfectly divisible
   across p >= 1 workers, no overhead, no contention); the parallel-reduction invariance needs an associative and commutative
   combine on the chunk results (for the integer combine of §5.3 this holds exactly); the normal-tail check needs the Gaussian
   loss model.
7. **Grader rule (autograder).** Applies in full (§5.6). A test demands an exception only for a condition the spec names.
8. **Money.** Integer cents (fixer-rules; BUILDER_RULES guardrail). Portfolio values and scenario losses are `int` cents. The VaR
   is an `int` in cents. The expected shortfall is an exact `Fraction` in cents, rounded only for display (half to even, stated on
   the page). No `float` enters a money value, a rank, or a reconciliation.
9. **No horizontal scroll at 360 px.** Code lines wrap or sit in a scrolling `pre` inside its container.
10. **Labs call `main()` at top level.** No `if __name__ == "__main__":` guard (`run_labs.py` runs `python -I -W error <twin>`, E5 §2.1 item 10).
11. **Labs deterministic and honest about time.** Seeded draws only (`random.Random(seed)`). No wall-clock time appears in any
    expected output (CS2 §11 item 2 precedent). Counts, exact fractions and integer tick models are the measurements. Any
    measured time belongs only to the project's local section, which no lab prints.
12. **Models are labelled as models.** Statements about a real machine (cache sizes, SIMD widths, GPU warps, the GIL's behaviour in
    CPython) are either (i) a stated parameter or assumption of the model in the lab, or (ii) ungraded naming pending §7 requests.
    No claim about a real machine is graded T, and none is graded above C.
13. **Ruling 13 (T versus C for worked values).** A value the page derives by hand in a numbered Example (with its hypotheses) is
    graded T with the Example as basis. A value that appears only in lab output, or rests on SIMULATED data, is graded C naming the
    lab. A card and the key-results row it mirrors carry the same grade and basis.
14. **Ruling 14 (honest-pending definitions).** Not expected for CS6. If a concept's definition waits for an admitted source, mark
    it "definition pending" and state the model the lesson does define separately.
15. **Process safety (ruling 20).** No agent kills processes by pattern (no `pkill`, no `killall`). The labs and grader start no
    processes or threads. The student-run speedup measurement is the only place a process pool appears.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a basis (derivation or lab). A B- or
  C-graded claim names its published counter-evidence (BUILDER_RULES §2.5). §7 lists which claims lack a registry record.
- Concepts: §1 table; `<dfn>` only for the 8 registered concepts plus plain `<dfn>` for other terms. No `<a class="concept">` for any
  concept outside the prerequisite closure of §0.1 (§4).
- Prerequisite links: `href="../../../concepts.html#<id>"` for closure concepts; `href="Lnn.html#def-<id>"` for earlier CS6 lessons.
  A lesson never links a concept defined in a later lesson.
- Labs: code lives once in `tests/labs/CS6/lab-CS6-Lnn-1.py` (and `lab-CS6-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Lab ids `lab-CS6-<page>-<n>` (`tools/check_pages.py` lab-id rule,
  numbering in display order, `T:tools/check_pages.py:258-261` per CS2 §0). Standard library only, plus `numpy` in L05 (Q11).
  Seeded RNG only; no network; under 10 s in Pyodide; no warnings under `-W error`.
- **SIMULATED label:** on every lab and figure that uses generated data (all labs except the exact closed-form ones; §6).
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`).
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in
  code comments.
- Banned strings (`tools/check_pages.py:58-72`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis `...` outside code.
- Percent or speedup statements state the base and the direction. "Speedup" is defined as T(1)/T(p) on the model's own ticks.
- A finite enumeration is grade C with its basis named, not T (CS2 precedent).
- Every "checked" or "verified" claim names the lab, line or test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration.
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 contract.

### 2.3 Notation (binding; `notation/notation.json`)

| Registered symbol or macro | Registered meaning (locator) | CS6 rule |
|---|---|---|
| `T` | number of return observations (`notation.json:112-114`, S1) | **Never used for time.** Wall-clock time is `W_p` (ticks or seconds, stated). |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and its inverse (`:117-120`, M4) | Used exactly for the Gaussian quantile: `z_\alpha = \Phi^{-1}(\alpha)`. |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (`:122-129`, M4) | Not used. Plain `\gamma` is free but not used. |
| `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` | AP1 (`:132-150`) | Not used. |
| `\N` (macro) | natural numbers (`:29-32`) | **Not used for the scenario count.** The count is the plain letter `n`, defined per lesson (local). |
| `\R` (macro) | real numbers (`:25-28`) | Standard. |
| `\E`, `\Var`, `\Prob` (macros) | expectation, variance, probability (`:5-8`, `:13-16`, `:9-12`) | Standard. |

Local symbols (allowed; `notation.json` `about`: conventionally local letters are defined per lesson): `n` scenario count,
`B` or `chunk_size` the scenarios per chunk, `p` the number of workers, `f` the parallel fraction, `S(p)` speedup, `W_p` wall
time at p workers, `\alpha` the tail level, `v_i` the position value in cents, `\Sigma` return covariance, `L` the loss
(positive is a loss), `\sigma_L` the loss standard deviation, `\varphi` the normal density (not `\Phi`), `K` the number of positions.
Plain letters for the chunk index: `c`. Each symbol is defined on the lesson or spec section where it first appears and
never redefined. The word **chunk** replaces "block" everywhere in CS6, because a GPU "thread block" is a different object (§4, D8).

NOTATION_REQUESTS: none. The plan uses local symbols and the registered macros above.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

Each lesson follows BUILDER_RULES §4.2 (why it matters; core content in Definition, Theorem, Proof, Example and Remark blocks;
inline lab; where the canon breaks; misconceptions (at least 3); problem set (at least 3 problems in each of Mechanics, Proof,
Empirical and Research, each with a worked solution in `<details class="solution">`); key-results table; retrieval quiz (8-15
items)). The debate brief is not required (no `debate:` key, §0.1). Each lesson's "Where the canon breaks" names at least one
model limit and what changes without it.

- **L01 `latency-vs-throughput`.** Definitions of latency (time from request to result) and throughput (results per unit time),
  with the units stated. The exact batching model: a server with fixed overhead per batch and a fixed cost per job. Derivation
  (grade T, model-conditional) of mean latency and throughput for the batch size. Remark: the batch size that maximizes throughput
  is not the one that minimizes latency. Lab computes both exactly. Canon breaks: the model has no queueing variability.
- **L02 `profiling`.** Definition of a profile as the attribution of a cost to parts of a program. The operation-counter method and
  its limit (counts are not time). Shares as exact fractions. The dominant stage bounds the gain from optimizing that stage alone:
  this sentence is derived in L03 and only referenced here. Canon breaks: counts ignore memory effects (L05 and the CS5 cache
  material, `memory-hierarchy`).
- **L03 `amdahls-law`.** Assumptions A1-A3 (timing model of §2.1 item 6). Theorem (T): S(p) = 1/((1-f)+f/p), and S(p) < 1/(1-f)
  for every finite p when f < 1 (proved with the `limit` concept, M2 closure). Example: f = 9/10 table with Fractions. The
  tick-level schedule in the lab reproduces S(p) exactly under A1-A3. Remark: Amdahl's law is the model's bound; the claim that
  real programs follow it is a separate, unproved statement (grade C at most, counter-evidence named: §7 request R5).
  Citation: `amdahl1967validity` at paper level, with no claim about its content (ungraded naming sentence, ruling 39 precedent).
- **L04 `threads-vs-processes`, `python-gil`.** Definitions of a thread (shared memory within a process) and a process (separate
  memory). The model: one interpreter lock, so at most one thread runs Python bytecode at a time. The lab's round-robin model
  states this as its assumption (§2.1 item 12); it does not assert it as a measured fact about CPython. Consequences in the model:
  CPU-bound tasks sum to the serial time; waiting tasks overlap. Canon breaks: C extensions and I/O release the lock in real
  CPython; the model does not represent that. Shared mutable state and race conditions are defined in prose (D8) with a lab
  counterexample in the model only if the builder adds one.
- **L05 `simd-vectorization`.** Definition of a lane and a vector operation. Lane-blocked sum with width w: the number of vector
  operations is ceil(n/w) and the scalar operation count is n (exact integers; grade T by the counting argument). The NumPy
  check: the vectorized ufunc result equals the Python loop result exactly for integers; the lab claims equality, not speed.
  Canon breaks: the lane model ignores alignment, masks and memory bandwidth.
- **L06 `gpu-programming-model`.** Definitions of a kernel, a thread, a warp of w lanes executing in lockstep (SIMT), and divergence.
  The lab's issue model: a branch taken by a subset of lanes issues both paths. Counts are exact integers for a stated w (w = 32
  is a parameter, not a claim about any device). Canon breaks: the browser and CI have no GPU, so no GPU code runs; the GPU
  statements are the model's.
- **L07 `parallel-rng-streams`.** Definitions: a stream (a sequence of draws from one generator), a chunk (a fixed range of
  scenario indices), and the chunk stream `random.Random(f"{seed}:{c}")` (fixed in the spec, §5.3). Theorem (T): when the chunk
  layout and each chunk's stream are fixed, the combined result does not depend on the order in which chunks finish (the
  combine is over exact values sorted by index, §5.3). Assumption: the chunk streams are treated as independent in the
  analysis; seeding does not prove non-overlap (grade C; counter-based and splittable RNG literature is REFERENCE_REQUEST R6). The
  curriculum lab (`yaml:561`) prints the bit-identical reversed-order and shuffled-order results, the layout dependence, and the
  root-n decrease of the standard error (M8 `monte-carlo-integration`, closure). Canon breaks: the integer-cent rounding and the
  Gaussian model are assumptions of this lesson.

Lesson-level constraints: no lesson uses distributed-systems, message-passing (MPI) or quantum-computing content (none is in
the curriculum's CS6 entry, `yaml:546-548`). No lesson claims a speedup for any real program.

---

## 4. DAG problems (concepts that natural CS6 content would use outside the closure)

Prerequisite closure of CS6 (computed, §0.1): {AC1, CF1, CS1, CS2, CS3, CS4, CS5, E1, FC1, FC2, M1, M2, M3, M4, M8, P0.1}.
Owners below are from `J:concepts` and `coursekit.concept_owner()` (planner check).

| Ref | Concept or term | Owner (outside closure) | Where natural CS6 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `value-at-risk` | PR4 (`curriculum/04-quant.yaml:339`) | the project brief (`yaml:563-566`): full-portfolio VaR | Plain prose. VaR is defined in the project spec as the order statistic of §5.3 (no `<dfn>`, no link). DAG_DEFECT logged. Adding PR4 to CS6 is not recommended: PR4's closure is 16 modules and 1,766 h (computed). Q4. |
| D2 | `expected-shortfall` | PR4 (`curriculum/04-quant.yaml:340`) | the project's ES output | Same as D1: plain prose definition in the spec. |
| D3 | `linear-factor-model` | AP2 | the return covariance could be described as a factor model | Not used by name. The covariance is built as B B^T + D with positive diagonal D (positive definiteness from M3 `positive-semidefinite-matrix`, closure). |
| D4 | `delta-method` | S1 | standard error of a sample quantile | Not used by name. The quantile standard error is an explicitly labelled ASSUMPTION (asymptotic normality of the sample quantile, stated, not proved), with the tolerance stated in §5.6 (Q5). |
| D5 | `estimator` (and sampling distribution) | S1 | the chunked Monte Carlo estimate in L07 | Plain prose in L07, defined at first use with a plain `<dfn>`, no link. |
| D6 | `vectorized-backtest` | QR2 | none | Not used. |
| D7 | `geometric-brownian-motion` | SC2 | path simulation | Not used. The project's return model is one-period and Gaussian (§5.2). |
| D8 | speedup, efficiency, strong and weak scaling, race condition, lock, shared state, false sharing | no concept in the curriculum (`J:concepts`, grep for speedup, scaling, lock, race, share: no owner) | L01-L04, L07 | Plain prose with plain `<dfn>` where defined; GLOSSARY_REQUESTS for speedup, efficiency, race condition, lock, shared state. Weak scaling and false sharing are not used. |
| D9 | Gustafson's law (scaled speedup) | no concept, no registry record | a natural counter-model to Amdahl | Not used (not in the curriculum, not in the registry). REFERENCE_REQUEST R5 lists it as a lead for counter-evidence only. |
| D10 | normal-variate generation (inverse transform, Box-Muller) | no concept in the curriculum (grep for sampling and box: none) | the project's Gaussian scenarios | Plain prose inside L07 as the method used by `random.gauss`, with no claim about its quality beyond the lab. Not a DAG defect unless a claim is made; Q6 asks whether the architect wants an owner. |
| D11 | `central-limit-theorem`, `normal-distribution`, `multivariate-normal`, `cholesky-decomposition`, `monte-carlo-integration`, `pseudo-random-number-generator`, `numerical-stability`, `limit` | M4, M8, M2 (all in closure) | L03, L07, the project | No issue. Linked. |
| D12 | `memory-hierarchy`, `value-semantics`, `raii`, `compilation-model`, `webassembly-compilation`, `python-cpp-bindings` | CS5 (in closure) | L02, L04, L05, L06; the C++ question (B2) | No issue. Linked where used. |

Each row has a resolution, so no DAG_DEFECT blocks the build except D1 and D2, which the architect confirms (Q4).
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring); an unlinked use of D1-D10 passes the tool, so the
verifier reads each lesson for these names (VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): autograder, ladder, spec, grader

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the rung order, `tools/check_projects.py:33` per E5 §5.1)

CS6 is tier M, so rungs 1 and 2 are kept to the minimum (BUILDER_RULES §5.1, `BUILDER_RULES.md:188-189`; BLUEPRINT §4 expertise reversal).

1. **Rung 1, worked example** (`lab-CS6-project-1`, exact, not SIMULATED): one fully solved, annotated computation of VaR and ES
   for a ten-value loss list in integer cents, with a "why" note at each step (the rank rule of §5.3). Short by design.
2. **Rung 2, completion** (`lab-CS6-project-2`, `class="lab completion"`, SIMULATED-free, exact): the `combine` function with two
   expressions replaced by `___`; graded instantly; every page line equals the twin line or contains a blank
   (`tools/run_labs.py`, per E5 §5.1 item 2).
3. **Rung 3, independent project** (autograded, §5.3-§5.6): `riskrun.py` to the frozen interface, plus the local speedup run and
   its report. `lab-CS6-project-3` is the rung-3 check: it prints the reference numbers for one small instance so the learner can
   compare (CS2 precedent, `course/modules/CS/CS2/project.html:46`).
4. **Rung 4, stretch** (optional, not hour-counted, no ceiling): a second tail measure (for example a different quantile
   estimator) with its own stated accuracy; or a batched NumPy evaluation of the chunk losses, checked for exact equality.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the context, inputs, required outputs, constraints and grading terms, `tools/check_projects.py:34`)

- **Context.** A quant developer must compute the VaR and expected shortfall of a linear portfolio by Monte Carlo, in parallel,
  and show that the parallel result equals the serial result. The run uses SIMULATED returns (§6).
- **Inputs.** A generated instance `make_instance(seed)` (§5.4): K positions (3 to 6) with integer-cent values, a symmetric
  positive-definite daily return covariance, a tail level `alpha` in {0.95, 0.99}, a scenario count `n`, and the chunk size.
  Every instance is SIMULATED and labelled so on the page. No real data is used.
- **Required outputs.** `riskrun.py` implementing the interface of §5.3. A short `scaling.md` (local run, §5.7).
- **Constraints.**
  - Integer cents for every money value; ES as an exact `Fraction`; rounding for display half to even, stated.
  - The chunk streams are exactly `random.Random(f"{seed}:{c}")`, one per chunk index c, and the scenario-to-chunk layout is the
    one of §5.3. These are fixed so that the rung-3 reference numbers mean the same thing for every learner.
  - No `float` in a loss, a rank, or a reconciliation.
  - Standard library only, plus nothing else (`data-packages=""`, Q11). Python version to be confirmed: the Pyodide pin string is `314.0.7` (`tools/vendor_spec.yaml:54`); the planner reads it as Python 3.14, which the verifier confirms.
- **Grading.** Autograder (`autograder`, `yaml:568`). The spec's grading entry names the autograder (`GRADING_WORDS`, `tools/check_projects.py:38`, and
  `grading_problems` at `tools/check_projects.py:41-50`). If Q1 changes the mode to `both`, the grading entry must name both the
  autograder and the rubric.
- **Reading list.** `ol.reading-list` cites `amdahl1967validity` and `hennessy2017computer` (registry keys only, §7).

### 5.3 Interface (frozen in the spec; file `riskrun.py`; unit-local, not Atlas)

Frozen before Builder E starts (Q8). Names and types are part of the contract; the grader imports only these names.

```text
CHUNK = 500                                  # default scenarios per chunk
@dataclass(frozen=True)
class VaRResult:
    var_cents: int        # the VaR: the ceil(alpha*n)-th smallest loss, in integer cents; a positive value is a loss
    es_cents: Fraction    # the expected shortfall: the mean of the largest n - ceil(alpha*n) + 1 losses, exact
    scenarios: int        # the number of scenarios used, which must equal the n requested

def var_and_es(losses: Sequence[int], alpha: float) -> tuple[int, Fraction]
def chunk_losses(instance: Mapping[str, Any], c: int, n: int, chunk_size: int = CHUNK) -> list[int]
def combine(chunks: Sequence[tuple[int, Sequence[int]]], alpha: float) -> VaRResult
def serial_var(instance: Mapping[str, Any], n: int, alpha: float, chunk_size: int = CHUNK) -> VaRResult
def parallel_var(instance: Mapping[str, Any], n: int, alpha: float, workers: int,
                 chunk_size: int = CHUNK) -> VaRResult
```

Definitions the spec states (they are the tests' oracle, so they are exact):
- **Rank.** `k = ceil(n * a)` where `a = Fraction(repr(alpha))` (the decimal value of `alpha`, not its binary value). For n = 10 and
  alpha = 0.7 the rank is 7 (the float product 0.7 * 10 is not an exact integer in binary, so a float `ceil` gives 8; this is
  the trap of mutant m04). Q9 records this choice.
- **VaR.** `var_cents = sorted(losses)[k - 1]` (the k-th smallest loss, 1-based).
- **ES.** `es_cents = Fraction(sum(sorted(losses)[k - 1:]), n - k + 1)`, the mean of the n - k + 1 largest losses, exact.
- **Losses.** For scenario j of chunk c, draw K standard normals z_1..z_K in index order from the chunk stream, set
  `R = Lchol @ z` where `Lchol` is the Cholesky factor of the return covariance, and `loss = round(-sum(v_i * R_i))` with Python's
  `round` (half to even). Losses are `int` cents.
- **Chunk layout.** Chunk c holds scenario indices `[c * chunk_size, min((c + 1) * chunk_size, n))`. The number of chunks is
  `ceil(n / chunk_size)`. Chunk c draws only from `random.Random(f"{seed}:{c}")` and draws exactly as many scenarios as its
  range holds, so a full chunk does not depend on n.
- **combine.** Accepts the chunk results in any order, sorts them by chunk index, concatenates, and applies `var_and_es`. The
  result is therefore invariant under the order of the input list (exact integers and Fractions).
- **serial_var** equals `combine` over all chunks computed in index order. **parallel_var** computes the same chunks by any executor
  (serial or a process or thread pool) and returns the same `VaRResult` for every `workers` value.

**Named ValueError conditions (the only ones a test may demand).** Each named condition has its own test in both directions (§5.5):
- `alpha` not in the open interval (0, 1), in `var_and_es`, `combine`, `serial_var` and `parallel_var`;
- `n < 1` in `chunk_losses`, `serial_var` and `parallel_var`;
- `chunk_size < 1` in `chunk_losses`, `serial_var` and `parallel_var`;
- `workers < 1` in `parallel_var`.

Not named, so no test may demand an exception type: an empty loss list, a non-symmetric covariance, a non-positive-definite
covariance, an out-of-range chunk index. A correct implementation may return any value or raise any exception for those.

### 5.4 Instances (`grader/instance.py`)

`make_instance(seed: int) -> dict` is deterministic. For each seed it returns a dict with keys `seed`, `values_cents` (K ints,
K in {3, 4, 5, 6}, each in [100 000, 5 000 000]), `cov` (K x K floats: `B B^T + D`, with B of size K x 2 and entries drawn from
a seeded generator at the daily scale, and D diagonal with positive entries), `alpha` (0.95 or 0.99), `n` (default 10 000),
`chunk_size` (500), and `invalid` (one case that a named condition refuses, returned as a separate key). Every instance is valid.
Seeds 0-49 give materially different values and covariances (BUILDER_RULES §5.3). The docstring and the page say: **SIMULATED
returns; not market data.**

ASSUMPTION (Q5): the scale of the daily covariance (entries and diagonal range) is a planning choice. The builder fixes it, and
states it on the page as a modelling choice, not as an estimate of any market.

### 5.5 Tests (`grader/test_project.py`): properties and numbers only

Every test is under 5 s in Pyodide; the suite is under 60 s (BUILDER_RULES §5.3.4). Failure messages name the property violated
and give a concept hint; they never print the expected answer (`__tracebackhide__`, fixer-rules). The list is the minimum:

1. **Instance validity.** `make_instance` is deterministic (same seed, same dict); covariance symmetric with positive diagonal; the
   learner's `chunk_losses` output has the right length and `int` type.
2. **Exact VaR and ES on hand losses (oracle of §5.3).** For losses 1..10: alpha 0.9 gives VaR 9 and ES 19/2; alpha 0.5 gives VaR 5
   and ES 15/2 (the largest six: 5..10, mean 15/2); alpha 0.7 gives VaR 7 (the decimal rank rule, not the float trap). One test per
   case, both sides of the rank boundary (rank 7 and rank 8 cases).
3. **Named conditions, both directions.** alpha = 0 raises, alpha = 1 raises, alpha = 0.5 accepts (per function listed in §5.3);
   n = 0 raises, n = 1 accepts; chunk_size = 0 raises, chunk_size = 1 accepts; workers = 0 raises, workers = 1 accepts.
4. **Analytic tail check (seeds 0-49).** Population `sigma_L = sqrt(v' Sigma v)` in cents; `VaR = z sigma_L` and
   `ES = sigma_L phi(z) / (1 - alpha)` with `z = NormalDist().inv_cdf(alpha)` (standard library). The VaR error must lie within
   5 standard errors of the asymptotic quantile standard error (ASSUMPTION, §4 D4), plus one cent. The ES must lie within a stated
   relative tolerance (Q5; the builder fixes the number from the reference's measured error over seeds 0-49 and records it).
5. **Sign and ordering.** VaR is positive at alpha 0.95 and 0.99 on every seed; ES is at least VaR on every seed.
6. **Reconciliation.** `parallel_var` equals `serial_var` exactly (field by field) for workers in {1, 2, 3, 4} and for workers = 1000
   (ruling 36: no cap on workers; one accept test at a size beyond any realistic threshold).
7. **Order invariance.** `combine` over the chunk results gives the same `VaRResult` for the index-ordered list, the reversed list
   and a seeded shuffle.
8. **Chunk independence.** Two different chunk indices give different loss lists; a full chunk's losses do not depend on n.
9. **Scenario count.** `serial_var(n)` reports `scenarios == n` for n not a multiple of chunk_size (for example n = 1 237, chunk 500).
10. **Invalid instance refused.** The `invalid` key of `make_instance` is refused by a named condition only.
11. **Correlation sensitivity.** On an instance whose covariance has a large off-diagonal term, the analytic check (test 4) applies
    with the full quadratic form (kills mutant m07).

### 5.6 Starter, reference, and tolerances

- `grader/starter.py` raises `NotImplementedError` in every function; the suite must fail on it (`run_graders.py`).
- `grader/reference.py` is the full solution (`riskrun.py` content). It must pass seeds 0-49 (`run_graders.py --unit CS6 --seeds 0-49`).
  The parallel path uses a process or thread pool only where the platform provides one; a serial map is the fallback, and both
  give the same result (the reconciliation test). Excluded from deployment (BLUEPRINT §7).
- Tolerances are fixed in the spec by the builder, from the reference's measured errors over seeds 0-49, and recorded on the page.
  The plan does not fix the numbers (ruling 22: the page's stated accuracy binds the grader).

### 5.7 Local speedup run (not graded by the autograder unless Q1 changes the mode)

On the reader's own machine: run `parallel_var` for workers in {1, 2, 4, 8} with a fixed n, record wall times with a stated timer,
compute S(p) = W_1 / W_p and the efficiency S(p)/p, fit the serial fraction with the L03 model, and say where the fit fails. The
page states that the numbers depend on the machine and that no output of this section is compared by the autograder. Process
pools are the student's own; no lab starts one (ruling 20).

### 5.8 Mutants and alternatives (the verifier's work; VERIFIER_RULES §2.6; fixer-rules item 19; ruling 9)

**Ten student-error mutants** (single-change copies of the reference, under `ledgers/CS6/mutants/`; first docstring line names
the error; each must be killed by a named test; `tools/mutate_graders.py --unit CS6 --seeds 0-9`):

| Id | Student error | Killed by |
|---|---|---|
| m01 | `combine` reads the VaR from the arrival order without sorting by chunk index | test 7 (order invariance) |
| m02 | every chunk seeded with `random.Random(f"{seed}")`, so chunks repeat each other | test 8 (chunk independence) |
| m03 | chunk streams keyed by the worker index instead of the chunk index | test 6 (reconciliation across workers) |
| m04 | rank computed as `math.ceil(alpha * n)` in floats (gives 8 at alpha 0.7, n 10) | test 2 (exact hand cases) |
| m05 | loss sign flipped (gains counted as losses) | tests 4 and 5 |
| m06 | expected shortfall reported as the VaR | test 4 (ES tolerance) |
| m07 | covariance used only on its diagonal (independent positions) | test 11 (correlation sensitivity), then 4 |
| m08 | the partial last chunk dropped, so `scenarios` is less than n | test 9 (scenario count) |
| m09 | a number hard-coded for seed 0 from an earlier, wrong run | test 4 on seed 0 |
| m10 | `workers < 1` silently treated as 1 | test 3 (named condition, workers) |

Any mutant that survives and differs only where the page states nothing goes to `ledgers/CS6/equivalent/` with a README proof
(ruling 9). A mutant that differs only inside a stated tolerance is equivalent under ruling 22 and ruling 25.

**Five alternative correct implementations** of different styles (all must pass seeds 0-49 by `run_graders.py`; ruling 10):
- alt1 generator style: chunks produced by a generator with `itertools.islice`.
- alt2 object style: a `RiskRun` dataclass holding the instance, with methods for chunks and the result.
- alt3 tail by heap: VaR from `sorted`, ES from `heapq.nlargest` over the tail; exact same values.
- alt4 pairwise tree combine: chunk results combined in a balanced tree of exact integers; order-invariant by construction.
- alt5 executor style: `concurrent.futures` pool with a documented serial fallback; no shared mutable state; identical results.

Each alternative is a different program; none may change a spec definition (§5.3). A correct alternative that fails any test
is a finding against the test (ruling 10), not against the alternative, and goes back to the grader's owner.

### 5.9 Rubric (not applicable under `autograder`)

If Q1 changes the mode to `both`, the rubric is: four to seven criteria, four observable levels each, exemplars at two or more
levels, for the speedup report and the reconciliation argument. The plan does not write it unless Q1 is decided that way. No
question bank (not adversarial).

### 5.10 Time budget (`<table id="hours">`, sums to 28 h; a one-line rationale per row; `tools/check_projects.py:58-75` rules per E5 §5.3)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One exact ten-value VaR and ES, annotated line by line |
| Rung 2, completion problem | 3 | Fill the two blanks in `combine`, then run the instant check |
| Serial VaR and ES: instance reading, losses, `var_and_es`, `serial_var` | 5 | Implement the rank rule exactly and the chunk streams |
| Chunked streams, `chunk_losses`, `combine`, `parallel_var` | 6 | Implement the layout, the stream key and the order-free combine |
| Named conditions and property tests against the spec | 4 | `ValueError` on the four named conditions; invariance checks |
| Local speedup run and Amdahl fit (section 5.7) | 4 | Four worker counts, a timer, the fit and where it fails |
| Report and self-assessment | 4 | Scaling note with the numbers; score against the exemplars (if Q1 is `both`) |
| **Total** | **28** | equals `data-hours-project` on the hub (31.1% of 90 h) |

---

## 6. Real-data policy

- **Embedded data: none.** No dataset is named for CS6 (`yaml:558-566`). The embedded snapshots are `fx_daily`, `fx_monthly`,
  `ust_daily` (`tools/data_sources.yaml`; `course/assets/data/market/MANIFEST.json`), none of which the CS6 pages need.
- **Real data: not used.** The project and every lab use generated, seeded data labelled **SIMULATED** (BUILDER_RULES §1.7).
- **Honest-pending note (project data page):** "The project's returns are generated from a seed and are not market data. The
  speedup numbers in section 5.7 depend on your machine and are not a benchmark of any system."
- No `data-files` attribute on any lab. No MANIFEST entry is added. No DATA_REQUESTS.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (verified in `references/references.json`)

| Key | Record (as read) | Status | Use in CS6 |
|---|---|---|---|
| `amdahl1967validity` | proceedings article, DOI 10.1145/1465482.1465560, year 1967, container "Proceedings of the April 18-20, 1967, spring joint computer conference ... (AFIPS '67 (Spring))", pages 483, ACM Press (`references/references.json:508`); `used_by: ["CS6"]` | verified (Crossref); title and year match `yaml:559` | L03, paper level only. Ungraded naming sentence: no claim about the paper's content is made, because the planner has not read the paper. Reading list. |
| `hennessy2017computer` | book, Open Library, year 2017, ISBN 9780128119068, Elsevier, "Computer Architecture: A Quantitative Approach", `used_by: ["CS6"]` (`references/references.json:12366`) | verified (Open Library) | Book level, for background on the hardware models of L05 and L06, ungraded. The record has no edition field, so "6th ed." from `yaml:560` is not repeated in prose (B4 precedent, E5 §7.1). Reading list. |
| `psfndpython` | primary issuer page, "The Python Language Reference — Python 3.13.16 documentation", `used_by: ["CS1"]` (`references/references.json:19476`) | verified (issuer) | NOT cited for the GIL or threading: the planner did not read whether it covers them. Cited only for language-level statements the builder has read (locator required). |
| `harris2020array` | Nature article, DOI 10.1038/s41586-020-2649-2, year 2020 (`references/references.json:11627`); `used_by: ["BLUEPRINT", "QR3"]` | verified | Optional, L05 only, paper level, ungraded, if NumPy is used (Q11). |
| `glasserman2003monte` | book, DOI 10.1007/978-0-387-21617-1 (`references/references.json:10373`); `used_by: ["M8"]` | verified | Not cited. The root-n statement is M8's concept (`monte-carlo-integration`) and is linked, not re-cited. |
| `cormen2022introduction` | book, Open Library (`references/references.json:5964`); `used_by: ["CS2"]` | verified | Not cited by CS6. |

Keys not used by CS6: `stroustrup2022tour` (CS5), `wilson2014best`, `wilson2017good` (CS4), `goldberg1991every` (M8).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only; no bibliographic record typed by the planner)

- **R1.** {doi: null, authors: "Python Software Foundation (lead only)", year: "not typed", title: "documentation of the threading module, concurrent.futures and multiprocessing (issuer page)", venue: "docs.python.org (primary; the architect checks references/authorities.yaml)", needed_for: "L04: any statement about threads, processes, the interpreter lock or the process pool. Until admitted, L04 states the lock only as the model's assumption", confidence: "the need is certain; no record exists in the registry for these pages (grep of references.json for threading or concurrent: none)"}
- **R2.** {doi: null, authors: "GPU programming-model documentation or a textbook chapter (lead only; author not typed)", year: "not typed", title: "GPU programming model: kernels, warps and divergence", venue: "not typed", needed_for: "L06: any claim about a real device beyond the model's stated parameters", confidence: "the need is certain; no record identified by this planner"}
- **R3.** {doi: null, authors: "SIMD vectorization reference (lead only; author not typed)", year: "not typed", title: "SIMD vector instructions and lane widths", venue: "not typed", needed_for: "L05: any claim about a real instruction set", confidence: "the need is certain; no record identified"}
- **R4.** {doi: null, authors: "profiling practice reference (lead only; author not typed)", year: "not typed", title: "sampling versus instrumenting profilers", venue: "not typed", needed_for: "L02: any claim about how a real profiler measures", confidence: "the need is certain; no record identified"}
- **R5.** {doi: null, authors: "Amdahl counter-evidence literature (lead only): Gustafson's scaled-speedup argument (name only; author and venue not typed)", year: "not typed", title: "scaled speedup and fixed-work speedup: counter-evidence to a fixed-fraction bound", venue: "not typed", needed_for: "L03 Remark: a graded claim that real programs follow the bound (B or C) must name counter-evidence (BUILDER_RULES §2.5)", confidence: "the need is certain; the lead is a name only"}
- **R6.** {doi: null, authors: "counter-based and splittable parallel RNG literature (lead only; author not typed)", year: "not typed", title: "independent parallel random-number streams: counter-based and splittable generators", venue: "not typed", needed_for: "L07: any claim that the chunk streams are independent in a stronger sense than seeding (grade C at most without the record)", confidence: "the need is certain; no record identified"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4).
Until resolved, L02-L07 teach the models with derivations and label every empirical sentence C with its basis or remove it.

---

## 8. Atlas milestone

None. No `atlas:` key on the CS6 project (`yaml:562-568`) and no Atlas entry names CS6 (`J:atlas`). No `atlas/CS6.contract.md`
is needed. The grader panel uses a unit-local file, as CS2 does (`course/modules/CS/CS2/project.html:250`).

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/CS/CS6/cards.json`, ids `CS6-c001` upward, `lesson` in L01-L07; every lesson has at least one card
  (`tools/check_pages.py`, card rules, per CS2 §9). Expected 40-70 cards: one per definition (8), per misconception (at least 3 per
  lesson, so at least 21), and per key result.
- Grade T for every derived result, with `"basis"` naming the derivation or lab (for example `"basis": "Lab 3, Theorem 3.1 (exact)"`).
- Cite a registry key only for an attributed claim; `cite` is `[]` for a model result (BUILDER_RULES §7).
- Cards for a SIMULATED result name the SIMULATED lab in `basis`. Each card tests one fact.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit CS6          # --page L03 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit CS6
.venv/bin/python tools/check_projects.py --unit CS6
.venv/bin/python tools/run_labs.py --unit CS6             # --page L03 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/CS/CS6/L03.html                       # after the twin exists
.venv/bin/python tools/embed_labs.py course/modules/CS/CS6/L03.html --refresh lab-CS6-L03-1  # after a twin edit
.venv/bin/python tools/run_graders.py --unit CS6 --seeds 0-49   # reference and starter (after the grader exists)
.venv/bin/ruff check tests/labs/CS6 course/modules/CS/CS6/grader && .venv/bin/ruff format --check tests/labs/CS6
.venv/bin/mypy tests/labs/CS6 course/modules/CS/CS6/grader
```

Verifier only, on a quiet machine: `.venv/bin/python tools/mutate_graders.py --unit CS6 --seeds 0-9` (the ten mutants of §5.8),
the five alternatives through `run_graders.py` (seeds 0-49), `.venv/bin/python tools/page_smoke.py --unit CS6` (Pyodide;
`run_graders` on the page), `.venv/bin/python tools/verify_refs.py --unit CS6`.

Architect, once before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. Flag checks confirmed in the tools: `check_pages.py` and `check_dag.py` take `--unit`
(`tools/coursekit.py` loads the units); `check_projects.py` takes `--unit`; `run_labs.py` takes `--unit` and `--page`;
`run_graders.py` takes `--unit` and `--seeds` (`tools/run_graders.py:1-25`, `:138-139`).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** Per §8. `check_projects.py:144-145` skips the contract check when no `atlas` key exists.
2. **No debate.** No `debate:` key (`yaml:541-568`), so the debate branch of `check_pages.py` does not apply. The interpolation of
   contested claims (the Amdahl model's fit, the GIL model) still falls under BUILDER_RULES §2.5.
3. **Browser parallelism is NOT ESTABLISHED.** The pinned Pyodide is 314.0.7 (`tools/vendor_spec.yaml:54`). Whether threads or process
   pools run in that build was not checked. The plan therefore assumes the browser runs one process and one thread, and every
   grader and lab uses a serial path. A verifier must confirm this once before L04 is built (a one-line test in Pyodide).
4. **Only Python labs and graders run.** `tools/run_labs.py:70-71` rejects any runtime other than `python`. No C++ grader or lab is
   possible with the present tools (B2).
5. **Rung 2 must be graded instantly.** `check_projects.py` requires a completion lab or a quiz (its completion test, E5 §11 item 4).
   The plan uses a completion lab.
6. **Unbuilt prerequisites.** CS5 and M8 are unbuilt (B3). Whether `concepts.html` anchors resolve for unbuilt modules was NOT
   ESTABLISHED: `tools/build_site.py:195-213` shows module hrefs are written only for built modules; the concept index logic
   was not read. `check_dag.py` checks linked uses against the curriculum closure, not against built pages (its docstring).
7. **Floating-point platforms.** `random.gauss` uses the platform's math library (ASSUMPTION, to be measured). The rung-3 numbers
   and the lab's printed values come from CPython and must match Pyodide. The builder prints integer results or values rounded to
   a stated digit count with a stated `data-tolerance`, and the verifier runs both interpreters to confirm (Q6).
8. **check_dag sees linked uses only.** Unlinked uses of D1-D10 (§4) pass the tool; the verifier reads for them.
9. **The hub's data-hours rules.** Lessons 6-12 h (`tools/check_pages.py:227`); hub split 62 + 28 = 90 (`:337-340`); project share
   31.1% (`:340`).
10. **Grader panel attributes.** `check_projects.py:122-137` requires `section.grader-panel` with `data-unit`, `data-grader`,
    `data-suite`, `data-solution`, `data-starter`, and the files `reference.py` and `instance.py` on disk. CS6 sets
    `data-solution="riskrun.py"`, `data-starter="starter.py"`, `data-suite="test_project.py"`, `data-support="instance.py"`.
11. **Studios.** STUDIO-CS does not require CS6 (`yaml:370-373`). CS6 feeds only the Quant Developer track (`meta.yaml:186`).
    Nothing in CS6 depends on the studio.

---

## 12. Open questions for the architect (numbered; the recommended decision is stated for each)

1. **(BLOCKING) Grading mode versus deliverables (B1).** The curriculum says `autograder` (`yaml:568`) while the deliverables
   include a scaling plot and a measured speedup (`yaml:565-567`). **RECOMMENDED:** change `yaml:568` to `both` and add a
   four-criterion rubric for the scaling report (speedup claim tied to the measured numbers; the Amdahl fit and where it fails;
   the reconciliation evidence). The alternative, keeping `autograder`, leaves a required deliverable ungraded.
2. **(BLOCKING) Language target (B2).** BLUEPRINT assigns C++20 to CS6 (`BLUEPRINT.md:332`); the tools run Python only
   (`tools/run_labs.py:70-71`). **RECOMMENDED:** Python for every runnable lab and the grader; C++ only as static, annotated
   code labelled "static code, not run" (BUILDER_RULES §1.6). A C++ implementation path would need an Emscripten pipeline that
   the vendor spec does not have.
3. **(BLOCKING) Build order (B3).** CS5 and M8 are unbuilt and CS6 depends on both. **RECOMMENDED:** build CS6 after CS5 and M8
   (BLUEPRINT §9, topological order). If the architect allows an earlier start, the verifier confirms the CS5 and M8 concept anchors.
4. **D1-D2: VaR and expected shortfall (PR4).** **RECOMMENDED:** plain prose with the order-statistic definitions in the spec (§5.3),
   no link, DAG_DEFECT logged. Do not add PR4 (closure 16 modules, 1,766 h).
5. **Quantile standard error and the ES tolerance (D4, §5.5 test 4).** The asymptotic quantile standard error is an ASSUMPTION,
   and the ES tolerance is a number the builder measures from seeds 0-49. **RECOMMENDED:** state the SE as numbered Assumption A3
   on the page; fix the ES tolerance from the measured reference error and record the measurement in the ledger.
6. **Platform-stable normal draws (§11 item 7).** **RECOMMENDED:** the builder measures the CPython-versus-Pyodide agreement of every
   printed value once; if any printed value differs, the lab prints it rounded to a stated digit count with a `data-tolerance`,
   and the page says so in one sentence. No change to the chunk streams (Q7 stays).
7. **Chunk streams fixed in the spec.** `random.Random(f"{seed}:{c}")` with the layout of §5.3. **RECOMMENDED:** yes. The page
   states that seeding does not prove non-overlap (grade C, REFERENCE_REQUEST R6).
8. **Interface freeze.** Confirm §5.3 (names, types, the four named conditions, the rank rule, the layout) as the spec to freeze
   before Builder E starts. **RECOMMENDED:** freeze.
9. **Rank rule on floats (the trap of m04).** The rank uses `Fraction(repr(alpha))`, so alpha = 0.7 and n = 10 give rank 7.
   **RECOMMENDED:** yes; the alternative (binary-exact `Fraction(alpha)`) gives rank 8 at alpha = 0.7, which a learner would not expect.
10. **The word "chunk".** **RECOMMENDED:** "chunk" for the scenario partition everywhere, to avoid the GPU "thread block" meaning.
11. **NumPy in L05 only.** The concept `numpy-vectorization` is in the closure (`J:concepts`, CS1), and numpy is shipped in Pyodide
    (`tools/vendor_spec.yaml:59`). **RECOMMENDED:** NumPy in the L05 lab only, with exact equality checks and no speed claim; the
    grader and the project stay stdlib (`data-packages=""`).
12. **Lesson count and hours.** **RECOMMENDED:** 7 lessons (62 h) and a 28 h project (31.1%). Alternative within the rules: merge L01
    and L02 into one 14 h lesson (6 lessons, 60 h) with a 30 h project (33.3%); this loses one concept-per-lesson separation.
13. **Rungs 1-2 at tier M.** BUILDER_RULES §5.1 keeps rungs 1-2 to the minimum from tier M (`BUILDER_RULES.md:188-189`).
    **RECOMMENDED:** rung 1 is one ten-value example; rung 2 has two blanks.
14. **Speedup measured only locally (ruling 20 and §5.7).** **RECOMMENDED:** as stated, with the page sentence that the numbers depend
    on the machine.
15. **Mutants and alternatives (§5.8).** Confirm the ten mutants and the five alternatives. **RECOMMENDED:** confirm.
16. **Chunk size and instance size.** Default `chunk_size = 500`, `n = 10 000`. **RECOMMENDED:** keep, and the builder reports the
    Pyodide time of the suite; if a test exceeds 5 s, reduce n for that test only, and say so.
17. **Hennessy edition.** The record has no edition field. **RECOMMENDED:** cite the key only and do not repeat "6th ed." (B4 precedent).
18. **REFERENCE_REQUESTS R1-R6 (§7.2).** **RECOMMENDED:** admit R1 (Python threading and process documentation through the issuer
    allowlist) before L04 is built, since L04's threads and processes claims otherwise rest on the model alone; R2-R6 may follow.
19. **Glossary requests.** speedup, efficiency, race condition, lock, shared state (D8). **RECOMMENDED:** plain prose, with
    GLOSSARY_REQUESTS for each, as CS2 Q10 did.
20. **Rung-3 reference numbers.** `lab-CS6-project-3` prints reference numbers for one small instance. **RECOMMENDED:** yes, with
    integer cents and the rank rule of Q9.

---

## 13. After the builders

1. The orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 with the hub; L03-L04; L05-L06; L07 (the curriculum lab, with
   the CPython and Pyodide comparison of Q6); the project (grader, ten mutants, five alternatives, instance sampling).
   Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/CS6.verification.json`; verifier scripts under `ledgers/CS6/scripts/`; mutants under `ledgers/CS6/mutants/`;
   equivalent mutants with README proofs under `ledgers/CS6/equivalent/` (ruling 9).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B3 must be resolved
   or named as honest gaps first.

Architect decisions: pending (§12). This plan is the planner's proposal. Items that could not be established are listed in §11
(items 3, 6, 7) and in §12 (Q6).
