# LX1 build plan: Financial History (2026-11-03)

Unit: **LX1 · Financial History** · tier U · 50 h · prerequisites FC1, E5 · no Atlas milestone · no debate key ·
grading `rubric` (no autograder) · output directory `course/modules/LX/LX1/` (part code `LX`) · lab twins `tests/labs/LX1/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits. Executors: Haiku builders A to E (one lesson or
the project each), builder F (cards), then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never
writes a ledger.

Evidence convention: every statement about the curriculum cites `file:line` read during planning. Anything not in the
curriculum or the registry is marked **NOT IN CURRICULUM** or **NOT IN REGISTRY**. Planner-derived statements about the
tooling were checked by reading the tool source or by running `tools/coursekit.py` (`prerequisite_closure`, `concept_owner`,
`unit`, `built_units`) through the repo venv. Planner-run inline checks (no repo script): the `fx_monthly.csv` blank-cell
count in §6, and the MANIFEST field reads in §6.

Status: **BLOCKING ISSUES EXIST (§0.3).** The hours are feasible. The curriculum lab's data (B1), the credit-channel
evidence (B2) and the Bretton Woods dating and definition (B3) are not supported by any registry source. The architect must
decide B1-B3 before the L03 and L04 builders start. L01, L02 and the project may start once the §12 decisions Q1-Q4 are made.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part LX, code `LX`, title "History, Law & Professional Conduct" | `curriculum/06-profession-capstone.yaml:2-4` |
| Studio STUDIO-LX requires LX1 and LX2 (not a module prerequisite of LX1) | `curriculum/06-profession-capstone.yaml:6-8` |
| LX1 id and title "Financial History" | `curriculum/06-profession-capstone.yaml:19-20` |
| Tier `U`, hours `50` | `curriculum/06-profession-capstone.yaml:21-22` |
| Prereqs `[FC1, E5]` (only) | `curriculum/06-profession-capstone.yaml:23` |
| Core: "Bubbles and panics from the Dutch Republic to 2008, the gold standard and the Great Depression, Bretton Woods and its end, the history of central banking." | `curriculum/06-profession-capstone.yaml:24-26` |
| `introduces` has 7 concepts (mapped to lessons in §1) | `curriculum/06-profession-capstone.yaml:27-34` |
| Sources: five free-text strings (Kindleberger & Aliber 2015; Friedman & Schwartz 1963; Bernanke 1983 "AER 73(3)"; Eichengreen 1992; Garber 2000) | `curriculum/06-profession-capstone.yaml:35-40` |
| Lab: "Gold-standard adherence vs. depression depth on embedded data." | `curriculum/06-profession-capstone.yaml:41` |
| Project "Then vs. now"; brief: "Pick one historical episode and one current market condition, and write a mechanism-level comparison that says where the analogy holds and where it breaks."; deliverable "Two-page essay, every claim cited."; grading `rubric` | `curriculum/06-profession-capstone.yaml:42-49` (title 43, brief 44-47, deliverable 48, grading 49) |
| No `debate:` key and no `atlas:` key on LX1 | `curriculum/06-profession-capstone.yaml:19-49` (absent) |
| No Atlas entry names LX1 (planner check over the `atlas` array) | `curriculum/curriculum.json` `atlas` (computed) |
| JSON row for LX1 matches the YAML (hours 50, prereqs FC1 and E5, 7 concepts, lab, rubric) | `curriculum/curriculum.json:11313-11346` (`"id": "LX1"`) |
| The 7 concepts each map to module LX1 (planner check via `concept_owner`) | `curriculum/curriculum.json` `concepts`: speculative-bubble 5101, financial-panic 2785, gold-standard 3017, debt-deflation 2149, credit-channel-depression 2025, bretton-woods-system 1585, lender-of-last-resort 3505 (each entry's `module` field is LX1) |
| LX1 is required by the Finance Degree–Bachelor's credential and listed under "Financial History" in its course map | `curriculum/meta.yaml:62-63` (requires), `curriculum/meta.yaml:89` (course map) |
| No module lists LX1 in `prereqs` (planner check) | `curriculum/curriculum.json` (computed) |
| FC1 (prereq) is tier U, 70 h, prereqs P0.1 and E1; built | `curriculum/02-economics-finance-core.yaml:363` (entry), `plans/FC1-build-plan.md` |
| E5 (prereq) is tier U, 110 h, prereq E1; built | `curriculum/02-economics-finance-core.yaml:155-158`; `course/modules/E/E5/index.html` exists |
| Prerequisite closure of LX1 (computed by the planner with `tools/coursekit.py` `prerequisite_closure("LX1")`): **{E1, E5, FC1, M1, M2, P0.1}** | run output, planner |
| Concepts introduced by closure modules (planner `concept_owner` count per module): FC1 10, E5 13, E1 13, M1 14, M2 13, P0.1 11; total **74** usable concepts | run output, planner |
| Tiers of the closure: E1, M1, M2, P0.1 are F; FC1, E5 are U; nothing above U | `coursekit.unit(...).entry['tier']`, run output |
| P0.1 reports as unbuilt in `coursekit.built_units()`; LX is unbuilt (`course/modules/LX` absent) | run output; `ls course/modules` |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 50 h (`curriculum/06-profession-capstone.yaml:22`). The tool rules:

- lesson `data-hours` 6-12 (`tools/check_pages.py` `check_lesson`, line 227);
- hub `data-hours-lessons + data-hours-project = 50` (`check_pages.py` `check_hub`, lines 337-338);
- project share 10-40% of 50, i.e. 5 to 20 h (`check_pages.py` `check_hub`, lines 339-340);
- lessons sum to the hub's lessons figure (`check_pages.py` `check_hub`, the lesson-hours comparison).

Chosen split: **4 lessons × 10 h = 40 h; project 10 h (20%)**. 40 + 10 = 50. Feasible. **No STOP condition on hours.**

### 0.3 Blocking issues (architect decision required before the L03 and L04 builders start)

**B1. The curriculum lab names embedded data that does not exist for it.**
- The lab says "on embedded data" (`curriculum/06-profession-capstone.yaml:41`). The lab's variables are gold-standard
  adherence and depression depth (the same line).
- The embedded datasets are `fx_daily`, `fx_monthly` and `ust_daily` (`tools/data_sources.yaml:19`, `:53`, `:91`;
  `course/assets/data/market/MANIFEST.json`, ids at lines 32 and 63 and the `fx_daily` entry). None is a gold, price,
  output or bank-failure series. `ust_daily` starts 2000-01-03 (`MANIFEST.json`, `first` of `ust_daily`).
- `tools/data_sources.yaml` `rejected:` (lines 119-135) lists only the French library and Open Source Asset Pricing.
- BUILDER_RULES §6.6 bars embedding a series until its issuer's redistribution grant is quoted from the issuer's page
  (`BUILDER_RULES.md:337-386`). The planner did not read any historical-series issuer page and names none from memory.
- **Plan's default (architect to confirm):** the L03 curriculum lab is a SIMULATED stylised two-economy model (BUILDER_RULES
  §1.7, `BUILDER_RULES.md:62-64`) with an honest-pending note on L03 stating that no redistributable historical series is
  embedded, and a DATA_REQUEST (§7.2). The lab's claims are the model's claims only. Real data is used in L04 (§6), not for
  the curriculum lab.

**B2. The credit-channel claim has no citable registry key.**
- Source string: "Bernanke (1983), 'Nonmonetary Effects of the Financial Crisis in the Propagation of the Great Depression',
  AER 73(3)" (`curriculum/06-profession-capstone.yaml:38`).
- Not in `references/references.json`. Review queue entry at `references/review_queue.json:1610` (reason: "no candidate
  established identity"). The only candidate there, DOI `10.3386/w1054`, is an **NBER working paper** with a different title
  form (review queue candidate `type: report`). It is **not** the AER article and must not be admitted as that article.
- Consequence: no L03 page may make an empirical credit-channel claim with a citation. The mechanism is taught as a model
  (grade T, conditional on its stated assumptions, §3). Empirical attribution waits for a REFERENCE_REQUEST (§7.2).

**B3. The Bretton Woods definition and its end date have no registry source.**
- The core names "Bretton Woods and its end" (`curriculum/06-profession-capstone.yaml:25-26`). The concept
  `bretton-woods-system` is LX1's (`curriculum/curriculum.json:1585`).
- The planner grepped the registry for Bretton Woods, gold-exchange and dollar-convertibility titles and found none
  (NOT IN REGISTRY). The concept's definition and any date for the system's end therefore have no admitted source.
- What **is** established: the embedded `fx_monthly` series begins in January 1971 (`course/assets/data/market/MANIFEST.json`,
  `first` = "1971-01" at line 58). The lab may start its window there and say so. No claim that the system ended in any
  year is stated until a primary source is admitted (§7.2, REFERENCE_REQUEST 3).
- Consequence: the L04 definition and any dated end claim are blocked until B3 is resolved. The L04 lab is not blocked.

Non-blocking, but the architect should see them:

- **N1. Kindleberger & Aliber (2015).** Curriculum string `curriculum/06-profession-capstone.yaml:36`. Not in the registry;
  review queue entry `references/review_queue.json:1557` ("no candidate established identity"). Its review-queue candidate
  DOI `10.1007/978-1-137-52574-1` lists `first_author: Aliber`, which does not establish the cited identity. **Not admitted.**
  The page cites no Kindleberger key until a record is admitted (§7.2, REFERENCE_REQUEST 1).
- **N2. Friedman & Schwartz (1963).** Curriculum string `curriculum/06-profession-capstone.yaml:37` names two authors. The
  registry record `friedman1963monetary` (`references/references.json:9399`) lists the author "Friedman" only, with title
  "A monetary history of the United States 1867-1960" and year 1963. Cite the key only and do not type the second author
  in prose. The architect may correct the record through `tools/add_reference.py`; no builder edits it.
- **N3. Garber (2000) and Eichengreen (1992).** Both match their curriculum strings
  (`curriculum/06-profession-capstone.yaml:39-40`) and their registry records (`references/references.json:9667` and
  `:7946`). Usable.
- **N4. Current market condition (project).** No embedded source applies (§6). Q7 decides how a student sources it.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

4 lessons × 10 h = 40 h; project 10 h; total 50 h. Concept counts per row sum to 2+2+2+1 = 7, each concept in exactly one row
(`curriculum/06-profession-capstone.yaml:28-34`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `curriculum/06-profession-capstone.yaml:28-34`) | Lab (twin id, `tests/labs/LX1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Bubbles and panics: from the Dutch Republic to 2008 | `speculative-bubble`, `financial-panic` | `lab-LX1-L01-1`: fundamental value of a constant-growth asset by the closed form and a finite sum (M1 `growing-perpetuity` linked); a seeded SIMULATED price path with the gap above the stated fundamental printed. SIMULATED. | 10 | Builder A |
| L02 | The gold standard and debt deflation | `gold-standard`, `debt-deflation` | `lab-LX1-L02-1`: the real value of a fixed nominal debt in integer cents over an illustrative price path (SIMULATED), with half-up rounding stated | 10 | Builder B |
| L03 | The Great Depression: the credit channel and the lender of last resort | `credit-channel-depression`, `lender-of-last-resort` | `lab-LX1-L03-1` (**the curriculum lab**, `curriculum/06-profession-capstone.yaml:41`, SIMULATED per B1): a stylised two-economy model of parity adherence and output depth; the printed ordering is the model's, not history's | 10 | Builder C |
| L04 | Bretton Woods and its end | `bretton-woods-system` (blocked on B3 for its definition) | `lab-LX1-L04-1` (**real embedded data**, `data-files="fx_monthly.csv"`): dispersion of monthly log changes of one spot rate in two windows from the first MANIFEST month | 10 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 40 / 10 | none | none | - | Builder A |
| project | "Then vs. now" (`rubric`, §5) | none | `lab-LX1-project-1` (rung 1, SIMULATED), `lab-LX1-project-2` (rung 2, `class="lab completion"`, SIMULATED), `lab-LX1-project-3` (rung 3 check, real data) | 10 | Builder E |
| cards | `cards.json` from L01-L04 | none | none | - | Builder F (after A-E) |

**Deviation from the orchestrator's "about three lessons per builder":** a 50 h unit at 6-12 h per lesson gives four lessons
(§0.2), so each lesson builder owns one lesson. A three-per-builder split would leave two builders with no lesson. Q1 records
this and the alternative.

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes the hub after L01 exists, so the
lesson map is right; the cross-check runs at integration. Builder E writes the project, its rubric and exemplars, and its
three project labs. LX1 has **no grader** (rubric-only; §5.4 and §11), so no `grader/` directory is written.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses M1 `growing-perpetuity` and `present-value` (in closure; links to `../../../concepts.html#<id>`) and defines
  `speculative-bubble` and `financial-panic` in that order.
- L02 uses E5 `price-index-inflation` (in closure; link) for the price path, and L01's `speculative-bubble` only in prose
  (earlier lesson; link allowed as `L01.html#def-speculative-bubble` if used). Defines `gold-standard`, then `debt-deflation`.
- L03 uses L02's `gold-standard` and `debt-deflation` (links to `L02.html#def-...`) and E5 `business-cycle` and
  `national-accounts` (in closure; links). Defines `credit-channel-depression`, then `lender-of-last-resort`.
- L04 uses L02 `gold-standard` and L03 `lender-of-last-resort` (links). Defines `bretton-woods-system` last (B3 gates the
  definition). Its central-banking history after 1944 is prose with no `data-concept`.

Hours check: 4 × 10 = 40 (hub `data-hours-lessons="40"`); project 10 (hub `data-hours-project="10"`); total 50.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to LX1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` (the template, with its
Architect decisions, binding precedent), `plans/FC1-build-plan.md` (the nearest built precedent: its §2.1 lessons learned and
§7 DAG risk), this file. Study `course/modules/FC/FC1/` for layout (built). `course/templates/` holds the four skeletons.
Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded
   only at display. A page that shows a rounded figure states its rounding rule (half up, to the cent or to a stated
   decimal). Precedent: AC4 KNOWN LIMITATION 3, CF1 L01 Remark 5.2, FC1 §2.1 item 1.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only
   what the printed numbers show. Precedent: M1 LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Only the registry keys in §7.1 may be cited, and only at book or paper level unless the
   builder has read the locator. No page, table, year, coefficient, date or quotation is typed from memory. A historical
   episode's fact is stated only if a registry source the builder has read supports it, or it is removed (fixer rule: "unread
   standard/book content is ungraded or removed"). The planner read no historical text.
4. **Scope words need a computation or an explicit hypothesis.** "every", "all", "never", "always", "any", "the first", "the
   last", "central banking", "the gold standard" (as a universal), "bubbles", "panics" are used only where a derivation, a
   finite check, a lab or a cited source makes the claim. The scope of the unit is named in L01: episodes are examples, not
   a survey of all history (the core's "from the Dutch Republic to 2008" (`curriculum/06-profession-capstone.yaml:25`) is a
   scope, and the page must not claim coverage beyond the episodes it reads).
5. **Define before use.** Each of the 7 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson, and never before it. Terms outside the 7 (nominal debt, real debt, deflation, convertibility, parity, fundamental
   value, bank run, lender of last resort in L01-L02, the credit channel as a mechanism, central bank) are defined in prose
   with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
6. **Proposition hypotheses explicit.** Every Theorem, Proposition and Derivation lists numbered Assumptions (A1, A2, ...)
   before the statement. Examples: the fundamental-value closed form needs `r > g` and a constant dividend growth rate
   (A1, A2); the real-debt identity needs a fixed nominal debt in cents and a positive price level (A1, A2); the L03 model
   needs its parameters in the stated ranges (A1-A3).
7. **Grader rule.** Not applicable (rubric-only; §5.4). The autograder rules of BUILDER_RULES §5.3 and the mutant rules of
   fixer-rules line 19 do not apply to LX1.
8. **Money is integer cents.** Any money amount in a lab or in prose (the nominal debt, the real debt) is an `int` count of
   cents, computed from `Fraction` and rounded once, half up, with the rule stated (FC1 §2.1 item 8). No float money.
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own
   container; no element forces the page wider than 360 px. Enforced by `page_smoke.py`; builders do not run it.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no
    `if __name__ == "__main__":` guard. `run_labs.py` runs each twin as `python -I -W error <twin>`. The M1 twin
    `tests/labs/M1/lab-M1-L04-1.py` is the model.
11. **Basis-explicit rates.** Any rate or spread is stated with its unit (per cent per year, or a decimal per period), its
    convention (simple or log growth, per period) and its source (MANIFEST entry, or the lab's own parameter).
12. **Fail loud on bad data.** A lab that reads a CSV raises on a blank or non-numeric cell in a column it uses. It never
    skips a row silently (`CLAUDE.md` core guardrail: no silent fallbacks). §6.2 gives the blank cells this affects.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, `BLUEPRINT.md:156-163`) and a registry key or a derivation. A B- or
  C-graded claim names its published counter-evidence (BUILDER_RULES §1.5, `BUILDER_RULES.md:57-59`). **The registry holds no
  source for the credit-channel, gold-standard causation or bubble-existence claims that this plan has checked.** Those
  claims are derivations of a stated model (grade T, conditional), or are removed, or go to §7.2 with the counter-evidence lead.
- Concepts: §1 table; `<dfn>` only for the 7 concepts plus plain `<dfn>` for other terms. No `<a class="concept">` for any
  concept outside the prerequisite closure {E1, E5, FC1, M1, M2, P0.1} (§4).
- Prerequisite links: `href="../../../concepts.html#<id>"` for E1, E5, FC1, M1, M2 and P0.1 concepts (BUILDER_RULES §4.1).
  `href="Lnn.html#def-<id>"` for earlier LX1 lessons. A lesson never links a concept defined in a later lesson.
- Hub prerequisite links: the hub may link the built prerequisite hubs `../../FC/FC1/index.html` and `../../E/E5/index.html`
  (both exist; §11 item 3). No hub link to P0.1 (unbuilt).
- Labs: code lives once in `tests/labs/LX1/lab-LX1-Lnn-1.py` (and `lab-LX1-project-1..3.py`). The page carries
  `@@LAB:<file>@@` and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match
  `lab-LX1-<page>-<n>` (`check_pages.py`). Standard library only (`fractions`, `math`, `random.Random(seed)`, `csv`); seeded
  RNG only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- SIMULATED label: on every lab or figure that uses generated numbers (L01, L02, L03, the project's rungs 1-2). The real-data
  lab (L04, project rung-3 check) carries no SIMULATED label and names its dataset, licence and MANIFEST retrieval date
  (BUILDER_RULES §6.6, "Using a dataset in a lab").
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`,
  `course/concepts.html`, `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in
  code comments (precedent: M1 "Convention (project Q5)"; AC4 KNOWN 9).
- Banned strings (`tools/check_pages.py` lines 58-72 `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` outside code.
- Percent changes state the base and the direction. Growth and change rates state the convention (log or simple; per period).
- A finite enumeration is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10
  output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that LX1 must not give a different meaning (`notation/notation.json` `symbols` array and `macros`):

| Registered symbol | Registered meaning (locator) | LX1 rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation/notation.json` `symbols`, module S1) | **Not used.** A time horizon is `H`. |
| `R_f` | gross riskless return (AP1) | **Not used.** Nominal rate is `i`; real rate is `r`. |
| `\mathbb{Q}` | risk-neutral measure (AP1) | **Not used.** |
| `\Phi`, `\gamma_3`, `\gamma_4`, `R^\ast`, `R^{e\ast}` | M4 and AP1 meanings | **Not used.** |
| `\E` (macro) | expectation operator | Not used. Expected inflation, if needed, is `\pi^{e}_t` and is defined in prose. |
| `\R` (macro) | real numbers | Use `\R` for the real line, the registered macro (`notation/notation.json` `macros`). |

Local symbols (allowed; each defined on the lesson where it first appears and never redefined): `D` nominal debt in integer
cents (defined in L02), `P` price level (L02), `\pi` inflation (the E5 `price-index-inflation` meaning), `i` nominal interest
rate, `r` real interest rate, `g` growth rate of a dividend (L01), `d` dividend (L01), `F` fundamental value (L01), `H` horizon,
`s` spread or share where a lesson needs one. A symbol with a registered meaning is not reused with another meaning.

NOTATION_REQUESTS: none. The plan uses only local symbols and the registered `\R` macro.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the BUILDER_RULES §4.2 structure. Mandatory content, by lesson:

- **L01** `speculative-bubble`, `financial-panic`. Derivation (grade T, conditional): with a constant dividend growth `g`
  and discount rate `r` (A1: `r > g`; A2: `d_t` grows at the constant rate `g`), the fundamental value is `F = d_1 / (r - g)`
  (link M1 `growing-perpetuity`; the closed form is the M1 result, and the lab checks it). `speculative-bubble` is defined as
  a price `P_t` above the stated fundamental `F_t` by a stated gap, with `F_t` fixed by assumption (a definition, grade T
  conditional on A1-A2). `financial-panic` is defined in prose with no empirical claim. Episode content (the Dutch Republic,
  the 2008 panic) is book-level only, from `garber2000famous` for the early episodes, after the builder reads the book's
  table of contents or the cited passage (VERIFIER §2.1). Two-sided treatment: bubble-existence is contested. The fundamentals
  account (Garber) is registered; no counter-account key is registered (REFERENCE_REQUEST 4). Where the canon breaks: `F` is
  not observable; the constant-growth assumption fails for any non-constant dividend path.
- **L02** `gold-standard`, `debt-deflation`. Definitions in prose: gold-standard convertibility and parity (plain `<dfn>`
  with no `data-concept` for "parity" and "convertibility"). Derivation (grade T): for a fixed nominal debt `D` (A1) and a
  positive price level `P_t` (A2), the real debt is `D / P_t`; over one period the real burden multiplies by `P_0 / P_1`
  (exact). The lab computes this in integer cents for an illustrative path, labelled SIMULATED. `debt-deflation` is defined
  as the rise in real debt that a fall in `P` produces when `D` is fixed. Empirical claims about the interwar gold standard
  cite `eichengreen1992golden` at book level (title locator: "1919-1939", `references/references.json:7946`), grade C with
  the basis named, or are removed. Two-sided: the causal role of the gold standard is contested; the counter-evidence is
  REFERENCE_REQUEST 6 (no key registered). Where the canon breaks: a fixed `D` ignores default and renegotiation.
- **L03** `credit-channel-depression`, `lender-of-last-resort`. The credit channel is defined as a mechanism (grade T, in
  the stated model only): an external-finance premium that rises as bank balance sheets weaken, with a parameter in the lab
  (A1-A3). The lesson does not claim the channel's size. The monetary account of the Depression cites `friedman1963monetary`
  at book level (title locator: "1867-1960", `references/references.json:9399`), grade C, with the credit account named as
  the competing account and its key missing (B2). `lender-of-last-resort` is defined in prose as the central bank's
  lending to solvent but illiquid institutions against collateral (a definition, grade T conditional on the definition).
  **B2 blocks any empirical claim about the credit channel.** **The curriculum lab** (`lab-LX1-L03-1`, B1) is a stylised
  two-economy model: economy X holds parity; economy Y leaves it at a stated date; a deflation shock of stated size; output
  depth from the model's own equation. The lab prints the depth for each path. The interpretation says the ordering comes
  from the stated assumptions and says nothing about any historical economy. Where the canon breaks: the model has one good,
  no default, no fiscal response.
- **L04** `bretton-woods-system` (definition blocked on B3). The real-data lab (`lab-LX1-L04-1`) reads `fx_monthly.csv`
  (`data-files`), selects one column with no blank cells in the window (§6.2), computes the standard deviation of monthly log
  changes in two windows from the first MANIFEST month (January 1971) and from a later window stated on the page, and prints
  both with the rounding rule. The interpretation says the series shows dispersion, not cause. Spot rates only, as the
  `fx_monthly` note states (`tools/data_sources.yaml:62-64`). No date for the system's end is stated (B3). The definition
  of the system is taught only after B3 is resolved. Where the canon breaks: the series is spot-only and has no interest
  differential (the MANIFEST note), and the window choice matters.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one model limit and what changes without it.
- No lesson uses a term from outside the closure as a link. Outside-closure concepts are plain prose (§4).
- Each lesson has at least three misconceptions (BUILDER_RULES §4.2 item 6), a problem set of at least three problems in each
  of the Mechanics, Proof, Empirical and Research tiers with worked solutions in `<details class="solution">`, a key-results
  table, and an 8-15 item retrieval quiz with explanations (BUILDER_RULES §4.2 items 7-9).
- No debate brief: LX1 has no `debate` key (§0.1). The two-sided rule (BUILDER_RULES §1.5) applies to every contested claim
  anyway (§2.2).

---

## 4. DAG problems (concepts that natural LX1 content would use outside the closure)

Prerequisite closure of LX1 (computed): **{E1, E5, FC1, M1, M2, P0.1}**, with 74 usable concepts (§0.1). Owners below are from
`curriculum/curriculum.json` `concepts` (each entry's `module` field; line of the concept's key given).

| Ref | Concept | Owner (outside closure) | `curriculum.json` line | Where natural LX1 content would use it | Resolution in this plan |
|---|---|---|---|---|---|
| D1 | `bank-run` | SR1 | 1425 | the panic mechanism (L01, L03) | Plain prose; no link; no `data-concept`. |
| D2 | `fire-sale` | SR1 | 2797 | 2008 spread of distress (L01) | Plain prose. |
| D3 | `leverage-cycle` | SR2 | 3517 | the 2008 credit boom (L01) | Plain prose. |
| D4 | `banking-crisis`, `currency-crisis-models` | E9 | 1429, 2089 | crisis episodes (L01, L04) | Plain prose. |
| D5 | `covered-interest-parity`, `uncovered-interest-parity` | E8 | 2009, 5493 | capital mobility under a fixed rate (L04) | Plain prose; no parity formula is written. |
| D6 | `efficient-markets-hypothesis` | FC3 | 2465 | the bubble definition's test (L01) | Plain prose. Q10 asks whether FC3 should be a prerequisite. |
| D7 | `moral-hazard` | E2 | 3953 | deposit insurance and bailouts (L03) | Plain prose. |
| D8 | `fisher-relation` | CF1 | 2825 | real versus nominal rates under deflation (L02) | Avoided: §3 L02 computes `D / P_t` directly. If the real-rate story is used, plain prose, no link. |
| D9 | `bank-reserves`, `central-bank-balance-sheet` | FI4 | 1421, 1725 | the lender of last resort's balance sheet (L03, L04) | Plain prose. |
| D10 | `credit-default-swap`, `network-contagion` | CR2, SR3 | 2033, 4045 | 2008 contagion (L01) | Plain prose, names only. |
| D11 | `term-spread` | FI1 | 5345 | an optional current-condition signal (project) | Plain prose only if the student uses it; not in any lab. |
| D12 | `crisis-mechanism-map` | GM5 | 2045 | a comparison map (project) | Not used. |
| D13 | `expectation` | M4 | 2625 | expected inflation in L02 (if used) | Plain prose; the `\E` macro is not used (§2.3). Q2. |
| D14 | `fx-market-structure` | X1 | 2949 | the FX regime (L04) | Plain prose, no market-structure claim. |
| D15 | `sovereign-default-model` | E9 | 5085 | sovereign defaults in the gold-standard era (L02) | Plain prose, no model. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Q2 and Q10 ask the architect to confirm the defaults.**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring); an unlinked use of D1-D15 passes the tool, so the
verifier reads every lesson for these names (VERIFIER §2.9).

---

## 5. Project (`project.html`, Builder E): rubric-graded, ladder, spec, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order, line 33)

1. **Rung 1, worked example** (`lab-LX1-project-1`, SIMULATED): one fully solved, annotated computation of the real-debt burden
   of a fixed nominal debt over an illustrative five-period price path, followed by one comparison of the two paths. Each
   step has a "why" annotation. Full length (tier U; BLUEPRINT §4 minimum applies from tier M).
2. **Rung 2, completion** (`lab-LX1-project-2`, `class="lab completion"`, SIMULATED): the real-debt line and the burden-change
   line are removed (`___`). Graded instantly. Its twin is the completed solution; every page line equals the twin line or
   contains a blank (`tools/run_labs.py` docstring). `check_projects.py` requires a completion lab or a quiz (line 90).
3. **Rung 3, independent project** (graded by rubric): "Then vs. now", a two-page essay on one historical episode and one
   current market condition, with a mechanism-level comparison (§5.2). `lab-LX1-project-3` is the rung-3 check: it recomputes,
   from `fx_monthly.csv`, the dispersion figures that a Level 4 essay may quote, and prints the table with the rounding rule.
4. **Rung 4, stretch** (optional, not graded): a third episode, or a test of one claim in the essay on the embedded `fx_monthly`
   series (spot-only, as its note states), with the test's window and its limitation stated.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A student must write a two-page comparison of one historical episode and one current market condition, showing
  where the analogy holds and where it breaks, with the mechanism stated at each step. Every claim is cited.
- **Inputs.**
  1. The student's chosen episode and current condition. The student selects both (no list is supplied by the page).
  2. Sources for each claim, each with a DOI, an ISBN or the issuer's URL, and a locator (page, table or section).
  3. Optional: `fx_monthly` (MANIFEST id `fx_monthly`, columns and blanks in §6.2), for one spot-rate test in rung 4 or in
     the rung-3 check.
  4. The worked example and the completion problem use SIMULATED paths only (§6.1).
- **Required outputs.** One file `essay.md` (or a printed PDF) of two pages, and the exemplar-style self-assessment form
  (§5.4). The essay states, for each episode and for the current condition: the mechanism as a chain of at least three steps,
  the step where the analogy fails and the evidence for the failure, and each computed number with its formula and rounding rule.
  "Two pages" is the length rule Q5 proposes (the tools do not check length).
- **Constraints.**
  - Every computed number is computed from unrounded values, with the rounding rule stated.
  - Every claim about a dataset is limited to its MANIFEST note (for `fx_monthly`: spot rates only, last noon rate of the month).
  - No claim about a source beyond its locator; a claim graded B or C names its counter-evidence.
  - No claim about an episode's date or outcome without a locator in a source the student has read.
  - Standard library or any tool the student chooses; the rubric does not depend on the tool.
- **Grading.** Rubric (§5.4). The grading entry names the rubric (`GRADING_WORDS`, `check_projects.py` line 38 requires the word
  "rubric"). Adversarial question bank: not required (Q6).
- **Reading list** (registry keys only, §7.1): `friedman1963monetary`, `eichengreen1992golden`, `garber2000famous`, and
  `reinhart2009this` (optional, book-level, with the student's own locator).

### 5.3 Time budget (`<table id="hours">`, sums to 10 h; every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 1 | One solved SIMULATED path, annotated line by line |
| Rung 2, completion problem | 1 | Fill the two blanks, then run the instant check |
| Episode and condition selection, and sourcing with locators | 2 | Choose two episodes, find two locators per claim |
| Mechanism outline (chains of at least three steps, failure step) | 1.5 | One chain per episode, the failure step named |
| Drafting the two-page essay | 2.5 | Two pages, every claim cited, every number with its rule |
| Self-assessment against exemplars | 2 | Score the essay with the rubric, compare with exemplar-a and exemplar-b |
| **Total** | **10** | Equals `data-hours-project` on the hub |

Estimates are the planner's. Verifier estimates within 30% fail (VERIFIER §2.6, "Hours").

### 5.4 Rubric (`table.rubric#rubric`; `check_projects.py` `rubric_problems`, lines 58-73)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to 1
(the tool counts `td` cells). Every level descriptor is observable.

1. **Episode and condition.** L4: names both episodes and the condition with dates, and cites a locator for each date. L3:
   names both with dates and one locator each. L2: names both; a date or a locator is missing for one. L1: "picks two events".
2. **Mechanism comparison.** L4: states each mechanism as a chain of at least three steps and names the first step where the
   analogy fails, with the evidence for the failure. L3: two chains of three steps; the failure step is named without evidence.
   L2: lists similarities and one difference, no chain. L1: "discusses similarities".
3. **Evidence and citation.** L4: every factual claim carries a citation with a locator (page, table or section) or is marked as
   the student's own inference; every B- or C-graded claim names counter-evidence. L3: every claim cited, at most two without
   a locator, counter-evidence named for at least one claim. L2: most claims cited; no counter-evidence named. L1: "some sources
   listed".
4. **Quantitative check.** L4: each computed number comes from unrounded values, states its rounding rule, and cites the formula
   (a lab line or a derivation). L3: unrounded values and a rule for every number but one. L2: rounds before computing, or
   states no rule. L1: "rounds the numbers".
5. **Limits and scope.** L4: names at least two limits of the analogy and, for each, the evidence that would test it. L3: names
   two limits, one with a test. L2: names one limit. L1: "notes some caveats".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written essays on one episode pair,
annotated with the descriptors each passage meets or misses. The pair must differ from the worked example's pair. Self-assessment
form (`section.rubric-self`, `data-rubric="rubric"`, `data-exemplars="exemplar-a exemplar-b"`, as in E5 and M1). The page shows
where the student's scores diverge from the exemplar scores. Calibration: the verifier scores both exemplars blind, within one
level per criterion (VERIFIER §2.6).

**Autograder analogue.** LX1 is rubric-only (`curriculum/06-profession-capstone.yaml:49`). No grader, no mutants and no five
alternative implementations are written. The requirement for ten student-error mutants and five alternative correct
implementations applies to graders (fixer-rules line 19, architect rulings 9-10). The planner's analogue, for the verifier's
calibration only: **ten student-error patterns** the rubric must catch, and **five alternative correct essay designs**.
- Student errors: (1) real debt computed as nominal debt, with no division by `P`; (2) a percent change with no base or
  direction; (3) "bubble" used for any price rise, with no fundamental stated; (4) a citation whose locator does not contain the
  claim; (5) an analogy asserted to hold, with no failure step; (6) numbers rounded before computing; (7) a causal gold-standard
  claim stated as an empirical finding with no source; (8) a current-condition number with no source; (9) a rung-2 blank filled
  with a number from memory; (10) an episode date stated with no locator.
- Five alternative correct designs (categories only; the planner asserts no fact about any episode): (a) an interwar
  convertibility episode against a current peg under stress; (b) a nineteenth-century banking panic against a current run on a
  wholesale funding market; (c) an early speculative episode against a later asset boom; (d) the fixed-rate period against a
  current fixed-rate regime; (e) the credit channel of the 1930s against a modern credit-tightening episode. Each must reach
  Level 4 on criterion 2 to be a correct alternative.

---

## 6. Real-data policy

### 6.1 Embedded and not embedded

- **Embedded, redistributable (grant quoted):** `fx_monthly` (Federal Reserve H.10, spot rates, USD per unit of foreign
  currency). Quoted public-domain grant: `tools/data_sources.yaml:57-60` (the `licence` text and `licence_url`); the
  `note` (spot only; last noon rate of the month; EUR starts 1999): `tools/data_sources.yaml:62-64`. MANIFEST entry: id at
  `course/assets/data/market/MANIFEST.json:32`, first month `"1971-01"` at line 58, last `"2026-09"`, 669 rows, columns AUD,
  CAD, CHF, DKK, EUR, GBP, JPY, NOK, NZD, SEK. The file exists on disk: `course/assets/data/market/fx_monthly.csv`.
- **Embedded, not relevant to LX1:** `fx_daily` (2000-01-03 onward) and `ust_daily` (2000-01-03 onward; `tbill_3m` and
  `cmt_10y`). Neither covers the interwar years. Not used.
- **Not embedded, no grant found:** historical gold reserves, interwar price levels, output, unemployment, bank failures.
  No entry exists in `tools/data_sources.yaml` for them, and `rejected:` lists only the French library and Open Source Asset
  Pricing (lines 119-135). **Not embedded.** The L03 curriculum lab is SIMULATED (B1).
- **Honest-pending note** on L03 and on the project's data-inputs section: "The curriculum names embedded data for this lab. No
  redistributable historical series for gold adherence or output depth is embedded yet. The lab uses a stylised model labelled
  SIMULATED." Cited to the DATA_REQUEST in §7.2.

### 6.2 The `fx_monthly` columns (planner count, inline check of `course/assets/data/market/fx_monthly.csv`)

- 669 data rows, first month `1971-01`, last month `2026-09`.
- Blank cells: **EUR has 336 blanks** (the months before 1999; the euro's start, `tools/data_sources.yaml:63`).
- **No blank cells** in AUD, CAD, CHF, DKK, GBP, JPY, NOK, NZD, SEK over 669 rows (planner count). The L04 lab uses GBP or
  JPY (builder's choice, stated on the page). A blank in the chosen column raises (§2.1 item 12); EUR is not used before 1999.
- Published values are kept as text in the CSV (MANIFEST transform); the lab parses each used value as a decimal and fails on any
  other text.

### 6.3 Data requests (no source named by the planner)

See §7.2, DATA_REQUEST D-1. The planner does not name an issuer, a series or a licence from memory.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`)

| Key | Record (as read) | Status | Use in LX1 |
|---|---|---|---|
| `friedman1963monetary` | Open Library record, "A monetary history of the United States 1867-1960", Friedman, year 1963, ISBN 0691041474 (`references/references.json:9399`); `used_by: ["LX1"]`; `source_strings` matches the curriculum's first author and year | verified | L03 monetary account (book level, grade C with the credit account named as competing and not yet registered). **N2:** the record lists Friedman only; cite the key only. |
| `eichengreen1992golden` | Open Library record, "Golden fetters: the gold standard and the Great Depression, 1919-1939", Eichengreen, year 1992, ISBN 0195064313 (`references/references.json:7946`); `used_by: ["LX1"]`; matches `curriculum/06-profession-capstone.yaml:39` | verified | L02 and L03 interwar gold-standard claims (book level; grade C with the basis named); reading list |
| `garber2000famous` | Crossref record, "Famous First Bubbles: The Fundamentals of Early Manias", Garber, year 2000, DOI `10.7551/mitpress/2958.001.0001` (`references/references.json:9667`); `used_by: ["LX1"]`; matches `curriculum/06-profession-capstone.yaml:40` | verified | L01 early-episode content (book level, after the builder reads the cited passage); reading list |
| `reinhart2009this` | Crossref record, "This Time Is Different: Eight Centuries of Financial Folly", Reinhart and Rogoff, year 2009 (`references/references.json:19643`); `used_by: ["E9"]` | verified | optional, reading list only; any claim it supports is book level, and its counter-evidence is `herndon2013high` only for a debt-growth claim (`references/references.json:12402`), which LX1 does not plan to make |

Optional, not planned: `diamond1983bank` (`references/references.json:6773`, bank runs, `used_by: ["SR1"]`), and
`gorton2012securitized` (`references/references.json:10783`, `used_by: ["SR1"]`). Using either requires the two-sided treatment
the page cannot yet supply (B2 and REFERENCE_REQUEST 4); they are not used by default.

Not to be used by LX1: `mishkin2021economics` (FC1), `gali2015monetary` and `clarida1999science` (E6), and any key whose `used_by`
is another module without the architect's approval.

### 7.2 REFERENCE_REQUESTS and DATA_REQUESTS (for the architect; lead only, no bibliographic record typed)

REFERENCE_REQUESTS:
1. `{doi: null, authors: "Kindleberger & Aliber (lead only)", year: "2015 (lead only)", title: "Manias, Panics, and Crashes, 7th ed. (lead only)", venue: "book (lead only)", needed_for: "L01 speculative-bubble and financial-panic attribution (curriculum source string yaml:36)", confidence: "the curriculum string exists (curriculum/06-profession-capstone.yaml:36); the review queue records 'no candidate established identity' (references/review_queue.json:1557). The candidate DOI 10.1007/978-1-137-52574-1 lists first author Aliber and is not admitted."}`
2. `{doi: null, authors: "Bernanke (lead only)", year: "1983 (lead only)", title: "Nonmonetary Effects of the Financial Crisis in the Propagation of the Great Depression (lead only)", venue: "American Economic Review, volume 73, issue 3 (lead only; record not typed)", needed_for: "L03 empirical credit-channel claim (B2)", confidence: "the curriculum string exists (yaml:38). The review queue candidate (DOI 10.3386/w1054) is an NBER working paper with a different venue (review_queue.json:1610); it must not be admitted as the AER article."}`
3. `{doi: null, authors: "not typed (topic only)", year: "not typed", title: "a primary or survey source for the Bretton Woods system's definition and its end", venue: "not typed", needed_for: "L04 definition of bretton-woods-system and any dated end claim (B3)", confidence: "the need is certain; no record is identified by this planner. Candidate sources must come from an allow-listed issuer domain (references/authorities.yaml) or a publisher's stable URL."}`
4. `{doi: null, authors: "not typed (topic only)", year: "not typed", title: "empirical evidence on the fundamentals versus non-fundamental account of historical bubbles", venue: "not typed", needed_for: "L01 two-sided treatment of the bubble claim (BUILDER_RULES §1.5)", confidence: "the need is certain; no record identified by the planner."}`
5. `{doi: null, authors: "not typed (topic only)", year: "not typed", title: "the monetary versus credit-channel debate on the Great Depression, with the credit account's empirical evidence", venue: "not typed", needed_for: "L03 counter-evidence to friedman1963monetary and the credit-channel claim (BUILDER_RULES §1.5)", confidence: "the need is certain; no record identified by the planner. B2 is the main case."}`
6. `{doi: null, authors: "not typed (topic only)", year: "not typed", title: "empirical evidence on the causal role of the gold standard in the interwar depression", venue: "not typed", needed_for: "L02 and L03 counter-evidence to any causal gold-standard claim", confidence: "the need is certain; no record identified by the planner."}`

DATA_REQUESTS:
- D-1 `{source_url: "not identified", series_id: "not identified", license: "not read", transform: "not defined", needed_for: "L03 curriculum lab, if the architect wants real historical data (B1). The planner names no issuer from memory; the source must have its redistribution grant quoted from its page (BUILDER_RULES §6.6, steps 1-2)."}`

The architect resolves REFERENCE_REQUESTS through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page;
BUILDER_RULES §2.4). Until resolved, L01-L04 teach models by derivation and make no empirical attribution. Each empirical
sentence is graded C at most, with its basis named, or is removed.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for LX1 (`curriculum/06-profession-capstone.yaml:19-49` has no `atlas:` key;
no Atlas entry names LX1, §0.1). No `atlas/LX1.contract.md` is needed, and no contract is drafted here. The studio STUDIO-LX
requires LX1 (`curriculum/06-profession-capstone.yaml:8`); that requirement does not create an Atlas milestone.

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/LX/LX1/cards.json`, ids `LX1-c001` upward, `lesson` in L01-L04, one card per definition (the 7 concepts),
  each derivation (the fundamental value, the real-debt identity, the L03 model's ordering as a model result), each key
  result, and each misconception (BUILDER_RULES §7). `check_pages.py` `check_cards` checks the id prefix, the lesson existence,
  the grades and the registry keys.
- Grade T for every derived result, with `"basis"` naming the lab or derivation that establishes it, for example
  `"basis": "Lab 2 (SIMULATED, exact in integer cents)"`.
- Cite a registry key only for an empirical or attributed claim (§7.1). `cite` is `[]` where the card is a model or a definition.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`. Cards for the L04 result name `Lab 4 (fx_monthly, MANIFEST
  retrieved 2026-10-19)`; the `retrieved` date is at `course/assets/data/market/MANIFEST.json`.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit LX1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit LX1
.venv/bin/python tools/check_projects.py --unit LX1
.venv/bin/python tools/run_labs.py --unit LX1               # --page L04 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/LX/LX1/L01.html                          # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/LX/LX1/L02.html --refresh lab-LX1-L02-1  # after editing a twin
.venv/bin/ruff check tests/labs/LX1 && .venv/bin/ruff format --check tests/labs/LX1
.venv/bin/mypy tests/labs/LX1                                # strict, repository configuration
```

Not run for LX1:
- `tools/run_graders.py --unit LX1` is not needed: LX1 has no autograder (`curriculum/06-profession-capstone.yaml:49`), so the
  tool prints "no autograder" for it (the same rule E5 relies on, `tools/run_graders.py` lines 138-139).
- `tools/mutate_graders.py` is not needed (no autograder).

Verifier only, on a quiet machine: `.venv/bin/python tools/page_smoke.py --unit LX1` (not run by builders; timing-sensitive),
`.venv/bin/python tools/verify_refs.py --unit LX1` (the unit ledger's run, VERIFIER §2.1), and
`.venv/bin/python tools/fetch_data.py --check` (offline; confirms the `fx_monthly` snapshot and its MANIFEST entry, which L04
reads, match).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md.

Flag checks: `tools/check_pages.py`, `tools/check_dag.py` and `tools/check_projects.py` accept `--unit`; `tools/run_labs.py`
accepts `--unit` and `--page`; `tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`. The planner did not execute the
builder commands; only the coursekit closure, concept-owner and built-unit functions were run (§0.1), plus the inline reads in §6.

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No `atlas:` key on LX1 (`curriculum/06-profession-capstone.yaml:19-49`). `check_projects.py` skips the
   contract check (line 144-146). No `atlas/LX1.contract.md` is needed.
2. **No debate.** LX1 has no `debate:` key, so `check_pages.py` does not require a debate brief. The two-sided rule still applies
   (BUILDER_RULES §1.5).
3. **Built prerequisites.** FC1 and E5 are built (`course/modules/FC/FC1/index.html`, `course/modules/E/E5/index.html`), so the
   hub may link them. P0.1 is unbuilt (coursekit `built_units()`), so its concepts are linked only through `concepts.html`
   anchors. Q9 asks the architect to confirm.
4. **Rung 2 must be graded instantly.** `check_projects.py` accepts a completion lab or a quiz (line 90). The plan uses a
   completion lab.
5. **One curriculum lab, four required.** The curriculum names one lab (`curriculum/06-profession-capstone.yaml:41`).
   BUILDER_RULES §3.4 requires a numerical check per key formula; the plan adds one lab per lesson (E5 precedent, §1).
6. **check_dag sees linked uses only.** Unlinked uses of D1-D15 (§4) pass the tool; the verifier reads for them.
7. **Rubric-only grading.** No grader, no mutants. `check_projects.py` requires the rubric and two exemplars at two levels
   (`rubric_problems`, lines 58-73), and the spec's grading entry must name "rubric" (`GRADING_WORDS`, line 38).
8. **The "two pages" length rule is not checked by any tool.** The rubric and the verifier check it by hand (Q5).
9. **fx_monthly blanks.** EUR has 336 blank cells before 1999 (§6.2). A lab that reads EUR without a guard fails at run time, by design.

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Lesson count and ownership.** Confirm 4 lessons × 10 h, project 10 h (20%), one lesson per builder (A to D), the project to E,
   cards to F. **RECOMMENDED:** this split. Alternative within the rules: 5 lessons × 8 h with the project at 10 h. Three lessons per
   builder would leave builders without a lesson.
2. **D13 `expectation` and expected inflation.** Plain prose, no link (E1 and E5 precedent). **RECOMMENDED:** plain prose; the
   `\E` macro is not used. Alternative: add M4 as a prerequisite (a curriculum change).
3. **Outside-closure concepts (§4, D1-D15).** Confirm plain prose with no link and no `data-concept`. **RECOMMENDED:** confirm.
   No prerequisite change.
4. **B1, the curriculum lab's data.** The lab is SIMULATED with an honest-pending note and DATA_REQUEST D-1. **RECOMMENDED:** this default.
   Alternative: a redistributable historical source is read, its grant quoted, and added to `tools/data_sources.yaml` first.
   **BLOCKING for L03.**
5. **Project length.** "Two pages" with no tool check. **RECOMMENDED:** keep the length rule, and state it on the page as "two printed
   pages at the page's default type size". The tools do not measure it.
6. **Adversarial?** The project is an essay, not an IC defence or debate. No 15-angle question bank. **RECOMMENDED:** confirm, not
   adversarial.
7. **Current-condition sourcing (N4).** The student may cite any source that carries a DOI, an ISBN or an issuer URL with a
   locator, not only registry keys. **RECOMMENDED:** this, because no registry source covers current conditions, and the rubric
   rewards locators (criterion 3). The reading list stays registry-only.
8. **B2, the credit-channel claim.** L03 teaches the mechanism as a model and makes no empirical attribution until the AER article is
   admitted or a different key is chosen. **RECOMMENDED:** this default; the architect resolves REFERENCE_REQUEST 2 through
   `tools/add_reference.py`. The NBER working paper is not admitted in its place.
9. **B3, Bretton Woods.** L04's definition and any end date wait for REFERENCE_REQUEST 3. The L04 lab does not wait. **RECOMMENDED:**
   this. Until then, the L04 page states only the lab's facts and the first MANIFEST month.
10. **FC3 as a prerequisite.** The bubble definition's test (`efficient-markets-hypothesis`, D6) is plain prose. **RECOMMENDED:** no
    change. Alternative: add FC3 to LX1's prerequisites (a curriculum change; FC3 is outside the closure).
11. **Friedman & Schwartz author field (N2).** Cite the key only; do not type the second author. **RECOMMENDED:** this. The architect
    may correct the registry record through `tools/add_reference.py`; the planner did not edit it.
12. **Notation.** Local symbols only (§2.3); avoid `T`, `R_f`, `\mathbb{Q}`. **RECOMMENDED:** confirm; no NOTATION_REQUESTS.
13. **Figures.** No live figures and no new kernel. **RECOMMENDED:** confirm (BUILDER_RULES §6.4 would need a kernel and a test).
14. **Glossary.** Terms outside the 7 concepts (nominal and real debt, deflation, convertibility, parity, fundamental value, bank run,
    central bank) are plain `<dfn>` with no `data-concept`. **RECOMMENDED:** confirm; no GLOSSARY_REQUESTS.
15. **Hub links to built prerequisites (§11 item 3).** **RECOMMENDED:** link `../../FC/FC1/index.html` and `../../E/E5/index.html` from
    the hub's prerequisite list; P0.1 through `concepts.html` anchors only.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 (includes the lab of L02), L03 (the curriculum lab, B1 and B2
   wording), L04 (the real-data lab and its blank-cell guard), project (rubric and exemplar calibration, blind scoring), and the
   cards (sampled). Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/LX1.verification.json`; verifier scripts archived under `ledgers/LX1/scripts/` (VERIFIER §3). No
   `ledgers/LX1/mutants/` (rubric-only).
4. The branch merges only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B3 must be resolved or
   named as honest gaps first.

Architect decisions: pending (§12). This plan is the planner's proposal.

## Architect decisions

Pending. Each entry in §12 carries the planner's RECOMMENDED decision; the architect confirms or replaces each one before the
builders start.

## Architect decisions (2026-11-03, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank. plans/FINAL-ARCHITECT-RULINGS.md and ~/.fanout/fixer-rules.md bind every builder. No reference is admitted in this batch: a statement whose source is a REFERENCE_REQUEST is not made, or it is taught as a model result with no attribution.
Module specifics: 4 lessons x 10 h + 10 h rubric project; one lesson per builder. L03 uses a SIMULATED stylised model with an honest-pending note and a DATA_REQUEST; no empirical credit-channel citation; the Bretton Woods definition and end date wait for a request.
