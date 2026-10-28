import re,html,subprocess,sys
root='/tmp/verify11-CF1-a'
for lab,page in [('L01','L01'),('L02','L02')]:
    src=open(f'{root}/course/modules/CF/CF1/{page}.html',encoding='utf-8').read()
    m=re.search(r'<pre class="expected"[^>]*>(.*?)</pre>',src,re.S)
    exp=html.unescape(m.group(1))
    out=subprocess.run([f'{root}/.venv/bin/python','-I','-W','error',f'{root}/tests/labs/CF1/lab-CF1-{lab}-1.py'],capture_output=True,text=True).stdout
    code=re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>',src,re.S).group(1)
    code=html.unescape(code)
    twin=open(f'{root}/tests/labs/CF1/lab-CF1-{lab}-1.py',encoding='utf-8').read()
    print(lab,'expected==twin stdout:',exp.strip()==out.strip(),'page code==twin:',code.strip()==twin.strip())
    if code.strip()!=twin.strip():
        import difflib;print('\n'.join(list(difflib.unified_diff(twin.splitlines(),code.splitlines(),lineterm=''))[:20]))
