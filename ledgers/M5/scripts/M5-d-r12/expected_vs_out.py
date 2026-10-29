import html, re, sys
page = open("course/modules/M/M5/project.html", encoding="utf-8").read()
exp = [html.unescape(e) for e in re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)]
for i in (1, 2, 3):
    out = open(f"{sys.argv[1]}/lab-M5-project-{i}.out", encoding="utf-8").read()
    print(i, "expected == output:", exp[i - 1].strip() == out.strip())
