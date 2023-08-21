import os, subprocess, requests
from pprint import pprint

headers = {
    'X-GitHub-Api-Version': '2022-11-28'
}

token = os.environ["GH_TOKEN"]

upstream_url = "https://github.com/bazelbuild/bazel.git"
upstream_repo = upstream_url.replace("https://github.com/", "").replace(".git", "")

def check_closed(pr_number, api_repo_name):
    r = requests.get(f'https://api.github.com/repos/{api_repo_name}/pulls/{pr_number}', headers=headers)
    if r.status_code == 404:
        response_issue = requests.get(f'https://api.github.com/repos/{api_repo_name}/issues/{pr_number}', headers=headers)
        if response_issue.json()["state"] == "closed": return True
    elif r.json()["state"] == "closed": return True
    return False

def get_commit_id(pr_number, actor_name, action_event, api_repo_name):
    params = {
        "per_page": 100
    }
    r = requests.get(f'https://api.github.com/repos/{api_repo_name}/issues/{pr_number}/events', headers=headers, params=params)
    commit_id = None
    for event in r.json():
        if (event["actor"]["login"] in actor_name) and (event["commit_id"] != None) and (commit_id == None) and (event["event"] == action_event):
            commit_id = event["commit_id"]
        elif (event["actor"]["login"] in actor_name) and (event["commit_id"] != None) and (commit_id != None) and (event["event"] == action_event):
            raise ValueError(f'PR#{pr_number} has multiple commits by {actor_name}')
    
    if commit_id == None: raise ValueError(f'PR#{pr_number} has NO commit made by {actor_name}')

    return commit_id

def get_reviewers(pr_number, api_repo_name, is_prod):
    r = requests.get(f'https://api.github.com/repos/{api_repo_name}/pulls/{pr_number}/reviews', headers=headers)
    if len(r.json()) == 0: raise ValueError(f"PR#{pr_number} has no approver at all.")
    approvers_list = []
    for review in r.json():
        if review["state"] == "APPROVED": approvers_list.append(review["user"]["login"])
    if len(approvers_list) == 0:
        raise ValueError(f"PR#{pr_number} has no approval from the approver(s).")
    return ["iancha1992"]
    
    # Now, check if the users in the list are googlers
    # if is_prod == True:
    #     googler_approvers_list = []
    #     token_headers = headers.copy()
    #     token_headers["Authorization"] = f"Bearer {token}"
    #     for user_data in approvers_list:
    #         login_name = user_data["login"]
    #         response_check = requests.get(f"https://api.github.com/users/{login_name}/hovercard", headers=token_headers).json()
    #         message_keywords_list = []
    #         for context in response_check["contexts"]:
    #             message_keywords_list.extend(context["message"].split())
    #         if "@bazelbuild" in message_keywords_list and "@googlers" in message_keywords_list: googler_approvers_list.append(user_data)
    #     if len(googler_approvers_list) == 0:
    #         raise ValueError(f"PR#{pr_number} has no GOOGLE approver.")
    #     return googler_approvers_list
    # return approvers_list

def extract_release_numbers_data(pr_number, api_repo_name):

    def get_all_milestones_data():
        r = requests.get(f'https://api.github.com/repos/{api_repo_name}/milestones', headers=headers)
        milestones_data = list(map(lambda n: {"title": n["title"].split("release blockers")[0].replace(" ", ""), "number": n["number"]}, r.json()))
        return milestones_data

    def get_milestoned_issues(milestones, pr_number):
        results= {}
        for milestone in milestones:
            params = {
                "milestone": milestone["number"]
            }
            r = requests.get(f'https://api.github.com/repos/{api_repo_name}/issues', headers=headers, params=params)
            for issue in r.json():
                if issue["body"] == f'Forked from #{pr_number}' and issue["state"] == "open":
                    results[milestone["title"]] = issue["number"]
                    break
        print("This is the results", results)
        return results

    milestones_data = get_all_milestones_data()
    milestoned_issues = get_milestoned_issues(milestones_data, pr_number)
    return milestoned_issues

def cherry_pick(commit_id, release_branch_name, target_branch_name, issue_number, is_first_time, input_data):
    print("Cherrypicking now!")
    print(commit_id, release_branch_name, target_branch_name, issue_number, is_first_time, input_data)
    # token = os.environ["GH_TOKEN"]
    gh_cli_repo_name = f"{input_data['user_name']}/bazel"
    repo_url = f"git@github.com:{gh_cli_repo_name}.git"
    master_branch = input_data["master_branch"]
    user_name = input_data["user_name"]

    def clone_and_sync_repo():
        print("Cloning and syncing the repo...")
        subprocess.run(['gh', 'repo', 'sync', gh_cli_repo_name, "-b", master_branch])
        subprocess.run(['gh', 'repo', 'sync', gh_cli_repo_name, "-b", release_branch_name])
        subprocess.run(['git', 'clone', f"https://{user_name}:{token}@github.com/{gh_cli_repo_name}.git"])
        subprocess.run(['git', 'config', '--global', 'user.name', user_name])
        subprocess.run(['git', 'config', '--global', 'user.email', input_data["email"]])
        os.chdir("bazel")
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
        subprocess.run(['git', 'remote', '-v'])

    def checkout_release_number():
        subprocess.run(['git', 'fetch', '--all'])  # Fetch all branches
        status_checkout_release = subprocess.run(['git', 'checkout', release_branch_name])
        
        # Create the new release branch from the upstream if not exists already.
        if status_checkout_release.returncode != 0:
            print(f"There is NO branch called {release_branch_name}...")
            print(f"Creating the {release_branch_name} from upstream, {upstream_url}")
            subprocess.run(['git', 'remote', 'add', 'upstream', upstream_url])
            subprocess.run(['git', 'remote', '-v'])
            subprocess.run(['git', 'fetch', 'upstream'])
            subprocess.run(['git', 'branch', release_branch_name, f"upstream/{release_branch_name}"])
            release_push_status = subprocess.run(['git', 'push', '--set-upstream', 'origin', release_branch_name])
            if release_push_status.returncode != 0:
                raise ValueError(f"Could not create and push the branch, {release_branch_name}")
            subprocess.run(['git', 'remote', 'rm', 'upstream'])
            subprocess.run(['git', 'checkout', release_branch_name])

        status_checkout_target = subprocess.run(['git', 'checkout', '-b', target_branch_name])

        # Need to let the user know that there is already a created branch with the same name and bazel-io needs to delete the branch
        if status_checkout_target.returncode != 0:
            issue_comment(issue_number, f"Cherry-pick was being attempted. But, it failed due to already existent branch called {target_branch_name}\ncc: @bazelbuild/triage", input_data["api_repo_name"], input_data["is_prod"])
            raise ValueError(f"There may already be a branch called, {target_branch_name}")

    def run_cherrypick():
        print(f"Cherry-picking the commit id {commit_id} in CP branch: {target_branch_name}")
        if input_data["is_prod"] == True:
            cherrypick_status = subprocess.run(['git', 'cherry-pick', commit_id])
        else:
            cherrypick_status = subprocess.run(['git', 'cherry-pick', '-m', '1', commit_id])

        if cherrypick_status.returncode == 0:
            print(f"Successfully Cherry-picked, pushing it to branch: {target_branch_name}")
            push_status = subprocess.run(['git', 'push', '--set-upstream', 'origin', target_branch_name])
            if push_status.returncode != 0:
                issue_comment(issue_number, f"Cherry-pick was attempted, but failed to push. Please check if the branch, {target_branch_name}, exists\ncc: @bazelbuild/triage", input_data["api_repo_name"], input_data["is_prod"])
                raise ValueError(f"Could not create and push the branch, {release_branch_name}")
        else:
            issue_comment(issue_number, "Cherry-pick was attempted but there were merge conflicts. Please resolve manually.\ncc: @bazelbuild/triage", input_data["api_repo_name"], input_data["is_prod"])
            raise ValueError("Cherry-pick was attempted but there were merge conflicts. Please resolve manually.")
        
    if is_first_time == True:
        clone_and_sync_repo()
    checkout_release_number()
    run_cherrypick()
    return 0

def create_pr(reviewers, release_number, issue_number, labels, issue_data, release_branch_name, target_branch_name, user_name, api_repo_name, is_prod):
    def send_pr_msg(issue_number, head_branch, release_branch):
        print("Sending the pr msg...")
        params = {
            "head": head_branch,
            "base": release_branch,
            "state": "open"
        }
        print(f"This is the issue number, {issue_number}")
        r = requests.get(f'https://api.github.com/repos/{upstream_repo}/pulls', headers=headers, params=params).json()
        if len(r) == 1:
            cherry_picked_pr_number = r[0]["number"]
            print(f"Cherry-picked in {cherry_picked_pr_number}")
            issue_comment(issue_number, f"Cherry-picked in https://github.com/{upstream_repo}/pull/{cherry_picked_pr_number}", api_repo_name, is_prod)
        else:
            print("Failed to send PR msg")
            issue_comment(issue_number, "Failed to send PR msg \ncc: @bazelbuild/triage", api_repo_name, is_prod)
            raise ValueError("Failed to send PR msg")

    head_branch = f"{user_name}:{target_branch_name}"
    # reviewers_str = ",".join([str(r["login"]) for r in reviewers])
    reviewers_str = ",".join(reviewers)
    labels_str = ",".join(labels)
    pr_title = f"[{release_number}] {issue_data['title']}"
    pr_body = issue_data['body']

    status_create_pr = subprocess.run(['gh', 'pr', 'create', "--repo", upstream_repo, "--title", pr_title, "--body", pr_body, "--head", head_branch, "--base", release_branch_name,  '--label', labels_str, '--reviewer', reviewers_str])
    print("status_create_pr", status_create_pr)
    if status_create_pr.returncode != 0:
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "PR failed to be created."])
    else:
        print("PR was successfully created")
        send_pr_msg(issue_number, head_branch, release_branch_name)

def get_labels(pr_number, api_repo_name):
    r = requests.get(f'https://api.github.com/repos/{api_repo_name}/issues/{pr_number}/labels', headers=headers)
    labels_list = list(map(lambda x: x["name"], r.json()))
    labels_list = list(filter(lambda label: "area" in label or "team" in label, labels_list))
    if "awaiting-review" not in labels_list: labels_list.append("awaiting-review")
    return labels_list

def get_issue_data(pr_number, commit_id, api_repo_name):
    data = {}
    response_issue = requests.get(f'https://api.github.com/repos/{api_repo_name}/issues/{pr_number}', headers=headers)
    data["title"] = response_issue.json()["title"]

    response_commit = requests.get(f"https://api.github.com/repos/{api_repo_name}/commits/{commit_id}")
    original_msg = response_commit.json()["commit"]["message"]
    pr_body = None
    if "\n\n" in original_msg:
        pr_body = original_msg[original_msg.index("\n\n") + 2:]
    else:
        pr_body = original_msg
    commit_str_body = f"Commit https://github.com/{api_repo_name}/commit/{commit_id}"
    if "PiperOrigin-RevId" in pr_body:
        piper_index = pr_body.index("PiperOrigin-RevId")
        pr_body = pr_body[:piper_index] + f"{commit_str_body}\n\n" + pr_body[piper_index:]
    else:
        pr_body += f"\n\n{commit_str_body}"

    data["body"] = pr_body
    return data

def issue_comment(issue_number, body_content, api_repo_name, is_prod):
    print("Issuing Comment!", issue_number, body_content, api_repo_name)
    if is_prod == True:
        subprocess.run(['git', 'remote', 'add', 'upstream', upstream_url])
        subprocess.run(['gh', 'repo', 'set-default', upstream_repo])
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', body_content])
        subprocess.run(['git', 'remote', 'rm', 'upstream'])
        subprocess.run(['gh', 'repo', 'set-default', api_repo_name])
    else:
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', body_content])
