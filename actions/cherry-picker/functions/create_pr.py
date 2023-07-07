import subprocess
from pprint import pprint

def create_pr(commit_id, pr_number, reviewers, release_number, issue_number, labels, issue_data, pr_data):
    head_branch = f"iancha1992:{pr_data['target_branch_name']}"
    release_branch = pr_data["release_branch_name"]
    reviewers_str = ",".join([str(r["login"]) for r in reviewers])
    labels_str = ",".join(labels)
    pr_title = issue_data["title"]
    pr_body = issue_data["body"]
    
    subprocess.run(['gh', 'pr', 'create', "--repo", "bazelbuild/bazel", "--title", pr_title, "--body", pr_body, "--head", head_branch, "--base", release_branch,  '--label', labels_str, '--reviewer', reviewers_str])
