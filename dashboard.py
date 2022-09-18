import pandas as pd
import numpy as np
import streamlit as st
import graph
import re

#%% VARIABLE
DATA_PATH = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
MAP_PATH = "https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv"

#%% Data Loading
df = pd.read_csv(DATA_PATH)
df_map = pd.read_csv(MAP_PATH, delimiter='"')

# map coordinate
df_map = df_map[['Alpha-3 code', 'Latitude (average)', 'Longitude (average)']]
df_map.columns = ['iso_code', 'lat', 'lon']



#%%
temp_ = df_map.to_dict('index')

latitude_ = {}
longitude_ = {}
for i in temp_:
    latitude_.update({temp_[i]['iso_code']: temp_[i]['lat']})
    longitude_.update({temp_[i]['iso_code']: temp_[i]['lon']})
    
df['lat'] = df.iso_code.map(latitude_).fillna(np.nan)
df['lon'] = df.iso_code.map(longitude_).fillna(np.nan)


#%% Data Segmentation

############################
# energy consumption (twh) #
############################
consumption = ['country', 'iso_code', 'year']

keyword = "consumption"
for col in df.columns:
    if re.search(keyword, col):
        consumption.append(col)
        
# remove
consumption.remove('fossil_fuel_consumption')
        
df_cons = df[consumption]

##############
# generation #
##############
generation = ['country', 'iso_code', 'year', 'electricity_generation']

df_gen = df[generation]

##########
# carbon #
##########
carb = ['country', 'iso_code', 'year', 'carbon_intensity_elec']

df_carb = df[carb]
#%% Streamlit

st.set_page_config(
    page_title = 'World Energy Consumption',
    page_icon = '✅',
    layout = 'wide'
)

main_title = "World Energy Consumption"
st.markdown(f"<h1 style='text-align: left; color: black;'>{main_title}</h1>", unsafe_allow_html=True)


# kpi 1 

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown("**Energy Consumption**")
    st.plotly_chart(graph.fig1(df_cons), use_container_width=True)

with kpi2:
    st.markdown("**World Electricity Generation**")
    st.plotly_chart(graph.fig2(df_gen), use_container_width=True)
    

with kpi3:
    st.markdown("**Carbon intensity of electricity production**")
    st.plotly_chart(graph.fig3(df_carb), use_container_width=True)


st.markdown("## Chart Layout")

options = st.multiselect(
    'Country',
    df.iso_code.unique(),
    ['AFG', 'ZMB', 'ARG'])

df_line = pd.DataFrame()

for i in options:
    temp_ = df[['year', 'population']][df.iso_code==i].set_index('year')
    df_line = pd.concat([df_line, temp_], axis=1)
    
df_line.columns = options

st.line_chart(df_line)



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    