"""Round 5 verifier (M3-c): builds ledgers/M3/M3-c.json from the round-4 row ids.

Rows re-checked this round carry fresh evidence (commands run on pin 09b8751, or the full read of L07-L09 with the
line cites given). Rows whose cited subject is byte-identical since the round-4 pin 2657ab5 are carried, with the
prefix the brief requires. Run from the checkout: python -I ledgers/M3/scripts/M3-c-r5/build_fragment_r5.py
"""
import json
from pathlib import Path

ROOT = Path("/tmp/verifyB5-M3-c")
prev = json.loads(Path("/tmp/fanout-frags/B-M3-c.round4.json").read_text())
old = {r["id"]: r for r in prev["rows"]}

CARRY_FILES = "course/modules/M/M3/cards.json (objects M3-c115..M3-c177 only; git diff 2657ab5 09b8751 changes cards of L02, L03, L06 only)"
CMD = "run this round on pin 09b8751"

fresh = {
 "M3c-cmd-pin": f"{CMD}: git rev-parse HEAD = 09b8751. git diff --stat 2657ab5 09b8751 lists no change to course/modules/M/M3/L07.html, L08.html, L09.html, tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py, or the slice cards (cards.json hunks only at L02, L03, L06; grep of the diff for lesson L07-L09 returns 0). Delta on the slice is empty.",
 "M3c-cmd-check-pages": f"{CMD}: .venv/bin/python tools/check_pages.py --unit M3 --page L07 -> 'check_pages M3 L07: PASS'; same for L08 and L09.",
 "M3c-cmd-check-dag": f"{CMD}: .venv/bin/python tools/check_dag.py --unit M3 -> 'check_dag M3: PASS'.",
 "M3c-cmd-run-labs": f"{CMD}: .venv/bin/python tools/run_labs.py --unit M3 -> 'run_labs M3: PASS (12/12)'; --page L07, --page L08 -> 'PASS (1/1)' each; L09 PASS (1/1) in the first run.",
 "M3c-cmd-twins-isolated": f"{CMD}: .venv/bin/python -I -W error tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py -> exit 0 each; stderr captured empty.",
 "M3c-cmd-embed-equal": "ledgers/M3/scripts/M3-c-r5/embed_and_numbers_r5.py (run by me, python -I -W error): for L07, L08, L09 the embedded code block equals the twin text (True) and the real run output equals the pre class=expected block (True); rc 0 each.",
 "M3c-cmd-page-smoke": f"{CMD}: .venv/bin/python tools/page_smoke.py --unit M3 --pages L07 L08 L09 --skip-sweep -> 'page_smoke M3: PASS', rc 0 (output kept at /tmp/M3-v/c/page_smoke_r5.txt).",
 "M3c-cmd-ruff-mypy": f"{CMD}: ruff check on the three twins -> 'All checks passed!'; ruff format --check -> '3 files already formatted'; mypy --no-incremental on the three twins -> 'Success: no issues found in 3 source files'.",
 "M3c-cmd-refs": f"{CMD}: tools/verify_refs.py --unit M3 (live) -> 'live re-verification of M3: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'. references/ is unchanged since the round-4 pin.",
 "M3c-cmd-build-site": f"{CMD}: .venv/bin/python tools/build_site.py --check -> 'site data current: 6 outputs' (course/assets/data/glossary.json changed in the delta; the check passes on the new state).",
 "M3c-cmd-pytest": f"{CMD}: .venv/bin/python -m pytest -q -k M3 -> exit 0 (12 dots, 100%).",
 "M3c-hours": f"{CMD}: data-hours of L01..L09 = 12,11,12,12,12,11,11,12,12, summing to 105 (L07 11, L08 12, L09 12 at L07.html:2, L08.html:2, L09.html:2). index.html data-hours-lessons=105 and data-hours-project=45 (index.html:29, changed in the delta) agree. Pace not judged (architect ruling).",
 "M3c-lab-docstrings-claims": "Read this round: lab-M3-L07-1.py docstring (lines 1-14: SIMULATED, seed 7, the statements of Theorem 1.2, 2.2, Remark 1.4; duplicated-column part), lab-M3-L08-1.py docstring (lines 1-14: seed 8, three planted factors, shares from unrounded eigenvalues printed to one decimal), lab-M3-L09-1.py docstring (lines 1-19: seed 20261028, 40 matrices, size 5, noise 0.35 per raw entry before symmetrising, counts scope). Each sentence matches the code and the embedded output.",
 "M3c-embed-exact-all": "ledgers/M3/scripts/M3-c-r5/embed_and_numbers_r5.py: all three embedded code blocks byte-equal their twins (after strip) and the three expected blocks equal the real run output.",
 "M3c-cos-shares-unrounded": "ledgers/M3/scripts/M3-c-r5/recompute_numbers_r5.py (written and run by me, own code): unrounded shares 75.8728, 18.0888, 5.1619 percent (print 75.9, 18.1, 5.2); unrounded |cos| level 0.999381, slope 0.998544, curvature 0.999019 (print 0.9994, 0.9985, 0.9990); misconception 1 'at least 0.9985' holds (0.998544 >= 0.9985).",
 "M3c-num-L07-E2": "L07.html:298 (E2 solution). Recomputed with recompute_numbers_r5.py: A^T y = (18.37970, 3.09586, -17.60350), so (18.38, 3.10, -17.60) at two decimals as printed in the solution. Check prints False for beta = 0 since max |A^T y| >= 1e-9.",
 "M3c-num-L07-lab-print": "L07.html:177-178, 196-197: recomputed beta = (1.332519, 0.848811, -0.411964) -> printed 1.3325 0.8488 -0.4120; residual norm 0.895128 -> printed 0.8951 (misconception 1 at L07.html:218 agrees).",
 "M3c-num-L07-worked": "L07.html:239 (M1: P = (1/2)[[1,1],[1,1]], p = (1,1), residual (1,-1)), 246-248 (M2: normal equations give beta1 = 1/2, beta0 = 7/6, fitted 7/6, 5/3, 13/6, residuals -1/6, 1/3, -1/6; sum 0; inner product with x 0), 255 (M3: 25 = 9 + 16). All re-derived by hand this round.",
 "M3c-math-L07-T12": "L07.html:63-81 read in full this round: Theorem 1.2 (a) G = A^T A invertible via x^T G x = ||Ax||^2 > 0 and the spectral theorem; (b) existence and uniqueness; (c) P symmetric, P^2 = P. Each step re-derived; the Fact 1.2 of Lesson 6 citation matches L06.html:64.",
 "M3c-math-L07-T13-T22-R14": "L07.html:83-121: Theorem 1.3 (strict closest point; expansion uses p-w in W orthogonal to y-p), Remark 1.4 (Pythagoras), Theorem 2.2 (least squares = projection; normal equations). Proofs re-derived; hypotheses (independent columns) stated in each statement.",
 "M3c-math-L07-P-R-problems": "L07.html:262-334: P1, P2, P3, R1, R2, R3 re-derived; R1 cites Theorem 3.7 of Lesson 1 (L01.html:161, a spanning list of n vectors bounds an independent list). R3 check: Q = I - P, Q^2 = Q, Qy orthogonal to W, Qy = 0 iff y in W.",
 "M3c-math-L07-R1-existence": "L07.html:316: existence by a maximal independent list in W of length at most n (L01 Theorem 3.7 at L01.html:161); spans W by maximality; W = {0} handled. Re-derived.",
 "M3c-math-L07-misconception2": "L07.html:222: P = diag(1,0) sends (3,4) to (3,0); P is identity only if W = R^n; P1 gives Py in W, so Py = y forces y in W. Re-derived.",
 "M3c-math-L07-misconception1-3": "L07.html:217-229: residual not zero for y outside W (Pythagoras), P = diag(1,0) has no inverse since P^2 = P and P = I would be false. Re-derived.",
 "M3c-math-L07-canon-normal-eq": "L07.html:209 (canon: independence needed for the formula; P3 gives singularity; Lab 1 non-unique coefficients). Consistent with P3 and the lab output lines 198-199.",
 "M3c-math-L07-why-normal-eq": "L07.html:52 (why-it-matters): normal equations and projection; cites Theorem 2.2(b) which states the normal equations (L07.html:112).",
 "M3c-simulated-L07-lab-text": "L07.html:132 (lab docstring of the page), 200 (interpretation): SIMULATED, seed 7, intercept 1.5, slopes 0.8 and -0.4, noise 0.3, and conditioning not tested; matches lab-M3-L07-1.py:3, 7, 28-29.",
 "M3c-num-L07-lab-intro-hypothesis": "L07.html:198 (hypothesis line that accompanies the interpretation: tolerance 1e-9, four-decimal coefficients, duplicated-column part) matches the lab's code and output (L07.html:190-199).",
 "M3c-num-L08-shares": "L08.html:284 (interpretation), 146 (hypothesis): 75.8728 -> 75.9, 18.0888 -> 18.1, 5.1619 -> 5.2 percent, from unrounded eigenvalues (recompute_numbers_r5.py). Cards M3-c139, M3-c140 are unchanged objects.",
 "M3c-num-L08-rescale": "L08.html:284, 374-377: rescaled first share 0.9791448785 -> 0.9791 and old 0.7587281517 -> 0.7587, as printed (recompute_numbers_r5.py).",
 "M3c-num-L08-M1": "L08.html:319-334 (M1 and M2 solutions) and the quiz near 460: X rows (1,2),(3,4),(5,9); centred squared norms 13, 1, 20; M = [[4,7],[7,13]]; trace 17; det 3; eigenvalues (17 +/- sqrt 277)/2. Re-derived by hand.",
 "M3c-num-L08-worked-misc": "L08.html:326, 333, 341, 448, 483-485: diag(4,1,1) shares 2/3, 1/6, 1/6; 9M scaling of M3 gives 18/27 and 9/27; quiz share 1/2 for eigenvalues 2,1,1; all re-derived.",
 "M3c-num-L08-E1-bound": "L08.html:146, 284, 374-377 and twin lab-M3-L08-1.py:114-120 (bound = 100 M11/(trace + 99 M11)). Recomputed: unrounded bound 0.9483461; from printed inputs 13.6818 and 88.2028 gives 0.9483461, so the four-decimal claim holds; 0.9483 lies between 0.7587 and 0.9791.",
 "M3c-num-L08-E3-rounding": "L08.html:389-391 (E3): rounded values 75.9+18.1+5.2 = 99.2; unrounded sum 99.1236 (recompute_numbers_r5.py) lies within the stated bound 99.2 +/- 0.15.",
 "M3c-num-L08-cosine-floor": "L08.html:304 (misconception 1): absolute cosines at least 0.9985; unrounded minimum 0.998544 >= 0.9985 (recompute_numbers_r5.py).",
 "M3c-num-L08-E1-printed-basis": "L08.html:284 (interpretation): 'computed from the unrounded M11 and trace' matches the lab code (twin lines 114-120, unrounded m11 and trace).",
 "M3c-math-L08-P1-P3-R2": "L08.html:342-360 (P1-P3) and 399-402 (problem R1 solution, cited as R2 in round 4): column means, scaling, P3 lambda1 >= M11 via Theorem 2.1(a) with u = e1. Re-derived.",
 "M3c-math-L08-props": "L08.html:61-133 read in full this round: Prop 1.1 (PSD), Prop 1.2 (trace), Def 1.3, Thm 1.4 (Z^T Z/(T-1) = Lambda), Thm 2.1 (a),(b), Cor 2.2, Prop 2.3 (scaling), Remark 2.4 (one column rescaled). All re-derived; scaling claim holds with c != 0 since c^2 > 0 preserves order.",
 "M3c-math-L08-T21-equality": "L08.html:112 (equality case, c_i = 0 for lambda_i < lambda_1), 285, 402 (R1: tie gives the whole eigenspace). Re-derived.",
 "M3c-math-L08-R3-nonzero-count": "L08.html:406-416 (R3): X tilde = F B^T, M = B G B^T, W = BQ eigenvectors, exactly three nonzero eigenvalues when rank F = 3 (G invertible). Re-derived.",
 "M3c-math-L08-E1-share-rise": "L08.html:374-393 (E1 statement and solution): (1,1) entry becomes 100 M11, trace becomes S0 + 99 M11; bound from P3. Re-derived.",
 "M3c-math-L08-why-proves": "L08.html:52 (why-it-matters): PCA first direction carries the largest squared movement (Corollary 2.2); simulated check; no real-curve claim.",
 "M3c-math-L08-misc3-causal": "L08.html:312 (misconception 3): order follows the eigenvalues (Theorem 2.1); the lab does not vary scales; no causal claim beyond the lab. Checked against twin lab-M3-L08-1.py planted scales 8, 4, 2 (line 192-194 of the page code).",
 "M3c-math-L08-misc1-claim": "L08.html:303-304 (misconception 1): Theorem 2.1 uses only M; the lab's cosines 0.9985 or more; scales 8, 4, 2 vs noise 0.5; the lab does not test other scales. Consistent with the output.",
 "M3c-prose-L08-canon-data": "L08.html:283-291 (canon-breaks: Treasury lab not run; two series). Checked against course/assets/data/market/MANIFEST.json: ust_daily columns tbill_3m and cmt_10y only (two tenors); fx series are currencies, not tenors. The claim that no embedded multi-tenor series with three or more tenors exists holds.",
 "M3c-prose-L08-canon-freedom": "L08.html:293 (canon bullet on sign and ties; cites Lesson 6): L06.html:229 states the sign freedom of singular vectors. Re-read this round.",
 "M3c-prose-L07-L08-references": "L07.html:426 (references sentence) confirmed. L08 references section is at L08.html:516-519 with the sentence at line 518; round 4 cited line 510, a stale locator (the claim itself is unchanged and true). L09 references section at L09.html:585-588.",
 "M3c-math-L08-cosine-none": "L08.html:137 (cosine and orthogonalizing paragraph): Lesson 7 Theorem 1.2 for the orthogonal projection; the cosine definition uses nonzero vectors. Re-read this round.",
 "M3c-num-L09-values": "L09.html:106-107 (C0 witness -2.4), 179-180 (Example 3.6), 332 (M3 witness), 338-342 (lab interpretation), 374-393 (E1 distances), 440 (E2), 445-447 (E3). Recomputed: C0 eigenvalues -0.8, 1.9, 1.9; ||C0-B||^2 = 0.64 = sum of squared negative eigenvalues; R entries 0.5, 0.5, -0.5; ||C0-R||_F = 0.9797959 -> 0.9798.",
 "M3c-num-L09-count": "L09.html:52, 338-342 (23 of 40 not PSD; 23 of 23 correlation check; 23 of 23 closer). Recomputed independently in recompute_numbers_r5.py: nonpsd 23, feasible 23, closer 23.",
 "M3c-num-L09-worked": "L09.html:383 (M1: eigenvalues 1.6 and 0.4), 388-390 (M2: squared norm 4.88 = 2.2^2 + 0.2^2), 395-397 (M3: roots (13 +/- sqrt 41)/2, C12 = 1/3). Re-derived by hand.",
 "M3c-math-L09-lemmas-props": "L09.html:73-161 read in full this round: Lemma 1.3 (orthogonal conjugation preserves Frobenius norm, trace cyclicity), Prop 3.2 (a),(b), Prop 3.3 (a),(b), Prop 3.4 (rescaling), Prop 3.5 (zero diagonal forces zero row). All re-derived; Prop 3.5 proof numbers: delta*b_jj < |b_ij| holds.",
 "M3c-math-L09-method2": "L09.html:185-190 (Method 1, Method 2) and 193 (hypothesis): code alternating_projections matches the stop rule (|y-x| < 1e-12 or 500 steps); W has unit diagonal by construction; no convergence claim made. Re-read this round.",
 "M3c-math-L09-examples": "L09.html:101-108 (Example 2.3: x^T C0 x = 3 - 5.4 = -2.4), 176-181 (Example 3.6), problem R2 solution (L09.html:465: diag(1,4) rescales to identity). Re-derived.",
 "M3c-prose-L09-remark22": "L09.html:98 (Remark 2.2): existence and uniqueness not asserted; Method 1 proven under positive diagonal; Method 2 not claimed. Consistent with the lab and Props 3.2, 3.4.",
 "M3c-prose-L09-misc3-W": "L09.html:368 (misconception 3): 23 non-PSD instances where W passes the check and is strictly closer than R; 'up to that tolerance' qualifier present. Consistent with output lines 339-341.",
 "M3c-prose-L09-rescale-claim": "L09.html:364 (misconception 2): congruence D^{-1/2} B D^{-1/2} preserves PSD (Prop 3.4 proof, L09.html:157-158). Re-derived.",
 "M3c-prose-L09-why-closer": "L09.html:52 (why-it-matters): clip-and-rescale proven; alternating projections not proven; 23 of 40 numbers match the lab output.",
 "M3c-prose-L09-singular-repair": "L09.html:350 (singular repair): Example 3.6 R has eigenvalue 0 with eigenvector (1,-1); Prop 3.3(a) monotonicity in epsilon: each term (epsilon - lambda_i)^2 nondecreasing and terms added as epsilon grows. Re-derived.",
 "M3c-simulated-labelling-L07-L08": "L07.html:125-135, 200, 246; L08.html:146, 151, 276, 284, 292-296, 425-433: each SIMULATED label present; no real data claimed. The page cites data only through the MANIFEST check above.",
 "M3c-simulated-labelling-L09": "L09.html:52, 193, 342, 349-350, 492: SIMULATED stated for the 40 seeded matrices; results graded C naming the lab (L09.html:492-493).",
 "M3c-twin-L08-diff": "tests/labs/M3/lab-M3-L08-1.py:114-120 is the bound code; page code equal to twin (embed_and_numbers_r5.py: embedded code == twin True).",
 "M3c-notation": "notation/notation.json conformity re-read for the symbols used on L07-L09 (M, Lambda, P, G, C, R, W, M11); changed text lines in the delta are none on L07-L09. Re-read this round; no mismatch.",
 "M3c-dag-no-outside-concepts": "check_dag M3 PASS (this round); L07 cites Theorem 2.2(b) (internal), L08 cites Lesson 4, Lesson 6 (both within M3 and in the prerequisite closure), L09 cites Lesson 5 for PSD (within M3). No concept outside the unit closure used by name or link.",
 "M3c-math-L09-cosine-none": "L08.html:137 read this round (no cosine claim in L09; the row's location is the same paragraph).",
 "M3c-process-words": "grep of L07.html, L08.html, L09.html for builder, verifier, round, unit report, REQUEST: no hits in learner text (only 'round' absent; cards in slice have no process words).",
 "M3c-scope-words": "grep of L07-L09 for every, all, only, always, any, same, drives, offsets, raises: each occurrence was read; each carries a computation or proof (e.g. L09.html:52 'in all 23' with 23 of 23 printed; L07.html:200 'every full-column-rank design' covered by Theorem 1.2).",
 "M3c-banned-phrases": "grep of L07-L09 for roughly half, about 6%, historically, typically, usually, generally, clearly, obviously, and ellipses: only quiz-stem blanks (cloze) matched the ellipsis pattern (L07.html:394,408; L08.html:445,459,505; L09.html:523,532), which the brief classifies as cloze, not omissions.",
}

carried_ids = {"M3c-card-L07-c168", "M3c-cards-L07", "M3c-cards-L08", "M3c-cards-L09", "M3c-cards-duplicates", "M3c-cards-new-L07-L09"}
card_fresh = {
 "M3c-cards-duplicates": "cards.json now has 179 cards with 179 unique ids (run this round). Duplicate-content scan of the slice objects: byte-identical objects since the round-4 pin (see the carry prefix), so the round-4 scan still holds for L07-L09.",
}

rows = []
for rid, r in old.items():
    if rid in fresh:
        ev = fresh[rid]
    elif rid in card_fresh:
        ev = card_fresh[rid]
    else:
        ev = (f"Carried from round 4 (course/modules/M/M3/L07.html, L08.html, L09.html, tests/labs/M3/lab-M3-L07-1.py, "
              f"lab-M3-L08-1.py, lab-M3-L09-1.py and the slice card objects byte-identical since the previous pin 2657ab5; "
              f"git diff 2657ab5 09b8751 is empty on those paths, cards.json hunks only at L02, L03, L06): {r['evidence']}")
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})

assert len(rows) == 74 == len({x["id"] for x in rows}), len(rows)
frag = {
 "unit": "M3",
 "slice": "M3-c",
 "round": 5,
 "verifier": "Haiku 5.5 independent verifier, slice M3-c, round 5. Did not build M3.",
 "pin": "09b8751",
 "base": "2657ab5 (round-4 pin). Delta on the slice computed with git diff 2657ab5 09b8751: no change to L07.html, L08.html, L09.html, the three lab twins, or the slice cards; the delta touches index.html, project.html, glossary.json and cards of L02, L03, L06 outside this slice (re-checked: hours and build_site).",
 "checkout": "/tmp/verifyB5-M3-c (detached at 09b8751, .venv symlinked)",
 "scratch": "/tmp/M3-v/c",
 "verified_at": "2026-10-28",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Architect ruling: lab twins are demonstrations; mutation testing applies to project graders only, so no mutants are listed (mutants []).",
  "Hours: pace not judged (architect ruling); the hub split 105 + 45 = 150 and the lesson sum 105 were re-checked.",
  "Round-4 prose row M3c-prose-L07-L08-references cited L08.html:510 for the references sentence; the sentence is at L08.html:518 in the same unchanged file. Locator corrected here; the claim is unchanged.",
  "Every L07-L09 page was read in full this round (not only the hunks), and every number was recomputed by ledgers/M3/scripts/M3-c-r5/recompute_numbers_r5.py (own code, not the lab twin).",
  "Live reference run: tools/verify_refs.py --unit M3 gave 2 of 560 entries with 0 problems; no registry key of this slice changed.",
  "Not checked: card texts of L07-L09 were not re-read line by line this round (carried by byte-identity of the card objects); the full gate (check_projects, mutate_graders, run_graders) is not run because the slice has no project grader.",
  "Not checked: primary sources for the textbook references (Axler, Strang) were not read; the pages attribute no result to a source (L07.html:426, L08.html:518), so no external attribution is asserted.",
  "Shared-file state: glossary.json and index.html changed in the delta; build_site --check and check_dag were re-run and pass.",
 ],
 "summary": {"rows": 74, "pass": 74, "fail": 0, "unverifiable": 0, "mutants": 0},
 "verdict": "PASS",
}
out = ROOT / "ledgers/M3/M3-c.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, len(rows))
