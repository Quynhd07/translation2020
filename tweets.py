import os 
# import tweepy objects
import tweepy
# sys module provides info about contraints, functions, methods of interpreter
import sys
from collections import Counter 
from datetime import datetime, date, time, timedelta

consumer_key = os.getenv('translation_consumer_key')
consumer_secret = os.getenv('translation_consumer_secret')
access_token = os.getenv('translation_access_token')
access_token_secret = os.getenv('translation_access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# create list of handlers of leading candidates

account_list = ['JoeBiden', 'BernieSanders', 'realDonaldTrump','MikeBloomberg', 'ElizabethWarren', 'TulsiGabbard']

# iterate through list of candidates and pass into tweepy's API.get_user()
for candidate in account_list:
    candidate_info = api.get_user(candidate)
    print("name: " + candidate_info.name)
    print("screen_name: " + candidate_info.screen_name)
    print("description: " + candidate_info.description)
    print("statuses_count: " + str(candidate_info.statuses_count))
    print("friends_count: " + str(candidate_info.friends_count))
    print("followers_count: " + str(candidate_info.followers_count))

