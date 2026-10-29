import json, sys
from pathlib import Path
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyB13-CS2-d")
P = "Carried from round 12 (cited lines byte-identical since pin ff38842):"
Q = "Carried from round 12 (cited files byte-identical since pin ff38842):"
R = lambda i, check, loc, status, ev: {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
rows = [
 R("D-01", "2.1 citations: registry key used by project.html", "course/modules/CS/CS2/project.html:411-413; references/references.json", "PASS",
   P + " project.html:411-413 unchanged. Re-run: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'."),
 R("D-02", "2.5 labs: Lab 1 prose and printed numbers", "course/modules/CS/CS2/project.html:55,145,389; tests/labs/CS2/lab-CS2-project-1.py", "PASS",
   "Re-run this round: run_labs --unit CS2 -> 'run_labs CS2: PASS (14/14)'; lab-CS2-project-1.py alone under python -I -W error exit 0."),
 R("D-03", "2.2 numbers: Lab 2 prose and expected output", "course/modules/CS/CS2/project.html:149-151,185-188; tests/labs/CS2/lab-CS2-project-2.py:1-20", "PASS",
   "Re-run this round: run_labs PASS; twin alone exit 0. Lab-2 twin byte-identical since ff38842 (git diff stat empty for tests/labs/CS2). Page 149-151 and 185-188 unchanged."),
 R("D-04", "2.2 numbers: Lab 3 prose and expected output", "course/modules/CS/CS2/project.html:329-338; tests/labs/CS2/lab-CS2-project-3.py", "PASS",
   "Re-run this round: run_labs PASS; twin alone exit 0; lab-3 twin and page 329-338 unchanged since ff38842."),
 R("D-05", "2.6 spec: the ten named ValueError conditions each have a test", "course/modules/CS/CS2/project.html:209,224; grader/test_project.py", "PASS",
   "Re-verified (line 209 changed this delta: 'every number' -> 'the numbers'; the ten conditions text is unchanged, checked word by word against ff38842). run_graders CS2 seeds 0-49: PASS (reference 50/50). Grader byte-identical."),
 R("D-06", "2.6 spec: value and window rules of Constraints", "course/modules/CS/CS2/project.html:209; grader/test_project.py", "PASS",
   "Re-verified: line 209 text changed only in the article 'every'->'the'; value and window rules unchanged. Alternatives A and B (below, D-14) pass 10/10 seeds, so no over-constraint in the rules as worded."),
 R("D-07", "2.6 grader: documented test count equals collect-only count", "course/modules/CS/CS2/project.html:211; grader/test_project.py", "PASS",
   "Re-verified: project.html:211 changed only by the added '(defined under Conventions below)' parenthetical. Collect-only in a workspace built like tools/run_graders.py (CS2-d-r13/mkws.sh, reference as streamstats.py): '171 tests collected'. Page states 171."),
 R("D-08", "2.6 grader: Constraints and Grading paragraph structure", "course/modules/CS/CS2/project.html:219; grader/test_project.py", "PASS",
   "Re-verified: project.html:219 is the 'Exact counts' bullet; this delta changed it (added 'The rank target is the smallest integer at or above qn − εn.'). Grader unchanged. The page's rank definition is checked in D-42, which FAILS on a clamp the sentence omits."),
]
rows += [
 R("D-09", "2.6 grader: instance.py cases", "course/modules/CS/CS2/grader/instance.py:8-13", "PASS", P + " grader/instance.py byte-identical; grader run PASS."),
 R("D-10", "2.6 grader: Constraints vs instance checks", "course/modules/CS/CS2/project.html:198; grader/instance.py:27-50", "PASS", P + " project.html:198 unchanged; instance.py byte-identical."),
 R("D-11", "2.6 grader: reference and starter", "course/modules/CS/CS2/grader/reference.py; grader/starter.py", "PASS", P + " grader files byte-identical; reference 50/50 seeds."),
 R("D-12", "2.6 grader: reference algorithms", "course/modules/CS/CS2/grader/reference.py:94-143", "PASS", P + " reference.py byte-identical; re-read this round at lines 16-52 and 103-143."),
 R("D-13", "2.6 grader: reference rank target", "course/modules/CS/CS2/grader/reference.py:95-101", "PASS", P + " reference.py byte-identical. Target line is max(1, ceil(...)) at line 137 (see D-42 for the prose consequence)."),
 R("D-14", "2.6 grader: correct alternatives pass", "ledgers/CS2/scripts/CS2-d-r13/alts/*", "PASS",
   "Re-run this round on new alternatives: alt_r13_A (sketch never compresses, exact sorted-rank semantics) 10/10 seeds rc 0 (171 passed each); alt_r13_B (rank target as -floor(epsilon n - qn)) 10/10 seeds rc 0. Prior round's 13 alternatives not re-run (grader byte-identical)."),
 R("D-15", "2.6 grader: mutation gate", "ledgers/CS2/mutants/ (108 files)", "PASS",
   "Re-run this round: tools/mutate_graders.py --unit CS2 -> 'FAIL (101/104 killed)', CS2-d-r13/mutate.out. Survivors are the same three carried mutants d8_01, d8_02, d9_04, which the round-11 ruling treats as correct solutions under the stated guarantee; the gate exit 1 is the known carried state, not a new survivor. No new grader survivor."),
 R("D-16", "2.6 grader and labs: suite and twins are the contract's objects", "tests/labs/CS2; course/modules/CS/CS2/grader", "PASS", P + " tests/labs/CS2 and grader byte-identical since ff38842; re-run this round."),
 R("D-17", "2.2 labs: printed rows match prose", "tests/labs/CS2/lab-CS2-project-1..3.py; project.html:53-146, 262-337", "PASS", "Re-run this round: run_labs PASS 14/14; all three twins exit 0 alone."),
 R("D-18", "2.7 structure: sections and headings", "course/modules/CS/CS2/project.html", "PASS", "Re-verified: page_smoke CS2 PASS this round; heading changes of this delta (none new beyond line 209-219 prose) do not alter structure."),
 R("D-19", "2.8 hours arithmetic", "course/modules/CS/CS2/project.html:33, 233-241; course/modules/CS/CS2/index.html (data-hours-lessons)", "PASS", P + " project.html:33 and 233-241 unchanged; index.html unchanged."),
 R("D-20", "2.4 project spec: Output and Example block", "course/modules/CS/CS2/project.html:348-391", "PASS", P + " lines 348-391 unchanged (delta hunks at 209, 211, 219 only)."),
 R("D-21", "2.4 project spec: sample numbers", "course/modules/CS/CS2/project.html:372, 383-390", "PASS", P + " lines unchanged."),
 R("D-22", "2.3 notation: symbols", "course/modules/CS/CS2/project.html; notation/notation.json", "PASS", "Re-verified: new prose uses q, n, ε and 'rank target' only; ε and n already defined at project.html:216 and 219 before this delta; notation.json unchanged (byte-identical since ff38842). 'rank target' is a term, defined at line 219 (see D-42)."),
 R("D-23", "2.6 spec: Constraints wording vs. grader", "course/modules/CS/CS2/project.html:198, 209, 218", "PASS", "Re-verified: line 209 changed by 'every'->'the' only; 198 and 218 unchanged; grader unchanged; run_graders PASS."),
 R("D-24", "2.9 structure: hub and lesson cross references", "course/modules/CS/CS2/project.html:42, 45, 149, 161; course/modules/CS/CS2/index.html:69-71, 161, 164", "PASS", P + " cited lines unchanged; check_pages CS2 PASS this round."),
 R("D-25", "2.7 requirements: test dependency pins", "course/modules/CS/CS2/project.html:249, 257; requirements-dev.txt:2", "PASS", P + " cited lines unchanged; requirements-dev.txt unchanged."),
 R("D-26", "2.7 page: link to starter", "course/modules/CS/CS2/project.html:426", "PASS", P + " line 426 unchanged; page_smoke PASS."),
 R("D-27", "2.10 cards: file integrity", "course/modules/CS/CS2/cards.json", "PASS",
   "Re-run this round: 206 cards, 206 unique ids, 206 unique fronts, grades T=131 C=75 (matches D-29 and D-28). Every number token in front/back appears in its own lesson text (0 misses)."),
 R("D-28", "2.10 cards: C-grade cards cite conjecture basis", "course/modules/CS/CS2/cards.json (C cards); course/modules/CS/CS2/L02-L11.html", "PASS", "Re-verified: no grade changes this delta (C count 75 unchanged); C cards' text unchanged except none; script check in D-27."),
 R("D-29", "2.10 cards: T cards match lesson", "course/modules/CS/CS2/cards.json (131 T cards); course/modules/CS/CS2/L01-L11.html", "PASS", "Re-verified: 131 T cards; numbers-in-lesson check 0 misses; changed T cards c089, c095, c096, c135 re-read against L07/L10 (D-39, D-40, D-43)."),
 R("D-30", "2.10 cards: sampled cards agree with lesson", "course/modules/CS/CS2/cards.json: CS2-c102, CS2-c023, CS2-c165, CS2-c063, c125, c195", "PASS", P + " these six cards are byte-identical in cards.json (diff of ff38842..fca6bb1 touches only c089, c095, c096, c135, and the round-12 set)."),
 R("D-31", "2.10 cards: no duplicate cards", "course/modules/CS/CS2/cards.json", "PASS", "Re-run this round: 206 unique ids and 206 unique fronts."),
 R("D-32", "2.10 cards: round-11 fixes and related cards", "course/modules/CS/CS2/cards.json: CS2-c137, CS2-c153, CS2-c133, c033, c037, c091, c096, c112", "PASS",
   "Re-verified: c096 changed this delta and is re-read against L07 Proposition 4.2 and the 2^40 arithmetic (41 bits; 2^40 + 1 > 10^12). c137, c153, c133, c033, c037, c091, c112 unchanged since ff38842 (diff contains no hunk at them)."),
 R("D-33", "2.6 spec: grading line count and Constraints", "course/modules/CS/CS2/project.html:209, 220; grader/test_project.py", "PASS", "Re-verified: 209 and 220 read this round; grader collect-only 171; run_graders PASS."),
 R("D-34", "2.9 structure: Rung 3 matches the curriculum scope (rolling mean)", "course/modules/CS/CS2/project.html:196, 216; curriculum/curriculum.json:6708; curriculum/01-foundations.yaml:445", "FAIL",
   "Re-verified from scratch this round: curriculum.json:6708 brief reads 'Implement O(1)-update rolling mean, variance (Welford), min/max (monotonic deque) and an approximate quantile sketch'; 01-foundations.yaml:445 has the same phrase. project.html:216 reads 'the Welford statistics are cumulative', and the page has no rolling mean (grep 'rolling mean' in project.html and index.html: no match). Brief and page disagree. Fix: architect decision (add a rolling mean to the page, or correct the brief and regenerate the curriculum). Not a verifier fix."),
 R("D-35", "2.1 page-level cross-check of grader, labs and cards", "course/modules/CS/CS2/project.html; course/modules/CS/CS2/cards.json; grader/*.py; tests/labs/CS2/*.py", "PASS", "Re-run this round: run_graders PASS, run_labs 14/14, page_smoke CS2 PASS, check_pages/check_dag/check_projects CS2 PASS, verify_refs offline 0 problems, mypy strict on tests/labs/CS2 'Success: no issues found in 14 source files', ruff check tests/labs/CS2 'All checks passed!'."),
 R("D-36", "2.2 numbers: Lab 1 and project body text", "course/modules/CS/CS2/project.html:353-354, 369-370, 380-383, 355", "PASS", P + " lines unchanged."),
 R("D-37", "2.6 grader: quantile rounding trap", "course/modules/CS/CS2/grader/test_project.py (~line 868); ledgers/CS2/mutants/d8_04_quantile_rounds_q_to_six_places.py", "PASS", "Re-run this round: mutate_graders list includes d8_04 killed (gate output CS2-d-r13/mutate.out)."),
 R("D-38", "2.6 grader: round-11 mutants", "ledgers/CS2/mutants/d11_01..04", "PASS", "Re-run this round as part of tools/mutate_graders.py --unit CS2: all four killed."),
 R("D-39", "2.10 cards: L03, L07, L08 cards", "course/modules/CS/CS2/cards.json; course/modules/CS/CS2/L03.html, L07.html, L08.html", "PASS",
   "Re-verified for the changed L07 cards: c089 (f(6)=2 by 3+3; largest-coin-first 4+1+1, three coins) matches L07 'uses 4 + 1 + 1, three coins, while 3 + 3 uses two (Example 2.4)'. c095 (first failure at amount 6, Problem P3) matches L07 'The smallest amount where the rule fails for this set is 6 (Problem P3)'; hand check: greedy optimal for amounts 1..5. c096 matches L07 Proposition 4.2 and the 2^40 arithmetic. L03 and L08 cards unchanged."),
 R("D-40", "2.10 cards: L09 cards", "course/modules/CS/CS2/cards.json; course/modules/CS/CS2/L09.html 117-138", "PASS", P + " cards in L09 and lines 117-138 unchanged."),
 R("D-41", "2.6 grader: round-12 mutants", "ledgers/CS2/mutants/d12_01, d12_02, d12_03", "PASS", "Re-run this round as part of the gate: d12_01, d12_02, d12_03 killed (gate output)."),
]
rows.append(R("D-42", "2.5 project prose: rank target definition vs reference code", "course/modules/CS/CS2/project.html:219; course/modules/CS/CS2/grader/reference.py:137", "FAIL",
   "New sentence in this delta: 'The rank target is the smallest integer at or above qn − εn.' The reference computes target = max(1, ceil(qn − εn)) (reference.py:137). For q = 0, n = 5, epsilon = 0.1: qn − εn = −0.5, the literal sentence gives 0, the code gives 1 (python check this round). The lower-bound inequality is vacuous there, so the guarantee holds, but the stated definition is not the code's. Fix: add 'and at least 1' to the sentence at project.html:219 (or state the clamp)."))
cards_rows = [
 R("D-43", "2.10 cards: changed T cards c135 (L10)", "course/modules/CS/CS2/cards.json: CS2-c135; course/modules/CS/CS2/L10.html", "PASS",
   "Re-verified: front/back read against L10: Corollary 2.5(c) 'one insertion can remove w entries'; step (1) removes candidates 'at least' the new value for the minimum version (L10 'The maximum version replaces at least in step (1) by at most'). Series x0<...<x(w-1) then a lower value: step (1) removes all w entries. Numbers all appear in L10."),
]
rows += cards_rows
mutants = [
 {"id": "r13_01", "name": "r13_01_welford_skips_repeated_value.py", "description": "Welford update returns early when x equals the current mean, so the count and M2 miss that value.", "killed_by": "test_welford_constant_stream_has_zero_variance (seed 0)"},
 {"id": "r13_02", "name": "r13_02_sample_variance_of_two_values_is_zero.py", "description": "variance(1) returns 0.0 when exactly two values were added.", "killed_by": "test_welford_sample_variance_of_two_values_is_defined (seed 0)"},
 {"id": "r13_03", "name": "r13_03_rank_slack_uses_n_plus_one.py", "description": "rank target uses ceil(qn - epsilon(n+1)), so the lower rank bound can be missed by one rank.", "killed_by": "test_sketch_rank_guarantee_on_short_streams[2-0.2] and 5 more (seed 0); 10/10 seeds fail"},
 {"id": "r13_04", "name": "r13_04_quantile_returns_predecessor.py", "description": "quantile returns the stored value one position before the rank target.", "killed_by": "test_sketch_value_that_denotes_a_number_is_refused_or_correct[True-1.0] and 31 more (seed 0)"},
]
frag = {
 "unit": "CS2", "slice": "d", "round": 13,
 "verifier": "independent verifier (Haiku), round 13",
 "pin": "fca6bb104984c6a724fc214d8073158e610e995a",
 "base": "ff388424d9d056b7a57868dab5ae7f7cdeef60f6",
 "checkout": str(ROOT), "scratch": "ledgers/CS2/scripts/CS2-d-r13",
 "verified_at": "2026-10-29T12:00:00+00:00",
 "verdict": "FAIL", "rows": rows, "mutants": mutants,
 "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Delta since round-12 pin ff38842 (fca6bb1 commit touches only project.html and cards.json): project.html:209 (article change), :211 (parenthetical), :219 (new rank-target sentence); cards.json c089, c095, c096, c135. Every hunk read; each changed card re-read against L07/L10.",
  "Round-12 FAIL D-34 unchanged and re-verified (FAIL). New FAIL D-42: rank-target sentence vs reference clamp max(1, ceil(...)).",
  "Gate: tools/mutate_graders.py --unit CS2 exits 1 with 101/104 killed; same three carried survivors (d8_01, d8_02, d9_04). Four new mutants r13_01..04 are killed; a first attempt at a fifth (rank slack n-1) survived because it is a correct variant under the guarantee, so it was dropped and replaced by r13_03 (n+1), which is a real violation.",
  "Environment: pytest on course/modules/CS/CS2/grader/test_project.py needs the workspace of tools/run_graders.py (streamstats.py); direct collection in the checkout fails with ModuleNotFoundError, as expected; collection in the workspace gives 171.",
  "Not checked: full pytest suite beyond CS2 slice, page_smoke full sweep (ran with --skip-sweep), the 13 round-12 alternatives (not re-run; grader byte-identical), visual layout beyond page_smoke, the non-CS2 tests/test_labs.py cases.",
 ],
 "summary": "Slice d round 13: FAIL. 43 rows: 40 PASS, 2 FAIL (D-34 brief/page rolling-mean scope, architect decision; D-42 rank-target sentence omits the max(1, .) clamp, one-line fix). Round-12 mutant gate unchanged (101/104). Four new mutants r13_01..04 killed.",
}
out = ROOT / "ledgers/CS2/CS2-d.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False), encoding="utf-8")
print(sum(1 for r in rows if r["status"] == "PASS"), "PASS;", [r["id"] for r in rows if r["status"] != "PASS"])
