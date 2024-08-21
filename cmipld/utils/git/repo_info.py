import os, subprocess

from typing import List, Dict, Any, Tuple


def toplevel():
    return os.popen('git rev-parse --show-toplevel').read().strip()

def ldpath(path):
    # path = f'organisations/institutions'
    loc = os.path.abspath(f"{toplevel()}/JSONLD/{path}/")
    return loc

def url():
    return subprocess.getoutput('git remote get-url origin').replace('.git', '').strip()

def commit_override_author(entry,where):
    if os.environ.get('OVERRIDE_AUTHOR'):
        print(f'git commit -a --author="{os.environ["OVERRIDE_AUTHOR"].strip()} <{os.environ["OVERRIDE_AUTHOR"].strip()}@users.noreply.github.com>" -m "New entry {entry} to the {where} LD file"')
        return True
    return False

def commit(message):
    os.popen(f'git commit -a -m "{message}"').read()
    
def addfile(file):
    os.popen(f'git add {file}').read()



def get_cmip_repo_info() -> Tuple[str, str, str]:
    """Retrieve repository information and tags."""
    repo = subprocess.getoutput('git remote get-url origin').replace('.git', '/blob/main/JSONLD').strip()
    cv_tag = subprocess.getoutput("curl -s https://api.github.com/repos/WCRP-CMIP/CMIP6Plus_CVs/tags | jq -r '.[0].name'").strip()
    mip_tag = subprocess.getoutput("curl -s https://api.github.com/repos/PCMDI/mip-cmor-tables/tags | jq -r '.[0].name'").strip()
    return repo, cv_tag, mip_tag