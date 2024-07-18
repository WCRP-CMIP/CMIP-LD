
def name_description(data,key='name',value='description'):
    return dict([(x[key],x[value]) for x in data])

def key_only(data,key='name'):
    return [x[key] for x in data]


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
    data = [d['organisation-id'] for d in data]
    return name_description(data,key='cmip-acronym',value='name')
def cmip6plus_descriptors (data):
    data.update(data['index'])
    del data['index']
    return data





##################################
### Main processing function #####
##################################
local_globals = globals()

async def process(prefix,file,data=None):
    name = f'{prefix}_{file}'.replace('-','_')
    
    data.clean()
    # print(list(local_globals)
    if name in local_globals:
        data.data = local_globals[name](data.data) 
    else:
        print('no parsing function found', name)
    
    return data.json
