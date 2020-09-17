import yfinance as yf
import numpy as np
import time
import matplotlib.pyplot as plt


# AMD, INTC
stockdata = {}
stocks = ['FB','NVDA','NKE','AAPL', 'MSFT', 'AMD', 'KO', 'AMZN', 'GOOGL', 'DIS', 'V', 'MA'] # 0-1-2-3-4-5
stocks += ['TSLA','WMT','JPM','VZ','BAC','PFE','NFLX','INTC']
#stocks += ['CVS', 'NVAX']
#stocks += ['SRNE', 'MOS']

port = []
stockPerf = {}
edges = [[]]
weights = [[]]
visited = []

"""
1. hente masse stock data fra div stocks
2. sette opp en edge matrix
3. regne ut vekter, med formel fra artikkel
4. lag en mst
4.1 fjerne de høyeste vektene fra edgematrisen. 0->0.8
4.2 gjør dfs, finn ut om man har en sykel, (treffer på en visited node)
4.3 gjenta til man har en mut
5. bruk ytternodene i mut. rate etter logperf og std og yf data recommends?
6. implementer UCLD1 algoritmen
7. se hvor bra detta egt er.
"""

startT = '2015-2-19' # 3 year max ish
endT = '2015-3-19' # bruke til å etablere verdier
endT2 = '2020-8-15' # tipper etter dette punktet

def visit(index, indexB, edgeList): # [[4], [3], [3], [4], []]
    global visited
    a = False
    if index == indexB: # quit case
        return True
    elif edgeList[index] != []:
        visited.append(index)
        i = 0
        while (a == False) and i<len(edgeList[index]):
            a = visit(edgeList[index][i], indexB, edgeList)
            i += 1
    return a
edgeVals = {} # index - [weight fromindex]
def mstVisit(index, edgeList, weights, mutedges): # Prims
    visited.append(index)
    for i in edgeList[index]:
        Wval = weights[index][edgeList[index].index(i)]
        if i in edgeVals.keys():
            if Wval < edgeVals[i][0] and not (i in visited):
                edgeVals[i] = [Wval, index]
        elif not (i in visited):
            edgeVals[i] = [Wval, index]

    if len(visited) != len(stocks):
        Wvalues = [edgeVals[z][0] for z in edgeVals.keys()]
        maxKey = list(edgeVals.keys())[np.argmin(list(Wvalues))]
        fromKey = list(edgeVals[maxKey])[1]
        print(maxKey, fromKey)
        mutedges = addList(fromKey, maxKey, maxKey, fromKey, mutedges)
        del edgeVals[maxKey]
        mutedges = mstVisit(maxKey, edgeList, weights, mutedges)
    return mutedges
def addList(a, b, va, vb, datalist):
    datalist[a].append(va)
    while True:
        try:
            datalist[b].append(vb)
            return datalist.copy()
        except:
            datalist.append([])
def remList(a,b, c, vc, datalist):
    del datalist[a][b]
    datalist[c].remove(vc)
    return datalist
def fetch(startT, endT, incList):
    global stocks
    for stock in stocks: # O(N)
        df = yf.Ticker(stock).history(period='1d', start=startT, end=endT)
        data = df.values.tolist()
        stockvals = [data[i][j] for i in range(len(data)) for j in incList] # includes high / low of the day
        stockvals = np.array(stockvals)
        stockdata[stock] = stockvals
    return stockdata
stockdata = fetch(startT, endT, [0, 1, 2, 3])
for stock in stocks:
    logPrice = np.mean(np.log(stockdata[stock][1:]/stockdata[stock][:-1]))
    stockPerf[stock] = [logPrice, 1/stockdata[stock].std()]
    print(stock, logPrice, stockdata[stock].std())

for stockA in stocks: # O(N^2) time. stock A ==> B 1-2 1-3 2-3
    indexA = stocks.index(stockA)
    for stockB in stocks[indexA:]:
        indexB = stocks.index(stockB)
        if stockA != stockB:
            try:
                dataA = stockdata[stockA]
                dataB = stockdata[stockB]
                covar = np.cov(dataA, dataB)[0, 1]/(dataA.std()*dataB.std())
                print(stockA, stockB, covar)
                covar = np.sqrt(2*(1-covar))
                edges = addList(indexA, indexB, indexB, indexA, edges)
                weights = addList(indexA, indexB, covar, covar, weights)
            except:
                print("BAD", stockA, stockB)
                pass

mutedges = [[]]
visited = []
perfweight = []

mutedges = mstVisit(0 ,edges, weights, mutedges)
numVert = [len(mutedges[i]) for i in range(len(mutedges))]
root = np.argmax(numVert)
for i in range(len(stocks)):
    if numVert[i] == 1:
        port.append(stocks[i])
# UCB1
def choose(stock, stockdata, cum, stockPerf):
    a = stockdata[stock][t]
    b = stockdata[stock][t-1]
    cum += a-b
    new = (stockPerf[stock][0] + np.log(a/b))*0.5
    return [cum, new]
print(port)

cum = 0
used = [0]*len(port)
upperbound = [0]*len(port)
stockdata = fetch(endT, endT2, [0])

cumVals = []
bestVals = []
for t in range(1, len(stockdata[stocks[0]])):
    if t<len(port)+1: # use stock port[t]
        best = t-1
    else: # use equation
        for i in range(len(port)):
            upperbound[i] = stockPerf[port[i]][0] + np.sqrt(2*np.log(t)/(used[i]*t))
        best = np.argmax(upperbound)
    cum, stockPerf[port[best]][0] = choose(port[best], stockdata, cum, stockPerf)
    used[best] += 1
    cumVals.append(cum)
    bestVals.append(best)
print(cum)
plt.plot(bestVals)
plt.show()
plt.plot(cumVals)
plt.show()
