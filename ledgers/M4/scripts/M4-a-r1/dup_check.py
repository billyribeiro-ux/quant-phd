import sys
from collections import Counter
sys.path.insert(0, sys.argv[1])
import importlib.util
spec = importlib.util.spec_from_file_location("rung1", sys.argv[1] + "/rung1_block.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for fam in ("gaussian", "student_t"):
    xs = m.simulate(fam)
    c = Counter(xs)
    extra = len(xs) - len(c)
    print(fam, "n", len(xs), "distinct", len(c), "extra copies", extra, "max multiplicity", max(c.values()))
