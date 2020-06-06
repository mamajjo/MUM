import json

class Config(object):
    def __init__(self, dataSourceRaw, dataSourceMapped, useOnlineData, test_size, n_splits, should_describe_data, n_components_pca):
        self.dataSourceRaw = dataSourceRaw
        self.dataSourceMapped = dataSourceMapped
        self.useOnlineData = useOnlineData
        self.test_size = test_size
        self.n_splits = n_splits
        self.should_describe_data = should_describe_data
        self.n_components_pca = n_components_pca

def as_config(dict, dataSetName):
    return Config(
        dict[dataSetName]['dataSourceRaw'],
        dict[dataSetName]['dataSourceMapped'],
        dict[dataSetName]['useOnlineData'],
        dict[dataSetName]['test_size'],
        dict[dataSetName]['n_splits'],
        dict[dataSetName]['should_describe_data'],
        dict[dataSetName]['n_components_pca'],
    )

def create_global_config(json_string = """
    {
        "it_data":{
            "dataSourceRaw": "./data/result_table.csv",
            "dataSourceMapped": "./data/joinit_data.csv",
            "useOnlineData": false,
            "test_size": 0.2,
            "n_splits": 10,
            "should_describe_data": true,
            "n_components_pca": 10
        }
    }"""):
    return as_config(json.loads(json_string), 'it_data')
