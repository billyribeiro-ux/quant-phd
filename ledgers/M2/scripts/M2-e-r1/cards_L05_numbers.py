from fractions import Fraction as F
h = 1e-4
p = lambda x: (x**2+1)*x**3
c = lambda x: (x**2+1)**3
q = lambda x: (x**2+1)/(x+2)
cd = lambda f,x: (f(x+h)-f(x-h))/(2*h)
print('p central', f"{cd(p,1.5):.9f}", 'abs diff', f"{abs(cd(p,1.5)-32.0625):.3e}")
print('q central diff', f"{abs(cd(q,1.5)-29/49):.3e}", 'q analytic', 29/49)
print('c central', f"{cd(c,1.5):.9f}", 'abs diff', f"{abs(cd(c,1.5)-95.0625):.3e}")
print('L4 Q(0.001)', (1.001**3-1)/0.001)
print('(a) 1-h', (1-1e-4)**2, '1+h', 2*(1+1e-4))
