import importlib.util, math, sys
spec = importlib.util.spec_from_file_location("ref", "/tmp/cf1-v/d/r8/ref.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
print("neighbour factor", math.exp((math.log(1e4) - math.log(1e-4)) / 4000))
def flows_from_roots(r1, r2):
    # NPV(r) = c0 + c1 x + c2 x^2 with x = 1/(1+r), roots in r; c2 = 1 monic in x
    x1, x2 = 1 / (1 + r1), 1 / (1 + r2)
    return [x1 * x2, -(x1 + x2), 1.0]
def check(r1, r2):
    f = flows_from_roots(r1, r2)
    roots = ref.irr_roots(f)
    print(r1, r2, "->", roots)
    # verify the flows give those roots
    print("  npv at roots", [ref.npv(r, f) for r in (r1, r2)])
check(0.1, 0.101)
check(0.1, 0.11)
# close() definition
src = open("/tmp/verify8-CF1-d/course/modules/CF/CF1/grader/test_project.py").read().splitlines()
print("\n".join(src[62:72]))
