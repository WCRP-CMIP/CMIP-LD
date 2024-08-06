

from collections import Counter
from pyld import jsonld
from cmipld import CMIPFileUtils,Frame,locations
from cmipld.utils.classfn import sorted_dict
import re,json,sys,os
from typing import Dict, Any, List, Optional


class JSONLDGraphProcessor:
    """
    A class to process JSON-LD files and extract information.

    Attributes:
    - latest_data: The latest JSON-LD data.
    """
    
    # def __init__(self):
    #     ...

    async def make_graph(self,loaditems):
        """ create the graph. """
        
        self.lddata = await CMIPFileUtils.load(loaditems)
        print(len(self.lddata))

        # classic id extraction for checks
        ids = set(re.findall(r'"@id"\s*:\s*"([^"]+)"', json.dumps(self.lddata)))

        # get the triplets
        triplets = jsonld.to_rdf(self.lddata)

        # grab all the types and ids
        type_map = {}
        self.nodes = []
        self.links = []

        clink = lambda s: '/'.join(s.split('/')[:-1])
        prefix = lambda s: s.split(':')[0]


        for group in triplets.values():
            for t in group:
                s = str(t)
                if 'literal' not in s and '_:' not in s:
                    if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' in s:
                        type_map[t['subject']['value']] = t['object']['value']
                        
                        node = dict(id=clink(t['subject']['value']),type=t['object']['value'], origin=prefix(t['subject']['value']))
                        if node['origin']!='https':
                            self.nodes.append(node)
                    else:
                        try:
                            link = dict(source=clink(t['subject']['value']),target=clink(t['object']['value']),predicate=t['predicate']['value'])
                            self.links.append(link)
                            
                            # additional origin links
                            src  = link['source']
                            path = re.split(r'[:/]',src)
                            for i in range(1,len(path)):
                                me = path[i-1]
                                n2 = dict(id=me,type='directory',origin=path[0])
                                self.nodes.append(n2)
                                l2= dict(source=path[i-1],target=path[i],predicate='_')
                                self.links.append(l2)
                            # dont forget the final node. 
                            me = path[i]
                            n2 = dict(id=me,type='directory-path',origin=path[0])
                            self.nodes.append(n2)
                            # link up to original
                            l2= dict(source=path[i],target=src,predicate='_')
                            self.links.append(l2)
                            
                        except:
                            # skips out the blank nodes
                            print(t)
                            ...
                                    
        directories = list(set(triplets.keys()))
        # find missing and problem keys 
        self.missing = list(set(ids) - set(type_map.keys()) - set(directories))
        from collections import Counter

        nodeweights = Counter([i['id'] for i in self.nodes])
        linkweights = Counter([f"{i['source']} -> {i['target']}" for i in self.links])

        for i in self.nodes:
            i['weight'] = nodeweights[i['id']]
            
        for i in self.links: 
            i['weight'] = linkweights[f"{i['source']} -> {i['target']}"]


        self.nodes = list(dict([(i['id'],i) for i in self.nodes]).values())
        self.links = list(dict([((i['source'],i['target'],i['predicate']),i) for i in self.links]).values())



        self.types = dict([[v,clink(k)] for k,v in type_map.items()])


        # since the types are defined by the vocab
        self.vocab = {v: k.replace('mip:','') for k, v in self.types.items() if 'https' not in v}

        self.graph = dict(nodes=self.nodes,links=self.links,types=self.types,vocab=self.vocab, missing = self.missing)
        
        return self
        
    def read_graph(self,location = 'network.json'):
        """ read the graph from a file. """
        self.graph = json.load(open(location,'r'))
        
        return self
        
    def write(self,location = 'network.json',item = 'graph'):
        """ write the graph to a file. """
        
        data = self.__dict__.get(item)
        if data == {}:
            print(f"No {item} to write")
            return
        
        with open(location,'w') as f:
            json.dump(data,f,indent=2)
            
        print(f"{item.capitalize()} written to {location}")

    # @staticmethod
    def linked(self,selection,direction = 'source'):
        """ get the linked items for a selection """
    
        
        if direction == 'source':
            return [link for link in self.graph['links'] if link['source'] == selection]
        elif direction == 'target':
            return [link for link in self.graph['links'] if link['target'] == selection]
        
        else:
            return [link for link in self.graph['links'] if link['source'] == selection or link['target'] == selection]
        
        

    def walk_graph(self,sid):
        links = self.linked(sid,'source')
        
        if len(links) == 0:
            return  {
                "@extend": True
           } 
        
        output = {}
        for link in links:
            output[link['predicate']] = self.walk_graph(link['target'])
            
        return output


    def get_context(self,selection):
    # selection = 'mip:source-id'
        sid = self.graph['types'][selection]
        structure = self.walk_graph(sid)
        return json.dumps({"@context":{"@vocab":selection.replace('mip:',''),**structure}}, indent=2)
            

    def clean_entry(self,entry: Dict[str, Any], ignore: bool = False) -> Dict[str, Any]:
        """
        Clean an entry by removing certain keys and simplifying the structure.

        Args:
            entry (Dict[str, Any]): The entry to clean.
            ignore (bool): Whether to ignore certain conditions.

        Returns:
            Dict[str, Any]: The cleaned entry.
        """
        nentry = {}
        if '@id' in entry and not ignore:
            return {}
        
        if isinstance(entry, dict):
            for key, value in entry.items():
                if key[0] == '@':
                    continue
           
                if isinstance(value, (str, int, float, bool)) or value is None:
                    nentry[key] = ""  
                elif isinstance(value, dict):
                    if '@id' in value:
                        nentry[key] = {}
                    else:                        
                        cleaned_value = self.clean_entry(value, False)
                        if cleaned_value:  # Only add non-empty dictionaries
                            nentry[key] = cleaned_value
                            
                elif isinstance(value, list):
                    nentry[key] = {}
                       
                else:
                    print('-else', key, value)
        return nentry

    @property
    def generate_frames(self) -> Dict[str, Dict[str, Any]]:
        """
        Generate frames from the graph's vocabulary.

        Returns:
            Dict[str, Dict[str, Any]]: The generated frames.
        """
        frames = {}
        for k, v in self.graph['vocab'].items():
            if 'graph' in v:
                continue
            
            data = Frame(self.lddata, {"@type": f'mip:{v}', "@embed": "@always"})
            if not len(data.data):
                continue
            
            print(k, v)
            single = data.data[-1]
            cleaned = self.clean_entry(single, ignore=True)
            cleaned['@type'] = f'mip:{v}'
            cleaned['@context'] = {"@vocab": v, '@base': k}
            cleaned['@embed'] = '@always'
            cleaned['@explicit'] = True 
            frames[k] = cleaned 
        
        self.frames = frames
        return frames

    @property
    def link_frames(self) -> List[Dict[str, Any]]:
        """
        Link frames based on their relationships.

        Args:
            frames (Dict[str, Dict[str, Any]]): The frames to link.

        Returns:
            List[Dict[str, Any]]: List of failed links.
        """
        fail = []
        for select in self.frames:
            links = self.linked(select, 'source')
            if not links:
                continue
            # print(links)
            for link in links:
                try:
                    self.frames[select][link['predicate']] = self.frames[link['target']]
                except Exception as e:
                    link['error'] = str(e)
                    fail.append(link)
                    continue
        
        print("Failed links:", fail)
        
        self.failed_links = fail
        return self.frames
        
        
    def load_frame(self,frame):
        self.frames = json.load(open(frame,'r'))
        return self
    
    @property
    def filter_frames(self):
        self.get_prefix
        # select only frames that are in the repo
        self.frames = {k: v for k, v in self.frames.items() if self.prefix in k}    
        
    def update_frames(self,overwrite = True):

        self.get_prefix

        for location in self.frames:
            if self.prefix not in location:
                continue
            
            file = location.replace(self.prefix, self.repo_root+'/JSONLD/') + '/frame.jsonld'
            assert os.path.exists(file), f'No file found at {file}'
            
            if overwrite:
                # this should aready exist for there to be an LD entry
                previous = json.load(open(file,'r'))
                  
                content = sorted_dict(self.frames[location])
                if content != previous and content: 
                    with open(file, 'w') as f:   
                        json.dump(content, f, indent=4)
                        print(f'Written frame: {location} ({file})')

                    
        print(f'All frames updated sucessfully. ')

    @property
    def get_prefix(self):
        if hasattr(self,'prefix'):
            return 
        repo_root = os.popen('git rev-parse --show-toplevel').read().strip()
        repo_url = os.popen('git config --get remote.origin.url').read().strip().replace('.git', '')

        namesplit = locations.namesplit(repo_url)

        try:
            assert locations.namesplit(repo_root)[1] == namesplit[1]
        except AssertionError:
            
            print('Repositories must be registered within cmipld.locations file. \n These are:')
            for s in locations.rmap:
                print(s)
                
            sys.exit(f'You tried to submit: {locations.namesplit(repo_root)[1]} whilst expected: {namesplit[1]}')

        self.prefix = locations.rmap[namesplit]
        self.repo_root = repo_root
        


if __name__ == "__main__":
    import argparse

    def context():
        parser = argparse.ArgumentParser(description='Uses the graph.json to generate a context for a type.')
        parser.add_argument('type', type=str, help='type you want to check')
        parser.add_argument('graph', type=str, help='The file(s) to use to generate the context network.json')
        args = parser.parse_args()
        
        print(args)
        
