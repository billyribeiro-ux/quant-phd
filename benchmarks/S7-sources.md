# Sources log (reached = R, unreachable = U, secondary = S)

## Cornell
- R https://classes.cornell.edu/browse/roster/FA25/class/ORIE/5256 — ORIE 5256 Special Topics in FE V, instructor Lopez De Prado; ML tools; MEng FE NYC; offered 2022FA-2025FA.
- R https://www.quantresearch.org/Lectures.htm — "Academic materials for Cornell University's ORIE 5256 course": Lectures 1-10 incl. 5 Backtesting I, 6 Backtesting II, 10 Seven reasons ML funds fail; seminars 2026 "What is the FDR in finance?", "Sharpe Ratio Inference: a new standard".
- U SSRN lecture PDFs (abstract_id 3257497, 3261943 etc.) — HTTP 403 (curl and WebFetch).
- S https://www.cxoadvisory.com/big-ideas/investment-strategy-development-coursework — secondary summary of the ORIE 5256 slides: Backtesting I (track backtests per dataset; CV "many scenarios" not single walk-forward; bagging to detect overfitting); Backtesting II (drawdown, time under water, turnover, Sharpe corrected for non-normality, short samples, snooping; predicted vs actual; symmetric vs asymmetric payouts; probability strategy fails); 7 reasons (overlap, train/test leakage, reuse w/o snooping adjustment).

## UChicago
- R https://home.uchicago.edu/~amshaikh/webfiles/multiple_topics.pdf — Shaikh "Multiple Testing" notes (PDF created 2009-03; course not named in file; teaching page https://home.uchicago.edu/~amshaikh/teaching.html lists Econometrics Spring 2009, Topics in Econometrics Winter 2009). Covers: p-values super-uniform; finance example 1.2 strategies vs benchmark; strong vs weak FWER; Bonferroni optimal among single-step (disjoint construction); step-down/step-up; Holm proof + Holm cannot be improved (least favourable constructions); generic max-T step-down with monotone critical values (Romano-Wolf 2005); k-FWER single-step kα/s and step-down (Lehmann-Romano constants) with proof; FDP exceedance control Pr{FDP>γ}≤α; FDR, BY; asymptotic p-values.

## Berkeley
- R https://stat210a.berkeley.edu/fall-2025/ — Stat 210A Theoretical Statistics (PhD), Fall 2025: Lecture 25 Bootstrap; Lecture 26 Multiple Testing parts I-II (Dec 2, Dec 4).
- R https://stat210a.berkeley.edu/fall-2025/handwritten/lecture26-multipletesting.pdf — handwritten (text layer recognized): outline 1 multiple testing, 2 FWER control, 3 step-down, 4 simultaneous intervals/deduced inference, 5 FDR, 6 BH; Šidák, Holm, closure principle, Scheffé, simultaneous CIs for regression coefficients by simulation (max-|t| quantile), BH empirical-Bayes interpretation, Storey-Taylor-Siegmund martingale proof, FDR under general dependence (log m correction).

## CMU
- R https://www.stat.cmu.edu/~siva/teaching/705/lec23.pdf — 36-705 Intermediate Statistics (Fall 2019, Balakrishnan) lecture 23: permutation two-sample test; FWER; Šidák; Bonferroni; Holm; "what error rate should we control (journal/field)"; FDR definition; BH next.

## Stanford
- R https://bulletin.stanford.edu/courses/1254781 — STATS 300C Theory of Statistics III: global testing in high dimensions (Bonferroni, Fisher, chi-square, higher criticism; sparse vs dense), FWER, FDR, BH, knockoffs, e-values and anytime-valid inference, false coverage rate, post-selection inference, conformal, permutation testing, James-Stein, empirical Bayes.
- R https://22-23.bulletin.stanford.edu/courses/2152461 — MS&E 448 Big Financial Data & Algorithmic Trading (2022-23): project course; models must be justified "beyond pure econometric and data mining approaches"; no explicit multiple-testing content.
- U explorecourses.stanford.edu (JS/login wall).

## Columbia
- R https://doc.sis.columbia.edu/subj/IEOR/_Fall2026.html , _Spring2026.html, _Fall2025.html — titles only: E4709 Statistical Analysis & Time Series, E4576 Data-driven Methods in Finance, E4723 AI Investment Mgmt, E4721 Computational Portfolio Construction, E4733 Algorithmic Trading, E4630 Asset Allocation, E4737 AI Applications in Finance. No descriptions/syllabi.
- U https://ieor.columbia.edu/content/algorithmic-trading (403 curl + WebFetch); U https://courses.business.columbia.edu/B9156 (403 curl + WebFetch; search snippet says Python backtesting course, "No Syllabus"); U bulletin.engineering.columbia.edu course search (JS; returns home page); U doc.sis E4733-20261-001 ("Section removed").

## Princeton
- U https://fan.princeton.edu/fan/classes/524.html , /525.html , /teaching.html — Cloudflare 403 (curl and WebFetch). Search snippet only: ORF 524 Statistical Theory and Methods (Fan).
- U https://www.columbia.edu/~skk2175/courses.html (Cloudflare 403).

## MIT
- R https://ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/pages/syllabus/ , /lecture-notes/ , /readings/ — 15.450 Analytics of Finance (Kogan, F2010): L9 small-sample inference and bootstrap (CLM 7.2, Efron-Tibshirani, Davison-Hinkley ch2, Stambaugh 1999); no multiple-testing lecture.
- R https://ocw.mit.edu/courses/14-382-econometrics-spring-2017/pages/lecture-notes/ — 14.382 Econometrics (Chernozhukov, S2017): L1 Least squares, partialling-out, simultaneous inference; L5 bootstrapping; L11 high-dim sparse inference.
- R https://ocw.mit.edu/courses/14-382-econometrics-spring-2017/c62d33e015c910b0d126bcc9344cf2c5_MIT14_382S17_lec1.pdf — Theorem 3 joint confidence band: c = (1-α) quantile of ||N(0,C)||∞ (sup-t band), simulated; Pennsylvania re-employment experiment: simultaneous c=2.27 vs pointwise 1.65 vs Bonferroni 2.33; only 1 of 3 pointwise-significant effects survives.
- R https://ocw.mit.edu/courses/14-384-time-series-analysis-fall-2013/pages/lecture-notes/ — 14.384 Time Series (Mikusheva, F2013): L2-3 HAC, L9 bootstrap, L19 breaks; no multiple testing.
- R https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/pages/lecture-slides/ — topic titles not parsed (table empty in text).
- S (search snippet) MIT 15.458 Financial Data Science and Computing — registrar listing FA18 (stuff.mit.edu) inference, regression, time series in R; no backtesting text.
- R https://www.stat.berkeley.edu/~wfithian/courses/stat212a/syllabus.pdf — Stat 212A Topics in Selective Inference (Fithian, F2015): families/selection/type I error rates; comparing normal means; p-value methods; step-down and closure; FDR and BH; FDR under dependence; false coverage-statement rate (FDR for CIs); empirical Bayes view of FDR; local FDR; post-selection inference in regression and via conditional inference; replicability and meta-analysis. Assessment: 3±1 problem sets 30%, proposal 10%, final project 60% (paper report / new problem / software).

## UChicago (finance)
- R https://finmath.uchicago.edu/curriculum/degree-concentrations/trading/finm-33150/ — FINM 33150 Quantitative Trading Strategies (Boonstra): spread/carry trades, parameter reversion, model prediction/evaluation, market making; regressions; "achieving trustworthy performance"; data from Quandl.
- U syllabus links on Box (https://uchicago.box.com/s/36zjvvwe7a6i2mxhnbw76ca3x6kouab5 , .../8cxj2g2oy7eoqq53pj6n1p3cxfe3c3ye) — Box login wall.
- U https://finmath.uchicago.edu/curriculum/degree-concentrations/trading/finm-35910/ — returned 1-byte body. Search snippet only: "robust back-testing frameworks".
- R https://www.cmu.edu/mscf/academics/curriculum/index.html — MSCF course descriptions: 46921 FDS I (linear/nonparametric models, estimation, uncertainty quantification); 46923 FDS II (data cleaning, viz, dimension reduction, clustering, Bayesian methods, "making discovery claims"); 46926/46927 ML I-II (model validation and assessment); 46929 Financial Time Series (forecasting, trading strategies, cointegration); 46979 Asset Management ("use statistical methods to validate the existence of premiums associated with these factors ... how to back-test these portfolios ... transaction costs, liquidity, taxes"); 46982 Microstructure (real intraday data, Kdb+); 46983 ML capstone with a financial firm.

## NYU
- R https://math-finance.cims.nyu.edu/academics/ — Courant MS Math Finance course descriptions: MATH-GA 2708 Algorithmic Trading & Quantitative Strategies ("simulation techniques, back-testing strategies, and performance measurement ... model risk mitigation"); MATH-GA 2707 Time Series & Stat Arb ("practical issues in simulation techniques", transaction costs); ML & Computational Statistics (hypothesis testing, model selection, cross-validation); MATH-GA 2047 Trends in Financial Data Science (alt data, ML). No explicit multiple-testing text.
- R https://engineering.nyu.edu/sites/default/files/2021-02/FRE-GY%207121%20Statistical%20Arbitrage.pdf — NYU Tandon FRE-GY 7121 Statistical Arbitrage (Totouom-Tangho): "proper backtesting ... data mining"; programme item "Backtesting. Data mining. Applications of machine learning. Data error detection. Survivorship bias."; "Deploying and monitoring. Style drift"; "monitor for excess deviations from expected performance"; grading 30% HW, 60% final project.
- U https://math.nyu.edu/dynamic/graduate/ms-mathematics-finance/course-descriptions/ (404).
- R http://pages.stern.nyu.edu/~sternfin/PhD/RichmondSyllabus.pdf (linked from https://www.stern.nyu.edu/experience-stern/about/departments-centers-initiatives/academic-departments/finance/academic-programs/phd-overview/current-phd-course-offerings) — Stern PhD Financial Theory V Empirical AP (Richmond, Spring 2019): one-page topic list incl. "Cross-section and the factor zoo", "Mutual Funds and Hedge Funds"; requirements problem sets, abstracts, midterm, short paper. No reading list.

## Penn
- R https://www.econ.upenn.edu/sites/default/files/filevault/u4/econ221spring2015.pdf — Econ 221 Econometric Forecasting (Jonathan Wright, Spring 2015, undergrad): "model selection for forecasting", "recursive and related methods for diagnosing and selecting forecasting models", "evaluating a single forecast; comparing forecast accuracy; encompassing and forecast combination", "preliminary series, revised series" (data vintages). Primary text: Diebold open text.
- R https://www.sas.upenn.edu/~fdiebold/Teaching221/Forecasting.pdf — Diebold, Forecasting (619 pp, 2024 build): ch.10 Point forecast evaluation incl. Diebold-Mariano test ("superior or merely lucky"), DM via HAC regression on intercept, conditional DM; ch.12 forecast combination; ch.15 model selection (information criteria, cross validation, stepwise, shrinkage); in-sample overfitting / data mining p.290.

## Harvard
- R https://pll.harvard.edu/course/data-analysis-life-sciences-3-statistical-inference-and-modeling-high-throughput-experiments — Harvard Chan PH525.3x (online): multiple comparison problem, FWER, FDR, Bonferroni, q-values, EDA, hierarchical models and empirical Bayes, R code.
- R https://maxkasy.github.io/home/files/teaching/MicroeconometricMethods/2140part1syllabusspring2018.pdf (Kasy course archive https://maxkasy.github.io/home/teaching/) — Harvard Econ 2140 (Kasy & Tamer, Spring 2018): statistical decision theory; Bayesian estimation; value-added estimation; ridge/lasso; Stigler 1990 Galtonian shrinkage; Stein 1981; bootstrap; subsampling; confidence bands. (scholar.harvard.edu copy U: 403.)
- R https://maxkasy.github.io/home/TopicsInEconometrics2019 — Harvard Ec2148 Topics (fall 2019): "Shrinkage in the normal means model", decision theory, bandits.

## Berkeley MFE
- R https://mfe.haas.berkeley.edu/academics/curriculum — core: 230E Empirical Methods (MLE, GMM, GARCH, non-parametric; volatility/correlation stability; financial databases); 230P Financial Data Science (model selection, trees, bagging, boosting, RF); 230O Applied Finance Project.
- R https://mfe.haas.berkeley.edu/academics/electives — 230ZB Deep Learning for Finance II ("teach students experimental methods to evaluate published models in a critical way"); 230GA Equity Markets (active management: forecasting returns, risk, cost; "how to research active strategies"); 230X High Frequency; 230K Dynamic Asset Mgmt. No explicit multiple-testing text.
- R https://faculty.wharton.upenn.edu/?p=50925 — Wharton FNCE 2450/7450 Hedge Funds (Ronen Israel): strategies "illustrated using real data, and students learn to use 'backtesting' to evaluate a strategy"; performance measurement; students "analyze and manipulate real data".
- U https://apps.wharton.upenn.edu/syllabi/?term=202630&course=FNCE7450401 (401 Unauthorized). U https://backtester.wharton.upenn.edu (connection reset).

## Princeton (finance)
- R https://bcf.princeton.edu/academic-programs/master-in-finance/requirements-core-courses/ — MFin core: FIN 505/ORF 505 Statistical Analysis of Financial Data (heavy tails, copulas, robust regression, ML); FIN 504/ORF 504 Financial Econometrics (predictability, factor pricing, GMM, VAR, ML). No multiple-testing/backtest text.
- U https://orfe.princeton.edu/graduate/courses , https://registrar.princeton.edu/course-offerings (403).

## UChicago Booth
- R https://dachxiu.chicagobooth.edu/ (teaching section) — B34902 Asset Pricing II PhD (Xiu): ML in empirical AP, inference on alphas, "when, where, and why algorithms may fail"; B20800 Big Data: "model choice and false discovery rates", bootstrap, CV, real datasets incl. investment; B41210 Financial Analytics (MiF): actual financial datasets. Page lists Giglio-Liao-Xiu "Thousands of Alpha Tests" (RFS 2021) under research "Multiple Testing".
- R http://dachxiu.chicagobooth.edu/download/SoFiE_2018.pdf , SoFiE_2021.pdf, SoFiE_2024.pdf — SoFiE summer-school schedules (Kelly & Xiu): no multiple-testing lecture found.
- U https://github.com/TaddyLab/MBAcourse (proxy 403).

## Yale
- R https://som.yale.edu/programs/mms-asset-management/curriculum — MAM sample schedule: Quantitative Investing (Fall 1-2), Statistical Foundations, Financial Econometrics, Machine Learning.
- S (search snippet of som.yale.edu sample-courses page, https://som.yale.edu/node/191015 = 403): Quantitative Investing (Moskowitz) "Students will replicate studies and design their own tests of theories and apply them to the data."
- R https://som.yale.edu/sofie-financial-machine-learning-summer-school — SoFiE 2025 at Yale SOM: complexity, benign overfit, ML factor pricing; no multiple-testing item.

## Berkeley (more)
- R https://data102.org/fa25/ — Data 102 (undergrad) Lecture 4 Multiple Hypothesis Testing and FDR control; bandits.

## Cornell (more)
- R https://classes.cornell.edu/browse/roster/SP26/class/ORIE/5640 — ORIE 5640 Statistics for FE (regression, ARIMA, GARCH, factor models, risk measures, copulas, Bayesian; R). No multiple testing.
- R https://ocw.mit.edu/courses/14-382-econometrics-spring-2017/48094f9cc619ec6c5a5b56aa3bdfc360_MIT14_382S17_lec5.pdf — 14.382 L5 Bootstrapping: bootstrap simultaneous confidence rectangle for all components; block bootstrap for dependent data (Künsch-type, block size tied to HAC trimming).
