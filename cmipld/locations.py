from .utils.classfn import DotAccessibleDict

LatestFiles = DotAccessibleDict({
    'cmip6plus_ld': ['WCRP-CMIP','CMIP6Plus_CVs','compiled/graph_data.min.json','jsonld'],
    'mip_cmor_tabes_ld': ['PCMDI','mip-cmor-tables','compiled/graph_data.min.json','jsonld'],
})


mapping = {
    'cmip6plus:': 'https://github.com/WCRP-CMIP/CMIP6Plus_CVs',
    'mip-cmor-tables:': 'https://github.com/PCMDI/mip-cmor-tables',
}

namesplit = lambda x: tuple(x.split('/')[3:5])

rmap = {namesplit(v):k for k,v in mapping.items()}