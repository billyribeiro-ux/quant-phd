import re,html,sys
sys.path.insert(0,'/tmp/fc1-v/a-r2')
page={'1':'/tmp/verifyC2-FC1-a/course/modules/FC/FC1/L01.html','2':'/tmp/verifyC2-FC1-a/course/modules/FC/FC1/L02.html','3':'/tmp/verifyC2-FC1-a/course/modules/FC/FC1/L03.html'}
for n,p in page.items():
    t=open(p,encoding='utf-8').read()
    exp=re.search(r'<pre class="expected"[^>]*>(.*?)</pre>',t,re.S).group(1)
    exp=html.unescape(exp).rstrip('\n')
    got=open(f'/tmp/fc1-v/a-r2/out{n}.txt',encoding='utf-8').read().rstrip('\n')
    code=re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>',t,re.S).group(1)
    code=html.unescape(code).rstrip('\n')
    twin=open(f'/tmp/verifyC2-FC1-a/tests/labs/FC1/lab-FC1-L0{n}-1.py',encoding='utf-8').read().rstrip('\n')
    print('L0'+n,'output match:',exp==got,'code==twin:',code==twin)
