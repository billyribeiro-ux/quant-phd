import json, subprocess
C = "/Users/billyribeiro/.fanout/wt/verifyB17-M3-c"
S = "ledgers/M3/scripts/M3-c-r17"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/B-M3-c.round16.json"))
CARRY = "Carried from round 16 (cited lines byte-identical since 5e88c50; the 5e88c50..86c4a0b hunks touch only L07.html 201, 207 and cards.json entries listed in the notes): "
RE = "Re-verified in round 17 (5e88c50..86c4a0b hunks read): "
over = {}
def row(i, status, ev, check=None, loc=None):
    over[i] = (status, ev, check, loc)
row("GATE-01", "PASS", f"check_pages.py --all: M3 line 'check_pages M3: PASS' (log {S}/check_pages.log, exit 0)")
row("GATE-02", "PASS", f"check_dag.py --all: 'check_dag M3: PASS' (log {S}/check_dag.log, exit 0)")
row("GATE-03", "PASS", f"build_site.py --check: 'site data current: 6 outputs', exit 0 ({S}/build_site.log)")
row("GATE-04", "PASS", f"render_curriculum.py exit 0; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json exit 0 ({S}/render.log, {S}/render_diff.log)")
row("GATE-05", "PASS", f"run_labs.py --unit M3: 'run_labs M3: PASS (12/12)', exit 0 ({S}/run_labs_M3.log)")
row("GATE-06", "PASS", f"page_smoke.py --unit M3 --pages L07 L08 L09: 'page_smoke M3: PASS', each page PASS, lab timings 0.0 s ({S}/page_smoke.log)")
row("GATE-07", "PASS", f"ruff check . exit 0; ruff format --check '358 files already formatted', exit 0 ({S}/ruff.log)")
row("GATE-08", "PASS", f"mypy --no-incremental: 'Success: no issues found in 255 source files', exit 0 ({S}/mypy.log)")
row("GATE-09", "PASS", f"pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_docs_figures.py tests/test_page_smoke.py: 100% dots, exit 0 ({S}/pytest_labs_docs.log)")
row("GATE-10", "PASS", f"verify_refs.py --offline: '560 entries, 0 problems', exit 0 ({S}/verify_refs.log)")
row("GATE-11", "PASS", f"fetch_data.py --check: '3 datasets, 0 problems', exit 0 ({S}/fetch_data.log)")
row("GATE-12", "PASS", f"check_projects.py --all: 'check_projects M3: PASS', exit 0 ({S}/check_projects.log)")
row("TWIN-01", "PASS", f"python -I -W error on tests/labs/M3/lab-M3-L07-1.py, L08, L09: exit 0 each; L07 stdout equals the 10-line output in {S}/twin_L07.out (includes 'two coefficient vectors that differ by a null direction give the same fitted values: True' and 'rank ... 2 (of 3)')")
row("TWIN-02", "PASS", f"twin_page_check.py (round-16 script re-run, {S}/twin_page_check.log): for L07, L08, L09 data-run code equals twin after html.unescape and expected block equals twin output: all True")
row("MATH-L07-01", "PASS", CARRY + "L07.html:63-96 proofs of Theorem 1.2 and Theorem 1.3 and Remark 1.4; no hunk touches these lines.")
row("MATH-L07-02", "PASS", CARRY + "L07.html:107-121, 322-331 (Theorem 2.2 and proof); not in any hunk.")
row("MATH-L07-03", "PASS", CARRY + "L07.html:232-310, 313-319 (Problems M1, M2, R1); not in any hunk.")
row("NUM-L07-01", "PASS", CARRY + "L07.html:191-200 printed block; the printed coefficients and residual norm are the twin output in twin_L07.out; the changed line 201 is outside the cited range.")
row("NUM-L07-02", "PASS", CARRY + "L07.html:299 unchanged.")
row("NUM-L07-03", "PASS", CARRY + "L07.html:305-306 unchanged; intercept 1.3325 equals beta_0 in twin_L07.out.")
row("MATH-L08-01", "PASS", CARRY + "L08.html is byte-identical to 5e88c50 (git diff 5e88c50 86c4a0b shows no L08 hunk).")
row("MATH-L08-02", "PASS", CARRY + "L08.html byte-identical.")
row("NUM-L08-01", "PASS", CARRY + "L08.html byte-identical; twin_L08.out equals the L08 expected block (twin_page_check.log).")
row("NUM-L08-02", "PASS", CARRY + "L08.html byte-identical; shares in twin_L08.out.")
row("NUM-L08-03", "PASS", CARRY + "L08.html byte-identical.")
row("MATH-L09-01", "PASS", CARRY + "L09.html:73-181 unchanged; the only L09 hunk is line 394.")
row("NUM-L09-01", "PASS", CARRY + "L09.html:52, 98, 346 unchanged; twin_L09.out matches the printed C0 numbers (-0.8, 1.9, 1.9; x^T C0 x = -2.4; squared distance 0.64).")
row("NUM-L09-02", "PASS", CARRY + "L09.html:333-345 expected block equals twin_L09.out (twin_page_check.log).")
row("NUM-L09-03", "PASS", CARRY + "L09.html:441-444, 563-566 unchanged.")
row("NUM-L09-04", "PASS", CARRY + "L09.html:339-341, 346 unchanged; R entries match twin_L09.out.")
row("NUM-L09-05", "PASS", CARRY + "L09.html:180 unchanged; Example 3.6 values re-derived in round 16.")
row("NUM-L09-06", "PASS", RE + "L09.html:394 changed; the 4.88 = 4.84 + 0.04 arithmetic is unchanged and re-derived: A = [[1,1.2],[1.2,1]] has eigenvalues 1 +/- 1.2 = 2.2 and -0.2, and 2.2^2 + 0.2^2 = 4.88 = sum of squared entries 1+1.44+1.44+1. The other cited lines (387-449, 491-497) are unchanged.")
row("NOTATION-01", "PASS", RE + "notation/notation.json unchanged since 5e88c50 (git diff empty); the new L07 line 201 uses only A^{\\top}A, rank and null direction, all already defined in L07.")
row("NOTATION-02", "PASS", RE + "L07 line 201 and L09 line 394 introduce no new symbol; W is not used in the changed sentences.")
row("STRUCT-L07-01", "PASS", RE + "diff 5e88c50..86c4a0b on L07.html shows two changed list/paragraph lines (201, 207); section order s1-s8, canon-breaks, misconceptions and problem tiers unchanged.")
row("STRUCT-L08-01", "PASS", CARRY + "L08.html byte-identical.")
row("STRUCT-L09-01", "PASS", RE + "L09.html diff is one line (394) inside a solution details block; structure unchanged.")
row("DATA-L08-01", "PASS", CARRY + "L08.html byte-identical.")
row("SIM-LABEL-01", "PASS", RE + "lab docstrings in tests/labs/M3/lab-M3-L07-1.py, L09 twin unchanged (lab files not in delta); L07.html:201 still says 'The response is SIMULATED'.")
row("DAG-01", "PASS", RE + "check_dag.py --all: 'check_dag M3: PASS' (log " + S + "/check_dag.log); L07 and L09 meta rows not in the delta.")
row("CROSSREF-01", "PASS", CARRY + "L07.html:75, 207 (207 is an edited sentence, its cross-reference to Theorem 1.2 and Theorem 2.2 unchanged) and 317 unchanged; L09.html:56, 112, 387 unchanged (387 is the M2 problem start, line 394 edited but its cross-reference is to Lemma 1.3 which is still Frobenius-invariance at L09.html:74).")
row("HOURS-01", "PASS", CARRY + "data-hours and eyebrow lines (L07 line 2, 35; L08; L09; index.html) not in the delta; check_pages PASS.")
row("PROSE-01", "PASS", RE + "numbers in the changed prose recomputed: L07 line 201 'rank 2 of 3' (twin_L07.out), 'the coefficients ... 4 decimals' not restated; L09 line 394 4.88 (above). Other prose numbers in L07 125-200 and L09 193-342 unchanged.")
row("GRADE-01", "PASS", RE + "L07 key-results T rows, L08 and L09 key-results (L07.html:342-346; L08.html:428-434; L09.html:484-497) unchanged; grades of the changed cards c119, c123, c134, c136, c192, c194-c196, c200, c201 are T and each back carries the Assuming F1 to F4 marker (card_hyp_r17.py).")
row("ASSUME-01", "PASS", CARRY + "L07.html:209, 292, 299 and L08.html:290 unchanged; markers present.")
row("ASSUME-02", "PASS", CARRY + "L08.html:140-141 and L09.html:98, 116, 123, 139, 185, 187, 364, 417, 451, 460 unchanged (grep 'Assuming F1' in L09 returns the same sites; L09 line 394 is an unmarked-sentence edit that is marked, see MATH row).")
row("ASSUME-03", "PASS", CARRY + "L08.html byte-identical.")
row("ASSUME-04", "PASS", CARRY + "L07.html:265, 272, 317 and L09.html:449, 460 unchanged.")
row("ASSUME-05", "PASS", RE + "L07.html:219 unchanged ('Assuming F1 to F4 of Lesson 4, the residual is orthogonal to the columns of A, not zero'); the canon-breaks item at 209 also carries the marker.")
row("ASSUME-06", "PASS", RE + "previous FAIL resolved. L07.html:201 now reads 'assuming F1 to F4 of Lesson 4, the proofs above cover every full-column-rank design'. grep -n -i 'full-column-rank|full column rank|every full' L07.html returns only lines 201 (marked) and 389 (quiz distractor 'r = 0 whenever A has full column rank', graded wrong by the explanation at line 392 'it is zero only when y is in the column space'). L07.html:207 'Assuming F1 to F4 ... for any A' is marked.")
row("CARD-HYP-01", "PASS", RE + "ids c117-c123, c134-c137, c143-c145, c153-c157, c161, c165, c168: c123, c134, c136 changed; their backs read 'Assuming F1 to F4 of Lesson 4, ...' (cards_refs_r17.log, card_hyp_r17.log: no NO_HYP for these ids). Others unchanged.")
row("CARD-HYP-02", "PASS", CARRY + "cards c142, c153, c158 byte-identical in the delta.")
row("CARD-HYP-03", "PASS", CARRY + "card c127 byte-identical in the delta (round-16 change, not in 5e88c50..86c4a0b).")
row("CARD-C183", "PASS", CARRY + "card c183 byte-identical in the delta.")
row("CARD-C161", "PASS", CARRY + "card c161 byte-identical in the delta.")
row("CARD-C130", "PASS", RE + "card c130 changed (front and back split). Current back: 'The matrix whose rows are the centred rows x~_t = x_t minus the vector of column means. Every column of X~ has mean zero (Section 1).' L08.html:54 'Centred data and the matrix of cross-products' is section 1; no numbers in the card, so the number check is vacuous.")
row("CARD-C138", "PASS", CARRY + "card c138 byte-identical; L08.html:131-133 byte-identical.")
row("CARD-OK-01", "FAIL", RE + "per-card scan (card_hyp_r17.py): every T-graded L07-L09 card whose back cites a Theorem/Proposition/Lemma/Corollary whose lesson statement begins with Assuming F1 carries the marker, EXCEPT that the ungraded cards c198 and c199 cite Definition 1.3 (stated under Assuming F1 to F4 at L08.html, Definition 1.3 block) without the marker. See CARD-HYP-04.", "2.7-cards", "course/modules/M/M3/cards.json ids M3-c198, M3-c199")
row("CARD-DUP-01", "PASS", RE + "cards_refs_r17.py: 201 cards, 201 unique ids, 201 unique fronts.")
row("CLAIM-L07-01", "PASS", RE + "L07.html:219 unchanged; the claim 'the residual is orthogonal to the columns of A' is graded T in Theorem 2.2(c) (L07.html Theorem 2.2 block) and the line carries the marker.")
row("CLAIM-L07-02", "PASS", CARRY + "L07.html:65, 75-80, 90, 316-317 unchanged.")
row("CLAIM-L07-03", "PASS", CARRY + "L07.html:109, 112, 120 unchanged.")
row("REMARK-L08-01", "PASS", CARRY + "L08.html byte-identical.")
row("REMARK-L08-02", "PASS", CARRY + "L08.html byte-identical.")
row("REMARK-L08-03", "PASS", CARRY + "L08.html byte-identical.")
row("PROSE-02", "PASS", RE + "L07.html:201 and 207 and 219 re-read against the twin (null-direction and rank lines, TWIN-01); L09.html:52, 98, 187, 193, 346, 352-353, 372, 496-497 unchanged.")
row("PROCESS-01", "PASS", RE + "grep -n -i -E 'for brevity|obvious|clearly|well known|TODO|TBD|lorem|beyond the scope|roughly|historically' on L07.html, L09.html, cards.json: no matches.")
row("REG-01", "PASS", RE + "notation/notation.json unchanged; verify_refs.py --offline 560 entries, 0 problems.")
rows = []
for r in prev["rows"]:
    i = r["id"]
    if i in over:
        st, ev, chk, loc = over[i]
        rows.append({"id": i, "check": chk or r["check"], "location": loc or r["location"], "status": st, "evidence": ev})
    else:
        raise SystemExit("missing row " + i)
new = {"id": "CARD-HYP-04", "check": "2.7-cards", "location": "course/modules/M/M3/cards.json ids M3-c198, M3-c199 (L08.html Definition 1.3)", "status": "FAIL",
       "evidence": "Definition 1.3 in L08.html opens 'Assuming F1 to F4 of Lesson 4, such a decomposition exists for every real symmetric matrix' and defines the score z_tk = x~_t^T v_k and the explained share s_k = lambda_k / sum lambda_j from that decomposition. Round-16 card c133 carried the marker; the round-17 split created c198 (score) and c199 (share), whose backs cite '(Definition 1.3)' with no 'Assuming F1 to F4' prefix (card_hyp_r17.py NO_HYP lines). Fix: prefix the backs of M3-c198 and M3-c199 with 'Assuming F1 to F4 of Lesson 4,'."}
rows.append(new)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids))
for r in rows:
    if r["id"] == "CARD-OK-01":
        r["evidence"] += " Gated by CARD-HYP-04."
        r["fix"] = "Resolve CARD-HYP-04: prefix the backs of M3-c198 and M3-c199 with 'Assuming F1 to F4 of Lesson 4,'."
    if r["id"] == "CARD-HYP-04":
        r["fix"] = "Prefix the backs of M3-c198 and M3-c199 with 'Assuming F1 to F4 of Lesson 4,'."
nonpass = [r for r in rows if r["status"] != "PASS"]
frag = {
 "unit": "M3", "slice": "c", "round": 17,
 "verifier": "independent Haiku verifier, checkout verifyB17-M3-c",
 "pin": "86c4a0b150b8513c203a247d527436fd8c57cc19", "base": "5e88c5085716527995791d30120edf4facd3cf5a",
 "checkout": C, "scratch": C + "/" + S, "verified_at": "2026-10-29",
 "verdict": "FAIL" if nonpass else "PASS",
 "rows": rows, "mutants": [],
 "registry_flags": [], "freshness_flags": [],
 "notes": ("Delta 5e88c50..86c4a0b (round-16 fix commit) read hunk by hunk: L07.html 201 (ASSUME-06 fix, marker added) and 207 (canon-breaks item rewording); L09.html 394 (M2 solution clause, Lemma 1.3 reference); cards.json: cards edited/split (c025, c031, c034, c050, c063-c065, c067, c082, c119, c123, c130, c133-c134, c136, c175, c182) and added c187-c202 except c191. Every changed card re-checked against its cited lesson block (cards_refs_r17.py, block_text.py: definitions/theorems/sections exist; numbers appear in lesson). Hypothesis check (card_hyp_r17.py) flags only c198 and c199 as real. Labs: three twins re-run under python -I -W error, page-code and expected-block equality re-checked. Re-ran all gates for the slice (GATE rows) and the five targeted pytest suites. Slice c has no project grader, so no grader mutation run; lab twins are demonstrations (ruling), so no lab mutation run. Not checked: full pytest suite (targeted suites only, per changed-only rule); L08.html not re-read line by line (byte-identical, carried); verify_refs without --offline (no live Crossref run; no citation in L07-L09 requires a live check beyond registry keys); the L07 quiz explanations other than the L07q5 explanation (line 392) were not re-derived (not in the delta). Card-level scope: cards not in the delta carried by byte identity of the card entry."),
 "summary": f"M3-c round 17: {len(rows)} rows, {len(rows)-len(nonpass)} PASS, {len(nonpass)} non-PASS ({', '.join(r['id'] for r in nonpass)}). ASSUME-06 from round 16 now PASS. New finding CARD-HYP-04 (c198, c199 lost the F1 to F4 marker in the round-16 card split). All gates PASS fresh.",
}
json.dump(frag, open(C + "/ledgers/M3/M3-c.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(rows), [r["id"] for r in nonpass])
