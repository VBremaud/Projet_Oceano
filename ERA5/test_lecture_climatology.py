import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs


###OPEN FILE
FILE = "../Climatology_ERA5.nc" #DATASET NETCDF

### Input

Indice_MOIS = np.arange(0.,12.,1) #numéro du mois 1 pour janvier etc
Variable_obs = "sst"

LATITUDE = slice(50,-50)
LONGITUDE = slice(120,200)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

#t2m, u10, v10, sst, sp, tp

### Traitement
X_DS =  xr.open_dataset(FILE)

print(X_DS)
print(X_DS[Variable_obs].coords)

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE)

X_mean = np.mean(X,axis=0)

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units


### Affichage

ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

"titlestr = Variable_obs + ' '+ MOIS[int(Indice_MOIS)-1] + ' '+'1959 - 2022'"
titlestr='test'
Y = (X[5]+X[6]+X[7])/3-(X[0]+X[1]+X[11])/3
print(X[8])

plt.pcolormesh(lons, lats, Y, transform=ccrs.PlateCarree(),cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()