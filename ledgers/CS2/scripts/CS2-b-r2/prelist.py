import sys, re, html
src=open(sys.argv[1],encoding='utf-8').read()
pres=re.findall(r'<pre[^>]*>(.*?)</pre>', src, re.S)
for i,p in enumerate(pres):
    t=html.unescape(re.sub(r'<[^>]+>','',p))
    open(f"{sys.argv[2]}_pre{i}.txt","w").write(t)
    print(i, len(t.splitlines()), repr(t.splitlines()[0][:70]) if t.strip() else '')
