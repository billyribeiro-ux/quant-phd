# Proposals for central files: L03–L04 gap work (G4, G6, G9, G12)

Branch `worktree-g6-g4`. Lesson pages, lab twins and checked snippets are committed on the branch. Everything
below is a central file (registry, curriculum, cards) that the branch does not carry. Apply it centrally, then
regenerate. The lesson pages cite the registry keys and define the concepts listed here, so `check_pages`,
`check_dag` and the cards check fail until it is applied.

Every gate in CLAUDE.md that touches these files passed with the edits below applied temporarily. The
exception is the live registry check, which had three network errors on unrelated entries (see "Gate
results").

## 1. Registry: add_reference.py commands

Each command was run in the worktree exactly as written. DOIs were looked up on the Crossref API and abstracts
read on Crossref or OpenAlex, with no email address or other personal data. The Clark–McCracken abstract
appears only on RePEc, as a copy of another version, so L04 cites that paper at title level only. The
Fan–Liao–Yao abstract was read on the Econometric Society's page for the article.

| # | Command | Result |
|---|---|---|
| 1 | `python3 tools/add_reference.py --doi 10.1080/07350015.1995.10524599 --source "Diebold & Mariano (1995), 'Comparing Predictive Accuracy', JBES 13(3)" --used-by S7` | ADDED `diebold1995comparing` |
| 2 | `python3 tools/add_reference.py --doi 10.2307/1913610 --source "Newey & West (1987), Econometrica 55(3)" --used-by S7` | UPDATED `newey1987simple` (used_by S2 → S2, S7) |
| 3 | `python3 tools/add_reference.py --doi 10.1198/016214501753382129 --source "Efron, Tibshirani, Storey & Tusher (2001), 'Empirical Bayes Analysis of a Microarray Experiment', JASA 96(456)" --used-by S7` | ADDED `efron2001empirical` |
| 4 | `python3 tools/add_reference.py --doi 10.1198/016214504000000089 --source "Efron (2004), 'Large-Scale Simultaneous Hypothesis Testing: The Choice of a Null Hypothesis', JASA 99(465)" --used-by S7` | ADDED `efron2004large` |
| 5 | `python3 tools/add_reference.py --doi 10.1214/07-sts236 --source "Efron (2008), 'Microarrays, Empirical Bayes and the Two-Groups Model', Statistical Science 23(1)" --used-by S7` | ADDED `efron2008microarrays` |
| 6 | `python3 tools/add_reference.py --doi 10.1080/01621459.1973.10481350 --source "Efron & Morris (1973), 'Stein's Estimation Rule and Its Competitors—An Empirical Bayes Approach', JASA 68(341)" --used-by S7` | ADDED `efron1973steins` |
| 7 | `python3 tools/add_reference.py --doi 10.1080/01621459.1975.10479864 --source "Efron & Morris (1975), 'Data Analysis Using Stein's Estimator and Its Generalizations', JASA 70(350)" --used-by S7` | ADDED `efron1975data` |
| 8 | `python3 tools/add_reference.py --doi "10.1016/s0304-4076(01)00071-9" --source "Clark & McCracken (2001), 'Tests of Equal Forecast Accuracy and Encompassing for Nested Models', Journal of Econometrics 105(1)" --used-by S7` | ADDED `clark2001tests` |
| 9 | `python3 tools/add_reference.py --doi 10.1111/j.1468-0262.2006.00718.x --source "Giacomini & White (2006), 'Tests of Conditional Predictive Ability', Econometrica 74(6)" --used-by S7` | ADDED `giacomini2006tests` |
| 10 | `python3 tools/add_reference.py --doi 10.1080/07350015.2014.983236 --source "Diebold (2015), 'Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on the Use and Abuse of Diebold–Mariano Tests', JBES 33(1)" --used-by S7` | ADDED `diebold2015comparing` |
| 11 | `python3 tools/add_reference.py --doi 10.1080/07350015.1998.10524759 --source "Harvey, Leybourne & Newbold (1998), 'Tests for Forecast Encompassing', JBES 16(2)" --used-by S7` | ADDED `harvey1998tests` |
| 12 | `python3 tools/add_reference.py --doi 10.1057/jors.1969.103 --source "Bates & Granger (1969), 'The Combination of Forecasts', Journal of the Operational Research Society 20(4)" --used-by S7` | ADDED `bates1969combination` |
| 13 | `python3 tools/add_reference.py --doi 10.3982/ecta12749 --source "Fan, Liao & Yao (2015), 'Power Enhancement in High-Dimensional Cross-Sectional Tests', Econometrica 83(4)" --used-by S7` | ADDED `fan2015power` |
| 14 | `python3 tools/add_reference.py --doi 10.1214/009053604000000265 --source "Donoho & Jin (2004), 'Higher Criticism for Detecting Sparse Heterogeneous Mixtures', Annals of Statistics 32(3)" --used-by S7` | ADDED `donoho2004higher` |
| 15 | `python3 tools/add_reference.py --doi 10.1198/jasa.2011.tm11181 --source "Efron (2011), 'Tweedie's Formula and Selection Bias', JASA 106(496)" --used-by S7` | ADDED `efron2011tweedies` |

### Keys, with DOI, record and where they are cited

| Key | DOI | Record (as admitted) | Cited in |
|---|---|---|---|
| `diebold1995comparing` | 10.1080/07350015.1995.10524599 | JBES 13(3), 253–263, 1995 | L04 §1 (Abstract) |
| `newey1987simple` | 10.2307/1913610 | Econometrica 55(3), 703, 1987 (existing, S2) | L04 §1 (Abstract); key results |
| `clark2001tests` | 10.1016/s0304-4076(01)00071-9 | Journal of Econometrics 105(1), 85–110, 2001 | L04 Remark 1.4 (Title) |
| `giacomini2006tests` | 10.1111/j.1468-0262.2006.00718.x | Econometrica 74(6), 1545–1578, 2006 | L04 Remark 1.4 (Abstract) |
| `diebold2015comparing` | 10.1080/07350015.2014.983236 | JBES 33(1), 2015 | L04 Remark 1.4 (Abstract) |
| `harvey1998tests` | 10.1080/07350015.1998.10524759 | JBES 16(2), 254–259, 1998 | L04 Remark 1.6 (Abstract) |
| `bates1969combination` | 10.1057/jors.1969.103 | Journal of the Operational Research Society 20(4), 451–468, 1969 | L04 Remark 1.6 (Abstract) |
| `fan2015power` | 10.3982/ecta12749 | Econometrica 83(4), 1497–1541, 2015 (no print date on Crossref; the issued year 2015 is shown) | L04 Remark 4.3 (Abstract) |
| `donoho2004higher` | 10.1214/009053604000000265 | Annals of Statistics 32(3), 962–994, 2004 | L04 Remark 4.3 (Abstract) |
| `efron2001empirical` | 10.1198/016214501753382129 | JASA 96(456), 1151–1160, 2001 | L03 Remark 7.5 (Abstract) |
| `efron2004large` | 10.1198/016214504000000089 | JASA 99(465), 96–104, 2004 | L03 §7 and Remark 7.5 (Abstract) |
| `efron2008microarrays` | 10.1214/07-sts236 | Statistical Science 23(1), 1–22, 2008 | L03 §7 (Abstract) |
| `efron2011tweedies` | 10.1198/jasa.2011.tm11181 | JASA 106(496), 1602–1614, 2011 | L03 §7 (Abstract); key results; one card |
| `efron1973steins` | 10.1080/01621459.1973.10481350 | JASA 68(341), 117–130, 1973 | L03 §7 (Abstract) |
| `efron1975data` | 10.1080/01621459.1975.10479864 | JASA 70(350), 311–319, 1975 | L03 §7 (Abstract) |

Notes:

- **Efron & Morris (1973):** Crossref holds two DOIs for the same article, JSTOR 10.2307/2284155 (page "117"
  only) and Taylor & Francis 10.1080/01621459.1973.10481350 (pages 117–130). The second was admitted.
- **James & Stein (1961):** not admitted. Efron & Morris (1975) attribute the 1961 estimator in their
  abstract, and L03 cites that attribution.
- **Excluded:** West (1996) and Harvey, Leybourne & Newbold (1997) were looked up and not admitted, because
  nothing in the lessons needs them.

## 2. Curriculum: `curriculum/01-foundations.yaml`, entry S7

Add four concepts to `introduces`. Place the first three after `benjamini-yekutieli` and the fourth after
`expected-maximum-sharpe`, so the list keeps lesson order:

```yaml
          two-group-model: "Two-group model for large-scale testing"            # L03 Definition 7.1
          local-fdr: "Local false discovery rate (lfdr)"                        # L03 Definition 7.2
          empirical-bayes-shrinkage: "Empirical Bayes shrinkage of many Sharpe ratios"  # L03 Definition 7.7
          diebold-mariano-test: "Diebold–Mariano test of equal predictive accuracy"     # L04 Definition 1.2
```

Append these strings to `sources`, after the Gelman & Loken (2014) entry. Each one matches its admitted
registry record exactly.

```yaml
          - "Diebold & Mariano (1995), 'Comparing Predictive Accuracy', JBES 13(3)"
          - "Newey & West (1987), Econometrica 55(3)"
          - "Clark & McCracken (2001), 'Tests of Equal Forecast Accuracy and Encompassing for Nested Models', Journal of Econometrics 105(1)"
          - "Giacomini & White (2006), 'Tests of Conditional Predictive Ability', Econometrica 74(6)"
          - "Diebold (2015), 'Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on the Use and Abuse of Diebold–Mariano Tests', JBES 33(1)"
          - "Harvey, Leybourne & Newbold (1998), 'Tests for Forecast Encompassing', JBES 16(2)"
          - "Bates & Granger (1969), 'The Combination of Forecasts', Journal of the Operational Research Society 20(4)"
          - "Fan, Liao & Yao (2015), 'Power Enhancement in High-Dimensional Cross-Sectional Tests', Econometrica 83(4)"
          - "Donoho & Jin (2004), 'Higher Criticism for Detecting Sparse Heterogeneous Mixtures', Annals of Statistics 32(3)"
          - "Efron, Tibshirani, Storey & Tusher (2001), 'Empirical Bayes Analysis of a Microarray Experiment', JASA 96(456)"
          - "Efron (2004), 'Large-Scale Simultaneous Hypothesis Testing: The Choice of a Null Hypothesis', JASA 99(465)"
          - "Efron (2008), 'Microarrays, Empirical Bayes and the Two-Groups Model', Statistical Science 23(1)"
          - "Efron (2011), 'Tweedie's Formula and Selection Bias', JASA 106(496)"
          - "Efron & Morris (1973), 'Stein's Estimation Rule and Its Competitors—An Empirical Bayes Approach', JASA 68(341)"
          - "Efron & Morris (1975), 'Data Analysis Using Stein's Estimator and Its Generalizations', JASA 70(350)"
```

`uses` needs no change. L03 §7 links `data-snooping-bias` (L01) and `sharpe-ratio-standard-error-iid` (S1). L04
§1 links `hac-standard-errors` (S2), which is already listed.

Optional: the `core` line could name the new topics, for example "…FDR, local FDR and empirical Bayes
shrinkage, Diebold–Mariano, the factor-zoo t-stat hurdle…". That would change `CURRICULUM.md`, so the branch
leaves it alone.

Afterwards, regenerate: `python3 tools/render_curriculum.py` and `python3 tools/build_site.py`.

## 3. Hours

**No hours change is applied.** L03 and L04 still declare 7 study hours. The hub split is still 56 lesson
hours and 24 project hours, because changing it means editing `project.html`, which this work must not touch.

**Estimate:** each lesson grows by about 1.5 study hours.

- **L03:** a new section with
  - 2 definitions and 4 propositions with proofs;
  - a lab;
  - problems M4 and P4, one misconception and three quiz items.
- **L04:**
  - 1 definition and 1 proposition with proofs, and 5 remarks;
  - problems M4, P4, P5 and E4 (P4 alone has a four-part proof);
  - one misconception and four quiz items.

**Proposed split:** L03 8 h, L04 8 h, project 22 h. Lessons would total 58 h and the module would stay at
80 h. The project would take 22/80 = 27.5% of the module, inside BUILDER_RULES §4.3's 10–40%.

**Edits this needs:**

- L03 and L04: `data-hours="8"` and the eyebrows.
- `index.html`: `data-hours-lessons="58"` and `data-hours-project="22"`, the hours-split label, the L03 and L04
  card kickers, and the sentence "Eight lessons of seven study hours each".
- `project.html`: `data-hours-project="22"`, and its per-deliverable time estimates rescaled to 22 h.

The alternative is to keep the split and treat the material as part of each lesson's 7 h. This is the
parent's decision.

## 4. Cards (`course/modules/S/S7/cards.json`)

Seventeen new cards: ten for L03 and seven for L04. Each back can be checked against the lesson text. When
applied, the ids become the next free numbers, S7-c109 to S7-c125 at the current head. For the gate run, the
cards were appended in this order.

```json
[
 {
  "id": "S7-cNEW-1",
  "lesson": "L03",
  "front": "In the two-group model, define the local and the tail-area false discovery rates.",
  "back": "\\(\\mathrm{lfdr}(z) = \\pi_0 f_0(z)/f(z) = \\Prob(H = 0 \\mid Z = z)\\) and \\(\\mathrm{Fdr}(z) = \\pi_0 S_0(z)/S(z) = \\Prob(H = 0 \\mid Z \\ge z)\\), where \\(f = \\pi_0 f_0 + \\pi_1 f_1\\) is the mixture density and \\(S_0\\), \\(S\\) are upper-tail probabilities (Definition 7.2).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-2",
  "lesson": "L03",
  "front": "How are the tail-area and local false discovery rates related, and which is larger at the edge of a tail region?",
  "back": "\\(\\mathrm{Fdr}(z) = \\E[\\mathrm{lfdr}(Z) \\mid Z \\ge z]\\): the tail rate averages the local rate over the region. When the likelihood ratio \\(f_1/f_0\\) is non-decreasing, lfdr is non-increasing and \\(\\mathrm{lfdr}(z) \\ge \\mathrm{Fdr}(z)\\), so the edge of a rejection list is more likely null than its average (Proposition 7.3).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-3",
  "lesson": "L03",
  "front": "In what sense is the Benjamini–Hochberg procedure a tail-area rule?",
  "back": "Estimating \\(S(z)\\) by the empirical share \\(R(z)/N\\) and \\(\\pi_0\\) by 1 gives \\(\\widehat{\\mathrm{Fdr}}(Z_{(k)}) = N p_{(k)}/k\\), which is at most \\(q\\) exactly when \\(p_{(k)} \\le kq/N\\): BH rejects the largest tail region whose estimated Fdr is at most \\(q\\). In the two-group model the positive FDR of a tail rule is exactly \\(\\mathrm{Fdr}(z)\\) (Proposition 7.4).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-4",
  "lesson": "L03",
  "front": "State the posterior of a true Sharpe ratio \\(\\theta \\sim \\Normal(\\mu, \\tau^2)\\) given an estimate \\(X \\mid \\theta \\sim \\Normal(\\theta, \\sigma^2)\\), and how empirical Bayes shrinkage fits it.",
  "back": "\\(\\theta \\mid X \\sim \\Normal(\\mu + B(X - \\mu), B\\sigma^2)\\) with \\(B = \\tau^2/(\\tau^2 + \\sigma^2)\\), and marginally \\(X \\sim \\Normal(\\mu, \\tau^2 + \\sigma^2)\\) (Proposition 7.6). Empirical Bayes shrinkage fits \\(\\hat\\mu = \\bar X\\) and \\(\\hat\\tau^2 = \\max\\{0, s_X^2 - \\sigma^2\\}\\) by moments (Definition 7.7).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-5",
  "lesson": "L03",
  "front": "Why does choosing the best of many strategies not bias its posterior mean?",
  "back": "For independent pairs and the true prior, \\(\\E[\\theta_{n^\\ast} \\mid X] = \\sum_n \\indic\\{n^\\ast = n\\}\\,\\E[\\theta_n \\mid X_n] = \\tilde\\theta_{n^\\ast}\\) for any selection rule \\(n^\\ast\\) that depends on the data, so \\(\\E[\\tilde\\theta_{n^\\ast}] = \\E[\\theta_{n^\\ast}]\\). The raw estimate keeps the data-snooping bias (Proposition 7.8).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-6",
  "lesson": "L03",
  "front": "State Tweedie's formula.",
  "back": "If \\(X \\mid \\theta \\sim \\Normal(\\theta, \\sigma^2)\\) and \\(\\theta\\) has any distribution, \\(\\E[\\theta \\mid X = x] = x + \\sigma^2 f'(x)/f(x)\\), where \\(f\\) is the marginal density of \\(X\\). A normal prior gives the linear rule \\(\\mu + B(x - \\mu)\\) (Proposition 7.9).",
  "grade": "T",
  "cite": [
   "efron2011tweedies"
  ]
 },
 {
  "id": "S7-cNEW-7",
  "lesson": "L03",
  "front": "In Lab 4, how well do normal-prior shrinkage and Tweedie's formula correct the top-ranked of 500 simulated strategies?",
  "back": "With normally distributed true Sharpe ratios, shrinkage cuts the winner's annualized bias from 0.939 to 0.023 (standard error 0.026). When 90% of the strategies are null, it over-corrects to \\(-0.535\\), and Tweedie's formula with a kernel density estimate leaves 0.215 of the raw 0.850.",
  "grade": "C",
  "basis": "Lab 4 (simulation)"
 },
 {
  "id": "S7-cNEW-8",
  "lesson": "L03",
  "front": "What does Efron argue about the null distribution in large-scale testing, and why does it matter for a backtest universe?",
  "back": "Many simultaneous tests allow the null itself to be estimated, and this empirical null may be considerably more dispersed than the theoretical null used for a single case (Remark 7.5). Autocorrelated or overlapping returns widen the null of Sharpe-ratio z-statistics, and a theoretical null then makes local false discovery rates too small.",
  "grade": "B",
  "cite": [
   "efron2004large"
  ]
 },
 {
  "id": "S7-cNEW-9",
  "lesson": "L03",
  "front": "Does every discovery on a BH list at \\(q = 10\\%\\) have at most a 10% chance of being a null?",
  "back": "No. \\(q\\) bounds the expected share of nulls on the list, an average over its members (Proposition 7.4). With a monotone likelihood ratio the members near the cutoff are more likely null than that average (Proposition 7.3); in Lab 4 the last of 26 BH rejections at \\(q = 0.10\\) has a true lfdr of 0.287.",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-10",
  "lesson": "L03",
  "front": "How do deflation and empirical Bayes shrinkage respond as the true dispersion of Sharpe ratios across trials grows?",
  "back": "Shrinkage moves the winner less, since \\(B \\to 1\\). The deflation benchmark \\(\\SR_0 = s_X c_N\\) grows like \\(\\sqrt{\\tau^2 + \\sigma^2}\\): deflation treats all observed dispersion as luck, while shrinkage attributes \\(\\tau^2\\) of it to real differences (Problem P4).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-11",
  "lesson": "L04",
  "front": "Define the Diebold–Mariano statistic.",
  "back": "\\(\\mathrm{DM} = \\bar d/(\\hat\\sigma_{\\mathrm{LR}}/\\sqrt{T})\\) for the loss differential \\(d_t\\), with \\(\\hat\\sigma^2_{\\mathrm{LR}} = \\hat\\gamma(0) + 2\\sum_{j=1}^{\\ell}(1 - j/(\\ell+1))\\,\\hat\\gamma(j)\\), a Bartlett-weighted long-run variance. It tests equal predictive accuracy, \\(\\mu = 0\\) (Definition 1.2).",
  "grade": "T",
  "cite": [
   "diebold1995comparing"
  ]
 },
 {
  "id": "S7-cNEW-12",
  "lesson": "L04",
  "front": "Under what conditions is the Diebold–Mariano statistic asymptotically standard normal?",
  "back": "When the loss differential is covariance stationary with absolutely summable autocovariances, \\(\\sqrt{T}(\\bar d - \\mu)\\) satisfies a central limit theorem with long-run variance \\(\\sigma^2_{\\mathrm{LR}} \\gt 0\\), and \\(\\hat\\sigma^2_{\\mathrm{LR}}\\) is consistent. Then \\(\\mathrm{DM} \\dto \\Normal(0, 1)\\) under \\(\\mu = 0\\), and \\(\\mathrm{DM} \\to \\infty\\) when \\(\\mu \\gt 0\\) (Proposition 1.3).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-13",
  "lesson": "L04",
  "front": "Why does the Diebold–Mariano normal limit fail for nested models under the null?",
  "back": "If the extra coefficients are zero, the two population forecasts coincide, so the population loss differential is zero in every period and \\(\\sigma^2_{\\mathrm{LR}} = 0\\); the sample differential is pure estimation error (Remark 1.4).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-14",
  "lesson": "L04",
  "front": "When does forecast 0 encompass forecast 1, and does equal accuracy imply it?",
  "back": "When the MSE-optimal combination weight on forecast 1, \\(\\lambda^\\ast = \\E[e_0(e_0 - e_1)]/\\E[(e_0 - e_1)^2]\\), is zero. Equal accuracy does not imply it: equal mean squared errors \\(s^2\\) and error correlation \\(\\rho \\lt 1\\) give \\(\\lambda^\\ast = 1/2\\) and a combination with mean squared error \\(s^2(1 + \\rho)/2 \\lt s^2\\) (Remark 1.6).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-15",
  "lesson": "L04",
  "front": "Why is a sign-flip (permutation) test of equal accuracy invalid for an autocorrelated loss differential?",
  "back": "Random signs keep the marginal distributions but remove the autocovariances, so the reference variance of \\(T^{-1/2}\\sum_t d_t\\) is about \\(\\gamma(0)\\), not \\(\\sigma^2_{\\mathrm{LR}}\\). At \\(\\phi = 0.5\\) a nominal two-sided 5% test rejects a true null with probability \\(2(1 - \\Phi(1.96/\\sqrt3)) = 0.258\\) (Remark 3.5).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-16",
  "lesson": "L04",
  "front": "Against which alternatives are max-type and sum-type global statistics powerful?",
  "back": "A maximum is built for sparse alternatives, a few strong effects; a sum for dense ones, many weak effects. With \\(K = 100\\) independent statistics at level 0.05, one standardized mean of 4 gives power 0.775 for the maximum and 0.107 for the sum, while a hundred means of 0.3 give 0.133 and 0.912 (Problem P4).",
  "grade": "T"
 },
 {
  "id": "S7-cNEW-17",
  "lesson": "L04",
  "front": "Why does the long-run variance estimate use Bartlett weights?",
  "back": "With them it equals \\((T(\\ell + 1))^{-1}\\sum_s S_s^2\\), a scaled sum of squared moving sums of the demeaned series, so it is non-negative in every sample; flat weights can give a negative value (Problem P5).",
  "grade": "T"
 }
]
```

## 5. Other central files

- **Notation:** no request. The pages use `\mathrm{lfdr}`, `\mathrm{Fdr}`, `\mathrm{DM}` and `\mathrm{LR}`,
  which are KaTeX built-ins, plus the registered macros `\E`, `\Prob`, `\Var`, `\Cov`, `\Normal`, `\indic`,
  `\dto`, `\pto`, `\argmax`, `\SR`, `\hSR`, `\DSR` and `\emgamma`.
- **No other central file is needed:** no new data, figures or vendor files.

## 6. What changed on the branch

**L03 (`course/modules/S/S7/L03.html`).** A new §7, "Local false discovery rates and empirical Bayes", sits
between §6 (Storey) and the finance section. The old §7–§13 renumber to §8–§14; nothing outside L03 links
those anchors.

- **Definition 7.1:** the two-group model.
- **Definition 7.2:** the local and tail-area false discovery rates.
- **Proposition 7.3:** Fdr(z) = E[lfdr(Z) | Z ≥ z], and lfdr ≥ Fdr at the edge of the tail under a monotone
  likelihood ratio. With proof.
- **Proposition 7.4:** the pFDR of a tail rule is exactly Fdr; BH is the tail-area rule with π0 = 1; the
  q-value is inf Fdr, consistent with §6's description of Storey's q-value. With proof.
- **Remark 7.5:** Efron's empirical Bayes estimate, and the empirical null.
- **Proposition 7.6:** the normal posterior. With proof.
- **Definition 7.7:** empirical Bayes shrinkage, with the shrinkage factor fitted by moments, and the (N − 3)
  Stein constant derived through E[1/χ²_ν].
- **Proposition 7.8:** selection does not bias a posterior mean, which corrects L01's data-snooping bias.
- **Proposition 7.9:** Tweedie's formula.
- **Lab 4** (`tests/labs/S7/lab-S7-L03-4.py`, seed 306, SIMULATED, 500 strategies, about 1.5 s of CPU
  locally):
  - pooled checks of Proposition 7.3;
  - the lfdr of the last BH rejection (true 0.287 at q = 0.10);
  - the top-ranked strategy's raw, shrunk and Tweedie Sharpe ratios.
  - Across 200 universes, normal-prior shrinkage removes the winner's bias in the normal design: 0.939 →
    0.023, with standard error 0.026.
  - In the two-group design, shrinkage over-corrects to −0.535 and Tweedie leaves 0.215 of 0.850. The lab
    reports this honestly instead of claiming that shrinkage always works.
- **Problems:**
  - M4: lfdr, Fdr and BH's estimate, by hand.
  - P4: shrinkage against L07's deflated Sharpe ratio. The deflation benchmark treats real dispersion as
    luck: on Lab 4's universe DSR = 0.903 for a winner with true lfdr 0.001.
  - R2: now points to the two-group model.
- **Also:** misconception 5 (BH's q is not a per-discovery bound), a canon-break bullet on the empirical null,
  three key results and quiz items L03q11–q13.

**L04 (`course/modules/S/S7/L04.html`).** No sections renumber; L07 links `L04.html#s3`.

- **§1:**
  - Definition 1.2: the DM statistic with a Bartlett/Newey–West long-run variance.
  - Proposition 1.3: the DM limit under covariance stationarity of the loss differential, a CLT and a
    consistent long-run variance, with proof.
  - Remark 1.4: nested models, where σ²_LR = 0 under the null (Clark–McCracken, Giacomini–White, Diebold
    2015).
  - Remark 1.5: the Reality Check as the multi-model generalization and the SPA as the maximum of DM-type
    statistics, linked to Definition 1.1.
  - Remark 1.6: encompassing and combination, with the λ* derivation and the result that equal accuracy does
    not imply encompassing (Harvey–Leybourne–Newbold, Bates–Granger).
- **Remark 3.5 (G12):** sign-flip and permutation tests use the iid variance γ(0), with size 0.258 at φ = 0.5
  and 0.150 at φ = 0.3. What the stationary bootstrap keeps.
- **Remark 4.3 (G9):** maxima are built for sparse alternatives and sums for dense ones (Fan–Liao–Yao,
  Donoho–Jin).
- **Problems:**
  - M4: DM by hand.
  - P4: max against sum, with closed forms, a checked snippet `sol-S7-L04-P4`, and a complete proof of the
    √K against √(ln K) scaling.
  - P5: Bartlett weights give a non-negative estimate in every sample.
  - E4: the size of the naive t, sign-flip, DM–NW and stationary-bootstrap tests, with checked snippet
    `sol-S7-L04-E4`.
- **Also:** misconception 5 (permutation tests are not safe for autocorrelated differentials), four key
  results and quiz items L04q11–q14.

**Hub (`course/modules/S/S7/index.html`):** the L03 and L04 card bodies name the new topics. The hours are
unchanged.

## 7. Gate results

The gates ran in the worktree after merging `claude/phase0-foundations-s7-pilot` at 727ed58, which brings in
the data-area chart.js and the stricter sweep. Sections 1, 2 and 4 were applied temporarily and then reverted.
The binaries came from `/home/user/quant-phd/.venv`.

| Gate | Result |
|---|---|
| `ruff check .` / `ruff format --check .` | All checks passed / 69 files already formatted |
| `mypy` (strict) | Success: no issues found in 65 source files |
| `pytest` | 164 tests, all passed (exit 0) |
| `render_curriculum.py` | valid: 25 parts, 134 modules, 157 projects, 13,695 h. With section 2 applied, `CURRICULUM.md` and `curriculum/curriculum.json` change as the YAML does; commit them together. |
| `build_site.py`, then `build_site.py --check` | site data current: 6 outputs |
| `verify_refs.py --offline` | 529 entries, 0 problems |
| `verify_refs.py` (live) | 529 entries, 3 problems. All 3 are network resets from openlibrary.org for unrelated book ISBNs (`damodaran2012investment`, `ramalho2021fluent`, `spivak2008calculus`). The 15 entries above re-verified against Crossref. |
| `check_pages.py --all` / `check_dag.py --all` / `check_projects.py --all` | PASS / PASS / PASS |
| `run_labs.py --unit S7` | PASS (34/34): Lab 4 and the snippets `sol-S7-L04-E4` and `sol-S7-L04-P4` are included |
| `page_smoke.py --unit S7 --pages L03 L04` (labs and the figure sweep) | PASS. In Pyodide, L03 Lab 4 runs in 3.0 s against a 10 s limit. |
| `page_smoke.py --unit S7 --pages index --skip-labs` | PASS |

Not run: `run_graders.py` and `mutate_graders.py`, because the grader, the project and the A8 contract are
untouched.

On the branch alone, without sections 1, 2 and 4, two checks fail: `check_pages` reports the unknown
registry keys and `check_dag` reports the undeclared concepts. Both are expected.
