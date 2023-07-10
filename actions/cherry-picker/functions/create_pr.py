import subprocess
from pprint import pprint

def create_pr(commit_id, pr_number, reviewers, release_number, issue_number, labels, issue_data, pr_data):
    head_branch = f"iancha1992:{pr_data['target_branch_name']}"
    release_branch = pr_data["release_branch_name"]
    reviewers_str = ",".join([str(r["login"]) for r in reviewers])
    labels_str = ",".join(labels)
    pr_title = issue_data["title"]
    pr_body = f"[{release_number}] {issue_data['body']}"
    # subprocess.run(["gh", "repo", "set-default"])
    status_create_pr = subprocess.run(['gh', 'pr', 'create', "--repo", "bazelbuild/bazel", "--title", pr_title, "--body", pr_body, "--head", head_branch, "--base", release_branch,  '--label', labels_str, '--reviewer', reviewers_str])
    print("status_create_pr", status_create_pr)
    # print("status_create_pr", status_create_pr)
    if status_create_pr.returncode != 0:
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "PR failed to be created."])
    else:
        print("PR was successfully created")
        # subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', f"Cherry-pick in https://github.com/bazelbuild/bazel/pull/"])
