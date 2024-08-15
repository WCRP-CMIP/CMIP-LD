from . import functions 
from . import add



def update_env(key,value):
   
    github_env_file = "/home/runner/work/_temp/_runner_file/_github_env"  # Temporary path used by GitHub Actions

    with open(github_env_file, "a") as env_file:
        env_file.write(f"{key}={value}\n")
