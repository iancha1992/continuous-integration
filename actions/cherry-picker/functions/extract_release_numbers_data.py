import requests
from pprint import pprint

def get_all_milestones_data():
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/milestones', headers=headers)
    print("tupac")
    # pprint(r.json())

    milestones_data = list(map(lambda n: {"title": n["title"].split("release blockers")[0].replace(" ", ""), "number": n["number"]}, r.json()))
    return milestones_data


def extract_release_numbers_data():
    milestones_data = get_all_milestones_data()
    print("This is milestones_Datss", milestones_data)

    
