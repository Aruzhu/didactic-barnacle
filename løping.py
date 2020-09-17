# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 11:23:32 2020

@author: jon39
"""
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

interc = 0
def getCoeff(paceArr):
    global interc
    if paceArr != []:
        x = np.arange(1,len(paceArr)+1).reshape(-1,1)
        y = np.array(paceArr)
        model = LinearRegression()
        model.fit(x,y)
        interc = model.intercept_
        return model.coef_[0]
    else:
        return -1
    
spread = xlrd.open_workbook("C:/Users/jon39/OneDrive/Dokumenter/løping.xlsx")
løp = spread.sheet_by_name('løp')
downIndex = 2 # index of first km time of first race
horrIndex = 4

raceValues = []
paceAvg = []
coefs = []
cof = 1
timeVal = 1

race = downIndex-1

while cof != -1:
    race += 1 # reset
    timeVal = 1
    timeIndex = horrIndex-1
    raceValues = []
    
   
    while timeVal != '':
        timeIndex += 1
        try:
            timeVal = løp.cell(race,timeIndex).value
        except:
            break
        if timeVal != '':
            raceValues.append(timeVal)
    plt.plot(raceValues)
    cof = getCoeff(raceValues)
    #paceAvg.append(løp.cell(race,timeIndex-2).value)
    if cof != -1:
        coefs.append(cof)
plt.show()
plt.plot(coefs)
plt.show()
print(coefs)
print(getCoeff(coefs), interc)
print(paceAvg)
