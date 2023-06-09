const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);

const payload = github.context.payload;

console.log("Gomez")
console.log("This is the payload");
console.log(payload);

// const issue_number = payload.number;

// async function getPrEventsInfos() {
//     const response = await octokit.request(`GET /repos/bazelbuild/bazel/issues/18130/events`, {
//         headers: {
//             'X-GitHub-Api-Version': '2022-11-28'
//         }
//     });
//     return response.data;
// };


// let commitId;

// Promise.all([getPrEventsInfos()])
//     .then((responses) => {
//         console.log("Congress")
//         console.log(responses);

//         for (const response of responses[0]) {
//             if ((response.actor.login == "copybara-service[bot]") && (response.commit_id != null) && (commitId == null)) {
//                 commitId = response.commit_id
//                 console.log("FAnta");
//                 console.log(commitId)
//             }
//             else if ((response.actor.login == "copybara-service[bot]") && (response.commit_id != null) && (commitId != null)) {
//                 console.log("Anotherone")
//                 console.log(commitId)
//                 throw "There are multiple commits made by copybara-service[bot]. There can only be one."
//             }
//         }
//     })
