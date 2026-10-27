"""Build the round-8 L07-L08 fragment from the round-7 fragment (context only; every PASS row is re-judged)."""
import json

SRC = "/tmp/ac2-frags/L07-L08.round7.json"
OUT = "/tmp/verify-ac2r8-l78/ledgers/AC2/L07-L08.json"
frag = json.load(open(SRC))

L07C = "Carried from round 7 (course/modules/AC/AC2/L07.html, tests/labs/AC2/lab-AC2-L07-1.py, references/, atlas/, curriculum/ byte-identical since 6adfd01): "
L08C = "Carried from round 7 (course/modules/AC/AC2/L08.html byte-identical since 6adfd01 except line 93, and tests/labs/AC2/lab-AC2-L08-1.py byte-identical): "
CARDC = "Carried from round 7 (course/modules/AC/AC2/cards.json entries other than AC2-c024, AC2-c072, AC2-c107 byte-identical since 6adfd01): "

FRESH = {
 "L07-L08-cmd-pin": "HEAD e6788c2 (git rev-parse --short HEAD); git status shows only '?? .venv' (symlink). Pin matches the round-8 brief.",
 "L07-L08-cmd-run_labs": "tools/run_labs.py --unit AC2 re-run: 'run_labs AC2: PASS (11/11)', rc 0 (ledgers/AC2/scripts/L07-L08-r8/run_labs.out).",
 "L07-L08-cmd-twins": "python -I -W error tests/labs/AC2/lab-AC2-L07-1.py rc 0 (last lines 'signals unchanged under money x1000: 400/400'); lab-AC2-L08-1.py rc 0 (AND FPR 0.0050, OR FPR 0.1450). Outputs in /tmp/ac2-v/L07-L08-r8/.",
 "L07-L08-cmd-embed": "tools/run_labs.py --unit AC2 PASS (11/11) keeps page and twin in agreement (run_labs covers the @@LAB/@@OUT blocks); embed_labs.py --help confirms the marker contract. The lab twins are byte-identical since 6adfd01.",
 "L07-L08-cmd-page_smoke": "tools/page_smoke.py --unit AC2 --pages L07 L08: 'page_smoke modules/AC/AC2/L08.html: PASS', 'page_smoke AC2: PASS', rc 0; lab-AC2-L08-1 runs in 0.0 s.",
 "L07-L08-cmd-check_pages_dag_projects": "tools/check_pages.py --all: 'check_pages AC2: PASS' rc 0; tools/check_dag.py --all: 'check_dag AC2: PASS' rc 0; tools/check_projects.py --all: 'check_projects AC2: PASS' rc 0.",
 "L07-L08-cmd-lint_mypy": "ruff check on the two twins: 'All checks passed!'; ruff format --check: '2 files already formatted'; mypy --no-incremental on the two twins: 'Success: no issues found in 2 source files'.",
 "L07-L08-cmd-pytest": ".venv/bin/python -m pytest -q -k 'AC2 or ac2 or L07 or L08': rc 0, output ends '[100%]' (ledgers/AC2/scripts/L07-L08-r8/pytest.out).",
 "L07-L08-cmd-verify_refs": "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' rc 0; tools/verify_refs.py --unit AC2 (live): 'live re-verification of AC2: 7 of 560 entries, 0 problems' rc 0.",
 "L07-L08-loc-access-claims-L08": "L08.html line 93 re-read (the only changed line in L08). It records https://doi.org/10.2469/faj.v55.n5.2296 as returning HTTP 302 to https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, which returned HTTP 403: reproduced today by plain curl (ledgers/AC2/scripts/L07-L08-r8/access_check.out). Ivey PDF link HTTP 200; Wikipedia HTTP 200.",
 "L07-L08-loc-beneish-constants-label": "L08.html lines 93 and 95 re-read this round: the constants are labelled UNCONFIRMED, derived from one secondary page, and the 'used only' scope lists the lab, section 3, misconception 2, E1 and quiz 5. Other lines cited (56, 60, 97, 106, 439-443, 530, 566) byte-identical since 6adfd01.",
 "L07-L08-r2-constants-provenance": "L08.html line 93 re-read: the Wikipedia provenance, Scribd and ycharts footnotes, and the DOI access statement match the Wikipedia page and the plain-curl statuses reproduced this round (access_check.out).",
 "L07-L08-r2-wiki-constants": "Wikipedia 'Beneish M-score' fetched by plain curl (HTTP 200, 98385 bytes): the equation '−4.84 + 0.92 × DSRI + 0.528 × GMI + 0.404 × AQI + 0.892 × SGI + 0.115 × DEPI −0.172 × SGAI + 4.679 × TATA − 0.327 × LVGI' appears verbatim; L08.html lines 93 and 115 quote the same nine values. Lab docstring and constants unchanged since 6adfd01.",
 "L07-L08-r3-access": "L08.html line 93 access statuses reproduced by plain curl today: doi.org/10.2469/faj.v55.n5.2296 HTTP 302; tandfonline.com full-text URL HTTP 403; Ivey PDF HTTP 200; Wikipedia HTTP 200 (access_check.out).",
 "L07-L08-r3-wiki-fetch": "Wikipedia 'Beneish M-score' (https://en.wikipedia.org/wiki/Beneish_M-score) fetched by plain curl: HTTP 200. The M-score formula is footnoted '[ 1 ]' to the Scribd reference; 'Scribd' and 'ycharts' appear in the references list; 'The threshold value is -1.78 for the model whose coefficients are reported above' is present.",
 "L07-L08-r3-weights-only-source": "L08.html line 93 re-read: the candidate values come from one secondary web page (Wikipedia, read 2026-10-27), which the fetch above confirms gives all nine values; the lesson labels them unconfirmed (ruling 1, not failed).",
 "L07-L08-r4-wiki-threshold-cite": "Wikipedia threshold sentence re-read: 'The threshold value is -1.78 for the model whose coefficients are reported above. (see Beneish 1999, Beneish, Lee, and Nichols 2013, and Beneish and Vorst 2020)'. L08.html line 97 says it cites 'Beneish 1999' by name with two other works and no page: matches.",
 "L07-L08-r5-card-c107-jstor": "cards.json AC2-c107 back re-read: records the DOI URL, HTTP 302 and HTTP 403 (reproduced by plain curl), and contains no JSTOR statement.",
 "L07-L08-r6-jstor-challenge": "No JSTOR access statement remains in L07.html, L08.html, cards.json or plans/AC2-open-items.md (case-insensitive grep for jstor, bot check, challenge, 403, 302 returns only the Beneish DOI/tandfonline and Ivey/Wikipedia statements re-verified above). The row's subject is removed, so PASS.",
 "L07-L08-r6-wiki-recheck": "Wikipedia 'Beneish M-score' re-fetched today (HTTP 200): nine candidate values and the -1.78 threshold confirmed; L08.html lines 93, 95, 97 and lab docstring lines 114-118 read; UNCONFIRMED labels present.",
 "L07-L08-r7-access-url-recorded": "The round-7 FAIL is fixed: L08.html line 93 and cards AC2-c107 record the DOI URL https://doi.org/10.2469/faj.v55.n5.2296 and the tandfonline URL; plain curl reproduces 302 from the DOI (location https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296) and 403 from that URL today (ledgers/AC2/scripts/L07-L08-r8/access_check.sh and access_check.out). The Piotroski Ivey access statement (L07 line 104) links the PDF, HTTP 200 today. Plans row 16 carries the same URLs and statuses.",
 "L07-L08-r3-open-items-content": "plans/AC2-open-items.md rows 16, 19 and 26 re-read: row 16 records the DOI link, HTTP 302 and tandfonline HTTP 403 (reproduced); UNCONFIRMED and OPEN labels present. git diff 6adfd01 HEAD shows only row 16 changed in that file.",
 "L07-L08-r6-delta-coverage": "git diff --stat 6adfd01 HEAD -- course tests atlas plans references curriculum: 7 files (course/modules/AC/AC2/L02.html, L08.html, cards.json, grader/test_project.py, index.html, project.html; plans/AC2-open-items.md). L07.html, both lab twins, references, atlas and curriculum: unchanged. Slice hunks read: L08.html line 93, cards c107 and plans row 16; the L02, L05-card, project and grader hunks belong to other slices.",
 "L07-L08-cards-dupes": "cards.json (python re-scan this round): 140 entries, ids exactly AC2-c001..AC2-c140, unique; no duplicate front or back text. Entries changed vs 6adfd01: AC2-c024, AC2-c072, AC2-c107 only (none is an L07 card).",
 "L07-L08-cards-L08-A": "cards.json AC2-c107 re-read against L08.html line 93, line 95 and the lab label: grade C, basis naming the Wikipedia secondary page and the UNCONFIRMED label (ruling 1, not failed). Entries c106, c108-c115 and c129 byte-identical since 6adfd01 (scan above).",
 "L07-L08-struct-banned-phrases": "Case-insensitive scan of L07.html and L08.html for 'roughly half', 'about 6%', 'historically', 'this build', 'builder', 'REQUESTS', 'unit report', 'jstor', 'recall': zero hits in both. Two '...' in L07.html are Python annotation and docstring text (tuple[int, ...] and a docstring), not omitted content; zero ellipses in L08.html.",
 "L07-L08-r2-process-words": "L07.html and L08.html re-scanned case-insensitively for 'this build', 'builder', 'REQUESTS', 'unit report': zero hits.",
 "L07-L08-hours": "L07.html data-hours=\"10\", L08.html data-hours=\"12\", index.html data-hours-lessons=\"76\" (unchanged; index.html changed only in the L05 card title).",
 "L07-L08-r3-piotroski-fetch": "Ivey-hosted Piotroski (2000) PDF (https://www.ivey.uwo.ca/media/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf) fetched by plain curl: HTTP 200 (access_check.out). Locators carried from round 7; L07.html unchanged.",
}

def carry(row):
    loc = row["location"]
    if "cards" in loc and "L08" not in loc:
        pref = CARDC
    elif any(k in loc for k in ("L08", "cards", "plans", "open-items")):
        pref = L08C
    else:
        pref = L07C
    row["status"] = "PASS"
    row["evidence"] = pref + row["evidence"]
    return row

rows = []
for r in frag["rows"]:
    if r["id"] in FRESH:
        r["status"] = "PASS"
        r["evidence"] = FRESH[r["id"]]
        rows.append(r)
    else:
        if r["status"] != "PASS":
            raise SystemExit(f"unexpected non-PASS carry row {r['id']}")
        rows.append(carry(r))

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)) == 121, len(ids)
assert set(FRESH) <= set(ids)
fresh_n = len(FRESH)
out = {
 "unit": "AC2",
 "slice": "L07-L08",
 "round": 8,
 "verifier": "round-8 independent verifier for slice L07-L08 (did not build AC2; not the round-7 verifier)",
 "pin": "e6788c2",
 "base": None,
 "previous_ledger": "round 7, pin 6adfd01: 121 rows, 120 PASS, 1 FAIL (L07-L08-r7-access-url-recorded)",
 "checkout": "/tmp/verify-ac2r8-l78 (detached at e6788c2; .venv symlinked)",
 "scratch": "/tmp/ac2-v/L07-L08-r8",
 "archive_scripts": "ledgers/AC2/scripts/L07-L08-r8/ (access_check.sh, build_fragment.py and the .out files)",
 "verified_at": "2026-10-27",
 "verdict": "PASS",
 "mutants": [],
 "registry_flags": frag["registry_flags"],
 "freshness_flags": [],
 "notes": (
  "Round 8 (pin e6788c2). Delta since 6adfd01 for this slice: L08.html line 93 (access sentence now records the DOI URL, HTTP 302 and the tandfonline URL, HTTP 403); cards.json AC2-c107 (same sentence); plans/AC2-open-items.md row 16 (same URLs). L07.html, both lab twins, references, atlas and curriculum are byte-identical since 6adfd01. "
  "The round-7 FAIL L07-L08-r7-access-url-recorded is PASS: plain curl reproduced 302 from https://doi.org/10.2469/faj.v55.n5.2296 with location https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, and 403 from that tandfonline URL (ledgers/AC2/scripts/L07-L08-r8/access_check.out, 2026-10-27). "
  "The Ivey PDF and Wikipedia pages returned HTTP 200. The Wikipedia nine candidate values and the -1.78 threshold were re-grepped verbatim. The Beneish constants stay UNCONFIRMED (ruling 1, not failed). "
  "Not checked: the Beneish (1999) paper text (tandfonline HTTP 403; not bypassed); the Piotroski and Sloan passages beyond the locators read in rounds 6-7. Out of slice: the grader hunk (240 checks) and the L02 and L05-card hunks belong to other slices. "
  "No new defect found in the rewritten sentence: its claims match the reproduced statuses."
 ),
 "summary": f"{len(rows)} rows, 0 FAIL, 0 UNVERIFIABLE: {fresh_n} re-verified this round, {len(rows) - fresh_n} carried from round 7 (hunk-scoped byte-identity, stated per row)",
 "rows": rows,
}
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
print("rows", len(rows), "fresh", fresh_n, "carried", len(rows) - fresh_n)
