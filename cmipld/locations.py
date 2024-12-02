from .utils import DotAccessibleDict

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
    'wcrp-universe': 'https://wcrp-cmip.github.io/WCRP-UNIVERSE/',
    'mip-variables': 'https://wcrp-cmip.github.io/MIP-variables/',
    'cmip6plus': 'https://wcrp-cmip.github.io/CMIP6Plus_CVs/',
    'cmip7': 'https://wcrp-cmip.github.io/CMIP7_CVs/',
    # 'mip-cmor-tables': 'https://PCMDI.github.io/mip-cmor-tables/',
    'cf': 'https://wcrp-cmip.github.io/CF/',
    'obs4mips': 'https://wolfiex.github.io/obs4MIPs-cmor-tables-ld//'
}

historic = ['mip-variables','cmip6plus','cmip7','cf','wcrp-universe','mip-cmor-tables','mip-variables:', 'cmip6plus:', 'cmip7:', 'cf:', 'wcrp-universe:', 'mip-cmor-tables:']


# namesplit = lambda x: tuple(x.split('/')[3:5])

# rmap = {namesplit(v):k for k,v in mapping.items()}
# urlmap = {v:k for k,v in mapping.items()}
