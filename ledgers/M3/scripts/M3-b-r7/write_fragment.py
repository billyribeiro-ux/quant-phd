import json, sys
from pathlib import Path
R = "M3b-r6-"
def carried(n, files):
    return f"Carried from round 6 ({files} byte-identical since the previous pin 44f1eb6): "
rows = []
def add(i, check, location, status, evidence, fix=None):
    r = {"id": f"{R}{i:02d}", "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)
add(1, "prose: mid-sentence capitalisation (round-6 FAIL, re-verified)", "course/modules/M/M3/L04.html:166 (Example 2.6)", "PASS",
    "grep -n -o 'and Under Assumptions' course/modules/M/M3/L04.html returns nothing; line 166 now reads 'and under Assumptions F1 to F4, Corollary 2.5 gives' (diff 44f1eb6..7aa909e). Arithmetic re-derived: scripts/M3-b-r7/indep_numbers.out line 'L04 Ex2.6 QLQt=A True'.")
add(2, "L04 Lemma 1.3, Lemma 1.4 (T)", "course/modules/M/M3/L04.html:78-95 region (text lines 34-41)", "PASS",
    carried(2, "course/modules/M/M3/L04.html lines 78-95 of the pin") + "the diff hunks of L04.html are at why-it-matters (line 48), Example 2.6 (line 166) and R3 (line 391) only; the lemma text and proofs are unchanged and were re-read.")
add(3, "L04 Lemma 2.1, Lemma 2.2 (T)", "course/modules/M/M3/L04.html:110-127", "PASS",
    carried(3, "L04.html lines 110-127") + "re-read this round: Lemma 2.1 conjugation step and Lemma 2.2 real/imaginary-part step are complete.")
add(4, "L04 Theorem 2.3 proof, Proposition 2.4, Corollary 2.5 (T)", "course/modules/M/M3/L04.html:129-162", "PASS",
    carried(4, "L04.html lines 129-162") + "re-read this round; Theorem 2.3 statement (line ~56 text view) unchanged.")
add(5, "L04 Example 2.6 and Remark 2.7 numbers (T)", "course/modules/M/M3/L04.html:163-172", "PASS",
    "scripts/M3-b-r7/indep_numbers.out: 'L04 Ex2.6 QLQt=A True', y=(0.70710678, 0.70710678), N eigenvalues [1.0, 3.0], |ip| 0.7071067811865475; hand check of N-I and N-3I null spaces (Remark 2.7). Re-verified because line 166 changed.")
add(6, "L04 Remark 1.5 cross-reference, Remark 1.6 characteristic polynomial", "course/modules/M/M3/L04.html:43-45; course/modules/M/M3/L03.html:96", "PASS",
    carried(6, "L04.html lines 43-45 and L03.html") + "L03.html:96 'Example 1.6 (a symmetric 2 x 2 matrix)' re-grepped this round; eigenvalues (7 +/- sqrt5)/2 for [[4,1],[1,3]] confirmed by indep_numbers.out.")
add(7, "L04 problem set M1-M3, P1-P3, E1-E3, R1-R3 (numbers and proofs)", "course/modules/M/M3/L04.html:168-266 (text view 166-206)", "PASS",
    "Re-derived this round: M1 <v,w>=0 and eigenvalues (7+/-sqrt5)/2 = 4.618, 2.382 (indep_numbers.out 'L04 M1'); M2 Q Lambda Q^T = [[2,3],[3,2]] (indep_numbers.out 'L04 M2'); M3 x^TAx = 6 both ways; P1, P2, P3 proofs complete; E3 = 1/sqrt2 = 0.70710678; R1 z=(1,-i), Rz=iz, z*Rz=2i (indep_numbers.out 'L04 R1'); R2 proof; R3 hypotheses now cite F1 of Lesson 4 and Lemma 1.4 (diff hunk line 391), proof correct.")
add(8, "L04 retrieval quiz answers and explanations", "course/modules/M/M3/L04.html:425-503", "PASS",
    carried(8, "L04.html lines 425-503") + "quiz hunk not in diff; re-read the quiz text this round (sections 7, text view 230-282).")
add(9, "L04 Lab 1 twin: page code equals twin; twin under python -I -W error; output equals expected block", "course/modules/M/M3/L04.html:177-264; tests/labs/M3/lab-M3-L04-1.py", "PASS",
    "scripts/M3-b-r7/twin_vs_page.out: 'L04 code==twin: True exit: 0 stderr: '' out==expected: True 9 9'. page_smoke: scripts/M3-b-r7/page_smoke_L04-06.out 'page_smoke modules/M/M3/L04.html: PASS'.")
add(10, "L04 Lab 1 prose: docstring, hypothesis, interpretation, key-results claims", "course/modules/M/M3/L04.html:176-189, 229, 415", "PASS",
    "Re-read this round. 200 matrices, 1200 pairs = 200 x C(4,2) (code line 118-121), TOL 1e-10, GAP 1e-6 (code line 96). Printed lines 143-150 match the prose 'every' claims. Key-results row 229 'more than 1e-6 apart' matches GAP.")
add(11, "L04 'Where the canon breaks' and misconceptions", "course/modules/M/M3/L04.html:153-165", "PASS",
    "Re-read: I_2 example (1,0) and (1,1)/sqrt2 not orthogonal, (1,0) and (0,1) orthogonal; Misconception 1 (N, rotation), 2 (4,1;1,3 via Q Lambda Q^T), 3 (Proposition 2.4 applies to different eigenvalues only) correct.")
add(12, "L04 DAG: concept links and dependency closure", "course/modules/M/M3/L04.html:13-14, 21; tools/check_dag.py --unit M3", "PASS",
    "Command: .venv/bin/python tools/check_dag.py --unit M3 -> 'check_dag M3: PASS'. Why-it-matters now names the spectral theorem (Theorem 2.3, stated below); forward reference, defined in the same lesson.")
add(13, "L04 notation against notation/notation.json", "course/modules/M/M3/L04.html (all math)", "PASS",
    "notation/notation.json symbols: T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. None used in L04-L06 with another meaning. Macros used (\\R, \\diag, \\E) match the registry. Local symbols (Q, Lambda, N, R, S, W, mu, tau in L05) defined in text.")
add(14, "L05 Theorem 2.1 and Theorem 2.2 (eigenvalue tests), both directions", "course/modules/M/M3/L05.html:44-52 (text view 44-52)", "PASS",
    "Re-read every line. Theorem 2.1 (<=): w real nonzero eigenvector, 0 <= w^TAw = lambda||w||^2. (=>) via Corollary 2.5 of Lesson 4. Theorem 2.2 (<): 'Then 0 < w^TAw = lambda||w||^2, so lambda > 0' (raw HTML line 125). Assumption statement is correct: F1-F4 enter only via Lesson 4 Theorem 2.3 in the converse.")
add(15, "L05 Propositions 1.5, 1.6, 2.3, 2.4 and Remark 2.7 (T)", "course/modules/M/M3/L05.html:31-66", "PASS",
    "Re-read. Prop 1.5 symmetric and x^TB^TBx=||Bx||^2; Prop 1.6 e_i gives A_ii >= 0 and sums/nonnegative multiples; Prop 2.3 lambda_j y_j^2 = 0 => Ax=0; Prop 2.4 B=Lambda^{1/2}Q^T gives B^TB=A (indep_numbers.out 'L05 Ex2.5 B^TB' [[2,1],[1,2]]); Remark 2.7 (OB)^T(OB)=B^TB.")
add(16, "L05 Examples 1.7, 2.5, 2.6, Remark 1.8, Remark 3.2 numbers (T)", "course/modules/M/M3/L05.html:39-42, 62-64, 70-71", "PASS",
    "indep_numbers.out: 'L05 Ex2.5 B^TB [[2,1],[1,2]]'; 'L05 R3.2 eig [~0, 1, 3]'. Hand: Ex1.7 x^TAx = 1-4+1 = -2; Remark 1.8 x^TMx = x1^2+x2^2, char poly lambda^2-2lambda+2 zeros 1+/-i; Ex2.6 eigenvalues 3 and -1, (1,-1) eigenvector for -1.")
add(17, "L05 Lab 1 Part B counts (118, 4, -1) and their derivation in E2 and prose", "course/modules/M/M3/L05.html:113-127, 225-227; text 'grid angles' lines", "PASS",
    "scripts/M3-b-r7/indep_numbers.out 'L05 B: neg 118 zero 4 min -1.0 check 1+2sin2t True'; 'L05 E2 interior 106..164 + 286..344: 118 0.3278'. Lab output lines 168-170 match. Form 1+2 sin 2t verified against cos^2+4cos sin+sin^2.")
add(18, "L05 Lab 1 claim that the singular matrix's eigenvalue is printed as 0.0000 and its sign is never shown", "course/modules/M/M3/L05.html:81-82, 173, 190; lab code line 151-153", "PASS",
    "Code prints 0.0 when abs(values[0]) <= TOL (Part D, lab code). Output line 173 'eigenvalues sorted: 0.0000 1.0000 3.0000'. Consistent with the prose.")
add(19, "L05 Lab 1 twin: page code equals twin; twin under -I -W error; output equals expected block", "course/modules/M/M3/L05.html:74-175; tests/labs/M3/lab-M3-L05-1.py", "PASS",
    "scripts/M3-b-r7/twin_vs_page.out: 'L05 code==twin: True exit: 0 stderr: '' out==expected: True 12 12'. page_smoke L05 PASS.")
add(20, "L05 Lab 1 prose: docstring, hypothesis and interpretation", "course/modules/M/M3/L05.html:72-83, 177", "PASS",
    "Docstring 'Part A and Part B use fixed matrices ... Part C uses seeded samples' matches code (no randomness in A, B; rng seed 2604 in C). 'Standard library apart from numpy' matches imports (math, numpy). Printed 500 of 500 and 100000 of 100000 match output lines 171-172.")
add(21, "L05 canon-breaks, misconceptions, and the Remark 1.8 section-4 cross-reference", "course/modules/M/M3/L05.html:178-190", "PASS",
    "Re-read. Remark 1.8 is discussed in §4 (line 180) as the non-symmetric case. Misconception 1 (Example 1.7 with positive entries) and 2 (G of Remark 3.2 has eigenvalue 0 at (1,1,-1)) are correct; Misconception 3 matches Part D.")
add(22, "L05 problem set and retrieval quiz numbers", "course/modules/M/M3/L05.html:340-390 (problem set), 455-535 (quiz)", "PASS",
    "Re-derived: M1 eigenvalues 3 and 1; M2 eigenvalues 0 and 5 and x=(2,-1) form 0 (4-8+4); M3 eigenvalues 2 and 4, x^TAx at (1,1) = 4; R2 (1,-1) gives -2. Quiz data-correct options (lines 467, 480, 494, 504, 517, 531) match explanations; quiz numeric answers 1, 3 correct.")
add(23, "L05 cross-references to L01 (e_i) and L03 (Problem M2)", "course/modules/M/M3/L05.html:38, 186, 201", "PASS",
    "L01.html Example 3.9 defines e_i, the standard basis (grep line 183). L03.html line 298 'M2 · Eigenvalues of a singular matrix' with A=[[1,2],[2,4]] (grep line 306), eigenvalues 0 and 5 match L05 M2 and the P-matrix in L03 line 308.")
add(24, "L05 key-results table and Lab 1 grade labels", "course/modules/M/M3/L05.html:246-254; L05.html:177 (grade C span)", "PASS",
    "Key-results rows match the proved results and lab counts. The inline grade label before 'The angle count 118' is a span data-grade=\"C\" (raw HTML line 303), consistent with the C convention.")
add(25, "L06 Fact 1.2, Lemma 1.3 (extension to a basis), Proposition 2.1 (T)", "course/modules/M/M3/L06.html:23-39", "PASS",
    carried(25, "L06.html lines 23-39") + "observation (non-blocking): the Lemma 1.3 proof and Step 5 of Theorem 2.2 use 'orthonormal vectors are independent' without citing Lesson 4 Lemma 1.3; the fact is proved in L04 and is standard.")
add(26, "L06 Theorem 2.2 (SVD) proof, Steps 1 to 5, including the non-square case; statement sentence on left and right singular vectors", "course/modules/M/M3/L06.html:40-51", "PASS",
    "Re-read. Statement now defines left singular vectors (columns of U) and right singular vectors (columns of V) in the same sentence as the term (raw line 101). Step 2 orthonormality chain, Step 4 AV=UΣ for j>r via ||Av_j||^2=lambda_j=0, Step 5 VV^T=I by Fact 1.2 and rank = r verified.")
add(27, "L06 Theorem 2.3 (singular values determined by A) and Proposition 2.4 (Frobenius identity)", "course/modules/M/M3/L06.html:52-59", "PASS",
    carried(27, "L06.html lines 52-59") + "re-read: similarity argument and trace cyclicity argument complete; Frobenius identity matches indep_numbers.out ('L06 Frob 30.0' for [[1,2],[3,4]]).")
add(28, "L06 Remark 2.5 and misconceptions 1 to 3", "course/modules/M/M3/L06.html:137-150", "PASS",
    carried(28, "L06.html lines 137-150 (no hunk in the diff)") + "re-read: sign pair and I_2 example correct ([[0,1],[1,0]] orthogonal, U Sigma V^T = I); misconception 1 A=[[0,1],[0,0]] gives A^TA=diag(0,1) (verified).")
add(29, "L06 Lab 1 twin: page code equals twin; twin under -I -W error; output equals expected block", "course/modules/M/M3/L06.html:60-135; tests/labs/M3/lab-M3-L06-1.py", "PASS",
    "scripts/M3-b-r7/twin_vs_page.out: 'L06 code==twin: True exit: 0 stderr: '' out==expected: True 8 8'. page_smoke L06 PASS.")
add(30, "L06 Lab 1 prose: hypothesis, docstring, interpretation, and the E2 planted-rank explanation", "course/modules/M/M3/L06.html:61, 136, 181-187", "PASS",
    "Docstring: five seeds x two shapes = ten matrices (code lines 96-100). Seed-0 4x3 singular values 2.2335 0.9250 0.3348 match indep_numbers.out 'L06 seed0 sv [2.2335 0.925 0.3348]'. E2 bound: columns of BC lie in span of columns of B, rank <= 2 (proved). Prose 'the printed count is an observation' is accurate.")
add(31, "L06 problem set (M1-M3, P1-P3, E1-E3, R1-R3) and quiz numeric answers", "course/modules/M/M3/L06.html:154-257", "PASS",
    "Re-derived: M1 diag(3,4) gives sigma 4,3 and U=V swap; M2 eigenvalues 2,0 and sigma sqrt2 (indep_numbers.out 'L06 M2 sv [1.41421356 0.]'); M3 Sigma 3x2 with I_2; E3 A^TA trace 25, det 0, sigma 5 and Frobenius 25; P2 and P3 corrected hypotheses (Assuming F1 to F4 / F1); R1 proof (injective maps between eigenspaces; equal multiplicities) complete; R2 (Assuming F4) rank-nullity dimension argument correct; R3 (Assuming F1) correct.")
add(32, "L06 why-it-matters, canon-breaks and Lesson 8 cross-references", "course/modules/M/M3/L06.html:21, 141-143", "PASS",
    "Lesson 8 section 1 is 'Centred data and the matrix of cross-products' (grep L08.html line 54); L08.html lines 67 and 127 use the scaled Gram matrix with (T-1), consistent with the claim at L06 line 143. Non-square bullet: rank <= m, so at least n-m zero eigenvalues, Theorem 2.3 n-k zeros (raw line 236). Verified.")
add(33, "L06 terms defined before use (column space, Frobenius norm, trace, similar matrices, singular values)", "course/modules/M/M3/L06.html:35", "FAIL",
    "L06.html line 35 says 'The column space of A is the span of its columns (Lesson 1).' Lesson 1 does not state this: grep -i 'column space' over course/modules/M/M3/L01.html, L02.html and L03.html returns no hit; L01 Definition 3.3 (raw line 127) defines rank as the number of pivots and Example 3.9 defines only e_i. The definition is attributed to a lesson that does not contain it, and the term is used before it is defined on this page (Theorem 2.2 statement uses 'dimension of its column space').",
    "Replace '(Lesson 1)' in course/modules/M/M3/L06.html line 35 with a self-contained definition: 'The column space of A is the set of vectors Ax, which is the span of the columns of A.' (or define it before Theorem 2.2). Do not cite Lesson 1 for it unless Lesson 1 states it.")
add(34, "L06 lab-linked key results and quiz (grade C and T labels; quiz explanations)", "course/modules/M/M3/L06.html:206-213, 216-257", "PASS",
    "Key-results row 213 is grade C (lab output, finite check). Quiz answers: (1) symmetric and nonnegative eigenvalues, (2) sigma 5, (3) 1,1,1, (4) 30, (5) 0,1 from A^TA=diag(0,1), (6) k=2, (7) orthogonal-by-definition option 'U=V=0' rejected, (8) 8 for 2I_2 all correct.")
add(35, "Cards for L04 (16), L05 (26), L06 (15): agreement with lesson text; numbers present; no duplicate cards", "course/modules/M/M3/cards.json", "PASS",
    "scripts/M3-b-r7/cards_check.out: total 180, dup ids [], per lesson L04 16, L05 26, L06 15. Changed cards M3-c084 (T, diagonal entries, Proposition 1.6) and M3-c180 (T, sums and nonnegative multiples, Proposition 1.6) agree with L05 Proposition 1.6 text; no number missing from lesson text. No L04 or L06 card changed.")
add(36, "Hours arithmetic: lesson study hours against the hub split", "course/modules/M/M3/L01-L09.html 'study hours'; course/modules/M/M3/index.html:29", "PASS",
    "Per-lesson study hours: L01 12, L02 11, L03 12, L04 12, L05 12, L06 11, L07 11, L08 12, L09 12; sum 105 = hub data-hours-lessons=105. Project 45 = data-hours-project=45; tier total 150 = 'Tier F · 150 hours'. Consistent.")
add(37, "Gate commands for the slice", "tools/check_pages.py, check_dag.py, check_projects.py, run_labs.py, page_smoke.py, render_curriculum.py, verify_refs.py", "PASS",
    "Output: 'check_pages M3: PASS'; 'check_dag M3: PASS'; 'check_projects M3: PASS'; 'run_labs M3: PASS (1/1)' for L04, L05, L06; render_curriculum + git diff --exit-code CURRICULUM.md curriculum/curriculum.json exit 0; 'offline integrity: 560 entries, 0 problems'; page_smoke --pages L04 L05 L06 'page_smoke M3: PASS' (scripts/M3-b-r7/page_smoke_L04-06.out). NOT run: ruff, mypy, pytest (no Python file in the slice changed; tests/labs/M3 changes in this delta are L01, L02 and project-3 only, outside slice b).")
add(38, "Process words and learner-facing text", "course/modules/M/M3/L04.html, L05.html, L06.html, cards.json", "PASS",
    "grep -i 'round|builder|verifier|architect|open item' over L04-L06 returns only 'rounded' (lab-output wording). Changed text (Assuming F1..F4 prefixes, left/right singular vector sentence) contains no process words.")
add(39, "Delta hunks since previous pin (44f1eb6..7aa909e) for the slice", "git diff 44f1eb6 7aa909e -- course/modules/M/M3/L04.html L05.html L06.html cards.json", "PASS",
    "Every hunk read. L04: why-it-matters (l.21 text), Example 2.6 'under' (l.166), R3 'Assuming F1 of Lesson 4' with Lemma 1.4 citation (l.391-394). L05: 'Assuming F1 to F4 of Lesson 4' prefixes on M1, M2, M3, P3, R1, R2 (l.340-420). L06: Theorem 2.2 left/right singular vector sentence (l.101); P2, P3, R1, R2, R3 'Assuming' prefixes (l.297-350). cards: c084, c161 (L09, outside slice), c154-157 (L09), c120-121 (L07), c038-039 (L02) outside slice; c084 and c180 in slice and verified. Lab twins for L04-L06 unchanged in the delta.")
add(40, "Mutants and alternative implementations (lesson labs are demonstrations; mutation testing applies to project graders)", "tests/labs/M3/lab-M3-L04-1.py, L05-1, L06-1", "PASS",
    "Not applicable to lesson slice per the rulings: no grader in slice b. Lab twins unchanged in the delta; re-run (twin_vs_page.out) exits 0 with expected output. No new mutants required.")
out = {
 "unit": "M3", "slice": "b", "round": 7,
 "verifier": "independent Haiku verifier, slice b (did not build M3)",
 "pin": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4",
 "base": "44f1eb6 (round-6 pin; delta 44f1eb6..7aa909e read in full for the slice)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-M3-b",
 "scratch": "/tmp/m3b7 (L04.txt, L05.txt, L06.txt text views)",
 "verified_at": "2026-10-28",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Round-6 row M3b-r6-01 (L04 line 166 capital U) is fixed and re-verified PASS.",
  "New defect found this round: M3b-r6-33 (L06 line 35 cites Lesson 1 for the column-space definition, which Lesson 1 does not contain).",
  "Scripts: ledgers/M3/scripts/M3-b-r7/ (twin_vs_page.py/.out, indep_numbers.py/.out, cards_check.py/.out, page_smoke_L04-06.out, write_fragment.py).",
  "Not checked: rendered KaTeX layout and dark-mode appearance (page_smoke ran headless, no screenshot diff); ruff, mypy and pytest were not run because no Python file of the slice changed; L01, L02, L03, L07, L08, L09 read only at cited lines; the registry key axler2024linear and strang2023introduction were not read, and the lesson cites no passage from them."
 ],
 "summary": "Slice b (L04-L06 and twins) round 7: FAIL on one row, M3b-r6-33 (L06 line 35 column-space definition attributed to Lesson 1, which does not state it). 39 PASS, 1 FAIL, 0 UNVERIFIABLE. Round-6 FAIL M3b-r6-01 is fixed. All gate commands in scope pass; lab twins run and match expected output."
}
p = Path("ledgers/M3/M3-b.json")
p.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("rows", len(rows), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
