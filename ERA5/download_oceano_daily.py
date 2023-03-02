"""
Récupère des données mensuelles d'océano.
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
username = "vbremaud"
password = "Vincent1"
URL = "my.cmems-du.eu/thredds/dodsC/global-reanalysis-phy-001-031-grepv2-monthly" #sans le http://
OUTPUT = "oceano_monthly.nc"

### Input


LATITUDE = slice(-15,15) #opposé à ERA5
LONGITUDE = slice(-180,180)

ANNEE = np.arange(1994,2010,1)
# zos,


### Traitement

print('ok')
X_DS = (
    xr.open_dataset("https://"+username+":"+password+"@"+URL))
print(X_DS)

VAR_DATA = []
VAR_TIME=[]

for i in range(len(ANNEE)):
    X = X_DS['zos_oras'].sel(longitude=LONGITUDE, latitude=LATITUDE).sel(time=str(ANNEE[i]),method="ffill")
    #expver=1 reanalyse ERA5
    print(X)

    unit = X.units
    times = X.coords['time']

    lats = X.coords['latitude']
    lons = X.coords['longitude']
    Xdata = X.data
    VAR_TIME.append(list(np.arange(1+i*12,13+i*12,1)))
    VAR_DATA.append(Xdata)

ds = Dataset(OUTPUT, mode="w")

ds.set_fill_off()

time = ds.createDimension('time', 12*len(ANNEE))
longitude = ds.createDimension('longitude', len(lons))
latitude = ds.createDimension('latitude', len(lats))

times1 = ds.createVariable('time', 'f4', ('time',))
lons1 = ds.createVariable('longitude', 'f4', ('longitude',))
lats1 = ds.createVariable('latitude', 'f4', ('latitude',))

zos = ds.createVariable('zos', 'f4', ('time', 'latitude', 'longitude',))


lats1[:]=lats
lons1[:]=lons

#add netcdf attributes

zos.units = unit

for i in range(len(ANNEE)):
    times1[i*12:(i+1)*12]=np.array(VAR_TIME[i])
    zos[i*12:(i+1)*12,:,:] = np.array(VAR_DATA[i])

ds.close();