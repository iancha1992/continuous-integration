import requests
from pprint import pprint

def get_reviewers(pr_number):
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/pulls/{pr_number}/reviews', headers=headers)
    print("This is the reviewers")
    pprint(r.json())
    if len(r.json()) == 0: raise ValueError(f"PR#{pr_number} has no approver.")
    approvers_list = []
    for review in r.json():
        if review["state"] == "APPROVED":
            data = {
                "login": review.user.login,
                "id": review.user.id
            }
            approvers_list.append(data)
    if len(approvers_list) == 0:
        raise ValueError(f"PR#{pr_number} has no approver.")
    
    return approvers_list
