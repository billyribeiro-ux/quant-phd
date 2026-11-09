import json
import sys

RE = "ledgers/FC2/scripts/FC2-b-r6/"
OLD = "/Users/billyribeiro/.fanout/frags/S-FC2-b.round5.json"
rows = json.load(open(RE + "rows_r6_partial.json", encoding="utf-8"))
old = {r["id"]: r for r in json.load(open(OLD, encoding="utf-8"))["rows"]}
by = {r["id"]: r for r in rows}

def set_ev(rid, ev):
    by[rid]["evidence"] = ev

set_ev("FC2b-lab-L04-twin",
  f"Changed this delta: twin docstring line 11 (tests/labs/FC2/lab-FC2-L04-1.py:11) and page lines 136 and 243. Page code equals the twin exactly (script: code==twin); expected block L04.html:220-242 equals twin stdout exactly ({RE}L04_twin_stdout.txt, {RE}L04.out). Output re-derived: call payoff 25.00 at 125 and profit 17.00; break-evens 108.00 and 93.00; path hold values 6.56, 7.29, 8.10, 9.00, 10.00; best exercise dates 1 (18.00) and 3 (14.58).")
set_ev("FC2b-lab-L06-twin",
  f"Changed this delta: page lines 171-175 and twin docstring lines 4-9 (same text). Page code equals the twin exactly; expected block L06.html:294-316 equals twin stdout exactly ({RE}L06_twin_stdout.txt). Interpretation L06.html:317 consistent with output: shares as fractions (1/2, 3/4, 5/6), bond -20, -30, -50.")
set_ev("FC2b-lab-L06-docstring",
  f"Re-verified against this delta's docstring change (adds 'and in closed form'). Output lines in the expected block L06.html:294-316: integer-cents lines are 299 (V0 one period, 3000 cents), 300 (discounted expectation, 3000 cents), 306 (backward-induction V0, 4500 cents) and 307 (closed form, 4500 cents), as the docstring lists. After-move, expiry and stock values (297, 303-305, 309) print in currency units only; shares and bond positions print as Fractions or integers (298, 308, 310, 311). cents() is half-up (twin code). Output saved in {RE}L06.out.")
set_ev("FC2b-num-L04",
  "Re-derived each number again: 0.10536 (ln(10/9), L04.html:116); 6.56, 18.00, 14.58 (Example 2.5); 108.00 and 93.00 break-evens; 17.00 and 25.00 (L04.html:243, 266); 127.43484 (R1, L04.html:360: 20000/729 = 27.434842, plus 100); 32.805 (R3, L04.html:374: 50 * 0.6561); E1 values 10.00, 8.10, 9.00, 7.29 (L04.html:335). Line 243 changed sentence adds no number. All agree with the printed expected block.")
set_ev("FC2b-struct-L05",
  "Section order and counts unchanged (heading ids s1-s10; the delta replaces text on lines already present; quiz 9 items at L05.html:464-534; problem set 12 items M1-M3, P1-P3, E1-E3, R1-R3 at L05.html:348-436). Re-read in full this round.")
set_ev("FC2b-cards-delta-round1",
  set_ev.__name__ and by["FC2b-cards-delta-round1"]["evidence"].replace("c060 PASS (Prop 2.2 under A2, A3 at L04.html:99;", "c060 PASS (Proposition 2.2 under A2, A3, L04.html:95-96 with proof L04.html:99;"))
set_ev("FC2b-banned-process",
  "Re-read this delta's hunks and grepped L04-L06 and both twins for builder, verifier, round, revised, previous, updated, corrected, fixed, draft, TODO, delta: matches were only 'fixed' (a fixed list, a fixed rate, fixed u, d, R_f), the 'Previous' navigation links, and the 'fixed-point rule' of the usd() docstring. None is process language.")
set_ev("FC2b-notation",
  f"Carried in substance: notation/, references/, tools/ and plans/FC2-build-plan.md are byte-identical to dde0486b (git diff --quiet), so the registered symbols are unchanged. The delta adds no new symbol: its only new label, (N), is the hypothesis defined at L05.html:76 (see FC2b-define-before-use-N). Round-5 symbol checks for L04-L06 apply to every math hunk not changed here.")
set_ev("FC2b-define-before-use-self-financing",
  "Carried from round 5 (L06.html:161-162 and L06.html:167 unchanged in this delta): Definition 3.5 defines the self-financing strategy at L06.html:161-162 before its first use at L06.html:167 (the lab hypothesis); no earlier use.")
set_ev("FC2b-misconception-L04-L06-other",
  "L04 misconceptions 1-4 (L04.html:256-271) re-read; misconceptions 1 and 2 (L04.html:258, 262) changed in this delta and re-derived (see FC2b-plan-L04-no-L05-result). Carried from round 5 for L05.html:327-337 and L06.html:327-335, byte-identical since dde0486b: L05 misconceptions 1-4 and L06 misconceptions 1-3 re-derived (L06 Example 3.4 numbers 156.25, 56.25, 36, 70.3125 re-checked).")
set_ev("FC2b-lab-L05-twin",
  f"Carried from round 5 (tests/labs/FC2/lab-FC2-L05-1.py and L05.html:131-287 byte-identical since dde0486b; L05 delta hunks are at lines 51, 301, 310, 483, 517 only). Re-run this round: twin under python -I -W error exit 0, 0 bytes stderr; stdout equals the expected block L05.html:265-285 exactly ({RE}L05_twin_stdout.txt, {RE}L05.out).")
set_ev("FC2b-cards-L05-rest", by["FC2b-cards-L05-rest"]["evidence"])
set_ev("FC2b-lab-L04-hypothesis",
  "Hypothesis (L04.html:125, unchanged this delta) re-read: call payoff zero at each grid spot up to 100 USD and spot minus 100 above it; profit negative below 108 and positive above; put break-even 93; best exercise dates 1 (call) and 3 (put); holding the call to expiry worth 6.56 USD at date 0. The expected block L04.html:220-242 matches the run exactly.")

# Rows still to add
extra = [
  {"id": "FC2b-num-L06", "check": "prose numbers", "location": "L06.html prose numbers (lines 94, 99, 157, 319, 332, 335, 342-388, 441-476)", "status": "PASS",
   "evidence": "Carried from round 5 (L06.html lines 94, 99, 157, 319, 332, 335, 342-388, 441-476 byte-identical since dde0486b; the one L06.html hunk is lines 171-175): the numbers were re-derived this round: 3000 and 4000 cents (Example 1.5, M1), 1/2, 2/3, -80/3, 40, 48 (M3), 60 (E2, 6000 cents), 75, 45, 56.25, 36, 70.3125 (1125/16), 156.25, 28 quote arbitrage at 2.5 (E3), 25 (R2), 0.75 and 0.5 quiz answers. All agree with the printed output and the page formulas."},
  {"id": "FC2b-struct-L06", "check": "structure", "location": "L06.html (BUILDER_RULES 4.2 order and counts)", "status": "PASS",
   "evidence": "Carried from round 5 (L06.html heading ids s1-s9 and block order byte-identical since dde0486b; the one hunk is the lab paragraph at lines 171-175): sections 1-9, 3 Definitions and 3 Theorems in sections 1-3, a 4-section canon-breaks, 6 problem-set items per tier (M1-M3, P1-P3, E1-E3, R1-R3), 10 quiz items at L06.html:413-481."},
  {"id": "FC2b-define-before-use-N", "check": "define-before-use (verifier class 5); notation label (N)",
   "location": "L05.html:51 (first use, why-it-matters) vs L05.html:76 (definition of (N))", "status": "FAIL",
   "evidence": "Introduced by this delta: the previous L05.html:51 had no (N); the new text reads 'under A1 to A5, (N) and a non-negative rate' at L05.html:51. The hypothesis is first defined at L05.html:76 ('The bounds below use one more hypothesis, (N): the spot price at expiry is non-negative.'). grep -n '(N)' over L05.html gives line 51 first, then 76, 80, 95, 97, 102, 124, 337, 384, 523. The summary paragraph therefore uses a labelled hypothesis before the page defines it. Checked: no other L04-L06 label is used before its definition in the delta (Theorem 4.1 at L05.html:51 is a forward reference to a numbered result, which is allowed).",
   "fix": "At L05.html:51 either write the hypothesis in words ('under A1 to A5, a non-negative spot at expiry, and a non-negative rate'), or add 'the hypothesis (N) of Section 2' at the first use. No other change; the hypotheses stated stay the same."},
]
rows = [by.get(r["id"], r) for r in rows] + extra
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert set(old) <= set(ids), set(old) - set(ids)
# drop the stale duplicate-carry text that referenced round-5 subjects we did not change: keep as is
fragment = {
  "unit": "FC2",
  "slice": "b",
  "round": 6,
  "verifier": "Haiku independent verifier, FC2 slice b round 6 (did not build FC2)",
  "pin": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a",
  "base": "dde0486beeb0312e4ac1cc03aaa02e56644adb24 (round-5 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-FC2-b.round5.json). Delta dde0486b..e896b7a4 read in full for the slice: L04.html hunks at lines 51, 111, 120, 133-136 (lab docstring), 243, 248, 258, 262; L05.html at 51, 301, 310, 483, 517; L06.html at 171-175 (lab docstring); tests/labs/FC2/lab-FC2-L04-1.py line 11; tests/labs/FC2/lab-FC2-L06-1.py lines 4-9; cards.json: FC2-c059, c060, c081, c082 changed, c184 and c185 added, c176 removed (c046 and c050 are L03, outside the slice).",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyS6-FC2-b",
  "scratch": "ledgers/FC2/scripts/FC2-b-r6/ (all scripts and outputs; nothing written outside the checkout)",
  "verified_at": "2026-11-09T00:00:00+00:00",
  "verdict": "FAIL",
  "rows": rows,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Scope: slice b = L04.html, L05.html, L06.html; lab twins tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py; the 72 slice cards (L04 18, L05 25, L06 29) in course/modules/FC/FC2/cards.json.",
    "Carry rule: a PASS row is carried only when its cited subject is byte-identical since dde0486b (git diff dde0486b e896b7a4). Rows whose subject changed were re-verified from scratch: L04 lines 51, 111, 120, 133-136, 243, 248, 258, 262; L05 lines 51, 301, 310, 483, 517; L06 lines 171-175; cards c059, c060, c081, c082, c184, c185 and c176. The round-5 FAIL rows (FC2b-plan-L04-no-L05-result, FC2b-cards-hypotheses, FC2b-cards-delta-round1) were re-verified and now PASS.",
    "Mutation testing: not applicable. Slice b has no project grader; per the rulings mutants apply only to project graders. mutants is empty. Gate evidence for the unit (run_graders 50/50 seeds) is recorded in FC2b-cmd-run_graders.",
    "Judgement, accepted and not failed: L04.html:262 says exercising at once is never better than selling. It follows from Proposition 2.2 (proved in L04) and expressly leaves holding against selling open; it is not the plan's 'early exercise of a non-dividend call is never optimal' result, which Theorem 4.1 in L05 proves. The architect may read plans/FC2-build-plan.md lines 431-432 more broadly; if so, record a ruling.",
    "Observation, not a row: Theorem 4.1 (L05.html:301) lists (N) among its hypotheses, but its proof (L05.html:303-306) never invokes (N). A superset of hypotheses is not a failure under the rules; the builder may keep or drop (N) from the statement and from its Remark 4.2 and card FC2-c071.",
    "Observation, not a row: the lab twin docstrings (L04 line 11, L06 lines 4-9) were re-checked against the outputs: the L06 cents list now matches the printed cents lines exactly (see FC2b-lab-L06-docstring). D sweep of the L05 construction (l05_d_sweep_r6.txt): the docstring claims (bound violations at D = 1/100, convexity holding for every tested D, every check holding at D = 9/10) match.",
    "Committed state note: ledgers/FC2/FC2-b.json as committed at the checkout pin is a round-7 fragment for pin 0d2d0f3 (an ancestor of e896b7a4). It was overwritten in the checkout's working tree by this round-6 fragment as the task specifies; nothing was committed.",
    "Not checked: a browser screenshot or visual review of L04-L06 (page_smoke geometry and console checks passed; no visual review); the live verify_refs run (network; no L04-L06 page cites a key); the hub, L01-L03, L07-L08 and project pages except where the unit gates cover them; the L03 card changes FC2-c046 and c050 (outside the slice); the full curriculum source for lesson hours (only the hub split and data-hours were checked); the A3 and A2 modelling choices themselves (hypotheses, not proved).",
  ],
  "summary": "FC2 slice b round 6 (pin e896b7a4, delta from dde0486b): 71 rows, 70 PASS, 1 FAIL. The FAIL is low severity: FC2b-define-before-use-N (L05.html:51 uses the hypothesis label (N) before it is defined at L05.html:76; introduced by this delta). The three round-5 FAIL rows are fixed and PASS. All gates pass in this checkout: check_pages, check_dag, check_projects, run_graders (50/50 seeds), run_labs (unit 11/11 and each page), page_smoke (L04, L05, L06 alone), twins under python -I -W error with exact output match, ruff, mypy --no-incremental, pytest subsets, verify_refs --offline.",
}
json.dump(fragment, open("ledgers/FC2/FC2-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open("ledgers/FC2/FC2-b.json", "a", encoding="utf-8").write("\n")
print("rows", len(rows), "PASS", sum(r["status"] == "PASS" for r in rows), "FAIL", sum(r["status"] == "FAIL" for r in rows))
