"""Assemble ledgers/M3/M3-d.json from the rows and mutants written by closing_build_fragment.py."""
import datetime
import json

ROOT = "/Users/billyribeiro/.fanout/wt/verifyG1-M3-d"
rows = json.load(open("/private/tmp/verifyG1-M3-d-txt/rows_out.json", encoding="utf-8"))
mutants = json.load(open("/private/tmp/verifyG1-M3-d-txt/mutants_out.json", encoding="utf-8"))
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "PASS" if counts["PASS"] == len(rows) and all(m.get("killed_by") for m in mutants) else "FAIL"
notes = (
    "Closing delta (ruling 30) of slice d, round 1: base F2-M3-d.round1 (pin 95f3f8cb, verdict FAIL with one row, cards-L08). "
    "Delta 95f3f8cb..2a805c83 on the slice: L07.html line 56; L08.html line 312; L09.html lines 52, 200-201, 353; cards.json (4 records: M3-c138, c141, c145, c174); tests/labs/M3/lab-M3-L09-1.py lines 9-11. "
    "project.html, grader/, index.html, L01-L06 pages, tests/labs/M3 twins other than L09, mutants/, alternatives/, equivalent/, retired/, references, tools, curriculum, notation and course/assets/js/python.js are byte-identical to 95f3f8cb (git diff --quiet). "
    "No mutant was authored (ruling 37). The standing run of 184 mutants killed 184/184 by named tests. "
    "| Ruling-26 FAIL kinds: none found in the delta. The base FAIL cards-L08 is closed: c145 is regraded C naming the Lab 1 SIMULATED panel, and its text no longer claims a data-dependent level label without a witness. "
    "| Corrections to base evidence: the 198-test statement is at project.html line 239, not 247 (gate-collect-only, grader-test-count-and-purity). The base's card counts 50/122/38 were partitioned as 50 without grade, 122 grade-only, 38 grade-and-basis; now 50/121/39. "
    "| LOW (not a ruling-26 kind, not a FAIL): the letter N is used for Q M Q^T at L09.html line 79 and for the lab noise matrix in the L09 docstring (row delta-notation-local-N-L09). "
    "| LOW (carried): c075 wording 'so no pair was skipped' follows from the printed 1200 rather than from the stated rule (base note). "
    "| Governance (not a verdict input, carried): the brief amendment in curriculum/01-foundations.yaml (commit 6f5f300a) is not recorded as an architect ruling; plans/M3-build-plan.md section 9 B3 still reads 'Architect decision required'. "
    "| Calibration: no blind scorer file for M3 exists in ~/.fanout/blind/ (checked: none matching m3); the base calibration rows (project-exemplars, project-rubric, rubric-C4-level2-vague) are carried and remain not strictly blind (open gap). "
    "| Could not check or did not do: the Pyodide/browser run of the grader and alternatives (only local pytest and page_smoke on L07-L09 and the project page carried); a live Crossref run this round (verify_refs --unit M3 live, carried from base); a line-by-line re-read of the 170 unchanged card records against lesson text (only the records whose cited text changed were re-read); render_curriculum was not re-run because no curriculum source or cards consumer changed (tools/check_pages.py is the only tool that reads cards.json)."
)
summary = (
    f"M3 slice d closing delta round 1 on 2a805c83 (base 95f3f8cb): verdict {verdict}. "
    f"{len(rows)} rows: PASS {counts['PASS']}, FAIL {counts.get('FAIL', 0)}, UNVERIFIABLE {counts.get('UNVERIFIABLE', 0)}. "
    f"Base FAIL cards-L08 closed (c145 regraded C). Mutants in ledgers/M3/mutants/: {len(mutants)}, all KILLED by named tests in the standing run."
)
frag = {
    "unit": "M3",
    "slice": "d",
    "round": 1,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, closing delta round 1 (ruling 30); shares no context with the builders",
    "pin": "2a805c831410ab77c38c227f7e121e8537193ce9",
    "base": "F2-M3-d.round1 (pin 95f3f8cb21c2cd9fc904430bd30a6b734d01f672); delta 95f3f8cb..2a805c83 on this slice. Rulings 30, 37 and 26 (FAIL kinds) apply.",
    "checkout": ROOT,
    "scratch": "ledgers/M3/scripts/M3-d-r1/",
    "verified_at": datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
out = f"{ROOT}/ledgers/M3/M3-d.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(out, "a", encoding="utf-8").write("\n")
print("wrote", out, "rows", len(rows), "verdict", verdict)
