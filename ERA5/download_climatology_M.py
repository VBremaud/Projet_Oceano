"""
Télécharge dans un fichier download.nc les données Mensuels de variable physique sur la bande équatoriale de 1959 à 2022
"""

import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels-monthly-means',
    {
        'format': 'netcdf',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
            'convective_precipitation', 'mean_sea_level_pressure', 'mean_surface_net_long_wave_radiation_flux',
            'sea_surface_temperature', 'surface_pressure', 'total_precipitation','mean_surface_latent_heat_flux', 'mean_surface_net_long_wave_radiation_flux_clear_sky', 'mean_surface_sensible_heat_flux',
        ],
        'year': [
            '1959', '1960', '1961',
            '1962', '1963', '1964',
            '1965', '1966', '1967',
            '1968', '1969', '1970',
            '1971', '1972', '1973',
            '1974', '1975', '1976',
            '1977', '1978', '1979',
            '1980', '1981', '1982',
            '1983', '1984', '1985',
            '1986', '1987', '1988',
            '1989', '1990', '1991',
            '1992', '1993', '1994',
            '1995', '1996', '1997',
            '1998', '1999', '2000',
            '2001', '2002', '2003',
            '2004', '2005', '2006',
            '2007', '2008', '2009',
            '2010', '2011', '2012',
            '2013', '2014', '2015',
            '2016', '2017', '2018',
            '2019', '2020', '2021',
            '2022',
        ],
        'product_type': 'monthly_averaged_reanalysis',
        'time': '00:00',
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'area': [
            30, -180, -30,
            180,
        ],
    },
    'download.nc')