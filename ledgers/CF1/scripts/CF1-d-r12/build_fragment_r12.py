"""Round 12 CF1-d fragment builder: carries round-11 rows only where the cited subject is byte-identical, re-verified rows get new evidence."""
import json, re, sys
from pathlib import Path

ROOT = Path("/tmp/verify12-CF1-d")
prev = json.loads(Path("/tmp/fanout-frags/CF1-d.round11.json").read_text(encoding="utf-8"))
old = {r["id"]: r for r in prev["rows"]}

G = ("grader/test_project.py (its only change since 91946cf is the insertion of two functions at line 113; every cited "
     "function body is byte-identical, checked with git diff -U0)")
P = ("project.html (cited lines unchanged since 91946cf; the only hunks are lines 189-192 and 421, checked with git diff -U0)")
C = ("cards.json (the only entries changed since 91946cf are CF1-c027, c042, c068 and the new c101-c103; the cited cards are "
     "byte-identical)")
L = "the lesson, lab and index files cited (unchanged since 91946cf, checked with git diff --stat)"
PREFIX = {"G": G, "P": P, "C": C, "L": L}

def strip_chain(text):
    return re.sub(r"^(Carried from round \d+ \(.*?\):\s*)+", "", text, flags=re.S)

rows = []
def carry(rid, group, extra=""):
    r = dict(old[rid])
    r["status"] = "PASS"
    base = strip_chain(r["evidence"])
    r["evidence"] = f"Carried from round 11 ({PREFIX[group]}): {extra}{base}" if group in PREFIX else base
    r.pop("verdict", None)
    rows.append(r)

def fresh(rid, status, location, evidence, fix=None, check=None):
    r = {"id": rid, "check": check or old.get(rid, {}).get("check", rid), "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- fresh rows (re-run or re-read this round) ----
fresh("proj-exemplar-b-crossing-claim", "PASS",
      "course/modules/CF/CF1/project.html line 421 (Exemplar B, 1 Recommendation; sentence rewritten this round)",
      "Recomputed on the reference (ledgers/CF1/scripts/CF1-d-r12/recompute_r12.py output): NPV at 0.10 of [-9000, 3150, 4000, 5000] is 926.00; "
      "irr_roots returns [0.1531770302362352]; the NPV at 0.153177 is 0.0005, i.e. zero at the 1e-6 rate step. Analytic check of the new "
      "sentence: each t >= 1 term C_t/(1+r)^t with C_t > 0 falls strictly as r rises for r > -1 while the t = 0 term is constant, so NPV "
      "falls strictly; NPV tends to +infinity as r tends to -1 from above and to -9000 as r grows, so it crosses zero exactly once. "
      "Lab 3 prints the IRR root 0.153177 (twin output ledgers/CF1/scripts/CF1-d-r12/twin_lab-CF1-project-3.out).")
fresh("proj-exemplar-numbers", "PASS", "course/modules/CF/CF1/project.html lines 400-440 (Exemplar B sections 1-5)",
      "926.00 recomputed (npv at 0.10). Shield PV 750 * (1/1.1 + 1/1.21 + 1/1.331) = 1865.14 recomputed. Flows -9000, 3150, 4000, 5000 "
      "match Lab 1 step 6 in ledgers/CF1/scripts/CF1-d-r12/twin_lab-CF1-project-1.out. Working capital -600.00, -50.00, +650.00 match "
      "that output's nwc lines (nwc_1 = 600.00, nwc_2 = 650.00) and sum to zero. IRR 15.3177 percent and simple payback 2.37 "
      "and discounted 2.7535 years match twin_lab-CF1-project-3.out (0.153177, 2.370000, 2.753500).")
fresh("proj-hours-table", "PASS", "course/modules/CF/CF1/project.html lines 216-230 (time budget)",
      "Component hours 1 + 1 + 4 + 2 + 1 + 1 + 2 = 12, matching the stated total 12 and the 12-hour project; the total row cites 48 lesson hours "
      "and 12 project hours, which give the module's 60 hours (index.html line 29 data-hours-lessons 48, data-hours-project 12).")
fresh("proj-banned-phrases", "PASS", "course/modules/CF/CF1/project.html; course/modules/CF/CF1/cards.json; changed passages in L06.html lines 211 and 223",
      "Scripted scan of project.html and cards.json for roughly, about, historically, typically, usually, generally, ..., ellipsis, half, most, "
      "often, round, build, builder, verifier, REQUESTS and unit report. Hits: 'about 600 to 900 words' (length guidance, not a claim), "
      "'nothing about any company', 'a claim about what firms do', 'at most' (grading rule), 'half a period' (a card question), 'often firms use "
      "payback' (a card question whose answer is No). No banned claim phrase and no process word. The two changed L06 paragraphs were read: "
      "they contain no banned phrase.")
fresh("proj-structure-and-gates", "PASS", "tools/check_projects.py, tools/check_pages.py, tools/check_dag.py (CF1)",
      "check_projects CF1: PASS; check_pages CF1: PASS; check_dag CF1: PASS (ledgers/CF1/scripts/CF1-d-r12/check_*.out).")
fresh("proj-pytest-lab-helper", "PASS", "tests/labs/CF1/*.py; tools/run_labs.py",
      "run_labs CF1: PASS (9/9). Each CF1 twin run under python -I -W error exits 0 (ledgers/CF1/scripts/CF1-d-r12/twin_lab-*.out).")
fresh("proj-test-count-72", "PASS", "course/modules/CF/CF1/project.html line 192 (Grading mode); grader/test_project.py",
      "Page states 120 checks. pytest --collect-only on the reference (runone.py collect) gives 120 tests; the same count on seeds 0, 1, 7, 49 and 134675774 (collect_seeds.py).")
fresh("proj-grader-reference-50-seeds", "PASS", "course/modules/CF/CF1/grader; tools/run_graders.py",
      "run_graders CF1 --seeds 0-49: PASS (reference 50/50 seeds; ledgers/CF1/scripts/CF1-d-r12/graders.out).")
fresh("proj-page-smoke", "PASS", "course/modules/CF/CF1/project.html in-browser grader",
      "page_smoke --unit CF1 --pages project: PASS; in-browser grader: All 120 tests pass on seed 1393221784 (ledgers/CF1/scripts/CF1-d-r12/page_smoke_project.out).")
fresh("proj-verify-refs", "PASS", "tools/verify_refs.py; references/references.json",
      "verify_refs --offline: 560 entries, 0 problems. verify_refs --unit CF1 (live): 2 of 560 entries, 0 problems "
      "(ledgers/CF1/scripts/CF1-d-r12/verify_refs_*.out).")
fresh("proj-check-dag", "PASS", "tools/check_dag.py", "check_dag CF1: PASS (ledgers/CF1/scripts/CF1-d-r12/check_dag.out).")
fresh("proj-ruff-format", "PASS", "course/modules/CF/CF1/grader; tests/labs/CF1",
      "ruff check and ruff format --check on the grader and the labs: All checks passed; 13 files already formatted.")
fresh("proj-mypy-grader-gate", "PASS", "course/modules/CF/CF1/grader/*.py; tests/labs/CF1",
      "mypy --no-incremental on the grader and the labs: Success, no issues found in 13 source files.")
fresh("proj-collect-count-50-seeds", "PASS", "course/modules/CF/CF1/grader/test_project.py; course/modules/CF/CF1/project.html line 192",
      "Collect count 120 on five seeds (0, 1, 7, 49, 134675774); the count is seed-independent because every parametrize list is a literal (test_project.py parametrize lines 104, 257, 361, 366, 392, 490, 547, 726).")
fresh("proj-spec-count-118-hub", "PASS", "course/modules/CF/CF1/project.html line 192 (Grading mode)",
      "The page now says 120 checks; the collected count is 120 (see proj-test-count-72). The previous 118 is no longer stated anywhere in the project page.")
fresh("proj-count-cause-wording", "PASS", "course/modules/CF/CF1/project.html line 192 (Grading mode); grader/test_project.py parametrize lists",
      "The sentence says the count is taken with pytest --collect-only on the reference and does not depend on the seed because no parametrize list's length depends on the seed. Every parametrize list in test_project.py is a literal (lines 104, 257, 361, 366, 392, 490, 547, 726; the multi-line ones at 490 and 726 read as literal pytest.param entries). Collect count is 120 on five seeds (proj-collect-count-50-seeds).")
fresh("proj-hours-arithmetic-split", "PASS", "course/modules/CF/CF1/index.html lines 29-41; L01-L06 data-hours",
      "index.html data-hours-lessons 48 and data-hours-project 12; 60 module hours and 20.0 percent (12 / 60) on line 41. Each lesson has data-hours=\"8\" (six lessons, 48 hours). Project hours table sums to 12. The split agrees with the lesson hours.")
fresh("proj-mutants-killed", "PASS", "ledgers/CF1/mutants/ (95 files); tools/mutate_graders.py",
      "mutate_graders --unit CF1 --seeds 0-9: PASS (95/95 killed; ledgers/CF1/scripts/CF1-d-r12/mutate_all_r12.out). No survivor.")
fresh("proj-mutant-m58-zero-flow-time-index", "PASS",
      "ledgers/CF1/mutants/m58_npv_drops_zero_flows_from_the_time_index.py; course/modules/CF/CF1/grader/test_project.py lines 113-124 (new tests)",
      "Round 11 FAIL is closed. The builder added test_npv_keeps_a_zero_flow_in_its_time_index (npv(0.1, [-100, 0, 121]) == 0). m58 is now KILLED on seed 0 by test_npv_keeps_a_zero_flow_in_its_time_index (mutate_all_r12.out). Independent check: reference npv(0.1,[-100,0,121]) = -1.4e-14 and m58 would give 10.0.")
fresh("proj-mutants-round11-new", "PASS", "ledgers/CF1/mutants/m59_monte_carlo_reseeds_at_seed_plus_draw_index.py; m60_fisher_nominal_clamped_at_zero.py",
      "Both KILLED in mutate_all_r12.out (m59 by the seeded-stream test; m60 by test_fisher_round_trip_is_exact on seed 0).")
fresh("proj-alternatives-correct", "PASS", "ledgers/CF1/scripts/CF1-d-r9/alts/ (10 engines), ledgers/CF1/scripts/CF1-d-r12/alts/ (5 engines)",
      "All 10 round-9 engines and all 5 round-10, 5 round-11 and 5 round-12 engines pass the current grader on seeds 0-9 (run_alts_r12.py output; 25 engines). Alternatives include a different IRR grid (2001 points), a running discount factor, a rounding cutoff of 1e-12 in payback, split exponentials for the draw multiplier and a log1p Fisher form.")
fresh("proj-alternatives-round10", "PASS", "ledgers/CF1/scripts/CF1-d-r10/alts/ (alt_r10_1..5)",
      "Re-run on the current grader, seeds 0-9: all 5 PASS.")
fresh("proj-alternatives-round11", "PASS", "round-11 scratch engines (alt_r11_1..5, /tmp/CF1-v/d11/alts; copies not in the ledger)",
      "Re-run on the current grader, seeds 0-9: all 5 PASS.")
fresh("proj-equivalent-mutant-proof", "PASS", "ledgers/CF1/mutants/ (95 files)",
      "No equivalent mutant is kept: all 95 mutants are killed, so no equivalence proof is needed.")
fresh("cards-missing-grade-or-basis", "PASS", "course/modules/CF/CF1/cards.json (103 entries)",
      "Scripted: every card has a grade in {C, T} and a non-empty basis. Changed cards c027, c042, c068, c101, c102, c103 have grade C and basis 'Lab N (SIMULATED...)'.")
fresh("cards-duplicate-scan", "PASS", "course/modules/CF/CF1/cards.json",
      "Scripted: 103 ids, 0 duplicate ids, 0 duplicate fronts.")
fresh("cards-numbers-in-lesson", "PASS", "course/modules/CF/CF1/cards.json; lesson HTML and lab outputs",
      "Scripted: every number in every card back (103 cards) occurs in the lesson, project or index HTML text or in the lab output files (ledgers/CF1/scripts/CF1-d-r11/twin_lab-CF1-L0n-1.out). Checked by substring, not by context; the context checks are in the card rows below.")
fresh("cards-grade-semantics", "PASS", "course/modules/CF/CF1/cards.json",
      "Scripted: 74 T cards and 29 C cards. Every C card's basis is a lab (SIMULATED), a convention section (c002, c003, c014, c071, c096) or a section reference; no T card cites a lab. The convention cards are C with the convention as basis, as BLUEPRINT section 3 requires.")
fresh("cards-count-vs-plan", "FAIL", "plans/CF1-build-plan.md line 240; course/modules/CF/CF1/cards.json",
      "Recounted this round: 103 cards, per lesson L01 18, L02 17, L03 16, L04 20, L05 17, L06 15. The plan (line 240) says 'the planner expects four to six per lesson (one per definition, key result and misconception)'. Every lesson is 2.5 to 5 times that expectation. The round added three cards (c101-c103), which raises the count further.",
      fix="Architect to decide the per-lesson rule: either amend plans/CF1-build-plan.md line 240 to the count that the BUILDER_RULES section 7 rule produces, or remove cards that are not one fact each (the Lab 1 and Lab 2 restatements, c027 and c101 included) until the count meets the stated expectation.")
fresh("index-ladder-rung1-worked-example", "FAIL", "course/modules/CF/CF1/index.html line 151 (The project ladder, Worked example); course/modules/CF/CF1/project.html lines 42-44 and 56-131",
      "Re-verified (index.html unchanged since 91946cf). Hub line 151 says rung 1 is 'A year-1 worked after-tax operating cash flow and working-capital line on a small project ... Lab 2 prints the later years and the NPV of the same project.' The project page rung 1 (project.html lines 42-44) is Lab 1: a three-year SIMULATED machine project that prints every year's flow (twin_lab-CF1-project-1.out) and an NPV of 926.00 dollars at 10 percent. Lab 2 is the completion problem of the same project with three blanks. The hub's rung 1 description names the wrong exercise.",
      fix="Rewrite index.html lines 151-152: rung 1 = 'Lab 1 on the project page: a three-year SIMULATED machine project, each year's flow and the NPV at 10 percent (926.00 dollars)'; rung 2 = 'Lab 2 on the project page: the after-tax cash-flow line of that same project with its three blanks'.")
fresh("cards-changed-r12-c027-c042-c068-c101-c103", "PASS", "course/modules/CF/CF1/cards.json CF1-c027, c042, c068, c101, c102, c103",
      "c027 back 534.24 (L02 line 157; lab output line 269); 'paid in every scenario' is stated in L02 lines 296 and 379. c101 back -1,465.76 and 2,000.00 below the incremental NPV (lab output lines 270-271, L02 line 157). c042 back 113,637.49 at 3 percent and real NPV 263,709.14 (L03 line 261). c103 back 194,368.27 at 5 percent (L03 line 332). c068 back 2.750 years simple (L05 line 101; lab output line 193). c102 back 3.469 years discounted (L05 line 101; lab output line 193). Each card has grade C and a Lab 1 or Lab 2 basis; each card's number recomputes from the printed lab value.")
fresh("proj-process-words-r10", "PASS", "course/modules/CF/CF1/project.html; course/modules/CF/CF1/cards.json (scripted); L01.html and L02.html (unchanged)",
      "Scripted scan of project.html and cards.json for build, builder, round, verifier, REQUESTS and unit report: no hit in learner text.")
fresh("proj-mutants-round12-new", "PASS", "ledgers/CF1/mutants/r12d_01..r12d_05 (new this round); ledgers/CF1/scripts/CF1-d-r12/make_alts_and_mutants_r12.py",
      "Five new student-error mutants written this round, each KILLED on seed 0: r12d_01 shield dropped in the final year (test_depreciation_shield_is_depreciation_times_tax_rate); r12d_02 payback accepts a zero outlay (test_payback_rejects_a_first_flow_that_is_not_an_outlay[zero-outlay]); r12d_03 lognormal correction added instead of subtracted (test_monte_carlo_draws_follow_the_seeded_gauss_stream); r12d_04 NPV indexes from the last flow (test_npv_two_flow_closed_form); r12d_05 real flag deflates operating flows only (test_real_flows_are_deflated_year_by_year).")
fresh("proj-grader-new-tests-r12", "PASS", "course/modules/CF/CF1/grader/test_project.py lines 113-127 (test_npv_keeps_a_zero_flow_in_its_time_index, test_npv_keeps_a_leading_zero_flow_in_its_time_index)",
      "Both new assertions are spec-stated: the page's NPV bullet defines the sum over every t, so a zero flow keeps its time index. Values: npv(0.1, [-100, 0, 121]) = -1.4e-14 (zero within the close tolerance); npv(0.1, [0, 121]) = 110.0. Both pass the reference on seeds 0-9 and the 25 alternatives. m58 is killed by the first. The test messages state the arithmetic correctly (121 / 1.1 ** 2 = 100 at the second flow; 121 / 1.1 = 110).")
fresh("proj-npv-zero-flow-alternatives-r12", "PASS", "ledgers/CF1/scripts/CF1-d-r12/alts/alt_r12_1_npv_running_discount_factor.py",
      "A running-discount-factor NPV (no power per flow) passes both new tests and the rest of the suite on seeds 0-9: the test is not an over-constraint on the arithmetic route.")
fresh("cards-c101-c103-agreement", "PASS", "course/modules/CF/CF1/cards.json CF1-c101, c102, c103; L02, L03, L05 text",
      "Each new card's front asks for a number that the lesson prints (L02 line 157; L03 line 332; L05 line 101): the fronts match the lab outputs in the lesson text.")

# ---- carried rows (cited subject byte-identical since 91946cf) ----
for rid in ["proj-npv-empty-overconstraint", "proj-named-errors-untested", "proj-capex-negative-untested", "proj-must-raise-text-claim",
            "proj-error-message-unenforced", "proj-never-prints-or-mutates-unenforced", "proj-tangent-root-claim",
            "proj-tangent-endpoint-reported", "proj-mc-draw-method-unenforced", "proj-high-end-test-spec-justified",
            "proj-irr-window-unenforced", "proj-irr-window-end-intervals", "proj-tolerance-relative-only", "proj-tolerance-rationale",
            "proj-fisher-tolerance-zero-cases", "proj-window-end-high-unenforced", "proj-irr-window-high-end-cover",
            "proj-stdlib-and-no-instance-import-unenforced", "proj-grader-new-tests-r10", "proj-grader-new-tests-r11",
            "proj-tolerance-claim-note", "proj-tolerance-six-checks-enumerated", "proj-named-errors-tax-share-one",
            "proj-mc-mean-three-se-false-failure", "proj-tolerance-nine-recount"]:
    carry(rid, "G")
for rid in ["proj-capex-float-overconstraint", "proj-wc-timing-unenforced", "proj-exemplar-b-locator", "proj-rung1-step-line-wording",
            "proj-browser-storage-claim", "proj-spec-formulas-and-window", "proj-exemplar-a-quote", "proj-about-39-percent",
            "proj-registry-reading-list", "proj-registry-graham-glasserman", "proj-lessons-cross-ref", "proj-irr-close-roots-missed",
            "proj-ladder-skip-condition", "proj-exemplar-b-evidence-line", "proj-memo-rubric-caption", "proj-irr-grid-close-pair-example",
            "proj-unrounded-gap-claim", "proj-lab3-recomputed-numbers"]:
    carry(rid, "P")
carry("proj-irr-grid-convention-unenforced", "P", extra="cited lines 206-207 unchanged; line 192 changed only in the count, which this row does not cite; the grid example was recomputed this round (-100, 220.1, -121.11 returns [], -100, 221, -122.1 returns [0.1, 0.11]). ")
for rid in ["proj-mutant-tangent-survivor", "proj-mutants-round4-new", "proj-mutants-round5-new", "proj-mutants-round6-new",
            "proj-mutants-round7-new", "proj-mutants-round8-new", "proj-mutants-round9-new", "proj-mutants-round10-new",
            "proj-sign-changes-convention", "proj-two-root-witness", "proj-lab1-twin-output", "proj-lab2-completion-twin",
            "proj-lab3-sanity-run", "proj-lab2-docstring-claim"]:
    carry(rid, "L", extra="labs and mutant files unchanged; labs re-run this round (exit 0) and mutants re-run (95/95 killed); ")
for rid in ["cards-misconception-locator", "cards-cite-keys-and-locators", "cards-arithmetic-recomputed", "cards-lab-derived-numbers",
            "cards-prose-garbled-c067", "cards-changed-c014-c037-c047-c057", "cards-changed-c016-c044-c051-c052",
            "cards-c080-positive-variance-dropped", "cards-changed-c071-c084", "cards-changed-c071-lesson-agreement",
            "cards-c065-payback-basis", "cards-c012-npv-falls-scope", "proj-cards-c071-not-established"]:
    carry(rid, "C")
for rid in ["lesson-l01-conventional-rewrites", "lesson-l02-rewrites", "lesson-l05-rewrites", "index-card-and-hub-wording",
            "lesson-l02-canon-earnings-claim", "lesson-l02-why-section3-ref", "lesson-l02-r1-same-period-fraction",
            "lesson-l02-references-concept-claim", "lesson-l02-accrual-definition"]:
    carry(rid, "L")
carry("lesson-l06-rewrites", "L", extra="the cited L06 lines 129, 138 and 147 are outside the changed hunks (lines 211 and 223); ")

ids = [r["id"] for r in rows]
missing = [rid for rid in old if rid not in ids]
print("missing previous ids:", missing)
frag = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 12,
    "verifier": "independent verifier (Haiku), round 12 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json)",
    "pin": "aebdc15 (detached, /tmp/verify12-CF1-d)",
    "base": "91946cf (round-11 pin); delta computed with git diff --stat and git diff -U0 91946cf aebdc15",
    "checkout": "/tmp/verify12-CF1-d",
    "scratch": "/tmp/CF1-v/d12",
    "verified_at": "2026-10-28",
    "verdict": "",
    "rows": rows,
}
print("rows:", len(rows), "non-PASS:", [r["id"] for r in rows if r["status"] != "PASS"])
out = ROOT / "ledgers/CF1/CF1-d.json"

mutants = []
for line in Path("/tmp/verify12-CF1-d/ledgers/CF1/scripts/CF1-d-r12/mutate_all_r12.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({"file": f"ledgers/CF1/mutants/{name}", "description": desc,
                    "killed_by": killed if status == "KILLED" else None})
frag["mutants"] = mutants
frag["verdict"] = "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS"
frag["registry_flags"] = [
    "glasserman2003monte: used_by lists M8 only; CF1 cites it (project.html Exemplar B section 5, L06 Remark 2.4, cards CF1-c084). references/references.json is unchanged since 91946cf; add CF1 with tools/add_reference.py or confirm the architect's ruling.",
    "damodaran2012investment: used_by lists CF4 only; CF1 lists it in the project reading list (project.html reading section). references/references.json is unchanged since 91946cf.",
]
frag["freshness_flags"] = []
frag["notes"] = (
    "Delta 91946cf..aebdc15 for this slice: project.html lines 189-192 (test count 118 to 120) and 421 (Exemplar B recommendation sentence); "
    "grader/test_project.py one insertion at line 113 (two npv zero-flow tests, 14 lines); cards.json CF1-c027, c042, c068 text changed and "
    "c101-c103 added (103 cards); ledgers/CF1/mutants gained fix11_02..fix11_11 and m58-m60 (all in the mutant list, all killed). "
    "Commands run this round (outputs in ledgers/CF1/scripts/CF1-d-r12/): check_projects, check_pages, check_dag (CF1 PASS); run_labs CF1 (9/9); "
    "each CF1 twin under python -I -W error (exit 0, outputs saved); run_graders CF1 --seeds 0-49 (50/50); runone.py collect (120) and "
    "collect_seeds.py (120 on five seeds); mutate_graders CF1 --seeds 0-9 (95/95 killed); page_smoke CF1 project (in-browser 120/120); "
    "ruff check and format --check; mypy --no-incremental on grader and labs; verify_refs --offline (560, 0 problems) and --unit CF1 (2 of 560, 0 problems); "
    "25 alternative engines (r9 10, r10 5, r11 5, r12 5) on seeds 0-9, all pass; five new mutants r12d_01..05, all killed. "
    "Not checked: the full repository gate; pytest outside CF1; the L06 changed passages (lines 211 and 223, other slice) beyond the banned-phrase read; "
    "the other lessons' prose beyond the cited rows; the hours beyond arithmetic (architect ruling: design targets); live checks beyond CF1 registry entries; "
    "the test count change (118 to 120) is confirmed by collection and by the diff, not by re-reading every carried test body."
)
frag["summary"] = (
    f"CF1-d round 12: {frag['verdict']}. Rows {len(rows)}: PASS {sum(r['status'] == 'PASS' for r in rows)}, "
    f"non-PASS {sum(r['status'] != 'PASS' for r in rows)} (cards-count-vs-plan, index-ladder-rung1-worked-example). "
    f"Mutants {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed; the round-11 survivor m58 is now killed by the new test. "
    "Five new student-error mutants (r12d_01..05) killed; five new alternative engines pass; 25 engines in total pass."
)
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "mutants", len(mutants))
