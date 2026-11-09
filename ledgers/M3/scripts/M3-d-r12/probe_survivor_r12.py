"""Round-12 verifier (M3 slice d): direct probe of the survivor v12d_03 against the reference, for the grader-named-conditions
row. Run from the checkout root with python -I."""

import importlib.util

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

REF = "course/modules/M/M3/grader/reference.py"
MUT = "ledgers/M3/scripts/M3-d-r12/survivors/v12d_03_clip_validates_symmetry_only_for_default_floor.py"
for name, path in [("reference", REF), ("survivor v12d_03", MUT)]:
    m = load(name.replace(" ", "_"), path)
    for label, call in [
        ("clip_repair asymmetric 1e-1 input, floor=0.1", lambda: m.clip_repair([[1.0, 0.3], [0.5, 1.0]], floor=0.1)),
        ("clip_repair asymmetric 1e-1 input, default floor", lambda: m.clip_repair([[1.0, 0.3], [0.5, 1.0]])),
    ]:
        try:
            r = call()
            print(name, "|", label, "| returned", [[round(x, 6) for x in row] for row in r])
        except ValueError as e:
            print(name, "|", label, "| ValueError:", str(e)[:70])
