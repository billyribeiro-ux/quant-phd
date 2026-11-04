"""LX2-d round 1: printed page of each SR 26-2 attachment quotation cited by the cards and L04.

The attachment (sr2602a1.pdf, fetched by fetch_sources.sh) carries printed page numbers as footers. The text is
flattened, each quotation is located by character offset, and the page is the first footer line after that offset.
Also checks that the words 'hit' and 'bias' do not occur in the attachment or the letter.
Usage: python3 -I sr_pages.py   (reads /tmp/lx2d-src/att.txt and letter.txt)
"""
import re
att_lines = open('/tmp/lx2d-src/att.txt', encoding='utf-8').read().split('\n')
letter = open('/tmp/lx2d-src/letter.txt', encoding='utf-8').read()
# build flattened text with a map from char offset to the line index
flat_parts, offsets = [], []
pos = 0
for idx, ln in enumerate(att_lines):
    if re.match(r'^\s{20,}\d{1,2}\s*$', ln):
        s = ' '  # footer line: excluded from the text, kept for page mapping
    else:
        s = re.sub(r'\s+', ' ', ln).strip() + ' '
    flat_parts.append(s)
    offsets.append((pos, idx))
    pos += len(s)
flat = ''.join(flat_parts)
footer_idx = [(idx, int(m.group(1))) for idx, ln in enumerate(att_lines) for m in [re.match(r'^\s{20,}(\d{1,2})\s*$', ln)] if m]
def line_of(offset):
    best = 0
    for start, idx in offsets:
        if start <= offset:
            best = idx
        else:
            break
    return best
def page_of_line(idx):
    for j, p in footer_idx:
        if j >= idx:
            return p
    return None
def locate(q):
    q = re.sub(r'\s+', ' ', q)
    k = flat.find(q)
    if k < 0:
        return None, None
    ln = line_of(k)
    return page_of_line(ln), ln + 1
quotes = {
 'model definition (complex quantitative method)': 'a complex quantitative method, system, or approach',
 'excludes simple arithmetic calculations': 'simple arithmetic calculations, such as those found within spreadsheets',
 'model risk definition': 'the potential for adverse financial consequences associated with models',
 'responsible for adopting (start, page 1)': 'Each banking organization ultimately is responsible for adopting model',
 'does not set forth enforceable standards': 'does not set forth enforceable standards or prescriptive requirements',
 'will not result in supervisory criticism': 'will not result in supervisory criticism against a banking organization',
 'footnote 1 supervisory action': 'supervisory action may result for any violations of law or unsafe or unsound practices',
 'Conceptual Soundness heading': 'Conceptual Soundness Validating conceptual soundness involves',
 'Outcomes Analysis heading': 'Outcomes Analysis Outcomes analysis compares model outputs',
 'Outcomes Analysis paragraph 1 definition': 'outcomes analysis compares model outputs to corresponding real-world outcomes',
 'outcomes analysis can take many forms (paragraph 2)': 'Outcomes analysis can take many forms',
 'persistent deviations (paragraph 1)': 'persistent deviations outside of the banking organization',
 'Ongoing Model Monitoring definition': 'Ongoing model monitoring involves an evaluation',
 'Model validation evaluates (section V)': 'Model validation evaluates whether models perform as expected',
 'Effective model use depends (section IV)': 'Effective model use depends on a clear understanding',
 'Users of model output benefit (before Components)': 'Users of model output benefit from understanding',
 'Components of Model Validation heading': 'Components of Model Validation',
}
for name, q in quotes.items():
    page, line = locate(q)
    print(f"{name}: printed page {page} (text line {line})")
att_text = open('/tmp/lx2d-src/att.txt', encoding='utf-8').read()
print('attachment contains hit/bias (case-insensitive substring):', [w for w in ['hit', 'bias'] if re.search(w, att_text, re.I)])
print('letter contains hit/bias (case-insensitive substring):', [w for w in ['hit', 'bias'] if re.search(w, letter, re.I)])
print('footer pages found:', [p for _, p in footer_idx])
print('letter supersedes 11-7:', 'SR letter 11-7' in letter, '| 21-8:', 'SR letter 21-8' in letter, '| Supersedes: label:', 'Supersedes:' in letter)
