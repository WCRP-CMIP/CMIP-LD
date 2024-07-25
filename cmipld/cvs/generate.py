'''
Generation script for creating a CV from the CMIP6Plus and MIP tables.

python -m cmipld.cvs.generate

'''
# python -m cmipld.cvs.generate

# Import the library
from cmipld import *
import asyncio,json
from collections import OrderedDict
from parse import process



async def main():
    # we can load the latest cmpi6plus and mip table files from github
    
    # latest = await CMIPFileUtils.load_latest(CMIPFileUtils)
    
    # manual read since we are in development. 
    mip= await CMIPFileUtils.read_file_fs('/Users/daniel.ellis/WIPwork/mip-cmor-tables/compiled/graph_data.json')
    cmip6plus =  await CMIPFileUtils.read_file_fs('/Users/daniel.ellis/WIPwork/CMIP6Plus_CVs/ compiled/graph_data.json')
    
    latest = sum([mip,cmip6plus],[])


    CV = {}
    # OrderedDict()


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
        
        CV[key.replace('-','_')] = add_new
        
    # nominal_resolution
    

    ##################################
    ### CMIP6Plus Core #####
    ##################################
        
    frame = get_frame('cmip6plus','descriptors')
    data = Frame(latest,frame,False).clean()
    add_new = await process('cmip6plus','descriptors',data)
    CV.update(add_new)

    ##################################
    ### CMIP6Plus #####
    ##################################
    # organisations
    # native-nominal-resolution
    for key in 'organisations source-id activity-id experiment-id sub-experiment-id'.split():
        
        # run the frame. 
        frame = get_frame('cmip6plus',key)
        
        # get results using frame
        data = Frame(latest,frame)
        
        # any additional processing?
        add_new = await process('cmip6plus',key,data)
        
        # pprint(add_new)
        print(key)
        CV[key.replace('-','_')] = add_new
        
    
    
    
    ##################################
    ### fix the file #####
    ##################################

        
    CV = OrderedDict(sorted((k, (v)) for k, v in CV.items()))
    
    with open('CV.json','w') as f:
            json.dump(dict(CV = CV),f,indent=4)    
        
        







if __name__ == "__main__":
    asyncio.run(main())