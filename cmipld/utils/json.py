from collections import OrderedDict


class DotAccessibleDict:
    def __init__(self, entries):
        self.entries = dict(entries)
        for key in self.entries.keys():
            self.__dict__[key] = self.entries[key]

    # def __getattr__(self, name):
    #     if name in self.entries:
    #         return self.entries[name]
    #     else:
    #         raise AttributeError(f"'DotAccessibleDict' object has no attribute '{name}'")

    def __str__(self):
        return str(self.entries.keys())
    

def sorted_json(dct):
    """
    Sort a dictionary by keys and return an OrderedDict.

    Args:
    dct (dict): The input dictionary to be sorted.

    Returns:
    OrderedDict: A new OrderedDict with items sorted by keys.
    """
    if not isinstance(dct, dict):
        return dct
    
    od = OrderedDict()
    keys = ['@context','id','type']
    for i in keys:
        if i in dct:
            od[i] = dct[i]
    for key in sorted(dct.keys()):
        if key not in keys:
            od[key] = dct[key]
            
    return od
    
    # return sorted((k, v) for k, v in dct.items()))
    
    

def sorted_ctx(dct):
    """
    Sort a dictionary by keys and return an OrderedDict.

    Args:
    dct (dict): The input dictionary to be sorted.

    Returns:
    OrderedDict: A new OrderedDict with items sorted by keys.
    """
    assert isinstance(dct, dict)
    assert '@context' in dct
    
    ctx = OrderedDict()
    
    # lddefinitions
    for ck,cv in sorted(dct['@context'].items()):
        if ck[0] == '@':
            ctx[ck] = cv
    
    # ld objects
    for ck,cv in sorted(dct['@context'].items()):
        if isinstance(cv,str) and cv[0] == '@':
            ctx[ck] = cv
            
    
    # prefix
    for ck,cv in sorted(dct['@context'].items()):
        if ck[-1] == ':':
            ctx[ck] = cv
            
            
    # others
    
    # non context items
    for ck,cv in sorted(dct['@context'].items()):
        if '@context' not in cv:
            ctx[ck] = cv
            
    # context items (links)
    for ck,cv in sorted(dct['@context'].items()):
        if '@context' in cv:
            ctx[ck] = cv
            
    dct['@context'] = ctx
    dct['@embed'] = '@always'
    return dct
    