import requests

def get_issue_data(pr_number, commit_id):
    data = {}
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response_issue = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues/{pr_number}', headers=headers)
    data["title"] = response_issue.json()["title"]

    response_commit = requests.get(f"https://api.github.com/repos/iancha1992/bazel/commits/{commit_id}")
    # data["body"] = response_commit.json()["commit"]["message"]
    original_msg = response_commit.json()["commit"]["message"]
    pr_body = None
    if "\n\n" in original_msg:
        pr_body = original_msg[original_msg.index("\n\n") + 2:]
    else:
        pr_body = original_msg
    commit_str_body = "Commit https://github.com/iancha1992/bazel/commit/some_commit_id"
    if "PiperOrigin-RevId" in pr_body:
        piper_index = pr_body.index("PiperOrigin-RevId")
        pr_body = pr_body[:piper_index] + f"{commit_str_body}\n\n" + pr_body[piper_index:]
    else:
        pr_body += f"\n\n{commit_str_body}"

    data["body"] = pr_body
    return data
