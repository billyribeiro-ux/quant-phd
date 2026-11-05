import re, sys, html
def norm(s):
    s = html.unescape(s)
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('—', '--').replace('–', '-').replace('­','')
    s = re.sub(r'\s+', ' ', s)
    return s
def flat_source(paths):
    t = ''
    for p in paths:
        raw = open(p, encoding='utf-8', errors='replace').read()
        # join hyphenated line breaks like 'con- sistent'
        raw = re.sub(r'(\w)-\n\s*(\w)', r'\1\2', raw)
        t += ' ' + raw
    t = norm(t)
    t = re.sub(r'[\*—]', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    # strip running headers like 'Cite as: 521 U. S. 642 (1997) 679' and 'Opinion of Scalia, J.' and 'UNITED STATES v. O'HAGAN 680'
    t = re.sub(r'Cite as: 521 U\. S\. 642 \(1997\)\s*\d*', ' ', t)
    t = re.sub(r'\d{3}\s+UNITED STATES v\. O\'HAGAN', ' ', t)
    t = re.sub(r'UNITED STATES v\. O\'HAGAN\s+\d{3}', ' ', t)
    t = re.sub(r'Opinion of [A-Za-z ,.]+?, J\.', ' ', t)
    t = re.sub(r'Opinion of the Court', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t
if __name__ == '__main__':
    src = flat_source(sys.argv[2:])
    text = open(sys.argv[1], encoding='utf-8').read()
    text = re.sub(r'<[^>]+>', '', text)
    quotes = re.findall(r'“([^”]{12,})”', text)
    for q in quotes:
        qn = norm(q)
        # drop bracketed alterations and ellipses: test each piece of >=4 words
        pieces = [p.strip(' .,;:') for p in re.split(r'\[[^\]]*\]|\.\.\.|\. \. \.|…', qn)]
        ok = True; miss = []
        for p in pieces:
            if len(p.split()) < 4: continue
            if p not in src:
                ok = False; miss.append(p)
        print(('OK  ' if ok else 'MISS'), qn[:90], ('' if ok else ' || missing: ' + ' ... '.join(m[:80] for m in miss)))
