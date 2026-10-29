from fractions import Fraction as F

S = 100
A = 100
K = [80, 90, 100, 110, 120]


def call(k, d):
    return max(S - d * k, 0) + F(max(A - k, 0), 10)


def holds(d):
    for k in K:
        c = call(k, d)
        p = c - S + d * k
        if not (0 <= c <= S and c >= max(S - d * k, 0) and 0 <= p <= d * k and p >= max(d * k - S, 0)):
            return False
    return True


print("D=1/41", holds(F(1, 41)), "D=1/40", holds(F(1, 40)), "D=1/100", holds(F(1, 100)), "D=9/10", holds(F(9, 10)), "D=2", holds(F(2)))
bad = [F(i, 1000) for i in range(1, 5000) if not holds(F(i, 1000))]
print("failing D in (0,5) step 1/1000: count", len(bad), "max", max(bad))
