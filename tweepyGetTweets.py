from __future__ import print_function
from datetime import datetime
from pytz import timezone
import pytz
import tweepy
import json
from pymongo import MongoClient

date_format='%m/%d/%Y %H:%M:%S %Z'
date = datetime.now(tz=pytz.timezone('US/Pacific'))
print("****************************************************************")
print("***** Get Tweet Program Starts at", date.strftime(date_format), "*****")
print("****************************************************************")

MONGO_HOST= 'mongodb://localhost/twitterdb'
WORDS = ['BTC', 'Ethereum', 'blockchain', 'Bitcoin', 'ETH']

twitterSecrets = {}
with open('../twitterSecrets.json') as json_data:
	twitterSecrets = json.load(json_data)
	print("Twitter Secrets: ", twitterSecrets)

CONSUMER_KEY = twitterSecrets['CONSUMER_KEY']
CONSUMER_SECRET = twitterSecrets["CONSUMER_SECRET"]
ACCESS_TOKEN = twitterSecrets["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = twitterSecrets["ACCESS_TOKEN_SECRET"]

db = MongoClient(MONGO_HOST).twitterdb
total_counter = 0

class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 
    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        db.twitter_error.insert({'status_code': repr(status_code)})
        return False

    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            #grab the 'created_at' data from the Tweet to use for display
            #created_at = datajson['created_at']

            #print out a message to the screen that we have collected a tweet
            #print("Tweet collected at " + str(created_at))

            #insert the data into the mongoDB into a collection called twitter_search
            #if twitter_search doesn't exist, it will be created.
            db.twitter_search.insert(datajson)
        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.

listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)
