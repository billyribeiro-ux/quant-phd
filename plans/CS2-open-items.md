# CS2 open items (Builder A: hub and L01-L03)

Owner: Builder A. Scope: `course/modules/CS/CS2/index.html`, `L01.html`, `L02.html`, `L03.html`, and the twins
`tests/labs/CS2/lab-CS2-L01-1.py`, `lab-CS2-L02-1.py`, `lab-CS2-L03-1.py`. Nothing outside those files was written.

## Requests and defects

- DAG_DEFECT · `expectation` and `random-variable` (owner M4, outside the CS2 closure {CS1, M1, P0.1}). Used in
  L02 Assumption 2.1, Proposition 2.2 and Corollary 2.3, where the average search cost is an expected value over
  random bucket assignments. The pages use plain words ("expected value", "probability-weighted sum"), with no
  `<dfn>` and no link. This follows the architect's Q2 precedent for M4 terms. Architect decision needed.
- GLOSSARY_REQUESTS · `array` (L01 §1, defined in prose as a sequence of slots indexed from 0). `simple uniform hashing`
  (L02 Assumption 2.1, defined as a stated assumption on the page; not a registry concept).
- REFERENCE_REQUESTS: none. Only `cormen2022introduction` is cited (hub reading list and the lesson reference
  sections), with no locator and no statement attributed to it.
- DATA_REQUESTS: none. Every stream, key set and event stream is seeded and labelled SIMULATED on its page.
- CONTRACT_CHANGE_REQUESTS: none.
- NOTATION_REQUESTS: none. Only standard KaTeX commands are used (`\lfloor`, `\rfloor`, `\bmod`, `\dots`, `\dfrac`, `\tfrac`).

## Known limitations (state for the verifier)

- Lab counts are in an explicit counting model (comparisons, moves, steps). No time is measured anywhere in L01-L03.
- L02's model values (`1 + (n-1)/(2m)` and `alpha`) are expectations under simple uniform hashing. The lab's hash
  is one fixed multiplicative function and one seeded key set, so the printed gaps are single realizations.
- L03's printed doubling ratios come from one seeded stream per size and are graded C, not growth proofs.
- L03 Proposition 1.6 bounds the sorted-list moves by 2N(N+1). The lab does not print that check; the page
  compares the printed 4378444 at N = 4096 with the bound by hand from the printed value.
- L01 Lab 1's "comparisons at most n" line checks 1000 values; the bound for every n is Proposition 1.6.
- The hub's lesson-hour total and the hub's lesson map depend on L04-L11 (not built by this builder). The hub
  check fails until those pages exist with a declared total of 100 h.
- project.html and cards.json are not written by this builder (Builders E and F).

# CS2 open items (Builder C: L07 and L08)

Owner: Builder C. Scope: `course/modules/CS/CS2/L07.html`, `L08.html`, and the twins
`tests/labs/CS2/lab-CS2-L07-1.py`, `lab-CS2-L08-1.py`. Nothing outside those files was written by this builder.

## Requests and defects

- GLOSSARY_REQUESTS · `multiset` (L07 §2, Definition 2.1, defined in plain words). `FIFO queue`, `price level`,
  `limit order`, `resting order`, `crossing` and `uncrossed` (L08 §1, Definitions 1.1 and 1.2, plain words; `price level`
  and `order-book data structure` are the curriculum's wording only for the latter). `table fill` and `memoized recursion`
  (L07 §1, Definition 1.1, defined inside the dynamic-programming definition). No `<dfn>` on any of these.
- REFERENCE_REQUESTS: none. L07 and L08 cite no registry key. The curriculum's source (Cormen et al.) is not attributed
  to any statement on these pages, and no locator is needed.
- DATA_REQUESTS: none. Every stream and instance is generated from a fixed seed and labelled SIMULATED in the lab text.
- CONTRACT_CHANGE_REQUESTS: none.
- NOTATION_REQUESTS: none. Only standard KaTeX commands are used (`\lfloor`, `\lceil`, `\min`, `\max`, `\infty`).
- DAG_DEFECTS: none new. L07 links `mathematical-induction` and `exponential-and-logarithm` (M1, now a CS2 prerequisite);
  L08 links `hash-map` (L02) and `binary-search` (L04). L08 Proposition 3.2 proves the halving-search bound on the page,
  so L08 does not rely on the L04 proof.

## Known limitations (state for the verifier)

- L07 Lab 1 exhaustive search covers small sizes only (LCS first string of length at most 7, coin amounts at most 12),
  so its agreement is a check on 60 seeded instances, not on all inputs. Theorems 2.2 and 3.3 carry the general claim.
- L07 Lab 1 part C reports one realization (the pair ACGTACG and TGCATGC, and amount 20). The 28, 47, 183, 20736 counts
  are exact for this code but are a single run, graded C.
- L07 Proposition 3.5 states "at most c mn elementary operations for a fixed constant c". The constant is not fixed, so
  the claim is O(mn), not a count.
- L08 Lab 1 part C: queue steps are 7 against 298 orders added, so the bound of Lemma 3.1 is not tested tightly on this
  stream. The lab checks the weaker bound against the orders added; the lesson states the sharper bound of orders rested.
- L08 model: two message types only (limit orders and cancellations), prices on a one-cent grid, no stop, iceberg or
  hidden orders, no latency. Proposition 2.2 is proved for this model; the lab checks one seeded stream against a
  reference, which is a check, not a proof of the code's invariants.
- L08 Lab 1 uses an integer generator (linear congruential), not `random`, so the stream does not depend on the
  random module of any Python version. Both labs are standard library only and run under `python -I -W error`.
- Quiz numeric items use `data-tolerance="0"`; the answers are integers, so an exact match is intended.
- Not yet verified by an independent verifier (VERIFIER_RULES). Cards for L07 and L08 are written by Builder F.

# CS2 open items: Builder D (L09-L11)

Owner: Builder D. Scope: `course/modules/CS/CS2/L09.html`, `L10.html`, `L11.html`, and the twins
`tests/labs/CS2/lab-CS2-L09-1.py`, `lab-CS2-L10-1.py`, `lab-CS2-L11-1.py`. Nothing outside those files was written.

## Requests and defects (Builder D)

- DAG_DEFECT · `variance` (M4, index 12). Used as plain sample and population variance formulas in L09 Definition 1.1,
  Corollary 2.3, problem P3 and quiz item 2. No `<dfn>`, no link (architect decision, issue 2 and Q2).
- DAG_DEFECT · `quantile-function` (M4, index 12). Used as "approximate q-quantile" in L11 Definition 1.2, Theorem 2.5
  and the misconceptions. Plain formula, no `<dfn>`, no link (architect decision, issue 2 and Q2).
- GLOSSARY_REQUESTS · `stream` and `online statistic` (L09 §1); `window`, `rolling minimum`, `rolling maximum`
  (L10 Definition 1.1); `double-ended list` (L10 Definition 2.1, the deque's structure); `amortized cost` (L10, before
  Theorem 2.4); `rank`, `strict rank`, `approximate quantile` (L11 Definitions 1.1 and 1.2); `compaction`, `level`,
  `capacity` (L11 Definition 2.1, sketch terms defined in that lesson). Each is defined in prose on its page.
- REFERENCE_REQUESTS: none. No registry key is cited on L09, L10 or L11, and no statement is attributed to a source.
- DATA_REQUESTS: none. Every stream is seeded and labelled SIMULATED on its page.
- CONTRACT_CHANGE_REQUESTS: none.
- NOTATION_REQUESTS: none. Standard KaTeX commands only (`\sum`, `\lceil`, `\lfloor`, `\varepsilon`, `\texttt`,
  `\Bigl`, `\Bigr`, `\displaystyle`, `\ldots`, `\cdots`). No program macro is used.

## Cross-builder links (verified present)

- L10 links `L01.html#def-big-o-complexity` (Builder A): present in `L01.html`.
- L11 links `L04.html#def-comparison-sorting` and `L04.html#def-binary-search` (Builder B): present in `L04.html`.

## Known limitations (Builder D)

- L09: the floating-point error of Welford's update is measured on one seeded stream at three offsets. It is not bounded
  in general, and the page says so. The statement that the naive formula returns exactly 0.0 at offset 1e9 is a fact
  about this stream only.
- L09 Research R1 (weighted Welford) is labelled as a sketch. Only the second algebra step is checked, on one example.
- L10: the amortized claim is a count of operations over totals, not a timing. The lab measures operation counts only.
- L11: the sketch's guarantee (Theorem 2.5) is proved for every stream. The lab checks nine probe quantiles at two
  epsilons on one seeded stream. The per-level compaction counts in E2 come from a counter added to the same code and
  are not printed by the lab. The memory bound (Corollary 2.6) is not claimed optimal.
- L11: epsilon is an exact Fraction in the lab. The project interface in plan 6.3 uses float epsilon; that interface belongs to Builder E.
- Hours: L09 10 h, L10 8 h, L11 7 h (25 h, the plan's split).

# CS2 open items: Builder E (project page, grader, project labs)

Owner: Builder E. Scope: `course/modules/CS/CS2/project.html`, `course/modules/CS/CS2/grader/` (`reference.py`,
`instance.py`, `starter.py`, `test_project.py`), and the twins `tests/labs/CS2/lab-CS2-project-1.py`, `-2.py`, `-3.py`.
Nothing outside those files was written. No ledger was written (see the first request below).

## Requests and defects

- PROCESS_CONFLICT · The task asked for the ten student-error mutants to be written into `ledgers/CS2/mutants/`. The
  plan (section 4, section 6.7) and BUILDER_RULES state that a builder never writes a ledger, and that mutants are the
  verifier's output (VERIFIER_RULES section 2.6). The ten mutants are therefore kept outside the repository, in
  `/tmp/cs2-scratch/mut/` (single-change copies of `reference.py`, each with a one-line docstring). Each is killed by
  the suite on seeds 0 to 9. `tools/mutate_graders.py --unit CS2` was not run, because it reads `ledgers/CS2/mutants`.
  Architect decision: confirm the verifier writes the mutants, or authorise the builder to place them.
- VERIFIER_NOTE · The five alternative correct implementations are kept in `/tmp/cs2-scratch/alt/` (the note the plan
  asks for, as code): (1) exact stored list, two-pass mean and variance, brute-force rolling, nearest-rank sketch;
  (2) Welford with the (n-1)/n delta-squared form, a two-list monotonic deque, and a Greenwald-Khanna-style sketch
  compressed every five inserts; (3) exact `Fraction` sums, brute-force rolling, exact list with the slack; (4) shifted
  data sums (shift by the first value), with the reference deque and sketch; (5) the reference Welford and rolling
  classes with an exact-list sketch. All five pass the 112 checks on seeds 0 to 9 (and on seeds 0 to 49 for the
  reference).
- GLOSSARY_REQUESTS · `rank guarantee` (project page, Conventions: the two inequalities on the counts below and at or
  below the answer), `probe quantile` (Inputs: the ten quantiles at which the suite checks the guarantee), `exact
  counts` (Conventions: rational arithmetic on the floats of the stream). Plain words on the page; no `<dfn>`.
- REFERENCE_REQUESTS: none. The reading list cites `cormen2022introduction` with no locator, and says so on the page.
- DATA_REQUESTS: none. Every stream is generated from the seed by `grader/instance.py` and labelled SIMULATED.
- CONTRACT_CHANGE_REQUESTS: none. No Atlas milestone.
- DAG_DEFECTS: none new. `variance` and `quantile` appear as plain formulas and plain words (architect decision Q2).
  The project links `mathematical-induction` (M1, now a CS2 prerequisite) and the concepts of L09, L10 and L11.

## Known limitations (state for the verifier)

- Test count: `pytest --collect-only` gives 112 checks for every seed (checked on seeds 0, 13 and 49 before the final
  edits, and on the final files for seed 0). The page quotes 112. Re-count after any edit to `test_project.py`.
- Welford tolerance: the offsets are 0, 10,000 and 1,000,000. In a scratch sweep of 200 streams at offset 1,000,000 the
  reference's worst relative error was 3.4e-11, and the naive sum-of-squares formula fails on the large-offset seeds. The
  instance docstring says so without quoting these figures.
- The sketch is the Greenwald-Khanna-style design in `reference.py`, with the invariant `g + delta <= floor(2 epsilon n) + 1`
  and the query `target = max(1, ceil(q n - epsilon n))`. The page states the guarantee and does not prove it: the proof
  of the sketch's guarantee is the student's work in the design note, and the exemplar does not claim one. Memory is
  not bounded by the specification, and the suite does not test it.
- Infinite values and non-real values are outside the domain. The suite checks them only by the refuse-or-correct rule
  (an exception of any type, or the correct answer, or for infinities a non-finite result). Memory and merge are not tested.
- The in-browser Pyodide run was not executed by this builder. `run_graders.py` ran the suite with local CPython only,
  under the same flags as the browser (`--assert=plain -W error`).
- `page_smoke.py` results are reported in the builder's final message, not here.
- `check_pages.py --unit CS2` fails only on `cards.json`, which is Builder F's file. The lesson pages and the hub were
  not edited by this builder.

## Builder B: lessons L04-L06 (owner B)

Scope: `course/modules/CS/CS2/L04.html`, `L05.html`, `L06.html`, and the twins `tests/labs/CS2/lab-CS2-L04-1.py`,
`lab-CS2-L05-1.py`, `lab-CS2-L06-1.py`. Nothing else was written by Builder B.

- GLOSSARY_REQUESTS (prose without a concept key, as in the CS1 Q3 precedent): graph, vertex, edge, path, simple
  path, walk, hop count, adjacency list, FIFO queue (L06); binary tree, binary search tree, height, in-order sequence,
  balance factor, rotation (L05); decision tree, leaf, probe, gap (L04). Each is defined in the lesson that first uses it.
- NOTATION_REQUESTS: \(\varphi = (1 + \sqrt{5})/2\), the golden ratio, in L05 Proposition 2.4 and its proof. The local
  symbols \(\mathrm{dist}\), \(\delta\), \(\beta\), \(N(h)\) and \(M(h)\) are defined in place (L06 Definition 1.1, L04
  Proposition 3.2, L05 Definition 2.2 and Lemma 2.3).
- DAG_DEFECTS: none. L04 and L05 use M1's `mathematical-induction` and `exponential-and-logarithm` through the
  prerequisite now in CS2's closure (architect decision 1). No DAG_DEFECT is logged for these.
- REFERENCE_REQUESTS: none. No claim in L04-L06 is attributed to `cormen2022introduction`; the registry record has no
  locator, so the pages name it only as the unit's listed textbook.
- Known limitations (to carry into the verifier's ledger):
  - L05 Remark 3.2: the AVL rule after each insertion is checked on one seeded run of 500 keys, not proved. Deletion is
    not covered. This is an honest gap, not a graded result (the key-results row reads "not graded").
  - L04 Part D checks the unsuccessful-search worst case only (Proposition 3.2); the successful search is not claimed.
  - L06: weighted shortest paths and directed-graph DFS classification are not covered (Section 4 says so).
  - No time is measured in any L04-L06 lab (architect decision Q3); every count is a count of comparisons, rotation
    calls, enqueues or inspections.
  - Each quiz names `cards.json`, which Builder F writes after A-D. Until then the cards check reports the file missing.
- Checks run by Builder B (targeted): `check_pages --unit CS2 --page L04|L05|L06` PASS; `check_dag --unit CS2` PASS (the
  whole unit at the time of the run); `run_labs --unit CS2 --page L04|L05|L06` PASS (1/1 each);
  `pytest tests/test_labs.py -k CS2` PASS; `ruff check` and `mypy --no-incremental` PASS on the three twins;
  `page_smoke --unit CS2 --pages L04 L05 L06` PASS (the last gate, run alone).
- Not run by Builder B: `check_projects`, `run_graders`, `mutate_graders` (Builder E); the cards check (Builder F).
