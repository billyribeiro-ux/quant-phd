"""Builds ledgers/M3/M3-b.json (round 5) from the round-4 rows plus the round-5 verification results."""
import json
import sys

ROOT = sys.argv[1]
r4 = json.load(open("/tmp/fanout-frags/B-M3-b.round4.json", encoding="utf-8"))
DELTA = ("delta 2657ab5..09b8751 touches only L04.html lines 51,166,321,339,389; L05.html lines 160,235-236 (lab docstring),"
         " 384,427,475; L06.html lines 235,236,302,320,327,345; cards.json M3-c102 (plus L02/L03 cards outside this slice)")
CARRY = "Carried from round 4 (cited passage byte-identical since the previous pin; " + DELTA + "): "
FRESH = "Re-verified in round 5 at 09b8751: "

override = {
    "M3b-L05-problems": ("PASS", FRESH + "P3 solution (L05 line 384) now says 'under Assumptions F1 to F4 of Lesson 4, Proposition 2.3 gives A e_i = 0', so the hypothesis is stated where it is used; the round-4 defect is fixed. Problems M1-M3, P1-P2, E1-E3, R1-R3 unchanged (lines 342-434 apart from 384 and 427); line 427 adds only 'under Assumptions F1 to F4 of Lesson 4' before Theorem 2.1, which Theorem 2.1 states. Re-derived: P3 statement Prop 2.3 hypotheses match; the rest carried."),
    "M3b-L06-problems": ("FAIL", "Row covers the whole problem set. P2 (L06 line 302) and E1 (line 318-320) now pass (P2's 'Under Assumptions F1 to F4' fixes the round-4 defect; E1 unchanged and correct). M1, M2, M3, P1, P3, E3, R2, R3 re-derived and correct. FAIL is inherited from M3b-r4-L06-R1 (R1 proof gap, L06 line 345, still unfixed in this delta) and M3b-r5-L06-E2 (E2 lower bound missing, L06 line 327)."),
    "M3b-r4-L06-R1": ("FAIL", FRESH + "R1 solution (L06 line 345) changed only its assumption label to 'Assumptions F1 to F4 of Lesson 4 (Theorem 2.3)'. The gap is unchanged: the proof concludes 'Both matrices are symmetric, so the positive eigenvalues of A^T A and A A^T agree with multiplicity', but never states that for a symmetric matrix the multiplicity of an eigenvalue equals the dimension of its eigenspace (this follows from the orthonormal eigenbasis of Theorem 2.3 of Lesson 4, which is not cited for it). The equal-dimension argument for each lambda > 0 is correct (re-derived: E maps injectively into E' via v -> Av, since ||Av||^2 = lambda ||v||^2). Fix: add one sentence: 'By Theorem 2.3 of Lesson 4, the number of diagonal entries of Lambda equal to lambda is dim E, so the multiplicity of lambda in the spectrum of A^T A equals dim E; the same holds for A A^T.'"),
    "M3b-r4-card-c102": ("PASS", FRESH + "M3-c102 back (cards.json line 704) now reads 'Assuming F1 of Lesson 4, Q Q^T = I, and ||Qx|| = ||x|| ... The proof applies F1 to Q^T and Q.' Matches the Fact 1.2 proof (L06 line 70): 'F1 applied to M = Q^T and N = Q, which satisfy MN = Q^T Q = I'. Card and lesson agree; the hypothesis F1 is stated on both."),
    "M3b-L04-L06-cards-pass": ("PASS", FRESH + "Cards in range M3-c063..c114 and c179 read in full (dump of cards.json, L04/L05/L06). Only c102 changed in this range in the delta; it now matches its lesson (row M3b-r4-card-c102). Each other card was compared to its lesson section again: hypotheses F1 to F4 are stated where the lesson states them (c087-c090, c098, c099, c102, c106-c108, c112-c114, c178), and every number on the cards appears in its lesson (c073 1/sqrt2 ~ 0.7071; c095 118 of 360; c110 2.2335/0.9250/0.3348)."),
    "M3b-r4-L05-partB-docstring": ("PASS", FRESH + "Part B docstring (tests/labs/M3/lab-M3-L05-1.py lines 233-236, learner-visible) now reads 'exact minimum on the circle is -1, at t = 135 and t = 315 degrees, and it is zero at t = 105, 165, 285 and 345 degrees'. Recomputed: 1 + 2 sin(2t) = -1 iff 2t = 270 mod 360, so t = 135, 315; = 0 iff sin(2t) = -1/2, so t = 105, 165, 285, 345. The twin output is unchanged (negative grid angles 118, zeros 4), so the docstring now agrees with the code and output. The corresponding L05 page text (Lab 1 Part B) matches."),
    "M3b-r3-quiz-numbers": ("PASS", FRESH + "Quiz explanation L05 line 475 now: 'The smallest is 1: the eigenvalues are 1 and 3, as Lesson 4, Example 2.6 computes with Lambda = diag(3, 1).' Quiz item asks the smallest eigenvalue of [[2,1],[1,2]]: eigenvalues 3 and 1, so the answer 1 is correct. Example 2.6 of Lesson 4 (line 166) is that matrix. Other quiz answers in L04 (421-504) and L06 (383-453) unchanged and re-checked: 6 pairs; 1/sqrt2; ||A||_F^2 = 30 for [[1,2],[3,4]]; 8 for 2I_2; sigma of (3 4) = 5; x^T A x = -2 at (1,-1)."),
    "M3b-r3-scope-words": ("PASS", FRESH + "Every changed sentence in the delta was scanned for scope words: L04 lines 51,166,321,339,389 (added 'Under Assumptions F1 to F4' qualifiers, each sentence keeps the proof it cites); L05 lines 160,384,427,475 (qualifier added; 'Proposition 2.4 gives one of them' and 'Theorem 2.1 does that' now hold under F1-F4); L06 lines 235-236, 302 ('every singular value' statement, proved), 320, 327 ('every column of BC is a combination' computed from the product), 345 ('for every lambda > 0' is the computed equal-dimension statement). cards c102 ('for every x in R^m', computed in Fact 1.2)."),
    "M3b-L05-proofs": ("PASS", FRESH + "L05 Remark 2.7 (line 160) changed to 'and, under Assumptions F1 to F4 of Lesson 4, Proposition 2.4 gives one of them'; re-derived: O = -I gives (-B)^T(-B) = A, and Prop 2.4 gives the factor B = Lambda^{1/2} Q^T under the stated hypotheses. Other proofs unchanged and re-derived in round 4 and round 5 (Thm 2.1 line 114-115; Thm 2.2 line 125; Prop 2.3 line 135; Prop 2.4 line 145; Ex 2.5 line 150 gives B^T B = [[2,1],[1,2]]; Ex 2.6 line 155)."),
    "M3b-L04-examples-problems": ("PASS", FRESH + "L04 Example 2.6 (line 166) re-derived: Q Lambda Q^T = [[2,1],[1,2]]; y = Q^T x = (1/sqrt2, 1/sqrt2) for x = (1,0); Corollary 2.5 gives 3/2 + 1/2 = 2 = x^T A x. Problem solution (line 321): y = (1/sqrt2)(-1,3); 3/2 + 9/2 = 6 = x^T A x for A = [[2,1],[1,2]], x = (1,-2) (direct: 2 - 4 + 8 = 6). Problem (line 339): correct, F1 used for invertibility. Problem (line 389): y = e_1 at x = q_1, maximum lambda_1, correct. Other problems unchanged: M1-M3, P1-P3, E1-E3, R1-R3 re-derived (M1 eigenvalues (7 +- sqrt5)/2; M2 Q Lambda Q^T = [[2,3],[3,2]]; M3 x^T A x = 6; E3 0.70710678)."),
    "M3b-r3-L04-whymatters-L08": ("PASS", FRESH + "L04 why-it-matters (line 51) now reads 'Lesson 8 applies it to a symmetric matrix of centred data, and under Assumptions F1 to F4 the eigenvectors it uses are perpendicular'. L08 Definition 1.3 (line 82) defines the principal directions as the columns of V in a spectral decomposition M = V Lambda V^T, and L08 applies the spectral theorem to the symmetric matrix M, so the claim matches the lesson it cites. L08 unchanged in the delta."),
    "M3b-L06-proofs": ("PASS", FRESH + "Proofs re-derived this round: Fact 1.2 (line 70) and Lemma 1.3 (line 80) use F1 and F3 as stated; Prop 2.1 (line 92-96: x^T A^T A x = ||Ax||^2, the complex quotient argument); Theorem 2.2 Steps 1-5 (lines 106-112); Theorem 2.3 (line 122: similarity of Sigma^T Sigma and A^T A; V^T = V^{-1} from Fact 1.2); Prop 2.4 (line 131-133: trace identity, cyclic trace). No gap found in these. The R1 proof is a Research problem, not part of these proofs, and is tracked in M3b-r4-L06-R1."),
    "M3b-L06-two-routes": ("PASS", FRESH + "Why-it-matters (line 52) and Theorem 2.2 proof Step 1 (line 106) unchanged in this delta and re-read; both name the spectral theorem applied to A^T A and carry 'Under Assumptions F1 to F4 of Lesson 4'."),
    "M3b-process-words": ("PASS", FRESH + "Scan of tag-stripped visible text of L04.html, L05.html, L06.html for build, builder, round, verifier, REQUESTS, unit report, roughly, historically, Higham, Eckart, Beneish, Litterman, and the new delta lines: no process word; only 'about' (L04/L05/L06 text: 'says nothing about', 'statement about exact eigenvalues', 'Any statement about B') and none is a numeric approximation."),
    "M3b-citation-scope": ("PASS", FRESH + "L04 Section 8 (line 508), L05 Section 9 (line 542), L06 Section 8 (line 457) still state that no passage is cited and no claim is attributed to a source; grep of L04-L06 and cards.json for Higham, Eckart, Beneish, Litterman, Strang, Axler returns no bibliographic claim in the delta."),
    "M3b-hours": ("PASS", FRESH + "data-hours on L01-L09 (9 files, data-hours attributes not in the delta): 11, 12, 12, 12, 11, 11, 12, 12, 12; sum 105 = index.html data-hours-lessons=\"105\" (re-computed with awk). Unit total 105 + 45 = 150 hours as stated. Hours are not judged on pace (architect ruling)."),
    "M3b-L05-lab-numbers": ("PASS", FRESH + "Part B docstring (line 233-236) now gives t = 135 and 315 for the minimum; the printed numbers do not change (twin output 'negative grid angles 118'; '118/360 = 0.3278'; one third = 120 degrees, card c095). Part A/Part C/Part D numbers re-read: Part D eigenvalues 0.0000, 1.0000, 3.0000 printed, Remark 3.2 eigenvalues 0, 1, 3 (verified by the twin output)."),
    "M3b-L05-definition-order": ("PASS", "Carried from round 4 (cited passage byte-identical since the previous pin; " + DELTA + "): Definitions 1.3 (line 66), 1.4 (line 71), Prop 1.5 (line 76) and line 51 unchanged; the delta adds the qualifier at L05 line 160 only, which uses Gram matrix (defined at 66) and Proposition 2.4 (defined at line 140) as before."),
    "M3b-L05-real-eigenvector-gap": ("PASS", "Carried from round 4 (cited passage byte-identical since the previous pin; " + DELTA + "): Theorem 2.1 proof (=>) line 114 and Theorem 2.2 proof (=>) line 125 unchanged in the delta. Re-read this round: 'real and imaginary parts of Av = lambda v ... one of x, y nonzero'; lambda real by L04 Lemma 2.1; positive direction 0 < w^T A w = lambda ||w||^2."),
    "M3b-L05-partC-nonnegative": ("PASS", "Carried from round 4 (cited passage byte-identical since the previous pin; " + DELTA + "): Lab 1 Part C code and its interpretation (L05 line 303) unchanged; the twin reruns this round and prints the counts (see M3b-embedded-output-blocks)."),
    "M3b-r4-lab-twin-output-regen": ("PASS", FRESH + "Twin outputs regenerated this round at 09b8751 into /tmp/M3-v/b5/twin-L04.out, twin-L05.out, twin-L06.out (each run under python -I -W error, exit 0). Comparison with embedded expected blocks by ledgers/M3/scripts/M3-b-r5/embed_compare_b5.py: each page has one non-code pre block and it equals the twin stdout line for line (9, 12, 8 lines)."),
    "M3b-embedded-output-blocks": ("PASS", FRESH + "ledgers/M3/scripts/M3-b-r5/embed_compare_b5.py run at 09b8751: L04 9 lines, L05 12 lines, L06 8 lines, each equal to its expected block."),
    "M3b-check-pages": ("PASS", FRESH + "tools/check_pages.py --unit M3 at 09b8751: 'check_pages M3: PASS'."),
    "M3b-check-dag": ("PASS", FRESH + "tools/check_dag.py --all at 09b8751: 14 PASS lines, exit 0. Note: the brief names prerequisites AC1, S0, S2; the curriculum entry for M3 has prereqs [M1] (curriculum/01-foundations.yaml:161); check_dag was run on the curriculum as it stands."),
    "M3b-run-labs": ("PASS", FRESH + "tools/run_labs.py --unit M3: 'run_labs M3: PASS (12/12)'."),
    "M3b-page-smoke": ("PASS", FRESH + "tools/page_smoke.py --unit M3 --pages L04 L05 L06: PASS for L04, L05, L06; lab times 0.1 s, 0.1 s, 0.0 s; runtime boot 1.1 s."),
    "M3b-twins-run": ("PASS", FRESH + "python -I -W error on tests/labs/M3/lab-M3-L04-1.py, lab-M3-L05-1.py, lab-M3-L06-1.py: exit 0 each."),
    "M3b-ruff-mypy": ("PASS", FRESH + "ruff check tests/labs/M3: 'All checks passed!'; ruff format --check: '12 files already formatted' (the folder); mypy --no-incremental on the three L04-L06 twins: 'Success: no issues found in 3 source files'."),
    "M3b-pytest-labs": ("PASS", FRESH + "pytest -q -k M3 tests/test_labs.py tests/test_run_labs.py: 12 passed."),
    "M3b-refs": ("PASS", FRESH + "tools/verify_refs.py --unit M3: 'live re-verification of M3: 2 of 560 entries, 0 problems'; offline: '560 entries, 0 problems'. Unit cites no passage locator; no HTTP status claimed."),
    "M3b-pin-and-scope": ("PASS", FRESH + "git rev-parse HEAD = 09b87514c240fd5cc904939ec6aba2ca0388ede4 (detached). Previous round pin 2657ab5. Slice delta saved to ledgers/M3/scripts/M3-b-r5/delta_L04-06.diff (275 lines) with L04/L05/L06 pages, cards.json and tests/labs/M3/lab-M3-L05-1.py."),
}

new_rows = [
    {"id": "M3b-r5-L06-E2-why-two", "check": "2.4-mathematics", "location": "course/modules/M/M3/L06.html E2 solution (line 327), prompt (line 325)",
     "status": "FAIL",
     "evidence": "E2 asks 'Explain why two is the expected count, using Theorem 2.2'. The solution proves only rank <= 2 ('every column of BC is a combination of the two columns of B'). It never proves rank >= 2 (for example that B and C have full rank for the seed or almost surely), so 'two' is not explained; the solution falls back to 'the printed count is consistent with the rank being 2' (the printed value of Lab 1). It also says the threshold 1e-10 relative 'is the convention that lets the floating-point count agree with the rank', which asserts an effect the lab does not test (Section 3 bullet 3 and interpretation line 224 say the lab tests only this threshold). Fix: state the lower bound (for example, for the seed the two columns of B and the rows of C are independent, so rank = 2) or change the prompt to 'why at most two', and reword the threshold sentence to 'is the convention this lab uses'."},
]
rows = []
for r in r4["rows"]:
    rid = r["id"]
    if rid in override:
        status, ev = override[rid]
        rows.append({**r, "status": status, "evidence": ev})
    else:
        rows.append({**r, "status": "PASS", "evidence": CARRY + r["evidence"]})
rows.extend(new_rows)
FIX = {
    "M3b-L06-problems": "Fix the two sub-rows: M3b-r4-L06-R1 and M3b-r5-L06-E2-why-two.",
    "M3b-r4-L06-R1": "Add one sentence to the R1 solution (L06 line 345): 'By Theorem 2.3 of Lesson 4, the number of diagonal entries of Lambda equal to lambda is dim E, so the multiplicity of lambda in the spectrum of A^T A equals dim E; the same holds for A A^T.'",
    "M3b-r5-L06-E2-why-two": "Prove rank >= 2 for the seed (or state that the count is read off the lab), and reword 'is the convention that lets the floating-point count agree with the rank' to 'is the convention this lab uses'; or change the prompt to 'why at most two'.",
}
for r in new_rows:
    r["fix"] = FIX[r["id"]]
rows = [dict(r, fix=FIX[r["id"]]) if r["id"] in FIX else r for r in rows]
statuses = [r["status"] for r in rows]
out = {
    "unit": "M3",
    "slice": "M3-b",
    "round": 5,
    "verifier": "independent verifier (Haiku), M3-b round 5",
    "pin": "09b87514c240fd5cc904939ec6aba2ca0388ede4",
    "base": "2657ab5 is the round-4 pin (fragment B-M3-b.round4.json); delta 2657ab5..09b8751 for the M3-b slice (saved as ledgers/M3/scripts/M3-b-r5/delta_L04-06.diff).",
    "previous_ledger": "/tmp/fanout-frags/B-M3-b.round4.json",
    "checkout": "/tmp/verifyB5-M3-b",
    "scratch": "/tmp/M3-v/b5",
    "verified_at": "2026-10-28T18:00:00+00:00",
    "verdict": "FAIL" if any(s != "PASS" for s in statuses) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice is lessons L04-L06, their lab twins, and cards M3-c063..c114 and c179. No project grader, so no mutants (architect ruling); mutate_graders and run_graders were not run.",
        "Carry rule: a round-4 PASS row is carried only where its cited passage is not in the delta hunks listed in each carried evidence string; rows whose cited passage changed were re-verified (FRESH prefix).",
        "Unchanged in the delta but read in full this round: L04 and L05 all sections, L06 Sections 1-4 and problem set, all cards in range.",
        "Brief prerequisite list (AC1, S0, S2) does not match the curriculum entry for M3 (prereqs [M1], curriculum/01-foundations.yaml:161); check_dag was run on the curriculum as it stands.",
        "Not checked: no live fetch of any external source (the unit cites axler2024linear and strang2023introduction without locators, and no HTTP status is claimed). Index, L01-L03, L07-L09 and project are other slices. Index.html line 70 (mastery bar) changed in the delta and is outside this slice.",
        "Lab 1 Part C (500 Gram matrices, 100000 forms) and L06 Lab 1 numbers were re-run through their twins only; they were not re-derived by an independent algorithm beyond the spot checks named in the rows.",
        "Hours judged only by arithmetic (architect ruling).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": statuses.count("PASS"),
        "fail": statuses.count("FAIL"),
        "unverifiable": statuses.count("UNVERIFIABLE"),
        "fail_ids": [r["id"] for r in rows if r["status"] != "PASS"],
    },
}
json.dump(out, open(f"{ROOT}/ledgers/M3/M3-b.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(out["summary"])
