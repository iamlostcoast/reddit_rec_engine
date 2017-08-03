rimport pandas as pd
import numpy as np
import requests
import sqlite3
import datetime
import time
import global_vars

conn = sqlite3.Connection("./reddit_rec_data.sqlite")

client_auth = requests.auth.HTTPBasicAuth('i0viuENaWrt_NA', 'AEjbSfKYCg1AK-mxF-dh7N6lp6c')
post_data = {"grant_type": "password", "username": "iamlostcoast", "password": global_vars.get_reddit_pass()}
headers = {"User-Agent": "bot 0.1"}
access_response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth,
                                data=post_data, headers=headers)
access_token = access_response.json()['access_token'].encode('ascii')
auth_headers = {"Authorization": "bearer %s" % access_token, "User-Agent": "bot 0.1"}

def get_user_comments(authors, auth_headers, allowed_fails=10):
    fails = 0
    comments_dict = {}
    print datetime.datetime.now()
    for i, author in enumerate(authors):
        response = requests.get("https://reddit.com/user/%s/comments.json" % author, headers=auth_headers)
        data = None
        try:
            data = response.json()
        except:
            print "Error: ", response.status_code
            time.sleep(2)
            if fails < allowed_fails:
                fails += 1
                continue
            else:
                break
        # going to save this user's upvotes to a new dictionary
        user_sub_comms = {}

        # Need to set fails back to 0 if we get here, only want to fully break if we're getting many successive fails
        fails = 0
        # we're sometimes getting down to the next loop with a json file with no data.  Let's do a try except that will stop that.
        try:
data_test = data['data']
        except:
            continue

        # we can scroll through meta data on upvoted articles in the data/children elements of the json file
        for element in data['data']['children']:
            subreddit = element['data']['subreddit_name_prefixed']
            if subreddit in user_sub_comms.keys():
                user_sub_comms[subreddit] += 1
            else:
                user_sub_comms[subreddit] = 1

        comments_dict[author] = user_sub_comms
        if i % 100 == 0:
            print 'current iteration: ', i
            print 'current time: ', datetime.datetime.now()
            time.sleep(2)
    return comments_dict


authors = pd.read_sql("SELECT * FROM author_names", con=conn)
print "Count of authors: ", len(set(authors))
print authors.shape
print authors.columns
authors = authors.iloc[:, 1].tolist()

authors = pd.read_sql("SELECT * FROM authors;", con=conn)
print "Count of authors: ", len(set(authors))
print authors.shape
print authors.columns
authors = authors.iloc[:, 1].tolist()

for i in range(200):
    print 'author_range: ', i*1000, (i+1)*1000
    author_list = list(set(authors))[i*1000:(i+1)*1000]
    if len(author_list) == 0:
        break
    comments = get_user_comments(authors=author_list, auth_headers=auth_headers)
    comments_df = pd.DataFrame(comments).T
    comments_df.reset_index(inplace=True)
    comments_df.rename(columns={'index': 'user'}, inplace=True)
    user_columns = [c for c in comments_df.columns if c != 'user']
    comments_long = pd.melt(comments_df, value_vars=user_columns, id_vars=['user']).dropna().reset_index(drop=True)

    comments_long.to_sql('comment_data', con=conn, if_exists='append')
    comments_long.to_csv('comment_data_%s.csv' % str(i), index=False)
    time.sleep(2)
