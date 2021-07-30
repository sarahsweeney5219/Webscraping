from psaw import PushshiftAPI
import psycopg2
import datetime
import csv
import pandas as pd

api = PushshiftAPI()

start_time = int(datetime.datetime(2021,1,30).timestamp())

posts = api.search_submissions(after=start_time,
                            subreddit='wallstreetbets',
                            filter=['url','author', 'title', 'subreddit']
                            )
count = 0
while count < 100:
    for post in posts:
        word = post.title.split()
        #see if maybe we can replace this with a lambda?
        tickers = list(set(filter(lambda word: word.lower().startswith('$'), word)))
        if len(tickers) > 0:
            count += 1
            ticker = tickers[0]
            postTitle = post.title
            postTicker = ticker
            postAuthor = post.author
            postUrl = post.url
            print(postTicker, postTitle, postUrl, postAuthor, postUrl, sep=" ")



