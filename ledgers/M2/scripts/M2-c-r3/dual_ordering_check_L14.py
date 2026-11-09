"""Does the L14 lab Dual class support a comparison x > 0 (needed by the branch example in Section 6)? (verifier round 3)"""
import io, contextlib, runpy
with contextlib.redirect_stdout(io.StringIO()):
    ns = runpy.run_path("tests/labs/M2/lab-M2-L14-1.py", run_name="lab")
Dual = ns["Dual"]
try:
    print("Dual(0,1) > 0 ->", Dual(0.0, 1.0) > 0)
except TypeError as ex:
    print("TypeError:", ex)
