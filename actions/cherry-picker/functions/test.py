import requests
from pprint import pprint

# headers = {
#     'X-GitHub-Api-Version': '2022-11-28',
#     # "owner": "bazelbuild",
#     # "repo": "bazel"
# }

# # params = {
# #     "head": "iancha1992:cp142-6.3.0",
# #     "base": "fake-release-6.3.0",
# #     "state": "all"
# # }

# params = {
#     "head": "iancha1992:cp18945",
#     "base": "release-6.3.0",
#     "state": "open"
# }


# print("~" * 60)
# r = requests.get(f'https://api.github.com/repos/bazelbuild/bazel/pulls', headers=headers, params=params).json()


pr_body = "This is the body of the PR.\r\n\r\nThank you.\r\n\r\nPiperOrigin-RevIsd: 540750474"
commit_str_body = "Commit https://github.com/iancha1992/bazel/commit/some_commit_id"

if "PiperOrigin-RevId" in pr_body:
    piper_index = pr_body.index("PiperOrigin-RevId")
    pr_body = pr_body[:piper_index] + f"{commit_str_body}\n\n" + pr_body[piper_index:]

else:
    pr_body += f"\n\n{commit_str_body}"

# print(pr_body.index("PiperOrigin-RevId"))

print(pr_body)
# print(pr_body)










