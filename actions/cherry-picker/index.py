import os
from functions.check_closed import check_closed
from functions.get_commit_id import get_commit_id

token = os.environ["INPUT_TOKEN"]
triggered_on = os.environ["INPUT_TRIGGERED_ON"]
pr_number = os.environ["INPUT_PR_NUMBER"] if triggered_on == "closed" else os.environ["INPUT_PR_NUMBER"].split("#")[1]
# actor_name = "copybara-service[bot]";
# action_event = "closed";
actor_name = "iancha1992"
action_event = "merged"

# Check if the PR is closed.
if check_closed(pr_number) == False: raise ValueError(f'The PR #{pr_number} is not closed yet.')

# Retrieve commit_id. If doesn't exist or multiple commit id's, then raise error.
commit_id = get_commit_id(pr_number, actor_name, action_event)
print("Here is the commitid", commit_id)


# Retrieve approvers(reviewers) of the PR
