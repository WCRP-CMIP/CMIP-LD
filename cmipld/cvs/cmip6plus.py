def get_entry(data,entry='label'):
    if isinstance(data,dict):
        data = list(data.values())
        print(data)
    return [i.get(entry) for i in data]

def name_entry(data,value = 'description', key='label'):
    if isinstance(data,list):
        {entry[key]: entry[value] for entry in data}


def license(data):
    return data

'''
# Activity:Name

Experiment:
    
    
frequency : x:what
gridl:x:what


institutionL: x:what
license:licensestr

mipera - value only

nominal = list



realm

source

sub ex :what





# def tables(data):
#     return get_entry(data['tables'])

'''





functionlist = {}

##################################
# Literals 
##################################

literals = ['tracking-id', 'drs', 'index', 'required-global-attributes' ,'repo'] 

for name in literals:
    field = name.replace('-','_')
    def literal_wrapper(data, field=field): 
        return data[field]
    functionlist[name] = literal_wrapper



##################################
# Name: Description pairs. 
##################################

name_description = ['realm','frequency','grid-label','nominal','sub_experiment'] 

for name in name_description:
    field = name.replace('-','_')
    def nd_wrapper(data, field=field): 
        return name_entry(data)
    functionlist[name] = nd_wrapper




##################################
# Label Extraction
##################################

'''
All of the following names formulate a function of the format

def <name> (data):
    return get_entry(data[<name>])

This function saves us having to hard code them all. 

# ids are specified with a '-' as not to affect path parsing, 
# # however keys are not allowed '-' and must contain '_' instead.
'''

# List of function names 
named_entry_feed = ['mip-era','activity','product', 'tables']
    # 'tables',

for name in named_entry_feed:

    field = name.replace('-','_')
    
    def entry_wrapper(data, field=field):  
        return get_entry(data[field],entry='label')
    
    functionlist[name] = entry_wrapper







locals().update(functionlist)

# end named field 






    