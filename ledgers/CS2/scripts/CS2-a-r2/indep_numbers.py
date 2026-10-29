"""Independent recomputation of slice-a prose numbers (CS2 L01-L04)."""
import math
from fractions import Fraction as F

# L01
print("L01 1023/511 =", float(F(1023, 511)), "-> 4dp", f"{1023/511:.4f}", "exact 2+1/511 =", 2 + F(1, 511) == F(1023, 511))
print("L01 1/511 =", f"{1/511:.7f}", "1024^2 =", 1024**2, "1024^2 == 2^20:", 1024**2 == 2**20)
print("L01 E3/Prop1.3 floor(1000)+1 =", math.floor(1000) + 1)
# L02 exact successful totals and averages
for n, tot in [(16, 16), (32, 37), (64, 97), (128, 257), (256, 772)]:
    print("L02 n", n, "avg exact", F(tot, n), f"{tot/n:.4f}", "model 1+(n-1)/128 =", F(128 + n - 1, 128), float(F(128 + n - 1, 128)))
print("L02 257/128 =", float(F(257, 128)), "193/64 =", float(F(193, 64)), "193/64-257/128 =", float(F(193, 64) - F(257, 128)))
print("L02 unsucc: 134/500", 134/500, "270/500", 270/500, "548/500", 548/500, "1016/500", 1016/500, "2014/500", 2014/500)
print("L02 gap(n=16)", float(F(16, 16) - (1 + F(15, 128))), "gap n=32", float(F(37, 32) - (1 + F(31, 128))))
print("L02 R3 difference check (n-2m+1)/(2m) at n=2m-1 zero; m=64 n=127:", F(127 - 128 + 1, 128))
print("L02 E2 1275/50 =", 1275 / 50, " 50*51/2 =", 50 * 51 // 2)
print("L02 M2 73/64 =", float(F(73, 64)))
print("L02 misc3 n/(2m) at n=128, m=64:", F(128, 128), " (n-1)/(2m)=", F(127, 128))
# L03
print("L03 6*4096*12 =", 6 * 4096 * 12, " margin =", 6 * 4096 * 12 - 166912)
print("L03 2*4096*4097 =", 2 * 4096 * 4097, " ratio 4378444/that =", 4378444 / (2 * 4096 * 4097))
print("L03 sums: 107+98 =", 107 + 98, " 241+361 =", 241 + 361, " 1617+4514 =", 1617 + 4514, " 3802+4933 =", 3802 + 4933,
      " 3742+17663 =", 3742 + 17663, " 8517+10623 =", 8517 + 10623)
print("L03 92609/8192 =", 92609 / 8192, " 2N ops at 4096 =", 2 * 4096)
print("L03 heap move ratio list:", [round(b / a, 4) for a, b in [(1, 1)]])
print("L03 bit_length check floor(log2 N): ", [(N, N.bit_length() - 1) for N in (16, 4096)])
# L04
lg = math.lgamma(1025) / math.log(2)
print("L04 log2(1024!) =", f"{lg:.6f}", " ceil =", math.ceil(lg), " (1024!-1).bit_length() =", (math.factorial(1024) - 1).bit_length())
print("L04 log2(1000!) =", f"{math.lgamma(1001)/math.log(2):.4f}", " 500*log2(500) =", f"{500*math.log2(500):.4f}")
print("L04 5120/8770 =", f"{5120/8770:.6f}", " 262431/8886 =", f"{262431/8886:.6f}")
print("L04 7! ceil log2 =", math.ceil(math.log2(math.factorial(7))), " (7!-1).bit_length() =", (math.factorial(7) - 1).bit_length())
print("L04 log2 6 =", f"{math.log2(6):.4f}", " 2^9*10 =", 10 * 2**9, " 1024*10 =", 1024 * 10)
print("L04 gaps sum (n+1) for n=1..1000 =", sum(n + 1 for n in range(1, 1001)))
print("L04 Cor2.2 n=1000 holds:", math.log2(math.factorial(1000)) >= 500 * math.log2(500))
