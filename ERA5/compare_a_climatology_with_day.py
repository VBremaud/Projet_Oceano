"""
Affiche l'anomalie d'une journée donnée par rapport à la climatologie. À partir d'un fichier netcdf.
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
FILE2 = "download_2006.nc"

### Input

Indice_MOIS = '7' #numéro du mois 1 pour janvier etc
Variable_obs = "tp"

LATITUDE = slice(90,-90) #50 / -50
LONGITUDE = slice(0,360) #120 / 200


MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

#t2m, u10, v10, sst, sp, tp

### Traitement
X_DS =  xr.open_dataset(FILE)
X_DS2 = xr.open_dataset(FILE2)

print(X_DS)
print(X_DS[Variable_obs].coords)
print(X_DS2)

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE).sel(time=float(Indice_MOIS))

X2 = X_DS2[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE)

print(X2.shape)

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

print(X2.units)

### Affichage

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr = 'Anomalie de ' +Variable_obs + ' '+MOIS[int(Indice_MOIS)-1]+' '+ '2006'

print(X/30)
print('ok')
print(np.mean(X2,axis=0))
plt.pcolormesh(lons, lats, np.mean(X2,axis=0)-X/30,  transform=ccrs.PlateCarree(),cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()