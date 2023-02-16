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

Indice_MOIS = '0' #numéro du mois
Variable_obs = "t2m"

LATITUDE = slice(90,-90)
LONGITUDE = slice(0,360)

#t2m, u10, v10, sst, sp, tp

### Traitement
X_DS =  xr.open_dataset(FILE)
print(X_DS)

print(X_DS[Variable_obs].sel(expver=1).coords)

X = X_DS[Variable_obs].sel(expver=1, longitude=LONGITUDE, latitude=LATITUDE) #expver=1 reanalyse ERA5
#print(np.shape(X))

Indice_MOIS = int(Indice_MOIS)
I = np.arange(Indice_MOIS,len(X[:,0,0]),12)  #modulo 12 car 12 mois dans l'année

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

X_mois =[X[i,:,:] for i in I]
print(np.shape(X_mois))

X_mean = np.mean(X_mois,axis=0)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

### Affichage

ax = plt.axes(projection=ccrs.PlateCarree())

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

print(len(lats))
print(len(lons))
print(np.shape(X_mean))

titlestr = Variable_obs + ' '+ MOIS[Indice_MOIS] + ' '+'1959 - 2022'
plt.pcolormesh(lons, lats, X_mean, transform=ccrs.PlateCarree(),cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()