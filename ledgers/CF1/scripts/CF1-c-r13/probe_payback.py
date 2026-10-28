g = {}
src = open("tests/labs/CF1/lab-CF1-L05-1.py", encoding="utf-8").read().replace("\nmain()", "\n")
exec(compile(src, "twin", "exec"), g)
p = g["payback"]
for f in ([0, -1, 2], [-1, 0, 2], [-5, 5], [-100, 50, 60]):
    try:
        print(f, p(f))
    except Exception as e:
        print(f, type(e).__name__, e)
