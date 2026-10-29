import sys
src = open(sys.argv[1], encoding="utf-8").read().replace("\nmain()", "\n")
ns = {"__name__": "x"}
exec(compile(src, sys.argv[1], "exec"), ns)
for b in (0.5, 0.9, 0.95):
    vals, pol, count = ns["solve"](ns["GRID"], b)
    print("beta", b, "iterations", count)
