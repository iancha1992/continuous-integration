import requests
from pprint import pprint

def get_all_milestones_data():
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/milestones', headers=headers)
    milestones_data = list(map(lambda n: {"title": n["title"].split("release blockers")[0].replace(" ", ""), "number": n["number"]}, r.json()))
    return milestones_data

def get_milestoned_issues(milestones, pr_number):
    print("get_milestoned_issues()")
    pprint(milestones)
    results= {}
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    for milestone in milestones:
        params = {
            "milestone": milestone["number"]
        }
        r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues', headers=headers, params=params)
        print("quietresults")
        pprint(r.json())
        for issue in r.json():
            if issue["body"] == f'Forked from #{pr_number}' and issue["state"] == "open":
                # data = {
                #     "issue_number": issue["number"],
                #     "release_number": milestone["title"]
                # }
                results[milestone["title"]] = issue["number"]
                break
    print("results for get_imlestoned_issues")
    pprint(results)
    return results

def extract_release_numbers_data(pr_number):
    milestones_data = get_all_milestones_data()
    milestoned_issues = get_milestoned_issues(milestones_data, pr_number)
    return milestoned_issues
