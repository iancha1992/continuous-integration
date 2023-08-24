import os
from vars import input_data
from functions import cherry_pick, create_pr

milestone_title = os.environ["INPUT_MILESTONE_TITLE"]
milestoned_issue_number = os.environ["INPUT_MILESTONED_ISSUE_NUMBER"]
issue_body = os.environ["INPUT_ISSUE_BODY"]
# issue_body = "@bazel-io cherry-pick\r\ncommits: xyz, abc\r\nreviewers: @iancha1992\r\nteam: team-ExternalDeps"

issue_body_split = issue_body.split("\r\n")

issue_body_dict = {}

for info in issue_body_split:
    if "commit" in info.lower().split(":")[0]:
        issue_body_dict["commits"] = info[info.index(":") + 2:].replace(" ", "").split(",")
    elif "reviewer" in info.lower().split(":")[0]:
        issue_body_dict["reviewers"] = info[info.index(":") + 2:].replace(" ", "").split(",")
    elif "team" in info.lower().split(":")[0]:
        issue_body_dict["labels"] = info[info.index(":") + 2:].replace(" ", "").split(",")

print("issue_body_dict")
print(issue_body_dict)

for commit_id in issue_body_dict["commits"]:
    release_number = milestone_title.split(" release blockers")[0]
    release_branch_name = f"{input_data['release_branch_name_initials']}{release_number}"
    target_branch_name = f"cp{milestoned_issue_number}-{release_number}"
    reviewers = issue_body_dict["reviewers"]
    labels = issue_body_dict["labels"]
    pr_title_body = "This is just testing!!!!!!!"
    cherry_pick(commit_id, release_branch_name, target_branch_name, True, input_data)
    create_pr(reviewers, release_number, milestoned_issue_number, labels, pr_title_body, release_branch_name, target_branch_name, input_data["user_name"], input_data["api_repo_name"], input_data["is_prod"])
