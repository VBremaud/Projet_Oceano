import xarray as xr
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import numpy as np
import cartopy.crs as ccrs


###OPEN FILE
username = "vbremaud"
password = "Vincent1"
URL = "my.cmems-du.eu/thredds/dodsC/global-reanalysis-phy-001-031-grepv2-mnstd-monthly" #sans le http://

### Input

Indice_MOIS = '0' #numéro du mois
Variable_obs = "thetao_mean"

LATITUDE = slice(-90,90) #opposé à ERA5
LONGITUDE = slice(-180,180) #attention différent de ERA5

DEPTH = 0 #if data product

MOIS = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Spetembre','Octobre','Novembre','Décembre']

#mlotst, zos, thetao, uo, vo

### Traitement

X_DS = (xr.open_dataset("https://"+username+":"+password+"@"+URL))
print(X_DS)


X = X_DS[Variable_obs].sel(latitude=LATITUDE, longitude=LONGITUDE).isel(depth=DEPTH)

Indice_MOIS = int(Indice_MOIS)
I = np.arange(Indice_MOIS,len(X[:,0,0]),12)  #modulo 12 car 12 mois dans l'année

unit = X.units
lats = X.coords['latitude']
lons = X.coords['longitude']

X_mois =[X[i,:,:] for i in I]
print(np.shape(X_mois))

X_mean = np.mean(X_mois,axis=0)


### Affichage

ax = plt.axes(projection=ccrs.PlateCarree())

ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

titlestr = Variable_obs + ' '+ MOIS[Indice_MOIS] + ' '+'1993 - 2020'
plt.pcolormesh(lons, lats, X_mean, transform=ccrs.PlateCarree(),cmap='RdBu_r')
plt.colorbar(label=Variable_obs+' '+unit)
plt.title(titlestr,pad=20)

plt.show()

