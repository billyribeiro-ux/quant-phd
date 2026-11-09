"""Round-14 verifier: builds the fragment's mutant list from the mutant files and the two kill-check outputs.
Argument 1 is the checkout root. Writes out/mutants_r14.json (read by build_fragment_r14.py)."""
import json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
O = root / "ledgers/LX1/scripts/LX1-c-r14/out"
lines = (O / "kill_check_all_mutants_existing.out").read_text(encoding="utf-8").splitlines() + \
        (O / "kill_new_r14.out").read_text(encoding="utf-8").splitlines()
res = {}
for l in lines:
    m = re.match(r"(KILLED|SURVIVED) \| ([^|]+?) \| ?(.*)$", l)
    if m:
        res[m.group(2).strip()] = (m.group(1), m.group(3).strip())
muts = []
for p in sorted((root / "ledgers/LX1/mutants").glob("*.py")):
    if p.name not in res:
        continue
    text = p.read_text(encoding="utf-8")
    if p.name.startswith("r14"):
        desc = next((l for l in text.splitlines()[:3] if "Student error" in l), text.split("\n", 1)[0])
        desc = desc.split("Student error:")[-1].strip().strip('"')
    else:
        desc = text.split("\n", 1)[0].strip().strip('"')
    status, why = res[p.name]
    if status == "KILLED":
        kind = ("nonzero exit or stderr" if why.startswith("rc=") else
                "expected-block differs" if "expected-block differs" in why else "damaged-snapshot check did not raise")
        killed_by = f"tools kill check (ledgers/LX1/scripts/LX1-c-r14/out/kill_check_all_mutants_existing.out or kill_new_r14.out): {kind}"
    else:
        killed_by = None
        desc += " SURVIVED: stdout matches the expected block and exit 0 with the agreement check removed; see row proj-lab3-raise-claims-untested."
    muts.append({"id": p.name, "description": desc[:230].rstrip(), "killed_by": killed_by})
(O / "mutants_r14.json").write_text(json.dumps(muts, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(len(muts), sum(1 for m in muts if m["killed_by"]))
