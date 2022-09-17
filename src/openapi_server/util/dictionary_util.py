import inflection
from typing import List

def remove_keys(input_dict: dict, keys: List[str]) -> dict:
    clone = {** input_dict}
    for k in keys:
        del clone[k]
    return clone


def camelize_keys(input_dict: dict) -> dict:
    camelCaseKeys = list(map(lambda e: inflection.camelize(e, False), input_dict.keys()))
    return dict(zip(camelCaseKeys,list(input_dict.values()))) 
