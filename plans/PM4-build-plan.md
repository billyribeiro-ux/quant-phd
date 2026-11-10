# PM4 Build Plan: Real Estate Finance & Mortgage-Backed Securities

Unit: **PM4 · Real Estate Finance & Mortgage-Backed Securities** · tier M · 80 h · prerequisites FI1, CF4, DV1 · grading `autograder` · output directory `course/modules/PM/PM4/` · lab twins `tests/labs/PM4/` · grader `course/modules/PM/PM4/grader/`.

---

## 0. Curriculum Facts & Requirements

### 0.1 Curriculum Facts (`curriculum/curriculum.json`)

| Field | Value |
|---|---|
| id | `PM4` |
| title | `Real Estate Finance & Mortgage-Backed Securities` |
| part | `PM` (`Private Markets & Real Estate`) |
| tier | `M` |
| hours | `80` |
| prereqs | `["FI1", "CF4", "DV1"]` |
| core | Mortgage math, prepayment and negative convexity, agency MBS, REITs and cap rates, the housing boom and bust. |
| introduces | `prepayment-model`, `negative-convexity`, `agency-mbs-pass-through`, `option-adjusted-spread`, `effective-duration`, `reit`, `cap-rate`, `housing-boom-bust` |
| sources | `schwartz1989prepayment`: Schwartz & Torous (1989), JF 44(2); `stanton1995rational`: Stanton (1995), RFS 8(3); `mian2009consequences`: Mian & Sufi (2009), QJE 124(4) |
| lab | Negative convexity of a pass-through. |
| project | Title: "MBS pricer"; brief: "Price an agency pass-through by Monte Carlo with a rate-driven prepayment model, and compute OAS, effective duration and convexity."; deliverable: "Tested pricer."; grading: `autograder` |

### 0.2 Hours Breakdown

- Lessons: **6 lessons × 8 h = 48 h** (60.0% of module hours)
- Project: **32 h** (40.0% of module hours, within the 10–40% curriculum requirement)
- Total: **48 + 32 = 80 h**

### 0.3 Introduced Concepts Mapping

| Concept ID | Name | Assigned Lesson |
|---|---|---|
| `prepayment-model` | Prepayment model | L01 |
| `agency-mbs-pass-through` | Agency MBS pass-through | L02 |
| `negative-convexity` | Negative convexity | L03 |
| `option-adjusted-spread` | Option-adjusted spread | L04 |
| `effective-duration` | Effective duration and convexity | L04 |
| `cap-rate` | Capitalization rate | L05 |
| `reit` | Real estate investment trust | L05 |
| `housing-boom-bust` | The 2000s housing boom and bust | L06 |

### 0.4 Verified Registry Keys

| Key | Citation | Role in PM4 |
|---|---|---|
| `schwartz1989prepayment` | Schwartz & Torous (1989), JF 44(2) | Primary source for hazard-rate prepayment modeling, empirical estimation of refinancing response, and valuation impact in L01, L03, L04 |
| `stanton1995rational` | Stanton (1995), RFS 8(3) | Primary source for rational prepayment under heterogeneous transaction costs and decision-lag frictions in L01, L03, L04 |
| `mian2009consequences` | Mian & Sufi (2009), QJE 124(4) | Primary source for subprime mortgage expansion, geographical credit growth vs. income growth, and foreclosure contagion in L06 |
| `gurkaynak2007us` | Gürkaynak, Sack & Wright (2007), JME 54(8) | Benchmark Treasury curve for discounting, forward rates, and OAS benchmarking in L04 and Project |
| `vasicek1977equilibrium` | Vasicek (1977), JFE 5(2) | One-factor short rate dynamics for term-structure simulation in L04 and Project |
| `cox1985theory` | Cox, Ingersoll & Ross (1985), Econometrica 53(2) | Mean-reverting interest rate diffusion benchmark in L04 |
| `hull2021options` | Hull (2021), Options, Futures, and Other Derivatives | Reference for interest rate derivatives and Monte Carlo simulation mechanics |
| `damodaran2012investment` | Damodaran (2012), Investment Valuation, 3rd ed. | Reference for real estate cash flows, cap rates, and REIT valuation metrics in L05 |
| `campbell2006household` | Campbell (2006), JF 61(4) | Household finance context for mortgage choices and refinancing inertia in L01 |

---

## 1. Lesson Specifications

### Lesson 1: Mortgage Mechanics, Prepayment Dynamics & Hazard Rate Models (8 h)
- **Introduced Concept:** `<dfn id="def-prepayment-model" data-concept="prepayment-model">prepayment model</dfn>`
- **Focus:** Constant-payment mortgage amortization equations; Single Monthly Mortality (SMM) and Conditional Prepayment Rate (CPR); the PSA benchmark curve; empirical hazard rate modeling (Schwartz & Torous 1989); rational prepayment with transaction costs and inattention (Stanton 1995); burnout dynamics and seasonal factors.
- **Inline Lab:** `lab-PM4-L01-1.py` - Prepayment modeling: PSA benchmark vs. Schwartz-Torous hazard rate across interest rate shocks.

### Lesson 2: Agency MBS Pass-Throughs & Cash Flow Waterfalls (8 h)
- **Introduced Concept:** `<dfn id="def-agency-mbs-pass-through" data-concept="agency-mbs-pass-through">Agency MBS pass-through</dfn>`
- **Focus:** Structure of agency pass-throughs (Ginnie Mae, Fannie Mae, Freddie Mac); gross coupon vs. net pass-through coupon (servicing fee and guarantee fee); monthly principal and interest cash flow waterfalls; pool factors; TBA market trading conventions and delay days.
- **Inline Lab:** `lab-PM4-L02-1.py` - Agency pass-through waterfall generator, pool factor evolution, and delay-day adjusted cash flows.

### Lesson 3: Negative Convexity, Price Compression & Embedded Options (8 h)
- **Introduced Concept:** `<dfn id="def-negative-convexity" data-concept="negative-convexity">negative convexity</dfn>`
- **Focus:** Callable bond decomposition; borrower refinancing option; price compression near and above par; negative convexity region; asymmetric duration behavior (duration contraction in rallies, duration extension in selloffs); mortgage basis and convexity hedging feedback loops.
- **Inline Lab:** `lab-PM4-L03-1.py` - Negative convexity: price-yield curve of an agency pass-through vs. bullet bond, verifying local concavity ($d^2P/dy^2 < 0$) and duration extension.

### Lesson 4: Option-Adjusted Spread (OAS) & Effective Risk Metrics (8 h)
- **Introduced Concepts:**
  `<dfn id="def-option-adjusted-spread" data-concept="option-adjusted-spread">option-adjusted spread</dfn>`
  `<dfn id="def-effective-duration" data-concept="effective-duration">effective duration and convexity</dfn>`
- **Focus:** Limitations of static and Z-spreads; risk-neutral Monte Carlo short-rate simulation (Vasicek / Hull-White); path-dependent cash flow generation; calibration of OAS equating simulated expectation to market price; effective duration ($D_{\text{eff}}$) and effective convexity ($C_{\text{eff}}$) via $\pm \Delta y$ curve bumping.
- **Inline Lab:** `lab-PM4-L04-1.py` - Monte Carlo OAS pricer and effective duration/convexity engine for pass-through securities.

### Lesson 5: Commercial Real Estate, Cap Rates & REIT Valuation (8 h)
- **Introduced Concepts:**
  `<dfn id="def-cap-rate" data-concept="cap-rate">capitalization rate</dfn>`
  `<dfn id="def-reit" data-concept="reit">Real Estate Investment Trust</dfn>`
- **Focus:** Commercial property operating statements: PGI, EGI, OpEx, and Net Operating Income (NOI); capitalization rate definition ($R = \text{NOI}/V$) and relation to Gordon growth ($R = r - g$); REIT legal structures and tax qualification; Funds From Operations (FFO) and Adjusted FFO (AFFO); Net Asset Value (NAV) per share bridge.
- **Inline Lab:** `lab-PM4-L05-1.py` - Commercial property cash flow waterfall, cap-rate valuation, and REIT NAV / AFFO reconciliation.

### Lesson 6: The 2000s Housing Boom, Subprime Securitization & Systemic Bust (8 h)
- **Introduced Concept:** `<dfn id="def-housing-boom-bust" data-concept="housing-boom-bust">2000s housing boom and bust</dfn>`
- **Focus:** The originate-to-distribute model; non-agency RMBS and CDO tranche structuring; empirical findings of Mian & Sufi (2009) on credit supply expansion, subprime zip-code decoupling, and mortgage default clustering; home equity extraction via cash-out refinancings; foreclosure spirals and systemic contagion.
- **Inline Lab:** `lab-PM4-L06-1.py` - Mian-Sufi zip-code credit expansion and default rate empirical simulation.

---

## 2. Project Specification: "MBS Pricer" (32 h)

### 2.1 Scope & Ladder
- **Rung 1 (Worked Example):** Deterministic single-path valuation of a 30-year fixed-rate pass-through with PSA prepayment schedule.
- **Rung 2 (Completion Problem):** Completion lab `lab-PM4-project-1.py` completing the stochastic path cash-flow accumulator and Monte Carlo discounting engine.
- **Rung 3 (Independent Project):** Production Monte Carlo MBS pricer:
  1. Generate risk-neutral interest rate paths under mean-reverting short-rate dynamics.
  2. Implement a rate-driven prepayment function combining baseline turnover, refinancing incentive function $\text{CPR}(r_m - r_t)$, and path burnout state tracking.
  3. Formulate pathwise cash flow waterfalls with servicing fees and delay adjustments.
  4. Calibrate the Option-Adjusted Spread (OAS) matching a given market price via Brent / bisection root finding.
  5. Compute effective duration ($D_{\text{eff}}$) and effective convexity ($C_{\text{eff}}$) using symmetric $\pm 25$ bps parallel shifts.
- **Rung 4 (Stretch Extension):** Two-factor short-rate model, stochastic housing equity option with endogenous default, and sequential-pay CMO tranche waterfalls.

### 2.2 Autograder Architecture
- `grader/instance.py`: Generates seed-dependent pool specifications (balance $B_0$, WAC, net coupon $c$, WAM), interest rate parameters ($r_0$, $\kappa$, $\theta$, $\sigma$), prepayment coefficients, and market price $P_{\text{mkt}}$.
- `grader/reference.py`: Reference solver implementing exact vectorized Monte Carlo pricing, OAS bisection, and finite-difference effective Greeks.
- `grader/starter.py`: Skeleton module with type annotations and `NotImplementedError` stubs.
- `grader/integrity.py`: Validates input types, positive balances, realistic interest rates, and finite parameter ranges.
- `grader/test_project.py`: Pytest suite running across seeds 0–49, testing:
  - Cash flow conservation and terminal pool factor convergence to 0.
  - Zero-spread pricing consistency.
  - OAS monotonicity: higher market price yields lower OAS.
  - Effective duration bounds: positive duration for pass-throughs, lower than option-free bonds.
  - Effective convexity negative sign in the refinancing window.
  - Tolerances and numerical stability.
- 5 mutants killed in `ledgers/PM4/mutants/`.

---

## 3. Retrieval Cards (30 Cards)
- 5 cards per lesson (L01 through L06) covering core definitions, theorems, empirical findings, and misconceptions.
