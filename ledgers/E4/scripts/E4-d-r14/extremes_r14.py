import importlib.util, math
REF = "/Users/billyribeiro/.fanout/wt/verifyE14-E4-d/course/modules/E/E4/grader/reference.py"
spec = importlib.util.spec_from_file_location("ref", REF); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
INST = "/Users/billyribeiro/.fanout/wt/verifyE14-E4-d/course/modules/E/E4/grader/instance.py"
spec2 = importlib.util.spec_from_file_location("inst", INST); inst = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(inst)
for sd, c in [(1e150, 0.0), (1e150, 350.0), (1e-50, 350.0), (0.5, 350.0), (1e-300, 0.1), (1.0, 1e-300), (1e-50, 1e-300), (1e-50, 0.15), (1e-50, 0.12), (0.5, 1.0)]:
    try:
        o = ref.solve_model(sd, c); print(sd, c, o)
    except Exception as e:
        print(sd, c, "EXC", type(e).__name__, e)
# interior check for seeds 0..49 and 0..999
bad = []
for s in range(1000):
    i = inst.make_instance(s)
    o = ref.solve_model(i["noise_sd"], i["info_cost"])
    if not (0.0 < o["informed_fraction"] < 1.0): bad.append(s)
print("non-interior seeds among 0..999:", bad[:10], len(bad))
print("seeds 0..49 interior count:", sum(1 for s in range(50) if 0 < ref.solve_model(inst.make_instance(s)["noise_sd"], inst.make_instance(s)["info_cost"])["informed_fraction"] < 1))
