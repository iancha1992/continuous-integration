import requests
from pprint import pprint

def get_all_milestones_data():
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/milestones', headers=headers)
    milestones_data = list(map(lambda n: {"title": n["title"].split("release blockers")[0].replace(" ", ""), "number": n["number"]}, r.json()))
    return milestones_data

def get_milestoned_issues(milestones):
    results= {}
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    for milestone in milestones:
        params = {
            milestone: milestone["number"]
        }
        r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/issues', headers=headers, params=params)
        print("quietresults")
        pprint(r.json())










def extract_release_numbers_data():
    milestones_data = get_all_milestones_data()
    milestoned_issues = get_milestoned_issues(milestones_data)

