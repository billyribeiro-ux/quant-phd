"""Banned-phrase, process-word and ellipsis scan of the BK4 slice pages (visible text, outside code blocks)."""
import re, html, sys
ROOT = sys.argv[1]
banned = ['TODO', 'TBD', 'lorem', 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise',
          'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known',
          'obviously', 'clearly']
proc = r'\b(builder|build|verifier|verification|round|REQUESTS?|unit report|fixer|planner|architect|ledger|fragment)\b'
hits = 0
for p in ['index', 'L01', 'L02', 'L03']:
    raw = open(f'{ROOT}/course/modules/BK/BK4/{p}.html', encoding='utf-8').read()
    txt = html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>', '', raw, flags=re.S))
    txt = re.sub(r'<[^>]+>', ' ', txt)
    for b in banned:
        for m in re.finditer(re.escape(b), txt, re.I):
            hits += 1; print(p, 'BANNED', b)
    for m in re.finditer(proc, txt, re.I):
        hits += 1; print(p, 'PROCESS', m.group(0))
    stripped = re.sub(r'<pre.*?</pre>|<code.*?</code>', '', raw, flags=re.S)
    stripped = html.unescape(re.sub(r'<[^>]+>', ' ', stripped))
    for m in re.finditer(r'\.\.\.|…', stripped):
        hits += 1; print(p, 'ELLIPSIS', stripped[max(0, m.start()-30):m.end()+10].replace('\n', ' '))
print('hits:', hits)
