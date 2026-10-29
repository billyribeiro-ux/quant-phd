import numpy as np
C = np.array([[1,0.7,0.3,-0.6],[0.7,1,0.5,0.4],[0.3,0.5,1,0.2],[-0.6,0.4,0.2,1]], float)
v = np.array([0.10,0.20,0.15,0.30])
w, V = np.linalg.eigh(C)
print('min eig', f'{w.min():.6f}')
X = V @ np.diag(np.maximum(w,0)) @ V.T
d = np.diag(X); Y = X / np.sqrt(np.outer(d,d))
print('clip dist', f'{np.linalg.norm(Y-C):.6f}', 'diag dev', f'{np.abs(np.diag(Y)-1).max():.2e}')
# Dykstra independent: alternating projections with Dykstra corrections via numpy
def psd(M):
    ww,VV = np.linalg.eigh((M+M.T)/2); return VV @ np.diag(np.maximum(ww,0)) @ VV.T
x = C.copy(); ps = np.zeros_like(C); pu = np.zeros_like(C)
for it in range(5000):
    y = psd(x+ps); ps = x+ps-y
    xn = y+pu; np.fill_diagonal(xn,1.0); pu = y+pu-xn
    done = np.linalg.norm(xn-y)<=1e-12 and np.linalg.norm(xn-x)<=1e-12
    x = xn
    if done: break
print('proj dist', f'{np.linalg.norm(x-C):.6f}', 'iters', it+1, 'min eig proj', f'{np.linalg.eigvalsh(x).min():.2e}')
print('entry diff', f'{np.abs(x-Y).max():.6f}', 'gap', f'{np.linalg.norm(Y-C)-np.linalg.norm(x-C):.6f}')
S_ = np.diag(v) @ C @ np.diag(v)
u = np.linalg.solve(S_, np.ones(4)); print('weights', ' '.join(f'{t:.6f}' for t in u/u.sum()), 'det', f'{np.linalg.det(C):.6f}')
# A3 two-asset closed form check with random a,b,rho
rng = np.random.default_rng(1)
err=0
for _ in range(1000):
    a,b = rng.uniform(0.05,0.5,2); r = rng.uniform(-0.99,0.99)
    S2 = np.diag([a,b]) @ np.array([[1,r],[r,1]]) @ np.diag([a,b])
    u2 = np.linalg.solve(S2, np.ones(2)); u2/=u2.sum()
    den = a*a+b*b-2*r*a*b
    cf = np.array([b*(b-r*a), a*(a-r*b)])/den
    err=max(err,np.abs(u2-cf).max())
print('A3 closed form max err', f'{err:.2e}')
