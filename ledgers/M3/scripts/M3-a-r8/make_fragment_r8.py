import json, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyB8-M3-a"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/B-M3-a.round7.json", encoding="utf-8"))
CARRY = ("Carried from round 7 (cited lines byte-identical since 7aa909e; delta 7aa909e..ce7b382 hunks in this "
         "file are outside the cited lines: L01.html 171-180,487; L02.html 7,583; L03.html 411-476; cards.json "
         "hunks at lines 31,58,129,245,368,524,590,850,929,1153): ")
# rows re-verified this round (fresh evidence)
fresh = {
 "a6-L01-indep-rank-thms": "Re-verified round 8: Theorem 3.8 (L01.html:171-180) changed only by the basis letter c->d (diff 7aa909e..ce7b382). Hypothesis, proof logic (Theorem 3.7 applied with k>m, symmetric argument) unchanged and correct. Other statements in 126-180 byte-identical. Letter collision recorded in a8-L01-notation-d.",
 "a6-L01-problems": "Re-verified round 8: R1 solution (L01.html:487) rewritten. Checked: Lemma 3.4 uses pivot inversion only (scalar-field properties ok for Q); Section 4 bullet 'The field is the reals' (L01.html:376) says results are not claimed for other scalar fields, matching the solution; Lab 1 uses fractions.Fraction (tests/labs/M3/lab-M3-L01-1.py:21,49,144). Other problem solutions in 408-503 byte-identical. The R1 solution's new sentence is a correct claim.",
 "a6-L01-structure-prose": "Re-verified round 8: changed lines L01.html:171-180 and 487 scanned for process words (grep -i builder|verifier|round|fragment|TODO|agent|claude) on index, L01-L03: no matches in L01-L03 learner text. Honest gap: unchanged regions carried line-by-line from round 7 only.",
 "a6-L02-quiz-keyresults": "Re-verified round 8: q9 distractor (L02.html:583) now 'That the 7 rejected draws were invertible'; the lab prints 'singular draws of P rejected before an invertible P was found: 7' (L02.html:351; twin run output) and the explanation at L02.html:359 says the 7 draws are singular; recount (scripts M3-a-r8/recount.out) gives rejected 7. Keys for q1-q10 unchanged apart from this line.",
 "a6-L02-structure-prose": "Re-verified round 8: changed lines L02.html:7 (meta description, P^-1 A P) and 583 (quiz option) scanned; no process words; grep -i (builder|verifier|round|fragment|TODO|agent|claude) on L02.html: only a learner exercise 'Verify the computation of Example 4.3' (L02.html:456), not a process word. Honest gap: unchanged regions carried from round 7.",
 "a6-L03-quiz-keyresults": "Re-verified round 8: the only L03 change in 389-487 is adding style=\"min-inline-size: 0\" to six <fieldset> tags (L03.html:411,425,439,448,462,476). git diff 7aa909e..ce7b382 shows no change to prompts, options, data-correct or explanations.",
 "a6-L03-structure-prose": "Re-verified round 8: the only L03 change is the six fieldset style attributes (L03.html:411-476); no prose changed. Process-word grep on L03.html: no matches.",
 "a6-dag-concepts": "Re-run round 8: .venv/bin/python tools/check_dag.py --all -> 'check_dag CF1: PASS', 'check_dag AP1: PASS', exit 0 (scripts M3-a-r8/check_dag.out). Concept links in index/L01-L03 unchanged except the rename and style edits.",
 "a6-render-page-smoke": "Re-run round 8: tools/page_smoke.py --unit M3 -> 'page_smoke M3: PASS', exit 0 (scripts M3-a-r8/page_smoke.out). The L03 fieldset style change is covered by the horizontal-scroll check.",
 "a6-gates-lint-types": "Re-run round 8: ruff check tests/labs/M3 -> All checks passed; ruff format --check -> 12 files already formatted; mypy --no-incremental on the three M3 L01-L03 twins -> Success: no issues found in 3 source files; pytest tests/test_labs.py -k M3 -> 12 passed (scripts M3-a-r8/ruff.out, mypy.out, pytest_m3.out). tests/labs/M3 is byte-identical since 7aa909e (no twin in the delta).",
 "a6-L01-lab-twin-page": "Re-run round 8: twin_vs_page.py (scripts M3-a-r8/twin_vs_page.out): L01 page code == twin True, twin exit 0 under python -I -W error, expected == output True; L02 and L03 likewise. tools/run_labs.py --unit M3 -> 'run_labs M3: PASS (12/12)'.",
 "a6-L01-lab-numbers": "Re-run round 8: numpy recount (scripts M3-a-r8/recount.py, recount.out): L01 counts 188, 0, 198, 0; planted dependent 100, independent triples 100, rank-3 100. Matches L01.html:355 expected output and card M3-c016..c019.",
 "a6-L02-lab-twin-page": "Re-run round 8: twin_vs_page.py L02 page code == twin True; twin exit 0; expected == output True (scripts M3-a-r8/twin_vs_page.out).",
 "a6-L02-lab-numbers": "Re-run round 8: numpy recount (recount.out): rejected 7, formula 50, composition 50, first matrix [[3,-17.5,12.333],[0,5,-1.667],[-2,8,-6]] matches L02.html:349-357 output 3 -35/2 37/3 / 0 5 -5/3 / -2 8 -6.",
 "a6-L02-notation-S": "Carried from round 7 (cited lines byte-identical since 7aa909e): the round-8 L02 changes are at lines 7 and 583, which contain no S symbol.",
 "a6-notation-registry": "Carried from round 7 (cited lines byte-identical since 7aa909e): round-8 changes (L02.html:7, 583; L01.html:171-180, 487; L03 fieldsets) do not touch any registered symbol; notation/notation.json is not in the delta. Local-letter collision on L01 handled in a8-L01-notation-d.",
 "a6-hub-data-claims": "Carried from round 7 (cited lines byte-identical since 7aa909e): index.html is unchanged in the delta; project.html hunks in 7aa909e..ce7b382 are at lines 37 and 229-622 (outputs), none at 53,60,103,185,289,292.",
 "a6-hub-cards": "Carried from round 7 (cited lines byte-identical since 7aa909e): index.html unchanged; L01-L03 h1 lines unchanged (hunks at L01 171-180,487; L02 7,583; L03 411-476).",
 "a6-hub-m1-refs": "Carried from round 7 (cited lines byte-identical since 7aa909e): index.html unchanged; L01.html:37 not in any hunk.",
}
for r in prev["rows"]:
    rid = r["id"]
    if rid in fresh:
        r["status"] = "PASS"
        r["evidence"] = fresh[rid]
    elif r["status"] == "PASS":
        r["evidence"] = CARRY + r["evidence"].replace("Carried from round 6 (cited locator bytes unchanged since 44f1eb6; hunk list 44f1eb6..7aa909e checked, no hunk inside the cited lines): ", "").replace("Carried from round 6 (cited locator bytes unchanged since 44f1eb6; hunk list 44f1eb6..7aa909e checked, no hunk inside the cited lines):", "")
    # a7 FAIL rows: fixed and re-verified in round 8
    if rid == "a7-L02-card-M3-c036":
        r["status"] = "PASS"
        r["evidence"] = ("Re-verified round 8: cards.json card M3-c036 (line 245-246) now reads 'If Ã = P^{-1} A P with P invertible, what is A in terms of Ã?' back 'A = P Ã P^{-1} (Corollary 4.2)', matching L02.html:167-172 (Theorem 4.1, Corollary 4.2 with widetilde A) and the Corollary's proof.")
    if rid == "a7-L02-meta-description-B":
        r["status"] = "PASS"
        r["evidence"] = ("Re-verified round 8: L02.html:7 meta description now reads 'the change-of-basis formula P^-1 A P proved', so B no longer names the matrix; B is the basis symbol only (L02.html:153, Theorem 4.1). Locator grep shows no matrix use of B on L02.")
rows = prev["rows"]
new = [
 {"id": "a8-L01-card-c014", "check": "cards agree with current lesson text (round-8 rename c->d)",
  "location": "course/modules/M/M3/cards.json:92 (card M3-c014); course/modules/M/M3/L01.html:174",
  "status": "FAIL",
  "evidence": "Card M3-c014 back still reads 'If b1, ..., bm and c1, ..., ck are both bases ... then m = k (Theorem 3.8, invariance of dimension)'. Round 8 changed Theorem 3.8 to 'a basis b_1, ..., b_m and a basis d_1, ..., d_k' (L01.html:174) and the proof to d_1..d_k (L01.html:179). The card no longer matches the lesson text, which the rules require (VERIFIER_RULES item 10).",
  "fix": "Change card M3-c014 back to 'If b1, ..., bm and d1, ..., dk are both bases ...' (or revert the letter once the notation item below is fixed, using the same letter in both places)."},
 {"id": "a8-L01-notation-d", "check": "notation: one meaning per symbol on the page (precedent: round-7 row a7-L02-meta-description-B)",
  "location": "course/modules/M/M3/L01.html:103, 174, 179, 494",
  "status": "FAIL",
  "evidence": "On L01 the symbol d now means three things: basis vectors d_1..d_k (L01.html:174,179, Theorem 3.8); scalar coefficients y = sum_i d_i v_i (L01.html:103, proof of Proposition 2.2); polynomial degrees d_1..d_m (L01.html:494, Problem set solution). A letter that names a basis in one place and a degree or coefficient in another breaks the one-meaning-per-page rule applied in round 7 to B. Note: the earlier c_1..c_k basis letter (round 7 PASS) had the same class of collision with the coefficients c_i in Definition 3.1 (L01.html:115) and in Lemma 3.4 onward; round 7 passed it, which was a miss.",
  "fix": "Pick a letter with no other use on L01 (grep -F 'f_' on L01.html returns 0 hits; f_1..f_k is free), rename L01.html:174 and 179 and card M3-c014 back, and re-run check_pages and the card check."},
 {"id": "a8-L01-thm38-math", "check": "2.4 mathematics: Theorem 3.8 after the rename",
  "location": "course/modules/M/M3/L01.html:171-180",
  "status": "PASS",
  "evidence": "Read the changed hunk: only the second basis letter changed (c->d) in the statement (line 174) and the proof (line 179). Hypothesis (finite bases, real vector space) and the argument (Theorem 3.7 with k>m gives dependence of d_1..d_k, contradiction; symmetric step gives m<=k) are unchanged and correct. Other statements in 126-180 are byte-identical."},
 {"id": "a8-L02-q9-option", "check": "2.9 quiz distractor vs lab output",
  "location": "course/modules/M/M3/L02.html:583 and 351",
  "status": "PASS",
  "evidence": "Distractor 'That the 7 rejected draws were invertible' is false: L02.html:351 prints 'singular draws of P rejected before an invertible P was found: 7' and L02.html:359 says the 7 rejected draws are singular matrices P. Recount rejected 7 (recount.out). The correct option ('Agreement on the 50 seeded pairs') unchanged."},
 {"id": "a8-cards-c005-c009-c019", "check": "cards agree with current lesson text (L01)",
  "location": "course/modules/M/M3/cards.json:31 (c005), 58 (c009), 129-130 (c019)",
  "status": "PASS",
  "evidence": "c005 matches Proposition 2.2 (L01.html:97, smallest subspace). c009 back 'leave the solutions of Ac = 0 unchanged (Definition 3.3)' matches Definition 3.3 (L01.html:127). c019 'how many of the 200 seeded lists of four vectors in R^3 are independent' -> '0 of 200 (Lab 1 output)' matches expected line R^3, 4 vectors: independent in 0 of 200 (L01.html:355; run_labs output). Corollary 3.6 cited for the prediction. Numbers in every L01 card back appear in L01.html (script M3-a-r8/cards_l1to3.py prints no missing numbers)."},
 {"id": "a8-card-c054", "check": "cards agree with current lesson text (L03)",
  "location": "course/modules/M/M3/cards.json:366-368 (card M3-c054); L03.html:358",
  "status": "PASS",
  "evidence": "Card back: dim E_1 = 2 minus rank(B-I), rank 1, so dim E_1 = 1 (Problem E3; Lesson 1, Proposition 3.12). L03.html:358 solution gives (B-I)(x,y)=(y,0), E_1 = {(x,0)}, dimension 1 = 2 - rank. Rank-1 claim re-derived by hand: B-I = [[0,1],[0,0]]."},
 {"id": "a8-L03-fieldset-style", "check": "page structure: fieldset change is style-only",
  "location": "course/modules/M/M3/L03.html:411,425,439,448,462,476",
  "status": "PASS",
  "evidence": "git diff 7aa909e..ce7b382 for L03.html: six hunks, each replacing <fieldset> with <fieldset style=\"min-inline-size: 0\">. No text, option or key changed. page_smoke M3 PASS (no horizontal scroll at 360 px)."},
 {"id": "a8-process-words", "check": "2.9 learner text free of process words",
  "location": "course/modules/M/M3/index.html, L01.html, L02.html, L03.html",
  "status": "PASS",
  "evidence": "grep -i -E 'builder|verifier|verif|round [0-9]|fragment|TODO|TBD|FIXME|agent|claude|we will|I will|pending review|in review' over the four files: one match, L02.html:456 'Verify the computation of Example 4.3 without using the lab' (a learner instruction, not a process word). Output in M3-a-r8/process_words.out."},
 {"id": "a8-run-labs-m3", "check": "2.5 labs: all M3 inline labs run and match pages",
  "location": "tools/run_labs.py --unit M3; tests/labs/M3/lab-M3-L0{1,2,3}-1.py",
  "status": "PASS",
  "evidence": "tools/run_labs.py --unit M3 -> 'run_labs M3: PASS (12/12)', exit 0 (M3-a-r8/run_labs.out). tests/test_labs.py -k M3 -> 12 passed (pytest_m3.out)."},
 {"id": "a8-gates-check-pages", "check": "2.9 structure gates",
  "location": "tools/check_pages.py --unit M3; tools/check_dag.py --all",
  "status": "PASS",
  "evidence": "check_pages M3: PASS (check_pages.out). check_dag --all: CF1 PASS, AP1 PASS, exit 0 (check_dag.out)."},
]
frag = {
 "unit": "M3", "slice": "a", "round": 8,
 "verifier": "independent Haiku verifier (round 8), not a builder of M3",
 "pin": "ce7b382",
 "base": "7aa909e (round-7 pin); delta 7aa909e..ce7b382 read for slice a: index.html unchanged; L01.html 171-180 (Thm 3.8 letter c->d), 487 (R1 solution); L02.html 7 (meta), 583 (q9 option); L03.html 411-476 (fieldset style only); cards.json M3-c005, c009, c014 (not changed, still stale), c019, c036, c054; tests/labs/M3 unchanged",
 "checkout": ROOT,
 "scratch": ROOT + "/ledgers/M3/scripts/M3-a-r8",
 "verified_at": "2026-10-29T02:45:00+00:00",
 "verdict": "FAIL",
 "rows": rows + new,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": ("Lesson slice: mutants not required (VERIFIER_RULES 2.6 is for project slices); none run. "
   "Round-8 fresh evidence: twin_vs_page.py, recount.py, cards_l1to3.py, run_labs --unit M3, check_pages --unit M3, check_dag --all, page_smoke --unit M3, ruff, mypy --no-incremental, pytest tests/test_labs.py -k M3. "
   "Not checked: verify_refs live run (no references/ change in the delta; round-7 ran --offline only); full line-by-line re-read of unchanged regions of L01-L03 (carried by the byte-identical-locator rule, as in round 7); project.html and L04-L09 (other slices). "
   "Fixes needed before a PASS: a8-L01-card-c014 and a8-L01-notation-d (rename Theorem 3.8's basis letter on L01.html:174,179 to a letter unused on L01, e.g. f, and change card M3-c014 to match)."),
 "summary": ("Slice a round 8: 2 FAIL rows (a8-L01-card-c014: card M3-c014 still cites c_1..c_k after the Theorem 3.8 rename to d_1..d_k; a8-L01-notation-d: d means basis vectors, coefficients and degrees on L01). "
   "Both round-7 FAIL rows (a7-L02-card-M3-c036, a7-L02-meta-description-B) are fixed and re-verified PASS. "
   "All other rows PASS (carried or re-verified). Verdict FAIL."),
}
out = "/Users/billyribeiro/.fanout/wt/verifyB8-M3-a/ledgers/M3/M3-a.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("rows", len(frag["rows"]), "FAIL", sum(r["status"] == "FAIL" for r in frag["rows"]))
