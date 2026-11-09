# PC1 build plan: Research Writing & Presentation (planner draft, 2026-11-09)

Unit: **PC1 · Research Writing & Presentation** · tier U · 30 h · prerequisites P0.1, S0 · no Atlas milestone · no debate key ·
grading `rubric` (no autograder) · output directory `course/modules/PC/PC1/` (part code `PC`) · lab twins `tests/labs/PC1/` ·
cards `course/modules/PC/PC1/cards.json` · studio STUDIO-PC (PC1 is a member; the studio requires PC2 only).
Planner: Haiku, plan only. No lesson text, no git operations, no commits. Only this file was written.
Executors: Haiku builders, then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement cites `file:line` (or the JSON line) read during planning. Anything not in the
curriculum is marked **NOT IN CURRICULUM**. Tool behaviour cites the tool source line that was read. Closure and owner
computations were run through `tools/coursekit.py` with `.venv/bin/python -I`. No file other than this plan was read as a source of
bibliographic fact; no bibliographic fact is typed from memory.

Binding inputs read in full for this plan: `BLUEPRINT.md`, `BUILDER_RULES.md`, `VERIFIER_RULES.md`, `references/SEED_REPORT.md`,
`/Users/billyribeiro/.fanout/fixer-rules.md`, `plans/FINAL-ARCHITECT-RULINGS.md`, `plans/E5-build-plan.md` (structure template).
Precedents read: `plans/PC3-build-plan.md` §0.2 and its architect decisions (line 633), `plans/AC2-build-plan.md` (ownership table, lines 45-66).

**Status: BLOCKING ISSUE B1 exists (§0.3). Everything else is feasible. No dataset is needed.** The architect confirms the default
for B1 before the builders start.

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part PC, code `PC`, title "Professional Craft", order 23; STUDIO-PC; its module list places PC1 (`yaml:105`), PC2 (`yaml:130`), PC3 (`yaml:157`) | `curriculum/06-profession-capstone.yaml:88-92` (part and studio header) |
| PC1 id `PC1`, title "Research Writing & Presentation", tier `U` | `curriculum/06-profession-capstone.yaml:105-107`; `curriculum/curriculum.json:11411-11413` |
| Hours `30` | `curriculum/06-profession-capstone.yaml:108`; `curriculum.json:11414` |
| Prereqs `[P0.1, S0]` (only) | `curriculum/06-profession-capstone.yaml:109`; `curriculum.json:11415-11418` |
| Core: "Writing a finance paper (structure, introductions that state the result, tables that stand alone), slides, presenting to an expert audience." | `curriculum/06-profession-capstone.yaml:110-112` |
| `introduces` has 5 concepts: `research-paper-structure`, `results-first-introduction`, `standalone-table`, `figure-redesign`, `expert-presentation` | `curriculum/06-profession-capstone.yaml:113-118`; `curriculum.json:11420-11426` |
| Sources (two free-text strings): "Cochrane (2005), 'Writing Tips for Ph.D. Students' (note)"; "McCloskey, Economical Writing, 3rd ed. (2019)" | `curriculum/06-profession-capstone.yaml:119-121`; `curriculum.json:11427-11430` |
| Lab: "Table and figure redesign drill." (singular) | `curriculum/06-profession-capstone.yaml:122`; `curriculum.json:11431` |
| Project "Rewrite a weak paper introduction". Brief: "Rewrite three supplied weak introductions to the Cochrane standard, and annotate every change." | `curriculum/06-profession-capstone.yaml:123-127`; `curriculum.json:11432-11434` |
| Deliverable "Rewrites plus annotations."; grading `rubric` | `curriculum/06-profession-capstone.yaml:128-129`; `curriculum.json:11435-11436` |
| No `debate:` key on PC1 | `curriculum/06-profession-capstone.yaml:105-129` (absent) |
| No `atlas:` key on the PC1 project; no entry of the `atlas` array names PC1 (the 20 entries name CS1, CS3, S0, S4, FI1, DV4, F1, S7, QR2, MS3, PR2, PR4, FI3, CR1, AC2, CF4, QR3, GM1, SR3, GM4) | `curriculum/curriculum.json` `atlas` array (computed with `coursekit`, planner) |
| PC1 is required by the bachelor's credential only (BS-FIN) | `curriculum/meta.yaml:58-63` (requires list, PC1 at line 63); computed credential scan |
| PC1 is the course "Business Communication" in the Quantitative & business core group | `curriculum/meta.yaml:75` |
| Topological position 19 of 134 | `curriculum/curriculum.json` `topological_order` (computed) |
| JSON row agrees with YAML (hours, prereqs, five concepts, lab, rubric) | `curriculum/curriculum.json:11411-11437` |
| The five PC1 concepts are owned by PC1 (computed by `coursekit.concept_owner`); line refs | `curriculum.json:2649` (expert-presentation), `:2753` (figure-redesign), `:4773` (research-paper-structure), `:4789` (results-first-introduction), `:5161` (standalone-table) |
| PC2 requires PC1 (downstream; PC2 must not be used by PC1 content) | `curriculum/06-profession-capstone.yaml:134` |

### 0.2 Prerequisite closure, built status, nearest built precedent

Closure computed by `tools/coursekit.py` `prerequisite_closure("PC1")` (function at `tools/coursekit.py:239-249`), run through
`.venv/bin/python -I`: **{CS1, P0.1, S0}**. Usable concepts (the closure's `introduces`): P0.1 has 11 (`curriculum/01-foundations.yaml:6`;
concept list in the P0.1 module object near `curriculum.json:6231`), CS1 has 12 (`01-foundations.yaml:383`), S0 has 10 (`01-foundations.yaml:587`).
Total **33 usable concepts**.

Built status (`coursekit.built_units()`): **none of CS1, P0.1, S0 is built**. `course/modules/` has no `P0`, no `CS/CS1`, and only `S7` under `S`.
Plans exist for all three (`plans/CS1-build-plan.md`, `plans/P0.1-build-plan.md`, `plans/S0-build-plan.md`).

So PC1 has **no built prerequisite**. Nearest built precedent, by the PC3 method (`plans/PC3-build-plan.md` §0.2: the built unit whose
closure contains the most closure members, ties by smaller closure): AC2, S7 and AP1 each contain all three PC1 closure members
(closure size 10 for AC2 and S7). **AC2** is adopted as the content-free precedent because it has S0 as a direct prerequisite
(`plans/AC2-build-plan.md` header and ownership table, lines 45-66). The same-part built sibling **PC3** (`course/modules/PC/PC3/`,
`ledgers/PC3.verification.json`, verdict PASS) is adopted for the PC-part layout. Per BUILDER_RULES §4.1, `course/modules/S/S7/` is the
reference instance of every template and is read by every builder. No prerequisite plan supplies content for PC1.

### 0.3 Blocking issues (architect decision required before builders start)

**B1 (BLOCKING). The project brief names a standard that the curriculum does not define and that has no registry source.**
- The brief says "to the Cochrane standard" (`curriculum/06-profession-capstone.yaml:125-127`; `curriculum.json:11432-11434`).
  The curriculum names no content of that standard. The source string "Cochrane (2005), 'Writing Tips for Ph.D. Students' (note)"
  (`yaml:120`; `json:11428`) has **no registry record**: `references/review_queue.json:1672` "no candidate established identity";
  `references/SEED_REPORT.md:55` lists it as used by PC1 and in the review queue.
- The three candidate DOIs in the review queue for that string are different works (Soil Science 2005; NBER working paper w11193
  "Financial Markets and the Real Economy"; ITNOW "software developer"; `review_queue.json:1680-1716`). **None may be admitted.**
- The admission path of `references/authorities.yaml` allows issuer and publisher pages on listed domains only. No listed domain
  hosts a personal writing note. The note cannot be admitted by the builders, and the planner did not read it.
- A student cannot finish the project "without asking a clarifying question" (BUILDER_RULES §5.2) while the standard is undefined.
- **Recommended decision (default in this plan):** the project page defines the standard itself. Its five rubric criteria (§5.4) and
  the module's own rules (L02) are the standard, and no author is cited for it. The architect amends the brief at
  `curriculum/06-profession-capstone.yaml:125-127` to read "to the standard stated in the specification" (a curriculum change; builders
  never edit `curriculum/*.yaml`). The source string at `yaml:120` stays in the curriculum as a REFERENCE_REQUEST (§7.2).

**Non-blocking, but the architect should see them:**

- **B2. McCloskey, *Economical Writing*, 3rd ed. (2019) (`yaml:121`).** No registry record. The review queue lists one candidate that
  matches the title, first author and year: DOI `10.7208/chicago/9780226448107.001.0001` (`references/review_queue.json:1725` entry, first
  candidate). This is a **lead only**. `tools/add_reference.py` must confirm it against the citation string (BLUEPRINT §3; BUILDER_RULES
  §2.4). **Trap:** `references/references.json:720` (`andrews2023inference`, "Andrews, Kitagawa & McCloskey") has the family name
  McCloskey (line 736). It is a different work. A builder must not match "McCloskey" by family name. Until the record is admitted,
  no PC1 page cites McCloskey, and the lessons teach without it.
- **B3. Coverage gap.** The rung-3 project grades introductions only (`yaml:124-128`). The core names slides and presenting
  (`yaml:111-112`), and the lab names tables and figures (`yaml:122`). `standalone-table`, `figure-redesign` and `expert-presentation`
  are therefore taught and quizzed but **not graded by the rung-3 project**. The plan keeps rung 3 exactly to the curriculum scope
  (VERIFIER_RULES §2.6). Optional rung 4 covers slides and tables (§5.1). Architect decides whether to add a graded deliverable
  (curriculum change). See §12 Q8.
- **B4. P0.1 hours conflict.** `plans/P0.1-build-plan.md` ("BLOCKING CONFLICT") shows P0.1's 6 h cannot satisfy the page hour rules.
  PC1 links only to P0.1 concept ids, which do not change if P0.1's hours are revised. No PC1 change follows, but the P0.1 page must exist
  before `concepts.html` anchors resolve.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

**4 lessons × 6 h = 24 h; project 6 h; total 30 h.** Each lesson sits at the 6 h floor of `tools/check_pages.py` (`check_lesson`, line
228: lessons are 6–12 study hours). The project is 6 of 30 h = **20%**, inside the 10–40% band (`check_pages.py:339-340`, 3 to 12 h).
Hub split: `data-hours-lessons="24"`, `data-hours-project="6"` (`check_pages.py:337-342`). Concept counts per row sum to 1+1+2+1 = **5**,
each concept in exactly one row (`curriculum/06-profession-capstone.yaml:113-118`).

| Lesson | Title (working) | Concepts it defines (`introduces`) | Lab (twin id, `tests/labs/PC1/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Structure of a finance paper | `research-paper-structure` | `lab-PC1-L01-1`: section-budget and first-number checker on a SIMULATED outline (exact integers) | 6 | Builder A |
| L02 | An introduction that states the result | `results-first-introduction` | `lab-PC1-L02-1`: a result sentence built from an unrounded SIMULATED estimate in `Fraction`, with the rounding rule printed | 6 | Builder B |
| L03 | A table that stands alone; figure redesign | `standalone-table`, `figure-redesign` | `lab-PC1-L03-1`: the **curriculum lab** (`yaml:122`): a standalone-table checklist on a SIMULATED regression table, plus the truncated-axis ratio of a bar pair (`misleading-chart`, S0) in `Fraction` | 6 | Builder C |
| L04 | Presenting to an expert audience | `expert-presentation` | `lab-PC1-L04-1`: a 20-minute slot budget in `Fraction` (slides and question reserve), table printed | 6 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 24/6 | none | none | - | Builder A |
| project | Rewrite a weak paper introduction (`rubric`, §5) | none | `lab-PC1-project-1` (rung 1), `lab-PC1-project-2` (rung 2, `class="lab completion"`), `lab-PC1-project-3` (rung 3 self-check) | 6 | Builder E |
| cards | `cards.json` from L01-L04 | none | none | - | Builder F (after A-E) |

**Deviation from the brief, flagged.** The orchestrator's rule of "about three lessons per builder" does not fit a 4-lesson, 30 h unit.
The plan gives one lesson per builder so that builders A to D each own one lesson, and Builder E owns the project. The alternative
(two lesson builders with two lessons each, A: L01-L02 plus index, B: L03-L04, and E for the project) is open question Q4.

**Ownership rule.** Each builder writes only its own lesson page, its own twin(s) and its own `embed_labs` output. Builder A also writes
`index.html` after L01 exists. Builder E writes `project.html`, the project labs, the rubric and the exemplars.

**Execution order (links run backward only).** A, then B, then C, then D, then E, then F. Each lesson links to the definitions of the
lessons before it (§3). The project links to the lesson definitions (§5), so E starts after D. Builder F runs last.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses only closure concepts: `paper-anatomy`, `identification`, `robustness-check`, `replication` (P0.1).
- L02 uses L01 (`research-paper-structure`) and P0.1 `evidence-grade`, `identification`.
- L03 uses L01 and L02 (`results-first-introduction`, for the table title that states the finding), and S0 `misleading-chart`,
  `graphical-perception`, `anscombes-quartet`, `empirical-distribution`.
- L04 uses L02 and L03, and P0.1 `steelmanning`, `replication`, `project-ladder`.

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to PC1)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, `plans/E5-build-plan.md` §2 (binding carried-over
lessons), `plans/FINAL-ARCHITECT-RULINGS.md`, `plans/PC3-build-plan.md` (its architect decisions, line 633), this file. Study
`course/modules/S/S7/` (reference instance of every template) and `course/modules/PC/PC3/` (same-part layout). `course/templates/`
holds `hub.html`, `lesson.html`, `project.html`, `studio.html`. Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded only at
   display. A page that shows a rounded figure states its rounding rule (`fixer-rules.md` line 6).
   For PC1 this covers the result sentence in L02 and the lab outputs. Percent changes state the base and the direction.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what
   the printed numbers show. A lab that counts formatting checks does **not** show that a table is good; the interpretation must say so
   (`fixer-rules.md` line 7).
3. **Attribute nothing unread.** Only registry keys (§7) may be cited, and only at book or paper level unless the builder has read the
   abstract (`fixer-rules.md` line 8; VERIFIER_RULES §2.1). No page, table, equation, quotation or date is typed from memory. A builder
   never states what the Cochrane note or the McCloskey book says (B1, B2). Precedent: AC2, AC4 §0 ("never type a page or table from memory").
4. **Scope words need a computation, a witness or an explicit hypothesis** (`fixer-rules.md` line 9). In PC1 prose these are the
   dangerous ones: "every", "all", "never", "always", "any", "the standard", "good", "effective", "best", "top journals", "referees
   want". Each is removed or backed by a checklist, a count or a stated hypothesis.
5. **Define before use.** Each of the 5 PC1 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned lesson,
   and never before it. Terms outside the 5 (for example "standard error", "standard deviation", "referee", "roadmap", "word budget",
   "annotation") are defined in prose at first use with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>`
   without `data-concept`; `check_dag.py` line 47).
6. **Explicit hypotheses for checklists.** A "standalone" or "first-result" test is a definition with stated conditions. It is graded T
   only as "conditional on the stated checklist" (BUILDER_RULES §3.3; `fixer-rules.md` line 12).
7. **Grader rule.** Not applicable (rubric-only; §5). If an autograder is ever added, the rules of BUILDER_RULES §5.3 apply.
8. **Money.** PC1 has no money output. The slot budget and word counts are exact integers or `Fraction` values.
9. **No horizontal scroll at 360 px** (`fixer-rules.md` line 14). Every table sits in a wrapping or scrolling container (`table-wrap`).
   Code blocks scroll inside their own container. Quiz options use `min-inline-size: 0` on fieldsets. Escape `$` as `\$` inside math.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py`; the E5 plan cites lines 51-60, not re-read for this plan; the M1 twin
    `tests/labs/M1/lab-M1-L04-1.py` is the model).
11. **Process words are banned in learner text** (`fixer-rules.md` line 14): "build", "builder", "round", "verifier", "REQUESTS",
    "unit report". PC1 is a writing unit, so "build" is a natural word and must not appear in learner text. Use "construct", "write"
    or "assemble". Use "rounding" (E5 precedent), not the bare word "round".
12. **No live figures.** No `chart.js` figure and no new JS kernel (§12 Q11). Before/after figures are static inline SVG with `<title>`
    and `<desc>` (BUILDER_RULES §6.3), colours from CSS tokens only, legible at 360 px in light and dark.
13. **Fictional papers are labelled.** Every supplied or illustrative paper is labelled "Hypothetical paper. Not a real study." Every
    generated number is labelled **SIMULATED** (BUILDER_RULES §1.7). No real author names appear in any hypothetical paper (§12 Q9).
14. **Hub lesson titles match each lesson's `<h1>` at integration** (precedent: CF1 KNOWN 3).

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key or a derivation. Writing advice is not an empirical
  finding. Its grade is **T** only when it is a definition or a mechanical checklist with stated conditions, and **D** otherwise, written
  as "It is widely claimed …" and flagged (BLUEPRINT §3 grade D). **No B or C claim is planned** (§3); if a builder adds one, it names
  its published counter-evidence (BUILDER_RULES §2.5), and none is in the registry for PC1.
- Concepts: §1 table; `<dfn>` only for the 5 registered concepts plus plain `<dfn>` for other terms. No `<a class="concept">` for any concept
  outside the closure {CS1, P0.1, S0} (§4).
- Prerequisite links: `href="../../../concepts.html#<id>"` for CS1, P0.1 and S0 concepts (the same depth as `course/modules/E/E5/`). Earlier
  PC1 lessons: `href="Lnn.html#def-<id>"`. A lesson never links a concept defined in a later lesson. There is no link to a P0.1 or S0 hub,
  because neither is built.
- Labs: code lives once in `tests/labs/PC1/lab-PC1-Lnn-1.py` (and `lab-PC1-project-1..3.py`). The page carries `@@LAB:<file>@@` and
  `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-PC1-<page>-<n>` (`check_pages.py`
  `check_lesson`, lab-id rule). Standard library only (`fractions`, `math`, `random.Random(seed)` if any RNG). No network. Under 10 s in Pyodide.
- SIMULATED label on every lab or figure that uses generated numbers (L01, L02, L03, all project labs). L04 is arithmetic on a stated plan
  and carries the label "Illustrative plan. Not data."
- Never hand-edit generated files (`CURRICULUM.md`, `curriculum/curriculum.json`, `course/index.html`, `course/concepts.html`,
  `course/assets/data/*`, `references/*.json`, `MANIFEST.json`). Request changes; do not write them.
- Learner-visible text: no process words (§2.1 item 11) and no planning references in code comments.
- Banned strings (`tools/check_pages.py` lines 58-72, `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the scope",
  "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well known", "obviously",
  "clearly", and any ellipsis `...` outside code. PC1 prose must avoid "effective", "best practice" and "referees want" unless a grade-D flag
  and "It is widely claimed" wording are used.
- A finite enumeration (for example the set of checklist items) is grade C with its basis named, not grade T (precedent: M1 L06).
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output contract.

### 2.3 Notation (binding; `notation/notation.json`)

Registered symbols that PC1 must not give a different meaning (`notation/notation.json` `symbols` array and `macros` object):
- `T` (number of return observations, module S1): **not used.** Counts of words, pages or slides are written `N_w`, `N_s`, `N_q` and defined on the page.
- `\se` (macro, standard error): **allowed** if a table note writes a standard error in math. The prose term "standard error" is a plain `<dfn>` (§2.1 item 5).
- `\E`, `\Corr`, `\Cov`, `\Var` (macros): not used. PC1 has no derivation that needs them. Plain prose names "correlation" and "variance" (the M3 precedent, FINAL rulings item 3).
- `\R`: real numbers, standard (FINAL rulings item 1).
- `\SR`, `\hSR`, `\PSR`, `\DSR`, `\PBO`, `\FWER`, `\FDR`, `\FDP`: not used. A hypothetical paper's Sharpe ratio, if any, is written in words.

Local symbols allowed (defined on the lesson where they first appear): `N_w`, `N_s`, `N_q` (counts), `x` and `\hat\beta` for a SIMULATED coefficient in L02 and L03, `SE` text in tables.

NOTATION_REQUESTS: none.

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the BUILDER_RULES §4.2 structure in order: why it matters (≤120 words), core content (Definition, Theorem, Proof,
Example, Remark blocks), inline lab, where the canon breaks, misconceptions (≥3), problem set (≥3 problems in each of the four tiers, with a full
worked solution each, `check_pages.py:286-292`), key-results table, retrieval quiz (8–15 items). A debate brief is not required (no `debate:` key).
The four tier names are fixed by the tool (`tools/check_pages.py:76`: "mechanics", "proof", "empirical", "research"). For PC1 they mean: Mechanics = edit
and count exercises; Proof = argument-logic exercises (does a claim follow from the stated result?); Empirical = claim-to-evidence exercises on a
hypothetical paper; Research = an open rewrite or design question with a stated checklist. Twelve problems per lesson are required.

- **L01 `research-paper-structure`** (defines it; links P0.1 `paper-anatomy`, `identification`, `robustness-check`, `replication`). Content: the
  section order that this module uses for an empirical finance paper (introduction, data, method, results, robustness, conclusion), with the
  job of each section stated as a definition. The order is a **module convention**, not an empirical finding. It is taught as a definition
  (grade T, conditional on the stated convention) and never as "most papers do this" (that claim would be grade D at most). The lab checks the
  first-number position of the hypothetical introduction and the section budget on a SIMULATED outline. Canon breaks: theory papers with no
  data section, short notes, and papers whose headline is a method. Misconceptions to cover (≥3): "the literature review must come first";
  "the introduction should describe the paper's plan"; "the structure is fixed by the journal".
- **L02 `results-first-introduction`** (defines it; links P0.1 `evidence-grade`, `identification`, `robustness-check`). Content: the result
  sentence (estimate, unit, sample, direction, magnitude) and the rule that the first paragraph states it before any literature. Derivation: a
  rounded magnitude is computed from the unrounded estimate and the rounding rule is stated (T, in a numbered Example). Claim scope rule: a
  sentence never states a sample, period or method wider than the hypothetical paper's (T, as a checklist definition). Advice about what
  readers do is grade D. Canon breaks: a null result, a descriptive paper, a paper whose contribution is a data set. Misconceptions (≥3):
  "a headline number without a unit is enough"; "the abstract can replace the introduction's result sentence"; "a rounded number may be
  compared with the threshold it sits near".
- **L03 `standalone-table`, `figure-redesign`** (define both; link L02 `results-first-introduction`, S0 `misleading-chart`, `graphical-perception`,
  `anscombes-quartet`, `empirical-distribution`). Content: the checklist of a table that stands alone (title states the finding; every column has
  a unit; every coefficient has its standard error in the stated form; N and the sample are in the note; every symbol is defined in the note;
  stars or significance markers are defined in the note). The checklist is a definition with stated conditions (grade T, conditional). The
  figure section covers the truncated-axis effect: with the axis starting at 90, bars of 92 and 100 have a visual length ratio of 1/5, while the
  true ratio is 92/100 (exact arithmetic in the lab; grade T in a numbered Example). Encoding rank (position, then length, then angle or area) is the S0
  `graphical-perception` concept; its attribution to Cleveland and McGill is graded only if the builder has read the abstract of
  `cleveland1984graphical` (§7.1). Canon breaks: a table with more than one natural unit, a figure whose axis must not start at zero. Misconceptions (≥3):
  "a table with stars needs no note"; "a truncated axis is a cosmetic choice"; "a figure is redesigned by adding colour".
  **Lab `lab-PC1-L03-1` is the curriculum lab** (`yaml:122`).
- **L04 `expert-presentation`** (defines it; links P0.1 `steelmanning`, `replication`, `project-ladder`). Content: a talk to an expert audience is
  organised around the result and the strongest objection; the slot is budgeted as an exact fraction of the time (lab); a question is answered by
  first restating it. Every claim about audiences and referees is grade D with "It is widely claimed" and a flag. Canon breaks: a non-expert
  audience, and a talk where the paper is not yet written. Misconceptions (≥3): "slides should repeat the paper"; "the Q&A is the last five
  minutes"; "a steelman is a reply to the critic".

Lesson-level constraints:
- Each lesson's "Where the canon breaks" names at least one limit of the advice and what changes without it.
- No lesson uses E6, E8, AP, CF or PC2 concepts (PC2 `investment-memo`, `trade-pitch`, `catalyst`, `pre-mortem`; CF4 valuation). Those are outside
  the closure or downstream.
- No lesson states a number about any real paper, journal or audience.

---

## 4. DAG problems (concepts that natural PC1 content would use outside the closure)

Prerequisite closure of PC1 (computed): **{CS1, P0.1, S0}**, 33 usable concepts (§0.2). Owners below are read from `curriculum.json` `concepts` (planner
check through `coursekit.concept_owner`). Concepts in the closure are **linked**, not re-taught: P0.1 `paper-anatomy`, `evidence-grade`,
`identification`, `robustness-check`, `replication`, `steelmanning`, `project-ladder`, `citation-registry`; S0 `misleading-chart`,
`graphical-perception`, `anscombes-quartet`, `empirical-distribution`, `robust-statistics`, `outlier-detection`, `qq-plot`.

| Ref | Concept | Owner (outside closure) | Where natural PC1 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `research-paper-structure` vs P0.1 `paper-anatomy` | P0.1 (in closure) | L01 section order versus P0.1's anatomy (question, identification, data, inference, robustness) | **Possible overlap, not a DAG defect.** PC1 defines only the section order of the paper it writes and links `paper-anatomy` for the content of each part. Architect confirms (§12 Q6). |
| D2 | `expectation` (M4) | M4 (`curriculum.json` concepts) | "expected return" in a hypothetical introduction | Plain prose, no link, no dfn. Avoid the word in the lesson text. (Architect may add M4; not recommended, §12 Q2.) |
| D3 | `hypothesis-test`, `p-value`, `confidence-interval`, `estimator` (S1); `ols-estimator`, `clustered-standard-errors`, `heteroskedasticity-robust-standard-errors`, `hac-standard-errors`, `coefficient-of-determination` (S2) | S1, S2 | regression tables (L03), the standard error in a table note, the significance stars | Plain prose. The table convention "standard error in parentheses; the error type stated in the note" is a convention, not an inference result. No S1 or S2 concept is linked or defined. (§12 Q3.) |
| D4 | `sharpe-ratio`, `sharpe-ratio-standard-error-iid` (S1) | S1 | a hypothetical paper's headline Sharpe ratio | Not used. Hypothetical papers use plain outcome names ("the portfolio return", "the spread"). |
| D5 | `event-study`, `difference-in-differences`, `instrumental-variables` (S6) | S6 | hypothetical identification sentences in the rewrites | Not used by name. "Compare the treated and control groups before and after" is plain prose. |
| D6 | `data-snooping-bias`, `backtest-overfitting` (S7); `publication-bias`, `factor-zoo` (F5); `survivorship-bias` (F1); `look-ahead-bias` (QR1) | S7, F5, F1, QR1 | "limits" criterion of the rubric; the canon-breaks sections | Plain prose descriptions of limits, with no concept link. The rubric's limits criterion names "sample" and "identification", which are closure concepts. |
| D7 | `correlation`, `covariance-matrix`, `variance`, `normal-distribution` (M4) | M4 | a standalone table with a correlation column | Plain prose, the M3 precedent (FINAL rulings item 3). "Standard deviation" is a plain `<dfn>`. |
| D8 | `referee-report` (CAP1), `pre-registration` (CAP4), `board-presentation` (CAP0), `investment-memo`, `trade-pitch`, `ic-adversarial-qa` (PC2) | CAP0, CAP1, CAP4, PC2 | the expert-presentation lesson's audience and Q&A | Plain prose ("referee", "investment committee") with no link. PC2 is downstream of PC1 (`yaml:134`). |
| D9 | "roadmap", "word budget", "annotation", "claim scope" | none in the curriculum | rubric terms and checklists | Plain `<dfn>` with no `data-concept`, defined on first use (§2.1 item 5). |

Each row has a resolution, so no DAG_DEFECT blocks the build. **Each row needs the architect's confirmation** (§12 Q2, Q3, Q6). `check_dag.py`
sees only linked uses (`tools/check_dag.py` docstring). An unlinked use of D1-D8 passes the tool, so the verifier reads every lesson for these names
(VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): rubric-graded, ladder, spec, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `tools/check_projects.py:33` lists the rungs in order)

Tier U keeps all four rungs at full length: placement skips apply to rungs 1-2 only on a placement pass (BUILDER_RULES §5.1), and the
expertise-reversal minimum applies from tier M (BLUEPRINT §4).

1. **Rung 1, worked example** (`lab-PC1-project-1`, SIMULATED): one fully solved, annotated rewrite of **hypothetical introduction H1**. Each
   step carries a "why" annotation (the result moved to sentence one; the unit added; the sample stated; the claim narrowed to the sample).
   The lab prints the structural checks before and after the rewrite (first-result position, unit present, roadmap present, annotation count).
2. **Rung 2, completion** (`lab-PC1-project-2`, `class="lab completion"`, SIMULATED): the result sentence and the roadmap sentence of hypothetical
   introduction H2 carry blanks (`___`). Graded instantly. Its twin is the completed solution, and every page line equals the twin line or contains
   a blank (`tools/run_labs.py` docstring). `check_projects.py:89-90` requires a completion lab or a quiz; the completion lab is used.
3. **Rung 3, independent project** (graded by rubric): rewrite **H1, H2 and H3** and annotate every change (curriculum scope exactly, `yaml:123-128`).
   `lab-PC1-project-3` is the rung-3 **self-check**: it reads the learner's rewrite text (run locally on `rewrite-H1.md` to `rewrite-H3.md` and
   `annotations.md`; in the browser, the learner pastes the text into the lab's input block, because the browser writes only the files a lab lists
   in `data-files`) and prints the structural checks (first-result position, unit present, roadmap present, annotation count equals change count). It scores **structure only** and says so on the page. It does not
   grade quality.
4. **Rung 4, stretch** (optional, not graded, not in the hours table): a 10-minute talk outline for one rewritten introduction, with the slot
   budget from L04's lab; or a re-drawn table from a SIMULATED regression with the L03 checklist applied. This is the only place slides and
   tables are used (B3).

### 5.2 Spec (`dl.spec`; `tools/check_projects.py:34` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A researcher must rewrite three introductions of hypothetical papers so that each states its result first, with a unit, a
  sample and a scope the paper supports, and annotates every change. The rewrites are read by a seminar audience of experts.
- **Inputs.** Three **hypothetical introductions**, H1, H2, H3, each labelled "Hypothetical paper. Not a real study. All numbers SIMULATED." They
  carry no real author names and cite no real works. Each has a fixed text in the page (the full text is in the page, not in a file). Their
  numbers are generated by the builder, labelled SIMULATED, and written into the page text. No dataset, no `data-files`, no MANIFEST entry.
- **Required outputs.** Three files, named exactly: `rewrite-H1.md`, `rewrite-H2.md`, `rewrite-H3.md`, and one annotations file `annotations.md`.
  Every changed sentence appears in `annotations.md` with the original text, the new text and the rule applied (the rules are the five
  criteria in §5.4). A rewrite is 150 to 250 words. The 150-to-250 word band is a spec constraint, not an empirical claim.
- **Constraints.**
  - No citation of a real work. A citation in a rewrite is allowed only when it is a registry key listed in the reading list (§7.1); none is
    required.
  - Every number in a rewrite is copied from the hypothetical paper, with its unit, and is not recomputed from another number unless the
    rewrite states the rounding rule.
  - The rewrite must not claim a sample, period or method wider than the hypothetical paper states.
  - The specification states the standard in these five criteria (B1). "To the Cochrane standard" is not used in the page text.
  - Any tool may be used to write the rewrites. The rubric does not depend on the tool.
- **Grading.** Rubric (`rubric`), by the criteria in §5.4. The spec's grading entry names the rubric (`GRADING_WORDS`, `check_projects.py:38`).
  Not adversarial: no question bank (§12 Q15).
- **Reading list.** `ol.reading-list` cites `keshav2007read` only (registry key, verified, `references/references.json:14473`). It is a reading
  entry, and the page attributes no claim to it. (Cochrane and McCloskey are not cited; B1, B2.)

### 5.3 Time budget (`<table id="hours">`, sums to 6 h; every row needs a one-line rationale; `check_projects.py` `hours` check)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate H1) | 1 | One solved SIMULATED rewrite, annotated line by line |
| Rung 2, completion problem (fill two blanks in H2, run the instant check) | 1 | Two blanks, then the completion lab |
| Rewrites of H1, H2 and H3 | 2 | Three rewrites of 150-250 words each |
| Annotations of every change | 1 | One line per change: original, new, rule |
| Self-assessment against the exemplars | 1 | Score one's own rewrite by the five criteria, then compare with exemplar-a and exemplar-b |
| **Total** | **6** | Equals `data-hours-project` on the hub |

### 5.4 Rubric (`table.rubric#rubric`; `check_projects.py` `rubric_problems`, lines 58-73)

Five criteria, one table row each: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to 1 (`check_projects.py:58-73`).
Every descriptor is observable (counts, presence or absence, a stated scope). Levels 2 and 3 are written by Builder E to the same standard.

1. **Result first.** Level 4: the first paragraph states the headline estimate with its unit, sample and direction, before any literature sentence.
   Level 1: the headline result is absent from the first paragraph, or it is stated without a unit.
2. **Claim scope.** Level 4: every claim names its sample, period and method, and no claim exceeds the hypothetical paper's stated sample.
   Level 1: a claim generalizes beyond the supplied paper.
3. **Roadmap and structure.** Level 4: the roadmap names each later section by its content, in the L01 order. Level 1: no roadmap, or a roadmap that
   lists section numbers only ("Section 2 describes the data").
4. **Annotation.** Level 4: every changed sentence has an annotation with the original text, the new text and the rule; the annotation count equals
   the change count. Level 1: changes are not annotated, or annotations say only "improved".
5. **Limits.** Level 4: one limit per rewrite, tied to the sample or the identification, in one sentence. Level 1: "notes some caveats".

**Exemplars.** **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, both fully written rewrites of hypothetical introduction H1,
annotated with the descriptors each passage meets or misses. The page's self-assessment form is `section.rubric-self` with `data-rubric="rubric"`
and `data-exemplars="exemplar-a exemplar-b"` (as in M1 and E1).

**Student-error patterns (the annotation targets for the exemplars, not mutants).** The exemplars must show these ten errors, each tied to a
criterion: (1) headline result after the literature review (C1); (2) a result stated without a unit (C1); (3) a claim wider than the paper's sample
(C2); (4) a roadmap that names sections but not findings (C3); (5) a table note with an undefined symbol (C3, L03); (6) a standard error reported
without its form (L03); (7) a silent change with no annotation (C4); (8) a percentage change computed from rounded levels (L02 rule); (9) a citation
that is not in the reading list (C2, B1 reasons); (10) a generic limitation not tied to the identification (C5).

**Analogue of the autograder rule.** The "ten mutants and five alternative correct implementations" rule (BUILDER_RULES §5.3; E5 architect decision)
applies to autograders only. PC1 is rubric-only (`yaml:129`), so the rule is **not applicable**. The ten error patterns above are the rubric's
equivalent of a mutant list, and exemplar-a and exemplar-b are the calibration set (blind scoring by a dedicated scorer, FINAL rulings items 15 and 23).

---

## 6. Real-data policy

- **No real data is needed.** PC1 contains no empirical result to reproduce. Every number is SIMULATED and labelled. No issuer's data is embedded,
  no `data-files` attribute is used, and no MANIFEST entry is added (BUILDER_RULES §6.6).
- **Hypothetical papers.** The three introductions and the outlines are fiction, labelled "Hypothetical paper. Not a real study." They cite no real
  work and use no real author names. A real published introduction is not used: it would need a verified source and a reading of the paper
  (BUILDER_RULES §2.3, §2.4).
- **Honest-pending note.** The curriculum names no data for PC1. The page states that no real paper is used, and says why (§12 Q9).
- **DATA_REQUESTS:** none.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (only keys verified in `references/references.json`; each grepped and read this session)

| Key | Record (as read) | Status | Use in PC1 |
|---|---|---|---|
| `keshav2007read` | `references/references.json:14473`; "How to read a paper" (registry record, verified); `used_by: ["P0.1"]` | verified | Reading list only (paper level). No claim is attributed to it unless the builder reads the abstract. |
| `cleveland1984graphical` | `references/references.json:5517`; "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods" (verified); `used_by: ["S0"]` | verified | L03 encoding rank, **only if the builder reads the abstract** and grades the claim per BLUEPRINT §3. Otherwise the S0 concept name is used with no attribution. |
| `anscombe1973graphs` | `references/references.json:896`; "Graphs in Statistical Analysis" (verified); `used_by: ["S0"]` | verified | L03 "plot before you summarize", **only if the builder reads the abstract**. |
| `tukey1977exploratory` | `references/references.json:21902`; "Exploratory data analysis" (verified); `used_by: ["S0"]` | verified | **Not used** (the S0 concept is linked, not re-attributed). |
| `dunlosky2013improving` | `references/references.json:7453`; verified; `used_by: ["P0.1"]` | verified | **Not used** by PC1 content. |

None of these lists PC1 in `used_by`. Adding PC1 is a registry update made through the registry tools by the architect. Builders never edit a record.

**Trap list (do not match these by name or year).** `cochrane2005asset` (`references/references.json:5558`, *Asset pricing*) and `cochrane2005bond`
(`:5592`, "Bond Risk Premia") are different works and must not be cited as the 2005 "Writing Tips" note. `andrews2023inference` (`:720`, co-author
McCloskey, `:736`) is not the McCloskey book.

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

- {doi: null, authors: "Cochrane (lead only; first name and affiliation not typed)", year: "2005 (curriculum string, yaml:120)", title: "Writing Tips for Ph.D. Students", venue: "note (curriculum string; the venue is not typed)", needed_for: "B1: the 'Cochrane standard' named in the project brief (yaml:125-127); the L02 standard, if the architect keeps the citation", confidence: "the source string exists; no registry record; the three review-queue candidates (review_queue.json:1680-1716) are different works and must not be admitted; the allow-listed domains in references/authorities.yaml do not host a personal writing note, so admission needs an architect decision on the admission path"}
- {doi: "10.7208/chicago/9780226448107.001.0001 (candidate from references/review_queue.json, first candidate; lead only, unverified)", authors: "McCloskey (lead only)", year: "2019 (curriculum string, yaml:121)", title: "Economical Writing, Third Edition: Thirty-Five Rules for Clear and Persuasive Prose (candidate title; lead only)", venue: "book (curriculum string)", needed_for: "B2: the book in the curriculum source list; not cited until admitted", confidence: "title, first author and year match the curriculum string per the review-queue notes; add_reference.py must confirm the record. Do not match by family name: andrews2023inference (references.json:720) is a different work"}
- {doi: null, authors: "Literature on the effect of writing choices on reader or referee outcomes (lead only; no author typed)", year: "not typed", title: "empirical evidence on results-first introductions or table layout", venue: "not typed", needed_for: "optional. Only if a PC1 page wants an empirical claim about writing; default: none, all such claims are grade D", confidence: "the planner identifies no record"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer page; BUILDER_RULES §2.4). Until then the lessons
teach the conventions and the checklists, and no source is cited for what the Cochrane note or the McCloskey book says.

---

## 8. Atlas milestone

None. The curriculum names no Atlas milestone for PC1 (computed: no PC1 entry in the `atlas` array; no `atlas:` key on the project,
`yaml:123-129`). `check_projects.py` skips the contract check (`check_projects.py:144-146`). No `atlas/PC1.contract.md` is needed.

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/PC/PC1/cards.json`, ids `PC1-c001` upward, `lesson` in L01-L04, one card per definition, checklist, key result and misconception
  (BUILDER_RULES §7). `check_pages.py` `check_cards` (line 366) checks the id prefix, the lesson existence, every lesson having at least one card,
  the grades and the registry keys.
- Grade T for every checklist or derived result, with `"basis"` naming the lab, Example or definition that establishes it, for example
  `"basis": "Lab 3, Example 2 (exact Fractions)"`. Grade D cards carry the flag in `front` or `back`.
- Cite a registry key only for an attributed claim (L03 `cleveland1984graphical`, only if its abstract was read). `cite` is `[]` otherwise.
- Cards for a SIMULATED result name the SIMULATED lab in `basis`.
- A card and the key-results row it mirrors carry the same grade and basis (FINAL rulings item 13).

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit PC1            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit PC1
.venv/bin/python tools/check_projects.py --unit PC1
.venv/bin/python tools/run_labs.py --unit PC1               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/PC/PC1/L01.html            # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/PC/PC1/L02.html --refresh lab-PC1-L02-1   # after editing a twin
.venv/bin/ruff check tests/labs/PC1 && .venv/bin/ruff format --check tests/labs/PC1
.venv/bin/mypy tests/labs/PC1                               # strict, repository configuration
```

Not run for PC1:
- `tools/run_graders.py --unit PC1` is not needed. It prints "no autograder" for a rubric unit (`tools/run_graders.py:138-139`).
- `tools/mutate_graders.py` is not needed (no autograder).

Verifier only, on a quiet machine: `.venv/bin/python tools/page_smoke.py --unit PC1` (not run by builders; timing-sensitive),
`.venv/bin/python tools/verify_refs.py --unit PC1` (the unit ledger's run, VERIFIER §2.1). No `fetch_data.py` run (no dataset).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`, and the full gate in CLAUDE.md.

Flag checks: `tools/check_pages.py`, `tools/check_dag.py` and `tools/check_projects.py` accept `--unit`; `tools/run_labs.py` accepts `--unit` and `--page`;
`tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`. The planner did not execute the builder commands; only the coursekit closure, owner, atlas
and built-status functions were run (§0).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** Computed: no `atlas:` key on the project and no `atlas` entry names PC1. `check_projects.py` skips the contract check (lines 144-146).
2. **No debate.** PC1 has no `debate:` key (`yaml:105-129`), so `check_pages.py:412-413` does not require a debate brief.
3. **Rubric-only grading.** No grader, no mutants, no alternatives. `check_projects.py` requires a rubric with 4-7 criteria and four levels each, and
   exemplars at two levels (`rubric_problems`, lines 58-73). The spec's grading entry must name "rubric" (`GRADING_WORDS`, line 38).
4. **Rung 2 must be graded instantly.** `check_projects.py:89-90` accepts a completion lab or a quiz; the plan uses a completion lab.
5. **One curriculum lab, four required.** The curriculum names one lab (`yaml:122`). BUILDER_RULES §6 asks for a numerical check per key formula, so the plan
   adds one lab per lesson (E5 precedent). The curriculum lab is `lab-PC1-L03-1`.
6. **Problem tiers are fixed by the tool.** `check_pages.py:76` requires the four tier names, and each tier needs ≥3 problems with worked solutions
   (`check_pages.py:286-292`). The PC1 meaning of each tier is in §3.
7. **Misconceptions ≥3 per lesson** (`check_pages.py:279`), and each needs the wrong belief and the reason it is wrong (`check_pages.py:282-283`).
8. **Lesson hours 6 is the floor** (`check_pages.py:228`). Four lessons at 6 h is the only split of 24 h that gives four lessons; the tool accepts it.
9. **check_dag sees linked uses only.** Unlinked uses of D1-D8 (§4) pass the tool; the verifier reads for them.
10. **The studio.** PC1 is a member of STUDIO-PC (`yaml:92-105`), which requires PC2 only (`yaml:94`). No studio page is built by this unit.
11. **Built prerequisites.** None (§0.2). Links go to `concepts.html` anchors only. The hub must not link a P0.1, S0 or CS1 page.

---

## 12. Open questions for the architect (numbered; each needs a decision before the builders start)

1. **B1 (BLOCKING), "to the Cochrane standard".** Undefined in the curriculum (`yaml:125-127`), no registry record for the note (`review_queue.json:1672`),
   no allow-listed domain. **RECOMMENDED:** the project page defines the standard through the five rubric criteria (§5.4) and the L02 rules; no author is
   cited for it; the architect amends `yaml:125-127` to "to the standard stated in the specification". Alternative: admit a new domain to
   `references/authorities.yaml` (a policy change) and read the note before writing any standard into the page.
2. **D2, `expectation` (M4).** **RECOMMENDED:** plain prose, no link (E5 and E1 precedent). Do not add M4 as a prerequisite.
3. **D3-D8, the other outside concepts.** **RECOMMENDED:** confirm the defaults in §4 (no S1 or S2 concept, no S6 method names, no S7 or F5 concept
   links, no CAP or PC2 links, M4 concepts as plain prose).
4. **Lesson count, hours and builder ownership.** **RECOMMENDED:** 4 lessons × 6 h, project 6 h (20%), one lesson per builder A-D, Builder E for the
   project, Builder F for cards. Alternative A: 3 lessons × 8 h, project 6 h (L03 would then own both table and figure and the expert talk would
   share L02's hours, a worse concept split). Alternative B: 4 × 6 h with two lesson builders (A: L01-L02 plus index; B: L03-L04) and E for the
   project. The alternatives do not change the hours.
5. **Lab helpers.** Twins must be standalone (no imports between twins), so the checklist code is repeated in L01, L03 and project-3.
   **RECOMMENDED:** confirm that a short repeated checklist (≤ 25 lines) in each twin is accepted, and that a shared helper module in
   `tests/labs/PC1/` is not added (the tool's twin runner is not known to load one). BUILDER_RULES §6.1 says "lab code lives once"; a repeated
   checklist is a deviation to be recorded, not a second copy of the lab.
6. **D1, `research-paper-structure` versus P0.1 `paper-anatomy`.** **RECOMMENDED:** keep both. PC1 defines only the section order of a finance paper
   it writes, and links `paper-anatomy` for what each part contains. The architect confirms there is no DAG_DEFECT (BUILDER_RULES §1.10).
7. **Empirical claims about writing.** **RECOMMENDED:** no claim about the effect of writing on readers or referees is made above grade D. Every such
   claim is written "It is widely claimed …" and flagged. No registry source for writing effects is identified (§7.2 third row is optional).
8. **Coverage gap (B3).** Rung 3 grades introductions only (`yaml:124-128`), while L03 and L04 cover tables, figures and presentation.
   **RECOMMENDED:** keep rung 3 exactly to the curriculum scope; teach and quiz L03-L04; offer tables and slides in optional rung 4 only. An architect
   who wants them graded adds a deliverable to `yaml:123-129` (a curriculum change).
9. **Hypothetical papers.** **RECOMMENDED:** the three introductions are fictional, labelled "Hypothetical paper. Not a real study. All numbers SIMULATED.",
   with no real author names and no real citations. Real introductions would need a verified source and a read paper, and the planner recommends against them.
10. **Data.** **RECOMMENDED:** confirm that PC1 uses no dataset, no `data-files` and no MANIFEST entry, and that every number is SIMULATED.
11. **Figures.** **RECOMMENDED:** no live figure and no new kernel. The before/after pairs in L03 are at most two static inline SVGs with `<title>` and
    `<desc>` (BUILDER_RULES §6.3). Confirm, or request one figure with a kernel and test (BUILDER_RULES §6.4).
12. **Registry bookkeeping.** **RECOMMENDED:** the architect adds PC1 to `used_by` for any key a PC1 page cites, through the registry tools. Default
    keys: `keshav2007read` (reading list); `cleveland1984graphical` and `anscombe1973graphs` only if the builder reads their abstracts. No key is cited
    on the planner's reading alone.
13. **Notation.** **RECOMMENDED:** confirm §2.3: `T` not used; `\se` allowed in table notes; no NOTATION_REQUESTS.
14. **Glossary.** **RECOMMENDED:** terms outside the 5 concepts (roadmap, word budget, annotation, claim scope, standard error, standard deviation,
    referee) are plain `<dfn>` with no `data-concept`. No GLOSSARY_REQUESTS.
15. **Adversarial?** **RECOMMENDED:** not adversarial. The project is a rewrite, not an IC defence, so no 15-angle question bank. Confirm.
16. **Nearest built precedent.** **RECOMMENDED:** AC2 (`plans/AC2-build-plan.md`) as the content-free precedent, PC3 as the same-part layout precedent,
    and S7 as the reference template instance. Confirm.
17. **Problem-tier content.** **RECOMMENDED:** keep the four tool tier names with the PC1 meanings in §3. No change to the tool.

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles, the `build` and `round` word check).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01 plus index; L02; L03 (includes the curriculum lab, `lab-PC1-L03-1`); L04; project (rubric
   and exemplar calibration). Failing rows return to the builder that owns the file, with only the failing rows.
3. **Blind exemplar scoring is done by a dedicated scorer** (FINAL rulings items 15 and 23). The scorer never opens the project page: it runs a stripping
   script over each exemplar and reads only the script's output, then scores by the five criteria. Scores must match the exemplar annotations within one level per criterion.
4. Ledger at `ledgers/PC1.verification.json`. Verifier scripts archived under `ledgers/PC1/scripts/` (VERIFIER_RULES §3). No `ledgers/PC1/mutants/` (rubric-only).
5. Ruling 30 applies: when a slice is closed, a delta verification re-verifies the non-PASS rows and the changed hunks, and carries the rest with their evidence.
6. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. **B1 must be resolved or named as an honest gap first.**

Architect decisions: pending (§12). This plan is the planner's proposal. The binding defaults in `plans/E5-build-plan.md` (Architect decisions,
2026-10-28) and in `plans/PC3-build-plan.md` (Architect decisions, 2026-11-03) apply to PC1 unless §12 changes them.
