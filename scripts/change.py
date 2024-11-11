# -*- coding: utf-8 -*-
"""
Created on Wed May 20 20:42:35 2020

@author: HP
"""

import xarray as xr
import numpy as np


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





def find_changepoint(x, y, char=None, order=1):
    rss = np.nan * x
    for n in range(2, len(x)- 2):
        _, rssval = piecewise_polyfit(x, y, n, order)
        rss[n] = rssval
    if char.lower()=='onset':
        n0 = np.nanargmin(rss)
    elif char.lower()=='cessation':
        n0 = np.nanargmax(rss)
    x0 = x[n0]
    ypred, _ = piecewise_polyfit(x, y, n0)
    
    #print(x0)
    return x0, ypred, rss



var='vimd'
Data=xr.open_dataset('cum_vimd.nc')
Data_2_use=Data[var]

x=np.arange(1,len(Data.time)+1)
y=Data_2_use.values.flatten()


[a,b,c]=find_changepoint(x,y,char='onset')

print('Onset Changepoint: ', Data.time.values[a-1])


[a,b,c]=find_changepoint(x,y,char='cessation')

print('Cessation Changepoint: ', Data.time.values[a-1])

