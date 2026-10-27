"""Round-5: recompute L02 prose numbers from the printed/unrounded values (no twin import)."""
import math
print("0.1179*0.8701*1.6936 =", round(0.1179 * 0.8701 * 1.6936, 5), "(prose: 0.1737 in last digit; lab identity holds unrounded)")
print("gap 0.1925/0.1820-1 =", round((0.1925 / 0.1820 - 1) * 100, 2), "% (prose 5.8%)")
print("mismatch 0.1108?  leverage*ta? ; year-end turnover product check: 0.9133 (avg) vs stated mismatch 0.1838")
print("ln(0.0874/0.1179) =", round(math.log(0.0874 / 0.1179), 4), "(prose -0.2993)")
print("ln(0.1237/0.1738) =", round(math.log(0.1237 / 0.1738), 4), "(prose -0.3400)")
print("ln(0.8511/0.8701) =", round(math.log(0.8511 / 0.8701), 4), "(prose -0.0221)")
print("ln(1.6628/1.6936) =", round(math.log(1.6628 / 1.6936), 4), "(prose -0.0184)")
print("unrounded shares from printed logs: net margin -0.2997/-0.3401 =", round(-0.2997 / -0.3401 * 100, 1), "%; ",
      "asset turnover", round(-0.0221 / -0.3401 * 100, 1), "%; leverage", round(-0.0184 / -0.3401 * 100, 1), "%")
print("E3 0.12*365 =", 0.12 * 365, "; 120/900*365 =", round(120 / 900 * 365, 2), "; 120/900*360 =", round(120 / 900 * 360, 2))
print("DSO 2022 restated: 135826937/1145473837*365 =", round(135826937 / 1145473837 * 365, 2))
print("DSO 2022 with filed 1131.9: 135826937/1131.9e6*365 =", round(135826937 / 1131.9e6 * 365, 2))
print("filed revenue implied by recv/0.12 =", round(135826937 / 0.12 / 1e6, 3), "M")
print("restated/filed - 1 =", round(1145473837 / (135826937 / 0.12) - 1, 5), "(generator factor 1.012)")
print("net margin as filed 0.1228 -> NI implied", round(0.1228 * 1131.9, 2), "; restated", round(0.1214 * 1145.47, 2))
