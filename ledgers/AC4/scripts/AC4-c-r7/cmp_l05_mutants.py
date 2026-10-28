import html, re, subprocess
root="/tmp/verify7-AC4-c"; py=f"{root}/.venv/bin/python"
t=open(f"{root}/course/modules/AC/AC4/L05.html",encoding="utf-8").read()
exp=html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>',t,re.S).group(1)).strip()
for f in ["n04_L05_fixed_overhead_flexes_with_units.py","n05_L05_flexed_uses_actual_kg.py"]:
    out=subprocess.run([py,"-I","-W","error",f"{root}/ledgers/AC4/mutants/AC4-c-r7/{f}"],capture_output=True,text=True)
    print(f, "rc", out.returncode, "MATCH" if out.stdout.strip()==exp else "DIFFERS")
    print("  differing lines:", [l for l in out.stdout.splitlines() if l not in exp.splitlines()][:4])
