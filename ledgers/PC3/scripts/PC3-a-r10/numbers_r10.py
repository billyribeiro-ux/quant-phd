"""Round-10 PC3 slice a: independent recomputation of the numbers in index.html, L01, L02 and L03 prose."""
import math
from fractions import Fraction as F
from itertools import product

def show(label, value):
    print(f"{label}: {value}")

print("== L01 Example 1.4 and Part 1")
lo, hi = F(12000), F(234000)
show("ratio", hi / lo)
show("ln 19.5", round(math.log(19.5), 10))
show("geometric midpoint", round(math.sqrt(12000 * 234000), 10))
show("geometric midpoint 2dp", f"{math.sqrt(12000 * 234000):.2f}")
show("geometric midpoint 4dp", f"{math.sqrt(12000 * 234000):.4f}")
show("factor widths", [round(math.log(v), 10) for v in (3, 5, 1.3)])
show("sum of factor widths", round(math.log(3) + math.log(5) + math.log(1.3), 10))
show("ln 1.3 4dp", f"{math.log(1.3):.4f}")
show("ln 3 4dp", f"{math.log(3):.4f}")
show("ln 5 4dp", f"{math.log(5):.4f}")

print("== L01 Part 2 narrowings")
base = math.log(19.5)
q_drop = math.log(10 / 2) - math.log(8 / 4)  # quote updates [2,10] -> [4,8]
s_drop = math.log(60 / 20) - math.log(40 / 20)
m_drop = math.log(390 / 300) - math.log(360 / 330)
show("symbols reduction", f"{s_drop:.10f}")
show("quote reduction", f"{q_drop:.10f}")
show("minutes reduction", f"{m_drop:.10f}")
show("quote share of baseline (float)", f"{q_drop / base * 100:.6f} percent")
show("minutes share of baseline (float)", f"{m_drop / base * 100:.6f} percent")
show("totals", [f"{base - d:.4f}" for d in (s_drop, q_drop, m_drop)])
print("== L01 E2 (new text at L01.html:408)")
show("four-place quotient 0.9163/2.9704", f"{0.9163 / 2.9704:.8f} = {100 * 0.9163 / 2.9704:.6f} percent")
show("four-place quotient to 2dp percent", f"{100 * 0.9163 / 2.9704:.2f}")
show("four-place quotient to 1dp percent", f"{100 * 0.9163 / 2.9704:.1f}")
show("full precision quote share", f"{0.9162907319 / 2.9704144656:.8f}")
show("full precision quote share percent 1dp", f"{100 * 0.9162907319 / 2.9704144656:.1f}")
show("full precision minutes share", f"{0.1753528875 / 2.9704144656:.8f}")
show("full precision minutes share percent 1dp", f"{100 * 0.1753528875 / 2.9704144656:.1f}")
show("full precision share 6dp", f"{0.9162907319 / 2.9704144656:.6f}")
show("minutes share 6dp", f"{0.1753528875 / 2.9704144656:.6f}")

print("== L01 Part 3 and Example 1.7")
for n in (2, 5, 10):
    for x in (F(1, 100), F(1, 20)):
        rem = (1 + x) ** n - 1 - n * x
        bnd = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
        print(f"n={n} x={x}: rem={float(rem):.10f} bound={float(bnd):.10f} rem<=bound={rem <= bnd}")
rem = float((F(101, 100)) ** 10 - 1 - F(10, 100))
bnd = 45 * (1.01 ** 8) * 0.0001
show("Ex1.7 remainder", f"{rem:.10f}")
show("Ex1.7 bound", f"{bnd:.10f}")
show("Ex1.7 ratio rem/bound", f"{rem / bnd:.6f}")
show("Ex1.7 bound/rem - 1", f"{bnd / rem - 1:.6f}")
show("(1.01)^10 10dp", f"{1.01 ** 10:.10f}")
show("(1.05)^10 10dp", f"{1.05 ** 10:.10f}")
rem20 = 1.05 ** 10 - 1 - 0.5
show("x=1/20 rem", f"{rem20:.10f}")
show("x=1/20 rem/exact", f"{rem20 / 1.05 ** 10:.6f} ")
bnd20 = 45 * (1.05 ** 8) * 0.0025
show("x=1/20 bound", f"{bnd20:.10f}")
show("ln(4) 6dp", f"{math.log(4):.6f}")
show("ln 16 4dp", f"{math.log(16):.4f}")
show("sqrt(2808000000) 4dp", f"{math.sqrt(2808000000):.4f}")

print("== L01 E3, R1, R3 numbers")
show("ln16.5 4dp", f"{math.log(16.5):.4f}")
show("ln19.5-ln16.5 6dp", f"{math.log(19.5) - math.log(16.5):.6f}")
show("half total", f"{base / 2:.4f}")
show("R3 ln(2.5/1.01)", f"{math.log(2.5 / 1.01):.6f}")
show("R3 ln(3/2)", f"{math.log(1.5):.6f}")
show("R3 ln2.5", f"{math.log(2.5):.6f}")
show("R3 ln3", f"{math.log(3):.6f}")
show("M2 ln16", f"{math.log(16):.4f}")
show("M1 ln4.2", f"{math.log(4.2):.6f}")

print("== L01 M1-M3 exact")
show("M3 remainder", F(1331, 1000) - 1 - F(3, 10))
show("M3 bound", F(3 * 2, 2) * F(11, 10) * F(1, 100))

print("== L02 Monty Hall, urn, coins by brute enumeration (independent of lab)")
doors = (0, 1, 2)
def monty(rule):
    stay = switch = total = F(0)
    for car, pick in product(doors, doors):
        others = [d for d in doors if d != pick]
        for opened in others:
            if rule == "A":
                goats = [d for d in others if d != car]
                if opened not in goats:
                    continue
                p = F(1, len(goats))
            else:
                if opened == car:
                    continue
                p = F(1, 2)
            w = F(1, 9) * p
            total += w
            sw = [d for d in others if d != opened][0]
            stay += w * (pick == car)
            switch += w * (sw == car)
    return stay / total, switch / total
show("Monty A (stay, switch)", monty("A"))
show("Monty B (stay, switch)", monty("B"))
balls = ["r", "r", "r", "b", "b"]
pairs = [(i, j) for i in range(5) for j in range(5) if i != j]
show("urn 20 pairs", len(pairs))
show("urn second red", F(sum(balls[j] == "r" for i, j in pairs), 20))
show("urn first red", F(sum(balls[i] == "r" for i, j in pairs), 20))
show("urn both red", F(sum(balls[i] == "r" and balls[j] == "r" for i, j in pairs), 20))
blue_first = [(i, j) for i, j in pairs if balls[i] == "b"]
show("urn second red | first blue", F(sum(balls[j] == "r" for i, j in blue_first), len(blue_first)))
show("bag posterior", F(1, 2) * F(3, 4) / F(1, 2))
show("P(red) bag", F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4))
show("E2 twoflips P(both|>=1)", F(1, 4) / F(3, 4))
show("E2 two flips P(both|first H)", F(1, 4) / F(1, 2))
show("M2 L02 P(A|B)", (F(1, 2) * F(3, 10)) / (F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10)))
show("M1 L02 sum=7 | first 3", F(1, 36) / F(6, 36))
show("E1 L02 1-1/64-6/64", 1 - F(1, 64) - F(6, 64))
show("R3 L02 blue-first red prob", F(3, 3))

print("== L03 values")
show("E[face]", F(21, 6))
show("E[100 face]", 100 * F(21, 6))
show("continuation", 100 * F(21, 6) - 100)
vals = [max(100 * f, F(250)) for f in range(1, 7)]
show("backward value", sum(vals) / 6)
show("value 1150/3 float 2dp", f"{float(sum(vals) / 6):.2f}")
show("choice gain", sum(vals) / 6 - 350)
show("choice gain float 2dp", f"{float(sum(vals) / 6 - 350):.2f}")
show("R2 gain fee=1", sum(max(100 * f, F(349)) for f in range(1, 7)) / 6 - 350)
show("R2 gain fee=100", sum(max(100 * f, F(250)) for f in range(1, 7)) / 6 - 350)

def stop_value(outcomes, rule, horizon=6):
    def value(hist):
        if len(hist) == horizon or rule(hist):
            return F(sum(hist))
        return sum((p * value(hist + (x,)) for x, p in outcomes), F(0))
    return value(())

rules = {
    "play all": lambda h: False,
    "first win": lambda h: bool(h) and h[-1] > 0,
    "first loss": lambda h: bool(h) and h[-1] < 0,
    "total 100": lambda h: sum(h) >= 100,
    "total 200 abs": lambda h: sum(h) >= 200 or sum(h) <= -200,
}
fair = ((100, F(1, 2)), (-100, F(1, 2)))
biased = ((150, F(1, 2)), (-100, F(1, 2)))
for name, rule in rules.items():
    print(f"fair {name}: {stop_value(fair, rule)}   biased {name}: {stop_value(biased, rule)}")
show("R1 two-turn look-ahead mean", F(200 + 100 + 0 - 100, 4))
show("E2 L03 625/8-150", F(625, 8) - 150)
show("E2 L03 float", float(F(625, 8) - 150))
show("E3 L03 1150/3-350", F(1150, 3) - 350)
show("M2 L03 p", F(1, 3))
show("M3 L03 expected", F(1, 2) * 100 + F(1, 2) * (-50 + 100 * F(7, 2)))
show("M1 L03 net", 100 * F(7, 2) - 50)
