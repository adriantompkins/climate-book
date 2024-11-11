from __future__ import division

import sys
sys.path.append('/scratch/oayim/project/atmos-tools')

import xarray as xray
import numpy as np
import atmos as atm
#from atm import *
data=xray.open_dataset('final_prec_asia_sn10_30_we60_100.nc')

#tmp = data.sel(time=slice('2000-01-01 11:30:00', '2000-012-31 11:30:00'))
#tmp2 = data.sel(time=slice('2000-06-01T11:30:00', '2000-12-31T11:30:00'))
dsloc = data.sel(lon=1, lat=1, method='nearest')

#dsloc1 = tmp2.sel(lon=1, lat=1, method='nearest')


y=dsloc['time']
x=np.arange(1,366,1)
n=150



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

print(np.shape(x))  
print(np.shape(y)) 
print(y)
#onset=x0
#p=[]
#tt=find_changepoint(x,y)
#p.append(tt)
print(tt)

