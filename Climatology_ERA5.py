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
FILE = "ERA5/download.nc" #DATASET NETCDF
OUTPUT = "Climatology_ERA5.nc"

### Input

Indice_MOIS = np.arange(0,12,1) #numéro du mois
Variable_obs = ["t2m", "u10", "v10", "sst", "sp", "tp"]

LATITUDE = slice(90,-90)
LONGITUDE = slice(0,360)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']


#t2m, u10, v10, sst, sp, tp

### Traitement

X_DS =  xr.open_dataset(FILE)
print(X_DS)

VAR_DATA = []
VAR_UNITS = []

for i in range(len(Variable_obs)): #à modifier
    VAR_DATA_TIME=[]
    for t in Indice_MOIS :
        X = X_DS[Variable_obs[i]].sel(expver=1, longitude=LONGITUDE, latitude=LATITUDE) #expver=1 reanalyse ERA5
        #print(np.shape(X))

        I = np.arange(t,len(X[:,0,0]),12)  #modulo 12 car 12 mois dans l'année

        unit = X.units
        lats = X.coords['latitude']
        lons = X.coords['longitude']

        X_mois =[X[i,:,:] for i in I]
        print(np.shape(X_mois))

        X_mean = np.mean(X_mois,axis=0)
        if i==0:
            print(X_mean)
        VAR_DATA_TIME.append(X_mean)

    VAR_UNITS.append(unit)
    VAR_DATA.append(VAR_DATA_TIME)


ds = Dataset(OUTPUT, mode="w")

ds.set_fill_off()

time = ds.createDimension('time', len(MOIS))
longitude = ds.createDimension('longitude', len(lons))
latitude = ds.createDimension('latitude', len(lats))

times = ds.createVariable('time', 'f4', ('time',))
lons1 = ds.createVariable('longitude', 'f4', ('longitude',))
lats1 = ds.createVariable('latitude', 'f4', ('latitude',))

t2m = ds.createVariable('t2m', 'f4', ('time', 'latitude', 'longitude',))
u10 = ds.createVariable('u10', 'f4', ('time', 'latitude', 'longitude',))
v10 = ds.createVariable('v10', 'f4', ('time', 'latitude', 'longitude',))
sst = ds.createVariable('sst', 'f4', ('time', 'latitude', 'longitude',))
sp = ds.createVariable('sp', 'f4', ('time', 'latitude', 'longitude',))
tp = ds.createVariable('tp', 'f4', ('time', 'latitude', 'longitude',))

times[:]=np.array(Indice_MOIS)+1
lats1[:]=lats
lons1[:]=lons

#add netcdf attributes
t2m.units = VAR_UNITS[0]
u10.units = VAR_UNITS[1]
v10.units = VAR_UNITS[2]
sst.units = VAR_UNITS[3]
sp.units = VAR_UNITS[4]
tp.units = VAR_UNITS[5]

for i in range(len(Indice_MOIS)):
    t2m[i,:,:]=np.array(VAR_DATA[0][i])
    u10[i,:,:]=np.array(VAR_DATA[1][i])
    v10[i,:,:]=np.array(VAR_DATA[2][i])
    sst[i,:,:]=np.array(VAR_DATA[3][i])
    sp[i,:,:]=np.array(VAR_DATA[4][i])
    tp[i,:,:]=np.array(VAR_DATA[5][i])

ds.close();

"""
### Affichage

ax = plt.axes(projection=ccrs.PlateCarree())

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr = Variable_obs + ' '+ MOIS[Indice_MOIS-1] + ' '+'1959 - 2022'
plt.pcolormesh(lons, lats, X_mean, transform=ccrs.PlateCarree(),cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()
"""
