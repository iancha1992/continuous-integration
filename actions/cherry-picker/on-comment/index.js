const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);

const payload = github.context.payload;

console.log("Gomez")
console.log("This is the payload");
console.log(payload);

const issue_number = payload.number;
const pr_number = payload.issue.body.split("#")[1];
console.log("This is my pr number", pr_number);

actor_name = "copybara-service[bot]";


async function getIssueEventsInfos() {
    const response = await octokit.request(`GET /repos/bazelbuild/bazel/issues/18130/events`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });
    return response.data;
};

async function getPrEventsInfos() {
    const response = await octokit.request(`GET /repos/bazelbuild/bazel/pulls/18130`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });
    return response.data;
}


https://api.github.com/repos/bazelbuild/bazel/pulls/18130

let commitId;

Promise.all([getPrEventsInfos(), getIssueEventsInfos()])
    .then((responses) => {
        console.log("Congress")
        console.log(responses);

        if (responses[0].state != "closed") {
            throw (`Pull Request ${pr_number} is not closed yet. Only closed ones are cherry-pickable.`)
        }

        for (const response of responses[1]) {
            if ((response.actor.login == actor_name) && (response.commit_id != null) && (commitId == null)) {
                commitId = response.commit_id
                console.log("FAnta");
                console.log(commitId)
            }
            else if ((response.actor.login == actor_name) && (response.commit_id != null) && (commitId != null)) {
                console.log("Anotherone")
                console.log(commitId)
                throw "There are multiple commits made by copybara-service[bot]. There can only be one."
            }
        }

    })
