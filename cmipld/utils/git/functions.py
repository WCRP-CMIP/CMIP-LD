from . import functions 
from . import add



def update_env(key,value):
    import os
    github_env_file = os.environ.get("GITHUB_ENV") 

    with open(github_env_file, "a") as env_file:
        env_file.write(f"{key}={value}\n")


def update_summary(md):
    import os
    github_env_file = os.environ.get("GITHUB_STEP_SUMMARY") 

    with open(github_env_file, "a") as summary:
        summary.write(f"{md}\n")
        
        
        
def update_issue_title (issue_number,kind,payload):
    # change issue name to reflect contents. 
    print(os.popen(f'gh issue edit {issue_number} --title "Add {kind}: {payload["client_payload"]["name"]}"').read())


def update_issue(issue_number,comment,err=True):
    out = os.popen(f'gh issue comment {issue_number} --body "{comment}"')
    if err: 
        print(out)
        sys.exit(comment)

def close_issue(issue_number, comment,err=True):
    print(os.popen(f'gh issue close {issue_number} -c "{comment}"'))
    if err: sys.exit(comment)
    
def jr(file):
    return json.load(open(file,'r'))

def jw(data,file):
    return json.dump(data,open(file,'w'), indent=4)

def getfile(fileend):
    import glob
    return glob.glob(f'*{fileend}.json')

def pp(js):
    import pprint
    pprint.pprint(js)