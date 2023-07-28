


# release_number = "6.3.0"

release_number = "6.3.1"

# release_number = "6.3.0"

last_digit = release_number.split(".")[2]

print(last_digit)


if int(last_digit) == 0:
    pass

else:
    previous_release_number =  + str(int(last_digit) + 1)
    # previous_release_number = release_number.split(".")[2]
    # previous_release_number = str(int(release_number[-1]) + 1)
    # print(previous_release_number)



