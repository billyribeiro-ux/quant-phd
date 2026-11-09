import re, subprocess, sys, html
root = sys.argv[1]
page = open(f"{root}/course/modules/E/E3/L02.html", encoding="utf-8").read()
twin = open(f"{root}/tests/labs/E3/lab-E3-L02-1.py", encoding="utf-8").read()
out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E3/lab-E3-L02-1.py"],
                     capture_output=True, text=True, check=True).stdout
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
exp = html.unescape(exp)
print("expected block == twin output:", exp.strip() == out.strip())
# lines whose value is not six decimals, and not a cents/scale/check token
for line in out.strip().splitlines():
    toks = line.split()
    nums = [t for t in toks if re.fullmatch(r"-?\d+(\.\d+)?", t)]
    bad = [t for t in nums if not re.fullmatch(r"-?\d+\.\d{6}", t)]
    if bad:
        print("non-six-decimal numeric tokens:", bad, "| line:", line[:70])
# the sentence
m = re.search(r"Other values are unrounded.*?False checks are printed as given\.", twin, re.S)
print("twin sentence:", " ".join(m.group(0).split()))
print("sentence in page:", " ".join(m.group(0).split()) in " ".join(page.split()))
print("dimensionless in twin relative docstring:", "dimensionless" in twin)
