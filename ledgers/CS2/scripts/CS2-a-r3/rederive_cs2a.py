# Independent re-derivation of numbers quoted in CS2 L01-L04 prose (verifier round 3).
import math
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_EVEN

# ---- L01 ----
print("L01 2+1/511 =", 2 + 1/511, " 1023/511 =", 1023/511, " 1/511 =", 1/511)
print("L01 1000n>n^2 first fail n:", next(n for n in range(1, 5000) if not n*n <= 1000*n))
print("L01 k=2..10 ratio 2+1/(2^(k-1)-1):", [round(2+1/(2**(k-1)-1),4) for k in range(2,11)])
print("L01 floor(1000)+1 =", math.floor(1000)+1)

# ---- L02 ----
M = 2654435761
def bucket_of(key, m=64):
    return ((key*M) % 2**32) % m
import random
rng = random.Random(2026)
keys = rng.sample(range(10**9), 256)
stored_all = set(keys)
absent = [x for x in rng.sample(range(10**9), 2000) if x not in stored_all][:500]
def build(n):
    chains = [[] for _ in range(64)]
    for k in keys[:n]:
        c = chains[bucket_of(k)]
        if k not in c: c.append(k)
    return chains
def look(chains, key):
    b = chains[bucket_of(key)]
    p = 0
    for s in b:
        p += 1
        if s == key: return True, p
    return False, p
print("L02 model check and totals:")
for n in (16, 32, 64, 128, 256):
    ch = build(n)
    succ = sum(look(ch, k)[1] for k in keys[:n])
    uns = sum(look(ch, k)[1] for k in absent)
    chainlen = max(len(c) for c in ch)
    print(f"  n={n} succ_total={succ} succ_avg={succ/n:.7f} uns_total={uns} uns_avg={uns/500:.7f} longest={chainlen} model_succ={1+(n-1)/128:.7f} alpha={n/64}")
    # integers whose quotient rounds (half-even, 4dp) to the printed value
    def ints_rounding(total_den, printed, lo_t, hi_t):
        return [t for t in range(lo_t, hi_t) if Decimal(t)/Decimal(total_den) == Decimal(t)/Decimal(total_den) and
                f"{round(t/total_den, 4):.4f}" == printed]
    ps = f"{succ/n:.4f}"; pu = f"{uns/500:.4f}"
    cand_s = [t for t in range(max(0,succ-3), succ+4) if f"{t/n:.4f}" == ps]
    cand_u = [t for t in range(max(0,uns-3), uns+4) if f"{t/500:.4f}" == pu]
    print(f"    printed succ {ps} integer totals rounding to it: {cand_s}; printed unsucc {pu} integer totals: {cand_u}")
    print(f"    succ gap measured-model = {succ/n - (1+(n-1)/128):+.7f}; unsucc gap = {uns/500 - n/64:+.7f}")

# colliding set
colliding = [64*j for j in range(1, 51)]
chc = [[] for _ in range(64)]
for k in colliding: chc[bucket_of(k)].append(k)
print("L02 colliding succ total", sum(look(chc,k)[1] for k in colliding), "miss", look(chc, 64*51))
print("L02 claim h(64j)=0 for j<2000:", all(bucket_of(64*j)==0 for j in range(2000)))
print("L02 Example 2.5 64^-49 =", 64**-49.0 if False else Fraction(64, 64**50))
print("L02 M2 73/64 =", 73/64, " 1+9/64 =", 1+9/64)
print("L02 257/128=", 257/128, "193/64=", 193/64, "772/256=", 772/256, "193*4==772", 193*4==772)
print("L02 model diff 256 vs 128:", (1+255/128)-(1+127/128), " measured:", 193/64-257/128)
print("L02 successful gaps:", [round(t/n-(1+(n-1)/128),7) for t,n in [(16,16),(37,32),(97,64),(257,128),(772,256)]])
print("L02 unsucc gaps:", [round(t/500-a,4) for t,a in [(134,0.25),(270,0.5),(548,1),(1016,2),(2014,4)]])

# ---- L03 ----
print("L03 6*4096*12 =", 6*4096*12, " minus 166912 =", 6*4096*12-166912)
print("L03 2*4096*4097 =", 2*4096*4097, " 4378444/that =", 4378444/(2*4096*4097))
print("L03 16: 107+98=", 107+98, " 241+361=", 241+361)
print("L03 128: 1617+4514=", 1617+4514, " 3802+4933=", 3802+4933)
print("L03 256: 3742+17663=", 3742+17663, " 8517+10623=", 8517+10623)
print("L03 92609/8192=", 92609/8192)
sl_moves = [98,284,1002,4514,17663,65561,269578,1086043,4378444]
sl_ratios = [round(b/a,4) for a,b in zip(sl_moves, sl_moves[1:])]
hp_moves = [361,929,2209,4933,10623,21095,42401,87863,181761]
hp_ratios = [round(b/a,4) for a,b in zip(hp_moves, hp_moves[1:])]
hp_cmp = [241,648,1625,3802,8517,17831,37178,78710,166912]
hp_cr = [round(b/a,4) for a,b in zip(hp_cmp, hp_cmp[1:])]
print("L03 sorted move ratios (N=64..4096):", sl_ratios)
print("L03 heap move ratios (N=64..4096):", hp_ratios)
print("L03 heap cmp ratios (N=64..4096):", hp_cr)
print("L03 heap cmp ratios N=512..4096:", hp_cr[3:])
print("L03 heap 1625/683? sorted cmp at 64:", 683)

# ---- L04 ----
print("L04 ceil log2 1024! =", (math.factorial(1024)-1).bit_length(), " log2(1024!)=", math.lgamma(1025)/math.log(2))
print("L04 5120/8770 =", 5120/8770)
print("L04 262431/8886 =", 262431/8886, "rounded", round(262431/8886, 2))
print("L04 margin check:")
ln2 = math.log(2.0)
margins = []
for n in range(2, 1001):
    lhs = math.lgamma(n+1)/ln2
    rhs = (n/2)*math.log2(n/2)
    margins.append((lhs-rhs, n))
print("  min margin", min(margins), " n=2 margin", margins[0])
print("  any margin < 1 for n>2 ?", [m for m in margins if m[1]>2 and m[0] < 1.0][:3])
print("L04 log2(1000!)=", math.lgamma(1001)/ln2, " 500 log2 500=", 500*math.log2(500))
print("L04 log2 3! ceil", math.ceil(math.log2(6)))
print("L04 n-choose-2 for 7:", 7*6//2)
print("L04 Part B lower ceil log2 n!:", [(n, (math.factorial(n)-1).bit_length(), n*(n-1).bit_length()) for n in range(2,8)])
print("L04 Part B upper n*ceil log2 n:", [(n, n*((n-1).bit_length())) for n in range(2,8)])
print("L04 gaps total:", sum(n+1 for n in range(1,1001)))
print("L04 2*4096 / rounding: 1024 sorted insertion n-1 =", 1023, " 10*2^9 =", 10*2**9)
