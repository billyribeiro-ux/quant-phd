import re, sys
root = sys.argv[1]
L04 = open(root + "/course/modules/M/M5/L04.html", encoding="utf-8").read()
L01 = open(root + "/course/modules/M/M5/L01.html", encoding="utf-8").read()
q5 = re.search(r'Which pair of points shows[^<]*', L04).group(0)
print("L04 q5 prompt:", q5)
print("L04 q5 correct option is a triple:", "x=0</span>" in L04 or "\\(x=0\\)" in L04)
print("L04 Example 3.6 limit-order step present:", "so \\(\\lvert x\\rvert\\le 0\\)" in L04)
print("L04 Proof 3 squeeze step present:", "so the left side does too" in L04)
print("L04 pseudometric defined at first use:", L04.find("<em>pseudometric</em>") < L04.find("pseudometric, not a metric"))
print("L01 why-it-matters claims '(§5 proves this)':", "(§5 proves this)" in L01)
s5 = L01[L01.find('id="misconceptions"'):L01.find('id="problems"')]
print("L01 §5 proves irrationality of the supremum (rational case):", "rational" in s5 and "not rational" in s5)
print("L01 §5 misconception 3 premise is 'equalled some endpoint':", "equalled some endpoint" in s5)
