import re, sys
path = sys.argv[1]
L = open(path, encoding="utf-8").read().split("\n")
out, skip = [], False
for line in L[616:692]:
    if 'class="annotation"' in line:
        skip = True
    if skip:
        if "</aside>" in line:
            skip = False
        continue
    if "exemplar-verdict" in line:
        continue
    out.append(re.sub(r' data-(scores|level)="[^"]*"', "", line))
print("\n".join(out))
