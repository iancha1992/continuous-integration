const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);

const payload = github.context.payload;
console.log("This is the payload");
console.log(payload);
const issue_number = payload.number;

async function getPrEventsInfos() {
    // const response = await octokit.request(`GET /repos/iancha1992/gh_practice/issues/${issue_number}/events`, {
    //     headers: {
    //         'X-GitHub-Api-Version': '2022-11-28'
    //     }
    // });

    const response = await octokit.request(`GET /repos/bazelbuild/bazel/issues/18305/events`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });
    return response.data;
};


// getPrEventsInfos().then((response) => {
//     prEventsInfos = response
//     // commidId = getCommitId();

// });

let commitId;

Promise.all([getPrEventsInfos()])
    .then((responses) => {
        console.log("Congress")
        console.log(responses);

        // Checking events
        for (const response of responses[0]) {
            // console.log(response);
            // console.log("Goooooogle", typeof response.commit_id);
            if ((response.actor.login == "copybara-service[bot]") && (response.commit_id != null)) {
                // commitId = response.commit_id
                // console.log(commitId)
                // console.log(typeof response.commit_id)
                console.log("FAnta")
            };

            // console.log("This is commit ID!!!!", commitId)
        }

        

    })






// function getCommitId() {
//     console.log("NBA", prEventsInfos)
//     for (info of prEventsInfos) {
//         console.log("brady", info)
//     }

// };

// commidId = getCommitId();





// function isCherryPickable() {
//     getPrEvents()
//         .then((response) => {
            
//             console.log("defense", response)
//         })

//     return true
// };

// if (isCherryPickable() == true) {
//     console.log("hihi")
// }