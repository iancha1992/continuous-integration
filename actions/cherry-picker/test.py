import requests, subprocess
from pprint import pprint

headers = {
    'X-GitHub-Api-Version': '2022-11-28',
}



# git shortlog -s -n -e


# # url = 'https://api.github.com/repos/bazelbuild/bazel/issues/19173/comments'
# url = 'https://api.github.com/repos/bazelbuild/bazel/collaborators'

# url = "https://api.github.com/users/iancha1992/social_accounts"

# url = "https://api.github.com/users/iancha1992/social_accounts"

url = "https://api.github.com/users/haxorz/events/public"

# r = requests.get(url, headers=headers)


def taylor():
    print("Taylor!!!")
    raise Exception("hihihi")

try:
    print("Hello world")
    taylor()
    print("Bye")

except Exception as e:
    print("Except!!!!")
    # print(e)
    print("cherry", str(e))
    print("cherry", str(e), "aaaa", "Cccc")
    # print("cherry", type(str(e)))