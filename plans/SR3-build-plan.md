# Build Plan: SR3 · Measuring Systemic Risk

## 1. Unit Identity & Metadata
- **Unit**: SR3
- **Title**: Measuring Systemic Risk
- **Tier**: M (Mastery, 50 hours)
- **Part**: SR (Systemic Risk & Financial Stability, `course/modules/SR/SR3/`)
- **Prerequisites**: SR1 (Runs, Liquidity & Fire Sales), PR4 (Risk Measurement)
- **Hours Budget**: Lessons 40 h (L01: 10 h, L02: 10 h, L03: 10 h, L04: 10 h) + Project 10 h = 50 h total (Project is 20% of total hours).
- **Core Topics**: CoVaR & quantile regression (Adrian & Brunnermeier 2016 AER), Marginal Expected Shortfall & LRMES (Acharya et al. 2017 RFS), SRISK & conditional capital shortfall (Brownlees & Engle 2017 RFS), network contagion & interbank cascades (Acemoglu et al. 2015 AER).
- **Introduced Concepts**:
  - `covar`: "CoVaR" (defined in L01, `<dfn id="def-covar" data-concept="covar">CoVaR</dfn>`)
  - `marginal-expected-shortfall`: "Marginal expected shortfall" (defined in L02, `<dfn id="def-marginal-expected-shortfall" data-concept="marginal-expected-shortfall">Marginal expected shortfall</dfn>`)
  - `srisk`: "SRISK" (defined in L03, `<dfn id="def-srisk" data-concept="srisk">SRISK</dfn>`)
  - `network-contagion`: "Network contagion" (defined in L04, `<dfn id="def-network-contagion" data-concept="network-contagion">Network contagion</dfn>`)
- **Atlas Milestone**: Milestone A19 (`atlas/A19.contract.md`), delivers `atlas.systemic` (`atlas/systemic.py`).
- **Verified References**:
  - `adrian2016covar`: Adrian & Brunnermeier (2016), AER 106(7): 1705–1741.
  - `acharya2016measuring`: Acharya, Pedersen, Philippon & Richardson (2017), RFS 30(1): 2–47.
  - `brownlees2016srisk`: Brownlees & Engle (2017), RFS 30(1): 48–79.
  - `acemoglu2015systemic`: Acemoglu, Ozdaglar & Tahbaz-Salehi (2015), AER 105(2): 564–608.
  - `adrian2010liquidity`: Adrian & Shin (2010), JFI 19(3): 418–437.
  - `brunnermeier2008market`: Brunnermeier & Pedersen (2009), RFS 22(6): 2201–2238.
  - `engle1982autoregressive`: Engle (1982), Econometrica 50(4): 987–1007.
  - `white1980heteroskedastici`: White (1980), Econometrica 48(4): 817–838.

---

## 2. Lessons Architecture

### Lesson 1: CoVaR & Quantile Regression (10 h)
- **Why it matters**: Microprudential risk metrics like individual VaR fail to capture externalities; CoVaR quantifies the spillover risk an institution imposes on the entire financial system when stressed.
- **Concept defined**: `covar` (`<dfn id="def-covar" data-concept="covar">CoVaR</dfn>`)
- **Key Theory & Theorems**:
  - Definition of $\text{CoVaR}_{q}^{s|i}$: the $q$-quantile of system losses conditional on institution $i$ experiencing its own $q$-quantile loss $\text{VaR}_q^i$.
  - $\Delta\text{CoVaR}_q^i = \text{CoVaR}_q^{s|i} - \text{CoVaR}_q^{s|\text{median}} = \hat{\beta}_q^i (\text{VaR}_q^i - \text{VaR}_{0.5}^i)$ (Adrian & Brunnermeier 2016 Theorem / Eq. 6).
  - Quantile regression objective: pinball loss $\rho_q(u) = u(q - \indic_{\{u < 0\}})$ and first-order conditions.
  - Macroeconomic state variables $M_{t-1}$ (volatility, credit spread, term slope, liquidity spread).
  - Difference between systemic contribution (institution distress driving system distress) vs systemic vulnerability (institution vulnerable to system distress).
  - Dollar $\Delta\text{CoVaR}^\$ = W_i \cdot \Delta\text{CoVaR}_i$.
- **Lab 1**: `lab-SR3-L01-1.py` - CoVaR and $\Delta\text{CoVaR}$ estimation via linear quantile optimization and OLS benchmark comparison on institutional returns.
- **Misconceptions**: (1) An institution with low individual VaR cannot be systemically dangerous; (2) $\Delta\text{CoVaR}$ is symmetric between institution and system; (3) Conditioning on institution distress implies direct bilateral counterparty exposure.
- **Problem Set**: 12 problems (3 Mechanics, 3 Proof, 3 Empirical, 3 Research) with complete solutions.
- **Quiz**: 10 items.

### Lesson 2: Marginal Expected Shortfall & Long-Run MES (10 h)
- **Why it matters**: Formalizes systemic risk through welfare economics and negative externalities; MES measures how much an institution's equity erodes during a severe market downturn.
- **Concept defined**: `marginal-expected-shortfall` (`<dfn id="def-marginal-expected-shortfall" data-concept="marginal-expected-shortfall">Marginal expected shortfall</dfn>`)
- **Key Theory & Theorems**:
  - Definition of MES: $\text{MES}_\alpha^i = -\E[R_i \mid R_{\text{sys}} \le \text{VaR}_\alpha^{\text{sys}}]$.
  - Microfoundations: systemic expected shortfall (SES), optimal Pigouvian systemic tax based on expected capital shortfall externalities.
  - Tail dependence and the link between standard equity beta $\beta_i$ and MES under joint normality vs heavy tails.
  - Long-Run MES (LRMES): expected equity drop over a 6-month crisis with a 40% systemic market drop: $\text{LRMES}_i = 1 - \exp(\ln(1 - d) \cdot \beta_i)$ or $\text{LRMES}_i \approx 1 - \exp(-18 \times \text{MES}_i)$.
- **Lab 1**: `lab-SR3-L02-1.py` - Non-parametric MES, extreme crisis conditioning, and LRMES projection across financial firms.
- **Misconceptions**: (1) MES is proportional to standard CAPM beta in all distributions; (2) MES measures the risk of the institution failing alone; (3) Diversification across institutions reduces aggregate MES.
- **Problem Set**: 12 problems with complete solutions.
- **Quiz**: 10 items.

### Lesson 3: SRISK & Conditional Capital Shortfall Index (10 h)
- **Why it matters**: Combines market-based tail risk (LRMES) with accounting balance sheet leverage and firm size to deliver a dollar-denominated systemic capital shortfall measure.
- **Concept defined**: `srisk` (`<dfn id="def-srisk" data-concept="srisk">SRISK</dfn>`)
- **Key Theory & Theorems**:
  - Prudential capital fraction $k$ (e.g. 8% for US, 5.5% for Europe).
  - Book debt $D_i$ and market value of equity $W_i$.
  - Post-crisis equity value: $W_i^{\text{crisis}} = (1 - \text{LRMES}_i) W_i$.
  - Post-crisis total assets: $A_i^{\text{crisis}} = D_i + (1 - \text{LRMES}_i) W_i$.
  - Required equity capital: $k A_i^{\text{crisis}} = k (D_i + (1 - \text{LRMES}_i) W_i)$.
  - Capital shortfall formula: $\text{SRISK}_i = \max\left(0, \; k D_i - (1 - k)(1 - \text{LRMES}_i) W_i\right)$.
  - Aggregate systemic risk: $\text{SRISK}_{\text{sys}} = \sum_i \text{SRISK}_i$ and systemic contribution percentage $\text{SRISK}\%_i$.
  - Comparative statics: $\frac{\partial \text{SRISK}_i}{\partial D_i} = k$, $\frac{\partial \text{SRISK}_i}{\partial \text{LRMES}_i} = (1 - k) W_i$, $\frac{\partial \text{SRISK}_i}{\partial W_i} = -(1 - k)(1 - \text{LRMES}_i)$.
- **Lab 1**: `lab-SR3-L03-1.py` - Multi-firm conditional capital shortfall computation, sensitivity decomposition, and aggregate index tracking.
- **Misconceptions**: (1) A firm with negative capital shortfall (surplus) offsets other firms' deficits in aggregate SRISK; (2) High leverage alone creates high SRISK regardless of LRMES; (3) SRISK is purely an equity market measure that ignores debt liabilities.
- **Problem Set**: 12 problems with complete solutions.
- **Quiz**: 10 items.

### Lesson 4: Network Contagion & Interbank Cascade Dynamics (10 h)
- **Why it matters**: Financial institutions do not fail in isolation; nominal bilateral interbank liabilities create complex cascade channels that exhibit non-linear phase transitions.
- **Concept defined**: `network-contagion` (`<dfn id="def-network-contagion" data-concept="network-contagion">Network contagion</dfn>`)
- **Key Theory & Theorems**:
  - Interbank network structure: bilateral nominal liability matrix $L_{ij}$, total obligations $\bar{p}_i = \sum_j L_{ij}$, relative liabilities $\Pi_{ij} = L_{ij} / \bar{p}_i$.
  - Eisenberg-Noe clearing payments: $p_i^* = \min\left(\bar{p}_i, \; \max\left(0, \; z_i + \sum_j \Pi_{ji} p_j^* - b_i\right)\right)$.
  - Acemoglu, Ozdaglar & Tahbaz-Salehi (2015) phase transition theorem: dense networks diversify and absorb small shocks ($\epsilon < \epsilon^*$), but act as contagion propagation mechanisms that maximize distress under large catastrophic shocks ($\epsilon > \epsilon^*$).
  - Topology comparison: complete network vs ring network vs tiered money-center / core-periphery architecture.
  - Cascade dynamics: iterative default rounds, systemic loss multipliers, and waterfall liquidation.
- **Lab 1**: `lab-SR3-L04-1.py` - Fixed-point Picard clearing vector solver, cascade round simulation, and phase-transition threshold verification under varying network connectivity.
- **Misconceptions**: (1) Greater network interconnectedness always enhances financial stability; (2) Network contagion occurs only when counterparties hold zero equity capital; (3) The clearing vector depends on the sequence in which defaults are declared.
- **Problem Set**: 12 problems with complete solutions.
- **Quiz**: 10 items.

---

## 3. Project Architecture: Atlas A19 Systemic-Risk Monitor (10 h)
- **Milestone**: A19 (`atlas.systemic` in `atlas/systemic.py`)
- **Contract**: `atlas/A19.contract.md`
- **Ladder**:
  - Rung 1: Worked example (`lab-SR3-project-1.py`)
  - Rung 2: Completion problem (`lab-SR3-project-2.py`, completion lab)
  - Rung 3: Independent project (Full systemic monitor with CoVaR, MES, SRISK, Network Clearing, and Alert Thresholds)
  - Rung 4: Stretch extension (`lab-SR3-project-3.py`, dynamic multi-horizon stress cascade engine)
- **Grader**:
  - `grader/instance.py`: deterministic instance generator (seed 0-49)
  - `grader/reference.py`: reference implementation passing all tests
  - `grader/starter.py`: template with NotImplementedError
  - `grader/test_project.py`: acceptance test suite
  - 5 adversarial mutants in `ledgers/SR3/mutants/` (all killed)
- **Cards**: 24 comprehensive cards in `course/modules/SR/SR3/cards.json`.
