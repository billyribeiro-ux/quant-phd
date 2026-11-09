from fractions import Fraction
# chain strikes [1,2,7], calls [7,7,4], puts [8,9,11], spot 0, df 1, fee 0, spread 0; strike index 1 (K=2)
low, mid, high = 1, 2, 7
c_low, c_mid, c_high = 7, 7, 4
# r17_d style: float weights (high-mid)/(high-low) and (mid-low)/(high-low)
wl = (high - mid) / (high - low)
wh = (mid - low) / (high - low)
chord_f = wl * c_low + wh * c_high
print("float weights", repr(wl), repr(wh), "float chord", repr(chord_f), "less call", repr(chord_f - c_mid))
print("float gross via int((-sd+0.5)//1)", int((-(chord_f - c_mid) + 0.5)//1))
# exact
e = Fraction(high - mid, high - low) * c_low + Fraction(mid - low, high - low) * c_high
print("exact chord", e, "exact sd", e - c_mid)
# r16_c style: float weights converted to Fraction
fl = Fraction(wl) * c_low + Fraction(wh) * c_high
print("Fraction(float weights) chord", fl, "equals 13/2:", fl == Fraction(13, 2))
# 2.5 chain from comment at test_project 884-888: chain [1,2,7] calls [2,3,5] puts [3,5,12]
cl = wl * 2 + wh * 5
print("chain [1,2,7] calls [2,3,5] float chord (via calls at low,high = 2,5):", repr(wl*2 + wh*5), repr(wl*2+wh*5 - 3))
print("Fraction of float weights for 2,5 chord:", Fraction(wl)*2 + Fraction(wh)*5, Fraction(wl)*2 + Fraction(wh)*5 == Fraction(5,2))
print("5/6 exact in binary?", Fraction(5,6) == Fraction(wl*0+ (high-mid)/(high-low)))
print("1/6 float is", repr(1/6), Fraction(1/6) == Fraction(1,6), "5/6 float is", repr(5/6), Fraction(5/6)==Fraction(5,6))
