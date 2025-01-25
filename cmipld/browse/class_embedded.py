import os 
import cmipld
from cmipld import processor
from p_tqdm import p_map
from pyld import jsonld
from .class_depends import Depends

import signal
# Timeout handler
def handler(signum, frame):
    raise TimeoutError("Function timed out!")
# Set up signal handler for timeout
signal.signal(signal.SIGALRM, handler)


class EmbeddedFrame(Depends):
    def __init__(self,url, timeout = 5):
        self.url = processor.resolve_prefix(url)
        
        self.dependencies = processor.depends(url,graph=True)
        
        self.context = processor.contextify(url)
        
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
        framed = jsonld.frame(self.corpus,frame)
        
        if '@graph' in framed:
            framed = framed['@graph']
            
        return framed