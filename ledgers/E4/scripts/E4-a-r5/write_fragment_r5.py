"""Builds the round-5 fragment for E4 slice a from the round-4 rows (ids kept) plus the round-5 rows.

Every round-4 row was re-verified in round 5 by a full re-read of the slice (the round-5 delta is single-line
in-place substitutions, so the round-4 locators still hold). Only the three round-4 FAIL rows change status.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
R4 = Path("/Users/billyribeiro/.fanout/frags/E-E4-a.round4.json")
OUT = ROOT / "ledgers" / "E4" / "E4-a.json"
SCR = "ledgers/E4/scripts/E4-a-r5/"

r4 = json.loads(R4.read_text(encoding="utf-8"))
prefix = ("R5 re-verified by full re-read of the slice (round-5 delta = in-place single-line substitutions, "
          "round-4 locators hold): ")

updated = {
    "E4a-r4-def33-hypothesis": (
        "PASS",
        "L03.html line 69 now reads 'let x be a strictly positive bundle (x_r > 0 for every state r)'. A4 gives "
        "U_i = -inf at a zero entry, so the partial derivatives are defined only there; the definition is now "
        "consistent. Re-derived MRS formula pi_s u'(x_s)/(pi_t u'(x_t)) (line 71) unchanged.",
    ),
    "E4a-r4-gg-undefined": (
        "PASS",
        "grep -F '\\gg' over index.html, L01-L03 and tests/labs/E4/lab-E4-L0[123]-1.py returns no line "
        "(log in " + SCR + "structure_counts.out session; command output empty). L02 line 466 now says 'every entry "
        "of ebar strictly positive', line 510 'strictly positive prices q'; L03 lines 93, 376, 378 use words.",
    ),
    "E4a-r4-P2-only-scope": (
        "PASS",
        "L03.html line 333 prompt now reads 'using the formulas of Proposition 2.9 and the derivative of the "
        "logarithm, u_i'(x) = 1/x'; the solution (line 335) uses exactly those; re-derived MRS "
        "(pi_s ebar_t)/(pi_t ebar_s) = q*_s/q*_t with theta_i cancelling (" + SCR + "rederive_numbers.out).",
    ),
}

rows = []
for r in r4["rows"]:
    if r["id"] in updated:
        st, ev = updated[r["id"]]
        rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
    else:
        rows.append({"id": r["id"], "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": prefix + r["evidence"]})

new = [
    ("E4a-r5-cmd-check_pages-E4", "2.9 structure / banned phrases", "index.html, L01.html, L02.html, L03.html",
     "PASS", "`.venv/bin/python tools/check_pages.py --unit E4` -> 'check_pages E4: PASS' (rc 0); log " + SCR + "check_pages_E4.out. Also `--all` grep for E4: PASS."),
    ("E4a-r5-cmd-check_dag", "2.9 DAG", "index.html, L01-L03",
     "PASS", "`.venv/bin/python tools/check_dag.py --all` rc 0, 27 PASS lines, line 13 'check_dag E4: PASS' (" + SCR + "check_dag.out). Concept closure: E2 L03 defines adverse-selection, E2 L04 signaling, E1 defines competitive equilibrium."),
    ("E4a-r5-cmd-run_labs", "2.5 labs", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
     "PASS", "`.venv/bin/python tools/run_labs.py --unit E4` rc 0, output 'run_labs E4: PASS (12/12)' (" + SCR + "run_labs_E4.out)."),
    ("E4a-r5-lab-twins-alone", "2.5 labs (twins alone)", "tests/labs/E4/lab-E4-L01-1.py, L02-1.py, L03-1.py",
     "PASS", "Run from cwd /tmp with `python -I -W error` on each twin: rc 0 for L01, L02, L03; stderr 0 bytes each; stdout saved to " + SCR + "twin-L0x.out."),
    ("E4a-r5-lab-embed-equality", "2.5 labs (page = twin = expected)", "L01.html, L02.html, L03.html lab sections",
     "PASS", SCR + "check_twins_embed.py output ALL_OK: page code == twin for L01-L03 (True), page pre.expected == twin output (True), twin stderr empty (" + SCR + "check_twins_embed.out)."),
    ("E4a-r5-cmd-ruff-mypy", "tooling gates", "tests/labs/E4 twins; repository mypy",
     "PASS", "`ruff check` and `ruff format --check` on the three twins: pass (ruff_twins.out, ruff_format_twins.out). `mypy --no-incremental` on the full repository: 'Success: no issues found in 385 source files' (mypy_full.out)."),
    ("E4a-r5-cmd-pytest", "tooling tests", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
     "PASS", "`.venv/bin/pytest -q` on the three modules: all dots, rc 0 (" + SCR + "pytest_relevant.out)."),
    ("E4a-r5-cmd-page_smoke", "2.9 page smoke", "index.html, L01.html, L02.html, L03.html",
     "PASS", "`.venv/bin/python tools/page_smoke.py --unit E4 --pages index.html L01.html L02.html L03.html` rc 0, 'page_smoke E4: PASS' (" + SCR + "page_smoke_E4_abc.out)."),
    ("E4a-r5-cmd-verify_refs", "2.1 citations", "data-references of index.html, L01-L03 (empty lists)",
     "PASS", "`verify_refs.py --offline`: 'offline integrity: 560 entries, 0 problems'. `verify_refs.py --unit E4` (live Crossref): '3 of 560 entries, 0 problems'. The four slice pages cite no registry key (empty data-references), so nothing in slice a is cited (" + SCR + "verify_refs_*.out)."),
    ("E4a-r5-structure-counts", "2.9 structure minimums", "L01-L03 and index.html",
     "PASS", "structure_counts.py output: why-it-matters words L01 107, L02 117, L03 120 (<=120); 3 misconceptions each; 3 problems in each of 4 tiers each; 12 solution blocks each; quiz items 9 each with 9 explain blocks; key-results rows 5, 6, 5; hub objectives 8, lesson cards 9, placement items 8 with 2 data-skill (" + SCR + "structure_counts.out). Section order matches BUILDER_RULES 4.2 (no debate field in curriculum E4, so no debate brief)."),
    ("E4a-r5-hours", "2.9 hours arithmetic", "index.html lines 29, 40-43; curriculum.json E4 entry; L01-L03 data-hours",
     "PASS", "Hub data-hours-lessons=72, data-hours-project=28, sum 100 = curriculum E4 hours 100 (curriculum.json E4 entry, Tier M). 9 lessons x 8 h = 72 (cards 'L0n · 8 h'; L01-L03 data-hours=8). 28% of 100 is within the 10-40% band."),
    ("E4a-r5-num-rederive", "2.2 numbers", "index.html lines 68, 73, 117-126; L01 lines 113-161, 262-281, 320-336, 386, 402-404, 448-462; L02 lines 124-126, 187, 299-363, 377-393, 429-443, 506-529; L03 lines 119, 250-261, 301-310, 335-336, 385, 476",
     "PASS", "Independent exact re-derivation in " + SCR + "rederive_numbers.py (77 exact checks, all OK, plus float check): L01 V(x)=340/3, V(y)=56, combined 596/3, E x=235/4, M1 55/3 and 25/2 and 35/6, M3 -1/8, 11/8, 17/8, R2 1/4 and 1; L02 theta=9/16, 7/16, q*=(1/8,1/32,1/16), x1*=(9/4,9/2,9/4), x2*=(7/4,7/2,7/4), Remark 2.6 wealth 11 and 9, demands (11/4)^3 and (9/4)^3, excess (1,-3,1), q.z=0, unweighted sum -1; L03 MRS 4, 2, 1/2 for both agents, price ratios 4, 2, 1/2, endowment MRS 8/3 and 8, R2 derivatives 1/12 and 1/4; hub Q1 6, Q5 8, 6/8=75%, 7/8=87.5%. Float check: both agents' utility gains positive at eps = 1e-2, 1e-3, 1e-4."),
    ("E4a-r5-hunk-index-lede", "2.9 prose / DAG (hub lede)", "index.html line 33",
     "PASS", "Lesson map in the lede checked against the lesson titles: Lessons 1-2 Arrow-Debreu securities and equilibrium, 3 first welfare theorem, 4 complete/incomplete, 5-6 RE with and without noise traders, 7 informativeness, 8 Grossman-Stiglitz, 9 no-trade theorem (lesson h1s in L01-L03 and cards in index.html lines 141-149). Hours 72/28 unchanged."),
    ("E4a-r5-hunk-L01-A2-section", "2.9 prose / cross-reference", "L01.html line 51",
     "PASS", "'Assumption A2 (§3)': the section numbered 3 in L01 is 'Valuation and the prices of the securities' and contains Assumption A2 (line 99). Cross-reference correct."),
    ("E4a-r5-hunk-L02-remark26-section-refs", "2.9 prose / cross-reference / numbers", "L02.html line 125",
     "PASS", "'Example 2.11 (§4)': §4 is 'An equilibrium in closed form' containing Example 2.11 (line 186). 'Proposition 2.8 (§3)': §3 'Logarithmic utility and the closed-form demand' contains Prop 2.8 (line 143). Values re-derived: w1=11, w2=9, demands (11/4)^3 and (9/4)^3 with pi=(1/2,1/4,1/4), excess (1,-3,1) (rederive_numbers.out)."),
    ("E4a-r5-hunk-L02-R3-every-entry", "2.9 prose (problem R3 prompt)", "L02.html line 466 and solution line 468",
     "PASS", "Prompt now asks which parts need 'every entry of ebar strictly positive' and 'w_i > 0'. Solution (line 468) says Prop 2.9 needs ebar_s > 0 for every state and Prop 2.8 needs only w > 0 and q in (0,inf)^S; consistent with A3 and Prop 2.8 (line 144)."),
    ("E4a-r5-hunk-L02-Q3-strict-positive", "2.9 prose (quiz Q3)", "L02.html line 510 and explain line 516",
     "PASS", "'at any strictly positive prices q at which both agents have demands' has the same meaning as 'q >> 0' and Prop 2.5 (line 110) hypothesis q in (0,inf)^S; the correct option q.z(q)=0 and the explanation are unchanged and consistent."),
    ("E4a-r5-hunk-L03-def33", "2.4 mathematics (Definition 3.3)", "L03.html line 69",
     "PASS", "Hypothesis is strictly positive bundle, consistent with the convention U_i=-inf at a zero entry (A4, L02 line 66-68). u_i' > 0 on (0,inf) is argued in the proof of (b) (line 109): u' >= 0 by strict increase, u' nonincreasing by concavity, and u'(z)=0 at any z would force u constant on (z,inf). Forward pointer to Prop 3.4 (b) is explicit (see E4a-r5-forward-ref)."),
    ("E4a-r5-hunk-L03-prop34a-step", "2.4 mathematics (proof of Prop 3.4 (a))", "L03.html line 93",
     "PASS", "Lemma 2.4 hypotheses (w_i > 0 from q* strictly positive and e^i strictly positive by A3, and q* in (0,inf)^S) are met; conclusion 'every entry of x^{i*} strictly positive' is Lemma 2.4's conclusion (line 101); U_i finite and q*.x=w_i (Prop 2.5, line 115). Step 1-3 algebra re-read (lines 94-100)."),
    ("E4a-r5-hunk-L03-counts-only", "2.9 prose / lab interpretation", "L03.html lines 124, 261, 280",
     "PASS", "Removal of 'only' at line 280 is accurate: Part B (code lines 233-240) counts grid allocations for which improves() holds (no agent worse off by more than TOL, one better by more than TOL), which is Definition 3.2. Output 0 and 2 (lines 258-259) reproduced by " + SCR + "twin-L03.out."),
    ("E4a-r5-hunk-L03-P2-prompt", "2.9 prose (problem P2)", "L03.html lines 333-335",
     "PASS", "Prompt now permits the derivative of the logarithm; solution uses u_i'(x)=1/x (line 335) with x*_s = theta_i ebar_s; MRS = (pi_s ebar_t)/(pi_t ebar_s) = q*_s/q*_t (re-derived)."),
    ("E4a-r5-hunk-L03-R1-prompt", "2.9 prose (problem R1)", "L03.html lines 376-378",
     "PASS", "Prompt now refers to 'strict positivity of every price q*_s'; solution (line 378) uses q* . (ebar - (y1+y2)) >= 0 because every price is strictly positive, and the contradiction is valid (q* . ybar sum > q* . ebar)."),
    ("E4a-r5-hunk-L03-R2-solution", "2.4 mathematics (problem R2)", "L03.html line 385",
     "PASS", "Re-derived: y1=(3-e, 4+4e, 1), y2=(1+e, 4-4e, 3) add to (4,8,4); dU1/de at 0 = 1/2*(-1/3)+1/4*1 = 1/12; dU2/de = 1/2*1+1/4*(-1) = 1/4 (rederive_numbers.out lines). Endowment MRS_12: agent 1 (1/2/3)/(1/4/4)=8/3, agent 2 (1/2/1)/(1/4/4)=8. 'Agent 1 needs 8/3 units of state 2 to give up one unit of state 1' is the Def 3.3 convention (dx2 = MRS_12 * (-dx1) at constant utility). The 4-per-unit trade gains both agents. Float check with eps 1e-2, 1e-3, 1e-4: both gains positive."),
    ("E4a-r5-gg-symbol-gone", "2.9 notation / define-before-use", "index.html, L01-L03, tests/labs/E4 twins",
     "PASS", "`grep -F '\\gg'` over the slice and the three twins returns no lines; `grep -F '\\ll'` no lines."),
    ("E4a-r5-notation-registry", "2.8/2.9 notation (BUILDER_RULES 3)", "notation/notation.json; slice pages",
     "PASS", "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q and macros including \\E, \\R, \\indic, \\Prob. Slice uses \\E (expectation, L01 line 138) and \\R (e.g., L01 line 79, L03 line 59), and mathrm{MRS}, iota, pi, theta, lambda and Omega, which the registry leaves to each lesson (its 'about' text). No registered symbol appears with another meaning. Observation (not a registered symbol, so not a FAIL): e denotes the security e_s (L01 Def 1.3) and, with superscript, agent endowments e^i (L02 Def 2.1 onward); L03 line 105 restates e_s as the Arrow-Debreu security."),
    ("E4a-r5-scope-word-scan", "2.9 prose (rule 4 scope words)", "index.html, L01-L03",
     "PASS", "grep -o -i for only|always|never|exactly|same|all|every|any|in general|drives over the four pages and every hit read in context (about 90 hits). Each universal claim has a stated hypothesis or a proof (e.g. L01 line 62 A1; L01 line 88 proof uses no probability; L02 line 120 A4 and A1; L03 line 367 grid vs continuum)."),
    ("E4a-r5-hub-kkt-unused", "2.9 prose / DAG usage (hub prerequisite claim)", "index.html line 63",
     "FAIL", "Hub line 63 says 'From M7 it uses Lagrange multipliers and the KKT conditions' (link data-concept=\"kkt-conditions\"). grep -i -E 'KKT|Karush' over index.html, L01-L09 and project.html returns matches only in index.html (count 4 in index.html, 0 in every lesson and project.html). The lesson text, the labs and the project never use KKT. Lagrange multipliers are used (L02 lab Part D 'multiplier', L02 E3 solution, placement item 3). The concept claim 'the unit uses ... the KKT conditions' is unsupported in the pages."),
    ("E4a-r5-hub-prereq-usage", "2.9 prose / DAG usage (hub prerequisite list)", "index.html lines 63 (other concepts)",
     "PASS", "Each other concept linked in the hub prerequisite paragraph is used in an E4 page: utility-maximization, competitive-equilibrium, pareto-efficiency (L03), externality (L03 canon-breaks), expected-utility (L02 Uses), certainty-equivalent and arrow-pratt-risk-aversion (L08), adverse-selection (L09, E2 L03 defines it), random-variable, expectation, variance, correlation, normal-distribution, conditional-expectation-elementary (L05-L08), linear-map and vector-space (L01, L04), orthogonal-projection (L06 Lemma 6.4 'linear projection', outside slice a), derivative (L02 R2) and gradient (L03 proof of (b)). Links resolve (check_pages PASS)."),
    ("E4a-r5-forward-ref", "2.9 prose (terms used before definition)", "L03.html line 69; L02.html lines 125, 71; L01.html line 51",
     "PASS", "Forward pointers are explicit: Def 3.3 cites the proof of Prop 3.4 (b), which is a proof already in the lesson, and L02 Remark 2.6 cites 'Example 2.11 (§4)' and 'Proposition 2.8 (§3)' by section. The rule forbids links to a later lesson, not to a later section; no concept is linked to a later lesson."),
    ("E4a-r5-quiz-explanations", "2.9 retrieval quiz", "L01.html 437-505; L02.html 495-567; L03.html 418-486",
     "PASS", "All 27 quiz items read; each explanation's numbers re-derived (L01 Q2 4.25, Q4 3, Q7 0.6; L02 Q2 2, Q5 0.125; L03 Q2 2, Q5 2, Q8 4); each cited lesson item exists (Problem M1, P1, P2, M2, Misconceptions 1-3, Remark 2.10, Remark 3.5)."),
    ("E4a-r5-why-it-matters", "2.9 structure (BUILDER_RULES 4.2 item 1)", "L01.html line 51; L02.html line 51; L03.html line 51",
     "PASS", "Word counts (structure_counts.out): 107, 117, 120; all at most 120."),
]

for rid, check, location, status, evidence in new:
    rec = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        rec["fix"] = ("In index.html line 63 delete the clause 'and <a class=\"concept\" data-concept=\"kkt-conditions\" "
                      "href=\"../../../concepts.html#kkt-conditions\">the KKT conditions</a>' (keep Lagrange multipliers), "
                      "or add a sentence in a lesson that uses the KKT conditions. Then re-run check_dag and check_pages.")
    rows.append(rec)

ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate row ids"

fragment = {
    "unit": "E4",
    "slice": "a",
    "round": 5,
    "verifier": "Haiku independent verifier, E4-a round 5 (did not build E4; no shared context with the builders)",
    "pin": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
    "base": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba (round-4 pin). Delta in the slice: index.html line 33; L01.html line 51; L02.html lines 125, 466, 510; L03.html lines 69, 93, 280, 333, 376, 378, 385 (12 single-line in-place substitutions). tests/labs/E4/lab-E4-L0[123]-1.py unchanged since 9a02b1a (L02 twin unchanged since 9a02b1a).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE5-E4-a (detached at 7376a5e; .venv symlinked)",
    "scratch": "/tmp only for twin runs (cwd /tmp, python -I -W error). Scripts and logs under ledgers/E4/scripts/E4-a-r5/.",
    "verified_at": "2026-11-04T16:41:40+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Whole slice read line by line this round: index.html (173 lines), L01.html (524), L02.html (576 with head and tail), L03.html (520 incl. head/tail), and the three twins. Every hunk of the round-5 delta was read and re-derived.",
        "Round-4 FAIL rows E4a-r4-def33-hypothesis, E4a-r4-gg-undefined and E4a-r4-P2-only-scope are fixed in the text and re-verified PASS.",
        "Single new FAIL: E4a-r5-hub-kkt-unused (hub prerequisite claim that E4 uses the KKT conditions; no E4 page uses them).",
        "Not a row (observation): e is used both for the Arrow-Debreu security e_s (L01 Def 1.3) and for endowments e^i (L02 onward). Neither is a registered symbol; L03 line 105 restates e_s. A reader could confuse e^i_s with e_s; a lesson-level note would remove the risk.",
        "Not a row (observation): the hub lede (line 33) and index card text name 'noise traders' and 'Arrow-Debreu securities' before their lesson definitions. This is overview naming, consistent with the round-4 judgement.",
        "Not a row (observation): L03 why-it-matters is exactly 120 words, at the limit of BUILDER_RULES 4.2 item 1.",
        "Mutants: none. Slice a has no grader (the lab twins are demonstrations under the ruling; no lab was graded as a mutation target).",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants_killed": 0,
        "mutants": 0,
    },
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", OUT, fragment["summary"])
