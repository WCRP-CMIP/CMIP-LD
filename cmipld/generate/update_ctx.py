from ..locations import mapping
from ..utils import sorted_ctx

import glob
import json
import tqdm

def main():
    ctxs = glob.glob('data_descriptors/*/*_context')
    print('Updating contexts: to match latest repository prefixes')
    for cx in tqdm.tqdm(ctxs):
        
        data = json.load(open(cx))
        data['@context'].update(mapping)
        
        data = sorted_ctx(data)

        with open(cx,'w') as f:
            json.dump(data,f,indent=4)
