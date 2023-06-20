const cherrypickRunner = require("../cherry-pick-runner/index.js");
const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);
const payload = github.context.payload;
const triggeredOn = core.getInput("triggered-on");

if (triggeredOn == "commented") {
    var prNumber = payload.issue.body.split("#")[1];
}

else if (triggeredOn == "closed") {
    var prNumber = payload.number;
}

console.log("This is the payload", payload);

async function getIssueEventsInfos() {
    const response = await octokit.request(`GET /repos/iancha1992/bazel/issues/${prNumber}/events`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        },
        per_page: 100
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

// async function getMilestonedIssues() {
//     const response = await octokit.request(`GET /repos/iancha1992/bazel/issues`, {
//         headers: {
//             'X-GitHub-Api-Version': '2022-11-28'
//         },
//         per_page: 100,
//         milestone: 1

//     });
//     return response.data;
// }

async function getAllMilestonesIdsAndTitles() {
    const response = await octokit.request(`GET /repos/iancha1992/bazel/milestones`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });
    let milestonedIssues = [];
    response.data.map((item) => {
        milestone = {
            title: item.title.split("release blockers")[0].replace(" ", ""),
            number: item.number
        };
        milestonedIssues.push(milestone);
    });
    console.log("Now requesting for milestonedIssues Infos...")
    let finalData = [];
    for (let issue of milestonedIssues) {
        const issuesData = await octokit.request(`GET /repos/iancha1992/bazel/issues`, {
            headers: {
                'X-GitHub-Api-Version': '2022-11-28'
            },
            milestone: issue.number
        });
        console.log("This is the milestonedissues", issuesData);
        // const filteredMilestonedIssues = issuesData.data.filter((item) => item.body == `Forked from #${prNumber}`);
        for (let forkedIssue of issuesData.data) {
            if (forkedIssue.body == `Forked from #${prNumber}`) {
                data = {
                    issueNumber: forkedIssue.number,
                    releaseNumber: issue.title,
                }
                finalData.push(data);
                break;
            }
        }
        console.log("This is the final data", finalData);
    };


};

async function getAllIssuesForIssue() {
    pass
}

// getAllMilestonesIdsAndTitles().then(response => {
//     console.log("water");
//     console.log(response);
// })


// function() {
//     getAllMilestones()
// };

let cherrypickData;


function getCommitId(issueEvents) {
    const actorName = "iancha1992";
    // const actorName = "copybara-service[bot]";
    const actionEvent = "merged";
    // const actionEvent = "closed";
    let commitId = null;

    console.log("This is the issueEvents", issueEvents);

    for (let e of issueEvents) {
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
    if (reviews.length == 0) {
        return null
    }

    let approvers_list = [];
    for (let review of reviews) {
        if (review.state == "APPROVED") {
            let data = {
                "login": review.user.login,
                "id": review.user.id
            }
            approvers_list.push(data)
        }
    }
    return approvers_list;
}





function extractReleaseNumber() {
    // if (triggeredOn == "commented") {
    //     return payload.issue.milestone.title.split("release blockers")[0]
    // }
    // else if (triggeredOn == "closed") {
    //     getAllMilestonesIdsAndTitles().then(response => {
    //         console.log("water");
    //         console.log(response);
    //     })
    // }

    getAllMilestonesIdsAndTitles().then(response => {
        console.log("water");
        console.log(response);
        // milestoneNumber = response.number;



    })
}

Promise.all([getPrEventsInfos(), getIssueEventsInfos(), getReviews()])
    .then((responses) => {
        console.log(`Checking if Pull Request #${prNumber} is closed...`);

        // Check if the PR was closed.
        if (responses[0].state != "closed") {
            // Needs better implemention for throwing error here later
            throw (`Pull Request #${prNumber} is not closed yet. Only closed ones are cherry-pickable.`);
        }
        console.log(`Confirmed that Pull Request #${prNumber} is closed.`);

        // Check if there is exactly one Copybara commit ID.
        console.log("Now checking if there is a commit ID..");
        let commitId = getCommitId(responses[1]);
        if (commitId == null) {
            throw `There is no available commit made!`
        }
        console.log(`Retrieved the commit ID, ${commitId}`);
    
        // Get the approver(reviewer) of the PR.
        console.log("Now retrieving the approver's infos...");
        let reviewer = getReviewer(responses[2]);
        if (!reviewer) {
            throw ("There was no approver!");
        }
        console.log(reviewer);
        console.log(`PR #${prNumber} is good to cherry-pick.`);

        const releaseNumber = extractReleaseNumber();

        // let cherrypickData;

        // if (triggeredOn == "commented") {
        //     pass
            
            
        // }
        
        // else if (triggeredOn == "closed") {
        //     pass
        // }

        // let cherrypickData = 

        cherrypickRunner(commitId, prNumber, token, reviewer, releaseNumber);

    }).catch((e) => {
        console.log(e);
    })


