"""Round-9 check: the reference rejects the two proposed three-position non-positive-pivot covariances in both families.
Usage: python -I <this file> from the checkout root."""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location("ref", pathlib.Path("course/modules/M/M4/grader/reference.py"))
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
for cov in ([[1e-4, 0, 0], [0, 1e-4, 0], [0, 0, -1e-4]], [[1, 0, 1], [0, 1, 1], [1, 1, 1]]):
    for fam, nu in (("gaussian", None), ("student_t", 5)):
        try:
            ref.simulate_losses([1000, 1000, 1000], cov, 10, 0, fam, nu)
            print("NO ERROR", fam, cov)
        except ValueError as e:
            print("ValueError", fam, str(e)[:60])
