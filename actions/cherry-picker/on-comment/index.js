// import { cherrypickRunner } from "../cherry-pick-runner/index.js";

const cherrypickRunner = require("../cherry-pick-runner/index");

const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);

const payload = github.context.payload;

console.log("Gomez")
console.log("This is the payload");
console.log(payload);

const issueNumber = payload.issue.number;
const prNumber = payload.issue.body.split("#")[1];
console.log("This is my pr number", prNumber);

actorName = "copybara-service[bot]";


async function getIssueEventsInfos() {
    const response = await octokit.request(`GET /repos/iancha1992/bazel/issues/${issueNumber}/events`, {
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
        console.log("Congress");
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
        for (const response of responses[1]) {
            if ((response.actor.login == actorName) && (response.commit_id != null) && (commitId == null)) {
                commitId = response.commit_id
                console.log("FAnta");
                console.log(commitId)
            }
            else if ((response.actor.login == actorName) && (response.commit_id != null) && (commitId != null)) {
                console.log("Anotherone")
                console.log(commitId)
                throw "There are multiple commits made by copybara-service[bot]. There can only be one."
            }
        }
        if (commitId == null) {
            throw `There is no commit made by ${actorName}`
        } else {
            pass
            // cherrypickRunner(commitId);
        }




    }).catch((e) => {
        console.log(e);
    })
