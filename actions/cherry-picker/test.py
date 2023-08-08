import requests, subprocess




# # 19173

# headers = {
#     'X-GitHub-Api-Version': '2022-11-28',

# }
# # url = 'https://api.github.com/repos/bazelbuild/bazel/issues/19173/comments'
# url = 'https://api.github.com/repos/bazelbuild/bazel/collaborators'

# r = requests.get(url, headers=headers)
# # x = requests.post(url, json = myobj)

# print(r.text)

# gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/repos/bazelbuild/bazel/collaborators/iancha1992


# result = subprocess.run(['gh', 'api', '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', 'https://api.github.com/repos/bazelbuild/bazel/collaborators/brentleyjones'])  # Syncing

print("~~~~~" * 100)

result = subprocess.run(['gh', 'api', '-XGET', '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', '-F', 'per_page=100', '-F', 'permission=admin', 'repos/bazelbuild/bazel/collaborators'])
# print(result.returncode)print

# print("~~~~~" * 100)