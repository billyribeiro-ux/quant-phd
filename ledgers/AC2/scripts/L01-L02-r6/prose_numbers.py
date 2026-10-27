import math
# printed values from the lab output (L02 expected block), 4 dp
nm23, at23, lev23, roe23 = 0.1179, 0.8701, 1.6936, 0.1738
nm24, at24, lev24, roe24 = 0.0874, 0.8511, 1.6628, 0.1237
print("product 2023 rounded factors:", round(nm23*at23*lev23, 5))
print("ln(roe24/roe23) printed:", round(math.log(roe24/roe23), 4), " ln nm:", round(math.log(nm24/nm23), 4), " ln at:", round(math.log(at24/at23), 4), " ln lev:", round(math.log(lev24/lev23), 4))
print("ln(0.0874/0.1179)=", round(math.log(0.0874/0.1179), 4), " ln(0.1237/0.1738)=", round(math.log(0.1237/0.1738), 4))
print("E2 unrounded shares printed: -0.2997/-0.3401 =", round(100*(-0.2997)/(-0.3401),1), " -0.0221/-0.3401=", round(100*(-0.0221)/(-0.3401),1), " -0.0184/-0.3401=", round(100*(-0.0184)/(-0.3401),1))
print("sum of printed shares:", round(88.1+6.5+5.4,1))
print("ROE 2022 avg/ye gap:", round(100*(0.1925/0.1820-1),2), "%")
print("mismatch 2022:", round(0.1214*0*1 + 0,4))
print("ROE 2021->22 %:", round(100*(0.1925/0.2100-1),2), " 22->23 %:", round(100*(0.1738/0.1925-1),2), " 23->24 %:", round(100*(0.1237/0.1738-1),2))
print("M1 check:", round(50/280,4), round(750/280,4), round(0.1*(500/750)*(750/280),4), round(50/750,4))
print("M2:", round(120/900*365,2), round(120/900*360,2), round(365/360,4), round(100*(365/360-1),2))
print("M3:", 400/250, 360/1000)
print("R3 factor:", round(1/((1+1/1.2)/2),4), round(2*1.2/2.2,4), round(100*(2*1.2/2.2-1),2), round((1+1/1.2)/2,4))
print("E3 DSO 2022:", round(43.80*1131.9/1145.5,3), " restated/orig:", round(1145.5/1131.9,5), " 1131.9*1.012=", round(1131.9*1.012,2), " 0.12*365=", 0.12*365)
print("Example 4.2: DSO at 1145.5 w/ 0.12*1131.9 recv:", round(0.12*1131.9/1145.5*365,3))
print("Remark 2.1 at g=0.2 quotient:", round(2*1.2/2.2,4))
print("E3: 43.80 ok; 365 DSO 2022 recv=0.12*1131.9:", round(0.12*1131.9,3))
