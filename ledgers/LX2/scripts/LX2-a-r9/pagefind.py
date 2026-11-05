import subprocess, re, sys
pdf, pats = sys.argv[1], sys.argv[2:]
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
for i in range(1, n + 1):
    t = subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), '-layout', pdf, '-'], capture_output=True, text=True).stdout
    flat = re.sub(r'\s+', ' ', t).replace('’', "'").replace('“', '"').replace('”', '"')
    nums = re.findall(r'(?m)^\s*(\d{3})\s+\S|\S\s+(\d{3})\s*$', t)
    hdr = sorted({a or b for a, b in nums})
    for p in pats:
        q = re.sub(r'\s+', ' ', p).replace('’', "'")
        if q in flat:
            print(f'pdfpage={i} hdr_nums={hdr} FOUND: {p[:70]}')
