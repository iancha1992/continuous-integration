import requests
from pprint import pprint

def get_all_milestones_data():
    headers = {
        'X-GitHub-Api-Version': '2022-11-28'
    }
    r = requests.get(f'https://api.github.com/repos/iancha1992/bazel/milestones', headers=headers)
    print("tupac")
    pprint(r.json())
    return r.json()


def extract_release_numbers_data():
    milestones_data = get_all_milestones_data()

    
