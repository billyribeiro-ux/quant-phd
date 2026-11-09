"""Delta from the round-2 pin and why-it-matters word counts for the slice (run from the checkout root)."""
import html
import re
import subprocess

R2 = "9294b914a51647c66d2dee62c4a112c76ba04900"
HEAD = "8196077d5f56c3919d33e69888176d197d378ad4"
paths = [f"course/modules/M/M2/L{n}.html" for n in ("07", "08", "09", "10", "11", "12")] + [
    "course/modules/M/M2/cards.json", "tests/labs/M2/lab-M2-L07-1.py", "tests/labs/M2/lab-M2-L08-1.py",
    "tests/labs/M2/lab-M2-L09-1.py", "tests/labs/M2/lab-M2-L10-1.py", "tests/labs/M2/lab-M2-L11-1.py",
    "tests/labs/M2/lab-M2-L12-1.py", "notation/notation.json", "tools/check_pages.py"]
out = subprocess.run(["git", "diff", "--stat", R2, HEAD, "--", *paths], capture_output=True, text=True).stdout
print("delta stat (slice paths) round2->round3 pin:\n" + out)
for n in ("07", "08", "09", "10", "11", "12"):
    src = open(f"course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    m = re.search(r'class="why-it-matters"[^>]*>(.*?)</p>', src, re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
    print(f"L{n} why-it-matters words: {len(txt.split())}")
