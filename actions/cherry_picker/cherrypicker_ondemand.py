import os

issue_body = os.environ["INPUT_ISSUE_BODY"]
# issue_body = "@bazel-io cherry-pick\r\ncommits: xyz, abc\r\nreviewers: @iancha1992\r\nteam: team-ExternalDeps"

print("ONDEMAND LUNCH!")
print("issue_body")
print("banana")
print(issue_body)


if "\n" in issue_body:
    print("candy!!!")


