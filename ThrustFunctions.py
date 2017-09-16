
# coding: utf-8

# In[30]:

import krpc
import csv
#import math
import time


# In[31]:

conn = krpc.connect()


# In[32]:

vessel = conn.space_center.active_vessel
kerbin = conn.space_center.bodies['Kerbin']

#cframe = conn.space_center.ReferenceFrame.create_hybrid(kerbin.reference_frame,vessel.surface_reference_frame)


# In[42]:

# Reads variables from CSV and assigns to lists

logsheet = open("APTD.csv",'rb')
reader = csv.reader(logsheet)
variables = []
reader.next()
for row in reader:
    variables.append(row)
logsheet.close()

variables = [list(x) for x in zip(*variables)]

altL   = [float(x) for x in variables[0]]
pressL = [float(x) for x in variables[1]]
tempL  = [float(x) for x in variables[2]]
densL  = [float(x) for x in variables[3]]

del variables


# In[28]:

# Returns static atmospheric pressure at given altitude
def altPress(altitude):
    i = [abs(altitude-x) for x in altL].index(min([abs(altitude-x) for x in altL]))
    return pressL[i]


# In[65]:

# Thrust = Vac Thrust -((Vac Thrust - Sea Level Thrust)*(local press / sea lvl press))
vacThrust = 215000.0 #vessel.max_vacuum_thrust
tRange = 46578.78125 #Newtons
seaPress = 100142.2578125

# Returns thrust at given altitude. Depends on externally defined variables
def Thrust(alt):
    return  vacThrust - ( tRange * ( altPress(alt) / seaPress ) )


# In[ ]:

# Fuel flow rate in kilograms per second
kgps = (vessel.max_thrust ) / (vessel.specific_impulse * kerbin.surface_gravity)


# In[88]:

# Reverse Thrust Vector
# Takes a velocity vector, altitude, and vessel mass 
# Returns thrust acceleration as a vector in the opposite direction
def RTV(vvec, alt, mass):
    def axis(x):
        return ( Thrust(alt) * (vvec[x]/sum(vvec)) ) / mass
    return (-axis(0), -axis(1), -axis(2) )

