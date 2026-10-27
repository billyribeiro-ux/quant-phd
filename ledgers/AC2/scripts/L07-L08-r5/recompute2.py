from fractions import Fraction as F
rows=[]
for p in [F(1,1000),F(1,100),F(5,100)]:
    for spec in [F(90,100),F(95,100),F(99,100)]:
        fpr=1-spec; s=F(1,2)
        ppv=p*s/(p*s+(1-p)*fpr); flags=1000*(1-p)*fpr
        rows.append((float(p),float(spec),float(fpr),round(float(ppv),4),round(float(flags),2)))
for r in rows: print(r)
print('E2 ratio 0.3448/0.0099 =', 0.3448/0.0099, ' exact PPVs ratio', float((F(5,100)*F(1,2)/(F(5,100)*F(1,2)+F(95,100)*F(5,100)))/(F(1,1000)*F(1,2)/(F(1,1000)*F(1,2)+F(999,1000)*F(5,100)))))
print('P3 LEV', float(F(300,950)), float(F(310,1050)))
print('E3 LEV', float(F(300,1150)), float(F(330,1050)))
print('E2 118/1100', float(F(118,1100)), 'vs 117/1100', float(F(117,1100)))
print('prop4.3 AND/OR', 0.10*0.05, 1-(1-0.10)*(1-0.05))
print('growth witness DSRI', (F(150,1500))/(F(100,1000)), 'SGAI', (F(225,1500))/(F(150,1000)), 'SGI', F(1500,1000))
print('E1 gap', -1.5067-(-2.4747))
print('PPV 0.005/0.0545', float(F(5,1000)/F(545,10000)))
