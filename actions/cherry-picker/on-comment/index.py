import os
token = os.environ["INPUT_TOKEN"]
pr_number = os.environ["INPUT_PR_NUMBER"]
triggered_on = os.environ["INPUT_TRIGGERED_ON"]

print("This is the payload!")
print(pr_number)

