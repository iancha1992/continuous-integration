const core = require('@actions/core');
const github = require('@actions/github');
const token = core.getInput("token");
const octokit = github.getOctokit(token);

const payload = github.context.payload;
console.log("This is the payload");
console.log(payload);

console.log("hello world!");
