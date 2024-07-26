
from collections import OrderedDict

def name_description(data,key='name',value='description'):
    return dict([(x[key],x[value]) for x in data])

def key_only(data,key='name'):
    return list(set([x[key] for x in data]))


##################################
### MIP Table fns      ###########
##################################

def mip_cmor_tables_source_type (data):
    return key_only(data)

def mip_cmor_tables_frequency (data):
    return name_description(data)

def mip_cmor_tables_realm (data):
    return name_description(data)

def mip_cmor_tables_grid_label (data):
    return name_description(data)

##################################
### CMIP fns            ###########
##################################

def cmip6plus_organisations (data):
    data = [d['organisation_id'] for d in data]
    return name_description(data,key='cmip_acronym',value='name')

def cmip6plus_descriptors (data):
    data.update(data['index'])
    del data['index']
    data['DRS'] = data['drs']
    del data['drs']
    return data

def cmip6plus_source_id (data):
    
    sid = OrderedDict()
    for source in sorted(data,key=lambda x: x['source_id']):
        # ideally organisation 
        source['institution_id'] = source['organisation_id'].get('cmip_acronym','')
        
        source['license'].update(source['license'].get('kind',{}))
        
      
        source['source'] = f"{source['source_id']} ({source['release_year']}): \n  "
       
        
       
        #    combine the model-components
        for i in source['model_component']:
            try:
                source['source'] += f"{i['name']} ({i['realm']})\n  "
            except Exception as e:
                
                print('Missing',i, source['source_id'])
                
                print(e)
                
            
        # del source['license']['kind']
        # del source['license']['conditions']
        
        del source['model_component']
        sid[source['source_id']] = source
        
    return sid
        
def cmip6plus_native_nominal_resolution (data):
    print(data[0])
    return list(set([f"{x['nominal_resolution'].get('value',x['nominal_resolution'])}{x['nominal_resolution'].get('unit',{}).get('si','km')}" for x in data]))
    

def cmip6plus_sub_experiment_id (data):
    return name_description(data,'sub_experiment_id','description')


def cmip6plus_experiment_id (data):
    eid = OrderedDict()
    for e in sorted(data,key=lambda x: x['experiment_id']):
        for i in ['additional_allowed','required']:
            if isinstance(e['model_components'][i],str):
 
                e['model_components'][i] = [e['model_components'][i]]
        eid[e['experiment_id']] = e
    
    return eid



##################################
### Main processing function #####
##################################
local_globals = globals()

async def process(prefix,file,data=None):
    name = f'{prefix}_{file}'.replace('-','_')
    # prepare for use. 
    
    data.clean_cv
    if name in local_globals:
        data.data = local_globals[name](data.data) 
    else:
        print('no parsing function found', name)
    
    return data.json
