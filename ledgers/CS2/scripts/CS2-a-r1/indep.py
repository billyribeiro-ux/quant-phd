import random, math
from fractions import Fraction
# independent re-implementation of L02 lab keys and lookups
M = 2654435761
def b(k, m): return ((k*M) % 2**32) % m
rng = random.Random(2026)
keys = rng.sample(range(10**9), 256)
ks = set(keys)
absent = [x for x in rng.sample(range(10**9), 2000) if x not in ks][:500]
def build(n):
    ch = [[] for _ in range(64)]
    for k in keys[:n]:
        c = ch[b(k,64)]
        if k not in c: c.append(k)
    return ch
def succ(ch, k):
    c = ch[b(k,64)]; return c.index(k)+1
def unsucc(ch, k):
    return len(ch[b(k,64)])
for n in (16,32,64,128,256):
    ch = build(n)
    st = sum(succ(ch,k) for k in keys[:n]); ut = sum(unsucc(ch,k) for k in absent)
    print(n, "succ total", st, "exact avg", Fraction(st,n), float(Fraction(st,n)), "model", float(1+Fraction(n-1,128)),
          "unsucc total", ut, "exact", Fraction(ut,500), float(Fraction(ut,500)))
# L02 misconception 3 claim: increase of successful avg n=128 -> 256
s128 = Fraction(sum(succ(build(128),k) for k in keys[:128]),128); s256=Fraction(sum(succ(build(256),k) for k in keys[:256]),256)
print("increase", float(s256-s128), "n/(2m) at n=128:", Fraction(128,128), "(n-1)/(2m) at 128:", Fraction(127,128))
# L04 checks
lb = math.factorial(1024)
print("ceil log2 1024!", (lb-1).bit_length(), "check via bit_length ok")
print("log2(1024!)", math.log2(lb))
print("5120/8770", 5120/8770, "262431/8886", 262431/8886)
print("ceil log2 1000!", (math.factorial(1000)-1).bit_length())
