import importlib.util, random, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
R = "/Users/billyribeiro/.fanout/wt/verifyE14-E4-d"
ref = load(R + "/course/modules/E/E4/grader/reference.py", "ref")
lit = load(R + "/ledgers/E4/equivalent/literal_price_sign.py", "lit")
rng = random.Random(14)
worst = [0.0, 0.0, 0.0]; n = 0
for _ in range(3000):
    sd = rng.uniform(0.05, 3.0); c = rng.uniform(0.0, 0.4)
    a = ref.solve_model(sd, c); b = lit.solve_model(sd, c)
    for k, key in enumerate(("informed_fraction", "price_informativeness", "indifference_gap")):
        worst[k] = max(worst[k], abs(a[key] - b[key]))
    n += 1
print("n", n, "max abs diff per output", worst)
print("literal_price_sign has solve_model:", hasattr(lit, "solve_model"), "MAX_BISECTION_STEPS", lit.MAX_BISECTION_STEPS)
