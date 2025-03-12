
from pydantic import BaseModel, Field, field_validator
from pydantic import StrictStr, StrictBool, StrictFloat
from typing import Union, Optional
import json,os
from cmipld import mapping,jsonld


from ..components import id_field, type_field, validate_date


class experiment_model(BaseModel,id_field,type_field):

    tier:int
    minimum_number_of_years: int = Field(..., alias="minimum-number-of-years")
    start_date: Optional[StrictStr] = Field(..., alias="start-date")
    branch_date: Optional[StrictStr] = Field(..., alias="branch-date")
    model_realms: Optional[list[dict]] = Field(..., alias="model-realms")
    description: StrictStr
    parent_experiment: StrictStr = Field(..., alias="parent-experiment")
    
    

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
    
    
    @field_validator('start_date', mode='after')
    @classmethod
    def s_date(cls,value):
        validate_date(value)
        return value
    
    @field_validator('branch_date', mode='after')
    @classmethod
    def s_date(cls,value):
        validate_date(value)
        return value
    

    @field_validator('model_realms', mode='after')
    @classmethod
    def ld_realms(cls,value):
        
        urlbase = cmipld.mapping['universal']
        for i in value:
            
            url = f'{urlbase}source-type/{i['id']}'
            try:
                jsonld.expand(url)
            except:
                raise ValueError(f"Invalid model realm: {i['id']}. Please check {url} exists and the data is correct. If missing, this may need to be registered. ")
            # jsonld.compact(url,url)['label']
        return value
        
    @field_validator('parent_experiment', mode='after')
    @classmethod
    def parent_e(cls,value):
        if value == 'none':
            return value
        
        dir = 'src-data/experiment/'
        if value not in [f.replace('.json','') for f in os.listdir(dir) ]:
            
            raise ValueError(f"Parent experiment {value} not found in {dir}")
        
        print('can a parent experiment be exist in another project?')

        return value
    
    
        
    
    def json(self):
        return self.model_json_dump()
    
# Example usage
# a = EMD(**{'num':'1','id':'ts-t'})