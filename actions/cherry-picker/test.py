import requests



# 19173

headers = {
    'X-GitHub-Api-Version': '2022-11-28'
}
# url = 'https://api.github.com/repos/bazelbuild/bazel/issues/19173/comments'
url = 'https://api.github.com/repos/iancha1992/bazel/issues/239/comments'
myobj = {
    'body': 'testing',
}

r = requests.post(url, headers=headers, json=myobj)
# x = requests.post(url, json = myobj)

print(r.text)