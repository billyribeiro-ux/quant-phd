# PROPOSALS-L07: central edits for benchmark gap G8 (S7 L07)

Builder output for G8 (benchmarks/S7.md): minimum track-record length and a test of
two Sharpe ratios, in `course/modules/S/S7/L07.html` only. Everything below touches
shared files, which this branch does not change. Apply it centrally, then run
`tools/render_curriculum.py` and `tools/build_site.py`.

## 1. References admitted (run in the worktree; registry diff not committed)

Each command ran once, in this order, against Crossref with no email or personal
data. Every record matched its citation string, and the dry run printed the same record.

```bash
.venv/bin/python tools/add_reference.py --doi 10.1016/j.jempfin.2008.03.002 \
  --source "Ledoit & Wolf (2008), 'Robust Performance Hypothesis Testing with the Sharpe Ratio', Journal of Empirical Finance 15(5)" \
  --used-by S7
# ADDED ledoit2008robust -> 10.1016/j.jempfin.2008.03.002

.venv/bin/python tools/add_reference.py --doi 10.1111/j.1540-6261.1981.tb04891.x \
  --source "Jobson & Korkie (1981), 'Performance Hypothesis Testing with the Sharpe and Treynor Measures', JF 36(4)" \
  --used-by S7
# ADDED jobson1981performance -> 10.1111/j.1540-6261.1981.tb04891.x

.venv/bin/python tools/add_reference.py --doi 10.3905/jpm.2026.1.837 \
  --source "López de Prado, Lipton & Zoonekynd (2026), 'Sharpe Ratio Inference: A New Standard for Decision Making and Reporting', Journal of Portfolio Management 52(6)" \
  --used-by S7
# ADDED prado2026sharpe -> 10.3905/jpm.2026.1.837

.venv/bin/python tools/add_reference.py --doi 10.3905/jpm.2026.070 \
  --source "López de Prado & Porcu (2026), 'The Deflated Sharpe Ratio: A Unified Framework for Search-Adjusted Performance Inference', Journal of Portfolio Management" \
  --used-by S7
# ADDED prado2026deflated -> 10.3905/jpm.2026.070
```

After all four, `verify_refs.py --offline` reported "519 entries, 0 problems".
`prado2026deflated` is an online-first record: Crossref has no volume or issue
yet, and the page `jpm.2026.070`. The live `verify_refs.py` run will need its
volume and issue backfilled once JPM assigns them.

### What each source was read for, and where it is used

| Key | Read | Used in L07 | Grade |
|---|---|---|---|
| `bailey2012sharpe` (already in the registry) | Author version, "This version: July 2012" (davidhbailey.com/dhbpapers/sharpe-frontier.pdf): Section 1 p. 4, Section 3 Eq. (11), Section 4 Eqs. (12)–(13) and text, Section 5 p. 11, Appendix A.3 text and code | Remark 2.7 (definition and formula of MinTRL; observations, not calendar time; asymptotic basis; reported values 2.73/2.83/3.24/4.99 years and 59.895 months); Remark 2.10 (their claim of validity beyond iid) | T, T, T, C |
| `ledoit2008robust` | Working-paper version, IEW Zurich No. 320, January 2008 (econ.uzh.ch/apps/workingpapers/wp/iewwp320.pdf): Abstract, Sections 2, 3, 3.1, Remark 3.1, Sections 4–4.3, Table 1 | §5 (Ω of the corrected Jobson–Korkie test, T); §5 simulation finding and bootstrap proposal (B); Remark 2.10 (Opdyke's time-series formulae equal his iid ones, B); Remark 5.6 (HAC long-run covariance, T); key-results rows | T, B, B, T |
| `jobson1981performance` | Crossref record only. No abstract exists in Crossref, OpenAlex or RePEc, and the full text (Wiley, JSTOR) is closed | Cited jointly with `ledoit2008robust` in one T span in §5 that reports what Ledoit and Wolf say about the Jobson–Korkie test. The locator points at Ledoit and Wolf. No claim rests on Jobson and Korkie's text alone | T (via L&W) |
| `opdyke2007comparing` (already in the registry) | Abstract (RePEc IDEAS record of the article) | §5: a two-sample statistic without normality, simulated under fat tails, asymmetry and strong positive correlation; counter-evidence named (Ledoit and Wolf, Remark 2.10) | C |
| `prado2026sharpe` | Abstract via OpenAlex | Remark 1.5 (closed-form approximation under jointly non-normal, serially correlated returns, a problem they call long-standing and open; Lo's stationary derivation named as the counterweight); Remark 2.9 (pitfall: ignoring power and minimum sample length) | C, C |
| `prado2026deflated` | Abstract via OpenAlex | §3, after Example 3.2's paragraph: the original DSR as a location benchmark, and DSR-LS adding the dispersion of the selected maximum while staying compatible with PSR and MinTRL. R4 points to it without describing its mechanics | C |

Locators that cite a working-paper or author version say so ("working-paper
version of January 2008", "author version of July 2012"), following L07's
existing convention for `bailey2014deflated`.

### Not admitted

- **Memmel (2003), "Performance Hypothesis Testing with the Sharpe Ratio",
  Finance Letters 1, 21–23.** I searched Crossref (author and bibliographic
  queries) and OpenAlex: neither has a DOI or a record. Finance Letters is not on
  an allow-listed publisher domain in `references/authorities.yaml`, so
  `add_reference.py` has no admissible path. The page therefore never names Memmel.
  It speaks of "the corrected form that Ledoit and Wolf describe" and attributes the
  correction through `ledoit2008robust` (Abstract and Section 2). If the architect
  finds an authoritative page for the article, the §5 sentence can name Memmel and
  cite him.
- The other freshness flags in `ledgers/S7/L07-L08.json` (López de Prado & Porcu
  2026 SSRN on weak dependence; Sobti 2026 SSRN) are working papers I did not
  read. They are not used.

## 2. Curriculum edits (`curriculum/01-foundations.yaml`, module S7)

Add to `introduces:`, with each new line placed after the line named here:

```yaml
          minimum-track-record-length: "Minimum track-record length (MinTRL)"                              # after probabilistic-sharpe-ratio
          sharpe-ratio-difference-test: "Test of equal Sharpe ratios for two strategies on the same periods"  # after effective-number-of-trials
```

Pages that define them: `L07.html#def-minimum-track-record-length` (Definition 2.5)
and `L07.html#def-sharpe-ratio-difference-test` (Definition 5.3).

Add to `sources:`, after the Opdyke (2007) line:

```yaml
          - "Jobson & Korkie (1981), 'Performance Hypothesis Testing with the Sharpe and Treynor Measures', JF 36(4)"
          - "Ledoit & Wolf (2008), 'Robust Performance Hypothesis Testing with the Sharpe Ratio', Journal of Empirical Finance 15(5)"
          - "López de Prado, Lipton & Zoonekynd (2026), 'Sharpe Ratio Inference: A New Standard for Decision Making and Reporting', Journal of Portfolio Management 52(6)"
          - "López de Prado & Porcu (2026), 'The Deflated Sharpe Ratio: A Unified Framework for Search-Adjusted Performance Inference', Journal of Portfolio Management"
```

With these edits `render_curriculum.py` reported "25 parts, 134 modules, 157
projects, 13,695 h (6.34 FTE years)": the hours are unchanged, because I did not
change them in the branch.

### Hours: recommended change, not applied

L07 still declares `data-hours="7"`, and the hub still splits S7 as 56 lesson
hours and 24 project hours. G8 adds about 40% to L07. I estimated the added study
time with the item rates that reproduce L07's current 7 h:

| Added item | Estimate |
|---|---|
| MinTRL in §2: Definition 2.5, Proposition 2.6 and proof, Remark 2.7 with the reproduced numbers, Example 2.8, the years paragraph, Remarks 2.9–2.10 | 0.75 h |
| §5: Theorem 5.1 with its four-step proof, Corollary 5.2, Definition 5.3, Proposition 5.4 with proof, Example 5.5, Remark 5.6 | 0.75 h |
| Lab 4: three parts, run and interpret | 0.25 h |
| Six problems: M4 and M5 at about 10 min each, P4, P5 and E4 at about 20 min each, R4 at about 30 min | 1.7 h |
| Two misconceptions, four quiz items, key results | 0.15 h |
| **Total** | **≈ 3.5 h** |

Recommendation: raise L07 from 7 h to 10 h and S7 from 80 h to 83 h, keeping the
project at 24 h (29% of 83, inside the 10–40% rule). If adopted, these
non-central edits must land together, or `check_pages.py` fails:

- `course/modules/S/S7/L07.html`: `data-hours="10"`; eyebrow "S7 · Lesson 7 of 8 · 10 study hours".
- `course/modules/S/S7/index.html`: `data-hours-lessons="59"`; the hours-split aria-label and the bar; "80 hours" in the meta description and the eyebrow becomes 83; "Eight lessons of seven study hours each" becomes "Seven lessons of seven study hours and one of ten"; card kicker "L07 · 10 h".
- `curriculum/01-foundations.yaml`: S7 `hours: 83`, then re-render. Credential and program totals change by +3 h, and BLUEPRINT's tables must be re-copied from `render_curriculum.py`'s output (CLAUDE.md rule 5).

A smaller option is +2 h (L07 at 9 h, S7 at 82 h), treating R4 and E4 as stretch work.

## 3. New cards for `course/modules/S/S7/cards.json`

All for lesson L07; renumber the ids. Cards without a grade follow the existing
convention for definitions and misconceptions (for example S7-c089 and S7-c097).

```json
[
  {"id": "S7-cNEW-1", "lesson": "L07", "front": "Define the minimum track-record length (MinTRL).", "back": "The smallest number of observations at which \\(\\PSR(\\SR^\\ast)\\), with the estimates \\(\\hSR\\), \\(\\hat\\gamma_3\\), \\(\\hat\\gamma_4\\) held fixed, reaches \\(1-\\alpha\\). A record needs at least \\(\\lceil\\mathrm{MinTRL}\\rceil\\) observations (L07 Definition 2.5)."},
  {"id": "S7-cNEW-2", "lesson": "L07", "front": "Give the minimum track-record length in closed form, and say where its leading 1 comes from.", "back": "\\(\\mathrm{MinTRL} = 1 + \\hat b\\,\\big(z_{1-\\alpha}/(\\hSR - \\SR^\\ast)\\big)^2\\), with \\(\\hat b = 1 - \\hat\\gamma_3\\hSR + \\tfrac{\\hat\\gamma_4 - 1}{4}\\hSR^2\\): the PSR formula solved for \\(T\\). The 1 comes from the \\(T - 1\\) in PSR's standard error; this is Bailey and López de Prado's Eq. (13).", "grade": "T", "cite": ["bailey2012sharpe"]},
  {"id": "S7-cNEW-3", "lesson": "L07", "front": "With the estimates fixed, what does halving the margin \\(\\hSR - \\SR^\\ast\\) do to MinTRL?", "back": "It multiplies \\(\\mathrm{MinTRL} - 1\\) by 4, since \\(\\mathrm{MinTRL} - 1\\) is proportional to \\((\\hSR - \\SR^\\ast)^{-2}\\). As \\(\\hSR \\downarrow \\SR^\\ast\\), MinTRL diverges.", "grade": "T"},
  {"id": "S7-cNEW-4", "lesson": "L07", "front": "Roughly how many years of near-normal daily returns does \\(\\PSR(0)\\) need to reach 0.95, at an annualized Sharpe ratio of 1 and of 0.5?", "back": "About \\(z_{0.95}^2/\\SR_{\\text{ann}}^2\\): 2.7 years at 1 and 10.8 years at 0.5, for iid returns and before any search is priced.", "grade": "T"},
  {"id": "S7-cNEW-5", "lesson": "L07", "front": "A strategy's record runs exactly the MinTRL computed from its true Sharpe ratio and moments. How often does its PSR reach \\(1 - \\alpha\\)?", "back": "About half the time: the test statistic is centred on the critical value (49% of records in the L07 Lab 4 simulation). Power of 80% at 95% needs \\(T_\\beta - 1 = 2.29\\,(\\mathrm{MinTRL} - 1)\\).", "grade": "T"},
  {"id": "S7-cNEW-6", "lesson": "L07", "front": "How does positive autocorrelation change the minimum track-record length?", "back": "It lengthens it. \\(\\mathrm{MinTRL} - 1\\) is proportional to the variance of \\(\\hSR\\), and for AR(1) returns with a small Sharpe ratio the leading term of that variance grows by \\((1+\\phi)/(1-\\phi)\\): 1.86 at \\(\\phi = 0.3\\). The iid formula understates the record needed.", "grade": "T"},
  {"id": "S7-cNEW-7", "lesson": "L07", "front": "For iid pairs of returns, what is the asymptotic variance \\(\\theta\\) of \\(\\sqrt{T}(\\hSR_1 - \\hSR_2)\\)?", "back": "\\(\\theta = \\Var(\\psi_1 - \\psi_2)\\) with \\(\\psi_i = u_i - \\tfrac{\\SR_i}{2}(u_i^2 - 1)\\), \\(u_i\\) the standardized return: \\(V_1 + V_2 - 2\\rho + \\SR_1\\kappa_{21} + \\SR_2\\kappa_{12} - \\tfrac12\\SR_1\\SR_2(\\kappa_{22} - 1)\\), where \\(\\kappa_{ab} = \\E[u_1^a u_2^b]\\).", "grade": "T"},
  {"id": "S7-cNEW-8", "lesson": "L07", "front": "What is the corrected Jobson–Korkie variance of a Sharpe-ratio difference?", "back": "For iid bivariate-normal returns, \\(\\theta = 2(1-\\rho) + \\tfrac12(\\SR_1^2 + \\SR_2^2) - \\SR_1\\SR_2\\rho^2\\), divided by \\(T\\): the normal special case of the general delta-method variance.", "grade": "T", "cite": ["ledoit2008robust"]},
  {"id": "S7-cNEW-9", "lesson": "L07", "front": "What goes wrong if two correlated strategies' Sharpe ratios are tested as if the strategies were independent?", "back": "The test uses \\(V_1 + V_2\\) instead of \\(\\theta\\). Under positive correlation it is undersized and nearly powerless (no rejections in 4000 samples at \\(\\rho = 0.9\\) in the L07 Lab 4 simulation); under negative correlation it rejects a true null too often.", "grade": "T"},
  {"id": "S7-cNEW-10", "lesson": "L07", "front": "How does the paired test of two Sharpe ratios relate to White's Reality Check?", "back": "It is the \\(K = 1\\) case: one challenger against a benchmark. Picking the best of \\(K\\) strategies by Sharpe ratio and then running the paired test on it is data snooping; the Reality Check, with statistic \\(\\max_k \\sqrt{T}(\\hSR_k - \\hSR_0)\\), prices the search."},
  {"id": "S7-cNEW-11", "lesson": "L07", "front": "What do Ledoit and Wolf (2008) find about the corrected Jobson–Korkie test, and what do they propose instead?", "back": "In simulations with 120 observations it rejects a true null too often under heavy tails or serial dependence, and HAC standard errors are often liberal. They propose a studentized time-series bootstrap interval for the difference, which works well for iid and time-series data in their designs.", "grade": "B", "cite": ["ledoit2008robust"]},
  {"id": "S7-cNEW-12", "lesson": "L07", "front": "Misconception: “A record longer than MinTRL proves skill.” Why is it wrong?", "back": "Computed from the record's own estimates, MinTRL restates the PSR test: a longer record rejects \\(\\SR \\le \\SR^\\ast\\) at level \\(\\alpha\\), which is not a probability of skill. Computed from a true Sharpe ratio, it is a break-even length that passes only about half the time."},
  {"id": "S7-cNEW-13", "lesson": "L07", "front": "Misconception: “Two Sharpe ratios whose confidence intervals overlap cannot be told apart.” Why is it wrong?", "back": "The standard error of the difference depends on the correlation. In L07 Example 5.5 each annualized Sharpe ratio has a standard error of about 0.45, yet a difference of 0.32 is significant (p = 0.025), because \\(\\hat\\rho = 0.95\\) makes the paired standard error 4.5 times smaller than the naive one."},
  {"id": "S7-cNEW-14", "lesson": "L07", "front": "What is DSR-LS?", "back": "A deflated-Sharpe-ratio variant proposed by López de Prado and Porcu (2026). It adds the dispersion of the selected maximum to the original location benchmark, keeping a form compatible with PSR and MinTRL.", "grade": "C", "cite": ["prado2026deflated"]}
]
```

## 4. Other central items

- **Glossary and concept index.** `build_site.py` picks up the two new concepts
  automatically once the curriculum edit lands. The checked run regenerated
  `course/assets/data/glossary.json`, `program.json`, `references.json`,
  `course/concepts.html` and `course/index.html`; none of those changes is committed.
- **Notation (optional).** The page writes MinTRL as `\mathrm{MinTRL}`, just as the
  registered `\PSR` expands to `\mathrm{PSR}`. If MinTRL is to be used
  program-wide, register `\MinTRL` → `\mathrm{MinTRL}` in `notation/notation.json`
  ("minimum track-record length, in observations"). No page needs it now.
- **Hub card (optional).** The L07 card on `course/modules/S/S7/index.html` could
  read: "The Sharpe ratio's variance under skewness and kurtosis, the probabilistic
  and deflated Sharpe ratios, the minimum track-record length, the effective number
  of trials, and a paired test of two Sharpe ratios." I left the hub untouched to
  avoid merge conflicts with other gap builders.
- **Ledger.** `ledgers/S7/L07-L08.json` (round 6, PASS 136/136) predates these
  changes. L07 needs re-verification of the new rows: Definition 2.5 to Remark 2.10,
  §5, Lab 4, M4, M5, P4, P5, E4, R4, misconceptions 5–6, quiz items 12–15 and the
  new key-results rows. It also needs re-checking of the renumbered sections
  (old §5–§11 are now §6–§12) and the small edits to Remark 1.5, §3, the "why it
  matters" paragraph and the canon-breaks dependence bullet.
- **Cross-references kept stable.** §1–§4 and every block in them keep their
  numbers, so S7-c069 ("L07 Proposition 4.2"), S7-c090 ("L07 Definition 4.1") and
  L08's "Lesson 7, Section 4" stay correct. No page links to L07's `#s5`–`#s11`.

## 5. A8 project: rung-4 stretch suggestion (the contract is unchanged)

Do not change the A8 contract, grader or reference. A stretch item for
`project.html` rung 4:

> **Track-record length and paired comparisons.** Add, outside `atlas.integrity`'s
> frozen API, `min_track_record_length(returns, sr_benchmark=0.0, alpha=0.05) ->
> float` (L07 Proposition 2.6: `1 + bracket * (z/(SR - SR*))**2`, raising
> `ValueError` when `SR <= SR*`) and `sharpe_difference_test(returns_1, returns_2,
> normal=False) -> tuple[float, float]` returning (Z, two-sided p) with the paired
> variance (4) or (5) and the `T - 1` convention of Definition 5.3. Check MinTRL
> against Bailey and López de Prado's 59.895 months (Remark 2.7), and the paired
> test's size by repeating Lab 4, Part 2.

A future contract version could adopt both functions through
`CONTRACT_CHANGE_REQUESTS`. I am not requesting that now.
