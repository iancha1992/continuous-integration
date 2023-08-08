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

result = subprocess.run(['gh', 'api', '-XGET', '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', '-F', 'per_page=100', 'repos/bazelbuild/bazel/collaborators'])
# print(result.returncode)

# print("~~~~~" * 100)

print(result.check_returncode)

# team_labels = ["team-CLI", "P3", "team-OSS", "team-Core", "P1", "team-Bazel", "team-Android", "area-java"]


# labels_list = list(filter(lambda label: "area" in label or "team" in label, team_labels))



