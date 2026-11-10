# Build Plan: SR2 · Leverage Cycles

## 1. Unit Identity & Metadata
- **Unit**: SR2
- **Title**: Leverage Cycles
- **Tier**: D (Doctoral, 60 hours)
- **Part**: SR (Systemic Risk & Financial Stability, `course/modules/SR/SR2/`)
- **Prerequisites**: SR1 (Runs, Liquidity & Fire Sales), AP6 (Intermediary Asset Pricing)
- **Hours Budget**: Lessons 48 h (L01: 10 h, L02: 10 h, L03: 10 h, L04: 9 h, L05: 9 h) + Project 12 h = 60 h total (Project is 20% of total hours).
- **Core Topics**: Endogenous leverage, procyclical balance sheets (Adrian & Shin 2010), Geanakoplos collateral equilibrium & margin shocks (Geanakoplos 2010), macro models with a financial sector (Brunnermeier & Sannikov 2014).
- **Introduced Concepts**:
  - `procyclical-leverage`: "Procyclical leverage" (L01)
  - `collateral-equilibrium`: "Collateral equilibrium" (L02)
  - `leverage-cycle`: "Leverage cycle" (L04)
  - `macro-financial-friction-model`: "Macro model with a financial sector" (L05)
- **Verified References**:
  - `adrian2010liquidity` (Adrian & Shin 2010, JFI 19(3): 418-437)
  - `adrian2014financial` (Adrian, Etula & Muir 2014, JF 69(6): 2557-2596)
  - `geanakoplos2010leverage` (Geanakoplos 2010, NBER Macro Ann 24(1): 1-66)
  - `brunnermeier2014macroeconomic` (Brunnermeier & Sannikov 2014, AER 104(2): 379-421)
  - `brunnermeier2008market` (Brunnermeier & Pedersen 2008, RFS 22(6): 2201-2238)
  - `shleifer2011fire` (Shleifer & Vishny 2011, JEP 25(1): 29-48)
  - `shleifer1997limits` (Shleifer & Vishny 1997, JF 52(1): 35-55)
  - `gorton2012securitized` (Gorton & Metrick 2012, JFE 104(3): 425-451)
  - `he2013intermediary` (He & Krishnamurthy 2013, AER 103(2): 732-770)

---

## 2. Lessons Architecture

### Lesson 1: Procyclical Leverage and Intermediary Balance Sheets (10 h)
- **Why it matters**: Explains why modern financial intermediaries amplify business cycles rather than dampening them, establishing mark-to-market accounting mechanisms.
- **Concept defined**: `procyclical-leverage` (`<dfn id="def-procyclical-leverage" data-concept="procyclical-leverage">`)
- **Key Theory & Theorems**:
  - Distinction between household/corporate countercyclical leverage vs broker-dealer procyclical leverage.
  - Value-at-Risk (VaR) equity constraint: $E_t \ge \alpha \cdot \text{VaR}_t = \alpha \cdot Z \cdot \sigma_t A_t \implies L_t \le \frac{1}{\alpha Z \sigma_t}$.
  - Proposition: In low-volatility regimes ($\sigma_t \downarrow$), permissible leverage expands mechanically; in high-volatility regimes ($\sigma_t \uparrow$), rapid deleveraging is mandatory.
  - Adrian–Shin balance sheet adjustment identity: $\Delta A_{\text{new}} = L^* \Delta A$.
- **Lab 1**: `lab-SR2-L01-1.py` - Simulates broker-dealer balance sheet adjustments under countercyclical, constant, and procyclical VaR leverage rules, showing fire-sale supply under price drops.
- **Misconceptions**: (1) High leverage caused by debt inertia; (2) Commercial banks and broker-dealers manage leverage identically; (3) Mark-to-market accounting is always stabilizing.
- **Problem Set**: 12 problems (3 Mechanics, 3 Proof, 3 Empirical, 3 Research) with complete solutions.
- **Quiz**: 10 items.

### Lesson 2: Geanakoplos Collateral Equilibrium Mechanics (10 h)
- **Why it matters**: Demonstrates how collateral constraints replace standard Walrasian market clearing and determine endogenous debt capacity and asset prices.
- **Concept defined**: `collateral-equilibrium` (`<dfn id="def-collateral-equilibrium" data-concept="collateral-equilibrium">`)
- **Key Theory & Theorems**:
  - The collateral contract space $(j, C)$ with no-recourse default payoffs $\min(j, V_s)$.
  - Two-state safe loan condition: $L = V_D / R_f$.
  - Theorem: Marginal Buyer Determination in Collateral Equilibrium. Risk-neutral continuum of investors $h \in [0, 1]$ with $p^h = h$.
    - Marginal buyer condition: $\frac{h^*(V_U - V_D)}{P - V_D} = R_f$.
    - Asset market clearing: $\frac{1 - h^*}{P - V_D} = Q$.
    - Closed form: $h^* = \frac{1}{1 + (V_U - V_D)/R_f}$, $P = V_D/R_f + \frac{(V_U - V_D)/R_f}{1 + (V_U - V_D)/R_f}$.
- **Lab 1**: `lab-SR2-L02-1.py` - Exact numerical solution and analytical verification of the Geanakoplos two-state collateral equilibrium.
- **Misconceptions**: (1) Interest rates are the sole price of credit (ignoring collateral haircuts); (2) Optimists always set asset prices alone; (3) Collateral requirements prevent all price volatility.
- **Problem Set**: 12 problems with complete solutions.
- **Quiz**: 10 items.

### Lesson 3: Margin Spirals and Fire Sales (10 h)
- **Why it matters**: Models the non-linear positive feedback loop linking falling asset values to widening hair-cuts and forced asset sales in wholesale funding markets.
- **Key Theory & Theorems**:
  - Brunnermeier–Pedersen (2008) model: Funding liquidity vs market liquidity.
  - Loss spiral vs margin spiral.
  - Haircut widening mechanics under endogenous risk and VaR constraints.
  - Multiplier condition: $\mathcal{M} = \frac{1}{1 - \kappa \frac{\partial \text{Sales}}{\partial P}}$. Proof of divergence threshold.
  - The repo market freeze (Gorton & Metrick 2012).
- **Lab 1**: `lab-SR2-L03-1.py` - Simulates discrete-time loss and margin spirals, computing the critical feedback multiplier.
- **Misconceptions**: (1) A solvent financial institution cannot be brought down by margin calls; (2) Central bank discount window access automatically eliminates wholesale margin runs; (3) Haircuts are fixed contractual parameters.
- **Problem Set**: 12 problems with complete solutions.
- **Quiz**: 10 items.

### Lesson 4: The Leverage Cycle Over Macroeconomic Cycles (9 h)
- **Why it matters**: Unifies credit booms, volatility compression, sudden margin shocks, and macroeconomic contractions across multi-period trees.
- **Concept defined**: `leverage-cycle` (`<dfn id="def-leverage-cycle" data-concept="leverage-cycle">`)
- **Key Theory & Theorems**:
  - Multi-period tree $t=0, 1, 2$: calm regime vs news shock.
  - Why tranquil periods induce endogenous vulnerability: bad state variance shrinks, lenders lower haircuts, optimists lever up.
  - Bad news shock: raises variance, triggers margin shock, wipes out optimist equity.
  - Double price crash: fundamental downgrade + marginal buyer shift downward to pessimists.
  - Macroprudential policy: regulating leverage vs interest rates.
- **Lab 1**: `lab-SR2-L04-1.py` - Multi-period simulation of the leverage cycle across calm, shock, and bust phases.
- **Misconceptions**: (1) Asset bubbles require irrational exuberance; (2) Lowering interest rates during a leverage cycle bust restores asset prices without equity recapitalization; (3) Stable asset prices indicate financial stability.
- **Problem Set**: 12 problems with complete solutions.
- **Quiz**: 10 items.

### Lesson 5: Macroeconomic Models with Intermediary Balance Sheets (9 h)
- **Why it matters**: Bridges micro-foundations of intermediary balance sheets to dynamic continuous-time stochastic general equilibrium models.
- **Concept defined**: `macro-financial-friction-model` (`<dfn id="def-macro-financial-friction-model" data-concept="macro-financial-friction-model">`)
- **Key Theory & Theorems**:
  - Brunnermeier & Sannikov (2014) model: Productive experts with capital $K_t$ vs households.
  - Expert net worth share $\eta_t = \frac{N_t}{q_t K_t}$ as endogenous state variable.
  - Drift and diffusion equations for $\eta_t$.
  - The Volatility Paradox: Low exogenous volatility leads to high leverage, generating high endogenous risk and instability.
  - Non-linear systemic crisis state and fire-sale dynamics near $\eta \to 0$.
- **Lab 1**: `lab-SR2-L05-1.py` - Numerical solution of the Brunnermeier–Sannikov state-variable boundary value ODE/PDE for capital price $q(\eta)$ and expert wealth share $\eta$.
- **Misconceptions**: (1) Linear DSGE models with representative agents capture financial crises; (2) The financial sector is a passive intermediary between savers and investors; (3) Low macroeconomic volatility implies low systemic risk.
- **Problem Set**: 12 problems with complete solutions.
- **Quiz**: 10 items.

---

## 3. Project: Leverage-Cycle Model

### Specification
- **Title**: Leverage-Cycle Model: Collateral Equilibrium & Margin Shock Solver
- **Hours**: 12 h
- **Deliverables**:
  1. `solver.py`: Python module containing `solve_geanakoplos_equilibrium`, `simulate_margin_shock`, and `solve_three_period_cycle`.
  2. `writeup.md`: Quantitative research memo evaluating equilibrium prices, margin spirals, and policy implications.
- **Grading**: Both (Autograder on `solver.py` across 50 seeds; Rubric on `writeup.md` with 5 criteria across 4 levels).
- **Ladder**:
  - Rung 1: Worked example solving representative Geanakoplos model (`lab-SR2-project-1.py`).
  - Rung 2: Completion problem with `___` blanks (`lab-SR2-project-2.py`).
  - Rung 3: Full independent solver with parameter validation and edge cases.
  - Rung 4: Open-ended extension to multi-state endogenous default or continuous optimism distributions.

---

## 4. Cards & Testing Plan
- `cards.json`: 22-24 atomic cards with valid grades (T/A/B/C) and verified references.
- Lab twins in `tests/labs/SR2/`: 8 twins total (5 lesson labs + 3 project labs).
- Autograder suite in `grader/`:
  - `instance.py`: deterministic generator `make_instance(seed: int) -> dict`.
  - `reference.py`: reference implementation.
  - `starter.py`: stub implementation for students.
  - `test_project.py`: comprehensive pytest suite (algebraic identities, KKT conditions, boundary checks, 50 seeds).
- Mutants in `ledgers/SR2/mutants/`: 5 plausible wrong implementations, all killed by `mutate_graders.py`.
