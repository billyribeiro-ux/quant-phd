"""Print the unrounded values of Lab 2 (project-2 twin) by importing its functions; reads the twin's own code."""
import runpy, sys
ns = runpy.run_path(sys.argv[1], run_name="lab2_probe")  # runs main() once (prints); we recompute below
import math
gdp, price = ns["simulated_path"]()["gdp"], ns["simulated_path"]()["price"]
yields = ns["simulated_yields"](ns["simulated_path"]()["policy"])
latest = ns["QUARTERS"] - 1
intercept, slope = ns["trend_fit"](gdp, latest)
print("unrounded term spread", yields["cmt_10y"][latest] - yields["tbill_3m"][latest])
print("unrounded log gap", 100.0 * (math.log(gdp[latest]) - (intercept + slope * (ns["WINDOW"] - 1))))
