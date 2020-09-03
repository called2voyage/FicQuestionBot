# Copyright 2018-2020 called2voyage
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import praw
from prawutils.submissions import loop_submissions, search_title
import re
import os
import time
from random import randint

reddit = praw.Reddit('bot1')
print(reddit.user.me())
subreddit = reddit.subreddit("IAmAFiction")
print(subreddit)

def ask_question(submission, *args):
    posts_replied_to = args[0]
    questions = args[1]
    print("Accessing new")
    if submission.id not in posts_replied_to:
        print("Accessing submission")
        if search_title(submission, "\[Fic\]", "AMA"):
            success = False
            while not success:
                try:
                    submission.reply(questions[randint(0, len(questions)-1)])
                    success = True
                except praw.exceptions.APIException as e:
                    time.sleep(660)
            print("Bot replying to : ", submission.title)
            posts_replied_to.append(submission.id)

questions = []

with open('questions.txt', 'r') as f:
    questions_list_str = ""
    for line in f:
        questions_list_str = '%s%s' % (questions_list_str, line)
    questions = eval(questions_list_str)

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

loop_submissions(subreddit, ask_question, 10, posts_replied_to, questions)

with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
