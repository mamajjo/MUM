from pathlib import Path

class Config(object):
    def __init__(self, dataSourceUrl, test_size, n_splits, should_describe_data):
        self.dataSourceUrl = dataSourceUrl
        self.test_size = test_size
        self.n_splits = n_splits
        self.should_describe_data = should_describe_data
        
import json

def as_config(dct):
    return Config(
        dct['dataSourceUrl'],
        dct['test_size'],
        dct['n_splits'],
        dct['should_describe_data'],
        )

configuration = json.loads(Path("configuration.json").read_text(), object_hook = as_config)