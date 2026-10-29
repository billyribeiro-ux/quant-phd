"""Assemble the CF8-a round-9 fragment from the round-8 row set plus round-9 re-verification evidence."""
import json
import sys

SCR = "ledgers/CF8/scripts/CF8-a-r9/"
C8 = "Carried from round 8 (course/modules/CF/CF8/index.html byte-identical since the round-8 pin f618cf1): "
C8L1 = "Carried from round 8 (course/modules/CF/CF8/L01.html lines cited here byte-identical since f618cf1; the round-9 hunk is at L01.html:182 only): "
C8L2 = "Carried from round 8 (course/modules/CF/CF8/L02.html lines cited here byte-identical since f618cf1; the round-9 hunk is at L02.html:538 only): "

def row(rid, check, loc, evidence, status="PASS"):
    return {"id": rid, "check": check, "location": loc, "status": status, "evidence": evidence}

rows = [
    row("H-01-structure", "2.9 structure", "course/modules/CF/CF8/index.html:1-172", C8 + "whole hub read in round 8 (sections in BUILDER_RULES §4 order, hours 40 + 10 = 50). check_pages CF8 PASS this round (" + SCR + "check_pages.out)."),
    row("H-02-placement-arithmetic", "2.9 / hours", "course/modules/CF/CF8/index.html:38-41, 69, 81, 86-93, 122-130", C8 + "placement arithmetic re-derived in round 8 (" + SCR + "../../CF8-a-r8/recompute_l02.py is round-8 scratch; the figures are unchanged, index.html is byte-identical)."),
    row("H-03-rubric-wording", "2.9 prose", "course/modules/CF/CF8/index.html:33, 153", C8 + "five criteria, four levels each; project.html:466-473 agrees (read round 8)."),
    row("H-04-closure-links", "2.9 / DAG", "course/modules/CF/CF8/index.html:35-120", C8 + "hub links point only to closure concepts (CF1, M1, AC1, P0.1); check_dag CF8 PASS this round (" + SCR + "check_dag.out)."),
    row("H-05-cmd-check-tools", "command", SCR + "check_pages.out, check_dag.out, check_projects.out", "Re-run this round at pin 33744e5: 'check_pages CF8: PASS' (exit 0); 'check_dag CF8: PASS' (exit 0); 'check_projects CF8: PASS' (exit 0). Outputs in " + SCR + "."),
    row("H-06-process-words", "2.9 prose", "course/modules/CF/CF8/index.html:161, 166; L01.html:182; L02.html:194", "Word-boundary scan this round (grep -w -i 'build|builder|verifier|round|REQUESTS') over index.html, L01.html and L02.html returns no hits. L01.html:182 (changed this round) contains 'rounded' and 'request' only, neither a process word. L02.html:194 is unchanged ('Predicted before running' is a hypothesis label)."),
    row("L01-01-structure", "2.9 structure", "course/modules/CF/CF8/L01.html:1-664", "Round-9 diff for L01.html is one line (182, same line count, so every other line number is unchanged). Section order re-read this round: h2 s1 (53), s2 (71), s3 (115), s4 (149), lab (180), s5 (416), canon-breaks (418), misconceptions (428), problems (446), key results (551), quiz (568), references (649). check_pages CF8 PASS (" + SCR + "check_pages.out)."),
    row("L01-02-numbers", "2.2 numbers", "course/modules/CF/CF8/L01.html:55-146, 362-437, 454-547, 582-645", C8L1 + "the cited ranges exclude line 182; the Part C figures printed in the lab expected block (L01.html:390-412) were re-read and match the exact arithmetic in " + SCR + "recompute_r9.out (release 123287671.2329 cents exact, 123287671 rounded half up, receivables after 1076712328.7671)."),
    row("L01-03-mathematics", "2.4 mathematics", "course/modules/CF/CF8/L01.html:85-168", C8L1 + "no change in the cited range."),
    row("L01-04-remark-1-2-promise", "2.9 cross-reference", "course/modules/CF/CF8/L01.html:68, 97, 112, 154-156", C8L1 + "no change in the cited lines."),
    row("L01-05-lab-1", "2.5 labs", "course/modules/CF/CF8/L01.html:182 (hypothesis), 183-389 (code), 390-412 (expected); tests/labs/CF8/lab-CF8-L01-1.py", "Round-9 hunk changed the hypothesis at L01.html:182: 'printed exactly to four decimals and as whole cents rounded half up'. Verified: twin lines 171-173 print the exact release with 4 decimals (f-string :.4f) and the released cents via to_cents (half up); expected lines show '123287671.2329' and '123287671' (L01.html:397-398). run_labs CF8 PASS 8/8 (" + SCR + "run_labs.out). Twin alone, 'python -I -W error' from an empty directory: exit 0, stderr 0 bytes (" + SCR + "twin-L01-1.out, twin-L01-1.err). Claim now matches the output. recompute_r9.out confirms 123287671.23287672 exact to 8 dp, 4dp .2329."),
    row("L01-06-quiz", "2.9 / 2.7", "course/modules/CF/CF8/L01.html:568-647", C8L1 + "no change in the cited range; check_pages CF8 PASS."),
    row("L01-07-problems", "2.4 mathematics", "course/modules/CF/CF8/L01.html:446-549", C8L1 + "no change in the cited range."),
    row("L01-08-grades-and-claims", "2.3 grades", "course/modules/CF/CF8/L01.html:557-562", C8L1 + "no change in the cited range."),
    row("L01-09-dag-process-words", "2.9 / DAG", "course/modules/CF/CF8/L01.html:37, 55, 117, 146, 182", "Re-verified for line 182 (changed hunk): no link and no dfn in the new text, no process word (word-boundary scan), no undefined concept. Other cited lines unchanged since round 8. check_dag CF8 PASS this round (" + SCR + "check_dag.out)."),
    row("L01-10-why-it-matters-length", "2.9 prose", "course/modules/CF/CF8/L01.html:51", C8L1 + "check_pages CF8 PASS this round enforces the 120-word limit (" + SCR + "check_pages.out)."),
    row("L02-01-structure", "2.9 structure", "course/modules/CF/CF8/L02.html:1-615", "Round-9 diff for L02.html is one line (538, same line count). Section order re-read this round: s1 (53), s2 (99), s3 (116), s4 (165), lab (192), s5 (365), canon-breaks (367), misconceptions (378), problems (396), key results (501), quiz (520), references (601). check_pages CF8 PASS (" + SCR + "check_pages.out); page_smoke L02.html PASS (" + SCR + "page_smoke_CF8_a_r9.out)."),
    row("L02-02-numbers", "2.2 numbers", "course/modules/CF/CF8/L02.html:81, 113, 157, 362, 381-382, 410-419, 455-462, 466-471, 478-480, 523-595", C8L2 + "the one hunk in this range (538) changes the stem's gap wording, not a number. Quiz numbers 37.24, 12.29, 7.89, 41923.36 re-derived exactly in " + SCR + "recompute_r9.out and by the round-8 scripts; the Remark 2.2 figures (lab rows 37.24/44.59, 18.43/20.13, 14.90/15.89, 37.63/44.86) re-derived in recompute_r9.out, compounded > simple in all four rows."),
    row("L02-03-hypothesis-n-missing", "2.4 mathematics / hypotheses", "course/modules/CF/CF8/L02.html:55, 81, 103, 113, 373, 441-444, 544", C8L2 + "Prop 2.1 (line 103) states 'N - k <= 365'; Remark 2.2 (113) and canon (373) carry 'at most 365 days'; quiz item 3 (538) now says 'less than 365 days', which is the strict case of the same proposition (line 544 unchanged)."),
    row("L02-04-why-it-matters-overclaim", "2.9 prose", "course/modules/CF/CF8/L02.html:51", C8L2 + "no change in the cited line."),
    row("L02-05-proofs", "2.4 mathematics", "course/modules/CF/CF8/L02.html:68-192", C8L2 + "no change in the cited range. Prop 2.1 proof re-read in full at 106-109 (h(x) = (1+x)^q - 1 - qx, h' >= 0, strict for q > 1), and recomputed: h = 0 exactly at gap 365 (q = 1), positive at gaps 364, 300, 20 (" + SCR + "recompute_r9.out)."),
    row("L02-06-lab-2", "2.5 labs", "course/modules/CF/CF8/L02.html:192-363 (hypothesis 194, code 195-337, expected 338-361); tests/labs/CF8/lab-CF8-L02-1.py", C8L2 + "the lab twin and its expected block are unchanged. run_labs CF8 PASS 8/8 (" + SCR + "run_labs.out); twin alone under python -I -W error: exit 0, stderr 0 bytes (" + SCR + "twin-L02-1.out, twin-L02-1.err)."),
    row("L02-07-closure-links", "2.9 / DAG", "course/modules/CF/CF8/L02.html:37, 134-147, 157, 194, 382, 412-415, 459, 506", C8L2 + "no change in the cited lines; check_dag CF8 PASS this round."),
    row("L02-08-quiz", "2.7 / 2.3 / 2.4", "course/modules/CF/CF8/L02.html:519-598 (item L02q3 at 537-545; stem line 538)", "Round-8 FAIL resolved. Stem at L02.html:538 now reads 'for a gap of less than 365 days'. Keyed answer (line 541) 'The compounded annual cost' is correct: Prop 2.1 proof gives (1+x)^q - 1 >= qx with strictness for q > 1, and recompute_r9.out shows h(x) > 0 at gaps 364, 300, 20 and h = 0 at 365. The explain (line 544-545) matches. Other items' numbers re-derived in recompute_r9.out (37.24, 7.89, 12.29, 41923.36 via round-8 scripts)."),
    row("L02-09-problems", "2.4 / 2.2", "course/modules/CF/CF8/L02.html:395-498 (R3 at 486-492, solution at 490)", C8L2 + "no change in the cited range."),
    row("L02-10-canon-misconceptions-grades", "2.3 / 2.9", "course/modules/CF/CF8/L02.html:363-393, 500-517", C8L2 + "no change in the cited range; canon bullet (373) carries 'at most 365 days'."),
    row("L02-11-compounding-scope-remark-2-2", "2.2 / 2.4 scope", "course/modules/CF/CF8/L02.html:113", C8L2 + "Remark 2.2 re-read this round in full: 'For a gap of at most 365 days, Proposition 2.1 shows that it is never the larger of the two' (simple figure). Four lab rows at gaps 20, 20, 50, 30 are all at most 365 and compounded > simple in each (recompute_r9.out)."),
    row("NOTATION-01", "2.4 notation", "course/modules/CF/CF8/index.html, L01.html, L02.html (all math)", "Round-9 hunks contain no math (L01.html:182 and L02.html:538 are plain prose, no backslash-delimited expressions). Notation conforms to the round-8 scan of every math expression (" + "round-8 ledger row NOTATION-01). Symbols in the changed text: none."),
    row("DAG-01", "2.9 / DAG", SCR + "check_dag.out; course/modules/CF/CF8/index.html, L01.html, L02.html", "check_dag CF8 PASS this round (exit 0). The round-9 hunks add no link and no concept use."),
    row("CMD-run-labs", "2.5 command", SCR + "run_labs.out, twin-L01-1.out, twin-L02-1.out", "run_labs --unit CF8: 'run_labs CF8: PASS (8/8)', exit 0 (re-run this round). Twins alone under python -I -W error from an empty directory: L01 exit 0, L02 exit 0, stderr empty."),
    row("CMD-page-smoke", "2.9 command", SCR + "page_smoke_CF8_a_r9.out", "page_smoke.py --unit CF8 --pages index L01 L02: 'page_smoke modules/CF/CF8/index.html: PASS', 'L01.html: PASS', 'L02.html: PASS', 'page_smoke CF8: PASS' (exit 0, re-run this round)."),
    row("CMD-verify-refs", "2.1 command", SCR + "verify_refs_offline.out", "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', exit 0 (re-run this round). L01.html:652 and L02.html:603 reference lists are empty, so no citation keys are used in this slice."),
    row("CMD-ruff-mypy-twins", "2.5 command", SCR + "ruff_check.out, mypy.out", "ruff check on both twins: 'All checks passed!'; ruff format --check: 2 files already formatted; mypy --no-incremental on both: 'Success: no issues found in 2 source files' (exit 0, re-run this round)."),
    row("CMD-pytest-subset", "2.5 command", SCR + "pytest_CF8_labs.out", "pytest tests/test_labs.py -k CF8 -q: 8 passed, exit 0 (re-run this round)."),
]

frag = {
    "unit": "CF8",
    "slice": "CF8-a",
    "round": 9,
    "verifier": "Haiku independent verifier, CF8-a round 9 (did not build CF8; no shared context with builders)",
    "pin": "33744e5a",
    "base": "f618cf17 (round-8 pin). Delta f618cf1..33744e5 for slice files: L01.html:182 (lab 1 hypothesis: 'printed exactly to four decimals and as whole cents rounded half up'), L02.html:538 (quiz item L02q3 stem: 'for a gap of at most 365 days' changed to 'less than 365 days'). index.html and lab twins unchanged. cards.json changed but is outside slice a.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC9-CF8-a (detached at 33744e5, .venv symlinked)",
    "scratch": "ledgers/CF8/scripts/CF8-a-r9/",
    "verified_at": "2026-10-29T00:00:00Z",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Lab twins are demonstrations, so mutation testing does not apply (VERIFIER rulings) and mutants is empty. Round-9 hunks read in full: L01.html:182 (checked against twin lines 171-173 and expected lines 397-398) and L02.html:538 (checked against Prop 2.1 at line 103, its proof at 106-109, Remark 2.2 and the lab expected block). Rows whose cited ranges are byte-identical to the round-8 pin are carried with the round-8 prefix; rows whose cited range contains a changed line or the whole file were re-verified this round. Not re-read line by line this round: the unchanged text of index.html, L01.html outside the changed line, and L02.html outside the changed line (carried under the carry rule). cards.json (outside slice a) not checked. project.html and L03-L05 not in this slice. No live verify_refs run (no citations in slice).",
    "summary": "CF8 slice a round 9: 34 rows, PASS=34, FAIL=0. Round-8 FAIL L02-08-quiz resolved (stem now 'less than 365 days', keyed answer correct). Lab 1 hypothesis wording matches the twin output. All command rows re-run at 33744e5 and passing: check_pages, check_dag, check_projects, run_labs (8/8), page_smoke (index, L01, L02), verify_refs --offline (560 entries, 0 problems), ruff, mypy, pytest -k CF8 (8 passed), and the twins alone under -I -W error.",
}

json.dump(frag, open("ledgers/CF8/CF8-a.json", "w"), indent=2, ensure_ascii=False)
print("written", len(rows), "rows")
