import os
from vars import input_data
from functions import cherry_pick

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
    cherry_pick(commit_id, release_branch_name, target_branch_name, True, input_data)
