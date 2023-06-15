const cherrypickRunner = (commitId, prNumber, token, reviewer, releaseNumber) => {
    console.log(`Running cherrypicking with commitID ${commitId}, PR#${prNumber}`);
    console.log("Reviewers!!!");
    console.log(reviewer);
    console.log("This is the releaseNumber");
    console.log(releaseNumber);
}

module.exports = cherrypickRunner;