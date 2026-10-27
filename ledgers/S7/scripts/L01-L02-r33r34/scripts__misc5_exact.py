"""Exact probability that a two-sided 5% z-test on iid N(0,1) data (no drift) rejects at some look among 756 daily looks,
by a grid recursion over the partial sum S_t (killed when |S_t| >= 1.959964 sqrt(t)). Lab 4 simulates 0.506 for this quantity."""
import math
import numpy as np
from scipy import stats
from scipy.signal import fftconvolve

c = stats.norm.ppf(0.975)
N = 756
dx = 0.01
half = 130.0
x = np.arange(-half, half + dx / 2, dx)
kx = np.arange(-7.0, 7.0 + dx / 2, dx)
kern = stats.norm.pdf(kx) * dx
kern /= kern.sum()
p = np.zeros_like(x)
p[np.argmin(np.abs(x))] = 1.0
surv = []
for t in range(1, N + 1):
    p = fftconvolve(p, kern, mode="same")
    p[np.abs(x) >= c * math.sqrt(t)] = 0.0
    surv.append(float(p.sum()))
print(f"grid: points={x.size}, dx={dx}, looks={N}, kernel points={kx.size}")
print(f"survival after 756 looks = {surv[-1]:.6f}")
print(f"P(reject at some look among 1..756) = {1 - surv[-1]:.4f}")
print(f"P(reject by look 5) = {1 - surv[4]:.4f}; by look 36 = {1 - surv[35]:.4f}; by look 252 = {1 - surv[251]:.4f}")
