"""Builds ledgers/M1/M1-b.json for round 20 (slice b: L04, L05 and twins). Rows are the verifier's own.
Previous round's row ids are kept; a row is re-verified (fresh) when its cited lines or subject changed in the
delta 51fa336..fd9a9b7 (L04.html 244, 261, 358; L05.html 236, 255-256), otherwise carried."""
import json
import pathlib
import sys

PREV = json.load(open("/tmp/fanout-frags/M1-b.round19.json"))
CARRY = ("Carried from round 19 (course/modules/M/M1/L04.html, L05.html and cards.json byte-identical since the "
         "previous pin 51fa336 at the cited lines; the delta changes only L04.html lines 244, 261, 358 and "
         "L05.html lines 236, 255-256, none cited here):")
OUT = "ledgers/M1/scripts/M1-b-r20/out/"
FRESH = {}   # id -> (status, evidence, fix)

def fresh(i, status, ev, fix=""):
    FRESH[i] = (status, ev, fix)

fresh("M1-b-cmd-pin", "PASS",
      "git rev-parse HEAD = fd9a9b72f000e509f3af78babf970cd4c9a847e4 (detached checkout). Delta 51fa336..fd9a9b7 for "
      "M1 slice b: L04.html lines 244, 261, 358; L05.html lines 236, 255-256 (git diff -U0); cards.json and "
      "tests/labs/M1 unchanged. Lesson pages: L04 473 lines, L05 486 lines (wc), 180 card entries.")
fresh("M1-b-cmd-run_labs", "PASS",
      "Command: .venv/bin/python tools/run_labs.py --unit M1 (exit 0): 'run_labs M1: PASS (11/11)'. Saved at " + OUT + "run_labs.txt.")
fresh("M1-b-cmd-twins", "PASS",
      "Each twin run with python -I -W error from a scratch directory: exit 0, empty stderr (" + OUT + "twin_L04.out, twin_L05.out). "
      "Stdout equals the <pre class=\"expected\"> block of L04.html and L05.html (string equality True). L04 prints 27 lines "
      "(Part A 6, Part B 14, Part C 7); L05 prints 13. Embedded code block equals the twin file for both (True).")
fresh("M1-b-cmd-page_smoke", "PASS",
      "Command: tools/page_smoke.py --unit M1 --pages L04 L05 (exit 0): both pages PASS, 'page_smoke M1: PASS'. " + OUT + "page_smoke.txt.")
fresh("M1-b-cmd-check_pages_dag", "PASS",
      "check_pages --unit M1: 'check_pages M1: PASS'; check_dag --unit M1: 'check_dag M1: PASS' (" + OUT + "check_pages.txt, check_dag.txt).")
fresh("M1-b-cmd-lint-types", "PASS",
      "ruff check exit 0 ('All checks passed!'); ruff format --check exit 0 ('2 files already formatted'); mypy --no-incremental: "
      "'Success: no issues found in 2 source files' (" + OUT + "ruff.txt, mypy.txt).")
fresh("M1-b-cmd-refs", "PASS",
      "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (exit 0). verify_refs.py --unit M1: "
      "'live re-verification of M1: 1 of 560 entries, 0 problems' (exit 0). L04 and L05 cite no registry key (references "
      "sections: 'This lesson cites no outside source'). " + OUT + "verify_refs_offline.txt, verify_refs_live_M1.txt.")
fresh("M1-b-cmd-pytest", "PASS",
      "pytest -q tests/test_run_labs.py tests/test_page_checks.py tests/test_labs.py: exit 0 (" + OUT + "pytest.txt).")
fresh("M1-b-2.2-L04-numbers-recomputed", "PASS",
      "Recomputed in Decimal at 60 digits (" + OUT + "recompute_L04.txt, script recompute.py): e^0.05 = 1.0512710964; "
      "Part B errors and factors agree with the printed table; ratio of errors 1000->10000 unrounded 9.99969 and "
      "10000->100000 unrounded 9.99997 (interpretation line 218 correct); Part C unrounded monthly 1,647,009.4977, daily "
      "1,648,664.8138, continuous 1,648,721.2707, annual 1,628,894.6268; monthly minus annual unrounded 18,114.87 and "
      "continuous minus daily unrounded 56.46 (correct); printed-value ratio 1656/56 = 29.57; unrounded gap "
      "1,655.3161 -> 1,655.32 and ratio 1655.3161/56.4569 = 29.32 (E3 solution, correct). Misconception 2 values 0.0011618979 "
      "and 0.0000035999 recomputed. EAR 365 - EAR 12 = 0.0001055986 (E1 correct). 8% monthly EAR 0.0829995068 (M1 correct). "
      "Example 3.2 exact 1.05^10 = 16679880978201/10240000000000 agrees.")
fresh("M1-b-2.2-L04-M3-rounding", "PASS",
      "Recomputed (" + OUT + "recompute_L04.txt): e^(0.05/12) = 1.00417535929112, 12 x 0.004175359291 = 0.050104311492 (page value "
      "agrees to the stated digits); (1 + 0.0501043115/12)^12 = 1.0512710964 to ten places (page M3 check correct).")
fresh("M1-b-2.2-L04-E2-digits", "PASS",
      "Recomputed: F_1000000 = 1.051271095062 (printed 1.0512710951), e^0.05 = 1.051271096376; first eight decimals 05127109 "
      "agree, differ at the ninth (5 vs 6); printed error 0.0000000013141 (page E2 correct).")
fresh("M1-b-2.2-L05-numbers-recomputed", "PASS",
      "Recomputed (" + OUT + "recompute_L05.txt): PV at t=5 annual 783526.1665, semiannual 781198.4017, continuous 778800.7831. "
      "Printed-value gap 2,328 (line 270) and unrounded 2,327.7647 -> 2,327.76 (correct). Unrounded semiannual-continuous "
      "2,397.6187 -> 2,397.62 (correct). Interpretation line 236: printed table values and the 4,725-cent spread (783,526 - 778,801) "
      "agree; 'as Proposition 2.2 states' compares printed rows with an inequality the page states under E. Example 3.1 values "
      "agree. E3 at t=10: 613,913.2535 -> 613,913 cents (correct).")
fresh("M1-b-2.2-L05-M1-M3-rounding", "PASS",
      "Recomputed (" + OUT + "recompute_L05.txt): 1.04^-3 = 0.888996358671 (M1 six-place 0.888996 correct); 1/1.1236 = 0.889996440014 and "
      "250000 x 0.88999644 = 222,499.11 -> 222,499 (M2 correct); e^-0.06 = 0.941764533584, 500000 x = 470,882.27 (M3 correct).")
fresh("M1-b-2.2-L05-R2-check", "PASS",
      "Recomputed: 1.052409779149^10 = 1.666666666668 (1.6666666667 to ten places); 1/1.6666666667 = 0.6 to ten places; shorter "
      "1.0524097791^10 = 1.666666665892 (printed 1.6666666659 correct); 1+r error 4.9e-11 and 10(1+r)^9 = 15.84 ('about 15.8' correct).")
fresh("M1-b-2.4-math-L04", "PASS",
      "Proofs re-read on this round: Prop 2.1 (83-100), Prop 2.2 (101-115), Prop 3.1 (224-228), R3 (361-367). None of the cited lines "
      "changed; R2 at 358 changed and is verified in M1-b-r20-delta-L04-358-R2.")
fresh("M1-b-2.4-math-L05", "PASS",
      "Assumption E consequences (i)-(iii), Prop 1.4, Remark 1.5, Props 2.1, 2.2, 2.4 re-read in full; no changed line in these ranges; "
      "the proofs are valid under the stated hypotheses.")
fresh("M1-b-2.4-L05-quiz-L05q5", "PASS",
      "Quiz q5 (431-438): Lab 1 prints 778,801 as the lowest present value (twin output). The explanation's 'annual is largest, by "
      "Propositions 2.2 and 2.4' is correct; 'Lab 1 prints the continuous value below the semiannual value' is a printed-value statement, correct.")
fresh("M1-b-2.3-grades", "PASS",
      "Props 2.1, 2.2, 2.4 and 1.4 are proved on their pages (T); the changed lines (244, 261, 358, 236, 255-256) carry no grade, "
      "so the grades are unchanged and correct.")
fresh("M1-b-2.5-lab-L04", "PASS",
      "Lab 1 hypothesis (117) re-read: Part A five frequencies (tuple of 5), Part B ten values of m (PERIODS has 10), error = e^r minus "
      "factor, Part C four conventions; factor_increases_with_periods and factor_below_continuous print True; no random import. "
      "Misconceptions 1-3 (253-261) re-read: line 261 (misconception 3) now scopes Assumption E correctly; the remaining "
      "Remark 2.3 finding is in M1-b-r20-E-scope-remarks.")
fresh("M1-b-2.5-lab-L05", "PASS",
      "Lab 1 hypothesis (142): five t values (YEARS tuple of 5), annual, semiannual and continuous factors, equivalent-rate factor, present "
      "values at t=5 printed. The interpretation (236) claims are read off the printed table and checks, which the printed output "
      "supports. Remark 2.3 (127) is flagged separately in M1-b-r20-E-scope-remarks.")
fresh("M1-b-2.9-structure-prose", "PASS",
      "Full pages re-read this round (every line). Banned-phrase grep (roughly, historically, typically, generally, usually, builder, "
      "verifier, round N, ellipsis) on L04.html and L05.html: no hit. Section template present on both pages.")
fresh("M1-b-2.9-DAG", "PASS",
      "check_dag --unit M1: PASS (re-run this round). L04 meta-rows and definitions unchanged in the delta.")
fresh("M1-b-hours", "PASS",
      "Lesson data-hours: L01 8, L02 9, L03 9, L04 9, L05 8, L06 9, L07 9, L08 9; sum 70 equals the hub data-hours-lessons=70 and "
      "index.html:149 ('Lessons 1 and 5 declare 8 hours, the other six declare 9'). Arithmetic only; pace not judged.")
fresh("M1-b-2.7-cards", "FAIL",
      "Card M1-c068 (cards.json:458-461) back '(1 + r/m)^(mt), because mt is the number of periods (Remark 1.3).' The current "
      "Remark 1.3 (L04.html:70) states the factor 'with mt a whole number' and says mt is then the number of periods. The card drops "
      "that condition; still unchanged in this delta (cards.json unchanged since 51fa336). Other L04/L05 cards match their current "
      "lesson lines (checked each; full scan: 180 entries, no duplicate id or front). Card M1-c088 (L05) is a second card defect, "
      "row M1-b-r20-cards-c088.",
      "Change the back of M1-c068 (cards.json line 461) to: '(1 + r/m)^(mt) when mt is a whole number, because mt is then the number "
      "of periods (Remark 1.3).'")
fresh("M1-b-r19-cards-scan", "PASS",
      "Round 20 scan of cards.json: 180 entries; L04 16, L05 21; no duplicate id, no duplicate front (Counter scan, " + OUT + "cards_scan.txt).")
fresh("M1-b-r7-L04-244-periodic", "PASS",
      "L04.html:244 changed this delta: 'Periods that do not fit the horizon. Remark 1.3 counts periods, so it applies when mt is a whole "
      "number, and then the exponent is a whole number of periods.' Matches Remark 1.3 (line 70). 'Lab 1 uses whole years' is correct "
      "(years=1 and 10 in the lab's periodic_factor calls). Continuous factors are not periodic (continuous_factor).")
fresh("M1-b-2.5-lab-L04-misc-261", "PASS",
      "L04.html:261 (misconception 3, changed): 'Proposition 2.2, under Assumption E, proves F_m(r) < e^r ... Each extra compounding period "
      "raises the factor (Proposition 2.1). Under Assumption E, no finite frequency reaches the continuous factor.' The Prop 2.2 scope is "
      "stated. Prop 2.1 needs r > 0; the sentence 'Each extra compounding period raises the factor' is read inside the preceding clause "
      "'for every r > 0' of the same paragraph (at r = 0 every factor is 1, so the clause is needed). Lab 1 Part B shows each printed "
      "factor below e^0.05 (printed).")
fresh("M1-b-r20-delta-L04-358-R2", "PASS",
      "L04.html:358 (R2 solution, changed): 'So, under Assumption E, no finite compounding frequency reaches the continuous effective rate "
      "... Under the same assumption, an offer compounded continuously ... pays a strictly higher one-year growth than any offer ... "
      "compounded a finite number of times.' Proof: F_m(r) < e^r (Prop 2.2) gives EAR_m(r) < e^r - 1 for r > 0 (the problem's own "
      "hypothesis). Scope is stated correctly.")
fresh("M1-b-r20-delta-L05-255-256", "PASS",
      "L05.html:255-256 (canon-breaks bullets, changed): 'The rule that turns dates into years changes t, and so changes the factor. This "
      "lesson does not choose a rule.' and 'Each factor here applies one rate r to one time t.' Consistent with Remark 1.3 (L05 line 97ish: "
      "t is an input) and with Definition 1.1 (one r, one t per factor).")
fresh("M1-b-r20-cards-c088", "FAIL",
      "Card M1-c088 (cards.json:594-597, grade T): 'No. The semiannual factor is strictly smaller (Proposition 2.4) ...'. Proposition 2.4 "
      "(L05.html:131-133) is stated 'Assume E' and its proof uses the monotonicity of x to the t from (ii), which rests on E. The card "
      "states the T-grade result without the hypothesis, while card M1-c086 for the same proposition says 'under Assumption E' (scope "
      "inconsistency between cards).",
      "Change the back of M1-c088 to: 'No. Under Assumption E, the semiannual factor is strictly smaller (Proposition 2.4), so the two conventions give different discount factors at t = 5.'")
fresh("M1-b-r20-E-scope-remarks", "FAIL",
      "Two scope defects in remarks that cite Proposition 2.2 (which is stated under Assumption E). (1) L04.html:79 (Assumption E block) says E "
      "'is used in Proposition 2.2, in the places that cite that proposition (Lab 1, Problem R2, the key-results table, quiz item 5 and "
      "the misconception in §5), and directly in Problem R3', but Remark 2.3 (L04.html:111-113: 'Propositions 2.1 and 2.2 say that the "
      "factors rise with m and stay below e^r') cites Proposition 2.2 and is not in the list; the remark also drops E. (2) L05.html:126-128 "
      "Remark 2.3: 'Proposition 2.2 says that treating r as a continuous rate discounts more than treating r as an annual effective rate' "
      "omits the hypothesis 'Assume E' of Proposition 2.2 (L05.html:116-118). For r > 0, e^(-rt) < (1+r)^(-t) is equivalent to the "
      "inequality ln(1+r) < r, which is E, so the remark's claim carries E.",
      "L04.html line 79: add 'Remark 2.3' to the list of places (or write 'Under Assumption E' in Remark 2.3, line 112). L05.html "
      "Remark 2.3 (line 127): change to 'Under Assumption E, Proposition 2.2 says that treating r as a continuous rate discounts more ...'.")
fresh("M1-b-r20-L05-236-interp", "PASS",
      "L05.html:236 (interpretation, changed 'requires' -> 'states'): see M1-b-2.5-lab-L05 and M1-b-2.2-L05-numbers-recomputed; the printed "
      "table and checks support each claim.")

rows = []
for r in PREV["rows"]:
    i = r["id"]
    if i in FRESH:
        st, ev, fix = FRESH[i]
    else:
        st, ev, fix = "PASS", CARRY + " " + r["evidence"].split("): ", 1)[-1] if "Carried from round" in r["evidence"] else CARRY + " " + r["evidence"], ""
        if "Carried from round" in r["evidence"]:
            ev = CARRY + " " + r["evidence"].split("):", 1)[-1].lstrip()
    if i not in FRESH and r["status"] != "PASS":
        raise SystemExit("unexpected non-PASS carry " + i)
    row = {"id": i, "check": r["check"], "location": r["location"], "status": st, "evidence": ev}
    if fix:
        row["fix"] = fix
    rows.append(row)
extra = [i for i in FRESH if i not in {r["id"] for r in PREV["rows"]}]
for i in extra:
    st, ev, fix = FRESH[i]
    src = {"M1-b-r20-cards-c088": ("2.7 cards: card M1-c088 (L05) against Proposition 2.4", "cards.json:594-597; L05.html:131-133"),
           "M1-b-r20-E-scope-remarks": ("Scope of Assumption E in the remarks that cite Proposition 2.2", "L04.html:79, 111-113; L05.html:126-128"),
           "M1-b-r20-delta-L04-358-R2": ("2.2/2.4 delta: L04 R2 solution (changed line 358)", "course/modules/M/M1/L04.html:358"),
           "M1-b-r20-delta-L05-255-256": ("canon-breaks bullets (changed lines 255-256)", "course/modules/M/M1/L05.html:255-256"),
           "M1-b-r20-L05-236-interp": ("interpretation line 236 (changed)", "course/modules/M/M1/L05.html:236"),
           "M1-b-2.5-lab-L04-misc-261": ("misconception 3 (changed line 261)", "course/modules/M/M1/L04.html:261"),
           }[i]
    row = {"id": i, "check": src[0], "location": src[1], "status": st, "evidence": ev}
    if fix:
        row["fix"] = fix
    rows.append(row)

# ids for the new delta rows that re-verify lines already listed above
fragment = {
    "unit": "M1",
    "slice": "M1-b",
    "round": 20,
    "verifier": "independent verifier (Haiku), round 20",
    "pin": "fd9a9b72f000e509f3af78babf970cd4c9a847e4",
    "base": "51fa336 (round 19 pin; delta re-read: L04.html 244, 261, 358; L05.html 236, 255-256)",
    "previous_fragment": "/tmp/fanout-frags/M1-b.round19.json",
    "checkout": "/tmp/verify20-M1-b",
    "scratch": "/tmp/M1-v/M1-b-r20",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b is lessons L04 and L05 with their twins, not a project slice: no new student-error mutants, alternative "
        "implementations or mutant re-runs apply (same ruling as rounds 16-19). ledgers/M1/mutants/ holds the project mutants (slices a/c). "
        "Architect ruling on lab twins applied: the twins' outputs are checked against the embedded expected blocks, not mutated.",
        "Delta 51fa336..fd9a9b7 for this slice: L04.html lines 244, 261, 358 and L05.html lines 236, 255-256 (git diff -U0). "
        "cards.json, tests/labs/M1 and L03.html unchanged in this slice. The AC1 lab twin lab-AC1-L04-1.py changed; it is outside M1.",
        "Round 19 row M1-b-2.7-cards is still FAIL: card M1-c068 unchanged, Remark 1.3 condition still unreflected in the card. "
        "Round 20 adds M1-b-r20-cards-c088 (card drops Assumption E) and M1-b-r20-E-scope-remarks (Remark 2.3 in L04 and L05).",
        "Round 19 note correction: the L04 twin prints 27 lines (not 17); the L05 twin prints 13 lines.",
        "Not checked: no external source is cited or read in this slice (L04 and L05 cite no registry key); the registry check is a live "
        "sample (1 of 560 entries) plus the full offline integrity pass. Lab output is exact arithmetic (no SIMULATED data, no grade C "
        "basis from a simulation). Card M1-c180 (lesson L07) is outside this slice.",
    ],
    "summary": {},
}
pass_n = sum(1 for r in rows if r["status"] == "PASS")
fail_n = sum(1 for r in rows if r["status"] == "FAIL")
fragment["summary"] = {"rows": len(rows), "pass": pass_n, "fail": fail_n, "unverifiable": 0}
fragment["verdict"] = "PASS" if fail_n == 0 else "FAIL"
path = pathlib.Path("/tmp/verify20-M1-b/ledgers/M1/M1-b.json")
path.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n")
print(path, fragment["summary"], fragment["verdict"])
