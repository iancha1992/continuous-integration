import subprocess
def create_pr(commit_id, pr_number, reviewers, release_number, issue_number, pr_url, repo_name):
    print(commit_id, pr_number, reviewers, release_number, issue_number)
    subprocess.run('gh', 'pr', 'create', '--base', 'test_16910', '--head', 'test_16910_1', '--label', 'team-CLI,' '-r', 'iancha1992', '--title', "[6.3.0]no", '--body', "Everything works aaaa")

create_pr("63a2d53", 103, [{'login': 'chaheein123', 'id': 23069091}], "6.3.0", 106, "https://github.com/iancha1992/bazel/pull/new/cp103", "iancha1992/bazel")







