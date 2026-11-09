import json, datetime
ns = {}
exec(open("ledgers/E3/scripts/E3-f-r18/write_fragment_part2.py", encoding="utf-8").read(), ns)
rows = ns["rows"]
from collections import Counter
c = Counter(r["status"] for r in rows)
notes = [
 "Slice scope: course/modules/E/E3/L01.html..L04.html, their lab twins tests/labs/E3/lab-E3-L01-1.py..L04-1.py, and all 178 cards of course/modules/E/E3/cards.json (91 belong to L01-L04). L05-L08 pages, twins, grader and project belong to other slices; they were read only where a card or a notation row depends on them (word-level diff for renames, card text for the 9 changed L05-L08 cards).",
 "Base: round-15 fragment ~/.fanout/frags/D-E3-f.round15.json (pin dde0486b). The round-17 fragment named in the task (~/.fanout/frags/D-E3-f.round17.json) does not exist in ~/.fanout/frags; the latest is round 15, so it is used as the context base and no round-16/17 PASS rows are trusted.",
 "Delta dde0486b..4540351d in scope: L01.html (172 lines), L03.html (12), L04.html (2), cards.json (16 cards changed: E3-c005, c007, c008, c017, c036, c037, c177 in L01-L03, and c078, c080, c100, c104, c105, c107, c116, c143, c145 in L05-L08), lab-E3-L01-1.py (20 lines). L02.html and the L02-L04 twins are byte-identical and their rows are carried with the carry prefix.",
 "Outside the slice, observed and not a row: at 4540351d tests/test_lx1_project_lab3.py::test_a_population_sd_variant_of_the_two_pass_check_raises fails (rc 1; ledgers/E3/scripts/E3-f-r18/out/pytest_e3.out). It is an LX1 test; the E3 and non-LX1 lab subsets pass (pytest_E3_only.out, pytest_lab_not_lx1.out).",
 "No project grader in this slice, so mutants: [] (lab twins are demonstrations per the ruling for project graders only). No mutation runs were made.",
 "Round-15 FAIL E3f-r15-notation-tilde-L03 is resolved: the Theorem 2.1 proof now uses \\check u and the affine \\tilde u in L03 has one meaning.",
 "Observation (not a row): L03 also renames the CRRA exponent a to iota (F2, Definition 1.1, Proposition 1.2 and proof, Proposition 1.7 proof, cards E3-c036, c037, c188). Ruling 33 does not ask for it, but iota is used only in L03 and its cards, so it satisfies ruling 33's letter test.",
 "Observation (not a row): card E3-c106 keeps basis 'Example 2.3'; Proposition 2.1 would be the proved basis (LOW, carried from round 15).",
 "Observation (not a row): Lab 1 of L01 prints the label 'xi' and the twin uses xi; the same letter appears in L02 (\\xi) and project.html. See the FAIL row E3f-r18-notation-ruling33-letters.",
 "Round-15 rows E3f-cmd-pytest-labs and E3f-r15-delta were restated for this round: the pytest row is split into E3-only and non-LX1 subsets (the combined command hits the LX1 failure above); the delta row lists this round's hunks.",
]
verdict = "PASS" if c["FAIL"] == 0 and c["UNVERIFIABLE"] == 0 else "FAIL"
frag = {
 "unit": "E3",
 "slice": "f",
 "round": 18,
 "verifier": "Claude Haiku 5.5, independent verifier for E3-f, round 18 (closing delta; did not build E3)",
 "pin": "4540351dc664559cdfd371b908f2b4e644cf4297",
 "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-15 pin; delta dde0486b..4540351d)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD18-E3-f",
 "scratch": "ledgers/E3/scripts/E3-f-r18/",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": notes,
 "summary": {"rows": len(rows), "pass": c["PASS"], "fail": c["FAIL"], "unverifiable": c["UNVERIFIABLE"]},
}
json.dump(frag, open("ledgers/E3/E3-f.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(frag["summary"], verdict)
