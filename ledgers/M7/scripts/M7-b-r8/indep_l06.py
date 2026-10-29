from fractions import Fraction as F
# independent re-derivation: LCG per lab twin spec, solve with Gaussian elimination over Fractions
def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) % 2**31
        yield s
g = lcg(2026)
def draw(mod):
    return next(g) % mod
n = 4
M = [[F(draw(7) - 3) for _ in range(n)] for _ in range(n)]
mu = [F(draw(13) + 2, 100) for _ in range(n)]
Sig = [[sum(M[k][i]*M[k][j] for k in range(n))/F(16) + (F(1,10) if i==j else F(0)) for j in range(n)] for i in range(n)]
def solve(A, b):
    m = len(A); Ab = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(m):
        p = next(r for r in range(c, m) if Ab[r][c] != 0)
        Ab[c], Ab[p] = Ab[p], Ab[c]
        for r in range(m):
            if r != c and Ab[r][c] != 0:
                f = Ab[r][c]/Ab[c][c]
                Ab[r] = [Ab[r][k]-f*Ab[c][k] for k in range(m+1)]
    return [Ab[i][m]/Ab[i][i] for i in range(m)]
ones = [F(1)]*n
y = solve(Sig, mu); z = solve(Sig, ones)
for gam in [F(1), F(2), F(4), F(8), F(16)]:
    lam = (sum(y) - gam)/sum(z)
    w = [(y[i]-lam*z[i])/gam for i in range(n)]
    risk = sum(w[i]*Sig[i][j]*w[j] for i in range(n) for j in range(n))
    ret = sum(mu[i]*w[i] for i in range(n))
    print(float(gam), 'ret', round(float(ret),6), 'risk', round(float(risk),6), 'sum', sum(w)==1, 'lam', lam, 'sum z', sum(z))
print('mu', [str(v) for v in mu])
# M1 hand example
S2 = [[F(2),F(0)],[F(0),F(2)]]; mu2=[F(1,10),F(1,20)]
yy=solve(S2,mu2); zz=solve(S2,[F(1),F(1)]); lam=(sum(yy)-1)/sum(zz)
print('M1', yy, zz, lam, [yy[i]-lam*zz[i] for i in range(2)])
