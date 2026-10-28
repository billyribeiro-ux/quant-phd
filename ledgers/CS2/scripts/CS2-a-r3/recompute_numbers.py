"""Independent recomputation of the CS2-a numbers from first principles (not from the lab code).

Usage: python recompute_numbers.py. Prints the exact values that the pages state.
"""
import math
from fractions import Fraction
import random

# ---- L02: hash table, independent re-implementation of the lab's keys and bucket map
M = 2654435761
def bucket(x, m=64):
    return ((x * M) % 2**32) % m

rng = random.Random(2026)
keys = rng.sample(range(10**9), 256)
stored = set(keys)
absent_all = rng.sample(range(10**9), 2000)
absent = [x for x in absent_all if x not in stored][:500]
print("absent count", len(absent))

def chains_for(keyset):
    ch = [[] for _ in range(64)]
    for k in keyset:
        b = bucket(k)
        if k not in ch[b]:
            ch[b].append(k)
    return ch

def probes_succ(ch, k):
    c = ch[bucket(k)]
    return c.index(k) + 1

def probes_unsucc(ch, k):
    return len(ch[bucket(k)])

for n in (16, 32, 64, 128, 256):
    ch = chains_for(keys[:n])
    S = sum(probes_succ(ch, k) for k in keys[:n])
    U = sum(probes_unsucc(ch, k) for k in absent)
    model_s = Fraction(1) + Fraction(n - 1, 128)
    model_u = Fraction(n, 64)
    print(f"n={n} S_total={S} S_avg={Fraction(S, n)} ({float(Fraction(S,n)):.7f}) model_s={model_s} "
          f"gap_s={Fraction(S, n) - model_s} U_total={U} U_avg={Fraction(U, len(absent))} "
          f"U_avg_float={U/len(absent):.6f} model_u={model_u} gap_u={Fraction(U, len(absent)) - model_u}")
ch = chains_for([64 * j for j in range(1, 51)])
print("colliding buckets", sorted({bucket(64 * j) for j in range(1, 51)}),
      "succ total", sum(probes_succ(ch, 64 * j) for j in range(1, 51)),
      "unsucc probes for 3264", probes_unsucc(ch, 3264), "3264 in table", 3264 in set(64*j for j in range(1,51)))

# claim in L02 Misconception 3 / E1: 257/128, 193/64
print("257/128 =", Fraction(257, 128), float(Fraction(257,128)), " 193/64 =", Fraction(193, 64), " diff =", Fraction(193,64)-Fraction(257,128))
print("model increase 128->256:", Fraction(255, 128) - Fraction(127, 128))

# Prop 1.4 check: h(64j)=0 for j in 0..2000
assert all(bucket(64 * j) == 0 for j in range(0, 2001))
# P1 / E2 checks
print("50*51/2 =", 50*51//2, " avg", Fraction(1275, 50), float(Fraction(1275,50)))
# example 2.5
print("64^-49 check: 64*(1/64)^50 == 64^-49 :", Fraction(64) * Fraction(1, 64)**50 == Fraction(1, 64**49))

# ---- L04
print("ceil log2(1024!) =", math.ceil(math.log2(math.factorial(1024))) if False else (math.factorial(1024).bit_length() - 1 if (math.factorial(1024) & (math.factorial(1024)-1)) else math.factorial(1024).bit_length() - 1))
L = math.log2(math.factorial(1024))
print("log2(1024!) =", repr(L))
print("ceil(log2(1024!)) via exact integer test:", next(c for c in range(20000) if 2**c >= math.factorial(1024)))
print("5120/8770 =", 5120/8770, " 262431/8886 =", 262431/8886, " 4737/8886 +29 =", 29 + 4737/8886)
print("log2(1000!) =", math.lgamma(1001)/math.log(2), " 500*log2(500)=", 500*math.log2(500))
print("(1000/2)log2(500) =", 500*math.log2(500))
# Part C margin at n=2 is 1; check min margin over 2..1000 using exact log2(n!)
def log2fact(n):
    return sum(math.log2(k) for k in range(2, n+1))
margins = [(log2fact(n) - (n/2)*math.log2(n/2), n) for n in range(2, 1001)]
print("min margin (approx)", min(margins))
# Part D, sum of gaps
print("sum (n+1) for n=1..1000 =", sum(n+1 for n in range(1,1001)))
# Remark 1.4(c) and merge sort 2^k
print("k*2^(k-1) at k=10:", 10*2**9)
# 1000! in lab: log2(1000!) fixed 8529.3980?
print("log2(1000!) 4dp", f"{log2fact(1000):.4f}")
