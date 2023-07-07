import subprocess
from pprint import pprint

def create_pr(commit_id, pr_number, reviewers, release_number, issue_number, labels, issue_data, pr_data):
    reviewers = [
        {'login': 'chaheein123', 'id': 23069091},
        {'login': 'pavanksingh123', 'id': 23069091},
        {'login': 'sunilk123', 'id': 23069091},
    ]
    labels = []
    head_branch = f"iancha1992:{pr_data['target_branch_name']}"
    release_branch = pr_data["release_branch_name"]
    reviewers_str = ",".join([str(r["login"]) for r in reviewers])
    labels_str = ",".join(labels)
    
    # subprocess.run(['gh', 'pr', 'create', "--repo", "bazelbuild/bazel", "--title", "abc", "--body", "pr body!!", "--head", head_branch, "--base", release_branch,  '--label', "team-Android", '--reviewer', reviewers_str])

    print(reviewers_str)
    print(labels_str)


create_pr(1, 2, [], 3, 2, [], 1)
