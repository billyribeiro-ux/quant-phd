import random
from fractions import Fraction
random.seed(7)
four_bad = six_bad = 0
N = 3000
for _ in range(N):
    n = random.randint(1, 4)
    bu = [random.randint(1, 500) for _ in range(n)]; au = [random.randint(0, 600) for _ in range(n)]
    bp = [random.randint(100, 5000) for _ in range(n)]; ap = [random.randint(100, 5000) for _ in range(n)]
    q1 = [random.randint(0, 4) for _ in range(n)]; q2 = [random.randint(0, 4) for _ in range(n)]
    s1, s2, a1, a2 = (random.randint(1, 900) for _ in range(4))
    AQ1, AQ2 = random.randint(0, 3000), random.randint(0, 3000)
    F, FA = random.randint(0, 10**6), random.randint(0, 10**6)
    BU, AT = sum(bu), sum(au)
    def run(s1, s2, a1, a2, FA):
        bud = sum(bu[i]*(bp[i]-q1[i]*s1-q2[i]*s2) for i in range(n)) - F
        act = sum(au[i]*ap[i] for i in range(n)) - a1*AQ1 - a2*AQ2 - FA
        flex = Fraction(AT, BU)*sum(bu[i]*(bp[i]-q1[i]*s1-q2[i]*s2) for i in range(n)) + 0 - F  # flexed revenue less variable less F
        flex = Fraction(AT,BU)*sum(bu[i]*bp[i] for i in range(n)) - Fraction(AT,BU)*sum(bu[i]*(q1[i]*s1+q2[i]*s2) for i in range(n)) - F
        price = sum((ap[i]-bp[i])*au[i] for i in range(n))
        volume = flex - bud
        mix = sum(au[i]*(bp[i]-q1[i]*s1-q2[i]*s2) for i in range(n)) - F - flex
        e1 = s1*(sum(q1[i]*au[i] for i in range(n)) - AQ1)
        e2 = s2*(sum(q2[i]*au[i] for i in range(n)) - AQ2)
        ipv = (s1-a1)*AQ1 + (s2-a2)*AQ2
        fov = F - FA
        total = act - bud
        return price + volume + mix + e1 + e2, price + volume + mix + e1 + e2 + ipv + fov, total
    f, _, t = run(s1, s2, s1, s2, F)            # inputs at standard price, fixed at budget
    if f != t: four_bad += 1
    _, six, t2 = run(s1, s2, a1, a2, FA)
    if six != t2: six_bad += 1
print("four figures, inputs at standard price, fixed at budget: mismatches", four_bad, "of", N)
print("six figures (with ipv and fixed overhead variance), general: mismatches", six_bad, "of", N)
