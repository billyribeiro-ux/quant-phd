"""Round 7, CF1-b: writes ledgers/CF1/CF1-b.json from the round-6 fragment (context) and this round's evidence."""
import json, sys
from datetime import UTC, datetime

PREV = "/tmp/fanout-frags/CF1-b.round6.json"
OUT = sys.argv[1]
prev = json.load(open(PREV, encoding="utf-8"))
prev_rows = {r["id"]: r for r in prev["rows"]}
CHANGED = "L03 l.67, L04 l.7, l.118, l.300, l.456 and cards basis fields only"
PREFIX = "Carried from round 6 ({files} byte-identical since the previous pin d57df1e at the cited lines; round-7 changes are " + CHANGED + "): "

def carry(rid, files):
    old = prev_rows[rid]
    assert old["status"] == "PASS", rid
    body = old["evidence"]
    if body.startswith("Carried from round"):
        body = body.split("): ", 1)[1]
    return {"id": rid, "check": old["check"], "location": old["location"], "status": "PASS",
            "evidence": PREFIX.format(files=files) + body}

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = []
A = rows.append

# ---- commands and tools, re-run this round
A(row("CF1-b-cmd-check-pages", "2.9-structure", "tools/check_pages.py", "PASS",
      "Run at de53f7e: `.venv/bin/python tools/check_pages.py --all` printed 'check_pages CF1: PASS' (also M1, S7, AC1, AC2, AC4, AP1 PASS); exit 0."))
A(row("CF1-b-cmd-check-dag", "DAG/concepts", "tools/check_dag.py", "PASS",
      "Run at de53f7e: `.venv/bin/python tools/check_dag.py --all` printed 'check_dag CF1: PASS' (all units PASS); exit 0."))
A(row("CF1-b-cmd-run-labs", "2.5-labs", "tools/run_labs.py --unit CF1", "PASS",
      "Run at de53f7e: 'run_labs CF1: PASS (9/9)'; exit 0."))
A(row("CF1-b-lab-twin-direct", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py, tests/labs/CF1/lab-CF1-L04-1.py", "PASS",
      "`.venv/bin/python -I -W error` on each twin: exit 0, empty stderr (ledgers/CF1/scripts/CF1-b-r7/ outputs in /tmp/cf1-v/CF1-b-r7/). Script ledgers/CF1/scripts/CF1-b-r7/embed_and_cards_check.py (run with /usr/bin/python3 -I; stdlib only): embedded code equals the twin (stripped) for both pages, and each 'expected' block equals the twin's stdout exactly."))
A(row("CF1-b-lab-twin-lint", "2.5-labs", "tests/labs/CF1/lab-CF1-L03-1.py, tests/labs/CF1/lab-CF1-L04-1.py", "PASS",
      "`.venv/bin/ruff check` on both twins: 'All checks passed!'; `ruff format --check`: '2 files already formatted'; `.venv/bin/mypy --no-incremental` on both: 'Success: no issues found in 2 source files'."))
A(row("CF1-b-lab-L03-1", "2.5-labs", "course/modules/CF/CF1/L03.html l.122-126, l.123 hypothesis, l.242 interpretation; tests/labs/CF1/lab-CF1-L03-1.py", "PASS",
      "Read in full. Hypothesis l.123: nominal rate 0.0918, consistency equality, mixed overstates and understates, grid of 12 pairs, no random numbers: each matches the output (nominal rate 0.091800; both consistent NPVs 263709.14; mixed 377346.63 and 161465.80; grid 4 x 3 = 12 cases, largest gap 0.000000). Interpretation l.242: 'the first two NPV lines are equal' and 'zero at 0.00 inflation, as Theorem 2.3 states' (table 0.00 gives 0.00; the gap rises 36913.22, 113637.49, 194368.27) match the output; the 'Lab does not show' sentence is a scope limit the code supports (inputs written in code). Output in /tmp/cf1-v/CF1-b-r7/lab-CF1-L03-1.out."))
A(row("CF1-b-lab-L04-1", "2.5-labs", "course/modules/CF/CF1/L04.html l.143-145, l.146-299 (lab), l.299-300 interpretation; tests/labs/CF1/lab-CF1-L04-1.py", "PASS",
      "Read in full. Embedded code equals the twin; expected block equals the twin's stdout exactly (script above). Interpretation l.300 (changed this round): profile signs '-' at 0.00 and 0.05, '0' at 0.10, '+' at 0.15, '0' at 0.20, '-' at 0.25 and 0.30 match the printed sign column; 'two sign changes, bisected to 0.100000 and 0.200000' matches the printed roots; 'largest gap ... over six test rates, prints as 0.000000 cents': the lab's gap tuple (-0.4, 0.0, 0.05, 0.15, 0.5, 2.0) has six entries and prints 0.000000; crossover 0.200000 and the ranking table match. The grid step 0.0001 in l.118 matches GRID_STEP in the twin. Hypothesis l.145 matches the output. Output /tmp/cf1-v/CF1-b-r7/lab-CF1-L04-1.out; independent Fraction recomputation in ledgers/CF1/scripts/CF1-b-r7/recompute_delta.py."))
A(row("CF1-b-lab-L03-E2-claim", "2.5-labs", "course/modules/CF/CF1/L03.html E2 solution (l.339-342)", "PASS",
      "Re-run this round on a copy with INFLATION = 0.00 (ledgers/CF1/scripts/CF1-b-r7/lab_copy_claims.sh): 'mixed minus real, cents: 0.00'; 'NPV real flows at nominal rate (mixed): 263709.14 USD' equal to the real NPV; table row 0.00 prints 0.00. The solution's claims hold."))
A(row("CF1-b-lab-L03-E3-claim", "2.5-labs", "course/modules/CF/CF1/L03.html E3 solution (l.346-348)", "PASS",
      "Re-run this round on a copy with REAL_RATE = 0.10 (same script): 'real rate 0.100000, inflation 0.030000, nominal rate 0.133000' (solution: 1.10 x 1.03 - 1 = 0.133); 'largest absolute gap, consistent minus real, cents: 0.000000'. The real NPV changes (137236.03 USD), as the solution says the student should check."))
A(row("CF1-b-numbers-L03", "2.2-numbers", "course/modules/CF/CF1/L03.html Example 1.4 (l.79), Example 2.5 (l.118), Sec 3 (l.248), misconceptions (l.257, l.261, l.265, l.269), M1-M3 (l.282-298), P3 (l.323), E1 (l.332-334), E3 (l.346-348), R2 (l.366), R3 (l.373), key results (l.385-391)", "PASS",
      "Re-derived this round (ledgers/CF1/scripts/CF1-b-r7/recompute_delta.py): Ex 1.4 0.0918, additive 0.09, gap 0.0018; Ex 2.5 nominal NPV 257.70969 (257.71), real rate 0.048544; l.248 two-line example 205 x 1.05 / 200 - 1 = 0.07625 and implied inflation 0.025; E1 shares 73.7 / 14.0 / 43.1 per cent (0.73706, 0.13998, 0.43092); R2 ratio 2.06; R3 b = 1.06/2.03 = 0.522167; P3 sqrt(0.005) = 0.070711; M1 gap 0.001; M2 1061.208; M3 94.545. Lab-printed values (263,709.14; 113,637.49; 161,465.80; 194,368.27) match the output file."))
A(row("CF1-b-numbers-L04", "2.2-numbers", "course/modules/CF/CF1/L04.html Example 3.2 (l.101-103), Prop 3.3 (l.109-110), Example 4.2 (l.135), Remark 5.1 (l.307), R1-R3 (l.424, l.431, l.436-438), misconceptions (l.322-334), E2 (l.406), E3 (l.413), M2 (l.356), quiz (l.474-535)", "PASS",
      "Re-derived with Fractions (recompute_delta.py): P NPV at 0, 5, 10, 15, 20, 25, 30 per cent = -2000.00, -680.27, 0.00, 189.04, 0.00, -480.00, -1183.43; factorization equals direct NPV at the six test rates; Ex 4.2 NPVs 18181.82 and 27272.73 at 10 per cent, 8333.33 each at 20 per cent; crossover (1e7 and 1.2e7 cents) at 0.2; M2 x = 0.884437, r = 0.130662; R1 NPV at 10 per cent 0.322314, IRRs 0 and 400 per cent; R2 IRR_A = sqrt(3) - 1 = 0.732051, NPV_A 147.93, NPV_B 81.82; R3 FV 250.00 and -750.00; E2 (A = -100k, +120k): IRR_A 20 per cent, crossover 0.30, NPV_A -11111.11 and NPV_B -14814.81 at 35 per cent, disagreement above 30 per cent; E3 -680.27; quiz 189.04, 0.21, 13.07, 0.2, 0."))
A(row("CF1-b-notation-other-symbols", "2.4-notation", "course/modules/CF/CF1/L03.html, L04.html", "PASS",
      "Whole files re-read this round. The delta adds no new symbol: L03 l.67 and L04 l.7, l.118, l.300, l.456 use only the registered or local symbols already in the page (n, r, pi, N, NPV, IRR, A, B, P); the Delta K and Delta C of the Theorem 4.1 summary row are not in the delta (l.454 unchanged). notation/notation.json consulted for N (local, defined at L04 Definition 1.1 l.57)."))
A(row("CF1-b-notation", "2.4-notation", "course/modules/CF/CF1/L04.html Definition 1.1 (l.57), Theorem 1.3 (l.67), Remark 5.1 (l.307), R3 (l.436), quiz (l.533)", "PASS",
      prev_rows["CF1-b-notation"]["evidence"].replace("Carried from round 5 (", "Carried from round 6 (").replace("byte-identical since the previous pin 00745fe", "byte-identical since the previous pin d57df1e")))
A(row("CF1-b-prose-banned-scan", "2.9-structure", "course/modules/CF/CF1/L03.html, course/modules/CF/CF1/L04.html (full files)", "PASS",
      "/usr/bin/grep -i over both full files for roughly, historically, half, about, percentages, ellipses, builder, verifier, round, requests, unit report, build, simply, clearly, obviously, typically, generally, usually, most, always, only, every, same, drives, offsets, raises, as much as, single, all: every hit read. Changed sentences: L03 l.67 ('algebraic identity'), L04 l.7 ('single example'), l.118, l.300, l.456 contain no banned phrase ('half a point' in the L03 P3 title is not 'roughly half'). Scope words in the changed sentences are checked in the rows for those lines."))
A(row("CF1-b-structure-L03", "2.9-structure", "course/modules/CF/CF1/L03.html", "PASS",
      "check_pages CF1 PASS at de53f7e; full read of L03: eyebrow, heading, lab, section order, quiz (L03q1-q9 in lesson order), references block and lesson-nav present."))
A(row("CF1-b-structure-L04", "2.9-structure", "course/modules/CF/CF1/L04.html", "PASS",
      "check_pages CF1 PASS at de53f7e; full read of L04: sections 1-11, lab block, quiz (L04q1-q10 with explanations), references block and lesson-nav present; meta description checked in CF1-b-r5-meta-L04-description."))
A(row("CF1-b-dag-concepts-L03-L04", "DAG/concepts", "course/modules/CF/CF1/L03.html, L04.html (dfn ids)", "PASS",
      "check_dag CF1 PASS. dfn ids: L03 def-fisher-relation, def-real-vs-nominal-cash-flows; L04 def-internal-rate-of-return, def-multiple-irr-problem; each defined once. Concepts used (present-value, discount-factor, net-present-value) are defined in the prerequisite units or L01 (meta-row links)."))
A(row("CF1-b-hours-L03-L04", "hours", "course/modules/CF/CF1/L03.html l.2, L04.html l.2, L05, L06, index.html l.29, l.31", "PASS",
      "grep: data-hours=\"8\" on L01 to L06; index data-hours-lessons=\"48\", data-hours-project=\"12\", header 'Tier U · 60 hours'. 6 x 8 = 48; 48 + 12 = 60. Consistent. Pace not failed (architect ruling)."))
A(row("CF1-b-attribution-fisher", "2.3-grades/attribution", "course/modules/CF/CF1/L03.html l.67 and l.476", "PASS",
      "Changed l.67 (re-read): names no author or source; it states only which results depend on constant rates. l.476 says no verified source is cited for the Fisher relation's history or empirical status, and the page cites no registry source (no data-cite in L03). No attribution to read."))
A(row("CF1-b-simulated-label", "2.3-grades", "course/modules/CF/CF1/L03.html l.122, l.123, l.126; course/modules/CF/CF1/L04.html l.101, l.144, l.148, l.456", "PASS",
      "Re-read: L03 l.122 'Lab 1 · One SIMULATED project', l.123 'discounts one SIMULATED project', l.126 'SIMULATED: the project is a fixed input'. L04 l.101 'the SIMULATED project', l.144 'Lab 1 · SIMULATED cash flows', l.148 'SIMULATED: every cash flow is a fixed input'. L04 l.456 is now grade T and is proved on the page (Prop 3.3, Thm 4.1); the lab is cited only as a cross-check, so no lab-read result is graded T."))
A(row("CF1-b-process-words", "2.9-structure", "course/modules/CF/CF1/L03.html, course/modules/CF/CF1/L04.html", "PASS",
      "grep -i for builder, verifier, round, REQUESTS, unit report, build over both full files: no learner-text hits. The changed sentences contain none."))
A(row("CF1-b-quiz-L03q5", "2.4-math", "course/modules/CF/CF1/L03.html quiz item L03q5 (l.430-436)", "PASS",
      "Re-read: answer 'Positive: the NPV is overstated' matches Theorem 2.3 (l.102-105) under the stated hypotheses; explanation (l.436) matches."))
A(row("CF1-b-prose-L03-about43", "2.2-numbers", "course/modules/CF/CF1/L03.html misconception 2 (l.261)", "PASS",
      "113,637.49 / 263,709.14 = 0.43092 -> 43.1 per cent (recomputed); the 0.4309 displayed is consistent with its displayed inputs."))
A(row("CF1-b-prose-L04-superlative", "2.9-structure", "course/modules/CF/CF1/L04.html why-it-matters (l.51) and references (l.542)", "PASS",
      "Re-read in full: no superlative or universal claim beyond the Theorem 2.1 scope; references l.542 says the lesson makes no claim about firm usage."))
A(row("CF1-b-prose-L03-misconception-overstates", "2.2-numbers", "course/modules/CF/CF1/L03.html misconception 2 (l.261) and misconception 3 (l.265); key results l.387-388", "PASS",
      "Misconception 2 'overstates' matches Theorem 2.3 (positive sum, recomputed 113,637.49); misconception 3 'understates' matches Remark 2.4 and prints 161,465.80 (lab output)."))
A(row("CF1-b-grades-L03", "2.3-grades", "course/modules/CF/CF1/L03.html key results l.385-391; Thm 1.3 (l.70-71), Thm 2.2 (l.90-92), Thm 2.3 (l.102-105), Remark 2.4 (l.112-113)", "PASS",
      "Each T row is a theorem proved on the page; each C row is read off Lab 1 with 'SIMULATED inputs' in its basis (l.390-391). Re-read this round."))
A(row("CF1-b-grades-L04", "2.3-grades", "course/modules/CF/CF1/L04.html key results l.450-457; Thm 1.3 (l.65-68), Thm 2.1 (l.77-79), Cor 2.2 (l.85-86), Prop 3.3 (l.107-110), Thm 4.1 (l.125-127), Remark 5.1 (l.305-307)", "PASS",
      "Re-read this round. Row l.456 (changed: C to T, 'crossover of A and B is 20 per cent'): T is correct because Prop 3.3 gives the sign pattern and the roots, and Theorem 4.1 with Example 4.2 gives r* = 120000/100000 - 1 = 0.20; the lab's 0.200000 is a cross-check only. Row l.455 'Exact arithmetic in Example 4.2': 130/100 - 1 = 30 per cent, 250/200 - 1 = 25 per cent, NPVs recomputed, T is correct for typed inputs. Other T rows match their proofs."))
A(row("CF1-b-math-L03-thm22-23-convergence", "2.4-math", "course/modules/CF/CF1/L03.html Theorem 2.2 (l.90-92), proof (l.95-98), Theorem 2.3 (l.102-105), proof (l.107-108), Remark 2.4 (l.112-113)", "PASS",
      "Byte-identical cited lines; re-read this round. Proofs follow from Definition 1.2 and the term-by-term identity; the Theorem 2.3 claim is strict only where a later real flow is positive, as stated."))
A(row("CF1-b-math-L03-P2", "2.4-math", "course/modules/CF/CF1/L03.html problem P2 (l.312-316)", "PASS",
      "Re-derived: pi/(1+r) for the single inflow at t = 1 is nonzero for pi > 0; the pi = 0 direction needs no sign assumption (every term vanishes). Carried, cited lines unchanged."))
A(row("CF1-b-math-L03-theorems-proofs", "2.4-math", "course/modules/CF/CF1/L03.html Def 1.1-1.2 (l.56-64), Thm 1.3 (l.70-71), Thm 2.2 proof (l.95-98), Thm 2.3 proof (l.107-108), R1 (l.357-359), R2 (l.364-366), R3 (l.371-373), P1 (l.307-309)", "PASS",
      "Re-read this round. R1 price-level cancellation, R2 q = (1+pi)/(1+r) series, R3 b = a(1+r)/(2+pi) all re-derived (recompute_delta.py). Carried, cited lines unchanged."))
A(row("CF1-b-math-L03-sec3-two-line", "2.4-math", "course/modules/CF/CF1/L03.html Section 3 (l.248) and quiz item L03q9 (l.458-464)", "PASS",
      "Re-derived: 205 x 1.05 / 200 - 1 = 0.07625; implied inflation 0.025 (neither line's 0 or 5 per cent). Carried, cited lines unchanged."))
A(row("CF1-b-math-L04-thms", "2.4-math", "course/modules/CF/CF1/L04.html Thm 1.3 (l.65-70), Thm 2.1 (l.77-83), Cor 2.2 (l.85-89), Prop 3.3 (l.107-113), Thm 4.1 (l.125-131)", "PASS",
      "Re-read this round. Theorem 2.1 proof (strict monotonicity, IVT, x <= 1 iff P(1) >= 0) and Theorem 4.1 difference -dK + dC/(1+r) re-derived. Carried, cited lines unchanged."))
A(row("CF1-b-math-L04-R2", "2.4-math", "course/modules/CF/CF1/L04.html problem R2 title and solution (l.428-431)", "PASS",
      "Re-derived: NPV difference (C_B - C_A)/(1+r) > 0; equal outlays of 100, inflows 300 at t = 2 and 200 at t = 1: IRR_A = sqrt(3) - 1, IRR_B = 1, NPV_A 147.93 and NPV_B 81.82 at 10 per cent: NPV ranks A, IRR ranks B. Carried, cited lines unchanged."))
A(row("CF1-b-math-L04-remark51", "2.4-math", "course/modules/CF/CF1/L04.html Remark 5.1 (l.305-307), Section 5 (l.303-309), R3 (l.436-438)", "PASS",
      "Re-derived: at 20 per cent with N = 2, -100000 x 1.44 + 230000 x 1.2 - 132000 = 0 (recomputed). Section 5 is l.303-309 (the round-6 locator correction stands; l.311-316 is Section 6). R3 FV 250.00 and -750.00 recomputed. Carried, cited lines unchanged."))
A(row("CF1-b-prose-L04-why-one-sign-change", "2.4-math", "course/modules/CF/CF1/L04.html why-it-matters (l.51); scope check against Theorem 2.1 (l.79)", "PASS",
      "The why-it-matters sentence states that one outlay followed by non-negative inflows gives a unique IRR, which Theorem 2.1 proves under the hypothesis of l.75; 'more sign changes it can have two values' is a 'can' claim that Example 3.2 witnesses. Carried, line unchanged."))
A(row("CF1-b-term-conventional", "2.9-structure", "course/modules/CF/CF1/L04.html l.73, l.75, l.312", "PASS",
      "Term 'conventional' is defined at l.75 before its use at l.312 ('a basis for a conventional project'); l.73 heading uses no term. Carried, lines unchanged."))
A(row("CF1-b-prose-L04-conventional-def", "2.4-math", "course/modules/CF/CF1/L04.html l.75, l.79", "PASS",
      "Definition at l.75 matches the hypothesis of Theorem 2.1 (l.79): C_0 < 0, C_t >= 0 for t >= 1, C_t > 0 for some t >= 1. Carried, lines unchanged."))
A(row("CF1-b-heading-L04-s2", "2.9-structure", "course/modules/CF/CF1/L04.html Section 2 heading (l.73)", "PASS",
      "Heading 'One outlay, then non-negative inflows, not all zero: exactly one IRR' matches Theorem 2.1 (l.79). Carried, line unchanged."))
A(row("CF1-b-r5-recompute-delta", "2.2-numbers", "ledgers/CF1/scripts/CF1-b-r6/ (absent from this checkout)", "PASS",
      "Superseded. The round-5 script ledgers/CF1/scripts/CF1-b-r5/recompute_delta.py and the round-6 scripts ledgers/CF1/scripts/CF1-b-r6/ are not in this checkout (ledgers/CF1 holds only scripts/CF1-b-r7/ at de53f7e), so they were not re-run. Every printed and displayed value they covered is re-derived this round by ledgers/CF1/scripts/CF1-b-r7/recompute_delta.py and the lab outputs in /tmp/cf1-v/CF1-b-r7/."))
A(row("CF1-b-r5-L03-l87-mixed-discounting", "2.4-math", "course/modules/CF/CF1/L03.html Definition 2.1 (l.86, last sentence)", "PASS",
      "Carried, line unchanged. Sentence defines mixed discounting as discounting nominal flows at the real rate or real flows at the nominal rate, consistent with Theorem 2.3 and Remark 2.4."))
A(row("CF1-b-r5-L04-table-thm41-remark51", "2.3-grades", "course/modules/CF/CF1/L04.html key-results table rows for Theorem 4.1 and Remark 5.1 (l.451-460)", "PASS",
      "Re-verified because row l.456 changed. Rows l.451-455 and 457 unchanged and correct. Row l.456: grade T, 'the crossover of A and B is 20 per cent', proved in Prop 3.3 and Theorem 4.1 with Example 4.2 (recomputed: 0.2); sign pattern -, +, - is Prop 3.3's three intervals (recomputed sign at 0.05, 0.15, 0.25). Row l.457 Remark 5.1 identity re-checked."))
A(row("CF1-b-r5-meta-L04-description", "2.9-structure", "course/modules/CF/CF1/L04.html line 7, meta name=description", "FAIL",
      "New text (de53f7e): '... has exactly one IRR, the single example of a project with two sign changes and two IRRs (Example 3.2), and the mutually exclusive case ...'. The first clause matches Theorem 2.1 (l.79). The uniqueness word 'single' is contradicted inside the page: Problem M3 (l.359-363) is a second project with flows -1, +2.5, -1.5, two sign changes and IRRs 0 and 50 per cent (recomputed: NPV = -(1.5x - 1)(x - 1)), and Problem R1 (l.420-424) is a third, flows -1, +6, -5, IRRs 0 and 400 per cent. The page therefore does not support 'the single example'.",
      "In line 7 replace 'the single example of a project with two sign changes and two IRRs (Example 3.2)' with 'the worked example of a project with two sign changes and two IRRs (Example 3.2)', which names the example without claiming it is the only one. Then re-run check_pages."))
A(row("CF1-b-r5-cards-scope-c037", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c037 front, back and basis", "PASS",
      "Back text unchanged (cites Theorem 2.2, constant rates, finitely many nonzero terms, matching l.90-92). New basis field 'Theorem 2.2, proved in Section 2' matches l.90 in §2 (l.82-99)."))
A(row("CF1-b-cards-L03-finiteness-and-positivity", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c037 (basis changed), CF1-c038 (basis changed), CF1-c044 (basis changed) against L03 Theorem 2.2 (l.90-92), Theorem 2.3 (l.102-105)", "PASS",
      "Texts unchanged; basis fields 'Theorem 2.2, proved in Section 2', 'Theorem 2.3, proved in Section 2', 'Theorem 2.3, proved in Section 2' match the lesson's sections (§2 holds Theorems 2.2 and 2.3). Each card back matches its theorem."))
A(row("CF1-b-cards-L04-one-sign-change", "2.7-cards", "course/modules/CF/CF1/cards.json CF1-c051, CF1-c052 (basis changed), CF1-c058 (basis changed) against L04 Theorem 2.1 (l.79), Corollary 2.2 (l.85-86)", "PASS",
      "Texts unchanged and correct; bases 'Theorem 2.1, proved in Section 2', 'Corollary 2.2, proved in Section 2', 'Corollary 2.2 ...; Proposition 3.3, proved in Section 3' match the lesson sections."))
A(row("CF1-b-cards-L03-L04-other-29", "2.7-cards", "course/modules/CF/CF1/cards.json: CF1-c033 to c036, c039 to c043, c045 to c050, c053 to c061, c088, c091 to c095 (every L03/L04 card)", "PASS",
      "Every L03 and L04 card printed and read against its lesson this round: front and back text unchanged from the previous pin; each new basis field (c036, c039, c040, c043, c050, c053, c054, c055, c057, c058, c059, c060, c061, c092 to c095) matches a result in its own lesson (Theorem, Proposition, Corollary, Remark or Example in the named section). Lab-basis cards (c041, c042, c045, c046, c056) cite Lab 1 SIMULATED, consistent with the lab output figures they quote."))
A(row("CF1-b-cards-duplicate-scan", "2.7-cards", "course/modules/CF/CF1/cards.json", "PASS",
      "ledgers/CF1/scripts/CF1-b-r7/embed_and_cards_check.py: cards 100; duplicate ids none; duplicate fronts none; duplicate backs none. Changed cards are basis-only (script diff of the previous pin: 55 cards, all with a basis field added, front/back/grade/lesson unchanged)."))
A(row("CF1-b-prose-L03-l67-each-theorem", "2.4-math", "course/modules/CF/CF1/L03.html l.67 (changed this round: 'Theorem 1.3 is an algebraic identity between the two rates')", "PASS",
      "Changed sentence: 'This lesson does not settle it, and no result below depends on it, because Theorem 2.2 takes both rates as constant, Theorem 2.3 and Remark 2.4 are stated for one real rate and one inflation rate, and Theorem 1.3 is an algebraic identity between the two rates.' Checked: Theorem 2.2 takes r and pi constant (l.91); Theorem 2.3 is for one pi > 0 and one r > -1 (l.102-103); Remark 2.4 is under Theorem 2.3's assumptions (l.112-113); Theorem 1.3 is n = r + pi + r pi, an algebraic consequence of Definition 1.2 for the given pi (l.70-71, proof l.74) and carries no assumption about stability. The results below that vary the rate (R1, Section 3, R2) are not claimed to hold without constancy. The 'between the two rates' wording is acceptable: pi is held fixed in the identity. 'Algebraic' is what the proof shows (expansion only)."))
A(row("CF1-b-r6-L03-l242-interpretation", "2.2-numbers", "course/modules/CF/CF1/L03.html l.242", "PASS",
      "Carried, cited line unchanged. Checked this round against the output: 'first two NPV lines are equal' and 'zero at 0.00 inflation, as Theorem 2.3 states'."))
A(row("CF1-b-r6-L03-l469-quiz-explain", "2.4-math", "course/modules/CF/CF1/L03.html l.469 (quiz item explain)", "PASS",
      "Carried, cited line unchanged. The printed gap 0.000000 is in the lab output; Theorem 2.2 (l.90-92) is the equality stated."))
A(row("CF1-b-r6-L04-l312-accept-or-reject", "2.4-math", "course/modules/CF/CF1/L04.html l.312 (section 6, first paragraph)", "PASS",
      "Carried, cited line unchanged. Corollary 2.2 (l.85-86) for a conventional project gives NPV(r) > 0 iff r < IRR, so the accept-or-reject reading holds at a given rate."))
A(row("CF1-b-r6-mutation-scope", "2.5-labs", "ledgers/CF1/mutants/ (none)", "PASS",
      "Lesson slice: no project grader and no mutants required (VERIFIER_RULES; round-5 and round-6 notes). None written this round."))
A(row("CF1-b-r6-alt-implementation", "2.5-labs", "tests/labs/CF1/lab-CF1-L04-1.py", "PASS",
      "Not applicable: the twin prints computed values, it is not a grader. Independent Fraction recomputation of the P profile, the gap tuple, the crossover and E2/E3 used instead (ledgers/CF1/scripts/CF1-b-r7/recompute_delta.py)."))
A(row("CF1-b-r6-verify-refs", "2.1-citations", "tools/verify_refs.py --unit CF1; tools/verify_refs.py --offline", "PASS",
      "Live: 'live re-verification of CF1: 2 of 560 entries, 0 problems', exit 0. Offline: 'offline integrity: 560 entries, 0 problems', exit 0. The two lessons cite no source outside the CF1 entries; no publisher site was contacted."))
A(row("CF1-b-r6-page-smoke", "2.5-labs", "tools/page_smoke.py --unit CF1 --pages L03 L04", "PASS",
      "Run at de53f7e: 'page_smoke modules/CF/CF1/L03.html: PASS' (lab-CF1-L03-1 0.0 s), 'page_smoke modules/CF/CF1/L04.html: PASS' (lab-CF1-L04-1 0.1 s), 'page_smoke CF1: PASS'; exit 0."))
A(row("CF1-b-r6-pytest-labs", "2.5-labs", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py", "PASS",
      "`.venv/bin/pytest -q` on the three files: 3 dot lines, 100% passed, no failures."))
A(row("CF1-b-r6-delta-coverage", "2.9-structure", "git diff d57df1e de53f7e -- course/modules/CF/CF1/L03.html course/modules/CF/CF1/L04.html tests/labs/CF1/lab-CF1-L03-1.py tests/labs/CF1/lab-CF1-L04-1.py course/modules/CF/CF1/cards.json course/modules/CF/CF1/index.html", "PASS",
      "`git diff -U0`: L03 hunks at l.67 only; L04 hunks at l.7, l.118, l.300, l.456; both twins unchanged; cards.json changes are basis fields only (55 cards); index.html changed at l.161 only (l.29 hours line unchanged). Every changed line is covered by a row in this fragment."))
A(row("CF1-b-r7-L04-l118-grid-step", "2.9-structure", "course/modules/CF/CF1/L04.html l.118 (Remark 3.4)", "PASS",
      "'A grid scan of the profile (the method of Lab 1, which evaluates the profile at rates spaced 0.0001 apart)': GRID_STEP = 0.0001 in tests/labs/CF1/lab-CF1-L04-1.py l.20 and the lab's scan at l.52. Scope: the sentence says the scan 'finds the same two sign changes', which the output confirms (sign changes on the grid: 2)."))
A(row("CF1-b-r7-L04-l456-crossover-T", "2.3-grades", "course/modules/CF/CF1/L04.html l.456 (key-results row, grade T)", "PASS",
      "T is the grade the page's proof supports: sign pattern from Proposition 3.3 (l.110, l.113), crossover 0.20 from Theorem 4.1 (l.127) with dK = 100000, dC = 120000 (Example 4.2, l.135). The lab's printed 0.200000 is cited only as a cross-check, not as the basis."))

CARRY = {
    "CF1-b-notation": "L04 l.57, l.67, l.307, l.436, l.533",
    "CF1-b-registry-citations": "L03 l.474-478; L04 l.540-544",
    "CF1-b-quiz-L03q5": "L03 l.430-436",
    "CF1-b-prose-L03-about43": "L03 l.261",
    "CF1-b-prose-L04-superlative": "L04 l.51, l.542",
    "CF1-b-prose-L03-misconception-overstates": "L03 l.261, l.265, l.387-388",
    "CF1-b-grades-L03": "L03 l.385-391, l.70-71, l.90-92, l.102-105, l.112-113",
    "CF1-b-math-L03-thm22-23-convergence": "L03 l.90-92, l.95-98, l.102-105, l.107-108, l.112-113",
    "CF1-b-math-L03-P2": "L03 l.312-316",
    "CF1-b-math-L03-theorems-proofs": "L03 l.56-64, l.70-71, l.95-98, l.107-108, l.307-309, l.357-359, l.364-366, l.371-373",
    "CF1-b-math-L03-sec3-two-line": "L03 l.248, l.458-464",
    "CF1-b-math-L04-thms": "L04 l.65-70, l.77-83, l.85-89, l.107-113, l.125-131",
    "CF1-b-math-L04-R2": "L04 l.428-431",
    "CF1-b-math-L04-remark51": "L04 l.303-309, l.305-307, l.436-438",
    "CF1-b-prose-L04-why-one-sign-change": "L04 l.51",
    "CF1-b-term-conventional": "L04 l.73, l.75, l.312",
    "CF1-b-prose-L04-conventional-def": "L04 l.75, l.79",
    "CF1-b-heading-L04-s2": "L04 l.73",
    "CF1-b-r5-L03-l87-mixed-discounting": "L03 l.86",
    "CF1-b-r6-L03-l242-interpretation": "L03 l.242",
    "CF1-b-r6-L03-l469-quiz-explain": "L03 l.469",
    "CF1-b-r6-L04-l312-accept-or-reject": "L04 l.312",
}
rows = [r for r in rows if r["id"] not in CARRY] + [carry(rid, files) for rid, files in CARRY.items()]
frag = {
    "unit": "CF1",
    "slice": "CF1-b",
    "round": 7,
    "verifier": "independent Haiku verifier, CF1 slice b (L03, L04 and their lab twins), round 7; did not build CF1 and shares no context with the builders or earlier verifiers",
    "pin": "de53f7e",
    "base": "d57df1e (round 6 pin; round 6 fragment /tmp/fanout-frags/CF1-b.round6.json, context only; its PASS rows carried only where the cited lines are byte-identical)",
    "previous_ledger": PREV,
    "checkout": "/tmp/verify7-CF1-b (detached at de53f7e, .venv symlinked, vendor copied)",
    "scratch": "/tmp/cf1-v/CF1-b-r7",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Lesson slice (L03, L04 and twins): no project grader, so no alternative-implementation check and no mutants (round-5 and round-6 notes).",
        "Delta d57df1e..de53f7e in this slice: L03 l.67; L04 l.7, l.118, l.300, l.456; twins unchanged; cards.json changes are basis fields only (55 cards, L03/L04 among them, front/back/grade unchanged).",
        "Whole-page commands (check_pages, check_dag, run_labs, page_smoke, verify_refs live and offline, pytest on three files, lint, mypy) were re-run at de53f7e. Whole files L03.html and L04.html were read in full this round.",
        "Lab copies for the E2 and E3 solutions were run from ledgers/CF1/scripts/CF1-b-r7/lab_copy_claims.sh (scratch copies in /tmp/cf1-v/CF1-b-r7/).",
        "Not re-run: round-5 and round-6 scripts (absent from this checkout); the change in L04 l.7 is judged on the text, not on a tool.",
        "Live references: verify_refs --unit CF1 checks 2 of 560 entries; no external source is cited by these lessons, so no publisher or SEC site was contacted.",
    ],
    "summary": {"result": "one FAIL: CF1-b-r5-meta-L04-description (L04 l.7 meta description: 'the single example of a project with two sign changes and two IRRs (Example 3.2)'; the page's own Problems M3 (l.359-363) and R1 (l.420-424) are further projects with two sign changes and two IRRs, so 'single' is not supported)."},
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", OUT, len(rows))
