"""
Affiche la moyenne climatique d'une variable 3d oécano sur une année à partir de la climatologie mensuelle.
"""


import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs


###OPEN FILE
FILE = "../Climatology_oceano_3d.nc" #DATASET NETCDF #attention au nom du fichier

### Input

Variable_obs = "thetao"

LATITUDE = slice(-30,30) #be careful à la latitude opposé ERA5
DEPTH = slice(0,1000) #profondeur en mètre (on peut aller jusqu'au fond)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

#uo, vo, thetao,

### Traitement
X_DS =  xr.open_dataset(FILE)

print(X_DS)
print(X_DS[Variable_obs].coords)

X = X_DS[Variable_obs].sel(depth=DEPTH,latitude=LATITUDE)
V0 = X_DS["vo"].sel(depth=DEPTH,latitude=LATITUDE)

V0_mean = np.mean(V0,axis=0)
X_mean = np.mean(X,axis=0)

lats = X.coords['latitude']
depths = X.coords['depth']
unit = X.units

I = np.arange(0,len(depths),2)
J = np.arange(0,len(lats),10)
J=J[1:-1]
DEPTHS = [depths.data[i] for i in I]
LATS = [lats.data[j] for j in J]
print(DEPTHS)
print(LATS)
print(len(DEPTHS))
print(len(LATS))
W0_M = np.zeros([len(LATS),len(DEPTHS)])
V0_M = np.empty([len(LATS),len(DEPTHS)])
print(V0_mean.shape)
for j in range(len(J)):
    for i in range(len(I)):
        print(J[j],I[i])
        V0_M[i,j]=V0_mean.data[I[i],J[j]]

GRADV = np.gradient(V0_M,axis=1)


### Affichage

ax = plt.axes()
titlestr='Moyenne annuelle climatique 1959 - 2022  à 180°E '+Variable_obs


plt.contourf(lats, depths, X_mean,levels=500,cmap='turbo')
plt.colorbar(label=Variable_obs+' '+unit)
ax.invert_yaxis()
plt.title(titlestr,pad=20)
plt.xlabel("latitude [°]")
plt.ylabel("profondeur [m]")
plt.contour(lats, depths, X_mean,np.array([20])) #uniquement pour thetao
CS = plt.contour(lats, depths, V0_mean)
ax.clabel(CS, CS.levels, inline=True, fontsize=10)
#plt.quiver(np.array(LATS),np.array(DEPTHS),V0_M,W0_M)
"""
vmax=max(np.max(GRADV),-np.min(GRADV))
vmin=-vmax
plt.contourf(LATS, DEPTHS, GRADV,vmin=vmin,vmax=vmax,levels=500,cmap='RdBu_r')
plt.colorbar(label="GRADV")
CS = plt.contour(lats, depths, V0_mean)
ax.clabel(CS, CS.levels, inline=True, fontsize=10)
ax.invert_yaxis()
plt.title(titlestr,pad=20)
plt.xlabel("latitude [°]")
plt.ylabel("profondeur [m]")
"""
plt.show()


plt.show()