import json
import pandas as pd
import csv
import re
from textblob import TextBlob
import string
import os
import time
from twitter_credentials import *
from datetime import datetime

from datetime import timedelta


# Libraries for Twitter API
import tweepy
from tweepy import OAuthHandler

# Accessing the credentials from twitterapi.py
from twitter_api import access_token

accesstoken = access_token
accesstokensecret = access_secret_token
apikey = api_key
apisecretkey = api_security_key

# Connecting to Twitter API
auth = OAuthHandler(apikey, apisecretkey)
auth.set_access_token(accesstoken, accesstokensecret)
api = tweepy.API(auth)


def tweetcollector(search_words, date_since, date_until, numTweets, numRuns):
    # Define a pandas dataframe to store the data
    df_tweets = pd.DataFrame(columns=['username', 'location', 'text', 'hashtags']
                             )
    program_start = time.time()                          
    start = datetime.strptime(date_since, "%Y-%m-%d")
    stop = datetime.strptime(date_until, "%Y-%m-%d")
    for i in range(0, numRuns):
        next_day  = start + timedelta(days=1) 
        while start < stop  : 
            next_day  = start + timedelta(days=1)    

            tweets = tweepy.Cursor(api.search, q=search_words + " -filter:retweets", lang="en", exclude_replies=True,
                               include_rts=False, since=start, until=next_day,
                               tweet_mode='extended').items(numTweets)

            tweet_list = [tweet for tweet in tweets]
        
            noTweets = 0
            for tweet in tweet_list:

                username = tweet.user.screen_name
                location = tweet.user.location
                hashtags = tweet.entities['hashtags']

                try:
                    # Check wether the tweet was re-tweeted.

                    text = tweet.retweeted_status.full_text

                except AttributeError:

                    # if it Not a Retweeted tweet run the following code

                    text = tweet.full_text

                    the_tweet = [username, location, text, hashtags]

                    df_tweets.loc[len(df_tweets)] = the_tweet

                    noTweets += 1
                

                    # 15 minute sleep time because of twitter requests limitation.
                    
                    time.sleep(940)

                    tot_csv_timesamp = datetime.today().strftime('%Y%m%d_%H%M%S')

                    # Defining a path for storing the collected tweet
                    path = os.getcwd()
                    filename = path + '/HurricaneIan/' + tot_csv_timesamp + 'Hurricane Ian.csv'

                # The pandas dataframe is converted into CSV fil Format.
                    df_tweets.to_csv(filename, index=False)
            start = start + timedelta(days=1)
               


# Initialise the variable for the function created

search_words = 'Ian hurricane OR Ian storm OR Ian extreme Weather OR #Ian_hurricane OR Ian flooding OR Ian Climate change OR #Hurricane_Ian OR Ian disaster OR Ian Hurricane evacuation OR Ian tornado  -is:retweet -is:reply place_country:US lang:en'

date_since = '2022-09-20'
NumberOfTweets = 2500
NumberOfRuns = 6
date_until = '2022-11-14'
# Call the function tweetcollector
tweetcollector(search_words, date_since, date_until, NumberOfTweets, NumberOfRuns)
