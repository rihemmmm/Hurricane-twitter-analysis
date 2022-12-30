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
    start = datetime.strptime(date_since, "%Y-%m-%d")
    stop = datetime.strptime(date_until, "%Y-%m-%d")
    for i in range(0, numRuns): 
        next_fetch  = start + timedelta(seconds=940) 
        while start < stop and noTweets<500 : 
        
            tweets = tweepy.Cursor(api.search, q=search_words + " -filter:retweets", lang="en", exclude_replies=True,
                               include_rts=False, since=start,until =next_fetch, max_results=500,
                               tweet_mode='extended').items(numTweets)

            tweet_list = [tweet for tweet in tweets]
        
            noTweets = 0
            for tweet in tweet_list:
                username = tweet.user.screen_name
                location = tweet.user.location
                hashtags = tweet.entities['hashtags']
                # if it Not a Retweeted tweet run the following code

                text = tweet.full_text

                the_tweet = [username, location, text, hashtags]

                df_tweets.loc[len(df_tweets)] = the_tweet

                noTweets += 1
                
                tot_csv_timesamp = datetime.today().strftime('%Y%m%d_%H%M%S')

                # Defining a path for storing the collected tweet
                path = os.getcwd()
                filename = path + '/HurricaneIan/' + tot_csv_timesamp + 'Hurricane Ian.csv'

                # The pandas dataframe is converted into CSV fil Format.
                df_tweets.to_csv(filename, index=False)
            time.sleep(940)
            start  = start + timedelta(seconds=940) 

            
               


# Initialise the variable for the function created

search_words = 'Ian hurricane OR Ian storm OR Ian extreme Weather OR #Ian_hurricane OR Ian flooding OR Ian Climate change OR #Hurricane_Ian OR Ian disaster OR Ian Hurricane evacuation OR Ian tornado OR Ian Bad weather OR Bad_weather Ian OR Ian badweather OR Hurricane Ian extreme weather OR extreme_weather OR extremeweather OR extreme weather event OR extreme_weather_event OR extreme_weatherevent  OR Ian hurricane OR hurricanes IAN OR Ian_Hurricane OR Ian_storm OR storm_IAN OR Hurricanes OR hurricanes OR IAN_storm OR storms OR IAN Hurricane OR IAN_hurricane OR hurricane Ian OR Hurricane_Ian OR TORNADO OR Tornadoes OR Ian tornado OR IANTORNADO OR Ian_Tornado OR  Ian disaster OR disasters OR IAN_disaster OR climate weather hurricane OR  OR Ian flood OR IAN_flood OR flood Ian OR flood IAN OR Ian_flooding OR Evacuation Hurricane OR hurricane Evacuation OR Evacuation Ian OR Ian evacuation hurricane OR Ian_evacuation OR Ian hurricane hospital OR Ian_hurricane_hospital OR Ian emergency OR IAN EMERGENCY OR IAN EVACUATION OR IAN_emergency_evacuation OR doctors evacuation hurricane hospital OR Ian Health insurance OR Hurricane health access OR Hurricane_Hospital_access OR hurricane_hospital_acces OR health care system Ian OR Ian health care system OR #Ian_hurricane OR #Ian_storm OR #Ian_extreme_Weather OR #Ian_hurricane OR #Ian_flooding OR #Ian_climate_change OR #Hurricane_Ian OR #Ian_disaster OR #Ian_Hurricane_evacuation OR #IanHurricaneevacuation OR #Ian_tornado OR #Iantornado OR #Bad_weather OR #Ian_Bad_weather OR #Ian_badweather OR #Ian_extreme_weather OR #Hurricanes_extreme_weather OR #hurricane_extreme_weather_event OR #extreme_weatherevent  OR #Ian_hurricane OR #hurricanes  OR #Ian_Hurricane OR #Ian_storm OR #storm_IAN OR #Hurricanes OR #IAN_storm OR #storms OR #IAN_Hurricane OR #IAN_hurricane OR #Hurricane_Ian OR #TORNADO OR #Tornadoes OR #Ian_tornado OR #IANTORNADO OR #Ian_Tornado OR  #Ian_disaster OR #Iandisaster OR #IAN_disaster OR #climate_weather_hurricane OR #Ian_flood OR #IAN_flood OR #flood_Ian OR #flood_IAN OR #Ian_flooding OR #Evacuation_hurricane OR #Evacuation_Hurricane OR #hurricane_Evacuation OR #Evacuation_Ian OR #Ian_evacuation_hurricane OR #Ian_evacuation OR #Ian_hurricane_hospital OR #Ian_hurricane_hospital OR #Ian_emergency OR #IAN_EMERGENCY OR #IAN_EVACUATION OR #IAN_emergency_evacuation OR #doctors_evacuation_hurricane_hospital OR #Ian_Health_insurance OR #Hurricane_health_access OR #Hurricane_Hospital_access OR #hurricane_hospital_access OR #healthcare_system_Ian OR #Ian_healthcare_system  -is:retweet -is:reply place_country:US lang:en '

date_since = '2022-09-19'
NumberOfTweets = 2500
NumberOfRuns = 6
date_until = '2022-11-14'
# Call the function tweetcollector
tweetcollector(search_words, date_since, date_until, NumberOfTweets, NumberOfRuns)
