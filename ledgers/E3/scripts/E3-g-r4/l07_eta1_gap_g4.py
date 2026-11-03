"""Check the L07 Exercise E3 claim: with eta = 1 the closed form differs from omega_1(p) = p by about 3.13e-1 on the 1001-point grid.

Usage: python -I l07_eta1_gap_g4.py   (stdlib only)
"""
import math

grid = [i / 1000 for i in range(1001)]


def omega(p: float, eta: float) -> float:
    if p in (0.0, 1.0):
        return p
    return p**eta / (p**eta + (1.0 - p) ** eta) ** (1.0 / eta)


closed = [math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p))) for p in grid]
gap_closed_vs_eta1 = max(abs(c - p) for c, p in zip(closed, grid))
gap_general_vs_identity_eta1 = max(abs(omega(p, 1.0) - p) for p in grid)
print(f"largest |closed form - p| on grid = {gap_closed_vs_eta1:.6e}")
print(f"largest |omega_eta=1(p) - p| on grid = {gap_general_vs_identity_eta1:.6e}")
