"""Independent recomputation of CS2 L05-L08 numbers (round 4, CS2-b). Written from the page text, not from the lab code."""
import math
from functools import lru_cache

# ---- L05 numbers
phi = (1 + 5 ** 0.5) / 2
N = [0, 1]
for h in range(2, 13):
    N.append(1 + N[h - 1] + N[h - 2])
print("L05 N(0..7)", N[:8])
print("L05 1/log2(phi) = %.9f" % (1 / math.log2(phi)))
print("L05 ln3/lnphi = %.4f ; ln8/lnphi = %.4f ; ln377/lnphi = %.4f ; ln65/lnphi = %.4f ; ln501/lnphi = %.4f"
      % (math.log(3) / math.log(phi), math.log(8) / math.log(phi), math.log(377) / math.log(phi),
         math.log(65) / math.log(phi), math.log(501) / math.log(phi)))
print("L05 ln377=%.4f lnphi=%.4f" % (math.log(377), math.log(phi)))
print("L05 272/500 = %.4f ; 63+53+2*(55+57) = %d" % (272 / 500, 63 + 53 + 2 * (55 + 57)))
print("L05 phi^h <= N(h)+1 for h=1..12:", all(N[h] + 1 >= phi ** h for h in range(1, 13)))
print("L05 M3 N(5)=", N[5], " R3 N(5)=", N[5])

# ---- L06 numbers
print("L06 40000/1438 = %.4f ; 1238/200 = %.2f ; 2*619=%d ; 772-200=%d ; 440 pairs=%d ; 1080 = %d"
      % (40000 / 1438, 1238 / 200, 2 * 619, 772 - 200, 8 * (3 + 6 + 10 + 15 + 21), 8 * (9 + 16 + 25 + 36 + 49)))

# ---- L07 numbers
def f_table(D, A):
    INF = float("inf")
    f = [0] + [INF] * A
    for a in range(1, A + 1):
        f[a] = min([1 + f[a - c] for c in D if c <= a] or [INF])
    return f
print("L07 f(0..6) for {1,3,4} =", f_table((1, 3, 4), 6))
print("L07 f(9) for {2,5} =", f_table((2, 5), 9)[9], " f(7)=", f_table((2, 5), 9)[7], " f(4)=", f_table((2, 5), 9)[4])
print("L07 f(0..1024) for {1,3,4} contains", len(f_table((1, 3, 4), 1024)), "entries (amount 1024 table length)")
print("L07 2^40 bits =", (2 ** 40).bit_length(), " 2^40 =", 2 ** 40, " > 1e12:", 2 ** 40 > 10 ** 12)
print("L07 2^20+1 =", 2 ** 20 + 1, " bits(2^20)=", (2 ** 20).bit_length())
print("L07 bits(1000)=", (1000).bit_length())
# largest-coin-first for {1,3,4} amount 6
def greedy(D, a):
    used = 0
    while a:
        a -= max(c for c in D if c <= a)
        used += 1
    return used
print("L07 greedy(6) for {1,3,4} =", greedy((1, 3, 4), 6), "; greedy 1..6:", [greedy((1, 3, 4), a) for a in range(1, 7)])
print("L07 f(1..6) =", f_table((1, 3, 4), 6)[1:])
# LCS of AB, BA and ACGTACG / TGCATGC
def lcs(x, y):
    m, n = len(x), len(y)
    T = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            T[i][j] = T[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else max(T[i - 1][j], T[i][j - 1])
    return T[m][n]
print("L07 LCS(AB,BA)=", lcs("AB", "BA"), " LCS(ACGTACG,TGCATGC)=", lcs("ACGTACG", "TGCATGC"))

# memo counts for the LCS pair (independent)
def memo_counts(x, y):
    cache = {}
    calls = [0]
    def go(i, j):
        calls[0] += 1
        if i == 0 or j == 0:
            return 0
        if (i, j) in cache:
            return cache[(i, j)]
        v = go(i - 1, j - 1) + 1 if x[i - 1] == y[j - 1] else max(go(i - 1, j), go(i, j - 1))
        cache[(i, j)] = v
        return v
    go(len(x), len(y))
    return len(cache), calls[0]
def naive_calls(x, y):
    calls = [0]
    def go(i, j):
        calls[0] += 1
        if i == 0 or j == 0:
            return 0
        if x[i - 1] == y[j - 1]:
            return go(i - 1, j - 1) + 1
        return max(go(i - 1, j), go(i, j - 1))
    go(len(x), len(y))
    return calls[0]
print("L07 memo stored/calls =", memo_counts("ACGTACG", "TGCATGC"), " naive calls =", naive_calls("ACGTACG", "TGCATGC"))
# coins amount 20, {1,3,4}: memo stored, calls, naive calls
def coin_memo_counts(D, A):
    cache = {}
    calls = [0]
    def best(a):
        calls[0] += 1
        if a == 0:
            return 0
        if a in cache:
            return cache[a]
        r = min([1 + best(a - c) for c in D if c <= a])
        cache[a] = r
        return r
    r = best(A)
    return r, len(cache), calls[0]
def coin_naive(D, A):
    calls = [0]
    def best(a):
        calls[0] += 1
        if a == 0:
            return 0
        return min([1 + best(a - c) for c in D if c <= a])
    best(A)
    return calls[0]
print("L07 coins(1,3,4) amount 20: (fewest, stored, memo calls) =", coin_memo_counts((1, 3, 4), 20), " naive =", coin_naive((1, 3, 4), 20))

# ---- L08 independent order book (list-based, no sorted structure), same seeded stream as Part B/C
MULT, INC, MOD = 1103515245, 12345, 2 ** 31
class G:
    def __init__(self, s): self.s = s % MOD
    def below(self, n):
        self.s = (MULT * self.s + INC) % MOD
        return (self.s >> 16) % n
g = G(20261029)
orders = []   # live resting: dict(oid, side, price, qty, seq)
trades_total = 0; cancels = 0; traded_msgs = 0; new = 0
creations = 0; removals = 0
def level_exists(side, price):
    return any(o["side"] == side and o["price"] == price for o in orders)
for step in range(400):
    live = sorted(o["oid"] for o in orders)
    if live and g.below(100) < 25:
        oid = live[g.below(len(live))]
        victim = [o for o in orders if o["oid"] == oid][0]
        before = level_exists(victim["side"], victim["price"])
        orders.remove(victim)
        cancels += 1
        if not level_exists(victim["side"], victim["price"]):
            removals += 1
    else:
        side = "B" if g.below(2) == 0 else "S"
        price = 10000 - 20 + g.below(41)
        qty = 1 + g.below(20)
        new += 1
        oid = new
        rem = qty
        opp = "S" if side == "B" else "B"
        if side == "B":
            cands = sorted([o for o in orders if o["side"] == "S" and o["price"] <= price], key=lambda o: (o["price"], o["oid"]))
        else:
            cands = sorted([o for o in orders if o["side"] == "B" and o["price"] >= price], key=lambda o: (-o["price"], o["oid"]))
        tr = 0
        for o in cands:
            if rem == 0:
                break
            f = min(rem, o["qty"])
            o["qty"] -= f; rem -= f; tr += 1
        trades_total += tr
        traded_msgs += bool(tr)
        before_levels = {(o["side"], o["price"]) for o in orders}
        orders = [o for o in orders if o["qty"] > 0]
        removals += len(before_levels - {(o["side"], o["price"]) for o in orders})
        if rem > 0:
            if not level_exists(side, price):
                creations += 1
            orders.append({"oid": oid, "side": side, "price": price, "qty": rem})
bids = [o["price"] for o in orders if o["side"] == "B"]; asks = [o["price"] for o in orders if o["side"] == "S"]
print("L08 independent: new", new, "cancels", cancels, "traded msgs", traded_msgs, "executions", trades_total,
      "resting", len(orders), "best bid", max(bids) if bids else None, "best ask", min(asks) if asks else None,
      "levels created", creations, "removed", removals)
