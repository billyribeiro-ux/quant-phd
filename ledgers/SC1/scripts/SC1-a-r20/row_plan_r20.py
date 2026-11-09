"""SC1-a round 20: which round-19 rows are re-verified this round (FRESH) and which are carried.
A carried row is PASS only when its cited subject is byte-identical since cd4dd7df (see notes in the fragment).
Usage (checkout root): python3 -I ledgers/SC1/scripts/SC1-a-r20/row_plan_r20.py"""
import json
import re
import subprocess

prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-a.round19.json", encoding="utf-8"))
FRESH = {
    "SC1a-gate-check-pages", "SC1a-gate-check-dag", "SC1a-gate-run-labs", "SC1a-gate-page-smoke",
    "SC1a-gate-lint-types-tests", "SC1a-gate-verify-refs", "SC1a-r7-gate-check-projects", "SC1a-r7-katex-render",
    "SC1a-r8-links-anchors", "SC1a-r15-gate-ruff-check", "SC1a-r15-links-anchors-scripted", "SC1a-r18-page-smoke-alone",
    "SC1a-r18-page-vs-twin", "SC1a-r10-cmd-check_pages", "SC1a-r10-cmd-check_dag", "SC1a-r10-cmd-check_projects",
    "SC1a-r10-cmd-run_labs", "SC1a-r10-cmd-page_smoke", "SC1a-r10-cmd-twins-python-I-W-error",
    "SC1a-r10-cmd-verify_refs", "SC1a-r10-cmd-ruff-mypy", "SC1a-r10-cmd-pytest-SC1",
    "SC1a-lab-L01-twin", "SC1a-lab-L02-twin", "SC1a-lab-L03-twin", "SC1a-r8-lab-mutants", "SC1a-r10-lab-mutants-4of4",
    "SC1a-r11-lab-mutants-6of6", "SC1a-r14-lab-mutants-new3", "SC1a-r15-lab-mutants-p1-p3", "SC1a-r16-lab-mutants-35",
    "SC1a-r16-lab-q1-q3-new", "SC1a-r16-mutants-list", "SC1a-r19-lab-mutants-all-38", "SC1a-r16-L01-lab-output",
    "SC1a-r16-L02-lab-output", "SC1a-r16-L03-lab-output",
    "SC1a-math-L02-A2-sketch", "SC1a-r10-L03-why-sample-means", "SC1a-r17-hunk-L03-51", "SC1a-r16-why-words",
    "SC1a-r17-banned-changed-lines", "SC1a-banned-phrases", "SC1a-r16-banned-phrases", "SC1a-r18-banned-scan",
    "SC1a-process-words", "SC1a-r10-process-words", "SC1a-r16-process-words", "SC1a-r16-scope-words",
    "SC1a-r16-notation", "SC1a-notation-macros", "SC1a-notation-no-registered-collision", "SC1a-notation-T-subscript",
    "SC1a-r10-notation-collisions", "SC1a-r18-notation-macros", "SC1a-r4-notation-S-symbol-L02",
    "SC1a-r15-counts", "SC1a-r10-cards-dup-hypotheses", "SC1a-r11-cards-scan", "SC1a-r13-cards-L01-L03-read",
    "SC1a-r14-cards-L01-L03-changed", "SC1a-r16-cards-L01-L03-full", "SC1a-r16-cards-grade-field",
    "SC1a-r17-card-c017-definition-fixes", "SC1a-r18-card-c017", "SC1a-r18-cards-full-scan", "SC1a-r19-card-c243",
    "SC1a-r19-c243-proposition-content", "SC1a-r19-cards-struct", "SC1a-r19-delta-read", "SC1a-r18-delta-read",
    "SC1a-r17-delta-read", "SC1a-r16-delta-read", "SC1a-r15-delta-read", "SC1a-r11-delta-read",
    "SC1a-r11-numbers-recomputed", "SC1a-r18-lab-L03-gap-13.22", "SC1a-r16-math-proofs", "SC1a-r10-lab-L01-L02-L03-claims",
    "SC1a-r18-notation-macros", "SC1a-r18-banned-scan", "SC1a-r18-hunk-L03-270", "SC1a-r18-hunk-L03-278",
    "SC1a-r18-hunk-L03-116", "SC1a-r18-hunk-L03-260", "SC1a-r18-hunk-L02-51", "SC1a-r16-scope-words",
}
touched_not_fresh = []
for r in prev["rows"]:
    if r["id"] in FRESH:
        continue
    loc = r.get("location") or ""
    if re.search(r"cards\.json|L02\.html|L03\.html", loc):
        touched_not_fresh.append((r["id"], loc[:120]))
print("rows", len(prev["rows"]), "FRESH ids present:", sum(1 for r in prev["rows"] if r["id"] in FRESH))
print("missing FRESH ids:", sorted(FRESH - {r["id"] for r in prev["rows"]}))
print("non-fresh rows whose location names cards.json/L02.html/L03.html:")
for i, l in touched_not_fresh:
    print("  ", i, "|", l)
