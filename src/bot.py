import tweepy
from secrets import *
from requests import get
from bs4 import BeautifulSoup
import datetime

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def find_id(title):
    url = "http://www.imdb.com/find?ref_=nv_sr_fn&q="

    #add title to the search
    parts = title.split()

    for t in parts:
        url += (t + "+")

    url += str(datetime.datetime.now().year)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    
    try: 
        findSection = html_soup.find('table', {'class' : 'findList'}).find_all('tr')
        tt_id = str(findSection[0].find('a'))
        return(tt_id[tt_id.find("/title/") + len("/title/") : tt_id.rfind("/?")])
    except (TypeError, KeyError) as e:
        return("Movie not found")

def find_schedule(zipcode, title_id):
    base_url = "http://www.imdb.com/showtimes/title/" 

    url = base_url + str(title_id) + "/US/" + str(zipcode)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    theater_container = html_soup.find_all('div' , {'class' : 'list detail'})

    top_search = theater_container[0].find_all('div')
    theater = str(top_search[0].find('span', {'itemprop' : 'name'}).next) 

    new_url = str(top_search[0].find('div' , {'class' : 'fav_box'}).find('a', {'itemprop' :
        'url'})) 
    url = "http://www.imdb.com" + new_url[new_url.find("href=") + len("href=") + 1 :
            new_url.find("itemprop") - 1]

    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    
    title_container = html_soup.find('div', {'class' : 'list detail'}).find('div').find_all('div', {'itemtype' : 'http://schema.org/Movie'})
    
    showtimes = None

    for t in title_container:

        if title_id in str(t.find('div', {'class' : 'image'}).find('a')):
            print("This works")
            showtimes = t.find('div', {'class' : 'showtimes'}).find_all('a')
            for s in showtimes:
                if "Tickets" not in str(s.next):
                    theater += " | " + str(s.next)

    return theater

def read_mention(mention):
    title = mention[mention.find(' ') + 1 : mention.rfind(' ')]  
    zipcode = mention.split()[-1] 

    return title, zipcode

def tweet_showtimes(showtimes, username, status_id):
    
    api.update_status(status='@{} {}'.format(username, showtimes))

#Override streamer
class TweetStreamer(tweepy.StreamListener):
    
    #New status 
    def on_status(self, status):

        username = status.user.screen_name
        status_id = status.id

        title, zipcode = read_mention(status.text)

        title_id = find_id(title)
        showtimes = find_schedule(zipcode, title_id) 

        tweet_showtimes(showtimes, username, status_id)

def StartStream():
    stream_listener = TweetStreamer()
    twitter_stream = tweepy.Stream(auth, stream_listener)
    twitter_stream.filter(track=[bot_username])

if __name__ == '__main__':
    StartStream()
