
import glob, os, json
from ..locations import compact_url
from ..utils.git import io2url

def main():

    for dir in glob.glob("./data_descriptors/*/"):
        # DO THIS EXTERNALLY
        
        if not os.path.exists(dir+'_schema_') and not os.path.exists(dir+'_context'):
            # skip all directories without a schema and context
            continue
        
        contents = sorted([i.split('/')[-1].replace('.json','') for i in glob.glob(dir+'*.json')])
        
        # get the existing schema
        schema = json.load(open(dir+'_schema_'))
        schema['id'] = dir.split('/')[-2]
        
        
        # Update the files that exist
        # if '$defs' not in schema:
        #     schema['$defs'] = {}

        schema['contains'] = {
            "type": "string",
            "enum": contents
        }
            
            
        # Lets update the LD linked references. 
    
        ctx = json.load(open(dir+'_context_'))['@context']
        
        if not isinstance(ctx, list):
            ctx = [ctx]

        for c in ctx:
            if isinstance(c, dict):
                for key, value in c.items():
                    
                    
                    if isinstance(value, dict) and '@id' in value.values():
                        
                        ref = value["@context"].replace("_context_","")
                        
                        description = value.get('description',f'A reference object from <a href={ref}> {compact_url(ref)} </a>')
                        
                        schema['properties'][key] = {
                            "type": schema['properties'][key].get("type","string"),
                            "description": description,
                            "$ref":f"{ref}_schema_#/contains"
                        }
                
                # undo earlier mistake
                if key in schema:
                    del schema[key]
                        
                schema['base'] = io2url(c['@base'],path_base='data_descriptors/')
                
        # from pprint import pprint
        
        
        print(schema.keys())
        
        json.dump(schema, open(dir+'_schema_','w'), indent=4)
        
        print('add schema -> schema.json in production')
        
        
        
        
        
if __name__ == "__main__":
    main()