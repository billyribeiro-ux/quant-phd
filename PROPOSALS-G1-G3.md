# PROPOSALS-G1-G3: central edits for benchmark gaps G1 (real data) and G3 (graded written work)

This file lists every change to shared files that the work on branch
`worktree-agent-a2395469a948ee020` needs. None of these edits is committed on
the branch. The gates were run with all of them applied temporarily and then
reverted (section 8). Apply them centrally in the order below.

Committed on the branch (not central):

- **L05 §8, "On market data: thirty trend rules in six currencies"** (sections
  9–14 renumbered from 8–13, and the four in-page "§8" references now read
  "§9"): the excess-return identity (4) of a currency position, and **Lab 6**,
  30 moving-average rules on `fx_daily.csv` tested by the Reality Check, the
  SPA-style test, StepM and the sup-t band from one set of joint
  stationary-bootstrap draws. One quiz item, two key-results rows, a sentence
  in the canon-breaks bullet on block length. `data-hours` 10 → 11.
- **L08 §6, "Both tools on market data"**: **Lab 4**, PBO and DSR (with the
  effective number of trials) on a 40-rule time-series momentum grid on
  `fx_monthly.csv`; Problem **P4** (expected cross-sectional variance of
  dependent trials, with proof); a canon-breaks bullet on spot returns; one
  quiz item; two key-results rows. `data-hours` 7 → 8.
- **project.html**: the integrity memo (rung 3, rubric-graded), Lab 3 (the
  memo's trial set), the brief, `table.rubric` (six criteria × four levels),
  two annotated exemplars (`data-level` 2 and 4), the self-assessment form,
  the extended spec (mode "both") and time budget. `data-hours-project`
  24 → 30.
- **course/assets/js/rubric.js** (new), **site.js** (four lines: load
  rubric.js for `section.rubric-self`), **course.css** and **print.css**
  (additive rules for `.exemplar`, `.annotation`, `.rubric-self`). These are
  design-system files; the additions touch no existing rule, but please check
  them against other branches' edits to the same files.
- **tools/check_projects.py**: `grading_problems()`; mode "both" now requires
  the grading entry to name the autograder and the rubric. Tests in
  `tests/test_page_checks.py`.
- **tests/test_memo_exemplars.py** (new): pins every exemplar number to its
  computation; **tests/js/rubric.test.mjs** (new); **tests/test_labs.py**: the
  two tests that ran the draft twin now run the three real-data labs.
- **tests/labs/S7/draft-realdata-check.py** removed.

## 1. References

No new source was admitted. The two momentum papers the pages cite were
already verified registry entries (used by F3). I ran `add_reference.py` by DOI
so that the registry records S7 as a user; each printed `UPDATED`:

```bash
.venv/bin/python tools/add_reference.py --doi 10.1016/j.jfineco.2011.11.003 --source "Moskowitz, Ooi & Pedersen (2012), JFE 104(2)" --used-by S7
# UPDATED moskowitz2012time used_by=['F3', 'S7']
.venv/bin/python tools/add_reference.py --doi 10.1016/j.jfineco.2019.08.004 --source "Huang, Li, Wang & Zhou (2020), JFE 135(3)" --used-by S7
# UPDATED huang2020time used_by=['F3', 'S7']
```

The resulting `references/references.json` diff is the two `used_by` lists
(plus `generated_at`). `course/assets/data/references.json` does not change.

**What was read, and how each source is used.**

| Key | Read | Use on the pages |
|---|---|---|
| `moskowitz2012time` | Abstract, from OpenAlex (`api.openalex.org/works/doi:10.1016/j.jfineco.2011.11.003`, no email or key sent) | L08 §6: one grade-B claim, `data-locator="Abstract"`: significant time-series momentum in equity index, currency, commodity and bond futures for each of 58 instruments, persistence for 1 to 12 months, partial reversal at longer horizons. Project reading list. |
| `huang2020time` | Title only. Neither OpenAlex nor Crossref holds its abstract, and the OpenAlex search for another version was refused for its shared daily budget; I did not request a key, since that needs an email. | L08 §6: the counter-evidence for the B claim, `data-grade="B" data-locator="Title"`, stating only that the study is titled "Time series momentum: Is it there?". Project reading list. |

`menkhoff2012currency` (Menkhoff, Sarno, Schmeling & Schrimpf 2012) is in the
registry, but no abstract was readable by the allowed routes, so it is not
cited. A verifier with access to the full texts may want to strengthen the
Huang et al. claim beyond its title.

## 2. Curriculum: the S7 entry in `curriculum/01-foundations.yaml`

Applied for the final gate run exactly as follows, on top of integrate-r7 at
12847fd plus 7bcf0e8 (L07 G8), where S7 stands at 92 h. Per the coordinator's
instruction, the module total is for central recomputation: this branch adds
**+8 h** (L05 +1, L08 +1, project +6), so S7 was 100 h in my run.

```diff
@@ -829,7 +829,7 @@ parts:
       - id: S7
         title: "Research Integrity & Multiple Testing"
         tier: M
-        hours: 92
+        hours: 100
         prereqs: [S1, S2, S3]
         core: >-
           Data snooping, the Reality Check, SPA, Romano–Wolf, FDR, the factor-zoo t-stat
@@ -975,13 +975,17 @@ parts:
           - "Howard, Ramdas, McAuliffe & Sekhon (2021), 'Time-Uniform, Nonparametric, Nonasymptotic Confidence Sequences', Annals of Statistics 49(2)"
           - "Johari, Koomen, Pekelis & Walsh (2022), 'Always Valid Inference: Continuous Monitoring of A/B Tests', Operations Research 70(3)"
           - "Ramdas, Grünwald, Vovk & Shafer (2023), 'Game-Theoretic Statistics and Safe Anytime-Valid Inference', Statistical Science 38(4)"
+          - "Moskowitz, Ooi & Pedersen (2012), JFE 104(2)"
+          - "Huang, Li, Wang & Zhou (2020), JFE 135(3)"
         lab: "Random-strategy overfitting engine: in-sample vs. out-of-sample Sharpe."
         project:
           title: "Atlas A8: research-integrity module"
           brief: >-
             Add deflated Sharpe, PBO, Romano–Wolf and BH adjustments to Atlas as one
             integrity report computed from a backtest's full trial set, ready for the
-            backtester (A9) to attach to every result it returns.
-          deliverable: "Atlas at milestone A8."
-          grading: autograder
+            backtester (A9) to attach to every result it returns; then use it to write an
+            integrity memo to an investment committee on a real currency-momentum grid
+            (Federal Reserve H.10 spot rates), graded by rubric against annotated exemplars.
+          deliverable: "Atlas at milestone A8, and the integrity memo."
+          grading: both
           atlas: A8
```

The two source strings are appended at the end of the S7 `sources` list,
wherever that ends after other branches' edits; they are the strings F3 already
uses, so they resolve to the existing keys.

**Concepts.** None new. The pages link only concepts S7 already introduces or
uses: `reality-check`, `superior-predictive-ability` and `stationary-bootstrap`
(L04), `deflated-sharpe-ratio` and `effective-number-of-trials` (L07).
`check_dag.py --all` passes.

**Hours** (the only hour figures this branch proposes, per the coordinator):

| Page | Before | After | Why |
|---|---|---|---|
| L05 `data-hours` | 10 | **11** | §8: the identity (4) with its derivation, and Lab 6 (117 lines of code, a 19-line output, an interpretation) plus a quiz item |
| L08 `data-hours` | 7 | **8** | Lab 4 (112 lines of code, a 14-line output, a long interpretation), Problem P4 with its proof, a canon-breaks bullet and a quiz item |
| project `data-hours-project` | 24 | **30** | the memo: 1 h to rebuild the trial set and run the module on it, 4 h to write, 1 h to self-assess and calibrate (the three new time-budget rows below) |

The project's share in my run was 30/100 = 30%, inside the 10–40% band.

New time-budget rows in `project.html` (committed), with the total:

| Component | Hours | Rationale |
|---|---|---|
| Rebuild the trial set with Lab 3, check its checksums, and run your module on it with `memo/run_memo.py` | 1 | Lab 3's code is given; the hour goes into wiring it to your package and checking that your DSR and PBO match Lesson 8's Lab 4 to the printed digits. |
| Write the integrity memo | 4 | Five fixed sections, 1,200–1,800 words: most of the time goes into the evidence and limitations, because each statistic must be read for what it says and what it does not. |
| Self-assess, score the two exemplars blind, calibrate and revise | 1 | Six criteria for your memo and for each exemplar, then one revision pass on the criteria where your scoring diverged from the official scoring. |
| **Total** | **30** | 24 hours for the module and 6 for the memo; the hub gives the module's split between lessons and project. |

## 3. `render_curriculum.py` output in the final gate run

Copied from the tool's output and from the diff it wrote to `CURRICULUM.md`,
with the edits of section 2 applied on the merged base; none was typed. The
central recomputation supersedes them if other branches change hours too.

```
curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)
```

From `CURRICULUM.md` (before → after):

- Total design hours: 13,707 → **13,715**.
- Master's in Finance / Financial Engineering: 7,658 → **7,666** h (3.55). PhD in Finance: 9,183 → **9,191** h, 4.25 → **4.26** FTE years.
- Financial Econometrics core: 302 → **310**. Tier M: 5,782 → **5,790** h.
- Master's-Equivalent: 11,147 → **11,155** (5.16). Doctoral Candidate: 12,507 → **12,515** (5.79). Doctoral: 13,707 → **13,715** (6.35).
- Quantitative Researcher: 4,068 → **4,076**, 1.88 → **1.89**. Quant Developer: 3,768 → **3,776**, 1.74 → **1.75**. Research doctorate path: 5,638 → **5,646** (2.61).
- S7 line: `M · 92 h` → `M · 100 h`; the project line's grading `autograder` → `both`, with the new brief and deliverable; the two sources appended.

## 4. The S7 hub, `course/modules/S/S7/index.html`

The coordinator recomputes the hub's hours. The non-hour text changes are
proposed here; the hour strings I used for the gate run follow them, for
reference. Each old string occurs once.

**Text (proposed):**

| Old | New |
|---|---|
| `<li><strong>Project:</strong> Atlas A8, autograded</li>` | `<li><strong>Project:</strong> Atlas A8, autograded, and an integrity memo, graded by rubric</li>` |
| L05 card body `…simultaneous bands from the same draws, and control of the k-FWER and of false discovery exceedance.</span>` | `…simultaneous bands from the same draws, control of the k-FWER and of false discovery exceedance, and a rule universe on Federal Reserve exchange-rate data.</span>` |
| L08 card body `Backtest overfitting as a property of selection, PBO, and combinatorially symmetric cross-validation.</span>` | `Backtest overfitting as a property of selection, PBO, combinatorially symmetric cross-validation, and PBO and DSR on a currency momentum grid.</span>` |
| Ladder rung 3 `…DSR, PBO, Romano–Wolf and BH, attached to every backtest result. Autograded on your own seeded instance.</p>` | `…DSR, PBO, Romano–Wolf and BH, attached to every backtest result, autograded on your own seeded instance; then an integrity memo on a real currency momentum grid, graded by rubric against annotated exemplars.</p>` |

**Hours (used in the gate run; recompute centrally):** `92 hours` → `100 hours`
(meta description and eyebrow); `data-hours-lessons="68" data-hours-project="24"`
→ `"70"`, `"30"`; aria-label `68 lesson hours and 24 project hours` → `70 … 30`;
bar widths `74%`/`26%` → `70%`/`30%`; `68 h lessons · 24 h project (26%)` →
`70 h lessons · 30 h project (30%)`; `Eight lessons of seven to ten study hours
each.` → `…seven to eleven…`; card kickers `L05 · 10 h` → `L05 · 11 h`,
`L08 · 7 h` → `L08 · 8 h`.

## 5. New cards for `course/modules/S/S7/cards.json`

Ids to be assigned after S7-c163 (the last id on the merged base). Grade T cards need no citation; the two C
cards name their basis as the key-results tables do.

```json
[
  {"id": "S7-cNEW-1", "lesson": "L05", "front": "What does a currency rule's return computed from spot rates leave out?", "back": "A long position's excess return is \\(r_t + (i^\\ast - i) + i^\\ast r_t\\) (Lesson 5, equation (4)). The spot return \\(r_t\\) omits the carry \\(i^\\ast - i\\), whose bias on a rule's mean can have either sign, the small cross term \\(i^\\ast r_t\\), and every trading cost.", "grade": "T"},
  {"id": "S7-cNEW-2", "lesson": "L05", "front": "On daily H.10 spot rates from 2000-10-17 to 2026-09-30, how many of 30 moving-average rules on six currencies beat cash?", "back": "None, even per rule: the largest t-statistic was 1.105, against 1.645 per rule and 2.837 for StepM's first step. The Reality Check p-value was 0.852, and every 95% sup-t interval contained zero and spanned at least 10.08 percentage points a year. These are spot returns, not tradable excess returns.", "grade": "C", "basis": "Lab 6 (H.10 spot rates, retrieved 2026-10-17)"},
  {"id": "S7-cNEW-3", "lesson": "L08", "front": "What is the expected cross-sectional sample variance of N trials with a common mean, a common variance \\(\\sigma^2\\) and mean pairwise correlation \\(\\bar\\rho\\)?", "back": "\\(\\sigma^2(1 - \\bar\\rho)\\), whatever the correlation matrix; unequal means add their own dispersion (Problem P4). For skill-free trials' Sharpe ratios that is close to \\((1 - \\bar\\rho)/T\\).", "grade": "T"},
  {"id": "S7-cNEW-4", "lesson": "L08", "front": "Lesson 8, Lab 4: what are the DSR of the best of 40 currency momentum rules on H.10 spot rates (2001-02 to 2026-09), and the grid's PBO?", "back": "DSR 0.489 (0.228 with the effective number of trials and variance 1/T) and PBO 0.733 with 16 blocks: what an uninformative selection produces. It is not a 73% chance of losing money.", "grade": "C", "basis": "Lab 4 (H.10 spot rates, retrieved 2026-10-17)"},
  {"id": "S7-cNEW-5", "lesson": "L08", "front": "Why can omitted carry change a PBO computed on spot returns?", "back": "An omitted return that is roughly constant for each trial shifts that trial's column, and adding a constant to a column can change every logit (Problem P2). A PBO on spot returns audits the selection of spot-return rules, not of the strategies a desk would trade.", "grade": "T"}
]
```

## 6. Anything else central

- **BLUEPRINT §9** names the pilot "**S7** (theory + autograder)". With this
  branch S7 is graded in mode both; suggested text: "**S7** (theory, autograder
  and a rubric-graded memo)".
- **benchmarks/S7.md** (reviewer report): G1 and G3 can be marked as addressed
  by L05 Lab 6, L08 Lab 4 and the project memo once the central edits land.
  I left the report untouched.
- **cards for lessons' new quiz items**: the cards above cover the new content;
  no existing card changes.
- **Ledger**: the verifier should re-check L05 §8, L08 §6 and P4, and the
  project's §7 (rubric observability, exemplar annotations against the rubric,
  and the two reference claims of section 1).

## 7. Designs, fixed before the first run

Written in my scratch notes on 2026-10-18 before any FX analysis was run, and
reproduced in each lab's hypothesis: the windows (fx_daily: the whole file;
fx_monthly: from the first month in which all ten currencies have a rate),
the rule grids, the selection metric, the bootstrap (mean block length 10, B =
1,000, block lengths 5 and 20 as checks), S = 16 for PBO with 8 and 10 as
checks, and the memo's integrity call with the A8 defaults. No design was
changed after its results were seen.

## 8. Gate results

Final run on 2026-10-18, on this branch merged with integrate-r7 at 12847fd and
7bcf0e8 (which contain `claude/phase0-foundations-s7-pilot` at 8722a86), with
every edit of sections 1–4 applied and the cards of section 5 not applied. The
central edits were then reverted with `git checkout` on the seven files; the
branch commits none of them. Outputs as printed:

| Gate | Result |
|---|---|
| `ruff check .` | `All checks passed!` |
| `ruff format --check .` | `79 files already formatted` |
| `mypy` (strict) | `Success: no issues found in 75 source files` |
| `pytest` | exit 0, 247 tests, including `test_memo_exemplars.py` (12), the new `test_page_checks.py` cases (8), `test_labs.py`'s real-data lab tests (3 + the embed test), and `tests/js/rubric.test.mjs` (9 Node tests) through `test_js.py` |
| `render_curriculum.py` | `curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)`; a second run left `CURRICULUM.md` and `curriculum.json` byte-identical |
| `build_site.py --check` | `site data current: 6 outputs` |
| `verify_refs.py --offline` | `offline integrity: 548 entries, 0 problems` (no live run: no new source was admitted) |
| `fetch_data.py --check` | `fetch_data: 3 datasets, 0 problems`; nothing under `course/assets/data/market/` changed |
| `check_pages.py --all` | `check_pages S7: PASS` |
| `check_dag.py --all` | `check_dag S7: PASS` |
| `check_projects.py --all` | `check_projects S7: PASS` (with `grading: both`) |
| `run_labs.py --unit S7` | `run_labs S7: PASS (41/41)` |
| `run_graders.py --all --seeds 0-49` | `run_graders S7: PASS (reference 50/50 seeds, slowest 2.7 s)` |
| `mutate_graders.py --all` | `mutate_graders S7: PASS (77/77 killed)` |
| `page_smoke.py --unit S7 --pages L05 L08 project` (both themes, 360 px and desktop, figure sweep, labs in Pyodide, in-browser grader) | `page_smoke S7: PASS`. In Pyodide: L05 Lab 6 2.2 s, L08 Lab 4 2.0 s, project Lab 3 0.1 s; `in-browser grader: All 141 tests pass on seed 301174465. (5.4 s)` |

Locally (CPython), Lab 6 runs in about 1.1 s, Lab 4 in about 1.3 s and the
project's Lab 3 in about 0.2 s.

**The self-assessment form, driven in Chromium.** `page_smoke.py` renders the
form but does not operate it, so a separate Playwright script, not committed,
drove it in both themes at 360 px. It checked that the annotations are hidden
before reveal; that the 18 radio groups render; that Space and an arrow key
score a criterion from the keyboard; that scoring Exemplar A one level high on
C2 yields "matched the official level on 5 of 6" and "higher on C2" and one
highlighted cell; that the annotations show after reveal; that the scores and
the revealed state survive a reload; that "Clear my scores" clears them; that
there is no horizontal scroll and no console error. It passed. Making it a
permanent check would mean extending `page_smoke.py`, which I did not do.
