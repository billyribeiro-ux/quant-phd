"""Round-5 independent re-derivation of every prose number in the M5-b slice (L05-L07)."""
import math
from fractions import Fraction as F

print("L05 2^50 =", 2**50)
for n in (10, 100, 1000):
    print(f"L05 0.99^{n} = {0.99**n:.10f}")
print("L05 least n with (1/2)^n < 1/1000:", min(n for n in range(1, 100) if F(1, 2**n) < F(1, 1000)))
print("L05 ln 0.99 =", f"{math.log(0.99):.8f}", " 100 ln 0.99 =", f"{100*math.log(0.99):.6f}", " exp =", f"{math.exp(100*math.log(0.99)):.5f}")
print("L05 (1/2)^9 =", F(1, 512), "(1/2)^10 =", F(1, 1024), "(1/2)^3 =", F(1, 8))

print("L06 1/4 - 12/49 =", F(1, 4) - F(12, 49), float(F(1, 4) - F(12, 49)))
print("L06 C(10,2) =", math.comb(10, 2), " width after step 8 =", F(1, 2**8), float(F(1, 256)))
xs = [F(k, 7) for k in range(8)]
best = max(xs, key=lambda x: (x * (1 - x), -x))
print("L06 sevenths argmax first", min((x for x in xs if x*(1-x) == max(y*(1-y) for y in xs))), "max", max(x*(1-x) for x in xs))
xs10 = [F(k, 10) for k in range(11)]
print("L06 tenths max", max(x*(1-x) for x in xs10), "at", [x for x in xs10 if x*(1-x) == max(y*(1-y) for y in xs10)])

beta = math.sin(1)
print("L07 sin1 =", f"{beta:.10f}", " cos1 =", f"{math.cos(1):.6f}")
x = 0.0
xbar = 0.7390851332151607
iters = [x]
for _ in range(30):
    x = math.cos(x); iters.append(x)
c = abs(iters[1] - iters[0])
for n in (0, 1, 2, 5, 10, 20, 30):
    err = abs(iters[n] - xbar)
    bound = beta**n * c / (1 - beta)
    print(f"L07 n={n} x_n={iters[n]:.6f} err={err:.6e} bound={bound:.6e} ok={err <= bound + 1e-12}")
print("L07 bound/err at n=5 =", (beta**5*c/(1-beta)) / abs(iters[5]-xbar), " 2.661258/0.05439523 =", 2.661258/0.05439523)
print("L07 all n 0..30 err<=bound:", all(abs(iters[n]-xbar) <= beta**n*c/(1-beta) + 1e-12 for n in range(31)))

# Part B: grid of 201 points on [0,1], all pairs and adjacent pairs
grid = [i/200 for i in range(201)]
q_all = max(abs(math.cos(a)-math.cos(b))/abs(a-b) for i,a in enumerate(grid) for b in grid[i+1:])
q_adj = max(abs(math.cos(grid[i])-math.cos(grid[i+1]))/(grid[i+1]-grid[i]) for i in range(200))
print("L07 B max over all pairs", f"{q_all:.15f}", " adjacent", f"{q_adj:.15f}", " sin1", f"{beta:.15f}")
print("L07 E3 sin1 - (cos .995 - cos 1)/0.005 =", f"{beta - (math.cos(0.995)-math.cos(1))/0.005:.10f}")
print("L07 E2 f'(5)=", f"{5/math.sqrt(26):.7f}", " f'(50)=", f"{50/math.sqrt(2501):.7f}")
# Part C grids
for W in (5, 50):
    g = [-W + 2*W*i/200 for i in range(201)]
    f = lambda t: math.sqrt(t*t+1)
    qm = max(abs(f(a)-f(b))/abs(a-b) for i,a in enumerate(g) for b in g[i+1:])
    qa = max(abs(f(g[i])-f(g[i+1]))/abs(g[i+1]-g[i]) for i in range(200))
    dmin = min(f(t)-t for t in g)
    print(f"L07 C W={W} max ratio all-pairs {qm:.6f} adjacent {qa:.6f} min f(x)-x {dmin:.6f} sqrt(W^2+1)-W {math.sqrt(W*W+1)-W:.7f}")
print("L07 M2 bound n=13", 3/3**13, " n=14", 3/3**14)
print("L07 R2 threshold n*", math.log(1/(1e-6*(1-beta)))/math.log(1/beta))
print("L07 R2 beta^90/(1-b)", beta**90/(1-beta), " beta^91/(1-b)", beta**91/(1-beta))
print("L07 E1 ratio", 2.661258/0.05439523)
print("L07 Ex 2.3 bound == error:", all(abs(3*3**-n - abs(3-(3-3*3**-n))) < 1e-15 for n in range(0, 30)))
