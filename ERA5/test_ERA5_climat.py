import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs

#print(ds.info())

### Input

Indice_MOIS = '1' #numéro du mois
FILE = "download.nc" #DATASET NETCDF
Variable_obs = "t2m"
Unit="K"

#t2m, u10, v10, sst, sp, tp

### Traitement
X_DS =  xr.open_dataset(FILE)
print(X_DS)

print(X_DS[Variable_obs].sel(expver=1).coords)

X = X_DS[Variable_obs].sel(expver=1) #expver=1 reanalyse ERA5
#print(np.shape(X))

Indice_MOIS = int(Indice_MOIS)
I = np.arange(Indice_MOIS,len(X[:,0,0]),12)  #modulo 12 car 12 mois dans l'année

lats = X.coords['latitude']
lons = X.coords['longitude']

X_mois =[X[i,:,:] for i in I]
print(np.shape(X_mois))

X_mean = np.mean(X_mois,axis=0)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

### Affichage

ax = plt.axes(projection=ccrs.Robinson())

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr = Variable_obs + ' '+ MOIS[Indice_MOIS-1] + ' '+'1959 - 2022'
plt.pcolormesh(lons, lats, X_mean, transform=ccrs.PlateCarree(),cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+Unit)
plt.title(titlestr,pad=20)

plt.show()
