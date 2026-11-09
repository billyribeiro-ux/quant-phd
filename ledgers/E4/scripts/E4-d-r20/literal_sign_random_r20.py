"""Round-20 check of the README claim for ledgers/E4/equivalent/literal_price_sign.py: 3000 random inputs, reference vs variant.
Usage: python3 -I literal_sign_random_r20.py <checkout-root>"""
import importlib.util, random, sys
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
root = sys.argv[1]
ref = load(root + "/course/modules/E/E4/grader/reference.py", "ref")
var = load(root + "/ledgers/E4/equivalent/literal_price_sign.py", "var")
rng = random.Random(1)
worst = 0.0
for _ in range(3000):
    sd = rng.uniform(0.05, 3.0); c = rng.uniform(0.0, 0.4)
    a, b = ref.solve_model(sd, c), var.solve_model(sd, c)
    worst = max(worst, max(abs(a[k] - b[k]) for k in a))
print("3000 random inputs, largest absolute difference in any output:", worst)
