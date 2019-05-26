#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import config
import os
import praw
import time

def bot_login():
	r = praw.Reddit(username = config.username,
		password = config.password,
		client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = "hotdog_bot")

	return r

def run_bot(r, comments_replied_to):
	for comment in r.subreddit("all").comments(limit = None):
		if "hotdog" in comment.body.lower() and comment.id not in comments_replied_to and comment.author != r.user.me() and "bot" not in comment.author.name.lower():
			comment.downvote()
			comment.reply("You put \"hotdog\", did you mean open-faced sausage sandwich? 🌭 \n***\n^I'm ^a ^bot *^bleep, ^bloop*")
			comments_replied_to.append(comment.id)

			with open("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))

	return comments_replied_to
	
def delete_negative_comments(comments):
	for comment in comments:
		if comment.score < 1:
			comment.delete()
			print("removed")

r = bot_login()
comments_replied_to = get_saved_comments()

while True:
	try:
		bot_comments = reddit.user.me().comments.new(limit = None)
		delete_negative_comments(bot_comments)
		run_bot(reddit, comments_replied_to)

	except Exception as e:
		print(e)
		continue