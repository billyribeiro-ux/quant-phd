import sys
sys.path.insert(0, ".")
import sensitivity_engine as sol

def check(name, fn):
    try:
        print(name, fn())
    except Exception as e:
        print(name, "EXC", type(e).__name__, e)

check("ad x^3 at 1e5 (want 3e10)", lambda: sol.ad_derivative(lambda x: x * x * x, 1e5))
check("fd central x^3 at 1e5 step 1e-6 (fd, for contrast)", lambda: sol.fd_derivative(lambda x: x * x * x, 1e5, 1e-6, "central"))
