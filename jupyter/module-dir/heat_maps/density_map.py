import numpy as np
import pandas as pd
import webbrowser
import folium
from folium.plugins import HeatMap
import geopandas as gpd
from geopy import Nominatim
from IPython.display import display

lat_column_name = 'lat'
lon_column_name = 'lon'
numerical_column_name = 'no'
province_column_name = 'province'
province_id_column_name = 'province_id'
city_column_name = 'city'
id_column_name = 'id'
country_code_column_name = 'country_code'

def get_province_from_address (address_text, province_string = "województwo ",
                               split_sign=","):
    province = address_text.partition(province_string)[2] 
    province = province.partition(split_sign)[0] 
    
    return province
    
def fill_geo_info(places_data, loc_column_name, fill_province = False):
    locator = Nominatim(user_agent="myGeocoder")
    
    for i, row in places_data.iterrows():
        location = locator.geocode(row[loc_column_name])
        if location is not None:
            places_data.loc[i,lat_column_name] = location.latitude
            places_data.loc[i,lon_column_name] = location.longitude
            if fill_province:
                places_data.loc[i, province_column_name] = get_province_from_address(
                location.address)
        else:
            print(f"Could not find latitude/longitude for {row[loc_column_name]}")
            
    return places_data

def print_heat_map(places_data, file_path = 'heat_map.html', 
                   heat_column_name = numerical_column_name):

    places_len = len(places_data)
    
    lat = np.array(places_data[lat_column_name][0:places_len])
    lon = np.array(places_data[lon_column_name][0:places_len])
    no = np.array(places_data[heat_column_name][0:places_len],dtype=float)
    data = [[lat[i],lon[i],no[i]] for i in range(places_len)] 
    
    #location is the center location, draw a Map, and start zooming is 6 times.
    map_osm = folium.Map(location=[lat.mean(),lon.mean()],zoom_start=6,control_scale=True)
    HeatMap(data).add_to(map_osm) # Add heat map to the created map
    display(map_osm)
    map_osm.save(file_path) # Save as html file
    webbrowser.open(file_path) # Default browser open

def print_province_heat_map(province_data = None, heat_column_name = numerical_column_name,
                            province_key_column_name = province_id_column_name,
                            file_path = 'province_heat_map.html',
                            legend_name = None):    
    #preprocessing 
    province_data = province_data.dropna()
    province_data[province_id_column_name]=\
        province_data[province_id_column_name].astype(int)
    
    province_geo_paths = get_province_geo_paths()
    province_map = folium.Map([52, 19], zoom_start=6)
    folium.Choropleth(geo_data=province_geo_paths,
                  data=province_data,
                    # kolumna z kluczem, kolumna z wartościami
                  columns=[province_key_column_name, heat_column_name], 
                      # klucz z geoJSON
                  key_on='feature.properties.JPT_KOD_JE', 
                  fill_color='YlOrRd', 
                  fill_opacity=0.7,
                  line_opacity=0.2,
                  legend_name=legend_name).add_to(province_map)
    # zapisanie utworzonej mapy do pliku HTML
    display(province_map)
    province_map.save(outfile = file_path)
    webbrowser.open(file_path) # Default browser open
    
def get_province_geo_paths():
    province_shapes = gpd.read_file('wojewodztwa.shp')
    province_shapes = province_shapes[['JPT_KOD_JE', "geometry"]]
    province_shapes['JPT_KOD_JE']=province_shapes['JPT_KOD_JE'].astype(int)
    
    # uproszczenie geometrii (mniejsza wartosc = bardziej dokładnie)
    province_shapes.geometry = province_shapes.geometry.simplify(0.005)
    province_geo_path = province_shapes.to_json()
    return province_geo_path

def group_by_city(data, address_column_name):
    unique_places = data.groupby(address_column_name)[id_column_name].nunique()
    places = pd.DataFrame({city_column_name:unique_places.index,
                           numerical_column_name:unique_places.values})
    places[lat_column_name]=np.nan
    places[lon_column_name]=np.nan
    return places

def density_heat_map(df):
    # print heat map with offer count
    grouped_city_data = group_by_city(df, city_column_name)
    places_map = fill_geo_info(grouped_city_data, city_column_name)
    print_heat_map(places_map)