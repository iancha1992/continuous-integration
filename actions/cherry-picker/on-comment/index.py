import os
token = os.environ["INPUT_TOKEN"]
payload = os.environ["PAYLOAD"]
triggered_on = os.environ["INPUT_TRIGGERED_ON"]

print("This is the payload!")
print(payload)