import json
import re
import argparse
from typing import Any, Dict, List, Union, Set
from functools import lru_cache
from urllib.parse import urljoin
from pyld import jsonld

from .interactive import open_jless_with_memory

from ..locations import mapping
matches =re.compile(f"({'|'.join(mapping.keys())})")

class JsonLdProcessor:
    """
    A class for processing JSON-LD documents with recursive expansion and ID resolution.
    
    Features:
    - Recursively expands and resolves @id fields containing URLs
    - Handles document caching
    - Supports compact and expanded document formats
    - Maintains context handling
    - Extracts document dependencies
    """
    
    def __init__(self):
        """Initialize the processor with a cached document loader."""
        self.loader = jsonld.requests_document_loader()
    
    @staticmethod
    def _extract_base_url(url: str) -> str:
        """
        Extract the base URL from a full URL path.
        
        Args:
            url: The full URL to process
            
        Returns:
            The base URL containing protocol and domain
        """
        parts = url.split('/')
        return '/'.join(parts[:3])
    
    @lru_cache(maxsize=100)
    def _load_document(self, url: str) -> Dict:
        """
        Load and cache a JSON-LD document from a URL.
        
        Args:
            url: The URL to fetch the document from
            
        Returns:
            The loaded document
        """
        return self.loader(url)['document']
    
    def _resolve_ids(self, 
                     data: Union[Dict, List], 
                     compact: bool = True) -> Union[Dict, List]:
        """
        Recursively resolve @id fields in the document.
        
        Args:
            data: The data structure to process
            compact: Whether to compact the resulting document
            
        Returns:
            The processed data structure with resolved IDs
        """
        if isinstance(data, dict):
            if '@id' in data and not '@type' in data and data['@id'].startswith('http'):
                
                # print('!!!',data['@id'])
                
                try:
                    expanded = self.expand_document(
                        data['@id'],
                        compact=compact,
                        is_nested=True
                    )
                except jsonld.JsonLdError:
                    print('\n WARNING missing id: ',data['@id'])
                    expanded = None
                if expanded:
                    data = expanded[0]
            
            return {
                key: self._resolve_ids(value, compact)
                for key, value in data.items()
            }
        
        elif isinstance(data, list):
            return [self._resolve_ids(item, compact) for item in data]
        
        return data
    
    def extract_dependencies(self, url: str, relative: bool = False) -> Set[str]:
        """
        Extract all dependencies (@id references) from a JSON-LD document.
        
        Args:
            url: URL of the JSON-LD document
            relative: If True, returns relative URLs, if False returns absolute URLs
            
        Returns:
            Set of dependency URLs found in the document
        """
        try:
            # Frame the document to extract all @id references
            framed = jsonld.frame(url, {'@explicit': True}, options={'defaultLoader': self.loader})
            ids = framed.get('@graph', [])
            
            # Process URLs based on relative flag
            if relative:
                return {item['@id'] for item in ids if '@id' in item}
            else:
                return {urljoin(url, item['@id']) for item in ids if '@id' in item}
                
        except Exception as e:
            print(f"Error extracting dependencies: {str(e)}")
            return set()
    
    
    def depends(self,query,**kwargs):
        print(kwargs)
        # if arg in locations, then use that and give that level. 
        query = self.replace_prefix(query)
        return self.extract_dependencies(query,**kwargs)
    
    @staticmethod
    def replace_prefix(query):        
        m = matches.search(query+':')
        if m:
            match = m.group()
            if len(match)-1 == len(query):
                query = f"{mapping[match]}graph.jsonld"
            else:
                query = query.replace(match, mapping[match])
            print('Substituting prefix:')
            print(match,query)
        return query
    
    def get(self,query,**kwargs):
        query = self.replace_prefix(query)
        return self.expand_document(query,**kwargs)
    
    def expand_document(self,
                       jsonld_doc: Union[str, Dict],
                       compact: bool = True,
                       expand_ctx: bool = True,
                       expand_links: bool = True,
                       is_nested: bool = False) -> List[Dict]:
        """
        Expand a JSON-LD document and resolve all referenced URLs.
        
        Args:
            jsonld_doc: The JSON-LD document to process (URL or dict)
            compact: Whether to compact the final document
            expand_ctx: Whether to expand the context
            expand_links: Whether to expand linked documents
            is_nested: Whether this is a nested expansion
            
        Returns:
            List of processed documents
        """
        doc = self._load_document(jsonld_doc) if isinstance(jsonld_doc, str) else jsonld_doc
        
        expanded = jsonld.expand(jsonld_doc, options={'defaultLoader': self.loader})
        
        processed = []
        for item in expanded:
            if expand_links:
                processed_item = self._resolve_ids(item, compact).copy()
            else:
                processed_item = item.copy()
            
            if compact and not is_nested:
                base_url = self._extract_base_url(jsonld_doc) if isinstance(jsonld_doc, str) else None
                processed_item = jsonld.compact(
                    processed_item,
                    doc['@context'],
                    options={'base': base_url} if base_url else {}
                )
            
            if isinstance(processed_item, dict):
                processed_item = json.loads(
                    re.sub(r'"context"', '"@context"', json.dumps(processed_item))
                )
            
            if expand_ctx and '@context' in processed_item and isinstance(processed_item['@context'], str):
                processed_item['@context'] = self.loader(processed_item['@context'])['document']
                
            processed.append(processed_item)
        
        return processed


    def find_missing(self,url):
        '''
        Get all the references in an LD object, 
        and check if they exist.
        '''
        from tqdm import tqdm
        from ..utils.urltools import url_exists
        
        links = self.depends(url)
        missing = [link for link in tqdm(links) if not url_exists(link)]
        
        return missing

# LOCATION>S.MAPPING


