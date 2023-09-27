issue_comment_body = f"The following commits were cherry-picked in 123, 234, 4556, 789, "

issue_comment_body = issue_comment_body[::-1].replace(" ,", ".", 1)[::-1]


print(issue_comment_body)