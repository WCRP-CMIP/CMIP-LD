from .utils import DotAccessibleDict
import re

# Registered locations
mapping = {
    'wcrp-universe': 'https://wcrp-cmip.github.io/WCRP-universe/',
    'mip-variables': 'https://wcrp-cmip.github.io/MIP-variables/',
    'cmip6plus': 'https://wcrp-cmip.github.io/CMIP6Plus_CVs/',
    'cmip7': 'https://wcrp-cmip.github.io/CMIP7_CVs/',
    'cf': 'https://wcrp-cmip.github.io/CF/',
    'obs4mips': 'https://wolfiex.github.io/obs4MIPs-cmor-tables-ld//'
}

# sort
mapping = dict(sorted(mapping.items(), key=lambda item: len(item[0])))


# a dot accessible dict of the mapping
latest = DotAccessibleDict(dict([i,j +'graph'] for i,j in mapping.items()))


def fetchAll(subset=None):
    if subset:
        subset = {k:latest[k] for k in subset}
    else:
        subset = latest
        
    # expanded = []
    # for i in 
    



# regex matching if these exist
matches = re.compile(f"({'|'.join([i+':' for i in mapping.keys()])})")

def resolve_url(url):
    if url.startswith('http') and url.count(':')>2:
        return mapping.get(url,url)
    else:
        return url
    
def compact_url(url):
    if url.startswith('http') and url.count(':')>2:
        for k,v in mapping.items():
            if url.startswith(v):
                return url.replace(v,k+':')
        return url
    else:
        return url




