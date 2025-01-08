import cmipld
from pprint import pprint
process = cmipld.JsonLdProcessor()


res = process.get('https://wcrp-cmip.github.io/CMIP6Plus_CVs/project/activity.json',compact = True)




pprint(res)
