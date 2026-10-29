import subprocess, glob, os, sys
root="/tmp/verify30-AC4-a"; py=f"{root}/.venv/bin/python"
base=subprocess.run([py,"-I","-W","error",f"{root}/tests/labs/AC4/lab-AC4-L02-1.py"],capture_output=True,text=True).stdout
for f in sorted(glob.glob(f"{root}/ledgers/AC4/mutants/AC4-a-r30/*.py")):
    r=subprocess.run([py,"-I","-W","error",f],capture_output=True,text=True)
    print("KILLED" if (r.returncode!=0 or r.stdout!=base) else "SURVIVED", r.returncode, os.path.basename(f))
    if r.stdout!=base:
        import difflib
        print("  ", [l for l in difflib.unified_diff(base.splitlines(), r.stdout.splitlines(), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++','---')][:3])
