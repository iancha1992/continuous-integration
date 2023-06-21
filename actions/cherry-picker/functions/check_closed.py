import requests
def check_closed(pr_number):
    print("Closing!")
    r = requests.get(f'/repos/iancha1992/bazel/pulls/{pr_number}')
    print(r.text)
    



