import base64
import configparser
import time
import requests
import pandas as pd
# Replace these with your own keys and tokens
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_secret_key = config['twitter']['api_key_secret']

access_token = config['twitter']['access_tokenn']
access_token_secret = config['twitter']['access_token_secret']

# Concatenate the keys and tokens
bearer_token_credentials = api_key + ':' + api_secret_key

# Base64 encode the credentials
bearer_token_credentials_bytes = bearer_token_credentials.encode('ascii')
base64_encoded_bearer_token_credentials = base64.b64encode(bearer_token_credentials_bytes).decode('ascii')

# Create the headers for the request
headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Authorization": f"Basic {base64_encoded_bearer_token_credentials}"
}

# Make the request to the API
response = requests.post("https://api.twitter.com/oauth2/token", headers=headers, data={"grant_type": "client_credentials"})

# Get the bearer token from the response
bearer_token = response.json()["access_token"]

# Use the bearer token to authenticate future requests
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

# Set the initial max_position to None
max_position = None

# Define the query and other parameters
query = '("Hurricane" OR "Storm" OR "Extreme Weather" OR "Flooding" OR "Climate Change" OR "Tornado" OR "Bad Weather" ' \
        'OR "Extreme Weather Event") ( "Ian" OR "#Ian" OR "#Ian_hurricane" OR "#Ian_storm" OR ' \
        '"#Ian_extreme_Weather" OR "#Ian_flooding" OR "#Ian_climate_change" OR "#Hurricane_Ian" OR "#Ian_disaster" OR ' \
        '"#Ian_tornado" OR "#Ian_badweather" OR "#Ian_extreme_weather" OR "#Ian_tornado" OR "#Ian_Tornado" OR ' \
        '"#Ian_disaster" OR "#climate_weather_hurricane" OR "#Ian_flood" ) ("Evacuation" OR ' \
        '"Emergency" OR "EVACUATION" OR "Hospital" OR "Health Insurance" OR "Health Access" OR "Hospital Access" OR ' \
        '"Health Care System" OR "#hurricane_Evacuation" OR "#Evacuation_Ian" OR "#Ian_evacuation_hurricane" OR ' \
        '"#Ian_evacuation" OR "#Ian_hurricane_hospital" OR "#Ian_emergency" OR "#ian_EVACUATION" OR ' \
        '"#ian_emergency_evacuation" OR "#Ian_Health_insurance" OR "#Hurricane_health_access" OR ' \
        '"#hurricane_hospital_access" OR "#healthcare_system_Ian" OR "#Ian_Hurricane_evacuation") lang:en -is:retweet ' \
        '-is:reply '

# Create a variable to keep track of the number of tweets fetched
numberoftweets = 0

# Define the endpoint
endpoint = 'https://api.twitter.com/2/tweets/search/all'
# Define the start and end date
start_date = '2022-09-20T00:00:00Z'
end_date = '2022-10-20T00:00:00Z'

# Fetch tweets in a loop, updating the max_position each time
df = pd.DataFrame()
tweet_ids = set() # set to store tweet ids
while True:
    # Define the parameters
    params = {
        "query": query,
        "max_position": max_position,
        "start_time": start_date,
        "end_time": end_date,
        "tweet.fields": "created_at",

    }
    # Make the request
    response = requests.get(endpoint, headers=headers, params=params)
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    # Check the rate limit headers
    rate_limit_remaining = response.headers.get("x-rate-limit-remaining")
    rate_limit_reset = response.headers.get("x-rate-limit-reset")

    # If the rate limit has been exceeded, wait until the rate limit resets
    if rate_limit_remaining and int(rate_limit_remaining) == 0:
        reset_time = int(rate_limit_reset)
        current_time = int(time.time())
        wait_time = reset_time - current_time
        if wait_time > 0:
            time.sleep(wait_time)
            continue

    if response.status_code == 200:
        # Get the tweets
        tweets = response.json()['data']
        # Iterate over the tweets and process them as needed
        for tweet in tweets:
            print(tweet)
            # add the tweet id to the set
            tweet_ids.add(tweet['id'])
            numberoftweets += 1
            if numberoftweets >= 500:
                    break
        end_time = tweets[-1]['created_at']

        # Update max_position with the next_token value
        max_position = response.json()['meta']['next_token']

        # Convert the response to a pandas dataframe

        data = response.json()
        df = pd.concat([df, pd.DataFrame.from_records(data["data"])], ignore_index=True)
        # Write the dataframe to a CSV file
        df.to_excel('twitter_data_ian2.xlsx', index=False)

        # check if the response has next_position, if not break the loop
        if 'next_position' not in response.json():
            break
    else:
        print(f'Error: {response.status_code}')
        print(response.text)


print(end_time)
