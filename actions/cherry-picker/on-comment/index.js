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
};

async function getReviews() {
    const response = await octokit.request(`GET /repos/iancha1992/bazel/pulls/${prNumber}/reviews`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });
    return response.data;
};

function getCommitId(issueEvents) {
    const actorName = "iancha1992";
    // actorName = "copybara-service[bot]";
    const actionEvent = "merged";
    // actionEvent = "closed";
    let commitId = null;
    for (let e of issueEvents) {
        console.log("This is the response!!!", e);
        if ((e.actor.login == actorName) && (e.commit_id != null) && (commitId == null) && (e.event == actionEvent)) {
            commitId = e.commit_id;
        }
        else if ((e.actor.login == actorName) && (e.commit_id != null) && (commitId != null) && (e.event == actionEvent)) {
            throw "There are multiple commits made by copybara-service[bot]. There can only be one."
        }
    }
    return commitId;
};

function getReviewer(reviews) {
    if (reviews.length() == 0) {
        return null
    }

    let approvers_list = [];
    for (let review of reviews) {
        if (review.state == "APPROVED") {
            let data = {
                "login": review.login,
                "id": review.id
            }
            approvers_list.push(data)
        }
    }
    return approvers_list;
}

// https://api.github.com/repos/bazelbuild/bazel/pulls/18130


Promise.all([getPrEventsInfos(), getIssueEventsInfos(), getReviews()])
    .then((responses) => {
        console.log(responses);
        console.log(`Checking if Pull Request #${prNumber} is closed...`);

        // Check if the PR was closed.
        if (responses[0].state != "closed") {
            // Needs better implemention for throwing error here later
            throw (`Pull Request #${prNumber} is not closed yet. Only closed ones are cherry-pickable.`);
        }
        console.log(`Confirmed that Pull Request #${prNumber} is closed.`);

        // Check if there is exactly one Copybara commit ID.
        console.log("Now checking if there is a commit ID..");

        // Check if copybara has one commit ID and retrieve
        // for (let response of responses[1]) {
        //     console.log("This is allresponses!", responses[1])
        //     console.log("This is the response!!!", response);
        //     if ((response.actor.login == actorName) && (response.commit_id != null) && (commitId == null) && (response.event == actionEvent)) {
        //         console.log("This is the response!!!", response);
        //         commitId = response.commit_id;
        //     }
        //     else if ((response.actor.login == actorName) && (response.commit_id != null) && (commitId != null) && (response.event == actionEvent)) {
        //         throw "There are multiple commits made by copybara-service[bot]. There can only be one."
        //     }
        // }
        let commitId = getCommitId(responses[1]);
        if (commitId == null) {
            throw `There is no commit made by ${actorName}`
        }
        console.log(`Retrieved the commit ID, ${commitId}`);
    
        console.log("Now retrieving the approver's infos...");

        // Get the approver(reviewer) of the PR.
        let reviewer = getReviewer(responses[2]);
        if (!reviewer) {
            throw ("There was no approver!");
        }

        console.log(`PR #${prNumber} is good to cherry-pick.`);

        cherrypickRunner(commitId, prNumber, token, reviewer);







    }).catch((e) => {
        console.log(e);
    })
