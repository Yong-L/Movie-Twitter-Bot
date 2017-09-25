import tweepy
from secrets import *
import requests
from bs4 import BeautifulSoup

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#Override streamer
class TweetStreamer(tweepy.StreamListener):
    
    #New status 
    def on_status(self, status):
        print(status.text)

#movie_bot = TweetStreamer()
#stream = tweepy.Stream(auth, movie_bot)
#stream.filter(track=['bot_username'])

if __name__ == '__main__':
    stream_listener = TweetStreamer()
    twitter_stream = tweepy.Stream(auth, stream_listener)
    twitter_stream.filter(track=['yongsulee000'])
