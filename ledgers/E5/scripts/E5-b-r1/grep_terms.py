import re, sys, html
pat = re.compile(r"rational|new keynesian|determinacy|open economy|exchange rate|HANK|dynamic programming|lagrang|kkt|gordon|expectation|filter|standard deviation|correlation|regression|consistent estimator|empirical distribution|coefficient of determination|policy rate|taylor|multiplier|steady state|solow|hicks|phelps|blanchard|friedman|builder|verifier|\bbuild\b|\bround\b|REQUEST|unit report|TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|important to note|studies show|experts agree|well known|obviously|clearly|roughly|historically|about 6|\.\.\.|…|…", re.I)
for f in sys.argv[1:]:
    t = open(f, encoding="utf-8").read()
    t = re.sub(r"<pre><code.*?</code></pre>", "[CODE]", t, flags=re.S)
    t = re.sub(r"<pre class=\"expected\".*?</pre>", "[EXP]", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    for n, line in enumerate(t.splitlines(), 1):
        for m in pat.finditer(line):
            s = max(0, m.start()-60); e = min(len(line), m.end()+50)
            print(f, n, repr(line[s:e]))
