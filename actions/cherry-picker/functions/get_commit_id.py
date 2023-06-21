import requests
def get_commit_id(pr_number):
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    params = {
        "per_page": 100
    }
    r = requests.get(f'https://api.github.com/repos/repos/iancha1992/bazel/issues/{pr_number}/events', headers=headers, params=params)
    print("getcommitiddd")
    print(r.text)