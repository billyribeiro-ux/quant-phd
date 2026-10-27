# Independent re-implementation of Lab 4 (L04) from the embedded CSV, to recheck the printed numbers.
import csv, sys
import numpy as np
rows = list(csv.reader(open(sys.argv[1], encoding="utf-8", newline="")))
hdr = rows[0]
cols = hdr[1:]
data = [[float(v) if v else np.nan for v in r[1:]] for r in rows[1:]]
A = np.array(data)
ok = ~np.isnan(A).any(axis=1)
first = int(np.argmax(ok))
keep = [i for i, c in enumerate(cols) if c != "DKK"]
P = A[:, keep]
names = [cols[i] for i in keep]
X = P[first + 1:] / P[first:-1]
T = X.shape[0]
G = X.T @ X / T
b = np.linalg.solve(G, np.ones(len(keep)))
m = X @ b
print("T", T, "names", names)
print("max abs E_T[x* x]-1 (repr)", float(np.abs(X.T @ m / T - 1).max()))
print("mean %.4f sd %.4f min %.4f max %.4f" % (m.mean(), m.std(), m.min(), m.max()))
print("weights", np.round(b, 2).tolist())
