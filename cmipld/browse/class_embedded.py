import os 
import cmipld
from cmipld import processor
from p_tqdm import p_map
from pyld import jsonld
from .class_depends import Depends
from .contexts import get_context

import signal
# Timeout handler
def handler(signum, frame):
    raise TimeoutError("Function timed out!")
# Set up signal handler for timeout
signal.signal(signal.SIGALRM, handler)


class EmbeddedFrame(Depends):
    def __init__(self,url, timeout = 10):
        self.url = processor.resolve_prefix(url)
        
        self.dependencies = processor.depends(url,graph=True)
        
        self.context_url = processor.contextify(url)
        
        # expand_context here
        self.context = get_context(self.context_url)
        
        self.container = []
        self.me = None
        
        
        if '@container' in str(self.context):
            print('WARNING: Part of the loaded context contains a "@container" this may mean referenced items become nested in framing.\n Please use .iterative_frame() instead.')
            
            self.dirpath = os.path.dirname(self.url)
            # filter out direct path. 
            
            # index for the corpus item
            self.me = [i for i,u in enumerate(self.dependencies) if self.dirpath in u ] 
            assert len(self.me) == 1
            self.me = self.me[0]
            
            
            
            
            # get the container items
            self.container = [k for k,v in self.context.items() if '@container' in v ]
                    

        self.urlindex = self.dependencies
        
        
        # if self.corpus takes too long
        signal.alarm(len(self.dependencies)*timeout)
        
        try:
            self.corpus = {'@graph':p_map(jsonld.expand,self.dependencies)}
            
        except TimeoutError:
            print('Extraction took to long', 'extracting files in serial to check for problems.')
            
            self.corpus = {'@graph':[]}
            for i in self.dependencies:
                # if a problem occurs (error) this will tell us which file is responsible. 
                print(f'Loading {i}.')
                self.corpus['@graph'].append(jsonld.expand(i))
                
            print('Serial loading completed sucessfuly. ')
            
        signal.alarm(0)  # Cancel the alarm
        
        
    def frame(self,frame={}):
        if '@context' not in frame:
            frame['@context'] = self.context
        if '@embed' not in frame:
            frame['@embed'] = '@always'
        framed = jsonld.frame(self.corpus,frame,options={'embed':'@always','extractAllScripts':True,'expandContest':True})
        
        if '@graph' in framed:
            framed = framed['@graph']
        
        
        # if self.container:
            
        #     for id,val in enumerate(framed):
        #         for cnt in self.container:
                    
        #             for v in val:
        #                 framed[id][cnt][v]self.corpus['@graph'][self.me][id]
        
            
            
            
        return framed
    
    def iterative_frame(self,frame):
        
        # get referenced ids.
        independant_ids = [f'{self.dirpath}/{i}' for i in jsonld.frame(self.url,{"@explicit":True})['@graph'] if '@type' in i]
        
        framed = jsonld.frame({"@graph":[id]+self.corpus})
        
    
