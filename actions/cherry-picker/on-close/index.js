const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);

const payload = github.context.payload;
console.log("This is the payload");
console.log(payload);
const issue_number = payload.number;

async function getPrEventsInfos() {
    const response = await octokit.request(`GET /repos/iancha1992/gh_practice/issues/${issue_number}/events`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });
    console.log("MMMMMMMMM", response.data)
    return response.data




    // .then(response => {
    //     console.log("This is the responseindex", response.data);
    //     prEventsInfos = response.data
    //     // return response.data;
    // });

};

// getPrEventsInfos().then((response) => {
//     prEventsInfos = response
//     // commidId = getCommitId();

// });

Promise.all([getPrEventsInfos()])
    .then((responses) => {
        console.log("Congress")
        console.log(responses);
        for (const response of responses) {
            console.log(response)
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