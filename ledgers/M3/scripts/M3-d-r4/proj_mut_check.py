import sys, importlib.util
sys.path.insert(0, "/tmp/verifyB4-M3-d/course/modules/M/M3/grader")
import instance
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ref = load("/tmp/verifyB4-M3-d/course/modules/M/M3/grader/reference.py", "ref")
m4 = load("/tmp/verifyB4-M3-d/ledgers/M3/mutants/r4d_m04_projection_default_iterations_fifty.py", "m4")
m5 = load("/tmp/verifyB4-M3-d/ledgers/M3/mutants/r4d_m05_projection_stops_on_gap_only.py", "m5")
def mineig(a):
    v,_ = ref._eigh(a); return min(v)
worst = {"ref": (0,0), "m4": (0,0), "m5": (0,0)}
diffs = {"m4": 0, "m5": 0}
for s in range(50):
    I = instance.make_instance(s)
    c = I["corr"]
    r = ref.projection_repair(c)
    for name, mod in (("m4", m4), ("m5", m5)):
        y = mod.projection_repair(c)
        d = max(abs(y[i][j]-r[i][j]) for i in range(len(c)) for j in range(len(c)))
        diffs[name] = max(diffs[name], d)
        ev = mineig(y)
        worst[name] = (min(worst[name][0], ev), max(worst[name][1], max(abs(y[i][i]-1) for i in range(len(c)))))
print("max entry diff vs reference over seeds 0-49:", diffs)
print("worst (min eig, max diag dev) per mutant:", worst)
