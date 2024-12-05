from . import actions 
from . import release 
from . import repo_info
from . import tree
from .functions import *  

import re 

def extract_repo_info(github_pages_url):
    """Extract username and repository name from GitHub Pages URL."""
    pattern = r'https{0,1}://([a-zA-Z0-9-_]+)\.github\.io/([a-zA-Z0-9-_]+)/(.*)?'
    match = re.match(pattern, github_pages_url)

    if match:
        username = match.group(1)
        repo_name = match.group(2)
        path = match.group(3)
        return username, repo_name, path
    else:
        raise ValueError("Invalid GitHub Pages URL")

def io2url(github_pages_url, branch='main', path_base=''):

    username, repo_name, path = extract_repo_info(github_pages_url)
    base_url = f'https://github.com/{username}/{repo_name}/tree/{branch}/{path_base}{path}'
    
    return base_url