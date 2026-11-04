import sys, importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod); return mod
R = "/Users/billyribeiro/.fanout/wt/verifyE3-BK4-c/"
f = load(R + "ledgers/BK4/mutants/r3f_defaulter_upper_bound_from_max_id.py", "mut_f")
ref = load(R + "course/modules/BK/BK4/grader/reference.py", "ref")
e = load(R + "ledgers/BK4/mutants/r3e_sizing_counts_distinct_losses.py", "mut_e")
print("r3f, defaulter_id 0 (not a member; page requires ValueError naming defaulter_id):")
for label, mod in (("reference", ref), ("r3f mutant", f)):
    try:
        print(f" {label}: result", mod.waterfall(10, 0, {1: 5, 2: 5}, {1: 4, 2: 6}, 0))
    except Exception as x:
        print(f" {label}: raised", type(x).__name__, "-", x)
for L, t in (([5, 5, 10], 5000), ([5, 5, 10, 20], 5000), ([5, 5, 5, 9, 12], 6000)):
    print(f"r3e, losses {L}, target {t}: reference {ref.margin_for_cover(L, t)}  mutant {e.margin_for_cover(L, t)}")
