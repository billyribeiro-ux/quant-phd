# CS2 build plan: Algorithms & Data Structures (planner output, 2026-10-28)

Unit: **CS2 · Algorithms & Data Structures** · tier F · 130 h · prerequisites CS1 · no Atlas milestone · grading `both`
(autograder for the streaming statistics library, rubric for the Welford proof and design note) · output directory
`course/modules/CS/CS2/` (part code `CS`). Phase 2 fan-out (BLUEPRINT §9). Owner: orchestrator (architect). Executors:
Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.
Status: planner proposal. Section 2 lists blocking DAG issues that need an architect decision before builders start.
No lesson content is written here. No git operations were run.

Evidence keys used below: `C:<file>:<line>` = curriculum line read; `J:<path>` = `curriculum/curriculum.json` entry read;
`R:<key>` = registry record read in `references/references.json`; `T:<file>:<line>` = tooling line read;
`P:<file>:<line>` = prior plan line read.

## 0. Curriculum facts (read, with locators)

| Fact | Evidence |
|---|---|
| Entry: id CS2, title "Algorithms & Data Structures", tier F, hours 130, prereqs [CS1] | `C:curriculum/01-foundations.yaml:416-420` |
| Core text: complexity, arrays, hash maps, heaps, trees, graphs, sorting, searching, dynamic programming, order-book and event-queue data structures | `C:...:421-424` |
| Thirteen introduced concepts, one per line | `C:...:425-438` |
| Sources: one free-text string, Cormen, Leiserson, Rivest & Stein, 4th ed. (2022) | `C:...:439-440` |
| Lab: "Heap-based event queue vs. a sorted list at scale." | `C:...:441` |
| Project "Streaming statistics library": O(1)-update rolling mean, variance (Welford), min/max (monotonic deque), approximate quantile sketch; prove Welford's update | `C:...:442-447` |
| Project deliverable "Tested library plus proof."; grading `both` | `C:...:448-449` |
| No `debate` key, no `atlas` key on the project | `C:...:416-449` (absent) |
| JSON row mirrors the YAML (hours 130, prereqs [CS1], thirteen concepts with `module: CS2`, sources, lab, grading both) | `J:curriculum/curriculum.json` `parts[2].modules[1]`; `curriculum/curriculum.json` line 6678 (`"id": "CS2"`) |
| No Atlas milestone names CS2; the only CS entry in the atlas list is A1 (module CS1) | `curriculum/meta.yaml:199-201`; no other `module: CS2` in `meta.yaml` |
| CS2 is a listed requirement of STUDIO-CS ("Limit Order Book Matching Engine", requires CS2, CS5) and a prerequisite of CS3-, CS4- and MS1-level modules | `curriculum/01-foundations.yaml:370-372` (STUDIO-CS requires), `:485`, `:514` (prereqs [CS2, CS3], [CS2, CS4]); `curriculum/04-quant.yaml:468` (prereqs [MS1, CS2]); `curriculum/06-profession-capstone.yaml:161`; `CURRICULUM.md:265` (studio title) |
| Prerequisite closure of CS2 = {CS1, P0.1} | computed from `J:` prereqs (CS1 prereqs [P0.1] at `C:...:385-386` in the CS1 block, P0.1 has no prereqs) |
| Topological order: P0.1 (0), M1 (2), CS1 (3), CS2 (7), S0 (9), M4 (12) | `J:topological_order` |
| Hours rules: lesson 6-12 h; hub lessons + project = curriculum hours; project 10-40% | `T:tools/check_pages.py:227-228, 337-340` |
| Lab id must be `lab-CS2-<page>-<n>` and numbered in display order | `T:tools/check_pages.py:258-261` |
| Grading words must match the mode; `both` requires "autograd" and "rubric" in the spec's grading entry | `T:tools/check_projects.py:41-50` |
| Rubric: 4-7 criteria, four levels each, exemplars at two or more levels | `T:tools/check_projects.py:58-75` (`rubric_problems`), applied when grading is `rubric` or `both` at `:138-139` |
| Cards: id `CS2-cNNN`, `lesson` must exist, non-T grade needs `cite` or `basis`, every lesson needs a card | `T:tools/check_pages.py:366-398` |
| No horizontal scroll at 360 px | `T:tools/page_smoke.py:5-12, 343` |

**Hours.** The curriculum's 130 h satisfies every tool rule (see §3). No STOP condition arises.

## 1. The DAG as written (what CS2 may use without definition)

Usable without definition: P0.1 concepts (`J:` P0.1 introduces: evidence-grade, paper-anatomy, identification,
robustness-check, replication, steelmanning, project-ladder, prerequisite-dag, atlas-platform, citation-registry,
notation-conventions) and the twelve CS1 concepts (`C:curriculum/01-foundations.yaml:390-402`): python-function-scope,
python-data-structures, python-class, structural-protocol, type-hints, python-exceptions, python-modules-packages,
numpy-vectorization, pandas-index-alignment, simple-return, log-return, unit-test.

Concepts a CS2 lesson needs that lie **outside** that closure (checked against `J:concepts`):

| Needed in CS2 | Owner | Module topo index | Where it is needed | Status |
|---|---|---|---|---|
| Proof by induction (`mathematical-induction`) | M1 | 2 | Welford correctness (L09), monotonic-deque amortization (L10), DP correctness (L07), AVL height (L05) | **Blocking DAG issue 1** |
| Direct proof, proof by contradiction | M1 | 2 | lower-bound and correctness arguments (L04, L07) | Blocking DAG issue 1 |
| Exponential and logarithm (`exponential-and-logarithm`) | M1 | 2 | \(\log_2 n\) in big-O, binary search, heap height (L01, L03, L04, L05) | Blocking DAG issue 1 |
| Geometric series (`geometric-series`) | M1 | 2 | sums in the complexity proofs (L01) | Blocking DAG issue 1 |
| Variance and standard deviation (`variance`) | M4 | 12 | Welford's mean and variance (L09) | DAG issue 2 |
| Quantile function (`quantile-function`) | M4 | 12 | the quantile sketch's target and rank definition (L11) | DAG issue 2 |
| Limit (`limit`) | M2 | later | not needed if big-O is defined by inequalities with witnesses (Section 4.1 rule) | avoid |
| Limit order book (`limit-order-book`) | FC1 | 26 | the order-book lesson uses only the data structure (`order-book-data-structure`, CS2) | avoid the link |
| Robust statistics (`robust-statistics`) | S0 | 9 | not needed; the quantile sketch is defined from ranks | avoid |

Concepts CS2 introduces are at `J:concepts` with `module: CS2` (all 13 verified present; `big-o-complexity`,
`hash-map`, `binary-heap`, `event-queue`, `balanced-search-tree`, `graph-traversal`, `comparison-sorting`,
`binary-search`, `dynamic-programming`, `order-book-data-structure`, `welford-algorithm`, `monotonic-deque`,
`quantile-sketch`).

Core-text topics with no concept key (arrays, trees as a general notion, graphs as a general notion, sorting as a
general term, searching, FIFO queue, price level, rank): taught in prose, never `<dfn>`, logged in GLOSSARY_REQUESTS
(same precedent as CS1 Q3 and CF1 Q2).

## 2. Blocking issues (architect decision required before L01, L07, L09 builders start)

1. **BLOCKING · M1 is missing from CS2's closure.** The closure is {CS1, P0.1} (computed in §0). CS2 must use proof by
   induction, direct proof, contradiction, logarithms and geometric series. All are M1 concepts
   (`J:concepts`: `mathematical-induction`, `direct-proof`, `proof-by-contradiction`, `exponential-and-logarithm`,
   `geometric-series`; `C:curriculum/01-foundations.yaml:97, 110` for the M1 introduces). Options:
   - (a) **Recommended.** Add `M1` to CS2's `prereqs` in the curriculum (`C:...:420`), then regenerate. Acyclic: M1's
     closure is {P0.1} (`J:` M1 prereqs [P0.1]) and does not contain CS2. Adds M1 to every closure that contains CS2; the architect checks the
     credential maps (`CURRICULUM.md`) after regeneration.
   - (b) Keep the closure. Builders write the proofs in plain words with no `<dfn>` and no link, and every such use
     is logged as a `DAG_DEFECT`. The Welford and comparison-sort proofs would then rest on undefined induction.
     Not recommended.
   The planner cannot edit `curriculum/*.yaml`; this is a request.
2. **DAG issue · M4 terms (`variance`, `quantile-function`).** Outside the closure (topo index 12). Welford's concept is
   "mean and variance" (`C:...:436`), so the lesson necessarily writes the sample-variance formula. Recommended
   resolution, matching the CF1 Q2 decision: the formula is written inline as a formula with its definition in plain
   words, no `<dfn>` and no link, logged as `DAG_DEFECT`. Adding M4 to CS2's prereqs is not recommended: M4's closure
   is {M1, M2, P0.1} (acyclic), but M4 would pull M2 and 120 h into a 130 h unit. Architect decision.
3. **Not blocking, reported.** The hours split satisfies the tool rules (§3). The architect is asked only to confirm it.

## 3. Hours (sums to the curriculum's 130 h)

Lessons 100 h over 11 lessons, each inside 6-12 h (`T:tools/check_pages.py:227-228`). Project 30 h = 23.1% of 130,
inside 10-40% (`T:tools/check_pages.py:339`).

| Lesson | Title (working) | Hours |
|---|---|---|
| L01 | Complexity and arrays | 8 |
| L02 | Hash maps | 9 |
| L03 | Binary heaps and the event queue | 10 |
| L04 | Comparison sorting and binary search | 10 |
| L05 | Balanced search trees | 9 |
| L06 | Graph traversal | 9 |
| L07 | Dynamic programming | 10 |
| L08 | Order books: price levels with FIFO queues | 10 |
| L09 | Welford's online mean and variance | 10 |
| L10 | Monotonic deque for rolling minimum and maximum | 8 |
| L11 | Streaming quantile sketch | 7 |
| **Lessons total** | | **100** |
| Project | Streaming statistics library (`both`) | 30 |
| **Total** | | **130** (= `C:...:419`) |

Hub: `<main data-hours-lessons="100" data-hours-project="30">` (`T:tools/check_pages.py:332-342`).

## 4. Rules for every builder (binding; BUILDER_RULES adapted to CS2)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md` (§1-§10), `BLUEPRINT.md` §3-§8, this file, and
`plans/CS1-build-plan.md` (same part, same foundations-style Python voice). Study `course/modules/M/M1/` (proof-heavy
template, grader and cards), `course/modules/AC/AC4/` (plan only: both-grading, rubric memo, exemplars), and
`course/modules/AC/AC2/` (lab twin naming). Templates: `course/templates/{hub,lesson,project,studio}.html` and
`README.md`. Imitate structure, not wording. 

### 4.1 Campaign lessons (binding; from AC2, AC1, M1, AC4, CF1 verification rounds)

These are the defects the verification campaign actually found. Each one is a rule a builder must follow and a row a
verifier must check.

1. **Numbers recomputed from unrounded values.** Every printed number, in prose or in an expected block, is computed
   from the unrounded value and then rounded for display. A verifier recomputes from the unrounded value, never from a
   printed rounded value (CF1 open items, `P:plans/CF1-open-items.md:53`).
2. **Lab statements match code and output.** The `hypothesis` and `interpretation` paragraphs state only what the
   twin's code and its expected output show. A hypothesis that names a quantity the code does not print is a FAIL.
3. **Attribute nothing unread.** A claim attributed to Cormen or any other source must rest on a locator the builder
   has read. No locator is available to CS2 builders from the registry (the record carries no page or section), so
   textbook content is either proved on the page (grade T) or stated as a basis-backed result (see rule 9), never
   attributed to a locator.
4. **Scope words need a computation.** "O(1)", "amortized O(1)", "all", "every", "never", "always", "exact", "stable"
   each need either a proof on the page or a lab that computes the quantity. "Stable" for Welford is tested by a lab
   that measures error, not asserted (see Section 6).
5. **Define before use.** Every term is defined (or defined in plain words) before its first use in the unit. A
   `<dfn>` is used only for the thirteen concepts in §5, at the lesson that owns them. Each later use links back.
6. **Proposition hypotheses explicit.** Every theorem and proposition states its hypotheses as a numbered list before
   the statement (for example: "Assume \(n \ge 1\), the inputs are finite reals, and arithmetic is exact"). A proof
   that uses a hypothesis not stated is a FAIL.
7. **Grader tests demand an exception type only for conditions the page names.** The spec lists the conditions that
   raise `ValueError` (Section 6.3). A test asserts `ValueError` only for those conditions. For any other invalid input
   the test asserts that the call does not return a wrong answer silently, and it does not name an exception type.
8. **Five alternative correct implementations must pass.** The grader checks properties and numbers (values, rank
   bounds, invariants), never internal state or a specific algorithm. Any correct implementation of the interface
   in Section 6.3 must pass, including an exact sorted-list quantile sketch, a naive two-pass variance that is exact on
   the test instances, a deque with a different internal layout, and two different sketch designs. The builder checks
   this by writing at least five alternative correct solutions as a verifier-facing note; the verifier does the same.
9. **Integer cents for money.** Order-book prices and quantities are `int` (price in integer cents or ticks, quantity
   in integer shares). No `float` in the order-book code path, the price keys, or the reconciliation. Statistics code
   uses `float` only where the curriculum asks for real-valued statistics.
10. **No horizontal scroll at 360 px.** Long code lines wrap or sit in a horizontally scrollable `pre` inside its own
    container, never the page (`T:tools/page_smoke.py:343`). Diagrams are legible at 360 px in light and dark mode.
11. **Labs call `main()` at top level.** Each lab twin ends with a top-level call `main()` (no `if __name__ == "__main__"`
    guard), so the same bytes run identically in Pyodide and under CPython. The twin's `main()` prints only the output
    the expected block records.

Other binding rules (BUILDER_RULES, unchanged): no TODO, TBD, lorem, "for brevity", "left as an exercise" without a
full solution; no filler openers; every number is computed, quoted with a locator, or derived; no external runtime
dependency; no CDN; no edits outside the output directory; no `git commit`, no push; do not run `page_smoke.py`
(verifiers run it on a quiet machine); targeted checks only (§10).

### 4.2 Lesson content rules

- **Big-O is defined by inequalities with witnesses** (\(f \in O(g)\) iff there exist \(c>0\), \(n_0\) with
  \(f(n) \le c\,g(n)\) for all \(n \ge n_0\)). The limit form is not used (M2 concept, outside the closure).
- **Every complexity claim** is either proved on the page (grade T) or computed by a lab that counts operations. Counts,
  not wall-clock times, are the measurement (Section 6.1 and Q3). A claim that an operation is O(1) states the
  operation count it proves.
- **Comparison-sort lower bound (L04)** is proved on the page via the decision-tree argument: hypotheses listed, \(n!\)
  leaves, height at least \(\log_2(n!)\), and the bound \(\log_2(n!) \ge \tfrac{n}{2}\log_2\tfrac{n}{2}\) derived step by
  step (grade T). No source is needed for it.
- **Welford (L09)** is proved by induction on \(n\) (assumptions listed; inductive step shows both the mean and the
  sum of squared deviations update, each algebraic step shown). This depends on Blocking issue 1.
- **Graded claims** carry `data-grade` and `data-cite` only from the registry keys in §8, or `data-basis` naming the lab
  or problem that establishes the result (BUILDER_RULES §7). A non-T grade with neither is a FAIL.
- **Misconceptions (at least three per lesson)** are stated with the wrong belief, the correction and the computation
  or lab that shows it (for example: "hashing is O(1) always" corrected by a lab that counts probes on a colliding
  key set).

## 5. Outline and file ownership (one row per lesson)

Each concept of the thirteen is defined in exactly one lesson (13 = 1+1+2+2+1+1+1+1+1+1+1). The lab twin is the first
lab; the curriculum lab sits in L03 (curriculum lab, `C:...:441`). Lesson pages are `course/modules/CS/CS2/Lnn.html`.

| Lesson | Title (working) | Concepts it defines (from `introduces`) | Lab twin id (`tests/labs/CS2/lab-CS2-Lnn-1.py`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Complexity and arrays | `big-o-complexity` | `lab-CS2-L01-1`: operation counts of a single loop and a nested loop over arrays, with the ratio of counts printed at \(n = 2^k\); the claim is the count growth, not time | 8 | A |
| L02 | Hash maps | `hash-map` | `lab-CS2-L02-1`: chained hash table on a seeded key set; probe counts at several loads; a colliding key set shows the worst case | 9 | A |
| L03 | Binary heaps and the event queue | `binary-heap`, `event-queue` | `lab-CS2-L03-1` (**the curriculum lab**): heap-based event queue versus a sorted list on the same seeded event stream at increasing \(N\); comparison and move counts printed, and the two pop orders checked equal | 10 | A |
| L04 | Comparison sorting and binary search | `comparison-sorting`, `binary-search` | `lab-CS2-L04-1`: comparison counts of insertion sort and merge sort on seeded inputs; binary-search probe counts checked against \(\lfloor \log_2 n\rfloor + 1\) for every \(n \le 1000\) | 10 | B |
| L05 | Balanced search trees | `balanced-search-tree` | `lab-CS2-L05-1`: AVL insert with rotations on seeded keys; the balance invariant and the height bound checked after every insert (variant: Q5) | 9 | B |
| L06 | Graph traversal | `graph-traversal` | `lab-CS2-L06-1`: BFS shortest hop counts checked against a brute-force search on seeded small graphs; DFS discovery and finish order checked against the parenthesis property | 9 | B |
| L07 | Dynamic programming | `dynamic-programming` | `lab-CS2-L07-1`: longest common subsequence and coin change by memoized recursion and by table fill, checked against exhaustive search on small instances; subproblem counts printed | 10 | C |
| L08 | Order books: price levels with FIFO queues | `order-book-data-structure` | `lab-CS2-L08-1`: a book of integer-cent price levels with FIFO queues, fed a seeded message stream; price-time priority checked; best bid and ask checked against a sorted scan | 10 | C |
| L09 | Welford's online mean and variance | `welford-algorithm` | `lab-CS2-L09-1`: Welford against the two-pass mean and variance and a naive sum-of-squares formula, on a stream with a large common offset; error against an exact `fractions.Fraction` reference printed to a stated digit count | 10 | D |
| L10 | Monotonic deque for rolling minimum and maximum | `monotonic-deque` | `lab-CS2-L10-1`: rolling min and max over a seeded series, checked against brute force for every window; total deque operations counted and shown \(\le 2n\) | 8 | D |
| L11 | Streaming quantile sketch | `quantile-sketch` | `lab-CS2-L11-1`: the sketch's rank error against the exact rank on a seeded stream, checked against the stated \(\varepsilon n\) bound for every probe quantile | 7 | D |
| hub | Module hub | none | none | - | A |
| project | Streaming statistics library (`both`) | none | `lab-CS2-project-1..3` (rungs 1-3) | 30 | E |
| grader | `grader/instance.py`, `reference.py`, `starter.py`, `test_project.py` | none | none | - | E |
| cards | `cards.json` from L01-L11 | none | none | - | F (after A-D) |

Ownership: A writes the hub and L01-L03; B writes L04-L06; C writes L07-L08; D writes L09-L11; E writes the project
page and the grader folder; F writes `cards.json` after A-D finish. A builder writes only its own lesson pages and twins.

Ordering check (no later definition is linked): L02 uses big-O (L01); L03 uses big-O and the array notion (prose);
L04 uses heaps (L03) only for heapsort examples and big-O (L01); L05 uses comparisons (L04); L06 uses hash maps (L02)
for adjacency; L07 uses big-O and recursion (prose); L08 uses hash maps (L02), heaps or balanced trees (L03, L05) and
FIFO queues (prose); L09 uses big-O (L01) and the Blocking issue 1 proof tools; L10 uses big-O (L01) and the
amortization argument; L11 uses comparisons and binary search (L04) and the quantile definition (prose, DAG issue 2).

## 6. Project ladder, grader design and rubric (Builder E)

### 6.1 Ladder (`project.html`)

Rung 1 · worked example (`lab-CS2-project-1`, skippable on placement): a fully solved, annotated `RollingMinMax` on a
seeded series of length 12, with a "why" note at each step.
Rung 2 · completion problem (`lab-CS2-project-2`, `class="lab completion"`): the Welford update with the mean and
M2 lines removed (`___`); graded instantly; every line equals the twin or contains a blank.
Rung 3 · independent project: the library `streamstats.py` to the interface in §6.3, the Welford proof write-up, and the
design note. `lab-CS2-project-3` is the rung-3 check.
Rung 4 · stretch (optional, no ceiling, not hour-counted): a weighted or time-decayed Welford accumulator, or a
merge operation for two quantile sketches, with a stated hypothesis.

Tier F keeps rungs 1-2 at full length (BLUEPRINT §4: the minimum applies from tier M upward).

### 6.2 Time budget (table `id="hours"`, one-line rationale per row; sums to 30)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1 worked example | 2 | Read and annotate one rolling-min computation |
| Rung 2 completion | 3 | Fill the Welford update and run the instant check |
| Welford accumulator and its tests | 4 | Implement and check against the exact reference |
| Welford proof write-up | 4 | Induction with every algebra step, stated hypotheses |
| Monotonic-deque min and max with tests | 4 | Implement, check against brute force per window |
| Quantile sketch with rank-error tests | 6 | Design the sketch and prove its \(\varepsilon n\) bound |
| Package API, input validation, property tests | 4 | `ValueError` on the named conditions, invariants |
| Report and self-assessment | 3 | Design note; score against the exemplars |
| **Total** | **30** | equals `data-hours-project` on the hub |

### 6.3 Interface (frozen in the spec, file `streamstats.py`, unit-local, not Atlas)

No Atlas contract exists for CS2 (`J:` no `atlas` key; §7). The spec is the only contract.

- `class WelfordAccumulator`: `update(x: float) -> None`; property `count -> int`; `mean() -> float`;
  `variance(ddof: int = 1) -> float` with `ddof` in {0, 1}. `ValueError` when `mean()` or `variance()` is called before
  any value (`count == 0`), or when `variance(1)` is called with `count < 2`. A NaN input raises `ValueError`.
- `class RollingMinMax(window: int)`: `push(x: float) -> None`; `minimum() -> float`; `maximum() -> float` over the last
  `window` values. `ValueError` when `window < 1`, when a NaN is pushed, or when a query is made before any push.
- `class QuantileSketch(epsilon: float)`: `add(x: float) -> None`; `quantile(q: float) -> float`. `ValueError` when
  `epsilon` is not in (0, 1), when `q` is not in [0, 1], when a NaN is added, or when `quantile` is called on an empty
  sketch. **Guarantee (the only thing tested):** for \(n\) values added, the returned \(v\) satisfies
  \(\#\{x_i < v\} \le qn + \varepsilon n\) and \(\#\{x_i \le v\} \ge qn - \varepsilon n\), using the exact counts on the
  stream.
- Any correct implementation of these classes passes (Section 4.1 rule 8). No test reads a private attribute.

### 6.4 Instances (`grader/instance.py`)

`make_instance(seed: int) -> dict` returns, for each seed, a seeded stream of 20-400 finite floats with a common offset
drawn from the seed (so the naive sum-of-squares formula fails on some seeds), a window in [2, 30], an \(\varepsilon\) in
{0.05, 0.1, 0.2}, and a probe list of quantiles. Every instance is valid. Labelled in the docstring and on the page as
**SIMULATED generated streams; not market data**. Seeds 0-49 give materially different answers (BUILDER_RULES §5.3).
One invalid case per seed, chosen from the named conditions only, is returned under a separate key.

### 6.5 Tests (`grader/test_project.py`)

Properties and numbers only:
- Welford mean and variance against the exact `Fraction` reference to a relative tolerance of \(10^{-9}\) on every seed.
- `variance(0)` and `variance(1)` related by \(n/(n-1)\) exactly, to floating-point tolerance.
- Rolling min and max equal brute force over every window of every seed.
- Sketch rank bound in the §6.3 guarantee for every probe quantile.
- The `ValueError` conditions named in §6.3, one test each. No other exception type is required.
- Reject-invalid tests check that the invalid instance from `make_instance` is refused.
- Each test under 5 s in Pyodide; the suite under 60 s (BUILDER_RULES §5.3.4).

Feedback: a failing test names the property violated and gives a concept hint (for example "variance drifts when the
stream has a large offset: see the update formula"). It never prints the expected answer.

### 6.6 Starter and reference

`grader/starter.py` raises `NotImplementedError` in every method; the suite must fail on it.
`grader/reference.py` is the full solution (`streamstats.py` content). It must pass seeds 0-49
(`run_graders.py --unit CS2 --seeds 0-49`). Excluded from deployment (BLUEPRINT §7).

### 6.7 Mutants the verifier writes (at least three; VERIFIER_RULES §2.6)

Suggested, each must be killed by a test: (1) naive \(\sum x^2 - n\bar x^2\) variance (fails on large-offset seeds);
(2) population variance (`ddof=0`) returned as sample variance; (3) deque that never expires an index, so the window is
off by one; (4) quantile sketch that returns the nearest rank without the \(\varepsilon n\) slack, failing on some seeds;
(5) a hard-coded answer for seed 0. Equivalent mutants (indistinguishable from the reference on all inputs) are proved
and left out of `mutants` (VERIFIER §2.6).

### 6.8 Rubric (the proof and the design note)

`grading: both`, so the rubric path applies (`T:tools/check_projects.py:138-139`). Rubric is 4-7 criteria, each with four
observable levels (no vague descriptor). Proposed criteria, to be finalized by the builder:
1. Hypotheses are listed before the Welford statement, and each is used in the proof.
2. Base case and inductive step are both shown; each algebra step is justified.
3. The variance invariant is stated and carried through the step.
4. Exact arithmetic versus floating point is named, and the claim matches which one the proof assumes.
5. The design note states the sketch guarantee and the probe set it was checked on, and says what it does not cover.
6. The written claims about speed or stability are tied to a lab output (count or measured error), not to a timing.

Exemplars: fully written, at level 4 and level 2, each annotated with the descriptors it meets or misses. Self-assessment
form; the page shows the divergence from the exemplar scores. No question bank (not an adversarial project).

## 7. Atlas and real data

- **Atlas: none.** `curriculum/meta.yaml:199-201` lists A1 for CS1 only; the CS2 project has no `atlas:` key
  (`C:...:442-449`). No `atlas/CS2.contract.md` is needed. The grader panel uses a unit-local file (AP1 and AC4 pattern),
  not `atlas/`. Q4 asks whether the library should later become an Atlas component.
- **Real data: none.** The curriculum names no dataset for CS2 (`C:...:440`). The only cleared embeddable datasets are
  `fx_daily`, `fx_monthly` and `ust_daily` (`P:plans/CS1-build-plan.md`, MANIFEST per `course/assets/data/market/MANIFEST.json`).
  None is needed. Every stream, message log and graph is generated with a seed and labelled **SIMULATED** on the page,
  in each figure source line and in the grader docstring (BLUEPRINT §5.3).
- No `data-files` attribute on any lab. No `DATA_REQUESTS`.
- Bring-your-own-data is not required by the project.

## 8. Registry keys the module may cite

Verified in `references/references.json` on 2026-10-28:

| Key | Record read | Use in CS2 | Caveat |
|---|---|---|---|
| `cormen2022introduction` | Open Library book, status verified, year 2022, MIT Press, ISBN 9780262046305, `used_by: ["CS2"]`, title "Introduction to Algorithms, Fourth Edition", four authors | the curriculum source; cite for textbook exposition only, with no locator | The record has no page, section or table. No number, quotation or locator may be attributed to it. Its curriculum string year (2022) matches the record |
| `dunlosky2013improving` | verified, used_by P0.1 | retrieval-practice statements on the quiz pages, if any | none |
| `roediger2006test` | verified, used_by P0.2 | retrieval practice | none |
| `sweller1985use` | verified, used_by BLUEPRINT | worked examples (rung 1) | none |
| `kalyuga2003expertise` | verified, used_by AP1, P0.2, S7 | expertise reversal (placement skips rungs) | none |
| `kirschner2006minimal`, `hmelosilver2007scaffolding` | verified, used_by BLUEPRINT | project ladder | none |
| `freeman2014active` | verified, used_by BLUEPRINT | labs inline | none |

Keys not used by CS2: `psfndpython`, `ramalho2021fluent` (CS1), `velleman2019prove` (M1). The registry is not
consulted for any other claim.

**REFERENCE_REQUESTS (never typed from memory; architect runs `add_reference.py`; each is a lead, not a source):**

- `{doi: null, authors: "to be looked up (lead from memory: B. P. Welford)", year: null, title: "Welford's online algorithm for the sample mean and variance (the 1962 note in Technometrics)", venue: "to be looked up", needed_for: "L09 provenance of the method. Not needed for the proof, which is on the page (grade T)", confidence: low}`
- `{doi: null, authors: "to be looked up (lead from memory: M. Greenwald, S. Khanna)", year: null, title: "a streaming quantile summary paper (lead: Greenwald and Khanna, 2001)", venue: "to be looked up", needed_for: "L11 only if the builder adopts a published sketch and cites its guarantee. Not needed if the sketch and its bound are proved on the page", confidence: low}`
- `{doi: null, authors: "to be looked up", year: null, title: "a published treatment of the rank-error guarantee of a streaming quantile sketch", venue: "to be looked up", needed_for: "L11 grade-B claim about sketch accuracy, if made", confidence: low}`

Nothing is cited for the order book, heaps, hash tables or graph algorithms beyond Cormen as the curriculum's source.

## 9. Cards builder (Builder F, after A-D)

- `course/modules/CS/CS2/cards.json`; ids `CS2-c001` upward (`T:tools/check_pages.py:381`).
- Every lesson L01-L11 has at least one card (`T:tools/check_pages.py:396-398`). Expected total 50-80 cards: one per
  definition (13), per misconception (at least 3 per lesson, 33), and per key result or lab result.
- Fields: `id`, `lesson`, `front`, `back`, `grade`, and either `cite` (registry keys from §8 only) or `basis` (lab or
  problem name, for example `"basis": "Lab 3 (curriculum lab), counted comparisons"`). A non-T grade needs `cite` or
  `basis` (`T:tools/check_pages.py:392-394`). Proof results are grade T with no `cite`.
- Each back must be checkable against the lesson text. No trivia cards.

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit CS2          # --page L03 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit CS2
.venv/bin/python tools/check_projects.py --unit CS2
.venv/bin/python tools/run_labs.py --unit CS2             # --page L03 for one lesson
.venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49
.venv/bin/python tools/embed_labs.py course/modules/CS/CS2/L03.html   # per page, after the twin exists
.venv/bin/ruff check tests/labs/CS2 course/modules/CS/CS2/grader && .venv/bin/ruff format --check tests/labs/CS2
.venv/bin/mypy tests/labs/CS2 course/modules/CS/CS2/grader
.venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9    # verifier only
.venv/bin/python tools/page_smoke.py --unit CS2                    # verifier only, quiet machine
```

Flags are those cited in `P:plans/M1-build-plan.md` and `P:plans/CS1-build-plan.md` (`check_pages --unit|--all --page`,
`check_projects --unit|--all`, `check_dag --unit|--all`, `run_labs --unit|--all --page`, `run_graders --unit|--all
--seeds`). The planner did not execute any of them; they are not verified against CS2 yet. Mypy targets are a suggestion;
the repo gate is `.venv/bin/mypy` with its strict config. Architect-only, once before merge: `check_pages.py --all`,
`build_site.py --check`, `render_curriculum.py`.

## 11. Tooling assumptions that do not hold, or are unverified, for CS2

1. **M1 concepts are outside the closure** (Blocking issue 1). `check_dag` would reject a link to them; the proofs would
   be plain-word and invisible to the tool, so the verifier must read for them (`T:tools/check_dag.py` docstring).
2. **Timing is not byte-comparable.** The curriculum lab says "at scale" (`C:...:441`). `run_labs` compares expected
   output, so a measured time cannot appear there (CS1 Q4 precedent). The plan uses operation counts.
3. **No Atlas contract, no debate, no data.** `check_projects` Atlas branch and the `check_pages` debate branch
   (`T:tools/check_pages.py:412`) do not apply.
4. **Grading `both` exercises the rubric path** (`T:tools/check_projects.py:138-139`): two exemplars
   at two levels and 4-7 criteria are required.
5. **Pyodide is stdlib-only for CS2.** `heapq`, `bisect`, `collections`, `fractions`, `random`, `math`, `dataclasses` are
   in the Python stdlib. pytest is vendored (`T:tools/vendor_spec.yaml:53-59`). No numpy or pandas is needed.
6. **Python version.** The curriculum's CS1 says Python 3.13 (`C:...:404`); the runtime pin is 3.14
   (`T:tools/vendor_spec.yaml:55`, CS1 Q2). CS2 inherits the open question.
7. **Quantile sketch is unspecified by the curriculum.** The curriculum says "an approximate quantile sketch" (`C:...:445-446`)
   with no algorithm or guarantee. The grader can test only a stated guarantee (Q6).
8. **Cormen has no locator in the registry.** Textbook claims are proved on the page or attributed to the key without
   a locator.

## 12. Open questions for the architect (numbered)

1. **(Blocking) M1 in CS2's prerequisites.** Add `M1` to CS2's `prereqs` (recommended; acyclic, M1 closure {P0.1}), or
   accept plain-word induction, logs and geometric sums with `DAG_DEFECT` entries? Proofs in L01, L04, L07, L09, L10 and
   L05 depend on the answer.
2. **M4 terms (`variance`, `quantile-function`).** Confirm plain formulas with no `<dfn>` and no link, logged as
   `DAG_DEFECT`, as in the CF1 Q2 decision. Adding M4 is not recommended (it pulls M2 and 120 h).
3. **Curriculum lab "at scale".** Confirm the lab reports operation counts (comparisons, moves) and an equality check of
   pop orders, not time. Same decision as CS1 Q4; apply it consistently.
4. **Sketch algorithm and guarantee.** Choose: (a) a deterministic sketch whose \(\varepsilon n\) bound the builder proves
   on the page; or (b) a published sketch, admitted through `add_reference.py` first (REFERENCE_REQUESTS §8). Recommended: (a).
   Without either, L11 has an honest gap and the project's sketch part is unverifiable.
5. **Balanced tree variant.** The curriculum names "balanced search tree" without a variant. Recommended: AVL, because its
   height bound has a short proof on the page (uses M1 induction, Blocking issue 1). Confirm.
6. **Order-book semantics.** Confirm price-time priority, integer-cent prices (`int`, no float), and that the book is
   SIMULATED only (no real order flow). The curriculum's wording is "price levels with FIFO queues" (`C:...:435`).
7. **Lesson count and hours.** Confirm 11 lessons at 100 h and a 30 h project (23%). Alternative: 9 lessons by merging L02
   into L01 and L10 into L09 (keeps each concept assigned once).
8. **Interface freeze.** Confirm §6.3 (three classes, the named `ValueError` conditions, the sketch guarantee) as the spec
   to freeze before Builder E starts.
9. **Python version.** Confirm the teaching target (3.13 per the curriculum, or 3.14 per the runtime), as in CS1 Q2.
10. **Core topics without concept keys** (arrays, sorting as a general term, searching, FIFO, rank, trees and graphs as
    general notions). Confirm prose only with no `<dfn>`, logged in GLOSSARY_REQUESTS (CS1 Q3 precedent).
11. **Cormen attribution.** Confirm that textbook content is either proved on the page or attributed to
    `cormen2022introduction` without a locator (no locator is available in the registry).
12. **Rubric scope.** Confirm the rubric covers the Welford proof and the design note, with no question bank.
13. **Learning-science keys.** Confirm that CS2 pages cite learning-science keys only where a claim needs one (none
    is required by the curriculum for this module).

## Architect decisions (2026-10-28, binding)
Issue 1: M1 added to CS2 prerequisites in the curriculum (done, regenerated). Issue 2/Q2: variance and quantile are plain inline formulas, no dfn, no link. Q3: the curriculum lab reports operation counts, never wall-clock time. Q4: a deterministic quantile sketch with a proof of its error guarantee on the page (no published sketch cited). Q5: AVL. Q6: price-time priority, integer-cent prices, SIMULATED order flow. Q7: 11 lessons / 100 h and a 30 h project. Q8: freeze the interface in plan 6.3 before building. Q9: target Python 3.14 (the repository pin). Remaining questions: follow the plan's recommendation.
