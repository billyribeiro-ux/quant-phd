import importlib.util, math
spec = importlib.util.spec_from_file_location("ref", "/tmp/verify6-CF1-d/course/modules/CF/CF1/grader/reference.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
def quad(r1, r2):
    x1, x2 = 1 / (1 + r1), 1 / (1 + r2)
    return [x1 * x2, -(x1 + x2), 1.0]
for r2 in (0.101, 0.11, 0.102, 0.105, 0.2):
    f = quad(0.1, r2)
    print("roots 0.1 and", r2, "flows", [round(c, 6) for c in f], "reference irr_roots:", ref.irr_roots(f))
# grid points near the 0.1 root for the 0.101 case
xs = [math.exp(math.log(1e-4) + (math.log(1e4) - math.log(1e-4)) * k / 4000) for k in range(4001)]
for r in (0.1, 0.101):
    x = 1 / (1 + r)
    k = max(i for i, v in enumerate(xs) if v <= x)
    print("root", r, "x", x, "bracketed by grid indices", k, k + 1, "grid x", xs[k], xs[k + 1])
print("step factor", xs[1] / xs[0])
