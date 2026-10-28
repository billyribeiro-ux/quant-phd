import importlib.util, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("/tmp/verify6-CF1-d/course/modules/CF/CF1/grader/reference.py", "ref")
m36 = load("/tmp/verify6-CF1-d/ledgers/CF1/mutants/m36_window_low_end_extended_to_one_millionth.py", "m36")
for flows in ([-1.0, 1e5], [-1.0, 1.0 / 1.5e-4], [-10000.0, 1.0]):
    print(flows, "reference:", ref.irr_roots(flows), "m36:", m36.irr_roots(flows))
print("rate of x=1e-5:", 1 / 1e-5 - 1)
