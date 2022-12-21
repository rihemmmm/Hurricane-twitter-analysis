import configparser
import pandas as pd
import tweepy


# read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


keywords= 'Ian hurricane (Ian storm OR extreme Weather OR #Ian OR flooding Hospital OR Climate change OR #Hurricane ' \
          'OR Ian storm Mental Health -is:retweet -is:reply place_country:US lang:en) -is:retweet -is:reply ' \
          'place_country:US lang:en '

limit=500
tweets = tweepy.Cursor(api.search_tweets, q=keywords, count=100 ,lang="en", tweet_mode='extended',exclude_replies=True, include_rts = False ,since='2022-09-20',until='2022-11-14').items(limit)
# create dataframe
columns = ['Time', 'User', 'Tweet']
data = []
for tweet in tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])

df = pd.DataFrame(data, columns=columns)

df.to_csv('tweets.csv')
