"""E3-e round 13: assemble ledgers/E3/E3-e.json from the r13 scripts' outputs (python -I)."""
import json
import sys

ROOT = sys.argv[1]
S = f"{ROOT}/ledgers/E3/scripts/E3-e-r13"
mut_lines = [l.rstrip("\n") for l in open(f"{S}/mutate_graders_E3.out", encoding="utf-8")]
mutants = []
for line in mut_lines:
    if line.startswith("KILLED "):
        body = line[len("KILLED "):]
        name, rest = body.split(": ", 1)
        desc, killed = rest.rsplit(" -> ", 1)
        mutants.append({"id": name.rsplit(".", 1)[0], "description": desc, "file": f"ledgers/E3/mutants/{name}", "killed_by": killed})
    elif line.startswith("SURVIVED "):
        body = line[len("SURVIVED "):]
        name = body.split(":", 1)[0]
        mutants.append({"id": name.rsplit(".", 1)[0], "description": "Logit log term computed as log(1 + exp(t)) without the stable form; overflows only for large |z|. Survivor is informational: project.html states no numerical-stability requirement (grep for overflow, large, extreme, finite finds none).", "file": f"ledgers/E3/mutants/{name}", "killed_by": ""})
for n in ["r13n01_half_cent_rounded_half_to_even", "r13n02_loss_aversion_scales_gain_branch", "r13n03_logit_scale_in_dollars_not_hundreds"]:
    assert any(m["id"] == n for m in mutants), n

rows = json.load(open(f"{S}/rows.json", encoding="utf-8"))
frag = {
    "unit": "E3", "slice": "e", "round": 13,
    "verifier": "Haiku independent verifier, E3-e round 13 (did not build E3)",
    "pin": "762f636", "base": "460b696 (round-12 pin; round-12 fragment /Users/billyribeiro/.fanout/frags/C-E3-e.round12.json)",
    "checkout": ROOT, "scratch": "/tmp/e3e_r13/", "verified_at": "2026-10-29",
    "verdict": "FAIL", "rows": rows, "mutants": mutants,
    "registry_flags": [], "freshness_flags": [],
    "notes": [
        "Delta 460b696..762f636 inside the slice: course/modules/E/E3/cards.json (c050, c082, c137 changed; c172, c173 added), course/modules/E/E3/L03.html (lab print reword and its expected block), L05.html and L06.html (References paragraphs: data-cite removed, graded D claims became ungraded naming sentences), tests/labs/E3/lab-E3-L03-1.py (print reword), plans/E3-build-plan.md line 392 (exemplar wording). project.html is byte-identical to 460b696, so its rows are carried where their other subjects are unchanged.",
        "Mutation tool verdict is FAIL 59/60: the survivor ledgers/E3/mutants/r10n06_logit_log_term_naive_exp_overflow.py (round-10 mutant) is recorded with killed_by empty. Per the verifier rulings it is informational, since project.html states no numerical-stability requirement; the ledger verdict stays FAIL because the mechanical rule requires every mutant killed, and the verdict here is FAIL for the four rows below anyway.",
        "Previous round's FAIL on the L03 lab print (every gamma vs the GAMMAS loop) is resolved: the reworded print matches the code and the page expected block.",
        "Not run: references/verify_refs.py --offline and tools/fetch_data.py --check (no reference or data file changed in this delta); the full pytest suite (only the targeted subset); ruff/mypy on the whole repo (only the changed L03 twin was linted).",
        "Not checked: the 97 T-grade cards were not each checked line by line against their cited Proposition, Theorem or Remark text; see row E3e-r12-cards-T-lesson-agreement.",
        "Interpretation rulings applied: L05.html:609 and L06.html:531 naming sentences are read against references/references.json (epstein1989substitution: Epstein, Zin; kahneman1979prospect: Kahneman, Tversky) and state no result; accepted as ungraded naming.",
    ],
    "summary": {},
}
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
frag["summary"] = {"pass": counts.get("PASS", 0), "fail": counts.get("FAIL", 0), "unverifiable": counts.get("UNVERIFIABLE", 0), "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
json.dump(frag, open(f"{ROOT}/ledgers/E3/E3-e.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(frag["summary"])
