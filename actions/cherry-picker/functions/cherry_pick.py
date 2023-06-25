import os, subprocess, requests, github3
from github import Github

def cherry_pick(commit_id, pr_number, reviewers, release_number, issue_number):
    token = os.environ["GH_TOKEN"]
    print("Cherrypicking")
    print("commit id", commit_id)
    print("prnumber", pr_number)
    print("reviewers", reviewers)
    print("release_number", release_number)
    print("Issuenumber", issue_number)

    commit_id = "a9f5e2180ac949ad4dd365cc5fc9ceaa116034ce"

    g = Github(token)
    gh_cli_repo_name = "iancha1992/bazel"
    repo_url = 'git@github.com:iancha1992/bazel.git'

    fork_owner = "Pavank1992"
    repo_name = "bazel"
    master_branch = 'release_test'
    # release_branch_name = "release-" + release_number
    release_branch_name = 'release_test'
    target_branch_name = f"cp{pr_number}"
    # target_branch_name = 'release_test'
    all_branch = ["master", "release_test"]

    def clone_and_sync_repo():
        print("Cloning and syncing the repo...")
        subprocess.run(['gh', 'repo', 'sync', gh_cli_repo_name])  # Syncing
        subprocess.run(['gh', 'repo', 'clone', gh_cli_repo_name])
        os.chdir(repo_name)

    def remove_upstream_and_add_origin():
        subprocess.run(['git', 'remote', 'rm', 'upstream'])
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
        print("git remote -v")
        subprocess.run(['git', 'remote', '-v'])

    def checkout_release_number():
        print("git fetch --all")
        subprocess.run(['git', 'fetch', '--all'])  # Fetch all branches
        # print("git checkout", master_branch)
        # subprocess.run(['git', 'checkout', master_branch])
        print(f'git checkout {release_branch_name}')
        subprocess.run(['git', 'checkout', release_branch_name])
        print(f'git checkout -b {target_branch_name}')
        status_checkout = subprocess.run(['git', 'checkout', '-b', target_branch_name])

        # Need to let the user know that there is already a created branch with the same name and bazel-io needs to delete the branch
        if status_checkout.returncode != 0:
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', f"Cherry-pick was being attempted. But, it failed due to already existent branch called {target_branch_name}"])

    def run_cherrypick():
        # Create a new branch for cherry-picking
        cp_branch_name = f'cp{pr_number}'

        # Cherry-pick the specified commit
        print(f"Cherry-picking the commit id {commit_id} in CP branch: {cp_branch_name}")
        status = subprocess.run(['git', 'cherry-pick', commit_id])
        if status.returncode == 0:
            print(f"Successfully Cherry-picked, pushing it to branch: {cp_branch_name}")
            # username = "iancha1992"
            # password = "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"
            # git_env = {
            #     "GIT_COMMITTER_NAME": username,
            #     "GIT_COMMITTER_EMAIL": username + "@google.com",
            #     "GIT_AUTHOR_NAME": username,
            #     "GIT_AUTHOR_EMAIL": username + "@google.com",
            #     "GIT_TERMINAL_PROMPT": "0",
            #     "GIT_ASKPASS": "echo",
            #     "GIT_USERNAME": username,
            #     "GIT_PASSWORD": password,
            #     "SECRET_TOKEN": token
            # }
            subprocess.run(['git', 'push', '--set-upstream', 'origin', cp_branch_name])
        else:
            subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--body', "Cherry-pick was attempted. But there was merge conflicts."])

    print('Cherry-picking Started')
    clone_and_sync_repo()
    remove_upstream_and_add_origin()
    checkout_release_number()
    run_cherrypick()
    # print('...end...')
