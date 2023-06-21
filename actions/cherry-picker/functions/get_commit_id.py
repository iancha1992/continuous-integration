import requests
from pprint import pprint

def get_commit_id(pr_number, actor_name, action_event):
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    params = {
        "per_page": 100
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues/{pr_number}/events', headers=headers, params=params)
    print("getcommitiddd")
    pprint(r.json())

    commit_id = None

    for event in r.json():
        if (event["actor"]["login"] == actor_name) and (event["commit_id"] != None) and (commit_id == None) and (event["event"] == action_event):
            commit_id = event["commit_id"]
        elif (event["actor"]["login"] == actor_name) and (event["commit_id"] != None) and (commit_id != None) and (event["event"] == action_event):
            raise ValueError(f'PR#{pr_number} has multiple commits by {actor_name}')
    
    if commit_id == None: raise ValueError(f'PR#{pr_number} has NO commit made by {actor_name}')

    return commit_id