"""
Affiche la moyenne climatique d'une variable sur une année à partir de la climatologie mensuelle.
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

Variable_obs = "tp"

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
U0 = X_DS["u10"].sel(longitude=LONGITUDE,latitude=LATITUDE)
V0 = X_DS["v10"].sel(longitude=LONGITUDE,latitude=LATITUDE)

X_mean = np.mean(X,axis=0)
U0_mean = np.mean(U0,axis=0)
V0_mean = np.mean(V0,axis=0)
print(np.shape(X_mean),np.shape(U0_mean),np.shape(V0_mean))

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

I = np.arange(0,len(lons),20)
J = np.arange(0,len(lats),20)
LONS = [lons.data[i] for i in I]
LATS = [lats.data[j] for j in J]
U0_M = np.empty([len(LATS),len(LONS)])
V0_M = np.empty([len(LATS),len(LONS)])

for j in range(len(J)):
    for i in range(len(I)):
        U0_M[j,i]=U0_mean.data[J[j],I[i]]
        V0_M[j,i]=V0_mean.data[J[j],I[i]]

### Affichage

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr='Moyenne annuelle climatique 1959 - 2022 '+Variable_obs

plt.pcolormesh(lons, lats, X_mean,vmax=0.015, transform=ccrs.PlateCarree(),cmap='Blues')
plt.colorbar(label=Variable_obs+' '+unit)
print(np.shape(U0_M),np.shape(V0_M),len(LONS),len(LATS))
plt.quiver(np.array(LONS),np.array(LATS),U0_M,V0_M,scale=500,headlength=7,headwidth=5,width=0.001,transform=ccrs.PlateCarree())
plt.title(titlestr,pad=20)


plt.show()