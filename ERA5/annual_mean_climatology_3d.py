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

X_mean = np.mean(X,axis=0)

lats = X.coords['latitude']
depths = X.coords['depth']
unit = X.units

### Affichage

ax = plt.axes()
titlestr='Moyenne annuelle climatique 1959 - 2022  à 180°E '+Variable_obs

plt.contourf(lats, depths, X_mean,levels=100,cmap='viridis')
plt.colorbar(label=Variable_obs+' '+unit)
ax.invert_yaxis()
plt.title(titlestr,pad=20)
plt.xlabel("latitude [°]")
plt.ylabel("profondeur [m]")
plt.contour(lats, depths, X_mean,np.array([20])) #uniquement pour thetao

plt.show()