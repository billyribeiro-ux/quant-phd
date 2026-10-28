import re,sys,html
root="/tmp/verify11-CF1-c"
for lab in ["L05","L06"]:
    page=open(f"{root}/course/modules/CF/CF1/{lab}.html",encoding="utf-8").read()
    twin=open(f"{root}/tests/labs/CF1/lab-CF1-{lab}-1.py",encoding="utf-8").read()
    m=re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>',page,re.S)
    code=html.unescape(m.group(1)) if m else None
    print(lab,"run block found",bool(m),"equal to twin:",code==twin if code else None, "len",len(code or ""),len(twin))
    ex=re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>',page,re.S)
    print(lab,"expected blocks",len(ex))
    for e in ex: print(repr(html.unescape(re.sub(r'<[^>]+>','',e))[:300]))
