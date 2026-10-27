"""Round-4: recompute M2 and M3 answers and the R1 'Lab 1 method' claim with the L01 twin (read-only)."""
import sys, types
sys.modules.pop("twin", None)
def load(path):
    with open(path, encoding="utf-8") as fh:
        src = fh.read().rstrip()
    src = src[: -len("main()")]
    mod = types.ModuleType("twin"); sys.modules["twin"] = mod
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod
L1 = load("/tmp/verify-ac2r4-l12/tests/labs/AC2/lab-AC2-L01-1.py")
f = L1.make_filer()
for cut in ["2023-02-14", "2023-02-15", "2024-02-29", None, "2023-06-30"]:
    t = L1.standardize(f, cut)
    print("M2 cut", cut, "FY2022 revenue", t.get("2022-12-31", {}).get("revenue"))
for cut in ["2025-01-31", "2025-02-15"]:
    t = L1.standardize(f, cut)
    print("M3 cut", cut, "2024-12-31 present", "2024-12-31" in t)
print("period ends no cut", list(L1.standardize(f, None)))
