import os 

def toplevel():
    return os.popen('git rev-parse --show-toplevel').read().strip()

def ldpath(path):
    # path = f'organisations/institutions'
    toplevel = os.popen('git rev-parse --show-toplevel').read().strip()
    loc = f"{toplevel()}/JSONLD/{path}/"
    return loc


def commit_override_author(entry,where):
    if os.environ.get('OVERRIDE_AUTHOR'):
        print(f'git commit -a --author="{os.environ["OVERRIDE_AUTHOR"].strip()} <{os.environ["OVERRIDE_AUTHOR"].strip()}@users.noreply.github.com>" -m "New entry {entry} to the {where} LD file"')
        return True
    return False

def commit(message):
    os.popen(f'git commit -a -m "{message}"').read()
    
def addfile(file):
    os.popen(f'git add {file}').read()
