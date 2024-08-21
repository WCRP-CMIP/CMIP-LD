print(1)
# python -m cmipld.tests.elements
import cmipld.tests.elements
import configparser, importlib
# from . import activity

conf = '''
[activity]
    Name = CMIP
    Long_Name =  Coupled Model Intercomparison Project
    URL = https://wcrp-cmip.org 
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
        entrylib = getattr(cmipld.tests.elements,section)
        # class + data
        entryclass = getattr(entrylib,section)()
        
        # print(entry)
        
        entryclass.create_jsonld(entry)
        

    except ModuleNotFoundError as e:
        errors.append(f"No such module {section} in cmipld. Please check the congifuration file template.")
        continue
    
    
    
    
    

    if errors:
        print(errors)  
        
    print(entrylib.template)
        
        
    # git add one file. 
    # git commit with user
    # git push 
    
    