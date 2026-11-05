# Round 7 verifier (SC1-a) fragment builder. Written by the round-7 verifier from its own review of the
# 4bd8cb9..06994db1 delta; it carries round-6 PASS rows only where the cited lines are byte-identical
# (git diff -U0 4bd8cb9 06994db1 lists the changed lines: L01 67,69,102,115,136,215,353,370,434; L02 313;
# L03 382,437,443; index.html, tests/labs/SC1/*, notation/, references/, tools/ unchanged).
# Usage: python3 -I build_fragment.py <repo_root> <prev_fragment_json>
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.load(open(sys.argv[2], encoding="utf-8"))

CARRY_PREFIX = (
    "Carried from round 6 (cited lines byte-identical since the previous pin 4bd8cb9; "
    "git diff -U0 4bd8cb9 06994db1 does not touch them): "
)

# Rows re-verified from scratch this round (subject changed, or new gate evidence).
FRESH = {
    "SC1a-gate-check-pages": "Round 7 at 06994db1: tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 (ledgers/SC1/scripts/SC1-a-r7/check_pages.out).",
    "SC1a-gate-check-dag": "Round 7 at 06994db1: tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 (ledgers/SC1/scripts/SC1-a-r7/check_dag.out).",
    "SC1a-gate-run-labs": "Round 7 at 06994db1: tools/run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)', exit 0 (ledgers/SC1/scripts/SC1-a-r7/run_labs_unit.txt).",
    "SC1a-gate-page-smoke": "Round 7 at 06994db1: tools/page_smoke.py --unit SC1 --pages index.html L01.html L02.html L03.html --skip-sweep -> 'page_smoke SC1: PASS', exit 0 (ledgers/SC1/scripts/SC1-a-r7/page_smoke.out). The sweep was skipped as in round 6; the four pages have no figure controls.",
    "SC1a-gate-lint-types-tests": "Round 7 at 06994db1: ruff check and ruff format --check on tests/labs/SC1 pass (ledgers/SC1/scripts/SC1-a-r7/ruff.out); mypy --no-incremental: 'Success: no issues found in 385 source files' (mypy.out); pytest -q -k SC1: exit 0 (pytest_sc1.out).",
    "SC1a-gate-verify-refs": "Round 7 at 06994db1: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (ledgers/SC1/scripts/SC1-a-r7/verify_refs.out). No reference record changed in the delta.",
    "SC1a-lab-L01-twin": "Round 7 at 06994db1: twin tests/labs/SC1/lab-SC1-L01-1.py run as python3 -I -W error from an empty scratch dir: exit 0, empty stderr; stdout equals the L01.html expected block line for line (scripts/SC1-a-r7/expected_vs_twin.py: 'L01 expected lines: 6 twin lines: 6 EQUAL'; page code equals twin: True). Output in twin-L01.out.",
    "SC1a-lab-L02-twin": "Round 7 at 06994db1: twin run under python3 -I -W error: exit 0, empty stderr; stdout equals the L02.html expected block (12 lines EQUAL; page code equals twin: True) (scripts/SC1-a-r7/twin-L02.out).",
    "SC1a-lab-L03-twin": "Round 7 at 06994db1: twin run under python3 -I -W error: exit 0, empty stderr; stdout equals the L03.html expected block (35 lines EQUAL; page code equals twin: True) (scripts/SC1-a-r7/twin-L03.out).",
    "SC1a-lab-claims-L01": "Round 7 at 06994db1: L01.html:136 (hypothesis) now says a dyadic partition of depth n has 2**n pieces of length t/2**n. The twin's dyadic_variance_sum uses width = t / 2**n over 2**n pieces, so the claim matches the code. Printed '15 of 15' and '81 of 81' are produced by the twin (twin-L01.out). L01.html:208 interpretation checked: the three time sums, the Cov(B_{1/4},B_{5/8}) = 1/4 line (grid i=2, j=5) and the 81 ordered pairs are as described.",
    "SC1a-numbers-L03-SE-follow": "Round 7 at 06994db1, recomputed in scripts/SC1-a-r7/expected_vs_twin.py over all 16 printed rows: largest |se / (H*sqrt(2/N)/20) - 1| = 13.21% at H=2, N=1 (0.1601 vs 0.141421); this is within the stated 14 percent and matches the prose 13.2 percent at L03.html:398.",
    "SC1a-grade-L01": "Round 7 at 06994db1: T grades at L01.html:83, :101, :119 and the key-results rows at :350-353 are re-checked. The row at :353 changed (its basis text now also names the product extension); the extension is proved at L01.html:215 (product measure, U uniform and independent of B, Borel C), so T stands. Other rows unchanged.",
    "SC1a-math-L01-remark1.3": "Round 7 at 06994db1: Remark 1.3 (L01.html:101-113) re-derived. Only the title (line 102) and the Gaussian-process sentence (line 115, now with &lt; escaped) changed in text; the proof uses (D3) for independence of the increments with t_0=0, (D2) for their laws, A1(b) for normality, and Proposition 1.2 for the covariance min(t_i,t_j).",
    "SC1a-math-L01-canon-construction": "Round 7 at 06994db1: round 6 FAIL is fixed. L01.html:215 now builds U on the product space (Omega x (0,1), F (x) Bor(0,1), P (x) Leb) with B extended by B_t(omega,u)=B_t(omega) and U(omega,u)=u. Checked: every event of sigma(B) has the form A x (0,1); P((A x (0,1)) cap (Omega x C)) = P(A) Leb(C), so U is independent of B; the extended B keeps continuous paths; B~_t = B_t + 1{t=U} has B~_0 = 0 since U in (0,1); P(U in F) = 0 for finite F gives equal finite-dimensional laws; B~_U = B_U + 1 and B~_t -> B_U as t -> U, so the path is discontinuous at U on every outcome. The hypotheses (A1(a), A1(b), A1(e), A2, Assumption 2.1, Remark 2.6, H1) are named. The statement is correct.",
    "SC1a-math-L03-misc-claims": "Round 7 at 06994db1: L03.html:259-261, :270, :274-279 re-derived (E|Z| = sqrt(2/pi); absolute-sum growth sqrt(2Nt/pi); fourth-moment canon constant c). R1 (:366-368), R2 (:372-375) and R3 (:379-382, changed) re-derived: E Q = t, Var Q = N^2 * 2(t/N)^2 = 2t^2, mesh condition as stated. See the row for the R3 wording defect (SC1a-r4-thm23-counterexample-L03).",
    "SC1a-grade-L02-remark2.6": "Round 7 at 06994db1: grade T for Remark 2.6 (L02.html:302-318) is correct: the statement is proved on the page given the hypotheses it lists (H1 copies, H2 A1(a), A1(b), A1(e), A2, Assumption 2.1). The proof has one false sentence (L02.html:314), recorded in SC1a-math-L02-thm2.5-extension, which does not change the grade. Line 313 changed only by escaping the less-than sign.",
    "SC1a-exercises-L01-L03": "Round 7 at 06994db1: every worked solution re-read and hand-checked: L01 M1-M3 (Cov 1/3, Var 1/3, Var(3B_1-B_2)=5), P1-P3, E1-E3 (3/64, 16*3/64=3/4, 2*1/8=1/4), R1-R3 (R2/R3 under §4, unchanged by the delta except line 370); L02 M1-M3 (Var U_1 = 1/4, check 1/8+1/8=1/4), P1-P3, E1-E3 (216 = 18+24+35+54+85; level-1 bound 0.832555 = sqrt(4 log 2)/2), R1-R3; L03 M1-M3, P1-P3, E1-E3 (16*255/1536 = 2.65625; sqrt(2/128)=1/8, 2*(1/8)/20 = 0.0125), R1-R3 (R3 wording defect recorded separately). Numeric checks in scripts/SC1-a-r7/expected_vs_twin.py.",
    "SC1a-misconceptions-canon": "Round 7 at 06994db1: each misconception re-derived: L01 (Cov(B_{1/2},B_1)=1/2; 1/100 gives sd 1/10 = 10h; §4 process has same laws, different paths), L02 (series with 1+k/2 lower bound: each block of 2^{i-1} terms each >= 2^{-i} sums to >= 1/2; coefficient scale c^2 = 2^{-(n+2)}; t^n limit), L03 (E|Z| = sqrt(2/pi); sqrt(2Nt/pi); constant limit). L02.html:319-327 and :332-345 and L03.html:256-281 are unchanged text.",
    "SC1a-canon-breaks-ungraded": "Round 7 at 06994db1: L01.html:215-217 (changed at 215) carry no T grade of their own; claims re-derived (product-extension counterexample as above; item 2 under 'the assumptions of the first item'; item 3 with B_1 = +/-1, mean 0, variance 1, not normal). L02.html:319-327 and L03.html:259-261 unchanged and re-derived (L02 item 4: X_{1/3}=0 vs Normal(0,1/3)).",
    "SC1a-notation-macros": "Round 7 at 06994db1: all custom macros on the four pages are in notation/notation.json (macros checked by scripts/SC1-a-r7/katex_render_check.js, which loads the registered macros): 1280 math spans of index, L01, L02, L03 render with KaTeX and zero parse errors (katex_render.out). The changed L01 canon uses standard LaTeX (\\operatorname, \\mathrm, \\mathcal, \\tilde), not program macros.",
    "SC1a-notation-no-registered-collision": "Round 7 at 06994db1: grep of the four pages for the registered symbols: T appears only as the mention at L03.html:120 (the program's notation reserves T), \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}: 0 hits in L01-L03 (grep output 0 for each). The new letter F in L01.html:215 is a separate defect, recorded in SC1a-r7-notation-F-collision-L01.",
    "SC1a-process-words": "Round 7 at 06994db1: grep (case-insensitive) on index, L01-L03 and the twins for builder, verifier, fixer, ledger, round, draft, agent, reviewer, audit, TODO, TBD, lorem, clearly, obviously: no process word; the only substring hits are 'around' (scripts/SC1-a-r7/process_words.out).",
    "SC1a-banned-phrases": "Round 7 at 06994db1: tools/check_pages.py --unit SC1 PASS (its banned-string list) on the four pages.",
    "SC1a-structure-L01-L03": "Round 7 at 06994db1: check_pages PASS; L01 heading at line 69 renamed 'Covariance and finite-dimensional normality' (no stale reference to the old heading anywhere in course/, grep). Each lesson keeps grade legend, problem set, key results, quiz, references, lesson-nav.",
    "SC1a-scope-L01-prop1.2-only": "Round 7 at 06994db1: L01.html:216 ('Under the assumptions of the first item ... holds for B on every outcome and for B~ on no outcome') re-checked against the changed item 1: B continuous on every outcome; B~ discontinuous at U on every outcome; laws equal. Claim correct.",
    "SC1a-ref-L01-every-result": "Round 7 at 06994db1: L01.html:434 (changed) now says the only result taken from another lesson is Remark 2.6 of Lesson 2, used in §4 under A1(a), A1(b), A1(e), A2 and Assumption 2.1. The lesson does use Remark 2.6 (L02.html:302-306 statement) and the dependencies listed there are A1(a), A1(b), A1(e), A2 and Assumption 2.1. Correct.",
    "SC1a-reference-section-L02-L03": "Round 7 at 06994db1: References sections checked: L01.html:434 (changed, re-read: cites no registry source), L02.html:547 (unchanged), L03.html:491 (unchanged; Shreve cited by key with no passage locator, consistent with index.html:184).",
    "SC1a-r4-twin-timing-and-purity": "Round 7 at 06994db1: twins L01-L03 run under python3 -I -W error from an empty scratch dir: exit 0, stderr empty, no network, no file read (scripts/SC1-a-r7/twin-L0*.out, .err). Runtime far under the 10 s page_smoke budget (page_smoke PASS).",
    "SC1a-r5-gaussian-process-scope-L01": "Round 7 at 06994db1: L01.html:107 (Remark 1.3 scope) unchanged; L01.html:115 (Gaussian process definition) re-read: the byte change is only the escape of the less-than sign in 0&lt;t_1, and the sentence still defines the Gaussian process over vectors with 0<t_1<...<t_r; Remark 1.3 gives the law for those vectors.",
    "SC1a-r6-variance-t0-L01": "Round 6 FAIL is fixed. L01.html:67 now reads: (D1) gives Var(B_0)=0 (the case t=0) and (D2) with s=0 gives Var(B_t)=t for t>0. Both cases are checked against Definition 1.1: (D1) is B_0=0, (D2) is for 0<=s<t.",
    "SC1a-r6-quiz-mesh-hypothesis-L03": "Round 6 FAIL is fixed. L03.html:437-443 asks which assumption, added in the conclusion of Theorem 2.3, is the mesh condition; the keyed answer is Assumption 3.1, which the Theorem's conclusion adds ('Assuming also Assumption 3.1'). The distractor Assumption 3.2 is hypothesis (H2). Consistent with L03.html:101-104.",
}

# Rows whose content is now a defect.
FAILS = {
    "SC1a-math-L02-thm2.5-extension": (
        "FAIL",
        "course/modules/SC/SC1/L02.html:314 (Refinement paragraph of the proof of Remark 2.6, unchanged text, re-read this round at 06994db1). "
        "The sentence 'Each unit interval contains at most one such piece, so the pieces of one increment of W come from distinct copies' is false for more than two times. "
        "Counterexample: s_0=0.2, s_1=0.5, s_2=0.8. No integer lies in [0.2, 0.8], so the refined points are 0.2, 0.5, 0.8 and the pieces (0.2,0.5] and (0.5,0.8] both lie in [0,1] and both come from copy B^(0). "
        "The (D2) step uses only two times, where the claim does hold (for s<t each unit interval holds at most one piece), and (D3) handles same-copy pieces explicitly, so the defect is confined to this sentence. "
        "Recomputed by hand from the refinement definition.",
        "Restrict the sentence to two times: 'For s<t, each unit interval contains at most one such piece, so the pieces of W_t - W_s come from distinct copies.' Leave the (D2) and (D3) paragraphs unchanged.",
    ),
    "SC1a-r4-thm23-counterexample-L03": (
        "FAIL",
        "course/modules/SC/SC1/L03.html:382 (R3 solution, changed at 06994db1). The solution says 'Two hypotheses fail. (H1) fails ... (H2) gives no conclusion here', so it both states that (H2) fails and that it does not apply. Assumption 3.2 is a stated fact about independent variables, and (H2) is not a false hypothesis; the premise that fails is the independence in (H1). The contradiction is in the wording of the solution, not in the arithmetic (E Q = t, Var Q = 2t^2 re-checked).",
        "Replace 'Two hypotheses fail.' with 'One hypothesis fails.' and keep the (H1) sentence; (H2) then reads 'does not apply here, because Assumption 3.2 is stated for independent variables and these squares are not independent'.",
    ),
}

NEW_PASS = [
    {
        "id": "SC1a-r7-notation-F-clarity-L01",
        "check": "2.4-notation",
        "location": "course/modules/SC/SC1/L01.html:215",
        "status": "PASS",
        "evidence": "Round 7 at 06994db1: the letter F denotes a finite set of times in 'For every finite set of times F, P(U in F)=0' and the sigma-algebra \\(\\mathcal F\\) appears in the same item. F is not a registered symbol (notation/notation.json lists T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q only), and the rule that a registered symbol never takes another meaning is not broken. Non-blocking clarity suggestion: name the finite time set G, so the two objects do not share a letter in one paragraph.",
    },
    {
        "id": "SC1a-r7-gate-check-projects",
        "check": "2.9-projects-tool",
        "location": "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 7 at 06994db1: tools/check_projects.py --unit SC1 -> 'check_projects SC1: PASS', exit 0 (ledgers/SC1/scripts/SC1-a-r7/check_projects.out). Project pages are outside slice a and were not read.",
    },
    {
        "id": "SC1a-r7-katex-render",
        "check": "2.9-math-rendered",
        "location": "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 7 at 06994db1: scripts/SC1-a-r7/katex_render_check.js renders every \\( \\) and \\[ \\] span (1280 spans) with the vendored KaTeX (course/assets/vendor/katex/katex.min.js) and the registered macros from notation/notation.json, throwOnError true: 0 parse errors (ledgers/SC1/scripts/SC1-a-r7/katex_render.out).",
    },
    {
        "id": "SC1a-r7-forward-refs-L01-s4",
        "check": "2.9-define-before-use",
        "location": "course/modules/SC/SC1/L01.html:215 and :217 (canon-breaks §4)",
        "status": "PASS",
        "evidence": "Round 7 at 06994db1: §4 of L01 names Assumption A2, Assumption 2.1 and Remark 2.6 of Lesson 2 before they appear. The plan (line 184) forbids links to later concepts; the page does not link them, and each is named with its lesson ('both stated in Lesson 2'). check_dag PASS. Flagged for the architect as a forward reference, not a FAIL.",
    },
]

rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in FAILS:
        status, evidence, fix = FAILS[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": status,
                     "evidence": evidence, "fix": fix})
    elif rid in FRESH:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": FRESH[rid]})
    else:
        if r["status"] != "PASS":
            raise SystemExit(f"unassigned non-PASS previous row {rid}")
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY_PREFIX + r["evidence"]})

for r in NEW_PASS:
    rows.append(r)
    seen.add(r["id"])

for rid in FAILS:
    if rid not in {x["id"] for x in rows}:
        raise SystemExit(f"fail row {rid} not present")

all_ids = [x["id"] for x in rows]
assert len(all_ids) == len(set(all_ids)), "duplicate ids"

mutants = [
    {
        "id": "SC1a-r6-lab-mut1-L01-min-to-max",
        "description": "lab-SC1-L01-1: covariance_from_increments uses max(i, j) instead of min(i, j) (sum over the wrong number of increments)",
        "killed_by": "run of the mutated twin: 'covariance equals min(s, t) on the grid: 9 of 81 pairs' differs from the expected block '81 of 81' (ledgers/SC1/scripts/SC1-a-r7/SC1a-r6-lab-mut1-L01-min-to-max.out)",
    },
    {
        "id": "SC1a-r6-lab-mut2-L02-scale",
        "description": "lab-SC1-L02-1: level-term supremum uses 2**(-m/2) instead of 2**(-(m+1)/2)",
        "killed_by": "run of the mutated twin: 'grid supremum of each level term equals the formula ... True' becomes False and the observed sup lines differ from the expected block (ledgers/SC1/scripts/SC1-a-r7/SC1a-r6-lab-mut2-L02-scale.out)",
    },
    {
        "id": "SC1a-r6-lab-mut3-L03-closed-form",
        "description": "lab-SC1-L03-1: closed form uses (4 N^2 + 1) instead of (4 N^2 - 1) in the t-squared check",
        "killed_by": "run of the mutated twin: 'closed form matches: False' at every level, and the sum lines differ from the expected block (ledgers/SC1/scripts/SC1-a-r7/SC1a-r6-lab-mut3-L03-closed-form.out)",
    },
]

notes = (
    "Round 7 at 06994db1 (base 4bd8cb9, the round-6 pin). Full slice re-read: index.html (190 lines), L01.html (446), "
    "L02.html (561, including the lab), L03.html (505, including the lab), and the three twins. Delta 4bd8cb9..06994db1 for the slice: "
    "L01 lines 67, 69, 102, 115, 136, 215, 353, 370, 434; L02 line 313 (escape of the less-than sign plus no semantic change in the Remark 2.6 proof, but the sentence at line 314 is unchanged and false, see FAIL); "
    "L03 lines 382, 437, 443. index.html, the twins, notation/, references/ and tools/ are byte-identical to the previous pin. "
    "The round-6 FAILs are fixed: L01 canon construction (product extension), L01 t=0 variance, L03 quiz mesh wording. "
    "New FAILs: L02 line 314 (refinement claim false for more than two times; (D2) is unaffected), L03 line 382 (contradictory 'two hypotheses fail'). Non-blocking note: L01 line 215 uses the letter F for a finite time set beside the sigma-algebra \\mathcal F; F is not registered, so it is a clarity suggestion only. "
    "Plan deviation noted, not a FAIL: plan Q5 asked for the [0,1] to [0,infinity) extension to carry the sketch label; Remark 2.6 is a full proof given A2 (listed as a hypothesis) and is graded T. "
    "Lab-twin sanity mutants (3) re-run and killed. L01 line 115 mixes &lt; with a raw < before a backslash; it renders (KaTeX and the browser accept it), so it is noted, not failed. "
    "Not checked: cards.json outside the slice (four L01-L03 cards touched by the delta were read: SC1-c040, c052, c053, c054); the full pytest suite (only -k SC1); run_graders and mutate_graders (no grader in this slice); verify_refs without --offline (no reference changed); fetch_data --check, render_curriculum and build_site --check (no curriculum, site data or market input changed in this slice); the 50-seed sweep of the L02 lab was not re-run (lab unchanged, round-6 result carried)."
)

fragment = {
    "unit": "SC1",
    "slice": "SC1-a",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier SC1-a round 7 (did not build SC1; re-read the full slice at 06994db1; delta from 4bd8cb9 read hunk by hunk; gates and twins re-run)",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin, E-SC1-a.round6.json)",
    "checkout": str(root),
    "scratch": "ledgers/SC1/scripts/SC1-a-r7/ (build_fragment.py, expected_vs_twin.py, katex_render_check.js, outputs)",
    "verified_at": "2026-11-04",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": "",
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
fragment["summary"] = (
    f"SC1-a round 7 at 06994db1: verdict FAIL. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
    f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Mutants {len(mutants)}/{len(mutants)} killed. FAIL rows: "
    + "; ".join(sorted(FAILS.keys()))
    + "."
)

out = root / "ledgers/SC1/SC1-a.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, counts, "rows", len(rows))
