# Independent recomputation for the M2-a slice (pin 1817191). Exact Fractions where possible.
# Usage: .venv/bin/python -I ledgers/M2/scripts/M2-a-r2/recompute_r2.py
from fractions import Fraction as F
ok = True
def check(name, cond):
    global ok
    ok = ok and cond
    print(("PASS " if cond else "FAIL ") + name)

check("L01 |a_n-2| = 1/(n+1) for n=1..2000", all(abs(F(2*n+1, n+1) - 2) == F(1, n+1) for n in range(1, 2001)))
least = next(N for N in range(1, 5001) if all(abs(F(2*n+1, n+1)-2) < F(1, 1000) for n in range(N, 5001)))
check(f"L01 least N for 1/1000 is 1000 (got {least})", least == 1000)
check("L01 a_1000 = 2001/1001 = 1.999000999...", float(F(2001, 1001)) == 1.999000999000999)
check("L01 1/(n+1) < 1e-4 exactly when n >= 10000", all((F(1, n+1) < F(1, 10**4)) == (n >= 10000) for n in range(9990, 10010)))
def a(n): return F(2*n+1, n+1)
def b(n): return F(n+2, n)
check("L02 sum error = (n+2)/(n(n+1)), n=1..500", all(abs(a(n)+b(n)-3) == F(n+2, n*(n+1)) for n in range(1, 501)))
check("L02 product error = (3n+2)/(n(n+1)), n=1..500", all(abs(a(n)*b(n)-2) == F(3*n+2, n*(n+1)) for n in range(1, 501)))
check("L02 quotient error = (5n+4)/((n+1)(n+2)), n=1..500", all(abs(a(n)/b(n)-2) == F(5*n+4, (n+1)*(n+2)) for n in range(1, 501)))
check("L02 n=10 sum error 12/110 = 6/55", abs(a(10)+b(10)-3) == F(6, 55))
check("L02 n=100 product error 302/10100", abs(a(100)*b(100)-2) == F(302, 10100))
check("L02 n=1 quotient error 3/2", abs(a(1)/b(1)-2) == F(3, 2))
for k in range(1, 5):
    h = F(1, 10**k)
    check(f"L03 gap k={k} equals 1+4h-h^2", (2*(1+h)) - (1-h)**2 == 1 + 4*h - h*h)
check("L03 gap at h=0.1 is 1.39", F(139, 100) == 1 + F(4, 10) - F(1, 100))
check("L03 grid of 38 points (k=-19..19, k!=0)", len([k for k in range(-19, 20) if k != 0]) == 38)
check("L04 Q(h)=3+3h+h^2 for h=10^-1..10^-6", all(((1+h)**3 - 1)/h == 3 + 3*h + h*h for h in (F(1, 10**k) for k in range(1, 7))))
def p(x): return (x*x+1)*x**3
def pp(x): return 5*x**4 + 3*x*x
def q(x): return (x*x+1)/(x+2)
def qp(x): return (x*x+4*x-1)/(x+2)**2
def cp(x): return 6*x*(x*x+1)**2
for x in (F(3, 2), F(-1, 3), F(7, 5)):
    check(f"L05 product-rule expression equals p'(x) at {x}", 2*x*x**3 + (x*x+1)*3*x*x == pp(x))
    check(f"L05 chain-rule expression at {x}", 3*(x*x+1)**2*2*x == cp(x))
check("L05 p'(1.5)=32.0625", pp(F(3, 2)) == F(513, 16))
check("L05 q'(1.5)=29/49", qp(F(3, 2)) == F(29, 49))
check("L05 c'(1.5)=95.0625", cp(F(3, 2)) == F(1521, 16))
x = F(3, 2); H = F(1, 10**4)
exact_err_q = (q(x+H)-q(x-H))/(2*H) - qp(x)
lead_q = H*H*(-30/(x+2)**4)/6
print(f"  L05 q exact central-difference error = {float(exact_err_q):.6e}; leading h^2 q'''/6 = {float(lead_q):.6e}; ratio {float(exact_err_q/lead_q):.7f}")
check("L05 exact error = h^2 q'''/6 to 1e-5 relative at h=1e-4 (leading-order sentence holds)", abs(float(exact_err_q/lead_q) - 1) < 1e-5)
X = 1.5; Hf = 1e-4
qf = lambda t: (t*t+1.0)/(t+2.0)
float_err = (qf(X+Hf)-qf(X-Hf))/(2*Hf) - (X*X+4*X-1)/(X+2)**2
print(f"  L05 q float central-difference error = {float_err:.6e}; float minus exact = {float_err - float(exact_err_q):.3e} (double-precision round-off)")
f = lambda t: (t if t < 1 else F(-5))
check("L06 counterexample: f(x)=x on [0,1), f(1)=-5: f'=1>0 on (0,1), but f(1/2) > f(1)", f(F(1, 2)) > f(F(1)))
print("ALL OK" if ok else "SOME CHECK FAILED (see FAIL lines)")
