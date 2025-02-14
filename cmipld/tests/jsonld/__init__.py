# from .components import * 
from pydantic import BaseModel, field_validator


def field_test(extended_class):
    # dynamic class
    return type(extended_class.__name__, (BaseModel, extended_class), {})

def multi_field_test(args):
    assert isinstance(args, list)
    return type('multi_field_test', (BaseModel, *args), {})