from cmipld.tests.elements.global_import import *
from typing import List, Optional
import asyncio

elementpath = 'organisations/institutions'
elementtype = "institution"
owners=['mip-cmor-tables:']

repo_path = repo_info.ldpath('')
repourl = repo_info.url()
reposhort = urlmap[repourl]

####################################################
# Issue Templates
####################################################
conf = f'''
[{elementtype}]
    Acronym = "CMIP-IPO"
    Full_Name = "Coupled Model Intercomparison Project: International Project Office"
    ROR = "000fg4e24"
    
    # only change the item below to "update" if you are submitting a correction. 
    action = "new"
''' 

description = '''
'''

more_info = ''




URL_TEMPLATE = 'https://api.ror.org/organizations/{}'

def similarity(name1, name2):
    from difflib import SequenceMatcher
   
    matcher = SequenceMatcher(None, name1, name2)
    similarity = matcher.ratio() * 100

    return similarity



async def parse_ror_data(ror,cmip_acronym):
    
    """Parse ROR data and return relevant information."""
    
    url = URL_TEMPLATE.format(ror)
    ror_data = await  CMIPFileUtils().read_file_url(url)
    if ror_data:

        return {
            "@id": ldname(f"mip-cmor-tables:organisations/institutions/{cmip_acronym.lower()}"),
            "@type": elementtype,
            "cmip_acronym": cmip_acronym,
            "ror": ror_data['id'].split('/')[-1],
            "name": ror_data['name'],
            "url": ror_data.get('links', []) ,
            "established": ror_data.get('established'),
            "kind": ror_data.get('types', [])[0] if ror_data.get('types') else None,
            "labels": [i['label'] for i in ror_data.get('lables', [])],
            "aliases": ror_data.get('aliases', []),
            "acronyms": ror_data.get('acronyms', []),
            "location": {
                "@id": f"mip-cmor-tables:organisations/institutions/location/{ror_data['id'].split('/')[-1]}",
                "@type": "location",
                "@nest": {
                    "lat":  ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
                    "lon":  ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
                    "city": ror_data['addresses'][0].get('city') if ror_data.get('addresses') else None,
                    "country": list(ror_data['country'].values())  if ror_data.get('country') else None
                }
            }         
            #  can reverse match consortiums or members from here.    
            
        }
    else:
        return None
    

####################################################
# Validation Functions
####################################################

class LocationNestModel(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None
    city: Optional[str] = None
    country: Optional[List[str]] = None

class LocationModel(BaseModel):
    id: str = Field(..., alias="@id")
    type: str = Field(..., alias="@type")
    nest: LocationNestModel = Field(..., alias="@nest")
    
class Validate(BaseModel):
    '''
    Pydantic model for validating element files
    '''
    
    id: str = Field(..., alias="@id")
    type: str = Field(..., alias="@type")
    cmip_acronym: str
    ror: str
    name: str
    kind: str
    url: Optional[List[HttpUrl]] = None
    established: Optional[int] = None
    org_type: Optional[str] = Field(None, alias="type")
    labels: List[str] = []
    aliases: List[str] = []
    acronyms: List[str] = []
    location: LocationModel

    

    @field_validator('id')
    def id(cls, v):
        if not v.startswith(f"{reposhort}:{elementpath}"):
            raise ValueError('must start with the correct path')
        return v
    
    @field_validator('type')
    def type(cls, v):
        if v != elementtype:
            raise ValueError(f'{v} must be {elementtype} ')
        return v
    
    @field_validator('name')
    def name(cls, v):
        if len(v) < 3 or len(v) > 250:
            raise ValueError('must be at between 3 and 250 characters')
        return v
    
    @field_validator('acronyms')
    def acronym_on_ror(cls, v, values):  
        # values.data.acronyms === v
        return values.data['cmip_acronym'] in v
   
   
    # after alias resolved
    @model_validator(mode='before')#before
    def check_keys(cls, values):
        return check_all_keys_present(cls, values)
        

####################################################
# Element Class
####################################################
class institution(MIPConfig):
    
    def __init__(self) -> None:
        # super().__init__()
        
        self.checks = Validate
        


    ##### Config to JSONLD #####
    def create_jsonld(self,conf,write=True):

        self.conf = conf
        self.action = conf['action']
        del conf['action']
        
        self.json = asyncio.run(parse_ror_data(conf['ror'],conf['acronym']))
    
        path = ldname(f"{repo_path}/{elementpath}/{self.conf['acronym'].lower()}.json")
        
        # def update_issue_title (what,payload):
        if self.action == 'new':
            if os.path.exists(path):
                cmipld.utils.git.close_issue('### File Already Exists \n Closing Issue. \n If you meant to update the file, please change the action to "update"')
                raise FileExistsError(f'File Already Exists {path}')
            
            self.pullname = f"Add {elementtype}:{self.getid}"
            cmipld.utils.git.update_issue_title(f"{self.pullname} [{self.json['cmip_acronym']}] - {self.json['name']}")

        
        
        
        ##########################
        # Check for Similarity in full name
        ##########################
        likeness = similarity(self.json['name'], self.conf['full_name'])
        comment = f"####Similarity: {likeness:.2f}% <br> `[\"{self.json['name']}\" | \"{self.conf['full_name']}\"]`"
        
        if likeness < 55:
            # exit 
            comment = f'#Closing Issue <br> {comment} <br> Please review and edit the configuration above. If unsure check the ROR ID {URL_TEMPLATE.format(self.json["ror"])}'
            cmipld.utils.git.close_issue(comment)
        
        else:
            cmipld.utils.git.update_issue(f'#Sanity Check \n {comment}')
            
        
        if self.validate(self.json):
            # print(json.dumps(self.json, indent=4))
            
            if write:
                
                cmipld.utils.git.prepare_pull(f'{elementtype}:{self.getid}','main')

                with open(path, 'w') as f:
                    json.dump(cmipld.utils.sorted_dict(self.json), f, indent=4)
                    
                author = os.environ.get('OVERRIDE_AUTHOR','cmip-ipo')
                cmipld.utils.git.addfile(path,author,f"New entry {self.getid} to the {elementpath} LD file")
                
                
                
                
                
                
                print(path)
                
                
            
                
            return True
        else: 
            return False
        
# publish 
# dispatch with changes. 
# create PR


# util to change _- and vive versa



# global checks to ensure no duplicates. Enure before accepting pull request 


        
        
        
def test_config():
    # test_config()
    import configparser
    cfg = configparser.ConfigParser()
    cfg.read_string(conf)
    
    element = __file__.split('/')[-1].split('.')[0]
    templateconf =  dict(cfg[element])
    
    test = globals()[element]()
    test.create_jsonld(templateconf,write=False)
    
    
    
def get_template():
    
    if reposhort not in owners:
        return None
    
    test_config()
    
    location = repo_path.replace('JSONLD',f".github/ISSUE_TEMPLATE/{elementtype}.md") 
    
    print(f"Saving {elementtype} to {location}")
    
    return create_template(elementtype, more_info, conf,location)


    
   
        