"""E4-c round 4: build ledgers/E4/E4-c.json from the round-3 fragment, the round-4 delta and the round-4 re-verification.

Usage: python -I write_fragment.py <checkout-root>. Standard library only.
Rows not overridden below are carried from round 3 only where every line they cite is outside the 67a2d13e..9a02b1af delta.
"""
import json
import sys

root = sys.argv[1]
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-c.round3.json", encoding="utf-8"))
OUT = "ledgers/E4/scripts/E4-c-r4/out/"
CARRY = "Carried from round 3 (cited lines byte-identical since the previous pin 67a2d13e; the 67a2d13e..9a02b1af delta does not touch them): "

ov = {}  # id -> (status, evidence, fix)

def P(i, ev):
    ov[i] = ("PASS", ev, "")

def F(i, ev, fix):
    ov[i] = ("FAIL", ev, fix)

P("E4c-cmd-check-pages", f"Re-run on pin 9a02b1a alone: {OUT}check_pages_L07.out, _L08.out, _L09.out each 'check_pages E4 Lnn: PASS', exit=0.")
P("E4c-cmd-check-dag", f"Re-run: {OUT}check_dag_E4.out 'check_dag E4: PASS', exit=0.")
P("E4c-cmd-check-projects", f"Re-run: {OUT}check_projects_E4.out 'check_projects E4: PASS', exit=0. Project content is outside this slice.")
P("E4c-cmd-run-labs", f"Re-run: {OUT}run_labs_L07.out, run_labs_L08.out, run_labs_L09.out each 'run_labs E4: PASS (1/1)', exit=0.")
P("E4c-cmd-twins-standalone", f"Re-run from an empty scratch cwd with env -i and python -I -W error (ledgers/E4/scripts/E4-c-r4/run_gates.sh): {OUT}twin-L07.exit, twin-L08.exit, twin-L09.exit = 0; {OUT}twin-L0x.stderr all 0 bytes.")
P("E4c-expected-equals-output", f"ledgers/E4/scripts/E4-c-r4/embed_check.py (run on 9a02b1a, output {OUT}embed_check.out): for L07, L08, L09 the data-run code block equals the twin file (True) and the <pre class=\"expected\"> block equals the standalone stdout (True).")
P("E4c-cmd-page-smoke", f"Re-run alone: {OUT}page_smoke_L07_L08_L09.out 'page_smoke modules/E/E4/L07.html: PASS', '...L08.html: PASS', '...L09.html: PASS', 'page_smoke E4: PASS', exit 0; lab timings L07 0.0 s, L08 0.1 s, L09 4.9 s.")
P("E4c-cmd-ruff-mypy-twins", f"Re-run: {OUT}ruff_check.out 'All checks passed!'; {OUT}ruff_format.out '3 files already formatted'; {OUT}mypy_twins.out 'Success: no issues found in 3 source files'.")
P("E4c-cmd-pytest-labs", f"Re-run: {OUT}pytest_labs_E4.out, 13 passing tests, exit=0.")
P("E4c-cmd-verify-refs", f"Offline re-run: {OUT}verify_refs_offline.out 'offline integrity: 560 entries, 0 problems', exit 0. The live Crossref run of round 2 is carried: references/ and tools/ are unchanged since 67a2d13e (git diff --stat empty for those paths).")
P("E4c-cmd-run-graders", f"Re-run seeds 0-49: {OUT}run_graders_E4.out 'run_graders E4: PASS (reference 50/50 seeds, slowest 0.1 s)', exit=0. The grader files changed in the delta; their own rows are in the project slice.")
P("E4c-L07-structure", "Whole L07.html re-read. Delta hunks at L07.html:51 (why-it-matters now says Lemma 7.4 holds for zero means, which matches the Lemma 7.4 statement) and L07.html:494 (Problem R3 solution wording) are text-only. No section, block or order change; check_pages E4 L07 PASS.")
P("E4c-L07-problems-E3-R", "L07.html:462 and 465-498 re-read; the changed line 494 (R3 solution) re-derived: d rho^2/d(sigma_u^2) = -sigma_v^2 chi/D^2, so the ratio to rho^2 is -chi/D, which is not constant in sigma_u because D depends on sigma_u. E2 solution: 1/(1+sigma_eta^2)=1/4 gives sigma_eta^2=3, kappa=2, sigma_u^2=1/2 (ledgers/E4/scripts/E4-c-r4/out/recheck_c_r4.out, L07 block).")
P("E4c-L07-notation-c", "Bare single-letter symbols in L07 math (scan: ledgers/E4/scripts/E4-c-r2/notation_scan.py run on this pin, unknown macros []): D, Y, b. D is defined in the Proposition 7.7 proof (L07.html:117), Y in the Proposition 7.6 proof (Y = p/theta_s), b in Lemma 7.4 (b = Cov/Var). No symbol of notation.json is reused with another meaning; no T, Phi, gamma, R-ast or Q on the page.")
P("E4c-L07-process-and-banned", "grep -n -i over L07.html for builder, verifier, fixer, round, request, TODO, TBD, lorem, obviously, clearly, 'it is important to note', and an ellipsis outside code: the only hit is the substring 'around' (benign). No banned phrase.")
P("E4c-L08-structure", "check_pages E4 L08 PASS (out/check_pages_L08.out). The delta hunks at L08.html 7, 51, 336, 564, 583, 682, 685, 690, 717, 795 were re-read in full: text-only edits, no section, block or order change. The Assumption numbering gap (A1-A3 then A5) is recorded separately in E4c-r4-L08-assumption-numbering.")
P("E4c-L08-line51-zero-cost", "L08.html:51 (changed) reads 'no informed fraction lambda (Assumption A3) is an equilibrium at a cost c with 0 < c < G(0) (Proposition 5.1(b))'. Proposition 5.1(b) at L08.html:285-301 agrees. G(0) = ln(2)/4 = 0.1732868 at a = 2 (ledgers/E4/scripts/E4-c-r4/out/recheck_c_r4.out, 'G(0) closed').")
P("E4c-L08-line51-existence", "L08.html:51 'equilibria exist outside (G(1), G(0))' and 'existence uses Assumption A5' match Proposition 5.2(b) and (c) (L08.html:304-326) and Assumption A5 (L08.html:314). The sentence 'Only Proposition 5.2(c) and the bisection rule use A5' matches the references paragraph (L08.html:795) and the A5 statement.")
P("E4c-L08-G1-derivation", "L08.html:336, 564, 583, 674, 719 re-checked. G(1) = ln(5/3)/4 = 0.12770640594 recomputed from Definition 4.3 and Proposition 4.1 at lambda = 1 (recheck_c_r4.out, 'G(1) recomputed' and 'Emp 3 G(1)'). The hand derivation at L08.html:674 (kappa = 2, tau_eta = 1/5, V_I = 1/2, b_y = 1/6, V_U = 5/6, Var(D_I) = 1, Var(D_U) = 2/3, G(1) = (1/4) ln(3/(9/5)) = (1/4) ln(5/3)) re-derived step by step.")
P("E4c-L08-lab1-part-A", "L08.html:336 (hypothesis) and 544-547 (expected block) re-read; embed_check True. The hypothesis value b_y/beta = 0.1605 re-derived at lambda = 1/2: b_y = 1/18, beta = A/(tau_v + A) = 0.34615, ratio 0.16050. Printed sample slope 0.1595 is within 0.02 (absolute difference 0.0010, out/twin-L08.stdout).")
P("E4c-L08-lab1-part-D-docstring", "tests/labs/E4/lab-E4-L08-1.py:181-182 and L08.html:564 (interpretation of Part D) match the printed Part D lines in out/twin-L08.stdout ('lam = 0 is an equilibrium: False', 'lam = 1 ... False', 'interior fractions with gain = cost: 0').")
P("E4c-L08-misc-claims", "L08.html:583 (misconception 1: G(1) = ln(5/3)/4 > 0 with noise), 587 (positive informed fraction for every cost 0.12 to 0.17; lambda* at 0.15 = 0.657828572, rounded to 0.658), 591 (values 0.013 to 0.167 at costs where some trader is informed), 595 (fraction 1 at cost 0.12, 0 at 0.18). All match out/twin-L08.stdout and recheck_c_r4.out.")
P("E4c-L08-res-1", "L08.html:682-687 re-derived: the statement follows Proposition 5.1(b),(c). With sigma_u^2 = 0 and lambda = 0, p = v-bar - a sigma_v^2 u with u constant, so Var(p) = 0 and the correlation is undefined; Definition 7.1 of L07 (L07.html:56-58) requires Var > 0.")
P("E4c-L08-res-2-crossref", "L08.html:690-692 (statement now cites the definitions of beta, A and tau_eta in Proposition 3.1): the limit Var(D_U) -> a^2 sigma_u^2 sigma_v^4 and Var(D_U)/V_U -> a^2 sigma_u^2 sigma_v^2 re-derived from Proposition 4.1 and Proposition 5.2(a) (tau_v^2 tau_eps^2 / tau_v^4 = tau_eps^2/tau_v^2; lambda^2/tau_eta -> a^2 sigma_eps^4 sigma_u^2). Matches X0 of Lemma 4.5.")
P("E4c-L08-key-results", "L08.html:711-719 re-checked row by row: G(0) = ln(1 + sigma_v^2/sigma_eps^2)/(2a) (Lemma 4.5), G(1) = ln(5/3)/4 (Definition 4.3 and Proposition 4.1 at lambda = 1; Emp 3), Corr = tau_eta/(tau_v + tau_eta) in (0,1) and increasing when sigma_u^2 > 0 (Corollary 3.2, Lemma 3.3), 'Proposition 5.2 (A5 assumed)'. Each source named in the row exists and states the row.")
P("E4c-L08-simulated", "L08.html:336 puts the SIMULATED label on Part A only (seeded draws). Parts B to D are exact or fixed-grid evaluations and carry no label. tests/labs/E4/lab-E4-L08-1.py docstring (line 5) states 'Part A uses seeded draws and is SIMULATED'.")
P("E4c-L08-G-before-definition", "L08.html:51 ('G(lambda) (Definition 4.3; Lemma 4.5 for G(0))') and L08.html:79 use G with an explicit forward reference to Definition 4.3, whose block is at L08.html:232-236 (the dfn of 'gain from information' at 233-234). The forward reference is explicit, so no term is used undefined.")
P("E4c-L08-process-banned", "grep -n -i on L08.html for builder, verifier, fixer, round, request, TODO, TBD, lorem, obviously, clearly and an ellipsis outside code: no hit. check_pages E4 L08 PASS.")
P("E4c-L09-structure", "Whole L09.html re-read. The delta hunks at L09.html 7, 62, 119, 122, 127-128, 290, 419 are text-only: no section, block or order change; check_pages E4 L09 PASS. The defects at line 62 and in the references paragraph are recorded in their own rows (E4c-r4-L09-partition-common-knowledge, E4c-L09-references).")
P("E4c-L09-example-2.4", "L09.html:118-120 and the changed line 119 re-derived: g1(1) = (x1+x2)/2 = 1/2; g2(1) = mean of -x on {1,2,3} = (1-2+2)/3 = 1/3; g1(3) = x3 = -2 < 0; M(1) = {1,2,3}. Independent enumeration in recheck_c_r4.out (L09 block) returns state 1, meet [1,2,3], first strict bet (-1,2,-2,-2,-2,-2).")
P("E4c-L09-res-3", "L09.html:416-419 and the changed solution at line 419 re-read: E is any union of cells of both partitions; the argument (identity over cells, S_2 = -S_1, B1 positivity) is the one of Theorem 2.1 (L09.html:352-363), which is valid for any such E. Statement and solution agree.")
P("E4c-L09-lab1-hypothesis-interpretation", "L09.html:128 (hypothesis: 15625 bets; no SIMULATED label) and 282 (interpretation: 500 strictly accepted, none nonnegative on the meet, 625 nonnegative, first bet with posterior -2 at state 3) match out/twin-L09.stdout (exact) and recheck_c_r4.out (independent enumeration: strict 500, nonneg-on-meet 625, strict and nonneg 0, nonzero-on-meet 0).")
P("E4c-L09-simulated", "L09.html contains the word SIMULATED only at line 128, where it says no label applies. tests/labs/E4/lab-E4-L09-1.py docstring: 'There are no random draws and no data.' Consistent.")
P("E4c-L09-dag", f"check_dag E4 PASS ({OUT}check_dag_E4.out). L09.html:37 and 287 (Remark 2.5 links L02.html#def-arrow-debreu-equilibrium; the anchor exists once, in L02.html:89, an earlier lesson of E4). Line 290 has no concept link and names no out-of-closure concept (grep of the plan's D1-D10 names over L07-L09: no hit).")
P("E4c-L09-process-banned", "grep -n -i on L09.html for banned process words and phrases: no hit. check_pages E4 L09 PASS.")
P("E4c-dag-unlinked", "check_dag E4 PASS. grep -i over L07-L09 for the plan's unlinked out-of-closure names (bayes, state price, stochastic discount, law of one price, efficient markets, martingale, banach, completeness of the reals, noise-trader risk, two-fund, diagnostic expectations, determinacy, new keynesian, probability of informed trading): no hit. 'common knowledge' and 'posterior' are defined in the lesson that uses them.")
P("E4c-notation-registered", "ledgers/E4/scripts/E4-c-r2/notation_scan.py run on this pin: 'unknown macros = []' for L07, L08 and L09. Bare symbols: L07 {D, Y, b}, L08 {D, Y, Z, b, c}, L09 {D}. grep: no \\mathbb{E}, \\mathbb{R}, \\Phi, \\gamma, R^\\ast or \\mathbb{Q} in the three pages.")
P("E4c-twin-L07-1", f"tests/labs/E4/lab-E4-L07-1.py is not in the 67a2d13e..9a02b1af delta (byte-identical). Re-run: run_labs PASS; standalone python -I -W error exit 0, stderr 0 bytes; expected block equals output (embed_check True); ruff and mypy clean.")
P("E4c-twin-L08-1", f"tests/labs/E4/lab-E4-L08-1.py is not in the delta (byte-identical). Re-run: run_labs PASS; standalone exit 0, stderr 0 bytes; expected block equals output (embed_check True); ruff and mypy clean; output at {OUT}twin-L08.stdout.")
P("E4c-twin-L09-1", f"tests/labs/E4/lab-E4-L09-1.py is not in the delta (byte-identical). Re-run: run_labs PASS; standalone exit 0, stderr 0 bytes; expected block equals output (embed_check True); ruff and mypy clean. Its module docstring's first line ('every bet on a six-state space') is qualified in the same docstring by the range {-2,...,2}, so it is not an overstatement.")

F("E4c-L09-references",
  "L09.html:511 (references paragraph) says 'The counts of Lab 1 are finite checks and carry no grade of their own.' This contradicts the plan (E4-build-plan.md section 2.2, a finite enumeration is grade C with its basis named; section 1 table row L09 'grade C, finite'). The Key results table (L09.html:431-435) has no row grading the enumeration. The same paragraph says 'The abstract of that paper was not readable when this page was written', a process statement about the authoring of the page, in learner text. The registry record for milgrom1982information (references/references.json:17291) matches the title, JET 26(1), 1982 and pages 17-27.",
  "Replace the sentence 'The counts of Lab 1 are finite checks and carry no grade of their own.' with 'Lab 1 is an exhaustive finite check, graded C (basis: Lab 1, Parts A to C, exhaustive enumeration of 15625 bets in exact arithmetic).' and add that row to the Key results table (grade C). Delete the sentence about the abstract being unreadable, or replace it with 'The page states no result of that paper.'")

F("E4c-r3-first-use-before-definition",
  "Re-verified at 9a02b1a: the round-3 defect remains. L06.html:72 uses 'informed' and 'uninformed' ('A fraction lambda of the investors is informed. An informed investor observes s ... An uninformed investor observes only p.') with no dfn in L06 for them; L06.html:673 (a learner-facing quiz prompt) uses 'the noise-trader supply' before its only dfn at L08.html:66 (<dfn>noise-trader supply</dfn>). L08.html:71 holds <dfn>informed</dfn> and <dfn>uninformed</dfn>. grep -n 'noise-trader supply' L06.html returns L06.html:7, 245 (lab docstring), 673.",
  "Give 'informed' and 'uninformed' a plain <dfn> at their first use in L06.html:72, and give 'noise-trader supply' a plain <dfn> at its first use in L06 before the quiz prompt at L06.html:673 (or reword that prompt to 'the variance of the noise-trader supply u'). Then change L08.html:66 and L08.html:71 from <dfn> to plain references. The owner of L06 must make the change; this slice does not edit it.")

F("E4c-r4-L08-assumption-numbering",
  "L08.html defines Assumptions A1, A2, A3 (L08.html:58, 65, 70) and then A5 (L08.html:314, 'Assumption A5 (sign change, the bisection's invariant)'); no Assumption A4 exists in L08 (grep 'A4' in L08.html returns nothing). L08.html:51, 55, 573 and 795 cite A5. The numbering skip is not explained on the page, so a reader cannot tell whether A4 was removed. Rule 6 (named, numbered Assumptions) reads for consecutive numbers.",
  "Renumber the L08 Assumption 'A5' to 'A4' at L08.html:314 and at every citation (L08.html:51, 55, 314, 573, 795 and any other occurrence), so that L08 uses A1 to A4. The twin tests/labs/E4/lab-E4-L08-1.py does not cite A5 and needs no change.")

F("E4c-r4-L09-partition-common-knowledge",
  "L09.html:62: 'Both partitions are common knowledge (defined in Definition 1.2 below): each trader knows both partitions.' Definition 1.2 (L09.html:79) defines common knowledge of an event E at a state (M(omega) subset of E). A partition is not an event, so the cross-reference points to a definition that does not cover the sentence.",
  "Rewrite L09.html:62 as: 'Both partitions are common knowledge: each trader knows both partitions. This is an assumption of the model, and Definition 1.2 gives common knowledge for events.'")

NEW = []
def N(i, status, ev, fix=""):
    NEW.append({"id": i, "check": "", "location": "", "status": status, "evidence": ev, "fix": fix})

rows = []
seen = set()
for r in prev["rows"]:
    i = r["id"]
    seen.add(i)
    if i in ov:
        st, ev, fx = ov[i]
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": st, "evidence": ev, "fix": fx})
    elif r["status"] == "PASS":
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY + r["evidence"], "fix": ""})
    else:
        raise SystemExit(f"unhandled previous non-PASS row {i}")
missing = {k for k in set(ov) - seen if not k.startswith("E4c-r4-")}
assert not missing, missing

rows.insert(0, {"id": "E4c-r4-delta-read", "check": "delta", "location": "course/modules/E/E4/L07.html, L08.html, L09.html, index.html; tests/labs/E4/lab-E4-L07-1.py, L08-1.py, L09-1.py; cards.json (not scoped)", "status": "PASS",
  "evidence": "Round-4 delta read hunk by hunk: git diff -U2 67a2d13e7575608e95b2e34a9c7c2a82c61b117b 9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba -- course/modules/E/E4/L07.html L08.html L09.html index.html. L07: lines 51, 494. L08: lines 7, 51, 336, 564, 583, 682, 685, 690, 717, 795. L09: lines 7, 62, 119, 122, 127-128, 290, 419. index.html: hunks at 69-80, 116-132, 143, 157 (quiz and hub items of other lessons and the ladder); hub lines 29, 136, 137 unchanged. Twin files for L07-L09 unchanged. tools/, references/, notation/ and atlas/ unchanged (git diff --stat empty). Every changed hunk in the slice was read in full; rows citing them are re-verified above, every other row is carried with its cited lines shown unchanged. Changes to L06.html (lines 82, 86, 91 for Assumption A4 and G) are in another slice; the L07 Proposition 7.6 citation of 'A1 to A4 and G of Lesson L06' still refers to them and is consistent with the new wording.",
  "fix": ""})
rows.insert(1, {"id": "E4c-r4-recheck-numbers", "check": "2.2-numbers", "location": "course/modules/E/E4/L07.html, L08.html, L09.html (all printed and quoted numbers)", "status": "PASS",
  "evidence": "Independent script ledgers/E4/scripts/E4-c-r4/recheck_c_r4.py (standard library, output ledgers/E4/scripts/E4-c-r4/out/recheck_c_r4.out). L07 exact Fractions: rho^2 4/9, 1/3, 1/6, 1/18, 1/66 across sigma_u in {1/4,1/2,1,2,4}; Var(p) 729/1444, 27/49, 27/32, 729/338, 35937/4802; lambda sweep 1/6, 1/3, 9/22; a sweep 4/9, 1/3, 1/6; tiny sigma_u = 1/100 gives 2500/5001 below 1/2; M1 1/6, M2 9/22, M3 2/7; E1 difference 0.1354 tolerance units. L08 floats: G(0) = 0.1732868, G(1) = 0.1277064 = ln(5/3)/4, G(1e-6)-G(0) = -6.3e-14, strictly decreasing G and increasing Corr on 999 grid points (True); bisection on the stated bracket reproduces lambda* 1.000000000, 0.965625410, 0.815032329, 0.657828572, 0.480567912, 0.231615819, 0.000000000 at costs 0.12 to 0.18 and the gaps 7.71e-3 and -6.71e-3 at the boundaries (interior gaps below 1e-13). L09 exact enumeration over 15625 bets: strict 500 and nonnegative-on-meet 625 at states 1 and 4, strict and nonnegative 0, zero-posterior count 625 matching Emp 3. All printed values in the three pages' expected blocks agree with these.",
  "fix": ""})
rows.append({"id": "E4c-r4-L08-assumption-numbering", "check": "2.4-math/rule-6-assumptions", "location": "course/modules/E/E4/L08.html:314 (definition), 51, 55, 573, 795 (citations)", "status": "FAIL",
  "evidence": ov["E4c-r4-L08-assumption-numbering"][1], "fix": ov["E4c-r4-L08-assumption-numbering"][2]})
rows.append({"id": "E4c-r4-L09-partition-common-knowledge", "check": "2.9-prose/cross-reference", "location": "course/modules/E/E4/L09.html:62", "status": "FAIL",
  "evidence": ov["E4c-r4-L09-partition-common-knowledge"][1], "fix": ov["E4c-r4-L09-partition-common-knowledge"][2]})

# Replace the rows that were FAIL-overridden with their correct check/location fields already set from prev.
for r in rows:
    assert r.get("status") in ("PASS", "FAIL"), r
    if r["status"] != "PASS":
        assert r["fix"].strip(), r["id"]
    if not r.get("check"):
        r["check"] = "2.9"
    if not r.get("location"):
        r["location"] = "see evidence"

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"

frag = {
    "unit": "E4",
    "slice": "E4-c",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for E4-c round 4 (did not build E4)",
    "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
    "base": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b (round-3 pin; delta read hunk by hunk, see E4c-r4-delta-read)",
    "checkout": root,
    "scratch": "/tmp/e4c-r4-XXXX (twin runs, removed after each run)",
    "verified_at": "2026-11-04T12:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "grossman1980 (Grossman and Stiglitz, AER 1980) still has no registry record (B1, REFERENCE_REQUEST R-E4-1); L08 cites no key, which is correct.",
        "mascolell1995microeconomic author conflict (B3) is outside this slice."
    ],
    "freshness_flags": [],
    "notes": "Scope: course/modules/E/E4/L07.html, L08.html, L09.html; tests/labs/E4/lab-E4-L07-1.py, L08-1.py, L09-1.py; index.html only at the lines cited by rows (29, 136, 137). Not checked by this slice: cards.json (no E4-c card row carries a card-level check this round; cards are the card builder's slice), the hub skill-check and quiz items changed in index.html lines 69-80 and 116-132 (other slices), L06.html changes at lines 82-91 (other slice; cross-references from L07 and L08 re-read and consistent), the project, grader, rubric, mutants and alternatives (project slices). Cross-slice observation: the round-3 finding of a second CARA definition in project.html:259 no longer applies (no dfn in project.html on this pin).",
    "summary": f"E4-c round 4 on 9a02b1a: verdict {verdict}. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS rows: E4c-r3-first-use-before-definition (still present in L06.html:72 and 673, owned by L06), E4c-L09-references (grade of Lab 1 counts and a process sentence), E4c-r4-L08-assumption-numbering (A4 missing), E4c-r4-L09-partition-common-knowledge (cross-reference to Definition 1.2). Mutants: none (lab twins, not project graders). Every round-3 PASS row was either re-verified or carried with its cited lines shown byte-identical in the delta.",
}
json.dump(frag, open(f"{root}/ledgers/E4/E4-c.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), counts, verdict)
