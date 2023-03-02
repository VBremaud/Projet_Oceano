"""
Affiche l'anomalie d'un mois d'une année donnée par rapport à la climatologie. Exemple : voir anomalie de SSH décembre 1997, El Nino.
"""

import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs


###OPEN FILE
FILE = "../Climatology_oceano.nc" #DATASET NETCDF
FILE2 = "global-reanalysis-phy-001-031-grepv2-daily_1677620973812.nc"

### Input

Indice_MOIS = '12' #numéro du mois 1 pour janvier etc
Variable_obs = "zos"

LATITUDE = slice(-5,5)
LONGITUDE = slice(-180,180)
ANNEE = '1998'

TIME = ANNEE+'-'+Indice_MOIS+'-16'
MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

#zos_oras

### Traitement
X_DS =  xr.open_dataset(FILE)
X_DS2 = xr.open_dataset(FILE2)

print(X_DS)
print(X_DS[Variable_obs].coords)
print(X_DS2)

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE).sel(time=float(Indice_MOIS))

X2 = X_DS2["zos_oras"].sel(longitude=LONGITUDE,latitude=LATITUDE).sel(time=TIME,method="ffill")

print(X)
print(X2)
print(X2.shape)
print(X.shape)

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units


### Affichage

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr = 'Anomalie de ' +Variable_obs + ' '+MOIS[int(Indice_MOIS)-1]+' '+ ANNEE

plt.pcolormesh(lons, lats, X2-X,  transform=ccrs.PlateCarree(),cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()