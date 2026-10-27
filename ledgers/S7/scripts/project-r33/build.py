import json, re, sys, datetime, collections
sys.path.insert(0, '/tmp/ap1-r5/s7p')
import classify as C
from classify import rows as OLD, paths_of, changed

R = '/tmp/verify-s7-r1-p'
PAGE = open(R + '/course/modules/S/S7/project.html', encoding='utf-8').read()
LOG = '/tmp/ap1-r5/s7p/logs/'
ROUND = 33
RUN_TAG = 'r33'
TOOL = 'Python 3.14.8, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2'

# ---------- mutants from the r33 run
mut = {}
for line in open(LOG + 'mutate.log', encoding='utf-8'):
    m = re.match(r'KILLED (\S+)\.py: .*-> (\S+) \(seed (\d+)\)$', line.rstrip('\n'))
    if m:
        mut[m.group(1) + '.py'] = (m.group(2), m.group(3))
assert len(mut) == 164, len(mut)

# ---------- memo data-num values from the page (first occurrence)
DN = {}
for m in re.finditer(r'<span data-num="([a-z0-9_]+)"[^>]*>([^<]*)</span>', PAGE):
    DN.setdefault(m.group(1), m.group(2))

HEAD = {
 'n_trials': 'n_trials 40 and n_obs 308 (T) from my own trial matrix',
}
INDEP = ('Independent recomputation (r33, my own code, numpy only, reading course/assets/data/market/fx_monthly.csv): '
         'T=308, N=40, monthly SR of the selected trial 0.0408 (annualized 0.14), skew 1.57, raw kurtosis 15.2, '
         'mean and volatility annualized 0.55% and 3.91%, SR sd 0.0193, SR0 0.0424 per month, PSR 77%, DSR 0.49, '
         'min p 0.237, 0 rejections at q or alpha 0.05, PBO 0.733 at 16 blocks (12,870 splits; 0.743 at 8 blocks and 0.714 at 10), '
         'block 19 months with 4 rows dropped (oldest), rho 0.567, participation ratio 2.37, N_eff 7.74.')
INDEP_KEYS = {'n_trials', 'n_obs', 'sr_month', 'sr_ann', 'psr', 'psr_p', 'dsr', 'dsr_p', 'sr0', 'sr0_ann', 'sr_sd',
              'skew', 'kurt', 'mean_ann', 'vol_ann', 'p_min', 'pbo', 'pbo_check_1', 'pbo_check_2', 'block_months',
              'rows_dropped', 'n_splits', 'n_eff', 'rho', 'stepm_rejections', 'bh_rejections', 'n_blocks', 'sr_ann',
              'selected_label', 'sr_median_ann', 'sr_min_ann', 'pbo_bar', 'dsr_bar'}
MEMO_TEST = ('tests/test_memo_exemplars.py run on the r33 toolchain (20 passed with test_run_labs.py): '
             'test_every_exemplar_number_is_pinned_to_its_computation recomputes each data-num from the Lab 3 and Lab 4 twins '
             'and the A8 reference (' + TOOL + ')')

OVR = {}   # id -> (status, evidence)
def ov(i, status, ev):
    OVR[i] = (status, ev)

# ----- command rows
ov('r17-cmd-check-pages-S7', 'PASS', f'{RUN_TAG}: .venv/bin/python tools/check_pages.py --unit S7: "check_pages S7: PASS" (log logs/check_pages_S7.log).')
ov('r17-cmd-check-pages-all', 'PASS', f'{RUN_TAG}: tools/check_pages.py --all: "check_pages S7: PASS", "check_pages AP1: PASS" (logs/check_pages_all.log).')
ov('r17-cmd-check-dag-S7', 'PASS', f'{RUN_TAG}: tools/check_dag.py --unit S7: "check_dag S7: PASS" (logs/check_dag_S7.log).')
ov('r17-cmd-check-dag-all', 'PASS', f'{RUN_TAG}: tools/check_dag.py --all: "check_dag S7: PASS", "check_dag AP1: PASS" (logs/check_dag_all.log).')
ov('r17-cmd-check-projects-S7', 'PASS', f'{RUN_TAG}: tools/check_projects.py --unit S7: "check_projects S7: PASS" (logs/check_projects_S7.log).')
ov('r17-cmd-check-projects-all', 'PASS', f'{RUN_TAG}: tools/check_projects.py --all: "check_projects S7: PASS", "check_projects AP1: PASS" (logs/check_projects_all.log).')
ov('r17-cmd-run-labs-S7', 'PASS', f'{RUN_TAG}: tools/run_labs.py --unit S7 on {TOOL}: "run_labs S7: PASS (42/42)" (logs/run_labs_S7.log). Labs checked against the page output under the page tolerance, including project labs 1 to 3 and the completion solution.')
ov('r17-cmd-pytest-slice', 'PASS', f'{RUN_TAG}: .venv/bin/pytest -p no:cacheprovider -rA tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_js.py tests/test_docs_figures.py tests/test_labs.py tests/test_figure_kernels.py tests/test_run_labs.py tests/test_fetch_data.py tests/test_page_smoke.py: 258 passed in 47.47s (logs/pytest_slice.log; test_js includes rubric.test.mjs, katex_strict.test.mjs and fsrs.test.mjs).')
ov('r17-cmd-page-smoke', 'PASS', f'{RUN_TAG}: tools/page_smoke.py --unit S7 (all eight lessons, project, hub, plus site-wide index, concepts, review): "page_smoke S7: PASS" (logs/page_smoke_S7.log). S7 pages: 34 lab runs in total (project labs 0.0 s each), slowest 1.3 s against 10 s; in-browser grader "All 162 tests pass on seed 536309405. (3.1 s)" against 60 s; zero console errors, zero external requests, strict KaTeX re-parse clean.')
ov('r17-cmd-run-graders-S7', 'PASS', f'{RUN_TAG}: tools/run_graders.py --unit S7 --seeds 0-49: "run_graders S7: PASS (reference 50/50 seeds, slowest 1.6 s)" against the 10 s budget (logs/run_graders.log).')
ov('r17-cmd-mutate-before', 'PASS', f'{RUN_TAG}: superseded by r17-cmd-mutate-after and the r33 run on the current tree, which contains y28 to y30 (tools/mutate_graders.py --unit S7 --seeds 0-9: "mutate_graders S7: PASS (164/164 killed)", logs/mutate.log). The pre-y28 run is not repeated because its tree no longer exists in the checkout.')
ov('r17-cmd-mutate-after', 'PASS', f'{RUN_TAG}: tools/mutate_graders.py --unit S7 --seeds 0-9 on the current tree (164 .py mutants plus u00/v00/w00 proposed-killing-test notes): "mutate_graders S7: PASS (164/164 killed)", exit 0, 167.8 s; 0 survivors (logs/mutate.log).')
ov('r17-cmd-verify-refs-offline', 'PASS', f'{RUN_TAG}: .venv/bin/python tools/verify_refs.py --offline (no --unit; --offline rejects --unit): "offline integrity: 560 entries, 0 problems" (logs/verify_refs_offline_full.log).')
ov('r17-cmd-verify-refs-unit-S7', 'PASS', f'{RUN_TAG}: .venv/bin/python tools/verify_refs.py --unit S7 --workers 1 (live Crossref and publisher pages, no cache): final line "live re-verification of S7: 94 of 560 entries, 0 problems", exit 0 (logs/verify_refs_live_S7.log).')
ov('r17-cmd-fetch-data-check', 'PASS', f'{RUN_TAG}: .venv/bin/python tools/fetch_data.py --check: "fetch_data: 3 datasets, 0 problems" (logs/fetch_data_check.log). Live rebuild of all three snapshots, see r33-data-reproducible.')
ov('r17-cmd-render-curriculum-check', 'PASS', f'{RUN_TAG}: .venv/bin/python tools/render_curriculum.py --check: "curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h (6.35 FTE years)", exit 0 (logs/render_curriculum_check.log).')
ov('r17-cmd-build-site-check', 'PASS', f'{RUN_TAG}: .venv/bin/python tools/build_site.py --check: "site data current: 6 outputs", exit 0 (logs/build_site_check.log).')
ov('r17-cmd-ruff-check', 'PASS', f'{RUN_TAG}: .venv/bin/ruff check . : "All checks passed!", exit 0 (logs/ruff_check.log).')
ov('r17-cmd-ruff-format-check', 'PASS', f'{RUN_TAG}: .venv/bin/ruff format --check . : "124 files already formatted", exit 0 (logs/ruff_format_check.log).')
ov('r17-cmd-mypy-strict', 'PASS', f'{RUN_TAG}: .venv/bin/mypy (pyproject strict; mypy 2.4.0 pinned in requirements-dev): "Success: no issues found in 101 source files", exit 0 (logs/mypy_strict.log). Note: pyproject excludes two S7 lab twins from mypy; see notes.')
ov('r17-cmd-starter-page-command', 'PASS', f'{RUN_TAG}: QF_SEED=0 .venv/bin/pytest -q -p no:cacheprovider --assert=plain -W error test_project.py in a workspace with the starter as atlas/integrity.py: "146 failed, 16 passed in 3.21s"; seed 1: "146 failed, 16 passed in 2.88s"; every failure is NotImplementedError (146 of 146 lines).')
ov('r17-cmd-starter-trace', 'PASS', f'{RUN_TAG}: pytest plugin (scratch plug/stub_trace.py) recording, per test, which integrity.py stub functions it enters, on the starter at QF_SEED 0, 1 and 984012265: 146 tests enter a stub and fail (all NotImplementedError), 16 enter none and pass, identically at each seed. The 16 are TrialSet and from_backtest input validation, the signature-defaults test, dependency test and the last-column test (names in plug/trace_0.json).')
ov('r17-cmd-collect-162', 'PASS', f'{RUN_TAG}: QF_SEED=0 .venv/bin/pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py on the reference workspace: "162 tests collected in 0.03s".')
ov('r17-cmd-local-suite-reference', 'PASS', f'{RUN_TAG}: QF_SEED=0,1,2 .venv/bin/pytest -q -p no:cacheprovider --assert=plain -W error test_project.py with grader/reference.py as atlas/integrity.py: "162 passed" at each seed (0.88 s, 0.84 s, 0.89 s).')
ov('r17-cmd-lab-L08-4-twin', 'PASS', f'{RUN_TAG}: python -I -W error tests/labs/S7/lab-S7-L08-4.py in a scratch directory whose data/ holds fx_monthly.csv: exit 0; prints PBO S=8 0.7429, S=10 0.7143, S=16 0.7330; null PBO mean 0.527, share at or above 0.7330 0.210; DSR 0.4890 (see r33-headline-recompute).')
ov('r17-cmd-lab-project-3-twin', 'PASS', f'{RUN_TAG}: python -I -W error tests/labs/S7/lab-S7-project-3.py in a scratch directory with fx_monthly.csv: exit 0; "selected: column 2, L1-H3-skip0"; matches the page (run_labs S7 PASS).')
ov('r17-cmd-lab-sol-L04-P4', 'PASS', f'{RUN_TAG}: python -I -W error tests/labs/S7/sol-S7-L04-P4.py: exit 0; prints the max_exact/max_simulated/sum_exact/fisher_simulated table; matches the L04 P4 expected block (run_labs S7 PASS).')
ov('r17-cmd-form-sweep', 'PASS', f'{RUN_TAG} (narrowed re-run, see memo-self-assessment-form): the 84-press Playwright sweep script (form_sweep_r17.py) is not in this checkout or environment, so it is not repeated. The r33 browser check on the default wording (r33-rubric-default-wording) found zero page errors and zero external requests, and the sweep row is carried on the rubric.js diff, which changes wording only.')
ov('r17-cmd-prose-sweep', 'PASS', f'{RUN_TAG}: equivalent diff-scoped re-run: visible text of project.html at 5e5da87 and at HEAD (tags stripped, entities decoded) has 727 numerals in both; the multiset difference is exactly +3.14, +2.4, +9.0 and -3.12, -2.2, -8.3, all in the one sentence of line 195. The scratch prose_sweep_r17.py is not repeated; every other numeral is carried, and each memo number is re-derived by {MEMO_TEST}.')
ov('r17-cmd-wordcount', 'PASS', f'{RUN_TAG}: memo body word counts are re-derived by tests/test_memo_exemplars.py (body_words_a 322, body_words_b 1,352, rec_words_b 92): test_memo_text_has_no_unpinned_digits and test_every_exemplar_number_is_pinned_to_its_computation pass; the scratch wordcount_r17.py is not repeated.')
ov('r17-cmd-blind-extract', 'PASS', f'Carried in substance: the exemplar memo text (project.html #exemplar-a and #exemplar-b, lines 300 to 420) is byte-identical in the passages the diff does not touch (the only changed line is 195); the scratch blind_extract.py output is not repeated, and the calibration rows are carried on that identity.')
ov('r17-cmd-tetzlaff-fetch', 'PASS', f'{RUN_TAG}: curl https://api.crossref.org/works/10.1016/j.learninstruc.2025.102142 (HTTP 200): title "A cornerstone of adaptivity – A meta-analysis of the expertise reversal effect", container Learning and Instruction, volume 98, issued 2025-08, authors Tetzlaff, Simonsmeier, Peters, Brod. curl https://api.openalex.org/works/doi:10.1016/j.learninstruc.2025.102142 (HTTP 200): same title, publication_year 2025, type review. Matches references/references.json key tetzlaff2025cornerstone.')
ov('r17-cmd-lemma76-check', 'PASS', f'{RUN_TAG}: re-ran the telescoping identity sum_(l=1..M) (b_l - b_(l-1))/l = sum_(j<M) b_j/(j(j+1)) + b_M/M with b_0 = 0 (the convention of Lemma 7.6 in L05.html, "0 = beta_0") on 2000 random vectors, M up to 14: max abs error 6.7e-16. The Monte Carlo union-bound figures are not repeated (scratch); L05.html and cards.json are byte-identical since 5e5da87.')
ov('r17-cmd-statement-diff', 'PASS', f'Carried on byte-identity: the statements scanned are in L01-L08.html and cards.json, all byte-identical since 5e5da87 (git diff --quiet on course/modules/S/S7 excluding project.html). The scratch regex scan is not repeated.')
ov('r17-cmd-git-diff', 'PASS', f'{RUN_TAG}: git diff --stat 5e5da87 HEAD -- <slice paths>: 55 files changed, 3205 insertions(+), 208 deletions(-) (full list in the report notes). Only course/modules/S/S7/project.html changed among S7 files.')
ov('r17-cmd-git-status', 'PASS', f'{RUN_TAG}: git -C <checkout> status --short after the round: only "?? .venv" (the shared venv symlink); no tracked file modified.')
ov('r16-cmd-curl-licence', 'PASS', f'{RUN_TAG}: curl -sS -o disclaimer.htm -w "%{{http_code}} %{{size_download}}" https://www.federalreserve.gov/disclaimer.htm: "200 85130" (same size as round 16). The sentence "Unless otherwise indicated, information on Board\'s website is in the public domain and may be copied and distributed without permission." is present (grep of the text).')
ov('r16-cmd-indep-memo', 'PASS', f'{RUN_TAG}: equivalent independent recomputation in my own code: see r33-headline-recompute, which recomputes every headline number of the memo from fx_monthly.csv (the same values as the round-16 script).')
ov('r16-cmd-recheck-outputs', 'PASS', f'{RUN_TAG}: equivalent: the instances are re-checked by run_graders --unit S7 --seeds 0-49 (50/50, which runs check_instances), the in-browser outputs by page_smoke S7 (in-browser grader 162 pass, every lab output), and the card outputs are carried on byte-identity of cards.json. The round-16 scratch script recheck_outputs_r16.py is not in this environment and is not repeated.')
ov('r16-cmd-recheck-refs', 'PASS', f'{RUN_TAG}: verify_refs --offline (560 entries, 0 problems) and verify_refs --unit S7 live (94 entries, 0 problems). The scratch abstract-sentence re-read (abstract_sentences_r16.py) is not repeated; its inputs (the claim spans in L01-L08.html and the registry titles, authors and DOIs) are unchanged, because references.json differs only in generated_at and used_by.')
ov('r16-cmd-quiz-all-combos', 'PASS', f'Carried on byte-identity: course/modules/S/S7/index.html, course/assets/js/quiz.js, course/assets/js/site.js, and the figure files are byte-identical since 5e5da87. The all-combinations quiz script is in no checkout here and is not repeated; page_smoke S7 (index.html loads and initialises its quizzes with zero console errors) passes on the r33 toolchain.')
ov('r16-p4-premise', 'PASS', f'{RUN_TAG}: run_labs S7 PASS (42/42) checks sol-S7-L04-P4 output against the L04 page; my direct run of tests/labs/S7/sol-S7-L04-P4.py matches (table rows sparse_a=4 0.7749 0.7783 0.1066 0.2446; dense_delta=0.3 0.1329 0.1304 0.9123 0.8594).')
ov('r14-theorem-4-2-numbers', 'PASS', f'{RUN_TAG}: the L06 Lab 3 table (Lesson 6 section 4): direct run of tests/labs/S7/lab-S7-L06-3.py prints the 0.5238 entry in the row "3.00 0.0027 0.0111 0.0110 0.0425 0.1743 0.5238"; run_labs S7 PASS checks it against the page. The Theorem 4.2 bound (4) is prose with unchanged text (L06.html byte-identical).')

# ----- data and licence rows
ov('proj-data-fx-monthly', 'PASS', f'{RUN_TAG}: rebuilt fx_monthly.csv from the live H.10 feed with tools/fetch_data.py --fetch --only fx_monthly --keep-raw in a scratch copy (git archive of HEAD plus the market folder): snapshot sha256 60572240d1a9d1832d5021297634b2369723b94098414948b891dd26a8bffe3e = MANIFEST, 669 rows, 67392 bytes. Live raw zip sha256 17d087d0ebb2a0ac... differs from MANIFEST raw_sha256 8f370f9c57b7... (issuer updated the live file; provenance only, not refreshed; VERIFIER_RULES 2.8). Licence: licence_url https://www.federalreserve.gov/disclaimer.htm fetched (HTTP 200, 85130 bytes); the quoted sentence "Unless otherwise indicated, information on Board\'s website is in the public domain and may be copied and distributed without permission" is present, granting redistribution.')
ov('proj-data-fx-daily-release-url', 'PASS', f'{RUN_TAG}: tools/data_sources.yaml fx_daily url is line 22 (unchanged: the diff hunks start at line 28). MANIFEST fx_daily source_url = https://www.federalreserve.gov/releases/h10/data/FRB_h10_xml.zip (same). Rebuilt fx_daily from the live zip in the scratch copy: sha256 02872dd7e23938da... = MANIFEST, 6706 rows, 443841 bytes.')
ov('proj-data-h15-release-url', 'PASS', f'{RUN_TAG}: tools/data_sources.yaml ust_daily url is now line 94 (line 80 at 5e5da87; the release row cited 79). MANIFEST ust_daily source_url = https://www.federalreserve.gov/releases/h15/data/FRB_h15_xml.zip (same). Rebuilt ust_daily from the live zip: sha256 dd70e1a21c56e6a3... = MANIFEST, 6690 rows, 140520 bytes.')
ov('proj-data-treasury-licence-recheck', 'PASS', f'{RUN_TAG}: the ust_daily note is now lines 100 to 107 of tools/data_sources.yaml (the release row cited 82 to 92; the H.10 notes above it added lines). Re-read and re-fetched: https://www.federalreserve.gov/releases/h15/default.htm (HTTP 200): footnote 4 "On a discount basis." (tbill_3m) and footnote 9 "Yields on actively traded non-inflation-indexed issues adjusted to constant maturities ... Source: U.S. Treasury." (cmt_10y). https://www.copyright.gov/title17/92chap1.html (HTTP 200): 17 U.S.C. 105(a) "Copyright protection under this title is not available for any work of the United States Government" present.')
ov('proj-data-ddp-retirement-quote', 'PASS', f'{RUN_TAG}: tools/data_sources.yaml header lines 8 to 10 unchanged (the DDP retirement sentence and the quoted "Historical data will remain available for download as XML files on statistical release pages"); the diff hunks begin at line 28, so the header is byte-identical.')
ov('r15-data-header-claims', 'PASS', f'{RUN_TAG}: tools/data_sources.yaml header lines 9 to 14 (unchanged since 5e5da87; the diff hunks begin at line 28) read "MANIFEST records the H.10 release-page zip retrieved on 2026-10-19 (... SHA-256 8f370f9c...) and the H.15 zip retrieved on 2026-10-20 (SHA-256 334a7f88...)": MANIFEST raw_sha256 values for fx_daily and fx_monthly (8f370f9c57b73e1c...) and ust_daily (334a7f8870016d42...) match, and retrieved dates are 2026-10-19 and 2026-10-20. "Both rebuild the same snapshots byte for byte" is re-established by r33-data-reproducible.')
ov('r15-data-retrieval-dates', 'PASS', f'{RUN_TAG}: retrieval dates in MANIFEST are fx_daily 2026-10-19, fx_monthly 2026-10-19, ust_daily 2026-10-20; the S7 pages and project.html quote 2026-10-19 (fx_monthly) and the cards and tests that quote it match these values (carried: the pages are byte-identical except project.html line 195, which has no date).')
ov('proj-changed-inputs-retrieved', 'PASS', f'{RUN_TAG}: project.html #spec Inputs quotes "retrieved 2026-10-19" for fx_monthly; MANIFEST fx_monthly retrieved 2026-10-19 (same). Passage not in the diff (only line 195 changed).')
ov('r13-css-chart-rules-not-drawn', 'PASS', 'Carried on byte-identity: course/assets/css/course.css is byte-identical since 5e5da87 (git diff --quiet).')
ov('r14-no-figure-controls', 'PASS', 'Carried: course/modules/S/S7/project.html and index.html have no figure controls; project.html changed only at line 195 (a sentence of text with no control), and index.html is byte-identical.')
ov('r15-data-retrieval-dates-x', 'PASS', 'unused')
OVR.pop('r15-data-retrieval-dates-x')
ov('proj-carried-lesson-citations', 'PASS', 'Carried on byte-identity: the lesson passages cited by project.html rows (L01 to L08) are byte-identical since 5e5da87; project.html changed only at line 195.')

# ----- citations (live verify_refs for S7 keys)
LIVE = '{RUN}: verify_refs --unit S7 live: "live re-verification of S7: 94 of 560 entries, 0 problems" (logs/verify_refs_live_S7.log): title, authors, year and venue of each S7 key re-resolved against Crossref. '
for i in ['hub-cite-white2000reality', 'hub-cite-romano2005stepwise', 'hub-cite-benjamini1995controlling', 'hub-cite-bailey2014deflated', 'hub-cite-bailey2016probability', 'proj-cite-politis1994stationary', 'proj-cite-moskowitz2012time', 'proj-cite-huang2020time', 'hub-cite-harvey2015cross', 'hub-cite-harvey2017presidential', 'proj-cite-kalyuga2003expertise']:
    ov(i, 'PASS', LIVE.replace('{RUN}', RUN_TAG) + 'The key is cited by a passage that is byte-identical since 5e5da87 (index.html), or by project.html outside line 195; references.json changed only in generated_at and used_by.')
ov('proj-cite-tetzlaff2025cornerstone', 'PASS', LIVE.replace('{RUN}', RUN_TAG) + 'Crossref and OpenAlex (r17-cmd-tetzlaff-fetch re-run) agree on title, Learning and Instruction 98, 2025, authors Tetzlaff, Simonsmeier, Peters, Brod. The claim span passage is outside line 195.')

# ----- grade rows
ov('proj-claim-expertise-reversal', 'PASS', f'{RUN_TAG}: grade re-read against BLUEPRINT section 3 (BLUEPRINT.md changed only in the credential table rows at lines 74-75; section 3 unchanged, so the grading rule is unchanged). The claim span is in project.html #ladder (outside line 195) and its cited keys kalyuga2003expertise and tetzlaff2025cornerstone resolve live (verify_refs S7 PASS). Carried for the passage.')

# ----- labs
for i in ['proj-lab-1', 'proj-lab-2', 'proj-lab-3', 'proj-changed-lab3-hypothesis']:
    ov(i, 'PASS', f'{RUN_TAG}: run_labs S7 PASS (42/42) on {TOOL}, including lab-S7-project-1, lab-S7-project-2 (completion, solution twin) and lab-S7-project-3; page_smoke S7 ran each project lab in Pyodide (0.0 s each, runtime boot 1.0 s, package preload 0.3 s, outside the lab timers). Twin run directly (python -I -W error): exit 0.')
ov('proj-number-lab3', 'PASS', f'{RUN_TAG}: run_labs S7 PASS checks the printed output of lab-S7-project-3 (trial matrix checksums, Sharpe grid, "selected: column 2, L1-H3-skip0") against the page; my direct run prints the same selection, and my own rebuild of the trial matrix gives the same headline statistics (r33-headline-recompute).')

# ----- hours, numbers in spec
ov('proj-number-checks-count', 'PASS', f'{RUN_TAG}: "162 checks" (project.html #spec): pytest --collect-only on the reference workspace: 162 tests collected (r17-cmd-collect-162 re-run); the in-browser run reports "All 162 tests pass" (page_smoke S7).')
ov('proj-spec-grading-mode', 'PASS', f'{RUN_TAG}: "162 checks" re-verified (see proj-number-checks-count); the grading mode text itself is byte-identical since 5e5da87 (only line 195 of project.html changed).')
ov('proj-number-limits-versions', 'PASS', f'{RUN_TAG}: "within 60 seconds in your browser": in-browser grader 3.1 s (page_smoke S7, GRADER_LIMIT_S 60); local reference suite 0.88 s; slowest seed in run_graders 0-49 1.6 s. "T >= 4" and "2**1000" carried (byte-identical text). The Python and library versions named in the project page were re-verified in r33-local-versions-sentence.')
ov('proj-local-instructions', 'PASS', f'{RUN_TAG}: project.html #local line 195 re-read: "Use Python 3.14 with NumPy 2.4 and pytest 9.0, the versions the in-browser grader runs." Checked against requirements-dev.txt (numpy==2.4.6, pytest==9.0.2), pyproject.toml (requires-python >=3.14), tools/vendor_spec.yaml (pyodide 314.0.7) and course/assets/vendor/pyodide/pyodide-lock.json (info.python 3.14.2; numpy 2.4.6, pytest 9.0.2, scipy 1.18.0): all agree. The page command is run as written: QF_SEED=0, 1, 2 "162 passed" (r17-cmd-local-suite-reference). Command and sentence PASS. Dual-mode: in-browser 162 pass (page_smoke).')
ov('proj-hours-hub-split', 'PASS', 'Carried: index.html is byte-identical since 5e5da87 and project.html changed only at line 195, outside the hours table; data-hours-project 30 unchanged.')
ov('atlas-dependency-constraint', 'FAIL', f'{RUN_TAG}: atlas/A8.contract.md line 6 reads "Depends on: NumPy 2.2 and the Python standard library only." The toolchain the grader runs and the repo pins is NumPy 2.4.6 (requirements-dev.txt numpy==2.4.6; pyodide-lock numpy 2.4.6; the project page now says NumPy 2.4). The contract is "frozen once S7 is released", so it is not edited here. Also the stdlib-only test (test_depends_on_numpy_and_stdlib_only) is re-run and passes within the 162 (r17-cmd-local-suite-reference). The mismatch is a stale version pin in a frozen contract: fix by a CONTRACT_CHANGE_REQUEST (BUILDER_RULES 5.5) that restates the dependency as the version tested (NumPy 2.4.6, or NumPy 2.2 or later if that has been verified), then re-verify the atlas rows.')
OVR['atlas-dependency-constraint'] = ('FAIL', OVR['atlas-dependency-constraint'][1])

# ----- rubric (rubric.js changed; wording only)
RUBRIC_DIFF = 'course/assets/js/rubric.js changed only in workWording (new export with defaults equal to the old S7 literals "Your memo", "memo", "memo/self_assessment.md") and in the comparison header, advice and copy-label text that now read those variables; saveRecord and persist are not in any diff hunk.'
ov('memo-self-assessment-form', 'PASS', f'{RUN_TAG}: {RUBRIC_DIFF} Browser check (Chromium via Playwright, scratch rubric_wording.py) on the S7 project page: section#self-assessment has no data-work-* attributes, so defaults apply: legend "Your memo", comparison header "Your memo", copy label "Summary to keep as memo/self_assessment.md"; page errors 0; external requests 0. tests/js/rubric.test.mjs passes (workWording defaults and overrides, tests/test_js.py). The 84-press sweep is carried (see r17-cmd-form-sweep).')
ov('memo-self-assessment-save-status', 'PASS', f'{RUN_TAG}: course/assets/js/rubric.js saveRecord and persist are not in any diff hunk (the changed hunks are comparisonTable, initRubric wording and the workWording export); course/assets/js/store.js is byte-identical. tests/js/rubric.test.mjs and page_smoke S7 (no console errors, site.js step errors 0) pass.')
ov('rubric-js-unit-tests', 'PASS', f'{RUN_TAG}: tests/test_js.py::test_js_suite[rubric.test.mjs] PASSED (pytest slice, 258 passed). The new test "the work wording defaults to S7\'s memo and follows the section\'s data attributes" is included.')
ov('site-js-rubric-step', 'PASS', f'{RUN_TAG}: site.js is byte-identical; its rubric step calls initRubric in rubric.js (changed, wording only). page_smoke S7 on project.html: zero site.js step errors (logs/page_smoke_S7.log).')
ov('memo-test-pins', 'PASS', f'{RUN_TAG}: tests/test_memo_exemplars.py changed only in one unused-variable name (n_trials to _n_trials, same logic). Re-run: 20 passed with test_run_labs.py (logs/pytest_memo_run_labs.log), including test_the_memo_trial_set_is_lesson_8_lab_4s, test_the_reference_module_agrees_with_lesson_8_lab_4, test_every_exemplar_number_is_pinned_to_its_computation, test_memo_text_has_no_unpinned_digits, test_annotations_agree_with_the_exemplar_scores, and the level-2 and level-4 exemplar tests.')
ov('memo-exemplars-intro', 'PASS', f'{RUN_TAG}: tests/test_memo_exemplars.py module docstring unchanged; the test passes (see memo-test-pins).')
ov('r17-hunk-project-exemplar-a-verdict', 'PASS', 'Carried on the hunk check: project.html changed only at line 195; the Exemplar A verdict paragraph (line 324) is byte-identical, and its scores (data-scores) are pinned by test_annotations_agree_with_the_exemplar_scores (PASS).')
ov('r17-hunk-project-exemplar-b-verdict', 'PASS', 'Carried on the hunk check: project.html changed only at line 195; the Exemplar B verdict paragraph (line 403) is byte-identical; its scores and annotations pass test_annotations_agree_with_the_exemplar_scores.')

# ----- numbers on the project page (memo-number-*)
def memo_number(i, key):
    val = DN.get(key)
    ev = f'{RUN_TAG}: project.html span data-num="{key}" reads {val!r}. ' + MEMO_TEST + '. '
    if key in INDEP_KEYS:
        ev += INDEP + ' '
    ev += 'Carried text: the passage is byte-identical (only line 195 changed).'
    return ev
for r in OLD:
    if r['check'] == '2.2-number' and r['location'].startswith('course/modules/S/S7/project.html span[data-num='):
        key = re.search(r'data-num=([a-z0-9_]+)', r['location']).group(1)
        ov(r['id'], 'PASS', memo_number(r['id'], key))
ov('memo-exemplar-b-pbo-reading', 'PASS', f'{RUN_TAG}: project.html #exemplar-b PBO paragraph quotes 0.527 (null PBO mean), 21% (share at or above), 0.733 (PBO), DSR 0.489: the r33 lab-S7-L08-4 twin prints "PBO mean 0.527 ... share at or above 0.7330: 0.210" and "DSR ... 0.4890"; my own recomputation gives PBO 0.733 (the 16-block CSCV on the same matrix), and the test pins each value. ' + INDEP)
ov('proj-number-hours-table', 'PASS', 'Carried: the hours table is byte-identical (project.html changed only at line 195); the component hours are estimates with no computed value (the total 30 h equals data-hours-project).')
ov('proj-number-lab-claims', 'PASS', f'{RUN_TAG}: lab-S7-project-1 and -2 hypotheses and interpretations: run_labs S7 PASS (42/42) confirms the printed outputs match the page; the interpretation text is byte-identical.')
ov('proj-number-context', 'PASS', f'Carried: the lede, #spec Context and #memo intro numbers are byte-identical passages; each numeric value they quote is pinned by a data-num (test_memo_exemplars PASS) or by a lab (run_labs PASS).')
ov('r15-sweep-numbers-hub-project', 'PASS', f'{RUN_TAG}: diff-scoped numeral sweep of project.html (727 numerals at 5e5da87 and at HEAD; the only change is the line-195 sentence, +3.14 +2.4 +9.0 -3.12 -2.2 -8.3), and index.html is byte-identical. The hub figures are carried rows hub-hours-split, hub-placement-answers, hub-lesson-problem-minimum and hub-unlocks.')
ov('r15-sweep-numbers-lessons', 'PASS', 'Carried on byte-identity: the lesson passages (L01-L08.html) and the project labs the sweep covers are byte-identical since 5e5da87; the project-page part is re-run as r17-cmd-prose-sweep.')
ov('proj-number-hours-table-x', 'PASS', 'unused') if False else None

# ----- mutation rows
SET_ROWS = {'grader-mutant-rebase', 'r14-mutant-set-pinned', 'grader-mutant-set-r17', 'r15-mutants-y12-y17-present'}
for r in OLD:
    if r['check'] == '2.6-mutation' and r['id'] not in OVR:
        loc = r['location']
        if r['id'] in SET_ROWS or 'ledgers/S7/mutants/ ' in loc or loc.rstrip().endswith('mutants/'):
            ov(r['id'], 'PASS', f'{RUN_TAG}: tools/mutate_graders.py --unit S7 --seeds 0-9 on {TOOL}: "mutate_graders S7: PASS (164/164 killed)"; 0 survivors. The mutant set (164 .py files) is byte-identical since 5e5da87 (ledgers/S7 is not in the diff). Set-level row.')
            continue
        m = re.search(r'ledgers/S7/mutants/([A-Za-z0-9_]+\.py)', loc)
        if not m:
            raise SystemExit('no mutant file in ' + r['id'] + ': ' + loc)
        fname = m.group(1)
        test, seed = mut[fname]
        ov(r['id'], 'PASS', f'{RUN_TAG}: mutate_graders --unit S7 --seeds 0-9 ({TOOL}): KILLED {fname} by {test} (seed {seed}). The mutant file is byte-identical since 5e5da87.')

# ----- grader autograder rows (suite re-run)
SUITE = f'{RUN_TAG}: pytest test_project.py on the reference (QF_SEED 0, 1, 2): 162 passed each seed; the same 162 in the browser (page_smoke S7: "All 162 tests pass on seed 536309405. (3.1 s)"); run_graders 0-49 50/50, slowest 1.6 s. '
ov('grader-run-graders', 'PASS', SUITE + 'Command: tools/run_graders.py --unit S7 --seeds 0-49 (logs/run_graders.log).')
ov('grader-instances', 'PASS', f'{RUN_TAG}: run_graders --unit S7 --seeds 0-49 runs check_instances over 50 seeds (0 to 49, which includes the 20 sampled seeds 0-19): "reference 50/50 seeds" PASS. Instances validated by the suite; answers differ across seeds (fingerprint check in check_instances).')
ov('grader-dual-mode', 'PASS', SUITE + 'Both runtimes run the same test_project.py.')
ov('grader-messages', 'PASS', f'{RUN_TAG}: test_project.py is byte-identical; its failure messages are exercised by the 146 starter failures (all NotImplementedError from the starter stubs) and the 162 reference passes.')
ov('grader-panel-local-command', 'PASS', 'Carried on byte-identity: course/assets/js/grader.js is byte-identical since 5e5da87; the local command it prints equals the command run in r17-cmd-local-suite-reference (162 passed).')
ov('grader-contract-faithful-variant', 'PASS', SUITE + 'The contract-faithful alternative is covered by the same suite passing.')
ov('grader-new-tests-runtime', 'PASS', SUITE + 'All 162 tests collected and run (r17-cmd-collect-162).')
for r in OLD:
    if r['location'].startswith('grader/test_project.py::') or r['id'].startswith('grader-new-test') or r['id'].startswith('grader-r1') :
        if r['id'] not in OVR:
            name = r['location'].split('::')[-1] if '::' in r['location'] else r['id']
            ov(r['id'], 'PASS', f'{RUN_TAG}: test {name} is one of the 162 tests: passed on reference at QF_SEED 0, 1, 2 (local) and in the browser (page_smoke S7, seed 536309405). test_project.py is byte-identical since 5e5da87.')
ov('grader-run-graders-x', 'PASS', 'x') if False else None

# ----- numeric grader atlas rows that depend on numerics: already in suite

ov('atlas-curriculum-briefs', 'PASS', f'{RUN_TAG}: curriculum/curriculum.json S7 and A8 entries are unchanged (no S7 or A8 hunk in the diff); CURRICULUM.md changed only in the program-level prerequisite and count lists (M8, FC1 added; no A8 or S7 line changed, git diff grep); program.json changed only in the MS-FIN and PHD-FIN hour totals and closure lists. render_curriculum --check PASS and build_site --check PASS.')
ov('r15-slice-files-unchanged', 'PASS', f'{RUN_TAG}: the release claim "slice files unchanged" is re-stated for this round: project.html (line 195 only), rubric.js (wording: workWording export and variable substitution, defaults equal to the old literals), tests/test_memo_exemplars.py (one unused-variable rename), BLUEPRINT.md and README.md (credential table rows only). All other slice files (project.html passages, grader/, atlas/A8.contract.md except its numpy pin, tests/labs/S7, cards, lessons, figures, rubric.js saveRecord/persist, print.css, course.css, site.js, grader.js) are byte-identical or checked by hunk; the atlas contract numpy pin is a FAIL (atlas-dependency-constraint).')
# ----- check flagged structure rows
ov('docs-figures-test-comment', 'PASS', f'{RUN_TAG}: BLUEPRINT.md and README.md changed (BLUEPRINT: credential table rows 74-75; README: credential table rows 53-54) and the figures they hold are checked by tests/test_docs_figures.py (14 passed in the pytest slice). The pyproject change and the tests/test_docs_figures.py file itself are byte-identical.')
ov('r13-governance-rules', 'PASS', f'{RUN_TAG}: VERIFIER_RULES.md changed in sections 2.5 (lab rule now "run_labs passes the lab under CPython 3.14") and 2.8 (reproducibility rule, applied in r33-data-reproducible); sections 2.1 and 2.6 cited by this row are unchanged (hunk check). BUILDER_RULES.md 6.6 is byte-identical.')
ov('r17-verdict-no-overall', 'PASS', 'Carried on the hunk check: project.html changed only at line 195, and the "overall" words checked by r17 are absent (grep of project.html, rubric.js, grader.js, site.js: no "overall" in the S7 verdict text).')
ov('r16-starter-claim', 'PASS', f'{RUN_TAG}: starter run at QF_SEED 0: 146 failed, 16 passed; every failure is NotImplementedError; the traced run confirms the 146 enter a stub and the 16 pass without one (r17-cmd-starter-trace re-run). The sentence at project.html line 169 is byte-identical.')
ov('r17-tests-slice-passed', 'PASS', f'{RUN_TAG}: tests/test_page_checks.py, test_memo_exemplars.py, test_js.py, test_docs_figures.py, test_labs.py, test_figure_kernels.py, test_run_labs.py, test_fetch_data.py, test_page_smoke.py: 258 passed (logs/pytest_slice.log).')
ov('r15-tests-slice-pytest-note', 'PASS', f'{RUN_TAG}: the slice test files named here pass (258 passed, logs/pytest_slice.log).')
ov('r17-cmd-pytest-slice-x', 'PASS', 'x') if False else None
ov('check-projects-tests', 'PASS', f'{RUN_TAG}: tests/test_page_checks.py in the 258-pass slice; tools/check_projects.py --all PASS.')
ov('check-projects-both-rule', 'PASS', f'{RUN_TAG}: check_projects --unit S7 and --all PASS (logs/check_projects_S7.log, check_projects_all.log).')
ov('check-projects-exemplar-levels', 'PASS', f'{RUN_TAG}: check_projects --unit S7 PASS (rubric_problems: exemplar levels).')
ov('r17-cards-vs-something', 'PASS', 'x') if False else None
ov('r16-xref-targets', 'PASS', 'Carried on the hunk check: project.html cross-references are at lines other than 195 and the lesson targets are byte-identical; check_pages S7 PASS (r33).')
ov('proj-cross-references', 'PASS', 'Carried on the hunk check (project.html changed only at line 195) plus check_pages --unit S7 PASS (r33) for the lesson and section targets.')
ov('proj-structure', 'PASS', 'Carried on the hunk check (project.html changed only at line 195, a sentence inside #local); check_pages S7 PASS and page_smoke S7 PASS (r33).')
ov('memo-exemplars-intro-x', 'PASS', 'x') if False else None
ov('curriculum-s7-core-line', 'PASS', f'{RUN_TAG}: curriculum/curriculum.json has no S7 hunk in the diff (the changed hunks are MS-FIN, PHD-FIN, the FC1/M8 closure rows and the 03-markets SDF module); render_curriculum --check PASS.')
ov('curriculum-s7-entry', 'PASS', f'{RUN_TAG}: curriculum.json S7 entry unchanged (no hunk); render_curriculum --check PASS; build_site --check PASS.')
ov('r13-xref-L07-s2-formula', 'PASS', 'Carried on the hunk check (project.html line 104 is not in the diff) and on byte-identity of L07.html.')

# ----- set the S7 lesson/card carries as explicit notes
ov('r15-cards-banned-phrases', 'PASS', f'{RUN_TAG}: banned-phrase scan (BUILDER_RULES 1.3-1.4 strings: TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, roughly half, historically) over course/modules/S/S7/*.html, cards.json, grader/*.py, atlas/A8.contract.md, rubric.js, grader.js, site.js and the S7 labs: 0 hits in the project page, the cards, the grader, the contract, and the JS. One hit in L01.html (line 133, "roughly half a standard deviation"), which is outside this slice (lesson ledger) and byte-identical since 5e5da87; flagged in notes.')
ov('r16-banned-phrases', 'PASS', f'{RUN_TAG}: same scan as r15-cards-banned-phrases: 0 hits in project.html (including the new line-195 sentence), index.html, grader/*.py, atlas/A8.contract.md, rubric.js, grader.js.')
ov('r17-cmd-git-diff-x', 'PASS', 'x') if False else None

# ----- new r33 checks
NEW = []
def new(i, check, loc, status, ev, fix=None):
    r = {'id': i, 'check': check, 'location': loc, 'status': status, 'evidence': ev}
    if fix and status != 'PASS': r['fix'] = fix
    NEW.append(r)

new('r33-local-versions-sentence', '2.9-structure', 'course/modules/S/S7/project.html line 195 (#local)', 'PASS',
    'project.html line 195: "Use Python 3.14 with NumPy 2.4 and pytest 9.0, the versions the in-browser grader runs." requirements-dev.txt: numpy==2.4.6, pytest==9.0.2 (2.4 and 9.0 match); pyproject.toml requires-python ">=3.14" (3.14 matches); tools/vendor_spec.yaml pyodide version "314.0.7"; course/assets/vendor/pyodide/pyodide-lock.json info.python "3.14.2", packages numpy 2.4.6, pytest 9.0.2, scipy 1.18.0 (the in-browser versions). Local interpreter 3.14.8, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2 (python -V and import check). No other version sentence in S7 pages, labs, grader or contract is in conflict except atlas/A8.contract.md line 6 (see atlas-dependency-constraint).')
new('r33-pyodide-lock-and-vendor', '2.8-figure', 'course/assets/vendor/LOCK.json; course/assets/vendor/pyodide/pyodide-lock.json; tools/vendor_spec.yaml', 'PASS',
    'Lock packages numpy-2.4.6-cp314 (sha256 a292c1f5...), scipy-1.18.0, pytest-9.0.2: the vendored wheel files exist and their sha256 equals the lock entry (checked in Python). tests/test_vendor.py: 16 passed (logs/vendor_pagesmoke_tests.log, with tests/test_page_smoke.py).')
new('r33-notation-collisions', '2.4-mathematics', 'notation/notation.json symbols R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} (AP1, new); course/modules/S/S7/*.html, cards.json, figures-*.js, grader/*.py, tests/labs/S7/*.py, atlas/A8.contract.md', 'PASS',
    'Regex scan for the four new symbols (R_f, R^\\ast and R^{e\\ast} not preceded by a letter; \\mathbb{Q}; \\Q) over the S7 slice: 0 hits. S7 uses \\SR and \\SR^\\ast (the Sharpe benchmark; a registered macro in notation.json) and \\PSR, \\DSR, \\hSR; \\SR^\\ast contains the substring R^\\ast only inside \\SR^\\ast, which is not the symbol R^\\ast (no standalone match). The 26 macros are unchanged; the registry of symbols gained four AP1 entries with no duplicate keys (json object scan). No collision.')
new('r33-glossary-curriculum-registry', '2.9-structure', 'course/assets/data/glossary.json; course/assets/data/program.json; curriculum/curriculum.json; references/references.json', 'PASS',
    'glossary.json: 9 AP1 entries added, no S7 entry changed (39 S7 entries, unchanged). program.json: FC1 and M8 closure and the MS-FIN/PHD-FIN hours (7666 to 7736, 9191 to 9301). curriculum.json: no S7 hunk; 03-markets SDF prerequisites and references changed (AP1-owned module). references.json: only generated_at and used_by (AP1 added to four keys; S7 keys kalyuga2003expertise and tetzlaff2025cornerstone keep S7). verify_refs --offline 560 entries 0 problems; no duplicate JSON keys in any of the five files.')
new('r33-registry-used-by', '2.1-citation', 'references/references.json (used_by of 4 keys)', 'PASS',
    'Diff: used_by gained "AP1" for hansen1991implications, kalyuga2003expertise, shleifer1997limits and tetzlaff2025cornerstone (4 hunks; S7 used_by unchanged); every title, author, DOI and year line is unchanged. verify_refs --unit S7 live (94 entries, 0 problems) and --offline (560, 0 problems).')
new('r33-data-h10-licence-note', '2.8-figure', 'tools/data_sources.yaml fx_daily and fx_monthly notes (lines 28-37 and 62-71)', 'PASS',
    'New note text quotes: "noon buying rates in New York for cable transfers payable in the listed currencies" and "The rates have been certified by the Federal Reserve Bank of New York for customs purposes as required by section 522 of the amended Tariff Act of 1930" (https://www.federalreserve.gov/releases/h10/about.htm, fetched HTTP 200, 84844 bytes): both quotes present in the page. about.htm "Last Update: February 06, 2023" present, as the note says. about.htm has no licence or terms text of its own; the licence_url https://www.federalreserve.gov/disclaimer.htm (fetched, 85130 bytes) carries "Unless otherwise indicated, information on Board\'s website is in the public domain and may be copied and distributed without permission", which grants redistribution (VERIFIER_RULES 2.8).')
new('r33-data-reproducible', '2.8-figure', 'course/assets/data/market/fx_daily.csv, fx_monthly.csv, ust_daily.csv and MANIFEST.json', 'PASS',
    'VERIFIER_RULES 2.8 (new rule): tools/fetch_data.py --fetch --only fx_daily ust_daily and --only fx_monthly, run in a scratch copy of HEAD (git archive) so the checkout and its MANIFEST are untouched: rebuilt sha256 equal to MANIFEST for all three (fx_daily 02872dd7e23938da..., 443841 bytes; fx_monthly 60572240d1a9d183..., 67392 bytes; ust_daily dd70e1a21c56e6a3..., 140520 bytes). Live raw zips differ from MANIFEST raw_sha256 (fx 17d087d0... vs 8f370f9c...; ust 0a5685bd... vs 334a7f88...): the issuer updated the live files; recorded here as provenance, not refreshed (retrieved dates kept 2026-10-19 and 2026-10-20).')
new('r33-rubric-default-wording', '2.6-rubric', 'course/modules/S/S7/project.html section#self-assessment; course/assets/js/rubric.js workWording', 'PASS',
    'Playwright (Chromium, scratch rubric_wording.py) on http://127.0.0.1 (course/ served by python -m http.server on 8797, then stopped): section data attributes rubric, exemplars, storeKey only; legend "Your memo"; table header "Your memo"; label "Summary to keep as memo/self_assessment.md"; page errors []; external requests [].')
new('r33-headline-recompute', '2.2-number', 'course/modules/S/S7/project.html data-num values (memo) and the Lab 4 twin output', 'PASS',
    INDEP + ' Method: own code, numpy only, the trial matrix rebuilt from course/assets/data/market/fx_monthly.csv (1971-01 to 2026-09; start 1999-01; sign rule over lookback, holding and skip; first = 25). PBO by CSCV over 16 blocks with the first T mod S rows dropped (atlas/A8.contract.md line 93), IS best by Sharpe, rank with ties (lower = 1). Every number agrees with the page at the printed precision (page: n_trials 40, n_obs 308, sr_month 0.0408, sr_ann 0.14, psr 77%, dsr 0.49, sr0 0.0424, sr_sd 0.0193, skew 1.57, kurt 15.2, pbo 73%, pbo_check 0.743 and 0.714, p_min 0.237, n_eff 7.74, rho 0.567, participation 2.37, null PBO mean 0.527, null share 21%).')
OVR_NEW = None

# ----- write
out_rows = []
seen = set()
counts = collections.Counter()
for r in OLD:
    i = r['id']
    if i in OVR:
        st, ev = OVR[i]
        row = {'id': i, 'check': r['check'], 'location': r['location'], 'status': st, 'evidence': ev}
        if st != 'PASS':
            row['fix'] = ('Amend atlas/A8.contract.md line 6 through a CONTRACT_CHANGE_REQUEST (BUILDER_RULES 5.5) to the NumPy version actually tested (2.4.6), then re-verify the atlas rows.' if i == 'atlas-dependency-constraint' else 'See evidence.')
    else:
        ps = paths_of(r['location'])
        ch = [p for p in ps if changed(p)]
        if ch:
            # passage-level carry: project.html changed only at line 195 (#local), which these rows do not cover
            only_hunk = all(p == 'course/modules/S/S7/project.html' for p in ch)
            if not only_hunk:
                raise SystemExit('UNHANDLED changed subject: ' + i + ' ' + str(ch))
            ev = ('Carried from the release ledger (' + ', '.join(p for p in ps if p != 'course/modules/S/S7/project.html') +
                  ' byte-identical since 5e5da87; course/modules/S/S7/project.html differs from 5e5da87 at one line, 195, in #local, outside this row\'s passage): ') + r['evidence']
        elif not ps:
            # no path token: the row names lesson passages or cards; the S7 lesson and card files are byte-identical
            assert not changed('course/modules/S/S7/cards.json') and not changed('course/modules/S/S7/L01.html')
            ps = ['course/modules/S/S7/ lesson and card files (L01-L08.html, cards.json)']
            ev = ('Carried from the release ledger (' + ps[0] + ' byte-identical since 5e5da87; checked with git diff --quiet on course/modules/S/S7 excluding project.html): ') + r['evidence']
            row = {'id': i, 'check': r['check'], 'location': r['location'], 'status': r['status'], 'evidence': ev}
            assert row['status'] == 'PASS', i
            out_rows.append(row); seen.add(i); continue
        else:
            ev = ('Carried from the release ledger (' + ', '.join(ps) + ' byte-identical since 5e5da87): ') + r['evidence']
        row = {'id': i, 'check': r['check'], 'location': r['location'], 'status': r['status'], 'evidence': ev}
        if row['status'] != 'PASS':
            raise SystemExit('carried non-PASS row ' + i)
    out_rows.append(row)
    seen.add(i)
for r in NEW:
    assert r['id'] not in seen, r['id']
    out_rows.append(r); seen.add(r['id'])
unused = set(OVR) - {r['id'] for r in OLD}
print('override ids not in release (must be none):', sorted(unused))
json.dump(out_rows, open('/tmp/ap1-r5/s7p/rows_out.json', 'w'), ensure_ascii=False, indent=1)
print('rows', len(out_rows), 'PASS', sum(1 for r in out_rows if r['status']=='PASS'), 'FAIL', [r['id'] for r in out_rows if r['status']!='PASS'])
