import importlib.util, math
REF = "/Users/billyribeiro/.fanout/wt/verifyE14-E4-d/course/modules/E/E4/grader/reference.py"
spec = importlib.util.spec_from_file_location("ref", REF); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
root = 2.0224e-51
k = 0; w = 1.0
while w > 1e-12 * root:
    w /= 2; k += 1
print("halvings to width <= 1e-12*root (root 2.0224e-51):", k)
def closed(sd, c):
    t = 2.0 * math.exp(-4.0 * c) - 1.0
    return 2.0 * sd * math.sqrt(t / (1.0 - t))
for cap in (200, 240):
    ref.MAX_BISECTION_STEPS = cap
    for c in (0.17076911209, 0.17076911209224613):
        ex = closed(1e-50, c); out = ref.solve_model(1e-50, c)["informed_fraction"]
        print("cap", cap, "cost", c, "rel err", f"{abs(out-ex)/ex:.4e}")
print("2^-200 =", 2.0**-200, " 1e-10*root(2.0224e-51) =", 1e-10*2.0224e-51)
print("2^-240 vs 1e-12*root at 6e-61:", 2.0**-240, 1e-12*6e-61)
