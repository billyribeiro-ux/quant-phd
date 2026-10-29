import re, sys, pathlib, hashlib, subprocess
root = pathlib.Path(sys.argv[1])
P = "44f1eb6a417ce687a9b88c7ee917e72566b29892"
for n in range(13, 19):
    p = f"course/modules/M/M2/L{n}.html"
    t = (root / p).read_text(encoding="utf-8")
    order = [m.group(1) for m in re.finditer(r'<(section|div|p|h2|ul|ol|nav|header)[^>]*(?:class="([^"]*)")?[^>]*>', t)]
    marks = {k: t.find(k) for k in ['class="why-it-matters"', 'id="s1"', 'class="lab"', 'class="canon-breaks"', 'class="misconceptions"', 'class="problem-set"', 'class="key-results"', 'id="key-results"', 'class="quiz"', 'id="references"']}
    seq = sorted(marks.items(), key=lambda kv: kv[1])
    wm = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S).group(1)
    wc = len(re.sub(r"<[^>]+>|\\\(|\\\)", " ", wm).split())
    probs = len(re.findall(r'class="problem"', t))
    sols = len(re.findall(r'<details class="solution">', t))
    items = len(re.findall(r'<li class="item"', t))
    explains = len(re.findall(r'<div class="explain" hidden>', t))
    correct = len(re.findall(r'data-correct', t))
    print(f"L{n}: order {[k for k,_ in seq]}; why_words {wc}; problems {probs}; solutions {sols}; quiz items {items}; explain divs {explains}; data-correct {correct}; data-hours {'data-hours=\"10\"' in t}")
    cur = hashlib.sha256((root / p).read_bytes()).hexdigest()[:12]
    old = subprocess.run(["git", "show", f"{P}:{p}"], capture_output=True, cwd=root).stdout
    print(f"   page sha now {cur}; identical to round-6 pin: {hashlib.sha256(old).hexdigest()[:12] == cur}")
    tw = f"tests/labs/M2/lab-M2-L{n}-1.py"
    oldt = subprocess.run(["git", "show", f"{P}:{tw}"], capture_output=True, cwd=root).stdout
    print(f"   twin identical to round-6 pin: {oldt == (root / tw).read_bytes()}")
