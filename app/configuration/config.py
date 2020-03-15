from pathlib import Path

class Config(object):
    def __init__(self, dataSourceUrl):
        self.dataSourceUrl = dataSourceUrl
import json

def as_config(dct):
    return Config(
        dct['dataSourceUrl']
        )

configuration = json.loads(Path("configuration.json").read_text(), object_hook = as_config)