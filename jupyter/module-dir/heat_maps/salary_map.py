from heat_maps.density_map import print_province_heat_map, fill_geo_info
import pandas as pd
import numpy as np

lat_column_name = 'lat'
lon_column_name = 'lon'
numerical_column_name = 'no'
province_column_name = 'province'
province_id_column_name = 'province_id'
city_column_name = 'city'
id_column_name = 'id'
country_code_column_name = 'country_code'

def get_province_ids():
    return pd.read_csv('woj_oznaczenia.csv', engine='python')

def get_city_data(data, address_column_name):
    unique_places = data.groupby(address_column_name)[id_column_name].nunique()
    
    places = pd.DataFrame({city_column_name:unique_places.index})
    places[lat_column_name]=np.nan
    places[lon_column_name]=np.nan
    places[province_column_name]=np.nan
    
    return places

def show_map(df):
    places_map = get_city_data(df, city_column_name)
    places_map = fill_geo_info(places_map, city_column_name, fill_province=True)

    # jjit_data = jjit_data.drop([lat_column_name, lon_column_name, province_column_name])
    jjit_data = pd.merge(df, places_map, how='outer', 
                        left_on=city_column_name, right_on=city_column_name)
    province_ids = get_province_ids()

    #group by province and aggregate min salary
    min_salary_per_province_data = jjit_data.groupby(by=province_column_name) \
        .agg({'salary_from':'mean'}) \
        .rename(columns={'salary_from':'mean_salary_from'}) \
        .reset_index()

    #merge with province GUGiK data (we need province id)
    province_data = pd.merge(min_salary_per_province_data, province_ids, how='outer',
                            left_on=province_column_name, right_on=province_column_name)

    print_province_heat_map(province_data = province_data,
                            heat_column_name="mean_salary_from",
                            file_path="min.html",
                            legend_name="Średnie minimalne wynagrodzenia")

                            #group by province and aggregate max salary
    max_salary_per_province_data = jjit_data.groupby(province_column_name) \
        .agg({'salary_to':'mean'}) \
        .rename(columns={'salary_to':'mean_salary_to'}) \
        .reset_index()

    #merge with province GUGiK data (we need province id)
    province_data = pd.merge(max_salary_per_province_data, province_ids, how='outer',
                            left_on=province_column_name, right_on=province_column_name)

    print_province_heat_map(province_data = province_data,
                            heat_column_name="mean_salary_to",
                            file_path="maks.html",
                            legend_name="Średnie maksymalne wynagrodzenia")