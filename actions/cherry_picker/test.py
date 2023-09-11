# import re

# # def hi(a):
# #     if a == "bye":
# #         print("hihihi")




# # hi("aaaa")

# url = "https://github.com/iancha1992/bazel/commit/a2b775467c1b36bd1c935d35770916105cd7102d"




# new_url = re.sub(r'https://.*/commit/', "", url)

# # flags=re.IGNORECASE

# print(new_url)



# class IanException(Exception):
#     # print("mynameiseminem!")
#     pass

# raise IanException("hiya!!!!!")



# yoyo = str({"awefwef": "aaaaa"})


# print(yoyo["awefwef"])

# yoyo = {"awefwef": "aaaaa"}





# # print(yoyo)
# print(type(yoyo) is dict)





class PushCpException(Exception):
    pass

class GeneralCpException(Exception):
    pass







try:
    raise PushCpException("hi")
except PushCpException as e:
    print("byeah!")
except Exception as e:
    print("hiya!!!!!!")
