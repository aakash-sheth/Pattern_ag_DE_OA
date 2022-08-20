import os
import pandas as pd
import requests

def load_data(folder_path):
    data  = dict()
    for file in os.listdir(folder_path):
        if '.csv' in file:
            file_path = os.path.join(folder_path, file) 
            data[file.split('.')[0]] = pd.read_csv(file_path)
    return data

def get_fips_code(lat, long):
    url = 'https://geo.fcc.gov/api/census/block/find?latitude=%s&longitude=%s&format=json' % (
        lat, long)
    response = requests.get(url)
    data = response.json()
    state = data['State']['FIPS']
    county = data['County']['FIPS'][2:]
    fips_code = state+county
    return fips_code

def cokey_weighted_avg(hzdept,hzdepb):
    return abs(hzdept - hzdepb) / hzdepb

