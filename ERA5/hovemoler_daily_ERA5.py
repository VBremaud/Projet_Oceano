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
import pandas as pd


###OPEN FILE
FILE = "download_ERA5_daily.nc" #DATASET NETCDF
FILE2 = "../Climatology_ERA5.nc"

### Input

#numéro du mois 1 pour janvier etc
Variable_obs = "mtnlwrf"

LATITUDE = slice(8,-8)
LONGITUDE = slice(-180,180)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']
MOIS_BIS = ['-01-','-02-','-03-','-04-','-05-','-06-','-07-','-08-','-09-','-10-','-11-','-12-']

MOIS_CLIM = np.arange(1,12,1)
#t2m, u10, v10, sst, sp, tp

### Traitement
X_DS =  xr.open_dataset(FILE)
X_DS2 = xr.open_dataset(FILE2)

print(X_DS)
print(X_DS2)

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE)

X2 = X_DS2[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE)

print(X.shape)
print(X2.shape)
TEMPS = X2.coords['time']

TEMPS1 = TEMPS.data
TEMPS1[::-1] = TEMPS1

X2_DATA = X2.data
X2_DATA = np.nanmean(X2_DATA, axis=1)

X_DATA = X.data
X_DATA = np.nanmean(X_DATA, axis=1)

print(np.shape(X_DATA),np.shape(X2_DATA))

X_final = np.empty(np.shape(X_DATA))
for i in range(len(X_DATA)):
    X_final[i] = X_DATA[i] - X2_DATA[(i//(30))%12]

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

for i in range(len(lons.data)):
    if lons.data[i]>-90:
        I1 = i
        break

for i in range(len(lons.data)):
    if lons.data[i]>50:
        I2 = i
        break

LONS = np.linspace(50,360-90,I1+len(lons.data)-I2)
X_Final = np.empty((len(X_final[:,0]),len(LONS)))

for i in range(len(lons.data)):
    data = X_final[:,i]
    d = pd.Series(data)
    correct = d.rolling(15).mean()
    X_final[:,i] = correct

print(len(LONS))
print(np.shape(X_Final))
print(len(lons.data)-I2)
for i in range(len(X_final[:,0])):
    X_Final[i,:len(lons.data)-I2]=X_final[i,I2:]
    X_Final[i,len(lons.data)-I2:]=X_final[i,:I1]


#TEMPS = np.linspace(1997,2002,len(X_final[:,0]))
TEMPS = X.coords['time'].data

#I1 = np.index()

### Affichage
print(np.shape(X_Final))

vmax=max(np.nanmax(X_Final),-np.nanmin(X_Final))
vmin=-vmax
print(vmin)

titlestr = 'Hovmöller anomalie de OLR 5N-5S 15-day mean 2019-2022'

plt.contourf(LONS, TEMPS, X_Final,levels=20,vmin=vmin,vmax=vmax,cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
plt.gca().invert_yaxis()
plt.title(titlestr,pad=20)
plt.show()