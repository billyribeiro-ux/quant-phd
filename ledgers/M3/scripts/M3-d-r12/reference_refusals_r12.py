"""Round-12 verifier (M3 slice d): the reference refuses an asymmetric (1e-1) matrix under non-default arguments,
as project.html line 237 requires for each function where the named condition applies. Run from the checkout root
with python -I."""

import importlib.util

spec = importlib.util.spec_from_file_location("ref", "course/modules/M/M3/grader/reference.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
bad = [[1.0, 0.3], [0.5, 1.0]]
for name, call in [
    ("is_psd tol=1e-5", lambda: m.is_psd(bad, tol=1e-5)),
    ("projection_repair tol=1e-6", lambda: m.projection_repair(bad, tol=1e-6)),
    ("projection_repair max_iter=3", lambda: m.projection_repair(bad, max_iter=3)),
    ("clip_repair floor=0.1", lambda: m.clip_repair(bad, floor=0.1)),
    ("min_eigenvalue (default)", lambda: m.min_eigenvalue(bad)),
]:
    try:
        call()
        print(name, "no error")
    except ValueError:
        print(name, "ValueError")
