import requests, subprocess




# # 19173

# headers = {
#     'X-GitHub-Api-Version': '2022-11-28',
# }
# # url = 'https://api.github.com/repos/bazelbuild/bazel/issues/19173/comments'
# url = 'https://api.github.com/repos/bazelbuild/bazel/collaborators'

# url = "https://api.github.com/users/googlewalt/hovercard"

# r = requests.get(url, headers=headers)

# print(r.json())
# # x = requests.post(url, json = myobj)

# print(r.text)

# gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/bazelbuild/bazel/collaborators/iancha1992


# result = subprocess.run(['gh', 'api', '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', 'https://api.github.com/repos/bazelbuild/bazel/collaborators/brentleyjones'])  # Syncing
# result = subprocess.run(['gh', 'api', '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', '/users/googlewalt/hovercard'])  # Syncing


# print("~~~~~" * 100)

# result = subprocess.run(['gh', 'api', '-XGET', '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', '-F', 'per_page=100', 'repos/bazelbuild/bazel/collaborators'])
# print(result.returncode)

# print("~~~~~" * 100)

# print(result.check_returncode)


# mydict = {
#     "a": 1,
#     "b": 2
# }


# yo = mydict.copy()

# mydict["a"] = 10000





# print(yo["a"])

# headers = {
#     'X-GitHub-Api-Version': '2022-11-28',
# }
# token_headers = {
#     'X-GitHub-Api-Version': '2022-11-28',
# }





# response_check = requests.get(f"https://api.github.com/users/iancha1992/hovercard", headers=token_headers).json()
# for context in response_check["contexts"]:
#     message_keywords = context["message"].split()

#     print(message_keywords)


# print(response_check)

