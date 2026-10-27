import json, datetime, collections
rows = json.load(open('/tmp/ap1-r5/s7p/rows_out.json', encoding='utf-8'))
rel = json.load(open('/tmp/ap1-r5/s7p/project_release.json', encoding='utf-8'))
carried = sum(1 for r in rows if r['evidence'].startswith('Carried from the release ledger'))
c = collections.Counter(r['status'] for r in rows)
fails = [r['id'] for r in rows if r['status'] != 'PASS']
notes = (
"Round 33 (unit S7, PROJECT slice): toolchain re-confirmation of the released slice. Verifier: Haiku 5.5, independent of the builders "
"and of rounds 12-17; no build context. Pin 45548c1 (detached checkout /tmp/verify-s7-r1-p; base 5e5da87 'Release S7: unit ledger PASS'). "
"Previous ledger ledgers/S7/project.json (548 rows, all PASS, 164 mutants) read in full before any row was written. "
"Toolchain used for every run here: Python 3.14.8, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2; the in-browser runtime is Pyodide 314.0.7 "
"(Python 3.14.2, numpy 2.4.6, scipy 1.18.0, pytest 9.0.2 per course/assets/vendor/pyodide/pyodide-lock.json). "
"Delta: git diff --stat 5e5da87 HEAD over the slice paths: 55 files, 3205 insertions, 208 deletions. Among S7 files only "
"course/modules/S/S7/project.html changed, at line 195 (the Python/NumPy/pytest sentence in #local); git diff --quiet confirms that the rest of "
"course/modules/S/S7 (excluding project.html), tests/labs/S7, atlas/, benchmarks/S7.md, grader/ and ledgers/S7/mutants are byte-identical. "
"Shared changes checked for S7 relevance: notation (four AP1 symbols; no collision with any S7 page, card, grader, lab or contract, r33-notation-collisions); "
"references.json (generated_at and used_by only; r33-registry-used-by); glossary.json (nine AP1 entries; program.json and curriculum.json "
"have no S7 hunk); tools/data_sources.yaml (H.10 and H.15 licence notes, r33-data-h10-licence-note, proj-data-treasury-licence-recheck); "
"rubric.js (workWording export; S7 defaults equal the old literals, r33-rubric-default-wording); test_memo_exemplars.py, test_figure_kernels.py "
"(tolerance), page_smoke.py (strict KaTeX, preloads), build_site.py (rename), requirements/pyproject/vendor files, and new AP1 files outside this slice. "
"RE-RUN on the new toolchain (outputs in the scratch logs): run_graders --unit S7 --seeds 0-49: 50/50, slowest seed 1.6 s against the 10 s budget. "
"mutate_graders --unit S7 --seeds 0-9: 164/164 killed, 0 survivors; each mutant is killed by the same test name as in the release ledger. "
"run_labs --unit S7: 42/42. page_smoke --unit S7: PASS (project labs at most 1.3 s; in-browser grader 162 pass in 3.1 s against 60 s; zero console errors, external requests or unparsed math). "
"check_pages, check_dag, check_projects --unit S7 and --all: PASS. verify_refs --unit S7 (live): 'live re-verification of S7: 94 of 560 entries, 0 problems'; "
"verify_refs --offline: 'offline integrity: 560 entries, 0 problems'. fetch_data --check: '3 datasets, 0 problems'. "
"tests/test_memo_exemplars.py with tests/test_run_labs.py: 20 passed. Wider slice pytest (page_checks, memo_exemplars, js, docs_figures, labs, figure_kernels, run_labs, fetch_data, page_smoke): 258 passed. "
"ruff check, ruff format --check, mypy strict, render_curriculum --check, build_site --check: PASS. "
"NUMERICS, derived on this toolchain: independent code (numpy only; scratch indep/recompute.py) rebuilt the trial matrix from course/assets/data/market/fx_monthly.csv "
"and recomputed every headline memo number (r33-headline-recompute): T 308, N 40, selected SR 0.0408 (0.14 annualized), PSR 77%, DSR 0.49, SR0 0.0424, "
"SR sd 0.0193, skew 1.57, kurtosis 15.2, PBO 0.733 (16 blocks) with 0.743 (8) and 0.714 (10), min p 0.237, N_eff 7.74, rho 0.567. Every one agrees with the page. "
"test_memo_exemplars re-derives each data-num value from the Lab 3 and Lab 4 twins and the A8 reference (PASS). Lab 4 twin output matches the page (null PBO mean 0.527, share 0.210). "
"DATA (VERIFIER_RULES 2.8, reproducibility): all three snapshots (fx_daily, fx_monthly, ust_daily) rebuild byte-for-byte from the live feed in a scratch copy, sha256 equal to MANIFEST. "
"The live raw zips differ from MANIFEST raw_sha256 (the issuer updated them); recorded as provenance, not refreshed. "
"LICENCE: the MANIFEST licence_url disclaimer.htm (HTTP 200) carries the public-domain grant; the H.10 about.htm quotations in the new note are present, and about.htm has no terms of its own. "
"FAIL: atlas-dependency-constraint. atlas/A8.contract.md line 6 says 'Depends on: NumPy 2.2', but the grader runtime and requirements-dev.txt pin NumPy 2.4.6 and the project page now says 2.4. "
"The contract is frozen, so it was not edited; the fix is a CONTRACT_CHANGE_REQUEST (BUILDER_RULES 5.5). Every other row is PASS. "
f"CARRIED: {carried} rows carry the release evidence on byte-identity of their subject files, with the prefix 'Carried from the release ledger'. A row whose passage sits in project.html says so: that file differs only at line 195, outside the passage. "
"NOT RE-EXECUTED (scratch scripts from earlier rounds are not in this environment): r16-cmd-recheck-refs (abstract re-read), r16-cmd-quiz-all-combos, r17-cmd-blind-extract and r17-cmd-statement-diff are carried on byte-identity of their inputs, which are unchanged; "
"r16-cmd-recheck-outputs, r16-cmd-indep-memo, r17-cmd-prose-sweep, r17-cmd-wordcount, r17-cmd-lemma76-check (Monte Carlo part) and r17-cmd-form-sweep (84-press sweep) are PASS only with the narrower equivalent re-run stated in their evidence. "
"OUT-OF-SLICE OBSERVATIONS (not rows here): BLUEPRINT.md line 356 says 'Python 3.12+' (pyproject requires >=3.14). requirements-dev.txt lists playwright==1.64.1 twice (identical; harmless). "
"pyproject.toml excludes two S7 lab twins from mypy strict (tests/labs/S7/lab-S7-L08-4.py and lab-S7-L03-2.py) for numpy 2.5 stub reasons; they are not type-checked. "
"tests/test_figure_kernels.py relaxes the normCdf pdf tolerance to max(1e-12, 5e-14*(n-1)) with a comment that cites Python 3.15; the test passes on 3.14.8, and the comment's claim was not checked. "
"L01.html line 133 contains 'roughly half a standard deviation', which BUILDER_RULES 2.2 bans unless it meets (a)-(c); it is in the lesson ledger's scope and is carried there."
)
frag = {
 "unit": "S7",
 "slice": "project",
 "round": 33,
 "verifier": "Haiku 5.5, round 33 (independent of the S7 builders and of rounds 12-17); toolchain re-confirmation",
 "pin": "45548c1",
 "base": "5e5da87",
 "previous_ledger": "ledgers/S7/project.json (release, 548 rows, all PASS, 164 mutants; verified on the old toolchain)",
 "checkout": "/tmp/verify-s7-r1-p (detached)",
 "scratch": "/tmp/ap1-r5/s7p/ (logs/, indep/, plug/, web/, fetchcopy/, ws-dual/, starter/)",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "PASS" if not fails else "FAIL",
 "rows": rows,
 "mutants": rel["mutants"],
 "registry_flags": rel["registry_flags"] + ["references.json: used_by gained AP1 for hansen1991implications, kalyuga2003expertise, shleifer1997limits and tetzlaff2025cornerstone (round 33; content unchanged)."],
 "freshness_flags": rel["freshness_flags"],
 "notes": notes,
 "summary": {"rows": len(rows), "pass": c["PASS"], "fail": c["FAIL"], "unverifiable": c["UNVERIFIABLE"],
             "mutants": len(rel["mutants"]), "mutants_killed": len(rel["mutants"]), "fail_ids": fails},
}
json.dump(frag, open('/tmp/verify-s7-r1-p/ledgers/S7/project.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('written', frag['summary'], 'carried', carried)
