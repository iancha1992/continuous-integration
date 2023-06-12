const cherrypickRunner = require("../cherry-pick-runner/index");

const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);

const payload = github.context.payload;

console.log("This is the payload");
console.log(payload);

const issueNumber = payload.issue.number;
const prNumber = payload.issue.body.split("#")[1];
console.log("This is my pr number", prNumber);

async function getIssueEventsInfos() {
    const response = await octokit.request(`GET /repos/iancha1992/bazel/issues/${prNumber}/events`, {
        per_page: 100,
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });
    return response.data;
};

async function getPrEventsInfos() {
    const response = await octokit.request(`GET /repos/iancha1992/bazel/pulls/${prNumber}`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });
    return response.data;
}


// https://api.github.com/repos/bazelbuild/bazel/pulls/18130


Promise.all([getPrEventsInfos(), getIssueEventsInfos()])
    .then((responses) => {
        console.log(responses);
        console.log(`Checking if Pull Request #${prNumber} is closed...`);

        if (responses[0].state != "closed") {
            // Needs better implemention for throwing error here later
            throw (`Pull Request #${prNumber} is not closed yet. Only closed ones are cherry-pickable.`);
        }
        else {
            console.log(`Confirmed that Pull Request #${prNumber} is closed.`);
        }

        console.log("Now checking if there is a commit ID..");

        let commitId = null;

        actorName = "iancha1992";
        // actorName = "copybara-service[bot]";
        actionEvent = "merged";
        // actionEvent = "closed";

        for (let response of responses[1]) {
            console.log("This is allresponses!", responses[1])
            console.log("This is the response!!!", response);
            if ((response.actor.login == actorName) && (response.commit_id != null) && (commitId == null) && (response.event == actionEvent)) {
                console.log("This is the response!!!", response);
                commitId = response.commit_id;
            }
            else if ((response.actor.login == actorName) && (response.commit_id != null) && (commitId != null) && (response.event == actionEvent)) {
                throw "There are multiple commits made by copybara-service[bot]. There can only be one."
            }
        }
        if (commitId == null) {
            throw `There is no commit made by ${actorName}`
        } else {
            console.log(`Retrieved the commit ID, ${commitId}`);
            console.log("Now unto cherrypicking this!!");
            // cherrypickRunner(commitId);
        }
    }).catch((e) => {
        console.log(e);
    })
