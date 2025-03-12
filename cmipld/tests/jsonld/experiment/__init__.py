
from pydantic import BaseModel, field_validator
from pydantic import StrictStr, StrictBool, StrictFloat
from typing import Union, Optional
import json



from ..components import id_field, type_field


class experiment(BaseModel,id_field,type_field,ror_field):

    tier:int

    @field_validator('type', mode='after')  
    @classmethod
    def type_contains(cls,value):
        assert 'wcrp:experiment' in value
        return value
    
    @field_validator('tier', mode='after')  
    @classmethod
    def tier_val(cls,value):
        assert value in [1,2,3]
        return value
    
    
    
    def json(self):
        return self.model_json_dump()
    
# Example usage
# a = EMD(**{'num':'1','id':'ts-t'})