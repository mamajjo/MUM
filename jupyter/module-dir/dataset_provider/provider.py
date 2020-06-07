from pandas import read_csv, json_normalize, read_json
import json
import numpy as np
import urllib.request 
import requests

def get_jobs_info(api_url = 'https://justjoin.it/api/offers'):
    headers = {'Content-Type': 'application/json'}
    response = requests.get(api_url, headers=headers)
    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def map_columns_to_csv(dataset, cfg):
    skill_map = read_csv('/home/jovyan/host-note/data/deduplicated_skills-edit.csv', sep=":")
    unique_skill_columns = (skill_map['Skill'])

    for skill in unique_skill_columns:
        dataset[str(skill)] = 0
    result_df = dataset
    for index, row in dataset.iterrows():
        skill_dict = row['skills']
        for skill_level_tuple in skill_dict:
            name = skill_level_tuple['name']
            mapped_val = np.where(skill_map['Skill'] == name)
            if len(mapped_val) is 0 or len(mapped_val[0]) is 0:
                # TEMPORARY HACK
                print(f"Could not find '{name}' in map")
                continue
            name_index_in_map = mapped_val[0][0]
            name = skill_map.iloc[name_index_in_map]['Skill']
            if not name == '-':
                if row[name] == 0:
                    row[name] = skill_level_tuple['level']
                elif not row[name] == 0:
                    row[name] = row[name] if row[name] >= skill_level_tuple['level'] else skill_level_tuple['level']
        result_df.loc[index] = row
    result_df.to_csv(cfg.dataSourceMapped)

def find_exchange_rate(code, table):
    return next(filter(lambda c: c["code"]==code, table[0]["rates"]))["mid"]

def take_only_country_translate_currency(df):
    curr_table = None
    uniq_countries = df['country_code'].nunique()
    uniq_currencies = df['salary_currency'].nunique()
    if uniq_countries != 1 or uniq_currencies != 1:
        print(f"Found {uniq_countries} countries and {uniq_currencies} currencies!")
        print(f"Dropping foreign countries and translating currencies...")
        df = df.loc[df["country_code"] == "PL"]
        if not curr_table:
            with urllib.request.urlopen("https://api.nbp.pl/api/exchangerates/tables/a/?format=json") as url:
                curr_table = json.loads(url.read().decode())
        to_translate = df.loc[df["salary_currency"] != "pln"]
        for curr in to_translate.salary_currency.unique():
            ex_rate = find_exchange_rate(curr.upper(), curr_table)
            df.loc[df["salary_currency"] == curr] = df.loc[df["salary_currency"] == curr].apply(lambda x: x*ex_rate if x.name in ["salary_from", "salary_to"] else ("pln" if x.name == "salary_currency" else x))
        print(f"Unique countries: {df['country_code'].nunique()}, currencies: {df['salary_currency'].nunique()}, observations: {df.shape[0]}")
    return df
    
def read_dataset(cfg):
    if cfg.useOnlineData:
        print("Taking data from online source...")
        jjit_json = get_jobs_info()
        dataset = json_normalize(jjit_json)
        map_columns_to_csv(dataset)
        return read_csv(cfg.dataSourceMapped)
    else:
        print("Taking data from local file...")
        return read_csv(cfg.dataSourceRaw)

def preprocess_data(df, cfg):
    df = df.drop(columns=["street", "address_text", "company_url", "company_logo_url"])
    # Save no-salary observations to separate dataframe: "salaryless_df"
    salaryless_df = df.loc[((df.salary_currency.isnull()) | (df.salary_from.isnull()))]
    df = df.loc[((df.salary_currency.notnull()) & (df.salary_from.notnull()))]
    print(f"Found {salaryless_df.shape[0]} job ads without salary range or currency")
    if cfg.should_describe_data:
        print(df.shape)
        print(df[["salary_from", "salary_to"]].describe())
    df = take_only_country_translate_currency(df)
    return df
    
def get_dataset(cfg):
    return preprocess_data(read_dataset(cfg), cfg)

def get_raw_dataset(cfg):
    print("GetRawDataset - Started")
    dataset = read_json("/home/jovyan/host-note/data/joinit_data.json")
    print("GetRawDataset - read_json - DONE")
    map_columns_to_csv(dataset, cfg)
    print("GetRawDataset - map_columns_to_csv - DONE")
    dataset = read_csv(cfg.dataSourceMapped)
    print("GetRawDataset - read_csv - DONE")
    return preprocess_data(dataset, cfg)

