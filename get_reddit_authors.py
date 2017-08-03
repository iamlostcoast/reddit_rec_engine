import pandas as pd
import praw
import sqlite3
import requests.auth
import requests
import global_vars

conn = sqlite3.Connection("./reddit_rec_data.sqlite")

r = praw.Reddit(client_id = 'i0viuENaWrt_NA', client_secret='AEjbSfKYCg1AK-mxF-dh7N6lp6c', user_agent = "bot 0.1",
               password=global_vars.get_reddit_pass(), username='iamlostcoast')

# Let's just make a long list of authors.

# we'll start off with 200000
authors = []
for (i, comment) in enumerate(r.subreddit('all').stream.comments()):
    if i <= 200000:
        authors.append(comment.author)
        # Going to check in every 10000
        if i % 10000 == 0:
            print "Count of iterations: ", i
            # Seems like there's a problem with the number of authors we're getting, after
            # running the script we only got about 1500?
            print "Count of distinct authors: ", len(set(authors))
    else:
        break

# Let's go ahead and save all these to our local db

author_strings = pd.Series([author.name.encode('ascii') for author in authors])
author_strings.to_sql('author_names', con=conn, if_exists='replace')
author_strings.to_csv("author_names.csv")
