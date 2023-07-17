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

# pprint(r)


response_commit = requests.get("https://api.github.com/repos/iancha1992/bazel/commits/cd33d148ad31a23ba87aa59c745e3ce826dcd967")
msg_body = response_commit.json()["commit"]["message"]

print("\n\n" in msg_body)
# print(msg_body)

print(msg_body[msg_body.index("\n\n") + 2:])
