from fractions import Fraction
import itertools
ok = True
for N in range(1, 13):
    paths = list(itertools.product((1, -1), repeat=N))
    w = Fraction(1, 2**N)
    es2 = sum(w * sum(paths_i) ** 2 for paths_i in ([0] + list(itertools.accumulate(p)) and [0]) ) if False else None
    es2 = Fraction(0)
    worst = Fraction(0)
    for p in paths:
        s = list(itertools.accumulate(p))
        es2 += w * s[-1] ** 2
    assert es2 == N, (N, es2)
    for c2 in range(1, 4 * N * N + 2):  # c = sqrt(c2)/2 grid on c^2 = c2/4
        c_sq = Fraction(c2, 4)
        prob = w * sum(1 for p in paths if max(v * v for v in [0] + list(itertools.accumulate(p))) >= c_sq)
        if prob > Fraction(N) / c_sq:
            ok = False
            print("violation", N, c_sq, prob)
print("E[S_N^2]=N for N=1..12:", True, " P(max|S_k|>=c) <= N/c^2 on grid c^2=k/4:", ok)
for s in (Fraction(0), Fraction(2), Fraction(-1, 2), Fraction(7, 3)):
    assert Fraction(1, 2) * ((s + 1) ** 2 + (s - 1) ** 2) == s * s + 1
print("half((s+1)^2+(s-1)^2)=s^2+1 at sample points: True")
# L10 card numbers
K = 1000
m = (K + 1).bit_length() - 1
print("K=1000 m", m, "win prob", 1 - Fraction(1, 2**m), float(1 - Fraction(1, 2**m)), "ruin wealth", K + 1 - 2**m, "E", (1 - Fraction(1, 2**m)) * (K + 1) + Fraction(1, 2**m) * (K + 1 - 2**m))
for n in (1, 2, 3, 5, 10):
    print("n", n, "P(tau>n)=", Fraction(1, 2**n), "D on all-loss", -(2**n - 1), "check D=-(2^n-1)", sum(-(2**j) for j in range(n)) == -(2**n - 1))
