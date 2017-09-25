import tweepy
from secrets import *
from requests import get
from bs4 import BeautifulSoup
import datetime

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def find_id(title):
    base_url = 'http://www.imdb.com/search/title?release_date=' + str(datetime.datetime.now().year) + "&title="

    #add title to the search
    parts = title.split()
    
    url_title = ""

    for t in parts:
        url_title += ("%20" + t)

    url = base_url + url_title

    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    movie_container = html_soup.find_all('div', {"class" : "lister-item mode-advanced"})

    #Assume that the top search is the best and most accurate
    top_search = movie_container[0]
    
    title_id = str(top_search.find("h3", {"class" : "lister-item-header"}).find("a"))
    return(title_id[(title_id.index("/title/") + len("/title/")) : title_id.index("/?")])

def find_schedule(zipcode, title_id):
    base_url = "http://www.imdb.com/showtimes/title/" 

    url = base_url + str(title_id) + "/US/" + str(zipcode)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    theater_container = html_soup.find_all('div' , {'class' : 'list detail'})

    top_search = theater_container[0].find_all('div')
    theater = top_search[0].find('span', {'itemprop' : 'name'}).next
    showtime = str(top_search[0].find('div', {'class' : 'showtimes'})).split()
    print(showtime)

#Override streamer
class TweetStreamer(tweepy.StreamListener):
    
    #New status 
    def on_status(self, status):

        username = status.user.screen_name
        status_id = status.id

        msg = "@%s hey what's up" % (username)
        api.update_status(msg)


#movie_bot = TweetStreamer()
#stream = tweepy.Stream(auth, movie_bot)
#stream.filter(track=['bot_username'])

def StartStream():
    stream_listener = TweetStreamer()
    twitter_stream = tweepy.Stream(auth, stream_listener)
    twitter_stream.filter(track=[bot_username])

if __name__ == '__main__':

    find_schedule(11364,find_id("American Made"))
