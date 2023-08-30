import os, requests
from functions import get_commit_id, get_reviewers, extract_release_numbers_data, cherry_pick, create_pr, get_labels, get_pr_body, issue_comment
from vars import input_data
from pprint import pprint

triggered_on = os.environ["INPUT_TRIGGERED_ON"]
pr_number = os.environ["INPUT_PR_NUMBER"] if triggered_on == "closed" else os.environ["INPUT_PR_NUMBER"].split("#")[1]
milestone_title = os.environ["INPUT_MILESTONE_TITLE"]
milestoned_issue_number = os.environ["INPUT_MILESTONED_ISSUE_NUMBER"]

issue_data = requests.get(f"https://api.github.com/repos/{input_data['api_repo_name']}/issues/{pr_number}", headers={'X-GitHub-Api-Version': '2022-11-28'}).json()

print("This is the issuedata!")
pprint(issue_data)

# Check if the PR is closed.
if issue_data["state"] != "closed": raise Exception(f'The PR #{pr_number} is not closed yet.')

# Retrieve commit_id. If the PR/issue has no commit or has multiple commits, then raise an error.
commit_id = get_commit_id(pr_number, input_data["actor_name"], input_data["action_event"], input_data["api_repo_name"])

# Retrieve approvers(reviewers) of the PR
reviewers = get_reviewers(pr_number, input_data["api_repo_name"], issue_data)

# Retrieve release_numbers
if triggered_on == "closed":
    release_numbers_data = extract_release_numbers_data(pr_number, input_data["api_repo_name"])
elif triggered_on == "commented":
    release_numbers_data = {milestone_title.split(" release blockers")[0]: milestoned_issue_number}

# Retrieve labels
labels = get_labels(pr_number, input_data["api_repo_name"])

# Retrieve issue/PR's title and body
pr_body = get_pr_body(commit_id, input_data["api_repo_name"])

# Perform cherry-pick and then create a pr if it's successful.
requires_clone = True
for k in release_numbers_data.keys():
    release_number = k
    release_branch_name = f"{input_data['release_branch_name_initials']}{release_number}"
    target_branch_name = f"cp{pr_number}-{release_number}"
    issue_number = release_numbers_data[k]
    pr_title = issue_data["title"]
    try:
        cherry_pick(commit_id, release_branch_name, target_branch_name, requires_clone, True, True, input_data)
        create_pr(reviewers, release_number, issue_number, labels, pr_title, pr_body, release_branch_name, target_branch_name, input_data["user_name"], input_data["api_repo_name"], input_data["is_prod"])
    except Exception as e:
        issue_comment(issue_number, str(e), input_data["api_repo_name"], input_data["is_prod"])
    requires_clone = False
