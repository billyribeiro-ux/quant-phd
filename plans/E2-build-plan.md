# E2 build plan: Game Theory & Information Economics (2026-10-28)

Unit: **E2 · Game Theory & Information Economics** · tier U · 110 h · prerequisites E1, M4 · no Atlas milestone · no debate ·
grading `both` (autograder + rubric) · output directory `course/modules/E/E2/` (part code `E`) · lab twins `tests/labs/E2/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders, then independent
Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Anything not in the
curriculum is marked **NOT IN CURRICULUM**. Planner-derived closed forms in §5.3 and §6 are hand derivations to be
re-derived by the builder and re-checked by the verifier; they are not sourced. The planner did not run any tool command
and did not read any full-text paper (see §10 Q9).

---

## 0. Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part E, code `E`, title "Economics"; STUDIO-E requires E6, E7 (not E2) | `curriculum/02-economics-finance-core.yaml:4-8` |
| E2 id, title "Game Theory & Information Economics" | `curriculum/02-economics-finance-core.yaml:50-51` |
| Tier `U`, hours `110` | `curriculum/02-economics-finance-core.yaml:52-53` |
| Prereqs `[E1, M4]` | `curriculum/02-economics-finance-core.yaml:54` |
| Core: "Nash and Bayesian-Nash equilibrium, adverse selection, signaling, screening, moral hazard, mechanism design, auctions." | `curriculum/02-economics-finance-core.yaml:55-57` |
| `introduces` has 12 concepts (listed in §3) | `curriculum/02-economics-finance-core.yaml:58-70` |
| Sources: eight free-text strings (Nash 1950; Akerlof 1970; Spence 1973; Rothschild & Stiglitz 1976; Holmström 1979; Vickrey 1961; Milgrom & Weber 1982; Fudenberg & Tirole 1991) | `curriculum/02-economics-finance-core.yaml:71-79` |
| Lab: "Winner's curse in a common-value auction." (one lab) | `curriculum/02-economics-finance-core.yaml:80` |
| Project "Treasury auction design"; brief: "Simulate uniform-price vs. discriminatory auctions with strategic bidders and compare revenue, bid shading and allocative efficiency."; deliverable "Simulator plus a design memo."; grading `both` | `curriculum/02-economics-finance-core.yaml:81-87` |
| No `debate:` key on E2 (the three debate keys in the file are at lines 270, 311, 460, in other modules) | `curriculum/02-economics-finance-core.yaml:50-87` (absent); `:270`, `:311`, `:460` |
| No `atlas:` key on E2 or its project; no atlas entry names E2 | `curriculum/02-economics-finance-core.yaml:50-87`; `curriculum/curriculum.json` `atlas` list (no `module: "E2"`); `curriculum/meta.yaml` atlas block |
| JSON row for E2 matches the YAML (hours 110, prereqs E1 and M4, 12 concepts, eight sources, lab, project, grading both) | `curriculum/curriculum.json:7375` (`"id": "E2"`) |
| All 12 concepts map to module E2 in the `concepts` dict | `curriculum/curriculum.json` `concepts` (planner check: 12 owners = E2) |
| Dependents of E2: E4 and CF3 (`prereqs` contain E2) | `curriculum/curriculum.json` `parts` modules (planner check) |
| E2 precedes E1 in build order at index 23; E1 at 16, M4 at 12, M2 at 5 | `curriculum/curriculum.json` `topological_order` (planner check) |
| Rendered row | `CURRICULUM.md:373` (`E2 · Game Theory & Information Economics · U · 110 h ← E1, M4`) |
| M4 (prereq): tier F, 120 h, prereqs [M2], 18 introduces including `expectation`, `independence`, `quantile-function`, `conditional-expectation-elementary`, `law-of-large-numbers` | `curriculum/01-foundations.yaml:190` (`- id: M4`); `curriculum/curriculum.json` row at `:6423` |
| E1 (prereq): 13 concepts, Cournot, Bertrand, monopoly, `competitive-equilibrium`, `pareto-efficiency`, `economic-surplus`, `utility-maximization` | `curriculum/02-economics-finance-core.yaml:18-47`; `curriculum/curriculum.json` row at `:7339` |
| M2 introduces `envelope-theorem`, `derivative`, `partial-derivative`, `hessian`, `implicit-function-theorem` | `curriculum/curriculum.json` row for M2 (planner read) |

### 0.1 Prerequisite closure (computed)

`coursekit.prerequisite_closure("E2")` run by the planner returned **{E1, M4, P0.1, M2, M1}** (`tools/coursekit.py`).
Concepts usable without definition or with a concept link: those introduced by E1 (13), M4 (18), M2 (13), M1 (14) and
P0.1 (11). The concept links allowed by `check_dag.py` are exactly these owners (`tools/check_dag.py` lines 1-20, 53-60).

Concepts that natural E2 content would use and that lie **outside** the closure (see §13): `bayesian-inference` (S1),
`expected-utility` (E3), `arrow-pratt-risk-aversion` (E3), `lagrange-multiplier`, `kkt-conditions`, `convex-set`,
`convex-function`, `principle-of-optimality` (M7), `first-welfare-theorem` and `arrow-debreu-equilibrium` (E4),
`risk-neutral-probability` (FC2).

Concepts inside the closure that E2 should link where it uses them: `competitive-equilibrium`, `monopoly`,
`cournot-competition`, `bertrand-competition`, `economic-surplus`, `deadweight-loss`, `pareto-efficiency`,
`utility-maximization` (E1); `expectation`, `independence`, `quantile-function`, `conditional-expectation-elementary`,
`law-of-large-numbers` (M4); `envelope-theorem`, `derivative`, `hessian` (M2); `present-value` (M1).

---

## 1. Feasibility of the hours (no conflict; no STOP condition)

The curriculum figure is 110 h (`curriculum/02-economics-finance-core.yaml:53`). The tool rules are:

- each lesson `data-hours` 6-12 (`tools/check_pages.py` line 227-228 region; the check is `if declared and not 6 <= declared <= 12`);
- hub `data-hours-lessons + data-hours-project = 110` (`tools/check_pages.py` lines 336-338: `abs(lessons_h + project_h - u.hours) > 1e-9`);
- project share 10-40% of 110, i.e. 11 to 44 h (`tools/check_pages.py` line 339: `0.10 <= project_h / u.hours <= 0.40`);
- lessons sum to the hub's lessons figure (`tools/check_pages.py` lines 341-342).

Chosen split: **9 lessons × 10 h = 90 h; project 20 h (18.2%)**. Satisfies every rule above. The hours are feasible, so
this plan raises no STOP condition. The split is an open question (§10 Q1).

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to E2)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `VERIFIER_RULES.md` §2 (what will be checked),
`plans/E1-build-plan.md` (its Architect decisions are binding precedent here), `plans/M1-build-plan.md`,
`plans/CF1-build-plan.md`, `plans/AC4-build-plan.md` (their Architect decisions are precedent), this file. Study
`course/modules/M/M1/` (hub, lesson, project, grader panel) and `course/modules/CF/CF1/` for layout. Imitate structure, not
wording. `course/templates/` holds the four skeletons (`hub.html`, `lesson.html`, `project.html`, `studio.html`).

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and
   rounded only at display. A page that shows a rounded figure says which rounding it uses. Precedent: AC4 KNOWN
   LIMITATION 3; CF1 L01 Remark 5.2; E1 plan §2.1 item 1.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints; the interpretation names only
   what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS (a "checked directly" phrase with no lab behind it).
3. **Attribute nothing unread.** Only the eight keys in §8 may be cited, and no locator, page, table, equation or number is
   typed from memory. A result from a source without a confirmed locator is either a derivation on the page (grade T) or
   is cited to the key at the book or paper level with no locator. Precedent: AC2, AC4 §0, E1 §2.1 item 3.
4. **Scope words need a computation.** "every", "all", "never", "always", "any", "unique", "the equilibrium", "optimal",
   "efficient", "revenue-maximizing" are used only where a proof, a finite enumeration, or a lab computes the claim. A
   finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06, E1 §2.2). Precedent: E1 §2.1 item 4.
5. **Define before use.** Each of the 12 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson and never before it (`tools/check_dag.py` enforces definition counts and link order). A lesson uses a concept
   only after the lesson that defines it. Unlinked uses are checked by the verifier (VERIFIER §2.9).
6. **Every proposition states its hypotheses.** Every Theorem, Proposition and Lemma block lists numbered **Assumptions**
   before the statement (for example: Assumption 1, bidders are risk neutral; Assumption 2, values are independent and
   drawn from the stated distribution). A grade T claim names every assumption it uses. Precedent: E1 §2.1 item 6.
7. **Grader tests demand an exception type only for conditions the page names.** The spec lists the invalid-input conditions
   and the exception type for each (§5.4). Any other invalid input may raise any exception or return. **Five alternative
   correct implementations must pass** the suite (§6). Precedent: E1 §2.1 item 7.
8. **Integer cents for money.** Every money output of the engine (bids, payments, revenue, surplus, efficiency totals) is an
   `int` in cents, computed from exact `Fraction`s and rounded once, half up, by the rule stated on the project page. No
   float money, no tolerance on money. Precedent: E1 Q6 and AC4 Q9/Q10.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; no element forces the page wider than 360 px. The verifier checks this with `page_smoke.py`.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `tools/run_labs.py` runs each twin as `python -I -W error <twin>` with no network
    (`tools/run_labs.py` line 55). The M1 twin `tests/labs/M1/lab-M1-L04-1.py` ends with `main()`.
11. **Lab ids and numbering.** Lab ids are `lab-E2-<page>-<n>` (`tools/check_pages.py`: `lab-{u.id}-{page.name}-\d+`, and
    `n` equals the lab's display position). Project labs are `lab-E2-project-<n>`.
12. **Notation.** Use only the macros registered in `notation/notation.json` (§2.3). A registered symbol never takes another
    meaning.
13. **Process words stay out of learner text.** No "builder", "verifier", "round", "REQUESTS", "unit report" in pages or
    code comments (precedent: E1 §2.2, M1 defect "Convention (project Q5)").

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation (`data-grade`,
  `data-cite`, `data-locator` as in BUILDER_RULES §2.1).
- Concepts: §3 table; `<dfn data-concept>` only for the 12 registered concepts. Terms outside the 12 may appear in prose
  and, if emphasised, as plain `<dfn>` without `data-concept`. `tools/check_dag.py` skips a `<dfn>` with no `data-concept`
  (`tools/check_dag.py` `if not concept: continue`, which is the planner's read of the loop at its line 47-48).
- Prerequisite links: `href="../../../concepts.html#<id>"` for E1, M4, M2, M1 and P0.1 concepts; `href="Lnn.html#def-<id>"`
  for earlier E2 lessons. A lesson never links a concept defined in a later lesson.
- Labs: code lives once, in `tests/labs/E2/lab-E2-Lnn-1.py` (and `lab-E2-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output by hand. Standard library only
  (`fractions`, `itertools`, `math`, `random` with `random.Random(seed)`). No network. Under 10 s in Pyodide. No warnings
  (`-W error`).
- SIMULATED label: only for simulated data (BUILDER_RULES §1.7). Exact enumerations and exact closed-form checks are not
  labelled SIMULATED. Seeded simulations (L08 lab, the project's generated cases) are labelled SIMULATED on the page and in
  the docstring.
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `notation/notation.json`). Request changes; do not write them.
- Banned strings (`tools/check_pages.py` lines 58-72): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is
  well known", "obviously", "clearly", and the three-dot ellipsis `...` (the regex has no exemption for code; avoid it
  everywhere until the verifier confirms code blocks are skipped).
- Percent changes state the base and the direction.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES
  §10 output contract.

### 2.3 Notation conflicts foreseen (`notation/notation.json`)

| Registered symbol or macro | Registered meaning (read) | Risk in E2 | Rule for builders |
|---|---|---|---|
| `T` (symbol row 1) | number of return observations in a sample (module S1) | "T" is the common letter for a type space or a time horizon in games | Use \(\Theta\) or \(\theta_i\) for types and \(t\) for time. Never `T` for a type set or a period count |
| `\Phi`, `\Phi^{-1}` (row 2) | standard normal CDF and its inverse (M4) | a normal signal model in the winner's-curse lab may tempt a generic CDF | Use `\Phi` only for the standard normal CDF. A generic distribution function is `F` with its distribution named in the lesson |
| `\N` (macro) | natural numbers | "N" for the number of bidders or players | Write the count as \(n\) (bidders) or \(I\) (players), defined locally. Never `\N` for a count |
| `\E`, `\Var`, `\Cov`, `\Prob`, `\indic` (macros) | expectation, variance, covariance, probability, indicator | a hand-written \(\mathbb{E}\) or \(P\) would not match the macro | Use the macros only |
| `\Normal` (macro) | normal distribution | use in signal models | Use `\Normal(\mu,\sigma^2)` only, never a hand-written \(\mathcal{N}\) |
| `\emgamma` (macro) | Euler–Mascheroni constant; plain gamma is left free | not used in E2 | Do not write \(\gamma\) for anything E2 defines unless it is local and stated |
| `\gamma_3`, `\gamma_4`, `R^\ast`, `R_f`, `\mathbb{Q}`, `\SR` and the other registered AP1, S1, S7 symbols | defined elsewhere | none expected | Do not use them with another meaning |

Payoffs: write \(u_i\) for bidder or player utility and \(\pi_i\) only if the lesson defines it locally. Bids \(b_i\), values
\(v_i\), types \(\theta_i\), reserve price \(r\), units \(k\) are local letters, defined in the lesson where first used
(BLUEPRINT §3 notation convention; `notation.json` `about`).

---

## 3. Outline and file ownership (proposed by this plan; the architect confirms in §10)

Lessons: 9 × 10 h = 90 h. Concepts: 12, each in exactly one row. Concept counts per row sum to 1+1+1+1+1+1+2+3+1 = 12.
Order follows the curriculum's `introduces` order (`curriculum/02-economics-finance-core.yaml:59-70`), regrouped so each
concept is defined after the concepts it depends on.

| Lesson | Title (working) | Concepts it defines (`introduces`, yaml 59-70) | Lab (twin id, `tests/labs/E2/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Strategic form and Nash equilibrium | `nash-equilibrium` (yaml 59) | `lab-E2-L01-1`: pure-strategy equilibria of finite two-player games by exhaustive best-response check; printed equilibrium set | 10 | Builder A |
| L02 | Bayesian games and Bayesian–Nash equilibrium | `bayesian-nash-equilibrium` (yaml 60) | `lab-E2-L02-1`: single-unit first-price auction, symmetric bid \((n-1)/n\cdot v\) checked by a grid best-response (§5.3) | 10 | Builder A |
| L03 | Adverse selection | `adverse-selection` (yaml 61) | `lab-E2-L03-1`: two-type market with unobserved quality; pooling versus separating prices, exact | 10 | Builder A |
| L04 | Signaling | `signaling` (yaml 62) | `lab-E2-L04-1`: two-type education-signaling separating equilibrium; incentive constraints checked exactly | 10 | Builder B |
| L05 | Screening | `screening` (yaml 63) | `lab-E2-L05-1`: two-type menu of contracts with incentive and participation constraints; information rent | 10 | Builder B |
| L06 | Moral hazard | `moral-hazard` (yaml 64) | `lab-E2-L06-1`: two-action effort problem, linear contract, incentive and participation constraints, optimal slope on an exact grid | 10 | Builder B |
| L07 | Mechanism design and the revelation principle | `mechanism-design`, `revelation-principle` (yaml 65-66) | `lab-E2-L07-1`: finite-type direct mechanism; every misreport enumerated, incentive compatibility checked | 10 | Builder C |
| L08 | Common-value auctions, the winner's curse and bid shading | `common-value-auction`, `winners-curse`, `bid-shading` (yaml 67-69) | `lab-E2-L08-1` (**the curriculum lab**, yaml 80): winner's curse in a common-value auction; seeded simulation, SIMULATED | 10 | Builder C |
| L09 | Uniform-price versus discriminatory auctions | `uniform-vs-discriminatory-auction` (yaml 70) | `lab-E2-L09-1`: k-unit payments under both formats on fixed bid profiles, revenue and efficiency in exact cents | 10 | Builder C |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 90/20 | none | none | - | Builder A |
| project | Treasury auction design (`both`, §5) | none | `lab-E2-project-1` (rung 1), `lab-E2-project-2` (rung 2, `class="lab completion"`), `lab-E2-project-3` (rung 3 check) | 20 | Builder D |
| grader | `grader/reference.py`, `starter.py`, `instance.py`, `test_project.py` | none | none | - | Builder E |
| cards | `cards.json` from L01-L09 | none | none | - | Builder F (after A-E) |

Ownership rule: each builder writes only its lesson files and twins. Builder A writes the hub after L01-L03 exist, so the lesson
map is right; the hub cross-check runs at integration. Builder E's grader is independent of the lessons and of the project page
text, and is written from the §5.2 interface only.

Ordering check (no lesson links a later definition):
- L01 uses only prose and the M1/M2 concepts `derivative` and `partial-derivative`, if needed for the best-response check.
- L02 uses L01 (`nash-equilibrium`) and M4 (`expectation`, `conditional-expectation-elementary`).
- L03 uses L02 (`bayesian-nash-equilibrium`) and E1 `competitive-equilibrium` (linked, in closure).
- L04 uses L03 (`adverse-selection`) and M4 (`expectation`).
- L05 uses L04 (`signaling`) and L03 (`adverse-selection`).
- L06 uses L02 (Bayesian expectation over effort outcomes), M2 `derivative` for the first-order condition, and L05 for the
  participation constraint language.
- L07 uses L05 (`screening`) and L04 (`signaling`) as the two worked special cases of the revelation principle.
- L08 uses L02 (`bayesian-nash-equilibrium`), L07 (`mechanism-design` in prose), and E1 `economic-surplus` (linked).
- L09 uses L08 (`bid-shading`, `winners-curse`) and L01 (`nash-equilibrium`).

Hours check: 9 × 10 = 90 (lessons; hub `data-hours-lessons="90"`); project 20 (hub `data-hours-project="20"`); 110 total = curriculum.

---

## 4. Hub (`index.html`, Builder A)

- `<html lang="en" data-root="../../../" data-unit="E2" data-page="index">` and
  `<main data-hours-lessons="90" data-hours-project="20">` (sums to 110; project 18.2%, inside 10-40%).
- 4-8 measurable objectives in `ol.objectives` (verbs such as compute, derive, check, compare, construct). Example: "Compute
  every pure-strategy Nash equilibrium of a finite two-player game by checking best responses."
- Prerequisites: E1 and M4 (with M2, M1, P0.1 through them). Links to the concept index anchors
  (`../../../concepts.html#<id>`) for the concepts used. Do not link an unbuilt E1 or M4 page: neither `course/modules/E/` nor
  `course/modules/M/M4/` exists (verified by listing `course/modules/`, which contains AC, AP, CF, M (M1 only), S).
- Placement diagnostic: `<section class="quiz" id="placement" data-unit="E2" data-page="placement" data-mastery="0.8">`.
  The bar 0.8 matches the M1 and E1 precedent. At least two `<li class="item" … data-skill>` items test what rungs 1-2 teach
  (the worked example's auction payment rule and the completion problem's missing step, `check_pages.py` line 352-353).
  The other items test E1 and M4 prerequisites: best responses, a conditional expectation, an implicit or envelope derivative.
- Lesson map: one `<a class="card" href="Lnn.html" data-progress-key="E2/Lnn">` per lesson, with `span.card-kicker` `Lnn · 10 h`
  (M1 pattern, `course/modules/M/M1/index.html:151-153`), and a link to `project.html`.
- Project ladder: `ol.ladder` with four `span.rung-title` entries in order (worked example, completion problem, independent
  project, stretch), `tools/check_projects.py` line 33.
- Tier U: rungs 1-2 keep full length (BLUEPRINT §4: the minimum applies from tier M upward).

---

## 5. Project (`project.html`, Builder D): ladder, spec, grader

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py` line 33 requires the order)

1. **Rung 1, worked example** (`lab-E2-project-1`): one fully solved, annotated payment and revenue calculation for a
   two-unit, four-bidder SIMULATED auction under both formats, in integer cents. Each step has a "why" annotation.
2. **Rung 2, completion** (`lab-E2-project-2`, `class="lab completion"`): the uniform-price clearing-rank line and the
   discriminatory payment line are removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals
   the twin line or contains a blank (completion rule, `tools/run_labs.py`).
3. **Rung 3, independent project** (graded): (a) the autograded engine `auction_sim.py` to the §5.2 interface, and (b) the
   design memo, rubric-graded (§5.5). `lab-E2-project-3` is the rung-3 check: it calls the engine on the reference case and
   prints the outcome table.
4. **Rung 4, stretch** (optional, not graded, open-ended): asymmetric bidders, a third format (for example a Dutch clock on
   the same bids), or a stated hypothesis about how bid shading changes with the number of bidders.

### 5.2 Spec (`dl.spec`; `tools/check_projects.py` lines 34-49 require the terms and the grading words)

Terms: Context (2-4 sentences), Inputs, Required outputs, Constraints, Grading. The grading entry must contain the words
"autograder" and "rubric" (`tools/check_projects.py` `GRADING_WORDS`, lines 30-49).

- **Context.** A Treasury-style issuer sells k identical units of a security to n bidders in a sealed-bid auction. The
  format (uniform-price or discriminatory) changes what winners pay, the revenue, the shading of bids and the allocation
  efficiency. The design question is which format to recommend, and how far the answer depends on the model.
- **Inputs (planner proposal, §10 Q5).** All money in integer cents. Values `v` and bids `b` are non-negative integers
  (cents). The bidder count `n` and the unit count `k` are integers with `1 <= k < n`. Generated instances are labelled
  **SIMULATED**. No real auction data is used (§9).
- **Required outputs.** `auction_sim.py` with the functions below; `memo.md` (the design memo).

  ```
  allocate(bids: list[int], units: int) -> list[bool]
  payments(format: str, bids: list[int], units: int) -> list[int]
  revenue(format: str, bids: list[int], units: int) -> int
  efficiency(values: list[int], bids: list[int], units: int) -> tuple[int, int]
  symmetric_bid_single_unit(format: str, n: int, value: int) -> int
  ```

  `format` is `"uniform"` or `"discriminatory"`. `allocate` awards the `units` highest bids; ties go to the lower bidder index.
  `payments` returns the amount each bidder pays, in cents (0 for a loser): under `"uniform"` each winner pays the
  `(units+1)`-th highest bid; under `"discriminatory"` each winner pays its own bid. `efficiency` returns
  `(value of the winners, value of the k highest values)`. `symmetric_bid_single_unit` returns the symmetric equilibrium bid
  for `units = 1` only (§5.3), rounded half up to the cent.
- **Constraints.**
  - Integer cents: each money output is an `int`, computed from exact `Fraction`s and rounded once, half up, to the
    nearest cent (rule stated on the page, in the spec and in the module docstring).
  - Valid input: `1 <= units < n` and non-negative integer bids and values (exception table, §5.4).
  - Standard library only; no network; the same code runs in Pyodide and under pytest.
- **Grading.** Autograder (`grader/test_project.py`, dual-mode) and rubric (`memo.md` against §5.5). The spec must name both.
- **Reading list.** `ol.reading-list` cites the eight §8 keys that the project uses (Vickrey 1961, Milgrom & Weber 1982 and
  Fudenberg & Tirole 1991 at most). It cites no key whose claim the project does not use.

### 5.3 Planner's reference closed forms (hand derivations; the builder re-derives them, §10 Q5)

Model proposed for the single-unit lab and the grader's equilibrium check: `n >= 2` bidders, independent private values,
each value uniform on \([0,1]\) (in cents: uniform on \([0,10000]\)), risk-neutral bidders (Assumption 1), symmetric strategies
(Assumption 2), each bidder wants one unit.

| Quantity (single unit, first price, symmetric) | Closed form | Derivation (short) |
|---|---|---|
| Symmetric equilibrium bid | \(b(v) = \frac{n-1}{n}\,v\) | Bidder with value \(v\) bids \(b\) to maximize \((v-b)\Pr(\text{win}) = (v-b)\,(b/\beta)^{n-1}\) on the bid range \([0,\beta]\), \(\beta = (n-1)/n\); first-order condition gives \(\beta = (n-1)/n\) |
| Expected revenue, first price | \(\frac{n-1}{n+1}\) | \(E[b(V_{(1)})] = \frac{n-1}{n}\,E[V_{(1)}] = \frac{n-1}{n}\cdot\frac{n}{n+1}\), with \(V_{(1)}\) the highest of \(n\) uniform values |
| Expected revenue, second price | \(\frac{n-1}{n+1}\) | \(E[V_{(2)}]\), the second highest of \(n\) uniform values |

The equality of the two revenues is an instance of revenue equivalence. The builder proves it for this model on the page with the
two calculations above; it cites no source for it (the revenue-equivalence literature is not in the registry, §8.1).

Checks the planner did by hand (builder and verifier re-check): the first-price bid is below value for \(n \ge 2\) and equals
value only in the limit \(n\to\infty\), so bid shading is strictly positive for every finite \(n\); with \(n=2\) the bid is
\(v/2\).

Multi-unit (\(1 < k < n\)): the planner **does not** derive an equilibrium for either format. The autograder tests the payment
and allocation rules on given bid profiles, which are exact and need no equilibrium. Strategic multi-unit bidding is taught in
the memo as a stated, student-chosen bidding rule (§10 Q5).

### 5.4 Exception table (grader tests demand these, and only these)

| Condition the page names | Exception | Message must name |
|---|---|---|
| `format` not `"uniform"` or `"discriminatory"` | `ValueError` | the two allowed names |
| `units < 1` or `units >= n` (no clearing rank exists) | `ValueError` | the condition, e.g. "units must satisfy 1 <= units < n" |
| a negative bid or value | `ValueError` | the condition violated |
| `n < 2` in `symmetric_bid_single_unit` | `ValueError` | "n must be at least 2" |

Any other invalid input may raise any exception or return; the tests do not require a type for it.

### 5.5 Rubric (memo; `both` requires it, `tools/check_projects.py` `rubric_problems`, lines 58-72)

Six criteria, each with four observable levels (level 4 down to level 1). Examples of required observability:

1. **Model and rules.** States the formats, the bidder count, the unit count and the value distribution. Level 4: lists `n`,
   `k`, the two payment rules and the Assumptions 1-2 with their scope. Level 1: "a simple auction".
2. **Derivation.** Shows the single-unit bid derivation with every step. Level 4: the first-order condition and the bid
   \((n-1)/n\cdot v\) reproduced for the stated `n`. Level 1: states a bid with no derivation.
3. **Revenue and shading.** Reports revenue in cents under both formats and the bid shading, with the rounding rule stated.
   Level 4: each figure in cents, sign and base of each difference.
4. **Common value and the winner's curse.** Explains what changes when values are common and signals are private. Level 4:
   names the signal model, the expected overpayment computed in the lab, and the seed.
5. **Efficiency and recommendation.** Compares allocative efficiency and recommends a format or none, naming what would change
   the answer. Level 4: recommendation follows from a computed number and names one changed assumption.
6. **Limits.** States risk neutrality, independence, symmetry, the unit-demand assumption and the absence of real Treasury data,
   and what changes without each. Level 4: each limit paired with its effect in the model.

Exemplars: **exemplar-a (level 4)** and **exemplar-b (level 2)**, fully written, annotated with the descriptors they meet or miss.
Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in M1). The
page shows where the student's scores diverge from the exemplar scores.

Adversarial question bank: not required (the memo is not an IC defence or debate; §10 Q9).

### 5.6 Time budget (`<table id="hours">`, sums to 20 h)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved reference case, annotated line by line |
| Rung 2, completion problem | 2 | Fill the clearing-rank and the discriminatory payment lines, then run the instant check |
| Autograded engine `auction_sim.py` and the test run | 8 | Implement the §5.2 interface, pass the suite on seeds 0-49, handle the exception table |
| Derivation of the single-unit bids and the revenue check | 3 | The §5.3 calculations, written as proofs with Assumptions |
| Design memo draft and revision | 4 | Cents, rounding rule, the six §5.5 criteria |
| Self-assessment against exemplars | 2 | Score the memo, then compare with exemplar-a and exemplar-b |
| **Total** | **20** | Equals `data-hours-project` on the hub |

---

## 6. Grader design (Builder E)

**Files (no Atlas; solution is unit-local).** `course/modules/E/E2/grader/`: `instance.py`, `reference.py` (the solution;
excluded from deployment, BLUEPRINT §7), `starter.py` (stubs that raise `NotImplementedError`), `test_project.py`. The
student file is `auction_sim.py` (§10 Q6).

Grader panel on `project.html`, as in M1 and CF1: `<section class="grader-panel" id="grader" data-unit="E2"
data-grader="grader/" data-suite="test_project.py" data-support="instance.py" data-solution="auction_sim.py"
data-starter="starter.py" data-packages=""></section>` (attributes checked by `tools/check_projects.py`, lines 122-136; the
panel element is at `course/modules/M/M1/project.html:203` for M1). `data-packages` is empty: standard library only.

- **`instance.py`**: `make_instance(seed: int) -> dict[str, Any]` (the exact signature check at `tools/check_projects.py`
  line 134 is `def make_instance(seed: int)`). Deterministic per seed through `random.Random(seed)`. Returns `n` in 2..5, `k` with
  `1 <= k < n`, and generated values in integer cents. Labelled **SIMULATED** in the docstring. Seeds 0-49 give materially
  different outcomes: the revenues and efficiency totals change, not only the labels. The verifier checks 20 sampled seeds.
- **`reference.py`**: the full solution with `Fraction` and one half-up rounding per money output. Passes every test on seeds
  0-49 (`run_graders.py --unit E2 --seeds 0-49`).
- **`starter.py`**: `NotImplementedError` stubs; the suite must fail on it (`tools/run_graders.py` checks this).
- **`test_project.py`** (properties and numbers; no hard-coded answers; each test recomputes its expected value from the
  instance's own parameters by an oracle written separately from `reference.py`):
  - the first-price symmetric bid equals \((n-1)/n\cdot v\) rounded half up to the cent, for every `n` in the instance;
  - second-price payments equal the \((k+1)\)-th highest bid for each winner (uniform), and each winner's own bid (discriminatory);
  - losers pay 0 under both formats; winners number exactly `k`; ties go to the lower index;
  - revenue equals the sum of `payments`, and never exceeds the sum of the winning bids;
  - efficiency with truthful bids (`bids == values`) returns the value of the `k` highest values as its first and second entries;
  - bid shading: first-price bids are at most value for every bidder on every seed;
  - the exception table (§5.4): each named condition raises `ValueError` naming the condition; no other exception type is
    required;
  - integer output: every money output is an `int`.
  - Failure messages name the violated property and hint at the concept. They never print the answer.
- **Dual mode**: the same suite runs in Pyodide and under pytest; each test under 5 s in Pyodide; the suite under 60 s.
- **Five alternative correct implementations** (must all pass; the verifier writes them as test-only fixtures in its
  scratch checkout and archives the scripts under `ledgers/E2/scripts/`): (1) closed-form payments and the closed-form bid
  for `units == 1`; (2) iterated grid best response on the integer-cent grid, stopped at the closed-form bid; (3) a
  sort-based clearing rule; (4) a counting-based clearing rule; (5) float arithmetic with the same half-up rule applied to
  the exact value of each output. The rule is stated, so no test is tolerance-based.

**Mutants (the verifier writes at least ten complete modules to `ledgers/E2/mutants/*.py`; `tools/mutate_graders.py` requires at
least three (`tools/mutate_graders.py` line 42), VERIFIER §2.6 requires three, and this plan requires ten; each must be killed;
`mutate_graders.py --unit E2 --seeds 0-9`):**
1. uniform-price winners pay their own bid (wrong payment rule);
2. discriminatory winners pay the clearing (rejected-bid) price;
3. uniform clearing price taken at the `units`-th highest bid (off-by-one rank);
4. ties broken toward the higher index (contradicts the stated rule);
5. the unit cap omitted, so more than `k` bidders win;
6. revenue summed over all bids, not winners' payments;
7. single-unit first-price bid uses \((n-2)/(n-1)\) (wrong bidder count);
8. bid shading sign flipped (first-price bids above value);
9. efficiency computed on bids instead of values;
10. payments truncated to the cent instead of rounded half up (breaks the cases where the exact value ends in .5 cents);
11. a hard-coded answer for seed 0.

Each mutant's docstring's first line describes the error. Record each mutant's description and the test that killed it in the
ledger (`tools/ledger.py`).

---

## 7. Cards builder (Builder F, after A-E)

- `course/modules/E/E2/cards.json`, ids `E2-c001` upward, `lesson` in `L01`-`L09`. `tools/check_pages.py` `check_cards`
  checks the unit prefix, the lesson names, the grades and the registry keys, and requires at least one card per lesson.
- One card per definition, theorem statement, key formula, key empirical result and misconception (BUILDER_RULES §7).
- Grade T for every derived result. Set `"basis"` to the lab or problem that establishes a numerical result, for example
  `"basis": "Lab 8, simulation (SIMULATED, seed 0-9)"` or `"basis": "Lab 2, exact check"`.
- Cite a registry key only for a claim the key supports (§8): for example `cite: ["vickrey1961counterspeculati"]` on a card that
  names the second-price rule as Vickrey's device, only after the verifier confirms the claim against the paper's abstract.
  Otherwise `cite` is `[]` and the card's `basis` names the lab.
- No duplicate fronts.

---

## 8. Registry keys the module may cite

All eight keys below exist in `references/references.json` with `status: "verified"` and `used_by` containing `"E2"`. Each
`source_strings` value matches the curriculum's text (the planner read each record in the registry).

| Key | Registry record (as read) | `references.json` line | Curriculum string | Use in E2 |
|---|---|---|---|---|
| `nash1950equilibrium` | Nash, "Equilibrium points in n-person games", PNAS 36(1), doi 10.1073/pnas.36.1.48, 1950 | 17849 | "Nash (1950), PNAS 36(1)" | L01 definition of Nash equilibrium (cite key only) |
| `akerlof1970market` | Akerlof, "The Market for Lemons", QJE 84(3), 1970 | 395 | "Akerlof (1970), QJE 84(3)" | L03 adverse selection |
| `spence1973job` | Spence, "Job Market Signaling", QJE 87(3), 1973 | 21113 | "Spence (1973), QJE 87(3)" | L04 signaling |
| `rothschild1976equilibrium` | Rothschild & Stiglitz, "Equilibrium in Competitive Insurance Markets", QJE 90(4), 1976 | 20312 | "Rothschild & Stiglitz (1976), QJE 90(4)" | L05 screening |
| `holmstrom1979moral` | Holmström, "Moral Hazard and Observability", Bell Journal of Economics 10(1), 1979 | 12604 | "Holmström (1979), Bell Journal of Economics 10(1)" | L06 moral hazard |
| `vickrey1961counterspeculati` | Vickrey, "Counterspeculation, Auctions, and Competitive Sealed Tenders", JF 16(1), 1961 | 22219 | "Vickrey (1961), JF 16(1)" | L08-L09 auctions (cite key only) |
| `milgrom1982theory` | Milgrom & Weber, "A Theory of Auctions and Competitive Bidding", Econometrica 50(5), 1982 | 17331 | "Milgrom & Weber (1982), Econometrica 50(5)" | L08-L09 auctions, common value and the linkage principle, only as cited |
| `fudenberg1991game` | Fudenberg & Tirole, *Game Theory*, MIT Press, 1991 | 9514 | "Fudenberg & Tirole, Game Theory (1991)" | L01-L02 solution concepts, textbook level, no locator |

Notes on the registry, to be checked by the verifier and not resolved by the planner:
- `vickrey1961counterspeculati`: the record lists years [1961, 2012]; `print_year` is 1961. The curriculum says 1961.
- `nash1950equilibrium`: the record lists years [1950, 2011]; `print_year` is 1950. The curriculum says 1950.
- `fudenberg1991game` has no DOI; the record carries a `openlibrary.org` URL and an ISBN. The planner did not confirm the
  ISBN against the edition. `tools/verify_refs.py --unit E2` (online, not run) is the identity check.
- Full-text access: the planner did not read any of the eight papers. Every attribution in E2 is limited to what the
  verifier reads in the abstract or the title (VERIFIER §2.1). No page, table, equation or coefficient from these papers may
  be cited (§10 Q9).

Keys in the registry that belong to other modules and are **not** E2 sources: `mascolell1995microeconomic` (used_by E4; the
curriculum's E4 text), `milgrom1982information` (Milgrom & Stokey 1982, used_by E4). Their use in E2 requires the architect's
approval (§10 Q8).

### 8.1 REFERENCE_REQUESTS (topics only; no bibliographic data typed from memory)

- **Topic: experimental evidence on bidding in common-value auctions and the winner's curse.** Needed for L08 (grade B or C
  claims about observed bidder behaviour; the two-sided requirement of BUILDER_RULES §1.5 applies). Admission path: a DOI
  supplied by the architect, through `tools/add_reference.py`. Blocks any empirical sentence in L08 (the lab is a model
  result, not an empirical one).
- **Topic: the operating rules of U.S. Treasury auctions (uniform-price and discriminatory formats).** Needed for the project's
  context and L09's one practice sentence. Admission path: an issuer page on `home.treasury.gov`, which is allow-listed in
  `references/authorities.yaml` (line 21). Until admitted, the practice sentence is omitted or graded D with "It is widely
  claimed" (BUILDER_RULES §2.2).
- **Topic: empirical comparisons of uniform-price and discriminatory auction revenue.** Needed for L09's two-sided debate
  statement if the builder makes one. None is required by the curriculum (no debate key, §0). Without it, L09 states the
  model result only and makes no empirical ranking claim.
- **Topic: the revenue-maximizing (optimal) auction and the revelation-principle primary literature beyond the eight keys.**
  Needed only if L07 or L08 names the optimal mechanism. Without it, the lesson states the finite-type result it proves and
  attributes nothing else.

The architect resolves these through `tools/add_reference.py`. Planner did not verify any new source, so none is proposed as a key.

---

## 9. Real-data policy

- **No real data.** The curriculum names no dataset for E2 (`curriculum/02-economics-finance-core.yaml:50-87` has eight
  free-text book and paper sources and no data field). The embedded snapshots (`course/assets/data/market/MANIFEST.json`
  holds `fx_daily`, `fx_monthly` and `ust_daily`, per `tools/data_sources.yaml`) are not about auctions.
- Lab and grader inputs are generated parameters and exact formulas. The L08 seeded simulation and the grader's generated
  cases carry the **SIMULATED** label on the page and in the docstring. The exact labs (L01-L07, L09, the project rung 1-2 checks)
  are not labelled SIMULATED (§2.2).
- No `data-files` attribute on any lab; no MANIFEST entry; no `DATA_REQUESTS` entry is needed.
- Real Treasury auction results are **not** proposed. `home.treasury.gov` is allow-listed for issuer pages
  (`references/authorities.yaml:21`), but the auction results files are not an issuer page the planner read, and no licence
  quote for them exists in `tools/data_sources.yaml`. If the architect wants a real-data exercise, the request goes to
  `DATA_REQUESTS` with the source URL, the licence quote, and the transform, and the page carries an honest-pending note.

---

## 10. Open questions for the architect (numbered; the first three block the project spec)

1. **Hours split.** 90 h lessons (9 × 10) and 20 h project (18.2%). Alternative: 8 lessons of 10 h with a 30 h project (27%), which
   requires merging two lessons (for example L03-L04). The 9-lesson split keeps one concept per lesson except L07 and L08.
   Confirm, or name the alternative.
2. **Project model (blocking for the grader interface).** The curriculum says "strategic bidders" (`yaml:83-85`). The planner
   proposes: symmetric independent private values, uniform on the cent grid, risk neutral; the single-unit equilibrium is
   derived and tested (§5.3); multi-unit formats are tested on payment and allocation rules only, with the bidding rule stated
   by the student in the memo (§5.3, last paragraph). Confirm, or choose an equilibrium-tested multi-unit model (requires a
   derivation the planner has not made).
3. **Frozen project interface (blocking).** Freeze the five function signatures in §5.2 and the exception table in §5.4 before
   building (precedent: E1 Q4-Q5, AC4 Q7-Q8). Confirm `auction_sim.py` as the student file name (§10 Q6 below).
4. **Optimisation without convexity or Lagrangians.** `lagrange-multiplier`, `kkt-conditions`, `convex-function`, `convex-set`
   and `principle-of-optimality` are M7 (outside the closure; `curriculum/curriculum.json` `concepts`). Mechanism design (L07)
   and moral hazard (L06) use finite-type enumeration and M2 derivatives, with the envelope theorem (`envelope-theorem`, M2,
   in the closure) for the information rent. Recommendation: this route, with no M7 concept and no name for the Lagrangian.
   The same decision was made for E1 (E1 Q3). Alternative: add M7 to E2's prerequisites (a curriculum change; not proposed).
5. **Bayesian inference (S1, outside the closure).** Bayesian–Nash equilibrium (L02) and the posterior in the common-value lab (L08)
   need Bayes' rule. The concept `bayesian-inference` is owned by S1 (`curriculum.json` concepts). Recommendation: Bayes' rule is
   stated in plain words from `conditional-expectation-elementary` (M4, in closure), with no link and no `data-concept` on the
   term (the CF1 Q2 and E1 Q10 precedent). Confirm.
6. **Solution file name.** Proposed `auction_sim.py`. Confirm.
7. **Money.** Integer cents with one half-up rounding per output, stated on the page (§2.1 item 8; E1 Q6). The
   symmetric bid in the autograder is rounded half up. Confirm.
8. **Sources beyond the curriculum.** Only the eight §8 keys are cited. Confirm: (a) `mascolell1995microeconomic` and
   `milgrom1982information` stay with E4; (b) no historical attribution beyond the registry title and year; (c) the four
   REFERENCE_REQUESTS topics in §8.1 are admitted through `add_reference.py` or the lessons teach the results without the
   attribution (planner recommends the latter for the empirical topics).
9. **Full-text reading.** The planner read no paper. VERIFIER §2.1 requires the abstract read for each attributed claim. Confirm
   that attributions limited to the abstract are acceptable for grade B and C claims, and that the verifier records the
   abstract source per row. Without this, every attribution is a grade-C claim with no locator.
10. **Expected utility and risk aversion (E3, outside the closure).** Bidders in §5 are risk neutral, and the Assumption says so.
    Recommendation: no risk-aversion content in E2. Confirm; the alternative is an E3 prerequisite (a curriculum change).
11. **Cournot across E1 and E2.** E1 describes the Cournot equilibrium without the word "Nash" (E1 Q2). E2 defines
    `nash-equilibrium` (L01) and must say that the Cournot equilibrium of E1 is a Nash equilibrium. Recommendation: a plain-prose
    cross-reference in L01 with a link to `../../../concepts.html#cournot-competition` (E1 is in the closure, so the link is
    allowed by `check_dag.py`). Confirm.
12. **Figures.** No figure is proposed. A bid-shading curve (\(b(v)=\frac{n-1}{n}v\)) would need a JS kernel and a test in
    `tests/test_figure_kernels.py` before use (BUILDER_RULES §6.4; CF1 Q6 precedent: no new figures). Confirm no figures.
13. **Adversarial memo.** The memo is an auction design memo, not an IC defence. No 15-angle question bank. Confirm (E1 Q9 and AC4
    Q8 precedent).
14. **Section list vs BUILDER_RULES §4.2.** `tools/check_pages.py` line 75 requires `references` as a lesson section after the
    quiz (`LESSON_SECTIONS`); BUILDER_RULES §4.2 lists nine items and no references section. The plan follows the tool. Confirm
    that the lesson template carries `section.references` (`course/templates/lesson.html` was not read by the planner).
15. **Plain terms outside the 12 concepts.** Terms such as `common knowledge`, `order statistics`, `reserve price`, `payoff`,
    `best response`, `principal-agent` (not a registered concept), `Bayes' rule`, `information rent`, `clearing price`,
    `allocative efficiency` are plain prose, with a plain `<dfn>` without `data-concept` where emphasised. Confirm; the term list
    becomes `GLOSSARY_REQUESTS` items.
16. **Order of lessons L03-L05.** Adverse selection (L03) is placed before signaling (L04) and screening (L05) because both respond
    to it. Confirm.

---

## 11. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

```bash
.venv/bin/python tools/check_pages.py --unit E2            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit E2
.venv/bin/python tools/check_projects.py --unit E2
.venv/bin/python tools/run_labs.py --unit E2              # --page L08 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/E/E2/L01.html   # per page, after twins are written
.venv/bin/python tools/embed_labs.py course/modules/E/E2/L08.html --refresh lab-E2-L08-1   # after editing a twin
.venv/bin/python tools/run_graders.py --unit E2 --seeds 0-49
.venv/bin/python tools/mutate_graders.py --unit E2 --seeds 0-9             # verifier only
.venv/bin/python tools/verify_refs.py --unit E2                            # verifier or architect; online
.venv/bin/ruff check tests/labs/E2 course/modules/E/E2/grader && .venv/bin/ruff format --check tests/labs/E2
.venv/bin/mypy                                            # strict, repository configuration
```

Flags as read by the planner: `check_pages.py`, `check_dag.py`, `check_projects.py` accept `--unit` (and `--all`) (`tools/check_projects.py`
argparse, line 159 region); `run_labs.py` accepts `--unit`, `--all`, `--page` (`tools/run_labs.py` lines 119-121); `run_graders.py`
accepts `--unit`, `--all`, `--seeds` (lines 129-131; default 0-49); `mutate_graders.py` accepts `--unit`, `--all`, `--seeds` (lines
30-32; default 0-9); `embed_labs.py` takes pages and `--refresh [LAB_ID ...]` (lines 130-131). The planner did not execute any of
these commands. `verify_refs.py --unit` is cited from VERIFIER §2.1; its flags were not read by the planner.

`page_smoke.py` is not run by builders (timing-sensitive; the verifier runs it on a quiet machine). Repo-wide gates (`check_pages.py
--all`, `check_dag.py --all`, `build_site.py --check`, `render_curriculum.py`, `verify_refs.py --offline`) are the architect's, once,
before any merge. Do not run them per builder.

---

## 12. Tooling assumptions that do not hold, or are unverified, for this unit (flagged)

1. **No Atlas milestone.** E2's project has no `atlas:` key (`curriculum/02-economics-finance-core.yaml:81-87`) and no atlas entry
   names E2. `tools/check_projects.py` skips the contract check (its Atlas branch is conditional on `atlas`). No
   `atlas/E2.contract.md` is needed, and none is drafted here. `atlas/` contains `A8.contract.md` and `A15.contract.md` only.
2. **No debate.** E2 has no `debate:` key (`curriculum/02-economics-finance-core.yaml:50-87`), so `check_pages.py` does not require a
   debate brief (`tools/check_pages.py` `if u.entry.get("debate")`, line 412 region).
3. **Tier-U grading `both`.** `check_projects.py` requires the rubric (4-7 criteria, four levels each, exemplars at two or more levels)
   and the grader panel (`data-unit`, `data-grader`, `data-suite`, `data-solution`, `data-starter`), and the spec's grading entry must
   contain "autograder" and "rubric" (`tools/check_projects.py` lines 41-50, 58-72, 122-136).
4. **One curriculum lab.** The curriculum names one lab (`yaml:80`). BUILDER_RULES §3.4 asks for a numerical check per key formula.
   The plan adds one lab per lesson (E1 Q2 and M1 Q2 precedent).
5. **Prerequisites are unbuilt.** E1, M2 and M4 are not built: `course/modules/` contains AC, AP, CF, M (M1 only) and S. The hub links
   prerequisite concepts through `concepts.html` anchors only. `concepts.html` contains the anchors for the closure concepts the plan
   links (`envelope-theorem`, `cournot-competition`, `conditional-expectation-elementary`, `expectation`, `independence`,
   `quantile-function`, `nash-equilibrium`, `pareto-efficiency`, `economic-surplus`, `law-of-large-numbers`; each count 1 in
   `course/concepts.html`).
6. **check_dag sees linked uses only.** An unlinked use of `bayesian-inference`, `expected-utility`, `lagrange-multiplier`,
   `kkt-conditions`, `convex-function` or `first-welfare-theorem` passes `check_dag.py`. The verifier must read every lesson for these
   names (VERIFIER §2.9; §10 Q4-Q5, Q10).
7. **Concept-link names for unregistered terms.** Plain prose or plain `<dfn>` (§10 Q15).
8. **Labs must be exact or labelled.** Exact labs use `fractions` and are `-W error` clean. Simulated labs are seeded
   (`random.Random(seed)`) and labelled SIMULATED.
9. **Registry identity.** All eight keys are verified and their `source_strings` match the curriculum text. The planner did not run
   `verify_refs.py`; the identity of the Fudenberg & Tirole record (ISBN, edition) is unchecked (§8 notes).
10. **Section list.** `check_pages.py` requires `references` as a lesson section (`tools/check_pages.py` line 75); BUILDER_RULES §4.2 does
    not list it (§10 Q14).

---

## 13. DAG problems (concepts that natural content would use outside the closure)

| Concept | Owner | Where the natural content uses it | Resolution in this plan |
|---|---|---|---|
| `bayesian-inference` | S1 (`curriculum.json` concepts) | Bayes' rule in L02 and the posterior in L08 | Plain prose from M4 conditional expectation; no link, no `data-concept` (§10 Q5) |
| `expected-utility`, `arrow-pratt-risk-aversion` | E3 | risk-averse bidders (L08, L09) | Not used; risk neutrality is Assumption 1 (§10 Q10) |
| `lagrange-multiplier`, `kkt-conditions`, `convex-function`, `convex-set`, `principle-of-optimality` | M7 | constrained optimal mechanisms (L06, L07) | Finite-type enumeration and M2 derivatives; `envelope-theorem` (M2, in closure) for rents (§10 Q4) |
| `first-welfare-theorem`, `arrow-debreu-equilibrium` | E4 | efficiency of equilibrium (L08, L09) | Not used; efficiency is the computed allocative value of §5.2 |
| `risk-neutral-probability` | FC2 | the phrase "risk-neutral" in auctions | Written as "risk neutral bidders" in prose; not linked and not defined |
| `principal-agent` (no concept row) | none | moral hazard framing (L06) | Plain prose, no concept (§10 Q15) |

No DAG_DEFECT is a build failure: each row has a resolution. Each row needs the architect's confirmation (§10 Q4, Q5, Q10).

---

## 14. After the builders

1. Orchestrator integrates; runs the §11 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L03, L04-L06, L07-L09, project. The project verifier writes at
   least ten mutants (§6) and the five alternative implementations (§6). Failing rows return to the builder that owns the file,
   with only the failing rows.
3. Ledger at `ledgers/E2.verification.json`; verifier scripts archived under `ledgers/E2/scripts/` (VERIFIER §3).
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed.

Architect decisions: pending (§10). This plan is the planner's proposal. Blocking before the builders start: §10 Q2 and Q3 (the
project model and the frozen interface). Q1, Q4, Q5, Q10 and Q11 have defaults that the builders may use if the architect does
not object.

## Architect decisions (2026-10-28, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank.
Module specifics: Nash equilibrium is defined here (E1 described it without the name); the project tests the single-unit closed form and the multi-unit payment and allocation rules only (no multi-unit equilibrium is claimed); attributions limited to the registry title and year; the Treasury practice claim is dropped.
