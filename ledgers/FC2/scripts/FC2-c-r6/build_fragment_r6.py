import json, re, datetime, sys

PREV = "/Users/billyribeiro/.fanout/frags/S-FC2-c.round5.json"
prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
PREFIX = "Carried from round 5 ({files} byte-identical since the previous pin): "

def strip_old(ev):
    ev = re.sub(r"^Carried from round \d+ \([^)]*\):\s*", "", ev)
    ev = ev.replace("Read this round.", "Read in round 5.")
    return ev

# carried rows: id -> files/lines that are byte-identical since dde0486b
carry = {
 "c-lab-L07-1-hypothesis": "course/modules/FC/FC2/L07.html line 156",
 "c-lab-L08-1-hypothesis": "course/modules/FC/FC2/L08.html line 125",
 "c-lab-L07-1-interpretation": "course/modules/FC/FC2/L07.html line 274 and expected block lines 259-273",
 "c-lab-L08-1-interpretation": "course/modules/FC/FC2/L08.html line 269",
 "c-lab-L07-rounding": "course/modules/FC/FC2/L07.html lines 152 and 166-169; tests/labs/FC2/lab-FC2-L07-1.py",
 "c-lab-L08-bracket-claim": "course/modules/FC/FC2/L08.html line 121; tests/labs/FC2/lab-FC2-L08-1.py lines 70 and 78-82",
 "c-num-L07-M1-M2": "course/modules/FC/FC2/L07.html lines 299-306",
 "c-num-L07-lab-table": "course/modules/FC/FC2/L07.html lines 152 and 259-273",
 "c-num-L07-misconceptions-E1-E2": "course/modules/FC/FC2/L07.html lines 288, 330 and 334",
 "c-num-L07-M3": "course/modules/FC/FC2/L07.html line 310",
 "c-num-L07-E3": "course/modules/FC/FC2/L07.html line 338",
 "c-num-L07-R2": "course/modules/FC/FC2/L07.html lines 345-348",
 "c-num-L08-L-M1": "course/modules/FC/FC2/L08.html lines 57, 251-252, 297 and 329",
 "c-num-L08-table": "course/modules/FC/FC2/L08.html lines 252-263",
 "c-num-L08-E2-E3": "course/modules/FC/FC2/L08.html lines 329 and 333",
 "c-num-L08-M3-halvings": "course/modules/FC/FC2/L08.html lines 269 and 305",
 "c-math-L07-lemmas-1": "course/modules/FC/FC2/L07.html lines 63-76 and 316",
 "c-math-L07-prop1.4-1.5": "course/modules/FC/FC2/L07.html lines 95-115",
 "c-math-L07-cross-refs": "course/modules/FC/FC2/L07.html lines 55, 103, 140, 281 and the cited lines of L04 (58-69, 90), L05 (63-64) and L06 (55-63, 110-141, 320-322); the L04, L05 and L06 files changed in this delta but their hunk headers (L04 51, 111, 120, 136, 240-260; L05 51, 310, 483, 517; L06 171-180) do not reach the cited lines",
 "c-math-L08-lemma2.1": "course/modules/FC/FC2/L08.html lines 67-84",
 "c-math-L08-lemma2.2": "course/modules/FC/FC2/L08.html lines 86-93",
 "c-math-L08-thm2.3": "course/modules/FC/FC2/L08.html lines 55, 96-97 and 104",
 "c-math-L08-prop3.2-bisection": "course/modules/FC/FC2/L08.html lines 108-119",
 "c-math-L08-canon-and-scope": "course/modules/FC/FC2/L08.html lines 121 and 273-276",
 "c-grade-L07": "course/modules/FC/FC2/L07.html lines 86, 358-366 and 369",
 "c-grade-L08": "course/modules/FC/FC2/L08.html lines 55, 356-359 and 362",
 "c-grade-lab-values": "course/modules/FC/FC2/L07.html line 369; course/modules/FC/FC2/L08.html line 362; cards FC2-c109, c110, c111, c117 and c129",
 "c-hours-L07-L08": "course/modules/FC/FC2/index.html (not in this delta); course/modules/FC/FC2/L07.html lines 2 and 34; course/modules/FC/FC2/L08.html lines 2 and 34",
 "c-card-02-c109-c117": "cards.json objects FC2-c109 to c117 and the lesson lines they cite",
 "c-card-03-c118": "cards.json object FC2-c118 and L07 lines 305-306",
 "c-card-04-c119-c131": "cards.json objects FC2-c119 to c131 (except none changed) and the L08 lines they cite",
 "c-card-05-c145-c151-c152-c167": "cards.json objects FC2-c145, c151, c152, c167 and L07 Section 4 line 279, L08 lines 108-119",
 "c-card-06-c182-c183": "cards.json objects FC2-c182 and FC2-c183 and L07 lines 90-91, L08 line 274",
}

FILES_NOTE = "the carried subject lines and cards are byte-identical since the previous pin"

fresh = {}
fresh["c-gate-check-pages"] = ("PASS", "2.9-structure-prose",
 "tools/check_pages.py --unit FC2; --unit FC2 --page L07; --unit FC2 --page L08; --all",
 "Run at pin e896b7a4: 'check_pages FC2: PASS' (exit 0); 'check_pages FC2 L07: PASS' (exit 0); 'check_pages FC2 L08: PASS' (exit 0); --all exit 0 with 27 PASS lines and no FAIL (scripts/FC2-c-r6 check_pages_unit.out, check_pages_L07.out, check_pages_L08.out, check_pages_all.out).")
fresh["c-gate-check-dag"] = ("PASS", "2.6-dag", "tools/check_dag.py --unit FC2",
 "Run at e896b7a4: 'check_dag FC2: PASS', exit 0 (scripts/FC2-c-r6 check_dag_unit.out). The delta adds no concept link or dfn to L07 or L08.")
fresh["c-gate-check-projects"] = ("PASS", "2.9-structure-prose", "tools/check_projects.py --unit FC2",
 "Run at e896b7a4: 'check_projects FC2: PASS', exit 0 (scripts/FC2-c-r6 check_projects_unit.out). project.html changed in the delta (one lede sentence); the check passes.")
fresh["c-gate-run-labs"] = ("PASS", "2.2-labs", "tools/run_labs.py --unit FC2 --page L07; --page L08; --unit FC2",
 "Run at e896b7a4: 'run_labs FC2: PASS (1/1)' for L07 and for L08; 'run_labs FC2: PASS (11/11)' for the unit; all exit 0 (scripts/FC2-c-r6 run_labs_L07.out, run_labs_L08.out, run_labs_unit.out).")
fresh["c-gate-pytest-labs"] = ("PASS", "2.2-labs", "tests/test_labs.py -k 'FC2 and (L07 or L08)' -rA",
 "PASSED tests/test_labs.py::test_lab_runs_and_matches_its_page[lab-FC2-L07-1] and [lab-FC2-L08-1]; exit 0 (scripts/FC2-c-r6 pytest_labs.out).")
fresh["c-gate-pytest-tooling"] = ("PASS", "2.2-labs", "tests/test_page_checks.py tests/test_run_labs.py",
 "pytest -q on the two files: 47 passed (dots only, no failures), exit 0 (scripts/FC2-c-r6 pytest_tooling.out). The delta touches no tool.")
fresh["c-gate-ruff"] = ("PASS", "2.4-math-notation", "ruff check . ; ruff format --check .",
 "'All checks passed!' (exit 0, ruff_check.out); '554 files already formatted' (exit 0, ruff_format.out).")
fresh["c-gate-mypy"] = ("PASS", "2.2-labs", "mypy --no-incremental (full repository; includes the two twins)",
 "'Success: no issues found in 385 source files', exit 0 (scripts/FC2-c-r6 mypy_full.out).")
fresh["c-gate-verify-refs"] = ("PASS", "2.1-citations", "tools/verify_refs.py --offline; tools/verify_refs.py --unit FC2 (live)",
 "Offline: 'offline integrity: 560 entries, 0 problems', exit 0; live FC2: 'live re-verification of FC2: 4 of 560 entries, 0 problems', exit 0 (scripts/FC2-c-r6 verify_refs_offline.out, verify_refs_unit_live.out). references/references.json is byte-identical since dde0486b.")
fresh["c-gate-page-smoke-L07"] = ("PASS", "2.9-structure-prose", "tools/page_smoke.py --unit FC2 --pages L07 (run with L08; Chromium, Pyodide)",
 "'page_smoke modules/FC/FC2/L07.html: PASS'; 'page_smoke FC2: PASS' (scripts/FC2-c-r6 page_smoke.out).")
fresh["c-gate-page-smoke-L08"] = ("PASS", "2.9-structure-prose", "tools/page_smoke.py --unit FC2 --pages L07 L08 (Chromium, Pyodide)",
 "'page_smoke modules/FC/FC2/L08.html: PASS'; 'page_smoke FC2: PASS' (scripts/FC2-c-r6 page_smoke.out).")
fresh["c-lab-L07-1-twin"] = ("PASS", "2.2-labs", "tests/labs/FC2/lab-FC2-L07-1.py; course/modules/FC/FC2/L07.html lines 157-273",
 "Twin byte-identical since dde0486b (not in the delta). Run alone: 'python -I -W error tests/labs/FC2/lab-FC2-L07-1.py' exit 0 (scripts/FC2-c-r6 twin_L07_isolated.out). run_labs L07 PASS, so the page code equals the twin and the expected block equals the output.")
fresh["c-lab-L08-1-twin"] = ("PASS", "2.2-labs", "tests/labs/FC2/lab-FC2-L08-1.py; course/modules/FC/FC2/L08.html lines 126-268",
 "Twin byte-identical since dde0486b. Run alone under python -I -W error: exit 0; the output rejects 4.00, 100.00 and 120.00 with the no-arbitrage message and prints 37 halvings for every case (scripts/FC2-c-r6 twin_L08_isolated.out). run_labs L08 PASS.")
fresh["c-lab-L07-1-hypothesis"] = None
fresh["c-num-L08-R2"] = ("PASS", "2.1-numbers-unrounded", "course/modules/FC/FC2/L08.html lines 340-343 (R2 problem and solution, line 343)",
 "Re-verified this round after the delta changed line 343. The sentence now reads 'a one-cent quote error moves the implied volatility by about 0.0266 volatility points (0.000266) to first order'. Recompute (scripts/FC2-c-r6 recompute_fc2c_r6.out): dC/dsigma = 100 phi(0.35) = 37.524035; 0.01/37.524035 = 0.000266496 in volatility units = 0.0266496 points, which rounds to 0.0266 at 4 dp and 0.000266 at 6 dp. The displayed-value route (0.01/37.52 = 0.0266525 points, 0.0267) is still given as route one in the same paragraph, and the unrounded route is the one the final sentence uses. The round-5 FAIL (0.0267 against the unrounded 0.000266) is resolved.")
fresh["c-math-L07-tree-lemma2.2-thm2.3"] = ("PASS", "2.3-math",
 "course/modules/FC/FC2/L07.html lines 119-141 (Def 2.1, Lemma 2.2, Thm 2.3 and proof); L06.html lines 64, 140-141, 323",
 "Delta changed L07 line 121 only (Definition 2.1: 'A6 of Lesson 6 holds at each node whenever r > 0 and h < sigma^2/r^2 (Lemma 2.2)'; the previous wording said 'A6 holds'). Checked: L06 line 64 defines A6 as 0 < d < R_f < u; L06 line 323 defines A6' as u, d and R_f fixed across nodes, which Definition 2.1 satisfies by construction. Lemma 2.2 (line 126) is an iff under r > 0 and sigma > 0; the lemma's proof (line 129) is valid. Recompute (recompute_fc2c_r6.out): 20000 random (r, sigma, h) trials give 0 mismatches between 0 < d < R < u and h < sigma^2/r^2 outside 1e-9 of the boundary; at n = 1, 2, 5, 10, 50, 400 both hold. sigma > 0 comes from A7 (L07 lines 90-91), in force in Section 2 and used by Theorem 2.3. Theorem 2.3 (line 134) lists A1-A5 and A7 with r > 0 and h < sigma^2/r^2; its proof's A6 is Lemma 2.2 and its A6' is Definition 2.1, so the statement carries the premises the proof uses, and Theorem 3.3 of L06 (line 140) needs A1, A2, A3, A5, A6 and A6', all supplied. Line 143 (A7' not used by Theorem 2.3) matches the statement. Observations in notes.")
fresh["c-notation-L07-L08"] = ("PASS", "2.4-math-notation", "course/modules/FC/FC2/L07.html and L08.html changed lines (121, 343); notation/notation.json (byte-identical since dde0486b)",
 "The two changed lines introduce no symbol: line 121 uses sigma, r, h, u^(n), d^(n), R^(n), q^(n) and the labels A6, A6' and A7 already defined on the page; line 343 uses phi, sigma, C, S, tau and the volatility-point unit. No symbol is reassigned. A7' is an assumption label following the primed convention of A6' (L06 line 323).")
fresh["c-dag-L07"] = ("PASS", "2.6-dag", "course/modules/FC/FC2/L07.html meta row (line 37), dfn (line 80), links (lines 37, 80, 103, 281)",
 "check_dag FC2 PASS at e896b7a4. The delta adds no concept link or dfn to L07; the changed line 121 contains no link.")
fresh["c-dag-L08"] = ("PASS", "2.6-dag", "course/modules/FC/FC2/L08.html lines 37, 51-69, 341, 395-404; both twins; cards.json FC2-c120",
 "check_dag FC2 PASS at e896b7a4. The delta adds no concept link to L08; the changed line 343 contains no link.")
fresh["c-prose-scope-words"] = ("PASS", "2.7-prose-scope", "L07.html line 121 and L08.html line 343 (the only changed lines of the two pages in this delta)",
 "Both changed sentences read in full. Line 121: 'the same at every node' is backed by the construction of Definition 2.1; 'whenever r > 0 and h < sigma^2/r^2' is backed by the iff of Lemma 2.2. Line 343: 'a one-cent quote error' is an indefinite claim hedged by 'about', 'at these inputs' and 'to first order', and the paragraph names the first-order derivation (Lemma 2.1). No new universal scope word enters the pages.")
fresh["c-prose-process-banned"] = ("PASS", "2.8-process-words", "L07.html and L08.html changed lines (121 and 343) and the lab docstrings of the two twins (unchanged)",
 "grep of the added lines for builder, verifier, round, rule, ledger: the only match is 'round' inside 'unrounded' (line 343), not a process word. 'registry key black1973pricing' (L07 line 86) is unchanged and recorded in registry_flags as before.")
fresh["c-struct-L07"] = ("PASS", "2.9-structure-prose", "course/modules/FC/FC2/L07.html (whole page; the delta hunk at line 121 read in full)",
 "The delta hunk is one line at the same position (hunk header '@@ -118,7 +118,7 @@'), so no section id, cross-reference target or line shift changed. check_pages L07 PASS and page_smoke L07 PASS at e896b7a4. The whole page was not re-read this round (delta protocol).")
fresh["c-struct-L08"] = ("PASS", "2.9-structure-prose", "course/modules/FC/FC2/L08.html (whole page; the delta hunk at line 343 read in full)",
 "The delta hunk is one line at the same position (hunk header '@@ -340,7 +340,7 @@'), no line shift. check_pages L08 PASS and page_smoke L08 PASS at e896b7a4. The whole page was not re-read this round (delta protocol).")
fresh["c-card-01-c099-c108"] = ("PASS", "2.10-cards", "course/modules/FC/FC2/cards.json FC2-c099..c108 (L07), against L07 lines 63-115 and 119-124",
 "Card objects byte-identical to dde0486b (scripts/FC2-c-r6 cards_check_r6.out: 'L07 count prev 22 head 22 identical objects True'). The card that cites the changed line, FC2-c105 ('same values at every node (Definition 2.1)'), still matches Definition 2.1 after the wording change; FC2-c106 ('If and only if h < sigma^2/r^2 (Lemma 2.2)') matches Lemma 2.2 (line 126). c103 and c104 match Prop 1.4 (line 96) and Prop 1.5 (lines 108-112).")
fresh["c-card-numbers"] = ("PASS", "2.10-cards", "cards.json: all L07 (22) and L08 (17) cards against their own lesson text",
 "scripts/FC2-c-r6 card_numbers_in_lesson_r6.py: every numeric token of length two or more in each L07/L08 card (front, back, basis) appears in its lesson file: 'total missing numeric tokens: 0'. scripts/FC2-c-r6 cards_check_r6.out: no card contains 0.0266, 0.0267, 0.000266 or 0.000267. The round-5 non-match (0.0267 in L08 R2) is no longer a card-to-lesson gap; the card numbers were re-derived in round 5 and their lesson lines are unchanged.")
fresh["c-card-duplicates"] = ("PASS", "2.10-cards", "cards.json (all 172 cards)",
 "scripts/FC2-c-r6 cards_check_r6.out: 172 cards (round 5: 171; FC2-c176 removed and FC2-c184, c185 added, all L04/L06), 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs (case-insensitive, whitespace-trimmed).")
fresh["c-card-coverage"] = ("PASS", "2.10-cards", "cards.json L07 (22 cards) and L08 (17 cards) vs BUILDER_RULES section 7 and plan section 10",
 "scripts/FC2-c-r6 cards_check_r6.out: L07 22 cards and L08 17 cards, objects identical to dde0486b; coverage as in round 5 (L07 c099-c118, c145, c182; L08 c119-c131, c151, c152, c167, c183). check_pages reports no 'no cards for' problem.")
fresh["c-ref-L07-L08-black1973"] = ("PASS", "2.1-citations", "L07.html line 86 (claim span, data-cite black1973pricing) and footer line 456; L08.html line 55 and footer line 454; references/references.json key black1973pricing",
 "references/references.json is byte-identical since dde0486b. Registry: journal-article, title 'The Pricing of Options and Corporate Liabilities', authors Black and Scholes, year 1973, container Journal of Political Economy, volume 81, issue 3, pages 637-654, DOI 10.1086/260062. Crossref re-fetched by plain curl this round: https://api.crossref.org/works/10.1086/260062 returned HTTP 200 with the same title, authors, container, volume 81, issue 3, pages 637-654 and type journal-article (scripts/FC2-c-r6 crossref_black1973_r6.json). Publisher page by plain curl https://www.journals.uchicago.edu/doi/10.1086/260062 returned HTTP 403 (curl_black1973_r6.out); https://doi.org/10.1086/260062 returns HTTP 302 to that URL. This is an access statement with a reproduced URL, so the paper text is not read; the pages claim only the attribution.")
fresh["c-assumption-A8-collision"] = ("PASS", "2.4-math-notation", "L07.html and L08.html (whole files); cards.json cards whose lesson is L07 or L08; L03.html lines 66 and 104",
 "grep 'A8' in L07.html and L08.html: 0 matches each (scripts/FC2-c-r6 output recorded in this round's check); no L07 or L08 card contains 'A8' (cards_check output). A8 and A8' remain only in L03 (line 104 and line 66, both unchanged in the delta). The closed-form assumption is A7' everywhere in the L07/L08 pages and cards.")
fresh["c-twin-page-equal"] = ("PASS", "2.2-labs", "tests/labs/FC2/lab-FC2-L07-1.py vs course/modules/FC/FC2/L07.html lines 157-273; tests/labs/FC2/lab-FC2-L08-1.py vs L08.html lines 126-268",
 "run_labs FC2 PASS for L07 and L08 (11/11 for the unit) and pytest test_lab_runs_and_matches_its_page PASS for both labs at e896b7a4. Neither twin is in the delta; the changed lines (L07 121, L08 343) are outside the lab blocks.")

new_row = ("PASS", "1.0-delta-inventory", "git diff --name-only dde0486b e896b7a4 (FC2 slice files); git diff dde0486b e896b7a4 -- course/modules/FC/FC2/L07.html course/modules/FC/FC2/L08.html course/modules/FC/FC2/cards.json",
 "Slice-file hunks: L07.html line 121 (Definition 2.1 wording), L08.html line 343 (R2 solution). cards.json: no object of L07 or L08 changed (scripts/FC2-c-r6 cards_check_r6.out); changed objects are FC2-c046 and c050 (L03), c059 and c060 (L04), c081 and c082 (L06); removed FC2-c176 (L04); added FC2-c184 and c185 (L06). Twins tests/labs/FC2/lab-FC2-L07-1.py and lab-FC2-L08-1.py are not in the delta. references/, notation/, curriculum/ and tools/ are not in the delta. index.html is not in the delta. Changed upstream files in FC2 (L03, L04, L05, L06, the L04 and L06 twins, project.html, grader/test_project.py) and plans/ are outside slice c; their hunks are checked only against the lines this slice cites (see the cross-reference rows).")

order = [r["id"] for r in prev["rows"]]
rows = []
for rid in order:
    old = prev_rows[rid]
    if rid in fresh and fresh[rid] is not None:
        status, check, location, evidence = fresh[rid]
        rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})
    elif rid in carry:
        files = carry[rid]
        rows.append({"id": rid, "check": old["check"], "location": old["location"], "status": old["status"],
                     "evidence": PREFIX.format(files=files) + strip_old(old["evidence"])})
    else:
        raise SystemExit("row not handled: " + rid)
rows.insert(order.index("c-gate-run-labs") + 1, {"id": "c-delta-inventory", "check": new_row[1], "location": new_row[2], "status": new_row[0], "evidence": new_row[3]})

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)) == 63, len(ids)
missing = [i for i in order if i not in ids]
assert not missing, missing
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"

frag = {
 "unit": "FC2",
 "slice": "c",
 "round": 6,
 "round_note": "Round 6 DELTA verification of FC2 slice c (L07-L08, twins, cards) at pin e896b7a4. Previous fragment: /Users/billyribeiro/.fanout/frags/S-FC2-c.round5.json (pin dde0486b, verdict FAIL on c-num-L08-R2). Delta dde0486b..e896b7a4 for the slice: L07.html line 121 (Definition 2.1 wording: 'A6 of Lesson 6 holds at each node whenever ...'), L08.html line 343 (R2 solution: 0.0267 to 0.0266 volatility points, (0.000266)), and cards.json (no L07 or L08 object changed; L03, L04 and L06 objects changed; FC2-c176 removed; FC2-c184 and c185 added). Twins, references/, notation/, curriculum/, tools/ and index.html unchanged. Upstream L03-L06 lessons and the project changed but none of the slice's cited lines is in their hunks.",
 "verifier": "claude-haiku-5-5, independent verifier (round 6; did not build FC2; no shared context with the builders)",
 "pin": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a",
 "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-FC2-c",
 "scratch": "ledgers/FC2/scripts/FC2-c-r6/ (gate outputs, recompute_fc2c_r6.py and .out, cards_check_r6.py and .out, card_numbers_in_lesson_r6.py and .out, crossref and curl outputs, build_fragment_r6.py)",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": prev["registry_flags"],
 "freshness_flags": [
   "Publisher page https://www.journals.uchicago.edu/doi/10.1086/260062 returned HTTP 403 to plain curl again on this round (curl_black1973_r6.out); the paper text was not read. Crossref returned HTTP 200 with matching metadata."
 ],
 "notes": [
   "Commands run at e896b7a4 (outputs in ledgers/FC2/scripts/FC2-c-r6/): check_pages (unit, L07, L08, --all), check_dag (unit), check_projects (unit), run_labs (L07, L08, unit), twins alone under python -I -W error, pytest test_labs (FC2 L07 and L08), pytest test_page_checks and test_run_labs, ruff check and format, mypy --no-incremental, verify_refs offline and live (FC2), page_smoke (L07, L08). All PASS, exit 0.",
   "Mutants: none. Slice c has no grader (lessons, lab twins and cards only); mutation testing does not apply to lab twins (verifier-rules ruling), and run_graders does not apply to this slice.",
   "Observation (not a row): Definition 2.1 (L07 line 121) cites Lemma 2.2 (stated at line 126) as the justification of the A6 sentence, a forward citation of a result. It is not a term used before definition and the sentence is correct; recorded here, not as a FAIL.",
   "Observation (not a row): the Definition 2.1 sentence on A6 states 'r > 0 and h < sigma^2/r^2' without restating sigma > 0, which Lemma 2.2 requires. sigma > 0 is part of A7 (L07 lines 90-91), which Section 2 uses, so the sentence is within the page's standing hypotheses.",
   "Observation (not a row, outside slice c): cards FC2-c184 and c185 (L06) match L06 Definitions 1.2 and 1.1 (L06 lines 63-64 and 58-60). FC2-c046, c050 (L03), c059, c060 (L04), c081, c082 (L06) and the removal of FC2-c176 (L04) are changes in other slices and were not verified here.",
   "Judgement on R2 (L08 line 343): the final sentence states 0.0266 volatility points, which is the unrounded first-order value (0.0266496 points), and it gives (0.000266) in volatility units; the paragraph's displayed-value route (0.0267) is still labelled as the displayed route. This is consistent at the printed precision.",
   "Not checked: the cited paper black1973pricing (publisher page returns HTTP 403 to plain curl; the attribution is recorded as an access statement); a whole-page re-read of L07 and L08 (delta protocol: the changed hunks were read in full and all carried rows cite unchanged lines); page_smoke for other pages and the full pytest suite (only the relevant subsets were run); the L03-L06 and project changes outside the slice."
 ],
 "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": counts["UNVERIFIABLE"]}
}
out = sys.argv[1]
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(out, "a", encoding="utf-8").write("\n")
print("rows", len(rows), counts, verdict)
