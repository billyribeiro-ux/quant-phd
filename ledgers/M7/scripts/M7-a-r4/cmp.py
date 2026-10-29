import re,sys,html
pairs={'L01':'lab-M7-L01-1','L02':'lab-M7-L02-1','L03':'lab-M7-L03-1'}
base='/tmp/verifyB4-M7-a/'
for n,t in pairs.items():
    page=open(base+f'course/modules/M/M7/{n}.html',encoding='utf-8').read()
    code=re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>',page,re.S).group(1)
    code=html.unescape(code)
    twin=open(base+f'tests/labs/M7/{t}.py',encoding='utf-8').read()
    exp=re.search(r'<pre class="expected"[^>]*>(.*?)</pre>',page,re.S).group(1)
    exp=html.unescape(exp)
    out=open(f'/tmp/m7v4/a/out-{n}.txt',encoding='utf-8').read()
    print(n,'code==twin:',code.strip()==twin.strip(),'expected==output:',exp.strip()==out.strip(), 'lines',len(out.splitlines()))
