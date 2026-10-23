import numpy as np

# Lesson 5, Example 5.3: three states, one traded payoff z that is negative in state 3.
probs = np.array([0.25, 0.5, 0.25])
m_true = np.array([1.2, 0.9, 0.8])  # a strictly positive SDF: the market is free of arbitrage
z = np.array([3.0, 1.0, -1.0])
price = float(probs @ (m_true * z))
x_star = z * price / float(probs @ z**2)  # projection of m_true on span{z}
print(f"price of z: {price:.4f}")
print("x* by state:", np.round(x_star, 6), "| x* prices z:", round(float(probs @ (x_star * z)), 6))
print(f"E[x*^2] = {probs @ x_star**2:.6f} <= E[m^2] = {probs @ m_true**2:.6f}")

# The SDF with the least second moment among those with m >= floor that price z is m = max(lam * z, floor),
# with lam set so that E[m z] = price (pointwise minimization of m^2 - 2 lam m z over m >= floor).
for floor in (0.0, 0.1, 0.5):
    lam_lo, lam_hi = 0.0, 10.0
    for _ in range(200):
        lam = 0.5 * (lam_lo + lam_hi)
        if probs @ (np.maximum(lam * z, floor) * z) < price:
            lam_lo = lam
        else:
            lam_hi = lam
    m_pos = np.maximum(lam * z, floor)
    print(
        f"floor {floor:.1f}: m = {np.round(m_pos, 4)}, prices z: {round(float(probs @ (m_pos * z)), 6)}, "
        f"E[m^2] = {probs @ m_pos**2:.4f}"
    )
