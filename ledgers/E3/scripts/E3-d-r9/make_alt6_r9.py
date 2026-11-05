# Round 9: alternative 6 (finite-difference step 1e-4 in the optimiser and the standard errors), built from the current reference.
import pathlib, sys
src = pathlib.Path("course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
assert src.count("_H = 1e-5  # finite-difference step in the transformed coordinates") == 1
out = src.replace("_H = 1e-5  # finite-difference step in the transformed coordinates", "_H = 1e-4  # ALT6: finite-difference step 1e-4 in transformed coordinates")
pathlib.Path("/tmp/E3d_r9_ws/alt6_elicit.py").write_text(out, encoding="utf-8")
print("alt6 written")
