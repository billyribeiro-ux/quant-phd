import json, math, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
c = [x for x in cards if x["id"] == "M6-c047"][0]
print("back:", c["back"])
f = lambda x, y: (x*x - y*y) / (x*x + y*y) ** 2
def simpson(g, a, b, n=20000):
    h = (b - a) / n
    s = g(a) + g(b) + sum((4 if i % 2 else 2) * g(a + i*h) for i in range(1, n))
    return s * h / 3
for x in (0.3, 0.5, 0.9):
    print("x", x, "int dy", round(simpson(lambda y: f(x, y), 0.0, 1.0), 9), "expect", round(1/(1+x*x), 9))
for y in (0.3, 0.7):
    print("y", y, "int dx", round(simpson(lambda x: f(x, y), 0.0, 1.0), 9), "expect", round(-1/(1+y*y), 9))
print("pi/4", math.pi/4)
