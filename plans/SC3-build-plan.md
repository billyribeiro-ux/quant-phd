# SC3 build plan: Change of Measure (planner output)

Unit: **SC3 · Change of Measure** · tier M · 80 h · prerequisite SC2 (closure M1, M2, M4, M5, M6, P0.1, SC1, SC2) · no Atlas
milestone · no debate key · grading `both` (autograder for the numerical engine, rubric for the derivations workbook) · output directory
`course/modules/SC/SC3/` (part code `SC`) · lab twins `tests/labs/SC3/` · grader `course/modules/SC/SC3/grader/`.

---

## 0. Curriculum facts and structure

### 0.1 Curriculum facts (read, with locators)

| Fact | Locator |
|---|---|
| Part SC, code `SC`, title "Stochastic Calculus & Continuous Time" | `curriculum/03-markets.yaml:489-491` |
| SC3 id `SC3`, title "Change of Measure" | `curriculum/03-markets.yaml:562-563` |
| Tier `M`, hours `80` | `curriculum/03-markets.yaml:564-565` |
| Prereqs `[SC2]` (only) | `curriculum/03-markets.yaml:566` |
| Core: "Girsanov's theorem, martingale representation, the risk-neutral measure, change of numeraire, the forward measure." | `curriculum/03-markets.yaml:567-569` |
| `introduces` has 7 concepts: `girsanov-theorem`, `market-price-of-risk`, `martingale-representation-theorem`, `change-of-numeraire`, `forward-measure`, `exchange-option`, `quanto-adjustment` | `curriculum/03-markets.yaml:570-577` |
| Sources (free text, not keys): "Geman, El Karoui & Rochet (1995), Journal of Applied Probability 32(2)" | `curriculum/03-markets.yaml:578-579` |
| Verified registry key for source: `geman1995changes` | `references/references.json` |
| Lab: "Importance sampling via Girsanov for deep-OTM options." | `curriculum/03-markets.yaml:580` |
| Project "Numeraire toolkit"; brief: "Price an exchange option and a quanto under appropriate numeraires, and verify against Monte Carlo under the original measure."; deliverable "Code plus derivations."; grading `both` | `curriculum/03-markets.yaml:581-587` |
| No `debate:` key and no `atlas:` key on SC3 or its project | `curriculum/03-markets.yaml:562-588` (absent) |
| Prerequisite closure of SC3 (computed): **{SC2, SC1, M6, M5, M4, M2, M1, P0.1}** | `tools/coursekit.py` `prerequisite_closure("SC3")` |
| Owners of the 7 SC3 concepts: all SC3 | `tools/coursekit.py` `concept_owner()` |

### 0.2 Hours breakdown

Curriculum total: **80 h**.
- Lessons: **7 lessons × 8 h = 56 h** (70%)
- Project: **24 h** (30%, within 10–40% bound)
Total: **56 + 24 = 80 h**.

### 0.3 Lessons outline

1. **L01: Girsanov's Theorem**
   - Concept defined: `<dfn id="def-girsanov-theorem" data-concept="girsanov-theorem">Girsanov's theorem</dfn>`
   - Core topics: Radon–Nikodym derivative process in continuous time, Doléans-Dade exponential martingales, Novikov's condition, Cameron–Martin–Girsanov drift transformation, abstract Bayes formula.
   - Lab `lab-SC3-L01-1.py`: Numerical verification of Girsanov drift shifting and density process martingale property.

2. **L02: Market Price of Risk and the Risk-Neutral Measure**
   - Concept defined: `<dfn id="def-market-price-of-risk" data-concept="market-price-of-risk">market price of risk</dfn>`
   - Core topics: Discounted asset dynamics under the physical measure \(\Prob\), drift elimination, Sharpe ratio of diffusion noise, equivalent martingale measure \(\mathbb{Q}\), multi-asset no-arbitrage condition.
   - Lab `lab-SC3-L02-1.py`: Verification of discounted asset price martingality under \(\mathbb{Q}\) vs drift under \(\Prob\).

3. **L03: The Martingale Representation Theorem and Replicating Portfolios**
   - Concept defined: `<dfn id="def-martingale-representation-theorem" data-concept="martingale-representation-theorem">martingale representation theorem</dfn>`
   - Core topics: Representation of Brownian martingales as Itô stochastic integrals, market completeness, replication of European claims, delta hedging representation \(\Delta_t = \psi_t / (\sigma S_t)\).
   - Lab `lab-SC3-L03-1.py`: Discrete delta hedging convergence and empirical replication error variance scaling as \(O(1/N)\).

4. **L04: Change of Numeraire and the Generalized Valuation Equation**
   - Concept defined: `<dfn id="def-change-of-numeraire" data-concept="change-of-numeraire">change of numeraire</dfn>`
   - Core topics: Geman, El Karoui & Rochet (1995) numeraire framework, Radon–Nikodym derivative between arbitrary numeraires, generalized pricing equation \(V_0 = N_0 \E^{\mathbb{Q}^N}[V_T / N_T]\), stock numeraire and probabilistic decomposition of Black–Scholes \(d_1\) and \(d_2\).
   - Lab `lab-SC3-L04-1.py`: Numerical check of numeraire invariance comparing money-market numeraire vs stock numeraire.

5. **L05: The Forward Measure and Stochastic Interest Rates**
   - Concept defined: `<dfn id="def-forward-measure" data-concept="forward-measure">forward measure</dfn>`
   - Core topics: \(T\)-forward measure \(\mathbb{Q}^T\) with zero-coupon bond numeraire \(P(t, T)\), decoupling stochastic discounting from terminal payoffs, forward price martingality, Black's (1976) formula under the forward measure.
   - Lab `lab-SC3-L05-1.py`: Option pricing under stochastic Vasicek short rates comparing risk-neutral simulation with the \(T\)-forward measure.

6. **L06: Exchange Options and the Margrabe Formula**
   - Concept defined: `<dfn id="def-exchange-option" data-concept="exchange-option">exchange option</dfn>`
   - Core topics: Margrabe (1978) option to exchange asset 2 for asset 1, pricing via asset 2 as numeraire, effective volatility \(\sigma_M = \sqrt{\sigma_1^2 - 2\rho\sigma_1\sigma_2 + \sigma_2^2}\), homogeneity of degree 1, put-call exchange parity.
   - Lab `lab-SC3-L06-1.py`: Closed-form Margrabe verification against 2D Monte Carlo, homogeneity of degree 1, and exchange parity.

7. **L07: Quanto Adjustments and Cross-Currency Derivatives**
   - Concept defined: `<dfn id="def-quanto-adjustment" data-concept="quanto-adjustment">quanto adjustment</dfn>`
   - Core topics: Cross-currency derivatives, foreign asset with domestic payment, domestic vs foreign risk-neutral measures, quanto drift adjustment \(r_f - \rho \sigma_S \sigma_X\), curriculum lab.
   - Lab `lab-SC3-L07-1.py`: Curriculum lab: "Importance sampling via Girsanov for deep-OTM options." (comparing standard Monte Carlo variance against Girsanov change-of-drift importance sampling for rare-event deep out-of-the-money options).

---

## 1. Project and Grader

### 1.1 Project Structure (`project.html`)
- Title: "Numeraire Toolkit"
- Rung 1: Worked example solving Margrabe exchange option on seed 0 (SIMULATED) under asset 2 numeraire vs 2D Monte Carlo.
- Rung 2: Completion problem completing the missing quanto drift adjustment \(-\rho \sigma_S \sigma_X\) and Margrabe volatility \(\sigma_M\).
- Rung 3: Independent project: `numeraire_toolkit.py` implementing Margrabe and quanto pricing, Monte Carlo validation, and invariance verification across arbitrary parameter instances.
- Rung 4: Stretch extension to multi-asset spread options and cross-currency quanto exchange contracts.
- Time budget: 24 h total (components sum to 24 with rationale).
- Rubric: 5 criteria, 4 performance levels, exemplars at level 4 and level 2.

### 1.2 Grader Suite (`grader/`)
- `instance.py`: deterministic, parameterized `make_instance(seed: int) -> dict[str, Any]`.
- `reference.py`: fully verified solution passing all tests across 50 seeds (0–49).
- `starter.py`: stubbed template raising `NotImplementedError`.
- `test_project.py`: acceptance suite testing:
  - Margrabe homogeneity of degree 1.
  - Put-call exchange parity.
  - Correlation monotonicity.
  - Agreement with Monte Carlo within statistical bands.
  - Quanto drift adjustment correctness.
  - Zero-correlation limit.
  - Input validation (ValueError on invalid parameters).
