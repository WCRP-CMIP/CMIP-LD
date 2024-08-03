'''
Generation script for creating a CV from the CMIP6Plus and MIP tables.

python -m cmipld.cvs.generate

'''
# python -m cmipld.cvs.generate

# Import the library
from cmipld import *
import asyncio,json,os
from collections import OrderedDict
from parse import process
from datetime import datetime


async def main():

    # latest = await sum([mip,cmip6plus],[])
    latest = await CMIPFileUtils.load(['/Users/daniel.ellis/WIPwork/CMIP6Plus_CVs/compiled/graph_data.json','/Users/daniel.ellis/WIPwork/mip-cmor-tables/compiled/graph_data.json'])

    CV = {}
    # OrderedDict()


    ##################################
    ### MIP Entries #####
    ##################################

    # mip entries
    for key in 'source-type frequency realm grid-label nominal-resolution'.split():
        
        # run the frame. 
        frame = get_frame('mip-cmor-tables',key)
        
        # get results using frame
        data = Frame(latest,frame)
        
        # any additional processing?
        print(key)
        add_new = await process('mip-cmor-tables',key,data)
        
        CV[key.replace('-','_')] = add_new
    

    ##################################
    ### CMIP6Plus Core #####
    ##################################
    
        
    frame = get_frame('cmip6plus','descriptors')
    data = Frame(latest,frame,False).clean(['rmld','missing','untag','lower'])
    
    add_new = await process('cmip6plus','descriptors',data,clean=['rmld','missing','untag','lower'])

    
    CV.update(add_new)

    # ##################################
    # ### CMIP6Plus #####
    # ##################################
    # # organisations
    # # native-nominal-resolution
    for key in 'organisations activity-id sub-experiment-id experiment-id source-id'.split():
        
        print(key)
        # run the frame. 
        frame = get_frame('cmip6plus',key)
        # get results using frame
        data = Frame(latest,frame)
        
        add_new = await process('cmip6plus',key,data)

        CV[key.replace('-','_')] = add_new
        
    CV['institution_id'] = CV['organisations']
    del CV['organisations']
    
    
    print('concluding')
    ##################################
    ### fix the file #####
    ##################################
    
    CV['version_metadata'] = {
        "file_modified" : datetime.now().date().isoformat(),
        "CV": {
            "version": os.popen('git describe --tags --abbrev=0').read().strip() or 'version tag read from repo running  - currently not in it. ', 
            "git_commit":os.popen('git rev-parse HEAD').read().strip(), 
            "gitbranch" : os.popen('git rev-parse --abbrev-ref HEAD').read().strip() } ,
        "future": 'miptables, checksum, etc'}
    
    print('above not fatal - version metadata')
            
    CV = OrderedDict(sorted((k, (v)) for k, v in CV.items()))
    
    # import pprint
    # pprint.pprint(CV)
    # print(CV)
    
    writelocation = os.path.join(os.path.dirname(__file__),'CV.json')
    
    with open(writelocation,'w') as f:
            json.dump(dict(CV = CV),f,indent=4)    
            print('written to ',f.name )    
        
        
    return os.path.abspath(writelocation)
        

def test(writelocation):
    
    import pytest
    
    # Run pytest and capture the result
    testsuite =os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests/cvs/'))
    print(testsuite,writelocation)
    result = pytest.main(["-v",f"--file-location={writelocation}", f"{testsuite}"])
    
    # # Print a summary based on the result
    # if result == pytest.ExitCode.OK:
    #     print("\nAll tests passed successfully!")
    # elif result == pytest.ExitCode.TESTS_FAILED:
    #     print("\nSome tests failed. Please check the output above for details.")
    # else:
    #     print(f"\nAn error occurred while running the tests. Exit code: {result}")
    

'''
!cd ../tests/;
!pytest -v --file-location='/Users/daniel.ellis/WIPwork/CMIP-LD/cmipld/cvs/CV.json' /Users/daniel.ellis/WIPwork/CMIP-LD/cmipld/tests/cvs

'''



if __name__ == "__main__":
    writelocation = asyncio.run(main())
    print('pass cv location into tests')
    test(writelocation)