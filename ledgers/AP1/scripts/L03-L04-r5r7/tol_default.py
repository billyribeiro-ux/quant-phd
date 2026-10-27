import inspect
from scipy.optimize import _linprog_highs as m
src = inspect.getsource(m)
import re
print(re.findall(r"primal_feasibility_tolerance.*?\n", src)[:6])
print("default None -> HiGHS option default:", "primal_feasibility_tolerance" in src)
