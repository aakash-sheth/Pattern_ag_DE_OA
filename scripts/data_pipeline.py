import pandas as pd
import shapely.wkt
import numpy as np

from utility_functions import load_data, get_fips_code, cokey_weighted_avg


folder_path = input("Enter input data path: ") #'./inputs'
folder_output_path = input("Enter input data path: ")

data = load_data(folder_path)
# Crops Data

data['crop'] = data['crop'][data['crop']['year'] == 2021][[
    'field_id', 'field_geometry', 'crop_type']]

# # Generate crop output file
data['crop'].to_csv(folder_output_path+'\crop_output.csv')


# Spectral Data processing
data['spectral']['ndvi'] = (data['spectral']['nir'] - data['spectral']['red']) / \
    (data['spectral']['nir'] + data['spectral']['red'])
data['spectral'] = data['spectral'][data['spectral']['ndvi'] == data['spectral']['ndvi'].max()][[
    'tile_id', 'tile_geometry', 'ndvi', 'date']]

data['spectral'].rename(
    columns={'ndvi': 'pos', 'date': 'pos_date'}, inplace=True)

# Generate spectral output file
data['spectral'].to_csv(folder_output_path+'\spectral_output.csv')



## Soil Data Processing
data['soil']['hz_layer_weights'] = data['soil'].groupby(['cokey'])['hzdept','hzdepb'].\
apply(lambda x : cokey_weighted_avg(x['hzdept'],x['hzdepb']).to_frame('hz_layer_weights'))

weighted_average = lambda x: np.average(x, weights=data['soil'].loc[x.index, "hz_layer_weights"])


data['soil'] = data['soil'].merge(data['soil'].groupby(['mukey']).\
                                  aggregate({'comppct': weighted_average}).reset_index().\
                                  rename(columns = {'comppct':'weighted_average_across_mukey'}),\
                                  on = 'mukey', how = 'left')

data['soil']=data['soil'][['mukey', 'mukey_geometry', 'om', 'cec', 'ph', 'hz_layer_weights','weighted_average_across_mukey']]

# Generate soil output file
data['soil'].to_csv(folder_output_path+'\soil_output.csv')


# Wether data processing
data['weather'] = data['weather'][data['weather']['year'] == 2021]

df_weather_agg = data['weather'].groupby(
    ['fips_code']).agg({'precip': ['sum'], 'temp': ['min', 'max', 'mean']})

data['weather'] = df_weather_agg.droplevel(level=0, axis=1)

data['weather'].rename(columns={'sum': 'precip', 'min': 'min_temp',
                                'max': 'max_temp', 'mean': 'mean_temp'}, inplace=True)
data['weather'].reset_index(inplace=True)


# lets convert crop field_geomatry string to appropriate format
data['crop']['centroid'] = data['crop']['field_geometry'].apply(
    lambda x: shapely.wkt.loads(x))
data['crop']['fips_code'] = data['crop']['centroid'].apply(
    lambda pos: get_fips_code(pos.centroid.y, pos.centroid.x)).astype(int)

data['weather'] = data['weather'].merge(
    data['crop'], on='fips_code', how='left')
data['weather']=data['weather'][[ 'field_id', 'precip', 'min_temp','max_temp', 'mean_temp']]

# Generate crop output file
data['weather'].to_csv(folder_output_path+'\weather_output.csv',)
