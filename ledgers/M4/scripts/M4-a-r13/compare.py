import re,sys,html,subprocess
root=sys.argv[1]
for L in ["01","02","03","04"]:
    page=open(f"{root}/course/modules/M/M4/L{L}.html",encoding="utf-8").read()
    twin=open(f"{root}/tests/labs/M4/lab-M4-L{L}-1.py",encoding="utf-8").read()
    m=re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>',page,re.S)
    code=html.unescape(m.group(1))
    print(L,"code==twin:",code.strip()==twin.strip(), "len",len(code), len(twin))
    e=re.search(r'<pre class="expected"[^>]*>(.*?)</pre>',page,re.S)
    exp=html.unescape(e.group(1)).strip()
    out=open(f"{root}/ledgers/M4/scripts/M4-a-r13/twin-L{L}.out",encoding="utf-8").read().strip()
    print(L,"expected==output:",exp==out, "n expected blocks", len(re.findall(r'<pre class="expected"',page)))
    if exp!=out:
        import difflib; print("\n".join(difflib.unified_diff(out.splitlines(),exp.splitlines(),lineterm="")))
