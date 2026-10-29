import json, sys
PIN = "448548f997b7957f7b1d418a28d47f50d4a80fa0"
C = "Carried from round 14 (cited subject byte-identical since the previous pin d2b4a87; no hunk of d2b4a87..448548f touches it):"
FRESH_GATE = "Fresh run r15 (log ledgers/M3/scripts/M3-c-r15/{log}): {msg}"
def carry(prev_status_note=""):
    return C + " " + prev_status_note
rows = []
def add(i, check, loc, status, ev):
    rows.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})
add("GATE-01","tools/check_pages.py","tools/check_pages.py","PASS",FRESH_GATE.format(log="check_pages.log", msg="'check_pages M3: PASS', exit 0 (fresh)."))
add("GATE-02","tools/check_dag.py","tools/check_dag.py","PASS",FRESH_GATE.format(log="check_dag.log", msg="'check_dag AP1: PASS', exit 0."))
add("GATE-03","tools/build_site.py --check","tools/build_site.py","PASS",FRESH_GATE.format(log="build_site_check.log", msg="'site data current: 6 outputs', exit 0."))
add("GATE-04","tools/render_curriculum.py and git diff --exit-code","tools/render_curriculum.py","PASS",FRESH_GATE.format(log="render.log, render_diff.log", msg="'curriculum valid: 25 parts, 134 modules, 157 projects, 13,715 h'; git diff --exit-code on CURRICULUM.md and curriculum/curriculum.json exit 0 after regeneration."))
add("GATE-05","tools/run_labs.py --unit M3","tools/run_labs.py","PASS",FRESH_GATE.format(log="run_labs_M3.log", msg="'run_labs M3: PASS (12/12)', exit 0."))
add("GATE-06","tools/page_smoke.py --unit M3 --pages L07 L08 L09","tools/page_smoke.py","PASS",FRESH_GATE.format(log="page_smoke.log", msg="'page_smoke M3: PASS', exit 0."))
add("GATE-07","pyproject.toml ruff config","pyproject.toml","PASS",FRESH_GATE.format(log="ruff.log", msg="'All checks passed!', '12 files already formatted', exit 0."))
add("GATE-08","pyproject.toml mypy config","pyproject.toml","PASS",FRESH_GATE.format(log="mypy.log", msg="'Success: no issues found in 255 source files', exit 0 (mypy --no-incremental)."))
add("GATE-09","tests/ M3-selected","tests/","PASS",FRESH_GATE.format(log="collect.log, pytest_M3.log", msg="collect-only -k M3 gives 12; pytest -k M3 exit 0."))
add("GATE-10","tools/verify_refs.py --offline","tools/verify_refs.py","PASS",FRESH_GATE.format(log="verify_refs.log", msg="'offline integrity: 560 entries, 0 problems', exit 0."))
add("GATE-11","tools/fetch_data.py --check","tools/fetch_data.py","PASS",FRESH_GATE.format(log="fetch_data.log", msg="'fetch_data: 3 datasets, 0 problems', exit 0."))
add("TWIN-01","Each twin runs under python -I -W error","tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py","PASS","Fresh: python -I -W error exit 0 for all three (twin_lab-M3-L07-1.out 11 lines, L08 15 lines, L09 14 lines, each ending exit 0); run_labs M3 12/12.")
add("TWIN-02","Page code equals twin; expected block equals output","course/modules/M/M3/L07.html, L08.html, L09.html","PASS","Fresh: run_labs M3 12/12 includes page-code-to-twin identity and expected-block match (run_labs_M3.log).")
add("MATH-L07-01","Theorem 1.2 to 1.3 proofs and Remark 1.4","course/modules/M/M3/L07.html:63-96","PASS",C+" L07.html:63-96 has no hunk in d2b4a87..448548f (diff hunks at 208, 291, 298 only).")
add("MATH-L07-02","Theorem 2.2 and Section 1 consequences","course/modules/M/M3/L07.html:107-121, 319-331","PASS",C+" no hunk in 107-121 or 319-331.")
add("MATH-L07-03","Problem set M1-M3, P1-P3, E1-E3, R1 numbers and proofs","course/modules/M/M3/L07.html:231-308 and 312-318","PASS","Delta hunks at L07.html:291 and 298 (inside 231-308) were re-read: each change inserts only 'Assuming F1 to F4 of Lesson 4,' or 'assuming F1 to F4 ...,' and leaves every number and algebra step unchanged (diff -U2 d2b4a87 448548f). Numbers at 298 re-derived fresh (NUM-L07-02). Other lines in 231-308 and 312-318 carried from round 14 (byte-identical since d2b4a87).")
add("NUM-L07-01","Lab 1 printed values and interpretation","course/modules/M/M3/L07.html:190-199, 200","PASS",C+" lines 190-200 unchanged; twin output 0.8951 (twin_lab-M3-L07-1.out).")
add("NUM-L07-02","E2 solution A^T y numbers","course/modules/M/M3/L07.html:298","PASS","Fresh: ledgers/M3/scripts/M3-c-r15/nums_L07_r15.py (np.random.default_rng(7), same generator as the twin) prints A^T y = [18.3797, 3.0959, -17.6035], i.e. (18.38, 3.10, -17.60) to two decimals as L07.html:298 states; max |A^T r| = 2.5e-15. Marker-only hunk at 298 re-read.")
add("NUM-L07-03","E3 intercept numbers and generator","course/modules/M/M3/L07.html:303-305; tests/labs/M3/lab-M3-L07-1.py lines 149-154","PASS",C+" lines 303-305 and the twin unchanged.")
add("MATH-L08-01","Proposition 1.1, 1.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3 proofs","course/modules/M/M3/L08.html:56-133","PASS",C+" no hunk in 56-133 (the L08 hunk at 290 is outside). Re-read Theorem 2.1(a),(b) and Proposition 2.3 statement and proof this round: correct.")
add("MATH-L08-02","Worked solutions and Remark 2.4 cross-checks","course/modules/M/M3/L08.html:323-416","PASS",C+" the hunk at L08.html:290 is outside this range; the marker hunks inside it were verified in round 14.")
add("NUM-L08-01","Lab 1 printed values","course/modules/M/M3/L08.html:270-285, 377","PASS",C+" no hunk in range; twin output 0.7587/0.9791 confirmed (twin_lab-M3-L08-1.out).")
add("NUM-L08-02","Shares 75.9, 18.1, 5.2 percent","course/modules/M/M3/L08.html:277-280, 284","PASS",C+" no hunk in range.")
add("NUM-L08-03","Solution numbers","course/modules/M/M3/L08.html:389-391","PASS",C+" no hunk in range.")
add("MATH-L09-01","Lemma 1.3 to Proposition 3.5 proofs","course/modules/M/M3/L09.html:73-181","PASS",C+" L09.html is byte-identical since d2b4a87.")
for i,loc in [("NUM-L09-01","L09.html:104-107, 329-331"),("NUM-L09-02","L09.html:334-338, 342"),("NUM-L09-03","L09.html:438-440; L09.html:559-562"),("NUM-L09-04","L09.html:341, 342"),("NUM-L09-05","L09.html:177-180"),("NUM-L09-06","L09.html:387-449")]:
    add(i,"Numbers and prose of L09","course/modules/M/M3/"+loc,"PASS",C+" L09.html byte-identical since d2b4a87; twin output 0.6400000000 confirmed for NUM-L09-02 (twin_lab-M3-L09-1.out).")
add("NOTATION-01","Symbols vs notation/notation.json","notation/notation.json; course/modules/M/M3/L07.html, L08.html, L09.html","PASS",C+" notation/ has no delta; new text adds no new symbol (only F1 to F4, already defined in L04).")
add("NOTATION-02","Symbol reuse","course/modules/M/M3/L07.html, L08.html, L09.html","PASS",C+" the new phrases use X, M, c, Theorem names; no reuse.")
add("STRUCT-L07-01","L07 structure","course/modules/M/M3/L07.html","PASS",C+" structure unchanged (hunks are single-paragraph text edits).")
add("STRUCT-L08-01","L08 structure","course/modules/M/M3/L08.html","PASS",C+" structure unchanged.")
add("STRUCT-L09-01","L09 structure","course/modules/M/M3/L09.html","PASS",C+" structure unchanged.")
add("DATA-L08-01","Dataset use in L08","course/modules/M/M3/L08.html:291","PASS",C+" line 291 unchanged (hunk is at 290).")
add("SIM-LABEL-01","SIMULATED labelling","tests/labs/M3/lab-M3-L07-1.py, L08-1.py, L09-1.py; page prose","PASS",C+" labs and labels unchanged.")
add("DAG-01","Concept DAG","tools/check_dag.py; L07-L09 meta-row links","PASS","Fresh: check_dag CF1 and AP1 PASS, exit 0.")
add("CROSSREF-01","Cross-citations","course/modules/M/M3/L07, L08, L09 cross-citations","PASS",C+" cited lines unchanged; new 'Lesson 4' references resolve to the F1 to F4 block at L04.html:56-62 (read).")
add("HOURS-01","Hours arithmetic","course/modules/M/M3/L07.html:2,35; L08.html:2,35; L09.html:2,35; index.html:154-156","PASS","Fresh: render_curriculum regenerates with no diff (render_diff.log exit 0); build_site --check current.")
add("PROSE-01","Prose numbers","course/modules/M/M3/L07.html:125-200; L08.html:146-284; L09.html:193-342","PASS",C+" no hunk in these ranges.")
add("GRADE-01","Grades","course/modules/M/M3/L07.html:342-346; L08.html:428-434; L09.html:484-493; cards.json","PASS","Fresh: cards.json changed cards c127 (T), c135 (T), c186 (T, Theorem 2.1(b)) read; grades match the lesson grade tables; c147 and c185 carry no grade field, as c147 did before.")
add("ASSUME-01","Unmarked F1-F4 restatements","course/modules/M/M3/L07.html:208, 291, 298; course/modules/M/M3/L08.html:290","PASS","Fresh: L07.html:208 'Assuming F1 to F4 of Lesson 4, Theorem 2.2(c) holds for every response vector'; L07.html:291 'Assuming F1 to F4 of Lesson 4, that holds for every response, by Theorem 2.2(c)'; L07.html:298 'and, assuming F1 to F4 of Lesson 4, by Theorem 2.2'; L08.html:290 'Assuming F1 to F4 of Lesson 4, Proposition 2.3 covers scaling the whole matrix X'. All four round-14 findings are fixed.")
add("ASSUME-02","Labs and prose that use F1-F4","course/modules/M/M3/L08.html:140-141; course/modules/M/M3/L09.html:98, 116, 123, 139, 185, 187, 342, 447",'PASS',C+" no hunk in these lines.")
add("ASSUME-03","Theorem 2.1 / Proposition 2.3 solution markers","course/modules/M/M3/L08.html:357, 414-416","PASS",C+" no hunk in these lines.")
add("ASSUME-04","R1 and E3 markers","course/modules/M/M3/L07.html:316 (R1); course/modules/M/M3/L09.html:447 (E3)","PASS",C+" no hunk in these lines.")
add("ASSUME-05","Unmarked restatement of Theorem 2.2(c) in the L07 misconception solution","course/modules/M/M3/L07.html:218","FAIL","L07.html:218 reads 'The residual is orthogonal to the columns of \\(A\\), not zero.' The clause asserts the orthogonality of the residual, which is Theorem 2.2(c) (L07.html:108-116, whose statement carries 'Assuming F1 to F4 of Lesson 4'). The marker appears only later in the same paragraph, before Remark 1.4, so the orthogonality assertion itself is unmarked. Lesson rule (L04 conventions, L07.html:52): a result that uses F1 to F4 says so where it is stated. Same defect class as round-14 ASSUME-01. Fix: insert 'Assuming F1 to F4 of Lesson 4,' before 'the residual is orthogonal' in L07.html:218.")
add("CARD-HYP-01","Cards carrying hypotheses","course/modules/M/M3/cards.json ids M3-c117 to c123, c134 to c137, c143 to c145, c153 to c157, c161, c165, c168","PASS","Re-read this round: c135 changed (front and back) and now reads 'Assuming F1 to F4 of Lesson 4, the first direction v_1 maximizes u^T M u ... (Theorem 2.1)'; marker present. Other listed cards byte-identical since d2b4a87 (the cards.json hunks are at c054, c127, c135, c147 and the appended c185, c186 only).")
add("CARD-HYP-02","Cards carrying hypotheses","course/modules/M/M3/cards.json ids M3-c142, M3-c153, M3-c158","PASS",C+" card entries byte-identical.")
add("CARD-C183","Card M3-c183 numbers","course/modules/M/M3/cards.json id M3-c183","PASS",C+" entry byte-identical.")
add("CARD-C161","Card M3-c161 numbers","course/modules/M/M3/cards.json id M3-c161","PASS",C+" entry byte-identical.")
add("CARD-C130","Card M3-c130 numbers","course/modules/M/M3/cards.json id M3-c130","PASS",C+" entry byte-identical.")
add("CARD-C138","Card M3-c138 numbers","course/modules/M/M3/cards.json id M3-c138; course/modules/M/M3/L08.html Remark 2.4 (lines 131-133)","PASS",C+" entry and cited lines byte-identical.")
add("CARD-OK-01","Card numbers appear in their lesson; card lesson fields","course/modules/M/M3/cards.json","PASS","Fresh: changed cards checked: c127 (Remark 1.4, lesson L07, value 0.8951 at L07.html:197 and 218), c135 (Theorem 2.1, L08), c147 (Definition 1.2, L09), c185 (Definition 1.2, L09), c186 (Theorem 2.1(b), L08), c054 (L03, example removed, no new number). 186 cards, unique ids. Hypothesis wording of c127 is a separate row (CARD-HYP-03).")
add("CARD-HYP-03","Card M3-c127 carries F1-F4 hypothesis on the orthogonality claim","course/modules/M/M3/cards.json id M3-c127 (back)","FAIL","Back text: 'False. The residual is orthogonal to the columns of A, not zero. For a response outside the column space, y - P y is not zero, ... Assuming F1 to F4 of Lesson 4, Remark 1.4 gives ...'. The orthogonality claim and the non-vanishing claim (Theorems 1.2 and 2.2(c)) are asserted before the marker, which in round 14 was at the front of the back text and was moved by this delta. Fix: restore 'Assuming F1 to F4 of Lesson 4,' before 'The residual is orthogonal' in the back of M3-c127.")
add("CARD-DUP-01","No duplicate cards","course/modules/M/M3/cards.json","PASS","Fresh: 186 cards, no duplicate id. c135 (first direction) and c186 (k-th direction, k >= 2) are distinct; c147 (norm) and c185 (distance) are distinct. grep 'k-th' returns only c186.")
add("CLAIM-L07-01","Claim: the residual is orthogonal (grade T)","course/modules/M/M3/L07.html:206","PASS",C+" line 206 unchanged.")
add("CLAIM-L07-02","Claim: Theorem 1.2 projection","course/modules/M/M3/L07.html:206; L07.html:90; L07.html:316","PASS",C+" lines unchanged.")
add("CLAIM-L07-03","Claim: normal equations","course/modules/M/M3/L07.html:206","PASS",C+" line unchanged.")
add("REMARK-L08-01","Remark 2.4 claim 1","course/modules/M/M3/L08.html:131-133","PASS",C+" unchanged.")
add("REMARK-L08-02","Remark 2.4 claim 2","course/modules/M/M3/L08.html:131-133","PASS",C+" unchanged.")
add("REMARK-L08-03","Remark 2.4 claim 3","course/modules/M/M3/L08.html:131-133","PASS",C+" unchanged.")
add("PROSE-02","Prose claims about the lab and the theorems","course/modules/M/M3/L07.html:206, 316; L08.html:132, 137, 282-284; L09.html:98, 118, 147, 349","PASS",C+" no hunk in these lines.")
add("PROCESS-01","No process words in learner text","course/modules/M/M3/L07.html, L08.html, L09.html","PASS","Fresh grep for round/verifier/builder/agent/fragment/this round in the three pages returns no match. The delta adds only 'Assuming F1 to F4 of Lesson 4' phrases.")
add("REG-01","Registry/notation regression","notation/notation.json; course/modules/M/M3/L07.html, L08.html, L09.html","PASS",C+" notation/ unchanged in the delta.")
frag = {
 "unit":"M3","slice":"c","round":15,
 "verifier":"independent Haiku verifier, checkout verifyB15-M3-c",
 "pin":PIN,"base":"d2b4a874a8deeeb77ce4e2ec8bab7479eaf4f00c",
 "checkout":"/Users/billyribeiro/.fanout/wt/verifyB15-M3-c",
 "scratch":"/Users/billyribeiro/.fanout/wt/verifyB15-M3-c/ledgers/M3/scripts/M3-c-r15",
 "verified_at":"2026-10-29","verdict":"FAIL","rows":rows,
 "mutants":[],
 "registry_flags":[],
 "freshness_flags":["L07.html:218 and card M3-c127 back carry the F1-F4 marker after the orthogonality claim (introduced by delta d2b4a87..448548f for c127)"],
 "notes":"Delta d2b4a87..448548f read hunk by hunk: L07.html 208, 291, 298; L08.html 290; cards.json c054, c127, c135, c147, appended c185, c186. All 4 round-14 ASSUME-01 sites are now marked. New FAIL rows: ASSUME-05 (L07.html:218) and CARD-HYP-03 (card M3-c127). Not counted by ruling: lab-M3-L09-1.py docstring (lines 6-8) cites Propositions 3.3 and 3.4 without the marker; it is a lab-check description, not a lesson statement. No project grader in this slice; no mutation run (ruling). Hidden explain blocks (e.g. L07.html:391, L08 hint 377) cite Theorem 2.2(c)/1.2(c) as pointers and were not counted as assertions.",
 "summary":"M3-c round 15: 66 rows, 64 PASS, 2 FAIL (F1-F4 marker missing on the orthogonality claim in L07.html:218 and card M3-c127). All gates PASS fresh."
}
json.dump(frag, open("ledgers/M3/M3-c.json","w"), indent=1, ensure_ascii=False)
print(len(rows), sum(r["status"]=="PASS" for r in rows))
