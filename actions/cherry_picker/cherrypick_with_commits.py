import os, re
from vars import input_data, upstream_repo
from functions import cherry_pick, create_pr, issue_comment, get_pr_body, GeneralCpException, PushCpException, push_to_branch

print("NEW TESTING")
milestone_title = os.environ["INPUT_MILESTONE_TITLE"]
milestoned_issue_number = os.environ["INPUT_MILESTONED_ISSUE_NUMBER"]
issue_title = os.environ['INPUT_ISSUE_TITLE']
issue_body = os.environ["INPUT_ISSUE_BODY"]

issue_body_split = issue_body.split("\r\n")
issue_body_dict = {}
for info in issue_body_split:
    if "commits:" in info:
        commits_url_list = info.replace("commits:", "").replace(" ", "").split(",")
        issue_body_dict["commits"] = []
        for commit_url in commits_url_list:
            c_id = re.sub(r'https://.*/commit/', "", commit_url)
            issue_body_dict["commits"].append(c_id)
    elif "reviewers:" in info:
        issue_body_dict["reviewers"] = info.replace("reviewers:", "").replace(" ", "").replace("@", "").split(",")
    elif "teams:" in info:
        issue_body_dict["labels"] = info.replace("teams:", "").replace(" ", "").replace("@", "").split(",")

print("issue_body_dict", issue_body_dict)

release_number = milestone_title.split(" release blockers")[0]
release_branch_name = f"{input_data['release_branch_name_initials']}{release_number}"
target_branch_name = f"cp_ondemand_{milestoned_issue_number}-{release_number}"
head_branch_name = f"{input_data['user_name']}:{target_branch_name}"
reviewers = issue_body_dict["reviewers"]
labels = issue_body_dict["labels"]
requires_clone = True
requires_checkout = True
successful_commits = []
failed_commits = []

for idx, commit_id in enumerate(issue_body_dict["commits"]):
    try:
        cherry_pick(commit_id, release_branch_name, target_branch_name, requires_clone, requires_checkout, input_data)
        msg_body = get_pr_body(commit_id, input_data["api_repo_name"])
        success_msg = {"commit_id": commit_id, "msg": msg_body}
        successful_commits.append(success_msg)
    except PushCpException as pe:
        issue_comment(milestoned_issue_number, str(pe), input_data["api_repo_name"], input_data["is_prod"])
        raise SystemExit(0)
    except Exception as e:
        failure_msg = {"commit_id": commit_id, "msg": str(e).replace("\ncc: @bazelbuild/triage", "")}
        failed_commits.append(failure_msg)
    requires_clone = False
    requires_checkout = False

try:
    push_to_branch(target_branch_name)
except Exception as e:
    issue_comment(milestoned_issue_number, str(e), input_data["api_repo_name"], input_data["is_prod"])
    raise SystemExit(0)

issue_comment_body = ""
if len(successful_commits):
    pr_body = f"This PR contains {len(successful_commits)} commit(s).\n\n"
    print(pr_body)
    for idx, commit in enumerate(successful_commits):
        pr_body += str((idx + 1)) + ") " + commit["msg"] + "\n\n"
    print("This is the reviewers, ", reviewers)
    # cherry_picked_pr_number = create_pr(reviewers, release_number, labels, issue_title, pr_body, release_branch_name, target_branch_name, input_data['user_name'])
    cherry_picked_pr_number = "19395"
    issue_comment_body = f"Cherry-picked in https://github.com/{upstream_repo}/pull/{cherry_picked_pr_number}, which includes the following commit(s): "

    for index, success_commit in enumerate(successful_commits):
        print("This is index!!", index)
        issue_comment_body += f"https://github.com/{input_data['api_repo_name']}/commit/{success_commit['commit_id']}"
        if index < len(successful_commits) - 1:
            issue_comment_body += ", "

    if len(failed_commits):
        failure_commits_str = f". There was(were) also {len(failed_commits)} failed commit(s): "
        for fail_commit in failed_commits:
            failure_commits_str += f"https://github.com/{input_data['api_repo_name']}/commit/{fail_commit['commit_id']} ({fail_commit['msg']})"
            if idx < len(failed_commits) - 1:
                failure_commits_str += ", "
        failure_commits_str += "The failed commit(s) are NOT included in the PR."
        issue_comment_body += failure_commits_str
else:
    issue_comment_body = "Cherry-pick(s) failed for "
    for idx, commit in enumerate(failed_commits):
        issue_comment_body += f" {commit['commit_id']} ({commit['msg']})"
        if idx < len(failed_commits) - 1:
            issue_comment_body += ", "

print("This is the issue_comment_body", issue_comment_body)
print("*" * 100)
print("successful_commits", successful_commits)
print("failed_commits", failed_commits)
issue_comment(milestoned_issue_number, issue_comment_body, input_data["api_repo_name"], input_data["is_prod"])
