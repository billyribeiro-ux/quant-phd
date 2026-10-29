import json
import sys

PIN = "9fd6aedde63046c002ed77af5b5152daf84a3abf"
PREV_PIN = "04626e9"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/C-FC1-a.round5.json", encoding="utf-8"))
CARRY_NOTE = ("Carried from round 5 (cited lines byte-identical since the previous pin 04626e9; the round-6 delta "
              "touches only L01.html 166 and 338, L02.html 50, L03.html 109-110 and 170-173, index.html 166, "
              "cards.json FC1-c030, tests/labs/FC1/lab-FC1-L03-1.py 2-4): ")
NEW = {
    "cmd-check-pages": "Run at 9fd6aed: .venv/bin/python tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (ledgers/FC1/scripts/FC1-a-r6/check_pages.txt).",
    "cmd-check-dag": "Run at 9fd6aed: tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0 (ledgers/FC1/scripts/FC1-a-r6/check_dag.txt).",
    "cmd-page-smoke": "Run at 9fd6aed: tools/page_smoke.py --unit FC1 --pages index/L01/L02/L03 -> 'page_smoke FC1: PASS', exit 0 (ledgers/FC1/scripts/FC1-a-r6/page_smoke.txt). Browser rendering not checked.",
    "cmd-run-labs-L01": "Run at 9fd6aed: tools/run_labs.py --unit FC1 -> 'run_labs FC1: PASS (8/8)', exit 0; covers lab-FC1-L01-1 (ledgers/FC1/scripts/FC1-a-r6/run_labs.txt).",
    "cmd-run-labs-L02": "Same unit run: 8/8 PASS includes lab-FC1-L02-1 (ledgers/FC1/scripts/FC1-a-r6/run_labs.txt).",
    "cmd-run-labs-L03": "Same unit run: 8/8 PASS includes lab-FC1-L03-1 (ledgers/FC1/scripts/FC1-a-r6/run_labs.txt); the L03 twin changed in this round (docstring only) and was re-run.",
    "cmd-twin-alone": "Each twin run alone with python3 -I -W error at 9fd6aed: exit 0 and stderr 0 bytes for L01, L02, L03 (ledgers/FC1/scripts/FC1-a-r6/twin-L0*-1.out, .err). Page vs twin (script run in this round): the embedded code in each lab section equals the twin after stripping the trailing newline (exact string equality differs only by the final newline); the expected block equals the twin output for L01, L02, L03 (identical text).",
    "cmd-ruff": "Run at 9fd6aed: ruff check . -> 'All checks passed!'; ruff format --check . -> '335 files already formatted', exit 0 (ledgers/FC1/scripts/FC1-a-r6/ruff.txt).",
    "cmd-mypy": "Run at 9fd6aed: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 229 source files', exit 0 (ledgers/FC1/scripts/FC1-a-r6/mypy.txt).",
    "cmd-pytest-slice": "Run at 9fd6aed: pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_page_checks.py -> all dots, exit 0 (ledgers/FC1/scripts/FC1-a-r6/pytest_slice.txt).",
    "cmd-verify-refs-live": "Run at 9fd6aed: tools/verify_refs.py --unit FC1 -> 'live re-verification of FC1: 2 of 560 entries, 0 problems', exit 0 (ledgers/FC1/scripts/FC1-a-r6/verify_refs.txt).",
    "grep-scope-words-L03": "Fresh on the changed hunks: L03.html 109-110 'Under A1 to A3, suppose a sequence is closed ... every trade happens at the same mid m' - 'every' is the explicit same-mid hypothesis of the statement; L03 170-173 docstring 'Each check is exact integer arithmetic, not a tolerance test' - no float or tolerance code in tests/labs/FC1/lab-FC1-L03-1.py (grep for float/isclose/abs: no match) and no decimal in twin-L03-1.out (grep '[0-9]\\.[0-9]': no match). Unchanged occurrences carried.",
    "banned-phrases-and-process-words": "grep of the added lines of the 04626e9..9fd6aed delta restricted to course/modules/FC/FC1/{index,L01,L02,L03,cards}.* and tests/labs/FC1/lab-FC1-L0{1,2,3}-1.py for builder/verifier/round/fragment/TODO/placeholder/fixed/agent: no match in slice files (ledgers/FC1/scripts/FC1-a-r6/slice_delta_04626e9_to_9fd6aed.diff). Matches exist only in out-of-slice L04/L05/project files.",
    "hub-core-reading-registry": "Re-verified: index.html line 166 now reads 'A Bank of England article listed among the curriculum's sources for FC1 (McLeay, Radia & Thomas, 2014) is not yet in the registry'. Curriculum source: curriculum/02-economics-finance-core.yaml line 386 '- \"McLeay, Radia & Thomas (2014), Bank of England Quarterly Bulletin Q1\"' inside the FC1 block (id FC1 at line 363). references/references.json: 0 matches for 'mcleay'; references/review_queue.json contains it (so 'not yet in the registry' holds). No lesson cites it (grep 'Bank of England|McLeay' in FC1 lesson HTML: none). verify_refs PASS above. Hub registry keys lines 164-171 unchanged otherwise.",
    "L01-prop4.1": "Re-verified: L01.html lines 149-167; line 166 (Remark 4.2) now 'This lesson states no legal or regulatory rule.' The proposition, proof (161) and assumption (150-156) are unchanged; the remark makes no numerical claim.",
    "L01-canon-breaks-misconceptions": "Re-verified: L01.html line 338 misconception now 'Listing equity as an asset as well as the residual would count it twice in the identity of Remark 1.2, because equity is already assets minus liabilities.' Remark 1.2 (line 63-64) states assets = liabilities + equity by definition, so the double-count reasoning is correct. Lines 315-341 otherwise unchanged.",
    "L03-cor2.4-prop2.3-P1-P2": "Re-verified: L03.html 108-110: Corollary 2.4 now 'Under A1 to A3, suppose a sequence is closed, I = 0, and every trade happens at the same mid m. Then P = C = s Q.' The proof (line 112-115 region, unchanged) uses A1 (p_t = m_t + sigma_t h) and I=0 to give C = hV = sQ with V = 2Q; the hypotheses now match what the proof uses. P1-P2 at 396-413 unchanged.",
    "L03-lab1-expected-vs-output": "Re-verified: the L03 lab docstring (embedded in the page at L03.html 169-175 and twin tests/labs/FC1/lab-FC1-L03-1.py) changed only in wording (exact integer arithmetic). Page code equals twin (after trailing-newline strip) and expected block equals twin output (ledgers/FC1/scripts/FC1-a-r6/twin-L03-1.out). Twin runs alone with -W error, exit 0.",
    "cards-L02-scan": "Re-verified: FC1-c030 back now reads 'Yes, on a hand reading of register entries 1 (cash, exchange), 3 (derivative, exchange), 4 (cash, OTC) and 6 (derivative, OTC) of the Lab 2 code. Lab 2 prints no cross-tabulation, so the claim rests on that hand reading, and the key-results table grades it C.' The key-results row at L02.html line 407 reads 'The four combinations of form and venue all occur in the register (Example 3.1)' with data-grade C and the basis 'a hand reading of register entries 1, 3, 4 and 6'. The card's grade (C) and basis match that row; the card no longer says Example 3.1 itself is graded (the R5 defect). Card grade field C and basis field match.",
    "cards-duplicates-and-numbers": "Re-run at 9fd6aed on course/modules/FC/FC1/cards.json: 111 cards, no duplicate ids; 71 cards for L01-L03 (the single-line change is the back of FC1-c030, count unchanged).",
    "L01-remark-hub-grade-row": None,
}


def carry(row, text):
    return dict(row, evidence=CARRY_NOTE + row["evidence"]) if text is None else dict(row, evidence=text)


rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid == "cards-L02-scan":
        rows.append(dict(r, status="PASS", evidence=NEW[rid], location="course/modules/FC/FC1/cards.json FC1-c030 (back); L02.html line 407 (key-results row)"))
        continue
    if rid in NEW and NEW[rid] is not None:
        rows.append(dict(r, status="PASS", evidence=NEW[rid]))
        continue
    if r["status"] != "PASS":
        raise SystemExit("unexpected non-PASS carried row " + rid)
    rows.append(dict(r, evidence=CARRY_NOTE + r["evidence"]))

rows.append({
    "id": "delta-L01-remark4.2-wording",
    "check": "2.9-prose",
    "location": "course/modules/FC/FC1/L01.html line 166 (Remark 4.2)",
    "status": "PASS",
    "evidence": "Changed hunk read: 'This lesson states no legal or regulatory rule.' The remark asserts no number and no fact about a regime; Assumption 4.0 and Proposition 4.1 (lines 150-161) are unchanged.",
})
rows.append({
    "id": "delta-L02-why-it-matters-def-pointer",
    "check": "2.9-prose",
    "location": "course/modules/FC/FC1/L02.html line 50 (why-it-matters)",
    "status": "PASS",
    "evidence": "Changed sentence: '... proves the counting rule that makes the taxonomy usable in a register (Definition 2.1).' Definition 2.1 (L02 line 91) is the instrument taxonomy and is what the counting rule (Proposition 2.5, line 117) applies to; the parenthetical points at the taxonomy, not a new claim. Non-blocking note: the counting rule itself is Proposition 2.5.",
})
rows.append({
    "id": "delta-L03-docstring-twin-page",
    "check": "2.5-labs",
    "location": "tests/labs/FC1/lab-FC1-L03-1.py lines 2-8 and course/modules/FC/FC1/L03.html lines 169-175",
    "status": "PASS",
    "evidence": "Twin and page docstring both read 'Each check is exact integer arithmetic, not a tolerance test.' Checked against the code: no float, isclose or abs tolerance in the twin (grep), and the output contains no decimal. The expected block's data-tolerance attribute is a run-time comparison setting, not a claim in the prose; it is not contradicted because the output has no non-integer value. Page code equals twin after trailing-newline strip (ledgers/FC1/scripts/FC1-a-r6/).",
})

fragment = {
    "unit": "FC1",
    "slice": "FC1-a",
    "round": 6,
    "verifier": "Haiku independent verifier, FC1-a round 6 (did not build FC1; read verifier-rules.md; computed the 04626e9..9fd6aed slice delta and read every changed hunk; re-verified the round-5 FAIL and every row whose cited lines changed; re-ran every command row)",
    "pin": PIN,
    "base": "04626e9 (round-5 pin). Slice delta 04626e9..9fd6aed: course/modules/FC/FC1/{L01,L02,L03,index}.html, cards.json (FC1-c030 only), tests/labs/FC1/lab-FC1-L03-1.py. Full slice delta saved at ledgers/FC1/scripts/FC1-a-r6/slice_delta_04626e9_to_9fd6aed.diff.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC6-FC1-a",
    "scratch": "/tmp/fc1a-r6/",
    "verified_at": "2026-10-29T00:00:00+00:00",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. The slice is the hub and lessons (plus L03 twin); mutate_graders is not applicable (verifier rules: lab twins are demonstrations, and this slice has no project grader).",
        "Round-5 FAIL cards-L02-scan is cleared: FC1-c030 no longer says Example 3.1 is graded C; the grade sits on the key-results row (L02.html line 407), and the card's grade and basis match it.",
        "Out of slice, not verified here: L04/L05, project.html, grader/test_project.py and their labs changed in the same range (9fd6aed); they belong to slices b/c.",
        "Could not check: rendered layout, console and screenshot of the hub and lessons (page_smoke prints only a unit summary); a live fetch of the McLeay, Radia & Thomas (2014) article (not needed: the hub cites only the curriculum yaml and the registry state, both read locally).",
        "Carried rows: rows whose cited lines are outside the round-6 delta carry the round-5 evidence with the carry prefix; the cited subjects are byte-identical at the line level (hunks listed in the base field).",
    ],
    "summary": "",
}
fragment["summary"] = ("Slice FC1-a round 6 at 9fd6aed: %d rows, %d PASS, %d non-PASS. Round-5 FAIL cards-L02-scan cleared. "
                        "Delta hunks (L01 166/338, L02 50, L03 109-110/170-173, index 166, c030, L03 twin docstring) read and re-verified; no new defect found."
                        % (len(rows), sum(r["status"] == "PASS" for r in rows), sum(r["status"] != "PASS" for r in rows)))
out = "/Users/billyribeiro/.fanout/wt/verifyC6-FC1-a/ledgers/FC1/FC1-a.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, len(rows), fragment["verdict"])
