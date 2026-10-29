import re,sys,html
page=open(sys.argv[1],encoding='utf-8').read()
out=open(sys.argv[2],encoding='utf-8').read()
m=re.search(r'<pre class="expected"[^>]*>(.*?)</pre>',page,re.S)
exp=html.unescape(m.group(1))
print("EXPECTED==OUTPUT:", exp.strip()==out.strip())
if exp.strip()!=out.strip():
    import difflib
    print("\n".join(difflib.unified_diff(exp.strip().splitlines(),out.strip().splitlines(),lineterm='')))
