import json, sys
R6 = "/Users/billyribeiro/.fanout/frags/C-FC2-b.round6.json"
root = sys.argv[1]
prev = json.load(open(R6, encoding="utf-8"))
C = "Carried from round 6 (%s byte-identical since the previous pin 9fd6aed): "
# Re-run or freshly read this round (subject changed or gate re-run at 0d2d0f3)
fresh = {
 "FC2-b-gate-check-pages": "Re-run at 0d2d0f3: tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS' (scripts/FC2-b-r7/gates_r7.out).",
 "FC2-b-gate-check-dag": "Re-run at 0d2d0f3: tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS' (gates_r7.out).",
 "FC2-b-banned-and-process-words": "check_pages banned-string PASS (re-run). Changed learner text read in full: L04.html:51, L05.html:51, L06.html:55 and cards c059, c060, c064, c078, c085, c087 contain no process words (no 'this round', 'the builder', 'verifier', 'corrected', 'round').",
 "FC2-b-page-smoke": "Re-run at 0d2d0f3: tools/page_smoke.py --unit FC2 --pages L04 L05 L06 --skip-sweep -> 'page_smoke L04/L05/L06: PASS', 'page_smoke FC2: PASS' (gates_r7.out).",
 "FC2-b-lab-run-L04": "Re-run at 0d2d0f3: tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)'; twin under python -I -W error exit 0, stderr 0 bytes (scripts/FC2-b-r7/fc2b_r7_twin_L04.err); page code == twin and stdout == expected block (scripts/FC2-b-r7/twin_vs_page_L04_L06.out).",
 "FC2-b-lab-L04-header": "Re-run: twin_vs_page_L04_L06.out 'L04: page code == twin: True ... stdout == expected block: True'. L04.html:233, :242 unchanged since 9fd6aed.",
 "FC2-b-lab-L05-run": "Re-run at 0d2d0f3: run_labs PASS; twin under -I -W error exit 0 stderr 0 bytes; page code == twin, stdout == expected block (twin_vs_page_L04_L06.out).",
 "FC2-b-lab-L05-claims": "L05.html:133 and :286 unchanged since 9fd6aed (carried for those lines), and the new L05.html:51 sentence 'plants two errors that the checks name' is verified: twin lines 118-127 plant one parity error (put at 100 USD + 300 cents) and one convexity error (call and put at 90 USD + 500 cents), and the printed output names both (fc2b_r7_twin_L05.out lines 'planted parity error ...', 'planted convexity error ...'). Also 'Lab 1 checks each identity on a SIMULATED price set' holds (twin docstring, lines 1-11).",
 "FC2-b-lab-L06-run": "Re-run at 0d2d0f3: run_labs PASS; twin -I -W error exit 0 stderr 0 bytes; page code == twin and stdout == expected block (twin_vs_page_L04_L06.out).",
 "FC2-b-cards-duplicates": "Re-run on course/modules/FC/FC2/cards.json at 0d2d0f3 (scripts/FC2-b-r7/cards_r7.out): 142 cards, dup ids [], dup fronts [] (normalised fronts).",
 "FC2-b-cards-removed-c077": "Re-run (cards_r7.out): 'missing numbers in c001..c144: [31, 77]'; c077 still absent, neighbours c076 and c078 unchanged in content except c078 which is re-verified below. c031 is out of slice (L02).",
 "FC2-b-card-c059": "cards.json FC2-c059 (L04, T): 'No. Under A2, A3 and A5, Proposition 2.3 proves only the weak inequality V_A(0) >= V_E(0) ...'. Proposition 2.3 is stated 'Under A2, A3 and A5' (L04.html:103-104); Remark 2.4 exists (L04.html:109-111). Hypothesis now matches the statement.",
 "FC2-b-card-c078": "cards.json FC2-c078 (L05, T): 'Under A1 to A5 and (N), C <= S (Theorem 2.2(a)) ... payoff min(S_tau, K) >= 0 (uses (N)), which A3 excludes.' Theorem 2.2 is stated 'Under A1, A2, A3, A4, A5 and (N)' (L05.html:85); L05.html:95(a) gives the same payoff min(S_tau,K) and uses (N). The round-6 FAIL (omitted (N)) is resolved.",
 "FC2-b-card-c145": "FC2-c145 (L05, 'Does put-call parity hold only for at-the-money options?') is removed in 9fd6aed..0d2d0f3 (cards.json: 'FC2-c145' absent; 142 cards; no reference to FC2-c145 in course/, tools/, tests/, references/, curriculum/ - grep). Its question is now FC2-c064 (L05), which answers 'Every strike ... (Theorem 1.2)' under A1 to A5 (Theorem 1.2 at L05.html:63-64). The round-6 FAIL row subject no longer exists; no duplicate card remains (dup fronts []).",
 "FC2-b-cards-new-L04-L06": "Re-run: ids of L04-L06 cards compared with 04626e9 (git show 04626e9:course/modules/FC/FC2/cards.json): added [] and removed [] for L04-L06. Changed in slice: c059, c060, c064, c078, c085, c087 (all re-verified in this round). c030 (L02) and c049 (L03) are out of slice.",
 "FC2-b-cards-L04-L06-hypothesis-audit": "Re-verified this round for every card whose text changed: c059 (A2,A3,A5 = Proposition 2.3 hypotheses), c060 (A2,A3 = Proposition 2.2 hypotheses), c064 (A1-A5 = Theorem 1.2 hypotheses), c078 (A1-A5,(N) = Theorem 2.2 hypotheses), c085 (A1,A2,A3,A5,A6 = Theorem 1.4 hypotheses, L06.html:78), c087 (Theorem 1.4 hypotheses by reference). Cards of L04-L06 not changed since 9fd6aed are carried. Every card's cited statement (Proposition, Theorem, Remark, Definition, Example, Problem, Lab) exists on the page: scripts/FC2-b-r7/cards_r7.out lines 'ref ...  on page: [...]' with no empty list for a card statement.",
 "FC2-b-cards-L05": "Re-verified this round: cards c063-c080 and c132 in cards.json (c145 now removed). c064 and c078 changed and were re-read against L05.html:55-71 (Theorem 1.2, Remark 1.3) and L05.html:84-98 (Theorem 2.2) and PASS. c069, c070, c071, c072-c075, c079, c080 unchanged since 9fd6aed (carried; their round-6 PASS evidence stands).",
 "FC2-b-cards-L06": "Re-verified this round: c081-c098, c136, c137 in cards.json. c085 and c087 changed and re-read against L06.html:63-64 (Definition 1.2, A6 = 0 < d < R_f < u), L06.html:77-88 (Theorem 1.4), L06.html:103-104 (Remark 1.7) and PASS. Others unchanged since 9fd6aed (carried).",
 "FC2-b-card-c085": "cards.json FC2-c085 (L06, T): front now 'Under A1, A2, A3, A5 and A6, what happens if a claim trades at a price pi different from the replicating cost V_0 ...'. Theorem 1.4 hypotheses are 'Under A1, A2, A3, A5 and A6' (L06.html:78). Back: zero-cost portfolio with strictly positive payoff, Theorem 1.4(c) and Example 1.6 exist (L06.html:79, :98-99). Arithmetic: sell claim for pi, buy replicating portfolio at V_0, lend pi-V0: today 0, expiry (pi-V0)R_f > 0 in both states. PASS.",
 "FC2-b-cards-L04": "Re-verified this round: cards c051-c062, c135, c142, c143 (c059 and c060 changed, re-read against L04.html:103-104 (Proposition 2.3), :109-111 (Remark 2.4), :96 (Proposition 2.2) and :68-70 (Definition 1.1); c061, c062, c051-c058, c135, c142, c143 unchanged since 9fd6aed, carried).",
 "FC2-b-hours": "Carried from round 6 (L04.html:2, L05.html:2, L06.html:2 and index.html:29,31,133,138-140 byte-identical since the previous pin; the delta changed only the why-it-matters text and the cards). check_pages PASS (re-run).",
 "FC2-b-notation": "Re-checked this round for the three changed learner sentences (L04.html:51, L05.html:51, L06.html:55): no math markup and no new symbol; they cite only Definition/Theorem numbers and A1-A6. Rest of the notation check carried (notation/notation.json unchanged since 9fd6aed).",
}
rows = []
new_rows = {
 "FC2-b-cross-refs-round7": ("cross-refs", "L04.html:51 'Definition 2.1 of Lesson 4'; L05.html:51 'Definition 3.1 of Lesson 5', 'Theorem 4.1 of Lesson 5'; L06.html:55 'Definition 1.2 of Lesson 6'",
   "PASS", "Each number exists in its named lesson: L04.html:90 Definition 2.1 (American and European exercise, which defines the intrinsic value h(S_t) at L04.html:93); L05.html:110 Definition 3.1 (convexity in strike); L05.html:300 Theorem 4.1; L06.html:63 Definition 1.2 (One-period binomial model; L06.html:64 states A6 as 0 < d < R_f < u, the 'binomial condition' the page names). The sentence 'These results use no price model' is not contradicted by L05.html:67 or Remark 1.3 (L05.html:70-71), which use no distribution for S_tau."),
}
for r in prev["rows"]:
    rid = r["id"]
    if rid in fresh:
        status = "PASS"
        ev = fresh[rid]
    else:
        status = "PASS"
        if r["status"] != "PASS":
            raise SystemExit("unexpected non-PASS carry " + rid)
        ev = (C % r["location"]) + r["evidence"]
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev})
for rid, (chk, loc, st, ev) in new_rows.items():
    rows.append({"id": rid, "check": chk, "location": loc, "status": st, "evidence": ev})
for rid in ["FC2-b-card-c145"]:
    pass
frag = {
 "unit": "FC2", "slice": "b", "round": 7,
 "verifier": "Haiku independent verifier (FC2 slice b, round 7; did not build FC2)",
 "pin": "0d2d0f3", "base": "9fd6aed (round-6 pin; delta 9fd6aed..0d2d0f3 read for every L04-L06 hunk and changed card; the 04626e9..9fd6aed hunks were verified in round 6 and are unchanged at 0d2d0f3)",
 "checkout": root, "scratch": "/tmp", "verified_at": "2026-10-29T06:10:00+00:00",
 "verdict": "PASS",
 "rows": rows, "mutants": [],
 "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Delta 9fd6aed..0d2d0f3 in slice b: L04.html:51 (why-it-matters), L05.html:51 (why-it-matters), L06.html:55 (A6 sentence); cards.json c059, c060, c064, c078, c085, c087 changed; c145 removed; c144 and c113 (L03, L07) and course/modules/E, CF, M, FC1 changes are out of slice. Every hunk read in context.",
  "Round-6 FAIL rows resolved: FC2-b-card-c078 (now states (N)), FC2-b-card-c145 (card removed, duplicate of c064 gone), FC2-b-cards-new-L04-L06 and FC2-b-cards-L04-L06-hypothesis-audit (all changed L04-L06 cards now name their hypotheses).",
  "Labs are demonstrations; lab twins tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py and lab-FC2-L06-1.py are byte-identical to 9fd6aed (git diff empty for tests/labs/FC2). Mutation testing does not apply to lab twins (verifier-rules ruling); no mutants written for this slice.",
  "Not run: full repo gate (ruff whole repo, mypy --no-incremental, render_curriculum, build_site --check, fetch_data --check, run_graders, mutate_graders, check_projects). No Python file in slice b changed, and the slice's Python (three lab twins) passes ruff check and ruff format --check.",
  "Not checked in slice b: L01-L03, L07-L08, project page and grader, project labs 1-3, hub index.html beyond the hours cross-check; out of slice.",
 ],
 "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
frag["summary"] = "FC2 slice b round 7 (pin 0d2d0f3): %d rows, %d PASS, %d FAIL. Round-6 FAIL rows resolved. Verdict PASS." % (len(rows), n_pass, len(rows) - n_pass)
json.dump(frag, open(root + "/ledgers/FC2/FC2-b.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(frag["summary"])
