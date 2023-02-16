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
username = "vbremaud"
password = "Vincent1"
URL = "my.cmems-du.eu/thredds/dodsC/cmems_mod_glo_phy_my_0.083_P1M-m" #sans le http://
OUTPUT = "Climatology_oceano.nc"

### Input

Indice_MOIS = np.arange(0,12,1) #numéro du mois
Variable_obs = ["mlotst", "zos", "thetao"]

LATITUDE = slice(-90,90) #opposé à ERA5
LONGITUDE = slice(-180,180) #attention différent de ERA5

DEPTH = 0 #if data product

#mlotst, zos, thetao

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']


#t2m, u10, v10, sst, sp, tp

### Traitement

X_DS = (
    xr.open_dataset("https://"+username+":"+password+"@"+URL))
print(X_DS)

VAR_DATA = []
VAR_UNITS = []

for i in range(len(Variable_obs)): #à modifier
    VAR_DATA_TIME=[]
    for t in Indice_MOIS :
        X = X_DS[Variable_obs[i]].sel(longitude=LONGITUDE, latitude=LATITUDE)
        print(np.shape(X))

        I = np.arange(t,len(X[:,0,0]),12)  #modulo 12 car 12 mois dans l'année
        print('ok')
        print(I)
        unit = X.units
        lats = X.coords['latitude']
        lons = X.coords['longitude']
        print('ok2')
        X_mois=np.empty([len(I),len(X[0,:,0]),len(X[0,0,:])])
        for j in range(len(I)) :
            print('ok')
            k=I[j]
            X_mois[j,:,:] = X[k,:,:]
        print(np.shape(X_mois))

        X_mean = np.mean(X_mois,axis=0)
        VAR_DATA_TIME.append(X_mean)
    print(i)
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

mlotst = ds.createVariable('mlotst', 'f4', ('time', 'latitude', 'longitude',))
zos = ds.createVariable('zos', 'f4', ('time', 'latitude', 'longitude',))
thetao = ds.createVariable('thetao', 'f4', ('time', 'latitude', 'longitude',))


times[:]=np.array(Indice_MOIS)+1
lats1[:]=lats
lons1[:]=lons

#add netcdf attributes
mlotst.units = VAR_UNITS[0]
zos.units = VAR_UNITS[1]
thetao.units = VAR_UNITS[2]

for i in range(len(Indice_MOIS)):
    mlotst[i,:,:]=np.array(VAR_DATA[0][i])
    zos[i,:,:]=np.array(VAR_DATA[1][i])
    thetao[i,:,:]=np.array(VAR_DATA[2][i])


ds.close();
