# X4 Build Plan: Digital Assets as a Macro Asset

Unit: **X4 · Digital Assets as a Macro Asset** · tier M · 40 h · prerequisites X1, F2 · no Atlas milestone · grading `both` (autograder for reserve stress test engine, rubric for stress test memo) · output directory `course/modules/X/X4/` · lab twins `tests/labs/X4/` · grader `course/modules/X/X4/grader/` · mutants `ledgers/X4/mutants/` · ledger `ledgers/X4/X4-a.json`.

---

## 0. Curriculum Facts & Metadata

| Fact | Locator |
|---|---|
| Part X, code `X`, title "Macro, Currencies & Commodity Dynamics" | `curriculum/curriculum.json` |
| Module ID | `X4` |
| Title | Digital Assets as a Macro Asset |
| Tier | `M` (Mastery) |
| Hours | 40 h total: 24 h lessons (4 lessons × 6 h) + 16 h project (40%) |
| Prerequisites | `[X1, F2]` (both verified) |
| Core | Crypto risk and return factors, stablecoin mechanics and reserve assets, correlation regimes with risk assets. Evidence graded strictly. |
| Concepts introduced (3) | `crypto-risk-factors`, `crypto-correlation-regimes`, `stablecoin-reserve-run` |
| Primary sources | `liu2020risks`, `liu2022common` |
| Additional verified sources | `diamond1983bank`, `gorton2012securitized`, `jiang2024monetary`, `brunnermeier2008market`, `carhart1997persistence`, `fama1993common`, `jegadeesh1993returns` |
| Project title | Stablecoin reserve stress test |
| Project brief | Model a fiat-backed stablecoin's reserve portfolio under redemption runs and rate shocks, and find the run size that breaks the peg. |
| Project grading | `both` (autograder and rubric) |

---

## 1. Lesson Map & Architecture

### L01: Cryptocurrency Statistical Properties & Time-Series Return Predictability (6 h)
- **Scope:** First and higher moments of crypto-asset returns (Bitcoin, Ethereum, major tokens). Extreme volatility, skewness, kurtosis, and fat-tailed distributions compared to equities, currencies, and gold.
- **Predictability factors:** Time-series return momentum (1 to 6 weeks) and investor attention proxies (Google Trends, active addresses, transaction counts, hash rate costs) as documented by Liu & Tsyvinski (2021, RFS). Evidence showing traditional macro factors (exchange rates, commodity prices, inflation shocks, equity market factors) did not predict crypto returns in early samples.
- **Twin Lab:** `tests/labs/X4/lab-X4-L01-1.py` - Evaluates time-series momentum vs. network user growth predictive regression and calculates higher moments.

### L02: Cross-Sectional Crypto Risk Factors (6 h)
- **Concept definition:** `<dfn id="def-crypto-risk-factors" data-concept="crypto-risk-factors">`
- **Scope:** The cross-section of cryptocurrency returns. Construction of cryptocurrency factor portfolios following Liu, Tsyvinski & Wu (2022, JF):
  1. Cryptocurrency Market (CMKT): Value-weighted crypto market excess return.
  2. Cryptocurrency Size (CSMB - Small Minus Big): Long small market-cap coins, short large-cap coins.
  3. Cryptocurrency Momentum (CMOM - High Minus Low return momentum): Long past winners (past 3-week return), short past losers.
  4. Network Value factors: Price-to-User ratio and Network Value to Transactions (NVT) ratio.
- **Econometrics:** Cross-sectional Fama-MacBeth two-pass regressions, factor spanning regressions (showing that CMKT, CSMB, CMOM span candidate alternative crypto anomalies), and Sharpe ratio comparisons.
- **Twin Lab:** `tests/labs/X4/lab-X4-L02-1.py` - Constructs CMKT, CSMB, CMOM factor returns, estimates Fama-MacBeth risk premia, and tests factor spanning.

### L03: Macro Liquidity Regimes & Bitcoin Beta (6 h)
- **Concept definition:** `<dfn id="def-crypto-correlation-regimes" data-concept="crypto-correlation-regimes">`
- **Scope:** The structural transition of digital assets from idiosyncratic fringe assets (2010–2019) to macro-sensitive high-beta risk assets (2020–present).
- **Mechanisms:** Central bank balance sheet expansions (QE vs. QT), global M2 liquidity shocks, and real interest rate sensitivity. Rolling correlation with the Nasdaq 100, S&P 500, US Dollar Index (DXY), and 10Y real Treasury yields.
- **Regime Modeling:** Two-state Markov regime-switching model and threshold regressions identifying the high-volatility/risk-on regime (high positive beta to tech equities) vs. low-correlation idiosyncratic regime.
- **Twin Lab:** `tests/labs/X4/lab-X4-L03-1.py` - Implements a 2-state regime-switching model and rolling beta analysis of Bitcoin returns against equity market and interest rate shocks.

### L04: Stablecoin Mechanics, Reserve Backing & Peg Run Dynamics (6 h)
- **Concept definition:** `<dfn id="def-stablecoin-reserve-run" data-concept="stablecoin-reserve-run">`
- **Scope:** Taxonomy of stablecoins: fiat-backed (USDC, USDT), over-collateralized crypto (DAI), and algorithmic unbacked (Terra/UST).
- **Run Mechanics:** Applying the Diamond–Dybvig (1983) and Gorton–Metrick (2012) framework to stablecoin balance sheets. Maturity mismatch (liquid redemption rights on demand vs. term reserve assets) and liquidity mismatch. Mark-to-market losses under monetary tightening (citing Jiang et al., 2024).
- **Liquidation Waterfall & De-Peg:** Tiered reserve asset liquidation (cash buffer -> reverse repo / overnight -> short-dated T-bills with mark-to-market duration discounts -> uninsured bank deposits subject to counterparty haircuts). Finding the critical redemption fraction \(R^*\) that triggers a NAV break below $1.00 (e.g. $0.995). Secondary market discount arbitrage and fire-sale spirals (Brunnermeier & Pedersen 2009).
- **Twin Lab:** `tests/labs/X4/lab-X4-L04-1.py` - Simulates a multi-tier reserve liquidation waterfall under cumulative redemptions and interest rate shocks to determine the exact peg-break threshold.

---

## 2. Project Architecture: Stablecoin Reserve Stress Test (16 h)

### 2.1 Project Ladder
- **Rung 1 (Worked Example):** Traces a 5-tier reserve liquidation waterfall for a $10B fiat-backed stablecoin subjected to a 35% redemption shock and 200 bps interest rate spike.
- **Rung 2 (Completion Problem):** Implements the haircut loss and liquidation waterfall functions with `___` blanks for mark-to-market duration losses and remaining reserve NAV calculation.
- **Rung 3 (Independent Project):** Full Python engine `stablecoin_stress.py` implementing:
  1. `ReservePortfolio`: Structured reserve assets (cash, overnight reverse repo, 3-month T-bills, 12-month Treasuries, bank deposits).
  2. `apply_rate_shock`: Modified duration mark-to-market loss computation across term assets.
  3. `simulate_redemption_run`: Sequential daily redemption execution across asset tiers with liquidation haircuts and cash replenishment.
  4. `find_peg_break_threshold`: Binary search identifying the exact cumulative redemption dollar amount / percentage \(R^*\) where secondary NAV falls below $0.995.
  5. `stress_test_report`: Comprehensive stress matrix across rate shocks (0 to 400 bps) and redemption velocity scenarios.
  6. Accompanied by a 1,500-word executive risk memo `memo.md` addressing balance sheet composition, bank run dynamics, and regulatory compliance (e.g., GENA / MiCA reserve requirements).
- **Rung 4 (Stretch):** Endogenous redemption velocity linked to secondary market DEX discount and dynamic liquidity feedback loops.

---

## 3. Autograder & Mutants Specification

### 3.1 Autograder Suite (`course/modules/X/X4/grader/`)
- `instance.py`: Generates randomized yet realistic stablecoin balance sheet sizes ($5B to $50B), asset allocations, asset durations, liquidation haircuts, and rate shocks across seeds.
- `reference.py`: Reference implementation of reserve portfolio stress test engine.
- `starter.py`: Scaffold with type signatures and docstrings, raising `NotImplementedError`.
- `test_project.py`: Pytest suite testing:
  - Input validation and conservation of asset value
  - Modified duration pricing accuracy
  - Liquidation priority adherence (cash -> repo -> short bills -> long notes -> deposits)
  - Monotonicity of NAV with respect to cumulative redemptions and rate shocks
  - Accuracy of peg-break threshold \(R^*\) within tolerance
  - Terminal recovery values when insolvent
- `integrity.py`: Schema validation, matrix and balance sheet invariant checks.

### 3.2 Verification Mutants (`ledgers/X4/mutants/`)
- `m01_no_duration_loss.py`: Ignores interest rate shocks on Treasury securities (zero mark-to-market loss).
- `m02_reverse_liquidation_order.py`: Liquidates illiquid / high-haircut assets before cash buffers.
- `m03_linear_threshold_guess.py`: Uses a constant approximation instead of binary search for peg break.
- `m04_omits_deposit_haircut.py`: Assumes bank deposits have 100% recovery during bank failure shocks.
- `m05_nav_uses_par_value.py`: Calculates NAV using nominal par value instead of market value post-liquidation.

---

## 4. Spaced-Retrieval Cards (`cards.json`)
20 atomic retrieval cards covering:
- Crypto return statistical moments (fat tails, skewness)
- Momentum in cryptocurrency returns (`liu2020risks`)
- Investor attention and network metrics (`liu2020risks`)
- Liu-Tsyvinski-Wu 3-factor model (`liu2022common`): CMKT, CSMB, CMOM
- Fama-MacBeth risk premia in crypto cross-section
- Network value to transactions (NVT) ratio
- Factor spanning methodology (`liu2022common`)
- Macro correlation regime shifts (2020 structural break)
- Central bank balance sheet expansions and crypto beta
- Real yield sensitivity of digital assets
- Regimes of Bitcoin correlation with equities
- Stablecoin classification and backing models
- Diamond-Dybvig bank run dynamics in stablecoins (`diamond1983bank`)
- Maturity and liquidity mismatch in reserve assets
- Mark-to-market losses on reserves from monetary tightening (`jiang2024monetary`)
- Liquidation waterfalls and fire-sale discounts (`brunnermeier2008market`)
- Break-the-buck peg trigger definition
- Secondary market discount arbitrage mechanics
- Strategic complementarity in stablecoin redemptions
- Regulatory reserve composition requirements
