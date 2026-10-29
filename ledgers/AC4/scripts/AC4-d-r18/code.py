import re,sys,html
src=open(sys.argv[1],encoding='utf-8').read()
m=re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>',src,re.S)
open(sys.argv[2],'w',encoding='utf-8').write(html.unescape(m.group(1))+'\n')
