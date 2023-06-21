import requests
from pprint import pprint

def check_closed(pr_number):
    print("Closing!")
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/pulls/{pr_number}', headers=headers)
    print("Dataha")
    pprint(r.json())
    if r.json().state == "closed": return True
    return False
