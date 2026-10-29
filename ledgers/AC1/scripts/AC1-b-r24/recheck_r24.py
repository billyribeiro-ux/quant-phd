# Independent recomputation of the numbers in the round-24 delta (L04 line 78/473, L05 lines 87/96, L06 lines 73/120/439/499, cards c088/c141).
import math

# L06 Lab 1 printed values (from the twin stdout), year by year.
interest = [4535544, 4000124, 3430973, 2825965, 2182842, 1499202, 772492]
payment = [13034272] * 6 + [13034273]
opening = [71992763, 63494035, 54459887, 44856588, 34648281, 23796851, 12261781]
amort = [10284680] * 6 + [10284683]
exp_f = [i + a for i, a in zip(interest, amort)]
exp_s_total = sum(payment)
n = 7
s_base = exp_s_total // n
exp_s = [s_base] * (n - 1) + [exp_s_total - s_base * (n - 1)]

print("sum payments", exp_s_total, "floor(sum/n)", s_base, "S shares", exp_s)
print("c141 S equals payment every year:", exp_s == payment)
print("opening falls each year:", all(opening[t] > opening[t + 1] for t in range(6)))
print("payment exceeds interest each year:", all(payment[t] > interest[t] for t in range(7)))
falls = [interest[t] - interest[t + 1] for t in range(6)]
print("interest falls:", falls, "min", min(falls))
print("amort year7 rise", amort[6] - amort[5], "< min interest fall:", amort[6] - amort[5] < min(falls))
print("F falls each year:", all(exp_f[t] > exp_f[t + 1] for t in range(6)), exp_f)
diff = [f - s for f, s in zip(exp_f, exp_s)]
print("F-S diffs", diff, "sum", sum(diff))
print("year1 diff", diff[0])
# L04 numbers: Prop 2.2 identity recomputed from the printed lines is in the lab; here check E1 counts.
ni_a = [3287820, -52491, 6513383, 4217443, 2059332, 7617569, 5979583, -1183435]
ni_b = [3287820, 3612039, 5291873, 6171018, 4523679, 4977802, 3339814, 2209445]
print("rule A lower in", [q for q in range(8) if ni_a[q] < ni_b[q]], "higher in", [q for q in range(8) if ni_a[q] > ni_b[q]], "equal", [q for q in range(8) if ni_a[q] == ni_b[q]])
print("cum diff", sum(ni_a) - sum(ni_b), "prepaid end 4974286")
# L06 rate-0 check of the c088 claim (no year-level equality needed for the Lab 1 answer)
