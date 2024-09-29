from .utils.classfn import DotAccessibleDict

LatestFiles = DotAccessibleDict({
    'cmip6plus_ld': ['WCRP-CMIP','CMIP6Plus_CVs','compiled/graph_data.min.json','jsonld'],
    'cmip6plus': ['WCRP-CMIP','CMIP6Plus_CVs','compiled/graph_data.min.json','main'],
    'mip_cmor_tables_ld': ['PCMDI','mip-cmor-tables','compiled/graph_data.min.json','jsonld'],
    'mip_cmor_tables': ['PCMDI','mip-cmor-tables','compiled/graph_data.min.json','main'],
    "CF": ['WCRP-CMIP','CF','compiled/graph_data.min.json','main'],
})


# locations mandatory for graphing script to run
mapping = {
    'cmip6plus:': 'https://github.com/WCRP-CMIP/CMIP6Plus_CVs',
    'mip-cmor-tables:': 'https://github.com/PCMDI/mip-cmor-tables',
    'wolfiex-mip-cmor-tables:': 'https://github.com/wolfiex/wolfiex-mip-cmor-tables',
}

namesplit = lambda x: tuple(x.split('/')[3:5])

rmap = {namesplit(v):k for k,v in mapping.items()}
urlmap = {v:k for k,v in mapping.items()}
