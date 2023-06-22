import os, subprocess, requests, github3
from github import Github

def cherry_pick(commit_id, pr_number, tok, reviewers, release_number, issue_number):
    token = os.environ["GH_TOKEN"]
    print("Cherrypicking")
    print("commit id", commit_id)
    print("prnumber", pr_number)
    print("reviewers", reviewers)
    print("release_number", release_number)
    print("Issuenumber", issue_number)

    # token = "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"
    # secret_token = "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"
    g = Github(token)
    # token = "abcd"
    repository_url = 'https://github.com/iancha1992/bazel'
    upstream_owner = "iancha1992"
    fork_owner = "Pavank1992"
    repo_name = "bazel"
    master_branch = 'release_test'
    #release_number = 'test_16910'
    # pr_number = '1234556'
    #commit_id = 'd013c6c119c35a262639a600491dbc128fbfa199'  # Taken sample commit ID
    all_branch = ["master", "release_test"]

    # for branch_name in all_branch:
    #     # Get the upstream branch's commit SHA
    #     upstream_url = f"https://api.github.com/repos/{upstream_owner}/{repo_name}/git/refs/heads/{branch_name}"
    #     upstream_response = requests.get(upstream_url, headers={"Authorization": f"token {token}"})
    #     upstream_commit_sha = upstream_response.json()["object"]["sha"]

    #     # Update the forked repository's branch reference
    #     fork_url = f"https://api.github.com/repos/{fork_owner}/{repo_name}/git/refs/heads/{branch_name}"
    #     fork_sha = {"sha": upstream_commit_sha}
    #     fork_response = requests.patch(fork_url, json=fork_sha, headers={"Authorization": f"token {token}"})

    #     # Check if the branch reference was successfully updated
    #     print(f'Syncing branches {branch_name} with upstream')
    #     if fork_response.status_code == 200:
    #         print(f"{branch_name} branch updated successfully.")
    #     else:
    #         print(f"Failed to update {branch_name} branch .")


    def clone_and_sync_repo(repo_url):
        # subprocess.run('gh', 'auth', 'login')
        subprocess.run(['gh', 'repo', 'sync', repo_url])  # Syncing
        subprocess.run(['gh', 'repo', 'clone', repo_url])
        subprocess.run('ls')
        print('debugging...')
        subprocess.run('pwd')
        print(repo_name)
        


    def checkout_release_number(repo_url, branch):
        # subprocess.run(['git', 'clone', repo_url])  # cloning
        # repo_name = repo_url.split('/')[-1].split('.')[0]
        os.chdir(repo_name)
        subprocess.run(['git', 'fetch', '--all'])  # Fetch all branches
        subprocess.run(['git', 'checkout', master_branch])
        # subprocess.run(['git', 'pull'])
        subprocess.run(['git', 'checkout', 'release-'+release_number])
        # subprocess.run(['git', 'pull'])


    def create_branch_and_cherrypick(pr_number, commit_id):
        # Create a new branch for cherry-picking
        cp_branch_name = f'cp{pr_number}'
        # subprocess.run(['git', 'config', '--global', 'user.email', 'pavanksingh@google.com'])
        # subprocess.run(['git', 'config', '--global', 'user.name', 'pavank1992'])
        print(f"creating CP branch {cp_branch_name}")
        subprocess.run(['git', 'checkout', '-b', cp_branch_name])

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
    clone_and_sync_repo(repository_url)
    checkout_release_number(repository_url, release_number)
    create_branch_and_cherrypick(pr_number, commit_id)
    print('...end...')
