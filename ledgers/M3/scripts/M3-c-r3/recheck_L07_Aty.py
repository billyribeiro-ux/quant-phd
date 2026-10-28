import numpy as np
from fractions import Fraction
rng = np.random.default_rng(7)
n=12
x1=rng.normal(size=n); x2=rng.normal(size=n); noise=rng.normal(scale=0.3,size=n)
y=1.5+0.8*x1-0.4*x2+noise
a=np.column_stack([np.ones(n),x1,x2])
print("A^T y", a.T@y)
print("A^T y rounded 2dp", np.round(a.T@y,2))
print("rank Gram", np.linalg.matrix_rank(a.T@a))
# E1 bound from unrounded values in lab L08
