"""Witness: the L01 twin raises on a conflicting (filed, accn) tie; the L02 twin's standardizer copy does not."""
import sys
def load(path):
    src = open(path, encoding="utf-8").read().rstrip()
    assert src.endswith("main()")
    ns = {}
    exec(compile(src[: -len("main()")], path, "exec"), ns)
    return ns
row = {"end": "2023-12-31", "filed": "2024-02-15", "form": "10-K", "fp": "FY", "accn": "SIM-2023-K"}
facts = {"facts": {"us-gaap": {"Assets": {"units": {"USD": [{**row, "val": 1.0}, {**row, "val": 2.0}]}}}}}
for label, path in (("L01 twin", sys.argv[1]), ("L02 twin", sys.argv[2])):
    ns = load(path)
    try:
        out = ns["standardize"](facts)
        print(label, "returned without error:", out)
    except ValueError as exc:
        print(label, "ValueError:", exc)
