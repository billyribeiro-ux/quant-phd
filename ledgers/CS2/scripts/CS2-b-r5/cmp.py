import html,re,sys
base='/tmp/verifyB5-CS2-b/'
for L in ['L05','L06','L07','L08']:
    page=open(base+f'course/modules/CS/CS2/{L}.html',encoding='utf-8').read()
    m=re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>',page,re.S)
    code=html.unescape(m.group(1))
    twin=open(base+f'tests/labs/CS2/lab-CS2-{L}-1.py',encoding='utf-8').read()
    e=re.search(r'<pre class="expected"[^>]*>(.*?)</pre>',page,re.S)
    exp=html.unescape(e.group(1))
    out=open(f'/tmp/CS2-v/CS2-b-r5/lab-{L}.out',encoding='utf-8').read()
    print(L,'code==twin',code.strip()==twin.strip(),'expected==run',exp.strip()==out.strip(), len(code), len(twin))
    if code.strip()!=twin.strip():
        import difflib
        print('\n'.join(list(difflib.unified_diff(twin.strip().splitlines(),code.strip().splitlines(),lineterm=''))[:30]))
    if exp.strip()!=out.strip():
        import difflib
        print('\n'.join(list(difflib.unified_diff(out.strip().splitlines(),exp.strip().splitlines(),lineterm=''))[:30]))
