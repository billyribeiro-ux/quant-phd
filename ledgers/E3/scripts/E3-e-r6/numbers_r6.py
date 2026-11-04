# Independent numeric checks for E3-e round 6 (own code; does not import the course grader)
import math
from fractions import Fraction as F
print("L08 EU CE", 2/(0.5/110000+0.5/95000), 4180000/41)
print("L08 maxmin", 1/((1/3)/110000+(2/3)/95000), "premium", 102500-4180000/41, 22500/41)
print("L08 premium CU", (102500-4180000/41)/100)
print("L08 maxmin shortfall", 100000-1/((1/3)/110000+(2/3)/95000))
# alpha-MEU tau=1/2 at midpoint 1/2
g = lambda p: p/110000+(1-p)/95000
print("alpha-MEU", 1/(0.5*g(1/3)+0.5*g(2/3)))
# L08 Model 4 prior set k=30..60 of 90
print("prior mean k", sum(range(30,61))/len(range(30,61))/90)
# ---- instrument facts from grader/instance.py for seed 0 and seed 49 are checked elsewhere; here the Lab 3 data
import re, pathlib
src = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD6-E3-e/tests/labs/E3/lab-E3-project-3.py").read_text()
ns = {}
pre = src.split("def main")[0]
exec(compile(pre.replace("from fractions import Fraction","from fractions import Fraction"), "lab3", "exec"), ns)
ANS = ns["ANSWERS"]
print("lab3 answers", len(ANS))
prizes=[]; counts=[]
for pid,ch,pa,qa,pb,qb in ANS:
    prizes += pa+pb; counts += [len(pa), len(pb)]
    for qs in (qa,qb):
        assert sum(F(x) for x in qs)==1, (pid,qs)
print("lab3 prize range", min(prizes), max(prizes), "prizes per lottery", sorted(set(counts)))
mixed = 0
for pid,ch,pa,qa,pb,qb in ANS:
    m=False
    for pr,qq in ((pa,qa),(pb,qb)):
        g_ = any(x>0 and F(p)>0 for x,p in zip(pr,qq)); l_ = any(x<0 and F(p)>0 for x,p in zip(pr,qq))
        m = m or (g_ and l_)
    mixed += m
print("lab3 mixed-sign answers", mixed)
print("pair 3 lotteries", ANS[3])
print("pair 0 lotteries", ANS[0])
