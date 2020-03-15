from pathlib import Path
from pandas import read_json

class Config(object):
    def __init__(self, dataSourceUrl, test_size, n_splits, should_describe_data):
        self.dataSourceUrl = dataSourceUrl
        self.test_size = test_size
        self.n_splits = n_splits
        self.should_describe_data = should_describe_data
        self.n_data_columns = n_data_columns

def as_config(dict):
    dataSetName = dict['chosenDataSet'][0]
    print(dict[dataSetName])
    return Config(
        dict[dataSetName]['dataSourceUrl'],
        dict[dataSetName]['test_size'],
        dict[dataSetName]['n_splits'],
        dict[dataSetName]['should_describe_data'],
    )

# configuration = json.loads(Path("configuration.json").read_text(), object_hook = as_config)
configuration = read_json("./configuration.json")
json_config = as_config(configuration)