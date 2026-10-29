# L19 Example 2.2: numeric f_xy = d/dy (f_x) off the origin, near origin along axes and diagonal.
def f(x, y):
    if x == 0 and y == 0:
        return 0.0
    return x * y * (x * x - y * y) / (x * x + y * y)
def fx(x, y):
    # analytic f_x off origin, from quotient rule via central difference at tiny step (high accuracy for t not tiny)
    h = 1e-9 * max(1.0, abs(x) + abs(y))
    return (f(x + h, y) - f(x - h, y)) / (2 * h)
def fxy(x, y, h=1e-4):
    return (fx(x, y + h) - fx(x, y - h)) / (2 * h)
for t in (1e-1, 1e-2, 1e-3):
    print("t=%g  f_xy(t,0)=%.6f  f_xy(0,t)=%.6f  f_xy(t,t)=%.6f" % (t, fxy(t, 0.0), fxy(0.0, t), fxy(t, t)))
