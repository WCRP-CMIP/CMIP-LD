from ..locations import mapping,historic
from ..utils import sorted_ctx
from collections import OrderedDict

import glob
import json
import tqdm

# sort by length of key
mapping = dict(sorted(mapping.items(), key=lambda item: len(item[0])))


def main():
    
    # note, an easier, but messier way can achieved by speifying two contexts in the file. 
    # @context: [context1, context2] 
    
    ctxs = glob.glob('data_descriptors/*/*_context')
    print('Updating contexts: to match latest repository prefixes')
    for cx in tqdm.tqdm(ctxs):
        
        try:
        
            data = json.load(open(cx))
            
            data = OrderedDict(sorted((k, v) for k, v in data.items()))
            
            for rm in  historic:
                if rm in data['@context']:
                    del data['@context'][rm]# list comprehension to remove historic prefixes from mapping
            
            data['@context'].update(mapping)
            
            data = sorted_ctx(data)

            with open(cx,'w') as f:
                json.dump(data,f,indent=4)
                
        except Exception as e:
            print(f"Error: {str(e)}")
            print(f"Error with {cx}")
            continue
            
