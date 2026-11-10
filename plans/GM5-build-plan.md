# GM5 Build Plan: Crises as Mechanisms

Unit: **GM5 · Crises as Mechanisms** · tier M · 80 h · prerequisites GM4, SR1 · grading `both` · output directory `course/modules/GM/GM5/` · lab twins `tests/labs/GM5/` · grader `course/modules/GM/GM5/grader/`.

---

## 0. Curriculum Facts & Requirements

### 0.1 Curriculum Facts (`curriculum/curriculum.json`)

| Field | Value |
|---|---|
| id | `GM5` |
| title | `Crises as Mechanisms` |
| part | `GM` (`Global Macro Trading`) |
| tier | `M` |
| hours | `80` |
| prereqs | `["GM4", "SR1"]` |
| core | 1992 ERM, 1997 Asia, 1998 LTCM/Russia, 2008, the 2010–12 euro crisis, the 2013 taper tantrum, the 2015 CHF de-peg, March 2020, 2022 gilts/LDI, 2023 SVB, the 2024 yen-carry unwind. Each is taught as a causal mechanism from primary sources. |
| introduces | `crisis-mechanism-map`, `forced-seller-dynamics`, `peg-abandonment`, `carry-unwind`, `policy-backstop` |
| sources | Primary reports & verified literature: `cftc1999hedge` (PWG LTCM 1999), `snb2015swiss` (SNB 2015 CHF de-peg), `frb2023fed` (Federal Reserve SVB Review 2023), `bis2024market` (BIS Bulletin 90 2024 carry unwind), `edwards1999hedge` (Edwards 1999 JEP) |
| lab | Mechanism simulators per episode. |
| project | Title: "Crisis mechanism dossier"; brief: "For two episodes, build a mechanism map (leverage, funding, forced sellers, policy response) from primary documents, plus a simulator reproducing the core dynamic."; deliverable: "Dossier plus simulators."; grading: `both` |

### 0.2 Hours Breakdown

- Lessons: **56 h** across 5 lessons:
  - L01: The Anatomy of Financial Crises & Mechanism Mapping (11 h)
  - L02: Leverage, Margin Cascades & Forced Sellers (11 h)
  - L03: Currency Pegs, Speculative Attacks & Asymmetric Defenses (11 h)
  - L04: Carry Trades, Crowding & Endogenous Unwinds (11 h)
  - L05: Funding Shocks, Fire Sales & Policy Backstops (12 h)
- Project: **24 h** (30.0% of module hours, within the 10–40% curriculum requirement)
- Total: **56 + 24 = 80 h**

### 0.3 Introduced Concepts Mapping

| Concept ID | Name | Assigned Lesson |
|---|---|---|
| `crisis-mechanism-map` | Crisis mechanism map | L01 |
| `forced-seller-dynamics` | Forced-seller dynamics | L02 |
| `peg-abandonment` | Currency-peg abandonment | L03 |
| `carry-unwind` | Carry-trade unwind | L04 |
| `policy-backstop` | Policy backstop in a crisis | L05 |

### 0.4 Core Historical Episodes Mapping

| Episode | Primary / Verified Sources | Primary Lesson | Core Dynamics Taught |
|---|---|---|---|
| 1992 ERM | `obstfeld1996models`, `krugman1979model` | L03 | Shadow exchange rate, interest rate defence costs, self-fulfilling speculative attack |
| 1997 Asia | `calvo1998capital`, `krugman1979model` | L03 | Sudden stops, foreign-currency debt mismatch, double drain (bank run + currency run) |
| 1998 LTCM/Russia | `cftc1999hedge`, `edwards1999hedge`, `shleifer1997limits` | L02 | Relative-value convergence trades, extreme leverage, margin calls, repo liquidity freeze |
| 2008 GFC | `brunnermeier2008market`, `adrian2010liquidity`, `shleifer2011fire` | L02, L05 | Subprime shock, shadow banking repo runs, loss and margin spirals, systemic fire sales |
| 2010–12 Euro Crisis | `shleifer2011fire`, `acharya2016measuring` | L05 | Sovereign-bank doom loop, redenomination risk, Draghi "whatever it takes" / OMT backstop |
| 2015 CHF De-peg | `snb2015swiss` | L03 | Asymmetric peg defense, reserve balance-sheet ballooning, instant 20%+ FX gap, dealer ruin |
| March 2020 Dash for Cash | `he2022treasury` | L05 | Treasury illiquidity, basis trade liquidations, mutual fund outflows, Fed secondary purchases |
| 2022 UK Gilts LDI | `brunnermeier2008market`, `shleifer2011fire` | L02 | Liability-driven investment leverage, interest rate swap margin calls, emergency BoE QE |
| 2023 SVB Run | `frb2023fed`, `diamond1983bank` | L05 | Uninsured depositor run, HTM duration losses, social-media velocity, BTFP emergency backstop |
| August 2024 Yen Unwind | `bis2024market`, `brunnermeier2008carry` | L04 | BoJ rate hike, Nikkei -12.4% plunge, carry deleveraging, cross-market volatility spike |

### 0.5 Verified Registry Keys

- `cftc1999hedge`: President's Working Group on Financial Markets (1999), Hedge Funds, Leverage, and the Lessons of Long-Term Capital Management
- `edwards1999hedge`: Edwards (1999), Hedge Funds and the Collapse of Long-Term Capital Management, JEP 13(2)
- `snb2015swiss`: Swiss National Bank (2015), Swiss National Bank discontinues minimum exchange rate and lowers interest rate to -0.75%
- `frb2023fed`: Board of Governors of the Federal Reserve System (2023), Review of the Federal Reserve's Supervision and Regulation of Silicon Valley Bank
- `bis2024market`: Bank for International Settlements (2024), The Market Turbulence and Carry Trade Unwind of August 2024, BIS Bulletin 90
- `brunnermeier2008market`: Brunnermeier & Pedersen (2009), Market Liquidity and Funding Liquidity, RFS 22(6)
- `brunnermeier2008carry`: Brunnermeier, Nagel & Pedersen (2008), Carry Trades and Currency Crashes, NBER / Macroeconomics Annual
- `shleifer1997limits`: Shleifer & Vishny (1997), The Limits of Arbitrage, JF 52(1)
- `shleifer2011fire`: Shleifer & Vishny (2011), Fire Sales in Finance and Macroeconomics, JEP 25(1)
- `krugman1979model`: Krugman (1979), A Model of Balance-of-Payments Crises, JMCB 11(3)
- `obstfeld1996models`: Obstfeld (1996), Models of Currency Crises with Self-Fulfilling Features, EER 40(3)
- `diamond1983bank`: Diamond & Dybvig (1983), Bank Runs, Deposit Insurance, and Liquidity, JPE 91(3)
- `adrian2010liquidity`: Adrian & Shin (2010), Liquidity and Leverage, JFI 19(3)
- `he2022treasury`: He, Nagel & Song (2022), Treasury Inconvenience Yields During the COVID-19 Crisis, JFE 143(1)
- `calvo1998capital`: Calvo (1998), Capital Flows and Capital-Market Crises: The Simple Economics of Sudden Stops, JAE 1(1)
- `reinhart2009this`: Reinhart & Rogoff (2009), This Time Is Different: Eight Centuries of Financial Folly, Princeton University Press
- `koijen2018carry`: Koijen, Moskowitz, Pedersen & Vrugt (2018), Carry, JFE 127(2)
- `menkhoff2012carry`: Menkhoff, Sarno, Schmeling & Schrimpf (2012), Carry Trades and Global Foreign Exchange Volatility, JFE 104(2)
- `almgren2001optimal`: Almgren & Chriss (2001), Optimal Execution of Portfolio Transactions, J. Risk 3(2)
- `acharya2016measuring`: Acharya, Pedersen, Philippon & Richardson (2017), Measuring Systemic Risk, RFS 30(1)

---

## 1. Project Specifications (`project.html` and `grader/`)

### 1.1 Project Structure
- Dual-graded: In-browser autograder panel + 5-criteria doctoral evaluation rubric (C1-C5).
- 4-Rung Ladder:
  - Rung 1: Worked Example — complete analytical & numerical trace of a leveraged fund experiencing a margin spiral and fire sale.
  - Rung 2: Completion Problem — interactive code lab filling critical blanks in margin call calculation and spiral feedback.
  - Rung 3: Independent Project — build full mechanism maps for two historical episodes and simulate quantitative forced-selling and policy-backstop dynamics under parameter stress.
  - Rung 4: Stretch Extension — multi-sector systemic contagion simulator coupling hedge funds, pension funds (LDI), and banking balance sheets.

### 1.2 Autograder Modules
- `instance.py`: deterministic instance generator producing randomized yet bounded balance sheets, shock magnitudes, market depth, haircut volatility sensitivities, and backstop parameters.
- `reference.py`: reference solution implementing:
  - `compute_margin_call(position, price, cash, debt, haircut)`
  - `calculate_forced_sales(position, price, equity, haircut, target_leverage)`
  - `estimate_fire_sale_discount(forced_volume, market_depth, permanent_impact_coef)`
  - `simulate_liquidity_spiral(p0, q0, cash0, debt0, haircut0, exogenous_shocks, lambda_impact, target_leverage, haircut_sensitivity, policy_backstop)`
  - `evaluate_policy_intervention(baseline_run, backstopped_run)`
  - `classify_crisis_regime(leverage, haircut_jump, spiral_multiplier, defaulted)`
- `test_project.py`: comprehensive pytest suite validating invariants, monotonicity, margin compliance, conservation of assets, and numerical tolerance across seeds 0-49.
- `starter.py`: template with full type annotations and `raise NotImplementedError`.
