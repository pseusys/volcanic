from configparser import ConfigParser
from typing import Dict


def read_config(filename: str = "default.ini") -> Dict[str, Dict[str, int]]:
    config = ConfigParser()
    config.read(filename)

    data = dict()
    for section in config.sections():
        data[section] = {key: int(config[section][key]) for key in config[section]}
    return data
