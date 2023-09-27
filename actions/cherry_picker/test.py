# import re
# # from vars import cherrypick_with_commits_infos
# def get_middle_text(all_str, left_str, right_str):
#     left_index = all_str.index(left_str) + len(left_str)
#     if right_str == None:
#         right_index = len(all_str)
#     else:
#         right_index = all_str.index(right_str)
#     # print(all_str[left_index:right_index])
#     return all_str[left_index:right_index]

# cherrypick_with_commits_infos = {
#     "commits": {
#         "left": "If multiple, then please separate by commas. Example: 9e90a6, f1da12\n\n\n",
#         "right": "\n\n### Which category",
#     },
#     "team_labels": {
#         "left": "Which category does this issue belong to?\n\n\n",
#         "right": "\n\n### Please provide the reviewers"
#     },
#     "reviewers": {
#         "left": "Please provide the reviewers of the PR once it is created after cherry-picking. Example: @iancha1992, @keertk\n\n\n",
#         "right": None
#     }
# }


# commits_text = cherrypick_with_commits_infos["commits"]
# team_labels_text = cherrypick_with_commits_infos["team_labels"]
# reviewers_text = cherrypick_with_commits_infos["reviewers"]

# issue_body = "### Please put the commit IDs (at least first 6 digits of the commit IDs). If multiple, then please separate by commas. Example: 9e90a6, f1da12\n\n\nhttps://github.com/iancha1992/bazel/commit/a2b775467c1b36bd1c935d35770916105cd7102d,79a0dc276cc81717ac2951d575e19f6a54d71e43,  https://github.com/iancha1992/bazel/commit/98d5d5f6980ec8513dc5c0ee95fcabe3b80beb47\n\n### Which category does this issue belong to?\n\n\nteam-OSS, team-Bazel, z-team-Apple, team-Rules-CPP\n\n### Please provide the reviewers of the PR once it is created after cherry-picking. Example: @iancha1992, @keertk\n\n\n@chaheein123"


# # hello = re.sub(r'https://.*/commit/', "", get_middle_text(issue_body, commits_text["left"], commits_text["right"])).replace(" ", "").split(",")

# hello = get_middle_text(issue_body, reviewers_text["left"], reviewers_text["right"]).replace(" ", "").split(",")
# print(hello)
# # result = map(lambda x: x)

# # aye = re.sub(r'https://.*/commit/', "", hello)

# # print(aye)

# # for index, value in enumerate(hello):
# #     print(index)
# #     hello[index] = re.sub(r'https://.*/commit/', "", hello[index])

# #     # i = re.sub(r'https://.*/commit/', "", i)

# # print(hello)
mystr = "abcde"
print(mystr[::-1])


