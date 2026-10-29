"""Build ledgers/CF1/CF1-d.json for round 25: carry byte-identical PASS rows, re-run the command families, re-verify cards.json."""
import json, re, subprocess
CHK = "/tmp/verify25-CF1-d"
PREV = json.load(open("/tmp/fanout-frags/CF1-d.round24.json"))
OUT = f"{CHK}/ledgers/CF1/CF1-d.json"
R = f"{CHK}/{'ledgers/CF1/scripts/CF1-d-r25/out'}"
PIN_PREV = "23cbd6a"

FRESH_CARDS = {
    "cards-grade-semantics": "Re-verified round 25 on the new cards.json: CF1-c110 is now grade T with basis 'Problem R3, values on L01 line 446 (Assumption 4.0 and Remark 4.3)'. The R3 arithmetic recomputed: 1.05/1.06 - 1 = -0.009433962 (page -0.0094, -0.009434...) and 1.05/1.03 - 1 = +0.019417476 (page +0.019417...). The claim the card states (the decision can change with the rate that applies) is the one proved by the R3 instance and listed as T at L01 line 466 ('the one instance in Problem R3 flips sign between the two rates'). Grade counts 60 T and 50 C (out/cards_check.out). The round-24 FAIL is fixed.",
    "cards-c110-content": "Re-verified round 25: CF1-c110 front and back agree with L01.html lines 119-125 (Assumption 4.0 'At every period the owner can lend or borrow any amount at the rate r'), line 323 (one-rate market is an assumption; Problem R3 shows the decision can change), line 342 and line 148 (Remark 4.3 'Problem R3 shows what the rule does when the two rates differ'). Basis cites line 446 where the values are printed. Out/cards_check.out.",
    "cards-missing-grade-or-basis": "Re-run round 25 (out/cards_check.out): 110 entries; every entry has id, lesson, front, back, grade, and a cite or basis; grade values only T (60) or C (50).",
    "cards-duplicate-scan": "Re-run round 25 (out/cards_check.out): 110 unique ids; no duplicate front and no duplicate back across the 110 entries.",
    "cards-count-vs-plan": "Re-run round 25 (out/cards_check.out): per-lesson counts L01 19, L02 18, L03 17, L04 23, L05 18, L06 15 (sum 110). Plan section 12 requires at least one card per lesson and no fixed number; every lesson has at least 15.",
    "cards-count-r19": "Superseded by the round-25 count: cards.json now has 110 entries (60 T, 50 C), out/cards_check.out. The round-19 count of 109 predates CF1-c110.",
    "r15-cards-numbers-and-grades": "Superseded by the round-25 count: cards.json now has 110 entries, 60 T and 50 C (out/cards_check.out); the round-15 count of 103 entries predates later additions.",
    "r21-cards-count-and-fields": "Re-run round 25 (out/cards_check.out): 110 entries, all fields present, grades T or C only.",
    "r24-cards-count-and-fields": "Re-run round 25 (out/cards_check.out): 110 entries, 60 T and 50 C; the round-24 count of 59 T and 51 C changes only because CF1-c110 is now T.",
    "r24-banned-process-scan": "Re-run round 25 (out/cards_check.out): banned phrases and process words (roughly half, about 6%, historically, ellipsis, builder, verifier, round) over all 110 cards: none found.",
    "r15-banned-phrase-scan": "Re-run round 25 (out/cards_check.out): the same scan over all 110 cards: none found.",
    "r16-banned-process-words-scan": "Re-run round 25 (out/cards_check.out): the same scan over all 110 cards: none found.",
    "proj-banned-phrases": "Project page part carried from round 24 (course/modules/CF/CF1/project.html byte-identical since 23cbd6a). Cards part re-run round 25 (out/cards_check.out): none found in 110 cards.",
    "cards-numbers-in-lesson": "Carried from round 24 (course/modules/CF/CF1/cards.json entries other than CF1-c110 byte-identical since 23cbd6a; the only changed entry in 23cbd6a..b49a857 is CF1-c110, whose back text is unchanged and whose numbers are none beyond the labels Remark 4.3 and Problem R3, both present at L01.html lines 147 and 442).",
}

# Command families re-run this round; the evidence names the output file.
FRESH_CMD = {}
def fam(ids, text):
    for i in ids:
        FRESH_CMD[i] = text

MUT = ("Re-run round 25: mutate_graders --unit CF1 --seeds 0-9 killed all 227 mutants present at its start (out/mutate_all.out: 'mutate_graders CF1: PASS (227/227 killed)', EXIT 0); the four new round-25 mutants v25d_01..04 were run separately with run_mut_one.sh and each is KILLED on seed 0 (out/mutate_v25d_new.out). Total top-level mutant files now 231.")
ALT = "Re-run round 25: run_alts25.py over all 52 unique alternative engines (71 files, rounds 8 to 25) on seeds 0-9; all 52 PASS (out/alts25.out). The three new engines r25_a, r25_b, r25_c are among them (ledgers/CF1/scripts/CF1-d-r25/alts/)."
COLL = "Re-run round 25: collect-only on the reference engine, seeds 0-10 and 49: 157 tests collected on every seed (out/collect.out); project.html line 192 says 157."
GRD = "Re-run round 25: tools/run_graders.py --unit CF1 --seeds 0-49: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)', EXIT 0 (out/run_graders.out)."
GATE = "Re-run round 25: check_pages.py --all, check_dag.py --all, check_projects.py --all, page_smoke.py --unit CF1 (project, index, concepts, review and CF1 summary PASS), ruff check and format --check on grader and labs, mypy --no-incremental on the repository (Success: no issues found in 153 source files) (out/*.out; exit codes 0)."
LABS = "Re-run round 25: run_labs.py --unit CF1: 9/9 PASS; the three project twins run under python -I -W error with exit 0 and empty stderr (out/twin_project_1..3.out and .err)."
REFS = "Re-run round 25: verify_refs.py --offline: 560 entries, 0 problems; verify_refs.py --unit CF1 (live): 2 of 560 entries, 0 problems (out/verify_refs_offline.out, out/verify_refs_live_unit.out)."
PYT = "Re-run round 25: pytest tests/test_labs.py tests/test_refs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_run_labs.py: all dots, EXIT 0 (out/pytest.out)."
HRS = "Re-run round 25 (arithmetic): hub data-hours-lessons 48 equals 6 lessons x data-hours 8 (L01-L06); hub and project data-hours-project 12; project time-budget table 1+1+4+2+1+1+2 = 12; total 60."

fam(["proj-mutants-killed", "proj-mutant-m58-zero-flow-time-index", "proj-mutants-round11-new", "proj-mutants-round4-new", "proj-mutants-round5-new",
     "proj-mutants-round6-new", "proj-mutants-round7-new", "proj-mutants-round8-new", "proj-mutants-round9-new", "proj-mutants-round10-new",
     "proj-mutants-round12-new", "proj-mutants-round17-new", "proj-mutants-round18-new", "proj-mutants-round19-new", "proj-mutants-r23-new",
     "proj-mutant-tangent-survivor", "proj-mutant-d19-m01-irr-zero-outlay-refused", "r13-mutant-r13v-04-fisher-rounding", "r13-mutants-r13d-killed",
     "r13-mutants-full-run", "r14-mutant-r14v-01-rate-above-one-read-as-percent", "r15-mutants-r15e-new", "r16-mutants-new-three", "r16-mutants-full-run",
     "r20-mutants-new-seven", "r20-mutants-full-run", "r21-mutants-new-four", "r21-mutants-full-run", "r22-mutants-new-four", "r22-mutants-full-run",
     "r24-mutants-full-run", "r24-mutants-new-five", "r24-mutants-count", "cmd-mutate-graders-r17", "cmd-mutate-graders-r18", "cmd-mutate-graders-r19"], MUT)
fam(["proj-alternatives-correct", "proj-alternatives-round10", "proj-alternatives-round11", "proj-npv-zero-flow-alternatives-r12", "proj-alternatives-round17-new",
     "proj-alternatives-round18-new", "proj-alternatives-rerun-all-prior-r18", "proj-alternatives-round19-new", "proj-alternatives-rerun-all-r19",
     "proj-alternatives-r23-new-engines", "r13-alternatives-new", "r13-prior-alternatives-rerun", "r14-alternatives-new", "r15-alternatives-three-new",
     "r15-alternatives-rerun-all-prior", "r16-alternatives-three-new", "r16-alternatives-rerun-all-prior", "r20-alternatives-three-new",
     "r20-alternatives-all-unique", "r21-alternatives-three-new", "r21-alternatives-all-unique", "r22-alternatives-three-new", "r22-alternatives-all-unique",
     "r24-alternatives-three-new", "r24-alternatives-all-unique"], ALT)
fam(["proj-collect-count-50-seeds", "proj-test-count-72", "proj-spec-count-118-hub", "proj-collect-154-r19", "r13-collect-count-126", "r15-page-count-138",
     "r16-collect-count-138", "r20-collect-157-seeds", "r21-collect-157-seeds", "r22-collect-count-seeds", "r24-collect-157", "proj-count-cause-wording",
     ], COLL)
fam(["proj-grader-reference-50-seeds", "r13-run-graders-50", "r21-run-graders-50", "r22-run-graders-50", "r24-run-graders-50", "cmd-run-graders-r19"], GRD)
fam(["proj-structure-and-gates", "proj-check-dag", "proj-ruff-format", "proj-mypy-grader-gate", "proj-page-smoke", "proj-page-smoke-r19", "proj-gates-ruff-mypy-r19",
     "r16-run-gates", "r20-gate-set", "r21-gates-checkers", "r21-ruff-mypy", "r21-page-smoke", "r22-gates-checkers", "r22-ruff-mypy", "r22-page-smoke-project",
     "r24-gates", "cmd-gates-r18", "cmd-check-gates-r19"], GATE)
fam(["proj-pytest-lab-helper", "proj-lab1-twin-output", "proj-lab2-completion-twin", "proj-lab3-sanity-run", "proj-lab-twins-isolated-r18", "proj-lab-twins-r19",
     "r13-twins-under-python-I-W-error", "r20-labs-pytest-and-twins", "r21-run-labs-and-twins", "r22-labs-pytest-twins", "r24-twins-isolated",
     "cmd-run-labs-r19"], LABS)
fam(["proj-verify-refs", "r16-live-registry-refs", "r20-registry-and-verify", "r21-verify-refs", "r22-verify-refs", "r24-verify-refs", "cmd-verify-refs-live-r17",
     "cmd-verify-refs-r19"], REFS)
fam(["proj-hours-table", "proj-hours-arithmetic-split", "r20-hub-hours-arithmetic", "r21-hours-arithmetic", "r22-hours", "r24-hours-arithmetic"], HRS)
fam(["r13-run-graders-50"], GRD)  # already above; idempotent
fam(["r16-collect-count-138"], COLL)

NEW_ROWS = [
    ("r25-delta-coverage", "2.9 / delta: round-24 pin 23cbd6a to round-25 pin b49a857, slice d", "git diff --stat 23cbd6a b49a857 -- course/modules/CF/CF1 tests/labs/CF1 ledgers/CF1 (47 files)",
     "PASS", "Only one slice file changed: course/modules/CF/CF1/cards.json (one hunk, entry CF1-c110: grade C to T, basis rewritten). project.html, grader/, tests/labs/CF1/, references/, tools/, index.html and L01-L06 are byte-identical to 23cbd6a (git diff --quiet). Changed hunks read in full (git diff 23cbd6a b49a857 -- course/modules/CF/CF1/cards.json)."),
    ("r25-mutants-v25d-new-four", "2.5 / mutation: four new student-error mutants of the project grader (round 25)", "ledgers/CF1/mutants/v25d_01..v25d_04 (generator ledgers/CF1/scripts/CF1-d-r25/make_mutants25.py)",
     "PASS", "v25d_01 payback with rate>0 ignores the rate (KILLED seed 0 by test_discounted_payback_uses_discounted_flows); v25d_02 Fisher adds the two rates (KILLED seed 0 by test_fisher_round_trip_is_exact); v25d_03 Monte Carlo without the -vol^2/2 correction (KILLED seed 0 by test_monte_carlo_draws_follow_the_seeded_gauss_stream); v25d_04 negative tax floored at zero (KILLED seed 0 by test_single_year_project_has_no_working_capital). Each is a student error the page states (Conventions: payback discounting; Fisher identity; Monte Carlo correction; 'A negative tax is a credit')."),
    ("r25-alternatives-three-new", "2.5 / over-constraint: three new correct alternative engines (round 25)", "ledgers/CF1/scripts/CF1-d-r25/alts/r25_a_multiplicative_grid_accumulation.py, r25_b_horner_npv_reversed.py, r25_c_payback_fsum_prefix.py",
     "PASS", "r25_a builds the 4,001-point log grid by accumulating a constant ratio (valid: the page says sampled evenly in log x); r25_b computes NPV by a Horner recursion from the last flow (equal to the sum by algebra); r25_c computes payback cumulatives with math.fsum over prefixes. Each passes the 157-test suite on seeds 0-9 (out/alts25.out)."),
    ("r25-collect-157-seeds", "2.9 / test count: page count equals the collected count, seeds 0-10 and 49", "course/modules/CF/CF1/project.html line 192; grader/test_project.py; ledgers/CF1/scripts/CF1-d-r25/collect_seeds.sh",
     "PASS", "157 tests collected on each of seeds 0 to 10 and 49 (out/collect.out); project.html line 192 says 157."),
    ("r25-cards-count-and-grades", "2.7 cards: count, grades, fields and duplicates after the CF1-c110 change", "course/modules/CF/CF1/cards.json; ledgers/CF1/scripts/CF1-d-r25/cards_check_r25.py (out/cards_check.out)",
     "PASS", "110 entries, 110 unique ids, 60 T and 50 C, no missing field, no duplicate front or back, no banned or process word (out/cards_check.out)."),
    ("r25-spot-recompute-lab3-and-rung1", "2.2 numbers: rung-1 NPV, paybacks, Fisher, IRR, Monte Carlo counts printed by the project lab 3 twin", "tests/labs/CF1/lab-CF1-project-3.py (out/twin_project_3.out); reference.py via python -I (round 25 spot check)",
     "PASS", "Recomputed by hand: NPV at 0.10 = -9000 + 3150/1.1 + 4000/1.21 + 5000/1.331 = 926.00; discounted payback = 2 + 2830.58/3756.57 = 2.7535; simple payback = 2 + 1850/5000 = 2.37; [-100,60,60] payback 1.666667; Fisher 1.05 x 1.03 - 1 = 0.0815. The reference IRR on the rung-1 flows gives 0.153177. IRR of [-100,220.1,-121.11] is [] and of [-100,221,-122.1] is [0.1, 0.11], matching the page's example. 787 of 2000 draws negative = 39.35 percent, matching project.html line 374."),
    ("r25-hours-and-page-count", "2.9 hours: hub split and project budget", "course/modules/CF/CF1/index.html line 29; project.html lines 33, 216-230",
     "PASS", "Hub data-hours-lessons 48 = 6 x 8 (L01 to L06 each data-hours 8); data-hours-project 12 = table 1+1+4+2+1+1+2."),
]

rows = []
carried_prefix = "Carried from round 24 (course/modules/CF/CF1/project.html, grader/, tests/labs/CF1/, references/, tools/, index.html and L01-L06 byte-identical since the round-24 pin 23cbd6a; cards.json entries other than CF1-c110 unchanged): "
for r in PREV["rows"]:
    rid = r["id"]
    if rid == "cards-grade-semantics" or rid in FRESH_CARDS:
        text = FRESH_CARDS[rid]
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": text})
        continue
    if rid in FRESH_CMD:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": FRESH_CMD[rid]})
        continue
    if rid == "r24-cards-count-and-fields":
        continue  # handled above
    if "c110" in (r["location"] + r["check"]):
        raise SystemExit(f"row {rid} cites CF1-c110 and needs a fresh entry")
    if "cards" in (r["id"] + r["check"] + r["location"]).lower():
        ev = ("Carried from round 24 (course/modules/CF/CF1/cards.json entries cited here are byte-identical since 23cbd6a; "
              "the only changed entry in 23cbd6a..b49a857 is CF1-c110): " + r["evidence"].replace("Carried from round 24", "carried earlier"))
    else:
        ev = "Carried from round 24 (" + "byte-identical since 23cbd6a" + "): " + r["evidence"]
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": ev})

for rid, check, loc, status, ev in NEW_ROWS:
    rows.append({"id": rid, "check": check, "location": loc, "status": status, "evidence": ev})

# The round-24 FAIL row cards-grade-semantics is now PASS (kept by id above).
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert {r["id"] for r in PREV["rows"]} <= set(ids), "a previous row id was dropped"

mutants = []
for line in open(f"{R}/mutate_all.out", encoding="utf-8"):
    m = re.match(r"KILLED (\S+?): (.*) -> (\S+) \(seed (\d+)\)", line.strip())
    if m:
        mutants.append({"file": f"ledgers/CF1/mutants/{m.group(1)}", "description": m.group(2), "killed_by": f"{m.group(3)} (seed {m.group(4)})"})
for line in open(f"{R}/mutate_v25d_new.out", encoding="utf-8"):
    m = re.match(r"KILLED (\S+?): (.*)", line.strip())
    if m:
        pass
new_desc = {
    "v25d_01_payback_ignores_discount_rate.py": "v25d_01: payback with rate > 0 ignores the rate and returns the simple payback.",
    "v25d_02_fisher_adds_the_two_rates.py": "v25d_02: Fisher conversion adds the two rates (real + inflation) instead of the exact identity.",
    "v25d_03_monte_carlo_no_mean_one_correction.py": "v25d_03: Monte Carlo multiplier omits the - volatility**2 / 2 correction, so E[m] is not one.",
    "v25d_04_negative_tax_floored_at_zero.py": "v25d_04: a negative tax is floored at zero, so a loss gives no credit.",
}
for line in open(f"{R}/mutate_v25d_new.out", encoding="utf-8"):
    m = re.match(r"KILLED (v25d_\S+?\.py) seed (\d+): FAILED (\S+)", line.strip())
    if m:
        mutants.append({"file": f"ledgers/CF1/mutants/{m.group(1)}", "description": new_desc[m.group(1)], "killed_by": f"{m.group(3)} (seed {m.group(2)})"})
assert len(mutants) == 231, len(mutants)

rows_fail = [r for r in rows if r["status"] != "PASS"]
verdict = "PASS" if not rows_fail else "FAIL"
frag = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 25,
    "verifier": "independent verifier (Haiku), round 25 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
    "pin": "b49a857 (detached, /tmp/verify25-CF1-d)",
    "base": "23cbd6a (round-24 pin; git diff --stat 23cbd6a b49a857 touches only course/modules/CF/CF1/cards.json in this slice)",
    "checkout": CHK,
    "scratch": "/tmp/CF1-v/d25",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": PREV["registry_flags"],
    "freshness_flags": [],
    "notes": ("Round 25 delta for this slice: course/modules/CF/CF1/cards.json only (entry CF1-c110 grade C with basis 'Assumption 4.0 and Remark 4.3; Problem R3' changed to grade T with basis 'Problem R3, values on L01 line 446 (Assumption 4.0 and Remark 4.3)'). "
              "The round-24 FAIL (cards-grade-semantics) is fixed: the claim is proved by the Problem R3 instance on L01.html line 446, listed as T at line 466. "
              "Re-run this round: check_pages, check_dag, check_projects, run_graders 0-49 (CF1 50/50), page_smoke, ruff, mypy (repository), pytest (five files), verify_refs offline and live, run_labs (9/9), twins under python -I -W error, collect-only on seeds 0-10 and 49 (157), all 227 earlier mutants on seeds 0-9 (227/227 killed), four new mutants v25d_01..04 (killed), 52 unique alternatives on seeds 0-9 (52 pass, three new). "
              "Carried (byte-identical since 23cbd6a): every other round-24 PASS row about project.html, grader, labs, index, lessons, references, and the cards entries other than CF1-c110. "
              "Not re-derived this round: the lesson-number rows carried from earlier rounds whose round-22 evidence is terse ('see evidence', e.g. r21-e1-e2-arithmetic, r22-l06-line106-recomputed-numbers); their subjects are byte-identical, so they are carried by the rule, not re-computed. "
              "Not re-read in full this round: project.html (476 lines) and test_project.py (967 lines); the delta does not touch them, and the spec lines 180-240 and reference.py were read in full this round. Not run: the live web reads (none cited by changed rows); the full repository pytest (only the five files that cover this unit)."),
    "summary": (f"CF1-d round 25 (pin b49a857): {len(rows)} rows, {len(rows_fail)} non-PASS; mutants {len(mutants)} of {len(mutants)} killed; "
                "alternatives 52 of 52 unique pass on seeds 0-9 (3 new); collect 157 on every tested seed; run_graders 50/50; gates PASS. "
                "The round-24 FAIL (cards-grade-semantics, CF1-c110) is fixed."),
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(rows), "non-PASS", len(rows_fail), "mutants", len(mutants), "verdict", verdict)
