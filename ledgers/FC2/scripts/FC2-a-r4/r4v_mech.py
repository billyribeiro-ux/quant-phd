"""Mechanical checks for FC2 slice a: hours, why-it-matters word counts, banned phrases, twin vs page code,
notation symbols, quiz/problem/misconception counts, and link targets."""
import html, json, re, sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
MOD = ROOT / 'course/modules/FC/FC2'
PAGES = ['index.html', 'L01.html', 'L02.html', 'L03.html']

def text_of(s):
    s = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(re.sub(r'\s+', ' ', s)).strip()

banned = ['TODO', 'TBD', 'lorem', 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise',
          'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known',
          'obviously', 'clearly', 'it can be shown', 'pkill', '…', '...', 'in this course we', 'we will see',
          'let us', "let's", 'as we saw', 'this section', 'in this lesson we', 'the reader', 'learners']
for p in PAGES:
    raw = (MOD / p).read_text(encoding='utf-8')
    t = text_of(raw)
    for b in banned:
        for m in re.finditer(re.escape(b), t, flags=re.I):
            print('BANNED-HIT', p, repr(b), '...', t[max(0, m.start()-60):m.end()+60])
    hrs = re.findall(r'data-hours(?:-lessons|-project)?="(\d+)"', raw)
    print(p, 'data-hours attrs:', hrs, 'eyebrow:', re.findall(r'class="eyebrow">([^<]*)<', raw))
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, flags=re.S)
    if wim:
        print(p, 'why-it-matters words:', len(text_of(wim.group(1)).split()))
    print(p, 'misconceptions:', raw.count('class="misconception"'),
          'quiz items:', raw.count('class="item"'),
          'problems:', len(re.findall(r'class="problem" id=', raw)),
          'tiers:', re.findall(r'data-tier="(\w+)"', raw))
    # problem ids per tier
    for tier in ['mechanics', 'proof', 'empirical', 'research']:
        m = re.search(r'data-tier="%s">(.*?)</div>\s*(?:<div class="tier"|</section>)' % tier, raw, flags=re.S)
        if m:
            print('   tier', tier, 'problems', re.findall(r'id="([A-Z]\d)"', m.group(1)))
    # solutions count
    print(p, 'solutions:', raw.count('<details class="solution">'), 'lab sections:', raw.count('class="lab'))

# twin vs page code
def run_block(raw):
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', raw, flags=re.S)
    return html.unescape(m.group(1)) if m else None

def expected_block(raw):
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', raw, flags=re.S)
    return html.unescape(m.group(1)) if m else None

for n in (1, 2, 3):
    raw = (MOD / f'L0{n}.html').read_text(encoding='utf-8')
    page_code = run_block(raw)
    twin = (ROOT / f'tests/labs/FC2/lab-FC2-L0{n}-1.py').read_text(encoding='utf-8')
    same = page_code is not None and page_code.strip('\n') == twin.strip('\n')
    print(f'L0{n} page code == twin (stripped): {same}; page code lines {len(page_code.splitlines()) if page_code else None}, twin lines {len(twin.splitlines())}')
    if not same and page_code:
        import difflib
        for line in list(difflib.unified_diff(twin.strip('\n').splitlines(), page_code.strip('\n').splitlines(), lineterm=''))[:20]:
            print('   ', line)
    print(f'L0{n} lab has @@ markers left:', '@@LAB' in raw or '@@OUT' in raw)
