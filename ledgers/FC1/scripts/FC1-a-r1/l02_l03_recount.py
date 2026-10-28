# Independent recount of the L02 typed-in register (from the REGISTER literal in tests/labs/FC1/lab-FC1-L02-1.py)
# and of the L03 Example 2.5 / Misconception 1 arithmetic. Run: python -I this.py
from collections import Counter
REG = [
 ("share listed on an exchange", "equities","cash","exchange"),
 ("share sold in a private negotiated trade","equities","cash","otc"),
 ("futures contract on an equity index","equities","derivative","exchange"),
 ("bond with a fixed coupon","rates","cash","otc"),
 ("futures contract on a government bond","rates","derivative","exchange"),
 ("interest rate swap","rates","derivative","otc"),
 ("corporate bond","credit","cash","otc"),
 ("credit default swap","credit","derivative","otc"),
 ("spot purchase of a currency","fx","cash","otc"),
 ("forward contract on a currency","fx","derivative","otc"),
 ("futures contract on crude oil","commodities","derivative","exchange"),
 ("physical quantity of a metal","commodities","cash","otc"),
]
deriv = [r for r in REG if r[2] == "derivative"]
print("derivative entries:", len(deriv), "exposure counts among derivatives:", dict(Counter(r[1] for r in deriv)))
print("exchange entries by form:", dict(Counter(r[2] for r in REG if r[3]=="exchange")))
h=2; m1=10000; mn=9990
C = -9998*100 + 9992*100; V=200; I = -(-100+100)
mid_move = (-1)*100*(m1-mn) + (+1)*100*(mn-mn)
print("Ex2.5 C", C, "hV", h*V, "mid-move", mid_move, "P", C + I*mn, "check", h*V+mid_move)
print("mid change", mn-m1, "cents; mid-move term", mid_move)
