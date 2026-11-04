# Builds alternative 6 (finite-difference step 1e-4 in the optimiser and standard errors) from the reference, for seeds 0-9 runs.
import pathlib
src = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-d/course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
assert src.count("_H = 1e-5  # finite-difference step in the transformed coordinates") == 1
out = src.replace("_H = 1e-5  # finite-difference step in the transformed coordinates", "_H = 1e-4  # ALT6: finite-difference step 1e-4 in transformed coordinates")
pathlib.Path("/Users/billyribeiro/.fanout/scratch-E3-d-r8/alt6.py").write_text(out, encoding="utf-8")
print("alt6 written to scratch")
