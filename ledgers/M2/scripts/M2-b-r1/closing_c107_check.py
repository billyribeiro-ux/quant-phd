# Closing-delta check of card M2-c107 (L08, Lab 1 part C) and of the printed digits it cites.
import math
x, n = 0.9, 1
xi = 1 - (1 - x) ** (1 / (n + 2))
exact = x ** (n + 1) / (1 - x)                      # R_n(x) for f = 1/(1-x), x0 = 0
f_np1 = lambda t: math.factorial(n + 1) / (1 - t) ** (n + 2)   # f^(n+1)(t)
lagr = f_np1(xi) * x ** (n + 1) / math.factorial(n + 1)
print(f"xi exact = {xi!r}")
print(f"xi printed (6 dp) = {xi:.6f}")
print(f"R_1(0.9) exact = {exact:.8f}")
print(f"Lagrange form at exact xi = {lagr:.8f}")
print(f"abs diff = {abs(lagr-exact):.3e}; 0 < xi < x: {0 < xi < x}")
print(f"Lagrange form at rounded xi 0.535841 = {f_np1(0.535841)*x**(n+1)/math.factorial(n+1):.8f}")
