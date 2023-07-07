import requests

def get_issue_data(pr_number, commit_id):
    data = {}
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response_issue = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues/{pr_number}', headers=headers)
    data["title"] = response_issue.json()["title"]

    response_commit = requests.get(f"https://api.github.com/repos/iancha1992/bazel/commits/{commit_id}")
    data["body"] = response_commit.json()["commit"]["message"]

    return data
