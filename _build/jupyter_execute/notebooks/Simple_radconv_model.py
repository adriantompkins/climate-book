#!/usr/bin/env python
# coding: utf-8

# In[1]:


import climlab


# In[2]:


from platform import python_version

print(python_version())


# In[3]:


state = climlab.column_state(num_lev=30)
state


# In[4]:


import climlab
alb = 0.25
#  State variables (Air and surface temperature)
state = climlab.column_state(num_lev=30)
#  Parent model process
rcm = climlab.TimeDependentProcess(state=state)
#  Fixed relative humidity
h2o = climlab.radiation.ManabeWaterVapor(state=state)
#  Couple water vapor to radiation
rad = climlab.radiation.RRTMG(state=state, specific_humidity=h2o.q, albedo=alb)
#  Convective adjustment
conv = climlab.convection.ConvectiveAdjustment(state=state, adj_lapse_rate=6.5)
#  Couple everything together
rcm.add_subprocess('Radiation', rad)
rcm.add_subprocess('WaterVapor', h2o)
rcm.add_subprocess('Convection', conv)
#  Run the model
rcm.integrate_years(1)
#  Check for energy balance
print (rcm.ASR - rcm.OLR)


# In[5]:


import importlib
importlib.import_module("climlab")


# In[ ]:




