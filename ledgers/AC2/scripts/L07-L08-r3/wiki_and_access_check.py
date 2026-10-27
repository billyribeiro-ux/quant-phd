"""Round-3 source checks: Wikipedia constants and reference attribution (read from a plain-curl copy),
and the plain-curl access statuses for the Beneish sources. Usage: python3 -I wiki_and_access_check.py <src_dir>
where <src_dir> holds wiki.html (curl -L https://en.wikipedia.org/wiki/Beneish_M-score) and wiki.txt."""
import html, re, sys
src = sys.argv[1]
s = open(f"{src}/wiki.html", encoding="utf-8", errors="replace").read()
t = open(f"{src}/wiki.txt", encoding="utf-8").read()
for name, v in [("intercept", "-4.84"), ("DSRI", "0.92"), ("GMI", "0.528"), ("AQI", "0.404"), ("SGI", "0.892"),
                ("DEPI", "0.115"), ("SGAI", "-0.172"), ("TATA", "4.679"), ("threshold", "-1.78")]:
    print(name, v, "present:", v in t or v.replace("-", "−") in t)
for absent in ["4.697", "-2.22", "−2.22"]:
    print("absent", absent, absent not in t)
# which reference numbers the coefficient formula cites
i = t.find("The formula to calculate the M-score is")
print("formula text:", t[i:i + 60].replace("\n", " ") if i >= 0 else "formula not found")
refs = [html.unescape(re.sub(r"<[^>]+>", " ", r)).strip() for r in re.findall(r'mw-reference-text[^>]*>(.*?)</span>', s, flags=re.S)]
refs = [r for r in refs if len(r) > 10 and not r.startswith(".mw-parser")]
for n, r in enumerate(refs[:2], 1):
    print(f"ref [{n}]:", " ".join(r.split())[:160])
i2 = t.find("threshold value is -1.78")
print("threshold sentence:", t[i2:i2 + 200].replace("\n", " "))
