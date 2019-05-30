import praw
import pdb
import re
import os
import time
from random import randint

reddit = praw.Reddit('bot1')
print(reddit.user.me())
subreddit = reddit.subreddit("IAmAFiction")
print(subreddit)

questions = [
    "Question 1",
    "Question 2",
]

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

for submission in subreddit.new(limit=10):
    print("Accessing new")
    if submission.id not in posts_replied_to:
        print("Accessing submission")
        if re.search("\[Fic\]", submission.title, re.IGNORECASE) or re.search("AMA", submission.title, re.IGNORECASE):
            success = False
            while not success:
                try:
                    submission.reply(questions[randint(0, len(questions)-1)])
                    success = True
                except praw.exceptions.APIException as e:
                    time.sleep(660)
            print("Bot replying to : ", submission.title)
            posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
