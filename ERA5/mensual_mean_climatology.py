"""
Affiche la climatologie d'une variable pour un mois donné.
"""

import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs

#print(ds.info())

###OPEN FILE
FILE = "../Climatology_ERA5.nc" #DATASET NETCDF


### Input

Indice_MOIS = '7' #numéro du mois 1 pour janvier
Variable_obs = "sst"

LATITUDE = slice(30,-30) #be careful à la latitude opposé ERA5 pour l'océan
LONGITUDE = slice(-180,180)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

#t2m, u10, v10, sst, sp, tp, msl, cp, msnlwrf, mslhf, msnlwrfcs, msshf
#mlotst, zos,

### Traitement
X_DS =  xr.open_dataset(FILE)

print(X_DS)
print(X_DS[Variable_obs].coords)

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE,time=float(Indice_MOIS))

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

### Affichage

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr='Moyenne climatique '+MOIS[int(Indice_MOIS)-1]+" 1959 - 2022 "+Variable_obs

plt.pcolormesh(lons, lats, X, transform=ccrs.PlateCarree(),cmap='viridis')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()


