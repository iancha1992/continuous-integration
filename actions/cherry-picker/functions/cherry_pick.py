import os, subprocess, requests, github3
from github import Github

def cherry_pick(commit_id, pr_number, reviewers, release_number, issue_number, is_first_time):
    token = os.environ["GH_TOKEN"]
    print("Cherrypicking")
    print("commit id", commit_id)
    print("prnumber", pr_number)
    print("reviewers", reviewers)
    print("release_number", release_number)
    print("Issuenumber", issue_number)

    g = Github(token)
    gh_cli_repo_name = "iancha1992/bazel"
    repo_url = f'git@github.com:{gh_cli_repo_name}.git'
    repo_name = gh_cli_repo_name.split("/")[1]
    master_branch = 'release_test'
    # release_branch_name = "release-" + release_numberj
    release_branch_name = f'fake-release-{release_number}'
    target_branch_name = f"cp{pr_number}-{release_number}"
    user_name = "iancha1992"
    # target_branch_name = 'release_test'

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
        print("git remote -v")
        subprocess.run(['git', 'remote', '-v'])

    def checkout_release_number():
        print("git fetch --all")
        subprocess.run(['git', 'fetch', '--all'])  # Fetch all branches
        print(f'git checkout {release_branch_name}')
        subprocess.run(['git', 'checkout', release_branch_name])
        print(f'git checkout -b {target_branch_name}')
        status_checkout = subprocess.run(['git', 'checkout', '-b', target_branch_name])

        # Need to let the user know that there is already a created branch with the same name and bazel-io needs to delete the branch
        if status_checkout.returncode != 0:
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', f"Cherry-pick was being attempted. But, it failed due to already existent branch called {target_branch_name}"])

    def run_cherrypick():
        push_status = None
        # Cherry-pick the specified commit
        print(f"Cherry-picking the commit id {commit_id} in CP branch: {target_branch_name}")
        # status = subprocess.run(['git', 'cherry-pick', commit_id])
        status = subprocess.run(['git', 'cherry-pick', '-m', '1', commit_id])
        if status.returncode == 0:
            print(f"Successfully Cherry-picked, pushing it to branch: {target_branch_name}")
            push_status = subprocess.run(['git', 'push', '--set-upstream', 'origin', target_branch_name])
        else:
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "Cherry-pick was attempted. But there was merge conflicts."])

        if push_status.returncode != 0:
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', f"Cherry-pick was attempted. But failed to push. Please check if the branch, {target_branch_name}, was already created"])

    if is_first_time == True:
        # The repo should be cloned only once to save time. Otherwise, it is a waste of time and space.
        clone_and_sync_repo()
        remove_upstream_and_add_origin()
    checkout_release_number()
    run_cherrypick()

    return {
        "master_branch": master_branch,
        "release_branch_name": release_branch_name,
        "target_branch_name": target_branch_name
    }
