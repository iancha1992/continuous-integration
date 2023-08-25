import re

# def hi(a):
#     if a == "bye":
#         print("hihihi")




# hi("aaaa")

url = "https://github.com/iancha1992/bazel/commit/a2b775467c1b36bd1c935d35770916105cd7102d"




new_url = re.sub(r'https://.*/commit/', "", url)

# flags=re.IGNORECASE

print(new_url)