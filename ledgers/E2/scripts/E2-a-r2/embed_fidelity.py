"""E2 slice a round 2: each lab twin source and its printed output appear verbatim in the lesson's <pre> blocks."""
import html, re, subprocess, sys
root = sys.argv[1]
for L, tw in [("L01", "lab-E2-L01-1"), ("L02", "lab-E2-L02-1"), ("L03", "lab-E2-L03-1")]:
    s = open(f"{root}/course/modules/E/E2/{L}.html", encoding="utf-8").read()
    src = open(f"{root}/tests/labs/E2/{tw}.py", encoding="utf-8").read()
    pres = [html.unescape(re.sub(r"<[^>]+>", "", p)) for p in re.findall(r"<pre[^>]*>(.*?)</pre>", s, re.S)]
    out = subprocess.run([sys.executable, "-I", "-W", "error", f"{root}/tests/labs/E2/{tw}.py"],
                         capture_output=True, text=True, check=True).stdout
    print(L, "source in pre:", any(src.strip() in p for p in pres), "output in pre:", any(out.strip() in p for p in pres))
