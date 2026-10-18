# PROPOSALS-L01: central edits for gap G7 (anytime-valid inference), S7 L01

Branch `worktree-agent-a7b15d7e14bc99240`. The lesson (`course/modules/S/S7/L01.html`) and its
new lab twin (`tests/labs/S7/lab-S7-L01-4.py`) are committed. Everything below is central and is
**not** in the branch: apply it, then regenerate with `tools/render_curriculum.py` and
`tools/build_site.py`. Until it is applied, `check_pages --unit S7` fails on the hours split
(L01 declares 10 h, the hub still says 56 lesson hours, the curriculum 80 h) and on the eight new
citation keys, which are not yet in the registry. With all of it applied, every gate passed in the
worktree (see the report).

## 1. References admitted

Each was admitted by DOI from Crossref with `tools/add_reference.py` in the worktree, after a
`--dry-run` with the same arguments. The commands, exactly as run, and the keys they produced:

```bash
.venv/bin/python tools/add_reference.py --doi 10.1214/23-STS894 --source "Ramdas, Grünwald, Vovk & Shafer (2023), 'Game-Theoretic Statistics and Safe Anytime-Valid Inference', Statistical Science 38(4)" --used-by S7
# ADDED ramdas2023game -> 10.1214/23-sts894
.venv/bin/python tools/add_reference.py --doi 10.1214/20-AOS1991 --source "Howard, Ramdas, McAuliffe & Sekhon (2021), 'Time-Uniform, Nonparametric, Nonasymptotic Confidence Sequences', Annals of Statistics 49(2)" --used-by S7
# ADDED howard2021time -> 10.1214/20-aos1991
.venv/bin/python tools/add_reference.py --doi 10.1214/aoms/1177696786 --source "Robbins (1970), 'Statistical Methods Related to the Law of the Iterated Logarithm', Annals of Mathematical Statistics 41(5)" --used-by S7
# ADDED robbins1970statistical -> 10.1214/aoms/1177696786
.venv/bin/python tools/add_reference.py --doi 10.2307/2343787 --source "Armitage, McPherson & Rowe (1969), 'Repeated Significance Tests on Accumulating Data', Journal of the Royal Statistical Society Series A (General) 132(2)" --used-by S7
# ADDED armitage1969repeated -> 10.2307/2343787
.venv/bin/python tools/add_reference.py --doi 10.1287/opre.2021.2135 --source "Johari, Koomen, Pekelis & Walsh (2022), 'Always Valid Inference: Continuous Monitoring of A/B Tests', Operations Research 70(3)" --used-by S7
# ADDED johari2022always -> 10.1287/opre.2021.2135
.venv/bin/python tools/add_reference.py --doi 10.1093/biomet/64.2.191 --source "Pocock (1977), 'Group Sequential Methods in the Design and Analysis of Clinical Trials', Biometrika 64(2)" --used-by S7
# ADDED pocock1977group -> 10.1093/biomet/64.2.191
.venv/bin/python tools/add_reference.py --doi 10.2307/2530245 --source "O'Brien & Fleming (1979), 'A Multiple Testing Procedure for Clinical Trials', Biometrics 35(3)" --used-by S7
# ADDED obrien1979multiple -> 10.2307/2530245
.venv/bin/python tools/add_reference.py --doi 10.1093/biomet/70.3.659 --source "Lan & DeMets (1983), 'Discrete Sequential Boundaries for Clinical Trials', Biometrika 70(3)" --used-by S7
# ADDED lan1983discrete -> 10.1093/biomet/70.3.659
```

After admission, `tools/verify_refs.py --offline` reported 523 entries, 0 problems.

Notes on admission:

- **Armitage et al.** A first dry run with the venue `JRSS-A 132(2)` was rejected (`venue=False`):
  `tools/refs/journals.py` has `JRSS-B` but no `JRSS-A`. The full venue name above passes. If you
  prefer the short house form, add `JRSS-A` to the journal table (central tooling); I did not.
- **Lan & DeMets, display.** Crossref records the first author's family name as `GORDON LAN`
  (given `K. K.`). `build_site.py` therefore renders the short cite as "Gordon Lan & DeMets (1983)"
  and the full entry as "Gordon Lan, K. K.; DeMets, David L.". The key (`lan1983discrete`) is
  right. A display fix needs a central decision (for example a family-name override honoured by
  `family_name()` in `build_site.py`); I made none.
- **Pocock.** Crossref's `POCOCK` renders as "Pocock" through the source string, as intended.

How each source was read (no email or personal data was sent in any request; Crossref requests
carried the tool's neutral User-Agent):

| Key | Abstract read via | Full text read | Locators used on the page |
|---|---|---|---|
| ramdas2023game | Crossref abstract | arXiv:2210.01948v2 (17 June 2023, "Submitted to Statistical Science") | Abstract; Sections 2.1, 2.2, 2.4, 2.5 (Eq. 8), 2.8, 2.9, 2.10, 4.1.2, 5.1 (Eqs. 21–22), 5.2, 5.3, 5.8, 6.2, each marked "(arXiv v2, 2023)" |
| howard2021time | Crossref abstract | arXiv:1810.08240v9 (6 Aug 2022) | Section 1; Section 3.2, Eq. (14); Proposition 3 and Section 3.5; Lemma 3 and Section 6, each marked "(arXiv v9, 2022)". Ramdas et al. (2023) cite "Howard et al. (2021, Lemma 3)", which confirms that numbering in the published version |
| johari2022always | Crossref abstract | arXiv:1512.04922 (read for context only) | Abstract only |
| armitage1969repeated | OpenAlex `abstract_inverted_index` (no abstract on Crossref). The text OpenAlex holds is the paper's opening, on p. 235 | Not reachable (JSTOR/Wiley) | p. 235 |
| robbins1970statistical | OpenAlex (opening of Section 1, p. 1397) | Project Euclid PDF blocked (HTTP challenge page) | p. 1397, Section 1 |
| pocock1977group | OpenAlex | Not reachable | Abstract |
| obrien1979multiple | OpenAlex | Not reachable | Abstract |
| lan1983discrete | OpenAlex | Not reachable | Abstract |

Locators that point into an arXiv version follow the L07 precedent ("author version of July
2014"). A verifier should confirm them against the published versions; any renumbering in the
published Statistical Science article would need a locator change.

## 2. Curriculum edits (`curriculum/01-foundations.yaml`, module S7)

**Hours: 80 → 83.** L01 grows from 7 to 10 study hours; the project stays at 24 h (A8 contract,
grader and project are unchanged), so lessons go from 56 to 59 h and the project share from 30.0%
to 28.9%. Justification, itemized for an M-tier student:

| New material | Estimate |
|---|---|
| §6 reading: Propositions 6.1 and 6.6, Theorem 6.4 and Corollary 6.5 with full proofs; Definition 6.3; Example 6.7; Remarks 6.2, 6.8, 6.9 | 60 min |
| Lab 4: run, read both tables, interpretation | 15 min |
| Problems M4 (15), M5 (25), P4 (15), R4 (30) | 85 min |
| New misconception and four quiz items | 5 min |
| **Itemized total** | **165 min ≈ 2.75 h** |

The same itemization of the existing L01 (sections 1–5, Labs 1–3, twelve problems, ten quiz
items) gives about 5.2 h against its declared 7 h, a ratio of 1.35; applied to 2.75 h that is
3.7 h. I propose +3 h. It is a design target like every other figure; pilot data should recalibrate
it.

**Introduces** (append to S7's `introduces`; each is defined once in L01 with `<dfn>`):

```yaml
          repeated-significance-testing: "Repeated significance testing (peeking) and its type I error inflation"
          e-value: "E-value"
          test-supermartingale: "Test supermartingale"
          ville-inequality: "Ville's inequality"
          anytime-valid-inference: "Anytime-valid inference"
          confidence-sequence: "Confidence sequence (time-uniform confidence interval)"
          alpha-spending: "Group-sequential design and alpha spending"
```

No existing concept in the curriculum collides with these ids or labels (checked by searching every
`curriculum/*.yaml`).

**Uses** (append to S7's `uses`; all are in S7's prerequisite closure and L01 now links them):

```yaml
          - confidence-interval                  # S1
          - conditional-expectation-elementary   # M4
          - law-of-large-numbers                 # M4
```

**Sources** (append to S7's `sources`, in this exact form; they are the `--source` strings above):

```yaml
          - "Armitage, McPherson & Rowe (1969), 'Repeated Significance Tests on Accumulating Data', Journal of the Royal Statistical Society Series A (General) 132(2)"
          - "Robbins (1970), 'Statistical Methods Related to the Law of the Iterated Logarithm', Annals of Mathematical Statistics 41(5)"
          - "Pocock (1977), 'Group Sequential Methods in the Design and Analysis of Clinical Trials', Biometrika 64(2)"
          - "O'Brien & Fleming (1979), 'A Multiple Testing Procedure for Clinical Trials', Biometrics 35(3)"
          - "Lan & DeMets (1983), 'Discrete Sequential Boundaries for Clinical Trials', Biometrika 70(3)"
          - "Howard, Ramdas, McAuliffe & Sekhon (2021), 'Time-Uniform, Nonparametric, Nonasymptotic Confidence Sequences', Annals of Statistics 49(2)"
          - "Johari, Koomen, Pekelis & Walsh (2022), 'Always Valid Inference: Continuous Monitoring of A/B Tests', Operations Research 70(3)"
          - "Ramdas, Grünwald, Vovk & Shafer (2023), 'Game-Theoretic Statistics and Safe Anytime-Valid Inference', Statistical Science 38(4)"
```

**What `render_curriculum.py` reported with these edits** (copied from its output and from
`git diff -U0 -- CURRICULUM.md`; on the merge base, before any other worker's edits):

```
curriculum valid: 25 parts, 134 modules, 157 projects, 13,698 h (6.34 FTE years)
```

| Figure in CURRICULUM.md | Before | After |
|---|---|---|
| Concepts (each introduced exactly once) | 1,121 | 1,128 |
| Total design hours | 13,695 | 13,698 |
| Master's in Finance / Financial Engineering, hours | 7,646 | 7,649 (≈170 credits, 3.54 FTE years, unchanged) |
| PhD in Finance, hours | 9,171 | 9,174 (≈204 credits, 4.25, unchanged) |
| Course map "Financial Econometrics" (S3, S4, S7) | 290 | 293 |
| Tier M hours | 5,770 | 5,773 |
| Master's-Equivalent milestone | 11,135 (5.16) | 11,138 (5.16) |
| Doctoral Candidate milestone | 12,495 (5.78) | 12,498 (5.79) |
| Doctoral milestone | 13,695 (6.34) | 13,698 (6.34) |
| Quantitative Researcher track | 4,056 (1.88) | 4,059 (1.88) |
| Quant Developer track | 3,756 (1.74) | 3,759 (1.74) |
| Research doctorate path | 5,626 (2.60) | 5,629 (2.61) |
| S7 line | 80 h | 83 h |

If other G-gap workers also change S7's hours, these figures must be re-rendered from the combined
sources, not added by hand.

## 3. Hub edits (`course/modules/S/S7/index.html`)

Kept out of the branch because every S7 lesson worker touches the same hours line. Required:

```diff
-    <main id="main" class="prose" data-hours-lessons="56" data-hours-project="24">
+    <main id="main" class="prose" data-hours-lessons="59" data-hours-project="24">
-<span class="card-kicker">L01 · 7 h</span>
+<span class="card-kicker">L01 · 10 h</span>
-...the extreme-value approximation, holdout reuse.</span>
+...the extreme-value approximation, holdout reuse, and anytime-valid monitoring of a live record.</span>
```

Optional (not applied anywhere): an eighth objective, which keeps the hub within 4–8:
"**Prove** Ville's inequality and **build** an anytime-valid monitor for a live track record,
**stating** what its guarantee assumes about the scale and tails of returns."

## 4. New retrieval cards (`course/modules/S/S7/cards.json`)

Twelve cards for L01, to be renumbered from S7-c109. With them appended as S7-c109 to S7-c120,
`check_pages --unit S7` passed (cards check included). Theorem cards are grade T; the definition
and misconception cards carry no grade, like S7-c001 and S7-c009; the lab card names its basis
exactly as the key-results row does.

```json
[
  {"id": "S7-cNEW-1", "lesson": "L01", "front": "Define an e-value for a null hypothesis \\(H_0\\).", "back": "A random variable \\(E \\ge 0\\) with \\(\\E_0[E] \\le 1\\) under every distribution in \\(H_0\\). By Markov's inequality, \\(\\Prob_0(E \\ge 1/\\alpha) \\le \\alpha\\)."},
  {"id": "S7-cNEW-2", "lesson": "L01", "front": "Define a test supermartingale for \\(H_0\\).", "back": "A sequence with \\(M_0 = 1\\), \\(M_t \\ge 0\\), each \\(M_t\\) a function of \\(Y_1, \\dots, Y_t\\), and \\(\\E_0[M_t \\mid Y_1, \\dots, Y_{t-1}] \\le M_{t-1}\\) under every null distribution: the wealth of a gambler who bets against \\(H_0\\) at odds fair or worse and never borrows."},
  {"id": "S7-cNEW-3", "lesson": "L01", "front": "State Ville's inequality.", "back": "If \\((M_t)\\) is a test supermartingale for \\(H_0\\) and \\(\\alpha \\in (0,1)\\), then \\(\\Prob_0(\\sup_t M_t \\ge 1/\\alpha) \\le \\alpha\\): the bound Markov's inequality gives for one fixed day holds for the whole path.", "grade": "T"},
  {"id": "S7-cNEW-4", "lesson": "L01", "front": "Under the null, how does the probability that a fixed-level z-test rejects at some look depend on the number of looks?", "back": "It rises strictly with every look and tends to 1, by the law of the iterated logarithm (Proposition 6.1). For equally spaced looks it depends only on their number.", "grade": "T", "cite": ["armitage1969repeated"]},
  {"id": "S7-cNEW-5", "lesson": "L01", "front": "Why may an analyst stop whenever they like if they reject when a test supermartingale reaches \\(1/\\alpha\\)?", "back": "For any random time \\(\\tau\\), however chosen, \\(\\{M_\\tau \\ge 1/\\alpha\\} \\subseteq \\{\\sup_t M_t \\ge 1/\\alpha\\}\\), so Ville's inequality bounds the type I error by \\(\\alpha\\) (Corollary 6.5).", "grade": "T"},
  {"id": "S7-cNEW-6", "lesson": "L01", "front": "Give the normal-mixture monitor for standardized returns \\(Y_t \\sim \\Normal(\\SR, 1)\\) with mixing precision \\(\\kappa\\).", "back": "\\(M_t = \\sqrt{\\kappa/(\\kappa+t)}\\,\\exp\\big(S_t^2/(2(\\kappa+t))\\big)\\), the average of the likelihood ratios \\(e^{\\lambda S_t - \\lambda^2 t/2}\\) over \\(\\lambda \\sim \\Normal(0, 1/\\kappa)\\). It is a test martingale under \\(\\SR = 0\\).", "grade": "T", "cite": ["ramdas2023game", "howard2021time"]},
  {"id": "S7-cNEW-7", "lesson": "L01", "front": "When does the normal-mixture monitor reject at level \\(\\alpha\\), and what hurdle is that after three years of daily data?", "back": "When \\(|S_t| \\ge b_t = \\sqrt{(\\kappa+t)\\,(2\\ln(1/\\alpha) + \\ln(1 + t/\\kappa))}\\). At \\(\\alpha = 0.05\\), \\(\\kappa = 252\\), \\(t = 756\\) it is a z-hurdle of 3.136, against 1.960 for one planned test.", "grade": "T"},
  {"id": "S7-cNEW-8", "lesson": "L01", "front": "What distinguishes a confidence sequence from a confidence interval?", "back": "A confidence interval covers the truth with probability \\(1-\\alpha\\) at one sample size fixed in advance; a confidence sequence covers it at all times at once, so it stays valid under continuous monitoring. Example: \\(C_t = [(S_t - b_t)/t,\\ (S_t + b_t)/t]\\)."},
  {"id": "S7-cNEW-9", "lesson": "L01", "front": "What does a group-sequential (alpha-spending) design need that an anytime-valid monitor does not?", "back": "A fixed total \\(\\alpha\\) divided among the looks it budgets for: Pocock and O'Brien–Fleming fix the number of looks, Lan and DeMets a rate of spending. A look beyond the budget raises the error above \\(\\alpha\\). The monitor needs no budget and pays with a wider boundary.", "grade": "T", "cite": ["pocock1977group", "obrien1979multiple", "lan1983discrete"]},
  {"id": "S7-cNEW-10", "lesson": "L01", "front": "In Lab 4 (SIMULATED), how long did the anytime-valid monitor take to confirm a true annualized Sharpe ratio of 1?", "back": "A median of 7.20 years, against 3.84 years for one pre-planned z-test to reach even odds of detection: about 1.9 times as long (2.3 times at a Sharpe ratio of 2).", "basis": "Lab 4 (SIMULATED)"},
  {"id": "S7-cNEW-11", "lesson": "L01", "front": "Misconception: “I check my strategy's t-statistic daily and will stop the first time it is significant at 5%; the 5% error rate still applies.” Why is it wrong?", "back": "The 5% belongs to one look fixed in advance. Under the null the chance of crossing at some look rises with every look and tends to one (Proposition 6.1); Lab 4 puts it at 0.51 for daily looks over three years. Stopping when the evidence looks good needs an anytime-valid statistic, such as an e-value compared with \\(1/\\alpha\\)."},
  {"id": "S7-cNEW-12", "lesson": "L01", "front": "Which input of the normal-mixture monitor cannot be learned from the data when returns are unbounded, and what still extends?", "back": "The scale: a sub-Gaussian parameter or a variance bound must be supplied in advance. With it the monitor stays valid for conditionally sub-Gaussian returns, and a test supermartingale of Wang and Ramdas covers heavy tails with a known variance bound; with an estimated scale the guarantee is only asymptotic.", "grade": "T", "cite": ["ramdas2023game"]}
]
```

## 5. DAG note: martingale theory is not an S7 prerequisite

M6 introduces `martingale`, `stopping-time`, `optional-stopping-theorem` and
`doob-maximal-inequality`, but M6 is **not** in S7's prerequisite closure (S7 ← S1, S2, S3; the
closure is CS1, M1–M4, P0.1, S0–S3). The lesson is therefore built to need none of them:

- test supermartingales are defined directly from M4's `conditional-expectation-elementary`
  (linked), as an S7 concept;
- Ville's inequality is proved from first principles, with a "frozen wealth" process and the tower
  property, without naming optional stopping or Doob's inequality;
- anytime validity (Corollary 6.5) is stated for **arbitrary random times**, which is stronger than
  the stopping-time version and needs no stopping-time concept; Howard et al.'s Lemma 3 is cited for
  the equivalence, phrased as "a time chosen by a rule that sees only the data so far".

No page links an M6 concept, and `check_dag --unit S7` passes. The words "martingale" and
"supermartingale" appear only inside the S7 concept "test (super)martingale", which the page
defines in full. If you would rather link M6, the alternative is to add M6 to S7's `prereqs`.
I computed its effect on `curriculum.json`: no credential or track changes hours (MS-FIN and
PHD-FIN already contain both, and every track whose closure contains S7 already contains M6), but
S7's own closure grows by M5 and M6 (280 h). I recommend keeping the page as built.

## 6. Other central items

- **BLUEPRINT.md and README.md quote figures that change** (rule 5 of CLAUDE.md: re-render and copy
  them; do not type them): BLUEPRINT §1.1 (7,646 and 9,171), §2 milestones table (11,135; 12,495
  and 5.78; 13,695) and §2 item 2 ("1,121 concepts"); README lines 30, 53, 54 and 65 (1,121;
  7,646; 9,171).
- **Regenerate** after applying §§1–4: `CURRICULUM.md`, `curriculum/curriculum.json`,
  `course/assets/data/*`, `course/index.html`, `course/concepts.html`.
- **benchmarks/S7.md** lists G7 as open; once merged it can point to L01 §6. I did not edit it.
- **No live figure** was added (optional in the brief). A figure of the normalized boundary
  \(b_t/\sqrt t\) against \(c\) would need a new kernel in the shared `course/assets/js/stats.js`
  with a test in `tests/test_figure_kernels.py`; I left both shared files untouched.
- **NOTATION_REQUESTS: none.** New symbols are local to §6 and defined there (\(Y_t, S_t, Z_t, c,
  p_n, M_t, E, h, W_n, \kappa, \lambda, L_t, \varphi_\kappa, b_t, C_t, \tau\)). \(\SR\) keeps its
  registered meaning (per-period population Sharpe ratio); \(\rho\) is not reused, because L01
  already uses it for equicorrelation.
