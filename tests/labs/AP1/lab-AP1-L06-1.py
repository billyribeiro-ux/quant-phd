import itertools
import math

# SIMULATED two-period tree: the stock moves up (x1.2) or down (x0.9) each period; the bond earns 2% a period.
# Discounted prices S_t / B_t must be a Q-martingale node by node (Theorem 3.3).
up, down, rate, s0, p_up = 1.2, 0.9, 0.02, 100.0, 0.6
q = (1 + rate - down) / (up - down)  # one-step risk-neutral probability of "up"
print(f"one-step q(up) = {q:.6f}  (no arbitrage needs 0 < q < 1: down < 1 + r < up)")

paths = list(itertools.product((1, 0), repeat=2))  # 1 = up
q_path = {w: math.prod(q if u else 1 - q for u in w) for w in paths}
p_path = {w: math.prod(p_up if u else 1 - p_up for u in w) for w in paths}  # the physical measure P
density = {w: q_path[w] / p_path[w] for w in paths}  # Radon-Nikodym derivative dQ/dP on the four paths
print("paths (1 = up):", paths)
print("Q of each path:", [round(q_path[w], 6) for w in paths])
print("dQ/dP on paths:", [round(density[w], 6) for w in paths])
print("E_P[dQ/dP] =", round(sum(p_path[w] * density[w] for w in paths), 12))


def stock(node: tuple[int, ...]) -> float:
    """Stock price after the moves in `node` (1 = up, 0 = down)."""
    return s0 * math.prod(up if u else down for u in node)


for node in [(), (1,), (0,)]:
    t = len(node)
    nxt = [stock((*node, u)) / (1 + rate) ** (t + 1) for u in (1, 0)]
    mart = q * nxt[0] + (1 - q) * nxt[1]
    print(f"node {node}: discounted price {stock(node) / (1 + rate) ** t:.6f}, E_Q[next discounted] {mart:.6f}")

# A call struck at 100 paying at date 2, valued as E_Q[payoff / B_2].
value = sum(q_path[w] * max(stock(w) - 100.0, 0.0) for w in paths) / (1 + rate) ** 2
print(f"call value E_Q[(S_2 - 100)^+ / B_2] = {value:.6f}")

# If the bond paid 25% a period, 1 + r > up: shorting the stock and buying bonds is an arbitrage.
bad_rate = 0.25
bad_q = (1 + bad_rate - down) / (up - down)
gain = [round(s0 * (1 + bad_rate) ** 2 - stock(w), 2) for w in paths]
print(f"rate {bad_rate:.2f}: q(up) = {bad_q:.4f}; short 1 share into bonds, date-2 gain by path: {gain}")
