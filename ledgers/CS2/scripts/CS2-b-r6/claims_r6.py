import math
phi = (1 + math.sqrt(5)) / 2
print("1/log2phi", round(1/math.log2(phi), 6))
print("log_phi(501)", round(math.log(501)/math.log(phi), 4), "log_phi(65)", round(math.log(65)/math.log(phi), 4))
print("ln377/lnphi", round(math.log(377)/math.log(phi), 4), "ln377", round(math.log(377), 4), "lnphi", round(math.log(phi), 4))
print("ln8/lnphi", round(math.log(8)/math.log(phi), 4), "ln3/lnphi", round(math.log(3)/math.log(phi), 4))
print("272/500", 272/500, "log2 64", math.log2(64))
N = [0, 1]
for h in range(2, 13): N.append(1 + N[h-1] + N[h-2])
print("N0..12", N)
print("phi^8,12", round(phi**8, 4), round(phi**12, 4))
print("2^40", 2**40, "2^20+1", 2**20+1, "1000 bits", (1000).bit_length(), "1024+1", 1024+1)
print("R2 proof n=7 N4 check", N[4], "nodes R2 = 1+4+2 =", 1+4+2)
print("LCS_1 greedy example: 6 coins greedy 4+1+1 ->3; ")
print("1438*27", 1438*27, "40000/1438", round(40000/1438, 4), "1238/200", 1238/200)
print("E1 L06: 772-200", 772-200)
print("L08: 102/400", 102/400)
