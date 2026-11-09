# H1: builds ledgers/E2/E2-d.json (closing delta round 1, pin d9de2fe5, base 2a805c83) from the base fragment.
# Re-verified rows get fresh evidence; every other base PASS row is carried under the carry prefix.
import json, re, sys
from datetime import datetime, timezone
from pathlib import Path
root = Path(sys.argv[1])
base = json.loads(Path("/Users/billyribeiro/.fanout/frags/G-E2-d.round1.json").read_text(encoding="utf-8"))
D = "ledgers/E2/scripts/E2-d-r1/"
CARRY = ("Carried from round 1 (the cited subject is byte-identical since the previous pin 2a805c83; the only E2-slice "
         "files changed since then are course/modules/E/E2/cards.json entries E2-c102, E2-c105 and E2-c136):")
FRESH = {
 "gate-check-pages": ("PASS", "tools/check_pages.py --unit E2 re-run at d9de2fe5: 'check_pages E2: PASS', exit 0 (" + D + "H1_check_pages.out)."),
 "gate-check-dag": ("PASS", "tools/check_dag.py --unit E2 re-run at d9de2fe5: 'check_dag E2: PASS', exit 0 (" + D + "H1_check_dag.out)."),
 "gate-check-projects": ("PASS", "tools/check_projects.py --unit E2 re-run at d9de2fe5: 'check_projects E2: PASS', exit 0 (" + D + "H1_check_projects.out)."),
 "gate-mutate-graders": ("PASS", "tools/mutate_graders.py --unit E2 re-run (standing set, ruling 37): 'mutate_graders E2: PASS (64/64 killed)', exit 0 (" + D + "H1_mutate_graders_E2.out). No new mutants written."),
 "gate-run-labs-unit": ("PASS", "tools/run_labs.py --unit E2 re-run: 'run_labs E2: PASS (12/12)', exit 0 (" + D + "H1_run_labs_unit.out)."),
 "gate-ruff": ("PASS", "Repository gate re-run at d9de2fe5 (the delta touches other units' .py files): 'ruff check .' -> 'All checks passed!' exit 0 (" + D + "H1_ruff_check.out); 'ruff format --check .' -> '555 files already formatted' exit 0 (" + D + "H1_ruff_format.out)."),
 "gate-mypy": ("PASS", "Repository gate re-run: 'mypy --no-incremental' -> 'Success: no issues found in 386 source files', exit 0 (" + D + "H1_mypy.out)."),
 "gate-verify-refs-offline": ("PASS", "tools/verify_refs.py --offline re-run: 'offline integrity: 560 entries, 0 problems', exit 0 (" + D + "H1_verify_refs_offline.out)."),
 "gate-build-site-check": ("PASS", "tools/build_site.py --check re-run: 'site data current: 6 outputs', exit 0 (" + D + "H1_build_site_check.out). cards.json is a build input and the site data is current."),
 "proj-process-words": ("PASS", "Process-word scan (" + D + "H1_process_words.py, .out) of the three cards changed since 2a805c83: E2-c102, E2-c105, E2-c136 have no hits. Whole-file hits are the economic term 'Delta' and ordinary 'fixed' only, not process words. project.html, grader/ and tests/labs/E2/ are byte-identical since 2a805c83 (carried in their own rows)."),
 "cards-structure": ("PASS", "tools/check_pages.py --unit E2 PASS (check_cards: unique ids, lesson exists, valid grade, cite keys, C-grade basis). " + D + "H1_cards_delta.py/.out: 136 cards, 0 duplicate ids, 0 duplicate fronts, 0 C-grade cards without basis; ids added vs 2a805c83 = [E2-c136] only, ids removed = none; changed vs 2a805c83 = [E2-c102, E2-c105]."),
 "cards-structure-r9": ("PASS", "Same as cards-structure: tools/check_pages.py --unit E2 PASS and " + D + "H1_cards_delta.out (136 cards, no duplicate ids or fronts, no C-grade card without basis)."),
 "cards-numbers-in-lesson": ("PASS", D + "H1_cards_delta.out: every number in every card's front and back (136 cards, commas removed) appears in its lesson HTML text; 'number problems: 0'. This includes the changed cards E2-c102, E2-c105 and the new E2-c136 (26680000, -26620718, 59282, 6669, 52613, 79810, 1334, 20000, 1333, 1333.67, 0.66, -0.67, -0.66656253 all occur in L08.html, e.g. lines 135, 258, 263-265, 293, 365, 372)."),
 "cards-changed-discrete-EM": ("PASS", "Base FAIL re-verified from scratch. " + D + "H1_discrete_em.py/.out: E[M] for n=5, a=2000 from the Proposition 2.2 formula with Fractions = 85418692002000/64048012001 = 1333.6665625260364 (formula equals enumeration for n in 1..4, a in 0..3). E2-c098 value and fraction correct (1333.67; 1333.66656253); its pointer '(Remark 2.3)' is a LOW locator error: Remark 2.3 (L08.html line 112) is the continuous analogue, and the Proposition 2.2 sum is at line 99 (see notes). E2-c099 correct against Proposition 3.1 (L08.html lines 124-125, proof 129-130). E2-c100 correct: 1333 - E[M] = -0.66656 -> -0.67 (L08.html line 135). E2-c105 (changed) now reads 'Not in general. For n = 5 and a = 2000 cents, a shading of 1333 cents leaves -0.67 cents (-0.66656253 unrounded; Remark 3.2); whether a positive whole-cent shading suffices depends on E[M] (Proposition 3.1).' The front asks about a positive shading; a positive c leaves c - E[M] (Proposition 3.1, line 125), and c = 1333 < E[M] = 1333.67 leaves -0.67, so the claim is true and the base counterexample (n=2, a=1, where a 1-cent shading suffices) no longer contradicts it. The number is stated in L08.html line 135 and line 293 (the lesson's 'Any positive shading removes the winner's curse' is the wrong claim there)."),
 "cards-changed-c102": ("PASS", "New row (E2-c102 changed by d9de2fe5). Back now: '59282 cents, against an exact total of 6669 cents. The difference is again 52613 cents, which is 0.66 standard errors (Lab 1, Part C). SIMULATED, seed 20261028.' Locators: L08.html line 263 (shaded_winner_profit_total_cents 59282), line 265 (exact_shaded 6669), line 264 (standard error 79810); 59282 - 6669 = 52613 and 52613/79810 = 0.6592 -> 0.66 (" + D + "H1_shift_check.out). Grade C with basis 'Lab 1, Parts B and C (SIMULATED, seed 20261028)' matches ruling 13 for a simulated-lab total. The removed sentence (26680000) is now carried by E2-c136."),
 "cards-new-c136": ("PASS", "New row E2-c136 (appended, L08, grade C, basis Lab 1 Parts B and C). Arithmetic: 59282 - (-26620718) = 26680000 = 20000 x 1334 (" + D + "H1_shift_check.out). Per auction: re-running the L08 Lab 1 auction loop with seed 20261028 and the same draw order gives shaded minus naive profit = 1334 in all 20000 auctions (" + D + "H1_shift_check.out). The page's own run: tests/labs/E2/lab-E2-L08-1.py under python -I -W error exit 0, output equals the page's expected block (" + D + "H1_twin_L08.out; comparison printed True). The same statement is an exercise solution in L08.html line 365. No hypothesis is missing: the claim is about the printed simulated totals of the same seeded auctions."),
}
rows_out = []
seen = set()
for r in base["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in FRESH:
        st, ev = FRESH[rid]
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
    elif r["status"] == "PASS":
        rows_out.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                         "evidence": CARRY + " " + r["evidence"]})
    else:
        raise SystemExit("base non-PASS row not re-verified: " + rid)
for rid in ("cards-changed-c102", "cards-new-c136"):
    st, ev = FRESH[rid]
    rows_out.append({"id": rid, "check": "2.7-cards", "location": "course/modules/E/E2/cards.json " + rid,
                     "status": st, "evidence": ev})
# mutants: the standing set, from the H1 run
mutants = []
for line in Path(root / D / "H1_mutate_graders_E2.out").read_text(encoding="utf-8").splitlines():
    if not line.startswith("KILLED "):
        continue
    m = re.match(r"KILLED (\S+?): (.*) -> (.*) \(seed (\d+)\)$", line)
    if not m:
        raise SystemExit("unparsed mutant line: " + line)
    mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3) + " (seed " + m.group(4) + ")"})
notes = " ".join([
 "Closing delta round 1 (ruling 30) from base 2a805c83 (base fragment ~/.fanout/frags/G-E2-d.round1.json, FAIL on cards-changed-discrete-EM) to pin d9de2fe5.",
 "git diff --name-only 2a805c83..d9de2fe5 over the E2 slice paths: course/modules/E/E2/cards.json is the only changed file (L01-L09, project.html, index.html, grader/, tests/labs/E2/, ledgers/E2/mutants/, notation/, references/, tools/, plans/E2-build-plan.md are all byte-identical).",
 "The cards.json delta: E2-c102 back loses the sentence '1334 times 20000 ... 26680000' (moved to E2-c136); E2-c105 front and back rewritten (the base FAIL fix, ruling 26 kind 'over-graded / false universal claim' cleared); E2-c136 added (grade C, Lab 1 Parts B and C). E2-c098, c099, c100 are byte-identical to 2a805c83 and were re-verified because the base row was FAIL.",
 "Out-of-slice hunks (plans/FINAL-ARCHITECT-RULINGS.md rulings 38a/39/40, plans/E3-open-items.md, tests/labs/CS2, E3, E5, M3, M4, M6, SC1, CF8, BK4 and the ledgers of those units) are not in this slice; the repo-wide ruff, ruff format and mypy gates were re-run at d9de2fe5 and pass.",
 "Base FAIL cleared: cards-changed-discrete-EM now PASS. Base PASS rows whose subjects did not change are carried with the carry prefix; the two new row ids cards-changed-c102 and cards-new-c136 cover the changed and new cards.",
 "LOW finding (not a ruling-26 kind, so not a FAIL under ruling 30; defer to plans/KNOWN-ISSUES.md or fix in a later round at the parent's choice): the back of E2-c098 reads 'It is the Proposition 2.2 sum evaluated exactly with fractions (Remark 2.3).' Remark 2.3 (L08.html line 112) is the continuous analogue a(n-1)/(n+1); the discrete sum is Proposition 2.2 (line 99). Fix: change '(Remark 2.3)' to '(Proposition 2.2)'. The value and fraction are correct.",
 "Judgement calls (same convention as the base round): E2-c098, c099, c100 and c105 cite Proposition 3.1 with its hypothesis (Assumptions 1 and 2) not restated on the card; the model is stated on the same lesson and the n = 5, a = 2000 values are on the card (base judgement call 1 for E2-c088). E2-c098 and c105 rest on the exact value E[M] = 85418692002000/64048012001, evaluated by fractions from Proposition 2.2 (table row L08.html line 413, T); accepted as T on the same basis the base round used. E2-c136 is graded C although the per-auction shift is provable (T); C is the conservative grade and is not an over-grade.",
 "Not run this round (targeted rule): full pytest (tests/test_labs.py -k E2 carried, no test reads cards.json; grep of tests/*.py and tools/*.py finds cards only in tools/check_pages.py); run_graders and run_alternatives (grader/ and alt files byte-identical); page_smoke and the project twins under python -I -W error (project.html and tests/labs/E2/lab-E2-project-*.py byte-identical; only the L08 twin was run in isolation); blind exemplar scorers (no rubric or exemplar text changed in E2).",
])
out = {
 "unit": "E2", "slice": "d", "round": 1,
 "verifier": "Claude Haiku 5.5, independent verifier for E2-d, closing delta round 1 (did not build E2; checkout verifyH1-E2-d)",
 "pin": "d9de2fe5", "base": "G-E2-d.round1.json (pin 2a805c83; FAIL on cards-changed-discrete-EM)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyH1-E2-d",
 "scratch": "none outside the checkout; all runs in ledgers/E2/scripts/E2-d-r1/ (files prefixed H1_)",
 "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "PASS",
 "rows": rows_out,
 "mutants": mutants,
 "registry_flags": [], "freshness_flags": [],
 "notes": notes,
}
ok_mut = len(mutants) == 64 and all(m.get("killed_by") for m in mutants)
counts = {s: sum(1 for r in rows_out if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
out["verdict"] = "PASS" if (counts["PASS"] == len(rows_out) and ok_mut) else "FAIL"
out["summary"] = ("E2-d closing delta round 1 on pin d9de2fe5 (base 2a805c83): %d rows, %d PASS, %d FAIL, %d UNVERIFIABLE; "
                  "standing mutants %d/%d killed (no new mutants, ruling 37). Base FAIL cards-changed-discrete-EM cleared "
                  "(E2-c105 rewritten and checked). New rows cards-changed-c102 and cards-new-c136 PASS. "
                  "One LOW citation locator (E2-c098 '(Remark 2.3)' should be '(Proposition 2.2)') recorded in notes, not a ruling-26 kind."
                  % (len(rows_out), counts["PASS"], counts["FAIL"], counts["UNVERIFIABLE"], len(mutants), 64))
Path(root / "ledgers/E2/E2-d.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows_out), counts, "mutants", len(mutants), "verdict", out["verdict"])
print("base ids missing:", sorted(seen - {x["id"] for x in rows_out}))
