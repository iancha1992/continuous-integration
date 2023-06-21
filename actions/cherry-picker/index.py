import os
from functions.check_closed import check_closed


token = os.environ["INPUT_TOKEN"]
triggered_on = os.environ["INPUT_TRIGGERED_ON"]
pr_number = os.environ["INPUT_PR_NUMBER"] if triggered_on == "closed" else os.environ["INPUT_PR_NUMBER"].split("#")[1]

print("This is prnumber!!!!!!!", pr_number)
check_closed(pr_number)

