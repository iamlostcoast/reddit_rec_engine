# Reddit Recommendation Project

In these notebooks, I am building a recommendation engine for Reddit, which specifically recommends particular subreddits.

### Data

Instead of ratings, I'm using user comments as a proxy. The data was pulled from the Reddit API in two steps.
First I pull a list of Reddit usernames from the comment stream, and then pull all the comments those users have ever written.  The scripts for pulling down that data from the API are in this repo

### Rec Engine

I explored using a few types of recommendation engine systems, including collaborative filtering using cosine similarities and singular value decomposition.


