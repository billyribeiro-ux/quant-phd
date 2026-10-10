# Master Blueprint — Doctoral Program in Global Macro & Quantitative Finance

**Status:** Architecture v1.0 (2026-10-10) · **Chief architect:** Claude · **Owner:** Billy Ribeiro
**Companion contracts:** [BUILDER_RULES.md](BUILDER_RULES.md) (system prompt for module builders) ·
[VERIFIER_RULES.md](VERIFIER_RULES.md) (system prompt for independent verifiers)

---

## 1. Mission and exit standard

Take a student from zero (high-school algebra) to the level of a graduate of the
coursework years of a top finance or economics PhD (Harvard, MIT, Yale, Chicago,
Stanford, Princeton). Then go past it in the areas that the academy teaches
weakly: implementation, research integrity, market plumbing, and the evidence
behind practice.

"PhD-level" is defined operationally. A graduate of this program can:

1. **Pass a first-year qualifying exam** in asset pricing theory, empirical
   asset pricing, econometrics and macro/monetary economics, closed-book and timed.
2. **Derive the canon from first principles.** That means the FTAP, the SDF,
   Black-Scholes-Merton via replication and via change of measure, affine term
   structure, Kyle's lambda, the Merton portfolio problem, and the NK
   three-equation model.
3. **Replicate a published empirical result** from raw data, with correct
   inference (HAC/clustered errors, Shanken correction, multiple-testing
   adjustment), and say where the result is fragile.
4. **Argue every major open debate** in the field (Section 9, CAP2). For each,
   they can state the strongest case for each side, the graded evidence, and
   what new evidence would settle it.
5. **Build production-grade research code.** That means point-in-time data,
   no lookahead, a realistic cost model, and out-of-sample protocols that
   withstand an adversarial referee.

The edge over a professor is not more theorems. It is the combination of
(a) the full theory canon, (b) a live map of which results replicate and which
don't, and (c) the implementation reality that most academic courses leave out.

---

## 2. The evidence standard (non-negotiable)

Every substantive claim on every page carries an **evidence grade** and at
least one **citation key** that resolves to the verified reference registry.

| Grade | Meaning | Allowed phrasing |
|---|---|---|
| **T** | Mathematical theorem, proven on the page or with a cited proof | "Theorem.", "It follows that" |
| **A** | Replicated out of sample, by independent teams, across periods and/or markets | "The evidence shows" |
| **B** | Peer-reviewed in a top venue, but not robustly replicated, or actively contested | "Published evidence indicates…; contested by…" |
| **C** | Working paper, practitioner research, single-sample or short-sample evidence | "One study finds…" |
| **D** | Practitioner lore with no systematic evidence | Only as "It is widely claimed that…", always flagged |
| **X** | Refuted, failed replication, or retracted | "Earlier work claimed…; this did not survive…" |

Rules that follow from the table:

- Numbers in prose come from one of three places. They are computed live on
  the page from embedded data, quoted with a precise locator (paper, table or
  figure, panel), or derived in a shown calculation. No other numbers.
- A claim graded B or C must name the counter-evidence if any exists. One-sided
  presentation of a contested claim is a build failure.
- Training-data recall is a **source of candidates, never a source of truth**.
  Every citation and every quoted number is checked against the source by the
  verifier before a module merges. This catches recall errors (wrong year,
  wrong journal, misattributed result) mechanically instead of trusting any
  model's confidence. It is the single feature that lets the program survive
  hostile review by the people it cites.
- **Freshness:** the knowledge base runs through mid-2026. During the build,
  verifiers check each working paper for a later published version, and each
  contested debate for 2025–2026 contributions, then update the registry.

---

## 3. Languages and tooling, with the evidence for each choice

The evidence for each choice is public: firms' own engineering
publications and job requirements, the dominant open-source quant libraries,
and the published scientific-computing literature. Module QR1 teaches this
section with full citations. Builders must not invent usage percentages or
survey statistics. Claims stay qualitative unless a verified survey is cited.

| Language | Role in industry and research | Program role | Runs in-page via |
|---|---|---|---|
| **Python 3** (NumPy, SciPy, pandas, Polars, statsmodels, scikit-learn, PyTorch) | Default research language across buy-side quant research and academic empirical finance. The core libraries are documented in peer-reviewed venues (NumPy: Harris et al. 2020, *Nature*; SciPy: Virtanen et al. 2020, *Nature Methods*; scikit-learn: Pedregosa et al. 2011, *JMLR*) | **Primary.** Every lab | Pyodide (CPython compiled to WebAssembly), vendored and pinned |
| **C++ (C++20)** | Pricing libraries (QuantLib is C++), low-latency trading systems, performance-critical risk | Pricing and HPC labs (DV4, QR7) | Compiled to WASM with Emscripten at build time; output asserted in CI |
| **SQL** | Research data access, point-in-time joins, warehouse queries | Data-engineering labs (QR2, F1) | DuckDB-WASM (supports window functions and `ASOF JOIN`, the core time-series join) |
| **q / kdb+** | Tick-data storage and analytics at many banks and HFT firms | Reading literacy (QR1 appendix) | Static, annotated code (not executed) |
| **R** | Academic econometrics and statistics | Reading literacy (S-series appendices) | Static, annotated code |
| **Rust, OCaml** | Trading infrastructure. Jane Street's use of OCaml is documented by the firm itself (Minsky, "OCaml for the Masses", *ACM Queue*, 2011) | Context only (QR1) | — |

**Front-end stack.** The pages are static HTML5 with vanilla ES modules, so there
is no framework churn. The site is designed for 10-year longevity.

- **Math:** KaTeX, vendored.
- **Charts and diagrams:** hand-authored inline SVG, plus D3 v7 (vendored) for
  data charts.
- **Runnable code:** Pyodide, DuckDB-WASM and Emscripten output, all vendored
  and pinned in `vendor/LOCK.json` with SHA-256 hashes. Nothing loads from a CDN
  at runtime.

**Self-contained means self-contained.** The whole site works offline. WASM
runtimes cannot load over `file://`, so the program ships with a one-line local
server (`python3 -m http.server`) and is also hostable as a static site with no
backend.

**Build and verification toolchain:** Python 3.12, pytest, Playwright with the
pre-installed Chromium, and a Crossref and DOI resolver client.

---

## 4. Repository and site architecture

```
course/
├── index.html                      # Program map: interactive prerequisite DAG, progress, search
├── assets/
│   ├── css/  tokens.css base.css components.css print.css
│   ├── js/   core.js (nav, theme, progress) lab.js (Pyodide/DuckDB runner)
│   │         chart.js (D3 wrappers) quiz.js refs.js (citation popovers)
│   ├── vendor/  katex/ pyodide/ duckdb-wasm/ d3/ LOCK.json
│   ├── data/    *.csv|*.parquet + MANIFEST.json
│   └── wasm/    compiled C++ lab modules
├── modules/<PART>/<ID>-<slug>.html # One page per module (92 modules, Section 9)
├── references/references.json      # THE citation registry. The only legal citation source
├── references/index.html           # Generated bibliography
├── notation/notation.json          # Global symbol registry. One symbol, one meaning
├── notation/glossary.json          # Defined terms → defining module
├── curriculum/curriculum.json      # DAG: id, title, prereqs, concepts_introduced, concepts_used, hours
├── ledgers/<ID>.verification.json  # Verifier output. A module merges only if every row passes
└── tools/
    ├── fetch_data.py       # Downloads public data, writes MANIFEST (url, retrieved_at, license, sha256, transform)
    ├── add_reference.py    # DOI → Crossref metadata → registry entry (never hand-typed)
    ├── verify_refs.py      # Re-resolves every DOI and cross-checks title, authors, year, venue
    ├── run_labs.py         # Executes every lab under the pinned Pyodide-matching CPython and asserts expected output
    ├── check_pages.py      # Template conformance, banned phrases, grade tags, citation keys, notation, a11y
    ├── check_dag.py        # Every concept used must be introduced in a transitive prerequisite
    └── page_smoke.py       # Playwright: zero console errors, KaTeX renders, labs execute in the browser, light/dark
```

**Data policy.** Embed only data whose license permits redistribution:

- FRED series in the public domain (third-party-copyrighted series excluded;
  the per-series rights notice is checked)
- the Kenneth French Data Library
- Robert Shiller's online data
- U.S. Treasury yield data
- the Fed's published datasets (e.g., the Gürkaynak-Sack-Wright curve)
- the Open Source Asset Pricing dataset (Chen and Zimmermann)
- BIS statistics where the terms permit

Licensed data (CRSP, Compustat, TAQ, Bloomberg) is **described, never
embedded**. Labs needing it use open substitutes.

Synthetic data is allowed for teaching mechanisms, but must be labelled
**SIMULATED** on the figure itself.

**Design system.**

- Colour tokens on `:root` with a dark-mode override.
- One serif for prose, one sans for UI, one mono for code. All fonts are
  vendored, with no Google Fonts call at runtime.
- 72ch prose measure, theorem/definition/proof callouts, and margin notes for
  citations.
- Print stylesheet, so every module prints as a clean study PDF.
- WCAG 2.2 AA throughout.

**Images.** Every image must teach a mechanism or show data. No stock photos
and no decoration. Diagrams are inline SVG with `<title>` and `<desc>` for
accessibility. Data charts carry a source line and retrieval date on the chart
itself.

---

## 5. Module page template (every page, same order)

1. **Header:** ID, title, prerequisites (linked), target study hours, 4–8
   learning objectives written as measurable verbs (derive, estimate, prove,
   implement, critique).
2. **Why it matters:** at most 150 words, with no motivational filler.
3. **Core content:** numbered sections, with Definition, Theorem, Proof,
   Example and Remark blocks. Every substantive claim carries a grade badge
   and citation key(s).
4. **Figures:** SVG diagrams and data charts with caption, source and
   retrieval date.
5. **Labs:** runnable code, each with a stated hypothesis, the code, the
   expected output (asserted in CI), and an interpretation.
6. **Where the canon breaks:** failed assumptions, failed replications, and
   regime dependence.
7. **Debate brief** (for modules with live controversies): the resolution, the
   strongest case for each side, graded evidence, the current state, and what
   evidence would settle it.
8. **Misconceptions:** each wrong belief, why it is wrong, and the evidence.
9. **Problem set,** in four tiers: Mechanics / Proof / Empirical /
   Research-grade, each with full worked solutions (collapsed).
10. **Key results table:** claim, grade, citation keys.
11. **Reading list:** required primary papers and optional extensions, all as
    registry keys.
12. **Self-check quiz:** 10–20 items, scored locally, with explanations.

---

## 6. Pedagogy

- **Spiral, not silo.** A concept introduced in maths reappears applied. For
  example, PCA (M3) comes back as level/slope/curvature (FI1) and as factor
  extraction (F6). The DAG records every reuse.
- **Derive, then test.** Each theorem comes with a numerical check in a lab.
  For example, put-call parity is checked on simulated paths, and BS Greeks
  against finite differences.
- **Primary sources over textbook paraphrase.** Students read the original
  papers on the reading lists. Pages teach how to read them.
- **Adversarial training.** Every empirical module includes an exercise in
  breaking a published result: costs, subsamples, multiple-testing
  adjustment, or alternative standard errors.

---

## 7. Build process (Claude Code, architect-led)

| Phase | Output | Gate |
|---|---|---|
| **0 — Foundations** | Design system, page template, all `tools/`, vendored runtimes with `LOCK.json`, `curriculum.json` (full DAG), `notation.json`, seed `references.json` (every key in Section 9 resolved through `add_reference.py`) | `verify_refs.py` 100% resolved; `page_smoke.py` passes on the template page |
| **1 — Pilot** | Two modules end-to-end: **S7** (research integrity) and **AP1** (no-arbitrage). They calibrate tone, density and verification cost | Architect review + full ledger pass; template and rules revised once based on the pilot |
| **2 — Fan-out** | Remaining modules, built in DAG order and batched by Part. Each module is written by one builder agent and checked by an independent verifier agent with fresh context | Ledger pass + `check_dag.py` + architect integration review |
| **3 — Integration** | Program map, cross-module links, glossary, bibliography, capstone debates, qualifying exam, thesis rubric | Full-site Playwright run; zero broken links; zero unresolved keys |
| **4 — Freshness pass** | 2025–2026 literature update for every debate brief and working paper | Verifier ledger rerun on the touched modules |

**Agent topology per module:** a builder (BUILDER_RULES) produces the page and
lab tests; a verifier (VERIFIER_RULES, separate context, never the same
agent) produces the ledger; the architect reviews diffs and merges. A verifier
failure goes back to the builder with the failing ledger rows only.

---

## 8. Seed canon notes

The citations in Section 9 are the seed list for the registry. Each one enters
`references.json` only through `add_reference.py` (DOI → Crossref metadata),
so the bibliographic fields are machine-sourced, not recalled.

Entries marked **[WP]** may have been published since. Entries marked **[V]**
are flagged for priority verification of venue, year and exact title. A key
that fails verification is removed or replaced before any module cites it.

Abbreviations:

- *JF* Journal of Finance
- *JFE* Journal of Financial Economics
- *RFS* Review of Financial Studies
- *AER* American Economic Review
- *QJE* Quarterly Journal of Economics
- *JPE* Journal of Political Economy
- *ECMA* Econometrica
- *REStud* Review of Economic Studies
- *REStat* Review of Economics and Statistics
- *JME* Journal of Monetary Economics
- *JET* Journal of Economic Theory
- *JPM* Journal of Portfolio Management
- *FAJ* Financial Analysts Journal
- *CFR* Critical Finance Review

---

## 9. Curriculum: 17 Parts, 92 modules

Notation used below:

- Each module line reads: ID · title · prerequisites · core content · anchor sources · signature lab.
- `→` means "requires".
- Target hours are design targets for study time, not claims.

### PART 0 — Orientation
- **P0.1 · How to Study This Program** · none · Evidence grades; how to read a
  paper (identification, data, inference, robustness); steelmanning; notation
  conventions; using the labs. · Lab: navigate the DAG; first Pyodide cell.

### PART I — Mathematical Foundations (M)
- **M1 · Proof, Logic & Real Analysis** · P0.1 · Sets, quantifiers, proof
  techniques, sequences, limits, continuity, completeness, compactness, metric
  spaces. · Abbott, *Understanding Analysis*; Rudin, *Principles of
  Mathematical Analysis*. · Lab: ε–δ visualizer.
- **M2 · Single & Multivariable Calculus** · M1 · Taylor's theorem, Riemann
  integration, gradients, Jacobians, Hessians, implicit-function and envelope
  theorems. · Lab: Taylor expansion of bond price (duration and convexity
  preview).
- **M3 · Linear Algebra** · M1 · Vector spaces, eigendecomposition, spectral
  theorem, SVD, PSD matrices, projections, least-squares geometry, PCA. ·
  Axler, *Linear Algebra Done Right*; Strang. · Lab: PCA of the Treasury curve
  (embedded FRED data).
- **M4 · Probability I** · M2 · Distributions, expectation, MGF and
  characteristic functions, the multivariate normal, conditioning, LLN, CLT,
  heavy tails. · Lab: CLT failure under infinite variance.
- **M5 · Measure-Theoretic Probability** · M1, M4 · σ-algebras, Lebesgue
  integral, MCT and DCT, Radon–Nikodym, conditional expectation as projection,
  filtrations, discrete martingales, optional stopping. · Williams,
  *Probability with Martingales* (1991); Billingsley. · Lab: martingale
  betting-system simulator.
- **M6 · Optimization** · M2, M3 · Convexity, Lagrange multipliers, KKT,
  duality, QP, dynamic programming and Bellman equations. · Boyd &
  Vandenberghe (2004); Stokey & Lucas (1989). · Lab: efficient-frontier QP
  solver.
- **M7 · Numerical Methods & Scientific Computing** · M2, M3, M4 · IEEE 754,
  conditioning, root finding, linear solvers, interpolation, quadrature, finite
  differences, RNG, Monte Carlo variance reduction. · Glasserman, *Monte Carlo
  Methods in Financial Engineering* (2003). · Lab: catastrophic-cancellation
  demo; antithetic and control variates.

### PART II — Statistics & Econometrics (S)
- **S1 · Statistical Inference** · M4 · Estimators, MLE asymptotics,
  Cramér–Rao, tests, power, confidence intervals, Bayesian inference,
  bootstrap. · Casella & Berger; Efron (1979, *Annals of Statistics*). · Lab:
  bootstrap vs. asymptotic CI.
- **S2 · Linear Regression** · S1, M3 · OLS geometry, Gauss–Markov,
  asymptotics, White (1980, *ECMA*), Newey–West (1987, *ECMA*), clustering
  (Petersen 2009, *RFS*), Stambaugh bias (Stambaugh 1999, *JFE*). · Lab:
  Stambaugh-bias Monte Carlo.
- **S3 · Time Series** · S2 · Stationarity, ARMA, Wold, unit roots
  (Dickey–Fuller 1979, *JASA*), spurious regression (Granger–Newbold 1974,
  *J. Econometrics*), cointegration (Engle–Granger 1987; Johansen 1991,
  *ECMA*), VARs (Sims 1980, *ECMA*), Kalman filter, Markov switching (Hamilton
  1989, *ECMA*). · Hamilton, *Time Series Analysis* (1994). · Lab: spurious
  regression generator.
- **S4 · Volatility Econometrics** · S3 · ARCH (Engle 1982, *ECMA*), GARCH
  (Bollerslev 1986, *J. Econometrics*), EGARCH (Nelson 1991, *ECMA*), realized
  volatility (Andersen–Bollerslev–Diebold–Labys 2003, *ECMA*), HAR (Corsi 2009,
  *J. Financial Econometrics*). · Lab: GARCH vs. HAR forecast evaluation.
- **S5 · GMM & Cross-Sectional Econometrics** · S2 · GMM (Hansen 1982,
  *ECMA*), Fama–MacBeth (1973, *JPE*), Shanken (1992, *RFS*),
  Gibbons–Ross–Shanken (1989, *ECMA*), panel methods. · Lab: GRS test on
  Fama–French portfolios.
- **S6 · Causal Inference** · S2 · Potential outcomes, IV, DiD, RDD, event
  studies (MacKinlay 1997, *JEL*), synthetic control (Abadie–Diamond–Hainmueller
  2010, *JASA*). · Angrist & Pischke (2009). · Lab: event study with
  correct-variance abnormal returns.
- **S7 · Research Integrity & Multiple Testing** · S1, S2 · Data snooping
  (Lo–MacKinlay 1990, *RFS*), White (2000, *ECMA*), Hansen SPA (2005, *JBES*),
  Romano–Wolf (2005, *ECMA*), Benjamini–Hochberg (1995, *JRSS-B*),
  Harvey–Liu–Zhu (2016, *RFS*), Harvey (2017, *JF*), deflated Sharpe
  (Bailey–López de Prado 2014, *JPM*), PBO (Bailey–Borwein–López de Prado–Zhu
  2017, *J. Computational Finance*). · Lab: random-strategy overfitting engine
  (in-sample vs. out-of-sample Sharpe).

### PART III — Stochastic Calculus & Continuous Time (SC)
- **SC1 · Stochastic Processes** · M5 · Brownian motion, quadratic variation,
  continuous martingales, the Markov property, stopping times. · Shreve,
  *Stochastic Calculus for Finance II* (2004). · Lab: quadratic-variation
  convergence.
- **SC2 · Itô Calculus & SDEs** · SC1 · Itô integral, Itô's lemma, GBM, OU,
  existence and uniqueness. · Lab: Euler–Maruyama, strong vs. weak convergence.
- **SC3 · Change of Measure** · SC2 · Girsanov, martingale representation,
  risk-neutral measure, change of numeraire (Geman–El Karoui–Rochet 1995, *J.
  Applied Probability*). · Lab: importance sampling via Girsanov.
- **SC4 · PDEs & Feynman–Kac** · SC2, M7 · Kolmogorov equations,
  Feynman–Kac, boundary conditions. · Lab: Crank–Nicolson solver.
- **SC5 · Jumps & Lévy Processes** · SC2 · Poisson and compound Poisson, Merton
  jump-diffusion (Merton 1976, *JFE*), Lévy–Khintchine, Variance Gamma
  (Madan–Carr–Chang 1998). · Cont & Tankov (2004). · Lab: jump-induced smile.
- **SC6 · Stochastic Control** · SC2, M6 · HJB equation, Merton portfolio
  problem (Merton 1969, *REStat*; 1971, *JET*). · Lab: Merton fraction vs.
  simulated utility.

### PART IV — Economic Foundations (E)
- **E1 · Decision Theory Under Risk & Ambiguity** · M6 · vNM expected utility,
  Arrow–Pratt (Pratt 1964, *ECMA*), stochastic dominance, Epstein–Zin (1989,
  *ECMA*), prospect theory (Kahneman–Tversky 1979, *ECMA*), ambiguity (Ellsberg
  1961, *QJE*; Gilboa–Schmeidler 1989). · Lab: certainty equivalents across
  preferences.
- **E2 · Equilibrium & Information** · E1 · Arrow–Debreu, complete markets,
  rational expectations (Muth 1961, *ECMA*), Grossman–Stiglitz (1980, *AER*),
  no-trade theorem (Milgrom–Stokey 1982, *JET*). · Mas-Colell, Whinston & Green
  (1995). · Lab: information-efficiency equilibrium.
- **E3 · Macroeconomics** · E1, M6, S3 · Solow (1956, *QJE*), RBC
  (Kydland–Prescott 1982, *ECMA*), New Keynesian (Clarida–Galí–Gertler 1999,
  *JEL*; Galí 2015; Woodford 2003), HANK (Kaplan–Moll–Violante 2018, *AER*). ·
  Lab: three-equation NK impulse responses.
- **E4 · Monetary Economics & Central Banking** · E3 · Taylor (1993),
  time inconsistency (Kydland–Prescott 1977, *JPE*; Barro–Gordon 1983, *JPE*),
  ZLB, operating frameworks (floor vs. corridor), QE evidence (Gagnon et al.
  2011, *IJCB*; Krishnamurthy–Vissing-Jorgensen 2011, *BPEA*; Bernanke 2020,
  *AER*), shock identification (Romer–Romer 2004, *AER*; Gertler–Karadi 2015,
  *AEJ:Macro*; Nakamura–Steinsson 2018, *QJE*), r* (Holston–Laubach–Williams
  2017, *JIE*), fiscal theory (Cochrane 2023, *The Fiscal Theory of the Price
  Level*), the 2021–23 inflation (Bernanke–Blanchard [WP][V]). · Lab: Taylor
  rule vs. realized policy rate.
- **E5 · International Macro & the Dollar** · E3 · UIP failure (Fama 1984,
  *JME*), CIP deviations (Du–Tepper–Verdelhan 2018, *JF*), the trilemma,
  Dornbusch overshooting (1976, *JPE*), the dominant currency paradigm
  (Gopinath et al. 2020, *AER*), the global financial cycle (Rey 2013, Jackson
  Hole; Miranda-Agrippino–Rey 2020, *REStud*), safe-asset convenience yields
  (Krishnamurthy–Vissing-Jorgensen 2012, *JPE*; Jiang–Krishnamurthy–Lustig
  2021, *JF*). · Obstfeld & Rogoff (1996). · Lab: Fama UIP regression.
- **E6 · Sovereign Debt, Crises & Political Economy** · E4, E5 · r−g dynamics
  (Blanchard 2019, *AER*), sovereign default (Eaton–Gersovitz 1981, *REStud*),
  currency-crisis models (Krugman 1979, *JMCB*; Obstfeld 1996, *EER*), sudden
  stops (Calvo 1998), Reinhart–Rogoff (2009; 2010) and the Herndon–Ash–Pollin
  (2014, *CJE*) replication. · Lab: debt-dynamics simulator.

### PART V — Asset Pricing Theory (AP)
- **AP1 · No-Arbitrage & the SDF** · M5, M6, E1 · Law of one price, FTAP
  (Harrison–Kreps 1979, *JET*; Harrison–Pliska 1981, *SPA*;
  Delbaen–Schachermayer 1994, *Math. Annalen*), state prices, p = E[mx]. ·
  Cochrane, *Asset Pricing* (rev. 2005); Duffie, *Dynamic Asset Pricing Theory*
  (2001). · Lab: arbitrage detection via LP.
- **AP2 · Mean-Variance, CAPM, ICAPM, APT** · AP1, M6 · Markowitz (1952, *JF*),
  Tobin (1958, *REStud*), Sharpe (1964, *JF*), Lintner (1965, *REStat*), Roll
  critique (1977, *JFE*), ICAPM (Merton 1973, *ECMA*), APT (Ross 1976, *JET*),
  Fama–French (1992, *JF*). · Lab: CAPM security market line on French
  portfolios.
- **AP3 · Consumption-Based Pricing & Puzzles** · AP1 · Lucas (1978, *ECMA*),
  Breeden (1979, *JFE*), Hansen–Singleton, the equity-premium puzzle
  (Mehra–Prescott 1985, *JME*), the risk-free-rate puzzle (Weil 1989, *JME*),
  HJ bounds (Hansen–Jagannathan 1991, *JPE*). · Lab: HJ bound vs. consumption
  data.
- **AP4 · Resolving the Puzzles** · AP3, E1 · Habit (Campbell–Cochrane 1999,
  *JPE*), long-run risk (Bansal–Yaron 2004, *JF*), disasters (Rietz 1988,
  *JME*; Barro 2006, *QJE*; Wachter 2013, *JF*), heterogeneous agents
  (Constantinides–Duffie 1996, *JPE*), Beeler–Campbell (2012, *CFR*). · Debate:
  which model survives the data. · Lab: simulate each model's moments.
- **AP5 · Present Value & Return Predictability** · AP1, S2 · Shiller (1981,
  *AER*), Campbell–Shiller (1988, *RFS*), Fama–French (1988, *JFE*),
  Welch–Goyal (2008, *RFS*) vs. Campbell–Thompson (2008, *RFS*), Cochrane
  (2008, *RFS*; 2011, *JF*). · Lab: CAPE regressions with Stambaugh-corrected
  inference (Shiller data).
- **AP6 · Intermediary & Institutional Asset Pricing** · AP1, AP5 · Limits to
  arbitrage (Shleifer–Vishny 1997, *JF*), He–Krishnamurthy (2013, *AER*),
  Adrian–Etula–Muir (2014, *JF*), He–Kelly–Manela (2017, *JFE*), slow-moving
  capital (Duffie 2010, *JF*), demand systems (Koijen–Yogo 2019, *JPE*), the
  inelastic-markets hypothesis (Gabaix–Koijen [WP][V]). · Lab:
  intermediary-factor pricing test.
- **AP7 · Behavioral Finance** · AP5, E1 · Noise traders (De Long et al. 1990,
  *JPE*), overreaction (De Bondt–Thaler 1985, *JF*), BSV (1998, *JFE*), DHS
  (1998, *JF*), Hong–Stein (1999, *JF*), sentiment (Baker–Wurgler 2006, *JF*),
  survey expectations (Greenwood–Shleifer 2014, *RFS*), diagnostic expectations
  (Bordalo–Gennaioli–La Porta–Shleifer 2019, *JF*). · Debate: risk vs.
  mispricing.
- **AP8 · Market Efficiency: The Full Debate** · AP5–AP7 · Fama (1970, *JF*;
  1991, *JF*), Grossman–Stiglitz, luck vs. skill (Fama–French 2010, *JF*),
  Berk–Green (2004, *JPE*), Berk–van Binsbergen (2015, *JFE*). · Lab:
  bootstrap luck-vs-skill test.

### PART VI — Empirical Asset Pricing & Factors (F)
- **F1 · Data & Methodology** · S5, AP2 · CRSP/Compustat structure (described),
  point-in-time discipline, survivorship and delisting bias (Shumway 1997,
  *JF*), portfolio sorts. · Lab: sorts on Ken French data; delisting-bias demo
  (SIMULATED).
- **F2 · The Classic Factors** · F1 · Size (Banz 1981, *JFE*), value (FF 1992,
  1993), momentum (Jegadeesh–Titman 1993, *JF*; Carhart 1997, *JF*),
  profitability and investment (Novy-Marx 2013, *JFE*; FF 2015, *JFE*;
  Hou–Xue–Zhang 2015, *RFS*), low risk (Frazzini–Pedersen 2014, *JFE*;
  Ang–Hodrick–Xing–Zhang 2006, *JF*), quality (Asness–Frazzini–Pedersen 2019,
  *RAS*). · Lab: factor statistics and spanning regressions.
- **F3 · Factors Across Asset Classes** · F2 · Value and momentum everywhere
  (Asness–Moskowitz–Pedersen 2013, *JF*), carry (Koijen–Moskowitz–Pedersen–Vrugt
  2018, *JFE*), time-series momentum (Moskowitz–Ooi–Pedersen 2012, *JFE*), a
  century of trend (Hurst–Ooi–Pedersen 2017, *JPM*), the challenge from
  Huang–Li–Wang–Zhou (2020, *JFE*). · Debate: is TSMOM real?
- **F4 · Crashes, Crowding & Decay** · F3 · Momentum crashes (Daniel–Moskowitz
  2016, *JFE*), the August 2007 quant quake (Khandani–Lo 2011, *J. Financial
  Markets*), post-publication decay (McLean–Pontiff 2016, *JF*), value's
  2018–2020 drawdown. · Lab: crash-conditional momentum.
- **F5 · The Factor Zoo & Replication** · F2, S7 · Harvey–Liu–Zhu (2016),
  Hou–Xue–Zhang (2020, *RFS*), Jensen–Kelly–Pedersen (2023, *JF*),
  Chen–Zimmermann (2022, *CFR*), Feng–Giglio–Xiu (2020, *JF*). · Debate: is
  there a replication crisis? · Lab: multiple-testing haircut on the open
  anomaly set.
- **F6 · Machine Learning in Asset Pricing** · F5, QR4 · Gu–Kelly–Xiu (2020,
  *RFS*), IPCA (Kelly–Pruitt–Su 2019, *JFE*), Chen–Pelger–Zhu (2024, *Mgmt
  Sci*), virtue of complexity (Kelly–Malamud–Zhou 2024, *JF*) vs. its critiques
  (Nagel [WP][V]), Kelly–Xiu (2023, *Foundations & Trends*). · Lab: ridge vs.
  OLS out-of-sample R².
- **F7 · Performance Evaluation & Skill** · F2, S3 · Jensen (1968, *JF*),
  Sharpe-ratio statistics (Lo 2002, *FAJ*), return smoothing
  (Getmansky–Lo–Makarov 2004, *JFE*), trend followers as lookback straddles
  (Fung–Hsieh 2001, *RFS*). · Lab: Sharpe CI under autocorrelation.

### PART VII — Fixed Income & Rates (FI)
- **FI1 · Bond Math & Curve Construction** · M2, M3 · Duration, convexity,
  bootstrapping, Nelson–Siegel (1987, *J. Business*), Svensson (1994, NBER WP),
  the GSW curve (Gürkaynak–Sack–Wright 2007, *JME*). · Lab: fit NS and
  Svensson.
- **FI2 · Term-Structure Models** · FI1, SC3 · Vasicek (1977, *JFE*), CIR
  (1985, *ECMA*), affine models (Duffie–Kan 1996, *Math. Finance*;
  Dai–Singleton 2000, *JF*), HJM (1992, *ECMA*), LMM (Brace–Gatarek–Musiela
  1997). · Lab: Vasicek closed form vs. Monte Carlo.
- **FI3 · Bond Risk Premia** · FI1, S3 · Fama–Bliss (1987, *AER*),
  Campbell–Shiller (1991, *REStud*), Cochrane–Piazzesi (2005, *AER*), the ACM
  term premium (Adrian–Crump–Moench 2013, *JFE*), Bauer–Hamilton (2018, *RFS*).
  · Debate: are bond returns predictable? · Lab: CP factor replication on GSW
  data.
- **FI4 · Money Markets & Plumbing** · FI1, E4 · Repo, SOFR, reserves, Fed
  balance sheet, the Treasury basis trade, dealer balance-sheet limits, the
  March 2020 dash for cash (He–Nagel–Song 2022, *JFE*), the SLR. · Lab: basis
  P&L with haircut and margin.
- **FI5 · Inflation-Linked Markets** · FI3 · TIPS, breakevens, liquidity
  premium (D'Amico–Kim–Wei 2018, *JFQA*), the TIPS–Treasury puzzle
  (Fleckenstein–Longstaff–Lustig 2014, *JF*). · Lab: breakeven decomposition.
- **FI6 · Interest-Rate Derivatives** · FI2, DV1 · Swaps, caps, swaptions,
  Black-76 (Black 1976, *JFE*), the Bachelier model, SABR (Hagan et al. 2002,
  *Wilmott*), multi-curve, the LIBOR→SOFR transition. · Lab: swaption under
  normal vs. lognormal models.

### PART VIII — Derivatives & Volatility (DV)
- **DV1 · Arbitrage Pricing of Derivatives** · AP1, SC3 · Put–call parity
  (Stoll 1969, *JF*), binomial (Cox–Ross–Rubinstein 1979, *JFE*), BSM (Black–Scholes 1973,
  *JPE*; Merton 1973, *Bell J.*), Greeks, discrete-hedging error. · Lab:
  delta-hedging simulator with costs.
- **DV2 · The Volatility Surface** · DV1 · Smile and skew, static-arbitrage
  conditions, SVI (Gatheral–Jacquier 2014, *Quant. Finance*), local vol (Dupire
  1994, *Risk*), risk-neutral densities (Breeden–Litzenberger 1978,
  *J. Business*). · Gatheral, *The Volatility Surface* (2006). · Lab: RND
  extraction.
- **DV3 · Stochastic & Rough Volatility** · DV2, SC5 · Heston (1993, *RFS*),
  SABR, rough volatility (Gatheral–Jaisson–Rosenbaum 2018, *Quant. Finance*;
  Bayer–Friz–Gatheral 2016, *Quant. Finance*). · Debate: is volatility rough?
  · Lab: Heston via characteristic function.
- **DV4 · Numerical Pricing (C++ module)** · DV1, M7, SC4 · Trees, finite
  differences, Monte Carlo (Boyle 1977, *JFE*), Longstaff–Schwartz (2001,
  *RFS*), Fourier (Carr–Madan 1999, *J. Comp. Finance*; Fang–Oosterlee 2008,
  *SIAM J. Sci. Comput.*), AAD (Giles–Glasserman 2006, *Risk*). · Lab: the same
  American option priced four ways (C++→WASM and Python).
- **DV5 · Variance Risk Premium & Vol Trading** · DV2, F2 · Variance swaps
  (Demeterfi–Derman–Kamal–Zou 1999, Goldman Sachs QS note), Cboe VIX
  methodology, VRP (Carr–Wu 2009, *RFS*; Bollerslev–Tauchen–Zhou 2009, *RFS*),
  option returns (Coval–Shumway 2001, *JF*), the February 2018 Volmageddon
  case, tail-hedging cost (Israelov [V]). · Debate: is short vol a free lunch?
- **DV6 · Exotics, Structured Products & Dealer Hedging** · DV3 · Barriers,
  Asians, autocallables, pinning (Ni–Pearson–Poteshman 2005, *JFE*), hedging
  demand and intraday momentum (Baltussen–Da–Lammers–Martens 2021, *JFE*). ·
  Lab: dealer gamma-exposure simulator (SIMULATED).

### PART IX — Credit & Corporate Finance (CR)
- **CR1 · Corporate Finance Essentials** · AP1 · Modigliani–Miller (1958,
  *AER*), agency (Jensen–Meckling 1976, *JFE*), pecking order (Myers–Majluf
  1984, *JFE*), payout and leverage dynamics. · Lab: MM with taxes and distress
  costs.
- **CR2 · Structural & Reduced-Form Credit** · CR1, SC3 · Merton (1974, *JF*),
  Black–Cox (1976, *JF*), Leland (1994, *JF*), Jarrow–Turnbull (1995, *JF*),
  Duffie–Singleton (1999, *RFS*), distance to default (Bharath–Shumway 2008,
  *RFS*), the credit-spread puzzle (Collin-Dufresne–Goldstein–Martin 2001, *JF*;
  Huang–Huang 2012, *RAPS*). · Lab: Merton model on a stylized firm.
- **CR3 · Credit Derivatives & Correlation** · CR2 · CDS mechanics, the
  CDS–bond basis, Gaussian copula (Li 2000, *J. Fixed Income*), CDO tranches
  and the 2008 failure. · Lab: tranche loss under correlation shifts.
- **CR4 · Credit Cycles** · CR2, E3 · Excess bond premium (Gilchrist–Zakrajšek
  2012, *AER*), credit sentiment (López-Salido–Stein–Zakrajšek 2017, *QJE*),
  private credit. · Lab: EBP as a recession predictor.

### PART X — FX, Commodities & Digital Assets (X)
- **X1 · FX Markets & Parity Conditions** · E5 · FX microstructure,
  UIP and CIP, PPP (Rogoff 1996, *JEL*), Meese–Rogoff (1983, *JIE*). · Lab:
  random walk vs. models out of sample.
- **X2 · Currency Risk Premia** · X1, F3 · Carry (Lustig–Roussanov–Verdelhan
  2011, *RFS*; Menkhoff–Sarno–Schmeling–Schrimpf 2012, *JF*), crash risk
  (Brunnermeier–Nagel–Pedersen 2008, *NBER Macro Annual*), FX momentum (MSSS
  2012, *JFE*), currency value (MSSS 2017, *RFS*), the dollar factor
  (Verdelhan 2018, *JF*), the peso problem (Burnside et al. 2011, *RFS*). ·
  Lab: carry-crash simulator.
- **X3 · Commodities** · AP1, F3 · The theory of storage (Kaldor 1939; Working
  1949; Brennan 1958, *AER*), hedging pressure (de Roon–Nijman–Veld 2000,
  *JF*), Gorton–Rouwenhorst (2006, *FAJ*), Erb–Harvey (2006, *FAJ*),
  financialization (Tang–Xiong 2012, *FAJ*), oil-shock decomposition (Kilian
  2009, *AER*), negative WTI in April 2020. · Lab: roll yield vs. spot return.
- **X4 · Digital Assets as a Macro Asset** · X1, F2 · Liu–Tsyvinski (2021,
  *RFS*), Liu–Tsyvinski–Wu (2022, *JF*), stablecoins and T-bill demand (grade
  B/C). · Lab: crypto factor exposures.

### PART XI — Global Macro Trading (GM)
- **GM1 · Macro Data & Nowcasting** · S3, E3 · Real-time vintages
  (Croushore–Stark 2001, *J. Econometrics*; ALFRED), dynamic factor models
  (Stock–Watson 2002, *JASA*), nowcasting (Giannone–Reichlin–Small 2008, *JME*).
  · Lab: revised-data lookahead bias in a backtest.
- **GM2 · Regimes & the Business Cycle** · GM1, S3 · Yield-curve recession
  signal (Estrella–Hardouvelis 1991, *JF*; Estrella–Mishkin 1998, *REStat*),
  Markov switching, stock–bond correlation regimes
  (Campbell–Sunderam–Viceira 2017, *CFR*; Campbell–Pflueger–Viceira 2020, *JPE*),
  inflation-regime evidence (Neville et al. [WP][V]). · Lab: stock–bond
  correlation sign flip.
- **GM3 · Trading Monetary Policy** · E4, S6 · Pre-FOMC drift (Lucca–Moench
  2015, *JF*), Fed information effects (Nakamura–Steinsson 2018), policy
  divergence and FX. · Lab: FOMC event study.
- **GM4 · Macro Strategy Construction** · GM2, FI3, X2, DV2 · Expressing a
  view (curve trades, relative value, options vs. delta-one), carry and
  roll-down, sizing, risk-reward asymmetry. · Lab: trade-expression comparator.
- **GM5 · Crises as Mechanisms** · GM4, SR1 · 1992 ERM, 1997 Asia, 1998
  LTCM/Russia, 2008, 2010–12 euro crisis, 2013 taper tantrum, 2015 CHF de-peg,
  March 2020, 2022 gilts/LDI, 2023 SVB, 2024 yen-carry unwind. Each episode is
  taught as a causal mechanism and cited to primary official or academic
  sources ([V] for each). · Lab: LDI collateral-spiral simulator.

### PART XII — Portfolio Construction & Risk (PR)
- **PR1 · Mean-Variance in Practice** · AP2, S1 · Estimation error (Michaud
  1989, *FAJ*; Chopra–Ziemba 1993, *JPM*), 1/N (DeMiguel–Garlappi–Uppal 2009,
  *RFS*), shrinkage (Ledoit–Wolf 2004, *J. Multivariate Analysis*; 2017, *RFS*),
  Black–Litterman (1992, *FAJ*). · Lab: optimizer instability.
- **PR2 · Risk Parity, Vol-Targeting & Leverage** · PR1 · Risk parity
  (Asness–Frazzini–Pedersen 2012, *FAJ*), vol-managed portfolios
  (Moreira–Muir 2017, *JF*) vs. Cederburg et al. (2020, *JFE*), vol targeting
  (Harvey et al. 2018, *JPM*). · Debate: are vol-managed portfolios a free
  lunch?
- **PR3 · Growth-Optimal Sizing** · PR1, SC6 · Kelly (1956, *Bell System
  Tech. J.*), Breiman (1961), fractional Kelly under parameter uncertainty
  (MacLean–Thorp–Ziemba 2011), Samuelson's critique (1979, *J. Banking &
  Finance*). · Lab: Kelly under estimation error.
- **PR4 · Risk Measurement** · PR1, S4 · VaR and ES, coherence (Artzner et al.
  1999, *Math. Finance*), VaR backtests (Kupiec 1995; Christoffersen 1998,
  *IER*), EVT (McNeil–Frey 2000, *J. Empirical Finance*), copulas, stress
  testing, FRTB. · McNeil–Frey–Embrechts (2015). · Lab: VaR backtest.
- **PR5 · Drawdowns & Capital Allocation** · PR3 · Maximum drawdown of
  Brownian motion (Magdon-Ismail et al. 2004, *J. Applied Probability*),
  drawdown constraints (Grossman–Zhou 1993, *Math. Finance*), risk of ruin,
  multi-strategy allocation. · Lab: drawdown distribution vs. Sharpe.
- **PR6 · Dynamic & Long-Horizon Allocation** · SC6, PR1 · Hedging demands,
  Campbell–Viceira (2002), LDI, the time-diversification fallacy. · Lab:
  horizon effects under mean reversion.

### PART XIII — Market Microstructure & Execution (MS)
- **MS1 · Microstructure Theory** · E2, S1 · Roll (1984, *JF*), Kyle (1985,
  *ECMA*), Glosten–Milgrom (1985, *JFE*), inventory (Ho–Stoll 1981, *JFE*), PIN
  (Easley et al. 1996, *JF*), the VPIN dispute (Easley–López de Prado–O'Hara
  2012, *RFS*, vs. Andersen–Bondarenko 2014, *J. Financial Markets*). · Lab:
  Kyle equilibrium.
- **MS2 · Limit Order Books & Market Structure** · MS1 · LOB dynamics
  (Cont–Stoikov–Talreja 2010, *Operations Research*), Reg NMS, dark pools, HFT
  (Brogaard–Hendershott–Riordan 2014, *RFS*), the 2010 Flash Crash (Kirilenko
  et al. 2017, *JF*), batch auctions (Budish–Cramton–Shim 2015, *QJE*). · Lab:
  queue-position simulator.
- **MS3 · Market Impact & Optimal Execution** · MS1, SC6 · The square-root law
  (Almgren et al. 2005, *Risk*; Tóth et al. 2011, *Phys. Rev. X*),
  Almgren–Chriss (2001, *J. Risk*), Obizhaeva–Wang (2013, *J. Financial
  Markets*). · Bouchaud et al., *Trades, Quotes and Prices* (2018). · Lab:
  Almgren–Chriss efficient frontier.
- **MS4 · Costs, Capacity & Implementation Shortfall** · MS3, F2 · Perold
  (1988, *JPM*), Novy-Marx–Velikov (2016, *RFS*), Patton–Weller (2020, *JFE*),
  Frazzini–Israel–Moskowitz [WP][V]. · Lab: anomaly returns net of cost.

### PART XIV — Quantitative Research Engineering (QR)
- **QR1 · The Quant Technology Stack** · P0.1 · Section 3 taught with
  evidence; testing; reproducibility; numerical determinism; reading
  literacy for q and R. · Lab: property-based tests for a pricing function.
- **QR2 · Research Data Engineering** · F1 · Point-in-time databases,
  corporate actions, tick data, timestamps and time zones, alternative data. ·
  Lab: DuckDB `ASOF JOIN` point-in-time merge.
- **QR3 · Backtesting Architecture** · QR2, S7 · Vectorized vs. event-driven
  backtests, signal-to-execution lags, cost models, walk-forward testing,
  purged/embargoed and combinatorial CV (López de Prado 2018, *Advances in
  Financial Machine Learning*). · Lab: lookahead-bias detector.
- **QR4 · Statistical Learning for Finance** · S1, M6 · Bias–variance, lasso
  (Tibshirani 1996, *JRSS-B*), boosting (Friedman 2001, *Annals of
  Statistics*), random forests (Breiman 2001, *Machine Learning*), neural nets,
  low signal-to-noise and non-stationarity, SHAP (Lundberg–Lee 2017, NeurIPS).
  · Hastie–Tibshirani–Friedman, *ESL*. · Lab: overfit vs. regularized learner.
- **QR5 · Text, Sequence Models & LLMs** · QR4 · Text as data
  (Gentzkow–Kelly–Taddy 2019, *JEL*), Loughran–McDonald (2011, *JF*),
  transformers (Vaswani et al. 2017, NeurIPS), LLM return-prediction claims
  (Lopez-Lira–Tang [WP]) vs. lookahead and contamination critiques
  (Glasserman–Lin [WP][V]). · Lab: dictionary sentiment with a contamination
  test.
- **QR6 · RL & Optimal Control in Trading** · QR4, SC6 · MDPs, Q-learning, RL
  for execution (Nevmyvaka–Feng–Kearns 2006, ICML), deep hedging
  (Buehler–Gonon–Teichmann–Wood 2019, *Quant. Finance*), failure modes under
  non-stationarity. · Lab: tabular RL execution vs. Almgren–Chriss.
- **QR7 · High-Performance Computing (C++ module)** · M7, DV4 · Memory layout,
  vectorization, templates, parallelism, GPUs, latency engineering basics. ·
  Lab: Monte Carlo in C++→WASM vs. NumPy.

### PART XV — Systemic Risk & Financial Stability (SR)
- **SR1 · Runs, Liquidity & Fire Sales** · AP6 · Diamond–Dybvig (1983, *JPE*),
  liquidity spirals (Brunnermeier–Pedersen 2009, *RFS*), fire sales
  (Shleifer–Vishny 2011, *JEP*), the run on repo (Gorton–Metrick 2012, *JFE*).
  · Lab: margin-spiral simulator.
- **SR2 · Leverage Cycles** · SR1 · Geanakoplos (2010, *NBER Macro Annual*),
  Adrian–Shin (2010, *JFI*), Brunnermeier–Sannikov (2014, *AER*). · Lab:
  procyclical-leverage simulation.
- **SR3 · Measuring Systemic Risk** · SR2, PR4 · CoVaR (Adrian–Brunnermeier
  2016, *AER*), SRISK (Brownlees–Engle 2017, *RFS*), MES (Acharya et al. 2017,
  *RFS*), network contagion (Acemoglu–Ozdaglar–Tahbaz-Salehi 2015, *AER*). ·
  Lab: CoVaR estimation.
- **SR4 · Regulation's Market Footprint** · SR3, FI4 · Basel III, SLR,
  Volcker, central clearing, dealer constraints and Treasury-market liquidity,
  post-2020 market reform. · Lab: balance-sheet cost of intermediation.

### PART XVI — Capstone (CAP)
- **CAP1 · Reading, Refereeing & Replicating** · F5, S7 · Referee-report
  craft; full replication of one published result from embedded open data.
- **CAP2 · The Great Debates** · all Parts · Twelve resolutions, each with a
  steelman for both sides, graded evidence and a "what would settle it"
  section:
  1. Markets are efficient.
  2. The equity premium is a risk premium.
  3. Value is dead.
  4. Most published factors are false discoveries.
  5. QE works mainly through portfolio balance.
  6. UIP failure is a risk premium.
  7. Complexity helps return prediction.
  8. Trend-following's edge survived 2009.
  9. Vol-managed portfolios beat their unmanaged counterparts after costs.
  10. r* has fallen permanently.
  11. The fiscal theory of the price level explains 2021–23.
  12. HFT improves market quality.
- **CAP3 · Qualifying Examination** · all · Timed written exams in asset
  pricing, econometrics and macro/monetary, modeled on PhD prelims, with full
  solutions.
- **CAP4 · Research Thesis & Defense** · CAP1 · An original extension of a
  replicated result, a full research pipeline, a written paper, and an
  oral-defense rubric.

**Parts and modules:**

| Part | Modules |
|---|---|
| 0 | 1 |
| I | 7 |
| II | 7 |
| III | 6 |
| IV | 6 |
| V | 8 |
| VI | 7 |
| VII | 6 |
| VIII | 6 |
| IX | 4 |
| X | 4 |
| XI | 5 |
| XII | 6 |
| XIII | 4 |
| XIV | 7 |
| XV | 4 |
| XVI | 4 |
| **Total** | **92** |

---

## 10. Definition of done (whole program)

- [ ] All 92 module ledgers pass with zero failing rows
- [ ] `verify_refs.py`: 100% of registry keys resolve; zero orphan or uncited keys
- [ ] `run_labs.py`: every lab executes and every expected output matches
- [ ] `check_dag.py`: zero concepts used before being introduced
- [ ] `page_smoke.py`: every page, in light and dark mode, has zero console errors and renders all math
- [ ] Lighthouse accessibility score ≥ 95 on every page; site works fully offline from a local server
- [ ] Every data file in `MANIFEST.json` has source, licence, retrieval date, hash and transform script
- [ ] The architect has read every module in full before release
