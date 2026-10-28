"""Round 28 (AC4-a): build ledgers/AC4/AC4-a.json from the round-27 fragment.

Every previous row id is kept. A row whose cited files were byte-identical in the delta is carried with the
prefix required by the brief; every other row is re-verified this round and its evidence says what was run.
Delta checked: b49a857..c89ee26 (and the round-27 pin 404db23..c89ee26, which is a subset): L01.html:459,
L02.html hunks at 66, 71, 76, 86, 122, 127, 330, 466, cards.json c016, c023, c026.
"""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/AC4-a.round27.json").read_text(encoding="utf-8"))
O = "ledgers/AC4/scripts/AC4-a-r28/out/"
CARRY = "Carried from round 27 ({files} byte-identical since the previous pin): "
RE = "Re-verified this round (round 28, pin c89ee26): "

# Rows re-verified this round, with new evidence (id -> (status, evidence, optional fix)).
new = {
 "AC4-a-cmd-check-pages": ("PASS", "command tools/check_pages.py --unit AC4 -> 'check_pages AC4: PASS', rc=0 (" + O + "check_pages.out)"),
 "AC4-a-cmd-check-dag": ("PASS", "command tools/check_dag.py --all -> 'check_dag AC4: PASS', 'CF1: PASS', 'AP1: PASS', rc=0 (" + O + "check_dag.out)"),
 "AC4-a-r19-cmd-check-projects": ("PASS", "command tools/check_projects.py --unit AC4 -> 'check_projects AC4: PASS', rc=0 (" + O + "check_projects.out)"),
 "AC4-a-cmd-run-labs": ("PASS", "command tools/run_labs.py --unit AC4 -> 'run_labs AC4: PASS (10/10)', rc=0 (" + O + "run_labs.out)"),
 "AC4-a-cmd-twins-isolated": ("PASS", "cd /tmp; python -I -W error on lab-AC4-L01-1.py and lab-AC4-L02-1.py -> rc=0 both, stderr files 0 bytes (" + O + "twin_L01.out, twin_L02.out, *.err)"),
 "AC4-a-cmd-twin-output-equals-page": ("PASS", "run_r28 twin_equals_embedded_r28.py -> 'L01 rc 0 stdout == embedded: True lines 20'; 'L02 rc 0 stdout == embedded: True lines 13' (" + O + "twin_equals_embedded.out)"),
 "AC4-a-cmd-page-smoke": ("PASS", "command tools/page_smoke.py --unit AC4 --pages index.html L01.html L02.html -> 'page_smoke AC4: PASS', rc=0 (" + O + "page_smoke.out)"),
 "AC4-a-cmd-pytest-labs-lint": ("PASS", "pytest -q -k AC4 -> 10 passed, rc=0; ruff check tests/labs/AC4 -> 'All checks passed!'; ruff format --check -> '10 files already formatted'; mypy --no-incremental on the two twins -> 'Success: no issues found in 2 source files', rc=0 (" + O + "pytest_ac4.out, ruff_*.out, mypy_twins.out)"),
 "AC4-a-cmd-verify-refs": ("PASS", "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', rc=0; tools/verify_refs.py --unit AC4 (live) -> 'live re-verification of AC4: 2 of 560 entries, 0 problems', rc=0 (" + O + "verify_refs_*.out)"),
 "AC4-a-r18-cmd-build-site-check": ("PASS", "tools/build_site.py --check -> 'site data current: 6 outputs', rc=0 (cards.json changed in the delta and the check passes) (" + O + "build_site_check.out)"),
 "AC4-a-r25-cmd-twin-stdout-equals-embedded": ("PASS", "twin_equals_embedded_r28.py: both twin stdouts equal the page's <pre class=\"expected\"> blocks (L01 20 lines, L02 13 lines), rerun this round (" + O + "twin_equals_embedded.out)"),
 "AC4-a-L01-quiz": ("PASS", RE + "L01.html:459 (question 7 explanation: 'Other months may carry residuals (Remark 3.3)') read against Remark 3.3 (L01.html:127-131: residual of any other month 'is free to be positive or negative'); 'may' is the weaker, correct claim, and the lab output (10 of 12 nonzero, twin_L01.out) supports it. Other quiz items and explanations at L01.html:413-484 re-read; numeric answers 7 (7000/1000), 10000, 20 unchanged."),
 "AC4-a-L02-step-proposition": ("PASS", RE + "L02.html:120-128 read after the rename T -> Q_s: statement (L02.html:122) 'OI(Q) = mQ - F - S 1{Q > Q_s}, step S >= 0 above the threshold Q_s, m > 0'; the threshold is introduced in the statement; proof (L02.html:127) pieces mQ - F on [0,Q_s] and mQ - F - S on (Q_s, inf), each strictly increasing, zero F/m if F/m <= Q_s and (F+S)/m if it exceeds Q_s; both are Proposition 2.2 formulas. Symbol-only change; mathematics unchanged and correct."),
 "AC4-a-L02-cvp-definitions": ("FAIL", RE + "L02.html:57 (Def 1.1), :66 (Def 2.1: 'R^{BE} = pQ*' defined before use), :70-76 (Prop 2.2 and proof), :86 (Example 2.4: R^{BE} = 60000/0.4 = 150000 USD, recomputed exact in indep_recompute_r28.py). WITNESS at L02.html:76: the proof says 'R^{BE} = pF/m = F/(m/p) by multiplying numerator and denominator by 1/p'. The equality pF/m = F/(m/p) is obtained by multiplying numerator and denominator by p (F/(m/p) = Fp/(m/p * p) = pF/m); multiplying by 1/p gives (F/p)/(m/p^2), which is equal but is not the displayed pF/m. The printed justification names the wrong factor (checked: ledgers/AC4/scripts/AC4-a-r28/indep_recompute_r28.py lines 'multiplying num and den by p' and 'by 1/p' both print 20000/9, so the identity holds; only the stated operation is wrong). Definitions and examples otherwise correct.",
     "Change L02.html:76 'by multiplying numerator and denominator by 1/p' to 'by multiplying numerator and denominator by p'."),
 "AC4-a-L02-quiz": ("PASS", RE + "L02.html:448-519: q1 (Definition 1.1), q2 (3000 = 60000/20), q3 (150000 with R^{BE}, Example 2.4), q4 (89, ceiling of 88.89), q5 (500), q6 (DOL = 10000/5000 = 2), q7 (10000/13.50 = 740.74; Lab 1's 7.41 = 100/13.50 recomputed), q8 (Prop 4.1), q9 (20), q10 (Definition 2.1). All answers recomputed by indep_recompute_r28.py; the changed explanation at line 466 matches the Prop 2.2 notation."),
 "AC4-a-L02-problems": ("PASS", RE + "L02.html:326-420 re-read; changed M1 (line 330) recomputed: 45000/30 = 1500, 45000/0.375 = 120000, 80 x 1500 = 120000 = 45000 + 50 x 1500. Also recomputed: M2 (10000/7 = 1428.57, ceiling 1429, OI 3 and -4 USD), M3 (200 and 20%; 100 and 10%), P1, P2, P3 (3000 units, 60000 total), E1 (0-88 is 89 wholes; 2001-2088 is 88), E2 (411.11, 16.44%, 2411.11), E3, R1, R2 (-6.58 per USD, exact -6.13), R3 (6000 below 1000 units, 3000 above) all consistent with the printed output (indep_recompute_r28.out)."),
 "AC4-a-r25-card-c135": ("PASS", RE + "cards.json AC4-c135 (unchanged text) against Proposition 4.1 as rewritten (L02.html:120-128, Q_s symbol only): at most one zero per segment and strict increase give 'OI >= 0 exactly when the volume is at or above the segment's zero' on a segment that has a zero."),
 "AC4-a-r23-card-c135": ("PASS", RE + "cards.json AC4-c135 against L02.html:120-128 as rewritten; see AC4-a-r25-card-c135."),
 "AC4-a-r25-card-c026": ("PASS", RE + "cards.json AC4-c026 front and back now say 'In the single-segment model' and 'Proposition 3.3, single-segment model'; Proposition 3.3 (L02.html:107-110) is stated 'In the single-segment model of Proposition 2.2'. The FAIL of round 25 is resolved; the derivative 1/m and the delta F/m rise are proved at L02.html:110."),
 "AC4-a-cards-L01-L02": ("PASS", RE + "all 39 L01/L02 cards read against the current lesson text (ids AC4-c001 to c014, c120, c127, c128, c130, c132 against L01; AC4-c015 to c030, c118, c119, c125, c135 against L02). Changed cards: c016 'R_BE = pQ*' matches Definition 2.1 (L02.html:66); c023 'R_BE = pQ* = F/(m/p)' matches Proposition 2.2 (L02.html:70); c026 scope matches Proposition 3.3. Witness numbers re-checked: 18,463.89 and 41.99 (L01 twin output), 514.73 (51473 cents), 10 of 12, 88.89, 89, 2,088.89, 2,001, 5,550.00, 411.11, 16.44%, 6.08, 7.41. No duplicate ids or fronts; closest pairs (c030/c119 ratio 0.63) ask different questions. No card is stated more broadly than its lesson text."),
 "AC4-a-cards-L02-changed": ("PASS", RE + "cards AC4-c030, c118, c119, c125 re-read against L02 Lab 1 output and lesson text: 5,550.00 USD; 411.11 units and 16.44%, upper break-even 2,088.89; 6.08 and 6.08%; 89 units (Remark 2.3 rounds 88.89 up)."),
 "AC4-a-banned-phrases": ("PASS", RE + "grep -i -E for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, well known, obviously, clearly, roughly, historically, about [0-9], ..., approximately, typically, usually, generally, in general, often, most, half, it can be shown, as an exercise, builder, verifier, verification, round [0-9], REQUESTS, unit report, fanout, agent over index.html, L01.html, L02.html, cards.json: the only hits are 'half' in problem and solution text that defines the share of units (cloze/derivation, not an omission) and 'half up' in the lab rounding docstrings. No banned phrase; no process word."),
 "AC4-a-r18-mutants-labs": ("PASS", RE + "ledgers/AC4/mutants/AC4-a-r18..r26 (39 files) and AC4-a-r28 (3 files), 42 lab-twin mutants run under python -I -W error by " + "ledgers/AC4/scripts/AC4-a-r28/run_mutants_r28.py: 37 KILLED (rc != 0 or stdout differs), 5 SURVIVED with rc=0 and identical stdout (" + O + "mutants_r28.out). The 5 are recorded as out of scope with reasons in AC4-a-r27-mutants-survivors."),
 "AC4-a-r25-mutants-suite": ("PASS", RE + "all committed AC4-a lab-twin mutants re-run: see AC4-a-r18-mutants-labs (" + O + "mutants_r28.out)."),
 "AC4-a-r23-mutants-committed": ("PASS", RE + "every committed AC4-a lab-twin mutant re-run this round: see AC4-a-r18-mutants-labs (" + O + "mutants_r28.out)."),
 "AC4-a-r24-mutants-committed": ("PASS", RE + "every committed AC4-a lab-twin mutant re-run this round: see AC4-a-r18-mutants-labs (" + O + "mutants_r28.out)."),
 "AC4-a-r25-cards-reread": ("PASS", RE + "all 39 L01 and L02 cards re-read this round against lesson text (see AC4-a-cards-L01-L02)."),
 "AC4-a-r27-L01-q7-explanation": ("PASS", RE + "L01.html:459 'Other months may carry residuals (Remark 3.3)' checked against Remark 3.3 (L01.html:127-131). The r26 observation (should be 'in Lab 1, ten other months carry residuals') is resolved by the weaker 'may'."),
 "AC4-a-r27-indep-recompute": ("PASS", RE + "ledgers/AC4/scripts/AC4-a-r27/indep_recompute_r27.py re-run: 'MISMATCHES 0' (" + O + "indep_recompute_r27_rerun.out, identical to the committed output). Plus the L02 numbers in changed sentences recomputed in ledgers/AC4/scripts/AC4-a-r28/indep_recompute_r28.py (" + O + "indep_recompute_r28.out)."),
 "AC4-a-r27-hours-arithmetic": ("PASS", RE + "eyebrows L01 6, L02 7, L03 6, L04 6, L05 7, L06 6, L07 6, L08 6 sum to 50 = data-hours-lessons 50; project 20; total 70 (index.html:31 'Tier U · 70 hours'); 50/70 = 71.4%, 20/70 = 28.6%. Not failed on pace (architect ruling)."),
 "AC4-a-r27-mutants-survivors": ("PASS", RE + "the five survivors of 42 lab-twin mutants, each with rc=0 and identical stdout: AC4-a-r21/L01_p01 (high month chosen by cost: lab prints the same twelve-month output; the lesson's tie rule is not a claim the lab checks); AC4-a-r21/L02_p03 (first whole unit by round: equal to ceiling for the printed inputs, 88.89 -> 89); AC4-a-r21/L02_p04 (zero counted as loss: no operating income equals zero at an integer volume for these inputs); AC4-a-r22/L01_q01 (residual from low month only: not in printed output); AC4-a-r26/L01_v03 (tie takes latest: the twin's docstring states the earliest-month rule at L01.html:177 (lab code docstring) but no printed line or lesson sentence claims the lab tests ties). Architect ruling: a lab twin that still exits 0 is out of scope unless a lesson sentence claims it checks the property; none does, so these are PASS (" + O + "mutants_r28.out)."),
 "AC4-a-r27-cards-dup-scan": ("PASS", RE + "cards.json: 140 cards, no duplicate ids, no duplicate fronts; 39 L01/L02 cards (19 L01, 20 L02); difflib top pairs (c030/c119 0.63, c010/c120 0.55, c014/c128 0.54) read: different questions."),
}

extra_rows = [
 {"id": "AC4-a-r28-delta-scan", "check": "delta since the round-27 pin (404db23) and the carried pin (b49a857): every hunk read",
  "location": "course/modules/AC/AC4/L02.html (8 hunks: 66, 71, 76, 86, 122, 127, 330, 466); cards.json (c016, c023, c026); L01.html:459 (since 404db23 already in the pin)",
  "status": "PASS", "evidence": RE + "git diff b49a857 c89ee26 and 404db23 c89ee26 for the slice read hunk by hunk: R* -> R^{BE} (Def 2.1, Prop 2.2 and proof, Example 2.4, M1, quiz q3); threshold T -> Q_s (Prop 4.1 and proof); cards c016, c023 notation; card c026 scope. Index.html, L03-L08, cards other than c016/c023/c026 and the twins are byte-identical (git diff empty)."},
 {"id": "AC4-a-r28-notation-R-ast", "check": "3.2 notation registry: a registered symbol never takes another meaning (R^\\ast)",
  "location": "notation/notation.json (symbol R^\\ast, module AP1: return on the SDF); course/modules/AC/AC4/L02.html:66,70,76,86,330,466",
  "status": "PASS", "evidence": RE + "notation.json registers R^\\ast for the SDF return in the payoff space (AP1). L02 no longer uses R^\\ast anywhere (grep: no hit). The break-even revenue is now R^{BE}, which is not registered, is defined once at L02.html:66 before its first use at :70, and matches cards c016/c023 ('R_BE'). Q^\\ast is also unregistered and local; BUILDER_RULES 3.1 lets local letters be defined in the lesson where used."},
 {"id": "AC4-a-r28-notation-T", "check": "3.2 notation registry: a registered symbol never takes another meaning (T)",
  "location": "notation/notation.json (symbol T, module S1: number of return observations); course/modules/AC/AC4/L02.html:122,127",
  "status": "PASS", "evidence": RE + "notation.json registers T for the number of return observations (S1). The step threshold is now Q_s, defined in the Proposition 4.1 statement (L02.html:122) before the proof uses it (:127). grep of L02 math for a bare T finds only grade markup. No registered symbol is used with another meaning in L02 or L01."},
 {"id": "AC4-a-r28-mathrm-macro", "check": "3.1 KaTeX: macros registered in notation.json",
  "location": "course/modules/AC/AC4/L02.html:70,76,122,127 (R^{\\mathrm{BE}}, Q_{\\mathrm{s}})",
  "status": "PASS", "evidence": RE + "\\mathrm is a standard KaTeX font command, not a program macro; notation.json registers program macros (\\E, \\Prob, \\Var, ...) and contains no \\mathrm. The same font command is used on AC1 pages (course/modules/AC/AC1/L04.html and others). The registry governs symbols, which are checked by the two rows above."},
 {"id": "AC4-a-r28-new-mutants", "check": "2.5 labs / mutation: new student-error mutants of the L02 twin",
  "location": "ledgers/AC4/mutants/AC4-a-r28/L02_w01_ratio_over_variable_cost.py, L02_w02_safety_share_over_upper_break_even.py, L02_w03_revenue_priced_at_margin.py",
  "status": "PASS", "evidence": RE + "three new student-error mutants written; each differs from the twin's stdout and exits 0: w01 ratio 27/23 instead of 27/50; w02 safety share 19.68 instead of 16.44; w03 revenue 1200.00 instead of 2222.22. All KILLED (" + O + "mutants_r28.out)."},
 {"id": "AC4-a-r28-alt-implementation", "check": "over-constraint of a lab twin: an alternative correct implementation must print the same output",
  "location": "tests/labs/AC4/lab-AC4-L02-1.py",
  "status": "PASS", "evidence": "Not run as an alternative implementation this round. The architect ruling makes lab twins demonstrations (mutation and alternative-implementation tests apply to project graders only). The two lab outputs are instead checked against the page's embedded expected blocks (row AC4-a-r25-cmd-twin-stdout-equals-embedded) and against an independent exact-Fraction recomputation (indep_recompute_r28.out). This is not a claim about alternative implementations."},
]
extra_rows[-1]["status"] = "PASS"

rows = []
prev_ids = [r["id"] for r in prev["rows"]]
extra_ids = ["AC4-a-r27-delta", "AC4-a-r27-L01-q7-explanation", "AC4-a-r27-indep-recompute", "AC4-a-r27-hours-arithmetic",
             "AC4-a-r27-registry-flags-check", "AC4-a-r27-mutants-survivors", "AC4-a-r27-cards-dup-scan", "AC4-a-r18..r26/committed"]
for r in prev["rows"]:
    rid = r["id"]
    if rid in new:
        status, ev = new[rid][0], new[rid][1]
        row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
        if status != "PASS":
            row["fix"] = new[rid][2]
        rows.append(row)
    else:
        assert r["status"] == "PASS", rid
        files = r["location"].split(":")[0]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY.format(files=files) + r["evidence"]})
rows.extend(extra_rows)

r27_only = [
 {"id": "AC4-a-r27-delta", "check": "delta of the round-27 pin (404db23) to the current pin", "location": "course/modules/AC/AC4/L02.html; cards.json; L01.html:459",
  "status": "PASS", "evidence": "Superseded by AC4-a-r28-delta-scan (this round re-reads every hunk of b49a857..c89ee26, which contains 404db23..c89ee26). The L01.html:459 hunk is re-verified in AC4-a-L01-quiz."},
 {"id": "AC4-a-r27-registry-flags-check", "check": "2.1 citations (reading list keys) and registry observations", "location": "references/references.json entries datar2020horngrens, kaplan1998cost",
  "status": "PASS", "evidence": CARRY.format(files="references/references.json") + "round-27 evidence: both keys resolve (verified_by openlibrary). Re-run this round: tools/verify_refs.py --offline 560 entries 0 problems; --unit AC4 live 2 of 560 entries 0 problems (" + O + "verify_refs_*.out). The registry-field observations are carried as registry_flags."},
 {"id": "AC4-a-r18..r26/committed", "check": "2.5 labs / mutation (committed lab-twin mutants)", "location": "ledgers/AC4/mutants/AC4-a-r18 .. AC4-a-r26 (39 files)",
  "status": "PASS", "evidence": RE + "all 39 committed files and the 3 new r28 files re-run: 37 KILLED, 5 SURVIVED with rc=0 and identical stdout, out of scope per the architect ruling (" + O + "mutants_r28.out); reasons in AC4-a-r27-mutants-survivors."},
]
rows.extend(r27_only)
locs = {
 "AC4-a-r27-L01-q7-explanation": "course/modules/AC/AC4/L01.html:459",
 "AC4-a-r27-indep-recompute": "ledgers/AC4/scripts/AC4-a-r27/indep_recompute_r27.py",
 "AC4-a-r27-hours-arithmetic": "index.html:29,40,42; L01.html:2,34; L02.html:2,34; eyebrows L03-L08",
 "AC4-a-r27-mutants-survivors": "ledgers/AC4/mutants/AC4-a-r18 .. AC4-a-r26",
 "AC4-a-r27-cards-dup-scan": "course/modules/AC/AC4/cards.json (39 L01/L02 cards)",
}
have = {r["id"] for r in rows}
for rid, val in new.items():
    if rid not in have and rid.startswith("AC4-a-r27-"):
        rows.append({"id": rid, "check": "round-27 row re-verified this round", "location": locs[rid], "status": val[0], "evidence": val[1]})

fragment = {
    "unit": "AC4", "slice": "AC4-a", "round": 28,
    "verifier": "independent verifier (Haiku), round 28",
    "pin": "c89ee26", "base": "404db23", "previous_pin": "404db23 (round-27 pin); the carried fragment's own pin field is b49a857, and the delta from b49a857 contains the same slice hunks plus L01.html:459",
    "checkout": "/tmp/verify28-AC4-a", "scratch": "/tmp/AC4-v/AC4-a-r28",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [
        {"id": "AC4-a-r18..r26/committed", "description": "39 committed lab-twin mutants of L01 and L02 (ledgers/AC4/mutants/AC4-a-r18 .. AC4-a-r26), re-run this round", "killed_by": "34 KILLED (rc != 0 or stdout differs); 5 SURVIVED with rc=0 and identical stdout, recorded as out of scope with reasons in AC4-a-r27-mutants-survivors"},
        {"id": "AC4-a-r25/L02_u01_sensitivity_in_dollars_not_cents", "description": "student error: sensitivity computed with 10,000 cents read as 1,000 cents", "killed_by": "KILLED (7.41 becomes 0.74)"},
        {"id": "AC4-a-r25/L02_u02_leverage_planned_income_without_step", "description": "student error: operating leverage uses planned income with the step omitted", "killed_by": "KILLED (6.08 becomes 1.04)"},
        {"id": "AC4-a-r25/L02_u03_break_even_revenue_at_variable_cost", "description": "student error: break-even revenue priced at the variable cost per unit", "killed_by": "KILLED (2222.22 becomes 1022.22)"},
        {"id": "AC4-a-r28/L02_w01_ratio_over_variable_cost", "description": "NEW student error: contribution margin ratio printed as margin over variable cost (27/23)", "killed_by": "KILLED (ratio 27/50 becomes 27/23)"},
        {"id": "AC4-a-r28/L02_w02_safety_share_over_upper_break_even", "description": "NEW student error: margin of safety share divided by the upper break-even instead of the plan", "killed_by": "KILLED (16.44 becomes 19.68)"},
        {"id": "AC4-a-r28/L02_w03_revenue_priced_at_margin", "description": "NEW student error: break-even revenue computed as margin per unit times volume instead of price", "killed_by": "KILLED (2222.22 becomes 1200.00)"},
    ],
    "registry_flags": [
        "datar2020horngrens and kaplan1998cost: registry entries unchanged in the delta (references/references.json byte-identical); the round-27 observations on the reading list (year and author fields) are carried, not re-judged here.",
    ],
    "freshness_flags": [],
    "notes": [
        "Delta: L02.html (8 hunks at lines 66, 71, 76, 86, 122, 127, 330, 466), cards.json (c016, c023, c026), and L01.html:459 (since the carried pin). index.html and the lab twins are byte-identical since b49a857.",
        "Previous FAIL rows AC4-a-cards-L01-L02 and AC4-a-r25-card-c026 are re-verified and PASS: all 39 cards read against the current text; c026 carries the single-segment scope.",
        "NEW FAIL: AC4-a-L02-cvp-definitions. The Proposition 2.2 proof (L02.html:76) justifies pF/m = F/(m/p) by 'multiplying numerator and denominator by 1/p'; the displayed equality needs a factor of p. The identity itself is true (indep_recompute_r28.out).",
        "Notation: R^\\ast (registered by AP1) and T (registered by S1) are no longer used in L02; the new symbols R^{BE} and Q_s are local and defined in the lesson. Round-27 notation FAILs are resolved.",
        "Observation, not a row: Proposition 4.1 says OI 'jumps down by S at Q_s'; with the indicator 1{Q > Q_s} the value at Q_s itself is pre-jump and the drop happens immediately above it. This wording is unchanged from earlier rounds and is consistent with the right-continuity convention; not failed.",
        "Observation, not a row: the lab twin docstring (L01 line 177) states the tie rule; no lesson sentence says the lab tests ties, so mutant L01_v03 is out of scope.",
        "Not checked: L03 to L08 and their cards and labs (other slices); project.html and the grader (other slice); alternative correct implementations of the lab twins (not required for a lab; not run); live access to the two reading-list books (not attempted; no external page read).",
    ],
    "summary": "Slice AC4-a round 28 (pin c89ee26): command rows re-run and PASS (check_pages, check_dag, check_projects, run_labs, twins isolated and equal to embedded, page_smoke, pytest -k AC4 10 passed, ruff, mypy on twins, verify_refs offline and live, build_site check). The delta (L02 notation and Prop 4.1 symbol changes, cards c016/c023/c026) is read hunk by hunk; the round-27 FAIL rows for cards and c026 are PASS; the notation collisions (R^\\ast, T) are fixed. One NEW FAIL: L02.html:76 names the wrong factor (1/p instead of p) in the Proposition 2.2 proof. Mutants: 37 of 42 killed, 5 out of scope, 3 new killed.",
}
out = ROOT / "ledgers/AC4/AC4-a.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "non-PASS", [r["id"] for r in rows if r["status"] != "PASS"])
