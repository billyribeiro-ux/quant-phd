import json, datetime
PREV = "/Users/billyribeiro/.fanout/frags/S-FC2-b.round8.json"
prev = json.load(open(PREV))
LESSON_FILES = ("course/modules/FC/FC2/L04.html, L05.html, L06.html, tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, "
                "lab-FC2-L06-1.py, plans/FC2-build-plan.md, notation/, references/, tools/")
CARD_FILES = "course/modules/FC/FC2/cards.json (cited cards byte-identical), L04-L06 html and twins byte-identical"
def carry(row, files=LESSON_FILES):
    ev = row["evidence"]
    return {"id": row["id"], "check": row["check"], "location": row["location"], "status": "PASS",
            "evidence": f"Carried from round 8 ({files} byte-identical since the previous pin 4540351d): {ev}"}
fresh = {}
def f(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix: r["fix"] = fix
    fresh[id_] = r
G = "ledgers/FC2/scripts/FC2-b-r9/gates_r9.txt"
f("FC2b-cmd-check_pages", "gate", "index, L01-L08, cards.json (unit gate)", "PASS",
  f"Re-run round 9 (cards.json changed in this delta): .venv/bin/python tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS' ({G}).")
f("FC2b-cmd-check_dag", "gate", "L04-L06 links and dfn", "PASS",
  f"Re-run round 9: tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS' ({G}).")
f("FC2b-cmd-check_projects", "gate", "project.html (unit gate, outside slice)", "PASS",
  f"Re-run round 9 (project.html and grader changed in this delta): tools/check_projects.py --unit FC2 -> 'check_projects FC2: PASS' ({G}).")
f("FC2b-cmd-run_graders", "gate", "grader/ (unit gate, outside slice)", "PASS",
  f"Re-run round 9 (grader/test_project.py changed): tools/run_graders.py --unit FC2 -> 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.5 s)' ({G}).")
f("FC2b-cmd-run_labs", "gate", "tests/labs/FC2 (unit, and L04, L05, L06 with --page)", "PASS",
  f"Re-run round 9 (project twins changed): tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)'; --page L04, L05, L06 -> 'PASS (1/1)' each ({G}).")
f("FC2b-cmd-page_smoke", "gate", "L04.html, L05.html, L06.html (each run alone)", "PASS",
  f"Re-run round 9: tools/page_smoke.py --unit FC2 --pages L04 (then L05, L06) -> 'page_smoke modules/FC/FC2/Lnn.html: PASS' and 'page_smoke FC2: PASS' for each alone ({G}).")
f("FC2b-cmd-twins-isolated", "lab", "tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py", "PASS",
  "Re-run round 9: each twin copied alone to a fresh /tmp directory and run with python3 -I -W error: exit 0 and stderr 0 bytes for L04, L05, L06 "
  "(ledgers/FC2/scripts/FC2-b-r9/twin_L04.out, twin_L05.out, twin_L06.out). L05 output: parity cost [0, 0, 0, 0, 0] on the synthetic set; "
  "payoff nonzero at 0 of 40 pairs; planted put error gives -300 cents at 100 USD; planted convexity error gives 3 violated triples, all with the 90 USD call at 9000 cents as the chord-interior point. "
  "L06 output: V0 = 30 = 3000 cents (one period), V0 = 45 = 4500 cents (two periods), self-financing True.")
f("FC2b-cmd-ruff", "gate", "tests/labs/FC2 twins", "PASS",
  "Re-run round 9: .venv/bin/ruff check tests/labs/FC2 -> 'All checks passed!'; ruff format --check -> '11 files already formatted' (gates_r9.txt).")
f("FC2b-cmd-mypy", "gate", "repository mypy configuration", "PASS",
  "Re-run round 9: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 386 source files' (gates_r9.txt).")
f("FC2b-cmd-pytest", "gate", "tests/test_labs.py -k FC2; tests/test_page_checks.py; tests/test_run_labs.py", "PASS",
  "Re-run round 9: .venv/bin/python -m pytest tests/test_labs.py -k FC2 -> 11 PASSED (-rA count 11; collect-only 11). "
  "pytest tests/test_page_checks.py tests/test_run_labs.py -> 47 passed (dot count 47; collect-only test_run_labs.py 6). The quiet run prints no summary line, so the counts are from -rA and collect-only.")
f("FC2b-cmd-verify_refs", "gate", "references/references.json; L04-L06 carry no data-cite", "PASS",
  "Re-run round 9: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (gates_r9.txt). references/ byte-identical to 4540351d.")
f("FC2b-cmd-mutate-standing", "mutation", "tools/mutate_graders.py --unit FC2 (standing set)", "PASS",
  "Run round 9 per ruling 37 (standing set, no new mutants): 'mutate_graders FC2: PASS (111/111 killed)' (gates_r9.txt).")
f("FC2b-cards-c197", "cards", "cards.json FC2-c197 (line 1280; L05, ungraded) vs L05.html:59 (Definition 1.1)", "PASS",
  "Re-verified round 9. The round-8 FAIL cited the result 'It is zero under parity (Definition 1.1; Theorem 1.2)' in this card. The card now reads 'C - P - S + DK, the initial cost of the parity portfolio in the proof of Theorem 1.2 (Definition 1.1).' L05.html:59 says exactly that: 'The difference C - P - S + DK is the initial cost of the parity portfolio in the proof of Theorem 1.2, and Lab 1 calls it the parity cost.' No theorem result is stated, so no hypothesis is owed. The result moved to FC2-c201, which fails (row FC2b-cards-c201).")
f("FC2b-cards-c201", "cards", "cards.json FC2-c201 (line 1286; L05, grade T) vs L05.html:63-64 (Theorem 1.2) and L05.html:67 (proof)", "FAIL",
  "Re-verified round 9 (new card). Front 'Under A3, why is the initial value of the parity portfolio zero?' names only A3. Back: 'The portfolio of Theorem 1.2 has zero payoff in every state.' That step uses A1, A2, A4 and A5 (L05.html:67: the lent cash returns K by A4 and A2, the short share costs S_tau by A1 and A2) and Lemma 1.2 of Lesson 4 (L04.html:76-80). The back ends 'so C - P - S + DK = 0 (Theorem 1.2)', which is the Theorem 1.2 result, graded T. Theorem 1.2 is stated under A1, A2, A3, A4 and A5 (L05.html:64). The card therefore states a theorem result under A3 alone, the same hypothesis omission that failed FC2b-cards-c197 in round 8. The A3 step itself is correct: A3 (L04.html:62) excludes V0 <= 0 with a non-negative payoff, applied to X when V0 < 0 and to -X when V0 > 0.",
  fix="Carry the hypotheses in the front and the back. Front: 'Under A1 to A5, why is C - P - S + DK = 0 (Theorem 1.2)?' Back: 'The portfolio has zero payoff in every state, by A1, A2, A4, A5 and Lemma 1.2 of Lesson 4. A3 then excludes a negative initial value, and a positive one through the portfolio -X, so the value is zero (Theorem 1.2).' Re-run check_pages and the card scripts.")
f("FC2b-cards-c205", "cards", "cards.json FC2-c205 (line 1329; L04, ungraded) vs L04.html:70 (Definition 1.1)", "PASS",
  "Re-verified round 9 (new card). Back 'A call is in the money when S_t > K, and a put when S_t < K (Definition 1.1).' L04.html:70: 'The call is in the money at a date when S_t > K, and the put when S_t < K.' Definitional, ungraded, one fact. Its fact moved from c051, which no longer carries it.")
f("FC2b-cards-c206", "cards", "cards.json FC2-c206 (line 1335; L06, ungraded) vs L06.html:71 (Definition 1.3)", "PASS",
  "Re-verified round 9 (new card). Back 'Δ uS_0 + R_f B = V_1(u) and Δ dS_0 + R_f B = V_1(d) (Definition 1.3).' L06.html:71 gives the same two equations, and L06.html:69 defines R_f B for the bond. The equations moved from c083. Definitional, ungraded, one fact.")
f("FC2b-cards-c051", "cards", "cards.json FC2-c051 (line 329; L04, ungraded) vs L04.html:70 (Definition 1.1)", "PASS",
  "Re-verified round 9. Back 'The call pays (S_tau - K)^+ and the put pays (K - S_tau)^+, where x^+ = max(x, 0) (Definition 1.1).' matches L04.html:70 and L04.html:73 (definition text). The in-the-money sentence moved to FC2-c205. This card's overlap with FC2-c192 is recorded in row FC2b-cards-near-duplicate.")
f("FC2b-cards-c083", "cards", "cards.json FC2-c083 (line 549; L06, ungraded) vs L06.html:69-73 (Definition 1.3)", "PASS",
  "Re-verified round 9. Back 'Δ shares and a bond position B, where B > 0 is cash lent and B < 0 is cash borrowed. Its cost today is V_0 = Δ S_0 + B (Definition 1.3).' matches L06.html:69 (shares, bond, B > 0 lent, B < 0 borrowed) and L06.html:73 (V_0 = Δ S_0 + B). The two equations moved to FC2-c206.")
f("FC2b-cards-near-duplicate", "cards", "cards.json FC2-c051 (line 329) and FC2-c192 (line 1250)", "FAIL",
  "Re-run round 9 with ledgers/FC2/scripts/FC2-b-r9/dup_r9.py (difflib ratio, threshold 0.6 on front or back, pairs with a slice card). "
  "Pair c051/c192: back ratio 0.70, front ratio 0.37. c051 asks for the call and put payoffs; c192's back states the same payoff formulas, 'a call pays (S_tau - K)^+ and a put pays (K - S_tau)^+ at expiry (Definition 1.1)'. "
  "The same fact is tested by two cards. Round 8 did not flag it because the c051 back then carried the in-the-money sentence and scored lower. "
  "Not an exact duplicate (no identical front or back). Other pairs above 0.6 that involve a slice card (c057/c135, c066/c162, c136/c137, c094/c137) test different facts.",
  fix="Keep the payoff formulas on FC2-c051 only. Change the back of FC2-c192 to 'The number K > 0 that the payoffs of Definition 1.1 are measured from (Definition 1.1).' Re-run dup_r9.py and confirm the pair drops below 0.6.")
f("FC2b-cards-duplicates", "cards", "cards.json whole deck (194 cards)", "PASS",
  "Re-run round 9 with ledgers/FC2/scripts/FC2-b-r9/cards_r9.py: 194 cards, ids unique, no duplicate fronts or backs after normalisation (cards_r9.txt). Ids have gaps (12, 31, 38, 45, 77, 133, 134, 147, 156, 157, 170, 175, 176); the round-8 deck had the same gaps, and no card was removed in this delta.")
f("FC2b-cards-coverage", "cards", "cards.json lessons L01-L08", "PASS",
  "Re-run round 9 (cards_r9.txt): per-lesson counts L01 22, L02 24, L03 23, L04 25, L05 27, L06 31, L07 24, L08 18 (194). Every lesson has at least one card. Changes since round 8: L02 +1 (c202), L03 +2 (c203, c204), L04 +1 (c205), L05 +1 (c201), L06 +1 (c206), L07 +1 (c207).")
f("FC2b-cards-grade-ruling9", "cards", "cards.json grades for L04-L06", "PASS",
  "Re-run round 9 (cards_r9.txt): C cards (c058, c061, c072, c073, c074, c079, c095, c155, c171) all have a basis; the T and C grades of the carried cards are unchanged bytes (cards_r9.txt); c201 (T) is checked in its own row; ungraded cards c051, c083, c205, c206 and c192-c197 are definitional. No derived result is ungraded (c158 is carried from round 7 as an observation).")
f("FC2b-cards-L04-grades", "cards", "cards.json FC2-c051..c062, c135, c142, c143, c158, c159, c179, c205 (L04)", "PASS",
  "Re-verified round 9 with cards_r9.txt. Grades unchanged for the carried cards. c051 and c205 are ungraded definitional cards; c205 matches L04.html:70 (in the money).")
f("FC2b-cards-L04-rest", "cards", "cards.json L04 cards without grade (c051, c053, c142, c143, c158, c159, c187, c192-c196, c205)", "PASS",
  "Re-verified round 9: all ungraded L04 cards are definitions, assumption restatements or the in-the-money card. Overlap of c051 with c192 is recorded in row FC2b-cards-near-duplicate, not here.")
f("FC2b-cards-L06-grades", "cards", "cards.json FC2-c081..c098, c136, c137, c148-c150, c163, c166, c174, c181 (L06)", "PASS",
  "Re-verified round 9 (cards_r9.txt): c083 is changed and re-checked against L06.html:69-73; the other cards are carried by the same byte-identity argument as their round-8 rows.")
f("FC2b-cards-L06-rest", "cards", "cards.json L06 cards without grade (c082, c083, c088, c090, c092, c166, c174, c184, c185, c206)", "PASS",
  "Re-verified round 9: c083 (re-checked against L06.html:69-73), c206 (L06.html:71), and the other ungraded L06 cards are carried from round 8.")
f("FC2b-cards-c176-added", "cards", "cards.json FC2-c176 (absent); FC2-c184, c185", "PASS",
  "Re-verified round 9 (cards_r9.txt, id list): FC2-c176 is absent from cards.json (gap in the id sequence, pre-existing) and c184, c185 are unchanged and consistent with Definitions 1.1 and 1.2 (L06.html:63-64).")
# carried rows
out = []
for r in prev["rows"]:
    if r["id"] in fresh:
        out.append(fresh.pop(r["id"]))
    elif r["id"].startswith("FC2b-cards-"):
        out.append(carry(r, CARD_FILES))
    else:
        out.append(carry(r))
for rid in list(fresh):
    out.append(fresh[rid])
# keep the order: put new rows after their neighbours
rows = out
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
counts = {"PASS": sum(r["status"] == "PASS" for r in rows), "FAIL": sum(r["status"] == "FAIL" for r in rows)}
frag = {
 "unit": "FC2", "slice": "b", "round": 9,
 "verifier": "Haiku independent verifier, FC2 slice b round 9 (closing delta under ruling 30; did not build FC2)",
 "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
 "base": "4540351dc664559cdfd371b908f2b4e644cf4297 (round-8 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-FC2-b.round8.json, verdict FAIL on FC2b-cards-c197). Delta 4540351d..95f3f8cb for the slice: course/modules/FC/FC2/cards.json only (c016 L02, c039 L03, c051 L04, c083 L06, c197 L05, c201 L05, c202-c204 L02/L03, c205 L04, c206 L06, c207 L07). L04.html, L05.html, L06.html, tests/labs/FC2/lab-FC2-L04/L05/L06-1.py, plans/FC2-build-plan.md, notation/, references/, tools/ are byte-identical (git diff empty; md5 of L04/L05/L06.html checked).",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyS9-FC2-b",
 "scratch": "ledgers/FC2/scripts/FC2-b-r9/",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "FAIL" if counts["FAIL"] else "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Closing delta (ruling 30): re-verified from scratch every round-8 non-PASS row (FC2b-cards-c197, now PASS for the card itself; its defect moved to FC2b-cards-c201, FAIL), every row whose subject changed (cards rows that touch c051, c083, c176 and the whole-deck rows; all gate rows, since project.html, grader/ and the project twins changed), and the new cards c201, c205, c206. Other rows carried with the carry prefix because their subjects are byte-identical.",
  "The round-8 fragment was read as context only. Its carried rows were not re-derived line by line; the L04-L06 prose, twins and expected blocks are byte-identical to 4540351d (md5 and empty git diff), so their rows are carried under ruling 30. The card numbers were re-checked against the re-run twin output (c056, c057, c058, c061, c072-c076, c079, c094-c098, c135-c137, c148, c155, c171).",
  "Standing mutant set re-run (tools/mutate_graders.py --unit FC2): 111/111 killed. No new mutants were written (ruling 37). The slice has no project grader, so mutants is empty.",
  "Out of this slice and not checked here: the changed cards c016 (L02), c039 (L03), c202, c203, c204 (L02, L03) and c207 (L07, grade T, cites Theorem 2.3 and Theorem 3.3 of Lesson 6). The unit-level gates and the duplicate scan covered them, but their lesson-text checks belong to their own slices.",
  "Observation, not a row: FC2-c201's grade T is correct for a theorem-level statement; the FAIL is the hypotheses, not the grade. FC2-c197 is ungraded and definitional, which is consistent with ruling 9.",
  "Observation: the fixed-leg card FC2-c039 and the floating-leg cards are out of this slice and were not checked; the delta changed them."
 ],
 "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "fresh_rows": len(fresh) if False else None},
}
frag["summary"] = {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": 0, "carried_rows": sum(1 for r in rows if r["evidence"].startswith("Carried from round 8"))}
json.dump(frag, open("ledgers/FC2/FC2-b.json", "w"), ensure_ascii=False, indent=1)
print(frag["verdict"], frag["summary"])
