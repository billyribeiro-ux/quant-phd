import math
d = math.sqrt(3) / 2
for n in (151, 152):
    print("R2 bound n", n, 0.9**n * d / 0.1)
print("naive printed ratio", 0.0000085808 / 0.0000009534, "unrounded", 0.9 / 0.1)
for b in (0.5, 0.9, 0.95):
    tau = 1e-12
    n = math.ceil(math.log(d / (tau * (1 - b))) / math.log(1 / b))
    while b**n * d / (1 - b) > tau:
        n += 1
    while b ** (n - 1) * d / (1 - b) <= tau:
        n -= 1
    print("E1 a priori least n at beta", b, n)
print("1/ln2, 1/ln(1/0.9), 1/ln(1/0.95)", 1 / math.log(2), 1 / math.log(1 / 0.9), 1 / math.log(1 / 0.95))
print("sup|V1-V0| over grid", max(math.sqrt(k**0.5 - kp) for k in (0.25, 0.5, 0.75, 1.0) for kp in (0.25, 0.5, 0.75, 1.0) if kp <= k**0.5 + 1e-15))
