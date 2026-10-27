import sys
path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")
for spec in sys.argv[2:]:
    a, b = (int(x) for x in spec.split("-"))
    print(f"=== {path.split('/')[-1]} {a}-{b}")
    for i in range(a, b + 1):
        print(f"{i}: {lines[i-1][:2000]}")
