"""Builds ledgers/M7/M7-a.json (round 7). Carries round-6 rows only where the cited subject is byte-identical."""
import json
import sys

CHK = "/Users/billyribeiro/.fanout/wt/verifyB7-M7-a"
R6 = "/Users/billyribeiro/.fanout/frags/B-M7-a.round6.json"
prev = json.load(open(R6, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}

FRESH_LAB = "run_labs --unit M7 --page L0x: PASS (1/1) this round (ledgers/M7/scripts/M7-a-r7/gates_1.txt); lab section identical to pin 44f1eb6 except noted"
CARRY = "Carried from round 6 (L01.html/L02.html/L03.html/index.html lines cited byte-identical since the previous pin 44f1eb6; no hunk touches them): "


def carry(rid, files, note=""):
    r = dict(prev_rows[rid])
    r["evidence"] = CARRY + files + ". " + r["evidence"] + ((" " + note) if note else "")
    r["status"] = "PASS"
    return r


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r


rows = []
# ---- hub
rows.append(row("M7a-hub-structure", "2.9 structure: hub sections and minimums", "course/modules/M/M7/index.html (whole file)", "PASS",
    "check_pages --unit M7: PASS (ledgers/M7/scripts/M7-a-r7/check_pages_unit.txt). Note: check_pages --page index is not a valid hub check (it treats index as a lesson and reports missing sections); the hub is checked by --unit only."))
rows.append(row("M7a-hub-hours", "2.9 hours split arithmetic", "index.html data-hours-lessons, data-hours-project, card-kicker L01-L08; L01-L08 data-hours", "PASS",
    "grep: data-hours-lessons=77, data-hours-project=33, 77+33=110 matching the page's '110 hours'. Card kickers L01..L08 = 9,9,10,10,10,10,9,10, sum 77; lesson data-hours L01 9, L02 9, L03 10, L04 10, L05 10, L06 10, L07 9, L08 10 (grep this round)."))
rows.append(carry("M7a-hub-placement-numbers", "index.html placement quiz lines 75-135 (no hunk)"))
rows.append(carry("M7a-hub-placement-explanations", "index.html lines 88-124 (no hunk)"))
rows.append(carry("M7a-hub-cross-refs", "index.html lines 156-161, 176 and project.html lines 44-55"))
rows.append(row("M7a-hub-dag-concepts", "2.9 / DAG: concept links and definitions", "index.html; L01.html; L02.html; L03.html; check_dag --unit M7", "PASS",
    "check_dag --unit M7: PASS (ledgers/M7/scripts/M7-a-r7/gates_1.txt). check_pages --unit M7 PASS (link and anchor checks). Line 65 concept links to positive-semidefinite-matrix unchanged in target."))
rows.append(carry("M7a-hub-covariance-disclaimer", "index.html line 167 (no hunk)"))
rows.append(carry("M7a-hub-attributions-registry", "index.html lines 170-177 (no hunk) and L01.html 548-551, L02.html 531-535 (no hunk)",
    "verify_refs --unit M7 (live, this round): 2 of 560 entries, 0 problems (ledgers/M7/scripts/M7-a-r7/verify_refs_unit_M7.txt). L03.html reference text changed (line 540, 'This lesson cites no source'): still cites nothing, so no attribution claim depends on it. Registry flag retained: stokey1989recursive has three authors."))
rows.append(row("M7a-hub-data-simulated", "2.8 data and SIMULATED labels", "index.html lines 37, 167; L01.html 165; L02.html 157; L03.html 140, 159", "PASS",
    "grep this round: SIMULATED at L01.html 165, L02.html 157, L03.html 159; L03 line 140 states the Sigma and mu are given inputs chosen by hand. grep -c for data-files|svg|figure: 0 in L01-L03, 1 in index.html (line 167 'no figure shows a real asset'). Line numbers moved from round 6 (L03 lines 143, 161-162 are now 140, 159)."))
rows.append(row("M7a-hub-page-smoke", "2.9 page_smoke: console, math, external requests, 360 px", "index.html, L01.html, L02.html, L03.html", "PASS",
    "page_smoke --unit M7 --pages index L01 L02 L03: PASS for all four pages, exit 0 (ledgers/M7/scripts/M7-a-r7/page_smoke.txt). Pyodide boot 1.1 to 1.2 s; labs 0.0 to 0.6 s."))
rows.append(row("M7a-hub-banned-phrases", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "index.html; L01.html; L02.html; L03.html", "PASS",
    "check_pages --unit M7 PASS includes the banned-string check on visible prose (ledgers/M7/scripts/M7-a-r7/check_pages_unit.txt). Grep this round for 'open item', 'planning', 'tracking', 'architect' in all four pages and the three twins: no matches."))
rows.append(row("M7a-hub-prereq-prose", "2.9 prose accuracy", "index.html line 65", "PASS",
    "Changed sentence: 'Lesson 2 uses a positive definite matrix Sigma, a stronger condition than positive semidefiniteness, defined there.' L02.html line 114 defines positive definite ('A symmetric n x n matrix Sigma is positive definite when x'Sigma x > 0 for every x != 0') and says it is stronger than the non-negativity of Lesson 1, Prop 3.2. Sigma is positive definite in L02 Prop 3.2 (line 122). Accurate."))
rows.append(carry("M7a-hub-lede-claims", "index.html line 141 (no hunk)"))
rows.append(row("M7a-hub-lede-kkt-scope", "2.9 prose accuracy", "index.html line 30 (lede), line 49", "PASS",
    "New lede phrase 'the Karush-Kuhn-Tucker (KKT) conditions for equality and inequality constraints': equality conditions are Lesson 2 (Lagrange, L02.html Def 2.1 and Thm 2.2) and inequality conditions Lesson 3 (L03.html Thm 2.1, conditions K1-K4). Accurate."))
rows.append(row("M7a-hub-l04-claims", "2.9 claims about lessons", "index.html line 52 and line 146 (card L04)", "PASS",
    "Changed: 'verify weak duality and the zero duality gap at a KKT point (Lesson 4)' and card 'the zero duality gap at a KKT point, with the grid bound on the gap'. L04.html Prop 1.4 (a grid bounds the duality gap, line 87) and Prop 2.1 (a KKT point gives zero gap, line 106) match both sentences. Weak duality is in Section 1 of L04."))
# ---- L01
rows.append(row("M7a-L01-why-it-matters", "2.9 prose accuracy", "L01.html line 51", "PASS",
    "Changed: 'proves the facts it uses apart from the spectral theorem (Assumption 1 below)'. Assumption 1 (spectral theorem, L01.html line 129) is the only result assumed; Lemma 3.1, Props 1.3, 2.3 and 3.2 (i)-(ii) are proved on the page (their proofs at lines 96-100, 108-121, 140-147). Prop 3.2 (iii) is conditional on Assumption 1 and says so (line 135). The page's uses of the Hessian and gradient are M2 definitions, not facts assumed."))
rows.append(carry("M7a-L01-structure", "L01.html (check_pages --unit M7 PASS this round; ledgers/M7/scripts/M7-a-r7/check_pages_unit.txt)"))
rows.append(row("M7a-L01-lab-run", "2.5 lab: run and twin identity", "L01.html lab section lines 157-310; tests/labs/M7/lab-M7-L01-1.py", "PASS",
    "run_labs --unit M7 --page L01: PASS (1/1) this round (ledgers/M7/scripts/M7-a-r7/gates_1.txt). Twin run: python -I -W error exit 0, stderr 0 bytes (ledgers/M7/scripts/M7-a-r7/L01.stderr). Twin file identical to pin 44f1eb6. Page lab code equality checked by run_labs."))
rows.append(row("M7a-L01-lab-numbers", "2.2 numbers printed by Lab 1", "L01.html lines 295-308 (expected block); tests/labs/M7/lab-M7-L01-1.py", "PASS",
    "Own script ledgers/M7/scripts/M7-a-r7/l01_hypothesis.py (exact Fraction, 625 ordered pairs x 5 weights = 3125 cases): Q1 chord failures 0 of 3125; Q2 chord failures 552 of 3125; ordered pairs with (x-y)'Q2(x-y)<0: 184; 3 x 184 = 552; gap identity 3125 of 3125 for Q1 and Q2 (ledgers/M7/scripts/M7-a-r7/l01_hypothesis.out). Twin output: Q2 chord inequality holds in 2573 of 3125 cases = 3125-552, matching."))
rows.append(row("M7a-L01-lab-prose", "2.5 hypothesis, interpretation and comments", "L01.html lines 159, 309, 319, 332, 336", "PASS",
    "Changed hypothesis (line 159): 'Q2 has eigenvalues 3 and -1, so the chord inequality should fail for Q2 in some cases'. Own run: 552 failing Q2 cases of 3125 (l01_hypothesis.out), so 'fail in some cases' is true. The 'three times the number of negative ordered pairs' prediction matches (552 = 3 x 184). 'Both identity lines read 3125 of 3125' matches. Other lines unchanged since round 6 and re-checked against the twin output."))
rows.append(carry("M7a-L01-lemma-3-1", "L01.html lines 108-121 (no hunk)"))
rows.append(row("M7a-L01-props", "2.4 Propositions 1.3, 2.3, 3.2 and proofs", "L01.html lines 66-148", "PASS",
    "Changed Prop 2.3 hypothesis sentence (line 95): 'The hypotheses are that S is convex, f is convex on S, and c is a real number.' Re-read the statement and proof (lines 92-100): the proof uses only S convex (z in S), Definition 2.1 for f, and c real. The 'exactly' was removed and the statement is unchanged in substance. Other lines carried from round 6 (no hunk)."))
rows.append(carry("M7a-L01-examples", "L01.html lines 61-63, 88-89, 124-125, 153-154 (no hunk)"))
rows.append(carry("M7a-L01-problems", "L01.html lines 345-444 (no hunk)"))
rows.append(carry("M7a-L01-key-results-grades", "L01.html lines 67, 93, 109, 134, 452-456 (no hunk)"))
rows.append(carry("M7a-L01-quiz", "L01.html lines 462-546 (no hunk)"))
rows.append(carry("M7a-L01-canon-misconceptions", "L01.html lines 313-339 (no hunk)"))
rows.append(carry("M7a-L01-notation", "L01.html (symbols unchanged: the edits add prose only, no new symbol)"))
# ---- L02
rows.append(carry("M7a-L02-structure", "L02.html section order (check_pages --unit M7 PASS this round covers L02)", "Edits at lines 40, 49, 58, 77 change words only; order and counts unchanged."))
rows.append(row("M7a-L02-lab-run", "2.5 lab: run and twin identity", "L02.html lab section 148-293; tests/labs/M7/lab-M7-L02-1.py", "PASS",
    "run_labs --unit M7 --page L02: PASS (1/1) this round. Changed: twin line 9-10 and page code line 162 'forms Sigma = A' A + I' (was 'builds'); run_labs confirms page code equals twin. Twin exit 0 under python -I -W error, stderr 0 bytes (ledgers/M7/scripts/M7-a-r7/L02.stderr)."))
rows.append(carry("M7a-L02-lab-numbers", "L02.html lines 279-291 (expected block; no hunk)"))
rows.append(carry("M7a-L02-lab-prose", "L02.html lines 150, 292, 311 (no hunk)"))
rows.append(row("M7a-L02-theorem-2-2", "2.4 Theorem 2.2 and proof (necessity)", "L02.html lines 68-85 (Theorem 2.2 and proof); Remark 2.3 at 86-88", "PASS",
    "Theorem 2.2 and proof (lines 68-85) unchanged: re-derived r = p - c g, r.g = 0, d = -r, p.d = -|r|^2 < 0, curve gamma(t) with gamma'(0)=d; contradiction with minimality. Remark 2.3 wording changed ('constructs' for 'builds'); the remark claim matches the proof."))
rows.append(carry("M7a-L02-assumption-1", "L02.html lines 67-70 (no hunk)"))
rows.append(carry("M7a-L02-examples", "L02.html lines 92-110 (no hunk)"))
rows.append(carry("M7a-L02-prop-3-2", "L02.html lines 121-136 (no hunk)"))
rows.append(row("M7a-L02-problems-quiz", "2.4 problem solutions and quiz numerics", "L02.html lines 330-427, 445-529; changed explanation line 521", "PASS",
    "Changed explanation (line 521, Q9): 'Symmetry does not: diag(1, 0) is symmetric and singular. A positive trace does not either: diag(1, 0) has trace 1 and is singular.' Checked: diag(1,0) is symmetric (yes), singular (det 0), trace 1 > 0, and not positive definite (x=(0,1) gives 0). The old counterexamples are replaced; the new ones are correct. Other items carried from round 6 (no hunk in the carried ranges)."))
rows.append(carry("M7a-L02-misconceptions-canon", "L02.html lines 295-322 (no hunk)"))
rows.append(row("M7a-L02-wording-theorem-applies", "2.9 prose accuracy", "L02.html line 118", "PASS",
    "Round 6 flagged 'Theorem 2.2 applies to it under Assumption 1' as loose. Now: 'so it meets the regularity hypothesis of Theorem 2.2. Under Assumption 1, Theorem 2.2 applies to every local minimizer of f on the budget set.' Checked against Theorem 2.2 (line 86-ish hypotheses): U open, f and h C^1 on R^n, h(x*)=0 for a feasible minimizer, grad h = 1 != 0. All hold. Fixed."))
rows.append(carry("M7a-L02-notation", "L02.html (no new symbol; \\operatorname{diag} used in an explanation already in use)"))
# ---- L03
rows.append(row("M7a-L03-why-and-limits", "2.9 prose accuracy", "L03.html line 98 (why-it-matters); lines 314-316 (limits bullets)", "PASS",
    "Why-it-matters now says sufficiency 'fails without convexity' and shows it by Example 2.3 (lines 123). Limits bullets (314-316): 'A minimizer can have no multipliers. Example 3.1 ... Slater's condition fails there. The converse direction is not treated on this page.' Consistent with Example 3.1 and the table; the causal word issue is in row M7a-L03-R-and-misconceptions."))
rows.append(row("M7a-L03-structure", "2.9 structure and minimums", "L03.html (whole file)", "PASS",
    "check_pages --unit M7 PASS this round (ledgers/M7/scripts/M7-a-r7/check_pages_unit.txt). Section 3 renamed to 'Slater's condition and an example'; section order unchanged."))
rows.append(row("M7a-L03-lab-run", "2.5 lab: run and twin identity", "L03.html lab section 155-306; tests/labs/M7/lab-M7-L03-1.py", "PASS",
    "run_labs --unit M7 --page L03: PASS (1/1) this round. Lab section and twin byte-identical to pin 44f1eb6 (own check, extract of the section compared: identical). Twin exit 0 under python -I -W error, stderr 0 bytes (ledgers/M7/scripts/M7-a-r7/L03.stderr)."))
rows.append(carry("M7a-L03-lab-numbers", "L03.html lab section (identical bytes, so lines 283-304 unchanged)"))
rows.append(carry("M7a-L03-lab-prose", "L03.html lab section lines 155-306 (identical bytes)"))
rows.append(row("M7a-L03-lemmas-thm", "2.4 Lemmas 1.4, 1.5 and Theorem 2.1 and proofs", "L03.html lines 77-114", "PASS",
    "Re-read this round. Lemma 1.5 (line 90-96): q(w) = (1/2) w'Sigma w - c'w convex when Sigma is PSD; identity (1/2)[theta x'Sigma x + (1-theta) y'Sigma y - z'Sigma z] = (1/2) theta (1-theta)(x-y)'Sigma(x-y) re-derived. Example 3.1's use with Sigma = 2, c = 0 gives q(w) = w^2, correct. Theorem 2.1 (lines 104-107) and its proof (line 110): hypotheses f, g_i convex and differentiable, h_j affine; the proof uses differentiability of phi (see row M7a-L03-remark-2-2). Lemma 1.4 (lines 77-86) carried from round 6 (no hunk)."))
rows.append(row("M7a-L03-examples-sec4", "2.4 Examples 2.3, 3.1, 4.1, 4.2 and Remarks", "L03.html lines 121-153, 308-311", "PASS",
    "Example 2.3 (line 123): f(-1/2) = -1/8 and (1/2) f(-1) + (1/2) f(0) = -1/2; -1/8 > -1/2 so convexity fails; f'(0)=0 gives (K1) with no multipliers; f(-1) < f(0). Recomputed by hand. The sentence 'convexity of f is the one hypothesis that fails' is correct (no constraints, so the g_i and h_j hypotheses are vacuous). Example 3.1 (line 130): feasible set {0}, grad g1(0) = 0, (K1) reads 1 = 0. Slater's condition text (line 130) matches the definition used in the table. Examples 4.1 and 4.2 (lines 144-149) unchanged from round 6."))
rows.append(row("M7a-L03-open-item-proof", "2.4 theorem without proof or citation (Open item 3.2)", "L03.html lines 126-133 (formerly the Open item 3.2 block)", "PASS",
    "Round 6 FAIL. The theorem-form assertion (KKT necessity under Slater's condition, 'then there exist lambda and nu') and its 'not proved, sketched or graded' block are removed (grep: no 'Open item' in the page). Line 133 now says only 'The converse direction ... is not treated on this page', which asserts no result. Table row 170 of round 6 replaced by a T-graded Example 3.1 row (line 171) that is derived from (K1) and the feasible set. No unproven theorem remains."))
rows.append(row("M7a-L03-open-item-wording", "2.9 process and deferral wording in learner text (BUILDER_RULES 1.3, process words)", "L03.html lines 126-133, 318, 431-441, 458, 504-543", "PASS",
    "Round 6 FAIL. grep -i 'open item' over L03.html, the three L03 twins and the hub: 0 matches (ledgers/M7/scripts/M7-a-r7/ grep recorded in the round's notes). The learner-facing 'Open item 3.2' label appears nowhere. Round-6 'tracking label' text is gone from R2, R3, the quiz and the references."))
rows.append(row("M7a-L03-R-and-misconceptions", "2.4 problem solutions, misconceptions and quiz numerics", "L03.html line 438 (R3 solution); line 519 (quiz L03q7 explanation)", "FAIL",
    "R1 (line 424) and R2 (line 431) re-verified and correct. R3 (line 438) says Example 3.1 shows 'no multiplier exists, because Slater's condition fails'. The page's own computation (line 130, (K1) reads 1 + lambda*0 = 0) gives the cause: grad g1(0) = 0. Slater's failure is not shown to be the cause, and failure of Slater's condition does not imply that no multiplier exists in general. The quiz explanation (line 519) says 'No strictly feasible point exists, so Slater's condition fails, and the optimum has no KKT point', which reads the same way. Misconceptions (lines 326-339) re-checked: correct.",
    "Line 438: replace 'and no multiplier exists, because Slater's condition fails' with 'and no multiplier exists, because grad g1(0) = 0 makes (K1) false for every multiplier; Slater's condition also fails there'. Line 519: replace 'so Slater's condition fails, and the optimum has no KKT point (Example 3.1)' with 'and Slater's condition fails there; the optimum has no KKT point because (K1) reads 1 = 0 (Example 3.1)'."))
rows.append(carry("M7a-L03-notation", "L03.html (edits add no new symbol; Open item block with its symbols removed)"))
rows.append(carry("M7a-L03-cross-lesson", "L03.html lines 37, 102, 320; L01.html line 102; L02.html line 37 (none in hunks)"))
rows.append(row("M7a-L03-remark-2-2", "2.4 Theorem 2.1 hypotheses versus the Remark that claims them complete", "L03.html line 118 (Remark 2.2 text), lines 104-110 (Theorem 2.1 and proof)", "FAIL",
    "Remark 2.2 says 'The proof uses the four conditions, the convexity of f and of the g_i, and the affineness of the h_j. It does not use any hypothesis beyond these'. The proof (line 110) uses that phi is differentiable and applies Lemma 1.4, which needs differentiability; Theorem 2.1 (line 105) lists 'convex and differentiable on R^n' as a hypothesis. Differentiability of f and g_i is therefore used and missing from the remark's list, so the 'no hypothesis beyond these' sentence is false as written.",
    "Line 118: replace 'the convexity of \\(f\\) and of the \\(g_i\\), and the affineness of the \\(h_j\\). It does not use any hypothesis beyond these' with 'the convexity and differentiability of \\(f\\) and of the \\(g_i\\), and the affineness of the \\(h_j\\). It does not use any hypothesis beyond these'."))
rows.append(carry("M7a-DAG-links-pages", "index.html, L01.html, L02.html, L03.html local hrefs",
    "check_dag --unit M7 PASS and check_pages --unit M7 PASS this round (link and anchor checks) confirm the links."))
rows.append(row("M7a-plan-compliance", "plan section 8 and architect decisions B1, B2, Q1-Q6, Q12", "plans/M7-build-plan.md section 4 and section 8 item 6 (Slater as hypothesis); index.html; L01-L03", "PASS",
    "plans/ unchanged between 44f1eb6 and 7aa909e (git diff empty for plans/). Plan item 6 requires KKT necessity to be stated with its hypothesis, not assumed; the necessity claim was removed rather than stated, which the plan allows (the plan lists it as an additional item, not a required result). Theorem 2.1 states all its hypotheses (plan item 6 KKT sufficiency). Hours 9/9/10 match plan section 4. Architect decision B1 (covariance outside M7) disclaimer at index.html line 167 unchanged."))

fragment = {
    "unit": "M7",
    "slice": "a",
    "round": 7,
    "verifier": "independent verifier (Haiku), round 7, fresh context, no builder context",
    "pin": "7aa909e",
    "base": "44f1eb6 (round 6 pin; B-M7-a.round6.json used as context only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-M7-a",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB7-M7-a/ledgers/M7/scripts/M7-a-r7",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "stokey1989recursive: the record has three authors (Stokey, Lucas, Prescott); the pages cite it as 'Stokey & Lucas' per the curriculum. No registry change requested (carried from round 6)."
    ],
    "freshness_flags": [],
    "notes": [
        "Slice a is not a project slice: no mutants and no alternative implementations required (VERIFIER_RULES 2.6 does not apply).",
        "Delta reviewed: git diff 44f1eb6..7aa909e for index.html, L01-L03 and tests/labs/M7 L01-L03 twins (all hunks read). Rows whose cited lines have no hunk are carried with the round-6 prefix; rows whose subject changed were re-verified.",
        "Round-6 FAIL rows M7a-L03-open-item-proof and M7a-L03-open-item-wording are resolved (the Open item block and label are removed).",
        "New FAILs: M7a-L03-R-and-misconceptions (causal 'because Slater's condition fails', lines 438 and 519) and M7a-L03-remark-2-2 (Remark 2.2 omits differentiability).",
        "check_pages --page index is not a valid hub check; the hub is validated by check_pages --unit M7 (PASS).",
        "Not checked: full M7 gate (only slice commands run); verify_refs --unit M7 live run was done (2 of 560 entries, 0 problems); Pyodide timing is page_smoke's measure only; no pytest run beyond the M7 lab tests (3 selected tests reported dots only, exit not captured separately); 2025-2026 freshness not reviewed (no debate brief in slice); Crossref lookup of Boyd and Stokey not re-read at the locator because no locator is cited.",
    ],
    "summary": {},
}
n = len(rows)
p = sum(1 for r in rows if r["status"] == "PASS")
f = sum(1 for r in rows if r["status"] == "FAIL")
u = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
fragment["summary"] = {"rows": n, "pass": p, "fail": f, "unverifiable": u}
out = CHK + "/ledgers/M7/M7-a.json"
json.dump(fragment, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out, fragment["summary"])
missing = set(prev_rows) - {r["id"] for r in rows}
print("round-6 ids not carried:", sorted(missing))
