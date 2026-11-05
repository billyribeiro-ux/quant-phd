# Re-derives every fact quoted in Exemplar B and Exemplar A from the Lab 3 answers printed on the page.
import sys, re, html
from fractions import Fraction
page = open(sys.argv[1], encoding="utf-8").read()
block = re.search(r'Rung 3 reference case.*?ANSWERS: list\[Answer\] = \[(.*?)\n\]', page, re.S).group(1)
answers = eval("[" + html.unescape(block) + "]", {"Fraction": Fraction})
prizes_all = []
ok_sum = True
counts = []
for pid, ch, pa, qa, pb, qb in answers:
    for prizes, probs in ((pa, qa), (pb, qb)):
        fr = [Fraction(p) for p in probs]
        ok_sum &= (sum(fr) == 1) and all(f >= 0 for f in fr)
        counts.append(len(prizes))
        prizes_all += prizes
print("pairs:", len(answers), "| min prize:", min(prizes_all), "| max prize:", max(prizes_all))
print("lotteries with prize counts:", sorted(set(counts)), "| all probability vectors sum to exactly 1:", ok_sum)
print("exemplar B pair 0 A:", answers[0][2], answers[0][3], "B:", answers[0][4], answers[0][5])
print("exemplar B pair 3 A:", answers[3][2], answers[3][3], "B:", answers[3][4], answers[3][5])
print("pair 3 choice:", answers[3][1], "| pair 0 choice:", answers[0][1])
print("prize values as printed in B (whole cents):", all(isinstance(x, int) for a in answers for x in a[2] + a[4]))
