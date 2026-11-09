from fractions import Fraction as F
# L04 M3: f(x)=1/x at 2, Q(h) = (1/(2+h)-1/2)/h ; check Q(h)+1/4 = h/(4(2+h)) and |Q+1/4| < |h|/4 for |h|<1
import random
for h in [F(1, 10), F(-1, 10), F(1, 3), F(-9, 10), F(99, 100), F(-1, 1000)]:
    Q = (1 / (2 + h) - F(1, 2)) / h
    assert Q == F(-1, 2 * (2 + h)), h
    assert Q + F(1, 4) == h / (4 * (2 + h)), h
    assert abs(Q + F(1, 4)) < abs(h) / 4, h
print('L04 M3 identities hold on sample points')
# L04 R1: Q(h) for x|x| at 0 equals |h|
for h in [F(1, 7), F(-1, 7)]:
    assert (h * abs(h)) / h == abs(h)
print('L04 R1 Q(h)=|h| holds on sample points')
# L05 central-difference errors at x=3/2, h=1e-4 (exact rationals)
x = F(3, 2); h = F(1, 10000)
fns = {
    'p': (lambda t: (t*t+1)*t**3, lambda t: 5*t**4 + 3*t*t),
    'q': (lambda t: (t*t+1)/(t+2), lambda t: (2*t*(t+2) - (t*t+1))/((t+2)**2)),
    'c': (lambda t: (t*t+1)**3, lambda t: 6*t*(t*t+1)**2),
}
for k, (f, df) in fns.items():
    cd = (f(x+h) - f(x-h)) / (2*h)
    err = cd - df(x)
    print(k, 'analytic', float(df(x)), 'central', float(cd), 'abs diff', float(abs(err)))
# p'''(x) = 60x^2 + 6 at 1.5 ; leading term h^2 p'''/6
print("p'''(1.5)", 60*x*x + 6, "h^2 p'''/6 =", float(h*h*(60*x*x+6)/6))
# x^3 central difference at x=1 equals 3 + h^2 exactly
h2 = F(1, 10000)
print('x^3 CD at 1 minus 3 == h^2:', ((1+h2)**3 - (1-h2)**3)/(2*h2) - 3 == h2*h2)
print('q prime exact 29/49:', (2*x*(x+2) - (x*x+1))/((x+2)**2) == F(29, 49))
print('c prime at 1.5 =', float(6*x*(x*x+1)**2))
