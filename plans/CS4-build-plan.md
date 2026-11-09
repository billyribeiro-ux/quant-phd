# CS4 build plan: Software Engineering & Reproducible Research (2026-11-09)

Unit: **CS4 · Software Engineering & Reproducible Research** · tier U · 80 h · prerequisites CS2, CS3 · no Atlas milestone ·
no debate key · grading `autograder` (no rubric, no exemplars) · output directory `course/modules/CS/CS4/` (part code `CS`) ·
lab twins `tests/labs/CS4/` · mutants and alternatives under `ledgers/CS4/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders A to E, then F for cards,
then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum fact cites `file:line` read during planning. Tooling facts cite `tools/<file>:<line>`.
Facts the planner derived by running a tool are marked **planner run**. Anything not in the curriculum or the repository is
marked **NOT IN CURRICULUM** or **NOT VERIFIED IN REPO**.

**Status: BLOCKING ISSUE B1 (§0.3) must be decided before Builder E starts. Builders A to D (lessons and labs) may start once
open questions Q3 to Q5 are decided, because lessons and labs do not depend on the grader harness.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| CS4 entry spans `curriculum/01-foundations.yaml:483-511`; id `CS4` at 483 | `curriculum/01-foundations.yaml:483` |
| Title "Software Engineering & Reproducible Research" | `curriculum/01-foundations.yaml:484` |
| Tier `U`, hours `80` | `curriculum/01-foundations.yaml:485-486` |
| Prereqs `[CS2, CS3]` (only) | `curriculum/01-foundations.yaml:487` |
| Core: "Git workflows, testing (unit, property-based, regression), typing, packaging, CI, environment pinning, determinism, code review." | `curriculum/01-foundations.yaml:488-490` |
| `introduces` has 9 concepts, one per line: git-branching-workflow, property-based-testing, regression-test, continuous-integration, python-packaging, dependency-pinning, deterministic-computation, bit-for-bit-reproducibility, code-review | `curriculum/01-foundations.yaml:491-500` |
| Sources: two free-text strings, Wilson et al. (2014), PLOS Biology 12(1); Wilson et al. (2017), PLOS Computational Biology 13(6) | `curriculum/01-foundations.yaml:501-503` |
| Lab: "A property-based test finds a bug a unit test missed." | `curriculum/01-foundations.yaml:504` |
| Project "Reproducibility audit"; brief: "Take a deliberately broken research repository (unpinned, non-deterministic, no tests) and make it reproduce bit-for-bit, documenting every fix." | `curriculum/01-foundations.yaml:505-509` (title 506, brief 507-509) |
| Deliverable "Fixed repository plus an audit log."; grading `autograder` | `curriculum/01-foundations.yaml:510-511` |
| No `debate` key and no `atlas` key on CS4 or its project | `curriculum/01-foundations.yaml:483-511` (absent); `curriculum/curriculum.json:6749` (`"id": "CS4"` row has keys id, title, tier, hours, prereqs, core, introduces, sources, lab, project, part only) |
| JSON row matches the YAML (9 concepts with `module: CS4`, hours 80, prereqs CS2 and CS3) | `curriculum/curriculum.json:6749` (planner run: `coursekit.concept_owner()` gives module CS4 for all nine) |
| No Atlas entry names CS4. A1 is CS1 and A2 is CS3 | `curriculum/meta.yaml:199-201` (A1, module CS1); `curriculum/meta.yaml:203-206` (A2, module CS3); `CURRICULUM.md:164-170` |
| BLUEPRINT says CS4 teaches the Atlas git workflow. This is prose, not a curriculum entry | `BLUEPRINT.md:266-268` |
| CS4 is required by CS5 (prereqs `[CS2, CS4]`) | `curriculum/01-foundations.yaml:516` (CS5 id at 512); `CURRICULUM.md:293` |
| CS4 is required by QR1 (prereqs `[CS3, CS4, S0]`) and QR3 (prereqs `[S2, M7, CS4, QR2]`) | `curriculum/04-quant.yaml:570` (under QR1 at 566); `curriculum/04-quant.yaml:627` (under QR3 at 623) |
| CS4 is a supporting prerequisite pulled into the Master's and PhD closures | `CURRICULUM.md:90` (Master's, heading at 67); `CURRICULUM.md:116` (PhD, heading at 92) |
| CS4 is not a listed requirement of any studio. STUDIO-CS requires CS2 and CS5 | `curriculum/01-foundations.yaml:371-373` |
| CS2 prereqs now `[CS1, M1]` (architect decision applied to the curriculum) | `curriculum/01-foundations.yaml:421`; `plans/CS2-build-plan.md:429` |
| CS3 prereqs `[CS1]`; CS3 is not built (no `course/modules/CS/CS3/`) | `curriculum/01-foundations.yaml:456`; `ls course/modules/CS` (planner run: only `CS2`) |
| CS1 prereqs `[P0.1]`; CS1 is not built | `curriculum/01-foundations.yaml:387`; `ls course/modules/CS` |
| Prerequisite closure of CS4 (planner run: `tools/coursekit.py` `prerequisite_closure("CS4")`): **{CS1, CS2, CS3, M1, P0.1}** | planner run |
| Concepts owned by that closure: 59 (68 concepts in the closure's modules, minus CS4's 9) | planner run over `curriculum/curriculum.json` `concepts` |
| Python version in the curriculum's CS1 source string is 3.13; the runtime pin is 3.14 (CS2 Q9 decided 3.14) | `curriculum/01-foundations.yaml:405`; `tools/vendor_spec.yaml:54` (`version: "314.0.7"`); `plans/CS2-build-plan.md:429` |
| Hours rules: lesson 6-12 h; hub lessons + project = curriculum hours; project 10-40% | `tools/check_pages.py` `check_lesson` (lines 227-228), `check_hub` (lines 335-340) |

**Registry records for the two curriculum sources** (read from `references/references.json`):

| Key | Record (as read) | Matches the curriculum string | Locator |
|---|---|---|---|
| `wilson2014best` | "Best Practices for Scientific Computing", PLoS Biology, volume 12, issue 1, pages e1001745, year 2014, DOI 10.1371/journal.pbio.1001745, `status: verified`, `used_by: ["CS4"]` | yes (venue, volume, issue, year) | `references/references.json:23140` |
| `wilson2017good` | "Good enough practices in scientific computing", PLOS Computational Biology, volume 13, issue 6, pages e1005510, year 2017, DOI 10.1371/journal.pcbi.1005510, `status: verified`, `used_by: ["CS4"]` | yes (venue, volume, issue, year); title capitalisation differs only | `references/references.json:23224` |

Neither record carries a locator (no page, section or table). The planner has **not read** either paper. Per BUILDER_RULES §2.3 and
VERIFIER §2.1, no claim may be attributed to either paper until a builder has read its abstract, and then only at paper level.

**Notation:** the registry's `T` (number of return observations) is at `notation/notation.json:112`. The macro `\R` is at
`notation/notation.json:25`. The planner found no program-wide symbol that CS4 needs (§2.3).

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 80 h (`curriculum/01-foundations.yaml:486`). Chosen split: **8 lessons × 7 h = 56 h; project 24 h
(30.0% of 80)**. 56 + 24 = 80. Lesson hours 7 are inside 6-12 (`tools/check_pages.py:227-228`). Project 30.0% is inside 10-40%
(`tools/check_pages.py:340`). **No STOP condition on hours.**

### 0.3 Blocking issues and design constraints

**B1 (BLOCKING, architect decision). The autograded deliverable is a repository, and the grader harness handles one file.**
- The curriculum's deliverable is a "Fixed repository plus an audit log" (`curriculum/01-foundations.yaml:510`), and the grading
  mode is `autograder` (`:511`). The autograder must therefore test a multi-file tree: `pyproject.toml`, a lock file, the study
  package, tests and a CI workflow.
- `tools/run_graders.py:51-63` (`workspace`) copies **one** solution file (`shutil.copy(solution_source, target)`, line 61).
- `tools/mutate_graders.py:41` globs mutants as `*.py` only, and `:49` builds a workspace from one mutant file.
- `tools/check_projects.py:131-134` hard-codes `reference.py` and `instance.py` as grader files.
- `course/assets/js/grader.js:36-46` builds one text editor with `accept: ".py"`, and `:94` pushes one solution path. The
  browser grader therefore cannot load a repository. `BLUEPRINT.md:270-272` describes zip export and import for the in-browser
  workspace, but `grader.js` (lines 36-46 and 89-95, read by the planner) has no such path.
- **Options.** (a) **Recommended:** extend the harness so the solution panel names a directory (`data-solution="repo/"`), the local
  runner and the mutation runner copy trees, and the browser workspace imports and exports a zip (BLUEPRINT §5.1). (b) Change the
  deliverable to one module (curriculum edit; not recommended, because the curriculum names a repository). (c) Keep a single-module
  autograded deliverable and move the repository layout to a rubric (the curriculum grading would become `both`; curriculum
  edit). The planner cannot edit `tools/`, `grader.js` or `curriculum/*.yaml`.
- Until B1 is decided, no CS4 grader can be run, and no mutant or alternative can be verified. §5 is written for option (a).

**B2 (design constraint, resolved by this plan). The grader runs in the browser and locally with different environments.**
- Pyodide's package lock contains `pytest`, `numpy`, `scipy`, `pyyaml`, `packaging`, `tomli` and `setuptools`, and **zero**
  entries named `hypothesis` (planner run: `grep -ic hypothesis course/assets/vendor/pyodide/pyodide-lock.json` gives 0). The
  vendor spec lists `packages: [numpy, scipy, pytest]` (`tools/vendor_spec.yaml:59`). `requirements-dev.txt:2-4` pins `pytest`,
  `ruff` and `mypy` only. **Therefore no lab and no test may import `hypothesis`.** The property-based lab uses a seeded stdlib
  generator (§3, L03).
- The local runner sets `PYTHONHASHSEED=0` (`tools/run_graders.py:73`; `tools/run_labs.py:60`). The browser sets only `QF_SEED`
  (`course/assets/js/grader.js:95`). Hash-seed dependence is therefore invisible in both modes. **No mutant depends on hash
  randomisation.**
- **NOT VERIFIED IN REPO:** the browser cannot start child processes (`subprocess`). The grader must therefore import the student's
  package in-process and compare bytes in-process. The plan does not depend on a subprocess.
- The browser grader passes the same `QF_SEED` for every test (`grader.js:95`), so the seed is a single integer per run.

**B3 (tooling gotcha, binding on Builder E). The instance fingerprint check can fail on a correct generator.**
- `tools/run_graders.py:88-98` (`check_instances`) fingerprints each instance field as
  `np.asarray(value).tobytes().hex()[:64]` for any value with `__len__` (line 93). Two consequences:
  (i) a `dict` value is hashed by object pointer and so looks nondeterministic across two calls, which is a **false FAIL**;
  (ii) a string or numeric array is fingerprinted by its first 32 bytes only, which is the first 8 characters of a `str`. Two
  seeds whose strings differ only after the first 8 characters look identical, which is a **false FAIL** ("some seeds produce
  identical instances").
- **Rule:** `make_instance(seed)` returns only `int`, `float` or `str` values. It includes an `int` field equal to `seed`. That
  field makes every full fingerprint unique, so the "identical instances" check cannot fire on a correct generator. The `str`
  fields need no discriminator of their own (the expected-output text begins with the same JSON header for every seed, which is
  harmless once the seed field is present).

**B4 (DAG, architect decision; recommended default in §4).** Four concepts that natural CS4 content uses sit outside the closure:
`ieee-754-floating-point` and `pseudo-random-number-generator` (both M8), `variance` (M4) and the wording "replication package"
(`replication-package`, CAP1). See §4 D1 to D4.

**B5 (CS2 precedent, binding).** The architect decided the CS2 `variance` and `quantile` issue as plain formulas with no `<dfn>` and no
link (`plans/CS2-build-plan.md:429`, "Issue 2/Q2"). CS4 follows the same rule (§4 D3).

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

**Structure rule.** The builders A to E each own a set of files. The brief asked for about three lessons per builder. That cannot
hold for five builders at 80 h: with 6-12 h per lesson the unit has room for at most 13 lessons, and five builders at three
lessons each would need 15. The plan therefore gives **two lessons per lesson builder (A to D)**, and Builder E owns the project
only. This is the same split the E5 plan uses (`plans/E5-build-plan.md` §1: A L01-L02, B L03-L04, C L05-L06, D L07-L08, E project),
and it is the architect question Q6.

8 lessons × 7 h = 56 h; project 24 h; total 80 h. Concepts per row sum to 2+1+1+1+1+1+1+1 = 9, each concept in exactly one row
(`curriculum/01-foundations.yaml:492-500`).

| Lesson | Title (working) | Concepts it defines (`introduces`) | Lab (twin id, `tests/labs/CS4/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Branches, pull requests and review | `git-branching-workflow`, `code-review` | `lab-CS4-L01-1`: a seeded SIMULATED commit history (a DAG of commits with two parents for merges). The merge base of two branch tips is computed by two methods and checked equal over 200 seeded histories; the count of histories is printed | 7 | A |
| L02 | Unit tests become regression tests | `regression-test` | `lab-CS4-L02-1`: a golden-output test pins the study's output for seed 0; a deliberate one-character change to a formula is caught and the failing line is printed | 7 | A |
| L03 | Property-based testing (**the curriculum lab**, `curriculum/01-foundations.yaml:504`) | `property-based-testing` | `lab-CS4-L03-1`: a seeded stdlib generator and a shrinking loop. A buggy `merge_intervals` passes three hand-picked unit tests and fails a property; the shrunk counterexample is printed. Stdlib only (§4 D5) | 7 | B |
| L04 | Python packaging | `python-packaging` | `lab-CS4-L04-1`: parse a `pyproject.toml` with `tomllib`; check the presence of `[build-system]` and of the required `[project]` keys; a file missing `[build-system]` is reported | 7 | B |
| L05 | Dependency pinning and lock files | `dependency-pinning` | `lab-CS4-L05-1`: check a lock file: every line is `name==version` with one or more `--hash=sha256:<64 hex>` items. The sha256 of a generated byte string is computed with `hashlib` and matched | 7 | C |
| L06 | Deterministic computation and seeded randomness | `deterministic-computation` | `lab-CS4-L06-1`: the same seed gives the same `random.Random` stream twice in one interpreter; the module-level `random` state leaks between two calls and the second result changes. SIMULATED stream | 7 | C |
| L07 | Bit-for-bit reproducibility | `bit-for-bit-reproducibility` | `lab-CS4-L07-1`: the same numbers summed in two orders give two different float bit patterns (printed with `float.hex`); exact `Fraction` sums are order-free and equal. Deterministic arithmetic, not SIMULATED | 7 | D |
| L08 | Continuous integration | `continuous-integration` | `lab-CS4-L08-1`: a gate that runs named checks in a fixed order and stops at the first failure; the exit status and the list of checks run are printed for two inputs. Simulated CI, not a CI service | 7 | D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 56/24 | none | none | - | A |
| project | Reproducibility audit (`autograder`, §5) | none | `lab-CS4-project-1` (rung 1), `lab-CS4-project-2` (rung 2, `class="lab completion"`), `lab-CS4-project-3` (rung 3 check) | 24 | E |
| grader | `grader/instance.py`, `grader/reference.py`, `grader/starter/` (the broken repository), `grader/test_project.py` | none | none | - | E |
| cards | `cards.json` from L01-L08 | none | none | - | F (after A-E) |

**Ownership rule.** Builder A writes `L01.html`, `L02.html`, its two twins and `index.html` (the hub, after L01 and L02 exist, with
the full lesson map). Builder B writes `L03.html`, `L04.html` and their twins. Builder C writes `L05.html`, `L06.html` and their
twins. Builder D writes `L07.html`, `L08.html` and their twins. Builder E writes `project.html`, the whole `grader/` folder and
`lab-CS4-project-1..3`. Builder F writes `cards.json` after A to E finish. No builder writes a file outside its list.

**Ordering check** (no lesson links a later definition; `tools/check_dag.py` checks linked uses only, its docstring):
- L01 uses only material in the closure, in prose (no concept link is needed).
- L02 uses `unit-test` (CS1, in closure) and L01 for the test workflow (prose).
- L03 uses `unit-test` (CS1) and `hash-map` (CS2) only in prose. Its generator uses `random.Random` (stdlib).
- L04 uses `python-modules-packages` (CS1, in closure).
- L05 uses `data-manifest` (CS3, in closure) by analogy only (prose, with a link to `../../../concepts.html#data-manifest` if the
  builder writes the analogy; otherwise no link).
- L06 uses `type-hints` (CS1, in closure) for the signatures in its code.
- L07 uses L06 (`deterministic-computation`) and the M8 concept in plain prose (D1).
- L08 uses L01 (`git-branching-workflow`) and L02 (`regression-test`) by link.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to CS4)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md` (§1-§10), `BLUEPRINT.md` §3-§8, `plans/CS2-build-plan.md` (the nearest built
prerequisite; its §4.1 rules 1-11 apply here), this file, and `plans/FINAL-ARCHITECT-RULINGS.md`. Study `course/modules/CS/CS2/` for layout and
grader grammar, and `course/templates/` (`hub.html`, `lesson.html`, `project.html`, `studio.html`, `README.md`). Imitate
structure, not wording.

### 2.1 Carried-over verification lessons (binding)

1. **Numbers from unrounded values.** Every printed number is computed from exact values (`fractions.Fraction`) and rounded only at
   display, with the rule stated. A verifier recomputes from unrounded values (`plans/CS2-build-plan.md` §4.1 rule 1).
2. **Lab statements match code and output.** A hypothesis states only what the printed output shows. An interpretation names only
   what the printed numbers show. A claim that a lab checks something the twin does not check is a FAIL.
3. **Attribute nothing unread.** Only the registry keys in §7 may be cited. Neither Wilson paper has been read by the planner, so
   any claim about their content is an **ungraded naming sentence** ("this page has not read the paper and cites it for no
   result"), as ruling 39 requires for title-only records. Claims about Git, CI services, Python packaging, IEEE 754 or the
   Python `random` module's algorithm are **not stated** unless a lab computes them in this interpreter (see rule 6).
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "same", "exact", "stable", "reproducible",
   "deterministic" are used only where a proof, a finite check or a lab computes the claim (FINAL-ARCHITECT ruling 37 and
   fixer-rules line 9). A claim that a practice "guarantees" reproducibility is banned. The correct claim is what the lab's
   check shows.
5. **Define before use.** Each of the nine concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its owning
   lesson and never before it. Other terms (commit, merge base, golden output, lock file, fixed point of a gate) are defined in
   plain prose with a plain `<dfn>` and no `data-concept`. `tools/check_dag.py` skips a `<dfn>` without `data-concept`.
6. **Facts about tools come from labs.** An IEEE 754 fact, a Python `random` fact or a packaging fact is stated only as what a lab
   prints ("in this interpreter, `0.1 + 0.2` gives `0.30000000000000004`" is a lab fact). Its grade is C with the lab as basis,
   (fixer-rules line 8; FINAL-ARCHITECT ruling 13). A value that appears only in lab output is graded C with the lab named as
   basis. T is allowed only where the page derives the value by hand in a numbered Example.
7. **Grader rules (autograder, §5).** A test demands an exception type only for a condition the page names. Every named condition
   gets its own test, in both directions of the condition (fixer-rules line 19). A failing check never prints the expected value
   (`__tracebackhide__`). The collect-only count is quoted on the page and updated at the end.
8. **Money.** CS4 has no money output. The study's outputs are exact rationals and integers only (§5.2).
9. **No horizontal scroll at 360 px.** Code blocks scroll inside their own container. Repository file trees and long paths wrap.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and no `if __name__ == "__main__":` guard
    (`tools/run_labs.py` runs each twin as `python -I -W error`; `plans/CS2-build-plan.md` §4.1 rule 11).
11. **Standard library only in labs and in the grader.** Labs and the grader use `fractions`, `hashlib`, `json`, `math`, `random`
    (seeded `random.Random(seed)` only), `tomllib`, `ast`, `pathlib`, `dataclasses`, `typing`. No `hypothesis` (B2). No network.
    `pytest` is the only third-party package and is vendored (`tools/vendor_spec.yaml:59`).
12. **Python 3.14** is the target (`tools/vendor_spec.yaml:54`; CS2 Q9 precedent). The code must pass `ruff check` and
    `mypy --strict` at 3.14.
13. **Process words are banned in learner text:** build, builder, round, verifier, REQUESTS, unit report, planner.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a lab or derivation basis.
- Concepts: §1 table. `<dfn>` only for the nine registered concepts, plus plain `<dfn>` for other terms.
- Prerequisite links: `href="../../../concepts.html#<id>"` for CS2, CS3, CS1, M1 and P0.1 concepts. `href="Lnn.html#def-<id>"`
  for earlier CS4 lessons. A lesson never links a concept defined in a later lesson. No link to a CS2 or CS3 page, because those
  pages are not CS4 prerequisites in the build sense; the concept index is the only target (BUILDER_RULES §4.1).
- Labs: code lives once in `tests/labs/CS4/lab-CS4-Lnn-1.py` (and `lab-CS4-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Lab ids match `lab-CS4-<page>-<n>` (`tools/check_pages.py:258-261`).
  No `data-files` attribute on any lab (§6).
- SIMULATED label on every lab or figure that uses generated data: L01 (commit DAG), L03 (generated intervals), L06 (streams), the
  project's study inputs and the project's worked example. The label is visible on the page and in the lab's hypothesis.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`).
- Banned strings (`tools/check_pages.py:58-74`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope", "left as
  an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously",
  "clearly", and any ellipsis `...` outside code.
- The lesson's sections follow BUILDER_RULES §4.2 and `tools/check_pages.py:75` (`LESSON_SECTIONS`: why-it-matters,
  canon-breaks, misconceptions, problems, key-results, quiz, references). Misconceptions: at least three per lesson.
- Hub lesson titles match each lesson's `<h1>` at integration.
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in BUILDER_RULES §10.

### 2.3 Notation (binding; `notation/notation.json`)

| Registered symbol | Registered meaning (locator) | CS4 rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation/notation.json:112`) | Do not use `T` for a test count, a time or a horizon. Use `n` for a count of values, `N` for a count of seeds |
| `\Phi`, `\gamma_3`, `\gamma_4`, `R^\ast`, `R^{e\ast}`, `R_f`, `\mathbb{Q}` | M4 and AP1 symbols | Not used |
| `\R` (macro, `notation/notation.json:25`) | real numbers | Standard, if used |
| `\Var` (macro) | variance operator | Use only for a variance written as an operator; the sample variance formula is written in full (§4 D3) |

Local symbols (defined on the lesson where first used, never redefined): `n` count of values, `s` seed, `x_i` the i-th generated
integer, `\mu` the sample mean (defined locally; the registry lists `\mu` as local), `p` and `q` for the numerator and denominator
of a rational. **NOTATION_REQUESTS: none.** The plan uses only local symbols and the registered `\R` macro.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson:

- **L01 `git-branching-workflow`, `code-review`.** A branch as a named pointer to a commit; a pull request as a proposed merge
  reviewed before it lands; the merge base of two branches as the common ancestor used for a three-way merge. The lab computes merge
  bases on seeded commit DAGs by two methods (walk-the-ancestors, and a breadth-first intersection) and checks equality. Claims
  about Git's storage model are not stated (rule 3). Code review: a review checklist of observable items (tests added, pins
  unchanged, the claim matches the lab). "Where the canon breaks": Git checks no test; a clean merge can change behaviour.
- **L02 `regression-test`.** A regression test pins a behaviour that once failed (or the current output for a fixed input). The
  golden-output test in the lab pins seed 0. "Where the canon breaks": a golden file fixes the current output, including a bug if
  the bug is in it; the lab shows a deliberate change caught, and the lesson does not claim the golden output is correct.
- **L03 `property-based-testing`** (curriculum lab). A property is a statement that must hold for every input in a generated
  class; a generator draws inputs from a seed; a shrinker reduces a failing input to a smaller one that still fails. The lab's
  `merge_intervals` has an edge-case bug (touching intervals are not merged when the second starts exactly at the first's end).
  Three unit tests with hand-picked inputs pass, and the property "the output intervals are disjoint and cover the same points"
  fails on a generated input; the shrunk counterexample is printed. "Where the canon breaks": a property test finds only the
  inputs its generator reaches; the lab says what it reached (count of cases) and nothing more. Misconception: "a passing property
  run proves the property" (corrected by the lab's count of cases).
- **L04 `python-packaging`.** A project as a directory with a `pyproject.toml`; the `[build-system]` table names the backend that
  builds the project; the `[project]` table names it. The lab parses a file with `tomllib` and reports the missing tables. The
  lesson does not state the PEP numbers or the backend's behaviour (not read; REFERENCE_REQUESTS R2). "Where the canon breaks": a
  repository that runs from its working directory can pass every test and still fail to install.
- **L05 `dependency-pinning`.** A lock file records exact versions and, per file, a sha256 digest, so an install can be checked
  against the recorded bytes. The lab checks format and hashes of generated byte strings. "Where the canon breaks": a hash pins
  bytes, not behaviour; a lock file pins what was resolved on one day, not what is correct. The lesson does not claim the lock
  protects against a malicious upstream (not read).
- **L06 `deterministic-computation`.** A seeded generator is a deterministic function of its seed within one interpreter. The lab
  shows: same seed, same stream, twice; the module-level generator's state changes between two calls in the same process.
  "Where the canon breaks": the lab shows identity within one interpreter only. The lesson does not claim identity across
  versions or platforms (not tested here).
- **L07 `bit-for-bit-reproducibility`.** Bit-for-bit reproduction: the output bytes of a rerun equal the output bytes of the first
  run. Floating-point addition is not associative, so the same numbers summed in another order can differ in their bits. The lab
  prints `float.hex` of two sums in two orders and the exact `Fraction` sums. The study uses exact rationals, which removes this
  cause. "Where the canon breaks": bit-for-bit equality is a claim about one build, one interpreter and one operation order.
- **L08 `continuous-integration`.** A CI gate runs a fixed list of commands in a clean environment and fails on the first failing
  command. The lab runs a simulated gate with two inputs and prints the commands run and the exit status. "Where the canon breaks":
  CI shows only what its configured commands check. A green gate is not a proof that the code is correct. The lesson does not
  describe a CI service's syntax (not read).

Lesson-level constraints:
- Each lesson's "Where the canon breaks" names at least one limit and what changes without it.
- Each lesson has a Debate brief only if the curriculum tags one. CS4 has no `debate` key (§0.1), so no lesson has a debate brief.
- The retrieval quiz (8-15 items) per lesson is required; it may test the lab results.

---

## 4. DAG problems (concepts that natural CS4 content would use outside the closure)

Prerequisite closure of CS4 (planner run): **{CS1, CS2, CS3, M1, P0.1}**. Owners below are from `curriculum/curriculum.json`
`concepts` (planner check).

| Ref | Concept | Owner (outside closure) | Where natural CS4 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `ieee-754-floating-point` | M8 (`curriculum/01-foundations.yaml:339`, M8 topo index 38) | L07 bit-for-bit: float addition order | Plain prose; the facts are computed in the lab (rule 6). M8 is **not** added to CS4's prerequisites by default. Adding M8 is acyclic (M8's closure is {AC1, CF1, CS1, E1, FC1, FC2, M1, M2, M3, M4, P0.1}, planner run, and does not contain CS4), but M8 has 110 h (`curriculum/01-foundations.yaml:332`) and would pull that closure into CS4. Architect decision (Q3). |
| D2 | `pseudo-random-number-generator` | M8 | L06: seeded generators | Plain prose ("a seeded generator"); no `<dfn>`; no link. Same decision as D1 (Q3). |
| D3 | `variance`, `quantile-function` (M4) | M4 | the study's sample variance; the sample variance formula in L07 and in the project | Plain formula inline, no `<dfn>`, no link, logged as DAG_DEFECT. Precedent: `plans/CS2-build-plan.md` Issue 2 and its architect decision (Q2). |
| D4 | `replication-package` | CAP1 (later capstone) | the phrase "replication package" for the audit's output | **Avoid the phrase.** Use "the repository" and "the audit log". Using the concept before CAP1 would be a use before introduction (BUILDER_RULES §1.10). |
| D5 | `hypothesis` library (not a concept) | not in Pyodide lock (B2) | the curriculum lab could use the library | Not used. The lab uses a seeded stdlib generator and shrinker (§3 L03). |
| D6 | `threads-vs-processes`, `parallel-rng-streams` (CS6); `timestamp-semantics` (QR1) | CS6, QR1 | parallel test runs in CI; time zones in output | Not used. CS4 runs no parallel job. Wall-clock time appears only as the broken repository's defect D3 (§5.2), in prose ("a timestamp"), without the concept's name. |
| D7 | `welford-algorithm`, `hash-map` (CS2); `data-manifest` (CS3); `unit-test`, `type-hints` (CS1); `replication` (P0.1) | in closure | usable | Usable with links to `../../../concepts.html#<id>`. Not required. |

Each row has a resolution, so no DAG_DEFECT blocks the build **if** the architect accepts the defaults in Q3 and Q4. `tools/check_dag.py`
checks linked uses only; an unlinked use of D1 to D4 passes the tool, so the verifier reads every lesson for these terms
(VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): autograder, ladder, spec, grader design

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` requires the rung order; tier U keeps rungs 1-2 at full length)

1. **Rung 1, worked example** (`lab-CS4-project-1`, SIMULATED). A fully solved, annotated repair of defect D3 (§5.2, wall-clock
   time in the output) on the study module, with a "why" note at each step, and the exact check that shows the repair (the
   study's output bytes are equal across two runs).
2. **Rung 2, completion problem** (`lab-CS4-project-2`, `class="lab completion"`): the seeded generator line of the study with the
   seed mixing removed (`___`). Graded instantly by the lab. Its twin is the completed solution; every page line equals the twin
   line or contains a blank (`tools/run_labs.py` docstring).
3. **Rung 3, independent project** (graded by the autograder, §5.3): the repair of defects D1 to D8 (§5.2) in the repository, the
   tests, and the audit log. `lab-CS4-project-3` is the rung-3 check: it runs the reference study for seed 7 and prints the exact
   output the repository must reproduce.
4. **Rung 4, stretch** (optional, not graded, no ceiling): a second check that the repository reproduces its output under a second
   interpreter version, or a property test of the study's output invariants, with a stated hypothesis.

### 5.2 Spec (`project.html`, `dl.spec`; `tools/check_projects.py:34` requires the terms context, inputs, required outputs,
constraints and grading)

- **Context.** A research group has a study repository that does not reproduce: installs vary, the output changes between runs,
  and the repository has no tests and no CI. Make it reproduce bit for bit, and document every fix in an audit log.
- **Inputs.** The broken repository `repo/` (the starter, §5.4). No external data. The study's inputs are generated from the seed
  by the exact formula in this spec (SIMULATED generated values, labelled on the page):
  `x_i = (1103515245 * s + 12345 * i * i + 7 * i) mod 1000003` for `i = 1, ..., 200`, where `s` is the seed. The planner checked
  (planner run, `python -I`) that the modulus 1000003 is prime and that seeds 0 to 49 give 50 distinct sequences.
- **Broken-repository defect catalogue (fixed for every seed; the same repository for everyone).**
  - D1 `unpinned-requirements`: the test dependency is declared as `pytest>=7`, not pinned.
  - D2 `unhashed-lock`: no lock file records exact versions with sha256 hashes.
  - D3 `wall-clock-in-output`: `run` writes the current time into its output.
  - D4 `input-order-dependence`: `summarize` reports the first value of its input under the key `first`, so the output depends
    on the order of the input.
  - D5 `no-tests`: the repository has no test files.
  - D6 `no-build-system`: `pyproject.toml` has no `[build-system]` table.
  - D7 `no-ci`: no CI workflow runs the test suite.
  - D8 `float-mean`: the mean is computed in floating point and printed as a decimal, so its bits depend on the operation order.
- **Required outputs** (exact names):
  - `repo/study/core.py` (or any module layout under the package `study`) that exposes `run(seed: int) -> str` and
    `summarize(values: Sequence[int]) -> dict[str, object]`.
  - `repo/requirements.lock`: one line per pinned package, `name==version` followed by one or more `--hash=sha256:<64 lowercase hex>`
    items (continuation lines allowed).
  - `repo/pyproject.toml` with `[build-system]` (keys `requires`, `build-backend`) and `[project]` (keys `name`, `version`,
    `requires-python`).
  - `repo/tests/test_*.py`: at least three test functions in total, each named `test_...`.
  - `repo/.github/workflows/ci.yml`: a `run:` step that invokes `pytest`.
  - `repo/AUDIT.md`: one row per defect D1 to D8, each row naming the defect ID, a path that exists in `repo/`, and the fix.
- **Output rules (exact).** `run(seed)` returns the JSON text
  `json.dumps({"count": n, "max": max, "mean": str(mean), "min": min, "variance": str(variance)}, sort_keys=True, indent=2) + "\n"`,
  where `mean = Fraction(sum(x), n)` and `variance = Fraction(n * sum(x*x) - sum(x)**2, n * (n - 1))` (sample variance, divisor
  n - 1). `str(Fraction)` gives the reduced form, and a whole number prints without a denominator. No timestamp, no hostname, no
  environment value appears in the output. Two calls with the same seed return identical text.
- **Named error conditions (the only ones tested).** `run(seed)` raises `ValueError` when `seed < 0`. `summarize(values)` raises
  `ValueError` when `len(values) < 2`. No other exception type is required, and no test requires one.
- **Constraints.**
  - Python 3.14. Standard library and `pytest` only (§2.1 rule 11).
  - No network access; no subprocess; no reading of files outside `repo/`.
  - `requirements.lock` is the only dependency record.
  - Every number in `AUDIT.md` is computed or quoted; the audit log has no numbers except the defect IDs.
- **Grading.** Autograder (`grader/test_project.py`, seeds 0 to 49). The spec's grading entry says "autograder" (this word is
  required by `tools/check_projects.py:38`). No rubric. No exemplars (the curriculum grading is `autograder` only, `curriculum/01-foundations.yaml:511`).
- **Reading list** (`ol.reading-list`, registry keys only): `wilson2014best`, `wilson2017good`. Read both abstracts before
  citing either (§7).

### 5.3 Autograder design (BUILDER_RULES §5.3; the grader lives in `course/modules/CS/CS4/grader/`)

1. **`grader/instance.py`** exposes `make_instance(seed: int) -> dict`. It returns only `int`, `float` or `str` values (B3), with an
   `int` field equal to the seed. It returns the seed's sequence length `n = 200`, the sequence as a comma-separated `str` (the
   first 8 characters differ by seed), and the expected output text as a `str` computed with `Fraction` from the spec formula
   (not from `reference.py`). Deterministic; 50 seeds give 50 materially different sequences (planner check, §5.2).
2. **`grader/reference.py`** is the full reference `study.core` module (the spec's solution). It passes the whole suite on seeds 0
   to 49 (`tools/run_graders.py --unit CS4 --seeds 0-49`, once B1 is decided). The reference repository tree is kept under
   `grader/reference_repo/` (layout pending B1, Q1).
3. **`grader/starter/`** is the broken repository (§5.2, D1 to D8). The suite must fail on it.
4. **`grader/test_project.py`** is a pytest suite, one isolated test per named condition and per property:
   - **T1** `test_lock_pins_every_requirement_exactly`: `requirements.lock` lines match `name==version` with one or more
     `--hash=sha256:<64 hex>` items (D1, D2).
   - **T2** `test_pyproject_declares_build_system_and_project`: `tomllib` parses `pyproject.toml`; `[build-system]` has `requires`
     and `build-backend`; `[project]` has `name`, `version`, `requires-python` (D6).
   - **T3** `test_ci_runs_pytest`: some `.github/workflows/*.yml` has a line that starts with `run:` and contains `pytest` (D7).
   - **T4** `test_tests_exist`: `tests/` has at least one `test_*.py` and at least three `test_` functions in total, found with
     `ast` (D5). The test does not inspect the tests' internals.
   - **T5** `test_run_matches_exact_text_seeds_0_to_49`: `run(s)` equals `make_instance(s)["expected"]` for seeds 0 to 49, byte for
     byte (D3, D8, mutants m03, m08).
   - **T6** `test_two_runs_identical`: `run(s)` called twice in one process gives identical text, for seeds 0 to 49 (D3, D4).
   - **T7** `test_summarize_is_order_invariant`: for seeds 0 to 49, a seeded permutation (`random.Random(s)`) of the values gives
     the same `summarize` result (D4).
   - **T8** `test_sample_variance_hand_example`: `summarize([1, 2, 4])` gives mean `"7/3"`, variance `"7/3"`, min 1, max 4, count 3.
     By hand, the sample variance is 14/3 divided by 2, which is 7/3, and the population variance would be 14/9. The test kills the
     population divisor by equality.
   - **T9** `test_seeds_give_materially_different_sequences`: the 50 sequences for seeds 0 to 49 are pairwise distinct (mutant m06).
   - **T10** `test_summarize_rejects_fewer_than_two_values` and `test_summarize_accepts_two_values`: the named `ValueError` in both
     directions (length 1 raises; length 2 does not).
   - **T11** `test_run_rejects_negative_seed` and `test_run_accepts_seed_zero`: the named `ValueError` in both directions.
   - **T12** `test_audit_log_names_every_defect`: `AUDIT.md` has a line for each of D1 to D8, and each line contains a path that
     exists under `repo/`.
   - **Not a student-facing test (T13):** `run_graders.py` checks that the suite fails on `grader/starter/`. The starter must fail.
   Each test finishes under 5 s in Pyodide; the suite under 60 s (BUILDER_RULES §5.3.4). Feedback names the property violated and
   a concept hint, and never prints the expected value.
5. **Dual mode.** The identical suite runs in the browser (pytest in Pyodide, `QF_SEED` only, `grader.js:95`) and locally
   (`run_graders.py`, `PYTHONHASHSEED=0`). No test depends on either environment setting (B2).
6. **Integrity.** Never claim the tests are secret. Integrity rests on per-seed instances (BUILDER_RULES §5.3.6).

### 5.4 Starter, reference, and the mutant and alternative sets (VERIFIER_RULES §2.6; FINAL-ARCHITECT rulings 9, 10, 19)

**Ten student-error mutants** (`ledgers/CS4/mutants/m01_*` to `m10_*`, each a single-change copy of the reference repository; the
first docstring line names the student error; each must be killed by at least one test on seeds 0 to 9):

| ID | Student error (first docstring line) | Killed by |
|---|---|---|
| m01 | `requirements.lock` pins a range (`pytest>=9`) instead of an exact version | T1 |
| m02 | `requirements.lock` has exact versions but no `--hash` items | T1 |
| m03 | `run` writes a timestamp into its output | T5, T6 |
| m04 | `summarize` reports the first input value under `first` (input-order dependence) | T7 |
| m05 | `pyproject.toml` lacks the `[build-system]` table | T2 |
| m06 | seed mixing uses `s // 2`, so seeds 2k and 2k+1 give identical sequences | T9, T5 |
| m07 | variance divides by `n` (population) instead of `n - 1` | T8, T5 |
| m08 | the mean is computed as a float and printed as a decimal | T5 |
| m09 | the test files are removed, so `tests/` has no test functions | T4 |
| m10 | the CI workflow runs `compileall` and never invokes `pytest` | T3 |

Mutant rules: none of the ten depends on hash randomisation (B2). None is an equivalent mutant, because each changes an output
or a stated file property. If a verifier finds a mutant that the page does not state (for example, a change that only the
starter's formatting exposes), it goes to `ledgers/CS4/equivalent/` with a README proof (ruling 9).

**Five alternative correct implementations** (`ledgers/CS4/alternatives/alt1_*` to `alt5_*`, each a complete repository in a
different style that passes seeds 0 to 49, and that the verifier runs under the same suite):
- **alt1**: a pure function layer, `Fraction` sums in plain loops; the lock file generated with sorted lines; the CI workflow with a
  matrix of one job.
- **alt2**: an exact accumulator class (integer running sums of `x` and `x*x`), with `variance` from the closed form in the spec.
- **alt3**: a two-pass `Fraction` mean, then a second pass for the squared deviations; `pyproject.toml` with a `[project]` table
  first.
- **alt4**: a `dataclass` `Summary` with `from_values` as a classmethod and validation in `__post_init__`; the lock file with hashes
  grouped per package.
- **alt5**: a generator-based pipeline (a `yield` per value), with `AUDIT.md` written as a table whose rows follow the spec's
  order; the CI workflow with two `run:` steps, one of which invokes `pytest`.
All five must pass seeds 0 to 49. A float-based alternative that is wrong on the exact rule (for example, a float mean in the
output) is a mutant, not an alternative (ruling 10).

### 5.5 Hours (`<table id="hours">`, sums to 24; one-line rationale per row; the hours block of `tools/check_projects.py` `check_unit`)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate the D3 repair) | 2 | One solved repair, annotated line by line |
| Rung 2, completion problem (fill the seed-mixing line; run the instant check) | 2 | One blank, one instant check |
| Triage of the repository and the first draft of `AUDIT.md` | 3 | Read every file of `repo/`, list the defects by ID |
| Fixes D1, D2, D6, D7: the lock file, `pyproject.toml`, the CI workflow | 6 | Write each file to its spec format and check it with the lab's parser |
| Fixes D3, D4, D8 and tests T5 to T9 in the study module | 5 | Remove the timestamp, the input-order dependence and the float mean; write the tests |
| Fix D5 and the remaining tests (T4, T10, T11) | 3 | Three named-condition tests, both directions each |
| Audit log completion, final run, reading the failing messages | 3 | One row per defect, each naming a path that exists |
| **Total** | **24** | Equals `data-hours-project` on the hub |

Arithmetic check: 2 + 2 + 3 + 6 + 5 + 3 + 3 = 24; 24 / 80 = 30.0%.

---

## 6. Real-data policy

- **No dataset.** The curriculum names no dataset for CS4 (`curriculum/01-foundations.yaml:501-504`: two sources, one lab
  sentence, one project brief). No `data-files` attribute and no `DATA_REQUESTS` entry is needed.
- **Generated values only.** The labs and the study use generated values, labelled SIMULATED (§2.2). The L07 lab uses deterministic
  arithmetic and is not labelled SIMULATED.
- **No MANIFEST entry, no snapshot, no `tools/data_sources.yaml` change.**
- **Bring-your-own-data is not used.** The project does not need a student file.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in CS4 |
|---|---|---|---|
| `wilson2014best` | `references/references.json:23140` (verified, `used_by: ["CS4"]`) | verified, curriculum source (`yaml:501`) | Reading list (paper level). No content claim until the abstract is read (§2.1 rule 3) |
| `wilson2017good` | `references/references.json:23224` (verified, `used_by: ["CS4"]`) | verified, curriculum source (`yaml:502-503`) | Reading list (paper level). Same rule |

Learning-science keys already in the registry, which CS4 may cite only where a claim about learning needs one (CS2 Q13 precedent):
`dunlosky2013improving` (used by P0.1), `roediger2006test` (P0.2), `sweller1985use` (BLUEPRINT), `kalyuga2003expertise` (AP1, P0.2, S7),
`kirschner2006minimal` (BLUEPRINT), `hmelosilver2007scaffolding` (BLUEPRINT), `freeman2014active` (BLUEPRINT). Their records are at
`references/references.json` (grep by key). Their use in CS4 is optional and is Q9.

**Not used by CS4:** `cormen2022introduction` (CS2's source; not a CS4 source). `harris2020array` (QR3, BLUEPRINT).

### 7.2 REFERENCE_REQUESTS (lead only; the architect runs `tools/add_reference.py`; no bibliographic record typed by the planner)

- {doi: null, authors: "lead only (not typed): the author of the property-based testing paper usually cited for the QuickCheck approach", year: "not typed", title: "lead only: a property-based testing paper (QuickCheck)", venue: "not typed", needed_for: "L03 attribution of the origin of property-based testing, only if the lesson names an origin", confidence: "low; the planner did not identify a record"}
- {doi: null, authors: "lead only (not typed): the Python packaging specification documents that define the [build-system] and [project] tables", year: "not typed", title: "lead only: the Python packaging specifications for pyproject.toml", venue: "primary document; add with an authoritative URL", needed_for: "L04 and T2: only if the lesson makes a claim about the format beyond the lab's parser; otherwise none", confidence: "low; numbers not typed"}
- {doi: null, authors: "not typed", year: "not typed", title: "Git documentation (primary) for the branch and merge-base terms used in L01", venue: "primary document; add with an authoritative URL", needed_for: "L01 only if a claim about Git's behaviour is made; the default is no such claim", confidence: "low"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN or an allow-listed issuer page; BUILDER_RULES §2.4). Until then, the
lessons teach each mechanism by a lab, and no source is attributed to them.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for CS4 (`curriculum/meta.yaml:199-206`; `CURRICULUM.md:164-170`), and the CS4 project has
no `atlas` key (`curriculum/01-foundations.yaml:505-511`). `atlas/` contracts are not needed. The BLUEPRINT sentence that CS4 teaches
the Atlas workflow (`BLUEPRINT.md:266-268`) is prose and does not create a milestone; Q10 asks whether the architect wants the
repository to become an Atlas component later.

---

## 9. Cards builder (Builder F, after A to E)

- `course/modules/CS/CS4/cards.json`, ids `CS4-c001` upward, `lesson` in L01 to L08 (`tools/check_pages.py:366-398` checks the id
  prefix, the lesson names, the grades and the registry keys; every lesson needs at least one card).
- Expected 45-70 cards: one per concept (9), one per key result, and one per misconception (at least 3 per lesson, 24).
- Grade T for a derivation (for example, the merge-base identity or the sample-variance hand example) with `basis` naming the lab or
  Example. Grade C for a lab result, with `basis` naming the lab, for example `"basis": "Lab L07-1 (exact Fraction sums)"`.
  A card cites a registry key only for a claim about a paper, and only after the paper's abstract is read (§7).
- A card and the key-results row it mirrors carry the same grade and basis.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit CS4          # --page L03 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit CS4
.venv/bin/python tools/check_projects.py --unit CS4
.venv/bin/python tools/run_labs.py --unit CS4             # --page L03 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/CS/CS4/L03.html            # per page, after the twin exists
.venv/bin/python tools/embed_labs.py course/modules/CS/CS4/L03.html --refresh lab-CS4-L03-1   # after a twin edit
.venv/bin/ruff check tests/labs/CS4 course/modules/CS/CS4/grader && .venv/bin/ruff format --check tests/labs/CS4
.venv/bin/mypy tests/labs/CS4 course/modules/CS/CS4/grader
```

Verifier only, on a quiet machine, after B1 is decided:
`.venv/bin/python tools/run_graders.py --unit CS4 --seeds 0-49`, `.venv/bin/python tools/mutate_graders.py --unit CS4 --seeds 0-9`,
`.venv/bin/python tools/page_smoke.py --unit CS4`, `.venv/bin/python tools/verify_refs.py --unit CS4`. Not needed: `fetch_data.py`
(no dataset).

Flags are those used by CS2 (`plans/CS2-build-plan.md:362-371`). The planner did not execute any builder command; only the
`coursekit` closure and concept-owner functions and the seed check were run (§0.1, §5.2). `run_graders.py` and `mutate_graders.py`
**will not run correctly for a directory solution** until B1 is decided (§11 item 1).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **Single-file solution (B1, blocking).** `tools/run_graders.py:61` copies one file; `tools/mutate_graders.py:41` globs `*.py`;
   `course/assets/js/grader.js:36-46` and `:94` handle one `.py` file; `tools/check_projects.py:131-134` hard-codes `reference.py` and
   `instance.py`. The CS4 grader needs a directory solution.
2. **No hypothesis (B2).** Absent from the Pyodide lock (planner run, 0 matches) and from `requirements-dev.txt`.
3. **Hash-seed invisibility (B2).** `tools/run_graders.py:73` and `tools/run_labs.py:60` set `PYTHONHASHSEED=0`; `grader.js:95` sets
   only `QF_SEED`. No mutant depends on it.
4. **Fingerprint pitfalls (B3).** `tools/run_graders.py:88-98`: dict values and long string prefixes produce false FAILs.
5. **No subprocess in the browser (NOT VERIFIED IN REPO).** The grader is in-process.
6. **CS1 and CS3 are not built.** `course/modules/CS/` has only CS2. Links to their concepts go to `concepts.html` anchors only.
   CS2 is built, but CS4 links to its concepts through `concepts.html` too (BUILDER_RULES §4.1).
7. **Rung 2 must be graded instantly.** `tools/check_projects.py` accepts a completion lab (`.lab.completion`) or a quiz (its rung 2
   rule at the top of `check_unit`). The plan uses a completion lab.
8. **Eight lessons, nine concepts, and the builder count.** The template's three-lessons-per-builder rule cannot hold (§1). Recorded.
9. **Lesson hours.** `tools/check_pages.py:227-228` (6-12 h) and the hub split (`:335-340`) are satisfied by §0.2.
10. **Python version.** The CS1 source string says 3.13 (`curriculum/01-foundations.yaml:405`); the runtime is 3.14
    (`tools/vendor_spec.yaml:54`). Q8 (CS2 Q9 precedent).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **(BLOCKING, B1) Directory solutions in the grader harness.** Options (a), (b), (c) in §0.3. **RECOMMENDED: (a)**, a directory
   solution (`data-solution="repo/"`) in `run_graders.py`, `mutate_graders.py`, `check_projects.py` and `grader.js`, with a zip
   import and export of the workspace (BLUEPRINT §5.1). Until decided, Builder E does not start.
2. **(BLOCKING for E) Reference and starter layout.** `check_projects.py:131-134` requires `grader/reference.py` and `grader/instance.py`.
   **RECOMMENDED:** `grader/reference.py` holds the reference `study/core.py` module; the full reference tree is `grader/reference_repo/`;
   the starter tree is `grader/starter/`. Follows from Q1(a).
3. **(DAG, D1 and D2) M8 concepts.** `ieee-754-floating-point` and `pseudo-random-number-generator`. **RECOMMENDED:** plain prose,
   no link, no `<dfn>`, facts computed in labs (rule 6). Adding M8 is acyclic but pulls M8's 110 h closure into CS4 (§4 D1).
4. **(DAG, D3) M4 `variance`.** **RECOMMENDED:** the CS2 precedent (plain formula, no `<dfn>`, no link, logged as DAG_DEFECT).
5. **Lesson count and hours.** **RECOMMENDED:** 8 lessons × 7 h and a 24 h project (30.0%). Alternatives within the rules:
   8 × 8 h and a 16 h project (20.0%); 9 × 6 h and a 26 h project (32.5%) with L01 split into two lessons, one per concept.
6. **Ownership deviation.** Builders A to D own two lessons each, E owns the project (§1). **RECOMMENDED:** accept.
7. **Stdlib property checker (B2).** **RECOMMENDED:** a seeded stdlib generator and shrinker in the L03 twin, no `hypothesis`.
8. **Python target.** **RECOMMENDED:** 3.14 (`tools/vendor_spec.yaml:54`), as CS2 Q9.
9. **Learning-science keys.** **RECOMMENDED:** cite a learning-science key only in a claim about learning (retrieval quiz, the project
   ladder's worked-example rung). Keys in §7.1; none required by the curriculum.
10. **Atlas.** **RECOMMENDED:** no Atlas milestone and no contract (§8). The repository may become an Atlas component in a later
    curriculum change.
11. **Typing.** The curriculum's core names typing (`curriculum/01-foundations.yaml:488-490`). **RECOMMENDED:** use the CS1 concept
    `type-hints` (in closure); the lesson L08 gate runs a type checker in its simulated form. No new concept.
12. **Wilson papers.** **RECOMMENDED:** builders read both abstracts before any sentence about them; until then each sentence is an
    ungraded naming sentence (§2.1 rule 3, ruling 39). The architect may instead admit a locator through `tools/add_reference.py`.
13. **Grading mode.** The curriculum grades the project `autograder` (`curriculum/01-foundations.yaml:511`). **RECOMMENDED:** keep
    `autograder`; the audit log is checked by T12 (one row per defect, each naming an existing path). Changing to `both` would be a
    curriculum edit and a rubric with exemplars.
14. **Defect catalogue fixed, not seed-dependent.** **RECOMMENDED:** the same broken repository for every seed; the seed varies the
    study's numbers and sequences (§5.2). A seed-dependent repository would need a browser generator (more tooling).
15. **Study formula.** **RECOMMENDED:** the spec formula in §5.2 (the planner checked 50 distinct sequences for seeds 0 to 49, and that
    1000003 is prime). The builder reruns the check and writes the result into the lab's interpretation only if the lab prints it.

Architect decisions: pending (§12). This plan is the planner's proposal.

---

## 13. After the builders

1. The orchestrator integrates the lessons, the hub and the project. It runs the §10 commands once and fixes cross-lesson defects (DAG,
   links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02, L03-L04, L05-L06, L07-L08 (labs included), then the project
   (grader, mutants, alternatives). Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/CS4.verification.json`, with fragments under `ledgers/CS4/` and verifier scripts under `ledgers/CS4/scripts/`
   (VERIFIER §3). Mutants in `ledgers/CS4/mutants/` (10 rows), alternatives in `ledgers/CS4/alternatives/` (5 rows), and any
   equivalent mutant in `ledgers/CS4/equivalent/` with a README proof (ruling 9).
4. Closing rounds follow the delta rule of FINAL-ARCHITECT ruling 30 and the no-new-mutants rule of ruling 37.
5. The branch merges only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1 must be resolved, or the
   project's gap named, before merge.
