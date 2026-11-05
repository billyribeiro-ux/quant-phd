import sys
p = sys.argv[1]
t = open(p).read()
Q = '" + LOG + "'  # literal source text: the generator concatenates LOG
reps = [
    (' Logs: " + LOG + "/probe_overflow (run inline; see E4d8-no-upper-bound)."', ' Log: ' + Q + '/probe_reference_r8.txt."'),
    ('costs below about 354.9 = ln(2^1024)/2... i.e. where exp(2c) is finite, noise volumes below about 1e153', 'costs up to 354 (cost 355 overflows exp(2c)), noise volumes up to 1e153'),
    ('(run inline; see E4d8-no-upper-bound)', '(log: probe_reference_r8.txt)'),
    ('Counterexamples (reference solve_model, scratch copies in " + LOG + "/../probe logs as recorded here):', 'Counterexamples (reference solve_model; ' + Q + '/probe_reference_r8.txt):'),
    ('Either restrict :326 to the finite range (cost below about 354.9 and noise volume below about 1e153, stated explicitly)', 'Either restrict :326 to the finite range (cost up to 354 and noise volume up to 1e153, stated explicitly)'),
    ("At sigma = 1e-30 it returns about 0.18 of the root's value instead of 9.656254e-31 (E4d8-cap-100-survives).", "At sigma = 1e-30 it returns 1.1832913578e-30 against the closed form 9.656254e-31 (23% high, gap -0.0291 instead of +3.8e-14; " + Q + "/probe_cap100_r8.txt) (E4d8-cap-100-survives)."),
    ('Observable: at sigma = 1e-30 the bracket after 100 halvings is 2^-100 = 7.9e-31, about 82% of the root 9.656254e-31, so the answer is wrong; the reference is within 3e-13 relative of the closed form.', 'Observable (' + Q + '/probe_cap100_r8.txt): at sigma = 1e-30 it returns 1.1832913578e-30 against 9.656254e-31 (23% high; gap -0.0291 against +3.8e-14); at sigma = 1e-40 it returns 3.944e-31 against 9.66e-41. The reference is within 3e-13 relative of the closed form at both (' + Q + '/probe_reference_r8.txt).'),
    ('Probe: sd = 1000 is rejected by this mutant and accepted by the reference (the probe test fails only for the mutant, checked this round).', 'Probe: sd = 1000 is rejected by this mutant and accepted by the reference (' + Q + '/probe_reference_r8.txt; the proposed test fails only for the mutant, checked this round).'),
    ('Probe: cost 50 is rejected by the mutant, accepted by the reference.', 'Probe: cost 50 is rejected by the mutant and accepted by the reference (' + Q + '/probe_reference_r8.txt).'),
]
for old, new in reps:
    print(t.count(old), old[:60])
    t = t.replace(old, new)
open(p, 'w').write(t)
