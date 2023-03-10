
import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
from scipy.interpolate import interp2d
import cartopy.crs as ccrs


###OPEN FILE
FILE = "Climatology_oceano_daily.nc" #DATASET NETCDF
FILE2 = "../Climatology_oceano.nc"

### Input

#numéro du mois 1 pour janvier etc
Variable_obs = "zos"

LATITUDE = slice(13.95,14.05)
LONGITUDE = slice(-180,180)
ANNEE = '1997'

TIME = ANNEE
MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

#t2m, u10, v10, sst, sp, tp

### Traitement
X_DS =  xr.open_dataset(FILE)
X_DS2 = xr.open_dataset(FILE2)

print(X_DS)
print(X_DS[Variable_obs].coords)
print(X_DS2)

X = X_DS[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE)

X2 = X_DS2[Variable_obs].sel(longitude=LONGITUDE,latitude=LATITUDE)

TEMPS = X2.coords['time']

TEMPS1 = TEMPS.data
TEMPS1[::-1] = TEMPS1

X2_DATA = X2.data
X2_DATA = np.squeeze(X2_DATA, axis=1)

X_DATA = X.data
X_DATA = np.squeeze(X_DATA, axis=1)

print(np.shape(X_DATA),np.shape(X2_DATA))

X_final = np.empty(np.shape(X_DATA))
for i in range(len(X_DATA)):
    X_final[i] = X_DATA[i] - X2_DATA[i%12]

lats = X.coords['latitude']
lons = X.coords['longitude']
unit = X.units

for i in range(len(lons.data)):
    if lons.data[i]>-110:
        I1 = i
        break

for i in range(len(lons.data)):
    if lons.data[i]>150:
        I2 = i
        break

LONS = np.linspace(150,360-110,I1+len(lons.data)-I2)
X_Final = np.empty((len(X_final[:,0]),len(LONS)))

print(len(LONS))
print(np.shape(X_Final))
print(len(lons.data)-I2)
for i in range(len(X_final[:,0])):
    X_Final[i,:len(lons.data)-I2]=X_final[i,I2:]
    X_Final[i,len(lons.data)-I2:]=X_final[i,:I1]


TEMPS = np.linspace(1994,2009,len(X_final[:,0]))

#I1 = np.index()

### Affichage

vmax=max(np.max(X_final),-np.min(X_final))
vmin=-vmax

titlestr = 'Hovmöller anomalie de SSH 14°'

plt.pcolormesh(LONS, TEMPS, X_Final, vmin=vmin,vmax=vmax,cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
#plt.gca().invert_yaxis()
plt.title(titlestr,pad=20)

plt.show()