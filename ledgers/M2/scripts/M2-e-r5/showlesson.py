import sys, re
lines = open(f"/tmp/M2-v/M2-e-r5/text/{sys.argv[1]}.txt", encoding="utf-8").read().split("\n")
out = []
skip = False
for ln in lines:
    if ln.startswith('"""M2 lab') or ln.startswith('"""M2') :
        skip = True
    if not skip:
        out.append(ln)
    if skip and re.match(r"^main\(\)\s*$", ln):
        skip = False
        out.append("[code omitted]")
    if skip and ln.strip().startswith("print") is False and False:
        pass
for ln in out:
    print(ln)
