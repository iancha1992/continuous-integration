import os

headers = {
    'X-GitHub-Api-Version': '2022-11-28'
}
token = os.environ["GH_TOKEN"]
upstream_url = "https://github.com/bazelbuild/bazel.git"
upstream_repo = upstream_url.replace("https://github.com/", "").replace(".git", "")

cherrypick_with_commits_infos = {
    "commits": {
        "left": "If multiple, then please separate by commas. Example: 9e90a6, f1da12\n\n\n",
        "right": "\n\n### Which category",
    },
    "team_labels": {
        "left": "Which category does this issue belong to?\n\n\n",
        "right": "\n\n### Please provide the reviewers"
    },
    "reviewers": {
        "left": "Please provide the reviewers of the PR once it is created after cherry-picking. Example:",
        "right": None
    }
}

if "INPUT_IS_PROD" not in os.environ or os.environ["INPUT_IS_PROD"] == "false":
    input_data = {
        "is_prod": False,
        "api_repo_name": "iancha1992/bazel",
        "master_branch": "release_test",
        "release_branch_name_initials": "fake-release-",
        "user_name": "iancha1992",
        "action_event": "merged",
        "actor_name": {
            "iancha1992",
            "Pavank1992",
            "chaheein123",
        },
        "email": "heec@google.com"
    }

elif os.environ["INPUT_IS_PROD"] == "true":
    input_data = {
        "is_prod": True,
        "api_repo_name": "bazelbuild/bazel",
        "master_branch": "master",
        "release_branch_name_initials": "release-",
        "user_name": "bazel-io",
        "action_event": "closed",
        "actor_name": {
            "copybara-service[bot]"
        },
        "email": "bazel-io-bot@google.com"
    }

