# PM3 Build Plan: Private Credit & Infrastructure

Unit: **PM3 · Private Credit & Infrastructure** · tier M · 40 h · prerequisites PM1, CR1 · grading `both` · output directory `course/modules/PM/PM3/` · lab twins `tests/labs/PM3/` · grader `course/modules/PM/PM3/grader/`.

---

## 0. Curriculum Facts & Requirements

### 0.1 Curriculum Facts (`curriculum/curriculum.json`)

| Field | Value |
|---|---|
| id | `PM3` |
| title | `Private Credit & Infrastructure` |
| part | `PM` (`Private Markets & Real Estate`) |
| tier | `M` |
| hours | `40` |
| prereqs | `["PM1", "CR1"]` |
| core | Direct lending, BDCs, unitranche structures, infrastructure cash flows, smoothing and marking. Thin evidence base, graded strictly. |
| introduces | `direct-lending`, `business-development-company`, `unitranche`, `infrastructure-cash-flows`, `appraisal-smoothing` |
| sources | `chernenko2022firms`: Chernenko, Erel & Prilmeier (2022), RFS 35(11); `davydiuk2024direct`: Davydiuk, Marchuk & Rosen (2024), JFE 162; `block2024survey`: Block, Jang, Kaplan & Schulze (2024), RCFS 13(2); `andonov2021institutional`: Andonov, Kräussl & Rauh (2021), RFS 34(8); `couts2024unsmoothing`: Couts, Gonçalves & Rossi (2024), RFS 37(7) |
| lab | Appraisal smoothing vs. public-market proxies. |
| project | Title: "Unsmoothing private credit"; brief: "Unsmooth a reported private-credit return series, and compare its true risk with a public leveraged-loan proxy."; deliverable: "Code plus memo."; grading: `both` |

### 0.2 Hours Breakdown

- Lessons: **4 lessons = 26 h** (65.0% of module hours)
  - L01: Direct Lending & Middle-Market Credit (6 h)
  - L02: BDCs, Unitranche Loans & Capital Structure Subordination (7 h)
  - L03: Infrastructure Assets, Concessions & Cash-Flow Profiles (6 h)
  - L04: Appraisal Smoothing, De-smoothing Models & Hidden Risk (7 h)
- Capstone Project: **14 h** (35.0% of module hours, within the 10–40% curriculum requirement)
- Total: **26 + 14 = 40 h**

### 0.3 Introduced Concepts Mapping

| Concept ID | Name | Assigned Lesson |
|---|---|---|
| `direct-lending` | Direct lending | L01 |
| `business-development-company` | Business development company (BDC) | L02 |
| `unitranche` | Unitranche loan | L02 |
| `infrastructure-cash-flows` | Infrastructure cash flows | L03 |
| `appraisal-smoothing` | Appraisal smoothing and marking of private assets | L04 |

### 0.4 Verified Registry Keys

| Key | Citation | Role in PM3 |
|---|---|---|
| `chernenko2022firms` | Chernenko, Erel & Prilmeier (2022), RFS 35(11) | Direct lending vs bank loans, middle-market borrower risk profiles, leverage ratios, and pricing in L01 |
| `davydiuk2024direct` | Davydiuk, Marchuk & Rosen (2024), JFE 162 | Direct lender loan terms, covenant structures, EBITDA add-backs, and lender concentration in L01, L02 |
| `block2024survey` | Block, Jang, Kaplan & Schulze (2024), RCFS 13(2) | Private debt fund manager survey, target IRRs, underwriting metrics, workout frequencies, and leverage in L01, L02 |
| `andonov2021institutional` | Andonov, Kräussl & Rauh (2021), RFS 34(8) | Institutional investors in infrastructure, fund vs direct performance, concession cash flows, and public pension bias in L03 |
| `couts2024unsmoothing` | Couts, Gonçalves & Rossi (2024), RFS 37(7) | Unsmoothing private fund returns, state-space filtering, true vs reported volatility, beta to leveraged loans in L04, Project |
| `getmansky2004econometric` | Getmansky, Lo & Makarov (2004), JFE 74(3) | Moving-average return smoothing model, serial correlation, and variance distortion formulas in L04, Project |

---

## 1. Lesson Specifications

### Lesson 1: Direct Lending & Middle-Market Credit (6 h)
- **Introduced Concept:** `<dfn id="def-direct-lending" data-concept="direct-lending">Direct lending</dfn>`
- **Focus:** Growth of nonbank corporate lending post-GFC; borrower selection and the bank-disintermediation premium; floating-rate contract architecture (SOFR, spreads, floors, original issue discounts [OID]); financial maintenance covenants vs incurrence covenants; EBITDA add-backs and synthetic covenant relaxation.
- **Inline Lab:** `lab-PM3-L01-1.py` - Floating-rate direct loan yield engine: all-in yields across SOFR regimes with floors, OID amortization, and prepayment call schedules.

### Lesson 2: BDCs, Unitranche Loans & Capital Structure Subordination (7 h)
- **Introduced Concepts:**
  - `<dfn id="def-business-development-company" data-concept="business-development-company">Business development company (BDC)</dfn>`
  - `<dfn id="def-unitranche" data-concept="unitranche">Unitranche loan</dfn>`
- **Focus:** BDC regulatory architecture under the 1940 Act and 2018 Small Business Credit Availability Act; asset coverage ratios and RIC tax conduit rules; unitranche loan structuring and the Agreement Among Lenders (AAL); First-Out (FO) and Last-Out (LO) synthetic subordination; cash flow and liquidation recovery waterfalls; Level 3 fair value accounting under ASC 820.
- **Inline Lab:** `lab-PM3-L02-1.py` - Unitranche Agreement Among Lenders (AAL) recovery and yield waterfall: FO/LO cash flow distribution and loss absorption under enterprise distress.

### Lesson 3: Infrastructure Assets, Concessions & Cash-Flow Profiles (6 h)
- **Introduced Concept:** `<dfn id="def-infrastructure-cash-flows" data-concept="infrastructure-cash-flows">Infrastructure cash flows</dfn>`
- **Focus:** Economic vs social infrastructure; concession contracts (DBFOM) and Public-Private Partnerships (P3); availability payment mechanisms vs volume/demand risk (toll elasticity); project finance ring-fenced SPVs; non-recourse debt sizing; debt service coverage ratios (DSCR), loan life coverage ratios (LLCR), and debt service reserve accounts (DSRA); institutional performance and governance distortions (Andonov et al. 2021).
- **Inline Lab:** `lab-PM3-L03-1.py` - Project finance infrastructure cash flow model: CFADS sculpting, DSCR/LLCR constraints, and availability vs merchant equity return profiles.

### Lesson 4: Appraisal Smoothing, De-smoothing Models & Hidden Risk (7 h)
- **Introduced Concept:** `<dfn id="def-appraisal-smoothing" data-concept="appraisal-smoothing">Appraisal smoothing and marking of private assets</dfn>`
- **Focus:** Mechanics of Level 3 appraisal marking in illiquid debt and private assets; AR(1) and MA(q) econometric smoothing models; theoretical derivation of observed vs true variance, beta, and Sharpe ratios; de-smoothing methodologies (Geltner inversion, Getmansky et al. 2004, state-space de-smoothing in Couts et al. 2024); empirical comparison between private debt indices and public syndicated leveraged loan proxies.
- **Inline Lab:** `lab-PM3-L04-1.py` - AR(1) de-smoothing engine on quarterly private debt returns: parameter estimation, true volatility recovery, beta expansion, and Sharpe ratio adjustment.

---

## 2. Project Specification: "Unsmoothing Private Credit" (14 h)

### 2.1 Scope & Ladder
- **Rung 1 (Worked Example):** Step-by-step de-smoothing of an illustrative 20-quarter reported private credit return series, verifying exact AR(1) inversion, volatility expansion, and beta correction.
- **Rung 2 (Completion Problem):** `lab-PM3-project-1.py`: Complete the core de-smoothing kernel, variance correction factor, beta regression, and de-smoothed risk statistics.
- **Rung 3 (Independent Project):** Production module `reference.py` tested across 50 seeds by `test_project.py`, and an institutional LP due diligence memo evaluated by rubric C1–C5.
- **Rung 4 (Stretch):** Time-varying smoothing Kalman filter, regime-switching autocorrelation, and liquidity-risk alpha decomposition.

### 2.2 Autograder & Rubric
- `grader/instance.py`: Generates 40 quarters of reported private credit returns and public leveraged loan proxy returns with seed-dependent parameters.
- `grader/reference.py`: Reference implementation passing seeds 0–49 in under 5 seconds.
- `grader/starter.py`: Incomplete implementation raising `NotImplementedError` or returning blanks to verify fail behavior.
- `grader/test_project.py`: Robust pytest suite checking mathematical properties, bounds, invariants, and numeric outputs.
- `ledgers/PM3/mutants/`: 5 mutants (`mutant_1.py` to `mutant_5.py`) testing subtle student errors, deterministically killed on seed 0.
