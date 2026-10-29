import re,sys,html
pg=open(sys.argv[1]).read()
for L in ['01','02','03','04']:
    out=open(f'/tmp/M5-v/a-r5/lab-L{L}.out').read()
    m=re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', pg[pg.find('lab'):], re.S)
    print(L, 'twin output bytes', len(out))
