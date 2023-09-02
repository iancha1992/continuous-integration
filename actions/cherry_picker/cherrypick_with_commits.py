import os, re, subprocess
from vars import input_data, upstream_repo
from functions import cherry_pick, create_pr, issue_comment, get_pr_body

milestone_title = os.environ["INPUT_MILESTONE_TITLE"]
milestoned_issue_number = os.environ["INPUT_MILESTONED_ISSUE_NUMBER"]
issue_title = os.environ['INPUT_ISSUE_TITLE']
issue_body = os.environ["INPUT_ISSUE_BODY"]

issue_body_split = issue_body.split("\r\n")
issue_body_dict = {}
for info in issue_body_split:
    if "commit" in info.lower().split(":")[0]:
        issue_body_dict["commits"] = re.sub(r'https://.*/commit/', "", info[info.index(":") + 1:].replace(" ", "")).split(",")
    elif "reviewer" in info.lower().split(":")[0]:
        issue_body_dict["reviewers"] = info[info.index(":") + 1:].replace(" ", "").replace("@", "").split(",")
    elif "team" in info.lower().split(":")[0]:
        issue_body_dict["labels"] = info[info.index(":") + 1:].replace(" ", "").replace("@", "").split(",")

print("issue_body_dict", issue_body_dict)

release_number = milestone_title.split(" release blockers")[0]
release_branch_name = f"{input_data['release_branch_name_initials']}{release_number}"
target_branch_name = f"cp_ondemand_{milestoned_issue_number}-{release_number}"
head_branch_name = f"{input_data['user_name']}:{target_branch_name}"
reviewers = issue_body_dict["reviewers"]
labels = issue_body_dict["labels"]
requires_clone = True
requires_checkout = True
requires_cherrypick_push = False
successful_commits = []
failed_commits = []

for idx, commit_id in enumerate(issue_body_dict["commits"]):
    if idx >= len(issue_body_dict["commits"]) - 1: requires_cherrypick_push = True    
    try:
        cherry_pick(commit_id, release_branch_name, target_branch_name, requires_clone, requires_checkout, requires_cherrypick_push, input_data)
        msg_body = get_pr_body(commit_id, input_data["api_repo_name"])
        successful_commits = {"commit_id": commit_id, "msg": msg_body}
        successful_commits.append(commit_id)
    except Exception as e:
        failure_msg = {"commit_id": commit_id, "msg": str(e)}
        failed_commits.append(failure_msg)
    requires_clone = False
    requires_checkout = False

issue_comment_body = ""
if len(successful_commits):
    pr_body = f"This PR contains {len(successful_commits)} commit(s).\n\n"
    print(pr_body)
    for idx, commit in enumerate(successful_commits):
        pr_body += (idx + 1) + ") " + commit["msg_body"] + "\n\n"
    cherry_picked_pr_number = create_pr(reviewers, release_number, labels, issue_title, pr_body, release_branch_name, target_branch_name, input_data['user_name'])
    issue_comment_body = f"Cherry-picked in https://github.com/{upstream_repo}/pull/{cherry_picked_pr_number}. There were {len(successful_commits)} successful commits"

    success_commits_str = " ("
    for idx, success_commit in enumerate(successful_commits):
        success_commits_str += f"https://github.com/{input_data['api_repo_name']}/commit/{success_commit['commit_id']}"
        if idx < len(success_commit) - 1:
            success_commits_str += ", "
    success_commits_str += ")"

    issue_comment_body += success_commits_str

    if len(failed_commits):
        failure_commits_str = f"It also has {len(failed_commits)} failed commits, "
        for fail_commit in failed_commits:
            failure_commits_str += f"https://github.com/{input_data['api_repo_name']}/commit/{fail_commit['commit_id']} ({fail_commit['msg']})"
            if idx < len(failed_commits) - 1:
                failure_commits_str += ", "
        failure_commits_str += ", which are not included in the PR."
        issue_comment_body += failure_commits_str

else:
    issue_comment_body = "Cherry-picked failed for "
    for idx, commit in enumerate(failed_commits):
        issue_comment_body += f" {commit['commit_id']}"
        if idx < len(failed_commits) - 1:
            issue_comment_body += ", "

print("This is the issue_comment_body", issue_comment_body)
issue_comment(milestoned_issue_number, issue_comment_body, input_data["api_repo_name"], input_data["is_prod"])

