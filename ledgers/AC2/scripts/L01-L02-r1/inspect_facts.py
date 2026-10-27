import json,sys
d=json.load(open(sys.argv[1]))
g=d["facts"]["us-gaap"]
tags=["Revenues","RevenueFromContractWithCustomerExcludingAssessedTax","SalesRevenueNet","NetIncomeLoss","Assets","CostOfRevenue","CostOfGoodsAndServicesSold","AccountsReceivableNetCurrent","LongTermDebtNoncurrent","CommonStockSharesOutstanding","StockholdersEquity","LiabilitiesCurrent","AssetsCurrent","CashAndCashEquivalentsAtCarryingValue","OperatingIncomeLoss","DepreciationDepletionAndAmortization","DepreciationAndAmortization","Depreciation","NetCashProvidedByUsedInOperatingActivities","PropertyPlantAndEquipmentNet","Liabilities","SellingGeneralAndAdministrativeExpense"]
for t in tags:
    if t not in g: print(t,"ABSENT"); continue
    units=g[t]["units"]
    for u,rows in units.items():
        keys=set()
        for r in rows: keys|=set(r.keys())
        forms={}
        for r in rows: forms[r["form"]]=forms.get(r["form"],0)+1
        print(t,u,"n=",len(rows),"forms=",forms,"keys=",sorted(keys))
