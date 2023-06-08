const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);

console.log("This is the real. Testing adam");
const payload = github.context.payload;
console.log(payload);
const issue_number = payload.number;


async function getPrEvents() {
    await octokit.request(`GET /repos/iancha1992/gh_practice/issues/${issue_number}/events`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    }).then(response => {
        console.log("This is the responseindex", response)
        return response
    })
    // .catch(err => {

    // })

    // console.log("Finalss")
    // console.log(gitIssueEventsResponse.data)
    // return gitIssueEventsResponse.data
};

const prEvents = async () => {
    return await getPrEvents()
}



console.log("This is the prevents PLANTS")
console.log(prEvents);
