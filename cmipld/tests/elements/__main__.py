print(1)
# python -m cmipld.tests.elements
import cmipld.tests.elements
import configparser
# from . import activity
import json,sys,os,re

issue_body = os.environ.get('ISSUE_BODY')
issue_submitter = os.environ.get('ISSUE_SUBMITTER')
repo = os.environ.get('REPO').replace('https://github.com','https://api.github.com/repos')
token = os.environ.get('GH_TOKEN')






conf = '''
[institution]
    Acronym = CMIP-IPO
    Full_Name = CMIP Model Intercomparison Project Office
    ROR = 000fg4e24
    
    # only change the item below to "update" if you are submitting a correction. 
    action = new    
    
[activity]
    Name = CMIP
    Long_Name =  Coupled Model Intercomparison Project
    URL = https://wcrp-cmip.org
    
    # only change the item below to "update" if you are submitting a correction. 
    action = new
    
[sub-experiment-id]
    name =  new-sub-experiment
    description = A sample sub-experiment id
    
    # only change the item below to "update" if you are submitting a correction. 
    action = new
''' 


errors = []

# process conf
config = configparser.ConfigParser()
config.read_string(conf)

# print(config.sections())

for section in config.sections():
    try: 
        # data 
        entry = dict(config[section])
        # library
        section = section.replace('-',"_")
        entrylib = getattr(cmipld.tests.elements,section)
        # class + data
        entryclass = getattr(entrylib,section)()
        
        # print(entry)
        
        entryclass.create_jsonld(entry,write=True)
        
        # write
        # change branch 
        

        kind = __file__.split('/')[-1].replace('.py','')

        payload = {
            "event_type": kind,
            "client_payload": {
                "name": data['acronym'], # we need this to define the pull request
                "issue": issue_number,
                "author" : issue_submitter,
                "data" : json.dumps(data)
            }
        }


dispatch(token,payload,repo)

        
        

    except ModuleNotFoundError as e:
        errors.append(f"No such module {section} in cmipld. Please check the congifuration file template.")
        continue
    
    
    
    
    

    if errors:
        print(errors)  
        
        
        
    # git add one file. 
    # git commit with user
    # git push 
    
    