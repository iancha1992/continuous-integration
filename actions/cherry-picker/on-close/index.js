const core = require('@actions/core');
const github = require('@actions/github');


const token = core.getInput("token");
const octokit = github.getOctokit(token);


console.log("Testing adam");
const payload = github.context.payload;

console.log(payload);


async function run() {
    const commentsResponse = await octokit.request(`GET /repos/iancha1992/gh_practice/issues/${issue_number}/comments`, {
        headers: {
            'X-GitHub-Api-Version': '2022-11-28'
        }
    });


    console.log("Comments?")
    console.log(commentsResponse.data)
}

run();
