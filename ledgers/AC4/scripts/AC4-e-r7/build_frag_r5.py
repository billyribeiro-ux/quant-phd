"""Build the round-5 AC4-e fragment from the round-5 runs (mutate_graders output and the checks listed in the rows)."""
import json, re, pathlib, sys
ROOT = pathlib.Path(sys.argv[1]).resolve()
MUT_OUT = pathlib.Path("/tmp/ac4-v/e5/mutate.out").read_text()
killed = {}
for line in MUT_OUT.splitlines():
    m = re.match(r"(KILLED|SURVIVED) (m\d\d_\S+?)\.py: (.*) -> (.*)$", line)
    if m:
        killed[m.group(2)] = (m.group(1), m.group(3), m.group(4))
prev = json.load(open("/tmp/fanout-frags/AC4-e.round4.json"))
desc_prev = {x["id"]: x["description"] for x in prev["mutants"]}
NEW_DESC = {
    "m25_missing_actual_inputs_defaults_to_zero": "Case field actual_inputs_used treated as optional and read as 0 when absent (a case without a required field is accepted).",
    "m26_master_accepts_negative_input_price": "master_budget alone skips the negative-input-price check (it normalises a negative input price to 0 before validating).",
    "m27_master_returns_cached_object": "master_budget returns one cached object after the first call instead of a fresh object.",
    "m28_debug_print_left_in_flexible_budget": "A debugging print left in flexible_budget.",
    "m29_master_marks_the_argument": "master_budget writes a marker key into the caller's case dictionary.",
}
mutants = []
for name, (status, description, test) in killed.items():
    entry = {"id": name, "file": f"ledgers/AC4/mutants/{name}.py",
             "description": NEW_DESC.get(name, desc_prev.get(name, description))}
    if status == "KILLED":
        entry["killed_by"] = test.replace(" (seed 0)", "").strip() + " (seed 0)"
    mutants.append(entry)
mutants.sort(key=lambda x: x["id"])
print("mutants", len(mutants), "killed", sum(1 for m in mutants if "killed_by" in m))
json.dump(mutants, open("/tmp/ac4-v/e5/mutants.json", "w"), indent=1)
