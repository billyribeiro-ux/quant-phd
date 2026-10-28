import sys
import numpy as np
sys.path.insert(0, "/tmp/verifyB2-M3-d/course/modules/M/M3/grader")
import reference as ref
C = np.array([[1.0, 0.7, 0.3, -0.6], [0.7, 1.0, 0.5, 0.4], [0.3, 0.5, 1.0, 0.2], [-0.6, 0.4, 0.2, 1.0]])
v = np.array([0.10, 0.20, 0.15, 0.30])
for name, M in [("clip", np.array(ref.clip_repair(C.tolist()))), ("proj", np.array(ref.projection_repair(C.tolist())))]:
    S = np.diag(v) @ M @ np.diag(v)
    vals, vecs = np.linalg.eigh(S)
    u = vecs[:, 0]
    print(name, "smallest eigenvalue of Sigma:", vals[0], "| normalised null vector (sum 1):", np.round(u / u.sum(), 6), "| sum of u:", u.sum())
    print("   residual |Sigma u|:", np.linalg.norm(S @ u))
