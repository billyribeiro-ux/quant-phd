import math
# Example 3.3 product of rounded FY2023 factors
print("ex3.3 product", round(0.1179*0.8701*1.6936, 6))
# log decomposition 2023->2024 from printed ROEs (2023 0.1738, 2024 0.1237) and printed factors
roe_a, roe_b = 0.1738, 0.1237
lt = math.log(roe_b/roe_a); print("log total", round(lt, 4))
f = {"nm": (0.0874/0.1179), "at": (0.8511/0.8701), "lev": (1.6628/1.6936)}
for k, v in f.items(): print(k, round(math.log(v), 5), round(math.log(v)/lt*100, 2))
print("sum shares", round(sum(math.log(v)/lt*100 for v in f.values()), 2))
# Remark 2.1 factor at g=0.2
print("remark 2.1", round(2*1.2/2.2, 4))
print("ROE gap %", round((0.1925/0.1820-1)*100, 2))
# Example 4.2 DSO and margins
print("dso restated", round(43.8*1131.9/1145.5, 2), "margin filed", round(139.034/1131.891, 4), "restated", round(139.034/1145.5, 4))
print("lev/ROE mismatch shown", 0.1214 and "n/a")
