"""
Affiche l'écart type interannuel d'une variable (moyenne sur les années puis écart type). ERA5 ONLY
"""

from netCDF4 import Dataset
import os
import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs

#print(ds.info())

###OPEN FILE
FILE = "download.nc" #DATASET NETCDF

### Input

Variable_obs = "sst" #ERA5 ONLY

LATITUDE = slice(30,-30)
LONGITUDE = slice(-180,180)


MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']


#t2m, u10, v10, sst, sp, tp, msl, cp, msnlwrf, mslhf, msnlwrfcs, msshf
#mlotst, zos,
#msnlwrf = mean_surface_net_long_wave_radiation_flux
#mslhf = mean_surface_latent_heat_flux
#msnlwrfcs = mean_surface_net_long_wave_radiation_flux_clear_sky
#msshf= mean_surface_sensible_heat_flux

### Traitement
X_DS =  xr.open_dataset(FILE)

print(X_DS)
print(X_DS[Variable_obs].coords)

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE).sel(expver=1)

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

N = int(len(X[:,0,0])/12)
X_annual = np.empty([N, len(lats),len(lons)])


for i in range(N):
    Y = X.data[N*i:N*(i+1),:,:]
    X_annual[i,:,:] = np.mean(X.data[N*i:N*(i+1),:,:],axis=0)

X_std = np.nanstd(X_annual,axis=0)

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

### Affichage

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr='Ecart type interannuel 1959 - 2022 '+Variable_obs

plt.pcolormesh(lons, lats, X_std, transform=ccrs.PlateCarree(),cmap='viridis')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()
