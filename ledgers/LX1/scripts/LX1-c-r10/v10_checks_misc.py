"""Round-10 verifier: small checks for LX1-c. (1) the citation string on project.html equals the MANIFEST citation;
(2) every href on project.html resolves (ids present, files exist); (3) the hub hours figure; (4) the page's
claim that labs 1 and 2 read no file; (5) the 'SIMULATED' count inside the Lab 3 section. Argument 1: checkout root."""
import json, os, re, sys
root = sys.argv[1]
os.chdir(root)
page_path = "course/modules/LX/LX1/project.html"
src = open(page_path, encoding="utf-8").read()
man = json.load(open("course/assets/data/market/MANIFEST.json", encoding="utf-8"))
fx = [d for d in man["datasets"] if d["id"] == "fx_monthly"][0]
cit = fx["citation"]
print("(1) MANIFEST citation in page text (:277):", src.split("\n")[276].count(cit) >= 1, "| (:285):", src.split("\n")[284].count(cit) >= 1)
print("(1b) lab 3 docstring has citation:", cit in open("tests/labs/LX1/lab-LX1-project-3.py", encoding="utf-8").read())
ids = set(re.findall(r'id="([^"]+)"', src))
bad = []
for href in re.findall(r'href="([^"]+)"', src):
    if href.startswith("http"):
        continue
    if href.startswith("#"):
        if href[1:] not in ids:
            bad.append(href)
        continue
    path, _, frag = href.partition("#")
    target = os.path.normpath(os.path.join(os.path.dirname(page_path), path))
    if not os.path.exists(target):
        bad.append(("missing", href))
    elif frag and f'id="{frag}"' not in open(target, encoding="utf-8").read():
        bad.append(("missing id", href))
print("(2) href problems:", bad)
hub = open("course/modules/LX/LX1/index.html", encoding="utf-8").read()
print("(3) hub project hours:", re.findall(r'data-hours-project="(\d+)"', hub), "| page:", re.findall(r'data-hours-project="(\d+)"', src))
lines = src.split("\n")
for lab in ("lab-LX1-project-1", "lab-LX1-project-2", "lab-LX1-project-3"):
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, src, re.S).group(0)
    print("(4)", lab, "reads a file:", bool(re.search(r"open\(|read_text|csv\.|DictReader", sec)), "| data-files:", re.findall(r'data-files="([^"]+)"', sec))
sec3 = re.search(r'<section class="lab[^"]*" id="lab-LX1-project-3".*?</section>', src, re.S).group(0)
print("(5) SIMULATED occurrences in lab 3 section:", len(re.findall("simulated", sec3, re.I)))
