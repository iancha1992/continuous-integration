import os
from functions import check_closed, get_commit_id, get_reviewers, extract_release_numbers_data, cherry_pick, create_pr, get_labels, get_issue_data

triggered_on = os.environ["INPUT_TRIGGERED_ON"]
pr_number = os.environ["INPUT_PR_NUMBER"] if triggered_on == "closed" else os.environ["INPUT_PR_NUMBER"].split("#")[1]
milestone_title = os.environ["INPUT_MILESTONE_TITLE"]
milestoned_issue_number = os.environ["INPUT_MILESTONED_ISSUE_NUMBER"]
is_prod = os.environ["INPUT_IS_PROD"]

if is_prod == "true":
    input_data = {
        "is_prod": True,
        "gh_cli_repo_name": "bazelbuild/bazel",
        "master_branch": "master",
        "release_branch_name_initials": "release-",
        "user_name": "bazel-io",
        "action_event": "closed",
        "actor_name": {
            "copybara-service[bot]"
        }
    }

else:
    input_data = {
        "is_prod": False,
        "gh_cli_repo_name": "iancha1992/bazel",
        "master_branch": "release_test",
        "release_branch_name_initials": "fake-release-",
        "user_name": "iancha1992",
        "action_event": "merged",
        "actor_name": {
            "iancha1992",
            "Pavank1992",
            "chaheein123",
        }
    }

# Check if the PR is closed.
if check_closed(pr_number, input_data["gh_cli_repo_name"]) == False: raise ValueError(f'The PR #{pr_number} is not closed yet.')

# Retrieve commit_id. If doesn't exist or multiple commit id's, then raise error.
commit_id = get_commit_id(pr_number, input_data["actor_name"], input_data["action_event"], input_data["gh_cli_repo_name"])

# Retrieve approvers(reviewers) of the PR
reviewers = get_reviewers(pr_number, input_data["gh_cli_repo_name"])

# Retrieve release_numbers
if triggered_on == "closed":
    release_numbers_data = extract_release_numbers_data(pr_number, input_data["gh_cli_repo_name"])
else:
    release_numbers_data = {milestone_title.split(" release blockers")[0]: milestoned_issue_number}

# Retrieve labels
labels = get_labels(pr_number, input_data["gh_cli_repo_name"])

# Retrieve issue/PR's title and body
issue_data = get_issue_data(pr_number, commit_id, input_data["gh_cli_repo_name"])

is_first_time = True
for k in release_numbers_data.keys():
    release_number = k
    release_branch_name = f"{input_data['release_branch_name_initials']}{release_number}"
    target_branch_name = f"cp{pr_number}-{release_number}"
    issue_number = release_numbers_data[k]
    try:
        cherrypick_status = cherry_pick(commit_id, release_branch_name, target_branch_name, issue_number, is_first_time, input_data)
    except:
        cherrypick_status = 1
    if cherrypick_status == 0:
        create_pr(reviewers, release_number, issue_number, labels, issue_data, release_branch_name, target_branch_name, input_data["user_name"])
    is_first_time = False
