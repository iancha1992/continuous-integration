import subprocess
import requests
from pprint import pprint

def send_pr_msg(issue_number, head_branch, release_branch):
    headers = {
        'X-GitHub-Api-Version': '2022-11-28',
    }
    # params = {
    #     "head": "iancha1992:cp142-6.3.0",
    #     "base": "fake-release-6.3.0",
    #     "state": "open"
    # }

    params = {
        "head": head_branch,
        "base": release_branch,
        "state": "open"
    }

    r = requests.get(f'https://api.github.com/repos/bazelbuild/bazel/pulls', headers=headers, params=params).json()
    if len(r) == 1:
        cherry_picked_pr_number = r[0]["number"]
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', f"Cherry-pick in https://github.com/bazelbuild/bazel/pull/{cherry_picked_pr_number}"])
    else:
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "Failed to send PR msg"])

def create_pr(reviewers, release_number, issue_number, labels, issue_data, pr_data):
    head_branch = f"iancha1992:{pr_data['target_branch_name']}"
    release_branch = pr_data["release_branch_name"]
    reviewers_str = ",".join([str(r["login"]) for r in reviewers])
    if "awaiting-review" not in labels:
        labels.append("awaiting-review")
    labels_str = ",".join(labels)
    pr_title = f"[{release_number}] {issue_data['title']}"
    pr_body = issue_data['body']
    # subprocess.run(["gh", "repo", "set-default"])
    status_create_pr = subprocess.run(['gh', 'pr', 'create', "--repo", "bazelbuild/bazel", "--title", pr_title, "--body", pr_body, "--head", head_branch, "--base", release_branch,  '--label', labels_str, '--reviewer', reviewers_str])
    print("status_create_pr", status_create_pr)
    # print("status_create_pr", status_create_pr)
    if status_create_pr.returncode != 0:
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "PR failed to be created."])
    else:
        print("PR was successfully created")
        # send_pr_msg(issue_number, head_branch, release_branch)
