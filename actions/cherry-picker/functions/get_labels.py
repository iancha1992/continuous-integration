import requests

def get_labels(pr_number):
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues/{pr_number}/labels', headers=headers)
    return(list(map(lambda x: x["name"], r.json())))
