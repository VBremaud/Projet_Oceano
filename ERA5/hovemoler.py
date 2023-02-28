"""
Affiche l'anomalie d'un mois d'une année donnée par rapport à la climatologie. Exemple : voir anomalie de SST décembre 1997, El Nino.
"""

import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs


###OPEN FILE
FILE = "../Climatology_ERA5.nc" #DATASET NETCDF
FILE2 = "download.nc"

### Input

#numéro du mois 1 pour janvier etc
Variable_obs = "sst"

LATITUDE = slice(4.95,5.05)
LONGITUDE = slice(-180,180)
ANNEE = '1997'

TIME = ANNEE
MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

#t2m, u10, v10, sst, sp, tp

### Traitement
X_DS =  xr.open_dataset(FILE)
X_DS2 = xr.open_dataset(FILE2)

print(X_DS)
print(X_DS[Variable_obs].coords)
print(X_DS2)

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE).isel(longitude=LONGITUDE)

X2 = X_DS2[Variable_obs].sel(expver=1,longitude=LONGITUDE,latitude=LATITUDE).sel(time=ANNEE,method="ffill")

print(X2.shape)

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units


### Affichage

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr = 'Anomalie de ' +Variable_obs + ' '+MOIS[int(Indice_MOIS)-1]+' '+ ANNEE

plt.pcolormesh(lons, lats, X2[int(Indice_MOIS)-1]-X,  transform=ccrs.PlateCarree(),cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()