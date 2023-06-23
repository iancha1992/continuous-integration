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

    g = Github(token)
    # repository_url = 'https://github.com/iancha1992/bazel'
    repository_url = "iancha1992/bazel"
    fork_owner = "Pavank1992"
    repo_name = "bazel"
    master_branch = 'master'
    release_branch_name = "release-" + release_number
    target_branch_name = f"cp{pr_number}"
    #release_number = 'test_16910'
    # pr_number = '1234556'
    #commit_id = 'd013c6c119c35a262639a600491dbc128fbfa199'  # Taken sample commit ID
    all_branch = ["master", "release_test"]



    def clone_and_sync_repo():
        print("Cloning and syncing the repo...")
        subprocess.run(['gh', 'repo', 'sync', repository_url])  # Syncing
        subprocess.run(['gh', 'repo', 'clone', repository_url])
        

    def checkout_release_number(repository_url, branch):
        os.chdir(repo_name)
        print("git remote -v")
        subprocess.run(['git', 'remote', '-v'])
        # print("git fetch --all")
        # subprocess.run(['git', 'fetch', '--all'])  # Fetch all branches
        # print("git checkout", master_branch)
        # subprocess.run(['git', 'checkout', master_branch])
        # print(f'git checkout {release_branch_name}')
        # subprocess.run(['git', 'checkout', release_branch_name])
        # print(f'git checkout -b {target_branch_name}')
        # subprocess.run(['git', 'checkout', '-b', target_branch_name])

        

    def run_cherrypick(pr_number, commit_id):
        # Create a new branch for cherry-picking
        cp_branch_name = f'cp{pr_number}'
        # subprocess.run(['git', 'config', '--global', 'user.email', 'pavanksingh@google.com'])
        # subprocess.run(['git', 'config', '--global', 'user.name', 'pavank1992'])

        # Cherry-pick the specified commit
        print(f"cherry-picking the commit id {commit_id} in CP branch: {cp_branch_name}")
        status = subprocess.run(['git', 'cherry-pick', commit_id])
        if status.returncode == 0:
            print(f"Successfully Cherry-picked, pushing it to branch: {cp_branch_name}")
            # env = dict(os.environ)
            username = "iancha1992"
            password = "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"
            git_env = {
                "GIT_COMMITTER_NAME": username,
                "GIT_COMMITTER_EMAIL": username + "@google.com",
                "GIT_AUTHOR_NAME": username,
                "GIT_AUTHOR_EMAIL": username + "@google.com",
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_ASKPASS": "echo",
                "GIT_USERNAME": username,
                "GIT_PASSWORD": password,
                "SECRET_TOKEN": token
            }
            print("aaaaa")
            subprocess.run(['git', 'push', '--set-upstream', 'origin', cp_branch_name], env=git_env)
            print("bbbb")
        else:
            print("Cherry-pick unsuccessful. Please proceed manually.")

    print('Cherry-picking Started')
    clone_and_sync_repo()
    checkout_release_number(repository_url, release_number)
    # run_cherrypick(pr_number, commit_id)
    # print('...end...')
