"à modifier et commenter"

import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs

#print(ds.info())

### Input

Indice_MOIS = '0' #numéro du mois
FILE = "download.nc" #DATASET NETCDF
Variable_obs = "sst"


#t2m, u10, v10, sst, sp, tp

### Traitement
X_DS =  xr.open_dataset(FILE)
print(X_DS)

print(X_DS[Variable_obs].sel(expver=1).coords)

LATITUDE = slice(23,-23)
LONGITUDE = slice(0,360)
print(LATITUDE,LONGITUDE)
X = X_DS[Variable_obs].sel(expver=1, longitude=LONGITUDE, latitude=LATITUDE) #expver=1 reanalyse ERA5
print(np.shape(X))

Indice_MOIS = int(Indice_MOIS)
I = np.arange(Indice_MOIS,len(X[:,0,0]),12)  #modulo 12 car 12 mois dans l'année

unit = X.units
lats = X.coords['latitude']
lons = X.coords['longitude']

X_mois =np.array([X[i,:,:] for i in I])

I2 = np.arange(7,len(X[:,0,0]),12)
X_mois2 =[X[i,:,:] for i in I2]

print(np.shape(X_mois))

#X_mean = np.mean(X_mois,axis=0)
#Test = (X_mois-np.mean(X,axis=0))**2

M = np.mean(X,axis=0)
print(np.shape(M))
X_mois12 =[np.array(X[i,:,:])-M for i in I]
X_mois21 =[np.array(X[i,:,:])-M for i in I2]
print(X_mois12)
X_mean = np.sqrt(np.mean((np.array(X_mois12)**2+np.array(X_mois21)**2),axis=0)/2)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

### Affichage

ax = plt.axes(projection=ccrs.Robinson())

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr = Variable_obs + ' '+ MOIS[Indice_MOIS-1] + ' '+'1959 - 2022'
plt.pcolormesh(lons, lats, X_mean, transform=ccrs.PlateCarree(),cmap='RdBu_r',vmax=3)
plt.colorbar(location='bottom',label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()
