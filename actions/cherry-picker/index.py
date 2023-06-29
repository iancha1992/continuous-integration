import os
from functions.check_closed import check_closed
from functions.get_commit_id import get_commit_id
from functions.get_reviewers import get_reviewers
from functions.extract_release_numbers_data import extract_release_numbers_data
from functions.cherry_pick import cherry_pick
from functions.create_pr import create_pr

triggered_on = os.environ["INPUT_TRIGGERED_ON"]
pr_number = os.environ["INPUT_PR_NUMBER"] if triggered_on == "closed" else os.environ["INPUT_PR_NUMBER"].split("#")[1]
# actor_name = "copybara-service[bot]";
# action_event = "closed";
# actor_name = "iancha1992"
# actor_name = "Pavank1992"
actor_name = {
    "iancha1992",
    "Pavank1992"
}
action_event = "merged"

# Check if the PR is closed.
if check_closed(pr_number) == False: raise ValueError(f'The PR #{pr_number} is not closed yet.')

# Retrieve commit_id. If doesn't exist or multiple commit id's, then raise error.
commit_id = get_commit_id(pr_number, actor_name, action_event)
print("Here is the commitid", commit_id)


# Retrieve approvers(reviewers) of the PR
reviewers = get_reviewers(pr_number)

# Retrieve release_numbers
release_numbers_data = extract_release_numbers_data(pr_number)

for k in release_numbers_data.keys():
    release_number = k
    issue_number = release_numbers_data[k]
    cherry_pick(commit_id, pr_number, reviewers, release_number, issue_number)
    # create_pr(commit_id, pr_number, reviewers, release_number, issue_number)

    # cherry_pick(commit_id, pr_number, reviewers, release_number, issue_number)