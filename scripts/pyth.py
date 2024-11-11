#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:58:51 2020

@author: oayim
"""

from netCDF4 import Dataset as nd
import numpy as np
import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt
from datetime import datetime, timedelta #
import xarray as xr
import matplotlib.patches as mpatches

data=xr.open_dataset('final_prec_asia_sn10_30_we60_100.nc')
evap=xr.open_dataset('final_evap_asia_sn10_30_we60_100.nc')
vimd=xr.open_dataset('final_vimd_asia_sn10_30_we60_100.nc')
cum=xr.open_dataset('cum_vimd.nc')
tcwv=xr.open_dataset('phone.nc')
stor=xr.open_dataset('out.nc')
pe=xr.open_dataset('cum_MFC.nc')

tru=data
dat1=evap
dat2=vimd
dat3=cum
dat4=tcwv
dat5=stor
dat6=pe

tru['new']=data['tp']
dat1['e']=evap['e']
dat2['vimd']=vimd['vimd']
dat3['cum']=cum['vimd']
dat4['tcwv']=tcwv['tp']
dat5['stor']=stor['tcwv']
dat6['pe']=pe['tp']

#daily_data12 = tru.groupby('time.day').mean('time')
#dd_evap = dat1.groupby('time.day').mean('time')
#dd_vimd = dat2.groupby('time.day').mean('time')



pp=tru.sel(lon=0, lat=0, method='nearest')
ev=dat1.sel(lon=0, lat=0, method='nearest')
vimd=dat2.sel(lon=0, lat=0, method='nearest')
cum=dat3.sel(lon=0, lat=0, method='nearest')
tc=dat4.sel(lon=0, lat=0, method='nearest')
st=dat5.sel(lon=0, lat=0, method='nearest')
dt=dat6.sel(lon=0, lat=0, method='nearest')

fig, ax =plt.subplots()
plt.figure()

lns1=ax.plot(pp['new'], 'k-', label='precip')
ax.set_ylabel('$mmday^{-1}$')
ax.set_xlabel('Days of the Year')
#ax.legend(loc='upper left', borderaxespad=0, frameon=False)
ax.set_ylim(-5,15,1)

lns6=ax.plot(st['stor'], 'm-.', label='Residual')
ax.legend(loc='upper left', borderaxespad=0, frameon=False)

lns2=ax.plot(ev['e'],'r-',label='evap')
ax.legend(loc='upper left', borderaxespad=0, frameon=False)

ln5=ax.plot(vimd['vimd'], 'g-',label='MFC')
#ax.legend(loc='upper left', borderaxespad=0, frameon=False)


ax1=ax.twinx()
ax1.set_ylabel('mm')
lns3=ax1.plot(cum['cum'],'p', label= 'CMFC')
#ax1.legend(loc= 'center left', borderaxespad=0, frameon=False)

lns4=ax.plot(tc['tcwv'],'y', label= 'Storage')
#ax1.legend(loc= 'center left', borderaxespad=0, frameon=False)
#ax1.set_ylim(-20,20)

lns = lns1+lns2+lns3+lns4+ln5+lns6
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc='upper left')

#ax.grid()
#ax.set_ylim(-0.5,0.5)
#ax1.set_ylim(-2,22)
ax.set_title('Daily Average')

#plt.plot(tc['tcwv'],'b-', label= 'Storage')
#plt.plot(st['stor'],'k-', label= 'Residual')
#plt.legend()
#plt.title('Total Column Water Volume')
#plt.ylabel('$mm/day$')
#plt.xlabel('Days of the Year')
#pp['new'].plot.line('o-',color='blue',figsize=(15,10))


#ev['e'].plot.line('o-',color='red',figsize=(15,10))


#vimd['vimd'].plot.line('o-',color='black',figsize=(15,10))
#black_patch = mpatches.Patch(color='black', label='VIMD')
#plt.legend(handles=[black_patch,])

#cum['cum'].plot.line('o-',color='green',figsize=(15,10))
#green_patch = mpatches.Patch(color='green', label='Cum_VIMD')
#plt.legend(handles=[green_patch,])
plt.plot(dt['pe'],'b-', label= 'P-E')
plt.plot(cum['cum'],'k-', label= 'MFC')

xcoords = [0.22058956, 0.33088437, 2.20589566]
for xc in xcoords:
    plt.axvline(x=xc)
plt.axvline(x=140)
plt.legend()


#plt.savefig(fname='try.png', dpi='500', format='png')
plt.tight_layout()  
plt.show()

