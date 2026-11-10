# GM3 Build Plan: Trading Monetary Policy

Unit: **GM3 · Trading Monetary Policy** · tier M · 50 h · prerequisites E7, S6 · grading `both` · output directory `course/modules/GM/GM3/` · lab twins `tests/labs/GM3/` · grader `course/modules/GM/GM3/grader/`.

---

## 0. Curriculum Facts & Requirements

### 0.1 Curriculum Facts (`curriculum/curriculum.json`)

| Field | Value |
|---|---|
| id | `GM3` |
| title | `Trading Monetary Policy` |
| part | `GM` (`Global Macro & Relative Value`) |
| tier | `M` |
| hours | `50` |
| prereqs | `["E7", "S6"]` |
| core | FOMC event studies, the pre-FOMC drift, information effects, policy divergence and FX. |
| introduces | `fomc-event-study`, `pre-fomc-drift`, `fed-information-effect`, `policy-divergence-fx` |
| sources | `lucca2015prefomc`: Lucca & Moench (2015), JF 70(1); `nakamura2018high`: Nakamura & Steinsson (2018), QJE 133(3); `kuttner2001monetary`: Kuttner (2001), JME 47(3); `bernanke2005explains`: Bernanke & Kuttner (2005), JF 60(3) |
| lab | FOMC event study. |
| project | Title: "Pre-FOMC drift: out-of-sample check"; brief: "Re-test the pre-FOMC drift on post-publication data, and report whether it survived."; deliverable: "Code plus note."; grading: `both` |

### 0.2 Hours Breakdown

- Lessons: **5 lessons × 6 h = 30 h** (60.0% of module hours)
- Project: **20 h** (40.0% of module hours, within the 10–40% curriculum requirement)
- Total: **30 + 20 = 50 h**

### 0.3 Introduced Concepts Mapping

| Concept ID | Name | Assigned Lesson |
|---|---|---|
| `fomc-event-study` | FOMC event study | L01 |
| `pre-fomc-drift` | Pre-FOMC announcement drift | L02 |
| `fed-information-effect` | Fed information effect | L03 |
| `policy-divergence-fx` | Policy divergence and exchange rates | L04 |

*(L05 covers Cross-Asset Execution, Volatility Crush, and Event Risk Management).*

### 0.4 Verified Registry Keys

| Key | Citation | Role in GM3 |
|---|---|---|
| `lucca2015prefomc` | Lucca & Moench (2015), JF 70(1) | Core source for L02 (pre-FOMC drift) and Project |
| `nakamura2018high` | Nakamura & Steinsson (2018), QJE 133(3) | Core source for L03 (Fed information effect, policy news shock) |
| `kuttner2001monetary` | Kuttner (2001), JME 47(3) | Core source for L01 (Fed funds futures scaling, surprise identification) |
| `bernanke2005explains` | Bernanke & Kuttner (2005), JF 60(3) | Core source for L01 (equity response to monetary policy surprises) |
| `gertler2015monetary` | Gertler & Karadi (2015), AEJ: Macro 7(1) | High-frequency surprise identification and external instrument SVAR |
| `brunnermeier2008carry` | Brunnermeier, Nagel & Pedersen (2008), NBER Macro Annual 23 | L04 currency crashes, carry unwinds, and liquidity spirals |
| `lustig2011common` | Lustig, Roussanov & Verdelhan (2011), RFS 24(11) | L04 currency risk premia and common risk factors in FX |
| `menkhoff2012carry` | Menkhoff, Sarno, Schmeling & Schrimpf (2012), JFE 104(1) | L04 FX volatility risk and carry trade returns |
| `du2018deviations` | Du, Tepper & Verdelhan (2018), JF 73(3) | L04 CIP deviations, cross-currency basis, balance sheet frictions |
| `fama1984forward` | Fama (1984), JME 14(3) | L04 Forward premium puzzle and UIP failure |
| `dornbusch1976expectations` | Dornbusch (1976), JPE 84(6) | L04 Overshooting exchange rate model |
| `romer2004new` | Romer & Romer (2004), AER 94(4) | L03 Narrative monetary policy identification |
| `bis2024market` | BIS (2024), BIS Bulletin 90 | L04 August 2024 JPY carry trade unwind case study |

---

## 1. Lesson Structure & Outlines

- **L01: High-Frequency Identification & FOMC Event Studies (6 h)**
  - Introduces `fomc-event-study`.
  - Fed funds futures market mechanics, monthly average settlement.
  - Kuttner scaling formula derivation, boundary condition adjustments.
  - Event window selection: intraday 30-min window vs daily window; signal-to-noise ratio.
  - Equity market response: Bernanke-Kuttner regression specification, transmission channels (cash flow vs discount rate).
  - Lab: Fed funds surprise calculation and OLS regression of equity returns.

- **L02: The Pre-FOMC Announcement Drift (6 h)**
  - Introduces `pre-fomc-drift`.
  - Lucca & Moench (2015) baseline findings: 49 bps drift in 24h prior to scheduled announcement.
  - Absence of drift in unscheduled meetings and placebo days.
  - Global equity market transmission (FTSE, DAX, Nikkei).
  - Economic theories: information leakage vs risk premium / resolution of uncertainty.
  - Post-publication degradation, regime shifts (press conferences, forward guidance).
  - Lab: Bootstrap testing of pre-FOMC cumulative returns and Sharpe ratios against placebo windows.

- **L03: The Fed Information Effect & Central Bank Communication (6 h)**
  - Introduces `fed-information-effect`.
  - The empirical puzzle: simultaneous rise in interest rates and upward revision in growth forecasts.
  - Nakamura & Steinsson (2018) policy news shock (first PC across 30-min surprises).
  - Disentangling pure policy shocks from Delphic information revelations.
  - High-frequency sign restrictions and forecast revisions (Greenbook / SPF).
  - Asset pricing implications for equities, term premia, and real rates.
  - Lab: Policy news shock construction via PCA and sign-restriction shock classification.

- **L04: Central Bank Policy Divergence & FX Carry Dynamics (6 h)**
  - Introduces `policy-divergence-fx`.
  - Asynchronous monetary cycles and the Uncovered Interest Rate Parity (UIP) puzzle (Fama 1984).
  - Carry trade mechanics: funding in low-yielding currencies (JPY, CHF) vs investing in high-yielders.
  - Carry crash risk and negative skewness (Brunnermeier et al. 2008, Menkhoff et al. 2012).
  - The anatomy of policy divergence shocks: August 2024 BOJ hike / carry unwind.
  - Covered Interest Parity (CIP) deviations and bank balance sheet constraints (Du et al. 2018).
  - Lab: Cross-currency policy divergence, UIP regressions, and carry drawdown simulation with `fx_daily.csv` and `ust_daily.csv`.

- **L05: Macro Cross-Asset Execution & Event Trading Systems (6 h)**
  - Event trading lifecycle: pre-announcement positioning, in-event execution, post-announcement drift.
  - Volatility surface dynamics: the pre-FOMC implied volatility premium and immediate volatility crush.
  - Market microstructure: bid-ask spread widening, book depth depletion, execution slippage in the 30-min window.
  - Cross-asset correlation jumps: Treasury yields, USD index, equity futures, credit spreads.
  - Quantitative execution strategies: Straddles / strangles, limit-order execution algorithms, jump-robust risk budgeting.
  - Lab: Volatility crush simulation, straddle PnL attribution, and execution slippage modeling.

---

## 2. Project Specification (`project.html` & `grader/`)

- **Project Title:** Pre-FOMC drift: out-of-sample check.
- **Brief:** Re-test the pre-FOMC drift on post-publication data, and report whether it survived.
- **Deliverable:** Code plus note.
- **Grading Mode:** `both` (Autograder + Rubric).
- **Ladder:**
  - Rung 1: Worked Example — Calculating pre-FOMC drift and placebo distribution on in-sample data.
  - Rung 2: Completion Problem — Completing the out-of-sample drift estimation, bootstrap t-stat, and decay factor.
  - Rung 3: Independent Project — Building a complete out-of-sample event study pipeline:
    1. Parse FOMC schedule and hourly / daily returns.
    2. Compute in-sample (1994-2011) vs out-of-sample (2012-2024) drift metrics (mean return, annualized Sharpe ratio, win rate).
    3. Generate 1,000 placebo pseudo-event windows to establish non-parametric null distributions.
    4. Implement decay tests and structural break detection (Chow test / Bai-Perron).
    5. Evaluate economic explanations (press conference introduction, VIX regimes, interest rate levels).
  - Rung 4: Stretch Problem — High-frequency intraday momentum and options volatility arbitrage around modern FOMC cycles.
- **Grader Architecture:**
  - `instance.py`: Generates seed-dependent synthetic multi-year event study panels with varying pre-announcement drift intensities, noise levels, and structural break points.
  - `reference.py`: Computes in-sample and out-of-sample event window returns, placebo permutation tests, t-statistics, and structural break metrics.
  - `test_project.py`: Pytest suite testing statistical invariants, sample period boundaries, non-negative variances, permutation test sizes, and numerical tolerances.
  - `starter.py`: Empty scaffolding with complete signatures and docstrings.
  - `integrity.py`: Deterministic hash and AST integrity checks.
  - Mutants: 5 distinct economic / econometric failure modes in `ledgers/GM3/mutants/` and `course/modules/GM/GM3/grader/mutants/`.
