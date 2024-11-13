from .utils.classfn import DotAccessibleDict

# LatestFiles = DotAccessibleDict({
#     'cmip6plus_ld': ['WCRP-CMIP','CMIP6Plus_CVs','graph_data.min.json','jsonld'],
#     'cmip6plus': ['WCRP-CMIP','CMIP6Plus_CVs','graph_data.min.json','main'],
#     'mip_cmor_tables_ld': ['PCMDI','mip-cmor-tables','graph_data.min.json','jsonld'],
#     'mip_cmor_tables': ['PCMDI','mip-cmor-tables','graph_data.min.json','main'],
#     "CF": ['WCRP-CMIP','CF','compiled/graph_data.min.json','main'],
# })





# locations mandatory for graphing script to run
# added to contexts
mapping = {
    'wcrp-universe:': 'https://WCRP-CMIP.github.io/WCRP-UNIVERSE/',
    'mip-variables:': 'https://WCRP-CMIP/github.io/MIPvariables/',
    'cmip6plus:': 'https://WCRP-CMIP.github.io/CMIP6Plus_CVs/',
    'cmip7:': 'https://WCRP-CMIP.github.io/CMIP7_CVs/',
    'mip-cmor-tables:': 'https://PCMDI.github.io/mip-cmor-tables/',
    'cf': 'https://WCRP-CMIP.github.io/WCRP-CMIP/CF/',
}


namesplit = lambda x: tuple(x.split('/')[3:5])

rmap = {namesplit(v):k for k,v in mapping.items()}
urlmap = {v:k for k,v in mapping.items()}
