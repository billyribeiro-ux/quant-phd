"""Independent recomputation of the SC1 L07 exact walk tails and the standard-error arithmetic (stdlib, read-only)."""
import math

def tail_max_at_least(n, m):
    # Count length-n walks with running max >= m via the reflection identity, computed from binomials directly:
    # #{M_n >= m} = #{S_n >= m} + #{S_n > m}; S_n = 2u - n with u up-steps.
    ge = sum(math.comb(n, u) for u in range(n + 1) if 2 * u - n >= m)
    gt = sum(math.comb(n, u) for u in range(n + 1) if 2 * u - n > m)
    return (ge + gt) / 2 ** n

for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    print(f"N={n} m={m} P(M_N>=m)={tail_max_at_least(n, m):.6f}")
print("2(1-Phi(1)) =", f"{math.erfc(1 / math.sqrt(2)):.10f}")
# E2: S_16 >= 4 means u >= 10; S_16 > 4 means u >= 11
print("S16>=4 count", sum(math.comb(16, u) for u in range(16 + 1) if 2 * u - 16 >= 4),
      "S16>4 count", sum(math.comb(16, u) for u in range(17) if 2 * u - 16 > 4))
# E3: SE of proportion k/n with divisor n-1
k, n = 121, 400
print("SE k=121 n=400:", f"{math.sqrt(k * (n - k) / (n * n * (n - 1))):.6f}")
print("E[M_1] =", f"{math.sqrt(2 / math.pi):.9f}")
