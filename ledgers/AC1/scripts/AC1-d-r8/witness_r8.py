import importlib.util, sys
def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("/tmp/verify8-AC1-d/course/modules/AC/AC1/grader/reference.py")
mut = load(sys.argv[1])
tx = [{"date": "2024-01-02", "lines": [{"account": "cash", "debit": 5, "credit": 0}, {"account": "common_stock", "debit": 0, "credit": 6}]}]
for name, m in (("reference", ref), ("mutant", mut)):
    try:
        m.post(tx); print(name, "accepted")
    except ValueError as e:
        print(name, "ValueError:", e)
