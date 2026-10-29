import sys
sys.path.insert(0, "tests/labs/M2")
from fractions import Fraction
from importlib.machinery import SourceFileLoader
import runpy
ns = {}
src = open("tests/labs/M2/lab-M2-L23-1.py", encoding="utf-8").read().replace("\nmain()\n", "\n")
exec(compile(src, "twin", "exec"), ns)
price = ns["price"]
y = 0.04 + 0.01
print("float yield exact value minus 1/20:", Fraction(y) - Fraction(1, 20))
print("exact price at float yield minus face (cents):", float(price(y) - 100000))
print("exact price at rational 5% minus face:", price(Fraction(1, 20)) if False else "n/a")
