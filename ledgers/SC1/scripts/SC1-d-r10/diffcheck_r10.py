import html, re, sys, difflib
from pathlib import Path
root=Path(sys.argv[1])
page=(root/"course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
for lab_id in ["lab-SC1-project-1","lab-SC1-project-3"]:
    m=re.search(r'id="%s".*?<pre><code class="language-python" data-run>(.*?)</code></pre>'%lab_id,page,re.S)
    code=html.unescape(m.group(1))
    twin=(root/"tests/labs/SC1"/f"{lab_id}.py").read_text(encoding="utf-8")
    print(lab_id, "raw equal-after-strip:", code.rstrip("\n")==twin.rstrip("\n"))
    for i,(a,b) in enumerate(zip(twin.splitlines(),code.splitlines())):
        if a!=b: print(i+1, repr(a)); print(i+1, repr(b))
