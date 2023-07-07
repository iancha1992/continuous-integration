import subprocess
from pprint import pprint

def create_pr(commit_id, pr_number, reviewers, release_number, issue_number, pr_data):
    # reviewers = [
    #     {'login': 'chaheein123', 'id': 23069091},
    #     {'login': 'pavanksingh123', 'id': 23069091},
    #     {'login': 'sunilk123', 'id': 23069091},
    # ]
    head_branch = f"iancha1992:{pr_data['target_branch_name']}"
    release_branch = pr_data["release_branch_name"]
    reviewers_str = ",".join([str(r["login"]) for r in reviewers])
    
    subprocess.run(['gh', 'pr', 'create', "--repo", "bazelbuild/bazel", "--title", "abc", "--body", "pr body!!", "--head", head_branch, "--base", release_branch,  '--label', "team-Android", '--reviewer', reviewers_str])

    print(reviewers_str)


create_pr(1, 2, [], 3, 2, 1)
