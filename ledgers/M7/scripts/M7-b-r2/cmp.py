import re,sys,html
for t in ['L04','L05','L06']:
    src=open(f'course/modules/M/M7/{t}.html').read()
    m=re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>',src,re.S)
    exp=html.unescape(m[0]).strip()
    got=open(f'/tmp/M7-v/b/out/{t}.txt').read().strip()
    print(t,'match' if exp==got else 'MISMATCH', len(m))
