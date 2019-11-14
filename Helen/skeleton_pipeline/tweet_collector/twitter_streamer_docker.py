#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 13:47:10 2019

@author: hcamphausen
"""

from config import cfg
import json

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from pymongo import MongoClient

import time


client = MongoClient('mongodb')
db=client.twitter

def authenticate():

    """ Function used for handling twitter authentication.
        Please fill in your keys and tokens """

    auth = OAuthHandler(cfg['CONSUMER_API_KEY'], cfg['CONSUMER_API_SECRET'])
    auth.set_access_token(cfg['ACCESS_TOKEN'], cfg['ACCESS_TOKEN_SECRET'])
    return auth

#def write_tweet(tweet_dict):
#
#    df = pd.DataFrame(index = [1], data=tweet_dict)
#
#    with open('test.csv', 'a') as f:
#        df.to_csv(f, mode='a', header=f.tell()==0)
#
##    df.to_csv('test.csv', mode='a', header=None)


def load_into_mongo(tweet_dict):
    
    """ create mongo database and collection"""

    db.trump_tweets.insert(tweet_dict)


class TwitterStreamer(StreamListener):

    def on_data(self, data):

        """ Whatever we put in this method defines what is donw with every single tweet as it is intercepted
            in real-time. It loads the json into a mongodb """

        tweet = json.loads(data)
        print(len(tweet))
        
        if 'text' in tweet.keys():
            
            if 'extended_tweet' in tweet:
                text = tweet['extended_tweet']['full_text']
            else:
                text = tweet['text']
    
            if not tweet['text'].startswith('RT') and text != '':
                
                tweet_dict = {'created_at': tweet['created_at'],
                         'id': tweet['id_str'],
                         'text': text,
                         'username': tweet['user']['screen_name'],
                         'followers':tweet['user']['followers_count'],
                         'retweets': tweet['retweet_count'],
                         'location': tweet['user']['location'],
                         'raw' : tweet,
                         'timestamp' : time.asctime()}
        
                load_into_mongo(tweet_dict)
                print('tweet_uploaded')

               
    def on_error(self,status):

        """ If rate-limiting occurs """
        if status == 420:
            print(status)
            return False


if __name__ == '__main__':

    """ The following code should be run only when I type
        'python twitter_streamer.py' in the terminal """

    # 1. Autheicate ourselves
    auth = authenticate()

    # 2. Instansiate our TwitterStreamer
    streamer = TwitterStreamer()

    # 3. Wrap the 2 variables into a Stream object to actually
    # start the stream

    stream= Stream(auth, streamer)

    stream.filter(track = ['Trump'],languages = ['en'])
