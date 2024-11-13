from ..locations import mapping
from ..utils import sorted_ctx
from collections import OrderedDict

import glob
import json
import tqdm

def main():
    
    # note, an easier, but messier way can achieved by speifying two contexts in the file. 
    # @context: [context1, context2] 
    
    ctxs = glob.glob('data_descriptors/*/*_context')
    print('Updating contexts: to match latest repository prefixes')
    for cx in tqdm.tqdm(ctxs):
        
        data = json.load(open(cx))
        
        data = OrderedDict(sorted((k, v) for k, v in data.items()))
        
        data['@context'].update(mapping)
        
        data = sorted_ctx(data)

        with open(cx,'w') as f:
            json.dump(data,f,indent=4)
