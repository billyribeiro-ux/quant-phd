import re,sys,html
src=open(sys.argv[1],encoding='utf-8').read()
m=re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>',src,re.S)
for i,x in enumerate(m):
    open(sys.argv[2]+f'.exp{i}','w',encoding='utf-8').write(html.unescape(x)+'\n')
print(len(m))
