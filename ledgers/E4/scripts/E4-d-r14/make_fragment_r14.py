"""Build ledgers/E4/E4-d.json for round 14 (carry rule, fresh overrides, mutate output)."""
import json, re, sys
sys.path.insert(0, "/tmp/e4d14/frag")
from overrides_r14 import O, S
from fix_overrides_r14 import FIX
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE14-E4-d"
PIN = "8e5751c903f0246115eba746afdf5d71f612bb37"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-E4-d.round13.json"))
for k, (st, ev) in FIX.items():
    O[k] = (st, ev, None)
CARRY_OK = {
    "E4d2-exemplar-B-C1-annotation": "project.html:604-611",
    "E4d3-atlas-studios-na": "atlas/, studios/",
    "E4d6-alt-extra-damped": "ledgers/E4/scripts/E4-d-r6/candidates/damped_fixed_point_log_r6.py",
    "E4d6-stop-rule-measured": "course/modules/E/E4/grader/reference.py:22-23,:138; ledgers/E4/scripts/E4-d-fix-r11/logs/check_corner_*",
    "E4d8-tiny-root-reference": "course/modules/E/E4/grader/reference.py",
    "E4d10-l06-dependency": "course/modules/E/E4/L06.html:57,:66,:169; course/modules/E/E4/L07.html:62",
    "E4d11-alt-closed-form": "ledgers/E4/scripts/E4-d-r11/alts/alt_r11_a.py",
    "E4d12-alt-variants-new": "ledgers/E4/scripts/E4-d-r12/alts/alt_r12_a.py, alt_r12_b.py, alt_r12_c.py",
}
UNVER = {
 "E4d-exemplar-A-calibration": ("project.html:537-601 (Exemplar A) with data-scores 2,2,1,2,1", "An independent verifier who has not read the Exemplar A annotations or data-scores (project.html:537-601) scores Exemplar A blind on C1-C5 and compares within one level per criterion."),
 "E4d-exemplar-B-calibration": ("project.html:602-661 (Exemplar B) with data-scores 4,4,4,4,4", "An independent verifier who has not read the Exemplar B annotations or data-scores (project.html:602-661) scores Exemplar B blind on C1-C5 and compares within one level per criterion."),
 "E4d4-calibration-blind": ("project.html:537-601 (Exemplar A)", "Independent blind scoring of Exemplar A (see E4d-exemplar-A-calibration)."),
 "E4d5-calibration-B-blind": ("project.html:602-661 (Exemplar B)", "Independent blind scoring of Exemplar B (see E4d-exemplar-B-calibration)."),
 "E4d8-alternatives-r8": ("ledgers/E4/alternatives/alt_r8_a.py, alt_r8_b.py (round 8)", "Retire the round-8 citation (no current file cites alt_r8_a or alt_r8_b) or restore both files at a pin."),
 "E4d9-alternatives-v9": ("ledgers/E4/alternatives/alt_v9_1_interior_gap_zero.py, alt_v9_2_log_space.py, alt_v9_3_grid_then_bisect.py (round 9)", "Retire the round-9 citation or restore the three files at a pin."),
}
UNVER_EVIDENCE = ("Not blind-scorable this round. The verifier printed Exemplar A's annotations and the data-level attributes of both exemplars (project.html:537-661) while reading the report, and the round-13 fragment states the data-scores, so no blind score can be recorded. A rubric-only reading of the memo text gives A = 2,2,1,2,1 and B = 4,4,4,4,4, which agrees with the page, but that reading is not blind and is not calibration evidence. ")
rows = []
for r in prev["rows"]:
    i = r["id"]
    if i in UNVER:
        loc, fix = UNVER[i]
        ev = UNVER_EVIDENCE + (f"For {i}: the subject is absent or unscored at {PIN}." if i.endswith(("r8", "v9")) else "")
        if i.endswith(("r8", "v9")):
            ev = f"{loc} are absent at {PIN} (ls ledgers/E4/alternatives: alt_1.py..alt_8.py only); no current slice file cites them, and the round-8/9 logs that name them cannot re-establish the results. Not re-readable, so UNVERIFIABLE."
        rows.append({"id": i, "check": r["check"], "location": loc if i.endswith(("r8","v9")) else r["location"], "status": "UNVERIFIABLE", "evidence": ev, "fix": fix})
    elif i in O:
        st, ev, _ = O[i]
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": st, "evidence": ev})
    elif i in CARRY_OK:
        rows.append({"id": i, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": f"Carried from round 13 ({CARRY_OK[i]} byte-identical since the previous pin, e919577): " + r["evidence"]})
    else:
        raise SystemExit(f"unresolved round-13 id {i}")
NEW = [
 ("E4d14-mutants-r14-new", "mutants", "PASS", f"Five new student-error mutants (ledgers/E4/mutants/mutant_r14_01..05, written by ledgers/E4/scripts/E4-d-r14/make_mutants_r14.py from grader/reference.py, one exact replacement each): all KILLED in {S}/mutate_E4_0_9_with_r14.txt: r14_01 by test_unit_fraction_is_reported_at_zero_cost; r14_02 by test_noise_volume_nan_is_rejected; r14_03 by test_gap_is_the_oracle_gap_at_the_reported_fraction[first]; r14_04 by test_boundary_rule_holds[first]; r14_05 by test_unit_fraction_is_reported_at_zero_cost. Overlap in kind: r14_02 duplicates the existing mutant_r4f_nan_noise_volume_passes.py (killed by test_noise_volume_infinite_is_rejected); the others are different errors."),
 ("E4d14-corner-scan", "numbers", "PASS", f"Re-run of the README corner scan (sd = 1e-50*(1+0.002 i), i<300; cost c_edge-0.0005+0.0005 j/299; 90000 cases, reference with the cap changed): cap 200 -> 11598 cases over 1e-10, max 1.5322e-10 at sd 1e-50, cost 0.17076911209224613; cap 240 -> 0 over, max 5.1420e-13 ({S}/corner_scan_r14.txt). Matches the README (E4d13-readme-corner-domain)."),
 ("E4d14-accuracy-sweep", "numbers", "PASS", f"Random sweep, 20000 seeds of the interior: sd log-uniform on [1e-50, 4.9], tau-bar uniform on [0.01, tau_y(1)); reference root vs Proposition 4 closed form: 0 cases above 1e-10, max relative error 1.818e-12 ({S}/sweep_r14.txt). Covers the constraint 'noise volume at least 1e-50 and tau-bar at least 1e-2' beyond the corner."),
 ("E4d14-equivalent-literal-3000", "equivalence", "PASS", f"literal_price_sign.py vs reference.py on 3000 random inputs (sd in [0.05, 3], cost in [0, 0.4]): max |difference| in informed_fraction, informativeness and gap = 0.0 ({S}/equiv_r14.txt). The variant is output-identical, so no test can kill it; the architect item in the README stands."),
 ("E4d14-delta-read", "delta", "PASS", "Delta since e919577 in slice d, every hunk read: project.html lines 304 (Lab 3 prose after Prop 5) and 319 (Constraints: fraction-1 precision clause); grader/test_project.py lines 422-458 (fraction-1 tolerances to 1e-14); ledgers/E4/equivalent/README.md (domain and cost, rows of the stop-rule section), literal_price_sign.py and three variant files (comment reflow only); ledgers/E4/mutants/mutant_r13_01..05 (new files); plans/E4-build-plan.md (ruling appended at line 719 on). No other E4 slice-d file changed (instance.py, reference.py, starter.py, labs, alternatives, notation, references, tools unchanged)."),
]
for i, _, st, ev in NEW:
    rows.append({"id": i, "check": "2.6-round-14", "location": "see evidence", "status": st, "evidence": ev})

# mutants
mut_lines = [l for l in open(f"{ROOT}/{S}/mutate_E4_0_9_with_r14.txt", encoding="utf-8") if l.startswith("KILLED ")]
mutants = []
for l in mut_lines:
    head, _, rest = l[len("KILLED "):].partition(": ")
    desc, _, killer = rest.rpartition(" -> ")
    m = re.match(r"(.*) \(seed (\d+)\)\s*$", killer)
    test, seed = m.group(1), m.group(2)
    mutants.append({"id": head[:-3], "description": desc.strip(), "file": f"ledgers/E4/mutants/{head}", "killed_by": f"{test} (seed {seed})"})
assert len(mutants) == 122, len(mutants)

from collections import Counter
counts = Counter(r["status"] for r in rows)
verdict = "PASS" if counts["PASS"] == len(rows) and all(m["killed_by"] for m in mutants) else "FAIL"
notes = [
 "Delta since the round-13 pin e919577 in slice d: project.html lines 304 and 319 (prose only); grader/test_project.py lines 422-458 (fraction-1 tolerances raised to 1e-14, the round-13 FAIL); ledgers/E4/equivalent/README.md (domain and full-digit cost; round-13 FAIL) and four variant files (comment reflow only); ledgers/E4/mutants/mutant_r13_01..05 (new files, 8e5751c); plans/E4-build-plan.md (architect ruling on the alternatives, appended at line 719 on). Every hunk read. Round-13 rows carried only where the cited lines are outside these hunks (prefix 'Carried from round 13').",
 "Calibration (E4d-exemplar-A/B-calibration, E4d4/E4d5 calibration): UNVERIFIABLE. Blind scoring was not achieved in round 14. The verifier printed Exemplar A's annotations and both exemplars' data-level/data-scores while reading the report, and the round-13 fragment already states them. Non-blind rubric reading: A = 2,2,1,2,1; B = 4,4,4,4,4 (agrees with the page; not evidence). Fix: a verifier who has not read those blocks scores them blind.",
 "Stale citations (E4d8-alternatives-r8, E4d9-alternatives-v9): UNVERIFIABLE because the cited files are absent at this pin. Fix: retire the citations or restore the files at a pin.",
 "verify_refs --unit E4 (live): the first run timed out on one openlibrary request (mascolell1995microeconomic). Plain curl to the same URL returned HTTP 302 and the retry was 0 problems. Recorded in E4d-cmd-verify-refs; not a registry defect.",
 "Architect items (not rows, per the round-13 convention; none is a defect of a row): (a) literal_price_sign.py is output-identical to the reference on every input, so Proposition 1's sign of b_u/b_s cannot be tested (ledgers/E4/equivalent/README.md section 'What the architect must decide'). (b) The stop-rule variants (v9_02, r6_08, r7_01) differ from the reference only inside the 1e-12 stop tolerance, but they do alter the stated stop test and the reported point; the README asks whether the page must state the reported point (exemplar B's midpoint sentence at project.html:619 is the only statement of it). (c) Below sd = 1e-50 the solver is silently inaccurate (sd = 1e-300 returns fraction 2.8e-73, informativeness 0.5 from float underflow of a^2 sd^2, indifference_gap -0.2214): the page discloses this at project.html:326, and a fail-loud rule below 1e-50 is the architect's call. (d) The round-8/9 alternative citations (see above).",
 "New student-error mutants: five (mutant_r14_01..05). mutant_r14_02 overlaps in kind with the existing mutant_r4f_nan_noise_volume_passes.py.",
 "Not checked by this verifier: lessons L01-L09, cards.json (slice e), the other project pages; tools/render_curriculum.py and the full pytest suite (not in the slice gate); the Pyodide interpreter itself (page_smoke runs the repo harness); the blind score (see calibration); the accuracy at sd above 4.9 or at tau-bar below 1e-2 (not claimed by the page, so not tested); the literal Crossref live run for all 560 entries (only the unit's three entries and the offline integrity). The 22 x 22 box check (Lab 3) is the lab's computed check; the whole-box argument is the bound at project.html:315 (checked numerically on 1000 seeds and by the proof).",
 "Commands run on 8e5751c (all outputs in ledgers/E4/scripts/E4-d-r14/): check_projects, check_pages, check_dag, run_labs (project, all), run_graders 0-49, page_smoke project alone, ruff check, ruff format --check, mypy --no-incremental, pytest relevant subset, verify_refs offline and E4 live (x2), fetch_data --check, build_site --check, mutate_graders E4 0-9 (122 files), alternatives and equivalents 0-49 (run_candidates), twins under python -I -W error, collect-only (48).",
]
frag = {
 "unit": "E4", "slice": "d", "round": 14,
 "verifier": "Haiku independent verifier, E4 slice d, round 14 (did not build E4; checkout pinned at 8e5751c)",
 "pin": PIN,
 "base": "e919577b45b431ce68e1e6533b00b8a301277937 (round-13 pin); delta in slice d listed in notes",
 "checkout": ROOT,
 "scratch": "/tmp/e4d14",
 "verified_at": "2026-11-05T18:00:00+00:00",
 "verdict": verdict,
 "rows": rows,
 "mutants": mutants,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": notes,
 "summary": f"E4 slice d round 14: verdict {verdict}. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Mutants: {len(mutants)} files in ledgers/E4/mutants/ (117 + 5 new), {sum(1 for m in mutants if m['killed_by'])} killed on seeds 0-9. Round-13 non-PASS rows: 3 FAIL fixed (E4d13-endpoint-gap-precision, E4d13-alternatives-plan-list (by the 2026-11-05 ruling), E4d13-readme-corner-domain) and 1 FAIL fixed (E4d12-equivalent-readme-numbers). Remaining non-PASS: 4 calibration rows (blind scoring not achieved) and 2 stale citations.",
}
out = f"{ROOT}/ledgers/E4/E4-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", out, "rows", len(rows), dict(counts), "mutants", len(mutants), "verdict", verdict)
