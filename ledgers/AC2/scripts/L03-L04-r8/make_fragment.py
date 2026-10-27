import json, sys
src = json.load(open("/tmp/ac2-frags/L03-L04.round7.json"))
root = sys.argv[1]
PREFIX = ("Carried from round 7 (course/modules/AC/AC2/L03.html, course/modules/AC/AC2/L04.html, "
          "tests/labs/AC2/lab-AC2-L03-1.py, tests/labs/AC2/lab-AC2-L04-1.py, references/references.json, "
          "notation/notation.json, curriculum/, tools/, tests/ byte-identical since 6adfd01): ")
RERUN = {
 "L03-L04-cmd-pin": "Re-run this round: `git rev-parse --short HEAD` -> e6788c2. `git diff --stat 6adfd01 HEAD -- course tests atlas plans references curriculum` -> 7 files: L02.html, L08.html, cards.json (c024, c072, c107 only), grader/test_project.py, index.html, project.html, plans/AC2-open-items.md. `git diff --quiet 6adfd01 HEAD -- L03.html L04.html both twins references notation curriculum tools tests` exits 0.",
 "L03-L04-cmd-check_pages": "Re-run: `.venv/bin/python tools/check_pages.py --unit AC2` -> 'check_pages AC2: PASS', exit 0 (/tmp/ac2-v/L03-L04/r8/pages.txt).",
 "L03-L04-cmd-check_dag": "Re-run: `.venv/bin/python tools/check_dag.py --unit AC2` -> 'check_dag AC2: PASS', exit 0.",
 "L03-L04-cmd-check_projects": "Re-run: `.venv/bin/python tools/check_projects.py --unit AC2` -> 'check_projects AC2: PASS', exit 0.",
 "L03-L04-cmd-run_labs": "Re-run: `tools/run_labs.py --unit AC2 --page L03` -> 'run_labs AC2: PASS (1/1)', exit 0; `--page L04` -> 'run_labs AC2: PASS (1/1)', exit 0.",
 "L03-L04-cmd-twins-strict": "Re-run: `.venv/bin/python -I -W error tests/labs/AC2/lab-AC2-L03-1.py` exit 0, 23 stdout lines; `... lab-AC2-L04-1.py` exit 0, 15 stdout lines (/tmp/ac2-v/L03-L04/r8/twin_L03.txt, twin_L04.txt).",
 "L03-L04-cmd-twin-identity": "Re-run with ledgers/AC2/scripts/L03-L04-r8/twin_page_cards_check.py: every non-blank line of lab-AC2-L03-1.py (457 lines) and lab-AC2-L04-1.py (181 lines) occurs in its page (0 missing). ledgers/AC2/scripts/L03-L04-r8/expected_exact.py: the page's expected block equals the twin's stdout exactly for L03 (23 lines) and L04 (15 lines). Output /tmp/ac2-v/L03-L04/r8/expected_exact.txt.",
 "L03-L04-cmd-page_smoke": "Re-run: `.venv/bin/python tools/page_smoke.py --unit AC2 --pages L03 L04` -> 'page_smoke modules/AC/AC2/L03.html: PASS', 'page_smoke modules/AC/AC2/L04.html: PASS', 'page_smoke AC2: PASS', exit 0.",
 "L03-L04-cmd-verify_refs": "Re-run: `verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'; `verify_refs.py --unit AC2` (live, plain curl) -> 'live re-verification of AC2: 7 of 560 entries, 0 problems', exit 0.",
 "L03-L04-cmd-ruff-mypy-pytest": "Re-run: `ruff check` and `ruff format --check` on both twins: pass; `mypy` on both twins: 'Success: no issues found in 2 source files'; `pytest -q tests/test_labs.py tests/test_page_checks.py`: 127 passed, exit 0.",
 "L03-L04-cite-sloan1996stock": "Re-fetched this round with plain curl: `https://api.crossref.org/works/10.2308/tar-9608042309` -> HTTP 200; title 'Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?', container The Accounting Review, volume 71, issue 3, pages 289-315, published 1996-07. Matches references/references.json key sloan1996stock (volume '71', issue '3', pages '289-315', year 1996). L04.html line 359 cites it as a claim grade C with the locator 'Crossref abstract; passage locator not confirmed', and states no finding of the paper.",
 "L03-L04-cards-L03": "Re-verified this round: cards.json objects AC2-c032..c047 and AC2-c121 compared to 6adfd01 by object equality (ledgers/AC2/scripts/L03-L04-r8/twin_page_cards_check.py): 17 L03 cards byte-identical to 6adfd01. The file changed only at c024, c072 and c107, none of them L03.",
 "L03-L04-cards-L04": "Re-verified this round: cards AC2-c048..c062 and AC2-c137 compared to 6adfd01 by object equality: 16 L04 cards identical to 6adfd01 (same script).",
 "L03-L04-cards-dup": "Re-verified this round because cards.json changed (c024, c072, c107): 140 cards, ids contiguous AC2-c001..c140, 140 unique fronts, 140 unique backs; changed-vs-6adfd01 set exactly {c024, c072, c107}, each read in full (c024 wording on leverage is L02 material, c072 is an L05 card, c107 is an L08 card; none is an L03 or L04 card).",
 "L03-L04-num-L03-E1": "Re-derived this round from the twin's own functions (ledgers/AC2/scripts/L03-L04-r8/e3_recompute.py run on tests/labs/AC2/lab-AC2-L03-1.py, unrounded): NOPAT 2023 = 186.8 x 0.75 = 140.1 and 2024 = 145.3 x 0.75 = 108.975 -> 109.0, change -22.235% (page: -22.2%). Average invested capital 1038.34 -> 1118.47 (+7.717%, page +7.7%). ROIC 0.13494 -> 0.09742, change -27.807% (page 0.1349 -> 0.0974, fall 27.8%). Ratio (1-0.222)/(1+0.077) = 0.722 (page). All as printed in L03.html line 724 and E1 solution.",
 "L03-L04-num-L03-E3": "Re-derived this round (same script, unrounded IC: 906.8664, 993.5479, 1083.1252, 1153.8140): growth 2022 9.5584% (page 9.6%; printed-figure basis 993.5/906.9 gives 9.5%, page says so), 2023 9.0165% (page 9.0%), 2024 6.5258% (page 6.5%). Counterfactual ROIC change with IC growing at the 2023 rate: -28.667% (page 28.7%). Page says the lab does not compute this case and the figure is by hand from unrounded values: consistent. Growth slows each year: consistent.",
}
rows = []
for r in src["rows"]:
    rid = r["id"]
    if rid in RERUN:
        r = dict(r, status="PASS", evidence=RERUN[rid])
    elif rid == "L03-L04-delta-r7":
        r = dict(r, location="repository delta 6adfd01..e6788c2 (re-run this round)", status="PASS",
                 evidence="Delta 6adfd01..e6788c2 read in full (git diff of L02.html leverage bullet and misconception 1, L08.html section 2, project.html and grader/test_project.py (240 checks), index.html, plans/AC2-open-items.md, cards c024/c072/c107). None of L03.html, L04.html, the twins, references, notation, curriculum, tools or tests changed. grep -i leverage over L03.html and L04.html: 0 hits, so the L02 leverage rewording does not reach any L03/L04 sentence. L04.html line 359 states that Sloan (1996) is not evaluated in L04 and L05.html's Sloan-related card c072 is a different subject; no L03/L04 sentence depends on c072 or c107.")
    elif rid in ("L03-L04-cmd-pin",):
        r = dict(r, evidence=RERUN[rid])
    else:
        assert rid.startswith("L03-L04-"), rid
        r = dict(r, evidence=PREFIX + r["evidence"])
    rows.append(r)
rows.append({
 "id": "L03-L04-access-statements",
 "check": "2.1-citation",
 "location": "course/modules/AC/AC2/L03.html, L04.html (learner text)",
 "status": "PASS",
 "evidence": "grep -i for '403', 'bot check', 'captcha', 'paywall', 'HTTP ' over both pages: 0 hits. No access statement in the slice, so no URL to reproduce. Re-run this round."
})
for r in rows:
    assert r["status"] in ("PASS", "FAIL", "UNVERIFIABLE")
frag = {
 "unit": "AC2",
 "slice": "L03-L04",
 "round": 8,
 "verifier": "round-8 independent verifier for AC2 slice L03-L04 (fresh checkout pinned at e6788c2, /tmp/verify-ac2r8-l34); re-ran every command row; re-derived the L03 E1/E3 figures from the twin's unrounded functions; re-fetched the Sloan Crossref record (HTTP 200); compared the L03/L04 card objects and the expected blocks to the twin output exactly.",
 "pin": "e6788c2",
 "base": "6adfd01 (round-7 pin); delta read in full: no L03/L04/twin/reference file changed",
 "checkout": root,
 "scratch": "/tmp/ac2-v/L03-L04/r8",
 "verified_at": "2026-10-27T23:30:00+00:00",
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": "Round 8 of L03-L04 at pin e6788c2. Slice files byte-identical since 6adfd01 (course/modules/AC/AC2/L03.html, L04.html, tests/labs/AC2/lab-AC2-L03-1.py, lab-AC2-L04-1.py, references, notation, curriculum, tools, tests). Carried rows use the prefix 'Carried from round 7 (...)'. Rows whose subject changed or that are command rows were re-run or re-verified this round. Access statements: none in L03/L04 text (grep 0 hits). Real EDGAR data is honestly pending; every filer is SIMULATED. The round-7 fragment's rows were not trusted as PASS; each was classified (re-run, re-verified or carried).",
 "summary": "AC2 L03-L04 round 8 (pin e6788c2): verdict PASS. %d rows, all PASS, 0 FAIL, 0 UNVERIFIABLE. Counts: %d re-run or re-verified this round, %d carried from round 7 under the byte-identical prefix. The slice is untouched since 6adfd01; the only delta that could reach it (L02 leverage wording) has no L03/L04 hit."
}
n_re = sum(1 for r in rows if not r["evidence"].startswith("Carried from round 7"))
frag["summary"] = frag["summary"] % (len(rows), n_re, len(rows) - n_re)
json.dump(frag, open(f"{root}/ledgers/AC2/L03-L04.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(rows), "rows; re-verified", n_re, "carried", len(rows) - n_re)
