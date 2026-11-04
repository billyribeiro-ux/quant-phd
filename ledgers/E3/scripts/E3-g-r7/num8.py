from fractions import Fraction as F
import math
W1, WL, W0 = 110000, 95000, 100000
def ce(p, w1=W1, wl=WL):
    return 1/(p/F(w1) + (1-p)/F(wl))
print('EU ce 1/2', float(ce(F(1,2))), ce(F(1,2)) == F(4180000,41), F(4180000,41))
print('maxmin 1/3', float(ce(F(1,3))))
print('ce 1/4', ce(F(1,4)), float(ce(F(1,4))), F(1672000,17), float(F(1672000,17)))
print('ce 3/4', float(ce(F(3,4))))
print('premium', F(102500)-ce(F(1,2)), float(F(102500)-ce(F(1,2))), F(22500,41))
print('known red', float(ce(F(1,3), W1, W0)), 'known black', float(ce(F(2,3), W1, W0)))
print('known red mirrored check', float(1/(F(1,3)/110000 + F(2,3)/100000)))
print('known black', float(1/(F(2,3)/110000 + F(1,3)/100000)))
print('amb full set red min', min(float(ce(F(k,90), W1, W0)) for k in range(91)))
print('ambig full set black min', min(float(1/(F(k,90)/W1 + (1-F(k,90))/W0 * 0 + 0)) if False else 0 for k in range(1)))
# black bet on full set: black prob q=1-k/90; ce_bet(q)
def ce_bet(q):
    return 1/(q/F(W1) + (1-q)/F(W0))
print('black full min', float(min(ce_bet(1-F(k,90)) for k in range(91))))
print('30-60 red min', float(min(ce_bet(F(k,90)) for k in range(30,61))), 'black min', float(min(ce_bet(1-F(k,90)) for k in range(30,61))))
print('prospect', 5-math.sqrt(50), -((-(5-math.sqrt(50)))/2)**2, 100000 - 100*((math.sqrt(50)-5)/2)**2*100/100)
ce_cu = -((math.sqrt(50)-5)/2)**2
print('prospect CE CU', ce_cu, 'cents', ce_cu*100, 'wealth', 100000+ce_cu*100)
print('risk premium cu', float(F(548.7805)) if False else 548.7805/100)
print('maxmin - w0', float(ce(F(1,3)) - W0))
print('M2 ce 3/4 exact', ce(F(3,4)))
print('mean', F(110000)/4 + F(95000)*3/4)
print('EZ CE w psi=0.5', 4180000/41)
print('prospect eq c.CU check', 0.5*10 + 0.5*(-2*math.sqrt(50)))
