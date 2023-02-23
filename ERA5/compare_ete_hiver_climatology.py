"""
Affiche la moyenne climatique d'une variable sur l'été et l'hiver à partir de la climatologie mensuelle.
"""



import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs


###OPEN FILE
FILE = "../Climatology_ERA5.nc" #DATASET NETCDF #attention au nom du fichier

### Input

Variable_obs = "sst"

LATITUDE = slice(30,-30) #be careful à la latitude opposé ERA5
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

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE)

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

### Affichage

plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr='Moyenne annuelle climatique hiver DJV 1959 - 2022 '+Variable_obs

plt.pcolormesh(lons, lats, (X[11]+X[0]+X[1])/3, transform=ccrs.PlateCarree(),cmap='viridis')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr='Moyenne annuelle climatique été JJA 1959 - 2022 '+Variable_obs

plt.pcolormesh(lons, lats, (X[5]+X[6]+X[7])/3, transform=ccrs.PlateCarree(),cmap='viridis')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()