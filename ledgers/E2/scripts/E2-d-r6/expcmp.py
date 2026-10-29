import re,sys,subprocess,html
page=open(sys.argv[1],encoding='utf-8').read()
labs=re.findall(r'<section class="lab[^"]*" id="([^"]+)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>',page,re.S)
for lid,code,exp in labs:
    code=html.unescape(code); exp=html.unescape(exp)
    twin=sys.argv[2]+'/'+lid.replace('lab-E2-project-','lab-E2-project-')+'.py'
    out=subprocess.run([sys.executable,'-I','-W','error',twin],capture_output=True,text=True).stdout
    print(lid,'expected==output:',out.strip()==exp.strip(), 'page code==twin:', code.strip()==open(twin,encoding='utf-8').read().strip())
