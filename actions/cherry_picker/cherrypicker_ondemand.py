import os, re
from vars import input_data
from functions import cherry_pick, create_pr, issue_comment

milestone_title = os.environ["INPUT_MILESTONE_TITLE"]
milestoned_issue_number = os.environ["INPUT_MILESTONED_ISSUE_NUMBER"]
issue_body = os.environ["INPUT_ISSUE_BODY"]

issue_body_split = issue_body.split("\r\n")

issue_body_dict = {}

for info in issue_body_split:
    if "commit" in info.lower().split(":")[0]:
        issue_body_dict["commits"] = re.sub(r'https://.*/commit/', "", info[info.index(":") + 1:].replace(" ", "")).split(",")
        # info[info.index(":") + 1:].replace(" ", "").split(",")
        # re.sub(r'https://.*/commit/', "", url)
    elif "reviewer" in info.lower().split(":")[0]:
        issue_body_dict["reviewers"] = info[info.index(":") + 1:].replace(" ", "").replace("@", "").split(",")
    elif "team" in info.lower().split(":")[0]:
        issue_body_dict["labels"] = info[info.index(":") + 1:].replace(" ", "").replace("@", "").split(",")

print("issue_body_dict")
print(issue_body_dict)

requires_clone = True
requires_checkout = True
requires_cherrypick_push = False
for idx, commit_id in enumerate(issue_body_dict["commits"]):
    if idx >= len(issue_body_dict["commits"]) - 1: requires_cherrypick_push = True
    release_number = milestone_title.split(" release blockers")[0]
    release_branch_name = f"{input_data['release_branch_name_initials']}{release_number}"
    target_branch_name = f"cp{milestoned_issue_number}-{release_number}"
    reviewers = issue_body_dict["reviewers"]
    labels = issue_body_dict["labels"]
    pr_title_body = "Please ignore this is just testing.. Automation testing"
    try:
        cherry_pick(commit_id, release_branch_name, target_branch_name, requires_clone, requires_checkout, requires_cherrypick_push, input_data)
    # create_pr(reviewers, release_number, milestoned_issue_number, labels, haha, release_branch_name, target_branch_name, input_data["user_name"], input_data["api_repo_name"], input_data["is_prod"])
    except Exception as e:
        issue_comment(milestoned_issue_number, str(e), input_data["api_repo_name"], input_data["is_prod"])
    requires_clone = False
    requires_checkout = False
