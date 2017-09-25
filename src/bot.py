import tweepy
from secrets import *
import requests
from bs4 import BeautifulSoup

# Create OAuthHandler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_key, access_secret)

#Construct API instance
api = tweepy.API(auth)

public_tweets = api.home_timeline()

#Prints the tweets that are public
for tweet in public_tweets:
    print(tweet.text)

class TweetStreamer(tweepy.StreamListener):
    
    #New status 
    def on_status(self, status):
        username = status.user.screen_name
        status_id = status.id

        print("Works")

movie_bot = TweetStreamer()
stream = tweepy.Stream(auth, movie_bot)
stream.filter(track=['bot_username'])
