"""Recompute the matrix of the projection (x, y) -> (x, 0) on R^2 in bases (e1, e2) and (e2, e1).

Columns are the coordinate vectors of L(b_j) in the output basis (here the same basis as the input).
Exact arithmetic with Fraction. Prints both matrices and the page's claimed matrices.
"""
from fractions import Fraction

def L(v):
    x, y = v
    return (x, Fraction(0))

def coords(basis, w):
    # solve w = x*b1 + y*b2 for a 2x2 basis given as two vectors (exact, Cramer's rule)
    (a, c), (b, d) = basis[0], basis[1]
    det = a * d - b * c
    x = (w[0] * d - b * w[1]) / det
    y = (a * w[1] - c * w[0]) / det
    return (x, y)

def matrix(basis_in, basis_out):
    cols = [coords(basis_out, L(b)) for b in basis_in]
    # matrix rows: row i, column j
    return [[cols[j][i] for j in range(2)] for i in range(2)]

e1 = (Fraction(1), Fraction(0))
e2 = (Fraction(0), Fraction(1))
print("basis (e1,e2):", matrix([e1, e2], [e1, e2]))
print("basis (e2,e1):", matrix([e2, e1], [e2, e1]))
print("page claim for (e2,e1): [[0,1],[0,0]]")
