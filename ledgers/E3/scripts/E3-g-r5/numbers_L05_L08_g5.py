from fractions import Fraction as F
import math, json, collections
# L05
print("L05 CE1 at gamma=2, tree 1/2 on 1, 1/2 on 4:", 1/((F(1,2)*F(1)**-1)+(F(1,2)*F(4)**-1)))
print("L05 CE1 at 1/4 on 1, 3/4 on 3:", 1/(F(1,4)+F(3,4)/3))
print("L05 remark1.5 CE for {2,3}:", 1/((F(1,2)*F(1,2)**-1)+(F(1,2)*F(1,3)**-1)) if False else 1/(F(1,2)*(F(1,2))+F(1,2)*F(1,3)))
b=F(9,10); c0=F(2)
V0inv = (1-b)/c0 + b*F(5,8)
print("V0 =", 1/V0inv, " U =", -(F(1,2)*0 + (1-b)/c0 + b*F(5,8)), "(-(1-b)/c0 part) check U=", -(F(1,20)+F(9,16)))
print("L05 M2 V0 (beta=1/2,c0=1,c1=3,psi=1/2):", 1/(F(1,2)*1 + F(1,2)*F(1,3)))
print("L05 E2 V0 changed tree:", 1/(F(1,20)+F(9,10)*F(7,16)))
# L06
print("L06 lam*=5/3:", F(1,2)*1000/(F(1,2)*600))
print("L06 W(2)=", F(1,2)*1000 - F(1,2)*2*600)
print("L06 sqrt(5/3)=", math.sqrt(5/3), " alpha=delta=.5 W(2)=", 0.5*math.sqrt(1000)-0.5*2*math.sqrt(600))
print("L06 lambda_R p=1/3 g=1000 l=300:", (1/3*math.sqrt(1000-400/3))/((2/3)*math.sqrt(300+400/3)), math.sqrt(2)/2)
print("L06 remark 2.5 combined 700-300*2=", F(1,4)*2000+F(1,2)*400-F(1,4)*2*1200, " separate 2*(500-600)=", 2*(F(1,2)*1000-F(1,2)*2*600))
# L08
W1, WL, W0 = 110000, 95000, 100000
print("L08 EU CE=", F(1,1)/(F(1,2)/W1+F(1,2)/WL), float(F(1,1)/(F(1,2)/W1+F(1,2)/WL)), "4180000/41=", float(F(4180000,41)))
print("L08 maxmin p=1/3 CE=", float(1/(F(1,3)/W1+F(2,3)/WL)))
print("L08 CE p=1/4 =", float(1/(F(1,4)/W1+F(3,4)/WL)), " p=3/4 =", float(1/(F(3,4)/W1+F(1,4)/WL)))
print("L08 known urn red (1/3) CE =", float(1/(F(1,3)/110000+F(2,3)/100000)), " black (2/3) CE=", float(1/(F(2,3)/110000+F(1,3)/100000)))
print("L08 premium 102500-EU CE =", float(102500-F(4180000,41)), " CU:", float((102500-F(4180000,41))/100))
print("L08 Model2 V=5-sqrt50=", 5-math.sqrt(50), " CE change CU=", -(-(5-math.sqrt(50))/2)**2, " cents=", -(-(5-math.sqrt(50))/2)**2*100, " wealth=", 100000-(-(-(5-math.sqrt(50))/2)**2*100))
print("L08 maxmin minus wealth=", float(F(1,1)/(F(1,3)/W1+F(2,3)/WL))-100000)
print("L08 EU CE at P(red)=1/2 with W0 changes: 1/2*v(100)+1/2*v(-50) CU:", 0.5*10+0.5*(-2*math.sqrt(50)))
# dedicated counts
cards = json.load(open('course/modules/E/E3/cards.json'))
cnt = collections.Counter(); per = collections.Counter()
for c in cards:
    if c.get('lesson') in ('L05','L06','L07','L08'):
        cnt[c.get('grade')] += 1; per[c['lesson']] += 1
print("slice counts by grade", dict(cnt), "by lesson", dict(per), "total", sum(cnt.values()))
