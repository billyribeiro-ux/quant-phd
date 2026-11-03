# Remark 1.4 hypotheses hold for f(x, a) = -x^2/2 (C^2), a0 = 0, xhat(0) = 0 (f_x = 0, f_xx = -1 != 0),
# xhat continuous at 0; but xhat(a) = |a| is not a maximizer for a != 0 (H2 fails) and is not differentiable at 0.
def f_x(x, a):
    return -x

def xhat(a):
    return abs(a)

for a in (0.1, 0.01, -0.01):
    print("a", a, "xhat", xhat(a), "f_x(xhat(a),a)", f_x(xhat(a), a), "maximizer (f(.,a) max at 0)?", xhat(a) == 0)
h = 1e-6
print("difference quotient of xhat at 0 from right", (xhat(h) - xhat(0)) / h, " from left", (xhat(-h) - xhat(0)) / (-h))
