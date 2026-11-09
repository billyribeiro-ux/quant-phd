import json, subprocess, datetime, sys
CHECK = "/Users/billyribeiro/.fanout/wt/verifyS9-FC2-c"
base = json.load(open("/Users/billyribeiro/.fanout/frags/S-FC2-c.round6.json", encoding="utf-8"))
out_dir = "ledgers/FC2/scripts/FC2-c-r9/out"
PAGES = "course/modules/FC/FC2/L07.html, course/modules/FC/FC2/L08.html and tests/labs/FC2/lab-FC2-L07-1.py, lab-FC2-L08-1.py"
CARD_PFX = ("Carried from round 6 (course/modules/FC/FC2/cards.json objects of the cited L07/L08 cards identical since "
            "e896b7a4, out/cards_objects_r9.out; L07.html and L08.html byte-identical):")
PAGE_PFX = f"Carried from round 6 ({PAGES} byte-identical since e896b7a4):"

RERUN = {
 "c-gate-check-pages": ("PASS", "Run on 95f3f8cb: `.venv/bin/python tools/check_pages.py --unit FC2` -> 'check_pages FC2: PASS' exit 0; `--unit FC2 --page L07` -> 'check_pages FC2 L07: PASS' exit 0; `--unit FC2 --page L08` -> 'check_pages FC2 L08: PASS' exit 0 (out/check_pages_FC2.out, check_pages_L07.out, check_pages_L08.out). check_cards validates the 194 cards, including FC2-c199, c200 and c207 (ids, lesson, grade, cite keys, per-lesson coverage)."),
 "c-gate-check-dag": ("PASS", "Run on 95f3f8cb: `tools/check_dag.py --unit FC2` -> 'check_dag FC2: PASS', exit 0 (out/check_dag_FC2.out). The delta adds no concept link or dfn to L07 or L08."),
 "c-gate-check-projects": ("PASS", "Run on 95f3f8cb: `tools/check_projects.py --unit FC2` -> 'check_projects FC2: PASS', exit 0 (out/check_projects_FC2.out). project.html and its grader changed in the delta; they are outside slice c."),
 "c-gate-run-labs": ("PASS", "Run on 95f3f8cb: `tools/run_labs.py --unit FC2 --page L07` -> 'run_labs FC2: PASS (1/1)' exit 0; `--page L08` -> 'run_labs FC2: PASS (1/1)' exit 0 (out/run_labs_L07.out, run_labs_L08.out). Expected blocks equal the output."),
 "c-gate-page-smoke-L07": ("PASS", "Run on 95f3f8cb: `tools/page_smoke.py --unit FC2 --pages L07 L08` (Chromium, Pyodide) -> 'page_smoke modules/FC/FC2/L07.html: PASS', 'page_smoke FC2: PASS', exit 0 (out/page_smoke_L07_L08.out). Re-run because the quiz reads cards.json, which changed."),
 "c-gate-page-smoke-L08": ("PASS", "Run on 95f3f8cb: `tools/page_smoke.py --unit FC2 --pages L07 L08` -> 'page_smoke modules/FC/FC2/L08.html: PASS', 'page_smoke FC2: PASS', exit 0 (out/page_smoke_L07_L08.out)."),
 "c-gate-pytest-labs": ("PASS", "Run on 95f3f8cb: `.venv/bin/pytest -q tests/test_labs.py -k 'FC2 and (L07 or L08)'` -> 2 passed (dots only, no failure), exit 0 (out/pytest_labs_L07_L08.out)."),
 "c-gate-pytest-tooling": ("PASS", "Run on 95f3f8cb: `.venv/bin/pytest -q tests/test_page_checks.py tests/test_run_labs.py` -> 47 passed (47 dots, no failure), exit 0 (out/pytest_tooling.out). The two test files and tools/ are byte-identical since e896b7a4."),
 "c-gate-ruff": ("PASS", "Run on 95f3f8cb: `.venv/bin/ruff check .` -> 'All checks passed!' exit 0 (out/ruff_check_repo.out); `.venv/bin/ruff format --check .` -> '555 files already formatted' exit 0 (out/ruff_format_repo.out). Twins alone: ruff check and format --check clean (out/ruff_twins.out)."),
 "c-gate-mypy": ("PASS", "Run on 95f3f8cb: `.venv/bin/mypy --no-incremental` (full repo) -> 'Success: no issues found in 386 source files', exit 0 (out/mypy_repo.out). Twins alone: 'Success: no issues found in 2 source files' (out/mypy_twins.out)."),
 "c-gate-verify-refs": ("PASS", "Run on 95f3f8cb: `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs_offline.out); `tools/verify_refs.py --unit FC2` (live, plain Crossref client) -> 'live re-verification of FC2: 4 of 560 entries, 0 problems', exit 0 (out/verify_refs_FC2_live.out). references/references.json and tools/ are byte-identical since e896b7a4."),
 "c-lab-L07-1-twin": ("PASS", "Isolated run on 95f3f8cb: `.venv/bin/python -I -W error tests/labs/FC2/lab-FC2-L07-1.py` exit 0 (out/twin_L07_exit.out; 15 stdout lines in out/twin_L07.stdout). The twin is byte-identical to e896b7a4 (git diff --quiet empty)."),
 "c-lab-L08-1-twin": ("PASS", "Isolated run on 95f3f8cb: `.venv/bin/python -I -W error tests/labs/FC2/lab-FC2-L08-1.py` exit 0 (out/twin_L08_exit.out). Its stdout (out/twin_L08.stdout) prints the nine-row table with 37 halvings in every row and rejects 0.00, 4.00, 100.00 and 120.00 with the bounds message, as the page's expected block states. Twin byte-identical to e896b7a4."),
 "c-twin-page-equal": ("PASS", "run_labs FC2 PASS for L07 and L08 on 95f3f8cb (out/run_labs_L07.out, run_labs_L08.out); pytest tests/test_labs.py -k 'FC2 and (L07 or L08)' 2 passed (out/pytest_labs_L07_L08.out), which includes test_lab_runs_and_matches_its_page for both labs."),
 "c-delta-inventory": ("PASS", "`git diff --name-only e896b7a4 95f3f8cb -- course/modules/FC/FC2 tests/labs/FC2`: cards.json, L04.html, L05.html, L06.html, project.html, grader/test_project.py, and labs project-1..3. `git diff --quiet e896b7a4 95f3f8cb` on L07.html, L08.html, lab-FC2-L07-1.py and lab-FC2-L08-1.py and index.html is empty, so the slice pages and twins are unchanged. Slice-relevant delta: cards.json (new FC2-c199, c200, c207 for L07/L08; new cards c186-c206 for other lessons; reworded cards c006, c009, c016, c039, c051, c062, c083, c144, c178, c179 for other lessons). No card of L07 or L08 was changed."),
 "c-card-numbers": ("PASS", "out/cards_r9.out: every numeric token of length two or more in each L07 and L08 card (front, back, basis) appears in its lesson file, including the new cards (FC2-c199 tokens 7; FC2-c200 tokens 8, 0, 5, 1; FC2-c207 tokens 1, 5, 7, 0, 2.3, 3.3, 6). Missing tokens: none. Script: scripts/FC2-c-r9/cards_r9.py."),
 "c-card-duplicates": ("PASS", "out/cards_r9.out: 194 cards, ids unique, 0 duplicate fronts, 0 duplicate backs (whitespace and case normalised). Token-Jaccard >= 0.45 pairs: none involves FC2-c199, c200 or c207; the highest L07 pair, c109 and c118, asks different quantities (call value vs put value). Process-word scan (out/process_scope_new_cards.out): the only hits in any card are 'rule' in its trading or mathematical sense (FC2-c062, c132), which is not a process word."),
 "c-card-coverage": ("PASS", "out/cards_objects_r9.out: L07 now 24 cards (c099-c118, c145, c182, c199, c207), L08 now 18 cards (c119-c131, c151, c152, c167, c183, c200). Every previous L07 and L08 object is identical (True). Coverage of the round-6 map is kept, and the three new cards add coverage (FC2-c199 the volatility definition, FC2-c200 the lower bound, FC2-c207 Theorem 2.3)."),
 "c-assumption-A8-collision": ("PASS", "grep -c 'A8' on L07.html and L08.html: 0 and 0 (run this round). The new cards FC2-c199, c200 and c207 contain no 'A8' (out/process_scope_new_cards.out and cards_r9 scan). A8 and A8' remain only in L03."),
 "c-prose-process-banned": ("PASS", "L07.html and L08.html are byte-identical to e896b7a4 (git diff --quiet). Process-word scan of the new cards (out/process_scope_new_cards.out): no builder, verifier, verification, round, ruling, ledger, slice, checkout, pin or rule in FC2-c199, c200 or c207."),
 "c-math-L07-cross-refs": ("PASS", "L07.html lines 55, 103, 140, 281 are byte-identical to e896b7a4. Upstream cited lines: L04.html lines 58-69 and 90 are outside every L04 delta hunk (hunks at 84, 99, 120, 243, 248, 250, 317, 421); L05.html lines 63-64 are outside every L05 delta hunk (hunks at 51, 107, 286, 325, 441, 511); L06.html lines 55-63 are re-read: the only L06 change is line 55, the A2 wording 'the riskless return below' became 'the riskless return \\(R_f\\) of Definition 1.1', and the cited Definition 1.1 (line 58-59) and Theorem 3.3 (lines 140-141) are unchanged. The L06 change adds a forward reference and no content, so the cross-reference statements stand."),
 "c-dag-L07": ("PASS", "out/check_dag_FC2.out: 'check_dag FC2: PASS' exit 0 on 95f3f8cb. L07.html line 37 meta row and the concept links are unchanged (byte-identical)."),
 "c-dag-L08": ("PASS", "out/check_dag_FC2.out: 'check_dag FC2: PASS' exit 0 on 95f3f8cb. L08.html concept links are unchanged (byte-identical), and cards.json FC2-c120 is unchanged in its object."),
 "c-struct-L07": ("PASS", "check_pages L07 PASS and page_smoke L07 PASS on 95f3f8cb (out/check_pages_L07.out; out/page_smoke_L07_L08.out). L07.html is byte-identical to e896b7a4, so no section id or cross-reference target moved."),
 "c-struct-L08": ("PASS", "check_pages L08 PASS and page_smoke L08 PASS on 95f3f8cb (out/check_pages_L08.out; out/page_smoke_L07_L08.out). L08.html is byte-identical to e896b7a4."),
 "c-ref-L07-L08-black1973": ("PASS", "references/references.json is byte-identical since e896b7a4. The black1973pricing registry record (key black1973pricing, doi 10.1086/260062, verified_by crossref, journal-article, Black and Scholes, 1973, Journal of Political Economy 81(3) 637-654) is unchanged. Live re-verification of FC2 this round: 4 of 560 entries, 0 problems (out/verify_refs_FC2_live.out). The paper text is not checked, and the lesson states that it does not check it (L07 line 86; L08 line 55)."),
 "c-notation-L07-L08": ("PASS", "notation/notation.json is byte-identical since e896b7a4 (git diff --quiet). It registers 8 program-wide symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q). L07 and L08 use Phi for the standard normal function (L07 line 64) with the registered meaning; sigma, r, h, tau, V_n, q^(n) and R^(n) are local and defined on the page (L07 lines 121, 136, 149)."),
}

new_rows = [
 {"id": "c9-card-199", "check": "2.10-cards", "location": "course/modules/FC/FC2/cards.json FC2-c199 (new, L07) vs L07.html line 51 (why-it-matters paragraph)", "status": "PASS",
  "evidence": "Card: 'What is the volatility σ of the stock in Lesson 7?' Back: 'The standard deviation of the stock's log return per square root of a year (Lesson 7, introduction).' L07.html line 51 reads 'the stock's volatility \\(\\sigma\\) (the standard deviation of its log return per square root of a year) is constant'. Agrees word for word. The locator 'introduction' names the opening paragraph before Section 1 (the only paragraph before 'Section 1' is line 51); PASS. No grade field, which check_pages allows. Numbers: '7' is a single digit."},
 {"id": "c9-card-200", "check": "2.10-cards", "location": "course/modules/FC/FC2/cards.json FC2-c200 (new, L08) vs L08.html lines 55-58 (Section 1)", "status": "PASS",
  "evidence": "Card: 'What is the lower bound L for a European call in Lesson 8?' Back: 'L = max(S − K e^{−rτ}, 0), the lower bound of Lesson 5 for a European call with the same inputs (Section 1).' L08.html line 55 reads 'The lower bound of Lesson 5 for a European call, with the same inputs, is' and lines 56-58 give L = max(S − K e^{−rτ}, 0). The formula string matches exactly (check in out/cards_r9.out). L05.html lines 59 and 154 keep D = e^{−rτ} and the bound max(S − DK, 0); the L05 lines carrying it are not in the delta. The scope word 'same' refers to the inputs of this lesson and is backed by line 55."},
 {"id": "c9-card-207", "check": "2.4-mathematics", "location": "course/modules/FC/FC2/cards.json FC2-c207 (new, L07) vs L07.html lines 119-122 (Def 2.1), 125-130 (Lemma 2.2), 132-141 (Theorem 2.3 and proof); L06.html lines 111, 138-141 (risk-neutral probability, Theorem 3.3)", "status": "PASS",
  "evidence": "Card: 'Yes. Under A1 to A5 and A7, with r > 0 and h < σ²/r², V_n is e^{−rτ} times the expectation of the payoff max(S_τ − K, 0) under the weights q^(n), which are the tree's risk-neutral probabilities (Theorem 2.3, from Theorem 3.3 of Lesson 6).' Theorem 2.3 (L07 lines 133-137) states V_n = e^{−rτ} Σ_k binom(n,k) (q^(n))^k (1−q^(n))^{n−k} max(S (u^(n))^k (d^(n))^{n−k} − K, 0) under A1, A2, A3, A4, A5 and A7 with r > 0 and h < σ²/r²: the card's formula is that sum read as an expectation under the binomial weights, and its hypotheses match the theorem's statement. The proof (line 140) cites Theorem 3.3 of L06 with N = n and R^(n), giving discount (R^(n))^{−n} = e^{−rτ}. Definition 2.1 (line 121) gives q^(n) = (R^(n) − d^(n))/(u^(n) − d^(n)), the L06 risk-neutral probability q = (R_f − d)/(u − d) (L06 line 111) with R^(n) in place of R_f. Theorem 3.3 of L06 (line 140-141) is the multi-period pricing result with weights as in its Definition 3.2. Key-results row L07 line 366 says the same thing. The grade T is right: the statement is Theorem 2.3, proved on the page, and it rests on L06 Theorem 3.3 (T in L06's key results)."},
 {"id": "c9-card-207-hypotheses", "check": "2.4-hypotheses", "location": "course/modules/FC/FC2/cards.json FC2-c207 back vs L07.html line 134 and line 121, 126", "status": "PASS",
  "evidence": "The hypotheses named in the card (A1 to A5, A7, r > 0, h < σ²/r²) are exactly those of Theorem 2.3 (line 134). A6 and A6′ are not named, and they are not needed in the card: the theorem's proof (line 140) derives A6 at each node from Lemma 2.2 (line 126, which requires r > 0 and σ > 0; σ > 0 is part of A7, line 59). The card does not add or drop a hypothesis."},
 {"id": "c9-card-207-notation", "check": "2.4-notation", "location": "course/modules/FC/FC2/cards.json FC2-c207; notation/notation.json; L07.html lines 121, 136, 149", "status": "PASS",
  "evidence": "Symbols in the card: V_n, q^(n), h, σ, r, τ, K, S_τ and max; Φ is not used in the card. V_n is defined in Theorem 2.3 (line 136) and Definition 3.1 (line 149); q^(n), h, u^(n), d^(n), R^(n) in Definition 2.1 (line 121). notation/notation.json (byte-identical since e896b7a4) registers no symbol with these meanings, so no clash; the registered symbols R_f and Phi are not used with another meaning in the card. Notation rule satisfied."},
 {"id": "c9-card-objects", "check": "2.10-cards", "location": "course/modules/FC/FC2/cards.json (whole file vs e896b7a4)", "status": "PASS",
  "evidence": "out/cards_objects_r9.out (script scripts/FC2-c-r9/cards_objects_r9.py, comparing the e896b7a4 file with 95f3f8cb): L07 prev 22 cards, now 24, all previous objects identical (True), added FC2-c199 and FC2-c207; L08 prev 17, now 18, all previous objects identical (True), added FC2-c200. Changed previous objects are in L01-L04, L06 only (c006, c009, c016, c039, c051, c062, c083, c144, c178, c179), none in L07 or L08."},
 {"id": "c9-upstream-delta", "check": "2.6-DAG", "location": "course/modules/FC/FC2/L04.html, L05.html, L06.html, index.html (delta hunks vs cited lines of L07 and L08)", "status": "PASS",
  "evidence": "git diff -U0 e896b7a4 95f3f8cb: L04.html changes at lines 84, 99, 120, 243, 248, 250, 317, 421 (none in the cited L04 lines 58-69, 90); L05.html changes at lines 51, 107, 286, 325, 441, 511 (none in the cited L05 lines 59, 63-64, 154); L06.html changes at line 55 only (A2 forward reference to R_f of Definition 1.1; content unchanged). index.html is byte-identical. The cited lines of L07 and L08 in these upstream files are unchanged, so every carried cross-reference stands."},
]

rows = []
carried = 0
for r in base["rows"]:
    rid = r["id"]
    if rid in RERUN:
        status, ev = RERUN[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
    else:
        if rid.startswith("c-card") or rid == "c-grade-lab-values" or rid == "c-dag-L08":
            pfx = CARD_PFX
        elif rid == "c-hours-L07-L08":
            pfx = "Carried from round 6 (course/modules/FC/FC2/index.html byte-identical since e896b7a4; L07.html and L08.html byte-identical; the cited hours lines are unchanged):"
        elif rid == "c-math-L07-tree-lemma2.2-thm2.3":
            pfx = "Carried from round 6 (course/modules/FC/FC2/L07.html byte-identical since e896b7a4; cited L06.html lines 64, 140-141, 323 are outside every L06 delta hunk, whose only change is line 55):"
        elif rid in ("c-prose-scope-words",):
            pfx = PAGE_PFX
        else:
            pfx = PAGE_PFX
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": pfx + " " + r["evidence"]})
        carried += 1
rows.extend(new_rows)
assert len({r["id"] for r in rows}) == len(rows)
missing = [k for k in RERUN if k not in {r["id"] for r in base["rows"]}]
assert not missing, missing

frag = {
 "unit": "FC2", "slice": "c", "round": 9,
 "verifier": "Claude Haiku 5.5, independent verifier for FC2-c, round 9 (closing delta; did not build FC2). Protocol: /Users/billyribeiro/.fanout/verifier-rules.md.",
 "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
 "base": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a (round-6 pin; base fragment /Users/billyribeiro/.fanout/frags/S-FC2-c.round6.json, verdict PASS, 63 rows). The file given as the round-8 fragment (S-FC2-c.round8.json) carries round-4 content at pin b276325; it was read as context only and none of its PASS rows were trusted. Its pin is an ancestor of e896b7a4 and the slice pages are byte-identical to e896b7a4, so the round-6 base is the one used for carries.",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyS9-FC2-c",
 "scratch": "ledgers/FC2/scripts/FC2-c-r9/ (scripts and out/ kept in the checkout)",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
 "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "L07.html (458 lines) and L08.html (456 lines) were read in full this round. Delta read in full: cards.json hunks for FC2 L07 and L08 (new objects FC2-c199, c200, c207; no reworded L07 or L08 card), and the L07/L08 pages and twins, which are byte-identical to e896b7a4 (git diff --quiet). The three new cards were checked line by line against L07.html lines 51, 119-141, 140 and L08.html lines 55-58 and the L06 cross-cited lines 111 and 138-141.",
  "Re-run this round on 95f3f8cb (outputs in ledgers/FC2/scripts/FC2-c-r9/out/): check_pages (unit, L07, L08), check_dag, check_projects, run_labs L07 and L08, twins alone under python -I -W error (exit 0), page_smoke L07 L08, pytest test_labs subset (2 passed), pytest test_page_checks and test_run_labs (47 passed), ruff check and format on the repo and on the twins, mypy --no-incremental on the repo (386 files) and on the twins, verify_refs --offline and --unit FC2 (live, 4 entries). All exit 0.",
  "Not re-run (carried, subject byte-identical to e896b7a4): the page-level math, numbers and hours rows for L07 and L08 (the pages did not change); the cards whose objects are identical (cards_objects_r9.out). The twins were run once more; the page-level number checks were not recomputed beyond what run_labs and the carried rows already cover.",
  "Observation, not a row (outside slice c): FC2-c192 (L04) and FC2-c051 (L04) both answer about the strike in different words; not duplicates. FC2-c066 (L05) and FC2-c161 (L05) have token Jaccard 0.78 (ranges of a call and of a put) and are different questions. Other slices own these cards.",
  "Observation, not a row (not a defect): the 'Lesson 7, introduction' locator of FC2-c199 points to the opening why-it-matters paragraph (L07 line 51), which is the only text before Section 1. The wording is precise enough that the card is checked against it.",
  "Not checked: the paper black1973pricing (the lesson states it does not check the text); the project slice, grader and the L01-L06 cards (other slices); mutate_graders and run_graders (slice c has no grader; the page twins are lab demonstrations, so mutation testing does not apply under the verifier-rules ruling); the whole-repo page_smoke (only L07 and L08 were run); the Crossref live run covers the four FC2 entries only, as the FC2 verify command reports.",
 ],
 "summary": "FC2-c round 9: verdict PASS. 63 round-6 ids kept (carried or re-run, none FAIL) plus 7 new rows (c9-card-199, c9-card-200, c9-card-207, c9-card-207-hypotheses, c9-card-207-notation, c9-card-objects, c9-upstream-delta; the L07 and L08 pages were byte-identical). The delta for slice c is three new cards: FC2-c199 (volatility definition), FC2-c200 (lower bound) and FC2-c207 (n-step tree as discounted risk-neutral expectation). All three agree with the current lesson text and carry the theorem's hypotheses; every card number appears in its lesson; no duplicate cards. All gates run on 95f3f8cb exit 0.",
}
json.dump(frag, open("ledgers/FC2/FC2-c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "carried", carried, "verdict", frag["verdict"])
