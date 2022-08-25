#  划分模块
from importlib import import_module


def get_variables(type,country):
    return import_module(f'{type}.{country}.variable')