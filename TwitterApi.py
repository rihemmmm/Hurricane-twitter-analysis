import requests
import base64
import json
import time
import configparser
import twitter_credentials

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
query = 'Ian hurricane OR Ian storm OR Ian extreme Weather OR #Ian_hurricane OR Ian flooding OR Ian Climate ' \
               'change OR #Hurricane_Ian -is:retweet -is:reply place_country:US lang:en '


# Define the endpoint
endpoint = 'https://api.twitter.com/2/tweets/search/all'
# Define the start and end date
start_date = '2022-09-19T00:00:00Z'
end_date = '2022-09-20T00:00:00Z'

# Fetch tweets in a loop, updating the max_position each time
while True:
    # Define the parameters
    params = {
        "query": query,
        "max_position": max_position,
        "start_time": start_date,
        "end_time": end_date
    }
    # Make the request
    response = requests.get(endpoint, headers=headers, params=params)

    # Check the rate limit headers
    rate_limit_remaining = response.headers.get("x-rate-limit-remaining")
    rate_limit_reset = response.headers.get("x-rate-limit-reset")

    # If the rate limit has been exceeded, wait until the rate limit resets
    if rate_limit_remaining and int(rate_limit_remaining) == 0:
        reset_time = int(rate_limit_reset)
        current_time = int(time.time())
        wait_time = reset_time - current_time
        time.sleep(wait_time)
        continue

    if response.status_code == 200:
        # Get the tweets
        tweets = response.json()['data']
        # Iterate over the tweets and process them as needed
        for tweet in tweets:
            print(tweet)
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

# Convert the response to a pandas dataframe


