"""Build ledgers/M2/M2-c.json (round 3) from the row decisions made while reading the slice (python -I)."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/B-M2-c.round2.json").read_text(encoding="utf-8"))
C = "Carried from round 2 (course/modules/M/M2/L13-L18 cited sentences and tests/labs/M2/lab-M2-L14..L18 byte-identical since the previous pin): "
R = "Re-verified on aa3c26c: "
F = {}  # id -> (status, evidence, fix)
F["M2c-cmd-check_pages"] = ("PASS", R + "`.venv/bin/python tools/check_pages.py --unit M2` -> 'check_pages M2: PASS' (rc 0).", None)
F["M2c-cmd-check_dag"] = ("PASS", R + "`tools/check_dag.py --unit M2` -> 'check_dag M2: PASS' (rc 0).", None)
F["M2c-cmd-run_labs"] = ("PASS", R + "`tools/run_labs.py --unit M2` -> 'run_labs M2: PASS (27/27)'; each twin run alone as `python -I -W error` exit 0 (outputs in /tmp/M2-v/c/twin_L13..L18.out).", None)
F["M2c-cmd-page_smoke"] = ("PASS", R + "`tools/page_smoke.py --unit M2 --pages L13 L14 L15 L16 L17 L18` -> six pages PASS, 'page_smoke M2: PASS' (rc 0).", None)
F["M2c-cmd-ruff-mypy"] = ("PASS", R + "`ruff check` and `ruff format --check` on tests/labs/M2/lab-M2-L13..L18-1.py: all passed, 6 files formatted; `mypy --no-incremental` on the six twins: no issues.", None)
F["M2c-cmd-verify_refs"] = ("PASS", R + "`tools/verify_refs.py --offline`: 560 entries, 0 problems; `--unit M2`: 2 of 560 entries, 0 problems. references/ and tools/ unchanged 1817191..aa3c26c (git diff --stat empty).", None)
F["M2c-hours-arith"] = ("PASS", R + "index.html data-hours-lessons=240 and data-hours-project=60 (sum 300); project.html data-hours-project=60; L13..L18 eyebrow and data-hours=10 each; 24 x 10 = 240.", None)
F["M2c-links-anchors"] = ("PASS", R + "Python -I scan of every href in L13..L18: each #fragment exists in its page, each relative file and fragment (e.g. ../../../concepts.html#exponential-and-logarithm, L01.html#def-limit) resolves. No broken link.", None)
F["M2c-dag-closure"] = ("PASS", R + "check_dag M2 PASS; L13..L18 concept links use only M2 concepts and M1 exponential-and-logarithm (plan lines 30-31 closure: M1 and P0.1).", None)
F["M2c-banned-scan"] = ("PASS", R + "regex scan of visible prose of L13..L18 for 'roughly half', 'about 6%', 'historically' and ellipses: 0 hits.", None)
F["M2c-process-words"] = ("PASS", R + "visible prose of L13..L18 scanned for builder, verifier, round N, unit report, REQUESTS: 0 hits.", None)
F["M2c-quiz-misc-counts"] = ("PASS", R + "L13 quiz has 10 items (within 8-15); L14..L18 quiz blocks are outside the changed sentences of the delta and unchanged in count.", None)
F["M2c-why-words"] = ("PASS", R + "why-it-matters word counts: L13 106, L14 97, L15 89, L16 95, L17 83, L18 102 (all <= 120).", None)
F["M2c-num-L13"] = ("PASS", R + "Corollary 4.1 lab hypothesis now says M = e is the limit of max|f''| on [1,1+h0] (e^(1+h0)), and L13 Section 5 uses M = e only as that value. Recomputed (scripts/M2-c-r3/arithmetic_checks.out): h* forward = 1.8076e-8; central (3 delta/e)^(1/3) = 6.2578e-6; 2 sqrt(e delta) = 4.9136e-8; Example 2.3 intervals 0.0135914..0.0137280 and 4.4854e-5..4.5760e-5; R1 h* = 0.038360; ratios 32.62 and 301.10 (Misconception 1, 2). Lab printed table re-run and identical.", None)
F["M2c-num-L14"] = ("FAIL", R + "Example 4.1 values f(2)=15.232760911274 and f'(2)=21.731770521812 match the displayed 15.232760911 and 21.731770522. But the E1 solution (L14.html, emp-1) states that 2.3197768247 x 0.5403023059 x 2 = 2.5067615350; the product of those displayed factors is 2.5067615351175796 (arithmetic_checks.out, python -I), so the tenth decimal is wrong by 1e-10.", "In the emp-1 solution of L14.html write 2.5067615351 for the product of the displayed factors (or write 'agrees to nine decimals' with the printed 2.5067615350).")
F["M2c-num-L15"] = ("PASS", R + "L15 interpretation: 2/(3 sqrt 3) = 0.38490018 (script output 0.3849001794597505); sequence f(1/n,1/n)=1/(2n) and g=1/2; lab output re-run identical.", None)
F["M2c-num-L16"] = ("PASS", R + "Example 1.3: 4+2e^2 = 18.778112198, 1+e^2 = 8.389056099; E1: F_xxx = y^3 e^(xy) <= e^2.00001, bound 1e-10/6 x 7.39 = 1.2e-10; delta = 2^-52-ish spacing near 11.39 gives delta/h = 8.9e-11; E3: 2+3e^2 = 24.167168. All recomputed.", None)
F["M2c-num-L17"] = ("PASS", R + "|grad| = 2.12727907824 (script), angle 61.9602 deg, L-infinity maximum over the unit square 2.410182 (unrounded), unit vectors (0.4701, 0.8826) and (0.5326, 1): recomputed.", None)
F["M2c-num-L18"] = ("PASS", R + "Example 4.2 Jacobian [[2,-4],[4,2]] at (1,2) recomputed from the partials; R3 bound 3 delta/(2 h*) statement consistent with P3 of L13.", None)
F["M2c-lab-L13"] = ("PASS", R + "Twin line 16 now `EXACT = math.e`, the docstring says errors are measured against math.e (line 6), and the page embed (L13.html) carries the same code. Output re-run: forward minimum 1e-08, central minimum 1e-05, tie with 1e-07 at 5.858691e-11 vs 5.858736e-11 (difference 4.4e-17 < 1e-15, as the interpretation says).", None)
for n in range(14, 19):
    F[f"M2c-lab-L{n}"] = ("PASS", C + f"tests/labs/M2/lab-M2-L{n}-1.py byte-identical; twin rerun exit 0; page embed matches (run_labs PASS).", None)
F["M2c-grades-L13"] = ("PASS", R + "Key-results rows: T rows are Theorems 2.1, 2.2, Prop 3.2, Cor 4.1 (hypotheses listed) and the Example 2.3 rows, which are T under the explicit Assumption 1; C rows are the lab results. The grades match the stated hypotheses. The card grades disagree for the Example 2.3 claims: see M2c-cards-L13.", None)
F["M2c-grades-L14"] = ("PASS", R + "Assumption 1 is now stated and Prop 3.1 and Prop 5.2 say 'Assume Assumption 1'; key-results rows are T under it and C for the lab. Consistent with the stated hypotheses.", None)
for n in range(15, 19):
    F[f"M2c-grades-L{n}"] = ("PASS", R + f"L{n} claim spans and key-results table: rows changed by Assumption 1 are T under the explicit assumption; lab rows C. Consistent.", None)
F["M2c-math-L13"] = ("PASS", R + "Thm 2.1, Thm 2.2 (proofs re-derived), Prop 3.2, Cor 4.1 (B'(h), B''(h), h*, B(h*) recomputed), P1-P3 and M1-M3, E1-E3, R1-R3 re-derived. The round-2 exp-derivative gap is now an explicit Assumption 1.", None)
F["M2c-math-L14"] = ("PASS", R + "Def 2.1 formulas, Prop 3.1 (induction with Assumption 1 in the statement), Prop 5.2 path sum, Example 5.1 adjoints (2+cos1 = 2.540302306), Example 4.1 (recomputed), M1-M3, P1-P3, R1 ((a+e1+e2)^3 coefficient 6a, f''=6a), R3 (max(x,0)). Only the E1 digit is wrong: M2c-num-L14.", None)
for n in range(15, 19):
    F[f"M2c-math-L{n}"] = ("PASS", C + f"L{n} proofs and problems; the sentences changed by Assumption 1 were re-derived: L16 F_xxx, F_xy=F_yx (24.167168); L17 partials and gradient (1, 1.8775825619), directional formula, R1, R2 and E2 third partials 6u1^2u2 - u2^3 cos y; L18 R1 partials and the sequence (rho_k) limit -1.", None)
F["M2c-math-L17-R2"] = ("PASS", R + "L17 R2: f=x^2 y/(x^2+y^4): partials at origin 0; D_u f(0)=sin(theta) for cos(theta)!=0 (t cos^2 sin/(cos^2 + t^2 sin^4) / t -> sin); d f/dx = 2 x y^5/(x^2+y^4)^2 = 1/(2y) on x=y^2. Re-derived.", None)
F["M2c-prose-L13-quiz-cancel"] = ("PASS", C + "L13 misconception 2 and quiz explanation L13q4 unchanged in the delta.", None)
F["M2c-prose-L14-E2"] = ("PASS", R + "L14 E2 solution re-read: grid 0.5..3.0; the claim that the lab does not establish points outside the grid is accurate.", None)
F["M2c-prose-L16-L18-hypothesis"] = ("PASS", C + "L16 Remark/Prop hypothesis text and L18 Theorem 4.1 hypothesis (every partial exists on a ball, continuous at a) unchanged in meaning.", None)
F["M2c-prose-L17-example-after"] = ("PASS", C + "L17 line 76 example text unchanged in meaning.", None)
F["M2c-prose-L17-heading"] = ("PASS", C + "L17 Section 4 bullet 1 unchanged in meaning.", None)
F["M2c-prose-L18-sin-not-Au"] = ("PASS", R + "L18 Section 5 bullet 2 and card M2-c276: f=x^2y/(x^2+y^4) partials 0 at origin, D_u f(0)=sin theta, so no array A works; re-derived.", None)
F["M2c-cards-dupscan"] = ("PASS", R + "cards.json: 376 cards (was 377: M2-c164 removed in the delta); slice ids M2-c181..M2-c279 unique, 99 slice cards; no duplicate ids and no duplicate fronts across the file (python -I scan).", None)
F["M2c-cards-L13"] = ("FAIL", R + "M2-c188 and M2-c189 are graded C (basis: 'the assumed fact'), but the L13 key-results rows for the same Example 2.3 bounds are graded T under Assumption 1. M2-c190 is graded T and gives the ratio interval 9.990..10.101 and 98.91..101.11 without naming Assumption 1, which the lesson's row and Example 2.3 use. M2-c181..c187, c191..c201 checked against the current text (ok).", "Make the card grades match the lesson (T with 'under Assumption 1' in the back for c188, c189, c190, or lower the key-results rows to C) and add 'under Assumption 1' to the back of M2-c190.")
F["M2c-cards-L14"] = ("FAIL", R + "M2-c218 is fixed (back now says the tangent is the derivative of the program as written; matches Section 6 and misconception 3). But M2-c211 (Proposition 5.2, T) omits the hypothesis 'Assume Assumption 1' that the lesson states, and M2-c206 (Example 4.1, T) gives f'(2) without naming Assumption 1 that the example uses. Other L14 cards checked against the lesson text (ok).", "Add 'under Assumption 1' (Proposition 5.2 hypothesis list) to M2-c211 and to the back of M2-c206.")
F["M2c-cards-L15"] = ("PASS", C + "L15 cards M2-c220..c238 unchanged; the one changed L15 sentence (line 9 scope) is not cited by any card; cards agree with the lesson text.", None)
F["M2c-cards-L16"] = ("FAIL", R + "M2-c241 (T) gives F_x and F_y at (1,2) for Example 1.3, but L16 Example 1.3 now starts 'Under Assumption 1, holding y fixed ...' and the card names no assumption. The other L16 cards checked against text (ok).", "Add 'under Assumption 1' to the back of M2-c241.")
F["M2c-cards-L17"] = ("FAIL", R + "L17 now states Assumption 1 for the sin derivative in Example 1.2, Example 2.3 and Problem R1, but the T cards M2-c252 (gradient of Example 1.2), M2-c255 (directional formula of Example 2.3), M2-c258 (largest-coordinate-norm steepest direction, which uses the gradient), M2-c262 (Example 2.3 formula in every direction) and M2-c264 (steepest direction under the largest-coordinate norm) name no assumption. Cards M2-c251, c253, c254, c256, c257, c259..c261, c263 checked (ok).", "Add 'under Assumption 1 (derivative of sin is cos)' to the backs of M2-c252, c255, c258, c262, c264.")
F["M2c-cards-L18"] = ("FAIL", R + "M2-c277 (T) says f is differentiable at the origin and its partial in x is not continuous there; Problem R1 (L18) now says 'Under Assumption 1' for the partial derivative formula, and the card names no assumption. Other L18 cards (c265..c279 except c277) checked against text (ok).", "Add 'under Assumption 1' to the back of M2-c277.")
F["M2c-quiz-answers"] = ("PASS", R + "L13 quiz numeric answers 2.5, 2, 0.1 and mc keys checked: L13q1 forward order h, L13q5 grows without bound, L13q7 h*=2 sqrt(delta/M), L13q9 0 for |t| central quotient; L14q1 epsilon^2=0, L14q2 tangent 7 at x=2 (2x+3). Others in the unchanged quiz blocks.", None)
F["M2c-scope-words"] = ("PASS", R + "every 'only', 'always', 'all', 'same', 'every' in visible prose of L13..L18 was listed (python -I scan) and the ones that make a claim were witnessed: e.g. L15 'the norm is zero only at the zero point', L15 sup|g| = 1/2 'over all theta', L17 'exists only in the four axis directions' (computed), L18 'Jacobian is the only array' (Prop 3.2), L14 'the same function max(x,0)' (both programs compute it).", None)
F["M2c-freshness"] = ("PASS", R + "no debate brief and no registry key cited on L13..L18 (References sections say so).", None)
F["M2c-attribution"] = ("PASS", C + "References sections of L13..L18 cite only the curriculum sources by name and state that no locator is confirmed; no bibliographic data is typed from memory.", None)

prev_rows = prev["rows"]
ids = [r["id"] for r in prev_rows]
extra = [i for i in F if i not in ids]
rows = []
for r in prev_rows:
    st, ev, fix = F[r["id"]]
    row = {"id": r["id"], "check": r["check"], "location": r["location"], "status": st, "evidence": ev}
    if fix:
        row["fix"] = fix
    rows.append(row)
assert not extra, extra
out = {
    "unit": "M2",
    "slice": "M2-c",
    "round": 3,
    "verifier": "independent Haiku verifier (M2 slice c, round 3; did not build M2; no shared context with builders or earlier verifiers)",
    "pin": "aa3c26c",
    "base": "1817191 (the round-2 pin; delta computed with git diff 1817191 aa3c26c)",
    "previous_fragment": "/tmp/fanout-frags/B-M2-c.round2.json (context only; PASS rows re-decided; carried only where the cited sentences are unchanged)",
    "checkout": "/tmp/verifyB3-M2-c (detached at aa3c26c; .venv symlinked; vendor copied)",
    "scratch": "/tmp/M2-v/c",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "delta_since_previous_pin": "course/modules/M/M2/L13.html, L14.html, L15.html, L16.html, L17.html, L18.html (Assumption 1 sentences added; scope words edited; L13 lab-related prose); tests/labs/M2/lab-M2-L13-1.py (EXACT = math.e, docstring unchanged); course/modules/M/M2/cards.json (cards M2-c188, c205, c218 in the slice changed; others outside the slice); index.html and project.html hours unchanged. Unchanged: tests/labs/M2/lab-M2-L14..L18-1.py, references/, tools/, notation/, plans/.",
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lesson slice, not a project slice: no mutants written or run (ARCHITECT ruling: mutation applies to project graders only); no alternative implementations run.",
        "Brief closure text ('AC1, S0, S2') differs from plans/M2-build-plan.md lines 30-31 ('M1 and P0.1 only'); the plan was used.",
        "Not run: tools/build_site.py --check, tools/render_curriculum.py, tools/fetch_data.py --check, tools/check_projects.py (not slice gates); the full gate (not requested).",
        "The exp and sin derivative facts are now explicit Assumption 1 on each page; T rows that depend on them are read as conditional T under an explicit assumption (no proof of exp'=exp is given or cited). Flagged only where a card drops the assumption.",
        "Hours: L13-L18 at 10 h each, arithmetic only; pace not judged (architect ruling).",
        "R1 of L13 says Proposition 3.2's hypothesis fails for a random error; accepted as the page states it (Prop 3.2 treats the error as a fixed function).",
    ],
    "summary": {},
    "rows": rows,
}
from collections import Counter
c = Counter(r["status"] for r in rows)
out["summary"] = {"rows": len(rows), "pass": c["PASS"], "fail": c["FAIL"], "unverifiable": c["UNVERIFIABLE"],
                  "fail_ids": [r["id"] for r in rows if r["status"] != "PASS"]}
Path(root / "ledgers/M2/M2-c.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(out["summary"])
