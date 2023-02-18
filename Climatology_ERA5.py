"""
Calcule la moyenne climatologique pour chaque mois des variables ERA5 contenu dans le fichier download.nc. Renvoi un fichier netcdf contenant les moyennes climatiques pour chaque mois de l'année.
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
FILE = "ERA5/download.nc" #DATASET NETCDF
OUTPUT = "Climatology_ERA5.nc"

### Input

Indice_MOIS = np.arange(0,12,1) #numéro du mois
Variable_obs = ["t2m", "u10", "v10", "sst", "sp", "tp", "msl", "cp", "msnlwrf","mslhf","msnlwrfcs","msshf"]

LATITUDE = slice(90,-90)
LONGITUDE = slice(-180,180)

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']


#t2m, u10, v10, sst, sp, tp, msl, cp, msnlwrf, mslhf, msnlwrfcs, msshf

### Traitement

X_DS =  xr.open_dataset(FILE)
print(X_DS)

VAR_DATA = []
VAR_UNITS = []

for i in range(len(Variable_obs)):
    VAR_DATA_TIME=[]
    for t in Indice_MOIS :
        X = X_DS[Variable_obs[i]].sel(expver=1, longitude=LONGITUDE, latitude=LATITUDE) #expver=1 reanalyse ERA5
        #print(np.shape(X))

        I = np.arange(t,len(X[:,0,0]),12)  #modulo 12 car 12 mois dans l'année

        unit = X.units
        lats = X.coords['latitude']
        lons = X.coords['longitude']
        X_mois =[X.data[i,:,:] for i in I]

        X_mean = np.nanmean(X_mois,axis=0)
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
msl = ds.createVariable('msl', 'f4', ('time', 'latitude', 'longitude',))
cp = ds.createVariable('cp', 'f4', ('time', 'latitude', 'longitude',))
msnlwrf = ds.createVariable('msnlwrf', 'f4', ('time', 'latitude', 'longitude',))
mslhf = ds.createVariable('mslhf', 'f4', ('time', 'latitude', 'longitude',))
msnlwrfcs = ds.createVariable('msnlwrfcs', 'f4', ('time', 'latitude', 'longitude',))
msshf = ds.createVariable('msshf', 'f4', ('time', 'latitude', 'longitude',))

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
msl.units = VAR_UNITS[6]
cp.units = VAR_UNITS[7]
msnlwrf.units = VAR_UNITS[8]
mslhf.units = VAR_UNITS[9]
msnlwrfcs.units = VAR_UNITS[10]
msshf.units = VAR_UNITS[11]

for i in range(len(Indice_MOIS)):
    t2m[i,:,:]=np.array(VAR_DATA[0][i])
    u10[i,:,:]=np.array(VAR_DATA[1][i])
    v10[i,:,:]=np.array(VAR_DATA[2][i])
    sst[i,:,:]=np.array(VAR_DATA[3][i])
    sp[i,:,:]=np.array(VAR_DATA[4][i])
    tp[i,:,:]=np.array(VAR_DATA[5][i])
    msl[i,:,:]=np.array(VAR_DATA[6][i])
    cp[i,:,:]=np.array(VAR_DATA[7][i])
    msnlwrf[i,:,:]=np.array(VAR_DATA[8][i])
    mslhf[i,:,:]=np.array(VAR_DATA[9][i])
    msnlwrfcs[i,:,:]=np.array(VAR_DATA[10][i])
    msshf[i,:,:]=np.array(VAR_DATA[11][i])

ds.close();

