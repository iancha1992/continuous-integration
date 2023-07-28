import os, subprocess, requests, github3
from github import Github
from pprint import pprint

headers = {
    'X-GitHub-Api-Version': '2022-11-28'
}

def check_closed(pr_number):
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/pulls/{pr_number}', headers=headers)
    if r.json()["state"] == "closed": return True
    return False

def get_commit_id(pr_number, actor_name, action_event):
    params = {
        "per_page": 100
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues/{pr_number}/events', headers=headers, params=params)
    commit_id = None
    for event in r.json():
        if (event["actor"]["login"] in actor_name) and (event["commit_id"] != None) and (commit_id == None) and (event["event"] == action_event):
            commit_id = event["commit_id"]
        elif (event["actor"]["login"] in actor_name) and (event["commit_id"] != None) and (commit_id != None) and (event["event"] == action_event):
            raise ValueError(f'PR#{pr_number} has multiple commits by {actor_name}')
    
    if commit_id == None: raise ValueError(f'PR#{pr_number} has NO commit made by {actor_name}')

    return commit_id

def get_reviewers(pr_number):
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/pulls/{pr_number}/reviews', headers=headers)
    if len(r.json()) == 0: raise ValueError(f"PR#{pr_number} has no approver.")
    approvers_list = []
    for review in r.json():
        if review["state"] == "APPROVED":
            data = {
                "login": review["user"]["login"],
                "id": review["user"]["id"]
            }
            approvers_list.append(data)
    if len(approvers_list) == 0:
        raise ValueError(f"PR#{pr_number} has no approver.")    
    return approvers_list

def extract_release_numbers_data(pr_number):

    def get_all_milestones_data():
        r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/milestones', headers=headers)
        milestones_data = list(map(lambda n: {"title": n["title"].split("release blockers")[0].replace(" ", ""), "number": n["number"]}, r.json()))
        return milestones_data

    def get_milestoned_issues(milestones, pr_number):
        results= {}
        for milestone in milestones:
            params = {
                "milestone": milestone["number"]
            }
            r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues', headers=headers, params=params)
            for issue in r.json():
                if issue["body"] == f'Forked from #{pr_number}' and issue["state"] == "open":
                    results[milestone["title"]] = issue["number"]
                    break
        print("This is the results", results)
        return results

    milestones_data = get_all_milestones_data()
    milestoned_issues = get_milestoned_issues(milestones_data, pr_number)
    return milestoned_issues

def cherry_pick(commit_id, pr_number, release_number, issue_number, is_first_time, github_data):
    token = os.environ["GH_TOKEN"]
    g = Github(token)
    gh_cli_repo_name = github_data["gh_cli_repo_name"]
    repo_url = f'git@github.com:{gh_cli_repo_name}.git'
    upstream_url = "git@github.com:bazelbuild/bazel.git"
    repo_name = gh_cli_repo_name.split("/")[1]
    master_branch = github_data["master_branch"]
    release_branch_name = f"{github_data['release_branch_name_initials']}{release_number}"
    target_branch_name = f"cp{pr_number}-{release_number}"
    user_name = github_data["user_name"]
    result_data = {
        "release_branch_name": release_branch_name,
        "target_branch_name": target_branch_name,
        "is_successful": True
    }

    def clone_and_sync_repo():
        print("Cloning and syncing the repo...")
        subprocess.run(['gh', 'repo', 'sync', gh_cli_repo_name, "-b", master_branch])  # Syncing
        subprocess.run(['gh', 'repo', 'sync', gh_cli_repo_name, "-b", release_branch_name])
        subprocess.run(['git', 'clone', f'https://{user_name}:{token}@github.com/{gh_cli_repo_name}.git'])
        subprocess.run(['git', 'config', '--global', 'user.name', 'iancha1992'])
        subprocess.run(['git', 'config', '--global', 'user.email', 'heec@google.com'])
        os.chdir(repo_name)

    def remove_upstream_and_add_origin():
        subprocess.run(['git', 'remote', 'rm', 'upstream'])
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
        subprocess.run(['git', 'remote', '-v'])

    def checkout_release_number():
        subprocess.run(['git', 'fetch', '--all'])  # Fetch all branches
        status_checkout_release = subprocess.run(['git', 'checkout', release_branch_name])
        
        # Create the new release branch from the upstream if not exists already.
        if status_checkout_release.returncode != 0:
            print(f"There is NO branch called {release_branch_name}...")
            print(f"Creating the {release_branch_name} from upstream, ({upstream_url})")
            subprocess.run(['git', 'remote', 'add', 'upstream', upstream_url], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
            subprocess.run(['git', 'fetch', 'upstream'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
            subprocess.run(['git', 'branch', release_branch_name, f'upstream/{release_branch_name}'], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
            release_push_status = subprocess.run(['git', 'push', '--set-upstream', 'origin', release_branch_name], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
            if release_push_status.returncode != 0:
                result_data["is_successful"] = False
                return
            subprocess.run(['git', 'remote', 'rm', 'upstream'])
            subprocess.run(['git', 'checkout', release_branch_name], stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

        status_checkout_target = subprocess.run(['git', 'checkout', '-b', target_branch_name])

        # Need to let the user know that there is already a created branch with the same name and bazel-io needs to delete the branch
        if status_checkout_target.returncode != 0:
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', f"Cherry-pick was being attempted. But, it failed due to already existent branch called {target_branch_name}"])

    def run_cherrypick():
        # Cherry-pick the specified commit
        print(f"Cherry-picking the commit id {commit_id} in CP branch: {target_branch_name}")
        if github_data["is_prod"] == True:
            status = subprocess.run(['git', 'cherry-pick', commit_id])
        else:
            status = subprocess.run(['git', 'cherry-pick', '-m', '1', commit_id])

        if status.returncode == 0:
            print(f"Successfully Cherry-picked, pushing it to branch: {target_branch_name}")
            push_status = subprocess.run(['git', 'push', '--set-upstream', 'origin', target_branch_name])
            if push_status.returncode != 0:
                subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', f"Cherry-pick was attempted, but failed to push. Please check if the branch, {target_branch_name}, exists"])
                result_data["is_successful"] = False
        else:
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "Cherry-pick was attempted but there were merge conflicts. Please resolve manually."])
            result_data["is_successful"] = False
        
    if is_first_time == True:
        clone_and_sync_repo()
        remove_upstream_and_add_origin()
    checkout_release_number()
    if result_data["is_successful"] == True:
        run_cherrypick()
    return result_data

def create_pr(reviewers, release_number, issue_number, labels, issue_data, pr_data, user_name):
    def send_pr_msg(issue_number, head_branch, release_branch):
        params = {
            "head": head_branch,
            "base": release_branch,
            "state": "open"
        }
        r = requests.get(f'https://api.github.com/repos/bazelbuild/bazel/pulls', headers=headers, params=params).json()
        if len(r) == 1:
            cherry_picked_pr_number = r[0]["number"]
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', f"Cherry-pick in https://github.com/bazelbuild/bazel/pull/{cherry_picked_pr_number}"])
        else:
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "Failed to send PR msg"])

    head_branch = f"{user_name}:{pr_data['target_branch_name']}"
    release_branch = pr_data["release_branch_name"]
    reviewers_str = ",".join([str(r["login"]) for r in reviewers])

    if "awaiting-review" not in labels:
        labels.append("awaiting-review")
    labels_str = ",".join(labels)
    pr_title = f"[{release_number}] {issue_data['title']}"
    pr_body = issue_data['body']

    status_create_pr = subprocess.run(['gh', 'pr', 'create', "--repo", "bazelbuild/bazel", "--title", pr_title, "--body", pr_body, "--head", head_branch, "--base", release_branch,  '--label', labels_str, '--reviewer', reviewers_str])
    print("status_create_pr", status_create_pr)
    if status_create_pr.returncode != 0:
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "PR failed to be created."])
    else:
        print("PR was successfully created")
        send_pr_msg(issue_number, head_branch, release_branch)

def get_labels(pr_number):
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues/{pr_number}/labels', headers=headers)
    return(list(map(lambda x: x["name"], r.json())))

def get_issue_data(pr_number, commit_id):
    data = {}
    response_issue = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues/{pr_number}', headers=headers)
    data["title"] = response_issue.json()["title"]

    response_commit = requests.get(f"https://api.github.com/repos/iancha1992/bazel/commits/{commit_id}")
    original_msg = response_commit.json()["commit"]["message"]
    pr_body = None
    if "\n\n" in original_msg:
        pr_body = original_msg[original_msg.index("\n\n") + 2:]
    else:
        pr_body = original_msg
    commit_str_body = f"Commit https://github.com/iancha1992/bazel/commit/{commit_id}"
    if "PiperOrigin-RevId" in pr_body:
        piper_index = pr_body.index("PiperOrigin-RevId")
        pr_body = pr_body[:piper_index] + f"{commit_str_body}\n\n" + pr_body[piper_index:]
    else:
        pr_body += f"\n\n{commit_str_body}"

    data["body"] = pr_body
    return data
