from . import functions 
from . import add
import os, subprocess
from typing import List, Dict, Any, Tuple

def update_env(key,value):
    import os
    github_env_file = os.environ.get("GITHUB_ENV") 

    with open(github_env_file, "a") as env_file:
        env_file.write(f"{key}={value}\n")





def update_summary(md):
    import os
    if "GITHUB_STEP_SUMMARY" in os.environ:
        github_env_file = os.environ.get("GITHUB_STEP_SUMMARY") 

        with open(github_env_file, "a") as summary:
            summary.write(f"{md}\n")
    else:
        print(md)
        

        
def update_issue_title (what):
    # change issue name to reflect contents. 
    if 'ISSUE_NUMBER' in os.environ:
        issue_number = os.environ['ISSUE_NUMBER']
        print(os.popen(f'gh issue edit {issue_number} --title "{what}"').read())
        # : {payload["client_payload"]["name"]}"
    print(f"Title Updated: {what}")


def update_issue(comment,err=True,summarize=True):
    if 'ISSUE_NUMBER' in os.environ:
        issue_number = os.environ['ISSUE_NUMBER']
        out = os.popen(f'gh issue comment {issue_number} --body \'{comment}\' ').read()
        if summarize:
            update_summary(comment)
        if err: 
            print(out)
            raise ValueError(comment)
        
    
    print(comment)


def close_issue(issue_number, comment,err=True):
    if 'ISSUE_NUMBER' in os.environ:
        issue_number = os.environ['ISSUE_NUMBER']
        print(os.popen(f'gh issue close {issue_number} -c "{comment}"'))
        if err: 
            raise ValueError(comment)
            # sys.exit(comment)
    
    print(comment)
    
    
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
    
    
    
def prepare_pull(feature_branch,base_branch):
    issue_number = os.environ['ISSUE_NUMBER']
    if issue_number:
        feature_branch = f'{feature_branch}-{issue_number}'
        cmd = f'''
            base_branch="{base_branch}"
            feature_branch="{feature_branch}"
            git pull
                
            remote_branch='origin/{feature_branch}'
            branch_info=$(git rev-parse --verify '$remote_branch' >/dev/null 2>&1 || true)
            echo "branch info: $branch_info"
            
            if [ -n "$branch_info" ]; then
                echo "checkout existing"
                git checkout {feature_branch}
                git reset --hard origin/main
            else
                echo "checkout new"
                git checkout -b {feature_branch}
            fi
            
            git push origin {feature_branch} -f 
                '''
        print(os.popen(cmd).read())
        return feature_branch
    return False
    
    



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

def commit_one(location,author,comment,branch=None):
    print(os.popen(f'git add {location}').read())
    print(os.popen(f'git commit -a --author="{author} <{author}@users.noreply.github.com>" -m "{comment}"').read())
    if branch:
        print(os.popen(f'git push origin {branch} --force').read())
    else:
        print(os.popen(f'git push').read())
    


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



def reset_branch(branch):
    # if a branch exists, reset it to main, then progress. 
    




def pull_req(content,feature_branch, req_author):
    # gh_token, issue, base_branch
    # Set git configuration
    subprocess.run(['git', 'config', '--global', 'user.email', f'{req_author}@users.noreply.github.com'])
    subprocess.run(['git', 'config', '--global', 'user.name', req_author])


    # remote_branch=f'origin/{feature_branch}'
    
    branchinfo= os.popen("$(git rev-parse --verify '{feature_branch}' >/dev/null 2>&1 || true)").read()
    
    print('---', branchinfo)
    update_issue(f'Branch Info: {branchinfo}',False)
    
    # cmds= [
    #     f"git checkout {branch}",
    #     f"git reset --hard origin/main",
    # ]
    
    
    


#     # Check if branch_info exists (not provided in the function parameters, assuming it's a global variable)
#     if 'branch_info' in globals() and branch_info:
#         # Get open pull requests
#         api_url = f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/pulls?state=open&head={branch}'
#         headers = {'Authorization': f'token {gh_token}'}
#         response = subprocess.run(['curl', '-s', '-H', f'Authorization: token {gh_token}', api_url], capture_output=True, text=True)
#         pull_requests = json.loads(response.stdout)
        
#         for pr in pull_requests:
#             pr_number = pr['number']
#             comment_body = f"""This pull request (#{pr_number}) was automatically updated by a GitHub Actions workflow.

# Data submitted by @{req_author}

# Adding the following updated data.

# ```js
# {content}