import json
import pandas as pd
import re
from textblob import TextBlob
import string
import os
import time
from datetime import datetime
from datetime import timedelta
# Libraries for Twitter API
import tweepy
import configparser
from tweepy import OAuthHandler

# Connecting to Twitter API
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_tokenn']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def tweetcollector(search_words, date_since, date_until, NumberOfTweets, NumberOfRuns):
    # Define a pandas dataframe to store the data
    df_tweets = pd.DataFrame(columns=['username', 'location', 'text', 'hashtags']
                             )

    for i in range(0, NumberOfRuns):
        # We will time how long it takes to scrape tweets for each run:

        tweets = tweepy.Paginator(api.search, q=search_words + " -filter:retweets", lang="en", exclude_replies=True,
                               include_rts=False, since=date_since, until=date_until,
                               tweet_mode='extended').flatten(limit=NumberOfTweets)

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
                time.sleep(920)

                tot_csv_timesamp = datetime.today().strftime('%Y%m%d_%H%M%S')

                # Defining a path for storing the collected tweet
                path = os.getcwd()
                filename = path + '/HurricaneIan/' + tot_csv_timesamp + 'Hurricane Ian.csv'

                # The pandas dataframe is converted into CSV fil Format.
                df_tweets.to_csv(filename, index=False)
    print (tweet_list)



# Initialise the variable for the function created

search_words = 'Ian hurricane OR Ian storm OR Ian extreme Weather OR #Ian_hurricane OR Ian flooding OR Ian Climate ' \
               'change OR #Hurricane_Ian OR Ian disaster OR Ian Hurricane evacuation OR Ian tornado OR Ian Bad ' \
               'weather OR Bad_weather Ian OR Ian badweather OR Hurricane Ian extreme weather OR extreme_weather OR ' \
               'extremeweather OR extreme weather event OR extreme_weather_event OR extreme_weatherevent  OR Ian ' \
               'hurricane OR hurricanes IAN OR Ian_Hurricane OR Ian_storm OR storm_IAN OR Hurricanes OR hurricanes OR ' \
               'IAN_storm OR storms OR IAN Hurricane OR IAN_hurricane OR hurricane Ian OR Hurricane_Ian OR TORNADO OR ' \
               'Tornadoes OR Ian tornado OR IANTORNADO OR Ian_Tornado OR  Ian disaster OR disasters OR IAN_disaster ' \
               'OR climate weather hurricane OR  OR Ian flood OR IAN_flood OR flood Ian OR flood IAN OR Ian_flooding ' \
               'OR Evacuation Hurricane OR hurricane Evacuation OR Evacuation Ian OR Ian evacuation hurricane OR ' \
               'Ian_evacuation OR Ian hurricane hospital OR Ian_hurricane_hospital OR Ian emergency OR IAN EMERGENCY ' \
               'OR IAN EVACUATION OR IAN_emergency_evacuation OR doctors evacuation hurricane hospital OR Ian Health ' \
               'insurance OR Hurricane health access OR Hurricane_Hospital_access OR hurricane_hospital_acces OR ' \
               'health care system Ian OR Ian health care system OR #Ian_hurricane OR #Ian_storm OR ' \
               '#Ian_extreme_Weather OR #Ian_hurricane OR #Ian_flooding OR #Ian_climate_change OR #Hurricane_Ian OR ' \
               '#Ian_disaster OR #Ian_Hurricane_evacuation OR #IanHurricaneevacuation OR #Ian_tornado OR #Iantornado ' \
               'OR #Bad_weather OR #Ian_Bad_weather OR #Ian_badweather OR #Ian_extreme_weather OR ' \
               '#Hurricanes_extreme_weather OR #hurricane_extreme_weather_event OR #extreme_weatherevent  OR ' \
               '#Ian_hurricane OR #hurricanes  OR #Ian_Hurricane OR #Ian_storm OR #storm_IAN OR #Hurricanes OR ' \
               '#IAN_storm OR #storms OR #IAN_Hurricane OR #IAN_hurricane OR #Hurricane_Ian OR #TORNADO OR #Tornadoes ' \
               'OR #Ian_tornado OR #IANTORNADO OR #Ian_Tornado OR  #Ian_disaster OR #Iandisaster OR #IAN_disaster OR ' \
               '#climate_weather_hurricane OR #Ian_flood OR #IAN_flood OR #flood_Ian OR #flood_IAN OR #Ian_flooding ' \
               'OR #Evacuation_hurricane OR #Evacuation_Hurricane OR #hurricane_Evacuation OR #Evacuation_Ian OR ' \
               '#Ian_evacuation_hurricane OR #Ian_evacuation OR #Ian_hurricane_hospital OR #Ian_hurricane_hospital OR ' \
               '#Ian_emergency OR #IAN_EMERGENCY OR #IAN_EVACUATION OR #IAN_emergency_evacuation OR ' \
               '#doctors_evacuation_hurricane_hospital OR #Ian_Health_insurance OR #Hurricane_health_access OR ' \
               '#Hurricane_Hospital_access OR #hurricane_hospital_access OR #healthcare_system_Ian OR ' \
               '#Ian_healthcare_system  -is:retweet -is:reply place_country:US lang:en '

date_since = '2022-09-19'
NumberOfTweets = 3000
NumberOfRuns = 6
date_until = '2022-09-20'
# Call the function tweetcollector
tweetcollector(search_words, date_since, date_until, NumberOfTweets, NumberOfRuns)




