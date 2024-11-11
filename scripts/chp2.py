# -*- coding: utf-8 -*-
"""
Created on Wed May 20 20:42:35 2020

@author: HP
"""

import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime, timedelta #

def split(x, n):
    return x[:n], x[n:]

def piecewise_polyfit(x, y, n, order=1):
    y = np.ma.masked_array(y, np.isnan(y))
    x1, x2 = split(x, n)
    y1, y2 = split(y, n)
    p1 = np.ma.polyfit(x1, y1, order)
    p2 = np.ma.polyfit(x2, y2, order)
    if np.isnan(p1).any() or np.isnan(p2).any():
        raise ValueError('NaN for polyfit coeffs. Check data.') 
    ypred1 = np.polyval(p1, x1)
    ypred2 = np.polyval(p2, x2)
    ypred = np.concatenate([ypred1, ypred2])
    rss = np.sum((y - ypred)**2)
    return ypred, rss



def find_changepoint(x, y, order=1):
    rss = np.nan * x
    for n in range(2, len(x)- 2):
        _, rssval = piecewise_polyfit(x, y, n, order)
        rss[n] = rssval
    n0 = np.nanargmin(rss)
    x0 = x[n0]
    ypred, _ = piecewise_polyfit(x, y, n0)
    print(x0)
    return x0, ypred, rss


#def find_changepoint(x, y, char=None, order=1):
 #   rss = np.nan * x
  #  for n in range(2, len(x)- 2):
   #     _, rssval = piecewise_polyfit(x, y, n, order)
    #    rss[n] = rssval
   # if char.lower()=='onset':
    #    n0 = np.nanargmin(rss)
 #   elif char.lower()=='cessation':
  #      n0 = np.nanargmax(rss)
  #  x0 = x[n0]
   # ypred, _ = piecewise_polyfit(x, y, n0)
    
    #print(x0)
   # return x0, ypred, rss


var='vimd'
Data=xr.open_dataset('cum_vimd.nc')
Dat=xr.open_dataset('cum_MFC.nc')


Data_2_use=Data[var]
MFC=Dat['tp']

PE=MFC.values.flatten()
CM=Data_2_use.values.flatten()

onset=np.arange(1,len(Data.time) - 121)
cessation=np.arange(1,len(Data.time) - 243)



y0 =Data_2_use.sel(time=slice('2000-01-01T11:30:00', '2000-08-31T11:30:00'))
y=y0.values.flatten()

j0 =MFC.sel(time=slice('2000-01-01T11:30:00', '2000-08-31T11:30:00'))
j=j0.values.flatten()



y1= Data_2_use.sel(time=slice('2000-09-01T11:30:00', '2000-12-31T11:30:00'))
yy=y1.values.flatten()

v0=MFC.sel(time=slice('2000-09-01T11:30:00', '2000-12-31T11:30:00'))
v=v0.values.flatten()



[a,b,c]=find_changepoint(onset,y)
[e,f,g]=find_changepoint(cessation,yy)

[k,l,m]=find_changepoint(onset,j)
[q,r,s]=find_changepoint(cessation,v)

#print(pp)
#print(np.shape(j),np.shape(v))
#print(np.shape(cessation),np.shape(yy))
d=[]
n=[]
d.append(a)
d.append(e+244)

n.append(k)
n.append(q+244)

print(d)
print('Changepoint of Onset: ', Data.time.values[a])
print('Changepoint of Cessation: ', Data.time.values[e+244])


print('Changepoint of MFC_Onset: ', Data.time.values[k])
print('Changepoint of MFC_Cessation: ', Data.time.values[q+244])


plt.plot(PE,'b-', label= 'Cum(P-E)')
plt.plot(CM,'r-', label= 'Cum_MFC')
#plt.title('Cumulative Storage and Change Point Indices')
plt.ylabel('$mm/day$')
plt.xlabel('Days of the Year')

#xcoords = [0.22058956, 0.33088437, 2.20589566]
for xc in d:
    plt.axvline(x=xc,color='r', linestyle='--')
    
for xc in n:
    plt.axvline(x=xc,color='b', linestyle='-')
    
 
#plt.axvline(x=140)
plt.legend()
plt.show()
