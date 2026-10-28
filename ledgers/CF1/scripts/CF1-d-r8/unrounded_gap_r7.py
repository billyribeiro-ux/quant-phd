"""Unrounded values behind the printed Lab 3 numbers (project page, Monte Carlo paragraph). Usage: python -I this.py <checkout>"""
import math
import pathlib
import sys

src = pathlib.Path(sys.argv[1], "tests/labs/CF1/lab-CF1-project-3.py").read_text()
ns: dict = {}
exec(src.rsplit("main()", 1)[0], ns)
base = ns["project_flows"](1.0)
det = ns["npv"](ns["RATE"], base)
draws = ns["monte_carlo_draws"](0.2, 2000, 42)
n = len(draws)
mean = sum(draws) / n
sd = math.sqrt(sum((d - mean) ** 2 for d in draws) / (n - 1))
se = sd / math.sqrt(n)
print(f"det NPV {det!r}")
print(f"MC mean {mean!r}")
print(f"gap det-mean {det - mean!r}  (printed 926.00-885.85 = {926.00 - 885.85:.2f})")
print(f"sd {sd!r} se {se!r}")
print(f"gap/se {(det - mean) / se:.6f}; 40.15/54.68 = {40.15 / 54.68:.6f}; gap/se rounded-se {(det-mean)/54.68:.6f}")
print(f"negative share {sum(1 for d in draws if d < 0)/n:.6f}; 787/2000 = {787/2000:.6f}")
print(f"sd/mean {sd/mean:.6f}; 2445.52/885.85 = {2445.52/885.85:.6f}")
print(f"z-check 2000 draws: mean-one of m check (sum of exp terms) n/a; 2445.52 vs printed sd {sd:.2f}")
