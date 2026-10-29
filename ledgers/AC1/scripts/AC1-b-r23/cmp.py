import re,html,sys
for t in ["L04","L05","L06"]:
    page=open(f"/tmp/verify23-AC1-b/course/modules/AC/AC1/{t}.html",encoding="utf-8").read()
    blocks=re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>',page,re.S)
    out=open(f"/tmp/AC1-v/b23/twin_{t}.out").read()
    exp=[html.unescape(b) for b in blocks]
    print(t,"expected blocks",len(blocks),"match any:",[e.strip()==out.strip() for e in exp])
