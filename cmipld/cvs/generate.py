print('test')
# python -m cmipld.cvs.generate

# Import the library
from cmipld import *
import asyncio
from collections import OrderedDict
import parse
from parse import process
from pprint import pprint
import json


async def main():
    # we can load the latest cmpi6plus and mip table files from github
    # latest = await CMIPFileUtils.load_latest(CMIPFileUtils)
    mip= await CMIPFileUtils.read_file_fs('/Users/daniel.ellis/WIPwork/mip-cmor-tables/JSONLD/scripts/compiled/graph_data.json')
    cmip6plus =  await CMIPFileUtils.read_file_fs('/Users/daniel.ellis/WIPwork/CMIP6Plus_CVs/JSONLD/scripts/compiled/graph_data.json')
    
    latest = sum([mip,cmip6plus],[])


    CV = OrderedDict()


    ##################################
    ### MIP Entries #####
    ##################################

    # mip entries
    for key in 'source-type frequency realm grid-label'.split():
        
        # run the frame. 
        frame = get_frame('mip-cmor-tables',key)
        
        # get results using frame
        data = Frame(latest,frame)
        
        
        # any additional processing?
        add_new = await process('mip-cmor-tables',key,data)
        
        # pprint(add_new)
        print(key)
        CV[key] = add_new
        
    # nominal_resolution
    
    ##################################
    ### CMIP6Plus #####
    ##################################
    
    for key in 'organisations'.split():
        
        # run the frame. 
        frame = get_frame('cmip6plus',key)
        
        # get results using frame
        data = Frame(latest,frame)
        
        # any additional processing?
        add_new = await process('cmip6plus',key,data)
        
        # pprint(add_new)
        print(key)
        CV[key] = add_new
        
  
    ##################################
    ### CMIP6Plus Core #####
    ##################################
        
    frame = get_frame('cmip6plus','descriptors')
    data = Frame(latest,frame,False).clean()
    add_new = await process('cmip6plus','descriptors',data)
    CV.update(add_new)


     
    print(list(CV.keys()))
    
    print("mip:core-descriptors" in str(latest))
    
    # from pyld import jsonld
    # print(jsonld.frame(latest,{"@type":"mip:core-descriptors"}))
    
    with open('CV.json','w') as f:
            json.dump(CV,f,indent=4)    
        
        




print("nominal-resolution!!!!!!!!")







if __name__ == "__main__":
    asyncio.run(main())