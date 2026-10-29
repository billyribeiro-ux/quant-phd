import math
target = math.e
def central(fun, x, h):
    return (fun(x + h) - fun(x - h)) / (2.0 * h)
for k in (5, 6, 7):
    h = 10.0**-k
    e = abs(central(math.exp, 1.0, h) - target)
    print(k, repr(h), repr(e), f"{e:.6e}")
e5 = abs(central(math.exp, 1.0, 1e-5) - target)
e7 = abs(central(math.exp, 1.0, 1e-7) - target)
print("diff", e7 - e5, abs(e7-e5), "ulp(e)", math.ulp(math.e), "ulp(1)", math.ulp(1.0))
print("ratio of logs ", math.log10(6.3e-6), math.log10(1e-5), math.log10(1e-6))
