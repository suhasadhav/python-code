######################################################
# Title: Auto retweet from particular handles or hashtags
# File: generateInsta.py
# Author: Suhas Adhav
# Date: 18 April 2021
######################################################
import tweepy
import settings
import random

# Authenticate to Twitter
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
# Create API object
api = tweepy.API(auth)
TWEET_COUNT = 0

def rt(api, id):
    global TWEET_COUNT
    if TWEET_COUNT < settings.MAX_TWEETS:
        try:
            api.retweet(id)
            print("Retweeting: " + str(id))
            TWEET_COUNT = TWEET_COUNT + 1
        except:
            print("Already Retweeted: "+ str(id))
    else:
        print("Exiting Program Max Reached")
        exit()
    

for handle in settings.RT_HANDLES:
    tweets = api.user_timeline(id=handle, count=3)
    for tweet in tweets:
        if TWEET_COUNT < settings.MAX_TWEETS:
            rt(api, tweet.id)
        else:
            exit()