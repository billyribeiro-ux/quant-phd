# CS5 build plan: C++ & Systems for Finance (2026-11-09)

Unit: **CS5 · C++ & Systems for Finance** · tier M · 130 h · prerequisites [CS2, CS4] · no Atlas milestone · no debate key ·
project grading `autograder` (no rubric) · output directory `course/modules/CS/CS5/` (part code `CS`) · lab twins
`tests/labs/CS5/` · grader folder `course/modules/CS/CS5/grader/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. This file is the only file written.
Executors after architect sign-off: Haiku builders A to E (and F for cards), then independent Haiku verifiers
(VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: `C:<file>:<line>` = curriculum source line read; `J:<path>` = `curriculum/curriculum.json` path read;
`R:<file>:<line>` = registry line read; `T:<file>:<line>` = tool line read; `P:<file>` = prior plan read; `X:<file>` = binding
rules read. Anything not in the curriculum is marked **NOT IN CURRICULUM**. Planner-derived statements about the tooling were
checked by reading tool source or by running `tools/coursekit.py` (`prerequisite_closure`, `concept_owner`, `unit`) through
the repo venv (`.venv/bin/python -I`). No tool gate was executed by the planner.

**Status: BLOCKING ISSUES EXIST (§0.3).** The hours are feasible. The gate has no runner for C++ labs, no C++ grader path,
and no in-browser C++ runtime. The architect must decide B1 to B6 before the builders start.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part CS, order 2, "Computing & Software Engineering"; CS5 is its fifth module | `C:curriculum/01-foundations.yaml:367-369` (part), `:512` (CS5 id) |
| CS5 id and title "C++ & Systems for Finance" | `C:curriculum/01-foundations.yaml:512-513` |
| Tier `M`, hours `130` | `C:curriculum/01-foundations.yaml:514-515` |
| Prereqs `[CS2, CS4]` | `C:curriculum/01-foundations.yaml:516` |
| Core: "Modern C++ (C++20): value semantics, RAII, templates, the STL, memory hierarchy, cache effects, compilation, Python bindings, WASM compilation." | `C:curriculum/01-foundations.yaml:517-519` |
| `introduces` has **nine** concepts, one per line: value-semantics, raii, cpp-templates, standard-template-library, memory-hierarchy, struct-of-arrays, compilation-model, python-cpp-bindings, webassembly-compilation | `C:curriculum/01-foundations.yaml:520-529` |
| Sources: Stroustrup, A Tour of C++, 3rd ed. (2022); Drepper (2007), 'What Every Programmer Should Know About Memory' (no venue, no publisher given) | `C:curriculum/01-foundations.yaml:530-532` |
| Lab: "Array-of-structs vs. struct-of-arrays cache benchmark." (the curriculum lab; "benchmark" is a timing word, see B4) | `C:curriculum/01-foundations.yaml:533` |
| Project "C++ Monte Carlo kernel"; brief: "Port a Python Monte Carlo pricer to C++ with identical seeded output, expose it to Python, and document the speedup and where it comes from."; deliverable "C++ kernel, bindings, equivalence tests, benchmark."; grading `autograder` | `C:curriculum/01-foundations.yaml:534-540` (title 535, brief 536-538, deliverable 539, grading 540) |
| No `debate:` key on CS5; no `atlas:` key on the CS5 project | `C:curriculum/01-foundations.yaml:512-540` (absent) |
| No Atlas entry names CS5 (Atlas entries A1 to A20 are on CS1, CS3, and others; `meta.yaml:199-275`); the curriculum.json `atlas` key has no CS5 value | `C:curriculum/meta.yaml:199-275`; `J:atlas` (planner walk of the JSON) |
| JSON row mirrors the YAML (hours 130, prereqs CS2 and CS4, nine concepts with `module: CS5`, sources, lab, grading autograder) | `J:curriculum/curriculum.json:6783` (`"id": "CS5"`) |
| Topological index 21 of 134 (CS1 3, CS2 7, CS3 8, CS4 15, CS5 21, CS6 51, M8 38, DV4 98) | `J:topological_order` |
| Usable closure: CS5's prerequisite closure is **{CS1, CS2, CS3, CS4, M1, P0.1}**, computed with `coursekit.prerequisite_closure("CS5")` | planner run output; `tools/coursekit.py:239` |
| Closure hours: CS1 120 + CS2 130 + CS3 80 + CS4 80 + M1 100 + P0.1 6 = **516 h**; closure concepts (`introduces`): 12 + 13 + 9 + 9 + 14 + 11 = **68** | unit hours at `C:curriculum/01-foundations.yaml:386` (CS1), `:420` (CS2), `:455` (CS3), `:486` (CS4), `:90` (M1), `:9` (P0.1); planner sum via coursekit |
| Built prerequisites: CS2 (`course/modules/CS/CS2/`) and M1 (`course/modules/M/M1/`). Unbuilt: CS1, CS3, CS4, P0.1 (no `course/modules/CS/CS1|CS3|CS4`; no CS4 plan) | filesystem; `tools/coursekit.py` `built_units` |
| CS2 prereqs now `[CS1, M1]` (the CS2 architect decision added M1) | `C:curriculum/01-foundations.yaml:421`; `P:plans/CS2-build-plan.md:428-429` |
| CS4 prereqs `[CS2, CS3]`; CS4 introduces include `deterministic-computation` and `bit-for-bit-reproducibility` (both used by CS5 content) | `C:curriculum/01-foundations.yaml:487`, `:491-500` |
| CS5 concept owners: all nine are owned by CS5 (`concept_owner`) | `J:concepts/<id>/module` (planner check via `coursekit.concept_owner`) |
| CS5 is a requirement of STUDIO-CS ("Limit Order Book Matching Engine", requires `[CS2, CS5]`; brief asks for "C++ engine + Python API" with Python bindings) | `C:curriculum/01-foundations.yaml:370-381` (requires 373; brief 377-380) |
| Downstream: CS6 requires `[CS5, M8]`; DV4 "Numerical Pricing (C++)" requires `[DV1, M8, SC4, CS5]` | `C:curriculum/01-foundations.yaml:545`; `C:curriculum/03-markets.yaml:774` |
| CS5 is in the MS-FIN credential closure and supporting list | `J:stats.credentials[1].closure` (index 19), `J:stats.credentials[1].supporting` (index 11); `J:credentials` ids `[BS-FIN, MS-FIN, PHD-FIN]` |
| The closure of M8 (the Monte Carlo and IEEE 754 module) is {AC1, CF1, CS1, E1, FC1, FC2, M1, M2, M3, M4, M8, P0.1} = **1,366 h** including M8; M8 is not in CS5's closure | planner run of `coursekit.prerequisite_closure("M8")` plus hours; M8 entry `C:curriculum/01-foundations.yaml:329-365` (id 329, prereqs 333) |
| M8 introduces `ieee-754-floating-point`, `pseudo-random-number-generator`, `monte-carlo-integration`, `antithetic-variates`, `control-variates`, `importance-sampling` | `C:curriculum/01-foundations.yaml:338-353` |
| Concept index `course/concepts.html` contains the anchor `deterministic-computation` (concept index covers unbuilt modules), so a link to a CS4 concept can resolve | `course/concepts.html` (grep, planner) |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 130 h (`C:curriculum/01-foundations.yaml:515`). Tool rules:

- lesson `data-hours` 6 to 12 (`T:tools/check_pages.py:227`);
- hub `data-hours-lessons + data-hours-project = 130` (`T:tools/check_pages.py:332-342`);
- project share 10 to 40% of 130, i.e. 13 to 52 h (`T:tools/check_pages.py:339`);
- lessons sum to the hub's lessons figure (`T:tools/check_pages.py:332-342`).

Chosen split: **9 lessons × 10 h = 90 h; project 40 h (30.8%)**. 90 + 40 = 130. Feasible. **No STOP condition on hours.**

### 0.3 Blocking issues (architect decision required before builders start)

**B1. No gate can run C++ labs, and no runner exists for a C++ twin.** The curriculum's runtime for C++ is native
(BLUEPRINT §6 `BLUEPRINT.md:332`: "Emscripten → WASM at build time; native locally"). The tools do not implement either path:

- `T:tools/run_labs.py:70-71`: any runtime other than `python` returns "has no local runner yet".
- `T:tools/coursekit.py:273-274`: `Lab.twin` is hard-coded to `tests/labs/<UNIT>/<id>.py`; a `.cpp` twin cannot be addressed.
- `T:tools/embed_labs.py:84-88` and `T:tools/run_labs.py:55`: twins are run with `sys.executable -I -W error`; no compile step.
- `T:tools/page_smoke.py:245-270`: every lab on a page is executed in Pyodide (`page.evaluate`), with no runtime branch.
- `T:tools/check_pages.py:262-263` accepts `cpp` as a runtime value, but nothing executes it; `T:tools/check_pages.py:145-160` checks
  only `language-python` code blocks, so a C++ snippet on a page is not run by any gate (BUILDER_RULES §1.6 would be unenforced).
- `T:tools/mutate_graders.py:41` globs `ledgers/<UNIT>/mutants/*.py`; a C++ mutant cannot be run.

Vendored browser runtime: `course/assets/vendor/LOCK.json` and `tools/vendor_spec.yaml:53-57` pin Pyodide only. BLUEPRINT §6
says Emscripten output joins the lock file "with the first SQL and C++ modules" (`BLUEPRINT.md:346-347`). It has not.

**Recommended decision (Q1):** the architect approves a native C++ harness as a separate tooling unit, owned by the architect and
not by the builders (BUILDER_RULES §1.9 forbids builders editing shared tools). It adds: a `.cpp` twin suffix for `runtime="cpp"`
(`coursekit.py`), a compile-and-run step with a pinned flag set (`run_labs.py`, `embed_labs.py`), a skip list in `page_smoke.py`
for cpp labs that says so, and a compile-and-run mode in `run_graders.py` and `mutate_graders.py` (B3). Until it exists, no
C++ lab or C++ grader can satisfy BUILDER_RULES §1.6 or §6.1.

**B2. The browser cannot run a C++ grader, so BUILDER_RULES §5.3.4 and BLUEPRINT §5.2 (dual-mode) cannot be met as written.**
BUILDER_RULES §5.3.4 requires the identical suite in Pyodide and locally, each test under 5 s in Pyodide (`X:BUILDER_RULES.md:228-230`).
BLUEPRINT §5.2 states the same (`BLUEPRINT.md:276-284`). `page_smoke.py` runs a grader by pasting `reference.py` into the browser
panel (`T:tools/page_smoke.py:291-297`). For C++ no browser runtime exists (B1).

**Recommended decision (Q2):** CS5's autograder is native-only, and the project page says so in one sentence. The architect waives the
in-browser clause for this unit. The parts that can run in the browser stay in the browser: rung 1 and rung 2 (Python, §5.1).

**B3. The grader file convention conflicts with a compiled solution.** BUILDER_RULES §5.3.2 says `grader/reference.py` is the
full solution and must pass seeds 0 to 49 (`X:BUILDER_RULES.md:213-218`). `T:tools/check_projects.py:131-133` requires
`reference.py`, `instance.py`, the suite and the starter to exist in the grader folder. `T:tools/run_graders.py:51-61` copies a
single `reference.py` as the solution and runs `pytest` on it (`run_graders.py:65`). A C++ kernel is not a `.py` file.

**Recommended decision (Q3):** `grader/reference.py` is the Python oracle (the executable definition of the spec, §5.2). It is
also the source of expected values in the tests. `grader/reference_cpp/` holds the C++ reference solution (the kernel and the
binding). The architect amends §5.3.2 for compiled-language projects and adds a compile-and-run mode to `run_graders.py` (B1).

**B4. The curriculum lab says "benchmark".** `C:curriculum/01-foundations.yaml:533`. A timing benchmark is machine-dependent, and
`run_labs` compares expected output exactly (`T:tools/run_labs.py:101`; `compare_output` at `T:tools/coursekit.py:321-333`). The CS2
precedent replaces time with operation counts (`P:plans/CS2-build-plan.md` §12 Q3 and the CS2 architect decision at line 429).

**Recommended decision (Q6):** L05 lab counts the cache lines and bytes touched by an array-of-structs and a struct-of-arrays
scan under a stated line-size assumption (a deterministic model, labelled as a model). The native timing is an optional,
un-embedded stretch, reported with its machine and compiler. The architect decides whether to edit `yaml:533`; builders do not.
The counting precedent is `P:plans/CS2-build-plan.md` §12 Q3 (line 406-407) and the CS2 architect decision (line 429).

**B5. The brief presupposes a Python Monte Carlo pricer whose concepts are outside CS5's closure.** The brief says "Port a Python
Monte Carlo pricer" (`C:curriculum/01-foundations.yaml:536-537`). The concepts of a Monte Carlo pricer are M8's (`C:curriculum/01-foundations.yaml:338-353`).
M8 is not in CS5's closure (§0.1). Adding M8 raises the closure from 516 h to 1,366 h (§0.1).

**Recommended decision (Q4):** do not add M8. The spec supplies the whole numerical contract: the integer generator, the draw
order, the normal transform, the pricing formula and the standard error (§5.2), plus the Python oracle. The project then tests C++
engineering against a stated contract, not Monte Carlo theory.

**B6. "Identical seeded output" (`C:curriculum/01-foundations.yaml:537`) cannot be bit-for-bit for transcendental functions.**
The Python `math` and the C++ math library can differ in the last bit of `log`, `exp` and `cos`. The integer stream can be
bit-for-bit. The prices cannot in general.

**Recommended decision (Q5):** the integer stream is bit-for-bit identical (test T1, §5.4). Prices and standard errors agree with the
oracle within relative 1e-9 (plus absolute 1e-12). The spec says "identical" for the stream and "within stated tolerance" for prices.

**Non-blocking, reported to the architect:**

- **N1 Drepper (2007) has no admitted record.** `C:curriculum/01-foundations.yaml:532`. The review queue holds it as "no candidate
  established identity" (`T:references/review_queue.json:3`; `SEED_REPORT.md:29`, "used by CS5"). Its candidate DOI
  `10.1145/1454456.1454464` (`references/review_queue.json:12`) is a 2008 *Queue* article on transactional memory, a different work.
  It must not be admitted. The authorities allow-list (`references/authorities.yaml`) has no issuer or publisher entry for this
  report. REFERENCE_REQUEST (§7.2).
- **N2 `minsky2011ocaml` says `used_by: CS5`, but CS5 does not cite it.** `R:references/references.json:17413` (`used_by` includes
  `CS5`); `extra_sources.yaml:21` lists CS5. The curriculum's CS5 sources (`C:curriculum/01-foundations.yaml:530-532`) do not include
  it, and BLUEPRINT §6 places OCaml in "context only" (`BLUEPRINT.md:335`). CS5 does not cite it. The architect corrects the stale
  `used_by` (builders never edit registry records).
- **N3 Stroustrup edition.** `C:curriculum/01-foundations.yaml:531` says "3rd ed. (2022)". The record `R:references/references.json:21452`
  has year 2022, Open Library ISBN 9780136823544, and no edition field. Cite the key only; no edition in prose (the Blanchard precedent in
  `P:plans/E5-build-plan.md` §0.3 B4).
- **N4 CS4 is unbuilt.** No `course/modules/CS/CS4/` and no CS4 plan exist. CS5's prerequisite CS4 is taught in no built page. CS5 links
  to CS4 concepts resolve to `course/concepts.html` (§0.1); the definitions exist only when CS4 is built.
- **N5 The local compiler is not pinned.** `clang++ --version` reports Apple clang 21.0.0 at `/usr/bin/clang++`. No C or C++ compiler
  is in `~/.config/mise/config.toml` (read only; cmake 4.4.4 is at its line 25). `ninja`, `emcc` and `wasm-ld` are not on PATH.
  A probe showed that `clang++ --target=wasm32 -c` produces an object file (exit 0), so compile-only WASM work is possible locally.
  Pinning a compiler requires the user to run a `mise-root use -g <tool>@<version>` command after the architect picks a verified
  version. The planner did not run any mise command and supplies no version (Q8).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

9 lessons × 10 h = 90 h; project 40 h; total 130 h. The nine concepts are spread one per lesson; each appears in exactly one row
(`C:curriculum/01-foundations.yaml:520-529`).

| Lesson | Title (working) | Concept it defines (`yaml:521-529`) | Lab (twin id; runtime) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Compilation and linking | `compilation-model` | `lab-CS5-L01-1` (cpp): a two-translation-unit program; a deliberately duplicated non-inline definition is shown to fail at link, and the exit status is printed | 10 | A |
| L02 | Value semantics | `value-semantics` | `lab-CS5-L02-1` (cpp): a counting type; copy and move counts for a fixed sequence of operations, printed exactly | 10 | A |
| L03 | RAII and ownership | `raii` | `lab-CS5-L03-1` (cpp): a scope guard that counts acquisitions and releases on normal exit and on exception unwinding | 10 | A |
| L04 | Memory hierarchy and cache effects | `memory-hierarchy` | `lab-CS5-L04-1` (python, model): cache lines touched by sequential and strided scans of an array, under the stated line-size assumption (§3) | 10 | B |
| L05 | Array-of-structs vs. struct-of-arrays | `struct-of-arrays` | `lab-CS5-L05-1` (python, model; the curriculum lab, B4): lines and bytes touched to read one field of M records in AoS and SoA layouts | 10 | B |
| L06 | C++ templates and concepts | `cpp-templates` | `lab-CS5-L06-1` (cpp): a concept-constrained sum accepts arithmetic types; a rejected type is shown to fail to compile, and the compile status is printed | 10 | C |
| L07 | The standard template library | `standard-template-library` | `lab-CS5-L07-1` (cpp): container choice by operation counts on a seeded key stream: `std::vector`, `std::unordered_map` (CS2 hash map), `std::priority_queue` (CS2 binary heap) | 10 | C |
| L08 | Python bindings for C++ | `python-cpp-bindings` | `lab-CS5-L08-1` (mixed; B1): a C function with integer error codes, called from Python through `ctypes`; the mapping to `ValueError` is printed | 10 | D |
| L09 | Compilation to WebAssembly | `webassembly-compilation` | `lab-CS5-L09-1` (cpp, local): a freestanding wasm32 object produced by clang; the first eight bytes are checked (magic and version); no link and no browser run (Q7) | 10 | D |
| hub | `index.html` | none | none | - | A |
| project | `project.html`, `grader/`, project labs | none | `lab-CS5-project-1` (python, rung 1, SIMULATED); `lab-CS5-project-2` (python, `class="lab completion"`, rung 2, SIMULATED); `lab-CS5-project-3` (cpp, rung 3 check, SIMULATED) | 40 | E |
| cards | `cards.json` from L01 to L09 | none | none | - | F (after A to E) |

Builder ownership:

- **A**: L01, L02, L03, and `index.html` (the hub) after L01 to L03 exist.
- **B**: L04, L05.
- **C**: L06, L07.
- **D**: L08, L09.
- **E**: `project.html`, every file in `grader/` (including `reference_cpp/`, `starter`, `instance.py`, `test_project.py`), and the three project labs. E
  does not depend on the lesson text.
- **F**: `cards.json` after A to E finish.

A builder writes only its own pages, its twins and its files. Shared files (`references.json`, `notation.json`, MANIFEST,
`check_*` tools, the harness of B1) are requests (BUILDER_RULES §1.9).

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):

- L01 uses only CS1 and CS4 prose (build discipline; CS4 `deterministic-computation` and `bit-for-bit-reproducibility` are in
  closure).
- L02 uses L01 (`compilation-model`, for headers and inline definitions) in prose only.
- L03 uses L02 (`value-semantics`: a moved-from object and destruction) in prose.
- L04 uses CS2 `big-o-complexity` (for counts) and L01 only in prose.
- L05 uses L04 (`memory-hierarchy`) and L02 (copy counts as a layout cost, prose).
- L06 uses L02 (value semantics of template arguments) in prose; M1 `exponential-and-logarithm` is not needed.
- L07 uses L03 (containers own memory), L06 (templates), and CS2 `hash-map`, `binary-heap`, `big-o-complexity` (links to CS2 concepts,
  which are in closure).
- L08 uses L03 (ownership across a boundary) and L02 (copies of arguments); CS1 `python-function-scope` and `type-hints` (in closure).
- L09 uses L01 (the compile step) and L08 (the boundary); no later link.

Project labs use only the project spec's own definitions (§5.2) and CS1 `numpy-vectorization` is not used.

Hours check: 9 × 10 = 90 (hub `data-hours-lessons="90"`); project 40 (hub `data-hours-project="40"`); 130 total.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to CS5)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3 to §8, `plans/E5-build-plan.md` §2 (the structure precedent),
`plans/CS2-build-plan.md` (the nearest built prerequisite, same part, same rules for counts and grader), `plans/FINAL-ARCHITECT-RULINGS.md`
(rulings 9, 10, 13, 14, 19, 22, 25, 26, 30, 36, 37, 39), `/Users/billyribeiro/.fanout/fixer-rules.md`, and this file. Study
`course/modules/CS/CS2/` (hub, lesson, project and grader layout) and `course/modules/M/M1/` (lab twin naming). `course/templates/`
holds the four skeletons. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact integers or `fractions.Fraction` where possible,
   and rounded only at display, with the rule stated (for example, the project's standard error is shown to six decimals). Precedent:
   `P:plans/CS2-build-plan.md` §4.1 rule 1 (CF1 open items).
2. **Lab statements match code and output.** The hypothesis states the result the twin prints. The interpretation names only what
   the printed numbers show. A C++ lab's printed line is produced by the compiled program, never typed. Precedent: M1 LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Only the registry keys in §7 may be cited, at book level unless the builder has read the relevant text.
   No page, edition, section, number or date is typed from memory (`X:BUILDER_RULES.md:36-39`). Language-rule claims about C++ are
   not attributed to the ISO standard, which has no registry record and whose domain is not on the allow-list; each is either shown by a
   lab with the named compiler (grade C, basis = that lab) or stated as "not stated here".
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "zero-cost", "no overhead", "exact", "portable",
   "faster", "cache-friendly" are used only where a count, a compile result or a test computes the claim. CS5 scope, to confirm
   (Q20): single-threaded code; C++20 only; the one-sector generator and the single-step GBM terminal value of the
   project spec; no parallel, SIMD, GPU or profiling claims (those are CS6, §4 D6).
5. **Define before use.** Each of the nine concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson and
   never before it. Terms outside the nine are defined in prose at first use with a plain `<dfn>` and no `data-concept`
   (`T:tools/check_dag.py` skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation block lists its numbered Assumptions before the
   statement. Examples the builders must state: the cache-line count holds under Assumption A1 (a line of 64 bytes, aligned arrays);
   the ODR claim in L01 holds for the stated translation units; the counting claims in L02 and L03 hold for the stated operation sequence.
7. **Grader rule.** For the project grader, a test asserts an exception type only for a condition the spec names (§5.2 lists them).
   Each named condition gets its own isolated test in both directions of every inequality (rulings 19 and 36). Ruling 19 is binding for
   the grader: 10 student-error mutants, five alternatives, `__tracebackhide__ = True` on each check, and a failing check never prints the
   expected value.
8. **Money.** CS5 has no `*_cents` field. The project's prices are floats in currency units, documented in the spec. If a cents field is
   ever added it is `int` (i64) end to end (`X:CLAUDE.md` money rule).
9. **No horizontal scroll at 360 px.** Code blocks scroll inside their own `pre` container; tables wrap; nothing forces the page wider than
   360 px. `page_smoke.py` is the verifier's check (`T:tools/page_smoke.py:343`).
10. **Labs call `main()` at top level.** Every Python twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard (`T:tools/run_labs.py:55`). C++ twins have a `main` function as usual. The M1 twin `tests/labs/M1/lab-M1-L04-1.py` is the Python model.
11. **Model labs are labelled.** A lab that counts lines or operations in a model (L04, L05) says "model" on the page, and states that the
    counts are not measurements (precedent: CS2 Q3).
12. **Named assumptions.** Any fact about hardware (a 64-byte cache line, cache sizes), the compiler, or the platform is a named
    Assumption (A1, A2, ...) in the lesson or spec. It is not stated as a general fact (fixer rule 12).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a basis (a derivation, a lab or a test).
  A B- or C-graded claim names its counter-evidence (BUILDER_RULES §2.5). The registry holds no record that this plan checked for a
  claim about C++ performance; such claims are C with a lab basis or are removed.
- Concepts: §1 table. `<dfn>` only for the nine registered concepts, plus plain `<dfn>` for other terms (§2.1 rule 5).
- Links: `href="../../../concepts.html#<id>"` for CS1, CS2, CS3, CS4, M1 and P0.1 concepts; `href="Lnn.html#def-<id>"` for earlier CS5
  lessons. A lesson never links a concept defined in a later lesson. A link to an unbuilt module's concept (CS3, CS4, CS1) is
  allowed only through `concepts.html` (N4).
- Labs: code lives once in `tests/labs/CS5/lab-CS5-Lnn-1.py` (or `.cpp` under B1 option A) and `lab-CS5-project-1..3`. The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Lab ids match `lab-CS5-<page>-<n>` (`T:tools/check_pages.py:258-259`).
  Never type expected output. Standard library only for Python twins (`random.Random(seed)` for any seeded data); no network.
- SIMULATED label: on every lab or figure that uses generated data (the project's worked example, completion lab, rung 3 check, and the grader's
  instances). The L04 and L05 model labs use no random data; they are labelled "model", not "SIMULATED".
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in code comments
  (`P:plans/E5-build-plan.md` §2.2).
- Banned strings (`T:tools/check_pages.py:58-72`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
  "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Growth and speedup ratios state the base and the measure.
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- C++ code blocks on pages are not checked by `check_pages.py` (`T:tools/check_pages.py:145-160` checks Python only). Every C++
  block must be a lab twin or a checked snippet compiled by the harness of B1; a verifier compiles every C++ block it finds (BUILDER_RULES §1.6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols and macros that CS5 must not give another meaning (`notation/notation.json`, `symbols` and `macros`):

| Registered | Registered meaning (locator) | CS5 rule |
|---|---|---|
| `T` | number of return observations (`notation.json` symbol `T`, module S1) | **Conflict.** Maturity is written `\tau`. No bare `T` anywhere in CS5. |
| `R_f`, `R^\ast`, `R^{e\ast}`, `\mathbb{Q}` | AP1 meanings (`notation.json` symbols) | Not used. The interest rate is `r`. `\mathbb{Q}` only with its registered meaning, and not needed. |
| `\Phi`, `\Phi^{-1}` | standard normal CDF and inverse (M4) | Not used. The normal draw is the Box–Muller transform in the spec (§5.2), so no inverse CDF appears. |
| `\gamma_3`, `\gamma_4` | skewness, kurtosis (M4) | Not used. |
| `\E`, `\Var`, `\se`, `\Normal`, `\R`, `\iid`, `\indic` | registered macros (`notation.json` `macros`) | Use as registered. `\se` is the standard error of the price estimate (§5.2). |

Local symbols (allowed; `notation.json` `about`): `S_0` spot, `K` strike, `r` interest rate, `\sigma` volatility (conventionally local),
`\tau` maturity, `n` number of paths, `u_i` uniforms, `z_i` normal draws. Each is defined on the lesson or spec section
where it first appears and never redefined. Program names in C++ (`s0`, `strike`, `n_paths`) are code identifiers, not symbols.

NOTATION_REQUESTS: none. The plan uses only local symbols and the registered macros above.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the BUILDER_RULES §4.2 structure. Mandatory content, by lesson:

- **L01 `compilation-model`.** Translation units, headers, declarations versus definitions, linking, the one-definition rule, and `inline`.
  Lab `lab-CS5-L01-1` shows, by compile and link exit status, that a duplicated non-inline definition across two units fails at link.
  Claim grades: the link failure is C with basis = the lab. No registry key (the standard is not admitted, §7.2).
- **L02 `value-semantics`.** Copy and move construction and assignment, moved-from state, the rule of zero and the rule of five, and value
  equality. Lab `lab-CS5-L02-1` counts copies and moves for a fixed sequence on a counting type; the counts are exact integers. Grade of the
  counts: C, basis = the lab.
- **L03 `raii`.** Ownership bound to scope; destructors run on normal exit and unwinding. Lab `lab-CS5-L03-1` counts acquisitions and releases;
  the counts must balance on every path. Where the canon breaks: shared ownership and cycles (prose only; no registry key).
- **L04 `memory-hierarchy`.** Lines, sets, locality and the cost of a miss, stated as a model with Assumption A1 (64-byte line, aligned
  array). Derivation (T): the number of distinct lines touched by a sequential scan of `N` elements of `s` bytes is `ceil(N s / 64)` under A1
  and an aligned start; the claim is proved on the page. Lab `lab-CS5-L04-1` (python, model) prints the counts for sequential and strided scans.
  No hardware claim beyond A1 is made.
- **L05 `struct-of-arrays`.** Array-of-structs versus struct-of-arrays layouts. Lab `lab-CS5-L05-1` (python, model; the curriculum lab) counts
  lines and bytes touched to read one field of `M` records for stated record sizes. The page says the counts are a model, and that a timing
  is not claimed (B4). Grade of the layout claim: T for the count under A1; C for any statement about speed, basis = the lab.
- **L06 `cpp-templates`.** Function and class templates, C++20 concepts and `requires` clauses, and compile-time rejection. Lab `lab-CS5-L06-1`
  shows that a concept-constrained sum accepts arithmetic types and that a rejected type fails to compile (compile status printed).
- **L07 `standard-template-library`.** Containers and algorithms, iterators, and the operation counts of `std::vector` (append),
  `std::unordered_map` (CS2 `hash-map`) and `std::priority_queue` (CS2 `binary-heap`). Lab `lab-CS5-L07-1` prints operation counts on a
  seeded key stream; the expected complexity classes are stated from CS2 (grade T by CS2 concept, a link into the closure) and the counts
  are C, basis = the lab.
- **L08 `python-cpp-bindings`.** The three mechanisms (CPython extension API, `ctypes` with `extern "C"`, and third-party binding libraries)
  compared in prose, and the chosen one (`ctypes`, Q10). Integer error codes mapped to Python `ValueError` for the named conditions. Lab
  `lab-CS5-L08-1` (mixed runtime, B1) calls a C function from Python through `ctypes` and prints the mapping. No third-party binding library is
  named as a claim; none has a registry record (§7.2).
- **L09 `webassembly-compilation`.** The compile-to-wasm32 pipeline, the WebAssembly binary header (magic bytes and version), and what the
  browser needs that a native build does not (a loader, imports, the linear memory). Lab `lab-CS5-L09-1` (cpp, local) compiles a freestanding
  kernel with clang to wasm32, then checks the first eight bytes of the object (magic and version). Honest gap (Q7): the lesson does not link,
  load or run the module in a browser, because no `wasm-ld` or Emscripten is pinned (N5). The lesson states this on the page.

Lesson-level constraints:

- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it (for example, one-sector
  count models in L04 and L05, no threads in L07, the ctypes boundary in L08).
- No lesson uses a term from CS6 (Amdahl's law, SIMD, threads, GIL, profiling, latency versus throughput) as a concept (§4 D6).
- Misconceptions: at least three per lesson, each with the wrong belief, the correction and the lab or derivation that shows it.
- Retrieval quiz: 8 to 15 items per lesson, each with an explanation read against its lesson (precedent: CF1 KNOWN 6).

---

## 4. DAG problems (concepts that natural CS5 content would use outside the closure)

Prerequisite closure of CS5 (computed): **{CS1, CS2, CS3, CS4, M1, P0.1}**, 68 usable concepts (§0.1). Owners below are from
`curriculum.json` `concepts` (planner check via `concept_owner`).

| Ref | Concept (owner) | Where natural CS5 content would use it | Resolution in this plan |
|---|---|---|---|
| D1 | `ieee-754-floating-point` (M8, topo 38) | the identical-output claim (L08 and the spec); double-precision arithmetic | Plain prose "IEEE 754 binary64 (double)" with no link and no `<dfn>`. Architect default (no link to outside-closure concepts). The spec states the tolerance (§5.2). |
| D2 | `pseudo-random-number-generator`, `monte-carlo-integration`, `antithetic-variates`, `control-variates` (M8) | the project's generator and estimator | Plain prose in the project spec. The spec defines the generator and the estimator completely. No variance reduction is in scope. Q4. |
| D3 | `geometric-brownian-motion` (SC2), `black-scholes-formula` (FC2), `risk-neutral-valuation` (no key) | the pricer's model | The spec states the terminal-value formula in plain words and symbols (§5.2). No link. |
| D4 | `expectation`, `variance` (M4) | the standard error uses a sample variance; `\E` and `\Var` appear in the spec | The formula is written inline with its meaning in plain words, no `<dfn>`, no link (CS2 Q2 precedent). Logged as DAG_DEFECT. |
| D5 | inverse normal CDF (`\Phi^{-1}`, M4 registered symbol) | a normal draw method | Not used: Box–Muller in the spec (§5.2). |
| D6 | `amdahls-law`, `simd-vectorization`, `threads-vs-processes`, `python-gil`, `profiling`, `latency-vs-throughput` (CS6) | the speedup discussion (L05, L07, the project's report) | Not used. No parallel, SIMD or profiling claim. The speedup is described as single-thread, per-kernel, with the method stated. |
| D7 | `discount-factor`, `continuous-compounding`, `exponential-and-logarithm` (M1) | the discount factor `e^{-r tau}` in the spec | In closure (M1). Link is allowed. No DAG issue. |
| D8 | move semantics, undefined behaviour, pointers, const-correctness, build systems (CMake), test frameworks, pybind11 or nanobind, sanitizers, hardware cache sizes | L02, L03, L08, the project's build | NOT IN CURRICULUM as concepts. Plain prose, no `<dfn>`. Architect may request GLOSSARY_REQUESTS (CS2 Q10 precedent). Any hardware fact is a named assumption (§2.1 rule 12). |
| D9 | unbuilt prerequisites CS1, CS3, CS4 and P0.1 (not built) | links to their concepts | Allowed only through `concepts.html` anchors (N4). The planner verified that the anchor `deterministic-computation` exists in `course/concepts.html`. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation (Q4, Q21).**
`check_dag.py` checks linked uses only (`T:tools/check_dag.py` docstring). An unlinked use of D1 to D6 passes the tool, so the verifier
reads every lesson and the project for these names (VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): autograder, ladder, spec, interface, grader

### 5.1 Ladder (BLUEPRINT §5.1; `T:tools/check_projects.py:33` requires the rung order, RUNGS)

CS5 is tier M. From tier M upward, rungs 1 and 2 are kept to the minimum (`X:BUILDER_RULES.md:188-189`; `BLUEPRINT.md:222-223`).

1. **Rung 1, worked example** (`lab-CS5-project-1`, python, SIMULATED, runs in the browser): one fully solved, annotated path of the Python oracle
   with four draws, step by step: generator output, uniforms, the normal draw, the terminal value, the payoff, the discounted mean and the
   standard error. Each step has a "why" annotation. Short by design (minimal rung).
2. **Rung 2, completion** (`lab-CS5-project-2`, `class="lab completion"`, python, SIMULATED): two lines of the oracle are removed (`___`): the
   Box–Muller line and the sample-variance line. Graded instantly. The twin is the completed oracle; every page line equals the twin line or contains a
   blank (`T:tools/run_labs.py` docstring; `T:tools/check_projects.py:89` requires a completion lab or a quiz).
3. **Rung 3, independent project** (graded by autograder): the C++ kernel, the Python binding, the tests and the report (§5.2, §5.3).
   `lab-CS5-project-3` (cpp, native) is the rung-3 check: it runs the reference kernel on the default instance and prints the price, the
   standard error and the stream's first four outputs. It is graded by the native suite, not by the browser.
4. **Rung 4, stretch** (optional, not graded, not hour-counted): a second generator that satisfies the same stream contract for the same tests, or a
   payoff template that accepts a user payoff through a C++20 concept. The stretch states its hypothesis and its test.

### 5.2 Spec (`project.html`, `<dl class="spec">`; `T:tools/check_projects.py:34` requires context, inputs, required outputs, constraints, grading)

- **Context.** An analyst needs a C++ kernel that prices a European call and put by Monte Carlo under the stated model, with a standard error, and
  that exposes the result to Python. The kernel must reproduce the stated integer stream exactly, so that a result can be checked against the Python
  oracle. The project tests engineering against this contract.
- **Inputs.** No dataset (§6). The instance is generated by `make_instance(seed)` (§5.4) and labelled SIMULATED. The inputs are the spot `S_0`
  (float, `> 0`), the strike `K` (float, `> 0`), the rate `r` (float, a decimal rate per year, continuous compounding), the volatility `\sigma`
  (float, `> 0`, per year), the maturity `\tau` (float, years, `> 0`), the number of paths `n` (int, `>= 2`) and the seed (int, `0` to `2^64 - 1`).
  Non-finite floats are rejected.
- **Generator (a stated contract; constants to be fixed by the architect, Q11).** A 64-bit state advanced by integer operations only; the output
  for the state after each advance is a 64-bit unsigned integer `x`. A uniform is `u = ((x >> 11) + 0.5) * 2^{-53}`, which lies in `(0,1)`
  (`x >> 11` is in `[0, 2^53 - 1]`). The generator state is initialised from the seed by a stated integer rule. The planner does not type the
  constants (Q11).
- **Draw order.** Path `i` (`0` to `n - 1`) uses the next two uniforms in stream order, `u_{2i}` then `u_{2i+1}`. Box–Muller:
  `z_i = \sqrt{-2 \ln u_{2i}} \cos(2\pi u_{2i+1})`. Terminal value: `S_T = S_0 \exp((r - \sigma^2/2)\tau + \sigma\sqrt{\tau} z_i)`.
  Payoffs: call `\max(S_T - K, 0)`, put `\max(K - S_T, 0)`; discounted by `e^{-r\tau}`. Price = the mean of the discounted payoffs. Standard error
  `\se = \sqrt{ \sum_i (d_i - \bar d)^2 / (n-1) } / \sqrt{n}` with `d_i` the discounted payoff and `\bar d` their mean (sample variance, `n - 1`).
  The call and the put use the same draws.
- **Interface (frozen by this spec; the only contract).**
  - `rng_stream(seed: int, count: int) -> list[int]`: the first `count` 64-bit outputs for `seed`. `ValueError` when `count < 0`, or when
    `seed` is not an integer in `[0, 2^64 - 1]`.
  - `price_call_and_put(s0: float, strike: float, rate: float, vol: float, maturity: float, n_paths: int, seed: int) -> tuple[float, float, float, float]`
    returning `(call, call_se, put, put_se)`. `ValueError` for exactly these named conditions: any input non-finite; `s0 <= 0`; `strike <= 0`;
    `vol <= 0`; `maturity <= 0`; `n_paths < 2`; `seed` out of range. No other exception type is specified.
  - C ABI for `ctypes` (the binding is part of the deliverable): `extern "C"` functions with integer status codes; the Python wrapper maps them to the
    `ValueError` conditions above (Q10).
- **Tolerance.** The integer stream must equal the oracle bit for bit. Prices and standard errors must agree with the oracle within relative
  `1e-9` plus absolute `1e-12` (Q5).
- **Required outputs.** `kernel/mc_price.hpp`, `kernel/mc_price.cpp` (C++20, no third-party library), `bindings/streamkernel.py` (the `ctypes`
  wrapper with the frozen interface), `BENCHMARK.md` (method, machine, compiler string, repeats, median; the speedup against the Python oracle),
  `REPORT.md` (one page: where the speedup comes from, with the L04 and L05 counts cited as the model they are).
- **Constraints.** C++20 only. No third-party library. Single thread. Compiler flags fixed by the harness (B1), for example
  `-std=c++20 -Wall -Wextra -Werror -O2`; the exact set is fixed by the architect (Q8). Standard library and `ctypes` only on the Python side.
  Every number in `REPORT.md` states its unit, its rounding rule and its source (the run that printed it).
- **Grading.** Autograder (`grading: autograder` in the page's spec entry; `T:tools/check_projects.py:38` `GRADING_WORDS` requires the word
  "autograder"). No rubric. No exemplars required (`T:tools/check_projects.py:138-139` applies only to rubric or both).
- **Reading list** (`ol.reading-list`, registry keys only; §7.1): `stroustrup2022tour`; `glasserman2003monte` only if the architect approves
  (Q15). Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 40 h; one-line rationale per row; `T:tools/check_projects.py:103-121`)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate one path) | 2 | One solved four-draw path in Python, annotated line by line |
| Rung 2, completion problem | 2 | Fill the Box–Muller and sample-variance lines, then run the instant check |
| Generator and draw order in C++ | 7 | Integer state, the uniform map, the stream equal to the oracle bit for bit |
| Pricer, payoffs, discounting and standard error | 7 | Path loop, both payoffs from the same draws, `n - 1` in the variance |
| `extern "C"` boundary and `ctypes` wrapper | 6 | Status codes, the named `ValueError` mapping, input checks |
| Equivalence and property tests run locally | 6 | Suite on seeds 0 to 49; fix to green; time under the limits |
| Benchmark method and write-up (`BENCHMARK.md`) | 6 | Fixed flags, machine, repeats, median; speedup stated with its method |
| Report (`REPORT.md`) | 4 | One page: where the speedup comes from, grounded in the lab counts |
| **Total** | **40** | Equals `data-hours-project` on the hub |

Check: 2 + 2 + 7 + 7 + 6 + 6 + 6 + 4 = 40. Project share 40/130 = 30.8%, inside 10 to 40%.

### 5.4 Grader design (`grader/`; autograder; BUILDER_RULES §5.3; FINAL-ARCHITECT-RULINGS 9, 10, 19, 22, 25, 36, 37)

Files (the names are required by `T:tools/check_projects.py:131-133`):

- `grader/instance.py`: `make_instance(seed: int) -> dict`. Deterministic (`random.Random(seed)`, stdlib). Valid ranges, stated in the docstring
  and labelled SIMULATED: `S_0` in [50, 150]; `K` in [0.5 S_0, 1.5 S_0]; `r` in [0, 0.1]; `\sigma` in [0.05, 0.6]; `\tau` in [0.1, 3.0];
  `n` in [2000, 5000]. The MC seed is the instance seed. Each seed also returns one invalid case, chosen from the named conditions only, under a
  separate key. The fingerprint check of `T:tools/run_graders.py:79-103` requires distinct instances across seeds.
- `grader/reference.py`: the Python oracle (§5.2 in full; `math` and `fractions` as needed). It is the executable definition and the source of
  expected values (Q3). It also runs the suite in "oracle mode" (Q3).
- `grader/reference_cpp/`: the C++ reference kernel and binding, the solution under test.
- `grader/starter.py`: the `ctypes` wrapper with every function raising `NotImplementedError`. The suite must fail on it (`T:tools/run_graders.py:162-166`).
- `grader/conftest.py` (native only): compiles `kernel/*.cpp` with the harness flags and loads the library with `ctypes` (B1). It is not part of
  the browser path.
- `grader/test_project.py`: the suite. Each check has `__tracebackhide__ = True` (precedent `course/modules/CS/CS2/grader/test_project.py:55`).
  A failing check names the violated property and gives a concept hint. It never prints the expected value (ruling 19).

Tests (properties and numbers; one isolated test per named condition, both directions):

- **T1 stream bit-for-bit.** `rng_stream(seed, 64)` equals the oracle's list for every seed 0 to 49.
- **T2 price and standard error match the oracle.** For every seed 0 to 49, call, call_se, put and put_se agree within relative 1e-9 plus absolute 1e-12.
- **T3 standard error uses `n - 1`.** Two-path instance (`n_paths = 2`): `call_se` equals `|d_1 - d_2| / 2` exactly from the oracle's discounted payoffs
  (the sample variance is `(d_1 - d_2)^2 / 2`; its square root divided by `\sqrt{2}` is `|d_1 - d_2| / 2`).
- **T4 put-call identity on the same draws.** `call - put = e^{-r\tau} (\bar S_T - K)` where `\bar S_T` is the oracle's sample mean terminal value,
  within T2 tolerance.
- **T5 monotone in spot.** Same seed, `S_0` times 1.01: call does not decrease and put does not increase (per-draw monotonicity), tolerance 1e-12.
- **T6 non-negative prices.** `call >= 0`, `put >= 0` for seeds 0 to 49.
- **T7 different seeds differ.** All ten prices for seeds 0 to 9 are distinct.
- **T8 to T22 named conditions, one test each, both directions:**
  - `s0`: `0` raises, `1e-12` accepted (T8, T9);
  - `strike`: `0` raises, `1e-12` accepted (T10, T11);
  - `vol`: `0` raises, `1e-12` accepted (T12, T13);
  - `maturity`: `0` raises, `1e-12` accepted (T14, T15);
  - `n_paths`: `1` raises, `2` accepted (T16, T17);
  - non-finite input (`nan`, `inf`) raises (T18);
  - `seed`: `-1` raises, `2^64` raises, `2^64 - 1` accepted (T19, T20);
  - `rng_stream` count: `-1` raises, `0` returns `[]` (T21, T22).
  No other exception type is asserted (BUILDER_RULES §5.3.3; ruling 19). No threshold test beyond the named bounds (ruling 36; the spec states no upper limit).
- **Timing.** Each test under 5 s locally; the whole suite under 60 s (`T:tools/run_graders.py:40`, `SUITE_LIMIT_S`). Benchmarks are not tests.
- **Runtime in browser.** Not applicable (B2). The page says so.

Feedback: a failing check names the property and gives a concept hint ("the standard error divides by `n - 1`; see the variance definition"). It never
prints the expected price or standard error.

### 5.5 Ten student-error mutants (`ledgers/CS5/mutants/`; single-change copies of `grader/reference_cpp/`; ruling 19)

Each mutant opens with a first docstring line that names the student error. The suite must kill each one on seeds 0 to 9
(`T:tools/mutate_graders.py` usage; B1 for the C++ runner).

| # | Student error (single change) | Killed by (planned) |
|---|---|---|
| m01 | the generator's output is advanced once before the first draw is used (stream skips element 0) | T1, T2 |
| m02 | the draw order is swapped: `z = \sqrt{-2\ln u_{2i+1}} \cos(2\pi u_{2i})` (same law, different path values) | T2 |
| m03 | the discount factor is omitted from the price (undiscounted mean) | T2 |
| m04 | drift written as `r` in place of `r - \sigma^2/2` (the Itô correction is missing) | T2 |
| m05 | the standard error divides by `n` (population variance, `ddof = 0`) | T3, T2 |
| m06 | the accumulator is `float` (single precision) instead of `double` | T2 |
| m07 | the call payoff is not truncated at zero (`S_T - K`, signed) | T2, T6 |
| m08 | the put payoff is copied from the call (`\max(S_T - K, 0)`), a sign error | T2, T4 |
| m09 | the seed is mapped as `seed + 1` | T1, T2 |
| m10 | `vol <= 0` is accepted silently (no `ValueError`) | T12 |

Equivalent mutants are not expected. A change that differs from the reference only inside the stated tolerance (for example, a different
summation order) is equivalent and goes to `ledgers/CS5/equivalent/` with a README proof (rulings 9, 22, 25). No mutant is written at the tolerance
boundary (ruling 25). The mutants are written by the verifier in a fresh context (VERIFIER_RULES §2.6); the list above is the planner's suggestion
(CS2 precedent). Pass gate: `mutate_graders --unit CS5 --seeds 0-9` kills all ten.

### 5.6 Five alternative correct implementations (`ledgers/CS5/alternatives/`; ruling 10)

Each must pass seeds 0 to 49 (ruling 10), each written independently of the reference, each a different style:

1. plain loops; a `std::vector<double>` of discounted payoffs, then a two-pass mean and variance;
2. batched draws: the `2n` uniforms are generated into a buffer in stream order, then consumed in path order (same draw order as the spec);
3. a class `Pricer` owning the generator state (RAII), with `std::span` input for the payoffs;
4. a generic kernel over a generator type constrained by a C++20 concept (the same integer stream);
5. compensated (Neumaier) summation for the mean and the sum of squares. It differs only in rounding and passes T2 within 1e-9.

A "different method" that changes the draw order, uses a library normal generator (not the spec's transform), or uses a different
generator is a mutant, not an alternative (ruling 10: a float-based alternative that is wrong on a stated rule is a mutant).

### 5.7 Benchmark note (not graded numerically)

`BENCHMARK.md` records method, machine, compiler string and repeats. The suite checks equality, never time (CS2 Q3 precedent; timing is not
byte-comparable, `T:tools/run_labs.py:101` compares output only). A speedup claim in `REPORT.md` is C with the benchmark file as its basis.

---

## 6. Real-data policy

- **No dataset is named.** The CS5 entry names no dataset (`C:curriculum/01-foundations.yaml:512-540`). No `data-files` attribute on any lab.
  No MANIFEST entry is added by builders.
- **Simulated only.** Every generated instance (project labs, grader instances) is labelled SIMULATED on the page and in the grader docstring
  (BLUEPRINT §5.3, "Simulated data is always labelled SIMULATED").
- **Bring-your-own-data.** Not required. No CSV schema is documented.
- **DATA_REQUESTS:** none.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (verified in `references/references.json`)

| Key | Record (as read) | Status | Use in CS5 |
|---|---|---|---|
| `stroustrup2022tour` | book, Stroustrup, year 2022, Open Library ISBN 9780136823544, Pearson; `used_by: ["CS5"]` (`R:references/references.json:21452`) | verified | the curriculum source (`C:curriculum/01-foundations.yaml:531`); book-level exposition in L01 to L08; reading list. No locator. No edition in prose (N3). |
| `glasserman2003monte` | book, Glasserman, 2003, Springer; `used_by: ["M8"]` (`R:references/references.json:10373`) | verified | Project reading list only, if the architect approves (Q15). Makes no claim in the lessons. |
| `goldberg1991every` | article, Goldberg, 1991, ACM Computing Surveys; `used_by: ["M8"]` (`R:references/references.json:10493`) | verified | Not cited by default. The architect may allow it for the identical-output note in the spec (D1), at book or paper level only. |

Not cited by CS5: `minsky2011ocaml` (N2; `R:references/references.json:17413`); `cormen2022introduction` (CS2 source); `hennessy2017computer`
(CS6; the memory background is a named assumption, §2.1 rule 12); `amdahl1967validity` (CS6); `psfndpython` and `ramalho2021fluent` (CS1).
No key for pybind11, nanobind, CMake, GoogleTest, the C++ standard, Box and Muller, or the Python `ctypes` documentation exists in the registry.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed by the planner)

- `{doi: null, authors: "Drepper (lead only; the first author's name is the curriculum string)", year: "2007 (lead only; curriculum string, yaml:532)", title: "What Every Programmer Should Know About Memory", venue: "not typed; the curriculum string gives no venue", needed_for: "L04 attribution of the memory-hierarchy background, if a claim needs it; not needed if L04 states A1 as an assumption", confidence: "the curriculum string exists; the registry has no record; the review-queue candidate (DOI 10.1145/1454456.1454464, review_queue.json:12) is a different article and must not be admitted. An admission path needs an issuer or publisher page on an allow-listed domain (references/authorities.yaml), which this planner did not find."}`
- `{doi: null, authors: "Box and Muller (lead only, from memory; not verified)", year: "not typed", title: "the normal-deviate transform used in the spec", venue: "not typed", needed_for: "attribution of the transform in the spec (optional); the transform is defined in the spec itself", confidence: "low; the planner does not type the record"}`
- `{doi: null, authors: "Python Software Foundation (lead only)", year: "not typed", title: "ctypes foreign function library, Python documentation", venue: "docs.python.org (issuer domain on the allow-list, authorities.yaml, short psf)", needed_for: "L08 and the project's binding reference, if a claim about ctypes behaviour is made", confidence: "the domain is allow-listed; the page has not been read by the planner"}`
- `{doi: null, authors: "ISO/IEC JTC 1 (lead only; no record)", year: "not typed", title: "the C++20 language standard", venue: "not typed", needed_for: "none recommended; language claims are shown by labs with the named compiler (§2.1 rule 3)", confidence: "no allow-listed domain for the standard in references/authorities.yaml"}`
- `{doi: null, authors: "not identified (lead only)", year: "not typed", title: "a source for a typical cache-line size and cache capacities", venue: "not typed", needed_for: "only if a claim about hardware in general is made; default is Assumption A1, stated as an assumption", confidence: "the need is optional"}`

The architect resolves these through `tools/add_reference.py` (DOI, ISBN or an allow-listed issuer page; `X:BUILDER_RULES.md:93-95`).
Until then the lessons teach the models with derivations and labs, and any empirical or attributed sentence is removed or graded C with its basis.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for CS5 (§0.1). No `atlas/CS5.contract.md` is needed. The grader panel uses a
unit-local folder (CS2 precedent, `P:plans/CS2-build-plan.md` §7). Whether the kernel later becomes an Atlas component is outside this
plan (Q16 for STUDIO-CS).

---

## 9. Cards builder (Builder F, after A to E)

- `course/modules/CS/CS5/cards.json`, ids `CS5-c001` upward, `lesson` in L01 to L09 (`T:tools/check_pages.py:381-398`).
- One card per definition (nine), per misconception (at least 27 across nine lessons), and per key result (lab or derivation). Expected total
  50 to 80 cards.
- Grade T only for a derivation on the page (for example, the L04 line count under A1). `basis` names the lab or derivation that establishes a
  result, for example `"basis": "Lab L04-1 (model), A1"`. `cite` is `[]` where the result is a model result.
- A card for a C++ result cites the lab that compiled it, never the standard.
- No trivia cards. Each back is checkable against the lesson text.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted, once the B1 harness exists (`--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit CS5            # --page L03 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit CS5
.venv/bin/python tools/check_projects.py --unit CS5
.venv/bin/python tools/run_labs.py --unit CS5               # --page L04 for one lesson; cpp labs need the B1 runner
.venv/bin/python tools/embed_labs.py course/modules/CS/CS5/L01.html    # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/CS/CS5/L04.html --refresh lab-CS5-L04-1   # after editing a twin
.venv/bin/ruff check tests/labs/CS5 course/modules/CS/CS5/grader && .venv/bin/ruff format --check tests/labs/CS5 course/modules/CS/CS5/grader
.venv/bin/mypy tests/labs/CS5 course/modules/CS/CS5/grader                 # Python files only; strict, repository configuration
```

Not run for CS5 until the B1 and B3 tooling exists: `tools/run_graders.py --unit CS5 --seeds 0-49` (its Python-only path cannot run the C++
reference, `T:tools/run_graders.py:51-61`), `tools/mutate_graders.py --unit CS5 --seeds 0-9` (globs `*.py` only, `T:tools/mutate_graders.py:41`).

Verifier only, on a quiet machine: `.venv/bin/python tools/page_smoke.py --unit CS5 --pages <pages>` (not run by builders; timing-sensitive;
cpp labs are skipped by the B1 runner with a stated reason), `.venv/bin/python tools/verify_refs.py --unit CS5` (the unit ledger's run,
VERIFIER §2.1), and the native suite locally (`pytest course/modules/CS/CS5/grader/test_project.py` through the B1 harness).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`, and the full
gate in CLAUDE.md.

Flag checks: `check_pages.py`, `check_dag.py` and `check_projects.py` accept `--unit` and `--all`; `run_labs.py` accepts `--unit` and `--page`
(`T:tools/run_labs.py` `main`). The planner did not execute builder commands. It ran only the coursekit closure, concept-owner and hours functions (§0.1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No C++ runner anywhere in the gate** (B1). `run_labs.py:70-71`, `coursekit.py:273-274`, `embed_labs.py:84-88`, `page_smoke.py:245-270`.
2. **No in-browser C++** (B2). Pyodide only (`course/assets/vendor/LOCK.json`; `tools/vendor_spec.yaml:53-57`).
3. **Grader is Python-only and single-file** (B3). `run_graders.py:51-61`, `:65`, `:137-140`; `check_projects.py:131-133`.
4. **Mutants are Python-only** (B1). `mutate_graders.py:41`.
5. **No Atlas milestone and no debate.** `check_projects.py` skips the contract check when no `atlas:` key exists (`T:tools/check_projects.py:144-146`).
   `check_pages.py` requires a debate brief only when the entry has one (no debate key here).
6. **Rung 2 must be graded instantly.** `check_projects.py:89` accepts a completion lab or a quiz; the plan uses a completion lab (Python).
7. **Rubric not required.** `grading: autograder` only (`C:curriculum/01-foundations.yaml:540`); `check_projects.py:138-139` applies only to rubric or both.
8. **C++ code blocks are not checked** by `check_pages.py` (`T:tools/check_pages.py:145-160` checks only `language-python`).
9. **Lab count.** `check_pages.py` requires at least one inline lab per lesson (`T:tools/check_pages.py:253-255`); the plan has one per lesson, and the curriculum names one (`C:curriculum/01-foundations.yaml:533`). The plan's one-per-lesson choice is recorded here.
10. **Python version.** The vendored Pyodide is Python 3.14 (`course/assets/vendor/LOCK.json` URL `pyodide/v314.0.7`). `~/.config/mise/config.toml` pins Python 3.15.0 at line 45, and its comment at line 3 names 3.14 as the default. Graders run under the repo venv; the architect confirms which interpreter the local graders use.
11. **Compiler identity.** Apple clang 21.0.0 is the local compiler (N5). Its output (for example, warning sets and `long double` width) may differ from a Linux compiler. The page records the compiler string the harness prints.
12. **The M8 concepts are outside the closure.** Any link to them is a DAG defect (§4 D1 to D5). The verifier reads for unlinked uses (`T:tools/check_dag.py` docstring).

---

## 12. Open questions for the architect (numbered; each with a RECOMMENDED decision)

1. **(Blocking; B1) Native C++ harness.** Approve a separate tooling unit that adds a `cpp` runner for labs and the grader, a compile step with a
   pinned flag set, a skip with a stated reason in `page_smoke.py` for cpp labs, and a compile-and-run mode in `run_graders.py` and
   `mutate_graders.py`. **RECOMMENDED: approve, owned by the architect, before any builder starts.** L08 needs a mixed runtime (Python driver plus a
   compiled library); **RECOMMENDED: the same harness, with a Python twin that compiles and loads the library.**
2. **(Blocking; B2) Native-only autograder.** Waive the in-browser clause of BUILDER_RULES §5.3.4 and BLUEPRINT §5.2 for CS5. **RECOMMENDED: yes;
   the page states it in one sentence; rungs 1 and 2 stay in the browser.**
3. **(Blocking; B3) Grader file convention.** `grader/reference.py` is the Python oracle; `grader/reference_cpp/` is the C++ solution; amend
   BUILDER_RULES §5.3.2 for compiled-language projects. **RECOMMENDED: yes.**
4. **(Blocking; B5, D2 to D5) Do not add M8 to CS5's prerequisites.** The spec supplies the numerical contract and the oracle. Adding M8 raises the
   closure from 516 h to 1,366 h (§0.1). **RECOMMENDED: no prerequisite change.** Confirm the plain-prose resolutions in §4.
5. **(Blocking; B6) Tolerance statement.** The stream is bit-for-bit; prices and standard errors agree within relative 1e-9 plus absolute 1e-12.
   **RECOMMENDED: yes.**
6. **(Blocking for L05; B4) Curriculum lab "benchmark" (`yaml:533`).** Replace the timing lab with a deterministic model that counts cache lines
   and bytes; the timing is an optional un-embedded stretch. **RECOMMENDED: yes; the architect edits `yaml:533` if the wording must change.**
7. **(Honest gap; L09) WebAssembly.** (a) Accept the gap: the lab compiles a freestanding wasm32 object and checks its header; no link, no
   browser run; the page says so. (b) Pin Emscripten (the planner cannot choose a verified version; the user runs a `mise-root use -g` command
   after the architect picks one). **RECOMMENDED: (a) now; (b) only if the architect wants an in-browser C++ module (it would also add the
   first C++ entry to `vendor/LOCK.json`, BLUEPRINT §6).**
8. **(Verification blocker, not a builder blocker; N5) Compiler pin.** The local compiler is Apple clang 21.0.0 outside mise. **RECOMMENDED: the architect
   picks one verified compiler version for the harness; until a pin exists, every C++ output records the compiler string and the page says it.**
9. **Lesson count and hours.** **RECOMMENDED: 9 lessons × 10 h and a 40 h project (30.8%).** Alternatives within the rules: 8 lessons (merge L02 and L03, 80 h)
   with a 50 h project (38.5%); or 10 lessons × 9 h with a 40 h project. The concept assignment stays one per concept in every option.
10. **Bindings mechanism.** **RECOMMENDED: `ctypes` with `extern "C"` and integer status codes.** No third-party binding library: none has a registry
    record or a vendor entry; a library dependency would also change the spec's constraint "no third-party library".
11. **Generator constants.** The generator's integer constants are not typed by the planner. **RECOMMENDED: the architect specifies the generator and
    records where the constants came from (a source the architect has read). If none is admitted, the spec states the constants as its own definition,
    with Assumption A3 that the constants give a stream with no structure the tests can see.**
12. **Stroustrup edition.** **RECOMMENDED: cite the key only; no edition in prose** (N3; the E5 Blanchard precedent).
13. **Drepper.** **RECOMMENDED: no citation; L04 states A1 as an assumption. The architect may admit the paper through an allow-listed page later (§7.2).**
14. **`minsky2011ocaml` used_by.** **RECOMMENDED: CS5 does not cite it; the architect corrects the stale `used_by` (N2).**
15. **Reading-list keys.** **RECOMMENDED: `stroustrup2022tour` for the lessons and the reading list; `glasserman2003monte` in the project reading list only.**
16. **STUDIO-CS (downstream).** The studio requires CS5 (`yaml:373`) and asks for a C++ engine with Python bindings (`yaml:377-380`). Its grader will need
    the same harness. **RECOMMENDED: out of CS5's scope; confirm that the studio's grader is planned on the B1 harness.**
17. **Rungs 1 and 2 minimal.** **RECOMMENDED: minimal, as §5.1 describes, because CS5 is tier M (`X:BUILDER_RULES.md:188-189`).**
18. **Speedup not graded numerically.** **RECOMMENDED: yes; `BENCHMARK.md` and `REPORT.md` are reviewed by method, not by value.**
19. **Hardware assumption.** **RECOMMENDED: Assumption A1 (64-byte line, aligned arrays) stated as an assumption in L04 and L05, and nowhere as a general fact.**
20. **Scope.** **RECOMMENDED: single-thread; C++20 only; no CMake requirement for the student (the harness fixes the command); no CS6 content.**
21. **Glossary.** Plain-prose terms (move semantics, undefined behaviour, pointers, build systems) are plain `<dfn>`-free prose. **RECOMMENDED: no
    GLOSSARY_REQUESTS (CS2 Q10 precedent), unless the architect wants a glossary entry.**

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles, the lab-id numbering).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 to L03 (the three C++ labs and their compile results), L04 and L05 (the model labs and
   the counts), L06 and L07 (the C++ labs), L08 and L09 (the mixed and the WASM lab), and the project (the grader, the 10 mutants, the 5 alternatives,
   the labs). Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/CS5.verification.json`. Mutants at `ledgers/CS5/mutants/`, alternatives at `ledgers/CS5/alternatives/`, equivalent proofs at
   `ledgers/CS5/equivalent/` with a README, and verifier scripts under `ledgers/CS5/scripts/` (VERIFIER §3). No rubric exemplars (autograder only).
4. Delta verification closes the slice (FINAL-ARCHITECT-RULINGS 30). The unit is merged only when the unit ledger is PASS, or its remaining gaps
   (L09 link and run, the compiler pin, any honest gap) are named and agreed by the architect. B1, B2 and B3 must be resolved first.

Architect decisions: pending (§12). This plan is the planner's proposal. Where the architect answers a question, the architect's answer is appended
below this line and binds the builders (the CS2 plan's "Architect decisions" section is the precedent).
