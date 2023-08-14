import requests, subprocess
from pprint import pprint

headers = {
    'X-GitHub-Api-Version': '2022-11-28',
}



# git shortlog -s -n -e


# # url = 'https://api.github.com/repos/bazelbuild/bazel/issues/19173/comments'
# url = 'https://api.github.com/repos/bazelbuild/bazel/collaborators'

# url = "https://api.github.com/users/iancha1992/social_accounts"

# url = "https://api.github.com/users/iancha1992/social_accounts"

url = "https://api.github.com/users/haxorz/events/public"

# r = requests.get(url, headers=headers)

# print("*" * 150)
# pprint(r.json(), depth=100000)





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

# hi = []

# bye = ",".join(hi)

# print(bye)

upstream_url = "https://github.com/bazelbuild/bazel.git"



hi = upstream_url.split("https://github.com/")[1].replace(".git", "")

print(hi)