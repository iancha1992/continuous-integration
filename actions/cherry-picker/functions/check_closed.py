import requests
from pprint import pprint

def check_closed(pr_number):
    print("Closing!")
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/pulls/{pr_number}', headers=headers)
    print("Dataha")
    print(r.json()["state"])
    if r.json().state == "closed":
        print("ITS CLOSED")
        return True
    return False
