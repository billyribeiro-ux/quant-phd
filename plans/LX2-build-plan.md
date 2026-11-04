# LX2 build plan: Securities Law, Regulation & Professional Conduct (2026-11-03)

Unit: **LX2 · Securities Law, Regulation & Professional Conduct** · tier U · 50 h · prerequisite FC1 · no Atlas milestone ·
no debate key · grading `rubric` (no autograder) · output directory `course/modules/LX/LX2/` (part code `LX`) · lab twins
`tests/labs/LX2/`.
Planner: Haiku, plan only. No lesson content, no git operations, no commits, no build tools run. Executors: Haiku builders,
then independent Haiku verifiers (VERIFIER_RULES). A builder never verifies and never writes a ledger.

Evidence convention: every curriculum statement cites `file:line` read during planning. Registry facts cite
`references/references.json` by key and line. Anything not in the curriculum or the registry is marked **NOT IN CURRICULUM** or
**NOT IN REGISTRY**. Planner-derived facts about the tooling were computed by `tools/coursekit.py` (`prerequisite_closure`,
`concept_owner`, `unit`) through `.venv/bin/python`. One page outside the repo was read by the planner (§0.4).

**Status: BLOCKING ISSUES EXIST (§0.3). The hours and the lesson split are feasible. The legal sources for two of the eleven
concepts (Dodd–Frank, MiFID II) and the doctrine source for one more (Texas Gulf Sulphur) are not admitted, so those statements
cannot be graded yet. The architect must decide B1–B4 before the L02 and L03 builders start.**

---

## 0. Curriculum facts and blocking issues

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part LX, title "History, Law & Professional Conduct"; LX1 and LX2 are its two modules | `curriculum/06-profession-capstone.yaml:1-4` (part header), `:19` (LX1), `:50` (LX2) |
| STUDIO-LX requires LX1 and LX2 (the studio is not part of this unit) | `curriculum/06-profession-capstone.yaml:6-8` |
| LX2 id and title "Securities Law, Regulation & Professional Conduct" | `curriculum/06-profession-capstone.yaml:50-51` |
| Tier `U`, hours `50` | `curriculum/06-profession-capstone.yaml:52-53` |
| Prereqs `[FC1]` (only) | `curriculum/06-profession-capstone.yaml:54` |
| Core: "The 1933 and 1934 Acts, insider-trading doctrine, manipulation, disclosure, Dodd-Frank, MiFID II, fiduciary duty, conflicts of interest, model-risk governance." | `curriculum/06-profession-capstone.yaml:55-58` |
| `introduces` has 11 concepts (mapped to lessons in §3) | `curriculum/06-profession-capstone.yaml:59-70` |
| Sources: seven free-text strings (1933 Act; 1934 Act; *Texas Gulf Sulphur*; *Dirks*; *O'Hagan*; SR 26-2; CFA Code) | `curriculum/06-profession-capstone.yaml:71-78` |
| Lab: "Insider-trading fact-pattern classifier (rule-based, with doctrine citations)." | `curriculum/06-profession-capstone.yaml:79` |
| Project "Model-risk validation report"; brief: a validation report "to the standard of SR 26-2 (which superseded SR 11-7 in 2026) on one of your own Atlas models: conceptual soundness, outcomes analysis, limitations, ongoing monitoring"; deliverable "Validation report."; grading `rubric` | `curriculum/06-profession-capstone.yaml:80-86` (title 81, brief 82-84, deliverable 85, grading 86) |
| No `debate:` key on LX2 | `curriculum/06-profession-capstone.yaml:50-86` (absent) |
| No `atlas:` key on the LX2 project; no Atlas milestone names LX2 (the `atlas` block at `curriculum.json` line 172 has no LX2 path; computed by walking the JSON) | `curriculum/06-profession-capstone.yaml:80-86`; `curriculum/curriculum.json:172` |
| JSON row mirrors the YAML (hours 50, prereqs FC1, 11 concepts, 7 sources, lab, project, grading rubric) | `curriculum/curriculum.json:11348` (`"id": "LX2"`) |
| All 11 concepts map to module LX2 in `concepts` (planner check: `concept_owner()` returns LX2 for `securities-registration`, `exchange-act-1934`, `insider-trading-doctrine`, `tipper-tippee-liability`, `misappropriation-theory`, `market-manipulation`, `dodd-frank-act`, `mifid-ii`, `fiduciary-duty`, `conflict-of-interest`, `model-risk-management`) | `curriculum/curriculum.json` `concepts` (the `/module` path of each entry) |
| LX2 is required by the bachelor's credential, listed in the "Business Law & Professional Ethics" course map, and is a topic of the CFA "Ethical and Professional Standards" body | `curriculum/meta.yaml:63`, `:74`, `:153`; `curriculum/curriculum.json` `credentials/0/requires` and `bodies_of_knowledge/0/topics` |
| A later module lists LX2 as a prerequisite | `curriculum/05-macro-alternatives.yaml:509` (`prereqs: [SR1, FI4, LX2]`) |
| The generated mirror of the LX2 row is `CURRICULUM.md` | `CURRICULUM.md:1117-1120` (generated; never hand-edited) |
| Prerequisite closure of LX2, computed: **{E1, FC1, M1, M2, P0.1}**, 61 usable concepts (13 + 10 + 14 + 13 + 11) | `tools/coursekit.py` `prerequisite_closure("LX2")`, run by the planner; per-module `introduces` counts from `unit(...).entry` |

### 0.2 Hours feasibility (no conflict)

The curriculum figure is 50 h (`curriculum/06-profession-capstone.yaml:53`). The tool rules (taken from the E5 plan's citations,
`plans/E5-build-plan.md` §0.2, which read `tools/check_pages.py`):

- lesson `data-hours` 6-12 (`tools/check_pages.py` `check_lesson`, line 227);
- hub `data-hours-lessons + data-hours-project = 50` (`check_pages.py` `check_hub`, lines 337-338);
- project share 10-40% of 50, i.e. 5 to 20 h (`check_pages.py` lines 339-340);
- lessons sum to the hub's lessons figure (`check_pages.py` lines 341-342).

Chosen split: **4 lessons × 9 h = 36 h; project 14 h (28%)**. 36 + 14 = 50. Feasible. **No STOP condition on hours.**
Alternatives inside the rules are listed in §12 Q1.

### 0.3 Blocking issues (architect decision required before the builders start)

**B1. Two of the eleven concepts have no source at all.** `dodd-frank-act` ("Dodd–Frank Act") and `mifid-ii` ("MiFID II") are
introduced (`curriculum/06-profession-capstone.yaml:66-67`) and named in the core (`:57`), but no entry in the seven `sources`
strings (`:71-78`) names either text.
- Registry: no record and no review-queue entry for either. `references/references.json` and `references/review_queue.json`
  contain no `dodd`, `frank` or `mifid` key or source string (planner grep; the only matches in `review_queue.json` are unrelated
  titles).
- Consequence: no L03 sentence may state what either instrument requires (BUILDER_RULES §1.1; the fixer-rules rule that a
  statement about what a standard requires and nobody read is not graded). L03 can name the instrument and say its content is
  **not stated here** until a source is admitted (§7.2, REFERENCE_REQUESTS 2 and 3).
- **Recommended resolution (Q3):** keep the two concepts, admit the primary texts through `tools/add_reference.py`, and let L03
  state only what the admitted text says.

**B2. MiFID II's primary text has no allow-listed domain.** `references/authorities.yaml` (41 lines) lists issuers and publishers
for U.S. agencies, the Bank of England, BIS, SNB, FASB, IFRS, Cboe, the Kenneth French library, CFA Institute and others. The
planner grepped it: zero matches for `europa`, `eur-lex` or `esma`. `add_reference.py` admits a record only through an
allow-listed domain (BLUEPRINT §3; `references/authorities.yaml` header).
- **Recommended resolution (Q4):** architect decides whether an EU issuer domain is added to `authorities.yaml`. Until then
  MiFID II content is not stated (see B1).

**B3. Texas Gulf Sulphur is not in the registry.** The source string `"SEC v. Texas Gulf Sulphur Co., 401 F.2d 833 (2d Cir. 1968)"`
(`curriculum/06-profession-capstone.yaml:74`) has a review-queue entry with reason "primary document: add manually with an
authoritative URL" (`references/review_queue.json:1663-1668`, `used_by: ["LX2"]`). No key exists in `references/references.json`
(planner grep for `texas`, `gulf`, `sulphur`). It is the first case the curriculum lists (`:74`, after the two Acts at `:72-73`).
- Consequence: L02 may cite *Dirks* (`gpo1983dirks`) and *O'Hagan* (`gpo1997united`) now. Any L02 sentence that depends on
  *Texas Gulf Sulphur* (including the classifier's classical-theory branch, until the builder has read the opinion) waits for
  admission (§7.2, REFERENCE_REQUEST 1). An allow-listed domain for the opinion exists: `case.law` (Caselaw Access Project),
  listed in `references/authorities.yaml` issuers. `govinfo.gov` and `supremecourt.gov` are listed too but host U.S. Reports, not
  F.2d.

**B4. The project's Atlas wording has no Atlas milestone behind it.** The brief says "on one of your own Atlas models"
(`curriculum/06-profession-capstone.yaml:82-84`). No Atlas milestone names LX2 (§0.1). Atlas is not a source the rubric can
rely on. This is the same defect as E5's B2 (`plans/E5-build-plan.md` §0.3).
- **Recommended resolution (Q6):** the project supplies one documented SIMULATED model case in its spec. Atlas appears only in
  rung 4 as optional. The architect either accepts this reading or amends `:82-84` (a curriculum change; builders do not edit
  `curriculum/*.yaml`).

Non-blocking, but the architect should see them:

- **N1. *Dirks* record: title and year disagree.** `references/references.json` key `gpo1983dirks` (line 10823): the title field
  reads "Dirks v. SEC, 463 U.S. 646 (1982)" and the `year` field reads 1983. The curriculum string reads "(1983)"
  (`curriculum/06-profession-capstone.yaml:75`). The builder cites the key only and writes no year in prose (Q8). Correction is
  the architect's, through `add_reference.py`. No builder edits a record.
- **N2. CFA Code record type.** Key `cfandcode` (`references/references.json:4946`) has `type: "primary"`; the curriculum string
  says "(practitioner)" (`curriculum/06-profession-capstone.yaml:78`); the record's own `notes.title_recall` echoes the
  "(practitioner)" string. The grade for CFA-sourced claims is set by the BLUEPRINT scale, not by the record's type (Q10).
- **N3. FC1 ledger is FAIL.** `ledgers/FC1.verification.json` verdict `FAIL` (verified 2026-11-02). Its failing rows are
  `proj-mutants-killed` (72/75 killed) and `proj-mutant-r13n01`, `-r13n02`, `-r13n03` (three binary-float mutants that survive
  on seeds 0-9). LX2 does not run FC1's grader and links to FC1 concepts only through `concepts.html` anchors. Q11 decides
  whether the LX2 merge waits for FC1 PASS.

### 0.4 Planner reads outside the repository (one page)

- `https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm` (the page behind registry key `frb2026fed`,
  `references/references.json:9187`) was read by the planner through WebFetch, as a summary. The summary reports:
  - issue date April 17, 2026 and the title "Revised Guidance on Model Risk Management" (matches `frb2026fed` title, line 9190);
  - the body sentence "...issuing the attached Revised Guidance on Model Risk Management, which supersedes and replaces SR letter
    11-7," and a "Supersedes:" list that names SR 11-7 and also **SR 21-8** (model risk management for BSA/AML systems).
  - **The builder must read the page itself** and quote the sentence with its locator. The planner's summary is evidence of the
    supersession claim only, not a locator. The curriculum's "superseded SR 11-7 in 2026" (`:70`, `:83`) is supported in
    substance by this summary. SR 21-8 is not a curriculum string and is not cited unless the builder reads it in the page.

---

## 1. Outline and file ownership (fixed by this plan; the architect confirms)

4 lessons × 9 h = 36 h; project 14 h; total 50 h. Concept counts per row sum to 2 + 3 + 3 + 3 = 11, each concept in exactly one
row (`curriculum/06-profession-capstone.yaml:59-70`).

| Lesson | Title (working) | Concepts it defines (`introduces`, `:60-70`) | Lab (twin id, `tests/labs/LX2/`) | Hours | Owner |
|---|---|---|---|---|---|
| L01 | Registration, disclosure and the two Acts | `securities-registration`, `exchange-act-1934` | `lab-LX2-L01-1`: a finite state machine of the lesson's own registration-to-reporting states; the lab enumerates every state and transition, prints the reachable set, and checks that no transition leaves the set. No statutory timing is coded. (grade C, a finite enumeration of the lesson's model, M1 precedent) | 9 | Builder A |
| L02 | Insider trading and tipping | `insider-trading-doctrine`, `tipper-tippee-liability`, `misappropriation-theory` | **`lab-LX2-L02-1` (the curriculum lab, `:79`)**: the insider-trading fact-pattern classifier. Eight HYPOTHETICAL fact patterns, authored for the lab (not case records). Each pattern is classified by stated rules; the printed table names the branch that fired and the registry key the branch rests on. Standard library only. | 9 | Builder B |
| L03 | Manipulation, Dodd–Frank and MiFID II | `market-manipulation`, `dodd-frank-act`, `mifid-ii` | `lab-LX2-L03-1`: a seeded order-event stream on the FC1 limit-order-book mechanics (FC1 `limit-order-book`, `order-types` are in the closure); a cancel-to-fill ratio per trader, exact in `Fraction`, against a **demonstration** threshold labelled as not a regulatory threshold. SIMULATED. | 9 | Builder C |
| L04 | Fiduciary duty, conflicts and model-risk governance | `fiduciary-duty`, `conflict-of-interest`, `model-risk-management` | `lab-LX2-L04-1`: outcomes analysis on a SIMULATED forecast and realised path: hit rate and bias in `Fraction`, the rounding rule printed, the definitions of both measures stated before the run. | 9 | Builder D |
| index | Hub: objectives, prerequisites, placement, lesson map, ladder, hours split 36 / 14 | none | none | - | Builder A |
| project | Model-risk validation report (`rubric`, §5) | none | `lab-LX2-project-1` (rung 1), `lab-LX2-project-2` (rung 2, `class="lab completion"`), `lab-LX2-project-3` (rung 3 check) | 14 | Builder E |
| cards | `cards.json` from L01-L04 | none | none | - | Builder F (after A-E) |

Ownership rule: each builder writes only its own lesson files and twins. Builder A writes the hub after L01 exists, so the lesson map
and titles are right; the cross-check runs at integration. Builder E writes the project, its rubric and exemplars, and does not
depend on the lessons' text beyond the four element names in §5.2.

**Deviation from the template (Q2).** BLUEPRINT §5 and the E5 template give about two or three lessons per builder. A 50-hour
unit with lessons of 6-12 h has four lessons, so each lesson builder owns one lesson. FC1 (`plans/FC1-build-plan.md` §3) and E5
(§1) use the same one-or-two-per-builder pattern. The hub stays with Builder A.

Coverage check: 2 + 3 + 3 + 3 = 11, each concept in one row, matching `curriculum/06-profession-capstone.yaml:60-70`.

Ordering check (no lesson links a later definition; `check_dag.py` checks linked uses, §4):
- L01 uses FC1 `exchange-vs-otc` and `financial-intermediary` only as prerequisite links (`concepts.html` anchors) and does not
  link any LX2 concept.
- L02 uses L01's `securities-registration` and `exchange-act-1934` in prose for the reporting duty; the two doctrines are defined
  here, in the order insider trading, tipping, misappropriation.
- L03 uses L02's `insider-trading-doctrine` and `misappropriation-theory` only in prose (manipulation is a separate prohibition);
  `market-manipulation` is defined first in L03; `dodd-frank-act` and `mifid-ii` are defined last, with their scope only (§0.3 B1).
- L04 uses L03's `market-manipulation` only in prose (a conflicted adviser can also manipulate); `fiduciary-duty` is defined before
  `conflict-of-interest`, and `model-risk-management` closes the lesson.

Not in this table: the curriculum assigns no debate (no `debate:` key, §0.1). Lessons carry no debate brief. Contested claims are
handled by the two-sided rule (§2.2, BUILDER_RULES §2.5).

---

## 2. Binding rules for every builder (BUILDER_RULES adapted to LX2)

Read first, in full: `CLAUDE.md`, `BUILDER_RULES.md`, `BLUEPRINT.md` §3-§8, this file, `plans/FC1-build-plan.md` §2.1 (its
lessons-learned list is binding precedent), `plans/E5-build-plan.md` §2.1, `plans/LX1-build-plan.md` §2.1 (sibling in the same
part) and `course/modules/FC/FC1/` for layout and the hub and project grammar. `course/templates/` holds the four skeletons.
Imitate structure, not wording.

### 2.1 Carried-over verification lessons (binding; each was a real defect in an earlier campaign)

1. **Numbers from unrounded values.** Every number in prose is computed from exact values (`fractions.Fraction`) and rounded only
   at display. A page that shows a rounded figure says which rounding it uses. LX2 has few numbers: the lab's ratios and the
   project's rates. Precedents: AC4 KNOWN LIMITATION 3; FC1 §2.1 item 1.
2. **Lab statements match code and output.** The hypothesis states the result the lab prints. The interpretation names only what the
   printed table shows. A lab that classifies hypothetical patterns says nothing about how a court would rule. Precedent: M1
   LESSON_TEXT_DEFECTS.
3. **Attribute nothing unread.** Only the keys in §7.1 may be cited. The builder reads the source page (or the opinion, or the
   statute section) before stating what it says, and quotes the sentence with its locator (page, section, paragraph or opinion
   page). No legal holding, section, subsection, date, dollar amount, reporter cite or quotation is typed from memory. A statement
   about what a statute or rule requires that the builder did not read is **not graded**: it reads "not stated here" or it is
   deleted (fixer-rules, "GRADES for unread standards"). Precedent: E5 §2.1 item 3; FC1 §2.1 item 3.
4. **Scope words need a computation or an explicit hypothesis.** "every", "all", "never", "always", "any", "the law", "the rule",
   "prohibited", "required", "illegal" are used only where the cited text says so, or where a lab or an explicit enumeration makes
   the claim. Most legal statements are grade C with the source key and locator (§2.3). A finite enumeration of the lesson's own
   model is grade C with its basis named, not grade T (M1 L06 precedent).
5. **Define before use.** Each of the 11 concepts is defined with `<dfn id="def-<id>" data-concept="<id>">` in its assigned
   lesson and never before it (§1). Terms outside the 11 concepts (for example "material information", "scienter", "fraud",
   "tippee", "disclosure", "fiduciary" as a noun, "adviser", "investment committee", "model owner", "model inventory") are defined
   in prose at first use with a plain `<dfn>` and no `data-concept` (`tools/check_dag.py` skips a `<dfn>` without `data-concept`).
   Their statutory or doctrinal definitions are quoted from the source with a locator, or the term is left undefined.
6. **Assumptions explicit.** Every Definition that depends on a condition, and every model result in the labs, lists its numbered
   Assumptions (A1, A2, ...). Legal conditions are quoted from the source with a locator (for example, the elements of a claim
   named in the opinion), never reconstructed.
7. **Grader rule.** Not applicable (rubric-only; §5). See §5.7 for the contingency if the architect changes grading.
8. **Money.** LX2 has no money output in its lab or project. If an amount appears (for example a penalty in a quoted statute), it is
   quoted with its locator and never converted. Any money the project computes is integer cents with the rounding rule stated
   (BUILDER_RULES 1.2; precedent FC1 §2.1 item 8).
9. **No horizontal scroll at 360 px.** Tables wrap or sit in a scrolling container; code blocks scroll inside their own container.
   Quiz options use `fieldset` with `min-inline-size:0` (fixer-rules). `page_smoke.py` is the verifier's check.
10. **Labs call `main()` at top level.** Every twin ends with an unconditional `main()` call and has no `if __name__ == "__main__":`
    guard. `run_labs.py` runs each twin as `python -I -W error <twin>` (`tools/run_labs.py` line 55). Precedent:
    `tests/labs/M1/lab-M1-L04-1.py` (fixer-rules; FC1 §2.1 item 10).
11. **Labels for generated content.** Hypothetical fact patterns carry the label **HYPOTHETICAL** on the page and in the twin's
    docstring, because they are authored scenarios, not case data. Generated order events and generated forecast paths carry the
    label **SIMULATED** (BUILDER_RULES 1.7). No lab or project input is presented as a real case, a real firm or a real trade.

### 2.2 Standing rules (BUILDER_RULES, unchanged)

- Evidence: every claim carries a grade (T/A/B/C/D/X, BLUEPRINT §3) and a registry key with a locator, or a derivation on the page.
  A B- or C-graded claim names its published counter-evidence (BUILDER_RULES §2.5). For legal doctrine, §2.3 applies.
- Concepts: §1 table; a `<dfn>` only for the 11 registered concepts, plus a plain `<dfn>` for other terms (§2.1 item 5). No
  `<a class="concept">` for any concept outside the prerequisite closure {E1, FC1, M1, M2, P0.1} (§4).
- Prerequisite links: `href="../../../concepts.html#<id>"` for E1, FC1, M1, M2 and P0.1 concepts; `href="Lnn.html#def-<id>"` for
  earlier LX2 lessons. A lesson never links a concept defined in a later lesson. There is no link to an FC1 hub page: FC1 links go
  to `concepts.html` anchors only.
- Labs: code lives once in `tests/labs/LX2/lab-LX2-Lnn-1.py` (and `lab-LX2-project-1..3.py`). The page carries `@@LAB:<file>@@`
  and `@@OUT:<file>@@`; `tools/embed_labs.py` fills them. Never type expected output. Lab ids match `lab-LX2-<page>-<n>`
  (`check_pages.py` `check_lesson`). Standard library only (`fractions`, `random.Random(seed)`, `dataclasses`, `enum`); seeded RNG
  only; no network; under 10 s in Pyodide; no warnings (`-W error`).
- Learner-visible text: no process words (build, builder, round, verifier, REQUESTS, unit report) and no planning references in
  code comments.
- Banned strings (`tools/check_pages.py` lines 58-72, `BANNED`): TODO, TBD, lorem, "for brevity", "details omitted", "beyond the
  scope", "left as an exercise", "you can add more", "it is important to note", "studies show", "experts agree", "it is well
  known", "obviously", "clearly", and any ellipsis `...` outside code.
- Every "checked" or "verified" claim names the lab, the line or the test that did the check.
- Hub lesson titles match each lesson's `<h1>` at integration (precedent: CF1 KNOWN 3).
- Quiz explanations are read against their lesson (precedent: CF1 KNOWN 6).
- No `git commit`, no push. Report files written, commands run with exact output, and every gap in the BUILDER_RULES §10 output
  contract.

### 2.3 Legal and regulatory statements (binding for this unit; no BLUEPRINT grade covers them)

BLUEPRINT §3 grades empirical and theoretical claims. A holding or a statutory requirement is neither. The plan's default (Q7):

- Every holding, element or requirement is quoted or paraphrased **from the admitted source** and carries
  `data-cite="<key>"` and `data-locator` (section, paragraph, or opinion page as printed in the source).
- The grade is **C**: a single-source reading, named as such, with the key and locator. A paraphrase that the builder has not
  checked against the source is not graded at all.
- Each lesson says once, in its opening, that the text is an educational reading of cited sources, not legal advice.
- A statement that depends on a secondary commentary (no commentary key is in the registry) is removed or marked **not stated here**.

### 2.4 Notation (binding; `notation/notation.json`)

LX2 has little mathematics. The labs use counts, a finite state machine and exact ratios.

| Registered symbol or macro | Registered meaning (locator) | LX2 rule |
|---|---|---|
| `T` | number of return observations in a sample (`notation/notation.json`, `symbols`, module S1) | Never used for a time horizon, a period or a trader count in LX2. Write `H` for a horizon. |
| `\E`, `\Prob`, `\R` | expectation, probability measure, real numbers (`notation/notation.json`, `macros`) | Used only where the lab or project needs them. Prefer counts and ratios in words. `\R` is the registered macro, never `\mathbb{R}`. |
| `\SR`, `\PBO`, `\FDR` | Sharpe ratio, backtest-overfitting probability, false discovery rate (`symbols` / `macros`) | Not used. |

Local symbols (defined on the lesson where they first appear and never redefined): `h` hit indicator, `b` bias, `\hat{y}_t` forecast,
`y_t` realised value, `c` cancellation count, `f` fill count (L03 lab). The bias is `\operatorname{bias}=\frac{1}{H}\sum_{t}(\hat{y}_t - y_t)`,
defined on L04 before the lab.

NOTATION_REQUESTS: none. No new symbol is needed.

### 2.5 Hypothetical and simulated content

- Lab L02 uses HYPOTHETICAL fact patterns: eight authored scenarios, each with its facts listed in the twin's source as data. The page
  never says a scenario happened.
- Lab L03 and lab L04 use SIMULATED data from seeded generators (`random.Random(seed)`). The seed and the generator are printed.
- No real data is used anywhere in LX2 (§6).

---

## 3. Lesson content plan (what each lesson must cover; no lesson text)

For each lesson the builder writes the §2.2 structure (BUILDER_RULES §4.2). Mandatory content, by lesson. Every legal statement
follows §2.3.

- **L01 `securities-registration`, `exchange-act-1934`.** The two Acts as the lesson's subject: what each Act's text covers, read
  from `gpondsecurities` (the 1933 Act, `references/references.json` line 10908 title) and `gpondsecuritiesb` (the 1934 Act, line
  10946 title). The registration and reporting duties are quoted with their section locators. The lab's state machine is the
  lesson's model of the registration-to-reporting lifecycle, labelled as a model. "Where the canon breaks": the lifecycle omits
  exemptions the text provides (the exemption list is not read by the planner; the builder states that the lab does not model it).
- **L02 `insider-trading-doctrine`, `tipper-tippee-liability`, `misappropriation-theory`.** Doctrine as stated in the admitted
  opinions: *Dirks* (`gpo1983dirks`) and *O'Hagan* (`gpo1997united`). The classical theory, tipping and misappropriation are each
  quoted from the opinion with its page locator. *Texas Gulf Sulphur* enters only after admission (§0.3 B3). The lab is the
  curriculum lab (`:79`): eight HYPOTHETICAL patterns, each classified by the lesson's stated rules; the rules are the quoted
  elements, and the output names the element that decided each pattern. "Where the canon breaks": the classifier decides
  nothing a court decides; facts outside the eight patterns, and any question of materiality or intent, are outside the lab.
  Market context: the information-advantage intuition uses FC3's `efficient-markets-hypothesis` in plain prose (§4 D1).
- **L03 `market-manipulation`, `dodd-frank-act`, `mifid-ii`.** Manipulation as a defined term: its definition is quoted from the
  admitted primary text that defines it (not yet admitted; B1 and the registry: no manipulation source is listed in the curriculum
  for this concept). Until a source is admitted, `market-manipulation` is taught as the **behaviour in the lab** (cancel-to-fill
  pattern on the FC1 order book), with the sentence "the legal definition is not stated here". The lab's threshold is a
  demonstration value, not a rule. Dodd–Frank and MiFID II: scope and content only after REFERENCE_REQUESTS 2 and 3 are admitted
  (§0.3 B1, B2); otherwise each concept is defined by its name and "content not stated here". "Where the canon breaks": the
  order-book model has no broker, no latency and no cross-venue routing.
- **L04 `fiduciary-duty`, `conflict-of-interest`, `model-risk-management`.** Fiduciary duty and conflicts: the curriculum's sources
  for these two concepts are the CFA Code (`cfandcode`, `:78`) only; no statute or case in the curriculum sources governs them
  (§7.2 REFERENCE_REQUEST 6). Model-risk management: SR 26-2 (`frb2026fed`, `:77`), read by the builder from its page (§0.4);
  the four element names used in the project (conceptual soundness, outcomes analysis, limitations, ongoing monitoring) come from
  the curriculum (`:83-84`) and must match the page's headings or be stated as the curriculum's list. The supersession of SR 11-7
  (and of SR 21-8 if the builder reads it in the page) is stated with its locator. The lab (L04) demonstrates outcomes analysis on
  a SIMULATED path. "Where the canon breaks": the outcomes measures are the lab's definitions, not the regulator's.

Lesson-level constraints:
- Each lesson's "Where the canon breaks" section names at least one limit of its model (§3 above lists them) and what changes
  without it.
- No lesson uses an E6, E8 or other out-of-closure concept as a defined term. Out-of-closure concepts appear only as plain prose
  (§4).

---

## 4. DAG problems (concepts that natural LX2 content would use outside the closure)

Prerequisite closure of LX2 (computed): **{E1, FC1, M1, M2, P0.1}**, 61 usable concepts. Owners below are from
`curriculum/curriculum.json` `concepts` (planner check with `concept_owner()`).

| Ref | Concept | Owner (outside closure) | Where natural LX2 content would use it | Resolution in this plan |
|---|---|---|---|---|
| D1 | `efficient-markets-hypothesis` | FC3 | the information-advantage intuition behind insider trading (L02) | Plain prose, no link, no `<dfn>`. The lesson does not rely on the hypothesis for any claim. Q9 asks whether to add FC3 as a prerequisite instead. |
| D2 | `voluntary-disclosure`, `information-content-of-earnings` | AC3 | disclosure duties and the price response to information (L01, L02) | Plain prose. The disclosure duty is quoted from the 1933 and 1934 Acts, not from AC3. |
| D3 | `agency-costs`, `board-governance` | CF3 | conflicts and fiduciary duty (L04) | Plain prose; the duty is taught from the CFA Code and the admitted sources, not the agency model. |
| D4 | `moral-hazard`, `adverse-selection` | E2 | information asymmetry in insider trading (L02) and conflicts (L04) | Plain prose. No game-theoretic model is used. |
| D5 | `kyle-model`, `glosten-milgrom-model` | MS1 | informed trading and the price effect of an informed order (L02, L03) | Not used. The manipulation lab is a pattern count, not a model of informed trading. |
| D6 | `model-integrity-checks`, `model-reconciliation`, `spreadsheet-error-risk` | CF7 | outcomes analysis and model governance checks (L04, project) | Plain prose in the project's rubric (criterion 2 and 4). The checks are described, not taught as defined concepts. Q10 asks whether CF7 should be a prerequisite. |
| D7 | `value-at-risk`, `stress-testing`, `backtest-overfitting` | PR4, PR4, S7 | the project's model case is a forecasting model; "limitations" may name these | Plain prose in the project spec only if a student uses them. Not defined. Not used by any lab. |
| D8 | `central-clearing-mandate` | SR4 | the swap-clearing duty in Dodd–Frank (L03) | Not used until B1 is resolved; then plain prose. |
| D9 | `hypothesis-test`, `t-statistic`, `statistical-power` | S1 | any inference on the outcomes analysis | Not used. The outcomes analysis uses counts and a hit rate, no test. |

Each row has a resolution, so no DAG_DEFECT blocks the build. **The architect confirms D1-D9 (Q9, Q10).**
`check_dag.py` checks linked uses only (`tools/check_dag.py` docstring); an unlinked use of D1-D9 passes the tool, so the verifier
reads every lesson for these names (VERIFIER_RULES §2.9).

---

## 5. Project (`project.html`, Builder E): rubric-graded, ladder, spec, rubric

### 5.1 Ladder (BLUEPRINT §5.1; `check_projects.py` requires the order, line 33)

1. **Rung 1, worked example** (`lab-LX2-project-1`, SIMULATED): one fully solved, annotated validation of a worked SIMULATED
   forecasting model: the four element checks in the order of §5.2, each with a "why" annotation. Full length (tier U; BLUEPRINT §4).
2. **Rung 2, completion** (`lab-LX2-project-2`, `class="lab completion"`, SIMULATED): the hit-rate line and the bias line of the
   outcomes analysis are replaced by `___`. Graded instantly. Its twin is the completed solution; every page line equals the twin
   line or contains a blank (`tools/run_labs.py` docstring). `check_projects.py` requires a completion lab or a quiz.
3. **Rung 3, independent project** (graded by rubric): the validation report of the model case in §5.2 with the four sections
   named there. `lab-LX2-project-3` is the rung-3 check: it recomputes the report's default numbers from the case inputs and prints
   the table the report must quote.
4. **Rung 4, stretch** (optional, not graded): validate a second model case (a student-chosen SIMULATED or the student's own model,
   with its documentation), or compare the two reports' limitations sections.

### 5.2 Spec (`dl.spec`; `check_projects.py` requires the terms context, inputs, required outputs, constraints, grading)

- **Context.** A model-risk reviewer must give a validation report on a forecasting model used to set a monthly planning figure.
  The report follows the four elements named in the curriculum: conceptual soundness, outcomes analysis, limitations and ongoing
  monitoring (`curriculum/06-profession-capstone.yaml:83-84`). The report quotes the SR 26-2 structure only as the builder reads it
  in the admitted page (§3 L04).
- **Inputs.** (1) The model case: a one-page documentation of a SIMULATED forecast model (its inputs, equation and a stated
  assumption list), and (2) a CSV of the model's forecasts and realised values, SIMULATED, with a stated seed. No real data (§6).
  The CSV is embedded and opened as `data/<file>` only if the lab lists it in `data-files`; the project's CSV is student-facing
  and read in the browser, never uploaded.
- **Required outputs.** A report file `validation.md` with four sections, in this order: Conceptual soundness; Outcomes analysis;
  Limitations; Ongoing monitoring. Each number in the outcomes section is computed from unrounded values, with the rounding rule
  stated, and cites the series and the period it uses.
- **Constraints.**
  - Every number cites the input file, the period and the definition used (hit rate, bias).
  - No claim about the model beyond the documentation and the data supplied.
  - Each regulatory or doctrinal statement carries a registry key and a locator (§2.3).
  - Standard library or any tool the student chooses; the rubric does not depend on the tool.
  - No series from Atlas is used (B4).
- **Grading.** Rubric (`rubric`, §5.4). The spec's grading entry names the rubric. Adversarial question bank: not required (Q14).
- **Reading list.** `ol.reading-list` cites `frb2026fed` and `cfandcode`, and `gpondsecurities` and `gpondsecuritiesb` for the
  Acts, `gpo1983dirks` and `gpo1997united` for the cases (registry keys only; §7.1). Nothing else.

### 5.3 Time budget (`<table id="hours">`, sums to 14 h; every row needs a one-line rationale)

| Component | Hours | Rationale |
|---|---|---|
| Rung 1, worked example (read and annotate) | 2 | One solved SIMULATED validation, annotated line by line |
| Rung 2, completion problem | 2 | Fill the hit-rate and bias lines, then run the instant check |
| Model case intake: read the documentation, state the assumption list | 2 | Read the one-page case, list the assumptions, state what is not documented |
| Outcomes analysis: hit rate, bias, rounding rule | 3 | Compute both measures from unrounded values over the stated period, state the rule |
| Report: the four sections, every number cited | 3 | Write the four sections with keys and locators for each regulatory statement |
| Self-assessment against exemplars | 2 | Score the report with the rubric, then compare with exemplar-a and exemplar-b |
| **Total** | **14** | Equals `data-hours-project` on the hub |

### 5.4 Rubric (`table.rubric#rubric`; `check_projects.py` `rubric_problems`, lines 58-73)

Five criteria. Each criterion is one table row: the criterion name in a `th`, and exactly four `td` cells for levels 4 down to 1.
Every level descriptor is observable.

1. **Conceptual soundness.** Level 4: names each assumption of the model case, states how the report tests it (with the test named),
   and says which assumption it could not test. Level 1: "looks sound".
2. **Outcomes analysis.** Level 4: states the hit-rate and bias definitions, the period, the rounding rule, and computes both from
   unrounded values. Level 1: "checks accuracy".
3. **Limitations.** Level 4: names each limit, the evidence in the case that shows it, and what would change if the limit were
   removed. Level 1: "notes some caveats".
4. **Ongoing monitoring.** Level 4: names one metric, its threshold with the basis for the threshold, its frequency, and the role that
   reviews it. Level 1: "monitors regularly".
5. **Evidence and citation.** Level 4: every regulatory or doctrinal statement carries a registry key and a locator, and every
   statement the report cannot source is marked not stated here. Level 1: "cites sources".

Exemplars: **exemplar-a (`data-level="4"`)** and **exemplar-b (`data-level="2"`)**, fully written validations of the SIMULATED case,
annotated with the descriptors each passage meets or misses. Self-assessment form (`section.rubric-self`, `data-rubric="rubric"`,
`data-exemplars="exemplar-a exemplar-b"`, as in E5 and M1). The page shows where the student's scores diverge from the exemplar
scores. Calibration: the verifier scores both exemplars blind, within one level per criterion (VERIFIER §2.6).

### 5.5 Atlas and data

No Atlas (B4). No embedded data (§6).

### 5.6 Hypothetical content in the project

The case documentation is SIMULATED and labelled. No case is presented as a real firm or a real model.

### 5.7 Contingency: only if the architect changes grading to `both` (Q13)

Not planned. The curriculum grading is `rubric` (`curriculum/06-profession-capstone.yaml:86`). If the architect changes it, the
numeric part (the outcomes analysis) is the autograder, and the following applies:

- **`grader/instance.py`**: `make_instance(seed: int) -> dict`, generating a forecast path and a realised path from `random.Random(seed)`.
- **`grader/reference.py`**: the full solution with `Fraction` and one rounding step.
- **Ten student-error mutants** (`ledgers/LX2/mutants/`, one docstring line each):
  1. hit rate computed over the calibration window instead of the stated validation window;
  2. bias sign reversed (realised minus forecast written as forecast minus realised);
  3. rounding by truncation toward zero instead of the stated rule;
  4. denominator includes the burn-in rows;
  5. bias averaged in percentage terms and reported as a level;
  6. off-by-one alignment, so each forecast is compared with the realised value one period later (lookahead);
  7. the measure computed in binary floats, failing on the rounding boundary;
  8. a hit defined as `>=` where the stated rule is strict;
  9. missing rows silently dropped instead of failing loud;
  10. a hard-coded answer for seed 0.
- **Five alternative correct implementations** (must pass seeds 0-49): (1) `Fraction` throughout with one final rounding; (2)
  integer basis points with integer division for the rounding rule; (3) a class-based implementation; (4) a generator-based
  streaming implementation; (5) a list-comprehension implementation of the two counts. A float implementation that applies the
  stated rule to the exact value of each output is an alternative; a float implementation that is wrong on the rule is a mutant.
- Failure messages name the violated property and never print the expected value (`__tracebackhide__`).

---

## 6. Real-data policy

- **No real data.** The curriculum names no dataset for LX2 (`curriculum/06-profession-capstone.yaml:79` lab, `:80-86` project).
  The registry has no dataset for this unit. `tools/data_sources.yaml` lists only the Federal Reserve H.10 and H.15 releases
  (embedded) and the French library and Open Source Asset Pricing (rejected). None is relevant.
- The lab L02 is HYPOTHETICAL and the labs L03, L04 and the project are SIMULATED. Each carries its label (§2.1 item 11).
- **DATA_REQUESTS: none.** No `data-files` attribute on any lab. No MANIFEST entry is added by builders.

---

## 7. Registry keys and requests

### 7.1 Keys the module may cite (verified in `references/references.json`; read by the planner)

| Key | Record (as read) | Status | Use in LX2 |
|---|---|---|---|
| `gpondsecurities` | Securities Act of 1933, GovInfo COMPS-1884 (`references/references.json` line 10908 title; `used_by: ["LX2"]`); `year` null | verified, `verified_by: issuer` | L01 (the 1933 Act); reading list |
| `gpondsecuritiesb` | Securities Exchange Act of 1934, GovInfo COMPS-1885 (line 10946 title; `used_by: ["LX2"]`); `year` null | verified, `verified_by: issuer` | L01 (the 1934 Act); reading list |
| `gpo1983dirks` | *Dirks v. SEC*, 463 U.S. 646, GovInfo USREPORTS-463-646 (key line 10823). Title field reads "(1982)", year field 1983 (N1) | verified, `verified_by: issuer` | L02 tipping and classical theory; classifier citation; reading list. Cite by key, no year in prose (Q8) |
| `gpo1997united` | *United States v. O'Hagan*, 521 U.S. 642, GovInfo USREPORTS-521-642 (title line 10868; `year` 1997) | verified, `verified_by: issuer` | L02 misappropriation; classifier citation; reading list |
| `frb2026fed` | SR 26-2, *Revised Guidance on Model Risk Management*, Federal Reserve, April 17, 2026 (`references/references.json` line 9185; URL line 9187; `year` 2026) | verified, `verified_by: issuer` | L04 model-risk governance; project spec; reading list |
| `cfandcode` | CFA Institute, *Code of Ethics and Standards of Professional Conduct* (key line 4946; URL line 4948; record type `primary`, N2) | verified, `verified_by: issuer` | L04 fiduciary duty and conflicts; project reading list. The grade is set by BLUEPRINT §3, not by the record's type |

Not established and **not citable** until admitted: *Texas Gulf Sulphur* (§0.3 B3), Dodd–Frank, MiFID II, the Investment Advisers
Act-type source for fiduciary duty (§7.2 item 6), SR 11-7 (no key; its supersession is stated only through `frb2026fed`), SR 21-8
(not in the curriculum; not cited).

### 7.2 REFERENCE_REQUESTS (for the architect; lead only, no bibliographic record typed)

1. {doi: null, authors: "Texas Gulf Sulphur litigation, Second Circuit (lead only)", year: "1968 (lead only; curriculum string, `curriculum/06-profession-capstone.yaml:74`)", title: "SEC v. Texas Gulf Sulphur Co.", venue: "reporter cite as the curriculum gives it (lead only; record not typed)", needed_for: "L02 classical-theory branch and the classifier's citation; L02 cannot cite it until admitted", confidence: "the review queue holds the string (`references/review_queue.json:1663-1668`); the candidate page is expected at an allow-listed domain (`case.law` is in `references/authorities.yaml`); the planner has not read the opinion"}
2. {doi: null, authors: "Dodd–Frank statute (lead only; the architect names the primary text)", year: "not typed", title: "Dodd–Frank Act (curriculum concept name `dodd-frank-act`, `:66`)", venue: "U.S. statute (lead only)", needed_for: "L03 scope of the Act; no content may be stated without it (§0.3 B1)", confidence: "the concept and the core name the Act (`:57`, `:66`); no source string names it (`:71-78`); candidate issuers `govinfo.gov` and `uscode.house.gov` are allow-listed"}
3. {doi: null, authors: "MiFID II text (lead only; the architect names the primary text)", year: "not typed", title: "MiFID II (curriculum concept name `mifid-ii`, `:67`)", venue: "EU legislation (lead only)", needed_for: "L03 scope; no content without a read source (§0.3 B1)", confidence: "the concept and the core name it (`:57`, `:67`); no source string names it; no EU domain is allow-listed (§0.3 B2), so the admission path needs an architect decision first"}
4. {doi: null, authors: "SR 11-7 (lead only)", year: "2011 (lead only; not typed as a record)", title: "Guidance on Model Risk Management (superseded per the SR 26-2 page)", venue: "Federal Reserve supervisory letter (lead only)", needed_for: "optional: L04 may cite the superseded letter only if the builder needs its text; default: not cited", confidence: "named in the curriculum (`:70`, `:83`) and in the fetched summary of `frb2026fed` (§0.4); no record exists; federalreserve.gov is allow-listed"}
5. {doi: null, authors: "not identified by the planner", year: "not typed", title: "any primary text on the duties of investment advisers (lead only)", venue: "not typed", needed_for: "L04 fiduciary-duty content, because the curriculum's only source for it is the CFA Code (`:78`)", confidence: "the need is certain; the planner names no statute or rule from memory. Architect to name the text"}
6. {doi: null, authors: "Practitioner commentary on model-risk outcomes analysis (lead only)", year: "not typed", title: "not identified", venue: "not typed", needed_for: "L04 two-sided treatment, if the lesson makes a graded B or C claim about outcomes testing", confidence: "the need is conditional; default is to avoid such claims (§3 L04)"}

The architect resolves these through `tools/add_reference.py` (DOI, ISBN, or an allow-listed issuer or publisher page;
`references/authorities.yaml`). Until resolved, the lessons teach the quoted sources only, mark everything else **not stated here**, and
grade legal statements per §2.3.

---

## 8. Atlas milestone

None. No Atlas milestone names LX2 (§0.1). No `atlas/LX2.contract.md` is needed; `check_projects.py` checks a contract only when the
project names an `atlas` key (`check_projects.py` lines 144-146), and LX2's project names none. The brief's Atlas wording is B4.

---

## 9. Cards builder (Builder F, after A-E)

- `course/modules/LX/LX2/cards.json`, ids `LX2-c001` upward, `lesson` in L01-L04, one card per definition, theorem-free result, key
  result and misconception (BUILDER_RULES §7). `check_pages.py` `check_cards` checks the id prefix, the lesson existence, the grades
  and the registry keys.
- Doctrine and statute cards: grade C, `cite` lists the key(s) with the locator in the back. A card never states a holding that the
  admitted source does not contain.
- Lab-derived cards (the state machine, the classifier, the cancel-to-fill ratio, the outcomes measures): `grade` T with `basis`
  naming the lab and the line that establishes it, for example `"basis": "Lab 2 (classifier table, pattern 3)"`. A card on a
  SIMULATED result names SIMULATED in `basis`. A card on a HYPOTHETICAL pattern names HYPOTHETICAL.
- Cards for Dodd–Frank and MiFID II are not written until B1 and B2 are resolved.

---

## 10. Commands (targeted; run from `/Users/billyribeiro/dev/quant-phd`)

Builder checks, targeted (per file while building; `--page` while a lesson is in progress):

```bash
.venv/bin/python tools/check_pages.py --unit LX2            # --page L01 while lessons are in progress
.venv/bin/python tools/check_dag.py --unit LX2
.venv/bin/python tools/check_projects.py --unit LX2
.venv/bin/python tools/run_labs.py --unit LX2               # --page L02 for one lesson
.venv/bin/python tools/embed_labs.py course/modules/LX/LX2/L01.html                        # per page, after twins exist
.venv/bin/python tools/embed_labs.py course/modules/LX/LX2/L02.html --refresh lab-LX2-L02-1 # after editing a twin
.venv/bin/ruff check tests/labs/LX2 && .venv/bin/ruff format --check tests/labs/LX2
.venv/bin/mypy tests/labs/LX2                               # strict, repository configuration
```

Not run for LX2:
- `tools/run_graders.py --unit LX2` is not needed: it prints "no autograder" for a rubric unit (`tools/run_graders.py` skips units
  whose grading is not `autograder` or `both`; E5 plan §10 cites lines 138-139).
- `tools/mutate_graders.py` is not needed (no autograder).

Verifier only, on a quiet machine: `.venv/bin/python tools/page_smoke.py --unit LX2` (not run by builders; timing-sensitive) and
`.venv/bin/python tools/verify_refs.py --unit LX2` (the unit ledger's run, VERIFIER §2.1). No `fetch_data.py` run (no dataset).

Architect, once, before any merge: `check_pages.py --all`, `check_dag.py --all`, `check_projects.py --all`, `build_site.py --check`,
`render_curriculum.py` followed by `git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json`, `verify_refs.py --offline`,
and the full gate in CLAUDE.md. The FC1 ledger (N3) is checked before the merge.

Flag checks: `tools/check_pages.py`, `tools/check_dag.py` and `tools/check_projects.py` accept `--unit`; `tools/run_labs.py` accepts
`--unit` and `--page`; `tools/embed_labs.py` accepts pages and `--refresh [LAB_ID ...]`. The planner did not execute the builder
commands; only the coursekit closure and concept-owner functions were run (§0.1), and the SR 26-2 page was read as a summary (§0.4).

---

## 11. Tooling assumptions that do not hold for this unit (flagged)

1. **No Atlas milestone.** No Atlas entry names LX2 (§0.1). The brief's Atlas wording is B4.
2. **No debate.** LX2 has no `debate:` key, so `check_pages.py` does not require a debate brief (§0.1). Contested claims (the scope of
   insider-trading liability; whether manipulation patterns are unlawful) are handled by the two-sided rule (BUILDER_RULES §2.5).
3. **Rubric-only grading.** No grader, no mutants, no alternative implementations for the project (§5.7 is contingency only).
   `check_projects.py` requires the rubric and two exemplars at two levels (`rubric_problems`, lines 58-73), and the spec's grading
   entry must name "rubric" (`GRADING_WORDS`).
4. **Rung 2 must be graded instantly.** `check_projects.py` accepts a completion lab or a quiz. The plan uses a completion lab.
5. **One curriculum lab, four lessons.** The curriculum names one lab (`:79`, the classifier). BUILDER_RULES §3.4 asks for a
   numerical check per key formula; LX2 has no formula, so the lab per lesson is a structural check (§1). This is a deviation the
   architect should see.
6. **FC1 is not gated by LX2.** LX2 links FC1 concepts through `concepts.html` only; FC1 is built (`course/modules/FC/FC1/`) with a
   FAIL ledger (N3).
7. **check_dag sees linked uses only.** Unlinked uses of D1-D9 (§4) pass the tool; the verifier reads for them.
8. **Hours rule.** Lesson hours 6-12 (`check_pages.py` line 227) and the hub split (lines 337-342) are satisfied by §1.
9. **Quoted sources are read by builders, not by the tool.** `check_pages.py` checks that keys exist, not that the quoted sentence is
   in the source. The verifier does that (VERIFIER §2.1 attribution rule).

---

## 12. Open questions for the architect (numbered; each with the planner's RECOMMENDED decision)

1. **Lesson count and hours.** Confirm 4 lessons × 9 h and a 14 h project (28%). Alternatives within the rules: 5 × 8 h and a 10 h
   project (20%); 3 × 12 h and a 14 h project. **RECOMMENDED: 4 × 9 h and 14 h.** Five lessons would split the insider-trading lesson
   and leave the project with 10 h, which is too little for a four-element report.
2. **Builder ownership.** Confirm one lesson per lesson builder, the deviation from "about three per builder" (§1). **RECOMMENDED:
   Builder A: L01 and `index.html`; Builder B: L02 (curriculum lab); Builder C: L03; Builder D: L04; Builder E: `project.html`,
   rubric, exemplars and project labs; Builder F: `cards.json`.**
3. **B1, Dodd–Frank and MiFID II sources.** Two concepts have no source (§0.3 B1). **RECOMMENDED: admit the primary texts through
   `add_reference.py` (REFERENCE_REQUESTS 2 and 3) before L03 is written. Until then L03 names each instrument and says "content not
   stated here".**
4. **B2, EU issuer domain.** MiFID II's primary text is not on an allow-listed domain (§0.3 B2). **RECOMMENDED: the architect decides
   whether an EU issuer domain is added to `references/authorities.yaml`. If not, MiFID II is taught as "content not stated here" and
   the concept's scope is removed from L03's defined terms.**
5. **B3, Texas Gulf Sulphur.** **RECOMMENDED: admit the opinion through `add_reference.py` using an allow-listed page (`case.law` is
   allow-listed). L02 cites *Dirks* and *O'Hagan* now; the classical-theory branch waits for the admitted opinion.**
6. **B4, Atlas wording.** Confirm that the project uses one SIMULATED model case documented in its spec, with Atlas only as optional
   rung 4 (default). **RECOMMENDED: accept the default; optionally amend `curriculum/06-profession-capstone.yaml:82-84` in a later
   curriculum change.**
7. **Legal statements and grades.** BLUEPRINT §3 has no grade for legal holdings. **RECOMMENDED: grade each holding or requirement C
   with its key and locator (§2.3), state once that the text is not legal advice, and treat any paraphrase not checked against the
   source as ungraded. The architect may add a legal grade to BLUEPRINT if that is preferred; that is a BLUEPRINT change.**
8. **N1, the *Dirks* record.** Title "(1982)" against year 1983 (`references/references.json` line 10823 area). **RECOMMENDED: the
   builder cites `gpo1983dirks` by key with no year in prose. The architect corrects the record through `add_reference.py`; no builder
   edits it.**
9. **D1 and D2, FC3 and AC3 concepts.** **RECOMMENDED: plain prose with no link (default for every module, architect decision of
   2026-10-28). The architect may add FC3 or AC3 as a prerequisite instead; that is a curriculum change.**
10. **D6, CF7 concepts, and N2, the CFA record type.** **RECOMMENDED: plain prose for the CF7 model-governance concepts; cite the
   CFA Code by key `cfandcode` and let the BLUEPRINT scale set the grade, with the record-type mismatch left to the architect.**
11. **N3, FC1 ledger FAIL.** **RECOMMENDED: LX2 builders start now (LX2 does not run FC1's grader). The LX2 merge waits until FC1's
   ledger is PASS, per BLUEPRINT §9 Phase 2's ledger gate, unless the architect waives the gate for LX2 in writing.**
12. **Fiduciary duty source.** The only source for `fiduciary-duty` and `conflict-of-interest` in the curriculum is the CFA Code
   (`:78`). **RECOMMENDED: the architect names an adviser-duty primary text (REFERENCE_REQUEST 5). Until then L04 teaches both
   concepts from the CFA Code at grade C, with the key cited, and says the legal content is not stated here.**
13. **Grading.** **RECOMMENDED: keep `rubric` (`:86`). §5.7 is the contingency design if the architect changes it to `both`.**
14. **Adversarial?** The project is a validation report, not an IC defence or debate. **RECOMMENDED: no question bank.**
15. **Lab labels.** **RECOMMENDED: label the L02 patterns HYPOTHETICAL and the L03, L04 and project data SIMULATED (§2.1 item 11).
   No real case or firm name appears in any lab input.**
16. **Notation and figures.** **RECOMMENDED: no new NOTATION_REQUESTS, no figures, no JS kernel (§2.4; BUILDER_RULES §6.4).**
17. **Glossary.** Terms outside the 11 concepts (§2.1 item 5) are plain `<dfn>`. **RECOMMENDED: no GLOSSARY_REQUESTS.**
18. **SR 26-2 supersession.** The fetched summary (§0.4) supports "superseded SR 11-7" and also names SR 21-8 in the supersedes list.
   **RECOMMENDED: L04 states the supersession from the builder's own reading of the page, with its locator. The curriculum string is
   not changed.**

---

## 13. After the builders

1. Orchestrator integrates; runs the §10 commands once; fixes cross-lesson defects (DAG, links, hours, hub titles).
2. Independent Haiku verifiers in fresh checkouts, by slice: L01-L02 (includes the curriculum lab), L03-L04, project (rubric and
   exemplar calibration). Failing rows return to the builder that owns the file, with only the failing rows.
3. Ledger at `ledgers/LX2.verification.json`; verifier scripts archived under `ledgers/LX2/scripts/` (VERIFIER §3). No
   `ledgers/LX2/mutants/` (rubric-only) unless §5.7 is adopted.
4. The branch is merged only when the unit ledger is PASS, or its remaining gaps are named and agreed. B1-B4 must be resolved or
   named as honest gaps first, and the FC1 ledger gate (N3, Q11) is decided.

Architect decisions: pending (§12). This plan is the planner's proposal.

---

## Architect decisions

Pending. Each entry in §12 carries the planner's RECOMMENDED decision; the architect confirms or replaces each one before the builders
start. Until Q3 and Q5 are decided, L03 and L02 (the Texas Gulf branch) do not start. The L01, L04 and the project may start once
Q1, Q2, Q6 and Q7 are decided.

## Architect decisions (2026-11-03, binding). Where the plan states a recommendation for an open question, follow it. Defaults for every module: concepts outside the prerequisite closure are plain prose with no link and no dfn; registry keys whose record conflicts with the curriculum string are cited by key with the registry's own fields only or not at all (never edit a record, never type bibliographic data); no real data unless a redistributable source with a quoted reuse statement exists, otherwise SIMULATED with an honest-pending note and a DATA_REQUEST in plans/<UNIT>-open-items.md; no figures or new JS kernels; ten student-error mutants and five alternative correct implementations for every grader; not adversarial, no question bank. plans/FINAL-ARCHITECT-RULINGS.md and ~/.fanout/fixer-rules.md bind every builder. No reference is admitted in this batch: a statement whose source is a REFERENCE_REQUEST is not made, or it is taught as a model result with no attribution.
Module specifics: 4 lessons x 9 h + 14 h project; one lesson per builder. L03 names Dodd-Frank and MiFID II and says content not stated here; no legal source is admitted in this batch; holdings are graded C with key and locator where a registry key exists, the text is not legal advice; Dirks is cited by key with no year in prose; L02 patterns are labelled HYPOTHETICAL and later data SIMULATED. The LX2 merge waits for FC1's ledger to be PASS.
